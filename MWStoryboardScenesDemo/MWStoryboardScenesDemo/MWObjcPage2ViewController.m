//
//  MWObjcPage2ViewController.m
//  MSStoryboardScenesDemo
//
//  Created by Waldal, Marius on 15/06/16.
//  Copyright © 2016 Lonely Penguin. All rights reserved.
//

#import "MWObjcPage2ViewController.h"

@interface MWObjcPage2ViewController ()

@end

@implementation MWObjcPage2ViewController

- (void)viewDidLoad {
    [super viewDidLoad];

}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];

}


- (IBAction)returnToPage1:(id)sender {
    [self.presentingViewController dismissViewControllerAnimated:YES completion:nil];
}

@end
