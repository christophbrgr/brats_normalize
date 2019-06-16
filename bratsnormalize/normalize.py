# -*- coding: UTF-8 -*-
"""Module providing a normalization function to adjust passed mri images 
to the range 0...1 and ensure that the background is 0 as well as that 
no voxel of the brain area has the value 0

"""
__version__ = '0.1'
__author__  = 'Christoph Berger'

import numpy as np
import glob
import own_itk as oitk
import os
import argparse

class bratsNorm():
    thresh = 10
    verbose = False

    def normalize(self, image, mask):
        image = np.multiply(image,mask)
        image = image - image.min()
        image += 0.0001
        image = np.divide(image, image.max())
        image = np.multiply(image, mask)
        return image
    
    def iterate(self, input, output, mask=None):
        '''
        input folder containing an arbitrary number of .nii.gz scans
        set mask to False if your image already has a background value of zero
        if mask is None, this code will attempt to generate a new one based on 
        simple thresholding
        '''
        scans = glob.glob(os.path.join(input,'*.nii*'))
        length = len(scans)
        if self.verbose:
            print('{} files found.'.format(length))
        for scan in scans:
            if self.verbose: 
                print('Current path:{}'.format(scan))
            self.run(scan, output, mask)

    
    def run(self, scan, output, mask=None): 
        img = oitk.get_itk_image(scan)
        image = oitk.get_itk_array(img)
        if mask is None:
            mask = self.generateMask(image, self.thresh)
        if mask is False:
            mask = np.zeros(image.shape)
            mask[image > 0] = 1
        normalized = self.normalize(image, mask)
        oitk.write_itk_image(oitk.make_itk_image(normalized, proto_image=img), os.path.join(output, os.path.split(scan)[1]))
        
    def generateMask(self, image, threshold=10):
        mask = np.zeros(image.shape)
        mask[image > threshold] = 1
        return mask

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input",
                    help="Input folder or input file")
    parser.add_argument("output",
                    help="Output will be written in this folder")
    parser.add_argument("-m", "--mask",
                    help="Optionally provide one mask for all passed files")
    parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
    parser.add_argument("-t", "--threshold",
                    help="Set threshold for crappy masking", type=int)
    args = parser.parse_args()

    # setup everything and assemble variables
    b = bratsNorm()
    if args.verbose:
        b.verbose = True

    if args.threshold:
        b.thresh = args.threshold

    output = os.path.abspath(args.output)
    if args.mask is None: 
        mask = False
    else: 
        mask = oitk.get_itk_array(oitk.get_itk_image(args.mask))

    if os.path.isdir(args.input) is True:
        input = os.path.abspath(args.input)
        b.iterate(input, output, mask)
    else:
        b.run(args.input, output, mask)
    




