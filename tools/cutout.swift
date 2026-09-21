import Vision
import AppKit
import CoreImage
let a = CommandLine.arguments
let url = URL(fileURLWithPath: a[1])
let handler = VNImageRequestHandler(url: url, options: [:])
let req = VNGenerateForegroundInstanceMaskRequest()
do {
  try handler.perform([req])
  guard let obs = req.results?.first else { print("no result"); exit(1) }
  let buf = try obs.generateMaskedImage(ofInstances: obs.allInstances, from: handler, croppedToInstancesExtent: true)
  let ci = CIImage(cvPixelBuffer: buf)
  let ctx = CIContext()
  let cs = CGColorSpace(name: CGColorSpace.sRGB)!
  let data = ctx.pngRepresentation(of: ci, format: .RGBA8, colorSpace: cs, options: [:])!
  try data.write(to: URL(fileURLWithPath: a[2]))
  print("ok", a[2])
} catch { print("err", error) }
