//
//  ContentView.swift
//  techExploration
//
//  Created by Brian Ozawa Burns on 5/2/24.
//

import SwiftUI
import ARKit
import RealityKit
import SceneKit
import Vision
import GoogleGenerativeAI

struct ContentView : View {
    @State private var screenPosition: CGPoint? = nil
    @State private var backendResponse: String = "backend response will be displayed here..."
    @State private var capturedImage: UIImage?
    @State private var showARView: Bool = false
    @State private var coordinates: [[String: Int]]?
    @State private var objectCoords: [ObjectCoords]?
    
    var body: some View {
        ZStack(alignment: .bottomLeading, content: {
            if showARView {
                HStack {
                    ARViewContainer(screenPosition: screenPosition, capturedImage: $capturedImage, coordinates: $coordinates, objectCoords: $objectCoords)
                                    .edgesIgnoringSafeArea(.all)
                }.onTapGesture {
                    let tapLocation = UIScreen.main.bounds.center
                    screenPosition = tapLocation
                }
                BackendInteractor(backendResponse: $backendResponse, capturedImage: $capturedImage, showARView: $showARView, coordinates: $coordinates, objectCoords: $objectCoords)
            } else {
                UIKitCameraView(capturedImage: $capturedImage).edgesIgnoringSafeArea(.all)
                BackendInteractor(backendResponse: $backendResponse, capturedImage: $capturedImage, showARView: $showARView, coordinates: $coordinates, objectCoords: $objectCoords)
            }
        })
    }
}

struct ARViewContainer: UIViewRepresentable {
    let screenPosition: CGPoint?
    @Binding var capturedImage: UIImage?
    @Binding var coordinates: [[String: Int]]?
    @Binding var objectCoords: [ObjectCoords]?

    func makeUIView(context: Context) -> ARSCNView {
        let sceneView = ARSCNView(frame: .zero)
        sceneView.delegate = context.coordinator

        // configure the AR session
        let configuration = ARWorldTrackingConfiguration()
        configuration.planeDetection = [.horizontal, .vertical]
        sceneView.session.run(configuration)

        return sceneView
    }

    func updateUIView(_ uiView: ARSCNView, context: Context) {
        // perform raycast if screenPosition is provided
        if let screenPosition = screenPosition {
//            context.coordinator.performRaycast(at: screenPosition, in: uiView)
            context.coordinator.performRaycast(screenPosition: screenPosition, uiView: uiView, coordinates: coordinates!, capturedImage: capturedImage)
//            context.coordinator.performRaycast(screenPosition: screenPosition, uiView: uiView, coordinates: coordinates!, capturedImage: capturedImage, objectCoords: objectCoords!)
        }
    }

    func makeCoordinator() -> Coordinator {
        return Coordinator(screenPosition: screenPosition)
    }

    class Coordinator: NSObject, ARSCNViewDelegate {
        let screenPosition: CGPoint?

        init(screenPosition: CGPoint?) {
            self.screenPosition = screenPosition
        }
        
        func performRaycast(screenPosition: CGPoint, uiView: ARSCNView, coordinates: [[String: Int]], capturedImage: UIImage?, objectCoords: [ObjectCoords]) {
            for objectCoord in objectCoords {
                print(objectCoord)
            }
        }
        
