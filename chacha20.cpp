#include "chacha20.hpp"
#include <cstring>
#include <iostream>

// Constructor: initializes the ChaCha20 state based on the key, nonce, and counter
ChaCha20::ChaCha20(const std::vector<uint8_t>& key, const std::vector<uint8_t>& nonce, uint32_t counter) {
    if (key.size() != 32 || nonce.size() != 12) {
        throw std::invalid_argument("Invalid key or nonce size");
    }

    state[0] = 0x61707865; state[1] = 0x3320646e; state[2] = 0x79622d36; state[3] = 0x3c2d0a6e;
    
    // Load the 32-byte key into the state
    for (size_t i = 0; i < 8; ++i) {
        state[4 + i] = (key[i * 4 + 0] << 24) | (key[i * 4 + 1] << 16) | (key[i * 4 + 2] << 8) | key[i * 4 + 3];
    }

    // Initialize counter
    state[12] = (counter >> 24) & 0xFF;
    state[13] = (counter >> 16) & 0xFF;
    state[14] = (counter >> 8) & 0xFF;
    state[15] = counter & 0xFF;

    // Load the 96-bit nonce into the state
    for (size_t i = 0; i < 3; ++i) {
        state[16 + i] = (nonce[i * 4 + 0] << 24) | (nonce[i * 4 + 1] << 16) | (nonce[i * 4 + 2] << 8) | nonce[i * 4 + 3];
    }
}

// Quarter round function for ChaCha20
void ChaCha20::quarterRound(uint32_t& a, uint32_t& b, uint32_t& c, uint32_t& d) {
    a += b; d ^= a; d = (d << 16) | (d >> (32 - 16));
    c += d; b ^= c; b = (b << 12) | (b >> (32 - 12));
    a += b; d ^= a; d = (d << 8) | (d >> (32 - 8));
    c += d; b ^= c; b = (b << 7) | (b >> (32 - 7));
}

// One round of the ChaCha20 algorithm
void ChaCha20::round() {
    for (int i = 0; i < 10; ++i) {
        quarterRound(state[0], state[4], state[8], state[12]);
        quarterRound(state[1], state[5], state[9], state[13]);
        quarterRound(state[2], state[6], state[10], state[14]);
        quarterRound(state[3], state[7], state[11], state[15]);

        quarterRound(state[0], state[5], state[10], state[15]);
        quarterRound(state[1], state[6], state[11], state[12]);
        quarterRound(state[2], state[7], state[8], state[13]);
        quarterRound(state[3], state[4], state[9], state[14]);
    }
}

// Generate one ChaCha20 block (64 bytes of keystream)
void ChaCha20::generateBlock(std::vector<uint8_t>& output) {
    uint32_t originalState[16];
    std::memcpy(originalState, state, sizeof(state));

    // Perform 10 rounds
    for (int i = 0; i < 10; ++i) {
        round();
    }

    // Add the original state back to the state
    for (int i = 0; i < 16; ++i) {
        state[i] += originalState[i];
    }

    // Output the generated keystream to the output vector
    for (int i = 0; i < 16; ++i) {
        output[i * 4 + 0] = (state[i] >> 24) & 0xFF;
        output[i * 4 + 1] = (state[i] >> 16) & 0xFF;
        output[i * 4 + 2] = (state[i] >> 8) & 0xFF;
        output[i * 4 + 3] = state[i] & 0xFF;
    }

    // Increment the counter
    state[12] += 1;
    if (state[12] == 0) {
        state[13] += 1;
    }
}

