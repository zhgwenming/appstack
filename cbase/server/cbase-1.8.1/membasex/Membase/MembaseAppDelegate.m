//
//  MembaseAppDelegate.m
//  Membase
//
//  Created by Dustin Sallings on 3/22/11.
//  Copyright 2011 NorthScale. All rights reserved.
//

#import "MembaseAppDelegate.h"

#define MIN_LIFETIME 10
#define FORCEKILL_INTERVAL 15.0

@implementation MembaseAppDelegate

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification
{
    // Insert code here to initialize your application
}

-(void)applicationWillTerminate:(NSNotification *)notification
{
    NSLog(@"Terminating.");
}

- (NSApplicationTerminateReply)applicationShouldTerminate:(NSApplication *)sender {
    BOOL isRunning = [task isRunning];
    shuttingDown = YES;
    NSLog(@"Asked if we should terminate with%s task running.", isRunning ? "" : "out");
    if (isRunning) {
        [self stopTask];
    }
    return isRunning ? NSTerminateCancel : NSTerminateNow;
}

-(void)teardown:(id)sender {
    shuttingDown = YES;
    NSImage *statusIcon = [NSImage imageNamed:@"Couchbase-Status-shutdown-bw.png"];
    [statusBar setImage: statusIcon];
    [self stopTask];
}

-(void)applicationWillFinishLaunching:(NSNotification *)notification
{
//	SUUpdater *updater = [SUUpdater sharedUpdater];
//	SUUpdaterDelegate *updaterDelegate = [[SUUpdaterDelegate alloc] init];
//	[updater setDelegate: updaterDelegate];
}

- (IBAction)showAboutPanel:(id)sender {
    [NSApp activateIgnoringOtherApps:YES];
    [[NSApplication sharedApplication] orderFrontStandardAboutPanel:sender];
}

-(void)awakeFromNib
{
    hasSeenStart = NO;
    shuttingDown = NO;
    
    [[NSUserDefaults standardUserDefaults]
     registerDefaults: [NSDictionary dictionaryWithObjectsAndKeys:
                        [NSNumber numberWithBool:YES], @"browseAtStart", nil, nil]];
    NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
    
    statusBar=[[NSStatusBar systemStatusBar] statusItemWithLength: 30.0];
    NSImage *statusIcon = [NSImage imageNamed:@"Couchbase-Status-bw.png"];
    [statusBar setImage: statusIcon];
    [statusBar setMenu: statusMenu];
    [statusBar setEnabled:YES];
    [statusBar setHighlightMode:YES];
    [statusBar retain];
    
    
    [launchBrowserItem setState:([defaults boolForKey:@"browseAtStart"] ? NSOnState : NSOffState)];
    [self updateAddItemButtonState];
    
	[self launchMembase];
}

-(IBAction)start:(id)sender
{
    if([task isRunning]) {
        [self stopTask];
        return;
    } 
    
    [self launchMembase];
}

-(void)killTask {
    NSLog(@"Force terminating task");
    [task terminate];
}

-(void)stopTask
{
    if (taskKiller) {
        return; // Already shutting down.
    }
    NSFileHandle *writer;
    writer = [in fileHandleForWriting];
    [writer writeData:[@"q().\n" dataUsingEncoding:NSASCIIStringEncoding]];
    [writer closeFile];
    taskKiller = [NSTimer scheduledTimerWithTimeInterval:FORCEKILL_INTERVAL
                                                  target:self
                                                selector:@selector(killTask)
                                                userInfo:nil
                                                 repeats:NO];
}

/* found at http://www.cocoadev.com/index.pl?ApplicationSupportFolder */
- (NSString *)applicationSupportFolder:(NSString*)appName {
    NSString *applicationSupportFolder = nil;
    FSRef foundRef;
    OSErr err = FSFindFolder(kUserDomain, kApplicationSupportFolderType, kDontCreateFolder, &foundRef);
    if (err == noErr) {
        unsigned char path[PATH_MAX];
        OSStatus validPath = FSRefMakePath(&foundRef, path, sizeof(path));
        if (validPath == noErr) {
            applicationSupportFolder = [[NSFileManager defaultManager] stringWithFileSystemRepresentation:(const char*)path
                                                                                                   length:(NSUInteger)strlen((char*)path)];
        }
    }
	applicationSupportFolder = [applicationSupportFolder stringByAppendingPathComponent:appName];
    return applicationSupportFolder;
}

