#ifndef CHACHA20_HPP
#define CHACHA20_HPP

#include <vector>
#include <cstdint>

class ChaCha20 {
public:
    ChaCha20(const std::vector<uint8_t>& key, const std::vector<uint8_t>& nonce, uint32_t counter = 0);
    void generateBlock(std::vector<uint8_t>& output); // Generate keystream block

private:
    void quarterRound(uint32_t& a, uint32_t& b, uint32_t& c, uint32_t& d);
    void round(); // Perform 1 round of ChaCha20
    void load_state(); // Load the initial state from the key, nonce, and counter

    uint32_t state[16]; // The internal state array
};

#endif // CHACHA20_HPP

