#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
#include <cstdint>
#include "chacha20.hpp"  // Include the header for ChaCha20

// Function to XOR input file with keystream and write to output
void xorFiles(const std::string& inputFile, const std::string& outputFile, ChaCha20& cipher) {
    std::ifstream inFile(inputFile, std::ios::binary);
    std::ofstream outFile(outputFile, std::ios::binary);

    if (!inFile.is_open() || !outFile.is_open()) {
        throw std::runtime_error("Error opening files.");
    }

    std::vector<uint8_t> buffer(64);      // Keystream block
    std::vector<uint8_t> fileBuffer(64);  // Input file buffer

    while (inFile.read(reinterpret_cast<char*>(fileBuffer.data()), 64) || inFile.gcount() > 0) {
        size_t bytesRead = inFile.gcount();

        cipher.generateBlock(buffer);

        for (size_t i = 0; i < bytesRead; ++i) {
            fileBuffer[i] ^= buffer[i];
        }

        outFile.write(reinterpret_cast<char*>(fileBuffer.data()), bytesRead);
    }
}

// Function to print first ChaCha20 keystream block in hex
void printChaChaBlock(const std::string& keyFile, const std::string& nonceFile) {
    std::ifstream keyIn(keyFile, std::ios::binary);
    std::vector<uint8_t> key(32);
    keyIn.read(reinterpret_cast<char*>(key.data()), 32);
    if (!keyIn || keyIn.gcount() != 32) {
        std::cerr << "Error: key file must contain exactly 32 bytes." << std::endl;
        return;
    }

    std::ifstream nonceIn(nonceFile, std::ios::binary);
    std::vector<uint8_t> nonce(12);
    nonceIn.read(reinterpret_cast<char*>(nonce.data()), 12);
    if (!nonceIn || nonceIn.gcount() != 12) {
        std::cerr << "Error: nonce file must contain exactly 12 bytes." << std::endl;
        return;
    }

    ChaCha20 cipher(key, nonce, 0);
    std::vector<uint8_t> block(64);
    cipher.generateBlock(block);

    std::cout << "ChaCha20 Block (64 bytes):" << std::endl;
    for (size_t i = 0; i < block.size(); ++i) {
        std::cout << std::hex << std::setw(2) << std::setfill('0')
                  << static_cast<int>(block[i]) << ((i % 16 == 15) ? "\n" : " ");
    }
    std::cout << std::dec; // restore default
}

int main(int argc, char* argv[]) {
    if (argc == 3) {
        printChaChaBlock(argv[1], argv[2]);
        return 0;
    }

    if (argc == 4) {
        std::string keyFile = argv[1];
        std::string nonceFile = argv[2];
        std::string inputFile = argv[3];

        std::ifstream keyIn(keyFile, std::ios::binary);
        std::vector<uint8_t> key(32);
        keyIn.read(reinterpret_cast<char*>(key.data()), 32);
        if (!keyIn || keyIn.gcount() != 32) {
            std::cerr << "Error: key file must contain exactly 32 bytes." << std::endl;
            return 1;
        }

        std::ifstream nonceIn(nonceFile, std::ios::binary);
        std::vector<uint8_t> nonce(12);
        nonceIn.read(reinterpret_cast<char*>(nonce.data()), 12);
        if (!nonceIn || nonceIn.gcount() != 12) {
            std::cerr << "Error: nonce file must contain exactly 12 bytes." << std::endl;
            return 1;
        }

        ChaCha20 cipher(key, nonce, 0);
        xorFiles(inputFile, "output.txt", cipher);
        std::cout << "Operation complete. Output saved to 'output.txt'." << std::endl;
        return 0;
    }

    std::cerr << "Usage:\n"
              << "  " << argv[0] << " <key_file> <nonce_file> <input_file>\n"
              << "  " << argv[0] << " <key_file> <nonce_file>\n";
    return 1;
}

