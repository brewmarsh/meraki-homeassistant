var d0 = Object.defineProperty;
var p0 = (e, t, n) => t in e ? d0(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var Go = (e, t, n) => (p0(e, typeof t != "symbol" ? t + "" : t, n), n);
function m0(e, t) {
  for (var n = 0; n < t.length; n++) {
    const r = t[n];
    if (typeof r != "string" && !Array.isArray(r)) {
      for (const o in r)
        if (o !== "default" && !(o in e)) {
          const i = Object.getOwnPropertyDescriptor(r, o);
          i && Object.defineProperty(e, o, i.get ? i : {
            enumerable: !0,
            get: () => r[o]
          });
        }
    }
  }
  return Object.freeze(Object.defineProperty(e, Symbol.toStringTag, { value: "Module" }));
}
function Nd(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
function Gt(e) {
  if (e.__esModule)
    return e;
  var t = e.default;
  if (typeof t == "function") {
    var n = function r() {
      return this instanceof r ? Reflect.construct(t, arguments, this.constructor) : t.apply(this, arguments);
    };
    n.prototype = t.prototype;
  } else
    n = {};
  return Object.defineProperty(n, "__esModule", { value: !0 }), Object.keys(e).forEach(function(r) {
    var o = Object.getOwnPropertyDescriptor(e, r);
    Object.defineProperty(n, r, o.get ? o : {
      enumerable: !0,
      get: function() {
        return e[r];
      }
    });
  }), n;
}
var zd = { exports: {} }, cl = {}, Ld = { exports: {} }, D = {};
/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var No = Symbol.for("react.element"), h0 = Symbol.for("react.portal"), g0 = Symbol.for("react.fragment"), y0 = Symbol.for("react.strict_mode"), v0 = Symbol.for("react.profiler"), x0 = Symbol.for("react.provider"), S0 = Symbol.for("react.context"), w0 = Symbol.for("react.forward_ref"), k0 = Symbol.for("react.suspense"), C0 = Symbol.for("react.memo"), E0 = Symbol.for("react.lazy"), Ec = Symbol.iterator;
function _0(e) {
  return e === null || typeof e != "object" ? null : (e = Ec && e[Ec] || e["@@iterator"], typeof e == "function" ? e : null);
}
var jd = { isMounted: function() {
  return !1;
}, enqueueForceUpdate: function() {
}, enqueueReplaceState: function() {
}, enqueueSetState: function() {
} }, Id = Object.assign, Ad = {};
function Cr(e, t, n) {
  this.props = e, this.context = t, this.refs = Ad, this.updater = n || jd;
}
Cr.prototype.isReactComponent = {};
Cr.prototype.setState = function(e, t) {
  if (typeof e != "object" && typeof e != "function" && e != null)
    throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
  this.updater.enqueueSetState(this, e, t, "setState");
};
Cr.prototype.forceUpdate = function(e) {
  this.updater.enqueueForceUpdate(this, e, "forceUpdate");
};
function bd() {
}
bd.prototype = Cr.prototype;
function qa(e, t, n) {
  this.props = e, this.context = t, this.refs = Ad, this.updater = n || jd;
}
var Ja = qa.prototype = new bd();
Ja.constructor = qa;
Id(Ja, Cr.prototype);
Ja.isPureReactComponent = !0;
var _c = Array.isArray, Dd = Object.prototype.hasOwnProperty, eu = { current: null }, Fd = { key: !0, ref: !0, __self: !0, __source: !0 };
function Bd(e, t, n) {
  var r, o = {}, i = null, l = null;
  if (t != null)
    for (r in t.ref !== void 0 && (l = t.ref), t.key !== void 0 && (i = "" + t.key), t)
      Dd.call(t, r) && !Fd.hasOwnProperty(r) && (o[r] = t[r]);
  var s = arguments.length - 2;
  if (s === 1)
    o.children = n;
  else if (1 < s) {
    for (var a = Array(s), u = 0; u < s; u++)
      a[u] = arguments[u + 2];
    o.children = a;
  }
  if (e && e.defaultProps)
    for (r in s = e.defaultProps, s)
      o[r] === void 0 && (o[r] = s[r]);
  return { $$typeof: No, type: e, key: i, ref: l, props: o, _owner: eu.current };
}
function $0(e, t) {
  return { $$typeof: No, type: e.type, key: t, ref: e.ref, props: e.props, _owner: e._owner };
}
function tu(e) {
  return typeof e == "object" && e !== null && e.$$typeof === No;
}
function P0(e) {
  var t = { "=": "=0", ":": "=2" };
  return "$" + e.replace(/[=:]/g, function(n) {
    return t[n];
  });
}
var $c = /\/+/g;
function fs(e, t) {
  return typeof e == "object" && e !== null && e.key != null ? P0("" + e.key) : t.toString(36);
}
function hi(e, t, n, r, o) {
  var i = typeof e;
  (i === "undefined" || i === "boolean") && (e = null);
  var l = !1;
  if (e === null)
    l = !0;
  else
    switch (i) {
      case "string":
      case "number":
        l = !0;
        break;
      case "object":
        switch (e.$$typeof) {
          case No:
          case h0:
            l = !0;
        }
    }
  if (l)
    return l = e, o = o(l), e = r === "" ? "." + fs(l, 0) : r, _c(o) ? (n = "", e != null && (n = e.replace($c, "$&/") + "/"), hi(o, t, n, "", function(u) {
      return u;
    })) : o != null && (tu(o) && (o = $0(o, n + (!o.key || l && l.key === o.key ? "" : ("" + o.key).replace($c, "$&/") + "/") + e)), t.push(o)), 1;
  if (l = 0, r = r === "" ? "." : r + ":", _c(e))
    for (var s = 0; s < e.length; s++) {
      i = e[s];
      var a = r + fs(i, s);
      l += hi(i, t, n, a, o);
    }
  else if (a = _0(e), typeof a == "function")
    for (e = a.call(e), s = 0; !(i = e.next()).done; )
      i = i.value, a = r + fs(i, s++), l += hi(i, t, n, a, o);
  else if (i === "object")
    throw t = String(e), Error("Objects are not valid as a React child (found: " + (t === "[object Object]" ? "object with keys {" + Object.keys(e).join(", ") + "}" : t) + "). If you meant to render a collection of children, use an array instead.");
  return l;
}
function Qo(e, t, n) {
  if (e == null)
    return e;
  var r = [], o = 0;
  return hi(e, r, "", "", function(i) {
    return t.call(n, i, o++);
  }), r;
}
function T0(e) {
  if (e._status === -1) {
    var t = e._result;
    t = t(), t.then(function(n) {
      (e._status === 0 || e._status === -1) && (e._status = 1, e._result = n);
    }, function(n) {
      (e._status === 0 || e._status === -1) && (e._status = 2, e._result = n);
    }), e._status === -1 && (e._status = 0, e._result = t);
  }
  if (e._status === 1)
    return e._result.default;
  throw e._result;
}
var be = { current: null }, gi = { transition: null }, R0 = { ReactCurrentDispatcher: be, ReactCurrentBatchConfig: gi, ReactCurrentOwner: eu };
function Wd() {
  throw Error("act(...) is not supported in production builds of React.");
}
D.Children = { map: Qo, forEach: function(e, t, n) {
  Qo(e, function() {
    t.apply(this, arguments);
  }, n);
}, count: function(e) {
  var t = 0;
  return Qo(e, function() {
    t++;
  }), t;
}, toArray: function(e) {
  return Qo(e, function(t) {
    return t;
  }) || [];
}, only: function(e) {
  if (!tu(e))
    throw Error("React.Children.only expected to receive a single React element child.");
  return e;
} };
D.Component = Cr;
D.Fragment = g0;
D.Profiler = v0;
D.PureComponent = qa;
D.StrictMode = y0;
D.Suspense = k0;
D.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = R0;
D.act = Wd;
D.cloneElement = function(e, t, n) {
  if (e == null)
    throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + e + ".");
  var r = Id({}, e.props), o = e.key, i = e.ref, l = e._owner;
  if (t != null) {
    if (t.ref !== void 0 && (i = t.ref, l = eu.current), t.key !== void 0 && (o = "" + t.key), e.type && e.type.defaultProps)
      var s = e.type.defaultProps;
    for (a in t)
      Dd.call(t, a) && !Fd.hasOwnProperty(a) && (r[a] = t[a] === void 0 && s !== void 0 ? s[a] : t[a]);
  }
  var a = arguments.length - 2;
  if (a === 1)
    r.children = n;
  else if (1 < a) {
    s = Array(a);
    for (var u = 0; u < a; u++)
      s[u] = arguments[u + 2];
    r.children = s;
  }
  return { $$typeof: No, type: e.type, key: o, ref: i, props: r, _owner: l };
};
D.createContext = function(e) {
  return e = { $$typeof: S0, _currentValue: e, _currentValue2: e, _threadCount: 0, Provider: null, Consumer: null, _defaultValue: null, _globalName: null }, e.Provider = { $$typeof: x0, _context: e }, e.Consumer = e;
};
D.createElement = Bd;
D.createFactory = function(e) {
  var t = Bd.bind(null, e);
  return t.type = e, t;
};
D.createRef = function() {
  return { current: null };
};
D.forwardRef = function(e) {
  return { $$typeof: w0, render: e };
};
D.isValidElement = tu;
D.lazy = function(e) {
  return { $$typeof: E0, _payload: { _status: -1, _result: e }, _init: T0 };
};
D.memo = function(e, t) {
  return { $$typeof: C0, type: e, compare: t === void 0 ? null : t };
};
D.startTransition = function(e) {
  var t = gi.transition;
  gi.transition = {};
  try {
    e();
  } finally {
    gi.transition = t;
  }
};
D.unstable_act = Wd;
D.useCallback = function(e, t) {
  return be.current.useCallback(e, t);
};
D.useContext = function(e) {
  return be.current.useContext(e);
};
D.useDebugValue = function() {
};
D.useDeferredValue = function(e) {
  return be.current.useDeferredValue(e);
};
D.useEffect = function(e, t) {
  return be.current.useEffect(e, t);
};
D.useId = function() {
  return be.current.useId();
};
D.useImperativeHandle = function(e, t, n) {
  return be.current.useImperativeHandle(e, t, n);
};
D.useInsertionEffect = function(e, t) {
  return be.current.useInsertionEffect(e, t);
};
D.useLayoutEffect = function(e, t) {
  return be.current.useLayoutEffect(e, t);
};
D.useMemo = function(e, t) {
  return be.current.useMemo(e, t);
};
D.useReducer = function(e, t, n) {
  return be.current.useReducer(e, t, n);
};
D.useRef = function(e) {
  return be.current.useRef(e);
};
D.useState = function(e) {
  return be.current.useState(e);
};
D.useSyncExternalStore = function(e, t, n) {
  return be.current.useSyncExternalStore(e, t, n);
};
D.useTransition = function() {
  return be.current.useTransition();
};
D.version = "18.3.1";
Ld.exports = D;
var C = Ld.exports;
const Ct = /* @__PURE__ */ Nd(C), Gs = /* @__PURE__ */ m0({
  __proto__: null,
  default: Ct
}, [C]);
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var O0 = C, M0 = Symbol.for("react.element"), N0 = Symbol.for("react.fragment"), z0 = Object.prototype.hasOwnProperty, L0 = O0.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, j0 = { key: !0, ref: !0, __self: !0, __source: !0 };
function Ud(e, t, n) {
  var r, o = {}, i = null, l = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (r in t)
    z0.call(t, r) && !j0.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps)
    for (r in t = e.defaultProps, t)
      o[r] === void 0 && (o[r] = t[r]);
  return { $$typeof: M0, type: e, key: i, ref: l, props: o, _owner: L0.current };
}
cl.Fragment = N0;
cl.jsx = Ud;
cl.jsxs = Ud;
zd.exports = cl;
var $ = zd.exports, Qs = {}, Vd = { exports: {} }, tt = {}, Hd = { exports: {} }, Kd = {};
/**
 * @license React
 * scheduler.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
(function(e) {
  function t(R, z) {
    var I = R.length;
    R.push(z);
    e:
      for (; 0 < I; ) {
        var Z = I - 1 >>> 1, ae = R[Z];
        if (0 < o(ae, z))
          R[Z] = z, R[I] = ae, I = Z;
        else
          break e;
      }
  }
  function n(R) {
    return R.length === 0 ? null : R[0];
  }
  function r(R) {
    if (R.length === 0)
      return null;
    var z = R[0], I = R.pop();
    if (I !== z) {
      R[0] = I;
      e:
        for (var Z = 0, ae = R.length, Xt = ae >>> 1; Z < Xt; ) {
          var _e = 2 * (Z + 1) - 1, Pt = R[_e], j = _e + 1, xe = R[j];
          if (0 > o(Pt, I))
            j < ae && 0 > o(xe, Pt) ? (R[Z] = xe, R[j] = I, Z = j) : (R[Z] = Pt, R[_e] = I, Z = _e);
          else if (j < ae && 0 > o(xe, I))
            R[Z] = xe, R[j] = I, Z = j;
          else
            break e;
        }
    }
    return z;
  }
  function o(R, z) {
    var I = R.sortIndex - z.sortIndex;
    return I !== 0 ? I : R.id - z.id;
  }
  if (typeof performance == "object" && typeof performance.now == "function") {
    var i = performance;
    e.unstable_now = function() {
      return i.now();
    };
  } else {
    var l = Date, s = l.now();
    e.unstable_now = function() {
      return l.now() - s;
    };
  }
  var a = [], u = [], c = 1, f = null, p = 3, v = !1, y = !1, g = !1, _ = typeof setTimeout == "function" ? setTimeout : null, m = typeof clearTimeout == "function" ? clearTimeout : null, d = typeof setImmediate < "u" ? setImmediate : null;
  typeof navigator < "u" && navigator.scheduling !== void 0 && navigator.scheduling.isInputPending !== void 0 && navigator.scheduling.isInputPending.bind(navigator.scheduling);
  function h(R) {
    for (var z = n(u); z !== null; ) {
      if (z.callback === null)
        r(u);
      else if (z.startTime <= R)
        r(u), z.sortIndex = z.expirationTime, t(a, z);
      else
        break;
      z = n(u);
    }
  }
  function x(R) {
    if (g = !1, h(R), !y)
      if (n(a) !== null)
        y = !0, ve(E);
      else {
        var z = n(u);
        z !== null && he(x, z.startTime - R);
      }
  }
  function E(R, z) {
    y = !1, g && (g = !1, m(T), T = -1), v = !0;
    var I = p;
    try {
      for (h(z), f = n(a); f !== null && (!(f.expirationTime > z) || R && !F()); ) {
        var Z = f.callback;
        if (typeof Z == "function") {
          f.callback = null, p = f.priorityLevel;
          var ae = Z(f.expirationTime <= z);
          z = e.unstable_now(), typeof ae == "function" ? f.callback = ae : f === n(a) && r(a), h(z);
        } else
          r(a);
        f = n(a);
      }
      if (f !== null)
        var Xt = !0;
      else {
        var _e = n(u);
        _e !== null && he(x, _e.startTime - z), Xt = !1;
      }
      return Xt;
    } finally {
      f = null, p = I, v = !1;
    }
  }
  var k = !1, w = null, T = -1, N = 5, O = -1;
  function F() {
    return !(e.unstable_now() - O < N);
  }
  function A() {
    if (w !== null) {
      var R = e.unstable_now();
      O = R;
      var z = !0;
      try {
        z = w(!0, R);
      } finally {
        z ? L() : (k = !1, w = null);
      }
    } else
      k = !1;
  }
  var L;
  if (typeof d == "function")
    L = function() {
      d(A);
    };
  else if (typeof MessageChannel < "u") {
    var U = new MessageChannel(), te = U.port2;
    U.port1.onmessage = A, L = function() {
      te.postMessage(null);
    };
  } else
    L = function() {
      _(A, 0);
    };
  function ve(R) {
    w = R, k || (k = !0, L());
  }
  function he(R, z) {
    T = _(function() {
      R(e.unstable_now());
    }, z);
  }
  e.unstable_IdlePriority = 5, e.unstable_ImmediatePriority = 1, e.unstable_LowPriority = 4, e.unstable_NormalPriority = 3, e.unstable_Profiling = null, e.unstable_UserBlockingPriority = 2, e.unstable_cancelCallback = function(R) {
    R.callback = null;
  }, e.unstable_continueExecution = function() {
    y || v || (y = !0, ve(E));
  }, e.unstable_forceFrameRate = function(R) {
    0 > R || 125 < R ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : N = 0 < R ? Math.floor(1e3 / R) : 5;
  }, e.unstable_getCurrentPriorityLevel = function() {
    return p;
  }, e.unstable_getFirstCallbackNode = function() {
    return n(a);
  }, e.unstable_next = function(R) {
    switch (p) {
      case 1:
      case 2:
      case 3:
        var z = 3;
        break;
      default:
        z = p;
    }
    var I = p;
    p = z;
    try {
      return R();
    } finally {
      p = I;
    }
  }, e.unstable_pauseExecution = function() {
  }, e.unstable_requestPaint = function() {
  }, e.unstable_runWithPriority = function(R, z) {
    switch (R) {
      case 1:
      case 2:
      case 3:
      case 4:
      case 5:
        break;
      default:
        R = 3;
    }
    var I = p;
    p = R;
    try {
      return z();
    } finally {
      p = I;
    }
  }, e.unstable_scheduleCallback = function(R, z, I) {
    var Z = e.unstable_now();
    switch (typeof I == "object" && I !== null ? (I = I.delay, I = typeof I == "number" && 0 < I ? Z + I : Z) : I = Z, R) {
      case 1:
        var ae = -1;
        break;
      case 2:
        ae = 250;
        break;
      case 5:
        ae = 1073741823;
        break;
      case 4:
        ae = 1e4;
        break;
      default:
        ae = 5e3;
    }
    return ae = I + ae, R = { id: c++, callback: z, priorityLevel: R, startTime: I, expirationTime: ae, sortIndex: -1 }, I > Z ? (R.sortIndex = I, t(u, R), n(a) === null && R === n(u) && (g ? (m(T), T = -1) : g = !0, he(x, I - Z))) : (R.sortIndex = ae, t(a, R), y || v || (y = !0, ve(E))), R;
  }, e.unstable_shouldYield = F, e.unstable_wrapCallback = function(R) {
    var z = p;
    return function() {
      var I = p;
      p = z;
      try {
        return R.apply(this, arguments);
      } finally {
        p = I;
      }
    };
  };
})(Kd);
Hd.exports = Kd;
var I0 = Hd.exports;
/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var A0 = C, et = I0;
function P(e) {
  for (var t = "https://reactjs.org/docs/error-decoder.html?invariant=" + e, n = 1; n < arguments.length; n++)
    t += "&args[]=" + encodeURIComponent(arguments[n]);
  return "Minified React error #" + e + "; visit " + t + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
}
var Gd = /* @__PURE__ */ new Set(), lo = {};
function In(e, t) {
  mr(e, t), mr(e + "Capture", t);
}
function mr(e, t) {
  for (lo[e] = t, e = 0; e < t.length; e++)
    Gd.add(t[e]);
}
var Ut = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), Ys = Object.prototype.hasOwnProperty, b0 = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, Pc = {}, Tc = {};
function D0(e) {
  return Ys.call(Tc, e) ? !0 : Ys.call(Pc, e) ? !1 : b0.test(e) ? Tc[e] = !0 : (Pc[e] = !0, !1);
}
function F0(e, t, n, r) {
  if (n !== null && n.type === 0)
    return !1;
  switch (typeof t) {
    case "function":
    case "symbol":
      return !0;
    case "boolean":
      return r ? !1 : n !== null ? !n.acceptsBooleans : (e = e.toLowerCase().slice(0, 5), e !== "data-" && e !== "aria-");
    default:
      return !1;
  }
}
function B0(e, t, n, r) {
  if (t === null || typeof t > "u" || F0(e, t, n, r))
    return !0;
  if (r)
    return !1;
  if (n !== null)
    switch (n.type) {
      case 3:
        return !t;
      case 4:
        return t === !1;
      case 5:
        return isNaN(t);
      case 6:
        return isNaN(t) || 1 > t;
    }
  return !1;
}
function De(e, t, n, r, o, i, l) {
  this.acceptsBooleans = t === 2 || t === 3 || t === 4, this.attributeName = r, this.attributeNamespace = o, this.mustUseProperty = n, this.propertyName = e, this.type = t, this.sanitizeURL = i, this.removeEmptyString = l;
}
var Re = {};
"children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(e) {
  Re[e] = new De(e, 0, !1, e, null, !1, !1);
});
[["acceptCharset", "accept-charset"], ["className", "class"], ["htmlFor", "for"], ["httpEquiv", "http-equiv"]].forEach(function(e) {
  var t = e[0];
  Re[t] = new De(t, 1, !1, e[1], null, !1, !1);
});
["contentEditable", "draggable", "spellCheck", "value"].forEach(function(e) {
  Re[e] = new De(e, 2, !1, e.toLowerCase(), null, !1, !1);
});
["autoReverse", "externalResourcesRequired", "focusable", "preserveAlpha"].forEach(function(e) {
  Re[e] = new De(e, 2, !1, e, null, !1, !1);
});
"allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(e) {
  Re[e] = new De(e, 3, !1, e.toLowerCase(), null, !1, !1);
});
["checked", "multiple", "muted", "selected"].forEach(function(e) {
  Re[e] = new De(e, 3, !0, e, null, !1, !1);
});
["capture", "download"].forEach(function(e) {
  Re[e] = new De(e, 4, !1, e, null, !1, !1);
});
["cols", "rows", "size", "span"].forEach(function(e) {
  Re[e] = new De(e, 6, !1, e, null, !1, !1);
});
["rowSpan", "start"].forEach(function(e) {
  Re[e] = new De(e, 5, !1, e.toLowerCase(), null, !1, !1);
});
var nu = /[\-:]([a-z])/g;
function ru(e) {
  return e[1].toUpperCase();
}
"accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(e) {
  var t = e.replace(
    nu,
    ru
  );
  Re[t] = new De(t, 1, !1, e, null, !1, !1);
});
"xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(e) {
  var t = e.replace(nu, ru);
  Re[t] = new De(t, 1, !1, e, "http://www.w3.org/1999/xlink", !1, !1);
});
["xml:base", "xml:lang", "xml:space"].forEach(function(e) {
  var t = e.replace(nu, ru);
  Re[t] = new De(t, 1, !1, e, "http://www.w3.org/XML/1998/namespace", !1, !1);
});
["tabIndex", "crossOrigin"].forEach(function(e) {
  Re[e] = new De(e, 1, !1, e.toLowerCase(), null, !1, !1);
});
Re.xlinkHref = new De("xlinkHref", 1, !1, "xlink:href", "http://www.w3.org/1999/xlink", !0, !1);
["src", "href", "action", "formAction"].forEach(function(e) {
  Re[e] = new De(e, 1, !1, e.toLowerCase(), null, !0, !0);
});
function ou(e, t, n, r) {
  var o = Re.hasOwnProperty(t) ? Re[t] : null;
  (o !== null ? o.type !== 0 : r || !(2 < t.length) || t[0] !== "o" && t[0] !== "O" || t[1] !== "n" && t[1] !== "N") && (B0(t, n, o, r) && (n = null), r || o === null ? D0(t) && (n === null ? e.removeAttribute(t) : e.setAttribute(t, "" + n)) : o.mustUseProperty ? e[o.propertyName] = n === null ? o.type === 3 ? !1 : "" : n : (t = o.attributeName, r = o.attributeNamespace, n === null ? e.removeAttribute(t) : (o = o.type, n = o === 3 || o === 4 && n === !0 ? "" : "" + n, r ? e.setAttributeNS(r, t, n) : e.setAttribute(t, n))));
}
var Qt = A0.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, Yo = Symbol.for("react.element"), Gn = Symbol.for("react.portal"), Qn = Symbol.for("react.fragment"), iu = Symbol.for("react.strict_mode"), Xs = Symbol.for("react.profiler"), Qd = Symbol.for("react.provider"), Yd = Symbol.for("react.context"), lu = Symbol.for("react.forward_ref"), Zs = Symbol.for("react.suspense"), qs = Symbol.for("react.suspense_list"), su = Symbol.for("react.memo"), Jt = Symbol.for("react.lazy"), Xd = Symbol.for("react.offscreen"), Rc = Symbol.iterator;
function zr(e) {
  return e === null || typeof e != "object" ? null : (e = Rc && e[Rc] || e["@@iterator"], typeof e == "function" ? e : null);
}
var se = Object.assign, ds;
function Vr(e) {
  if (ds === void 0)
    try {
      throw Error();
    } catch (n) {
      var t = n.stack.trim().match(/\n( *(at )?)/);
      ds = t && t[1] || "";
    }
  return `
` + ds + e;
}
var ps = !1;
function ms(e, t) {
  if (!e || ps)
    return "";
  ps = !0;
  var n = Error.prepareStackTrace;
  Error.prepareStackTrace = void 0;
  try {
    if (t)
      if (t = function() {
        throw Error();
      }, Object.defineProperty(t.prototype, "props", { set: function() {
        throw Error();
      } }), typeof Reflect == "object" && Reflect.construct) {
        try {
          Reflect.construct(t, []);
        } catch (u) {
          var r = u;
        }
        Reflect.construct(e, [], t);
      } else {
        try {
          t.call();
        } catch (u) {
          r = u;
        }
        e.call(t.prototype);
      }
    else {
      try {
        throw Error();
      } catch (u) {
        r = u;
      }
      e();
    }
  } catch (u) {
    if (u && r && typeof u.stack == "string") {
      for (var o = u.stack.split(`
`), i = r.stack.split(`
`), l = o.length - 1, s = i.length - 1; 1 <= l && 0 <= s && o[l] !== i[s]; )
        s--;
      for (; 1 <= l && 0 <= s; l--, s--)
        if (o[l] !== i[s]) {
          if (l !== 1 || s !== 1)
            do
              if (l--, s--, 0 > s || o[l] !== i[s]) {
                var a = `
` + o[l].replace(" at new ", " at ");
                return e.displayName && a.includes("<anonymous>") && (a = a.replace("<anonymous>", e.displayName)), a;
              }
            while (1 <= l && 0 <= s);
          break;
        }
    }
  } finally {
    ps = !1, Error.prepareStackTrace = n;
  }
  return (e = e ? e.displayName || e.name : "") ? Vr(e) : "";
}
function W0(e) {
  switch (e.tag) {
    case 5:
      return Vr(e.type);
    case 16:
      return Vr("Lazy");
    case 13:
      return Vr("Suspense");
    case 19:
      return Vr("SuspenseList");
    case 0:
    case 2:
    case 15:
      return e = ms(e.type, !1), e;
    case 11:
      return e = ms(e.type.render, !1), e;
    case 1:
      return e = ms(e.type, !0), e;
    default:
      return "";
  }
}
function Js(e) {
  if (e == null)
    return null;
  if (typeof e == "function")
    return e.displayName || e.name || null;
  if (typeof e == "string")
    return e;
  switch (e) {
    case Qn:
      return "Fragment";
    case Gn:
      return "Portal";
    case Xs:
      return "Profiler";
    case iu:
      return "StrictMode";
    case Zs:
      return "Suspense";
    case qs:
      return "SuspenseList";
  }
  if (typeof e == "object")
    switch (e.$$typeof) {
      case Yd:
        return (e.displayName || "Context") + ".Consumer";
      case Qd:
        return (e._context.displayName || "Context") + ".Provider";
      case lu:
        var t = e.render;
        return e = e.displayName, e || (e = t.displayName || t.name || "", e = e !== "" ? "ForwardRef(" + e + ")" : "ForwardRef"), e;
      case su:
        return t = e.displayName || null, t !== null ? t : Js(e.type) || "Memo";
      case Jt:
        t = e._payload, e = e._init;
        try {
          return Js(e(t));
        } catch {
        }
    }
  return null;
}
function U0(e) {
  var t = e.type;
  switch (e.tag) {
    case 24:
      return "Cache";
    case 9:
      return (t.displayName || "Context") + ".Consumer";
    case 10:
      return (t._context.displayName || "Context") + ".Provider";
    case 18:
      return "DehydratedFragment";
    case 11:
      return e = t.render, e = e.displayName || e.name || "", t.displayName || (e !== "" ? "ForwardRef(" + e + ")" : "ForwardRef");
    case 7:
      return "Fragment";
    case 5:
      return t;
    case 4:
      return "Portal";
    case 3:
      return "Root";
    case 6:
      return "Text";
    case 16:
      return Js(t);
    case 8:
      return t === iu ? "StrictMode" : "Mode";
    case 22:
      return "Offscreen";
    case 12:
      return "Profiler";
    case 21:
      return "Scope";
    case 13:
      return "Suspense";
    case 19:
      return "SuspenseList";
    case 25:
      return "TracingMarker";
    case 1:
    case 0:
    case 17:
    case 2:
    case 14:
    case 15:
      if (typeof t == "function")
        return t.displayName || t.name || null;
      if (typeof t == "string")
        return t;
  }
  return null;
}
function hn(e) {
  switch (typeof e) {
    case "boolean":
    case "number":
    case "string":
    case "undefined":
      return e;
    case "object":
      return e;
    default:
      return "";
  }
}
function Zd(e) {
  var t = e.type;
  return (e = e.nodeName) && e.toLowerCase() === "input" && (t === "checkbox" || t === "radio");
}
function V0(e) {
  var t = Zd(e) ? "checked" : "value", n = Object.getOwnPropertyDescriptor(e.constructor.prototype, t), r = "" + e[t];
  if (!e.hasOwnProperty(t) && typeof n < "u" && typeof n.get == "function" && typeof n.set == "function") {
    var o = n.get, i = n.set;
    return Object.defineProperty(e, t, { configurable: !0, get: function() {
      return o.call(this);
    }, set: function(l) {
      r = "" + l, i.call(this, l);
    } }), Object.defineProperty(e, t, { enumerable: n.enumerable }), { getValue: function() {
      return r;
    }, setValue: function(l) {
      r = "" + l;
    }, stopTracking: function() {
      e._valueTracker = null, delete e[t];
    } };
  }
}
function Xo(e) {
  e._valueTracker || (e._valueTracker = V0(e));
}
function qd(e) {
  if (!e)
    return !1;
  var t = e._valueTracker;
  if (!t)
    return !0;
  var n = t.getValue(), r = "";
  return e && (r = Zd(e) ? e.checked ? "true" : "false" : e.value), e = r, e !== n ? (t.setValue(e), !0) : !1;
}
function zi(e) {
  if (e = e || (typeof document < "u" ? document : void 0), typeof e > "u")
    return null;
  try {
    return e.activeElement || e.body;
  } catch {
    return e.body;
  }
}
function ea(e, t) {
  var n = t.checked;
  return se({}, t, { defaultChecked: void 0, defaultValue: void 0, value: void 0, checked: n ?? e._wrapperState.initialChecked });
}
function Oc(e, t) {
  var n = t.defaultValue == null ? "" : t.defaultValue, r = t.checked != null ? t.checked : t.defaultChecked;
  n = hn(t.value != null ? t.value : n), e._wrapperState = { initialChecked: r, initialValue: n, controlled: t.type === "checkbox" || t.type === "radio" ? t.checked != null : t.value != null };
}
function Jd(e, t) {
  t = t.checked, t != null && ou(e, "checked", t, !1);
}
function ta(e, t) {
  Jd(e, t);
  var n = hn(t.value), r = t.type;
  if (n != null)
    r === "number" ? (n === 0 && e.value === "" || e.value != n) && (e.value = "" + n) : e.value !== "" + n && (e.value = "" + n);
  else if (r === "submit" || r === "reset") {
    e.removeAttribute("value");
    return;
  }
  t.hasOwnProperty("value") ? na(e, t.type, n) : t.hasOwnProperty("defaultValue") && na(e, t.type, hn(t.defaultValue)), t.checked == null && t.defaultChecked != null && (e.defaultChecked = !!t.defaultChecked);
}
function Mc(e, t, n) {
  if (t.hasOwnProperty("value") || t.hasOwnProperty("defaultValue")) {
    var r = t.type;
    if (!(r !== "submit" && r !== "reset" || t.value !== void 0 && t.value !== null))
      return;
    t = "" + e._wrapperState.initialValue, n || t === e.value || (e.value = t), e.defaultValue = t;
  }
  n = e.name, n !== "" && (e.name = ""), e.defaultChecked = !!e._wrapperState.initialChecked, n !== "" && (e.name = n);
}
function na(e, t, n) {
  (t !== "number" || zi(e.ownerDocument) !== e) && (n == null ? e.defaultValue = "" + e._wrapperState.initialValue : e.defaultValue !== "" + n && (e.defaultValue = "" + n));
}
var Hr = Array.isArray;
function ir(e, t, n, r) {
  if (e = e.options, t) {
    t = {};
    for (var o = 0; o < n.length; o++)
      t["$" + n[o]] = !0;
    for (n = 0; n < e.length; n++)
      o = t.hasOwnProperty("$" + e[n].value), e[n].selected !== o && (e[n].selected = o), o && r && (e[n].defaultSelected = !0);
  } else {
    for (n = "" + hn(n), t = null, o = 0; o < e.length; o++) {
      if (e[o].value === n) {
        e[o].selected = !0, r && (e[o].defaultSelected = !0);
        return;
      }
      t !== null || e[o].disabled || (t = e[o]);
    }
    t !== null && (t.selected = !0);
  }
}
function ra(e, t) {
  if (t.dangerouslySetInnerHTML != null)
    throw Error(P(91));
  return se({}, t, { value: void 0, defaultValue: void 0, children: "" + e._wrapperState.initialValue });
}
function Nc(e, t) {
  var n = t.value;
  if (n == null) {
    if (n = t.children, t = t.defaultValue, n != null) {
      if (t != null)
        throw Error(P(92));
      if (Hr(n)) {
        if (1 < n.length)
          throw Error(P(93));
        n = n[0];
      }
      t = n;
    }
    t == null && (t = ""), n = t;
  }
  e._wrapperState = { initialValue: hn(n) };
}
function ep(e, t) {
  var n = hn(t.value), r = hn(t.defaultValue);
  n != null && (n = "" + n, n !== e.value && (e.value = n), t.defaultValue == null && e.defaultValue !== n && (e.defaultValue = n)), r != null && (e.defaultValue = "" + r);
}
function zc(e) {
  var t = e.textContent;
  t === e._wrapperState.initialValue && t !== "" && t !== null && (e.value = t);
}
function tp(e) {
  switch (e) {
    case "svg":
      return "http://www.w3.org/2000/svg";
    case "math":
      return "http://www.w3.org/1998/Math/MathML";
    default:
      return "http://www.w3.org/1999/xhtml";
  }
}
function oa(e, t) {
  return e == null || e === "http://www.w3.org/1999/xhtml" ? tp(t) : e === "http://www.w3.org/2000/svg" && t === "foreignObject" ? "http://www.w3.org/1999/xhtml" : e;
}
var Zo, np = function(e) {
  return typeof MSApp < "u" && MSApp.execUnsafeLocalFunction ? function(t, n, r, o) {
    MSApp.execUnsafeLocalFunction(function() {
      return e(t, n, r, o);
    });
  } : e;
}(function(e, t) {
  if (e.namespaceURI !== "http://www.w3.org/2000/svg" || "innerHTML" in e)
    e.innerHTML = t;
  else {
    for (Zo = Zo || document.createElement("div"), Zo.innerHTML = "<svg>" + t.valueOf().toString() + "</svg>", t = Zo.firstChild; e.firstChild; )
      e.removeChild(e.firstChild);
    for (; t.firstChild; )
      e.appendChild(t.firstChild);
  }
});
function so(e, t) {
  if (t) {
    var n = e.firstChild;
    if (n && n === e.lastChild && n.nodeType === 3) {
      n.nodeValue = t;
      return;
    }
  }
  e.textContent = t;
}
var Xr = {
  animationIterationCount: !0,
  aspectRatio: !0,
  borderImageOutset: !0,
  borderImageSlice: !0,
  borderImageWidth: !0,
  boxFlex: !0,
  boxFlexGroup: !0,
  boxOrdinalGroup: !0,
  columnCount: !0,
  columns: !0,
  flex: !0,
  flexGrow: !0,
  flexPositive: !0,
  flexShrink: !0,
  flexNegative: !0,
  flexOrder: !0,
  gridArea: !0,
  gridRow: !0,
  gridRowEnd: !0,
  gridRowSpan: !0,
  gridRowStart: !0,
  gridColumn: !0,
  gridColumnEnd: !0,
  gridColumnSpan: !0,
  gridColumnStart: !0,
  fontWeight: !0,
  lineClamp: !0,
  lineHeight: !0,
  opacity: !0,
  order: !0,
  orphans: !0,
  tabSize: !0,
  widows: !0,
  zIndex: !0,
  zoom: !0,
  fillOpacity: !0,
  floodOpacity: !0,
  stopOpacity: !0,
  strokeDasharray: !0,
  strokeDashoffset: !0,
  strokeMiterlimit: !0,
  strokeOpacity: !0,
  strokeWidth: !0
}, H0 = ["Webkit", "ms", "Moz", "O"];
Object.keys(Xr).forEach(function(e) {
  H0.forEach(function(t) {
    t = t + e.charAt(0).toUpperCase() + e.substring(1), Xr[t] = Xr[e];
  });
});
function rp(e, t, n) {
  return t == null || typeof t == "boolean" || t === "" ? "" : n || typeof t != "number" || t === 0 || Xr.hasOwnProperty(e) && Xr[e] ? ("" + t).trim() : t + "px";
}
function op(e, t) {
  e = e.style;
  for (var n in t)
    if (t.hasOwnProperty(n)) {
      var r = n.indexOf("--") === 0, o = rp(n, t[n], r);
      n === "float" && (n = "cssFloat"), r ? e.setProperty(n, o) : e[n] = o;
    }
}
var K0 = se({ menuitem: !0 }, { area: !0, base: !0, br: !0, col: !0, embed: !0, hr: !0, img: !0, input: !0, keygen: !0, link: !0, meta: !0, param: !0, source: !0, track: !0, wbr: !0 });
function ia(e, t) {
  if (t) {
    if (K0[e] && (t.children != null || t.dangerouslySetInnerHTML != null))
      throw Error(P(137, e));
    if (t.dangerouslySetInnerHTML != null) {
      if (t.children != null)
        throw Error(P(60));
      if (typeof t.dangerouslySetInnerHTML != "object" || !("__html" in t.dangerouslySetInnerHTML))
        throw Error(P(61));
    }
    if (t.style != null && typeof t.style != "object")
      throw Error(P(62));
  }
}
function la(e, t) {
  if (e.indexOf("-") === -1)
    return typeof t.is == "string";
  switch (e) {
    case "annotation-xml":
    case "color-profile":
    case "font-face":
    case "font-face-src":
    case "font-face-uri":
    case "font-face-format":
    case "font-face-name":
    case "missing-glyph":
      return !1;
    default:
      return !0;
  }
}
var sa = null;
function au(e) {
  return e = e.target || e.srcElement || window, e.correspondingUseElement && (e = e.correspondingUseElement), e.nodeType === 3 ? e.parentNode : e;
}
var aa = null, lr = null, sr = null;
function Lc(e) {
  if (e = jo(e)) {
    if (typeof aa != "function")
      throw Error(P(280));
    var t = e.stateNode;
    t && (t = hl(t), aa(e.stateNode, e.type, t));
  }
}
function ip(e) {
  lr ? sr ? sr.push(e) : sr = [e] : lr = e;
}
function lp() {
  if (lr) {
    var e = lr, t = sr;
    if (sr = lr = null, Lc(e), t)
      for (e = 0; e < t.length; e++)
        Lc(t[e]);
  }
}
function sp(e, t) {
  return e(t);
}
function ap() {
}
var hs = !1;
function up(e, t, n) {
  if (hs)
    return e(t, n);
  hs = !0;
  try {
    return sp(e, t, n);
  } finally {
    hs = !1, (lr !== null || sr !== null) && (ap(), lp());
  }
}
function ao(e, t) {
  var n = e.stateNode;
  if (n === null)
    return null;
  var r = hl(n);
  if (r === null)
    return null;
  n = r[t];
  e:
    switch (t) {
      case "onClick":
      case "onClickCapture":
      case "onDoubleClick":
      case "onDoubleClickCapture":
      case "onMouseDown":
      case "onMouseDownCapture":
      case "onMouseMove":
      case "onMouseMoveCapture":
      case "onMouseUp":
      case "onMouseUpCapture":
      case "onMouseEnter":
        (r = !r.disabled) || (e = e.type, r = !(e === "button" || e === "input" || e === "select" || e === "textarea")), e = !r;
        break e;
      default:
        e = !1;
    }
  if (e)
    return null;
  if (n && typeof n != "function")
    throw Error(P(231, t, typeof n));
  return n;
}
var ua = !1;
if (Ut)
  try {
    var Lr = {};
    Object.defineProperty(Lr, "passive", { get: function() {
      ua = !0;
    } }), window.addEventListener("test", Lr, Lr), window.removeEventListener("test", Lr, Lr);
  } catch {
    ua = !1;
  }
function G0(e, t, n, r, o, i, l, s, a) {
  var u = Array.prototype.slice.call(arguments, 3);
  try {
    t.apply(n, u);
  } catch (c) {
    this.onError(c);
  }
}
var Zr = !1, Li = null, ji = !1, ca = null, Q0 = { onError: function(e) {
  Zr = !0, Li = e;
} };
function Y0(e, t, n, r, o, i, l, s, a) {
  Zr = !1, Li = null, G0.apply(Q0, arguments);
}
function X0(e, t, n, r, o, i, l, s, a) {
  if (Y0.apply(this, arguments), Zr) {
    if (Zr) {
      var u = Li;
      Zr = !1, Li = null;
    } else
      throw Error(P(198));
    ji || (ji = !0, ca = u);
  }
}
function An(e) {
  var t = e, n = e;
  if (e.alternate)
    for (; t.return; )
      t = t.return;
  else {
    e = t;
    do
      t = e, t.flags & 4098 && (n = t.return), e = t.return;
    while (e);
  }
  return t.tag === 3 ? n : null;
}
function cp(e) {
  if (e.tag === 13) {
    var t = e.memoizedState;
    if (t === null && (e = e.alternate, e !== null && (t = e.memoizedState)), t !== null)
      return t.dehydrated;
  }
  return null;
}
function jc(e) {
  if (An(e) !== e)
    throw Error(P(188));
}
function Z0(e) {
  var t = e.alternate;
  if (!t) {
    if (t = An(e), t === null)
      throw Error(P(188));
    return t !== e ? null : e;
  }
  for (var n = e, r = t; ; ) {
    var o = n.return;
    if (o === null)
      break;
    var i = o.alternate;
    if (i === null) {
      if (r = o.return, r !== null) {
        n = r;
        continue;
      }
      break;
    }
    if (o.child === i.child) {
      for (i = o.child; i; ) {
        if (i === n)
          return jc(o), e;
        if (i === r)
          return jc(o), t;
        i = i.sibling;
      }
      throw Error(P(188));
    }
    if (n.return !== r.return)
      n = o, r = i;
    else {
      for (var l = !1, s = o.child; s; ) {
        if (s === n) {
          l = !0, n = o, r = i;
          break;
        }
        if (s === r) {
          l = !0, r = o, n = i;
          break;
        }
        s = s.sibling;
      }
      if (!l) {
        for (s = i.child; s; ) {
          if (s === n) {
            l = !0, n = i, r = o;
            break;
          }
          if (s === r) {
            l = !0, r = i, n = o;
            break;
          }
          s = s.sibling;
        }
        if (!l)
          throw Error(P(189));
      }
    }
    if (n.alternate !== r)
      throw Error(P(190));
  }
  if (n.tag !== 3)
    throw Error(P(188));
  return n.stateNode.current === n ? e : t;
}
function fp(e) {
  return e = Z0(e), e !== null ? dp(e) : null;
}
function dp(e) {
  if (e.tag === 5 || e.tag === 6)
    return e;
  for (e = e.child; e !== null; ) {
    var t = dp(e);
    if (t !== null)
      return t;
    e = e.sibling;
  }
  return null;
}
var pp = et.unstable_scheduleCallback, Ic = et.unstable_cancelCallback, q0 = et.unstable_shouldYield, J0 = et.unstable_requestPaint, de = et.unstable_now, eg = et.unstable_getCurrentPriorityLevel, uu = et.unstable_ImmediatePriority, mp = et.unstable_UserBlockingPriority, Ii = et.unstable_NormalPriority, tg = et.unstable_LowPriority, hp = et.unstable_IdlePriority, fl = null, zt = null;
function ng(e) {
  if (zt && typeof zt.onCommitFiberRoot == "function")
    try {
      zt.onCommitFiberRoot(fl, e, void 0, (e.current.flags & 128) === 128);
    } catch {
    }
}
var Et = Math.clz32 ? Math.clz32 : ig, rg = Math.log, og = Math.LN2;
function ig(e) {
  return e >>>= 0, e === 0 ? 32 : 31 - (rg(e) / og | 0) | 0;
}
var qo = 64, Jo = 4194304;
function Kr(e) {
  switch (e & -e) {
    case 1:
      return 1;
    case 2:
      return 2;
    case 4:
      return 4;
    case 8:
      return 8;
    case 16:
      return 16;
    case 32:
      return 32;
    case 64:
    case 128:
    case 256:
    case 512:
    case 1024:
    case 2048:
    case 4096:
    case 8192:
    case 16384:
    case 32768:
    case 65536:
    case 131072:
    case 262144:
    case 524288:
    case 1048576:
    case 2097152:
      return e & 4194240;
    case 4194304:
    case 8388608:
    case 16777216:
    case 33554432:
    case 67108864:
      return e & 130023424;
    case 134217728:
      return 134217728;
    case 268435456:
      return 268435456;
    case 536870912:
      return 536870912;
    case 1073741824:
      return 1073741824;
    default:
      return e;
  }
}
function Ai(e, t) {
  var n = e.pendingLanes;
  if (n === 0)
    return 0;
  var r = 0, o = e.suspendedLanes, i = e.pingedLanes, l = n & 268435455;
  if (l !== 0) {
    var s = l & ~o;
    s !== 0 ? r = Kr(s) : (i &= l, i !== 0 && (r = Kr(i)));
  } else
    l = n & ~o, l !== 0 ? r = Kr(l) : i !== 0 && (r = Kr(i));
  if (r === 0)
    return 0;
  if (t !== 0 && t !== r && !(t & o) && (o = r & -r, i = t & -t, o >= i || o === 16 && (i & 4194240) !== 0))
    return t;
  if (r & 4 && (r |= n & 16), t = e.entangledLanes, t !== 0)
    for (e = e.entanglements, t &= r; 0 < t; )
      n = 31 - Et(t), o = 1 << n, r |= e[n], t &= ~o;
  return r;
}
function lg(e, t) {
  switch (e) {
    case 1:
    case 2:
    case 4:
      return t + 250;
    case 8:
    case 16:
    case 32:
    case 64:
    case 128:
    case 256:
    case 512:
    case 1024:
    case 2048:
    case 4096:
    case 8192:
    case 16384:
    case 32768:
    case 65536:
    case 131072:
    case 262144:
    case 524288:
    case 1048576:
    case 2097152:
      return t + 5e3;
    case 4194304:
    case 8388608:
    case 16777216:
    case 33554432:
    case 67108864:
      return -1;
    case 134217728:
    case 268435456:
    case 536870912:
    case 1073741824:
      return -1;
    default:
      return -1;
  }
}
function sg(e, t) {
  for (var n = e.suspendedLanes, r = e.pingedLanes, o = e.expirationTimes, i = e.pendingLanes; 0 < i; ) {
    var l = 31 - Et(i), s = 1 << l, a = o[l];
    a === -1 ? (!(s & n) || s & r) && (o[l] = lg(s, t)) : a <= t && (e.expiredLanes |= s), i &= ~s;
  }
}
function fa(e) {
  return e = e.pendingLanes & -1073741825, e !== 0 ? e : e & 1073741824 ? 1073741824 : 0;
}
function gp() {
  var e = qo;
  return qo <<= 1, !(qo & 4194240) && (qo = 64), e;
}
function gs(e) {
  for (var t = [], n = 0; 31 > n; n++)
    t.push(e);
  return t;
}
function zo(e, t, n) {
  e.pendingLanes |= t, t !== 536870912 && (e.suspendedLanes = 0, e.pingedLanes = 0), e = e.eventTimes, t = 31 - Et(t), e[t] = n;
}
function ag(e, t) {
  var n = e.pendingLanes & ~t;
  e.pendingLanes = t, e.suspendedLanes = 0, e.pingedLanes = 0, e.expiredLanes &= t, e.mutableReadLanes &= t, e.entangledLanes &= t, t = e.entanglements;
  var r = e.eventTimes;
  for (e = e.expirationTimes; 0 < n; ) {
    var o = 31 - Et(n), i = 1 << o;
    t[o] = 0, r[o] = -1, e[o] = -1, n &= ~i;
  }
}
function cu(e, t) {
  var n = e.entangledLanes |= t;
  for (e = e.entanglements; n; ) {
    var r = 31 - Et(n), o = 1 << r;
    o & t | e[r] & t && (e[r] |= t), n &= ~o;
  }
}
var K = 0;
function yp(e) {
  return e &= -e, 1 < e ? 4 < e ? e & 268435455 ? 16 : 536870912 : 4 : 1;
}
var vp, fu, xp, Sp, wp, da = !1, ei = [], sn = null, an = null, un = null, uo = /* @__PURE__ */ new Map(), co = /* @__PURE__ */ new Map(), tn = [], ug = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
function Ac(e, t) {
  switch (e) {
    case "focusin":
    case "focusout":
      sn = null;
      break;
    case "dragenter":
    case "dragleave":
      an = null;
      break;
    case "mouseover":
    case "mouseout":
      un = null;
      break;
    case "pointerover":
    case "pointerout":
      uo.delete(t.pointerId);
      break;
    case "gotpointercapture":
    case "lostpointercapture":
      co.delete(t.pointerId);
  }
}
function jr(e, t, n, r, o, i) {
  return e === null || e.nativeEvent !== i ? (e = { blockedOn: t, domEventName: n, eventSystemFlags: r, nativeEvent: i, targetContainers: [o] }, t !== null && (t = jo(t), t !== null && fu(t)), e) : (e.eventSystemFlags |= r, t = e.targetContainers, o !== null && t.indexOf(o) === -1 && t.push(o), e);
}
function cg(e, t, n, r, o) {
  switch (t) {
    case "focusin":
      return sn = jr(sn, e, t, n, r, o), !0;
    case "dragenter":
      return an = jr(an, e, t, n, r, o), !0;
    case "mouseover":
      return un = jr(un, e, t, n, r, o), !0;
    case "pointerover":
      var i = o.pointerId;
      return uo.set(i, jr(uo.get(i) || null, e, t, n, r, o)), !0;
    case "gotpointercapture":
      return i = o.pointerId, co.set(i, jr(co.get(i) || null, e, t, n, r, o)), !0;
  }
  return !1;
}
function kp(e) {
  var t = En(e.target);
  if (t !== null) {
    var n = An(t);
    if (n !== null) {
      if (t = n.tag, t === 13) {
        if (t = cp(n), t !== null) {
          e.blockedOn = t, wp(e.priority, function() {
            xp(n);
          });
          return;
        }
      } else if (t === 3 && n.stateNode.current.memoizedState.isDehydrated) {
        e.blockedOn = n.tag === 3 ? n.stateNode.containerInfo : null;
        return;
      }
    }
  }
  e.blockedOn = null;
}
function yi(e) {
  if (e.blockedOn !== null)
    return !1;
  for (var t = e.targetContainers; 0 < t.length; ) {
    var n = pa(e.domEventName, e.eventSystemFlags, t[0], e.nativeEvent);
    if (n === null) {
      n = e.nativeEvent;
      var r = new n.constructor(n.type, n);
      sa = r, n.target.dispatchEvent(r), sa = null;
    } else
      return t = jo(n), t !== null && fu(t), e.blockedOn = n, !1;
    t.shift();
  }
  return !0;
}
function bc(e, t, n) {
  yi(e) && n.delete(t);
}
function fg() {
  da = !1, sn !== null && yi(sn) && (sn = null), an !== null && yi(an) && (an = null), un !== null && yi(un) && (un = null), uo.forEach(bc), co.forEach(bc);
}
function Ir(e, t) {
  e.blockedOn === t && (e.blockedOn = null, da || (da = !0, et.unstable_scheduleCallback(et.unstable_NormalPriority, fg)));
}
function fo(e) {
  function t(o) {
    return Ir(o, e);
  }
  if (0 < ei.length) {
    Ir(ei[0], e);
    for (var n = 1; n < ei.length; n++) {
      var r = ei[n];
      r.blockedOn === e && (r.blockedOn = null);
    }
  }
  for (sn !== null && Ir(sn, e), an !== null && Ir(an, e), un !== null && Ir(un, e), uo.forEach(t), co.forEach(t), n = 0; n < tn.length; n++)
    r = tn[n], r.blockedOn === e && (r.blockedOn = null);
  for (; 0 < tn.length && (n = tn[0], n.blockedOn === null); )
    kp(n), n.blockedOn === null && tn.shift();
}
var ar = Qt.ReactCurrentBatchConfig, bi = !0;
function dg(e, t, n, r) {
  var o = K, i = ar.transition;
  ar.transition = null;
  try {
    K = 1, du(e, t, n, r);
  } finally {
    K = o, ar.transition = i;
  }
}
function pg(e, t, n, r) {
  var o = K, i = ar.transition;
  ar.transition = null;
  try {
    K = 4, du(e, t, n, r);
  } finally {
    K = o, ar.transition = i;
  }
}
function du(e, t, n, r) {
  if (bi) {
    var o = pa(e, t, n, r);
    if (o === null)
      $s(e, t, r, Di, n), Ac(e, r);
    else if (cg(o, e, t, n, r))
      r.stopPropagation();
    else if (Ac(e, r), t & 4 && -1 < ug.indexOf(e)) {
      for (; o !== null; ) {
        var i = jo(o);
        if (i !== null && vp(i), i = pa(e, t, n, r), i === null && $s(e, t, r, Di, n), i === o)
          break;
        o = i;
      }
      o !== null && r.stopPropagation();
    } else
      $s(e, t, r, null, n);
  }
}
var Di = null;
function pa(e, t, n, r) {
  if (Di = null, e = au(r), e = En(e), e !== null)
    if (t = An(e), t === null)
      e = null;
    else if (n = t.tag, n === 13) {
      if (e = cp(t), e !== null)
        return e;
      e = null;
    } else if (n === 3) {
      if (t.stateNode.current.memoizedState.isDehydrated)
        return t.tag === 3 ? t.stateNode.containerInfo : null;
      e = null;
    } else
      t !== e && (e = null);
  return Di = e, null;
}
function Cp(e) {
  switch (e) {
    case "cancel":
    case "click":
    case "close":
    case "contextmenu":
    case "copy":
    case "cut":
    case "auxclick":
    case "dblclick":
    case "dragend":
    case "dragstart":
    case "drop":
    case "focusin":
    case "focusout":
    case "input":
    case "invalid":
    case "keydown":
    case "keypress":
    case "keyup":
    case "mousedown":
    case "mouseup":
    case "paste":
    case "pause":
    case "play":
    case "pointercancel":
    case "pointerdown":
    case "pointerup":
    case "ratechange":
    case "reset":
    case "resize":
    case "seeked":
    case "submit":
    case "touchcancel":
    case "touchend":
    case "touchstart":
    case "volumechange":
    case "change":
    case "selectionchange":
    case "textInput":
    case "compositionstart":
    case "compositionend":
    case "compositionupdate":
    case "beforeblur":
    case "afterblur":
    case "beforeinput":
    case "blur":
    case "fullscreenchange":
    case "focus":
    case "hashchange":
    case "popstate":
    case "select":
    case "selectstart":
      return 1;
    case "drag":
    case "dragenter":
    case "dragexit":
    case "dragleave":
    case "dragover":
    case "mousemove":
    case "mouseout":
    case "mouseover":
    case "pointermove":
    case "pointerout":
    case "pointerover":
    case "scroll":
    case "toggle":
    case "touchmove":
    case "wheel":
    case "mouseenter":
    case "mouseleave":
    case "pointerenter":
    case "pointerleave":
      return 4;
    case "message":
      switch (eg()) {
        case uu:
          return 1;
        case mp:
          return 4;
        case Ii:
        case tg:
          return 16;
        case hp:
          return 536870912;
        default:
          return 16;
      }
    default:
      return 16;
  }
}
var rn = null, pu = null, vi = null;
function Ep() {
  if (vi)
    return vi;
  var e, t = pu, n = t.length, r, o = "value" in rn ? rn.value : rn.textContent, i = o.length;
  for (e = 0; e < n && t[e] === o[e]; e++)
    ;
  var l = n - e;
  for (r = 1; r <= l && t[n - r] === o[i - r]; r++)
    ;
  return vi = o.slice(e, 1 < r ? 1 - r : void 0);
}
function xi(e) {
  var t = e.keyCode;
  return "charCode" in e ? (e = e.charCode, e === 0 && t === 13 && (e = 13)) : e = t, e === 10 && (e = 13), 32 <= e || e === 13 ? e : 0;
}
function ti() {
  return !0;
}
function Dc() {
  return !1;
}
function nt(e) {
  function t(n, r, o, i, l) {
    this._reactName = n, this._targetInst = o, this.type = r, this.nativeEvent = i, this.target = l, this.currentTarget = null;
    for (var s in e)
      e.hasOwnProperty(s) && (n = e[s], this[s] = n ? n(i) : i[s]);
    return this.isDefaultPrevented = (i.defaultPrevented != null ? i.defaultPrevented : i.returnValue === !1) ? ti : Dc, this.isPropagationStopped = Dc, this;
  }
  return se(t.prototype, { preventDefault: function() {
    this.defaultPrevented = !0;
    var n = this.nativeEvent;
    n && (n.preventDefault ? n.preventDefault() : typeof n.returnValue != "unknown" && (n.returnValue = !1), this.isDefaultPrevented = ti);
  }, stopPropagation: function() {
    var n = this.nativeEvent;
    n && (n.stopPropagation ? n.stopPropagation() : typeof n.cancelBubble != "unknown" && (n.cancelBubble = !0), this.isPropagationStopped = ti);
  }, persist: function() {
  }, isPersistent: ti }), t;
}
var Er = { eventPhase: 0, bubbles: 0, cancelable: 0, timeStamp: function(e) {
  return e.timeStamp || Date.now();
}, defaultPrevented: 0, isTrusted: 0 }, mu = nt(Er), Lo = se({}, Er, { view: 0, detail: 0 }), mg = nt(Lo), ys, vs, Ar, dl = se({}, Lo, { screenX: 0, screenY: 0, clientX: 0, clientY: 0, pageX: 0, pageY: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, getModifierState: hu, button: 0, buttons: 0, relatedTarget: function(e) {
  return e.relatedTarget === void 0 ? e.fromElement === e.srcElement ? e.toElement : e.fromElement : e.relatedTarget;
}, movementX: function(e) {
  return "movementX" in e ? e.movementX : (e !== Ar && (Ar && e.type === "mousemove" ? (ys = e.screenX - Ar.screenX, vs = e.screenY - Ar.screenY) : vs = ys = 0, Ar = e), ys);
}, movementY: function(e) {
  return "movementY" in e ? e.movementY : vs;
} }), Fc = nt(dl), hg = se({}, dl, { dataTransfer: 0 }), gg = nt(hg), yg = se({}, Lo, { relatedTarget: 0 }), xs = nt(yg), vg = se({}, Er, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }), xg = nt(vg), Sg = se({}, Er, { clipboardData: function(e) {
  return "clipboardData" in e ? e.clipboardData : window.clipboardData;
} }), wg = nt(Sg), kg = se({}, Er, { data: 0 }), Bc = nt(kg), Cg = {
  Esc: "Escape",
  Spacebar: " ",
  Left: "ArrowLeft",
  Up: "ArrowUp",
  Right: "ArrowRight",
  Down: "ArrowDown",
  Del: "Delete",
  Win: "OS",
  Menu: "ContextMenu",
  Apps: "ContextMenu",
  Scroll: "ScrollLock",
  MozPrintableKey: "Unidentified"
}, Eg = {
  8: "Backspace",
  9: "Tab",
  12: "Clear",
  13: "Enter",
  16: "Shift",
  17: "Control",
  18: "Alt",
  19: "Pause",
  20: "CapsLock",
  27: "Escape",
  32: " ",
  33: "PageUp",
  34: "PageDown",
  35: "End",
  36: "Home",
  37: "ArrowLeft",
  38: "ArrowUp",
  39: "ArrowRight",
  40: "ArrowDown",
  45: "Insert",
  46: "Delete",
  112: "F1",
  113: "F2",
  114: "F3",
  115: "F4",
  116: "F5",
  117: "F6",
  118: "F7",
  119: "F8",
  120: "F9",
  121: "F10",
  122: "F11",
  123: "F12",
  144: "NumLock",
  145: "ScrollLock",
  224: "Meta"
}, _g = { Alt: "altKey", Control: "ctrlKey", Meta: "metaKey", Shift: "shiftKey" };
function $g(e) {
  var t = this.nativeEvent;
  return t.getModifierState ? t.getModifierState(e) : (e = _g[e]) ? !!t[e] : !1;
}
function hu() {
  return $g;
}
var Pg = se({}, Lo, { key: function(e) {
  if (e.key) {
    var t = Cg[e.key] || e.key;
    if (t !== "Unidentified")
      return t;
  }
  return e.type === "keypress" ? (e = xi(e), e === 13 ? "Enter" : String.fromCharCode(e)) : e.type === "keydown" || e.type === "keyup" ? Eg[e.keyCode] || "Unidentified" : "";
}, code: 0, location: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, repeat: 0, locale: 0, getModifierState: hu, charCode: function(e) {
  return e.type === "keypress" ? xi(e) : 0;
}, keyCode: function(e) {
  return e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
}, which: function(e) {
  return e.type === "keypress" ? xi(e) : e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
} }), Tg = nt(Pg), Rg = se({}, dl, { pointerId: 0, width: 0, height: 0, pressure: 0, tangentialPressure: 0, tiltX: 0, tiltY: 0, twist: 0, pointerType: 0, isPrimary: 0 }), Wc = nt(Rg), Og = se({}, Lo, { touches: 0, targetTouches: 0, changedTouches: 0, altKey: 0, metaKey: 0, ctrlKey: 0, shiftKey: 0, getModifierState: hu }), Mg = nt(Og), Ng = se({}, Er, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }), zg = nt(Ng), Lg = se({}, dl, {
  deltaX: function(e) {
    return "deltaX" in e ? e.deltaX : "wheelDeltaX" in e ? -e.wheelDeltaX : 0;
  },
  deltaY: function(e) {
    return "deltaY" in e ? e.deltaY : "wheelDeltaY" in e ? -e.wheelDeltaY : "wheelDelta" in e ? -e.wheelDelta : 0;
  },
  deltaZ: 0,
  deltaMode: 0
}), jg = nt(Lg), Ig = [9, 13, 27, 32], gu = Ut && "CompositionEvent" in window, qr = null;
Ut && "documentMode" in document && (qr = document.documentMode);
var Ag = Ut && "TextEvent" in window && !qr, _p = Ut && (!gu || qr && 8 < qr && 11 >= qr), Uc = String.fromCharCode(32), Vc = !1;
function $p(e, t) {
  switch (e) {
    case "keyup":
      return Ig.indexOf(t.keyCode) !== -1;
    case "keydown":
      return t.keyCode !== 229;
    case "keypress":
    case "mousedown":
    case "focusout":
      return !0;
    default:
      return !1;
  }
}
function Pp(e) {
  return e = e.detail, typeof e == "object" && "data" in e ? e.data : null;
}
var Yn = !1;
function bg(e, t) {
  switch (e) {
    case "compositionend":
      return Pp(t);
    case "keypress":
      return t.which !== 32 ? null : (Vc = !0, Uc);
    case "textInput":
      return e = t.data, e === Uc && Vc ? null : e;
    default:
      return null;
  }
}
function Dg(e, t) {
  if (Yn)
    return e === "compositionend" || !gu && $p(e, t) ? (e = Ep(), vi = pu = rn = null, Yn = !1, e) : null;
  switch (e) {
    case "paste":
      return null;
    case "keypress":
      if (!(t.ctrlKey || t.altKey || t.metaKey) || t.ctrlKey && t.altKey) {
        if (t.char && 1 < t.char.length)
          return t.char;
        if (t.which)
          return String.fromCharCode(t.which);
      }
      return null;
    case "compositionend":
      return _p && t.locale !== "ko" ? null : t.data;
    default:
      return null;
  }
}
var Fg = { color: !0, date: !0, datetime: !0, "datetime-local": !0, email: !0, month: !0, number: !0, password: !0, range: !0, search: !0, tel: !0, text: !0, time: !0, url: !0, week: !0 };
function Hc(e) {
  var t = e && e.nodeName && e.nodeName.toLowerCase();
  return t === "input" ? !!Fg[e.type] : t === "textarea";
}
function Tp(e, t, n, r) {
  ip(r), t = Fi(t, "onChange"), 0 < t.length && (n = new mu("onChange", "change", null, n, r), e.push({ event: n, listeners: t }));
}
var Jr = null, po = null;
function Bg(e) {
  Dp(e, 0);
}
function pl(e) {
  var t = qn(e);
  if (qd(t))
    return e;
}
function Wg(e, t) {
  if (e === "change")
    return t;
}
var Rp = !1;
if (Ut) {
  var Ss;
  if (Ut) {
    var ws = "oninput" in document;
    if (!ws) {
      var Kc = document.createElement("div");
      Kc.setAttribute("oninput", "return;"), ws = typeof Kc.oninput == "function";
    }
    Ss = ws;
  } else
    Ss = !1;
  Rp = Ss && (!document.documentMode || 9 < document.documentMode);
}
function Gc() {
  Jr && (Jr.detachEvent("onpropertychange", Op), po = Jr = null);
}
function Op(e) {
  if (e.propertyName === "value" && pl(po)) {
    var t = [];
    Tp(t, po, e, au(e)), up(Bg, t);
  }
}
function Ug(e, t, n) {
  e === "focusin" ? (Gc(), Jr = t, po = n, Jr.attachEvent("onpropertychange", Op)) : e === "focusout" && Gc();
}
function Vg(e) {
  if (e === "selectionchange" || e === "keyup" || e === "keydown")
    return pl(po);
}
function Hg(e, t) {
  if (e === "click")
    return pl(t);
}
function Kg(e, t) {
  if (e === "input" || e === "change")
    return pl(t);
}
function Gg(e, t) {
  return e === t && (e !== 0 || 1 / e === 1 / t) || e !== e && t !== t;
}
var $t = typeof Object.is == "function" ? Object.is : Gg;
function mo(e, t) {
  if ($t(e, t))
    return !0;
  if (typeof e != "object" || e === null || typeof t != "object" || t === null)
    return !1;
  var n = Object.keys(e), r = Object.keys(t);
  if (n.length !== r.length)
    return !1;
  for (r = 0; r < n.length; r++) {
    var o = n[r];
    if (!Ys.call(t, o) || !$t(e[o], t[o]))
      return !1;
  }
  return !0;
}
function Qc(e) {
  for (; e && e.firstChild; )
    e = e.firstChild;
  return e;
}
function Yc(e, t) {
  var n = Qc(e);
  e = 0;
  for (var r; n; ) {
    if (n.nodeType === 3) {
      if (r = e + n.textContent.length, e <= t && r >= t)
        return { node: n, offset: t - e };
      e = r;
    }
    e: {
      for (; n; ) {
        if (n.nextSibling) {
          n = n.nextSibling;
          break e;
        }
        n = n.parentNode;
      }
      n = void 0;
    }
    n = Qc(n);
  }
}
function Mp(e, t) {
  return e && t ? e === t ? !0 : e && e.nodeType === 3 ? !1 : t && t.nodeType === 3 ? Mp(e, t.parentNode) : "contains" in e ? e.contains(t) : e.compareDocumentPosition ? !!(e.compareDocumentPosition(t) & 16) : !1 : !1;
}
function Np() {
  for (var e = window, t = zi(); t instanceof e.HTMLIFrameElement; ) {
    try {
      var n = typeof t.contentWindow.location.href == "string";
    } catch {
      n = !1;
    }
    if (n)
      e = t.contentWindow;
    else
      break;
    t = zi(e.document);
  }
  return t;
}
function yu(e) {
  var t = e && e.nodeName && e.nodeName.toLowerCase();
  return t && (t === "input" && (e.type === "text" || e.type === "search" || e.type === "tel" || e.type === "url" || e.type === "password") || t === "textarea" || e.contentEditable === "true");
}
function Qg(e) {
  var t = Np(), n = e.focusedElem, r = e.selectionRange;
  if (t !== n && n && n.ownerDocument && Mp(n.ownerDocument.documentElement, n)) {
    if (r !== null && yu(n)) {
      if (t = r.start, e = r.end, e === void 0 && (e = t), "selectionStart" in n)
        n.selectionStart = t, n.selectionEnd = Math.min(e, n.value.length);
      else if (e = (t = n.ownerDocument || document) && t.defaultView || window, e.getSelection) {
        e = e.getSelection();
        var o = n.textContent.length, i = Math.min(r.start, o);
        r = r.end === void 0 ? i : Math.min(r.end, o), !e.extend && i > r && (o = r, r = i, i = o), o = Yc(n, i);
        var l = Yc(
          n,
          r
        );
        o && l && (e.rangeCount !== 1 || e.anchorNode !== o.node || e.anchorOffset !== o.offset || e.focusNode !== l.node || e.focusOffset !== l.offset) && (t = t.createRange(), t.setStart(o.node, o.offset), e.removeAllRanges(), i > r ? (e.addRange(t), e.extend(l.node, l.offset)) : (t.setEnd(l.node, l.offset), e.addRange(t)));
      }
    }
    for (t = [], e = n; e = e.parentNode; )
      e.nodeType === 1 && t.push({ element: e, left: e.scrollLeft, top: e.scrollTop });
    for (typeof n.focus == "function" && n.focus(), n = 0; n < t.length; n++)
      e = t[n], e.element.scrollLeft = e.left, e.element.scrollTop = e.top;
  }
}
var Yg = Ut && "documentMode" in document && 11 >= document.documentMode, Xn = null, ma = null, eo = null, ha = !1;
function Xc(e, t, n) {
  var r = n.window === n ? n.document : n.nodeType === 9 ? n : n.ownerDocument;
  ha || Xn == null || Xn !== zi(r) || (r = Xn, "selectionStart" in r && yu(r) ? r = { start: r.selectionStart, end: r.selectionEnd } : (r = (r.ownerDocument && r.ownerDocument.defaultView || window).getSelection(), r = { anchorNode: r.anchorNode, anchorOffset: r.anchorOffset, focusNode: r.focusNode, focusOffset: r.focusOffset }), eo && mo(eo, r) || (eo = r, r = Fi(ma, "onSelect"), 0 < r.length && (t = new mu("onSelect", "select", null, t, n), e.push({ event: t, listeners: r }), t.target = Xn)));
}
function ni(e, t) {
  var n = {};
  return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit" + e] = "webkit" + t, n["Moz" + e] = "moz" + t, n;
}
var Zn = { animationend: ni("Animation", "AnimationEnd"), animationiteration: ni("Animation", "AnimationIteration"), animationstart: ni("Animation", "AnimationStart"), transitionend: ni("Transition", "TransitionEnd") }, ks = {}, zp = {};
Ut && (zp = document.createElement("div").style, "AnimationEvent" in window || (delete Zn.animationend.animation, delete Zn.animationiteration.animation, delete Zn.animationstart.animation), "TransitionEvent" in window || delete Zn.transitionend.transition);
function ml(e) {
  if (ks[e])
    return ks[e];
  if (!Zn[e])
    return e;
  var t = Zn[e], n;
  for (n in t)
    if (t.hasOwnProperty(n) && n in zp)
      return ks[e] = t[n];
  return e;
}
var Lp = ml("animationend"), jp = ml("animationiteration"), Ip = ml("animationstart"), Ap = ml("transitionend"), bp = /* @__PURE__ */ new Map(), Zc = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
function yn(e, t) {
  bp.set(e, t), In(t, [e]);
}
for (var Cs = 0; Cs < Zc.length; Cs++) {
  var Es = Zc[Cs], Xg = Es.toLowerCase(), Zg = Es[0].toUpperCase() + Es.slice(1);
  yn(Xg, "on" + Zg);
}
yn(Lp, "onAnimationEnd");
yn(jp, "onAnimationIteration");
yn(Ip, "onAnimationStart");
yn("dblclick", "onDoubleClick");
yn("focusin", "onFocus");
yn("focusout", "onBlur");
yn(Ap, "onTransitionEnd");
mr("onMouseEnter", ["mouseout", "mouseover"]);
mr("onMouseLeave", ["mouseout", "mouseover"]);
mr("onPointerEnter", ["pointerout", "pointerover"]);
mr("onPointerLeave", ["pointerout", "pointerover"]);
In("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" "));
In("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));
In("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]);
In("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" "));
In("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" "));
In("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
var Gr = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), qg = new Set("cancel close invalid load scroll toggle".split(" ").concat(Gr));
function qc(e, t, n) {
  var r = e.type || "unknown-event";
  e.currentTarget = n, X0(r, t, void 0, e), e.currentTarget = null;
}
function Dp(e, t) {
  t = (t & 4) !== 0;
  for (var n = 0; n < e.length; n++) {
    var r = e[n], o = r.event;
    r = r.listeners;
    e: {
      var i = void 0;
      if (t)
        for (var l = r.length - 1; 0 <= l; l--) {
          var s = r[l], a = s.instance, u = s.currentTarget;
          if (s = s.listener, a !== i && o.isPropagationStopped())
            break e;
          qc(o, s, u), i = a;
        }
      else
        for (l = 0; l < r.length; l++) {
          if (s = r[l], a = s.instance, u = s.currentTarget, s = s.listener, a !== i && o.isPropagationStopped())
            break e;
          qc(o, s, u), i = a;
        }
    }
  }
  if (ji)
    throw e = ca, ji = !1, ca = null, e;
}
function q(e, t) {
  var n = t[Sa];
  n === void 0 && (n = t[Sa] = /* @__PURE__ */ new Set());
  var r = e + "__bubble";
  n.has(r) || (Fp(t, e, 2, !1), n.add(r));
}
function _s(e, t, n) {
  var r = 0;
  t && (r |= 4), Fp(n, e, r, t);
}
var ri = "_reactListening" + Math.random().toString(36).slice(2);
function ho(e) {
  if (!e[ri]) {
    e[ri] = !0, Gd.forEach(function(n) {
      n !== "selectionchange" && (qg.has(n) || _s(n, !1, e), _s(n, !0, e));
    });
    var t = e.nodeType === 9 ? e : e.ownerDocument;
    t === null || t[ri] || (t[ri] = !0, _s("selectionchange", !1, t));
  }
}
function Fp(e, t, n, r) {
  switch (Cp(t)) {
    case 1:
      var o = dg;
      break;
    case 4:
      o = pg;
      break;
    default:
      o = du;
  }
  n = o.bind(null, t, n, e), o = void 0, !ua || t !== "touchstart" && t !== "touchmove" && t !== "wheel" || (o = !0), r ? o !== void 0 ? e.addEventListener(t, n, { capture: !0, passive: o }) : e.addEventListener(t, n, !0) : o !== void 0 ? e.addEventListener(t, n, { passive: o }) : e.addEventListener(t, n, !1);
}
function $s(e, t, n, r, o) {
  var i = r;
  if (!(t & 1) && !(t & 2) && r !== null)
    e:
      for (; ; ) {
        if (r === null)
          return;
        var l = r.tag;
        if (l === 3 || l === 4) {
          var s = r.stateNode.containerInfo;
          if (s === o || s.nodeType === 8 && s.parentNode === o)
            break;
          if (l === 4)
            for (l = r.return; l !== null; ) {
              var a = l.tag;
              if ((a === 3 || a === 4) && (a = l.stateNode.containerInfo, a === o || a.nodeType === 8 && a.parentNode === o))
                return;
              l = l.return;
            }
          for (; s !== null; ) {
            if (l = En(s), l === null)
              return;
            if (a = l.tag, a === 5 || a === 6) {
              r = i = l;
              continue e;
            }
            s = s.parentNode;
          }
        }
        r = r.return;
      }
  up(function() {
    var u = i, c = au(n), f = [];
    e: {
      var p = bp.get(e);
      if (p !== void 0) {
        var v = mu, y = e;
        switch (e) {
          case "keypress":
            if (xi(n) === 0)
              break e;
          case "keydown":
          case "keyup":
            v = Tg;
            break;
          case "focusin":
            y = "focus", v = xs;
            break;
          case "focusout":
            y = "blur", v = xs;
            break;
          case "beforeblur":
          case "afterblur":
            v = xs;
            break;
          case "click":
            if (n.button === 2)
              break e;
          case "auxclick":
          case "dblclick":
          case "mousedown":
          case "mousemove":
          case "mouseup":
          case "mouseout":
          case "mouseover":
          case "contextmenu":
            v = Fc;
            break;
          case "drag":
          case "dragend":
          case "dragenter":
          case "dragexit":
          case "dragleave":
          case "dragover":
          case "dragstart":
          case "drop":
            v = gg;
            break;
          case "touchcancel":
          case "touchend":
          case "touchmove":
          case "touchstart":
            v = Mg;
            break;
          case Lp:
          case jp:
          case Ip:
            v = xg;
            break;
          case Ap:
            v = zg;
            break;
          case "scroll":
            v = mg;
            break;
          case "wheel":
            v = jg;
            break;
          case "copy":
          case "cut":
          case "paste":
            v = wg;
            break;
          case "gotpointercapture":
          case "lostpointercapture":
          case "pointercancel":
          case "pointerdown":
          case "pointermove":
          case "pointerout":
          case "pointerover":
          case "pointerup":
            v = Wc;
        }
        var g = (t & 4) !== 0, _ = !g && e === "scroll", m = g ? p !== null ? p + "Capture" : null : p;
        g = [];
        for (var d = u, h; d !== null; ) {
          h = d;
          var x = h.stateNode;
          if (h.tag === 5 && x !== null && (h = x, m !== null && (x = ao(d, m), x != null && g.push(go(d, x, h)))), _)
            break;
          d = d.return;
        }
        0 < g.length && (p = new v(p, y, null, n, c), f.push({ event: p, listeners: g }));
      }
    }
    if (!(t & 7)) {
      e: {
        if (p = e === "mouseover" || e === "pointerover", v = e === "mouseout" || e === "pointerout", p && n !== sa && (y = n.relatedTarget || n.fromElement) && (En(y) || y[Vt]))
          break e;
        if ((v || p) && (p = c.window === c ? c : (p = c.ownerDocument) ? p.defaultView || p.parentWindow : window, v ? (y = n.relatedTarget || n.toElement, v = u, y = y ? En(y) : null, y !== null && (_ = An(y), y !== _ || y.tag !== 5 && y.tag !== 6) && (y = null)) : (v = null, y = u), v !== y)) {
          if (g = Fc, x = "onMouseLeave", m = "onMouseEnter", d = "mouse", (e === "pointerout" || e === "pointerover") && (g = Wc, x = "onPointerLeave", m = "onPointerEnter", d = "pointer"), _ = v == null ? p : qn(v), h = y == null ? p : qn(y), p = new g(x, d + "leave", v, n, c), p.target = _, p.relatedTarget = h, x = null, En(c) === u && (g = new g(m, d + "enter", y, n, c), g.target = h, g.relatedTarget = _, x = g), _ = x, v && y)
            t: {
              for (g = v, m = y, d = 0, h = g; h; h = Dn(h))
                d++;
              for (h = 0, x = m; x; x = Dn(x))
                h++;
              for (; 0 < d - h; )
                g = Dn(g), d--;
              for (; 0 < h - d; )
                m = Dn(m), h--;
              for (; d--; ) {
                if (g === m || m !== null && g === m.alternate)
                  break t;
                g = Dn(g), m = Dn(m);
              }
              g = null;
            }
          else
            g = null;
          v !== null && Jc(f, p, v, g, !1), y !== null && _ !== null && Jc(f, _, y, g, !0);
        }
      }
      e: {
        if (p = u ? qn(u) : window, v = p.nodeName && p.nodeName.toLowerCase(), v === "select" || v === "input" && p.type === "file")
          var E = Wg;
        else if (Hc(p))
          if (Rp)
            E = Kg;
          else {
            E = Vg;
            var k = Ug;
          }
        else
          (v = p.nodeName) && v.toLowerCase() === "input" && (p.type === "checkbox" || p.type === "radio") && (E = Hg);
        if (E && (E = E(e, u))) {
          Tp(f, E, n, c);
          break e;
        }
        k && k(e, p, u), e === "focusout" && (k = p._wrapperState) && k.controlled && p.type === "number" && na(p, "number", p.value);
      }
      switch (k = u ? qn(u) : window, e) {
        case "focusin":
          (Hc(k) || k.contentEditable === "true") && (Xn = k, ma = u, eo = null);
          break;
        case "focusout":
          eo = ma = Xn = null;
          break;
        case "mousedown":
          ha = !0;
          break;
        case "contextmenu":
        case "mouseup":
        case "dragend":
          ha = !1, Xc(f, n, c);
          break;
        case "selectionchange":
          if (Yg)
            break;
        case "keydown":
        case "keyup":
          Xc(f, n, c);
      }
      var w;
      if (gu)
        e: {
          switch (e) {
            case "compositionstart":
              var T = "onCompositionStart";
              break e;
            case "compositionend":
              T = "onCompositionEnd";
              break e;
            case "compositionupdate":
              T = "onCompositionUpdate";
              break e;
          }
          T = void 0;
        }
      else
        Yn ? $p(e, n) && (T = "onCompositionEnd") : e === "keydown" && n.keyCode === 229 && (T = "onCompositionStart");
      T && (_p && n.locale !== "ko" && (Yn || T !== "onCompositionStart" ? T === "onCompositionEnd" && Yn && (w = Ep()) : (rn = c, pu = "value" in rn ? rn.value : rn.textContent, Yn = !0)), k = Fi(u, T), 0 < k.length && (T = new Bc(T, e, null, n, c), f.push({ event: T, listeners: k }), w ? T.data = w : (w = Pp(n), w !== null && (T.data = w)))), (w = Ag ? bg(e, n) : Dg(e, n)) && (u = Fi(u, "onBeforeInput"), 0 < u.length && (c = new Bc("onBeforeInput", "beforeinput", null, n, c), f.push({ event: c, listeners: u }), c.data = w));
    }
    Dp(f, t);
  });
}
function go(e, t, n) {
  return { instance: e, listener: t, currentTarget: n };
}
function Fi(e, t) {
  for (var n = t + "Capture", r = []; e !== null; ) {
    var o = e, i = o.stateNode;
    o.tag === 5 && i !== null && (o = i, i = ao(e, n), i != null && r.unshift(go(e, i, o)), i = ao(e, t), i != null && r.push(go(e, i, o))), e = e.return;
  }
  return r;
}
function Dn(e) {
  if (e === null)
    return null;
  do
    e = e.return;
  while (e && e.tag !== 5);
  return e || null;
}
function Jc(e, t, n, r, o) {
  for (var i = t._reactName, l = []; n !== null && n !== r; ) {
    var s = n, a = s.alternate, u = s.stateNode;
    if (a !== null && a === r)
      break;
    s.tag === 5 && u !== null && (s = u, o ? (a = ao(n, i), a != null && l.unshift(go(n, a, s))) : o || (a = ao(n, i), a != null && l.push(go(n, a, s)))), n = n.return;
  }
  l.length !== 0 && e.push({ event: t, listeners: l });
}
var Jg = /\r\n?/g, ey = /\u0000|\uFFFD/g;
function ef(e) {
  return (typeof e == "string" ? e : "" + e).replace(Jg, `
`).replace(ey, "");
}
function oi(e, t, n) {
  if (t = ef(t), ef(e) !== t && n)
    throw Error(P(425));
}
function Bi() {
}
var ga = null, ya = null;
function va(e, t) {
  return e === "textarea" || e === "noscript" || typeof t.children == "string" || typeof t.children == "number" || typeof t.dangerouslySetInnerHTML == "object" && t.dangerouslySetInnerHTML !== null && t.dangerouslySetInnerHTML.__html != null;
}
var xa = typeof setTimeout == "function" ? setTimeout : void 0, ty = typeof clearTimeout == "function" ? clearTimeout : void 0, tf = typeof Promise == "function" ? Promise : void 0, ny = typeof queueMicrotask == "function" ? queueMicrotask : typeof tf < "u" ? function(e) {
  return tf.resolve(null).then(e).catch(ry);
} : xa;
function ry(e) {
  setTimeout(function() {
    throw e;
  });
}
function Ps(e, t) {
  var n = t, r = 0;
  do {
    var o = n.nextSibling;
    if (e.removeChild(n), o && o.nodeType === 8)
      if (n = o.data, n === "/$") {
        if (r === 0) {
          e.removeChild(o), fo(t);
          return;
        }
        r--;
      } else
        n !== "$" && n !== "$?" && n !== "$!" || r++;
    n = o;
  } while (n);
  fo(t);
}
function cn(e) {
  for (; e != null; e = e.nextSibling) {
    var t = e.nodeType;
    if (t === 1 || t === 3)
      break;
    if (t === 8) {
      if (t = e.data, t === "$" || t === "$!" || t === "$?")
        break;
      if (t === "/$")
        return null;
    }
  }
  return e;
}
function nf(e) {
  e = e.previousSibling;
  for (var t = 0; e; ) {
    if (e.nodeType === 8) {
      var n = e.data;
      if (n === "$" || n === "$!" || n === "$?") {
        if (t === 0)
          return e;
        t--;
      } else
        n === "/$" && t++;
    }
    e = e.previousSibling;
  }
  return null;
}
var _r = Math.random().toString(36).slice(2), Nt = "__reactFiber$" + _r, yo = "__reactProps$" + _r, Vt = "__reactContainer$" + _r, Sa = "__reactEvents$" + _r, oy = "__reactListeners$" + _r, iy = "__reactHandles$" + _r;
function En(e) {
  var t = e[Nt];
  if (t)
    return t;
  for (var n = e.parentNode; n; ) {
    if (t = n[Vt] || n[Nt]) {
      if (n = t.alternate, t.child !== null || n !== null && n.child !== null)
        for (e = nf(e); e !== null; ) {
          if (n = e[Nt])
            return n;
          e = nf(e);
        }
      return t;
    }
    e = n, n = e.parentNode;
  }
  return null;
}
function jo(e) {
  return e = e[Nt] || e[Vt], !e || e.tag !== 5 && e.tag !== 6 && e.tag !== 13 && e.tag !== 3 ? null : e;
}
function qn(e) {
  if (e.tag === 5 || e.tag === 6)
    return e.stateNode;
  throw Error(P(33));
}
function hl(e) {
  return e[yo] || null;
}
var wa = [], Jn = -1;
function vn(e) {
  return { current: e };
}
function ee(e) {
  0 > Jn || (e.current = wa[Jn], wa[Jn] = null, Jn--);
}
function Y(e, t) {
  Jn++, wa[Jn] = e.current, e.current = t;
}
var gn = {}, Le = vn(gn), Ue = vn(!1), Mn = gn;
function hr(e, t) {
  var n = e.type.contextTypes;
  if (!n)
    return gn;
  var r = e.stateNode;
  if (r && r.__reactInternalMemoizedUnmaskedChildContext === t)
    return r.__reactInternalMemoizedMaskedChildContext;
  var o = {}, i;
  for (i in n)
    o[i] = t[i];
  return r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = t, e.__reactInternalMemoizedMaskedChildContext = o), o;
}
function Ve(e) {
  return e = e.childContextTypes, e != null;
}
function Wi() {
  ee(Ue), ee(Le);
}
function rf(e, t, n) {
  if (Le.current !== gn)
    throw Error(P(168));
  Y(Le, t), Y(Ue, n);
}
function Bp(e, t, n) {
  var r = e.stateNode;
  if (t = t.childContextTypes, typeof r.getChildContext != "function")
    return n;
  r = r.getChildContext();
  for (var o in r)
    if (!(o in t))
      throw Error(P(108, U0(e) || "Unknown", o));
  return se({}, n, r);
}
function Ui(e) {
  return e = (e = e.stateNode) && e.__reactInternalMemoizedMergedChildContext || gn, Mn = Le.current, Y(Le, e), Y(Ue, Ue.current), !0;
}
function of(e, t, n) {
  var r = e.stateNode;
  if (!r)
    throw Error(P(169));
  n ? (e = Bp(e, t, Mn), r.__reactInternalMemoizedMergedChildContext = e, ee(Ue), ee(Le), Y(Le, e)) : ee(Ue), Y(Ue, n);
}
var bt = null, gl = !1, Ts = !1;
function Wp(e) {
  bt === null ? bt = [e] : bt.push(e);
}
function ly(e) {
  gl = !0, Wp(e);
}
function xn() {
  if (!Ts && bt !== null) {
    Ts = !0;
    var e = 0, t = K;
    try {
      var n = bt;
      for (K = 1; e < n.length; e++) {
        var r = n[e];
        do
          r = r(!0);
        while (r !== null);
      }
      bt = null, gl = !1;
    } catch (o) {
      throw bt !== null && (bt = bt.slice(e + 1)), pp(uu, xn), o;
    } finally {
      K = t, Ts = !1;
    }
  }
  return null;
}
var er = [], tr = 0, Vi = null, Hi = 0, st = [], at = 0, Nn = null, Ft = 1, Bt = "";
function Sn(e, t) {
  er[tr++] = Hi, er[tr++] = Vi, Vi = e, Hi = t;
}
function Up(e, t, n) {
  st[at++] = Ft, st[at++] = Bt, st[at++] = Nn, Nn = e;
  var r = Ft;
  e = Bt;
  var o = 32 - Et(r) - 1;
  r &= ~(1 << o), n += 1;
  var i = 32 - Et(t) + o;
  if (30 < i) {
    var l = o - o % 5;
    i = (r & (1 << l) - 1).toString(32), r >>= l, o -= l, Ft = 1 << 32 - Et(t) + o | n << o | r, Bt = i + e;
  } else
    Ft = 1 << i | n << o | r, Bt = e;
}
function vu(e) {
  e.return !== null && (Sn(e, 1), Up(e, 1, 0));
}
function xu(e) {
  for (; e === Vi; )
    Vi = er[--tr], er[tr] = null, Hi = er[--tr], er[tr] = null;
  for (; e === Nn; )
    Nn = st[--at], st[at] = null, Bt = st[--at], st[at] = null, Ft = st[--at], st[at] = null;
}
var qe = null, Ze = null, re = !1, kt = null;
function Vp(e, t) {
  var n = ct(5, null, null, 0);
  n.elementType = "DELETED", n.stateNode = t, n.return = e, t = e.deletions, t === null ? (e.deletions = [n], e.flags |= 16) : t.push(n);
}
function lf(e, t) {
  switch (e.tag) {
    case 5:
      var n = e.type;
      return t = t.nodeType !== 1 || n.toLowerCase() !== t.nodeName.toLowerCase() ? null : t, t !== null ? (e.stateNode = t, qe = e, Ze = cn(t.firstChild), !0) : !1;
    case 6:
      return t = e.pendingProps === "" || t.nodeType !== 3 ? null : t, t !== null ? (e.stateNode = t, qe = e, Ze = null, !0) : !1;
    case 13:
      return t = t.nodeType !== 8 ? null : t, t !== null ? (n = Nn !== null ? { id: Ft, overflow: Bt } : null, e.memoizedState = { dehydrated: t, treeContext: n, retryLane: 1073741824 }, n = ct(18, null, null, 0), n.stateNode = t, n.return = e, e.child = n, qe = e, Ze = null, !0) : !1;
    default:
      return !1;
  }
}
function ka(e) {
  return (e.mode & 1) !== 0 && (e.flags & 128) === 0;
}
function Ca(e) {
  if (re) {
    var t = Ze;
    if (t) {
      var n = t;
      if (!lf(e, t)) {
        if (ka(e))
          throw Error(P(418));
        t = cn(n.nextSibling);
        var r = qe;
        t && lf(e, t) ? Vp(r, n) : (e.flags = e.flags & -4097 | 2, re = !1, qe = e);
      }
    } else {
      if (ka(e))
        throw Error(P(418));
      e.flags = e.flags & -4097 | 2, re = !1, qe = e;
    }
  }
}
function sf(e) {
  for (e = e.return; e !== null && e.tag !== 5 && e.tag !== 3 && e.tag !== 13; )
    e = e.return;
  qe = e;
}
function ii(e) {
  if (e !== qe)
    return !1;
  if (!re)
    return sf(e), re = !0, !1;
  var t;
  if ((t = e.tag !== 3) && !(t = e.tag !== 5) && (t = e.type, t = t !== "head" && t !== "body" && !va(e.type, e.memoizedProps)), t && (t = Ze)) {
    if (ka(e))
      throw Hp(), Error(P(418));
    for (; t; )
      Vp(e, t), t = cn(t.nextSibling);
  }
  if (sf(e), e.tag === 13) {
    if (e = e.memoizedState, e = e !== null ? e.dehydrated : null, !e)
      throw Error(P(317));
    e: {
      for (e = e.nextSibling, t = 0; e; ) {
        if (e.nodeType === 8) {
          var n = e.data;
          if (n === "/$") {
            if (t === 0) {
              Ze = cn(e.nextSibling);
              break e;
            }
            t--;
          } else
            n !== "$" && n !== "$!" && n !== "$?" || t++;
        }
        e = e.nextSibling;
      }
      Ze = null;
    }
  } else
    Ze = qe ? cn(e.stateNode.nextSibling) : null;
  return !0;
}
function Hp() {
  for (var e = Ze; e; )
    e = cn(e.nextSibling);
}
function gr() {
  Ze = qe = null, re = !1;
}
function Su(e) {
  kt === null ? kt = [e] : kt.push(e);
}
var sy = Qt.ReactCurrentBatchConfig;
function br(e, t, n) {
  if (e = n.ref, e !== null && typeof e != "function" && typeof e != "object") {
    if (n._owner) {
      if (n = n._owner, n) {
        if (n.tag !== 1)
          throw Error(P(309));
        var r = n.stateNode;
      }
      if (!r)
        throw Error(P(147, e));
      var o = r, i = "" + e;
      return t !== null && t.ref !== null && typeof t.ref == "function" && t.ref._stringRef === i ? t.ref : (t = function(l) {
        var s = o.refs;
        l === null ? delete s[i] : s[i] = l;
      }, t._stringRef = i, t);
    }
    if (typeof e != "string")
      throw Error(P(284));
    if (!n._owner)
      throw Error(P(290, e));
  }
  return e;
}
function li(e, t) {
  throw e = Object.prototype.toString.call(t), Error(P(31, e === "[object Object]" ? "object with keys {" + Object.keys(t).join(", ") + "}" : e));
}
function af(e) {
  var t = e._init;
  return t(e._payload);
}
function Kp(e) {
  function t(m, d) {
    if (e) {
      var h = m.deletions;
      h === null ? (m.deletions = [d], m.flags |= 16) : h.push(d);
    }
  }
  function n(m, d) {
    if (!e)
      return null;
    for (; d !== null; )
      t(m, d), d = d.sibling;
    return null;
  }
  function r(m, d) {
    for (m = /* @__PURE__ */ new Map(); d !== null; )
      d.key !== null ? m.set(d.key, d) : m.set(d.index, d), d = d.sibling;
    return m;
  }
  function o(m, d) {
    return m = mn(m, d), m.index = 0, m.sibling = null, m;
  }
  function i(m, d, h) {
    return m.index = h, e ? (h = m.alternate, h !== null ? (h = h.index, h < d ? (m.flags |= 2, d) : h) : (m.flags |= 2, d)) : (m.flags |= 1048576, d);
  }
  function l(m) {
    return e && m.alternate === null && (m.flags |= 2), m;
  }
  function s(m, d, h, x) {
    return d === null || d.tag !== 6 ? (d = js(h, m.mode, x), d.return = m, d) : (d = o(d, h), d.return = m, d);
  }
  function a(m, d, h, x) {
    var E = h.type;
    return E === Qn ? c(m, d, h.props.children, x, h.key) : d !== null && (d.elementType === E || typeof E == "object" && E !== null && E.$$typeof === Jt && af(E) === d.type) ? (x = o(d, h.props), x.ref = br(m, d, h), x.return = m, x) : (x = $i(h.type, h.key, h.props, null, m.mode, x), x.ref = br(m, d, h), x.return = m, x);
  }
  function u(m, d, h, x) {
    return d === null || d.tag !== 4 || d.stateNode.containerInfo !== h.containerInfo || d.stateNode.implementation !== h.implementation ? (d = Is(h, m.mode, x), d.return = m, d) : (d = o(d, h.children || []), d.return = m, d);
  }
  function c(m, d, h, x, E) {
    return d === null || d.tag !== 7 ? (d = Rn(h, m.mode, x, E), d.return = m, d) : (d = o(d, h), d.return = m, d);
  }
  function f(m, d, h) {
    if (typeof d == "string" && d !== "" || typeof d == "number")
      return d = js("" + d, m.mode, h), d.return = m, d;
    if (typeof d == "object" && d !== null) {
      switch (d.$$typeof) {
        case Yo:
          return h = $i(d.type, d.key, d.props, null, m.mode, h), h.ref = br(m, null, d), h.return = m, h;
        case Gn:
          return d = Is(d, m.mode, h), d.return = m, d;
        case Jt:
          var x = d._init;
          return f(m, x(d._payload), h);
      }
      if (Hr(d) || zr(d))
        return d = Rn(d, m.mode, h, null), d.return = m, d;
      li(m, d);
    }
    return null;
  }
  function p(m, d, h, x) {
    var E = d !== null ? d.key : null;
    if (typeof h == "string" && h !== "" || typeof h == "number")
      return E !== null ? null : s(m, d, "" + h, x);
    if (typeof h == "object" && h !== null) {
      switch (h.$$typeof) {
        case Yo:
          return h.key === E ? a(m, d, h, x) : null;
        case Gn:
          return h.key === E ? u(m, d, h, x) : null;
        case Jt:
          return E = h._init, p(
            m,
            d,
            E(h._payload),
            x
          );
      }
      if (Hr(h) || zr(h))
        return E !== null ? null : c(m, d, h, x, null);
      li(m, h);
    }
    return null;
  }
  function v(m, d, h, x, E) {
    if (typeof x == "string" && x !== "" || typeof x == "number")
      return m = m.get(h) || null, s(d, m, "" + x, E);
    if (typeof x == "object" && x !== null) {
      switch (x.$$typeof) {
        case Yo:
          return m = m.get(x.key === null ? h : x.key) || null, a(d, m, x, E);
        case Gn:
          return m = m.get(x.key === null ? h : x.key) || null, u(d, m, x, E);
        case Jt:
          var k = x._init;
          return v(m, d, h, k(x._payload), E);
      }
      if (Hr(x) || zr(x))
        return m = m.get(h) || null, c(d, m, x, E, null);
      li(d, x);
    }
    return null;
  }
  function y(m, d, h, x) {
    for (var E = null, k = null, w = d, T = d = 0, N = null; w !== null && T < h.length; T++) {
      w.index > T ? (N = w, w = null) : N = w.sibling;
      var O = p(m, w, h[T], x);
      if (O === null) {
        w === null && (w = N);
        break;
      }
      e && w && O.alternate === null && t(m, w), d = i(O, d, T), k === null ? E = O : k.sibling = O, k = O, w = N;
    }
    if (T === h.length)
      return n(m, w), re && Sn(m, T), E;
    if (w === null) {
      for (; T < h.length; T++)
        w = f(m, h[T], x), w !== null && (d = i(w, d, T), k === null ? E = w : k.sibling = w, k = w);
      return re && Sn(m, T), E;
    }
    for (w = r(m, w); T < h.length; T++)
      N = v(w, m, T, h[T], x), N !== null && (e && N.alternate !== null && w.delete(N.key === null ? T : N.key), d = i(N, d, T), k === null ? E = N : k.sibling = N, k = N);
    return e && w.forEach(function(F) {
      return t(m, F);
    }), re && Sn(m, T), E;
  }
  function g(m, d, h, x) {
    var E = zr(h);
    if (typeof E != "function")
      throw Error(P(150));
    if (h = E.call(h), h == null)
      throw Error(P(151));
    for (var k = E = null, w = d, T = d = 0, N = null, O = h.next(); w !== null && !O.done; T++, O = h.next()) {
      w.index > T ? (N = w, w = null) : N = w.sibling;
      var F = p(m, w, O.value, x);
      if (F === null) {
        w === null && (w = N);
        break;
      }
      e && w && F.alternate === null && t(m, w), d = i(F, d, T), k === null ? E = F : k.sibling = F, k = F, w = N;
    }
    if (O.done)
      return n(
        m,
        w
      ), re && Sn(m, T), E;
    if (w === null) {
      for (; !O.done; T++, O = h.next())
        O = f(m, O.value, x), O !== null && (d = i(O, d, T), k === null ? E = O : k.sibling = O, k = O);
      return re && Sn(m, T), E;
    }
    for (w = r(m, w); !O.done; T++, O = h.next())
      O = v(w, m, T, O.value, x), O !== null && (e && O.alternate !== null && w.delete(O.key === null ? T : O.key), d = i(O, d, T), k === null ? E = O : k.sibling = O, k = O);
    return e && w.forEach(function(A) {
      return t(m, A);
    }), re && Sn(m, T), E;
  }
  function _(m, d, h, x) {
    if (typeof h == "object" && h !== null && h.type === Qn && h.key === null && (h = h.props.children), typeof h == "object" && h !== null) {
      switch (h.$$typeof) {
        case Yo:
          e: {
            for (var E = h.key, k = d; k !== null; ) {
              if (k.key === E) {
                if (E = h.type, E === Qn) {
                  if (k.tag === 7) {
                    n(m, k.sibling), d = o(k, h.props.children), d.return = m, m = d;
                    break e;
                  }
                } else if (k.elementType === E || typeof E == "object" && E !== null && E.$$typeof === Jt && af(E) === k.type) {
                  n(m, k.sibling), d = o(k, h.props), d.ref = br(m, k, h), d.return = m, m = d;
                  break e;
                }
                n(m, k);
                break;
              } else
                t(m, k);
              k = k.sibling;
            }
            h.type === Qn ? (d = Rn(h.props.children, m.mode, x, h.key), d.return = m, m = d) : (x = $i(h.type, h.key, h.props, null, m.mode, x), x.ref = br(m, d, h), x.return = m, m = x);
          }
          return l(m);
        case Gn:
          e: {
            for (k = h.key; d !== null; ) {
              if (d.key === k)
                if (d.tag === 4 && d.stateNode.containerInfo === h.containerInfo && d.stateNode.implementation === h.implementation) {
                  n(m, d.sibling), d = o(d, h.children || []), d.return = m, m = d;
                  break e;
                } else {
                  n(m, d);
                  break;
                }
              else
                t(m, d);
              d = d.sibling;
            }
            d = Is(h, m.mode, x), d.return = m, m = d;
          }
          return l(m);
        case Jt:
          return k = h._init, _(m, d, k(h._payload), x);
      }
      if (Hr(h))
        return y(m, d, h, x);
      if (zr(h))
        return g(m, d, h, x);
      li(m, h);
    }
    return typeof h == "string" && h !== "" || typeof h == "number" ? (h = "" + h, d !== null && d.tag === 6 ? (n(m, d.sibling), d = o(d, h), d.return = m, m = d) : (n(m, d), d = js(h, m.mode, x), d.return = m, m = d), l(m)) : n(m, d);
  }
  return _;
}
var yr = Kp(!0), Gp = Kp(!1), Ki = vn(null), Gi = null, nr = null, wu = null;
function ku() {
  wu = nr = Gi = null;
}
function Cu(e) {
  var t = Ki.current;
  ee(Ki), e._currentValue = t;
}
function Ea(e, t, n) {
  for (; e !== null; ) {
    var r = e.alternate;
    if ((e.childLanes & t) !== t ? (e.childLanes |= t, r !== null && (r.childLanes |= t)) : r !== null && (r.childLanes & t) !== t && (r.childLanes |= t), e === n)
      break;
    e = e.return;
  }
}
function ur(e, t) {
  Gi = e, wu = nr = null, e = e.dependencies, e !== null && e.firstContext !== null && (e.lanes & t && (We = !0), e.firstContext = null);
}
function dt(e) {
  var t = e._currentValue;
  if (wu !== e)
    if (e = { context: e, memoizedValue: t, next: null }, nr === null) {
      if (Gi === null)
        throw Error(P(308));
      nr = e, Gi.dependencies = { lanes: 0, firstContext: e };
    } else
      nr = nr.next = e;
  return t;
}
var _n = null;
function Eu(e) {
  _n === null ? _n = [e] : _n.push(e);
}
function Qp(e, t, n, r) {
  var o = t.interleaved;
  return o === null ? (n.next = n, Eu(t)) : (n.next = o.next, o.next = n), t.interleaved = n, Ht(e, r);
}
function Ht(e, t) {
  e.lanes |= t;
  var n = e.alternate;
  for (n !== null && (n.lanes |= t), n = e, e = e.return; e !== null; )
    e.childLanes |= t, n = e.alternate, n !== null && (n.childLanes |= t), n = e, e = e.return;
  return n.tag === 3 ? n.stateNode : null;
}
var en = !1;
function _u(e) {
  e.updateQueue = { baseState: e.memoizedState, firstBaseUpdate: null, lastBaseUpdate: null, shared: { pending: null, interleaved: null, lanes: 0 }, effects: null };
}
function Yp(e, t) {
  e = e.updateQueue, t.updateQueue === e && (t.updateQueue = { baseState: e.baseState, firstBaseUpdate: e.firstBaseUpdate, lastBaseUpdate: e.lastBaseUpdate, shared: e.shared, effects: e.effects });
}
function Wt(e, t) {
  return { eventTime: e, lane: t, tag: 0, payload: null, callback: null, next: null };
}
function fn(e, t, n) {
  var r = e.updateQueue;
  if (r === null)
    return null;
  if (r = r.shared, B & 2) {
    var o = r.pending;
    return o === null ? t.next = t : (t.next = o.next, o.next = t), r.pending = t, Ht(e, n);
  }
  return o = r.interleaved, o === null ? (t.next = t, Eu(r)) : (t.next = o.next, o.next = t), r.interleaved = t, Ht(e, n);
}
function Si(e, t, n) {
  if (t = t.updateQueue, t !== null && (t = t.shared, (n & 4194240) !== 0)) {
    var r = t.lanes;
    r &= e.pendingLanes, n |= r, t.lanes = n, cu(e, n);
  }
}
function uf(e, t) {
  var n = e.updateQueue, r = e.alternate;
  if (r !== null && (r = r.updateQueue, n === r)) {
    var o = null, i = null;
    if (n = n.firstBaseUpdate, n !== null) {
      do {
        var l = { eventTime: n.eventTime, lane: n.lane, tag: n.tag, payload: n.payload, callback: n.callback, next: null };
        i === null ? o = i = l : i = i.next = l, n = n.next;
      } while (n !== null);
      i === null ? o = i = t : i = i.next = t;
    } else
      o = i = t;
    n = { baseState: r.baseState, firstBaseUpdate: o, lastBaseUpdate: i, shared: r.shared, effects: r.effects }, e.updateQueue = n;
    return;
  }
  e = n.lastBaseUpdate, e === null ? n.firstBaseUpdate = t : e.next = t, n.lastBaseUpdate = t;
}
function Qi(e, t, n, r) {
  var o = e.updateQueue;
  en = !1;
  var i = o.firstBaseUpdate, l = o.lastBaseUpdate, s = o.shared.pending;
  if (s !== null) {
    o.shared.pending = null;
    var a = s, u = a.next;
    a.next = null, l === null ? i = u : l.next = u, l = a;
    var c = e.alternate;
    c !== null && (c = c.updateQueue, s = c.lastBaseUpdate, s !== l && (s === null ? c.firstBaseUpdate = u : s.next = u, c.lastBaseUpdate = a));
  }
  if (i !== null) {
    var f = o.baseState;
    l = 0, c = u = a = null, s = i;
    do {
      var p = s.lane, v = s.eventTime;
      if ((r & p) === p) {
        c !== null && (c = c.next = {
          eventTime: v,
          lane: 0,
          tag: s.tag,
          payload: s.payload,
          callback: s.callback,
          next: null
        });
        e: {
          var y = e, g = s;
          switch (p = t, v = n, g.tag) {
            case 1:
              if (y = g.payload, typeof y == "function") {
                f = y.call(v, f, p);
                break e;
              }
              f = y;
              break e;
            case 3:
              y.flags = y.flags & -65537 | 128;
            case 0:
              if (y = g.payload, p = typeof y == "function" ? y.call(v, f, p) : y, p == null)
                break e;
              f = se({}, f, p);
              break e;
            case 2:
              en = !0;
          }
        }
        s.callback !== null && s.lane !== 0 && (e.flags |= 64, p = o.effects, p === null ? o.effects = [s] : p.push(s));
      } else
        v = { eventTime: v, lane: p, tag: s.tag, payload: s.payload, callback: s.callback, next: null }, c === null ? (u = c = v, a = f) : c = c.next = v, l |= p;
      if (s = s.next, s === null) {
        if (s = o.shared.pending, s === null)
          break;
        p = s, s = p.next, p.next = null, o.lastBaseUpdate = p, o.shared.pending = null;
      }
    } while (1);
    if (c === null && (a = f), o.baseState = a, o.firstBaseUpdate = u, o.lastBaseUpdate = c, t = o.shared.interleaved, t !== null) {
      o = t;
      do
        l |= o.lane, o = o.next;
      while (o !== t);
    } else
      i === null && (o.shared.lanes = 0);
    Ln |= l, e.lanes = l, e.memoizedState = f;
  }
}
function cf(e, t, n) {
  if (e = t.effects, t.effects = null, e !== null)
    for (t = 0; t < e.length; t++) {
      var r = e[t], o = r.callback;
      if (o !== null) {
        if (r.callback = null, r = n, typeof o != "function")
          throw Error(P(191, o));
        o.call(r);
      }
    }
}
var Io = {}, Lt = vn(Io), vo = vn(Io), xo = vn(Io);
function $n(e) {
  if (e === Io)
    throw Error(P(174));
  return e;
}
function $u(e, t) {
  switch (Y(xo, t), Y(vo, e), Y(Lt, Io), e = t.nodeType, e) {
    case 9:
    case 11:
      t = (t = t.documentElement) ? t.namespaceURI : oa(null, "");
      break;
    default:
      e = e === 8 ? t.parentNode : t, t = e.namespaceURI || null, e = e.tagName, t = oa(t, e);
  }
  ee(Lt), Y(Lt, t);
}
function vr() {
  ee(Lt), ee(vo), ee(xo);
}
function Xp(e) {
  $n(xo.current);
  var t = $n(Lt.current), n = oa(t, e.type);
  t !== n && (Y(vo, e), Y(Lt, n));
}
function Pu(e) {
  vo.current === e && (ee(Lt), ee(vo));
}
var ie = vn(0);
function Yi(e) {
  for (var t = e; t !== null; ) {
    if (t.tag === 13) {
      var n = t.memoizedState;
      if (n !== null && (n = n.dehydrated, n === null || n.data === "$?" || n.data === "$!"))
        return t;
    } else if (t.tag === 19 && t.memoizedProps.revealOrder !== void 0) {
      if (t.flags & 128)
        return t;
    } else if (t.child !== null) {
      t.child.return = t, t = t.child;
      continue;
    }
    if (t === e)
      break;
    for (; t.sibling === null; ) {
      if (t.return === null || t.return === e)
        return null;
      t = t.return;
    }
    t.sibling.return = t.return, t = t.sibling;
  }
  return null;
}
var Rs = [];
function Tu() {
  for (var e = 0; e < Rs.length; e++)
    Rs[e]._workInProgressVersionPrimary = null;
  Rs.length = 0;
}
var wi = Qt.ReactCurrentDispatcher, Os = Qt.ReactCurrentBatchConfig, zn = 0, le = null, Se = null, ke = null, Xi = !1, to = !1, So = 0, ay = 0;
function Oe() {
  throw Error(P(321));
}
function Ru(e, t) {
  if (t === null)
    return !1;
  for (var n = 0; n < t.length && n < e.length; n++)
    if (!$t(e[n], t[n]))
      return !1;
  return !0;
}
function Ou(e, t, n, r, o, i) {
  if (zn = i, le = t, t.memoizedState = null, t.updateQueue = null, t.lanes = 0, wi.current = e === null || e.memoizedState === null ? dy : py, e = n(r, o), to) {
    i = 0;
    do {
      if (to = !1, So = 0, 25 <= i)
        throw Error(P(301));
      i += 1, ke = Se = null, t.updateQueue = null, wi.current = my, e = n(r, o);
    } while (to);
  }
  if (wi.current = Zi, t = Se !== null && Se.next !== null, zn = 0, ke = Se = le = null, Xi = !1, t)
    throw Error(P(300));
  return e;
}
function Mu() {
  var e = So !== 0;
  return So = 0, e;
}
function Rt() {
  var e = { memoizedState: null, baseState: null, baseQueue: null, queue: null, next: null };
  return ke === null ? le.memoizedState = ke = e : ke = ke.next = e, ke;
}
function pt() {
  if (Se === null) {
    var e = le.alternate;
    e = e !== null ? e.memoizedState : null;
  } else
    e = Se.next;
  var t = ke === null ? le.memoizedState : ke.next;
  if (t !== null)
    ke = t, Se = e;
  else {
    if (e === null)
      throw Error(P(310));
    Se = e, e = { memoizedState: Se.memoizedState, baseState: Se.baseState, baseQueue: Se.baseQueue, queue: Se.queue, next: null }, ke === null ? le.memoizedState = ke = e : ke = ke.next = e;
  }
  return ke;
}
function wo(e, t) {
  return typeof t == "function" ? t(e) : t;
}
function Ms(e) {
  var t = pt(), n = t.queue;
  if (n === null)
    throw Error(P(311));
  n.lastRenderedReducer = e;
  var r = Se, o = r.baseQueue, i = n.pending;
  if (i !== null) {
    if (o !== null) {
      var l = o.next;
      o.next = i.next, i.next = l;
    }
    r.baseQueue = o = i, n.pending = null;
  }
  if (o !== null) {
    i = o.next, r = r.baseState;
    var s = l = null, a = null, u = i;
    do {
      var c = u.lane;
      if ((zn & c) === c)
        a !== null && (a = a.next = { lane: 0, action: u.action, hasEagerState: u.hasEagerState, eagerState: u.eagerState, next: null }), r = u.hasEagerState ? u.eagerState : e(r, u.action);
      else {
        var f = {
          lane: c,
          action: u.action,
          hasEagerState: u.hasEagerState,
          eagerState: u.eagerState,
          next: null
        };
        a === null ? (s = a = f, l = r) : a = a.next = f, le.lanes |= c, Ln |= c;
      }
      u = u.next;
    } while (u !== null && u !== i);
    a === null ? l = r : a.next = s, $t(r, t.memoizedState) || (We = !0), t.memoizedState = r, t.baseState = l, t.baseQueue = a, n.lastRenderedState = r;
  }
  if (e = n.interleaved, e !== null) {
    o = e;
    do
      i = o.lane, le.lanes |= i, Ln |= i, o = o.next;
    while (o !== e);
  } else
    o === null && (n.lanes = 0);
  return [t.memoizedState, n.dispatch];
}
function Ns(e) {
  var t = pt(), n = t.queue;
  if (n === null)
    throw Error(P(311));
  n.lastRenderedReducer = e;
  var r = n.dispatch, o = n.pending, i = t.memoizedState;
  if (o !== null) {
    n.pending = null;
    var l = o = o.next;
    do
      i = e(i, l.action), l = l.next;
    while (l !== o);
    $t(i, t.memoizedState) || (We = !0), t.memoizedState = i, t.baseQueue === null && (t.baseState = i), n.lastRenderedState = i;
  }
  return [i, r];
}
function Zp() {
}
function qp(e, t) {
  var n = le, r = pt(), o = t(), i = !$t(r.memoizedState, o);
  if (i && (r.memoizedState = o, We = !0), r = r.queue, Nu(tm.bind(null, n, r, e), [e]), r.getSnapshot !== t || i || ke !== null && ke.memoizedState.tag & 1) {
    if (n.flags |= 2048, ko(9, em.bind(null, n, r, o, t), void 0, null), Ce === null)
      throw Error(P(349));
    zn & 30 || Jp(n, t, o);
  }
  return o;
}
function Jp(e, t, n) {
  e.flags |= 16384, e = { getSnapshot: t, value: n }, t = le.updateQueue, t === null ? (t = { lastEffect: null, stores: null }, le.updateQueue = t, t.stores = [e]) : (n = t.stores, n === null ? t.stores = [e] : n.push(e));
}
function em(e, t, n, r) {
  t.value = n, t.getSnapshot = r, nm(t) && rm(e);
}
function tm(e, t, n) {
  return n(function() {
    nm(t) && rm(e);
  });
}
function nm(e) {
  var t = e.getSnapshot;
  e = e.value;
  try {
    var n = t();
    return !$t(e, n);
  } catch {
    return !0;
  }
}
function rm(e) {
  var t = Ht(e, 1);
  t !== null && _t(t, e, 1, -1);
}
function ff(e) {
  var t = Rt();
  return typeof e == "function" && (e = e()), t.memoizedState = t.baseState = e, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: wo, lastRenderedState: e }, t.queue = e, e = e.dispatch = fy.bind(null, le, e), [t.memoizedState, e];
}
function ko(e, t, n, r) {
  return e = { tag: e, create: t, destroy: n, deps: r, next: null }, t = le.updateQueue, t === null ? (t = { lastEffect: null, stores: null }, le.updateQueue = t, t.lastEffect = e.next = e) : (n = t.lastEffect, n === null ? t.lastEffect = e.next = e : (r = n.next, n.next = e, e.next = r, t.lastEffect = e)), e;
}
function om() {
  return pt().memoizedState;
}
function ki(e, t, n, r) {
  var o = Rt();
  le.flags |= e, o.memoizedState = ko(1 | t, n, void 0, r === void 0 ? null : r);
}
function yl(e, t, n, r) {
  var o = pt();
  r = r === void 0 ? null : r;
  var i = void 0;
  if (Se !== null) {
    var l = Se.memoizedState;
    if (i = l.destroy, r !== null && Ru(r, l.deps)) {
      o.memoizedState = ko(t, n, i, r);
      return;
    }
  }
  le.flags |= e, o.memoizedState = ko(1 | t, n, i, r);
}
function df(e, t) {
  return ki(8390656, 8, e, t);
}
function Nu(e, t) {
  return yl(2048, 8, e, t);
}
function im(e, t) {
  return yl(4, 2, e, t);
}
function lm(e, t) {
  return yl(4, 4, e, t);
}
function sm(e, t) {
  if (typeof t == "function")
    return e = e(), t(e), function() {
      t(null);
    };
  if (t != null)
    return e = e(), t.current = e, function() {
      t.current = null;
    };
}
function am(e, t, n) {
  return n = n != null ? n.concat([e]) : null, yl(4, 4, sm.bind(null, t, e), n);
}
function zu() {
}
function um(e, t) {
  var n = pt();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && Ru(t, r[1]) ? r[0] : (n.memoizedState = [e, t], e);
}
function cm(e, t) {
  var n = pt();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && Ru(t, r[1]) ? r[0] : (e = e(), n.memoizedState = [e, t], e);
}
function fm(e, t, n) {
  return zn & 21 ? ($t(n, t) || (n = gp(), le.lanes |= n, Ln |= n, e.baseState = !0), t) : (e.baseState && (e.baseState = !1, We = !0), e.memoizedState = n);
}
function uy(e, t) {
  var n = K;
  K = n !== 0 && 4 > n ? n : 4, e(!0);
  var r = Os.transition;
  Os.transition = {};
  try {
    e(!1), t();
  } finally {
    K = n, Os.transition = r;
  }
}
function dm() {
  return pt().memoizedState;
}
function cy(e, t, n) {
  var r = pn(e);
  if (n = { lane: r, action: n, hasEagerState: !1, eagerState: null, next: null }, pm(e))
    mm(t, n);
  else if (n = Qp(e, t, n, r), n !== null) {
    var o = Ae();
    _t(n, e, r, o), hm(n, t, r);
  }
}
function fy(e, t, n) {
  var r = pn(e), o = { lane: r, action: n, hasEagerState: !1, eagerState: null, next: null };
  if (pm(e))
    mm(t, o);
  else {
    var i = e.alternate;
    if (e.lanes === 0 && (i === null || i.lanes === 0) && (i = t.lastRenderedReducer, i !== null))
      try {
        var l = t.lastRenderedState, s = i(l, n);
        if (o.hasEagerState = !0, o.eagerState = s, $t(s, l)) {
          var a = t.interleaved;
          a === null ? (o.next = o, Eu(t)) : (o.next = a.next, a.next = o), t.interleaved = o;
          return;
        }
      } catch {
      } finally {
      }
    n = Qp(e, t, o, r), n !== null && (o = Ae(), _t(n, e, r, o), hm(n, t, r));
  }
}
function pm(e) {
  var t = e.alternate;
  return e === le || t !== null && t === le;
}
function mm(e, t) {
  to = Xi = !0;
  var n = e.pending;
  n === null ? t.next = t : (t.next = n.next, n.next = t), e.pending = t;
}
function hm(e, t, n) {
  if (n & 4194240) {
    var r = t.lanes;
    r &= e.pendingLanes, n |= r, t.lanes = n, cu(e, n);
  }
}
var Zi = { readContext: dt, useCallback: Oe, useContext: Oe, useEffect: Oe, useImperativeHandle: Oe, useInsertionEffect: Oe, useLayoutEffect: Oe, useMemo: Oe, useReducer: Oe, useRef: Oe, useState: Oe, useDebugValue: Oe, useDeferredValue: Oe, useTransition: Oe, useMutableSource: Oe, useSyncExternalStore: Oe, useId: Oe, unstable_isNewReconciler: !1 }, dy = { readContext: dt, useCallback: function(e, t) {
  return Rt().memoizedState = [e, t === void 0 ? null : t], e;
}, useContext: dt, useEffect: df, useImperativeHandle: function(e, t, n) {
  return n = n != null ? n.concat([e]) : null, ki(
    4194308,
    4,
    sm.bind(null, t, e),
    n
  );
}, useLayoutEffect: function(e, t) {
  return ki(4194308, 4, e, t);
}, useInsertionEffect: function(e, t) {
  return ki(4, 2, e, t);
}, useMemo: function(e, t) {
  var n = Rt();
  return t = t === void 0 ? null : t, e = e(), n.memoizedState = [e, t], e;
}, useReducer: function(e, t, n) {
  var r = Rt();
  return t = n !== void 0 ? n(t) : t, r.memoizedState = r.baseState = t, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: e, lastRenderedState: t }, r.queue = e, e = e.dispatch = cy.bind(null, le, e), [r.memoizedState, e];
}, useRef: function(e) {
  var t = Rt();
  return e = { current: e }, t.memoizedState = e;
}, useState: ff, useDebugValue: zu, useDeferredValue: function(e) {
  return Rt().memoizedState = e;
}, useTransition: function() {
  var e = ff(!1), t = e[0];
  return e = uy.bind(null, e[1]), Rt().memoizedState = e, [t, e];
}, useMutableSource: function() {
}, useSyncExternalStore: function(e, t, n) {
  var r = le, o = Rt();
  if (re) {
    if (n === void 0)
      throw Error(P(407));
    n = n();
  } else {
    if (n = t(), Ce === null)
      throw Error(P(349));
    zn & 30 || Jp(r, t, n);
  }
  o.memoizedState = n;
  var i = { value: n, getSnapshot: t };
  return o.queue = i, df(tm.bind(
    null,
    r,
    i,
    e
  ), [e]), r.flags |= 2048, ko(9, em.bind(null, r, i, n, t), void 0, null), n;
}, useId: function() {
  var e = Rt(), t = Ce.identifierPrefix;
  if (re) {
    var n = Bt, r = Ft;
    n = (r & ~(1 << 32 - Et(r) - 1)).toString(32) + n, t = ":" + t + "R" + n, n = So++, 0 < n && (t += "H" + n.toString(32)), t += ":";
  } else
    n = ay++, t = ":" + t + "r" + n.toString(32) + ":";
  return e.memoizedState = t;
}, unstable_isNewReconciler: !1 }, py = {
  readContext: dt,
  useCallback: um,
  useContext: dt,
  useEffect: Nu,
  useImperativeHandle: am,
  useInsertionEffect: im,
  useLayoutEffect: lm,
  useMemo: cm,
  useReducer: Ms,
  useRef: om,
  useState: function() {
    return Ms(wo);
  },
  useDebugValue: zu,
  useDeferredValue: function(e) {
    var t = pt();
    return fm(t, Se.memoizedState, e);
  },
  useTransition: function() {
    var e = Ms(wo)[0], t = pt().memoizedState;
    return [e, t];
  },
  useMutableSource: Zp,
  useSyncExternalStore: qp,
  useId: dm,
  unstable_isNewReconciler: !1
}, my = { readContext: dt, useCallback: um, useContext: dt, useEffect: Nu, useImperativeHandle: am, useInsertionEffect: im, useLayoutEffect: lm, useMemo: cm, useReducer: Ns, useRef: om, useState: function() {
  return Ns(wo);
}, useDebugValue: zu, useDeferredValue: function(e) {
  var t = pt();
  return Se === null ? t.memoizedState = e : fm(t, Se.memoizedState, e);
}, useTransition: function() {
  var e = Ns(wo)[0], t = pt().memoizedState;
  return [e, t];
}, useMutableSource: Zp, useSyncExternalStore: qp, useId: dm, unstable_isNewReconciler: !1 };
function St(e, t) {
  if (e && e.defaultProps) {
    t = se({}, t), e = e.defaultProps;
    for (var n in e)
      t[n] === void 0 && (t[n] = e[n]);
    return t;
  }
  return t;
}
function _a(e, t, n, r) {
  t = e.memoizedState, n = n(r, t), n = n == null ? t : se({}, t, n), e.memoizedState = n, e.lanes === 0 && (e.updateQueue.baseState = n);
}
var vl = { isMounted: function(e) {
  return (e = e._reactInternals) ? An(e) === e : !1;
}, enqueueSetState: function(e, t, n) {
  e = e._reactInternals;
  var r = Ae(), o = pn(e), i = Wt(r, o);
  i.payload = t, n != null && (i.callback = n), t = fn(e, i, o), t !== null && (_t(t, e, o, r), Si(t, e, o));
}, enqueueReplaceState: function(e, t, n) {
  e = e._reactInternals;
  var r = Ae(), o = pn(e), i = Wt(r, o);
  i.tag = 1, i.payload = t, n != null && (i.callback = n), t = fn(e, i, o), t !== null && (_t(t, e, o, r), Si(t, e, o));
}, enqueueForceUpdate: function(e, t) {
  e = e._reactInternals;
  var n = Ae(), r = pn(e), o = Wt(n, r);
  o.tag = 2, t != null && (o.callback = t), t = fn(e, o, r), t !== null && (_t(t, e, r, n), Si(t, e, r));
} };
function pf(e, t, n, r, o, i, l) {
  return e = e.stateNode, typeof e.shouldComponentUpdate == "function" ? e.shouldComponentUpdate(r, i, l) : t.prototype && t.prototype.isPureReactComponent ? !mo(n, r) || !mo(o, i) : !0;
}
function gm(e, t, n) {
  var r = !1, o = gn, i = t.contextType;
  return typeof i == "object" && i !== null ? i = dt(i) : (o = Ve(t) ? Mn : Le.current, r = t.contextTypes, i = (r = r != null) ? hr(e, o) : gn), t = new t(n, i), e.memoizedState = t.state !== null && t.state !== void 0 ? t.state : null, t.updater = vl, e.stateNode = t, t._reactInternals = e, r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = o, e.__reactInternalMemoizedMaskedChildContext = i), t;
}
function mf(e, t, n, r) {
  e = t.state, typeof t.componentWillReceiveProps == "function" && t.componentWillReceiveProps(n, r), typeof t.UNSAFE_componentWillReceiveProps == "function" && t.UNSAFE_componentWillReceiveProps(n, r), t.state !== e && vl.enqueueReplaceState(t, t.state, null);
}
function $a(e, t, n, r) {
  var o = e.stateNode;
  o.props = n, o.state = e.memoizedState, o.refs = {}, _u(e);
  var i = t.contextType;
  typeof i == "object" && i !== null ? o.context = dt(i) : (i = Ve(t) ? Mn : Le.current, o.context = hr(e, i)), o.state = e.memoizedState, i = t.getDerivedStateFromProps, typeof i == "function" && (_a(e, t, i, n), o.state = e.memoizedState), typeof t.getDerivedStateFromProps == "function" || typeof o.getSnapshotBeforeUpdate == "function" || typeof o.UNSAFE_componentWillMount != "function" && typeof o.componentWillMount != "function" || (t = o.state, typeof o.componentWillMount == "function" && o.componentWillMount(), typeof o.UNSAFE_componentWillMount == "function" && o.UNSAFE_componentWillMount(), t !== o.state && vl.enqueueReplaceState(o, o.state, null), Qi(e, n, o, r), o.state = e.memoizedState), typeof o.componentDidMount == "function" && (e.flags |= 4194308);
}
function xr(e, t) {
  try {
    var n = "", r = t;
    do
      n += W0(r), r = r.return;
    while (r);
    var o = n;
  } catch (i) {
    o = `
Error generating stack: ` + i.message + `
` + i.stack;
  }
  return { value: e, source: t, stack: o, digest: null };
}
function zs(e, t, n) {
  return { value: e, source: null, stack: n ?? null, digest: t ?? null };
}
function Pa(e, t) {
  try {
    console.error(t.value);
  } catch (n) {
    setTimeout(function() {
      throw n;
    });
  }
}
var hy = typeof WeakMap == "function" ? WeakMap : Map;
function ym(e, t, n) {
  n = Wt(-1, n), n.tag = 3, n.payload = { element: null };
  var r = t.value;
  return n.callback = function() {
    Ji || (Ji = !0, Aa = r), Pa(e, t);
  }, n;
}
function vm(e, t, n) {
  n = Wt(-1, n), n.tag = 3;
  var r = e.type.getDerivedStateFromError;
  if (typeof r == "function") {
    var o = t.value;
    n.payload = function() {
      return r(o);
    }, n.callback = function() {
      Pa(e, t);
    };
  }
  var i = e.stateNode;
  return i !== null && typeof i.componentDidCatch == "function" && (n.callback = function() {
    Pa(e, t), typeof r != "function" && (dn === null ? dn = /* @__PURE__ */ new Set([this]) : dn.add(this));
    var l = t.stack;
    this.componentDidCatch(t.value, { componentStack: l !== null ? l : "" });
  }), n;
}
function hf(e, t, n) {
  var r = e.pingCache;
  if (r === null) {
    r = e.pingCache = new hy();
    var o = /* @__PURE__ */ new Set();
    r.set(t, o);
  } else
    o = r.get(t), o === void 0 && (o = /* @__PURE__ */ new Set(), r.set(t, o));
  o.has(n) || (o.add(n), e = Ry.bind(null, e, t, n), t.then(e, e));
}
function gf(e) {
  do {
    var t;
    if ((t = e.tag === 13) && (t = e.memoizedState, t = t !== null ? t.dehydrated !== null : !0), t)
      return e;
    e = e.return;
  } while (e !== null);
  return null;
}
function yf(e, t, n, r, o) {
  return e.mode & 1 ? (e.flags |= 65536, e.lanes = o, e) : (e === t ? e.flags |= 65536 : (e.flags |= 128, n.flags |= 131072, n.flags &= -52805, n.tag === 1 && (n.alternate === null ? n.tag = 17 : (t = Wt(-1, 1), t.tag = 2, fn(n, t, 1))), n.lanes |= 1), e);
}
var gy = Qt.ReactCurrentOwner, We = !1;
function Ie(e, t, n, r) {
  t.child = e === null ? Gp(t, null, n, r) : yr(t, e.child, n, r);
}
function vf(e, t, n, r, o) {
  n = n.render;
  var i = t.ref;
  return ur(t, o), r = Ou(e, t, n, r, i, o), n = Mu(), e !== null && !We ? (t.updateQueue = e.updateQueue, t.flags &= -2053, e.lanes &= ~o, Kt(e, t, o)) : (re && n && vu(t), t.flags |= 1, Ie(e, t, r, o), t.child);
}
function xf(e, t, n, r, o) {
  if (e === null) {
    var i = n.type;
    return typeof i == "function" && !Bu(i) && i.defaultProps === void 0 && n.compare === null && n.defaultProps === void 0 ? (t.tag = 15, t.type = i, xm(e, t, i, r, o)) : (e = $i(n.type, null, r, t, t.mode, o), e.ref = t.ref, e.return = t, t.child = e);
  }
  if (i = e.child, !(e.lanes & o)) {
    var l = i.memoizedProps;
    if (n = n.compare, n = n !== null ? n : mo, n(l, r) && e.ref === t.ref)
      return Kt(e, t, o);
  }
  return t.flags |= 1, e = mn(i, r), e.ref = t.ref, e.return = t, t.child = e;
}
function xm(e, t, n, r, o) {
  if (e !== null) {
    var i = e.memoizedProps;
    if (mo(i, r) && e.ref === t.ref)
      if (We = !1, t.pendingProps = r = i, (e.lanes & o) !== 0)
        e.flags & 131072 && (We = !0);
      else
        return t.lanes = e.lanes, Kt(e, t, o);
  }
  return Ta(e, t, n, r, o);
}
function Sm(e, t, n) {
  var r = t.pendingProps, o = r.children, i = e !== null ? e.memoizedState : null;
  if (r.mode === "hidden")
    if (!(t.mode & 1))
      t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, Y(or, Ye), Ye |= n;
    else {
      if (!(n & 1073741824))
        return e = i !== null ? i.baseLanes | n : n, t.lanes = t.childLanes = 1073741824, t.memoizedState = { baseLanes: e, cachePool: null, transitions: null }, t.updateQueue = null, Y(or, Ye), Ye |= e, null;
      t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, r = i !== null ? i.baseLanes : n, Y(or, Ye), Ye |= r;
    }
  else
    i !== null ? (r = i.baseLanes | n, t.memoizedState = null) : r = n, Y(or, Ye), Ye |= r;
  return Ie(e, t, o, n), t.child;
}
function wm(e, t) {
  var n = t.ref;
  (e === null && n !== null || e !== null && e.ref !== n) && (t.flags |= 512, t.flags |= 2097152);
}
function Ta(e, t, n, r, o) {
  var i = Ve(n) ? Mn : Le.current;
  return i = hr(t, i), ur(t, o), n = Ou(e, t, n, r, i, o), r = Mu(), e !== null && !We ? (t.updateQueue = e.updateQueue, t.flags &= -2053, e.lanes &= ~o, Kt(e, t, o)) : (re && r && vu(t), t.flags |= 1, Ie(e, t, n, o), t.child);
}
function Sf(e, t, n, r, o) {
  if (Ve(n)) {
    var i = !0;
    Ui(t);
  } else
    i = !1;
  if (ur(t, o), t.stateNode === null)
    Ci(e, t), gm(t, n, r), $a(t, n, r, o), r = !0;
  else if (e === null) {
    var l = t.stateNode, s = t.memoizedProps;
    l.props = s;
    var a = l.context, u = n.contextType;
    typeof u == "object" && u !== null ? u = dt(u) : (u = Ve(n) ? Mn : Le.current, u = hr(t, u));
    var c = n.getDerivedStateFromProps, f = typeof c == "function" || typeof l.getSnapshotBeforeUpdate == "function";
    f || typeof l.UNSAFE_componentWillReceiveProps != "function" && typeof l.componentWillReceiveProps != "function" || (s !== r || a !== u) && mf(t, l, r, u), en = !1;
    var p = t.memoizedState;
    l.state = p, Qi(t, r, l, o), a = t.memoizedState, s !== r || p !== a || Ue.current || en ? (typeof c == "function" && (_a(t, n, c, r), a = t.memoizedState), (s = en || pf(t, n, s, r, p, a, u)) ? (f || typeof l.UNSAFE_componentWillMount != "function" && typeof l.componentWillMount != "function" || (typeof l.componentWillMount == "function" && l.componentWillMount(), typeof l.UNSAFE_componentWillMount == "function" && l.UNSAFE_componentWillMount()), typeof l.componentDidMount == "function" && (t.flags |= 4194308)) : (typeof l.componentDidMount == "function" && (t.flags |= 4194308), t.memoizedProps = r, t.memoizedState = a), l.props = r, l.state = a, l.context = u, r = s) : (typeof l.componentDidMount == "function" && (t.flags |= 4194308), r = !1);
  } else {
    l = t.stateNode, Yp(e, t), s = t.memoizedProps, u = t.type === t.elementType ? s : St(t.type, s), l.props = u, f = t.pendingProps, p = l.context, a = n.contextType, typeof a == "object" && a !== null ? a = dt(a) : (a = Ve(n) ? Mn : Le.current, a = hr(t, a));
    var v = n.getDerivedStateFromProps;
    (c = typeof v == "function" || typeof l.getSnapshotBeforeUpdate == "function") || typeof l.UNSAFE_componentWillReceiveProps != "function" && typeof l.componentWillReceiveProps != "function" || (s !== f || p !== a) && mf(t, l, r, a), en = !1, p = t.memoizedState, l.state = p, Qi(t, r, l, o);
    var y = t.memoizedState;
    s !== f || p !== y || Ue.current || en ? (typeof v == "function" && (_a(t, n, v, r), y = t.memoizedState), (u = en || pf(t, n, u, r, p, y, a) || !1) ? (c || typeof l.UNSAFE_componentWillUpdate != "function" && typeof l.componentWillUpdate != "function" || (typeof l.componentWillUpdate == "function" && l.componentWillUpdate(r, y, a), typeof l.UNSAFE_componentWillUpdate == "function" && l.UNSAFE_componentWillUpdate(r, y, a)), typeof l.componentDidUpdate == "function" && (t.flags |= 4), typeof l.getSnapshotBeforeUpdate == "function" && (t.flags |= 1024)) : (typeof l.componentDidUpdate != "function" || s === e.memoizedProps && p === e.memoizedState || (t.flags |= 4), typeof l.getSnapshotBeforeUpdate != "function" || s === e.memoizedProps && p === e.memoizedState || (t.flags |= 1024), t.memoizedProps = r, t.memoizedState = y), l.props = r, l.state = y, l.context = a, r = u) : (typeof l.componentDidUpdate != "function" || s === e.memoizedProps && p === e.memoizedState || (t.flags |= 4), typeof l.getSnapshotBeforeUpdate != "function" || s === e.memoizedProps && p === e.memoizedState || (t.flags |= 1024), r = !1);
  }
  return Ra(e, t, n, r, i, o);
}
function Ra(e, t, n, r, o, i) {
  wm(e, t);
  var l = (t.flags & 128) !== 0;
  if (!r && !l)
    return o && of(t, n, !1), Kt(e, t, i);
  r = t.stateNode, gy.current = t;
  var s = l && typeof n.getDerivedStateFromError != "function" ? null : r.render();
  return t.flags |= 1, e !== null && l ? (t.child = yr(t, e.child, null, i), t.child = yr(t, null, s, i)) : Ie(e, t, s, i), t.memoizedState = r.state, o && of(t, n, !0), t.child;
}
function km(e) {
  var t = e.stateNode;
  t.pendingContext ? rf(e, t.pendingContext, t.pendingContext !== t.context) : t.context && rf(e, t.context, !1), $u(e, t.containerInfo);
}
function wf(e, t, n, r, o) {
  return gr(), Su(o), t.flags |= 256, Ie(e, t, n, r), t.child;
}
var Oa = { dehydrated: null, treeContext: null, retryLane: 0 };
function Ma(e) {
  return { baseLanes: e, cachePool: null, transitions: null };
}
function Cm(e, t, n) {
  var r = t.pendingProps, o = ie.current, i = !1, l = (t.flags & 128) !== 0, s;
  if ((s = l) || (s = e !== null && e.memoizedState === null ? !1 : (o & 2) !== 0), s ? (i = !0, t.flags &= -129) : (e === null || e.memoizedState !== null) && (o |= 1), Y(ie, o & 1), e === null)
    return Ca(t), e = t.memoizedState, e !== null && (e = e.dehydrated, e !== null) ? (t.mode & 1 ? e.data === "$!" ? t.lanes = 8 : t.lanes = 1073741824 : t.lanes = 1, null) : (l = r.children, e = r.fallback, i ? (r = t.mode, i = t.child, l = { mode: "hidden", children: l }, !(r & 1) && i !== null ? (i.childLanes = 0, i.pendingProps = l) : i = wl(l, r, 0, null), e = Rn(e, r, n, null), i.return = t, e.return = t, i.sibling = e, t.child = i, t.child.memoizedState = Ma(n), t.memoizedState = Oa, e) : Lu(t, l));
  if (o = e.memoizedState, o !== null && (s = o.dehydrated, s !== null))
    return yy(e, t, l, r, s, o, n);
  if (i) {
    i = r.fallback, l = t.mode, o = e.child, s = o.sibling;
    var a = { mode: "hidden", children: r.children };
    return !(l & 1) && t.child !== o ? (r = t.child, r.childLanes = 0, r.pendingProps = a, t.deletions = null) : (r = mn(o, a), r.subtreeFlags = o.subtreeFlags & 14680064), s !== null ? i = mn(s, i) : (i = Rn(i, l, n, null), i.flags |= 2), i.return = t, r.return = t, r.sibling = i, t.child = r, r = i, i = t.child, l = e.child.memoizedState, l = l === null ? Ma(n) : { baseLanes: l.baseLanes | n, cachePool: null, transitions: l.transitions }, i.memoizedState = l, i.childLanes = e.childLanes & ~n, t.memoizedState = Oa, r;
  }
  return i = e.child, e = i.sibling, r = mn(i, { mode: "visible", children: r.children }), !(t.mode & 1) && (r.lanes = n), r.return = t, r.sibling = null, e !== null && (n = t.deletions, n === null ? (t.deletions = [e], t.flags |= 16) : n.push(e)), t.child = r, t.memoizedState = null, r;
}
function Lu(e, t) {
  return t = wl({ mode: "visible", children: t }, e.mode, 0, null), t.return = e, e.child = t;
}
function si(e, t, n, r) {
  return r !== null && Su(r), yr(t, e.child, null, n), e = Lu(t, t.pendingProps.children), e.flags |= 2, t.memoizedState = null, e;
}
function yy(e, t, n, r, o, i, l) {
  if (n)
    return t.flags & 256 ? (t.flags &= -257, r = zs(Error(P(422))), si(e, t, l, r)) : t.memoizedState !== null ? (t.child = e.child, t.flags |= 128, null) : (i = r.fallback, o = t.mode, r = wl({ mode: "visible", children: r.children }, o, 0, null), i = Rn(i, o, l, null), i.flags |= 2, r.return = t, i.return = t, r.sibling = i, t.child = r, t.mode & 1 && yr(t, e.child, null, l), t.child.memoizedState = Ma(l), t.memoizedState = Oa, i);
  if (!(t.mode & 1))
    return si(e, t, l, null);
  if (o.data === "$!") {
    if (r = o.nextSibling && o.nextSibling.dataset, r)
      var s = r.dgst;
    return r = s, i = Error(P(419)), r = zs(i, r, void 0), si(e, t, l, r);
  }
  if (s = (l & e.childLanes) !== 0, We || s) {
    if (r = Ce, r !== null) {
      switch (l & -l) {
        case 4:
          o = 2;
          break;
        case 16:
          o = 8;
          break;
        case 64:
        case 128:
        case 256:
        case 512:
        case 1024:
        case 2048:
        case 4096:
        case 8192:
        case 16384:
        case 32768:
        case 65536:
        case 131072:
        case 262144:
        case 524288:
        case 1048576:
        case 2097152:
        case 4194304:
        case 8388608:
        case 16777216:
        case 33554432:
        case 67108864:
          o = 32;
          break;
        case 536870912:
          o = 268435456;
          break;
        default:
          o = 0;
      }
      o = o & (r.suspendedLanes | l) ? 0 : o, o !== 0 && o !== i.retryLane && (i.retryLane = o, Ht(e, o), _t(r, e, o, -1));
    }
    return Fu(), r = zs(Error(P(421))), si(e, t, l, r);
  }
  return o.data === "$?" ? (t.flags |= 128, t.child = e.child, t = Oy.bind(null, e), o._reactRetry = t, null) : (e = i.treeContext, Ze = cn(o.nextSibling), qe = t, re = !0, kt = null, e !== null && (st[at++] = Ft, st[at++] = Bt, st[at++] = Nn, Ft = e.id, Bt = e.overflow, Nn = t), t = Lu(t, r.children), t.flags |= 4096, t);
}
function kf(e, t, n) {
  e.lanes |= t;
  var r = e.alternate;
  r !== null && (r.lanes |= t), Ea(e.return, t, n);
}
function Ls(e, t, n, r, o) {
  var i = e.memoizedState;
  i === null ? e.memoizedState = { isBackwards: t, rendering: null, renderingStartTime: 0, last: r, tail: n, tailMode: o } : (i.isBackwards = t, i.rendering = null, i.renderingStartTime = 0, i.last = r, i.tail = n, i.tailMode = o);
}
function Em(e, t, n) {
  var r = t.pendingProps, o = r.revealOrder, i = r.tail;
  if (Ie(e, t, r.children, n), r = ie.current, r & 2)
    r = r & 1 | 2, t.flags |= 128;
  else {
    if (e !== null && e.flags & 128)
      e:
        for (e = t.child; e !== null; ) {
          if (e.tag === 13)
            e.memoizedState !== null && kf(e, n, t);
          else if (e.tag === 19)
            kf(e, n, t);
          else if (e.child !== null) {
            e.child.return = e, e = e.child;
            continue;
          }
          if (e === t)
            break e;
          for (; e.sibling === null; ) {
            if (e.return === null || e.return === t)
              break e;
            e = e.return;
          }
          e.sibling.return = e.return, e = e.sibling;
        }
    r &= 1;
  }
  if (Y(ie, r), !(t.mode & 1))
    t.memoizedState = null;
  else
    switch (o) {
      case "forwards":
        for (n = t.child, o = null; n !== null; )
          e = n.alternate, e !== null && Yi(e) === null && (o = n), n = n.sibling;
        n = o, n === null ? (o = t.child, t.child = null) : (o = n.sibling, n.sibling = null), Ls(t, !1, o, n, i);
        break;
      case "backwards":
        for (n = null, o = t.child, t.child = null; o !== null; ) {
          if (e = o.alternate, e !== null && Yi(e) === null) {
            t.child = o;
            break;
          }
          e = o.sibling, o.sibling = n, n = o, o = e;
        }
        Ls(t, !0, n, null, i);
        break;
      case "together":
        Ls(t, !1, null, null, void 0);
        break;
      default:
        t.memoizedState = null;
    }
  return t.child;
}
function Ci(e, t) {
  !(t.mode & 1) && e !== null && (e.alternate = null, t.alternate = null, t.flags |= 2);
}
function Kt(e, t, n) {
  if (e !== null && (t.dependencies = e.dependencies), Ln |= t.lanes, !(n & t.childLanes))
    return null;
  if (e !== null && t.child !== e.child)
    throw Error(P(153));
  if (t.child !== null) {
    for (e = t.child, n = mn(e, e.pendingProps), t.child = n, n.return = t; e.sibling !== null; )
      e = e.sibling, n = n.sibling = mn(e, e.pendingProps), n.return = t;
    n.sibling = null;
  }
  return t.child;
}
function vy(e, t, n) {
  switch (t.tag) {
    case 3:
      km(t), gr();
      break;
    case 5:
      Xp(t);
      break;
    case 1:
      Ve(t.type) && Ui(t);
      break;
    case 4:
      $u(t, t.stateNode.containerInfo);
      break;
    case 10:
      var r = t.type._context, o = t.memoizedProps.value;
      Y(Ki, r._currentValue), r._currentValue = o;
      break;
    case 13:
      if (r = t.memoizedState, r !== null)
        return r.dehydrated !== null ? (Y(ie, ie.current & 1), t.flags |= 128, null) : n & t.child.childLanes ? Cm(e, t, n) : (Y(ie, ie.current & 1), e = Kt(e, t, n), e !== null ? e.sibling : null);
      Y(ie, ie.current & 1);
      break;
    case 19:
      if (r = (n & t.childLanes) !== 0, e.flags & 128) {
        if (r)
          return Em(e, t, n);
        t.flags |= 128;
      }
      if (o = t.memoizedState, o !== null && (o.rendering = null, o.tail = null, o.lastEffect = null), Y(ie, ie.current), r)
        break;
      return null;
    case 22:
    case 23:
      return t.lanes = 0, Sm(e, t, n);
  }
  return Kt(e, t, n);
}
var _m, Na, $m, Pm;
_m = function(e, t) {
  for (var n = t.child; n !== null; ) {
    if (n.tag === 5 || n.tag === 6)
      e.appendChild(n.stateNode);
    else if (n.tag !== 4 && n.child !== null) {
      n.child.return = n, n = n.child;
      continue;
    }
    if (n === t)
      break;
    for (; n.sibling === null; ) {
      if (n.return === null || n.return === t)
        return;
      n = n.return;
    }
    n.sibling.return = n.return, n = n.sibling;
  }
};
Na = function() {
};
$m = function(e, t, n, r) {
  var o = e.memoizedProps;
  if (o !== r) {
    e = t.stateNode, $n(Lt.current);
    var i = null;
    switch (n) {
      case "input":
        o = ea(e, o), r = ea(e, r), i = [];
        break;
      case "select":
        o = se({}, o, { value: void 0 }), r = se({}, r, { value: void 0 }), i = [];
        break;
      case "textarea":
        o = ra(e, o), r = ra(e, r), i = [];
        break;
      default:
        typeof o.onClick != "function" && typeof r.onClick == "function" && (e.onclick = Bi);
    }
    ia(n, r);
    var l;
    n = null;
    for (u in o)
      if (!r.hasOwnProperty(u) && o.hasOwnProperty(u) && o[u] != null)
        if (u === "style") {
          var s = o[u];
          for (l in s)
            s.hasOwnProperty(l) && (n || (n = {}), n[l] = "");
        } else
          u !== "dangerouslySetInnerHTML" && u !== "children" && u !== "suppressContentEditableWarning" && u !== "suppressHydrationWarning" && u !== "autoFocus" && (lo.hasOwnProperty(u) ? i || (i = []) : (i = i || []).push(u, null));
    for (u in r) {
      var a = r[u];
      if (s = o != null ? o[u] : void 0, r.hasOwnProperty(u) && a !== s && (a != null || s != null))
        if (u === "style")
          if (s) {
            for (l in s)
              !s.hasOwnProperty(l) || a && a.hasOwnProperty(l) || (n || (n = {}), n[l] = "");
            for (l in a)
              a.hasOwnProperty(l) && s[l] !== a[l] && (n || (n = {}), n[l] = a[l]);
          } else
            n || (i || (i = []), i.push(
              u,
              n
            )), n = a;
        else
          u === "dangerouslySetInnerHTML" ? (a = a ? a.__html : void 0, s = s ? s.__html : void 0, a != null && s !== a && (i = i || []).push(u, a)) : u === "children" ? typeof a != "string" && typeof a != "number" || (i = i || []).push(u, "" + a) : u !== "suppressContentEditableWarning" && u !== "suppressHydrationWarning" && (lo.hasOwnProperty(u) ? (a != null && u === "onScroll" && q("scroll", e), i || s === a || (i = [])) : (i = i || []).push(u, a));
    }
    n && (i = i || []).push("style", n);
    var u = i;
    (t.updateQueue = u) && (t.flags |= 4);
  }
};
Pm = function(e, t, n, r) {
  n !== r && (t.flags |= 4);
};
function Dr(e, t) {
  if (!re)
    switch (e.tailMode) {
      case "hidden":
        t = e.tail;
        for (var n = null; t !== null; )
          t.alternate !== null && (n = t), t = t.sibling;
        n === null ? e.tail = null : n.sibling = null;
        break;
      case "collapsed":
        n = e.tail;
        for (var r = null; n !== null; )
          n.alternate !== null && (r = n), n = n.sibling;
        r === null ? t || e.tail === null ? e.tail = null : e.tail.sibling = null : r.sibling = null;
    }
}
function Me(e) {
  var t = e.alternate !== null && e.alternate.child === e.child, n = 0, r = 0;
  if (t)
    for (var o = e.child; o !== null; )
      n |= o.lanes | o.childLanes, r |= o.subtreeFlags & 14680064, r |= o.flags & 14680064, o.return = e, o = o.sibling;
  else
    for (o = e.child; o !== null; )
      n |= o.lanes | o.childLanes, r |= o.subtreeFlags, r |= o.flags, o.return = e, o = o.sibling;
  return e.subtreeFlags |= r, e.childLanes = n, t;
}
function xy(e, t, n) {
  var r = t.pendingProps;
  switch (xu(t), t.tag) {
    case 2:
    case 16:
    case 15:
    case 0:
    case 11:
    case 7:
    case 8:
    case 12:
    case 9:
    case 14:
      return Me(t), null;
    case 1:
      return Ve(t.type) && Wi(), Me(t), null;
    case 3:
      return r = t.stateNode, vr(), ee(Ue), ee(Le), Tu(), r.pendingContext && (r.context = r.pendingContext, r.pendingContext = null), (e === null || e.child === null) && (ii(t) ? t.flags |= 4 : e === null || e.memoizedState.isDehydrated && !(t.flags & 256) || (t.flags |= 1024, kt !== null && (Fa(kt), kt = null))), Na(e, t), Me(t), null;
    case 5:
      Pu(t);
      var o = $n(xo.current);
      if (n = t.type, e !== null && t.stateNode != null)
        $m(e, t, n, r, o), e.ref !== t.ref && (t.flags |= 512, t.flags |= 2097152);
      else {
        if (!r) {
          if (t.stateNode === null)
            throw Error(P(166));
          return Me(t), null;
        }
        if (e = $n(Lt.current), ii(t)) {
          r = t.stateNode, n = t.type;
          var i = t.memoizedProps;
          switch (r[Nt] = t, r[yo] = i, e = (t.mode & 1) !== 0, n) {
            case "dialog":
              q("cancel", r), q("close", r);
              break;
            case "iframe":
            case "object":
            case "embed":
              q("load", r);
              break;
            case "video":
            case "audio":
              for (o = 0; o < Gr.length; o++)
                q(Gr[o], r);
              break;
            case "source":
              q("error", r);
              break;
            case "img":
            case "image":
            case "link":
              q(
                "error",
                r
              ), q("load", r);
              break;
            case "details":
              q("toggle", r);
              break;
            case "input":
              Oc(r, i), q("invalid", r);
              break;
            case "select":
              r._wrapperState = { wasMultiple: !!i.multiple }, q("invalid", r);
              break;
            case "textarea":
              Nc(r, i), q("invalid", r);
          }
          ia(n, i), o = null;
          for (var l in i)
            if (i.hasOwnProperty(l)) {
              var s = i[l];
              l === "children" ? typeof s == "string" ? r.textContent !== s && (i.suppressHydrationWarning !== !0 && oi(r.textContent, s, e), o = ["children", s]) : typeof s == "number" && r.textContent !== "" + s && (i.suppressHydrationWarning !== !0 && oi(
                r.textContent,
                s,
                e
              ), o = ["children", "" + s]) : lo.hasOwnProperty(l) && s != null && l === "onScroll" && q("scroll", r);
            }
          switch (n) {
            case "input":
              Xo(r), Mc(r, i, !0);
              break;
            case "textarea":
              Xo(r), zc(r);
              break;
            case "select":
            case "option":
              break;
            default:
              typeof i.onClick == "function" && (r.onclick = Bi);
          }
          r = o, t.updateQueue = r, r !== null && (t.flags |= 4);
        } else {
          l = o.nodeType === 9 ? o : o.ownerDocument, e === "http://www.w3.org/1999/xhtml" && (e = tp(n)), e === "http://www.w3.org/1999/xhtml" ? n === "script" ? (e = l.createElement("div"), e.innerHTML = "<script><\/script>", e = e.removeChild(e.firstChild)) : typeof r.is == "string" ? e = l.createElement(n, { is: r.is }) : (e = l.createElement(n), n === "select" && (l = e, r.multiple ? l.multiple = !0 : r.size && (l.size = r.size))) : e = l.createElementNS(e, n), e[Nt] = t, e[yo] = r, _m(e, t, !1, !1), t.stateNode = e;
          e: {
            switch (l = la(n, r), n) {
              case "dialog":
                q("cancel", e), q("close", e), o = r;
                break;
              case "iframe":
              case "object":
              case "embed":
                q("load", e), o = r;
                break;
              case "video":
              case "audio":
                for (o = 0; o < Gr.length; o++)
                  q(Gr[o], e);
                o = r;
                break;
              case "source":
                q("error", e), o = r;
                break;
              case "img":
              case "image":
              case "link":
                q(
                  "error",
                  e
                ), q("load", e), o = r;
                break;
              case "details":
                q("toggle", e), o = r;
                break;
              case "input":
                Oc(e, r), o = ea(e, r), q("invalid", e);
                break;
              case "option":
                o = r;
                break;
              case "select":
                e._wrapperState = { wasMultiple: !!r.multiple }, o = se({}, r, { value: void 0 }), q("invalid", e);
                break;
              case "textarea":
                Nc(e, r), o = ra(e, r), q("invalid", e);
                break;
              default:
                o = r;
            }
            ia(n, o), s = o;
            for (i in s)
              if (s.hasOwnProperty(i)) {
                var a = s[i];
                i === "style" ? op(e, a) : i === "dangerouslySetInnerHTML" ? (a = a ? a.__html : void 0, a != null && np(e, a)) : i === "children" ? typeof a == "string" ? (n !== "textarea" || a !== "") && so(e, a) : typeof a == "number" && so(e, "" + a) : i !== "suppressContentEditableWarning" && i !== "suppressHydrationWarning" && i !== "autoFocus" && (lo.hasOwnProperty(i) ? a != null && i === "onScroll" && q("scroll", e) : a != null && ou(e, i, a, l));
              }
            switch (n) {
              case "input":
                Xo(e), Mc(e, r, !1);
                break;
              case "textarea":
                Xo(e), zc(e);
                break;
              case "option":
                r.value != null && e.setAttribute("value", "" + hn(r.value));
                break;
              case "select":
                e.multiple = !!r.multiple, i = r.value, i != null ? ir(e, !!r.multiple, i, !1) : r.defaultValue != null && ir(
                  e,
                  !!r.multiple,
                  r.defaultValue,
                  !0
                );
                break;
              default:
                typeof o.onClick == "function" && (e.onclick = Bi);
            }
            switch (n) {
              case "button":
              case "input":
              case "select":
              case "textarea":
                r = !!r.autoFocus;
                break e;
              case "img":
                r = !0;
                break e;
              default:
                r = !1;
            }
          }
          r && (t.flags |= 4);
        }
        t.ref !== null && (t.flags |= 512, t.flags |= 2097152);
      }
      return Me(t), null;
    case 6:
      if (e && t.stateNode != null)
        Pm(e, t, e.memoizedProps, r);
      else {
        if (typeof r != "string" && t.stateNode === null)
          throw Error(P(166));
        if (n = $n(xo.current), $n(Lt.current), ii(t)) {
          if (r = t.stateNode, n = t.memoizedProps, r[Nt] = t, (i = r.nodeValue !== n) && (e = qe, e !== null))
            switch (e.tag) {
              case 3:
                oi(r.nodeValue, n, (e.mode & 1) !== 0);
                break;
              case 5:
                e.memoizedProps.suppressHydrationWarning !== !0 && oi(r.nodeValue, n, (e.mode & 1) !== 0);
            }
          i && (t.flags |= 4);
        } else
          r = (n.nodeType === 9 ? n : n.ownerDocument).createTextNode(r), r[Nt] = t, t.stateNode = r;
      }
      return Me(t), null;
    case 13:
      if (ee(ie), r = t.memoizedState, e === null || e.memoizedState !== null && e.memoizedState.dehydrated !== null) {
        if (re && Ze !== null && t.mode & 1 && !(t.flags & 128))
          Hp(), gr(), t.flags |= 98560, i = !1;
        else if (i = ii(t), r !== null && r.dehydrated !== null) {
          if (e === null) {
            if (!i)
              throw Error(P(318));
            if (i = t.memoizedState, i = i !== null ? i.dehydrated : null, !i)
              throw Error(P(317));
            i[Nt] = t;
          } else
            gr(), !(t.flags & 128) && (t.memoizedState = null), t.flags |= 4;
          Me(t), i = !1;
        } else
          kt !== null && (Fa(kt), kt = null), i = !0;
        if (!i)
          return t.flags & 65536 ? t : null;
      }
      return t.flags & 128 ? (t.lanes = n, t) : (r = r !== null, r !== (e !== null && e.memoizedState !== null) && r && (t.child.flags |= 8192, t.mode & 1 && (e === null || ie.current & 1 ? we === 0 && (we = 3) : Fu())), t.updateQueue !== null && (t.flags |= 4), Me(t), null);
    case 4:
      return vr(), Na(e, t), e === null && ho(t.stateNode.containerInfo), Me(t), null;
    case 10:
      return Cu(t.type._context), Me(t), null;
    case 17:
      return Ve(t.type) && Wi(), Me(t), null;
    case 19:
      if (ee(ie), i = t.memoizedState, i === null)
        return Me(t), null;
      if (r = (t.flags & 128) !== 0, l = i.rendering, l === null)
        if (r)
          Dr(i, !1);
        else {
          if (we !== 0 || e !== null && e.flags & 128)
            for (e = t.child; e !== null; ) {
              if (l = Yi(e), l !== null) {
                for (t.flags |= 128, Dr(i, !1), r = l.updateQueue, r !== null && (t.updateQueue = r, t.flags |= 4), t.subtreeFlags = 0, r = n, n = t.child; n !== null; )
                  i = n, e = r, i.flags &= 14680066, l = i.alternate, l === null ? (i.childLanes = 0, i.lanes = e, i.child = null, i.subtreeFlags = 0, i.memoizedProps = null, i.memoizedState = null, i.updateQueue = null, i.dependencies = null, i.stateNode = null) : (i.childLanes = l.childLanes, i.lanes = l.lanes, i.child = l.child, i.subtreeFlags = 0, i.deletions = null, i.memoizedProps = l.memoizedProps, i.memoizedState = l.memoizedState, i.updateQueue = l.updateQueue, i.type = l.type, e = l.dependencies, i.dependencies = e === null ? null : { lanes: e.lanes, firstContext: e.firstContext }), n = n.sibling;
                return Y(ie, ie.current & 1 | 2), t.child;
              }
              e = e.sibling;
            }
          i.tail !== null && de() > Sr && (t.flags |= 128, r = !0, Dr(i, !1), t.lanes = 4194304);
        }
      else {
        if (!r)
          if (e = Yi(l), e !== null) {
            if (t.flags |= 128, r = !0, n = e.updateQueue, n !== null && (t.updateQueue = n, t.flags |= 4), Dr(i, !0), i.tail === null && i.tailMode === "hidden" && !l.alternate && !re)
              return Me(t), null;
          } else
            2 * de() - i.renderingStartTime > Sr && n !== 1073741824 && (t.flags |= 128, r = !0, Dr(i, !1), t.lanes = 4194304);
        i.isBackwards ? (l.sibling = t.child, t.child = l) : (n = i.last, n !== null ? n.sibling = l : t.child = l, i.last = l);
      }
      return i.tail !== null ? (t = i.tail, i.rendering = t, i.tail = t.sibling, i.renderingStartTime = de(), t.sibling = null, n = ie.current, Y(ie, r ? n & 1 | 2 : n & 1), t) : (Me(t), null);
    case 22:
    case 23:
      return Du(), r = t.memoizedState !== null, e !== null && e.memoizedState !== null !== r && (t.flags |= 8192), r && t.mode & 1 ? Ye & 1073741824 && (Me(t), t.subtreeFlags & 6 && (t.flags |= 8192)) : Me(t), null;
    case 24:
      return null;
    case 25:
      return null;
  }
  throw Error(P(156, t.tag));
}
function Sy(e, t) {
  switch (xu(t), t.tag) {
    case 1:
      return Ve(t.type) && Wi(), e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, t) : null;
    case 3:
      return vr(), ee(Ue), ee(Le), Tu(), e = t.flags, e & 65536 && !(e & 128) ? (t.flags = e & -65537 | 128, t) : null;
    case 5:
      return Pu(t), null;
    case 13:
      if (ee(ie), e = t.memoizedState, e !== null && e.dehydrated !== null) {
        if (t.alternate === null)
          throw Error(P(340));
        gr();
      }
      return e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, t) : null;
    case 19:
      return ee(ie), null;
    case 4:
      return vr(), null;
    case 10:
      return Cu(t.type._context), null;
    case 22:
    case 23:
      return Du(), null;
    case 24:
      return null;
    default:
      return null;
  }
}
var ai = !1, ze = !1, wy = typeof WeakSet == "function" ? WeakSet : Set, M = null;
function rr(e, t) {
  var n = e.ref;
  if (n !== null)
    if (typeof n == "function")
      try {
        n(null);
      } catch (r) {
        fe(e, t, r);
      }
    else
      n.current = null;
}
function za(e, t, n) {
  try {
    n();
  } catch (r) {
    fe(e, t, r);
  }
}
var Cf = !1;
function ky(e, t) {
  if (ga = bi, e = Np(), yu(e)) {
    if ("selectionStart" in e)
      var n = { start: e.selectionStart, end: e.selectionEnd };
    else
      e: {
        n = (n = e.ownerDocument) && n.defaultView || window;
        var r = n.getSelection && n.getSelection();
        if (r && r.rangeCount !== 0) {
          n = r.anchorNode;
          var o = r.anchorOffset, i = r.focusNode;
          r = r.focusOffset;
          try {
            n.nodeType, i.nodeType;
          } catch {
            n = null;
            break e;
          }
          var l = 0, s = -1, a = -1, u = 0, c = 0, f = e, p = null;
          t:
            for (; ; ) {
              for (var v; f !== n || o !== 0 && f.nodeType !== 3 || (s = l + o), f !== i || r !== 0 && f.nodeType !== 3 || (a = l + r), f.nodeType === 3 && (l += f.nodeValue.length), (v = f.firstChild) !== null; )
                p = f, f = v;
              for (; ; ) {
                if (f === e)
                  break t;
                if (p === n && ++u === o && (s = l), p === i && ++c === r && (a = l), (v = f.nextSibling) !== null)
                  break;
                f = p, p = f.parentNode;
              }
              f = v;
            }
          n = s === -1 || a === -1 ? null : { start: s, end: a };
        } else
          n = null;
      }
    n = n || { start: 0, end: 0 };
  } else
    n = null;
  for (ya = { focusedElem: e, selectionRange: n }, bi = !1, M = t; M !== null; )
    if (t = M, e = t.child, (t.subtreeFlags & 1028) !== 0 && e !== null)
      e.return = t, M = e;
    else
      for (; M !== null; ) {
        t = M;
        try {
          var y = t.alternate;
          if (t.flags & 1024)
            switch (t.tag) {
              case 0:
              case 11:
              case 15:
                break;
              case 1:
                if (y !== null) {
                  var g = y.memoizedProps, _ = y.memoizedState, m = t.stateNode, d = m.getSnapshotBeforeUpdate(t.elementType === t.type ? g : St(t.type, g), _);
                  m.__reactInternalSnapshotBeforeUpdate = d;
                }
                break;
              case 3:
                var h = t.stateNode.containerInfo;
                h.nodeType === 1 ? h.textContent = "" : h.nodeType === 9 && h.documentElement && h.removeChild(h.documentElement);
                break;
              case 5:
              case 6:
              case 4:
              case 17:
                break;
              default:
                throw Error(P(163));
            }
        } catch (x) {
          fe(t, t.return, x);
        }
        if (e = t.sibling, e !== null) {
          e.return = t.return, M = e;
          break;
        }
        M = t.return;
      }
  return y = Cf, Cf = !1, y;
}
function no(e, t, n) {
  var r = t.updateQueue;
  if (r = r !== null ? r.lastEffect : null, r !== null) {
    var o = r = r.next;
    do {
      if ((o.tag & e) === e) {
        var i = o.destroy;
        o.destroy = void 0, i !== void 0 && za(t, n, i);
      }
      o = o.next;
    } while (o !== r);
  }
}
function xl(e, t) {
  if (t = t.updateQueue, t = t !== null ? t.lastEffect : null, t !== null) {
    var n = t = t.next;
    do {
      if ((n.tag & e) === e) {
        var r = n.create;
        n.destroy = r();
      }
      n = n.next;
    } while (n !== t);
  }
}
function La(e) {
  var t = e.ref;
  if (t !== null) {
    var n = e.stateNode;
    switch (e.tag) {
      case 5:
        e = n;
        break;
      default:
        e = n;
    }
    typeof t == "function" ? t(e) : t.current = e;
  }
}
function Tm(e) {
  var t = e.alternate;
  t !== null && (e.alternate = null, Tm(t)), e.child = null, e.deletions = null, e.sibling = null, e.tag === 5 && (t = e.stateNode, t !== null && (delete t[Nt], delete t[yo], delete t[Sa], delete t[oy], delete t[iy])), e.stateNode = null, e.return = null, e.dependencies = null, e.memoizedProps = null, e.memoizedState = null, e.pendingProps = null, e.stateNode = null, e.updateQueue = null;
}
function Rm(e) {
  return e.tag === 5 || e.tag === 3 || e.tag === 4;
}
function Ef(e) {
  e:
    for (; ; ) {
      for (; e.sibling === null; ) {
        if (e.return === null || Rm(e.return))
          return null;
        e = e.return;
      }
      for (e.sibling.return = e.return, e = e.sibling; e.tag !== 5 && e.tag !== 6 && e.tag !== 18; ) {
        if (e.flags & 2 || e.child === null || e.tag === 4)
          continue e;
        e.child.return = e, e = e.child;
      }
      if (!(e.flags & 2))
        return e.stateNode;
    }
}
function ja(e, t, n) {
  var r = e.tag;
  if (r === 5 || r === 6)
    e = e.stateNode, t ? n.nodeType === 8 ? n.parentNode.insertBefore(e, t) : n.insertBefore(e, t) : (n.nodeType === 8 ? (t = n.parentNode, t.insertBefore(e, n)) : (t = n, t.appendChild(e)), n = n._reactRootContainer, n != null || t.onclick !== null || (t.onclick = Bi));
  else if (r !== 4 && (e = e.child, e !== null))
    for (ja(e, t, n), e = e.sibling; e !== null; )
      ja(e, t, n), e = e.sibling;
}
function Ia(e, t, n) {
  var r = e.tag;
  if (r === 5 || r === 6)
    e = e.stateNode, t ? n.insertBefore(e, t) : n.appendChild(e);
  else if (r !== 4 && (e = e.child, e !== null))
    for (Ia(e, t, n), e = e.sibling; e !== null; )
      Ia(e, t, n), e = e.sibling;
}
var $e = null, wt = !1;
function Zt(e, t, n) {
  for (n = n.child; n !== null; )
    Om(e, t, n), n = n.sibling;
}
function Om(e, t, n) {
  if (zt && typeof zt.onCommitFiberUnmount == "function")
    try {
      zt.onCommitFiberUnmount(fl, n);
    } catch {
    }
  switch (n.tag) {
    case 5:
      ze || rr(n, t);
    case 6:
      var r = $e, o = wt;
      $e = null, Zt(e, t, n), $e = r, wt = o, $e !== null && (wt ? (e = $e, n = n.stateNode, e.nodeType === 8 ? e.parentNode.removeChild(n) : e.removeChild(n)) : $e.removeChild(n.stateNode));
      break;
    case 18:
      $e !== null && (wt ? (e = $e, n = n.stateNode, e.nodeType === 8 ? Ps(e.parentNode, n) : e.nodeType === 1 && Ps(e, n), fo(e)) : Ps($e, n.stateNode));
      break;
    case 4:
      r = $e, o = wt, $e = n.stateNode.containerInfo, wt = !0, Zt(e, t, n), $e = r, wt = o;
      break;
    case 0:
    case 11:
    case 14:
    case 15:
      if (!ze && (r = n.updateQueue, r !== null && (r = r.lastEffect, r !== null))) {
        o = r = r.next;
        do {
          var i = o, l = i.destroy;
          i = i.tag, l !== void 0 && (i & 2 || i & 4) && za(n, t, l), o = o.next;
        } while (o !== r);
      }
      Zt(e, t, n);
      break;
    case 1:
      if (!ze && (rr(n, t), r = n.stateNode, typeof r.componentWillUnmount == "function"))
        try {
          r.props = n.memoizedProps, r.state = n.memoizedState, r.componentWillUnmount();
        } catch (s) {
          fe(n, t, s);
        }
      Zt(e, t, n);
      break;
    case 21:
      Zt(e, t, n);
      break;
    case 22:
      n.mode & 1 ? (ze = (r = ze) || n.memoizedState !== null, Zt(e, t, n), ze = r) : Zt(e, t, n);
      break;
    default:
      Zt(e, t, n);
  }
}
function _f(e) {
  var t = e.updateQueue;
  if (t !== null) {
    e.updateQueue = null;
    var n = e.stateNode;
    n === null && (n = e.stateNode = new wy()), t.forEach(function(r) {
      var o = My.bind(null, e, r);
      n.has(r) || (n.add(r), r.then(o, o));
    });
  }
}
function xt(e, t) {
  var n = t.deletions;
  if (n !== null)
    for (var r = 0; r < n.length; r++) {
      var o = n[r];
      try {
        var i = e, l = t, s = l;
        e:
          for (; s !== null; ) {
            switch (s.tag) {
              case 5:
                $e = s.stateNode, wt = !1;
                break e;
              case 3:
                $e = s.stateNode.containerInfo, wt = !0;
                break e;
              case 4:
                $e = s.stateNode.containerInfo, wt = !0;
                break e;
            }
            s = s.return;
          }
        if ($e === null)
          throw Error(P(160));
        Om(i, l, o), $e = null, wt = !1;
        var a = o.alternate;
        a !== null && (a.return = null), o.return = null;
      } catch (u) {
        fe(o, t, u);
      }
    }
  if (t.subtreeFlags & 12854)
    for (t = t.child; t !== null; )
      Mm(t, e), t = t.sibling;
}
function Mm(e, t) {
  var n = e.alternate, r = e.flags;
  switch (e.tag) {
    case 0:
    case 11:
    case 14:
    case 15:
      if (xt(t, e), Tt(e), r & 4) {
        try {
          no(3, e, e.return), xl(3, e);
        } catch (g) {
          fe(e, e.return, g);
        }
        try {
          no(5, e, e.return);
        } catch (g) {
          fe(e, e.return, g);
        }
      }
      break;
    case 1:
      xt(t, e), Tt(e), r & 512 && n !== null && rr(n, n.return);
      break;
    case 5:
      if (xt(t, e), Tt(e), r & 512 && n !== null && rr(n, n.return), e.flags & 32) {
        var o = e.stateNode;
        try {
          so(o, "");
        } catch (g) {
          fe(e, e.return, g);
        }
      }
      if (r & 4 && (o = e.stateNode, o != null)) {
        var i = e.memoizedProps, l = n !== null ? n.memoizedProps : i, s = e.type, a = e.updateQueue;
        if (e.updateQueue = null, a !== null)
          try {
            s === "input" && i.type === "radio" && i.name != null && Jd(o, i), la(s, l);
            var u = la(s, i);
            for (l = 0; l < a.length; l += 2) {
              var c = a[l], f = a[l + 1];
              c === "style" ? op(o, f) : c === "dangerouslySetInnerHTML" ? np(o, f) : c === "children" ? so(o, f) : ou(o, c, f, u);
            }
            switch (s) {
              case "input":
                ta(o, i);
                break;
              case "textarea":
                ep(o, i);
                break;
              case "select":
                var p = o._wrapperState.wasMultiple;
                o._wrapperState.wasMultiple = !!i.multiple;
                var v = i.value;
                v != null ? ir(o, !!i.multiple, v, !1) : p !== !!i.multiple && (i.defaultValue != null ? ir(
                  o,
                  !!i.multiple,
                  i.defaultValue,
                  !0
                ) : ir(o, !!i.multiple, i.multiple ? [] : "", !1));
            }
            o[yo] = i;
          } catch (g) {
            fe(e, e.return, g);
          }
      }
      break;
    case 6:
      if (xt(t, e), Tt(e), r & 4) {
        if (e.stateNode === null)
          throw Error(P(162));
        o = e.stateNode, i = e.memoizedProps;
        try {
          o.nodeValue = i;
        } catch (g) {
          fe(e, e.return, g);
        }
      }
      break;
    case 3:
      if (xt(t, e), Tt(e), r & 4 && n !== null && n.memoizedState.isDehydrated)
        try {
          fo(t.containerInfo);
        } catch (g) {
          fe(e, e.return, g);
        }
      break;
    case 4:
      xt(t, e), Tt(e);
      break;
    case 13:
      xt(t, e), Tt(e), o = e.child, o.flags & 8192 && (i = o.memoizedState !== null, o.stateNode.isHidden = i, !i || o.alternate !== null && o.alternate.memoizedState !== null || (Au = de())), r & 4 && _f(e);
      break;
    case 22:
      if (c = n !== null && n.memoizedState !== null, e.mode & 1 ? (ze = (u = ze) || c, xt(t, e), ze = u) : xt(t, e), Tt(e), r & 8192) {
        if (u = e.memoizedState !== null, (e.stateNode.isHidden = u) && !c && e.mode & 1)
          for (M = e, c = e.child; c !== null; ) {
            for (f = M = c; M !== null; ) {
              switch (p = M, v = p.child, p.tag) {
                case 0:
                case 11:
                case 14:
                case 15:
                  no(4, p, p.return);
                  break;
                case 1:
                  rr(p, p.return);
                  var y = p.stateNode;
                  if (typeof y.componentWillUnmount == "function") {
                    r = p, n = p.return;
                    try {
                      t = r, y.props = t.memoizedProps, y.state = t.memoizedState, y.componentWillUnmount();
                    } catch (g) {
                      fe(r, n, g);
                    }
                  }
                  break;
                case 5:
                  rr(p, p.return);
                  break;
                case 22:
                  if (p.memoizedState !== null) {
                    Pf(f);
                    continue;
                  }
              }
              v !== null ? (v.return = p, M = v) : Pf(f);
            }
            c = c.sibling;
          }
        e:
          for (c = null, f = e; ; ) {
            if (f.tag === 5) {
              if (c === null) {
                c = f;
                try {
                  o = f.stateNode, u ? (i = o.style, typeof i.setProperty == "function" ? i.setProperty("display", "none", "important") : i.display = "none") : (s = f.stateNode, a = f.memoizedProps.style, l = a != null && a.hasOwnProperty("display") ? a.display : null, s.style.display = rp("display", l));
                } catch (g) {
                  fe(e, e.return, g);
                }
              }
            } else if (f.tag === 6) {
              if (c === null)
                try {
                  f.stateNode.nodeValue = u ? "" : f.memoizedProps;
                } catch (g) {
                  fe(e, e.return, g);
                }
            } else if ((f.tag !== 22 && f.tag !== 23 || f.memoizedState === null || f === e) && f.child !== null) {
              f.child.return = f, f = f.child;
              continue;
            }
            if (f === e)
              break e;
            for (; f.sibling === null; ) {
              if (f.return === null || f.return === e)
                break e;
              c === f && (c = null), f = f.return;
            }
            c === f && (c = null), f.sibling.return = f.return, f = f.sibling;
          }
      }
      break;
    case 19:
      xt(t, e), Tt(e), r & 4 && _f(e);
      break;
    case 21:
      break;
    default:
      xt(
        t,
        e
      ), Tt(e);
  }
}
function Tt(e) {
  var t = e.flags;
  if (t & 2) {
    try {
      e: {
        for (var n = e.return; n !== null; ) {
          if (Rm(n)) {
            var r = n;
            break e;
          }
          n = n.return;
        }
        throw Error(P(160));
      }
      switch (r.tag) {
        case 5:
          var o = r.stateNode;
          r.flags & 32 && (so(o, ""), r.flags &= -33);
          var i = Ef(e);
          Ia(e, i, o);
          break;
        case 3:
        case 4:
          var l = r.stateNode.containerInfo, s = Ef(e);
          ja(e, s, l);
          break;
        default:
          throw Error(P(161));
      }
    } catch (a) {
      fe(e, e.return, a);
    }
    e.flags &= -3;
  }
  t & 4096 && (e.flags &= -4097);
}
function Cy(e, t, n) {
  M = e, Nm(e);
}
function Nm(e, t, n) {
  for (var r = (e.mode & 1) !== 0; M !== null; ) {
    var o = M, i = o.child;
    if (o.tag === 22 && r) {
      var l = o.memoizedState !== null || ai;
      if (!l) {
        var s = o.alternate, a = s !== null && s.memoizedState !== null || ze;
        s = ai;
        var u = ze;
        if (ai = l, (ze = a) && !u)
          for (M = o; M !== null; )
            l = M, a = l.child, l.tag === 22 && l.memoizedState !== null ? Tf(o) : a !== null ? (a.return = l, M = a) : Tf(o);
        for (; i !== null; )
          M = i, Nm(i), i = i.sibling;
        M = o, ai = s, ze = u;
      }
      $f(e);
    } else
      o.subtreeFlags & 8772 && i !== null ? (i.return = o, M = i) : $f(e);
  }
}
function $f(e) {
  for (; M !== null; ) {
    var t = M;
    if (t.flags & 8772) {
      var n = t.alternate;
      try {
        if (t.flags & 8772)
          switch (t.tag) {
            case 0:
            case 11:
            case 15:
              ze || xl(5, t);
              break;
            case 1:
              var r = t.stateNode;
              if (t.flags & 4 && !ze)
                if (n === null)
                  r.componentDidMount();
                else {
                  var o = t.elementType === t.type ? n.memoizedProps : St(t.type, n.memoizedProps);
                  r.componentDidUpdate(o, n.memoizedState, r.__reactInternalSnapshotBeforeUpdate);
                }
              var i = t.updateQueue;
              i !== null && cf(t, i, r);
              break;
            case 3:
              var l = t.updateQueue;
              if (l !== null) {
                if (n = null, t.child !== null)
                  switch (t.child.tag) {
                    case 5:
                      n = t.child.stateNode;
                      break;
                    case 1:
                      n = t.child.stateNode;
                  }
                cf(t, l, n);
              }
              break;
            case 5:
              var s = t.stateNode;
              if (n === null && t.flags & 4) {
                n = s;
                var a = t.memoizedProps;
                switch (t.type) {
                  case "button":
                  case "input":
                  case "select":
                  case "textarea":
                    a.autoFocus && n.focus();
                    break;
                  case "img":
                    a.src && (n.src = a.src);
                }
              }
              break;
            case 6:
              break;
            case 4:
              break;
            case 12:
              break;
            case 13:
              if (t.memoizedState === null) {
                var u = t.alternate;
                if (u !== null) {
                  var c = u.memoizedState;
                  if (c !== null) {
                    var f = c.dehydrated;
                    f !== null && fo(f);
                  }
                }
              }
              break;
            case 19:
            case 17:
            case 21:
            case 22:
            case 23:
            case 25:
              break;
            default:
              throw Error(P(163));
          }
        ze || t.flags & 512 && La(t);
      } catch (p) {
        fe(t, t.return, p);
      }
    }
    if (t === e) {
      M = null;
      break;
    }
    if (n = t.sibling, n !== null) {
      n.return = t.return, M = n;
      break;
    }
    M = t.return;
  }
}
function Pf(e) {
  for (; M !== null; ) {
    var t = M;
    if (t === e) {
      M = null;
      break;
    }
    var n = t.sibling;
    if (n !== null) {
      n.return = t.return, M = n;
      break;
    }
    M = t.return;
  }
}
function Tf(e) {
  for (; M !== null; ) {
    var t = M;
    try {
      switch (t.tag) {
        case 0:
        case 11:
        case 15:
          var n = t.return;
          try {
            xl(4, t);
          } catch (a) {
            fe(t, n, a);
          }
          break;
        case 1:
          var r = t.stateNode;
          if (typeof r.componentDidMount == "function") {
            var o = t.return;
            try {
              r.componentDidMount();
            } catch (a) {
              fe(t, o, a);
            }
          }
          var i = t.return;
          try {
            La(t);
          } catch (a) {
            fe(t, i, a);
          }
          break;
        case 5:
          var l = t.return;
          try {
            La(t);
          } catch (a) {
            fe(t, l, a);
          }
      }
    } catch (a) {
      fe(t, t.return, a);
    }
    if (t === e) {
      M = null;
      break;
    }
    var s = t.sibling;
    if (s !== null) {
      s.return = t.return, M = s;
      break;
    }
    M = t.return;
  }
}
var Ey = Math.ceil, qi = Qt.ReactCurrentDispatcher, ju = Qt.ReactCurrentOwner, ft = Qt.ReactCurrentBatchConfig, B = 0, Ce = null, ye = null, Te = 0, Ye = 0, or = vn(0), we = 0, Co = null, Ln = 0, Sl = 0, Iu = 0, ro = null, Be = null, Au = 0, Sr = 1 / 0, At = null, Ji = !1, Aa = null, dn = null, ui = !1, on = null, el = 0, oo = 0, ba = null, Ei = -1, _i = 0;
function Ae() {
  return B & 6 ? de() : Ei !== -1 ? Ei : Ei = de();
}
function pn(e) {
  return e.mode & 1 ? B & 2 && Te !== 0 ? Te & -Te : sy.transition !== null ? (_i === 0 && (_i = gp()), _i) : (e = K, e !== 0 || (e = window.event, e = e === void 0 ? 16 : Cp(e.type)), e) : 1;
}
function _t(e, t, n, r) {
  if (50 < oo)
    throw oo = 0, ba = null, Error(P(185));
  zo(e, n, r), (!(B & 2) || e !== Ce) && (e === Ce && (!(B & 2) && (Sl |= n), we === 4 && nn(e, Te)), He(e, r), n === 1 && B === 0 && !(t.mode & 1) && (Sr = de() + 500, gl && xn()));
}
function He(e, t) {
  var n = e.callbackNode;
  sg(e, t);
  var r = Ai(e, e === Ce ? Te : 0);
  if (r === 0)
    n !== null && Ic(n), e.callbackNode = null, e.callbackPriority = 0;
  else if (t = r & -r, e.callbackPriority !== t) {
    if (n != null && Ic(n), t === 1)
      e.tag === 0 ? ly(Rf.bind(null, e)) : Wp(Rf.bind(null, e)), ny(function() {
        !(B & 6) && xn();
      }), n = null;
    else {
      switch (yp(r)) {
        case 1:
          n = uu;
          break;
        case 4:
          n = mp;
          break;
        case 16:
          n = Ii;
          break;
        case 536870912:
          n = hp;
          break;
        default:
          n = Ii;
      }
      n = Fm(n, zm.bind(null, e));
    }
    e.callbackPriority = t, e.callbackNode = n;
  }
}
function zm(e, t) {
  if (Ei = -1, _i = 0, B & 6)
    throw Error(P(327));
  var n = e.callbackNode;
  if (cr() && e.callbackNode !== n)
    return null;
  var r = Ai(e, e === Ce ? Te : 0);
  if (r === 0)
    return null;
  if (r & 30 || r & e.expiredLanes || t)
    t = tl(e, r);
  else {
    t = r;
    var o = B;
    B |= 2;
    var i = jm();
    (Ce !== e || Te !== t) && (At = null, Sr = de() + 500, Tn(e, t));
    do
      try {
        Py();
        break;
      } catch (s) {
        Lm(e, s);
      }
    while (1);
    ku(), qi.current = i, B = o, ye !== null ? t = 0 : (Ce = null, Te = 0, t = we);
  }
  if (t !== 0) {
    if (t === 2 && (o = fa(e), o !== 0 && (r = o, t = Da(e, o))), t === 1)
      throw n = Co, Tn(e, 0), nn(e, r), He(e, de()), n;
    if (t === 6)
      nn(e, r);
    else {
      if (o = e.current.alternate, !(r & 30) && !_y(o) && (t = tl(e, r), t === 2 && (i = fa(e), i !== 0 && (r = i, t = Da(e, i))), t === 1))
        throw n = Co, Tn(e, 0), nn(e, r), He(e, de()), n;
      switch (e.finishedWork = o, e.finishedLanes = r, t) {
        case 0:
        case 1:
          throw Error(P(345));
        case 2:
          wn(e, Be, At);
          break;
        case 3:
          if (nn(e, r), (r & 130023424) === r && (t = Au + 500 - de(), 10 < t)) {
            if (Ai(e, 0) !== 0)
              break;
            if (o = e.suspendedLanes, (o & r) !== r) {
              Ae(), e.pingedLanes |= e.suspendedLanes & o;
              break;
            }
            e.timeoutHandle = xa(wn.bind(null, e, Be, At), t);
            break;
          }
          wn(e, Be, At);
          break;
        case 4:
          if (nn(e, r), (r & 4194240) === r)
            break;
          for (t = e.eventTimes, o = -1; 0 < r; ) {
            var l = 31 - Et(r);
            i = 1 << l, l = t[l], l > o && (o = l), r &= ~i;
          }
          if (r = o, r = de() - r, r = (120 > r ? 120 : 480 > r ? 480 : 1080 > r ? 1080 : 1920 > r ? 1920 : 3e3 > r ? 3e3 : 4320 > r ? 4320 : 1960 * Ey(r / 1960)) - r, 10 < r) {
            e.timeoutHandle = xa(wn.bind(null, e, Be, At), r);
            break;
          }
          wn(e, Be, At);
          break;
        case 5:
          wn(e, Be, At);
          break;
        default:
          throw Error(P(329));
      }
    }
  }
  return He(e, de()), e.callbackNode === n ? zm.bind(null, e) : null;
}
function Da(e, t) {
  var n = ro;
  return e.current.memoizedState.isDehydrated && (Tn(e, t).flags |= 256), e = tl(e, t), e !== 2 && (t = Be, Be = n, t !== null && Fa(t)), e;
}
function Fa(e) {
  Be === null ? Be = e : Be.push.apply(Be, e);
}
function _y(e) {
  for (var t = e; ; ) {
    if (t.flags & 16384) {
      var n = t.updateQueue;
      if (n !== null && (n = n.stores, n !== null))
        for (var r = 0; r < n.length; r++) {
          var o = n[r], i = o.getSnapshot;
          o = o.value;
          try {
            if (!$t(i(), o))
              return !1;
          } catch {
            return !1;
          }
        }
    }
    if (n = t.child, t.subtreeFlags & 16384 && n !== null)
      n.return = t, t = n;
    else {
      if (t === e)
        break;
      for (; t.sibling === null; ) {
        if (t.return === null || t.return === e)
          return !0;
        t = t.return;
      }
      t.sibling.return = t.return, t = t.sibling;
    }
  }
  return !0;
}
function nn(e, t) {
  for (t &= ~Iu, t &= ~Sl, e.suspendedLanes |= t, e.pingedLanes &= ~t, e = e.expirationTimes; 0 < t; ) {
    var n = 31 - Et(t), r = 1 << n;
    e[n] = -1, t &= ~r;
  }
}
function Rf(e) {
  if (B & 6)
    throw Error(P(327));
  cr();
  var t = Ai(e, 0);
  if (!(t & 1))
    return He(e, de()), null;
  var n = tl(e, t);
  if (e.tag !== 0 && n === 2) {
    var r = fa(e);
    r !== 0 && (t = r, n = Da(e, r));
  }
  if (n === 1)
    throw n = Co, Tn(e, 0), nn(e, t), He(e, de()), n;
  if (n === 6)
    throw Error(P(345));
  return e.finishedWork = e.current.alternate, e.finishedLanes = t, wn(e, Be, At), He(e, de()), null;
}
function bu(e, t) {
  var n = B;
  B |= 1;
  try {
    return e(t);
  } finally {
    B = n, B === 0 && (Sr = de() + 500, gl && xn());
  }
}
function jn(e) {
  on !== null && on.tag === 0 && !(B & 6) && cr();
  var t = B;
  B |= 1;
  var n = ft.transition, r = K;
  try {
    if (ft.transition = null, K = 1, e)
      return e();
  } finally {
    K = r, ft.transition = n, B = t, !(B & 6) && xn();
  }
}
function Du() {
  Ye = or.current, ee(or);
}
function Tn(e, t) {
  e.finishedWork = null, e.finishedLanes = 0;
  var n = e.timeoutHandle;
  if (n !== -1 && (e.timeoutHandle = -1, ty(n)), ye !== null)
    for (n = ye.return; n !== null; ) {
      var r = n;
      switch (xu(r), r.tag) {
        case 1:
          r = r.type.childContextTypes, r != null && Wi();
          break;
        case 3:
          vr(), ee(Ue), ee(Le), Tu();
          break;
        case 5:
          Pu(r);
          break;
        case 4:
          vr();
          break;
        case 13:
          ee(ie);
          break;
        case 19:
          ee(ie);
          break;
        case 10:
          Cu(r.type._context);
          break;
        case 22:
        case 23:
          Du();
      }
      n = n.return;
    }
  if (Ce = e, ye = e = mn(e.current, null), Te = Ye = t, we = 0, Co = null, Iu = Sl = Ln = 0, Be = ro = null, _n !== null) {
    for (t = 0; t < _n.length; t++)
      if (n = _n[t], r = n.interleaved, r !== null) {
        n.interleaved = null;
        var o = r.next, i = n.pending;
        if (i !== null) {
          var l = i.next;
          i.next = o, r.next = l;
        }
        n.pending = r;
      }
    _n = null;
  }
  return e;
}
function Lm(e, t) {
  do {
    var n = ye;
    try {
      if (ku(), wi.current = Zi, Xi) {
        for (var r = le.memoizedState; r !== null; ) {
          var o = r.queue;
          o !== null && (o.pending = null), r = r.next;
        }
        Xi = !1;
      }
      if (zn = 0, ke = Se = le = null, to = !1, So = 0, ju.current = null, n === null || n.return === null) {
        we = 1, Co = t, ye = null;
        break;
      }
      e: {
        var i = e, l = n.return, s = n, a = t;
        if (t = Te, s.flags |= 32768, a !== null && typeof a == "object" && typeof a.then == "function") {
          var u = a, c = s, f = c.tag;
          if (!(c.mode & 1) && (f === 0 || f === 11 || f === 15)) {
            var p = c.alternate;
            p ? (c.updateQueue = p.updateQueue, c.memoizedState = p.memoizedState, c.lanes = p.lanes) : (c.updateQueue = null, c.memoizedState = null);
          }
          var v = gf(l);
          if (v !== null) {
            v.flags &= -257, yf(v, l, s, i, t), v.mode & 1 && hf(i, u, t), t = v, a = u;
            var y = t.updateQueue;
            if (y === null) {
              var g = /* @__PURE__ */ new Set();
              g.add(a), t.updateQueue = g;
            } else
              y.add(a);
            break e;
          } else {
            if (!(t & 1)) {
              hf(i, u, t), Fu();
              break e;
            }
            a = Error(P(426));
          }
        } else if (re && s.mode & 1) {
          var _ = gf(l);
          if (_ !== null) {
            !(_.flags & 65536) && (_.flags |= 256), yf(_, l, s, i, t), Su(xr(a, s));
            break e;
          }
        }
        i = a = xr(a, s), we !== 4 && (we = 2), ro === null ? ro = [i] : ro.push(i), i = l;
        do {
          switch (i.tag) {
            case 3:
              i.flags |= 65536, t &= -t, i.lanes |= t;
              var m = ym(i, a, t);
              uf(i, m);
              break e;
            case 1:
              s = a;
              var d = i.type, h = i.stateNode;
              if (!(i.flags & 128) && (typeof d.getDerivedStateFromError == "function" || h !== null && typeof h.componentDidCatch == "function" && (dn === null || !dn.has(h)))) {
                i.flags |= 65536, t &= -t, i.lanes |= t;
                var x = vm(i, s, t);
                uf(i, x);
                break e;
              }
          }
          i = i.return;
        } while (i !== null);
      }
      Am(n);
    } catch (E) {
      t = E, ye === n && n !== null && (ye = n = n.return);
      continue;
    }
    break;
  } while (1);
}
function jm() {
  var e = qi.current;
  return qi.current = Zi, e === null ? Zi : e;
}
function Fu() {
  (we === 0 || we === 3 || we === 2) && (we = 4), Ce === null || !(Ln & 268435455) && !(Sl & 268435455) || nn(Ce, Te);
}
function tl(e, t) {
  var n = B;
  B |= 2;
  var r = jm();
  (Ce !== e || Te !== t) && (At = null, Tn(e, t));
  do
    try {
      $y();
      break;
    } catch (o) {
      Lm(e, o);
    }
  while (1);
  if (ku(), B = n, qi.current = r, ye !== null)
    throw Error(P(261));
  return Ce = null, Te = 0, we;
}
function $y() {
  for (; ye !== null; )
    Im(ye);
}
function Py() {
  for (; ye !== null && !q0(); )
    Im(ye);
}
function Im(e) {
  var t = Dm(e.alternate, e, Ye);
  e.memoizedProps = e.pendingProps, t === null ? Am(e) : ye = t, ju.current = null;
}
function Am(e) {
  var t = e;
  do {
    var n = t.alternate;
    if (e = t.return, t.flags & 32768) {
      if (n = Sy(n, t), n !== null) {
        n.flags &= 32767, ye = n;
        return;
      }
      if (e !== null)
        e.flags |= 32768, e.subtreeFlags = 0, e.deletions = null;
      else {
        we = 6, ye = null;
        return;
      }
    } else if (n = xy(n, t, Ye), n !== null) {
      ye = n;
      return;
    }
    if (t = t.sibling, t !== null) {
      ye = t;
      return;
    }
    ye = t = e;
  } while (t !== null);
  we === 0 && (we = 5);
}
function wn(e, t, n) {
  var r = K, o = ft.transition;
  try {
    ft.transition = null, K = 1, Ty(e, t, n, r);
  } finally {
    ft.transition = o, K = r;
  }
  return null;
}
function Ty(e, t, n, r) {
  do
    cr();
  while (on !== null);
  if (B & 6)
    throw Error(P(327));
  n = e.finishedWork;
  var o = e.finishedLanes;
  if (n === null)
    return null;
  if (e.finishedWork = null, e.finishedLanes = 0, n === e.current)
    throw Error(P(177));
  e.callbackNode = null, e.callbackPriority = 0;
  var i = n.lanes | n.childLanes;
  if (ag(e, i), e === Ce && (ye = Ce = null, Te = 0), !(n.subtreeFlags & 2064) && !(n.flags & 2064) || ui || (ui = !0, Fm(Ii, function() {
    return cr(), null;
  })), i = (n.flags & 15990) !== 0, n.subtreeFlags & 15990 || i) {
    i = ft.transition, ft.transition = null;
    var l = K;
    K = 1;
    var s = B;
    B |= 4, ju.current = null, ky(e, n), Mm(n, e), Qg(ya), bi = !!ga, ya = ga = null, e.current = n, Cy(n), J0(), B = s, K = l, ft.transition = i;
  } else
    e.current = n;
  if (ui && (ui = !1, on = e, el = o), i = e.pendingLanes, i === 0 && (dn = null), ng(n.stateNode), He(e, de()), t !== null)
    for (r = e.onRecoverableError, n = 0; n < t.length; n++)
      o = t[n], r(o.value, { componentStack: o.stack, digest: o.digest });
  if (Ji)
    throw Ji = !1, e = Aa, Aa = null, e;
  return el & 1 && e.tag !== 0 && cr(), i = e.pendingLanes, i & 1 ? e === ba ? oo++ : (oo = 0, ba = e) : oo = 0, xn(), null;
}
function cr() {
  if (on !== null) {
    var e = yp(el), t = ft.transition, n = K;
    try {
      if (ft.transition = null, K = 16 > e ? 16 : e, on === null)
        var r = !1;
      else {
        if (e = on, on = null, el = 0, B & 6)
          throw Error(P(331));
        var o = B;
        for (B |= 4, M = e.current; M !== null; ) {
          var i = M, l = i.child;
          if (M.flags & 16) {
            var s = i.deletions;
            if (s !== null) {
              for (var a = 0; a < s.length; a++) {
                var u = s[a];
                for (M = u; M !== null; ) {
                  var c = M;
                  switch (c.tag) {
                    case 0:
                    case 11:
                    case 15:
                      no(8, c, i);
                  }
                  var f = c.child;
                  if (f !== null)
                    f.return = c, M = f;
                  else
                    for (; M !== null; ) {
                      c = M;
                      var p = c.sibling, v = c.return;
                      if (Tm(c), c === u) {
                        M = null;
                        break;
                      }
                      if (p !== null) {
                        p.return = v, M = p;
                        break;
                      }
                      M = v;
                    }
                }
              }
              var y = i.alternate;
              if (y !== null) {
                var g = y.child;
                if (g !== null) {
                  y.child = null;
                  do {
                    var _ = g.sibling;
                    g.sibling = null, g = _;
                  } while (g !== null);
                }
              }
              M = i;
            }
          }
          if (i.subtreeFlags & 2064 && l !== null)
            l.return = i, M = l;
          else
            e:
              for (; M !== null; ) {
                if (i = M, i.flags & 2048)
                  switch (i.tag) {
                    case 0:
                    case 11:
                    case 15:
                      no(9, i, i.return);
                  }
                var m = i.sibling;
                if (m !== null) {
                  m.return = i.return, M = m;
                  break e;
                }
                M = i.return;
              }
        }
        var d = e.current;
        for (M = d; M !== null; ) {
          l = M;
          var h = l.child;
          if (l.subtreeFlags & 2064 && h !== null)
            h.return = l, M = h;
          else
            e:
              for (l = d; M !== null; ) {
                if (s = M, s.flags & 2048)
                  try {
                    switch (s.tag) {
                      case 0:
                      case 11:
                      case 15:
                        xl(9, s);
                    }
                  } catch (E) {
                    fe(s, s.return, E);
                  }
                if (s === l) {
                  M = null;
                  break e;
                }
                var x = s.sibling;
                if (x !== null) {
                  x.return = s.return, M = x;
                  break e;
                }
                M = s.return;
              }
        }
        if (B = o, xn(), zt && typeof zt.onPostCommitFiberRoot == "function")
          try {
            zt.onPostCommitFiberRoot(fl, e);
          } catch {
          }
        r = !0;
      }
      return r;
    } finally {
      K = n, ft.transition = t;
    }
  }
  return !1;
}
function Of(e, t, n) {
  t = xr(n, t), t = ym(e, t, 1), e = fn(e, t, 1), t = Ae(), e !== null && (zo(e, 1, t), He(e, t));
}
function fe(e, t, n) {
  if (e.tag === 3)
    Of(e, e, n);
  else
    for (; t !== null; ) {
      if (t.tag === 3) {
        Of(t, e, n);
        break;
      } else if (t.tag === 1) {
        var r = t.stateNode;
        if (typeof t.type.getDerivedStateFromError == "function" || typeof r.componentDidCatch == "function" && (dn === null || !dn.has(r))) {
          e = xr(n, e), e = vm(t, e, 1), t = fn(t, e, 1), e = Ae(), t !== null && (zo(t, 1, e), He(t, e));
          break;
        }
      }
      t = t.return;
    }
}
function Ry(e, t, n) {
  var r = e.pingCache;
  r !== null && r.delete(t), t = Ae(), e.pingedLanes |= e.suspendedLanes & n, Ce === e && (Te & n) === n && (we === 4 || we === 3 && (Te & 130023424) === Te && 500 > de() - Au ? Tn(e, 0) : Iu |= n), He(e, t);
}
function bm(e, t) {
  t === 0 && (e.mode & 1 ? (t = Jo, Jo <<= 1, !(Jo & 130023424) && (Jo = 4194304)) : t = 1);
  var n = Ae();
  e = Ht(e, t), e !== null && (zo(e, t, n), He(e, n));
}
function Oy(e) {
  var t = e.memoizedState, n = 0;
  t !== null && (n = t.retryLane), bm(e, n);
}
function My(e, t) {
  var n = 0;
  switch (e.tag) {
    case 13:
      var r = e.stateNode, o = e.memoizedState;
      o !== null && (n = o.retryLane);
      break;
    case 19:
      r = e.stateNode;
      break;
    default:
      throw Error(P(314));
  }
  r !== null && r.delete(t), bm(e, n);
}
var Dm;
Dm = function(e, t, n) {
  if (e !== null)
    if (e.memoizedProps !== t.pendingProps || Ue.current)
      We = !0;
    else {
      if (!(e.lanes & n) && !(t.flags & 128))
        return We = !1, vy(e, t, n);
      We = !!(e.flags & 131072);
    }
  else
    We = !1, re && t.flags & 1048576 && Up(t, Hi, t.index);
  switch (t.lanes = 0, t.tag) {
    case 2:
      var r = t.type;
      Ci(e, t), e = t.pendingProps;
      var o = hr(t, Le.current);
      ur(t, n), o = Ou(null, t, r, e, o, n);
      var i = Mu();
      return t.flags |= 1, typeof o == "object" && o !== null && typeof o.render == "function" && o.$$typeof === void 0 ? (t.tag = 1, t.memoizedState = null, t.updateQueue = null, Ve(r) ? (i = !0, Ui(t)) : i = !1, t.memoizedState = o.state !== null && o.state !== void 0 ? o.state : null, _u(t), o.updater = vl, t.stateNode = o, o._reactInternals = t, $a(t, r, e, n), t = Ra(null, t, r, !0, i, n)) : (t.tag = 0, re && i && vu(t), Ie(null, t, o, n), t = t.child), t;
    case 16:
      r = t.elementType;
      e: {
        switch (Ci(e, t), e = t.pendingProps, o = r._init, r = o(r._payload), t.type = r, o = t.tag = zy(r), e = St(r, e), o) {
          case 0:
            t = Ta(null, t, r, e, n);
            break e;
          case 1:
            t = Sf(null, t, r, e, n);
            break e;
          case 11:
            t = vf(null, t, r, e, n);
            break e;
          case 14:
            t = xf(null, t, r, St(r.type, e), n);
            break e;
        }
        throw Error(P(
          306,
          r,
          ""
        ));
      }
      return t;
    case 0:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : St(r, o), Ta(e, t, r, o, n);
    case 1:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : St(r, o), Sf(e, t, r, o, n);
    case 3:
      e: {
        if (km(t), e === null)
          throw Error(P(387));
        r = t.pendingProps, i = t.memoizedState, o = i.element, Yp(e, t), Qi(t, r, null, n);
        var l = t.memoizedState;
        if (r = l.element, i.isDehydrated)
          if (i = { element: r, isDehydrated: !1, cache: l.cache, pendingSuspenseBoundaries: l.pendingSuspenseBoundaries, transitions: l.transitions }, t.updateQueue.baseState = i, t.memoizedState = i, t.flags & 256) {
            o = xr(Error(P(423)), t), t = wf(e, t, r, n, o);
            break e;
          } else if (r !== o) {
            o = xr(Error(P(424)), t), t = wf(e, t, r, n, o);
            break e;
          } else
            for (Ze = cn(t.stateNode.containerInfo.firstChild), qe = t, re = !0, kt = null, n = Gp(t, null, r, n), t.child = n; n; )
              n.flags = n.flags & -3 | 4096, n = n.sibling;
        else {
          if (gr(), r === o) {
            t = Kt(e, t, n);
            break e;
          }
          Ie(e, t, r, n);
        }
        t = t.child;
      }
      return t;
    case 5:
      return Xp(t), e === null && Ca(t), r = t.type, o = t.pendingProps, i = e !== null ? e.memoizedProps : null, l = o.children, va(r, o) ? l = null : i !== null && va(r, i) && (t.flags |= 32), wm(e, t), Ie(e, t, l, n), t.child;
    case 6:
      return e === null && Ca(t), null;
    case 13:
      return Cm(e, t, n);
    case 4:
      return $u(t, t.stateNode.containerInfo), r = t.pendingProps, e === null ? t.child = yr(t, null, r, n) : Ie(e, t, r, n), t.child;
    case 11:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : St(r, o), vf(e, t, r, o, n);
    case 7:
      return Ie(e, t, t.pendingProps, n), t.child;
    case 8:
      return Ie(e, t, t.pendingProps.children, n), t.child;
    case 12:
      return Ie(e, t, t.pendingProps.children, n), t.child;
    case 10:
      e: {
        if (r = t.type._context, o = t.pendingProps, i = t.memoizedProps, l = o.value, Y(Ki, r._currentValue), r._currentValue = l, i !== null)
          if ($t(i.value, l)) {
            if (i.children === o.children && !Ue.current) {
              t = Kt(e, t, n);
              break e;
            }
          } else
            for (i = t.child, i !== null && (i.return = t); i !== null; ) {
              var s = i.dependencies;
              if (s !== null) {
                l = i.child;
                for (var a = s.firstContext; a !== null; ) {
                  if (a.context === r) {
                    if (i.tag === 1) {
                      a = Wt(-1, n & -n), a.tag = 2;
                      var u = i.updateQueue;
                      if (u !== null) {
                        u = u.shared;
                        var c = u.pending;
                        c === null ? a.next = a : (a.next = c.next, c.next = a), u.pending = a;
                      }
                    }
                    i.lanes |= n, a = i.alternate, a !== null && (a.lanes |= n), Ea(
                      i.return,
                      n,
                      t
                    ), s.lanes |= n;
                    break;
                  }
                  a = a.next;
                }
              } else if (i.tag === 10)
                l = i.type === t.type ? null : i.child;
              else if (i.tag === 18) {
                if (l = i.return, l === null)
                  throw Error(P(341));
                l.lanes |= n, s = l.alternate, s !== null && (s.lanes |= n), Ea(l, n, t), l = i.sibling;
              } else
                l = i.child;
              if (l !== null)
                l.return = i;
              else
                for (l = i; l !== null; ) {
                  if (l === t) {
                    l = null;
                    break;
                  }
                  if (i = l.sibling, i !== null) {
                    i.return = l.return, l = i;
                    break;
                  }
                  l = l.return;
                }
              i = l;
            }
        Ie(e, t, o.children, n), t = t.child;
      }
      return t;
    case 9:
      return o = t.type, r = t.pendingProps.children, ur(t, n), o = dt(o), r = r(o), t.flags |= 1, Ie(e, t, r, n), t.child;
    case 14:
      return r = t.type, o = St(r, t.pendingProps), o = St(r.type, o), xf(e, t, r, o, n);
    case 15:
      return xm(e, t, t.type, t.pendingProps, n);
    case 17:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : St(r, o), Ci(e, t), t.tag = 1, Ve(r) ? (e = !0, Ui(t)) : e = !1, ur(t, n), gm(t, r, o), $a(t, r, o, n), Ra(null, t, r, !0, e, n);
    case 19:
      return Em(e, t, n);
    case 22:
      return Sm(e, t, n);
  }
  throw Error(P(156, t.tag));
};
function Fm(e, t) {
  return pp(e, t);
}
function Ny(e, t, n, r) {
  this.tag = e, this.key = n, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.ref = null, this.pendingProps = t, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = r, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
}
function ct(e, t, n, r) {
  return new Ny(e, t, n, r);
}
function Bu(e) {
  return e = e.prototype, !(!e || !e.isReactComponent);
}
function zy(e) {
  if (typeof e == "function")
    return Bu(e) ? 1 : 0;
  if (e != null) {
    if (e = e.$$typeof, e === lu)
      return 11;
    if (e === su)
      return 14;
  }
  return 2;
}
function mn(e, t) {
  var n = e.alternate;
  return n === null ? (n = ct(e.tag, t, e.key, e.mode), n.elementType = e.elementType, n.type = e.type, n.stateNode = e.stateNode, n.alternate = e, e.alternate = n) : (n.pendingProps = t, n.type = e.type, n.flags = 0, n.subtreeFlags = 0, n.deletions = null), n.flags = e.flags & 14680064, n.childLanes = e.childLanes, n.lanes = e.lanes, n.child = e.child, n.memoizedProps = e.memoizedProps, n.memoizedState = e.memoizedState, n.updateQueue = e.updateQueue, t = e.dependencies, n.dependencies = t === null ? null : { lanes: t.lanes, firstContext: t.firstContext }, n.sibling = e.sibling, n.index = e.index, n.ref = e.ref, n;
}
function $i(e, t, n, r, o, i) {
  var l = 2;
  if (r = e, typeof e == "function")
    Bu(e) && (l = 1);
  else if (typeof e == "string")
    l = 5;
  else
    e:
      switch (e) {
        case Qn:
          return Rn(n.children, o, i, t);
        case iu:
          l = 8, o |= 8;
          break;
        case Xs:
          return e = ct(12, n, t, o | 2), e.elementType = Xs, e.lanes = i, e;
        case Zs:
          return e = ct(13, n, t, o), e.elementType = Zs, e.lanes = i, e;
        case qs:
          return e = ct(19, n, t, o), e.elementType = qs, e.lanes = i, e;
        case Xd:
          return wl(n, o, i, t);
        default:
          if (typeof e == "object" && e !== null)
            switch (e.$$typeof) {
              case Qd:
                l = 10;
                break e;
              case Yd:
                l = 9;
                break e;
              case lu:
                l = 11;
                break e;
              case su:
                l = 14;
                break e;
              case Jt:
                l = 16, r = null;
                break e;
            }
          throw Error(P(130, e == null ? e : typeof e, ""));
      }
  return t = ct(l, n, t, o), t.elementType = e, t.type = r, t.lanes = i, t;
}
function Rn(e, t, n, r) {
  return e = ct(7, e, r, t), e.lanes = n, e;
}
function wl(e, t, n, r) {
  return e = ct(22, e, r, t), e.elementType = Xd, e.lanes = n, e.stateNode = { isHidden: !1 }, e;
}
function js(e, t, n) {
  return e = ct(6, e, null, t), e.lanes = n, e;
}
function Is(e, t, n) {
  return t = ct(4, e.children !== null ? e.children : [], e.key, t), t.lanes = n, t.stateNode = { containerInfo: e.containerInfo, pendingChildren: null, implementation: e.implementation }, t;
}
function Ly(e, t, n, r, o) {
  this.tag = t, this.containerInfo = e, this.finishedWork = this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.pendingContext = this.context = null, this.callbackPriority = 0, this.eventTimes = gs(0), this.expirationTimes = gs(-1), this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = gs(0), this.identifierPrefix = r, this.onRecoverableError = o, this.mutableSourceEagerHydrationData = null;
}
function Wu(e, t, n, r, o, i, l, s, a) {
  return e = new Ly(e, t, n, s, a), t === 1 ? (t = 1, i === !0 && (t |= 8)) : t = 0, i = ct(3, null, null, t), e.current = i, i.stateNode = e, i.memoizedState = { element: r, isDehydrated: n, cache: null, transitions: null, pendingSuspenseBoundaries: null }, _u(i), e;
}
function jy(e, t, n) {
  var r = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
  return { $$typeof: Gn, key: r == null ? null : "" + r, children: e, containerInfo: t, implementation: n };
}
function Bm(e) {
  if (!e)
    return gn;
  e = e._reactInternals;
  e: {
    if (An(e) !== e || e.tag !== 1)
      throw Error(P(170));
    var t = e;
    do {
      switch (t.tag) {
        case 3:
          t = t.stateNode.context;
          break e;
        case 1:
          if (Ve(t.type)) {
            t = t.stateNode.__reactInternalMemoizedMergedChildContext;
            break e;
          }
      }
      t = t.return;
    } while (t !== null);
    throw Error(P(171));
  }
  if (e.tag === 1) {
    var n = e.type;
    if (Ve(n))
      return Bp(e, n, t);
  }
  return t;
}
function Wm(e, t, n, r, o, i, l, s, a) {
  return e = Wu(n, r, !0, e, o, i, l, s, a), e.context = Bm(null), n = e.current, r = Ae(), o = pn(n), i = Wt(r, o), i.callback = t ?? null, fn(n, i, o), e.current.lanes = o, zo(e, o, r), He(e, r), e;
}
function kl(e, t, n, r) {
  var o = t.current, i = Ae(), l = pn(o);
  return n = Bm(n), t.context === null ? t.context = n : t.pendingContext = n, t = Wt(i, l), t.payload = { element: e }, r = r === void 0 ? null : r, r !== null && (t.callback = r), e = fn(o, t, l), e !== null && (_t(e, o, l, i), Si(e, o, l)), l;
}
function nl(e) {
  if (e = e.current, !e.child)
    return null;
  switch (e.child.tag) {
    case 5:
      return e.child.stateNode;
    default:
      return e.child.stateNode;
  }
}
function Mf(e, t) {
  if (e = e.memoizedState, e !== null && e.dehydrated !== null) {
    var n = e.retryLane;
    e.retryLane = n !== 0 && n < t ? n : t;
  }
}
function Uu(e, t) {
  Mf(e, t), (e = e.alternate) && Mf(e, t);
}
function Iy() {
  return null;
}
var Um = typeof reportError == "function" ? reportError : function(e) {
  console.error(e);
};
function Vu(e) {
  this._internalRoot = e;
}
Cl.prototype.render = Vu.prototype.render = function(e) {
  var t = this._internalRoot;
  if (t === null)
    throw Error(P(409));
  kl(e, t, null, null);
};
Cl.prototype.unmount = Vu.prototype.unmount = function() {
  var e = this._internalRoot;
  if (e !== null) {
    this._internalRoot = null;
    var t = e.containerInfo;
    jn(function() {
      kl(null, e, null, null);
    }), t[Vt] = null;
  }
};
function Cl(e) {
  this._internalRoot = e;
}
Cl.prototype.unstable_scheduleHydration = function(e) {
  if (e) {
    var t = Sp();
    e = { blockedOn: null, target: e, priority: t };
    for (var n = 0; n < tn.length && t !== 0 && t < tn[n].priority; n++)
      ;
    tn.splice(n, 0, e), n === 0 && kp(e);
  }
};
function Hu(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11);
}
function El(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11 && (e.nodeType !== 8 || e.nodeValue !== " react-mount-point-unstable "));
}
function Nf() {
}
function Ay(e, t, n, r, o) {
  if (o) {
    if (typeof r == "function") {
      var i = r;
      r = function() {
        var u = nl(l);
        i.call(u);
      };
    }
    var l = Wm(t, r, e, 0, null, !1, !1, "", Nf);
    return e._reactRootContainer = l, e[Vt] = l.current, ho(e.nodeType === 8 ? e.parentNode : e), jn(), l;
  }
  for (; o = e.lastChild; )
    e.removeChild(o);
  if (typeof r == "function") {
    var s = r;
    r = function() {
      var u = nl(a);
      s.call(u);
    };
  }
  var a = Wu(e, 0, !1, null, null, !1, !1, "", Nf);
  return e._reactRootContainer = a, e[Vt] = a.current, ho(e.nodeType === 8 ? e.parentNode : e), jn(function() {
    kl(t, a, n, r);
  }), a;
}
function _l(e, t, n, r, o) {
  var i = n._reactRootContainer;
  if (i) {
    var l = i;
    if (typeof o == "function") {
      var s = o;
      o = function() {
        var a = nl(l);
        s.call(a);
      };
    }
    kl(t, l, e, o);
  } else
    l = Ay(n, t, e, o, r);
  return nl(l);
}
vp = function(e) {
  switch (e.tag) {
    case 3:
      var t = e.stateNode;
      if (t.current.memoizedState.isDehydrated) {
        var n = Kr(t.pendingLanes);
        n !== 0 && (cu(t, n | 1), He(t, de()), !(B & 6) && (Sr = de() + 500, xn()));
      }
      break;
    case 13:
      jn(function() {
        var r = Ht(e, 1);
        if (r !== null) {
          var o = Ae();
          _t(r, e, 1, o);
        }
      }), Uu(e, 1);
  }
};
fu = function(e) {
  if (e.tag === 13) {
    var t = Ht(e, 134217728);
    if (t !== null) {
      var n = Ae();
      _t(t, e, 134217728, n);
    }
    Uu(e, 134217728);
  }
};
xp = function(e) {
  if (e.tag === 13) {
    var t = pn(e), n = Ht(e, t);
    if (n !== null) {
      var r = Ae();
      _t(n, e, t, r);
    }
    Uu(e, t);
  }
};
Sp = function() {
  return K;
};
wp = function(e, t) {
  var n = K;
  try {
    return K = e, t();
  } finally {
    K = n;
  }
};
aa = function(e, t, n) {
  switch (t) {
    case "input":
      if (ta(e, n), t = n.name, n.type === "radio" && t != null) {
        for (n = e; n.parentNode; )
          n = n.parentNode;
        for (n = n.querySelectorAll("input[name=" + JSON.stringify("" + t) + '][type="radio"]'), t = 0; t < n.length; t++) {
          var r = n[t];
          if (r !== e && r.form === e.form) {
            var o = hl(r);
            if (!o)
              throw Error(P(90));
            qd(r), ta(r, o);
          }
        }
      }
      break;
    case "textarea":
      ep(e, n);
      break;
    case "select":
      t = n.value, t != null && ir(e, !!n.multiple, t, !1);
  }
};
sp = bu;
ap = jn;
var by = { usingClientEntryPoint: !1, Events: [jo, qn, hl, ip, lp, bu] }, Fr = { findFiberByHostInstance: En, bundleType: 0, version: "18.3.1", rendererPackageName: "react-dom" }, Dy = { bundleType: Fr.bundleType, version: Fr.version, rendererPackageName: Fr.rendererPackageName, rendererConfig: Fr.rendererConfig, overrideHookState: null, overrideHookStateDeletePath: null, overrideHookStateRenamePath: null, overrideProps: null, overridePropsDeletePath: null, overridePropsRenamePath: null, setErrorHandler: null, setSuspenseHandler: null, scheduleUpdate: null, currentDispatcherRef: Qt.ReactCurrentDispatcher, findHostInstanceByFiber: function(e) {
  return e = fp(e), e === null ? null : e.stateNode;
}, findFiberByHostInstance: Fr.findFiberByHostInstance || Iy, findHostInstancesForRefresh: null, scheduleRefresh: null, scheduleRoot: null, setRefreshHandler: null, getCurrentFiber: null, reconcilerVersion: "18.3.1-next-f1338f8080-20240426" };
if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u") {
  var ci = __REACT_DEVTOOLS_GLOBAL_HOOK__;
  if (!ci.isDisabled && ci.supportsFiber)
    try {
      fl = ci.inject(Dy), zt = ci;
    } catch {
    }
}
tt.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = by;
tt.createPortal = function(e, t) {
  var n = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
  if (!Hu(t))
    throw Error(P(200));
  return jy(e, t, null, n);
};
tt.createRoot = function(e, t) {
  if (!Hu(e))
    throw Error(P(299));
  var n = !1, r = "", o = Um;
  return t != null && (t.unstable_strictMode === !0 && (n = !0), t.identifierPrefix !== void 0 && (r = t.identifierPrefix), t.onRecoverableError !== void 0 && (o = t.onRecoverableError)), t = Wu(e, 1, !1, null, null, n, !1, r, o), e[Vt] = t.current, ho(e.nodeType === 8 ? e.parentNode : e), new Vu(t);
};
tt.findDOMNode = function(e) {
  if (e == null)
    return null;
  if (e.nodeType === 1)
    return e;
  var t = e._reactInternals;
  if (t === void 0)
    throw typeof e.render == "function" ? Error(P(188)) : (e = Object.keys(e).join(","), Error(P(268, e)));
  return e = fp(t), e = e === null ? null : e.stateNode, e;
};
tt.flushSync = function(e) {
  return jn(e);
};
tt.hydrate = function(e, t, n) {
  if (!El(t))
    throw Error(P(200));
  return _l(null, e, t, !0, n);
};
tt.hydrateRoot = function(e, t, n) {
  if (!Hu(e))
    throw Error(P(405));
  var r = n != null && n.hydratedSources || null, o = !1, i = "", l = Um;
  if (n != null && (n.unstable_strictMode === !0 && (o = !0), n.identifierPrefix !== void 0 && (i = n.identifierPrefix), n.onRecoverableError !== void 0 && (l = n.onRecoverableError)), t = Wm(t, null, e, 1, n ?? null, o, !1, i, l), e[Vt] = t.current, ho(e), r)
    for (e = 0; e < r.length; e++)
      n = r[e], o = n._getVersion, o = o(n._source), t.mutableSourceEagerHydrationData == null ? t.mutableSourceEagerHydrationData = [n, o] : t.mutableSourceEagerHydrationData.push(
        n,
        o
      );
  return new Cl(t);
};
tt.render = function(e, t, n) {
  if (!El(t))
    throw Error(P(200));
  return _l(null, e, t, !1, n);
};
tt.unmountComponentAtNode = function(e) {
  if (!El(e))
    throw Error(P(40));
  return e._reactRootContainer ? (jn(function() {
    _l(null, null, e, !1, function() {
      e._reactRootContainer = null, e[Vt] = null;
    });
  }), !0) : !1;
};
tt.unstable_batchedUpdates = bu;
tt.unstable_renderSubtreeIntoContainer = function(e, t, n, r) {
  if (!El(n))
    throw Error(P(200));
  if (e == null || e._reactInternals === void 0)
    throw Error(P(38));
  return _l(e, t, n, !1, r);
};
tt.version = "18.3.1-next-f1338f8080-20240426";
function Vm() {
  if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function"))
    try {
      __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(Vm);
    } catch (e) {
      console.error(e);
    }
}
Vm(), Vd.exports = tt;
var Hm = Vd.exports;
const fi = /* @__PURE__ */ Nd(Hm);
var zf = Hm;
Qs.createRoot = zf.createRoot, Qs.hydrateRoot = zf.hydrateRoot;
function Eo(e) {
  let t = "https://mui.com/production-error/?code=" + e;
  for (let n = 1; n < arguments.length; n += 1)
    t += "&args[]=" + encodeURIComponent(arguments[n]);
  return "Minified MUI error #" + e + "; visit " + t + " for the full message.";
}
const Fy = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Eo
}, Symbol.toStringTag, { value: "Module" })), wr = "$$material";
function S() {
  return S = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t];
      for (var r in n)
        ({}).hasOwnProperty.call(n, r) && (e[r] = n[r]);
    }
    return e;
  }, S.apply(null, arguments);
}
function W(e, t) {
  if (e == null)
    return {};
  var n = {};
  for (var r in e)
    if ({}.hasOwnProperty.call(e, r)) {
      if (t.indexOf(r) !== -1)
        continue;
      n[r] = e[r];
    }
  return n;
}
var By = !1;
function Wy(e) {
  if (e.sheet)
    return e.sheet;
  for (var t = 0; t < document.styleSheets.length; t++)
    if (document.styleSheets[t].ownerNode === e)
      return document.styleSheets[t];
}
function Uy(e) {
  var t = document.createElement("style");
  return t.setAttribute("data-emotion", e.key), e.nonce !== void 0 && t.setAttribute("nonce", e.nonce), t.appendChild(document.createTextNode("")), t.setAttribute("data-s", ""), t;
}
var Vy = /* @__PURE__ */ function() {
  function e(n) {
    var r = this;
    this._insertTag = function(o) {
      var i;
      r.tags.length === 0 ? r.insertionPoint ? i = r.insertionPoint.nextSibling : r.prepend ? i = r.container.firstChild : i = r.before : i = r.tags[r.tags.length - 1].nextSibling, r.container.insertBefore(o, i), r.tags.push(o);
    }, this.isSpeedy = n.speedy === void 0 ? !By : n.speedy, this.tags = [], this.ctr = 0, this.nonce = n.nonce, this.key = n.key, this.container = n.container, this.prepend = n.prepend, this.insertionPoint = n.insertionPoint, this.before = null;
  }
  var t = e.prototype;
  return t.hydrate = function(r) {
    r.forEach(this._insertTag);
  }, t.insert = function(r) {
    this.ctr % (this.isSpeedy ? 65e3 : 1) === 0 && this._insertTag(Uy(this));
    var o = this.tags[this.tags.length - 1];
    if (this.isSpeedy) {
      var i = Wy(o);
      try {
        i.insertRule(r, i.cssRules.length);
      } catch {
      }
    } else
      o.appendChild(document.createTextNode(r));
    this.ctr++;
  }, t.flush = function() {
    this.tags.forEach(function(r) {
      var o;
      return (o = r.parentNode) == null ? void 0 : o.removeChild(r);
    }), this.tags = [], this.ctr = 0;
  }, e;
}(), Ne = "-ms-", rl = "-moz-", V = "-webkit-", Km = "comm", Ku = "rule", Gu = "decl", Hy = "@import", Gm = "@keyframes", Ky = "@layer", Gy = Math.abs, $l = String.fromCharCode, Qy = Object.assign;
function Yy(e, t) {
  return Pe(e, 0) ^ 45 ? (((t << 2 ^ Pe(e, 0)) << 2 ^ Pe(e, 1)) << 2 ^ Pe(e, 2)) << 2 ^ Pe(e, 3) : 0;
}
function Qm(e) {
  return e.trim();
}
function Xy(e, t) {
  return (e = t.exec(e)) ? e[0] : e;
}
function H(e, t, n) {
  return e.replace(t, n);
}
function Ba(e, t) {
  return e.indexOf(t);
}
function Pe(e, t) {
  return e.charCodeAt(t) | 0;
}
function _o(e, t, n) {
  return e.slice(t, n);
}
function Ot(e) {
  return e.length;
}
function Qu(e) {
  return e.length;
}
function di(e, t) {
  return t.push(e), e;
}
function Zy(e, t) {
  return e.map(t).join("");
}
var Pl = 1, kr = 1, Ym = 0, Ke = 0, ge = 0, $r = "";
function Tl(e, t, n, r, o, i, l) {
  return { value: e, root: t, parent: n, type: r, props: o, children: i, line: Pl, column: kr, length: l, return: "" };
}
function Br(e, t) {
  return Qy(Tl("", null, null, "", null, null, 0), e, { length: -e.length }, t);
}
function qy() {
  return ge;
}
function Jy() {
  return ge = Ke > 0 ? Pe($r, --Ke) : 0, kr--, ge === 10 && (kr = 1, Pl--), ge;
}
function Je() {
  return ge = Ke < Ym ? Pe($r, Ke++) : 0, kr++, ge === 10 && (kr = 1, Pl++), ge;
}
function jt() {
  return Pe($r, Ke);
}
function Pi() {
  return Ke;
}
function Ao(e, t) {
  return _o($r, e, t);
}
function $o(e) {
  switch (e) {
    case 0:
    case 9:
    case 10:
    case 13:
    case 32:
      return 5;
    case 33:
    case 43:
    case 44:
    case 47:
    case 62:
    case 64:
    case 126:
    case 59:
    case 123:
    case 125:
      return 4;
    case 58:
      return 3;
    case 34:
    case 39:
    case 40:
    case 91:
      return 2;
    case 41:
    case 93:
      return 1;
  }
  return 0;
}
function Xm(e) {
  return Pl = kr = 1, Ym = Ot($r = e), Ke = 0, [];
}
function Zm(e) {
  return $r = "", e;
}
function Ti(e) {
  return Qm(Ao(Ke - 1, Wa(e === 91 ? e + 2 : e === 40 ? e + 1 : e)));
}
function ev(e) {
  for (; (ge = jt()) && ge < 33; )
    Je();
  return $o(e) > 2 || $o(ge) > 3 ? "" : " ";
}
function tv(e, t) {
  for (; --t && Je() && !(ge < 48 || ge > 102 || ge > 57 && ge < 65 || ge > 70 && ge < 97); )
    ;
  return Ao(e, Pi() + (t < 6 && jt() == 32 && Je() == 32));
}
function Wa(e) {
  for (; Je(); )
    switch (ge) {
      case e:
        return Ke;
      case 34:
      case 39:
        e !== 34 && e !== 39 && Wa(ge);
        break;
      case 40:
        e === 41 && Wa(e);
        break;
      case 92:
        Je();
        break;
    }
  return Ke;
}
function nv(e, t) {
  for (; Je() && e + ge !== 47 + 10; )
    if (e + ge === 42 + 42 && jt() === 47)
      break;
  return "/*" + Ao(t, Ke - 1) + "*" + $l(e === 47 ? e : Je());
}
function rv(e) {
  for (; !$o(jt()); )
    Je();
  return Ao(e, Ke);
}
function ov(e) {
  return Zm(Ri("", null, null, null, [""], e = Xm(e), 0, [0], e));
}
function Ri(e, t, n, r, o, i, l, s, a) {
  for (var u = 0, c = 0, f = l, p = 0, v = 0, y = 0, g = 1, _ = 1, m = 1, d = 0, h = "", x = o, E = i, k = r, w = h; _; )
    switch (y = d, d = Je()) {
      case 40:
        if (y != 108 && Pe(w, f - 1) == 58) {
          Ba(w += H(Ti(d), "&", "&\f"), "&\f") != -1 && (m = -1);
          break;
        }
      case 34:
      case 39:
      case 91:
        w += Ti(d);
        break;
      case 9:
      case 10:
      case 13:
      case 32:
        w += ev(y);
        break;
      case 92:
        w += tv(Pi() - 1, 7);
        continue;
      case 47:
        switch (jt()) {
          case 42:
          case 47:
            di(iv(nv(Je(), Pi()), t, n), a);
            break;
          default:
            w += "/";
        }
        break;
      case 123 * g:
        s[u++] = Ot(w) * m;
      case 125 * g:
      case 59:
      case 0:
        switch (d) {
          case 0:
          case 125:
            _ = 0;
          case 59 + c:
            m == -1 && (w = H(w, /\f/g, "")), v > 0 && Ot(w) - f && di(v > 32 ? jf(w + ";", r, n, f - 1) : jf(H(w, " ", "") + ";", r, n, f - 2), a);
            break;
          case 59:
            w += ";";
          default:
            if (di(k = Lf(w, t, n, u, c, o, s, h, x = [], E = [], f), i), d === 123)
              if (c === 0)
                Ri(w, t, k, k, x, i, f, s, E);
              else
                switch (p === 99 && Pe(w, 3) === 110 ? 100 : p) {
                  case 100:
                  case 108:
                  case 109:
                  case 115:
                    Ri(e, k, k, r && di(Lf(e, k, k, 0, 0, o, s, h, o, x = [], f), E), o, E, f, s, r ? x : E);
                    break;
                  default:
                    Ri(w, k, k, k, [""], E, 0, s, E);
                }
        }
        u = c = v = 0, g = m = 1, h = w = "", f = l;
        break;
      case 58:
        f = 1 + Ot(w), v = y;
      default:
        if (g < 1) {
          if (d == 123)
            --g;
          else if (d == 125 && g++ == 0 && Jy() == 125)
            continue;
        }
        switch (w += $l(d), d * g) {
          case 38:
            m = c > 0 ? 1 : (w += "\f", -1);
            break;
          case 44:
            s[u++] = (Ot(w) - 1) * m, m = 1;
            break;
          case 64:
            jt() === 45 && (w += Ti(Je())), p = jt(), c = f = Ot(h = w += rv(Pi())), d++;
            break;
          case 45:
            y === 45 && Ot(w) == 2 && (g = 0);
        }
    }
  return i;
}
function Lf(e, t, n, r, o, i, l, s, a, u, c) {
  for (var f = o - 1, p = o === 0 ? i : [""], v = Qu(p), y = 0, g = 0, _ = 0; y < r; ++y)
    for (var m = 0, d = _o(e, f + 1, f = Gy(g = l[y])), h = e; m < v; ++m)
      (h = Qm(g > 0 ? p[m] + " " + d : H(d, /&\f/g, p[m]))) && (a[_++] = h);
  return Tl(e, t, n, o === 0 ? Ku : s, a, u, c);
}
function iv(e, t, n) {
  return Tl(e, t, n, Km, $l(qy()), _o(e, 2, -2), 0);
}
function jf(e, t, n, r) {
  return Tl(e, t, n, Gu, _o(e, 0, r), _o(e, r + 1, -1), r);
}
function fr(e, t) {
  for (var n = "", r = Qu(e), o = 0; o < r; o++)
    n += t(e[o], o, e, t) || "";
  return n;
}
function lv(e, t, n, r) {
  switch (e.type) {
    case Ky:
      if (e.children.length)
        break;
    case Hy:
    case Gu:
      return e.return = e.return || e.value;
    case Km:
      return "";
    case Gm:
      return e.return = e.value + "{" + fr(e.children, r) + "}";
    case Ku:
      e.value = e.props.join(",");
  }
  return Ot(n = fr(e.children, r)) ? e.return = e.value + "{" + n + "}" : "";
}
function sv(e) {
  var t = Qu(e);
  return function(n, r, o, i) {
    for (var l = "", s = 0; s < t; s++)
      l += e[s](n, r, o, i) || "";
    return l;
  };
}
function av(e) {
  return function(t) {
    t.root || (t = t.return) && e(t);
  };
}
function qm(e) {
  var t = /* @__PURE__ */ Object.create(null);
  return function(n) {
    return t[n] === void 0 && (t[n] = e(n)), t[n];
  };
}
var uv = function(t, n, r) {
  for (var o = 0, i = 0; o = i, i = jt(), o === 38 && i === 12 && (n[r] = 1), !$o(i); )
    Je();
  return Ao(t, Ke);
}, cv = function(t, n) {
  var r = -1, o = 44;
  do
    switch ($o(o)) {
      case 0:
        o === 38 && jt() === 12 && (n[r] = 1), t[r] += uv(Ke - 1, n, r);
        break;
      case 2:
        t[r] += Ti(o);
        break;
      case 4:
        if (o === 44) {
          t[++r] = jt() === 58 ? "&\f" : "", n[r] = t[r].length;
          break;
        }
      default:
        t[r] += $l(o);
    }
  while (o = Je());
  return t;
}, fv = function(t, n) {
  return Zm(cv(Xm(t), n));
}, If = /* @__PURE__ */ new WeakMap(), dv = function(t) {
  if (!(t.type !== "rule" || !t.parent || // positive .length indicates that this rule contains pseudo
  // negative .length indicates that this rule has been already prefixed
  t.length < 1)) {
    for (var n = t.value, r = t.parent, o = t.column === r.column && t.line === r.line; r.type !== "rule"; )
      if (r = r.parent, !r)
        return;
    if (!(t.props.length === 1 && n.charCodeAt(0) !== 58 && !If.get(r)) && !o) {
      If.set(t, !0);
      for (var i = [], l = fv(n, i), s = r.props, a = 0, u = 0; a < l.length; a++)
        for (var c = 0; c < s.length; c++, u++)
          t.props[u] = i[a] ? l[a].replace(/&\f/g, s[c]) : s[c] + " " + l[a];
    }
  }
}, pv = function(t) {
  if (t.type === "decl") {
    var n = t.value;
    // charcode for l
    n.charCodeAt(0) === 108 && // charcode for b
    n.charCodeAt(2) === 98 && (t.return = "", t.value = "");
  }
};
function Jm(e, t) {
  switch (Yy(e, t)) {
    case 5103:
      return V + "print-" + e + e;
    case 5737:
    case 4201:
    case 3177:
    case 3433:
    case 1641:
    case 4457:
    case 2921:
    case 5572:
    case 6356:
    case 5844:
    case 3191:
    case 6645:
    case 3005:
    case 6391:
    case 5879:
    case 5623:
    case 6135:
    case 4599:
    case 4855:
    case 4215:
    case 6389:
    case 5109:
    case 5365:
    case 5621:
    case 3829:
      return V + e + e;
    case 5349:
    case 4246:
    case 4810:
    case 6968:
    case 2756:
      return V + e + rl + e + Ne + e + e;
    case 6828:
    case 4268:
      return V + e + Ne + e + e;
    case 6165:
      return V + e + Ne + "flex-" + e + e;
    case 5187:
      return V + e + H(e, /(\w+).+(:[^]+)/, V + "box-$1$2" + Ne + "flex-$1$2") + e;
    case 5443:
      return V + e + Ne + "flex-item-" + H(e, /flex-|-self/, "") + e;
    case 4675:
      return V + e + Ne + "flex-line-pack" + H(e, /align-content|flex-|-self/, "") + e;
    case 5548:
      return V + e + Ne + H(e, "shrink", "negative") + e;
    case 5292:
      return V + e + Ne + H(e, "basis", "preferred-size") + e;
    case 6060:
      return V + "box-" + H(e, "-grow", "") + V + e + Ne + H(e, "grow", "positive") + e;
    case 4554:
      return V + H(e, /([^-])(transform)/g, "$1" + V + "$2") + e;
    case 6187:
      return H(H(H(e, /(zoom-|grab)/, V + "$1"), /(image-set)/, V + "$1"), e, "") + e;
    case 5495:
    case 3959:
      return H(e, /(image-set\([^]*)/, V + "$1$`$1");
    case 4968:
      return H(H(e, /(.+:)(flex-)?(.*)/, V + "box-pack:$3" + Ne + "flex-pack:$3"), /s.+-b[^;]+/, "justify") + V + e + e;
    case 4095:
    case 3583:
    case 4068:
    case 2532:
      return H(e, /(.+)-inline(.+)/, V + "$1$2") + e;
    case 8116:
    case 7059:
    case 5753:
    case 5535:
    case 5445:
    case 5701:
    case 4933:
    case 4677:
    case 5533:
    case 5789:
    case 5021:
    case 4765:
      if (Ot(e) - 1 - t > 6)
        switch (Pe(e, t + 1)) {
          case 109:
            if (Pe(e, t + 4) !== 45)
              break;
          case 102:
            return H(e, /(.+:)(.+)-([^]+)/, "$1" + V + "$2-$3$1" + rl + (Pe(e, t + 3) == 108 ? "$3" : "$2-$3")) + e;
          case 115:
            return ~Ba(e, "stretch") ? Jm(H(e, "stretch", "fill-available"), t) + e : e;
        }
      break;
    case 4949:
      if (Pe(e, t + 1) !== 115)
        break;
    case 6444:
      switch (Pe(e, Ot(e) - 3 - (~Ba(e, "!important") && 10))) {
        case 107:
          return H(e, ":", ":" + V) + e;
        case 101:
          return H(e, /(.+:)([^;!]+)(;|!.+)?/, "$1" + V + (Pe(e, 14) === 45 ? "inline-" : "") + "box$3$1" + V + "$2$3$1" + Ne + "$2box$3") + e;
      }
      break;
    case 5936:
      switch (Pe(e, t + 11)) {
        case 114:
          return V + e + Ne + H(e, /[svh]\w+-[tblr]{2}/, "tb") + e;
        case 108:
          return V + e + Ne + H(e, /[svh]\w+-[tblr]{2}/, "tb-rl") + e;
        case 45:
          return V + e + Ne + H(e, /[svh]\w+-[tblr]{2}/, "lr") + e;
      }
      return V + e + Ne + e + e;
  }
  return e;
}
var mv = function(t, n, r, o) {
  if (t.length > -1 && !t.return)
    switch (t.type) {
      case Gu:
        t.return = Jm(t.value, t.length);
        break;
      case Gm:
        return fr([Br(t, {
          value: H(t.value, "@", "@" + V)
        })], o);
      case Ku:
        if (t.length)
          return Zy(t.props, function(i) {
            switch (Xy(i, /(::plac\w+|:read-\w+)/)) {
              case ":read-only":
              case ":read-write":
                return fr([Br(t, {
                  props: [H(i, /:(read-\w+)/, ":" + rl + "$1")]
                })], o);
              case "::placeholder":
                return fr([Br(t, {
                  props: [H(i, /:(plac\w+)/, ":" + V + "input-$1")]
                }), Br(t, {
                  props: [H(i, /:(plac\w+)/, ":" + rl + "$1")]
                }), Br(t, {
                  props: [H(i, /:(plac\w+)/, Ne + "input-$1")]
                })], o);
            }
            return "";
          });
    }
}, hv = [mv], eh = function(t) {
  var n = t.key;
  if (n === "css") {
    var r = document.querySelectorAll("style[data-emotion]:not([data-s])");
    Array.prototype.forEach.call(r, function(g) {
      var _ = g.getAttribute("data-emotion");
      _.indexOf(" ") !== -1 && (document.head.appendChild(g), g.setAttribute("data-s", ""));
    });
  }
  var o = t.stylisPlugins || hv, i = {}, l, s = [];
  l = t.container || document.head, Array.prototype.forEach.call(
    // this means we will ignore elements which don't have a space in them which
    // means that the style elements we're looking at are only Emotion 11 server-rendered style elements
    document.querySelectorAll('style[data-emotion^="' + n + ' "]'),
    function(g) {
      for (var _ = g.getAttribute("data-emotion").split(" "), m = 1; m < _.length; m++)
        i[_[m]] = !0;
      s.push(g);
    }
  );
  var a, u = [dv, pv];
  {
    var c, f = [lv, av(function(g) {
      c.insert(g);
    })], p = sv(u.concat(o, f)), v = function(_) {
      return fr(ov(_), p);
    };
    a = function(_, m, d, h) {
      c = d, v(_ ? _ + "{" + m.styles + "}" : m.styles), h && (y.inserted[m.name] = !0);
    };
  }
  var y = {
    key: n,
    sheet: new Vy({
      key: n,
      container: l,
      nonce: t.nonce,
      speedy: t.speedy,
      prepend: t.prepend,
      insertionPoint: t.insertionPoint
    }),
    nonce: t.nonce,
    inserted: i,
    registered: {},
    insert: a
  };
  return y.sheet.hydrate(s), y;
}, th = { exports: {} }, G = {};
/** @license React v16.13.1
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ee = typeof Symbol == "function" && Symbol.for, Yu = Ee ? Symbol.for("react.element") : 60103, Xu = Ee ? Symbol.for("react.portal") : 60106, Rl = Ee ? Symbol.for("react.fragment") : 60107, Ol = Ee ? Symbol.for("react.strict_mode") : 60108, Ml = Ee ? Symbol.for("react.profiler") : 60114, Nl = Ee ? Symbol.for("react.provider") : 60109, zl = Ee ? Symbol.for("react.context") : 60110, Zu = Ee ? Symbol.for("react.async_mode") : 60111, Ll = Ee ? Symbol.for("react.concurrent_mode") : 60111, jl = Ee ? Symbol.for("react.forward_ref") : 60112, Il = Ee ? Symbol.for("react.suspense") : 60113, gv = Ee ? Symbol.for("react.suspense_list") : 60120, Al = Ee ? Symbol.for("react.memo") : 60115, bl = Ee ? Symbol.for("react.lazy") : 60116, yv = Ee ? Symbol.for("react.block") : 60121, vv = Ee ? Symbol.for("react.fundamental") : 60117, xv = Ee ? Symbol.for("react.responder") : 60118, Sv = Ee ? Symbol.for("react.scope") : 60119;
function rt(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Yu:
        switch (e = e.type, e) {
          case Zu:
          case Ll:
          case Rl:
          case Ml:
          case Ol:
          case Il:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case zl:
              case jl:
              case bl:
              case Al:
              case Nl:
                return e;
              default:
                return t;
            }
        }
      case Xu:
        return t;
    }
  }
}
function nh(e) {
  return rt(e) === Ll;
}
G.AsyncMode = Zu;
G.ConcurrentMode = Ll;
G.ContextConsumer = zl;
G.ContextProvider = Nl;
G.Element = Yu;
G.ForwardRef = jl;
G.Fragment = Rl;
G.Lazy = bl;
G.Memo = Al;
G.Portal = Xu;
G.Profiler = Ml;
G.StrictMode = Ol;
G.Suspense = Il;
G.isAsyncMode = function(e) {
  return nh(e) || rt(e) === Zu;
};
G.isConcurrentMode = nh;
G.isContextConsumer = function(e) {
  return rt(e) === zl;
};
G.isContextProvider = function(e) {
  return rt(e) === Nl;
};
G.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Yu;
};
G.isForwardRef = function(e) {
  return rt(e) === jl;
};
G.isFragment = function(e) {
  return rt(e) === Rl;
};
G.isLazy = function(e) {
  return rt(e) === bl;
};
G.isMemo = function(e) {
  return rt(e) === Al;
};
G.isPortal = function(e) {
  return rt(e) === Xu;
};
G.isProfiler = function(e) {
  return rt(e) === Ml;
};
G.isStrictMode = function(e) {
  return rt(e) === Ol;
};
G.isSuspense = function(e) {
  return rt(e) === Il;
};
G.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === Rl || e === Ll || e === Ml || e === Ol || e === Il || e === gv || typeof e == "object" && e !== null && (e.$$typeof === bl || e.$$typeof === Al || e.$$typeof === Nl || e.$$typeof === zl || e.$$typeof === jl || e.$$typeof === vv || e.$$typeof === xv || e.$$typeof === Sv || e.$$typeof === yv);
};
G.typeOf = rt;
th.exports = G;
var wv = th.exports, rh = wv, kv = {
  $$typeof: !0,
  render: !0,
  defaultProps: !0,
  displayName: !0,
  propTypes: !0
}, Cv = {
  $$typeof: !0,
  compare: !0,
  defaultProps: !0,
  displayName: !0,
  propTypes: !0,
  type: !0
}, oh = {};
oh[rh.ForwardRef] = kv;
oh[rh.Memo] = Cv;
var Ev = !0;
function ih(e, t, n) {
  var r = "";
  return n.split(" ").forEach(function(o) {
    e[o] !== void 0 ? t.push(e[o] + ";") : o && (r += o + " ");
  }), r;
}
var qu = function(t, n, r) {
  var o = t.key + "-" + n.name;
  // we only need to add the styles to the registered cache if the
  // class name could be used further down
  // the tree but if it's a string tag, we know it won't
  // so we don't have to add it to registered cache.
  // this improves memory usage since we can avoid storing the whole style string
  (r === !1 || // we need to always store it if we're in compat mode and
  // in node since emotion-server relies on whether a style is in
  // the registered cache to know whether a style is global or not
  // also, note that this check will be dead code eliminated in the browser
  Ev === !1) && t.registered[o] === void 0 && (t.registered[o] = n.styles);
}, Ju = function(t, n, r) {
  qu(t, n, r);
  var o = t.key + "-" + n.name;
  if (t.inserted[n.name] === void 0) {
    var i = n;
    do
      t.insert(n === i ? "." + o : "", i, t.sheet, !0), i = i.next;
    while (i !== void 0);
  }
};
function _v(e) {
  for (var t = 0, n, r = 0, o = e.length; o >= 4; ++r, o -= 4)
    n = e.charCodeAt(r) & 255 | (e.charCodeAt(++r) & 255) << 8 | (e.charCodeAt(++r) & 255) << 16 | (e.charCodeAt(++r) & 255) << 24, n = /* Math.imul(k, m): */
    (n & 65535) * 1540483477 + ((n >>> 16) * 59797 << 16), n ^= /* k >>> r: */
    n >>> 24, t = /* Math.imul(k, m): */
    (n & 65535) * 1540483477 + ((n >>> 16) * 59797 << 16) ^ /* Math.imul(h, m): */
    (t & 65535) * 1540483477 + ((t >>> 16) * 59797 << 16);
  switch (o) {
    case 3:
      t ^= (e.charCodeAt(r + 2) & 255) << 16;
    case 2:
      t ^= (e.charCodeAt(r + 1) & 255) << 8;
    case 1:
      t ^= e.charCodeAt(r) & 255, t = /* Math.imul(h, m): */
      (t & 65535) * 1540483477 + ((t >>> 16) * 59797 << 16);
  }
  return t ^= t >>> 13, t = /* Math.imul(h, m): */
  (t & 65535) * 1540483477 + ((t >>> 16) * 59797 << 16), ((t ^ t >>> 15) >>> 0).toString(36);
}
var $v = {
  animationIterationCount: 1,
  aspectRatio: 1,
  borderImageOutset: 1,
  borderImageSlice: 1,
  borderImageWidth: 1,
  boxFlex: 1,
  boxFlexGroup: 1,
  boxOrdinalGroup: 1,
  columnCount: 1,
  columns: 1,
  flex: 1,
  flexGrow: 1,
  flexPositive: 1,
  flexShrink: 1,
  flexNegative: 1,
  flexOrder: 1,
  gridRow: 1,
  gridRowEnd: 1,
  gridRowSpan: 1,
  gridRowStart: 1,
  gridColumn: 1,
  gridColumnEnd: 1,
  gridColumnSpan: 1,
  gridColumnStart: 1,
  msGridRow: 1,
  msGridRowSpan: 1,
  msGridColumn: 1,
  msGridColumnSpan: 1,
  fontWeight: 1,
  lineHeight: 1,
  opacity: 1,
  order: 1,
  orphans: 1,
  scale: 1,
  tabSize: 1,
  widows: 1,
  zIndex: 1,
  zoom: 1,
  WebkitLineClamp: 1,
  // SVG-related properties
  fillOpacity: 1,
  floodOpacity: 1,
  stopOpacity: 1,
  strokeDasharray: 1,
  strokeDashoffset: 1,
  strokeMiterlimit: 1,
  strokeOpacity: 1,
  strokeWidth: 1
}, Pv = !1, Tv = /[A-Z]|^ms/g, Rv = /_EMO_([^_]+?)_([^]*?)_EMO_/g, lh = function(t) {
  return t.charCodeAt(1) === 45;
}, Af = function(t) {
  return t != null && typeof t != "boolean";
}, As = /* @__PURE__ */ qm(function(e) {
  return lh(e) ? e : e.replace(Tv, "-$&").toLowerCase();
}), bf = function(t, n) {
  switch (t) {
    case "animation":
    case "animationName":
      if (typeof n == "string")
        return n.replace(Rv, function(r, o, i) {
          return Mt = {
            name: o,
            styles: i,
            next: Mt
          }, o;
        });
  }
  return $v[t] !== 1 && !lh(t) && typeof n == "number" && n !== 0 ? n + "px" : n;
}, Ov = "Component selectors can only be used in conjunction with @emotion/babel-plugin, the swc Emotion plugin, or another Emotion-aware compiler transform.";
function Po(e, t, n) {
  if (n == null)
    return "";
  var r = n;
  if (r.__emotion_styles !== void 0)
    return r;
  switch (typeof n) {
    case "boolean":
      return "";
    case "object": {
      var o = n;
      if (o.anim === 1)
        return Mt = {
          name: o.name,
          styles: o.styles,
          next: Mt
        }, o.name;
      var i = n;
      if (i.styles !== void 0) {
        var l = i.next;
        if (l !== void 0)
          for (; l !== void 0; )
            Mt = {
              name: l.name,
              styles: l.styles,
              next: Mt
            }, l = l.next;
        var s = i.styles + ";";
        return s;
      }
      return Mv(e, t, n);
    }
    case "function": {
      if (e !== void 0) {
        var a = Mt, u = n(e);
        return Mt = a, Po(e, t, u);
      }
      break;
    }
  }
  var c = n;
  if (t == null)
    return c;
  var f = t[c];
  return f !== void 0 ? f : c;
}
function Mv(e, t, n) {
  var r = "";
  if (Array.isArray(n))
    for (var o = 0; o < n.length; o++)
      r += Po(e, t, n[o]) + ";";
  else
    for (var i in n) {
      var l = n[i];
      if (typeof l != "object") {
        var s = l;
        t != null && t[s] !== void 0 ? r += i + "{" + t[s] + "}" : Af(s) && (r += As(i) + ":" + bf(i, s) + ";");
      } else {
        if (i === "NO_COMPONENT_SELECTOR" && Pv)
          throw new Error(Ov);
        if (Array.isArray(l) && typeof l[0] == "string" && (t == null || t[l[0]] === void 0))
          for (var a = 0; a < l.length; a++)
            Af(l[a]) && (r += As(i) + ":" + bf(i, l[a]) + ";");
        else {
          var u = Po(e, t, l);
          switch (i) {
            case "animation":
            case "animationName": {
              r += As(i) + ":" + u + ";";
              break;
            }
            default:
              r += i + "{" + u + "}";
          }
        }
      }
    }
  return r;
}
var Df = /label:\s*([^\s;{]+)\s*(;|$)/g, Mt;
function bo(e, t, n) {
  if (e.length === 1 && typeof e[0] == "object" && e[0] !== null && e[0].styles !== void 0)
    return e[0];
  var r = !0, o = "";
  Mt = void 0;
  var i = e[0];
  if (i == null || i.raw === void 0)
    r = !1, o += Po(n, t, i);
  else {
    var l = i;
    o += l[0];
  }
  for (var s = 1; s < e.length; s++)
    if (o += Po(n, t, e[s]), r) {
      var a = i;
      o += a[s];
    }
  Df.lastIndex = 0;
  for (var u = "", c; (c = Df.exec(o)) !== null; )
    u += "-" + c[1];
  var f = _v(o) + u;
  return {
    name: f,
    styles: o,
    next: Mt
  };
}
var Nv = function(t) {
  return t();
}, sh = Gs["useInsertionEffect"] ? Gs["useInsertionEffect"] : !1, ah = sh || Nv, Ff = sh || C.useLayoutEffect, zv = !1, uh = /* @__PURE__ */ C.createContext(
  // we're doing this to avoid preconstruct's dead code elimination in this one case
  // because this module is primarily intended for the browser and node
  // but it's also required in react native and similar environments sometimes
  // and we could have a special build just for that
  // but this is much easier and the native packages
  // might use a different theme context in the future anyway
  typeof HTMLElement < "u" ? /* @__PURE__ */ eh({
    key: "css"
  }) : null
), Lv = uh.Provider, ec = function(t) {
  return /* @__PURE__ */ C.forwardRef(function(n, r) {
    var o = C.useContext(uh);
    return t(n, o, r);
  });
}, Pr = /* @__PURE__ */ C.createContext({}), tc = {}.hasOwnProperty, Ua = "__EMOTION_TYPE_PLEASE_DO_NOT_USE__", jv = function(t, n) {
  var r = {};
  for (var o in n)
    tc.call(n, o) && (r[o] = n[o]);
  return r[Ua] = t, r;
}, Iv = function(t) {
  var n = t.cache, r = t.serialized, o = t.isStringTag;
  return qu(n, r, o), ah(function() {
    return Ju(n, r, o);
  }), null;
}, Av = /* @__PURE__ */ ec(function(e, t, n) {
  var r = e.css;
  typeof r == "string" && t.registered[r] !== void 0 && (r = t.registered[r]);
  var o = e[Ua], i = [r], l = "";
  typeof e.className == "string" ? l = ih(t.registered, i, e.className) : e.className != null && (l = e.className + " ");
  var s = bo(i, void 0, C.useContext(Pr));
  l += t.key + "-" + s.name;
  var a = {};
  for (var u in e)
    tc.call(e, u) && u !== "css" && u !== Ua && !zv && (a[u] = e[u]);
  return a.className = l, n && (a.ref = n), /* @__PURE__ */ C.createElement(C.Fragment, null, /* @__PURE__ */ C.createElement(Iv, {
    cache: t,
    serialized: s,
    isStringTag: typeof o == "string"
  }), /* @__PURE__ */ C.createElement(o, a));
}), bv = Av, bs = { exports: {} }, Bf;
function ch() {
  return Bf || (Bf = 1, function(e) {
    function t() {
      return e.exports = t = Object.assign ? Object.assign.bind() : function(n) {
        for (var r = 1; r < arguments.length; r++) {
          var o = arguments[r];
          for (var i in o)
            ({}).hasOwnProperty.call(o, i) && (n[i] = o[i]);
        }
        return n;
      }, e.exports.__esModule = !0, e.exports.default = e.exports, t.apply(null, arguments);
    }
    e.exports = t, e.exports.__esModule = !0, e.exports.default = e.exports;
  }(bs)), bs.exports;
}
ch();
var Wf = function(t, n) {
  var r = arguments;
  if (n == null || !tc.call(n, "css"))
    return C.createElement.apply(void 0, r);
  var o = r.length, i = new Array(o);
  i[0] = bv, i[1] = jv(t, n);
  for (var l = 2; l < o; l++)
    i[l] = r[l];
  return C.createElement.apply(null, i);
};
(function(e) {
  var t;
  t || (t = e.JSX || (e.JSX = {}));
})(Wf || (Wf = {}));
var Dv = /* @__PURE__ */ ec(function(e, t) {
  var n = e.styles, r = bo([n], void 0, C.useContext(Pr)), o = C.useRef();
  return Ff(function() {
    var i = t.key + "-global", l = new t.sheet.constructor({
      key: i,
      nonce: t.sheet.nonce,
      container: t.sheet.container,
      speedy: t.sheet.isSpeedy
    }), s = !1, a = document.querySelector('style[data-emotion="' + i + " " + r.name + '"]');
    return t.sheet.tags.length && (l.before = t.sheet.tags[0]), a !== null && (s = !0, a.setAttribute("data-emotion", i), l.hydrate([a])), o.current = [l, s], function() {
      l.flush();
    };
  }, [t]), Ff(function() {
    var i = o.current, l = i[0], s = i[1];
    if (s) {
      i[1] = !1;
      return;
    }
    if (r.next !== void 0 && Ju(t, r.next, !0), l.tags.length) {
      var a = l.tags[l.tags.length - 1].nextElementSibling;
      l.before = a, l.flush();
    }
    t.insert("", r, l, !1);
  }, [t, r.name]), null;
});
function Dl() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  return bo(t);
}
function Tr() {
  var e = Dl.apply(void 0, arguments), t = "animation-" + e.name;
  return {
    name: t,
    styles: "@keyframes " + t + "{" + e.styles + "}",
    anim: 1,
    toString: function() {
      return "_EMO_" + this.name + "_" + this.styles + "_EMO_";
    }
  };
}
var Fv = /^((children|dangerouslySetInnerHTML|key|ref|autoFocus|defaultValue|defaultChecked|innerHTML|suppressContentEditableWarning|suppressHydrationWarning|valueLink|abbr|accept|acceptCharset|accessKey|action|allow|allowUserMedia|allowPaymentRequest|allowFullScreen|allowTransparency|alt|async|autoComplete|autoPlay|capture|cellPadding|cellSpacing|challenge|charSet|checked|cite|classID|className|cols|colSpan|content|contentEditable|contextMenu|controls|controlsList|coords|crossOrigin|data|dateTime|decoding|default|defer|dir|disabled|disablePictureInPicture|disableRemotePlayback|download|draggable|encType|enterKeyHint|fetchpriority|fetchPriority|form|formAction|formEncType|formMethod|formNoValidate|formTarget|frameBorder|headers|height|hidden|high|href|hrefLang|htmlFor|httpEquiv|id|inputMode|integrity|is|keyParams|keyType|kind|label|lang|list|loading|loop|low|marginHeight|marginWidth|max|maxLength|media|mediaGroup|method|min|minLength|multiple|muted|name|nonce|noValidate|open|optimum|pattern|placeholder|playsInline|popover|popoverTarget|popoverTargetAction|poster|preload|profile|radioGroup|readOnly|referrerPolicy|rel|required|reversed|role|rows|rowSpan|sandbox|scope|scoped|scrolling|seamless|selected|shape|size|sizes|slot|span|spellCheck|src|srcDoc|srcLang|srcSet|start|step|style|summary|tabIndex|target|title|translate|type|useMap|value|width|wmode|wrap|about|datatype|inlist|prefix|property|resource|typeof|vocab|autoCapitalize|autoCorrect|autoSave|color|incremental|fallback|inert|itemProp|itemScope|itemType|itemID|itemRef|on|option|results|security|unselectable|accentHeight|accumulate|additive|alignmentBaseline|allowReorder|alphabetic|amplitude|arabicForm|ascent|attributeName|attributeType|autoReverse|azimuth|baseFrequency|baselineShift|baseProfile|bbox|begin|bias|by|calcMode|capHeight|clip|clipPathUnits|clipPath|clipRule|colorInterpolation|colorInterpolationFilters|colorProfile|colorRendering|contentScriptType|contentStyleType|cursor|cx|cy|d|decelerate|descent|diffuseConstant|direction|display|divisor|dominantBaseline|dur|dx|dy|edgeMode|elevation|enableBackground|end|exponent|externalResourcesRequired|fill|fillOpacity|fillRule|filter|filterRes|filterUnits|floodColor|floodOpacity|focusable|fontFamily|fontSize|fontSizeAdjust|fontStretch|fontStyle|fontVariant|fontWeight|format|from|fr|fx|fy|g1|g2|glyphName|glyphOrientationHorizontal|glyphOrientationVertical|glyphRef|gradientTransform|gradientUnits|hanging|horizAdvX|horizOriginX|ideographic|imageRendering|in|in2|intercept|k|k1|k2|k3|k4|kernelMatrix|kernelUnitLength|kerning|keyPoints|keySplines|keyTimes|lengthAdjust|letterSpacing|lightingColor|limitingConeAngle|local|markerEnd|markerMid|markerStart|markerHeight|markerUnits|markerWidth|mask|maskContentUnits|maskUnits|mathematical|mode|numOctaves|offset|opacity|operator|order|orient|orientation|origin|overflow|overlinePosition|overlineThickness|panose1|paintOrder|pathLength|patternContentUnits|patternTransform|patternUnits|pointerEvents|points|pointsAtX|pointsAtY|pointsAtZ|preserveAlpha|preserveAspectRatio|primitiveUnits|r|radius|refX|refY|renderingIntent|repeatCount|repeatDur|requiredExtensions|requiredFeatures|restart|result|rotate|rx|ry|scale|seed|shapeRendering|slope|spacing|specularConstant|specularExponent|speed|spreadMethod|startOffset|stdDeviation|stemh|stemv|stitchTiles|stopColor|stopOpacity|strikethroughPosition|strikethroughThickness|string|stroke|strokeDasharray|strokeDashoffset|strokeLinecap|strokeLinejoin|strokeMiterlimit|strokeOpacity|strokeWidth|surfaceScale|systemLanguage|tableValues|targetX|targetY|textAnchor|textDecoration|textRendering|textLength|to|transform|u1|u2|underlinePosition|underlineThickness|unicode|unicodeBidi|unicodeRange|unitsPerEm|vAlphabetic|vHanging|vIdeographic|vMathematical|values|vectorEffect|version|vertAdvY|vertOriginX|vertOriginY|viewBox|viewTarget|visibility|widths|wordSpacing|writingMode|x|xHeight|x1|x2|xChannelSelector|xlinkActuate|xlinkArcrole|xlinkHref|xlinkRole|xlinkShow|xlinkTitle|xlinkType|xmlBase|xmlns|xmlnsXlink|xmlLang|xmlSpace|y|y1|y2|yChannelSelector|z|zoomAndPan|for|class|autofocus)|(([Dd][Aa][Tt][Aa]|[Aa][Rr][Ii][Aa]|x)-.*))$/, Bv = /* @__PURE__ */ qm(
  function(e) {
    return Fv.test(e) || e.charCodeAt(0) === 111 && e.charCodeAt(1) === 110 && e.charCodeAt(2) < 91;
  }
  /* Z+1 */
), Wv = !1, Uv = Bv, Vv = function(t) {
  return t !== "theme";
}, Uf = function(t) {
  return typeof t == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  t.charCodeAt(0) > 96 ? Uv : Vv;
}, Vf = function(t, n, r) {
  var o;
  if (n) {
    var i = n.shouldForwardProp;
    o = t.__emotion_forwardProp && i ? function(l) {
      return t.__emotion_forwardProp(l) && i(l);
    } : i;
  }
  return typeof o != "function" && r && (o = t.__emotion_forwardProp), o;
}, Hv = function(t) {
  var n = t.cache, r = t.serialized, o = t.isStringTag;
  return qu(n, r, o), ah(function() {
    return Ju(n, r, o);
  }), null;
}, Kv = function e(t, n) {
  var r = t.__emotion_real === t, o = r && t.__emotion_base || t, i, l;
  n !== void 0 && (i = n.label, l = n.target);
  var s = Vf(t, n, r), a = s || Uf(o), u = !a("as");
  return function() {
    var c = arguments, f = r && t.__emotion_styles !== void 0 ? t.__emotion_styles.slice(0) : [];
    if (i !== void 0 && f.push("label:" + i + ";"), c[0] == null || c[0].raw === void 0)
      f.push.apply(f, c);
    else {
      var p = c[0];
      f.push(p[0]);
      for (var v = c.length, y = 1; y < v; y++)
        f.push(c[y], p[y]);
    }
    var g = ec(function(_, m, d) {
      var h = u && _.as || o, x = "", E = [], k = _;
      if (_.theme == null) {
        k = {};
        for (var w in _)
          k[w] = _[w];
        k.theme = C.useContext(Pr);
      }
      typeof _.className == "string" ? x = ih(m.registered, E, _.className) : _.className != null && (x = _.className + " ");
      var T = bo(f.concat(E), m.registered, k);
      x += m.key + "-" + T.name, l !== void 0 && (x += " " + l);
      var N = u && s === void 0 ? Uf(h) : a, O = {};
      for (var F in _)
        u && F === "as" || N(F) && (O[F] = _[F]);
      return O.className = x, d && (O.ref = d), /* @__PURE__ */ C.createElement(C.Fragment, null, /* @__PURE__ */ C.createElement(Hv, {
        cache: m,
        serialized: T,
        isStringTag: typeof h == "string"
      }), /* @__PURE__ */ C.createElement(h, O));
    });
    return g.displayName = i !== void 0 ? i : "Styled(" + (typeof o == "string" ? o : o.displayName || o.name || "Component") + ")", g.defaultProps = t.defaultProps, g.__emotion_real = g, g.__emotion_base = o, g.__emotion_styles = f, g.__emotion_forwardProp = s, Object.defineProperty(g, "toString", {
      value: function() {
        return l === void 0 && Wv ? "NO_COMPONENT_SELECTOR" : "." + l;
      }
    }), g.withComponent = function(_, m) {
      var d = e(_, S({}, n, m, {
        shouldForwardProp: Vf(g, m, !0)
      }));
      return d.apply(void 0, f);
    }, g;
  };
}, Gv = [
  "a",
  "abbr",
  "address",
  "area",
  "article",
  "aside",
  "audio",
  "b",
  "base",
  "bdi",
  "bdo",
  "big",
  "blockquote",
  "body",
  "br",
  "button",
  "canvas",
  "caption",
  "cite",
  "code",
  "col",
  "colgroup",
  "data",
  "datalist",
  "dd",
  "del",
  "details",
  "dfn",
  "dialog",
  "div",
  "dl",
  "dt",
  "em",
  "embed",
  "fieldset",
  "figcaption",
  "figure",
  "footer",
  "form",
  "h1",
  "h2",
  "h3",
  "h4",
  "h5",
  "h6",
  "head",
  "header",
  "hgroup",
  "hr",
  "html",
  "i",
  "iframe",
  "img",
  "input",
  "ins",
  "kbd",
  "keygen",
  "label",
  "legend",
  "li",
  "link",
  "main",
  "map",
  "mark",
  "marquee",
  "menu",
  "menuitem",
  "meta",
  "meter",
  "nav",
  "noscript",
  "object",
  "ol",
  "optgroup",
  "option",
  "output",
  "p",
  "param",
  "picture",
  "pre",
  "progress",
  "q",
  "rp",
  "rt",
  "ruby",
  "s",
  "samp",
  "script",
  "section",
  "select",
  "small",
  "source",
  "span",
  "strong",
  "style",
  "sub",
  "summary",
  "sup",
  "table",
  "tbody",
  "td",
  "textarea",
  "tfoot",
  "th",
  "thead",
  "time",
  "title",
  "tr",
  "track",
  "u",
  "ul",
  "var",
  "video",
  "wbr",
  // SVG
  "circle",
  "clipPath",
  "defs",
  "ellipse",
  "foreignObject",
  "g",
  "image",
  "line",
  "linearGradient",
  "mask",
  "path",
  "pattern",
  "polygon",
  "polyline",
  "radialGradient",
  "rect",
  "stop",
  "svg",
  "text",
  "tspan"
], Va = Kv.bind(null);
Gv.forEach(function(e) {
  Va[e] = Va(e);
});
function Qv(e, t) {
  const n = eh({
    key: "css",
    prepend: e
  });
  if (t) {
    const r = n.insert;
    n.insert = (...o) => (o[1].styles.match(/^@layer\s+[^{]*$/) || (o[1].styles = `@layer mui {${o[1].styles}}`), r(...o));
  }
  return n;
}
const Ds = /* @__PURE__ */ new Map();
function Yv(e) {
  const {
    injectFirst: t,
    enableCssLayer: n,
    children: r
  } = e, o = C.useMemo(() => {
    const i = `${t}-${n}`;
    if (typeof document == "object" && Ds.has(i))
      return Ds.get(i);
    const l = Qv(t, n);
    return Ds.set(i, l), l;
  }, [t, n]);
  return t || n ? /* @__PURE__ */ $.jsx(Lv, {
    value: o,
    children: r
  }) : r;
}
function Xv(e) {
  return e == null || Object.keys(e).length === 0;
}
function fh(e) {
  const {
    styles: t,
    defaultTheme: n = {}
  } = e, r = typeof t == "function" ? (o) => t(Xv(o) ? n : o) : t;
  return /* @__PURE__ */ $.jsx(Dv, {
    styles: r
  });
}
/**
 * @mui/styled-engine v5.18.0
 *
 * @license MIT
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
function nc(e, t) {
  return Va(e, t);
}
const dh = (e, t) => {
  Array.isArray(e.__emotion_styles) && (e.__emotion_styles = t(e.__emotion_styles));
}, Hf = [];
function ol(e) {
  return Hf[0] = e, bo(Hf);
}
const Zv = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  GlobalStyles: fh,
  StyledEngineProvider: Yv,
  ThemeContext: Pr,
  css: Dl,
  default: nc,
  internal_processStyles: dh,
  internal_serializeStyles: ol,
  keyframes: Tr
}, Symbol.toStringTag, { value: "Module" }));
function Dt(e) {
  if (typeof e != "object" || e === null)
    return !1;
  const t = Object.getPrototypeOf(e);
  return (t === null || t === Object.prototype || Object.getPrototypeOf(t) === null) && !(Symbol.toStringTag in e) && !(Symbol.iterator in e);
}
function ph(e) {
  if (/* @__PURE__ */ C.isValidElement(e) || !Dt(e))
    return e;
  const t = {};
  return Object.keys(e).forEach((n) => {
    t[n] = ph(e[n]);
  }), t;
}
function It(e, t, n = {
  clone: !0
}) {
  const r = n.clone ? S({}, e) : e;
  return Dt(e) && Dt(t) && Object.keys(t).forEach((o) => {
    /* @__PURE__ */ C.isValidElement(t[o]) ? r[o] = t[o] : Dt(t[o]) && // Avoid prototype pollution
    Object.prototype.hasOwnProperty.call(e, o) && Dt(e[o]) ? r[o] = It(e[o], t[o], n) : n.clone ? r[o] = Dt(t[o]) ? ph(t[o]) : t[o] : r[o] = t[o];
  }), r;
}
const qv = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: It,
  isPlainObject: Dt
}, Symbol.toStringTag, { value: "Module" })), Jv = ["values", "unit", "step"], e1 = (e) => {
  const t = Object.keys(e).map((n) => ({
    key: n,
    val: e[n]
  })) || [];
  return t.sort((n, r) => n.val - r.val), t.reduce((n, r) => S({}, n, {
    [r.key]: r.val
  }), {});
};
function mh(e) {
  const {
    // The breakpoint **start** at this value.
    // For instance with the first breakpoint xs: [xs, sm).
    values: t = {
      xs: 0,
      // phone
      sm: 600,
      // tablet
      md: 900,
      // small laptop
      lg: 1200,
      // desktop
      xl: 1536
      // large screen
    },
    unit: n = "px",
    step: r = 5
  } = e, o = W(e, Jv), i = e1(t), l = Object.keys(i);
  function s(p) {
    return `@media (min-width:${typeof t[p] == "number" ? t[p] : p}${n})`;
  }
  function a(p) {
    return `@media (max-width:${(typeof t[p] == "number" ? t[p] : p) - r / 100}${n})`;
  }
  function u(p, v) {
    const y = l.indexOf(v);
    return `@media (min-width:${typeof t[p] == "number" ? t[p] : p}${n}) and (max-width:${(y !== -1 && typeof t[l[y]] == "number" ? t[l[y]] : v) - r / 100}${n})`;
  }
  function c(p) {
    return l.indexOf(p) + 1 < l.length ? u(p, l[l.indexOf(p) + 1]) : s(p);
  }
  function f(p) {
    const v = l.indexOf(p);
    return v === 0 ? s(l[1]) : v === l.length - 1 ? a(l[v]) : u(p, l[l.indexOf(p) + 1]).replace("@media", "@media not all and");
  }
  return S({
    keys: l,
    values: i,
    up: s,
    down: a,
    between: u,
    only: c,
    not: f,
    unit: n
  }, o);
}
const t1 = {
  borderRadius: 4
}, n1 = t1;
function io(e, t) {
  return t ? It(e, t, {
    clone: !1
    // No need to clone deep, it's way faster.
  }) : e;
}
const rc = {
  xs: 0,
  // phone
  sm: 600,
  // tablet
  md: 900,
  // small laptop
  lg: 1200,
  // desktop
  xl: 1536
  // large screen
}, Kf = {
  // Sorted ASC by size. That's important.
  // It can't be configured as it's used statically for propTypes.
  keys: ["xs", "sm", "md", "lg", "xl"],
  up: (e) => `@media (min-width:${rc[e]}px)`
};
function mt(e, t, n) {
  const r = e.theme || {};
  if (Array.isArray(t)) {
    const i = r.breakpoints || Kf;
    return t.reduce((l, s, a) => (l[i.up(i.keys[a])] = n(t[a]), l), {});
  }
  if (typeof t == "object") {
    const i = r.breakpoints || Kf;
    return Object.keys(t).reduce((l, s) => {
      if (Object.keys(i.values || rc).indexOf(s) !== -1) {
        const a = i.up(s);
        l[a] = n(t[s], s);
      } else {
        const a = s;
        l[a] = t[a];
      }
      return l;
    }, {});
  }
  return n(t);
}
function r1(e = {}) {
  var t;
  return ((t = e.keys) == null ? void 0 : t.reduce((r, o) => {
    const i = e.up(o);
    return r[i] = {}, r;
  }, {})) || {};
}
function Gf(e, t) {
  return e.reduce((n, r) => {
    const o = n[r];
    return (!o || Object.keys(o).length === 0) && delete n[r], n;
  }, t);
}
function o1(e, t) {
  if (typeof e != "object")
    return {};
  const n = {}, r = Object.keys(t);
  return Array.isArray(e) ? r.forEach((o, i) => {
    i < e.length && (n[o] = !0);
  }) : r.forEach((o) => {
    e[o] != null && (n[o] = !0);
  }), n;
}
function Fl({
  values: e,
  breakpoints: t,
  base: n
}) {
  const r = n || o1(e, t), o = Object.keys(r);
  if (o.length === 0)
    return e;
  let i;
  return o.reduce((l, s, a) => (Array.isArray(e) ? (l[s] = e[a] != null ? e[a] : e[i], i = a) : typeof e == "object" ? (l[s] = e[s] != null ? e[s] : e[i], i = s) : l[s] = e, l), {});
}
function X(e) {
  if (typeof e != "string")
    throw new Error(Eo(7));
  return e.charAt(0).toUpperCase() + e.slice(1);
}
const i1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: X
}, Symbol.toStringTag, { value: "Module" }));
function Bl(e, t, n = !0) {
  if (!t || typeof t != "string")
    return null;
  if (e && e.vars && n) {
    const r = `vars.${t}`.split(".").reduce((o, i) => o && o[i] ? o[i] : null, e);
    if (r != null)
      return r;
  }
  return t.split(".").reduce((r, o) => r && r[o] != null ? r[o] : null, e);
}
function il(e, t, n, r = n) {
  let o;
  return typeof e == "function" ? o = e(n) : Array.isArray(e) ? o = e[n] || r : o = Bl(e, n) || r, t && (o = t(o, r, e)), o;
}
function pe(e) {
  const {
    prop: t,
    cssProperty: n = e.prop,
    themeKey: r,
    transform: o
  } = e, i = (l) => {
    if (l[t] == null)
      return null;
    const s = l[t], a = l.theme, u = Bl(a, r) || {};
    return mt(l, s, (f) => {
      let p = il(u, o, f);
      return f === p && typeof f == "string" && (p = il(u, o, `${t}${f === "default" ? "" : X(f)}`, f)), n === !1 ? p : {
        [n]: p
      };
    });
  };
  return i.propTypes = {}, i.filterProps = [t], i;
}
function l1(e) {
  const t = {};
  return (n) => (t[n] === void 0 && (t[n] = e(n)), t[n]);
}
const s1 = {
  m: "margin",
  p: "padding"
}, a1 = {
  t: "Top",
  r: "Right",
  b: "Bottom",
  l: "Left",
  x: ["Left", "Right"],
  y: ["Top", "Bottom"]
}, Qf = {
  marginX: "mx",
  marginY: "my",
  paddingX: "px",
  paddingY: "py"
}, u1 = l1((e) => {
  if (e.length > 2)
    if (Qf[e])
      e = Qf[e];
    else
      return [e];
  const [t, n] = e.split(""), r = s1[t], o = a1[n] || "";
  return Array.isArray(o) ? o.map((i) => r + i) : [r + o];
}), oc = ["m", "mt", "mr", "mb", "ml", "mx", "my", "margin", "marginTop", "marginRight", "marginBottom", "marginLeft", "marginX", "marginY", "marginInline", "marginInlineStart", "marginInlineEnd", "marginBlock", "marginBlockStart", "marginBlockEnd"], ic = ["p", "pt", "pr", "pb", "pl", "px", "py", "padding", "paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "paddingX", "paddingY", "paddingInline", "paddingInlineStart", "paddingInlineEnd", "paddingBlock", "paddingBlockStart", "paddingBlockEnd"];
[...oc, ...ic];
function Do(e, t, n, r) {
  var o;
  const i = (o = Bl(e, t, !1)) != null ? o : n;
  return typeof i == "number" ? (l) => typeof l == "string" ? l : i * l : Array.isArray(i) ? (l) => typeof l == "string" ? l : i[l] : typeof i == "function" ? i : () => {
  };
}
function hh(e) {
  return Do(e, "spacing", 8);
}
function Fo(e, t) {
  if (typeof t == "string" || t == null)
    return t;
  const n = Math.abs(t), r = e(n);
  return t >= 0 ? r : typeof r == "number" ? -r : `-${r}`;
}
function c1(e, t) {
  return (n) => e.reduce((r, o) => (r[o] = Fo(t, n), r), {});
}
function f1(e, t, n, r) {
  if (t.indexOf(n) === -1)
    return null;
  const o = u1(n), i = c1(o, r), l = e[n];
  return mt(e, l, i);
}
function gh(e, t) {
  const n = hh(e.theme);
  return Object.keys(e).map((r) => f1(e, t, r, n)).reduce(io, {});
}
function ue(e) {
  return gh(e, oc);
}
ue.propTypes = {};
ue.filterProps = oc;
function ce(e) {
  return gh(e, ic);
}
ce.propTypes = {};
ce.filterProps = ic;
function d1(e = 8) {
  if (e.mui)
    return e;
  const t = hh({
    spacing: e
  }), n = (...r) => (r.length === 0 ? [1] : r).map((i) => {
    const l = t(i);
    return typeof l == "number" ? `${l}px` : l;
  }).join(" ");
  return n.mui = !0, n;
}
function Wl(...e) {
  const t = e.reduce((r, o) => (o.filterProps.forEach((i) => {
    r[i] = o;
  }), r), {}), n = (r) => Object.keys(r).reduce((o, i) => t[i] ? io(o, t[i](r)) : o, {});
  return n.propTypes = {}, n.filterProps = e.reduce((r, o) => r.concat(o.filterProps), []), n;
}
function ut(e) {
  return typeof e != "number" ? e : `${e}px solid`;
}
function gt(e, t) {
  return pe({
    prop: e,
    themeKey: "borders",
    transform: t
  });
}
const p1 = gt("border", ut), m1 = gt("borderTop", ut), h1 = gt("borderRight", ut), g1 = gt("borderBottom", ut), y1 = gt("borderLeft", ut), v1 = gt("borderColor"), x1 = gt("borderTopColor"), S1 = gt("borderRightColor"), w1 = gt("borderBottomColor"), k1 = gt("borderLeftColor"), C1 = gt("outline", ut), E1 = gt("outlineColor"), Ul = (e) => {
  if (e.borderRadius !== void 0 && e.borderRadius !== null) {
    const t = Do(e.theme, "shape.borderRadius", 4), n = (r) => ({
      borderRadius: Fo(t, r)
    });
    return mt(e, e.borderRadius, n);
  }
  return null;
};
Ul.propTypes = {};
Ul.filterProps = ["borderRadius"];
Wl(p1, m1, h1, g1, y1, v1, x1, S1, w1, k1, Ul, C1, E1);
const Vl = (e) => {
  if (e.gap !== void 0 && e.gap !== null) {
    const t = Do(e.theme, "spacing", 8), n = (r) => ({
      gap: Fo(t, r)
    });
    return mt(e, e.gap, n);
  }
  return null;
};
Vl.propTypes = {};
Vl.filterProps = ["gap"];
const Hl = (e) => {
  if (e.columnGap !== void 0 && e.columnGap !== null) {
    const t = Do(e.theme, "spacing", 8), n = (r) => ({
      columnGap: Fo(t, r)
    });
    return mt(e, e.columnGap, n);
  }
  return null;
};
Hl.propTypes = {};
Hl.filterProps = ["columnGap"];
const Kl = (e) => {
  if (e.rowGap !== void 0 && e.rowGap !== null) {
    const t = Do(e.theme, "spacing", 8), n = (r) => ({
      rowGap: Fo(t, r)
    });
    return mt(e, e.rowGap, n);
  }
  return null;
};
Kl.propTypes = {};
Kl.filterProps = ["rowGap"];
const _1 = pe({
  prop: "gridColumn"
}), $1 = pe({
  prop: "gridRow"
}), P1 = pe({
  prop: "gridAutoFlow"
}), T1 = pe({
  prop: "gridAutoColumns"
}), R1 = pe({
  prop: "gridAutoRows"
}), O1 = pe({
  prop: "gridTemplateColumns"
}), M1 = pe({
  prop: "gridTemplateRows"
}), N1 = pe({
  prop: "gridTemplateAreas"
}), z1 = pe({
  prop: "gridArea"
});
Wl(Vl, Hl, Kl, _1, $1, P1, T1, R1, O1, M1, N1, z1);
function dr(e, t) {
  return t === "grey" ? t : e;
}
const L1 = pe({
  prop: "color",
  themeKey: "palette",
  transform: dr
}), j1 = pe({
  prop: "bgcolor",
  cssProperty: "backgroundColor",
  themeKey: "palette",
  transform: dr
}), I1 = pe({
  prop: "backgroundColor",
  themeKey: "palette",
  transform: dr
});
Wl(L1, j1, I1);
function Xe(e) {
  return e <= 1 && e !== 0 ? `${e * 100}%` : e;
}
const A1 = pe({
  prop: "width",
  transform: Xe
}), lc = (e) => {
  if (e.maxWidth !== void 0 && e.maxWidth !== null) {
    const t = (n) => {
      var r, o;
      const i = ((r = e.theme) == null || (r = r.breakpoints) == null || (r = r.values) == null ? void 0 : r[n]) || rc[n];
      return i ? ((o = e.theme) == null || (o = o.breakpoints) == null ? void 0 : o.unit) !== "px" ? {
        maxWidth: `${i}${e.theme.breakpoints.unit}`
      } : {
        maxWidth: i
      } : {
        maxWidth: Xe(n)
      };
    };
    return mt(e, e.maxWidth, t);
  }
  return null;
};
lc.filterProps = ["maxWidth"];
const b1 = pe({
  prop: "minWidth",
  transform: Xe
}), D1 = pe({
  prop: "height",
  transform: Xe
}), F1 = pe({
  prop: "maxHeight",
  transform: Xe
}), B1 = pe({
  prop: "minHeight",
  transform: Xe
});
pe({
  prop: "size",
  cssProperty: "width",
  transform: Xe
});
pe({
  prop: "size",
  cssProperty: "height",
  transform: Xe
});
const W1 = pe({
  prop: "boxSizing"
});
Wl(A1, lc, b1, D1, F1, B1, W1);
const U1 = {
  // borders
  border: {
    themeKey: "borders",
    transform: ut
  },
  borderTop: {
    themeKey: "borders",
    transform: ut
  },
  borderRight: {
    themeKey: "borders",
    transform: ut
  },
  borderBottom: {
    themeKey: "borders",
    transform: ut
  },
  borderLeft: {
    themeKey: "borders",
    transform: ut
  },
  borderColor: {
    themeKey: "palette"
  },
  borderTopColor: {
    themeKey: "palette"
  },
  borderRightColor: {
    themeKey: "palette"
  },
  borderBottomColor: {
    themeKey: "palette"
  },
  borderLeftColor: {
    themeKey: "palette"
  },
  outline: {
    themeKey: "borders",
    transform: ut
  },
  outlineColor: {
    themeKey: "palette"
  },
  borderRadius: {
    themeKey: "shape.borderRadius",
    style: Ul
  },
  // palette
  color: {
    themeKey: "palette",
    transform: dr
  },
  bgcolor: {
    themeKey: "palette",
    cssProperty: "backgroundColor",
    transform: dr
  },
  backgroundColor: {
    themeKey: "palette",
    transform: dr
  },
  // spacing
  p: {
    style: ce
  },
  pt: {
    style: ce
  },
  pr: {
    style: ce
  },
  pb: {
    style: ce
  },
  pl: {
    style: ce
  },
  px: {
    style: ce
  },
  py: {
    style: ce
  },
  padding: {
    style: ce
  },
  paddingTop: {
    style: ce
  },
  paddingRight: {
    style: ce
  },
  paddingBottom: {
    style: ce
  },
  paddingLeft: {
    style: ce
  },
  paddingX: {
    style: ce
  },
  paddingY: {
    style: ce
  },
  paddingInline: {
    style: ce
  },
  paddingInlineStart: {
    style: ce
  },
  paddingInlineEnd: {
    style: ce
  },
  paddingBlock: {
    style: ce
  },
  paddingBlockStart: {
    style: ce
  },
  paddingBlockEnd: {
    style: ce
  },
  m: {
    style: ue
  },
  mt: {
    style: ue
  },
  mr: {
    style: ue
  },
  mb: {
    style: ue
  },
  ml: {
    style: ue
  },
  mx: {
    style: ue
  },
  my: {
    style: ue
  },
  margin: {
    style: ue
  },
  marginTop: {
    style: ue
  },
  marginRight: {
    style: ue
  },
  marginBottom: {
    style: ue
  },
  marginLeft: {
    style: ue
  },
  marginX: {
    style: ue
  },
  marginY: {
    style: ue
  },
  marginInline: {
    style: ue
  },
  marginInlineStart: {
    style: ue
  },
  marginInlineEnd: {
    style: ue
  },
  marginBlock: {
    style: ue
  },
  marginBlockStart: {
    style: ue
  },
  marginBlockEnd: {
    style: ue
  },
  // display
  displayPrint: {
    cssProperty: !1,
    transform: (e) => ({
      "@media print": {
        display: e
      }
    })
  },
  display: {},
  overflow: {},
  textOverflow: {},
  visibility: {},
  whiteSpace: {},
  // flexbox
  flexBasis: {},
  flexDirection: {},
  flexWrap: {},
  justifyContent: {},
  alignItems: {},
  alignContent: {},
  order: {},
  flex: {},
  flexGrow: {},
  flexShrink: {},
  alignSelf: {},
  justifyItems: {},
  justifySelf: {},
  // grid
  gap: {
    style: Vl
  },
  rowGap: {
    style: Kl
  },
  columnGap: {
    style: Hl
  },
  gridColumn: {},
  gridRow: {},
  gridAutoFlow: {},
  gridAutoColumns: {},
  gridAutoRows: {},
  gridTemplateColumns: {},
  gridTemplateRows: {},
  gridTemplateAreas: {},
  gridArea: {},
  // positions
  position: {},
  zIndex: {
    themeKey: "zIndex"
  },
  top: {},
  right: {},
  bottom: {},
  left: {},
  // shadows
  boxShadow: {
    themeKey: "shadows"
  },
  // sizing
  width: {
    transform: Xe
  },
  maxWidth: {
    style: lc
  },
  minWidth: {
    transform: Xe
  },
  height: {
    transform: Xe
  },
  maxHeight: {
    transform: Xe
  },
  minHeight: {
    transform: Xe
  },
  boxSizing: {},
  // typography
  fontFamily: {
    themeKey: "typography"
  },
  fontSize: {
    themeKey: "typography"
  },
  fontStyle: {
    themeKey: "typography"
  },
  fontWeight: {
    themeKey: "typography"
  },
  letterSpacing: {},
  textTransform: {},
  lineHeight: {},
  textAlign: {},
  typography: {
    cssProperty: !1,
    themeKey: "typography"
  }
}, Bo = U1;
function V1(...e) {
  const t = e.reduce((r, o) => r.concat(Object.keys(o)), []), n = new Set(t);
  return e.every((r) => n.size === Object.keys(r).length);
}
function H1(e, t) {
  return typeof e == "function" ? e(t) : e;
}
function yh() {
  function e(n, r, o, i) {
    const l = {
      [n]: r,
      theme: o
    }, s = i[n];
    if (!s)
      return {
        [n]: r
      };
    const {
      cssProperty: a = n,
      themeKey: u,
      transform: c,
      style: f
    } = s;
    if (r == null)
      return null;
    if (u === "typography" && r === "inherit")
      return {
        [n]: r
      };
    const p = Bl(o, u) || {};
    return f ? f(l) : mt(l, r, (y) => {
      let g = il(p, c, y);
      return y === g && typeof y == "string" && (g = il(p, c, `${n}${y === "default" ? "" : X(y)}`, y)), a === !1 ? g : {
        [a]: g
      };
    });
  }
  function t(n) {
    var r;
    const {
      sx: o,
      theme: i = {},
      nested: l
    } = n || {};
    if (!o)
      return null;
    const s = (r = i.unstable_sxConfig) != null ? r : Bo;
    function a(u) {
      let c = u;
      if (typeof u == "function")
        c = u(i);
      else if (typeof u != "object")
        return u;
      if (!c)
        return null;
      const f = r1(i.breakpoints), p = Object.keys(f);
      let v = f;
      return Object.keys(c).forEach((y) => {
        const g = H1(c[y], i);
        if (g != null)
          if (typeof g == "object")
            if (s[y])
              v = io(v, e(y, g, i, s));
            else {
              const _ = mt({
                theme: i
              }, g, (m) => ({
                [y]: m
              }));
              V1(_, g) ? v[y] = t({
                sx: g,
                theme: i,
                nested: !0
              }) : v = io(v, _);
            }
          else
            v = io(v, e(y, g, i, s));
      }), !l && i.modularCssLayers ? {
        "@layer sx": Gf(p, v)
      } : Gf(p, v);
    }
    return Array.isArray(o) ? o.map(a) : a(o);
  }
  return t;
}
const vh = yh();
vh.filterProps = ["sx"];
const Wo = vh;
function xh(e, t) {
  const n = this;
  return n.vars && typeof n.getColorSchemeSelector == "function" ? {
    [n.getColorSchemeSelector(e).replace(/(\[[^\]]+\])/, "*:where($1)")]: t
  } : n.palette.mode === e ? t : {};
}
const K1 = ["breakpoints", "palette", "spacing", "shape"];
function Uo(e = {}, ...t) {
  const {
    breakpoints: n = {},
    palette: r = {},
    spacing: o,
    shape: i = {}
  } = e, l = W(e, K1), s = mh(n), a = d1(o);
  let u = It({
    breakpoints: s,
    direction: "ltr",
    components: {},
    // Inject component definitions.
    palette: S({
      mode: "light"
    }, r),
    spacing: a,
    shape: S({}, n1, i)
  }, l);
  return u.applyStyles = xh, u = t.reduce((c, f) => It(c, f), u), u.unstable_sxConfig = S({}, Bo, l == null ? void 0 : l.unstable_sxConfig), u.unstable_sx = function(f) {
    return Wo({
      sx: f,
      theme: this
    });
  }, u;
}
const G1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Uo,
  private_createBreakpoints: mh,
  unstable_applyStyles: xh
}, Symbol.toStringTag, { value: "Module" }));
function Q1(e) {
  return Object.keys(e).length === 0;
}
function sc(e = null) {
  const t = C.useContext(Pr);
  return !t || Q1(t) ? e : t;
}
const Y1 = Uo();
function Gl(e = Y1) {
  return sc(e);
}
function Fs(e) {
  const t = ol(e);
  return e !== t && t.styles ? (t.styles.match(/^@layer\s+[^{]*$/) || (t.styles = `@layer global{${t.styles}}`), t) : e;
}
function Sh({
  styles: e,
  themeId: t,
  defaultTheme: n = {}
}) {
  const r = Gl(n), o = t && r[t] || r;
  let i = typeof e == "function" ? e(o) : e;
  return o.modularCssLayers && (Array.isArray(i) ? i = i.map((l) => Fs(typeof l == "function" ? l(o) : l)) : i = Fs(i)), /* @__PURE__ */ $.jsx(fh, {
    styles: i
  });
}
const X1 = ["sx"], Z1 = (e) => {
  var t, n;
  const r = {
    systemProps: {},
    otherProps: {}
  }, o = (t = e == null || (n = e.theme) == null ? void 0 : n.unstable_sxConfig) != null ? t : Bo;
  return Object.keys(e).forEach((i) => {
    o[i] ? r.systemProps[i] = e[i] : r.otherProps[i] = e[i];
  }), r;
};
function Ql(e) {
  const {
    sx: t
  } = e, n = W(e, X1), {
    systemProps: r,
    otherProps: o
  } = Z1(n);
  let i;
  return Array.isArray(t) ? i = [r, ...t] : typeof t == "function" ? i = (...l) => {
    const s = t(...l);
    return Dt(s) ? S({}, r, s) : r;
  } : i = S({}, r, t), S({}, o, {
    sx: i
  });
}
const q1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Wo,
  extendSxProp: Ql,
  unstable_createStyleFunctionSx: yh,
  unstable_defaultSxConfig: Bo
}, Symbol.toStringTag, { value: "Module" })), Yf = (e) => e, J1 = () => {
  let e = Yf;
  return {
    configure(t) {
      e = t;
    },
    generate(t) {
      return e(t);
    },
    reset() {
      e = Yf;
    }
  };
}, ex = J1(), ac = ex;
function wh(e) {
  var t, n, r = "";
  if (typeof e == "string" || typeof e == "number")
    r += e;
  else if (typeof e == "object")
    if (Array.isArray(e)) {
      var o = e.length;
      for (t = 0; t < o; t++)
        e[t] && (n = wh(e[t])) && (r && (r += " "), r += n);
    } else
      for (n in e)
        e[n] && (r && (r += " "), r += n);
  return r;
}
function J() {
  for (var e, t, n = 0, r = "", o = arguments.length; n < o; n++)
    (e = arguments[n]) && (t = wh(e)) && (r && (r += " "), r += t);
  return r;
}
const tx = ["className", "component"];
function nx(e = {}) {
  const {
    themeId: t,
    defaultTheme: n,
    defaultClassName: r = "MuiBox-root",
    generateClassName: o
  } = e, i = nc("div", {
    shouldForwardProp: (s) => s !== "theme" && s !== "sx" && s !== "as"
  })(Wo);
  return /* @__PURE__ */ C.forwardRef(function(a, u) {
    const c = Gl(n), f = Ql(a), {
      className: p,
      component: v = "div"
    } = f, y = W(f, tx);
    return /* @__PURE__ */ $.jsx(i, S({
      as: v,
      ref: u,
      className: J(p, o ? o(r) : r),
      theme: t && c[t] || c
    }, y));
  });
}
const rx = {
  active: "active",
  checked: "checked",
  completed: "completed",
  disabled: "disabled",
  error: "error",
  expanded: "expanded",
  focused: "focused",
  focusVisible: "focusVisible",
  open: "open",
  readOnly: "readOnly",
  required: "required",
  selected: "selected"
};
function Ge(e, t, n = "Mui") {
  const r = rx[t];
  return r ? `${n}-${r}` : `${ac.generate(e)}-${t}`;
}
function Qe(e, t, n = "Mui") {
  const r = {};
  return t.forEach((o) => {
    r[o] = Ge(e, o, n);
  }), r;
}
var kh = { exports: {} }, Q = {};
/**
 * @license React
 * react-is.production.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var uc = Symbol.for("react.transitional.element"), cc = Symbol.for("react.portal"), Yl = Symbol.for("react.fragment"), Xl = Symbol.for("react.strict_mode"), Zl = Symbol.for("react.profiler"), ql = Symbol.for("react.consumer"), Jl = Symbol.for("react.context"), es = Symbol.for("react.forward_ref"), ts = Symbol.for("react.suspense"), ns = Symbol.for("react.suspense_list"), rs = Symbol.for("react.memo"), os = Symbol.for("react.lazy"), ox = Symbol.for("react.view_transition"), ix = Symbol.for("react.client.reference");
function yt(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case uc:
        switch (e = e.type, e) {
          case Yl:
          case Zl:
          case Xl:
          case ts:
          case ns:
          case ox:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Jl:
              case es:
              case os:
              case rs:
                return e;
              case ql:
                return e;
              default:
                return t;
            }
        }
      case cc:
        return t;
    }
  }
}
Q.ContextConsumer = ql;
Q.ContextProvider = Jl;
Q.Element = uc;
Q.ForwardRef = es;
Q.Fragment = Yl;
Q.Lazy = os;
Q.Memo = rs;
Q.Portal = cc;
Q.Profiler = Zl;
Q.StrictMode = Xl;
Q.Suspense = ts;
Q.SuspenseList = ns;
Q.isContextConsumer = function(e) {
  return yt(e) === ql;
};
Q.isContextProvider = function(e) {
  return yt(e) === Jl;
};
Q.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === uc;
};
Q.isForwardRef = function(e) {
  return yt(e) === es;
};
Q.isFragment = function(e) {
  return yt(e) === Yl;
};
Q.isLazy = function(e) {
  return yt(e) === os;
};
Q.isMemo = function(e) {
  return yt(e) === rs;
};
Q.isPortal = function(e) {
  return yt(e) === cc;
};
Q.isProfiler = function(e) {
  return yt(e) === Zl;
};
Q.isStrictMode = function(e) {
  return yt(e) === Xl;
};
Q.isSuspense = function(e) {
  return yt(e) === ts;
};
Q.isSuspenseList = function(e) {
  return yt(e) === ns;
};
Q.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === Yl || e === Zl || e === Xl || e === ts || e === ns || typeof e == "object" && e !== null && (e.$$typeof === os || e.$$typeof === rs || e.$$typeof === Jl || e.$$typeof === ql || e.$$typeof === es || e.$$typeof === ix || e.getModuleId !== void 0);
};
Q.typeOf = yt;
kh.exports = Q;
var Xf = kh.exports;
const lx = /^\s*function(?:\s|\s*\/\*.*\*\/\s*)+([^(\s/]*)\s*/;
function Ch(e) {
  const t = `${e}`.match(lx);
  return t && t[1] || "";
}
function Eh(e, t = "") {
  return e.displayName || e.name || Ch(e) || t;
}
function Zf(e, t, n) {
  const r = Eh(t);
  return e.displayName || (r !== "" ? `${n}(${r})` : n);
}
function sx(e) {
  if (e != null) {
    if (typeof e == "string")
      return e;
    if (typeof e == "function")
      return Eh(e, "Component");
    if (typeof e == "object")
      switch (e.$$typeof) {
        case Xf.ForwardRef:
          return Zf(e, e.render, "ForwardRef");
        case Xf.Memo:
          return Zf(e, e.type, "memo");
        default:
          return;
      }
  }
}
const ax = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: sx,
  getFunctionName: Ch
}, Symbol.toStringTag, { value: "Module" })), ux = ["ownerState"], cx = ["variants"], fx = ["name", "slot", "skipVariantsResolver", "skipSx", "overridesResolver"];
function dx(e) {
  return Object.keys(e).length === 0;
}
function px(e) {
  return typeof e == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  e.charCodeAt(0) > 96;
}
function Bs(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
function qf(e, t) {
  return t && e && typeof e == "object" && e.styles && !e.styles.startsWith("@layer") && (e.styles = `@layer ${t}{${String(e.styles)}}`), e;
}
const mx = Uo(), hx = (e) => e && e.charAt(0).toLowerCase() + e.slice(1);
function pi({
  defaultTheme: e,
  theme: t,
  themeId: n
}) {
  return dx(t) ? e : t[n] || t;
}
function gx(e) {
  return e ? (t, n) => n[e] : null;
}
function Oi(e, t, n) {
  let {
    ownerState: r
  } = t, o = W(t, ux);
  const i = typeof e == "function" ? e(S({
    ownerState: r
  }, o)) : e;
  if (Array.isArray(i))
    return i.flatMap((l) => Oi(l, S({
      ownerState: r
    }, o), n));
  if (i && typeof i == "object" && Array.isArray(i.variants)) {
    const {
      variants: l = []
    } = i;
    let a = W(i, cx);
    return l.forEach((u) => {
      let c = !0;
      if (typeof u.props == "function" ? c = u.props(S({
        ownerState: r
      }, o, r)) : Object.keys(u.props).forEach((f) => {
        (r == null ? void 0 : r[f]) !== u.props[f] && o[f] !== u.props[f] && (c = !1);
      }), c) {
        Array.isArray(a) || (a = [a]);
        const f = typeof u.style == "function" ? u.style(S({
          ownerState: r
        }, o, r)) : u.style;
        a.push(n ? qf(ol(f), n) : f);
      }
    }), a;
  }
  return n ? qf(ol(i), n) : i;
}
function yx(e = {}) {
  const {
    themeId: t,
    defaultTheme: n = mx,
    rootShouldForwardProp: r = Bs,
    slotShouldForwardProp: o = Bs
  } = e, i = (l) => Wo(S({}, l, {
    theme: pi(S({}, l, {
      defaultTheme: n,
      themeId: t
    }))
  }));
  return i.__mui_systemSx = !0, (l, s = {}) => {
    dh(l, (k) => k.filter((w) => !(w != null && w.__mui_systemSx)));
    const {
      name: a,
      slot: u,
      skipVariantsResolver: c,
      skipSx: f,
      // TODO v6: remove `lowercaseFirstLetter()` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      overridesResolver: p = gx(hx(u))
    } = s, v = W(s, fx), y = a && a.startsWith("Mui") || u ? "components" : "custom", g = c !== void 0 ? c : (
      // TODO v6: remove `Root` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      u && u !== "Root" && u !== "root" || !1
    ), _ = f || !1;
    let m, d = Bs;
    u === "Root" || u === "root" ? d = r : u ? d = o : px(l) && (d = void 0);
    const h = nc(l, S({
      shouldForwardProp: d,
      label: m
    }, v)), x = (k) => typeof k == "function" && k.__emotion_real !== k || Dt(k) ? (w) => {
      const T = pi({
        theme: w.theme,
        defaultTheme: n,
        themeId: t
      });
      return Oi(k, S({}, w, {
        theme: T
      }), T.modularCssLayers ? y : void 0);
    } : k, E = (k, ...w) => {
      let T = x(k);
      const N = w ? w.map(x) : [];
      a && p && N.push((A) => {
        const L = pi(S({}, A, {
          defaultTheme: n,
          themeId: t
        }));
        if (!L.components || !L.components[a] || !L.components[a].styleOverrides)
          return null;
        const U = L.components[a].styleOverrides, te = {};
        return Object.entries(U).forEach(([ve, he]) => {
          te[ve] = Oi(he, S({}, A, {
            theme: L
          }), L.modularCssLayers ? "theme" : void 0);
        }), p(A, te);
      }), a && !g && N.push((A) => {
        var L;
        const U = pi(S({}, A, {
          defaultTheme: n,
          themeId: t
        })), te = U == null || (L = U.components) == null || (L = L[a]) == null ? void 0 : L.variants;
        return Oi({
          variants: te
        }, S({}, A, {
          theme: U
        }), U.modularCssLayers ? "theme" : void 0);
      }), _ || N.push(i);
      const O = N.length - w.length;
      if (Array.isArray(k) && O > 0) {
        const A = new Array(O).fill("");
        T = [...k, ...A], T.raw = [...k.raw, ...A];
      }
      const F = h(T, ...N);
      return l.muiName && (F.muiName = l.muiName), F;
    };
    return h.withConfig && (E.withConfig = h.withConfig), E;
  };
}
const vx = yx(), xx = vx;
function ll(e, t) {
  const n = S({}, t);
  return Object.keys(e).forEach((r) => {
    if (r.toString().match(/^(components|slots)$/))
      n[r] = S({}, e[r], n[r]);
    else if (r.toString().match(/^(componentsProps|slotProps)$/)) {
      const o = e[r] || {}, i = t[r];
      n[r] = {}, !i || !Object.keys(i) ? n[r] = o : !o || !Object.keys(o) ? n[r] = i : (n[r] = S({}, i), Object.keys(o).forEach((l) => {
        n[r][l] = ll(o[l], i[l]);
      }));
    } else
      n[r] === void 0 && (n[r] = e[r]);
  }), n;
}
function Sx(e) {
  const {
    theme: t,
    name: n,
    props: r
  } = e;
  return !t || !t.components || !t.components[n] || !t.components[n].defaultProps ? r : ll(t.components[n].defaultProps, r);
}
function wx({
  props: e,
  name: t,
  defaultTheme: n,
  themeId: r
}) {
  let o = Gl(n);
  return r && (o = o[r] || o), Sx({
    theme: o,
    name: t,
    props: e
  });
}
const kx = typeof window < "u" ? C.useLayoutEffect : C.useEffect, fc = kx;
function Cx(e, t = Number.MIN_SAFE_INTEGER, n = Number.MAX_SAFE_INTEGER) {
  return Math.max(t, Math.min(e, n));
}
const Ex = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Cx
}, Symbol.toStringTag, { value: "Module" }));
function _x(...e) {
  return e.reduce((t, n) => n == null ? t : function(...o) {
    t.apply(this, o), n.apply(this, o);
  }, () => {
  });
}
function $x(e, t = 166) {
  let n;
  function r(...o) {
    const i = () => {
      e.apply(this, o);
    };
    clearTimeout(n), n = setTimeout(i, t);
  }
  return r.clear = () => {
    clearTimeout(n);
  }, r;
}
function Px(e, t) {
  return () => null;
}
function Tx(e, t) {
  var n, r;
  return /* @__PURE__ */ C.isValidElement(e) && t.indexOf(
    // For server components `muiName` is avaialble in element.type._payload.value.muiName
    // relevant info - https://github.com/facebook/react/blob/2807d781a08db8e9873687fccc25c0f12b4fb3d4/packages/react/src/ReactLazy.js#L45
    // eslint-disable-next-line no-underscore-dangle
    (n = e.type.muiName) != null ? n : (r = e.type) == null || (r = r._payload) == null || (r = r.value) == null ? void 0 : r.muiName
  ) !== -1;
}
function _h(e) {
  return e && e.ownerDocument || document;
}
function Rx(e) {
  return _h(e).defaultView || window;
}
function Ox(e, t) {
  return () => null;
}
function $h(e, t) {
  typeof e == "function" ? e(t) : e && (e.current = t);
}
let Jf = 0;
function Mx(e) {
  const [t, n] = C.useState(e), r = e || t;
  return C.useEffect(() => {
    t == null && (Jf += 1, n(`mui-${Jf}`));
  }, [t]), r;
}
const ed = Gs["useId".toString()];
function Ph(e) {
  if (ed !== void 0) {
    const t = ed();
    return e ?? t;
  }
  return Mx(e);
}
function Nx(e, t, n, r, o) {
  return null;
}
function zx({
  controlled: e,
  default: t,
  name: n,
  state: r = "value"
}) {
  const {
    current: o
  } = C.useRef(e !== void 0), [i, l] = C.useState(t), s = o ? e : i, a = C.useCallback((u) => {
    o || l(u);
  }, []);
  return [s, a];
}
function Qr(e) {
  const t = C.useRef(e);
  return fc(() => {
    t.current = e;
  }), C.useRef((...n) => (
    // @ts-expect-error hide `this`
    (0, t.current)(...n)
  )).current;
}
function To(...e) {
  return C.useMemo(() => e.every((t) => t == null) ? null : (t) => {
    e.forEach((n) => {
      $h(n, t);
    });
  }, e);
}
const td = {};
function Lx(e, t) {
  const n = C.useRef(td);
  return n.current === td && (n.current = e(t)), n;
}
const jx = [];
function Ix(e) {
  C.useEffect(e, jx);
}
class is {
  constructor() {
    this.currentId = null, this.clear = () => {
      this.currentId !== null && (clearTimeout(this.currentId), this.currentId = null);
    }, this.disposeEffect = () => this.clear;
  }
  static create() {
    return new is();
  }
  /**
   * Executes `fn` after `delay`, clearing any previously scheduled call.
   */
  start(t, n) {
    this.clear(), this.currentId = setTimeout(() => {
      this.currentId = null, n();
    }, t);
  }
}
function Th() {
  const e = Lx(is.create).current;
  return Ix(e.disposeEffect), e;
}
let ls = !0, Ha = !1;
const Ax = new is(), bx = {
  text: !0,
  search: !0,
  url: !0,
  tel: !0,
  email: !0,
  password: !0,
  number: !0,
  date: !0,
  month: !0,
  week: !0,
  time: !0,
  datetime: !0,
  "datetime-local": !0
};
function Dx(e) {
  const {
    type: t,
    tagName: n
  } = e;
  return !!(n === "INPUT" && bx[t] && !e.readOnly || n === "TEXTAREA" && !e.readOnly || e.isContentEditable);
}
function Fx(e) {
  e.metaKey || e.altKey || e.ctrlKey || (ls = !0);
}
function Ws() {
  ls = !1;
}
function Bx() {
  this.visibilityState === "hidden" && Ha && (ls = !0);
}
function Wx(e) {
  e.addEventListener("keydown", Fx, !0), e.addEventListener("mousedown", Ws, !0), e.addEventListener("pointerdown", Ws, !0), e.addEventListener("touchstart", Ws, !0), e.addEventListener("visibilitychange", Bx, !0);
}
function Ux(e) {
  const {
    target: t
  } = e;
  try {
    return t.matches(":focus-visible");
  } catch {
  }
  return ls || Dx(t);
}
function Rh() {
  const e = C.useCallback((o) => {
    o != null && Wx(o.ownerDocument);
  }, []), t = C.useRef(!1);
  function n() {
    return t.current ? (Ha = !0, Ax.start(100, () => {
      Ha = !1;
    }), t.current = !1, !0) : !1;
  }
  function r(o) {
    return Ux(o) ? (t.current = !0, !0) : !1;
  }
  return {
    isFocusVisibleRef: t,
    onFocus: r,
    onBlur: n,
    ref: e
  };
}
function ot(e, t, n = void 0) {
  const r = {};
  return Object.keys(e).forEach(
    // `Object.keys(slots)` can't be wider than `T` because we infer `T` from `slots`.
    // @ts-expect-error https://github.com/microsoft/TypeScript/pull/12253#issuecomment-263132208
    (o) => {
      r[o] = e[o].reduce((i, l) => {
        if (l) {
          const s = t(l);
          s !== "" && i.push(s), n && n[l] && i.push(n[l]);
        }
        return i;
      }, []).join(" ");
    }
  ), r;
}
function Vx(e) {
  return typeof e == "string";
}
function Hx(e, t, n) {
  return e === void 0 || Vx(e) ? t : S({}, t, {
    ownerState: S({}, t.ownerState, n)
  });
}
function Kx(e, t = []) {
  if (e === void 0)
    return {};
  const n = {};
  return Object.keys(e).filter((r) => r.match(/^on[A-Z]/) && typeof e[r] == "function" && !t.includes(r)).forEach((r) => {
    n[r] = e[r];
  }), n;
}
function nd(e) {
  if (e === void 0)
    return {};
  const t = {};
  return Object.keys(e).filter((n) => !(n.match(/^on[A-Z]/) && typeof e[n] == "function")).forEach((n) => {
    t[n] = e[n];
  }), t;
}
function Gx(e) {
  const {
    getSlotProps: t,
    additionalProps: n,
    externalSlotProps: r,
    externalForwardedProps: o,
    className: i
  } = e;
  if (!t) {
    const v = J(n == null ? void 0 : n.className, i, o == null ? void 0 : o.className, r == null ? void 0 : r.className), y = S({}, n == null ? void 0 : n.style, o == null ? void 0 : o.style, r == null ? void 0 : r.style), g = S({}, n, o, r);
    return v.length > 0 && (g.className = v), Object.keys(y).length > 0 && (g.style = y), {
      props: g,
      internalRef: void 0
    };
  }
  const l = Kx(S({}, o, r)), s = nd(r), a = nd(o), u = t(l), c = J(u == null ? void 0 : u.className, n == null ? void 0 : n.className, i, o == null ? void 0 : o.className, r == null ? void 0 : r.className), f = S({}, u == null ? void 0 : u.style, n == null ? void 0 : n.style, o == null ? void 0 : o.style, r == null ? void 0 : r.style), p = S({}, u, n, a, s);
  return c.length > 0 && (p.className = c), Object.keys(f).length > 0 && (p.style = f), {
    props: p,
    internalRef: u.ref
  };
}
function Qx(e, t, n) {
  return typeof e == "function" ? e(t, n) : e;
}
const Yx = /* @__PURE__ */ C.createContext(null), Oh = Yx;
function Mh() {
  return C.useContext(Oh);
}
const Xx = typeof Symbol == "function" && Symbol.for, Zx = Xx ? Symbol.for("mui.nested") : "__THEME_NESTED__";
function qx(e, t) {
  return typeof t == "function" ? t(e) : S({}, e, t);
}
function Jx(e) {
  const {
    children: t,
    theme: n
  } = e, r = Mh(), o = C.useMemo(() => {
    const i = r === null ? n : qx(r, n);
    return i != null && (i[Zx] = r !== null), i;
  }, [n, r]);
  return /* @__PURE__ */ $.jsx(Oh.Provider, {
    value: o,
    children: t
  });
}
const eS = ["value"], tS = /* @__PURE__ */ C.createContext();
function nS(e) {
  let {
    value: t
  } = e, n = W(e, eS);
  return /* @__PURE__ */ $.jsx(tS.Provider, S({
    value: t ?? !0
  }, n));
}
const Nh = /* @__PURE__ */ C.createContext(void 0);
function rS({
  value: e,
  children: t
}) {
  return /* @__PURE__ */ $.jsx(Nh.Provider, {
    value: e,
    children: t
  });
}
function oS(e) {
  const {
    theme: t,
    name: n,
    props: r
  } = e;
  if (!t || !t.components || !t.components[n])
    return r;
  const o = t.components[n];
  return o.defaultProps ? ll(o.defaultProps, r) : !o.styleOverrides && !o.variants ? ll(o, r) : r;
}
function iS({
  props: e,
  name: t
}) {
  const n = C.useContext(Nh);
  return oS({
    props: e,
    name: t,
    theme: {
      components: n
    }
  });
}
function lS(e) {
  const t = sc(), n = Ph() || "", {
    modularCssLayers: r
  } = e;
  let o = "mui.global, mui.components, mui.theme, mui.custom, mui.sx";
  return !r || t !== null ? o = "" : typeof r == "string" ? o = r.replace(/mui(?!\.)/g, o) : o = `@layer ${o};`, fc(() => {
    const i = document.querySelector("head");
    if (!i)
      return;
    const l = i.firstChild;
    if (o) {
      var s;
      if (l && (s = l.hasAttribute) != null && s.call(l, "data-mui-layer-order") && l.getAttribute("data-mui-layer-order") === n)
        return;
      const u = document.createElement("style");
      u.setAttribute("data-mui-layer-order", n), u.textContent = o, i.prepend(u);
    } else {
      var a;
      (a = i.querySelector(`style[data-mui-layer-order="${n}"]`)) == null || a.remove();
    }
  }, [o, n]), o ? /* @__PURE__ */ $.jsx(Sh, {
    styles: o
  }) : null;
}
const rd = {};
function od(e, t, n, r = !1) {
  return C.useMemo(() => {
    const o = e && t[e] || t;
    if (typeof n == "function") {
      const i = n(o), l = e ? S({}, t, {
        [e]: i
      }) : i;
      return r ? () => l : l;
    }
    return e ? S({}, t, {
      [e]: n
    }) : S({}, t, n);
  }, [e, t, n, r]);
}
function sS(e) {
  const {
    children: t,
    theme: n,
    themeId: r
  } = e, o = sc(rd), i = Mh() || rd, l = od(r, o, n), s = od(r, i, n, !0), a = l.direction === "rtl", u = lS(l);
  return /* @__PURE__ */ $.jsx(Jx, {
    theme: s,
    children: /* @__PURE__ */ $.jsx(Pr.Provider, {
      value: l,
      children: /* @__PURE__ */ $.jsx(nS, {
        value: a,
        children: /* @__PURE__ */ $.jsxs(rS, {
          value: l == null ? void 0 : l.components,
          children: [u, t]
        })
      })
    })
  });
}
const aS = ["className", "component", "disableGutters", "fixed", "maxWidth", "classes"], uS = Uo(), cS = xx("div", {
  name: "MuiContainer",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[`maxWidth${X(String(n.maxWidth))}`], n.fixed && t.fixed, n.disableGutters && t.disableGutters];
  }
}), fS = (e) => wx({
  props: e,
  name: "MuiContainer",
  defaultTheme: uS
}), dS = (e, t) => {
  const n = (a) => Ge(t, a), {
    classes: r,
    fixed: o,
    disableGutters: i,
    maxWidth: l
  } = e, s = {
    root: ["root", l && `maxWidth${X(String(l))}`, o && "fixed", i && "disableGutters"]
  };
  return ot(s, n, r);
};
function pS(e = {}) {
  const {
    // This will allow adding custom styled fn (for example for custom sx style function)
    createStyledComponent: t = cS,
    useThemeProps: n = fS,
    componentName: r = "MuiContainer"
  } = e, o = t(({
    theme: l,
    ownerState: s
  }) => S({
    width: "100%",
    marginLeft: "auto",
    boxSizing: "border-box",
    marginRight: "auto",
    display: "block"
  }, !s.disableGutters && {
    paddingLeft: l.spacing(2),
    paddingRight: l.spacing(2),
    // @ts-ignore module augmentation fails if custom breakpoints are used
    [l.breakpoints.up("sm")]: {
      paddingLeft: l.spacing(3),
      paddingRight: l.spacing(3)
    }
  }), ({
    theme: l,
    ownerState: s
  }) => s.fixed && Object.keys(l.breakpoints.values).reduce((a, u) => {
    const c = u, f = l.breakpoints.values[c];
    return f !== 0 && (a[l.breakpoints.up(c)] = {
      maxWidth: `${f}${l.breakpoints.unit}`
    }), a;
  }, {}), ({
    theme: l,
    ownerState: s
  }) => S({}, s.maxWidth === "xs" && {
    // @ts-ignore module augmentation fails if custom breakpoints are used
    [l.breakpoints.up("xs")]: {
      // @ts-ignore module augmentation fails if custom breakpoints are used
      maxWidth: Math.max(l.breakpoints.values.xs, 444)
    }
  }, s.maxWidth && // @ts-ignore module augmentation fails if custom breakpoints are used
  s.maxWidth !== "xs" && {
    // @ts-ignore module augmentation fails if custom breakpoints are used
    [l.breakpoints.up(s.maxWidth)]: {
      // @ts-ignore module augmentation fails if custom breakpoints are used
      maxWidth: `${l.breakpoints.values[s.maxWidth]}${l.breakpoints.unit}`
    }
  }));
  return /* @__PURE__ */ C.forwardRef(function(s, a) {
    const u = n(s), {
      className: c,
      component: f = "div",
      disableGutters: p = !1,
      fixed: v = !1,
      maxWidth: y = "lg"
    } = u, g = W(u, aS), _ = S({}, u, {
      component: f,
      disableGutters: p,
      fixed: v,
      maxWidth: y
    }), m = dS(_, r);
    return (
      // @ts-ignore theme is injected by the styled util
      /* @__PURE__ */ $.jsx(o, S({
        as: f,
        ownerState: _,
        className: J(m.root, c),
        ref: a
      }, g))
    );
  });
}
function mS(e, t) {
  return S({
    toolbar: {
      minHeight: 56,
      [e.up("xs")]: {
        "@media (orientation: landscape)": {
          minHeight: 48
        }
      },
      [e.up("sm")]: {
        minHeight: 64
      }
    }
  }, t);
}
var me = {}, zh = { exports: {} };
(function(e) {
  function t(n) {
    return n && n.__esModule ? n : {
      default: n
    };
  }
  e.exports = t, e.exports.__esModule = !0, e.exports.default = e.exports;
})(zh);
var dc = zh.exports;
const hS = /* @__PURE__ */ Gt(Fy), gS = /* @__PURE__ */ Gt(Ex);
var Lh = dc;
Object.defineProperty(me, "__esModule", {
  value: !0
});
var Ro = me.alpha = bh;
me.blend = PS;
me.colorChannel = void 0;
var Ka = me.darken = mc;
me.decomposeColor = ht;
me.emphasize = Dh;
var yS = me.getContrastRatio = kS;
me.getLuminance = sl;
me.hexToRgb = jh;
me.hslToRgb = Ah;
var Ga = me.lighten = hc;
me.private_safeAlpha = CS;
me.private_safeColorChannel = void 0;
me.private_safeDarken = ES;
me.private_safeEmphasize = $S;
me.private_safeLighten = _S;
me.recomposeColor = Rr;
me.rgbToHex = wS;
var id = Lh(hS), vS = Lh(gS);
function pc(e, t = 0, n = 1) {
  return (0, vS.default)(e, t, n);
}
function jh(e) {
  e = e.slice(1);
  const t = new RegExp(`.{1,${e.length >= 6 ? 2 : 1}}`, "g");
  let n = e.match(t);
  return n && n[0].length === 1 && (n = n.map((r) => r + r)), n ? `rgb${n.length === 4 ? "a" : ""}(${n.map((r, o) => o < 3 ? parseInt(r, 16) : Math.round(parseInt(r, 16) / 255 * 1e3) / 1e3).join(", ")})` : "";
}
function xS(e) {
  const t = e.toString(16);
  return t.length === 1 ? `0${t}` : t;
}
function ht(e) {
  if (e.type)
    return e;
  if (e.charAt(0) === "#")
    return ht(jh(e));
  const t = e.indexOf("("), n = e.substring(0, t);
  if (["rgb", "rgba", "hsl", "hsla", "color"].indexOf(n) === -1)
    throw new Error((0, id.default)(9, e));
  let r = e.substring(t + 1, e.length - 1), o;
  if (n === "color") {
    if (r = r.split(" "), o = r.shift(), r.length === 4 && r[3].charAt(0) === "/" && (r[3] = r[3].slice(1)), ["srgb", "display-p3", "a98-rgb", "prophoto-rgb", "rec-2020"].indexOf(o) === -1)
      throw new Error((0, id.default)(10, o));
  } else
    r = r.split(",");
  return r = r.map((i) => parseFloat(i)), {
    type: n,
    values: r,
    colorSpace: o
  };
}
const Ih = (e) => {
  const t = ht(e);
  return t.values.slice(0, 3).map((n, r) => t.type.indexOf("hsl") !== -1 && r !== 0 ? `${n}%` : n).join(" ");
};
me.colorChannel = Ih;
const SS = (e, t) => {
  try {
    return Ih(e);
  } catch {
    return e;
  }
};
me.private_safeColorChannel = SS;
function Rr(e) {
  const {
    type: t,
    colorSpace: n
  } = e;
  let {
    values: r
  } = e;
  return t.indexOf("rgb") !== -1 ? r = r.map((o, i) => i < 3 ? parseInt(o, 10) : o) : t.indexOf("hsl") !== -1 && (r[1] = `${r[1]}%`, r[2] = `${r[2]}%`), t.indexOf("color") !== -1 ? r = `${n} ${r.join(" ")}` : r = `${r.join(", ")}`, `${t}(${r})`;
}
function wS(e) {
  if (e.indexOf("#") === 0)
    return e;
  const {
    values: t
  } = ht(e);
  return `#${t.map((n, r) => xS(r === 3 ? Math.round(255 * n) : n)).join("")}`;
}
function Ah(e) {
  e = ht(e);
  const {
    values: t
  } = e, n = t[0], r = t[1] / 100, o = t[2] / 100, i = r * Math.min(o, 1 - o), l = (u, c = (u + n / 30) % 12) => o - i * Math.max(Math.min(c - 3, 9 - c, 1), -1);
  let s = "rgb";
  const a = [Math.round(l(0) * 255), Math.round(l(8) * 255), Math.round(l(4) * 255)];
  return e.type === "hsla" && (s += "a", a.push(t[3])), Rr({
    type: s,
    values: a
  });
}
function sl(e) {
  e = ht(e);
  let t = e.type === "hsl" || e.type === "hsla" ? ht(Ah(e)).values : e.values;
  return t = t.map((n) => (e.type !== "color" && (n /= 255), n <= 0.03928 ? n / 12.92 : ((n + 0.055) / 1.055) ** 2.4)), Number((0.2126 * t[0] + 0.7152 * t[1] + 0.0722 * t[2]).toFixed(3));
}
function kS(e, t) {
  const n = sl(e), r = sl(t);
  return (Math.max(n, r) + 0.05) / (Math.min(n, r) + 0.05);
}
function bh(e, t) {
  return e = ht(e), t = pc(t), (e.type === "rgb" || e.type === "hsl") && (e.type += "a"), e.type === "color" ? e.values[3] = `/${t}` : e.values[3] = t, Rr(e);
}
function CS(e, t, n) {
  try {
    return bh(e, t);
  } catch {
    return e;
  }
}
function mc(e, t) {
  if (e = ht(e), t = pc(t), e.type.indexOf("hsl") !== -1)
    e.values[2] *= 1 - t;
  else if (e.type.indexOf("rgb") !== -1 || e.type.indexOf("color") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] *= 1 - t;
  return Rr(e);
}
function ES(e, t, n) {
  try {
    return mc(e, t);
  } catch {
    return e;
  }
}
function hc(e, t) {
  if (e = ht(e), t = pc(t), e.type.indexOf("hsl") !== -1)
    e.values[2] += (100 - e.values[2]) * t;
  else if (e.type.indexOf("rgb") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] += (255 - e.values[n]) * t;
  else if (e.type.indexOf("color") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] += (1 - e.values[n]) * t;
  return Rr(e);
}
function _S(e, t, n) {
  try {
    return hc(e, t);
  } catch {
    return e;
  }
}
function Dh(e, t = 0.15) {
  return sl(e) > 0.5 ? mc(e, t) : hc(e, t);
}
function $S(e, t, n) {
  try {
    return Dh(e, t);
  } catch {
    return e;
  }
}
function PS(e, t, n, r = 1) {
  const o = (a, u) => Math.round((a ** (1 / r) * (1 - n) + u ** (1 / r) * n) ** r), i = ht(e), l = ht(t), s = [o(i.values[0], l.values[0]), o(i.values[1], l.values[1]), o(i.values[2], l.values[2])];
  return Rr({
    type: "rgb",
    values: s
  });
}
const TS = {
  black: "#000",
  white: "#fff"
}, Oo = TS, RS = {
  50: "#fafafa",
  100: "#f5f5f5",
  200: "#eeeeee",
  300: "#e0e0e0",
  400: "#bdbdbd",
  500: "#9e9e9e",
  600: "#757575",
  700: "#616161",
  800: "#424242",
  900: "#212121",
  A100: "#f5f5f5",
  A200: "#eeeeee",
  A400: "#bdbdbd",
  A700: "#616161"
}, OS = RS, MS = {
  50: "#f3e5f5",
  100: "#e1bee7",
  200: "#ce93d8",
  300: "#ba68c8",
  400: "#ab47bc",
  500: "#9c27b0",
  600: "#8e24aa",
  700: "#7b1fa2",
  800: "#6a1b9a",
  900: "#4a148c",
  A100: "#ea80fc",
  A200: "#e040fb",
  A400: "#d500f9",
  A700: "#aa00ff"
}, Fn = MS, NS = {
  50: "#ffebee",
  100: "#ffcdd2",
  200: "#ef9a9a",
  300: "#e57373",
  400: "#ef5350",
  500: "#f44336",
  600: "#e53935",
  700: "#d32f2f",
  800: "#c62828",
  900: "#b71c1c",
  A100: "#ff8a80",
  A200: "#ff5252",
  A400: "#ff1744",
  A700: "#d50000"
}, Bn = NS, zS = {
  50: "#fff3e0",
  100: "#ffe0b2",
  200: "#ffcc80",
  300: "#ffb74d",
  400: "#ffa726",
  500: "#ff9800",
  600: "#fb8c00",
  700: "#f57c00",
  800: "#ef6c00",
  900: "#e65100",
  A100: "#ffd180",
  A200: "#ffab40",
  A400: "#ff9100",
  A700: "#ff6d00"
}, Wr = zS, LS = {
  50: "#e3f2fd",
  100: "#bbdefb",
  200: "#90caf9",
  300: "#64b5f6",
  400: "#42a5f5",
  500: "#2196f3",
  600: "#1e88e5",
  700: "#1976d2",
  800: "#1565c0",
  900: "#0d47a1",
  A100: "#82b1ff",
  A200: "#448aff",
  A400: "#2979ff",
  A700: "#2962ff"
}, Wn = LS, jS = {
  50: "#e1f5fe",
  100: "#b3e5fc",
  200: "#81d4fa",
  300: "#4fc3f7",
  400: "#29b6f6",
  500: "#03a9f4",
  600: "#039be5",
  700: "#0288d1",
  800: "#0277bd",
  900: "#01579b",
  A100: "#80d8ff",
  A200: "#40c4ff",
  A400: "#00b0ff",
  A700: "#0091ea"
}, Un = jS, IS = {
  50: "#e8f5e9",
  100: "#c8e6c9",
  200: "#a5d6a7",
  300: "#81c784",
  400: "#66bb6a",
  500: "#4caf50",
  600: "#43a047",
  700: "#388e3c",
  800: "#2e7d32",
  900: "#1b5e20",
  A100: "#b9f6ca",
  A200: "#69f0ae",
  A400: "#00e676",
  A700: "#00c853"
}, Vn = IS, AS = ["mode", "contrastThreshold", "tonalOffset"], ld = {
  // The colors used to style the text.
  text: {
    // The most important text.
    primary: "rgba(0, 0, 0, 0.87)",
    // Secondary text.
    secondary: "rgba(0, 0, 0, 0.6)",
    // Disabled text have even lower visual prominence.
    disabled: "rgba(0, 0, 0, 0.38)"
  },
  // The color used to divide different elements.
  divider: "rgba(0, 0, 0, 0.12)",
  // The background colors used to style the surfaces.
  // Consistency between these values is important.
  background: {
    paper: Oo.white,
    default: Oo.white
  },
  // The colors used to style the action elements.
  action: {
    // The color of an active action like an icon button.
    active: "rgba(0, 0, 0, 0.54)",
    // The color of an hovered action.
    hover: "rgba(0, 0, 0, 0.04)",
    hoverOpacity: 0.04,
    // The color of a selected action.
    selected: "rgba(0, 0, 0, 0.08)",
    selectedOpacity: 0.08,
    // The color of a disabled action.
    disabled: "rgba(0, 0, 0, 0.26)",
    // The background color of a disabled action.
    disabledBackground: "rgba(0, 0, 0, 0.12)",
    disabledOpacity: 0.38,
    focus: "rgba(0, 0, 0, 0.12)",
    focusOpacity: 0.12,
    activatedOpacity: 0.12
  }
}, Us = {
  text: {
    primary: Oo.white,
    secondary: "rgba(255, 255, 255, 0.7)",
    disabled: "rgba(255, 255, 255, 0.5)",
    icon: "rgba(255, 255, 255, 0.5)"
  },
  divider: "rgba(255, 255, 255, 0.12)",
  background: {
    paper: "#121212",
    default: "#121212"
  },
  action: {
    active: Oo.white,
    hover: "rgba(255, 255, 255, 0.08)",
    hoverOpacity: 0.08,
    selected: "rgba(255, 255, 255, 0.16)",
    selectedOpacity: 0.16,
    disabled: "rgba(255, 255, 255, 0.3)",
    disabledBackground: "rgba(255, 255, 255, 0.12)",
    disabledOpacity: 0.38,
    focus: "rgba(255, 255, 255, 0.12)",
    focusOpacity: 0.12,
    activatedOpacity: 0.24
  }
};
function sd(e, t, n, r) {
  const o = r.light || r, i = r.dark || r * 1.5;
  e[t] || (e.hasOwnProperty(n) ? e[t] = e[n] : t === "light" ? e.light = Ga(e.main, o) : t === "dark" && (e.dark = Ka(e.main, i)));
}
function bS(e = "light") {
  return e === "dark" ? {
    main: Wn[200],
    light: Wn[50],
    dark: Wn[400]
  } : {
    main: Wn[700],
    light: Wn[400],
    dark: Wn[800]
  };
}
function DS(e = "light") {
  return e === "dark" ? {
    main: Fn[200],
    light: Fn[50],
    dark: Fn[400]
  } : {
    main: Fn[500],
    light: Fn[300],
    dark: Fn[700]
  };
}
function FS(e = "light") {
  return e === "dark" ? {
    main: Bn[500],
    light: Bn[300],
    dark: Bn[700]
  } : {
    main: Bn[700],
    light: Bn[400],
    dark: Bn[800]
  };
}
function BS(e = "light") {
  return e === "dark" ? {
    main: Un[400],
    light: Un[300],
    dark: Un[700]
  } : {
    main: Un[700],
    light: Un[500],
    dark: Un[900]
  };
}
function WS(e = "light") {
  return e === "dark" ? {
    main: Vn[400],
    light: Vn[300],
    dark: Vn[700]
  } : {
    main: Vn[800],
    light: Vn[500],
    dark: Vn[900]
  };
}
function US(e = "light") {
  return e === "dark" ? {
    main: Wr[400],
    light: Wr[300],
    dark: Wr[700]
  } : {
    main: "#ed6c02",
    // closest to orange[800] that pass 3:1.
    light: Wr[500],
    dark: Wr[900]
  };
}
function VS(e) {
  const {
    mode: t = "light",
    contrastThreshold: n = 3,
    tonalOffset: r = 0.2
  } = e, o = W(e, AS), i = e.primary || bS(t), l = e.secondary || DS(t), s = e.error || FS(t), a = e.info || BS(t), u = e.success || WS(t), c = e.warning || US(t);
  function f(g) {
    return yS(g, Us.text.primary) >= n ? Us.text.primary : ld.text.primary;
  }
  const p = ({
    color: g,
    name: _,
    mainShade: m = 500,
    lightShade: d = 300,
    darkShade: h = 700
  }) => {
    if (g = S({}, g), !g.main && g[m] && (g.main = g[m]), !g.hasOwnProperty("main"))
      throw new Error(Eo(11, _ ? ` (${_})` : "", m));
    if (typeof g.main != "string")
      throw new Error(Eo(12, _ ? ` (${_})` : "", JSON.stringify(g.main)));
    return sd(g, "light", d, r), sd(g, "dark", h, r), g.contrastText || (g.contrastText = f(g.main)), g;
  }, v = {
    dark: Us,
    light: ld
  };
  return It(S({
    // A collection of common colors.
    common: S({}, Oo),
    // prevent mutable object.
    // The palette mode, can be light or dark.
    mode: t,
    // The colors used to represent primary interface elements for a user.
    primary: p({
      color: i,
      name: "primary"
    }),
    // The colors used to represent secondary interface elements for a user.
    secondary: p({
      color: l,
      name: "secondary",
      mainShade: "A400",
      lightShade: "A200",
      darkShade: "A700"
    }),
    // The colors used to represent interface elements that the user should be made aware of.
    error: p({
      color: s,
      name: "error"
    }),
    // The colors used to represent potentially dangerous actions or important messages.
    warning: p({
      color: c,
      name: "warning"
    }),
    // The colors used to present information to the user that is neutral and not necessarily important.
    info: p({
      color: a,
      name: "info"
    }),
    // The colors used to indicate the successful completion of an action that user triggered.
    success: p({
      color: u,
      name: "success"
    }),
    // The grey colors.
    grey: OS,
    // Used by `getContrastText()` to maximize the contrast between
    // the background and the text.
    contrastThreshold: n,
    // Takes a background color and returns the text color that maximizes the contrast.
    getContrastText: f,
    // Generate a rich color object.
    augmentColor: p,
    // Used by the functions below to shift a color's luminance by approximately
    // two indexes within its tonal palette.
    // E.g., shift from Red 500 to Red 300 or Red 700.
    tonalOffset: r
  }, v[t]), o);
}
const HS = ["fontFamily", "fontSize", "fontWeightLight", "fontWeightRegular", "fontWeightMedium", "fontWeightBold", "htmlFontSize", "allVariants", "pxToRem"];
function KS(e) {
  return Math.round(e * 1e5) / 1e5;
}
const ad = {
  textTransform: "uppercase"
}, ud = '"Roboto", "Helvetica", "Arial", sans-serif';
function GS(e, t) {
  const n = typeof t == "function" ? t(e) : t, {
    fontFamily: r = ud,
    // The default font size of the Material Specification.
    fontSize: o = 14,
    // px
    fontWeightLight: i = 300,
    fontWeightRegular: l = 400,
    fontWeightMedium: s = 500,
    fontWeightBold: a = 700,
    // Tell MUI what's the font-size on the html element.
    // 16px is the default font-size used by browsers.
    htmlFontSize: u = 16,
    // Apply the CSS properties to all the variants.
    allVariants: c,
    pxToRem: f
  } = n, p = W(n, HS), v = o / 14, y = f || ((m) => `${m / u * v}rem`), g = (m, d, h, x, E) => S({
    fontFamily: r,
    fontWeight: m,
    fontSize: y(d),
    // Unitless following https://meyerweb.com/eric/thoughts/2006/02/08/unitless-line-heights/
    lineHeight: h
  }, r === ud ? {
    letterSpacing: `${KS(x / d)}em`
  } : {}, E, c), _ = {
    h1: g(i, 96, 1.167, -1.5),
    h2: g(i, 60, 1.2, -0.5),
    h3: g(l, 48, 1.167, 0),
    h4: g(l, 34, 1.235, 0.25),
    h5: g(l, 24, 1.334, 0),
    h6: g(s, 20, 1.6, 0.15),
    subtitle1: g(l, 16, 1.75, 0.15),
    subtitle2: g(s, 14, 1.57, 0.1),
    body1: g(l, 16, 1.5, 0.15),
    body2: g(l, 14, 1.43, 0.15),
    button: g(s, 14, 1.75, 0.4, ad),
    caption: g(l, 12, 1.66, 0.4),
    overline: g(l, 12, 2.66, 1, ad),
    // TODO v6: Remove handling of 'inherit' variant from the theme as it is already handled in Material UI's Typography component. Also, remember to remove the associated types.
    inherit: {
      fontFamily: "inherit",
      fontWeight: "inherit",
      fontSize: "inherit",
      lineHeight: "inherit",
      letterSpacing: "inherit"
    }
  };
  return It(S({
    htmlFontSize: u,
    pxToRem: y,
    fontFamily: r,
    fontSize: o,
    fontWeightLight: i,
    fontWeightRegular: l,
    fontWeightMedium: s,
    fontWeightBold: a
  }, _), p, {
    clone: !1
    // No need to clone deep
  });
}
const QS = 0.2, YS = 0.14, XS = 0.12;
function ne(...e) {
  return [`${e[0]}px ${e[1]}px ${e[2]}px ${e[3]}px rgba(0,0,0,${QS})`, `${e[4]}px ${e[5]}px ${e[6]}px ${e[7]}px rgba(0,0,0,${YS})`, `${e[8]}px ${e[9]}px ${e[10]}px ${e[11]}px rgba(0,0,0,${XS})`].join(",");
}
const ZS = ["none", ne(0, 2, 1, -1, 0, 1, 1, 0, 0, 1, 3, 0), ne(0, 3, 1, -2, 0, 2, 2, 0, 0, 1, 5, 0), ne(0, 3, 3, -2, 0, 3, 4, 0, 0, 1, 8, 0), ne(0, 2, 4, -1, 0, 4, 5, 0, 0, 1, 10, 0), ne(0, 3, 5, -1, 0, 5, 8, 0, 0, 1, 14, 0), ne(0, 3, 5, -1, 0, 6, 10, 0, 0, 1, 18, 0), ne(0, 4, 5, -2, 0, 7, 10, 1, 0, 2, 16, 1), ne(0, 5, 5, -3, 0, 8, 10, 1, 0, 3, 14, 2), ne(0, 5, 6, -3, 0, 9, 12, 1, 0, 3, 16, 2), ne(0, 6, 6, -3, 0, 10, 14, 1, 0, 4, 18, 3), ne(0, 6, 7, -4, 0, 11, 15, 1, 0, 4, 20, 3), ne(0, 7, 8, -4, 0, 12, 17, 2, 0, 5, 22, 4), ne(0, 7, 8, -4, 0, 13, 19, 2, 0, 5, 24, 4), ne(0, 7, 9, -4, 0, 14, 21, 2, 0, 5, 26, 4), ne(0, 8, 9, -5, 0, 15, 22, 2, 0, 6, 28, 5), ne(0, 8, 10, -5, 0, 16, 24, 2, 0, 6, 30, 5), ne(0, 8, 11, -5, 0, 17, 26, 2, 0, 6, 32, 5), ne(0, 9, 11, -5, 0, 18, 28, 2, 0, 7, 34, 6), ne(0, 9, 12, -6, 0, 19, 29, 2, 0, 7, 36, 6), ne(0, 10, 13, -6, 0, 20, 31, 3, 0, 8, 38, 7), ne(0, 10, 13, -6, 0, 21, 33, 3, 0, 8, 40, 7), ne(0, 10, 14, -6, 0, 22, 35, 3, 0, 8, 42, 7), ne(0, 11, 14, -7, 0, 23, 36, 3, 0, 9, 44, 8), ne(0, 11, 15, -7, 0, 24, 38, 3, 0, 9, 46, 8)], qS = ZS, JS = ["duration", "easing", "delay"], ew = {
  // This is the most common easing curve.
  easeInOut: "cubic-bezier(0.4, 0, 0.2, 1)",
  // Objects enter the screen at full velocity from off-screen and
  // slowly decelerate to a resting point.
  easeOut: "cubic-bezier(0.0, 0, 0.2, 1)",
  // Objects leave the screen at full velocity. They do not decelerate when off-screen.
  easeIn: "cubic-bezier(0.4, 0, 1, 1)",
  // The sharp curve is used by objects that may return to the screen at any time.
  sharp: "cubic-bezier(0.4, 0, 0.6, 1)"
}, Fh = {
  shortest: 150,
  shorter: 200,
  short: 250,
  // most basic recommended timing
  standard: 300,
  // this is to be used in complex animations
  complex: 375,
  // recommended when something is entering screen
  enteringScreen: 225,
  // recommended when something is leaving screen
  leavingScreen: 195
};
function cd(e) {
  return `${Math.round(e)}ms`;
}
function tw(e) {
  if (!e)
    return 0;
  const t = e / 36;
  return Math.round((4 + 15 * t ** 0.25 + t / 5) * 10);
}
function nw(e) {
  const t = S({}, ew, e.easing), n = S({}, Fh, e.duration);
  return S({
    getAutoHeightDuration: tw,
    create: (o = ["all"], i = {}) => {
      const {
        duration: l = n.standard,
        easing: s = t.easeInOut,
        delay: a = 0
      } = i;
      return W(i, JS), (Array.isArray(o) ? o : [o]).map((u) => `${u} ${typeof l == "string" ? l : cd(l)} ${s} ${typeof a == "string" ? a : cd(a)}`).join(",");
    }
  }, e, {
    easing: t,
    duration: n
  });
}
const rw = {
  mobileStepper: 1e3,
  fab: 1050,
  speedDial: 1050,
  appBar: 1100,
  drawer: 1200,
  modal: 1300,
  snackbar: 1400,
  tooltip: 1500
}, ow = rw, iw = ["breakpoints", "mixins", "spacing", "palette", "transitions", "typography", "shape"];
function gc(e = {}, ...t) {
  const {
    mixins: n = {},
    palette: r = {},
    transitions: o = {},
    typography: i = {}
  } = e, l = W(e, iw);
  if (e.vars && // The error should throw only for the root theme creation because user is not allowed to use a custom node `vars`.
  // `generateCssVars` is the closest identifier for checking that the `options` is a result of `extendTheme` with CSS variables so that user can create new theme for nested ThemeProvider.
  e.generateCssVars === void 0)
    throw new Error(Eo(18));
  const s = VS(r), a = Uo(e);
  let u = It(a, {
    mixins: mS(a.breakpoints, n),
    palette: s,
    // Don't use [...shadows] until you've verified its transpiled code is not invoking the iterator protocol.
    shadows: qS.slice(),
    typography: GS(s, i),
    transitions: nw(o),
    zIndex: S({}, ow)
  });
  return u = It(u, l), u = t.reduce((c, f) => It(c, f), u), u.unstable_sxConfig = S({}, Bo, l == null ? void 0 : l.unstable_sxConfig), u.unstable_sx = function(f) {
    return Wo({
      sx: f,
      theme: this
    });
  }, u;
}
const lw = gc(), yc = lw;
function Bh() {
  const e = Gl(yc);
  return e[wr] || e;
}
var Vo = {}, Vs = { exports: {} }, fd;
function sw() {
  return fd || (fd = 1, function(e) {
    function t(n, r) {
      if (n == null)
        return {};
      var o = {};
      for (var i in n)
        if ({}.hasOwnProperty.call(n, i)) {
          if (r.indexOf(i) !== -1)
            continue;
          o[i] = n[i];
        }
      return o;
    }
    e.exports = t, e.exports.__esModule = !0, e.exports.default = e.exports;
  }(Vs)), Vs.exports;
}
const aw = /* @__PURE__ */ Gt(Zv), uw = /* @__PURE__ */ Gt(qv), cw = /* @__PURE__ */ Gt(i1), fw = /* @__PURE__ */ Gt(ax), dw = /* @__PURE__ */ Gt(G1), pw = /* @__PURE__ */ Gt(q1);
var Or = dc;
Object.defineProperty(Vo, "__esModule", {
  value: !0
});
var mw = Vo.default = Pw;
Vo.shouldForwardProp = Mi;
Vo.systemDefaultTheme = void 0;
var it = Or(ch()), Qa = Or(sw()), al = ww(aw), hw = uw;
Or(cw);
Or(fw);
var gw = Or(dw), yw = Or(pw);
const vw = ["ownerState"], xw = ["variants"], Sw = ["name", "slot", "skipVariantsResolver", "skipSx", "overridesResolver"];
function Wh(e) {
  if (typeof WeakMap != "function")
    return null;
  var t = /* @__PURE__ */ new WeakMap(), n = /* @__PURE__ */ new WeakMap();
  return (Wh = function(r) {
    return r ? n : t;
  })(e);
}
function ww(e, t) {
  if (!t && e && e.__esModule)
    return e;
  if (e === null || typeof e != "object" && typeof e != "function")
    return { default: e };
  var n = Wh(t);
  if (n && n.has(e))
    return n.get(e);
  var r = { __proto__: null }, o = Object.defineProperty && Object.getOwnPropertyDescriptor;
  for (var i in e)
    if (i !== "default" && Object.prototype.hasOwnProperty.call(e, i)) {
      var l = o ? Object.getOwnPropertyDescriptor(e, i) : null;
      l && (l.get || l.set) ? Object.defineProperty(r, i, l) : r[i] = e[i];
    }
  return r.default = e, n && n.set(e, r), r;
}
function kw(e) {
  return Object.keys(e).length === 0;
}
function Cw(e) {
  return typeof e == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  e.charCodeAt(0) > 96;
}
function Mi(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
function dd(e, t) {
  return t && e && typeof e == "object" && e.styles && !e.styles.startsWith("@layer") && (e.styles = `@layer ${t}{${String(e.styles)}}`), e;
}
const Ew = Vo.systemDefaultTheme = (0, gw.default)(), _w = (e) => e && e.charAt(0).toLowerCase() + e.slice(1);
function mi({
  defaultTheme: e,
  theme: t,
  themeId: n
}) {
  return kw(t) ? e : t[n] || t;
}
function $w(e) {
  return e ? (t, n) => n[e] : null;
}
function Ni(e, t, n) {
  let {
    ownerState: r
  } = t, o = (0, Qa.default)(t, vw);
  const i = typeof e == "function" ? e((0, it.default)({
    ownerState: r
  }, o)) : e;
  if (Array.isArray(i))
    return i.flatMap((l) => Ni(l, (0, it.default)({
      ownerState: r
    }, o), n));
  if (i && typeof i == "object" && Array.isArray(i.variants)) {
    const {
      variants: l = []
    } = i;
    let a = (0, Qa.default)(i, xw);
    return l.forEach((u) => {
      let c = !0;
      if (typeof u.props == "function" ? c = u.props((0, it.default)({
        ownerState: r
      }, o, r)) : Object.keys(u.props).forEach((f) => {
        (r == null ? void 0 : r[f]) !== u.props[f] && o[f] !== u.props[f] && (c = !1);
      }), c) {
        Array.isArray(a) || (a = [a]);
        const f = typeof u.style == "function" ? u.style((0, it.default)({
          ownerState: r
        }, o, r)) : u.style;
        a.push(n ? dd((0, al.internal_serializeStyles)(f), n) : f);
      }
    }), a;
  }
  return n ? dd((0, al.internal_serializeStyles)(i), n) : i;
}
function Pw(e = {}) {
  const {
    themeId: t,
    defaultTheme: n = Ew,
    rootShouldForwardProp: r = Mi,
    slotShouldForwardProp: o = Mi
  } = e, i = (l) => (0, yw.default)((0, it.default)({}, l, {
    theme: mi((0, it.default)({}, l, {
      defaultTheme: n,
      themeId: t
    }))
  }));
  return i.__mui_systemSx = !0, (l, s = {}) => {
    (0, al.internal_processStyles)(l, (k) => k.filter((w) => !(w != null && w.__mui_systemSx)));
    const {
      name: a,
      slot: u,
      skipVariantsResolver: c,
      skipSx: f,
      // TODO v6: remove `lowercaseFirstLetter()` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      overridesResolver: p = $w(_w(u))
    } = s, v = (0, Qa.default)(s, Sw), y = a && a.startsWith("Mui") || u ? "components" : "custom", g = c !== void 0 ? c : (
      // TODO v6: remove `Root` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      u && u !== "Root" && u !== "root" || !1
    ), _ = f || !1;
    let m, d = Mi;
    u === "Root" || u === "root" ? d = r : u ? d = o : Cw(l) && (d = void 0);
    const h = (0, al.default)(l, (0, it.default)({
      shouldForwardProp: d,
      label: m
    }, v)), x = (k) => typeof k == "function" && k.__emotion_real !== k || (0, hw.isPlainObject)(k) ? (w) => {
      const T = mi({
        theme: w.theme,
        defaultTheme: n,
        themeId: t
      });
      return Ni(k, (0, it.default)({}, w, {
        theme: T
      }), T.modularCssLayers ? y : void 0);
    } : k, E = (k, ...w) => {
      let T = x(k);
      const N = w ? w.map(x) : [];
      a && p && N.push((A) => {
        const L = mi((0, it.default)({}, A, {
          defaultTheme: n,
          themeId: t
        }));
        if (!L.components || !L.components[a] || !L.components[a].styleOverrides)
          return null;
        const U = L.components[a].styleOverrides, te = {};
        return Object.entries(U).forEach(([ve, he]) => {
          te[ve] = Ni(he, (0, it.default)({}, A, {
            theme: L
          }), L.modularCssLayers ? "theme" : void 0);
        }), p(A, te);
      }), a && !g && N.push((A) => {
        var L;
        const U = mi((0, it.default)({}, A, {
          defaultTheme: n,
          themeId: t
        })), te = U == null || (L = U.components) == null || (L = L[a]) == null ? void 0 : L.variants;
        return Ni({
          variants: te
        }, (0, it.default)({}, A, {
          theme: U
        }), U.modularCssLayers ? "theme" : void 0);
      }), _ || N.push(i);
      const O = N.length - w.length;
      if (Array.isArray(k) && O > 0) {
        const A = new Array(O).fill("");
        T = [...k, ...A], T.raw = [...k.raw, ...A];
      }
      const F = h(T, ...N);
      return l.muiName && (F.muiName = l.muiName), F;
    };
    return h.withConfig && (E.withConfig = h.withConfig), E;
  };
}
function Tw(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
const Rw = (e) => Tw(e) && e !== "classes", Ow = Rw, Mw = mw({
  themeId: wr,
  defaultTheme: yc,
  rootShouldForwardProp: Ow
}), oe = Mw, Nw = ["theme"];
function zw(e) {
  let {
    theme: t
  } = e, n = W(e, Nw);
  const r = t[wr];
  let o = r || t;
  return typeof t != "function" && (r && !r.vars ? o = S({}, r, {
    vars: null
  }) : t && !t.vars && (o = S({}, t, {
    vars: null
  }))), /* @__PURE__ */ $.jsx(sS, S({}, n, {
    themeId: r ? wr : void 0,
    theme: o
  }));
}
const Lw = (e) => {
  let t;
  return e < 1 ? t = 5.11916 * e ** 2 : t = 4.5 * Math.log(e + 1) + 2, (t / 100).toFixed(2);
}, pd = Lw;
function Fe(e) {
  return iS(e);
}
function jw(e) {
  return /* @__PURE__ */ $.jsx(Sh, S({}, e, {
    defaultTheme: yc,
    themeId: wr
  }));
}
const Iw = (e, t) => S({
  WebkitFontSmoothing: "antialiased",
  // Antialiasing.
  MozOsxFontSmoothing: "grayscale",
  // Antialiasing.
  // Change from `box-sizing: content-box` so that `width`
  // is not affected by `padding` or `border`.
  boxSizing: "border-box",
  // Fix font resize problem in iOS
  WebkitTextSizeAdjust: "100%"
}, t && !e.vars && {
  colorScheme: e.palette.mode
}), Aw = (e) => S({
  color: (e.vars || e).palette.text.primary
}, e.typography.body1, {
  backgroundColor: (e.vars || e).palette.background.default,
  "@media print": {
    // Save printer ink.
    backgroundColor: (e.vars || e).palette.common.white
  }
}), bw = (e, t = !1) => {
  var n;
  const r = {};
  t && e.colorSchemes && Object.entries(e.colorSchemes).forEach(([l, s]) => {
    var a;
    r[e.getColorSchemeSelector(l).replace(/\s*&/, "")] = {
      colorScheme: (a = s.palette) == null ? void 0 : a.mode
    };
  });
  let o = S({
    html: Iw(e, t),
    "*, *::before, *::after": {
      boxSizing: "inherit"
    },
    "strong, b": {
      fontWeight: e.typography.fontWeightBold
    },
    body: S({
      margin: 0
    }, Aw(e), {
      // Add support for document.body.requestFullScreen().
      // Other elements, if background transparent, are not supported.
      "&::backdrop": {
        backgroundColor: (e.vars || e).palette.background.default
      }
    })
  }, r);
  const i = (n = e.components) == null || (n = n.MuiCssBaseline) == null ? void 0 : n.styleOverrides;
  return i && (o = [o, i]), o;
};
function Dw(e) {
  const t = Fe({
    props: e,
    name: "MuiCssBaseline"
  }), {
    children: n,
    enableColorScheme: r = !1
  } = t;
  return /* @__PURE__ */ $.jsxs(C.Fragment, {
    children: [/* @__PURE__ */ $.jsx(jw, {
      styles: (o) => bw(o, r)
    }), n]
  });
}
const Fw = pS({
  createStyledComponent: oe("div", {
    name: "MuiContainer",
    slot: "Root",
    overridesResolver: (e, t) => {
      const {
        ownerState: n
      } = e;
      return [t.root, t[`maxWidth${X(String(n.maxWidth))}`], n.fixed && t.fixed, n.disableGutters && t.disableGutters];
    }
  }),
  useThemeProps: (e) => Fe({
    props: e,
    name: "MuiContainer"
  })
}), Bw = Fw;
function Ww(e) {
  return Ge("MuiTypography", e);
}
Qe("MuiTypography", ["root", "h1", "h2", "h3", "h4", "h5", "h6", "subtitle1", "subtitle2", "body1", "body2", "inherit", "button", "caption", "overline", "alignLeft", "alignRight", "alignCenter", "alignJustify", "noWrap", "gutterBottom", "paragraph"]);
const Uw = ["align", "className", "component", "gutterBottom", "noWrap", "paragraph", "variant", "variantMapping"], Vw = (e) => {
  const {
    align: t,
    gutterBottom: n,
    noWrap: r,
    paragraph: o,
    variant: i,
    classes: l
  } = e, s = {
    root: ["root", i, e.align !== "inherit" && `align${X(t)}`, n && "gutterBottom", r && "noWrap", o && "paragraph"]
  };
  return ot(s, Ww, l);
}, Hw = oe("span", {
  name: "MuiTypography",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.variant && t[n.variant], n.align !== "inherit" && t[`align${X(n.align)}`], n.noWrap && t.noWrap, n.gutterBottom && t.gutterBottom, n.paragraph && t.paragraph];
  }
})(({
  theme: e,
  ownerState: t
}) => S({
  margin: 0
}, t.variant === "inherit" && {
  // Some elements, like <button> on Chrome have default font that doesn't inherit, reset this.
  font: "inherit"
}, t.variant !== "inherit" && e.typography[t.variant], t.align !== "inherit" && {
  textAlign: t.align
}, t.noWrap && {
  overflow: "hidden",
  textOverflow: "ellipsis",
  whiteSpace: "nowrap"
}, t.gutterBottom && {
  marginBottom: "0.35em"
}, t.paragraph && {
  marginBottom: 16
})), md = {
  h1: "h1",
  h2: "h2",
  h3: "h3",
  h4: "h4",
  h5: "h5",
  h6: "h6",
  subtitle1: "h6",
  subtitle2: "h6",
  body1: "p",
  body2: "p",
  inherit: "p"
}, Kw = {
  primary: "primary.main",
  textPrimary: "text.primary",
  secondary: "secondary.main",
  textSecondary: "text.secondary",
  error: "error.main"
}, Gw = (e) => Kw[e] || e, Qw = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = Fe({
    props: t,
    name: "MuiTypography"
  }), o = Gw(r.color), i = Ql(S({}, r, {
    color: o
  })), {
    align: l = "inherit",
    className: s,
    component: a,
    gutterBottom: u = !1,
    noWrap: c = !1,
    paragraph: f = !1,
    variant: p = "body1",
    variantMapping: v = md
  } = i, y = W(i, Uw), g = S({}, i, {
    align: l,
    color: o,
    className: s,
    component: a,
    gutterBottom: u,
    noWrap: c,
    paragraph: f,
    variant: p,
    variantMapping: v
  }), _ = a || (f ? "p" : v[p] || md[p]) || "span", m = Vw(g);
  return /* @__PURE__ */ $.jsx(Hw, S({
    as: _,
    ref: n,
    ownerState: g,
    className: J(m.root, s)
  }, y));
}), On = Qw;
function Yw(e) {
  return Ge("MuiCircularProgress", e);
}
Qe("MuiCircularProgress", ["root", "determinate", "indeterminate", "colorPrimary", "colorSecondary", "svg", "circle", "circleDeterminate", "circleIndeterminate", "circleDisableShrink"]);
const Xw = ["className", "color", "disableShrink", "size", "style", "thickness", "value", "variant"];
let ss = (e) => e, hd, gd, yd, vd;
const qt = 44, Zw = Tr(hd || (hd = ss`
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
`)), qw = Tr(gd || (gd = ss`
  0% {
    stroke-dasharray: 1px, 200px;
    stroke-dashoffset: 0;
  }

  50% {
    stroke-dasharray: 100px, 200px;
    stroke-dashoffset: -15px;
  }

  100% {
    stroke-dasharray: 100px, 200px;
    stroke-dashoffset: -125px;
  }
`)), Jw = (e) => {
  const {
    classes: t,
    variant: n,
    color: r,
    disableShrink: o
  } = e, i = {
    root: ["root", n, `color${X(r)}`],
    svg: ["svg"],
    circle: ["circle", `circle${X(n)}`, o && "circleDisableShrink"]
  };
  return ot(i, Yw, t);
}, e2 = oe("span", {
  name: "MuiCircularProgress",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[n.variant], t[`color${X(n.color)}`]];
  }
})(({
  ownerState: e,
  theme: t
}) => S({
  display: "inline-block"
}, e.variant === "determinate" && {
  transition: t.transitions.create("transform")
}, e.color !== "inherit" && {
  color: (t.vars || t).palette[e.color].main
}), ({
  ownerState: e
}) => e.variant === "indeterminate" && Dl(yd || (yd = ss`
      animation: ${0} 1.4s linear infinite;
    `), Zw)), t2 = oe("svg", {
  name: "MuiCircularProgress",
  slot: "Svg",
  overridesResolver: (e, t) => t.svg
})({
  display: "block"
  // Keeps the progress centered
}), n2 = oe("circle", {
  name: "MuiCircularProgress",
  slot: "Circle",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.circle, t[`circle${X(n.variant)}`], n.disableShrink && t.circleDisableShrink];
  }
})(({
  ownerState: e,
  theme: t
}) => S({
  stroke: "currentColor"
}, e.variant === "determinate" && {
  transition: t.transitions.create("stroke-dashoffset")
}, e.variant === "indeterminate" && {
  // Some default value that looks fine waiting for the animation to kicks in.
  strokeDasharray: "80px, 200px",
  strokeDashoffset: 0
  // Add the unit to fix a Edge 16 and below bug.
}), ({
  ownerState: e
}) => e.variant === "indeterminate" && !e.disableShrink && Dl(vd || (vd = ss`
      animation: ${0} 1.4s ease-in-out infinite;
    `), qw)), r2 = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = Fe({
    props: t,
    name: "MuiCircularProgress"
  }), {
    className: o,
    color: i = "primary",
    disableShrink: l = !1,
    size: s = 40,
    style: a,
    thickness: u = 3.6,
    value: c = 0,
    variant: f = "indeterminate"
  } = r, p = W(r, Xw), v = S({}, r, {
    color: i,
    disableShrink: l,
    size: s,
    thickness: u,
    value: c,
    variant: f
  }), y = Jw(v), g = {}, _ = {}, m = {};
  if (f === "determinate") {
    const d = 2 * Math.PI * ((qt - u) / 2);
    g.strokeDasharray = d.toFixed(3), m["aria-valuenow"] = Math.round(c), g.strokeDashoffset = `${((100 - c) / 100 * d).toFixed(3)}px`, _.transform = "rotate(-90deg)";
  }
  return /* @__PURE__ */ $.jsx(e2, S({
    className: J(y.root, o),
    style: S({
      width: s,
      height: s
    }, _, a),
    ownerState: v,
    ref: n,
    role: "progressbar"
  }, m, p, {
    children: /* @__PURE__ */ $.jsx(t2, {
      className: y.svg,
      ownerState: v,
      viewBox: `${qt / 2} ${qt / 2} ${qt} ${qt}`,
      children: /* @__PURE__ */ $.jsx(n2, {
        className: y.circle,
        style: g,
        ownerState: v,
        cx: qt,
        cy: qt,
        r: (qt - u) / 2,
        fill: "none",
        strokeWidth: u
      })
    })
  }));
}), o2 = r2, i2 = ["className", "elementType", "ownerState", "externalForwardedProps", "getSlotOwnerState", "internalForwardedProps"], l2 = ["component", "slots", "slotProps"], s2 = ["component"];
function xd(e, t) {
  const {
    className: n,
    elementType: r,
    ownerState: o,
    externalForwardedProps: i,
    getSlotOwnerState: l,
    internalForwardedProps: s
  } = t, a = W(t, i2), {
    component: u,
    slots: c = {
      [e]: void 0
    },
    slotProps: f = {
      [e]: void 0
    }
  } = i, p = W(i, l2), v = c[e] || r, y = Qx(f[e], o), g = Gx(S({
    className: n
  }, a, {
    externalForwardedProps: e === "root" ? p : void 0,
    externalSlotProps: y
  })), {
    props: {
      component: _
    },
    internalRef: m
  } = g, d = W(g.props, s2), h = To(m, y == null ? void 0 : y.ref, t.ref), x = l ? l(d) : {}, E = S({}, o, x), k = e === "root" ? _ || u : _, w = Hx(v, S({}, e === "root" && !u && !c[e] && s, e !== "root" && !c[e] && s, d, k && {
    as: k
  }, {
    ref: h
  }), E);
  return Object.keys(x).forEach((T) => {
    delete w[T];
  }), [v, w];
}
function a2(e) {
  return Ge("MuiPaper", e);
}
Qe("MuiPaper", ["root", "rounded", "outlined", "elevation", "elevation0", "elevation1", "elevation2", "elevation3", "elevation4", "elevation5", "elevation6", "elevation7", "elevation8", "elevation9", "elevation10", "elevation11", "elevation12", "elevation13", "elevation14", "elevation15", "elevation16", "elevation17", "elevation18", "elevation19", "elevation20", "elevation21", "elevation22", "elevation23", "elevation24"]);
const u2 = ["className", "component", "elevation", "square", "variant"], c2 = (e) => {
  const {
    square: t,
    elevation: n,
    variant: r,
    classes: o
  } = e, i = {
    root: ["root", r, !t && "rounded", r === "elevation" && `elevation${n}`]
  };
  return ot(i, a2, o);
}, f2 = oe("div", {
  name: "MuiPaper",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[n.variant], !n.square && t.rounded, n.variant === "elevation" && t[`elevation${n.elevation}`]];
  }
})(({
  theme: e,
  ownerState: t
}) => {
  var n;
  return S({
    backgroundColor: (e.vars || e).palette.background.paper,
    color: (e.vars || e).palette.text.primary,
    transition: e.transitions.create("box-shadow")
  }, !t.square && {
    borderRadius: e.shape.borderRadius
  }, t.variant === "outlined" && {
    border: `1px solid ${(e.vars || e).palette.divider}`
  }, t.variant === "elevation" && S({
    boxShadow: (e.vars || e).shadows[t.elevation]
  }, !e.vars && e.palette.mode === "dark" && {
    backgroundImage: `linear-gradient(${Ro("#fff", pd(t.elevation))}, ${Ro("#fff", pd(t.elevation))})`
  }, e.vars && {
    backgroundImage: (n = e.vars.overlays) == null ? void 0 : n[t.elevation]
  }));
}), d2 = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = Fe({
    props: t,
    name: "MuiPaper"
  }), {
    className: o,
    component: i = "div",
    elevation: l = 1,
    square: s = !1,
    variant: a = "elevation"
  } = r, u = W(r, u2), c = S({}, r, {
    component: i,
    elevation: l,
    square: s,
    variant: a
  }), f = c2(c);
  return /* @__PURE__ */ $.jsx(f2, S({
    as: i,
    ownerState: c,
    className: J(f.root, o),
    ref: n
  }, u));
}), Uh = d2;
function p2(e) {
  return Ge("MuiAlert", e);
}
const m2 = Qe("MuiAlert", ["root", "action", "icon", "message", "filled", "colorSuccess", "colorInfo", "colorWarning", "colorError", "filledSuccess", "filledInfo", "filledWarning", "filledError", "outlined", "outlinedSuccess", "outlinedInfo", "outlinedWarning", "outlinedError", "standard", "standardSuccess", "standardInfo", "standardWarning", "standardError"]), Sd = m2;
function Ya(e, t) {
  return Ya = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, r) {
    return n.__proto__ = r, n;
  }, Ya(e, t);
}
function Vh(e, t) {
  e.prototype = Object.create(t.prototype), e.prototype.constructor = e, Ya(e, t);
}
const wd = {
  disabled: !1
}, ul = Ct.createContext(null);
var h2 = function(t) {
  return t.scrollTop;
}, Yr = "unmounted", kn = "exited", Cn = "entering", Kn = "entered", Xa = "exiting", Yt = /* @__PURE__ */ function(e) {
  Vh(t, e);
  function t(r, o) {
    var i;
    i = e.call(this, r, o) || this;
    var l = o, s = l && !l.isMounting ? r.enter : r.appear, a;
    return i.appearStatus = null, r.in ? s ? (a = kn, i.appearStatus = Cn) : a = Kn : r.unmountOnExit || r.mountOnEnter ? a = Yr : a = kn, i.state = {
      status: a
    }, i.nextCallback = null, i;
  }
  t.getDerivedStateFromProps = function(o, i) {
    var l = o.in;
    return l && i.status === Yr ? {
      status: kn
    } : null;
  };
  var n = t.prototype;
  return n.componentDidMount = function() {
    this.updateStatus(!0, this.appearStatus);
  }, n.componentDidUpdate = function(o) {
    var i = null;
    if (o !== this.props) {
      var l = this.state.status;
      this.props.in ? l !== Cn && l !== Kn && (i = Cn) : (l === Cn || l === Kn) && (i = Xa);
    }
    this.updateStatus(!1, i);
  }, n.componentWillUnmount = function() {
    this.cancelNextCallback();
  }, n.getTimeouts = function() {
    var o = this.props.timeout, i, l, s;
    return i = l = s = o, o != null && typeof o != "number" && (i = o.exit, l = o.enter, s = o.appear !== void 0 ? o.appear : l), {
      exit: i,
      enter: l,
      appear: s
    };
  }, n.updateStatus = function(o, i) {
    if (o === void 0 && (o = !1), i !== null)
      if (this.cancelNextCallback(), i === Cn) {
        if (this.props.unmountOnExit || this.props.mountOnEnter) {
          var l = this.props.nodeRef ? this.props.nodeRef.current : fi.findDOMNode(this);
          l && h2(l);
        }
        this.performEnter(o);
      } else
        this.performExit();
    else
      this.props.unmountOnExit && this.state.status === kn && this.setState({
        status: Yr
      });
  }, n.performEnter = function(o) {
    var i = this, l = this.props.enter, s = this.context ? this.context.isMounting : o, a = this.props.nodeRef ? [s] : [fi.findDOMNode(this), s], u = a[0], c = a[1], f = this.getTimeouts(), p = s ? f.appear : f.enter;
    if (!o && !l || wd.disabled) {
      this.safeSetState({
        status: Kn
      }, function() {
        i.props.onEntered(u);
      });
      return;
    }
    this.props.onEnter(u, c), this.safeSetState({
      status: Cn
    }, function() {
      i.props.onEntering(u, c), i.onTransitionEnd(p, function() {
        i.safeSetState({
          status: Kn
        }, function() {
          i.props.onEntered(u, c);
        });
      });
    });
  }, n.performExit = function() {
    var o = this, i = this.props.exit, l = this.getTimeouts(), s = this.props.nodeRef ? void 0 : fi.findDOMNode(this);
    if (!i || wd.disabled) {
      this.safeSetState({
        status: kn
      }, function() {
        o.props.onExited(s);
      });
      return;
    }
    this.props.onExit(s), this.safeSetState({
      status: Xa
    }, function() {
      o.props.onExiting(s), o.onTransitionEnd(l.exit, function() {
        o.safeSetState({
          status: kn
        }, function() {
          o.props.onExited(s);
        });
      });
    });
  }, n.cancelNextCallback = function() {
    this.nextCallback !== null && (this.nextCallback.cancel(), this.nextCallback = null);
  }, n.safeSetState = function(o, i) {
    i = this.setNextCallback(i), this.setState(o, i);
  }, n.setNextCallback = function(o) {
    var i = this, l = !0;
    return this.nextCallback = function(s) {
      l && (l = !1, i.nextCallback = null, o(s));
    }, this.nextCallback.cancel = function() {
      l = !1;
    }, this.nextCallback;
  }, n.onTransitionEnd = function(o, i) {
    this.setNextCallback(i);
    var l = this.props.nodeRef ? this.props.nodeRef.current : fi.findDOMNode(this), s = o == null && !this.props.addEndListener;
    if (!l || s) {
      setTimeout(this.nextCallback, 0);
      return;
    }
    if (this.props.addEndListener) {
      var a = this.props.nodeRef ? [this.nextCallback] : [l, this.nextCallback], u = a[0], c = a[1];
      this.props.addEndListener(u, c);
    }
    o != null && setTimeout(this.nextCallback, o);
  }, n.render = function() {
    var o = this.state.status;
    if (o === Yr)
      return null;
    var i = this.props, l = i.children;
    i.in, i.mountOnEnter, i.unmountOnExit, i.appear, i.enter, i.exit, i.timeout, i.addEndListener, i.onEnter, i.onEntering, i.onEntered, i.onExit, i.onExiting, i.onExited, i.nodeRef;
    var s = W(i, ["children", "in", "mountOnEnter", "unmountOnExit", "appear", "enter", "exit", "timeout", "addEndListener", "onEnter", "onEntering", "onEntered", "onExit", "onExiting", "onExited", "nodeRef"]);
    return (
      // allows for nested Transitions
      /* @__PURE__ */ Ct.createElement(ul.Provider, {
        value: null
      }, typeof l == "function" ? l(o, s) : Ct.cloneElement(Ct.Children.only(l), s))
    );
  }, t;
}(Ct.Component);
Yt.contextType = ul;
Yt.propTypes = {};
function Hn() {
}
Yt.defaultProps = {
  in: !1,
  mountOnEnter: !1,
  unmountOnExit: !1,
  appear: !1,
  enter: !0,
  exit: !0,
  onEnter: Hn,
  onEntering: Hn,
  onEntered: Hn,
  onExit: Hn,
  onExiting: Hn,
  onExited: Hn
};
Yt.UNMOUNTED = Yr;
Yt.EXITED = kn;
Yt.ENTERING = Cn;
Yt.ENTERED = Kn;
Yt.EXITING = Xa;
const g2 = Yt;
function y2(e) {
  if (e === void 0)
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function vc(e, t) {
  var n = function(i) {
    return t && C.isValidElement(i) ? t(i) : i;
  }, r = /* @__PURE__ */ Object.create(null);
  return e && C.Children.map(e, function(o) {
    return o;
  }).forEach(function(o) {
    r[o.key] = n(o);
  }), r;
}
function v2(e, t) {
  e = e || {}, t = t || {};
  function n(c) {
    return c in t ? t[c] : e[c];
  }
  var r = /* @__PURE__ */ Object.create(null), o = [];
  for (var i in e)
    i in t ? o.length && (r[i] = o, o = []) : o.push(i);
  var l, s = {};
  for (var a in t) {
    if (r[a])
      for (l = 0; l < r[a].length; l++) {
        var u = r[a][l];
        s[r[a][l]] = n(u);
      }
    s[a] = n(a);
  }
  for (l = 0; l < o.length; l++)
    s[o[l]] = n(o[l]);
  return s;
}
function Pn(e, t, n) {
  return n[t] != null ? n[t] : e.props[t];
}
function x2(e, t) {
  return vc(e.children, function(n) {
    return C.cloneElement(n, {
      onExited: t.bind(null, n),
      in: !0,
      appear: Pn(n, "appear", e),
      enter: Pn(n, "enter", e),
      exit: Pn(n, "exit", e)
    });
  });
}
function S2(e, t, n) {
  var r = vc(e.children), o = v2(t, r);
  return Object.keys(o).forEach(function(i) {
    var l = o[i];
    if (C.isValidElement(l)) {
      var s = i in t, a = i in r, u = t[i], c = C.isValidElement(u) && !u.props.in;
      a && (!s || c) ? o[i] = C.cloneElement(l, {
        onExited: n.bind(null, l),
        in: !0,
        exit: Pn(l, "exit", e),
        enter: Pn(l, "enter", e)
      }) : !a && s && !c ? o[i] = C.cloneElement(l, {
        in: !1
      }) : a && s && C.isValidElement(u) && (o[i] = C.cloneElement(l, {
        onExited: n.bind(null, l),
        in: u.props.in,
        exit: Pn(l, "exit", e),
        enter: Pn(l, "enter", e)
      }));
    }
  }), o;
}
var w2 = Object.values || function(e) {
  return Object.keys(e).map(function(t) {
    return e[t];
  });
}, k2 = {
  component: "div",
  childFactory: function(t) {
    return t;
  }
}, xc = /* @__PURE__ */ function(e) {
  Vh(t, e);
  function t(r, o) {
    var i;
    i = e.call(this, r, o) || this;
    var l = i.handleExited.bind(y2(i));
    return i.state = {
      contextValue: {
        isMounting: !0
      },
      handleExited: l,
      firstRender: !0
    }, i;
  }
  var n = t.prototype;
  return n.componentDidMount = function() {
    this.mounted = !0, this.setState({
      contextValue: {
        isMounting: !1
      }
    });
  }, n.componentWillUnmount = function() {
    this.mounted = !1;
  }, t.getDerivedStateFromProps = function(o, i) {
    var l = i.children, s = i.handleExited, a = i.firstRender;
    return {
      children: a ? x2(o, s) : S2(o, l, s),
      firstRender: !1
    };
  }, n.handleExited = function(o, i) {
    var l = vc(this.props.children);
    o.key in l || (o.props.onExited && o.props.onExited(i), this.mounted && this.setState(function(s) {
      var a = S({}, s.children);
      return delete a[o.key], {
        children: a
      };
    }));
  }, n.render = function() {
    var o = this.props, i = o.component, l = o.childFactory, s = W(o, ["component", "childFactory"]), a = this.state.contextValue, u = w2(this.state.children).map(l);
    return delete s.appear, delete s.enter, delete s.exit, i === null ? /* @__PURE__ */ Ct.createElement(ul.Provider, {
      value: a
    }, u) : /* @__PURE__ */ Ct.createElement(ul.Provider, {
      value: a
    }, /* @__PURE__ */ Ct.createElement(i, s, u));
  }, t;
}(Ct.Component);
xc.propTypes = {};
xc.defaultProps = k2;
const C2 = xc;
function E2(e) {
  const {
    className: t,
    classes: n,
    pulsate: r = !1,
    rippleX: o,
    rippleY: i,
    rippleSize: l,
    in: s,
    onExited: a,
    timeout: u
  } = e, [c, f] = C.useState(!1), p = J(t, n.ripple, n.rippleVisible, r && n.ripplePulsate), v = {
    width: l,
    height: l,
    top: -(l / 2) + i,
    left: -(l / 2) + o
  }, y = J(n.child, c && n.childLeaving, r && n.childPulsate);
  return !s && !c && f(!0), C.useEffect(() => {
    if (!s && a != null) {
      const g = setTimeout(a, u);
      return () => {
        clearTimeout(g);
      };
    }
  }, [a, s, u]), /* @__PURE__ */ $.jsx("span", {
    className: p,
    style: v,
    children: /* @__PURE__ */ $.jsx("span", {
      className: y
    })
  });
}
const _2 = Qe("MuiTouchRipple", ["root", "ripple", "rippleVisible", "ripplePulsate", "child", "childLeaving", "childPulsate"]), lt = _2, $2 = ["center", "classes", "className"];
let as = (e) => e, kd, Cd, Ed, _d;
const Za = 550, P2 = 80, T2 = Tr(kd || (kd = as`
  0% {
    transform: scale(0);
    opacity: 0.1;
  }

  100% {
    transform: scale(1);
    opacity: 0.3;
  }
`)), R2 = Tr(Cd || (Cd = as`
  0% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
`)), O2 = Tr(Ed || (Ed = as`
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(0.92);
  }

  100% {
    transform: scale(1);
  }
`)), M2 = oe("span", {
  name: "MuiTouchRipple",
  slot: "Root"
})({
  overflow: "hidden",
  pointerEvents: "none",
  position: "absolute",
  zIndex: 0,
  top: 0,
  right: 0,
  bottom: 0,
  left: 0,
  borderRadius: "inherit"
}), N2 = oe(E2, {
  name: "MuiTouchRipple",
  slot: "Ripple"
})(_d || (_d = as`
  opacity: 0;
  position: absolute;

  &.${0} {
    opacity: 0.3;
    transform: scale(1);
    animation-name: ${0};
    animation-duration: ${0}ms;
    animation-timing-function: ${0};
  }

  &.${0} {
    animation-duration: ${0}ms;
  }

  & .${0} {
    opacity: 1;
    display: block;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background-color: currentColor;
  }

  & .${0} {
    opacity: 0;
    animation-name: ${0};
    animation-duration: ${0}ms;
    animation-timing-function: ${0};
  }

  & .${0} {
    position: absolute;
    /* @noflip */
    left: 0px;
    top: 0;
    animation-name: ${0};
    animation-duration: 2500ms;
    animation-timing-function: ${0};
    animation-iteration-count: infinite;
    animation-delay: 200ms;
  }
`), lt.rippleVisible, T2, Za, ({
  theme: e
}) => e.transitions.easing.easeInOut, lt.ripplePulsate, ({
  theme: e
}) => e.transitions.duration.shorter, lt.child, lt.childLeaving, R2, Za, ({
  theme: e
}) => e.transitions.easing.easeInOut, lt.childPulsate, O2, ({
  theme: e
}) => e.transitions.easing.easeInOut), z2 = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = Fe({
    props: t,
    name: "MuiTouchRipple"
  }), {
    center: o = !1,
    classes: i = {},
    className: l
  } = r, s = W(r, $2), [a, u] = C.useState([]), c = C.useRef(0), f = C.useRef(null);
  C.useEffect(() => {
    f.current && (f.current(), f.current = null);
  }, [a]);
  const p = C.useRef(!1), v = Th(), y = C.useRef(null), g = C.useRef(null), _ = C.useCallback((x) => {
    const {
      pulsate: E,
      rippleX: k,
      rippleY: w,
      rippleSize: T,
      cb: N
    } = x;
    u((O) => [...O, /* @__PURE__ */ $.jsx(N2, {
      classes: {
        ripple: J(i.ripple, lt.ripple),
        rippleVisible: J(i.rippleVisible, lt.rippleVisible),
        ripplePulsate: J(i.ripplePulsate, lt.ripplePulsate),
        child: J(i.child, lt.child),
        childLeaving: J(i.childLeaving, lt.childLeaving),
        childPulsate: J(i.childPulsate, lt.childPulsate)
      },
      timeout: Za,
      pulsate: E,
      rippleX: k,
      rippleY: w,
      rippleSize: T
    }, c.current)]), c.current += 1, f.current = N;
  }, [i]), m = C.useCallback((x = {}, E = {}, k = () => {
  }) => {
    const {
      pulsate: w = !1,
      center: T = o || E.pulsate,
      fakeElement: N = !1
      // For test purposes
    } = E;
    if ((x == null ? void 0 : x.type) === "mousedown" && p.current) {
      p.current = !1;
      return;
    }
    (x == null ? void 0 : x.type) === "touchstart" && (p.current = !0);
    const O = N ? null : g.current, F = O ? O.getBoundingClientRect() : {
      width: 0,
      height: 0,
      left: 0,
      top: 0
    };
    let A, L, U;
    if (T || x === void 0 || x.clientX === 0 && x.clientY === 0 || !x.clientX && !x.touches)
      A = Math.round(F.width / 2), L = Math.round(F.height / 2);
    else {
      const {
        clientX: te,
        clientY: ve
      } = x.touches && x.touches.length > 0 ? x.touches[0] : x;
      A = Math.round(te - F.left), L = Math.round(ve - F.top);
    }
    if (T)
      U = Math.sqrt((2 * F.width ** 2 + F.height ** 2) / 3), U % 2 === 0 && (U += 1);
    else {
      const te = Math.max(Math.abs((O ? O.clientWidth : 0) - A), A) * 2 + 2, ve = Math.max(Math.abs((O ? O.clientHeight : 0) - L), L) * 2 + 2;
      U = Math.sqrt(te ** 2 + ve ** 2);
    }
    x != null && x.touches ? y.current === null && (y.current = () => {
      _({
        pulsate: w,
        rippleX: A,
        rippleY: L,
        rippleSize: U,
        cb: k
      });
    }, v.start(P2, () => {
      y.current && (y.current(), y.current = null);
    })) : _({
      pulsate: w,
      rippleX: A,
      rippleY: L,
      rippleSize: U,
      cb: k
    });
  }, [o, _, v]), d = C.useCallback(() => {
    m({}, {
      pulsate: !0
    });
  }, [m]), h = C.useCallback((x, E) => {
    if (v.clear(), (x == null ? void 0 : x.type) === "touchend" && y.current) {
      y.current(), y.current = null, v.start(0, () => {
        h(x, E);
      });
      return;
    }
    y.current = null, u((k) => k.length > 0 ? k.slice(1) : k), f.current = E;
  }, [v]);
  return C.useImperativeHandle(n, () => ({
    pulsate: d,
    start: m,
    stop: h
  }), [d, m, h]), /* @__PURE__ */ $.jsx(M2, S({
    className: J(lt.root, i.root, l),
    ref: g
  }, s, {
    children: /* @__PURE__ */ $.jsx(C2, {
      component: null,
      exit: !0,
      children: a
    })
  }));
}), L2 = z2;
function j2(e) {
  return Ge("MuiButtonBase", e);
}
const I2 = Qe("MuiButtonBase", ["root", "disabled", "focusVisible"]), A2 = I2, b2 = ["action", "centerRipple", "children", "className", "component", "disabled", "disableRipple", "disableTouchRipple", "focusRipple", "focusVisibleClassName", "LinkComponent", "onBlur", "onClick", "onContextMenu", "onDragLeave", "onFocus", "onFocusVisible", "onKeyDown", "onKeyUp", "onMouseDown", "onMouseLeave", "onMouseUp", "onTouchEnd", "onTouchMove", "onTouchStart", "tabIndex", "TouchRippleProps", "touchRippleRef", "type"], D2 = (e) => {
  const {
    disabled: t,
    focusVisible: n,
    focusVisibleClassName: r,
    classes: o
  } = e, l = ot({
    root: ["root", t && "disabled", n && "focusVisible"]
  }, j2, o);
  return n && r && (l.root += ` ${r}`), l;
}, F2 = oe("button", {
  name: "MuiButtonBase",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})({
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  position: "relative",
  boxSizing: "border-box",
  WebkitTapHighlightColor: "transparent",
  backgroundColor: "transparent",
  // Reset default value
  // We disable the focus ring for mouse, touch and keyboard users.
  outline: 0,
  border: 0,
  margin: 0,
  // Remove the margin in Safari
  borderRadius: 0,
  padding: 0,
  // Remove the padding in Firefox
  cursor: "pointer",
  userSelect: "none",
  verticalAlign: "middle",
  MozAppearance: "none",
  // Reset
  WebkitAppearance: "none",
  // Reset
  textDecoration: "none",
  // So we take precedent over the style of a native <a /> element.
  color: "inherit",
  "&::-moz-focus-inner": {
    borderStyle: "none"
    // Remove Firefox dotted outline.
  },
  [`&.${A2.disabled}`]: {
    pointerEvents: "none",
    // Disable link interactions
    cursor: "default"
  },
  "@media print": {
    colorAdjust: "exact"
  }
}), B2 = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = Fe({
    props: t,
    name: "MuiButtonBase"
  }), {
    action: o,
    centerRipple: i = !1,
    children: l,
    className: s,
    component: a = "button",
    disabled: u = !1,
    disableRipple: c = !1,
    disableTouchRipple: f = !1,
    focusRipple: p = !1,
    LinkComponent: v = "a",
    onBlur: y,
    onClick: g,
    onContextMenu: _,
    onDragLeave: m,
    onFocus: d,
    onFocusVisible: h,
    onKeyDown: x,
    onKeyUp: E,
    onMouseDown: k,
    onMouseLeave: w,
    onMouseUp: T,
    onTouchEnd: N,
    onTouchMove: O,
    onTouchStart: F,
    tabIndex: A = 0,
    TouchRippleProps: L,
    touchRippleRef: U,
    type: te
  } = r, ve = W(r, b2), he = C.useRef(null), R = C.useRef(null), z = To(R, U), {
    isFocusVisibleRef: I,
    onFocus: Z,
    onBlur: ae,
    ref: Xt
  } = Rh(), [_e, Pt] = C.useState(!1);
  u && _e && Pt(!1), C.useImperativeHandle(o, () => ({
    focusVisible: () => {
      Pt(!0), he.current.focus();
    }
  }), []);
  const [j, xe] = C.useState(!1);
  C.useEffect(() => {
    xe(!0);
  }, []);
  const vt = j && !c && !u;
  C.useEffect(() => {
    _e && p && !c && j && R.current.pulsate();
  }, [c, p, _e, j]);
  function je(b, kc, f0 = f) {
    return Qr((Cc) => (kc && kc(Cc), !f0 && R.current && R.current[b](Cc), !0));
  }
  const bn = je("start", k), Ho = je("stop", _), Jh = je("stop", m), e0 = je("stop", T), t0 = je("stop", (b) => {
    _e && b.preventDefault(), w && w(b);
  }), n0 = je("start", F), r0 = je("stop", N), o0 = je("stop", O), i0 = je("stop", (b) => {
    ae(b), I.current === !1 && Pt(!1), y && y(b);
  }, !1), l0 = Qr((b) => {
    he.current || (he.current = b.currentTarget), Z(b), I.current === !0 && (Pt(!0), h && h(b)), d && d(b);
  }), us = () => {
    const b = he.current;
    return a && a !== "button" && !(b.tagName === "A" && b.href);
  }, cs = C.useRef(!1), s0 = Qr((b) => {
    p && !cs.current && _e && R.current && b.key === " " && (cs.current = !0, R.current.stop(b, () => {
      R.current.start(b);
    })), b.target === b.currentTarget && us() && b.key === " " && b.preventDefault(), x && x(b), b.target === b.currentTarget && us() && b.key === "Enter" && !u && (b.preventDefault(), g && g(b));
  }), a0 = Qr((b) => {
    p && b.key === " " && R.current && _e && !b.defaultPrevented && (cs.current = !1, R.current.stop(b, () => {
      R.current.pulsate(b);
    })), E && E(b), g && b.target === b.currentTarget && us() && b.key === " " && !b.defaultPrevented && g(b);
  });
  let Ko = a;
  Ko === "button" && (ve.href || ve.to) && (Ko = v);
  const Nr = {};
  Ko === "button" ? (Nr.type = te === void 0 ? "button" : te, Nr.disabled = u) : (!ve.href && !ve.to && (Nr.role = "button"), u && (Nr["aria-disabled"] = u));
  const u0 = To(n, Xt, he), wc = S({}, r, {
    centerRipple: i,
    component: a,
    disabled: u,
    disableRipple: c,
    disableTouchRipple: f,
    focusRipple: p,
    tabIndex: A,
    focusVisible: _e
  }), c0 = D2(wc);
  return /* @__PURE__ */ $.jsxs(F2, S({
    as: Ko,
    className: J(c0.root, s),
    ownerState: wc,
    onBlur: i0,
    onClick: g,
    onContextMenu: Ho,
    onFocus: l0,
    onKeyDown: s0,
    onKeyUp: a0,
    onMouseDown: bn,
    onMouseLeave: t0,
    onMouseUp: e0,
    onDragLeave: Jh,
    onTouchEnd: r0,
    onTouchMove: o0,
    onTouchStart: n0,
    ref: u0,
    tabIndex: u ? -1 : A,
    type: te
  }, Nr, ve, {
    children: [l, vt ? (
      /* TouchRipple is only needed client-side, x2 boost on the server. */
      /* @__PURE__ */ $.jsx(L2, S({
        ref: z,
        center: i
      }, L))
    ) : null]
  }));
}), W2 = B2;
function U2(e) {
  return Ge("MuiIconButton", e);
}
const V2 = Qe("MuiIconButton", ["root", "disabled", "colorInherit", "colorPrimary", "colorSecondary", "colorError", "colorInfo", "colorSuccess", "colorWarning", "edgeStart", "edgeEnd", "sizeSmall", "sizeMedium", "sizeLarge"]), H2 = V2, K2 = ["edge", "children", "className", "color", "disabled", "disableFocusRipple", "size"], G2 = (e) => {
  const {
    classes: t,
    disabled: n,
    color: r,
    edge: o,
    size: i
  } = e, l = {
    root: ["root", n && "disabled", r !== "default" && `color${X(r)}`, o && `edge${X(o)}`, `size${X(i)}`]
  };
  return ot(l, U2, t);
}, Q2 = oe(W2, {
  name: "MuiIconButton",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.color !== "default" && t[`color${X(n.color)}`], n.edge && t[`edge${X(n.edge)}`], t[`size${X(n.size)}`]];
  }
})(({
  theme: e,
  ownerState: t
}) => S({
  textAlign: "center",
  flex: "0 0 auto",
  fontSize: e.typography.pxToRem(24),
  padding: 8,
  borderRadius: "50%",
  overflow: "visible",
  // Explicitly set the default value to solve a bug on IE11.
  color: (e.vars || e).palette.action.active,
  transition: e.transitions.create("background-color", {
    duration: e.transitions.duration.shortest
  })
}, !t.disableRipple && {
  "&:hover": {
    backgroundColor: e.vars ? `rgba(${e.vars.palette.action.activeChannel} / ${e.vars.palette.action.hoverOpacity})` : Ro(e.palette.action.active, e.palette.action.hoverOpacity),
    // Reset on touch devices, it doesn't add specificity
    "@media (hover: none)": {
      backgroundColor: "transparent"
    }
  }
}, t.edge === "start" && {
  marginLeft: t.size === "small" ? -3 : -12
}, t.edge === "end" && {
  marginRight: t.size === "small" ? -3 : -12
}), ({
  theme: e,
  ownerState: t
}) => {
  var n;
  const r = (n = (e.vars || e).palette) == null ? void 0 : n[t.color];
  return S({}, t.color === "inherit" && {
    color: "inherit"
  }, t.color !== "inherit" && t.color !== "default" && S({
    color: r == null ? void 0 : r.main
  }, !t.disableRipple && {
    "&:hover": S({}, r && {
      backgroundColor: e.vars ? `rgba(${r.mainChannel} / ${e.vars.palette.action.hoverOpacity})` : Ro(r.main, e.palette.action.hoverOpacity)
    }, {
      // Reset on touch devices, it doesn't add specificity
      "@media (hover: none)": {
        backgroundColor: "transparent"
      }
    })
  }), t.size === "small" && {
    padding: 5,
    fontSize: e.typography.pxToRem(18)
  }, t.size === "large" && {
    padding: 12,
    fontSize: e.typography.pxToRem(28)
  }, {
    [`&.${H2.disabled}`]: {
      backgroundColor: "transparent",
      color: (e.vars || e).palette.action.disabled
    }
  });
}), Y2 = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = Fe({
    props: t,
    name: "MuiIconButton"
  }), {
    edge: o = !1,
    children: i,
    className: l,
    color: s = "default",
    disabled: a = !1,
    disableFocusRipple: u = !1,
    size: c = "medium"
  } = r, f = W(r, K2), p = S({}, r, {
    edge: o,
    color: s,
    disabled: a,
    disableFocusRipple: u,
    size: c
  }), v = G2(p);
  return /* @__PURE__ */ $.jsx(Q2, S({
    className: J(v.root, l),
    centerRipple: !0,
    focusRipple: !u,
    disabled: a,
    ref: n
  }, f, {
    ownerState: p,
    children: i
  }));
}), Hh = Y2;
function X2(e) {
  return Ge("MuiSvgIcon", e);
}
Qe("MuiSvgIcon", ["root", "colorPrimary", "colorSecondary", "colorAction", "colorError", "colorDisabled", "fontSizeInherit", "fontSizeSmall", "fontSizeMedium", "fontSizeLarge"]);
const Z2 = ["children", "className", "color", "component", "fontSize", "htmlColor", "inheritViewBox", "titleAccess", "viewBox"], q2 = (e) => {
  const {
    color: t,
    fontSize: n,
    classes: r
  } = e, o = {
    root: ["root", t !== "inherit" && `color${X(t)}`, `fontSize${X(n)}`]
  };
  return ot(o, X2, r);
}, J2 = oe("svg", {
  name: "MuiSvgIcon",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.color !== "inherit" && t[`color${X(n.color)}`], t[`fontSize${X(n.fontSize)}`]];
  }
})(({
  theme: e,
  ownerState: t
}) => {
  var n, r, o, i, l, s, a, u, c, f, p, v, y;
  return {
    userSelect: "none",
    width: "1em",
    height: "1em",
    display: "inline-block",
    // the <svg> will define the property that has `currentColor`
    // for example heroicons uses fill="none" and stroke="currentColor"
    fill: t.hasSvgAsChild ? void 0 : "currentColor",
    flexShrink: 0,
    transition: (n = e.transitions) == null || (r = n.create) == null ? void 0 : r.call(n, "fill", {
      duration: (o = e.transitions) == null || (o = o.duration) == null ? void 0 : o.shorter
    }),
    fontSize: {
      inherit: "inherit",
      small: ((i = e.typography) == null || (l = i.pxToRem) == null ? void 0 : l.call(i, 20)) || "1.25rem",
      medium: ((s = e.typography) == null || (a = s.pxToRem) == null ? void 0 : a.call(s, 24)) || "1.5rem",
      large: ((u = e.typography) == null || (c = u.pxToRem) == null ? void 0 : c.call(u, 35)) || "2.1875rem"
    }[t.fontSize],
    // TODO v5 deprecate, v6 remove for sx
    color: (f = (p = (e.vars || e).palette) == null || (p = p[t.color]) == null ? void 0 : p.main) != null ? f : {
      action: (v = (e.vars || e).palette) == null || (v = v.action) == null ? void 0 : v.active,
      disabled: (y = (e.vars || e).palette) == null || (y = y.action) == null ? void 0 : y.disabled,
      inherit: void 0
    }[t.color]
  };
}), Kh = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = Fe({
    props: t,
    name: "MuiSvgIcon"
  }), {
    children: o,
    className: i,
    color: l = "inherit",
    component: s = "svg",
    fontSize: a = "medium",
    htmlColor: u,
    inheritViewBox: c = !1,
    titleAccess: f,
    viewBox: p = "0 0 24 24"
  } = r, v = W(r, Z2), y = /* @__PURE__ */ C.isValidElement(o) && o.type === "svg", g = S({}, r, {
    color: l,
    component: s,
    fontSize: a,
    instanceFontSize: t.fontSize,
    inheritViewBox: c,
    viewBox: p,
    hasSvgAsChild: y
  }), _ = {};
  c || (_.viewBox = p);
  const m = q2(g);
  return /* @__PURE__ */ $.jsxs(J2, S({
    as: s,
    className: J(m.root, i),
    focusable: "false",
    color: u,
    "aria-hidden": f ? void 0 : !0,
    role: f ? "img" : void 0,
    ref: n
  }, _, v, y && o.props, {
    ownerState: g,
    children: [y ? o.props.children : o, f ? /* @__PURE__ */ $.jsx("title", {
      children: f
    }) : null]
  }));
});
Kh.muiName = "SvgIcon";
const $d = Kh;
function Mr(e, t) {
  function n(r, o) {
    return /* @__PURE__ */ $.jsx($d, S({
      "data-testid": `${t}Icon`,
      ref: o
    }, r, {
      children: e
    }));
  }
  return n.muiName = $d.muiName, /* @__PURE__ */ C.memo(/* @__PURE__ */ C.forwardRef(n));
}
const ek = Mr(/* @__PURE__ */ $.jsx("path", {
  d: "M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2, 4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0, 0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"
}), "SuccessOutlined"), tk = Mr(/* @__PURE__ */ $.jsx("path", {
  d: "M12 5.99L19.53 19H4.47L12 5.99M12 2L1 21h22L12 2zm1 14h-2v2h2v-2zm0-6h-2v4h2v-4z"
}), "ReportProblemOutlined"), nk = Mr(/* @__PURE__ */ $.jsx("path", {
  d: "M11 15h2v2h-2zm0-8h2v6h-2zm.99-5C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"
}), "ErrorOutline"), rk = Mr(/* @__PURE__ */ $.jsx("path", {
  d: "M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"
}), "InfoOutlined"), ok = Mr(/* @__PURE__ */ $.jsx("path", {
  d: "M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
}), "Close"), ik = ["action", "children", "className", "closeText", "color", "components", "componentsProps", "icon", "iconMapping", "onClose", "role", "severity", "slotProps", "slots", "variant"], lk = (e) => {
  const {
    variant: t,
    color: n,
    severity: r,
    classes: o
  } = e, i = {
    root: ["root", `color${X(n || r)}`, `${t}${X(n || r)}`, `${t}`],
    icon: ["icon"],
    message: ["message"],
    action: ["action"]
  };
  return ot(i, p2, o);
}, sk = oe(Uh, {
  name: "MuiAlert",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[n.variant], t[`${n.variant}${X(n.color || n.severity)}`]];
  }
})(({
  theme: e
}) => {
  const t = e.palette.mode === "light" ? Ka : Ga, n = e.palette.mode === "light" ? Ga : Ka;
  return S({}, e.typography.body2, {
    backgroundColor: "transparent",
    display: "flex",
    padding: "6px 16px",
    variants: [...Object.entries(e.palette).filter(([, r]) => r.main && r.light).map(([r]) => ({
      props: {
        colorSeverity: r,
        variant: "standard"
      },
      style: {
        color: e.vars ? e.vars.palette.Alert[`${r}Color`] : t(e.palette[r].light, 0.6),
        backgroundColor: e.vars ? e.vars.palette.Alert[`${r}StandardBg`] : n(e.palette[r].light, 0.9),
        [`& .${Sd.icon}`]: e.vars ? {
          color: e.vars.palette.Alert[`${r}IconColor`]
        } : {
          color: e.palette[r].main
        }
      }
    })), ...Object.entries(e.palette).filter(([, r]) => r.main && r.light).map(([r]) => ({
      props: {
        colorSeverity: r,
        variant: "outlined"
      },
      style: {
        color: e.vars ? e.vars.palette.Alert[`${r}Color`] : t(e.palette[r].light, 0.6),
        border: `1px solid ${(e.vars || e).palette[r].light}`,
        [`& .${Sd.icon}`]: e.vars ? {
          color: e.vars.palette.Alert[`${r}IconColor`]
        } : {
          color: e.palette[r].main
        }
      }
    })), ...Object.entries(e.palette).filter(([, r]) => r.main && r.dark).map(([r]) => ({
      props: {
        colorSeverity: r,
        variant: "filled"
      },
      style: S({
        fontWeight: e.typography.fontWeightMedium
      }, e.vars ? {
        color: e.vars.palette.Alert[`${r}FilledColor`],
        backgroundColor: e.vars.palette.Alert[`${r}FilledBg`]
      } : {
        backgroundColor: e.palette.mode === "dark" ? e.palette[r].dark : e.palette[r].main,
        color: e.palette.getContrastText(e.palette[r].main)
      })
    }))]
  });
}), ak = oe("div", {
  name: "MuiAlert",
  slot: "Icon",
  overridesResolver: (e, t) => t.icon
})({
  marginRight: 12,
  padding: "7px 0",
  display: "flex",
  fontSize: 22,
  opacity: 0.9
}), uk = oe("div", {
  name: "MuiAlert",
  slot: "Message",
  overridesResolver: (e, t) => t.message
})({
  padding: "8px 0",
  minWidth: 0,
  overflow: "auto"
}), Pd = oe("div", {
  name: "MuiAlert",
  slot: "Action",
  overridesResolver: (e, t) => t.action
})({
  display: "flex",
  alignItems: "flex-start",
  padding: "4px 0 0 16px",
  marginLeft: "auto",
  marginRight: -8
}), Td = {
  success: /* @__PURE__ */ $.jsx(ek, {
    fontSize: "inherit"
  }),
  warning: /* @__PURE__ */ $.jsx(tk, {
    fontSize: "inherit"
  }),
  error: /* @__PURE__ */ $.jsx(nk, {
    fontSize: "inherit"
  }),
  info: /* @__PURE__ */ $.jsx(rk, {
    fontSize: "inherit"
  })
}, ck = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = Fe({
    props: t,
    name: "MuiAlert"
  }), {
    action: o,
    children: i,
    className: l,
    closeText: s = "Close",
    color: a,
    components: u = {},
    componentsProps: c = {},
    icon: f,
    iconMapping: p = Td,
    onClose: v,
    role: y = "alert",
    severity: g = "success",
    slotProps: _ = {},
    slots: m = {},
    variant: d = "standard"
  } = r, h = W(r, ik), x = S({}, r, {
    color: a,
    severity: g,
    variant: d,
    colorSeverity: a || g
  }), E = lk(x), k = {
    slots: S({
      closeButton: u.CloseButton,
      closeIcon: u.CloseIcon
    }, m),
    slotProps: S({}, c, _)
  }, [w, T] = xd("closeButton", {
    elementType: Hh,
    externalForwardedProps: k,
    ownerState: x
  }), [N, O] = xd("closeIcon", {
    elementType: ok,
    externalForwardedProps: k,
    ownerState: x
  });
  return /* @__PURE__ */ $.jsxs(sk, S({
    role: y,
    elevation: 0,
    ownerState: x,
    className: J(E.root, l),
    ref: n
  }, h, {
    children: [f !== !1 ? /* @__PURE__ */ $.jsx(ak, {
      ownerState: x,
      className: E.icon,
      children: f || p[g] || Td[g]
    }) : null, /* @__PURE__ */ $.jsx(uk, {
      ownerState: x,
      className: E.message,
      children: i
    }), o != null ? /* @__PURE__ */ $.jsx(Pd, {
      ownerState: x,
      className: E.action,
      children: o
    }) : null, o == null && v ? /* @__PURE__ */ $.jsx(Pd, {
      ownerState: x,
      className: E.action,
      children: /* @__PURE__ */ $.jsx(w, S({
        size: "small",
        "aria-label": s,
        title: s,
        color: "inherit",
        onClick: v
      }, T, {
        children: /* @__PURE__ */ $.jsx(N, S({
          fontSize: "small"
        }, O))
      }))
    }) : null]
  }));
}), fk = ck, dk = Qe("MuiBox", ["root"]), pk = dk, mk = gc(), hk = nx({
  themeId: wr,
  defaultTheme: mk,
  defaultClassName: pk.root,
  generateClassName: ac.generate
}), ln = hk;
function gk(e) {
  return Ge("MuiCard", e);
}
Qe("MuiCard", ["root"]);
const yk = ["className", "raised"], vk = (e) => {
  const {
    classes: t
  } = e;
  return ot({
    root: ["root"]
  }, gk, t);
}, xk = oe(Uh, {
  name: "MuiCard",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})(() => ({
  overflow: "hidden"
})), Sk = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = Fe({
    props: t,
    name: "MuiCard"
  }), {
    className: o,
    raised: i = !1
  } = r, l = W(r, yk), s = S({}, r, {
    raised: i
  }), a = vk(s);
  return /* @__PURE__ */ $.jsx(xk, S({
    className: J(a.root, o),
    elevation: i ? 8 : void 0,
    ref: n,
    ownerState: s
  }, l));
}), Gh = Sk;
function wk(e) {
  return Ge("MuiCardContent", e);
}
Qe("MuiCardContent", ["root"]);
const kk = ["className", "component"], Ck = (e) => {
  const {
    classes: t
  } = e;
  return ot({
    root: ["root"]
  }, wk, t);
}, Ek = oe("div", {
  name: "MuiCardContent",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})(() => ({
  padding: 16,
  "&:last-child": {
    paddingBottom: 24
  }
})), _k = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = Fe({
    props: t,
    name: "MuiCardContent"
  }), {
    className: o,
    component: i = "div"
  } = r, l = W(r, kk), s = S({}, r, {
    component: i
  }), a = Ck(s);
  return /* @__PURE__ */ $.jsx(Ek, S({
    as: i,
    className: J(a.root, o),
    ownerState: s,
    ref: n
  }, l));
}), Qh = _k;
function Rd(e, t) {
  var n, r;
  const {
    timeout: o,
    easing: i,
    style: l = {}
  } = e;
  return {
    duration: (n = l.transitionDuration) != null ? n : typeof o == "number" ? o : o[t.mode] || 0,
    easing: (r = l.transitionTimingFunction) != null ? r : typeof i == "object" ? i[t.mode] : i,
    delay: l.transitionDelay
  };
}
const $k = {
  configure: (e) => {
    ac.configure(e);
  }
}, Pk = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  capitalize: X,
  createChainedFunction: _x,
  createSvgIcon: Mr,
  debounce: $x,
  deprecatedPropType: Px,
  isMuiElement: Tx,
  ownerDocument: _h,
  ownerWindow: Rx,
  requirePropFactory: Ox,
  setRef: $h,
  unstable_ClassNameGenerator: $k,
  unstable_useEnhancedEffect: fc,
  unstable_useId: Ph,
  unsupportedProp: Nx,
  useControlled: zx,
  useEventCallback: Qr,
  useForkRef: To,
  useIsFocusVisible: Rh
}, Symbol.toStringTag, { value: "Module" }));
function Tk(e) {
  return Ge("MuiCollapse", e);
}
Qe("MuiCollapse", ["root", "horizontal", "vertical", "entered", "hidden", "wrapper", "wrapperInner"]);
const Rk = ["addEndListener", "children", "className", "collapsedSize", "component", "easing", "in", "onEnter", "onEntered", "onEntering", "onExit", "onExited", "onExiting", "orientation", "style", "timeout", "TransitionComponent"], Ok = (e) => {
  const {
    orientation: t,
    classes: n
  } = e, r = {
    root: ["root", `${t}`],
    entered: ["entered"],
    hidden: ["hidden"],
    wrapper: ["wrapper", `${t}`],
    wrapperInner: ["wrapperInner", `${t}`]
  };
  return ot(r, Tk, n);
}, Mk = oe("div", {
  name: "MuiCollapse",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[n.orientation], n.state === "entered" && t.entered, n.state === "exited" && !n.in && n.collapsedSize === "0px" && t.hidden];
  }
})(({
  theme: e,
  ownerState: t
}) => S({
  height: 0,
  overflow: "hidden",
  transition: e.transitions.create("height")
}, t.orientation === "horizontal" && {
  height: "auto",
  width: 0,
  transition: e.transitions.create("width")
}, t.state === "entered" && S({
  height: "auto",
  overflow: "visible"
}, t.orientation === "horizontal" && {
  width: "auto"
}), t.state === "exited" && !t.in && t.collapsedSize === "0px" && {
  visibility: "hidden"
})), Nk = oe("div", {
  name: "MuiCollapse",
  slot: "Wrapper",
  overridesResolver: (e, t) => t.wrapper
})(({
  ownerState: e
}) => S({
  // Hack to get children with a negative margin to not falsify the height computation.
  display: "flex",
  width: "100%"
}, e.orientation === "horizontal" && {
  width: "auto",
  height: "100%"
})), zk = oe("div", {
  name: "MuiCollapse",
  slot: "WrapperInner",
  overridesResolver: (e, t) => t.wrapperInner
})(({
  ownerState: e
}) => S({
  width: "100%"
}, e.orientation === "horizontal" && {
  width: "auto",
  height: "100%"
})), Yh = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = Fe({
    props: t,
    name: "MuiCollapse"
  }), {
    addEndListener: o,
    children: i,
    className: l,
    collapsedSize: s = "0px",
    component: a,
    easing: u,
    in: c,
    onEnter: f,
    onEntered: p,
    onEntering: v,
    onExit: y,
    onExited: g,
    onExiting: _,
    orientation: m = "vertical",
    style: d,
    timeout: h = Fh.standard,
    // eslint-disable-next-line react/prop-types
    TransitionComponent: x = g2
  } = r, E = W(r, Rk), k = S({}, r, {
    orientation: m,
    collapsedSize: s
  }), w = Ok(k), T = Bh(), N = Th(), O = C.useRef(null), F = C.useRef(), A = typeof s == "number" ? `${s}px` : s, L = m === "horizontal", U = L ? "width" : "height", te = C.useRef(null), ve = To(n, te), he = (j) => (xe) => {
    if (j) {
      const vt = te.current;
      xe === void 0 ? j(vt) : j(vt, xe);
    }
  }, R = () => O.current ? O.current[L ? "clientWidth" : "clientHeight"] : 0, z = he((j, xe) => {
    O.current && L && (O.current.style.position = "absolute"), j.style[U] = A, f && f(j, xe);
  }), I = he((j, xe) => {
    const vt = R();
    O.current && L && (O.current.style.position = "");
    const {
      duration: je,
      easing: bn
    } = Rd({
      style: d,
      timeout: h,
      easing: u
    }, {
      mode: "enter"
    });
    if (h === "auto") {
      const Ho = T.transitions.getAutoHeightDuration(vt);
      j.style.transitionDuration = `${Ho}ms`, F.current = Ho;
    } else
      j.style.transitionDuration = typeof je == "string" ? je : `${je}ms`;
    j.style[U] = `${vt}px`, j.style.transitionTimingFunction = bn, v && v(j, xe);
  }), Z = he((j, xe) => {
    j.style[U] = "auto", p && p(j, xe);
  }), ae = he((j) => {
    j.style[U] = `${R()}px`, y && y(j);
  }), Xt = he(g), _e = he((j) => {
    const xe = R(), {
      duration: vt,
      easing: je
    } = Rd({
      style: d,
      timeout: h,
      easing: u
    }, {
      mode: "exit"
    });
    if (h === "auto") {
      const bn = T.transitions.getAutoHeightDuration(xe);
      j.style.transitionDuration = `${bn}ms`, F.current = bn;
    } else
      j.style.transitionDuration = typeof vt == "string" ? vt : `${vt}ms`;
    j.style[U] = A, j.style.transitionTimingFunction = je, _ && _(j);
  }), Pt = (j) => {
    h === "auto" && N.start(F.current || 0, j), o && o(te.current, j);
  };
  return /* @__PURE__ */ $.jsx(x, S({
    in: c,
    onEnter: z,
    onEntered: Z,
    onEntering: I,
    onExit: ae,
    onExited: Xt,
    onExiting: _e,
    addEndListener: Pt,
    nodeRef: te,
    timeout: h === "auto" ? null : h
  }, E, {
    children: (j, xe) => /* @__PURE__ */ $.jsx(Mk, S({
      as: a,
      className: J(w.root, l, {
        entered: w.entered,
        exited: !c && A === "0px" && w.hidden
      }[j]),
      style: S({
        [L ? "minWidth" : "minHeight"]: A
      }, d),
      ref: ve
    }, xe, {
      // `ownerState` is set after `childProps` to override any existing `ownerState` property in `childProps`
      // that might have been forwarded from the Transition component.
      ownerState: S({}, k, {
        state: j
      }),
      children: /* @__PURE__ */ $.jsx(Nk, {
        ownerState: S({}, k, {
          state: j
        }),
        className: w.wrapper,
        ref: O,
        children: /* @__PURE__ */ $.jsx(zk, {
          ownerState: S({}, k, {
            state: j
          }),
          className: w.wrapperInner,
          children: i
        })
      })
    }))
  }));
});
Yh.muiSupportAuto = !0;
const Lk = Yh;
var Sc = {}, Hs = {};
const jk = /* @__PURE__ */ Gt(Pk);
var Od;
function Ik() {
  return Od || (Od = 1, function(e) {
    "use client";
    Object.defineProperty(e, "__esModule", {
      value: !0
    }), Object.defineProperty(e, "default", {
      enumerable: !0,
      get: function() {
        return t.createSvgIcon;
      }
    });
    var t = jk;
  }(Hs)), Hs;
}
var Ak = dc;
Object.defineProperty(Sc, "__esModule", {
  value: !0
});
var Xh = Sc.default = void 0, bk = Ak(Ik()), Dk = $;
Xh = Sc.default = (0, bk.default)(/* @__PURE__ */ (0, Dk.jsx)("path", {
  d: "M16.59 8.59 12 13.17 7.41 8.59 6 10l6 6 6-6z"
}), "ExpandMore");
function Fk(e) {
  return Ge("MuiDivider", e);
}
Qe("MuiDivider", ["root", "absolute", "fullWidth", "inset", "middle", "flexItem", "light", "vertical", "withChildren", "withChildrenVertical", "textAlignRight", "textAlignLeft", "wrapper", "wrapperVertical"]);
const Bk = ["absolute", "children", "className", "component", "flexItem", "light", "orientation", "role", "textAlign", "variant"], Wk = (e) => {
  const {
    absolute: t,
    children: n,
    classes: r,
    flexItem: o,
    light: i,
    orientation: l,
    textAlign: s,
    variant: a
  } = e;
  return ot({
    root: ["root", t && "absolute", a, i && "light", l === "vertical" && "vertical", o && "flexItem", n && "withChildren", n && l === "vertical" && "withChildrenVertical", s === "right" && l !== "vertical" && "textAlignRight", s === "left" && l !== "vertical" && "textAlignLeft"],
    wrapper: ["wrapper", l === "vertical" && "wrapperVertical"]
  }, Fk, r);
}, Uk = oe("div", {
  name: "MuiDivider",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.absolute && t.absolute, t[n.variant], n.light && t.light, n.orientation === "vertical" && t.vertical, n.flexItem && t.flexItem, n.children && t.withChildren, n.children && n.orientation === "vertical" && t.withChildrenVertical, n.textAlign === "right" && n.orientation !== "vertical" && t.textAlignRight, n.textAlign === "left" && n.orientation !== "vertical" && t.textAlignLeft];
  }
})(({
  theme: e,
  ownerState: t
}) => S({
  margin: 0,
  // Reset browser default style.
  flexShrink: 0,
  borderWidth: 0,
  borderStyle: "solid",
  borderColor: (e.vars || e).palette.divider,
  borderBottomWidth: "thin"
}, t.absolute && {
  position: "absolute",
  bottom: 0,
  left: 0,
  width: "100%"
}, t.light && {
  borderColor: e.vars ? `rgba(${e.vars.palette.dividerChannel} / 0.08)` : Ro(e.palette.divider, 0.08)
}, t.variant === "inset" && {
  marginLeft: 72
}, t.variant === "middle" && t.orientation === "horizontal" && {
  marginLeft: e.spacing(2),
  marginRight: e.spacing(2)
}, t.variant === "middle" && t.orientation === "vertical" && {
  marginTop: e.spacing(1),
  marginBottom: e.spacing(1)
}, t.orientation === "vertical" && {
  height: "100%",
  borderBottomWidth: 0,
  borderRightWidth: "thin"
}, t.flexItem && {
  alignSelf: "stretch",
  height: "auto"
}), ({
  ownerState: e
}) => S({}, e.children && {
  display: "flex",
  whiteSpace: "nowrap",
  textAlign: "center",
  border: 0,
  borderTopStyle: "solid",
  borderLeftStyle: "solid",
  "&::before, &::after": {
    content: '""',
    alignSelf: "center"
  }
}), ({
  theme: e,
  ownerState: t
}) => S({}, t.children && t.orientation !== "vertical" && {
  "&::before, &::after": {
    width: "100%",
    borderTop: `thin solid ${(e.vars || e).palette.divider}`,
    borderTopStyle: "inherit"
  }
}), ({
  theme: e,
  ownerState: t
}) => S({}, t.children && t.orientation === "vertical" && {
  flexDirection: "column",
  "&::before, &::after": {
    height: "100%",
    borderLeft: `thin solid ${(e.vars || e).palette.divider}`,
    borderLeftStyle: "inherit"
  }
}), ({
  ownerState: e
}) => S({}, e.textAlign === "right" && e.orientation !== "vertical" && {
  "&::before": {
    width: "90%"
  },
  "&::after": {
    width: "10%"
  }
}, e.textAlign === "left" && e.orientation !== "vertical" && {
  "&::before": {
    width: "10%"
  },
  "&::after": {
    width: "90%"
  }
})), Vk = oe("span", {
  name: "MuiDivider",
  slot: "Wrapper",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.wrapper, n.orientation === "vertical" && t.wrapperVertical];
  }
})(({
  theme: e,
  ownerState: t
}) => S({
  display: "inline-block",
  paddingLeft: `calc(${e.spacing(1)} * 1.2)`,
  paddingRight: `calc(${e.spacing(1)} * 1.2)`
}, t.orientation === "vertical" && {
  paddingTop: `calc(${e.spacing(1)} * 1.2)`,
  paddingBottom: `calc(${e.spacing(1)} * 1.2)`
})), Zh = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = Fe({
    props: t,
    name: "MuiDivider"
  }), {
    absolute: o = !1,
    children: i,
    className: l,
    component: s = i ? "div" : "hr",
    flexItem: a = !1,
    light: u = !1,
    orientation: c = "horizontal",
    role: f = s !== "hr" ? "separator" : void 0,
    textAlign: p = "center",
    variant: v = "fullWidth"
  } = r, y = W(r, Bk), g = S({}, r, {
    absolute: o,
    component: s,
    flexItem: a,
    light: u,
    orientation: c,
    role: f,
    textAlign: p,
    variant: v
  }), _ = Wk(g);
  return /* @__PURE__ */ $.jsx(Uk, S({
    as: s,
    className: J(_.root, l),
    role: f,
    ref: n,
    ownerState: g
  }, y, {
    children: i ? /* @__PURE__ */ $.jsx(Vk, {
      className: _.wrapper,
      ownerState: g,
      children: i
    }) : null
  }));
});
Zh.muiSkipListHighlight = !0;
const Hk = Zh, Kk = /* @__PURE__ */ C.createContext(), Md = Kk;
function Gk(e) {
  return Ge("MuiGrid", e);
}
const Qk = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], Yk = ["column-reverse", "column", "row-reverse", "row"], Xk = ["nowrap", "wrap-reverse", "wrap"], Ur = ["auto", !0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], Zk = Qe("MuiGrid", [
  "root",
  "container",
  "item",
  "zeroMinWidth",
  // spacings
  ...Qk.map((e) => `spacing-xs-${e}`),
  // direction values
  ...Yk.map((e) => `direction-xs-${e}`),
  // wrap values
  ...Xk.map((e) => `wrap-xs-${e}`),
  // grid sizes for all breakpoints
  ...Ur.map((e) => `grid-xs-${e}`),
  ...Ur.map((e) => `grid-sm-${e}`),
  ...Ur.map((e) => `grid-md-${e}`),
  ...Ur.map((e) => `grid-lg-${e}`),
  ...Ur.map((e) => `grid-xl-${e}`)
]), Mo = Zk, qk = ["className", "columns", "columnSpacing", "component", "container", "direction", "item", "rowSpacing", "spacing", "wrap", "zeroMinWidth"];
function pr(e) {
  const t = parseFloat(e);
  return `${t}${String(e).replace(String(t), "") || "px"}`;
}
function Jk({
  theme: e,
  ownerState: t
}) {
  let n;
  return e.breakpoints.keys.reduce((r, o) => {
    let i = {};
    if (t[o] && (n = t[o]), !n)
      return r;
    if (n === !0)
      i = {
        flexBasis: 0,
        flexGrow: 1,
        maxWidth: "100%"
      };
    else if (n === "auto")
      i = {
        flexBasis: "auto",
        flexGrow: 0,
        flexShrink: 0,
        maxWidth: "none",
        width: "auto"
      };
    else {
      const l = Fl({
        values: t.columns,
        breakpoints: e.breakpoints.values
      }), s = typeof l == "object" ? l[o] : l;
      if (s == null)
        return r;
      const a = `${Math.round(n / s * 1e8) / 1e6}%`;
      let u = {};
      if (t.container && t.item && t.columnSpacing !== 0) {
        const c = e.spacing(t.columnSpacing);
        if (c !== "0px") {
          const f = `calc(${a} + ${pr(c)})`;
          u = {
            flexBasis: f,
            maxWidth: f
          };
        }
      }
      i = S({
        flexBasis: a,
        flexGrow: 0,
        maxWidth: a
      }, u);
    }
    return e.breakpoints.values[o] === 0 ? Object.assign(r, i) : r[e.breakpoints.up(o)] = i, r;
  }, {});
}
function eC({
  theme: e,
  ownerState: t
}) {
  const n = Fl({
    values: t.direction,
    breakpoints: e.breakpoints.values
  });
  return mt({
    theme: e
  }, n, (r) => {
    const o = {
      flexDirection: r
    };
    return r.indexOf("column") === 0 && (o[`& > .${Mo.item}`] = {
      maxWidth: "none"
    }), o;
  });
}
function qh({
  breakpoints: e,
  values: t
}) {
  let n = "";
  Object.keys(t).forEach((o) => {
    n === "" && t[o] !== 0 && (n = o);
  });
  const r = Object.keys(e).sort((o, i) => e[o] - e[i]);
  return r.slice(0, r.indexOf(n));
}
function tC({
  theme: e,
  ownerState: t
}) {
  const {
    container: n,
    rowSpacing: r
  } = t;
  let o = {};
  if (n && r !== 0) {
    const i = Fl({
      values: r,
      breakpoints: e.breakpoints.values
    });
    let l;
    typeof i == "object" && (l = qh({
      breakpoints: e.breakpoints.values,
      values: i
    })), o = mt({
      theme: e
    }, i, (s, a) => {
      var u;
      const c = e.spacing(s);
      return c !== "0px" ? {
        marginTop: `-${pr(c)}`,
        [`& > .${Mo.item}`]: {
          paddingTop: pr(c)
        }
      } : (u = l) != null && u.includes(a) ? {} : {
        marginTop: 0,
        [`& > .${Mo.item}`]: {
          paddingTop: 0
        }
      };
    });
  }
  return o;
}
function nC({
  theme: e,
  ownerState: t
}) {
  const {
    container: n,
    columnSpacing: r
  } = t;
  let o = {};
  if (n && r !== 0) {
    const i = Fl({
      values: r,
      breakpoints: e.breakpoints.values
    });
    let l;
    typeof i == "object" && (l = qh({
      breakpoints: e.breakpoints.values,
      values: i
    })), o = mt({
      theme: e
    }, i, (s, a) => {
      var u;
      const c = e.spacing(s);
      return c !== "0px" ? {
        width: `calc(100% + ${pr(c)})`,
        marginLeft: `-${pr(c)}`,
        [`& > .${Mo.item}`]: {
          paddingLeft: pr(c)
        }
      } : (u = l) != null && u.includes(a) ? {} : {
        width: "100%",
        marginLeft: 0,
        [`& > .${Mo.item}`]: {
          paddingLeft: 0
        }
      };
    });
  }
  return o;
}
function rC(e, t, n = {}) {
  if (!e || e <= 0)
    return [];
  if (typeof e == "string" && !Number.isNaN(Number(e)) || typeof e == "number")
    return [n[`spacing-xs-${String(e)}`]];
  const r = [];
  return t.forEach((o) => {
    const i = e[o];
    Number(i) > 0 && r.push(n[`spacing-${o}-${String(i)}`]);
  }), r;
}
const oC = oe("div", {
  name: "MuiGrid",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e, {
      container: r,
      direction: o,
      item: i,
      spacing: l,
      wrap: s,
      zeroMinWidth: a,
      breakpoints: u
    } = n;
    let c = [];
    r && (c = rC(l, u, t));
    const f = [];
    return u.forEach((p) => {
      const v = n[p];
      v && f.push(t[`grid-${p}-${String(v)}`]);
    }), [t.root, r && t.container, i && t.item, a && t.zeroMinWidth, ...c, o !== "row" && t[`direction-xs-${String(o)}`], s !== "wrap" && t[`wrap-xs-${String(s)}`], ...f];
  }
})(({
  ownerState: e
}) => S({
  boxSizing: "border-box"
}, e.container && {
  display: "flex",
  flexWrap: "wrap",
  width: "100%"
}, e.item && {
  margin: 0
  // For instance, it's useful when used with a `figure` element.
}, e.zeroMinWidth && {
  minWidth: 0
}, e.wrap !== "wrap" && {
  flexWrap: e.wrap
}), eC, tC, nC, Jk);
function iC(e, t) {
  if (!e || e <= 0)
    return [];
  if (typeof e == "string" && !Number.isNaN(Number(e)) || typeof e == "number")
    return [`spacing-xs-${String(e)}`];
  const n = [];
  return t.forEach((r) => {
    const o = e[r];
    if (Number(o) > 0) {
      const i = `spacing-${r}-${String(o)}`;
      n.push(i);
    }
  }), n;
}
const lC = (e) => {
  const {
    classes: t,
    container: n,
    direction: r,
    item: o,
    spacing: i,
    wrap: l,
    zeroMinWidth: s,
    breakpoints: a
  } = e;
  let u = [];
  n && (u = iC(i, a));
  const c = [];
  a.forEach((p) => {
    const v = e[p];
    v && c.push(`grid-${p}-${String(v)}`);
  });
  const f = {
    root: ["root", n && "container", o && "item", s && "zeroMinWidth", ...u, r !== "row" && `direction-xs-${String(r)}`, l !== "wrap" && `wrap-xs-${String(l)}`, ...c]
  };
  return ot(f, Gk, t);
}, sC = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = Fe({
    props: t,
    name: "MuiGrid"
  }), {
    breakpoints: o
  } = Bh(), i = Ql(r), {
    className: l,
    columns: s,
    columnSpacing: a,
    component: u = "div",
    container: c = !1,
    direction: f = "row",
    item: p = !1,
    rowSpacing: v,
    spacing: y = 0,
    wrap: g = "wrap",
    zeroMinWidth: _ = !1
  } = i, m = W(i, qk), d = v || y, h = a || y, x = C.useContext(Md), E = c ? s || 12 : x, k = {}, w = S({}, m);
  o.keys.forEach((O) => {
    m[O] != null && (k[O] = m[O], delete w[O]);
  });
  const T = S({}, i, {
    columns: E,
    container: c,
    direction: f,
    item: p,
    rowSpacing: d,
    columnSpacing: h,
    wrap: g,
    zeroMinWidth: _,
    spacing: y
  }, k, {
    breakpoints: o.keys
  }), N = lC(T);
  return /* @__PURE__ */ $.jsx(Md.Provider, {
    value: E,
    children: /* @__PURE__ */ $.jsx(oC, S({
      ownerState: T,
      className: J(N.root, l),
      as: u,
      ref: n
    }, w))
  });
}), Ks = sC, aC = ({ devices: e }) => {
  const t = {
    Routing: e.filter((r) => {
      var o;
      return (o = r.model) == null ? void 0 : o.startsWith("MX");
    }),
    Switches: e.filter((r) => {
      var o;
      return (o = r.model) == null ? void 0 : o.startsWith("MS");
    }),
    Wireless: e.filter((r) => {
      var o;
      return (o = r.model) == null ? void 0 : o.startsWith("MR");
    }),
    Cameras: e.filter((r) => {
      var o;
      return (o = r.model) == null ? void 0 : o.startsWith("MV");
    })
  }, n = Object.entries(t).filter(([, r]) => r.length > 0);
  return /* @__PURE__ */ $.jsx(ln, { children: n.map(([r, o], i) => /* @__PURE__ */ $.jsxs(ln, { sx: { mb: i === n.length - 1 ? 0 : 3 }, children: [
    /* @__PURE__ */ $.jsx(On, { variant: "h6", sx: { mb: 1.5, color: "text.secondary" }, children: r }),
    /* @__PURE__ */ $.jsx(ln, { sx: { display: "flex", flexDirection: "column", gap: 1.5 }, children: o.map((l) => /* @__PURE__ */ $.jsx(
      ln,
      {
        sx: {
          p: 2,
          borderRadius: 1.5,
          backgroundColor: "rgba(0, 0, 0, 0.15)",
          border: "1px solid",
          borderColor: "rgba(255, 255, 255, 0.08)"
        },
        children: /* @__PURE__ */ $.jsxs(Ks, { container: !0, alignItems: "center", spacing: 2, children: [
          /* @__PURE__ */ $.jsx(Ks, { item: !0, xs: 12, sm: 6, children: /* @__PURE__ */ $.jsx(On, { variant: "body1", sx: { fontWeight: 500 }, children: l.name || "Unnamed Device" }) }),
          /* @__PURE__ */ $.jsx(Ks, { item: !0, xs: 12, sm: 6, sx: { textAlign: { sm: "right" } }, children: /* @__PURE__ */ $.jsxs(On, { variant: "body2", color: "text.secondary", children: [
            l.model,
            " (",
            l.mac,
            ")"
          ] }) })
        ] })
      },
      l.serial
    )) })
  ] }, r)) });
}, uC = oe((e) => {
  const { expand: t, ...n } = e;
  return /* @__PURE__ */ $.jsx(Hh, { ...n });
})(({ theme: e, expand: t }) => ({
  transform: t ? "rotate(180deg)" : "rotate(0deg)",
  marginLeft: "auto",
  color: e.palette.text.secondary,
  transition: e.transitions.create("transform", {
    duration: e.transitions.duration.shortest
  })
})), cC = ({ data: e }) => {
  const { networks: t = [], devices: n = [] } = e, [r, o] = C.useState(!1), i = (l) => {
    o(r === l ? !1 : l);
  };
  return /* @__PURE__ */ $.jsx(ln, { children: t.map((l) => {
    const s = n.filter((u) => u.networkId === l.id), a = r === l.id;
    return /* @__PURE__ */ $.jsxs(
      Gh,
      {
        sx: {
          mb: 2.5,
          borderRadius: 2,
          boxShadow: "none",
          border: "1px solid",
          borderColor: "rgba(255, 255, 255, 0.12)"
        },
        children: [
          /* @__PURE__ */ $.jsxs(
            ln,
            {
              sx: {
                display: "flex",
                alignItems: "center",
                cursor: "pointer",
                p: 2.5,
                "&:hover": {
                  backgroundColor: "rgba(255, 255, 255, 0.04)"
                }
              },
              onClick: () => i(l.id),
              children: [
                /* @__PURE__ */ $.jsx(On, { variant: "h5", component: "div", sx: { flexGrow: 1 }, children: l.name }),
                /* @__PURE__ */ $.jsx(
                  uC,
                  {
                    expand: a,
                    "aria-expanded": a,
                    "aria-label": "show more",
                    children: /* @__PURE__ */ $.jsx(Xh, {})
                  }
                )
              ]
            }
          ),
          /* @__PURE__ */ $.jsxs(Lk, { in: a, timeout: "auto", unmountOnExit: !0, children: [
            /* @__PURE__ */ $.jsx(Hk, { sx: { borderColor: "rgba(255, 255, 255, 0.12)" } }),
            /* @__PURE__ */ $.jsx(Qh, { sx: { p: 2.5 }, children: /* @__PURE__ */ $.jsx(aC, { devices: s }) })
          ] })
        ]
      },
      l.id
    );
  }) });
}, fC = () => /* @__PURE__ */ $.jsxs(ln, { sx: { mt: 4 }, children: [
  /* @__PURE__ */ $.jsx(On, { variant: "h5", component: "h2", sx: { mb: 2 }, children: "Event Log" }),
  /* @__PURE__ */ $.jsx(
    Gh,
    {
      sx: {
        borderRadius: 2,
        boxShadow: "none",
        border: "1px solid",
        borderColor: "rgba(255, 255, 255, 0.12)"
      },
      children: /* @__PURE__ */ $.jsx(Qh, { sx: { p: 2.5 }, children: /* @__PURE__ */ $.jsx(On, { color: "text.secondary", children: "Integration-specific events will be displayed here." }) })
    }
  )
] });
const dC = gc({
  palette: {
    mode: "dark",
    primary: {
      main: "#4fd1c5"
      // A modern teal
    },
    background: {
      default: "#1a202c",
      // A very dark slate blue
      paper: "#2d3748"
      // A dark slate blue
    },
    text: {
      primary: "#edf2f7",
      // A light gray
      secondary: "#a0aec0"
      // A medium gray
    }
  },
  typography: {
    fontFamily: "Roboto, sans-serif",
    h4: {
      fontWeight: 700
    },
    h5: {
      fontWeight: 600
    },
    h6: {
      fontWeight: 600
    }
  }
}), pC = ({ hass: e, config_entry_id: t }) => {
  const [n, r] = C.useState(null), [o, i] = C.useState(!0), [l, s] = C.useState(null);
  return C.useEffect(() => {
    if (!e || !e.connection) {
      s("Home Assistant connection object not found."), i(!1);
      return;
    }
    (async () => {
      try {
        const u = await e.connection.sendMessagePromise({
          type: "meraki_ha/get_config",
          config_entry_id: t
        });
        r(u);
      } catch (u) {
        console.error("Error fetching Meraki data:", u), s(`Failed to fetch Meraki data: ${u.message || "Unknown error"}`);
      } finally {
        i(!1);
      }
    })();
  }, [e, t]), /* @__PURE__ */ $.jsxs(zw, { theme: dC, children: [
    /* @__PURE__ */ $.jsx(Dw, {}),
    /* @__PURE__ */ $.jsxs(Bw, { maxWidth: "lg", sx: { mt: 4, mb: 4 }, children: [
      /* @__PURE__ */ $.jsx(On, { variant: "h4", component: "h1", gutterBottom: !0, children: "Meraki Control" }),
      o && /* @__PURE__ */ $.jsx(ln, { sx: { display: "flex", justifyContent: "center", p: 4 }, children: /* @__PURE__ */ $.jsx(o2, {}) }),
      l && /* @__PURE__ */ $.jsx(fk, { severity: "error", sx: { mt: 2 }, children: l }),
      !o && !l && n && /* @__PURE__ */ $.jsxs($.Fragment, { children: [
        /* @__PURE__ */ $.jsx(cC, { data: n }),
        /* @__PURE__ */ $.jsx(fC, {})
      ] })
    ] })
  ] });
};
class mC extends HTMLElement {
  constructor() {
    super(...arguments);
    Go(this, "_root");
    Go(this, "_hass");
    Go(this, "_panel");
  }
  connectedCallback() {
    this._root || (this._root = Qs.createRoot(this)), this._render();
  }
  disconnectedCallback() {
    this._root && (this._root.unmount(), this._root = void 0);
  }
  set hass(n) {
    this._hass = n, this._render();
  }
  set panel(n) {
    this._panel = n, this._render();
  }
  _render() {
    !this._root || !this._hass || !this._panel || this._root.render(
      /* @__PURE__ */ $.jsx(Ct.StrictMode, { children: /* @__PURE__ */ $.jsx(pC, { hass: this._hass, config_entry_id: this._panel.config.config_entry_id }) })
    );
  }
}
customElements.define("meraki-panel", mC);
