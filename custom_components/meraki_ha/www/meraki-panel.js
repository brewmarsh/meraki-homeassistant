function y0(e, t) {
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
function If(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
function Qt(e) {
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
var Lf = { exports: {} }, al = {}, zf = { exports: {} }, A = {};
/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var bo = Symbol.for("react.element"), v0 = Symbol.for("react.portal"), x0 = Symbol.for("react.fragment"), S0 = Symbol.for("react.strict_mode"), w0 = Symbol.for("react.profiler"), C0 = Symbol.for("react.provider"), k0 = Symbol.for("react.context"), E0 = Symbol.for("react.forward_ref"), _0 = Symbol.for("react.suspense"), $0 = Symbol.for("react.memo"), P0 = Symbol.for("react.lazy"), _c = Symbol.iterator;
function T0(e) {
  return e === null || typeof e != "object" ? null : (e = _c && e[_c] || e["@@iterator"], typeof e == "function" ? e : null);
}
var bf = { isMounted: function() {
  return !1;
}, enqueueForceUpdate: function() {
}, enqueueReplaceState: function() {
}, enqueueSetState: function() {
} }, jf = Object.assign, Af = {};
function Rr(e, t, n) {
  this.props = e, this.context = t, this.refs = Af, this.updater = n || bf;
}
Rr.prototype.isReactComponent = {};
Rr.prototype.setState = function(e, t) {
  if (typeof e != "object" && typeof e != "function" && e != null)
    throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
  this.updater.enqueueSetState(this, e, t, "setState");
};
Rr.prototype.forceUpdate = function(e) {
  this.updater.enqueueForceUpdate(this, e, "forceUpdate");
};
function Df() {
}
Df.prototype = Rr.prototype;
function qa(e, t, n) {
  this.props = e, this.context = t, this.refs = Af, this.updater = n || bf;
}
var Ja = qa.prototype = new Df();
Ja.constructor = qa;
jf(Ja, Rr.prototype);
Ja.isPureReactComponent = !0;
var $c = Array.isArray, Ff = Object.prototype.hasOwnProperty, eu = { current: null }, Bf = { key: !0, ref: !0, __self: !0, __source: !0 };
function Uf(e, t, n) {
  var r, o = {}, i = null, l = null;
  if (t != null)
    for (r in t.ref !== void 0 && (l = t.ref), t.key !== void 0 && (i = "" + t.key), t)
      Ff.call(t, r) && !Bf.hasOwnProperty(r) && (o[r] = t[r]);
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
  return { $$typeof: bo, type: e, key: i, ref: l, props: o, _owner: eu.current };
}
function R0(e, t) {
  return { $$typeof: bo, type: e.type, key: t, ref: e.ref, props: e.props, _owner: e._owner };
}
function tu(e) {
  return typeof e == "object" && e !== null && e.$$typeof === bo;
}
function O0(e) {
  var t = { "=": "=0", ":": "=2" };
  return "$" + e.replace(/[=:]/g, function(n) {
    return t[n];
  });
}
var Pc = /\/+/g;
function cs(e, t) {
  return typeof e == "object" && e !== null && e.key != null ? O0("" + e.key) : t.toString(36);
}
function gi(e, t, n, r, o) {
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
          case bo:
          case v0:
            l = !0;
        }
    }
  if (l)
    return l = e, o = o(l), e = r === "" ? "." + cs(l, 0) : r, $c(o) ? (n = "", e != null && (n = e.replace(Pc, "$&/") + "/"), gi(o, t, n, "", function(u) {
      return u;
    })) : o != null && (tu(o) && (o = R0(o, n + (!o.key || l && l.key === o.key ? "" : ("" + o.key).replace(Pc, "$&/") + "/") + e)), t.push(o)), 1;
  if (l = 0, r = r === "" ? "." : r + ":", $c(e))
    for (var s = 0; s < e.length; s++) {
      i = e[s];
      var a = r + cs(i, s);
      l += gi(i, t, n, a, o);
    }
  else if (a = T0(e), typeof a == "function")
    for (e = a.call(e), s = 0; !(i = e.next()).done; )
      i = i.value, a = r + cs(i, s++), l += gi(i, t, n, a, o);
  else if (i === "object")
    throw t = String(e), Error("Objects are not valid as a React child (found: " + (t === "[object Object]" ? "object with keys {" + Object.keys(e).join(", ") + "}" : t) + "). If you meant to render a collection of children, use an array instead.");
  return l;
}
function Xo(e, t, n) {
  if (e == null)
    return e;
  var r = [], o = 0;
  return gi(e, r, "", "", function(i) {
    return t.call(n, i, o++);
  }), r;
}
function M0(e) {
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
var Ue = { current: null }, yi = { transition: null }, N0 = { ReactCurrentDispatcher: Ue, ReactCurrentBatchConfig: yi, ReactCurrentOwner: eu };
function Wf() {
  throw Error("act(...) is not supported in production builds of React.");
}
A.Children = { map: Xo, forEach: function(e, t, n) {
  Xo(e, function() {
    t.apply(this, arguments);
  }, n);
}, count: function(e) {
  var t = 0;
  return Xo(e, function() {
    t++;
  }), t;
}, toArray: function(e) {
  return Xo(e, function(t) {
    return t;
  }) || [];
}, only: function(e) {
  if (!tu(e))
    throw Error("React.Children.only expected to receive a single React element child.");
  return e;
} };
A.Component = Rr;
A.Fragment = x0;
A.Profiler = w0;
A.PureComponent = qa;
A.StrictMode = S0;
A.Suspense = _0;
A.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = N0;
A.act = Wf;
A.cloneElement = function(e, t, n) {
  if (e == null)
    throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + e + ".");
  var r = jf({}, e.props), o = e.key, i = e.ref, l = e._owner;
  if (t != null) {
    if (t.ref !== void 0 && (i = t.ref, l = eu.current), t.key !== void 0 && (o = "" + t.key), e.type && e.type.defaultProps)
      var s = e.type.defaultProps;
    for (a in t)
      Ff.call(t, a) && !Bf.hasOwnProperty(a) && (r[a] = t[a] === void 0 && s !== void 0 ? s[a] : t[a]);
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
  return { $$typeof: bo, type: e.type, key: o, ref: i, props: r, _owner: l };
};
A.createContext = function(e) {
  return e = { $$typeof: k0, _currentValue: e, _currentValue2: e, _threadCount: 0, Provider: null, Consumer: null, _defaultValue: null, _globalName: null }, e.Provider = { $$typeof: C0, _context: e }, e.Consumer = e;
};
A.createElement = Uf;
A.createFactory = function(e) {
  var t = Uf.bind(null, e);
  return t.type = e, t;
};
A.createRef = function() {
  return { current: null };
};
A.forwardRef = function(e) {
  return { $$typeof: E0, render: e };
};
A.isValidElement = tu;
A.lazy = function(e) {
  return { $$typeof: P0, _payload: { _status: -1, _result: e }, _init: M0 };
};
A.memo = function(e, t) {
  return { $$typeof: $0, type: e, compare: t === void 0 ? null : t };
};
A.startTransition = function(e) {
  var t = yi.transition;
  yi.transition = {};
  try {
    e();
  } finally {
    yi.transition = t;
  }
};
A.unstable_act = Wf;
A.useCallback = function(e, t) {
  return Ue.current.useCallback(e, t);
};
A.useContext = function(e) {
  return Ue.current.useContext(e);
};
A.useDebugValue = function() {
};
A.useDeferredValue = function(e) {
  return Ue.current.useDeferredValue(e);
};
A.useEffect = function(e, t) {
  return Ue.current.useEffect(e, t);
};
A.useId = function() {
  return Ue.current.useId();
};
A.useImperativeHandle = function(e, t, n) {
  return Ue.current.useImperativeHandle(e, t, n);
};
A.useInsertionEffect = function(e, t) {
  return Ue.current.useInsertionEffect(e, t);
};
A.useLayoutEffect = function(e, t) {
  return Ue.current.useLayoutEffect(e, t);
};
A.useMemo = function(e, t) {
  return Ue.current.useMemo(e, t);
};
A.useReducer = function(e, t, n) {
  return Ue.current.useReducer(e, t, n);
};
A.useRef = function(e) {
  return Ue.current.useRef(e);
};
A.useState = function(e) {
  return Ue.current.useState(e);
};
A.useSyncExternalStore = function(e, t, n) {
  return Ue.current.useSyncExternalStore(e, t, n);
};
A.useTransition = function() {
  return Ue.current.useTransition();
};
A.version = "18.3.1";
zf.exports = A;
var w = zf.exports;
const qe = /* @__PURE__ */ If(w), Hs = /* @__PURE__ */ y0({
  __proto__: null,
  default: qe
}, [w]);
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var I0 = w, L0 = Symbol.for("react.element"), z0 = Symbol.for("react.fragment"), b0 = Object.prototype.hasOwnProperty, j0 = I0.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, A0 = { key: !0, ref: !0, __self: !0, __source: !0 };
function Vf(e, t, n) {
  var r, o = {}, i = null, l = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (r in t)
    b0.call(t, r) && !A0.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps)
    for (r in t = e.defaultProps, t)
      o[r] === void 0 && (o[r] = t[r]);
  return { $$typeof: L0, type: e, key: i, ref: l, props: o, _owner: j0.current };
}
al.Fragment = z0;
al.jsx = Vf;
al.jsxs = Vf;
Lf.exports = al;
var C = Lf.exports, Gs = {}, Hf = { exports: {} }, ot = {}, Gf = { exports: {} }, Kf = {};
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
  function t(T, N) {
    var I = T.length;
    T.push(N);
    e:
      for (; 0 < I; ) {
        var U = I - 1 >>> 1, ae = T[U];
        if (0 < o(ae, N))
          T[U] = N, T[I] = ae, I = U;
        else
          break e;
      }
  }
  function n(T) {
    return T.length === 0 ? null : T[0];
  }
  function r(T) {
    if (T.length === 0)
      return null;
    var N = T[0], I = T.pop();
    if (I !== N) {
      T[0] = I;
      e:
        for (var U = 0, ae = T.length, Zt = ae >>> 1; U < Zt; ) {
          var Te = 2 * (U + 1) - 1, Rt = T[Te], L = Te + 1, xe = T[L];
          if (0 > o(Rt, I))
            L < ae && 0 > o(xe, Rt) ? (T[U] = xe, T[L] = I, U = L) : (T[U] = Rt, T[Te] = I, U = Te);
          else if (L < ae && 0 > o(xe, I))
            T[U] = xe, T[L] = I, U = L;
          else
            break e;
        }
    }
    return N;
  }
  function o(T, N) {
    var I = T.sortIndex - N.sortIndex;
    return I !== 0 ? I : T.id - N.id;
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
  var a = [], u = [], c = 1, f = null, m = 3, v = !1, y = !1, g = !1, $ = typeof setTimeout == "function" ? setTimeout : null, p = typeof clearTimeout == "function" ? clearTimeout : null, d = typeof setImmediate < "u" ? setImmediate : null;
  typeof navigator < "u" && navigator.scheduling !== void 0 && navigator.scheduling.isInputPending !== void 0 && navigator.scheduling.isInputPending.bind(navigator.scheduling);
  function h(T) {
    for (var N = n(u); N !== null; ) {
      if (N.callback === null)
        r(u);
      else if (N.startTime <= T)
        r(u), N.sortIndex = N.expirationTime, t(a, N);
      else
        break;
      N = n(u);
    }
  }
  function x(T) {
    if (g = !1, h(T), !y)
      if (n(a) !== null)
        y = !0, ge(_);
      else {
        var N = n(u);
        N !== null && fe(x, N.startTime - T);
      }
  }
  function _(T, N) {
    y = !1, g && (g = !1, p(R), R = -1), v = !0;
    var I = m;
    try {
      for (h(N), f = n(a); f !== null && (!(f.expirationTime > N) || T && !D()); ) {
        var U = f.callback;
        if (typeof U == "function") {
          f.callback = null, m = f.priorityLevel;
          var ae = U(f.expirationTime <= N);
          N = e.unstable_now(), typeof ae == "function" ? f.callback = ae : f === n(a) && r(a), h(N);
        } else
          r(a);
        f = n(a);
      }
      if (f !== null)
        var Zt = !0;
      else {
        var Te = n(u);
        Te !== null && fe(x, Te.startTime - N), Zt = !1;
      }
      return Zt;
    } finally {
      f = null, m = I, v = !1;
    }
  }
  var E = !1, k = null, R = -1, z = 5, O = -1;
  function D() {
    return !(e.unstable_now() - O < z);
  }
  function F() {
    if (k !== null) {
      var T = e.unstable_now();
      O = T;
      var N = !0;
      try {
        N = k(!0, T);
      } finally {
        N ? j() : (E = !1, k = null);
      }
    } else
      E = !1;
  }
  var j;
  if (typeof d == "function")
    j = function() {
      d(F);
    };
  else if (typeof MessageChannel < "u") {
    var X = new MessageChannel(), te = X.port2;
    X.port1.onmessage = F, j = function() {
      te.postMessage(null);
    };
  } else
    j = function() {
      $(F, 0);
    };
  function ge(T) {
    k = T, E || (E = !0, j());
  }
  function fe(T, N) {
    R = $(function() {
      T(e.unstable_now());
    }, N);
  }
  e.unstable_IdlePriority = 5, e.unstable_ImmediatePriority = 1, e.unstable_LowPriority = 4, e.unstable_NormalPriority = 3, e.unstable_Profiling = null, e.unstable_UserBlockingPriority = 2, e.unstable_cancelCallback = function(T) {
    T.callback = null;
  }, e.unstable_continueExecution = function() {
    y || v || (y = !0, ge(_));
  }, e.unstable_forceFrameRate = function(T) {
    0 > T || 125 < T ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : z = 0 < T ? Math.floor(1e3 / T) : 5;
  }, e.unstable_getCurrentPriorityLevel = function() {
    return m;
  }, e.unstable_getFirstCallbackNode = function() {
    return n(a);
  }, e.unstable_next = function(T) {
    switch (m) {
      case 1:
      case 2:
      case 3:
        var N = 3;
        break;
      default:
        N = m;
    }
    var I = m;
    m = N;
    try {
      return T();
    } finally {
      m = I;
    }
  }, e.unstable_pauseExecution = function() {
  }, e.unstable_requestPaint = function() {
  }, e.unstable_runWithPriority = function(T, N) {
    switch (T) {
      case 1:
      case 2:
      case 3:
      case 4:
      case 5:
        break;
      default:
        T = 3;
    }
    var I = m;
    m = T;
    try {
      return N();
    } finally {
      m = I;
    }
  }, e.unstable_scheduleCallback = function(T, N, I) {
    var U = e.unstable_now();
    switch (typeof I == "object" && I !== null ? (I = I.delay, I = typeof I == "number" && 0 < I ? U + I : U) : I = U, T) {
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
    return ae = I + ae, T = { id: c++, callback: N, priorityLevel: T, startTime: I, expirationTime: ae, sortIndex: -1 }, I > U ? (T.sortIndex = I, t(u, T), n(a) === null && T === n(u) && (g ? (p(R), R = -1) : g = !0, fe(x, I - U))) : (T.sortIndex = ae, t(a, T), y || v || (y = !0, ge(_))), T;
  }, e.unstable_shouldYield = D, e.unstable_wrapCallback = function(T) {
    var N = m;
    return function() {
      var I = m;
      m = N;
      try {
        return T.apply(this, arguments);
      } finally {
        m = I;
      }
    };
  };
})(Kf);
Gf.exports = Kf;
var D0 = Gf.exports;
/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var F0 = w, rt = D0;
function P(e) {
  for (var t = "https://reactjs.org/docs/error-decoder.html?invariant=" + e, n = 1; n < arguments.length; n++)
    t += "&args[]=" + encodeURIComponent(arguments[n]);
  return "Minified React error #" + e + "; visit " + t + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
}
var Qf = /* @__PURE__ */ new Set(), po = {};
function An(e, t) {
  vr(e, t), vr(e + "Capture", t);
}
function vr(e, t) {
  for (po[e] = t, e = 0; e < t.length; e++)
    Qf.add(t[e]);
}
var Vt = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), Ks = Object.prototype.hasOwnProperty, B0 = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, Tc = {}, Rc = {};
function U0(e) {
  return Ks.call(Rc, e) ? !0 : Ks.call(Tc, e) ? !1 : B0.test(e) ? Rc[e] = !0 : (Tc[e] = !0, !1);
}
function W0(e, t, n, r) {
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
function V0(e, t, n, r) {
  if (t === null || typeof t > "u" || W0(e, t, n, r))
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
function We(e, t, n, r, o, i, l) {
  this.acceptsBooleans = t === 2 || t === 3 || t === 4, this.attributeName = r, this.attributeNamespace = o, this.mustUseProperty = n, this.propertyName = e, this.type = t, this.sanitizeURL = i, this.removeEmptyString = l;
}
var Ne = {};
"children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(e) {
  Ne[e] = new We(e, 0, !1, e, null, !1, !1);
});
[["acceptCharset", "accept-charset"], ["className", "class"], ["htmlFor", "for"], ["httpEquiv", "http-equiv"]].forEach(function(e) {
  var t = e[0];
  Ne[t] = new We(t, 1, !1, e[1], null, !1, !1);
});
["contentEditable", "draggable", "spellCheck", "value"].forEach(function(e) {
  Ne[e] = new We(e, 2, !1, e.toLowerCase(), null, !1, !1);
});
["autoReverse", "externalResourcesRequired", "focusable", "preserveAlpha"].forEach(function(e) {
  Ne[e] = new We(e, 2, !1, e, null, !1, !1);
});
"allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(e) {
  Ne[e] = new We(e, 3, !1, e.toLowerCase(), null, !1, !1);
});
["checked", "multiple", "muted", "selected"].forEach(function(e) {
  Ne[e] = new We(e, 3, !0, e, null, !1, !1);
});
["capture", "download"].forEach(function(e) {
  Ne[e] = new We(e, 4, !1, e, null, !1, !1);
});
["cols", "rows", "size", "span"].forEach(function(e) {
  Ne[e] = new We(e, 6, !1, e, null, !1, !1);
});
["rowSpan", "start"].forEach(function(e) {
  Ne[e] = new We(e, 5, !1, e.toLowerCase(), null, !1, !1);
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
  Ne[t] = new We(t, 1, !1, e, null, !1, !1);
});
"xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(e) {
  var t = e.replace(nu, ru);
  Ne[t] = new We(t, 1, !1, e, "http://www.w3.org/1999/xlink", !1, !1);
});
["xml:base", "xml:lang", "xml:space"].forEach(function(e) {
  var t = e.replace(nu, ru);
  Ne[t] = new We(t, 1, !1, e, "http://www.w3.org/XML/1998/namespace", !1, !1);
});
["tabIndex", "crossOrigin"].forEach(function(e) {
  Ne[e] = new We(e, 1, !1, e.toLowerCase(), null, !1, !1);
});
Ne.xlinkHref = new We("xlinkHref", 1, !1, "xlink:href", "http://www.w3.org/1999/xlink", !0, !1);
["src", "href", "action", "formAction"].forEach(function(e) {
  Ne[e] = new We(e, 1, !1, e.toLowerCase(), null, !0, !0);
});
function ou(e, t, n, r) {
  var o = Ne.hasOwnProperty(t) ? Ne[t] : null;
  (o !== null ? o.type !== 0 : r || !(2 < t.length) || t[0] !== "o" && t[0] !== "O" || t[1] !== "n" && t[1] !== "N") && (V0(t, n, o, r) && (n = null), r || o === null ? U0(t) && (n === null ? e.removeAttribute(t) : e.setAttribute(t, "" + n)) : o.mustUseProperty ? e[o.propertyName] = n === null ? o.type === 3 ? !1 : "" : n : (t = o.attributeName, r = o.attributeNamespace, n === null ? e.removeAttribute(t) : (o = o.type, n = o === 3 || o === 4 && n === !0 ? "" : "" + n, r ? e.setAttributeNS(r, t, n) : e.setAttribute(t, n))));
}
var Yt = F0.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, Zo = Symbol.for("react.element"), Zn = Symbol.for("react.portal"), qn = Symbol.for("react.fragment"), iu = Symbol.for("react.strict_mode"), Qs = Symbol.for("react.profiler"), Yf = Symbol.for("react.provider"), Xf = Symbol.for("react.context"), lu = Symbol.for("react.forward_ref"), Ys = Symbol.for("react.suspense"), Xs = Symbol.for("react.suspense_list"), su = Symbol.for("react.memo"), en = Symbol.for("react.lazy"), Zf = Symbol.for("react.offscreen"), Oc = Symbol.iterator;
function Dr(e) {
  return e === null || typeof e != "object" ? null : (e = Oc && e[Oc] || e["@@iterator"], typeof e == "function" ? e : null);
}
var se = Object.assign, ds;
function Xr(e) {
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
var fs = !1;
function ps(e, t) {
  if (!e || fs)
    return "";
  fs = !0;
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
    fs = !1, Error.prepareStackTrace = n;
  }
  return (e = e ? e.displayName || e.name : "") ? Xr(e) : "";
}
function H0(e) {
  switch (e.tag) {
    case 5:
      return Xr(e.type);
    case 16:
      return Xr("Lazy");
    case 13:
      return Xr("Suspense");
    case 19:
      return Xr("SuspenseList");
    case 0:
    case 2:
    case 15:
      return e = ps(e.type, !1), e;
    case 11:
      return e = ps(e.type.render, !1), e;
    case 1:
      return e = ps(e.type, !0), e;
    default:
      return "";
  }
}
function Zs(e) {
  if (e == null)
    return null;
  if (typeof e == "function")
    return e.displayName || e.name || null;
  if (typeof e == "string")
    return e;
  switch (e) {
    case qn:
      return "Fragment";
    case Zn:
      return "Portal";
    case Qs:
      return "Profiler";
    case iu:
      return "StrictMode";
    case Ys:
      return "Suspense";
    case Xs:
      return "SuspenseList";
  }
  if (typeof e == "object")
    switch (e.$$typeof) {
      case Xf:
        return (e.displayName || "Context") + ".Consumer";
      case Yf:
        return (e._context.displayName || "Context") + ".Provider";
      case lu:
        var t = e.render;
        return e = e.displayName, e || (e = t.displayName || t.name || "", e = e !== "" ? "ForwardRef(" + e + ")" : "ForwardRef"), e;
      case su:
        return t = e.displayName || null, t !== null ? t : Zs(e.type) || "Memo";
      case en:
        t = e._payload, e = e._init;
        try {
          return Zs(e(t));
        } catch {
        }
    }
  return null;
}
function G0(e) {
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
      return Zs(t);
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
function yn(e) {
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
function qf(e) {
  var t = e.type;
  return (e = e.nodeName) && e.toLowerCase() === "input" && (t === "checkbox" || t === "radio");
}
function K0(e) {
  var t = qf(e) ? "checked" : "value", n = Object.getOwnPropertyDescriptor(e.constructor.prototype, t), r = "" + e[t];
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
function qo(e) {
  e._valueTracker || (e._valueTracker = K0(e));
}
function Jf(e) {
  if (!e)
    return !1;
  var t = e._valueTracker;
  if (!t)
    return !0;
  var n = t.getValue(), r = "";
  return e && (r = qf(e) ? e.checked ? "true" : "false" : e.value), e = r, e !== n ? (t.setValue(e), !0) : !1;
}
function Ii(e) {
  if (e = e || (typeof document < "u" ? document : void 0), typeof e > "u")
    return null;
  try {
    return e.activeElement || e.body;
  } catch {
    return e.body;
  }
}
function qs(e, t) {
  var n = t.checked;
  return se({}, t, { defaultChecked: void 0, defaultValue: void 0, value: void 0, checked: n ?? e._wrapperState.initialChecked });
}
function Mc(e, t) {
  var n = t.defaultValue == null ? "" : t.defaultValue, r = t.checked != null ? t.checked : t.defaultChecked;
  n = yn(t.value != null ? t.value : n), e._wrapperState = { initialChecked: r, initialValue: n, controlled: t.type === "checkbox" || t.type === "radio" ? t.checked != null : t.value != null };
}
function ep(e, t) {
  t = t.checked, t != null && ou(e, "checked", t, !1);
}
function Js(e, t) {
  ep(e, t);
  var n = yn(t.value), r = t.type;
  if (n != null)
    r === "number" ? (n === 0 && e.value === "" || e.value != n) && (e.value = "" + n) : e.value !== "" + n && (e.value = "" + n);
  else if (r === "submit" || r === "reset") {
    e.removeAttribute("value");
    return;
  }
  t.hasOwnProperty("value") ? ea(e, t.type, n) : t.hasOwnProperty("defaultValue") && ea(e, t.type, yn(t.defaultValue)), t.checked == null && t.defaultChecked != null && (e.defaultChecked = !!t.defaultChecked);
}
function Nc(e, t, n) {
  if (t.hasOwnProperty("value") || t.hasOwnProperty("defaultValue")) {
    var r = t.type;
    if (!(r !== "submit" && r !== "reset" || t.value !== void 0 && t.value !== null))
      return;
    t = "" + e._wrapperState.initialValue, n || t === e.value || (e.value = t), e.defaultValue = t;
  }
  n = e.name, n !== "" && (e.name = ""), e.defaultChecked = !!e._wrapperState.initialChecked, n !== "" && (e.name = n);
}
function ea(e, t, n) {
  (t !== "number" || Ii(e.ownerDocument) !== e) && (n == null ? e.defaultValue = "" + e._wrapperState.initialValue : e.defaultValue !== "" + n && (e.defaultValue = "" + n));
}
var Zr = Array.isArray;
function ur(e, t, n, r) {
  if (e = e.options, t) {
    t = {};
    for (var o = 0; o < n.length; o++)
      t["$" + n[o]] = !0;
    for (n = 0; n < e.length; n++)
      o = t.hasOwnProperty("$" + e[n].value), e[n].selected !== o && (e[n].selected = o), o && r && (e[n].defaultSelected = !0);
  } else {
    for (n = "" + yn(n), t = null, o = 0; o < e.length; o++) {
      if (e[o].value === n) {
        e[o].selected = !0, r && (e[o].defaultSelected = !0);
        return;
      }
      t !== null || e[o].disabled || (t = e[o]);
    }
    t !== null && (t.selected = !0);
  }
}
function ta(e, t) {
  if (t.dangerouslySetInnerHTML != null)
    throw Error(P(91));
  return se({}, t, { value: void 0, defaultValue: void 0, children: "" + e._wrapperState.initialValue });
}
function Ic(e, t) {
  var n = t.value;
  if (n == null) {
    if (n = t.children, t = t.defaultValue, n != null) {
      if (t != null)
        throw Error(P(92));
      if (Zr(n)) {
        if (1 < n.length)
          throw Error(P(93));
        n = n[0];
      }
      t = n;
    }
    t == null && (t = ""), n = t;
  }
  e._wrapperState = { initialValue: yn(n) };
}
function tp(e, t) {
  var n = yn(t.value), r = yn(t.defaultValue);
  n != null && (n = "" + n, n !== e.value && (e.value = n), t.defaultValue == null && e.defaultValue !== n && (e.defaultValue = n)), r != null && (e.defaultValue = "" + r);
}
function Lc(e) {
  var t = e.textContent;
  t === e._wrapperState.initialValue && t !== "" && t !== null && (e.value = t);
}
function np(e) {
  switch (e) {
    case "svg":
      return "http://www.w3.org/2000/svg";
    case "math":
      return "http://www.w3.org/1998/Math/MathML";
    default:
      return "http://www.w3.org/1999/xhtml";
  }
}
function na(e, t) {
  return e == null || e === "http://www.w3.org/1999/xhtml" ? np(t) : e === "http://www.w3.org/2000/svg" && t === "foreignObject" ? "http://www.w3.org/1999/xhtml" : e;
}
var Jo, rp = function(e) {
  return typeof MSApp < "u" && MSApp.execUnsafeLocalFunction ? function(t, n, r, o) {
    MSApp.execUnsafeLocalFunction(function() {
      return e(t, n, r, o);
    });
  } : e;
}(function(e, t) {
  if (e.namespaceURI !== "http://www.w3.org/2000/svg" || "innerHTML" in e)
    e.innerHTML = t;
  else {
    for (Jo = Jo || document.createElement("div"), Jo.innerHTML = "<svg>" + t.valueOf().toString() + "</svg>", t = Jo.firstChild; e.firstChild; )
      e.removeChild(e.firstChild);
    for (; t.firstChild; )
      e.appendChild(t.firstChild);
  }
});
function mo(e, t) {
  if (t) {
    var n = e.firstChild;
    if (n && n === e.lastChild && n.nodeType === 3) {
      n.nodeValue = t;
      return;
    }
  }
  e.textContent = t;
}
var no = {
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
}, Q0 = ["Webkit", "ms", "Moz", "O"];
Object.keys(no).forEach(function(e) {
  Q0.forEach(function(t) {
    t = t + e.charAt(0).toUpperCase() + e.substring(1), no[t] = no[e];
  });
});
function op(e, t, n) {
  return t == null || typeof t == "boolean" || t === "" ? "" : n || typeof t != "number" || t === 0 || no.hasOwnProperty(e) && no[e] ? ("" + t).trim() : t + "px";
}
function ip(e, t) {
  e = e.style;
  for (var n in t)
    if (t.hasOwnProperty(n)) {
      var r = n.indexOf("--") === 0, o = op(n, t[n], r);
      n === "float" && (n = "cssFloat"), r ? e.setProperty(n, o) : e[n] = o;
    }
}
var Y0 = se({ menuitem: !0 }, { area: !0, base: !0, br: !0, col: !0, embed: !0, hr: !0, img: !0, input: !0, keygen: !0, link: !0, meta: !0, param: !0, source: !0, track: !0, wbr: !0 });
function ra(e, t) {
  if (t) {
    if (Y0[e] && (t.children != null || t.dangerouslySetInnerHTML != null))
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
function oa(e, t) {
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
var ia = null;
function au(e) {
  return e = e.target || e.srcElement || window, e.correspondingUseElement && (e = e.correspondingUseElement), e.nodeType === 3 ? e.parentNode : e;
}
var la = null, cr = null, dr = null;
function zc(e) {
  if (e = Do(e)) {
    if (typeof la != "function")
      throw Error(P(280));
    var t = e.stateNode;
    t && (t = pl(t), la(e.stateNode, e.type, t));
  }
}
function lp(e) {
  cr ? dr ? dr.push(e) : dr = [e] : cr = e;
}
function sp() {
  if (cr) {
    var e = cr, t = dr;
    if (dr = cr = null, zc(e), t)
      for (e = 0; e < t.length; e++)
        zc(t[e]);
  }
}
function ap(e, t) {
  return e(t);
}
function up() {
}
var ms = !1;
function cp(e, t, n) {
  if (ms)
    return e(t, n);
  ms = !0;
  try {
    return ap(e, t, n);
  } finally {
    ms = !1, (cr !== null || dr !== null) && (up(), sp());
  }
}
function ho(e, t) {
  var n = e.stateNode;
  if (n === null)
    return null;
  var r = pl(n);
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
var sa = !1;
if (Vt)
  try {
    var Fr = {};
    Object.defineProperty(Fr, "passive", { get: function() {
      sa = !0;
    } }), window.addEventListener("test", Fr, Fr), window.removeEventListener("test", Fr, Fr);
  } catch {
    sa = !1;
  }
function X0(e, t, n, r, o, i, l, s, a) {
  var u = Array.prototype.slice.call(arguments, 3);
  try {
    t.apply(n, u);
  } catch (c) {
    this.onError(c);
  }
}
var ro = !1, Li = null, zi = !1, aa = null, Z0 = { onError: function(e) {
  ro = !0, Li = e;
} };
function q0(e, t, n, r, o, i, l, s, a) {
  ro = !1, Li = null, X0.apply(Z0, arguments);
}
function J0(e, t, n, r, o, i, l, s, a) {
  if (q0.apply(this, arguments), ro) {
    if (ro) {
      var u = Li;
      ro = !1, Li = null;
    } else
      throw Error(P(198));
    zi || (zi = !0, aa = u);
  }
}
function Dn(e) {
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
function dp(e) {
  if (e.tag === 13) {
    var t = e.memoizedState;
    if (t === null && (e = e.alternate, e !== null && (t = e.memoizedState)), t !== null)
      return t.dehydrated;
  }
  return null;
}
function bc(e) {
  if (Dn(e) !== e)
    throw Error(P(188));
}
function eg(e) {
  var t = e.alternate;
  if (!t) {
    if (t = Dn(e), t === null)
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
          return bc(o), e;
        if (i === r)
          return bc(o), t;
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
  return e = eg(e), e !== null ? pp(e) : null;
}
function pp(e) {
  if (e.tag === 5 || e.tag === 6)
    return e;
  for (e = e.child; e !== null; ) {
    var t = pp(e);
    if (t !== null)
      return t;
    e = e.sibling;
  }
  return null;
}
var mp = rt.unstable_scheduleCallback, jc = rt.unstable_cancelCallback, tg = rt.unstable_shouldYield, ng = rt.unstable_requestPaint, pe = rt.unstable_now, rg = rt.unstable_getCurrentPriorityLevel, uu = rt.unstable_ImmediatePriority, hp = rt.unstable_UserBlockingPriority, bi = rt.unstable_NormalPriority, og = rt.unstable_LowPriority, gp = rt.unstable_IdlePriority, ul = null, zt = null;
function ig(e) {
  if (zt && typeof zt.onCommitFiberRoot == "function")
    try {
      zt.onCommitFiberRoot(ul, e, void 0, (e.current.flags & 128) === 128);
    } catch {
    }
}
var $t = Math.clz32 ? Math.clz32 : ag, lg = Math.log, sg = Math.LN2;
function ag(e) {
  return e >>>= 0, e === 0 ? 32 : 31 - (lg(e) / sg | 0) | 0;
}
var ei = 64, ti = 4194304;
function qr(e) {
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
function ji(e, t) {
  var n = e.pendingLanes;
  if (n === 0)
    return 0;
  var r = 0, o = e.suspendedLanes, i = e.pingedLanes, l = n & 268435455;
  if (l !== 0) {
    var s = l & ~o;
    s !== 0 ? r = qr(s) : (i &= l, i !== 0 && (r = qr(i)));
  } else
    l = n & ~o, l !== 0 ? r = qr(l) : i !== 0 && (r = qr(i));
  if (r === 0)
    return 0;
  if (t !== 0 && t !== r && !(t & o) && (o = r & -r, i = t & -t, o >= i || o === 16 && (i & 4194240) !== 0))
    return t;
  if (r & 4 && (r |= n & 16), t = e.entangledLanes, t !== 0)
    for (e = e.entanglements, t &= r; 0 < t; )
      n = 31 - $t(t), o = 1 << n, r |= e[n], t &= ~o;
  return r;
}
function ug(e, t) {
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
function cg(e, t) {
  for (var n = e.suspendedLanes, r = e.pingedLanes, o = e.expirationTimes, i = e.pendingLanes; 0 < i; ) {
    var l = 31 - $t(i), s = 1 << l, a = o[l];
    a === -1 ? (!(s & n) || s & r) && (o[l] = ug(s, t)) : a <= t && (e.expiredLanes |= s), i &= ~s;
  }
}
function ua(e) {
  return e = e.pendingLanes & -1073741825, e !== 0 ? e : e & 1073741824 ? 1073741824 : 0;
}
function yp() {
  var e = ei;
  return ei <<= 1, !(ei & 4194240) && (ei = 64), e;
}
function hs(e) {
  for (var t = [], n = 0; 31 > n; n++)
    t.push(e);
  return t;
}
function jo(e, t, n) {
  e.pendingLanes |= t, t !== 536870912 && (e.suspendedLanes = 0, e.pingedLanes = 0), e = e.eventTimes, t = 31 - $t(t), e[t] = n;
}
function dg(e, t) {
  var n = e.pendingLanes & ~t;
  e.pendingLanes = t, e.suspendedLanes = 0, e.pingedLanes = 0, e.expiredLanes &= t, e.mutableReadLanes &= t, e.entangledLanes &= t, t = e.entanglements;
  var r = e.eventTimes;
  for (e = e.expirationTimes; 0 < n; ) {
    var o = 31 - $t(n), i = 1 << o;
    t[o] = 0, r[o] = -1, e[o] = -1, n &= ~i;
  }
}
function cu(e, t) {
  var n = e.entangledLanes |= t;
  for (e = e.entanglements; n; ) {
    var r = 31 - $t(n), o = 1 << r;
    o & t | e[r] & t && (e[r] |= t), n &= ~o;
  }
}
var K = 0;
function vp(e) {
  return e &= -e, 1 < e ? 4 < e ? e & 268435455 ? 16 : 536870912 : 4 : 1;
}
var xp, du, Sp, wp, Cp, ca = !1, ni = [], an = null, un = null, cn = null, go = /* @__PURE__ */ new Map(), yo = /* @__PURE__ */ new Map(), nn = [], fg = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
function Ac(e, t) {
  switch (e) {
    case "focusin":
    case "focusout":
      an = null;
      break;
    case "dragenter":
    case "dragleave":
      un = null;
      break;
    case "mouseover":
    case "mouseout":
      cn = null;
      break;
    case "pointerover":
    case "pointerout":
      go.delete(t.pointerId);
      break;
    case "gotpointercapture":
    case "lostpointercapture":
      yo.delete(t.pointerId);
  }
}
function Br(e, t, n, r, o, i) {
  return e === null || e.nativeEvent !== i ? (e = { blockedOn: t, domEventName: n, eventSystemFlags: r, nativeEvent: i, targetContainers: [o] }, t !== null && (t = Do(t), t !== null && du(t)), e) : (e.eventSystemFlags |= r, t = e.targetContainers, o !== null && t.indexOf(o) === -1 && t.push(o), e);
}
function pg(e, t, n, r, o) {
  switch (t) {
    case "focusin":
      return an = Br(an, e, t, n, r, o), !0;
    case "dragenter":
      return un = Br(un, e, t, n, r, o), !0;
    case "mouseover":
      return cn = Br(cn, e, t, n, r, o), !0;
    case "pointerover":
      var i = o.pointerId;
      return go.set(i, Br(go.get(i) || null, e, t, n, r, o)), !0;
    case "gotpointercapture":
      return i = o.pointerId, yo.set(i, Br(yo.get(i) || null, e, t, n, r, o)), !0;
  }
  return !1;
}
function kp(e) {
  var t = $n(e.target);
  if (t !== null) {
    var n = Dn(t);
    if (n !== null) {
      if (t = n.tag, t === 13) {
        if (t = dp(n), t !== null) {
          e.blockedOn = t, Cp(e.priority, function() {
            Sp(n);
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
function vi(e) {
  if (e.blockedOn !== null)
    return !1;
  for (var t = e.targetContainers; 0 < t.length; ) {
    var n = da(e.domEventName, e.eventSystemFlags, t[0], e.nativeEvent);
    if (n === null) {
      n = e.nativeEvent;
      var r = new n.constructor(n.type, n);
      ia = r, n.target.dispatchEvent(r), ia = null;
    } else
      return t = Do(n), t !== null && du(t), e.blockedOn = n, !1;
    t.shift();
  }
  return !0;
}
function Dc(e, t, n) {
  vi(e) && n.delete(t);
}
function mg() {
  ca = !1, an !== null && vi(an) && (an = null), un !== null && vi(un) && (un = null), cn !== null && vi(cn) && (cn = null), go.forEach(Dc), yo.forEach(Dc);
}
function Ur(e, t) {
  e.blockedOn === t && (e.blockedOn = null, ca || (ca = !0, rt.unstable_scheduleCallback(rt.unstable_NormalPriority, mg)));
}
function vo(e) {
  function t(o) {
    return Ur(o, e);
  }
  if (0 < ni.length) {
    Ur(ni[0], e);
    for (var n = 1; n < ni.length; n++) {
      var r = ni[n];
      r.blockedOn === e && (r.blockedOn = null);
    }
  }
  for (an !== null && Ur(an, e), un !== null && Ur(un, e), cn !== null && Ur(cn, e), go.forEach(t), yo.forEach(t), n = 0; n < nn.length; n++)
    r = nn[n], r.blockedOn === e && (r.blockedOn = null);
  for (; 0 < nn.length && (n = nn[0], n.blockedOn === null); )
    kp(n), n.blockedOn === null && nn.shift();
}
var fr = Yt.ReactCurrentBatchConfig, Ai = !0;
function hg(e, t, n, r) {
  var o = K, i = fr.transition;
  fr.transition = null;
  try {
    K = 1, fu(e, t, n, r);
  } finally {
    K = o, fr.transition = i;
  }
}
function gg(e, t, n, r) {
  var o = K, i = fr.transition;
  fr.transition = null;
  try {
    K = 4, fu(e, t, n, r);
  } finally {
    K = o, fr.transition = i;
  }
}
function fu(e, t, n, r) {
  if (Ai) {
    var o = da(e, t, n, r);
    if (o === null)
      _s(e, t, r, Di, n), Ac(e, r);
    else if (pg(o, e, t, n, r))
      r.stopPropagation();
    else if (Ac(e, r), t & 4 && -1 < fg.indexOf(e)) {
      for (; o !== null; ) {
        var i = Do(o);
        if (i !== null && xp(i), i = da(e, t, n, r), i === null && _s(e, t, r, Di, n), i === o)
          break;
        o = i;
      }
      o !== null && r.stopPropagation();
    } else
      _s(e, t, r, null, n);
  }
}
var Di = null;
function da(e, t, n, r) {
  if (Di = null, e = au(r), e = $n(e), e !== null)
    if (t = Dn(e), t === null)
      e = null;
    else if (n = t.tag, n === 13) {
      if (e = dp(t), e !== null)
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
function Ep(e) {
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
      switch (rg()) {
        case uu:
          return 1;
        case hp:
          return 4;
        case bi:
        case og:
          return 16;
        case gp:
          return 536870912;
        default:
          return 16;
      }
    default:
      return 16;
  }
}
var ln = null, pu = null, xi = null;
function _p() {
  if (xi)
    return xi;
  var e, t = pu, n = t.length, r, o = "value" in ln ? ln.value : ln.textContent, i = o.length;
  for (e = 0; e < n && t[e] === o[e]; e++)
    ;
  var l = n - e;
  for (r = 1; r <= l && t[n - r] === o[i - r]; r++)
    ;
  return xi = o.slice(e, 1 < r ? 1 - r : void 0);
}
function Si(e) {
  var t = e.keyCode;
  return "charCode" in e ? (e = e.charCode, e === 0 && t === 13 && (e = 13)) : e = t, e === 10 && (e = 13), 32 <= e || e === 13 ? e : 0;
}
function ri() {
  return !0;
}
function Fc() {
  return !1;
}
function it(e) {
  function t(n, r, o, i, l) {
    this._reactName = n, this._targetInst = o, this.type = r, this.nativeEvent = i, this.target = l, this.currentTarget = null;
    for (var s in e)
      e.hasOwnProperty(s) && (n = e[s], this[s] = n ? n(i) : i[s]);
    return this.isDefaultPrevented = (i.defaultPrevented != null ? i.defaultPrevented : i.returnValue === !1) ? ri : Fc, this.isPropagationStopped = Fc, this;
  }
  return se(t.prototype, { preventDefault: function() {
    this.defaultPrevented = !0;
    var n = this.nativeEvent;
    n && (n.preventDefault ? n.preventDefault() : typeof n.returnValue != "unknown" && (n.returnValue = !1), this.isDefaultPrevented = ri);
  }, stopPropagation: function() {
    var n = this.nativeEvent;
    n && (n.stopPropagation ? n.stopPropagation() : typeof n.cancelBubble != "unknown" && (n.cancelBubble = !0), this.isPropagationStopped = ri);
  }, persist: function() {
  }, isPersistent: ri }), t;
}
var Or = { eventPhase: 0, bubbles: 0, cancelable: 0, timeStamp: function(e) {
  return e.timeStamp || Date.now();
}, defaultPrevented: 0, isTrusted: 0 }, mu = it(Or), Ao = se({}, Or, { view: 0, detail: 0 }), yg = it(Ao), gs, ys, Wr, cl = se({}, Ao, { screenX: 0, screenY: 0, clientX: 0, clientY: 0, pageX: 0, pageY: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, getModifierState: hu, button: 0, buttons: 0, relatedTarget: function(e) {
  return e.relatedTarget === void 0 ? e.fromElement === e.srcElement ? e.toElement : e.fromElement : e.relatedTarget;
}, movementX: function(e) {
  return "movementX" in e ? e.movementX : (e !== Wr && (Wr && e.type === "mousemove" ? (gs = e.screenX - Wr.screenX, ys = e.screenY - Wr.screenY) : ys = gs = 0, Wr = e), gs);
}, movementY: function(e) {
  return "movementY" in e ? e.movementY : ys;
} }), Bc = it(cl), vg = se({}, cl, { dataTransfer: 0 }), xg = it(vg), Sg = se({}, Ao, { relatedTarget: 0 }), vs = it(Sg), wg = se({}, Or, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }), Cg = it(wg), kg = se({}, Or, { clipboardData: function(e) {
  return "clipboardData" in e ? e.clipboardData : window.clipboardData;
} }), Eg = it(kg), _g = se({}, Or, { data: 0 }), Uc = it(_g), $g = {
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
}, Pg = {
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
}, Tg = { Alt: "altKey", Control: "ctrlKey", Meta: "metaKey", Shift: "shiftKey" };
function Rg(e) {
  var t = this.nativeEvent;
  return t.getModifierState ? t.getModifierState(e) : (e = Tg[e]) ? !!t[e] : !1;
}
function hu() {
  return Rg;
}
var Og = se({}, Ao, { key: function(e) {
  if (e.key) {
    var t = $g[e.key] || e.key;
    if (t !== "Unidentified")
      return t;
  }
  return e.type === "keypress" ? (e = Si(e), e === 13 ? "Enter" : String.fromCharCode(e)) : e.type === "keydown" || e.type === "keyup" ? Pg[e.keyCode] || "Unidentified" : "";
}, code: 0, location: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, repeat: 0, locale: 0, getModifierState: hu, charCode: function(e) {
  return e.type === "keypress" ? Si(e) : 0;
}, keyCode: function(e) {
  return e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
}, which: function(e) {
  return e.type === "keypress" ? Si(e) : e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
} }), Mg = it(Og), Ng = se({}, cl, { pointerId: 0, width: 0, height: 0, pressure: 0, tangentialPressure: 0, tiltX: 0, tiltY: 0, twist: 0, pointerType: 0, isPrimary: 0 }), Wc = it(Ng), Ig = se({}, Ao, { touches: 0, targetTouches: 0, changedTouches: 0, altKey: 0, metaKey: 0, ctrlKey: 0, shiftKey: 0, getModifierState: hu }), Lg = it(Ig), zg = se({}, Or, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }), bg = it(zg), jg = se({}, cl, {
  deltaX: function(e) {
    return "deltaX" in e ? e.deltaX : "wheelDeltaX" in e ? -e.wheelDeltaX : 0;
  },
  deltaY: function(e) {
    return "deltaY" in e ? e.deltaY : "wheelDeltaY" in e ? -e.wheelDeltaY : "wheelDelta" in e ? -e.wheelDelta : 0;
  },
  deltaZ: 0,
  deltaMode: 0
}), Ag = it(jg), Dg = [9, 13, 27, 32], gu = Vt && "CompositionEvent" in window, oo = null;
Vt && "documentMode" in document && (oo = document.documentMode);
var Fg = Vt && "TextEvent" in window && !oo, $p = Vt && (!gu || oo && 8 < oo && 11 >= oo), Vc = String.fromCharCode(32), Hc = !1;
function Pp(e, t) {
  switch (e) {
    case "keyup":
      return Dg.indexOf(t.keyCode) !== -1;
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
function Tp(e) {
  return e = e.detail, typeof e == "object" && "data" in e ? e.data : null;
}
var Jn = !1;
function Bg(e, t) {
  switch (e) {
    case "compositionend":
      return Tp(t);
    case "keypress":
      return t.which !== 32 ? null : (Hc = !0, Vc);
    case "textInput":
      return e = t.data, e === Vc && Hc ? null : e;
    default:
      return null;
  }
}
function Ug(e, t) {
  if (Jn)
    return e === "compositionend" || !gu && Pp(e, t) ? (e = _p(), xi = pu = ln = null, Jn = !1, e) : null;
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
      return $p && t.locale !== "ko" ? null : t.data;
    default:
      return null;
  }
}
var Wg = { color: !0, date: !0, datetime: !0, "datetime-local": !0, email: !0, month: !0, number: !0, password: !0, range: !0, search: !0, tel: !0, text: !0, time: !0, url: !0, week: !0 };
function Gc(e) {
  var t = e && e.nodeName && e.nodeName.toLowerCase();
  return t === "input" ? !!Wg[e.type] : t === "textarea";
}
function Rp(e, t, n, r) {
  lp(r), t = Fi(t, "onChange"), 0 < t.length && (n = new mu("onChange", "change", null, n, r), e.push({ event: n, listeners: t }));
}
var io = null, xo = null;
function Vg(e) {
  Fp(e, 0);
}
function dl(e) {
  var t = nr(e);
  if (Jf(t))
    return e;
}
function Hg(e, t) {
  if (e === "change")
    return t;
}
var Op = !1;
if (Vt) {
  var xs;
  if (Vt) {
    var Ss = "oninput" in document;
    if (!Ss) {
      var Kc = document.createElement("div");
      Kc.setAttribute("oninput", "return;"), Ss = typeof Kc.oninput == "function";
    }
    xs = Ss;
  } else
    xs = !1;
  Op = xs && (!document.documentMode || 9 < document.documentMode);
}
function Qc() {
  io && (io.detachEvent("onpropertychange", Mp), xo = io = null);
}
function Mp(e) {
  if (e.propertyName === "value" && dl(xo)) {
    var t = [];
    Rp(t, xo, e, au(e)), cp(Vg, t);
  }
}
function Gg(e, t, n) {
  e === "focusin" ? (Qc(), io = t, xo = n, io.attachEvent("onpropertychange", Mp)) : e === "focusout" && Qc();
}
function Kg(e) {
  if (e === "selectionchange" || e === "keyup" || e === "keydown")
    return dl(xo);
}
function Qg(e, t) {
  if (e === "click")
    return dl(t);
}
function Yg(e, t) {
  if (e === "input" || e === "change")
    return dl(t);
}
function Xg(e, t) {
  return e === t && (e !== 0 || 1 / e === 1 / t) || e !== e && t !== t;
}
var Tt = typeof Object.is == "function" ? Object.is : Xg;
function So(e, t) {
  if (Tt(e, t))
    return !0;
  if (typeof e != "object" || e === null || typeof t != "object" || t === null)
    return !1;
  var n = Object.keys(e), r = Object.keys(t);
  if (n.length !== r.length)
    return !1;
  for (r = 0; r < n.length; r++) {
    var o = n[r];
    if (!Ks.call(t, o) || !Tt(e[o], t[o]))
      return !1;
  }
  return !0;
}
function Yc(e) {
  for (; e && e.firstChild; )
    e = e.firstChild;
  return e;
}
function Xc(e, t) {
  var n = Yc(e);
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
    n = Yc(n);
  }
}
function Np(e, t) {
  return e && t ? e === t ? !0 : e && e.nodeType === 3 ? !1 : t && t.nodeType === 3 ? Np(e, t.parentNode) : "contains" in e ? e.contains(t) : e.compareDocumentPosition ? !!(e.compareDocumentPosition(t) & 16) : !1 : !1;
}
function Ip() {
  for (var e = window, t = Ii(); t instanceof e.HTMLIFrameElement; ) {
    try {
      var n = typeof t.contentWindow.location.href == "string";
    } catch {
      n = !1;
    }
    if (n)
      e = t.contentWindow;
    else
      break;
    t = Ii(e.document);
  }
  return t;
}
function yu(e) {
  var t = e && e.nodeName && e.nodeName.toLowerCase();
  return t && (t === "input" && (e.type === "text" || e.type === "search" || e.type === "tel" || e.type === "url" || e.type === "password") || t === "textarea" || e.contentEditable === "true");
}
function Zg(e) {
  var t = Ip(), n = e.focusedElem, r = e.selectionRange;
  if (t !== n && n && n.ownerDocument && Np(n.ownerDocument.documentElement, n)) {
    if (r !== null && yu(n)) {
      if (t = r.start, e = r.end, e === void 0 && (e = t), "selectionStart" in n)
        n.selectionStart = t, n.selectionEnd = Math.min(e, n.value.length);
      else if (e = (t = n.ownerDocument || document) && t.defaultView || window, e.getSelection) {
        e = e.getSelection();
        var o = n.textContent.length, i = Math.min(r.start, o);
        r = r.end === void 0 ? i : Math.min(r.end, o), !e.extend && i > r && (o = r, r = i, i = o), o = Xc(n, i);
        var l = Xc(
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
var qg = Vt && "documentMode" in document && 11 >= document.documentMode, er = null, fa = null, lo = null, pa = !1;
function Zc(e, t, n) {
  var r = n.window === n ? n.document : n.nodeType === 9 ? n : n.ownerDocument;
  pa || er == null || er !== Ii(r) || (r = er, "selectionStart" in r && yu(r) ? r = { start: r.selectionStart, end: r.selectionEnd } : (r = (r.ownerDocument && r.ownerDocument.defaultView || window).getSelection(), r = { anchorNode: r.anchorNode, anchorOffset: r.anchorOffset, focusNode: r.focusNode, focusOffset: r.focusOffset }), lo && So(lo, r) || (lo = r, r = Fi(fa, "onSelect"), 0 < r.length && (t = new mu("onSelect", "select", null, t, n), e.push({ event: t, listeners: r }), t.target = er)));
}
function oi(e, t) {
  var n = {};
  return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit" + e] = "webkit" + t, n["Moz" + e] = "moz" + t, n;
}
var tr = { animationend: oi("Animation", "AnimationEnd"), animationiteration: oi("Animation", "AnimationIteration"), animationstart: oi("Animation", "AnimationStart"), transitionend: oi("Transition", "TransitionEnd") }, ws = {}, Lp = {};
Vt && (Lp = document.createElement("div").style, "AnimationEvent" in window || (delete tr.animationend.animation, delete tr.animationiteration.animation, delete tr.animationstart.animation), "TransitionEvent" in window || delete tr.transitionend.transition);
function fl(e) {
  if (ws[e])
    return ws[e];
  if (!tr[e])
    return e;
  var t = tr[e], n;
  for (n in t)
    if (t.hasOwnProperty(n) && n in Lp)
      return ws[e] = t[n];
  return e;
}
var zp = fl("animationend"), bp = fl("animationiteration"), jp = fl("animationstart"), Ap = fl("transitionend"), Dp = /* @__PURE__ */ new Map(), qc = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
function xn(e, t) {
  Dp.set(e, t), An(t, [e]);
}
for (var Cs = 0; Cs < qc.length; Cs++) {
  var ks = qc[Cs], Jg = ks.toLowerCase(), ey = ks[0].toUpperCase() + ks.slice(1);
  xn(Jg, "on" + ey);
}
xn(zp, "onAnimationEnd");
xn(bp, "onAnimationIteration");
xn(jp, "onAnimationStart");
xn("dblclick", "onDoubleClick");
xn("focusin", "onFocus");
xn("focusout", "onBlur");
xn(Ap, "onTransitionEnd");
vr("onMouseEnter", ["mouseout", "mouseover"]);
vr("onMouseLeave", ["mouseout", "mouseover"]);
vr("onPointerEnter", ["pointerout", "pointerover"]);
vr("onPointerLeave", ["pointerout", "pointerover"]);
An("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" "));
An("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));
An("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]);
An("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" "));
An("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" "));
An("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
var Jr = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), ty = new Set("cancel close invalid load scroll toggle".split(" ").concat(Jr));
function Jc(e, t, n) {
  var r = e.type || "unknown-event";
  e.currentTarget = n, J0(r, t, void 0, e), e.currentTarget = null;
}
function Fp(e, t) {
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
          Jc(o, s, u), i = a;
        }
      else
        for (l = 0; l < r.length; l++) {
          if (s = r[l], a = s.instance, u = s.currentTarget, s = s.listener, a !== i && o.isPropagationStopped())
            break e;
          Jc(o, s, u), i = a;
        }
    }
  }
  if (zi)
    throw e = aa, zi = !1, aa = null, e;
}
function J(e, t) {
  var n = t[va];
  n === void 0 && (n = t[va] = /* @__PURE__ */ new Set());
  var r = e + "__bubble";
  n.has(r) || (Bp(t, e, 2, !1), n.add(r));
}
function Es(e, t, n) {
  var r = 0;
  t && (r |= 4), Bp(n, e, r, t);
}
var ii = "_reactListening" + Math.random().toString(36).slice(2);
function wo(e) {
  if (!e[ii]) {
    e[ii] = !0, Qf.forEach(function(n) {
      n !== "selectionchange" && (ty.has(n) || Es(n, !1, e), Es(n, !0, e));
    });
    var t = e.nodeType === 9 ? e : e.ownerDocument;
    t === null || t[ii] || (t[ii] = !0, Es("selectionchange", !1, t));
  }
}
function Bp(e, t, n, r) {
  switch (Ep(t)) {
    case 1:
      var o = hg;
      break;
    case 4:
      o = gg;
      break;
    default:
      o = fu;
  }
  n = o.bind(null, t, n, e), o = void 0, !sa || t !== "touchstart" && t !== "touchmove" && t !== "wheel" || (o = !0), r ? o !== void 0 ? e.addEventListener(t, n, { capture: !0, passive: o }) : e.addEventListener(t, n, !0) : o !== void 0 ? e.addEventListener(t, n, { passive: o }) : e.addEventListener(t, n, !1);
}
function _s(e, t, n, r, o) {
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
            if (l = $n(s), l === null)
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
  cp(function() {
    var u = i, c = au(n), f = [];
    e: {
      var m = Dp.get(e);
      if (m !== void 0) {
        var v = mu, y = e;
        switch (e) {
          case "keypress":
            if (Si(n) === 0)
              break e;
          case "keydown":
          case "keyup":
            v = Mg;
            break;
          case "focusin":
            y = "focus", v = vs;
            break;
          case "focusout":
            y = "blur", v = vs;
            break;
          case "beforeblur":
          case "afterblur":
            v = vs;
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
            v = Bc;
            break;
          case "drag":
          case "dragend":
          case "dragenter":
          case "dragexit":
          case "dragleave":
          case "dragover":
          case "dragstart":
          case "drop":
            v = xg;
            break;
          case "touchcancel":
          case "touchend":
          case "touchmove":
          case "touchstart":
            v = Lg;
            break;
          case zp:
          case bp:
          case jp:
            v = Cg;
            break;
          case Ap:
            v = bg;
            break;
          case "scroll":
            v = yg;
            break;
          case "wheel":
            v = Ag;
            break;
          case "copy":
          case "cut":
          case "paste":
            v = Eg;
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
        var g = (t & 4) !== 0, $ = !g && e === "scroll", p = g ? m !== null ? m + "Capture" : null : m;
        g = [];
        for (var d = u, h; d !== null; ) {
          h = d;
          var x = h.stateNode;
          if (h.tag === 5 && x !== null && (h = x, p !== null && (x = ho(d, p), x != null && g.push(Co(d, x, h)))), $)
            break;
          d = d.return;
        }
        0 < g.length && (m = new v(m, y, null, n, c), f.push({ event: m, listeners: g }));
      }
    }
    if (!(t & 7)) {
      e: {
        if (m = e === "mouseover" || e === "pointerover", v = e === "mouseout" || e === "pointerout", m && n !== ia && (y = n.relatedTarget || n.fromElement) && ($n(y) || y[Ht]))
          break e;
        if ((v || m) && (m = c.window === c ? c : (m = c.ownerDocument) ? m.defaultView || m.parentWindow : window, v ? (y = n.relatedTarget || n.toElement, v = u, y = y ? $n(y) : null, y !== null && ($ = Dn(y), y !== $ || y.tag !== 5 && y.tag !== 6) && (y = null)) : (v = null, y = u), v !== y)) {
          if (g = Bc, x = "onMouseLeave", p = "onMouseEnter", d = "mouse", (e === "pointerout" || e === "pointerover") && (g = Wc, x = "onPointerLeave", p = "onPointerEnter", d = "pointer"), $ = v == null ? m : nr(v), h = y == null ? m : nr(y), m = new g(x, d + "leave", v, n, c), m.target = $, m.relatedTarget = h, x = null, $n(c) === u && (g = new g(p, d + "enter", y, n, c), g.target = h, g.relatedTarget = $, x = g), $ = x, v && y)
            t: {
              for (g = v, p = y, d = 0, h = g; h; h = Bn(h))
                d++;
              for (h = 0, x = p; x; x = Bn(x))
                h++;
              for (; 0 < d - h; )
                g = Bn(g), d--;
              for (; 0 < h - d; )
                p = Bn(p), h--;
              for (; d--; ) {
                if (g === p || p !== null && g === p.alternate)
                  break t;
                g = Bn(g), p = Bn(p);
              }
              g = null;
            }
          else
            g = null;
          v !== null && ed(f, m, v, g, !1), y !== null && $ !== null && ed(f, $, y, g, !0);
        }
      }
      e: {
        if (m = u ? nr(u) : window, v = m.nodeName && m.nodeName.toLowerCase(), v === "select" || v === "input" && m.type === "file")
          var _ = Hg;
        else if (Gc(m))
          if (Op)
            _ = Yg;
          else {
            _ = Kg;
            var E = Gg;
          }
        else
          (v = m.nodeName) && v.toLowerCase() === "input" && (m.type === "checkbox" || m.type === "radio") && (_ = Qg);
        if (_ && (_ = _(e, u))) {
          Rp(f, _, n, c);
          break e;
        }
        E && E(e, m, u), e === "focusout" && (E = m._wrapperState) && E.controlled && m.type === "number" && ea(m, "number", m.value);
      }
      switch (E = u ? nr(u) : window, e) {
        case "focusin":
          (Gc(E) || E.contentEditable === "true") && (er = E, fa = u, lo = null);
          break;
        case "focusout":
          lo = fa = er = null;
          break;
        case "mousedown":
          pa = !0;
          break;
        case "contextmenu":
        case "mouseup":
        case "dragend":
          pa = !1, Zc(f, n, c);
          break;
        case "selectionchange":
          if (qg)
            break;
        case "keydown":
        case "keyup":
          Zc(f, n, c);
      }
      var k;
      if (gu)
        e: {
          switch (e) {
            case "compositionstart":
              var R = "onCompositionStart";
              break e;
            case "compositionend":
              R = "onCompositionEnd";
              break e;
            case "compositionupdate":
              R = "onCompositionUpdate";
              break e;
          }
          R = void 0;
        }
      else
        Jn ? Pp(e, n) && (R = "onCompositionEnd") : e === "keydown" && n.keyCode === 229 && (R = "onCompositionStart");
      R && ($p && n.locale !== "ko" && (Jn || R !== "onCompositionStart" ? R === "onCompositionEnd" && Jn && (k = _p()) : (ln = c, pu = "value" in ln ? ln.value : ln.textContent, Jn = !0)), E = Fi(u, R), 0 < E.length && (R = new Uc(R, e, null, n, c), f.push({ event: R, listeners: E }), k ? R.data = k : (k = Tp(n), k !== null && (R.data = k)))), (k = Fg ? Bg(e, n) : Ug(e, n)) && (u = Fi(u, "onBeforeInput"), 0 < u.length && (c = new Uc("onBeforeInput", "beforeinput", null, n, c), f.push({ event: c, listeners: u }), c.data = k));
    }
    Fp(f, t);
  });
}
function Co(e, t, n) {
  return { instance: e, listener: t, currentTarget: n };
}
function Fi(e, t) {
  for (var n = t + "Capture", r = []; e !== null; ) {
    var o = e, i = o.stateNode;
    o.tag === 5 && i !== null && (o = i, i = ho(e, n), i != null && r.unshift(Co(e, i, o)), i = ho(e, t), i != null && r.push(Co(e, i, o))), e = e.return;
  }
  return r;
}
function Bn(e) {
  if (e === null)
    return null;
  do
    e = e.return;
  while (e && e.tag !== 5);
  return e || null;
}
function ed(e, t, n, r, o) {
  for (var i = t._reactName, l = []; n !== null && n !== r; ) {
    var s = n, a = s.alternate, u = s.stateNode;
    if (a !== null && a === r)
      break;
    s.tag === 5 && u !== null && (s = u, o ? (a = ho(n, i), a != null && l.unshift(Co(n, a, s))) : o || (a = ho(n, i), a != null && l.push(Co(n, a, s)))), n = n.return;
  }
  l.length !== 0 && e.push({ event: t, listeners: l });
}
var ny = /\r\n?/g, ry = /\u0000|\uFFFD/g;
function td(e) {
  return (typeof e == "string" ? e : "" + e).replace(ny, `
`).replace(ry, "");
}
function li(e, t, n) {
  if (t = td(t), td(e) !== t && n)
    throw Error(P(425));
}
function Bi() {
}
var ma = null, ha = null;
function ga(e, t) {
  return e === "textarea" || e === "noscript" || typeof t.children == "string" || typeof t.children == "number" || typeof t.dangerouslySetInnerHTML == "object" && t.dangerouslySetInnerHTML !== null && t.dangerouslySetInnerHTML.__html != null;
}
var ya = typeof setTimeout == "function" ? setTimeout : void 0, oy = typeof clearTimeout == "function" ? clearTimeout : void 0, nd = typeof Promise == "function" ? Promise : void 0, iy = typeof queueMicrotask == "function" ? queueMicrotask : typeof nd < "u" ? function(e) {
  return nd.resolve(null).then(e).catch(ly);
} : ya;
function ly(e) {
  setTimeout(function() {
    throw e;
  });
}
function $s(e, t) {
  var n = t, r = 0;
  do {
    var o = n.nextSibling;
    if (e.removeChild(n), o && o.nodeType === 8)
      if (n = o.data, n === "/$") {
        if (r === 0) {
          e.removeChild(o), vo(t);
          return;
        }
        r--;
      } else
        n !== "$" && n !== "$?" && n !== "$!" || r++;
    n = o;
  } while (n);
  vo(t);
}
function dn(e) {
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
function rd(e) {
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
var Mr = Math.random().toString(36).slice(2), Lt = "__reactFiber$" + Mr, ko = "__reactProps$" + Mr, Ht = "__reactContainer$" + Mr, va = "__reactEvents$" + Mr, sy = "__reactListeners$" + Mr, ay = "__reactHandles$" + Mr;
function $n(e) {
  var t = e[Lt];
  if (t)
    return t;
  for (var n = e.parentNode; n; ) {
    if (t = n[Ht] || n[Lt]) {
      if (n = t.alternate, t.child !== null || n !== null && n.child !== null)
        for (e = rd(e); e !== null; ) {
          if (n = e[Lt])
            return n;
          e = rd(e);
        }
      return t;
    }
    e = n, n = e.parentNode;
  }
  return null;
}
function Do(e) {
  return e = e[Lt] || e[Ht], !e || e.tag !== 5 && e.tag !== 6 && e.tag !== 13 && e.tag !== 3 ? null : e;
}
function nr(e) {
  if (e.tag === 5 || e.tag === 6)
    return e.stateNode;
  throw Error(P(33));
}
function pl(e) {
  return e[ko] || null;
}
var xa = [], rr = -1;
function Sn(e) {
  return { current: e };
}
function ee(e) {
  0 > rr || (e.current = xa[rr], xa[rr] = null, rr--);
}
function q(e, t) {
  rr++, xa[rr] = e.current, e.current = t;
}
var vn = {}, Ae = Sn(vn), Ge = Sn(!1), Nn = vn;
function xr(e, t) {
  var n = e.type.contextTypes;
  if (!n)
    return vn;
  var r = e.stateNode;
  if (r && r.__reactInternalMemoizedUnmaskedChildContext === t)
    return r.__reactInternalMemoizedMaskedChildContext;
  var o = {}, i;
  for (i in n)
    o[i] = t[i];
  return r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = t, e.__reactInternalMemoizedMaskedChildContext = o), o;
}
function Ke(e) {
  return e = e.childContextTypes, e != null;
}
function Ui() {
  ee(Ge), ee(Ae);
}
function od(e, t, n) {
  if (Ae.current !== vn)
    throw Error(P(168));
  q(Ae, t), q(Ge, n);
}
function Up(e, t, n) {
  var r = e.stateNode;
  if (t = t.childContextTypes, typeof r.getChildContext != "function")
    return n;
  r = r.getChildContext();
  for (var o in r)
    if (!(o in t))
      throw Error(P(108, G0(e) || "Unknown", o));
  return se({}, n, r);
}
function Wi(e) {
  return e = (e = e.stateNode) && e.__reactInternalMemoizedMergedChildContext || vn, Nn = Ae.current, q(Ae, e), q(Ge, Ge.current), !0;
}
function id(e, t, n) {
  var r = e.stateNode;
  if (!r)
    throw Error(P(169));
  n ? (e = Up(e, t, Nn), r.__reactInternalMemoizedMergedChildContext = e, ee(Ge), ee(Ae), q(Ae, e)) : ee(Ge), q(Ge, n);
}
var Ft = null, ml = !1, Ps = !1;
function Wp(e) {
  Ft === null ? Ft = [e] : Ft.push(e);
}
function uy(e) {
  ml = !0, Wp(e);
}
function wn() {
  if (!Ps && Ft !== null) {
    Ps = !0;
    var e = 0, t = K;
    try {
      var n = Ft;
      for (K = 1; e < n.length; e++) {
        var r = n[e];
        do
          r = r(!0);
        while (r !== null);
      }
      Ft = null, ml = !1;
    } catch (o) {
      throw Ft !== null && (Ft = Ft.slice(e + 1)), mp(uu, wn), o;
    } finally {
      K = t, Ps = !1;
    }
  }
  return null;
}
var or = [], ir = 0, Vi = null, Hi = 0, ut = [], ct = 0, In = null, Bt = 1, Ut = "";
function Cn(e, t) {
  or[ir++] = Hi, or[ir++] = Vi, Vi = e, Hi = t;
}
function Vp(e, t, n) {
  ut[ct++] = Bt, ut[ct++] = Ut, ut[ct++] = In, In = e;
  var r = Bt;
  e = Ut;
  var o = 32 - $t(r) - 1;
  r &= ~(1 << o), n += 1;
  var i = 32 - $t(t) + o;
  if (30 < i) {
    var l = o - o % 5;
    i = (r & (1 << l) - 1).toString(32), r >>= l, o -= l, Bt = 1 << 32 - $t(t) + o | n << o | r, Ut = i + e;
  } else
    Bt = 1 << i | n << o | r, Ut = e;
}
function vu(e) {
  e.return !== null && (Cn(e, 1), Vp(e, 1, 0));
}
function xu(e) {
  for (; e === Vi; )
    Vi = or[--ir], or[ir] = null, Hi = or[--ir], or[ir] = null;
  for (; e === In; )
    In = ut[--ct], ut[ct] = null, Ut = ut[--ct], ut[ct] = null, Bt = ut[--ct], ut[ct] = null;
}
var tt = null, Je = null, re = !1, _t = null;
function Hp(e, t) {
  var n = ft(5, null, null, 0);
  n.elementType = "DELETED", n.stateNode = t, n.return = e, t = e.deletions, t === null ? (e.deletions = [n], e.flags |= 16) : t.push(n);
}
function ld(e, t) {
  switch (e.tag) {
    case 5:
      var n = e.type;
      return t = t.nodeType !== 1 || n.toLowerCase() !== t.nodeName.toLowerCase() ? null : t, t !== null ? (e.stateNode = t, tt = e, Je = dn(t.firstChild), !0) : !1;
    case 6:
      return t = e.pendingProps === "" || t.nodeType !== 3 ? null : t, t !== null ? (e.stateNode = t, tt = e, Je = null, !0) : !1;
    case 13:
      return t = t.nodeType !== 8 ? null : t, t !== null ? (n = In !== null ? { id: Bt, overflow: Ut } : null, e.memoizedState = { dehydrated: t, treeContext: n, retryLane: 1073741824 }, n = ft(18, null, null, 0), n.stateNode = t, n.return = e, e.child = n, tt = e, Je = null, !0) : !1;
    default:
      return !1;
  }
}
function Sa(e) {
  return (e.mode & 1) !== 0 && (e.flags & 128) === 0;
}
function wa(e) {
  if (re) {
    var t = Je;
    if (t) {
      var n = t;
      if (!ld(e, t)) {
        if (Sa(e))
          throw Error(P(418));
        t = dn(n.nextSibling);
        var r = tt;
        t && ld(e, t) ? Hp(r, n) : (e.flags = e.flags & -4097 | 2, re = !1, tt = e);
      }
    } else {
      if (Sa(e))
        throw Error(P(418));
      e.flags = e.flags & -4097 | 2, re = !1, tt = e;
    }
  }
}
function sd(e) {
  for (e = e.return; e !== null && e.tag !== 5 && e.tag !== 3 && e.tag !== 13; )
    e = e.return;
  tt = e;
}
function si(e) {
  if (e !== tt)
    return !1;
  if (!re)
    return sd(e), re = !0, !1;
  var t;
  if ((t = e.tag !== 3) && !(t = e.tag !== 5) && (t = e.type, t = t !== "head" && t !== "body" && !ga(e.type, e.memoizedProps)), t && (t = Je)) {
    if (Sa(e))
      throw Gp(), Error(P(418));
    for (; t; )
      Hp(e, t), t = dn(t.nextSibling);
  }
  if (sd(e), e.tag === 13) {
    if (e = e.memoizedState, e = e !== null ? e.dehydrated : null, !e)
      throw Error(P(317));
    e: {
      for (e = e.nextSibling, t = 0; e; ) {
        if (e.nodeType === 8) {
          var n = e.data;
          if (n === "/$") {
            if (t === 0) {
              Je = dn(e.nextSibling);
              break e;
            }
            t--;
          } else
            n !== "$" && n !== "$!" && n !== "$?" || t++;
        }
        e = e.nextSibling;
      }
      Je = null;
    }
  } else
    Je = tt ? dn(e.stateNode.nextSibling) : null;
  return !0;
}
function Gp() {
  for (var e = Je; e; )
    e = dn(e.nextSibling);
}
function Sr() {
  Je = tt = null, re = !1;
}
function Su(e) {
  _t === null ? _t = [e] : _t.push(e);
}
var cy = Yt.ReactCurrentBatchConfig;
function Vr(e, t, n) {
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
function ai(e, t) {
  throw e = Object.prototype.toString.call(t), Error(P(31, e === "[object Object]" ? "object with keys {" + Object.keys(t).join(", ") + "}" : e));
}
function ad(e) {
  var t = e._init;
  return t(e._payload);
}
function Kp(e) {
  function t(p, d) {
    if (e) {
      var h = p.deletions;
      h === null ? (p.deletions = [d], p.flags |= 16) : h.push(d);
    }
  }
  function n(p, d) {
    if (!e)
      return null;
    for (; d !== null; )
      t(p, d), d = d.sibling;
    return null;
  }
  function r(p, d) {
    for (p = /* @__PURE__ */ new Map(); d !== null; )
      d.key !== null ? p.set(d.key, d) : p.set(d.index, d), d = d.sibling;
    return p;
  }
  function o(p, d) {
    return p = hn(p, d), p.index = 0, p.sibling = null, p;
  }
  function i(p, d, h) {
    return p.index = h, e ? (h = p.alternate, h !== null ? (h = h.index, h < d ? (p.flags |= 2, d) : h) : (p.flags |= 2, d)) : (p.flags |= 1048576, d);
  }
  function l(p) {
    return e && p.alternate === null && (p.flags |= 2), p;
  }
  function s(p, d, h, x) {
    return d === null || d.tag !== 6 ? (d = Ls(h, p.mode, x), d.return = p, d) : (d = o(d, h), d.return = p, d);
  }
  function a(p, d, h, x) {
    var _ = h.type;
    return _ === qn ? c(p, d, h.props.children, x, h.key) : d !== null && (d.elementType === _ || typeof _ == "object" && _ !== null && _.$$typeof === en && ad(_) === d.type) ? (x = o(d, h.props), x.ref = Vr(p, d, h), x.return = p, x) : (x = Pi(h.type, h.key, h.props, null, p.mode, x), x.ref = Vr(p, d, h), x.return = p, x);
  }
  function u(p, d, h, x) {
    return d === null || d.tag !== 4 || d.stateNode.containerInfo !== h.containerInfo || d.stateNode.implementation !== h.implementation ? (d = zs(h, p.mode, x), d.return = p, d) : (d = o(d, h.children || []), d.return = p, d);
  }
  function c(p, d, h, x, _) {
    return d === null || d.tag !== 7 ? (d = Mn(h, p.mode, x, _), d.return = p, d) : (d = o(d, h), d.return = p, d);
  }
  function f(p, d, h) {
    if (typeof d == "string" && d !== "" || typeof d == "number")
      return d = Ls("" + d, p.mode, h), d.return = p, d;
    if (typeof d == "object" && d !== null) {
      switch (d.$$typeof) {
        case Zo:
          return h = Pi(d.type, d.key, d.props, null, p.mode, h), h.ref = Vr(p, null, d), h.return = p, h;
        case Zn:
          return d = zs(d, p.mode, h), d.return = p, d;
        case en:
          var x = d._init;
          return f(p, x(d._payload), h);
      }
      if (Zr(d) || Dr(d))
        return d = Mn(d, p.mode, h, null), d.return = p, d;
      ai(p, d);
    }
    return null;
  }
  function m(p, d, h, x) {
    var _ = d !== null ? d.key : null;
    if (typeof h == "string" && h !== "" || typeof h == "number")
      return _ !== null ? null : s(p, d, "" + h, x);
    if (typeof h == "object" && h !== null) {
      switch (h.$$typeof) {
        case Zo:
          return h.key === _ ? a(p, d, h, x) : null;
        case Zn:
          return h.key === _ ? u(p, d, h, x) : null;
        case en:
          return _ = h._init, m(
            p,
            d,
            _(h._payload),
            x
          );
      }
      if (Zr(h) || Dr(h))
        return _ !== null ? null : c(p, d, h, x, null);
      ai(p, h);
    }
    return null;
  }
  function v(p, d, h, x, _) {
    if (typeof x == "string" && x !== "" || typeof x == "number")
      return p = p.get(h) || null, s(d, p, "" + x, _);
    if (typeof x == "object" && x !== null) {
      switch (x.$$typeof) {
        case Zo:
          return p = p.get(x.key === null ? h : x.key) || null, a(d, p, x, _);
        case Zn:
          return p = p.get(x.key === null ? h : x.key) || null, u(d, p, x, _);
        case en:
          var E = x._init;
          return v(p, d, h, E(x._payload), _);
      }
      if (Zr(x) || Dr(x))
        return p = p.get(h) || null, c(d, p, x, _, null);
      ai(d, x);
    }
    return null;
  }
  function y(p, d, h, x) {
    for (var _ = null, E = null, k = d, R = d = 0, z = null; k !== null && R < h.length; R++) {
      k.index > R ? (z = k, k = null) : z = k.sibling;
      var O = m(p, k, h[R], x);
      if (O === null) {
        k === null && (k = z);
        break;
      }
      e && k && O.alternate === null && t(p, k), d = i(O, d, R), E === null ? _ = O : E.sibling = O, E = O, k = z;
    }
    if (R === h.length)
      return n(p, k), re && Cn(p, R), _;
    if (k === null) {
      for (; R < h.length; R++)
        k = f(p, h[R], x), k !== null && (d = i(k, d, R), E === null ? _ = k : E.sibling = k, E = k);
      return re && Cn(p, R), _;
    }
    for (k = r(p, k); R < h.length; R++)
      z = v(k, p, R, h[R], x), z !== null && (e && z.alternate !== null && k.delete(z.key === null ? R : z.key), d = i(z, d, R), E === null ? _ = z : E.sibling = z, E = z);
    return e && k.forEach(function(D) {
      return t(p, D);
    }), re && Cn(p, R), _;
  }
  function g(p, d, h, x) {
    var _ = Dr(h);
    if (typeof _ != "function")
      throw Error(P(150));
    if (h = _.call(h), h == null)
      throw Error(P(151));
    for (var E = _ = null, k = d, R = d = 0, z = null, O = h.next(); k !== null && !O.done; R++, O = h.next()) {
      k.index > R ? (z = k, k = null) : z = k.sibling;
      var D = m(p, k, O.value, x);
      if (D === null) {
        k === null && (k = z);
        break;
      }
      e && k && D.alternate === null && t(p, k), d = i(D, d, R), E === null ? _ = D : E.sibling = D, E = D, k = z;
    }
    if (O.done)
      return n(
        p,
        k
      ), re && Cn(p, R), _;
    if (k === null) {
      for (; !O.done; R++, O = h.next())
        O = f(p, O.value, x), O !== null && (d = i(O, d, R), E === null ? _ = O : E.sibling = O, E = O);
      return re && Cn(p, R), _;
    }
    for (k = r(p, k); !O.done; R++, O = h.next())
      O = v(k, p, R, O.value, x), O !== null && (e && O.alternate !== null && k.delete(O.key === null ? R : O.key), d = i(O, d, R), E === null ? _ = O : E.sibling = O, E = O);
    return e && k.forEach(function(F) {
      return t(p, F);
    }), re && Cn(p, R), _;
  }
  function $(p, d, h, x) {
    if (typeof h == "object" && h !== null && h.type === qn && h.key === null && (h = h.props.children), typeof h == "object" && h !== null) {
      switch (h.$$typeof) {
        case Zo:
          e: {
            for (var _ = h.key, E = d; E !== null; ) {
              if (E.key === _) {
                if (_ = h.type, _ === qn) {
                  if (E.tag === 7) {
                    n(p, E.sibling), d = o(E, h.props.children), d.return = p, p = d;
                    break e;
                  }
                } else if (E.elementType === _ || typeof _ == "object" && _ !== null && _.$$typeof === en && ad(_) === E.type) {
                  n(p, E.sibling), d = o(E, h.props), d.ref = Vr(p, E, h), d.return = p, p = d;
                  break e;
                }
                n(p, E);
                break;
              } else
                t(p, E);
              E = E.sibling;
            }
            h.type === qn ? (d = Mn(h.props.children, p.mode, x, h.key), d.return = p, p = d) : (x = Pi(h.type, h.key, h.props, null, p.mode, x), x.ref = Vr(p, d, h), x.return = p, p = x);
          }
          return l(p);
        case Zn:
          e: {
            for (E = h.key; d !== null; ) {
              if (d.key === E)
                if (d.tag === 4 && d.stateNode.containerInfo === h.containerInfo && d.stateNode.implementation === h.implementation) {
                  n(p, d.sibling), d = o(d, h.children || []), d.return = p, p = d;
                  break e;
                } else {
                  n(p, d);
                  break;
                }
              else
                t(p, d);
              d = d.sibling;
            }
            d = zs(h, p.mode, x), d.return = p, p = d;
          }
          return l(p);
        case en:
          return E = h._init, $(p, d, E(h._payload), x);
      }
      if (Zr(h))
        return y(p, d, h, x);
      if (Dr(h))
        return g(p, d, h, x);
      ai(p, h);
    }
    return typeof h == "string" && h !== "" || typeof h == "number" ? (h = "" + h, d !== null && d.tag === 6 ? (n(p, d.sibling), d = o(d, h), d.return = p, p = d) : (n(p, d), d = Ls(h, p.mode, x), d.return = p, p = d), l(p)) : n(p, d);
  }
  return $;
}
var wr = Kp(!0), Qp = Kp(!1), Gi = Sn(null), Ki = null, lr = null, wu = null;
function Cu() {
  wu = lr = Ki = null;
}
function ku(e) {
  var t = Gi.current;
  ee(Gi), e._currentValue = t;
}
function Ca(e, t, n) {
  for (; e !== null; ) {
    var r = e.alternate;
    if ((e.childLanes & t) !== t ? (e.childLanes |= t, r !== null && (r.childLanes |= t)) : r !== null && (r.childLanes & t) !== t && (r.childLanes |= t), e === n)
      break;
    e = e.return;
  }
}
function pr(e, t) {
  Ki = e, wu = lr = null, e = e.dependencies, e !== null && e.firstContext !== null && (e.lanes & t && (He = !0), e.firstContext = null);
}
function ht(e) {
  var t = e._currentValue;
  if (wu !== e)
    if (e = { context: e, memoizedValue: t, next: null }, lr === null) {
      if (Ki === null)
        throw Error(P(308));
      lr = e, Ki.dependencies = { lanes: 0, firstContext: e };
    } else
      lr = lr.next = e;
  return t;
}
var Pn = null;
function Eu(e) {
  Pn === null ? Pn = [e] : Pn.push(e);
}
function Yp(e, t, n, r) {
  var o = t.interleaved;
  return o === null ? (n.next = n, Eu(t)) : (n.next = o.next, o.next = n), t.interleaved = n, Gt(e, r);
}
function Gt(e, t) {
  e.lanes |= t;
  var n = e.alternate;
  for (n !== null && (n.lanes |= t), n = e, e = e.return; e !== null; )
    e.childLanes |= t, n = e.alternate, n !== null && (n.childLanes |= t), n = e, e = e.return;
  return n.tag === 3 ? n.stateNode : null;
}
var tn = !1;
function _u(e) {
  e.updateQueue = { baseState: e.memoizedState, firstBaseUpdate: null, lastBaseUpdate: null, shared: { pending: null, interleaved: null, lanes: 0 }, effects: null };
}
function Xp(e, t) {
  e = e.updateQueue, t.updateQueue === e && (t.updateQueue = { baseState: e.baseState, firstBaseUpdate: e.firstBaseUpdate, lastBaseUpdate: e.lastBaseUpdate, shared: e.shared, effects: e.effects });
}
function Wt(e, t) {
  return { eventTime: e, lane: t, tag: 0, payload: null, callback: null, next: null };
}
function fn(e, t, n) {
  var r = e.updateQueue;
  if (r === null)
    return null;
  if (r = r.shared, W & 2) {
    var o = r.pending;
    return o === null ? t.next = t : (t.next = o.next, o.next = t), r.pending = t, Gt(e, n);
  }
  return o = r.interleaved, o === null ? (t.next = t, Eu(r)) : (t.next = o.next, o.next = t), r.interleaved = t, Gt(e, n);
}
function wi(e, t, n) {
  if (t = t.updateQueue, t !== null && (t = t.shared, (n & 4194240) !== 0)) {
    var r = t.lanes;
    r &= e.pendingLanes, n |= r, t.lanes = n, cu(e, n);
  }
}
function ud(e, t) {
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
  tn = !1;
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
      var m = s.lane, v = s.eventTime;
      if ((r & m) === m) {
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
          switch (m = t, v = n, g.tag) {
            case 1:
              if (y = g.payload, typeof y == "function") {
                f = y.call(v, f, m);
                break e;
              }
              f = y;
              break e;
            case 3:
              y.flags = y.flags & -65537 | 128;
            case 0:
              if (y = g.payload, m = typeof y == "function" ? y.call(v, f, m) : y, m == null)
                break e;
              f = se({}, f, m);
              break e;
            case 2:
              tn = !0;
          }
        }
        s.callback !== null && s.lane !== 0 && (e.flags |= 64, m = o.effects, m === null ? o.effects = [s] : m.push(s));
      } else
        v = { eventTime: v, lane: m, tag: s.tag, payload: s.payload, callback: s.callback, next: null }, c === null ? (u = c = v, a = f) : c = c.next = v, l |= m;
      if (s = s.next, s === null) {
        if (s = o.shared.pending, s === null)
          break;
        m = s, s = m.next, m.next = null, o.lastBaseUpdate = m, o.shared.pending = null;
      }
    } while (1);
    if (c === null && (a = f), o.baseState = a, o.firstBaseUpdate = u, o.lastBaseUpdate = c, t = o.shared.interleaved, t !== null) {
      o = t;
      do
        l |= o.lane, o = o.next;
      while (o !== t);
    } else
      i === null && (o.shared.lanes = 0);
    zn |= l, e.lanes = l, e.memoizedState = f;
  }
}
function cd(e, t, n) {
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
var Fo = {}, bt = Sn(Fo), Eo = Sn(Fo), _o = Sn(Fo);
function Tn(e) {
  if (e === Fo)
    throw Error(P(174));
  return e;
}
function $u(e, t) {
  switch (q(_o, t), q(Eo, e), q(bt, Fo), e = t.nodeType, e) {
    case 9:
    case 11:
      t = (t = t.documentElement) ? t.namespaceURI : na(null, "");
      break;
    default:
      e = e === 8 ? t.parentNode : t, t = e.namespaceURI || null, e = e.tagName, t = na(t, e);
  }
  ee(bt), q(bt, t);
}
function Cr() {
  ee(bt), ee(Eo), ee(_o);
}
function Zp(e) {
  Tn(_o.current);
  var t = Tn(bt.current), n = na(t, e.type);
  t !== n && (q(Eo, e), q(bt, n));
}
function Pu(e) {
  Eo.current === e && (ee(bt), ee(Eo));
}
var oe = Sn(0);
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
var Ts = [];
function Tu() {
  for (var e = 0; e < Ts.length; e++)
    Ts[e]._workInProgressVersionPrimary = null;
  Ts.length = 0;
}
var Ci = Yt.ReactCurrentDispatcher, Rs = Yt.ReactCurrentBatchConfig, Ln = 0, ie = null, Se = null, Ee = null, Xi = !1, so = !1, $o = 0, dy = 0;
function Le() {
  throw Error(P(321));
}
function Ru(e, t) {
  if (t === null)
    return !1;
  for (var n = 0; n < t.length && n < e.length; n++)
    if (!Tt(e[n], t[n]))
      return !1;
  return !0;
}
function Ou(e, t, n, r, o, i) {
  if (Ln = i, ie = t, t.memoizedState = null, t.updateQueue = null, t.lanes = 0, Ci.current = e === null || e.memoizedState === null ? hy : gy, e = n(r, o), so) {
    i = 0;
    do {
      if (so = !1, $o = 0, 25 <= i)
        throw Error(P(301));
      i += 1, Ee = Se = null, t.updateQueue = null, Ci.current = yy, e = n(r, o);
    } while (so);
  }
  if (Ci.current = Zi, t = Se !== null && Se.next !== null, Ln = 0, Ee = Se = ie = null, Xi = !1, t)
    throw Error(P(300));
  return e;
}
function Mu() {
  var e = $o !== 0;
  return $o = 0, e;
}
function Mt() {
  var e = { memoizedState: null, baseState: null, baseQueue: null, queue: null, next: null };
  return Ee === null ? ie.memoizedState = Ee = e : Ee = Ee.next = e, Ee;
}
function gt() {
  if (Se === null) {
    var e = ie.alternate;
    e = e !== null ? e.memoizedState : null;
  } else
    e = Se.next;
  var t = Ee === null ? ie.memoizedState : Ee.next;
  if (t !== null)
    Ee = t, Se = e;
  else {
    if (e === null)
      throw Error(P(310));
    Se = e, e = { memoizedState: Se.memoizedState, baseState: Se.baseState, baseQueue: Se.baseQueue, queue: Se.queue, next: null }, Ee === null ? ie.memoizedState = Ee = e : Ee = Ee.next = e;
  }
  return Ee;
}
function Po(e, t) {
  return typeof t == "function" ? t(e) : t;
}
function Os(e) {
  var t = gt(), n = t.queue;
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
      if ((Ln & c) === c)
        a !== null && (a = a.next = { lane: 0, action: u.action, hasEagerState: u.hasEagerState, eagerState: u.eagerState, next: null }), r = u.hasEagerState ? u.eagerState : e(r, u.action);
      else {
        var f = {
          lane: c,
          action: u.action,
          hasEagerState: u.hasEagerState,
          eagerState: u.eagerState,
          next: null
        };
        a === null ? (s = a = f, l = r) : a = a.next = f, ie.lanes |= c, zn |= c;
      }
      u = u.next;
    } while (u !== null && u !== i);
    a === null ? l = r : a.next = s, Tt(r, t.memoizedState) || (He = !0), t.memoizedState = r, t.baseState = l, t.baseQueue = a, n.lastRenderedState = r;
  }
  if (e = n.interleaved, e !== null) {
    o = e;
    do
      i = o.lane, ie.lanes |= i, zn |= i, o = o.next;
    while (o !== e);
  } else
    o === null && (n.lanes = 0);
  return [t.memoizedState, n.dispatch];
}
function Ms(e) {
  var t = gt(), n = t.queue;
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
    Tt(i, t.memoizedState) || (He = !0), t.memoizedState = i, t.baseQueue === null && (t.baseState = i), n.lastRenderedState = i;
  }
  return [i, r];
}
function qp() {
}
function Jp(e, t) {
  var n = ie, r = gt(), o = t(), i = !Tt(r.memoizedState, o);
  if (i && (r.memoizedState = o, He = !0), r = r.queue, Nu(nm.bind(null, n, r, e), [e]), r.getSnapshot !== t || i || Ee !== null && Ee.memoizedState.tag & 1) {
    if (n.flags |= 2048, To(9, tm.bind(null, n, r, o, t), void 0, null), _e === null)
      throw Error(P(349));
    Ln & 30 || em(n, t, o);
  }
  return o;
}
function em(e, t, n) {
  e.flags |= 16384, e = { getSnapshot: t, value: n }, t = ie.updateQueue, t === null ? (t = { lastEffect: null, stores: null }, ie.updateQueue = t, t.stores = [e]) : (n = t.stores, n === null ? t.stores = [e] : n.push(e));
}
function tm(e, t, n, r) {
  t.value = n, t.getSnapshot = r, rm(t) && om(e);
}
function nm(e, t, n) {
  return n(function() {
    rm(t) && om(e);
  });
}
function rm(e) {
  var t = e.getSnapshot;
  e = e.value;
  try {
    var n = t();
    return !Tt(e, n);
  } catch {
    return !0;
  }
}
function om(e) {
  var t = Gt(e, 1);
  t !== null && Pt(t, e, 1, -1);
}
function dd(e) {
  var t = Mt();
  return typeof e == "function" && (e = e()), t.memoizedState = t.baseState = e, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: Po, lastRenderedState: e }, t.queue = e, e = e.dispatch = my.bind(null, ie, e), [t.memoizedState, e];
}
function To(e, t, n, r) {
  return e = { tag: e, create: t, destroy: n, deps: r, next: null }, t = ie.updateQueue, t === null ? (t = { lastEffect: null, stores: null }, ie.updateQueue = t, t.lastEffect = e.next = e) : (n = t.lastEffect, n === null ? t.lastEffect = e.next = e : (r = n.next, n.next = e, e.next = r, t.lastEffect = e)), e;
}
function im() {
  return gt().memoizedState;
}
function ki(e, t, n, r) {
  var o = Mt();
  ie.flags |= e, o.memoizedState = To(1 | t, n, void 0, r === void 0 ? null : r);
}
function hl(e, t, n, r) {
  var o = gt();
  r = r === void 0 ? null : r;
  var i = void 0;
  if (Se !== null) {
    var l = Se.memoizedState;
    if (i = l.destroy, r !== null && Ru(r, l.deps)) {
      o.memoizedState = To(t, n, i, r);
      return;
    }
  }
  ie.flags |= e, o.memoizedState = To(1 | t, n, i, r);
}
function fd(e, t) {
  return ki(8390656, 8, e, t);
}
function Nu(e, t) {
  return hl(2048, 8, e, t);
}
function lm(e, t) {
  return hl(4, 2, e, t);
}
function sm(e, t) {
  return hl(4, 4, e, t);
}
function am(e, t) {
  if (typeof t == "function")
    return e = e(), t(e), function() {
      t(null);
    };
  if (t != null)
    return e = e(), t.current = e, function() {
      t.current = null;
    };
}
function um(e, t, n) {
  return n = n != null ? n.concat([e]) : null, hl(4, 4, am.bind(null, t, e), n);
}
function Iu() {
}
function cm(e, t) {
  var n = gt();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && Ru(t, r[1]) ? r[0] : (n.memoizedState = [e, t], e);
}
function dm(e, t) {
  var n = gt();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && Ru(t, r[1]) ? r[0] : (e = e(), n.memoizedState = [e, t], e);
}
function fm(e, t, n) {
  return Ln & 21 ? (Tt(n, t) || (n = yp(), ie.lanes |= n, zn |= n, e.baseState = !0), t) : (e.baseState && (e.baseState = !1, He = !0), e.memoizedState = n);
}
function fy(e, t) {
  var n = K;
  K = n !== 0 && 4 > n ? n : 4, e(!0);
  var r = Rs.transition;
  Rs.transition = {};
  try {
    e(!1), t();
  } finally {
    K = n, Rs.transition = r;
  }
}
function pm() {
  return gt().memoizedState;
}
function py(e, t, n) {
  var r = mn(e);
  if (n = { lane: r, action: n, hasEagerState: !1, eagerState: null, next: null }, mm(e))
    hm(t, n);
  else if (n = Yp(e, t, n, r), n !== null) {
    var o = Be();
    Pt(n, e, r, o), gm(n, t, r);
  }
}
function my(e, t, n) {
  var r = mn(e), o = { lane: r, action: n, hasEagerState: !1, eagerState: null, next: null };
  if (mm(e))
    hm(t, o);
  else {
    var i = e.alternate;
    if (e.lanes === 0 && (i === null || i.lanes === 0) && (i = t.lastRenderedReducer, i !== null))
      try {
        var l = t.lastRenderedState, s = i(l, n);
        if (o.hasEagerState = !0, o.eagerState = s, Tt(s, l)) {
          var a = t.interleaved;
          a === null ? (o.next = o, Eu(t)) : (o.next = a.next, a.next = o), t.interleaved = o;
          return;
        }
      } catch {
      } finally {
      }
    n = Yp(e, t, o, r), n !== null && (o = Be(), Pt(n, e, r, o), gm(n, t, r));
  }
}
function mm(e) {
  var t = e.alternate;
  return e === ie || t !== null && t === ie;
}
function hm(e, t) {
  so = Xi = !0;
  var n = e.pending;
  n === null ? t.next = t : (t.next = n.next, n.next = t), e.pending = t;
}
function gm(e, t, n) {
  if (n & 4194240) {
    var r = t.lanes;
    r &= e.pendingLanes, n |= r, t.lanes = n, cu(e, n);
  }
}
var Zi = { readContext: ht, useCallback: Le, useContext: Le, useEffect: Le, useImperativeHandle: Le, useInsertionEffect: Le, useLayoutEffect: Le, useMemo: Le, useReducer: Le, useRef: Le, useState: Le, useDebugValue: Le, useDeferredValue: Le, useTransition: Le, useMutableSource: Le, useSyncExternalStore: Le, useId: Le, unstable_isNewReconciler: !1 }, hy = { readContext: ht, useCallback: function(e, t) {
  return Mt().memoizedState = [e, t === void 0 ? null : t], e;
}, useContext: ht, useEffect: fd, useImperativeHandle: function(e, t, n) {
  return n = n != null ? n.concat([e]) : null, ki(
    4194308,
    4,
    am.bind(null, t, e),
    n
  );
}, useLayoutEffect: function(e, t) {
  return ki(4194308, 4, e, t);
}, useInsertionEffect: function(e, t) {
  return ki(4, 2, e, t);
}, useMemo: function(e, t) {
  var n = Mt();
  return t = t === void 0 ? null : t, e = e(), n.memoizedState = [e, t], e;
}, useReducer: function(e, t, n) {
  var r = Mt();
  return t = n !== void 0 ? n(t) : t, r.memoizedState = r.baseState = t, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: e, lastRenderedState: t }, r.queue = e, e = e.dispatch = py.bind(null, ie, e), [r.memoizedState, e];
}, useRef: function(e) {
  var t = Mt();
  return e = { current: e }, t.memoizedState = e;
}, useState: dd, useDebugValue: Iu, useDeferredValue: function(e) {
  return Mt().memoizedState = e;
}, useTransition: function() {
  var e = dd(!1), t = e[0];
  return e = fy.bind(null, e[1]), Mt().memoizedState = e, [t, e];
}, useMutableSource: function() {
}, useSyncExternalStore: function(e, t, n) {
  var r = ie, o = Mt();
  if (re) {
    if (n === void 0)
      throw Error(P(407));
    n = n();
  } else {
    if (n = t(), _e === null)
      throw Error(P(349));
    Ln & 30 || em(r, t, n);
  }
  o.memoizedState = n;
  var i = { value: n, getSnapshot: t };
  return o.queue = i, fd(nm.bind(
    null,
    r,
    i,
    e
  ), [e]), r.flags |= 2048, To(9, tm.bind(null, r, i, n, t), void 0, null), n;
}, useId: function() {
  var e = Mt(), t = _e.identifierPrefix;
  if (re) {
    var n = Ut, r = Bt;
    n = (r & ~(1 << 32 - $t(r) - 1)).toString(32) + n, t = ":" + t + "R" + n, n = $o++, 0 < n && (t += "H" + n.toString(32)), t += ":";
  } else
    n = dy++, t = ":" + t + "r" + n.toString(32) + ":";
  return e.memoizedState = t;
}, unstable_isNewReconciler: !1 }, gy = {
  readContext: ht,
  useCallback: cm,
  useContext: ht,
  useEffect: Nu,
  useImperativeHandle: um,
  useInsertionEffect: lm,
  useLayoutEffect: sm,
  useMemo: dm,
  useReducer: Os,
  useRef: im,
  useState: function() {
    return Os(Po);
  },
  useDebugValue: Iu,
  useDeferredValue: function(e) {
    var t = gt();
    return fm(t, Se.memoizedState, e);
  },
  useTransition: function() {
    var e = Os(Po)[0], t = gt().memoizedState;
    return [e, t];
  },
  useMutableSource: qp,
  useSyncExternalStore: Jp,
  useId: pm,
  unstable_isNewReconciler: !1
}, yy = { readContext: ht, useCallback: cm, useContext: ht, useEffect: Nu, useImperativeHandle: um, useInsertionEffect: lm, useLayoutEffect: sm, useMemo: dm, useReducer: Ms, useRef: im, useState: function() {
  return Ms(Po);
}, useDebugValue: Iu, useDeferredValue: function(e) {
  var t = gt();
  return Se === null ? t.memoizedState = e : fm(t, Se.memoizedState, e);
}, useTransition: function() {
  var e = Ms(Po)[0], t = gt().memoizedState;
  return [e, t];
}, useMutableSource: qp, useSyncExternalStore: Jp, useId: pm, unstable_isNewReconciler: !1 };
function kt(e, t) {
  if (e && e.defaultProps) {
    t = se({}, t), e = e.defaultProps;
    for (var n in e)
      t[n] === void 0 && (t[n] = e[n]);
    return t;
  }
  return t;
}
function ka(e, t, n, r) {
  t = e.memoizedState, n = n(r, t), n = n == null ? t : se({}, t, n), e.memoizedState = n, e.lanes === 0 && (e.updateQueue.baseState = n);
}
var gl = { isMounted: function(e) {
  return (e = e._reactInternals) ? Dn(e) === e : !1;
}, enqueueSetState: function(e, t, n) {
  e = e._reactInternals;
  var r = Be(), o = mn(e), i = Wt(r, o);
  i.payload = t, n != null && (i.callback = n), t = fn(e, i, o), t !== null && (Pt(t, e, o, r), wi(t, e, o));
}, enqueueReplaceState: function(e, t, n) {
  e = e._reactInternals;
  var r = Be(), o = mn(e), i = Wt(r, o);
  i.tag = 1, i.payload = t, n != null && (i.callback = n), t = fn(e, i, o), t !== null && (Pt(t, e, o, r), wi(t, e, o));
}, enqueueForceUpdate: function(e, t) {
  e = e._reactInternals;
  var n = Be(), r = mn(e), o = Wt(n, r);
  o.tag = 2, t != null && (o.callback = t), t = fn(e, o, r), t !== null && (Pt(t, e, r, n), wi(t, e, r));
} };
function pd(e, t, n, r, o, i, l) {
  return e = e.stateNode, typeof e.shouldComponentUpdate == "function" ? e.shouldComponentUpdate(r, i, l) : t.prototype && t.prototype.isPureReactComponent ? !So(n, r) || !So(o, i) : !0;
}
function ym(e, t, n) {
  var r = !1, o = vn, i = t.contextType;
  return typeof i == "object" && i !== null ? i = ht(i) : (o = Ke(t) ? Nn : Ae.current, r = t.contextTypes, i = (r = r != null) ? xr(e, o) : vn), t = new t(n, i), e.memoizedState = t.state !== null && t.state !== void 0 ? t.state : null, t.updater = gl, e.stateNode = t, t._reactInternals = e, r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = o, e.__reactInternalMemoizedMaskedChildContext = i), t;
}
function md(e, t, n, r) {
  e = t.state, typeof t.componentWillReceiveProps == "function" && t.componentWillReceiveProps(n, r), typeof t.UNSAFE_componentWillReceiveProps == "function" && t.UNSAFE_componentWillReceiveProps(n, r), t.state !== e && gl.enqueueReplaceState(t, t.state, null);
}
function Ea(e, t, n, r) {
  var o = e.stateNode;
  o.props = n, o.state = e.memoizedState, o.refs = {}, _u(e);
  var i = t.contextType;
  typeof i == "object" && i !== null ? o.context = ht(i) : (i = Ke(t) ? Nn : Ae.current, o.context = xr(e, i)), o.state = e.memoizedState, i = t.getDerivedStateFromProps, typeof i == "function" && (ka(e, t, i, n), o.state = e.memoizedState), typeof t.getDerivedStateFromProps == "function" || typeof o.getSnapshotBeforeUpdate == "function" || typeof o.UNSAFE_componentWillMount != "function" && typeof o.componentWillMount != "function" || (t = o.state, typeof o.componentWillMount == "function" && o.componentWillMount(), typeof o.UNSAFE_componentWillMount == "function" && o.UNSAFE_componentWillMount(), t !== o.state && gl.enqueueReplaceState(o, o.state, null), Qi(e, n, o, r), o.state = e.memoizedState), typeof o.componentDidMount == "function" && (e.flags |= 4194308);
}
function kr(e, t) {
  try {
    var n = "", r = t;
    do
      n += H0(r), r = r.return;
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
function _a(e, t) {
  try {
    console.error(t.value);
  } catch (n) {
    setTimeout(function() {
      throw n;
    });
  }
}
var vy = typeof WeakMap == "function" ? WeakMap : Map;
function vm(e, t, n) {
  n = Wt(-1, n), n.tag = 3, n.payload = { element: null };
  var r = t.value;
  return n.callback = function() {
    Ji || (Ji = !0, za = r), _a(e, t);
  }, n;
}
function xm(e, t, n) {
  n = Wt(-1, n), n.tag = 3;
  var r = e.type.getDerivedStateFromError;
  if (typeof r == "function") {
    var o = t.value;
    n.payload = function() {
      return r(o);
    }, n.callback = function() {
      _a(e, t);
    };
  }
  var i = e.stateNode;
  return i !== null && typeof i.componentDidCatch == "function" && (n.callback = function() {
    _a(e, t), typeof r != "function" && (pn === null ? pn = /* @__PURE__ */ new Set([this]) : pn.add(this));
    var l = t.stack;
    this.componentDidCatch(t.value, { componentStack: l !== null ? l : "" });
  }), n;
}
function hd(e, t, n) {
  var r = e.pingCache;
  if (r === null) {
    r = e.pingCache = new vy();
    var o = /* @__PURE__ */ new Set();
    r.set(t, o);
  } else
    o = r.get(t), o === void 0 && (o = /* @__PURE__ */ new Set(), r.set(t, o));
  o.has(n) || (o.add(n), e = Ny.bind(null, e, t, n), t.then(e, e));
}
function gd(e) {
  do {
    var t;
    if ((t = e.tag === 13) && (t = e.memoizedState, t = t !== null ? t.dehydrated !== null : !0), t)
      return e;
    e = e.return;
  } while (e !== null);
  return null;
}
function yd(e, t, n, r, o) {
  return e.mode & 1 ? (e.flags |= 65536, e.lanes = o, e) : (e === t ? e.flags |= 65536 : (e.flags |= 128, n.flags |= 131072, n.flags &= -52805, n.tag === 1 && (n.alternate === null ? n.tag = 17 : (t = Wt(-1, 1), t.tag = 2, fn(n, t, 1))), n.lanes |= 1), e);
}
var xy = Yt.ReactCurrentOwner, He = !1;
function Fe(e, t, n, r) {
  t.child = e === null ? Qp(t, null, n, r) : wr(t, e.child, n, r);
}
function vd(e, t, n, r, o) {
  n = n.render;
  var i = t.ref;
  return pr(t, o), r = Ou(e, t, n, r, i, o), n = Mu(), e !== null && !He ? (t.updateQueue = e.updateQueue, t.flags &= -2053, e.lanes &= ~o, Kt(e, t, o)) : (re && n && vu(t), t.flags |= 1, Fe(e, t, r, o), t.child);
}
function xd(e, t, n, r, o) {
  if (e === null) {
    var i = n.type;
    return typeof i == "function" && !Bu(i) && i.defaultProps === void 0 && n.compare === null && n.defaultProps === void 0 ? (t.tag = 15, t.type = i, Sm(e, t, i, r, o)) : (e = Pi(n.type, null, r, t, t.mode, o), e.ref = t.ref, e.return = t, t.child = e);
  }
  if (i = e.child, !(e.lanes & o)) {
    var l = i.memoizedProps;
    if (n = n.compare, n = n !== null ? n : So, n(l, r) && e.ref === t.ref)
      return Kt(e, t, o);
  }
  return t.flags |= 1, e = hn(i, r), e.ref = t.ref, e.return = t, t.child = e;
}
function Sm(e, t, n, r, o) {
  if (e !== null) {
    var i = e.memoizedProps;
    if (So(i, r) && e.ref === t.ref)
      if (He = !1, t.pendingProps = r = i, (e.lanes & o) !== 0)
        e.flags & 131072 && (He = !0);
      else
        return t.lanes = e.lanes, Kt(e, t, o);
  }
  return $a(e, t, n, r, o);
}
function wm(e, t, n) {
  var r = t.pendingProps, o = r.children, i = e !== null ? e.memoizedState : null;
  if (r.mode === "hidden")
    if (!(t.mode & 1))
      t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, q(ar, Xe), Xe |= n;
    else {
      if (!(n & 1073741824))
        return e = i !== null ? i.baseLanes | n : n, t.lanes = t.childLanes = 1073741824, t.memoizedState = { baseLanes: e, cachePool: null, transitions: null }, t.updateQueue = null, q(ar, Xe), Xe |= e, null;
      t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, r = i !== null ? i.baseLanes : n, q(ar, Xe), Xe |= r;
    }
  else
    i !== null ? (r = i.baseLanes | n, t.memoizedState = null) : r = n, q(ar, Xe), Xe |= r;
  return Fe(e, t, o, n), t.child;
}
function Cm(e, t) {
  var n = t.ref;
  (e === null && n !== null || e !== null && e.ref !== n) && (t.flags |= 512, t.flags |= 2097152);
}
function $a(e, t, n, r, o) {
  var i = Ke(n) ? Nn : Ae.current;
  return i = xr(t, i), pr(t, o), n = Ou(e, t, n, r, i, o), r = Mu(), e !== null && !He ? (t.updateQueue = e.updateQueue, t.flags &= -2053, e.lanes &= ~o, Kt(e, t, o)) : (re && r && vu(t), t.flags |= 1, Fe(e, t, n, o), t.child);
}
function Sd(e, t, n, r, o) {
  if (Ke(n)) {
    var i = !0;
    Wi(t);
  } else
    i = !1;
  if (pr(t, o), t.stateNode === null)
    Ei(e, t), ym(t, n, r), Ea(t, n, r, o), r = !0;
  else if (e === null) {
    var l = t.stateNode, s = t.memoizedProps;
    l.props = s;
    var a = l.context, u = n.contextType;
    typeof u == "object" && u !== null ? u = ht(u) : (u = Ke(n) ? Nn : Ae.current, u = xr(t, u));
    var c = n.getDerivedStateFromProps, f = typeof c == "function" || typeof l.getSnapshotBeforeUpdate == "function";
    f || typeof l.UNSAFE_componentWillReceiveProps != "function" && typeof l.componentWillReceiveProps != "function" || (s !== r || a !== u) && md(t, l, r, u), tn = !1;
    var m = t.memoizedState;
    l.state = m, Qi(t, r, l, o), a = t.memoizedState, s !== r || m !== a || Ge.current || tn ? (typeof c == "function" && (ka(t, n, c, r), a = t.memoizedState), (s = tn || pd(t, n, s, r, m, a, u)) ? (f || typeof l.UNSAFE_componentWillMount != "function" && typeof l.componentWillMount != "function" || (typeof l.componentWillMount == "function" && l.componentWillMount(), typeof l.UNSAFE_componentWillMount == "function" && l.UNSAFE_componentWillMount()), typeof l.componentDidMount == "function" && (t.flags |= 4194308)) : (typeof l.componentDidMount == "function" && (t.flags |= 4194308), t.memoizedProps = r, t.memoizedState = a), l.props = r, l.state = a, l.context = u, r = s) : (typeof l.componentDidMount == "function" && (t.flags |= 4194308), r = !1);
  } else {
    l = t.stateNode, Xp(e, t), s = t.memoizedProps, u = t.type === t.elementType ? s : kt(t.type, s), l.props = u, f = t.pendingProps, m = l.context, a = n.contextType, typeof a == "object" && a !== null ? a = ht(a) : (a = Ke(n) ? Nn : Ae.current, a = xr(t, a));
    var v = n.getDerivedStateFromProps;
    (c = typeof v == "function" || typeof l.getSnapshotBeforeUpdate == "function") || typeof l.UNSAFE_componentWillReceiveProps != "function" && typeof l.componentWillReceiveProps != "function" || (s !== f || m !== a) && md(t, l, r, a), tn = !1, m = t.memoizedState, l.state = m, Qi(t, r, l, o);
    var y = t.memoizedState;
    s !== f || m !== y || Ge.current || tn ? (typeof v == "function" && (ka(t, n, v, r), y = t.memoizedState), (u = tn || pd(t, n, u, r, m, y, a) || !1) ? (c || typeof l.UNSAFE_componentWillUpdate != "function" && typeof l.componentWillUpdate != "function" || (typeof l.componentWillUpdate == "function" && l.componentWillUpdate(r, y, a), typeof l.UNSAFE_componentWillUpdate == "function" && l.UNSAFE_componentWillUpdate(r, y, a)), typeof l.componentDidUpdate == "function" && (t.flags |= 4), typeof l.getSnapshotBeforeUpdate == "function" && (t.flags |= 1024)) : (typeof l.componentDidUpdate != "function" || s === e.memoizedProps && m === e.memoizedState || (t.flags |= 4), typeof l.getSnapshotBeforeUpdate != "function" || s === e.memoizedProps && m === e.memoizedState || (t.flags |= 1024), t.memoizedProps = r, t.memoizedState = y), l.props = r, l.state = y, l.context = a, r = u) : (typeof l.componentDidUpdate != "function" || s === e.memoizedProps && m === e.memoizedState || (t.flags |= 4), typeof l.getSnapshotBeforeUpdate != "function" || s === e.memoizedProps && m === e.memoizedState || (t.flags |= 1024), r = !1);
  }
  return Pa(e, t, n, r, i, o);
}
function Pa(e, t, n, r, o, i) {
  Cm(e, t);
  var l = (t.flags & 128) !== 0;
  if (!r && !l)
    return o && id(t, n, !1), Kt(e, t, i);
  r = t.stateNode, xy.current = t;
  var s = l && typeof n.getDerivedStateFromError != "function" ? null : r.render();
  return t.flags |= 1, e !== null && l ? (t.child = wr(t, e.child, null, i), t.child = wr(t, null, s, i)) : Fe(e, t, s, i), t.memoizedState = r.state, o && id(t, n, !0), t.child;
}
function km(e) {
  var t = e.stateNode;
  t.pendingContext ? od(e, t.pendingContext, t.pendingContext !== t.context) : t.context && od(e, t.context, !1), $u(e, t.containerInfo);
}
function wd(e, t, n, r, o) {
  return Sr(), Su(o), t.flags |= 256, Fe(e, t, n, r), t.child;
}
var Ta = { dehydrated: null, treeContext: null, retryLane: 0 };
function Ra(e) {
  return { baseLanes: e, cachePool: null, transitions: null };
}
function Em(e, t, n) {
  var r = t.pendingProps, o = oe.current, i = !1, l = (t.flags & 128) !== 0, s;
  if ((s = l) || (s = e !== null && e.memoizedState === null ? !1 : (o & 2) !== 0), s ? (i = !0, t.flags &= -129) : (e === null || e.memoizedState !== null) && (o |= 1), q(oe, o & 1), e === null)
    return wa(t), e = t.memoizedState, e !== null && (e = e.dehydrated, e !== null) ? (t.mode & 1 ? e.data === "$!" ? t.lanes = 8 : t.lanes = 1073741824 : t.lanes = 1, null) : (l = r.children, e = r.fallback, i ? (r = t.mode, i = t.child, l = { mode: "hidden", children: l }, !(r & 1) && i !== null ? (i.childLanes = 0, i.pendingProps = l) : i = xl(l, r, 0, null), e = Mn(e, r, n, null), i.return = t, e.return = t, i.sibling = e, t.child = i, t.child.memoizedState = Ra(n), t.memoizedState = Ta, e) : Lu(t, l));
  if (o = e.memoizedState, o !== null && (s = o.dehydrated, s !== null))
    return Sy(e, t, l, r, s, o, n);
  if (i) {
    i = r.fallback, l = t.mode, o = e.child, s = o.sibling;
    var a = { mode: "hidden", children: r.children };
    return !(l & 1) && t.child !== o ? (r = t.child, r.childLanes = 0, r.pendingProps = a, t.deletions = null) : (r = hn(o, a), r.subtreeFlags = o.subtreeFlags & 14680064), s !== null ? i = hn(s, i) : (i = Mn(i, l, n, null), i.flags |= 2), i.return = t, r.return = t, r.sibling = i, t.child = r, r = i, i = t.child, l = e.child.memoizedState, l = l === null ? Ra(n) : { baseLanes: l.baseLanes | n, cachePool: null, transitions: l.transitions }, i.memoizedState = l, i.childLanes = e.childLanes & ~n, t.memoizedState = Ta, r;
  }
  return i = e.child, e = i.sibling, r = hn(i, { mode: "visible", children: r.children }), !(t.mode & 1) && (r.lanes = n), r.return = t, r.sibling = null, e !== null && (n = t.deletions, n === null ? (t.deletions = [e], t.flags |= 16) : n.push(e)), t.child = r, t.memoizedState = null, r;
}
function Lu(e, t) {
  return t = xl({ mode: "visible", children: t }, e.mode, 0, null), t.return = e, e.child = t;
}
function ui(e, t, n, r) {
  return r !== null && Su(r), wr(t, e.child, null, n), e = Lu(t, t.pendingProps.children), e.flags |= 2, t.memoizedState = null, e;
}
function Sy(e, t, n, r, o, i, l) {
  if (n)
    return t.flags & 256 ? (t.flags &= -257, r = Ns(Error(P(422))), ui(e, t, l, r)) : t.memoizedState !== null ? (t.child = e.child, t.flags |= 128, null) : (i = r.fallback, o = t.mode, r = xl({ mode: "visible", children: r.children }, o, 0, null), i = Mn(i, o, l, null), i.flags |= 2, r.return = t, i.return = t, r.sibling = i, t.child = r, t.mode & 1 && wr(t, e.child, null, l), t.child.memoizedState = Ra(l), t.memoizedState = Ta, i);
  if (!(t.mode & 1))
    return ui(e, t, l, null);
  if (o.data === "$!") {
    if (r = o.nextSibling && o.nextSibling.dataset, r)
      var s = r.dgst;
    return r = s, i = Error(P(419)), r = Ns(i, r, void 0), ui(e, t, l, r);
  }
  if (s = (l & e.childLanes) !== 0, He || s) {
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
      o = o & (r.suspendedLanes | l) ? 0 : o, o !== 0 && o !== i.retryLane && (i.retryLane = o, Gt(e, o), Pt(r, e, o, -1));
    }
    return Fu(), r = Ns(Error(P(421))), ui(e, t, l, r);
  }
  return o.data === "$?" ? (t.flags |= 128, t.child = e.child, t = Iy.bind(null, e), o._reactRetry = t, null) : (e = i.treeContext, Je = dn(o.nextSibling), tt = t, re = !0, _t = null, e !== null && (ut[ct++] = Bt, ut[ct++] = Ut, ut[ct++] = In, Bt = e.id, Ut = e.overflow, In = t), t = Lu(t, r.children), t.flags |= 4096, t);
}
function Cd(e, t, n) {
  e.lanes |= t;
  var r = e.alternate;
  r !== null && (r.lanes |= t), Ca(e.return, t, n);
}
function Is(e, t, n, r, o) {
  var i = e.memoizedState;
  i === null ? e.memoizedState = { isBackwards: t, rendering: null, renderingStartTime: 0, last: r, tail: n, tailMode: o } : (i.isBackwards = t, i.rendering = null, i.renderingStartTime = 0, i.last = r, i.tail = n, i.tailMode = o);
}
function _m(e, t, n) {
  var r = t.pendingProps, o = r.revealOrder, i = r.tail;
  if (Fe(e, t, r.children, n), r = oe.current, r & 2)
    r = r & 1 | 2, t.flags |= 128;
  else {
    if (e !== null && e.flags & 128)
      e:
        for (e = t.child; e !== null; ) {
          if (e.tag === 13)
            e.memoizedState !== null && Cd(e, n, t);
          else if (e.tag === 19)
            Cd(e, n, t);
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
  if (q(oe, r), !(t.mode & 1))
    t.memoizedState = null;
  else
    switch (o) {
      case "forwards":
        for (n = t.child, o = null; n !== null; )
          e = n.alternate, e !== null && Yi(e) === null && (o = n), n = n.sibling;
        n = o, n === null ? (o = t.child, t.child = null) : (o = n.sibling, n.sibling = null), Is(t, !1, o, n, i);
        break;
      case "backwards":
        for (n = null, o = t.child, t.child = null; o !== null; ) {
          if (e = o.alternate, e !== null && Yi(e) === null) {
            t.child = o;
            break;
          }
          e = o.sibling, o.sibling = n, n = o, o = e;
        }
        Is(t, !0, n, null, i);
        break;
      case "together":
        Is(t, !1, null, null, void 0);
        break;
      default:
        t.memoizedState = null;
    }
  return t.child;
}
function Ei(e, t) {
  !(t.mode & 1) && e !== null && (e.alternate = null, t.alternate = null, t.flags |= 2);
}
function Kt(e, t, n) {
  if (e !== null && (t.dependencies = e.dependencies), zn |= t.lanes, !(n & t.childLanes))
    return null;
  if (e !== null && t.child !== e.child)
    throw Error(P(153));
  if (t.child !== null) {
    for (e = t.child, n = hn(e, e.pendingProps), t.child = n, n.return = t; e.sibling !== null; )
      e = e.sibling, n = n.sibling = hn(e, e.pendingProps), n.return = t;
    n.sibling = null;
  }
  return t.child;
}
function wy(e, t, n) {
  switch (t.tag) {
    case 3:
      km(t), Sr();
      break;
    case 5:
      Zp(t);
      break;
    case 1:
      Ke(t.type) && Wi(t);
      break;
    case 4:
      $u(t, t.stateNode.containerInfo);
      break;
    case 10:
      var r = t.type._context, o = t.memoizedProps.value;
      q(Gi, r._currentValue), r._currentValue = o;
      break;
    case 13:
      if (r = t.memoizedState, r !== null)
        return r.dehydrated !== null ? (q(oe, oe.current & 1), t.flags |= 128, null) : n & t.child.childLanes ? Em(e, t, n) : (q(oe, oe.current & 1), e = Kt(e, t, n), e !== null ? e.sibling : null);
      q(oe, oe.current & 1);
      break;
    case 19:
      if (r = (n & t.childLanes) !== 0, e.flags & 128) {
        if (r)
          return _m(e, t, n);
        t.flags |= 128;
      }
      if (o = t.memoizedState, o !== null && (o.rendering = null, o.tail = null, o.lastEffect = null), q(oe, oe.current), r)
        break;
      return null;
    case 22:
    case 23:
      return t.lanes = 0, wm(e, t, n);
  }
  return Kt(e, t, n);
}
var $m, Oa, Pm, Tm;
$m = function(e, t) {
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
Oa = function() {
};
Pm = function(e, t, n, r) {
  var o = e.memoizedProps;
  if (o !== r) {
    e = t.stateNode, Tn(bt.current);
    var i = null;
    switch (n) {
      case "input":
        o = qs(e, o), r = qs(e, r), i = [];
        break;
      case "select":
        o = se({}, o, { value: void 0 }), r = se({}, r, { value: void 0 }), i = [];
        break;
      case "textarea":
        o = ta(e, o), r = ta(e, r), i = [];
        break;
      default:
        typeof o.onClick != "function" && typeof r.onClick == "function" && (e.onclick = Bi);
    }
    ra(n, r);
    var l;
    n = null;
    for (u in o)
      if (!r.hasOwnProperty(u) && o.hasOwnProperty(u) && o[u] != null)
        if (u === "style") {
          var s = o[u];
          for (l in s)
            s.hasOwnProperty(l) && (n || (n = {}), n[l] = "");
        } else
          u !== "dangerouslySetInnerHTML" && u !== "children" && u !== "suppressContentEditableWarning" && u !== "suppressHydrationWarning" && u !== "autoFocus" && (po.hasOwnProperty(u) ? i || (i = []) : (i = i || []).push(u, null));
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
          u === "dangerouslySetInnerHTML" ? (a = a ? a.__html : void 0, s = s ? s.__html : void 0, a != null && s !== a && (i = i || []).push(u, a)) : u === "children" ? typeof a != "string" && typeof a != "number" || (i = i || []).push(u, "" + a) : u !== "suppressContentEditableWarning" && u !== "suppressHydrationWarning" && (po.hasOwnProperty(u) ? (a != null && u === "onScroll" && J("scroll", e), i || s === a || (i = [])) : (i = i || []).push(u, a));
    }
    n && (i = i || []).push("style", n);
    var u = i;
    (t.updateQueue = u) && (t.flags |= 4);
  }
};
Tm = function(e, t, n, r) {
  n !== r && (t.flags |= 4);
};
function Hr(e, t) {
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
function Cy(e, t, n) {
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
      return ze(t), null;
    case 1:
      return Ke(t.type) && Ui(), ze(t), null;
    case 3:
      return r = t.stateNode, Cr(), ee(Ge), ee(Ae), Tu(), r.pendingContext && (r.context = r.pendingContext, r.pendingContext = null), (e === null || e.child === null) && (si(t) ? t.flags |= 4 : e === null || e.memoizedState.isDehydrated && !(t.flags & 256) || (t.flags |= 1024, _t !== null && (Aa(_t), _t = null))), Oa(e, t), ze(t), null;
    case 5:
      Pu(t);
      var o = Tn(_o.current);
      if (n = t.type, e !== null && t.stateNode != null)
        Pm(e, t, n, r, o), e.ref !== t.ref && (t.flags |= 512, t.flags |= 2097152);
      else {
        if (!r) {
          if (t.stateNode === null)
            throw Error(P(166));
          return ze(t), null;
        }
        if (e = Tn(bt.current), si(t)) {
          r = t.stateNode, n = t.type;
          var i = t.memoizedProps;
          switch (r[Lt] = t, r[ko] = i, e = (t.mode & 1) !== 0, n) {
            case "dialog":
              J("cancel", r), J("close", r);
              break;
            case "iframe":
            case "object":
            case "embed":
              J("load", r);
              break;
            case "video":
            case "audio":
              for (o = 0; o < Jr.length; o++)
                J(Jr[o], r);
              break;
            case "source":
              J("error", r);
              break;
            case "img":
            case "image":
            case "link":
              J(
                "error",
                r
              ), J("load", r);
              break;
            case "details":
              J("toggle", r);
              break;
            case "input":
              Mc(r, i), J("invalid", r);
              break;
            case "select":
              r._wrapperState = { wasMultiple: !!i.multiple }, J("invalid", r);
              break;
            case "textarea":
              Ic(r, i), J("invalid", r);
          }
          ra(n, i), o = null;
          for (var l in i)
            if (i.hasOwnProperty(l)) {
              var s = i[l];
              l === "children" ? typeof s == "string" ? r.textContent !== s && (i.suppressHydrationWarning !== !0 && li(r.textContent, s, e), o = ["children", s]) : typeof s == "number" && r.textContent !== "" + s && (i.suppressHydrationWarning !== !0 && li(
                r.textContent,
                s,
                e
              ), o = ["children", "" + s]) : po.hasOwnProperty(l) && s != null && l === "onScroll" && J("scroll", r);
            }
          switch (n) {
            case "input":
              qo(r), Nc(r, i, !0);
              break;
            case "textarea":
              qo(r), Lc(r);
              break;
            case "select":
            case "option":
              break;
            default:
              typeof i.onClick == "function" && (r.onclick = Bi);
          }
          r = o, t.updateQueue = r, r !== null && (t.flags |= 4);
        } else {
          l = o.nodeType === 9 ? o : o.ownerDocument, e === "http://www.w3.org/1999/xhtml" && (e = np(n)), e === "http://www.w3.org/1999/xhtml" ? n === "script" ? (e = l.createElement("div"), e.innerHTML = "<script><\/script>", e = e.removeChild(e.firstChild)) : typeof r.is == "string" ? e = l.createElement(n, { is: r.is }) : (e = l.createElement(n), n === "select" && (l = e, r.multiple ? l.multiple = !0 : r.size && (l.size = r.size))) : e = l.createElementNS(e, n), e[Lt] = t, e[ko] = r, $m(e, t, !1, !1), t.stateNode = e;
          e: {
            switch (l = oa(n, r), n) {
              case "dialog":
                J("cancel", e), J("close", e), o = r;
                break;
              case "iframe":
              case "object":
              case "embed":
                J("load", e), o = r;
                break;
              case "video":
              case "audio":
                for (o = 0; o < Jr.length; o++)
                  J(Jr[o], e);
                o = r;
                break;
              case "source":
                J("error", e), o = r;
                break;
              case "img":
              case "image":
              case "link":
                J(
                  "error",
                  e
                ), J("load", e), o = r;
                break;
              case "details":
                J("toggle", e), o = r;
                break;
              case "input":
                Mc(e, r), o = qs(e, r), J("invalid", e);
                break;
              case "option":
                o = r;
                break;
              case "select":
                e._wrapperState = { wasMultiple: !!r.multiple }, o = se({}, r, { value: void 0 }), J("invalid", e);
                break;
              case "textarea":
                Ic(e, r), o = ta(e, r), J("invalid", e);
                break;
              default:
                o = r;
            }
            ra(n, o), s = o;
            for (i in s)
              if (s.hasOwnProperty(i)) {
                var a = s[i];
                i === "style" ? ip(e, a) : i === "dangerouslySetInnerHTML" ? (a = a ? a.__html : void 0, a != null && rp(e, a)) : i === "children" ? typeof a == "string" ? (n !== "textarea" || a !== "") && mo(e, a) : typeof a == "number" && mo(e, "" + a) : i !== "suppressContentEditableWarning" && i !== "suppressHydrationWarning" && i !== "autoFocus" && (po.hasOwnProperty(i) ? a != null && i === "onScroll" && J("scroll", e) : a != null && ou(e, i, a, l));
              }
            switch (n) {
              case "input":
                qo(e), Nc(e, r, !1);
                break;
              case "textarea":
                qo(e), Lc(e);
                break;
              case "option":
                r.value != null && e.setAttribute("value", "" + yn(r.value));
                break;
              case "select":
                e.multiple = !!r.multiple, i = r.value, i != null ? ur(e, !!r.multiple, i, !1) : r.defaultValue != null && ur(
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
      return ze(t), null;
    case 6:
      if (e && t.stateNode != null)
        Tm(e, t, e.memoizedProps, r);
      else {
        if (typeof r != "string" && t.stateNode === null)
          throw Error(P(166));
        if (n = Tn(_o.current), Tn(bt.current), si(t)) {
          if (r = t.stateNode, n = t.memoizedProps, r[Lt] = t, (i = r.nodeValue !== n) && (e = tt, e !== null))
            switch (e.tag) {
              case 3:
                li(r.nodeValue, n, (e.mode & 1) !== 0);
                break;
              case 5:
                e.memoizedProps.suppressHydrationWarning !== !0 && li(r.nodeValue, n, (e.mode & 1) !== 0);
            }
          i && (t.flags |= 4);
        } else
          r = (n.nodeType === 9 ? n : n.ownerDocument).createTextNode(r), r[Lt] = t, t.stateNode = r;
      }
      return ze(t), null;
    case 13:
      if (ee(oe), r = t.memoizedState, e === null || e.memoizedState !== null && e.memoizedState.dehydrated !== null) {
        if (re && Je !== null && t.mode & 1 && !(t.flags & 128))
          Gp(), Sr(), t.flags |= 98560, i = !1;
        else if (i = si(t), r !== null && r.dehydrated !== null) {
          if (e === null) {
            if (!i)
              throw Error(P(318));
            if (i = t.memoizedState, i = i !== null ? i.dehydrated : null, !i)
              throw Error(P(317));
            i[Lt] = t;
          } else
            Sr(), !(t.flags & 128) && (t.memoizedState = null), t.flags |= 4;
          ze(t), i = !1;
        } else
          _t !== null && (Aa(_t), _t = null), i = !0;
        if (!i)
          return t.flags & 65536 ? t : null;
      }
      return t.flags & 128 ? (t.lanes = n, t) : (r = r !== null, r !== (e !== null && e.memoizedState !== null) && r && (t.child.flags |= 8192, t.mode & 1 && (e === null || oe.current & 1 ? we === 0 && (we = 3) : Fu())), t.updateQueue !== null && (t.flags |= 4), ze(t), null);
    case 4:
      return Cr(), Oa(e, t), e === null && wo(t.stateNode.containerInfo), ze(t), null;
    case 10:
      return ku(t.type._context), ze(t), null;
    case 17:
      return Ke(t.type) && Ui(), ze(t), null;
    case 19:
      if (ee(oe), i = t.memoizedState, i === null)
        return ze(t), null;
      if (r = (t.flags & 128) !== 0, l = i.rendering, l === null)
        if (r)
          Hr(i, !1);
        else {
          if (we !== 0 || e !== null && e.flags & 128)
            for (e = t.child; e !== null; ) {
              if (l = Yi(e), l !== null) {
                for (t.flags |= 128, Hr(i, !1), r = l.updateQueue, r !== null && (t.updateQueue = r, t.flags |= 4), t.subtreeFlags = 0, r = n, n = t.child; n !== null; )
                  i = n, e = r, i.flags &= 14680066, l = i.alternate, l === null ? (i.childLanes = 0, i.lanes = e, i.child = null, i.subtreeFlags = 0, i.memoizedProps = null, i.memoizedState = null, i.updateQueue = null, i.dependencies = null, i.stateNode = null) : (i.childLanes = l.childLanes, i.lanes = l.lanes, i.child = l.child, i.subtreeFlags = 0, i.deletions = null, i.memoizedProps = l.memoizedProps, i.memoizedState = l.memoizedState, i.updateQueue = l.updateQueue, i.type = l.type, e = l.dependencies, i.dependencies = e === null ? null : { lanes: e.lanes, firstContext: e.firstContext }), n = n.sibling;
                return q(oe, oe.current & 1 | 2), t.child;
              }
              e = e.sibling;
            }
          i.tail !== null && pe() > Er && (t.flags |= 128, r = !0, Hr(i, !1), t.lanes = 4194304);
        }
      else {
        if (!r)
          if (e = Yi(l), e !== null) {
            if (t.flags |= 128, r = !0, n = e.updateQueue, n !== null && (t.updateQueue = n, t.flags |= 4), Hr(i, !0), i.tail === null && i.tailMode === "hidden" && !l.alternate && !re)
              return ze(t), null;
          } else
            2 * pe() - i.renderingStartTime > Er && n !== 1073741824 && (t.flags |= 128, r = !0, Hr(i, !1), t.lanes = 4194304);
        i.isBackwards ? (l.sibling = t.child, t.child = l) : (n = i.last, n !== null ? n.sibling = l : t.child = l, i.last = l);
      }
      return i.tail !== null ? (t = i.tail, i.rendering = t, i.tail = t.sibling, i.renderingStartTime = pe(), t.sibling = null, n = oe.current, q(oe, r ? n & 1 | 2 : n & 1), t) : (ze(t), null);
    case 22:
    case 23:
      return Du(), r = t.memoizedState !== null, e !== null && e.memoizedState !== null !== r && (t.flags |= 8192), r && t.mode & 1 ? Xe & 1073741824 && (ze(t), t.subtreeFlags & 6 && (t.flags |= 8192)) : ze(t), null;
    case 24:
      return null;
    case 25:
      return null;
  }
  throw Error(P(156, t.tag));
}
function ky(e, t) {
  switch (xu(t), t.tag) {
    case 1:
      return Ke(t.type) && Ui(), e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, t) : null;
    case 3:
      return Cr(), ee(Ge), ee(Ae), Tu(), e = t.flags, e & 65536 && !(e & 128) ? (t.flags = e & -65537 | 128, t) : null;
    case 5:
      return Pu(t), null;
    case 13:
      if (ee(oe), e = t.memoizedState, e !== null && e.dehydrated !== null) {
        if (t.alternate === null)
          throw Error(P(340));
        Sr();
      }
      return e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, t) : null;
    case 19:
      return ee(oe), null;
    case 4:
      return Cr(), null;
    case 10:
      return ku(t.type._context), null;
    case 22:
    case 23:
      return Du(), null;
    case 24:
      return null;
    default:
      return null;
  }
}
var ci = !1, je = !1, Ey = typeof WeakSet == "function" ? WeakSet : Set, M = null;
function sr(e, t) {
  var n = e.ref;
  if (n !== null)
    if (typeof n == "function")
      try {
        n(null);
      } catch (r) {
        de(e, t, r);
      }
    else
      n.current = null;
}
function Ma(e, t, n) {
  try {
    n();
  } catch (r) {
    de(e, t, r);
  }
}
var kd = !1;
function _y(e, t) {
  if (ma = Ai, e = Ip(), yu(e)) {
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
          var l = 0, s = -1, a = -1, u = 0, c = 0, f = e, m = null;
          t:
            for (; ; ) {
              for (var v; f !== n || o !== 0 && f.nodeType !== 3 || (s = l + o), f !== i || r !== 0 && f.nodeType !== 3 || (a = l + r), f.nodeType === 3 && (l += f.nodeValue.length), (v = f.firstChild) !== null; )
                m = f, f = v;
              for (; ; ) {
                if (f === e)
                  break t;
                if (m === n && ++u === o && (s = l), m === i && ++c === r && (a = l), (v = f.nextSibling) !== null)
                  break;
                f = m, m = f.parentNode;
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
  for (ha = { focusedElem: e, selectionRange: n }, Ai = !1, M = t; M !== null; )
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
                  var g = y.memoizedProps, $ = y.memoizedState, p = t.stateNode, d = p.getSnapshotBeforeUpdate(t.elementType === t.type ? g : kt(t.type, g), $);
                  p.__reactInternalSnapshotBeforeUpdate = d;
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
          de(t, t.return, x);
        }
        if (e = t.sibling, e !== null) {
          e.return = t.return, M = e;
          break;
        }
        M = t.return;
      }
  return y = kd, kd = !1, y;
}
function ao(e, t, n) {
  var r = t.updateQueue;
  if (r = r !== null ? r.lastEffect : null, r !== null) {
    var o = r = r.next;
    do {
      if ((o.tag & e) === e) {
        var i = o.destroy;
        o.destroy = void 0, i !== void 0 && Ma(t, n, i);
      }
      o = o.next;
    } while (o !== r);
  }
}
function yl(e, t) {
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
function Na(e) {
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
function Rm(e) {
  var t = e.alternate;
  t !== null && (e.alternate = null, Rm(t)), e.child = null, e.deletions = null, e.sibling = null, e.tag === 5 && (t = e.stateNode, t !== null && (delete t[Lt], delete t[ko], delete t[va], delete t[sy], delete t[ay])), e.stateNode = null, e.return = null, e.dependencies = null, e.memoizedProps = null, e.memoizedState = null, e.pendingProps = null, e.stateNode = null, e.updateQueue = null;
}
function Om(e) {
  return e.tag === 5 || e.tag === 3 || e.tag === 4;
}
function Ed(e) {
  e:
    for (; ; ) {
      for (; e.sibling === null; ) {
        if (e.return === null || Om(e.return))
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
function Ia(e, t, n) {
  var r = e.tag;
  if (r === 5 || r === 6)
    e = e.stateNode, t ? n.nodeType === 8 ? n.parentNode.insertBefore(e, t) : n.insertBefore(e, t) : (n.nodeType === 8 ? (t = n.parentNode, t.insertBefore(e, n)) : (t = n, t.appendChild(e)), n = n._reactRootContainer, n != null || t.onclick !== null || (t.onclick = Bi));
  else if (r !== 4 && (e = e.child, e !== null))
    for (Ia(e, t, n), e = e.sibling; e !== null; )
      Ia(e, t, n), e = e.sibling;
}
function La(e, t, n) {
  var r = e.tag;
  if (r === 5 || r === 6)
    e = e.stateNode, t ? n.insertBefore(e, t) : n.appendChild(e);
  else if (r !== 4 && (e = e.child, e !== null))
    for (La(e, t, n), e = e.sibling; e !== null; )
      La(e, t, n), e = e.sibling;
}
var Re = null, Et = !1;
function qt(e, t, n) {
  for (n = n.child; n !== null; )
    Mm(e, t, n), n = n.sibling;
}
function Mm(e, t, n) {
  if (zt && typeof zt.onCommitFiberUnmount == "function")
    try {
      zt.onCommitFiberUnmount(ul, n);
    } catch {
    }
  switch (n.tag) {
    case 5:
      je || sr(n, t);
    case 6:
      var r = Re, o = Et;
      Re = null, qt(e, t, n), Re = r, Et = o, Re !== null && (Et ? (e = Re, n = n.stateNode, e.nodeType === 8 ? e.parentNode.removeChild(n) : e.removeChild(n)) : Re.removeChild(n.stateNode));
      break;
    case 18:
      Re !== null && (Et ? (e = Re, n = n.stateNode, e.nodeType === 8 ? $s(e.parentNode, n) : e.nodeType === 1 && $s(e, n), vo(e)) : $s(Re, n.stateNode));
      break;
    case 4:
      r = Re, o = Et, Re = n.stateNode.containerInfo, Et = !0, qt(e, t, n), Re = r, Et = o;
      break;
    case 0:
    case 11:
    case 14:
    case 15:
      if (!je && (r = n.updateQueue, r !== null && (r = r.lastEffect, r !== null))) {
        o = r = r.next;
        do {
          var i = o, l = i.destroy;
          i = i.tag, l !== void 0 && (i & 2 || i & 4) && Ma(n, t, l), o = o.next;
        } while (o !== r);
      }
      qt(e, t, n);
      break;
    case 1:
      if (!je && (sr(n, t), r = n.stateNode, typeof r.componentWillUnmount == "function"))
        try {
          r.props = n.memoizedProps, r.state = n.memoizedState, r.componentWillUnmount();
        } catch (s) {
          de(n, t, s);
        }
      qt(e, t, n);
      break;
    case 21:
      qt(e, t, n);
      break;
    case 22:
      n.mode & 1 ? (je = (r = je) || n.memoizedState !== null, qt(e, t, n), je = r) : qt(e, t, n);
      break;
    default:
      qt(e, t, n);
  }
}
function _d(e) {
  var t = e.updateQueue;
  if (t !== null) {
    e.updateQueue = null;
    var n = e.stateNode;
    n === null && (n = e.stateNode = new Ey()), t.forEach(function(r) {
      var o = Ly.bind(null, e, r);
      n.has(r) || (n.add(r), r.then(o, o));
    });
  }
}
function Ct(e, t) {
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
                Re = s.stateNode, Et = !1;
                break e;
              case 3:
                Re = s.stateNode.containerInfo, Et = !0;
                break e;
              case 4:
                Re = s.stateNode.containerInfo, Et = !0;
                break e;
            }
            s = s.return;
          }
        if (Re === null)
          throw Error(P(160));
        Mm(i, l, o), Re = null, Et = !1;
        var a = o.alternate;
        a !== null && (a.return = null), o.return = null;
      } catch (u) {
        de(o, t, u);
      }
    }
  if (t.subtreeFlags & 12854)
    for (t = t.child; t !== null; )
      Nm(t, e), t = t.sibling;
}
function Nm(e, t) {
  var n = e.alternate, r = e.flags;
  switch (e.tag) {
    case 0:
    case 11:
    case 14:
    case 15:
      if (Ct(t, e), Ot(e), r & 4) {
        try {
          ao(3, e, e.return), yl(3, e);
        } catch (g) {
          de(e, e.return, g);
        }
        try {
          ao(5, e, e.return);
        } catch (g) {
          de(e, e.return, g);
        }
      }
      break;
    case 1:
      Ct(t, e), Ot(e), r & 512 && n !== null && sr(n, n.return);
      break;
    case 5:
      if (Ct(t, e), Ot(e), r & 512 && n !== null && sr(n, n.return), e.flags & 32) {
        var o = e.stateNode;
        try {
          mo(o, "");
        } catch (g) {
          de(e, e.return, g);
        }
      }
      if (r & 4 && (o = e.stateNode, o != null)) {
        var i = e.memoizedProps, l = n !== null ? n.memoizedProps : i, s = e.type, a = e.updateQueue;
        if (e.updateQueue = null, a !== null)
          try {
            s === "input" && i.type === "radio" && i.name != null && ep(o, i), oa(s, l);
            var u = oa(s, i);
            for (l = 0; l < a.length; l += 2) {
              var c = a[l], f = a[l + 1];
              c === "style" ? ip(o, f) : c === "dangerouslySetInnerHTML" ? rp(o, f) : c === "children" ? mo(o, f) : ou(o, c, f, u);
            }
            switch (s) {
              case "input":
                Js(o, i);
                break;
              case "textarea":
                tp(o, i);
                break;
              case "select":
                var m = o._wrapperState.wasMultiple;
                o._wrapperState.wasMultiple = !!i.multiple;
                var v = i.value;
                v != null ? ur(o, !!i.multiple, v, !1) : m !== !!i.multiple && (i.defaultValue != null ? ur(
                  o,
                  !!i.multiple,
                  i.defaultValue,
                  !0
                ) : ur(o, !!i.multiple, i.multiple ? [] : "", !1));
            }
            o[ko] = i;
          } catch (g) {
            de(e, e.return, g);
          }
      }
      break;
    case 6:
      if (Ct(t, e), Ot(e), r & 4) {
        if (e.stateNode === null)
          throw Error(P(162));
        o = e.stateNode, i = e.memoizedProps;
        try {
          o.nodeValue = i;
        } catch (g) {
          de(e, e.return, g);
        }
      }
      break;
    case 3:
      if (Ct(t, e), Ot(e), r & 4 && n !== null && n.memoizedState.isDehydrated)
        try {
          vo(t.containerInfo);
        } catch (g) {
          de(e, e.return, g);
        }
      break;
    case 4:
      Ct(t, e), Ot(e);
      break;
    case 13:
      Ct(t, e), Ot(e), o = e.child, o.flags & 8192 && (i = o.memoizedState !== null, o.stateNode.isHidden = i, !i || o.alternate !== null && o.alternate.memoizedState !== null || (ju = pe())), r & 4 && _d(e);
      break;
    case 22:
      if (c = n !== null && n.memoizedState !== null, e.mode & 1 ? (je = (u = je) || c, Ct(t, e), je = u) : Ct(t, e), Ot(e), r & 8192) {
        if (u = e.memoizedState !== null, (e.stateNode.isHidden = u) && !c && e.mode & 1)
          for (M = e, c = e.child; c !== null; ) {
            for (f = M = c; M !== null; ) {
              switch (m = M, v = m.child, m.tag) {
                case 0:
                case 11:
                case 14:
                case 15:
                  ao(4, m, m.return);
                  break;
                case 1:
                  sr(m, m.return);
                  var y = m.stateNode;
                  if (typeof y.componentWillUnmount == "function") {
                    r = m, n = m.return;
                    try {
                      t = r, y.props = t.memoizedProps, y.state = t.memoizedState, y.componentWillUnmount();
                    } catch (g) {
                      de(r, n, g);
                    }
                  }
                  break;
                case 5:
                  sr(m, m.return);
                  break;
                case 22:
                  if (m.memoizedState !== null) {
                    Pd(f);
                    continue;
                  }
              }
              v !== null ? (v.return = m, M = v) : Pd(f);
            }
            c = c.sibling;
          }
        e:
          for (c = null, f = e; ; ) {
            if (f.tag === 5) {
              if (c === null) {
                c = f;
                try {
                  o = f.stateNode, u ? (i = o.style, typeof i.setProperty == "function" ? i.setProperty("display", "none", "important") : i.display = "none") : (s = f.stateNode, a = f.memoizedProps.style, l = a != null && a.hasOwnProperty("display") ? a.display : null, s.style.display = op("display", l));
                } catch (g) {
                  de(e, e.return, g);
                }
              }
            } else if (f.tag === 6) {
              if (c === null)
                try {
                  f.stateNode.nodeValue = u ? "" : f.memoizedProps;
                } catch (g) {
                  de(e, e.return, g);
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
      Ct(t, e), Ot(e), r & 4 && _d(e);
      break;
    case 21:
      break;
    default:
      Ct(
        t,
        e
      ), Ot(e);
  }
}
function Ot(e) {
  var t = e.flags;
  if (t & 2) {
    try {
      e: {
        for (var n = e.return; n !== null; ) {
          if (Om(n)) {
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
          r.flags & 32 && (mo(o, ""), r.flags &= -33);
          var i = Ed(e);
          La(e, i, o);
          break;
        case 3:
        case 4:
          var l = r.stateNode.containerInfo, s = Ed(e);
          Ia(e, s, l);
          break;
        default:
          throw Error(P(161));
      }
    } catch (a) {
      de(e, e.return, a);
    }
    e.flags &= -3;
  }
  t & 4096 && (e.flags &= -4097);
}
function $y(e, t, n) {
  M = e, Im(e);
}
function Im(e, t, n) {
  for (var r = (e.mode & 1) !== 0; M !== null; ) {
    var o = M, i = o.child;
    if (o.tag === 22 && r) {
      var l = o.memoizedState !== null || ci;
      if (!l) {
        var s = o.alternate, a = s !== null && s.memoizedState !== null || je;
        s = ci;
        var u = je;
        if (ci = l, (je = a) && !u)
          for (M = o; M !== null; )
            l = M, a = l.child, l.tag === 22 && l.memoizedState !== null ? Td(o) : a !== null ? (a.return = l, M = a) : Td(o);
        for (; i !== null; )
          M = i, Im(i), i = i.sibling;
        M = o, ci = s, je = u;
      }
      $d(e);
    } else
      o.subtreeFlags & 8772 && i !== null ? (i.return = o, M = i) : $d(e);
  }
}
function $d(e) {
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
              je || yl(5, t);
              break;
            case 1:
              var r = t.stateNode;
              if (t.flags & 4 && !je)
                if (n === null)
                  r.componentDidMount();
                else {
                  var o = t.elementType === t.type ? n.memoizedProps : kt(t.type, n.memoizedProps);
                  r.componentDidUpdate(o, n.memoizedState, r.__reactInternalSnapshotBeforeUpdate);
                }
              var i = t.updateQueue;
              i !== null && cd(t, i, r);
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
                cd(t, l, n);
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
                    f !== null && vo(f);
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
        je || t.flags & 512 && Na(t);
      } catch (m) {
        de(t, t.return, m);
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
function Pd(e) {
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
function Td(e) {
  for (; M !== null; ) {
    var t = M;
    try {
      switch (t.tag) {
        case 0:
        case 11:
        case 15:
          var n = t.return;
          try {
            yl(4, t);
          } catch (a) {
            de(t, n, a);
          }
          break;
        case 1:
          var r = t.stateNode;
          if (typeof r.componentDidMount == "function") {
            var o = t.return;
            try {
              r.componentDidMount();
            } catch (a) {
              de(t, o, a);
            }
          }
          var i = t.return;
          try {
            Na(t);
          } catch (a) {
            de(t, i, a);
          }
          break;
        case 5:
          var l = t.return;
          try {
            Na(t);
          } catch (a) {
            de(t, l, a);
          }
      }
    } catch (a) {
      de(t, t.return, a);
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
var Py = Math.ceil, qi = Yt.ReactCurrentDispatcher, zu = Yt.ReactCurrentOwner, mt = Yt.ReactCurrentBatchConfig, W = 0, _e = null, ve = null, Me = 0, Xe = 0, ar = Sn(0), we = 0, Ro = null, zn = 0, vl = 0, bu = 0, uo = null, Ve = null, ju = 0, Er = 1 / 0, Dt = null, Ji = !1, za = null, pn = null, di = !1, sn = null, el = 0, co = 0, ba = null, _i = -1, $i = 0;
function Be() {
  return W & 6 ? pe() : _i !== -1 ? _i : _i = pe();
}
function mn(e) {
  return e.mode & 1 ? W & 2 && Me !== 0 ? Me & -Me : cy.transition !== null ? ($i === 0 && ($i = yp()), $i) : (e = K, e !== 0 || (e = window.event, e = e === void 0 ? 16 : Ep(e.type)), e) : 1;
}
function Pt(e, t, n, r) {
  if (50 < co)
    throw co = 0, ba = null, Error(P(185));
  jo(e, n, r), (!(W & 2) || e !== _e) && (e === _e && (!(W & 2) && (vl |= n), we === 4 && rn(e, Me)), Qe(e, r), n === 1 && W === 0 && !(t.mode & 1) && (Er = pe() + 500, ml && wn()));
}
function Qe(e, t) {
  var n = e.callbackNode;
  cg(e, t);
  var r = ji(e, e === _e ? Me : 0);
  if (r === 0)
    n !== null && jc(n), e.callbackNode = null, e.callbackPriority = 0;
  else if (t = r & -r, e.callbackPriority !== t) {
    if (n != null && jc(n), t === 1)
      e.tag === 0 ? uy(Rd.bind(null, e)) : Wp(Rd.bind(null, e)), iy(function() {
        !(W & 6) && wn();
      }), n = null;
    else {
      switch (vp(r)) {
        case 1:
          n = uu;
          break;
        case 4:
          n = hp;
          break;
        case 16:
          n = bi;
          break;
        case 536870912:
          n = gp;
          break;
        default:
          n = bi;
      }
      n = Bm(n, Lm.bind(null, e));
    }
    e.callbackPriority = t, e.callbackNode = n;
  }
}
function Lm(e, t) {
  if (_i = -1, $i = 0, W & 6)
    throw Error(P(327));
  var n = e.callbackNode;
  if (mr() && e.callbackNode !== n)
    return null;
  var r = ji(e, e === _e ? Me : 0);
  if (r === 0)
    return null;
  if (r & 30 || r & e.expiredLanes || t)
    t = tl(e, r);
  else {
    t = r;
    var o = W;
    W |= 2;
    var i = bm();
    (_e !== e || Me !== t) && (Dt = null, Er = pe() + 500, On(e, t));
    do
      try {
        Oy();
        break;
      } catch (s) {
        zm(e, s);
      }
    while (1);
    Cu(), qi.current = i, W = o, ve !== null ? t = 0 : (_e = null, Me = 0, t = we);
  }
  if (t !== 0) {
    if (t === 2 && (o = ua(e), o !== 0 && (r = o, t = ja(e, o))), t === 1)
      throw n = Ro, On(e, 0), rn(e, r), Qe(e, pe()), n;
    if (t === 6)
      rn(e, r);
    else {
      if (o = e.current.alternate, !(r & 30) && !Ty(o) && (t = tl(e, r), t === 2 && (i = ua(e), i !== 0 && (r = i, t = ja(e, i))), t === 1))
        throw n = Ro, On(e, 0), rn(e, r), Qe(e, pe()), n;
      switch (e.finishedWork = o, e.finishedLanes = r, t) {
        case 0:
        case 1:
          throw Error(P(345));
        case 2:
          kn(e, Ve, Dt);
          break;
        case 3:
          if (rn(e, r), (r & 130023424) === r && (t = ju + 500 - pe(), 10 < t)) {
            if (ji(e, 0) !== 0)
              break;
            if (o = e.suspendedLanes, (o & r) !== r) {
              Be(), e.pingedLanes |= e.suspendedLanes & o;
              break;
            }
            e.timeoutHandle = ya(kn.bind(null, e, Ve, Dt), t);
            break;
          }
          kn(e, Ve, Dt);
          break;
        case 4:
          if (rn(e, r), (r & 4194240) === r)
            break;
          for (t = e.eventTimes, o = -1; 0 < r; ) {
            var l = 31 - $t(r);
            i = 1 << l, l = t[l], l > o && (o = l), r &= ~i;
          }
          if (r = o, r = pe() - r, r = (120 > r ? 120 : 480 > r ? 480 : 1080 > r ? 1080 : 1920 > r ? 1920 : 3e3 > r ? 3e3 : 4320 > r ? 4320 : 1960 * Py(r / 1960)) - r, 10 < r) {
            e.timeoutHandle = ya(kn.bind(null, e, Ve, Dt), r);
            break;
          }
          kn(e, Ve, Dt);
          break;
        case 5:
          kn(e, Ve, Dt);
          break;
        default:
          throw Error(P(329));
      }
    }
  }
  return Qe(e, pe()), e.callbackNode === n ? Lm.bind(null, e) : null;
}
function ja(e, t) {
  var n = uo;
  return e.current.memoizedState.isDehydrated && (On(e, t).flags |= 256), e = tl(e, t), e !== 2 && (t = Ve, Ve = n, t !== null && Aa(t)), e;
}
function Aa(e) {
  Ve === null ? Ve = e : Ve.push.apply(Ve, e);
}
function Ty(e) {
  for (var t = e; ; ) {
    if (t.flags & 16384) {
      var n = t.updateQueue;
      if (n !== null && (n = n.stores, n !== null))
        for (var r = 0; r < n.length; r++) {
          var o = n[r], i = o.getSnapshot;
          o = o.value;
          try {
            if (!Tt(i(), o))
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
function rn(e, t) {
  for (t &= ~bu, t &= ~vl, e.suspendedLanes |= t, e.pingedLanes &= ~t, e = e.expirationTimes; 0 < t; ) {
    var n = 31 - $t(t), r = 1 << n;
    e[n] = -1, t &= ~r;
  }
}
function Rd(e) {
  if (W & 6)
    throw Error(P(327));
  mr();
  var t = ji(e, 0);
  if (!(t & 1))
    return Qe(e, pe()), null;
  var n = tl(e, t);
  if (e.tag !== 0 && n === 2) {
    var r = ua(e);
    r !== 0 && (t = r, n = ja(e, r));
  }
  if (n === 1)
    throw n = Ro, On(e, 0), rn(e, t), Qe(e, pe()), n;
  if (n === 6)
    throw Error(P(345));
  return e.finishedWork = e.current.alternate, e.finishedLanes = t, kn(e, Ve, Dt), Qe(e, pe()), null;
}
function Au(e, t) {
  var n = W;
  W |= 1;
  try {
    return e(t);
  } finally {
    W = n, W === 0 && (Er = pe() + 500, ml && wn());
  }
}
function bn(e) {
  sn !== null && sn.tag === 0 && !(W & 6) && mr();
  var t = W;
  W |= 1;
  var n = mt.transition, r = K;
  try {
    if (mt.transition = null, K = 1, e)
      return e();
  } finally {
    K = r, mt.transition = n, W = t, !(W & 6) && wn();
  }
}
function Du() {
  Xe = ar.current, ee(ar);
}
function On(e, t) {
  e.finishedWork = null, e.finishedLanes = 0;
  var n = e.timeoutHandle;
  if (n !== -1 && (e.timeoutHandle = -1, oy(n)), ve !== null)
    for (n = ve.return; n !== null; ) {
      var r = n;
      switch (xu(r), r.tag) {
        case 1:
          r = r.type.childContextTypes, r != null && Ui();
          break;
        case 3:
          Cr(), ee(Ge), ee(Ae), Tu();
          break;
        case 5:
          Pu(r);
          break;
        case 4:
          Cr();
          break;
        case 13:
          ee(oe);
          break;
        case 19:
          ee(oe);
          break;
        case 10:
          ku(r.type._context);
          break;
        case 22:
        case 23:
          Du();
      }
      n = n.return;
    }
  if (_e = e, ve = e = hn(e.current, null), Me = Xe = t, we = 0, Ro = null, bu = vl = zn = 0, Ve = uo = null, Pn !== null) {
    for (t = 0; t < Pn.length; t++)
      if (n = Pn[t], r = n.interleaved, r !== null) {
        n.interleaved = null;
        var o = r.next, i = n.pending;
        if (i !== null) {
          var l = i.next;
          i.next = o, r.next = l;
        }
        n.pending = r;
      }
    Pn = null;
  }
  return e;
}
function zm(e, t) {
  do {
    var n = ve;
    try {
      if (Cu(), Ci.current = Zi, Xi) {
        for (var r = ie.memoizedState; r !== null; ) {
          var o = r.queue;
          o !== null && (o.pending = null), r = r.next;
        }
        Xi = !1;
      }
      if (Ln = 0, Ee = Se = ie = null, so = !1, $o = 0, zu.current = null, n === null || n.return === null) {
        we = 1, Ro = t, ve = null;
        break;
      }
      e: {
        var i = e, l = n.return, s = n, a = t;
        if (t = Me, s.flags |= 32768, a !== null && typeof a == "object" && typeof a.then == "function") {
          var u = a, c = s, f = c.tag;
          if (!(c.mode & 1) && (f === 0 || f === 11 || f === 15)) {
            var m = c.alternate;
            m ? (c.updateQueue = m.updateQueue, c.memoizedState = m.memoizedState, c.lanes = m.lanes) : (c.updateQueue = null, c.memoizedState = null);
          }
          var v = gd(l);
          if (v !== null) {
            v.flags &= -257, yd(v, l, s, i, t), v.mode & 1 && hd(i, u, t), t = v, a = u;
            var y = t.updateQueue;
            if (y === null) {
              var g = /* @__PURE__ */ new Set();
              g.add(a), t.updateQueue = g;
            } else
              y.add(a);
            break e;
          } else {
            if (!(t & 1)) {
              hd(i, u, t), Fu();
              break e;
            }
            a = Error(P(426));
          }
        } else if (re && s.mode & 1) {
          var $ = gd(l);
          if ($ !== null) {
            !($.flags & 65536) && ($.flags |= 256), yd($, l, s, i, t), Su(kr(a, s));
            break e;
          }
        }
        i = a = kr(a, s), we !== 4 && (we = 2), uo === null ? uo = [i] : uo.push(i), i = l;
        do {
          switch (i.tag) {
            case 3:
              i.flags |= 65536, t &= -t, i.lanes |= t;
              var p = vm(i, a, t);
              ud(i, p);
              break e;
            case 1:
              s = a;
              var d = i.type, h = i.stateNode;
              if (!(i.flags & 128) && (typeof d.getDerivedStateFromError == "function" || h !== null && typeof h.componentDidCatch == "function" && (pn === null || !pn.has(h)))) {
                i.flags |= 65536, t &= -t, i.lanes |= t;
                var x = xm(i, s, t);
                ud(i, x);
                break e;
              }
          }
          i = i.return;
        } while (i !== null);
      }
      Am(n);
    } catch (_) {
      t = _, ve === n && n !== null && (ve = n = n.return);
      continue;
    }
    break;
  } while (1);
}
function bm() {
  var e = qi.current;
  return qi.current = Zi, e === null ? Zi : e;
}
function Fu() {
  (we === 0 || we === 3 || we === 2) && (we = 4), _e === null || !(zn & 268435455) && !(vl & 268435455) || rn(_e, Me);
}
function tl(e, t) {
  var n = W;
  W |= 2;
  var r = bm();
  (_e !== e || Me !== t) && (Dt = null, On(e, t));
  do
    try {
      Ry();
      break;
    } catch (o) {
      zm(e, o);
    }
  while (1);
  if (Cu(), W = n, qi.current = r, ve !== null)
    throw Error(P(261));
  return _e = null, Me = 0, we;
}
function Ry() {
  for (; ve !== null; )
    jm(ve);
}
function Oy() {
  for (; ve !== null && !tg(); )
    jm(ve);
}
function jm(e) {
  var t = Fm(e.alternate, e, Xe);
  e.memoizedProps = e.pendingProps, t === null ? Am(e) : ve = t, zu.current = null;
}
function Am(e) {
  var t = e;
  do {
    var n = t.alternate;
    if (e = t.return, t.flags & 32768) {
      if (n = ky(n, t), n !== null) {
        n.flags &= 32767, ve = n;
        return;
      }
      if (e !== null)
        e.flags |= 32768, e.subtreeFlags = 0, e.deletions = null;
      else {
        we = 6, ve = null;
        return;
      }
    } else if (n = Cy(n, t, Xe), n !== null) {
      ve = n;
      return;
    }
    if (t = t.sibling, t !== null) {
      ve = t;
      return;
    }
    ve = t = e;
  } while (t !== null);
  we === 0 && (we = 5);
}
function kn(e, t, n) {
  var r = K, o = mt.transition;
  try {
    mt.transition = null, K = 1, My(e, t, n, r);
  } finally {
    mt.transition = o, K = r;
  }
  return null;
}
function My(e, t, n, r) {
  do
    mr();
  while (sn !== null);
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
  if (dg(e, i), e === _e && (ve = _e = null, Me = 0), !(n.subtreeFlags & 2064) && !(n.flags & 2064) || di || (di = !0, Bm(bi, function() {
    return mr(), null;
  })), i = (n.flags & 15990) !== 0, n.subtreeFlags & 15990 || i) {
    i = mt.transition, mt.transition = null;
    var l = K;
    K = 1;
    var s = W;
    W |= 4, zu.current = null, _y(e, n), Nm(n, e), Zg(ha), Ai = !!ma, ha = ma = null, e.current = n, $y(n), ng(), W = s, K = l, mt.transition = i;
  } else
    e.current = n;
  if (di && (di = !1, sn = e, el = o), i = e.pendingLanes, i === 0 && (pn = null), ig(n.stateNode), Qe(e, pe()), t !== null)
    for (r = e.onRecoverableError, n = 0; n < t.length; n++)
      o = t[n], r(o.value, { componentStack: o.stack, digest: o.digest });
  if (Ji)
    throw Ji = !1, e = za, za = null, e;
  return el & 1 && e.tag !== 0 && mr(), i = e.pendingLanes, i & 1 ? e === ba ? co++ : (co = 0, ba = e) : co = 0, wn(), null;
}
function mr() {
  if (sn !== null) {
    var e = vp(el), t = mt.transition, n = K;
    try {
      if (mt.transition = null, K = 16 > e ? 16 : e, sn === null)
        var r = !1;
      else {
        if (e = sn, sn = null, el = 0, W & 6)
          throw Error(P(331));
        var o = W;
        for (W |= 4, M = e.current; M !== null; ) {
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
                      ao(8, c, i);
                  }
                  var f = c.child;
                  if (f !== null)
                    f.return = c, M = f;
                  else
                    for (; M !== null; ) {
                      c = M;
                      var m = c.sibling, v = c.return;
                      if (Rm(c), c === u) {
                        M = null;
                        break;
                      }
                      if (m !== null) {
                        m.return = v, M = m;
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
                    var $ = g.sibling;
                    g.sibling = null, g = $;
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
                      ao(9, i, i.return);
                  }
                var p = i.sibling;
                if (p !== null) {
                  p.return = i.return, M = p;
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
                        yl(9, s);
                    }
                  } catch (_) {
                    de(s, s.return, _);
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
        if (W = o, wn(), zt && typeof zt.onPostCommitFiberRoot == "function")
          try {
            zt.onPostCommitFiberRoot(ul, e);
          } catch {
          }
        r = !0;
      }
      return r;
    } finally {
      K = n, mt.transition = t;
    }
  }
  return !1;
}
function Od(e, t, n) {
  t = kr(n, t), t = vm(e, t, 1), e = fn(e, t, 1), t = Be(), e !== null && (jo(e, 1, t), Qe(e, t));
}
function de(e, t, n) {
  if (e.tag === 3)
    Od(e, e, n);
  else
    for (; t !== null; ) {
      if (t.tag === 3) {
        Od(t, e, n);
        break;
      } else if (t.tag === 1) {
        var r = t.stateNode;
        if (typeof t.type.getDerivedStateFromError == "function" || typeof r.componentDidCatch == "function" && (pn === null || !pn.has(r))) {
          e = kr(n, e), e = xm(t, e, 1), t = fn(t, e, 1), e = Be(), t !== null && (jo(t, 1, e), Qe(t, e));
          break;
        }
      }
      t = t.return;
    }
}
function Ny(e, t, n) {
  var r = e.pingCache;
  r !== null && r.delete(t), t = Be(), e.pingedLanes |= e.suspendedLanes & n, _e === e && (Me & n) === n && (we === 4 || we === 3 && (Me & 130023424) === Me && 500 > pe() - ju ? On(e, 0) : bu |= n), Qe(e, t);
}
function Dm(e, t) {
  t === 0 && (e.mode & 1 ? (t = ti, ti <<= 1, !(ti & 130023424) && (ti = 4194304)) : t = 1);
  var n = Be();
  e = Gt(e, t), e !== null && (jo(e, t, n), Qe(e, n));
}
function Iy(e) {
  var t = e.memoizedState, n = 0;
  t !== null && (n = t.retryLane), Dm(e, n);
}
function Ly(e, t) {
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
  r !== null && r.delete(t), Dm(e, n);
}
var Fm;
Fm = function(e, t, n) {
  if (e !== null)
    if (e.memoizedProps !== t.pendingProps || Ge.current)
      He = !0;
    else {
      if (!(e.lanes & n) && !(t.flags & 128))
        return He = !1, wy(e, t, n);
      He = !!(e.flags & 131072);
    }
  else
    He = !1, re && t.flags & 1048576 && Vp(t, Hi, t.index);
  switch (t.lanes = 0, t.tag) {
    case 2:
      var r = t.type;
      Ei(e, t), e = t.pendingProps;
      var o = xr(t, Ae.current);
      pr(t, n), o = Ou(null, t, r, e, o, n);
      var i = Mu();
      return t.flags |= 1, typeof o == "object" && o !== null && typeof o.render == "function" && o.$$typeof === void 0 ? (t.tag = 1, t.memoizedState = null, t.updateQueue = null, Ke(r) ? (i = !0, Wi(t)) : i = !1, t.memoizedState = o.state !== null && o.state !== void 0 ? o.state : null, _u(t), o.updater = gl, t.stateNode = o, o._reactInternals = t, Ea(t, r, e, n), t = Pa(null, t, r, !0, i, n)) : (t.tag = 0, re && i && vu(t), Fe(null, t, o, n), t = t.child), t;
    case 16:
      r = t.elementType;
      e: {
        switch (Ei(e, t), e = t.pendingProps, o = r._init, r = o(r._payload), t.type = r, o = t.tag = by(r), e = kt(r, e), o) {
          case 0:
            t = $a(null, t, r, e, n);
            break e;
          case 1:
            t = Sd(null, t, r, e, n);
            break e;
          case 11:
            t = vd(null, t, r, e, n);
            break e;
          case 14:
            t = xd(null, t, r, kt(r.type, e), n);
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
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : kt(r, o), $a(e, t, r, o, n);
    case 1:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : kt(r, o), Sd(e, t, r, o, n);
    case 3:
      e: {
        if (km(t), e === null)
          throw Error(P(387));
        r = t.pendingProps, i = t.memoizedState, o = i.element, Xp(e, t), Qi(t, r, null, n);
        var l = t.memoizedState;
        if (r = l.element, i.isDehydrated)
          if (i = { element: r, isDehydrated: !1, cache: l.cache, pendingSuspenseBoundaries: l.pendingSuspenseBoundaries, transitions: l.transitions }, t.updateQueue.baseState = i, t.memoizedState = i, t.flags & 256) {
            o = kr(Error(P(423)), t), t = wd(e, t, r, n, o);
            break e;
          } else if (r !== o) {
            o = kr(Error(P(424)), t), t = wd(e, t, r, n, o);
            break e;
          } else
            for (Je = dn(t.stateNode.containerInfo.firstChild), tt = t, re = !0, _t = null, n = Qp(t, null, r, n), t.child = n; n; )
              n.flags = n.flags & -3 | 4096, n = n.sibling;
        else {
          if (Sr(), r === o) {
            t = Kt(e, t, n);
            break e;
          }
          Fe(e, t, r, n);
        }
        t = t.child;
      }
      return t;
    case 5:
      return Zp(t), e === null && wa(t), r = t.type, o = t.pendingProps, i = e !== null ? e.memoizedProps : null, l = o.children, ga(r, o) ? l = null : i !== null && ga(r, i) && (t.flags |= 32), Cm(e, t), Fe(e, t, l, n), t.child;
    case 6:
      return e === null && wa(t), null;
    case 13:
      return Em(e, t, n);
    case 4:
      return $u(t, t.stateNode.containerInfo), r = t.pendingProps, e === null ? t.child = wr(t, null, r, n) : Fe(e, t, r, n), t.child;
    case 11:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : kt(r, o), vd(e, t, r, o, n);
    case 7:
      return Fe(e, t, t.pendingProps, n), t.child;
    case 8:
      return Fe(e, t, t.pendingProps.children, n), t.child;
    case 12:
      return Fe(e, t, t.pendingProps.children, n), t.child;
    case 10:
      e: {
        if (r = t.type._context, o = t.pendingProps, i = t.memoizedProps, l = o.value, q(Gi, r._currentValue), r._currentValue = l, i !== null)
          if (Tt(i.value, l)) {
            if (i.children === o.children && !Ge.current) {
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
                    i.lanes |= n, a = i.alternate, a !== null && (a.lanes |= n), Ca(
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
                l.lanes |= n, s = l.alternate, s !== null && (s.lanes |= n), Ca(l, n, t), l = i.sibling;
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
        Fe(e, t, o.children, n), t = t.child;
      }
      return t;
    case 9:
      return o = t.type, r = t.pendingProps.children, pr(t, n), o = ht(o), r = r(o), t.flags |= 1, Fe(e, t, r, n), t.child;
    case 14:
      return r = t.type, o = kt(r, t.pendingProps), o = kt(r.type, o), xd(e, t, r, o, n);
    case 15:
      return Sm(e, t, t.type, t.pendingProps, n);
    case 17:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : kt(r, o), Ei(e, t), t.tag = 1, Ke(r) ? (e = !0, Wi(t)) : e = !1, pr(t, n), ym(t, r, o), Ea(t, r, o, n), Pa(null, t, r, !0, e, n);
    case 19:
      return _m(e, t, n);
    case 22:
      return wm(e, t, n);
  }
  throw Error(P(156, t.tag));
};
function Bm(e, t) {
  return mp(e, t);
}
function zy(e, t, n, r) {
  this.tag = e, this.key = n, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.ref = null, this.pendingProps = t, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = r, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
}
function ft(e, t, n, r) {
  return new zy(e, t, n, r);
}
function Bu(e) {
  return e = e.prototype, !(!e || !e.isReactComponent);
}
function by(e) {
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
function hn(e, t) {
  var n = e.alternate;
  return n === null ? (n = ft(e.tag, t, e.key, e.mode), n.elementType = e.elementType, n.type = e.type, n.stateNode = e.stateNode, n.alternate = e, e.alternate = n) : (n.pendingProps = t, n.type = e.type, n.flags = 0, n.subtreeFlags = 0, n.deletions = null), n.flags = e.flags & 14680064, n.childLanes = e.childLanes, n.lanes = e.lanes, n.child = e.child, n.memoizedProps = e.memoizedProps, n.memoizedState = e.memoizedState, n.updateQueue = e.updateQueue, t = e.dependencies, n.dependencies = t === null ? null : { lanes: t.lanes, firstContext: t.firstContext }, n.sibling = e.sibling, n.index = e.index, n.ref = e.ref, n;
}
function Pi(e, t, n, r, o, i) {
  var l = 2;
  if (r = e, typeof e == "function")
    Bu(e) && (l = 1);
  else if (typeof e == "string")
    l = 5;
  else
    e:
      switch (e) {
        case qn:
          return Mn(n.children, o, i, t);
        case iu:
          l = 8, o |= 8;
          break;
        case Qs:
          return e = ft(12, n, t, o | 2), e.elementType = Qs, e.lanes = i, e;
        case Ys:
          return e = ft(13, n, t, o), e.elementType = Ys, e.lanes = i, e;
        case Xs:
          return e = ft(19, n, t, o), e.elementType = Xs, e.lanes = i, e;
        case Zf:
          return xl(n, o, i, t);
        default:
          if (typeof e == "object" && e !== null)
            switch (e.$$typeof) {
              case Yf:
                l = 10;
                break e;
              case Xf:
                l = 9;
                break e;
              case lu:
                l = 11;
                break e;
              case su:
                l = 14;
                break e;
              case en:
                l = 16, r = null;
                break e;
            }
          throw Error(P(130, e == null ? e : typeof e, ""));
      }
  return t = ft(l, n, t, o), t.elementType = e, t.type = r, t.lanes = i, t;
}
function Mn(e, t, n, r) {
  return e = ft(7, e, r, t), e.lanes = n, e;
}
function xl(e, t, n, r) {
  return e = ft(22, e, r, t), e.elementType = Zf, e.lanes = n, e.stateNode = { isHidden: !1 }, e;
}
function Ls(e, t, n) {
  return e = ft(6, e, null, t), e.lanes = n, e;
}
function zs(e, t, n) {
  return t = ft(4, e.children !== null ? e.children : [], e.key, t), t.lanes = n, t.stateNode = { containerInfo: e.containerInfo, pendingChildren: null, implementation: e.implementation }, t;
}
function jy(e, t, n, r, o) {
  this.tag = t, this.containerInfo = e, this.finishedWork = this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.pendingContext = this.context = null, this.callbackPriority = 0, this.eventTimes = hs(0), this.expirationTimes = hs(-1), this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = hs(0), this.identifierPrefix = r, this.onRecoverableError = o, this.mutableSourceEagerHydrationData = null;
}
function Uu(e, t, n, r, o, i, l, s, a) {
  return e = new jy(e, t, n, s, a), t === 1 ? (t = 1, i === !0 && (t |= 8)) : t = 0, i = ft(3, null, null, t), e.current = i, i.stateNode = e, i.memoizedState = { element: r, isDehydrated: n, cache: null, transitions: null, pendingSuspenseBoundaries: null }, _u(i), e;
}
function Ay(e, t, n) {
  var r = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
  return { $$typeof: Zn, key: r == null ? null : "" + r, children: e, containerInfo: t, implementation: n };
}
function Um(e) {
  if (!e)
    return vn;
  e = e._reactInternals;
  e: {
    if (Dn(e) !== e || e.tag !== 1)
      throw Error(P(170));
    var t = e;
    do {
      switch (t.tag) {
        case 3:
          t = t.stateNode.context;
          break e;
        case 1:
          if (Ke(t.type)) {
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
    if (Ke(n))
      return Up(e, n, t);
  }
  return t;
}
function Wm(e, t, n, r, o, i, l, s, a) {
  return e = Uu(n, r, !0, e, o, i, l, s, a), e.context = Um(null), n = e.current, r = Be(), o = mn(n), i = Wt(r, o), i.callback = t ?? null, fn(n, i, o), e.current.lanes = o, jo(e, o, r), Qe(e, r), e;
}
function Sl(e, t, n, r) {
  var o = t.current, i = Be(), l = mn(o);
  return n = Um(n), t.context === null ? t.context = n : t.pendingContext = n, t = Wt(i, l), t.payload = { element: e }, r = r === void 0 ? null : r, r !== null && (t.callback = r), e = fn(o, t, l), e !== null && (Pt(e, o, l, i), wi(e, o, l)), l;
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
function Md(e, t) {
  if (e = e.memoizedState, e !== null && e.dehydrated !== null) {
    var n = e.retryLane;
    e.retryLane = n !== 0 && n < t ? n : t;
  }
}
function Wu(e, t) {
  Md(e, t), (e = e.alternate) && Md(e, t);
}
function Dy() {
  return null;
}
var Vm = typeof reportError == "function" ? reportError : function(e) {
  console.error(e);
};
function Vu(e) {
  this._internalRoot = e;
}
wl.prototype.render = Vu.prototype.render = function(e) {
  var t = this._internalRoot;
  if (t === null)
    throw Error(P(409));
  Sl(e, t, null, null);
};
wl.prototype.unmount = Vu.prototype.unmount = function() {
  var e = this._internalRoot;
  if (e !== null) {
    this._internalRoot = null;
    var t = e.containerInfo;
    bn(function() {
      Sl(null, e, null, null);
    }), t[Ht] = null;
  }
};
function wl(e) {
  this._internalRoot = e;
}
wl.prototype.unstable_scheduleHydration = function(e) {
  if (e) {
    var t = wp();
    e = { blockedOn: null, target: e, priority: t };
    for (var n = 0; n < nn.length && t !== 0 && t < nn[n].priority; n++)
      ;
    nn.splice(n, 0, e), n === 0 && kp(e);
  }
};
function Hu(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11);
}
function Cl(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11 && (e.nodeType !== 8 || e.nodeValue !== " react-mount-point-unstable "));
}
function Nd() {
}
function Fy(e, t, n, r, o) {
  if (o) {
    if (typeof r == "function") {
      var i = r;
      r = function() {
        var u = nl(l);
        i.call(u);
      };
    }
    var l = Wm(t, r, e, 0, null, !1, !1, "", Nd);
    return e._reactRootContainer = l, e[Ht] = l.current, wo(e.nodeType === 8 ? e.parentNode : e), bn(), l;
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
  var a = Uu(e, 0, !1, null, null, !1, !1, "", Nd);
  return e._reactRootContainer = a, e[Ht] = a.current, wo(e.nodeType === 8 ? e.parentNode : e), bn(function() {
    Sl(t, a, n, r);
  }), a;
}
function kl(e, t, n, r, o) {
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
    Sl(t, l, e, o);
  } else
    l = Fy(n, t, e, o, r);
  return nl(l);
}
xp = function(e) {
  switch (e.tag) {
    case 3:
      var t = e.stateNode;
      if (t.current.memoizedState.isDehydrated) {
        var n = qr(t.pendingLanes);
        n !== 0 && (cu(t, n | 1), Qe(t, pe()), !(W & 6) && (Er = pe() + 500, wn()));
      }
      break;
    case 13:
      bn(function() {
        var r = Gt(e, 1);
        if (r !== null) {
          var o = Be();
          Pt(r, e, 1, o);
        }
      }), Wu(e, 1);
  }
};
du = function(e) {
  if (e.tag === 13) {
    var t = Gt(e, 134217728);
    if (t !== null) {
      var n = Be();
      Pt(t, e, 134217728, n);
    }
    Wu(e, 134217728);
  }
};
Sp = function(e) {
  if (e.tag === 13) {
    var t = mn(e), n = Gt(e, t);
    if (n !== null) {
      var r = Be();
      Pt(n, e, t, r);
    }
    Wu(e, t);
  }
};
wp = function() {
  return K;
};
Cp = function(e, t) {
  var n = K;
  try {
    return K = e, t();
  } finally {
    K = n;
  }
};
la = function(e, t, n) {
  switch (t) {
    case "input":
      if (Js(e, n), t = n.name, n.type === "radio" && t != null) {
        for (n = e; n.parentNode; )
          n = n.parentNode;
        for (n = n.querySelectorAll("input[name=" + JSON.stringify("" + t) + '][type="radio"]'), t = 0; t < n.length; t++) {
          var r = n[t];
          if (r !== e && r.form === e.form) {
            var o = pl(r);
            if (!o)
              throw Error(P(90));
            Jf(r), Js(r, o);
          }
        }
      }
      break;
    case "textarea":
      tp(e, n);
      break;
    case "select":
      t = n.value, t != null && ur(e, !!n.multiple, t, !1);
  }
};
ap = Au;
up = bn;
var By = { usingClientEntryPoint: !1, Events: [Do, nr, pl, lp, sp, Au] }, Gr = { findFiberByHostInstance: $n, bundleType: 0, version: "18.3.1", rendererPackageName: "react-dom" }, Uy = { bundleType: Gr.bundleType, version: Gr.version, rendererPackageName: Gr.rendererPackageName, rendererConfig: Gr.rendererConfig, overrideHookState: null, overrideHookStateDeletePath: null, overrideHookStateRenamePath: null, overrideProps: null, overridePropsDeletePath: null, overridePropsRenamePath: null, setErrorHandler: null, setSuspenseHandler: null, scheduleUpdate: null, currentDispatcherRef: Yt.ReactCurrentDispatcher, findHostInstanceByFiber: function(e) {
  return e = fp(e), e === null ? null : e.stateNode;
}, findFiberByHostInstance: Gr.findFiberByHostInstance || Dy, findHostInstancesForRefresh: null, scheduleRefresh: null, scheduleRoot: null, setRefreshHandler: null, getCurrentFiber: null, reconcilerVersion: "18.3.1-next-f1338f8080-20240426" };
if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u") {
  var fi = __REACT_DEVTOOLS_GLOBAL_HOOK__;
  if (!fi.isDisabled && fi.supportsFiber)
    try {
      ul = fi.inject(Uy), zt = fi;
    } catch {
    }
}
ot.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = By;
ot.createPortal = function(e, t) {
  var n = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
  if (!Hu(t))
    throw Error(P(200));
  return Ay(e, t, null, n);
};
ot.createRoot = function(e, t) {
  if (!Hu(e))
    throw Error(P(299));
  var n = !1, r = "", o = Vm;
  return t != null && (t.unstable_strictMode === !0 && (n = !0), t.identifierPrefix !== void 0 && (r = t.identifierPrefix), t.onRecoverableError !== void 0 && (o = t.onRecoverableError)), t = Uu(e, 1, !1, null, null, n, !1, r, o), e[Ht] = t.current, wo(e.nodeType === 8 ? e.parentNode : e), new Vu(t);
};
ot.findDOMNode = function(e) {
  if (e == null)
    return null;
  if (e.nodeType === 1)
    return e;
  var t = e._reactInternals;
  if (t === void 0)
    throw typeof e.render == "function" ? Error(P(188)) : (e = Object.keys(e).join(","), Error(P(268, e)));
  return e = fp(t), e = e === null ? null : e.stateNode, e;
};
ot.flushSync = function(e) {
  return bn(e);
};
ot.hydrate = function(e, t, n) {
  if (!Cl(t))
    throw Error(P(200));
  return kl(null, e, t, !0, n);
};
ot.hydrateRoot = function(e, t, n) {
  if (!Hu(e))
    throw Error(P(405));
  var r = n != null && n.hydratedSources || null, o = !1, i = "", l = Vm;
  if (n != null && (n.unstable_strictMode === !0 && (o = !0), n.identifierPrefix !== void 0 && (i = n.identifierPrefix), n.onRecoverableError !== void 0 && (l = n.onRecoverableError)), t = Wm(t, null, e, 1, n ?? null, o, !1, i, l), e[Ht] = t.current, wo(e), r)
    for (e = 0; e < r.length; e++)
      n = r[e], o = n._getVersion, o = o(n._source), t.mutableSourceEagerHydrationData == null ? t.mutableSourceEagerHydrationData = [n, o] : t.mutableSourceEagerHydrationData.push(
        n,
        o
      );
  return new wl(t);
};
ot.render = function(e, t, n) {
  if (!Cl(t))
    throw Error(P(200));
  return kl(null, e, t, !1, n);
};
ot.unmountComponentAtNode = function(e) {
  if (!Cl(e))
    throw Error(P(40));
  return e._reactRootContainer ? (bn(function() {
    kl(null, null, e, !1, function() {
      e._reactRootContainer = null, e[Ht] = null;
    });
  }), !0) : !1;
};
ot.unstable_batchedUpdates = Au;
ot.unstable_renderSubtreeIntoContainer = function(e, t, n, r) {
  if (!Cl(n))
    throw Error(P(200));
  if (e == null || e._reactInternals === void 0)
    throw Error(P(38));
  return kl(e, t, n, !1, r);
};
ot.version = "18.3.1-next-f1338f8080-20240426";
function Hm() {
  if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function"))
    try {
      __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(Hm);
    } catch (e) {
      console.error(e);
    }
}
Hm(), Hf.exports = ot;
var Gm = Hf.exports;
const pi = /* @__PURE__ */ If(Gm);
var Id = Gm;
Gs.createRoot = Id.createRoot, Gs.hydrateRoot = Id.hydrateRoot;
function Oo(e) {
  let t = "https://mui.com/production-error/?code=" + e;
  for (let n = 1; n < arguments.length; n += 1)
    t += "&args[]=" + encodeURIComponent(arguments[n]);
  return "Minified MUI error #" + e + "; visit " + t + " for the full message.";
}
const Wy = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Oo
}, Symbol.toStringTag, { value: "Module" })), _r = "$$material";
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
function B(e, t) {
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
var Vy = !1;
function Hy(e) {
  if (e.sheet)
    return e.sheet;
  for (var t = 0; t < document.styleSheets.length; t++)
    if (document.styleSheets[t].ownerNode === e)
      return document.styleSheets[t];
}
function Gy(e) {
  var t = document.createElement("style");
  return t.setAttribute("data-emotion", e.key), e.nonce !== void 0 && t.setAttribute("nonce", e.nonce), t.appendChild(document.createTextNode("")), t.setAttribute("data-s", ""), t;
}
var Ky = /* @__PURE__ */ function() {
  function e(n) {
    var r = this;
    this._insertTag = function(o) {
      var i;
      r.tags.length === 0 ? r.insertionPoint ? i = r.insertionPoint.nextSibling : r.prepend ? i = r.container.firstChild : i = r.before : i = r.tags[r.tags.length - 1].nextSibling, r.container.insertBefore(o, i), r.tags.push(o);
    }, this.isSpeedy = n.speedy === void 0 ? !Vy : n.speedy, this.tags = [], this.ctr = 0, this.nonce = n.nonce, this.key = n.key, this.container = n.container, this.prepend = n.prepend, this.insertionPoint = n.insertionPoint, this.before = null;
  }
  var t = e.prototype;
  return t.hydrate = function(r) {
    r.forEach(this._insertTag);
  }, t.insert = function(r) {
    this.ctr % (this.isSpeedy ? 65e3 : 1) === 0 && this._insertTag(Gy(this));
    var o = this.tags[this.tags.length - 1];
    if (this.isSpeedy) {
      var i = Hy(o);
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
}(), be = "-ms-", rl = "-moz-", H = "-webkit-", Km = "comm", Gu = "rule", Ku = "decl", Qy = "@import", Qm = "@keyframes", Yy = "@layer", Xy = Math.abs, El = String.fromCharCode, Zy = Object.assign;
function qy(e, t) {
  return Oe(e, 0) ^ 45 ? (((t << 2 ^ Oe(e, 0)) << 2 ^ Oe(e, 1)) << 2 ^ Oe(e, 2)) << 2 ^ Oe(e, 3) : 0;
}
function Ym(e) {
  return e.trim();
}
function Jy(e, t) {
  return (e = t.exec(e)) ? e[0] : e;
}
function G(e, t, n) {
  return e.replace(t, n);
}
function Da(e, t) {
  return e.indexOf(t);
}
function Oe(e, t) {
  return e.charCodeAt(t) | 0;
}
function Mo(e, t, n) {
  return e.slice(t, n);
}
function Nt(e) {
  return e.length;
}
function Qu(e) {
  return e.length;
}
function mi(e, t) {
  return t.push(e), e;
}
function ev(e, t) {
  return e.map(t).join("");
}
var _l = 1, $r = 1, Xm = 0, Ye = 0, ye = 0, Nr = "";
function $l(e, t, n, r, o, i, l) {
  return { value: e, root: t, parent: n, type: r, props: o, children: i, line: _l, column: $r, length: l, return: "" };
}
function Kr(e, t) {
  return Zy($l("", null, null, "", null, null, 0), e, { length: -e.length }, t);
}
function tv() {
  return ye;
}
function nv() {
  return ye = Ye > 0 ? Oe(Nr, --Ye) : 0, $r--, ye === 10 && ($r = 1, _l--), ye;
}
function nt() {
  return ye = Ye < Xm ? Oe(Nr, Ye++) : 0, $r++, ye === 10 && ($r = 1, _l++), ye;
}
function jt() {
  return Oe(Nr, Ye);
}
function Ti() {
  return Ye;
}
function Bo(e, t) {
  return Mo(Nr, e, t);
}
function No(e) {
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
function Zm(e) {
  return _l = $r = 1, Xm = Nt(Nr = e), Ye = 0, [];
}
function qm(e) {
  return Nr = "", e;
}
function Ri(e) {
  return Ym(Bo(Ye - 1, Fa(e === 91 ? e + 2 : e === 40 ? e + 1 : e)));
}
function rv(e) {
  for (; (ye = jt()) && ye < 33; )
    nt();
  return No(e) > 2 || No(ye) > 3 ? "" : " ";
}
function ov(e, t) {
  for (; --t && nt() && !(ye < 48 || ye > 102 || ye > 57 && ye < 65 || ye > 70 && ye < 97); )
    ;
  return Bo(e, Ti() + (t < 6 && jt() == 32 && nt() == 32));
}
function Fa(e) {
  for (; nt(); )
    switch (ye) {
      case e:
        return Ye;
      case 34:
      case 39:
        e !== 34 && e !== 39 && Fa(ye);
        break;
      case 40:
        e === 41 && Fa(e);
        break;
      case 92:
        nt();
        break;
    }
  return Ye;
}
function iv(e, t) {
  for (; nt() && e + ye !== 47 + 10; )
    if (e + ye === 42 + 42 && jt() === 47)
      break;
  return "/*" + Bo(t, Ye - 1) + "*" + El(e === 47 ? e : nt());
}
function lv(e) {
  for (; !No(jt()); )
    nt();
  return Bo(e, Ye);
}
function sv(e) {
  return qm(Oi("", null, null, null, [""], e = Zm(e), 0, [0], e));
}
function Oi(e, t, n, r, o, i, l, s, a) {
  for (var u = 0, c = 0, f = l, m = 0, v = 0, y = 0, g = 1, $ = 1, p = 1, d = 0, h = "", x = o, _ = i, E = r, k = h; $; )
    switch (y = d, d = nt()) {
      case 40:
        if (y != 108 && Oe(k, f - 1) == 58) {
          Da(k += G(Ri(d), "&", "&\f"), "&\f") != -1 && (p = -1);
          break;
        }
      case 34:
      case 39:
      case 91:
        k += Ri(d);
        break;
      case 9:
      case 10:
      case 13:
      case 32:
        k += rv(y);
        break;
      case 92:
        k += ov(Ti() - 1, 7);
        continue;
      case 47:
        switch (jt()) {
          case 42:
          case 47:
            mi(av(iv(nt(), Ti()), t, n), a);
            break;
          default:
            k += "/";
        }
        break;
      case 123 * g:
        s[u++] = Nt(k) * p;
      case 125 * g:
      case 59:
      case 0:
        switch (d) {
          case 0:
          case 125:
            $ = 0;
          case 59 + c:
            p == -1 && (k = G(k, /\f/g, "")), v > 0 && Nt(k) - f && mi(v > 32 ? zd(k + ";", r, n, f - 1) : zd(G(k, " ", "") + ";", r, n, f - 2), a);
            break;
          case 59:
            k += ";";
          default:
            if (mi(E = Ld(k, t, n, u, c, o, s, h, x = [], _ = [], f), i), d === 123)
              if (c === 0)
                Oi(k, t, E, E, x, i, f, s, _);
              else
                switch (m === 99 && Oe(k, 3) === 110 ? 100 : m) {
                  case 100:
                  case 108:
                  case 109:
                  case 115:
                    Oi(e, E, E, r && mi(Ld(e, E, E, 0, 0, o, s, h, o, x = [], f), _), o, _, f, s, r ? x : _);
                    break;
                  default:
                    Oi(k, E, E, E, [""], _, 0, s, _);
                }
        }
        u = c = v = 0, g = p = 1, h = k = "", f = l;
        break;
      case 58:
        f = 1 + Nt(k), v = y;
      default:
        if (g < 1) {
          if (d == 123)
            --g;
          else if (d == 125 && g++ == 0 && nv() == 125)
            continue;
        }
        switch (k += El(d), d * g) {
          case 38:
            p = c > 0 ? 1 : (k += "\f", -1);
            break;
          case 44:
            s[u++] = (Nt(k) - 1) * p, p = 1;
            break;
          case 64:
            jt() === 45 && (k += Ri(nt())), m = jt(), c = f = Nt(h = k += lv(Ti())), d++;
            break;
          case 45:
            y === 45 && Nt(k) == 2 && (g = 0);
        }
    }
  return i;
}
function Ld(e, t, n, r, o, i, l, s, a, u, c) {
  for (var f = o - 1, m = o === 0 ? i : [""], v = Qu(m), y = 0, g = 0, $ = 0; y < r; ++y)
    for (var p = 0, d = Mo(e, f + 1, f = Xy(g = l[y])), h = e; p < v; ++p)
      (h = Ym(g > 0 ? m[p] + " " + d : G(d, /&\f/g, m[p]))) && (a[$++] = h);
  return $l(e, t, n, o === 0 ? Gu : s, a, u, c);
}
function av(e, t, n) {
  return $l(e, t, n, Km, El(tv()), Mo(e, 2, -2), 0);
}
function zd(e, t, n, r) {
  return $l(e, t, n, Ku, Mo(e, 0, r), Mo(e, r + 1, -1), r);
}
function hr(e, t) {
  for (var n = "", r = Qu(e), o = 0; o < r; o++)
    n += t(e[o], o, e, t) || "";
  return n;
}
function uv(e, t, n, r) {
  switch (e.type) {
    case Yy:
      if (e.children.length)
        break;
    case Qy:
    case Ku:
      return e.return = e.return || e.value;
    case Km:
      return "";
    case Qm:
      return e.return = e.value + "{" + hr(e.children, r) + "}";
    case Gu:
      e.value = e.props.join(",");
  }
  return Nt(n = hr(e.children, r)) ? e.return = e.value + "{" + n + "}" : "";
}
function cv(e) {
  var t = Qu(e);
  return function(n, r, o, i) {
    for (var l = "", s = 0; s < t; s++)
      l += e[s](n, r, o, i) || "";
    return l;
  };
}
function dv(e) {
  return function(t) {
    t.root || (t = t.return) && e(t);
  };
}
function Jm(e) {
  var t = /* @__PURE__ */ Object.create(null);
  return function(n) {
    return t[n] === void 0 && (t[n] = e(n)), t[n];
  };
}
var fv = function(t, n, r) {
  for (var o = 0, i = 0; o = i, i = jt(), o === 38 && i === 12 && (n[r] = 1), !No(i); )
    nt();
  return Bo(t, Ye);
}, pv = function(t, n) {
  var r = -1, o = 44;
  do
    switch (No(o)) {
      case 0:
        o === 38 && jt() === 12 && (n[r] = 1), t[r] += fv(Ye - 1, n, r);
        break;
      case 2:
        t[r] += Ri(o);
        break;
      case 4:
        if (o === 44) {
          t[++r] = jt() === 58 ? "&\f" : "", n[r] = t[r].length;
          break;
        }
      default:
        t[r] += El(o);
    }
  while (o = nt());
  return t;
}, mv = function(t, n) {
  return qm(pv(Zm(t), n));
}, bd = /* @__PURE__ */ new WeakMap(), hv = function(t) {
  if (!(t.type !== "rule" || !t.parent || // positive .length indicates that this rule contains pseudo
  // negative .length indicates that this rule has been already prefixed
  t.length < 1)) {
    for (var n = t.value, r = t.parent, o = t.column === r.column && t.line === r.line; r.type !== "rule"; )
      if (r = r.parent, !r)
        return;
    if (!(t.props.length === 1 && n.charCodeAt(0) !== 58 && !bd.get(r)) && !o) {
      bd.set(t, !0);
      for (var i = [], l = mv(n, i), s = r.props, a = 0, u = 0; a < l.length; a++)
        for (var c = 0; c < s.length; c++, u++)
          t.props[u] = i[a] ? l[a].replace(/&\f/g, s[c]) : s[c] + " " + l[a];
    }
  }
}, gv = function(t) {
  if (t.type === "decl") {
    var n = t.value;
    // charcode for l
    n.charCodeAt(0) === 108 && // charcode for b
    n.charCodeAt(2) === 98 && (t.return = "", t.value = "");
  }
};
function eh(e, t) {
  switch (qy(e, t)) {
    case 5103:
      return H + "print-" + e + e;
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
      return H + e + e;
    case 5349:
    case 4246:
    case 4810:
    case 6968:
    case 2756:
      return H + e + rl + e + be + e + e;
    case 6828:
    case 4268:
      return H + e + be + e + e;
    case 6165:
      return H + e + be + "flex-" + e + e;
    case 5187:
      return H + e + G(e, /(\w+).+(:[^]+)/, H + "box-$1$2" + be + "flex-$1$2") + e;
    case 5443:
      return H + e + be + "flex-item-" + G(e, /flex-|-self/, "") + e;
    case 4675:
      return H + e + be + "flex-line-pack" + G(e, /align-content|flex-|-self/, "") + e;
    case 5548:
      return H + e + be + G(e, "shrink", "negative") + e;
    case 5292:
      return H + e + be + G(e, "basis", "preferred-size") + e;
    case 6060:
      return H + "box-" + G(e, "-grow", "") + H + e + be + G(e, "grow", "positive") + e;
    case 4554:
      return H + G(e, /([^-])(transform)/g, "$1" + H + "$2") + e;
    case 6187:
      return G(G(G(e, /(zoom-|grab)/, H + "$1"), /(image-set)/, H + "$1"), e, "") + e;
    case 5495:
    case 3959:
      return G(e, /(image-set\([^]*)/, H + "$1$`$1");
    case 4968:
      return G(G(e, /(.+:)(flex-)?(.*)/, H + "box-pack:$3" + be + "flex-pack:$3"), /s.+-b[^;]+/, "justify") + H + e + e;
    case 4095:
    case 3583:
    case 4068:
    case 2532:
      return G(e, /(.+)-inline(.+)/, H + "$1$2") + e;
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
      if (Nt(e) - 1 - t > 6)
        switch (Oe(e, t + 1)) {
          case 109:
            if (Oe(e, t + 4) !== 45)
              break;
          case 102:
            return G(e, /(.+:)(.+)-([^]+)/, "$1" + H + "$2-$3$1" + rl + (Oe(e, t + 3) == 108 ? "$3" : "$2-$3")) + e;
          case 115:
            return ~Da(e, "stretch") ? eh(G(e, "stretch", "fill-available"), t) + e : e;
        }
      break;
    case 4949:
      if (Oe(e, t + 1) !== 115)
        break;
    case 6444:
      switch (Oe(e, Nt(e) - 3 - (~Da(e, "!important") && 10))) {
        case 107:
          return G(e, ":", ":" + H) + e;
        case 101:
          return G(e, /(.+:)([^;!]+)(;|!.+)?/, "$1" + H + (Oe(e, 14) === 45 ? "inline-" : "") + "box$3$1" + H + "$2$3$1" + be + "$2box$3") + e;
      }
      break;
    case 5936:
      switch (Oe(e, t + 11)) {
        case 114:
          return H + e + be + G(e, /[svh]\w+-[tblr]{2}/, "tb") + e;
        case 108:
          return H + e + be + G(e, /[svh]\w+-[tblr]{2}/, "tb-rl") + e;
        case 45:
          return H + e + be + G(e, /[svh]\w+-[tblr]{2}/, "lr") + e;
      }
      return H + e + be + e + e;
  }
  return e;
}
var yv = function(t, n, r, o) {
  if (t.length > -1 && !t.return)
    switch (t.type) {
      case Ku:
        t.return = eh(t.value, t.length);
        break;
      case Qm:
        return hr([Kr(t, {
          value: G(t.value, "@", "@" + H)
        })], o);
      case Gu:
        if (t.length)
          return ev(t.props, function(i) {
            switch (Jy(i, /(::plac\w+|:read-\w+)/)) {
              case ":read-only":
              case ":read-write":
                return hr([Kr(t, {
                  props: [G(i, /:(read-\w+)/, ":" + rl + "$1")]
                })], o);
              case "::placeholder":
                return hr([Kr(t, {
                  props: [G(i, /:(plac\w+)/, ":" + H + "input-$1")]
                }), Kr(t, {
                  props: [G(i, /:(plac\w+)/, ":" + rl + "$1")]
                }), Kr(t, {
                  props: [G(i, /:(plac\w+)/, be + "input-$1")]
                })], o);
            }
            return "";
          });
    }
}, vv = [yv], th = function(t) {
  var n = t.key;
  if (n === "css") {
    var r = document.querySelectorAll("style[data-emotion]:not([data-s])");
    Array.prototype.forEach.call(r, function(g) {
      var $ = g.getAttribute("data-emotion");
      $.indexOf(" ") !== -1 && (document.head.appendChild(g), g.setAttribute("data-s", ""));
    });
  }
  var o = t.stylisPlugins || vv, i = {}, l, s = [];
  l = t.container || document.head, Array.prototype.forEach.call(
    // this means we will ignore elements which don't have a space in them which
    // means that the style elements we're looking at are only Emotion 11 server-rendered style elements
    document.querySelectorAll('style[data-emotion^="' + n + ' "]'),
    function(g) {
      for (var $ = g.getAttribute("data-emotion").split(" "), p = 1; p < $.length; p++)
        i[$[p]] = !0;
      s.push(g);
    }
  );
  var a, u = [hv, gv];
  {
    var c, f = [uv, dv(function(g) {
      c.insert(g);
    })], m = cv(u.concat(o, f)), v = function($) {
      return hr(sv($), m);
    };
    a = function($, p, d, h) {
      c = d, v($ ? $ + "{" + p.styles + "}" : p.styles), h && (y.inserted[p.name] = !0);
    };
  }
  var y = {
    key: n,
    sheet: new Ky({
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
}, nh = { exports: {} }, Q = {};
/** @license React v16.13.1
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var $e = typeof Symbol == "function" && Symbol.for, Yu = $e ? Symbol.for("react.element") : 60103, Xu = $e ? Symbol.for("react.portal") : 60106, Pl = $e ? Symbol.for("react.fragment") : 60107, Tl = $e ? Symbol.for("react.strict_mode") : 60108, Rl = $e ? Symbol.for("react.profiler") : 60114, Ol = $e ? Symbol.for("react.provider") : 60109, Ml = $e ? Symbol.for("react.context") : 60110, Zu = $e ? Symbol.for("react.async_mode") : 60111, Nl = $e ? Symbol.for("react.concurrent_mode") : 60111, Il = $e ? Symbol.for("react.forward_ref") : 60112, Ll = $e ? Symbol.for("react.suspense") : 60113, xv = $e ? Symbol.for("react.suspense_list") : 60120, zl = $e ? Symbol.for("react.memo") : 60115, bl = $e ? Symbol.for("react.lazy") : 60116, Sv = $e ? Symbol.for("react.block") : 60121, wv = $e ? Symbol.for("react.fundamental") : 60117, Cv = $e ? Symbol.for("react.responder") : 60118, kv = $e ? Symbol.for("react.scope") : 60119;
function lt(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Yu:
        switch (e = e.type, e) {
          case Zu:
          case Nl:
          case Pl:
          case Rl:
          case Tl:
          case Ll:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Ml:
              case Il:
              case bl:
              case zl:
              case Ol:
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
function rh(e) {
  return lt(e) === Nl;
}
Q.AsyncMode = Zu;
Q.ConcurrentMode = Nl;
Q.ContextConsumer = Ml;
Q.ContextProvider = Ol;
Q.Element = Yu;
Q.ForwardRef = Il;
Q.Fragment = Pl;
Q.Lazy = bl;
Q.Memo = zl;
Q.Portal = Xu;
Q.Profiler = Rl;
Q.StrictMode = Tl;
Q.Suspense = Ll;
Q.isAsyncMode = function(e) {
  return rh(e) || lt(e) === Zu;
};
Q.isConcurrentMode = rh;
Q.isContextConsumer = function(e) {
  return lt(e) === Ml;
};
Q.isContextProvider = function(e) {
  return lt(e) === Ol;
};
Q.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Yu;
};
Q.isForwardRef = function(e) {
  return lt(e) === Il;
};
Q.isFragment = function(e) {
  return lt(e) === Pl;
};
Q.isLazy = function(e) {
  return lt(e) === bl;
};
Q.isMemo = function(e) {
  return lt(e) === zl;
};
Q.isPortal = function(e) {
  return lt(e) === Xu;
};
Q.isProfiler = function(e) {
  return lt(e) === Rl;
};
Q.isStrictMode = function(e) {
  return lt(e) === Tl;
};
Q.isSuspense = function(e) {
  return lt(e) === Ll;
};
Q.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === Pl || e === Nl || e === Rl || e === Tl || e === Ll || e === xv || typeof e == "object" && e !== null && (e.$$typeof === bl || e.$$typeof === zl || e.$$typeof === Ol || e.$$typeof === Ml || e.$$typeof === Il || e.$$typeof === wv || e.$$typeof === Cv || e.$$typeof === kv || e.$$typeof === Sv);
};
Q.typeOf = lt;
nh.exports = Q;
var Ev = nh.exports, oh = Ev, _v = {
  $$typeof: !0,
  render: !0,
  defaultProps: !0,
  displayName: !0,
  propTypes: !0
}, $v = {
  $$typeof: !0,
  compare: !0,
  defaultProps: !0,
  displayName: !0,
  propTypes: !0,
  type: !0
}, ih = {};
ih[oh.ForwardRef] = _v;
ih[oh.Memo] = $v;
var Pv = !0;
function lh(e, t, n) {
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
  Pv === !1) && t.registered[o] === void 0 && (t.registered[o] = n.styles);
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
function Tv(e) {
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
var Rv = {
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
}, Ov = !1, Mv = /[A-Z]|^ms/g, Nv = /_EMO_([^_]+?)_([^]*?)_EMO_/g, sh = function(t) {
  return t.charCodeAt(1) === 45;
}, jd = function(t) {
  return t != null && typeof t != "boolean";
}, bs = /* @__PURE__ */ Jm(function(e) {
  return sh(e) ? e : e.replace(Mv, "-$&").toLowerCase();
}), Ad = function(t, n) {
  switch (t) {
    case "animation":
    case "animationName":
      if (typeof n == "string")
        return n.replace(Nv, function(r, o, i) {
          return It = {
            name: o,
            styles: i,
            next: It
          }, o;
        });
  }
  return Rv[t] !== 1 && !sh(t) && typeof n == "number" && n !== 0 ? n + "px" : n;
}, Iv = "Component selectors can only be used in conjunction with @emotion/babel-plugin, the swc Emotion plugin, or another Emotion-aware compiler transform.";
function Io(e, t, n) {
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
        return It = {
          name: o.name,
          styles: o.styles,
          next: It
        }, o.name;
      var i = n;
      if (i.styles !== void 0) {
        var l = i.next;
        if (l !== void 0)
          for (; l !== void 0; )
            It = {
              name: l.name,
              styles: l.styles,
              next: It
            }, l = l.next;
        var s = i.styles + ";";
        return s;
      }
      return Lv(e, t, n);
    }
    case "function": {
      if (e !== void 0) {
        var a = It, u = n(e);
        return It = a, Io(e, t, u);
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
function Lv(e, t, n) {
  var r = "";
  if (Array.isArray(n))
    for (var o = 0; o < n.length; o++)
      r += Io(e, t, n[o]) + ";";
  else
    for (var i in n) {
      var l = n[i];
      if (typeof l != "object") {
        var s = l;
        t != null && t[s] !== void 0 ? r += i + "{" + t[s] + "}" : jd(s) && (r += bs(i) + ":" + Ad(i, s) + ";");
      } else {
        if (i === "NO_COMPONENT_SELECTOR" && Ov)
          throw new Error(Iv);
        if (Array.isArray(l) && typeof l[0] == "string" && (t == null || t[l[0]] === void 0))
          for (var a = 0; a < l.length; a++)
            jd(l[a]) && (r += bs(i) + ":" + Ad(i, l[a]) + ";");
        else {
          var u = Io(e, t, l);
          switch (i) {
            case "animation":
            case "animationName": {
              r += bs(i) + ":" + u + ";";
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
var Dd = /label:\s*([^\s;{]+)\s*(;|$)/g, It;
function Uo(e, t, n) {
  if (e.length === 1 && typeof e[0] == "object" && e[0] !== null && e[0].styles !== void 0)
    return e[0];
  var r = !0, o = "";
  It = void 0;
  var i = e[0];
  if (i == null || i.raw === void 0)
    r = !1, o += Io(n, t, i);
  else {
    var l = i;
    o += l[0];
  }
  for (var s = 1; s < e.length; s++)
    if (o += Io(n, t, e[s]), r) {
      var a = i;
      o += a[s];
    }
  Dd.lastIndex = 0;
  for (var u = "", c; (c = Dd.exec(o)) !== null; )
    u += "-" + c[1];
  var f = Tv(o) + u;
  return {
    name: f,
    styles: o,
    next: It
  };
}
var zv = function(t) {
  return t();
}, ah = Hs["useInsertionEffect"] ? Hs["useInsertionEffect"] : !1, uh = ah || zv, Fd = ah || w.useLayoutEffect, bv = !1, ch = /* @__PURE__ */ w.createContext(
  // we're doing this to avoid preconstruct's dead code elimination in this one case
  // because this module is primarily intended for the browser and node
  // but it's also required in react native and similar environments sometimes
  // and we could have a special build just for that
  // but this is much easier and the native packages
  // might use a different theme context in the future anyway
  typeof HTMLElement < "u" ? /* @__PURE__ */ th({
    key: "css"
  }) : null
), jv = ch.Provider, ec = function(t) {
  return /* @__PURE__ */ w.forwardRef(function(n, r) {
    var o = w.useContext(ch);
    return t(n, o, r);
  });
}, Ir = /* @__PURE__ */ w.createContext({}), tc = {}.hasOwnProperty, Ba = "__EMOTION_TYPE_PLEASE_DO_NOT_USE__", Av = function(t, n) {
  var r = {};
  for (var o in n)
    tc.call(n, o) && (r[o] = n[o]);
  return r[Ba] = t, r;
}, Dv = function(t) {
  var n = t.cache, r = t.serialized, o = t.isStringTag;
  return qu(n, r, o), uh(function() {
    return Ju(n, r, o);
  }), null;
}, Fv = /* @__PURE__ */ ec(function(e, t, n) {
  var r = e.css;
  typeof r == "string" && t.registered[r] !== void 0 && (r = t.registered[r]);
  var o = e[Ba], i = [r], l = "";
  typeof e.className == "string" ? l = lh(t.registered, i, e.className) : e.className != null && (l = e.className + " ");
  var s = Uo(i, void 0, w.useContext(Ir));
  l += t.key + "-" + s.name;
  var a = {};
  for (var u in e)
    tc.call(e, u) && u !== "css" && u !== Ba && !bv && (a[u] = e[u]);
  return a.className = l, n && (a.ref = n), /* @__PURE__ */ w.createElement(w.Fragment, null, /* @__PURE__ */ w.createElement(Dv, {
    cache: t,
    serialized: s,
    isStringTag: typeof o == "string"
  }), /* @__PURE__ */ w.createElement(o, a));
}), Bv = Fv, js = { exports: {} }, Bd;
function dh() {
  return Bd || (Bd = 1, function(e) {
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
  }(js)), js.exports;
}
dh();
var Ud = function(t, n) {
  var r = arguments;
  if (n == null || !tc.call(n, "css"))
    return w.createElement.apply(void 0, r);
  var o = r.length, i = new Array(o);
  i[0] = Bv, i[1] = Av(t, n);
  for (var l = 2; l < o; l++)
    i[l] = r[l];
  return w.createElement.apply(null, i);
};
(function(e) {
  var t;
  t || (t = e.JSX || (e.JSX = {}));
})(Ud || (Ud = {}));
var Uv = /* @__PURE__ */ ec(function(e, t) {
  var n = e.styles, r = Uo([n], void 0, w.useContext(Ir)), o = w.useRef();
  return Fd(function() {
    var i = t.key + "-global", l = new t.sheet.constructor({
      key: i,
      nonce: t.sheet.nonce,
      container: t.sheet.container,
      speedy: t.sheet.isSpeedy
    }), s = !1, a = document.querySelector('style[data-emotion="' + i + " " + r.name + '"]');
    return t.sheet.tags.length && (l.before = t.sheet.tags[0]), a !== null && (s = !0, a.setAttribute("data-emotion", i), l.hydrate([a])), o.current = [l, s], function() {
      l.flush();
    };
  }, [t]), Fd(function() {
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
function jl() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  return Uo(t);
}
function Lr() {
  var e = jl.apply(void 0, arguments), t = "animation-" + e.name;
  return {
    name: t,
    styles: "@keyframes " + t + "{" + e.styles + "}",
    anim: 1,
    toString: function() {
      return "_EMO_" + this.name + "_" + this.styles + "_EMO_";
    }
  };
}
var Wv = /^((children|dangerouslySetInnerHTML|key|ref|autoFocus|defaultValue|defaultChecked|innerHTML|suppressContentEditableWarning|suppressHydrationWarning|valueLink|abbr|accept|acceptCharset|accessKey|action|allow|allowUserMedia|allowPaymentRequest|allowFullScreen|allowTransparency|alt|async|autoComplete|autoPlay|capture|cellPadding|cellSpacing|challenge|charSet|checked|cite|classID|className|cols|colSpan|content|contentEditable|contextMenu|controls|controlsList|coords|crossOrigin|data|dateTime|decoding|default|defer|dir|disabled|disablePictureInPicture|disableRemotePlayback|download|draggable|encType|enterKeyHint|fetchpriority|fetchPriority|form|formAction|formEncType|formMethod|formNoValidate|formTarget|frameBorder|headers|height|hidden|high|href|hrefLang|htmlFor|httpEquiv|id|inputMode|integrity|is|keyParams|keyType|kind|label|lang|list|loading|loop|low|marginHeight|marginWidth|max|maxLength|media|mediaGroup|method|min|minLength|multiple|muted|name|nonce|noValidate|open|optimum|pattern|placeholder|playsInline|popover|popoverTarget|popoverTargetAction|poster|preload|profile|radioGroup|readOnly|referrerPolicy|rel|required|reversed|role|rows|rowSpan|sandbox|scope|scoped|scrolling|seamless|selected|shape|size|sizes|slot|span|spellCheck|src|srcDoc|srcLang|srcSet|start|step|style|summary|tabIndex|target|title|translate|type|useMap|value|width|wmode|wrap|about|datatype|inlist|prefix|property|resource|typeof|vocab|autoCapitalize|autoCorrect|autoSave|color|incremental|fallback|inert|itemProp|itemScope|itemType|itemID|itemRef|on|option|results|security|unselectable|accentHeight|accumulate|additive|alignmentBaseline|allowReorder|alphabetic|amplitude|arabicForm|ascent|attributeName|attributeType|autoReverse|azimuth|baseFrequency|baselineShift|baseProfile|bbox|begin|bias|by|calcMode|capHeight|clip|clipPathUnits|clipPath|clipRule|colorInterpolation|colorInterpolationFilters|colorProfile|colorRendering|contentScriptType|contentStyleType|cursor|cx|cy|d|decelerate|descent|diffuseConstant|direction|display|divisor|dominantBaseline|dur|dx|dy|edgeMode|elevation|enableBackground|end|exponent|externalResourcesRequired|fill|fillOpacity|fillRule|filter|filterRes|filterUnits|floodColor|floodOpacity|focusable|fontFamily|fontSize|fontSizeAdjust|fontStretch|fontStyle|fontVariant|fontWeight|format|from|fr|fx|fy|g1|g2|glyphName|glyphOrientationHorizontal|glyphOrientationVertical|glyphRef|gradientTransform|gradientUnits|hanging|horizAdvX|horizOriginX|ideographic|imageRendering|in|in2|intercept|k|k1|k2|k3|k4|kernelMatrix|kernelUnitLength|kerning|keyPoints|keySplines|keyTimes|lengthAdjust|letterSpacing|lightingColor|limitingConeAngle|local|markerEnd|markerMid|markerStart|markerHeight|markerUnits|markerWidth|mask|maskContentUnits|maskUnits|mathematical|mode|numOctaves|offset|opacity|operator|order|orient|orientation|origin|overflow|overlinePosition|overlineThickness|panose1|paintOrder|pathLength|patternContentUnits|patternTransform|patternUnits|pointerEvents|points|pointsAtX|pointsAtY|pointsAtZ|preserveAlpha|preserveAspectRatio|primitiveUnits|r|radius|refX|refY|renderingIntent|repeatCount|repeatDur|requiredExtensions|requiredFeatures|restart|result|rotate|rx|ry|scale|seed|shapeRendering|slope|spacing|specularConstant|specularExponent|speed|spreadMethod|startOffset|stdDeviation|stemh|stemv|stitchTiles|stopColor|stopOpacity|strikethroughPosition|strikethroughThickness|string|stroke|strokeDasharray|strokeDashoffset|strokeLinecap|strokeLinejoin|strokeMiterlimit|strokeOpacity|strokeWidth|surfaceScale|systemLanguage|tableValues|targetX|targetY|textAnchor|textDecoration|textRendering|textLength|to|transform|u1|u2|underlinePosition|underlineThickness|unicode|unicodeBidi|unicodeRange|unitsPerEm|vAlphabetic|vHanging|vIdeographic|vMathematical|values|vectorEffect|version|vertAdvY|vertOriginX|vertOriginY|viewBox|viewTarget|visibility|widths|wordSpacing|writingMode|x|xHeight|x1|x2|xChannelSelector|xlinkActuate|xlinkArcrole|xlinkHref|xlinkRole|xlinkShow|xlinkTitle|xlinkType|xmlBase|xmlns|xmlnsXlink|xmlLang|xmlSpace|y|y1|y2|yChannelSelector|z|zoomAndPan|for|class|autofocus)|(([Dd][Aa][Tt][Aa]|[Aa][Rr][Ii][Aa]|x)-.*))$/, Vv = /* @__PURE__ */ Jm(
  function(e) {
    return Wv.test(e) || e.charCodeAt(0) === 111 && e.charCodeAt(1) === 110 && e.charCodeAt(2) < 91;
  }
  /* Z+1 */
), Hv = !1, Gv = Vv, Kv = function(t) {
  return t !== "theme";
}, Wd = function(t) {
  return typeof t == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  t.charCodeAt(0) > 96 ? Gv : Kv;
}, Vd = function(t, n, r) {
  var o;
  if (n) {
    var i = n.shouldForwardProp;
    o = t.__emotion_forwardProp && i ? function(l) {
      return t.__emotion_forwardProp(l) && i(l);
    } : i;
  }
  return typeof o != "function" && r && (o = t.__emotion_forwardProp), o;
}, Qv = function(t) {
  var n = t.cache, r = t.serialized, o = t.isStringTag;
  return qu(n, r, o), uh(function() {
    return Ju(n, r, o);
  }), null;
}, Yv = function e(t, n) {
  var r = t.__emotion_real === t, o = r && t.__emotion_base || t, i, l;
  n !== void 0 && (i = n.label, l = n.target);
  var s = Vd(t, n, r), a = s || Wd(o), u = !a("as");
  return function() {
    var c = arguments, f = r && t.__emotion_styles !== void 0 ? t.__emotion_styles.slice(0) : [];
    if (i !== void 0 && f.push("label:" + i + ";"), c[0] == null || c[0].raw === void 0)
      f.push.apply(f, c);
    else {
      var m = c[0];
      f.push(m[0]);
      for (var v = c.length, y = 1; y < v; y++)
        f.push(c[y], m[y]);
    }
    var g = ec(function($, p, d) {
      var h = u && $.as || o, x = "", _ = [], E = $;
      if ($.theme == null) {
        E = {};
        for (var k in $)
          E[k] = $[k];
        E.theme = w.useContext(Ir);
      }
      typeof $.className == "string" ? x = lh(p.registered, _, $.className) : $.className != null && (x = $.className + " ");
      var R = Uo(f.concat(_), p.registered, E);
      x += p.key + "-" + R.name, l !== void 0 && (x += " " + l);
      var z = u && s === void 0 ? Wd(h) : a, O = {};
      for (var D in $)
        u && D === "as" || z(D) && (O[D] = $[D]);
      return O.className = x, d && (O.ref = d), /* @__PURE__ */ w.createElement(w.Fragment, null, /* @__PURE__ */ w.createElement(Qv, {
        cache: p,
        serialized: R,
        isStringTag: typeof h == "string"
      }), /* @__PURE__ */ w.createElement(h, O));
    });
    return g.displayName = i !== void 0 ? i : "Styled(" + (typeof o == "string" ? o : o.displayName || o.name || "Component") + ")", g.defaultProps = t.defaultProps, g.__emotion_real = g, g.__emotion_base = o, g.__emotion_styles = f, g.__emotion_forwardProp = s, Object.defineProperty(g, "toString", {
      value: function() {
        return l === void 0 && Hv ? "NO_COMPONENT_SELECTOR" : "." + l;
      }
    }), g.withComponent = function($, p) {
      var d = e($, S({}, n, p, {
        shouldForwardProp: Vd(g, p, !0)
      }));
      return d.apply(void 0, f);
    }, g;
  };
}, Xv = [
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
], Ua = Yv.bind(null);
Xv.forEach(function(e) {
  Ua[e] = Ua(e);
});
function Zv(e, t) {
  const n = th({
    key: "css",
    prepend: e
  });
  if (t) {
    const r = n.insert;
    n.insert = (...o) => (o[1].styles.match(/^@layer\s+[^{]*$/) || (o[1].styles = `@layer mui {${o[1].styles}}`), r(...o));
  }
  return n;
}
const As = /* @__PURE__ */ new Map();
function qv(e) {
  const {
    injectFirst: t,
    enableCssLayer: n,
    children: r
  } = e, o = w.useMemo(() => {
    const i = `${t}-${n}`;
    if (typeof document == "object" && As.has(i))
      return As.get(i);
    const l = Zv(t, n);
    return As.set(i, l), l;
  }, [t, n]);
  return t || n ? /* @__PURE__ */ C.jsx(jv, {
    value: o,
    children: r
  }) : r;
}
function Jv(e) {
  return e == null || Object.keys(e).length === 0;
}
function fh(e) {
  const {
    styles: t,
    defaultTheme: n = {}
  } = e, r = typeof t == "function" ? (o) => t(Jv(o) ? n : o) : t;
  return /* @__PURE__ */ C.jsx(Uv, {
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
function ph(e, t) {
  return Ua(e, t);
}
const e1 = (e, t) => {
  Array.isArray(e.__emotion_styles) && (e.__emotion_styles = t(e.__emotion_styles));
}, Hd = [];
function mh(e) {
  return Hd[0] = e, Uo(Hd);
}
const t1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  GlobalStyles: fh,
  StyledEngineProvider: qv,
  ThemeContext: Ir,
  css: jl,
  default: ph,
  internal_processStyles: e1,
  internal_serializeStyles: mh,
  keyframes: Lr
}, Symbol.toStringTag, { value: "Module" }));
function on(e) {
  if (typeof e != "object" || e === null)
    return !1;
  const t = Object.getPrototypeOf(e);
  return (t === null || t === Object.prototype || Object.getPrototypeOf(t) === null) && !(Symbol.toStringTag in e) && !(Symbol.iterator in e);
}
function hh(e) {
  if (/* @__PURE__ */ w.isValidElement(e) || !on(e))
    return e;
  const t = {};
  return Object.keys(e).forEach((n) => {
    t[n] = hh(e[n]);
  }), t;
}
function At(e, t, n = {
  clone: !0
}) {
  const r = n.clone ? S({}, e) : e;
  return on(e) && on(t) && Object.keys(t).forEach((o) => {
    /* @__PURE__ */ w.isValidElement(t[o]) ? r[o] = t[o] : on(t[o]) && // Avoid prototype pollution
    Object.prototype.hasOwnProperty.call(e, o) && on(e[o]) ? r[o] = At(e[o], t[o], n) : n.clone ? r[o] = on(t[o]) ? hh(t[o]) : t[o] : r[o] = t[o];
  }), r;
}
const n1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: At,
  isPlainObject: on
}, Symbol.toStringTag, { value: "Module" })), r1 = ["values", "unit", "step"], o1 = (e) => {
  const t = Object.keys(e).map((n) => ({
    key: n,
    val: e[n]
  })) || [];
  return t.sort((n, r) => n.val - r.val), t.reduce((n, r) => S({}, n, {
    [r.key]: r.val
  }), {});
};
function gh(e) {
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
  } = e, o = B(e, r1), i = o1(t), l = Object.keys(i);
  function s(m) {
    return `@media (min-width:${typeof t[m] == "number" ? t[m] : m}${n})`;
  }
  function a(m) {
    return `@media (max-width:${(typeof t[m] == "number" ? t[m] : m) - r / 100}${n})`;
  }
  function u(m, v) {
    const y = l.indexOf(v);
    return `@media (min-width:${typeof t[m] == "number" ? t[m] : m}${n}) and (max-width:${(y !== -1 && typeof t[l[y]] == "number" ? t[l[y]] : v) - r / 100}${n})`;
  }
  function c(m) {
    return l.indexOf(m) + 1 < l.length ? u(m, l[l.indexOf(m) + 1]) : s(m);
  }
  function f(m) {
    const v = l.indexOf(m);
    return v === 0 ? s(l[1]) : v === l.length - 1 ? a(l[v]) : u(m, l[l.indexOf(m) + 1]).replace("@media", "@media not all and");
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
const i1 = {
  borderRadius: 4
}, l1 = i1;
function fo(e, t) {
  return t ? At(e, t, {
    clone: !1
    // No need to clone deep, it's way faster.
  }) : e;
}
const nc = {
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
}, Gd = {
  // Sorted ASC by size. That's important.
  // It can't be configured as it's used statically for propTypes.
  keys: ["xs", "sm", "md", "lg", "xl"],
  up: (e) => `@media (min-width:${nc[e]}px)`
};
function yt(e, t, n) {
  const r = e.theme || {};
  if (Array.isArray(t)) {
    const i = r.breakpoints || Gd;
    return t.reduce((l, s, a) => (l[i.up(i.keys[a])] = n(t[a]), l), {});
  }
  if (typeof t == "object") {
    const i = r.breakpoints || Gd;
    return Object.keys(t).reduce((l, s) => {
      if (Object.keys(i.values || nc).indexOf(s) !== -1) {
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
function s1(e = {}) {
  var t;
  return ((t = e.keys) == null ? void 0 : t.reduce((r, o) => {
    const i = e.up(o);
    return r[i] = {}, r;
  }, {})) || {};
}
function Kd(e, t) {
  return e.reduce((n, r) => {
    const o = n[r];
    return (!o || Object.keys(o).length === 0) && delete n[r], n;
  }, t);
}
function a1(e, t) {
  if (typeof e != "object")
    return {};
  const n = {}, r = Object.keys(t);
  return Array.isArray(e) ? r.forEach((o, i) => {
    i < e.length && (n[o] = !0);
  }) : r.forEach((o) => {
    e[o] != null && (n[o] = !0);
  }), n;
}
function Al({
  values: e,
  breakpoints: t,
  base: n
}) {
  const r = n || a1(e, t), o = Object.keys(r);
  if (o.length === 0)
    return e;
  let i;
  return o.reduce((l, s, a) => (Array.isArray(e) ? (l[s] = e[a] != null ? e[a] : e[i], i = a) : typeof e == "object" ? (l[s] = e[s] != null ? e[s] : e[i], i = s) : l[s] = e, l), {});
}
function le(e) {
  if (typeof e != "string")
    throw new Error(Oo(7));
  return e.charAt(0).toUpperCase() + e.slice(1);
}
const u1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: le
}, Symbol.toStringTag, { value: "Module" }));
function Dl(e, t, n = !0) {
  if (!t || typeof t != "string")
    return null;
  if (e && e.vars && n) {
    const r = `vars.${t}`.split(".").reduce((o, i) => o && o[i] ? o[i] : null, e);
    if (r != null)
      return r;
  }
  return t.split(".").reduce((r, o) => r && r[o] != null ? r[o] : null, e);
}
function ol(e, t, n, r = n) {
  let o;
  return typeof e == "function" ? o = e(n) : Array.isArray(e) ? o = e[n] || r : o = Dl(e, n) || r, t && (o = t(o, r, e)), o;
}
function me(e) {
  const {
    prop: t,
    cssProperty: n = e.prop,
    themeKey: r,
    transform: o
  } = e, i = (l) => {
    if (l[t] == null)
      return null;
    const s = l[t], a = l.theme, u = Dl(a, r) || {};
    return yt(l, s, (f) => {
      let m = ol(u, o, f);
      return f === m && typeof f == "string" && (m = ol(u, o, `${t}${f === "default" ? "" : le(f)}`, f)), n === !1 ? m : {
        [n]: m
      };
    });
  };
  return i.propTypes = {}, i.filterProps = [t], i;
}
function c1(e) {
  const t = {};
  return (n) => (t[n] === void 0 && (t[n] = e(n)), t[n]);
}
const d1 = {
  m: "margin",
  p: "padding"
}, f1 = {
  t: "Top",
  r: "Right",
  b: "Bottom",
  l: "Left",
  x: ["Left", "Right"],
  y: ["Top", "Bottom"]
}, Qd = {
  marginX: "mx",
  marginY: "my",
  paddingX: "px",
  paddingY: "py"
}, p1 = c1((e) => {
  if (e.length > 2)
    if (Qd[e])
      e = Qd[e];
    else
      return [e];
  const [t, n] = e.split(""), r = d1[t], o = f1[n] || "";
  return Array.isArray(o) ? o.map((i) => r + i) : [r + o];
}), rc = ["m", "mt", "mr", "mb", "ml", "mx", "my", "margin", "marginTop", "marginRight", "marginBottom", "marginLeft", "marginX", "marginY", "marginInline", "marginInlineStart", "marginInlineEnd", "marginBlock", "marginBlockStart", "marginBlockEnd"], oc = ["p", "pt", "pr", "pb", "pl", "px", "py", "padding", "paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "paddingX", "paddingY", "paddingInline", "paddingInlineStart", "paddingInlineEnd", "paddingBlock", "paddingBlockStart", "paddingBlockEnd"];
[...rc, ...oc];
function Wo(e, t, n, r) {
  var o;
  const i = (o = Dl(e, t, !1)) != null ? o : n;
  return typeof i == "number" ? (l) => typeof l == "string" ? l : i * l : Array.isArray(i) ? (l) => typeof l == "string" ? l : i[l] : typeof i == "function" ? i : () => {
  };
}
function yh(e) {
  return Wo(e, "spacing", 8);
}
function Vo(e, t) {
  if (typeof t == "string" || t == null)
    return t;
  const n = Math.abs(t), r = e(n);
  return t >= 0 ? r : typeof r == "number" ? -r : `-${r}`;
}
function m1(e, t) {
  return (n) => e.reduce((r, o) => (r[o] = Vo(t, n), r), {});
}
function h1(e, t, n, r) {
  if (t.indexOf(n) === -1)
    return null;
  const o = p1(n), i = m1(o, r), l = e[n];
  return yt(e, l, i);
}
function vh(e, t) {
  const n = yh(e.theme);
  return Object.keys(e).map((r) => h1(e, t, r, n)).reduce(fo, {});
}
function ue(e) {
  return vh(e, rc);
}
ue.propTypes = {};
ue.filterProps = rc;
function ce(e) {
  return vh(e, oc);
}
ce.propTypes = {};
ce.filterProps = oc;
function g1(e = 8) {
  if (e.mui)
    return e;
  const t = yh({
    spacing: e
  }), n = (...r) => (r.length === 0 ? [1] : r).map((i) => {
    const l = t(i);
    return typeof l == "number" ? `${l}px` : l;
  }).join(" ");
  return n.mui = !0, n;
}
function Fl(...e) {
  const t = e.reduce((r, o) => (o.filterProps.forEach((i) => {
    r[i] = o;
  }), r), {}), n = (r) => Object.keys(r).reduce((o, i) => t[i] ? fo(o, t[i](r)) : o, {});
  return n.propTypes = {}, n.filterProps = e.reduce((r, o) => r.concat(o.filterProps), []), n;
}
function dt(e) {
  return typeof e != "number" ? e : `${e}px solid`;
}
function xt(e, t) {
  return me({
    prop: e,
    themeKey: "borders",
    transform: t
  });
}
const y1 = xt("border", dt), v1 = xt("borderTop", dt), x1 = xt("borderRight", dt), S1 = xt("borderBottom", dt), w1 = xt("borderLeft", dt), C1 = xt("borderColor"), k1 = xt("borderTopColor"), E1 = xt("borderRightColor"), _1 = xt("borderBottomColor"), $1 = xt("borderLeftColor"), P1 = xt("outline", dt), T1 = xt("outlineColor"), Bl = (e) => {
  if (e.borderRadius !== void 0 && e.borderRadius !== null) {
    const t = Wo(e.theme, "shape.borderRadius", 4), n = (r) => ({
      borderRadius: Vo(t, r)
    });
    return yt(e, e.borderRadius, n);
  }
  return null;
};
Bl.propTypes = {};
Bl.filterProps = ["borderRadius"];
Fl(y1, v1, x1, S1, w1, C1, k1, E1, _1, $1, Bl, P1, T1);
const Ul = (e) => {
  if (e.gap !== void 0 && e.gap !== null) {
    const t = Wo(e.theme, "spacing", 8), n = (r) => ({
      gap: Vo(t, r)
    });
    return yt(e, e.gap, n);
  }
  return null;
};
Ul.propTypes = {};
Ul.filterProps = ["gap"];
const Wl = (e) => {
  if (e.columnGap !== void 0 && e.columnGap !== null) {
    const t = Wo(e.theme, "spacing", 8), n = (r) => ({
      columnGap: Vo(t, r)
    });
    return yt(e, e.columnGap, n);
  }
  return null;
};
Wl.propTypes = {};
Wl.filterProps = ["columnGap"];
const Vl = (e) => {
  if (e.rowGap !== void 0 && e.rowGap !== null) {
    const t = Wo(e.theme, "spacing", 8), n = (r) => ({
      rowGap: Vo(t, r)
    });
    return yt(e, e.rowGap, n);
  }
  return null;
};
Vl.propTypes = {};
Vl.filterProps = ["rowGap"];
const R1 = me({
  prop: "gridColumn"
}), O1 = me({
  prop: "gridRow"
}), M1 = me({
  prop: "gridAutoFlow"
}), N1 = me({
  prop: "gridAutoColumns"
}), I1 = me({
  prop: "gridAutoRows"
}), L1 = me({
  prop: "gridTemplateColumns"
}), z1 = me({
  prop: "gridTemplateRows"
}), b1 = me({
  prop: "gridTemplateAreas"
}), j1 = me({
  prop: "gridArea"
});
Fl(Ul, Wl, Vl, R1, O1, M1, N1, I1, L1, z1, b1, j1);
function gr(e, t) {
  return t === "grey" ? t : e;
}
const A1 = me({
  prop: "color",
  themeKey: "palette",
  transform: gr
}), D1 = me({
  prop: "bgcolor",
  cssProperty: "backgroundColor",
  themeKey: "palette",
  transform: gr
}), F1 = me({
  prop: "backgroundColor",
  themeKey: "palette",
  transform: gr
});
Fl(A1, D1, F1);
function Ze(e) {
  return e <= 1 && e !== 0 ? `${e * 100}%` : e;
}
const B1 = me({
  prop: "width",
  transform: Ze
}), ic = (e) => {
  if (e.maxWidth !== void 0 && e.maxWidth !== null) {
    const t = (n) => {
      var r, o;
      const i = ((r = e.theme) == null || (r = r.breakpoints) == null || (r = r.values) == null ? void 0 : r[n]) || nc[n];
      return i ? ((o = e.theme) == null || (o = o.breakpoints) == null ? void 0 : o.unit) !== "px" ? {
        maxWidth: `${i}${e.theme.breakpoints.unit}`
      } : {
        maxWidth: i
      } : {
        maxWidth: Ze(n)
      };
    };
    return yt(e, e.maxWidth, t);
  }
  return null;
};
ic.filterProps = ["maxWidth"];
const U1 = me({
  prop: "minWidth",
  transform: Ze
}), W1 = me({
  prop: "height",
  transform: Ze
}), V1 = me({
  prop: "maxHeight",
  transform: Ze
}), H1 = me({
  prop: "minHeight",
  transform: Ze
});
me({
  prop: "size",
  cssProperty: "width",
  transform: Ze
});
me({
  prop: "size",
  cssProperty: "height",
  transform: Ze
});
const G1 = me({
  prop: "boxSizing"
});
Fl(B1, ic, U1, W1, V1, H1, G1);
const K1 = {
  // borders
  border: {
    themeKey: "borders",
    transform: dt
  },
  borderTop: {
    themeKey: "borders",
    transform: dt
  },
  borderRight: {
    themeKey: "borders",
    transform: dt
  },
  borderBottom: {
    themeKey: "borders",
    transform: dt
  },
  borderLeft: {
    themeKey: "borders",
    transform: dt
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
    transform: dt
  },
  outlineColor: {
    themeKey: "palette"
  },
  borderRadius: {
    themeKey: "shape.borderRadius",
    style: Bl
  },
  // palette
  color: {
    themeKey: "palette",
    transform: gr
  },
  bgcolor: {
    themeKey: "palette",
    cssProperty: "backgroundColor",
    transform: gr
  },
  backgroundColor: {
    themeKey: "palette",
    transform: gr
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
    style: Ul
  },
  rowGap: {
    style: Vl
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
    transform: Ze
  },
  maxWidth: {
    style: ic
  },
  minWidth: {
    transform: Ze
  },
  height: {
    transform: Ze
  },
  maxHeight: {
    transform: Ze
  },
  minHeight: {
    transform: Ze
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
}, Ho = K1;
function Q1(...e) {
  const t = e.reduce((r, o) => r.concat(Object.keys(o)), []), n = new Set(t);
  return e.every((r) => n.size === Object.keys(r).length);
}
function Y1(e, t) {
  return typeof e == "function" ? e(t) : e;
}
function xh() {
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
    const m = Dl(o, u) || {};
    return f ? f(l) : yt(l, r, (y) => {
      let g = ol(m, c, y);
      return y === g && typeof y == "string" && (g = ol(m, c, `${n}${y === "default" ? "" : le(y)}`, y)), a === !1 ? g : {
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
    const s = (r = i.unstable_sxConfig) != null ? r : Ho;
    function a(u) {
      let c = u;
      if (typeof u == "function")
        c = u(i);
      else if (typeof u != "object")
        return u;
      if (!c)
        return null;
      const f = s1(i.breakpoints), m = Object.keys(f);
      let v = f;
      return Object.keys(c).forEach((y) => {
        const g = Y1(c[y], i);
        if (g != null)
          if (typeof g == "object")
            if (s[y])
              v = fo(v, e(y, g, i, s));
            else {
              const $ = yt({
                theme: i
              }, g, (p) => ({
                [y]: p
              }));
              Q1($, g) ? v[y] = t({
                sx: g,
                theme: i,
                nested: !0
              }) : v = fo(v, $);
            }
          else
            v = fo(v, e(y, g, i, s));
      }), !l && i.modularCssLayers ? {
        "@layer sx": Kd(m, v)
      } : Kd(m, v);
    }
    return Array.isArray(o) ? o.map(a) : a(o);
  }
  return t;
}
const Sh = xh();
Sh.filterProps = ["sx"];
const Hl = Sh;
function wh(e, t) {
  const n = this;
  return n.vars && typeof n.getColorSchemeSelector == "function" ? {
    [n.getColorSchemeSelector(e).replace(/(\[[^\]]+\])/, "*:where($1)")]: t
  } : n.palette.mode === e ? t : {};
}
const X1 = ["breakpoints", "palette", "spacing", "shape"];
function lc(e = {}, ...t) {
  const {
    breakpoints: n = {},
    palette: r = {},
    spacing: o,
    shape: i = {}
  } = e, l = B(e, X1), s = gh(n), a = g1(o);
  let u = At({
    breakpoints: s,
    direction: "ltr",
    components: {},
    // Inject component definitions.
    palette: S({
      mode: "light"
    }, r),
    spacing: a,
    shape: S({}, l1, i)
  }, l);
  return u.applyStyles = wh, u = t.reduce((c, f) => At(c, f), u), u.unstable_sxConfig = S({}, Ho, l == null ? void 0 : l.unstable_sxConfig), u.unstable_sx = function(f) {
    return Hl({
      sx: f,
      theme: this
    });
  }, u;
}
const Z1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: lc,
  private_createBreakpoints: gh,
  unstable_applyStyles: wh
}, Symbol.toStringTag, { value: "Module" }));
function q1(e) {
  return Object.keys(e).length === 0;
}
function sc(e = null) {
  const t = w.useContext(Ir);
  return !t || q1(t) ? e : t;
}
const J1 = lc();
function ac(e = J1) {
  return sc(e);
}
function Ds(e) {
  const t = mh(e);
  return e !== t && t.styles ? (t.styles.match(/^@layer\s+[^{]*$/) || (t.styles = `@layer global{${t.styles}}`), t) : e;
}
function Ch({
  styles: e,
  themeId: t,
  defaultTheme: n = {}
}) {
  const r = ac(n), o = t && r[t] || r;
  let i = typeof e == "function" ? e(o) : e;
  return o.modularCssLayers && (Array.isArray(i) ? i = i.map((l) => Ds(typeof l == "function" ? l(o) : l)) : i = Ds(i)), /* @__PURE__ */ C.jsx(fh, {
    styles: i
  });
}
const ex = ["sx"], tx = (e) => {
  var t, n;
  const r = {
    systemProps: {},
    otherProps: {}
  }, o = (t = e == null || (n = e.theme) == null ? void 0 : n.unstable_sxConfig) != null ? t : Ho;
  return Object.keys(e).forEach((i) => {
    o[i] ? r.systemProps[i] = e[i] : r.otherProps[i] = e[i];
  }), r;
};
function Gl(e) {
  const {
    sx: t
  } = e, n = B(e, ex), {
    systemProps: r,
    otherProps: o
  } = tx(n);
  let i;
  return Array.isArray(t) ? i = [r, ...t] : typeof t == "function" ? i = (...l) => {
    const s = t(...l);
    return on(s) ? S({}, r, s) : r;
  } : i = S({}, r, t), S({}, o, {
    sx: i
  });
}
const nx = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Hl,
  extendSxProp: Gl,
  unstable_createStyleFunctionSx: xh,
  unstable_defaultSxConfig: Ho
}, Symbol.toStringTag, { value: "Module" })), Yd = (e) => e, rx = () => {
  let e = Yd;
  return {
    configure(t) {
      e = t;
    },
    generate(t) {
      return e(t);
    },
    reset() {
      e = Yd;
    }
  };
}, ox = rx(), uc = ox;
function kh(e) {
  var t, n, r = "";
  if (typeof e == "string" || typeof e == "number")
    r += e;
  else if (typeof e == "object")
    if (Array.isArray(e)) {
      var o = e.length;
      for (t = 0; t < o; t++)
        e[t] && (n = kh(e[t])) && (r && (r += " "), r += n);
    } else
      for (n in e)
        e[n] && (r && (r += " "), r += n);
  return r;
}
function V() {
  for (var e, t, n = 0, r = "", o = arguments.length; n < o; n++)
    (e = arguments[n]) && (t = kh(e)) && (r && (r += " "), r += t);
  return r;
}
const ix = ["className", "component"];
function lx(e = {}) {
  const {
    themeId: t,
    defaultTheme: n,
    defaultClassName: r = "MuiBox-root",
    generateClassName: o
  } = e, i = ph("div", {
    shouldForwardProp: (s) => s !== "theme" && s !== "sx" && s !== "as"
  })(Hl);
  return /* @__PURE__ */ w.forwardRef(function(a, u) {
    const c = ac(n), f = Gl(a), {
      className: m,
      component: v = "div"
    } = f, y = B(f, ix);
    return /* @__PURE__ */ C.jsx(i, S({
      as: v,
      ref: u,
      className: V(m, o ? o(r) : r),
      theme: t && c[t] || c
    }, y));
  });
}
const sx = {
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
function Pe(e, t, n = "Mui") {
  const r = sx[t];
  return r ? `${n}-${r}` : `${uc.generate(e)}-${t}`;
}
function Ce(e, t, n = "Mui") {
  const r = {};
  return t.forEach((o) => {
    r[o] = Pe(e, o, n);
  }), r;
}
var Eh = { exports: {} }, Z = {};
/**
 * @license React
 * react-is.production.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var cc = Symbol.for("react.transitional.element"), dc = Symbol.for("react.portal"), Kl = Symbol.for("react.fragment"), Ql = Symbol.for("react.strict_mode"), Yl = Symbol.for("react.profiler"), Xl = Symbol.for("react.consumer"), Zl = Symbol.for("react.context"), ql = Symbol.for("react.forward_ref"), Jl = Symbol.for("react.suspense"), es = Symbol.for("react.suspense_list"), ts = Symbol.for("react.memo"), ns = Symbol.for("react.lazy"), ax = Symbol.for("react.view_transition"), ux = Symbol.for("react.client.reference");
function St(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case cc:
        switch (e = e.type, e) {
          case Kl:
          case Yl:
          case Ql:
          case Jl:
          case es:
          case ax:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Zl:
              case ql:
              case ns:
              case ts:
                return e;
              case Xl:
                return e;
              default:
                return t;
            }
        }
      case dc:
        return t;
    }
  }
}
Z.ContextConsumer = Xl;
Z.ContextProvider = Zl;
Z.Element = cc;
Z.ForwardRef = ql;
Z.Fragment = Kl;
Z.Lazy = ns;
Z.Memo = ts;
Z.Portal = dc;
Z.Profiler = Yl;
Z.StrictMode = Ql;
Z.Suspense = Jl;
Z.SuspenseList = es;
Z.isContextConsumer = function(e) {
  return St(e) === Xl;
};
Z.isContextProvider = function(e) {
  return St(e) === Zl;
};
Z.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === cc;
};
Z.isForwardRef = function(e) {
  return St(e) === ql;
};
Z.isFragment = function(e) {
  return St(e) === Kl;
};
Z.isLazy = function(e) {
  return St(e) === ns;
};
Z.isMemo = function(e) {
  return St(e) === ts;
};
Z.isPortal = function(e) {
  return St(e) === dc;
};
Z.isProfiler = function(e) {
  return St(e) === Yl;
};
Z.isStrictMode = function(e) {
  return St(e) === Ql;
};
Z.isSuspense = function(e) {
  return St(e) === Jl;
};
Z.isSuspenseList = function(e) {
  return St(e) === es;
};
Z.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === Kl || e === Yl || e === Ql || e === Jl || e === es || typeof e == "object" && e !== null && (e.$$typeof === ns || e.$$typeof === ts || e.$$typeof === Zl || e.$$typeof === Xl || e.$$typeof === ql || e.$$typeof === ux || e.getModuleId !== void 0);
};
Z.typeOf = St;
Eh.exports = Z;
var Xd = Eh.exports;
const cx = /^\s*function(?:\s|\s*\/\*.*\*\/\s*)+([^(\s/]*)\s*/;
function _h(e) {
  const t = `${e}`.match(cx);
  return t && t[1] || "";
}
function $h(e, t = "") {
  return e.displayName || e.name || _h(e) || t;
}
function Zd(e, t, n) {
  const r = $h(t);
  return e.displayName || (r !== "" ? `${n}(${r})` : n);
}
function dx(e) {
  if (e != null) {
    if (typeof e == "string")
      return e;
    if (typeof e == "function")
      return $h(e, "Component");
    if (typeof e == "object")
      switch (e.$$typeof) {
        case Xd.ForwardRef:
          return Zd(e, e.render, "ForwardRef");
        case Xd.Memo:
          return Zd(e, e.type, "memo");
        default:
          return;
      }
  }
}
const fx = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: dx,
  getFunctionName: _h
}, Symbol.toStringTag, { value: "Module" }));
function Wa(e, t) {
  const n = S({}, t);
  return Object.keys(e).forEach((r) => {
    if (r.toString().match(/^(components|slots)$/))
      n[r] = S({}, e[r], n[r]);
    else if (r.toString().match(/^(componentsProps|slotProps)$/)) {
      const o = e[r] || {}, i = t[r];
      n[r] = {}, !i || !Object.keys(i) ? n[r] = o : !o || !Object.keys(o) ? n[r] = i : (n[r] = S({}, i), Object.keys(o).forEach((l) => {
        n[r][l] = Wa(o[l], i[l]);
      }));
    } else
      n[r] === void 0 && (n[r] = e[r]);
  }), n;
}
const px = typeof window < "u" ? w.useLayoutEffect : w.useEffect, Go = px;
function mx(e, t = Number.MIN_SAFE_INTEGER, n = Number.MAX_SAFE_INTEGER) {
  return Math.max(t, Math.min(e, n));
}
const hx = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: mx
}, Symbol.toStringTag, { value: "Module" }));
function gx(...e) {
  return e.reduce((t, n) => n == null ? t : function(...o) {
    t.apply(this, o), n.apply(this, o);
  }, () => {
  });
}
function yx(e, t = 166) {
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
function vx(e, t) {
  return () => null;
}
function Ph(e, t) {
  var n, r;
  return /* @__PURE__ */ w.isValidElement(e) && t.indexOf(
    // For server components `muiName` is avaialble in element.type._payload.value.muiName
    // relevant info - https://github.com/facebook/react/blob/2807d781a08db8e9873687fccc25c0f12b4fb3d4/packages/react/src/ReactLazy.js#L45
    // eslint-disable-next-line no-underscore-dangle
    (n = e.type.muiName) != null ? n : (r = e.type) == null || (r = r._payload) == null || (r = r.value) == null ? void 0 : r.muiName
  ) !== -1;
}
function Th(e) {
  return e && e.ownerDocument || document;
}
function xx(e) {
  return Th(e).defaultView || window;
}
function Sx(e, t) {
  return () => null;
}
function Rh(e, t) {
  typeof e == "function" ? e(t) : e && (e.current = t);
}
let qd = 0;
function wx(e) {
  const [t, n] = w.useState(e), r = e || t;
  return w.useEffect(() => {
    t == null && (qd += 1, n(`mui-${qd}`));
  }, [t]), r;
}
const Jd = Hs["useId".toString()];
function Oh(e) {
  if (Jd !== void 0) {
    const t = Jd();
    return e ?? t;
  }
  return wx(e);
}
function Cx(e, t, n, r, o) {
  return null;
}
function kx({
  controlled: e,
  default: t,
  name: n,
  state: r = "value"
}) {
  const {
    current: o
  } = w.useRef(e !== void 0), [i, l] = w.useState(t), s = o ? e : i, a = w.useCallback((u) => {
    o || l(u);
  }, []);
  return [s, a];
}
function eo(e) {
  const t = w.useRef(e);
  return Go(() => {
    t.current = e;
  }), w.useRef((...n) => (
    // @ts-expect-error hide `this`
    (0, t.current)(...n)
  )).current;
}
function jn(...e) {
  return w.useMemo(() => e.every((t) => t == null) ? null : (t) => {
    e.forEach((n) => {
      Rh(n, t);
    });
  }, e);
}
const ef = {};
function Ex(e, t) {
  const n = w.useRef(ef);
  return n.current === ef && (n.current = e(t)), n;
}
const _x = [];
function $x(e) {
  w.useEffect(e, _x);
}
class rs {
  constructor() {
    this.currentId = null, this.clear = () => {
      this.currentId !== null && (clearTimeout(this.currentId), this.currentId = null);
    }, this.disposeEffect = () => this.clear;
  }
  static create() {
    return new rs();
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
function Mh() {
  const e = Ex(rs.create).current;
  return $x(e.disposeEffect), e;
}
let os = !0, Va = !1;
const Px = new rs(), Tx = {
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
function Rx(e) {
  const {
    type: t,
    tagName: n
  } = e;
  return !!(n === "INPUT" && Tx[t] && !e.readOnly || n === "TEXTAREA" && !e.readOnly || e.isContentEditable);
}
function Ox(e) {
  e.metaKey || e.altKey || e.ctrlKey || (os = !0);
}
function Fs() {
  os = !1;
}
function Mx() {
  this.visibilityState === "hidden" && Va && (os = !0);
}
function Nx(e) {
  e.addEventListener("keydown", Ox, !0), e.addEventListener("mousedown", Fs, !0), e.addEventListener("pointerdown", Fs, !0), e.addEventListener("touchstart", Fs, !0), e.addEventListener("visibilitychange", Mx, !0);
}
function Ix(e) {
  const {
    target: t
  } = e;
  try {
    return t.matches(":focus-visible");
  } catch {
  }
  return os || Rx(t);
}
function Nh() {
  const e = w.useCallback((o) => {
    o != null && Nx(o.ownerDocument);
  }, []), t = w.useRef(!1);
  function n() {
    return t.current ? (Va = !0, Px.start(100, () => {
      Va = !1;
    }), t.current = !1, !0) : !1;
  }
  function r(o) {
    return Ix(o) ? (t.current = !0, !0) : !1;
  }
  return {
    isFocusVisibleRef: t,
    onFocus: r,
    onBlur: n,
    ref: e
  };
}
function Ie(e, t, n = void 0) {
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
function Ha(e) {
  return typeof e == "string";
}
function Lx(e, t, n) {
  return e === void 0 || Ha(e) ? t : S({}, t, {
    ownerState: S({}, t.ownerState, n)
  });
}
function zx(e, t = []) {
  if (e === void 0)
    return {};
  const n = {};
  return Object.keys(e).filter((r) => r.match(/^on[A-Z]/) && typeof e[r] == "function" && !t.includes(r)).forEach((r) => {
    n[r] = e[r];
  }), n;
}
function tf(e) {
  if (e === void 0)
    return {};
  const t = {};
  return Object.keys(e).filter((n) => !(n.match(/^on[A-Z]/) && typeof e[n] == "function")).forEach((n) => {
    t[n] = e[n];
  }), t;
}
function bx(e) {
  const {
    getSlotProps: t,
    additionalProps: n,
    externalSlotProps: r,
    externalForwardedProps: o,
    className: i
  } = e;
  if (!t) {
    const v = V(n == null ? void 0 : n.className, i, o == null ? void 0 : o.className, r == null ? void 0 : r.className), y = S({}, n == null ? void 0 : n.style, o == null ? void 0 : o.style, r == null ? void 0 : r.style), g = S({}, n, o, r);
    return v.length > 0 && (g.className = v), Object.keys(y).length > 0 && (g.style = y), {
      props: g,
      internalRef: void 0
    };
  }
  const l = zx(S({}, o, r)), s = tf(r), a = tf(o), u = t(l), c = V(u == null ? void 0 : u.className, n == null ? void 0 : n.className, i, o == null ? void 0 : o.className, r == null ? void 0 : r.className), f = S({}, u == null ? void 0 : u.style, n == null ? void 0 : n.style, o == null ? void 0 : o.style, r == null ? void 0 : r.style), m = S({}, u, n, a, s);
  return c.length > 0 && (m.className = c), Object.keys(f).length > 0 && (m.style = f), {
    props: m,
    internalRef: u.ref
  };
}
function jx(e, t, n) {
  return typeof e == "function" ? e(t, n) : e;
}
const Ax = /* @__PURE__ */ w.createContext(null), Ih = Ax;
function Lh() {
  return w.useContext(Ih);
}
const Dx = typeof Symbol == "function" && Symbol.for, Fx = Dx ? Symbol.for("mui.nested") : "__THEME_NESTED__";
function Bx(e, t) {
  return typeof t == "function" ? t(e) : S({}, e, t);
}
function Ux(e) {
  const {
    children: t,
    theme: n
  } = e, r = Lh(), o = w.useMemo(() => {
    const i = r === null ? n : Bx(r, n);
    return i != null && (i[Fx] = r !== null), i;
  }, [n, r]);
  return /* @__PURE__ */ C.jsx(Ih.Provider, {
    value: o,
    children: t
  });
}
const Wx = ["value"], Vx = /* @__PURE__ */ w.createContext();
function Hx(e) {
  let {
    value: t
  } = e, n = B(e, Wx);
  return /* @__PURE__ */ C.jsx(Vx.Provider, S({
    value: t ?? !0
  }, n));
}
const zh = /* @__PURE__ */ w.createContext(void 0);
function Gx({
  value: e,
  children: t
}) {
  return /* @__PURE__ */ C.jsx(zh.Provider, {
    value: e,
    children: t
  });
}
function Kx(e) {
  const {
    theme: t,
    name: n,
    props: r
  } = e;
  if (!t || !t.components || !t.components[n])
    return r;
  const o = t.components[n];
  return o.defaultProps ? Wa(o.defaultProps, r) : !o.styleOverrides && !o.variants ? Wa(o, r) : r;
}
function Qx({
  props: e,
  name: t
}) {
  const n = w.useContext(zh);
  return Kx({
    props: e,
    name: t,
    theme: {
      components: n
    }
  });
}
function Yx(e) {
  const t = sc(), n = Oh() || "", {
    modularCssLayers: r
  } = e;
  let o = "mui.global, mui.components, mui.theme, mui.custom, mui.sx";
  return !r || t !== null ? o = "" : typeof r == "string" ? o = r.replace(/mui(?!\.)/g, o) : o = `@layer ${o};`, Go(() => {
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
  }, [o, n]), o ? /* @__PURE__ */ C.jsx(Ch, {
    styles: o
  }) : null;
}
const nf = {};
function rf(e, t, n, r = !1) {
  return w.useMemo(() => {
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
function Xx(e) {
  const {
    children: t,
    theme: n,
    themeId: r
  } = e, o = sc(nf), i = Lh() || nf, l = rf(r, o, n), s = rf(r, i, n, !0), a = l.direction === "rtl", u = Yx(l);
  return /* @__PURE__ */ C.jsx(Ux, {
    theme: s,
    children: /* @__PURE__ */ C.jsx(Ir.Provider, {
      value: l,
      children: /* @__PURE__ */ C.jsx(Hx, {
        value: a,
        children: /* @__PURE__ */ C.jsxs(Gx, {
          value: l == null ? void 0 : l.components,
          children: [u, t]
        })
      })
    })
  });
}
function Zx(e, t) {
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
var he = {}, bh = { exports: {} };
(function(e) {
  function t(n) {
    return n && n.__esModule ? n : {
      default: n
    };
  }
  e.exports = t, e.exports.__esModule = !0, e.exports.default = e.exports;
})(bh);
var is = bh.exports;
const qx = /* @__PURE__ */ Qt(Wy), Jx = /* @__PURE__ */ Qt(hx);
var jh = is;
Object.defineProperty(he, "__esModule", {
  value: !0
});
var et = he.alpha = Bh;
he.blend = cS;
he.colorChannel = void 0;
var Ga = he.darken = pc;
he.decomposeColor = vt;
he.emphasize = Uh;
var eS = he.getContrastRatio = iS;
he.getLuminance = il;
he.hexToRgb = Ah;
he.hslToRgb = Fh;
var Ka = he.lighten = mc;
he.private_safeAlpha = lS;
he.private_safeColorChannel = void 0;
he.private_safeDarken = sS;
he.private_safeEmphasize = uS;
he.private_safeLighten = aS;
he.recomposeColor = zr;
he.rgbToHex = oS;
var of = jh(qx), tS = jh(Jx);
function fc(e, t = 0, n = 1) {
  return (0, tS.default)(e, t, n);
}
function Ah(e) {
  e = e.slice(1);
  const t = new RegExp(`.{1,${e.length >= 6 ? 2 : 1}}`, "g");
  let n = e.match(t);
  return n && n[0].length === 1 && (n = n.map((r) => r + r)), n ? `rgb${n.length === 4 ? "a" : ""}(${n.map((r, o) => o < 3 ? parseInt(r, 16) : Math.round(parseInt(r, 16) / 255 * 1e3) / 1e3).join(", ")})` : "";
}
function nS(e) {
  const t = e.toString(16);
  return t.length === 1 ? `0${t}` : t;
}
function vt(e) {
  if (e.type)
    return e;
  if (e.charAt(0) === "#")
    return vt(Ah(e));
  const t = e.indexOf("("), n = e.substring(0, t);
  if (["rgb", "rgba", "hsl", "hsla", "color"].indexOf(n) === -1)
    throw new Error((0, of.default)(9, e));
  let r = e.substring(t + 1, e.length - 1), o;
  if (n === "color") {
    if (r = r.split(" "), o = r.shift(), r.length === 4 && r[3].charAt(0) === "/" && (r[3] = r[3].slice(1)), ["srgb", "display-p3", "a98-rgb", "prophoto-rgb", "rec-2020"].indexOf(o) === -1)
      throw new Error((0, of.default)(10, o));
  } else
    r = r.split(",");
  return r = r.map((i) => parseFloat(i)), {
    type: n,
    values: r,
    colorSpace: o
  };
}
const Dh = (e) => {
  const t = vt(e);
  return t.values.slice(0, 3).map((n, r) => t.type.indexOf("hsl") !== -1 && r !== 0 ? `${n}%` : n).join(" ");
};
he.colorChannel = Dh;
const rS = (e, t) => {
  try {
    return Dh(e);
  } catch {
    return e;
  }
};
he.private_safeColorChannel = rS;
function zr(e) {
  const {
    type: t,
    colorSpace: n
  } = e;
  let {
    values: r
  } = e;
  return t.indexOf("rgb") !== -1 ? r = r.map((o, i) => i < 3 ? parseInt(o, 10) : o) : t.indexOf("hsl") !== -1 && (r[1] = `${r[1]}%`, r[2] = `${r[2]}%`), t.indexOf("color") !== -1 ? r = `${n} ${r.join(" ")}` : r = `${r.join(", ")}`, `${t}(${r})`;
}
function oS(e) {
  if (e.indexOf("#") === 0)
    return e;
  const {
    values: t
  } = vt(e);
  return `#${t.map((n, r) => nS(r === 3 ? Math.round(255 * n) : n)).join("")}`;
}
function Fh(e) {
  e = vt(e);
  const {
    values: t
  } = e, n = t[0], r = t[1] / 100, o = t[2] / 100, i = r * Math.min(o, 1 - o), l = (u, c = (u + n / 30) % 12) => o - i * Math.max(Math.min(c - 3, 9 - c, 1), -1);
  let s = "rgb";
  const a = [Math.round(l(0) * 255), Math.round(l(8) * 255), Math.round(l(4) * 255)];
  return e.type === "hsla" && (s += "a", a.push(t[3])), zr({
    type: s,
    values: a
  });
}
function il(e) {
  e = vt(e);
  let t = e.type === "hsl" || e.type === "hsla" ? vt(Fh(e)).values : e.values;
  return t = t.map((n) => (e.type !== "color" && (n /= 255), n <= 0.03928 ? n / 12.92 : ((n + 0.055) / 1.055) ** 2.4)), Number((0.2126 * t[0] + 0.7152 * t[1] + 0.0722 * t[2]).toFixed(3));
}
function iS(e, t) {
  const n = il(e), r = il(t);
  return (Math.max(n, r) + 0.05) / (Math.min(n, r) + 0.05);
}
function Bh(e, t) {
  return e = vt(e), t = fc(t), (e.type === "rgb" || e.type === "hsl") && (e.type += "a"), e.type === "color" ? e.values[3] = `/${t}` : e.values[3] = t, zr(e);
}
function lS(e, t, n) {
  try {
    return Bh(e, t);
  } catch {
    return e;
  }
}
function pc(e, t) {
  if (e = vt(e), t = fc(t), e.type.indexOf("hsl") !== -1)
    e.values[2] *= 1 - t;
  else if (e.type.indexOf("rgb") !== -1 || e.type.indexOf("color") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] *= 1 - t;
  return zr(e);
}
function sS(e, t, n) {
  try {
    return pc(e, t);
  } catch {
    return e;
  }
}
function mc(e, t) {
  if (e = vt(e), t = fc(t), e.type.indexOf("hsl") !== -1)
    e.values[2] += (100 - e.values[2]) * t;
  else if (e.type.indexOf("rgb") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] += (255 - e.values[n]) * t;
  else if (e.type.indexOf("color") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] += (1 - e.values[n]) * t;
  return zr(e);
}
function aS(e, t, n) {
  try {
    return mc(e, t);
  } catch {
    return e;
  }
}
function Uh(e, t = 0.15) {
  return il(e) > 0.5 ? pc(e, t) : mc(e, t);
}
function uS(e, t, n) {
  try {
    return Uh(e, t);
  } catch {
    return e;
  }
}
function cS(e, t, n, r = 1) {
  const o = (a, u) => Math.round((a ** (1 / r) * (1 - n) + u ** (1 / r) * n) ** r), i = vt(e), l = vt(t), s = [o(i.values[0], l.values[0]), o(i.values[1], l.values[1]), o(i.values[2], l.values[2])];
  return zr({
    type: "rgb",
    values: s
  });
}
const dS = {
  black: "#000",
  white: "#fff"
}, Lo = dS, fS = {
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
}, pS = fS, mS = {
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
}, Un = mS, hS = {
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
}, Wn = hS, gS = {
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
}, Qr = gS, yS = {
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
}, Vn = yS, vS = {
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
}, Hn = vS, xS = {
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
}, Gn = xS, SS = ["mode", "contrastThreshold", "tonalOffset"], lf = {
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
    paper: Lo.white,
    default: Lo.white
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
}, Bs = {
  text: {
    primary: Lo.white,
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
    active: Lo.white,
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
function sf(e, t, n, r) {
  const o = r.light || r, i = r.dark || r * 1.5;
  e[t] || (e.hasOwnProperty(n) ? e[t] = e[n] : t === "light" ? e.light = Ka(e.main, o) : t === "dark" && (e.dark = Ga(e.main, i)));
}
function wS(e = "light") {
  return e === "dark" ? {
    main: Vn[200],
    light: Vn[50],
    dark: Vn[400]
  } : {
    main: Vn[700],
    light: Vn[400],
    dark: Vn[800]
  };
}
function CS(e = "light") {
  return e === "dark" ? {
    main: Un[200],
    light: Un[50],
    dark: Un[400]
  } : {
    main: Un[500],
    light: Un[300],
    dark: Un[700]
  };
}
function kS(e = "light") {
  return e === "dark" ? {
    main: Wn[500],
    light: Wn[300],
    dark: Wn[700]
  } : {
    main: Wn[700],
    light: Wn[400],
    dark: Wn[800]
  };
}
function ES(e = "light") {
  return e === "dark" ? {
    main: Hn[400],
    light: Hn[300],
    dark: Hn[700]
  } : {
    main: Hn[700],
    light: Hn[500],
    dark: Hn[900]
  };
}
function _S(e = "light") {
  return e === "dark" ? {
    main: Gn[400],
    light: Gn[300],
    dark: Gn[700]
  } : {
    main: Gn[800],
    light: Gn[500],
    dark: Gn[900]
  };
}
function $S(e = "light") {
  return e === "dark" ? {
    main: Qr[400],
    light: Qr[300],
    dark: Qr[700]
  } : {
    main: "#ed6c02",
    // closest to orange[800] that pass 3:1.
    light: Qr[500],
    dark: Qr[900]
  };
}
function PS(e) {
  const {
    mode: t = "light",
    contrastThreshold: n = 3,
    tonalOffset: r = 0.2
  } = e, o = B(e, SS), i = e.primary || wS(t), l = e.secondary || CS(t), s = e.error || kS(t), a = e.info || ES(t), u = e.success || _S(t), c = e.warning || $S(t);
  function f(g) {
    return eS(g, Bs.text.primary) >= n ? Bs.text.primary : lf.text.primary;
  }
  const m = ({
    color: g,
    name: $,
    mainShade: p = 500,
    lightShade: d = 300,
    darkShade: h = 700
  }) => {
    if (g = S({}, g), !g.main && g[p] && (g.main = g[p]), !g.hasOwnProperty("main"))
      throw new Error(Oo(11, $ ? ` (${$})` : "", p));
    if (typeof g.main != "string")
      throw new Error(Oo(12, $ ? ` (${$})` : "", JSON.stringify(g.main)));
    return sf(g, "light", d, r), sf(g, "dark", h, r), g.contrastText || (g.contrastText = f(g.main)), g;
  }, v = {
    dark: Bs,
    light: lf
  };
  return At(S({
    // A collection of common colors.
    common: S({}, Lo),
    // prevent mutable object.
    // The palette mode, can be light or dark.
    mode: t,
    // The colors used to represent primary interface elements for a user.
    primary: m({
      color: i,
      name: "primary"
    }),
    // The colors used to represent secondary interface elements for a user.
    secondary: m({
      color: l,
      name: "secondary",
      mainShade: "A400",
      lightShade: "A200",
      darkShade: "A700"
    }),
    // The colors used to represent interface elements that the user should be made aware of.
    error: m({
      color: s,
      name: "error"
    }),
    // The colors used to represent potentially dangerous actions or important messages.
    warning: m({
      color: c,
      name: "warning"
    }),
    // The colors used to present information to the user that is neutral and not necessarily important.
    info: m({
      color: a,
      name: "info"
    }),
    // The colors used to indicate the successful completion of an action that user triggered.
    success: m({
      color: u,
      name: "success"
    }),
    // The grey colors.
    grey: pS,
    // Used by `getContrastText()` to maximize the contrast between
    // the background and the text.
    contrastThreshold: n,
    // Takes a background color and returns the text color that maximizes the contrast.
    getContrastText: f,
    // Generate a rich color object.
    augmentColor: m,
    // Used by the functions below to shift a color's luminance by approximately
    // two indexes within its tonal palette.
    // E.g., shift from Red 500 to Red 300 or Red 700.
    tonalOffset: r
  }, v[t]), o);
}
const TS = ["fontFamily", "fontSize", "fontWeightLight", "fontWeightRegular", "fontWeightMedium", "fontWeightBold", "htmlFontSize", "allVariants", "pxToRem"];
function RS(e) {
  return Math.round(e * 1e5) / 1e5;
}
const af = {
  textTransform: "uppercase"
}, uf = '"Roboto", "Helvetica", "Arial", sans-serif';
function OS(e, t) {
  const n = typeof t == "function" ? t(e) : t, {
    fontFamily: r = uf,
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
  } = n, m = B(n, TS), v = o / 14, y = f || ((p) => `${p / u * v}rem`), g = (p, d, h, x, _) => S({
    fontFamily: r,
    fontWeight: p,
    fontSize: y(d),
    // Unitless following https://meyerweb.com/eric/thoughts/2006/02/08/unitless-line-heights/
    lineHeight: h
  }, r === uf ? {
    letterSpacing: `${RS(x / d)}em`
  } : {}, _, c), $ = {
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
    button: g(s, 14, 1.75, 0.4, af),
    caption: g(l, 12, 1.66, 0.4),
    overline: g(l, 12, 2.66, 1, af),
    // TODO v6: Remove handling of 'inherit' variant from the theme as it is already handled in Material UI's Typography component. Also, remember to remove the associated types.
    inherit: {
      fontFamily: "inherit",
      fontWeight: "inherit",
      fontSize: "inherit",
      lineHeight: "inherit",
      letterSpacing: "inherit"
    }
  };
  return At(S({
    htmlFontSize: u,
    pxToRem: y,
    fontFamily: r,
    fontSize: o,
    fontWeightLight: i,
    fontWeightRegular: l,
    fontWeightMedium: s,
    fontWeightBold: a
  }, $), m, {
    clone: !1
    // No need to clone deep
  });
}
const MS = 0.2, NS = 0.14, IS = 0.12;
function ne(...e) {
  return [`${e[0]}px ${e[1]}px ${e[2]}px ${e[3]}px rgba(0,0,0,${MS})`, `${e[4]}px ${e[5]}px ${e[6]}px ${e[7]}px rgba(0,0,0,${NS})`, `${e[8]}px ${e[9]}px ${e[10]}px ${e[11]}px rgba(0,0,0,${IS})`].join(",");
}
const LS = ["none", ne(0, 2, 1, -1, 0, 1, 1, 0, 0, 1, 3, 0), ne(0, 3, 1, -2, 0, 2, 2, 0, 0, 1, 5, 0), ne(0, 3, 3, -2, 0, 3, 4, 0, 0, 1, 8, 0), ne(0, 2, 4, -1, 0, 4, 5, 0, 0, 1, 10, 0), ne(0, 3, 5, -1, 0, 5, 8, 0, 0, 1, 14, 0), ne(0, 3, 5, -1, 0, 6, 10, 0, 0, 1, 18, 0), ne(0, 4, 5, -2, 0, 7, 10, 1, 0, 2, 16, 1), ne(0, 5, 5, -3, 0, 8, 10, 1, 0, 3, 14, 2), ne(0, 5, 6, -3, 0, 9, 12, 1, 0, 3, 16, 2), ne(0, 6, 6, -3, 0, 10, 14, 1, 0, 4, 18, 3), ne(0, 6, 7, -4, 0, 11, 15, 1, 0, 4, 20, 3), ne(0, 7, 8, -4, 0, 12, 17, 2, 0, 5, 22, 4), ne(0, 7, 8, -4, 0, 13, 19, 2, 0, 5, 24, 4), ne(0, 7, 9, -4, 0, 14, 21, 2, 0, 5, 26, 4), ne(0, 8, 9, -5, 0, 15, 22, 2, 0, 6, 28, 5), ne(0, 8, 10, -5, 0, 16, 24, 2, 0, 6, 30, 5), ne(0, 8, 11, -5, 0, 17, 26, 2, 0, 6, 32, 5), ne(0, 9, 11, -5, 0, 18, 28, 2, 0, 7, 34, 6), ne(0, 9, 12, -6, 0, 19, 29, 2, 0, 7, 36, 6), ne(0, 10, 13, -6, 0, 20, 31, 3, 0, 8, 38, 7), ne(0, 10, 13, -6, 0, 21, 33, 3, 0, 8, 40, 7), ne(0, 10, 14, -6, 0, 22, 35, 3, 0, 8, 42, 7), ne(0, 11, 14, -7, 0, 23, 36, 3, 0, 9, 44, 8), ne(0, 11, 15, -7, 0, 24, 38, 3, 0, 9, 46, 8)], zS = LS, bS = ["duration", "easing", "delay"], jS = {
  // This is the most common easing curve.
  easeInOut: "cubic-bezier(0.4, 0, 0.2, 1)",
  // Objects enter the screen at full velocity from off-screen and
  // slowly decelerate to a resting point.
  easeOut: "cubic-bezier(0.0, 0, 0.2, 1)",
  // Objects leave the screen at full velocity. They do not decelerate when off-screen.
  easeIn: "cubic-bezier(0.4, 0, 1, 1)",
  // The sharp curve is used by objects that may return to the screen at any time.
  sharp: "cubic-bezier(0.4, 0, 0.6, 1)"
}, Wh = {
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
function cf(e) {
  return `${Math.round(e)}ms`;
}
function AS(e) {
  if (!e)
    return 0;
  const t = e / 36;
  return Math.round((4 + 15 * t ** 0.25 + t / 5) * 10);
}
function DS(e) {
  const t = S({}, jS, e.easing), n = S({}, Wh, e.duration);
  return S({
    getAutoHeightDuration: AS,
    create: (o = ["all"], i = {}) => {
      const {
        duration: l = n.standard,
        easing: s = t.easeInOut,
        delay: a = 0
      } = i;
      return B(i, bS), (Array.isArray(o) ? o : [o]).map((u) => `${u} ${typeof l == "string" ? l : cf(l)} ${s} ${typeof a == "string" ? a : cf(a)}`).join(",");
    }
  }, e, {
    easing: t,
    duration: n
  });
}
const FS = {
  mobileStepper: 1e3,
  fab: 1050,
  speedDial: 1050,
  appBar: 1100,
  drawer: 1200,
  modal: 1300,
  snackbar: 1400,
  tooltip: 1500
}, BS = FS, US = ["breakpoints", "mixins", "spacing", "palette", "transitions", "typography", "shape"];
function hc(e = {}, ...t) {
  const {
    mixins: n = {},
    palette: r = {},
    transitions: o = {},
    typography: i = {}
  } = e, l = B(e, US);
  if (e.vars && // The error should throw only for the root theme creation because user is not allowed to use a custom node `vars`.
  // `generateCssVars` is the closest identifier for checking that the `options` is a result of `extendTheme` with CSS variables so that user can create new theme for nested ThemeProvider.
  e.generateCssVars === void 0)
    throw new Error(Oo(18));
  const s = PS(r), a = lc(e);
  let u = At(a, {
    mixins: Zx(a.breakpoints, n),
    palette: s,
    // Don't use [...shadows] until you've verified its transpiled code is not invoking the iterator protocol.
    shadows: zS.slice(),
    typography: OS(s, i),
    transitions: DS(o),
    zIndex: S({}, BS)
  });
  return u = At(u, l), u = t.reduce((c, f) => At(c, f), u), u.unstable_sxConfig = S({}, Ho, l == null ? void 0 : l.unstable_sxConfig), u.unstable_sx = function(f) {
    return Hl({
      sx: f,
      theme: this
    });
  }, u;
}
const WS = hc(), gc = WS;
function Vh() {
  const e = ac(gc);
  return e[_r] || e;
}
var Ko = {}, Us = { exports: {} }, df;
function VS() {
  return df || (df = 1, function(e) {
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
  }(Us)), Us.exports;
}
const HS = /* @__PURE__ */ Qt(t1), GS = /* @__PURE__ */ Qt(n1), KS = /* @__PURE__ */ Qt(u1), QS = /* @__PURE__ */ Qt(fx), YS = /* @__PURE__ */ Qt(Z1), XS = /* @__PURE__ */ Qt(nx);
var br = is;
Object.defineProperty(Ko, "__esModule", {
  value: !0
});
var ZS = Ko.default = cw;
Ko.shouldForwardProp = Mi;
Ko.systemDefaultTheme = void 0;
var st = br(dh()), Qa = br(VS()), ll = ow(HS), qS = GS;
br(KS);
br(QS);
var JS = br(YS), ew = br(XS);
const tw = ["ownerState"], nw = ["variants"], rw = ["name", "slot", "skipVariantsResolver", "skipSx", "overridesResolver"];
function Hh(e) {
  if (typeof WeakMap != "function")
    return null;
  var t = /* @__PURE__ */ new WeakMap(), n = /* @__PURE__ */ new WeakMap();
  return (Hh = function(r) {
    return r ? n : t;
  })(e);
}
function ow(e, t) {
  if (!t && e && e.__esModule)
    return e;
  if (e === null || typeof e != "object" && typeof e != "function")
    return { default: e };
  var n = Hh(t);
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
function iw(e) {
  return Object.keys(e).length === 0;
}
function lw(e) {
  return typeof e == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  e.charCodeAt(0) > 96;
}
function Mi(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
function ff(e, t) {
  return t && e && typeof e == "object" && e.styles && !e.styles.startsWith("@layer") && (e.styles = `@layer ${t}{${String(e.styles)}}`), e;
}
const sw = Ko.systemDefaultTheme = (0, JS.default)(), aw = (e) => e && e.charAt(0).toLowerCase() + e.slice(1);
function hi({
  defaultTheme: e,
  theme: t,
  themeId: n
}) {
  return iw(t) ? e : t[n] || t;
}
function uw(e) {
  return e ? (t, n) => n[e] : null;
}
function Ni(e, t, n) {
  let {
    ownerState: r
  } = t, o = (0, Qa.default)(t, tw);
  const i = typeof e == "function" ? e((0, st.default)({
    ownerState: r
  }, o)) : e;
  if (Array.isArray(i))
    return i.flatMap((l) => Ni(l, (0, st.default)({
      ownerState: r
    }, o), n));
  if (i && typeof i == "object" && Array.isArray(i.variants)) {
    const {
      variants: l = []
    } = i;
    let a = (0, Qa.default)(i, nw);
    return l.forEach((u) => {
      let c = !0;
      if (typeof u.props == "function" ? c = u.props((0, st.default)({
        ownerState: r
      }, o, r)) : Object.keys(u.props).forEach((f) => {
        (r == null ? void 0 : r[f]) !== u.props[f] && o[f] !== u.props[f] && (c = !1);
      }), c) {
        Array.isArray(a) || (a = [a]);
        const f = typeof u.style == "function" ? u.style((0, st.default)({
          ownerState: r
        }, o, r)) : u.style;
        a.push(n ? ff((0, ll.internal_serializeStyles)(f), n) : f);
      }
    }), a;
  }
  return n ? ff((0, ll.internal_serializeStyles)(i), n) : i;
}
function cw(e = {}) {
  const {
    themeId: t,
    defaultTheme: n = sw,
    rootShouldForwardProp: r = Mi,
    slotShouldForwardProp: o = Mi
  } = e, i = (l) => (0, ew.default)((0, st.default)({}, l, {
    theme: hi((0, st.default)({}, l, {
      defaultTheme: n,
      themeId: t
    }))
  }));
  return i.__mui_systemSx = !0, (l, s = {}) => {
    (0, ll.internal_processStyles)(l, (E) => E.filter((k) => !(k != null && k.__mui_systemSx)));
    const {
      name: a,
      slot: u,
      skipVariantsResolver: c,
      skipSx: f,
      // TODO v6: remove `lowercaseFirstLetter()` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      overridesResolver: m = uw(aw(u))
    } = s, v = (0, Qa.default)(s, rw), y = a && a.startsWith("Mui") || u ? "components" : "custom", g = c !== void 0 ? c : (
      // TODO v6: remove `Root` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      u && u !== "Root" && u !== "root" || !1
    ), $ = f || !1;
    let p, d = Mi;
    u === "Root" || u === "root" ? d = r : u ? d = o : lw(l) && (d = void 0);
    const h = (0, ll.default)(l, (0, st.default)({
      shouldForwardProp: d,
      label: p
    }, v)), x = (E) => typeof E == "function" && E.__emotion_real !== E || (0, qS.isPlainObject)(E) ? (k) => {
      const R = hi({
        theme: k.theme,
        defaultTheme: n,
        themeId: t
      });
      return Ni(E, (0, st.default)({}, k, {
        theme: R
      }), R.modularCssLayers ? y : void 0);
    } : E, _ = (E, ...k) => {
      let R = x(E);
      const z = k ? k.map(x) : [];
      a && m && z.push((F) => {
        const j = hi((0, st.default)({}, F, {
          defaultTheme: n,
          themeId: t
        }));
        if (!j.components || !j.components[a] || !j.components[a].styleOverrides)
          return null;
        const X = j.components[a].styleOverrides, te = {};
        return Object.entries(X).forEach(([ge, fe]) => {
          te[ge] = Ni(fe, (0, st.default)({}, F, {
            theme: j
          }), j.modularCssLayers ? "theme" : void 0);
        }), m(F, te);
      }), a && !g && z.push((F) => {
        var j;
        const X = hi((0, st.default)({}, F, {
          defaultTheme: n,
          themeId: t
        })), te = X == null || (j = X.components) == null || (j = j[a]) == null ? void 0 : j.variants;
        return Ni({
          variants: te
        }, (0, st.default)({}, F, {
          theme: X
        }), X.modularCssLayers ? "theme" : void 0);
      }), $ || z.push(i);
      const O = z.length - k.length;
      if (Array.isArray(E) && O > 0) {
        const F = new Array(O).fill("");
        R = [...E, ...F], R.raw = [...E.raw, ...F];
      }
      const D = h(R, ...z);
      return l.muiName && (D.muiName = l.muiName), D;
    };
    return h.withConfig && (_.withConfig = h.withConfig), _;
  };
}
function dw(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
const fw = (e) => dw(e) && e !== "classes", Gh = fw, pw = ZS({
  themeId: _r,
  defaultTheme: gc,
  rootShouldForwardProp: Gh
}), Y = pw, mw = ["theme"];
function hw(e) {
  let {
    theme: t
  } = e, n = B(e, mw);
  const r = t[_r];
  let o = r || t;
  return typeof t != "function" && (r && !r.vars ? o = S({}, r, {
    vars: null
  }) : t && !t.vars && (o = S({}, t, {
    vars: null
  }))), /* @__PURE__ */ C.jsx(Xx, S({}, n, {
    themeId: r ? _r : void 0,
    theme: o
  }));
}
const gw = (e) => {
  let t;
  return e < 1 ? t = 5.11916 * e ** 2 : t = 4.5 * Math.log(e + 1) + 2, (t / 100).toFixed(2);
}, pf = gw;
function ke(e) {
  return Qx(e);
}
function yw(e) {
  return /* @__PURE__ */ C.jsx(Ch, S({}, e, {
    defaultTheme: gc,
    themeId: _r
  }));
}
const vw = (e, t) => S({
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
}), xw = (e) => S({
  color: (e.vars || e).palette.text.primary
}, e.typography.body1, {
  backgroundColor: (e.vars || e).palette.background.default,
  "@media print": {
    // Save printer ink.
    backgroundColor: (e.vars || e).palette.common.white
  }
}), Sw = (e, t = !1) => {
  var n;
  const r = {};
  t && e.colorSchemes && Object.entries(e.colorSchemes).forEach(([l, s]) => {
    var a;
    r[e.getColorSchemeSelector(l).replace(/\s*&/, "")] = {
      colorScheme: (a = s.palette) == null ? void 0 : a.mode
    };
  });
  let o = S({
    html: vw(e, t),
    "*, *::before, *::after": {
      boxSizing: "inherit"
    },
    "strong, b": {
      fontWeight: e.typography.fontWeightBold
    },
    body: S({
      margin: 0
    }, xw(e), {
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
function ww(e) {
  const t = ke({
    props: e,
    name: "MuiCssBaseline"
  }), {
    children: n,
    enableColorScheme: r = !1
  } = t;
  return /* @__PURE__ */ C.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ C.jsx(yw, {
      styles: (o) => Sw(o, r)
    }), n]
  });
}
function Cw(e) {
  return Pe("MuiCircularProgress", e);
}
Ce("MuiCircularProgress", ["root", "determinate", "indeterminate", "colorPrimary", "colorSecondary", "svg", "circle", "circleDeterminate", "circleIndeterminate", "circleDisableShrink"]);
const kw = ["className", "color", "disableShrink", "size", "style", "thickness", "value", "variant"];
let ls = (e) => e, mf, hf, gf, yf;
const Jt = 44, Ew = Lr(mf || (mf = ls`
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
`)), _w = Lr(hf || (hf = ls`
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
`)), $w = (e) => {
  const {
    classes: t,
    variant: n,
    color: r,
    disableShrink: o
  } = e, i = {
    root: ["root", n, `color${le(r)}`],
    svg: ["svg"],
    circle: ["circle", `circle${le(n)}`, o && "circleDisableShrink"]
  };
  return Ie(i, Cw, t);
}, Pw = Y("span", {
  name: "MuiCircularProgress",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[n.variant], t[`color${le(n.color)}`]];
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
}) => e.variant === "indeterminate" && jl(gf || (gf = ls`
      animation: ${0} 1.4s linear infinite;
    `), Ew)), Tw = Y("svg", {
  name: "MuiCircularProgress",
  slot: "Svg",
  overridesResolver: (e, t) => t.svg
})({
  display: "block"
  // Keeps the progress centered
}), Rw = Y("circle", {
  name: "MuiCircularProgress",
  slot: "Circle",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.circle, t[`circle${le(n.variant)}`], n.disableShrink && t.circleDisableShrink];
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
}) => e.variant === "indeterminate" && !e.disableShrink && jl(yf || (yf = ls`
      animation: ${0} 1.4s ease-in-out infinite;
    `), _w)), Ow = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
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
  } = r, m = B(r, kw), v = S({}, r, {
    color: i,
    disableShrink: l,
    size: s,
    thickness: u,
    value: c,
    variant: f
  }), y = $w(v), g = {}, $ = {}, p = {};
  if (f === "determinate") {
    const d = 2 * Math.PI * ((Jt - u) / 2);
    g.strokeDasharray = d.toFixed(3), p["aria-valuenow"] = Math.round(c), g.strokeDashoffset = `${((100 - c) / 100 * d).toFixed(3)}px`, $.transform = "rotate(-90deg)";
  }
  return /* @__PURE__ */ C.jsx(Pw, S({
    className: V(y.root, o),
    style: S({
      width: s,
      height: s
    }, $, a),
    ownerState: v,
    ref: n,
    role: "progressbar"
  }, p, m, {
    children: /* @__PURE__ */ C.jsx(Tw, {
      className: y.svg,
      ownerState: v,
      viewBox: `${Jt / 2} ${Jt / 2} ${Jt} ${Jt}`,
      children: /* @__PURE__ */ C.jsx(Rw, {
        className: y.circle,
        style: g,
        ownerState: v,
        cx: Jt,
        cy: Jt,
        r: (Jt - u) / 2,
        fill: "none",
        strokeWidth: u
      })
    })
  }));
}), Mw = Ow, Nw = ["className", "elementType", "ownerState", "externalForwardedProps", "getSlotOwnerState", "internalForwardedProps"], Iw = ["component", "slots", "slotProps"], Lw = ["component"];
function vf(e, t) {
  const {
    className: n,
    elementType: r,
    ownerState: o,
    externalForwardedProps: i,
    getSlotOwnerState: l,
    internalForwardedProps: s
  } = t, a = B(t, Nw), {
    component: u,
    slots: c = {
      [e]: void 0
    },
    slotProps: f = {
      [e]: void 0
    }
  } = i, m = B(i, Iw), v = c[e] || r, y = jx(f[e], o), g = bx(S({
    className: n
  }, a, {
    externalForwardedProps: e === "root" ? m : void 0,
    externalSlotProps: y
  })), {
    props: {
      component: $
    },
    internalRef: p
  } = g, d = B(g.props, Lw), h = jn(p, y == null ? void 0 : y.ref, t.ref), x = l ? l(d) : {}, _ = S({}, o, x), E = e === "root" ? $ || u : $, k = Lx(v, S({}, e === "root" && !u && !c[e] && s, e !== "root" && !c[e] && s, d, E && {
    as: E
  }, {
    ref: h
  }), _);
  return Object.keys(x).forEach((R) => {
    delete k[R];
  }), [v, k];
}
function zw(e) {
  return Pe("MuiPaper", e);
}
Ce("MuiPaper", ["root", "rounded", "outlined", "elevation", "elevation0", "elevation1", "elevation2", "elevation3", "elevation4", "elevation5", "elevation6", "elevation7", "elevation8", "elevation9", "elevation10", "elevation11", "elevation12", "elevation13", "elevation14", "elevation15", "elevation16", "elevation17", "elevation18", "elevation19", "elevation20", "elevation21", "elevation22", "elevation23", "elevation24"]);
const bw = ["className", "component", "elevation", "square", "variant"], jw = (e) => {
  const {
    square: t,
    elevation: n,
    variant: r,
    classes: o
  } = e, i = {
    root: ["root", r, !t && "rounded", r === "elevation" && `elevation${n}`]
  };
  return Ie(i, zw, o);
}, Aw = Y("div", {
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
    backgroundImage: `linear-gradient(${et("#fff", pf(t.elevation))}, ${et("#fff", pf(t.elevation))})`
  }, e.vars && {
    backgroundImage: (n = e.vars.overlays) == null ? void 0 : n[t.elevation]
  }));
}), Dw = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
    props: t,
    name: "MuiPaper"
  }), {
    className: o,
    component: i = "div",
    elevation: l = 1,
    square: s = !1,
    variant: a = "elevation"
  } = r, u = B(r, bw), c = S({}, r, {
    component: i,
    elevation: l,
    square: s,
    variant: a
  }), f = jw(c);
  return /* @__PURE__ */ C.jsx(Aw, S({
    as: i,
    ownerState: c,
    className: V(f.root, o),
    ref: n
  }, u));
}), Pr = Dw;
function Fw(e) {
  return Pe("MuiAlert", e);
}
const Bw = Ce("MuiAlert", ["root", "action", "icon", "message", "filled", "colorSuccess", "colorInfo", "colorWarning", "colorError", "filledSuccess", "filledInfo", "filledWarning", "filledError", "outlined", "outlinedSuccess", "outlinedInfo", "outlinedWarning", "outlinedError", "standard", "standardSuccess", "standardInfo", "standardWarning", "standardError"]), xf = Bw;
function Ya(e, t) {
  return Ya = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, r) {
    return n.__proto__ = r, n;
  }, Ya(e, t);
}
function Kh(e, t) {
  e.prototype = Object.create(t.prototype), e.prototype.constructor = e, Ya(e, t);
}
const Sf = {
  disabled: !1
}, sl = qe.createContext(null);
var Uw = function(t) {
  return t.scrollTop;
}, to = "unmounted", En = "exited", _n = "entering", Qn = "entered", Xa = "exiting", Xt = /* @__PURE__ */ function(e) {
  Kh(t, e);
  function t(r, o) {
    var i;
    i = e.call(this, r, o) || this;
    var l = o, s = l && !l.isMounting ? r.enter : r.appear, a;
    return i.appearStatus = null, r.in ? s ? (a = En, i.appearStatus = _n) : a = Qn : r.unmountOnExit || r.mountOnEnter ? a = to : a = En, i.state = {
      status: a
    }, i.nextCallback = null, i;
  }
  t.getDerivedStateFromProps = function(o, i) {
    var l = o.in;
    return l && i.status === to ? {
      status: En
    } : null;
  };
  var n = t.prototype;
  return n.componentDidMount = function() {
    this.updateStatus(!0, this.appearStatus);
  }, n.componentDidUpdate = function(o) {
    var i = null;
    if (o !== this.props) {
      var l = this.state.status;
      this.props.in ? l !== _n && l !== Qn && (i = _n) : (l === _n || l === Qn) && (i = Xa);
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
      if (this.cancelNextCallback(), i === _n) {
        if (this.props.unmountOnExit || this.props.mountOnEnter) {
          var l = this.props.nodeRef ? this.props.nodeRef.current : pi.findDOMNode(this);
          l && Uw(l);
        }
        this.performEnter(o);
      } else
        this.performExit();
    else
      this.props.unmountOnExit && this.state.status === En && this.setState({
        status: to
      });
  }, n.performEnter = function(o) {
    var i = this, l = this.props.enter, s = this.context ? this.context.isMounting : o, a = this.props.nodeRef ? [s] : [pi.findDOMNode(this), s], u = a[0], c = a[1], f = this.getTimeouts(), m = s ? f.appear : f.enter;
    if (!o && !l || Sf.disabled) {
      this.safeSetState({
        status: Qn
      }, function() {
        i.props.onEntered(u);
      });
      return;
    }
    this.props.onEnter(u, c), this.safeSetState({
      status: _n
    }, function() {
      i.props.onEntering(u, c), i.onTransitionEnd(m, function() {
        i.safeSetState({
          status: Qn
        }, function() {
          i.props.onEntered(u, c);
        });
      });
    });
  }, n.performExit = function() {
    var o = this, i = this.props.exit, l = this.getTimeouts(), s = this.props.nodeRef ? void 0 : pi.findDOMNode(this);
    if (!i || Sf.disabled) {
      this.safeSetState({
        status: En
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
          status: En
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
    var l = this.props.nodeRef ? this.props.nodeRef.current : pi.findDOMNode(this), s = o == null && !this.props.addEndListener;
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
    if (o === to)
      return null;
    var i = this.props, l = i.children;
    i.in, i.mountOnEnter, i.unmountOnExit, i.appear, i.enter, i.exit, i.timeout, i.addEndListener, i.onEnter, i.onEntering, i.onEntered, i.onExit, i.onExiting, i.onExited, i.nodeRef;
    var s = B(i, ["children", "in", "mountOnEnter", "unmountOnExit", "appear", "enter", "exit", "timeout", "addEndListener", "onEnter", "onEntering", "onEntered", "onExit", "onExiting", "onExited", "nodeRef"]);
    return (
      // allows for nested Transitions
      /* @__PURE__ */ qe.createElement(sl.Provider, {
        value: null
      }, typeof l == "function" ? l(o, s) : qe.cloneElement(qe.Children.only(l), s))
    );
  }, t;
}(qe.Component);
Xt.contextType = sl;
Xt.propTypes = {};
function Kn() {
}
Xt.defaultProps = {
  in: !1,
  mountOnEnter: !1,
  unmountOnExit: !1,
  appear: !1,
  enter: !0,
  exit: !0,
  onEnter: Kn,
  onEntering: Kn,
  onEntered: Kn,
  onExit: Kn,
  onExiting: Kn,
  onExited: Kn
};
Xt.UNMOUNTED = to;
Xt.EXITED = En;
Xt.ENTERING = _n;
Xt.ENTERED = Qn;
Xt.EXITING = Xa;
const Ww = Xt;
function Vw(e) {
  if (e === void 0)
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function yc(e, t) {
  var n = function(i) {
    return t && w.isValidElement(i) ? t(i) : i;
  }, r = /* @__PURE__ */ Object.create(null);
  return e && w.Children.map(e, function(o) {
    return o;
  }).forEach(function(o) {
    r[o.key] = n(o);
  }), r;
}
function Hw(e, t) {
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
function Rn(e, t, n) {
  return n[t] != null ? n[t] : e.props[t];
}
function Gw(e, t) {
  return yc(e.children, function(n) {
    return w.cloneElement(n, {
      onExited: t.bind(null, n),
      in: !0,
      appear: Rn(n, "appear", e),
      enter: Rn(n, "enter", e),
      exit: Rn(n, "exit", e)
    });
  });
}
function Kw(e, t, n) {
  var r = yc(e.children), o = Hw(t, r);
  return Object.keys(o).forEach(function(i) {
    var l = o[i];
    if (w.isValidElement(l)) {
      var s = i in t, a = i in r, u = t[i], c = w.isValidElement(u) && !u.props.in;
      a && (!s || c) ? o[i] = w.cloneElement(l, {
        onExited: n.bind(null, l),
        in: !0,
        exit: Rn(l, "exit", e),
        enter: Rn(l, "enter", e)
      }) : !a && s && !c ? o[i] = w.cloneElement(l, {
        in: !1
      }) : a && s && w.isValidElement(u) && (o[i] = w.cloneElement(l, {
        onExited: n.bind(null, l),
        in: u.props.in,
        exit: Rn(l, "exit", e),
        enter: Rn(l, "enter", e)
      }));
    }
  }), o;
}
var Qw = Object.values || function(e) {
  return Object.keys(e).map(function(t) {
    return e[t];
  });
}, Yw = {
  component: "div",
  childFactory: function(t) {
    return t;
  }
}, vc = /* @__PURE__ */ function(e) {
  Kh(t, e);
  function t(r, o) {
    var i;
    i = e.call(this, r, o) || this;
    var l = i.handleExited.bind(Vw(i));
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
      children: a ? Gw(o, s) : Kw(o, l, s),
      firstRender: !1
    };
  }, n.handleExited = function(o, i) {
    var l = yc(this.props.children);
    o.key in l || (o.props.onExited && o.props.onExited(i), this.mounted && this.setState(function(s) {
      var a = S({}, s.children);
      return delete a[o.key], {
        children: a
      };
    }));
  }, n.render = function() {
    var o = this.props, i = o.component, l = o.childFactory, s = B(o, ["component", "childFactory"]), a = this.state.contextValue, u = Qw(this.state.children).map(l);
    return delete s.appear, delete s.enter, delete s.exit, i === null ? /* @__PURE__ */ qe.createElement(sl.Provider, {
      value: a
    }, u) : /* @__PURE__ */ qe.createElement(sl.Provider, {
      value: a
    }, /* @__PURE__ */ qe.createElement(i, s, u));
  }, t;
}(qe.Component);
vc.propTypes = {};
vc.defaultProps = Yw;
const Xw = vc;
function Zw(e) {
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
  } = e, [c, f] = w.useState(!1), m = V(t, n.ripple, n.rippleVisible, r && n.ripplePulsate), v = {
    width: l,
    height: l,
    top: -(l / 2) + i,
    left: -(l / 2) + o
  }, y = V(n.child, c && n.childLeaving, r && n.childPulsate);
  return !s && !c && f(!0), w.useEffect(() => {
    if (!s && a != null) {
      const g = setTimeout(a, u);
      return () => {
        clearTimeout(g);
      };
    }
  }, [a, s, u]), /* @__PURE__ */ C.jsx("span", {
    className: m,
    style: v,
    children: /* @__PURE__ */ C.jsx("span", {
      className: y
    })
  });
}
const qw = Ce("MuiTouchRipple", ["root", "ripple", "rippleVisible", "ripplePulsate", "child", "childLeaving", "childPulsate"]), at = qw, Jw = ["center", "classes", "className"];
let ss = (e) => e, wf, Cf, kf, Ef;
const Za = 550, e2 = 80, t2 = Lr(wf || (wf = ss`
  0% {
    transform: scale(0);
    opacity: 0.1;
  }

  100% {
    transform: scale(1);
    opacity: 0.3;
  }
`)), n2 = Lr(Cf || (Cf = ss`
  0% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
`)), r2 = Lr(kf || (kf = ss`
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(0.92);
  }

  100% {
    transform: scale(1);
  }
`)), o2 = Y("span", {
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
}), i2 = Y(Zw, {
  name: "MuiTouchRipple",
  slot: "Ripple"
})(Ef || (Ef = ss`
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
`), at.rippleVisible, t2, Za, ({
  theme: e
}) => e.transitions.easing.easeInOut, at.ripplePulsate, ({
  theme: e
}) => e.transitions.duration.shorter, at.child, at.childLeaving, n2, Za, ({
  theme: e
}) => e.transitions.easing.easeInOut, at.childPulsate, r2, ({
  theme: e
}) => e.transitions.easing.easeInOut), l2 = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
    props: t,
    name: "MuiTouchRipple"
  }), {
    center: o = !1,
    classes: i = {},
    className: l
  } = r, s = B(r, Jw), [a, u] = w.useState([]), c = w.useRef(0), f = w.useRef(null);
  w.useEffect(() => {
    f.current && (f.current(), f.current = null);
  }, [a]);
  const m = w.useRef(!1), v = Mh(), y = w.useRef(null), g = w.useRef(null), $ = w.useCallback((x) => {
    const {
      pulsate: _,
      rippleX: E,
      rippleY: k,
      rippleSize: R,
      cb: z
    } = x;
    u((O) => [...O, /* @__PURE__ */ C.jsx(i2, {
      classes: {
        ripple: V(i.ripple, at.ripple),
        rippleVisible: V(i.rippleVisible, at.rippleVisible),
        ripplePulsate: V(i.ripplePulsate, at.ripplePulsate),
        child: V(i.child, at.child),
        childLeaving: V(i.childLeaving, at.childLeaving),
        childPulsate: V(i.childPulsate, at.childPulsate)
      },
      timeout: Za,
      pulsate: _,
      rippleX: E,
      rippleY: k,
      rippleSize: R
    }, c.current)]), c.current += 1, f.current = z;
  }, [i]), p = w.useCallback((x = {}, _ = {}, E = () => {
  }) => {
    const {
      pulsate: k = !1,
      center: R = o || _.pulsate,
      fakeElement: z = !1
      // For test purposes
    } = _;
    if ((x == null ? void 0 : x.type) === "mousedown" && m.current) {
      m.current = !1;
      return;
    }
    (x == null ? void 0 : x.type) === "touchstart" && (m.current = !0);
    const O = z ? null : g.current, D = O ? O.getBoundingClientRect() : {
      width: 0,
      height: 0,
      left: 0,
      top: 0
    };
    let F, j, X;
    if (R || x === void 0 || x.clientX === 0 && x.clientY === 0 || !x.clientX && !x.touches)
      F = Math.round(D.width / 2), j = Math.round(D.height / 2);
    else {
      const {
        clientX: te,
        clientY: ge
      } = x.touches && x.touches.length > 0 ? x.touches[0] : x;
      F = Math.round(te - D.left), j = Math.round(ge - D.top);
    }
    if (R)
      X = Math.sqrt((2 * D.width ** 2 + D.height ** 2) / 3), X % 2 === 0 && (X += 1);
    else {
      const te = Math.max(Math.abs((O ? O.clientWidth : 0) - F), F) * 2 + 2, ge = Math.max(Math.abs((O ? O.clientHeight : 0) - j), j) * 2 + 2;
      X = Math.sqrt(te ** 2 + ge ** 2);
    }
    x != null && x.touches ? y.current === null && (y.current = () => {
      $({
        pulsate: k,
        rippleX: F,
        rippleY: j,
        rippleSize: X,
        cb: E
      });
    }, v.start(e2, () => {
      y.current && (y.current(), y.current = null);
    })) : $({
      pulsate: k,
      rippleX: F,
      rippleY: j,
      rippleSize: X,
      cb: E
    });
  }, [o, $, v]), d = w.useCallback(() => {
    p({}, {
      pulsate: !0
    });
  }, [p]), h = w.useCallback((x, _) => {
    if (v.clear(), (x == null ? void 0 : x.type) === "touchend" && y.current) {
      y.current(), y.current = null, v.start(0, () => {
        h(x, _);
      });
      return;
    }
    y.current = null, u((E) => E.length > 0 ? E.slice(1) : E), f.current = _;
  }, [v]);
  return w.useImperativeHandle(n, () => ({
    pulsate: d,
    start: p,
    stop: h
  }), [d, p, h]), /* @__PURE__ */ C.jsx(o2, S({
    className: V(at.root, i.root, l),
    ref: g
  }, s, {
    children: /* @__PURE__ */ C.jsx(Xw, {
      component: null,
      exit: !0,
      children: a
    })
  }));
}), s2 = l2;
function a2(e) {
  return Pe("MuiButtonBase", e);
}
const u2 = Ce("MuiButtonBase", ["root", "disabled", "focusVisible"]), c2 = u2, d2 = ["action", "centerRipple", "children", "className", "component", "disabled", "disableRipple", "disableTouchRipple", "focusRipple", "focusVisibleClassName", "LinkComponent", "onBlur", "onClick", "onContextMenu", "onDragLeave", "onFocus", "onFocusVisible", "onKeyDown", "onKeyUp", "onMouseDown", "onMouseLeave", "onMouseUp", "onTouchEnd", "onTouchMove", "onTouchStart", "tabIndex", "TouchRippleProps", "touchRippleRef", "type"], f2 = (e) => {
  const {
    disabled: t,
    focusVisible: n,
    focusVisibleClassName: r,
    classes: o
  } = e, l = Ie({
    root: ["root", t && "disabled", n && "focusVisible"]
  }, a2, o);
  return n && r && (l.root += ` ${r}`), l;
}, p2 = Y("button", {
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
  [`&.${c2.disabled}`]: {
    pointerEvents: "none",
    // Disable link interactions
    cursor: "default"
  },
  "@media print": {
    colorAdjust: "exact"
  }
}), m2 = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
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
    focusRipple: m = !1,
    LinkComponent: v = "a",
    onBlur: y,
    onClick: g,
    onContextMenu: $,
    onDragLeave: p,
    onFocus: d,
    onFocusVisible: h,
    onKeyDown: x,
    onKeyUp: _,
    onMouseDown: E,
    onMouseLeave: k,
    onMouseUp: R,
    onTouchEnd: z,
    onTouchMove: O,
    onTouchStart: D,
    tabIndex: F = 0,
    TouchRippleProps: j,
    touchRippleRef: X,
    type: te
  } = r, ge = B(r, d2), fe = w.useRef(null), T = w.useRef(null), N = jn(T, X), {
    isFocusVisibleRef: I,
    onFocus: U,
    onBlur: ae,
    ref: Zt
  } = Nh(), [Te, Rt] = w.useState(!1);
  u && Te && Rt(!1), w.useImperativeHandle(o, () => ({
    focusVisible: () => {
      Rt(!0), fe.current.focus();
    }
  }), []);
  const [L, xe] = w.useState(!1);
  w.useEffect(() => {
    xe(!0);
  }, []);
  const wt = L && !c && !u;
  w.useEffect(() => {
    Te && m && !c && L && T.current.pulsate();
  }, [c, m, Te, L]);
  function De(b, kc, g0 = f) {
    return eo((Ec) => (kc && kc(Ec), !g0 && T.current && T.current[b](Ec), !0));
  }
  const Fn = De("start", E), Qo = De("stop", $), o0 = De("stop", p), i0 = De("stop", R), l0 = De("stop", (b) => {
    Te && b.preventDefault(), k && k(b);
  }), s0 = De("start", D), a0 = De("stop", z), u0 = De("stop", O), c0 = De("stop", (b) => {
    ae(b), I.current === !1 && Rt(!1), y && y(b);
  }, !1), d0 = eo((b) => {
    fe.current || (fe.current = b.currentTarget), U(b), I.current === !0 && (Rt(!0), h && h(b)), d && d(b);
  }), as = () => {
    const b = fe.current;
    return a && a !== "button" && !(b.tagName === "A" && b.href);
  }, us = w.useRef(!1), f0 = eo((b) => {
    m && !us.current && Te && T.current && b.key === " " && (us.current = !0, T.current.stop(b, () => {
      T.current.start(b);
    })), b.target === b.currentTarget && as() && b.key === " " && b.preventDefault(), x && x(b), b.target === b.currentTarget && as() && b.key === "Enter" && !u && (b.preventDefault(), g && g(b));
  }), p0 = eo((b) => {
    m && b.key === " " && T.current && Te && !b.defaultPrevented && (us.current = !1, T.current.stop(b, () => {
      T.current.pulsate(b);
    })), _ && _(b), g && b.target === b.currentTarget && as() && b.key === " " && !b.defaultPrevented && g(b);
  });
  let Yo = a;
  Yo === "button" && (ge.href || ge.to) && (Yo = v);
  const Ar = {};
  Yo === "button" ? (Ar.type = te === void 0 ? "button" : te, Ar.disabled = u) : (!ge.href && !ge.to && (Ar.role = "button"), u && (Ar["aria-disabled"] = u));
  const m0 = jn(n, Zt, fe), Cc = S({}, r, {
    centerRipple: i,
    component: a,
    disabled: u,
    disableRipple: c,
    disableTouchRipple: f,
    focusRipple: m,
    tabIndex: F,
    focusVisible: Te
  }), h0 = f2(Cc);
  return /* @__PURE__ */ C.jsxs(p2, S({
    as: Yo,
    className: V(h0.root, s),
    ownerState: Cc,
    onBlur: c0,
    onClick: g,
    onContextMenu: Qo,
    onFocus: d0,
    onKeyDown: f0,
    onKeyUp: p0,
    onMouseDown: Fn,
    onMouseLeave: l0,
    onMouseUp: i0,
    onDragLeave: o0,
    onTouchEnd: a0,
    onTouchMove: u0,
    onTouchStart: s0,
    ref: m0,
    tabIndex: u ? -1 : F,
    type: te
  }, Ar, ge, {
    children: [l, wt ? (
      /* TouchRipple is only needed client-side, x2 boost on the server. */
      /* @__PURE__ */ C.jsx(s2, S({
        ref: N,
        center: i
      }, j))
    ) : null]
  }));
}), xc = m2;
function h2(e) {
  return Pe("MuiIconButton", e);
}
const g2 = Ce("MuiIconButton", ["root", "disabled", "colorInherit", "colorPrimary", "colorSecondary", "colorError", "colorInfo", "colorSuccess", "colorWarning", "edgeStart", "edgeEnd", "sizeSmall", "sizeMedium", "sizeLarge"]), y2 = g2, v2 = ["edge", "children", "className", "color", "disabled", "disableFocusRipple", "size"], x2 = (e) => {
  const {
    classes: t,
    disabled: n,
    color: r,
    edge: o,
    size: i
  } = e, l = {
    root: ["root", n && "disabled", r !== "default" && `color${le(r)}`, o && `edge${le(o)}`, `size${le(i)}`]
  };
  return Ie(l, h2, t);
}, S2 = Y(xc, {
  name: "MuiIconButton",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.color !== "default" && t[`color${le(n.color)}`], n.edge && t[`edge${le(n.edge)}`], t[`size${le(n.size)}`]];
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
    backgroundColor: e.vars ? `rgba(${e.vars.palette.action.activeChannel} / ${e.vars.palette.action.hoverOpacity})` : et(e.palette.action.active, e.palette.action.hoverOpacity),
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
      backgroundColor: e.vars ? `rgba(${r.mainChannel} / ${e.vars.palette.action.hoverOpacity})` : et(r.main, e.palette.action.hoverOpacity)
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
    [`&.${y2.disabled}`]: {
      backgroundColor: "transparent",
      color: (e.vars || e).palette.action.disabled
    }
  });
}), w2 = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
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
  } = r, f = B(r, v2), m = S({}, r, {
    edge: o,
    color: s,
    disabled: a,
    disableFocusRipple: u,
    size: c
  }), v = x2(m);
  return /* @__PURE__ */ C.jsx(S2, S({
    className: V(v.root, l),
    centerRipple: !0,
    focusRipple: !u,
    disabled: a,
    ref: n
  }, f, {
    ownerState: m,
    children: i
  }));
}), C2 = w2;
function k2(e) {
  return Pe("MuiSvgIcon", e);
}
Ce("MuiSvgIcon", ["root", "colorPrimary", "colorSecondary", "colorAction", "colorError", "colorDisabled", "fontSizeInherit", "fontSizeSmall", "fontSizeMedium", "fontSizeLarge"]);
const E2 = ["children", "className", "color", "component", "fontSize", "htmlColor", "inheritViewBox", "titleAccess", "viewBox"], _2 = (e) => {
  const {
    color: t,
    fontSize: n,
    classes: r
  } = e, o = {
    root: ["root", t !== "inherit" && `color${le(t)}`, `fontSize${le(n)}`]
  };
  return Ie(o, k2, r);
}, $2 = Y("svg", {
  name: "MuiSvgIcon",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.color !== "inherit" && t[`color${le(n.color)}`], t[`fontSize${le(n.fontSize)}`]];
  }
})(({
  theme: e,
  ownerState: t
}) => {
  var n, r, o, i, l, s, a, u, c, f, m, v, y;
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
    color: (f = (m = (e.vars || e).palette) == null || (m = m[t.color]) == null ? void 0 : m.main) != null ? f : {
      action: (v = (e.vars || e).palette) == null || (v = v.action) == null ? void 0 : v.active,
      disabled: (y = (e.vars || e).palette) == null || (y = y.action) == null ? void 0 : y.disabled,
      inherit: void 0
    }[t.color]
  };
}), Qh = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
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
    viewBox: m = "0 0 24 24"
  } = r, v = B(r, E2), y = /* @__PURE__ */ w.isValidElement(o) && o.type === "svg", g = S({}, r, {
    color: l,
    component: s,
    fontSize: a,
    instanceFontSize: t.fontSize,
    inheritViewBox: c,
    viewBox: m,
    hasSvgAsChild: y
  }), $ = {};
  c || ($.viewBox = m);
  const p = _2(g);
  return /* @__PURE__ */ C.jsxs($2, S({
    as: s,
    className: V(p.root, i),
    focusable: "false",
    color: u,
    "aria-hidden": f ? void 0 : !0,
    role: f ? "img" : void 0,
    ref: n
  }, $, v, y && o.props, {
    ownerState: g,
    children: [y ? o.props.children : o, f ? /* @__PURE__ */ C.jsx("title", {
      children: f
    }) : null]
  }));
});
Qh.muiName = "SvgIcon";
const _f = Qh;
function jr(e, t) {
  function n(r, o) {
    return /* @__PURE__ */ C.jsx(_f, S({
      "data-testid": `${t}Icon`,
      ref: o
    }, r, {
      children: e
    }));
  }
  return n.muiName = _f.muiName, /* @__PURE__ */ w.memo(/* @__PURE__ */ w.forwardRef(n));
}
const P2 = jr(/* @__PURE__ */ C.jsx("path", {
  d: "M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2, 4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0, 0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"
}), "SuccessOutlined"), T2 = jr(/* @__PURE__ */ C.jsx("path", {
  d: "M12 5.99L19.53 19H4.47L12 5.99M12 2L1 21h22L12 2zm1 14h-2v2h2v-2zm0-6h-2v4h2v-4z"
}), "ReportProblemOutlined"), R2 = jr(/* @__PURE__ */ C.jsx("path", {
  d: "M11 15h2v2h-2zm0-8h2v6h-2zm.99-5C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"
}), "ErrorOutline"), O2 = jr(/* @__PURE__ */ C.jsx("path", {
  d: "M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"
}), "InfoOutlined"), M2 = jr(/* @__PURE__ */ C.jsx("path", {
  d: "M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
}), "Close"), N2 = ["action", "children", "className", "closeText", "color", "components", "componentsProps", "icon", "iconMapping", "onClose", "role", "severity", "slotProps", "slots", "variant"], I2 = (e) => {
  const {
    variant: t,
    color: n,
    severity: r,
    classes: o
  } = e, i = {
    root: ["root", `color${le(n || r)}`, `${t}${le(n || r)}`, `${t}`],
    icon: ["icon"],
    message: ["message"],
    action: ["action"]
  };
  return Ie(i, Fw, o);
}, L2 = Y(Pr, {
  name: "MuiAlert",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[n.variant], t[`${n.variant}${le(n.color || n.severity)}`]];
  }
})(({
  theme: e
}) => {
  const t = e.palette.mode === "light" ? Ga : Ka, n = e.palette.mode === "light" ? Ka : Ga;
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
        [`& .${xf.icon}`]: e.vars ? {
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
        [`& .${xf.icon}`]: e.vars ? {
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
}), z2 = Y("div", {
  name: "MuiAlert",
  slot: "Icon",
  overridesResolver: (e, t) => t.icon
})({
  marginRight: 12,
  padding: "7px 0",
  display: "flex",
  fontSize: 22,
  opacity: 0.9
}), b2 = Y("div", {
  name: "MuiAlert",
  slot: "Message",
  overridesResolver: (e, t) => t.message
})({
  padding: "8px 0",
  minWidth: 0,
  overflow: "auto"
}), $f = Y("div", {
  name: "MuiAlert",
  slot: "Action",
  overridesResolver: (e, t) => t.action
})({
  display: "flex",
  alignItems: "flex-start",
  padding: "4px 0 0 16px",
  marginLeft: "auto",
  marginRight: -8
}), Pf = {
  success: /* @__PURE__ */ C.jsx(P2, {
    fontSize: "inherit"
  }),
  warning: /* @__PURE__ */ C.jsx(T2, {
    fontSize: "inherit"
  }),
  error: /* @__PURE__ */ C.jsx(R2, {
    fontSize: "inherit"
  }),
  info: /* @__PURE__ */ C.jsx(O2, {
    fontSize: "inherit"
  })
}, j2 = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
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
    iconMapping: m = Pf,
    onClose: v,
    role: y = "alert",
    severity: g = "success",
    slotProps: $ = {},
    slots: p = {},
    variant: d = "standard"
  } = r, h = B(r, N2), x = S({}, r, {
    color: a,
    severity: g,
    variant: d,
    colorSeverity: a || g
  }), _ = I2(x), E = {
    slots: S({
      closeButton: u.CloseButton,
      closeIcon: u.CloseIcon
    }, p),
    slotProps: S({}, c, $)
  }, [k, R] = vf("closeButton", {
    elementType: C2,
    externalForwardedProps: E,
    ownerState: x
  }), [z, O] = vf("closeIcon", {
    elementType: M2,
    externalForwardedProps: E,
    ownerState: x
  });
  return /* @__PURE__ */ C.jsxs(L2, S({
    role: y,
    elevation: 0,
    ownerState: x,
    className: V(_.root, l),
    ref: n
  }, h, {
    children: [f !== !1 ? /* @__PURE__ */ C.jsx(z2, {
      ownerState: x,
      className: _.icon,
      children: f || m[g] || Pf[g]
    }) : null, /* @__PURE__ */ C.jsx(b2, {
      ownerState: x,
      className: _.message,
      children: i
    }), o != null ? /* @__PURE__ */ C.jsx($f, {
      ownerState: x,
      className: _.action,
      children: o
    }) : null, o == null && v ? /* @__PURE__ */ C.jsx($f, {
      ownerState: x,
      className: _.action,
      children: /* @__PURE__ */ C.jsx(k, S({
        size: "small",
        "aria-label": s,
        title: s,
        color: "inherit",
        onClick: v
      }, R, {
        children: /* @__PURE__ */ C.jsx(z, S({
          fontSize: "small"
        }, O))
      }))
    }) : null]
  }));
}), A2 = j2, D2 = Ce("MuiBox", ["root"]), F2 = D2, B2 = hc(), U2 = lx({
  themeId: _r,
  defaultTheme: B2,
  defaultClassName: F2.root,
  generateClassName: uc.generate
}), Tr = U2, W2 = /* @__PURE__ */ w.createContext(), Tf = W2;
function V2(e) {
  return Pe("MuiGrid", e);
}
const H2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], G2 = ["column-reverse", "column", "row-reverse", "row"], K2 = ["nowrap", "wrap-reverse", "wrap"], Yr = ["auto", !0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], zo = Ce("MuiGrid", [
  "root",
  "container",
  "item",
  "zeroMinWidth",
  // spacings
  ...H2.map((e) => `spacing-xs-${e}`),
  // direction values
  ...G2.map((e) => `direction-xs-${e}`),
  // wrap values
  ...K2.map((e) => `wrap-xs-${e}`),
  // grid sizes for all breakpoints
  ...Yr.map((e) => `grid-xs-${e}`),
  ...Yr.map((e) => `grid-sm-${e}`),
  ...Yr.map((e) => `grid-md-${e}`),
  ...Yr.map((e) => `grid-lg-${e}`),
  ...Yr.map((e) => `grid-xl-${e}`)
]), Q2 = ["className", "columns", "columnSpacing", "component", "container", "direction", "item", "rowSpacing", "spacing", "wrap", "zeroMinWidth"];
function yr(e) {
  const t = parseFloat(e);
  return `${t}${String(e).replace(String(t), "") || "px"}`;
}
function Y2({
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
      const l = Al({
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
          const f = `calc(${a} + ${yr(c)})`;
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
function X2({
  theme: e,
  ownerState: t
}) {
  const n = Al({
    values: t.direction,
    breakpoints: e.breakpoints.values
  });
  return yt({
    theme: e
  }, n, (r) => {
    const o = {
      flexDirection: r
    };
    return r.indexOf("column") === 0 && (o[`& > .${zo.item}`] = {
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
function Z2({
  theme: e,
  ownerState: t
}) {
  const {
    container: n,
    rowSpacing: r
  } = t;
  let o = {};
  if (n && r !== 0) {
    const i = Al({
      values: r,
      breakpoints: e.breakpoints.values
    });
    let l;
    typeof i == "object" && (l = Yh({
      breakpoints: e.breakpoints.values,
      values: i
    })), o = yt({
      theme: e
    }, i, (s, a) => {
      var u;
      const c = e.spacing(s);
      return c !== "0px" ? {
        marginTop: `-${yr(c)}`,
        [`& > .${zo.item}`]: {
          paddingTop: yr(c)
        }
      } : (u = l) != null && u.includes(a) ? {} : {
        marginTop: 0,
        [`& > .${zo.item}`]: {
          paddingTop: 0
        }
      };
    });
  }
  return o;
}
function q2({
  theme: e,
  ownerState: t
}) {
  const {
    container: n,
    columnSpacing: r
  } = t;
  let o = {};
  if (n && r !== 0) {
    const i = Al({
      values: r,
      breakpoints: e.breakpoints.values
    });
    let l;
    typeof i == "object" && (l = Yh({
      breakpoints: e.breakpoints.values,
      values: i
    })), o = yt({
      theme: e
    }, i, (s, a) => {
      var u;
      const c = e.spacing(s);
      return c !== "0px" ? {
        width: `calc(100% + ${yr(c)})`,
        marginLeft: `-${yr(c)}`,
        [`& > .${zo.item}`]: {
          paddingLeft: yr(c)
        }
      } : (u = l) != null && u.includes(a) ? {} : {
        width: "100%",
        marginLeft: 0,
        [`& > .${zo.item}`]: {
          paddingLeft: 0
        }
      };
    });
  }
  return o;
}
function J2(e, t, n = {}) {
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
const eC = Y("div", {
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
    r && (c = J2(l, u, t));
    const f = [];
    return u.forEach((m) => {
      const v = n[m];
      v && f.push(t[`grid-${m}-${String(v)}`]);
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
}), X2, Z2, q2, Y2);
function tC(e, t) {
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
const nC = (e) => {
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
  n && (u = tC(i, a));
  const c = [];
  a.forEach((m) => {
    const v = e[m];
    v && c.push(`grid-${m}-${String(v)}`);
  });
  const f = {
    root: ["root", n && "container", o && "item", s && "zeroMinWidth", ...u, r !== "row" && `direction-xs-${String(r)}`, l !== "wrap" && `wrap-xs-${String(l)}`, ...c]
  };
  return Ie(f, V2, t);
}, rC = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
    props: t,
    name: "MuiGrid"
  }), {
    breakpoints: o
  } = Vh(), i = Gl(r), {
    className: l,
    columns: s,
    columnSpacing: a,
    component: u = "div",
    container: c = !1,
    direction: f = "row",
    item: m = !1,
    rowSpacing: v,
    spacing: y = 0,
    wrap: g = "wrap",
    zeroMinWidth: $ = !1
  } = i, p = B(i, Q2), d = v || y, h = a || y, x = w.useContext(Tf), _ = c ? s || 12 : x, E = {}, k = S({}, p);
  o.keys.forEach((O) => {
    p[O] != null && (E[O] = p[O], delete k[O]);
  });
  const R = S({}, i, {
    columns: _,
    container: c,
    direction: f,
    item: m,
    rowSpacing: d,
    columnSpacing: h,
    wrap: g,
    zeroMinWidth: $,
    spacing: y
  }, E, {
    breakpoints: o.keys
  }), z = nC(R);
  return /* @__PURE__ */ C.jsx(Tf.Provider, {
    value: _,
    children: /* @__PURE__ */ C.jsx(eC, S({
      ownerState: R,
      className: V(z.root, l),
      as: u,
      ref: n
    }, k))
  });
}), Ws = rC;
function oC(e) {
  return Pe("MuiTypography", e);
}
Ce("MuiTypography", ["root", "h1", "h2", "h3", "h4", "h5", "h6", "subtitle1", "subtitle2", "body1", "body2", "inherit", "button", "caption", "overline", "alignLeft", "alignRight", "alignCenter", "alignJustify", "noWrap", "gutterBottom", "paragraph"]);
const iC = ["align", "className", "component", "gutterBottom", "noWrap", "paragraph", "variant", "variantMapping"], lC = (e) => {
  const {
    align: t,
    gutterBottom: n,
    noWrap: r,
    paragraph: o,
    variant: i,
    classes: l
  } = e, s = {
    root: ["root", i, e.align !== "inherit" && `align${le(t)}`, n && "gutterBottom", r && "noWrap", o && "paragraph"]
  };
  return Ie(s, oC, l);
}, sC = Y("span", {
  name: "MuiTypography",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.variant && t[n.variant], n.align !== "inherit" && t[`align${le(n.align)}`], n.noWrap && t.noWrap, n.gutterBottom && t.gutterBottom, n.paragraph && t.paragraph];
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
})), Rf = {
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
}, aC = {
  primary: "primary.main",
  textPrimary: "text.primary",
  secondary: "secondary.main",
  textSecondary: "text.secondary",
  error: "error.main"
}, uC = (e) => aC[e] || e, cC = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
    props: t,
    name: "MuiTypography"
  }), o = uC(r.color), i = Gl(S({}, r, {
    color: o
  })), {
    align: l = "inherit",
    className: s,
    component: a,
    gutterBottom: u = !1,
    noWrap: c = !1,
    paragraph: f = !1,
    variant: m = "body1",
    variantMapping: v = Rf
  } = i, y = B(i, iC), g = S({}, i, {
    align: l,
    color: o,
    className: s,
    component: a,
    gutterBottom: u,
    noWrap: c,
    paragraph: f,
    variant: m,
    variantMapping: v
  }), $ = a || (f ? "p" : v[m] || Rf[m]) || "span", p = lC(g);
  return /* @__PURE__ */ C.jsx(sC, S({
    as: $,
    ref: n,
    ownerState: g,
    className: V(p.root, s)
  }, y));
}), pt = cC, dC = () => /* @__PURE__ */ C.jsx(
  Pr,
  {
    elevation: 2,
    sx: {
      p: 2,
      mb: 3,
      textAlign: "center"
    },
    children: /* @__PURE__ */ C.jsx(pt, { variant: "h4", component: "h1", children: "Meraki Integration Control" })
  }
), fC = /* @__PURE__ */ w.createContext({}), gn = fC;
function pC(e) {
  return Pe("MuiList", e);
}
Ce("MuiList", ["root", "padding", "dense", "subheader"]);
const mC = ["children", "className", "component", "dense", "disablePadding", "subheader"], hC = (e) => {
  const {
    classes: t,
    disablePadding: n,
    dense: r,
    subheader: o
  } = e;
  return Ie({
    root: ["root", !n && "padding", r && "dense", o && "subheader"]
  }, pC, t);
}, gC = Y("ul", {
  name: "MuiList",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, !n.disablePadding && t.padding, n.dense && t.dense, n.subheader && t.subheader];
  }
})(({
  ownerState: e
}) => S({
  listStyle: "none",
  margin: 0,
  padding: 0,
  position: "relative"
}, !e.disablePadding && {
  paddingTop: 8,
  paddingBottom: 8
}, e.subheader && {
  paddingTop: 0
})), yC = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
    props: t,
    name: "MuiList"
  }), {
    children: o,
    className: i,
    component: l = "ul",
    dense: s = !1,
    disablePadding: a = !1,
    subheader: u
  } = r, c = B(r, mC), f = w.useMemo(() => ({
    dense: s
  }), [s]), m = S({}, r, {
    component: l,
    dense: s,
    disablePadding: a
  }), v = hC(m);
  return /* @__PURE__ */ C.jsx(gn.Provider, {
    value: f,
    children: /* @__PURE__ */ C.jsxs(gC, S({
      as: l,
      className: V(v.root, i),
      ref: n,
      ownerState: m
    }, c, {
      children: [u, o]
    }))
  });
}), Xh = yC;
function vC(e) {
  return Pe("MuiListItemButton", e);
}
const xC = Ce("MuiListItemButton", ["root", "focusVisible", "dense", "alignItemsFlexStart", "disabled", "divider", "gutters", "selected"]), Yn = xC, SC = ["alignItems", "autoFocus", "component", "children", "dense", "disableGutters", "divider", "focusVisibleClassName", "selected", "className"], wC = (e, t) => {
  const {
    ownerState: n
  } = e;
  return [t.root, n.dense && t.dense, n.alignItems === "flex-start" && t.alignItemsFlexStart, n.divider && t.divider, !n.disableGutters && t.gutters];
}, CC = (e) => {
  const {
    alignItems: t,
    classes: n,
    dense: r,
    disabled: o,
    disableGutters: i,
    divider: l,
    selected: s
  } = e, u = Ie({
    root: ["root", r && "dense", !i && "gutters", l && "divider", o && "disabled", t === "flex-start" && "alignItemsFlexStart", s && "selected"]
  }, vC, n);
  return S({}, n, u);
}, kC = Y(xc, {
  shouldForwardProp: (e) => Gh(e) || e === "classes",
  name: "MuiListItemButton",
  slot: "Root",
  overridesResolver: wC
})(({
  theme: e,
  ownerState: t
}) => S({
  display: "flex",
  flexGrow: 1,
  justifyContent: "flex-start",
  alignItems: "center",
  position: "relative",
  textDecoration: "none",
  minWidth: 0,
  boxSizing: "border-box",
  textAlign: "left",
  paddingTop: 8,
  paddingBottom: 8,
  transition: e.transitions.create("background-color", {
    duration: e.transitions.duration.shortest
  }),
  "&:hover": {
    textDecoration: "none",
    backgroundColor: (e.vars || e).palette.action.hover,
    // Reset on touch devices, it doesn't add specificity
    "@media (hover: none)": {
      backgroundColor: "transparent"
    }
  },
  [`&.${Yn.selected}`]: {
    backgroundColor: e.vars ? `rgba(${e.vars.palette.primary.mainChannel} / ${e.vars.palette.action.selectedOpacity})` : et(e.palette.primary.main, e.palette.action.selectedOpacity),
    [`&.${Yn.focusVisible}`]: {
      backgroundColor: e.vars ? `rgba(${e.vars.palette.primary.mainChannel} / calc(${e.vars.palette.action.selectedOpacity} + ${e.vars.palette.action.focusOpacity}))` : et(e.palette.primary.main, e.palette.action.selectedOpacity + e.palette.action.focusOpacity)
    }
  },
  [`&.${Yn.selected}:hover`]: {
    backgroundColor: e.vars ? `rgba(${e.vars.palette.primary.mainChannel} / calc(${e.vars.palette.action.selectedOpacity} + ${e.vars.palette.action.hoverOpacity}))` : et(e.palette.primary.main, e.palette.action.selectedOpacity + e.palette.action.hoverOpacity),
    // Reset on touch devices, it doesn't add specificity
    "@media (hover: none)": {
      backgroundColor: e.vars ? `rgba(${e.vars.palette.primary.mainChannel} / ${e.vars.palette.action.selectedOpacity})` : et(e.palette.primary.main, e.palette.action.selectedOpacity)
    }
  },
  [`&.${Yn.focusVisible}`]: {
    backgroundColor: (e.vars || e).palette.action.focus
  },
  [`&.${Yn.disabled}`]: {
    opacity: (e.vars || e).palette.action.disabledOpacity
  }
}, t.divider && {
  borderBottom: `1px solid ${(e.vars || e).palette.divider}`,
  backgroundClip: "padding-box"
}, t.alignItems === "flex-start" && {
  alignItems: "flex-start"
}, !t.disableGutters && {
  paddingLeft: 16,
  paddingRight: 16
}, t.dense && {
  paddingTop: 4,
  paddingBottom: 4
})), EC = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
    props: t,
    name: "MuiListItemButton"
  }), {
    alignItems: o = "center",
    autoFocus: i = !1,
    component: l = "div",
    children: s,
    dense: a = !1,
    disableGutters: u = !1,
    divider: c = !1,
    focusVisibleClassName: f,
    selected: m = !1,
    className: v
  } = r, y = B(r, SC), g = w.useContext(gn), $ = w.useMemo(() => ({
    dense: a || g.dense || !1,
    alignItems: o,
    disableGutters: u
  }), [o, g.dense, a, u]), p = w.useRef(null);
  Go(() => {
    i && p.current && p.current.focus();
  }, [i]);
  const d = S({}, r, {
    alignItems: o,
    dense: $.dense,
    disableGutters: u,
    divider: c,
    selected: m
  }), h = CC(d), x = jn(p, n);
  return /* @__PURE__ */ C.jsx(gn.Provider, {
    value: $,
    children: /* @__PURE__ */ C.jsx(kC, S({
      ref: x,
      href: y.href || y.to,
      component: (y.href || y.to) && l === "div" ? "button" : l,
      focusVisibleClassName: V(h.focusVisible, f),
      ownerState: d,
      className: V(h.root, v)
    }, y, {
      classes: h,
      children: s
    }))
  });
}), _C = EC;
function $C(e) {
  return Pe("MuiListItemText", e);
}
const PC = Ce("MuiListItemText", ["root", "multiline", "dense", "inset", "primary", "secondary"]), Of = PC, TC = ["children", "className", "disableTypography", "inset", "primary", "primaryTypographyProps", "secondary", "secondaryTypographyProps"], RC = (e) => {
  const {
    classes: t,
    inset: n,
    primary: r,
    secondary: o,
    dense: i
  } = e;
  return Ie({
    root: ["root", n && "inset", i && "dense", r && o && "multiline"],
    primary: ["primary"],
    secondary: ["secondary"]
  }, $C, t);
}, OC = Y("div", {
  name: "MuiListItemText",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [{
      [`& .${Of.primary}`]: t.primary
    }, {
      [`& .${Of.secondary}`]: t.secondary
    }, t.root, n.inset && t.inset, n.primary && n.secondary && t.multiline, n.dense && t.dense];
  }
})(({
  ownerState: e
}) => S({
  flex: "1 1 auto",
  minWidth: 0,
  marginTop: 4,
  marginBottom: 4
}, e.primary && e.secondary && {
  marginTop: 6,
  marginBottom: 6
}, e.inset && {
  paddingLeft: 56
})), MC = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
    props: t,
    name: "MuiListItemText"
  }), {
    children: o,
    className: i,
    disableTypography: l = !1,
    inset: s = !1,
    primary: a,
    primaryTypographyProps: u,
    secondary: c,
    secondaryTypographyProps: f
  } = r, m = B(r, TC), {
    dense: v
  } = w.useContext(gn);
  let y = a ?? o, g = c;
  const $ = S({}, r, {
    disableTypography: l,
    inset: s,
    primary: !!y,
    secondary: !!g,
    dense: v
  }), p = RC($);
  return y != null && y.type !== pt && !l && (y = /* @__PURE__ */ C.jsx(pt, S({
    variant: v ? "body2" : "body1",
    className: p.primary,
    component: u != null && u.variant ? void 0 : "span",
    display: "block"
  }, u, {
    children: y
  }))), g != null && g.type !== pt && !l && (g = /* @__PURE__ */ C.jsx(pt, S({
    variant: "body2",
    className: p.secondary,
    color: "text.secondary",
    display: "block"
  }, f, {
    children: g
  }))), /* @__PURE__ */ C.jsxs(OC, S({
    className: V(p.root, i),
    ownerState: $,
    ref: n
  }, m, {
    children: [y, g]
  }));
}), Zh = MC;
function Mf(e, t) {
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
const NC = {
  configure: (e) => {
    uc.configure(e);
  }
}, IC = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  capitalize: le,
  createChainedFunction: gx,
  createSvgIcon: jr,
  debounce: yx,
  deprecatedPropType: vx,
  isMuiElement: Ph,
  ownerDocument: Th,
  ownerWindow: xx,
  requirePropFactory: Sx,
  setRef: Rh,
  unstable_ClassNameGenerator: NC,
  unstable_useEnhancedEffect: Go,
  unstable_useId: Oh,
  unsupportedProp: Cx,
  useControlled: kx,
  useEventCallback: eo,
  useForkRef: jn,
  useIsFocusVisible: Nh
}, Symbol.toStringTag, { value: "Module" }));
function LC(e) {
  return Pe("MuiCollapse", e);
}
Ce("MuiCollapse", ["root", "horizontal", "vertical", "entered", "hidden", "wrapper", "wrapperInner"]);
const zC = ["addEndListener", "children", "className", "collapsedSize", "component", "easing", "in", "onEnter", "onEntered", "onEntering", "onExit", "onExited", "onExiting", "orientation", "style", "timeout", "TransitionComponent"], bC = (e) => {
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
  return Ie(r, LC, n);
}, jC = Y("div", {
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
})), AC = Y("div", {
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
})), DC = Y("div", {
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
})), qh = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
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
    onEntered: m,
    onEntering: v,
    onExit: y,
    onExited: g,
    onExiting: $,
    orientation: p = "vertical",
    style: d,
    timeout: h = Wh.standard,
    // eslint-disable-next-line react/prop-types
    TransitionComponent: x = Ww
  } = r, _ = B(r, zC), E = S({}, r, {
    orientation: p,
    collapsedSize: s
  }), k = bC(E), R = Vh(), z = Mh(), O = w.useRef(null), D = w.useRef(), F = typeof s == "number" ? `${s}px` : s, j = p === "horizontal", X = j ? "width" : "height", te = w.useRef(null), ge = jn(n, te), fe = (L) => (xe) => {
    if (L) {
      const wt = te.current;
      xe === void 0 ? L(wt) : L(wt, xe);
    }
  }, T = () => O.current ? O.current[j ? "clientWidth" : "clientHeight"] : 0, N = fe((L, xe) => {
    O.current && j && (O.current.style.position = "absolute"), L.style[X] = F, f && f(L, xe);
  }), I = fe((L, xe) => {
    const wt = T();
    O.current && j && (O.current.style.position = "");
    const {
      duration: De,
      easing: Fn
    } = Mf({
      style: d,
      timeout: h,
      easing: u
    }, {
      mode: "enter"
    });
    if (h === "auto") {
      const Qo = R.transitions.getAutoHeightDuration(wt);
      L.style.transitionDuration = `${Qo}ms`, D.current = Qo;
    } else
      L.style.transitionDuration = typeof De == "string" ? De : `${De}ms`;
    L.style[X] = `${wt}px`, L.style.transitionTimingFunction = Fn, v && v(L, xe);
  }), U = fe((L, xe) => {
    L.style[X] = "auto", m && m(L, xe);
  }), ae = fe((L) => {
    L.style[X] = `${T()}px`, y && y(L);
  }), Zt = fe(g), Te = fe((L) => {
    const xe = T(), {
      duration: wt,
      easing: De
    } = Mf({
      style: d,
      timeout: h,
      easing: u
    }, {
      mode: "exit"
    });
    if (h === "auto") {
      const Fn = R.transitions.getAutoHeightDuration(xe);
      L.style.transitionDuration = `${Fn}ms`, D.current = Fn;
    } else
      L.style.transitionDuration = typeof wt == "string" ? wt : `${wt}ms`;
    L.style[X] = F, L.style.transitionTimingFunction = De, $ && $(L);
  }), Rt = (L) => {
    h === "auto" && z.start(D.current || 0, L), o && o(te.current, L);
  };
  return /* @__PURE__ */ C.jsx(x, S({
    in: c,
    onEnter: N,
    onEntered: U,
    onEntering: I,
    onExit: ae,
    onExited: Zt,
    onExiting: Te,
    addEndListener: Rt,
    nodeRef: te,
    timeout: h === "auto" ? null : h
  }, _, {
    children: (L, xe) => /* @__PURE__ */ C.jsx(jC, S({
      as: a,
      className: V(k.root, l, {
        entered: k.entered,
        exited: !c && F === "0px" && k.hidden
      }[L]),
      style: S({
        [j ? "minWidth" : "minHeight"]: F
      }, d),
      ref: ge
    }, xe, {
      // `ownerState` is set after `childProps` to override any existing `ownerState` property in `childProps`
      // that might have been forwarded from the Transition component.
      ownerState: S({}, E, {
        state: L
      }),
      children: /* @__PURE__ */ C.jsx(AC, {
        ownerState: S({}, E, {
          state: L
        }),
        className: k.wrapper,
        ref: O,
        children: /* @__PURE__ */ C.jsx(DC, {
          ownerState: S({}, E, {
            state: L
          }),
          className: k.wrapperInner,
          children: i
        })
      })
    }))
  }));
});
qh.muiSupportAuto = !0;
const FC = qh;
var Sc = {}, Vs = {};
const BC = /* @__PURE__ */ Qt(IC);
var Nf;
function Jh() {
  return Nf || (Nf = 1, function(e) {
    "use client";
    Object.defineProperty(e, "__esModule", {
      value: !0
    }), Object.defineProperty(e, "default", {
      enumerable: !0,
      get: function() {
        return t.createSvgIcon;
      }
    });
    var t = BC;
  }(Vs)), Vs;
}
var UC = is;
Object.defineProperty(Sc, "__esModule", {
  value: !0
});
var e0 = Sc.default = void 0, WC = UC(Jh()), VC = C;
e0 = Sc.default = (0, WC.default)(/* @__PURE__ */ (0, VC.jsx)("path", {
  d: "m12 8-6 6 1.41 1.41L12 10.83l4.59 4.58L18 14z"
}), "ExpandLess");
var wc = {}, HC = is;
Object.defineProperty(wc, "__esModule", {
  value: !0
});
var t0 = wc.default = void 0, GC = HC(Jh()), KC = C;
t0 = wc.default = (0, GC.default)(/* @__PURE__ */ (0, KC.jsx)("path", {
  d: "M16.59 8.59 12 13.17 7.41 8.59 6 10l6 6 6-6z"
}), "ExpandMore");
function QC(e) {
  return Pe("MuiListItem", e);
}
const YC = Ce("MuiListItem", ["root", "container", "focusVisible", "dense", "alignItemsFlexStart", "disabled", "divider", "gutters", "padding", "button", "secondaryAction", "selected"]), Xn = YC;
function XC(e) {
  return Pe("MuiListItemSecondaryAction", e);
}
Ce("MuiListItemSecondaryAction", ["root", "disableGutters"]);
const ZC = ["className"], qC = (e) => {
  const {
    disableGutters: t,
    classes: n
  } = e;
  return Ie({
    root: ["root", t && "disableGutters"]
  }, XC, n);
}, JC = Y("div", {
  name: "MuiListItemSecondaryAction",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.disableGutters && t.disableGutters];
  }
})(({
  ownerState: e
}) => S({
  position: "absolute",
  right: 16,
  top: "50%",
  transform: "translateY(-50%)"
}, e.disableGutters && {
  right: 0
})), n0 = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
    props: t,
    name: "MuiListItemSecondaryAction"
  }), {
    className: o
  } = r, i = B(r, ZC), l = w.useContext(gn), s = S({}, r, {
    disableGutters: l.disableGutters
  }), a = qC(s);
  return /* @__PURE__ */ C.jsx(JC, S({
    className: V(a.root, o),
    ownerState: s,
    ref: n
  }, i));
});
n0.muiName = "ListItemSecondaryAction";
const ek = n0, tk = ["className"], nk = ["alignItems", "autoFocus", "button", "children", "className", "component", "components", "componentsProps", "ContainerComponent", "ContainerProps", "dense", "disabled", "disableGutters", "disablePadding", "divider", "focusVisibleClassName", "secondaryAction", "selected", "slotProps", "slots"], rk = (e, t) => {
  const {
    ownerState: n
  } = e;
  return [t.root, n.dense && t.dense, n.alignItems === "flex-start" && t.alignItemsFlexStart, n.divider && t.divider, !n.disableGutters && t.gutters, !n.disablePadding && t.padding, n.button && t.button, n.hasSecondaryAction && t.secondaryAction];
}, ok = (e) => {
  const {
    alignItems: t,
    button: n,
    classes: r,
    dense: o,
    disabled: i,
    disableGutters: l,
    disablePadding: s,
    divider: a,
    hasSecondaryAction: u,
    selected: c
  } = e;
  return Ie({
    root: ["root", o && "dense", !l && "gutters", !s && "padding", a && "divider", i && "disabled", n && "button", t === "flex-start" && "alignItemsFlexStart", u && "secondaryAction", c && "selected"],
    container: ["container"]
  }, QC, r);
}, ik = Y("div", {
  name: "MuiListItem",
  slot: "Root",
  overridesResolver: rk
})(({
  theme: e,
  ownerState: t
}) => S({
  display: "flex",
  justifyContent: "flex-start",
  alignItems: "center",
  position: "relative",
  textDecoration: "none",
  width: "100%",
  boxSizing: "border-box",
  textAlign: "left"
}, !t.disablePadding && S({
  paddingTop: 8,
  paddingBottom: 8
}, t.dense && {
  paddingTop: 4,
  paddingBottom: 4
}, !t.disableGutters && {
  paddingLeft: 16,
  paddingRight: 16
}, !!t.secondaryAction && {
  // Add some space to avoid collision as `ListItemSecondaryAction`
  // is absolutely positioned.
  paddingRight: 48
}), !!t.secondaryAction && {
  [`& > .${Yn.root}`]: {
    paddingRight: 48
  }
}, {
  [`&.${Xn.focusVisible}`]: {
    backgroundColor: (e.vars || e).palette.action.focus
  },
  [`&.${Xn.selected}`]: {
    backgroundColor: e.vars ? `rgba(${e.vars.palette.primary.mainChannel} / ${e.vars.palette.action.selectedOpacity})` : et(e.palette.primary.main, e.palette.action.selectedOpacity),
    [`&.${Xn.focusVisible}`]: {
      backgroundColor: e.vars ? `rgba(${e.vars.palette.primary.mainChannel} / calc(${e.vars.palette.action.selectedOpacity} + ${e.vars.palette.action.focusOpacity}))` : et(e.palette.primary.main, e.palette.action.selectedOpacity + e.palette.action.focusOpacity)
    }
  },
  [`&.${Xn.disabled}`]: {
    opacity: (e.vars || e).palette.action.disabledOpacity
  }
}, t.alignItems === "flex-start" && {
  alignItems: "flex-start"
}, t.divider && {
  borderBottom: `1px solid ${(e.vars || e).palette.divider}`,
  backgroundClip: "padding-box"
}, t.button && {
  transition: e.transitions.create("background-color", {
    duration: e.transitions.duration.shortest
  }),
  "&:hover": {
    textDecoration: "none",
    backgroundColor: (e.vars || e).palette.action.hover,
    // Reset on touch devices, it doesn't add specificity
    "@media (hover: none)": {
      backgroundColor: "transparent"
    }
  },
  [`&.${Xn.selected}:hover`]: {
    backgroundColor: e.vars ? `rgba(${e.vars.palette.primary.mainChannel} / calc(${e.vars.palette.action.selectedOpacity} + ${e.vars.palette.action.hoverOpacity}))` : et(e.palette.primary.main, e.palette.action.selectedOpacity + e.palette.action.hoverOpacity),
    // Reset on touch devices, it doesn't add specificity
    "@media (hover: none)": {
      backgroundColor: e.vars ? `rgba(${e.vars.palette.primary.mainChannel} / ${e.vars.palette.action.selectedOpacity})` : et(e.palette.primary.main, e.palette.action.selectedOpacity)
    }
  }
}, t.hasSecondaryAction && {
  // Add some space to avoid collision as `ListItemSecondaryAction`
  // is absolutely positioned.
  paddingRight: 48
})), lk = Y("li", {
  name: "MuiListItem",
  slot: "Container",
  overridesResolver: (e, t) => t.container
})({
  position: "relative"
}), sk = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
    props: t,
    name: "MuiListItem"
  }), {
    alignItems: o = "center",
    autoFocus: i = !1,
    button: l = !1,
    children: s,
    className: a,
    component: u,
    components: c = {},
    componentsProps: f = {},
    ContainerComponent: m = "li",
    ContainerProps: {
      className: v
    } = {},
    dense: y = !1,
    disabled: g = !1,
    disableGutters: $ = !1,
    disablePadding: p = !1,
    divider: d = !1,
    focusVisibleClassName: h,
    secondaryAction: x,
    selected: _ = !1,
    slotProps: E = {},
    slots: k = {}
  } = r, R = B(r.ContainerProps, tk), z = B(r, nk), O = w.useContext(gn), D = w.useMemo(() => ({
    dense: y || O.dense || !1,
    alignItems: o,
    disableGutters: $
  }), [o, O.dense, y, $]), F = w.useRef(null);
  Go(() => {
    i && F.current && F.current.focus();
  }, [i]);
  const j = w.Children.toArray(s), X = j.length && Ph(j[j.length - 1], ["ListItemSecondaryAction"]), te = S({}, r, {
    alignItems: o,
    autoFocus: i,
    button: l,
    dense: D.dense,
    disabled: g,
    disableGutters: $,
    disablePadding: p,
    divider: d,
    hasSecondaryAction: X,
    selected: _
  }), ge = ok(te), fe = jn(F, n), T = k.root || c.Root || ik, N = E.root || f.root || {}, I = S({
    className: V(ge.root, N.className, a),
    disabled: g
  }, z);
  let U = u || "li";
  return l && (I.component = u || "div", I.focusVisibleClassName = V(Xn.focusVisible, h), U = xc), X ? (U = !I.component && !u ? "div" : U, m === "li" && (U === "li" ? U = "div" : I.component === "li" && (I.component = "div")), /* @__PURE__ */ C.jsx(gn.Provider, {
    value: D,
    children: /* @__PURE__ */ C.jsxs(lk, S({
      as: m,
      className: V(ge.container, v),
      ref: fe,
      ownerState: te
    }, R, {
      children: [/* @__PURE__ */ C.jsx(T, S({}, N, !Ha(T) && {
        as: U,
        ownerState: S({}, te, N.ownerState)
      }, I, {
        children: j
      })), j.pop()]
    }))
  })) : /* @__PURE__ */ C.jsx(gn.Provider, {
    value: D,
    children: /* @__PURE__ */ C.jsxs(T, S({}, N, {
      as: U,
      ref: fe
    }, !Ha(T) && {
      ownerState: S({}, te, N.ownerState)
    }, I, {
      children: [j, x && /* @__PURE__ */ C.jsx(ek, {
        children: x
      })]
    }))
  });
}), ak = sk;
function uk(e) {
  return Pe("MuiDivider", e);
}
Ce("MuiDivider", ["root", "absolute", "fullWidth", "inset", "middle", "flexItem", "light", "vertical", "withChildren", "withChildrenVertical", "textAlignRight", "textAlignLeft", "wrapper", "wrapperVertical"]);
const ck = ["absolute", "children", "className", "component", "flexItem", "light", "orientation", "role", "textAlign", "variant"], dk = (e) => {
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
  return Ie({
    root: ["root", t && "absolute", a, i && "light", l === "vertical" && "vertical", o && "flexItem", n && "withChildren", n && l === "vertical" && "withChildrenVertical", s === "right" && l !== "vertical" && "textAlignRight", s === "left" && l !== "vertical" && "textAlignLeft"],
    wrapper: ["wrapper", l === "vertical" && "wrapperVertical"]
  }, uk, r);
}, fk = Y("div", {
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
  borderColor: e.vars ? `rgba(${e.vars.palette.dividerChannel} / 0.08)` : et(e.palette.divider, 0.08)
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
})), pk = Y("span", {
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
})), r0 = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
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
    textAlign: m = "center",
    variant: v = "fullWidth"
  } = r, y = B(r, ck), g = S({}, r, {
    absolute: o,
    component: s,
    flexItem: a,
    light: u,
    orientation: c,
    role: f,
    textAlign: m,
    variant: v
  }), $ = dk(g);
  return /* @__PURE__ */ C.jsx(fk, S({
    as: s,
    className: V($.root, l),
    role: f,
    ref: n,
    ownerState: g
  }, y, {
    children: i ? /* @__PURE__ */ C.jsx(pk, {
      className: $.wrapper,
      ownerState: g,
      children: i
    }) : null
  }));
});
r0.muiSkipListHighlight = !0;
const mk = r0, hk = ({ devices: e }) => !e || e.length === 0 ? /* @__PURE__ */ C.jsx(pt, { variant: "body2", children: "No devices found in this network." }) : /* @__PURE__ */ C.jsxs(Tr, { sx: { mt: 2 }, children: [
  /* @__PURE__ */ C.jsx(pt, { variant: "h6", gutterBottom: !0, children: "Devices" }),
  /* @__PURE__ */ C.jsx(Pr, { elevation: 1, children: /* @__PURE__ */ C.jsx(Xh, { dense: !0, children: e.map((t, n) => /* @__PURE__ */ C.jsxs(qe.Fragment, { children: [
    /* @__PURE__ */ C.jsx(ak, { children: /* @__PURE__ */ C.jsx(
      Zh,
      {
        primary: t.name || "Unnamed Device",
        secondary: /* @__PURE__ */ C.jsxs(C.Fragment, { children: [
          /* @__PURE__ */ C.jsxs(pt, { component: "span", variant: "body2", color: "text.primary", children: [
            "Model: ",
            t.model,
            " | Status: ",
            t.status
          ] }),
          /* @__PURE__ */ C.jsx("br", {}),
          t.lanIp && `IP: ${t.lanIp} | `,
          t.mac && `MAC: ${t.mac}`
        ] })
      }
    ) }),
    n < e.length - 1 && /* @__PURE__ */ C.jsx(mk, {})
  ] }, t.serial)) }) })
] }), gk = ({ data: e }) => {
  const [t, n] = w.useState(null), r = (l) => {
    n(t === l ? null : l);
  }, { networks: o, devices: i } = e;
  return !o || o.length === 0 ? /* @__PURE__ */ C.jsx(pt, { children: "No networks found." }) : /* @__PURE__ */ C.jsxs(Tr, { children: [
    /* @__PURE__ */ C.jsx(pt, { variant: "h5", gutterBottom: !0, children: "Networks" }),
    /* @__PURE__ */ C.jsx(Xh, { component: "nav", children: o.map((l) => /* @__PURE__ */ C.jsxs(qe.Fragment, { children: [
      /* @__PURE__ */ C.jsxs(_C, { onClick: () => r(l.id), children: [
        /* @__PURE__ */ C.jsx(Zh, { primary: l.name }),
        t === l.id ? /* @__PURE__ */ C.jsx(e0, {}) : /* @__PURE__ */ C.jsx(t0, {})
      ] }),
      /* @__PURE__ */ C.jsx(FC, { in: t === l.id, timeout: "auto", unmountOnExit: !0, children: /* @__PURE__ */ C.jsx(Tr, { sx: { pl: 4, py: 1 }, children: /* @__PURE__ */ C.jsx(hk, { devices: i.filter((s) => s.networkId === l.id) }) }) })
    ] }, l.id)) })
  ] });
};
function yk(e) {
  return Pe("MuiCard", e);
}
Ce("MuiCard", ["root"]);
const vk = ["className", "raised"], xk = (e) => {
  const {
    classes: t
  } = e;
  return Ie({
    root: ["root"]
  }, yk, t);
}, Sk = Y(Pr, {
  name: "MuiCard",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})(() => ({
  overflow: "hidden"
})), wk = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
    props: t,
    name: "MuiCard"
  }), {
    className: o,
    raised: i = !1
  } = r, l = B(r, vk), s = S({}, r, {
    raised: i
  }), a = xk(s);
  return /* @__PURE__ */ C.jsx(Sk, S({
    className: V(a.root, o),
    elevation: i ? 8 : void 0,
    ref: n,
    ownerState: s
  }, l));
}), Ck = wk;
function kk(e) {
  return Pe("MuiCardContent", e);
}
Ce("MuiCardContent", ["root"]);
const Ek = ["className", "component"], _k = (e) => {
  const {
    classes: t
  } = e;
  return Ie({
    root: ["root"]
  }, kk, t);
}, $k = Y("div", {
  name: "MuiCardContent",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})(() => ({
  padding: 16,
  "&:last-child": {
    paddingBottom: 24
  }
})), Pk = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = ke({
    props: t,
    name: "MuiCardContent"
  }), {
    className: o,
    component: i = "div"
  } = r, l = B(r, Ek), s = S({}, r, {
    component: i
  }), a = _k(s);
  return /* @__PURE__ */ C.jsx($k, S({
    as: i,
    className: V(a.root, o),
    ownerState: s,
    ref: n
  }, l));
}), Tk = Pk, Rk = () => /* @__PURE__ */ C.jsxs(Tr, { sx: { mt: 4 }, children: [
  /* @__PURE__ */ C.jsx(pt, { variant: "h5", component: "h2", sx: { mb: 2 }, children: "Event Log" }),
  /* @__PURE__ */ C.jsx(
    Ck,
    {
      sx: {
        borderRadius: 2,
        boxShadow: "none",
        border: "1px solid",
        borderColor: "divider"
      },
      children: /* @__PURE__ */ C.jsx(Tk, { sx: { p: 2.5 }, children: /* @__PURE__ */ C.jsx(pt, { color: "text.secondary", children: "Integration-specific events will be displayed here." }) })
    }
  )
] }), Ok = (e) => {
  const t = {
    "--primary-color": e ? "#4fd1c5" : "#3277a8",
    "--primary-background-color": e ? "#1a202c" : "#f5f5f5",
    "--card-background-color": e ? "#2d3748" : "#ffffff",
    "--primary-text-color": e ? "#edf2f7" : "#212121",
    "--secondary-text-color": e ? "#a0aec0" : "#727272",
    "--divider-color": e ? "rgba(255, 255, 255, 0.12)" : "rgba(0, 0, 0, 0.12)"
  };
  return {
    palette: {
      mode: e ? "dark" : "light",
      primary: {
        main: t["--primary-color"]
      },
      background: {
        default: t["--primary-background-color"],
        paper: t["--card-background-color"]
      },
      text: {
        primary: t["--primary-text-color"],
        secondary: t["--secondary-text-color"]
      },
      divider: t["--divider-color"]
    },
    typography: {
      fontFamily: "Roboto, sans-serif",
      h4: {
        fontWeight: 700,
        color: t["--primary-text-color"]
      },
      h5: {
        fontWeight: 600,
        color: t["--primary-text-color"]
      },
      h6: {
        fontWeight: 600,
        color: t["--secondary-text-color"]
      },
      body1: {
        color: t["--primary-text-color"]
      },
      body2: {
        color: t["--secondary-text-color"]
      }
    },
    components: {
      MuiCard: {
        styleOverrides: {
          root: {
            borderRadius: 8,
            boxShadow: "none",
            border: `1px solid ${t["--divider-color"]}`
          }
        }
      },
      MuiDivider: {
        styleOverrides: {
          root: {
            borderColor: t["--divider-color"]
          }
        }
      }
    }
  };
}, Mk = (e) => hc(Ok(e));
const Nk = ({ hass: e, config_entry_id: t }) => {
  const [n, r] = w.useState(null), [o, i] = w.useState(!0), [l, s] = w.useState(null), a = w.useMemo(() => {
    var u;
    return Mk(((u = e == null ? void 0 : e.themes) == null ? void 0 : u.darkMode) ?? !0);
  }, [e]);
  return w.useEffect(() => {
    if (!e || !e.connection) {
      s("Home Assistant connection object not found."), i(!1);
      return;
    }
    (async () => {
      try {
        const c = await e.connection.sendMessagePromise({
          type: "meraki_ha/get_config",
          config_entry_id: t
        });
        r(c);
      } catch (c) {
        console.error("Error fetching Meraki data:", c), s(`Failed to fetch Meraki data: ${c.message || "Unknown error"}`);
      } finally {
        i(!1);
      }
    })();
  }, [e, t]), /* @__PURE__ */ C.jsxs(hw, { theme: a, children: [
    /* @__PURE__ */ C.jsx(ww, {}),
    /* @__PURE__ */ C.jsxs(Tr, { sx: { p: 3, backgroundColor: a.palette.background.default, minHeight: "100vh" }, children: [
      /* @__PURE__ */ C.jsx(dC, {}),
      o && /* @__PURE__ */ C.jsx(Tr, { sx: { display: "flex", justifyContent: "center", p: 4 }, children: /* @__PURE__ */ C.jsx(Mw, {}) }),
      l && /* @__PURE__ */ C.jsx(A2, { severity: "error", sx: { mt: 2 }, children: l }),
      !o && !l && n && /* @__PURE__ */ C.jsxs(Ws, { container: !0, spacing: 3, children: [
        /* @__PURE__ */ C.jsx(Ws, { item: !0, xs: 12, children: /* @__PURE__ */ C.jsx(Pr, { elevation: 2, sx: { p: 2 }, children: /* @__PURE__ */ C.jsx(gk, { data: n }) }) }),
        /* @__PURE__ */ C.jsx(Ws, { item: !0, xs: 12, children: /* @__PURE__ */ C.jsx(Pr, { elevation: 2, sx: { p: 2 }, children: /* @__PURE__ */ C.jsx(Rk, {}) }) })
      ] })
    ] })
  ] });
};
class Ik extends HTMLElement {
  connectedCallback() {
    const t = document.createElement("div");
    t.id = "root", this.appendChild(t);
    const n = this.hass, r = this.panel.config.config_entry_id;
    Gs.createRoot(t).render(
      /* @__PURE__ */ C.jsx(qe.StrictMode, { children: /* @__PURE__ */ C.jsx(Nk, { hass: n, config_entry_id: r }) })
    );
  }
}
customElements.define("meraki-panel", Ik);
