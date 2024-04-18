import os
import pygame

base_img_path = "Graphics/player/"


def load_image(path):
    """
    Loads an image from the specified path, converts it to have an alpha channel, and sets its color key.

    :param path: The path to the image file, relative to the base image directory.
    :return: A Pygame Surface object with the loaded image.
    """
    img = pygame.image.load(base_img_path + path).convert_alpha()
    return img


def load_images(path):
    """
    Loads all images in a specified directory, sorted alphabetically.

    :param path: The path to the directory containing image files, relative to the base image directory.
    :return: A list of Pygame Surface objects of the loaded images.
    """

    images = []
    for img_name in sorted(os.listdir(base_img_path + path)):
        images.append(load_image(path + "/" + img_name))
    return images


class Animation:
    """
    Manages an animation sequence from a list of images, with control over the frame duration and looping behavior.

    :param images: A list of Pygame Surface objects that make up the animation frames.
    :param img_dur: The duration of each frame in the animation in game frames, defaults to 5.
    :param loop: A boolean that determines whether the animation should loop or play once, defaults to True.
    """

    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.img_duration = img_dur
        self.loop = loop
        # Indicates whether the animation is finished
        # (useful for non-looping animations)
        self.done = False
        self.frame = 0  # The current frame index

    def copy(self):
        """
        Creates a copy of this Animation object, allowing for independent animation sequences using the same frames.

        :return: A new instance of Animation with the same images, duration, and looping behavior.
        """
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        """
        Updates the animation frame, advancing it or looping it depending on the configuration.
        """
        if self.loop:
            self.frame = (self.frame + 1) % (
                self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1,
                             self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        """
        Retrieves the current image of the animation based on the current frame index.

        :return: The Pygame Surface object of the current frame.
        """
        return self.images[int(self.frame / self.img_duration)]
