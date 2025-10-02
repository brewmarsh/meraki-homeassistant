var C0 = Object.defineProperty;
var k0 = (e, t, n) => t in e ? C0(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var Ho = (e, t, n) => (k0(e, typeof t != "symbol" ? t + "" : t, n), n);
function _0(e, t) {
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
function $0(e) {
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
var Uf = { exports: {} }, cl = {}, Vf = { exports: {} }, D = {};
/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Oo = Symbol.for("react.element"), E0 = Symbol.for("react.portal"), P0 = Symbol.for("react.fragment"), T0 = Symbol.for("react.strict_mode"), R0 = Symbol.for("react.profiler"), M0 = Symbol.for("react.provider"), O0 = Symbol.for("react.context"), j0 = Symbol.for("react.forward_ref"), z0 = Symbol.for("react.suspense"), N0 = Symbol.for("react.memo"), b0 = Symbol.for("react.lazy"), Rc = Symbol.iterator;
function I0(e) {
  return e === null || typeof e != "object" ? null : (e = Rc && e[Rc] || e["@@iterator"], typeof e == "function" ? e : null);
}
var Hf = { isMounted: function() {
  return !1;
}, enqueueForceUpdate: function() {
}, enqueueReplaceState: function() {
}, enqueueSetState: function() {
} }, Kf = Object.assign, Gf = {};
function Cr(e, t, n) {
  this.props = e, this.context = t, this.refs = Gf, this.updater = n || Hf;
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
function Qf() {
}
Qf.prototype = Cr.prototype;
function qa(e, t, n) {
  this.props = e, this.context = t, this.refs = Gf, this.updater = n || Hf;
}
var Za = qa.prototype = new Qf();
Za.constructor = qa;
Kf(Za, Cr.prototype);
Za.isPureReactComponent = !0;
var Mc = Array.isArray, Yf = Object.prototype.hasOwnProperty, Ja = { current: null }, Xf = { key: !0, ref: !0, __self: !0, __source: !0 };
function qf(e, t, n) {
  var r, o = {}, i = null, l = null;
  if (t != null)
    for (r in t.ref !== void 0 && (l = t.ref), t.key !== void 0 && (i = "" + t.key), t)
      Yf.call(t, r) && !Xf.hasOwnProperty(r) && (o[r] = t[r]);
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
  return { $$typeof: Oo, type: e, key: i, ref: l, props: o, _owner: Ja.current };
}
function A0(e, t) {
  return { $$typeof: Oo, type: e.type, key: t, ref: e.ref, props: e.props, _owner: e._owner };
}
function eu(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Oo;
}
function L0(e) {
  var t = { "=": "=0", ":": "=2" };
  return "$" + e.replace(/[=:]/g, function(n) {
    return t[n];
  });
}
var Oc = /\/+/g;
function ps(e, t) {
  return typeof e == "object" && e !== null && e.key != null ? L0("" + e.key) : t.toString(36);
}
function pi(e, t, n, r, o) {
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
          case Oo:
          case E0:
            l = !0;
        }
    }
  if (l)
    return l = e, o = o(l), e = r === "" ? "." + ps(l, 0) : r, Mc(o) ? (n = "", e != null && (n = e.replace(Oc, "$&/") + "/"), pi(o, t, n, "", function(u) {
      return u;
    })) : o != null && (eu(o) && (o = A0(o, n + (!o.key || l && l.key === o.key ? "" : ("" + o.key).replace(Oc, "$&/") + "/") + e)), t.push(o)), 1;
  if (l = 0, r = r === "" ? "." : r + ":", Mc(e))
    for (var s = 0; s < e.length; s++) {
      i = e[s];
      var a = r + ps(i, s);
      l += pi(i, t, n, a, o);
    }
  else if (a = I0(e), typeof a == "function")
    for (e = a.call(e), s = 0; !(i = e.next()).done; )
      i = i.value, a = r + ps(i, s++), l += pi(i, t, n, a, o);
  else if (i === "object")
    throw t = String(e), Error("Objects are not valid as a React child (found: " + (t === "[object Object]" ? "object with keys {" + Object.keys(e).join(", ") + "}" : t) + "). If you meant to render a collection of children, use an array instead.");
  return l;
}
function Ko(e, t, n) {
  if (e == null)
    return e;
  var r = [], o = 0;
  return pi(e, r, "", "", function(i) {
    return t.call(n, i, o++);
  }), r;
}
function D0(e) {
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
var De = { current: null }, mi = { transition: null }, F0 = { ReactCurrentDispatcher: De, ReactCurrentBatchConfig: mi, ReactCurrentOwner: Ja };
function Zf() {
  throw Error("act(...) is not supported in production builds of React.");
}
D.Children = { map: Ko, forEach: function(e, t, n) {
  Ko(e, function() {
    t.apply(this, arguments);
  }, n);
}, count: function(e) {
  var t = 0;
  return Ko(e, function() {
    t++;
  }), t;
}, toArray: function(e) {
  return Ko(e, function(t) {
    return t;
  }) || [];
}, only: function(e) {
  if (!eu(e))
    throw Error("React.Children.only expected to receive a single React element child.");
  return e;
} };
D.Component = Cr;
D.Fragment = P0;
D.Profiler = R0;
D.PureComponent = qa;
D.StrictMode = T0;
D.Suspense = z0;
D.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = F0;
D.act = Zf;
D.cloneElement = function(e, t, n) {
  if (e == null)
    throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + e + ".");
  var r = Kf({}, e.props), o = e.key, i = e.ref, l = e._owner;
  if (t != null) {
    if (t.ref !== void 0 && (i = t.ref, l = Ja.current), t.key !== void 0 && (o = "" + t.key), e.type && e.type.defaultProps)
      var s = e.type.defaultProps;
    for (a in t)
      Yf.call(t, a) && !Xf.hasOwnProperty(a) && (r[a] = t[a] === void 0 && s !== void 0 ? s[a] : t[a]);
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
  return { $$typeof: Oo, type: e.type, key: o, ref: i, props: r, _owner: l };
};
D.createContext = function(e) {
  return e = { $$typeof: O0, _currentValue: e, _currentValue2: e, _threadCount: 0, Provider: null, Consumer: null, _defaultValue: null, _globalName: null }, e.Provider = { $$typeof: M0, _context: e }, e.Consumer = e;
};
D.createElement = qf;
D.createFactory = function(e) {
  var t = qf.bind(null, e);
  return t.type = e, t;
};
D.createRef = function() {
  return { current: null };
};
D.forwardRef = function(e) {
  return { $$typeof: j0, render: e };
};
D.isValidElement = eu;
D.lazy = function(e) {
  return { $$typeof: b0, _payload: { _status: -1, _result: e }, _init: D0 };
};
D.memo = function(e, t) {
  return { $$typeof: N0, type: e, compare: t === void 0 ? null : t };
};
D.startTransition = function(e) {
  var t = mi.transition;
  mi.transition = {};
  try {
    e();
  } finally {
    mi.transition = t;
  }
};
D.unstable_act = Zf;
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
Vf.exports = D;
var _ = Vf.exports;
const wn = /* @__PURE__ */ $0(_), Ys = /* @__PURE__ */ _0({
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
var B0 = _, W0 = Symbol.for("react.element"), U0 = Symbol.for("react.fragment"), V0 = Object.prototype.hasOwnProperty, H0 = B0.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, K0 = { key: !0, ref: !0, __self: !0, __source: !0 };
function Jf(e, t, n) {
  var r, o = {}, i = null, l = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (r in t)
    V0.call(t, r) && !K0.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps)
    for (r in t = e.defaultProps, t)
      o[r] === void 0 && (o[r] = t[r]);
  return { $$typeof: W0, type: e, key: i, ref: l, props: o, _owner: H0.current };
}
cl.Fragment = U0;
cl.jsx = Jf;
cl.jsxs = Jf;
Uf.exports = cl;
var y = Uf.exports, Xs = {}, ep = { exports: {} }, tt = {}, tp = { exports: {} }, np = {};
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
    var b = R.length;
    R.push(z);
    e:
      for (; 0 < b; ) {
        var re = b - 1 >>> 1, me = R[re];
        if (0 < o(me, z))
          R[re] = z, R[b] = me, b = re;
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
    var z = R[0], b = R.pop();
    if (b !== z) {
      R[0] = b;
      e:
        for (var re = 0, me = R.length, In = me >>> 1; re < In; ) {
          var Ie = 2 * (re + 1) - 1, Qt = R[Ie], yt = Ie + 1, An = R[yt];
          if (0 > o(Qt, b))
            yt < me && 0 > o(An, Qt) ? (R[re] = An, R[yt] = b, re = yt) : (R[re] = Qt, R[Ie] = b, re = Ie);
          else if (yt < me && 0 > o(An, b))
            R[re] = An, R[yt] = b, re = yt;
          else
            break e;
        }
    }
    return z;
  }
  function o(R, z) {
    var b = R.sortIndex - z.sortIndex;
    return b !== 0 ? b : R.id - z.id;
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
  var a = [], u = [], c = 1, d = null, p = 3, v = !1, x = !1, g = !1, E = typeof setTimeout == "function" ? setTimeout : null, m = typeof clearTimeout == "function" ? clearTimeout : null, f = typeof setImmediate < "u" ? setImmediate : null;
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
  function S(R) {
    if (g = !1, h(R), !x)
      if (n(a) !== null)
        x = !0, Ee($);
      else {
        var z = n(u);
        z !== null && Ge(S, z.startTime - R);
      }
  }
  function $(R, z) {
    x = !1, g && (g = !1, m(T), T = -1), v = !0;
    var b = p;
    try {
      for (h(z), d = n(a); d !== null && (!(d.expirationTime > z) || R && !U()); ) {
        var re = d.callback;
        if (typeof re == "function") {
          d.callback = null, p = d.priorityLevel;
          var me = re(d.expirationTime <= z);
          z = e.unstable_now(), typeof me == "function" ? d.callback = me : d === n(a) && r(a), h(z);
        } else
          r(a);
        d = n(a);
      }
      if (d !== null)
        var In = !0;
      else {
        var Ie = n(u);
        Ie !== null && Ge(S, Ie.startTime - z), In = !1;
      }
      return In;
    } finally {
      d = null, p = b, v = !1;
    }
  }
  var k = !1, C = null, T = -1, j = 5, M = -1;
  function U() {
    return !(e.unstable_now() - M < j);
  }
  function F() {
    if (C !== null) {
      var R = e.unstable_now();
      M = R;
      var z = !0;
      try {
        z = C(!0, R);
      } finally {
        z ? A() : (k = !1, C = null);
      }
    } else
      k = !1;
  }
  var A;
  if (typeof f == "function")
    A = function() {
      f(F);
    };
  else if (typeof MessageChannel < "u") {
    var Z = new MessageChannel(), xe = Z.port2;
    Z.port1.onmessage = F, A = function() {
      xe.postMessage(null);
    };
  } else
    A = function() {
      E(F, 0);
    };
  function Ee(R) {
    C = R, k || (k = !0, A());
  }
  function Ge(R, z) {
    T = E(function() {
      R(e.unstable_now());
    }, z);
  }
  e.unstable_IdlePriority = 5, e.unstable_ImmediatePriority = 1, e.unstable_LowPriority = 4, e.unstable_NormalPriority = 3, e.unstable_Profiling = null, e.unstable_UserBlockingPriority = 2, e.unstable_cancelCallback = function(R) {
    R.callback = null;
  }, e.unstable_continueExecution = function() {
    x || v || (x = !0, Ee($));
  }, e.unstable_forceFrameRate = function(R) {
    0 > R || 125 < R ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : j = 0 < R ? Math.floor(1e3 / R) : 5;
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
    var b = p;
    p = z;
    try {
      return R();
    } finally {
      p = b;
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
    var b = p;
    p = R;
    try {
      return z();
    } finally {
      p = b;
    }
  }, e.unstable_scheduleCallback = function(R, z, b) {
    var re = e.unstable_now();
    switch (typeof b == "object" && b !== null ? (b = b.delay, b = typeof b == "number" && 0 < b ? re + b : re) : b = re, R) {
      case 1:
        var me = -1;
        break;
      case 2:
        me = 250;
        break;
      case 5:
        me = 1073741823;
        break;
      case 4:
        me = 1e4;
        break;
      default:
        me = 5e3;
    }
    return me = b + me, R = { id: c++, callback: z, priorityLevel: R, startTime: b, expirationTime: me, sortIndex: -1 }, b > re ? (R.sortIndex = b, t(u, R), n(a) === null && R === n(u) && (g ? (m(T), T = -1) : g = !0, Ge(S, b - re))) : (R.sortIndex = me, t(a, R), x || v || (x = !0, Ee($))), R;
  }, e.unstable_shouldYield = U, e.unstable_wrapCallback = function(R) {
    var z = p;
    return function() {
      var b = p;
      p = z;
      try {
        return R.apply(this, arguments);
      } finally {
        p = b;
      }
    };
  };
})(np);
tp.exports = np;
var G0 = tp.exports;
/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Q0 = _, et = G0;
function P(e) {
  for (var t = "https://reactjs.org/docs/error-decoder.html?invariant=" + e, n = 1; n < arguments.length; n++)
    t += "&args[]=" + encodeURIComponent(arguments[n]);
  return "Minified React error #" + e + "; visit " + t + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
}
var rp = /* @__PURE__ */ new Set(), lo = {};
function Nn(e, t) {
  dr(e, t), dr(e + "Capture", t);
}
function dr(e, t) {
  for (lo[e] = t, e = 0; e < t.length; e++)
    rp.add(t[e]);
}
var Wt = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), qs = Object.prototype.hasOwnProperty, Y0 = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, jc = {}, zc = {};
function X0(e) {
  return qs.call(zc, e) ? !0 : qs.call(jc, e) ? !1 : Y0.test(e) ? zc[e] = !0 : (jc[e] = !0, !1);
}
function q0(e, t, n, r) {
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
function Z0(e, t, n, r) {
  if (t === null || typeof t > "u" || q0(e, t, n, r))
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
var tu = /[\-:]([a-z])/g;
function nu(e) {
  return e[1].toUpperCase();
}
"accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(e) {
  var t = e.replace(
    tu,
    nu
  );
  Me[t] = new Fe(t, 1, !1, e, null, !1, !1);
});
"xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(e) {
  var t = e.replace(tu, nu);
  Me[t] = new Fe(t, 1, !1, e, "http://www.w3.org/1999/xlink", !1, !1);
});
["xml:base", "xml:lang", "xml:space"].forEach(function(e) {
  var t = e.replace(tu, nu);
  Me[t] = new Fe(t, 1, !1, e, "http://www.w3.org/XML/1998/namespace", !1, !1);
});
["tabIndex", "crossOrigin"].forEach(function(e) {
  Me[e] = new Fe(e, 1, !1, e.toLowerCase(), null, !1, !1);
});
Me.xlinkHref = new Fe("xlinkHref", 1, !1, "xlink:href", "http://www.w3.org/1999/xlink", !0, !1);
["src", "href", "action", "formAction"].forEach(function(e) {
  Me[e] = new Fe(e, 1, !1, e.toLowerCase(), null, !0, !0);
});
function ru(e, t, n, r) {
  var o = Me.hasOwnProperty(t) ? Me[t] : null;
  (o !== null ? o.type !== 0 : r || !(2 < t.length) || t[0] !== "o" && t[0] !== "O" || t[1] !== "n" && t[1] !== "N") && (Z0(t, n, o, r) && (n = null), r || o === null ? X0(t) && (n === null ? e.removeAttribute(t) : e.setAttribute(t, "" + n)) : o.mustUseProperty ? e[o.propertyName] = n === null ? o.type === 3 ? !1 : "" : n : (t = o.attributeName, r = o.attributeNamespace, n === null ? e.removeAttribute(t) : (o = o.type, n = o === 3 || o === 4 && n === !0 ? "" : "" + n, r ? e.setAttributeNS(r, t, n) : e.setAttribute(t, n))));
}
var Gt = Q0.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, Go = Symbol.for("react.element"), Vn = Symbol.for("react.portal"), Hn = Symbol.for("react.fragment"), ou = Symbol.for("react.strict_mode"), Zs = Symbol.for("react.profiler"), op = Symbol.for("react.provider"), ip = Symbol.for("react.context"), iu = Symbol.for("react.forward_ref"), Js = Symbol.for("react.suspense"), ea = Symbol.for("react.suspense_list"), lu = Symbol.for("react.memo"), Zt = Symbol.for("react.lazy"), lp = Symbol.for("react.offscreen"), Nc = Symbol.iterator;
function zr(e) {
  return e === null || typeof e != "object" ? null : (e = Nc && e[Nc] || e["@@iterator"], typeof e == "function" ? e : null);
}
var le = Object.assign, ms;
function Hr(e) {
  if (ms === void 0)
    try {
      throw Error();
    } catch (n) {
      var t = n.stack.trim().match(/\n( *(at )?)/);
      ms = t && t[1] || "";
    }
  return `
` + ms + e;
}
var hs = !1;
function gs(e, t) {
  if (!e || hs)
    return "";
  hs = !0;
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
    hs = !1, Error.prepareStackTrace = n;
  }
  return (e = e ? e.displayName || e.name : "") ? Hr(e) : "";
}
function J0(e) {
  switch (e.tag) {
    case 5:
      return Hr(e.type);
    case 16:
      return Hr("Lazy");
    case 13:
      return Hr("Suspense");
    case 19:
      return Hr("SuspenseList");
    case 0:
    case 2:
    case 15:
      return e = gs(e.type, !1), e;
    case 11:
      return e = gs(e.type.render, !1), e;
    case 1:
      return e = gs(e.type, !0), e;
    default:
      return "";
  }
}
function ta(e) {
  if (e == null)
    return null;
  if (typeof e == "function")
    return e.displayName || e.name || null;
  if (typeof e == "string")
    return e;
  switch (e) {
    case Hn:
      return "Fragment";
    case Vn:
      return "Portal";
    case Zs:
      return "Profiler";
    case ou:
      return "StrictMode";
    case Js:
      return "Suspense";
    case ea:
      return "SuspenseList";
  }
  if (typeof e == "object")
    switch (e.$$typeof) {
      case ip:
        return (e.displayName || "Context") + ".Consumer";
      case op:
        return (e._context.displayName || "Context") + ".Provider";
      case iu:
        var t = e.render;
        return e = e.displayName, e || (e = t.displayName || t.name || "", e = e !== "" ? "ForwardRef(" + e + ")" : "ForwardRef"), e;
      case lu:
        return t = e.displayName || null, t !== null ? t : ta(e.type) || "Memo";
      case Zt:
        t = e._payload, e = e._init;
        try {
          return ta(e(t));
        } catch {
        }
    }
  return null;
}
function eg(e) {
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
      return ta(t);
    case 8:
      return t === ou ? "StrictMode" : "Mode";
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
function sp(e) {
  var t = e.type;
  return (e = e.nodeName) && e.toLowerCase() === "input" && (t === "checkbox" || t === "radio");
}
function tg(e) {
  var t = sp(e) ? "checked" : "value", n = Object.getOwnPropertyDescriptor(e.constructor.prototype, t), r = "" + e[t];
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
function Qo(e) {
  e._valueTracker || (e._valueTracker = tg(e));
}
function ap(e) {
  if (!e)
    return !1;
  var t = e._valueTracker;
  if (!t)
    return !0;
  var n = t.getValue(), r = "";
  return e && (r = sp(e) ? e.checked ? "true" : "false" : e.value), e = r, e !== n ? (t.setValue(e), !0) : !1;
}
function Oi(e) {
  if (e = e || (typeof document < "u" ? document : void 0), typeof e > "u")
    return null;
  try {
    return e.activeElement || e.body;
  } catch {
    return e.body;
  }
}
function na(e, t) {
  var n = t.checked;
  return le({}, t, { defaultChecked: void 0, defaultValue: void 0, value: void 0, checked: n ?? e._wrapperState.initialChecked });
}
function bc(e, t) {
  var n = t.defaultValue == null ? "" : t.defaultValue, r = t.checked != null ? t.checked : t.defaultChecked;
  n = pn(t.value != null ? t.value : n), e._wrapperState = { initialChecked: r, initialValue: n, controlled: t.type === "checkbox" || t.type === "radio" ? t.checked != null : t.value != null };
}
function up(e, t) {
  t = t.checked, t != null && ru(e, "checked", t, !1);
}
function ra(e, t) {
  up(e, t);
  var n = pn(t.value), r = t.type;
  if (n != null)
    r === "number" ? (n === 0 && e.value === "" || e.value != n) && (e.value = "" + n) : e.value !== "" + n && (e.value = "" + n);
  else if (r === "submit" || r === "reset") {
    e.removeAttribute("value");
    return;
  }
  t.hasOwnProperty("value") ? oa(e, t.type, n) : t.hasOwnProperty("defaultValue") && oa(e, t.type, pn(t.defaultValue)), t.checked == null && t.defaultChecked != null && (e.defaultChecked = !!t.defaultChecked);
}
function Ic(e, t, n) {
  if (t.hasOwnProperty("value") || t.hasOwnProperty("defaultValue")) {
    var r = t.type;
    if (!(r !== "submit" && r !== "reset" || t.value !== void 0 && t.value !== null))
      return;
    t = "" + e._wrapperState.initialValue, n || t === e.value || (e.value = t), e.defaultValue = t;
  }
  n = e.name, n !== "" && (e.name = ""), e.defaultChecked = !!e._wrapperState.initialChecked, n !== "" && (e.name = n);
}
function oa(e, t, n) {
  (t !== "number" || Oi(e.ownerDocument) !== e) && (n == null ? e.defaultValue = "" + e._wrapperState.initialValue : e.defaultValue !== "" + n && (e.defaultValue = "" + n));
}
var Kr = Array.isArray;
function nr(e, t, n, r) {
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
function ia(e, t) {
  if (t.dangerouslySetInnerHTML != null)
    throw Error(P(91));
  return le({}, t, { value: void 0, defaultValue: void 0, children: "" + e._wrapperState.initialValue });
}
function Ac(e, t) {
  var n = t.value;
  if (n == null) {
    if (n = t.children, t = t.defaultValue, n != null) {
      if (t != null)
        throw Error(P(92));
      if (Kr(n)) {
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
function cp(e, t) {
  var n = pn(t.value), r = pn(t.defaultValue);
  n != null && (n = "" + n, n !== e.value && (e.value = n), t.defaultValue == null && e.defaultValue !== n && (e.defaultValue = n)), r != null && (e.defaultValue = "" + r);
}
function Lc(e) {
  var t = e.textContent;
  t === e._wrapperState.initialValue && t !== "" && t !== null && (e.value = t);
}
function dp(e) {
  switch (e) {
    case "svg":
      return "http://www.w3.org/2000/svg";
    case "math":
      return "http://www.w3.org/1998/Math/MathML";
    default:
      return "http://www.w3.org/1999/xhtml";
  }
}
function la(e, t) {
  return e == null || e === "http://www.w3.org/1999/xhtml" ? dp(t) : e === "http://www.w3.org/2000/svg" && t === "foreignObject" ? "http://www.w3.org/1999/xhtml" : e;
}
var Yo, fp = function(e) {
  return typeof MSApp < "u" && MSApp.execUnsafeLocalFunction ? function(t, n, r, o) {
    MSApp.execUnsafeLocalFunction(function() {
      return e(t, n, r, o);
    });
  } : e;
}(function(e, t) {
  if (e.namespaceURI !== "http://www.w3.org/2000/svg" || "innerHTML" in e)
    e.innerHTML = t;
  else {
    for (Yo = Yo || document.createElement("div"), Yo.innerHTML = "<svg>" + t.valueOf().toString() + "</svg>", t = Yo.firstChild; e.firstChild; )
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
}, ng = ["Webkit", "ms", "Moz", "O"];
Object.keys(Xr).forEach(function(e) {
  ng.forEach(function(t) {
    t = t + e.charAt(0).toUpperCase() + e.substring(1), Xr[t] = Xr[e];
  });
});
function pp(e, t, n) {
  return t == null || typeof t == "boolean" || t === "" ? "" : n || typeof t != "number" || t === 0 || Xr.hasOwnProperty(e) && Xr[e] ? ("" + t).trim() : t + "px";
}
function mp(e, t) {
  e = e.style;
  for (var n in t)
    if (t.hasOwnProperty(n)) {
      var r = n.indexOf("--") === 0, o = pp(n, t[n], r);
      n === "float" && (n = "cssFloat"), r ? e.setProperty(n, o) : e[n] = o;
    }
}
var rg = le({ menuitem: !0 }, { area: !0, base: !0, br: !0, col: !0, embed: !0, hr: !0, img: !0, input: !0, keygen: !0, link: !0, meta: !0, param: !0, source: !0, track: !0, wbr: !0 });
function sa(e, t) {
  if (t) {
    if (rg[e] && (t.children != null || t.dangerouslySetInnerHTML != null))
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
function aa(e, t) {
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
var ua = null;
function su(e) {
  return e = e.target || e.srcElement || window, e.correspondingUseElement && (e = e.correspondingUseElement), e.nodeType === 3 ? e.parentNode : e;
}
var ca = null, rr = null, or = null;
function Dc(e) {
  if (e = No(e)) {
    if (typeof ca != "function")
      throw Error(P(280));
    var t = e.stateNode;
    t && (t = hl(t), ca(e.stateNode, e.type, t));
  }
}
function hp(e) {
  rr ? or ? or.push(e) : or = [e] : rr = e;
}
function gp() {
  if (rr) {
    var e = rr, t = or;
    if (or = rr = null, Dc(e), t)
      for (e = 0; e < t.length; e++)
        Dc(t[e]);
  }
}
function vp(e, t) {
  return e(t);
}
function yp() {
}
var vs = !1;
function xp(e, t, n) {
  if (vs)
    return e(t, n);
  vs = !0;
  try {
    return vp(e, t, n);
  } finally {
    vs = !1, (rr !== null || or !== null) && (yp(), gp());
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
var da = !1;
if (Wt)
  try {
    var Nr = {};
    Object.defineProperty(Nr, "passive", { get: function() {
      da = !0;
    } }), window.addEventListener("test", Nr, Nr), window.removeEventListener("test", Nr, Nr);
  } catch {
    da = !1;
  }
function og(e, t, n, r, o, i, l, s, a) {
  var u = Array.prototype.slice.call(arguments, 3);
  try {
    t.apply(n, u);
  } catch (c) {
    this.onError(c);
  }
}
var qr = !1, ji = null, zi = !1, fa = null, ig = { onError: function(e) {
  qr = !0, ji = e;
} };
function lg(e, t, n, r, o, i, l, s, a) {
  qr = !1, ji = null, og.apply(ig, arguments);
}
function sg(e, t, n, r, o, i, l, s, a) {
  if (lg.apply(this, arguments), qr) {
    if (qr) {
      var u = ji;
      qr = !1, ji = null;
    } else
      throw Error(P(198));
    zi || (zi = !0, fa = u);
  }
}
function bn(e) {
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
function Sp(e) {
  if (e.tag === 13) {
    var t = e.memoizedState;
    if (t === null && (e = e.alternate, e !== null && (t = e.memoizedState)), t !== null)
      return t.dehydrated;
  }
  return null;
}
function Fc(e) {
  if (bn(e) !== e)
    throw Error(P(188));
}
function ag(e) {
  var t = e.alternate;
  if (!t) {
    if (t = bn(e), t === null)
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
          return Fc(o), e;
        if (i === r)
          return Fc(o), t;
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
function wp(e) {
  return e = ag(e), e !== null ? Cp(e) : null;
}
function Cp(e) {
  if (e.tag === 5 || e.tag === 6)
    return e;
  for (e = e.child; e !== null; ) {
    var t = Cp(e);
    if (t !== null)
      return t;
    e = e.sibling;
  }
  return null;
}
var kp = et.unstable_scheduleCallback, Bc = et.unstable_cancelCallback, ug = et.unstable_shouldYield, cg = et.unstable_requestPaint, ce = et.unstable_now, dg = et.unstable_getCurrentPriorityLevel, au = et.unstable_ImmediatePriority, _p = et.unstable_UserBlockingPriority, Ni = et.unstable_NormalPriority, fg = et.unstable_LowPriority, $p = et.unstable_IdlePriority, dl = null, Ot = null;
function pg(e) {
  if (Ot && typeof Ot.onCommitFiberRoot == "function")
    try {
      Ot.onCommitFiberRoot(dl, e, void 0, (e.current.flags & 128) === 128);
    } catch {
    }
}
var kt = Math.clz32 ? Math.clz32 : gg, mg = Math.log, hg = Math.LN2;
function gg(e) {
  return e >>>= 0, e === 0 ? 32 : 31 - (mg(e) / hg | 0) | 0;
}
var Xo = 64, qo = 4194304;
function Gr(e) {
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
function bi(e, t) {
  var n = e.pendingLanes;
  if (n === 0)
    return 0;
  var r = 0, o = e.suspendedLanes, i = e.pingedLanes, l = n & 268435455;
  if (l !== 0) {
    var s = l & ~o;
    s !== 0 ? r = Gr(s) : (i &= l, i !== 0 && (r = Gr(i)));
  } else
    l = n & ~o, l !== 0 ? r = Gr(l) : i !== 0 && (r = Gr(i));
  if (r === 0)
    return 0;
  if (t !== 0 && t !== r && !(t & o) && (o = r & -r, i = t & -t, o >= i || o === 16 && (i & 4194240) !== 0))
    return t;
  if (r & 4 && (r |= n & 16), t = e.entangledLanes, t !== 0)
    for (e = e.entanglements, t &= r; 0 < t; )
      n = 31 - kt(t), o = 1 << n, r |= e[n], t &= ~o;
  return r;
}
function vg(e, t) {
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
function yg(e, t) {
  for (var n = e.suspendedLanes, r = e.pingedLanes, o = e.expirationTimes, i = e.pendingLanes; 0 < i; ) {
    var l = 31 - kt(i), s = 1 << l, a = o[l];
    a === -1 ? (!(s & n) || s & r) && (o[l] = vg(s, t)) : a <= t && (e.expiredLanes |= s), i &= ~s;
  }
}
function pa(e) {
  return e = e.pendingLanes & -1073741825, e !== 0 ? e : e & 1073741824 ? 1073741824 : 0;
}
function Ep() {
  var e = Xo;
  return Xo <<= 1, !(Xo & 4194240) && (Xo = 64), e;
}
function ys(e) {
  for (var t = [], n = 0; 31 > n; n++)
    t.push(e);
  return t;
}
function jo(e, t, n) {
  e.pendingLanes |= t, t !== 536870912 && (e.suspendedLanes = 0, e.pingedLanes = 0), e = e.eventTimes, t = 31 - kt(t), e[t] = n;
}
function xg(e, t) {
  var n = e.pendingLanes & ~t;
  e.pendingLanes = t, e.suspendedLanes = 0, e.pingedLanes = 0, e.expiredLanes &= t, e.mutableReadLanes &= t, e.entangledLanes &= t, t = e.entanglements;
  var r = e.eventTimes;
  for (e = e.expirationTimes; 0 < n; ) {
    var o = 31 - kt(n), i = 1 << o;
    t[o] = 0, r[o] = -1, e[o] = -1, n &= ~i;
  }
}
function uu(e, t) {
  var n = e.entangledLanes |= t;
  for (e = e.entanglements; n; ) {
    var r = 31 - kt(n), o = 1 << r;
    o & t | e[r] & t && (e[r] |= t), n &= ~o;
  }
}
var G = 0;
function Pp(e) {
  return e &= -e, 1 < e ? 4 < e ? e & 268435455 ? 16 : 536870912 : 4 : 1;
}
var Tp, cu, Rp, Mp, Op, ma = !1, Zo = [], on = null, ln = null, sn = null, uo = /* @__PURE__ */ new Map(), co = /* @__PURE__ */ new Map(), en = [], Sg = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
function Wc(e, t) {
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
      uo.delete(t.pointerId);
      break;
    case "gotpointercapture":
    case "lostpointercapture":
      co.delete(t.pointerId);
  }
}
function br(e, t, n, r, o, i) {
  return e === null || e.nativeEvent !== i ? (e = { blockedOn: t, domEventName: n, eventSystemFlags: r, nativeEvent: i, targetContainers: [o] }, t !== null && (t = No(t), t !== null && cu(t)), e) : (e.eventSystemFlags |= r, t = e.targetContainers, o !== null && t.indexOf(o) === -1 && t.push(o), e);
}
function wg(e, t, n, r, o) {
  switch (t) {
    case "focusin":
      return on = br(on, e, t, n, r, o), !0;
    case "dragenter":
      return ln = br(ln, e, t, n, r, o), !0;
    case "mouseover":
      return sn = br(sn, e, t, n, r, o), !0;
    case "pointerover":
      var i = o.pointerId;
      return uo.set(i, br(uo.get(i) || null, e, t, n, r, o)), !0;
    case "gotpointercapture":
      return i = o.pointerId, co.set(i, br(co.get(i) || null, e, t, n, r, o)), !0;
  }
  return !1;
}
function jp(e) {
  var t = Cn(e.target);
  if (t !== null) {
    var n = bn(t);
    if (n !== null) {
      if (t = n.tag, t === 13) {
        if (t = Sp(n), t !== null) {
          e.blockedOn = t, Op(e.priority, function() {
            Rp(n);
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
function hi(e) {
  if (e.blockedOn !== null)
    return !1;
  for (var t = e.targetContainers; 0 < t.length; ) {
    var n = ha(e.domEventName, e.eventSystemFlags, t[0], e.nativeEvent);
    if (n === null) {
      n = e.nativeEvent;
      var r = new n.constructor(n.type, n);
      ua = r, n.target.dispatchEvent(r), ua = null;
    } else
      return t = No(n), t !== null && cu(t), e.blockedOn = n, !1;
    t.shift();
  }
  return !0;
}
function Uc(e, t, n) {
  hi(e) && n.delete(t);
}
function Cg() {
  ma = !1, on !== null && hi(on) && (on = null), ln !== null && hi(ln) && (ln = null), sn !== null && hi(sn) && (sn = null), uo.forEach(Uc), co.forEach(Uc);
}
function Ir(e, t) {
  e.blockedOn === t && (e.blockedOn = null, ma || (ma = !0, et.unstable_scheduleCallback(et.unstable_NormalPriority, Cg)));
}
function fo(e) {
  function t(o) {
    return Ir(o, e);
  }
  if (0 < Zo.length) {
    Ir(Zo[0], e);
    for (var n = 1; n < Zo.length; n++) {
      var r = Zo[n];
      r.blockedOn === e && (r.blockedOn = null);
    }
  }
  for (on !== null && Ir(on, e), ln !== null && Ir(ln, e), sn !== null && Ir(sn, e), uo.forEach(t), co.forEach(t), n = 0; n < en.length; n++)
    r = en[n], r.blockedOn === e && (r.blockedOn = null);
  for (; 0 < en.length && (n = en[0], n.blockedOn === null); )
    jp(n), n.blockedOn === null && en.shift();
}
var ir = Gt.ReactCurrentBatchConfig, Ii = !0;
function kg(e, t, n, r) {
  var o = G, i = ir.transition;
  ir.transition = null;
  try {
    G = 1, du(e, t, n, r);
  } finally {
    G = o, ir.transition = i;
  }
}
function _g(e, t, n, r) {
  var o = G, i = ir.transition;
  ir.transition = null;
  try {
    G = 4, du(e, t, n, r);
  } finally {
    G = o, ir.transition = i;
  }
}
function du(e, t, n, r) {
  if (Ii) {
    var o = ha(e, t, n, r);
    if (o === null)
      Ts(e, t, r, Ai, n), Wc(e, r);
    else if (wg(o, e, t, n, r))
      r.stopPropagation();
    else if (Wc(e, r), t & 4 && -1 < Sg.indexOf(e)) {
      for (; o !== null; ) {
        var i = No(o);
        if (i !== null && Tp(i), i = ha(e, t, n, r), i === null && Ts(e, t, r, Ai, n), i === o)
          break;
        o = i;
      }
      o !== null && r.stopPropagation();
    } else
      Ts(e, t, r, null, n);
  }
}
var Ai = null;
function ha(e, t, n, r) {
  if (Ai = null, e = su(r), e = Cn(e), e !== null)
    if (t = bn(e), t === null)
      e = null;
    else if (n = t.tag, n === 13) {
      if (e = Sp(t), e !== null)
        return e;
      e = null;
    } else if (n === 3) {
      if (t.stateNode.current.memoizedState.isDehydrated)
        return t.tag === 3 ? t.stateNode.containerInfo : null;
      e = null;
    } else
      t !== e && (e = null);
  return Ai = e, null;
}
function zp(e) {
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
      switch (dg()) {
        case au:
          return 1;
        case _p:
          return 4;
        case Ni:
        case fg:
          return 16;
        case $p:
          return 536870912;
        default:
          return 16;
      }
    default:
      return 16;
  }
}
var nn = null, fu = null, gi = null;
function Np() {
  if (gi)
    return gi;
  var e, t = fu, n = t.length, r, o = "value" in nn ? nn.value : nn.textContent, i = o.length;
  for (e = 0; e < n && t[e] === o[e]; e++)
    ;
  var l = n - e;
  for (r = 1; r <= l && t[n - r] === o[i - r]; r++)
    ;
  return gi = o.slice(e, 1 < r ? 1 - r : void 0);
}
function vi(e) {
  var t = e.keyCode;
  return "charCode" in e ? (e = e.charCode, e === 0 && t === 13 && (e = 13)) : e = t, e === 10 && (e = 13), 32 <= e || e === 13 ? e : 0;
}
function Jo() {
  return !0;
}
function Vc() {
  return !1;
}
function nt(e) {
  function t(n, r, o, i, l) {
    this._reactName = n, this._targetInst = o, this.type = r, this.nativeEvent = i, this.target = l, this.currentTarget = null;
    for (var s in e)
      e.hasOwnProperty(s) && (n = e[s], this[s] = n ? n(i) : i[s]);
    return this.isDefaultPrevented = (i.defaultPrevented != null ? i.defaultPrevented : i.returnValue === !1) ? Jo : Vc, this.isPropagationStopped = Vc, this;
  }
  return le(t.prototype, { preventDefault: function() {
    this.defaultPrevented = !0;
    var n = this.nativeEvent;
    n && (n.preventDefault ? n.preventDefault() : typeof n.returnValue != "unknown" && (n.returnValue = !1), this.isDefaultPrevented = Jo);
  }, stopPropagation: function() {
    var n = this.nativeEvent;
    n && (n.stopPropagation ? n.stopPropagation() : typeof n.cancelBubble != "unknown" && (n.cancelBubble = !0), this.isPropagationStopped = Jo);
  }, persist: function() {
  }, isPersistent: Jo }), t;
}
var kr = { eventPhase: 0, bubbles: 0, cancelable: 0, timeStamp: function(e) {
  return e.timeStamp || Date.now();
}, defaultPrevented: 0, isTrusted: 0 }, pu = nt(kr), zo = le({}, kr, { view: 0, detail: 0 }), $g = nt(zo), xs, Ss, Ar, fl = le({}, zo, { screenX: 0, screenY: 0, clientX: 0, clientY: 0, pageX: 0, pageY: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, getModifierState: mu, button: 0, buttons: 0, relatedTarget: function(e) {
  return e.relatedTarget === void 0 ? e.fromElement === e.srcElement ? e.toElement : e.fromElement : e.relatedTarget;
}, movementX: function(e) {
  return "movementX" in e ? e.movementX : (e !== Ar && (Ar && e.type === "mousemove" ? (xs = e.screenX - Ar.screenX, Ss = e.screenY - Ar.screenY) : Ss = xs = 0, Ar = e), xs);
}, movementY: function(e) {
  return "movementY" in e ? e.movementY : Ss;
} }), Hc = nt(fl), Eg = le({}, fl, { dataTransfer: 0 }), Pg = nt(Eg), Tg = le({}, zo, { relatedTarget: 0 }), ws = nt(Tg), Rg = le({}, kr, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }), Mg = nt(Rg), Og = le({}, kr, { clipboardData: function(e) {
  return "clipboardData" in e ? e.clipboardData : window.clipboardData;
} }), jg = nt(Og), zg = le({}, kr, { data: 0 }), Kc = nt(zg), Ng = {
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
}, bg = {
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
}, Ig = { Alt: "altKey", Control: "ctrlKey", Meta: "metaKey", Shift: "shiftKey" };
function Ag(e) {
  var t = this.nativeEvent;
  return t.getModifierState ? t.getModifierState(e) : (e = Ig[e]) ? !!t[e] : !1;
}
function mu() {
  return Ag;
}
var Lg = le({}, zo, { key: function(e) {
  if (e.key) {
    var t = Ng[e.key] || e.key;
    if (t !== "Unidentified")
      return t;
  }
  return e.type === "keypress" ? (e = vi(e), e === 13 ? "Enter" : String.fromCharCode(e)) : e.type === "keydown" || e.type === "keyup" ? bg[e.keyCode] || "Unidentified" : "";
}, code: 0, location: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, repeat: 0, locale: 0, getModifierState: mu, charCode: function(e) {
  return e.type === "keypress" ? vi(e) : 0;
}, keyCode: function(e) {
  return e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
}, which: function(e) {
  return e.type === "keypress" ? vi(e) : e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
} }), Dg = nt(Lg), Fg = le({}, fl, { pointerId: 0, width: 0, height: 0, pressure: 0, tangentialPressure: 0, tiltX: 0, tiltY: 0, twist: 0, pointerType: 0, isPrimary: 0 }), Gc = nt(Fg), Bg = le({}, zo, { touches: 0, targetTouches: 0, changedTouches: 0, altKey: 0, metaKey: 0, ctrlKey: 0, shiftKey: 0, getModifierState: mu }), Wg = nt(Bg), Ug = le({}, kr, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }), Vg = nt(Ug), Hg = le({}, fl, {
  deltaX: function(e) {
    return "deltaX" in e ? e.deltaX : "wheelDeltaX" in e ? -e.wheelDeltaX : 0;
  },
  deltaY: function(e) {
    return "deltaY" in e ? e.deltaY : "wheelDeltaY" in e ? -e.wheelDeltaY : "wheelDelta" in e ? -e.wheelDelta : 0;
  },
  deltaZ: 0,
  deltaMode: 0
}), Kg = nt(Hg), Gg = [9, 13, 27, 32], hu = Wt && "CompositionEvent" in window, Zr = null;
Wt && "documentMode" in document && (Zr = document.documentMode);
var Qg = Wt && "TextEvent" in window && !Zr, bp = Wt && (!hu || Zr && 8 < Zr && 11 >= Zr), Qc = String.fromCharCode(32), Yc = !1;
function Ip(e, t) {
  switch (e) {
    case "keyup":
      return Gg.indexOf(t.keyCode) !== -1;
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
function Ap(e) {
  return e = e.detail, typeof e == "object" && "data" in e ? e.data : null;
}
var Kn = !1;
function Yg(e, t) {
  switch (e) {
    case "compositionend":
      return Ap(t);
    case "keypress":
      return t.which !== 32 ? null : (Yc = !0, Qc);
    case "textInput":
      return e = t.data, e === Qc && Yc ? null : e;
    default:
      return null;
  }
}
function Xg(e, t) {
  if (Kn)
    return e === "compositionend" || !hu && Ip(e, t) ? (e = Np(), gi = fu = nn = null, Kn = !1, e) : null;
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
      return bp && t.locale !== "ko" ? null : t.data;
    default:
      return null;
  }
}
var qg = { color: !0, date: !0, datetime: !0, "datetime-local": !0, email: !0, month: !0, number: !0, password: !0, range: !0, search: !0, tel: !0, text: !0, time: !0, url: !0, week: !0 };
function Xc(e) {
  var t = e && e.nodeName && e.nodeName.toLowerCase();
  return t === "input" ? !!qg[e.type] : t === "textarea";
}
function Lp(e, t, n, r) {
  hp(r), t = Li(t, "onChange"), 0 < t.length && (n = new pu("onChange", "change", null, n, r), e.push({ event: n, listeners: t }));
}
var Jr = null, po = null;
function Zg(e) {
  Yp(e, 0);
}
function pl(e) {
  var t = Yn(e);
  if (ap(t))
    return e;
}
function Jg(e, t) {
  if (e === "change")
    return t;
}
var Dp = !1;
if (Wt) {
  var Cs;
  if (Wt) {
    var ks = "oninput" in document;
    if (!ks) {
      var qc = document.createElement("div");
      qc.setAttribute("oninput", "return;"), ks = typeof qc.oninput == "function";
    }
    Cs = ks;
  } else
    Cs = !1;
  Dp = Cs && (!document.documentMode || 9 < document.documentMode);
}
function Zc() {
  Jr && (Jr.detachEvent("onpropertychange", Fp), po = Jr = null);
}
function Fp(e) {
  if (e.propertyName === "value" && pl(po)) {
    var t = [];
    Lp(t, po, e, su(e)), xp(Zg, t);
  }
}
function ev(e, t, n) {
  e === "focusin" ? (Zc(), Jr = t, po = n, Jr.attachEvent("onpropertychange", Fp)) : e === "focusout" && Zc();
}
function tv(e) {
  if (e === "selectionchange" || e === "keyup" || e === "keydown")
    return pl(po);
}
function nv(e, t) {
  if (e === "click")
    return pl(t);
}
function rv(e, t) {
  if (e === "input" || e === "change")
    return pl(t);
}
function ov(e, t) {
  return e === t && (e !== 0 || 1 / e === 1 / t) || e !== e && t !== t;
}
var $t = typeof Object.is == "function" ? Object.is : ov;
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
    if (!qs.call(t, o) || !$t(e[o], t[o]))
      return !1;
  }
  return !0;
}
function Jc(e) {
  for (; e && e.firstChild; )
    e = e.firstChild;
  return e;
}
function ed(e, t) {
  var n = Jc(e);
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
    n = Jc(n);
  }
}
function Bp(e, t) {
  return e && t ? e === t ? !0 : e && e.nodeType === 3 ? !1 : t && t.nodeType === 3 ? Bp(e, t.parentNode) : "contains" in e ? e.contains(t) : e.compareDocumentPosition ? !!(e.compareDocumentPosition(t) & 16) : !1 : !1;
}
function Wp() {
  for (var e = window, t = Oi(); t instanceof e.HTMLIFrameElement; ) {
    try {
      var n = typeof t.contentWindow.location.href == "string";
    } catch {
      n = !1;
    }
    if (n)
      e = t.contentWindow;
    else
      break;
    t = Oi(e.document);
  }
  return t;
}
function gu(e) {
  var t = e && e.nodeName && e.nodeName.toLowerCase();
  return t && (t === "input" && (e.type === "text" || e.type === "search" || e.type === "tel" || e.type === "url" || e.type === "password") || t === "textarea" || e.contentEditable === "true");
}
function iv(e) {
  var t = Wp(), n = e.focusedElem, r = e.selectionRange;
  if (t !== n && n && n.ownerDocument && Bp(n.ownerDocument.documentElement, n)) {
    if (r !== null && gu(n)) {
      if (t = r.start, e = r.end, e === void 0 && (e = t), "selectionStart" in n)
        n.selectionStart = t, n.selectionEnd = Math.min(e, n.value.length);
      else if (e = (t = n.ownerDocument || document) && t.defaultView || window, e.getSelection) {
        e = e.getSelection();
        var o = n.textContent.length, i = Math.min(r.start, o);
        r = r.end === void 0 ? i : Math.min(r.end, o), !e.extend && i > r && (o = r, r = i, i = o), o = ed(n, i);
        var l = ed(
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
var lv = Wt && "documentMode" in document && 11 >= document.documentMode, Gn = null, ga = null, eo = null, va = !1;
function td(e, t, n) {
  var r = n.window === n ? n.document : n.nodeType === 9 ? n : n.ownerDocument;
  va || Gn == null || Gn !== Oi(r) || (r = Gn, "selectionStart" in r && gu(r) ? r = { start: r.selectionStart, end: r.selectionEnd } : (r = (r.ownerDocument && r.ownerDocument.defaultView || window).getSelection(), r = { anchorNode: r.anchorNode, anchorOffset: r.anchorOffset, focusNode: r.focusNode, focusOffset: r.focusOffset }), eo && mo(eo, r) || (eo = r, r = Li(ga, "onSelect"), 0 < r.length && (t = new pu("onSelect", "select", null, t, n), e.push({ event: t, listeners: r }), t.target = Gn)));
}
function ei(e, t) {
  var n = {};
  return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit" + e] = "webkit" + t, n["Moz" + e] = "moz" + t, n;
}
var Qn = { animationend: ei("Animation", "AnimationEnd"), animationiteration: ei("Animation", "AnimationIteration"), animationstart: ei("Animation", "AnimationStart"), transitionend: ei("Transition", "TransitionEnd") }, _s = {}, Up = {};
Wt && (Up = document.createElement("div").style, "AnimationEvent" in window || (delete Qn.animationend.animation, delete Qn.animationiteration.animation, delete Qn.animationstart.animation), "TransitionEvent" in window || delete Qn.transitionend.transition);
function ml(e) {
  if (_s[e])
    return _s[e];
  if (!Qn[e])
    return e;
  var t = Qn[e], n;
  for (n in t)
    if (t.hasOwnProperty(n) && n in Up)
      return _s[e] = t[n];
  return e;
}
var Vp = ml("animationend"), Hp = ml("animationiteration"), Kp = ml("animationstart"), Gp = ml("transitionend"), Qp = /* @__PURE__ */ new Map(), nd = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
function hn(e, t) {
  Qp.set(e, t), Nn(t, [e]);
}
for (var $s = 0; $s < nd.length; $s++) {
  var Es = nd[$s], sv = Es.toLowerCase(), av = Es[0].toUpperCase() + Es.slice(1);
  hn(sv, "on" + av);
}
hn(Vp, "onAnimationEnd");
hn(Hp, "onAnimationIteration");
hn(Kp, "onAnimationStart");
hn("dblclick", "onDoubleClick");
hn("focusin", "onFocus");
hn("focusout", "onBlur");
hn(Gp, "onTransitionEnd");
dr("onMouseEnter", ["mouseout", "mouseover"]);
dr("onMouseLeave", ["mouseout", "mouseover"]);
dr("onPointerEnter", ["pointerout", "pointerover"]);
dr("onPointerLeave", ["pointerout", "pointerover"]);
Nn("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" "));
Nn("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));
Nn("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]);
Nn("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" "));
Nn("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" "));
Nn("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
var Qr = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), uv = new Set("cancel close invalid load scroll toggle".split(" ").concat(Qr));
function rd(e, t, n) {
  var r = e.type || "unknown-event";
  e.currentTarget = n, sg(r, t, void 0, e), e.currentTarget = null;
}
function Yp(e, t) {
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
          rd(o, s, u), i = a;
        }
      else
        for (l = 0; l < r.length; l++) {
          if (s = r[l], a = s.instance, u = s.currentTarget, s = s.listener, a !== i && o.isPropagationStopped())
            break e;
          rd(o, s, u), i = a;
        }
    }
  }
  if (zi)
    throw e = fa, zi = !1, fa = null, e;
}
function J(e, t) {
  var n = t[Ca];
  n === void 0 && (n = t[Ca] = /* @__PURE__ */ new Set());
  var r = e + "__bubble";
  n.has(r) || (Xp(t, e, 2, !1), n.add(r));
}
function Ps(e, t, n) {
  var r = 0;
  t && (r |= 4), Xp(n, e, r, t);
}
var ti = "_reactListening" + Math.random().toString(36).slice(2);
function ho(e) {
  if (!e[ti]) {
    e[ti] = !0, rp.forEach(function(n) {
      n !== "selectionchange" && (uv.has(n) || Ps(n, !1, e), Ps(n, !0, e));
    });
    var t = e.nodeType === 9 ? e : e.ownerDocument;
    t === null || t[ti] || (t[ti] = !0, Ps("selectionchange", !1, t));
  }
}
function Xp(e, t, n, r) {
  switch (zp(t)) {
    case 1:
      var o = kg;
      break;
    case 4:
      o = _g;
      break;
    default:
      o = du;
  }
  n = o.bind(null, t, n, e), o = void 0, !da || t !== "touchstart" && t !== "touchmove" && t !== "wheel" || (o = !0), r ? o !== void 0 ? e.addEventListener(t, n, { capture: !0, passive: o }) : e.addEventListener(t, n, !0) : o !== void 0 ? e.addEventListener(t, n, { passive: o }) : e.addEventListener(t, n, !1);
}
function Ts(e, t, n, r, o) {
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
  xp(function() {
    var u = i, c = su(n), d = [];
    e: {
      var p = Qp.get(e);
      if (p !== void 0) {
        var v = pu, x = e;
        switch (e) {
          case "keypress":
            if (vi(n) === 0)
              break e;
          case "keydown":
          case "keyup":
            v = Dg;
            break;
          case "focusin":
            x = "focus", v = ws;
            break;
          case "focusout":
            x = "blur", v = ws;
            break;
          case "beforeblur":
          case "afterblur":
            v = ws;
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
            v = Hc;
            break;
          case "drag":
          case "dragend":
          case "dragenter":
          case "dragexit":
          case "dragleave":
          case "dragover":
          case "dragstart":
          case "drop":
            v = Pg;
            break;
          case "touchcancel":
          case "touchend":
          case "touchmove":
          case "touchstart":
            v = Wg;
            break;
          case Vp:
          case Hp:
          case Kp:
            v = Mg;
            break;
          case Gp:
            v = Vg;
            break;
          case "scroll":
            v = $g;
            break;
          case "wheel":
            v = Kg;
            break;
          case "copy":
          case "cut":
          case "paste":
            v = jg;
            break;
          case "gotpointercapture":
          case "lostpointercapture":
          case "pointercancel":
          case "pointerdown":
          case "pointermove":
          case "pointerout":
          case "pointerover":
          case "pointerup":
            v = Gc;
        }
        var g = (t & 4) !== 0, E = !g && e === "scroll", m = g ? p !== null ? p + "Capture" : null : p;
        g = [];
        for (var f = u, h; f !== null; ) {
          h = f;
          var S = h.stateNode;
          if (h.tag === 5 && S !== null && (h = S, m !== null && (S = ao(f, m), S != null && g.push(go(f, S, h)))), E)
            break;
          f = f.return;
        }
        0 < g.length && (p = new v(p, x, null, n, c), d.push({ event: p, listeners: g }));
      }
    }
    if (!(t & 7)) {
      e: {
        if (p = e === "mouseover" || e === "pointerover", v = e === "mouseout" || e === "pointerout", p && n !== ua && (x = n.relatedTarget || n.fromElement) && (Cn(x) || x[Ut]))
          break e;
        if ((v || p) && (p = c.window === c ? c : (p = c.ownerDocument) ? p.defaultView || p.parentWindow : window, v ? (x = n.relatedTarget || n.toElement, v = u, x = x ? Cn(x) : null, x !== null && (E = bn(x), x !== E || x.tag !== 5 && x.tag !== 6) && (x = null)) : (v = null, x = u), v !== x)) {
          if (g = Hc, S = "onMouseLeave", m = "onMouseEnter", f = "mouse", (e === "pointerout" || e === "pointerover") && (g = Gc, S = "onPointerLeave", m = "onPointerEnter", f = "pointer"), E = v == null ? p : Yn(v), h = x == null ? p : Yn(x), p = new g(S, f + "leave", v, n, c), p.target = E, p.relatedTarget = h, S = null, Cn(c) === u && (g = new g(m, f + "enter", x, n, c), g.target = h, g.relatedTarget = E, S = g), E = S, v && x)
            t: {
              for (g = v, m = x, f = 0, h = g; h; h = Ln(h))
                f++;
              for (h = 0, S = m; S; S = Ln(S))
                h++;
              for (; 0 < f - h; )
                g = Ln(g), f--;
              for (; 0 < h - f; )
                m = Ln(m), h--;
              for (; f--; ) {
                if (g === m || m !== null && g === m.alternate)
                  break t;
                g = Ln(g), m = Ln(m);
              }
              g = null;
            }
          else
            g = null;
          v !== null && od(d, p, v, g, !1), x !== null && E !== null && od(d, E, x, g, !0);
        }
      }
      e: {
        if (p = u ? Yn(u) : window, v = p.nodeName && p.nodeName.toLowerCase(), v === "select" || v === "input" && p.type === "file")
          var $ = Jg;
        else if (Xc(p))
          if (Dp)
            $ = rv;
          else {
            $ = tv;
            var k = ev;
          }
        else
          (v = p.nodeName) && v.toLowerCase() === "input" && (p.type === "checkbox" || p.type === "radio") && ($ = nv);
        if ($ && ($ = $(e, u))) {
          Lp(d, $, n, c);
          break e;
        }
        k && k(e, p, u), e === "focusout" && (k = p._wrapperState) && k.controlled && p.type === "number" && oa(p, "number", p.value);
      }
      switch (k = u ? Yn(u) : window, e) {
        case "focusin":
          (Xc(k) || k.contentEditable === "true") && (Gn = k, ga = u, eo = null);
          break;
        case "focusout":
          eo = ga = Gn = null;
          break;
        case "mousedown":
          va = !0;
          break;
        case "contextmenu":
        case "mouseup":
        case "dragend":
          va = !1, td(d, n, c);
          break;
        case "selectionchange":
          if (lv)
            break;
        case "keydown":
        case "keyup":
          td(d, n, c);
      }
      var C;
      if (hu)
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
        Kn ? Ip(e, n) && (T = "onCompositionEnd") : e === "keydown" && n.keyCode === 229 && (T = "onCompositionStart");
      T && (bp && n.locale !== "ko" && (Kn || T !== "onCompositionStart" ? T === "onCompositionEnd" && Kn && (C = Np()) : (nn = c, fu = "value" in nn ? nn.value : nn.textContent, Kn = !0)), k = Li(u, T), 0 < k.length && (T = new Kc(T, e, null, n, c), d.push({ event: T, listeners: k }), C ? T.data = C : (C = Ap(n), C !== null && (T.data = C)))), (C = Qg ? Yg(e, n) : Xg(e, n)) && (u = Li(u, "onBeforeInput"), 0 < u.length && (c = new Kc("onBeforeInput", "beforeinput", null, n, c), d.push({ event: c, listeners: u }), c.data = C));
    }
    Yp(d, t);
  });
}
function go(e, t, n) {
  return { instance: e, listener: t, currentTarget: n };
}
function Li(e, t) {
  for (var n = t + "Capture", r = []; e !== null; ) {
    var o = e, i = o.stateNode;
    o.tag === 5 && i !== null && (o = i, i = ao(e, n), i != null && r.unshift(go(e, i, o)), i = ao(e, t), i != null && r.push(go(e, i, o))), e = e.return;
  }
  return r;
}
function Ln(e) {
  if (e === null)
    return null;
  do
    e = e.return;
  while (e && e.tag !== 5);
  return e || null;
}
function od(e, t, n, r, o) {
  for (var i = t._reactName, l = []; n !== null && n !== r; ) {
    var s = n, a = s.alternate, u = s.stateNode;
    if (a !== null && a === r)
      break;
    s.tag === 5 && u !== null && (s = u, o ? (a = ao(n, i), a != null && l.unshift(go(n, a, s))) : o || (a = ao(n, i), a != null && l.push(go(n, a, s)))), n = n.return;
  }
  l.length !== 0 && e.push({ event: t, listeners: l });
}
var cv = /\r\n?/g, dv = /\u0000|\uFFFD/g;
function id(e) {
  return (typeof e == "string" ? e : "" + e).replace(cv, `
`).replace(dv, "");
}
function ni(e, t, n) {
  if (t = id(t), id(e) !== t && n)
    throw Error(P(425));
}
function Di() {
}
var ya = null, xa = null;
function Sa(e, t) {
  return e === "textarea" || e === "noscript" || typeof t.children == "string" || typeof t.children == "number" || typeof t.dangerouslySetInnerHTML == "object" && t.dangerouslySetInnerHTML !== null && t.dangerouslySetInnerHTML.__html != null;
}
var wa = typeof setTimeout == "function" ? setTimeout : void 0, fv = typeof clearTimeout == "function" ? clearTimeout : void 0, ld = typeof Promise == "function" ? Promise : void 0, pv = typeof queueMicrotask == "function" ? queueMicrotask : typeof ld < "u" ? function(e) {
  return ld.resolve(null).then(e).catch(mv);
} : wa;
function mv(e) {
  setTimeout(function() {
    throw e;
  });
}
function Rs(e, t) {
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
function sd(e) {
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
var _r = Math.random().toString(36).slice(2), Mt = "__reactFiber$" + _r, vo = "__reactProps$" + _r, Ut = "__reactContainer$" + _r, Ca = "__reactEvents$" + _r, hv = "__reactListeners$" + _r, gv = "__reactHandles$" + _r;
function Cn(e) {
  var t = e[Mt];
  if (t)
    return t;
  for (var n = e.parentNode; n; ) {
    if (t = n[Ut] || n[Mt]) {
      if (n = t.alternate, t.child !== null || n !== null && n.child !== null)
        for (e = sd(e); e !== null; ) {
          if (n = e[Mt])
            return n;
          e = sd(e);
        }
      return t;
    }
    e = n, n = e.parentNode;
  }
  return null;
}
function No(e) {
  return e = e[Mt] || e[Ut], !e || e.tag !== 5 && e.tag !== 6 && e.tag !== 13 && e.tag !== 3 ? null : e;
}
function Yn(e) {
  if (e.tag === 5 || e.tag === 6)
    return e.stateNode;
  throw Error(P(33));
}
function hl(e) {
  return e[vo] || null;
}
var ka = [], Xn = -1;
function gn(e) {
  return { current: e };
}
function ee(e) {
  0 > Xn || (e.current = ka[Xn], ka[Xn] = null, Xn--);
}
function q(e, t) {
  Xn++, ka[Xn] = e.current, e.current = t;
}
var mn = {}, be = gn(mn), Ue = gn(!1), Tn = mn;
function fr(e, t) {
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
function Fi() {
  ee(Ue), ee(be);
}
function ad(e, t, n) {
  if (be.current !== mn)
    throw Error(P(168));
  q(be, t), q(Ue, n);
}
function qp(e, t, n) {
  var r = e.stateNode;
  if (t = t.childContextTypes, typeof r.getChildContext != "function")
    return n;
  r = r.getChildContext();
  for (var o in r)
    if (!(o in t))
      throw Error(P(108, eg(e) || "Unknown", o));
  return le({}, n, r);
}
function Bi(e) {
  return e = (e = e.stateNode) && e.__reactInternalMemoizedMergedChildContext || mn, Tn = be.current, q(be, e), q(Ue, Ue.current), !0;
}
function ud(e, t, n) {
  var r = e.stateNode;
  if (!r)
    throw Error(P(169));
  n ? (e = qp(e, t, Tn), r.__reactInternalMemoizedMergedChildContext = e, ee(Ue), ee(be), q(be, e)) : ee(Ue), q(Ue, n);
}
var At = null, gl = !1, Ms = !1;
function Zp(e) {
  At === null ? At = [e] : At.push(e);
}
function vv(e) {
  gl = !0, Zp(e);
}
function vn() {
  if (!Ms && At !== null) {
    Ms = !0;
    var e = 0, t = G;
    try {
      var n = At;
      for (G = 1; e < n.length; e++) {
        var r = n[e];
        do
          r = r(!0);
        while (r !== null);
      }
      At = null, gl = !1;
    } catch (o) {
      throw At !== null && (At = At.slice(e + 1)), kp(au, vn), o;
    } finally {
      G = t, Ms = !1;
    }
  }
  return null;
}
var qn = [], Zn = 0, Wi = null, Ui = 0, lt = [], st = 0, Rn = null, Dt = 1, Ft = "";
function xn(e, t) {
  qn[Zn++] = Ui, qn[Zn++] = Wi, Wi = e, Ui = t;
}
function Jp(e, t, n) {
  lt[st++] = Dt, lt[st++] = Ft, lt[st++] = Rn, Rn = e;
  var r = Dt;
  e = Ft;
  var o = 32 - kt(r) - 1;
  r &= ~(1 << o), n += 1;
  var i = 32 - kt(t) + o;
  if (30 < i) {
    var l = o - o % 5;
    i = (r & (1 << l) - 1).toString(32), r >>= l, o -= l, Dt = 1 << 32 - kt(t) + o | n << o | r, Ft = i + e;
  } else
    Dt = 1 << i | n << o | r, Ft = e;
}
function vu(e) {
  e.return !== null && (xn(e, 1), Jp(e, 1, 0));
}
function yu(e) {
  for (; e === Wi; )
    Wi = qn[--Zn], qn[Zn] = null, Ui = qn[--Zn], qn[Zn] = null;
  for (; e === Rn; )
    Rn = lt[--st], lt[st] = null, Ft = lt[--st], lt[st] = null, Dt = lt[--st], lt[st] = null;
}
var Ze = null, qe = null, ne = !1, Ct = null;
function em(e, t) {
  var n = ut(5, null, null, 0);
  n.elementType = "DELETED", n.stateNode = t, n.return = e, t = e.deletions, t === null ? (e.deletions = [n], e.flags |= 16) : t.push(n);
}
function cd(e, t) {
  switch (e.tag) {
    case 5:
      var n = e.type;
      return t = t.nodeType !== 1 || n.toLowerCase() !== t.nodeName.toLowerCase() ? null : t, t !== null ? (e.stateNode = t, Ze = e, qe = an(t.firstChild), !0) : !1;
    case 6:
      return t = e.pendingProps === "" || t.nodeType !== 3 ? null : t, t !== null ? (e.stateNode = t, Ze = e, qe = null, !0) : !1;
    case 13:
      return t = t.nodeType !== 8 ? null : t, t !== null ? (n = Rn !== null ? { id: Dt, overflow: Ft } : null, e.memoizedState = { dehydrated: t, treeContext: n, retryLane: 1073741824 }, n = ut(18, null, null, 0), n.stateNode = t, n.return = e, e.child = n, Ze = e, qe = null, !0) : !1;
    default:
      return !1;
  }
}
function _a(e) {
  return (e.mode & 1) !== 0 && (e.flags & 128) === 0;
}
function $a(e) {
  if (ne) {
    var t = qe;
    if (t) {
      var n = t;
      if (!cd(e, t)) {
        if (_a(e))
          throw Error(P(418));
        t = an(n.nextSibling);
        var r = Ze;
        t && cd(e, t) ? em(r, n) : (e.flags = e.flags & -4097 | 2, ne = !1, Ze = e);
      }
    } else {
      if (_a(e))
        throw Error(P(418));
      e.flags = e.flags & -4097 | 2, ne = !1, Ze = e;
    }
  }
}
function dd(e) {
  for (e = e.return; e !== null && e.tag !== 5 && e.tag !== 3 && e.tag !== 13; )
    e = e.return;
  Ze = e;
}
function ri(e) {
  if (e !== Ze)
    return !1;
  if (!ne)
    return dd(e), ne = !0, !1;
  var t;
  if ((t = e.tag !== 3) && !(t = e.tag !== 5) && (t = e.type, t = t !== "head" && t !== "body" && !Sa(e.type, e.memoizedProps)), t && (t = qe)) {
    if (_a(e))
      throw tm(), Error(P(418));
    for (; t; )
      em(e, t), t = an(t.nextSibling);
  }
  if (dd(e), e.tag === 13) {
    if (e = e.memoizedState, e = e !== null ? e.dehydrated : null, !e)
      throw Error(P(317));
    e: {
      for (e = e.nextSibling, t = 0; e; ) {
        if (e.nodeType === 8) {
          var n = e.data;
          if (n === "/$") {
            if (t === 0) {
              qe = an(e.nextSibling);
              break e;
            }
            t--;
          } else
            n !== "$" && n !== "$!" && n !== "$?" || t++;
        }
        e = e.nextSibling;
      }
      qe = null;
    }
  } else
    qe = Ze ? an(e.stateNode.nextSibling) : null;
  return !0;
}
function tm() {
  for (var e = qe; e; )
    e = an(e.nextSibling);
}
function pr() {
  qe = Ze = null, ne = !1;
}
function xu(e) {
  Ct === null ? Ct = [e] : Ct.push(e);
}
var yv = Gt.ReactCurrentBatchConfig;
function Lr(e, t, n) {
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
function oi(e, t) {
  throw e = Object.prototype.toString.call(t), Error(P(31, e === "[object Object]" ? "object with keys {" + Object.keys(t).join(", ") + "}" : e));
}
function fd(e) {
  var t = e._init;
  return t(e._payload);
}
function nm(e) {
  function t(m, f) {
    if (e) {
      var h = m.deletions;
      h === null ? (m.deletions = [f], m.flags |= 16) : h.push(f);
    }
  }
  function n(m, f) {
    if (!e)
      return null;
    for (; f !== null; )
      t(m, f), f = f.sibling;
    return null;
  }
  function r(m, f) {
    for (m = /* @__PURE__ */ new Map(); f !== null; )
      f.key !== null ? m.set(f.key, f) : m.set(f.index, f), f = f.sibling;
    return m;
  }
  function o(m, f) {
    return m = fn(m, f), m.index = 0, m.sibling = null, m;
  }
  function i(m, f, h) {
    return m.index = h, e ? (h = m.alternate, h !== null ? (h = h.index, h < f ? (m.flags |= 2, f) : h) : (m.flags |= 2, f)) : (m.flags |= 1048576, f);
  }
  function l(m) {
    return e && m.alternate === null && (m.flags |= 2), m;
  }
  function s(m, f, h, S) {
    return f === null || f.tag !== 6 ? (f = As(h, m.mode, S), f.return = m, f) : (f = o(f, h), f.return = m, f);
  }
  function a(m, f, h, S) {
    var $ = h.type;
    return $ === Hn ? c(m, f, h.props.children, S, h.key) : f !== null && (f.elementType === $ || typeof $ == "object" && $ !== null && $.$$typeof === Zt && fd($) === f.type) ? (S = o(f, h.props), S.ref = Lr(m, f, h), S.return = m, S) : (S = _i(h.type, h.key, h.props, null, m.mode, S), S.ref = Lr(m, f, h), S.return = m, S);
  }
  function u(m, f, h, S) {
    return f === null || f.tag !== 4 || f.stateNode.containerInfo !== h.containerInfo || f.stateNode.implementation !== h.implementation ? (f = Ls(h, m.mode, S), f.return = m, f) : (f = o(f, h.children || []), f.return = m, f);
  }
  function c(m, f, h, S, $) {
    return f === null || f.tag !== 7 ? (f = Pn(h, m.mode, S, $), f.return = m, f) : (f = o(f, h), f.return = m, f);
  }
  function d(m, f, h) {
    if (typeof f == "string" && f !== "" || typeof f == "number")
      return f = As("" + f, m.mode, h), f.return = m, f;
    if (typeof f == "object" && f !== null) {
      switch (f.$$typeof) {
        case Go:
          return h = _i(f.type, f.key, f.props, null, m.mode, h), h.ref = Lr(m, null, f), h.return = m, h;
        case Vn:
          return f = Ls(f, m.mode, h), f.return = m, f;
        case Zt:
          var S = f._init;
          return d(m, S(f._payload), h);
      }
      if (Kr(f) || zr(f))
        return f = Pn(f, m.mode, h, null), f.return = m, f;
      oi(m, f);
    }
    return null;
  }
  function p(m, f, h, S) {
    var $ = f !== null ? f.key : null;
    if (typeof h == "string" && h !== "" || typeof h == "number")
      return $ !== null ? null : s(m, f, "" + h, S);
    if (typeof h == "object" && h !== null) {
      switch (h.$$typeof) {
        case Go:
          return h.key === $ ? a(m, f, h, S) : null;
        case Vn:
          return h.key === $ ? u(m, f, h, S) : null;
        case Zt:
          return $ = h._init, p(
            m,
            f,
            $(h._payload),
            S
          );
      }
      if (Kr(h) || zr(h))
        return $ !== null ? null : c(m, f, h, S, null);
      oi(m, h);
    }
    return null;
  }
  function v(m, f, h, S, $) {
    if (typeof S == "string" && S !== "" || typeof S == "number")
      return m = m.get(h) || null, s(f, m, "" + S, $);
    if (typeof S == "object" && S !== null) {
      switch (S.$$typeof) {
        case Go:
          return m = m.get(S.key === null ? h : S.key) || null, a(f, m, S, $);
        case Vn:
          return m = m.get(S.key === null ? h : S.key) || null, u(f, m, S, $);
        case Zt:
          var k = S._init;
          return v(m, f, h, k(S._payload), $);
      }
      if (Kr(S) || zr(S))
        return m = m.get(h) || null, c(f, m, S, $, null);
      oi(f, S);
    }
    return null;
  }
  function x(m, f, h, S) {
    for (var $ = null, k = null, C = f, T = f = 0, j = null; C !== null && T < h.length; T++) {
      C.index > T ? (j = C, C = null) : j = C.sibling;
      var M = p(m, C, h[T], S);
      if (M === null) {
        C === null && (C = j);
        break;
      }
      e && C && M.alternate === null && t(m, C), f = i(M, f, T), k === null ? $ = M : k.sibling = M, k = M, C = j;
    }
    if (T === h.length)
      return n(m, C), ne && xn(m, T), $;
    if (C === null) {
      for (; T < h.length; T++)
        C = d(m, h[T], S), C !== null && (f = i(C, f, T), k === null ? $ = C : k.sibling = C, k = C);
      return ne && xn(m, T), $;
    }
    for (C = r(m, C); T < h.length; T++)
      j = v(C, m, T, h[T], S), j !== null && (e && j.alternate !== null && C.delete(j.key === null ? T : j.key), f = i(j, f, T), k === null ? $ = j : k.sibling = j, k = j);
    return e && C.forEach(function(U) {
      return t(m, U);
    }), ne && xn(m, T), $;
  }
  function g(m, f, h, S) {
    var $ = zr(h);
    if (typeof $ != "function")
      throw Error(P(150));
    if (h = $.call(h), h == null)
      throw Error(P(151));
    for (var k = $ = null, C = f, T = f = 0, j = null, M = h.next(); C !== null && !M.done; T++, M = h.next()) {
      C.index > T ? (j = C, C = null) : j = C.sibling;
      var U = p(m, C, M.value, S);
      if (U === null) {
        C === null && (C = j);
        break;
      }
      e && C && U.alternate === null && t(m, C), f = i(U, f, T), k === null ? $ = U : k.sibling = U, k = U, C = j;
    }
    if (M.done)
      return n(
        m,
        C
      ), ne && xn(m, T), $;
    if (C === null) {
      for (; !M.done; T++, M = h.next())
        M = d(m, M.value, S), M !== null && (f = i(M, f, T), k === null ? $ = M : k.sibling = M, k = M);
      return ne && xn(m, T), $;
    }
    for (C = r(m, C); !M.done; T++, M = h.next())
      M = v(C, m, T, M.value, S), M !== null && (e && M.alternate !== null && C.delete(M.key === null ? T : M.key), f = i(M, f, T), k === null ? $ = M : k.sibling = M, k = M);
    return e && C.forEach(function(F) {
      return t(m, F);
    }), ne && xn(m, T), $;
  }
  function E(m, f, h, S) {
    if (typeof h == "object" && h !== null && h.type === Hn && h.key === null && (h = h.props.children), typeof h == "object" && h !== null) {
      switch (h.$$typeof) {
        case Go:
          e: {
            for (var $ = h.key, k = f; k !== null; ) {
              if (k.key === $) {
                if ($ = h.type, $ === Hn) {
                  if (k.tag === 7) {
                    n(m, k.sibling), f = o(k, h.props.children), f.return = m, m = f;
                    break e;
                  }
                } else if (k.elementType === $ || typeof $ == "object" && $ !== null && $.$$typeof === Zt && fd($) === k.type) {
                  n(m, k.sibling), f = o(k, h.props), f.ref = Lr(m, k, h), f.return = m, m = f;
                  break e;
                }
                n(m, k);
                break;
              } else
                t(m, k);
              k = k.sibling;
            }
            h.type === Hn ? (f = Pn(h.props.children, m.mode, S, h.key), f.return = m, m = f) : (S = _i(h.type, h.key, h.props, null, m.mode, S), S.ref = Lr(m, f, h), S.return = m, m = S);
          }
          return l(m);
        case Vn:
          e: {
            for (k = h.key; f !== null; ) {
              if (f.key === k)
                if (f.tag === 4 && f.stateNode.containerInfo === h.containerInfo && f.stateNode.implementation === h.implementation) {
                  n(m, f.sibling), f = o(f, h.children || []), f.return = m, m = f;
                  break e;
                } else {
                  n(m, f);
                  break;
                }
              else
                t(m, f);
              f = f.sibling;
            }
            f = Ls(h, m.mode, S), f.return = m, m = f;
          }
          return l(m);
        case Zt:
          return k = h._init, E(m, f, k(h._payload), S);
      }
      if (Kr(h))
        return x(m, f, h, S);
      if (zr(h))
        return g(m, f, h, S);
      oi(m, h);
    }
    return typeof h == "string" && h !== "" || typeof h == "number" ? (h = "" + h, f !== null && f.tag === 6 ? (n(m, f.sibling), f = o(f, h), f.return = m, m = f) : (n(m, f), f = As(h, m.mode, S), f.return = m, m = f), l(m)) : n(m, f);
  }
  return E;
}
var mr = nm(!0), rm = nm(!1), Vi = gn(null), Hi = null, Jn = null, Su = null;
function wu() {
  Su = Jn = Hi = null;
}
function Cu(e) {
  var t = Vi.current;
  ee(Vi), e._currentValue = t;
}
function Ea(e, t, n) {
  for (; e !== null; ) {
    var r = e.alternate;
    if ((e.childLanes & t) !== t ? (e.childLanes |= t, r !== null && (r.childLanes |= t)) : r !== null && (r.childLanes & t) !== t && (r.childLanes |= t), e === n)
      break;
    e = e.return;
  }
}
function lr(e, t) {
  Hi = e, Su = Jn = null, e = e.dependencies, e !== null && e.firstContext !== null && (e.lanes & t && (We = !0), e.firstContext = null);
}
function ft(e) {
  var t = e._currentValue;
  if (Su !== e)
    if (e = { context: e, memoizedValue: t, next: null }, Jn === null) {
      if (Hi === null)
        throw Error(P(308));
      Jn = e, Hi.dependencies = { lanes: 0, firstContext: e };
    } else
      Jn = Jn.next = e;
  return t;
}
var kn = null;
function ku(e) {
  kn === null ? kn = [e] : kn.push(e);
}
function om(e, t, n, r) {
  var o = t.interleaved;
  return o === null ? (n.next = n, ku(t)) : (n.next = o.next, o.next = n), t.interleaved = n, Vt(e, r);
}
function Vt(e, t) {
  e.lanes |= t;
  var n = e.alternate;
  for (n !== null && (n.lanes |= t), n = e, e = e.return; e !== null; )
    e.childLanes |= t, n = e.alternate, n !== null && (n.childLanes |= t), n = e, e = e.return;
  return n.tag === 3 ? n.stateNode : null;
}
var Jt = !1;
function _u(e) {
  e.updateQueue = { baseState: e.memoizedState, firstBaseUpdate: null, lastBaseUpdate: null, shared: { pending: null, interleaved: null, lanes: 0 }, effects: null };
}
function im(e, t) {
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
  return o = r.interleaved, o === null ? (t.next = t, ku(r)) : (t.next = o.next, o.next = t), r.interleaved = t, Vt(e, n);
}
function yi(e, t, n) {
  if (t = t.updateQueue, t !== null && (t = t.shared, (n & 4194240) !== 0)) {
    var r = t.lanes;
    r &= e.pendingLanes, n |= r, t.lanes = n, uu(e, n);
  }
}
function pd(e, t) {
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
function Ki(e, t, n, r) {
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
    var d = o.baseState;
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
          var x = e, g = s;
          switch (p = t, v = n, g.tag) {
            case 1:
              if (x = g.payload, typeof x == "function") {
                d = x.call(v, d, p);
                break e;
              }
              d = x;
              break e;
            case 3:
              x.flags = x.flags & -65537 | 128;
            case 0:
              if (x = g.payload, p = typeof x == "function" ? x.call(v, d, p) : x, p == null)
                break e;
              d = le({}, d, p);
              break e;
            case 2:
              Jt = !0;
          }
        }
        s.callback !== null && s.lane !== 0 && (e.flags |= 64, p = o.effects, p === null ? o.effects = [s] : p.push(s));
      } else
        v = { eventTime: v, lane: p, tag: s.tag, payload: s.payload, callback: s.callback, next: null }, c === null ? (u = c = v, a = d) : c = c.next = v, l |= p;
      if (s = s.next, s === null) {
        if (s = o.shared.pending, s === null)
          break;
        p = s, s = p.next, p.next = null, o.lastBaseUpdate = p, o.shared.pending = null;
      }
    } while (1);
    if (c === null && (a = d), o.baseState = a, o.firstBaseUpdate = u, o.lastBaseUpdate = c, t = o.shared.interleaved, t !== null) {
      o = t;
      do
        l |= o.lane, o = o.next;
      while (o !== t);
    } else
      i === null && (o.shared.lanes = 0);
    On |= l, e.lanes = l, e.memoizedState = d;
  }
}
function md(e, t, n) {
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
var bo = {}, jt = gn(bo), yo = gn(bo), xo = gn(bo);
function _n(e) {
  if (e === bo)
    throw Error(P(174));
  return e;
}
function $u(e, t) {
  switch (q(xo, t), q(yo, e), q(jt, bo), e = t.nodeType, e) {
    case 9:
    case 11:
      t = (t = t.documentElement) ? t.namespaceURI : la(null, "");
      break;
    default:
      e = e === 8 ? t.parentNode : t, t = e.namespaceURI || null, e = e.tagName, t = la(t, e);
  }
  ee(jt), q(jt, t);
}
function hr() {
  ee(jt), ee(yo), ee(xo);
}
function lm(e) {
  _n(xo.current);
  var t = _n(jt.current), n = la(t, e.type);
  t !== n && (q(yo, e), q(jt, n));
}
function Eu(e) {
  yo.current === e && (ee(jt), ee(yo));
}
var oe = gn(0);
function Gi(e) {
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
var Os = [];
function Pu() {
  for (var e = 0; e < Os.length; e++)
    Os[e]._workInProgressVersionPrimary = null;
  Os.length = 0;
}
var xi = Gt.ReactCurrentDispatcher, js = Gt.ReactCurrentBatchConfig, Mn = 0, ie = null, Se = null, ke = null, Qi = !1, to = !1, So = 0, xv = 0;
function Oe() {
  throw Error(P(321));
}
function Tu(e, t) {
  if (t === null)
    return !1;
  for (var n = 0; n < t.length && n < e.length; n++)
    if (!$t(e[n], t[n]))
      return !1;
  return !0;
}
function Ru(e, t, n, r, o, i) {
  if (Mn = i, ie = t, t.memoizedState = null, t.updateQueue = null, t.lanes = 0, xi.current = e === null || e.memoizedState === null ? kv : _v, e = n(r, o), to) {
    i = 0;
    do {
      if (to = !1, So = 0, 25 <= i)
        throw Error(P(301));
      i += 1, ke = Se = null, t.updateQueue = null, xi.current = $v, e = n(r, o);
    } while (to);
  }
  if (xi.current = Yi, t = Se !== null && Se.next !== null, Mn = 0, ke = Se = ie = null, Qi = !1, t)
    throw Error(P(300));
  return e;
}
function Mu() {
  var e = So !== 0;
  return So = 0, e;
}
function Pt() {
  var e = { memoizedState: null, baseState: null, baseQueue: null, queue: null, next: null };
  return ke === null ? ie.memoizedState = ke = e : ke = ke.next = e, ke;
}
function pt() {
  if (Se === null) {
    var e = ie.alternate;
    e = e !== null ? e.memoizedState : null;
  } else
    e = Se.next;
  var t = ke === null ? ie.memoizedState : ke.next;
  if (t !== null)
    ke = t, Se = e;
  else {
    if (e === null)
      throw Error(P(310));
    Se = e, e = { memoizedState: Se.memoizedState, baseState: Se.baseState, baseQueue: Se.baseQueue, queue: Se.queue, next: null }, ke === null ? ie.memoizedState = ke = e : ke = ke.next = e;
  }
  return ke;
}
function wo(e, t) {
  return typeof t == "function" ? t(e) : t;
}
function zs(e) {
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
      if ((Mn & c) === c)
        a !== null && (a = a.next = { lane: 0, action: u.action, hasEagerState: u.hasEagerState, eagerState: u.eagerState, next: null }), r = u.hasEagerState ? u.eagerState : e(r, u.action);
      else {
        var d = {
          lane: c,
          action: u.action,
          hasEagerState: u.hasEagerState,
          eagerState: u.eagerState,
          next: null
        };
        a === null ? (s = a = d, l = r) : a = a.next = d, ie.lanes |= c, On |= c;
      }
      u = u.next;
    } while (u !== null && u !== i);
    a === null ? l = r : a.next = s, $t(r, t.memoizedState) || (We = !0), t.memoizedState = r, t.baseState = l, t.baseQueue = a, n.lastRenderedState = r;
  }
  if (e = n.interleaved, e !== null) {
    o = e;
    do
      i = o.lane, ie.lanes |= i, On |= i, o = o.next;
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
function sm() {
}
function am(e, t) {
  var n = ie, r = pt(), o = t(), i = !$t(r.memoizedState, o);
  if (i && (r.memoizedState = o, We = !0), r = r.queue, Ou(dm.bind(null, n, r, e), [e]), r.getSnapshot !== t || i || ke !== null && ke.memoizedState.tag & 1) {
    if (n.flags |= 2048, Co(9, cm.bind(null, n, r, o, t), void 0, null), _e === null)
      throw Error(P(349));
    Mn & 30 || um(n, t, o);
  }
  return o;
}
function um(e, t, n) {
  e.flags |= 16384, e = { getSnapshot: t, value: n }, t = ie.updateQueue, t === null ? (t = { lastEffect: null, stores: null }, ie.updateQueue = t, t.stores = [e]) : (n = t.stores, n === null ? t.stores = [e] : n.push(e));
}
function cm(e, t, n, r) {
  t.value = n, t.getSnapshot = r, fm(t) && pm(e);
}
function dm(e, t, n) {
  return n(function() {
    fm(t) && pm(e);
  });
}
function fm(e) {
  var t = e.getSnapshot;
  e = e.value;
  try {
    var n = t();
    return !$t(e, n);
  } catch {
    return !0;
  }
}
function pm(e) {
  var t = Vt(e, 1);
  t !== null && _t(t, e, 1, -1);
}
function hd(e) {
  var t = Pt();
  return typeof e == "function" && (e = e()), t.memoizedState = t.baseState = e, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: wo, lastRenderedState: e }, t.queue = e, e = e.dispatch = Cv.bind(null, ie, e), [t.memoizedState, e];
}
function Co(e, t, n, r) {
  return e = { tag: e, create: t, destroy: n, deps: r, next: null }, t = ie.updateQueue, t === null ? (t = { lastEffect: null, stores: null }, ie.updateQueue = t, t.lastEffect = e.next = e) : (n = t.lastEffect, n === null ? t.lastEffect = e.next = e : (r = n.next, n.next = e, e.next = r, t.lastEffect = e)), e;
}
function mm() {
  return pt().memoizedState;
}
function Si(e, t, n, r) {
  var o = Pt();
  ie.flags |= e, o.memoizedState = Co(1 | t, n, void 0, r === void 0 ? null : r);
}
function vl(e, t, n, r) {
  var o = pt();
  r = r === void 0 ? null : r;
  var i = void 0;
  if (Se !== null) {
    var l = Se.memoizedState;
    if (i = l.destroy, r !== null && Tu(r, l.deps)) {
      o.memoizedState = Co(t, n, i, r);
      return;
    }
  }
  ie.flags |= e, o.memoizedState = Co(1 | t, n, i, r);
}
function gd(e, t) {
  return Si(8390656, 8, e, t);
}
function Ou(e, t) {
  return vl(2048, 8, e, t);
}
function hm(e, t) {
  return vl(4, 2, e, t);
}
function gm(e, t) {
  return vl(4, 4, e, t);
}
function vm(e, t) {
  if (typeof t == "function")
    return e = e(), t(e), function() {
      t(null);
    };
  if (t != null)
    return e = e(), t.current = e, function() {
      t.current = null;
    };
}
function ym(e, t, n) {
  return n = n != null ? n.concat([e]) : null, vl(4, 4, vm.bind(null, t, e), n);
}
function ju() {
}
function xm(e, t) {
  var n = pt();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && Tu(t, r[1]) ? r[0] : (n.memoizedState = [e, t], e);
}
function Sm(e, t) {
  var n = pt();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && Tu(t, r[1]) ? r[0] : (e = e(), n.memoizedState = [e, t], e);
}
function wm(e, t, n) {
  return Mn & 21 ? ($t(n, t) || (n = Ep(), ie.lanes |= n, On |= n, e.baseState = !0), t) : (e.baseState && (e.baseState = !1, We = !0), e.memoizedState = n);
}
function Sv(e, t) {
  var n = G;
  G = n !== 0 && 4 > n ? n : 4, e(!0);
  var r = js.transition;
  js.transition = {};
  try {
    e(!1), t();
  } finally {
    G = n, js.transition = r;
  }
}
function Cm() {
  return pt().memoizedState;
}
function wv(e, t, n) {
  var r = dn(e);
  if (n = { lane: r, action: n, hasEagerState: !1, eagerState: null, next: null }, km(e))
    _m(t, n);
  else if (n = om(e, t, n, r), n !== null) {
    var o = Le();
    _t(n, e, r, o), $m(n, t, r);
  }
}
function Cv(e, t, n) {
  var r = dn(e), o = { lane: r, action: n, hasEagerState: !1, eagerState: null, next: null };
  if (km(e))
    _m(t, o);
  else {
    var i = e.alternate;
    if (e.lanes === 0 && (i === null || i.lanes === 0) && (i = t.lastRenderedReducer, i !== null))
      try {
        var l = t.lastRenderedState, s = i(l, n);
        if (o.hasEagerState = !0, o.eagerState = s, $t(s, l)) {
          var a = t.interleaved;
          a === null ? (o.next = o, ku(t)) : (o.next = a.next, a.next = o), t.interleaved = o;
          return;
        }
      } catch {
      } finally {
      }
    n = om(e, t, o, r), n !== null && (o = Le(), _t(n, e, r, o), $m(n, t, r));
  }
}
function km(e) {
  var t = e.alternate;
  return e === ie || t !== null && t === ie;
}
function _m(e, t) {
  to = Qi = !0;
  var n = e.pending;
  n === null ? t.next = t : (t.next = n.next, n.next = t), e.pending = t;
}
function $m(e, t, n) {
  if (n & 4194240) {
    var r = t.lanes;
    r &= e.pendingLanes, n |= r, t.lanes = n, uu(e, n);
  }
}
var Yi = { readContext: ft, useCallback: Oe, useContext: Oe, useEffect: Oe, useImperativeHandle: Oe, useInsertionEffect: Oe, useLayoutEffect: Oe, useMemo: Oe, useReducer: Oe, useRef: Oe, useState: Oe, useDebugValue: Oe, useDeferredValue: Oe, useTransition: Oe, useMutableSource: Oe, useSyncExternalStore: Oe, useId: Oe, unstable_isNewReconciler: !1 }, kv = { readContext: ft, useCallback: function(e, t) {
  return Pt().memoizedState = [e, t === void 0 ? null : t], e;
}, useContext: ft, useEffect: gd, useImperativeHandle: function(e, t, n) {
  return n = n != null ? n.concat([e]) : null, Si(
    4194308,
    4,
    vm.bind(null, t, e),
    n
  );
}, useLayoutEffect: function(e, t) {
  return Si(4194308, 4, e, t);
}, useInsertionEffect: function(e, t) {
  return Si(4, 2, e, t);
}, useMemo: function(e, t) {
  var n = Pt();
  return t = t === void 0 ? null : t, e = e(), n.memoizedState = [e, t], e;
}, useReducer: function(e, t, n) {
  var r = Pt();
  return t = n !== void 0 ? n(t) : t, r.memoizedState = r.baseState = t, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: e, lastRenderedState: t }, r.queue = e, e = e.dispatch = wv.bind(null, ie, e), [r.memoizedState, e];
}, useRef: function(e) {
  var t = Pt();
  return e = { current: e }, t.memoizedState = e;
}, useState: hd, useDebugValue: ju, useDeferredValue: function(e) {
  return Pt().memoizedState = e;
}, useTransition: function() {
  var e = hd(!1), t = e[0];
  return e = Sv.bind(null, e[1]), Pt().memoizedState = e, [t, e];
}, useMutableSource: function() {
}, useSyncExternalStore: function(e, t, n) {
  var r = ie, o = Pt();
  if (ne) {
    if (n === void 0)
      throw Error(P(407));
    n = n();
  } else {
    if (n = t(), _e === null)
      throw Error(P(349));
    Mn & 30 || um(r, t, n);
  }
  o.memoizedState = n;
  var i = { value: n, getSnapshot: t };
  return o.queue = i, gd(dm.bind(
    null,
    r,
    i,
    e
  ), [e]), r.flags |= 2048, Co(9, cm.bind(null, r, i, n, t), void 0, null), n;
}, useId: function() {
  var e = Pt(), t = _e.identifierPrefix;
  if (ne) {
    var n = Ft, r = Dt;
    n = (r & ~(1 << 32 - kt(r) - 1)).toString(32) + n, t = ":" + t + "R" + n, n = So++, 0 < n && (t += "H" + n.toString(32)), t += ":";
  } else
    n = xv++, t = ":" + t + "r" + n.toString(32) + ":";
  return e.memoizedState = t;
}, unstable_isNewReconciler: !1 }, _v = {
  readContext: ft,
  useCallback: xm,
  useContext: ft,
  useEffect: Ou,
  useImperativeHandle: ym,
  useInsertionEffect: hm,
  useLayoutEffect: gm,
  useMemo: Sm,
  useReducer: zs,
  useRef: mm,
  useState: function() {
    return zs(wo);
  },
  useDebugValue: ju,
  useDeferredValue: function(e) {
    var t = pt();
    return wm(t, Se.memoizedState, e);
  },
  useTransition: function() {
    var e = zs(wo)[0], t = pt().memoizedState;
    return [e, t];
  },
  useMutableSource: sm,
  useSyncExternalStore: am,
  useId: Cm,
  unstable_isNewReconciler: !1
}, $v = { readContext: ft, useCallback: xm, useContext: ft, useEffect: Ou, useImperativeHandle: ym, useInsertionEffect: hm, useLayoutEffect: gm, useMemo: Sm, useReducer: Ns, useRef: mm, useState: function() {
  return Ns(wo);
}, useDebugValue: ju, useDeferredValue: function(e) {
  var t = pt();
  return Se === null ? t.memoizedState = e : wm(t, Se.memoizedState, e);
}, useTransition: function() {
  var e = Ns(wo)[0], t = pt().memoizedState;
  return [e, t];
}, useMutableSource: sm, useSyncExternalStore: am, useId: Cm, unstable_isNewReconciler: !1 };
function St(e, t) {
  if (e && e.defaultProps) {
    t = le({}, t), e = e.defaultProps;
    for (var n in e)
      t[n] === void 0 && (t[n] = e[n]);
    return t;
  }
  return t;
}
function Pa(e, t, n, r) {
  t = e.memoizedState, n = n(r, t), n = n == null ? t : le({}, t, n), e.memoizedState = n, e.lanes === 0 && (e.updateQueue.baseState = n);
}
var yl = { isMounted: function(e) {
  return (e = e._reactInternals) ? bn(e) === e : !1;
}, enqueueSetState: function(e, t, n) {
  e = e._reactInternals;
  var r = Le(), o = dn(e), i = Bt(r, o);
  i.payload = t, n != null && (i.callback = n), t = un(e, i, o), t !== null && (_t(t, e, o, r), yi(t, e, o));
}, enqueueReplaceState: function(e, t, n) {
  e = e._reactInternals;
  var r = Le(), o = dn(e), i = Bt(r, o);
  i.tag = 1, i.payload = t, n != null && (i.callback = n), t = un(e, i, o), t !== null && (_t(t, e, o, r), yi(t, e, o));
}, enqueueForceUpdate: function(e, t) {
  e = e._reactInternals;
  var n = Le(), r = dn(e), o = Bt(n, r);
  o.tag = 2, t != null && (o.callback = t), t = un(e, o, r), t !== null && (_t(t, e, r, n), yi(t, e, r));
} };
function vd(e, t, n, r, o, i, l) {
  return e = e.stateNode, typeof e.shouldComponentUpdate == "function" ? e.shouldComponentUpdate(r, i, l) : t.prototype && t.prototype.isPureReactComponent ? !mo(n, r) || !mo(o, i) : !0;
}
function Em(e, t, n) {
  var r = !1, o = mn, i = t.contextType;
  return typeof i == "object" && i !== null ? i = ft(i) : (o = Ve(t) ? Tn : be.current, r = t.contextTypes, i = (r = r != null) ? fr(e, o) : mn), t = new t(n, i), e.memoizedState = t.state !== null && t.state !== void 0 ? t.state : null, t.updater = yl, e.stateNode = t, t._reactInternals = e, r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = o, e.__reactInternalMemoizedMaskedChildContext = i), t;
}
function yd(e, t, n, r) {
  e = t.state, typeof t.componentWillReceiveProps == "function" && t.componentWillReceiveProps(n, r), typeof t.UNSAFE_componentWillReceiveProps == "function" && t.UNSAFE_componentWillReceiveProps(n, r), t.state !== e && yl.enqueueReplaceState(t, t.state, null);
}
function Ta(e, t, n, r) {
  var o = e.stateNode;
  o.props = n, o.state = e.memoizedState, o.refs = {}, _u(e);
  var i = t.contextType;
  typeof i == "object" && i !== null ? o.context = ft(i) : (i = Ve(t) ? Tn : be.current, o.context = fr(e, i)), o.state = e.memoizedState, i = t.getDerivedStateFromProps, typeof i == "function" && (Pa(e, t, i, n), o.state = e.memoizedState), typeof t.getDerivedStateFromProps == "function" || typeof o.getSnapshotBeforeUpdate == "function" || typeof o.UNSAFE_componentWillMount != "function" && typeof o.componentWillMount != "function" || (t = o.state, typeof o.componentWillMount == "function" && o.componentWillMount(), typeof o.UNSAFE_componentWillMount == "function" && o.UNSAFE_componentWillMount(), t !== o.state && yl.enqueueReplaceState(o, o.state, null), Ki(e, n, o, r), o.state = e.memoizedState), typeof o.componentDidMount == "function" && (e.flags |= 4194308);
}
function gr(e, t) {
  try {
    var n = "", r = t;
    do
      n += J0(r), r = r.return;
    while (r);
    var o = n;
  } catch (i) {
    o = `
Error generating stack: ` + i.message + `
` + i.stack;
  }
  return { value: e, source: t, stack: o, digest: null };
}
function bs(e, t, n) {
  return { value: e, source: null, stack: n ?? null, digest: t ?? null };
}
function Ra(e, t) {
  try {
    console.error(t.value);
  } catch (n) {
    setTimeout(function() {
      throw n;
    });
  }
}
var Ev = typeof WeakMap == "function" ? WeakMap : Map;
function Pm(e, t, n) {
  n = Bt(-1, n), n.tag = 3, n.payload = { element: null };
  var r = t.value;
  return n.callback = function() {
    qi || (qi = !0, Da = r), Ra(e, t);
  }, n;
}
function Tm(e, t, n) {
  n = Bt(-1, n), n.tag = 3;
  var r = e.type.getDerivedStateFromError;
  if (typeof r == "function") {
    var o = t.value;
    n.payload = function() {
      return r(o);
    }, n.callback = function() {
      Ra(e, t);
    };
  }
  var i = e.stateNode;
  return i !== null && typeof i.componentDidCatch == "function" && (n.callback = function() {
    Ra(e, t), typeof r != "function" && (cn === null ? cn = /* @__PURE__ */ new Set([this]) : cn.add(this));
    var l = t.stack;
    this.componentDidCatch(t.value, { componentStack: l !== null ? l : "" });
  }), n;
}
function xd(e, t, n) {
  var r = e.pingCache;
  if (r === null) {
    r = e.pingCache = new Ev();
    var o = /* @__PURE__ */ new Set();
    r.set(t, o);
  } else
    o = r.get(t), o === void 0 && (o = /* @__PURE__ */ new Set(), r.set(t, o));
  o.has(n) || (o.add(n), e = Fv.bind(null, e, t, n), t.then(e, e));
}
function Sd(e) {
  do {
    var t;
    if ((t = e.tag === 13) && (t = e.memoizedState, t = t !== null ? t.dehydrated !== null : !0), t)
      return e;
    e = e.return;
  } while (e !== null);
  return null;
}
function wd(e, t, n, r, o) {
  return e.mode & 1 ? (e.flags |= 65536, e.lanes = o, e) : (e === t ? e.flags |= 65536 : (e.flags |= 128, n.flags |= 131072, n.flags &= -52805, n.tag === 1 && (n.alternate === null ? n.tag = 17 : (t = Bt(-1, 1), t.tag = 2, un(n, t, 1))), n.lanes |= 1), e);
}
var Pv = Gt.ReactCurrentOwner, We = !1;
function Ae(e, t, n, r) {
  t.child = e === null ? rm(t, null, n, r) : mr(t, e.child, n, r);
}
function Cd(e, t, n, r, o) {
  n = n.render;
  var i = t.ref;
  return lr(t, o), r = Ru(e, t, n, r, i, o), n = Mu(), e !== null && !We ? (t.updateQueue = e.updateQueue, t.flags &= -2053, e.lanes &= ~o, Ht(e, t, o)) : (ne && n && vu(t), t.flags |= 1, Ae(e, t, r, o), t.child);
}
function kd(e, t, n, r, o) {
  if (e === null) {
    var i = n.type;
    return typeof i == "function" && !Fu(i) && i.defaultProps === void 0 && n.compare === null && n.defaultProps === void 0 ? (t.tag = 15, t.type = i, Rm(e, t, i, r, o)) : (e = _i(n.type, null, r, t, t.mode, o), e.ref = t.ref, e.return = t, t.child = e);
  }
  if (i = e.child, !(e.lanes & o)) {
    var l = i.memoizedProps;
    if (n = n.compare, n = n !== null ? n : mo, n(l, r) && e.ref === t.ref)
      return Ht(e, t, o);
  }
  return t.flags |= 1, e = fn(i, r), e.ref = t.ref, e.return = t, t.child = e;
}
function Rm(e, t, n, r, o) {
  if (e !== null) {
    var i = e.memoizedProps;
    if (mo(i, r) && e.ref === t.ref)
      if (We = !1, t.pendingProps = r = i, (e.lanes & o) !== 0)
        e.flags & 131072 && (We = !0);
      else
        return t.lanes = e.lanes, Ht(e, t, o);
  }
  return Ma(e, t, n, r, o);
}
function Mm(e, t, n) {
  var r = t.pendingProps, o = r.children, i = e !== null ? e.memoizedState : null;
  if (r.mode === "hidden")
    if (!(t.mode & 1))
      t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, q(tr, Ye), Ye |= n;
    else {
      if (!(n & 1073741824))
        return e = i !== null ? i.baseLanes | n : n, t.lanes = t.childLanes = 1073741824, t.memoizedState = { baseLanes: e, cachePool: null, transitions: null }, t.updateQueue = null, q(tr, Ye), Ye |= e, null;
      t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, r = i !== null ? i.baseLanes : n, q(tr, Ye), Ye |= r;
    }
  else
    i !== null ? (r = i.baseLanes | n, t.memoizedState = null) : r = n, q(tr, Ye), Ye |= r;
  return Ae(e, t, o, n), t.child;
}
function Om(e, t) {
  var n = t.ref;
  (e === null && n !== null || e !== null && e.ref !== n) && (t.flags |= 512, t.flags |= 2097152);
}
function Ma(e, t, n, r, o) {
  var i = Ve(n) ? Tn : be.current;
  return i = fr(t, i), lr(t, o), n = Ru(e, t, n, r, i, o), r = Mu(), e !== null && !We ? (t.updateQueue = e.updateQueue, t.flags &= -2053, e.lanes &= ~o, Ht(e, t, o)) : (ne && r && vu(t), t.flags |= 1, Ae(e, t, n, o), t.child);
}
function _d(e, t, n, r, o) {
  if (Ve(n)) {
    var i = !0;
    Bi(t);
  } else
    i = !1;
  if (lr(t, o), t.stateNode === null)
    wi(e, t), Em(t, n, r), Ta(t, n, r, o), r = !0;
  else if (e === null) {
    var l = t.stateNode, s = t.memoizedProps;
    l.props = s;
    var a = l.context, u = n.contextType;
    typeof u == "object" && u !== null ? u = ft(u) : (u = Ve(n) ? Tn : be.current, u = fr(t, u));
    var c = n.getDerivedStateFromProps, d = typeof c == "function" || typeof l.getSnapshotBeforeUpdate == "function";
    d || typeof l.UNSAFE_componentWillReceiveProps != "function" && typeof l.componentWillReceiveProps != "function" || (s !== r || a !== u) && yd(t, l, r, u), Jt = !1;
    var p = t.memoizedState;
    l.state = p, Ki(t, r, l, o), a = t.memoizedState, s !== r || p !== a || Ue.current || Jt ? (typeof c == "function" && (Pa(t, n, c, r), a = t.memoizedState), (s = Jt || vd(t, n, s, r, p, a, u)) ? (d || typeof l.UNSAFE_componentWillMount != "function" && typeof l.componentWillMount != "function" || (typeof l.componentWillMount == "function" && l.componentWillMount(), typeof l.UNSAFE_componentWillMount == "function" && l.UNSAFE_componentWillMount()), typeof l.componentDidMount == "function" && (t.flags |= 4194308)) : (typeof l.componentDidMount == "function" && (t.flags |= 4194308), t.memoizedProps = r, t.memoizedState = a), l.props = r, l.state = a, l.context = u, r = s) : (typeof l.componentDidMount == "function" && (t.flags |= 4194308), r = !1);
  } else {
    l = t.stateNode, im(e, t), s = t.memoizedProps, u = t.type === t.elementType ? s : St(t.type, s), l.props = u, d = t.pendingProps, p = l.context, a = n.contextType, typeof a == "object" && a !== null ? a = ft(a) : (a = Ve(n) ? Tn : be.current, a = fr(t, a));
    var v = n.getDerivedStateFromProps;
    (c = typeof v == "function" || typeof l.getSnapshotBeforeUpdate == "function") || typeof l.UNSAFE_componentWillReceiveProps != "function" && typeof l.componentWillReceiveProps != "function" || (s !== d || p !== a) && yd(t, l, r, a), Jt = !1, p = t.memoizedState, l.state = p, Ki(t, r, l, o);
    var x = t.memoizedState;
    s !== d || p !== x || Ue.current || Jt ? (typeof v == "function" && (Pa(t, n, v, r), x = t.memoizedState), (u = Jt || vd(t, n, u, r, p, x, a) || !1) ? (c || typeof l.UNSAFE_componentWillUpdate != "function" && typeof l.componentWillUpdate != "function" || (typeof l.componentWillUpdate == "function" && l.componentWillUpdate(r, x, a), typeof l.UNSAFE_componentWillUpdate == "function" && l.UNSAFE_componentWillUpdate(r, x, a)), typeof l.componentDidUpdate == "function" && (t.flags |= 4), typeof l.getSnapshotBeforeUpdate == "function" && (t.flags |= 1024)) : (typeof l.componentDidUpdate != "function" || s === e.memoizedProps && p === e.memoizedState || (t.flags |= 4), typeof l.getSnapshotBeforeUpdate != "function" || s === e.memoizedProps && p === e.memoizedState || (t.flags |= 1024), t.memoizedProps = r, t.memoizedState = x), l.props = r, l.state = x, l.context = a, r = u) : (typeof l.componentDidUpdate != "function" || s === e.memoizedProps && p === e.memoizedState || (t.flags |= 4), typeof l.getSnapshotBeforeUpdate != "function" || s === e.memoizedProps && p === e.memoizedState || (t.flags |= 1024), r = !1);
  }
  return Oa(e, t, n, r, i, o);
}
function Oa(e, t, n, r, o, i) {
  Om(e, t);
  var l = (t.flags & 128) !== 0;
  if (!r && !l)
    return o && ud(t, n, !1), Ht(e, t, i);
  r = t.stateNode, Pv.current = t;
  var s = l && typeof n.getDerivedStateFromError != "function" ? null : r.render();
  return t.flags |= 1, e !== null && l ? (t.child = mr(t, e.child, null, i), t.child = mr(t, null, s, i)) : Ae(e, t, s, i), t.memoizedState = r.state, o && ud(t, n, !0), t.child;
}
function jm(e) {
  var t = e.stateNode;
  t.pendingContext ? ad(e, t.pendingContext, t.pendingContext !== t.context) : t.context && ad(e, t.context, !1), $u(e, t.containerInfo);
}
function $d(e, t, n, r, o) {
  return pr(), xu(o), t.flags |= 256, Ae(e, t, n, r), t.child;
}
var ja = { dehydrated: null, treeContext: null, retryLane: 0 };
function za(e) {
  return { baseLanes: e, cachePool: null, transitions: null };
}
function zm(e, t, n) {
  var r = t.pendingProps, o = oe.current, i = !1, l = (t.flags & 128) !== 0, s;
  if ((s = l) || (s = e !== null && e.memoizedState === null ? !1 : (o & 2) !== 0), s ? (i = !0, t.flags &= -129) : (e === null || e.memoizedState !== null) && (o |= 1), q(oe, o & 1), e === null)
    return $a(t), e = t.memoizedState, e !== null && (e = e.dehydrated, e !== null) ? (t.mode & 1 ? e.data === "$!" ? t.lanes = 8 : t.lanes = 1073741824 : t.lanes = 1, null) : (l = r.children, e = r.fallback, i ? (r = t.mode, i = t.child, l = { mode: "hidden", children: l }, !(r & 1) && i !== null ? (i.childLanes = 0, i.pendingProps = l) : i = wl(l, r, 0, null), e = Pn(e, r, n, null), i.return = t, e.return = t, i.sibling = e, t.child = i, t.child.memoizedState = za(n), t.memoizedState = ja, e) : zu(t, l));
  if (o = e.memoizedState, o !== null && (s = o.dehydrated, s !== null))
    return Tv(e, t, l, r, s, o, n);
  if (i) {
    i = r.fallback, l = t.mode, o = e.child, s = o.sibling;
    var a = { mode: "hidden", children: r.children };
    return !(l & 1) && t.child !== o ? (r = t.child, r.childLanes = 0, r.pendingProps = a, t.deletions = null) : (r = fn(o, a), r.subtreeFlags = o.subtreeFlags & 14680064), s !== null ? i = fn(s, i) : (i = Pn(i, l, n, null), i.flags |= 2), i.return = t, r.return = t, r.sibling = i, t.child = r, r = i, i = t.child, l = e.child.memoizedState, l = l === null ? za(n) : { baseLanes: l.baseLanes | n, cachePool: null, transitions: l.transitions }, i.memoizedState = l, i.childLanes = e.childLanes & ~n, t.memoizedState = ja, r;
  }
  return i = e.child, e = i.sibling, r = fn(i, { mode: "visible", children: r.children }), !(t.mode & 1) && (r.lanes = n), r.return = t, r.sibling = null, e !== null && (n = t.deletions, n === null ? (t.deletions = [e], t.flags |= 16) : n.push(e)), t.child = r, t.memoizedState = null, r;
}
function zu(e, t) {
  return t = wl({ mode: "visible", children: t }, e.mode, 0, null), t.return = e, e.child = t;
}
function ii(e, t, n, r) {
  return r !== null && xu(r), mr(t, e.child, null, n), e = zu(t, t.pendingProps.children), e.flags |= 2, t.memoizedState = null, e;
}
function Tv(e, t, n, r, o, i, l) {
  if (n)
    return t.flags & 256 ? (t.flags &= -257, r = bs(Error(P(422))), ii(e, t, l, r)) : t.memoizedState !== null ? (t.child = e.child, t.flags |= 128, null) : (i = r.fallback, o = t.mode, r = wl({ mode: "visible", children: r.children }, o, 0, null), i = Pn(i, o, l, null), i.flags |= 2, r.return = t, i.return = t, r.sibling = i, t.child = r, t.mode & 1 && mr(t, e.child, null, l), t.child.memoizedState = za(l), t.memoizedState = ja, i);
  if (!(t.mode & 1))
    return ii(e, t, l, null);
  if (o.data === "$!") {
    if (r = o.nextSibling && o.nextSibling.dataset, r)
      var s = r.dgst;
    return r = s, i = Error(P(419)), r = bs(i, r, void 0), ii(e, t, l, r);
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
      o = o & (r.suspendedLanes | l) ? 0 : o, o !== 0 && o !== i.retryLane && (i.retryLane = o, Vt(e, o), _t(r, e, o, -1));
    }
    return Du(), r = bs(Error(P(421))), ii(e, t, l, r);
  }
  return o.data === "$?" ? (t.flags |= 128, t.child = e.child, t = Bv.bind(null, e), o._reactRetry = t, null) : (e = i.treeContext, qe = an(o.nextSibling), Ze = t, ne = !0, Ct = null, e !== null && (lt[st++] = Dt, lt[st++] = Ft, lt[st++] = Rn, Dt = e.id, Ft = e.overflow, Rn = t), t = zu(t, r.children), t.flags |= 4096, t);
}
function Ed(e, t, n) {
  e.lanes |= t;
  var r = e.alternate;
  r !== null && (r.lanes |= t), Ea(e.return, t, n);
}
function Is(e, t, n, r, o) {
  var i = e.memoizedState;
  i === null ? e.memoizedState = { isBackwards: t, rendering: null, renderingStartTime: 0, last: r, tail: n, tailMode: o } : (i.isBackwards = t, i.rendering = null, i.renderingStartTime = 0, i.last = r, i.tail = n, i.tailMode = o);
}
function Nm(e, t, n) {
  var r = t.pendingProps, o = r.revealOrder, i = r.tail;
  if (Ae(e, t, r.children, n), r = oe.current, r & 2)
    r = r & 1 | 2, t.flags |= 128;
  else {
    if (e !== null && e.flags & 128)
      e:
        for (e = t.child; e !== null; ) {
          if (e.tag === 13)
            e.memoizedState !== null && Ed(e, n, t);
          else if (e.tag === 19)
            Ed(e, n, t);
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
          e = n.alternate, e !== null && Gi(e) === null && (o = n), n = n.sibling;
        n = o, n === null ? (o = t.child, t.child = null) : (o = n.sibling, n.sibling = null), Is(t, !1, o, n, i);
        break;
      case "backwards":
        for (n = null, o = t.child, t.child = null; o !== null; ) {
          if (e = o.alternate, e !== null && Gi(e) === null) {
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
function wi(e, t) {
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
function Rv(e, t, n) {
  switch (t.tag) {
    case 3:
      jm(t), pr();
      break;
    case 5:
      lm(t);
      break;
    case 1:
      Ve(t.type) && Bi(t);
      break;
    case 4:
      $u(t, t.stateNode.containerInfo);
      break;
    case 10:
      var r = t.type._context, o = t.memoizedProps.value;
      q(Vi, r._currentValue), r._currentValue = o;
      break;
    case 13:
      if (r = t.memoizedState, r !== null)
        return r.dehydrated !== null ? (q(oe, oe.current & 1), t.flags |= 128, null) : n & t.child.childLanes ? zm(e, t, n) : (q(oe, oe.current & 1), e = Ht(e, t, n), e !== null ? e.sibling : null);
      q(oe, oe.current & 1);
      break;
    case 19:
      if (r = (n & t.childLanes) !== 0, e.flags & 128) {
        if (r)
          return Nm(e, t, n);
        t.flags |= 128;
      }
      if (o = t.memoizedState, o !== null && (o.rendering = null, o.tail = null, o.lastEffect = null), q(oe, oe.current), r)
        break;
      return null;
    case 22:
    case 23:
      return t.lanes = 0, Mm(e, t, n);
  }
  return Ht(e, t, n);
}
var bm, Na, Im, Am;
bm = function(e, t) {
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
Im = function(e, t, n, r) {
  var o = e.memoizedProps;
  if (o !== r) {
    e = t.stateNode, _n(jt.current);
    var i = null;
    switch (n) {
      case "input":
        o = na(e, o), r = na(e, r), i = [];
        break;
      case "select":
        o = le({}, o, { value: void 0 }), r = le({}, r, { value: void 0 }), i = [];
        break;
      case "textarea":
        o = ia(e, o), r = ia(e, r), i = [];
        break;
      default:
        typeof o.onClick != "function" && typeof r.onClick == "function" && (e.onclick = Di);
    }
    sa(n, r);
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
          u === "dangerouslySetInnerHTML" ? (a = a ? a.__html : void 0, s = s ? s.__html : void 0, a != null && s !== a && (i = i || []).push(u, a)) : u === "children" ? typeof a != "string" && typeof a != "number" || (i = i || []).push(u, "" + a) : u !== "suppressContentEditableWarning" && u !== "suppressHydrationWarning" && (lo.hasOwnProperty(u) ? (a != null && u === "onScroll" && J("scroll", e), i || s === a || (i = [])) : (i = i || []).push(u, a));
    }
    n && (i = i || []).push("style", n);
    var u = i;
    (t.updateQueue = u) && (t.flags |= 4);
  }
};
Am = function(e, t, n, r) {
  n !== r && (t.flags |= 4);
};
function Dr(e, t) {
  if (!ne)
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
function je(e) {
  var t = e.alternate !== null && e.alternate.child === e.child, n = 0, r = 0;
  if (t)
    for (var o = e.child; o !== null; )
      n |= o.lanes | o.childLanes, r |= o.subtreeFlags & 14680064, r |= o.flags & 14680064, o.return = e, o = o.sibling;
  else
    for (o = e.child; o !== null; )
      n |= o.lanes | o.childLanes, r |= o.subtreeFlags, r |= o.flags, o.return = e, o = o.sibling;
  return e.subtreeFlags |= r, e.childLanes = n, t;
}
function Mv(e, t, n) {
  var r = t.pendingProps;
  switch (yu(t), t.tag) {
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
      return je(t), null;
    case 1:
      return Ve(t.type) && Fi(), je(t), null;
    case 3:
      return r = t.stateNode, hr(), ee(Ue), ee(be), Pu(), r.pendingContext && (r.context = r.pendingContext, r.pendingContext = null), (e === null || e.child === null) && (ri(t) ? t.flags |= 4 : e === null || e.memoizedState.isDehydrated && !(t.flags & 256) || (t.flags |= 1024, Ct !== null && (Wa(Ct), Ct = null))), Na(e, t), je(t), null;
    case 5:
      Eu(t);
      var o = _n(xo.current);
      if (n = t.type, e !== null && t.stateNode != null)
        Im(e, t, n, r, o), e.ref !== t.ref && (t.flags |= 512, t.flags |= 2097152);
      else {
        if (!r) {
          if (t.stateNode === null)
            throw Error(P(166));
          return je(t), null;
        }
        if (e = _n(jt.current), ri(t)) {
          r = t.stateNode, n = t.type;
          var i = t.memoizedProps;
          switch (r[Mt] = t, r[vo] = i, e = (t.mode & 1) !== 0, n) {
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
              for (o = 0; o < Qr.length; o++)
                J(Qr[o], r);
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
              bc(r, i), J("invalid", r);
              break;
            case "select":
              r._wrapperState = { wasMultiple: !!i.multiple }, J("invalid", r);
              break;
            case "textarea":
              Ac(r, i), J("invalid", r);
          }
          sa(n, i), o = null;
          for (var l in i)
            if (i.hasOwnProperty(l)) {
              var s = i[l];
              l === "children" ? typeof s == "string" ? r.textContent !== s && (i.suppressHydrationWarning !== !0 && ni(r.textContent, s, e), o = ["children", s]) : typeof s == "number" && r.textContent !== "" + s && (i.suppressHydrationWarning !== !0 && ni(
                r.textContent,
                s,
                e
              ), o = ["children", "" + s]) : lo.hasOwnProperty(l) && s != null && l === "onScroll" && J("scroll", r);
            }
          switch (n) {
            case "input":
              Qo(r), Ic(r, i, !0);
              break;
            case "textarea":
              Qo(r), Lc(r);
              break;
            case "select":
            case "option":
              break;
            default:
              typeof i.onClick == "function" && (r.onclick = Di);
          }
          r = o, t.updateQueue = r, r !== null && (t.flags |= 4);
        } else {
          l = o.nodeType === 9 ? o : o.ownerDocument, e === "http://www.w3.org/1999/xhtml" && (e = dp(n)), e === "http://www.w3.org/1999/xhtml" ? n === "script" ? (e = l.createElement("div"), e.innerHTML = "<script><\/script>", e = e.removeChild(e.firstChild)) : typeof r.is == "string" ? e = l.createElement(n, { is: r.is }) : (e = l.createElement(n), n === "select" && (l = e, r.multiple ? l.multiple = !0 : r.size && (l.size = r.size))) : e = l.createElementNS(e, n), e[Mt] = t, e[vo] = r, bm(e, t, !1, !1), t.stateNode = e;
          e: {
            switch (l = aa(n, r), n) {
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
                for (o = 0; o < Qr.length; o++)
                  J(Qr[o], e);
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
                bc(e, r), o = na(e, r), J("invalid", e);
                break;
              case "option":
                o = r;
                break;
              case "select":
                e._wrapperState = { wasMultiple: !!r.multiple }, o = le({}, r, { value: void 0 }), J("invalid", e);
                break;
              case "textarea":
                Ac(e, r), o = ia(e, r), J("invalid", e);
                break;
              default:
                o = r;
            }
            sa(n, o), s = o;
            for (i in s)
              if (s.hasOwnProperty(i)) {
                var a = s[i];
                i === "style" ? mp(e, a) : i === "dangerouslySetInnerHTML" ? (a = a ? a.__html : void 0, a != null && fp(e, a)) : i === "children" ? typeof a == "string" ? (n !== "textarea" || a !== "") && so(e, a) : typeof a == "number" && so(e, "" + a) : i !== "suppressContentEditableWarning" && i !== "suppressHydrationWarning" && i !== "autoFocus" && (lo.hasOwnProperty(i) ? a != null && i === "onScroll" && J("scroll", e) : a != null && ru(e, i, a, l));
              }
            switch (n) {
              case "input":
                Qo(e), Ic(e, r, !1);
                break;
              case "textarea":
                Qo(e), Lc(e);
                break;
              case "option":
                r.value != null && e.setAttribute("value", "" + pn(r.value));
                break;
              case "select":
                e.multiple = !!r.multiple, i = r.value, i != null ? nr(e, !!r.multiple, i, !1) : r.defaultValue != null && nr(
                  e,
                  !!r.multiple,
                  r.defaultValue,
                  !0
                );
                break;
              default:
                typeof o.onClick == "function" && (e.onclick = Di);
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
      return je(t), null;
    case 6:
      if (e && t.stateNode != null)
        Am(e, t, e.memoizedProps, r);
      else {
        if (typeof r != "string" && t.stateNode === null)
          throw Error(P(166));
        if (n = _n(xo.current), _n(jt.current), ri(t)) {
          if (r = t.stateNode, n = t.memoizedProps, r[Mt] = t, (i = r.nodeValue !== n) && (e = Ze, e !== null))
            switch (e.tag) {
              case 3:
                ni(r.nodeValue, n, (e.mode & 1) !== 0);
                break;
              case 5:
                e.memoizedProps.suppressHydrationWarning !== !0 && ni(r.nodeValue, n, (e.mode & 1) !== 0);
            }
          i && (t.flags |= 4);
        } else
          r = (n.nodeType === 9 ? n : n.ownerDocument).createTextNode(r), r[Mt] = t, t.stateNode = r;
      }
      return je(t), null;
    case 13:
      if (ee(oe), r = t.memoizedState, e === null || e.memoizedState !== null && e.memoizedState.dehydrated !== null) {
        if (ne && qe !== null && t.mode & 1 && !(t.flags & 128))
          tm(), pr(), t.flags |= 98560, i = !1;
        else if (i = ri(t), r !== null && r.dehydrated !== null) {
          if (e === null) {
            if (!i)
              throw Error(P(318));
            if (i = t.memoizedState, i = i !== null ? i.dehydrated : null, !i)
              throw Error(P(317));
            i[Mt] = t;
          } else
            pr(), !(t.flags & 128) && (t.memoizedState = null), t.flags |= 4;
          je(t), i = !1;
        } else
          Ct !== null && (Wa(Ct), Ct = null), i = !0;
        if (!i)
          return t.flags & 65536 ? t : null;
      }
      return t.flags & 128 ? (t.lanes = n, t) : (r = r !== null, r !== (e !== null && e.memoizedState !== null) && r && (t.child.flags |= 8192, t.mode & 1 && (e === null || oe.current & 1 ? we === 0 && (we = 3) : Du())), t.updateQueue !== null && (t.flags |= 4), je(t), null);
    case 4:
      return hr(), Na(e, t), e === null && ho(t.stateNode.containerInfo), je(t), null;
    case 10:
      return Cu(t.type._context), je(t), null;
    case 17:
      return Ve(t.type) && Fi(), je(t), null;
    case 19:
      if (ee(oe), i = t.memoizedState, i === null)
        return je(t), null;
      if (r = (t.flags & 128) !== 0, l = i.rendering, l === null)
        if (r)
          Dr(i, !1);
        else {
          if (we !== 0 || e !== null && e.flags & 128)
            for (e = t.child; e !== null; ) {
              if (l = Gi(e), l !== null) {
                for (t.flags |= 128, Dr(i, !1), r = l.updateQueue, r !== null && (t.updateQueue = r, t.flags |= 4), t.subtreeFlags = 0, r = n, n = t.child; n !== null; )
                  i = n, e = r, i.flags &= 14680066, l = i.alternate, l === null ? (i.childLanes = 0, i.lanes = e, i.child = null, i.subtreeFlags = 0, i.memoizedProps = null, i.memoizedState = null, i.updateQueue = null, i.dependencies = null, i.stateNode = null) : (i.childLanes = l.childLanes, i.lanes = l.lanes, i.child = l.child, i.subtreeFlags = 0, i.deletions = null, i.memoizedProps = l.memoizedProps, i.memoizedState = l.memoizedState, i.updateQueue = l.updateQueue, i.type = l.type, e = l.dependencies, i.dependencies = e === null ? null : { lanes: e.lanes, firstContext: e.firstContext }), n = n.sibling;
                return q(oe, oe.current & 1 | 2), t.child;
              }
              e = e.sibling;
            }
          i.tail !== null && ce() > vr && (t.flags |= 128, r = !0, Dr(i, !1), t.lanes = 4194304);
        }
      else {
        if (!r)
          if (e = Gi(l), e !== null) {
            if (t.flags |= 128, r = !0, n = e.updateQueue, n !== null && (t.updateQueue = n, t.flags |= 4), Dr(i, !0), i.tail === null && i.tailMode === "hidden" && !l.alternate && !ne)
              return je(t), null;
          } else
            2 * ce() - i.renderingStartTime > vr && n !== 1073741824 && (t.flags |= 128, r = !0, Dr(i, !1), t.lanes = 4194304);
        i.isBackwards ? (l.sibling = t.child, t.child = l) : (n = i.last, n !== null ? n.sibling = l : t.child = l, i.last = l);
      }
      return i.tail !== null ? (t = i.tail, i.rendering = t, i.tail = t.sibling, i.renderingStartTime = ce(), t.sibling = null, n = oe.current, q(oe, r ? n & 1 | 2 : n & 1), t) : (je(t), null);
    case 22:
    case 23:
      return Lu(), r = t.memoizedState !== null, e !== null && e.memoizedState !== null !== r && (t.flags |= 8192), r && t.mode & 1 ? Ye & 1073741824 && (je(t), t.subtreeFlags & 6 && (t.flags |= 8192)) : je(t), null;
    case 24:
      return null;
    case 25:
      return null;
  }
  throw Error(P(156, t.tag));
}
function Ov(e, t) {
  switch (yu(t), t.tag) {
    case 1:
      return Ve(t.type) && Fi(), e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, t) : null;
    case 3:
      return hr(), ee(Ue), ee(be), Pu(), e = t.flags, e & 65536 && !(e & 128) ? (t.flags = e & -65537 | 128, t) : null;
    case 5:
      return Eu(t), null;
    case 13:
      if (ee(oe), e = t.memoizedState, e !== null && e.dehydrated !== null) {
        if (t.alternate === null)
          throw Error(P(340));
        pr();
      }
      return e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, t) : null;
    case 19:
      return ee(oe), null;
    case 4:
      return hr(), null;
    case 10:
      return Cu(t.type._context), null;
    case 22:
    case 23:
      return Lu(), null;
    case 24:
      return null;
    default:
      return null;
  }
}
var li = !1, Ne = !1, jv = typeof WeakSet == "function" ? WeakSet : Set, O = null;
function er(e, t) {
  var n = e.ref;
  if (n !== null)
    if (typeof n == "function")
      try {
        n(null);
      } catch (r) {
        ue(e, t, r);
      }
    else
      n.current = null;
}
function ba(e, t, n) {
  try {
    n();
  } catch (r) {
    ue(e, t, r);
  }
}
var Pd = !1;
function zv(e, t) {
  if (ya = Ii, e = Wp(), gu(e)) {
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
          var l = 0, s = -1, a = -1, u = 0, c = 0, d = e, p = null;
          t:
            for (; ; ) {
              for (var v; d !== n || o !== 0 && d.nodeType !== 3 || (s = l + o), d !== i || r !== 0 && d.nodeType !== 3 || (a = l + r), d.nodeType === 3 && (l += d.nodeValue.length), (v = d.firstChild) !== null; )
                p = d, d = v;
              for (; ; ) {
                if (d === e)
                  break t;
                if (p === n && ++u === o && (s = l), p === i && ++c === r && (a = l), (v = d.nextSibling) !== null)
                  break;
                d = p, p = d.parentNode;
              }
              d = v;
            }
          n = s === -1 || a === -1 ? null : { start: s, end: a };
        } else
          n = null;
      }
    n = n || { start: 0, end: 0 };
  } else
    n = null;
  for (xa = { focusedElem: e, selectionRange: n }, Ii = !1, O = t; O !== null; )
    if (t = O, e = t.child, (t.subtreeFlags & 1028) !== 0 && e !== null)
      e.return = t, O = e;
    else
      for (; O !== null; ) {
        t = O;
        try {
          var x = t.alternate;
          if (t.flags & 1024)
            switch (t.tag) {
              case 0:
              case 11:
              case 15:
                break;
              case 1:
                if (x !== null) {
                  var g = x.memoizedProps, E = x.memoizedState, m = t.stateNode, f = m.getSnapshotBeforeUpdate(t.elementType === t.type ? g : St(t.type, g), E);
                  m.__reactInternalSnapshotBeforeUpdate = f;
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
          ue(t, t.return, S);
        }
        if (e = t.sibling, e !== null) {
          e.return = t.return, O = e;
          break;
        }
        O = t.return;
      }
  return x = Pd, Pd = !1, x;
}
function no(e, t, n) {
  var r = t.updateQueue;
  if (r = r !== null ? r.lastEffect : null, r !== null) {
    var o = r = r.next;
    do {
      if ((o.tag & e) === e) {
        var i = o.destroy;
        o.destroy = void 0, i !== void 0 && ba(t, n, i);
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
function Ia(e) {
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
function Lm(e) {
  var t = e.alternate;
  t !== null && (e.alternate = null, Lm(t)), e.child = null, e.deletions = null, e.sibling = null, e.tag === 5 && (t = e.stateNode, t !== null && (delete t[Mt], delete t[vo], delete t[Ca], delete t[hv], delete t[gv])), e.stateNode = null, e.return = null, e.dependencies = null, e.memoizedProps = null, e.memoizedState = null, e.pendingProps = null, e.stateNode = null, e.updateQueue = null;
}
function Dm(e) {
  return e.tag === 5 || e.tag === 3 || e.tag === 4;
}
function Td(e) {
  e:
    for (; ; ) {
      for (; e.sibling === null; ) {
        if (e.return === null || Dm(e.return))
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
function Aa(e, t, n) {
  var r = e.tag;
  if (r === 5 || r === 6)
    e = e.stateNode, t ? n.nodeType === 8 ? n.parentNode.insertBefore(e, t) : n.insertBefore(e, t) : (n.nodeType === 8 ? (t = n.parentNode, t.insertBefore(e, n)) : (t = n, t.appendChild(e)), n = n._reactRootContainer, n != null || t.onclick !== null || (t.onclick = Di));
  else if (r !== 4 && (e = e.child, e !== null))
    for (Aa(e, t, n), e = e.sibling; e !== null; )
      Aa(e, t, n), e = e.sibling;
}
function La(e, t, n) {
  var r = e.tag;
  if (r === 5 || r === 6)
    e = e.stateNode, t ? n.insertBefore(e, t) : n.appendChild(e);
  else if (r !== 4 && (e = e.child, e !== null))
    for (La(e, t, n), e = e.sibling; e !== null; )
      La(e, t, n), e = e.sibling;
}
var Pe = null, wt = !1;
function Yt(e, t, n) {
  for (n = n.child; n !== null; )
    Fm(e, t, n), n = n.sibling;
}
function Fm(e, t, n) {
  if (Ot && typeof Ot.onCommitFiberUnmount == "function")
    try {
      Ot.onCommitFiberUnmount(dl, n);
    } catch {
    }
  switch (n.tag) {
    case 5:
      Ne || er(n, t);
    case 6:
      var r = Pe, o = wt;
      Pe = null, Yt(e, t, n), Pe = r, wt = o, Pe !== null && (wt ? (e = Pe, n = n.stateNode, e.nodeType === 8 ? e.parentNode.removeChild(n) : e.removeChild(n)) : Pe.removeChild(n.stateNode));
      break;
    case 18:
      Pe !== null && (wt ? (e = Pe, n = n.stateNode, e.nodeType === 8 ? Rs(e.parentNode, n) : e.nodeType === 1 && Rs(e, n), fo(e)) : Rs(Pe, n.stateNode));
      break;
    case 4:
      r = Pe, o = wt, Pe = n.stateNode.containerInfo, wt = !0, Yt(e, t, n), Pe = r, wt = o;
      break;
    case 0:
    case 11:
    case 14:
    case 15:
      if (!Ne && (r = n.updateQueue, r !== null && (r = r.lastEffect, r !== null))) {
        o = r = r.next;
        do {
          var i = o, l = i.destroy;
          i = i.tag, l !== void 0 && (i & 2 || i & 4) && ba(n, t, l), o = o.next;
        } while (o !== r);
      }
      Yt(e, t, n);
      break;
    case 1:
      if (!Ne && (er(n, t), r = n.stateNode, typeof r.componentWillUnmount == "function"))
        try {
          r.props = n.memoizedProps, r.state = n.memoizedState, r.componentWillUnmount();
        } catch (s) {
          ue(n, t, s);
        }
      Yt(e, t, n);
      break;
    case 21:
      Yt(e, t, n);
      break;
    case 22:
      n.mode & 1 ? (Ne = (r = Ne) || n.memoizedState !== null, Yt(e, t, n), Ne = r) : Yt(e, t, n);
      break;
    default:
      Yt(e, t, n);
  }
}
function Rd(e) {
  var t = e.updateQueue;
  if (t !== null) {
    e.updateQueue = null;
    var n = e.stateNode;
    n === null && (n = e.stateNode = new jv()), t.forEach(function(r) {
      var o = Wv.bind(null, e, r);
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
                Pe = s.stateNode, wt = !1;
                break e;
              case 3:
                Pe = s.stateNode.containerInfo, wt = !0;
                break e;
              case 4:
                Pe = s.stateNode.containerInfo, wt = !0;
                break e;
            }
            s = s.return;
          }
        if (Pe === null)
          throw Error(P(160));
        Fm(i, l, o), Pe = null, wt = !1;
        var a = o.alternate;
        a !== null && (a.return = null), o.return = null;
      } catch (u) {
        ue(o, t, u);
      }
    }
  if (t.subtreeFlags & 12854)
    for (t = t.child; t !== null; )
      Bm(t, e), t = t.sibling;
}
function Bm(e, t) {
  var n = e.alternate, r = e.flags;
  switch (e.tag) {
    case 0:
    case 11:
    case 14:
    case 15:
      if (xt(t, e), Et(e), r & 4) {
        try {
          no(3, e, e.return), xl(3, e);
        } catch (g) {
          ue(e, e.return, g);
        }
        try {
          no(5, e, e.return);
        } catch (g) {
          ue(e, e.return, g);
        }
      }
      break;
    case 1:
      xt(t, e), Et(e), r & 512 && n !== null && er(n, n.return);
      break;
    case 5:
      if (xt(t, e), Et(e), r & 512 && n !== null && er(n, n.return), e.flags & 32) {
        var o = e.stateNode;
        try {
          so(o, "");
        } catch (g) {
          ue(e, e.return, g);
        }
      }
      if (r & 4 && (o = e.stateNode, o != null)) {
        var i = e.memoizedProps, l = n !== null ? n.memoizedProps : i, s = e.type, a = e.updateQueue;
        if (e.updateQueue = null, a !== null)
          try {
            s === "input" && i.type === "radio" && i.name != null && up(o, i), aa(s, l);
            var u = aa(s, i);
            for (l = 0; l < a.length; l += 2) {
              var c = a[l], d = a[l + 1];
              c === "style" ? mp(o, d) : c === "dangerouslySetInnerHTML" ? fp(o, d) : c === "children" ? so(o, d) : ru(o, c, d, u);
            }
            switch (s) {
              case "input":
                ra(o, i);
                break;
              case "textarea":
                cp(o, i);
                break;
              case "select":
                var p = o._wrapperState.wasMultiple;
                o._wrapperState.wasMultiple = !!i.multiple;
                var v = i.value;
                v != null ? nr(o, !!i.multiple, v, !1) : p !== !!i.multiple && (i.defaultValue != null ? nr(
                  o,
                  !!i.multiple,
                  i.defaultValue,
                  !0
                ) : nr(o, !!i.multiple, i.multiple ? [] : "", !1));
            }
            o[vo] = i;
          } catch (g) {
            ue(e, e.return, g);
          }
      }
      break;
    case 6:
      if (xt(t, e), Et(e), r & 4) {
        if (e.stateNode === null)
          throw Error(P(162));
        o = e.stateNode, i = e.memoizedProps;
        try {
          o.nodeValue = i;
        } catch (g) {
          ue(e, e.return, g);
        }
      }
      break;
    case 3:
      if (xt(t, e), Et(e), r & 4 && n !== null && n.memoizedState.isDehydrated)
        try {
          fo(t.containerInfo);
        } catch (g) {
          ue(e, e.return, g);
        }
      break;
    case 4:
      xt(t, e), Et(e);
      break;
    case 13:
      xt(t, e), Et(e), o = e.child, o.flags & 8192 && (i = o.memoizedState !== null, o.stateNode.isHidden = i, !i || o.alternate !== null && o.alternate.memoizedState !== null || (Iu = ce())), r & 4 && Rd(e);
      break;
    case 22:
      if (c = n !== null && n.memoizedState !== null, e.mode & 1 ? (Ne = (u = Ne) || c, xt(t, e), Ne = u) : xt(t, e), Et(e), r & 8192) {
        if (u = e.memoizedState !== null, (e.stateNode.isHidden = u) && !c && e.mode & 1)
          for (O = e, c = e.child; c !== null; ) {
            for (d = O = c; O !== null; ) {
              switch (p = O, v = p.child, p.tag) {
                case 0:
                case 11:
                case 14:
                case 15:
                  no(4, p, p.return);
                  break;
                case 1:
                  er(p, p.return);
                  var x = p.stateNode;
                  if (typeof x.componentWillUnmount == "function") {
                    r = p, n = p.return;
                    try {
                      t = r, x.props = t.memoizedProps, x.state = t.memoizedState, x.componentWillUnmount();
                    } catch (g) {
                      ue(r, n, g);
                    }
                  }
                  break;
                case 5:
                  er(p, p.return);
                  break;
                case 22:
                  if (p.memoizedState !== null) {
                    Od(d);
                    continue;
                  }
              }
              v !== null ? (v.return = p, O = v) : Od(d);
            }
            c = c.sibling;
          }
        e:
          for (c = null, d = e; ; ) {
            if (d.tag === 5) {
              if (c === null) {
                c = d;
                try {
                  o = d.stateNode, u ? (i = o.style, typeof i.setProperty == "function" ? i.setProperty("display", "none", "important") : i.display = "none") : (s = d.stateNode, a = d.memoizedProps.style, l = a != null && a.hasOwnProperty("display") ? a.display : null, s.style.display = pp("display", l));
                } catch (g) {
                  ue(e, e.return, g);
                }
              }
            } else if (d.tag === 6) {
              if (c === null)
                try {
                  d.stateNode.nodeValue = u ? "" : d.memoizedProps;
                } catch (g) {
                  ue(e, e.return, g);
                }
            } else if ((d.tag !== 22 && d.tag !== 23 || d.memoizedState === null || d === e) && d.child !== null) {
              d.child.return = d, d = d.child;
              continue;
            }
            if (d === e)
              break e;
            for (; d.sibling === null; ) {
              if (d.return === null || d.return === e)
                break e;
              c === d && (c = null), d = d.return;
            }
            c === d && (c = null), d.sibling.return = d.return, d = d.sibling;
          }
      }
      break;
    case 19:
      xt(t, e), Et(e), r & 4 && Rd(e);
      break;
    case 21:
      break;
    default:
      xt(
        t,
        e
      ), Et(e);
  }
}
function Et(e) {
  var t = e.flags;
  if (t & 2) {
    try {
      e: {
        for (var n = e.return; n !== null; ) {
          if (Dm(n)) {
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
          var i = Td(e);
          La(e, i, o);
          break;
        case 3:
        case 4:
          var l = r.stateNode.containerInfo, s = Td(e);
          Aa(e, s, l);
          break;
        default:
          throw Error(P(161));
      }
    } catch (a) {
      ue(e, e.return, a);
    }
    e.flags &= -3;
  }
  t & 4096 && (e.flags &= -4097);
}
function Nv(e, t, n) {
  O = e, Wm(e);
}
function Wm(e, t, n) {
  for (var r = (e.mode & 1) !== 0; O !== null; ) {
    var o = O, i = o.child;
    if (o.tag === 22 && r) {
      var l = o.memoizedState !== null || li;
      if (!l) {
        var s = o.alternate, a = s !== null && s.memoizedState !== null || Ne;
        s = li;
        var u = Ne;
        if (li = l, (Ne = a) && !u)
          for (O = o; O !== null; )
            l = O, a = l.child, l.tag === 22 && l.memoizedState !== null ? jd(o) : a !== null ? (a.return = l, O = a) : jd(o);
        for (; i !== null; )
          O = i, Wm(i), i = i.sibling;
        O = o, li = s, Ne = u;
      }
      Md(e);
    } else
      o.subtreeFlags & 8772 && i !== null ? (i.return = o, O = i) : Md(e);
  }
}
function Md(e) {
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
              Ne || xl(5, t);
              break;
            case 1:
              var r = t.stateNode;
              if (t.flags & 4 && !Ne)
                if (n === null)
                  r.componentDidMount();
                else {
                  var o = t.elementType === t.type ? n.memoizedProps : St(t.type, n.memoizedProps);
                  r.componentDidUpdate(o, n.memoizedState, r.__reactInternalSnapshotBeforeUpdate);
                }
              var i = t.updateQueue;
              i !== null && md(t, i, r);
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
                md(t, l, n);
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
                    var d = c.dehydrated;
                    d !== null && fo(d);
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
        Ne || t.flags & 512 && Ia(t);
      } catch (p) {
        ue(t, t.return, p);
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
function Od(e) {
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
function jd(e) {
  for (; O !== null; ) {
    var t = O;
    try {
      switch (t.tag) {
        case 0:
        case 11:
        case 15:
          var n = t.return;
          try {
            xl(4, t);
          } catch (a) {
            ue(t, n, a);
          }
          break;
        case 1:
          var r = t.stateNode;
          if (typeof r.componentDidMount == "function") {
            var o = t.return;
            try {
              r.componentDidMount();
            } catch (a) {
              ue(t, o, a);
            }
          }
          var i = t.return;
          try {
            Ia(t);
          } catch (a) {
            ue(t, i, a);
          }
          break;
        case 5:
          var l = t.return;
          try {
            Ia(t);
          } catch (a) {
            ue(t, l, a);
          }
      }
    } catch (a) {
      ue(t, t.return, a);
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
var bv = Math.ceil, Xi = Gt.ReactCurrentDispatcher, Nu = Gt.ReactCurrentOwner, dt = Gt.ReactCurrentBatchConfig, W = 0, _e = null, ge = null, Re = 0, Ye = 0, tr = gn(0), we = 0, ko = null, On = 0, Sl = 0, bu = 0, ro = null, Be = null, Iu = 0, vr = 1 / 0, It = null, qi = !1, Da = null, cn = null, si = !1, rn = null, Zi = 0, oo = 0, Fa = null, Ci = -1, ki = 0;
function Le() {
  return W & 6 ? ce() : Ci !== -1 ? Ci : Ci = ce();
}
function dn(e) {
  return e.mode & 1 ? W & 2 && Re !== 0 ? Re & -Re : yv.transition !== null ? (ki === 0 && (ki = Ep()), ki) : (e = G, e !== 0 || (e = window.event, e = e === void 0 ? 16 : zp(e.type)), e) : 1;
}
function _t(e, t, n, r) {
  if (50 < oo)
    throw oo = 0, Fa = null, Error(P(185));
  jo(e, n, r), (!(W & 2) || e !== _e) && (e === _e && (!(W & 2) && (Sl |= n), we === 4 && tn(e, Re)), He(e, r), n === 1 && W === 0 && !(t.mode & 1) && (vr = ce() + 500, gl && vn()));
}
function He(e, t) {
  var n = e.callbackNode;
  yg(e, t);
  var r = bi(e, e === _e ? Re : 0);
  if (r === 0)
    n !== null && Bc(n), e.callbackNode = null, e.callbackPriority = 0;
  else if (t = r & -r, e.callbackPriority !== t) {
    if (n != null && Bc(n), t === 1)
      e.tag === 0 ? vv(zd.bind(null, e)) : Zp(zd.bind(null, e)), pv(function() {
        !(W & 6) && vn();
      }), n = null;
    else {
      switch (Pp(r)) {
        case 1:
          n = au;
          break;
        case 4:
          n = _p;
          break;
        case 16:
          n = Ni;
          break;
        case 536870912:
          n = $p;
          break;
        default:
          n = Ni;
      }
      n = Xm(n, Um.bind(null, e));
    }
    e.callbackPriority = t, e.callbackNode = n;
  }
}
function Um(e, t) {
  if (Ci = -1, ki = 0, W & 6)
    throw Error(P(327));
  var n = e.callbackNode;
  if (sr() && e.callbackNode !== n)
    return null;
  var r = bi(e, e === _e ? Re : 0);
  if (r === 0)
    return null;
  if (r & 30 || r & e.expiredLanes || t)
    t = Ji(e, r);
  else {
    t = r;
    var o = W;
    W |= 2;
    var i = Hm();
    (_e !== e || Re !== t) && (It = null, vr = ce() + 500, En(e, t));
    do
      try {
        Lv();
        break;
      } catch (s) {
        Vm(e, s);
      }
    while (1);
    wu(), Xi.current = i, W = o, ge !== null ? t = 0 : (_e = null, Re = 0, t = we);
  }
  if (t !== 0) {
    if (t === 2 && (o = pa(e), o !== 0 && (r = o, t = Ba(e, o))), t === 1)
      throw n = ko, En(e, 0), tn(e, r), He(e, ce()), n;
    if (t === 6)
      tn(e, r);
    else {
      if (o = e.current.alternate, !(r & 30) && !Iv(o) && (t = Ji(e, r), t === 2 && (i = pa(e), i !== 0 && (r = i, t = Ba(e, i))), t === 1))
        throw n = ko, En(e, 0), tn(e, r), He(e, ce()), n;
      switch (e.finishedWork = o, e.finishedLanes = r, t) {
        case 0:
        case 1:
          throw Error(P(345));
        case 2:
          Sn(e, Be, It);
          break;
        case 3:
          if (tn(e, r), (r & 130023424) === r && (t = Iu + 500 - ce(), 10 < t)) {
            if (bi(e, 0) !== 0)
              break;
            if (o = e.suspendedLanes, (o & r) !== r) {
              Le(), e.pingedLanes |= e.suspendedLanes & o;
              break;
            }
            e.timeoutHandle = wa(Sn.bind(null, e, Be, It), t);
            break;
          }
          Sn(e, Be, It);
          break;
        case 4:
          if (tn(e, r), (r & 4194240) === r)
            break;
          for (t = e.eventTimes, o = -1; 0 < r; ) {
            var l = 31 - kt(r);
            i = 1 << l, l = t[l], l > o && (o = l), r &= ~i;
          }
          if (r = o, r = ce() - r, r = (120 > r ? 120 : 480 > r ? 480 : 1080 > r ? 1080 : 1920 > r ? 1920 : 3e3 > r ? 3e3 : 4320 > r ? 4320 : 1960 * bv(r / 1960)) - r, 10 < r) {
            e.timeoutHandle = wa(Sn.bind(null, e, Be, It), r);
            break;
          }
          Sn(e, Be, It);
          break;
        case 5:
          Sn(e, Be, It);
          break;
        default:
          throw Error(P(329));
      }
    }
  }
  return He(e, ce()), e.callbackNode === n ? Um.bind(null, e) : null;
}
function Ba(e, t) {
  var n = ro;
  return e.current.memoizedState.isDehydrated && (En(e, t).flags |= 256), e = Ji(e, t), e !== 2 && (t = Be, Be = n, t !== null && Wa(t)), e;
}
function Wa(e) {
  Be === null ? Be = e : Be.push.apply(Be, e);
}
function Iv(e) {
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
function tn(e, t) {
  for (t &= ~bu, t &= ~Sl, e.suspendedLanes |= t, e.pingedLanes &= ~t, e = e.expirationTimes; 0 < t; ) {
    var n = 31 - kt(t), r = 1 << n;
    e[n] = -1, t &= ~r;
  }
}
function zd(e) {
  if (W & 6)
    throw Error(P(327));
  sr();
  var t = bi(e, 0);
  if (!(t & 1))
    return He(e, ce()), null;
  var n = Ji(e, t);
  if (e.tag !== 0 && n === 2) {
    var r = pa(e);
    r !== 0 && (t = r, n = Ba(e, r));
  }
  if (n === 1)
    throw n = ko, En(e, 0), tn(e, t), He(e, ce()), n;
  if (n === 6)
    throw Error(P(345));
  return e.finishedWork = e.current.alternate, e.finishedLanes = t, Sn(e, Be, It), He(e, ce()), null;
}
function Au(e, t) {
  var n = W;
  W |= 1;
  try {
    return e(t);
  } finally {
    W = n, W === 0 && (vr = ce() + 500, gl && vn());
  }
}
function jn(e) {
  rn !== null && rn.tag === 0 && !(W & 6) && sr();
  var t = W;
  W |= 1;
  var n = dt.transition, r = G;
  try {
    if (dt.transition = null, G = 1, e)
      return e();
  } finally {
    G = r, dt.transition = n, W = t, !(W & 6) && vn();
  }
}
function Lu() {
  Ye = tr.current, ee(tr);
}
function En(e, t) {
  e.finishedWork = null, e.finishedLanes = 0;
  var n = e.timeoutHandle;
  if (n !== -1 && (e.timeoutHandle = -1, fv(n)), ge !== null)
    for (n = ge.return; n !== null; ) {
      var r = n;
      switch (yu(r), r.tag) {
        case 1:
          r = r.type.childContextTypes, r != null && Fi();
          break;
        case 3:
          hr(), ee(Ue), ee(be), Pu();
          break;
        case 5:
          Eu(r);
          break;
        case 4:
          hr();
          break;
        case 13:
          ee(oe);
          break;
        case 19:
          ee(oe);
          break;
        case 10:
          Cu(r.type._context);
          break;
        case 22:
        case 23:
          Lu();
      }
      n = n.return;
    }
  if (_e = e, ge = e = fn(e.current, null), Re = Ye = t, we = 0, ko = null, bu = Sl = On = 0, Be = ro = null, kn !== null) {
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
function Vm(e, t) {
  do {
    var n = ge;
    try {
      if (wu(), xi.current = Yi, Qi) {
        for (var r = ie.memoizedState; r !== null; ) {
          var o = r.queue;
          o !== null && (o.pending = null), r = r.next;
        }
        Qi = !1;
      }
      if (Mn = 0, ke = Se = ie = null, to = !1, So = 0, Nu.current = null, n === null || n.return === null) {
        we = 1, ko = t, ge = null;
        break;
      }
      e: {
        var i = e, l = n.return, s = n, a = t;
        if (t = Re, s.flags |= 32768, a !== null && typeof a == "object" && typeof a.then == "function") {
          var u = a, c = s, d = c.tag;
          if (!(c.mode & 1) && (d === 0 || d === 11 || d === 15)) {
            var p = c.alternate;
            p ? (c.updateQueue = p.updateQueue, c.memoizedState = p.memoizedState, c.lanes = p.lanes) : (c.updateQueue = null, c.memoizedState = null);
          }
          var v = Sd(l);
          if (v !== null) {
            v.flags &= -257, wd(v, l, s, i, t), v.mode & 1 && xd(i, u, t), t = v, a = u;
            var x = t.updateQueue;
            if (x === null) {
              var g = /* @__PURE__ */ new Set();
              g.add(a), t.updateQueue = g;
            } else
              x.add(a);
            break e;
          } else {
            if (!(t & 1)) {
              xd(i, u, t), Du();
              break e;
            }
            a = Error(P(426));
          }
        } else if (ne && s.mode & 1) {
          var E = Sd(l);
          if (E !== null) {
            !(E.flags & 65536) && (E.flags |= 256), wd(E, l, s, i, t), xu(gr(a, s));
            break e;
          }
        }
        i = a = gr(a, s), we !== 4 && (we = 2), ro === null ? ro = [i] : ro.push(i), i = l;
        do {
          switch (i.tag) {
            case 3:
              i.flags |= 65536, t &= -t, i.lanes |= t;
              var m = Pm(i, a, t);
              pd(i, m);
              break e;
            case 1:
              s = a;
              var f = i.type, h = i.stateNode;
              if (!(i.flags & 128) && (typeof f.getDerivedStateFromError == "function" || h !== null && typeof h.componentDidCatch == "function" && (cn === null || !cn.has(h)))) {
                i.flags |= 65536, t &= -t, i.lanes |= t;
                var S = Tm(i, s, t);
                pd(i, S);
                break e;
              }
          }
          i = i.return;
        } while (i !== null);
      }
      Gm(n);
    } catch ($) {
      t = $, ge === n && n !== null && (ge = n = n.return);
      continue;
    }
    break;
  } while (1);
}
function Hm() {
  var e = Xi.current;
  return Xi.current = Yi, e === null ? Yi : e;
}
function Du() {
  (we === 0 || we === 3 || we === 2) && (we = 4), _e === null || !(On & 268435455) && !(Sl & 268435455) || tn(_e, Re);
}
function Ji(e, t) {
  var n = W;
  W |= 2;
  var r = Hm();
  (_e !== e || Re !== t) && (It = null, En(e, t));
  do
    try {
      Av();
      break;
    } catch (o) {
      Vm(e, o);
    }
  while (1);
  if (wu(), W = n, Xi.current = r, ge !== null)
    throw Error(P(261));
  return _e = null, Re = 0, we;
}
function Av() {
  for (; ge !== null; )
    Km(ge);
}
function Lv() {
  for (; ge !== null && !ug(); )
    Km(ge);
}
function Km(e) {
  var t = Ym(e.alternate, e, Ye);
  e.memoizedProps = e.pendingProps, t === null ? Gm(e) : ge = t, Nu.current = null;
}
function Gm(e) {
  var t = e;
  do {
    var n = t.alternate;
    if (e = t.return, t.flags & 32768) {
      if (n = Ov(n, t), n !== null) {
        n.flags &= 32767, ge = n;
        return;
      }
      if (e !== null)
        e.flags |= 32768, e.subtreeFlags = 0, e.deletions = null;
      else {
        we = 6, ge = null;
        return;
      }
    } else if (n = Mv(n, t, Ye), n !== null) {
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
  var r = G, o = dt.transition;
  try {
    dt.transition = null, G = 1, Dv(e, t, n, r);
  } finally {
    dt.transition = o, G = r;
  }
  return null;
}
function Dv(e, t, n, r) {
  do
    sr();
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
  if (xg(e, i), e === _e && (ge = _e = null, Re = 0), !(n.subtreeFlags & 2064) && !(n.flags & 2064) || si || (si = !0, Xm(Ni, function() {
    return sr(), null;
  })), i = (n.flags & 15990) !== 0, n.subtreeFlags & 15990 || i) {
    i = dt.transition, dt.transition = null;
    var l = G;
    G = 1;
    var s = W;
    W |= 4, Nu.current = null, zv(e, n), Bm(n, e), iv(xa), Ii = !!ya, xa = ya = null, e.current = n, Nv(n), cg(), W = s, G = l, dt.transition = i;
  } else
    e.current = n;
  if (si && (si = !1, rn = e, Zi = o), i = e.pendingLanes, i === 0 && (cn = null), pg(n.stateNode), He(e, ce()), t !== null)
    for (r = e.onRecoverableError, n = 0; n < t.length; n++)
      o = t[n], r(o.value, { componentStack: o.stack, digest: o.digest });
  if (qi)
    throw qi = !1, e = Da, Da = null, e;
  return Zi & 1 && e.tag !== 0 && sr(), i = e.pendingLanes, i & 1 ? e === Fa ? oo++ : (oo = 0, Fa = e) : oo = 0, vn(), null;
}
function sr() {
  if (rn !== null) {
    var e = Pp(Zi), t = dt.transition, n = G;
    try {
      if (dt.transition = null, G = 16 > e ? 16 : e, rn === null)
        var r = !1;
      else {
        if (e = rn, rn = null, Zi = 0, W & 6)
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
                      no(8, c, i);
                  }
                  var d = c.child;
                  if (d !== null)
                    d.return = c, O = d;
                  else
                    for (; O !== null; ) {
                      c = O;
                      var p = c.sibling, v = c.return;
                      if (Lm(c), c === u) {
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
              var x = i.alternate;
              if (x !== null) {
                var g = x.child;
                if (g !== null) {
                  x.child = null;
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
                      no(9, i, i.return);
                  }
                var m = i.sibling;
                if (m !== null) {
                  m.return = i.return, O = m;
                  break e;
                }
                O = i.return;
              }
        }
        var f = e.current;
        for (O = f; O !== null; ) {
          l = O;
          var h = l.child;
          if (l.subtreeFlags & 2064 && h !== null)
            h.return = l, O = h;
          else
            e:
              for (l = f; O !== null; ) {
                if (s = O, s.flags & 2048)
                  try {
                    switch (s.tag) {
                      case 0:
                      case 11:
                      case 15:
                        xl(9, s);
                    }
                  } catch ($) {
                    ue(s, s.return, $);
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
            Ot.onPostCommitFiberRoot(dl, e);
          } catch {
          }
        r = !0;
      }
      return r;
    } finally {
      G = n, dt.transition = t;
    }
  }
  return !1;
}
function Nd(e, t, n) {
  t = gr(n, t), t = Pm(e, t, 1), e = un(e, t, 1), t = Le(), e !== null && (jo(e, 1, t), He(e, t));
}
function ue(e, t, n) {
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
          e = gr(n, e), e = Tm(t, e, 1), t = un(t, e, 1), e = Le(), t !== null && (jo(t, 1, e), He(t, e));
          break;
        }
      }
      t = t.return;
    }
}
function Fv(e, t, n) {
  var r = e.pingCache;
  r !== null && r.delete(t), t = Le(), e.pingedLanes |= e.suspendedLanes & n, _e === e && (Re & n) === n && (we === 4 || we === 3 && (Re & 130023424) === Re && 500 > ce() - Iu ? En(e, 0) : bu |= n), He(e, t);
}
function Qm(e, t) {
  t === 0 && (e.mode & 1 ? (t = qo, qo <<= 1, !(qo & 130023424) && (qo = 4194304)) : t = 1);
  var n = Le();
  e = Vt(e, t), e !== null && (jo(e, t, n), He(e, n));
}
function Bv(e) {
  var t = e.memoizedState, n = 0;
  t !== null && (n = t.retryLane), Qm(e, n);
}
function Wv(e, t) {
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
  r !== null && r.delete(t), Qm(e, n);
}
var Ym;
Ym = function(e, t, n) {
  if (e !== null)
    if (e.memoizedProps !== t.pendingProps || Ue.current)
      We = !0;
    else {
      if (!(e.lanes & n) && !(t.flags & 128))
        return We = !1, Rv(e, t, n);
      We = !!(e.flags & 131072);
    }
  else
    We = !1, ne && t.flags & 1048576 && Jp(t, Ui, t.index);
  switch (t.lanes = 0, t.tag) {
    case 2:
      var r = t.type;
      wi(e, t), e = t.pendingProps;
      var o = fr(t, be.current);
      lr(t, n), o = Ru(null, t, r, e, o, n);
      var i = Mu();
      return t.flags |= 1, typeof o == "object" && o !== null && typeof o.render == "function" && o.$$typeof === void 0 ? (t.tag = 1, t.memoizedState = null, t.updateQueue = null, Ve(r) ? (i = !0, Bi(t)) : i = !1, t.memoizedState = o.state !== null && o.state !== void 0 ? o.state : null, _u(t), o.updater = yl, t.stateNode = o, o._reactInternals = t, Ta(t, r, e, n), t = Oa(null, t, r, !0, i, n)) : (t.tag = 0, ne && i && vu(t), Ae(null, t, o, n), t = t.child), t;
    case 16:
      r = t.elementType;
      e: {
        switch (wi(e, t), e = t.pendingProps, o = r._init, r = o(r._payload), t.type = r, o = t.tag = Vv(r), e = St(r, e), o) {
          case 0:
            t = Ma(null, t, r, e, n);
            break e;
          case 1:
            t = _d(null, t, r, e, n);
            break e;
          case 11:
            t = Cd(null, t, r, e, n);
            break e;
          case 14:
            t = kd(null, t, r, St(r.type, e), n);
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
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : St(r, o), Ma(e, t, r, o, n);
    case 1:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : St(r, o), _d(e, t, r, o, n);
    case 3:
      e: {
        if (jm(t), e === null)
          throw Error(P(387));
        r = t.pendingProps, i = t.memoizedState, o = i.element, im(e, t), Ki(t, r, null, n);
        var l = t.memoizedState;
        if (r = l.element, i.isDehydrated)
          if (i = { element: r, isDehydrated: !1, cache: l.cache, pendingSuspenseBoundaries: l.pendingSuspenseBoundaries, transitions: l.transitions }, t.updateQueue.baseState = i, t.memoizedState = i, t.flags & 256) {
            o = gr(Error(P(423)), t), t = $d(e, t, r, n, o);
            break e;
          } else if (r !== o) {
            o = gr(Error(P(424)), t), t = $d(e, t, r, n, o);
            break e;
          } else
            for (qe = an(t.stateNode.containerInfo.firstChild), Ze = t, ne = !0, Ct = null, n = rm(t, null, r, n), t.child = n; n; )
              n.flags = n.flags & -3 | 4096, n = n.sibling;
        else {
          if (pr(), r === o) {
            t = Ht(e, t, n);
            break e;
          }
          Ae(e, t, r, n);
        }
        t = t.child;
      }
      return t;
    case 5:
      return lm(t), e === null && $a(t), r = t.type, o = t.pendingProps, i = e !== null ? e.memoizedProps : null, l = o.children, Sa(r, o) ? l = null : i !== null && Sa(r, i) && (t.flags |= 32), Om(e, t), Ae(e, t, l, n), t.child;
    case 6:
      return e === null && $a(t), null;
    case 13:
      return zm(e, t, n);
    case 4:
      return $u(t, t.stateNode.containerInfo), r = t.pendingProps, e === null ? t.child = mr(t, null, r, n) : Ae(e, t, r, n), t.child;
    case 11:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : St(r, o), Cd(e, t, r, o, n);
    case 7:
      return Ae(e, t, t.pendingProps, n), t.child;
    case 8:
      return Ae(e, t, t.pendingProps.children, n), t.child;
    case 12:
      return Ae(e, t, t.pendingProps.children, n), t.child;
    case 10:
      e: {
        if (r = t.type._context, o = t.pendingProps, i = t.memoizedProps, l = o.value, q(Vi, r._currentValue), r._currentValue = l, i !== null)
          if ($t(i.value, l)) {
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
        Ae(e, t, o.children, n), t = t.child;
      }
      return t;
    case 9:
      return o = t.type, r = t.pendingProps.children, lr(t, n), o = ft(o), r = r(o), t.flags |= 1, Ae(e, t, r, n), t.child;
    case 14:
      return r = t.type, o = St(r, t.pendingProps), o = St(r.type, o), kd(e, t, r, o, n);
    case 15:
      return Rm(e, t, t.type, t.pendingProps, n);
    case 17:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : St(r, o), wi(e, t), t.tag = 1, Ve(r) ? (e = !0, Bi(t)) : e = !1, lr(t, n), Em(t, r, o), Ta(t, r, o, n), Oa(null, t, r, !0, e, n);
    case 19:
      return Nm(e, t, n);
    case 22:
      return Mm(e, t, n);
  }
  throw Error(P(156, t.tag));
};
function Xm(e, t) {
  return kp(e, t);
}
function Uv(e, t, n, r) {
  this.tag = e, this.key = n, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.ref = null, this.pendingProps = t, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = r, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
}
function ut(e, t, n, r) {
  return new Uv(e, t, n, r);
}
function Fu(e) {
  return e = e.prototype, !(!e || !e.isReactComponent);
}
function Vv(e) {
  if (typeof e == "function")
    return Fu(e) ? 1 : 0;
  if (e != null) {
    if (e = e.$$typeof, e === iu)
      return 11;
    if (e === lu)
      return 14;
  }
  return 2;
}
function fn(e, t) {
  var n = e.alternate;
  return n === null ? (n = ut(e.tag, t, e.key, e.mode), n.elementType = e.elementType, n.type = e.type, n.stateNode = e.stateNode, n.alternate = e, e.alternate = n) : (n.pendingProps = t, n.type = e.type, n.flags = 0, n.subtreeFlags = 0, n.deletions = null), n.flags = e.flags & 14680064, n.childLanes = e.childLanes, n.lanes = e.lanes, n.child = e.child, n.memoizedProps = e.memoizedProps, n.memoizedState = e.memoizedState, n.updateQueue = e.updateQueue, t = e.dependencies, n.dependencies = t === null ? null : { lanes: t.lanes, firstContext: t.firstContext }, n.sibling = e.sibling, n.index = e.index, n.ref = e.ref, n;
}
function _i(e, t, n, r, o, i) {
  var l = 2;
  if (r = e, typeof e == "function")
    Fu(e) && (l = 1);
  else if (typeof e == "string")
    l = 5;
  else
    e:
      switch (e) {
        case Hn:
          return Pn(n.children, o, i, t);
        case ou:
          l = 8, o |= 8;
          break;
        case Zs:
          return e = ut(12, n, t, o | 2), e.elementType = Zs, e.lanes = i, e;
        case Js:
          return e = ut(13, n, t, o), e.elementType = Js, e.lanes = i, e;
        case ea:
          return e = ut(19, n, t, o), e.elementType = ea, e.lanes = i, e;
        case lp:
          return wl(n, o, i, t);
        default:
          if (typeof e == "object" && e !== null)
            switch (e.$$typeof) {
              case op:
                l = 10;
                break e;
              case ip:
                l = 9;
                break e;
              case iu:
                l = 11;
                break e;
              case lu:
                l = 14;
                break e;
              case Zt:
                l = 16, r = null;
                break e;
            }
          throw Error(P(130, e == null ? e : typeof e, ""));
      }
  return t = ut(l, n, t, o), t.elementType = e, t.type = r, t.lanes = i, t;
}
function Pn(e, t, n, r) {
  return e = ut(7, e, r, t), e.lanes = n, e;
}
function wl(e, t, n, r) {
  return e = ut(22, e, r, t), e.elementType = lp, e.lanes = n, e.stateNode = { isHidden: !1 }, e;
}
function As(e, t, n) {
  return e = ut(6, e, null, t), e.lanes = n, e;
}
function Ls(e, t, n) {
  return t = ut(4, e.children !== null ? e.children : [], e.key, t), t.lanes = n, t.stateNode = { containerInfo: e.containerInfo, pendingChildren: null, implementation: e.implementation }, t;
}
function Hv(e, t, n, r, o) {
  this.tag = t, this.containerInfo = e, this.finishedWork = this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.pendingContext = this.context = null, this.callbackPriority = 0, this.eventTimes = ys(0), this.expirationTimes = ys(-1), this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = ys(0), this.identifierPrefix = r, this.onRecoverableError = o, this.mutableSourceEagerHydrationData = null;
}
function Bu(e, t, n, r, o, i, l, s, a) {
  return e = new Hv(e, t, n, s, a), t === 1 ? (t = 1, i === !0 && (t |= 8)) : t = 0, i = ut(3, null, null, t), e.current = i, i.stateNode = e, i.memoizedState = { element: r, isDehydrated: n, cache: null, transitions: null, pendingSuspenseBoundaries: null }, _u(i), e;
}
function Kv(e, t, n) {
  var r = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
  return { $$typeof: Vn, key: r == null ? null : "" + r, children: e, containerInfo: t, implementation: n };
}
function qm(e) {
  if (!e)
    return mn;
  e = e._reactInternals;
  e: {
    if (bn(e) !== e || e.tag !== 1)
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
      return qp(e, n, t);
  }
  return t;
}
function Zm(e, t, n, r, o, i, l, s, a) {
  return e = Bu(n, r, !0, e, o, i, l, s, a), e.context = qm(null), n = e.current, r = Le(), o = dn(n), i = Bt(r, o), i.callback = t ?? null, un(n, i, o), e.current.lanes = o, jo(e, o, r), He(e, r), e;
}
function Cl(e, t, n, r) {
  var o = t.current, i = Le(), l = dn(o);
  return n = qm(n), t.context === null ? t.context = n : t.pendingContext = n, t = Bt(i, l), t.payload = { element: e }, r = r === void 0 ? null : r, r !== null && (t.callback = r), e = un(o, t, l), e !== null && (_t(e, o, l, i), yi(e, o, l)), l;
}
function el(e) {
  if (e = e.current, !e.child)
    return null;
  switch (e.child.tag) {
    case 5:
      return e.child.stateNode;
    default:
      return e.child.stateNode;
  }
}
function bd(e, t) {
  if (e = e.memoizedState, e !== null && e.dehydrated !== null) {
    var n = e.retryLane;
    e.retryLane = n !== 0 && n < t ? n : t;
  }
}
function Wu(e, t) {
  bd(e, t), (e = e.alternate) && bd(e, t);
}
function Gv() {
  return null;
}
var Jm = typeof reportError == "function" ? reportError : function(e) {
  console.error(e);
};
function Uu(e) {
  this._internalRoot = e;
}
kl.prototype.render = Uu.prototype.render = function(e) {
  var t = this._internalRoot;
  if (t === null)
    throw Error(P(409));
  Cl(e, t, null, null);
};
kl.prototype.unmount = Uu.prototype.unmount = function() {
  var e = this._internalRoot;
  if (e !== null) {
    this._internalRoot = null;
    var t = e.containerInfo;
    jn(function() {
      Cl(null, e, null, null);
    }), t[Ut] = null;
  }
};
function kl(e) {
  this._internalRoot = e;
}
kl.prototype.unstable_scheduleHydration = function(e) {
  if (e) {
    var t = Mp();
    e = { blockedOn: null, target: e, priority: t };
    for (var n = 0; n < en.length && t !== 0 && t < en[n].priority; n++)
      ;
    en.splice(n, 0, e), n === 0 && jp(e);
  }
};
function Vu(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11);
}
function _l(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11 && (e.nodeType !== 8 || e.nodeValue !== " react-mount-point-unstable "));
}
function Id() {
}
function Qv(e, t, n, r, o) {
  if (o) {
    if (typeof r == "function") {
      var i = r;
      r = function() {
        var u = el(l);
        i.call(u);
      };
    }
    var l = Zm(t, r, e, 0, null, !1, !1, "", Id);
    return e._reactRootContainer = l, e[Ut] = l.current, ho(e.nodeType === 8 ? e.parentNode : e), jn(), l;
  }
  for (; o = e.lastChild; )
    e.removeChild(o);
  if (typeof r == "function") {
    var s = r;
    r = function() {
      var u = el(a);
      s.call(u);
    };
  }
  var a = Bu(e, 0, !1, null, null, !1, !1, "", Id);
  return e._reactRootContainer = a, e[Ut] = a.current, ho(e.nodeType === 8 ? e.parentNode : e), jn(function() {
    Cl(t, a, n, r);
  }), a;
}
function $l(e, t, n, r, o) {
  var i = n._reactRootContainer;
  if (i) {
    var l = i;
    if (typeof o == "function") {
      var s = o;
      o = function() {
        var a = el(l);
        s.call(a);
      };
    }
    Cl(t, l, e, o);
  } else
    l = Qv(n, t, e, o, r);
  return el(l);
}
Tp = function(e) {
  switch (e.tag) {
    case 3:
      var t = e.stateNode;
      if (t.current.memoizedState.isDehydrated) {
        var n = Gr(t.pendingLanes);
        n !== 0 && (uu(t, n | 1), He(t, ce()), !(W & 6) && (vr = ce() + 500, vn()));
      }
      break;
    case 13:
      jn(function() {
        var r = Vt(e, 1);
        if (r !== null) {
          var o = Le();
          _t(r, e, 1, o);
        }
      }), Wu(e, 1);
  }
};
cu = function(e) {
  if (e.tag === 13) {
    var t = Vt(e, 134217728);
    if (t !== null) {
      var n = Le();
      _t(t, e, 134217728, n);
    }
    Wu(e, 134217728);
  }
};
Rp = function(e) {
  if (e.tag === 13) {
    var t = dn(e), n = Vt(e, t);
    if (n !== null) {
      var r = Le();
      _t(n, e, t, r);
    }
    Wu(e, t);
  }
};
Mp = function() {
  return G;
};
Op = function(e, t) {
  var n = G;
  try {
    return G = e, t();
  } finally {
    G = n;
  }
};
ca = function(e, t, n) {
  switch (t) {
    case "input":
      if (ra(e, n), t = n.name, n.type === "radio" && t != null) {
        for (n = e; n.parentNode; )
          n = n.parentNode;
        for (n = n.querySelectorAll("input[name=" + JSON.stringify("" + t) + '][type="radio"]'), t = 0; t < n.length; t++) {
          var r = n[t];
          if (r !== e && r.form === e.form) {
            var o = hl(r);
            if (!o)
              throw Error(P(90));
            ap(r), ra(r, o);
          }
        }
      }
      break;
    case "textarea":
      cp(e, n);
      break;
    case "select":
      t = n.value, t != null && nr(e, !!n.multiple, t, !1);
  }
};
vp = Au;
yp = jn;
var Yv = { usingClientEntryPoint: !1, Events: [No, Yn, hl, hp, gp, Au] }, Fr = { findFiberByHostInstance: Cn, bundleType: 0, version: "18.3.1", rendererPackageName: "react-dom" }, Xv = { bundleType: Fr.bundleType, version: Fr.version, rendererPackageName: Fr.rendererPackageName, rendererConfig: Fr.rendererConfig, overrideHookState: null, overrideHookStateDeletePath: null, overrideHookStateRenamePath: null, overrideProps: null, overridePropsDeletePath: null, overridePropsRenamePath: null, setErrorHandler: null, setSuspenseHandler: null, scheduleUpdate: null, currentDispatcherRef: Gt.ReactCurrentDispatcher, findHostInstanceByFiber: function(e) {
  return e = wp(e), e === null ? null : e.stateNode;
}, findFiberByHostInstance: Fr.findFiberByHostInstance || Gv, findHostInstancesForRefresh: null, scheduleRefresh: null, scheduleRoot: null, setRefreshHandler: null, getCurrentFiber: null, reconcilerVersion: "18.3.1-next-f1338f8080-20240426" };
if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u") {
  var ai = __REACT_DEVTOOLS_GLOBAL_HOOK__;
  if (!ai.isDisabled && ai.supportsFiber)
    try {
      dl = ai.inject(Xv), Ot = ai;
    } catch {
    }
}
tt.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = Yv;
tt.createPortal = function(e, t) {
  var n = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
  if (!Vu(t))
    throw Error(P(200));
  return Kv(e, t, null, n);
};
tt.createRoot = function(e, t) {
  if (!Vu(e))
    throw Error(P(299));
  var n = !1, r = "", o = Jm;
  return t != null && (t.unstable_strictMode === !0 && (n = !0), t.identifierPrefix !== void 0 && (r = t.identifierPrefix), t.onRecoverableError !== void 0 && (o = t.onRecoverableError)), t = Bu(e, 1, !1, null, null, n, !1, r, o), e[Ut] = t.current, ho(e.nodeType === 8 ? e.parentNode : e), new Uu(t);
};
tt.findDOMNode = function(e) {
  if (e == null)
    return null;
  if (e.nodeType === 1)
    return e;
  var t = e._reactInternals;
  if (t === void 0)
    throw typeof e.render == "function" ? Error(P(188)) : (e = Object.keys(e).join(","), Error(P(268, e)));
  return e = wp(t), e = e === null ? null : e.stateNode, e;
};
tt.flushSync = function(e) {
  return jn(e);
};
tt.hydrate = function(e, t, n) {
  if (!_l(t))
    throw Error(P(200));
  return $l(null, e, t, !0, n);
};
tt.hydrateRoot = function(e, t, n) {
  if (!Vu(e))
    throw Error(P(405));
  var r = n != null && n.hydratedSources || null, o = !1, i = "", l = Jm;
  if (n != null && (n.unstable_strictMode === !0 && (o = !0), n.identifierPrefix !== void 0 && (i = n.identifierPrefix), n.onRecoverableError !== void 0 && (l = n.onRecoverableError)), t = Zm(t, null, e, 1, n ?? null, o, !1, i, l), e[Ut] = t.current, ho(e), r)
    for (e = 0; e < r.length; e++)
      n = r[e], o = n._getVersion, o = o(n._source), t.mutableSourceEagerHydrationData == null ? t.mutableSourceEagerHydrationData = [n, o] : t.mutableSourceEagerHydrationData.push(
        n,
        o
      );
  return new kl(t);
};
tt.render = function(e, t, n) {
  if (!_l(t))
    throw Error(P(200));
  return $l(null, e, t, !1, n);
};
tt.unmountComponentAtNode = function(e) {
  if (!_l(e))
    throw Error(P(40));
  return e._reactRootContainer ? (jn(function() {
    $l(null, null, e, !1, function() {
      e._reactRootContainer = null, e[Ut] = null;
    });
  }), !0) : !1;
};
tt.unstable_batchedUpdates = Au;
tt.unstable_renderSubtreeIntoContainer = function(e, t, n, r) {
  if (!_l(n))
    throw Error(P(200));
  if (e == null || e._reactInternals === void 0)
    throw Error(P(38));
  return $l(e, t, n, !1, r);
};
tt.version = "18.3.1-next-f1338f8080-20240426";
function eh() {
  if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function"))
    try {
      __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(eh);
    } catch (e) {
      console.error(e);
    }
}
eh(), ep.exports = tt;
var qv = ep.exports, Ad = qv;
Xs.createRoot = Ad.createRoot, Xs.hydrateRoot = Ad.hydrateRoot;
function _o(e) {
  let t = "https://mui.com/production-error/?code=" + e;
  for (let n = 1; n < arguments.length; n += 1)
    t += "&args[]=" + encodeURIComponent(arguments[n]);
  return "Minified MUI error #" + e + "; visit " + t + " for the full message.";
}
const Zv = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: _o
}, Symbol.toStringTag, { value: "Module" })), yr = "$$material";
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
var Jv = !1;
function ey(e) {
  if (e.sheet)
    return e.sheet;
  for (var t = 0; t < document.styleSheets.length; t++)
    if (document.styleSheets[t].ownerNode === e)
      return document.styleSheets[t];
}
function ty(e) {
  var t = document.createElement("style");
  return t.setAttribute("data-emotion", e.key), e.nonce !== void 0 && t.setAttribute("nonce", e.nonce), t.appendChild(document.createTextNode("")), t.setAttribute("data-s", ""), t;
}
var ny = /* @__PURE__ */ function() {
  function e(n) {
    var r = this;
    this._insertTag = function(o) {
      var i;
      r.tags.length === 0 ? r.insertionPoint ? i = r.insertionPoint.nextSibling : r.prepend ? i = r.container.firstChild : i = r.before : i = r.tags[r.tags.length - 1].nextSibling, r.container.insertBefore(o, i), r.tags.push(o);
    }, this.isSpeedy = n.speedy === void 0 ? !Jv : n.speedy, this.tags = [], this.ctr = 0, this.nonce = n.nonce, this.key = n.key, this.container = n.container, this.prepend = n.prepend, this.insertionPoint = n.insertionPoint, this.before = null;
  }
  var t = e.prototype;
  return t.hydrate = function(r) {
    r.forEach(this._insertTag);
  }, t.insert = function(r) {
    this.ctr % (this.isSpeedy ? 65e3 : 1) === 0 && this._insertTag(ty(this));
    var o = this.tags[this.tags.length - 1];
    if (this.isSpeedy) {
      var i = ey(o);
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
}(), ze = "-ms-", tl = "-moz-", V = "-webkit-", th = "comm", Hu = "rule", Ku = "decl", ry = "@import", nh = "@keyframes", oy = "@layer", iy = Math.abs, El = String.fromCharCode, ly = Object.assign;
function sy(e, t) {
  return Te(e, 0) ^ 45 ? (((t << 2 ^ Te(e, 0)) << 2 ^ Te(e, 1)) << 2 ^ Te(e, 2)) << 2 ^ Te(e, 3) : 0;
}
function rh(e) {
  return e.trim();
}
function ay(e, t) {
  return (e = t.exec(e)) ? e[0] : e;
}
function H(e, t, n) {
  return e.replace(t, n);
}
function Ua(e, t) {
  return e.indexOf(t);
}
function Te(e, t) {
  return e.charCodeAt(t) | 0;
}
function $o(e, t, n) {
  return e.slice(t, n);
}
function Tt(e) {
  return e.length;
}
function Gu(e) {
  return e.length;
}
function ui(e, t) {
  return t.push(e), e;
}
function uy(e, t) {
  return e.map(t).join("");
}
var Pl = 1, xr = 1, oh = 0, Ke = 0, he = 0, $r = "";
function Tl(e, t, n, r, o, i, l) {
  return { value: e, root: t, parent: n, type: r, props: o, children: i, line: Pl, column: xr, length: l, return: "" };
}
function Br(e, t) {
  return ly(Tl("", null, null, "", null, null, 0), e, { length: -e.length }, t);
}
function cy() {
  return he;
}
function dy() {
  return he = Ke > 0 ? Te($r, --Ke) : 0, xr--, he === 10 && (xr = 1, Pl--), he;
}
function Je() {
  return he = Ke < oh ? Te($r, Ke++) : 0, xr++, he === 10 && (xr = 1, Pl++), he;
}
function zt() {
  return Te($r, Ke);
}
function $i() {
  return Ke;
}
function Io(e, t) {
  return $o($r, e, t);
}
function Eo(e) {
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
function ih(e) {
  return Pl = xr = 1, oh = Tt($r = e), Ke = 0, [];
}
function lh(e) {
  return $r = "", e;
}
function Ei(e) {
  return rh(Io(Ke - 1, Va(e === 91 ? e + 2 : e === 40 ? e + 1 : e)));
}
function fy(e) {
  for (; (he = zt()) && he < 33; )
    Je();
  return Eo(e) > 2 || Eo(he) > 3 ? "" : " ";
}
function py(e, t) {
  for (; --t && Je() && !(he < 48 || he > 102 || he > 57 && he < 65 || he > 70 && he < 97); )
    ;
  return Io(e, $i() + (t < 6 && zt() == 32 && Je() == 32));
}
function Va(e) {
  for (; Je(); )
    switch (he) {
      case e:
        return Ke;
      case 34:
      case 39:
        e !== 34 && e !== 39 && Va(he);
        break;
      case 40:
        e === 41 && Va(e);
        break;
      case 92:
        Je();
        break;
    }
  return Ke;
}
function my(e, t) {
  for (; Je() && e + he !== 47 + 10; )
    if (e + he === 42 + 42 && zt() === 47)
      break;
  return "/*" + Io(t, Ke - 1) + "*" + El(e === 47 ? e : Je());
}
function hy(e) {
  for (; !Eo(zt()); )
    Je();
  return Io(e, Ke);
}
function gy(e) {
  return lh(Pi("", null, null, null, [""], e = ih(e), 0, [0], e));
}
function Pi(e, t, n, r, o, i, l, s, a) {
  for (var u = 0, c = 0, d = l, p = 0, v = 0, x = 0, g = 1, E = 1, m = 1, f = 0, h = "", S = o, $ = i, k = r, C = h; E; )
    switch (x = f, f = Je()) {
      case 40:
        if (x != 108 && Te(C, d - 1) == 58) {
          Ua(C += H(Ei(f), "&", "&\f"), "&\f") != -1 && (m = -1);
          break;
        }
      case 34:
      case 39:
      case 91:
        C += Ei(f);
        break;
      case 9:
      case 10:
      case 13:
      case 32:
        C += fy(x);
        break;
      case 92:
        C += py($i() - 1, 7);
        continue;
      case 47:
        switch (zt()) {
          case 42:
          case 47:
            ui(vy(my(Je(), $i()), t, n), a);
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
        switch (f) {
          case 0:
          case 125:
            E = 0;
          case 59 + c:
            m == -1 && (C = H(C, /\f/g, "")), v > 0 && Tt(C) - d && ui(v > 32 ? Dd(C + ";", r, n, d - 1) : Dd(H(C, " ", "") + ";", r, n, d - 2), a);
            break;
          case 59:
            C += ";";
          default:
            if (ui(k = Ld(C, t, n, u, c, o, s, h, S = [], $ = [], d), i), f === 123)
              if (c === 0)
                Pi(C, t, k, k, S, i, d, s, $);
              else
                switch (p === 99 && Te(C, 3) === 110 ? 100 : p) {
                  case 100:
                  case 108:
                  case 109:
                  case 115:
                    Pi(e, k, k, r && ui(Ld(e, k, k, 0, 0, o, s, h, o, S = [], d), $), o, $, d, s, r ? S : $);
                    break;
                  default:
                    Pi(C, k, k, k, [""], $, 0, s, $);
                }
        }
        u = c = v = 0, g = m = 1, h = C = "", d = l;
        break;
      case 58:
        d = 1 + Tt(C), v = x;
      default:
        if (g < 1) {
          if (f == 123)
            --g;
          else if (f == 125 && g++ == 0 && dy() == 125)
            continue;
        }
        switch (C += El(f), f * g) {
          case 38:
            m = c > 0 ? 1 : (C += "\f", -1);
            break;
          case 44:
            s[u++] = (Tt(C) - 1) * m, m = 1;
            break;
          case 64:
            zt() === 45 && (C += Ei(Je())), p = zt(), c = d = Tt(h = C += hy($i())), f++;
            break;
          case 45:
            x === 45 && Tt(C) == 2 && (g = 0);
        }
    }
  return i;
}
function Ld(e, t, n, r, o, i, l, s, a, u, c) {
  for (var d = o - 1, p = o === 0 ? i : [""], v = Gu(p), x = 0, g = 0, E = 0; x < r; ++x)
    for (var m = 0, f = $o(e, d + 1, d = iy(g = l[x])), h = e; m < v; ++m)
      (h = rh(g > 0 ? p[m] + " " + f : H(f, /&\f/g, p[m]))) && (a[E++] = h);
  return Tl(e, t, n, o === 0 ? Hu : s, a, u, c);
}
function vy(e, t, n) {
  return Tl(e, t, n, th, El(cy()), $o(e, 2, -2), 0);
}
function Dd(e, t, n, r) {
  return Tl(e, t, n, Ku, $o(e, 0, r), $o(e, r + 1, -1), r);
}
function ar(e, t) {
  for (var n = "", r = Gu(e), o = 0; o < r; o++)
    n += t(e[o], o, e, t) || "";
  return n;
}
function yy(e, t, n, r) {
  switch (e.type) {
    case oy:
      if (e.children.length)
        break;
    case ry:
    case Ku:
      return e.return = e.return || e.value;
    case th:
      return "";
    case nh:
      return e.return = e.value + "{" + ar(e.children, r) + "}";
    case Hu:
      e.value = e.props.join(",");
  }
  return Tt(n = ar(e.children, r)) ? e.return = e.value + "{" + n + "}" : "";
}
function xy(e) {
  var t = Gu(e);
  return function(n, r, o, i) {
    for (var l = "", s = 0; s < t; s++)
      l += e[s](n, r, o, i) || "";
    return l;
  };
}
function Sy(e) {
  return function(t) {
    t.root || (t = t.return) && e(t);
  };
}
function sh(e) {
  var t = /* @__PURE__ */ Object.create(null);
  return function(n) {
    return t[n] === void 0 && (t[n] = e(n)), t[n];
  };
}
var wy = function(t, n, r) {
  for (var o = 0, i = 0; o = i, i = zt(), o === 38 && i === 12 && (n[r] = 1), !Eo(i); )
    Je();
  return Io(t, Ke);
}, Cy = function(t, n) {
  var r = -1, o = 44;
  do
    switch (Eo(o)) {
      case 0:
        o === 38 && zt() === 12 && (n[r] = 1), t[r] += wy(Ke - 1, n, r);
        break;
      case 2:
        t[r] += Ei(o);
        break;
      case 4:
        if (o === 44) {
          t[++r] = zt() === 58 ? "&\f" : "", n[r] = t[r].length;
          break;
        }
      default:
        t[r] += El(o);
    }
  while (o = Je());
  return t;
}, ky = function(t, n) {
  return lh(Cy(ih(t), n));
}, Fd = /* @__PURE__ */ new WeakMap(), _y = function(t) {
  if (!(t.type !== "rule" || !t.parent || // positive .length indicates that this rule contains pseudo
  // negative .length indicates that this rule has been already prefixed
  t.length < 1)) {
    for (var n = t.value, r = t.parent, o = t.column === r.column && t.line === r.line; r.type !== "rule"; )
      if (r = r.parent, !r)
        return;
    if (!(t.props.length === 1 && n.charCodeAt(0) !== 58 && !Fd.get(r)) && !o) {
      Fd.set(t, !0);
      for (var i = [], l = ky(n, i), s = r.props, a = 0, u = 0; a < l.length; a++)
        for (var c = 0; c < s.length; c++, u++)
          t.props[u] = i[a] ? l[a].replace(/&\f/g, s[c]) : s[c] + " " + l[a];
    }
  }
}, $y = function(t) {
  if (t.type === "decl") {
    var n = t.value;
    // charcode for l
    n.charCodeAt(0) === 108 && // charcode for b
    n.charCodeAt(2) === 98 && (t.return = "", t.value = "");
  }
};
function ah(e, t) {
  switch (sy(e, t)) {
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
      return V + e + tl + e + ze + e + e;
    case 6828:
    case 4268:
      return V + e + ze + e + e;
    case 6165:
      return V + e + ze + "flex-" + e + e;
    case 5187:
      return V + e + H(e, /(\w+).+(:[^]+)/, V + "box-$1$2" + ze + "flex-$1$2") + e;
    case 5443:
      return V + e + ze + "flex-item-" + H(e, /flex-|-self/, "") + e;
    case 4675:
      return V + e + ze + "flex-line-pack" + H(e, /align-content|flex-|-self/, "") + e;
    case 5548:
      return V + e + ze + H(e, "shrink", "negative") + e;
    case 5292:
      return V + e + ze + H(e, "basis", "preferred-size") + e;
    case 6060:
      return V + "box-" + H(e, "-grow", "") + V + e + ze + H(e, "grow", "positive") + e;
    case 4554:
      return V + H(e, /([^-])(transform)/g, "$1" + V + "$2") + e;
    case 6187:
      return H(H(H(e, /(zoom-|grab)/, V + "$1"), /(image-set)/, V + "$1"), e, "") + e;
    case 5495:
    case 3959:
      return H(e, /(image-set\([^]*)/, V + "$1$`$1");
    case 4968:
      return H(H(e, /(.+:)(flex-)?(.*)/, V + "box-pack:$3" + ze + "flex-pack:$3"), /s.+-b[^;]+/, "justify") + V + e + e;
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
            return H(e, /(.+:)(.+)-([^]+)/, "$1" + V + "$2-$3$1" + tl + (Te(e, t + 3) == 108 ? "$3" : "$2-$3")) + e;
          case 115:
            return ~Ua(e, "stretch") ? ah(H(e, "stretch", "fill-available"), t) + e : e;
        }
      break;
    case 4949:
      if (Te(e, t + 1) !== 115)
        break;
    case 6444:
      switch (Te(e, Tt(e) - 3 - (~Ua(e, "!important") && 10))) {
        case 107:
          return H(e, ":", ":" + V) + e;
        case 101:
          return H(e, /(.+:)([^;!]+)(;|!.+)?/, "$1" + V + (Te(e, 14) === 45 ? "inline-" : "") + "box$3$1" + V + "$2$3$1" + ze + "$2box$3") + e;
      }
      break;
    case 5936:
      switch (Te(e, t + 11)) {
        case 114:
          return V + e + ze + H(e, /[svh]\w+-[tblr]{2}/, "tb") + e;
        case 108:
          return V + e + ze + H(e, /[svh]\w+-[tblr]{2}/, "tb-rl") + e;
        case 45:
          return V + e + ze + H(e, /[svh]\w+-[tblr]{2}/, "lr") + e;
      }
      return V + e + ze + e + e;
  }
  return e;
}
var Ey = function(t, n, r, o) {
  if (t.length > -1 && !t.return)
    switch (t.type) {
      case Ku:
        t.return = ah(t.value, t.length);
        break;
      case nh:
        return ar([Br(t, {
          value: H(t.value, "@", "@" + V)
        })], o);
      case Hu:
        if (t.length)
          return uy(t.props, function(i) {
            switch (ay(i, /(::plac\w+|:read-\w+)/)) {
              case ":read-only":
              case ":read-write":
                return ar([Br(t, {
                  props: [H(i, /:(read-\w+)/, ":" + tl + "$1")]
                })], o);
              case "::placeholder":
                return ar([Br(t, {
                  props: [H(i, /:(plac\w+)/, ":" + V + "input-$1")]
                }), Br(t, {
                  props: [H(i, /:(plac\w+)/, ":" + tl + "$1")]
                }), Br(t, {
                  props: [H(i, /:(plac\w+)/, ze + "input-$1")]
                })], o);
            }
            return "";
          });
    }
}, Py = [Ey], uh = function(t) {
  var n = t.key;
  if (n === "css") {
    var r = document.querySelectorAll("style[data-emotion]:not([data-s])");
    Array.prototype.forEach.call(r, function(g) {
      var E = g.getAttribute("data-emotion");
      E.indexOf(" ") !== -1 && (document.head.appendChild(g), g.setAttribute("data-s", ""));
    });
  }
  var o = t.stylisPlugins || Py, i = {}, l, s = [];
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
  var a, u = [_y, $y];
  {
    var c, d = [yy, Sy(function(g) {
      c.insert(g);
    })], p = xy(u.concat(o, d)), v = function(E) {
      return ar(gy(E), p);
    };
    a = function(E, m, f, h) {
      c = f, v(E ? E + "{" + m.styles + "}" : m.styles), h && (x.inserted[m.name] = !0);
    };
  }
  var x = {
    key: n,
    sheet: new ny({
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
  return x.sheet.hydrate(s), x;
}, ch = { exports: {} }, Q = {};
/** @license React v16.13.1
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var $e = typeof Symbol == "function" && Symbol.for, Qu = $e ? Symbol.for("react.element") : 60103, Yu = $e ? Symbol.for("react.portal") : 60106, Rl = $e ? Symbol.for("react.fragment") : 60107, Ml = $e ? Symbol.for("react.strict_mode") : 60108, Ol = $e ? Symbol.for("react.profiler") : 60114, jl = $e ? Symbol.for("react.provider") : 60109, zl = $e ? Symbol.for("react.context") : 60110, Xu = $e ? Symbol.for("react.async_mode") : 60111, Nl = $e ? Symbol.for("react.concurrent_mode") : 60111, bl = $e ? Symbol.for("react.forward_ref") : 60112, Il = $e ? Symbol.for("react.suspense") : 60113, Ty = $e ? Symbol.for("react.suspense_list") : 60120, Al = $e ? Symbol.for("react.memo") : 60115, Ll = $e ? Symbol.for("react.lazy") : 60116, Ry = $e ? Symbol.for("react.block") : 60121, My = $e ? Symbol.for("react.fundamental") : 60117, Oy = $e ? Symbol.for("react.responder") : 60118, jy = $e ? Symbol.for("react.scope") : 60119;
function rt(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Qu:
        switch (e = e.type, e) {
          case Xu:
          case Nl:
          case Rl:
          case Ol:
          case Ml:
          case Il:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case zl:
              case bl:
              case Ll:
              case Al:
              case jl:
                return e;
              default:
                return t;
            }
        }
      case Yu:
        return t;
    }
  }
}
function dh(e) {
  return rt(e) === Nl;
}
Q.AsyncMode = Xu;
Q.ConcurrentMode = Nl;
Q.ContextConsumer = zl;
Q.ContextProvider = jl;
Q.Element = Qu;
Q.ForwardRef = bl;
Q.Fragment = Rl;
Q.Lazy = Ll;
Q.Memo = Al;
Q.Portal = Yu;
Q.Profiler = Ol;
Q.StrictMode = Ml;
Q.Suspense = Il;
Q.isAsyncMode = function(e) {
  return dh(e) || rt(e) === Xu;
};
Q.isConcurrentMode = dh;
Q.isContextConsumer = function(e) {
  return rt(e) === zl;
};
Q.isContextProvider = function(e) {
  return rt(e) === jl;
};
Q.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Qu;
};
Q.isForwardRef = function(e) {
  return rt(e) === bl;
};
Q.isFragment = function(e) {
  return rt(e) === Rl;
};
Q.isLazy = function(e) {
  return rt(e) === Ll;
};
Q.isMemo = function(e) {
  return rt(e) === Al;
};
Q.isPortal = function(e) {
  return rt(e) === Yu;
};
Q.isProfiler = function(e) {
  return rt(e) === Ol;
};
Q.isStrictMode = function(e) {
  return rt(e) === Ml;
};
Q.isSuspense = function(e) {
  return rt(e) === Il;
};
Q.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === Rl || e === Nl || e === Ol || e === Ml || e === Il || e === Ty || typeof e == "object" && e !== null && (e.$$typeof === Ll || e.$$typeof === Al || e.$$typeof === jl || e.$$typeof === zl || e.$$typeof === bl || e.$$typeof === My || e.$$typeof === Oy || e.$$typeof === jy || e.$$typeof === Ry);
};
Q.typeOf = rt;
ch.exports = Q;
var zy = ch.exports, fh = zy, Ny = {
  $$typeof: !0,
  render: !0,
  defaultProps: !0,
  displayName: !0,
  propTypes: !0
}, by = {
  $$typeof: !0,
  compare: !0,
  defaultProps: !0,
  displayName: !0,
  propTypes: !0,
  type: !0
}, ph = {};
ph[fh.ForwardRef] = Ny;
ph[fh.Memo] = by;
var Iy = !0;
function mh(e, t, n) {
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
  Iy === !1) && t.registered[o] === void 0 && (t.registered[o] = n.styles);
}, Zu = function(t, n, r) {
  qu(t, n, r);
  var o = t.key + "-" + n.name;
  if (t.inserted[n.name] === void 0) {
    var i = n;
    do
      t.insert(n === i ? "." + o : "", i, t.sheet, !0), i = i.next;
    while (i !== void 0);
  }
};
function Ay(e) {
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
var Ly = {
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
}, Dy = !1, Fy = /[A-Z]|^ms/g, By = /_EMO_([^_]+?)_([^]*?)_EMO_/g, hh = function(t) {
  return t.charCodeAt(1) === 45;
}, Bd = function(t) {
  return t != null && typeof t != "boolean";
}, Ds = /* @__PURE__ */ sh(function(e) {
  return hh(e) ? e : e.replace(Fy, "-$&").toLowerCase();
}), Wd = function(t, n) {
  switch (t) {
    case "animation":
    case "animationName":
      if (typeof n == "string")
        return n.replace(By, function(r, o, i) {
          return Rt = {
            name: o,
            styles: i,
            next: Rt
          }, o;
        });
  }
  return Ly[t] !== 1 && !hh(t) && typeof n == "number" && n !== 0 ? n + "px" : n;
}, Wy = "Component selectors can only be used in conjunction with @emotion/babel-plugin, the swc Emotion plugin, or another Emotion-aware compiler transform.";
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
      return Uy(e, t, n);
    }
    case "function": {
      if (e !== void 0) {
        var a = Rt, u = n(e);
        return Rt = a, Po(e, t, u);
      }
      break;
    }
  }
  var c = n;
  if (t == null)
    return c;
  var d = t[c];
  return d !== void 0 ? d : c;
}
function Uy(e, t, n) {
  var r = "";
  if (Array.isArray(n))
    for (var o = 0; o < n.length; o++)
      r += Po(e, t, n[o]) + ";";
  else
    for (var i in n) {
      var l = n[i];
      if (typeof l != "object") {
        var s = l;
        t != null && t[s] !== void 0 ? r += i + "{" + t[s] + "}" : Bd(s) && (r += Ds(i) + ":" + Wd(i, s) + ";");
      } else {
        if (i === "NO_COMPONENT_SELECTOR" && Dy)
          throw new Error(Wy);
        if (Array.isArray(l) && typeof l[0] == "string" && (t == null || t[l[0]] === void 0))
          for (var a = 0; a < l.length; a++)
            Bd(l[a]) && (r += Ds(i) + ":" + Wd(i, l[a]) + ";");
        else {
          var u = Po(e, t, l);
          switch (i) {
            case "animation":
            case "animationName": {
              r += Ds(i) + ":" + u + ";";
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
var Ud = /label:\s*([^\s;{]+)\s*(;|$)/g, Rt;
function Ao(e, t, n) {
  if (e.length === 1 && typeof e[0] == "object" && e[0] !== null && e[0].styles !== void 0)
    return e[0];
  var r = !0, o = "";
  Rt = void 0;
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
  Ud.lastIndex = 0;
  for (var u = "", c; (c = Ud.exec(o)) !== null; )
    u += "-" + c[1];
  var d = Ay(o) + u;
  return {
    name: d,
    styles: o,
    next: Rt
  };
}
var Vy = function(t) {
  return t();
}, gh = Ys["useInsertionEffect"] ? Ys["useInsertionEffect"] : !1, vh = gh || Vy, Vd = gh || _.useLayoutEffect, Hy = !1, yh = /* @__PURE__ */ _.createContext(
  // we're doing this to avoid preconstruct's dead code elimination in this one case
  // because this module is primarily intended for the browser and node
  // but it's also required in react native and similar environments sometimes
  // and we could have a special build just for that
  // but this is much easier and the native packages
  // might use a different theme context in the future anyway
  typeof HTMLElement < "u" ? /* @__PURE__ */ uh({
    key: "css"
  }) : null
), Ky = yh.Provider, Ju = function(t) {
  return /* @__PURE__ */ _.forwardRef(function(n, r) {
    var o = _.useContext(yh);
    return t(n, o, r);
  });
}, Er = /* @__PURE__ */ _.createContext({}), ec = {}.hasOwnProperty, Ha = "__EMOTION_TYPE_PLEASE_DO_NOT_USE__", Gy = function(t, n) {
  var r = {};
  for (var o in n)
    ec.call(n, o) && (r[o] = n[o]);
  return r[Ha] = t, r;
}, Qy = function(t) {
  var n = t.cache, r = t.serialized, o = t.isStringTag;
  return qu(n, r, o), vh(function() {
    return Zu(n, r, o);
  }), null;
}, Yy = /* @__PURE__ */ Ju(function(e, t, n) {
  var r = e.css;
  typeof r == "string" && t.registered[r] !== void 0 && (r = t.registered[r]);
  var o = e[Ha], i = [r], l = "";
  typeof e.className == "string" ? l = mh(t.registered, i, e.className) : e.className != null && (l = e.className + " ");
  var s = Ao(i, void 0, _.useContext(Er));
  l += t.key + "-" + s.name;
  var a = {};
  for (var u in e)
    ec.call(e, u) && u !== "css" && u !== Ha && !Hy && (a[u] = e[u]);
  return a.className = l, n && (a.ref = n), /* @__PURE__ */ _.createElement(_.Fragment, null, /* @__PURE__ */ _.createElement(Qy, {
    cache: t,
    serialized: s,
    isStringTag: typeof o == "string"
  }), /* @__PURE__ */ _.createElement(o, a));
}), Xy = Yy, Fs = { exports: {} }, Hd;
function xh() {
  return Hd || (Hd = 1, function(e) {
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
  }(Fs)), Fs.exports;
}
xh();
var Kd = function(t, n) {
  var r = arguments;
  if (n == null || !ec.call(n, "css"))
    return _.createElement.apply(void 0, r);
  var o = r.length, i = new Array(o);
  i[0] = Xy, i[1] = Gy(t, n);
  for (var l = 2; l < o; l++)
    i[l] = r[l];
  return _.createElement.apply(null, i);
};
(function(e) {
  var t;
  t || (t = e.JSX || (e.JSX = {}));
})(Kd || (Kd = {}));
var qy = /* @__PURE__ */ Ju(function(e, t) {
  var n = e.styles, r = Ao([n], void 0, _.useContext(Er)), o = _.useRef();
  return Vd(function() {
    var i = t.key + "-global", l = new t.sheet.constructor({
      key: i,
      nonce: t.sheet.nonce,
      container: t.sheet.container,
      speedy: t.sheet.isSpeedy
    }), s = !1, a = document.querySelector('style[data-emotion="' + i + " " + r.name + '"]');
    return t.sheet.tags.length && (l.before = t.sheet.tags[0]), a !== null && (s = !0, a.setAttribute("data-emotion", i), l.hydrate([a])), o.current = [l, s], function() {
      l.flush();
    };
  }, [t]), Vd(function() {
    var i = o.current, l = i[0], s = i[1];
    if (s) {
      i[1] = !1;
      return;
    }
    if (r.next !== void 0 && Zu(t, r.next, !0), l.tags.length) {
      var a = l.tags[l.tags.length - 1].nextElementSibling;
      l.before = a, l.flush();
    }
    t.insert("", r, l, !1);
  }, [t, r.name]), null;
});
function Dl() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  return Ao(t);
}
function Pr() {
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
var Zy = /^((children|dangerouslySetInnerHTML|key|ref|autoFocus|defaultValue|defaultChecked|innerHTML|suppressContentEditableWarning|suppressHydrationWarning|valueLink|abbr|accept|acceptCharset|accessKey|action|allow|allowUserMedia|allowPaymentRequest|allowFullScreen|allowTransparency|alt|async|autoComplete|autoPlay|capture|cellPadding|cellSpacing|challenge|charSet|checked|cite|classID|className|cols|colSpan|content|contentEditable|contextMenu|controls|controlsList|coords|crossOrigin|data|dateTime|decoding|default|defer|dir|disabled|disablePictureInPicture|disableRemotePlayback|download|draggable|encType|enterKeyHint|fetchpriority|fetchPriority|form|formAction|formEncType|formMethod|formNoValidate|formTarget|frameBorder|headers|height|hidden|high|href|hrefLang|htmlFor|httpEquiv|id|inputMode|integrity|is|keyParams|keyType|kind|label|lang|list|loading|loop|low|marginHeight|marginWidth|max|maxLength|media|mediaGroup|method|min|minLength|multiple|muted|name|nonce|noValidate|open|optimum|pattern|placeholder|playsInline|popover|popoverTarget|popoverTargetAction|poster|preload|profile|radioGroup|readOnly|referrerPolicy|rel|required|reversed|role|rows|rowSpan|sandbox|scope|scoped|scrolling|seamless|selected|shape|size|sizes|slot|span|spellCheck|src|srcDoc|srcLang|srcSet|start|step|style|summary|tabIndex|target|title|translate|type|useMap|value|width|wmode|wrap|about|datatype|inlist|prefix|property|resource|typeof|vocab|autoCapitalize|autoCorrect|autoSave|color|incremental|fallback|inert|itemProp|itemScope|itemType|itemID|itemRef|on|option|results|security|unselectable|accentHeight|accumulate|additive|alignmentBaseline|allowReorder|alphabetic|amplitude|arabicForm|ascent|attributeName|attributeType|autoReverse|azimuth|baseFrequency|baselineShift|baseProfile|bbox|begin|bias|by|calcMode|capHeight|clip|clipPathUnits|clipPath|clipRule|colorInterpolation|colorInterpolationFilters|colorProfile|colorRendering|contentScriptType|contentStyleType|cursor|cx|cy|d|decelerate|descent|diffuseConstant|direction|display|divisor|dominantBaseline|dur|dx|dy|edgeMode|elevation|enableBackground|end|exponent|externalResourcesRequired|fill|fillOpacity|fillRule|filter|filterRes|filterUnits|floodColor|floodOpacity|focusable|fontFamily|fontSize|fontSizeAdjust|fontStretch|fontStyle|fontVariant|fontWeight|format|from|fr|fx|fy|g1|g2|glyphName|glyphOrientationHorizontal|glyphOrientationVertical|glyphRef|gradientTransform|gradientUnits|hanging|horizAdvX|horizOriginX|ideographic|imageRendering|in|in2|intercept|k|k1|k2|k3|k4|kernelMatrix|kernelUnitLength|kerning|keyPoints|keySplines|keyTimes|lengthAdjust|letterSpacing|lightingColor|limitingConeAngle|local|markerEnd|markerMid|markerStart|markerHeight|markerUnits|markerWidth|mask|maskContentUnits|maskUnits|mathematical|mode|numOctaves|offset|opacity|operator|order|orient|orientation|origin|overflow|overlinePosition|overlineThickness|panose1|paintOrder|pathLength|patternContentUnits|patternTransform|patternUnits|pointerEvents|points|pointsAtX|pointsAtY|pointsAtZ|preserveAlpha|preserveAspectRatio|primitiveUnits|r|radius|refX|refY|renderingIntent|repeatCount|repeatDur|requiredExtensions|requiredFeatures|restart|result|rotate|rx|ry|scale|seed|shapeRendering|slope|spacing|specularConstant|specularExponent|speed|spreadMethod|startOffset|stdDeviation|stemh|stemv|stitchTiles|stopColor|stopOpacity|strikethroughPosition|strikethroughThickness|string|stroke|strokeDasharray|strokeDashoffset|strokeLinecap|strokeLinejoin|strokeMiterlimit|strokeOpacity|strokeWidth|surfaceScale|systemLanguage|tableValues|targetX|targetY|textAnchor|textDecoration|textRendering|textLength|to|transform|u1|u2|underlinePosition|underlineThickness|unicode|unicodeBidi|unicodeRange|unitsPerEm|vAlphabetic|vHanging|vIdeographic|vMathematical|values|vectorEffect|version|vertAdvY|vertOriginX|vertOriginY|viewBox|viewTarget|visibility|widths|wordSpacing|writingMode|x|xHeight|x1|x2|xChannelSelector|xlinkActuate|xlinkArcrole|xlinkHref|xlinkRole|xlinkShow|xlinkTitle|xlinkType|xmlBase|xmlns|xmlnsXlink|xmlLang|xmlSpace|y|y1|y2|yChannelSelector|z|zoomAndPan|for|class|autofocus)|(([Dd][Aa][Tt][Aa]|[Aa][Rr][Ii][Aa]|x)-.*))$/, Jy = /* @__PURE__ */ sh(
  function(e) {
    return Zy.test(e) || e.charCodeAt(0) === 111 && e.charCodeAt(1) === 110 && e.charCodeAt(2) < 91;
  }
  /* Z+1 */
), e1 = !1, t1 = Jy, n1 = function(t) {
  return t !== "theme";
}, Gd = function(t) {
  return typeof t == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  t.charCodeAt(0) > 96 ? t1 : n1;
}, Qd = function(t, n, r) {
  var o;
  if (n) {
    var i = n.shouldForwardProp;
    o = t.__emotion_forwardProp && i ? function(l) {
      return t.__emotion_forwardProp(l) && i(l);
    } : i;
  }
  return typeof o != "function" && r && (o = t.__emotion_forwardProp), o;
}, r1 = function(t) {
  var n = t.cache, r = t.serialized, o = t.isStringTag;
  return qu(n, r, o), vh(function() {
    return Zu(n, r, o);
  }), null;
}, o1 = function e(t, n) {
  var r = t.__emotion_real === t, o = r && t.__emotion_base || t, i, l;
  n !== void 0 && (i = n.label, l = n.target);
  var s = Qd(t, n, r), a = s || Gd(o), u = !a("as");
  return function() {
    var c = arguments, d = r && t.__emotion_styles !== void 0 ? t.__emotion_styles.slice(0) : [];
    if (i !== void 0 && d.push("label:" + i + ";"), c[0] == null || c[0].raw === void 0)
      d.push.apply(d, c);
    else {
      var p = c[0];
      d.push(p[0]);
      for (var v = c.length, x = 1; x < v; x++)
        d.push(c[x], p[x]);
    }
    var g = Ju(function(E, m, f) {
      var h = u && E.as || o, S = "", $ = [], k = E;
      if (E.theme == null) {
        k = {};
        for (var C in E)
          k[C] = E[C];
        k.theme = _.useContext(Er);
      }
      typeof E.className == "string" ? S = mh(m.registered, $, E.className) : E.className != null && (S = E.className + " ");
      var T = Ao(d.concat($), m.registered, k);
      S += m.key + "-" + T.name, l !== void 0 && (S += " " + l);
      var j = u && s === void 0 ? Gd(h) : a, M = {};
      for (var U in E)
        u && U === "as" || j(U) && (M[U] = E[U]);
      return M.className = S, f && (M.ref = f), /* @__PURE__ */ _.createElement(_.Fragment, null, /* @__PURE__ */ _.createElement(r1, {
        cache: m,
        serialized: T,
        isStringTag: typeof h == "string"
      }), /* @__PURE__ */ _.createElement(h, M));
    });
    return g.displayName = i !== void 0 ? i : "Styled(" + (typeof o == "string" ? o : o.displayName || o.name || "Component") + ")", g.defaultProps = t.defaultProps, g.__emotion_real = g, g.__emotion_base = o, g.__emotion_styles = d, g.__emotion_forwardProp = s, Object.defineProperty(g, "toString", {
      value: function() {
        return l === void 0 && e1 ? "NO_COMPONENT_SELECTOR" : "." + l;
      }
    }), g.withComponent = function(E, m) {
      var f = e(E, w({}, n, m, {
        shouldForwardProp: Qd(g, m, !0)
      }));
      return f.apply(void 0, d);
    }, g;
  };
}, i1 = [
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
], Ka = o1.bind(null);
i1.forEach(function(e) {
  Ka[e] = Ka(e);
});
function l1(e, t) {
  const n = uh({
    key: "css",
    prepend: e
  });
  if (t) {
    const r = n.insert;
    n.insert = (...o) => (o[1].styles.match(/^@layer\s+[^{]*$/) || (o[1].styles = `@layer mui {${o[1].styles}}`), r(...o));
  }
  return n;
}
const Bs = /* @__PURE__ */ new Map();
function s1(e) {
  const {
    injectFirst: t,
    enableCssLayer: n,
    children: r
  } = e, o = _.useMemo(() => {
    const i = `${t}-${n}`;
    if (typeof document == "object" && Bs.has(i))
      return Bs.get(i);
    const l = l1(t, n);
    return Bs.set(i, l), l;
  }, [t, n]);
  return t || n ? /* @__PURE__ */ y.jsx(Ky, {
    value: o,
    children: r
  }) : r;
}
function a1(e) {
  return e == null || Object.keys(e).length === 0;
}
function Sh(e) {
  const {
    styles: t,
    defaultTheme: n = {}
  } = e, r = typeof t == "function" ? (o) => t(a1(o) ? n : o) : t;
  return /* @__PURE__ */ y.jsx(qy, {
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
function tc(e, t) {
  return Ka(e, t);
}
const wh = (e, t) => {
  Array.isArray(e.__emotion_styles) && (e.__emotion_styles = t(e.__emotion_styles));
}, Yd = [];
function nl(e) {
  return Yd[0] = e, Ao(Yd);
}
const u1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  GlobalStyles: Sh,
  StyledEngineProvider: s1,
  ThemeContext: Er,
  css: Dl,
  default: tc,
  internal_processStyles: wh,
  internal_serializeStyles: nl,
  keyframes: Pr
}, Symbol.toStringTag, { value: "Module" }));
function Lt(e) {
  if (typeof e != "object" || e === null)
    return !1;
  const t = Object.getPrototypeOf(e);
  return (t === null || t === Object.prototype || Object.getPrototypeOf(t) === null) && !(Symbol.toStringTag in e) && !(Symbol.iterator in e);
}
function Ch(e) {
  if (/* @__PURE__ */ _.isValidElement(e) || !Lt(e))
    return e;
  const t = {};
  return Object.keys(e).forEach((n) => {
    t[n] = Ch(e[n]);
  }), t;
}
function Nt(e, t, n = {
  clone: !0
}) {
  const r = n.clone ? w({}, e) : e;
  return Lt(e) && Lt(t) && Object.keys(t).forEach((o) => {
    /* @__PURE__ */ _.isValidElement(t[o]) ? r[o] = t[o] : Lt(t[o]) && // Avoid prototype pollution
    Object.prototype.hasOwnProperty.call(e, o) && Lt(e[o]) ? r[o] = Nt(e[o], t[o], n) : n.clone ? r[o] = Lt(t[o]) ? Ch(t[o]) : t[o] : r[o] = t[o];
  }), r;
}
const c1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Nt,
  isPlainObject: Lt
}, Symbol.toStringTag, { value: "Module" })), d1 = ["values", "unit", "step"], f1 = (e) => {
  const t = Object.keys(e).map((n) => ({
    key: n,
    val: e[n]
  })) || [];
  return t.sort((n, r) => n.val - r.val), t.reduce((n, r) => w({}, n, {
    [r.key]: r.val
  }), {});
};
function kh(e) {
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
  } = e, o = L(e, d1), i = f1(t), l = Object.keys(i);
  function s(p) {
    return `@media (min-width:${typeof t[p] == "number" ? t[p] : p}${n})`;
  }
  function a(p) {
    return `@media (max-width:${(typeof t[p] == "number" ? t[p] : p) - r / 100}${n})`;
  }
  function u(p, v) {
    const x = l.indexOf(v);
    return `@media (min-width:${typeof t[p] == "number" ? t[p] : p}${n}) and (max-width:${(x !== -1 && typeof t[l[x]] == "number" ? t[l[x]] : v) - r / 100}${n})`;
  }
  function c(p) {
    return l.indexOf(p) + 1 < l.length ? u(p, l[l.indexOf(p) + 1]) : s(p);
  }
  function d(p) {
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
    not: d,
    unit: n
  }, o);
}
const p1 = {
  borderRadius: 4
}, m1 = p1;
function io(e, t) {
  return t ? Nt(e, t, {
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
}, Xd = {
  // Sorted ASC by size. That's important.
  // It can't be configured as it's used statically for propTypes.
  keys: ["xs", "sm", "md", "lg", "xl"],
  up: (e) => `@media (min-width:${nc[e]}px)`
};
function mt(e, t, n) {
  const r = e.theme || {};
  if (Array.isArray(t)) {
    const i = r.breakpoints || Xd;
    return t.reduce((l, s, a) => (l[i.up(i.keys[a])] = n(t[a]), l), {});
  }
  if (typeof t == "object") {
    const i = r.breakpoints || Xd;
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
function h1(e = {}) {
  var t;
  return ((t = e.keys) == null ? void 0 : t.reduce((r, o) => {
    const i = e.up(o);
    return r[i] = {}, r;
  }, {})) || {};
}
function qd(e, t) {
  return e.reduce((n, r) => {
    const o = n[r];
    return (!o || Object.keys(o).length === 0) && delete n[r], n;
  }, t);
}
function g1(e, t) {
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
  const r = n || g1(e, t), o = Object.keys(r);
  if (o.length === 0)
    return e;
  let i;
  return o.reduce((l, s, a) => (Array.isArray(e) ? (l[s] = e[a] != null ? e[a] : e[i], i = a) : typeof e == "object" ? (l[s] = e[s] != null ? e[s] : e[i], i = s) : l[s] = e, l), {});
}
function N(e) {
  if (typeof e != "string")
    throw new Error(_o(7));
  return e.charAt(0).toUpperCase() + e.slice(1);
}
const v1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: N
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
function rl(e, t, n, r = n) {
  let o;
  return typeof e == "function" ? o = e(n) : Array.isArray(e) ? o = e[n] || r : o = Bl(e, n) || r, t && (o = t(o, r, e)), o;
}
function de(e) {
  const {
    prop: t,
    cssProperty: n = e.prop,
    themeKey: r,
    transform: o
  } = e, i = (l) => {
    if (l[t] == null)
      return null;
    const s = l[t], a = l.theme, u = Bl(a, r) || {};
    return mt(l, s, (d) => {
      let p = rl(u, o, d);
      return d === p && typeof d == "string" && (p = rl(u, o, `${t}${d === "default" ? "" : N(d)}`, d)), n === !1 ? p : {
        [n]: p
      };
    });
  };
  return i.propTypes = {}, i.filterProps = [t], i;
}
function y1(e) {
  const t = {};
  return (n) => (t[n] === void 0 && (t[n] = e(n)), t[n]);
}
const x1 = {
  m: "margin",
  p: "padding"
}, S1 = {
  t: "Top",
  r: "Right",
  b: "Bottom",
  l: "Left",
  x: ["Left", "Right"],
  y: ["Top", "Bottom"]
}, Zd = {
  marginX: "mx",
  marginY: "my",
  paddingX: "px",
  paddingY: "py"
}, w1 = y1((e) => {
  if (e.length > 2)
    if (Zd[e])
      e = Zd[e];
    else
      return [e];
  const [t, n] = e.split(""), r = x1[t], o = S1[n] || "";
  return Array.isArray(o) ? o.map((i) => r + i) : [r + o];
}), rc = ["m", "mt", "mr", "mb", "ml", "mx", "my", "margin", "marginTop", "marginRight", "marginBottom", "marginLeft", "marginX", "marginY", "marginInline", "marginInlineStart", "marginInlineEnd", "marginBlock", "marginBlockStart", "marginBlockEnd"], oc = ["p", "pt", "pr", "pb", "pl", "px", "py", "padding", "paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "paddingX", "paddingY", "paddingInline", "paddingInlineStart", "paddingInlineEnd", "paddingBlock", "paddingBlockStart", "paddingBlockEnd"];
[...rc, ...oc];
function Lo(e, t, n, r) {
  var o;
  const i = (o = Bl(e, t, !1)) != null ? o : n;
  return typeof i == "number" ? (l) => typeof l == "string" ? l : i * l : Array.isArray(i) ? (l) => typeof l == "string" ? l : i[l] : typeof i == "function" ? i : () => {
  };
}
function _h(e) {
  return Lo(e, "spacing", 8);
}
function Do(e, t) {
  if (typeof t == "string" || t == null)
    return t;
  const n = Math.abs(t), r = e(n);
  return t >= 0 ? r : typeof r == "number" ? -r : `-${r}`;
}
function C1(e, t) {
  return (n) => e.reduce((r, o) => (r[o] = Do(t, n), r), {});
}
function k1(e, t, n, r) {
  if (t.indexOf(n) === -1)
    return null;
  const o = w1(n), i = C1(o, r), l = e[n];
  return mt(e, l, i);
}
function $h(e, t) {
  const n = _h(e.theme);
  return Object.keys(e).map((r) => k1(e, t, r, n)).reduce(io, {});
}
function se(e) {
  return $h(e, rc);
}
se.propTypes = {};
se.filterProps = rc;
function ae(e) {
  return $h(e, oc);
}
ae.propTypes = {};
ae.filterProps = oc;
function _1(e = 8) {
  if (e.mui)
    return e;
  const t = _h({
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
function at(e) {
  return typeof e != "number" ? e : `${e}px solid`;
}
function gt(e, t) {
  return de({
    prop: e,
    themeKey: "borders",
    transform: t
  });
}
const $1 = gt("border", at), E1 = gt("borderTop", at), P1 = gt("borderRight", at), T1 = gt("borderBottom", at), R1 = gt("borderLeft", at), M1 = gt("borderColor"), O1 = gt("borderTopColor"), j1 = gt("borderRightColor"), z1 = gt("borderBottomColor"), N1 = gt("borderLeftColor"), b1 = gt("outline", at), I1 = gt("outlineColor"), Ul = (e) => {
  if (e.borderRadius !== void 0 && e.borderRadius !== null) {
    const t = Lo(e.theme, "shape.borderRadius", 4), n = (r) => ({
      borderRadius: Do(t, r)
    });
    return mt(e, e.borderRadius, n);
  }
  return null;
};
Ul.propTypes = {};
Ul.filterProps = ["borderRadius"];
Wl($1, E1, P1, T1, R1, M1, O1, j1, z1, N1, Ul, b1, I1);
const Vl = (e) => {
  if (e.gap !== void 0 && e.gap !== null) {
    const t = Lo(e.theme, "spacing", 8), n = (r) => ({
      gap: Do(t, r)
    });
    return mt(e, e.gap, n);
  }
  return null;
};
Vl.propTypes = {};
Vl.filterProps = ["gap"];
const Hl = (e) => {
  if (e.columnGap !== void 0 && e.columnGap !== null) {
    const t = Lo(e.theme, "spacing", 8), n = (r) => ({
      columnGap: Do(t, r)
    });
    return mt(e, e.columnGap, n);
  }
  return null;
};
Hl.propTypes = {};
Hl.filterProps = ["columnGap"];
const Kl = (e) => {
  if (e.rowGap !== void 0 && e.rowGap !== null) {
    const t = Lo(e.theme, "spacing", 8), n = (r) => ({
      rowGap: Do(t, r)
    });
    return mt(e, e.rowGap, n);
  }
  return null;
};
Kl.propTypes = {};
Kl.filterProps = ["rowGap"];
const A1 = de({
  prop: "gridColumn"
}), L1 = de({
  prop: "gridRow"
}), D1 = de({
  prop: "gridAutoFlow"
}), F1 = de({
  prop: "gridAutoColumns"
}), B1 = de({
  prop: "gridAutoRows"
}), W1 = de({
  prop: "gridTemplateColumns"
}), U1 = de({
  prop: "gridTemplateRows"
}), V1 = de({
  prop: "gridTemplateAreas"
}), H1 = de({
  prop: "gridArea"
});
Wl(Vl, Hl, Kl, A1, L1, D1, F1, B1, W1, U1, V1, H1);
function ur(e, t) {
  return t === "grey" ? t : e;
}
const K1 = de({
  prop: "color",
  themeKey: "palette",
  transform: ur
}), G1 = de({
  prop: "bgcolor",
  cssProperty: "backgroundColor",
  themeKey: "palette",
  transform: ur
}), Q1 = de({
  prop: "backgroundColor",
  themeKey: "palette",
  transform: ur
});
Wl(K1, G1, Q1);
function Xe(e) {
  return e <= 1 && e !== 0 ? `${e * 100}%` : e;
}
const Y1 = de({
  prop: "width",
  transform: Xe
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
        maxWidth: Xe(n)
      };
    };
    return mt(e, e.maxWidth, t);
  }
  return null;
};
ic.filterProps = ["maxWidth"];
const X1 = de({
  prop: "minWidth",
  transform: Xe
}), q1 = de({
  prop: "height",
  transform: Xe
}), Z1 = de({
  prop: "maxHeight",
  transform: Xe
}), J1 = de({
  prop: "minHeight",
  transform: Xe
});
de({
  prop: "size",
  cssProperty: "width",
  transform: Xe
});
de({
  prop: "size",
  cssProperty: "height",
  transform: Xe
});
const ex = de({
  prop: "boxSizing"
});
Wl(Y1, ic, X1, q1, Z1, J1, ex);
const tx = {
  // borders
  border: {
    themeKey: "borders",
    transform: at
  },
  borderTop: {
    themeKey: "borders",
    transform: at
  },
  borderRight: {
    themeKey: "borders",
    transform: at
  },
  borderBottom: {
    themeKey: "borders",
    transform: at
  },
  borderLeft: {
    themeKey: "borders",
    transform: at
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
    transform: at
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
    transform: ur
  },
  bgcolor: {
    themeKey: "palette",
    cssProperty: "backgroundColor",
    transform: ur
  },
  backgroundColor: {
    themeKey: "palette",
    transform: ur
  },
  // spacing
  p: {
    style: ae
  },
  pt: {
    style: ae
  },
  pr: {
    style: ae
  },
  pb: {
    style: ae
  },
  pl: {
    style: ae
  },
  px: {
    style: ae
  },
  py: {
    style: ae
  },
  padding: {
    style: ae
  },
  paddingTop: {
    style: ae
  },
  paddingRight: {
    style: ae
  },
  paddingBottom: {
    style: ae
  },
  paddingLeft: {
    style: ae
  },
  paddingX: {
    style: ae
  },
  paddingY: {
    style: ae
  },
  paddingInline: {
    style: ae
  },
  paddingInlineStart: {
    style: ae
  },
  paddingInlineEnd: {
    style: ae
  },
  paddingBlock: {
    style: ae
  },
  paddingBlockStart: {
    style: ae
  },
  paddingBlockEnd: {
    style: ae
  },
  m: {
    style: se
  },
  mt: {
    style: se
  },
  mr: {
    style: se
  },
  mb: {
    style: se
  },
  ml: {
    style: se
  },
  mx: {
    style: se
  },
  my: {
    style: se
  },
  margin: {
    style: se
  },
  marginTop: {
    style: se
  },
  marginRight: {
    style: se
  },
  marginBottom: {
    style: se
  },
  marginLeft: {
    style: se
  },
  marginX: {
    style: se
  },
  marginY: {
    style: se
  },
  marginInline: {
    style: se
  },
  marginInlineStart: {
    style: se
  },
  marginInlineEnd: {
    style: se
  },
  marginBlock: {
    style: se
  },
  marginBlockStart: {
    style: se
  },
  marginBlockEnd: {
    style: se
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
    style: ic
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
}, Fo = tx;
function nx(...e) {
  const t = e.reduce((r, o) => r.concat(Object.keys(o)), []), n = new Set(t);
  return e.every((r) => n.size === Object.keys(r).length);
}
function rx(e, t) {
  return typeof e == "function" ? e(t) : e;
}
function Eh() {
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
      style: d
    } = s;
    if (r == null)
      return null;
    if (u === "typography" && r === "inherit")
      return {
        [n]: r
      };
    const p = Bl(o, u) || {};
    return d ? d(l) : mt(l, r, (x) => {
      let g = rl(p, c, x);
      return x === g && typeof x == "string" && (g = rl(p, c, `${n}${x === "default" ? "" : N(x)}`, x)), a === !1 ? g : {
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
    const s = (r = i.unstable_sxConfig) != null ? r : Fo;
    function a(u) {
      let c = u;
      if (typeof u == "function")
        c = u(i);
      else if (typeof u != "object")
        return u;
      if (!c)
        return null;
      const d = h1(i.breakpoints), p = Object.keys(d);
      let v = d;
      return Object.keys(c).forEach((x) => {
        const g = rx(c[x], i);
        if (g != null)
          if (typeof g == "object")
            if (s[x])
              v = io(v, e(x, g, i, s));
            else {
              const E = mt({
                theme: i
              }, g, (m) => ({
                [x]: m
              }));
              nx(E, g) ? v[x] = t({
                sx: g,
                theme: i,
                nested: !0
              }) : v = io(v, E);
            }
          else
            v = io(v, e(x, g, i, s));
      }), !l && i.modularCssLayers ? {
        "@layer sx": qd(p, v)
      } : qd(p, v);
    }
    return Array.isArray(o) ? o.map(a) : a(o);
  }
  return t;
}
const Ph = Eh();
Ph.filterProps = ["sx"];
const Bo = Ph;
function Th(e, t) {
  const n = this;
  return n.vars && typeof n.getColorSchemeSelector == "function" ? {
    [n.getColorSchemeSelector(e).replace(/(\[[^\]]+\])/, "*:where($1)")]: t
  } : n.palette.mode === e ? t : {};
}
const ox = ["breakpoints", "palette", "spacing", "shape"];
function Wo(e = {}, ...t) {
  const {
    breakpoints: n = {},
    palette: r = {},
    spacing: o,
    shape: i = {}
  } = e, l = L(e, ox), s = kh(n), a = _1(o);
  let u = Nt({
    breakpoints: s,
    direction: "ltr",
    components: {},
    // Inject component definitions.
    palette: w({
      mode: "light"
    }, r),
    spacing: a,
    shape: w({}, m1, i)
  }, l);
  return u.applyStyles = Th, u = t.reduce((c, d) => Nt(c, d), u), u.unstable_sxConfig = w({}, Fo, l == null ? void 0 : l.unstable_sxConfig), u.unstable_sx = function(d) {
    return Bo({
      sx: d,
      theme: this
    });
  }, u;
}
const ix = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Wo,
  private_createBreakpoints: kh,
  unstable_applyStyles: Th
}, Symbol.toStringTag, { value: "Module" }));
function lx(e) {
  return Object.keys(e).length === 0;
}
function lc(e = null) {
  const t = _.useContext(Er);
  return !t || lx(t) ? e : t;
}
const sx = Wo();
function Gl(e = sx) {
  return lc(e);
}
function Ws(e) {
  const t = nl(e);
  return e !== t && t.styles ? (t.styles.match(/^@layer\s+[^{]*$/) || (t.styles = `@layer global{${t.styles}}`), t) : e;
}
function Rh({
  styles: e,
  themeId: t,
  defaultTheme: n = {}
}) {
  const r = Gl(n), o = t && r[t] || r;
  let i = typeof e == "function" ? e(o) : e;
  return o.modularCssLayers && (Array.isArray(i) ? i = i.map((l) => Ws(typeof l == "function" ? l(o) : l)) : i = Ws(i)), /* @__PURE__ */ y.jsx(Sh, {
    styles: i
  });
}
const ax = ["sx"], ux = (e) => {
  var t, n;
  const r = {
    systemProps: {},
    otherProps: {}
  }, o = (t = e == null || (n = e.theme) == null ? void 0 : n.unstable_sxConfig) != null ? t : Fo;
  return Object.keys(e).forEach((i) => {
    o[i] ? r.systemProps[i] = e[i] : r.otherProps[i] = e[i];
  }), r;
};
function Ql(e) {
  const {
    sx: t
  } = e, n = L(e, ax), {
    systemProps: r,
    otherProps: o
  } = ux(n);
  let i;
  return Array.isArray(t) ? i = [r, ...t] : typeof t == "function" ? i = (...l) => {
    const s = t(...l);
    return Lt(s) ? w({}, r, s) : r;
  } : i = w({}, r, t), w({}, o, {
    sx: i
  });
}
const cx = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Bo,
  extendSxProp: Ql,
  unstable_createStyleFunctionSx: Eh,
  unstable_defaultSxConfig: Fo
}, Symbol.toStringTag, { value: "Module" })), Jd = (e) => e, dx = () => {
  let e = Jd;
  return {
    configure(t) {
      e = t;
    },
    generate(t) {
      return e(t);
    },
    reset() {
      e = Jd;
    }
  };
}, fx = dx(), sc = fx;
function Mh(e) {
  var t, n, r = "";
  if (typeof e == "string" || typeof e == "number")
    r += e;
  else if (typeof e == "object")
    if (Array.isArray(e)) {
      var o = e.length;
      for (t = 0; t < o; t++)
        e[t] && (n = Mh(e[t])) && (r && (r += " "), r += n);
    } else
      for (n in e)
        e[n] && (r && (r += " "), r += n);
  return r;
}
function B() {
  for (var e, t, n = 0, r = "", o = arguments.length; n < o; n++)
    (e = arguments[n]) && (t = Mh(e)) && (r && (r += " "), r += t);
  return r;
}
const px = ["className", "component"];
function mx(e = {}) {
  const {
    themeId: t,
    defaultTheme: n,
    defaultClassName: r = "MuiBox-root",
    generateClassName: o
  } = e, i = tc("div", {
    shouldForwardProp: (s) => s !== "theme" && s !== "sx" && s !== "as"
  })(Bo);
  return /* @__PURE__ */ _.forwardRef(function(a, u) {
    const c = Gl(n), d = Ql(a), {
      className: p,
      component: v = "div"
    } = d, x = L(d, px);
    return /* @__PURE__ */ y.jsx(i, w({
      as: v,
      ref: u,
      className: B(p, o ? o(r) : r),
      theme: t && c[t] || c
    }, x));
  });
}
const hx = {
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
  const r = hx[t];
  return r ? `${n}-${r}` : `${sc.generate(e)}-${t}`;
}
function ye(e, t, n = "Mui") {
  const r = {};
  return t.forEach((o) => {
    r[o] = ve(e, o, n);
  }), r;
}
var Oh = { exports: {} }, X = {};
/**
 * @license React
 * react-is.production.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ac = Symbol.for("react.transitional.element"), uc = Symbol.for("react.portal"), Yl = Symbol.for("react.fragment"), Xl = Symbol.for("react.strict_mode"), ql = Symbol.for("react.profiler"), Zl = Symbol.for("react.consumer"), Jl = Symbol.for("react.context"), es = Symbol.for("react.forward_ref"), ts = Symbol.for("react.suspense"), ns = Symbol.for("react.suspense_list"), rs = Symbol.for("react.memo"), os = Symbol.for("react.lazy"), gx = Symbol.for("react.view_transition"), vx = Symbol.for("react.client.reference");
function vt(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case ac:
        switch (e = e.type, e) {
          case Yl:
          case ql:
          case Xl:
          case ts:
          case ns:
          case gx:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Jl:
              case es:
              case os:
              case rs:
                return e;
              case Zl:
                return e;
              default:
                return t;
            }
        }
      case uc:
        return t;
    }
  }
}
X.ContextConsumer = Zl;
X.ContextProvider = Jl;
X.Element = ac;
X.ForwardRef = es;
X.Fragment = Yl;
X.Lazy = os;
X.Memo = rs;
X.Portal = uc;
X.Profiler = ql;
X.StrictMode = Xl;
X.Suspense = ts;
X.SuspenseList = ns;
X.isContextConsumer = function(e) {
  return vt(e) === Zl;
};
X.isContextProvider = function(e) {
  return vt(e) === Jl;
};
X.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === ac;
};
X.isForwardRef = function(e) {
  return vt(e) === es;
};
X.isFragment = function(e) {
  return vt(e) === Yl;
};
X.isLazy = function(e) {
  return vt(e) === os;
};
X.isMemo = function(e) {
  return vt(e) === rs;
};
X.isPortal = function(e) {
  return vt(e) === uc;
};
X.isProfiler = function(e) {
  return vt(e) === ql;
};
X.isStrictMode = function(e) {
  return vt(e) === Xl;
};
X.isSuspense = function(e) {
  return vt(e) === ts;
};
X.isSuspenseList = function(e) {
  return vt(e) === ns;
};
X.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === Yl || e === ql || e === Xl || e === ts || e === ns || typeof e == "object" && e !== null && (e.$$typeof === os || e.$$typeof === rs || e.$$typeof === Jl || e.$$typeof === Zl || e.$$typeof === es || e.$$typeof === vx || e.getModuleId !== void 0);
};
X.typeOf = vt;
Oh.exports = X;
var ef = Oh.exports;
const yx = /^\s*function(?:\s|\s*\/\*.*\*\/\s*)+([^(\s/]*)\s*/;
function jh(e) {
  const t = `${e}`.match(yx);
  return t && t[1] || "";
}
function zh(e, t = "") {
  return e.displayName || e.name || jh(e) || t;
}
function tf(e, t, n) {
  const r = zh(t);
  return e.displayName || (r !== "" ? `${n}(${r})` : n);
}
function xx(e) {
  if (e != null) {
    if (typeof e == "string")
      return e;
    if (typeof e == "function")
      return zh(e, "Component");
    if (typeof e == "object")
      switch (e.$$typeof) {
        case ef.ForwardRef:
          return tf(e, e.render, "ForwardRef");
        case ef.Memo:
          return tf(e, e.type, "memo");
        default:
          return;
      }
  }
}
const Sx = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: xx,
  getFunctionName: jh
}, Symbol.toStringTag, { value: "Module" })), wx = ["ownerState"], Cx = ["variants"], kx = ["name", "slot", "skipVariantsResolver", "skipSx", "overridesResolver"];
function _x(e) {
  return Object.keys(e).length === 0;
}
function $x(e) {
  return typeof e == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  e.charCodeAt(0) > 96;
}
function Us(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
function nf(e, t) {
  return t && e && typeof e == "object" && e.styles && !e.styles.startsWith("@layer") && (e.styles = `@layer ${t}{${String(e.styles)}}`), e;
}
const Ex = Wo(), Px = (e) => e && e.charAt(0).toLowerCase() + e.slice(1);
function ci({
  defaultTheme: e,
  theme: t,
  themeId: n
}) {
  return _x(t) ? e : t[n] || t;
}
function Tx(e) {
  return e ? (t, n) => n[e] : null;
}
function Ti(e, t, n) {
  let {
    ownerState: r
  } = t, o = L(t, wx);
  const i = typeof e == "function" ? e(w({
    ownerState: r
  }, o)) : e;
  if (Array.isArray(i))
    return i.flatMap((l) => Ti(l, w({
      ownerState: r
    }, o), n));
  if (i && typeof i == "object" && Array.isArray(i.variants)) {
    const {
      variants: l = []
    } = i;
    let a = L(i, Cx);
    return l.forEach((u) => {
      let c = !0;
      if (typeof u.props == "function" ? c = u.props(w({
        ownerState: r
      }, o, r)) : Object.keys(u.props).forEach((d) => {
        (r == null ? void 0 : r[d]) !== u.props[d] && o[d] !== u.props[d] && (c = !1);
      }), c) {
        Array.isArray(a) || (a = [a]);
        const d = typeof u.style == "function" ? u.style(w({
          ownerState: r
        }, o, r)) : u.style;
        a.push(n ? nf(nl(d), n) : d);
      }
    }), a;
  }
  return n ? nf(nl(i), n) : i;
}
function Rx(e = {}) {
  const {
    themeId: t,
    defaultTheme: n = Ex,
    rootShouldForwardProp: r = Us,
    slotShouldForwardProp: o = Us
  } = e, i = (l) => Bo(w({}, l, {
    theme: ci(w({}, l, {
      defaultTheme: n,
      themeId: t
    }))
  }));
  return i.__mui_systemSx = !0, (l, s = {}) => {
    wh(l, (k) => k.filter((C) => !(C != null && C.__mui_systemSx)));
    const {
      name: a,
      slot: u,
      skipVariantsResolver: c,
      skipSx: d,
      // TODO v6: remove `lowercaseFirstLetter()` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      overridesResolver: p = Tx(Px(u))
    } = s, v = L(s, kx), x = a && a.startsWith("Mui") || u ? "components" : "custom", g = c !== void 0 ? c : (
      // TODO v6: remove `Root` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      u && u !== "Root" && u !== "root" || !1
    ), E = d || !1;
    let m, f = Us;
    u === "Root" || u === "root" ? f = r : u ? f = o : $x(l) && (f = void 0);
    const h = tc(l, w({
      shouldForwardProp: f,
      label: m
    }, v)), S = (k) => typeof k == "function" && k.__emotion_real !== k || Lt(k) ? (C) => {
      const T = ci({
        theme: C.theme,
        defaultTheme: n,
        themeId: t
      });
      return Ti(k, w({}, C, {
        theme: T
      }), T.modularCssLayers ? x : void 0);
    } : k, $ = (k, ...C) => {
      let T = S(k);
      const j = C ? C.map(S) : [];
      a && p && j.push((F) => {
        const A = ci(w({}, F, {
          defaultTheme: n,
          themeId: t
        }));
        if (!A.components || !A.components[a] || !A.components[a].styleOverrides)
          return null;
        const Z = A.components[a].styleOverrides, xe = {};
        return Object.entries(Z).forEach(([Ee, Ge]) => {
          xe[Ee] = Ti(Ge, w({}, F, {
            theme: A
          }), A.modularCssLayers ? "theme" : void 0);
        }), p(F, xe);
      }), a && !g && j.push((F) => {
        var A;
        const Z = ci(w({}, F, {
          defaultTheme: n,
          themeId: t
        })), xe = Z == null || (A = Z.components) == null || (A = A[a]) == null ? void 0 : A.variants;
        return Ti({
          variants: xe
        }, w({}, F, {
          theme: Z
        }), Z.modularCssLayers ? "theme" : void 0);
      }), E || j.push(i);
      const M = j.length - C.length;
      if (Array.isArray(k) && M > 0) {
        const F = new Array(M).fill("");
        T = [...k, ...F], T.raw = [...k.raw, ...F];
      }
      const U = h(T, ...j);
      return l.muiName && (U.muiName = l.muiName), U;
    };
    return h.withConfig && ($.withConfig = h.withConfig), $;
  };
}
const Mx = Rx(), Ox = Mx;
function To(e, t) {
  const n = w({}, t);
  return Object.keys(e).forEach((r) => {
    if (r.toString().match(/^(components|slots)$/))
      n[r] = w({}, e[r], n[r]);
    else if (r.toString().match(/^(componentsProps|slotProps)$/)) {
      const o = e[r] || {}, i = t[r];
      n[r] = {}, !i || !Object.keys(i) ? n[r] = o : !o || !Object.keys(o) ? n[r] = i : (n[r] = w({}, i), Object.keys(o).forEach((l) => {
        n[r][l] = To(o[l], i[l]);
      }));
    } else
      n[r] === void 0 && (n[r] = e[r]);
  }), n;
}
function jx(e) {
  const {
    theme: t,
    name: n,
    props: r
  } = e;
  return !t || !t.components || !t.components[n] || !t.components[n].defaultProps ? r : To(t.components[n].defaultProps, r);
}
function zx({
  props: e,
  name: t,
  defaultTheme: n,
  themeId: r
}) {
  let o = Gl(n);
  return r && (o = o[r] || o), jx({
    theme: o,
    name: t,
    props: e
  });
}
const Nx = typeof window < "u" ? _.useLayoutEffect : _.useEffect, cc = Nx;
function bx(e, t = Number.MIN_SAFE_INTEGER, n = Number.MAX_SAFE_INTEGER) {
  return Math.max(t, Math.min(e, n));
}
const Ix = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: bx
}, Symbol.toStringTag, { value: "Module" }));
function Ax(...e) {
  return e.reduce((t, n) => n == null ? t : function(...o) {
    t.apply(this, o), n.apply(this, o);
  }, () => {
  });
}
function Lx(e, t = 166) {
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
function Dx(e, t) {
  return () => null;
}
function Fx(e, t) {
  var n, r;
  return /* @__PURE__ */ _.isValidElement(e) && t.indexOf(
    // For server components `muiName` is avaialble in element.type._payload.value.muiName
    // relevant info - https://github.com/facebook/react/blob/2807d781a08db8e9873687fccc25c0f12b4fb3d4/packages/react/src/ReactLazy.js#L45
    // eslint-disable-next-line no-underscore-dangle
    (n = e.type.muiName) != null ? n : (r = e.type) == null || (r = r._payload) == null || (r = r.value) == null ? void 0 : r.muiName
  ) !== -1;
}
function Nh(e) {
  return e && e.ownerDocument || document;
}
function Bx(e) {
  return Nh(e).defaultView || window;
}
function Wx(e, t) {
  return () => null;
}
function bh(e, t) {
  typeof e == "function" ? e(t) : e && (e.current = t);
}
let rf = 0;
function Ux(e) {
  const [t, n] = _.useState(e), r = e || t;
  return _.useEffect(() => {
    t == null && (rf += 1, n(`mui-${rf}`));
  }, [t]), r;
}
const of = Ys["useId".toString()];
function Ih(e) {
  if (of !== void 0) {
    const t = of();
    return e ?? t;
  }
  return Ux(e);
}
function Vx(e, t, n, r, o) {
  return null;
}
function Hx({
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
function Yr(e) {
  const t = _.useRef(e);
  return cc(() => {
    t.current = e;
  }), _.useRef((...n) => (
    // @ts-expect-error hide `this`
    (0, t.current)(...n)
  )).current;
}
function ol(...e) {
  return _.useMemo(() => e.every((t) => t == null) ? null : (t) => {
    e.forEach((n) => {
      bh(n, t);
    });
  }, e);
}
const lf = {};
function Kx(e, t) {
  const n = _.useRef(lf);
  return n.current === lf && (n.current = e(t)), n;
}
const Gx = [];
function Qx(e) {
  _.useEffect(e, Gx);
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
function Yx() {
  const e = Kx(is.create).current;
  return Qx(e.disposeEffect), e;
}
let ls = !0, Ga = !1;
const Xx = new is(), qx = {
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
function Zx(e) {
  const {
    type: t,
    tagName: n
  } = e;
  return !!(n === "INPUT" && qx[t] && !e.readOnly || n === "TEXTAREA" && !e.readOnly || e.isContentEditable);
}
function Jx(e) {
  e.metaKey || e.altKey || e.ctrlKey || (ls = !0);
}
function Vs() {
  ls = !1;
}
function eS() {
  this.visibilityState === "hidden" && Ga && (ls = !0);
}
function tS(e) {
  e.addEventListener("keydown", Jx, !0), e.addEventListener("mousedown", Vs, !0), e.addEventListener("pointerdown", Vs, !0), e.addEventListener("touchstart", Vs, !0), e.addEventListener("visibilitychange", eS, !0);
}
function nS(e) {
  const {
    target: t
  } = e;
  try {
    return t.matches(":focus-visible");
  } catch {
  }
  return ls || Zx(t);
}
function Ah() {
  const e = _.useCallback((o) => {
    o != null && tS(o.ownerDocument);
  }, []), t = _.useRef(!1);
  function n() {
    return t.current ? (Ga = !0, Xx.start(100, () => {
      Ga = !1;
    }), t.current = !1, !0) : !1;
  }
  function r(o) {
    return nS(o) ? (t.current = !0, !0) : !1;
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
function rS(e) {
  return typeof e == "string";
}
function oS(e, t, n) {
  return e === void 0 || rS(e) ? t : w({}, t, {
    ownerState: w({}, t.ownerState, n)
  });
}
function iS(e, t = []) {
  if (e === void 0)
    return {};
  const n = {};
  return Object.keys(e).filter((r) => r.match(/^on[A-Z]/) && typeof e[r] == "function" && !t.includes(r)).forEach((r) => {
    n[r] = e[r];
  }), n;
}
function sf(e) {
  if (e === void 0)
    return {};
  const t = {};
  return Object.keys(e).filter((n) => !(n.match(/^on[A-Z]/) && typeof e[n] == "function")).forEach((n) => {
    t[n] = e[n];
  }), t;
}
function lS(e) {
  const {
    getSlotProps: t,
    additionalProps: n,
    externalSlotProps: r,
    externalForwardedProps: o,
    className: i
  } = e;
  if (!t) {
    const v = B(n == null ? void 0 : n.className, i, o == null ? void 0 : o.className, r == null ? void 0 : r.className), x = w({}, n == null ? void 0 : n.style, o == null ? void 0 : o.style, r == null ? void 0 : r.style), g = w({}, n, o, r);
    return v.length > 0 && (g.className = v), Object.keys(x).length > 0 && (g.style = x), {
      props: g,
      internalRef: void 0
    };
  }
  const l = iS(w({}, o, r)), s = sf(r), a = sf(o), u = t(l), c = B(u == null ? void 0 : u.className, n == null ? void 0 : n.className, i, o == null ? void 0 : o.className, r == null ? void 0 : r.className), d = w({}, u == null ? void 0 : u.style, n == null ? void 0 : n.style, o == null ? void 0 : o.style, r == null ? void 0 : r.style), p = w({}, u, n, a, s);
  return c.length > 0 && (p.className = c), Object.keys(d).length > 0 && (p.style = d), {
    props: p,
    internalRef: u.ref
  };
}
function sS(e, t, n) {
  return typeof e == "function" ? e(t, n) : e;
}
const aS = /* @__PURE__ */ _.createContext(null), Lh = aS;
function Dh() {
  return _.useContext(Lh);
}
const uS = typeof Symbol == "function" && Symbol.for, cS = uS ? Symbol.for("mui.nested") : "__THEME_NESTED__";
function dS(e, t) {
  return typeof t == "function" ? t(e) : w({}, e, t);
}
function fS(e) {
  const {
    children: t,
    theme: n
  } = e, r = Dh(), o = _.useMemo(() => {
    const i = r === null ? n : dS(r, n);
    return i != null && (i[cS] = r !== null), i;
  }, [n, r]);
  return /* @__PURE__ */ y.jsx(Lh.Provider, {
    value: o,
    children: t
  });
}
const pS = ["value"], mS = /* @__PURE__ */ _.createContext();
function hS(e) {
  let {
    value: t
  } = e, n = L(e, pS);
  return /* @__PURE__ */ y.jsx(mS.Provider, w({
    value: t ?? !0
  }, n));
}
const Fh = /* @__PURE__ */ _.createContext(void 0);
function gS({
  value: e,
  children: t
}) {
  return /* @__PURE__ */ y.jsx(Fh.Provider, {
    value: e,
    children: t
  });
}
function vS(e) {
  const {
    theme: t,
    name: n,
    props: r
  } = e;
  if (!t || !t.components || !t.components[n])
    return r;
  const o = t.components[n];
  return o.defaultProps ? To(o.defaultProps, r) : !o.styleOverrides && !o.variants ? To(o, r) : r;
}
function yS({
  props: e,
  name: t
}) {
  const n = _.useContext(Fh);
  return vS({
    props: e,
    name: t,
    theme: {
      components: n
    }
  });
}
function xS(e) {
  const t = lc(), n = Ih() || "", {
    modularCssLayers: r
  } = e;
  let o = "mui.global, mui.components, mui.theme, mui.custom, mui.sx";
  return !r || t !== null ? o = "" : typeof r == "string" ? o = r.replace(/mui(?!\.)/g, o) : o = `@layer ${o};`, cc(() => {
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
  }, [o, n]), o ? /* @__PURE__ */ y.jsx(Rh, {
    styles: o
  }) : null;
}
const af = {};
function uf(e, t, n, r = !1) {
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
function SS(e) {
  const {
    children: t,
    theme: n,
    themeId: r
  } = e, o = lc(af), i = Dh() || af, l = uf(r, o, n), s = uf(r, i, n, !0), a = l.direction === "rtl", u = xS(l);
  return /* @__PURE__ */ y.jsx(fS, {
    theme: s,
    children: /* @__PURE__ */ y.jsx(Er.Provider, {
      value: l,
      children: /* @__PURE__ */ y.jsx(hS, {
        value: a,
        children: /* @__PURE__ */ y.jsxs(gS, {
          value: l == null ? void 0 : l.components,
          children: [u, t]
        })
      })
    })
  });
}
const wS = ["className", "component", "disableGutters", "fixed", "maxWidth", "classes"], CS = Wo(), kS = Ox("div", {
  name: "MuiContainer",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[`maxWidth${N(String(n.maxWidth))}`], n.fixed && t.fixed, n.disableGutters && t.disableGutters];
  }
}), _S = (e) => zx({
  props: e,
  name: "MuiContainer",
  defaultTheme: CS
}), $S = (e, t) => {
  const n = (a) => ve(t, a), {
    classes: r,
    fixed: o,
    disableGutters: i,
    maxWidth: l
  } = e, s = {
    root: ["root", l && `maxWidth${N(String(l))}`, o && "fixed", i && "disableGutters"]
  };
  return Ce(s, n, r);
};
function ES(e = {}) {
  const {
    // This will allow adding custom styled fn (for example for custom sx style function)
    createStyledComponent: t = kS,
    useThemeProps: n = _S,
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
    const c = u, d = l.breakpoints.values[c];
    return d !== 0 && (a[l.breakpoints.up(c)] = {
      maxWidth: `${d}${l.breakpoints.unit}`
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
      component: d = "div",
      disableGutters: p = !1,
      fixed: v = !1,
      maxWidth: x = "lg"
    } = u, g = L(u, wS), E = w({}, u, {
      component: d,
      disableGutters: p,
      fixed: v,
      maxWidth: x
    }), m = $S(E, r);
    return (
      // @ts-ignore theme is injected by the styled util
      /* @__PURE__ */ y.jsx(o, w({
        as: d,
        ownerState: E,
        className: B(m.root, c),
        ref: a
      }, g))
    );
  });
}
function PS(e, t) {
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
var fe = {}, Bh = { exports: {} };
(function(e) {
  function t(n) {
    return n && n.__esModule ? n : {
      default: n
    };
  }
  e.exports = t, e.exports.__esModule = !0, e.exports.default = e.exports;
})(Bh);
var yn = Bh.exports;
const TS = /* @__PURE__ */ Kt(Zv), RS = /* @__PURE__ */ Kt(Ix);
var Wh = yn;
Object.defineProperty(fe, "__esModule", {
  value: !0
});
var ct = fe.alpha = Kh;
fe.blend = FS;
fe.colorChannel = void 0;
var il = fe.darken = fc;
fe.decomposeColor = ht;
fe.emphasize = Gh;
var MS = fe.getContrastRatio = bS;
fe.getLuminance = sl;
fe.hexToRgb = Uh;
fe.hslToRgb = Hh;
var ll = fe.lighten = pc;
fe.private_safeAlpha = IS;
fe.private_safeColorChannel = void 0;
fe.private_safeDarken = AS;
fe.private_safeEmphasize = DS;
fe.private_safeLighten = LS;
fe.recomposeColor = Tr;
fe.rgbToHex = NS;
var cf = Wh(TS), OS = Wh(RS);
function dc(e, t = 0, n = 1) {
  return (0, OS.default)(e, t, n);
}
function Uh(e) {
  e = e.slice(1);
  const t = new RegExp(`.{1,${e.length >= 6 ? 2 : 1}}`, "g");
  let n = e.match(t);
  return n && n[0].length === 1 && (n = n.map((r) => r + r)), n ? `rgb${n.length === 4 ? "a" : ""}(${n.map((r, o) => o < 3 ? parseInt(r, 16) : Math.round(parseInt(r, 16) / 255 * 1e3) / 1e3).join(", ")})` : "";
}
function jS(e) {
  const t = e.toString(16);
  return t.length === 1 ? `0${t}` : t;
}
function ht(e) {
  if (e.type)
    return e;
  if (e.charAt(0) === "#")
    return ht(Uh(e));
  const t = e.indexOf("("), n = e.substring(0, t);
  if (["rgb", "rgba", "hsl", "hsla", "color"].indexOf(n) === -1)
    throw new Error((0, cf.default)(9, e));
  let r = e.substring(t + 1, e.length - 1), o;
  if (n === "color") {
    if (r = r.split(" "), o = r.shift(), r.length === 4 && r[3].charAt(0) === "/" && (r[3] = r[3].slice(1)), ["srgb", "display-p3", "a98-rgb", "prophoto-rgb", "rec-2020"].indexOf(o) === -1)
      throw new Error((0, cf.default)(10, o));
  } else
    r = r.split(",");
  return r = r.map((i) => parseFloat(i)), {
    type: n,
    values: r,
    colorSpace: o
  };
}
const Vh = (e) => {
  const t = ht(e);
  return t.values.slice(0, 3).map((n, r) => t.type.indexOf("hsl") !== -1 && r !== 0 ? `${n}%` : n).join(" ");
};
fe.colorChannel = Vh;
const zS = (e, t) => {
  try {
    return Vh(e);
  } catch {
    return e;
  }
};
fe.private_safeColorChannel = zS;
function Tr(e) {
  const {
    type: t,
    colorSpace: n
  } = e;
  let {
    values: r
  } = e;
  return t.indexOf("rgb") !== -1 ? r = r.map((o, i) => i < 3 ? parseInt(o, 10) : o) : t.indexOf("hsl") !== -1 && (r[1] = `${r[1]}%`, r[2] = `${r[2]}%`), t.indexOf("color") !== -1 ? r = `${n} ${r.join(" ")}` : r = `${r.join(", ")}`, `${t}(${r})`;
}
function NS(e) {
  if (e.indexOf("#") === 0)
    return e;
  const {
    values: t
  } = ht(e);
  return `#${t.map((n, r) => jS(r === 3 ? Math.round(255 * n) : n)).join("")}`;
}
function Hh(e) {
  e = ht(e);
  const {
    values: t
  } = e, n = t[0], r = t[1] / 100, o = t[2] / 100, i = r * Math.min(o, 1 - o), l = (u, c = (u + n / 30) % 12) => o - i * Math.max(Math.min(c - 3, 9 - c, 1), -1);
  let s = "rgb";
  const a = [Math.round(l(0) * 255), Math.round(l(8) * 255), Math.round(l(4) * 255)];
  return e.type === "hsla" && (s += "a", a.push(t[3])), Tr({
    type: s,
    values: a
  });
}
function sl(e) {
  e = ht(e);
  let t = e.type === "hsl" || e.type === "hsla" ? ht(Hh(e)).values : e.values;
  return t = t.map((n) => (e.type !== "color" && (n /= 255), n <= 0.03928 ? n / 12.92 : ((n + 0.055) / 1.055) ** 2.4)), Number((0.2126 * t[0] + 0.7152 * t[1] + 0.0722 * t[2]).toFixed(3));
}
function bS(e, t) {
  const n = sl(e), r = sl(t);
  return (Math.max(n, r) + 0.05) / (Math.min(n, r) + 0.05);
}
function Kh(e, t) {
  return e = ht(e), t = dc(t), (e.type === "rgb" || e.type === "hsl") && (e.type += "a"), e.type === "color" ? e.values[3] = `/${t}` : e.values[3] = t, Tr(e);
}
function IS(e, t, n) {
  try {
    return Kh(e, t);
  } catch {
    return e;
  }
}
function fc(e, t) {
  if (e = ht(e), t = dc(t), e.type.indexOf("hsl") !== -1)
    e.values[2] *= 1 - t;
  else if (e.type.indexOf("rgb") !== -1 || e.type.indexOf("color") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] *= 1 - t;
  return Tr(e);
}
function AS(e, t, n) {
  try {
    return fc(e, t);
  } catch {
    return e;
  }
}
function pc(e, t) {
  if (e = ht(e), t = dc(t), e.type.indexOf("hsl") !== -1)
    e.values[2] += (100 - e.values[2]) * t;
  else if (e.type.indexOf("rgb") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] += (255 - e.values[n]) * t;
  else if (e.type.indexOf("color") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] += (1 - e.values[n]) * t;
  return Tr(e);
}
function LS(e, t, n) {
  try {
    return pc(e, t);
  } catch {
    return e;
  }
}
function Gh(e, t = 0.15) {
  return sl(e) > 0.5 ? fc(e, t) : pc(e, t);
}
function DS(e, t, n) {
  try {
    return Gh(e, t);
  } catch {
    return e;
  }
}
function FS(e, t, n, r = 1) {
  const o = (a, u) => Math.round((a ** (1 / r) * (1 - n) + u ** (1 / r) * n) ** r), i = ht(e), l = ht(t), s = [o(i.values[0], l.values[0]), o(i.values[1], l.values[1]), o(i.values[2], l.values[2])];
  return Tr({
    type: "rgb",
    values: s
  });
}
const BS = {
  black: "#000",
  white: "#fff"
}, Ro = BS, WS = {
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
}, US = WS, VS = {
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
}, Dn = VS, HS = {
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
}, Fn = HS, KS = {
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
}, Wr = KS, GS = {
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
}, Bn = GS, QS = {
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
}, Wn = QS, YS = {
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
}, Un = YS, XS = ["mode", "contrastThreshold", "tonalOffset"], df = {
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
    paper: Ro.white,
    default: Ro.white
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
}, Hs = {
  text: {
    primary: Ro.white,
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
    active: Ro.white,
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
function ff(e, t, n, r) {
  const o = r.light || r, i = r.dark || r * 1.5;
  e[t] || (e.hasOwnProperty(n) ? e[t] = e[n] : t === "light" ? e.light = ll(e.main, o) : t === "dark" && (e.dark = il(e.main, i)));
}
function qS(e = "light") {
  return e === "dark" ? {
    main: Bn[200],
    light: Bn[50],
    dark: Bn[400]
  } : {
    main: Bn[700],
    light: Bn[400],
    dark: Bn[800]
  };
}
function ZS(e = "light") {
  return e === "dark" ? {
    main: Dn[200],
    light: Dn[50],
    dark: Dn[400]
  } : {
    main: Dn[500],
    light: Dn[300],
    dark: Dn[700]
  };
}
function JS(e = "light") {
  return e === "dark" ? {
    main: Fn[500],
    light: Fn[300],
    dark: Fn[700]
  } : {
    main: Fn[700],
    light: Fn[400],
    dark: Fn[800]
  };
}
function e2(e = "light") {
  return e === "dark" ? {
    main: Wn[400],
    light: Wn[300],
    dark: Wn[700]
  } : {
    main: Wn[700],
    light: Wn[500],
    dark: Wn[900]
  };
}
function t2(e = "light") {
  return e === "dark" ? {
    main: Un[400],
    light: Un[300],
    dark: Un[700]
  } : {
    main: Un[800],
    light: Un[500],
    dark: Un[900]
  };
}
function n2(e = "light") {
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
function r2(e) {
  const {
    mode: t = "light",
    contrastThreshold: n = 3,
    tonalOffset: r = 0.2
  } = e, o = L(e, XS), i = e.primary || qS(t), l = e.secondary || ZS(t), s = e.error || JS(t), a = e.info || e2(t), u = e.success || t2(t), c = e.warning || n2(t);
  function d(g) {
    return MS(g, Hs.text.primary) >= n ? Hs.text.primary : df.text.primary;
  }
  const p = ({
    color: g,
    name: E,
    mainShade: m = 500,
    lightShade: f = 300,
    darkShade: h = 700
  }) => {
    if (g = w({}, g), !g.main && g[m] && (g.main = g[m]), !g.hasOwnProperty("main"))
      throw new Error(_o(11, E ? ` (${E})` : "", m));
    if (typeof g.main != "string")
      throw new Error(_o(12, E ? ` (${E})` : "", JSON.stringify(g.main)));
    return ff(g, "light", f, r), ff(g, "dark", h, r), g.contrastText || (g.contrastText = d(g.main)), g;
  }, v = {
    dark: Hs,
    light: df
  };
  return Nt(w({
    // A collection of common colors.
    common: w({}, Ro),
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
    grey: US,
    // Used by `getContrastText()` to maximize the contrast between
    // the background and the text.
    contrastThreshold: n,
    // Takes a background color and returns the text color that maximizes the contrast.
    getContrastText: d,
    // Generate a rich color object.
    augmentColor: p,
    // Used by the functions below to shift a color's luminance by approximately
    // two indexes within its tonal palette.
    // E.g., shift from Red 500 to Red 300 or Red 700.
    tonalOffset: r
  }, v[t]), o);
}
const o2 = ["fontFamily", "fontSize", "fontWeightLight", "fontWeightRegular", "fontWeightMedium", "fontWeightBold", "htmlFontSize", "allVariants", "pxToRem"];
function i2(e) {
  return Math.round(e * 1e5) / 1e5;
}
const pf = {
  textTransform: "uppercase"
}, mf = '"Roboto", "Helvetica", "Arial", sans-serif';
function l2(e, t) {
  const n = typeof t == "function" ? t(e) : t, {
    fontFamily: r = mf,
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
    pxToRem: d
  } = n, p = L(n, o2), v = o / 14, x = d || ((m) => `${m / u * v}rem`), g = (m, f, h, S, $) => w({
    fontFamily: r,
    fontWeight: m,
    fontSize: x(f),
    // Unitless following https://meyerweb.com/eric/thoughts/2006/02/08/unitless-line-heights/
    lineHeight: h
  }, r === mf ? {
    letterSpacing: `${i2(S / f)}em`
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
    button: g(s, 14, 1.75, 0.4, pf),
    caption: g(l, 12, 1.66, 0.4),
    overline: g(l, 12, 2.66, 1, pf),
    // TODO v6: Remove handling of 'inherit' variant from the theme as it is already handled in Material UI's Typography component. Also, remember to remove the associated types.
    inherit: {
      fontFamily: "inherit",
      fontWeight: "inherit",
      fontSize: "inherit",
      lineHeight: "inherit",
      letterSpacing: "inherit"
    }
  };
  return Nt(w({
    htmlFontSize: u,
    pxToRem: x,
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
const s2 = 0.2, a2 = 0.14, u2 = 0.12;
function te(...e) {
  return [`${e[0]}px ${e[1]}px ${e[2]}px ${e[3]}px rgba(0,0,0,${s2})`, `${e[4]}px ${e[5]}px ${e[6]}px ${e[7]}px rgba(0,0,0,${a2})`, `${e[8]}px ${e[9]}px ${e[10]}px ${e[11]}px rgba(0,0,0,${u2})`].join(",");
}
const c2 = ["none", te(0, 2, 1, -1, 0, 1, 1, 0, 0, 1, 3, 0), te(0, 3, 1, -2, 0, 2, 2, 0, 0, 1, 5, 0), te(0, 3, 3, -2, 0, 3, 4, 0, 0, 1, 8, 0), te(0, 2, 4, -1, 0, 4, 5, 0, 0, 1, 10, 0), te(0, 3, 5, -1, 0, 5, 8, 0, 0, 1, 14, 0), te(0, 3, 5, -1, 0, 6, 10, 0, 0, 1, 18, 0), te(0, 4, 5, -2, 0, 7, 10, 1, 0, 2, 16, 1), te(0, 5, 5, -3, 0, 8, 10, 1, 0, 3, 14, 2), te(0, 5, 6, -3, 0, 9, 12, 1, 0, 3, 16, 2), te(0, 6, 6, -3, 0, 10, 14, 1, 0, 4, 18, 3), te(0, 6, 7, -4, 0, 11, 15, 1, 0, 4, 20, 3), te(0, 7, 8, -4, 0, 12, 17, 2, 0, 5, 22, 4), te(0, 7, 8, -4, 0, 13, 19, 2, 0, 5, 24, 4), te(0, 7, 9, -4, 0, 14, 21, 2, 0, 5, 26, 4), te(0, 8, 9, -5, 0, 15, 22, 2, 0, 6, 28, 5), te(0, 8, 10, -5, 0, 16, 24, 2, 0, 6, 30, 5), te(0, 8, 11, -5, 0, 17, 26, 2, 0, 6, 32, 5), te(0, 9, 11, -5, 0, 18, 28, 2, 0, 7, 34, 6), te(0, 9, 12, -6, 0, 19, 29, 2, 0, 7, 36, 6), te(0, 10, 13, -6, 0, 20, 31, 3, 0, 8, 38, 7), te(0, 10, 13, -6, 0, 21, 33, 3, 0, 8, 40, 7), te(0, 10, 14, -6, 0, 22, 35, 3, 0, 8, 42, 7), te(0, 11, 14, -7, 0, 23, 36, 3, 0, 9, 44, 8), te(0, 11, 15, -7, 0, 24, 38, 3, 0, 9, 46, 8)], d2 = c2, f2 = ["duration", "easing", "delay"], p2 = {
  // This is the most common easing curve.
  easeInOut: "cubic-bezier(0.4, 0, 0.2, 1)",
  // Objects enter the screen at full velocity from off-screen and
  // slowly decelerate to a resting point.
  easeOut: "cubic-bezier(0.0, 0, 0.2, 1)",
  // Objects leave the screen at full velocity. They do not decelerate when off-screen.
  easeIn: "cubic-bezier(0.4, 0, 1, 1)",
  // The sharp curve is used by objects that may return to the screen at any time.
  sharp: "cubic-bezier(0.4, 0, 0.6, 1)"
}, m2 = {
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
function hf(e) {
  return `${Math.round(e)}ms`;
}
function h2(e) {
  if (!e)
    return 0;
  const t = e / 36;
  return Math.round((4 + 15 * t ** 0.25 + t / 5) * 10);
}
function g2(e) {
  const t = w({}, p2, e.easing), n = w({}, m2, e.duration);
  return w({
    getAutoHeightDuration: h2,
    create: (o = ["all"], i = {}) => {
      const {
        duration: l = n.standard,
        easing: s = t.easeInOut,
        delay: a = 0
      } = i;
      return L(i, f2), (Array.isArray(o) ? o : [o]).map((u) => `${u} ${typeof l == "string" ? l : hf(l)} ${s} ${typeof a == "string" ? a : hf(a)}`).join(",");
    }
  }, e, {
    easing: t,
    duration: n
  });
}
const v2 = {
  mobileStepper: 1e3,
  fab: 1050,
  speedDial: 1050,
  appBar: 1100,
  drawer: 1200,
  modal: 1300,
  snackbar: 1400,
  tooltip: 1500
}, y2 = v2, x2 = ["breakpoints", "mixins", "spacing", "palette", "transitions", "typography", "shape"];
function mc(e = {}, ...t) {
  const {
    mixins: n = {},
    palette: r = {},
    transitions: o = {},
    typography: i = {}
  } = e, l = L(e, x2);
  if (e.vars && // The error should throw only for the root theme creation because user is not allowed to use a custom node `vars`.
  // `generateCssVars` is the closest identifier for checking that the `options` is a result of `extendTheme` with CSS variables so that user can create new theme for nested ThemeProvider.
  e.generateCssVars === void 0)
    throw new Error(_o(18));
  const s = r2(r), a = Wo(e);
  let u = Nt(a, {
    mixins: PS(a.breakpoints, n),
    palette: s,
    // Don't use [...shadows] until you've verified its transpiled code is not invoking the iterator protocol.
    shadows: d2.slice(),
    typography: l2(s, i),
    transitions: g2(o),
    zIndex: w({}, y2)
  });
  return u = Nt(u, l), u = t.reduce((c, d) => Nt(c, d), u), u.unstable_sxConfig = w({}, Fo, l == null ? void 0 : l.unstable_sxConfig), u.unstable_sx = function(d) {
    return Bo({
      sx: d,
      theme: this
    });
  }, u;
}
const S2 = mc(), hc = S2;
function w2() {
  const e = Gl(hc);
  return e[yr] || e;
}
var Uo = {}, Ks = { exports: {} }, gf;
function C2() {
  return gf || (gf = 1, function(e) {
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
  }(Ks)), Ks.exports;
}
const k2 = /* @__PURE__ */ Kt(u1), _2 = /* @__PURE__ */ Kt(c1), $2 = /* @__PURE__ */ Kt(v1), E2 = /* @__PURE__ */ Kt(Sx), P2 = /* @__PURE__ */ Kt(ix), T2 = /* @__PURE__ */ Kt(cx);
var Rr = yn;
Object.defineProperty(Uo, "__esModule", {
  value: !0
});
var R2 = Uo.default = W2;
Uo.shouldForwardProp = Ri;
Uo.systemDefaultTheme = void 0;
var ot = Rr(xh()), Qa = Rr(C2()), al = I2(k2), M2 = _2;
Rr($2);
Rr(E2);
var O2 = Rr(P2), j2 = Rr(T2);
const z2 = ["ownerState"], N2 = ["variants"], b2 = ["name", "slot", "skipVariantsResolver", "skipSx", "overridesResolver"];
function Qh(e) {
  if (typeof WeakMap != "function")
    return null;
  var t = /* @__PURE__ */ new WeakMap(), n = /* @__PURE__ */ new WeakMap();
  return (Qh = function(r) {
    return r ? n : t;
  })(e);
}
function I2(e, t) {
  if (!t && e && e.__esModule)
    return e;
  if (e === null || typeof e != "object" && typeof e != "function")
    return { default: e };
  var n = Qh(t);
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
function A2(e) {
  return Object.keys(e).length === 0;
}
function L2(e) {
  return typeof e == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  e.charCodeAt(0) > 96;
}
function Ri(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
function vf(e, t) {
  return t && e && typeof e == "object" && e.styles && !e.styles.startsWith("@layer") && (e.styles = `@layer ${t}{${String(e.styles)}}`), e;
}
const D2 = Uo.systemDefaultTheme = (0, O2.default)(), F2 = (e) => e && e.charAt(0).toLowerCase() + e.slice(1);
function di({
  defaultTheme: e,
  theme: t,
  themeId: n
}) {
  return A2(t) ? e : t[n] || t;
}
function B2(e) {
  return e ? (t, n) => n[e] : null;
}
function Mi(e, t, n) {
  let {
    ownerState: r
  } = t, o = (0, Qa.default)(t, z2);
  const i = typeof e == "function" ? e((0, ot.default)({
    ownerState: r
  }, o)) : e;
  if (Array.isArray(i))
    return i.flatMap((l) => Mi(l, (0, ot.default)({
      ownerState: r
    }, o), n));
  if (i && typeof i == "object" && Array.isArray(i.variants)) {
    const {
      variants: l = []
    } = i;
    let a = (0, Qa.default)(i, N2);
    return l.forEach((u) => {
      let c = !0;
      if (typeof u.props == "function" ? c = u.props((0, ot.default)({
        ownerState: r
      }, o, r)) : Object.keys(u.props).forEach((d) => {
        (r == null ? void 0 : r[d]) !== u.props[d] && o[d] !== u.props[d] && (c = !1);
      }), c) {
        Array.isArray(a) || (a = [a]);
        const d = typeof u.style == "function" ? u.style((0, ot.default)({
          ownerState: r
        }, o, r)) : u.style;
        a.push(n ? vf((0, al.internal_serializeStyles)(d), n) : d);
      }
    }), a;
  }
  return n ? vf((0, al.internal_serializeStyles)(i), n) : i;
}
function W2(e = {}) {
  const {
    themeId: t,
    defaultTheme: n = D2,
    rootShouldForwardProp: r = Ri,
    slotShouldForwardProp: o = Ri
  } = e, i = (l) => (0, j2.default)((0, ot.default)({}, l, {
    theme: di((0, ot.default)({}, l, {
      defaultTheme: n,
      themeId: t
    }))
  }));
  return i.__mui_systemSx = !0, (l, s = {}) => {
    (0, al.internal_processStyles)(l, (k) => k.filter((C) => !(C != null && C.__mui_systemSx)));
    const {
      name: a,
      slot: u,
      skipVariantsResolver: c,
      skipSx: d,
      // TODO v6: remove `lowercaseFirstLetter()` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      overridesResolver: p = B2(F2(u))
    } = s, v = (0, Qa.default)(s, b2), x = a && a.startsWith("Mui") || u ? "components" : "custom", g = c !== void 0 ? c : (
      // TODO v6: remove `Root` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      u && u !== "Root" && u !== "root" || !1
    ), E = d || !1;
    let m, f = Ri;
    u === "Root" || u === "root" ? f = r : u ? f = o : L2(l) && (f = void 0);
    const h = (0, al.default)(l, (0, ot.default)({
      shouldForwardProp: f,
      label: m
    }, v)), S = (k) => typeof k == "function" && k.__emotion_real !== k || (0, M2.isPlainObject)(k) ? (C) => {
      const T = di({
        theme: C.theme,
        defaultTheme: n,
        themeId: t
      });
      return Mi(k, (0, ot.default)({}, C, {
        theme: T
      }), T.modularCssLayers ? x : void 0);
    } : k, $ = (k, ...C) => {
      let T = S(k);
      const j = C ? C.map(S) : [];
      a && p && j.push((F) => {
        const A = di((0, ot.default)({}, F, {
          defaultTheme: n,
          themeId: t
        }));
        if (!A.components || !A.components[a] || !A.components[a].styleOverrides)
          return null;
        const Z = A.components[a].styleOverrides, xe = {};
        return Object.entries(Z).forEach(([Ee, Ge]) => {
          xe[Ee] = Mi(Ge, (0, ot.default)({}, F, {
            theme: A
          }), A.modularCssLayers ? "theme" : void 0);
        }), p(F, xe);
      }), a && !g && j.push((F) => {
        var A;
        const Z = di((0, ot.default)({}, F, {
          defaultTheme: n,
          themeId: t
        })), xe = Z == null || (A = Z.components) == null || (A = A[a]) == null ? void 0 : A.variants;
        return Mi({
          variants: xe
        }, (0, ot.default)({}, F, {
          theme: Z
        }), Z.modularCssLayers ? "theme" : void 0);
      }), E || j.push(i);
      const M = j.length - C.length;
      if (Array.isArray(k) && M > 0) {
        const F = new Array(M).fill("");
        T = [...k, ...F], T.raw = [...k.raw, ...F];
      }
      const U = h(T, ...j);
      return l.muiName && (U.muiName = l.muiName), U;
    };
    return h.withConfig && ($.withConfig = h.withConfig), $;
  };
}
function U2(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
const V2 = (e) => U2(e) && e !== "classes", Yh = V2, H2 = R2({
  themeId: yr,
  defaultTheme: hc,
  rootShouldForwardProp: Yh
}), Y = H2, K2 = ["theme"];
function G2(e) {
  let {
    theme: t
  } = e, n = L(e, K2);
  const r = t[yr];
  let o = r || t;
  return typeof t != "function" && (r && !r.vars ? o = w({}, r, {
    vars: null
  }) : t && !t.vars && (o = w({}, t, {
    vars: null
  }))), /* @__PURE__ */ y.jsx(SS, w({}, n, {
    themeId: r ? yr : void 0,
    theme: o
  }));
}
const Q2 = (e) => {
  let t;
  return e < 1 ? t = 5.11916 * e ** 2 : t = 4.5 * Math.log(e + 1) + 2, (t / 100).toFixed(2);
}, yf = Q2;
function pe(e) {
  return yS(e);
}
function Y2(e) {
  return /* @__PURE__ */ y.jsx(Rh, w({}, e, {
    defaultTheme: hc,
    themeId: yr
  }));
}
const X2 = (e, t) => w({
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
}), q2 = (e) => w({
  color: (e.vars || e).palette.text.primary
}, e.typography.body1, {
  backgroundColor: (e.vars || e).palette.background.default,
  "@media print": {
    // Save printer ink.
    backgroundColor: (e.vars || e).palette.common.white
  }
}), Z2 = (e, t = !1) => {
  var n;
  const r = {};
  t && e.colorSchemes && Object.entries(e.colorSchemes).forEach(([l, s]) => {
    var a;
    r[e.getColorSchemeSelector(l).replace(/\s*&/, "")] = {
      colorScheme: (a = s.palette) == null ? void 0 : a.mode
    };
  });
  let o = w({
    html: X2(e, t),
    "*, *::before, *::after": {
      boxSizing: "inherit"
    },
    "strong, b": {
      fontWeight: e.typography.fontWeightBold
    },
    body: w({
      margin: 0
    }, q2(e), {
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
function J2(e) {
  const t = pe({
    props: e,
    name: "MuiCssBaseline"
  }), {
    children: n,
    enableColorScheme: r = !1
  } = t;
  return /* @__PURE__ */ y.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ y.jsx(Y2, {
      styles: (o) => Z2(o, r)
    }), n]
  });
}
const ew = ES({
  createStyledComponent: Y("div", {
    name: "MuiContainer",
    slot: "Root",
    overridesResolver: (e, t) => {
      const {
        ownerState: n
      } = e;
      return [t.root, t[`maxWidth${N(String(n.maxWidth))}`], n.fixed && t.fixed, n.disableGutters && t.disableGutters];
    }
  }),
  useThemeProps: (e) => pe({
    props: e,
    name: "MuiContainer"
  })
}), tw = ew;
function nw(e) {
  return ve("MuiTypography", e);
}
ye("MuiTypography", ["root", "h1", "h2", "h3", "h4", "h5", "h6", "subtitle1", "subtitle2", "body1", "body2", "inherit", "button", "caption", "overline", "alignLeft", "alignRight", "alignCenter", "alignJustify", "noWrap", "gutterBottom", "paragraph"]);
const rw = ["align", "className", "component", "gutterBottom", "noWrap", "paragraph", "variant", "variantMapping"], ow = (e) => {
  const {
    align: t,
    gutterBottom: n,
    noWrap: r,
    paragraph: o,
    variant: i,
    classes: l
  } = e, s = {
    root: ["root", i, e.align !== "inherit" && `align${N(t)}`, n && "gutterBottom", r && "noWrap", o && "paragraph"]
  };
  return Ce(s, nw, l);
}, iw = Y("span", {
  name: "MuiTypography",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.variant && t[n.variant], n.align !== "inherit" && t[`align${N(n.align)}`], n.noWrap && t.noWrap, n.gutterBottom && t.gutterBottom, n.paragraph && t.paragraph];
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
})), xf = {
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
}, lw = {
  primary: "primary.main",
  textPrimary: "text.primary",
  secondary: "secondary.main",
  textSecondary: "text.secondary",
  error: "error.main"
}, sw = (e) => lw[e] || e, aw = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = pe({
    props: t,
    name: "MuiTypography"
  }), o = sw(r.color), i = Ql(w({}, r, {
    color: o
  })), {
    align: l = "inherit",
    className: s,
    component: a,
    gutterBottom: u = !1,
    noWrap: c = !1,
    paragraph: d = !1,
    variant: p = "body1",
    variantMapping: v = xf
  } = i, x = L(i, rw), g = w({}, i, {
    align: l,
    color: o,
    className: s,
    component: a,
    gutterBottom: u,
    noWrap: c,
    paragraph: d,
    variant: p,
    variantMapping: v
  }), E = a || (d ? "p" : v[p] || xf[p]) || "span", m = ow(g);
  return /* @__PURE__ */ y.jsx(iw, w({
    as: E,
    ref: n,
    ownerState: g,
    className: B(m.root, s)
  }, x));
}), K = aw;
function uw(e) {
  return ve("MuiCircularProgress", e);
}
ye("MuiCircularProgress", ["root", "determinate", "indeterminate", "colorPrimary", "colorSecondary", "svg", "circle", "circleDeterminate", "circleIndeterminate", "circleDisableShrink"]);
const cw = ["className", "color", "disableShrink", "size", "style", "thickness", "value", "variant"];
let ss = (e) => e, Sf, wf, Cf, kf;
const Xt = 44, dw = Pr(Sf || (Sf = ss`
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
`)), fw = Pr(wf || (wf = ss`
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
`)), pw = (e) => {
  const {
    classes: t,
    variant: n,
    color: r,
    disableShrink: o
  } = e, i = {
    root: ["root", n, `color${N(r)}`],
    svg: ["svg"],
    circle: ["circle", `circle${N(n)}`, o && "circleDisableShrink"]
  };
  return Ce(i, uw, t);
}, mw = Y("span", {
  name: "MuiCircularProgress",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[n.variant], t[`color${N(n.color)}`]];
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
}) => e.variant === "indeterminate" && Dl(Cf || (Cf = ss`
      animation: ${0} 1.4s linear infinite;
    `), dw)), hw = Y("svg", {
  name: "MuiCircularProgress",
  slot: "Svg",
  overridesResolver: (e, t) => t.svg
})({
  display: "block"
  // Keeps the progress centered
}), gw = Y("circle", {
  name: "MuiCircularProgress",
  slot: "Circle",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.circle, t[`circle${N(n.variant)}`], n.disableShrink && t.circleDisableShrink];
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
}) => e.variant === "indeterminate" && !e.disableShrink && Dl(kf || (kf = ss`
      animation: ${0} 1.4s ease-in-out infinite;
    `), fw)), vw = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = pe({
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
    variant: d = "indeterminate"
  } = r, p = L(r, cw), v = w({}, r, {
    color: i,
    disableShrink: l,
    size: s,
    thickness: u,
    value: c,
    variant: d
  }), x = pw(v), g = {}, E = {}, m = {};
  if (d === "determinate") {
    const f = 2 * Math.PI * ((Xt - u) / 2);
    g.strokeDasharray = f.toFixed(3), m["aria-valuenow"] = Math.round(c), g.strokeDashoffset = `${((100 - c) / 100 * f).toFixed(3)}px`, E.transform = "rotate(-90deg)";
  }
  return /* @__PURE__ */ y.jsx(mw, w({
    className: B(x.root, o),
    style: w({
      width: s,
      height: s
    }, E, a),
    ownerState: v,
    ref: n,
    role: "progressbar"
  }, m, p, {
    children: /* @__PURE__ */ y.jsx(hw, {
      className: x.svg,
      ownerState: v,
      viewBox: `${Xt / 2} ${Xt / 2} ${Xt} ${Xt}`,
      children: /* @__PURE__ */ y.jsx(gw, {
        className: x.circle,
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
}), Xh = vw, yw = ["className", "elementType", "ownerState", "externalForwardedProps", "getSlotOwnerState", "internalForwardedProps"], xw = ["component", "slots", "slotProps"], Sw = ["component"];
function _f(e, t) {
  const {
    className: n,
    elementType: r,
    ownerState: o,
    externalForwardedProps: i,
    getSlotOwnerState: l,
    internalForwardedProps: s
  } = t, a = L(t, yw), {
    component: u,
    slots: c = {
      [e]: void 0
    },
    slotProps: d = {
      [e]: void 0
    }
  } = i, p = L(i, xw), v = c[e] || r, x = sS(d[e], o), g = lS(w({
    className: n
  }, a, {
    externalForwardedProps: e === "root" ? p : void 0,
    externalSlotProps: x
  })), {
    props: {
      component: E
    },
    internalRef: m
  } = g, f = L(g.props, Sw), h = ol(m, x == null ? void 0 : x.ref, t.ref), S = l ? l(f) : {}, $ = w({}, o, S), k = e === "root" ? E || u : E, C = oS(v, w({}, e === "root" && !u && !c[e] && s, e !== "root" && !c[e] && s, f, k && {
    as: k
  }, {
    ref: h
  }), $);
  return Object.keys(S).forEach((T) => {
    delete C[T];
  }), [v, C];
}
function ww(e) {
  return ve("MuiPaper", e);
}
ye("MuiPaper", ["root", "rounded", "outlined", "elevation", "elevation0", "elevation1", "elevation2", "elevation3", "elevation4", "elevation5", "elevation6", "elevation7", "elevation8", "elevation9", "elevation10", "elevation11", "elevation12", "elevation13", "elevation14", "elevation15", "elevation16", "elevation17", "elevation18", "elevation19", "elevation20", "elevation21", "elevation22", "elevation23", "elevation24"]);
const Cw = ["className", "component", "elevation", "square", "variant"], kw = (e) => {
  const {
    square: t,
    elevation: n,
    variant: r,
    classes: o
  } = e, i = {
    root: ["root", r, !t && "rounded", r === "elevation" && `elevation${n}`]
  };
  return Ce(i, ww, o);
}, _w = Y("div", {
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
    backgroundImage: `linear-gradient(${ct("#fff", yf(t.elevation))}, ${ct("#fff", yf(t.elevation))})`
  }, e.vars && {
    backgroundImage: (n = e.vars.overlays) == null ? void 0 : n[t.elevation]
  }));
}), $w = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = pe({
    props: t,
    name: "MuiPaper"
  }), {
    className: o,
    component: i = "div",
    elevation: l = 1,
    square: s = !1,
    variant: a = "elevation"
  } = r, u = L(r, Cw), c = w({}, r, {
    component: i,
    elevation: l,
    square: s,
    variant: a
  }), d = kw(c);
  return /* @__PURE__ */ y.jsx(_w, w({
    as: i,
    ownerState: c,
    className: B(d.root, o),
    ref: n
  }, u));
}), gc = $w;
function Ew(e) {
  return ve("MuiAlert", e);
}
const Pw = ye("MuiAlert", ["root", "action", "icon", "message", "filled", "colorSuccess", "colorInfo", "colorWarning", "colorError", "filledSuccess", "filledInfo", "filledWarning", "filledError", "outlined", "outlinedSuccess", "outlinedInfo", "outlinedWarning", "outlinedError", "standard", "standardSuccess", "standardInfo", "standardWarning", "standardError"]), $f = Pw;
function Ya(e, t) {
  return Ya = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, r) {
    return n.__proto__ = r, n;
  }, Ya(e, t);
}
function Tw(e, t) {
  e.prototype = Object.create(t.prototype), e.prototype.constructor = e, Ya(e, t);
}
const Ef = wn.createContext(null);
function Rw(e) {
  if (e === void 0)
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function vc(e, t) {
  var n = function(i) {
    return t && _.isValidElement(i) ? t(i) : i;
  }, r = /* @__PURE__ */ Object.create(null);
  return e && _.Children.map(e, function(o) {
    return o;
  }).forEach(function(o) {
    r[o.key] = n(o);
  }), r;
}
function Mw(e, t) {
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
function Ow(e, t) {
  return vc(e.children, function(n) {
    return _.cloneElement(n, {
      onExited: t.bind(null, n),
      in: !0,
      appear: $n(n, "appear", e),
      enter: $n(n, "enter", e),
      exit: $n(n, "exit", e)
    });
  });
}
function jw(e, t, n) {
  var r = vc(e.children), o = Mw(t, r);
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
}, yc = /* @__PURE__ */ function(e) {
  Tw(t, e);
  function t(r, o) {
    var i;
    i = e.call(this, r, o) || this;
    var l = i.handleExited.bind(Rw(i));
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
      children: a ? Ow(o, s) : jw(o, l, s),
      firstRender: !1
    };
  }, n.handleExited = function(o, i) {
    var l = vc(this.props.children);
    o.key in l || (o.props.onExited && o.props.onExited(i), this.mounted && this.setState(function(s) {
      var a = w({}, s.children);
      return delete a[o.key], {
        children: a
      };
    }));
  }, n.render = function() {
    var o = this.props, i = o.component, l = o.childFactory, s = L(o, ["component", "childFactory"]), a = this.state.contextValue, u = zw(this.state.children).map(l);
    return delete s.appear, delete s.enter, delete s.exit, i === null ? /* @__PURE__ */ wn.createElement(Ef.Provider, {
      value: a
    }, u) : /* @__PURE__ */ wn.createElement(Ef.Provider, {
      value: a
    }, /* @__PURE__ */ wn.createElement(i, s, u));
  }, t;
}(wn.Component);
yc.propTypes = {};
yc.defaultProps = Nw;
const bw = yc;
function Iw(e) {
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
  } = e, [c, d] = _.useState(!1), p = B(t, n.ripple, n.rippleVisible, r && n.ripplePulsate), v = {
    width: l,
    height: l,
    top: -(l / 2) + i,
    left: -(l / 2) + o
  }, x = B(n.child, c && n.childLeaving, r && n.childPulsate);
  return !s && !c && d(!0), _.useEffect(() => {
    if (!s && a != null) {
      const g = setTimeout(a, u);
      return () => {
        clearTimeout(g);
      };
    }
  }, [a, s, u]), /* @__PURE__ */ y.jsx("span", {
    className: p,
    style: v,
    children: /* @__PURE__ */ y.jsx("span", {
      className: x
    })
  });
}
const Aw = ye("MuiTouchRipple", ["root", "ripple", "rippleVisible", "ripplePulsate", "child", "childLeaving", "childPulsate"]), it = Aw, Lw = ["center", "classes", "className"];
let as = (e) => e, Pf, Tf, Rf, Mf;
const Xa = 550, Dw = 80, Fw = Pr(Pf || (Pf = as`
  0% {
    transform: scale(0);
    opacity: 0.1;
  }

  100% {
    transform: scale(1);
    opacity: 0.3;
  }
`)), Bw = Pr(Tf || (Tf = as`
  0% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
`)), Ww = Pr(Rf || (Rf = as`
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(0.92);
  }

  100% {
    transform: scale(1);
  }
`)), Uw = Y("span", {
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
}), Vw = Y(Iw, {
  name: "MuiTouchRipple",
  slot: "Ripple"
})(Mf || (Mf = as`
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
`), it.rippleVisible, Fw, Xa, ({
  theme: e
}) => e.transitions.easing.easeInOut, it.ripplePulsate, ({
  theme: e
}) => e.transitions.duration.shorter, it.child, it.childLeaving, Bw, Xa, ({
  theme: e
}) => e.transitions.easing.easeInOut, it.childPulsate, Ww, ({
  theme: e
}) => e.transitions.easing.easeInOut), Hw = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = pe({
    props: t,
    name: "MuiTouchRipple"
  }), {
    center: o = !1,
    classes: i = {},
    className: l
  } = r, s = L(r, Lw), [a, u] = _.useState([]), c = _.useRef(0), d = _.useRef(null);
  _.useEffect(() => {
    d.current && (d.current(), d.current = null);
  }, [a]);
  const p = _.useRef(!1), v = Yx(), x = _.useRef(null), g = _.useRef(null), E = _.useCallback((S) => {
    const {
      pulsate: $,
      rippleX: k,
      rippleY: C,
      rippleSize: T,
      cb: j
    } = S;
    u((M) => [...M, /* @__PURE__ */ y.jsx(Vw, {
      classes: {
        ripple: B(i.ripple, it.ripple),
        rippleVisible: B(i.rippleVisible, it.rippleVisible),
        ripplePulsate: B(i.ripplePulsate, it.ripplePulsate),
        child: B(i.child, it.child),
        childLeaving: B(i.childLeaving, it.childLeaving),
        childPulsate: B(i.childPulsate, it.childPulsate)
      },
      timeout: Xa,
      pulsate: $,
      rippleX: k,
      rippleY: C,
      rippleSize: T
    }, c.current)]), c.current += 1, d.current = j;
  }, [i]), m = _.useCallback((S = {}, $ = {}, k = () => {
  }) => {
    const {
      pulsate: C = !1,
      center: T = o || $.pulsate,
      fakeElement: j = !1
      // For test purposes
    } = $;
    if ((S == null ? void 0 : S.type) === "mousedown" && p.current) {
      p.current = !1;
      return;
    }
    (S == null ? void 0 : S.type) === "touchstart" && (p.current = !0);
    const M = j ? null : g.current, U = M ? M.getBoundingClientRect() : {
      width: 0,
      height: 0,
      left: 0,
      top: 0
    };
    let F, A, Z;
    if (T || S === void 0 || S.clientX === 0 && S.clientY === 0 || !S.clientX && !S.touches)
      F = Math.round(U.width / 2), A = Math.round(U.height / 2);
    else {
      const {
        clientX: xe,
        clientY: Ee
      } = S.touches && S.touches.length > 0 ? S.touches[0] : S;
      F = Math.round(xe - U.left), A = Math.round(Ee - U.top);
    }
    if (T)
      Z = Math.sqrt((2 * U.width ** 2 + U.height ** 2) / 3), Z % 2 === 0 && (Z += 1);
    else {
      const xe = Math.max(Math.abs((M ? M.clientWidth : 0) - F), F) * 2 + 2, Ee = Math.max(Math.abs((M ? M.clientHeight : 0) - A), A) * 2 + 2;
      Z = Math.sqrt(xe ** 2 + Ee ** 2);
    }
    S != null && S.touches ? x.current === null && (x.current = () => {
      E({
        pulsate: C,
        rippleX: F,
        rippleY: A,
        rippleSize: Z,
        cb: k
      });
    }, v.start(Dw, () => {
      x.current && (x.current(), x.current = null);
    })) : E({
      pulsate: C,
      rippleX: F,
      rippleY: A,
      rippleSize: Z,
      cb: k
    });
  }, [o, E, v]), f = _.useCallback(() => {
    m({}, {
      pulsate: !0
    });
  }, [m]), h = _.useCallback((S, $) => {
    if (v.clear(), (S == null ? void 0 : S.type) === "touchend" && x.current) {
      x.current(), x.current = null, v.start(0, () => {
        h(S, $);
      });
      return;
    }
    x.current = null, u((k) => k.length > 0 ? k.slice(1) : k), d.current = $;
  }, [v]);
  return _.useImperativeHandle(n, () => ({
    pulsate: f,
    start: m,
    stop: h
  }), [f, m, h]), /* @__PURE__ */ y.jsx(Uw, w({
    className: B(it.root, i.root, l),
    ref: g
  }, s, {
    children: /* @__PURE__ */ y.jsx(bw, {
      component: null,
      exit: !0,
      children: a
    })
  }));
}), Kw = Hw;
function Gw(e) {
  return ve("MuiButtonBase", e);
}
const Qw = ye("MuiButtonBase", ["root", "disabled", "focusVisible"]), Yw = Qw, Xw = ["action", "centerRipple", "children", "className", "component", "disabled", "disableRipple", "disableTouchRipple", "focusRipple", "focusVisibleClassName", "LinkComponent", "onBlur", "onClick", "onContextMenu", "onDragLeave", "onFocus", "onFocusVisible", "onKeyDown", "onKeyUp", "onMouseDown", "onMouseLeave", "onMouseUp", "onTouchEnd", "onTouchMove", "onTouchStart", "tabIndex", "TouchRippleProps", "touchRippleRef", "type"], qw = (e) => {
  const {
    disabled: t,
    focusVisible: n,
    focusVisibleClassName: r,
    classes: o
  } = e, l = Ce({
    root: ["root", t && "disabled", n && "focusVisible"]
  }, Gw, o);
  return n && r && (l.root += ` ${r}`), l;
}, Zw = Y("button", {
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
  [`&.${Yw.disabled}`]: {
    pointerEvents: "none",
    // Disable link interactions
    cursor: "default"
  },
  "@media print": {
    colorAdjust: "exact"
  }
}), Jw = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = pe({
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
    disableTouchRipple: d = !1,
    focusRipple: p = !1,
    LinkComponent: v = "a",
    onBlur: x,
    onClick: g,
    onContextMenu: E,
    onDragLeave: m,
    onFocus: f,
    onFocusVisible: h,
    onKeyDown: S,
    onKeyUp: $,
    onMouseDown: k,
    onMouseLeave: C,
    onMouseUp: T,
    onTouchEnd: j,
    onTouchMove: M,
    onTouchStart: U,
    tabIndex: F = 0,
    TouchRippleProps: A,
    touchRippleRef: Z,
    type: xe
  } = r, Ee = L(r, Xw), Ge = _.useRef(null), R = _.useRef(null), z = ol(R, Z), {
    isFocusVisibleRef: b,
    onFocus: re,
    onBlur: me,
    ref: In
  } = Ah(), [Ie, Qt] = _.useState(!1);
  u && Ie && Qt(!1), _.useImperativeHandle(o, () => ({
    focusVisible: () => {
      Qt(!0), Ge.current.focus();
    }
  }), []);
  const [yt, An] = _.useState(!1);
  _.useEffect(() => {
    An(!0);
  }, []);
  const l0 = yt && !c && !u;
  _.useEffect(() => {
    Ie && p && !c && yt && R.current.pulsate();
  }, [c, p, Ie, yt]);
  function bt(I, Pc, w0 = d) {
    return Yr((Tc) => (Pc && Pc(Tc), !w0 && R.current && R.current[I](Tc), !0));
  }
  const s0 = bt("start", k), a0 = bt("stop", E), u0 = bt("stop", m), c0 = bt("stop", T), d0 = bt("stop", (I) => {
    Ie && I.preventDefault(), C && C(I);
  }), f0 = bt("start", U), p0 = bt("stop", j), m0 = bt("stop", M), h0 = bt("stop", (I) => {
    me(I), b.current === !1 && Qt(!1), x && x(I);
  }, !1), g0 = Yr((I) => {
    Ge.current || (Ge.current = I.currentTarget), re(I), b.current === !0 && (Qt(!0), h && h(I)), f && f(I);
  }), ds = () => {
    const I = Ge.current;
    return a && a !== "button" && !(I.tagName === "A" && I.href);
  }, fs = _.useRef(!1), v0 = Yr((I) => {
    p && !fs.current && Ie && R.current && I.key === " " && (fs.current = !0, R.current.stop(I, () => {
      R.current.start(I);
    })), I.target === I.currentTarget && ds() && I.key === " " && I.preventDefault(), S && S(I), I.target === I.currentTarget && ds() && I.key === "Enter" && !u && (I.preventDefault(), g && g(I));
  }), y0 = Yr((I) => {
    p && I.key === " " && R.current && Ie && !I.defaultPrevented && (fs.current = !1, R.current.stop(I, () => {
      R.current.pulsate(I);
    })), $ && $(I), g && I.target === I.currentTarget && ds() && I.key === " " && !I.defaultPrevented && g(I);
  });
  let Vo = a;
  Vo === "button" && (Ee.href || Ee.to) && (Vo = v);
  const jr = {};
  Vo === "button" ? (jr.type = xe === void 0 ? "button" : xe, jr.disabled = u) : (!Ee.href && !Ee.to && (jr.role = "button"), u && (jr["aria-disabled"] = u));
  const x0 = ol(n, In, Ge), Ec = w({}, r, {
    centerRipple: i,
    component: a,
    disabled: u,
    disableRipple: c,
    disableTouchRipple: d,
    focusRipple: p,
    tabIndex: F,
    focusVisible: Ie
  }), S0 = qw(Ec);
  return /* @__PURE__ */ y.jsxs(Zw, w({
    as: Vo,
    className: B(S0.root, s),
    ownerState: Ec,
    onBlur: h0,
    onClick: g,
    onContextMenu: a0,
    onFocus: g0,
    onKeyDown: v0,
    onKeyUp: y0,
    onMouseDown: s0,
    onMouseLeave: d0,
    onMouseUp: c0,
    onDragLeave: u0,
    onTouchEnd: p0,
    onTouchMove: m0,
    onTouchStart: f0,
    ref: x0,
    tabIndex: u ? -1 : F,
    type: xe
  }, jr, Ee, {
    children: [l, l0 ? (
      /* TouchRipple is only needed client-side, x2 boost on the server. */
      /* @__PURE__ */ y.jsx(Kw, w({
        ref: z,
        center: i
      }, A))
    ) : null]
  }));
}), xc = Jw;
function eC(e) {
  return ve("MuiIconButton", e);
}
const tC = ye("MuiIconButton", ["root", "disabled", "colorInherit", "colorPrimary", "colorSecondary", "colorError", "colorInfo", "colorSuccess", "colorWarning", "edgeStart", "edgeEnd", "sizeSmall", "sizeMedium", "sizeLarge"]), nC = tC, rC = ["edge", "children", "className", "color", "disabled", "disableFocusRipple", "size"], oC = (e) => {
  const {
    classes: t,
    disabled: n,
    color: r,
    edge: o,
    size: i
  } = e, l = {
    root: ["root", n && "disabled", r !== "default" && `color${N(r)}`, o && `edge${N(o)}`, `size${N(i)}`]
  };
  return Ce(l, eC, t);
}, iC = Y(xc, {
  name: "MuiIconButton",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.color !== "default" && t[`color${N(n.color)}`], n.edge && t[`edge${N(n.edge)}`], t[`size${N(n.size)}`]];
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
    backgroundColor: e.vars ? `rgba(${e.vars.palette.action.activeChannel} / ${e.vars.palette.action.hoverOpacity})` : ct(e.palette.action.active, e.palette.action.hoverOpacity),
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
      backgroundColor: e.vars ? `rgba(${r.mainChannel} / ${e.vars.palette.action.hoverOpacity})` : ct(r.main, e.palette.action.hoverOpacity)
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
    [`&.${nC.disabled}`]: {
      backgroundColor: "transparent",
      color: (e.vars || e).palette.action.disabled
    }
  });
}), lC = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = pe({
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
  } = r, d = L(r, rC), p = w({}, r, {
    edge: o,
    color: s,
    disabled: a,
    disableFocusRipple: u,
    size: c
  }), v = oC(p);
  return /* @__PURE__ */ y.jsx(iC, w({
    className: B(v.root, l),
    centerRipple: !0,
    focusRipple: !u,
    disabled: a,
    ref: n
  }, d, {
    ownerState: p,
    children: i
  }));
}), sC = lC;
function aC(e) {
  return ve("MuiSvgIcon", e);
}
ye("MuiSvgIcon", ["root", "colorPrimary", "colorSecondary", "colorAction", "colorError", "colorDisabled", "fontSizeInherit", "fontSizeSmall", "fontSizeMedium", "fontSizeLarge"]);
const uC = ["children", "className", "color", "component", "fontSize", "htmlColor", "inheritViewBox", "titleAccess", "viewBox"], cC = (e) => {
  const {
    color: t,
    fontSize: n,
    classes: r
  } = e, o = {
    root: ["root", t !== "inherit" && `color${N(t)}`, `fontSize${N(n)}`]
  };
  return Ce(o, aC, r);
}, dC = Y("svg", {
  name: "MuiSvgIcon",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.color !== "inherit" && t[`color${N(n.color)}`], t[`fontSize${N(n.fontSize)}`]];
  }
})(({
  theme: e,
  ownerState: t
}) => {
  var n, r, o, i, l, s, a, u, c, d, p, v, x;
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
    color: (d = (p = (e.vars || e).palette) == null || (p = p[t.color]) == null ? void 0 : p.main) != null ? d : {
      action: (v = (e.vars || e).palette) == null || (v = v.action) == null ? void 0 : v.active,
      disabled: (x = (e.vars || e).palette) == null || (x = x.action) == null ? void 0 : x.disabled,
      inherit: void 0
    }[t.color]
  };
}), qh = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = pe({
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
    titleAccess: d,
    viewBox: p = "0 0 24 24"
  } = r, v = L(r, uC), x = /* @__PURE__ */ _.isValidElement(o) && o.type === "svg", g = w({}, r, {
    color: l,
    component: s,
    fontSize: a,
    instanceFontSize: t.fontSize,
    inheritViewBox: c,
    viewBox: p,
    hasSvgAsChild: x
  }), E = {};
  c || (E.viewBox = p);
  const m = cC(g);
  return /* @__PURE__ */ y.jsxs(dC, w({
    as: s,
    className: B(m.root, i),
    focusable: "false",
    color: u,
    "aria-hidden": d ? void 0 : !0,
    role: d ? "img" : void 0,
    ref: n
  }, E, v, x && o.props, {
    ownerState: g,
    children: [x ? o.props.children : o, d ? /* @__PURE__ */ y.jsx("title", {
      children: d
    }) : null]
  }));
});
qh.muiName = "SvgIcon";
const Of = qh;
function Mr(e, t) {
  function n(r, o) {
    return /* @__PURE__ */ y.jsx(Of, w({
      "data-testid": `${t}Icon`,
      ref: o
    }, r, {
      children: e
    }));
  }
  return n.muiName = Of.muiName, /* @__PURE__ */ _.memo(/* @__PURE__ */ _.forwardRef(n));
}
const fC = Mr(/* @__PURE__ */ y.jsx("path", {
  d: "M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2, 4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0, 0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"
}), "SuccessOutlined"), pC = Mr(/* @__PURE__ */ y.jsx("path", {
  d: "M12 5.99L19.53 19H4.47L12 5.99M12 2L1 21h22L12 2zm1 14h-2v2h2v-2zm0-6h-2v4h2v-4z"
}), "ReportProblemOutlined"), mC = Mr(/* @__PURE__ */ y.jsx("path", {
  d: "M11 15h2v2h-2zm0-8h2v6h-2zm.99-5C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"
}), "ErrorOutline"), hC = Mr(/* @__PURE__ */ y.jsx("path", {
  d: "M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"
}), "InfoOutlined"), gC = Mr(/* @__PURE__ */ y.jsx("path", {
  d: "M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
}), "Close"), vC = ["action", "children", "className", "closeText", "color", "components", "componentsProps", "icon", "iconMapping", "onClose", "role", "severity", "slotProps", "slots", "variant"], yC = (e) => {
  const {
    variant: t,
    color: n,
    severity: r,
    classes: o
  } = e, i = {
    root: ["root", `color${N(n || r)}`, `${t}${N(n || r)}`, `${t}`],
    icon: ["icon"],
    message: ["message"],
    action: ["action"]
  };
  return Ce(i, Ew, o);
}, xC = Y(gc, {
  name: "MuiAlert",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[n.variant], t[`${n.variant}${N(n.color || n.severity)}`]];
  }
})(({
  theme: e
}) => {
  const t = e.palette.mode === "light" ? il : ll, n = e.palette.mode === "light" ? ll : il;
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
        [`& .${$f.icon}`]: e.vars ? {
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
        [`& .${$f.icon}`]: e.vars ? {
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
}), SC = Y("div", {
  name: "MuiAlert",
  slot: "Icon",
  overridesResolver: (e, t) => t.icon
})({
  marginRight: 12,
  padding: "7px 0",
  display: "flex",
  fontSize: 22,
  opacity: 0.9
}), wC = Y("div", {
  name: "MuiAlert",
  slot: "Message",
  overridesResolver: (e, t) => t.message
})({
  padding: "8px 0",
  minWidth: 0,
  overflow: "auto"
}), jf = Y("div", {
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
  success: /* @__PURE__ */ y.jsx(fC, {
    fontSize: "inherit"
  }),
  warning: /* @__PURE__ */ y.jsx(pC, {
    fontSize: "inherit"
  }),
  error: /* @__PURE__ */ y.jsx(mC, {
    fontSize: "inherit"
  }),
  info: /* @__PURE__ */ y.jsx(hC, {
    fontSize: "inherit"
  })
}, CC = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = pe({
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
    icon: d,
    iconMapping: p = zf,
    onClose: v,
    role: x = "alert",
    severity: g = "success",
    slotProps: E = {},
    slots: m = {},
    variant: f = "standard"
  } = r, h = L(r, vC), S = w({}, r, {
    color: a,
    severity: g,
    variant: f,
    colorSeverity: a || g
  }), $ = yC(S), k = {
    slots: w({
      closeButton: u.CloseButton,
      closeIcon: u.CloseIcon
    }, m),
    slotProps: w({}, c, E)
  }, [C, T] = _f("closeButton", {
    elementType: sC,
    externalForwardedProps: k,
    ownerState: S
  }), [j, M] = _f("closeIcon", {
    elementType: gC,
    externalForwardedProps: k,
    ownerState: S
  });
  return /* @__PURE__ */ y.jsxs(xC, w({
    role: x,
    elevation: 0,
    ownerState: S,
    className: B($.root, l),
    ref: n
  }, h, {
    children: [d !== !1 ? /* @__PURE__ */ y.jsx(SC, {
      ownerState: S,
      className: $.icon,
      children: d || p[g] || zf[g]
    }) : null, /* @__PURE__ */ y.jsx(wC, {
      ownerState: S,
      className: $.message,
      children: i
    }), o != null ? /* @__PURE__ */ y.jsx(jf, {
      ownerState: S,
      className: $.action,
      children: o
    }) : null, o == null && v ? /* @__PURE__ */ y.jsx(jf, {
      ownerState: S,
      className: $.action,
      children: /* @__PURE__ */ y.jsx(C, w({
        size: "small",
        "aria-label": s,
        title: s,
        color: "inherit",
        onClick: v
      }, T, {
        children: /* @__PURE__ */ y.jsx(j, w({
          fontSize: "small"
        }, M))
      }))
    }) : null]
  }));
}), kC = CC, _C = ye("MuiBox", ["root"]), $C = _C, EC = mc(), PC = mx({
  themeId: yr,
  defaultTheme: EC,
  defaultClassName: $C.root,
  generateClassName: sc.generate
}), zn = PC, TC = /* @__PURE__ */ _.createContext(), Nf = TC;
function RC(e) {
  return ve("MuiGrid", e);
}
const MC = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], OC = ["column-reverse", "column", "row-reverse", "row"], jC = ["nowrap", "wrap-reverse", "wrap"], Ur = ["auto", !0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], zC = ye("MuiGrid", [
  "root",
  "container",
  "item",
  "zeroMinWidth",
  // spacings
  ...MC.map((e) => `spacing-xs-${e}`),
  // direction values
  ...OC.map((e) => `direction-xs-${e}`),
  // wrap values
  ...jC.map((e) => `wrap-xs-${e}`),
  // grid sizes for all breakpoints
  ...Ur.map((e) => `grid-xs-${e}`),
  ...Ur.map((e) => `grid-sm-${e}`),
  ...Ur.map((e) => `grid-md-${e}`),
  ...Ur.map((e) => `grid-lg-${e}`),
  ...Ur.map((e) => `grid-xl-${e}`)
]), Mo = zC, NC = ["className", "columns", "columnSpacing", "component", "container", "direction", "item", "rowSpacing", "spacing", "wrap", "zeroMinWidth"];
function cr(e) {
  const t = parseFloat(e);
  return `${t}${String(e).replace(String(t), "") || "px"}`;
}
function bC({
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
          const d = `calc(${a} + ${cr(c)})`;
          u = {
            flexBasis: d,
            maxWidth: d
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
function IC({
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
function Zh({
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
    const i = Fl({
      values: r,
      breakpoints: e.breakpoints.values
    });
    let l;
    typeof i == "object" && (l = Zh({
      breakpoints: e.breakpoints.values,
      values: i
    })), o = mt({
      theme: e
    }, i, (s, a) => {
      var u;
      const c = e.spacing(s);
      return c !== "0px" ? {
        marginTop: `-${cr(c)}`,
        [`& > .${Mo.item}`]: {
          paddingTop: cr(c)
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
function LC({
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
    typeof i == "object" && (l = Zh({
      breakpoints: e.breakpoints.values,
      values: i
    })), o = mt({
      theme: e
    }, i, (s, a) => {
      var u;
      const c = e.spacing(s);
      return c !== "0px" ? {
        width: `calc(100% + ${cr(c)})`,
        marginLeft: `-${cr(c)}`,
        [`& > .${Mo.item}`]: {
          paddingLeft: cr(c)
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
function DC(e, t, n = {}) {
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
const FC = Y("div", {
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
    r && (c = DC(l, u, t));
    const d = [];
    return u.forEach((p) => {
      const v = n[p];
      v && d.push(t[`grid-${p}-${String(v)}`]);
    }), [t.root, r && t.container, i && t.item, a && t.zeroMinWidth, ...c, o !== "row" && t[`direction-xs-${String(o)}`], s !== "wrap" && t[`wrap-xs-${String(s)}`], ...d];
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
}), IC, AC, LC, bC);
function BC(e, t) {
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
const WC = (e) => {
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
  n && (u = BC(i, a));
  const c = [];
  a.forEach((p) => {
    const v = e[p];
    v && c.push(`grid-${p}-${String(v)}`);
  });
  const d = {
    root: ["root", n && "container", o && "item", s && "zeroMinWidth", ...u, r !== "row" && `direction-xs-${String(r)}`, l !== "wrap" && `wrap-xs-${String(l)}`, ...c]
  };
  return Ce(d, RC, t);
}, UC = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = pe({
    props: t,
    name: "MuiGrid"
  }), {
    breakpoints: o
  } = w2(), i = Ql(r), {
    className: l,
    columns: s,
    columnSpacing: a,
    component: u = "div",
    container: c = !1,
    direction: d = "row",
    item: p = !1,
    rowSpacing: v,
    spacing: x = 0,
    wrap: g = "wrap",
    zeroMinWidth: E = !1
  } = i, m = L(i, NC), f = v || x, h = a || x, S = _.useContext(Nf), $ = c ? s || 12 : S, k = {}, C = w({}, m);
  o.keys.forEach((M) => {
    m[M] != null && (k[M] = m[M], delete C[M]);
  });
  const T = w({}, i, {
    columns: $,
    container: c,
    direction: d,
    item: p,
    rowSpacing: f,
    columnSpacing: h,
    wrap: g,
    zeroMinWidth: E,
    spacing: x
  }, k, {
    breakpoints: o.keys
  }), j = WC(T);
  return /* @__PURE__ */ y.jsx(Nf.Provider, {
    value: $,
    children: /* @__PURE__ */ y.jsx(FC, w({
      ownerState: T,
      className: B(j.root, l),
      as: u,
      ref: n
    }, C))
  });
}), Qe = UC;
function VC(e) {
  return ve("MuiCard", e);
}
ye("MuiCard", ["root"]);
const HC = ["className", "raised"], KC = (e) => {
  const {
    classes: t
  } = e;
  return Ce({
    root: ["root"]
  }, VC, t);
}, GC = Y(gc, {
  name: "MuiCard",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})(() => ({
  overflow: "hidden"
})), QC = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = pe({
    props: t,
    name: "MuiCard"
  }), {
    className: o,
    raised: i = !1
  } = r, l = L(r, HC), s = w({}, r, {
    raised: i
  }), a = KC(s);
  return /* @__PURE__ */ y.jsx(GC, w({
    className: B(a.root, o),
    elevation: i ? 8 : void 0,
    ref: n,
    ownerState: s
  }, l));
}), Sr = QC;
function YC(e) {
  return ve("MuiCardActionArea", e);
}
const XC = ye("MuiCardActionArea", ["root", "focusVisible", "focusHighlight"]), Gs = XC, qC = ["children", "className", "focusVisibleClassName"], ZC = (e) => {
  const {
    classes: t
  } = e;
  return Ce({
    root: ["root"],
    focusHighlight: ["focusHighlight"]
  }, YC, t);
}, JC = Y(xc, {
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
  [`&:hover .${Gs.focusHighlight}`]: {
    opacity: (e.vars || e).palette.action.hoverOpacity,
    "@media (hover: none)": {
      opacity: 0
    }
  },
  [`&.${Gs.focusVisible} .${Gs.focusHighlight}`]: {
    opacity: (e.vars || e).palette.action.focusOpacity
  }
})), ek = Y("span", {
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
})), tk = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = pe({
    props: t,
    name: "MuiCardActionArea"
  }), {
    children: o,
    className: i,
    focusVisibleClassName: l
  } = r, s = L(r, qC), a = r, u = ZC(a);
  return /* @__PURE__ */ y.jsxs(JC, w({
    className: B(u.root, i),
    focusVisibleClassName: B(l, u.focusVisible),
    ref: n,
    ownerState: a
  }, s, {
    children: [o, /* @__PURE__ */ y.jsx(ek, {
      className: u.focusHighlight,
      ownerState: a
    })]
  }));
}), bf = tk;
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
}, ik = Y("div", {
  name: "MuiCardContent",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})(() => ({
  padding: 16,
  "&:last-child": {
    paddingBottom: 24
  }
})), lk = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = pe({
    props: t,
    name: "MuiCardContent"
  }), {
    className: o,
    component: i = "div"
  } = r, l = L(r, rk), s = w({}, r, {
    component: i
  }), a = ok(s);
  return /* @__PURE__ */ y.jsx(ik, w({
    as: i,
    className: B(a.root, o),
    ownerState: s,
    ref: n
  }, l));
}), wr = lk;
var Sc = {}, Qs = {};
const sk = {
  configure: (e) => {
    sc.configure(e);
  }
}, ak = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  capitalize: N,
  createChainedFunction: Ax,
  createSvgIcon: Mr,
  debounce: Lx,
  deprecatedPropType: Dx,
  isMuiElement: Fx,
  ownerDocument: Nh,
  ownerWindow: Bx,
  requirePropFactory: Wx,
  setRef: bh,
  unstable_ClassNameGenerator: sk,
  unstable_useEnhancedEffect: cc,
  unstable_useId: Ih,
  unsupportedProp: Vx,
  useControlled: Hx,
  useEventCallback: Yr,
  useForkRef: ol,
  useIsFocusVisible: Ah
}, Symbol.toStringTag, { value: "Module" })), uk = /* @__PURE__ */ Kt(ak);
var If;
function Or() {
  return If || (If = 1, function(e) {
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
  }(Qs)), Qs;
}
var ck = yn;
Object.defineProperty(Sc, "__esModule", {
  value: !0
});
var Jh = Sc.default = void 0, dk = ck(Or()), fk = y;
Jh = Sc.default = (0, dk.default)(/* @__PURE__ */ (0, fk.jsx)("path", {
  d: "M4 6h18V4H4c-1.1 0-2 .9-2 2v11H0v3h14v-3H4zm19 2h-6c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h6c.55 0 1-.45 1-1V9c0-.55-.45-1-1-1m-1 9h-4v-7h4z"
}), "Devices");
var wc = {}, pk = yn;
Object.defineProperty(wc, "__esModule", {
  value: !0
});
var e0 = wc.default = void 0, mk = pk(Or()), hk = y;
e0 = wc.default = (0, mk.default)(/* @__PURE__ */ (0, hk.jsx)("path", {
  d: "m1 9 2 2c4.97-4.97 13.03-4.97 18 0l2-2C16.93 2.93 7.08 2.93 1 9m8 8 3 3 3-3c-1.65-1.66-4.34-1.66-6 0m-4-4 2 2c2.76-2.76 7.24-2.76 10 0l2-2C15.14 9.14 8.87 9.14 5 13"
}), "Wifi");
var Cc = {}, gk = yn;
Object.defineProperty(Cc, "__esModule", {
  value: !0
});
var t0 = Cc.default = void 0, vk = gk(Or()), yk = y;
t0 = Cc.default = (0, vk.default)(/* @__PURE__ */ (0, yk.jsx)("path", {
  d: "m20.2 5.9.8-.8C19.6 3.7 17.8 3 16 3s-3.6.7-5 2.1l.8.8C13 4.8 14.5 4.2 16 4.2s3 .6 4.2 1.7m-.9.8c-.9-.9-2.1-1.4-3.3-1.4s-2.4.5-3.3 1.4l.8.8c.7-.7 1.6-1 2.5-1 .9 0 1.8.3 2.5 1zM19 13h-2V9h-2v4H5c-1.1 0-2 .9-2 2v4c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-4c0-1.1-.9-2-2-2M8 18H6v-2h2zm3.5 0h-2v-2h2zm3.5 0h-2v-2h2z"
}), "Router");
var kc = {}, xk = yn;
Object.defineProperty(kc, "__esModule", {
  value: !0
});
var n0 = kc.default = void 0, Sk = xk(Or()), wk = y;
n0 = kc.default = (0, Sk.default)(/* @__PURE__ */ (0, wk.jsx)("path", {
  d: "M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11z"
}), "Videocam");
var _c = {}, Ck = yn;
Object.defineProperty(_c, "__esModule", {
  value: !0
});
var r0 = _c.default = void 0, kk = Ck(Or()), _k = y;
r0 = _c.default = (0, kk.default)(/* @__PURE__ */ (0, _k.jsx)("path", {
  d: "M12 11c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m6 2c0-3.31-2.69-6-6-6s-6 2.69-6 6c0 2.22 1.21 4.15 3 5.19l1-1.74c-1.19-.7-2-1.97-2-3.45 0-2.21 1.79-4 4-4s4 1.79 4 4c0 1.48-.81 2.75-2 3.45l1 1.74c1.79-1.04 3-2.97 3-5.19M12 3C6.48 3 2 7.48 2 13c0 3.7 2.01 6.92 4.99 8.65l1-1.73C5.61 18.53 4 15.96 4 13c0-4.42 3.58-8 8-8s8 3.58 8 8c0 2.96-1.61 5.53-4 6.92l1 1.73c2.99-1.73 5-4.95 5-8.65 0-5.52-4.48-10-10-10"
}), "WifiTethering");
const Vr = ({ title: e, value: t, icon: n }) => /* @__PURE__ */ y.jsx(Sr, { children: /* @__PURE__ */ y.jsx(wr, { children: /* @__PURE__ */ y.jsxs(zn, { sx: { display: "flex", alignItems: "center" }, children: [
  /* @__PURE__ */ y.jsx(zn, { sx: { fontSize: "1.5rem", mr: 2 }, children: n }),
  /* @__PURE__ */ y.jsxs("div", { children: [
    /* @__PURE__ */ y.jsx(K, { color: "text.secondary", children: e }),
    /* @__PURE__ */ y.jsx(K, { variant: "h5", component: "div", children: t })
  ] })
] }) }) }), $k = /* @__PURE__ */ _.createContext(), o0 = $k;
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
}, Rk = Y("table", {
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
})), Af = "table", Mk = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = pe({
    props: t,
    name: "MuiTable"
  }), {
    className: o,
    component: i = Af,
    padding: l = "normal",
    size: s = "medium",
    stickyHeader: a = !1
  } = r, u = L(r, Pk), c = w({}, r, {
    component: i,
    padding: l,
    size: s,
    stickyHeader: a
  }), d = Tk(c), p = _.useMemo(() => ({
    padding: l,
    size: s,
    stickyHeader: a
  }), [l, s, a]);
  return /* @__PURE__ */ y.jsx(o0.Provider, {
    value: p,
    children: /* @__PURE__ */ y.jsx(Rk, w({
      as: i,
      role: i === Af ? null : "table",
      ref: n,
      className: B(d.root, o),
      ownerState: c
    }, u))
  });
}), Ok = Mk, jk = /* @__PURE__ */ _.createContext(), us = jk;
function zk(e) {
  return ve("MuiTableBody", e);
}
ye("MuiTableBody", ["root"]);
const Nk = ["className", "component"], bk = (e) => {
  const {
    classes: t
  } = e;
  return Ce({
    root: ["root"]
  }, zk, t);
}, Ik = Y("tbody", {
  name: "MuiTableBody",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})({
  display: "table-row-group"
}), Ak = {
  variant: "body"
}, Lf = "tbody", Lk = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = pe({
    props: t,
    name: "MuiTableBody"
  }), {
    className: o,
    component: i = Lf
  } = r, l = L(r, Nk), s = w({}, r, {
    component: i
  }), a = bk(s);
  return /* @__PURE__ */ y.jsx(us.Provider, {
    value: Ak,
    children: /* @__PURE__ */ y.jsx(Ik, w({
      className: B(a.root, o),
      as: i,
      ref: n,
      role: i === Lf ? null : "rowgroup",
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
    root: ["root", n, l && "stickyHeader", r !== "inherit" && `align${N(r)}`, o !== "normal" && `padding${N(o)}`, `size${N(i)}`]
  };
  return Ce(s, Fk, t);
}, Hk = Y("td", {
  name: "MuiTableCell",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[n.variant], t[`size${N(n.size)}`], n.padding !== "normal" && t[`padding${N(n.padding)}`], n.align !== "inherit" && t[`align${N(n.align)}`], n.stickyHeader && t.stickyHeader];
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
    ${e.palette.mode === "light" ? ll(ct(e.palette.divider, 1), 0.88) : il(ct(e.palette.divider, 1), 0.68)}`,
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
  const r = pe({
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
    variant: d
  } = r, p = L(r, Uk), v = _.useContext(o0), x = _.useContext(us), g = x && x.variant === "head";
  let E;
  l ? E = l : E = g ? "th" : "td";
  let m = a;
  E === "td" ? m = void 0 : !m && g && (m = "col");
  const f = d || x && x.variant, h = w({}, r, {
    align: o,
    component: E,
    padding: s || (v && v.padding ? v.padding : "normal"),
    size: u || (v && v.size ? v.size : "medium"),
    sortDirection: c,
    stickyHeader: f === "head" && v && v.stickyHeader,
    variant: f
  }), S = Vk(h);
  let $ = null;
  return c && ($ = c === "asc" ? "ascending" : "descending"), /* @__PURE__ */ y.jsx(Hk, w({
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
}, Xk = Y("div", {
  name: "MuiTableContainer",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})({
  width: "100%",
  overflowX: "auto"
}), qk = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = pe({
    props: t,
    name: "MuiTableContainer"
  }), {
    className: o,
    component: i = "div"
  } = r, l = L(r, Qk), s = w({}, r, {
    component: i
  }), a = Yk(s);
  return /* @__PURE__ */ y.jsx(Xk, w({
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
}, n_ = Y("thead", {
  name: "MuiTableHead",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})({
  display: "table-header-group"
}), r_ = {
  variant: "head"
}, Df = "thead", o_ = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = pe({
    props: t,
    name: "MuiTableHead"
  }), {
    className: o,
    component: i = Df
  } = r, l = L(r, e_), s = w({}, r, {
    component: i
  }), a = t_(s);
  return /* @__PURE__ */ y.jsx(us.Provider, {
    value: r_,
    children: /* @__PURE__ */ y.jsx(n_, w({
      as: i,
      className: B(a.root, o),
      ref: n,
      role: i === Df ? null : "rowgroup",
      ownerState: s
    }, l))
  });
}), i_ = o_;
function l_(e) {
  return ve("MuiTableRow", e);
}
const s_ = ye("MuiTableRow", ["root", "selected", "hover", "head", "footer"]), Ff = s_, a_ = ["className", "component", "hover", "selected"], u_ = (e) => {
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
}, c_ = Y("tr", {
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
  [`&.${Ff.hover}:hover`]: {
    backgroundColor: (e.vars || e).palette.action.hover
  },
  [`&.${Ff.selected}`]: {
    backgroundColor: e.vars ? `rgba(${e.vars.palette.primary.mainChannel} / ${e.vars.palette.action.selectedOpacity})` : ct(e.palette.primary.main, e.palette.action.selectedOpacity),
    "&:hover": {
      backgroundColor: e.vars ? `rgba(${e.vars.palette.primary.mainChannel} / calc(${e.vars.palette.action.selectedOpacity} + ${e.vars.palette.action.hoverOpacity}))` : ct(e.palette.primary.main, e.palette.action.selectedOpacity + e.palette.action.hoverOpacity)
    }
  }
})), Bf = "tr", d_ = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = pe({
    props: t,
    name: "MuiTableRow"
  }), {
    className: o,
    component: i = Bf,
    hover: l = !1,
    selected: s = !1
  } = r, a = L(r, a_), u = _.useContext(us), c = w({}, r, {
    component: i,
    hover: l,
    selected: s,
    head: u && u.variant === "head",
    footer: u && u.variant === "footer"
  }), d = u_(c);
  return /* @__PURE__ */ y.jsx(c_, w({
    as: i,
    ref: n,
    className: B(d.root, o),
    role: i === Bf ? null : "row",
    ownerState: c
  }, a));
}), Wf = d_, f_ = ({ devices: e, setActiveView: t }) => /* @__PURE__ */ y.jsx(Zk, { component: gc, children: /* @__PURE__ */ y.jsxs(Ok, { sx: { minWidth: 650 }, "aria-label": "simple table", children: [
  /* @__PURE__ */ y.jsx(i_, { children: /* @__PURE__ */ y.jsxs(Wf, { children: [
    /* @__PURE__ */ y.jsx(qt, { children: "Name" }),
    /* @__PURE__ */ y.jsx(qt, { children: "Status" }),
    /* @__PURE__ */ y.jsx(qt, { children: "Model" }),
    /* @__PURE__ */ y.jsx(qt, { children: "MAC Address" })
  ] }) }),
  /* @__PURE__ */ y.jsx(Dk, { children: e.map((n) => /* @__PURE__ */ y.jsxs(
    Wf,
    {
      onClick: () => {
        var o;
        const r = (o = n.model) != null && o.startsWith("MV") ? "camera" : "device";
        t({ view: r, deviceId: n.serial });
      },
      sx: { cursor: "pointer", "&:hover": { backgroundColor: "action.hover" } },
      children: [
        /* @__PURE__ */ y.jsx(qt, { component: "th", scope: "row", children: n.name || n.mac }),
        /* @__PURE__ */ y.jsx(qt, { children: n.status }),
        /* @__PURE__ */ y.jsx(qt, { children: n.model }),
        /* @__PURE__ */ y.jsx(qt, { children: n.mac })
      ]
    },
    n.serial
  )) })
] }) }), p_ = ({ setActiveView: e, data: t }) => {
  if (!t)
    return /* @__PURE__ */ y.jsx(K, { children: "Loading dashboard..." });
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
  return /* @__PURE__ */ y.jsxs(Qe, { container: !0, spacing: 3, children: [
    /* @__PURE__ */ y.jsx(Qe, { item: !0, xs: 12, sm: 6, md: 2.4, children: /* @__PURE__ */ y.jsx(Vr, { title: "Total Devices", value: i.totalDevices, icon: /* @__PURE__ */ y.jsx(Jh, {}) }) }),
    /* @__PURE__ */ y.jsx(Qe, { item: !0, xs: 12, sm: 6, md: 2.4, children: /* @__PURE__ */ y.jsx(Vr, { title: "Wireless APs", value: i.wirelessAps, icon: /* @__PURE__ */ y.jsx(e0, {}) }) }),
    /* @__PURE__ */ y.jsx(Qe, { item: !0, xs: 12, sm: 6, md: 2.4, children: /* @__PURE__ */ y.jsx(Vr, { title: "Switches", value: i.switches, icon: /* @__PURE__ */ y.jsx(t0, {}) }) }),
    /* @__PURE__ */ y.jsx(Qe, { item: !0, xs: 12, sm: 6, md: 2.4, children: /* @__PURE__ */ y.jsx(Vr, { title: "Cameras", value: i.cameras, icon: /* @__PURE__ */ y.jsx(n0, {}) }) }),
    /* @__PURE__ */ y.jsx(Qe, { item: !0, xs: 12, sm: 6, md: 2.4, children: /* @__PURE__ */ y.jsx(Vr, { title: "Virtual SSIDs", value: i.ssids, icon: /* @__PURE__ */ y.jsx(r0, {}) }) }),
    /* @__PURE__ */ y.jsxs(Qe, { item: !0, xs: 12, children: [
      /* @__PURE__ */ y.jsx(K, { variant: "h6", gutterBottom: !0, children: "Networks" }),
      /* @__PURE__ */ y.jsx(Qe, { container: !0, spacing: 2, children: o.map((l) => /* @__PURE__ */ y.jsx(Qe, { item: !0, xs: 12, sm: 6, md: 4, children: /* @__PURE__ */ y.jsx(Sr, { children: /* @__PURE__ */ y.jsx(bf, { onClick: () => e({ view: "network", networkId: l.id }), children: /* @__PURE__ */ y.jsx(wr, { children: /* @__PURE__ */ y.jsx(K, { gutterBottom: !0, variant: "h5", component: "div", children: l.name }) }) }) }) }, l.id)) })
    ] }),
    /* @__PURE__ */ y.jsxs(Qe, { item: !0, xs: 12, children: [
      /* @__PURE__ */ y.jsx(K, { variant: "h6", gutterBottom: !0, children: "Cameras" }),
      /* @__PURE__ */ y.jsx(Qe, { container: !0, spacing: 2, children: n.filter((l) => {
        var s;
        return (s = l.model) == null ? void 0 : s.startsWith("MV");
      }).map((l) => /* @__PURE__ */ y.jsx(Qe, { item: !0, xs: 12, sm: 6, md: 4, children: /* @__PURE__ */ y.jsx(Sr, { children: /* @__PURE__ */ y.jsx(bf, { onClick: () => e({ view: "camera", deviceId: l.serial }), children: /* @__PURE__ */ y.jsx(wr, { children: /* @__PURE__ */ y.jsx(K, { gutterBottom: !0, variant: "h5", component: "div", children: l.name || l.mac }) }) }) }) }, l.serial)) })
    ] }),
    /* @__PURE__ */ y.jsxs(Qe, { item: !0, xs: 12, children: [
      /* @__PURE__ */ y.jsx(K, { variant: "h6", gutterBottom: !0, sx: { mt: 4 }, children: "All Devices" }),
      /* @__PURE__ */ y.jsx(f_, { devices: n, setActiveView: e })
    ] })
  ] });
};
function m_(e) {
  return ve("MuiButton", e);
}
const h_ = ye("MuiButton", ["root", "text", "textInherit", "textPrimary", "textSecondary", "textSuccess", "textError", "textInfo", "textWarning", "outlined", "outlinedInherit", "outlinedPrimary", "outlinedSecondary", "outlinedSuccess", "outlinedError", "outlinedInfo", "outlinedWarning", "contained", "containedInherit", "containedPrimary", "containedSecondary", "containedSuccess", "containedError", "containedInfo", "containedWarning", "disableElevation", "focusVisible", "disabled", "colorInherit", "colorPrimary", "colorSecondary", "colorSuccess", "colorError", "colorInfo", "colorWarning", "textSizeSmall", "textSizeMedium", "textSizeLarge", "outlinedSizeSmall", "outlinedSizeMedium", "outlinedSizeLarge", "containedSizeSmall", "containedSizeMedium", "containedSizeLarge", "sizeMedium", "sizeSmall", "sizeLarge", "fullWidth", "startIcon", "endIcon", "icon", "iconSizeSmall", "iconSizeMedium", "iconSizeLarge"]), fi = h_, g_ = /* @__PURE__ */ _.createContext({}), v_ = g_, y_ = /* @__PURE__ */ _.createContext(void 0), x_ = y_, S_ = ["children", "color", "component", "className", "disabled", "disableElevation", "disableFocusRipple", "endIcon", "focusVisibleClassName", "fullWidth", "size", "startIcon", "type", "variant"], w_ = (e) => {
  const {
    color: t,
    disableElevation: n,
    fullWidth: r,
    size: o,
    variant: i,
    classes: l
  } = e, s = {
    root: ["root", i, `${i}${N(t)}`, `size${N(o)}`, `${i}Size${N(o)}`, `color${N(t)}`, n && "disableElevation", r && "fullWidth"],
    label: ["label"],
    startIcon: ["icon", "startIcon", `iconSize${N(o)}`],
    endIcon: ["icon", "endIcon", `iconSize${N(o)}`]
  }, a = Ce(s, m_, l);
  return w({}, l, a);
}, i0 = (e) => w({}, e.size === "small" && {
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
}), C_ = Y(xc, {
  shouldForwardProp: (e) => Yh(e) || e === "classes",
  name: "MuiButton",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[n.variant], t[`${n.variant}${N(n.color)}`], t[`size${N(n.size)}`], t[`${n.variant}Size${N(n.size)}`], n.color === "inherit" && t.colorInherit, n.disableElevation && t.disableElevation, n.fullWidth && t.fullWidth];
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
      backgroundColor: e.vars ? `rgba(${e.vars.palette.text.primaryChannel} / ${e.vars.palette.action.hoverOpacity})` : ct(e.palette.text.primary, e.palette.action.hoverOpacity),
      // Reset on touch devices, it doesn't add specificity
      "@media (hover: none)": {
        backgroundColor: "transparent"
      }
    }, t.variant === "text" && t.color !== "inherit" && {
      backgroundColor: e.vars ? `rgba(${e.vars.palette[t.color].mainChannel} / ${e.vars.palette.action.hoverOpacity})` : ct(e.palette[t.color].main, e.palette.action.hoverOpacity),
      // Reset on touch devices, it doesn't add specificity
      "@media (hover: none)": {
        backgroundColor: "transparent"
      }
    }, t.variant === "outlined" && t.color !== "inherit" && {
      border: `1px solid ${(e.vars || e).palette[t.color].main}`,
      backgroundColor: e.vars ? `rgba(${e.vars.palette[t.color].mainChannel} / ${e.vars.palette.action.hoverOpacity})` : ct(e.palette[t.color].main, e.palette.action.hoverOpacity),
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
    [`&.${fi.focusVisible}`]: w({}, t.variant === "contained" && {
      boxShadow: (e.vars || e).shadows[6]
    }),
    [`&.${fi.disabled}`]: w({
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
    border: e.vars ? `1px solid rgba(${e.vars.palette[t.color].mainChannel} / 0.5)` : `1px solid ${ct(e.palette[t.color].main, 0.5)}`
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
  [`&.${fi.focusVisible}`]: {
    boxShadow: "none"
  },
  "&:active": {
    boxShadow: "none"
  },
  [`&.${fi.disabled}`]: {
    boxShadow: "none"
  }
}), k_ = Y("span", {
  name: "MuiButton",
  slot: "StartIcon",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.startIcon, t[`iconSize${N(n.size)}`]];
  }
})(({
  ownerState: e
}) => w({
  display: "inherit",
  marginRight: 8,
  marginLeft: -4
}, e.size === "small" && {
  marginLeft: -2
}, i0(e))), __ = Y("span", {
  name: "MuiButton",
  slot: "EndIcon",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.endIcon, t[`iconSize${N(n.size)}`]];
  }
})(({
  ownerState: e
}) => w({
  display: "inherit",
  marginRight: -4,
  marginLeft: 8
}, e.size === "small" && {
  marginRight: -2
}, i0(e))), $_ = /* @__PURE__ */ _.forwardRef(function(t, n) {
  const r = _.useContext(v_), o = _.useContext(x_), i = To(r, t), l = pe({
    props: i,
    name: "MuiButton"
  }), {
    children: s,
    color: a = "primary",
    component: u = "button",
    className: c,
    disabled: d = !1,
    disableElevation: p = !1,
    disableFocusRipple: v = !1,
    endIcon: x,
    focusVisibleClassName: g,
    fullWidth: E = !1,
    size: m = "medium",
    startIcon: f,
    type: h,
    variant: S = "text"
  } = l, $ = L(l, S_), k = w({}, l, {
    color: a,
    component: u,
    disabled: d,
    disableElevation: p,
    disableFocusRipple: v,
    fullWidth: E,
    size: m,
    type: h,
    variant: S
  }), C = w_(k), T = f && /* @__PURE__ */ y.jsx(k_, {
    className: C.startIcon,
    ownerState: k,
    children: f
  }), j = x && /* @__PURE__ */ y.jsx(__, {
    className: C.endIcon,
    ownerState: k,
    children: x
  }), M = o || "";
  return /* @__PURE__ */ y.jsxs(C_, w({
    ownerState: k,
    className: B(r.className, C.root, c, M),
    component: u,
    disabled: d,
    focusRipple: !v,
    focusVisibleClassName: B(C.focusVisible, g),
    ref: n,
    type: h
  }, $, {
    classes: C,
    children: [T, s, j]
  }));
}), ul = $_;
var $c = {}, E_ = yn;
Object.defineProperty($c, "__esModule", {
  value: !0
});
var cs = $c.default = void 0, P_ = E_(Or()), T_ = y;
cs = $c.default = (0, P_.default)(/* @__PURE__ */ (0, T_.jsx)("path", {
  d: "M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20z"
}), "ArrowBack");
const R_ = ({ activeView: e, setActiveView: t, data: n }) => {
  const r = n.devices.find((o) => o.serial === e.deviceId);
  return r ? /* @__PURE__ */ y.jsxs(zn, { children: [
    /* @__PURE__ */ y.jsx(
      ul,
      {
        startIcon: /* @__PURE__ */ y.jsx(cs, {}),
        onClick: () => t({ view: "dashboard" }),
        sx: { mb: 2 },
        children: "Back to Dashboard"
      }
    ),
    /* @__PURE__ */ y.jsx(Sr, { children: /* @__PURE__ */ y.jsxs(wr, { children: [
      /* @__PURE__ */ y.jsx(K, { variant: "h6", gutterBottom: !0, children: "Device Details" }),
      /* @__PURE__ */ y.jsxs(K, { children: [
        "Name: ",
        r.name || r.mac
      ] }),
      /* @__PURE__ */ y.jsxs(K, { children: [
        "Status: ",
        r.status
      ] }),
      /* @__PURE__ */ y.jsxs(K, { children: [
        "Model: ",
        r.model
      ] }),
      /* @__PURE__ */ y.jsxs(K, { children: [
        "MAC Address: ",
        r.mac
      ] }),
      /* @__PURE__ */ y.jsxs(K, { children: [
        "Serial: ",
        r.serial
      ] })
    ] }) })
  ] }) : /* @__PURE__ */ y.jsx(K, { children: "Device not found" });
}, M_ = ({ activeView: e, setActiveView: t, data: n }) => {
  const r = n.networks.find((o) => o.id === e.networkId);
  return r ? /* @__PURE__ */ y.jsxs(zn, { children: [
    /* @__PURE__ */ y.jsx(
      ul,
      {
        startIcon: /* @__PURE__ */ y.jsx(cs, {}),
        onClick: () => t({ view: "dashboard" }),
        sx: { mb: 2 },
        children: "Back to Dashboard"
      }
    ),
    /* @__PURE__ */ y.jsx(Sr, { children: /* @__PURE__ */ y.jsxs(wr, { children: [
      /* @__PURE__ */ y.jsx(K, { variant: "h6", gutterBottom: !0, children: "Network Information" }),
      /* @__PURE__ */ y.jsxs(K, { children: [
        "Name: ",
        r.name
      ] }),
      /* @__PURE__ */ y.jsxs(K, { children: [
        "ID: ",
        r.id
      ] }),
      /* @__PURE__ */ y.jsxs(K, { children: [
        "Product Types: ",
        r.product_types.join(", ")
      ] })
    ] }) })
  ] }) : /* @__PURE__ */ y.jsx(K, { children: "Network not found" });
}, O_ = ({ hass: e, config_entry_id: t, activeView: n, setActiveView: r, data: o }) => {
  const i = o.devices.find((v) => v.serial === n.deviceId), [l, s] = _.useState(null), [a, u] = _.useState(!1), [c, d] = _.useState(null);
  if (!i)
    return /* @__PURE__ */ y.jsx(K, { children: "Camera not found" });
  const p = async () => {
    u(!0), d(null);
    try {
      const v = await e.connection.sendMessagePromise({
        type: "meraki_ha/get_camera_stream_url",
        config_entry_id: t,
        serial: i.serial
      });
      s(v.url);
    } catch (v) {
      console.error("Error fetching camera stream URL:", v), d(`Failed to fetch stream URL: ${v.message || "Unknown error"}`);
    } finally {
      u(!1);
    }
  };
  return /* @__PURE__ */ y.jsxs(zn, { children: [
    /* @__PURE__ */ y.jsx(
      ul,
      {
        startIcon: /* @__PURE__ */ y.jsx(cs, {}),
        onClick: () => r({ view: "dashboard" }),
        sx: { mb: 2 },
        children: "Back to Dashboard"
      }
    ),
    /* @__PURE__ */ y.jsx(Sr, { children: /* @__PURE__ */ y.jsxs(wr, { children: [
      /* @__PURE__ */ y.jsxs(K, { variant: "h6", gutterBottom: !0, children: [
        "Camera: ",
        i.name || i.mac
      ] }),
      /* @__PURE__ */ y.jsx(ul, { variant: "contained", onClick: p, disabled: a, children: "Get RTSP Stream URL" }),
      a && /* @__PURE__ */ y.jsx(Xh, { size: 24, sx: { ml: 2 } }),
      c && /* @__PURE__ */ y.jsx(K, { color: "error", sx: { mt: 2 }, children: c }),
      l && /* @__PURE__ */ y.jsxs(zn, { sx: { mt: 2 }, children: [
        /* @__PURE__ */ y.jsx(K, { children: "RTSP Stream URL:" }),
        /* @__PURE__ */ y.jsx(K, { component: "pre", sx: { wordBreak: "break-all" }, children: l }),
        /* @__PURE__ */ y.jsx(K, { variant: "caption", children: "You can open this URL with a media player that supports RTSP streams, like VLC." })
      ] }),
      !l && l !== null && !a && /* @__PURE__ */ y.jsx(K, { sx: { mt: 2 }, children: "No stream URL available for this camera. It might be an unsupported model (e.g., MV2 series) or offline." })
    ] }) })
  ] });
};
const j_ = mc({
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
        return /* @__PURE__ */ y.jsx(p_, { setActiveView: u, data: n });
      case "device":
        return /* @__PURE__ */ y.jsx(R_, { activeView: a, setActiveView: u, data: n });
      case "network":
        return /* @__PURE__ */ y.jsx(M_, { activeView: a, setActiveView: u, data: n });
      case "camera":
        return /* @__PURE__ */ y.jsx(O_, { hass: e, config_entry_id: t, activeView: a, setActiveView: u, data: n });
      default:
        return /* @__PURE__ */ y.jsx(K, { children: "Unknown view" });
    }
  };
  return /* @__PURE__ */ y.jsxs(G2, { theme: j_, children: [
    /* @__PURE__ */ y.jsx(J2, {}),
    /* @__PURE__ */ y.jsxs(tw, { maxWidth: "lg", sx: { mt: 4, mb: 4 }, children: [
      /* @__PURE__ */ y.jsx(K, { variant: "h4", component: "h1", gutterBottom: !0, children: "Meraki Control" }),
      o && /* @__PURE__ */ y.jsx(zn, { sx: { display: "flex", justifyContent: "center", p: 4 }, children: /* @__PURE__ */ y.jsx(Xh, {}) }),
      l && /* @__PURE__ */ y.jsx(kC, { severity: "error", sx: { mt: 2 }, children: l }),
      !o && !l && c()
    ] })
  ] });
};
class N_ extends HTMLElement {
  constructor() {
    super(...arguments);
    Ho(this, "_root");
    Ho(this, "_hass");
    Ho(this, "_panel");
  }
  connectedCallback() {
    this._root = Xs.createRoot(this), this._render();
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
      /* @__PURE__ */ y.jsx(wn.StrictMode, { children: /* @__PURE__ */ y.jsx(z_, { hass: this._hass, config_entry_id: this._panel.config.config_entry_id }) })
    );
  }
}
customElements.define("meraki-panel", N_);
