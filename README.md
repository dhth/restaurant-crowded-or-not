This is a simple image classifier based on Resnet-34 architecture, served as an API via Starlette.

This approach is based on learnings from a fast.ai MOOC that will be publicly available in Jan 2019.

Deployment approach is inspired by [@simonw](https://github.com/simonw)'s [repo](https://github.com/simonw/cougar-or-not).
 
The classifier uses a pre-trained resnet-34 (trained on imagenet) re-trained on a dataset of 500 images.
