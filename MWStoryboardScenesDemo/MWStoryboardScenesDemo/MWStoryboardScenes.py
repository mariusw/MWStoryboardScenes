#!/usr/bin/env python

import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

DEBUG = False

CONFIG_OPTIONS = {"MainStoryboard":
                      {"iphone": "MainStoryboard_iPhone",
                       "ipad": "MainStoryboard_iPad"},
                  "ObjcStoryboard":
                      {"iphone": "ObjcStoryboard_iPhone",
                       "ipad": "ObjcStoryboard_iPad"}}
PREFIX = "MW"
STORYBOARD_IDENTIFIER = "storyboardIdentifier"
CUSTOM_CLASS = "customClass"

INDENT = "    "
APP_ROOT_DIRECTORY = os.environ["SRCROOT"]
EXCLUDE_STORYBOARDS_SWIFT = []
EXCLUDE_STORYBOARDS_OBJC = []

if DEBUG:
    STORYBOARD_FILEPATHS = \
        ["/Users/the/full/path/to/your/app/MainStoryboard/MainStoryboard_iPhone.storyboard",
         "/Users/the/full/path/to/your/app/MainStoryboard/MainStoryboard_iPad.storyboard",
         "/Users/the/full/path/to/your/app/ObjcStoryboard/ObjcStoryboard_iPhone.storyboard",
         "/Users/the/full/path/to/your/app/ObjcStoryboard/ObjcStoryboard_iPad.storyboard"]
else:
    STORYBOARD_FILEPATHS = \
        [APP_ROOT_DIRECTORY + "/MWStoryboardScenesDemo/MainStoryboard/MainStoryboard_iPhone.storyboard",
         APP_ROOT_DIRECTORY + "/MWStoryboardScenesDemo/MainStoryboard/MainStoryboard_iPad.storyboard",
         APP_ROOT_DIRECTORY + "/MWStoryboardScenesDemo/ObjcStoryboard/ObjcStoryboard_iPhone.storyboard",
         APP_ROOT_DIRECTORY + "/MWStoryboardScenesDemo/ObjcStoryboard/ObjcStoryboard_iPad.storyboard"]


def process_storyboard(storyboard_file):
    """Parses the storyboard and stores all identifiers and custom class names in a dictionary for later use"""
    view_controllers = {}
    tree = ET.parse(storyboard_file)
    root = tree.getroot()

    for controller in root.findall(".//*[@" + STORYBOARD_IDENTIFIER + "]"):
        controller_identifier = controller.get(STORYBOARD_IDENTIFIER)
        controller_class = controller.get(CUSTOM_CLASS)
        if controller_identifier is None:
            continue

        view_controllers[controller_identifier] = controller_class
    return view_controllers


def remove_special_chars(value):
    return ''.join(e for e in value if e.isalnum())


def initial_lowercase(s):
    return s if len(s) == 0 else s[0].lower() + s[1:]


def initial_uppercase(s):
    return s if len(s) == 0 else s[0].upper() + s[1:]


def prepare_identifier(s):
    return remove_special_chars(initial_uppercase(s))


def has_prefix(s):
    return False if s is None else s.startswith(PREFIX)


def ensure_prefix(s):
    return s if has_prefix(s) else PREFIX + s


def remove_prefix(s):
    return s[len(PREFIX):] if has_prefix(s) else s


def check_for_duplicates(thelist):
    seen = set()
    for x in thelist:
        if x in seen:
            raise ImportError("Duplicate identifiers detected: (" + x + ")")
        seen.add(x)


def merge_dicts(iphonecontrollers, ipadcontrollers):
    """Add ipad controllers to the iphone controllers dict, but never overwrite a custom controller with None!"""
    all_controllers = iphonecontrollers.copy()
    for identifier, customclass in ipadcontrollers.items():
        if all_controllers.get(identifier) is None:
            all_controllers[identifier] = customclass
    return all_controllers


def match_config_with_filepaths(configopts, filepaths):
    allopts = {}
    for storyboard, opts in configopts.items():
        storyboardopts = {}
        for device, filename in opts.items():
            # match filename with path
            device_filepath = [s for s in filepaths if filename in s]

            # Add filename and  path to dict
            storyboardopts[device] = {filename: device_filepath}
            filepaths.remove(device_filepath[0])

        allopts[storyboard] = storyboardopts

    return allopts


def prefix_filename(s):
    path, filename = os.path.split(s)
    return path + "/" + PREFIX + filename


def collect_header_filenames():
    all_headers = set()
    for _, _, filenames in os.walk(APP_ROOT_DIRECTORY):
        for filename in filenames:
            if filename.endswith(".h"):
                all_headers.add(filename)

    return all_headers


