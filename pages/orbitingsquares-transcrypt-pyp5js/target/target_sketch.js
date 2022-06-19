// Transcrypt'ed from Python, 2022-02-26 21:36:45
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, all, any, assert, bool, bytearray, bytes, callable, chr, deepcopy, delattr, dict, dir, divmod, enumerate, getattr, hasattr, isinstance, issubclass, len, list, object, ord, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, set, setattr, sorted, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {ADD, ALT, ARROW, AUDIO, AUTO, AXES, BACKSPACE, BASELINE, BEVEL, BEZIER, BLEND, BLUR, BOLD, BOLDITALIC, BOTTOM, BURN, CENTER, CHORD, CLAMP, CLOSE, CONTROL, CORNER, CORNERS, CROSS, CURVE, DARKEST, DEGREES, DEG_TO_RAD, DELETE, DIFFERENCE, DILATE, DODGE, DOWN_ARROW, ENTER, ERODE, ESCAPE, EXCLUSION, FILL, GRAY, GRID, HALF_PI, HAND, HARD_LIGHT, HSB, HSL, IMAGE, IMMEDIATE, INVERT, ITALIC, LANDSCAPE, LEFT, LEFT_ARROW, LIGHTEST, LINEAR, LINES, LINE_LOOP, LINE_STRIP, MIRROR, MITER, MOVE, MULTIPLY, NEAREST, NORMAL, OPAQUE, OPEN, OPTION, OVERLAY, P2D, PI, PIE, POINTS, PORTRAIT, POSTERIZE, PROJECT, PVector, QUADRATIC, QUADS, QUAD_STRIP, QUARTER_PI, RADIANS, RADIUS, RAD_TO_DEG, REPEAT, REPLACE, RETURN, RGB, RIGHT, RIGHT_ARROW, ROUND, SCREEN, SHIFT, SOFT_LIGHT, SQUARE, STROKE, SUBTRACT, TAB, TAU, TEXT, TEXTURE, THRESHOLD, TOP, TRIANGLES, TRIANGLE_FAN, TRIANGLE_STRIP, TWO_PI, UP_ARROW, VIDEO, WAIT, WEBGL, _CTX_MIDDLE, _DEFAULT_FILL, _DEFAULT_LEADMULT, _DEFAULT_STROKE, _DEFAULT_TEXT_FILL, _P5_INSTANCE, abs, accelerationX, accelerationY, accelerationZ, acos, add_library, alpha, ambientLight, ambientMaterial, angleMode, append, applyMatrix, arc, arrayCopy, asin, atan, atan2, background, beginContour, beginShape, bezier, bezierDetail, bezierPoint, bezierTangent, bezierVertex, blend, blendMode, blue, boolean, box, brightness, byte, camera, ceil, changed, char, circle, color, colorMode, concat, cone, constrain, copy, cos, createA, createAudio, createButton, createCamera, createCanvas, createCapture, createCheckbox, createColorPicker, createDiv, createElement, createFileInput, createGraphics, createImage, createImg, createInput, createNumberDict, createP, createRadio, createSelect, createShader, createSlider, createSpan, createStringDict, createVector, createVideo, createWriter, cursor, curve, curveDetail, curvePoint, curveTangent, curveTightness, curveVertex, cylinder, day, debugMode, degrees, deviceOrientation, directionalLight, disableFriendlyErrors, displayDensity, displayHeight, displayWidth, dist, ellipse, ellipseMode, ellipsoid, endContour, endShape, erase, exp, fill, filter, float, floor, focused, frameCount, frameRate, fullscreen, getURL, getURLParams, getURLPath, global_p5_injection, green, height, hex, hour, httpDo, httpGet, httpPost, hue, image, imageMode, image_proxy, input, int, join, key, keyCode, keyIsPressed, lerp, lerpColor, lightness, lights, line, loadBytes, loadFont, loadImage, loadJSON, loadModel, loadPixels, loadShader, loadStrings, loadTable, loadXML, log, logOnloaded, loop, mag, map, match, matchAll, max, millis, min, minute, model, month, mouseButton, mouseIsPressed, mouseX, mouseY, nf, nfc, nfp, nfs, noCanvas, noCursor, noDebugMode, noErase, noFill, noLoop, noSmooth, noStroke, noTint, noise, noiseDetail, noiseSeed, norm, normalMaterial, orbitControl, ortho, pAccelerationX, pAccelerationY, pAccelerationZ, pRotationX, pRotationY, pRotationZ, perspective, pixelDensity, pixels, plane, pmouseX, pmouseY, point, pointLight, popMatrix, popStyle, pow, pre_draw, push, pushMatrix, pushStyle, pwinMouseX, pwinMouseY, py_clear, py_get, py_pop, py_set, py_sort, py_split, quad, quadraticVertex, radians, random, randomGaussian, randomSeed, rect, rectMode, red, redraw, remove, removeElements, resetMatrix, resetShader, resizeCanvas, reverse, rotate, rotateX, rotateY, rotateZ, rotationX, rotationY, rotationZ, round, saturation, save, saveCanvas, saveFrames, saveJSON, saveStrings, saveTable, scale, second, select, selectAll, setAttributes, setCamera, setMoveThreshold, setShakeThreshold, shader, shearX, shearY, shininess, shorten, shuffle, sin, size, smooth, specularMaterial, sphere, splice, splitTokens, sq, sqrt, square, start_p5, str, stroke, strokeCap, strokeJoin, strokeWeight, subset, tan, text, textAlign, textAscent, textDescent, textFont, textLeading, textSize, textStyle, textWidth, texture, textureMode, textureWrap, tint, torus, touches, translate, triangle, trim, turnAxis, unchar, unhex, updatePixels, vertex, width, winMouseX, winMouseY, windowHeight, windowWidth, year} from './pyp5js.js';
var __name__ = '__main__';
export var preload = function () {
	if (arguments.length) {
		var __ilastarg0__ = arguments.length - 1;
		if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
			var __allkwargs0__ = arguments [__ilastarg0__--];
			for (var __attrib0__ in __allkwargs0__) {
			}
		}
	}
	else {
	}
	// pass;
};
export var setup = function () {
	if (arguments.length) {
		var __ilastarg0__ = arguments.length - 1;
		if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
			var __allkwargs0__ = arguments [__ilastarg0__--];
			for (var __attrib0__ in __allkwargs0__) {
			}
		}
	}
	else {
	}
	// pass;
};
export var draw = function () {
	if (arguments.length) {
		var __ilastarg0__ = arguments.length - 1;
		if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
			var __allkwargs0__ = arguments [__ilastarg0__--];
			for (var __attrib0__ in __allkwargs0__) {
			}
		}
	}
	else {
	}
	// pass;
};
export var deviceMoved = null;
export var deviceTurned = null;
export var deviceShaken = null;
export var keyPressed = null;
export var keyReleased = null;
export var keyTyped = null;
export var mouseMoved = null;
export var mouseDragged = null;
export var mousePressed = null;
export var mouseReleased = null;
export var mouseClicked = null;
export var doubleClicked = null;
export var mouseWheel = null;
export var touchStarted = null;
export var touchMoved = null;
export var touchEnded = null;
export var windowResized = null;
export var keyIsDown = null;
export var NUM_SQUARES = 100;
export var BLUE = null;
export var DK_BLUE = null;
export var GREEN = null;
export var DK_GREEN = null;
export var squares = null;
export var Square =  __class__ ('Square', [object], {
	__module__: __name__,
	ROTATION_LIMIT: 0.03,
	ROTATION_TOLERANCE: 0.009,
	ORBIT_LIMIT: 0.003,
	ORBIT_TOLERANCE: 0.0001,
	get __init__ () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self._orbit = self._chooseOrbit () + random (0, int (width / 23));
		self._orbit_angle = random (TAU);
		self._position = createVector (cos (self._orbit_angle) * self._orbit, sin (self._orbit_angle) * self._orbit);
		self._size = random (int (width / 30), int (width / 20));
		self._rot_angle = random (TAU);
		self._s_color = color (0);
		self._s_opac = map (self._size, width / 30, width / 20, 150, 200);
		self._f_color = null;
		self._f_opac = map (self._size, width / 30, width / 20, 150, 200);
		self._recolor ();
		self._rot_speed = Square.avoidZero (Square.ROTATION_LIMIT, Square.ROTATION_TOLERANCE);
		self._orbit_speed = Square.avoidZero (Square.ORBIT_LIMIT, Square.ORBIT_TOLERANCE);
	});},
	get avoidZero () {return function (limit, tolerance) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'limit': var limit = __allkwargs0__ [__attrib0__]; break;
						case 'tolerance': var tolerance = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var value = random (-(limit), limit);
		while ((-(tolerance) < value && value < tolerance)) {
			var value = random (-(limit), limit);
			continue;
		}
		return value;
	};},
	get _chooseOrbit () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var chance = random (0, 1);
		if (chance < 0.18) {
			return width / 8;
		}
		else if (chance < 0.5) {
			return width / 4;
		}
		else if (chance < 0.78) {
			return width / 2.46;
		}
		else if (chance < 1.0) {
			return width / 1.7777;
		}
	});},
	get _move () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var x = self._position.x;
		var y = self._position.y;
		self._position.x = x * cos (self._orbit_speed) + y * sin (self._orbit_speed);
		self._position.y = y * cos (self._orbit_speed) - x * sin (self._orbit_speed);
		var orbit_angle = atan2 (self._position.y, self._position.x);
		self._orbit_angle = orbit_angle;
	});},
	get _recolor () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var angle = abs (self._orbit_angle);
		var half_pi = PI / 2;
		if (angle >= half_pi) {
			var shade = map (angle, PI, half_pi, 0, 0.5);
			var this_fill_color = GREEN;
			var other_fill_color = BLUE;
			var this_stroke_color = DK_GREEN;
			var other_stroke_color = DK_BLUE;
		}
		else {
			var shade = map (angle, 0, half_pi, 0, 0.5);
			var this_fill_color = BLUE;
			var other_fill_color = GREEN;
			var this_stroke_color = DK_BLUE;
			var other_stroke_color = DK_GREEN;
		}
		self._f_color = lerpColor (this_fill_color, other_fill_color, shade + random (-(0.02), 0.02));
		self._s_color = lerpColor (this_stroke_color, other_stroke_color, shade + random (-(0.02), 0.02));
	});},
	get draw () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self._move ();
		self._recolor ();
		self._s_color.setAlpha (self._s_opac);
		stroke (self._s_color);
		self._f_color.setAlpha (self._f_opac);
		fill (self._f_color);
		push ();
		translate (self._position.x, self._position.y);
		self._rot_angle += self._rot_speed;
		rotate (self._rot_angle);
		rect (0, 0, self._size, self._size);
		py_pop ();
	});},
	get __str__ () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		return 'Square:\norbit: {}\norbit_angle: {}\nposition: {}\nrot_angle: {}\ns_color: {}\nf_color: {}\nrot_speed: {}\norbit_speed: {}\n'.format (self._orbit, self._orbit_angle, self._position, self._rot_angle, self._s_color, self._f_color, self._rot_speed, self._orbit_speed);
	});}
});
var setup = function () {
	if (arguments.length) {
		var __ilastarg0__ = arguments.length - 1;
		if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
			var __allkwargs0__ = arguments [__ilastarg0__--];
			for (var __attrib0__ in __allkwargs0__) {
			}
		}
	}
	else {
	}
	frameRate (60);
	createCanvas (1280, 720, WEBGL);
	setAttributes ('antialias', true);
	strokeWeight (2);
	rectMode (CENTER);
	background (color (70, 71, 76));
	BLUE = color (21, 21, 235);
	DK_BLUE = color (10, 10, 115);
	GREEN = color (149, 194, 81);
	DK_GREEN = color (57, 74, 31);
	squares = (function () {
		var __accu0__ = [];
		for (var _ = 0; _ < NUM_SQUARES; _++) {
			__accu0__.append (Square ());
		}
		return __accu0__;
	}) ();
};
var draw = function () {
	if (arguments.length) {
		var __ilastarg0__ = arguments.length - 1;
		if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
			var __allkwargs0__ = arguments [__ilastarg0__--];
			for (var __attrib0__ in __allkwargs0__) {
			}
		}
	}
	else {
	}
	background (color (70, 71, 76));
	for (var square of squares) {
		square.draw ();
	}
};
export var event_functions = dict ({'deviceMoved': deviceMoved, 'deviceTurned': deviceTurned, 'deviceShaken': deviceShaken, 'keyPressed': keyPressed, 'keyReleased': keyReleased, 'keyTyped': keyTyped, 'mouseMoved': mouseMoved, 'mouseDragged': mouseDragged, 'mousePressed': mousePressed, 'mouseReleased': mouseReleased, 'mouseClicked': mouseClicked, 'doubleClicked': doubleClicked, 'mouseWheel': mouseWheel, 'touchStarted': touchStarted, 'touchMoved': touchMoved, 'touchEnded': touchEnded, 'windowResized': windowResized, 'keyIsDown': keyIsDown});
start_p5 (preload, setup, draw, event_functions);

//# sourceMappingURL=target_sketch.map