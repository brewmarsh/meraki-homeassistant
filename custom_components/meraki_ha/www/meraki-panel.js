var S0 = Object.defineProperty;
var w0 = (e, t, n) => t in e ? S0(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var Uo = (e, t, n) => (w0(e, typeof t != "symbol" ? t + "" : t, n), n);
function C0(e, t) {
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
function k0(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
function Kt(e) {
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
var Bf = { exports: {} }, sl = {}, Wf = { exports: {} }, D = {};
/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ro = Symbol.for("react.element"), _0 = Symbol.for("react.portal"), $0 = Symbol.for("react.fragment"), E0 = Symbol.for("react.strict_mode"), P0 = Symbol.for("react.profiler"), T0 = Symbol.for("react.provider"), R0 = Symbol.for("react.context"), M0 = Symbol.for("react.forward_ref"), O0 = Symbol.for("react.suspense"), z0 = Symbol.for("react.memo"), N0 = Symbol.for("react.lazy"), Tc = Symbol.iterator;
function j0(e) {
  return e === null || typeof e != "object" ? null : (e = Tc && e[Tc] || e["@@iterator"], typeof e == "function" ? e : null);
}
var Uf = { isMounted: function() {
  return !1;
}, enqueueForceUpdate: function() {
}, enqueueReplaceState: function() {
}, enqueueSetState: function() {
} }, Vf = Object.assign, Hf = {};
function xr(e, t, n) {
  this.props = e, this.context = t, this.refs = Hf, this.updater = n || Uf;
}
xr.prototype.isReactComponent = {};
xr.prototype.setState = function(e, t) {
  if (typeof e != "object" && typeof e != "function" && e != null)
    throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
  this.updater.enqueueSetState(this, e, t, "setState");
};
xr.prototype.forceUpdate = function(e) {
  this.updater.enqueueForceUpdate(this, e, "forceUpdate");
};
function Kf() {
}
Kf.prototype = xr.prototype;
function Ya(e, t, n) {
  this.props = e, this.context = t, this.refs = Hf, this.updater = n || Uf;
}
var Xa = Ya.prototype = new Kf();
Xa.constructor = Ya;
Vf(Xa, xr.prototype);
Xa.isPureReactComponent = !0;
var Rc = Array.isArray, Gf = Object.prototype.hasOwnProperty, qa = { current: null }, Qf = { key: !0, ref: !0, __self: !0, __source: !0 };
function Yf(e, t, n) {
  var r, o = {}, i = null, l = null;
  if (t != null)
    for (r in t.ref !== void 0 && (l = t.ref), t.key !== void 0 && (i = "" + t.key), t)
      Gf.call(t, r) && !Qf.hasOwnProperty(r) && (o[r] = t[r]);
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
  return { $$typeof: Ro, type: e, key: i, ref: l, props: o, _owner: qa.current };
}
function b0(e, t) {
  return { $$typeof: Ro, type: e.type, key: t, ref: e.ref, props: e.props, _owner: e._owner };
}
function Za(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Ro;
}
function A0(e) {
  var t = { "=": "=0", ":": "=2" };
  return "$" + e.replace(/[=:]/g, function(n) {
    return t[n];
  });
}
var Mc = /\/+/g;
function ds(e, t) {
  return typeof e == "object" && e !== null && e.key != null ? A0("" + e.key) : t.toString(36);
}
function di(e, t, n, r, o) {
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
          case Ro:
          case _0:
            l = !0;
        }
    }
  if (l)
    return l = e, o = o(l), e = r === "" ? "." + ds(l, 0) : r, Rc(o) ? (n = "", e != null && (n = e.replace(Mc, "$&/") + "/"), di(o, t, n, "", function(u) {
      return u;
    })) : o != null && (Za(o) && (o = b0(o, n + (!o.key || l && l.key === o.key ? "" : ("" + o.key).replace(Mc, "$&/") + "/") + e)), t.push(o)), 1;
  if (l = 0, r = r === "" ? "." : r + ":", Rc(e))
    for (var s = 0; s < e.length; s++) {
      i = e[s];
      var a = r + ds(i, s);
      l += di(i, t, n, a, o);
    }
  else if (a = j0(e), typeof a == "function")
    for (e = a.call(e), s = 0; !(i = e.next()).done; )
      i = i.value, a = r + ds(i, s++), l += di(i, t, n, a, o);
  else if (i === "object")
    throw t = String(e), Error("Objects are not valid as a React child (found: " + (t === "[object Object]" ? "object with keys {" + Object.keys(e).join(", ") + "}" : t) + "). If you meant to render a collection of children, use an array instead.");
  return l;
}
function Vo(e, t, n) {
  if (e == null)
    return e;
  var r = [], o = 0;
  return di(e, r, "", "", function(i) {
    return t.call(n, i, o++);
  }), r;
}
function I0(e) {
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
var De = { current: null }, fi = { transition: null }, L0 = { ReactCurrentDispatcher: De, ReactCurrentBatchConfig: fi, ReactCurrentOwner: qa };
function Xf() {
  throw Error("act(...) is not supported in production builds of React.");
}
D.Children = { map: Vo, forEach: function(e, t, n) {
  Vo(e, function() {
    t.apply(this, arguments);
  }, n);
}, count: function(e) {
  var t = 0;
  return Vo(e, function() {
    t++;
  }), t;
}, toArray: function(e) {
  return Vo(e, function(t) {
    return t;
  }) || [];
}, only: function(e) {
  if (!Za(e))
    throw Error("React.Children.only expected to receive a single React element child.");
  return e;
} };
D.Component = xr;
D.Fragment = $0;
D.Profiler = P0;
D.PureComponent = Ya;
D.StrictMode = E0;
D.Suspense = O0;
D.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = L0;
D.act = Xf;
D.cloneElement = function(e, t, n) {
  if (e == null)
    throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + e + ".");
  var r = Vf({}, e.props), o = e.key, i = e.ref, l = e._owner;
  if (t != null) {
    if (t.ref !== void 0 && (i = t.ref, l = qa.current), t.key !== void 0 && (o = "" + t.key), e.type && e.type.defaultProps)
      var s = e.type.defaultProps;
    for (a in t)
      Gf.call(t, a) && !Qf.hasOwnProperty(a) && (r[a] = t[a] === void 0 && s !== void 0 ? s[a] : t[a]);
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
  return { $$typeof: Ro, type: e.type, key: o, ref: i, props: r, _owner: l };
};
D.createContext = function(e) {
  return e = { $$typeof: R0, _currentValue: e, _currentValue2: e, _threadCount: 0, Provider: null, Consumer: null, _defaultValue: null, _globalName: null }, e.Provider = { $$typeof: T0, _context: e }, e.Consumer = e;
};
D.createElement = Yf;
D.createFactory = function(e) {
  var t = Yf.bind(null, e);
  return t.type = e, t;
};
D.createRef = function() {
  return { current: null };
};
D.forwardRef = function(e) {
  return { $$typeof: M0, render: e };
};
D.isValidElement = Za;
D.lazy = function(e) {
  return { $$typeof: N0, _payload: { _status: -1, _result: e }, _init: I0 };
};
D.memo = function(e, t) {
  return { $$typeof: z0, type: e, compare: t === void 0 ? null : t };
};
D.startTransition = function(e) {
  var t = fi.transition;
  fi.transition = {};
  try {
    e();
  } finally {
    fi.transition = t;
  }
};
D.unstable_act = Xf;
D.useCallback = function(e, t) {
  return De.current.useCallback(e, t);
};
D.useContext = function(e) {
  return De.current.useContext(e);
};
D.useDebugValue = function() {
};
D.useDeferredValue = function(e) {
  return De.current.useDeferredValue(e);
};
D.useEffect = function(e, t) {
  return De.current.useEffect(e, t);
};
D.useId = function() {
  return De.current.useId();
};
D.useImperativeHandle = function(e, t, n) {
  return De.current.useImperativeHandle(e, t, n);
};
D.useInsertionEffect = function(e, t) {
  return De.current.useInsertionEffect(e, t);
};
D.useLayoutEffect = function(e, t) {
  return De.current.useLayoutEffect(e, t);
};
D.useMemo = function(e, t) {
  return De.current.useMemo(e, t);
};
D.useReducer = function(e, t, n) {
  return De.current.useReducer(e, t, n);
};
D.useRef = function(e) {
  return De.current.useRef(e);
};
D.useState = function(e) {
  return De.current.useState(e);
};
D.useSyncExternalStore = function(e, t, n) {
  return De.current.useSyncExternalStore(e, t, n);
};
D.useTransition = function() {
  return De.current.useTransition();
};
D.version = "18.3.1";
Wf.exports = D;
var _ = Wf.exports;
const wn = /* @__PURE__ */ k0(_), Gs = /* @__PURE__ */ C0({
  __proto__: null,
  default: wn
}, [_]);
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var D0 = _, F0 = Symbol.for("react.element"), B0 = Symbol.for("react.fragment"), W0 = Object.prototype.hasOwnProperty, U0 = D0.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, V0 = { key: !0, ref: !0, __self: !0, __source: !0 };
function qf(e, t, n) {
  var r, o = {}, i = null, l = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (r in t)
    W0.call(t, r) && !V0.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps)
    for (r in t = e.defaultProps, t)
      o[r] === void 0 && (o[r] = t[r]);
  return { $$typeof: F0, type: e, key: i, ref: l, props: o, _owner: U0.current };
}
sl.Fragment = B0;
sl.jsx = qf;
sl.jsxs = qf;
Bf.exports = sl;
var x = Bf.exports, Qs = {}, Zf = { exports: {} }, et = {}, Jf = { exports: {} }, ep = {};
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
  function t(R, N) {
    var b = R.length;
    R.push(N);
    e:
      for (; 0 < b; ) {
        var ne = b - 1 >>> 1, pe = R[ne];
        if (0 < o(pe, N))
          R[ne] = N, R[b] = pe, b = ne;
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
    var N = R[0], b = R.pop();
    if (b !== N) {
      R[0] = b;
      e:
        for (var ne = 0, pe = R.length, bn = pe >>> 1; ne < bn; ) {
          var Ae = 2 * (ne + 1) - 1, Qt = R[Ae], vt = Ae + 1, An = R[vt];
          if (0 > o(Qt, b))
            vt < pe && 0 > o(An, Qt) ? (R[ne] = An, R[vt] = b, ne = vt) : (R[ne] = Qt, R[Ae] = b, ne = Ae);
          else if (vt < pe && 0 > o(An, b))
            R[ne] = An, R[vt] = b, ne = vt;
          else
            break e;
        }
    }
    return N;
  }
  function o(R, N) {
    var b = R.sortIndex - N.sortIndex;
    return b !== 0 ? b : R.id - N.id;
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
  var a = [], u = [], c = 1, f = null, p = 3, v = !1, y = !1, g = !1, E = typeof setTimeout == "function" ? setTimeout : null, m = typeof clearTimeout == "function" ? clearTimeout : null, d = typeof setImmediate < "u" ? setImmediate : null;
  typeof navigator < "u" && navigator.scheduling !== void 0 && navigator.scheduling.isInputPending !== void 0 && navigator.scheduling.isInputPending.bind(navigator.scheduling);
  function h(R) {
    for (var N = n(u); N !== null; ) {
      if (N.callback === null)
        r(u);
      else if (N.startTime <= R)
        r(u), N.sortIndex = N.expirationTime, t(a, N);
      else
        break;
      N = n(u);
    }
  }
  function S(R) {
    if (g = !1, h(R), !y)
      if (n(a) !== null)
        y = !0, Ee($);
      else {
        var N = n(u);
        N !== null && Ge(S, N.startTime - R);
      }
  }
  function $(R, N) {
    y = !1, g && (g = !1, m(T), T = -1), v = !0;
    var b = p;
    try {
      for (h(N), f = n(a); f !== null && (!(f.expirationTime > N) || R && !U()); ) {
        var ne = f.callback;
        if (typeof ne == "function") {
          f.callback = null, p = f.priorityLevel;
          var pe = ne(f.expirationTime <= N);
          N = e.unstable_now(), typeof pe == "function" ? f.callback = pe : f === n(a) && r(a), h(N);
        } else
          r(a);
        f = n(a);
      }
      if (f !== null)
        var bn = !0;
      else {
        var Ae = n(u);
        Ae !== null && Ge(S, Ae.startTime - N), bn = !1;
      }
      return bn;
    } finally {
      f = null, p = b, v = !1;
    }
  }
  var k = !1, C = null, T = -1, z = 5, M = -1;
  function U() {
    return !(e.unstable_now() - M < z);
  }
  function F() {
    if (C !== null) {
      var R = e.unstable_now();
      M = R;
      var N = !0;
      try {
        N = C(!0, R);
      } finally {
        N ? I() : (k = !1, C = null);
      }
    } else
      k = !1;
  }
  var I;
  if (typeof d == "function")
    I = function() {
      d(F);
    };
  else if (typeof MessageChannel < "u") {
    var q = new MessageChannel(), xe = q.port2;
    q.port1.onmessage = F, I = function() {
      xe.postMessage(null);
    };
  } else
    I = function() {
      E(F, 0);
    };
  function Ee(R) {
    C = R, k || (k = !0, I());
  }
  function Ge(R, N) {
    T = E(function() {
      R(e.unstable_now());
    }, N);
  }
  e.unstable_IdlePriority = 5, e.unstable_ImmediatePriority = 1, e.unstable_LowPriority = 4, e.unstable_NormalPriority = 3, e.unstable_Profiling = null, e.unstable_UserBlockingPriority = 2, e.unstable_cancelCallback = function(R) {
    R.callback = null;
  }, e.unstable_continueExecution = function() {
    y || v || (y = !0, Ee($));
  }, e.unstable_forceFrameRate = function(R) {
    0 > R || 125 < R ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : z = 0 < R ? Math.floor(1e3 / R) : 5;
  }, e.unstable_getCurrentPriorityLevel = function() {
    return p;
  }, e.unstable_getFirstCallbackNode = function() {
    return n(a);
  }, e.unstable_next = function(R) {
    switch (p) {
      case 1:
      case 2:
      case 3:
        var N = 3;
        break;
      default:
        N = p;
    }
    var b = p;
    p = N;
    try {
      return R();
    } finally {
      p = b;
    }
  }, e.unstable_pauseExecution = function() {
  }, e.unstable_requestPaint = function() {
  }, e.unstable_runWithPriority = function(R, N) {
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
    var b = p;
    p = R;
    try {
      return N();
    } finally {
      p = b;
    }
  }, e.unstable_scheduleCallback = function(R, N, b) {
    var ne = e.unstable_now();
    switch (typeof b == "object" && b !== null ? (b = b.delay, b = typeof b == "number" && 0 < b ? ne + b : ne) : b = ne, R) {
      case 1:
        var pe = -1;
        break;
      case 2:
        pe = 250;
        break;
      case 5:
        pe = 1073741823;
        break;
      case 4:
        pe = 1e4;
        break;
      default:
        pe = 5e3;
    }
    return pe = b + pe, R = { id: c++, callback: N, priorityLevel: R, startTime: b, expirationTime: pe, sortIndex: -1 }, b > ne ? (R.sortIndex = b, t(u, R), n(a) === null && R === n(u) && (g ? (m(T), T = -1) : g = !0, Ge(S, b - ne))) : (R.sortIndex = pe, t(a, R), y || v || (y = !0, Ee($))), R;
  }, e.unstable_shouldYield = U, e.unstable_wrapCallback = function(R) {
    var N = p;
    return function() {
      var b = p;
      p = N;
      try {
        return R.apply(this, arguments);
      } finally {
        p = b;
      }
    };
  };
})(ep);
Jf.exports = ep;
var H0 = Jf.exports;
/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var K0 = _, Je = H0;
function P(e) {
  for (var t = "https://reactjs.org/docs/error-decoder.html?invariant=" + e, n = 1; n < arguments.length; n++)
    t += "&args[]=" + encodeURIComponent(arguments[n]);
  return "Minified React error #" + e + "; visit " + t + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
}
var tp = /* @__PURE__ */ new Set(), ro = {};
function Nn(e, t) {
  cr(e, t), cr(e + "Capture", t);
}
function cr(e, t) {
  for (ro[e] = t, e = 0; e < t.length; e++)
    tp.add(t[e]);
}
var Wt = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), Ys = Object.prototype.hasOwnProperty, G0 = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, Oc = {}, zc = {};
function Q0(e) {
  return Ys.call(zc, e) ? !0 : Ys.call(Oc, e) ? !1 : G0.test(e) ? zc[e] = !0 : (Oc[e] = !0, !1);
}
function Y0(e, t, n, r) {
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
function X0(e, t, n, r) {
  if (t === null || typeof t > "u" || Y0(e, t, n, r))
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
function Fe(e, t, n, r, o, i, l) {
  this.acceptsBooleans = t === 2 || t === 3 || t === 4, this.attributeName = r, this.attributeNamespace = o, this.mustUseProperty = n, this.propertyName = e, this.type = t, this.sanitizeURL = i, this.removeEmptyString = l;
}
var Me = {};
"children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(e) {
  Me[e] = new Fe(e, 0, !1, e, null, !1, !1);
});
[["acceptCharset", "accept-charset"], ["className", "class"], ["htmlFor", "for"], ["httpEquiv", "http-equiv"]].forEach(function(e) {
  var t = e[0];
  Me[t] = new Fe(t, 1, !1, e[1], null, !1, !1);
});
["contentEditable", "draggable", "spellCheck", "value"].forEach(function(e) {
  Me[e] = new Fe(e, 2, !1, e.toLowerCase(), null, !1, !1);
});
["autoReverse", "externalResourcesRequired", "focusable", "preserveAlpha"].forEach(function(e) {
  Me[e] = new Fe(e, 2, !1, e, null, !1, !1);
});
"allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(e) {
  Me[e] = new Fe(e, 3, !1, e.toLowerCase(), null, !1, !1);
});
["checked", "multiple", "muted", "selected"].forEach(function(e) {
  Me[e] = new Fe(e, 3, !0, e, null, !1, !1);
});
["capture", "download"].forEach(function(e) {
  Me[e] = new Fe(e, 4, !1, e, null, !1, !1);
});
["cols", "rows", "size", "span"].forEach(function(e) {
  Me[e] = new Fe(e, 6, !1, e, null, !1, !1);
});
["rowSpan", "start"].forEach(function(e) {
  Me[e] = new Fe(e, 5, !1, e.toLowerCase(), null, !1, !1);
});
var Ja = /[\-:]([a-z])/g;
function eu(e) {
  return e[1].toUpperCase();
}
"accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(e) {
  var t = e.replace(
    Ja,
    eu
  );
  Me[t] = new Fe(t, 1, !1, e, null, !1, !1);
});
"xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(e) {
  var t = e.replace(Ja, eu);
  Me[t] = new Fe(t, 1, !1, e, "http://www.w3.org/1999/xlink", !1, !1);
});
["xml:base", "xml:lang", "xml:space"].forEach(function(e) {
  var t = e.replace(Ja, eu);
  Me[t] = new Fe(t, 1, !1, e, "http://www.w3.org/XML/1998/namespace", !1, !1);
});
["tabIndex", "crossOrigin"].forEach(function(e) {
  Me[e] = new Fe(e, 1, !1, e.toLowerCase(), null, !1, !1);
});
Me.xlinkHref = new Fe("xlinkHref", 1, !1, "xlink:href", "http://www.w3.org/1999/xlink", !0, !1);
["src", "href", "action", "formAction"].forEach(function(e) {
  Me[e] = new Fe(e, 1, !1, e.toLowerCase(), null, !0, !0);
});
function tu(e, t, n, r) {
  var o = Me.hasOwnProperty(t) ? Me[t] : null;
  (o !== null ? o.type !== 0 : r || !(2 < t.length) || t[0] !== "o" && t[0] !== "O" || t[1] !== "n" && t[1] !== "N") && (X0(t, n, o, r) && (n = null), r || o === null ? Q0(t) && (n === null ? e.removeAttribute(t) : e.setAttribute(t, "" + n)) : o.mustUseProperty ? e[o.propertyName] = n === null ? o.type === 3 ? !1 : "" : n : (t = o.attributeName, r = o.attributeNamespace, n === null ? e.removeAttribute(t) : (o = o.type, n = o === 3 || o === 4 && n === !0 ? "" : "" + n, r ? e.setAttributeNS(r, t, n) : e.setAttribute(t, n))));
}
var Gt = K0.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, Ho = Symbol.for("react.element"), Un = Symbol.for("react.portal"), Vn = Symbol.for("react.fragment"), nu = Symbol.for("react.strict_mode"), Xs = Symbol.for("react.profiler"), np = Symbol.for("react.provider"), rp = Symbol.for("react.context"), ru = Symbol.for("react.forward_ref"), qs = Symbol.for("react.suspense"), Zs = Symbol.for("react.suspense_list"), ou = Symbol.for("react.memo"), Zt = Symbol.for("react.lazy"), op = Symbol.for("react.offscreen"), Nc = Symbol.iterator;
function Mr(e) {
  return e === null || typeof e != "object" ? null : (e = Nc && e[Nc] || e["@@iterator"], typeof e == "function" ? e : null);
}
var ie = Object.assign, fs;
function Wr(e) {
  if (fs === void 0)
    try {
      throw Error();
    } catch (n) {
      var t = n.stack.trim().match(/\n( *(at )?)/);
      fs = t && t[1] || "";
    }
  return `
` + fs + e;
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
  return (e = e ? e.displayName || e.name : "") ? Wr(e) : "";
}
function q0(e) {
  switch (e.tag) {
    case 5:
      return Wr(e.type);
    case 16:
      return Wr("Lazy");
    case 13:
      return Wr("Suspense");
    case 19:
      return Wr("SuspenseList");
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
    case Vn:
      return "Fragment";
    case Un:
      return "Portal";
    case Xs:
      return "Profiler";
    case nu:
      return "StrictMode";
    case qs:
      return "Suspense";
    case Zs:
      return "SuspenseList";
  }
  if (typeof e == "object")
    switch (e.$$typeof) {
      case rp:
        return (e.displayName || "Context") + ".Consumer";
      case np:
        return (e._context.displayName || "Context") + ".Provider";
      case ru:
        var t = e.render;
        return e = e.displayName, e || (e = t.displayName || t.name || "", e = e !== "" ? "ForwardRef(" + e + ")" : "ForwardRef"), e;
      case ou:
        return t = e.displayName || null, t !== null ? t : Js(e.type) || "Memo";
      case Zt:
        t = e._payload, e = e._init;
        try {
          return Js(e(t));
        } catch {
        }
    }
  return null;
}
function Z0(e) {
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
      return t === nu ? "StrictMode" : "Mode";
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
function pn(e) {
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
function ip(e) {
  var t = e.type;
  return (e = e.nodeName) && e.toLowerCase() === "input" && (t === "checkbox" || t === "radio");
}
function J0(e) {
  var t = ip(e) ? "checked" : "value", n = Object.getOwnPropertyDescriptor(e.constructor.prototype, t), r = "" + e[t];
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
function Ko(e) {
  e._valueTracker || (e._valueTracker = J0(e));
}
function lp(e) {
  if (!e)
    return !1;
  var t = e._valueTracker;
  if (!t)
    return !0;
  var n = t.getValue(), r = "";
  return e && (r = ip(e) ? e.checked ? "true" : "false" : e.value), e = r, e !== n ? (t.setValue(e), !0) : !1;
}
function Ri(e) {
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
  return ie({}, t, { defaultChecked: void 0, defaultValue: void 0, value: void 0, checked: n ?? e._wrapperState.initialChecked });
}
function jc(e, t) {
  var n = t.defaultValue == null ? "" : t.defaultValue, r = t.checked != null ? t.checked : t.defaultChecked;
  n = pn(t.value != null ? t.value : n), e._wrapperState = { initialChecked: r, initialValue: n, controlled: t.type === "checkbox" || t.type === "radio" ? t.checked != null : t.value != null };
}
function sp(e, t) {
  t = t.checked, t != null && tu(e, "checked", t, !1);
}
function ta(e, t) {
  sp(e, t);
  var n = pn(t.value), r = t.type;
  if (n != null)
    r === "number" ? (n === 0 && e.value === "" || e.value != n) && (e.value = "" + n) : e.value !== "" + n && (e.value = "" + n);
  else if (r === "submit" || r === "reset") {
    e.removeAttribute("value");
    return;
  }
  t.hasOwnProperty("value") ? na(e, t.type, n) : t.hasOwnProperty("defaultValue") && na(e, t.type, pn(t.defaultValue)), t.checked == null && t.defaultChecked != null && (e.defaultChecked = !!t.defaultChecked);
}
function bc(e, t, n) {
  if (t.hasOwnProperty("value") || t.hasOwnProperty("defaultValue")) {
    var r = t.type;
    if (!(r !== "submit" && r !== "reset" || t.value !== void 0 && t.value !== null))
      return;
    t = "" + e._wrapperState.initialValue, n || t === e.value || (e.value = t), e.defaultValue = t;
  }
  n = e.name, n !== "" && (e.name = ""), e.defaultChecked = !!e._wrapperState.initialChecked, n !== "" && (e.name = n);
}
function na(e, t, n) {
  (t !== "number" || Ri(e.ownerDocument) !== e) && (n == null ? e.defaultValue = "" + e._wrapperState.initialValue : e.defaultValue !== "" + n && (e.defaultValue = "" + n));
}
var Ur = Array.isArray;
function tr(e, t, n, r) {
  if (e = e.options, t) {
    t = {};
    for (var o = 0; o < n.length; o++)
      t["$" + n[o]] = !0;
    for (n = 0; n < e.length; n++)
      o = t.hasOwnProperty("$" + e[n].value), e[n].selected !== o && (e[n].selected = o), o && r && (e[n].defaultSelected = !0);
  } else {
    for (n = "" + pn(n), t = null, o = 0; o < e.length; o++) {
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
  return ie({}, t, { value: void 0, defaultValue: void 0, children: "" + e._wrapperState.initialValue });
}
function Ac(e, t) {
  var n = t.value;
  if (n == null) {
    if (n = t.children, t = t.defaultValue, n != null) {
      if (t != null)
        throw Error(P(92));
      if (Ur(n)) {
        if (1 < n.length)
          throw Error(P(93));
        n = n[0];
      }
      t = n;
    }
    t == null && (t = ""), n = t;
  }
  e._wrapperState = { initialValue: pn(n) };
}
function ap(e, t) {
  var n = pn(t.value), r = pn(t.defaultValue);
  n != null && (n = "" + n, n !== e.value && (e.value = n), t.defaultValue == null && e.defaultValue !== n && (e.defaultValue = n)), r != null && (e.defaultValue = "" + r);
}
function Ic(e) {
  var t = e.textContent;
  t === e._wrapperState.initialValue && t !== "" && t !== null && (e.value = t);
}
function up(e) {
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
  return e == null || e === "http://www.w3.org/1999/xhtml" ? up(t) : e === "http://www.w3.org/2000/svg" && t === "foreignObject" ? "http://www.w3.org/1999/xhtml" : e;
}
var Go, cp = function(e) {
  return typeof MSApp < "u" && MSApp.execUnsafeLocalFunction ? function(t, n, r, o) {
    MSApp.execUnsafeLocalFunction(function() {
      return e(t, n, r, o);
    });
  } : e;
}(function(e, t) {
  if (e.namespaceURI !== "http://www.w3.org/2000/svg" || "innerHTML" in e)
    e.innerHTML = t;
  else {
    for (Go = Go || document.createElement("div"), Go.innerHTML = "<svg>" + t.valueOf().toString() + "</svg>", t = Go.firstChild; e.firstChild; )
      e.removeChild(e.firstChild);
    for (; t.firstChild; )
      e.appendChild(t.firstChild);
  }
});
function oo(e, t) {
  if (t) {
    var n = e.firstChild;
    if (n && n === e.lastChild && n.nodeType === 3) {
      n.nodeValue = t;
      return;
    }
  }
  e.textContent = t;
}
var Gr = {
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
}, eg = ["Webkit", "ms", "Moz", "O"];
Object.keys(Gr).forEach(function(e) {
  eg.forEach(function(t) {
    t = t + e.charAt(0).toUpperCase() + e.substring(1), Gr[t] = Gr[e];
  });
});
function dp(e, t, n) {
  return t == null || typeof t == "boolean" || t === "" ? "" : n || typeof t != "number" || t === 0 || Gr.hasOwnProperty(e) && Gr[e] ? ("" + t).trim() : t + "px";
}
function fp(e, t) {
  e = e.style;
  for (var n in t)
    if (t.hasOwnProperty(n)) {
      var r = n.indexOf("--") === 0, o = dp(n, t[n], r);
      n === "float" && (n = "cssFloat"), r ? e.setProperty(n, o) : e[n] = o;
    }
}
var tg = ie({ menuitem: !0 }, { area: !0, base: !0, br: !0, col: !0, embed: !0, hr: !0, img: !0, input: !0, keygen: !0, link: !0, meta: !0, param: !0, source: !0, track: !0, wbr: !0 });
function ia(e, t) {
  if (t) {
    if (tg[e] && (t.children != null || t.dangerouslySetInnerHTML != null))
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
function iu(e) {
  return e = e.target || e.srcElement || window, e.correspondingUseElement && (e = e.correspondingUseElement), e.nodeType === 3 ? e.parentNode : e;
}
var aa = null, nr = null, rr = null;
function Lc(e) {
  if (e = zo(e)) {
    if (typeof aa != "function")
      throw Error(P(280));
    var t = e.stateNode;
    t && (t = fl(t), aa(e.stateNode, e.type, t));
  }
}
function pp(e) {
  nr ? rr ? rr.push(e) : rr = [e] : nr = e;
}
function mp() {
  if (nr) {
    var e = nr, t = rr;
    if (rr = nr = null, Lc(e), t)
      for (e = 0; e < t.length; e++)
        Lc(t[e]);
  }
}
function hp(e, t) {
  return e(t);
}
function gp() {
}
var hs = !1;
function vp(e, t, n) {
  if (hs)
    return e(t, n);
  hs = !0;
  try {
    return hp(e, t, n);
  } finally {
    hs = !1, (nr !== null || rr !== null) && (gp(), mp());
  }
}
function io(e, t) {
  var n = e.stateNode;
  if (n === null)
    return null;
  var r = fl(n);
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
if (Wt)
  try {
    var Or = {};
    Object.defineProperty(Or, "passive", { get: function() {
      ua = !0;
    } }), window.addEventListener("test", Or, Or), window.removeEventListener("test", Or, Or);
  } catch {
    ua = !1;
  }
function ng(e, t, n, r, o, i, l, s, a) {
  var u = Array.prototype.slice.call(arguments, 3);
  try {
    t.apply(n, u);
  } catch (c) {
    this.onError(c);
  }
}
var Qr = !1, Mi = null, Oi = !1, ca = null, rg = { onError: function(e) {
  Qr = !0, Mi = e;
} };
function og(e, t, n, r, o, i, l, s, a) {
  Qr = !1, Mi = null, ng.apply(rg, arguments);
}
function ig(e, t, n, r, o, i, l, s, a) {
  if (og.apply(this, arguments), Qr) {
    if (Qr) {
      var u = Mi;
      Qr = !1, Mi = null;
    } else
      throw Error(P(198));
    Oi || (Oi = !0, ca = u);
  }
}
function jn(e) {
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
function yp(e) {
  if (e.tag === 13) {
    var t = e.memoizedState;
    if (t === null && (e = e.alternate, e !== null && (t = e.memoizedState)), t !== null)
      return t.dehydrated;
  }
  return null;
}
function Dc(e) {
  if (jn(e) !== e)
    throw Error(P(188));
}
function lg(e) {
  var t = e.alternate;
  if (!t) {
    if (t = jn(e), t === null)
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
          return Dc(o), e;
        if (i === r)
          return Dc(o), t;
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
function xp(e) {
  return e = lg(e), e !== null ? Sp(e) : null;
}
function Sp(e) {
  if (e.tag === 5 || e.tag === 6)
    return e;
  for (e = e.child; e !== null; ) {
    var t = Sp(e);
    if (t !== null)
      return t;
    e = e.sibling;
  }
  return null;
}
var wp = Je.unstable_scheduleCallback, Fc = Je.unstable_cancelCallback, sg = Je.unstable_shouldYield, ag = Je.unstable_requestPaint, ue = Je.unstable_now, ug = Je.unstable_getCurrentPriorityLevel, lu = Je.unstable_ImmediatePriority, Cp = Je.unstable_UserBlockingPriority, zi = Je.unstable_NormalPriority, cg = Je.unstable_LowPriority, kp = Je.unstable_IdlePriority, al = null, Ot = null;
function dg(e) {
  if (Ot && typeof Ot.onCommitFiberRoot == "function")
    try {
      Ot.onCommitFiberRoot(al, e, void 0, (e.current.flags & 128) === 128);
    } catch {
    }
}
var Ct = Math.clz32 ? Math.clz32 : mg, fg = Math.log, pg = Math.LN2;
function mg(e) {
  return e >>>= 0, e === 0 ? 32 : 31 - (fg(e) / pg | 0) | 0;
}
var Qo = 64, Yo = 4194304;
function Vr(e) {
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
function Ni(e, t) {
  var n = e.pendingLanes;
  if (n === 0)
    return 0;
  var r = 0, o = e.suspendedLanes, i = e.pingedLanes, l = n & 268435455;
  if (l !== 0) {
    var s = l & ~o;
    s !== 0 ? r = Vr(s) : (i &= l, i !== 0 && (r = Vr(i)));
  } else
    l = n & ~o, l !== 0 ? r = Vr(l) : i !== 0 && (r = Vr(i));
  if (r === 0)
    return 0;
  if (t !== 0 && t !== r && !(t & o) && (o = r & -r, i = t & -t, o >= i || o === 16 && (i & 4194240) !== 0))
    return t;
  if (r & 4 && (r |= n & 16), t = e.entangledLanes, t !== 0)
    for (e = e.entanglements, t &= r; 0 < t; )
      n = 31 - Ct(t), o = 1 << n, r |= e[n], t &= ~o;
  return r;
}
function hg(e, t) {
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
function gg(e, t) {
  for (var n = e.suspendedLanes, r = e.pingedLanes, o = e.expirationTimes, i = e.pendingLanes; 0 < i; ) {
    var l = 31 - Ct(i), s = 1 << l, a = o[l];
    a === -1 ? (!(s & n) || s & r) && (o[l] = hg(s, t)) : a <= t && (e.expiredLanes |= s), i &= ~s;
  }
}
function da(e) {
  return e = e.pendingLanes & -1073741825, e !== 0 ? e : e & 1073741824 ? 1073741824 : 0;
}
function _p() {
  var e = Qo;
  return Qo <<= 1, !(Qo & 4194240) && (Qo = 64), e;
}
function gs(e) {
  for (var t = [], n = 0; 31 > n; n++)
    t.push(e);
  return t;
}
function Mo(e, t, n) {
  e.pendingLanes |= t, t !== 536870912 && (e.suspendedLanes = 0, e.pingedLanes = 0), e = e.eventTimes, t = 31 - Ct(t), e[t] = n;
}
function vg(e, t) {
  var n = e.pendingLanes & ~t;
  e.pendingLanes = t, e.suspendedLanes = 0, e.pingedLanes = 0, e.expiredLanes &= t, e.mutableReadLanes &= t, e.entangledLanes &= t, t = e.entanglements;
  var r = e.eventTimes;
  for (e = e.expirationTimes; 0 < n; ) {
    var o = 31 - Ct(n), i = 1 << o;
    t[o] = 0, r[o] = -1, e[o] = -1, n &= ~i;
  }
}
function su(e, t) {
  var n = e.entangledLanes |= t;
  for (e = e.entanglements; n; ) {
    var r = 31 - Ct(n), o = 1 << r;
    o & t | e[r] & t && (e[r] |= t), n &= ~o;
  }
}
var K = 0;
function $p(e) {
  return e &= -e, 1 < e ? 4 < e ? e & 268435455 ? 16 : 536870912 : 4 : 1;
}
var Ep, au, Pp, Tp, Rp, fa = !1, Xo = [], on = null, ln = null, sn = null, lo = /* @__PURE__ */ new Map(), so = /* @__PURE__ */ new Map(), en = [], yg = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
function Bc(e, t) {
  switch (e) {
    case "focusin":
    case "focusout":
      on = null;
      break;
    case "dragenter":
    case "dragleave":
      ln = null;
      break;
    case "mouseover":
    case "mouseout":
      sn = null;
      break;
    case "pointerover":
    case "pointerout":
      lo.delete(t.pointerId);
      break;
    case "gotpointercapture":
    case "lostpointercapture":
      so.delete(t.pointerId);
  }
}
function zr(e, t, n, r, o, i) {
  return e === null || e.nativeEvent !== i ? (e = { blockedOn: t, domEventName: n, eventSystemFlags: r, nativeEvent: i, targetContainers: [o] }, t !== null && (t = zo(t), t !== null && au(t)), e) : (e.eventSystemFlags |= r, t = e.targetContainers, o !== null && t.indexOf(o) === -1 && t.push(o), e);
}
function xg(e, t, n, r, o) {
  switch (t) {
    case "focusin":
      return on = zr(on, e, t, n, r, o), !0;
    case "dragenter":
      return ln = zr(ln, e, t, n, r, o), !0;
    case "mouseover":
      return sn = zr(sn, e, t, n, r, o), !0;
    case "pointerover":
      var i = o.pointerId;
      return lo.set(i, zr(lo.get(i) || null, e, t, n, r, o)), !0;
    case "gotpointercapture":
      return i = o.pointerId, so.set(i, zr(so.get(i) || null, e, t, n, r, o)), !0;
  }
  return !1;
}
function Mp(e) {
  var t = Cn(e.target);
  if (t !== null) {
    var n = jn(t);
    if (n !== null) {
      if (t = n.tag, t === 13) {
        if (t = yp(n), t !== null) {
          e.blockedOn = t, Rp(e.priority, function() {
            Pp(n);
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
function pi(e) {
  if (e.blockedOn !== null)
    return !1;
  for (var t = e.targetContainers; 0 < t.length; ) {
    var n = pa(e.domEventName, e.eventSystemFlags, t[0], e.nativeEvent);
    if (n === null) {
      n = e.nativeEvent;
      var r = new n.constructor(n.type, n);
      sa = r, n.target.dispatchEvent(r), sa = null;
    } else
      return t = zo(n), t !== null && au(t), e.blockedOn = n, !1;
    t.shift();
  }
  return !0;
}
function Wc(e, t, n) {
  pi(e) && n.delete(t);
}
function Sg() {
  fa = !1, on !== null && pi(on) && (on = null), ln !== null && pi(ln) && (ln = null), sn !== null && pi(sn) && (sn = null), lo.forEach(Wc), so.forEach(Wc);
}
function Nr(e, t) {
  e.blockedOn === t && (e.blockedOn = null, fa || (fa = !0, Je.unstable_scheduleCallback(Je.unstable_NormalPriority, Sg)));
}
function ao(e) {
  function t(o) {
    return Nr(o, e);
  }
  if (0 < Xo.length) {
    Nr(Xo[0], e);
    for (var n = 1; n < Xo.length; n++) {
      var r = Xo[n];
      r.blockedOn === e && (r.blockedOn = null);
    }
  }
  for (on !== null && Nr(on, e), ln !== null && Nr(ln, e), sn !== null && Nr(sn, e), lo.forEach(t), so.forEach(t), n = 0; n < en.length; n++)
    r = en[n], r.blockedOn === e && (r.blockedOn = null);
  for (; 0 < en.length && (n = en[0], n.blockedOn === null); )
    Mp(n), n.blockedOn === null && en.shift();
}
var or = Gt.ReactCurrentBatchConfig, ji = !0;
function wg(e, t, n, r) {
  var o = K, i = or.transition;
  or.transition = null;
  try {
    K = 1, uu(e, t, n, r);
  } finally {
    K = o, or.transition = i;
  }
}
function Cg(e, t, n, r) {
  var o = K, i = or.transition;
  or.transition = null;
  try {
    K = 4, uu(e, t, n, r);
  } finally {
    K = o, or.transition = i;
  }
}
function uu(e, t, n, r) {
  if (ji) {
    var o = pa(e, t, n, r);
    if (o === null)
      Es(e, t, r, bi, n), Bc(e, r);
    else if (xg(o, e, t, n, r))
      r.stopPropagation();
    else if (Bc(e, r), t & 4 && -1 < yg.indexOf(e)) {
      for (; o !== null; ) {
        var i = zo(o);
        if (i !== null && Ep(i), i = pa(e, t, n, r), i === null && Es(e, t, r, bi, n), i === o)
          break;
        o = i;
      }
      o !== null && r.stopPropagation();
    } else
      Es(e, t, r, null, n);
  }
}
var bi = null;
function pa(e, t, n, r) {
  if (bi = null, e = iu(r), e = Cn(e), e !== null)
    if (t = jn(e), t === null)
      e = null;
    else if (n = t.tag, n === 13) {
      if (e = yp(t), e !== null)
        return e;
      e = null;
    } else if (n === 3) {
      if (t.stateNode.current.memoizedState.isDehydrated)
        return t.tag === 3 ? t.stateNode.containerInfo : null;
      e = null;
    } else
      t !== e && (e = null);
  return bi = e, null;
}
function Op(e) {
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
      switch (ug()) {
        case lu:
          return 1;
        case Cp:
          return 4;
        case zi:
        case cg:
          return 16;
        case kp:
          return 536870912;
        default:
          return 16;
      }
    default:
      return 16;
  }
}
var nn = null, cu = null, mi = null;
function zp() {
  if (mi)
    return mi;
  var e, t = cu, n = t.length, r, o = "value" in nn ? nn.value : nn.textContent, i = o.length;
  for (e = 0; e < n && t[e] === o[e]; e++)
    ;
  var l = n - e;
  for (r = 1; r <= l && t[n - r] === o[i - r]; r++)
    ;
  return mi = o.slice(e, 1 < r ? 1 - r : void 0);
}
function hi(e) {
  var t = e.keyCode;
  return "charCode" in e ? (e = e.charCode, e === 0 && t === 13 && (e = 13)) : e = t, e === 10 && (e = 13), 32 <= e || e === 13 ? e : 0;
}
function qo() {
  return !0;
}
function Uc() {
  return !1;
}
function tt(e) {
  function t(n, r, o, i, l) {
    this._reactName = n, this._targetInst = o, this.type = r, this.nativeEvent = i, this.target = l, this.currentTarget = null;
    for (var s in e)
      e.hasOwnProperty(s) && (n = e[s], this[s] = n ? n(i) : i[s]);
    return this.isDefaultPrevented = (i.defaultPrevented != null ? i.defaultPrevented : i.returnValue === !1) ? qo : Uc, this.isPropagationStopped = Uc, this;
  }
  return ie(t.prototype, { preventDefault: function() {
    this.defaultPrevented = !0;
    var n = this.nativeEvent;
    n && (n.preventDefault ? n.preventDefault() : typeof n.returnValue != "unknown" && (n.returnValue = !1), this.isDefaultPrevented = qo);
  }, stopPropagation: function() {
    var n = this.nativeEvent;
    n && (n.stopPropagation ? n.stopPropagation() : typeof n.cancelBubble != "unknown" && (n.cancelBubble = !0), this.isPropagationStopped = qo);
  }, persist: function() {
  }, isPersistent: qo }), t;
}
var Sr = { eventPhase: 0, bubbles: 0, cancelable: 0, timeStamp: function(e) {
  return e.timeStamp || Date.now();
}, defaultPrevented: 0, isTrusted: 0 }, du = tt(Sr), Oo = ie({}, Sr, { view: 0, detail: 0 }), kg = tt(Oo), vs, ys, jr, ul = ie({}, Oo, { screenX: 0, screenY: 0, clientX: 0, clientY: 0, pageX: 0, pageY: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, getModifierState: fu, button: 0, buttons: 0, relatedTarget: function(e) {
  return e.relatedTarget === void 0 ? e.fromElement === e.srcElement ? e.toElement : e.fromElement : e.relatedTarget;
}, movementX: function(e) {
  return "movementX" in e ? e.movementX : (e !== jr && (jr && e.type === "mousemove" ? (vs = e.screenX - jr.screenX, ys = e.screenY - jr.screenY) : ys = vs = 0, jr = e), vs);
}, movementY: function(e) {
  return "movementY" in e ? e.movementY : ys;
} }), Vc = tt(ul), _g = ie({}, ul, { dataTransfer: 0 }), $g = tt(_g), Eg = ie({}, Oo, { relatedTarget: 0 }), xs = tt(Eg), Pg = ie({}, Sr, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }), Tg = tt(Pg), Rg = ie({}, Sr, { clipboardData: function(e) {
  return "clipboardData" in e ? e.clipboardData : window.clipboardData;
} }), Mg = tt(Rg), Og = ie({}, Sr, { data: 0 }), Hc = tt(Og), zg = {
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
}, Ng = {
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
}, jg = { Alt: "altKey", Control: "ctrlKey", Meta: "metaKey", Shift: "shiftKey" };
function bg(e) {
  var t = this.nativeEvent;
  return t.getModifierState ? t.getModifierState(e) : (e = jg[e]) ? !!t[e] : !1;
}
function fu() {
  return bg;
}
var Ag = ie({}, Oo, { key: function(e) {
  if (e.key) {
    var t = zg[e.key] || e.key;
    if (t !== "Unidentified")
      return t;
  }
  return e.type === "keypress" ? (e = hi(e), e === 13 ? "Enter" : String.fromCharCode(e)) : e.type === "keydown" || e.type === "keyup" ? Ng[e.keyCode] || "Unidentified" : "";
}, code: 0, location: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, repeat: 0, locale: 0, getModifierState: fu, charCode: function(e) {
  return e.type === "keypress" ? hi(e) : 0;
}, keyCode: function(e) {
  return e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
}, which: function(e) {
  return e.type === "keypress" ? hi(e) : e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
} }), Ig = tt(Ag), Lg = ie({}, ul, { pointerId: 0, width: 0, height: 0, pressure: 0, tangentialPressure: 0, tiltX: 0, tiltY: 0, twist: 0, pointerType: 0, isPrimary: 0 }), Kc = tt(Lg), Dg = ie({}, Oo, { touches: 0, targetTouches: 0, changedTouches: 0, altKey: 0, metaKey: 0, ctrlKey: 0, shiftKey: 0, getModifierState: fu }), Fg = tt(Dg), Bg = ie({}, Sr, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }), Wg = tt(Bg), Ug = ie({}, ul, {
  deltaX: function(e) {
    return "deltaX" in e ? e.deltaX : "wheelDeltaX" in e ? -e.wheelDeltaX : 0;
  },
  deltaY: function(e) {
    return "deltaY" in e ? e.deltaY : "wheelDeltaY" in e ? -e.wheelDeltaY : "wheelDelta" in e ? -e.wheelDelta : 0;
  },
  deltaZ: 0,
  deltaMode: 0
}), Vg = tt(Ug), Hg = [9, 13, 27, 32], pu = Wt && "CompositionEvent" in window, Yr = null;
Wt && "documentMode" in document && (Yr = document.documentMode);
var Kg = Wt && "TextEvent" in window && !Yr, Np = Wt && (!pu || Yr && 8 < Yr && 11 >= Yr), Gc = String.fromCharCode(32), Qc = !1;
function jp(e, t) {
  switch (e) {
    case "keyup":
      return Hg.indexOf(t.keyCode) !== -1;
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
function bp(e) {
  return e = e.detail, typeof e == "object" && "data" in e ? e.data : null;
}
var Hn = !1;
function Gg(e, t) {
  switch (e) {
    case "compositionend":
      return bp(t);
    case "keypress":
      return t.which !== 32 ? null : (Qc = !0, Gc);
    case "textInput":
      return e = t.data, e === Gc && Qc ? null : e;
    default:
      return null;
  }
}
function Qg(e, t) {
  if (Hn)
    return e === "compositionend" || !pu && jp(e, t) ? (e = zp(), mi = cu = nn = null, Hn = !1, e) : null;
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
      return Np && t.locale !== "ko" ? null : t.data;
    default:
      return null;
  }
}
var Yg = { color: !0, date: !0, datetime: !0, "datetime-local": !0, email: !0, month: !0, number: !0, password: !0, range: !0, search: !0, tel: !0, text: !0, time: !0, url: !0, week: !0 };
function Yc(e) {
  var t = e && e.nodeName && e.nodeName.toLowerCase();
  return t === "input" ? !!Yg[e.type] : t === "textarea";
}
function Ap(e, t, n, r) {
  pp(r), t = Ai(t, "onChange"), 0 < t.length && (n = new du("onChange", "change", null, n, r), e.push({ event: n, listeners: t }));
}
var Xr = null, uo = null;
function Xg(e) {
  Gp(e, 0);
}
function cl(e) {
  var t = Qn(e);
  if (lp(t))
    return e;
}
function qg(e, t) {
  if (e === "change")
    return t;
}
var Ip = !1;
if (Wt) {
  var Ss;
  if (Wt) {
    var ws = "oninput" in document;
    if (!ws) {
      var Xc = document.createElement("div");
      Xc.setAttribute("oninput", "return;"), ws = typeof Xc.oninput == "function";
    }
    Ss = ws;
  } else
    Ss = !1;
  Ip = Ss && (!document.documentMode || 9 < document.documentMode);
}
function qc() {
  Xr && (Xr.detachEvent("onpropertychange", Lp), uo = Xr = null);
}
function Lp(e) {
  if (e.propertyName === "value" && cl(uo)) {
    var t = [];
    Ap(t, uo, e, iu(e)), vp(Xg, t);
  }
}
function Zg(e, t, n) {
  e === "focusin" ? (qc(), Xr = t, uo = n, Xr.attachEvent("onpropertychange", Lp)) : e === "focusout" && qc();
}
function Jg(e) {
  if (e === "selectionchange" || e === "keyup" || e === "keydown")
    return cl(uo);
}
function ev(e, t) {
  if (e === "click")
    return cl(t);
}
function tv(e, t) {
  if (e === "input" || e === "change")
    return cl(t);
}
function nv(e, t) {
  return e === t && (e !== 0 || 1 / e === 1 / t) || e !== e && t !== t;
}
var _t = typeof Object.is == "function" ? Object.is : nv;
function co(e, t) {
  if (_t(e, t))
    return !0;
  if (typeof e != "object" || e === null || typeof t != "object" || t === null)
    return !1;
  var n = Object.keys(e), r = Object.keys(t);
  if (n.length !== r.length)
    return !1;
  for (r = 0; r < n.length; r++) {
    var o = n[r];
    if (!Ys.call(t, o) || !_t(e[o], t[o]))
      return !1;
  }
  return !0;
}
function Zc(e) {
  for (; e && e.firstChild; )
    e = e.firstChild;
  return e;
}
function Jc(e, t) {
  var n = Zc(e);
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
    n = Zc(n);
  }
}
function Dp(e, t) {
  return e && t ? e === t ? !0 : e && e.nodeType === 3 ? !1 : t && t.nodeType === 3 ? Dp(e, t.parentNode) : "contains" in e ? e.contains(t) : e.compareDocumentPosition ? !!(e.compareDocumentPosition(t) & 16) : !1 : !1;
}
function Fp() {
  for (var e = window, t = Ri(); t instanceof e.HTMLIFrameElement; ) {
    try {
      var n = typeof t.contentWindow.location.href == "string";
    } catch {
      n = !1;
    }
    if (n)
      e = t.contentWindow;
    else
      break;
    t = Ri(e.document);
  }
  return t;
}
function mu(e) {
  var t = e && e.nodeName && e.nodeName.toLowerCase();
  return t && (t === "input" && (e.type === "text" || e.type === "search" || e.type === "tel" || e.type === "url" || e.type === "password") || t === "textarea" || e.contentEditable === "true");
}
function rv(e) {
  var t = Fp(), n = e.focusedElem, r = e.selectionRange;
  if (t !== n && n && n.ownerDocument && Dp(n.ownerDocument.documentElement, n)) {
    if (r !== null && mu(n)) {
      if (t = r.start, e = r.end, e === void 0 && (e = t), "selectionStart" in n)
        n.selectionStart = t, n.selectionEnd = Math.min(e, n.value.length);
      else if (e = (t = n.ownerDocument || document) && t.defaultView || window, e.getSelection) {
        e = e.getSelection();
        var o = n.textContent.length, i = Math.min(r.start, o);
        r = r.end === void 0 ? i : Math.min(r.end, o), !e.extend && i > r && (o = r, r = i, i = o), o = Jc(n, i);
        var l = Jc(
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
var ov = Wt && "documentMode" in document && 11 >= document.documentMode, Kn = null, ma = null, qr = null, ha = !1;
function ed(e, t, n) {
  var r = n.window === n ? n.document : n.nodeType === 9 ? n : n.ownerDocument;
  ha || Kn == null || Kn !== Ri(r) || (r = Kn, "selectionStart" in r && mu(r) ? r = { start: r.selectionStart, end: r.selectionEnd } : (r = (r.ownerDocument && r.ownerDocument.defaultView || window).getSelection(), r = { anchorNode: r.anchorNode, anchorOffset: r.anchorOffset, focusNode: r.focusNode, focusOffset: r.focusOffset }), qr && co(qr, r) || (qr = r, r = Ai(ma, "onSelect"), 0 < r.length && (t = new du("onSelect", "select", null, t, n), e.push({ event: t, listeners: r }), t.target = Kn)));
}
function Zo(e, t) {
  var n = {};
  return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit" + e] = "webkit" + t, n["Moz" + e] = "moz" + t, n;
}
var Gn = { animationend: Zo("Animation", "AnimationEnd"), animationiteration: Zo("Animation", "AnimationIteration"), animationstart: Zo("Animation", "AnimationStart"), transitionend: Zo("Transition", "TransitionEnd") }, Cs = {}, Bp = {};
Wt && (Bp = document.createElement("div").style, "AnimationEvent" in window || (delete Gn.animationend.animation, delete Gn.animationiteration.animation, delete Gn.animationstart.animation), "TransitionEvent" in window || delete Gn.transitionend.transition);
function dl(e) {
  if (Cs[e])
    return Cs[e];
  if (!Gn[e])
    return e;
  var t = Gn[e], n;
  for (n in t)
    if (t.hasOwnProperty(n) && n in Bp)
      return Cs[e] = t[n];
  return e;
}
var Wp = dl("animationend"), Up = dl("animationiteration"), Vp = dl("animationstart"), Hp = dl("transitionend"), Kp = /* @__PURE__ */ new Map(), td = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
function hn(e, t) {
  Kp.set(e, t), Nn(t, [e]);
}
for (var ks = 0; ks < td.length; ks++) {
  var _s = td[ks], iv = _s.toLowerCase(), lv = _s[0].toUpperCase() + _s.slice(1);
  hn(iv, "on" + lv);
}
hn(Wp, "onAnimationEnd");
hn(Up, "onAnimationIteration");
hn(Vp, "onAnimationStart");
hn("dblclick", "onDoubleClick");
hn("focusin", "onFocus");
hn("focusout", "onBlur");
hn(Hp, "onTransitionEnd");
cr("onMouseEnter", ["mouseout", "mouseover"]);
cr("onMouseLeave", ["mouseout", "mouseover"]);
cr("onPointerEnter", ["pointerout", "pointerover"]);
cr("onPointerLeave", ["pointerout", "pointerover"]);
Nn("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" "));
Nn("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));
Nn("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]);
Nn("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" "));
Nn("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" "));
Nn("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
var Hr = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), sv = new Set("cancel close invalid load scroll toggle".split(" ").concat(Hr));
function nd(e, t, n) {
  var r = e.type || "unknown-event";
  e.currentTarget = n, ig(r, t, void 0, e), e.currentTarget = null;
}
function Gp(e, t) {
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
          nd(o, s, u), i = a;
        }
      else
        for (l = 0; l < r.length; l++) {
          if (s = r[l], a = s.instance, u = s.currentTarget, s = s.listener, a !== i && o.isPropagationStopped())
            break e;
          nd(o, s, u), i = a;
        }
    }
  }
  if (Oi)
    throw e = ca, Oi = !1, ca = null, e;
}
function Z(e, t) {
  var n = t[Sa];
  n === void 0 && (n = t[Sa] = /* @__PURE__ */ new Set());
  var r = e + "__bubble";
  n.has(r) || (Qp(t, e, 2, !1), n.add(r));
}
function $s(e, t, n) {
  var r = 0;
  t && (r |= 4), Qp(n, e, r, t);
}
var Jo = "_reactListening" + Math.random().toString(36).slice(2);
function fo(e) {
  if (!e[Jo]) {
    e[Jo] = !0, tp.forEach(function(n) {
      n !== "selectionchange" && (sv.has(n) || $s(n, !1, e), $s(n, !0, e));
    });
    var t = e.nodeType === 9 ? e : e.ownerDocument;
    t === null || t[Jo] || (t[Jo] = !0, $s("selectionchange", !1, t));
  }
}
function Qp(e, t, n, r) {
  switch (Op(t)) {
    case 1:
      var o = wg;
      break;
    case 4:
      o = Cg;
      break;
    default:
      o = uu;
  }
  n = o.bind(null, t, n, e), o = void 0, !ua || t !== "touchstart" && t !== "touchmove" && t !== "wheel" || (o = !0), r ? o !== void 0 ? e.addEventListener(t, n, { capture: !0, passive: o }) : e.addEventListener(t, n, !0) : o !== void 0 ? e.addEventListener(t, n, { passive: o }) : e.addEventListener(t, n, !1);
}
function Es(e, t, n, r, o) {
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
            if (l = Cn(s), l === null)
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
  vp(function() {
    var u = i, c = iu(n), f = [];
    e: {
      var p = Kp.get(e);
      if (p !== void 0) {
        var v = du, y = e;
        switch (e) {
          case "keypress":
            if (hi(n) === 0)
              break e;
          case "keydown":
          case "keyup":
            v = Ig;
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
            v = Vc;
            break;
          case "drag":
          case "dragend":
          case "dragenter":
          case "dragexit":
          case "dragleave":
          case "dragover":
          case "dragstart":
          case "drop":
            v = $g;
            break;
          case "touchcancel":
          case "touchend":
          case "touchmove":
          case "touchstart":
            v = Fg;
            break;
          case Wp:
          case Up:
          case Vp:
            v = Tg;
            break;
          case Hp:
            v = Wg;
            break;
          case "scroll":
            v = kg;
            break;
          case "wheel":
            v = Vg;
            break;
          case "copy":
          case "cut":
          case "paste":
            v = Mg;
            break;
          case "gotpointercapture":
          case "lostpointercapture":
          case "pointercancel":
          case "pointerdown":
          case "pointermove":
          case "pointerout":
          case "pointerover":
          case "pointerup":
            v = Kc;
        }
        var g = (t & 4) !== 0, E = !g && e === "scroll", m = g ? p !== null ? p + "Capture" : null : p;
        g = [];
        for (var d = u, h; d !== null; ) {
          h = d;
          var S = h.stateNode;
          if (h.tag === 5 && S !== null && (h = S, m !== null && (S = io(d, m), S != null && g.push(po(d, S, h)))), E)
            break;
          d = d.return;
        }
        0 < g.length && (p = new v(p, y, null, n, c), f.push({ event: p, listeners: g }));
      }
    }
    if (!(t & 7)) {
      e: {
        if (p = e === "mouseover" || e === "pointerover", v = e === "mouseout" || e === "pointerout", p && n !== sa && (y = n.relatedTarget || n.fromElement) && (Cn(y) || y[Ut]))
          break e;
        if ((v || p) && (p = c.window === c ? c : (p = c.ownerDocument) ? p.defaultView || p.parentWindow : window, v ? (y = n.relatedTarget || n.toElement, v = u, y = y ? Cn(y) : null, y !== null && (E = jn(y), y !== E || y.tag !== 5 && y.tag !== 6) && (y = null)) : (v = null, y = u), v !== y)) {
          if (g = Vc, S = "onMouseLeave", m = "onMouseEnter", d = "mouse", (e === "pointerout" || e === "pointerover") && (g = Kc, S = "onPointerLeave", m = "onPointerEnter", d = "pointer"), E = v == null ? p : Qn(v), h = y == null ? p : Qn(y), p = new g(S, d + "leave", v, n, c), p.target = E, p.relatedTarget = h, S = null, Cn(c) === u && (g = new g(m, d + "enter", y, n, c), g.target = h, g.relatedTarget = E, S = g), E = S, v && y)
            t: {
              for (g = v, m = y, d = 0, h = g; h; h = In(h))
                d++;
              for (h = 0, S = m; S; S = In(S))
                h++;
              for (; 0 < d - h; )
                g = In(g), d--;
              for (; 0 < h - d; )
                m = In(m), h--;
              for (; d--; ) {
                if (g === m || m !== null && g === m.alternate)
                  break t;
                g = In(g), m = In(m);
              }
              g = null;
            }
          else
            g = null;
          v !== null && rd(f, p, v, g, !1), y !== null && E !== null && rd(f, E, y, g, !0);
        }
      }
      e: {
        if (p = u ? Qn(u) : window, v = p.nodeName && p.nodeName.toLowerCase(), v === "select" || v === "input" && p.type === "file")
          var $ = qg;
        else if (Yc(p))
          if (Ip)
            $ = tv;
          else {
            $ = Jg;
            var k = Zg;
          }
        else
          (v = p.nodeName) && v.toLowerCase() === "input" && (p.type === "checkbox" || p.type === "radio") && ($ = ev);
        if ($ && ($ = $(e, u))) {
          Ap(f, $, n, c);
          break e;
        }
        k && k(e, p, u), e === "focusout" && (k = p._wrapperState) && k.controlled && p.type === "number" && na(p, "number", p.value);
      }
      switch (k = u ? Qn(u) : window, e) {
        case "focusin":
          (Yc(k) || k.contentEditable === "true") && (Kn = k, ma = u, qr = null);
          break;
        case "focusout":
          qr = ma = Kn = null;
          break;
        case "mousedown":
          ha = !0;
          break;
        case "contextmenu":
        case "mouseup":
        case "dragend":
          ha = !1, ed(f, n, c);
          break;
        case "selectionchange":
          if (ov)
            break;
        case "keydown":
        case "keyup":
          ed(f, n, c);
      }
      var C;
      if (pu)
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
        Hn ? jp(e, n) && (T = "onCompositionEnd") : e === "keydown" && n.keyCode === 229 && (T = "onCompositionStart");
      T && (Np && n.locale !== "ko" && (Hn || T !== "onCompositionStart" ? T === "onCompositionEnd" && Hn && (C = zp()) : (nn = c, cu = "value" in nn ? nn.value : nn.textContent, Hn = !0)), k = Ai(u, T), 0 < k.length && (T = new Hc(T, e, null, n, c), f.push({ event: T, listeners: k }), C ? T.data = C : (C = bp(n), C !== null && (T.data = C)))), (C = Kg ? Gg(e, n) : Qg(e, n)) && (u = Ai(u, "onBeforeInput"), 0 < u.length && (c = new Hc("onBeforeInput", "beforeinput", null, n, c), f.push({ event: c, listeners: u }), c.data = C));
    }
    Gp(f, t);
  });
}
function po(e, t, n) {
  return { instance: e, listener: t, currentTarget: n };
}
function Ai(e, t) {
  for (var n = t + "Capture", r = []; e !== null; ) {
    var o = e, i = o.stateNode;
    o.tag === 5 && i !== null && (o = i, i = io(e, n), i != null && r.unshift(po(e, i, o)), i = io(e, t), i != null && r.push(po(e, i, o))), e = e.return;
  }
  return r;
}
function In(e) {
  if (e === null)
    return null;
  do
    e = e.return;
  while (e && e.tag !== 5);
  return e || null;
}
function rd(e, t, n, r, o) {
  for (var i = t._reactName, l = []; n !== null && n !== r; ) {
    var s = n, a = s.alternate, u = s.stateNode;
    if (a !== null && a === r)
      break;
    s.tag === 5 && u !== null && (s = u, o ? (a = io(n, i), a != null && l.unshift(po(n, a, s))) : o || (a = io(n, i), a != null && l.push(po(n, a, s)))), n = n.return;
  }
  l.length !== 0 && e.push({ event: t, listeners: l });
}
var av = /\r\n?/g, uv = /\u0000|\uFFFD/g;
function od(e) {
  return (typeof e == "string" ? e : "" + e).replace(av, `
`).replace(uv, "");
}
function ei(e, t, n) {
  if (t = od(t), od(e) !== t && n)
    throw Error(P(425));
}
function Ii() {
}
var ga = null, va = null;
function ya(e, t) {
  return e === "textarea" || e === "noscript" || typeof t.children == "string" || typeof t.children == "number" || typeof t.dangerouslySetInnerHTML == "object" && t.dangerouslySetInnerHTML !== null && t.dangerouslySetInnerHTML.__html != null;
}
var xa = typeof setTimeout == "function" ? setTimeout : void 0, cv = typeof clearTimeout == "function" ? clearTimeout : void 0, id = typeof Promise == "function" ? Promise : void 0, dv = typeof queueMicrotask == "function" ? queueMicrotask : typeof id < "u" ? function(e) {
  return id.resolve(null).then(e).catch(fv);
} : xa;
function fv(e) {
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
          e.removeChild(o), ao(t);
          return;
        }
        r--;
      } else
        n !== "$" && n !== "$?" && n !== "$!" || r++;
    n = o;
  } while (n);
  ao(t);
}
function an(e) {
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
function ld(e) {
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
var wr = Math.random().toString(36).slice(2), Mt = "__reactFiber$" + wr, mo = "__reactProps$" + wr, Ut = "__reactContainer$" + wr, Sa = "__reactEvents$" + wr, pv = "__reactListeners$" + wr, mv = "__reactHandles$" + wr;
function Cn(e) {
  var t = e[Mt];
  if (t)
    return t;
  for (var n = e.parentNode; n; ) {
    if (t = n[Ut] || n[Mt]) {
      if (n = t.alternate, t.child !== null || n !== null && n.child !== null)
        for (e = ld(e); e !== null; ) {
          if (n = e[Mt])
            return n;
          e = ld(e);
        }
      return t;
    }
    e = n, n = e.parentNode;
  }
  return null;
}
function zo(e) {
  return e = e[Mt] || e[Ut], !e || e.tag !== 5 && e.tag !== 6 && e.tag !== 13 && e.tag !== 3 ? null : e;
}
function Qn(e) {
  if (e.tag === 5 || e.tag === 6)
    return e.stateNode;
  throw Error(P(33));
}
function fl(e) {
  return e[mo] || null;
}
var wa = [], Yn = -1;
function gn(e) {
  return { current: e };
}
function J(e) {
  0 > Yn || (e.current = wa[Yn], wa[Yn] = null, Yn--);
}
function X(e, t) {
  Yn++, wa[Yn] = e.current, e.current = t;
}
var mn = {}, be = gn(mn), Ue = gn(!1), Tn = mn;
function dr(e, t) {
  var n = e.type.contextTypes;
  if (!n)
    return mn;
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
function Li() {
  J(Ue), J(be);
}
function sd(e, t, n) {
  if (be.current !== mn)
    throw Error(P(168));
  X(be, t), X(Ue, n);
}
function Yp(e, t, n) {
  var r = e.stateNode;
  if (t = t.childContextTypes, typeof r.getChildContext != "function")
    return n;
  r = r.getChildContext();
  for (var o in r)
    if (!(o in t))
      throw Error(P(108, Z0(e) || "Unknown", o));
  return ie({}, n, r);
}
function Di(e) {
  return e = (e = e.stateNode) && e.__reactInternalMemoizedMergedChildContext || mn, Tn = be.current, X(be, e), X(Ue, Ue.current), !0;
}
function ad(e, t, n) {
  var r = e.stateNode;
  if (!r)
    throw Error(P(169));
  n ? (e = Yp(e, t, Tn), r.__reactInternalMemoizedMergedChildContext = e, J(Ue), J(be), X(be, e)) : J(Ue), X(Ue, n);
}
var It = null, pl = !1, Ts = !1;
function Xp(e) {
  It === null ? It = [e] : It.push(e);
}
function hv(e) {
  pl = !0, Xp(e);
}
function vn() {
  if (!Ts && It !== null) {
    Ts = !0;
    var e = 0, t = K;
    try {
      var n = It;
      for (K = 1; e < n.length; e++) {
        var r = n[e];
        do
          r = r(!0);
        while (r !== null);
      }
      It = null, pl = !1;
    } catch (o) {
      throw It !== null && (It = It.slice(e + 1)), wp(lu, vn), o;
    } finally {
      K = t, Ts = !1;
    }
  }
  return null;
}
var Xn = [], qn = 0, Fi = null, Bi = 0, it = [], lt = 0, Rn = null, Dt = 1, Ft = "";
function xn(e, t) {
  Xn[qn++] = Bi, Xn[qn++] = Fi, Fi = e, Bi = t;
}
function qp(e, t, n) {
  it[lt++] = Dt, it[lt++] = Ft, it[lt++] = Rn, Rn = e;
  var r = Dt;
  e = Ft;
  var o = 32 - Ct(r) - 1;
  r &= ~(1 << o), n += 1;
  var i = 32 - Ct(t) + o;
  if (30 < i) {
    var l = o - o % 5;
    i = (r & (1 << l) - 1).toString(32), r >>= l, o -= l, Dt = 1 << 32 - Ct(t) + o | n << o | r, Ft = i + e;
  } else
    Dt = 1 << i | n << o | r, Ft = e;
}
function hu(e) {
  e.return !== null && (xn(e, 1), qp(e, 1, 0));
}
function gu(e) {
  for (; e === Fi; )
    Fi = Xn[--qn], Xn[qn] = null, Bi = Xn[--qn], Xn[qn] = null;
  for (; e === Rn; )
    Rn = it[--lt], it[lt] = null, Ft = it[--lt], it[lt] = null, Dt = it[--lt], it[lt] = null;
}
var qe = null, Xe = null, te = !1, wt = null;
function Zp(e, t) {
  var n = at(5, null, null, 0);
  n.elementType = "DELETED", n.stateNode = t, n.return = e, t = e.deletions, t === null ? (e.deletions = [n], e.flags |= 16) : t.push(n);
}
function ud(e, t) {
  switch (e.tag) {
    case 5:
      var n = e.type;
      return t = t.nodeType !== 1 || n.toLowerCase() !== t.nodeName.toLowerCase() ? null : t, t !== null ? (e.stateNode = t, qe = e, Xe = an(t.firstChild), !0) : !1;
    case 6:
      return t = e.pendingProps === "" || t.nodeType !== 3 ? null : t, t !== null ? (e.stateNode = t, qe = e, Xe = null, !0) : !1;
    case 13:
      return t = t.nodeType !== 8 ? null : t, t !== null ? (n = Rn !== null ? { id: Dt, overflow: Ft } : null, e.memoizedState = { dehydrated: t, treeContext: n, retryLane: 1073741824 }, n = at(18, null, null, 0), n.stateNode = t, n.return = e, e.child = n, qe = e, Xe = null, !0) : !1;
    default:
      return !1;
  }
}
function Ca(e) {
  return (e.mode & 1) !== 0 && (e.flags & 128) === 0;
}
function ka(e) {
  if (te) {
    var t = Xe;
    if (t) {
      var n = t;
      if (!ud(e, t)) {
        if (Ca(e))
          throw Error(P(418));
        t = an(n.nextSibling);
        var r = qe;
        t && ud(e, t) ? Zp(r, n) : (e.flags = e.flags & -4097 | 2, te = !1, qe = e);
      }
    } else {
      if (Ca(e))
        throw Error(P(418));
      e.flags = e.flags & -4097 | 2, te = !1, qe = e;
    }
  }
}
function cd(e) {
  for (e = e.return; e !== null && e.tag !== 5 && e.tag !== 3 && e.tag !== 13; )
    e = e.return;
  qe = e;
}
function ti(e) {
  if (e !== qe)
    return !1;
  if (!te)
    return cd(e), te = !0, !1;
  var t;
  if ((t = e.tag !== 3) && !(t = e.tag !== 5) && (t = e.type, t = t !== "head" && t !== "body" && !ya(e.type, e.memoizedProps)), t && (t = Xe)) {
    if (Ca(e))
      throw Jp(), Error(P(418));
    for (; t; )
      Zp(e, t), t = an(t.nextSibling);
  }
  if (cd(e), e.tag === 13) {
    if (e = e.memoizedState, e = e !== null ? e.dehydrated : null, !e)
      throw Error(P(317));
    e: {
      for (e = e.nextSibling, t = 0; e; ) {
        if (e.nodeType === 8) {
          var n = e.data;
          if (n === "/$") {
            if (t === 0) {
              Xe = an(e.nextSibling);
              break e;
            }
            t--;
          } else
            n !== "$" && n !== "$!" && n !== "$?" || t++;
        }
        e = e.nextSibling;
      }
      Xe = null;
    }
  } else
    Xe = qe ? an(e.stateNode.nextSibling) : null;
  return !0;
}
function Jp() {
  for (var e = Xe; e; )
    e = an(e.nextSibling);
}
function fr() {
  Xe = qe = null, te = !1;
}
function vu(e) {
  wt === null ? wt = [e] : wt.push(e);
}
var gv = Gt.ReactCurrentBatchConfig;
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
function ni(e, t) {
  throw e = Object.prototype.toString.call(t), Error(P(31, e === "[object Object]" ? "object with keys {" + Object.keys(t).join(", ") + "}" : e));
}
function dd(e) {
  var t = e._init;
  return t(e._payload);
}
function em(e) {
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
    return m = fn(m, d), m.index = 0, m.sibling = null, m;
  }
  function i(m, d, h) {
    return m.index = h, e ? (h = m.alternate, h !== null ? (h = h.index, h < d ? (m.flags |= 2, d) : h) : (m.flags |= 2, d)) : (m.flags |= 1048576, d);
  }
  function l(m) {
    return e && m.alternate === null && (m.flags |= 2), m;
  }
  function s(m, d, h, S) {
    return d === null || d.tag !== 6 ? (d = bs(h, m.mode, S), d.return = m, d) : (d = o(d, h), d.return = m, d);
  }
  function a(m, d, h, S) {
    var $ = h.type;
    return $ === Vn ? c(m, d, h.props.children, S, h.key) : d !== null && (d.elementType === $ || typeof $ == "object" && $ !== null && $.$$typeof === Zt && dd($) === d.type) ? (S = o(d, h.props), S.ref = br(m, d, h), S.return = m, S) : (S = Ci(h.type, h.key, h.props, null, m.mode, S), S.ref = br(m, d, h), S.return = m, S);
  }
  function u(m, d, h, S) {
    return d === null || d.tag !== 4 || d.stateNode.containerInfo !== h.containerInfo || d.stateNode.implementation !== h.implementation ? (d = As(h, m.mode, S), d.return = m, d) : (d = o(d, h.children || []), d.return = m, d);
  }
  function c(m, d, h, S, $) {
    return d === null || d.tag !== 7 ? (d = Pn(h, m.mode, S, $), d.return = m, d) : (d = o(d, h), d.return = m, d);
  }
  function f(m, d, h) {
    if (typeof d == "string" && d !== "" || typeof d == "number")
      return d = bs("" + d, m.mode, h), d.return = m, d;
    if (typeof d == "object" && d !== null) {
      switch (d.$$typeof) {
        case Ho:
          return h = Ci(d.type, d.key, d.props, null, m.mode, h), h.ref = br(m, null, d), h.return = m, h;
        case Un:
          return d = As(d, m.mode, h), d.return = m, d;
        case Zt:
          var S = d._init;
          return f(m, S(d._payload), h);
      }
      if (Ur(d) || Mr(d))
        return d = Pn(d, m.mode, h, null), d.return = m, d;
      ni(m, d);
    }
    return null;
  }
  function p(m, d, h, S) {
    var $ = d !== null ? d.key : null;
    if (typeof h == "string" && h !== "" || typeof h == "number")
      return $ !== null ? null : s(m, d, "" + h, S);
    if (typeof h == "object" && h !== null) {
      switch (h.$$typeof) {
        case Ho:
          return h.key === $ ? a(m, d, h, S) : null;
        case Un:
          return h.key === $ ? u(m, d, h, S) : null;
        case Zt:
          return $ = h._init, p(
            m,
            d,
            $(h._payload),
            S
          );
      }
      if (Ur(h) || Mr(h))
        return $ !== null ? null : c(m, d, h, S, null);
      ni(m, h);
    }
    return null;
  }
  function v(m, d, h, S, $) {
    if (typeof S == "string" && S !== "" || typeof S == "number")
      return m = m.get(h) || null, s(d, m, "" + S, $);
    if (typeof S == "object" && S !== null) {
      switch (S.$$typeof) {
        case Ho:
          return m = m.get(S.key === null ? h : S.key) || null, a(d, m, S, $);
        case Un:
          return m = m.get(S.key === null ? h : S.key) || null, u(d, m, S, $);
        case Zt:
          var k = S._init;
          return v(m, d, h, k(S._payload), $);
      }
      if (Ur(S) || Mr(S))
        return m = m.get(h) || null, c(d, m, S, $, null);
      ni(d, S);
    }
    return null;
  }
  function y(m, d, h, S) {
    for (var $ = null, k = null, C = d, T = d = 0, z = null; C !== null && T < h.length; T++) {
      C.index > T ? (z = C, C = null) : z = C.sibling;
      var M = p(m, C, h[T], S);
      if (M === null) {
        C === null && (C = z);
        break;
      }
      e && C && M.alternate === null && t(m, C), d = i(M, d, T), k === null ? $ = M : k.sibling = M, k = M, C = z;
    }
    if (T === h.length)
      return n(m, C), te && xn(m, T), $;
    if (C === null) {
      for (; T < h.length; T++)
        C = f(m, h[T], S), C !== null && (d = i(C, d, T), k === null ? $ = C : k.sibling = C, k = C);
      return te && xn(m, T), $;
    }
    for (C = r(m, C); T < h.length; T++)
      z = v(C, m, T, h[T], S), z !== null && (e && z.alternate !== null && C.delete(z.key === null ? T : z.key), d = i(z, d, T), k === null ? $ = z : k.sibling = z, k = z);
    return e && C.forEach(function(U) {
      return t(m, U);
    }), te && xn(m, T), $;
  }
  function g(m, d, h, S) {
    var $ = Mr(h);
    if (typeof $ != "function")
      throw Error(P(150));
    if (h = $.call(h), h == null)
      throw Error(P(151));
    for (var k = $ = null, C = d, T = d = 0, z = null, M = h.next(); C !== null && !M.done; T++, M = h.next()) {
      C.index > T ? (z = C, C = null) : z = C.sibling;
      var U = p(m, C, M.value, S);
      if (U === null) {
        C === null && (C = z);
        break;
      }
      e && C && U.alternate === null && t(m, C), d = i(U, d, T), k === null ? $ = U : k.sibling = U, k = U, C = z;
    }
    if (M.done)
      return n(
        m,
        C
      ), te && xn(m, T), $;
    if (C === null) {
      for (; !M.done; T++, M = h.next())
        M = f(m, M.value, S), M !== null && (d = i(M, d, T), k === null ? $ = M : k.sibling = M, k = M);
      return te && xn(m, T), $;
    }
    for (C = r(m, C); !M.done; T++, M = h.next())
      M = v(C, m, T, M.value, S), M !== null && (e && M.alternate !== null && C.delete(M.key === null ? T : M.key), d = i(M, d, T), k === null ? $ = M : k.sibling = M, k = M);
    return e && C.forEach(function(F) {
      return t(m, F);
    }), te && xn(m, T), $;
  }
  function E(m, d, h, S) {
    if (typeof h == "object" && h !== null && h.type === Vn && h.key === null && (h = h.props.children), typeof h == "object" && h !== null) {
      switch (h.$$typeof) {
        case Ho:
          e: {
            for (var $ = h.key, k = d; k !== null; ) {
              if (k.key === $) {
                if ($ = h.type, $ === Vn) {
                  if (k.tag === 7) {
                    n(m, k.sibling), d = o(k, h.props.children), d.return = m, m = d;
                    break e;
                  }
                } else if (k.elementType === $ || typeof $ == "object" && $ !== null && $.$$typeof === Zt && dd($) === k.type) {
                  n(m, k.sibling), d = o(k, h.props), d.ref = br(m, k, h), d.return = m, m = d;
                  break e;
                }
                n(m, k);
                break;
              } else
                t(m, k);
              k = k.sibling;
            }
            h.type === Vn ? (d = Pn(h.props.children, m.mode, S, h.key), d.return = m, m = d) : (S = Ci(h.type, h.key, h.props, null, m.mode, S), S.ref = br(m, d, h), S.return = m, m = S);
          }
          return l(m);
        case Un:
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
            d = As(h, m.mode, S), d.return = m, m = d;
          }
          return l(m);
        case Zt:
          return k = h._init, E(m, d, k(h._payload), S);
      }
      if (Ur(h))
        return y(m, d, h, S);
      if (Mr(h))
        return g(m, d, h, S);
      ni(m, h);
    }
    return typeof h == "string" && h !== "" || typeof h == "number" ? (h = "" + h, d !== null && d.tag === 6 ? (n(m, d.sibling), d = o(d, h), d.return = m, m = d) : (n(m, d), d = bs(h, m.mode, S), d.return = m, m = d), l(m)) : n(m, d);
  }
  return E;
}
var pr = em(!0), tm = em(!1), Wi = gn(null), Ui = null, Zn = null, yu = null;
function xu() {
  yu = Zn = Ui = null;
}
function Su(e) {
  var t = Wi.current;
  J(Wi), e._currentValue = t;
}
function _a(e, t, n) {
  for (; e !== null; ) {
    var r = e.alternate;
    if ((e.childLanes & t) !== t ? (e.childLanes |= t, r !== null && (r.childLanes |= t)) : r !== null && (r.childLanes & t) !== t && (r.childLanes |= t), e === n)
      break;
    e = e.return;
  }
}
function ir(e, t) {
  Ui = e, yu = Zn = null, e = e.dependencies, e !== null && e.firstContext !== null && (e.lanes & t && (We = !0), e.firstContext = null);
}
function dt(e) {
  var t = e._currentValue;
  if (yu !== e)
    if (e = { context: e, memoizedValue: t, next: null }, Zn === null) {
      if (Ui === null)
        throw Error(P(308));
      Zn = e, Ui.dependencies = { lanes: 0, firstContext: e };
    } else
      Zn = Zn.next = e;
  return t;
}
var kn = null;
function wu(e) {
  kn === null ? kn = [e] : kn.push(e);
}
function nm(e, t, n, r) {
  var o = t.interleaved;
  return o === null ? (n.next = n, wu(t)) : (n.next = o.next, o.next = n), t.interleaved = n, Vt(e, r);
}
function Vt(e, t) {
  e.lanes |= t;
  var n = e.alternate;
  for (n !== null && (n.lanes |= t), n = e, e = e.return; e !== null; )
    e.childLanes |= t, n = e.alternate, n !== null && (n.childLanes |= t), n = e, e = e.return;
  return n.tag === 3 ? n.stateNode : null;
}
var Jt = !1;
function Cu(e) {
  e.updateQueue = { baseState: e.memoizedState, firstBaseUpdate: null, lastBaseUpdate: null, shared: { pending: null, interleaved: null, lanes: 0 }, effects: null };
}
function rm(e, t) {
  e = e.updateQueue, t.updateQueue === e && (t.updateQueue = { baseState: e.baseState, firstBaseUpdate: e.firstBaseUpdate, lastBaseUpdate: e.lastBaseUpdate, shared: e.shared, effects: e.effects });
}
function Bt(e, t) {
  return { eventTime: e, lane: t, tag: 0, payload: null, callback: null, next: null };
}
function un(e, t, n) {
  var r = e.updateQueue;
  if (r === null)
    return null;
  if (r = r.shared, W & 2) {
    var o = r.pending;
    return o === null ? t.next = t : (t.next = o.next, o.next = t), r.pending = t, Vt(e, n);
  }
  return o = r.interleaved, o === null ? (t.next = t, wu(r)) : (t.next = o.next, o.next = t), r.interleaved = t, Vt(e, n);
}
function gi(e, t, n) {
  if (t = t.updateQueue, t !== null && (t = t.shared, (n & 4194240) !== 0)) {
    var r = t.lanes;
    r &= e.pendingLanes, n |= r, t.lanes = n, su(e, n);
  }
}
function fd(e, t) {
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
function Vi(e, t, n, r) {
  var o = e.updateQueue;
  Jt = !1;
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
              f = ie({}, f, p);
              break e;
            case 2:
              Jt = !0;
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
    On |= l, e.lanes = l, e.memoizedState = f;
  }
}
function pd(e, t, n) {
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
var No = {}, zt = gn(No), ho = gn(No), go = gn(No);
function _n(e) {
  if (e === No)
    throw Error(P(174));
  return e;
}
function ku(e, t) {
  switch (X(go, t), X(ho, e), X(zt, No), e = t.nodeType, e) {
    case 9:
    case 11:
      t = (t = t.documentElement) ? t.namespaceURI : oa(null, "");
      break;
    default:
      e = e === 8 ? t.parentNode : t, t = e.namespaceURI || null, e = e.tagName, t = oa(t, e);
  }
  J(zt), X(zt, t);
}
function mr() {
  J(zt), J(ho), J(go);
}
function om(e) {
  _n(go.current);
  var t = _n(zt.current), n = oa(t, e.type);
  t !== n && (X(ho, e), X(zt, n));
}
function _u(e) {
  ho.current === e && (J(zt), J(ho));
}
var re = gn(0);
function Hi(e) {
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
function $u() {
  for (var e = 0; e < Rs.length; e++)
    Rs[e]._workInProgressVersionPrimary = null;
  Rs.length = 0;
}
var vi = Gt.ReactCurrentDispatcher, Ms = Gt.ReactCurrentBatchConfig, Mn = 0, oe = null, Se = null, ke = null, Ki = !1, Zr = !1, vo = 0, vv = 0;
function Oe() {
  throw Error(P(321));
}
function Eu(e, t) {
  if (t === null)
    return !1;
  for (var n = 0; n < t.length && n < e.length; n++)
    if (!_t(e[n], t[n]))
      return !1;
  return !0;
}
function Pu(e, t, n, r, o, i) {
  if (Mn = i, oe = t, t.memoizedState = null, t.updateQueue = null, t.lanes = 0, vi.current = e === null || e.memoizedState === null ? wv : Cv, e = n(r, o), Zr) {
    i = 0;
    do {
      if (Zr = !1, vo = 0, 25 <= i)
        throw Error(P(301));
      i += 1, ke = Se = null, t.updateQueue = null, vi.current = kv, e = n(r, o);
    } while (Zr);
  }
  if (vi.current = Gi, t = Se !== null && Se.next !== null, Mn = 0, ke = Se = oe = null, Ki = !1, t)
    throw Error(P(300));
  return e;
}
function Tu() {
  var e = vo !== 0;
  return vo = 0, e;
}
function Pt() {
  var e = { memoizedState: null, baseState: null, baseQueue: null, queue: null, next: null };
  return ke === null ? oe.memoizedState = ke = e : ke = ke.next = e, ke;
}
function ft() {
  if (Se === null) {
    var e = oe.alternate;
    e = e !== null ? e.memoizedState : null;
  } else
    e = Se.next;
  var t = ke === null ? oe.memoizedState : ke.next;
  if (t !== null)
    ke = t, Se = e;
  else {
    if (e === null)
      throw Error(P(310));
    Se = e, e = { memoizedState: Se.memoizedState, baseState: Se.baseState, baseQueue: Se.baseQueue, queue: Se.queue, next: null }, ke === null ? oe.memoizedState = ke = e : ke = ke.next = e;
  }
  return ke;
}
function yo(e, t) {
  return typeof t == "function" ? t(e) : t;
}
function Os(e) {
  var t = ft(), n = t.queue;
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
      if ((Mn & c) === c)
        a !== null && (a = a.next = { lane: 0, action: u.action, hasEagerState: u.hasEagerState, eagerState: u.eagerState, next: null }), r = u.hasEagerState ? u.eagerState : e(r, u.action);
      else {
        var f = {
          lane: c,
          action: u.action,
          hasEagerState: u.hasEagerState,
          eagerState: u.eagerState,
          next: null
        };
        a === null ? (s = a = f, l = r) : a = a.next = f, oe.lanes |= c, On |= c;
      }
      u = u.next;
    } while (u !== null && u !== i);
    a === null ? l = r : a.next = s, _t(r, t.memoizedState) || (We = !0), t.memoizedState = r, t.baseState = l, t.baseQueue = a, n.lastRenderedState = r;
  }
  if (e = n.interleaved, e !== null) {
    o = e;
    do
      i = o.lane, oe.lanes |= i, On |= i, o = o.next;
    while (o !== e);
  } else
    o === null && (n.lanes = 0);
  return [t.memoizedState, n.dispatch];
}
function zs(e) {
  var t = ft(), n = t.queue;
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
    _t(i, t.memoizedState) || (We = !0), t.memoizedState = i, t.baseQueue === null && (t.baseState = i), n.lastRenderedState = i;
  }
  return [i, r];
}
function im() {
}
function lm(e, t) {
  var n = oe, r = ft(), o = t(), i = !_t(r.memoizedState, o);
  if (i && (r.memoizedState = o, We = !0), r = r.queue, Ru(um.bind(null, n, r, e), [e]), r.getSnapshot !== t || i || ke !== null && ke.memoizedState.tag & 1) {
    if (n.flags |= 2048, xo(9, am.bind(null, n, r, o, t), void 0, null), _e === null)
      throw Error(P(349));
    Mn & 30 || sm(n, t, o);
  }
  return o;
}
function sm(e, t, n) {
  e.flags |= 16384, e = { getSnapshot: t, value: n }, t = oe.updateQueue, t === null ? (t = { lastEffect: null, stores: null }, oe.updateQueue = t, t.stores = [e]) : (n = t.stores, n === null ? t.stores = [e] : n.push(e));
}
function am(e, t, n, r) {
  t.value = n, t.getSnapshot = r, cm(t) && dm(e);
}
function um(e, t, n) {
  return n(function() {
    cm(t) && dm(e);
  });
}
function cm(e) {
  var t = e.getSnapshot;
  e = e.value;
  try {
    var n = t();
    return !_t(e, n);
  } catch {
    return !0;
  }
}
function dm(e) {
  var t = Vt(e, 1);
  t !== null && kt(t, e, 1, -1);
}
function md(e) {
  var t = Pt();
  return typeof e == "function" && (e = e()), t.memoizedState = t.baseState = e, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: yo, lastRenderedState: e }, t.queue = e, e = e.dispatch = Sv.bind(null, oe, e), [t.memoizedState, e];
}
function xo(e, t, n, r) {
  return e = { tag: e, create: t, destroy: n, deps: r, next: null }, t = oe.updateQueue, t === null ? (t = { lastEffect: null, stores: null }, oe.updateQueue = t, t.lastEffect = e.next = e) : (n = t.lastEffect, n === null ? t.lastEffect = e.next = e : (r = n.next, n.next = e, e.next = r, t.lastEffect = e)), e;
}
function fm() {
  return ft().memoizedState;
}
function yi(e, t, n, r) {
  var o = Pt();
  oe.flags |= e, o.memoizedState = xo(1 | t, n, void 0, r === void 0 ? null : r);
}
function ml(e, t, n, r) {
  var o = ft();
  r = r === void 0 ? null : r;
  var i = void 0;
  if (Se !== null) {
    var l = Se.memoizedState;
    if (i = l.destroy, r !== null && Eu(r, l.deps)) {
      o.memoizedState = xo(t, n, i, r);
      return;
    }
  }
  oe.flags |= e, o.memoizedState = xo(1 | t, n, i, r);
}
function hd(e, t) {
  return yi(8390656, 8, e, t);
}
function Ru(e, t) {
  return ml(2048, 8, e, t);
}
function pm(e, t) {
  return ml(4, 2, e, t);
}
function mm(e, t) {
  return ml(4, 4, e, t);
}
function hm(e, t) {
  if (typeof t == "function")
    return e = e(), t(e), function() {
      t(null);
    };
  if (t != null)
    return e = e(), t.current = e, function() {
      t.current = null;
    };
}
function gm(e, t, n) {
  return n = n != null ? n.concat([e]) : null, ml(4, 4, hm.bind(null, t, e), n);
}
function Mu() {
}
function vm(e, t) {
  var n = ft();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && Eu(t, r[1]) ? r[0] : (n.memoizedState = [e, t], e);
}
function ym(e, t) {
  var n = ft();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && Eu(t, r[1]) ? r[0] : (e = e(), n.memoizedState = [e, t], e);
}
function xm(e, t, n) {
  return Mn & 21 ? (_t(n, t) || (n = _p(), oe.lanes |= n, On |= n, e.baseState = !0), t) : (e.baseState && (e.baseState = !1, We = !0), e.memoizedState = n);
}
function yv(e, t) {
  var n = K;
  K = n !== 0 && 4 > n ? n : 4, e(!0);
  var r = Ms.transition;
  Ms.transition = {};
  try {
    e(!1), t();
  } finally {
    K = n, Ms.transition = r;
  }
}
function Sm() {
  return ft().memoizedState;
}
function xv(e, t, n) {
  var r = dn(e);
  if (n = { lane: r, action: n, hasEagerState: !1, eagerState: null, next: null }, wm(e))
    Cm(t, n);
  else if (n = nm(e, t, n, r), n !== null) {
    var o = Le();
    kt(n, e, r, o), km(n, t, r);
  }
}
function Sv(e, t, n) {
  var r = dn(e), o = { lane: r, action: n, hasEagerState: !1, eagerState: null, next: null };
  if (wm(e))
    Cm(t, o);
  else {
    var i = e.alternate;
    if (e.lanes === 0 && (i === null || i.lanes === 0) && (i = t.lastRenderedReducer, i !== null))
      try {
        var l = t.lastRenderedState, s = i(l, n);
        if (o.hasEagerState = !0, o.eagerState = s, _t(s, l)) {
          var a = t.interleaved;
          a === null ? (o.next = o, wu(t)) : (o.next = a.next, a.next = o), t.interleaved = o;
          return;
        }
      } catch {
      } finally {
      }
    n = nm(e, t, o, r), n !== null && (o = Le(), kt(n, e, r, o), km(n, t, r));
  }
}
function wm(e) {
  var t = e.alternate;
  return e === oe || t !== null && t === oe;
}
function Cm(e, t) {
  Zr = Ki = !0;
  var n = e.pending;
  n === null ? t.next = t : (t.next = n.next, n.next = t), e.pending = t;
}
function km(e, t, n) {
  if (n & 4194240) {
    var r = t.lanes;
    r &= e.pendingLanes, n |= r, t.lanes = n, su(e, n);
  }
}
var Gi = { readContext: dt, useCallback: Oe, useContext: Oe, useEffect: Oe, useImperativeHandle: Oe, useInsertionEffect: Oe, useLayoutEffect: Oe, useMemo: Oe, useReducer: Oe, useRef: Oe, useState: Oe, useDebugValue: Oe, useDeferredValue: Oe, useTransition: Oe, useMutableSource: Oe, useSyncExternalStore: Oe, useId: Oe, unstable_isNewReconciler: !1 }, wv = { readContext: dt, useCallback: function(e, t) {
  return Pt().memoizedState = [e, t === void 0 ? null : t], e;
}, useContext: dt, useEffect: hd, useImperativeHandle: function(e, t, n) {
  return n = n != null ? n.concat([e]) : null, yi(
    4194308,
    4,
    hm.bind(null, t, e),
    n
  );
}, useLayoutEffect: function(e, t) {
  return yi(4194308, 4, e, t);
}, useInsertionEffect: function(e, t) {
  return yi(4, 2, e, t);
}, useMemo: function(e, t) {
  var n = Pt();
  return t = t === void 0 ? null : t, e = e(), n.memoizedState = [e, t], e;
}, useReducer: function(e, t, n) {
  var r = Pt();
  return t = n !== void 0 ? n(t) : t, r.memoizedState = r.baseState = t, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: e, lastRenderedState: t }, r.queue = e, e = e.dispatch = xv.bind(null, oe, e), [r.memoizedState, e];
}, useRef: function(e) {
  var t = Pt();
  return e = { current: e }, t.memoizedState = e;
}, useState: md, useDebugValue: Mu, useDeferredValue: function(e) {
  return Pt().memoizedState = e;
}, useTransition: function() {
  var e = md(!1), t = e[0];
  return e = yv.bind(null, e[1]), Pt().memoizedState = e, [t, e];
}, useMutableSource: function() {
}, useSyncExternalStore: function(e, t, n) {
  var r = oe, o = Pt();
  if (te) {
    if (n === void 0)
      throw Error(P(407));
    n = n();
  } else {
    if (n = t(), _e === null)
      throw Error(P(349));
    Mn & 30 || sm(r, t, n);
  }
  o.memoizedState = n;
  var i = { value: n, getSnapshot: t };
  return o.queue = i, hd(um.bind(
    null,
    r,
    i,
    e
  ), [e]), r.flags |= 2048, xo(9, am.bind(null, r, i, n, t), void 0, null), n;
}, useId: function() {
  var e = Pt(), t = _e.identifierPrefix;
  if (te) {
    var n = Ft, r = Dt;
    n = (r & ~(1 << 32 - Ct(r) - 1)).toString(32) + n, t = ":" + t + "R" + n, n = vo++, 0 < n && (t += "H" + n.toString(32)), t += ":";
  } else
    n = vv++, t = ":" + t + "r" + n.toString(32) + ":";
  return e.memoizedState = t;
}, unstable_isNewReconciler: !1 }, Cv = {
  readContext: dt,
  useCallback: vm,
  useContext: dt,
  useEffect: Ru,
  useImperativeHandle: gm,
  useInsertionEffect: pm,
  useLayoutEffect: mm,
  useMemo: ym,
  useReducer: Os,
  useRef: fm,
  useState: function() {
    return Os(yo);
  },
  useDebugValue: Mu,
  useDeferredValue: function(e) {
    var t = ft();
    return xm(t, Se.memoizedState, e);
  },
  useTransition: function() {
    var e = Os(yo)[0], t = ft().memoizedState;
    return [e, t];
  },
  useMutableSource: im,
  useSyncExternalStore: lm,
  useId: Sm,
  unstable_isNewReconciler: !1
}, kv = { readContext: dt, useCallback: vm, useContext: dt, useEffect: Ru, useImperativeHandle: gm, useInsertionEffect: pm, useLayoutEffect: mm, useMemo: ym, useReducer: zs, useRef: fm, useState: function() {
  return zs(yo);
}, useDebugValue: Mu, useDeferredValue: function(e) {
  var t = ft();
  return Se === null ? t.memoizedState = e : xm(t, Se.memoizedState, e);
}, useTransition: function() {
  var e = zs(yo)[0], t = ft().memoizedState;
  return [e, t];
}, useMutableSource: im, useSyncExternalStore: lm, useId: Sm, unstable_isNewReconciler: !1 };
function xt(e, t) {
  if (e && e.defaultProps) {
    t = ie({}, t), e = e.defaultProps;
    for (var n in e)
      t[n] === void 0 && (t[n] = e[n]);
    return t;
  }
  return t;
}
function $a(e, t, n, r) {
  t = e.memoizedState, n = n(r, t), n = n == null ? t : ie({}, t, n), e.memoizedState = n, e.lanes === 0 && (e.updateQueue.baseState = n);
}
var hl = { isMounted: function(e) {
  return (e = e._reactInternals) ? jn(e) === e : !1;
}, enqueueSetState: function(e, t, n) {
  e = e._reactInternals;
  var r = Le(), o = dn(e), i = Bt(r, o);
  i.payload = t, n != null && (i.callback = n), t = un(e, i, o), t !== null && (kt(t, e, o, r), gi(t, e, o));
}, enqueueReplaceState: function(e, t, n) {
  e = e._reactInternals;
  var r = Le(), o = dn(e), i = Bt(r, o);
  i.tag = 1, i.payload = t, n != null && (i.callback = n), t = un(e, i, o), t !== null && (kt(t, e, o, r), gi(t, e, o));
}, enqueueForceUpdate: function(e, t) {
  e = e._reactInternals;
  var n = Le(), r = dn(e), o = Bt(n, r);
  o.tag = 2, t != null && (o.callback = t), t = un(e, o, r), t !== null && (kt(t, e, r, n), gi(t, e, r));
} };
function gd(e, t, n, r, o, i, l) {
  return e = e.stateNode, typeof e.shouldComponentUpdate == "function" ? e.shouldComponentUpdate(r, i, l) : t.prototype && t.prototype.isPureReactComponent ? !co(n, r) || !co(o, i) : !0;
}
function _m(e, t, n) {
  var r = !1, o = mn, i = t.contextType;
  return typeof i == "object" && i !== null ? i = dt(i) : (o = Ve(t) ? Tn : be.current, r = t.contextTypes, i = (r = r != null) ? dr(e, o) : mn), t = new t(n, i), e.memoizedState = t.state !== null && t.state !== void 0 ? t.state : null, t.updater = hl, e.stateNode = t, t._reactInternals = e, r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = o, e.__reactInternalMemoizedMaskedChildContext = i), t;
}
function vd(e, t, n, r) {
  e = t.state, typeof t.componentWillReceiveProps == "function" && t.componentWillReceiveProps(n, r), typeof t.UNSAFE_componentWillReceiveProps == "function" && t.UNSAFE_componentWillReceiveProps(n, r), t.state !== e && hl.enqueueReplaceState(t, t.state, null);
}
function Ea(e, t, n, r) {
  var o = e.stateNode;
  o.props = n, o.state = e.memoizedState, o.refs = {}, Cu(e);
  var i = t.contextType;
  typeof i == "object" && i !== null ? o.context = dt(i) : (i = Ve(t) ? Tn : be.current, o.context = dr(e, i)), o.state = e.memoizedState, i = t.getDerivedStateFromProps, typeof i == "function" && ($a(e, t, i, n), o.state = e.memoizedState), typeof t.getDerivedStateFromProps == "function" || typeof o.getSnapshotBeforeUpdate == "function" || typeof o.UNSAFE_componentWillMount != "function" && typeof o.componentWillMount != "function" || (t = o.state, typeof o.componentWillMount == "function" && o.componentWillMount(), typeof o.UNSAFE_componentWillMount == "function" && o.UNSAFE_componentWillMount(), t !== o.state && hl.enqueueReplaceState(o, o.state, null), Vi(e, n, o, r), o.state = e.memoizedState), typeof o.componentDidMount == "function" && (e.flags |= 4194308);
}
function hr(e, t) {
  try {
    var n = "", r = t;
    do
      n += q0(r), r = r.return;
    while (r);
    var o = n;
  } catch (i) {
    o = `
Error generating stack: ` + i.message + `
` + i.stack;
  }
  return { value: e, source: t, stack: o, digest: null };
}
function Ns(e, t, n) {
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
var _v = typeof WeakMap == "function" ? WeakMap : Map;
function $m(e, t, n) {
  n = Bt(-1, n), n.tag = 3, n.payload = { element: null };
  var r = t.value;
  return n.callback = function() {
    Yi || (Yi = !0, Ia = r), Pa(e, t);
  }, n;
}
function Em(e, t, n) {
  n = Bt(-1, n), n.tag = 3;
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
    Pa(e, t), typeof r != "function" && (cn === null ? cn = /* @__PURE__ */ new Set([this]) : cn.add(this));
    var l = t.stack;
    this.componentDidCatch(t.value, { componentStack: l !== null ? l : "" });
  }), n;
}
function yd(e, t, n) {
  var r = e.pingCache;
  if (r === null) {
    r = e.pingCache = new _v();
    var o = /* @__PURE__ */ new Set();
    r.set(t, o);
  } else
    o = r.get(t), o === void 0 && (o = /* @__PURE__ */ new Set(), r.set(t, o));
  o.has(n) || (o.add(n), e = Lv.bind(null, e, t, n), t.then(e, e));
}
function xd(e) {
  do {
    var t;
    if ((t = e.tag === 13) && (t = e.memoizedState, t = t !== null ? t.dehydrated !== null : !0), t)
      return e;
    e = e.return;
  } while (e !== null);
  return null;
}
function Sd(e, t, n, r, o) {
  return e.mode & 1 ? (e.flags |= 65536, e.lanes = o, e) : (e === t ? e.flags |= 65536 : (e.flags |= 128, n.flags |= 131072, n.flags &= -52805, n.tag === 1 && (n.alternate === null ? n.tag = 17 : (t = Bt(-1, 1), t.tag = 2, un(n, t, 1))), n.lanes |= 1), e);
}
var $v = Gt.ReactCurrentOwner, We = !1;
function Ie(e, t, n, r) {
  t.child = e === null ? tm(t, null, n, r) : pr(t, e.child, n, r);
}
function wd(e, t, n, r, o) {
  n = n.render;
  var i = t.ref;
  return ir(t, o), r = Pu(e, t, n, r, i, o), n = Tu(), e !== null && !We ? (t.updateQueue = e.updateQueue, t.flags &= -2053, e.lanes &= ~o, Ht(e, t, o)) : (te && n && hu(t), t.flags |= 1, Ie(e, t, r, o), t.child);
}
function Cd(e, t, n, r, o) {
  if (e === null) {
    var i = n.type;
    return typeof i == "function" && !Lu(i) && i.defaultProps === void 0 && n.compare === null && n.defaultProps === void 0 ? (t.tag = 15, t.type = i, Pm(e, t, i, r, o)) : (e = Ci(n.type, null, r, t, t.mode, o), e.ref = t.ref, e.return = t, t.child = e);
  }
  if (i = e.child, !(e.lanes & o)) {
    var l = i.memoizedProps;
    if (n = n.compare, n = n !== null ? n : co, n(l, r) && e.ref === t.ref)
      return Ht(e, t, o);
  }
  return t.flags |= 1, e = fn(i, r), e.ref = t.ref, e.return = t, t.child = e;
}
function Pm(e, t, n, r, o) {
  if (e !== null) {
    var i = e.memoizedProps;
    if (co(i, r) && e.ref === t.ref)
      if (We = !1, t.pendingProps = r = i, (e.lanes & o) !== 0)
        e.flags & 131072 && (We = !0);
      else
        return t.lanes = e.lanes, Ht(e, t, o);
  }
  return Ta(e, t, n, r, o);
}
function Tm(e, t, n) {
  var r = t.pendingProps, o = r.children, i = e !== null ? e.memoizedState : null;
  if (r.mode === "hidden")
    if (!(t.mode & 1))
      t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, X(er, Qe), Qe |= n;
    else {
      if (!(n & 1073741824))
        return e = i !== null ? i.baseLanes | n : n, t.lanes = t.childLanes = 1073741824, t.memoizedState = { baseLanes: e, cachePool: null, transitions: null }, t.updateQueue = null, X(er, Qe), Qe |= e, null;
      t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, r = i !== null ? i.baseLanes : n, X(er, Qe), Qe |= r;
    }
  else
    i !== null ? (r = i.baseLanes | n, t.memoizedState = null) : r = n, X(er, Qe), Qe |= r;
  return Ie(e, t, o, n), t.child;
}
function Rm(e, t) {
  var n = t.ref;
  (e === null && n !== null || e !== null && e.ref !== n) && (t.flags |= 512, t.flags |= 2097152);
}
function Ta(e, t, n, r, o) {
  var i = Ve(n) ? Tn : be.current;
  return i = dr(t, i), ir(t, o), n = Pu(e, t, n, r, i, o), r = Tu(), e !== null && !We ? (t.updateQueue = e.updateQueue, t.flags &= -2053, e.lanes &= ~o, Ht(e, t, o)) : (te && r && hu(t), t.flags |= 1, Ie(e, t, n, o), t.child);
}
function kd(e, t, n, r, o) {
  if (Ve(n)) {
    var i = !0;
    Di(t);
  } else
    i = !1;
  if (ir(t, o), t.stateNode === null)
    xi(e, t), _m(t, n, r), Ea(t, n, r, o), r = !0;
  else if (e === null) {
    var l = t.stateNode, s = t.memoizedProps;
    l.props = s;
    var a = l.context, u = n.contextType;
    typeof u == "object" && u !== null ? u = dt(u) : (u = Ve(n) ? Tn : be.current, u = dr(t, u));
    var c = n.getDerivedStateFromProps, f = typeof c == "function" || typeof l.getSnapshotBeforeUpdate == "function";
    f || typeof l.UNSAFE_componentWillReceiveProps != "function" && typeof l.componentWillReceiveProps != "function" || (s !== r || a !== u) && vd(t, l, r, u), Jt = !1;
    var p = t.memoizedState;
    l.state = p, Vi(t, r, l, o), a = t.memoizedState, s !== r || p !== a || Ue.current || Jt ? (typeof c == "function" && ($a(t, n, c, r), a = t.memoizedState), (s = Jt || gd(t, n, s, r, p, a, u)) ? (f || typeof l.UNSAFE_componentWillMount != "function" && typeof l.componentWillMount != "function" || (typeof l.componentWillMount == "function" && l.componentWillMount(), typeof l.UNSAFE_componentWillMount == "function" && l.UNSAFE_componentWillMount()), typeof l.componentDidMount == "function" && (t.flags |= 4194308)) : (typeof l.componentDidMount == "function" && (t.flags |= 4194308), t.memoizedProps = r, t.memoizedState = a), l.props = r, l.state = a, l.context = u, r = s) : (typeof l.componentDidMount == "function" && (t.flags |= 4194308), r = !1);
  } else {
    l = t.stateNode, rm(e, t), s = t.memoizedProps, u = t.type === t.elementType ? s : xt(t.type, s), l.props = u, f = t.pendingProps, p = l.context, a = n.contextType, typeof a == "object" && a !== null ? a = dt(a) : (a = Ve(n) ? Tn : be.current, a = dr(t, a));
    var v = n.getDerivedStateFromProps;
    (c = typeof v == "function" || typeof l.getSnapshotBeforeUpdate == "function") || typeof l.UNSAFE_componentWillReceiveProps != "function" && typeof l.componentWillReceiveProps != "function" || (s !== f || p !== a) && vd(t, l, r, a), Jt = !1, p = t.memoizedState, l.state = p, Vi(t, r, l, o);
    var y = t.memoizedState;
    s !== f || p !== y || Ue.current || Jt ? (typeof v == "function" && ($a(t, n, v, r), y = t.memoizedState), (u = Jt || gd(t, n, u, r, p, y, a) || !1) ? (c || typeof l.UNSAFE_componentWillUpdate != "function" && typeof l.componentWillUpdate != "function" || (typeof l.componentWillUpdate == "function" && l.componentWillUpdate(r, y, a), typeof l.UNSAFE_componentWillUpdate == "function" && l.UNSAFE_componentWillUpdate(r, y, a)), typeof l.componentDidUpdate == "function" && (t.flags |= 4), typeof l.getSnapshotBeforeUpdate == "function" && (t.flags |= 1024)) : (typeof l.componentDidUpdate != "function" || s === e.memoizedProps && p === e.memoizedState || (t.flags |= 4), typeof l.getSnapshotBeforeUpdate != "function" || s === e.memoizedProps && p === e.memoizedState || (t.flags |= 1024), t.memoizedProps = r, t.memoizedState = y), l.props = r, l.state = y, l.context = a, r = u) : (typeof l.componentDidUpdate != "function" || s === e.memoizedProps && p === e.memoizedState || (t.flags |= 4), typeof l.getSnapshotBeforeUpdate != "function" || s === e.memoizedProps && p === e.memoizedState || (t.flags |= 1024), r = !1);
  }
  return Ra(e, t, n, r, i, o);
}
function Ra(e, t, n, r, o, i) {
  Rm(e, t);
  var l = (t.flags & 128) !== 0;
  if (!r && !l)
    return o && ad(t, n, !1), Ht(e, t, i);
  r = t.stateNode, $v.current = t;
  var s = l && typeof n.getDerivedStateFromError != "function" ? null : r.render();
  return t.flags |= 1, e !== null && l ? (t.child = pr(t, e.child, null, i), t.child = pr(t, null, s, i)) : Ie(e, t, s, i), t.memoizedState = r.state, o && ad(t, n, !0), t.child;
}
function Mm(e) {
  var t = e.stateNode;
  t.pendingContext ? sd(e, t.pendingContext, t.pendingContext !== t.context) : t.context && sd(e, t.context, !1), ku(e, t.containerInfo);
}
function _d(e, t, n, r, o) {
  return fr(), vu(o), t.flags |= 256, Ie(e, t, n, r), t.child;
}
var Ma = { dehydrated: null, treeContext: null, retryLane: 0 };
function Oa(e) {
  return { baseLanes: e, cachePool: null, transitions: null };
}
function Om(e, t, n) {
  var r = t.pendingProps, o = re.current, i = !1, l = (t.flags & 128) !== 0, s;
  if ((s = l) || (s = e !== null && e.memoizedState === null ? !1 : (o & 2) !== 0), s ? (i = !0, t.flags &= -129) : (e === null || e.memoizedState !== null) && (o |= 1), X(re, o & 1), e === null)
    return ka(t), e = t.memoizedState, e !== null && (e = e.dehydrated, e !== null) ? (t.mode & 1 ? e.data === "$!" ? t.lanes = 8 : t.lanes = 1073741824 : t.lanes = 1, null) : (l = r.children, e = r.fallback, i ? (r = t.mode, i = t.child, l = { mode: "hidden", children: l }, !(r & 1) && i !== null ? (i.childLanes = 0, i.pendingProps = l) : i = yl(l, r, 0, null), e = Pn(e, r, n, null), i.return = t, e.return = t, i.sibling = e, t.child = i, t.child.memoizedState = Oa(n), t.memoizedState = Ma, e) : Ou(t, l));
  if (o = e.memoizedState, o !== null && (s = o.dehydrated, s !== null))
    return Ev(e, t, l, r, s, o, n);
  if (i) {
    i = r.fallback, l = t.mode, o = e.child, s = o.sibling;
    var a = { mode: "hidden", children: r.children };
    return !(l & 1) && t.child !== o ? (r = t.child, r.childLanes = 0, r.pendingProps = a, t.deletions = null) : (r = fn(o, a), r.subtreeFlags = o.subtreeFlags & 14680064), s !== null ? i = fn(s, i) : (i = Pn(i, l, n, null), i.flags |= 2), i.return = t, r.return = t, r.sibling = i, t.child = r, r = i, i = t.child, l = e.child.memoizedState, l = l === null ? Oa(n) : { baseLanes: l.baseLanes | n, cachePool: null, transitions: l.transitions }, i.memoizedState = l, i.childLanes = e.childLanes & ~n, t.memoizedState = Ma, r;
  }
  return i = e.child, e = i.sibling, r = fn(i, { mode: "visible", children: r.children }), !(t.mode & 1) && (r.lanes = n), r.return = t, r.sibling = null, e !== null && (n = t.deletions, n === null ? (t.deletions = [e], t.flags |= 16) : n.push(e)), t.child = r, t.memoizedState = null, r;
}
function Ou(e, t) {
  return t = yl({ mode: "visible", children: t }, e.mode, 0, null), t.return = e, e.child = t;
}
function ri(e, t, n, r) {
  return r !== null && vu(r), pr(t, e.child, null, n), e = Ou(t, t.pendingProps.children), e.flags |= 2, t.memoizedState = null, e;
}
function Ev(e, t, n, r, o, i, l) {
  if (n)
    return t.flags & 256 ? (t.flags &= -257, r = Ns(Error(P(422))), ri(e, t, l, r)) : t.memoizedState !== null ? (t.child = e.child, t.flags |= 128, null) : (i = r.fallback, o = t.mode, r = yl({ mode: "visible", children: r.children }, o, 0, null), i = Pn(i, o, l, null), i.flags |= 2, r.return = t, i.return = t, r.sibling = i, t.child = r, t.mode & 1 && pr(t, e.child, null, l), t.child.memoizedState = Oa(l), t.memoizedState = Ma, i);
  if (!(t.mode & 1))
    return ri(e, t, l, null);
  if (o.data === "$!") {
    if (r = o.nextSibling && o.nextSibling.dataset, r)
      var s = r.dgst;
    return r = s, i = Error(P(419)), r = Ns(i, r, void 0), ri(e, t, l, r);
  }
  if (s = (l & e.childLanes) !== 0, We || s) {
    if (r = _e, r !== null) {
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
      o = o & (r.suspendedLanes | l) ? 0 : o, o !== 0 && o !== i.retryLane && (i.retryLane = o, Vt(e, o), kt(r, e, o, -1));
    }
    return Iu(), r = Ns(Error(P(421))), ri(e, t, l, r);
  }
  return o.data === "$?" ? (t.flags |= 128, t.child = e.child, t = Dv.bind(null, e), o._reactRetry = t, null) : (e = i.treeContext, Xe = an(o.nextSibling), qe = t, te = !0, wt = null, e !== null && (it[lt++] = Dt, it[lt++] = Ft, it[lt++] = Rn, Dt = e.id, Ft = e.overflow, Rn = t), t = Ou(t, r.children), t.flags |= 4096, t);
}
function $d(e, t, n) {
  e.lanes |= t;
  var r = e.alternate;
  r !== null && (r.lanes |= t), _a(e.return, t, n);
}
function js(e, t, n, r, o) {
  var i = e.memoizedState;
  i === null ? e.memoizedState = { isBackwards: t, rendering: null, renderingStartTime: 0, last: r, tail: n, tailMode: o } : (i.isBackwards = t, i.rendering = null, i.renderingStartTime = 0, i.last = r, i.tail = n, i.tailMode = o);
}
function zm(e, t, n) {
  var r = t.pendingProps, o = r.revealOrder, i = r.tail;
  if (Ie(e, t, r.children, n), r = re.current, r & 2)
    r = r & 1 | 2, t.flags |= 128;
  else {
    if (e !== null && e.flags & 128)
      e:
        for (e = t.child; e !== null; ) {
          if (e.tag === 13)
            e.memoizedState !== null && $d(e, n, t);
          else if (e.tag === 19)
            $d(e, n, t);
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
  if (X(re, r), !(t.mode & 1))
    t.memoizedState = null;
  else
    switch (o) {
      case "forwards":
        for (n = t.child, o = null; n !== null; )
          e = n.alternate, e !== null && Hi(e) === null && (o = n), n = n.sibling;
        n = o, n === null ? (o = t.child, t.child = null) : (o = n.sibling, n.sibling = null), js(t, !1, o, n, i);
        break;
      case "backwards":
        for (n = null, o = t.child, t.child = null; o !== null; ) {
          if (e = o.alternate, e !== null && Hi(e) === null) {
            t.child = o;
            break;
          }
          e = o.sibling, o.sibling = n, n = o, o = e;
        }
        js(t, !0, n, null, i);
        break;
      case "together":
        js(t, !1, null, null, void 0);
        break;
      default:
        t.memoizedState = null;
    }
  return t.child;
}
function xi(e, t) {
  !(t.mode & 1) && e !== null && (e.alternate = null, t.alternate = null, t.flags |= 2);
}
function Ht(e, t, n) {
  if (e !== null && (t.dependencies = e.dependencies), On |= t.lanes, !(n & t.childLanes))
    return null;
  if (e !== null && t.child !== e.child)
    throw Error(P(153));
  if (t.child !== null) {
    for (e = t.child, n = fn(e, e.pendingProps), t.child = n, n.return = t; e.sibling !== null; )
      e = e.sibling, n = n.sibling = fn(e, e.pendingProps), n.return = t;
    n.sibling = null;
  }
  return t.child;
}
function Pv(e, t, n) {
  switch (t.tag) {
    case 3:
      Mm(t), fr();
      break;
    case 5:
      om(t);
      break;
    case 1:
      Ve(t.type) && Di(t);
      break;
    case 4:
      ku(t, t.stateNode.containerInfo);
      break;
    case 10:
      var r = t.type._context, o = t.memoizedProps.value;
      X(Wi, r._currentValue), r._currentValue = o;
      break;
    case 13:
      if (r = t.memoizedState, r !== null)
        return r.dehydrated !== null ? (X(re, re.current & 1), t.flags |= 128, null) : n & t.child.childLanes ? Om(e, t, n) : (X(re, re.current & 1), e = Ht(e, t, n), e !== null ? e.sibling : null);
      X(re, re.current & 1);
      break;
    case 19:
      if (r = (n & t.childLanes) !== 0, e.flags & 128) {
        if (r)
          return zm(e, t, n);
        t.flags |= 128;
      }
      if (o = t.memoizedState, o !== null && (o.rendering = null, o.tail = null, o.lastEffect = null), X(re, re.current), r)
        break;
      return null;
    case 22:
    case 23:
      return t.lanes = 0, Tm(e, t, n);
  }
  return Ht(e, t, n);
}
var Nm, za, jm, bm;
Nm = function(e, t) {
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
za = function() {
};
jm = function(e, t, n, r) {
  var o = e.memoizedProps;
  if (o !== r) {
    e = t.stateNode, _n(zt.current);
    var i = null;
    switch (n) {
      case "input":
        o = ea(e, o), r = ea(e, r), i = [];
        break;
      case "select":
        o = ie({}, o, { value: void 0 }), r = ie({}, r, { value: void 0 }), i = [];
        break;
      case "textarea":
        o = ra(e, o), r = ra(e, r), i = [];
        break;
      default:
        typeof o.onClick != "function" && typeof r.onClick == "function" && (e.onclick = Ii);
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
          u !== "dangerouslySetInnerHTML" && u !== "children" && u !== "suppressContentEditableWarning" && u !== "suppressHydrationWarning" && u !== "autoFocus" && (ro.hasOwnProperty(u) ? i || (i = []) : (i = i || []).push(u, null));
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
          u === "dangerouslySetInnerHTML" ? (a = a ? a.__html : void 0, s = s ? s.__html : void 0, a != null && s !== a && (i = i || []).push(u, a)) : u === "children" ? typeof a != "string" && typeof a != "number" || (i = i || []).push(u, "" + a) : u !== "suppressContentEditableWarning" && u !== "suppressHydrationWarning" && (ro.hasOwnProperty(u) ? (a != null && u === "onScroll" && Z("scroll", e), i || s === a || (i = [])) : (i = i || []).push(u, a));
    }
    n && (i = i || []).push("style", n);
    var u = i;
    (t.updateQueue = u) && (t.flags |= 4);
  }
};
bm = function(e, t, n, r) {
  n !== r && (t.flags |= 4);
};
function Ar(e, t) {
  if (!te)
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
function ze(e) {
  var t = e.alternate !== null && e.alternate.child === e.child, n = 0, r = 0;
  if (t)
    for (var o = e.child; o !== null; )
      n |= o.lanes | o.childLanes, r |= o.subtreeFlags & 14680064, r |= o.flags & 14680064, o.return = e, o = o.sibling;
  else
    for (o = e.child; o !== null; )
      n |= o.lanes | o.childLanes, r |= o.subtreeFlags, r |= o.flags, o.return = e, o = o.sibling;
  return e.subtreeFlags |= r, e.childLanes = n, t;
}
function Tv(e, t, n) {
  var r = t.pendingProps;
  switch (gu(t), t.tag) {
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
      return ze(t), null;
    case 1:
      return Ve(t.type) && Li(), ze(t), null;
    case 3:
      return r = t.stateNode, mr(), J(Ue), J(be), $u(), r.pendingContext && (r.context = r.pendingContext, r.pendingContext = null), (e === null || e.child === null) && (ti(t) ? t.flags |= 4 : e === null || e.memoizedState.isDehydrated && !(t.flags & 256) || (t.flags |= 1024, wt !== null && (Fa(wt), wt = null))), za(e, t), ze(t), null;
    case 5:
      _u(t);
      var o = _n(go.current);
      if (n = t.type, e !== null && t.stateNode != null)
        jm(e, t, n, r, o), e.ref !== t.ref && (t.flags |= 512, t.flags |= 2097152);
      else {
        if (!r) {
          if (t.stateNode === null)
            throw Error(P(166));
          return ze(t), null;
        }
        if (e = _n(zt.current), ti(t)) {
          r = t.stateNode, n = t.type;
          var i = t.memoizedProps;
          switch (r[Mt] = t, r[mo] = i, e = (t.mode & 1) !== 0, n) {
            case "dialog":
              Z("cancel", r), Z("close", r);
              break;
            case "iframe":
            case "object":
            case "embed":
              Z("load", r);
              break;
            case "video":
            case "audio":
              for (o = 0; o < Hr.length; o++)
                Z(Hr[o], r);
              break;
            case "source":
              Z("error", r);
              break;
            case "img":
            case "image":
            case "link":
              Z(
                "error",
                r
              ), Z("load", r);
              break;
            case "details":
              Z("toggle", r);
              break;
            case "input":
              jc(r, i), Z("invalid", r);
              break;
            case "select":
              r._wrapperState = { wasMultiple: !!i.multiple }, Z("invalid", r);
              break;
            case "textarea":
              Ac(r, i), Z("invalid", r);
          }
          ia(n, i), o = null;
          for (var l in i)
            if (i.hasOwnProperty(l)) {
              var s = i[l];
              l === "children" ? typeof s == "string" ? r.textContent !== s && (i.suppressHydrationWarning !== !0 && ei(r.textContent, s, e), o = ["children", s]) : typeof s == "number" && r.textContent !== "" + s && (i.suppressHydrationWarning !== !0 && ei(
                r.textContent,
                s,
                e
              ), o = ["children", "" + s]) : ro.hasOwnProperty(l) && s != null && l === "onScroll" && Z("scroll", r);
            }
          switch (n) {
            case "input":
              Ko(r), bc(r, i, !0);
              break;
            case "textarea":
              Ko(r), Ic(r);
              break;
            case "select":
            case "option":
              break;
            default:
              typeof i.onClick == "function" && (r.onclick = Ii);
          }
          r = o, t.updateQueue = r, r !== null && (t.flags |= 4);
        } else {
          l = o.nodeType === 9 ? o : o.ownerDocument, e === "http://www.w3.org/1999/xhtml" && (e = up(n)), e === "http://www.w3.org/1999/xhtml" ? n === "script" ? (e = l.createElement("div"), e.innerHTML = "<script><\/script>", e = e.removeChild(e.firstChild)) : typeof r.is == "string" ? e = l.createElement(n, { is: r.is }) : (e = l.createElement(n), n === "select" && (l = e, r.multiple ? l.multiple = !0 : r.size && (l.size = r.size))) : e = l.createElementNS(e, n), e[Mt] = t, e[mo] = r, Nm(e, t, !1, !1), t.stateNode = e;
          e: {
            switch (l = la(n, r), n) {
              case "dialog":
                Z("cancel", e), Z("close", e), o = r;
                break;
              case "iframe":
              case "object":
              case "embed":
                Z("load", e), o = r;
                break;
              case "video":
              case "audio":
                for (o = 0; o < Hr.length; o++)
                  Z(Hr[o], e);
                o = r;
                break;
              case "source":
                Z("error", e), o = r;
                break;
              case "img":
              case "image":
              case "link":
                Z(
                  "error",
                  e
                ), Z("load", e), o = r;
                break;
              case "details":
                Z("toggle", e), o = r;
                break;
              case "input":
                jc(e, r), o = ea(e, r), Z("invalid", e);
                break;
              case "option":
                o = r;
                break;
              case "select":
                e._wrapperState = { wasMultiple: !!r.multiple }, o = ie({}, r, { value: void 0 }), Z("invalid", e);
                break;
              case "textarea":
                Ac(e, r), o = ra(e, r), Z("invalid", e);
                break;
              default:
                o = r;
            }
            ia(n, o), s = o;
            for (i in s)
              if (s.hasOwnProperty(i)) {
                var a = s[i];
                i === "style" ? fp(e, a) : i === "dangerouslySetInnerHTML" ? (a = a ? a.__html : void 0, a != null && cp(e, a)) : i === "children" ? typeof a == "string" ? (n !== "textarea" || a !== "") && oo(e, a) : typeof a == "number" && oo(e, "" + a) : i !== "suppressContentEditableWarning" && i !== "suppressHydrationWarning" && i !== "autoFocus" && (ro.hasOwnProperty(i) ? a != null && i === "onScroll" && Z("scroll", e) : a != null && tu(e, i, a, l));
              }
            switch (n) {
              case "input":
                Ko(e), bc(e, r, !1);
                break;
              case "textarea":
                Ko(e), Ic(e);
                break;
              case "option":
                r.value != null && e.setAttribute("value", "" + pn(r.value));
                break;
              case "select":
                e.multiple = !!r.multiple, i = r.value, i != null ? tr(e, !!r.multiple, i, !1) : r.defaultValue != null && tr(
                  e,
                  !!r.multiple,
                  r.defaultValue,
                  !0
                );
                break;
              default:
                typeof o.onClick == "function" && (e.onclick = Ii);
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
      return ze(t), null;
    case 6:
      if (e && t.stateNode != null)
        bm(e, t, e.memoizedProps, r);
      else {
        if (typeof r != "string" && t.stateNode === null)
          throw Error(P(166));
        if (n = _n(go.current), _n(zt.current), ti(t)) {
          if (r = t.stateNode, n = t.memoizedProps, r[Mt] = t, (i = r.nodeValue !== n) && (e = qe, e !== null))
            switch (e.tag) {
              case 3:
                ei(r.nodeValue, n, (e.mode & 1) !== 0);
                break;
              case 5:
                e.memoizedProps.suppressHydrationWarning !== !0 && ei(r.nodeValue, n, (e.mode & 1) !== 0);
            }
          i && (t.flags |= 4);
        } else
          r = (n.nodeType === 9 ? n : n.ownerDocument).createTextNode(r), r[Mt] = t, t.stateNode = r;
      }
      return ze(t), null;
    case 13:
      if (J(re), r = t.memoizedState, e === null || e.memoizedState !== null && e.memoizedState.dehydrated !== null) {
        if (te && Xe !== null && t.mode & 1 && !(t.flags & 128))
          Jp(), fr(), t.flags |= 98560, i = !1;
        else if (i = ti(t), r !== null && r.dehydrated !== null) {
          if (e === null) {
            if (!i)
              throw Error(P(318));
            if (i = t.memoizedState, i = i !== null ? i.dehydrated : null, !i)
              throw Error(P(317));
            i[Mt] = t;
          } else
            fr(), !(t.flags & 128) && (t.memoizedState = null), t.flags |= 4;
          ze(t), i = !1;
        } else
          wt !== null && (Fa(wt), wt = null), i = !0;
        if (!i)
          return t.flags & 65536 ? t : null;
      }
      return t.flags & 128 ? (t.lanes = n, t) : (r = r !== null, r !== (e !== null && e.memoizedState !== null) && r && (t.child.flags |= 8192, t.mode & 1 && (e === null || re.current & 1 ? we === 0 && (we = 3) : Iu())), t.updateQueue !== null && (t.flags |= 4), ze(t), null);
    case 4:
      return mr(), za(e, t), e === null && fo(t.stateNode.containerInfo), ze(t), null;
    case 10:
      return Su(t.type._context), ze(t), null;
    case 17:
      return Ve(t.type) && Li(), ze(t), null;
    case 19:
      if (J(re), i = t.memoizedState, i === null)
        return ze(t), null;
      if (r = (t.flags & 128) !== 0, l = i.rendering, l === null)
        if (r)
          Ar(i, !1);
        else {
          if (we !== 0 || e !== null && e.flags & 128)
            for (e = t.child; e !== null; ) {
              if (l = Hi(e), l !== null) {
                for (t.flags |= 128, Ar(i, !1), r = l.updateQueue, r !== null && (t.updateQueue = r, t.flags |= 4), t.subtreeFlags = 0, r = n, n = t.child; n !== null; )
                  i = n, e = r, i.flags &= 14680066, l = i.alternate, l === null ? (i.childLanes = 0, i.lanes = e, i.child = null, i.subtreeFlags = 0, i.memoizedProps = null, i.memoizedState = null, i.updateQueue = null, i.dependencies = null, i.stateNode = null) : (i.childLanes = l.childLanes, i.lanes = l.lanes, i.child = l.child, i.subtreeFlags = 0, i.deletions = null, i.memoizedProps = l.memoizedProps, i.memoizedState = l.memoizedState, i.updateQueue = l.updateQueue, i.type = l.type, e = l.dependencies, i.dependencies = e === null ? null : { lanes: e.lanes, firstContext: e.firstContext }), n = n.sibling;
                return X(re, re.current & 1 | 2), t.child;
              }
              e = e.sibling;
            }
          i.tail !== null && ue() > gr && (t.flags |= 128, r = !0, Ar(i, !1), t.lanes = 4194304);
        }
      else {
        if (!r)
          if (e = Hi(l), e !== null) {
            if (t.flags |= 128, r = !0, n = e.updateQueue, n !== null && (t.updateQueue = n, t.flags |= 4), Ar(i, !0), i.tail === null && i.tailMode === "hidden" && !l.alternate && !te)
              return ze(t), null;
          } else
            2 * ue() - i.renderingStartTime > gr && n !== 1073741824 && (t.flags |= 128, r = !0, Ar(i, !1), t.lanes = 4194304);
        i.isBackwards ? (l.sibling = t.child, t.child = l) : (n = i.last, n !== null ? n.sibling = l : t.child = l, i.last = l);
      }
      return i.tail !== null ? (t = i.tail, i.rendering = t, i.tail = t.sibling, i.renderingStartTime = ue(), t.sibling = null, n = re.current, X(re, r ? n & 1 | 2 : n & 1), t) : (ze(t), null);
    case 22:
    case 23:
      return Au(), r = t.memoizedState !== null, e !== null && e.memoizedState !== null !== r && (t.flags |= 8192), r && t.mode & 1 ? Qe & 1073741824 && (ze(t), t.subtreeFlags & 6 && (t.flags |= 8192)) : ze(t), null;
    case 24:
      return null;
    case 25:
      return null;
  }
  throw Error(P(156, t.tag));
}
function Rv(e, t) {
  switch (gu(t), t.tag) {
    case 1:
      return Ve(t.type) && Li(), e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, t) : null;
    case 3:
      return mr(), J(Ue), J(be), $u(), e = t.flags, e & 65536 && !(e & 128) ? (t.flags = e & -65537 | 128, t) : null;
    case 5:
      return _u(t), null;
    case 13:
      if (J(re), e = t.memoizedState, e !== null && e.dehydrated !== null) {
        if (t.alternate === null)
          throw Error(P(340));
        fr();
      }
      return e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, t) : null;
    case 19:
      return J(re), null;
    case 4:
      return mr(), null;
    case 10:
      return Su(t.type._context), null;
    case 22:
    case 23:
      return Au(), null;
    case 24:
      return null;
    default:
      return null;
  }
}
var oi = !1, je = !1, Mv = typeof WeakSet == "function" ? WeakSet : Set, O = null;
function Jn(e, t) {
  var n = e.ref;
  if (n !== null)
    if (typeof n == "function")
      try {
        n(null);
      } catch (r) {
        ae(e, t, r);
      }
    else
      n.current = null;
}
function Na(e, t, n) {
  try {
    n();
  } catch (r) {
    ae(e, t, r);
  }
}
var Ed = !1;
function Ov(e, t) {
  if (ga = ji, e = Fp(), mu(e)) {
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
  for (va = { focusedElem: e, selectionRange: n }, ji = !1, O = t; O !== null; )
    if (t = O, e = t.child, (t.subtreeFlags & 1028) !== 0 && e !== null)
      e.return = t, O = e;
    else
      for (; O !== null; ) {
        t = O;
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
                  var g = y.memoizedProps, E = y.memoizedState, m = t.stateNode, d = m.getSnapshotBeforeUpdate(t.elementType === t.type ? g : xt(t.type, g), E);
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
        } catch (S) {
          ae(t, t.return, S);
        }
        if (e = t.sibling, e !== null) {
          e.return = t.return, O = e;
          break;
        }
        O = t.return;
      }
  return y = Ed, Ed = !1, y;
}
function Jr(e, t, n) {
  var r = t.updateQueue;
  if (r = r !== null ? r.lastEffect : null, r !== null) {
    var o = r = r.next;
    do {
      if ((o.tag & e) === e) {
        var i = o.destroy;
        o.destroy = void 0, i !== void 0 && Na(t, n, i);
      }
      o = o.next;
    } while (o !== r);
  }
}
function gl(e, t) {
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
function ja(e) {
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
function Am(e) {
  var t = e.alternate;
  t !== null && (e.alternate = null, Am(t)), e.child = null, e.deletions = null, e.sibling = null, e.tag === 5 && (t = e.stateNode, t !== null && (delete t[Mt], delete t[mo], delete t[Sa], delete t[pv], delete t[mv])), e.stateNode = null, e.return = null, e.dependencies = null, e.memoizedProps = null, e.memoizedState = null, e.pendingProps = null, e.stateNode = null, e.updateQueue = null;
}
function Im(e) {
  return e.tag === 5 || e.tag === 3 || e.tag === 4;
}
function Pd(e) {
  e:
    for (; ; ) {
      for (; e.sibling === null; ) {
        if (e.return === null || Im(e.return))
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
function ba(e, t, n) {
  var r = e.tag;
  if (r === 5 || r === 6)
    e = e.stateNode, t ? n.nodeType === 8 ? n.parentNode.insertBefore(e, t) : n.insertBefore(e, t) : (n.nodeType === 8 ? (t = n.parentNode, t.insertBefore(e, n)) : (t = n, t.appendChild(e)), n = n._reactRootContainer, n != null || t.onclick !== null || (t.onclick = Ii));
  else if (r !== 4 && (e = e.child, e !== null))
    for (ba(e, t, n), e = e.sibling; e !== null; )
      ba(e, t, n), e = e.sibling;
}
function Aa(e, t, n) {
  var r = e.tag;
  if (r === 5 || r === 6)
    e = e.stateNode, t ? n.insertBefore(e, t) : n.appendChild(e);
  else if (r !== 4 && (e = e.child, e !== null))
    for (Aa(e, t, n), e = e.sibling; e !== null; )
      Aa(e, t, n), e = e.sibling;
}
var Pe = null, St = !1;
function Yt(e, t, n) {
  for (n = n.child; n !== null; )
    Lm(e, t, n), n = n.sibling;
}
function Lm(e, t, n) {
  if (Ot && typeof Ot.onCommitFiberUnmount == "function")
    try {
      Ot.onCommitFiberUnmount(al, n);
    } catch {
    }
  switch (n.tag) {
    case 5:
      je || Jn(n, t);
    case 6:
      var r = Pe, o = St;
      Pe = null, Yt(e, t, n), Pe = r, St = o, Pe !== null && (St ? (e = Pe, n = n.stateNode, e.nodeType === 8 ? e.parentNode.removeChild(n) : e.removeChild(n)) : Pe.removeChild(n.stateNode));
      break;
    case 18:
      Pe !== null && (St ? (e = Pe, n = n.stateNode, e.nodeType === 8 ? Ps(e.parentNode, n) : e.nodeType === 1 && Ps(e, n), ao(e)) : Ps(Pe, n.stateNode));
      break;
    case 4:
      r = Pe, o = St, Pe = n.stateNode.containerInfo, St = !0, Yt(e, t, n), Pe = r, St = o;
      break;
    case 0:
    case 11:
    case 14:
    case 15:
      if (!je && (r = n.updateQueue, r !== null && (r = r.lastEffect, r !== null))) {
        o = r = r.next;
        do {
          var i = o, l = i.destroy;
          i = i.tag, l !== void 0 && (i & 2 || i & 4) && Na(n, t, l), o = o.next;
        } while (o !== r);
      }
      Yt(e, t, n);
      break;
    case 1:
      if (!je && (Jn(n, t), r = n.stateNode, typeof r.componentWillUnmount == "function"))
        try {
          r.props = n.memoizedProps, r.state = n.memoizedState, r.componentWillUnmount();
        } catch (s) {
          ae(n, t, s);
        }
      Yt(e, t, n);
      break;
    case 21:
      Yt(e, t, n);
      break;
    case 22:
      n.mode & 1 ? (je = (r = je) || n.memoizedState !== null, Yt(e, t, n), je = r) : Yt(e, t, n);
      break;
    default:
      Yt(e, t, n);
  }
}
function Td(e) {
  var t = e.updateQueue;
  if (t !== null) {
    e.updateQueue = null;
    var n = e.stateNode;
    n === null && (n = e.stateNode = new Mv()), t.forEach(function(r) {
      var o = Fv.bind(null, e, r);
      n.has(r) || (n.add(r), r.then(o, o));
    });
  }
}
function yt(e, t) {
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
                Pe = s.stateNode, St = !1;
                break e;
              case 3:
                Pe = s.stateNode.containerInfo, St = !0;
                break e;
              case 4:
                Pe = s.stateNode.containerInfo, St = !0;
                break e;
            }
            s = s.return;
          }
        if (Pe === null)
          throw Error(P(160));
        Lm(i, l, o), Pe = null, St = !1;
        var a = o.alternate;
        a !== null && (a.return = null), o.return = null;
      } catch (u) {
        ae(o, t, u);
      }
    }
  if (t.subtreeFlags & 12854)
    for (t = t.child; t !== null; )
      Dm(t, e), t = t.sibling;
}
function Dm(e, t) {
  var n = e.alternate, r = e.flags;
  switch (e.tag) {
    case 0:
    case 11:
    case 14:
    case 15:
      if (yt(t, e), $t(e), r & 4) {
        try {
          Jr(3, e, e.return), gl(3, e);
        } catch (g) {
          ae(e, e.return, g);
        }
        try {
          Jr(5, e, e.return);
        } catch (g) {
          ae(e, e.return, g);
        }
      }
      break;
    case 1:
      yt(t, e), $t(e), r & 512 && n !== null && Jn(n, n.return);
      break;
    case 5:
      if (yt(t, e), $t(e), r & 512 && n !== null && Jn(n, n.return), e.flags & 32) {
        var o = e.stateNode;
        try {
          oo(o, "");
        } catch (g) {
          ae(e, e.return, g);
        }
      }
      if (r & 4 && (o = e.stateNode, o != null)) {
        var i = e.memoizedProps, l = n !== null ? n.memoizedProps : i, s = e.type, a = e.updateQueue;
        if (e.updateQueue = null, a !== null)
          try {
            s === "input" && i.type === "radio" && i.name != null && sp(o, i), la(s, l);
            var u = la(s, i);
            for (l = 0; l < a.length; l += 2) {
              var c = a[l], f = a[l + 1];
              c === "style" ? fp(o, f) : c === "dangerouslySetInnerHTML" ? cp(o, f) : c === "children" ? oo(o, f) : tu(o, c, f, u);
            }
            switch (s) {
              case "input":
                ta(o, i);
                break;
              case "textarea":
                ap(o, i);
                break;
              case "select":
                var p = o._wrapperState.wasMultiple;
                o._wrapperState.wasMultiple = !!i.multiple;
                var v = i.value;
                v != null ? tr(o, !!i.multiple, v, !1) : p !== !!i.multiple && (i.defaultValue != null ? tr(
                  o,
                  !!i.multiple,
                  i.defaultValue,
                  !0
                ) : tr(o, !!i.multiple, i.multiple ? [] : "", !1));
            }
            o[mo] = i;
          } catch (g) {
            ae(e, e.return, g);
          }
      }
      break;
    case 6:
      if (yt(t, e), $t(e), r & 4) {
        if (e.stateNode === null)
          throw Error(P(162));
        o = e.stateNode, i = e.memoizedProps;
        try {
          o.nodeValue = i;
        } catch (g) {
          ae(e, e.return, g);
        }
      }
      break;
    case 3:
      if (yt(t, e), $t(e), r & 4 && n !== null && n.memoizedState.isDehydrated)
        try {
          ao(t.containerInfo);
        } catch (g) {
          ae(e, e.return, g);
        }
      break;
    case 4:
      yt(t, e), $t(e);
      break;
    case 13:
      yt(t, e), $t(e), o = e.child, o.flags & 8192 && (i = o.memoizedState !== null, o.stateNode.isHidden = i, !i || o.alternate !== null && o.alternate.memoizedState !== null || (ju = ue())), r & 4 && Td(e);
      break;
    case 22:
      if (c = n !== null && n.memoizedState !== null, e.mode & 1 ? (je = (u = je) || c, yt(t, e), je = u) : yt(t, e), $t(e), r & 8192) {
        if (u = e.memoizedState !== null, (e.stateNode.isHidden = u) && !c && e.mode & 1)
          for (O = e, c = e.child; c !== null; ) {
            for (f = O = c; O !== null; ) {
              switch (p = O, v = p.child, p.tag) {
                case 0:
                case 11:
                case 14:
                case 15:
                  Jr(4, p, p.return);
                  break;
                case 1:
                  Jn(p, p.return);
                  var y = p.stateNode;
                  if (typeof y.componentWillUnmount == "function") {
                    r = p, n = p.return;
                    try {
                      t = r, y.props = t.memoizedProps, y.state = t.memoizedState, y.componentWillUnmount();
                    } catch (g) {
                      ae(r, n, g);
                    }
                  }
                  break;
                case 5:
                  Jn(p, p.return);
                  break;
                case 22:
                  if (p.memoizedState !== null) {
                    Md(f);
                    continue;
                  }
              }
              v !== null ? (v.return = p, O = v) : Md(f);
            }
            c = c.sibling;
          }
        e:
          for (c = null, f = e; ; ) {
            if (f.tag === 5) {
              if (c === null) {
                c = f;
                try {
                  o = f.stateNode, u ? (i = o.style, typeof i.setProperty == "function" ? i.setProperty("display", "none", "important") : i.display = "none") : (s = f.stateNode, a = f.memoizedProps.style, l = a != null && a.hasOwnProperty("display") ? a.display : null, s.style.display = dp("display", l));
                } catch (g) {
                  ae(e, e.return, g);
                }
              }
            } else if (f.tag === 6) {
              if (c === null)
                try {
                  f.stateNode.nodeValue = u ? "" : f.memoizedProps;
                } catch (g) {
                  ae(e, e.return, g);
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
      yt(t, e), $t(e), r & 4 && Td(e);
      break;
    case 21:
      break;
    default:
      yt(
        t,
        e
      ), $t(e);
  }
}
function $t(e) {
  var t = e.flags;
  if (t & 2) {
    try {
      e: {
        for (var n = e.return; n !== null; ) {
          if (Im(n)) {
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
          r.flags & 32 && (oo(o, ""), r.flags &= -33);
          var i = Pd(e);
          Aa(e, i, o);
          break;
        case 3:
        case 4:
          var l = r.stateNode.containerInfo, s = Pd(e);
          ba(e, s, l);
          break;
        default:
          throw Error(P(161));
      }
    } catch (a) {
      ae(e, e.return, a);
    }
    e.flags &= -3;
  }
  t & 4096 && (e.flags &= -4097);
}
function zv(e, t, n) {
  O = e, Fm(e);
}
function Fm(e, t, n) {
  for (var r = (e.mode & 1) !== 0; O !== null; ) {
    var o = O, i = o.child;
    if (o.tag === 22 && r) {
      var l = o.memoizedState !== null || oi;
      if (!l) {
        var s = o.alternate, a = s !== null && s.memoizedState !== null || je;
        s = oi;
        var u = je;
        if (oi = l, (je = a) && !u)
          for (O = o; O !== null; )
            l = O, a = l.child, l.tag === 22 && l.memoizedState !== null ? Od(o) : a !== null ? (a.return = l, O = a) : Od(o);
        for (; i !== null; )
          O = i, Fm(i), i = i.sibling;
        O = o, oi = s, je = u;
      }
      Rd(e);
    } else
      o.subtreeFlags & 8772 && i !== null ? (i.return = o, O = i) : Rd(e);
  }
}
function Rd(e) {
  for (; O !== null; ) {
    var t = O;
    if (t.flags & 8772) {
      var n = t.alternate;
      try {
        if (t.flags & 8772)
          switch (t.tag) {
            case 0:
            case 11:
            case 15:
              je || gl(5, t);
              break;
            case 1:
              var r = t.stateNode;
              if (t.flags & 4 && !je)
                if (n === null)
                  r.componentDidMount();
                else {
                  var o = t.elementType === t.type ? n.memoizedProps : xt(t.type, n.memoizedProps);
                  r.componentDidUpdate(o, n.memoizedState, r.__reactInternalSnapshotBeforeUpdate);
                }
              var i = t.updateQueue;
              i !== null && pd(t, i, r);
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
                pd(t, l, n);
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
                    f !== null && ao(f);
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
        je || t.flags & 512 && ja(t);
      } catch (p) {
        ae(t, t.return, p);
      }
    }
    if (t === e) {
      O = null;
      break;
    }
    if (n = t.sibling, n !== null) {
      n.return = t.return, O = n;
      break;
    }
    O = t.return;
  }
}
function Md(e) {
  for (; O !== null; ) {
    var t = O;
    if (t === e) {
      O = null;
      break;
    }
    var n = t.sibling;
    if (n !== null) {
      n.return = t.return, O = n;
      break;
    }
    O = t.return;
  }
}
function Od(e) {
  for (; O !== null; ) {
    var t = O;
    try {
      switch (t.tag) {
        case 0:
        case 11:
        case 15:
          var n = t.return;
          try {
            gl(4, t);
          } catch (a) {
            ae(t, n, a);
          }
          break;
        case 1:
          var r = t.stateNode;
          if (typeof r.componentDidMount == "function") {
            var o = t.return;
            try {
              r.componentDidMount();
            } catch (a) {
              ae(t, o, a);
            }
          }
          var i = t.return;
          try {
            ja(t);
          } catch (a) {
            ae(t, i, a);
          }
          break;
        case 5:
          var l = t.return;
          try {
            ja(t);
          } catch (a) {
            ae(t, l, a);
          }
      }
    } catch (a) {
      ae(t, t.return, a);
    }
    if (t === e) {
      O = null;
      break;
    }
    var s = t.sibling;
    if (s !== null) {
      s.return = t.return, O = s;
      break;
    }
    O = t.return;
  }
}
var Nv = Math.ceil, Qi = Gt.ReactCurrentDispatcher, zu = Gt.ReactCurrentOwner, ct = Gt.ReactCurrentBatchConfig, W = 0, _e = null, ge = null, Re = 0, Qe = 0, er = gn(0), we = 0, So = null, On = 0, vl = 0, Nu = 0, eo = null, Be = null, ju = 0, gr = 1 / 0, At = null, Yi = !1, Ia = null, cn = null, ii = !1, rn = null, Xi = 0, to = 0, La = null, Si = -1, wi = 0;
function Le() {
  return W & 6 ? ue() : Si !== -1 ? Si : Si = ue();
}
function dn(e) {
  return e.mode & 1 ? W & 2 && Re !== 0 ? Re & -Re : gv.transition !== null ? (wi === 0 && (wi = _p()), wi) : (e = K, e !== 0 || (e = window.event, e = e === void 0 ? 16 : Op(e.type)), e) : 1;
}
function kt(e, t, n, r) {
  if (50 < to)
    throw to = 0, La = null, Error(P(185));
  Mo(e, n, r), (!(W & 2) || e !== _e) && (e === _e && (!(W & 2) && (vl |= n), we === 4 && tn(e, Re)), He(e, r), n === 1 && W === 0 && !(t.mode & 1) && (gr = ue() + 500, pl && vn()));
}
function He(e, t) {
  var n = e.callbackNode;
  gg(e, t);
  var r = Ni(e, e === _e ? Re : 0);
  if (r === 0)
    n !== null && Fc(n), e.callbackNode = null, e.callbackPriority = 0;
  else if (t = r & -r, e.callbackPriority !== t) {
    if (n != null && Fc(n), t === 1)
      e.tag === 0 ? hv(zd.bind(null, e)) : Xp(zd.bind(null, e)), dv(function() {
        !(W & 6) && vn();
      }), n = null;
    else {
      switch ($p(r)) {
        case 1:
          n = lu;
          break;
        case 4:
          n = Cp;
          break;
        case 16:
          n = zi;
          break;
        case 536870912:
          n = kp;
          break;
        default:
          n = zi;
      }
      n = Qm(n, Bm.bind(null, e));
    }
    e.callbackPriority = t, e.callbackNode = n;
  }
}
function Bm(e, t) {
  if (Si = -1, wi = 0, W & 6)
    throw Error(P(327));
  var n = e.callbackNode;
  if (lr() && e.callbackNode !== n)
    return null;
  var r = Ni(e, e === _e ? Re : 0);
  if (r === 0)
    return null;
  if (r & 30 || r & e.expiredLanes || t)
    t = qi(e, r);
  else {
    t = r;
    var o = W;
    W |= 2;
    var i = Um();
    (_e !== e || Re !== t) && (At = null, gr = ue() + 500, En(e, t));
    do
      try {
        Av();
        break;
      } catch (s) {
        Wm(e, s);
      }
    while (1);
    xu(), Qi.current = i, W = o, ge !== null ? t = 0 : (_e = null, Re = 0, t = we);
  }
  if (t !== 0) {
    if (t === 2 && (o = da(e), o !== 0 && (r = o, t = Da(e, o))), t === 1)
      throw n = So, En(e, 0), tn(e, r), He(e, ue()), n;
    if (t === 6)
      tn(e, r);
    else {
      if (o = e.current.alternate, !(r & 30) && !jv(o) && (t = qi(e, r), t === 2 && (i = da(e), i !== 0 && (r = i, t = Da(e, i))), t === 1))
        throw n = So, En(e, 0), tn(e, r), He(e, ue()), n;
      switch (e.finishedWork = o, e.finishedLanes = r, t) {
        case 0:
        case 1:
          throw Error(P(345));
        case 2:
          Sn(e, Be, At);
          break;
        case 3:
          if (tn(e, r), (r & 130023424) === r && (t = ju + 500 - ue(), 10 < t)) {
            if (Ni(e, 0) !== 0)
              break;
            if (o = e.suspendedLanes, (o & r) !== r) {
              Le(), e.pingedLanes |= e.suspendedLanes & o;
              break;
            }
            e.timeoutHandle = xa(Sn.bind(null, e, Be, At), t);
            break;
          }
          Sn(e, Be, At);
          break;
        case 4:
          if (tn(e, r), (r & 4194240) === r)
            break;
          for (t = e.eventTimes, o = -1; 0 < r; ) {
            var l = 31 - Ct(r);
            i = 1 << l, l = t[l], l > o && (o = l), r &= ~i;
          }
          if (r = o, r = ue() - r, r = (120 > r ? 120 : 480 > r ? 480 : 1080 > r ? 1080 : 1920 > r ? 1920 : 3e3 > r ? 3e3 : 4320 > r ? 4320 : 1960 * Nv(r / 1960)) - r, 10 < r) {
            e.timeoutHandle = xa(Sn.bind(null, e, Be, At), r);
            break;
          }
          Sn(e, Be, At);
          break;
        case 5:
          Sn(e, Be, At);
          break;
        default:
          throw Error(P(329));
      }
    }
  }
  return He(e, ue()), e.callbackNode === n ? Bm.bind(null, e) : null;
}
function Da(e, t) {
  var n = eo;
  return e.current.memoizedState.isDehydrated && (En(e, t).flags |= 256), e = qi(e, t), e !== 2 && (t = Be, Be = n, t !== null && Fa(t)), e;
}
function Fa(e) {
  Be === null ? Be = e : Be.push.apply(Be, e);
}
function jv(e) {
  for (var t = e; ; ) {
    if (t.flags & 16384) {
      var n = t.updateQueue;
      if (n !== null && (n = n.stores, n !== null))
        for (var r = 0; r < n.length; r++) {
          var o = n[r], i = o.getSnapshot;
          o = o.value;
          try {
            if (!_t(i(), o))
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
function tn(e, t) {
  for (t &= ~Nu, t &= ~vl, e.suspendedLanes |= t, e.pingedLanes &= ~t, e = e.expirationTimes; 0 < t; ) {
    var n = 31 - Ct(t), r = 1 << n;
    e[n] = -1, t &= ~r;
  }
}
function zd(e) {
  if (W & 6)
    throw Error(P(327));
  lr();
  var t = Ni(e, 0);
  if (!(t & 1))
    return He(e, ue()), null;
  var n = qi(e, t);
  if (e.tag !== 0 && n === 2) {
    var r = da(e);
    r !== 0 && (t = r, n = Da(e, r));
  }
  if (n === 1)
    throw n = So, En(e, 0), tn(e, t), He(e, ue()), n;
  if (n === 6)
    throw Error(P(345));
  return e.finishedWork = e.current.alternate, e.finishedLanes = t, Sn(e, Be, At), He(e, ue()), null;
}
function bu(e, t) {
  var n = W;
  W |= 1;
  try {
    return e(t);
  } finally {
    W = n, W === 0 && (gr = ue() + 500, pl && vn());
  }
}
function zn(e) {
  rn !== null && rn.tag === 0 && !(W & 6) && lr();
  var t = W;
  W |= 1;
  var n = ct.transition, r = K;
  try {
    if (ct.transition = null, K = 1, e)
      return e();
  } finally {
    K = r, ct.transition = n, W = t, !(W & 6) && vn();
  }
}
function Au() {
  Qe = er.current, J(er);
}
function En(e, t) {
  e.finishedWork = null, e.finishedLanes = 0;
  var n = e.timeoutHandle;
  if (n !== -1 && (e.timeoutHandle = -1, cv(n)), ge !== null)
    for (n = ge.return; n !== null; ) {
      var r = n;
      switch (gu(r), r.tag) {
        case 1:
          r = r.type.childContextTypes, r != null && Li();
          break;
        case 3:
          mr(), J(Ue), J(be), $u();
          break;
        case 5:
          _u(r);
          break;
        case 4:
          mr();
          break;
        case 13:
          J(re);
          break;
        case 19:
          J(re);
          break;
        case 10:
          Su(r.type._context);
          break;
        case 22:
        case 23:
          Au();
      }
      n = n.return;
    }
  if (_e = e, ge = e = fn(e.current, null), Re = Qe = t, we = 0, So = null, Nu = vl = On = 0, Be = eo = null, kn !== null) {
    for (t = 0; t < kn.length; t++)
      if (n = kn[t], r = n.interleaved, r !== null) {
        n.interleaved = null;
        var o = r.next, i = n.pending;
        if (i !== null) {
          var l = i.next;
          i.next = o, r.next = l;
        }
        n.pending = r;
      }
    kn = null;
  }
  return e;
}
function Wm(e, t) {
  do {
    var n = ge;
    try {
      if (xu(), vi.current = Gi, Ki) {
        for (var r = oe.memoizedState; r !== null; ) {
          var o = r.queue;
          o !== null && (o.pending = null), r = r.next;
        }
        Ki = !1;
      }
      if (Mn = 0, ke = Se = oe = null, Zr = !1, vo = 0, zu.current = null, n === null || n.return === null) {
        we = 1, So = t, ge = null;
        break;
      }
      e: {
        var i = e, l = n.return, s = n, a = t;
        if (t = Re, s.flags |= 32768, a !== null && typeof a == "object" && typeof a.then == "function") {
          var u = a, c = s, f = c.tag;
          if (!(c.mode & 1) && (f === 0 || f === 11 || f === 15)) {
            var p = c.alternate;
            p ? (c.updateQueue = p.updateQueue, c.memoizedState = p.memoizedState, c.lanes = p.lanes) : (c.updateQueue = null, c.memoizedState = null);
          }
          var v = xd(l);
          if (v !== null) {
            v.flags &= -257, Sd(v, l, s, i, t), v.mode & 1 && yd(i, u, t), t = v, a = u;
            var y = t.updateQueue;
            if (y === null) {
              var g = /* @__PURE__ */ new Set();
              g.add(a), t.updateQueue = g;
            } else
              y.add(a);
            break e;
          } else {
            if (!(t & 1)) {
              yd(i, u, t), Iu();
              break e;
            }
            a = Error(P(426));
          }
        } else if (te && s.mode & 1) {
          var E = xd(l);
          if (E !== null) {
            !(E.flags & 65536) && (E.flags |= 256), Sd(E, l, s, i, t), vu(hr(a, s));
            break e;
          }
        }
        i = a = hr(a, s), we !== 4 && (we = 2), eo === null ? eo = [i] : eo.push(i), i = l;
        do {
          switch (i.tag) {
            case 3:
              i.flags |= 65536, t &= -t, i.lanes |= t;
              var m = $m(i, a, t);
              fd(i, m);
              break e;
            case 1:
              s = a;
              var d = i.type, h = i.stateNode;
              if (!(i.flags & 128) && (typeof d.getDerivedStateFromError == "function" || h !== null && typeof h.componentDidCatch == "function" && (cn === null || !cn.has(h)))) {
                i.flags |= 65536, t &= -t, i.lanes |= t;
                var S = Em(i, s, t);
                fd(i, S);
                break e;
              }
          }
          i = i.return;
        } while (i !== null);
      }
      Hm(n);
    } catch ($) {
      t = $, ge === n && n !== null && (ge = n = n.return);
      continue;
    }
    break;
  } while (1);
}
function Um() {
  var e = Qi.current;
  return Qi.current = Gi, e === null ? Gi : e;
}
function Iu() {
  (we === 0 || we === 3 || we === 2) && (we = 4), _e === null || !(On & 268435455) && !(vl & 268435455) || tn(_e, Re);
}
function qi(e, t) {
  var n = W;
  W |= 2;
  var r = Um();
  (_e !== e || Re !== t) && (At = null, En(e, t));
  do
    try {
      bv();
      break;
    } catch (o) {
      Wm(e, o);
    }
  while (1);
  if (xu(), W = n, Qi.current = r, ge !== null)
    throw Error(P(261));
  return _e = null, Re = 0, we;
}
function bv() {
  for (; ge !== null; )
    Vm(ge);
}
function Av() {
  for (; ge !== null && !sg(); )
    Vm(ge);
}
function Vm(e) {
  var t = Gm(e.alternate, e, Qe);
  e.memoizedProps = e.pendingProps, t === null ? Hm(e) : ge = t, zu.current = null;
}
function Hm(e) {
  var t = e;
  do {
    var n = t.alternate;
    if (e = t.return, t.flags & 32768) {
      if (n = Rv(n, t), n !== null) {
        n.flags &= 32767, ge = n;
        return;
      }
      if (e !== null)
        e.flags |= 32768, e.subtreeFlags = 0, e.deletions = null;
      else {
        we = 6, ge = null;
        return;
      }
    } else if (n = Tv(n, t, Qe), n !== null) {
      ge = n;
      return;
    }
    if (t = t.sibling, t !== null) {
      ge = t;
      return;
    }
    ge = t = e;
  } while (t !== null);
  we === 0 && (we = 5);
}
function Sn(e, t, n) {
  var r = K, o = ct.transition;
  try {
    ct.transition = null, K = 1, Iv(e, t, n, r);
  } finally {
    ct.transition = o, K = r;
  }
  return null;
}
function Iv(e, t, n, r) {
  do
    lr();
  while (rn !== null);
  if (W & 6)
    throw Error(P(327));
  n = e.finishedWork;
  var o = e.finishedLanes;
  if (n === null)
    return null;
  if (e.finishedWork = null, e.finishedLanes = 0, n === e.current)
    throw Error(P(177));
  e.callbackNode = null, e.callbackPriority = 0;
  var i = n.lanes | n.childLanes;
  if (vg(e, i), e === _e && (ge = _e = null, Re = 0), !(n.subtreeFlags & 2064) && !(n.flags & 2064) || ii || (ii = !0, Qm(zi, function() {
    return lr(), null;
  })), i = (n.flags & 15990) !== 0, n.subtreeFlags & 15990 || i) {
    i = ct.transition, ct.transition = null;
    var l = K;
    K = 1;
    var s = W;
    W |= 4, zu.current = null, Ov(e, n), Dm(n, e), rv(va), ji = !!ga, va = ga = null, e.current = n, zv(n), ag(), W = s, K = l, ct.transition = i;
  } else
    e.current = n;
  if (ii && (ii = !1, rn = e, Xi = o), i = e.pendingLanes, i === 0 && (cn = null), dg(n.stateNode), He(e, ue()), t !== null)
    for (r = e.onRecoverableError, n = 0; n < t.length; n++)
      o = t[n], r(o.value, { componentStack: o.stack, digest: o.digest });
  if (Yi)
    throw Yi = !1, e = Ia, Ia = null, e;
  return Xi & 1 && e.tag !== 0 && lr(), i = e.pendingLanes, i & 1 ? e === La ? to++ : (to = 0, La = e) : to = 0, vn(), null;
}
function lr() {
  if (rn !== null) {
    var e = $p(Xi), t = ct.transition, n = K;
    try {
      if (ct.transition = null, K = 16 > e ? 16 : e, rn === null)
        var r = !1;
      else {
        if (e = rn, rn = null, Xi = 0, W & 6)
          throw Error(P(331));
        var o = W;
        for (W |= 4, O = e.current; O !== null; ) {
          var i = O, l = i.child;
          if (O.flags & 16) {
            var s = i.deletions;
            if (s !== null) {
              for (var a = 0; a < s.length; a++) {
                var u = s[a];
                for (O = u; O !== null; ) {
                  var c = O;
                  switch (c.tag) {
                    case 0:
                    case 11:
                    case 15:
                      Jr(8, c, i);
                  }
                  var f = c.child;
                  if (f !== null)
                    f.return = c, O = f;
                  else
                    for (; O !== null; ) {
                      c = O;
                      var p = c.sibling, v = c.return;
                      if (Am(c), c === u) {
                        O = null;
                        break;
                      }
                      if (p !== null) {
                        p.return = v, O = p;
                        break;
                      }
                      O = v;
                    }
                }
              }
              var y = i.alternate;
              if (y !== null) {
                var g = y.child;
                if (g !== null) {
                  y.child = null;
                  do {
                    var E = g.sibling;
                    g.sibling = null, g = E;
                  } while (g !== null);
                }
              }
              O = i;
            }
          }
          if (i.subtreeFlags & 2064 && l !== null)
            l.return = i, O = l;
          else
            e:
              for (; O !== null; ) {
                if (i = O, i.flags & 2048)
                  switch (i.tag) {
                    case 0:
                    case 11:
                    case 15:
                      Jr(9, i, i.return);
                  }
                var m = i.sibling;
                if (m !== null) {
                  m.return = i.return, O = m;
                  break e;
                }
                O = i.return;
              }
        }
        var d = e.current;
        for (O = d; O !== null; ) {
          l = O;
          var h = l.child;
          if (l.subtreeFlags & 2064 && h !== null)
            h.return = l, O = h;
          else
            e:
              for (l = d; O !== null; ) {
                if (s = O, s.flags & 2048)
                  try {
                    switch (s.tag) {
                      case 0:
                      case 11:
                      case 15:
                        gl(9, s);
                    }
                  } catch ($) {
                    ae(s, s.return, $);
                  }
                if (s === l) {
                  O = null;
                  break e;
                }
                var S = s.sibling;
                if (S !== null) {
                  S.return = s.return, O = S;
                  break e;
                }
                O = s.return;
              }
        }
        if (W = o, vn(), Ot && typeof Ot.onPostCommitFiberRoot == "function")
          try {
            Ot.onPostCommitFiberRoot(al, e);
          } catch {
          }
        r = !0;
      }
      return r;
    } finally {
      K = n, ct.transition = t;
    }
  }
  return !1;
}
function Nd(e, t, n) {
  t = hr(n, t), t = $m(e, t, 1), e = un(e, t, 1), t = Le(), e !== null && (Mo(e, 1, t), He(e, t));
}
function ae(e, t, n) {
  if (e.tag === 3)
    Nd(e, e, n);
  else
    for (; t !== null; ) {
      if (t.tag === 3) {
        Nd(t, e, n);
        break;
      } else if (t.tag === 1) {
        var r = t.stateNode;
        if (typeof t.type.getDerivedStateFromError == "function" || typeof r.componentDidCatch == "function" && (cn === null || !cn.has(r))) {
          e = hr(n, e), e = Em(t, e, 1), t = un(t, e, 1), e = Le(), t !== null && (Mo(t, 1, e), He(t, e));
          break;
        }
      }
      t = t.return;
    }
}
function Lv(e, t, n) {
  var r = e.pingCache;
  r !== null && r.delete(t), t = Le(), e.pingedLanes |= e.suspendedLanes & n, _e === e && (Re & n) === n && (we === 4 || we === 3 && (Re & 130023424) === Re && 500 > ue() - ju ? En(e, 0) : Nu |= n), He(e, t);
}
function Km(e, t) {
  t === 0 && (e.mode & 1 ? (t = Yo, Yo <<= 1, !(Yo & 130023424) && (Yo = 4194304)) : t = 1);
  var n = Le();
  e = Vt(e, t), e !== null && (Mo(e, t, n), He(e, n));
}
function Dv(e) {
  var t = e.memoizedState, n = 0;
  t !== null && (n = t.retryLane), Km(e, n);
}
function Fv(e, t) {
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
  r !== null && r.delete(t), Km(e, n);
}
var Gm;
Gm = function(e, t, n) {
  if (e !== null)
    if (e.memoizedProps !== t.pendingProps || Ue.current)
      We = !0;
    else {
      if (!(e.lanes & n) && !(t.flags & 128))
        return We = !1, Pv(e, t, n);
      We = !!(e.flags & 131072);
    }
  else
    We = !1, te && t.flags & 1048576 && qp(t, Bi, t.index);
  switch (t.lanes = 0, t.tag) {
    case 2:
      var r = t.type;
      xi(e, t), e = t.pendingProps;
      var o = dr(t, be.current);
      ir(t, n), o = Pu(null, t, r, e, o, n);
      var i = Tu();
      return t.flags |= 1, typeof o == "object" && o !== null && typeof o.render == "function" && o.$$typeof === void 0 ? (t.tag = 1, t.memoizedState = null, t.updateQueue = null, Ve(r) ? (i = !0, Di(t)) : i = !1, t.memoizedState = o.state !== null && o.state !== void 0 ? o.state : null, Cu(t), o.updater = hl, t.stateNode = o, o._reactInternals = t, Ea(t, r, e, n), t = Ra(null, t, r, !0, i, n)) : (t.tag = 0, te && i && hu(t), Ie(null, t, o, n), t = t.child), t;
    case 16:
      r = t.elementType;
      e: {
        switch (xi(e, t), e = t.pendingProps, o = r._init, r = o(r._payload), t.type = r, o = t.tag = Wv(r), e = xt(r, e), o) {
          case 0:
            t = Ta(null, t, r, e, n);
            break e;
          case 1:
            t = kd(null, t, r, e, n);
            break e;
          case 11:
            t = wd(null, t, r, e, n);
            break e;
          case 14:
            t = Cd(null, t, r, xt(r.type, e), n);
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
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : xt(r, o), Ta(e, t, r, o, n);
    case 1:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : xt(r, o), kd(e, t, r, o, n);
    case 3:
      e: {
        if (Mm(t), e === null)
          throw Error(P(387));
        r = t.pendingProps, i = t.memoizedState, o = i.element, rm(e, t), Vi(t, r, null, n);
        var l = t.memoizedState;
        if (r = l.element, i.isDehydrated)
          if (i = { element: r, isDehydrated: !1, cache: l.cache, pendingSuspenseBoundaries: l.pendingSuspenseBoundaries, transitions: l.transitions }, t.updateQueue.baseState = i, t.memoizedState = i, t.flags & 256) {
            o = hr(Error(P(423)), t), t = _d(e, t, r, n, o);
            break e;
          } else if (r !== o) {
            o = hr(Error(P(424)), t), t = _d(e, t, r, n, o);
            break e;
          } else
            for (Xe = an(t.stateNode.containerInfo.firstChild), qe = t, te = !0, wt = null, n = tm(t, null, r, n), t.child = n; n; )
              n.flags = n.flags & -3 | 4096, n = n.sibling;
        else {
          if (fr(), r === o) {
            t = Ht(e, t, n);
            break e;
          }
          Ie(e, t, r, n);
        }
        t = t.child;
      }
      return t;
    case 5:
      return om(t), e === null && ka(t), r = t.type, o = t.pendingProps, i = e !== null ? e.memoizedProps : null, l = o.children, ya(r, o) ? l = null : i !== null && ya(r, i) && (t.flags |= 32), Rm(e, t), Ie(e, t, l, n), t.child;
    case 6:
      return e === null && ka(t), null;
    case 13:
      return Om(e, t, n);
    case 4:
      return ku(t, t.stateNode.containerInfo), r = t.pendingProps, e === null ? t.child = pr(t, null, r, n) : Ie(e, t, r, n), t.child;
    case 11:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : xt(r, o), wd(e, t, r, o, n);
    case 7:
      return Ie(e, t, t.pendingProps, n), t.child;
    case 8:
      return Ie(e, t, t.pendingProps.children, n), t.child;
    case 12:
      return Ie(e, t, t.pendingProps.children, n), t.child;
    case 10:
      e: {
        if (r = t.type._context, o = t.pendingProps, i = t.memoizedProps, l = o.value, X(Wi, r._currentValue), r._currentValue = l, i !== null)
          if (_t(i.value, l)) {
            if (i.children === o.children && !Ue.current) {
              t = Ht(e, t, n);
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
                      a = Bt(-1, n & -n), a.tag = 2;
                      var u = i.updateQueue;
                      if (u !== null) {
                        u = u.shared;
                        var c = u.pending;
                        c === null ? a.next = a : (a.next = c.next, c.next = a), u.pending = a;
                      }
                    }
                    i.lanes |= n, a = i.alternate, a !== null && (a.lanes |= n), _a(
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
                l.lanes |= n, s = l.alternate, s !== null && (s.lanes |= n), _a(l, n, t), l = i.sibling;
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
      return o = t.type, r = t.pendingProps.children, ir(t, n), o = dt(o), r = r(o), t.flags |= 1, Ie(e, t, r, n), t.child;
    case 14:
      return r = t.type, o = xt(r, t.pendingProps), o = xt(r.type, o), Cd(e, t, r, o, n);
    case 15:
      return Pm(e, t, t.type, t.pendingProps, n);
    case 17:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : xt(r, o), xi(e, t), t.tag = 1, Ve(r) ? (e = !0, Di(t)) : e = !1, ir(t, n), _m(t, r, o), Ea(t, r, o, n), Ra(null, t, r, !0, e, n);
    case 19:
      return zm(e, t, n);
    case 22:
      return Tm(e, t, n);
  }
  throw Error(P(156, t.tag));
};
function Qm(e, t) {
  return wp(e, t);
}
function Bv(e, t, n, r) {
  this.tag = e, this.key = n, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.ref = null, this.pendingProps = t, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = r, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
}
function at(e, t, n, r) {
  return new Bv(e, t, n, r);
}
function Lu(e) {
  return e = e.prototype, !(!e || !e.isReactComponent);
}
function Wv(e) {
  if (typeof e == "function")
    return Lu(e) ? 1 : 0;
  if (e != null) {
    if (e = e.$$typeof, e === ru)
      return 11;
    if (e === ou)
      return 14;
  }
  return 2;
}
function fn(e, t) {
  var n = e.alternate;
  return n === null ? (n = at(e.tag, t, e.key, e.mode), n.elementType = e.elementType, n.type = e.type, n.stateNode = e.stateNode, n.alternate = e, e.alternate = n) : (n.pendingProps = t, n.type = e.type, n.flags = 0, n.subtreeFlags = 0, n.deletions = null), n.flags = e.flags & 14680064, n.childLanes = e.childLanes, n.lanes = e.lanes, n.child = e.child, n.memoizedProps = e.memoizedProps, n.memoizedState = e.memoizedState, n.updateQueue = e.updateQueue, t = e.dependencies, n.dependencies = t === null ? null : { lanes: t.lanes, firstContext: t.firstContext }, n.sibling = e.sibling, n.index = e.index, n.ref = e.ref, n;
}
function Ci(e, t, n, r, o, i) {
  var l = 2;
  if (r = e, typeof e == "function")
    Lu(e) && (l = 1);
  else if (typeof e == "string")
    l = 5;
  else
    e:
      switch (e) {
        case Vn:
          return Pn(n.children, o, i, t);
        case nu:
          l = 8, o |= 8;
          break;
        case Xs:
          return e = at(12, n, t, o | 2), e.elementType = Xs, e.lanes = i, e;
        case qs:
          return e = at(13, n, t, o), e.elementType = qs, e.lanes = i, e;
        case Zs:
          return e = at(19, n, t, o), e.elementType = Zs, e.lanes = i, e;
        case op:
          return yl(n, o, i, t);
        default:
          if (typeof e == "object" && e !== null)
            switch (e.$$typeof) {
              case np:
                l = 10;
                break e;
              case rp:
                l = 9;
                break e;
              case ru:
                l = 11;
                break e;
              case ou:
                l = 14;
                break e;
              case Zt:
                l = 16, r = null;
                break e;
            }
          throw Error(P(130, e == null ? e : typeof e, ""));
      }
  return t = at(l, n, t, o), t.elementType = e, t.type = r, t.lanes = i, t;
}
function Pn(e, t, n, r) {
  return e = at(7, e, r, t), e.lanes = n, e;
}
function yl(e, t, n, r) {
  return e = at(22, e, r, t), e.elementType = op, e.lanes = n, e.stateNode = { isHidden: !1 }, e;
}
function bs(e, t, n) {
  return e = at(6, e, null, t), e.lanes = n, e;
}
function As(e, t, n) {
  return t = at(4, e.children !== null ? e.children : [], e.key, t), t.lanes = n, t.stateNode = { containerInfo: e.containerInfo, pendingChildren: null, implementation: e.implementation }, t;
}
function Uv(e, t, n, r, o) {
  this.tag = t, this.containerInfo = e, this.finishedWork = this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.pendingContext = this.context = null, this.callbackPriority = 0, this.eventTimes = gs(0), this.expirationTimes = gs(-1), this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = gs(0), this.identifierPrefix = r, this.onRecoverableError = o, this.mutableSourceEagerHydrationData = null;
}
function Du(e, t, n, r, o, i, l, s, a) {
  return e = new Uv(e, t, n, s, a), t === 1 ? (t = 1, i === !0 && (t |= 8)) : t = 0, i = at(3, null, null, t), e.current = i, i.stateNode = e, i.memoizedState = { element: r, isDehydrated: n, cache: null, transitions: null, pendingSuspenseBoundaries: null }, Cu(i), e;
}
function Vv(e, t, n) {
  var r = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
  return { $$typeof: Un, key: r == null ? null : "" + r, children: e, containerInfo: t, implementation: n };
}
function Ym(e) {
  if (!e)
    return mn;
  e = e._reactInternals;
  e: {
    if (jn(e) !== e || e.tag !== 1)
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
      return Yp(e, n, t);
  }
  return t;
}
function Xm(e, t, n, r, o, i, l, s, a) {
  return e = Du(n, r, !0, e, o, i, l, s, a), e.context = Ym(null), n = e.current, r = Le(), o = dn(n), i = Bt(r, o), i.callback = t ?? null, un(n, i, o), e.current.lanes = o, Mo(e, o, r), He(e, r), e;
}
function xl(e, t, n, r) {
  var o = t.current, i = Le(), l = dn(o);
  return n = Ym(n), t.context === null ? t.context = n : t.pendingContext = n, t = Bt(i, l), t.payload = { element: e }, r = r === void 0 ? null : r, r !== null && (t.callback = r), e = un(o, t, l), e !== null && (kt(e, o, l, i), gi(e, o, l)), l;
}
function Zi(e) {
  if (e = e.current, !e.child)
    return null;
  switch (e.child.tag) {
    case 5:
      return e.child.stateNode;
    default:
      return e.child.stateNode;
  }
}
function jd(e, t) {
  if (e = e.memoizedState, e !== null && e.dehydrated !== null) {
    var n = e.retryLane;
    e.retryLane = n !== 0 && n < t ? n : t;
  }
}
function Fu(e, t) {
  jd(e, t), (e = e.alternate) && jd(e, t);
}
function Hv() {
  return null;
}
var qm = typeof reportError == "function" ? reportError : function(e) {
  console.error(e);
};
function Bu(e) {
  this._internalRoot = e;
}
Sl.prototype.render = Bu.prototype.render = function(e) {
  var t = this._internalRoot;
  if (t === null)
    throw Error(P(409));
  xl(e, t, null, null);
};
Sl.prototype.unmount = Bu.prototype.unmount = function() {
  var e = this._internalRoot;
  if (e !== null) {
    this._internalRoot = null;
    var t = e.containerInfo;
    zn(function() {
      xl(null, e, null, null);
    }), t[Ut] = null;
  }
};
function Sl(e) {
  this._internalRoot = e;
}
Sl.prototype.unstable_scheduleHydration = function(e) {
  if (e) {
    var t = Tp();
    e = { blockedOn: null, target: e, priority: t };
    for (var n = 0; n < en.length && t !== 0 && t < en[n].priority; n++)
      ;
    en.splice(n, 0, e), n === 0 && Mp(e);
  }
};
function Wu(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11);
}
function wl(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11 && (e.nodeType !== 8 || e.nodeValue !== " react-mount-point-unstable "));
}
function bd() {
}
function Kv(e, t, n, r, o) {
  if (o) {
    if (typeof r == "function") {
      var i = r;
      r = function() {
        var u = Zi(l);
        i.call(u);
      };
    }
    var l = Xm(t, r, e, 0, null, !1, !1, "", bd);
    return e._reactRootContainer = l, e[Ut] = l.current, fo(e.nodeType === 8 ? e.parentNode : e), zn(), l;
  }
  for (; o = e.lastChild; )
    e.removeChild(o);
  if (typeof r == "function") {
    var s = r;
    r = function() {
      var u = Zi(a);
      s.call(u);
    };
  }
  var a = Du(e, 0, !1, null, null, !1, !1, "", bd);
  return e._reactRootContainer = a, e[Ut] = a.current, fo(e.nodeType === 8 ? e.parentNode : e), zn(function() {
    xl(t, a, n, r);
  }), a;
}
function Cl(e, t, n, r, o) {
  var i = n._reactRootContainer;
  if (i) {
    var l = i;
    if (typeof o == "function") {
      var s = o;
      o = function() {
        var a = Zi(l);
        s.call(a);
      };
    }
    xl(t, l, e, o);
  } else
    l = Kv(n, t, e, o, r);
  return Zi(l);
}
Ep = function(e) {
  switch (e.tag) {
    case 3:
      var t = e.stateNode;
      if (t.current.memoizedState.isDehydrated) {
        var n = Vr(t.pendingLanes);
        n !== 0 && (su(t, n | 1), He(t, ue()), !(W & 6) && (gr = ue() + 500, vn()));
      }
      break;
    case 13:
      zn(function() {
        var r = Vt(e, 1);
        if (r !== null) {
          var o = Le();
          kt(r, e, 1, o);
        }
      }), Fu(e, 1);
  }
};
au = function(e) {
  if (e.tag === 13) {
    var t = Vt(e, 134217728);
    if (t !== null) {
      var n = Le();
      kt(t, e, 134217728, n);
    }
    Fu(e, 134217728);
  }
};
Pp = function(e) {
  if (e.tag === 13) {
    var t = dn(e), n = Vt(e, t);
    if (n !== null) {
      var r = Le();
      kt(n, e, t, r);
    }
    Fu(e, t);
  }
};
Tp = function() {
  return K;
};
Rp = function(e, t) {
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
            var o = fl(r);
            if (!o)
              throw Error(P(90));
            lp(r), ta(r, o);
          }
        }
      }
      break;
    case "textarea":
      ap(e, n);
      break;
    case "select":
      t = n.value, t != null && tr(e, !!n.multiple, t, !1);
  }
};
hp = bu;
gp = zn;
var Gv = { usingClientEntryPoint: !1, Events: [zo, Qn, fl, pp, mp, bu] }, Ir = { findFiberByHostInstance: Cn, bundleType: 0, version: "18.3.1", rendererPackageName: "react-dom" }, Qv = { bundleType: Ir.bundleType, version: Ir.version, rendererPackageName: Ir.rendererPackageName, rendererConfig: Ir.rendererConfig, overrideHookState: null, overrideHookStateDeletePath: null, overrideHookStateRenamePath: null, overrideProps: null, overridePropsDeletePath: null, overridePropsRenamePath: null, setErrorHandler: null, setSuspenseHandler: null, scheduleUpdate: null, currentDispatcherRef: Gt.ReactCurrentDispatcher, findHostInstanceByFiber: function(e) {
  return e = xp(e), e === null ? null : e.stateNode;
}, findFiberByHostInstance: Ir.findFiberByHostInstance || Hv, findHostInstancesForRefresh: null, scheduleRefresh: null, scheduleRoot: null, setRefreshHandler: null, getCurrentFiber: null, reconcilerVersion: "18.3.1-next-f1338f8080-20240426" };
if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u") {
  var li = __REACT_DEVTOOLS_GLOBAL_HOOK__;
  if (!li.isDisabled && li.supportsFiber)
    try {
      al = li.inject(Qv), Ot = li;
    } catch {
    }
}
et.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = Gv;
et.createPortal = function(e, t) {
  var n = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
  if (!Wu(t))
    throw Error(P(200));
  return Vv(e, t, null, n);
};
et.createRoot = function(e, t) {
  if (!Wu(e))
    throw Error(P(299));
  var n = !1, r = "", o = qm;
  return t != null && (t.unstable_strictMode === !0 && (n = !0), t.identifierPrefix !== void 0 && (r = t.identifierPrefix), t.onRecoverableError !== void 0 && (o = t.onRecoverableError)), t = Du(e, 1, !1, null, null, n, !1, r, o), e[Ut] = t.current, fo(e.nodeType === 8 ? e.parentNode : e), new Bu(t);
};
et.findDOMNode = function(e) {
  if (e == null)
    return null;
  if (e.nodeType === 1)
    return e;
  var t = e._reactInternals;
  if (t === void 0)
    throw typeof e.render == "function" ? Error(P(188)) : (e = Object.keys(e).join(","), Error(P(268, e)));
  return e = xp(t), e = e === null ? null : e.stateNode, e;
};
et.flushSync = function(e) {
  return zn(e);
};
et.hydrate = function(e, t, n) {
  if (!wl(t))
    throw Error(P(200));
  return Cl(null, e, t, !0, n);
};
et.hydrateRoot = function(e, t, n) {
  if (!Wu(e))
    throw Error(P(405));
  var r = n != null && n.hydratedSources || null, o = !1, i = "", l = qm;
  if (n != null && (n.unstable_strictMode === !0 && (o = !0), n.identifierPrefix !== void 0 && (i = n.identifierPrefix), n.onRecoverableError !== void 0 && (l = n.onRecoverableError)), t = Xm(t, null, e, 1, n ?? null, o, !1, i, l), e[Ut] = t.current, fo(e), r)
    for (e = 0; e < r.length; e++)
      n = r[e], o = n._getVersion, o = o(n._source), t.mutableSourceEagerHydrationData == null ? t.mutableSourceEagerHydrationData = [n, o] : t.mutableSourceEagerHydrationData.push(
        n,
        o
      );
  return new Sl(t);
};
et.render = function(e, t, n) {
  if (!wl(t))
    throw Error(P(200));
  return Cl(null, e, t, !1, n);
};
et.unmountComponentAtNode = function(e) {
  if (!wl(e))
    throw Error(P(40));
  return e._reactRootContainer ? (zn(function() {
    Cl(null, null, e, !1, function() {
      e._reactRootContainer = null, e[Ut] = null;
    });
  }), !0) : !1;
};
et.unstable_batchedUpdates = bu;
et.unstable_renderSubtreeIntoContainer = function(e, t, n, r) {
  if (!wl(n))
    throw Error(P(200));
  if (e == null || e._reactInternals === void 0)
    throw Error(P(38));
  return Cl(e, t, n, !1, r);
};
et.version = "18.3.1-next-f1338f8080-20240426";
function Zm() {
  if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function"))
    try {
      __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(Zm);
    } catch (e) {
      console.error(e);
    }
}
Zm(), Zf.exports = et;
var Yv = Zf.exports, Ad = Yv;
Qs.createRoot = Ad.createRoot, Qs.hydrateRoot = Ad.hydrateRoot;
function wo(e) {
  let t = "https://mui.com/production-error/?code=" + e;
  for (let n = 1; n < arguments.length; n += 1)
    t += "&args[]=" + encodeURIComponent(arguments[n]);
  return "Minified MUI error #" + e + "; visit " + t + " for the full message.";
}
const Xv = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: wo
}, Symbol.toStringTag, { value: "Module" })), vr = "$$material";
function w() {
  return w = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t];
      for (var r in n)
        ({}).hasOwnProperty.call(n, r) && (e[r] = n[r]);
    }
    return e;
  }, w.apply(null, arguments);
}
function L(e, t) {
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
var qv = !1;
function Zv(e) {
  if (e.sheet)
    return e.sheet;
  for (var t = 0; t < document.styleSheets.length; t++)
    if (document.styleSheets[t].ownerNode === e)
      return document.styleSheets[t];
}
function Jv(e) {
  var t = document.createElement("style");
  return t.setAttribute("data-emotion", e.key), e.nonce !== void 0 && t.setAttribute("nonce", e.nonce), t.appendChild(document.createTextNode("")), t.setAttribute("data-s", ""), t;
}
var ey = /* @__PURE__ */ function() {
  function e(n) {
    var r = this;
    this._insertTag = function(o) {
      var i;
      r.tags.length === 0 ? r.insertionPoint ? i = r.insertionPoint.nextSibling : r.prepend ? i = r.container.firstChild : i = r.before : i = r.tags[r.tags.length - 1].nextSibling, r.container.insertBefore(o, i), r.tags.push(o);
    }, this.isSpeedy = n.speedy === void 0 ? !qv : n.speedy, this.tags = [], this.ctr = 0, this.nonce = n.nonce, this.key = n.key, this.container = n.container, this.prepend = n.prepend, this.insertionPoint = n.insertionPoint, this.before = null;
  }
  var t = e.prototype;
  return t.hydrate = function(r) {
    r.forEach(this._insertTag);
  }, t.insert = function(r) {
    this.ctr % (this.isSpeedy ? 65e3 : 1) === 0 && this._insertTag(Jv(this));
    var o = this.tags[this.tags.length - 1];
    if (this.isSpeedy) {
      var i = Zv(o);
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
}(), Ne = "-ms-", Ji = "-moz-", V = "-webkit-", Jm = "comm", Uu = "rule", Vu = "decl", ty = "@import", eh = "@keyframes", ny = "@layer", ry = Math.abs, kl = String.fromCharCode, oy = Object.assign;
function iy(e, t) {
  return Te(e, 0) ^ 45 ? (((t << 2 ^ Te(e, 0)) << 2 ^ Te(e, 1)) << 2 ^ Te(e, 2)) << 2 ^ Te(e, 3) : 0;
}
function th(e) {
  return e.trim();
}
function ly(e, t) {
  return (e = t.exec(e)) ? e[0] : e;
}
function H(e, t, n) {
  return e.replace(t, n);
}
function Ba(e, t) {
  return e.indexOf(t);
}
function Te(e, t) {
  return e.charCodeAt(t) | 0;
}
function Co(e, t, n) {
  return e.slice(t, n);
}
function Tt(e) {
  return e.length;
}
function Hu(e) {
  return e.length;
}
function si(e, t) {
  return t.push(e), e;
}
function sy(e, t) {
  return e.map(t).join("");
}
var _l = 1, yr = 1, nh = 0, Ke = 0, he = 0, Cr = "";
function $l(e, t, n, r, o, i, l) {
  return { value: e, root: t, parent: n, type: r, props: o, children: i, line: _l, column: yr, length: l, return: "" };
}
function Lr(e, t) {
  return oy($l("", null, null, "", null, null, 0), e, { length: -e.length }, t);
}
function ay() {
  return he;
}
function uy() {
  return he = Ke > 0 ? Te(Cr, --Ke) : 0, yr--, he === 10 && (yr = 1, _l--), he;
}
function Ze() {
  return he = Ke < nh ? Te(Cr, Ke++) : 0, yr++, he === 10 && (yr = 1, _l++), he;
}
function Nt() {
  return Te(Cr, Ke);
}
function ki() {
  return Ke;
}
function jo(e, t) {
  return Co(Cr, e, t);
}
function ko(e) {
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
function rh(e) {
  return _l = yr = 1, nh = Tt(Cr = e), Ke = 0, [];
}
function oh(e) {
  return Cr = "", e;
}
function _i(e) {
  return th(jo(Ke - 1, Wa(e === 91 ? e + 2 : e === 40 ? e + 1 : e)));
}
function cy(e) {
  for (; (he = Nt()) && he < 33; )
    Ze();
  return ko(e) > 2 || ko(he) > 3 ? "" : " ";
}
function dy(e, t) {
  for (; --t && Ze() && !(he < 48 || he > 102 || he > 57 && he < 65 || he > 70 && he < 97); )
    ;
  return jo(e, ki() + (t < 6 && Nt() == 32 && Ze() == 32));
}
function Wa(e) {
  for (; Ze(); )
    switch (he) {
      case e:
        return Ke;
      case 34:
      case 39:
        e !== 34 && e !== 39 && Wa(he);
        break;
      case 40:
        e === 41 && Wa(e);
        break;
      case 92:
        Ze();
        break;
    }
  return Ke;
}
function fy(e, t) {
  for (; Ze() && e + he !== 47 + 10; )
    if (e + he === 42 + 42 && Nt() === 47)
      break;
  return "/*" + jo(t, Ke - 1) + "*" + kl(e === 47 ? e : Ze());
}
function py(e) {
  for (; !ko(Nt()); )
    Ze();
  return jo(e, Ke);
}
function my(e) {
  return oh($i("", null, null, null, [""], e = rh(e), 0, [0], e));
}
function $i(e, t, n, r, o, i, l, s, a) {
  for (var u = 0, c = 0, f = l, p = 0, v = 0, y = 0, g = 1, E = 1, m = 1, d = 0, h = "", S = o, $ = i, k = r, C = h; E; )
    switch (y = d, d = Ze()) {
      case 40:
        if (y != 108 && Te(C, f - 1) == 58) {
          Ba(C += H(_i(d), "&", "&\f"), "&\f") != -1 && (m = -1);
          break;
        }
      case 34:
      case 39:
      case 91:
        C += _i(d);
        break;
      case 9:
      case 10:
      case 13:
      case 32:
        C += cy(y);
        break;
      case 92:
        C += dy(ki() - 1, 7);
        continue;
      case 47:
        switch (Nt()) {
          case 42:
          case 47:
            si(hy(fy(Ze(), ki()), t, n), a);
            break;
          default:
            C += "/";
        }
        break;
      case 123 * g:
        s[u++] = Tt(C) * m;
      case 125 * g:
      case 59:
      case 0:
        switch (d) {
          case 0:
          case 125:
            E = 0;
          case 59 + c:
            m == -1 && (C = H(C, /\f/g, "")), v > 0 && Tt(C) - f && si(v > 32 ? Ld(C + ";", r, n, f - 1) : Ld(H(C, " ", "") + ";", r, n, f - 2), a);
            break;
          case 59:
            C += ";";
          default:
            if (si(k = Id(C, t, n, u, c, o, s, h, S = [], $ = [], f), i), d === 123)
              if (c === 0)
                $i(C, t, k, k, S, i, f, s, $);
              else
                switch (p === 99 && Te(C, 3) === 110 ? 100 : p) {
                  case 100:
                  case 108:
                  case 109:
                  case 115:
                    $i(e, k, k, r && si(Id(e, k, k, 0, 0, o, s, h, o, S = [], f), $), o, $, f, s, r ? S : $);
                    break;
                  default:
                    $i(C, k, k, k, [""], $, 0, s, $);
                }
        }
        u = c = v = 0, g = m = 1, h = C = "", f = l;
        break;
      case 58:
        f = 1 + Tt(C), v = y;
      default:
        if (g < 1) {
          if (d == 123)
            --g;
          else if (d == 125 && g++ == 0 && uy() == 125)
            continue;
        }
        switch (C += kl(d), d * g) {
          case 38:
            m = c > 0 ? 1 : (C += "\f", -1);
            break;
          case 44:
            s[u++] = (Tt(C) - 1) * m, m = 1;
            break;
          case 64:
            Nt() === 45 && (C += _i(Ze())), p = Nt(), c = f = Tt(h = C += py(ki())), d++;
            break;
          case 45:
            y === 45 && Tt(C) == 2 && (g = 0);
        }
    }
  return i;
}
function Id(e, t, n, r, o, i, l, s, a, u, c) {
  for (var f = o - 1, p = o === 0 ? i : [""], v = Hu(p), y = 0, g = 0, E = 0; y < r; ++y)
    for (var m = 0, d = Co(e, f + 1, f = ry(g = l[y])), h = e; m < v; ++m)
      (h = th(g > 0 ? p[m] + " " + d : H(d, /&\f/g, p[m]))) && (a[E++] = h);
  return $l(e, t, n, o === 0 ? Uu : s, a, u, c);
}
function hy(e, t, n) {
  return $l(e, t, n, Jm, kl(ay()), Co(e, 2, -2), 0);
}
function Ld(e, t, n, r) {
  return $l(e, t, n, Vu, Co(e, 0, r), Co(e, r + 1, -1), r);
}
function sr(e, t) {
  for (var n = "", r = Hu(e), o = 0; o < r; o++)
    n += t(e[o], o, e, t) || "";
  return n;
}
function gy(e, t, n, r) {
  switch (e.type) {
    case ny:
      if (e.children.length)
        break;
    case ty:
    case Vu:
      return e.return = e.return || e.value;
    case Jm:
      return "";
    case eh:
      return e.return = e.value + "{" + sr(e.children, r) + "}";
    case Uu:
      e.value = e.props.join(",");
  }
  return Tt(n = sr(e.children, r)) ? e.return = e.value + "{" + n + "}" : "";
}
function vy(e) {
  var t = Hu(e);
  return function(n, r, o, i) {
    for (var l = "", s = 0; s < t; s++)
      l += e[s](n, r, o, i) || "";
    return l;
  };
}
function yy(e) {
  return function(t) {
    t.root || (t = t.return) && e(t);
  };
}
function ih(e) {
  var t = /* @__PURE__ */ Object.create(null);
  return function(n) {
    return t[n] === void 0 && (t[n] = e(n)), t[n];
  };
}
var xy = function(t, n, r) {
  for (var o = 0, i = 0; o = i, i = Nt(), o === 38 && i === 12 && (n[r] = 1), !ko(i); )
    Ze();
  return jo(t, Ke);
}, Sy = function(t, n) {
  var r = -1, o = 44;
  do
    switch (ko(o)) {
      case 0:
        o === 38 && Nt() === 12 && (n[r] = 1), t[r] += xy(Ke - 1, n, r);
        break;
      case 2:
        t[r] += _i(o);
        break;
      case 4:
        if (o === 44) {
          t[++r] = Nt() === 58 ? "&\f" : "", n[r] = t[r].length;
          break;
        }
      default:
        t[r] += kl(o);
    }
  while (o = Ze());
  return t;
}, wy = function(t, n) {
  return oh(Sy(rh(t), n));
}, Dd = /* @__PURE__ */ new WeakMap(), Cy = function(t) {
  if (!(t.type !== "rule" || !t.parent || // positive .length indicates that this rule contains pseudo
  // negative .length indicates that this rule has been already prefixed
  t.length < 1)) {
    for (var n = t.value, r = t.parent, o = t.column === r.column && t.line === r.line; r.type !== "rule"; )
      if (r = r.parent, !r)
        return;
    if (!(t.props.length === 1 && n.charCodeAt(0) !== 58 && !Dd.get(r)) && !o) {
      Dd.set(t, !0);
      for (var i = [], l = wy(n, i), s = r.props, a = 0, u = 0; a < l.length; a++)
        for (var c = 0; c < s.length; c++, u++)
          t.props[u] = i[a] ? l[a].replace(/&\f/g, s[c]) : s[c] + " " + l[a];
    }
  }
}, ky = function(t) {
  if (t.type === "decl") {
    var n = t.value;
    // charcode for l
    n.charCodeAt(0) === 108 && // charcode for b
    n.charCodeAt(2) === 98 && (t.return = "", t.value = "");
  }
};
function lh(e, t) {
  switch (iy(e, t)) {
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
      return V + e + Ji + e + Ne + e + e;
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
      if (Tt(e) - 1 - t > 6)
        switch (Te(e, t + 1)) {
          case 109:
            if (Te(e, t + 4) !== 45)
              break;
          case 102:
            return H(e, /(.+:)(.+)-([^]+)/, "$1" + V + "$2-$3$1" + Ji + (Te(e, t + 3) == 108 ? "$3" : "$2-$3")) + e;
          case 115:
            return ~Ba(e, "stretch") ? lh(H(e, "stretch", "fill-available"), t) + e : e;
        }
      break;
    case 4949:
      if (Te(e, t + 1) !== 115)
        break;
    case 6444:
      switch (Te(e, Tt(e) - 3 - (~Ba(e, "!important") && 10))) {
        case 107:
          return H(e, ":", ":" + V) + e;
        case 101:
          return H(e, /(.+:)([^;!]+)(;|!.+)?/, "$1" + V + (Te(e, 14) === 45 ? "inline-" : "") + "box$3$1" + V + "$2$3$1" + Ne + "$2box$3") + e;
      }
      break;
    case 5936:
      switch (Te(e, t + 11)) {
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
var _y = function(t, n, r, o) {
  if (t.length > -1 && !t.return)
    switch (t.type) {
      case Vu:
        t.return = lh(t.value, t.length);
        break;
      case eh:
        return sr([Lr(t, {
          value: H(t.value, "@", "@" + V)
        })], o);
      case Uu:
        if (t.length)
          return sy(t.props, function(i) {
            switch (ly(i, /(::plac\w+|:read-\w+)/)) {
              case ":read-only":
              case ":read-write":
                return sr([Lr(t, {
                  props: [H(i, /:(read-\w+)/, ":" + Ji + "$1")]
                })], o);
              case "::placeholder":
                return sr([Lr(t, {
                  props: [H(i, /:(plac\w+)/, ":" + V + "input-$1")]
                }), Lr(t, {
                  props: [H(i, /:(plac\w+)/, ":" + Ji + "$1")]
                }), Lr(t, {
                  props: [H(i, /:(plac\w+)/, Ne + "input-$1")]
                })], o);
            }
            return "";
          });
    }
}, $y = [_y], sh = function(t) {
  var n = t.key;
  if (n === "css") {
    var r = document.querySelectorAll("style[data-emotion]:not([data-s])");
    Array.prototype.forEach.call(r, function(g) {
      var E = g.getAttribute("data-emotion");
      E.indexOf(" ") !== -1 && (document.head.appendChild(g), g.setAttribute("data-s", ""));
    });
  }
  var o = t.stylisPlugins || $y, i = {}, l, s = [];
  l = t.container || document.head, Array.prototype.forEach.call(
    // this means we will ignore elements which don't have a space in them which
    // means that the style elements we're looking at are only Emotion 11 server-rendered style elements
    document.querySelectorAll('style[data-emotion^="' + n + ' "]'),
    function(g) {
      for (var E = g.getAttribute("data-emotion").split(" "), m = 1; m < E.length; m++)
        i[E[m]] = !0;
      s.push(g);
    }
  );
  var a, u = [Cy, ky];
  {
    var c, f = [gy, yy(function(g) {
      c.insert(g);
    })], p = vy(u.concat(o, f)), v = function(E) {
      return sr(my(E), p);
    };
    a = function(E, m, d, h) {
      c = d, v(E ? E + "{" + m.styles + "}" : m.styles), h && (y.inserted[m.name] = !0);
    };
  }
  var y = {
    key: n,
    sheet: new ey({
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
}, ah = { exports: {} }, G = {};
/** @license React v16.13.1
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var $e = typeof Symbol == "function" && Symbol.for, Ku = $e ? Symbol.for("react.element") : 60103, Gu = $e ? Symbol.for("react.portal") : 60106, El = $e ? Symbol.for("react.fragment") : 60107, Pl = $e ? Symbol.for("react.strict_mode") : 60108, Tl = $e ? Symbol.for("react.profiler") : 60114, Rl = $e ? Symbol.for("react.provider") : 60109, Ml = $e ? Symbol.for("react.context") : 60110, Qu = $e ? Symbol.for("react.async_mode") : 60111, Ol = $e ? Symbol.for("react.concurrent_mode") : 60111, zl = $e ? Symbol.for("react.forward_ref") : 60112, Nl = $e ? Symbol.for("react.suspense") : 60113, Ey = $e ? Symbol.for("react.suspense_list") : 60120, jl = $e ? Symbol.for("react.memo") : 60115, bl = $e ? Symbol.for("react.lazy") : 60116, Py = $e ? Symbol.for("react.block") : 60121, Ty = $e ? Symbol.for("react.fundamental") : 60117, Ry = $e ? Symbol.for("react.responder") : 60118, My = $e ? Symbol.for("react.scope") : 60119;
function nt(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Ku:
        switch (e = e.type, e) {
          case Qu:
          case Ol:
          case El:
          case Tl:
          case Pl:
          case Nl:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Ml:
              case zl:
              case bl:
              case jl:
              case Rl:
                return e;
              default:
                return t;
            }
        }
      case Gu:
        return t;
    }
  }
}
function uh(e) {
  return nt(e) === Ol;
}
G.AsyncMode = Qu;
G.ConcurrentMode = Ol;
G.ContextConsumer = Ml;
G.ContextProvider = Rl;
G.Element = Ku;
G.ForwardRef = zl;
G.Fragment = El;
G.Lazy = bl;
G.Memo = jl;
G.Portal = Gu;
G.Profiler = Tl;
G.StrictMode = Pl;
G.Suspense = Nl;
G.isAsyncMode = function(e) {
  return uh(e) || nt(e) === Qu;
};
G.isConcurrentMode = uh;
G.isContextConsumer = function(e) {
  return nt(e) === Ml;
};
G.isContextProvider = function(e) {
  return nt(e) === Rl;
};
G.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Ku;
};
G.isForwardRef = function(e) {
  return nt(e) === zl;
};
G.isFragment = function(e) {
  return nt(e) === El;
};
G.isLazy = function(e) {
  return nt(e) === bl;
};
G.isMemo = function(e) {
  return nt(e) === jl;
};
G.isPortal = function(e) {
  return nt(e) === Gu;
};
G.isProfiler = function(e) {
  return nt(e) === Tl;
};
G.isStrictMode = function(e) {
  return nt(e) === Pl;
};
G.isSuspense = function(e) {
  return nt(e) === Nl;
};
G.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === El || e === Ol || e === Tl || e === Pl || e === Nl || e === Ey || typeof e == "object" && e !== null && (e.$$typeof === bl || e.$$typeof === jl || e.$$typeof === Rl || e.$$typeof === Ml || e.$$typeof === zl || e.$$typeof === Ty || e.$$typeof === Ry || e.$$typeof === My || e.$$typeof === Py);
};
G.typeOf = nt;
ah.exports = G;
var Oy = ah.exports, ch = Oy, zy = {
  $$typeof: !0,
  render: !0,
  defaultProps: !0,
  displayName: !0,
  propTypes: !0
}, Ny = {
  $$typeof: !0,
  compare: !0,
  defaultProps: !0,
  displayName: !0,
  propTypes: !0,
  type: !0
}, dh = {};
dh[ch.ForwardRef] = zy;
dh[ch.Memo] = Ny;
var jy = !0;
function fh(e, t, n) {
  var r = "";
  return n.split(" ").forEach(function(o) {
    e[o] !== void 0 ? t.push(e[o] + ";") : o && (r += o + " ");
  }), r;
}
var Yu = function(t, n, r) {
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
  jy === !1) && t.registered[o] === void 0 && (t.registered[o] = n.styles);
}, Xu = function(t, n, r) {
  Yu(t, n, r);
  var o = t.key + "-" + n.name;
  if (t.inserted[n.name] === void 0) {
    var i = n;
    do
      t.insert(n === i ? "." + o : "", i, t.sheet, !0), i = i.next;
    while (i !== void 0);
  }
};
function by(e) {
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
var Ay = {
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
}, Iy = !1, Ly = /[A-Z]|^ms/g, Dy = /_EMO_([^_]+?)_([^]*?)_EMO_/g, ph = function(t) {
  return t.charCodeAt(1) === 45;
}, Fd = function(t) {
  return t != null && typeof t != "boolean";
}, Is = /* @__PURE__ */ ih(function(e) {
  return ph(e) ? e : e.replace(Ly, "-$&").toLowerCase();
}), Bd = function(t, n) {
  switch (t) {
    case "animation":
    case "animationName":
      if (typeof n == "string")
        return n.replace(Dy, function(r, o, i) {
          return Rt = {
            name: o,
            styles: i,
            next: Rt
          }, o;
        });
  }
  return Ay[t] !== 1 && !ph(t) && typeof n == "number" && n !== 0 ? n + "px" : n;
}, Fy = "Component selectors can only be used in conjunction with @emotion/babel-plugin, the swc Emotion plugin, or another Emotion-aware compiler transform.";
function _o(e, t, n) {
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
        return Rt = {
          name: o.name,
          styles: o.styles,
          next: Rt
        }, o.name;
      var i = n;
      if (i.styles !== void 0) {
        var l = i.next;
        if (l !== void 0)
          for (; l !== void 0; )
            Rt = {
              name: l.name,
              styles: l.styles,
              next: Rt
            }, l = l.next;
        var s = i.styles + ";";
        return s;
      }
      return By(e, t, n);
    }
    case "function": {
      if (e !== void 0) {
        var a = Rt, u = n(e);
        return Rt = a, _o(e, t, u);
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
function By(e, t, n) {
  var r = "";
  if (Array.isArray(n))
    for (var o = 0; o < n.length; o++)
      r += _o(e, t, n[o]) + ";";
  else
    for (var i in n) {
      var l = n[i];
      if (typeof l != "object") {
        var s = l;
        t != null && t[s] !== void 0 ? r += i + "{" + t[s] + "}" : Fd(s) && (r += Is(i) + ":" + Bd(i, s) + ";");
      } else {
        if (i === "NO_COMPONENT_SELECTOR" && Iy)
          throw new Error(Fy);
        if (Array.isArray(l) && typeof l[0] == "string" && (t == null || t[l[0]] === void 0))
          for (var a = 0; a < l.length; a++)
            Fd(l[a]) && (r += Is(i) + ":" + Bd(i, l[a]) + ";");
        else {
          var u = _o(e, t, l);
          switch (i) {
            case "animation":
            case "animationName": {
              r += Is(i) + ":" + u + ";";
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
var Wd = /label:\s*([^\s;{]+)\s*(;|$)/g, Rt;
function bo(e, t, n) {
  if (e.length === 1 && typeof e[0] == "object" && e[0] !== null && e[0].styles !== void 0)
    return e[0];
  var r = !0, o = "";
  Rt = void 0;
  var i = e[0];
  if (i == null || i.raw === void 0)
    r = !1, o += _o(n, t, i);
  else {
    var l = i;
    o += l[0];
  }
  for (var s = 1; s < e.length; s++)
    if (o += _o(n, t, e[s]), r) {
      var a = i;
      o += a[s];
    }
  Wd.lastIndex = 0;
  for (var u = "", c; (c = Wd.exec(o)) !== null; )
    u += "-" + c[1];
  var f = by(o) + u;
  return {
    name: f,
    styles: o,
    next: Rt
  };
}
var Wy = function(t) {
  return t();
}, mh = Gs["useInsertionEffect"] ? Gs["useInsertionEffect"] : !1, hh = mh || Wy, Ud = mh || _.useLayoutEffect, Uy = !1, gh = /* @__PURE__ */ _.createContext(
  // we're doing this to avoid preconstruct's dead code elimination in this one case
  // because this module is primarily intended for the browser and node
  // but it's also required in react native and similar environments sometimes
  // and we could have a special build just for that
  // but this is much easier and the native packages
  // might use a different theme context in the future anyway
  typeof HTMLElement < "u" ? /* @__PURE__ */ sh({
    key: "css"
  }) : null
), Vy = gh.Provider, qu = function(t) {
  return /* @__PURE__ */ _.forwardRef(function(n, r) {
    var o = _.useContext(gh);
    return t(n, o, r);
  });
}, kr = /* @__PURE__ */ _.createContext({}), Zu = {}.hasOwnProperty, Ua = "__EMOTION_TYPE_PLEASE_DO_NOT_USE__", Hy = function(t, n) {
  var r = {};
  for (var o in n)
    Zu.call(n, o) && (r[o] = n[o]);
  return r[Ua] = t, r;
}, Ky = function(t) {
  var n = t.cache, r = t.serialized, o = t.isStringTag;
  return Yu(n, r, o), hh(function() {
    return Xu(n, r, o);
  }), null;
}, Gy = /* @__PURE__ */ qu(function(e, t, n) {
  var r = e.css;
  typeof r == "string" && t.registered[r] !== void 0 && (r = t.registered[r]);
  var o = e[Ua], i = [r], l = "";
  typeof e.className == "string" ? l = fh(t.registered, i, e.className) : e.className != null && (l = e.className + " ");
  var s = bo(i, void 0, _.useContext(kr));
  l += t.key + "-" + s.name;
  var a = {};
  for (var u in e)
    Zu.call(e, u) && u !== "css" && u !== Ua && !Uy && (a[u] = e[u]);
  return a.className = l, n && (a.ref = n), /* @__PURE__ */ _.createElement(_.Fragment, null, /* @__PURE__ */ _.createElement(Ky, {
    cache: t,
    serialized: s,
    isStringTag: typeof o == "string"
  }), /* @__PURE__ */ _.createElement(o, a));
}), Qy = Gy, Ls = { exports: {} }, Vd;
function vh() {
  return Vd || (Vd = 1, function(e) {
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
  }(Ls)), Ls.exports;
}
vh();
var Hd = function(t, n) {
  var r = arguments;
  if (n == null || !Zu.call(n, "css"))
    return _.createElement.apply(void 0, r);
  var o = r.length, i = new Array(o);
  i[0] = Qy, i[1] = Hy(t, n);
  for (var l = 2; l < o; l++)
    i[l] = r[l];
  return _.createElement.apply(null, i);
};
(function(e) {
  var t;
  t || (t = e.JSX || (e.JSX = {}));
})(Hd || (Hd = {}));
var Yy = /* @__PURE__ */ qu(function(e, t) {
  var n = e.styles, r = bo([n], void 0, _.useContext(kr)), o = _.useRef();
  return Ud(function() {
    var i = t.key + "-global", l = new t.sheet.constructor({
      key: i,
      nonce: t.sheet.nonce,
      container: t.sheet.container,
      speedy: t.sheet.isSpeedy
    }), s = !1, a = document.querySelector('style[data-emotion="' + i + " " + r.name + '"]');
    return t.sheet.tags.length && (l.before = t.sheet.tags[0]), a !== null && (s = !0, a.setAttribute("data-emotion", i), l.hydrate([a])), o.current = [l, s], function() {
      l.flush();
    };
  }, [t]), Ud(function() {
    var i = o.current, l = i[0], s = i[1];
    if (s) {
      i[1] = !1;
      return;
    }
    if (r.next !== void 0 && Xu(t, r.next, !0), l.tags.length) {
      var a = l.tags[l.tags.length - 1].nextElementSibling;
      l.before = a, l.flush();
    }
    t.insert("", r, l, !1);
  }, [t, r.name]), null;
});
function Al() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  return bo(t);
}
function _r() {
  var e = Al.apply(void 0, arguments), t = "animation-" + e.name;
  return {
    name: t,
    styles: "@keyframes " + t + "{" + e.styles + "}",
    anim: 1,
    toString: function() {
      return "_EMO_" + this.name + "_" + this.styles + "_EMO_";
    }
  };
}
var Xy = /^((children|dangerouslySetInnerHTML|key|ref|autoFocus|defaultValue|defaultChecked|innerHTML|suppressContentEditableWarning|suppressHydrationWarning|valueLink|abbr|accept|acceptCharset|accessKey|action|allow|allowUserMedia|allowPaymentRequest|allowFullScreen|allowTransparency|alt|async|autoComplete|autoPlay|capture|cellPadding|cellSpacing|challenge|charSet|checked|cite|classID|className|cols|colSpan|content|contentEditable|contextMenu|controls|controlsList|coords|crossOrigin|data|dateTime|decoding|default|defer|dir|disabled|disablePictureInPicture|disableRemotePlayback|download|draggable|encType|enterKeyHint|fetchpriority|fetchPriority|form|formAction|formEncType|formMethod|formNoValidate|formTarget|frameBorder|headers|height|hidden|high|href|hrefLang|htmlFor|httpEquiv|id|inputMode|integrity|is|keyParams|keyType|kind|label|lang|list|loading|loop|low|marginHeight|marginWidth|max|maxLength|media|mediaGroup|method|min|minLength|multiple|muted|name|nonce|noValidate|open|optimum|pattern|placeholder|playsInline|popover|popoverTarget|popoverTargetAction|poster|preload|profile|radioGroup|readOnly|referrerPolicy|rel|required|reversed|role|rows|rowSpan|sandbox|scope|scoped|scrolling|seamless|selected|shape|size|sizes|slot|span|spellCheck|src|srcDoc|srcLang|srcSet|start|step|style|summary|tabIndex|target|title|translate|type|useMap|value|width|wmode|wrap|about|datatype|inlist|prefix|property|resource|typeof|vocab|autoCapitalize|autoCorrect|autoSave|color|incremental|fallback|inert|itemProp|itemScope|itemType|itemID|itemRef|on|option|results|security|unselectable|accentHeight|accumulate|additive|alignmentBaseline|allowReorder|alphabetic|amplitude|arabicForm|ascent|attributeName|attributeType|autoReverse|azimuth|baseFrequency|baselineShift|baseProfile|bbox|begin|bias|by|calcMode|capHeight|clip|clipPathUnits|clipPath|clipRule|colorInterpolation|colorInterpolationFilters|colorProfile|colorRendering|contentScriptType|contentStyleType|cursor|cx|cy|d|decelerate|descent|diffuseConstant|direction|display|divisor|dominantBaseline|dur|dx|dy|edgeMode|elevation|enableBackground|end|exponent|externalResourcesRequired|fill|fillOpacity|fillRule|filter|filterRes|filterUnits|floodColor|floodOpacity|focusable|fontFamily|fontSize|fontSizeAdjust|fontStretch|fontStyle|fontVariant|fontWeight|format|from|fr|fx|fy|g1|g2|glyphName|glyphOrientationHorizontal|glyphOrientationVertical|glyphRef|gradientTransform|gradientUnits|hanging|horizAdvX|horizOriginX|ideographic|imageRendering|in|in2|intercept|k|k1|k2|k3|k4|kernelMatrix|kernelUnitLength|kerning|keyPoints|keySplines|keyTimes|lengthAdjust|letterSpacing|lightingColor|limitingConeAngle|local|markerEnd|markerMid|markerStart|markerHeight|markerUnits|markerWidth|mask|maskContentUnits|maskUnits|mathematical|mode|numOctaves|offset|opacity|operator|order|orient|orientation|origin|overflow|overlinePosition|overlineThickness|panose1|paintOrder|pathLength|patternContentUnits|patternTransform|patternUnits|pointerEvents|points|pointsAtX|pointsAtY|pointsAtZ|preserveAlpha|preserveAspectRatio|primitiveUnits|r|radius|refX|refY|renderingIntent|repeatCount|repeatDur|requiredExtensions|requiredFeatures|restart|result|rotate|rx|ry|scale|seed|shapeRendering|slope|spacing|specularConstant|specularExponent|speed|spreadMethod|startOffset|stdDeviation|stemh|stemv|stitchTiles|stopColor|stopOpacity|strikethroughPosition|strikethroughThickness|string|stroke|strokeDasharray|strokeDashoffset|strokeLinecap|strokeLinejoin|strokeMiterlimit|strokeOpacity|strokeWidth|surfaceScale|systemLanguage|tableValues|targetX|targetY|textAnchor|textDecoration|textRendering|textLength|to|transform|u1|u2|underlinePosition|underlineThickness|unicode|unicodeBidi|unicodeRange|unitsPerEm|vAlphabetic|vHanging|vIdeographic|vMathematical|values|vectorEffect|version|vertAdvY|vertOriginX|vertOriginY|viewBox|viewTarget|visibility|widths|wordSpacing|writingMode|x|xHeight|x1|x2|xChannelSelector|xlinkActuate|xlinkArcrole|xlinkHref|xlinkRole|xlinkShow|xlinkTitle|xlinkType|xmlBase|xmlns|xmlnsXlink|xmlLang|xmlSpace|y|y1|y2|yChannelSelector|z|zoomAndPan|for|class|autofocus)|(([Dd][Aa][Tt][Aa]|[Aa][Rr][Ii][Aa]|x)-.*))$/, qy = /* @__PURE__ */ ih(
  function(e) {
    return Xy.test(e) || e.charCodeAt(0) === 111 && e.charCodeAt(1) === 110 && e.charCodeAt(2) < 91;
  }
  /* Z+1 */
), Zy = !1, Jy = qy, e1 = function(t) {
  return t !== "theme";
}, Kd = function(t) {
  return typeof t == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  t.charCodeAt(0) > 96 ? Jy : e1;
}, Gd = function(t, n, r) {
  var o;
  if (n) {
    var i = n.shouldForwardProp;
    o = t.__emotion_forwardProp && i ? function(l) {
      return t.__emotion_forwardProp(l) && i(l);
    } : i;
  }
  return typeof o != "function" && r && (o = t.__emotion_forwardProp), o;
}, t1 = function(t) {
  var n = t.cache, r = t.serialized, o = t.isStringTag;
  return Yu(n, r, o), hh(function() {
    return Xu(n, r, o);
  }), null;
}, n1 = function e(t, n) {
  var r = t.__emotion_real === t, o = r && t.__emotion_base || t, i, l;
  n !== void 0 && (i = n.label, l = n.target);
  var s = Gd(t, n, r), a = s || Kd(o), u = !a("as");
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
    var g = qu(function(E, m, d) {
      var h = u && E.as || o, S = "", $ = [], k = E;
      if (E.theme == null) {
        k = {};
        for (var C in E)
          k[C] = E[C];
        k.theme = _.useContext(kr);
      }
      typeof E.className == "string" ? S = fh(m.registered, $, E.className) : E.className != null && (S = E.className + " ");
      var T = bo(f.concat($), m.registered, k);
      S += m.key + "-" + T.name, l !== void 0 && (S += " " + l);
      var z = u && s === void 0 ? Kd(h) : a, M = {};
      for (var U in E)
        u && U === "as" || z(U) && (M[U] = E[U]);
      return M.className = S, d && (M.ref = d), /* @__PURE__ */ _.createElement(_.Fragment, null, /* @__PURE__ */ _.createElement(t1, {
        cache: m,
        serialized: T,
        isStringTag: typeof h == "string"
      }), /* @__PURE__ */ _.createElement(h, M));
    });
    return g.displayName = i !== void 0 ? i : "Styled(" + (typeof o == "string" ? o : o.displayName || o.name || "Component") + ")", g.defaultProps = t.defaultProps, g.__emotion_real = g, g.__emotion_base = o, g.__emotion_styles = f, g.__emotion_forwardProp = s, Object.defineProperty(g, "toString", {
      value: function() {
        return l === void 0 && Zy ? "NO_COMPONENT_SELECTOR" : "." + l;
      }
    }), g.withComponent = function(E, m) {
      var d = e(E, w({}, n, m, {
        shouldForwardProp: Gd(g, m, !0)
      }));
      return d.apply(void 0, f);
    }, g;
  };
}, r1 = [
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
], Va = n1.bind(null);
r1.forEach(function(e) {
  Va[e] = Va(e);
});
function o1(e, t) {
  const n = sh({
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
function i1(e) {
  const {
    injectFirst: t,
    enableCssLayer: n,
    children: r
  } = e, o = _.useMemo(() => {
    const i = `${t}-${n}`;
    if (typeof document == "object" && Ds.has(i))
      return Ds.get(i);
    const l = o1(t, n);
    return Ds.set(i, l), l;
  }, [t, n]);
  return t || n ? /* @__PURE__ */ x.jsx(Vy, {
    value: o,
    children: r
  }) : r;
}
function l1(e) {
  return e == null || Object.keys(e).length === 0;
}
function yh(e) {
  const {
    styles: t,
    defaultTheme: n = {}
  } = e, r = typeof t == "function" ? (o) => t(l1(o) ? n : o) : t;
  return /* @__PURE__ */ x.jsx(Yy, {
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
function Ju(e, t) {
  return Va(e, t);
}
const xh = (e, t) => {
  Array.isArray(e.__emotion_styles) && (e.__emotion_styles = t(e.__emotion_styles));
}, Qd = [];
function el(e) {
  return Qd[0] = e, bo(Qd);
}
const s1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  GlobalStyles: yh,
  StyledEngineProvider: i1,
  ThemeContext: kr,
  css: Al,
  default: Ju,
  internal_processStyles: xh,
  internal_serializeStyles: el,
  keyframes: _r
}, Symbol.toStringTag, { value: "Module" }));
function Lt(e) {
  if (typeof e != "object" || e === null)
    return !1;
  const t = Object.getPrototypeOf(e);
  return (t === null || t === Object.prototype || Object.getPrototypeOf(t) === null) && !(Symbol.toStringTag in e) && !(Symbol.iterator in e);
}
function Sh(e) {
  if (/* @__PURE__ */ _.isValidElement(e) || !Lt(e))
    return e;
  const t = {};
  return Object.keys(e).forEach((n) => {
    t[n] = Sh(e[n]);
  }), t;
}
function jt(e, t, n = {
  clone: !0
}) {
  const r = n.clone ? w({}, e) : e;
  return Lt(e) && Lt(t) && Object.keys(t).forEach((o) => {
    /* @__PURE__ */ _.isValidElement(t[o]) ? r[o] = t[o] : Lt(t[o]) && // Avoid prototype pollution
    Object.prototype.hasOwnProperty.call(e, o) && Lt(e[o]) ? r[o] = jt(e[o], t[o], n) : n.clone ? r[o] = Lt(t[o]) ? Sh(t[o]) : t[o] : r[o] = t[o];
  }), r;
}
const a1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: jt,
  isPlainObject: Lt
}, Symbol.toStringTag, { value: "Module" })), u1 = ["values", "unit", "step"], c1 = (e) => {
  const t = Object.keys(e).map((n) => ({
    key: n,
    val: e[n]
  })) || [];
  return t.sort((n, r) => n.val - r.val), t.reduce((n, r) => w({}, n, {
    [r.key]: r.val
  }), {});
};
function wh(e) {
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
  } = e, o = L(e, u1), i = c1(t), l = Object.keys(i);
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
  return w({
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
const d1 = {
  borderRadius: 4
}, f1 = d1;
function no(e, t) {
  return t ? jt(e, t, {
    clone: !1
    // No need to clone deep, it's way faster.
  }) : e;
}
const ec = {
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
}, Yd = {
  // Sorted ASC by size. That's important.
  // It can't be configured as it's used statically for propTypes.
  keys: ["xs", "sm", "md", "lg", "xl"],
  up: (e) => `@media (min-width:${ec[e]}px)`
};
function pt(e, t, n) {
  const r = e.theme || {};
  if (Array.isArray(t)) {
    const i = r.breakpoints || Yd;
    return t.reduce((l, s, a) => (l[i.up(i.keys[a])] = n(t[a]), l), {});
  }
  if (typeof t == "object") {
    const i = r.breakpoints || Yd;
    return Object.keys(t).reduce((l, s) => {
      if (Object.keys(i.values || ec).indexOf(s) !== -1) {
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
function p1(e = {}) {
  var t;
  return ((t = e.keys) == null ? void 0 : t.reduce((r, o) => {
    const i = e.up(o);
    return r[i] = {}, r;
  }, {})) || {};
}
function Xd(e, t) {
  return e.reduce((n, r) => {
    const o = n[r];
    return (!o || Object.keys(o).length === 0) && delete n[r], n;
  }, t);
}
function m1(e, t) {
  if (typeof e != "object")
    return {};
  const n = {}, r = Object.keys(t);
  return Array.isArray(e) ? r.forEach((o, i) => {
    i < e.length && (n[o] = !0);
  }) : r.forEach((o) => {
    e[o] != null && (n[o] = !0);
  }), n;
}
function Il({
  values: e,
  breakpoints: t,
  base: n
}) {
  const r = n || m1(e, t), o = Object.keys(r);
  if (o.length === 0)
    return e;
  let i;
  return o.reduce((l, s, a) => (Array.isArray(e) ? (l[s] = e[a] != null ? e[a] : e[i], i = a) : typeof e == "object" ? (l[s] = e[s] != null ? e[s] : e[i], i = s) : l[s] = e, l), {});
}
function j(e) {
  if (typeof e != "string")
    throw new Error(wo(7));
  return e.charAt(0).toUpperCase() + e.slice(1);
}
const h1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: j
}, Symbol.toStringTag, { value: "Module" }));
function Ll(e, t, n = !0) {
  if (!t || typeof t != "string")
    return null;
  if (e && e.vars && n) {
    const r = `vars.${t}`.split(".").reduce((o, i) => o && o[i] ? o[i] : null, e);
    if (r != null)
      return r;
  }
  return t.split(".").reduce((r, o) => r && r[o] != null ? r[o] : null, e);
}
function tl(e, t, n, r = n) {
  let o;
  return typeof e == "function" ? o = e(n) : Array.isArray(e) ? o = e[n] || r : o = Ll(e, n) || r, t && (o = t(o, r, e)), o;
}
function ce(e) {
  const {
    prop: t,
    cssProperty: n = e.prop,
    themeKey: r,
    transform: o
  } = e, i = (l) => {
    if (l[t] == null)
      return null;
    const s = l[t], a = l.theme, u = Ll(a, r) || {};
    return pt(l, s, (f) => {
      let p = tl(u, o, f);
      return f === p && typeof f == "string" && (p = tl(u, o, `${t}${f === "default" ? "" : j(f)}`, f)), n === !1 ? p : {
        [n]: p
      };
    });
  };
  return i.propTypes = {}, i.filterProps = [t], i;
}
function g1(e) {
  const t = {};
  return (n) => (t[n] === void 0 && (t[n] = e(n)), t[n]);
}
const v1 = {
  m: "margin",
  p: "padding"
}, y1 = {
  t: "Top",
  r: "Right",
  b: "Bottom",
  l: "Left",
  x: ["Left", "Right"],
  y: ["Top", "Bottom"]
}, qd = {
  marginX: "mx",
  marginY: "my",
  paddingX: "px",
  paddingY: "py"
}, x1 = g1((e) => {
  if (e.length > 2)
    if (qd[e])
      e = qd[e];
    else
      return [e];
  const [t, n] = e.split(""), r = v1[t], o = y1[n] || "";
  return Array.isArray(o) ? o.map((i) => r + i) : [r + o];
}), tc = ["m", "mt", "mr", "mb", "ml", "mx", "my", "margin", "marginTop", "marginRight", "marginBottom", "marginLeft", "marginX", "marginY", "marginInline", "marginInlineStart", "marginInlineEnd", "marginBlock", "marginBlockStart", "marginBlockEnd"], nc = ["p", "pt", "pr", "pb", "pl", "px", "py", "padding", "paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "paddingX", "paddingY", "paddingInline", "paddingInlineStart", "paddingInlineEnd", "paddingBlock", "paddingBlockStart", "paddingBlockEnd"];
[...tc, ...nc];
function Ao(e, t, n, r) {
  var o;
  const i = (o = Ll(e, t, !1)) != null ? o : n;
  return typeof i == "number" ? (l) => typeof l == "string" ? l : i * l : Array.isArray(i) ? (l) => typeof l == "string" ? l : i[l] : typeof i == "function" ? i : () => {
  };
}
function Ch(e) {
  return Ao(e, "spacing", 8);
}
function Io(e, t) {
  if (typeof t == "string" || t == null)
    return t;
  const n = Math.abs(t), r = e(n);
  return t >= 0 ? r : typeof r == "number" ? -r : `-${r}`;
}
function S1(e, t) {
  return (n) => e.reduce((r, o) => (r[o] = Io(t, n), r), {});
}
function w1(e, t, n, r) {
  if (t.indexOf(n) === -1)
    return null;
  const o = x1(n), i = S1(o, r), l = e[n];
  return pt(e, l, i);
}
function kh(e, t) {
  const n = Ch(e.theme);
  return Object.keys(e).map((r) => w1(e, t, r, n)).reduce(no, {});
}
function le(e) {
  return kh(e, tc);
}
le.propTypes = {};
le.filterProps = tc;
function se(e) {
  return kh(e, nc);
}
se.propTypes = {};
se.filterProps = nc;
function C1(e = 8) {
  if (e.mui)
    return e;
  const t = Ch({
    spacing: e
  }), n = (...r) => (r.length === 0 ? [1] : r).map((i) => {
    const l = t(i);
    return typeof l == "number" ? `${l}px` : l;
  }).join(" ");
  return n.mui = !0, n;
}
function Dl(...e) {
  const t = e.reduce((r, o) => (o.filterProps.forEach((i) => {
    r[i] = o;
  }), r), {}), n = (r) => Object.keys(r).reduce((o, i) => t[i] ? no(o, t[i](r)) : o, {});
  return n.propTypes = {}, n.filterProps = e.reduce((r, o) => r.concat(o.filterProps), []), n;
}
function st(e) {
  return typeof e != "number" ? e : `${e}px solid`;
}
function ht(e, t) {
  return ce({
    prop: e,
    themeKey: "borders",
    transform: t
  });
}
const k1 = ht("border", st), _1 = ht("borderTop", st), $1 = ht("borderRight", st), E1 = ht("borderBottom", st), P1 = ht("borderLeft", st), T1 = ht("borderColor"), R1 = ht("borderTopColor"), M1 = ht("borderRightColor"), O1 = ht("borderBottomColor"), z1 = ht("borderLeftColor"), N1 = ht("outline", st), j1 = ht("outlineColor"), Fl = (e) => {
  if (e.borderRadius !== void 0 && e.borderRadius !== null) {
    const t = Ao(e.theme, "shape.borderRadius", 4), n = (r) => ({
      borderRadius: Io(t, r)
    });
    return pt(e, e.borderRadius, n);
  }
  return null;
};
Fl.propTypes = {};
Fl.filterProps = ["borderRadius"];
Dl(k1, _1, $1, E1, P1, T1, R1, M1, O1, z1, Fl, N1, j1);
const Bl = (e) => {
  if (e.gap !== void 0 && e.gap !== null) {
    const t = Ao(e.theme, "spacing", 8), n = (r) => ({
      gap: Io(t, r)
    });
    return pt(e, e.gap, n);
  }
  return null;
};
Bl.propTypes = {};
Bl.filterProps = ["gap"];
const Wl = (e) => {
  if (e.columnGap !== void 0 && e.columnGap !== null) {
    const t = Ao(e.theme, "spacing", 8), n = (r) => ({
      columnGap: Io(t, r)
    });
    return pt(e, e.columnGap, n);
  }
  return null;
};
Wl.propTypes = {};
Wl.filterProps = ["columnGap"];
const Ul = (e) => {
  if (e.rowGap !== void 0 && e.rowGap !== null) {
    const t = Ao(e.theme, "spacing", 8), n = (r) => ({
      rowGap: Io(t, r)
    });
    return pt(e, e.rowGap, n);
  }
  return null;
};
Ul.propTypes = {};
Ul.filterProps = ["rowGap"];
const b1 = ce({
  prop: "gridColumn"
}), A1 = ce({
  prop: "gridRow"
}), I1 = ce({
  prop: "gridAutoFlow"
}), L1 = ce({
  prop: "gridAutoColumns"
}), D1 = ce({
  prop: "gridAutoRows"
}), F1 = ce({
  prop: "gridTemplateColumns"
}), B1 = ce({
  prop: "gridTemplateRows"
}), W1 = ce({
  prop: "gridTemplateAreas"
}), U1 = ce({
  prop: "gridArea"
});
Dl(Bl, Wl, Ul, b1, A1, I1, L1, D1, F1, B1, W1, U1);
function ar(e, t) {
  return t === "grey" ? t : e;
}
const V1 = ce({
  prop: "color",
  themeKey: "palette",
  transform: ar
}), H1 = ce({
  prop: "bgcolor",
  cssProperty: "backgroundColor",
  themeKey: "palette",
  transform: ar
}), K1 = ce({
  prop: "backgroundColor",
  themeKey: "palette",
  transform: ar
});
Dl(V1, H1, K1);
function Ye(e) {
  return e <= 1 && e !== 0 ? `${e * 100}%` : e;
}
const G1 = ce({
  prop: "width",
  transform: Ye
}), rc = (e) => {
  if (e.maxWidth !== void 0 && e.maxWidth !== null) {
    const t = (n) => {
      var r, o;
      const i = ((r = e.theme) == null || (r = r.breakpoints) == null || (r = r.values) == null ? void 0 : r[n]) || ec[n];
      return i ? ((o = e.theme) == null || (o = o.breakpoints) == null ? void 0 : o.unit) !== "px" ? {
        maxWidth: `${i}${e.theme.breakpoints.unit}`
      } : {
        maxWidth: i
      } : {
        maxWidth: Ye(n)
      };
    };
    return pt(e, e.maxWidth, t);
  }
  return null;
};
rc.filterProps = ["maxWidth"];
const Q1 = ce({
  prop: "minWidth",
  transform: Ye
}), Y1 = ce({
  prop: "height",
  transform: Ye
}), X1 = ce({
  prop: "maxHeight",
  transform: Ye
}), q1 = ce({
  prop: "minHeight",
  transform: Ye
});
ce({
  prop: "size",
  cssProperty: "width",
  transform: Ye
});
ce({
  prop: "size",
  cssProperty: "height",
  transform: Ye
});
const Z1 = ce({
  prop: "boxSizing"
});
Dl(G1, rc, Q1, Y1, X1, q1, Z1);
const J1 = {
  // borders
  border: {
    themeKey: "borders",
    transform: st
  },
  borderTop: {
    themeKey: "borders",
    transform: st
  },
  borderRight: {
    themeKey: "borders",
    transform: st
  },
  borderBottom: {
    themeKey: "borders",
    transform: st
  },
  borderLeft: {
    themeKey: "borders",
    transform: st
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
    transform: st
  },
  outlineColor: {
    themeKey: "palette"
  },
  borderRadius: {
    themeKey: "shape.borderRadius",
    style: Fl
  },
  // palette
  color: {
    themeKey: "palette",
    transform: ar
  },
  bgcolor: {
    themeKey: "palette",
    cssProperty: "backgroundColor",
    transform: ar
  },
  backgroundColor: {
    themeKey: "palette",
    transform: ar
  },
  // spacing
  p: {
    style: se
  },
  pt: {
    style: se
  },
  pr: {
    style: se
  },
  pb: {
    style: se
  },
  pl: {
    style: se
  },
  px: {
    style: se
  },
  py: {
    style: se
  },
  padding: {
    style: se
  },
  paddingTop: {
    style: se
  },
  paddingRight: {
    style: se
  },
  paddingBottom: {
    style: se
  },
  paddingLeft: {
    style: se
  },
  paddingX: {
    style: se
  },
  paddingY: {
    style: se
  },
  paddingInline: {
    style: se
  },
  paddingInlineStart: {
    style: se
  },
  paddingInlineEnd: {
    style: se
  },
  paddingBlock: {
    style: se
  },
  paddingBlockStart: {
    style: se
  },
  paddingBlockEnd: {
    style: se
  },
  m: {
    style: le
  },
  mt: {
    style: le
  },
  mr: {
    style: le
  },
  mb: {
    style: le
  },
  ml: {
    style: le
  },
  mx: {
    style: le
  },
  my: {
    style: le
  },
  margin: {
    style: le
  },
  marginTop: {
    style: le
  },
  marginRight: {
    style: le
  },
  marginBottom: {
    style: le
  },
  marginLeft: {
    style: le
  },
  marginX: {
    style: le
  },
  marginY: {
    style: le
  },
  marginInline: {
    style: le
  },
  marginInlineStart: {
    style: le
  },
  marginInlineEnd: {
    style: le
  },
  marginBlock: {
    style: le
  },
  marginBlockStart: {
    style: le
  },
  marginBlockEnd: {
    style: le
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
    style: Bl
  },
  rowGap: {
    style: Ul
  },
  columnGap: {
    style: Wl
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
    transform: Ye
  },
  maxWidth: {
    style: rc
  },
  minWidth: {
    transform: Ye
  },
  height: {
    transform: Ye
  },
  maxHeight: {
    transform: Ye
  },
  minHeight: {
    transform: Ye
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
}, Lo = J1;
function ex(...e) {
  const t = e.reduce((r, o) => r.concat(Object.keys(o)), []), n = new Set(t);
  return e.every((r) => n.size === Object.keys(r).length);
}
function tx(e, t) {
  return typeof e == "function" ? e(t) : e;
}
function _h() {
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
    const p = Ll(o, u) || {};
    return f ? f(l) : pt(l, r, (y) => {
      let g = tl(p, c, y);
      return y === g && typeof y == "string" && (g = tl(p, c, `${n}${y === "default" ? "" : j(y)}`, y)), a === !1 ? g : {
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
    const s = (r = i.unstable_sxConfig) != null ? r : Lo;
    function a(u) {
      let c = u;
      if (typeof u == "function")
        c = u(i);
      else if (typeof u != "object")
        return u;
      if (!c)
        return null;
      const f = p1(i.breakpoints), p = Object.keys(f);
      let v = f;
      return Object.keys(c).forEach((y) => {
        const g = tx(c[y], i);
        if (g != null)
          if (typeof g == "object")
            if (s[y])
              v = no(v, e(y, g, i, s));
            else {
              const E = pt({
                theme: i
              }, g, (m) => ({
                [y]: m
              }));
              ex(E, g) ? v[y] = t({
                sx: g,
                theme: i,
                nested: !0
              }) : v = no(v, E);
            }
          else
            v = no(v, e(y, g, i, s));
      }), !l && i.modularCssLayers ? {
        "@layer sx": Xd(p, v)
      } : Xd(p, v);
    }
    return Array.isArray(o) ? o.map(a) : a(o);
  }
  return t;
}
const $h = _h();
$h.filterProps = ["sx"];
const Do = $h;
function Eh(e, t) {
  const n = this;
  return n.vars && typeof n.getColorSchemeSelector == "function" ? {
    [n.getColorSchemeSelector(e).replace(/(\[[^\]]+\])/, "*:where($1)")]: t
  } : n.palette.mode === e ? t : {};
}
const nx = ["breakpoints", "palette", "spacing", "shape"];
function Fo(e = {}, ...t) {
  const {
    breakpoints: n = {},
    palette: r = {},
    spacing: o,
    shape: i = {}
  } = e, l = L(e, nx), s = wh(n), a = C1(o);
  let u = jt({
    breakpoints: s,
    direction: "ltr",
    components: {},
    // Inject component definitions.
    palette: w({
      mode: "light"
    }, r),
    spacing: a,
    shape: w({}, f1, i)
  }, l);
  return u.applyStyles = Eh, u = t.reduce((c, f) => jt(c, f), u), u.unstable_sxConfig = w({}, Lo, l == null ? void 0 : l.unstable_sxConfig), u.unstable_sx = function(f) {
    return Do({
      sx: f,
      theme: this
    });
  }, u;
}
const rx = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Fo,
  private_createBreakpoints: wh,
  unstable_applyStyles: Eh
}, Symbol.toStringTag, { value: "Module" }));
function ox(e) {
  return Object.keys(e).length === 0;
}
function oc(e = null) {
  const t = _.useContext(kr);
  return !t || ox(t) ? e : t;
}
const ix = Fo();
function Vl(e = ix) {
  return oc(e);
}
function Fs(e) {
  const t = el(e);
  return e !== t && t.styles ? (t.styles.match(/^@layer\s+[^{]*$/) || (t.styles = `@layer global{${t.styles}}`), t) : e;
}
function Ph({
  styles: e,
  themeId: t,
  defaultTheme: n = {}
}) {
  const r = Vl(n), o = t && r[t] || r;
  let i = typeof e == "function" ? e(o) : e;
  return o.modularCssLayers && (Array.isArray(i) ? i = i.map((l) => Fs(typeof l == "function" ? l(o) : l)) : i = Fs(i)), /* @__PURE__ */ x.jsx(yh, {
    styles: i
  });
}
const lx = ["sx"], sx = (e) => {
  var t, n;
  const r = {
    systemProps: {},
    otherProps: {}
  }, o = (t = e == null || (n = e.theme) == null ? void 0 : n.unstable_sxConfig) != null ? t : Lo;
  return Object.keys(e).forEach((i) => {
    o[i] ? r.systemProps[i] = e[i] : r.otherProps[i] = e[i];
  }), r;
};
function Hl(e) {
  const {
    sx: t
  } = e, n = L(e, lx), {
    systemProps: r,
    otherProps: o
  } = sx(n);
  let i;
  return Array.isArray(t) ? i = [r, ...t] : typeof t == "function" ? i = (...l) => {
    const s = t(...l);
    return Lt(s) ? w({}, r, s) : r;
  } : i = w({}, r, t), w({}, o, {
    sx: i
  });
}
const ax = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Do,
  extendSxProp: Hl,
  unstable_createStyleFunctionSx: _h,
  unstable_defaultSxConfig: Lo
}, Symbol.toStringTag, { value: "Module" })), Zd = (e) => e, ux = () => {
  let e = Zd;
  return {
    configure(t) {
      e = t;
    },
    generate(t) {
      return e(t);
    },
    reset() {
      e = Zd;
    }
  };
}, cx = ux(), ic = cx;
function Th(e) {
  var t, n, r = "";
  if (typeof e == "string" || typeof e == "number")
    r += e;
  else if (typeof e == "object")
    if (Array.isArray(e)) {
      var o = e.length;
      for (t = 0; t < o; t++)
        e[t] && (n = Th(e[t])) && (r && (r += " "), r += n);
    } else
      for (n in e)
        e[n] && (r && (r += " "), r += n);
  return r;
}
function B() {
  for (var e, t, n = 0, r = "", o = arguments.length; n < o; n++)
    (e = arguments[n]) && (t = Th(e)) && (r && (r += " "), r += t);
  return r;
}
const dx = ["className", "component"];
function fx(e = {}) {
  const {
    themeId: t,
    defaultTheme: n,
    defaultClassName: r = "MuiBox-root",
    generateClassName: o
  } = e, i = Ju("div", {
    shouldForwardProp: (s) => s !== "theme" && s !== "sx" && s !== "as"
  })(Do);
  return /* @__PURE__ */ _.forwardRef(function(a, u) {
    const c = Vl(n), f = Hl(a), {
      className: p,
      component: v = "div"
    } = f, y = L(f, dx);
    return /* @__PURE__ */ x.jsx(i, w({
      as: v,
      ref: u,
      className: B(p, o ? o(r) : r),
      theme: t && c[t] || c
    }, y));
  });
}
const px = {
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
function ve(e, t, n = "Mui") {
  const r = px[t];
  return r ? `${n}-${r}` : `${ic.generate(e)}-${t}`;
}
function ye(e, t, n = "Mui") {
  const r = {};
  return t.forEach((o) => {
    r[o] = ve(e, o, n);
  }), r;
}
var Rh = { exports: {} }, Y = {};
/**
 * @license React
 * react-is.production.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var lc = Symbol.for("react.transitional.element"), sc = Symbol.for("react.portal"), Kl = Symbol.for("react.fragment"), Gl = Symbol.for("react.strict_mode"), Ql = Symbol.for("react.profiler"), Yl = Symbol.for("react.consumer"), Xl = Symbol.for("react.context"), ql = Symbol.for("react.forward_ref"), Zl = Symbol.for("react.suspense"), Jl = Symbol.for("react.suspense_list"), es = Symbol.for("react.memo"), ts = Symbol.for("react.lazy"), mx = Symbol.for("react.view_transition"), hx = Symbol.for("react.client.reference");
function gt(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case lc:
        switch (e = e.type, e) {
          case Kl:
          case Ql:
          case Gl:
          case Zl:
          case Jl:
          case mx:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Xl:
              case ql:
              case ts:
              case es:
                return e;
              case Yl:
                return e;
              default:
                return t;
            }
        }
      case sc:
        return t;
    }
  }
}
Y.ContextConsumer = Yl;
Y.ContextProvider = Xl;
Y.Element = lc;
Y.ForwardRef = ql;
Y.Fragment = Kl;
Y.Lazy = ts;
Y.Memo = es;
Y.Portal = sc;
Y.Profiler = Ql;
Y.StrictMode = Gl;
Y.Suspense = Zl;
Y.SuspenseList = Jl;
Y.isContextConsumer = function(e) {
  return gt(e) === Yl;
};
Y.isContextProvider = function(e) {
  return gt(e) === Xl;
};
Y.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === lc;
};
Y.isForwardRef = function(e) {
  return gt(e) === ql;
};
Y.isFragment = function(e) {
  return gt(e) === Kl;
};
Y.isLazy = function(e) {
  return gt(e) === ts;
};
Y.isMemo = function(e) {
  return gt(e) === es;
};
Y.isPortal = function(e) {
  return gt(e) === sc;
};
Y.isProfiler = function(e) {
  return gt(e) === Ql;
};
Y.isStrictMode = function(e) {
  return gt(e) === Gl;
};
Y.isSuspense = function(e) {
  return gt(e) === Zl;
};
Y.isSuspenseList = function(e) {
  return gt(e) === Jl;
};
Y.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === Kl || e === Ql || e === Gl || e === Zl || e === Jl || typeof e == "object" && e !== null && (e.$$typeof === ts || e.$$typeof === es || e.$$typeof === Xl || e.$$typeof === Yl || e.$$typeof === ql || e.$$typeof === hx || e.getModuleId !== void 0);
};
Y.typeOf = gt;
Rh.exports = Y;
var Jd = Rh.exports;
const gx = /^\s*function(?:\s|\s*\/\*.*\*\/\s*)+([^(\s/]*)\s*/;
function Mh(e) {
  const t = `${e}`.match(gx);
  return t && t[1] || "";
}
function Oh(e, t = "") {
  return e.displayName || e.name || Mh(e) || t;
}
function ef(e, t, n) {
  const r = Oh(t);
  return e.displayName || (r !== "" ? `${n}(${r})` : n);
}
function vx(e) {
  if (e != null) {
    if (typeof e == "string")
      return e;
    if (typeof e == "function")
      return Oh(e, "Component");
    if (typeof e == "object")
      switch (e.$$typeof) {
        case Jd.ForwardRef:
          return ef(e, e.render, "ForwardRef");
        case Jd.Memo:
          return ef(e, e.type, "memo");
        default:
          return;
      }
  }
}
const yx = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: vx,
  getFunctionName: Mh
}, Symbol.toStringTag, { value: "Module" })), xx = ["ownerState"], Sx = ["variants"], wx = ["name", "slot", "skipVariantsResolver", "skipSx", "overridesResolver"];
function Cx(e) {
  return Object.keys(e).length === 0;
}
function kx(e) {
  return typeof e == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  e.charCodeAt(0) > 96;
}
function Bs(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
function tf(e, t) {
  return t && e && typeof e == "object" && e.styles && !e.styles.startsWith("@layer") && (e.styles = `@layer ${t}{${String(e.styles)}}`), e;
}
const _x = Fo(), $x = (e) => e && e.charAt(0).toLowerCase() + e.slice(1);
function ai({
  defaultTheme: e,
  theme: t,
  themeId: n
}) {
  return Cx(t) ? e : t[n] || t;
}
function Ex(e) {
  return e ? (t, n) => n[e] : null;
}
function Ei(e, t, n) {
  let {
    ownerState: r
  } = t, o = L(t, xx);
  const i = typeof e == "function" ? e(w({
    ownerState: r
  }, o)) : e;
  if (Array.isArray(i))
    return i.flatMap((l) => Ei(l, w({
      ownerState: r
    }, o), n));
  if (i && typeof i == "object" && Array.isArray(i.variants)) {
    const {
      variants: l = []
    } = i;
    let a = L(i, Sx);
    return l.forEach((u) => {
      let c = !0;
      if (typeof u.props == "function" ? c = u.props(w({
        ownerState: r
      }, o, r)) : Object.keys(u.props).forEach((f) => {
        (r == null ? void 0 : r[f]) !== u.props[f] && o[f] !== u.props[f] && (c = !1);
      }), c) {
        Array.isArray(a) || (a = [a]);
        const f = typeof u.style == "function" ? u.style(w({
          ownerState: r
        }, o, r)) : u.style;
        a.push(n ? tf(el(f), n) : f);
      }
    }), a;
  }
  return n ? tf(el(i), n) : i;
}
function Px(e = {}) {
  const {
    themeId: t,
    defaultTheme: n = _x,
    rootShouldForwardProp: r = Bs,
    slotShouldForwardProp: o = Bs
  } = e, i = (l) => Do(w({}, l, {
    theme: ai(w({}, l, {
      defaultTheme: n,
      themeId: t
    }))
  }));
  return i.__mui_systemSx = !0, (l, s = {}) => {
    xh(l, (k) => k.filter((C) => !(C != null && C.__mui_systemSx)));
    const {
      name: a,
      slot: u,
      skipVariantsResolver: c,
      skipSx: f,
      // TODO v6: remove `lowercaseFirstLetter()` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      overridesResolver: p = Ex($x(u))
    } = s, v = L(s, wx), y = a && a.startsWith("Mui") || u ? "components" : "custom", g = c !== void 0 ? c : (
      // TODO v6: remove `Root` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      u && u !== "Root" && u !== "root" || !1
    ), E = f || !1;
    let m, d = Bs;
    u === "Root" || u === "root" ? d = r : u ? d = o : kx(l) && (d = void 0);
    const h = Ju(l, w({
      shouldForwardProp: d,
      label: m
    }, v)), S = (k) => typeof k == "function" && k.__emotion_real !== k || Lt(k) ? (C) => {
      const T = ai({
        theme: C.theme,
        defaultTheme: n,
        themeId: t
      });
      return Ei(k, w({}, C, {
        theme: T
      }), T.modularCssLayers ? y : void 0);
    } : k, $ = (k, ...C) => {
      let T = S(k);
      const z = C ? C.map(S) : [];
      a && p && z.push((F) => {
        const I = ai(w({}, F, {
          defaultTheme: n,
          themeId: t
        }));
        if (!I.components || !I.components[a] || !I.components[a].styleOverrides)
          return null;
        const q = I.components[a].styleOverrides, xe = {};
        return Object.entries(q).forEach(([Ee, Ge]) => {
          xe[Ee] = Ei(Ge, w({}, F, {
            theme: I
          }), I.modularCssLayers ? "theme" : void 0);
        }), p(F, xe);
      }), a && !g && z.push((F) => {
        var I;
        const q = ai(w({}, F, {
          defaultTheme: n,
          themeId: t
        })), xe = q == null || (I = q.components) == null || (I = I[a]) == null ? void 0 : I.variants;
        return Ei({
          variants: xe
        }, w({}, F, {
          theme: q
        }), q.modularCssLayers ? "theme" : void 0);
      }), E || z.push(i);
      const M = z.length - C.length;
      if (Array.isArray(k) && M > 0) {
        const F = new Array(M).fill("");
        T = [...k, ...F], T.raw = [...k.raw, ...F];
      }
      const U = h(T, ...z);
      return l.muiName && (U.muiName = l.muiName), U;
    };
    return h.withConfig && ($.withConfig = h.withConfig), $;
  };
}
const Tx = Px(), Rx = Tx;
function $o(e, t) {
  const n = w({}, t);
  return Object.keys(e).forEach((r) => {
    if (r.toString().match(/^(components|slots)$/))
      n[r] = w({}, e[r], n[r]);
    else if (r.toString().match(/^(componentsProps|slotProps)$/)) {
      const o = e[r] || {}, i = t[r];
      n[r] = {}, !i || !Object.keys(i) ? n[r] = o : !o || !Object.keys(o) ? n[r] = i : (n[r] = w({}, i), Object.keys(o).forEach((l) => {
        n[r][l] = $o(o[l], i[l]);
      }));
    } else
      n[r] === void 0 && (n[r] = e[r]);
  }), n;
}
function Mx(e) {
  const {
    theme: t,
    name: n,
    props: r
  } = e;
  return !t || !t.components || !t.components[n] || !t.components[n].defaultProps ? r : $o(t.components[n].defaultProps, r);
}
function Ox({
  props: e,
  name: t,
  defaultTheme: n,
  themeId: r
}) {
  let o = Vl(n);
  return r && (o = o[r] || o), Mx({
    theme: o,
    name: t,
    props: e
  });
}
const zx = typeof window < "u" ? _.useLayoutEffect : _.useEffect, ac = zx;
function Nx(e, t = Number.MIN_SAFE_INTEGER, n = Number.MAX_SAFE_INTEGER) {
  return Math.max(t, Math.min(e, n));
}
const jx = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Nx
}, Symbol.toStringTag, { value: "Module" }));
function bx(...e) {
  return e.reduce((t, n) => n == null ? t : function(...o) {
    t.apply(this, o), n.apply(this, o);
  }, () => {
  });
}
function Ax(e, t = 166) {
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
function Ix(e, t) {
  return () => null;
}
function Lx(e, t) {
  var n, r;
  return /* @__PURE__ */ _.isValidElement(e) && t.indexOf(
    // For server components `muiName` is avaialble in element.type._payload.value.muiName
    // relevant info - https://github.com/facebook/react/blob/2807d781a08db8e9873687fccc25c0f12b4fb3d4/packages/react/src/ReactLazy.js#L45
    // eslint-disable-next-line no-underscore-dangle
    (n = e.type.muiName) != null ? n : (r = e.type) == null || (r = r._payload) == null || (r = r.value) == null ? void 0 : r.muiName
  ) !== -1;
}
function zh(e) {
  return e && e.ownerDocument || document;
}
function Dx(e) {
  return zh(e).defaultView || window;
}
function Fx(e, t) {
  return () => null;
}
function Nh(e, t) {
  typeof e == "function" ? e(t) : e && (e.current = t);
}
let nf = 0;
function Bx(e) {
  const [t, n] = _.useState(e), r = e || t;
  return _.useEffect(() => {
    t == null && (nf += 1, n(`mui-${nf}`));
  }, [t]), r;
}
const rf = Gs["useId".toString()];
function jh(e) {
  if (rf !== void 0) {
    const t = rf();
    return e ?? t;
  }
  return Bx(e);
}
function Wx(e, t, n, r, o) {
  return null;
}
function Ux({
  controlled: e,
  default: t,
  name: n,
  state: r = "value"
}) {
  const {
    current: o
  } = _.useRef(e !== void 0), [i, l] = _.useState(t), s = o ? e : i, a = _.useCallback((u) => {
    o || l(u);
  }, []);
  return [s, a];
}
function Kr(e) {
  const t = _.useRef(e);
  return ac(() => {
    t.current = e;
  }), _.useRef((...n) => (
    // @ts-expect-error hide `this`
    (0, t.current)(...n)
  )).current;
}
function nl(...e) {
  return _.useMemo(() => e.every((t) => t == null) ? null : (t) => {
    e.forEach((n) => {
      Nh(n, t);
    });
  }, e);
}
const of = {};
function Vx(e, t) {
  const n = _.useRef(of);
  return n.current === of && (n.current = e(t)), n;
}
const Hx = [];
function Kx(e) {
  _.useEffect(e, Hx);
}
class ns {
  constructor() {
    this.currentId = null, this.clear = () => {
      this.currentId !== null && (clearTimeout(this.currentId), this.currentId = null);
    }, this.disposeEffect = () => this.clear;
  }
  static create() {
    return new ns();
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
function Gx() {
  const e = Vx(ns.create).current;
  return Kx(e.disposeEffect), e;
}
let rs = !0, Ha = !1;
const Qx = new ns(), Yx = {
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
function Xx(e) {
  const {
    type: t,
    tagName: n
  } = e;
  return !!(n === "INPUT" && Yx[t] && !e.readOnly || n === "TEXTAREA" && !e.readOnly || e.isContentEditable);
}
function qx(e) {
  e.metaKey || e.altKey || e.ctrlKey || (rs = !0);
}
function Ws() {
  rs = !1;
}
function Zx() {
  this.visibilityState === "hidden" && Ha && (rs = !0);
}
function Jx(e) {
  e.addEventListener("keydown", qx, !0), e.addEventListener("mousedown", Ws, !0), e.addEventListener("pointerdown", Ws, !0), e.addEventListener("touchstart", Ws, !0), e.addEventListener("visibilitychange", Zx, !0);
}
function eS(e) {
  const {
    target: t
  } = e;
  try {
    return t.matches(":focus-visible");
  } catch {
  }
  return rs || Xx(t);
}
function bh() {
  const e = _.useCallback((o) => {
    o != null && Jx(o.ownerDocument);
  }, []), t = _.useRef(!1);
  function n() {
    return t.current ? (Ha = !0, Qx.start(100, () => {
      Ha = !1;
    }), t.current = !1, !0) : !1;
  }
  function r(o) {
    return eS(o) ? (t.current = !0, !0) : !1;
  }
  return {
    isFocusVisibleRef: t,
    onFocus: r,
    onBlur: n,
    ref: e
  };
}
function Ce(e, t, n = void 0) {
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
function tS(e) {
  return typeof e == "string";
}
function nS(e, t, n) {
  return e === void 0 || tS(e) ? t : w({}, t, {
    ownerState: w({}, t.ownerState, n)
  });
}
function rS(e, t = []) {
  if (e === void 0)
    return {};
  const n = {};
  return Object.keys(e).filter((r) => r.match(/^on[A-Z]/) && typeof e[r] == "function" && !t.includes(r)).forEach((r) => {
    n[r] = e[r];
  }), n;
}
function lf(e) {
  if (e === void 0)
    return {};
  const t = {};
  return Object.keys(e).filter((n) => !(n.match(/^on[A-Z]/) && typeof e[n] == "function")).forEach((n) => {
    t[n] = e[n];
  }), t;
}
function oS(e) {
  const {
    getSlotProps: t,
    additionalProps: n,
    externalSlotProps: r,
    externalForwardedProps: o,
    className: i
  } = e;
  if (!t) {
    const v = B(n == null ? void 0 : n.className, i, o == null ? void 0 : o.className, r == null ? void 0 : r.className), y = w({}, n == null ? void 0 : n.style, o == null ? void 0 : o.style, r == null ? void 0 : r.style), g = w({}, n, o, r);
    return v.length > 0 && (g.className = v), Object.keys(y).length > 0 && (g.style = y), {
      props: g,
      internalRef: void 0
    };
  }
  const l = rS(w({}, o, r)), s = lf(r), a = lf(o), u = t(l), c = B(u == null ? void 0 : u.className, n == null ? void 0 : n.className, i, o == null ? void 0 : o.className, r == null ? void 0 : r.className), f = w({}, u == null ? void 0 : u.style, n == null ? void 0 : n.style, o == null ? void 0 : o.style, r == null ? void 0 : r.style), p = w({}, u, n, a, s);
  return c.length > 0 && (p.className = c), Object.keys(f).length > 0 && (p.style = f), {
    props: p,
    internalRef: u.ref
  };
}
function iS(e, t, n) {
  return typeof e == "function" ? e(t, n) : e;
}
const lS = /* @__PURE__ */ _.createContext(null), Ah = lS;
function Ih() {
  return _.useContext(Ah);
}
const sS = typeof Symbol == "function" && Symbol.for, aS = sS ? Symbol.for("mui.nested") : "__THEME_NESTED__";
function uS(e, t) {
  return typeof t == "function" ? t(e) : w({}, e, t);
}
function cS(e) {
  const {
    children: t,
    theme: n
  } = e, r = Ih(), o = _.useMemo(() => {
    const i = r === null ? n : uS(r, n);
    return i != null && (i[aS] = r !== null), i;
  }, [n, r]);
  return /* @__PURE__ */ x.jsx(Ah.Provider, {
    value: o,
    children: t
  });
}
const dS = ["value"], fS = /* @__PURE__ */ _.createContext();
function pS(e) {
  let {
    value: t
  } = e, n = L(e, dS);
  return /* @__PURE__ */ x.jsx(fS.Provider, w({
    value: t ?? !0
  }, n));
}
const Lh = /* @__PURE__ */ _.createContext(void 0);
function mS({
  value: e,
  children: t
}) {
  return /* @__PURE__ */ x.jsx(Lh.Provider, {
    value: e,
    children: t
  });
}
function hS(e) {
  const {
    theme: t,
    name: n,
    props: r
  } = e;
  if (!t || !t.components || !t.components[n])
    return r;
  const o = t.components[n];
  return o.defaultProps ? $o(o.defaultProps, r) : !o.styleOverrides && !o.variants ? $o(o, r) : r;
}
function gS({
  props: e,
  name: t
}) {
  const n = _.useContext(Lh);
  return hS({
    props: e,
    name: t,
    theme: {
      components: n
    }
  });
}
function vS(e) {
  const t = oc(), n = jh() || "", {
    modularCssLayers: r
  } = e;
  let o = "mui.global, mui.components, mui.theme, mui.custom, mui.sx";
  return !r || t !== null ? o = "" : typeof r == "string" ? o = r.replace(/mui(?!\.)/g, o) : o = `@layer ${o};`, ac(() => {
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
  }, [o, n]), o ? /* @__PURE__ */ x.jsx(Ph, {
    styles: o
  }) : null;
}
const sf = {};
function af(e, t, n, r = !1) {
  return _.useMemo(() => {
    const o = e && t[e] || t;
    if (typeof n == "function") {
      const i = n(o), l = e ? w({}, t, {
        [e]: i
      }) : i;
      return r ? () => l : l;
    }
    return e ? w({}, t, {
      [e]: n
    }) : w({}, t, n);
  }, [e, t, n, r]);
}
function yS(e) {
  const {
    children: t,
    theme: n,
    themeId: r
  } = e, o = oc(sf), i = Ih() || sf, l = af(r, o, n), s = af(r, i, n, !0), a = l.direction === "rtl", u = vS(l);
  return /* @__PURE__ */ x.jsx(cS, {
    theme: s,
    children: /* @__PURE__ */ x.jsx(kr.Provider, {
      value: l,
      children: /* @__PURE__ */ x.jsx(pS, {
        value: a,
        children: /* @__PURE__ */ x.jsxs(mS, {
          value: l == null ? void 0 : l.components,
          children: [u, t]
        })
      })
    })
  });
}
const xS = ["className", "component", "disableGutters", "fixed", "maxWidth", "classes"], SS = Fo(), wS = Rx("div", {
  name: "MuiContainer",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[`maxWidth${j(String(n.maxWidth))}`], n.fixed && t.fixed, n.disableGutters && t.disableGutters];
  }
}), CS = (e) => Ox({
  props: e,
  name: "MuiContainer",
  defaultTheme: SS
}), kS = (e, t) => {
  const n = (a) => ve(t, a), {
    classes: r,
    fixed: o,
    disableGutters: i,
    maxWidth: l
  } = e, s = {
    root: ["root", l && `maxWidth${j(String(l))}`, o && "fixed", i && "disableGutters"]
  };
  return Ce(s, n, r);
};
function _S(e = {}) {
  const {
    // This will allow adding custom styled fn (for example for custom sx style function)
    createStyledComponent: t = wS,
    useThemeProps: n = CS,
    componentName: r = "MuiContainer"
  } = e, o = t(({
    theme: l,
    ownerState: s
  }) => w({
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
  }) => w({}, s.maxWidth === "xs" && {
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
  return /* @__PURE__ */ _.forwardRef(function(s, a) {
    const u = n(s), {
      className: c,
      component: f = "div",
      disableGutters: p = !1,
      fixed: v = !1,
      maxWidth: y = "lg"
    } = u, g = L(u, xS), E = w({}, u, {
      component: f,
      disableGutters: p,
      fixed: v,
      maxWidth: y
    }), m = kS(E, r);
    return (
      // @ts-ignore theme is injected by the styled util
      /* @__PURE__ */ x.jsx(o, w({
        as: f,
        ownerState: E,
        className: B(m.root, c),
        ref: a
      }, g))
    );
  });
}
function $S(e, t) {
  return w({
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
var de = {}, Dh = { exports: {} };
(function(e) {
  function t(n) {
    return n && n.__esModule ? n : {
      default: n
    };
  }
  e.exports = t, e.exports.__esModule = !0, e.exports.default = e.exports;
})(Dh);
var yn = Dh.exports;
const ES = /* @__PURE__ */ Kt(Xv), PS = /* @__PURE__ */ Kt(jx);
var Fh = yn;
Object.defineProperty(de, "__esModule", {
  value: !0
});
var ut = de.alpha = Vh;
de.blend = LS;
de.colorChannel = void 0;
var rl = de.darken = cc;
de.decomposeColor = mt;
de.emphasize = Hh;
var TS = de.getContrastRatio = NS;
de.getLuminance = il;
de.hexToRgb = Bh;
de.hslToRgb = Uh;
var ol = de.lighten = dc;
de.private_safeAlpha = jS;
de.private_safeColorChannel = void 0;
de.private_safeDarken = bS;
de.private_safeEmphasize = IS;
de.private_safeLighten = AS;
de.recomposeColor = $r;
de.rgbToHex = zS;
var uf = Fh(ES), RS = Fh(PS);
function uc(e, t = 0, n = 1) {
  return (0, RS.default)(e, t, n);
}
function Bh(e) {
  e = e.slice(1);
  const t = new RegExp(`.{1,${e.length >= 6 ? 2 : 1}}`, "g");
  let n = e.match(t);
  return n && n[0].length === 1 && (n = n.map((r) => r + r)), n ? `rgb${n.length === 4 ? "a" : ""}(${n.map((r, o) => o < 3 ? parseInt(r, 16) : Math.round(parseInt(r, 16) / 255 * 1e3) / 1e3).join(", ")})` : "";
}
function MS(e) {
  const t = e.toString(16);
  return t.length === 1 ? `0${t}` : t;
}
function mt(e) {
  if (e.type)
    return e;
  if (e.charAt(0) === "#")
    return mt(Bh(e));
  const t = e.indexOf("("), n = e.substring(0, t);
  if (["rgb", "rgba", "hsl", "hsla", "color"].indexOf(n) === -1)
    throw new Error((0, uf.default)(9, e));
  let r = e.substring(t + 1, e.length - 1), o;
  if (n === "color") {
    if (r = r.split(" "), o = r.shift(), r.length === 4 && r[3].charAt(0) === "/" && (r[3] = r[3].slice(1)), ["srgb", "display-p3", "a98-rgb", "prophoto-rgb", "rec-2020"].indexOf(o) === -1)
      throw new Error((0, uf.default)(10, o));
  } else
    r = r.split(",");
  return r = r.map((i) => parseFloat(i)), {
    type: n,
    values: r,
    colorSpace: o
  };
}
const Wh = (e) => {
  const t = mt(e);
  return t.values.slice(0, 3).map((n, r) => t.type.indexOf("hsl") !== -1 && r !== 0 ? `${n}%` : n).join(" ");
};
de.colorChannel = Wh;
const OS = (e, t) => {
  try {
    return Wh(e);
  } catch {
    return e;
  }
};
de.private_safeColorChannel = OS;
function $r(e) {
  const {
    type: t,
    colorSpace: n
  } = e;
  let {
    values: r
  } = e;
  return t.indexOf("rgb") !== -1 ? r = r.map((o, i) => i < 3 ? parseInt(o, 10) : o) : t.indexOf("hsl") !== -1 && (r[1] = `${r[1]}%`, r[2] = `${r[2]}%`), t.indexOf("color") !== -1 ? r = `${n} ${r.join(" ")}` : r = `${r.join(", ")}`, `${t}(${r})`;
}
function zS(e) {
  if (e.indexOf("#") === 0)
    return e;
  const {
    values: t
  } = mt(e);
  return `#${t.map((n, r) => MS(r === 3 ? Math.round(255 * n) : n)).join("")}`;
}
function Uh(e) {
  e = mt(e);
  const {
    values: t
  } = e, n = t[0], r = t[1] / 100, o = t[2] / 100, i = r * Math.min(o, 1 - o), l = (u, c = (u + n / 30) % 12) => o - i * Math.max(Math.min(c - 3, 9 - c, 1), -1);
  let s = "rgb";
  const a = [Math.round(l(0) * 255), Math.round(l(8) * 255), Math.round(l(4) * 255)];
  return e.type === "hsla" && (s += "a", a.push(t[3])), $r({
    type: s,
    values: a
  });
}
function il(e) {
  e = mt(e);
  let t = e.type === "hsl" || e.type === "hsla" ? mt(Uh(e)).values : e.values;
  return t = t.map((n) => (e.type !== "color" && (n /= 255), n <= 0.03928 ? n / 12.92 : ((n + 0.055) / 1.055) ** 2.4)), Number((0.2126 * t[0] + 0.7152 * t[1] + 0.0722 * t[2]).toFixed(3));
}
function NS(e, t) {
  const n = il(e), r = il(t);
  return (Math.max(n, r) + 0.05) / (Math.min(n, r) + 0.05);
}
function Vh(e, t) {
  return e = mt(e), t = uc(t), (e.type === "rgb" || e.type === "hsl") && (e.type += "a"), e.type === "color" ? e.values[3] = `/${t}` : e.values[3] = t, $r(e);
}
function jS(e, t, n) {
  try {
    return Vh(e, t);
  } catch {
    return e;
  }
}
function cc(e, t) {
  if (e = mt(e), t = uc(t), e.type.indexOf("hsl") !== -1)
    e.values[2] *= 1 - t;
  else if (e.type.indexOf("rgb") !== -1 || e.type.indexOf("color") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] *= 1 - t;
  return $r(e);
}
function bS(e, t, n) {
  try {
    return cc(e, t);
  } catch {
    return e;
  }
}
function dc(e, t) {
  if (e = mt(e), t = uc(t), e.type.indexOf("hsl") !== -1)
    e.values[2] += (100 - e.values[2]) * t;
  else if (e.type.indexOf("rgb") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] += (255 - e.values[n]) * t;
  else if (e.type.indexOf("color") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] += (1 - e.values[n]) * t;
  return $r(e);
}
function AS(e, t, n) {
  try {
    return dc(e, t);
  } catch {
    return e;
  }
}
function Hh(e, t = 0.15) {
  return il(e) > 0.5 ? cc(e, t) : dc(e, t);
}
function IS(e, t, n) {
  try {
    return Hh(e, t);
  } catch {
    return e;
  }
}
function LS(e, t, n, r = 1) {
  const o = (a, u) => Math.round((a ** (1 / r) * (1 - n) + u ** (1 / r) * n) ** r), i = mt(e), l = mt(t), s = [o(i.values[0], l.values[0]), o(i.values[1], l.values[1]), o(i.values[2], l.values[2])];
  return $r({
    type: "rgb",
    values: s
  });
}
const DS = {
  black: "#000",
  white: "#fff"
}, Eo = DS, FS = {
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
}, BS = FS, WS = {
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
}, Ln = WS, US = {
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
}, Dn = US, VS = {
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
}, Dr = VS, HS = {
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
}, Fn = HS, KS = {
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
}, Bn = KS, GS = {
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
}, Wn = GS, QS = ["mode", "contrastThreshold", "tonalOffset"], cf = {
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
    paper: Eo.white,
    default: Eo.white
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
    primary: Eo.white,
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
    active: Eo.white,
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
function df(e, t, n, r) {
  const o = r.light || r, i = r.dark || r * 1.5;
  e[t] || (e.hasOwnProperty(n) ? e[t] = e[n] : t === "light" ? e.light = ol(e.main, o) : t === "dark" && (e.dark = rl(e.main, i)));
}
function YS(e = "light") {
  return e === "dark" ? {
    main: Fn[200],
    light: Fn[50],
    dark: Fn[400]
  } : {
    main: Fn[700],
    light: Fn[400],
    dark: Fn[800]
  };
}
function XS(e = "light") {
  return e === "dark" ? {
    main: Ln[200],
    light: Ln[50],
    dark: Ln[400]
  } : {
    main: Ln[500],
    light: Ln[300],
    dark: Ln[700]
  };
}
function qS(e = "light") {
  return e === "dark" ? {
    main: Dn[500],
    light: Dn[300],
    dark: Dn[700]
  } : {
    main: Dn[700],
    light: Dn[400],
    dark: Dn[800]
  };
}
function ZS(e = "light") {
  return e === "dark" ? {
    main: Bn[400],
    light: Bn[300],
    dark: Bn[700]
  } : {
    main: Bn[700],
    light: Bn[500],
    dark: Bn[900]
  };
}
function JS(e = "light") {
  return e === "dark" ? {
    main: Wn[400],
    light: Wn[300],
    dark: Wn[700]
  } : {
    main: Wn[800],
    light: Wn[500],
    dark: Wn[900]
  };
}
function e2(e = "light") {
  return e === "dark" ? {
    main: Dr[400],
    light: Dr[300],
    dark: Dr[700]
  } : {
    main: "#ed6c02",
    // closest to orange[800] that pass 3:1.
    light: Dr[500],
    dark: Dr[900]
  };
}
function t2(e) {
  const {
    mode: t = "light",
    contrastThreshold: n = 3,
    tonalOffset: r = 0.2
  } = e, o = L(e, QS), i = e.primary || YS(t), l = e.secondary || XS(t), s = e.error || qS(t), a = e.info || ZS(t), u = e.success || JS(t), c = e.warning || e2(t);
  function f(g) {
    return TS(g, Us.text.primary) >= n ? Us.text.primary : cf.text.primary;
  }
  const p = ({
    color: g,
    name: E,
    mainShade: m = 500,
    lightShade: d = 300,
    darkShade: h = 700
  }) => {
    if (g = w({}, g), !g.main && g[m] && (g.main = g[m]), !g.hasOwnProperty("main"))
      throw new Error(wo(11, E ? ` (${E})` : "", m));
    if (typeof g.main != "string")
      throw new Error(wo(12, E ? ` (${E})` : "", JSON.stringify(g.main)));
    return df(g, "light", d, r), df(g, "dark", h, r), g.contrastText || (g.contrastText = f(g.main)), g;
  }, v = {
    dark: Us,
    light: cf
  };
  return jt(w({
    // A collection of common colors.
    common: w({}, Eo),
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
    grey: BS,
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
const n2 = ["fontFamily", "fontSize", "fontWeightLight", "fontWeightRegular", "fontWeightMedium", "fontWeightBold", "htmlFontSize", "allVariants", "pxToRem"];
function r2(e) {
  return Math.round(e * 1e5) / 1e5;
}
const ff = {
  textTransform: "uppercase"
}, pf = '"Roboto", "Helvetica", "Arial", sans-serif';
function o2(e, t) {
  const n = typeof t == "function" ? t(e) : t, {
    fontFamily: r = pf,
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
  } = n, p = L(n, n2), v = o / 14, y = f || ((m) => `${m / u * v}rem`), g = (m, d, h, S, $) => w({
    fontFamily: r,
    fontWeight: m,
    fontSize: y(d),
    // Unitless following https://meyerweb.com/eric/thoughts/2006/02/08/unitless-line-heights/
    lineHeight: h
  }, r === pf ? {
    letterSpacing: `${r2(S / d)}em`
  } : {}, $, c), E = {
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
    button: g(s, 14, 1.75, 0.4, ff),
    caption: g(l, 12, 1.66, 0.4),
    overline: g(l, 12, 2.66, 1, ff),
    // TODO v6: Remove handling of 'inherit' variant from the theme as it is already handled in Material UI's Typography component. Also, remember to remove the associated types.
    inherit: {
      fontFamily: "inherit",
      fontWeight: "inherit",
      fontSize: "inherit",
      lineHeight: "inherit",
      letterSpacing: "inherit"
    }
  };
  return jt(w({
    htmlFontSize: u,
    pxToRem: y,
    fontFamily: r,
    fontSize: o,
    fontWeightLight: i,
    fontWeightRegular: l,
    fontWeightMedium: s,
    fontWeightBold: a
  }, E), p, {
    clone: !1
    // No need to clone deep
  });
}
const i2 = 0.2, l2 = 0.14, s2 = 0.12;
function ee(...e) {
  return [`${e[0]}px ${e[1]}px ${e[2]}px ${e[3]}px rgba(0,0,0,${i2})`, `${e[4]}px ${e[5]}px ${e[6]}px ${e[7]}px rgba(0,0,0,${l2})`, `${e[8]}px ${e[9]}px ${e[10]}px ${e[11]}px rgba(0,0,0,${s2})`].join(",");
}
const a2 = ["none", ee(0, 2, 1, -1, 0, 1, 1, 0, 0, 1, 3, 0), ee(0, 3, 1, -2, 0, 2, 2, 0, 0, 1, 5, 0), ee(0, 3, 3, -2, 0, 3, 4, 0, 0, 1, 8, 0), ee(0, 2, 4, -1, 0, 4, 5, 0, 0, 1, 10, 0), ee(0, 3, 5, -1, 0, 5, 8, 0, 0, 1, 14, 0), ee(0, 3, 5, -1, 0, 6, 10, 0, 0, 1, 18, 0), ee(0, 4, 5, -2, 0, 7, 10, 1, 0, 2, 16, 1), ee(0, 5, 5, -3, 0, 8, 10, 1, 0, 3, 14, 2), ee(0, 5, 6, -3, 0, 9, 12, 1, 0, 3, 16, 2), ee(0, 6, 6, -3, 0, 10, 14, 1, 0, 4, 18, 3), ee(0, 6, 7, -4, 0, 11, 15, 1, 0, 4, 20, 3), ee(0, 7, 8, -4, 0, 12, 17, 2, 0, 5, 22, 4), ee(0, 7, 8, -4, 0, 13, 19, 2, 0, 5, 24, 4), ee(0, 7, 9, -4, 0, 14, 21, 2, 0, 5, 26, 4), ee(0, 8, 9, -5, 0, 15, 22, 2, 0, 6, 28, 5), ee(0, 8, 10, -5, 0, 16, 24, 2, 0, 6, 30, 5), ee(0, 8, 11, -5, 0, 17, 26, 2, 0, 6, 32, 5), ee(0, 9, 11, -5, 0, 18, 28, 2, 0, 7, 34, 6), ee(0, 9, 12, -6, 0, 19, 29, 2, 0, 7, 36, 6), ee(0, 10, 13, -6, 0, 20, 31, 3, 0, 8, 38, 7), ee(0, 10, 13, -6, 0, 21, 33, 3, 0, 8, 40, 7), ee(0, 10, 14, -6, 0, 22, 35, 3, 0, 8, 42, 7), ee(0, 11, 14, -7, 0, 23, 36, 3, 0, 9, 44, 8), ee(0, 11, 15, -7, 0, 24, 38, 3, 0, 9, 46, 8)], u2 = a2, c2 = ["duration", "easing", "delay"], d2 = {
  // This is the most common easing curve.
  easeInOut: "cubic-bezier(0.4, 0, 0.2, 1)",
  // Objects enter the screen at full velocity from off-screen and
  // slowly decelerate to a resting point.
  easeOut: "cubic-bezier(0.0, 0, 0.2, 1)",
  // Objects leave the screen at full velocity. They do not decelerate when off-screen.
  easeIn: "cubic-bezier(0.4, 0, 1, 1)",
  // The sharp curve is used by objects that may return to the screen at any time.
  sharp: "cubic-bezier(0.4, 0, 0.6, 1)"
}, f2 = {
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
function mf(e) {
  return `${Math.round(e)}ms`;
}
function p2(e) {
  if (!e)
    return 0;
  const t = e / 36;
  return Math.round((4 + 15 * t ** 0.25 + t / 5) * 10);
}
function m2(e) {
  const t = w({}, d2, e.easing), n = w({}, f2, e.duration);
  return w({
    getAutoHeightDuration: p2,
    create: (o = ["all"], i = {}) => {
      const {
        duration: l = n.standard,
        easing: s = t.easeInOut,
        delay: a = 0
      } = i;
      return L(i, c2), (Array.isArray(o) ? o : [o]).map((u) => `${u} ${typeof l == "string" ? l : mf(l)} ${s} ${typeof a == "string" ? a : mf(a)}`).join(",");
    }
  }, e, {
    easing: t,
    duration: n
  });
}
const h2 = {
  mobileStepper: 1e3,
  fab: 1050,
  speedDial: 1050,
  appBar: 1100,
  drawer: 1200,
  modal: 1300,
  snackbar: 1400,
  tooltip: 1500
}, g2 = h2, v2 = ["breakpoints", "mixins", "spacing", "palette", "transitions", "typography", "shape"];
function fc(e = {}, ...t) {
  const {
    mixins: n = {},
    palette: r = {},
    transitions: o = {},
    typography: i = {}
  } = e, l = L(e, v2);
  if (e.vars && // The error should throw only for the root theme creation because user is not allowed to use a custom node `vars`.
  // `generateCssVars` is the closest identifier for checking that the `options` is a result of `extendTheme` with CSS variables so that user can create new theme for nested ThemeProvider.
  e.generateCssVars === void 0)
    throw new Error(wo(18));
  const s = t2(r), a = Fo(e);
  let u = jt(a, {
    mixins: $S(a.breakpoints, n),
    palette: s,
    // Don't use [...shadows] until you've verified its transpiled code is not invoking the iterator protocol.
    shadows: u2.slice(),
    typography: o2(s, i),
    transitions: m2(o),
    zIndex: w({}, g2)
  });
  return u = jt(u, l), u = t.reduce((c, f) => jt(c, f), u), u.unstable_sxConfig = w({}, Lo, l == null ? void 0 : l.unstable_sxConfig), u.unstable_sx = function(f) {
    return Do({
      sx: f,
      theme: this
    });
  }, u;
}
const y2 = fc(), pc = y2;
function x2() {
  const e = Vl(pc);
  return e[vr] || e;
}
var Bo = {}, Vs = { exports: {} }, hf;
function S2() {
  return hf || (hf = 1, function(e) {
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
const w2 = /* @__PURE__ */ Kt(s1), C2 = /* @__PURE__ */ Kt(a1), k2 = /* @__PURE__ */ Kt(h1), _2 = /* @__PURE__ */ Kt(yx), $2 = /* @__PURE__ */ Kt(rx), E2 = /* @__PURE__ */ Kt(ax);
var Er = yn;
Object.defineProperty(Bo, "__esModule", {
  value: !0
});
var P2 = Bo.default = F2;
Bo.shouldForwardProp = Pi;
Bo.systemDefaultTheme = void 0;
var rt = Er(vh()), Ka = Er(S2()), ll = j2(w2), T2 = C2;
Er(k2);
Er(_2);
var R2 = Er($2), M2 = Er(E2);
const O2 = ["ownerState"], z2 = ["variants"], N2 = ["name", "slot", "skipVariantsResolver", "skipSx", "overridesResolver"];
function Kh(e) {
  if (typeof WeakMap != "function")
    return null;
  var t = /* @__PURE__ */ new WeakMap(), n = /* @__PURE__ */ new WeakMap();
  return (Kh = function(r) {
    return r ? n : t;
  })(e);
}
function j2(e, t) {
  if (!t && e && e.__esModule)
    return e;
  if (e === null || typeof e != "object" && typeof e != "function")
    return { default: e };
  var n = Kh(t);
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
function b2(e) {
  return Object.keys(e).length === 0;
}
function A2(e) {
  return typeof e == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  e.charCodeAt(0) > 96;
}
function Pi(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
function gf(e, t) {
  return t && e && typeof e == "object" && e.styles && !e.styles.startsWith("@layer") && (e.styles = `@layer ${t}{${String(e.styles)}}`), e;
}
const I2 = Bo.systemDefaultTheme = (0, R2.default)(), L2 = (e) => e && e.charAt(0).toLowerCase() + e.slice(1);
function ui({
  defaultTheme: e,
  theme: t,
  themeId: n
}) {
  return b2(t) ? e : t[n] || t;
}
function D2(e) {
  return e ? (t, n) => n[e] : null;
}
function Ti(e, t, n) {
  let {
    ownerState: r
  } = t, o = (0, Ka.default)(t, O2);
  const i = typeof e == "function" ? e((0, rt.default)({
    ownerState: r
  }, o)) : e;
  if (Array.isArray(i))
    return i.flatMap((l) => Ti(l, (0, rt.default)({
      ownerState: r
    }, o), n));
  if (i && typeof i == "object" && Array.isArray(i.variants)) {
    const {
      variants: l = []
    } = i;
    let a = (0, Ka.default)(i, z2);
    return l.forEach((u) => {
      let c = !0;
      if (typeof u.props == "function" ? c = u.props((0, rt.default)({
        ownerState: r
      }, o, r)) : Object.keys(u.props).forEach((f) => {
        (r == null ? void 0 : r[f]) !== u.props[f] && o[f] !== u.props[f] && (c = !1);
      }), c) {
        Array.isArray(a) || (a = [a]);
        const f = typeof u.style == "function" ? u.style((0, rt.default)({
          ownerState: r
        }, o, r)) : u.style;
        a.push(n ? gf((0, ll.internal_serializeStyles)(f), n) : f);
      }
    }), a;
  }
  return n ? gf((0, ll.internal_serializeStyles)(i), n) : i;
}
function F2(e = {}) {
  const {
    themeId: t,
    defaultTheme: n = I2,
    rootShouldForwardProp: r = Pi,
    slotShouldForwardProp: o = Pi
  } = e, i = (l) => (0, M2.default)((0, rt.default)({}, l, {
    theme: ui((0, rt.default)({}, l, {
      defaultTheme: n,
      themeId: t
    }))
  }));
  return i.__mui_systemSx = !0, (l, s = {}) => {
    (0, ll.internal_processStyles)(l, (k) => k.filter((C) => !(C != null && C.__mui_systemSx)));
    const {
      name: a,
      slot: u,
      skipVariantsResolver: c,
      skipSx: f,
      // TODO v6: remove `lowercaseFirstLetter()` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      overridesResolver: p = D2(L2(u))
    } = s, v = (0, Ka.default)(s, N2), y = a && a.startsWith("Mui") || u ? "components" : "custom", g = c !== void 0 ? c : (
      // TODO v6: remove `Root` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      u && u !== "Root" && u !== "root" || !1
    ), E = f || !1;
    let m, d = Pi;
    u === "Root" || u === "root" ? d = r : u ? d = o : A2(l) && (d = void 0);
    const h = (0, ll.default)(l, (0, rt.default)({
      shouldForwardProp: d,
      label: m
    }, v)), S = (k) => typeof k == "function" && k.__emotion_real !== k || (0, T2.isPlainObject)(k) ? (C) => {
      const T = ui({
        theme: C.theme,
        defaultTheme: n,
        themeId: t
      });
      return Ti(k, (0, rt.default)({}, C, {
        theme: T
      }), T.modularCssLayers ? y : void 0);
    } : k, $ = (k, ...C) => {
      let T = S(k);
      const z = C ? C.map(S) : [];
      a && p && z.push((F) => {
        const I = ui((0, rt.default)({}, F, {
          defaultTheme: n,
          themeId: t
        }));
        if (!I.components || !I.components[a] || !I.components[a].styleOverrides)
          return null;
        const q = I.components[a].styleOverrides, xe = {};
        return Object.entries(q).forEach(([Ee, Ge]) => {
          xe[Ee] = Ti(Ge, (0, rt.default)({}, F, {
            theme: I
          }), I.modularCssLayers ? "theme" : void 0);
        }), p(F, xe);
      }), a && !g && z.push((F) => {
        var I;
        const q = ui((0, rt.default)({}, F, {
          defaultTheme: n,
          themeId: t
        })), xe = q == null || (I = q.components) == null || (I = I[a]) == null ? void 0 : I.variants;
        return Ti({
          variants: xe
        }, (0, rt.default)({}, F, {
          theme: q
        }), q.modularCssLayers ? "theme" : void 0);
      }), E || z.push(i);
      const M = z.length - C.length;
      if (Array.isArray(k) && M > 0) {
        const F = new Array(M).fill("");
        T = [...k, ...F], T.raw = [...k.raw, ...F];
      }
      const U = h(T, ...z);
      return l.muiName && (U.muiName = l.muiName), U;
    };
    return h.withConfig && ($.withConfig = h.withConfig), $;
  };
}
function B2(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
const W2 = (e) => B2(e) && e !== "classes", Gh = W2, U2 = P2({
  themeId: vr,
  defaultTheme: pc,
  rootShouldForwardProp: Gh
}), Q = U2, V2 = ["theme"];
function H2(e) {
  let {
    theme: t
  } = e, n = L(e, V2);
  const r = t[vr];
  let o = r || t;
  return typeof t != "function" && (r && !r.vars ? o = w({}, r, {
    vars: null
  }) : t && !t.vars && (o = w({}, t, {
    vars: null
  }))), /* @__PURE__ */ x.jsx(yS, w({}, n, {
    themeId: r ? vr : void 0,
    theme: o
  }));
}
const K2 = (e) => {
  let t;
  return e < 1 ? t = 5.11916 * e ** 2 : t = 4.5 * Math.log(e + 1) + 2, (t / 100).toFixed(2);
}, vf = K2;
function fe(e) {
  return gS(e);
}
function G2(e) {
  return /* @__PURE__ */ x.jsx(Ph, w({}, e, {
    defaultTheme: pc,
    themeId: vr
  }));
}
const Q2 = (e, t) => w({
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
}), Y2 = (e) => w({
  color: (e.vars || e).palette.text.primary
}, e.typography.body1, {
  backgroundColor: (e.vars || e).palette.background.default,
  "@media print": {
    // Save printer ink.
    backgroundColor: (e.vars || e).palette.common.white
  }
}), X2 = (e, t = !1) => {
  var n;
  const r = {};
  t && e.colorSchemes && Object.entries(e.colorSchemes).forEach(([l, s]) => {
    var a;
    r[e.getColorSchemeSelector(l).replace(/\s*&/, "")] = {
      colorScheme: (a = s.palette) == null ? void 0 : a.mode
    };
  });
  let o = w({
    html: Q2(e, t),
    "*, *::before, *::after": {
      boxSizing: "inherit"
    },
    "strong, b": {
      fontWeight: e.typography.fontWeightBold
    },
    body: w({
      margin: 0
    }, Y2(e), {
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
function q2(e) {
  const t = fe({
    props: e,
    name: "MuiCssBaseline"
  }), {
    children: n,
    enableColorScheme: r = !1
  } = t;
  return /* @__PURE__ */ x.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ x.jsx(G2, {
      styles: (o) => X2(o, r)
    }), n]
  });
}
const Z2 = _S({
  createStyledComponent: Q("div", {
    name: "MuiContainer",
    slot: "Root",
    overridesResolver: (e, t) => {
      const {
        ownerState: n
      } = e;
      return [t.root, t[`maxWidth${j(String(n.maxWidth))}`], n.fixed && t.fixed, n.disableGutters && t.disableGutters];
    }
  }),
  useThemeProps: (e) => fe({
    props: e,
    name: "MuiContainer"
  })
}), J2 = Z2;
function ew(e) {
  return ve("MuiTypography", e);
}
ye("MuiTypography", ["root", "h1", "h2", "h3", "h4", "h5", "h6", "subtitle1", "subtitle2", "body1", "body2", "inherit", "button", "caption", "overline", "alignLeft", "alignRight", "alignCenter", "alignJustify", "noWrap", "gutterBottom", "paragraph"]);
const tw = ["align", "className", "component", "gutterBottom", "noWrap", "paragraph", "variant", "variantMapping"], nw = (e) => {
  const {
    align: t,
    gutterBottom: n,
    noWrap: r,
    paragraph: o,
    variant: i,
    classes: l
  } = e, s = {
    root: ["root", i, e.align !== "inherit" && `align${j(t)}`, n && "gutterBottom", r && "noWrap", o && "paragraph"]
  };
  return Ce(s, ew, l);
}, rw = Q("span", {
  name: "MuiTypography",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.variant && t[n.variant], n.align !== "inherit" && t[`align${j(n.align)}`], n.noWrap && t.noWrap, n.gutterBottom && t.gutterBottom, n.paragraph && t.paragraph];
  }
})(({
  theme: e,
  ownerState: t
}) => w({
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
})), yf = {
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
}, ow = {
  primary: "primary.main",
  textPrimary: "text.primary",
  secondary: "secondary.main",
  textSecondary: "text.secondary",
  error: "error.main"
}, iw = (e) => ow[e] || e, lw = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
    props: t,
    name: "MuiTypography"
  }), o = iw(r.color), i = Hl(w({}, r, {
    color: o
  })), {
    align: l = "inherit",
    className: s,
    component: a,
    gutterBottom: u = !1,
    noWrap: c = !1,
    paragraph: f = !1,
    variant: p = "body1",
    variantMapping: v = yf
  } = i, y = L(i, tw), g = w({}, i, {
    align: l,
    color: o,
    className: s,
    component: a,
    gutterBottom: u,
    noWrap: c,
    paragraph: f,
    variant: p,
    variantMapping: v
  }), E = a || (f ? "p" : v[p] || yf[p]) || "span", m = nw(g);
  return /* @__PURE__ */ x.jsx(rw, w({
    as: E,
    ref: n,
    ownerState: g,
    className: B(m.root, s)
  }, y));
}), me = lw;
function sw(e) {
  return ve("MuiCircularProgress", e);
}
ye("MuiCircularProgress", ["root", "determinate", "indeterminate", "colorPrimary", "colorSecondary", "svg", "circle", "circleDeterminate", "circleIndeterminate", "circleDisableShrink"]);
const aw = ["className", "color", "disableShrink", "size", "style", "thickness", "value", "variant"];
let os = (e) => e, xf, Sf, wf, Cf;
const Xt = 44, uw = _r(xf || (xf = os`
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
`)), cw = _r(Sf || (Sf = os`
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
`)), dw = (e) => {
  const {
    classes: t,
    variant: n,
    color: r,
    disableShrink: o
  } = e, i = {
    root: ["root", n, `color${j(r)}`],
    svg: ["svg"],
    circle: ["circle", `circle${j(n)}`, o && "circleDisableShrink"]
  };
  return Ce(i, sw, t);
}, fw = Q("span", {
  name: "MuiCircularProgress",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[n.variant], t[`color${j(n.color)}`]];
  }
})(({
  ownerState: e,
  theme: t
}) => w({
  display: "inline-block"
}, e.variant === "determinate" && {
  transition: t.transitions.create("transform")
}, e.color !== "inherit" && {
  color: (t.vars || t).palette[e.color].main
}), ({
  ownerState: e
}) => e.variant === "indeterminate" && Al(wf || (wf = os`
      animation: ${0} 1.4s linear infinite;
    `), uw)), pw = Q("svg", {
  name: "MuiCircularProgress",
  slot: "Svg",
  overridesResolver: (e, t) => t.svg
})({
  display: "block"
  // Keeps the progress centered
}), mw = Q("circle", {
  name: "MuiCircularProgress",
  slot: "Circle",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.circle, t[`circle${j(n.variant)}`], n.disableShrink && t.circleDisableShrink];
  }
})(({
  ownerState: e,
  theme: t
}) => w({
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
}) => e.variant === "indeterminate" && !e.disableShrink && Al(Cf || (Cf = os`
      animation: ${0} 1.4s ease-in-out infinite;
    `), cw)), hw = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
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
  } = r, p = L(r, aw), v = w({}, r, {
    color: i,
    disableShrink: l,
    size: s,
    thickness: u,
    value: c,
    variant: f
  }), y = dw(v), g = {}, E = {}, m = {};
  if (f === "determinate") {
    const d = 2 * Math.PI * ((Xt - u) / 2);
    g.strokeDasharray = d.toFixed(3), m["aria-valuenow"] = Math.round(c), g.strokeDashoffset = `${((100 - c) / 100 * d).toFixed(3)}px`, E.transform = "rotate(-90deg)";
  }
  return /* @__PURE__ */ x.jsx(fw, w({
    className: B(y.root, o),
    style: w({
      width: s,
      height: s
    }, E, a),
    ownerState: v,
    ref: n,
    role: "progressbar"
  }, m, p, {
    children: /* @__PURE__ */ x.jsx(pw, {
      className: y.svg,
      ownerState: v,
      viewBox: `${Xt / 2} ${Xt / 2} ${Xt} ${Xt}`,
      children: /* @__PURE__ */ x.jsx(mw, {
        className: y.circle,
        style: g,
        ownerState: v,
        cx: Xt,
        cy: Xt,
        r: (Xt - u) / 2,
        fill: "none",
        strokeWidth: u
      })
    })
  }));
}), gw = hw, vw = ["className", "elementType", "ownerState", "externalForwardedProps", "getSlotOwnerState", "internalForwardedProps"], yw = ["component", "slots", "slotProps"], xw = ["component"];
function kf(e, t) {
  const {
    className: n,
    elementType: r,
    ownerState: o,
    externalForwardedProps: i,
    getSlotOwnerState: l,
    internalForwardedProps: s
  } = t, a = L(t, vw), {
    component: u,
    slots: c = {
      [e]: void 0
    },
    slotProps: f = {
      [e]: void 0
    }
  } = i, p = L(i, yw), v = c[e] || r, y = iS(f[e], o), g = oS(w({
    className: n
  }, a, {
    externalForwardedProps: e === "root" ? p : void 0,
    externalSlotProps: y
  })), {
    props: {
      component: E
    },
    internalRef: m
  } = g, d = L(g.props, xw), h = nl(m, y == null ? void 0 : y.ref, t.ref), S = l ? l(d) : {}, $ = w({}, o, S), k = e === "root" ? E || u : E, C = nS(v, w({}, e === "root" && !u && !c[e] && s, e !== "root" && !c[e] && s, d, k && {
    as: k
  }, {
    ref: h
  }), $);
  return Object.keys(S).forEach((T) => {
    delete C[T];
  }), [v, C];
}
function Sw(e) {
  return ve("MuiPaper", e);
}
ye("MuiPaper", ["root", "rounded", "outlined", "elevation", "elevation0", "elevation1", "elevation2", "elevation3", "elevation4", "elevation5", "elevation6", "elevation7", "elevation8", "elevation9", "elevation10", "elevation11", "elevation12", "elevation13", "elevation14", "elevation15", "elevation16", "elevation17", "elevation18", "elevation19", "elevation20", "elevation21", "elevation22", "elevation23", "elevation24"]);
const ww = ["className", "component", "elevation", "square", "variant"], Cw = (e) => {
  const {
    square: t,
    elevation: n,
    variant: r,
    classes: o
  } = e, i = {
    root: ["root", r, !t && "rounded", r === "elevation" && `elevation${n}`]
  };
  return Ce(i, Sw, o);
}, kw = Q("div", {
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
  return w({
    backgroundColor: (e.vars || e).palette.background.paper,
    color: (e.vars || e).palette.text.primary,
    transition: e.transitions.create("box-shadow")
  }, !t.square && {
    borderRadius: e.shape.borderRadius
  }, t.variant === "outlined" && {
    border: `1px solid ${(e.vars || e).palette.divider}`
  }, t.variant === "elevation" && w({
    boxShadow: (e.vars || e).shadows[t.elevation]
  }, !e.vars && e.palette.mode === "dark" && {
    backgroundImage: `linear-gradient(${ut("#fff", vf(t.elevation))}, ${ut("#fff", vf(t.elevation))})`
  }, e.vars && {
    backgroundImage: (n = e.vars.overlays) == null ? void 0 : n[t.elevation]
  }));
}), _w = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
    props: t,
    name: "MuiPaper"
  }), {
    className: o,
    component: i = "div",
    elevation: l = 1,
    square: s = !1,
    variant: a = "elevation"
  } = r, u = L(r, ww), c = w({}, r, {
    component: i,
    elevation: l,
    square: s,
    variant: a
  }), f = Cw(c);
  return /* @__PURE__ */ x.jsx(kw, w({
    as: i,
    ownerState: c,
    className: B(f.root, o),
    ref: n
  }, u));
}), mc = _w;
function $w(e) {
  return ve("MuiAlert", e);
}
const Ew = ye("MuiAlert", ["root", "action", "icon", "message", "filled", "colorSuccess", "colorInfo", "colorWarning", "colorError", "filledSuccess", "filledInfo", "filledWarning", "filledError", "outlined", "outlinedSuccess", "outlinedInfo", "outlinedWarning", "outlinedError", "standard", "standardSuccess", "standardInfo", "standardWarning", "standardError"]), _f = Ew;
function Ga(e, t) {
  return Ga = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, r) {
    return n.__proto__ = r, n;
  }, Ga(e, t);
}
function Pw(e, t) {
  e.prototype = Object.create(t.prototype), e.prototype.constructor = e, Ga(e, t);
}
const $f = wn.createContext(null);
function Tw(e) {
  if (e === void 0)
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function hc(e, t) {
  var n = function(i) {
    return t && _.isValidElement(i) ? t(i) : i;
  }, r = /* @__PURE__ */ Object.create(null);
  return e && _.Children.map(e, function(o) {
    return o;
  }).forEach(function(o) {
    r[o.key] = n(o);
  }), r;
}
function Rw(e, t) {
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
function $n(e, t, n) {
  return n[t] != null ? n[t] : e.props[t];
}
function Mw(e, t) {
  return hc(e.children, function(n) {
    return _.cloneElement(n, {
      onExited: t.bind(null, n),
      in: !0,
      appear: $n(n, "appear", e),
      enter: $n(n, "enter", e),
      exit: $n(n, "exit", e)
    });
  });
}
function Ow(e, t, n) {
  var r = hc(e.children), o = Rw(t, r);
  return Object.keys(o).forEach(function(i) {
    var l = o[i];
    if (_.isValidElement(l)) {
      var s = i in t, a = i in r, u = t[i], c = _.isValidElement(u) && !u.props.in;
      a && (!s || c) ? o[i] = _.cloneElement(l, {
        onExited: n.bind(null, l),
        in: !0,
        exit: $n(l, "exit", e),
        enter: $n(l, "enter", e)
      }) : !a && s && !c ? o[i] = _.cloneElement(l, {
        in: !1
      }) : a && s && _.isValidElement(u) && (o[i] = _.cloneElement(l, {
        onExited: n.bind(null, l),
        in: u.props.in,
        exit: $n(l, "exit", e),
        enter: $n(l, "enter", e)
      }));
    }
  }), o;
}
var zw = Object.values || function(e) {
  return Object.keys(e).map(function(t) {
    return e[t];
  });
}, Nw = {
  component: "div",
  childFactory: function(t) {
    return t;
  }
}, gc = /* @__PURE__ */ function(e) {
  Pw(t, e);
  function t(r, o) {
    var i;
    i = e.call(this, r, o) || this;
    var l = i.handleExited.bind(Tw(i));
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
      children: a ? Mw(o, s) : Ow(o, l, s),
      firstRender: !1
    };
  }, n.handleExited = function(o, i) {
    var l = hc(this.props.children);
    o.key in l || (o.props.onExited && o.props.onExited(i), this.mounted && this.setState(function(s) {
      var a = w({}, s.children);
      return delete a[o.key], {
        children: a
      };
    }));
  }, n.render = function() {
    var o = this.props, i = o.component, l = o.childFactory, s = L(o, ["component", "childFactory"]), a = this.state.contextValue, u = zw(this.state.children).map(l);
    return delete s.appear, delete s.enter, delete s.exit, i === null ? /* @__PURE__ */ wn.createElement($f.Provider, {
      value: a
    }, u) : /* @__PURE__ */ wn.createElement($f.Provider, {
      value: a
    }, /* @__PURE__ */ wn.createElement(i, s, u));
  }, t;
}(wn.Component);
gc.propTypes = {};
gc.defaultProps = Nw;
const jw = gc;
function bw(e) {
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
  } = e, [c, f] = _.useState(!1), p = B(t, n.ripple, n.rippleVisible, r && n.ripplePulsate), v = {
    width: l,
    height: l,
    top: -(l / 2) + i,
    left: -(l / 2) + o
  }, y = B(n.child, c && n.childLeaving, r && n.childPulsate);
  return !s && !c && f(!0), _.useEffect(() => {
    if (!s && a != null) {
      const g = setTimeout(a, u);
      return () => {
        clearTimeout(g);
      };
    }
  }, [a, s, u]), /* @__PURE__ */ x.jsx("span", {
    className: p,
    style: v,
    children: /* @__PURE__ */ x.jsx("span", {
      className: y
    })
  });
}
const Aw = ye("MuiTouchRipple", ["root", "ripple", "rippleVisible", "ripplePulsate", "child", "childLeaving", "childPulsate"]), ot = Aw, Iw = ["center", "classes", "className"];
let is = (e) => e, Ef, Pf, Tf, Rf;
const Qa = 550, Lw = 80, Dw = _r(Ef || (Ef = is`
  0% {
    transform: scale(0);
    opacity: 0.1;
  }

  100% {
    transform: scale(1);
    opacity: 0.3;
  }
`)), Fw = _r(Pf || (Pf = is`
  0% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
`)), Bw = _r(Tf || (Tf = is`
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(0.92);
  }

  100% {
    transform: scale(1);
  }
`)), Ww = Q("span", {
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
}), Uw = Q(bw, {
  name: "MuiTouchRipple",
  slot: "Ripple"
})(Rf || (Rf = is`
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
`), ot.rippleVisible, Dw, Qa, ({
  theme: e
}) => e.transitions.easing.easeInOut, ot.ripplePulsate, ({
  theme: e
}) => e.transitions.duration.shorter, ot.child, ot.childLeaving, Fw, Qa, ({
  theme: e
}) => e.transitions.easing.easeInOut, ot.childPulsate, Bw, ({
  theme: e
}) => e.transitions.easing.easeInOut), Vw = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
    props: t,
    name: "MuiTouchRipple"
  }), {
    center: o = !1,
    classes: i = {},
    className: l
  } = r, s = L(r, Iw), [a, u] = _.useState([]), c = _.useRef(0), f = _.useRef(null);
  _.useEffect(() => {
    f.current && (f.current(), f.current = null);
  }, [a]);
  const p = _.useRef(!1), v = Gx(), y = _.useRef(null), g = _.useRef(null), E = _.useCallback((S) => {
    const {
      pulsate: $,
      rippleX: k,
      rippleY: C,
      rippleSize: T,
      cb: z
    } = S;
    u((M) => [...M, /* @__PURE__ */ x.jsx(Uw, {
      classes: {
        ripple: B(i.ripple, ot.ripple),
        rippleVisible: B(i.rippleVisible, ot.rippleVisible),
        ripplePulsate: B(i.ripplePulsate, ot.ripplePulsate),
        child: B(i.child, ot.child),
        childLeaving: B(i.childLeaving, ot.childLeaving),
        childPulsate: B(i.childPulsate, ot.childPulsate)
      },
      timeout: Qa,
      pulsate: $,
      rippleX: k,
      rippleY: C,
      rippleSize: T
    }, c.current)]), c.current += 1, f.current = z;
  }, [i]), m = _.useCallback((S = {}, $ = {}, k = () => {
  }) => {
    const {
      pulsate: C = !1,
      center: T = o || $.pulsate,
      fakeElement: z = !1
      // For test purposes
    } = $;
    if ((S == null ? void 0 : S.type) === "mousedown" && p.current) {
      p.current = !1;
      return;
    }
    (S == null ? void 0 : S.type) === "touchstart" && (p.current = !0);
    const M = z ? null : g.current, U = M ? M.getBoundingClientRect() : {
      width: 0,
      height: 0,
      left: 0,
      top: 0
    };
    let F, I, q;
    if (T || S === void 0 || S.clientX === 0 && S.clientY === 0 || !S.clientX && !S.touches)
      F = Math.round(U.width / 2), I = Math.round(U.height / 2);
    else {
      const {
        clientX: xe,
        clientY: Ee
      } = S.touches && S.touches.length > 0 ? S.touches[0] : S;
      F = Math.round(xe - U.left), I = Math.round(Ee - U.top);
    }
    if (T)
      q = Math.sqrt((2 * U.width ** 2 + U.height ** 2) / 3), q % 2 === 0 && (q += 1);
    else {
      const xe = Math.max(Math.abs((M ? M.clientWidth : 0) - F), F) * 2 + 2, Ee = Math.max(Math.abs((M ? M.clientHeight : 0) - I), I) * 2 + 2;
      q = Math.sqrt(xe ** 2 + Ee ** 2);
    }
    S != null && S.touches ? y.current === null && (y.current = () => {
      E({
        pulsate: C,
        rippleX: F,
        rippleY: I,
        rippleSize: q,
        cb: k
      });
    }, v.start(Lw, () => {
      y.current && (y.current(), y.current = null);
    })) : E({
      pulsate: C,
      rippleX: F,
      rippleY: I,
      rippleSize: q,
      cb: k
    });
  }, [o, E, v]), d = _.useCallback(() => {
    m({}, {
      pulsate: !0
    });
  }, [m]), h = _.useCallback((S, $) => {
    if (v.clear(), (S == null ? void 0 : S.type) === "touchend" && y.current) {
      y.current(), y.current = null, v.start(0, () => {
        h(S, $);
      });
      return;
    }
    y.current = null, u((k) => k.length > 0 ? k.slice(1) : k), f.current = $;
  }, [v]);
  return _.useImperativeHandle(n, () => ({
    pulsate: d,
    start: m,
    stop: h
  }), [d, m, h]), /* @__PURE__ */ x.jsx(Ww, w({
    className: B(ot.root, i.root, l),
    ref: g
  }, s, {
    children: /* @__PURE__ */ x.jsx(jw, {
      component: null,
      exit: !0,
      children: a
    })
  }));
}), Hw = Vw;
function Kw(e) {
  return ve("MuiButtonBase", e);
}
const Gw = ye("MuiButtonBase", ["root", "disabled", "focusVisible"]), Qw = Gw, Yw = ["action", "centerRipple", "children", "className", "component", "disabled", "disableRipple", "disableTouchRipple", "focusRipple", "focusVisibleClassName", "LinkComponent", "onBlur", "onClick", "onContextMenu", "onDragLeave", "onFocus", "onFocusVisible", "onKeyDown", "onKeyUp", "onMouseDown", "onMouseLeave", "onMouseUp", "onTouchEnd", "onTouchMove", "onTouchStart", "tabIndex", "TouchRippleProps", "touchRippleRef", "type"], Xw = (e) => {
  const {
    disabled: t,
    focusVisible: n,
    focusVisibleClassName: r,
    classes: o
  } = e, l = Ce({
    root: ["root", t && "disabled", n && "focusVisible"]
  }, Kw, o);
  return n && r && (l.root += ` ${r}`), l;
}, qw = Q("button", {
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
  [`&.${Qw.disabled}`]: {
    pointerEvents: "none",
    // Disable link interactions
    cursor: "default"
  },
  "@media print": {
    colorAdjust: "exact"
  }
}), Zw = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
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
    onContextMenu: E,
    onDragLeave: m,
    onFocus: d,
    onFocusVisible: h,
    onKeyDown: S,
    onKeyUp: $,
    onMouseDown: k,
    onMouseLeave: C,
    onMouseUp: T,
    onTouchEnd: z,
    onTouchMove: M,
    onTouchStart: U,
    tabIndex: F = 0,
    TouchRippleProps: I,
    touchRippleRef: q,
    type: xe
  } = r, Ee = L(r, Yw), Ge = _.useRef(null), R = _.useRef(null), N = nl(R, q), {
    isFocusVisibleRef: b,
    onFocus: ne,
    onBlur: pe,
    ref: bn
  } = bh(), [Ae, Qt] = _.useState(!1);
  u && Ae && Qt(!1), _.useImperativeHandle(o, () => ({
    focusVisible: () => {
      Qt(!0), Ge.current.focus();
    }
  }), []);
  const [vt, An] = _.useState(!1);
  _.useEffect(() => {
    An(!0);
  }, []);
  const o0 = vt && !c && !u;
  _.useEffect(() => {
    Ae && p && !c && vt && R.current.pulsate();
  }, [c, p, Ae, vt]);
  function bt(A, Ec, x0 = f) {
    return Kr((Pc) => (Ec && Ec(Pc), !x0 && R.current && R.current[A](Pc), !0));
  }
  const i0 = bt("start", k), l0 = bt("stop", E), s0 = bt("stop", m), a0 = bt("stop", T), u0 = bt("stop", (A) => {
    Ae && A.preventDefault(), C && C(A);
  }), c0 = bt("start", U), d0 = bt("stop", z), f0 = bt("stop", M), p0 = bt("stop", (A) => {
    pe(A), b.current === !1 && Qt(!1), y && y(A);
  }, !1), m0 = Kr((A) => {
    Ge.current || (Ge.current = A.currentTarget), ne(A), b.current === !0 && (Qt(!0), h && h(A)), d && d(A);
  }), us = () => {
    const A = Ge.current;
    return a && a !== "button" && !(A.tagName === "A" && A.href);
  }, cs = _.useRef(!1), h0 = Kr((A) => {
    p && !cs.current && Ae && R.current && A.key === " " && (cs.current = !0, R.current.stop(A, () => {
      R.current.start(A);
    })), A.target === A.currentTarget && us() && A.key === " " && A.preventDefault(), S && S(A), A.target === A.currentTarget && us() && A.key === "Enter" && !u && (A.preventDefault(), g && g(A));
  }), g0 = Kr((A) => {
    p && A.key === " " && R.current && Ae && !A.defaultPrevented && (cs.current = !1, R.current.stop(A, () => {
      R.current.pulsate(A);
    })), $ && $(A), g && A.target === A.currentTarget && us() && A.key === " " && !A.defaultPrevented && g(A);
  });
  let Wo = a;
  Wo === "button" && (Ee.href || Ee.to) && (Wo = v);
  const Rr = {};
  Wo === "button" ? (Rr.type = xe === void 0 ? "button" : xe, Rr.disabled = u) : (!Ee.href && !Ee.to && (Rr.role = "button"), u && (Rr["aria-disabled"] = u));
  const v0 = nl(n, bn, Ge), $c = w({}, r, {
    centerRipple: i,
    component: a,
    disabled: u,
    disableRipple: c,
    disableTouchRipple: f,
    focusRipple: p,
    tabIndex: F,
    focusVisible: Ae
  }), y0 = Xw($c);
  return /* @__PURE__ */ x.jsxs(qw, w({
    as: Wo,
    className: B(y0.root, s),
    ownerState: $c,
    onBlur: p0,
    onClick: g,
    onContextMenu: l0,
    onFocus: m0,
    onKeyDown: h0,
    onKeyUp: g0,
    onMouseDown: i0,
    onMouseLeave: u0,
    onMouseUp: a0,
    onDragLeave: s0,
    onTouchEnd: d0,
    onTouchMove: f0,
    onTouchStart: c0,
    ref: v0,
    tabIndex: u ? -1 : F,
    type: xe
  }, Rr, Ee, {
    children: [l, o0 ? (
      /* TouchRipple is only needed client-side, x2 boost on the server. */
      /* @__PURE__ */ x.jsx(Hw, w({
        ref: N,
        center: i
      }, I))
    ) : null]
  }));
}), vc = Zw;
function Jw(e) {
  return ve("MuiIconButton", e);
}
const eC = ye("MuiIconButton", ["root", "disabled", "colorInherit", "colorPrimary", "colorSecondary", "colorError", "colorInfo", "colorSuccess", "colorWarning", "edgeStart", "edgeEnd", "sizeSmall", "sizeMedium", "sizeLarge"]), tC = eC, nC = ["edge", "children", "className", "color", "disabled", "disableFocusRipple", "size"], rC = (e) => {
  const {
    classes: t,
    disabled: n,
    color: r,
    edge: o,
    size: i
  } = e, l = {
    root: ["root", n && "disabled", r !== "default" && `color${j(r)}`, o && `edge${j(o)}`, `size${j(i)}`]
  };
  return Ce(l, Jw, t);
}, oC = Q(vc, {
  name: "MuiIconButton",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.color !== "default" && t[`color${j(n.color)}`], n.edge && t[`edge${j(n.edge)}`], t[`size${j(n.size)}`]];
  }
})(({
  theme: e,
  ownerState: t
}) => w({
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
    backgroundColor: e.vars ? `rgba(${e.vars.palette.action.activeChannel} / ${e.vars.palette.action.hoverOpacity})` : ut(e.palette.action.active, e.palette.action.hoverOpacity),
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
  return w({}, t.color === "inherit" && {
    color: "inherit"
  }, t.color !== "inherit" && t.color !== "default" && w({
    color: r == null ? void 0 : r.main
  }, !t.disableRipple && {
    "&:hover": w({}, r && {
      backgroundColor: e.vars ? `rgba(${r.mainChannel} / ${e.vars.palette.action.hoverOpacity})` : ut(r.main, e.palette.action.hoverOpacity)
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
    [`&.${tC.disabled}`]: {
      backgroundColor: "transparent",
      color: (e.vars || e).palette.action.disabled
    }
  });
}), iC = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
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
  } = r, f = L(r, nC), p = w({}, r, {
    edge: o,
    color: s,
    disabled: a,
    disableFocusRipple: u,
    size: c
  }), v = rC(p);
  return /* @__PURE__ */ x.jsx(oC, w({
    className: B(v.root, l),
    centerRipple: !0,
    focusRipple: !u,
    disabled: a,
    ref: n
  }, f, {
    ownerState: p,
    children: i
  }));
}), lC = iC;
function sC(e) {
  return ve("MuiSvgIcon", e);
}
ye("MuiSvgIcon", ["root", "colorPrimary", "colorSecondary", "colorAction", "colorError", "colorDisabled", "fontSizeInherit", "fontSizeSmall", "fontSizeMedium", "fontSizeLarge"]);
const aC = ["children", "className", "color", "component", "fontSize", "htmlColor", "inheritViewBox", "titleAccess", "viewBox"], uC = (e) => {
  const {
    color: t,
    fontSize: n,
    classes: r
  } = e, o = {
    root: ["root", t !== "inherit" && `color${j(t)}`, `fontSize${j(n)}`]
  };
  return Ce(o, sC, r);
}, cC = Q("svg", {
  name: "MuiSvgIcon",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.color !== "inherit" && t[`color${j(n.color)}`], t[`fontSize${j(n.fontSize)}`]];
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
}), Qh = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
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
  } = r, v = L(r, aC), y = /* @__PURE__ */ _.isValidElement(o) && o.type === "svg", g = w({}, r, {
    color: l,
    component: s,
    fontSize: a,
    instanceFontSize: t.fontSize,
    inheritViewBox: c,
    viewBox: p,
    hasSvgAsChild: y
  }), E = {};
  c || (E.viewBox = p);
  const m = uC(g);
  return /* @__PURE__ */ x.jsxs(cC, w({
    as: s,
    className: B(m.root, i),
    focusable: "false",
    color: u,
    "aria-hidden": f ? void 0 : !0,
    role: f ? "img" : void 0,
    ref: n
  }, E, v, y && o.props, {
    ownerState: g,
    children: [y ? o.props.children : o, f ? /* @__PURE__ */ x.jsx("title", {
      children: f
    }) : null]
  }));
});
Qh.muiName = "SvgIcon";
const Mf = Qh;
function Pr(e, t) {
  function n(r, o) {
    return /* @__PURE__ */ x.jsx(Mf, w({
      "data-testid": `${t}Icon`,
      ref: o
    }, r, {
      children: e
    }));
  }
  return n.muiName = Mf.muiName, /* @__PURE__ */ _.memo(/* @__PURE__ */ _.forwardRef(n));
}
const dC = Pr(/* @__PURE__ */ x.jsx("path", {
  d: "M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2, 4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0, 0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"
}), "SuccessOutlined"), fC = Pr(/* @__PURE__ */ x.jsx("path", {
  d: "M12 5.99L19.53 19H4.47L12 5.99M12 2L1 21h22L12 2zm1 14h-2v2h2v-2zm0-6h-2v4h2v-4z"
}), "ReportProblemOutlined"), pC = Pr(/* @__PURE__ */ x.jsx("path", {
  d: "M11 15h2v2h-2zm0-8h2v6h-2zm.99-5C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"
}), "ErrorOutline"), mC = Pr(/* @__PURE__ */ x.jsx("path", {
  d: "M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"
}), "InfoOutlined"), hC = Pr(/* @__PURE__ */ x.jsx("path", {
  d: "M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
}), "Close"), gC = ["action", "children", "className", "closeText", "color", "components", "componentsProps", "icon", "iconMapping", "onClose", "role", "severity", "slotProps", "slots", "variant"], vC = (e) => {
  const {
    variant: t,
    color: n,
    severity: r,
    classes: o
  } = e, i = {
    root: ["root", `color${j(n || r)}`, `${t}${j(n || r)}`, `${t}`],
    icon: ["icon"],
    message: ["message"],
    action: ["action"]
  };
  return Ce(i, $w, o);
}, yC = Q(mc, {
  name: "MuiAlert",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[n.variant], t[`${n.variant}${j(n.color || n.severity)}`]];
  }
})(({
  theme: e
}) => {
  const t = e.palette.mode === "light" ? rl : ol, n = e.palette.mode === "light" ? ol : rl;
  return w({}, e.typography.body2, {
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
        [`& .${_f.icon}`]: e.vars ? {
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
        [`& .${_f.icon}`]: e.vars ? {
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
      style: w({
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
}), xC = Q("div", {
  name: "MuiAlert",
  slot: "Icon",
  overridesResolver: (e, t) => t.icon
})({
  marginRight: 12,
  padding: "7px 0",
  display: "flex",
  fontSize: 22,
  opacity: 0.9
}), SC = Q("div", {
  name: "MuiAlert",
  slot: "Message",
  overridesResolver: (e, t) => t.message
})({
  padding: "8px 0",
  minWidth: 0,
  overflow: "auto"
}), Of = Q("div", {
  name: "MuiAlert",
  slot: "Action",
  overridesResolver: (e, t) => t.action
})({
  display: "flex",
  alignItems: "flex-start",
  padding: "4px 0 0 16px",
  marginLeft: "auto",
  marginRight: -8
}), zf = {
  success: /* @__PURE__ */ x.jsx(dC, {
    fontSize: "inherit"
  }),
  warning: /* @__PURE__ */ x.jsx(fC, {
    fontSize: "inherit"
  }),
  error: /* @__PURE__ */ x.jsx(pC, {
    fontSize: "inherit"
  }),
  info: /* @__PURE__ */ x.jsx(mC, {
    fontSize: "inherit"
  })
}, wC = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
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
    iconMapping: p = zf,
    onClose: v,
    role: y = "alert",
    severity: g = "success",
    slotProps: E = {},
    slots: m = {},
    variant: d = "standard"
  } = r, h = L(r, gC), S = w({}, r, {
    color: a,
    severity: g,
    variant: d,
    colorSeverity: a || g
  }), $ = vC(S), k = {
    slots: w({
      closeButton: u.CloseButton,
      closeIcon: u.CloseIcon
    }, m),
    slotProps: w({}, c, E)
  }, [C, T] = kf("closeButton", {
    elementType: lC,
    externalForwardedProps: k,
    ownerState: S
  }), [z, M] = kf("closeIcon", {
    elementType: hC,
    externalForwardedProps: k,
    ownerState: S
  });
  return /* @__PURE__ */ x.jsxs(yC, w({
    role: y,
    elevation: 0,
    ownerState: S,
    className: B($.root, l),
    ref: n
  }, h, {
    children: [f !== !1 ? /* @__PURE__ */ x.jsx(xC, {
      ownerState: S,
      className: $.icon,
      children: f || p[g] || zf[g]
    }) : null, /* @__PURE__ */ x.jsx(SC, {
      ownerState: S,
      className: $.message,
      children: i
    }), o != null ? /* @__PURE__ */ x.jsx(Of, {
      ownerState: S,
      className: $.action,
      children: o
    }) : null, o == null && v ? /* @__PURE__ */ x.jsx(Of, {
      ownerState: S,
      className: $.action,
      children: /* @__PURE__ */ x.jsx(C, w({
        size: "small",
        "aria-label": s,
        title: s,
        color: "inherit",
        onClick: v
      }, T, {
        children: /* @__PURE__ */ x.jsx(z, w({
          fontSize: "small"
        }, M))
      }))
    }) : null]
  }));
}), CC = wC, kC = ye("MuiBox", ["root"]), _C = kC, $C = fc(), EC = fx({
  themeId: vr,
  defaultTheme: $C,
  defaultClassName: _C.root,
  generateClassName: ic.generate
}), Po = EC, PC = /* @__PURE__ */ _.createContext(), Nf = PC;
function TC(e) {
  return ve("MuiGrid", e);
}
const RC = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], MC = ["column-reverse", "column", "row-reverse", "row"], OC = ["nowrap", "wrap-reverse", "wrap"], Fr = ["auto", !0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], zC = ye("MuiGrid", [
  "root",
  "container",
  "item",
  "zeroMinWidth",
  // spacings
  ...RC.map((e) => `spacing-xs-${e}`),
  // direction values
  ...MC.map((e) => `direction-xs-${e}`),
  // wrap values
  ...OC.map((e) => `wrap-xs-${e}`),
  // grid sizes for all breakpoints
  ...Fr.map((e) => `grid-xs-${e}`),
  ...Fr.map((e) => `grid-sm-${e}`),
  ...Fr.map((e) => `grid-md-${e}`),
  ...Fr.map((e) => `grid-lg-${e}`),
  ...Fr.map((e) => `grid-xl-${e}`)
]), To = zC, NC = ["className", "columns", "columnSpacing", "component", "container", "direction", "item", "rowSpacing", "spacing", "wrap", "zeroMinWidth"];
function ur(e) {
  const t = parseFloat(e);
  return `${t}${String(e).replace(String(t), "") || "px"}`;
}
function jC({
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
      const l = Il({
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
          const f = `calc(${a} + ${ur(c)})`;
          u = {
            flexBasis: f,
            maxWidth: f
          };
        }
      }
      i = w({
        flexBasis: a,
        flexGrow: 0,
        maxWidth: a
      }, u);
    }
    return e.breakpoints.values[o] === 0 ? Object.assign(r, i) : r[e.breakpoints.up(o)] = i, r;
  }, {});
}
function bC({
  theme: e,
  ownerState: t
}) {
  const n = Il({
    values: t.direction,
    breakpoints: e.breakpoints.values
  });
  return pt({
    theme: e
  }, n, (r) => {
    const o = {
      flexDirection: r
    };
    return r.indexOf("column") === 0 && (o[`& > .${To.item}`] = {
      maxWidth: "none"
    }), o;
  });
}
function Yh({
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
function AC({
  theme: e,
  ownerState: t
}) {
  const {
    container: n,
    rowSpacing: r
  } = t;
  let o = {};
  if (n && r !== 0) {
    const i = Il({
      values: r,
      breakpoints: e.breakpoints.values
    });
    let l;
    typeof i == "object" && (l = Yh({
      breakpoints: e.breakpoints.values,
      values: i
    })), o = pt({
      theme: e
    }, i, (s, a) => {
      var u;
      const c = e.spacing(s);
      return c !== "0px" ? {
        marginTop: `-${ur(c)}`,
        [`& > .${To.item}`]: {
          paddingTop: ur(c)
        }
      } : (u = l) != null && u.includes(a) ? {} : {
        marginTop: 0,
        [`& > .${To.item}`]: {
          paddingTop: 0
        }
      };
    });
  }
  return o;
}
function IC({
  theme: e,
  ownerState: t
}) {
  const {
    container: n,
    columnSpacing: r
  } = t;
  let o = {};
  if (n && r !== 0) {
    const i = Il({
      values: r,
      breakpoints: e.breakpoints.values
    });
    let l;
    typeof i == "object" && (l = Yh({
      breakpoints: e.breakpoints.values,
      values: i
    })), o = pt({
      theme: e
    }, i, (s, a) => {
      var u;
      const c = e.spacing(s);
      return c !== "0px" ? {
        width: `calc(100% + ${ur(c)})`,
        marginLeft: `-${ur(c)}`,
        [`& > .${To.item}`]: {
          paddingLeft: ur(c)
        }
      } : (u = l) != null && u.includes(a) ? {} : {
        width: "100%",
        marginLeft: 0,
        [`& > .${To.item}`]: {
          paddingLeft: 0
        }
      };
    });
  }
  return o;
}
function LC(e, t, n = {}) {
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
const DC = Q("div", {
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
    r && (c = LC(l, u, t));
    const f = [];
    return u.forEach((p) => {
      const v = n[p];
      v && f.push(t[`grid-${p}-${String(v)}`]);
    }), [t.root, r && t.container, i && t.item, a && t.zeroMinWidth, ...c, o !== "row" && t[`direction-xs-${String(o)}`], s !== "wrap" && t[`wrap-xs-${String(s)}`], ...f];
  }
})(({
  ownerState: e
}) => w({
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
}), bC, AC, IC, jC);
function FC(e, t) {
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
const BC = (e) => {
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
  n && (u = FC(i, a));
  const c = [];
  a.forEach((p) => {
    const v = e[p];
    v && c.push(`grid-${p}-${String(v)}`);
  });
  const f = {
    root: ["root", n && "container", o && "item", s && "zeroMinWidth", ...u, r !== "row" && `direction-xs-${String(r)}`, l !== "wrap" && `wrap-xs-${String(l)}`, ...c]
  };
  return Ce(f, TC, t);
}, WC = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
    props: t,
    name: "MuiGrid"
  }), {
    breakpoints: o
  } = x2(), i = Hl(r), {
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
    zeroMinWidth: E = !1
  } = i, m = L(i, NC), d = v || y, h = a || y, S = _.useContext(Nf), $ = c ? s || 12 : S, k = {}, C = w({}, m);
  o.keys.forEach((M) => {
    m[M] != null && (k[M] = m[M], delete C[M]);
  });
  const T = w({}, i, {
    columns: $,
    container: c,
    direction: f,
    item: p,
    rowSpacing: d,
    columnSpacing: h,
    wrap: g,
    zeroMinWidth: E,
    spacing: y
  }, k, {
    breakpoints: o.keys
  }), z = BC(T);
  return /* @__PURE__ */ x.jsx(Nf.Provider, {
    value: $,
    children: /* @__PURE__ */ x.jsx(DC, w({
      ownerState: T,
      className: B(z.root, l),
      as: u,
      ref: n
    }, C))
  });
}), Et = WC;
function UC(e) {
  return ve("MuiCard", e);
}
ye("MuiCard", ["root"]);
const VC = ["className", "raised"], HC = (e) => {
  const {
    classes: t
  } = e;
  return Ce({
    root: ["root"]
  }, UC, t);
}, KC = Q(mc, {
  name: "MuiCard",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})(() => ({
  overflow: "hidden"
})), GC = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
    props: t,
    name: "MuiCard"
  }), {
    className: o,
    raised: i = !1
  } = r, l = L(r, VC), s = w({}, r, {
    raised: i
  }), a = HC(s);
  return /* @__PURE__ */ x.jsx(KC, w({
    className: B(a.root, o),
    elevation: i ? 8 : void 0,
    ref: n,
    ownerState: s
  }, l));
}), ls = GC;
function QC(e) {
  return ve("MuiCardActionArea", e);
}
const YC = ye("MuiCardActionArea", ["root", "focusVisible", "focusHighlight"]), Hs = YC, XC = ["children", "className", "focusVisibleClassName"], qC = (e) => {
  const {
    classes: t
  } = e;
  return Ce({
    root: ["root"],
    focusHighlight: ["focusHighlight"]
  }, QC, t);
}, ZC = Q(vc, {
  name: "MuiCardActionArea",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})(({
  theme: e
}) => ({
  display: "block",
  textAlign: "inherit",
  borderRadius: "inherit",
  // for Safari to work https://github.com/mui/material-ui/issues/36285.
  width: "100%",
  [`&:hover .${Hs.focusHighlight}`]: {
    opacity: (e.vars || e).palette.action.hoverOpacity,
    "@media (hover: none)": {
      opacity: 0
    }
  },
  [`&.${Hs.focusVisible} .${Hs.focusHighlight}`]: {
    opacity: (e.vars || e).palette.action.focusOpacity
  }
})), JC = Q("span", {
  name: "MuiCardActionArea",
  slot: "FocusHighlight",
  overridesResolver: (e, t) => t.focusHighlight
})(({
  theme: e
}) => ({
  overflow: "hidden",
  pointerEvents: "none",
  position: "absolute",
  top: 0,
  right: 0,
  bottom: 0,
  left: 0,
  borderRadius: "inherit",
  opacity: 0,
  backgroundColor: "currentcolor",
  transition: e.transitions.create("opacity", {
    duration: e.transitions.duration.short
  })
})), ek = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
    props: t,
    name: "MuiCardActionArea"
  }), {
    children: o,
    className: i,
    focusVisibleClassName: l
  } = r, s = L(r, XC), a = r, u = qC(a);
  return /* @__PURE__ */ x.jsxs(ZC, w({
    className: B(u.root, i),
    focusVisibleClassName: B(l, u.focusVisible),
    ref: n,
    ownerState: a
  }, s, {
    children: [o, /* @__PURE__ */ x.jsx(JC, {
      className: u.focusHighlight,
      ownerState: a
    })]
  }));
}), tk = ek;
function nk(e) {
  return ve("MuiCardContent", e);
}
ye("MuiCardContent", ["root"]);
const rk = ["className", "component"], ok = (e) => {
  const {
    classes: t
  } = e;
  return Ce({
    root: ["root"]
  }, nk, t);
}, ik = Q("div", {
  name: "MuiCardContent",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})(() => ({
  padding: 16,
  "&:last-child": {
    paddingBottom: 24
  }
})), lk = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
    props: t,
    name: "MuiCardContent"
  }), {
    className: o,
    component: i = "div"
  } = r, l = L(r, rk), s = w({}, r, {
    component: i
  }), a = ok(s);
  return /* @__PURE__ */ x.jsx(ik, w({
    as: i,
    className: B(a.root, o),
    ownerState: s,
    ref: n
  }, l));
}), ss = lk;
var yc = {}, Ks = {};
const sk = {
  configure: (e) => {
    ic.configure(e);
  }
}, ak = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  capitalize: j,
  createChainedFunction: bx,
  createSvgIcon: Pr,
  debounce: Ax,
  deprecatedPropType: Ix,
  isMuiElement: Lx,
  ownerDocument: zh,
  ownerWindow: Dx,
  requirePropFactory: Fx,
  setRef: Nh,
  unstable_ClassNameGenerator: sk,
  unstable_useEnhancedEffect: ac,
  unstable_useId: jh,
  unsupportedProp: Wx,
  useControlled: Ux,
  useEventCallback: Kr,
  useForkRef: nl,
  useIsFocusVisible: bh
}, Symbol.toStringTag, { value: "Module" })), uk = /* @__PURE__ */ Kt(ak);
var jf;
function Tr() {
  return jf || (jf = 1, function(e) {
    "use client";
    Object.defineProperty(e, "__esModule", {
      value: !0
    }), Object.defineProperty(e, "default", {
      enumerable: !0,
      get: function() {
        return t.createSvgIcon;
      }
    });
    var t = uk;
  }(Ks)), Ks;
}
var ck = yn;
Object.defineProperty(yc, "__esModule", {
  value: !0
});
var Xh = yc.default = void 0, dk = ck(Tr()), fk = x;
Xh = yc.default = (0, dk.default)(/* @__PURE__ */ (0, fk.jsx)("path", {
  d: "M4 6h18V4H4c-1.1 0-2 .9-2 2v11H0v3h14v-3H4zm19 2h-6c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h6c.55 0 1-.45 1-1V9c0-.55-.45-1-1-1m-1 9h-4v-7h4z"
}), "Devices");
var xc = {}, pk = yn;
Object.defineProperty(xc, "__esModule", {
  value: !0
});
var qh = xc.default = void 0, mk = pk(Tr()), hk = x;
qh = xc.default = (0, mk.default)(/* @__PURE__ */ (0, hk.jsx)("path", {
  d: "m1 9 2 2c4.97-4.97 13.03-4.97 18 0l2-2C16.93 2.93 7.08 2.93 1 9m8 8 3 3 3-3c-1.65-1.66-4.34-1.66-6 0m-4-4 2 2c2.76-2.76 7.24-2.76 10 0l2-2C15.14 9.14 8.87 9.14 5 13"
}), "Wifi");
var Sc = {}, gk = yn;
Object.defineProperty(Sc, "__esModule", {
  value: !0
});
var Zh = Sc.default = void 0, vk = gk(Tr()), yk = x;
Zh = Sc.default = (0, vk.default)(/* @__PURE__ */ (0, yk.jsx)("path", {
  d: "m20.2 5.9.8-.8C19.6 3.7 17.8 3 16 3s-3.6.7-5 2.1l.8.8C13 4.8 14.5 4.2 16 4.2s3 .6 4.2 1.7m-.9.8c-.9-.9-2.1-1.4-3.3-1.4s-2.4.5-3.3 1.4l.8.8c.7-.7 1.6-1 2.5-1 .9 0 1.8.3 2.5 1zM19 13h-2V9h-2v4H5c-1.1 0-2 .9-2 2v4c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-4c0-1.1-.9-2-2-2M8 18H6v-2h2zm3.5 0h-2v-2h2zm3.5 0h-2v-2h2z"
}), "Router");
var wc = {}, xk = yn;
Object.defineProperty(wc, "__esModule", {
  value: !0
});
var Jh = wc.default = void 0, Sk = xk(Tr()), wk = x;
Jh = wc.default = (0, Sk.default)(/* @__PURE__ */ (0, wk.jsx)("path", {
  d: "M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11z"
}), "Videocam");
var Cc = {}, Ck = yn;
Object.defineProperty(Cc, "__esModule", {
  value: !0
});
var e0 = Cc.default = void 0, kk = Ck(Tr()), _k = x;
e0 = Cc.default = (0, kk.default)(/* @__PURE__ */ (0, _k.jsx)("path", {
  d: "M12 11c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m6 2c0-3.31-2.69-6-6-6s-6 2.69-6 6c0 2.22 1.21 4.15 3 5.19l1-1.74c-1.19-.7-2-1.97-2-3.45 0-2.21 1.79-4 4-4s4 1.79 4 4c0 1.48-.81 2.75-2 3.45l1 1.74c1.79-1.04 3-2.97 3-5.19M12 3C6.48 3 2 7.48 2 13c0 3.7 2.01 6.92 4.99 8.65l1-1.73C5.61 18.53 4 15.96 4 13c0-4.42 3.58-8 8-8s8 3.58 8 8c0 2.96-1.61 5.53-4 6.92l1 1.73c2.99-1.73 5-4.95 5-8.65 0-5.52-4.48-10-10-10"
}), "WifiTethering");
const Br = ({ title: e, value: t, icon: n }) => /* @__PURE__ */ x.jsx(ls, { children: /* @__PURE__ */ x.jsx(ss, { children: /* @__PURE__ */ x.jsxs(Po, { sx: { display: "flex", alignItems: "center" }, children: [
  /* @__PURE__ */ x.jsx(Po, { sx: { fontSize: "2rem", mr: 2 }, children: n }),
  /* @__PURE__ */ x.jsxs("div", { children: [
    /* @__PURE__ */ x.jsx(me, { color: "text.secondary", children: e }),
    /* @__PURE__ */ x.jsx(me, { variant: "h5", component: "div", children: t })
  ] })
] }) }) }), $k = /* @__PURE__ */ _.createContext(), t0 = $k;
function Ek(e) {
  return ve("MuiTable", e);
}
ye("MuiTable", ["root", "stickyHeader"]);
const Pk = ["className", "component", "padding", "size", "stickyHeader"], Tk = (e) => {
  const {
    classes: t,
    stickyHeader: n
  } = e;
  return Ce({
    root: ["root", n && "stickyHeader"]
  }, Ek, t);
}, Rk = Q("table", {
  name: "MuiTable",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.stickyHeader && t.stickyHeader];
  }
})(({
  theme: e,
  ownerState: t
}) => w({
  display: "table",
  width: "100%",
  borderCollapse: "collapse",
  borderSpacing: 0,
  "& caption": w({}, e.typography.body2, {
    padding: e.spacing(2),
    color: (e.vars || e).palette.text.secondary,
    textAlign: "left",
    captionSide: "bottom"
  })
}, t.stickyHeader && {
  borderCollapse: "separate"
})), bf = "table", Mk = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
    props: t,
    name: "MuiTable"
  }), {
    className: o,
    component: i = bf,
    padding: l = "normal",
    size: s = "medium",
    stickyHeader: a = !1
  } = r, u = L(r, Pk), c = w({}, r, {
    component: i,
    padding: l,
    size: s,
    stickyHeader: a
  }), f = Tk(c), p = _.useMemo(() => ({
    padding: l,
    size: s,
    stickyHeader: a
  }), [l, s, a]);
  return /* @__PURE__ */ x.jsx(t0.Provider, {
    value: p,
    children: /* @__PURE__ */ x.jsx(Rk, w({
      as: i,
      role: i === bf ? null : "table",
      ref: n,
      className: B(f.root, o),
      ownerState: c
    }, u))
  });
}), Ok = Mk, zk = /* @__PURE__ */ _.createContext(), as = zk;
function Nk(e) {
  return ve("MuiTableBody", e);
}
ye("MuiTableBody", ["root"]);
const jk = ["className", "component"], bk = (e) => {
  const {
    classes: t
  } = e;
  return Ce({
    root: ["root"]
  }, Nk, t);
}, Ak = Q("tbody", {
  name: "MuiTableBody",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})({
  display: "table-row-group"
}), Ik = {
  variant: "body"
}, Af = "tbody", Lk = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
    props: t,
    name: "MuiTableBody"
  }), {
    className: o,
    component: i = Af
  } = r, l = L(r, jk), s = w({}, r, {
    component: i
  }), a = bk(s);
  return /* @__PURE__ */ x.jsx(as.Provider, {
    value: Ik,
    children: /* @__PURE__ */ x.jsx(Ak, w({
      className: B(a.root, o),
      as: i,
      ref: n,
      role: i === Af ? null : "rowgroup",
      ownerState: s
    }, l))
  });
}), Dk = Lk;
function Fk(e) {
  return ve("MuiTableCell", e);
}
const Bk = ye("MuiTableCell", ["root", "head", "body", "footer", "sizeSmall", "sizeMedium", "paddingCheckbox", "paddingNone", "alignLeft", "alignCenter", "alignRight", "alignJustify", "stickyHeader"]), Wk = Bk, Uk = ["align", "className", "component", "padding", "scope", "size", "sortDirection", "variant"], Vk = (e) => {
  const {
    classes: t,
    variant: n,
    align: r,
    padding: o,
    size: i,
    stickyHeader: l
  } = e, s = {
    root: ["root", n, l && "stickyHeader", r !== "inherit" && `align${j(r)}`, o !== "normal" && `padding${j(o)}`, `size${j(i)}`]
  };
  return Ce(s, Fk, t);
}, Hk = Q("td", {
  name: "MuiTableCell",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[n.variant], t[`size${j(n.size)}`], n.padding !== "normal" && t[`padding${j(n.padding)}`], n.align !== "inherit" && t[`align${j(n.align)}`], n.stickyHeader && t.stickyHeader];
  }
})(({
  theme: e,
  ownerState: t
}) => w({}, e.typography.body2, {
  display: "table-cell",
  verticalAlign: "inherit",
  // Workaround for a rendering bug with spanned columns in Chrome 62.0.
  // Removes the alpha (sets it to 1), and lightens or darkens the theme color.
  borderBottom: e.vars ? `1px solid ${e.vars.palette.TableCell.border}` : `1px solid
    ${e.palette.mode === "light" ? ol(ut(e.palette.divider, 1), 0.88) : rl(ut(e.palette.divider, 1), 0.68)}`,
  textAlign: "left",
  padding: 16
}, t.variant === "head" && {
  color: (e.vars || e).palette.text.primary,
  lineHeight: e.typography.pxToRem(24),
  fontWeight: e.typography.fontWeightMedium
}, t.variant === "body" && {
  color: (e.vars || e).palette.text.primary
}, t.variant === "footer" && {
  color: (e.vars || e).palette.text.secondary,
  lineHeight: e.typography.pxToRem(21),
  fontSize: e.typography.pxToRem(12)
}, t.size === "small" && {
  padding: "6px 16px",
  [`&.${Wk.paddingCheckbox}`]: {
    width: 24,
    // prevent the checkbox column from growing
    padding: "0 12px 0 16px",
    "& > *": {
      padding: 0
    }
  }
}, t.padding === "checkbox" && {
  width: 48,
  // prevent the checkbox column from growing
  padding: "0 0 0 4px"
}, t.padding === "none" && {
  padding: 0
}, t.align === "left" && {
  textAlign: "left"
}, t.align === "center" && {
  textAlign: "center"
}, t.align === "right" && {
  textAlign: "right",
  flexDirection: "row-reverse"
}, t.align === "justify" && {
  textAlign: "justify"
}, t.stickyHeader && {
  position: "sticky",
  top: 0,
  zIndex: 2,
  backgroundColor: (e.vars || e).palette.background.default
})), Kk = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
    props: t,
    name: "MuiTableCell"
  }), {
    align: o = "inherit",
    className: i,
    component: l,
    padding: s,
    scope: a,
    size: u,
    sortDirection: c,
    variant: f
  } = r, p = L(r, Uk), v = _.useContext(t0), y = _.useContext(as), g = y && y.variant === "head";
  let E;
  l ? E = l : E = g ? "th" : "td";
  let m = a;
  E === "td" ? m = void 0 : !m && g && (m = "col");
  const d = f || y && y.variant, h = w({}, r, {
    align: o,
    component: E,
    padding: s || (v && v.padding ? v.padding : "normal"),
    size: u || (v && v.size ? v.size : "medium"),
    sortDirection: c,
    stickyHeader: d === "head" && v && v.stickyHeader,
    variant: d
  }), S = Vk(h);
  let $ = null;
  return c && ($ = c === "asc" ? "ascending" : "descending"), /* @__PURE__ */ x.jsx(Hk, w({
    as: E,
    ref: n,
    className: B(S.root, i),
    "aria-sort": $,
    scope: m,
    ownerState: h
  }, p));
}), qt = Kk;
function Gk(e) {
  return ve("MuiTableContainer", e);
}
ye("MuiTableContainer", ["root"]);
const Qk = ["className", "component"], Yk = (e) => {
  const {
    classes: t
  } = e;
  return Ce({
    root: ["root"]
  }, Gk, t);
}, Xk = Q("div", {
  name: "MuiTableContainer",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})({
  width: "100%",
  overflowX: "auto"
}), qk = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
    props: t,
    name: "MuiTableContainer"
  }), {
    className: o,
    component: i = "div"
  } = r, l = L(r, Qk), s = w({}, r, {
    component: i
  }), a = Yk(s);
  return /* @__PURE__ */ x.jsx(Xk, w({
    ref: n,
    as: i,
    className: B(a.root, o),
    ownerState: s
  }, l));
}), Zk = qk;
function Jk(e) {
  return ve("MuiTableHead", e);
}
ye("MuiTableHead", ["root"]);
const e_ = ["className", "component"], t_ = (e) => {
  const {
    classes: t
  } = e;
  return Ce({
    root: ["root"]
  }, Jk, t);
}, n_ = Q("thead", {
  name: "MuiTableHead",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})({
  display: "table-header-group"
}), r_ = {
  variant: "head"
}, If = "thead", o_ = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
    props: t,
    name: "MuiTableHead"
  }), {
    className: o,
    component: i = If
  } = r, l = L(r, e_), s = w({}, r, {
    component: i
  }), a = t_(s);
  return /* @__PURE__ */ x.jsx(as.Provider, {
    value: r_,
    children: /* @__PURE__ */ x.jsx(n_, w({
      as: i,
      className: B(a.root, o),
      ref: n,
      role: i === If ? null : "rowgroup",
      ownerState: s
    }, l))
  });
}), i_ = o_;
function l_(e) {
  return ve("MuiTableRow", e);
}
const s_ = ye("MuiTableRow", ["root", "selected", "hover", "head", "footer"]), Lf = s_, a_ = ["className", "component", "hover", "selected"], u_ = (e) => {
  const {
    classes: t,
    selected: n,
    hover: r,
    head: o,
    footer: i
  } = e;
  return Ce({
    root: ["root", n && "selected", r && "hover", o && "head", i && "footer"]
  }, l_, t);
}, c_ = Q("tr", {
  name: "MuiTableRow",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.head && t.head, n.footer && t.footer];
  }
})(({
  theme: e
}) => ({
  color: "inherit",
  display: "table-row",
  verticalAlign: "middle",
  // We disable the focus ring for mouse, touch and keyboard users.
  outline: 0,
  [`&.${Lf.hover}:hover`]: {
    backgroundColor: (e.vars || e).palette.action.hover
  },
  [`&.${Lf.selected}`]: {
    backgroundColor: e.vars ? `rgba(${e.vars.palette.primary.mainChannel} / ${e.vars.palette.action.selectedOpacity})` : ut(e.palette.primary.main, e.palette.action.selectedOpacity),
    "&:hover": {
      backgroundColor: e.vars ? `rgba(${e.vars.palette.primary.mainChannel} / calc(${e.vars.palette.action.selectedOpacity} + ${e.vars.palette.action.hoverOpacity}))` : ut(e.palette.primary.main, e.palette.action.selectedOpacity + e.palette.action.hoverOpacity)
    }
  }
})), Df = "tr", d_ = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = fe({
    props: t,
    name: "MuiTableRow"
  }), {
    className: o,
    component: i = Df,
    hover: l = !1,
    selected: s = !1
  } = r, a = L(r, a_), u = _.useContext(as), c = w({}, r, {
    component: i,
    hover: l,
    selected: s,
    head: u && u.variant === "head",
    footer: u && u.variant === "footer"
  }), f = u_(c);
  return /* @__PURE__ */ x.jsx(c_, w({
    as: i,
    ref: n,
    className: B(f.root, o),
    role: i === Df ? null : "row",
    ownerState: c
  }, a));
}), Ff = d_, f_ = ({ devices: e, setActiveView: t }) => /* @__PURE__ */ x.jsx(Zk, { component: mc, children: /* @__PURE__ */ x.jsxs(Ok, { sx: { minWidth: 650 }, "aria-label": "simple table", children: [
  /* @__PURE__ */ x.jsx(i_, { children: /* @__PURE__ */ x.jsxs(Ff, { children: [
    /* @__PURE__ */ x.jsx(qt, { children: "Name" }),
    /* @__PURE__ */ x.jsx(qt, { children: "Status" }),
    /* @__PURE__ */ x.jsx(qt, { children: "Model" }),
    /* @__PURE__ */ x.jsx(qt, { children: "MAC Address" })
  ] }) }),
  /* @__PURE__ */ x.jsx(Dk, { children: e.map((n) => /* @__PURE__ */ x.jsxs(
    Ff,
    {
      onClick: () => t({ view: "device", deviceId: n.serial }),
      sx: { cursor: "pointer", "&:hover": { backgroundColor: "action.hover" } },
      children: [
        /* @__PURE__ */ x.jsx(qt, { component: "th", scope: "row", children: n.name || n.mac }),
        /* @__PURE__ */ x.jsx(qt, { children: n.status }),
        /* @__PURE__ */ x.jsx(qt, { children: n.model }),
        /* @__PURE__ */ x.jsx(qt, { children: n.mac })
      ]
    },
    n.serial
  )) })
] }) }), p_ = ({ setActiveView: e, data: t }) => {
  if (!t)
    return /* @__PURE__ */ x.jsx(me, { children: "Loading dashboard..." });
  const { devices: n = [], ssids: r = [], networks: o = [] } = t, i = {
    totalDevices: n.length,
    wirelessAps: n.filter((l) => {
      var s;
      return (s = l.model) == null ? void 0 : s.startsWith("MR");
    }).length,
    switches: n.filter((l) => {
      var s;
      return (s = l.model) == null ? void 0 : s.startsWith("MS");
    }).length,
    cameras: n.filter((l) => {
      var s;
      return (s = l.model) == null ? void 0 : s.startsWith("MV");
    }).length,
    ssids: r.length
  };
  return /* @__PURE__ */ x.jsxs(Et, { container: !0, spacing: 3, children: [
    /* @__PURE__ */ x.jsx(Et, { item: !0, xs: 12, sm: 6, md: 2.4, children: /* @__PURE__ */ x.jsx(Br, { title: "Total Devices", value: i.totalDevices, icon: /* @__PURE__ */ x.jsx(Xh, {}) }) }),
    /* @__PURE__ */ x.jsx(Et, { item: !0, xs: 12, sm: 6, md: 2.4, children: /* @__PURE__ */ x.jsx(Br, { title: "Wireless APs", value: i.wirelessAps, icon: /* @__PURE__ */ x.jsx(qh, {}) }) }),
    /* @__PURE__ */ x.jsx(Et, { item: !0, xs: 12, sm: 6, md: 2.4, children: /* @__PURE__ */ x.jsx(Br, { title: "Switches", value: i.switches, icon: /* @__PURE__ */ x.jsx(Zh, {}) }) }),
    /* @__PURE__ */ x.jsx(Et, { item: !0, xs: 12, sm: 6, md: 2.4, children: /* @__PURE__ */ x.jsx(Br, { title: "Cameras", value: i.cameras, icon: /* @__PURE__ */ x.jsx(Jh, {}) }) }),
    /* @__PURE__ */ x.jsx(Et, { item: !0, xs: 12, sm: 6, md: 2.4, children: /* @__PURE__ */ x.jsx(Br, { title: "Virtual SSIDs", value: i.ssids, icon: /* @__PURE__ */ x.jsx(e0, {}) }) }),
    /* @__PURE__ */ x.jsxs(Et, { item: !0, xs: 12, children: [
      /* @__PURE__ */ x.jsx(me, { variant: "h6", gutterBottom: !0, children: "Networks" }),
      /* @__PURE__ */ x.jsx(Et, { container: !0, spacing: 2, children: o.map((l) => /* @__PURE__ */ x.jsx(Et, { item: !0, xs: 12, sm: 6, md: 4, children: /* @__PURE__ */ x.jsx(ls, { children: /* @__PURE__ */ x.jsx(tk, { onClick: () => e({ view: "network", networkId: l.id }), children: /* @__PURE__ */ x.jsx(ss, { children: /* @__PURE__ */ x.jsx(me, { gutterBottom: !0, variant: "h5", component: "div", children: l.name }) }) }) }) }, l.id)) })
    ] }),
    /* @__PURE__ */ x.jsxs(Et, { item: !0, xs: 12, children: [
      /* @__PURE__ */ x.jsx(me, { variant: "h6", gutterBottom: !0, sx: { mt: 4 }, children: "All Devices" }),
      /* @__PURE__ */ x.jsx(f_, { devices: n, setActiveView: e })
    ] })
  ] });
};
function m_(e) {
  return ve("MuiButton", e);
}
const h_ = ye("MuiButton", ["root", "text", "textInherit", "textPrimary", "textSecondary", "textSuccess", "textError", "textInfo", "textWarning", "outlined", "outlinedInherit", "outlinedPrimary", "outlinedSecondary", "outlinedSuccess", "outlinedError", "outlinedInfo", "outlinedWarning", "contained", "containedInherit", "containedPrimary", "containedSecondary", "containedSuccess", "containedError", "containedInfo", "containedWarning", "disableElevation", "focusVisible", "disabled", "colorInherit", "colorPrimary", "colorSecondary", "colorSuccess", "colorError", "colorInfo", "colorWarning", "textSizeSmall", "textSizeMedium", "textSizeLarge", "outlinedSizeSmall", "outlinedSizeMedium", "outlinedSizeLarge", "containedSizeSmall", "containedSizeMedium", "containedSizeLarge", "sizeMedium", "sizeSmall", "sizeLarge", "fullWidth", "startIcon", "endIcon", "icon", "iconSizeSmall", "iconSizeMedium", "iconSizeLarge"]), ci = h_, g_ = /* @__PURE__ */ _.createContext({}), v_ = g_, y_ = /* @__PURE__ */ _.createContext(void 0), x_ = y_, S_ = ["children", "color", "component", "className", "disabled", "disableElevation", "disableFocusRipple", "endIcon", "focusVisibleClassName", "fullWidth", "size", "startIcon", "type", "variant"], w_ = (e) => {
  const {
    color: t,
    disableElevation: n,
    fullWidth: r,
    size: o,
    variant: i,
    classes: l
  } = e, s = {
    root: ["root", i, `${i}${j(t)}`, `size${j(o)}`, `${i}Size${j(o)}`, `color${j(t)}`, n && "disableElevation", r && "fullWidth"],
    label: ["label"],
    startIcon: ["icon", "startIcon", `iconSize${j(o)}`],
    endIcon: ["icon", "endIcon", `iconSize${j(o)}`]
  }, a = Ce(s, m_, l);
  return w({}, l, a);
}, n0 = (e) => w({}, e.size === "small" && {
  "& > *:nth-of-type(1)": {
    fontSize: 18
  }
}, e.size === "medium" && {
  "& > *:nth-of-type(1)": {
    fontSize: 20
  }
}, e.size === "large" && {
  "& > *:nth-of-type(1)": {
    fontSize: 22
  }
}), C_ = Q(vc, {
  shouldForwardProp: (e) => Gh(e) || e === "classes",
  name: "MuiButton",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[n.variant], t[`${n.variant}${j(n.color)}`], t[`size${j(n.size)}`], t[`${n.variant}Size${j(n.size)}`], n.color === "inherit" && t.colorInherit, n.disableElevation && t.disableElevation, n.fullWidth && t.fullWidth];
  }
})(({
  theme: e,
  ownerState: t
}) => {
  var n, r;
  const o = e.palette.mode === "light" ? e.palette.grey[300] : e.palette.grey[800], i = e.palette.mode === "light" ? e.palette.grey.A100 : e.palette.grey[700];
  return w({}, e.typography.button, {
    minWidth: 64,
    padding: "6px 16px",
    borderRadius: (e.vars || e).shape.borderRadius,
    transition: e.transitions.create(["background-color", "box-shadow", "border-color", "color"], {
      duration: e.transitions.duration.short
    }),
    "&:hover": w({
      textDecoration: "none",
      backgroundColor: e.vars ? `rgba(${e.vars.palette.text.primaryChannel} / ${e.vars.palette.action.hoverOpacity})` : ut(e.palette.text.primary, e.palette.action.hoverOpacity),
      // Reset on touch devices, it doesn't add specificity
      "@media (hover: none)": {
        backgroundColor: "transparent"
      }
    }, t.variant === "text" && t.color !== "inherit" && {
      backgroundColor: e.vars ? `rgba(${e.vars.palette[t.color].mainChannel} / ${e.vars.palette.action.hoverOpacity})` : ut(e.palette[t.color].main, e.palette.action.hoverOpacity),
      // Reset on touch devices, it doesn't add specificity
      "@media (hover: none)": {
        backgroundColor: "transparent"
      }
    }, t.variant === "outlined" && t.color !== "inherit" && {
      border: `1px solid ${(e.vars || e).palette[t.color].main}`,
      backgroundColor: e.vars ? `rgba(${e.vars.palette[t.color].mainChannel} / ${e.vars.palette.action.hoverOpacity})` : ut(e.palette[t.color].main, e.palette.action.hoverOpacity),
      // Reset on touch devices, it doesn't add specificity
      "@media (hover: none)": {
        backgroundColor: "transparent"
      }
    }, t.variant === "contained" && {
      backgroundColor: e.vars ? e.vars.palette.Button.inheritContainedHoverBg : i,
      boxShadow: (e.vars || e).shadows[4],
      // Reset on touch devices, it doesn't add specificity
      "@media (hover: none)": {
        boxShadow: (e.vars || e).shadows[2],
        backgroundColor: (e.vars || e).palette.grey[300]
      }
    }, t.variant === "contained" && t.color !== "inherit" && {
      backgroundColor: (e.vars || e).palette[t.color].dark,
      // Reset on touch devices, it doesn't add specificity
      "@media (hover: none)": {
        backgroundColor: (e.vars || e).palette[t.color].main
      }
    }),
    "&:active": w({}, t.variant === "contained" && {
      boxShadow: (e.vars || e).shadows[8]
    }),
    [`&.${ci.focusVisible}`]: w({}, t.variant === "contained" && {
      boxShadow: (e.vars || e).shadows[6]
    }),
    [`&.${ci.disabled}`]: w({
      color: (e.vars || e).palette.action.disabled
    }, t.variant === "outlined" && {
      border: `1px solid ${(e.vars || e).palette.action.disabledBackground}`
    }, t.variant === "contained" && {
      color: (e.vars || e).palette.action.disabled,
      boxShadow: (e.vars || e).shadows[0],
      backgroundColor: (e.vars || e).palette.action.disabledBackground
    })
  }, t.variant === "text" && {
    padding: "6px 8px"
  }, t.variant === "text" && t.color !== "inherit" && {
    color: (e.vars || e).palette[t.color].main
  }, t.variant === "outlined" && {
    padding: "5px 15px",
    border: "1px solid currentColor"
  }, t.variant === "outlined" && t.color !== "inherit" && {
    color: (e.vars || e).palette[t.color].main,
    border: e.vars ? `1px solid rgba(${e.vars.palette[t.color].mainChannel} / 0.5)` : `1px solid ${ut(e.palette[t.color].main, 0.5)}`
  }, t.variant === "contained" && {
    color: e.vars ? (
      // this is safe because grey does not change between default light/dark mode
      e.vars.palette.text.primary
    ) : (n = (r = e.palette).getContrastText) == null ? void 0 : n.call(r, e.palette.grey[300]),
    backgroundColor: e.vars ? e.vars.palette.Button.inheritContainedBg : o,
    boxShadow: (e.vars || e).shadows[2]
  }, t.variant === "contained" && t.color !== "inherit" && {
    color: (e.vars || e).palette[t.color].contrastText,
    backgroundColor: (e.vars || e).palette[t.color].main
  }, t.color === "inherit" && {
    color: "inherit",
    borderColor: "currentColor"
  }, t.size === "small" && t.variant === "text" && {
    padding: "4px 5px",
    fontSize: e.typography.pxToRem(13)
  }, t.size === "large" && t.variant === "text" && {
    padding: "8px 11px",
    fontSize: e.typography.pxToRem(15)
  }, t.size === "small" && t.variant === "outlined" && {
    padding: "3px 9px",
    fontSize: e.typography.pxToRem(13)
  }, t.size === "large" && t.variant === "outlined" && {
    padding: "7px 21px",
    fontSize: e.typography.pxToRem(15)
  }, t.size === "small" && t.variant === "contained" && {
    padding: "4px 10px",
    fontSize: e.typography.pxToRem(13)
  }, t.size === "large" && t.variant === "contained" && {
    padding: "8px 22px",
    fontSize: e.typography.pxToRem(15)
  }, t.fullWidth && {
    width: "100%"
  });
}, ({
  ownerState: e
}) => e.disableElevation && {
  boxShadow: "none",
  "&:hover": {
    boxShadow: "none"
  },
  [`&.${ci.focusVisible}`]: {
    boxShadow: "none"
  },
  "&:active": {
    boxShadow: "none"
  },
  [`&.${ci.disabled}`]: {
    boxShadow: "none"
  }
}), k_ = Q("span", {
  name: "MuiButton",
  slot: "StartIcon",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.startIcon, t[`iconSize${j(n.size)}`]];
  }
})(({
  ownerState: e
}) => w({
  display: "inherit",
  marginRight: 8,
  marginLeft: -4
}, e.size === "small" && {
  marginLeft: -2
}, n0(e))), __ = Q("span", {
  name: "MuiButton",
  slot: "EndIcon",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.endIcon, t[`iconSize${j(n.size)}`]];
  }
})(({
  ownerState: e
}) => w({
  display: "inherit",
  marginRight: -4,
  marginLeft: 8
}, e.size === "small" && {
  marginRight: -2
}, n0(e))), $_ = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = _.useContext(v_), o = _.useContext(x_), i = $o(r, t), l = fe({
    props: i,
    name: "MuiButton"
  }), {
    children: s,
    color: a = "primary",
    component: u = "button",
    className: c,
    disabled: f = !1,
    disableElevation: p = !1,
    disableFocusRipple: v = !1,
    endIcon: y,
    focusVisibleClassName: g,
    fullWidth: E = !1,
    size: m = "medium",
    startIcon: d,
    type: h,
    variant: S = "text"
  } = l, $ = L(l, S_), k = w({}, l, {
    color: a,
    component: u,
    disabled: f,
    disableElevation: p,
    disableFocusRipple: v,
    fullWidth: E,
    size: m,
    type: h,
    variant: S
  }), C = w_(k), T = d && /* @__PURE__ */ x.jsx(k_, {
    className: C.startIcon,
    ownerState: k,
    children: d
  }), z = y && /* @__PURE__ */ x.jsx(__, {
    className: C.endIcon,
    ownerState: k,
    children: y
  }), M = o || "";
  return /* @__PURE__ */ x.jsxs(C_, w({
    ownerState: k,
    className: B(r.className, C.root, c, M),
    component: u,
    disabled: f,
    focusRipple: !v,
    focusVisibleClassName: B(C.focusVisible, g),
    ref: n,
    type: h
  }, $, {
    classes: C,
    children: [T, s, z]
  }));
}), r0 = $_;
var kc = {}, E_ = yn;
Object.defineProperty(kc, "__esModule", {
  value: !0
});
var _c = kc.default = void 0, P_ = E_(Tr()), T_ = x;
_c = kc.default = (0, P_.default)(/* @__PURE__ */ (0, T_.jsx)("path", {
  d: "M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20z"
}), "ArrowBack");
const R_ = ({ activeView: e, setActiveView: t, data: n }) => {
  const r = n.devices.find((o) => o.serial === e.deviceId);
  return r ? /* @__PURE__ */ x.jsxs(Po, { children: [
    /* @__PURE__ */ x.jsx(
      r0,
      {
        startIcon: /* @__PURE__ */ x.jsx(_c, {}),
        onClick: () => t({ view: "dashboard" }),
        sx: { mb: 2 },
        children: "Back to Dashboard"
      }
    ),
    /* @__PURE__ */ x.jsx(ls, { children: /* @__PURE__ */ x.jsxs(ss, { children: [
      /* @__PURE__ */ x.jsx(me, { variant: "h6", gutterBottom: !0, children: "Device Details" }),
      /* @__PURE__ */ x.jsxs(me, { children: [
        "Name: ",
        r.name || r.mac
      ] }),
      /* @__PURE__ */ x.jsxs(me, { children: [
        "Status: ",
        r.status
      ] }),
      /* @__PURE__ */ x.jsxs(me, { children: [
        "Model: ",
        r.model
      ] }),
      /* @__PURE__ */ x.jsxs(me, { children: [
        "MAC Address: ",
        r.mac
      ] }),
      /* @__PURE__ */ x.jsxs(me, { children: [
        "Serial: ",
        r.serial
      ] })
    ] }) })
  ] }) : /* @__PURE__ */ x.jsx(me, { children: "Device not found" });
}, M_ = ({ activeView: e, setActiveView: t, data: n }) => {
  const r = n.networks.find((o) => o.id === e.networkId);
  return r ? /* @__PURE__ */ x.jsxs(Po, { children: [
    /* @__PURE__ */ x.jsx(
      r0,
      {
        startIcon: /* @__PURE__ */ x.jsx(_c, {}),
        onClick: () => t({ view: "dashboard" }),
        sx: { mb: 2 },
        children: "Back to Dashboard"
      }
    ),
    /* @__PURE__ */ x.jsx(ls, { children: /* @__PURE__ */ x.jsxs(ss, { children: [
      /* @__PURE__ */ x.jsx(me, { variant: "h6", gutterBottom: !0, children: "Network Information" }),
      /* @__PURE__ */ x.jsxs(me, { children: [
        "Name: ",
        r.name
      ] }),
      /* @__PURE__ */ x.jsxs(me, { children: [
        "ID: ",
        r.id
      ] }),
      /* @__PURE__ */ x.jsxs(me, { children: [
        "Product Types: ",
        r.product_types.join(", ")
      ] })
    ] }) })
  ] }) : /* @__PURE__ */ x.jsx(me, { children: "Network not found" });
};
const O_ = fc({
  palette: {
    mode: "dark"
  }
}), z_ = ({ hass: e, config_entry_id: t }) => {
  const [n, r] = _.useState(null), [o, i] = _.useState(!0), [l, s] = _.useState(null), [a, u] = _.useState({ view: "dashboard" });
  _.useEffect(() => {
    if (!e || !e.connection) {
      s("Home Assistant connection object not found."), i(!1);
      return;
    }
    (async () => {
      try {
        const p = await e.connection.sendMessagePromise({
          type: "meraki_ha/get_config",
          config_entry_id: t
        });
        r(p);
      } catch (p) {
        console.error("Error fetching Meraki data:", p), s(`Failed to fetch Meraki data: ${p.message || "Unknown error"}`);
      } finally {
        i(!1);
      }
    })();
  }, [e, t]);
  const c = () => {
    switch (a.view) {
      case "dashboard":
        return /* @__PURE__ */ x.jsx(p_, { setActiveView: u, data: n });
      case "device":
        return /* @__PURE__ */ x.jsx(R_, { activeView: a, setActiveView: u, data: n });
      case "network":
        return /* @__PURE__ */ x.jsx(M_, { activeView: a, setActiveView: u, data: n });
      default:
        return /* @__PURE__ */ x.jsx(me, { children: "Unknown view" });
    }
  };
  return /* @__PURE__ */ x.jsxs(H2, { theme: O_, children: [
    /* @__PURE__ */ x.jsx(q2, {}),
    /* @__PURE__ */ x.jsxs(J2, { maxWidth: "lg", sx: { mt: 4, mb: 4 }, children: [
      /* @__PURE__ */ x.jsx(me, { variant: "h4", component: "h1", gutterBottom: !0, children: "Meraki Control" }),
      o && /* @__PURE__ */ x.jsx(Po, { sx: { display: "flex", justifyContent: "center", p: 4 }, children: /* @__PURE__ */ x.jsx(gw, {}) }),
      l && /* @__PURE__ */ x.jsx(CC, { severity: "error", sx: { mt: 2 }, children: l }),
      !o && !l && c()
    ] })
  ] });
};
class N_ extends HTMLElement {
  constructor() {
    super(...arguments);
    Uo(this, "_root");
    Uo(this, "_hass");
    Uo(this, "_panel");
  }
  connectedCallback() {
    this._root = Qs.createRoot(this), this._render();
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
      /* @__PURE__ */ x.jsx(wn.StrictMode, { children: /* @__PURE__ */ x.jsx(z_, { hass: this._hass, config_entry_id: this._panel.config.config_entry_id }) })
    );
  }
}
customElements.define("meraki-panel", N_);
