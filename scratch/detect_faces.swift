import Foundation
import Vision
import AppKit

let imageDir = "assets/images"
let images = [
    "story_founder.jpg",
    "about_speaker.jpg",
    "hero_speaker.jpg",
    "hero_leadership.png",
    "hero_mentorship.png",
    "hero_sisterhood.png",
    "about_gesture.jpg",
    "hero_workshop.jpg"
]

func detectFaces(in imageName: String) {
    let path = "\(imageDir)/\(imageName)"
    guard let image = NSImage(contentsOfFile: path) else {
        print("Could not load image: \(path)")
        return
    }
    
    guard let tiffData = image.tiffRepresentation,
          let imageSource = CGImageSourceCreateWithData(tiffData as CFData, nil),
          let cgImage = CGImageSourceCreateImageAtIndex(imageSource, 0, nil) else {
        print("Could not create CGImage from: \(imageName)")
        return
    }
    
    let width = CGFloat(cgImage.width)
    let height = CGFloat(cgImage.height)
    
    let request = VNDetectFaceRectanglesRequest { (request, error) in
        guard error == nil else {
            print("Face detection error: \(error!)")
            return
        }
        
        guard let results = request.results as? [VNFaceObservation] else {
            return
        }
        
        print("\(imageName): found \(results.count) faces (dimensions: \(Int(width))x\(Int(height)))")
        
        for (index, face) in results.enumerated() {
            let bbox = face.boundingBox
            
            // Vision coordinates are normalized (0 to 1) and origin is bottom-left.
            // Convert to standard pixel coordinates (origin top-left).
            let w = bbox.width * width
            let h = bbox.height * height
            let x = bbox.minX * width
            let y = (1.0 - bbox.maxY) * height
            
            let centerX = x + w / 2.0
            let centerY = y + h / 2.0
            let radius = max(w, h) * 0.7 // add some padding to crop head/hair
            
            print("  Face \(index + 1): center_x=\(Int(centerX)), center_y=\(Int(centerY)), radius=\(Int(radius))")
        }
    }
    
    let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    do {
        try handler.perform([request])
    } catch {
        print("Failed to perform request: \(error)")
    }
}

for img in images {
    detectFaces(in: img)
}
