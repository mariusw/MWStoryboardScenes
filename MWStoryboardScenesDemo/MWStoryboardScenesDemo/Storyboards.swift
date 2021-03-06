/* Generated by 'MWStoryboardScenes' script as part of a Run Script Build Phase. Changes WILL BE OVERWRITTEN */

import UIKit


// MARK: -  Storyboard identifier enums

enum MainStoryboardIdentifier: String {
    case SwiftPage2 = "swiftPage2"
    case SwiftPage1 = "swiftPage1"

}

enum ObjcStoryboardIdentifier: String {
    case ObjcPage1 = "objcPage1"
    case ObjcPage2 = "objcPage2"

}

public class Storyboards: NSObject {

    // MARK: - Instantiators for MainStoryboard-- */

    static func instantiateSwiftPage2() -> Page2ViewController {
        return self.mainStoryboard.instantiateViewControllerWithIdentifier(MainStoryboardIdentifier.SwiftPage2.rawValue) as! Page2ViewController
    }

    static func instantiateSwiftPage1() -> Page1ViewController {
        return self.mainStoryboard.instantiateViewControllerWithIdentifier(MainStoryboardIdentifier.SwiftPage1.rawValue) as! Page1ViewController
    }

    // MARK: - Instantiators for ObjcStoryboard-- */

    static func instantiateObjcPage1() -> MWObjcPage1ViewController {
        return self.objcStoryboard.instantiateViewControllerWithIdentifier(ObjcStoryboardIdentifier.ObjcPage1.rawValue) as! MWObjcPage1ViewController
    }

    static func instantiateObjcPage2() -> MWObjcPage2ViewController {
        return self.objcStoryboard.instantiateViewControllerWithIdentifier(ObjcStoryboardIdentifier.ObjcPage2.rawValue) as! MWObjcPage2ViewController
    }

    // MARK: -  Private storyboard initializers

    private static var mainStoryboard : UIStoryboard {
        let identifier = UIDevice.currentDevice().userInterfaceIdiom == .Pad ? "MainStoryboard_iPad" : "MainStoryboard_iPhone"
        return UIStoryboard(name: identifier, bundle: nil)
    }

    private static var objcStoryboard : UIStoryboard {
        let identifier = UIDevice.currentDevice().userInterfaceIdiom == .Pad ? "ObjcStoryboard_iPad" : "ObjcStoryboard_iPhone"
        return UIStoryboard(name: identifier, bundle: nil)
    }

}

