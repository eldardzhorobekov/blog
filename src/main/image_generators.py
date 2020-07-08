from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFit

formats = 'jpeg png webp'.split()
sizes = '1000 650 325'.split()
# It's important to write sizes from higher to lower !
# Because some browsers don't support <srcset> by default
# So they choose the first appeared image.

for sz in sizes:
    for fm in formats:
        class ImageClass(ImageSpec):
            processors = [ResizeToFit(sz)]
            format = fm
            options = {'quality': 90}

        register.generator('main:thumbnail_%s_%s' % (fm, sz), ImageClass)
