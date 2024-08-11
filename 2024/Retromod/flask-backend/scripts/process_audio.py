import sys
import torch
import torchaudio
import torchaudio.transforms as T

class AudioProcessor:
    def __init__(self, model):
        self.model = model.to(self.get_device())

    def get_device(self):
        """
        Return the device to be used for processing (GPU if available, else CPU).
        """
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def enhance_audio(self, audio_tensor):
        """
        Enhances the audio data using a pre-trained deep learning model.
        Args:
            audio_tensor (torch.Tensor): The raw audio data as a tensor.
        
        Returns:
            torch.Tensor: Enhanced audio data.
        """
        # Ensure the model is in evaluation mode
        self.model.eval()

        # Move the audio tensor to the same device as the model
        audio_tensor = audio_tensor.to(self.get_device())

        # Apply the model for audio enhancement
        with torch.no_grad():
            enhanced_audio = self.model(audio_tensor.unsqueeze(0))  # Add batch dimension

        # Remove batch dimension and move back to CPU
        enhanced_audio = enhanced_audio.squeeze(0).cpu()

        # Normalize the audio to avoid clipping
        enhanced_audio = self.normalize_audio(enhanced_audio)

        return enhanced_audio

    def normalize_audio(self, audio_tensor):
        """
        Normalize the audio tensor to prevent clipping and distortion.
        Args:
            audio_tensor (torch.Tensor): The audio data to normalize.
        
        Returns:
            torch.Tensor: Normalized audio data.
        """
        # Normalize audio to a max value of 1
        return audio_tensor / torch.max(torch.abs(audio_tensor))

def load_audio(file_path):
    """
    Load the audio file into a tensor using torchaudio.
    Args:
        file_path (str): Path to the audio file.
    
    Returns:
        tuple: A tuple containing the audio tensor and the sampling rate.
    """
    try:
        audio_tensor, sample_rate = torchaudio.load(file_path)
        return audio_tensor, sample_rate
    except Exception as e:
        print(f"Error loading audio file: {e}")
        sys.exit(1)

def save_audio(file_path, audio_tensor, sample_rate):
    """
    Save the enhanced audio data back to a file using torchaudio.
    Args:
        file_path (str): Path to save the enhanced audio file.
        audio_tensor (torch.Tensor): The enhanced audio data.
        sample_rate (int): The sampling rate.
    """
    try:
        torchaudio.save(file_path, audio_tensor, sample_rate)
    except Exception as e:
        print(f"Error saving audio file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_audio.py <audio_file_path>")
        sys.exit(1)

    audio_path = sys.argv[1]
    audio_model = torch.load('audio_model.pth', map_location=torch.device('cpu'))  # Load your pre-trained audio model
    processor = AudioProcessor(audio_model)

    audio_tensor, sample_rate = load_audio(audio_path)
    enhanced_audio_tensor = processor.enhance_audio(audio_tensor)
    save_audio(audio_path.replace(".wav", "_enhanced.wav"), enhanced_audio_tensor, sample_rate)
