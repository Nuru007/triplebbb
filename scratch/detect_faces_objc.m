#import <Foundation/Foundation.h>
#import <CoreImage/CoreImage.h>

void detectFaces(NSString *imageName) {
    NSString *path = [NSString stringWithFormat:@"assets/images/%@", imageName];
    NSURL *imageURL = [NSURL fileURLWithPath:path];
    
    CIImage *image = [CIImage imageWithContentsOfURL:imageURL];
    if (!image) {
        NSLog(@"Could not load image: %@", path);
        return;
    }
    
    // Core Image coordinate system origin is bottom-left
    CGSize size = image.extent.size;
    CGFloat width = size.width;
    CGFloat height = size.height;
    
    CIContext *context = [CIContext contextWithOptions:nil];
    // Create CIDetector for faces with high accuracy
    CIDetector *detector = [CIDetector detectorOfType:CIDetectorTypeFace
                                              context:context
                                              options:@{CIDetectorAccuracy: CIDetectorAccuracyHigh}];
                                              
    NSArray *features = [detector featuresInImage:image];
    
    printf("%s: found %lu faces (dimensions: %dx%d)\n", 
           [imageName UTF8String], 
           (unsigned long)[features count], 
           (int)width, 
           (int)height);
           
    for (int i = 0; i < [features count]; i++) {
        CIFaceFeature *face = features[i];
        CGRect bounds = face.bounds;
        
        // Convert bottom-left coordinates to top-left coordinates
        CGFloat w = bounds.size.width;
        CGFloat h = bounds.size.height;
        CGFloat x = bounds.origin.x;
        CGFloat y = height - (bounds.origin.y + h);
        
        CGFloat centerX = x + w / 2.0;
        CGFloat centerY = y + h / 2.0;
        CGFloat radius = MAX(w, h) * 0.7; // pad to include hair/shoulders
        
        printf("  Face %d: center_x=%d, center_y=%d, radius=%d\n", 
               i + 1, 
               (int)centerX, 
               (int)centerY, 
               (int)radius);
    }
}

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSArray *images = @[
            @"story_founder.jpg",
            @"about_speaker.jpg",
            @"hero_speaker.jpg",
            @"hero_leadership.png",
            @"hero_mentorship.png",
            @"hero_sisterhood.png",
            @"about_gesture.jpg",
            @"hero_workshop.jpg"
        ];
        
        for (NSString *img in images) {
            detectFaces(img);
        }
    }
    return 0;
}
