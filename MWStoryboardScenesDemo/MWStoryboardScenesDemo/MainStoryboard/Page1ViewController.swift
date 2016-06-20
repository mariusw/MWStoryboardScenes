import UIKit

@objc (MWPage1ViewController)
class Page1ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }

    @IBAction func openPage2(sender: AnyObject) {
        let page2VC = Storyboards.instantiateSwiftPage2()
        self.presentViewController(page2VC, animated:true, completion:nil)
    }

    @IBAction func openObjcPage1(sender: AnyObject) {
        let objcPage1VC = Storyboards.instantiateObjcPage1()
        self.presentViewController(objcPage1VC, animated:true, completion:nil)
        
    }
    
    
}

