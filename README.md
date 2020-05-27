# Super-Resolution-image-GAN
This project aims to recover or restore high resolution image from low resolution image by applying deep neural network with adversarial network (Generative Adversarial Networks). The main target is to reconstruct super resolution image or high resolution image by up-scaling low resolution image such that texture detail in the reconstructed super resolution image is not lost. This has numerous applications like satellite and aerial image analysis, medical image processing, compressed image/video enhancement etc. The implementation revolves around GAN which is a deep neural network architectures comprised of two networks (Generator and Discriminator) pitting one against the other (thus the “adversarial”) whose main focus is to generate data from scratch.
# Usage
Network.py : Contains Generator and Discriminator Network Utils.py   : Contains utilities to process images
Utils_model.py : Contains optimizer and content loss code
train.py   : Used for training the model
test.py    : To test the model
