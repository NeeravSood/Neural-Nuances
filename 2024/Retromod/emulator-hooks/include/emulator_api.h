#ifndef EMULATOR_API_H
#define EMULATOR_API_H

#include <string>
#include <vector>
#include <memory>
#include <mutex>
#include <functional>
#include <stdexcept>

// Structure to hold texture data
struct Texture {
    unsigned int width = 0;
    unsigned int height = 0;
    std::shared_ptr<std::vector<unsigned char>> data;  // Use shared_ptr for automatic memory management

    Texture() : data(std::make_shared<std::vector<unsigned char>>()) {}
    Texture(unsigned int w, unsigned int h) : width(w), height(h), data(std::make_shared<std::vector<unsigned char>>(w * h * 4)) {}
};

// Structure to hold audio data
struct AudioData {
    std::vector<float> samples;  // Interleaved audio samples
    unsigned int sample_rate = 0;
    unsigned int channels = 0;

    AudioData() = default;
    AudioData(unsigned int rate, unsigned int ch, size_t sampleCount)
        : sample_rate(rate), channels(ch), samples(sampleCount) {}
};

// Exception class for emulator errors
class EmulatorException : public std::runtime_error {
public:
    explicit EmulatorException(const std::string& message)
        : std::runtime_error("Emulator Error: " + message) {}
};

// Memory management for resources
template <typename T>
class ResourcePool {
public:
    std::shared_ptr<T> acquire() {
        std::lock_guard<std::mutex> lock(pool_mutex);
        if (!pool.empty()) {
            auto res = pool.back();
            pool.pop_back();
            return res;
        }
        return std::make_shared<T>();
    }

    void release(std::shared_ptr<T> resource) {
        std::lock_guard<std::mutex> lock(pool_mutex);
        pool.push_back(resource);
    }

private:
    std::vector<std::shared_ptr<T>> pool;
    std::mutex pool_mutex;
};

ResourcePool<Texture> texturePool;
ResourcePool<AudioData> audioPool;

// Emulator API functions
bool initialize_emulator(const std::string& emulator_name, const std::string& config_file = "");
bool load_game(const std::string& game_path);
void run_game_loop(std::function<void()> custom_update = nullptr);
void shutdown_emulator();

// Rendering API
Texture get_current_frame_texture();
void render_texture(const Texture& texture);

// Audio Handling API
AudioData get_current_audio_data();
void play_audio(const AudioData& audio_data);

// Input Handling API
void register_input_callback(std::function<void(const InputEvent&)> callback);

// Advanced Rendering Options
void apply_shader_to_texture(Texture& texture, const std::string& shader_code);

// State Management API
bool save_state(const std::string& save_path);
bool load_state(const std::string& save_path);

#endif // EMULATOR_API_H
