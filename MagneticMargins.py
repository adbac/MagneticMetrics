"""
v.1.003

Observer to make sidebearings magnetic to outline modifications.  
Its aim to be used as a startup script so it can be activated and deactivated whenever you need.

Version history:
    v1.002: first private release
    v1.003: fix magnet multiple drawing

"""

import merz
from merz.tools.drawingTools import NSImageDrawingTools
from mojo.events import extractNSEvent
from mojo.roboFont import CurrentFont
from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber

pressedKey = "M"

class MagneticMetricsSubscriber(Subscriber):
    
    def glyphEditorDidOpen(self, info):

        glyphEditor = info["glyphEditor"]
        self.status = 0

        def magnetSymbolFactory(
                scale=1,
            ):
            bot = NSImageDrawingTools((50 * scale, 50 * scale))
            bot.scale(scale)
            bot.fill(0, 0, 0, .75)
            pen = bot.BezierPath()
            pen.moveTo((25, 15))
            pen.curveTo((20.0, 15.0), (17, 16), (17, 20))
            pen.lineTo((17, 45))
            pen.curveTo((17.0, 48.0), (15, 50), (9, 50))
            pen.curveTo((2, 50), (0, 48.0), (0, 45))
            pen.lineTo((0, 22))
            pen.curveTo((0, 6), (9, 0), (25, 0))
            pen.curveTo((41.0, 0.0), (50, 6), (50, 22))
            pen.lineTo((50, 45))
            pen.curveTo((50, 48), (48, 50), (41, 50))
            pen.curveTo((35, 50), (33, 48), (33, 45))
            pen.lineTo((33, 20))
            pen.curveTo((33, 16), (30, 15), (25, 15))
            pen.closePath()
            bot.drawPath(pen)

            bot.fill(1)
            pen = bot.BezierPath()
            pen.moveTo((25, 3))
            pen.curveTo((11.0, 3), (3, 8), (3, 22))
            pen.lineTo((3, 34))
            pen.lineTo((14, 34))
            pen.lineTo((14, 20))
            pen.curveTo((14.0, 14.0), (18, 12), (25, 12))
            pen.curveTo((32.0, 12.0), (36.0, 14.0), (36, 20))
            pen.lineTo((36, 34))
            pen.lineTo((47, 34))
            pen.lineTo((47, 22))
            pen.curveTo((47, 8), (39, 3), (25, 3))
            pen.closePath()
            bot.drawPath(pen)

            image = bot.getImage()
            return image

        merz.SymbolImageVendor.registerImageFactory("com.adbac.MagneticMargins.magnet", magnetSymbolFactory)

        magnetScale = .3

        self.magnetsLayer = glyphEditor.extensionContainer("com.adbac.MagneticMargins")
        self.magnetsLayer.setVisible(False)
        self.leftMagnet = self.magnetsLayer.appendSymbolSublayer(
            position=(0, 0),
            imageSettings=dict(
                name="com.adbac.MagneticMargins.magnet",
                scale=magnetScale,
            )
        )
        self.rightMagnet = self.magnetsLayer.appendSymbolSublayer(
            position=(0, 0),
            imageSettings=dict(
                name="com.adbac.MagneticMargins.magnet",
                scale=magnetScale,
            )
        )

    def glyphEditorDidKeyDown(self, info):
        event = info["NSEvent"]
        characters = event.characters()
        shiftDown = extractNSEvent(event)["shiftDown"]
        if shiftDown and characters == pressedKey :
            if self.status == 0:
                self.status = 1
                self.updateMagnetsPosition()
                self.magnetsLayer.setVisible(True)
            else:
                self.status = 0
                self.magnetsLayer.setVisible(False)

    def glyphEditorDidSetGlyph(self, info):
        self.glyph = info["glyph"]
        self.leftMargin = self.glyph.leftMargin
        self.rightMargin = self.glyph.rightMargin
        self.updateMagnetsPosition()

    def glyphEditorGlyphDidChangeContours(self, info):
        if self.status == 0:
            self.leftMargin = self.glyph.leftMargin
            self.rightMargin = self.glyph.rightMargin
        # Sends the glyph margins when tool isn’t active
        # so when you activate it the good margins will be used
        if self.status == 1:
            self.glyph.leftMargin = self.leftMargin
            self.glyph.rightMargin = self.rightMargin
            self.updateMagnetsPosition()

    def updateMagnetsPosition(self):
        yPosition = CurrentFont().info.capHeight / 2
        self.leftMagnet.setPosition((0, yPosition))
        self.rightMagnet.setPosition((self.glyph.width, yPosition))

registerGlyphEditorSubscriber(MagneticMetricsSubscriber)