        func performRaycast(screenPosition: CGPoint, uiView: ARSCNView, coordinates: [[String: Int]], capturedImage: UIImage?) {
//            let positions = [["x":100, "y":100],["x":200, "y":200],["x":300, "y":300],["x":400, "y":400]]
//            for position in positions {
            for position in coordinates {
//                print(capturedImage!.size.width)
//                print(capturedImage!.size.width)
//                print(capturedImage!.scale)
                
                
                print(position)
//                print(position["x"]!)
//                print(position["y"]!)
//                print(position["width"]!)
//                print(position["height"]!)
//                print()
                print(UIScreen.main.bounds.center)
                print(UIScreen.main.bounds.size)
                let x = Float(position["x"]!)
                let y = Float(position["y"]!)
                let width = Float(position["width"]!)
                let height = Float(position["height"]!)
//                let pos = CGPoint(x: Int(x/width) * Int(UIScreen.main.bounds.width), y: Int(y/height) * Int(UIScreen.main.bounds.height))
                let pos = CGPoint(x: Int(y/height * Float(UIScreen.main.bounds.size.width)), y: Int(x/width * Float(UIScreen.main.bounds.size.height)))
                guard let query = uiView.raycastQuery(from: pos,
                                                      allowing: .existingPlaneInfinite,
                                                      alignment: .any) else {
                    return
                }
                let results = uiView.session.raycast(query)

                if let result = results.first {
                    let intersectionPosition = result.worldTransform.translation

                    // highlight the detected object with a bounding box
                    highlightAt(position: intersectionPosition, in: uiView.scene.rootNode)
                }
            }
        }

//        func performRaycast(at screenPosition: CGPoint, in uiView: ARSCNView) {
//            guard let query = uiView.raycastQuery(from: screenPosition,
//                                                  allowing: .existingPlaneInfinite,
//                                                  alignment: .any) else {
//                return
//            }
//            let results = uiView.session.raycast(query)
//
//            if let result = results.first {
//                let intersectionPosition = result.worldTransform.translation
//
//                // highlight the detected object with a bounding box
//                highlightAt(position: intersectionPosition, in: uiView.scene.rootNode)
//            }
//        }

        func highlightAt(position: SIMD3<Float>, in rootNode: SCNNode) {
            // create a bounding box
            let boundingBox = SCNBox(width: 0.1, height: 0.1, length: 0.1, chamferRadius: 0)
            boundingBox.firstMaterial?.diffuse.contents = UIColor.red.withAlphaComponent(0.8)

            let node = SCNNode(geometry: boundingBox)
            node.position = SCNVector3(position.x, position.y, position.z)

            rootNode.addChildNode(node)

            // box animation
            let scaleUpAction = SCNAction.scale(to: 1.2, duration: 0.2)
            let scaleDownAction = SCNAction.scale(to: 1.0, duration: 0.2)
            let pulseAction = SCNAction.sequence([scaleUpAction, scaleDownAction])
            let repeatPulseAction = SCNAction.repeatForever(pulseAction)
            node.runAction(repeatPulseAction)
        }

        func renderer(_ renderer: SCNSceneRenderer, didAdd node: SCNNode, for anchor: ARAnchor) {
            // empty implementation
        }
    }
}

extension simd_float4x4 {
    var translation: SIMD3<Float> {
        return SIMD3<Float>(columns.3.x, columns.3.y, columns.3.z)
    }
}

extension CGRect {
    var center: CGPoint {
        return CGPoint(x: midX, y: midY)
    }
}

struct UIKitCameraView: UIViewControllerRepresentable {
    @Binding var capturedImage: UIImage?
    
    func makeUIViewController(context: Context) -> UIViewController {
        let viewController = CameraViewController(capturedImage: $capturedImage)
        return viewController
    }

    func updateUIViewController(_ uiViewController: UIViewController, context: Context) {
    }
}

class CameraViewController: UIViewController, AVCapturePhotoCaptureDelegate {
    var captureSession: AVCaptureSession!
    var backCamera: AVCaptureDevice!
    var photoOutput: AVCapturePhotoOutput!
    var previewLayer: AVCaptureVideoPreviewLayer!
    
    @Binding var capturedImage: UIImage?