def prepare_for_generation():
    all_storyboard_names = {}
    storyboard_controllers = {}
    all_iphone_identifiers = []
    all_ipad_identifiers = []
    all_iphone_classnames = []
    all_ipad_classnames = []

    # Read storyboard filenames from script settings
    options = match_config_with_filepaths(CONFIG_OPTIONS, STORYBOARD_FILEPATHS)

    for storyboard, storyboardopts in options.items():
        # Get the storyboard names
        iphone_storyboardname = storyboardopts["iphone"].keys()[0]
        ipad_storyboardname = storyboardopts["ipad"].keys()[0]
        all_storyboard_names[storyboard] = {"iphone": iphone_storyboardname, "ipad": ipad_storyboardname}

        # Get the storyboard file names
        iphone_storyboard = storyboardopts["iphone"].values()[0][0]
        ipad_storyboard = storyboardopts["ipad"].values()[0][0]

        # Parse storyboard files to collect all view controllers
        iphone_viewcontrollers = process_storyboard(iphone_storyboard)
        ipad_viewcontrollers = process_storyboard(ipad_storyboard)

        # Merge the dicts containing the view controllers
        all_viewcontrollers = merge_dicts(iphone_viewcontrollers, ipad_viewcontrollers)
        storyboard_controllers[storyboard] = all_viewcontrollers

        # Add all identifiers to list, so duplicates can be detected
        all_iphone_identifiers.extend(iphone_viewcontrollers.keys())
        all_ipad_identifiers.extend((ipad_viewcontrollers.keys()))

        # Add all class names to list, so filenames can be checked
        all_iphone_classnames.extend(iphone_viewcontrollers.values())
        all_ipad_classnames.extend(ipad_viewcontrollers.values())

    # Raise an ImportError if script finds duplicate identifiers!
    check_for_duplicates(all_iphone_identifiers)
    check_for_duplicates(all_ipad_identifiers)

    return storyboard_controllers, all_storyboard_names, options


def create_storyboards_header(opts, allstoryboardnames, storyboardcontrollers, all_headers):
    filepath = "FINStoryboards" if DEBUG else prefix_filename(os.environ["SCRIPT_OUTPUT_FILE_0"])
    mainclassname = os.path.basename(filepath)
    with open(filepath + ".h", "w") as headerFile:
        headerFile.write(
                "/* Generated by 'MWStoryboardScenes' script as part of a Run Script Build Phase. Changes WILL BE OVERWRITTEN */\n\n")
        headerFile.write("#import <Foundation/Foundation.h>\n")

        # Imports
        for storyboard, controllers in storyboardcontrollers.items():
            if storyboard in EXCLUDE_STORYBOARDS_OBJC:
                continue  # Skip generation for this storyboard

            for identifier, classname in controllers.items():
                if classname is not None:
                    if classname + ".h" in all_headers:
                        headerFile.write("#import \"" + classname + ".h\"\n")

        headerFile.write("\n")

        # Forward declarations for Swift classes
        for storyboard, controllers in storyboardcontrollers.items():
            if storyboard in EXCLUDE_STORYBOARDS_OBJC:
                continue  # Skip generation for this storyboard

            for identifier, classname in controllers.items():
                if classname is not None:
                    if classname + ".h" not in all_headers:
                        headerFile.write("@class " + ensure_prefix(classname) + ";\n")

        # Class definition
        headerFile.write("\n\n")
        headerFile.write("@interface " + mainclassname + " : NSObject\n")

        # Method declarations
        for storyboard, controllers in storyboardcontrollers.items():
            if storyboard in EXCLUDE_STORYBOARDS_OBJC:
                continue  # Skip generation for this storyboard

            headerFile.write("\n\n/* -- " + storyboard + " controllers -- */ \n\n")
            for identifier, classname in controllers.items():
                finalclassname = "UIViewController" if classname is None else ensure_prefix(classname)
                headerFile.write("+ (" + finalclassname + " *)instantiate" + initial_uppercase(identifier) + ";\n")

        headerFile.write("\n@end")


def create_storyboards_implementations(opts, storyboardcontrollers, all_headers):
    filepath = "FINStoryboards" if DEBUG else prefix_filename(os.environ["SCRIPT_OUTPUT_FILE_0"])
    mainclassname = os.path.basename(filepath)
    with open(filepath + ".m", "w") as implementationFile:
        implementationFile.write(
                "/* Generated by 'MWStoryboardScenes' script as part of a Run Script Build Phase. Changes WILL BE OVERWRITTEN */\n\n")
        implementationFile.write("#import \"" + mainclassname + ".h\"\n\n\n")
        implementationFile.write("@implementation " + mainclassname + "\n")

        # Class methods
        for storyboard, controllers in storyboardcontrollers.items():
            if storyboard in EXCLUDE_STORYBOARDS_OBJC:
                continue  # Skip generation for this storyboard

            implementationFile.write("\n#pragma mark -  " + storyboard + " instantiators\n\n")
            for identifier, controller_classname in controllers.items():
                finalclassname = "UIViewController" if controller_classname is None else ensure_prefix(
                        controller_classname)
                implementationFile.write(
                        "+ (" + finalclassname + " *)instantiate" + initial_uppercase(identifier + " {\n"))
                if finalclassname + ".h" in all_headers:
                    implementationFile.write(
                            INDENT + "return [[" + mainclassname + " " + storyboard + "] instantiateViewControllerWithIdentifier:@\"" + identifier + "\"];\n")
                else:
                    implementationFile.write(
                            INDENT + "return (" + finalclassname + " *)[[" + mainclassname + " " + storyboard + "] instantiateViewControllerWithIdentifier:@\"" + identifier + "\"];\n")
                implementationFile.write("}\n\n")

        # Storyboard initializers
        implementationFile.write("\n#pragma mark - Private storyboard initializers\n\n")
        for storyboard in storyboardcontrollers.keys():
            if storyboard in EXCLUDE_STORYBOARDS_OBJC:
                continue  # Skip generation for this storyboard

            implementationFile.write("+ (UIStoryboard *)" + storyboard + " {\n")
            implementationFile.write(
                    INDENT + "NSString *identifier = UI_USER_INTERFACE_IDIOM() == UIUserInterfaceIdiomPad ? @\"" + storyboard + "_iPad\" : @\"" + storyboard + "_iPhone\";\n")
            implementationFile.write(INDENT + "return [UIStoryboard storyboardWithName:identifier bundle:nil];\n")
            implementationFile.write("}\n\n")

        implementationFile.write("\n@end")


