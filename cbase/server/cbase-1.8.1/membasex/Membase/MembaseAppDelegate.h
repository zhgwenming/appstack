//
//  MembaseAppDelegate.h
//  Membase
//
//  Created by Dustin Sallings on 3/22/11.
//  Copyright 2011 NorthScale. All rights reserved.
//

#import <Cocoa/Cocoa.h>

#import "LoginItemManager.h"

@interface MembaseAppDelegate : NSObject <NSApplicationDelegate> {
@private
    NSStatusItem *statusBar;
    IBOutlet NSMenu *statusMenu;
    
    IBOutlet NSMenuItem *launchBrowserItem;
    IBOutlet NSMenuItem *launchAtStartupItem;
    IBOutlet LoginItemManager *loginItems;
    
    NSTask *task;
    NSTimer *taskKiller;
    NSPipe *in, *out;
    
    BOOL hasSeenStart;
    time_t startTime;

    BOOL shuttingDown;
}

-(IBAction)start:(id)sender;
-(IBAction)browse:(id)sender;
-(IBAction)teardown:(id)sender;

-(void)launchMembase;
-(void)stopTask;
-(void)openGUI;
-(void)taskTerminated:(NSNotification *)note;
-(void)cleanup;
-(NSString *)applicationSupportFolder;

-(void)updateAddItemButtonState;

-(IBAction)setLaunchPref:(id)sender;
-(IBAction)changeLoginItems:(id)sender;

-(IBAction)showAboutPanel:(id)sender;
-(IBAction)showTechSupport:(id)sender;


@end
