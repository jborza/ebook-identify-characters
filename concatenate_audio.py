import os
import subprocess

def concatenate_audio_files(input_dir, output_file):
    """
    Concatenate all WAV files in the input directory into a single WAV file using ffmpeg.

    :param input_dir: Directory containing the input WAV files (e.g., 1.wav, 2.wav, etc.).
    :param output_file: Path to the output WAV file.
    """
    # Ensure the directory exists
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory {input_dir} does not exist.")

    # Get a list of all .wav files sorted numerically
    wav_files = sorted(
        [f for f in os.listdir(input_dir) if f.endswith(".wav")],
        key=lambda x: int(os.path.splitext(x)[0])
    )

    if not wav_files:
        raise ValueError(f"No WAV files found in directory {input_dir}.")

    # Create a temporary file containing the list of WAV files
    file_list_path = os.path.join(input_dir, "file_list.txt")
    with open(file_list_path, "w") as file_list:
        for wav_file in wav_files:
            file_list.write(f"file '{wav_file}'\n")

    # Use ffmpeg to concatenate the files
    ffmpeg_command = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", file_list_path,
        "-c", "copy",
        output_file
    ]

    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Successfully created {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during ffmpeg execution: {e}")
    finally:
        # Clean up the temporary file list
        if os.path.exists(file_list_path):
            os.remove(file_list_path)


if __name__ == "__main__":
    # Directory containing the WAV files
    input_dir = "output_wavs"

    # Output file name
    output_file = "final_output.wav"

    # Concatenate audio files
    concatenate_audio_files(input_dir, output_file)