- (NSString *)applicationSupportFolder {
    return [self applicationSupportFolder:@"Couchbase"];
}

-(void)mkdirP:(NSString *)p {
    if(![[NSFileManager defaultManager] fileExistsAtPath:p]) {
		[[NSFileManager defaultManager] createDirectoryAtPath:p withIntermediateDirectories:YES attributes:nil error:NULL];
	}
}

-(void)updateConfig
{
	// determine data dir
    NSFileManager *fileManager = [NSFileManager defaultManager];

	NSString *appSupport = [self applicationSupportFolder];
    NSLog(@"App support dir:  %@", appSupport);
    assert(appSupport);
	// create if it doesn't exist
    [self mkdirP:[appSupport stringByAppendingPathComponent:@"data"]];
    [self mkdirP:[appSupport stringByAppendingPathComponent:@"priv"]];
    [self mkdirP:[appSupport stringByAppendingPathComponent:@"config"]];
    [self mkdirP:[appSupport stringByAppendingPathComponent:@"logs"]];
    [self mkdirP:[appSupport stringByAppendingPathComponent:@"mnesia"]];
    [self mkdirP:[appSupport stringByAppendingPathComponent:@"tmp"]];

    NSString *initSqlProto = [[NSBundle mainBundle] pathForResource:@"init" ofType:@"sql"];
    NSString *initSql = [appSupport stringByAppendingPathComponent:@"priv/init.sql"];

    if(![fileManager fileExistsAtPath:initSql]) {
        assert([fileManager fileExistsAtPath:initSqlProto]);
        [fileManager copyItemAtPath:initSqlProto
                             toPath:initSql
                              error:nil];
    }

    NSString *conf = [NSString stringWithFormat:@"{directory, \"%@\"}.\n", appSupport, nil];
    assert(conf);
    NSLog(@"Config:  %@", conf);

	// if data dirs are not set in local.ini
	NSMutableString *confFile = [[NSMutableString alloc] init];
    assert(confFile);
	[confFile appendString:[[NSBundle mainBundle] resourcePath]];
	[confFile appendString:@"/couchbase-core/priv/config"];
    NSLog(@"Config file:  %@", confFile);

    // Fix up the packaged data dir
    NSString *dataDir = [appSupport stringByAppendingPathComponent:@"data"];
    NSString *appDataDir = [[[NSBundle mainBundle] resourcePath]
                            stringByAppendingPathComponent:@"couchbase-core/data"];
    if ([fileManager fileExistsAtPath:appDataDir]) {
        [fileManager removeItemAtPath:appDataDir error:nil];
    }
    [fileManager createSymbolicLinkAtPath:appDataDir withDestinationPath:dataDir error:nil];

    [conf writeToFile:confFile atomically:YES encoding:NSUTF8StringEncoding error:NULL];
	[confFile release];
	// done
}

-(void)launchMembase
{
    [self updateConfig];

	in = [[NSPipe alloc] init];
	out = [[NSPipe alloc] init];
	task = [[NSTask alloc] init];
    
    startTime = time(NULL);

	NSMutableString *launchPath = [[NSMutableString alloc] init];
	[launchPath appendString:[[NSBundle mainBundle] resourcePath]];
	[launchPath appendString:@"/couchbase-core"];
	[task setCurrentDirectoryPath:launchPath];

    NSString *cmd = [launchPath stringByAppendingString:@"/start.sh"];

    NSString *pathStr = [launchPath stringByAppendingString:@"/bin"];
    pathStr = [pathStr stringByAppendingString:@":/bin:/usr/bin"];

    NSDictionary *env = [NSDictionary dictionaryWithObjectsAndKeys:
                         pathStr, @"PATH",
                         NSHomeDirectory(), @"HOME",
                         nil, nil];

    NSLog(@"Launching '%@' in '%@'", cmd, launchPath);
    [task setLaunchPath:cmd];
    [task setEnvironment:env];
	[task setStandardInput:in];
	[task setStandardOutput:out];
    
	NSFileHandle *fh = [out fileHandleForReading];
	NSNotificationCenter *nc;
	nc = [NSNotificationCenter defaultCenter];
    
	[nc addObserver:self
           selector:@selector(dataReady:)
               name:NSFileHandleReadCompletionNotification
             object:fh];
	
	[nc addObserver:self
           selector:@selector(taskTerminated:)
               name:NSTaskDidTerminateNotification
             object:task];
    
  	[task launch];
  	[fh readInBackgroundAndNotify];
}