    init(capturedImage: Binding<UIImage?>) {
        self._capturedImage = capturedImage
        super.init(nibName: nil, bundle: nil)
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    override func viewDidLoad() {
        super.viewDidLoad()

        setupCaptureSession()
        setupPreviewLayer()
        startRunningCaptureSession()
        setupButton()
    }

    func setupCaptureSession() {
        captureSession = AVCaptureSession()

        guard let backCamera = AVCaptureDevice.default(for: AVMediaType.video) else {
            print("Unable to access back camera!")
            return
        }
        self.backCamera = backCamera

        guard let input = try? AVCaptureDeviceInput(device: backCamera) else {
            print("Unable to initialize back camera input!")
            return
        }
        captureSession.addInput(input)

        photoOutput = AVCapturePhotoOutput()
        captureSession.addOutput(photoOutput)
    }

    func setupPreviewLayer() {
        previewLayer = AVCaptureVideoPreviewLayer(session: captureSession)
        previewLayer.videoGravity = AVLayerVideoGravity.resizeAspectFill
        previewLayer.frame = view.bounds
        view.layer.addSublayer(previewLayer)
    }

    func startRunningCaptureSession() {
        captureSession.startRunning()
    }

    func setupButton() {
        let button = UIButton(frame: CGRect(x: 0, y: 0, width: 200, height: 50))
        button.center = CGPoint(x: view.frame.width / 2, y: 4 * view.frame.height / 5) // Adjust the y position here
        button.setTitle("Capture Photo", for: .normal)
        button.addTarget(self, action: #selector(capturePhoto), for: .touchUpInside)
        button.backgroundColor = .blue
        button.layer.cornerRadius = 10
        view.addSubview(button)
    }

    @objc func capturePhoto() {
        let settings = AVCapturePhotoSettings()
        photoOutput.capturePhoto(with: settings, delegate: self)
    }

    func photoOutput(_ output: AVCapturePhotoOutput, didFinishProcessingPhoto photo: AVCapturePhoto, error: Error?) {
        guard let imageData = photo.fileDataRepresentation() else {
            print("Failed to get image data!")
            return
        }

        guard let image = UIImage(data: imageData) else {
            print("Failed to convert image data to UIImage!")
            return
        }

        // Set the captured image
        capturedImage = image
    }
}

struct BackendInteractor : View {
    
    @Binding var backendResponse: String
    @Binding var capturedImage: UIImage?
    @Binding var showARView: Bool
    @Binding var coordinates: [[String: Int]]?
    @Binding var objectCoords: [ObjectCoords]?
    
//    let models = ["gpt4o", "gpt4v", "geminiprov", "geminiflash", "llava"]
    let models = ["gpt4o", "gpt4v", "geminiprov", "geminiflash"]
    
    var body: some View {
        VStack {
            // Gemini Response
            Text(backendResponse)
                .frame(maxWidth: .infinity)
                .padding(20)
                .foregroundStyle(.white)
                .background(.black.opacity(0.8))
            Spacer()
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 20) {
                    ForEach(models, id: \.self) { model in
                        Button(action: {
                            Task {
                                await makeBackendRequest(model: model)
                            }
                        }, label: {
                            Text(model)
                                .padding(20)
                                .foregroundStyle(.white)
                                .background(.blue)
                        })
                    }
                }
            }
            // Textual query (with image)
//            HStack {
//                TextField("Textual query to Gemini...", text: $geminiQuery)
//                    .padding(20)
//                    .textFieldStyle(.roundedBorder)
//                    .onSubmit {
//                        geminiQuery = ""
//                        Task {
//                            await makeBackendRequest()
//                        }
//                    }
//                if !geminiQuery.isEmpty {
//                    Button {
//                        geminiQuery = ""
//                    }label: {
//                        Image(systemName: "multiply.circle.fill")
//                    }
//                    .padding(.trailing, 10)
//                }
//            }
//            .background(.black.opacity(0.8))
        }
    }
    
    func makeBackendRequest(model: String) async {
        let url = URL(string: "https://objects-out-of-place-backend-250025cdb745.herokuapp.com/" + model)!
        
        var imgBody = Data()
        guard let image = capturedImage?.jpegData(compressionQuality: 1.0) else {
            return
        }
        imgBody.append(image.base64EncodedString().data(using: .utf8)!)
        
        var imgRequest = URLRequest(url: url)
        imgRequest.httpMethod = "POST"
        imgRequest.httpBody = imgBody
        
        let imgTask = URLSession.shared.dataTask(with: imgRequest) { data, response, error in
            guard let data = data, error == nil else {
                return
            }
            
//            print("DEBUG: data -\n", data)
//            print("DEBUG: response -\n", response ?? "No response")
            
            do {
                let json = try JSONSerialization.jsonObject(with: data, options: .fragmentsAllowed) as! [String: Any]
                backendResponse = json["description"] as! String
                let centroids = json["centroids"] as! [[String: Int]]
                print(centroids)
                coordinates = centroids
//                let center_points = json["center points"] as! [ObjectCoords]
//                objectCoords = center_points
//                print("center_points:", center_points)
                showARView = true
            } catch let error as NSError {
                print("DEBUG: error in backend call")
                print(error)
            }
        }
        imgTask.resume()
    }
}

struct ObjectCoords {
    var object_name: String
    var centers: [[String: Int]]
}

#Preview {
    ContentView()
}
