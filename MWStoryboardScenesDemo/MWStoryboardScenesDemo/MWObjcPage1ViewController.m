//
//  MWObjcPage1ViewController.m
//  MSStoryboardScenesDemo
//
//  Created by Waldal, Marius on 15/06/16.
//  Copyright © 2016 Lonely Penguin. All rights reserved.
//

#import "MWObjcPage1ViewController.h"
#import "MWObjcPage2ViewController.h"
#import "MWStoryboards.h"
#import "MWStoryboardScenesDemo-Swift.h"

@interface MWObjcPage1ViewController ()

@end

@implementation MWObjcPage1ViewController

- (void)viewDidLoad {
    [super viewDidLoad];

}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];

}

- (IBAction)openPage2:(id)sender {
    MWObjcPage2ViewController *page2VC = [MWStoryboards instantiateObjcPage2];
    [self presentViewController:page2VC animated:YES completion:NULL];
    
}

- (IBAction)openSwiftPage1:(id)sender {
    MWPage1ViewController *swiftPage1VC = [MWStoryboards instantiateSwiftPage1];
    [self presentViewController:swiftPage1VC animated:YES completion:NULL];
}

@end