-(void)taskTerminated:(NSNotification *)note
{
    NSLog(@"Terminated with status %d", [[note object] terminationStatus]);
    [self cleanup];

    if (shuttingDown) {
        [NSApp terminate:self];
    } else {
        time_t now = time(NULL);
        if (now - startTime < MIN_LIFETIME) {
            NSInteger b = NSRunAlertPanel(@"Problem Running Couchbase",
                                          @"Couchbase doesn't seem to be operating properly.  "
                                          @"Check Console logs for more details.", @"Retry", @"Quit", nil);
            if (b == NSAlertAlternateReturn) {
                [NSApp terminate:self];
            }
        }

        [NSTimer scheduledTimerWithTimeInterval:1.0
                                         target:self selector:@selector(launchMembase)
                                       userInfo:nil
                                        repeats:NO];
    }
}

-(void)cleanup
{
    // Cancel our timer (may or may not have run).
    [taskKiller invalidate];
    taskKiller = nil;

    [task release];
    task = nil;
    
    [in release];
    in = nil;
    [out release];
    out = nil;
    
    [[NSNotificationCenter defaultCenter] removeObserver:self];
}

-(void)openGUI
{
	NSDictionary *info = [[NSBundle mainBundle] infoDictionary];
	NSString *homePage = [info objectForKey:@"HomePage"];
    NSURL *url=[NSURL URLWithString:homePage];
    [[NSWorkspace sharedWorkspace] openURL:url];
}

-(IBAction)browse:(id)sender
{
	[self openGUI];
}

- (void)appendData:(NSData *)d
{
    NSString *s = [[NSString alloc] initWithData: d
                                        encoding: NSUTF8StringEncoding];
    
    if (!hasSeenStart) {
        if ([s rangeOfString:@"Couchbase Server has started on web port 8091"].location != NSNotFound) {
            NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
            if ([defaults boolForKey:@"browseAtStart"]) {
                [self openGUI];
            }
            hasSeenStart = YES;
        }
    }
    
    NSLog(@"%@", s);
}

- (void)dataReady:(NSNotification *)n
{
    NSData *d;
    d = [[n userInfo] valueForKey:NSFileHandleNotificationDataItem];
    if ([d length]) {
        [self appendData:d];
    }
    if (task)
        [[out fileHandleForReading] readInBackgroundAndNotify];
}

-(IBAction)setLaunchPref:(id)sender {
    
    NSCellStateValue stateVal = [sender state];
    stateVal = (stateVal == NSOnState) ? NSOffState : NSOnState;
    
    NSLog(@"Setting launch pref to %s", stateVal == NSOnState ? "on" : "off");
    
    [[NSUserDefaults standardUserDefaults]
     setBool:(stateVal == NSOnState)
     forKey:@"browseAtStart"];
    
    [launchBrowserItem setState:([[NSUserDefaults standardUserDefaults]
                                  boolForKey:@"browseAtStart"] ? NSOnState : NSOffState)];
    
    [[NSUserDefaults standardUserDefaults] synchronize];
}

-(void) updateAddItemButtonState {
    [launchAtStartupItem setState:[loginItems inLoginItems] ? NSOnState : NSOffState];
}

-(IBAction)changeLoginItems:(id)sender {
    if([sender state] == NSOffState) {
        [loginItems addToLoginItems:self];
    } else {
        [loginItems removeLoginItem:self];
    }
    [self updateAddItemButtonState];
}

-(IBAction)showTechSupport:(id)sender {
    NSDictionary *info = [[NSBundle mainBundle] infoDictionary];
	NSString *homePage = [info objectForKey:@"SupportPage"];
    NSURL *url=[NSURL URLWithString:homePage];
    [[NSWorkspace sharedWorkspace] openURL:url];
    
}

@end