def create_swift_storyboard_enums(thefile, opts, vcs):
    thefile.write("\n// MARK: -  Storyboard identifier enums\n\n")

    for sbname, viewcontrollers in vcs.items():
        if sbname in EXCLUDE_STORYBOARDS_SWIFT:
            continue  # Skip generation for this storyboard

        enumname = sbname + "Identifier"
        thefile.write("enum " + enumname + ": String {\n")

        # cases for all view controllers
        for identifier in viewcontrollers.keys():
            thefile.write(INDENT + "case " + initial_uppercase(identifier) + " = \"" + identifier + "\"\n")

        thefile.write("\n")

        # Close enum
        thefile.write("}\n\n")


def create_swift_storyboard_class(thefile, sb_names, sb_controllers, all_headers):
    thefile.write("public class Storyboards: NSObject {\n\n")

    # Storyboard instantiators
    for sbname, controllers in sb_controllers.items():
        if sbname in EXCLUDE_STORYBOARDS_SWIFT:
            continue  # Skip generation for this storyboard

        enumname = sbname + "Identifier"
        thefile.write(INDENT + "// MARK: - Instantiators for " + sbname + "-- */\n\n")

        for identifier, customclass in controllers.items():
            classname = customclass if customclass is not None else "UIViewController"

            # Remove prefix from Swift names
            if "Menubar" in classname:
                print classname

            if classname + ".h" not in all_headers:
                classname = remove_prefix(classname)

            functionname = prepare_identifier(identifier)
            castclass = "" if classname == "UIViewController" else " as! " + classname
            thefile.write(INDENT * 1 + "static func instantiate" + functionname + "() -> " + classname + " {\n")
            thefile.write(INDENT * 2 +
                          "return self." + initial_lowercase(sbname) + ".instantiateViewControllerWithIdentifier(" +
                          enumname + "." + initial_uppercase(identifier) + ".rawValue)" + castclass + "\n")
            thefile.write(INDENT * 1 + "}\n\n")

    # Storyboard initializers
    thefile.write(INDENT + "// MARK: -  Private storyboard initializers\n\n")
    for sbname, device_sbnames in sb_names.items():
        thefile.write(INDENT + "private static var " + initial_lowercase(sbname) + " : UIStoryboard {\n")
        thefile.write(
                INDENT * 2 + "let identifier = UIDevice.currentDevice().userInterfaceIdiom == .Pad ? \"" + device_sbnames.get(
                        "ipad") + "\" : \"" + device_sbnames.get("iphone") + "\"\n")
        thefile.write(INDENT * 2 + "return UIStoryboard(name: identifier, bundle: nil)\n")
        thefile.write(INDENT + "}\n\n")

    thefile.write("}\n\n")


def create_swift_storyboards_file(opts, allstoryboardnames, storyboardcontrollers, all_headers):
    filename = "Storyboards.swift" if DEBUG else os.environ["SCRIPT_OUTPUT_FILE_0"]
    with open(filename + ".swift", "w") as storyboardsFile:
        storyboardsFile.write(
                "/* Generated by 'MWStoryboardScenes' script as part of a Run Script Build Phase. Changes WILL BE OVERWRITTEN */\n\n")
        storyboardsFile.write("import UIKit\n\n")

        # Create identifier enums
        create_swift_storyboard_enums(storyboardsFile, opts, storyboardcontrollers)
        create_swift_storyboard_class(storyboardsFile, allstoryboardnames, storyboardcontrollers, all_headers)


def main():
    storyboard_controllers, all_storyboard_names, options = prepare_for_generation()

    # Collect all header files in project
    all_headers = collect_header_filenames()

    # Objc generation
    create_storyboards_header(options, all_storyboard_names, storyboard_controllers, all_headers)
    create_storyboards_implementations(options, storyboard_controllers, all_headers)

    # Swift generation
    create_swift_storyboards_file(options, all_storyboard_names, storyboard_controllers, all_headers)


if __name__ == "__main__":
    main()