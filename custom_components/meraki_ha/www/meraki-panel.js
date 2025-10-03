var r0 = Object.defineProperty;
var o0 = (e, t, n) => t in e ? r0(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var Uo = (e, t, n) => (o0(e, typeof t != "symbol" ? t + "" : t, n), n);
function i0(e, t) {
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
function $d(e) {
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
var Rd = { exports: {} }, sl = {}, Od = { exports: {} }, F = {};
/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var $o = Symbol.for("react.element"), l0 = Symbol.for("react.portal"), s0 = Symbol.for("react.fragment"), a0 = Symbol.for("react.strict_mode"), u0 = Symbol.for("react.profiler"), c0 = Symbol.for("react.provider"), f0 = Symbol.for("react.context"), d0 = Symbol.for("react.forward_ref"), p0 = Symbol.for("react.suspense"), m0 = Symbol.for("react.memo"), h0 = Symbol.for("react.lazy"), wc = Symbol.iterator;
function y0(e) {
  return e === null || typeof e != "object" ? null : (e = wc && e[wc] || e["@@iterator"], typeof e == "function" ? e : null);
}
var Md = { isMounted: function() {
  return !1;
}, enqueueForceUpdate: function() {
}, enqueueReplaceState: function() {
}, enqueueSetState: function() {
} }, Nd = Object.assign, zd = {};
function wr(e, t, n) {
  this.props = e, this.context = t, this.refs = zd, this.updater = n || Md;
}
wr.prototype.isReactComponent = {};
wr.prototype.setState = function(e, t) {
  if (typeof e != "object" && typeof e != "function" && e != null)
    throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
  this.updater.enqueueSetState(this, e, t, "setState");
};
wr.prototype.forceUpdate = function(e) {
  this.updater.enqueueForceUpdate(this, e, "forceUpdate");
};
function Ld() {
}
Ld.prototype = wr.prototype;
function Ka(e, t, n) {
  this.props = e, this.context = t, this.refs = zd, this.updater = n || Md;
}
var Ga = Ka.prototype = new Ld();
Ga.constructor = Ka;
Nd(Ga, wr.prototype);
Ga.isPureReactComponent = !0;
var kc = Array.isArray, Id = Object.prototype.hasOwnProperty, Qa = { current: null }, jd = { key: !0, ref: !0, __self: !0, __source: !0 };
function Ad(e, t, n) {
  var r, o = {}, i = null, l = null;
  if (t != null)
    for (r in t.ref !== void 0 && (l = t.ref), t.key !== void 0 && (i = "" + t.key), t)
      Id.call(t, r) && !jd.hasOwnProperty(r) && (o[r] = t[r]);
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
  return { $$typeof: $o, type: e, key: i, ref: l, props: o, _owner: Qa.current };
}
function g0(e, t) {
  return { $$typeof: $o, type: e.type, key: t, ref: e.ref, props: e.props, _owner: e._owner };
}
function Ya(e) {
  return typeof e == "object" && e !== null && e.$$typeof === $o;
}
function v0(e) {
  var t = { "=": "=0", ":": "=2" };
  return "$" + e.replace(/[=:]/g, function(n) {
    return t[n];
  });
}
var Cc = /\/+/g;
function ls(e, t) {
  return typeof e == "object" && e !== null && e.key != null ? v0("" + e.key) : t.toString(36);
}
function fi(e, t, n, r, o) {
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
          case $o:
          case l0:
            l = !0;
        }
    }
  if (l)
    return l = e, o = o(l), e = r === "" ? "." + ls(l, 0) : r, kc(o) ? (n = "", e != null && (n = e.replace(Cc, "$&/") + "/"), fi(o, t, n, "", function(u) {
      return u;
    })) : o != null && (Ya(o) && (o = g0(o, n + (!o.key || l && l.key === o.key ? "" : ("" + o.key).replace(Cc, "$&/") + "/") + e)), t.push(o)), 1;
  if (l = 0, r = r === "" ? "." : r + ":", kc(e))
    for (var s = 0; s < e.length; s++) {
      i = e[s];
      var a = r + ls(i, s);
      l += fi(i, t, n, a, o);
    }
  else if (a = y0(e), typeof a == "function")
    for (e = a.call(e), s = 0; !(i = e.next()).done; )
      i = i.value, a = r + ls(i, s++), l += fi(i, t, n, a, o);
  else if (i === "object")
    throw t = String(e), Error("Objects are not valid as a React child (found: " + (t === "[object Object]" ? "object with keys {" + Object.keys(e).join(", ") + "}" : t) + "). If you meant to render a collection of children, use an array instead.");
  return l;
}
function Vo(e, t, n) {
  if (e == null)
    return e;
  var r = [], o = 0;
  return fi(e, r, "", "", function(i) {
    return t.call(n, i, o++);
  }), r;
}
function S0(e) {
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
var De = { current: null }, di = { transition: null }, x0 = { ReactCurrentDispatcher: De, ReactCurrentBatchConfig: di, ReactCurrentOwner: Qa };
function Dd() {
  throw Error("act(...) is not supported in production builds of React.");
}
F.Children = { map: Vo, forEach: function(e, t, n) {
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
  if (!Ya(e))
    throw Error("React.Children.only expected to receive a single React element child.");
  return e;
} };
F.Component = wr;
F.Fragment = s0;
F.Profiler = u0;
F.PureComponent = Ka;
F.StrictMode = a0;
F.Suspense = p0;
F.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = x0;
F.act = Dd;
F.cloneElement = function(e, t, n) {
  if (e == null)
    throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + e + ".");
  var r = Nd({}, e.props), o = e.key, i = e.ref, l = e._owner;
  if (t != null) {
    if (t.ref !== void 0 && (i = t.ref, l = Qa.current), t.key !== void 0 && (o = "" + t.key), e.type && e.type.defaultProps)
      var s = e.type.defaultProps;
    for (a in t)
      Id.call(t, a) && !jd.hasOwnProperty(a) && (r[a] = t[a] === void 0 && s !== void 0 ? s[a] : t[a]);
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
  return { $$typeof: $o, type: e.type, key: o, ref: i, props: r, _owner: l };
};
F.createContext = function(e) {
  return e = { $$typeof: f0, _currentValue: e, _currentValue2: e, _threadCount: 0, Provider: null, Consumer: null, _defaultValue: null, _globalName: null }, e.Provider = { $$typeof: c0, _context: e }, e.Consumer = e;
};
F.createElement = Ad;
F.createFactory = function(e) {
  var t = Ad.bind(null, e);
  return t.type = e, t;
};
F.createRef = function() {
  return { current: null };
};
F.forwardRef = function(e) {
  return { $$typeof: d0, render: e };
};
F.isValidElement = Ya;
F.lazy = function(e) {
  return { $$typeof: h0, _payload: { _status: -1, _result: e }, _init: S0 };
};
F.memo = function(e, t) {
  return { $$typeof: m0, type: e, compare: t === void 0 ? null : t };
};
F.startTransition = function(e) {
  var t = di.transition;
  di.transition = {};
  try {
    e();
  } finally {
    di.transition = t;
  }
};
F.unstable_act = Dd;
F.useCallback = function(e, t) {
  return De.current.useCallback(e, t);
};
F.useContext = function(e) {
  return De.current.useContext(e);
};
F.useDebugValue = function() {
};
F.useDeferredValue = function(e) {
  return De.current.useDeferredValue(e);
};
F.useEffect = function(e, t) {
  return De.current.useEffect(e, t);
};
F.useId = function() {
  return De.current.useId();
};
F.useImperativeHandle = function(e, t, n) {
  return De.current.useImperativeHandle(e, t, n);
};
F.useInsertionEffect = function(e, t) {
  return De.current.useInsertionEffect(e, t);
};
F.useLayoutEffect = function(e, t) {
  return De.current.useLayoutEffect(e, t);
};
F.useMemo = function(e, t) {
  return De.current.useMemo(e, t);
};
F.useReducer = function(e, t, n) {
  return De.current.useReducer(e, t, n);
};
F.useRef = function(e) {
  return De.current.useRef(e);
};
F.useState = function(e) {
  return De.current.useState(e);
};
F.useSyncExternalStore = function(e, t, n) {
  return De.current.useSyncExternalStore(e, t, n);
};
F.useTransition = function() {
  return De.current.useTransition();
};
F.version = "18.3.1";
Od.exports = F;
var C = Od.exports;
const wt = /* @__PURE__ */ $d(C), Bs = /* @__PURE__ */ i0({
  __proto__: null,
  default: wt
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
var w0 = C, k0 = Symbol.for("react.element"), C0 = Symbol.for("react.fragment"), E0 = Object.prototype.hasOwnProperty, _0 = w0.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, P0 = { key: !0, ref: !0, __self: !0, __source: !0 };
function Fd(e, t, n) {
  var r, o = {}, i = null, l = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (r in t)
    E0.call(t, r) && !P0.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps)
    for (r in t = e.defaultProps, t)
      o[r] === void 0 && (o[r] = t[r]);
  return { $$typeof: k0, type: e, key: i, ref: l, props: o, _owner: _0.current };
}
sl.Fragment = C0;
sl.jsx = Fd;
sl.jsxs = Fd;
Rd.exports = sl;
var T = Rd.exports, Ws = {}, bd = { exports: {} }, Ze = {}, Bd = { exports: {} }, Wd = {};
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
    var j = R.length;
    R.push(z);
    e:
      for (; 0 < j; ) {
        var q = j - 1 >>> 1, se = R[q];
        if (0 < o(se, z))
          R[q] = z, R[j] = se, j = q;
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
    var z = R[0], j = R.pop();
    if (j !== z) {
      R[0] = j;
      e:
        for (var q = 0, se = R.length, Xt = se >>> 1; q < Xt; ) {
          var _e = 2 * (q + 1) - 1, Pt = R[_e], I = _e + 1, Se = R[I];
          if (0 > o(Pt, j))
            I < se && 0 > o(Se, Pt) ? (R[q] = Se, R[I] = j, q = I) : (R[q] = Pt, R[_e] = j, q = _e);
          else if (I < se && 0 > o(Se, j))
            R[q] = Se, R[I] = j, q = I;
          else
            break e;
        }
    }
    return z;
  }
  function o(R, z) {
    var j = R.sortIndex - z.sortIndex;
    return j !== 0 ? j : R.id - z.id;
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
  var a = [], u = [], d = 1, f = null, m = 3, v = !1, g = !1, y = !1, _ = typeof setTimeout == "function" ? setTimeout : null, p = typeof clearTimeout == "function" ? clearTimeout : null, c = typeof setImmediate < "u" ? setImmediate : null;
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
    if (y = !1, h(R), !g)
      if (n(a) !== null)
        g = !0, ve(E);
      else {
        var z = n(u);
        z !== null && he(S, z.startTime - R);
      }
  }
  function E(R, z) {
    g = !1, y && (y = !1, p($), $ = -1), v = !0;
    var j = m;
    try {
      for (h(z), f = n(a); f !== null && (!(f.expirationTime > z) || R && !b()); ) {
        var q = f.callback;
        if (typeof q == "function") {
          f.callback = null, m = f.priorityLevel;
          var se = q(f.expirationTime <= z);
          z = e.unstable_now(), typeof se == "function" ? f.callback = se : f === n(a) && r(a), h(z);
        } else
          r(a);
        f = n(a);
      }
      if (f !== null)
        var Xt = !0;
      else {
        var _e = n(u);
        _e !== null && he(S, _e.startTime - z), Xt = !1;
      }
      return Xt;
    } finally {
      f = null, m = j, v = !1;
    }
  }
  var w = !1, x = null, $ = -1, N = 5, O = -1;
  function b() {
    return !(e.unstable_now() - O < N);
  }
  function A() {
    if (x !== null) {
      var R = e.unstable_now();
      O = R;
      var z = !0;
      try {
        z = x(!0, R);
      } finally {
        z ? L() : (w = !1, x = null);
      }
    } else
      w = !1;
  }
  var L;
  if (typeof c == "function")
    L = function() {
      c(A);
    };
  else if (typeof MessageChannel < "u") {
    var W = new MessageChannel(), ee = W.port2;
    W.port1.onmessage = A, L = function() {
      ee.postMessage(null);
    };
  } else
    L = function() {
      _(A, 0);
    };
  function ve(R) {
    x = R, w || (w = !0, L());
  }
  function he(R, z) {
    $ = _(function() {
      R(e.unstable_now());
    }, z);
  }
  e.unstable_IdlePriority = 5, e.unstable_ImmediatePriority = 1, e.unstable_LowPriority = 4, e.unstable_NormalPriority = 3, e.unstable_Profiling = null, e.unstable_UserBlockingPriority = 2, e.unstable_cancelCallback = function(R) {
    R.callback = null;
  }, e.unstable_continueExecution = function() {
    g || v || (g = !0, ve(E));
  }, e.unstable_forceFrameRate = function(R) {
    0 > R || 125 < R ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : N = 0 < R ? Math.floor(1e3 / R) : 5;
  }, e.unstable_getCurrentPriorityLevel = function() {
    return m;
  }, e.unstable_getFirstCallbackNode = function() {
    return n(a);
  }, e.unstable_next = function(R) {
    switch (m) {
      case 1:
      case 2:
      case 3:
        var z = 3;
        break;
      default:
        z = m;
    }
    var j = m;
    m = z;
    try {
      return R();
    } finally {
      m = j;
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
    var j = m;
    m = R;
    try {
      return z();
    } finally {
      m = j;
    }
  }, e.unstable_scheduleCallback = function(R, z, j) {
    var q = e.unstable_now();
    switch (typeof j == "object" && j !== null ? (j = j.delay, j = typeof j == "number" && 0 < j ? q + j : q) : j = q, R) {
      case 1:
        var se = -1;
        break;
      case 2:
        se = 250;
        break;
      case 5:
        se = 1073741823;
        break;
      case 4:
        se = 1e4;
        break;
      default:
        se = 5e3;
    }
    return se = j + se, R = { id: d++, callback: z, priorityLevel: R, startTime: j, expirationTime: se, sortIndex: -1 }, j > q ? (R.sortIndex = j, t(u, R), n(a) === null && R === n(u) && (y ? (p($), $ = -1) : y = !0, he(S, j - q))) : (R.sortIndex = se, t(a, R), g || v || (g = !0, ve(E))), R;
  }, e.unstable_shouldYield = b, e.unstable_wrapCallback = function(R) {
    var z = m;
    return function() {
      var j = m;
      m = z;
      try {
        return R.apply(this, arguments);
      } finally {
        m = j;
      }
    };
  };
})(Wd);
Bd.exports = Wd;
var T0 = Bd.exports;
/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var $0 = C, qe = T0;
function P(e) {
  for (var t = "https://reactjs.org/docs/error-decoder.html?invariant=" + e, n = 1; n < arguments.length; n++)
    t += "&args[]=" + encodeURIComponent(arguments[n]);
  return "Minified React error #" + e + "; visit " + t + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
}
var Ud = /* @__PURE__ */ new Set(), ro = {};
function Ln(e, t) {
  fr(e, t), fr(e + "Capture", t);
}
function fr(e, t) {
  for (ro[e] = t, e = 0; e < t.length; e++)
    Ud.add(t[e]);
}
var Wt = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), Us = Object.prototype.hasOwnProperty, R0 = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, Ec = {}, _c = {};
function O0(e) {
  return Us.call(_c, e) ? !0 : Us.call(Ec, e) ? !1 : R0.test(e) ? _c[e] = !0 : (Ec[e] = !0, !1);
}
function M0(e, t, n, r) {
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
function N0(e, t, n, r) {
  if (t === null || typeof t > "u" || M0(e, t, n, r))
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
var Re = {};
"children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(e) {
  Re[e] = new Fe(e, 0, !1, e, null, !1, !1);
});
[["acceptCharset", "accept-charset"], ["className", "class"], ["htmlFor", "for"], ["httpEquiv", "http-equiv"]].forEach(function(e) {
  var t = e[0];
  Re[t] = new Fe(t, 1, !1, e[1], null, !1, !1);
});
["contentEditable", "draggable", "spellCheck", "value"].forEach(function(e) {
  Re[e] = new Fe(e, 2, !1, e.toLowerCase(), null, !1, !1);
});
["autoReverse", "externalResourcesRequired", "focusable", "preserveAlpha"].forEach(function(e) {
  Re[e] = new Fe(e, 2, !1, e, null, !1, !1);
});
"allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(e) {
  Re[e] = new Fe(e, 3, !1, e.toLowerCase(), null, !1, !1);
});
["checked", "multiple", "muted", "selected"].forEach(function(e) {
  Re[e] = new Fe(e, 3, !0, e, null, !1, !1);
});
["capture", "download"].forEach(function(e) {
  Re[e] = new Fe(e, 4, !1, e, null, !1, !1);
});
["cols", "rows", "size", "span"].forEach(function(e) {
  Re[e] = new Fe(e, 6, !1, e, null, !1, !1);
});
["rowSpan", "start"].forEach(function(e) {
  Re[e] = new Fe(e, 5, !1, e.toLowerCase(), null, !1, !1);
});
var Xa = /[\-:]([a-z])/g;
function qa(e) {
  return e[1].toUpperCase();
}
"accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(e) {
  var t = e.replace(
    Xa,
    qa
  );
  Re[t] = new Fe(t, 1, !1, e, null, !1, !1);
});
"xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(e) {
  var t = e.replace(Xa, qa);
  Re[t] = new Fe(t, 1, !1, e, "http://www.w3.org/1999/xlink", !1, !1);
});
["xml:base", "xml:lang", "xml:space"].forEach(function(e) {
  var t = e.replace(Xa, qa);
  Re[t] = new Fe(t, 1, !1, e, "http://www.w3.org/XML/1998/namespace", !1, !1);
});
["tabIndex", "crossOrigin"].forEach(function(e) {
  Re[e] = new Fe(e, 1, !1, e.toLowerCase(), null, !1, !1);
});
Re.xlinkHref = new Fe("xlinkHref", 1, !1, "xlink:href", "http://www.w3.org/1999/xlink", !0, !1);
["src", "href", "action", "formAction"].forEach(function(e) {
  Re[e] = new Fe(e, 1, !1, e.toLowerCase(), null, !0, !0);
});
function Za(e, t, n, r) {
  var o = Re.hasOwnProperty(t) ? Re[t] : null;
  (o !== null ? o.type !== 0 : r || !(2 < t.length) || t[0] !== "o" && t[0] !== "O" || t[1] !== "n" && t[1] !== "N") && (N0(t, n, o, r) && (n = null), r || o === null ? O0(t) && (n === null ? e.removeAttribute(t) : e.setAttribute(t, "" + n)) : o.mustUseProperty ? e[o.propertyName] = n === null ? o.type === 3 ? !1 : "" : n : (t = o.attributeName, r = o.attributeNamespace, n === null ? e.removeAttribute(t) : (o = o.type, n = o === 3 || o === 4 && n === !0 ? "" : "" + n, r ? e.setAttributeNS(r, t, n) : e.setAttribute(t, n))));
}
var Qt = $0.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, Ho = Symbol.for("react.element"), Hn = Symbol.for("react.portal"), Kn = Symbol.for("react.fragment"), Ja = Symbol.for("react.strict_mode"), Vs = Symbol.for("react.profiler"), Vd = Symbol.for("react.provider"), Hd = Symbol.for("react.context"), eu = Symbol.for("react.forward_ref"), Hs = Symbol.for("react.suspense"), Ks = Symbol.for("react.suspense_list"), tu = Symbol.for("react.memo"), Jt = Symbol.for("react.lazy"), Kd = Symbol.for("react.offscreen"), Pc = Symbol.iterator;
function Mr(e) {
  return e === null || typeof e != "object" ? null : (e = Pc && e[Pc] || e["@@iterator"], typeof e == "function" ? e : null);
}
var le = Object.assign, ss;
function Br(e) {
  if (ss === void 0)
    try {
      throw Error();
    } catch (n) {
      var t = n.stack.trim().match(/\n( *(at )?)/);
      ss = t && t[1] || "";
    }
  return `
` + ss + e;
}
var as = !1;
function us(e, t) {
  if (!e || as)
    return "";
  as = !0;
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
    as = !1, Error.prepareStackTrace = n;
  }
  return (e = e ? e.displayName || e.name : "") ? Br(e) : "";
}
function z0(e) {
  switch (e.tag) {
    case 5:
      return Br(e.type);
    case 16:
      return Br("Lazy");
    case 13:
      return Br("Suspense");
    case 19:
      return Br("SuspenseList");
    case 0:
    case 2:
    case 15:
      return e = us(e.type, !1), e;
    case 11:
      return e = us(e.type.render, !1), e;
    case 1:
      return e = us(e.type, !0), e;
    default:
      return "";
  }
}
function Gs(e) {
  if (e == null)
    return null;
  if (typeof e == "function")
    return e.displayName || e.name || null;
  if (typeof e == "string")
    return e;
  switch (e) {
    case Kn:
      return "Fragment";
    case Hn:
      return "Portal";
    case Vs:
      return "Profiler";
    case Ja:
      return "StrictMode";
    case Hs:
      return "Suspense";
    case Ks:
      return "SuspenseList";
  }
  if (typeof e == "object")
    switch (e.$$typeof) {
      case Hd:
        return (e.displayName || "Context") + ".Consumer";
      case Vd:
        return (e._context.displayName || "Context") + ".Provider";
      case eu:
        var t = e.render;
        return e = e.displayName, e || (e = t.displayName || t.name || "", e = e !== "" ? "ForwardRef(" + e + ")" : "ForwardRef"), e;
      case tu:
        return t = e.displayName || null, t !== null ? t : Gs(e.type) || "Memo";
      case Jt:
        t = e._payload, e = e._init;
        try {
          return Gs(e(t));
        } catch {
        }
    }
  return null;
}
function L0(e) {
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
      return Gs(t);
    case 8:
      return t === Ja ? "StrictMode" : "Mode";
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
function mn(e) {
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
function Gd(e) {
  var t = e.type;
  return (e = e.nodeName) && e.toLowerCase() === "input" && (t === "checkbox" || t === "radio");
}
function I0(e) {
  var t = Gd(e) ? "checked" : "value", n = Object.getOwnPropertyDescriptor(e.constructor.prototype, t), r = "" + e[t];
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
  e._valueTracker || (e._valueTracker = I0(e));
}
function Qd(e) {
  if (!e)
    return !1;
  var t = e._valueTracker;
  if (!t)
    return !0;
  var n = t.getValue(), r = "";
  return e && (r = Gd(e) ? e.checked ? "true" : "false" : e.value), e = r, e !== n ? (t.setValue(e), !0) : !1;
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
function Qs(e, t) {
  var n = t.checked;
  return le({}, t, { defaultChecked: void 0, defaultValue: void 0, value: void 0, checked: n ?? e._wrapperState.initialChecked });
}
function Tc(e, t) {
  var n = t.defaultValue == null ? "" : t.defaultValue, r = t.checked != null ? t.checked : t.defaultChecked;
  n = mn(t.value != null ? t.value : n), e._wrapperState = { initialChecked: r, initialValue: n, controlled: t.type === "checkbox" || t.type === "radio" ? t.checked != null : t.value != null };
}
function Yd(e, t) {
  t = t.checked, t != null && Za(e, "checked", t, !1);
}
function Ys(e, t) {
  Yd(e, t);
  var n = mn(t.value), r = t.type;
  if (n != null)
    r === "number" ? (n === 0 && e.value === "" || e.value != n) && (e.value = "" + n) : e.value !== "" + n && (e.value = "" + n);
  else if (r === "submit" || r === "reset") {
    e.removeAttribute("value");
    return;
  }
  t.hasOwnProperty("value") ? Xs(e, t.type, n) : t.hasOwnProperty("defaultValue") && Xs(e, t.type, mn(t.defaultValue)), t.checked == null && t.defaultChecked != null && (e.defaultChecked = !!t.defaultChecked);
}
function $c(e, t, n) {
  if (t.hasOwnProperty("value") || t.hasOwnProperty("defaultValue")) {
    var r = t.type;
    if (!(r !== "submit" && r !== "reset" || t.value !== void 0 && t.value !== null))
      return;
    t = "" + e._wrapperState.initialValue, n || t === e.value || (e.value = t), e.defaultValue = t;
  }
  n = e.name, n !== "" && (e.name = ""), e.defaultChecked = !!e._wrapperState.initialChecked, n !== "" && (e.name = n);
}
function Xs(e, t, n) {
  (t !== "number" || Ri(e.ownerDocument) !== e) && (n == null ? e.defaultValue = "" + e._wrapperState.initialValue : e.defaultValue !== "" + n && (e.defaultValue = "" + n));
}
var Wr = Array.isArray;
function rr(e, t, n, r) {
  if (e = e.options, t) {
    t = {};
    for (var o = 0; o < n.length; o++)
      t["$" + n[o]] = !0;
    for (n = 0; n < e.length; n++)
      o = t.hasOwnProperty("$" + e[n].value), e[n].selected !== o && (e[n].selected = o), o && r && (e[n].defaultSelected = !0);
  } else {
    for (n = "" + mn(n), t = null, o = 0; o < e.length; o++) {
      if (e[o].value === n) {
        e[o].selected = !0, r && (e[o].defaultSelected = !0);
        return;
      }
      t !== null || e[o].disabled || (t = e[o]);
    }
    t !== null && (t.selected = !0);
  }
}
function qs(e, t) {
  if (t.dangerouslySetInnerHTML != null)
    throw Error(P(91));
  return le({}, t, { value: void 0, defaultValue: void 0, children: "" + e._wrapperState.initialValue });
}
function Rc(e, t) {
  var n = t.value;
  if (n == null) {
    if (n = t.children, t = t.defaultValue, n != null) {
      if (t != null)
        throw Error(P(92));
      if (Wr(n)) {
        if (1 < n.length)
          throw Error(P(93));
        n = n[0];
      }
      t = n;
    }
    t == null && (t = ""), n = t;
  }
  e._wrapperState = { initialValue: mn(n) };
}
function Xd(e, t) {
  var n = mn(t.value), r = mn(t.defaultValue);
  n != null && (n = "" + n, n !== e.value && (e.value = n), t.defaultValue == null && e.defaultValue !== n && (e.defaultValue = n)), r != null && (e.defaultValue = "" + r);
}
function Oc(e) {
  var t = e.textContent;
  t === e._wrapperState.initialValue && t !== "" && t !== null && (e.value = t);
}
function qd(e) {
  switch (e) {
    case "svg":
      return "http://www.w3.org/2000/svg";
    case "math":
      return "http://www.w3.org/1998/Math/MathML";
    default:
      return "http://www.w3.org/1999/xhtml";
  }
}
function Zs(e, t) {
  return e == null || e === "http://www.w3.org/1999/xhtml" ? qd(t) : e === "http://www.w3.org/2000/svg" && t === "foreignObject" ? "http://www.w3.org/1999/xhtml" : e;
}
var Go, Zd = function(e) {
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
}, j0 = ["Webkit", "ms", "Moz", "O"];
Object.keys(Gr).forEach(function(e) {
  j0.forEach(function(t) {
    t = t + e.charAt(0).toUpperCase() + e.substring(1), Gr[t] = Gr[e];
  });
});
function Jd(e, t, n) {
  return t == null || typeof t == "boolean" || t === "" ? "" : n || typeof t != "number" || t === 0 || Gr.hasOwnProperty(e) && Gr[e] ? ("" + t).trim() : t + "px";
}
function ep(e, t) {
  e = e.style;
  for (var n in t)
    if (t.hasOwnProperty(n)) {
      var r = n.indexOf("--") === 0, o = Jd(n, t[n], r);
      n === "float" && (n = "cssFloat"), r ? e.setProperty(n, o) : e[n] = o;
    }
}
var A0 = le({ menuitem: !0 }, { area: !0, base: !0, br: !0, col: !0, embed: !0, hr: !0, img: !0, input: !0, keygen: !0, link: !0, meta: !0, param: !0, source: !0, track: !0, wbr: !0 });
function Js(e, t) {
  if (t) {
    if (A0[e] && (t.children != null || t.dangerouslySetInnerHTML != null))
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
function ea(e, t) {
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
var ta = null;
function nu(e) {
  return e = e.target || e.srcElement || window, e.correspondingUseElement && (e = e.correspondingUseElement), e.nodeType === 3 ? e.parentNode : e;
}
var na = null, or = null, ir = null;
function Mc(e) {
  if (e = Mo(e)) {
    if (typeof na != "function")
      throw Error(P(280));
    var t = e.stateNode;
    t && (t = dl(t), na(e.stateNode, e.type, t));
  }
}
function tp(e) {
  or ? ir ? ir.push(e) : ir = [e] : or = e;
}
function np() {
  if (or) {
    var e = or, t = ir;
    if (ir = or = null, Mc(e), t)
      for (e = 0; e < t.length; e++)
        Mc(t[e]);
  }
}
function rp(e, t) {
  return e(t);
}
function op() {
}
var cs = !1;
function ip(e, t, n) {
  if (cs)
    return e(t, n);
  cs = !0;
  try {
    return rp(e, t, n);
  } finally {
    cs = !1, (or !== null || ir !== null) && (op(), np());
  }
}
function io(e, t) {
  var n = e.stateNode;
  if (n === null)
    return null;
  var r = dl(n);
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
var ra = !1;
if (Wt)
  try {
    var Nr = {};
    Object.defineProperty(Nr, "passive", { get: function() {
      ra = !0;
    } }), window.addEventListener("test", Nr, Nr), window.removeEventListener("test", Nr, Nr);
  } catch {
    ra = !1;
  }
function D0(e, t, n, r, o, i, l, s, a) {
  var u = Array.prototype.slice.call(arguments, 3);
  try {
    t.apply(n, u);
  } catch (d) {
    this.onError(d);
  }
}
var Qr = !1, Oi = null, Mi = !1, oa = null, F0 = { onError: function(e) {
  Qr = !0, Oi = e;
} };
function b0(e, t, n, r, o, i, l, s, a) {
  Qr = !1, Oi = null, D0.apply(F0, arguments);
}
function B0(e, t, n, r, o, i, l, s, a) {
  if (b0.apply(this, arguments), Qr) {
    if (Qr) {
      var u = Oi;
      Qr = !1, Oi = null;
    } else
      throw Error(P(198));
    Mi || (Mi = !0, oa = u);
  }
}
function In(e) {
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
function lp(e) {
  if (e.tag === 13) {
    var t = e.memoizedState;
    if (t === null && (e = e.alternate, e !== null && (t = e.memoizedState)), t !== null)
      return t.dehydrated;
  }
  return null;
}
function Nc(e) {
  if (In(e) !== e)
    throw Error(P(188));
}
function W0(e) {
  var t = e.alternate;
  if (!t) {
    if (t = In(e), t === null)
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
          return Nc(o), e;
        if (i === r)
          return Nc(o), t;
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
function sp(e) {
  return e = W0(e), e !== null ? ap(e) : null;
}
function ap(e) {
  if (e.tag === 5 || e.tag === 6)
    return e;
  for (e = e.child; e !== null; ) {
    var t = ap(e);
    if (t !== null)
      return t;
    e = e.sibling;
  }
  return null;
}
var up = qe.unstable_scheduleCallback, zc = qe.unstable_cancelCallback, U0 = qe.unstable_shouldYield, V0 = qe.unstable_requestPaint, fe = qe.unstable_now, H0 = qe.unstable_getCurrentPriorityLevel, ru = qe.unstable_ImmediatePriority, cp = qe.unstable_UserBlockingPriority, Ni = qe.unstable_NormalPriority, K0 = qe.unstable_LowPriority, fp = qe.unstable_IdlePriority, al = null, Nt = null;
function G0(e) {
  if (Nt && typeof Nt.onCommitFiberRoot == "function")
    try {
      Nt.onCommitFiberRoot(al, e, void 0, (e.current.flags & 128) === 128);
    } catch {
    }
}
var kt = Math.clz32 ? Math.clz32 : X0, Q0 = Math.log, Y0 = Math.LN2;
function X0(e) {
  return e >>>= 0, e === 0 ? 32 : 31 - (Q0(e) / Y0 | 0) | 0;
}
var Qo = 64, Yo = 4194304;
function Ur(e) {
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
function zi(e, t) {
  var n = e.pendingLanes;
  if (n === 0)
    return 0;
  var r = 0, o = e.suspendedLanes, i = e.pingedLanes, l = n & 268435455;
  if (l !== 0) {
    var s = l & ~o;
    s !== 0 ? r = Ur(s) : (i &= l, i !== 0 && (r = Ur(i)));
  } else
    l = n & ~o, l !== 0 ? r = Ur(l) : i !== 0 && (r = Ur(i));
  if (r === 0)
    return 0;
  if (t !== 0 && t !== r && !(t & o) && (o = r & -r, i = t & -t, o >= i || o === 16 && (i & 4194240) !== 0))
    return t;
  if (r & 4 && (r |= n & 16), t = e.entangledLanes, t !== 0)
    for (e = e.entanglements, t &= r; 0 < t; )
      n = 31 - kt(t), o = 1 << n, r |= e[n], t &= ~o;
  return r;
}
function q0(e, t) {
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
function Z0(e, t) {
  for (var n = e.suspendedLanes, r = e.pingedLanes, o = e.expirationTimes, i = e.pendingLanes; 0 < i; ) {
    var l = 31 - kt(i), s = 1 << l, a = o[l];
    a === -1 ? (!(s & n) || s & r) && (o[l] = q0(s, t)) : a <= t && (e.expiredLanes |= s), i &= ~s;
  }
}
function ia(e) {
  return e = e.pendingLanes & -1073741825, e !== 0 ? e : e & 1073741824 ? 1073741824 : 0;
}
function dp() {
  var e = Qo;
  return Qo <<= 1, !(Qo & 4194240) && (Qo = 64), e;
}
function fs(e) {
  for (var t = [], n = 0; 31 > n; n++)
    t.push(e);
  return t;
}
function Ro(e, t, n) {
  e.pendingLanes |= t, t !== 536870912 && (e.suspendedLanes = 0, e.pingedLanes = 0), e = e.eventTimes, t = 31 - kt(t), e[t] = n;
}
function J0(e, t) {
  var n = e.pendingLanes & ~t;
  e.pendingLanes = t, e.suspendedLanes = 0, e.pingedLanes = 0, e.expiredLanes &= t, e.mutableReadLanes &= t, e.entangledLanes &= t, t = e.entanglements;
  var r = e.eventTimes;
  for (e = e.expirationTimes; 0 < n; ) {
    var o = 31 - kt(n), i = 1 << o;
    t[o] = 0, r[o] = -1, e[o] = -1, n &= ~i;
  }
}
function ou(e, t) {
  var n = e.entangledLanes |= t;
  for (e = e.entanglements; n; ) {
    var r = 31 - kt(n), o = 1 << r;
    o & t | e[r] & t && (e[r] |= t), n &= ~o;
  }
}
var K = 0;
function pp(e) {
  return e &= -e, 1 < e ? 4 < e ? e & 268435455 ? 16 : 536870912 : 4 : 1;
}
var mp, iu, hp, yp, gp, la = !1, Xo = [], ln = null, sn = null, an = null, lo = /* @__PURE__ */ new Map(), so = /* @__PURE__ */ new Map(), tn = [], ey = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
function Lc(e, t) {
  switch (e) {
    case "focusin":
    case "focusout":
      ln = null;
      break;
    case "dragenter":
    case "dragleave":
      sn = null;
      break;
    case "mouseover":
    case "mouseout":
      an = null;
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
  return e === null || e.nativeEvent !== i ? (e = { blockedOn: t, domEventName: n, eventSystemFlags: r, nativeEvent: i, targetContainers: [o] }, t !== null && (t = Mo(t), t !== null && iu(t)), e) : (e.eventSystemFlags |= r, t = e.targetContainers, o !== null && t.indexOf(o) === -1 && t.push(o), e);
}
function ty(e, t, n, r, o) {
  switch (t) {
    case "focusin":
      return ln = zr(ln, e, t, n, r, o), !0;
    case "dragenter":
      return sn = zr(sn, e, t, n, r, o), !0;
    case "mouseover":
      return an = zr(an, e, t, n, r, o), !0;
    case "pointerover":
      var i = o.pointerId;
      return lo.set(i, zr(lo.get(i) || null, e, t, n, r, o)), !0;
    case "gotpointercapture":
      return i = o.pointerId, so.set(i, zr(so.get(i) || null, e, t, n, r, o)), !0;
  }
  return !1;
}
function vp(e) {
  var t = Cn(e.target);
  if (t !== null) {
    var n = In(t);
    if (n !== null) {
      if (t = n.tag, t === 13) {
        if (t = lp(n), t !== null) {
          e.blockedOn = t, gp(e.priority, function() {
            hp(n);
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
    var n = sa(e.domEventName, e.eventSystemFlags, t[0], e.nativeEvent);
    if (n === null) {
      n = e.nativeEvent;
      var r = new n.constructor(n.type, n);
      ta = r, n.target.dispatchEvent(r), ta = null;
    } else
      return t = Mo(n), t !== null && iu(t), e.blockedOn = n, !1;
    t.shift();
  }
  return !0;
}
function Ic(e, t, n) {
  pi(e) && n.delete(t);
}
function ny() {
  la = !1, ln !== null && pi(ln) && (ln = null), sn !== null && pi(sn) && (sn = null), an !== null && pi(an) && (an = null), lo.forEach(Ic), so.forEach(Ic);
}
function Lr(e, t) {
  e.blockedOn === t && (e.blockedOn = null, la || (la = !0, qe.unstable_scheduleCallback(qe.unstable_NormalPriority, ny)));
}
function ao(e) {
  function t(o) {
    return Lr(o, e);
  }
  if (0 < Xo.length) {
    Lr(Xo[0], e);
    for (var n = 1; n < Xo.length; n++) {
      var r = Xo[n];
      r.blockedOn === e && (r.blockedOn = null);
    }
  }
  for (ln !== null && Lr(ln, e), sn !== null && Lr(sn, e), an !== null && Lr(an, e), lo.forEach(t), so.forEach(t), n = 0; n < tn.length; n++)
    r = tn[n], r.blockedOn === e && (r.blockedOn = null);
  for (; 0 < tn.length && (n = tn[0], n.blockedOn === null); )
    vp(n), n.blockedOn === null && tn.shift();
}
var lr = Qt.ReactCurrentBatchConfig, Li = !0;
function ry(e, t, n, r) {
  var o = K, i = lr.transition;
  lr.transition = null;
  try {
    K = 1, lu(e, t, n, r);
  } finally {
    K = o, lr.transition = i;
  }
}
function oy(e, t, n, r) {
  var o = K, i = lr.transition;
  lr.transition = null;
  try {
    K = 4, lu(e, t, n, r);
  } finally {
    K = o, lr.transition = i;
  }
}
function lu(e, t, n, r) {
  if (Li) {
    var o = sa(e, t, n, r);
    if (o === null)
      ws(e, t, r, Ii, n), Lc(e, r);
    else if (ty(o, e, t, n, r))
      r.stopPropagation();
    else if (Lc(e, r), t & 4 && -1 < ey.indexOf(e)) {
      for (; o !== null; ) {
        var i = Mo(o);
        if (i !== null && mp(i), i = sa(e, t, n, r), i === null && ws(e, t, r, Ii, n), i === o)
          break;
        o = i;
      }
      o !== null && r.stopPropagation();
    } else
      ws(e, t, r, null, n);
  }
}
var Ii = null;
function sa(e, t, n, r) {
  if (Ii = null, e = nu(r), e = Cn(e), e !== null)
    if (t = In(e), t === null)
      e = null;
    else if (n = t.tag, n === 13) {
      if (e = lp(t), e !== null)
        return e;
      e = null;
    } else if (n === 3) {
      if (t.stateNode.current.memoizedState.isDehydrated)
        return t.tag === 3 ? t.stateNode.containerInfo : null;
      e = null;
    } else
      t !== e && (e = null);
  return Ii = e, null;
}
function Sp(e) {
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
      switch (H0()) {
        case ru:
          return 1;
        case cp:
          return 4;
        case Ni:
        case K0:
          return 16;
        case fp:
          return 536870912;
        default:
          return 16;
      }
    default:
      return 16;
  }
}
var rn = null, su = null, mi = null;
function xp() {
  if (mi)
    return mi;
  var e, t = su, n = t.length, r, o = "value" in rn ? rn.value : rn.textContent, i = o.length;
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
function jc() {
  return !1;
}
function Je(e) {
  function t(n, r, o, i, l) {
    this._reactName = n, this._targetInst = o, this.type = r, this.nativeEvent = i, this.target = l, this.currentTarget = null;
    for (var s in e)
      e.hasOwnProperty(s) && (n = e[s], this[s] = n ? n(i) : i[s]);
    return this.isDefaultPrevented = (i.defaultPrevented != null ? i.defaultPrevented : i.returnValue === !1) ? qo : jc, this.isPropagationStopped = jc, this;
  }
  return le(t.prototype, { preventDefault: function() {
    this.defaultPrevented = !0;
    var n = this.nativeEvent;
    n && (n.preventDefault ? n.preventDefault() : typeof n.returnValue != "unknown" && (n.returnValue = !1), this.isDefaultPrevented = qo);
  }, stopPropagation: function() {
    var n = this.nativeEvent;
    n && (n.stopPropagation ? n.stopPropagation() : typeof n.cancelBubble != "unknown" && (n.cancelBubble = !0), this.isPropagationStopped = qo);
  }, persist: function() {
  }, isPersistent: qo }), t;
}
var kr = { eventPhase: 0, bubbles: 0, cancelable: 0, timeStamp: function(e) {
  return e.timeStamp || Date.now();
}, defaultPrevented: 0, isTrusted: 0 }, au = Je(kr), Oo = le({}, kr, { view: 0, detail: 0 }), iy = Je(Oo), ds, ps, Ir, ul = le({}, Oo, { screenX: 0, screenY: 0, clientX: 0, clientY: 0, pageX: 0, pageY: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, getModifierState: uu, button: 0, buttons: 0, relatedTarget: function(e) {
  return e.relatedTarget === void 0 ? e.fromElement === e.srcElement ? e.toElement : e.fromElement : e.relatedTarget;
}, movementX: function(e) {
  return "movementX" in e ? e.movementX : (e !== Ir && (Ir && e.type === "mousemove" ? (ds = e.screenX - Ir.screenX, ps = e.screenY - Ir.screenY) : ps = ds = 0, Ir = e), ds);
}, movementY: function(e) {
  return "movementY" in e ? e.movementY : ps;
} }), Ac = Je(ul), ly = le({}, ul, { dataTransfer: 0 }), sy = Je(ly), ay = le({}, Oo, { relatedTarget: 0 }), ms = Je(ay), uy = le({}, kr, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }), cy = Je(uy), fy = le({}, kr, { clipboardData: function(e) {
  return "clipboardData" in e ? e.clipboardData : window.clipboardData;
} }), dy = Je(fy), py = le({}, kr, { data: 0 }), Dc = Je(py), my = {
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
}, hy = {
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
}, yy = { Alt: "altKey", Control: "ctrlKey", Meta: "metaKey", Shift: "shiftKey" };
function gy(e) {
  var t = this.nativeEvent;
  return t.getModifierState ? t.getModifierState(e) : (e = yy[e]) ? !!t[e] : !1;
}
function uu() {
  return gy;
}
var vy = le({}, Oo, { key: function(e) {
  if (e.key) {
    var t = my[e.key] || e.key;
    if (t !== "Unidentified")
      return t;
  }
  return e.type === "keypress" ? (e = hi(e), e === 13 ? "Enter" : String.fromCharCode(e)) : e.type === "keydown" || e.type === "keyup" ? hy[e.keyCode] || "Unidentified" : "";
}, code: 0, location: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, repeat: 0, locale: 0, getModifierState: uu, charCode: function(e) {
  return e.type === "keypress" ? hi(e) : 0;
}, keyCode: function(e) {
  return e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
}, which: function(e) {
  return e.type === "keypress" ? hi(e) : e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
} }), Sy = Je(vy), xy = le({}, ul, { pointerId: 0, width: 0, height: 0, pressure: 0, tangentialPressure: 0, tiltX: 0, tiltY: 0, twist: 0, pointerType: 0, isPrimary: 0 }), Fc = Je(xy), wy = le({}, Oo, { touches: 0, targetTouches: 0, changedTouches: 0, altKey: 0, metaKey: 0, ctrlKey: 0, shiftKey: 0, getModifierState: uu }), ky = Je(wy), Cy = le({}, kr, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }), Ey = Je(Cy), _y = le({}, ul, {
  deltaX: function(e) {
    return "deltaX" in e ? e.deltaX : "wheelDeltaX" in e ? -e.wheelDeltaX : 0;
  },
  deltaY: function(e) {
    return "deltaY" in e ? e.deltaY : "wheelDeltaY" in e ? -e.wheelDeltaY : "wheelDelta" in e ? -e.wheelDelta : 0;
  },
  deltaZ: 0,
  deltaMode: 0
}), Py = Je(_y), Ty = [9, 13, 27, 32], cu = Wt && "CompositionEvent" in window, Yr = null;
Wt && "documentMode" in document && (Yr = document.documentMode);
var $y = Wt && "TextEvent" in window && !Yr, wp = Wt && (!cu || Yr && 8 < Yr && 11 >= Yr), bc = String.fromCharCode(32), Bc = !1;
function kp(e, t) {
  switch (e) {
    case "keyup":
      return Ty.indexOf(t.keyCode) !== -1;
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
function Cp(e) {
  return e = e.detail, typeof e == "object" && "data" in e ? e.data : null;
}
var Gn = !1;
function Ry(e, t) {
  switch (e) {
    case "compositionend":
      return Cp(t);
    case "keypress":
      return t.which !== 32 ? null : (Bc = !0, bc);
    case "textInput":
      return e = t.data, e === bc && Bc ? null : e;
    default:
      return null;
  }
}
function Oy(e, t) {
  if (Gn)
    return e === "compositionend" || !cu && kp(e, t) ? (e = xp(), mi = su = rn = null, Gn = !1, e) : null;
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
      return wp && t.locale !== "ko" ? null : t.data;
    default:
      return null;
  }
}
var My = { color: !0, date: !0, datetime: !0, "datetime-local": !0, email: !0, month: !0, number: !0, password: !0, range: !0, search: !0, tel: !0, text: !0, time: !0, url: !0, week: !0 };
function Wc(e) {
  var t = e && e.nodeName && e.nodeName.toLowerCase();
  return t === "input" ? !!My[e.type] : t === "textarea";
}
function Ep(e, t, n, r) {
  tp(r), t = ji(t, "onChange"), 0 < t.length && (n = new au("onChange", "change", null, n, r), e.push({ event: n, listeners: t }));
}
var Xr = null, uo = null;
function Ny(e) {
  Ip(e, 0);
}
function cl(e) {
  var t = Xn(e);
  if (Qd(t))
    return e;
}
function zy(e, t) {
  if (e === "change")
    return t;
}
var _p = !1;
if (Wt) {
  var hs;
  if (Wt) {
    var ys = "oninput" in document;
    if (!ys) {
      var Uc = document.createElement("div");
      Uc.setAttribute("oninput", "return;"), ys = typeof Uc.oninput == "function";
    }
    hs = ys;
  } else
    hs = !1;
  _p = hs && (!document.documentMode || 9 < document.documentMode);
}
function Vc() {
  Xr && (Xr.detachEvent("onpropertychange", Pp), uo = Xr = null);
}
function Pp(e) {
  if (e.propertyName === "value" && cl(uo)) {
    var t = [];
    Ep(t, uo, e, nu(e)), ip(Ny, t);
  }
}
function Ly(e, t, n) {
  e === "focusin" ? (Vc(), Xr = t, uo = n, Xr.attachEvent("onpropertychange", Pp)) : e === "focusout" && Vc();
}
function Iy(e) {
  if (e === "selectionchange" || e === "keyup" || e === "keydown")
    return cl(uo);
}
function jy(e, t) {
  if (e === "click")
    return cl(t);
}
function Ay(e, t) {
  if (e === "input" || e === "change")
    return cl(t);
}
function Dy(e, t) {
  return e === t && (e !== 0 || 1 / e === 1 / t) || e !== e && t !== t;
}
var Et = typeof Object.is == "function" ? Object.is : Dy;
function co(e, t) {
  if (Et(e, t))
    return !0;
  if (typeof e != "object" || e === null || typeof t != "object" || t === null)
    return !1;
  var n = Object.keys(e), r = Object.keys(t);
  if (n.length !== r.length)
    return !1;
  for (r = 0; r < n.length; r++) {
    var o = n[r];
    if (!Us.call(t, o) || !Et(e[o], t[o]))
      return !1;
  }
  return !0;
}
function Hc(e) {
  for (; e && e.firstChild; )
    e = e.firstChild;
  return e;
}
function Kc(e, t) {
  var n = Hc(e);
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
    n = Hc(n);
  }
}
function Tp(e, t) {
  return e && t ? e === t ? !0 : e && e.nodeType === 3 ? !1 : t && t.nodeType === 3 ? Tp(e, t.parentNode) : "contains" in e ? e.contains(t) : e.compareDocumentPosition ? !!(e.compareDocumentPosition(t) & 16) : !1 : !1;
}
function $p() {
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
function fu(e) {
  var t = e && e.nodeName && e.nodeName.toLowerCase();
  return t && (t === "input" && (e.type === "text" || e.type === "search" || e.type === "tel" || e.type === "url" || e.type === "password") || t === "textarea" || e.contentEditable === "true");
}
function Fy(e) {
  var t = $p(), n = e.focusedElem, r = e.selectionRange;
  if (t !== n && n && n.ownerDocument && Tp(n.ownerDocument.documentElement, n)) {
    if (r !== null && fu(n)) {
      if (t = r.start, e = r.end, e === void 0 && (e = t), "selectionStart" in n)
        n.selectionStart = t, n.selectionEnd = Math.min(e, n.value.length);
      else if (e = (t = n.ownerDocument || document) && t.defaultView || window, e.getSelection) {
        e = e.getSelection();
        var o = n.textContent.length, i = Math.min(r.start, o);
        r = r.end === void 0 ? i : Math.min(r.end, o), !e.extend && i > r && (o = r, r = i, i = o), o = Kc(n, i);
        var l = Kc(
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
var by = Wt && "documentMode" in document && 11 >= document.documentMode, Qn = null, aa = null, qr = null, ua = !1;
function Gc(e, t, n) {
  var r = n.window === n ? n.document : n.nodeType === 9 ? n : n.ownerDocument;
  ua || Qn == null || Qn !== Ri(r) || (r = Qn, "selectionStart" in r && fu(r) ? r = { start: r.selectionStart, end: r.selectionEnd } : (r = (r.ownerDocument && r.ownerDocument.defaultView || window).getSelection(), r = { anchorNode: r.anchorNode, anchorOffset: r.anchorOffset, focusNode: r.focusNode, focusOffset: r.focusOffset }), qr && co(qr, r) || (qr = r, r = ji(aa, "onSelect"), 0 < r.length && (t = new au("onSelect", "select", null, t, n), e.push({ event: t, listeners: r }), t.target = Qn)));
}
function Zo(e, t) {
  var n = {};
  return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit" + e] = "webkit" + t, n["Moz" + e] = "moz" + t, n;
}
var Yn = { animationend: Zo("Animation", "AnimationEnd"), animationiteration: Zo("Animation", "AnimationIteration"), animationstart: Zo("Animation", "AnimationStart"), transitionend: Zo("Transition", "TransitionEnd") }, gs = {}, Rp = {};
Wt && (Rp = document.createElement("div").style, "AnimationEvent" in window || (delete Yn.animationend.animation, delete Yn.animationiteration.animation, delete Yn.animationstart.animation), "TransitionEvent" in window || delete Yn.transitionend.transition);
function fl(e) {
  if (gs[e])
    return gs[e];
  if (!Yn[e])
    return e;
  var t = Yn[e], n;
  for (n in t)
    if (t.hasOwnProperty(n) && n in Rp)
      return gs[e] = t[n];
  return e;
}
var Op = fl("animationend"), Mp = fl("animationiteration"), Np = fl("animationstart"), zp = fl("transitionend"), Lp = /* @__PURE__ */ new Map(), Qc = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
function yn(e, t) {
  Lp.set(e, t), Ln(t, [e]);
}
for (var vs = 0; vs < Qc.length; vs++) {
  var Ss = Qc[vs], By = Ss.toLowerCase(), Wy = Ss[0].toUpperCase() + Ss.slice(1);
  yn(By, "on" + Wy);
}
yn(Op, "onAnimationEnd");
yn(Mp, "onAnimationIteration");
yn(Np, "onAnimationStart");
yn("dblclick", "onDoubleClick");
yn("focusin", "onFocus");
yn("focusout", "onBlur");
yn(zp, "onTransitionEnd");
fr("onMouseEnter", ["mouseout", "mouseover"]);
fr("onMouseLeave", ["mouseout", "mouseover"]);
fr("onPointerEnter", ["pointerout", "pointerover"]);
fr("onPointerLeave", ["pointerout", "pointerover"]);
Ln("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" "));
Ln("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));
Ln("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]);
Ln("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" "));
Ln("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" "));
Ln("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
var Vr = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), Uy = new Set("cancel close invalid load scroll toggle".split(" ").concat(Vr));
function Yc(e, t, n) {
  var r = e.type || "unknown-event";
  e.currentTarget = n, B0(r, t, void 0, e), e.currentTarget = null;
}
function Ip(e, t) {
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
          Yc(o, s, u), i = a;
        }
      else
        for (l = 0; l < r.length; l++) {
          if (s = r[l], a = s.instance, u = s.currentTarget, s = s.listener, a !== i && o.isPropagationStopped())
            break e;
          Yc(o, s, u), i = a;
        }
    }
  }
  if (Mi)
    throw e = oa, Mi = !1, oa = null, e;
}
function Z(e, t) {
  var n = t[ma];
  n === void 0 && (n = t[ma] = /* @__PURE__ */ new Set());
  var r = e + "__bubble";
  n.has(r) || (jp(t, e, 2, !1), n.add(r));
}
function xs(e, t, n) {
  var r = 0;
  t && (r |= 4), jp(n, e, r, t);
}
var Jo = "_reactListening" + Math.random().toString(36).slice(2);
function fo(e) {
  if (!e[Jo]) {
    e[Jo] = !0, Ud.forEach(function(n) {
      n !== "selectionchange" && (Uy.has(n) || xs(n, !1, e), xs(n, !0, e));
    });
    var t = e.nodeType === 9 ? e : e.ownerDocument;
    t === null || t[Jo] || (t[Jo] = !0, xs("selectionchange", !1, t));
  }
}
function jp(e, t, n, r) {
  switch (Sp(t)) {
    case 1:
      var o = ry;
      break;
    case 4:
      o = oy;
      break;
    default:
      o = lu;
  }
  n = o.bind(null, t, n, e), o = void 0, !ra || t !== "touchstart" && t !== "touchmove" && t !== "wheel" || (o = !0), r ? o !== void 0 ? e.addEventListener(t, n, { capture: !0, passive: o }) : e.addEventListener(t, n, !0) : o !== void 0 ? e.addEventListener(t, n, { passive: o }) : e.addEventListener(t, n, !1);
}
function ws(e, t, n, r, o) {
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
  ip(function() {
    var u = i, d = nu(n), f = [];
    e: {
      var m = Lp.get(e);
      if (m !== void 0) {
        var v = au, g = e;
        switch (e) {
          case "keypress":
            if (hi(n) === 0)
              break e;
          case "keydown":
          case "keyup":
            v = Sy;
            break;
          case "focusin":
            g = "focus", v = ms;
            break;
          case "focusout":
            g = "blur", v = ms;
            break;
          case "beforeblur":
          case "afterblur":
            v = ms;
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
            v = Ac;
            break;
          case "drag":
          case "dragend":
          case "dragenter":
          case "dragexit":
          case "dragleave":
          case "dragover":
          case "dragstart":
          case "drop":
            v = sy;
            break;
          case "touchcancel":
          case "touchend":
          case "touchmove":
          case "touchstart":
            v = ky;
            break;
          case Op:
          case Mp:
          case Np:
            v = cy;
            break;
          case zp:
            v = Ey;
            break;
          case "scroll":
            v = iy;
            break;
          case "wheel":
            v = Py;
            break;
          case "copy":
          case "cut":
          case "paste":
            v = dy;
            break;
          case "gotpointercapture":
          case "lostpointercapture":
          case "pointercancel":
          case "pointerdown":
          case "pointermove":
          case "pointerout":
          case "pointerover":
          case "pointerup":
            v = Fc;
        }
        var y = (t & 4) !== 0, _ = !y && e === "scroll", p = y ? m !== null ? m + "Capture" : null : m;
        y = [];
        for (var c = u, h; c !== null; ) {
          h = c;
          var S = h.stateNode;
          if (h.tag === 5 && S !== null && (h = S, p !== null && (S = io(c, p), S != null && y.push(po(c, S, h)))), _)
            break;
          c = c.return;
        }
        0 < y.length && (m = new v(m, g, null, n, d), f.push({ event: m, listeners: y }));
      }
    }
    if (!(t & 7)) {
      e: {
        if (m = e === "mouseover" || e === "pointerover", v = e === "mouseout" || e === "pointerout", m && n !== ta && (g = n.relatedTarget || n.fromElement) && (Cn(g) || g[Ut]))
          break e;
        if ((v || m) && (m = d.window === d ? d : (m = d.ownerDocument) ? m.defaultView || m.parentWindow : window, v ? (g = n.relatedTarget || n.toElement, v = u, g = g ? Cn(g) : null, g !== null && (_ = In(g), g !== _ || g.tag !== 5 && g.tag !== 6) && (g = null)) : (v = null, g = u), v !== g)) {
          if (y = Ac, S = "onMouseLeave", p = "onMouseEnter", c = "mouse", (e === "pointerout" || e === "pointerover") && (y = Fc, S = "onPointerLeave", p = "onPointerEnter", c = "pointer"), _ = v == null ? m : Xn(v), h = g == null ? m : Xn(g), m = new y(S, c + "leave", v, n, d), m.target = _, m.relatedTarget = h, S = null, Cn(d) === u && (y = new y(p, c + "enter", g, n, d), y.target = h, y.relatedTarget = _, S = y), _ = S, v && g)
            t: {
              for (y = v, p = g, c = 0, h = y; h; h = An(h))
                c++;
              for (h = 0, S = p; S; S = An(S))
                h++;
              for (; 0 < c - h; )
                y = An(y), c--;
              for (; 0 < h - c; )
                p = An(p), h--;
              for (; c--; ) {
                if (y === p || p !== null && y === p.alternate)
                  break t;
                y = An(y), p = An(p);
              }
              y = null;
            }
          else
            y = null;
          v !== null && Xc(f, m, v, y, !1), g !== null && _ !== null && Xc(f, _, g, y, !0);
        }
      }
      e: {
        if (m = u ? Xn(u) : window, v = m.nodeName && m.nodeName.toLowerCase(), v === "select" || v === "input" && m.type === "file")
          var E = zy;
        else if (Wc(m))
          if (_p)
            E = Ay;
          else {
            E = Iy;
            var w = Ly;
          }
        else
          (v = m.nodeName) && v.toLowerCase() === "input" && (m.type === "checkbox" || m.type === "radio") && (E = jy);
        if (E && (E = E(e, u))) {
          Ep(f, E, n, d);
          break e;
        }
        w && w(e, m, u), e === "focusout" && (w = m._wrapperState) && w.controlled && m.type === "number" && Xs(m, "number", m.value);
      }
      switch (w = u ? Xn(u) : window, e) {
        case "focusin":
          (Wc(w) || w.contentEditable === "true") && (Qn = w, aa = u, qr = null);
          break;
        case "focusout":
          qr = aa = Qn = null;
          break;
        case "mousedown":
          ua = !0;
          break;
        case "contextmenu":
        case "mouseup":
        case "dragend":
          ua = !1, Gc(f, n, d);
          break;
        case "selectionchange":
          if (by)
            break;
        case "keydown":
        case "keyup":
          Gc(f, n, d);
      }
      var x;
      if (cu)
        e: {
          switch (e) {
            case "compositionstart":
              var $ = "onCompositionStart";
              break e;
            case "compositionend":
              $ = "onCompositionEnd";
              break e;
            case "compositionupdate":
              $ = "onCompositionUpdate";
              break e;
          }
          $ = void 0;
        }
      else
        Gn ? kp(e, n) && ($ = "onCompositionEnd") : e === "keydown" && n.keyCode === 229 && ($ = "onCompositionStart");
      $ && (wp && n.locale !== "ko" && (Gn || $ !== "onCompositionStart" ? $ === "onCompositionEnd" && Gn && (x = xp()) : (rn = d, su = "value" in rn ? rn.value : rn.textContent, Gn = !0)), w = ji(u, $), 0 < w.length && ($ = new Dc($, e, null, n, d), f.push({ event: $, listeners: w }), x ? $.data = x : (x = Cp(n), x !== null && ($.data = x)))), (x = $y ? Ry(e, n) : Oy(e, n)) && (u = ji(u, "onBeforeInput"), 0 < u.length && (d = new Dc("onBeforeInput", "beforeinput", null, n, d), f.push({ event: d, listeners: u }), d.data = x));
    }
    Ip(f, t);
  });
}
function po(e, t, n) {
  return { instance: e, listener: t, currentTarget: n };
}
function ji(e, t) {
  for (var n = t + "Capture", r = []; e !== null; ) {
    var o = e, i = o.stateNode;
    o.tag === 5 && i !== null && (o = i, i = io(e, n), i != null && r.unshift(po(e, i, o)), i = io(e, t), i != null && r.push(po(e, i, o))), e = e.return;
  }
  return r;
}
function An(e) {
  if (e === null)
    return null;
  do
    e = e.return;
  while (e && e.tag !== 5);
  return e || null;
}
function Xc(e, t, n, r, o) {
  for (var i = t._reactName, l = []; n !== null && n !== r; ) {
    var s = n, a = s.alternate, u = s.stateNode;
    if (a !== null && a === r)
      break;
    s.tag === 5 && u !== null && (s = u, o ? (a = io(n, i), a != null && l.unshift(po(n, a, s))) : o || (a = io(n, i), a != null && l.push(po(n, a, s)))), n = n.return;
  }
  l.length !== 0 && e.push({ event: t, listeners: l });
}
var Vy = /\r\n?/g, Hy = /\u0000|\uFFFD/g;
function qc(e) {
  return (typeof e == "string" ? e : "" + e).replace(Vy, `
`).replace(Hy, "");
}
function ei(e, t, n) {
  if (t = qc(t), qc(e) !== t && n)
    throw Error(P(425));
}
function Ai() {
}
var ca = null, fa = null;
function da(e, t) {
  return e === "textarea" || e === "noscript" || typeof t.children == "string" || typeof t.children == "number" || typeof t.dangerouslySetInnerHTML == "object" && t.dangerouslySetInnerHTML !== null && t.dangerouslySetInnerHTML.__html != null;
}
var pa = typeof setTimeout == "function" ? setTimeout : void 0, Ky = typeof clearTimeout == "function" ? clearTimeout : void 0, Zc = typeof Promise == "function" ? Promise : void 0, Gy = typeof queueMicrotask == "function" ? queueMicrotask : typeof Zc < "u" ? function(e) {
  return Zc.resolve(null).then(e).catch(Qy);
} : pa;
function Qy(e) {
  setTimeout(function() {
    throw e;
  });
}
function ks(e, t) {
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
function un(e) {
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
function Jc(e) {
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
var Cr = Math.random().toString(36).slice(2), Mt = "__reactFiber$" + Cr, mo = "__reactProps$" + Cr, Ut = "__reactContainer$" + Cr, ma = "__reactEvents$" + Cr, Yy = "__reactListeners$" + Cr, Xy = "__reactHandles$" + Cr;
function Cn(e) {
  var t = e[Mt];
  if (t)
    return t;
  for (var n = e.parentNode; n; ) {
    if (t = n[Ut] || n[Mt]) {
      if (n = t.alternate, t.child !== null || n !== null && n.child !== null)
        for (e = Jc(e); e !== null; ) {
          if (n = e[Mt])
            return n;
          e = Jc(e);
        }
      return t;
    }
    e = n, n = e.parentNode;
  }
  return null;
}
function Mo(e) {
  return e = e[Mt] || e[Ut], !e || e.tag !== 5 && e.tag !== 6 && e.tag !== 13 && e.tag !== 3 ? null : e;
}
function Xn(e) {
  if (e.tag === 5 || e.tag === 6)
    return e.stateNode;
  throw Error(P(33));
}
function dl(e) {
  return e[mo] || null;
}
var ha = [], qn = -1;
function gn(e) {
  return { current: e };
}
function J(e) {
  0 > qn || (e.current = ha[qn], ha[qn] = null, qn--);
}
function Y(e, t) {
  qn++, ha[qn] = e.current, e.current = t;
}
var hn = {}, Le = gn(hn), We = gn(!1), Rn = hn;
function dr(e, t) {
  var n = e.type.contextTypes;
  if (!n)
    return hn;
  var r = e.stateNode;
  if (r && r.__reactInternalMemoizedUnmaskedChildContext === t)
    return r.__reactInternalMemoizedMaskedChildContext;
  var o = {}, i;
  for (i in n)
    o[i] = t[i];
  return r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = t, e.__reactInternalMemoizedMaskedChildContext = o), o;
}
function Ue(e) {
  return e = e.childContextTypes, e != null;
}
function Di() {
  J(We), J(Le);
}
function ef(e, t, n) {
  if (Le.current !== hn)
    throw Error(P(168));
  Y(Le, t), Y(We, n);
}
function Ap(e, t, n) {
  var r = e.stateNode;
  if (t = t.childContextTypes, typeof r.getChildContext != "function")
    return n;
  r = r.getChildContext();
  for (var o in r)
    if (!(o in t))
      throw Error(P(108, L0(e) || "Unknown", o));
  return le({}, n, r);
}
function Fi(e) {
  return e = (e = e.stateNode) && e.__reactInternalMemoizedMergedChildContext || hn, Rn = Le.current, Y(Le, e), Y(We, We.current), !0;
}
function tf(e, t, n) {
  var r = e.stateNode;
  if (!r)
    throw Error(P(169));
  n ? (e = Ap(e, t, Rn), r.__reactInternalMemoizedMergedChildContext = e, J(We), J(Le), Y(Le, e)) : J(We), Y(We, n);
}
var At = null, pl = !1, Cs = !1;
function Dp(e) {
  At === null ? At = [e] : At.push(e);
}
function qy(e) {
  pl = !0, Dp(e);
}
function vn() {
  if (!Cs && At !== null) {
    Cs = !0;
    var e = 0, t = K;
    try {
      var n = At;
      for (K = 1; e < n.length; e++) {
        var r = n[e];
        do
          r = r(!0);
        while (r !== null);
      }
      At = null, pl = !1;
    } catch (o) {
      throw At !== null && (At = At.slice(e + 1)), up(ru, vn), o;
    } finally {
      K = t, Cs = !1;
    }
  }
  return null;
}
var Zn = [], Jn = 0, bi = null, Bi = 0, ot = [], it = 0, On = null, Ft = 1, bt = "";
function Sn(e, t) {
  Zn[Jn++] = Bi, Zn[Jn++] = bi, bi = e, Bi = t;
}
function Fp(e, t, n) {
  ot[it++] = Ft, ot[it++] = bt, ot[it++] = On, On = e;
  var r = Ft;
  e = bt;
  var o = 32 - kt(r) - 1;
  r &= ~(1 << o), n += 1;
  var i = 32 - kt(t) + o;
  if (30 < i) {
    var l = o - o % 5;
    i = (r & (1 << l) - 1).toString(32), r >>= l, o -= l, Ft = 1 << 32 - kt(t) + o | n << o | r, bt = i + e;
  } else
    Ft = 1 << i | n << o | r, bt = e;
}
function du(e) {
  e.return !== null && (Sn(e, 1), Fp(e, 1, 0));
}
function pu(e) {
  for (; e === bi; )
    bi = Zn[--Jn], Zn[Jn] = null, Bi = Zn[--Jn], Zn[Jn] = null;
  for (; e === On; )
    On = ot[--it], ot[it] = null, bt = ot[--it], ot[it] = null, Ft = ot[--it], ot[it] = null;
}
var Ye = null, Qe = null, ne = !1, xt = null;
function bp(e, t) {
  var n = st(5, null, null, 0);
  n.elementType = "DELETED", n.stateNode = t, n.return = e, t = e.deletions, t === null ? (e.deletions = [n], e.flags |= 16) : t.push(n);
}
function nf(e, t) {
  switch (e.tag) {
    case 5:
      var n = e.type;
      return t = t.nodeType !== 1 || n.toLowerCase() !== t.nodeName.toLowerCase() ? null : t, t !== null ? (e.stateNode = t, Ye = e, Qe = un(t.firstChild), !0) : !1;
    case 6:
      return t = e.pendingProps === "" || t.nodeType !== 3 ? null : t, t !== null ? (e.stateNode = t, Ye = e, Qe = null, !0) : !1;
    case 13:
      return t = t.nodeType !== 8 ? null : t, t !== null ? (n = On !== null ? { id: Ft, overflow: bt } : null, e.memoizedState = { dehydrated: t, treeContext: n, retryLane: 1073741824 }, n = st(18, null, null, 0), n.stateNode = t, n.return = e, e.child = n, Ye = e, Qe = null, !0) : !1;
    default:
      return !1;
  }
}
function ya(e) {
  return (e.mode & 1) !== 0 && (e.flags & 128) === 0;
}
function ga(e) {
  if (ne) {
    var t = Qe;
    if (t) {
      var n = t;
      if (!nf(e, t)) {
        if (ya(e))
          throw Error(P(418));
        t = un(n.nextSibling);
        var r = Ye;
        t && nf(e, t) ? bp(r, n) : (e.flags = e.flags & -4097 | 2, ne = !1, Ye = e);
      }
    } else {
      if (ya(e))
        throw Error(P(418));
      e.flags = e.flags & -4097 | 2, ne = !1, Ye = e;
    }
  }
}
function rf(e) {
  for (e = e.return; e !== null && e.tag !== 5 && e.tag !== 3 && e.tag !== 13; )
    e = e.return;
  Ye = e;
}
function ti(e) {
  if (e !== Ye)
    return !1;
  if (!ne)
    return rf(e), ne = !0, !1;
  var t;
  if ((t = e.tag !== 3) && !(t = e.tag !== 5) && (t = e.type, t = t !== "head" && t !== "body" && !da(e.type, e.memoizedProps)), t && (t = Qe)) {
    if (ya(e))
      throw Bp(), Error(P(418));
    for (; t; )
      bp(e, t), t = un(t.nextSibling);
  }
  if (rf(e), e.tag === 13) {
    if (e = e.memoizedState, e = e !== null ? e.dehydrated : null, !e)
      throw Error(P(317));
    e: {
      for (e = e.nextSibling, t = 0; e; ) {
        if (e.nodeType === 8) {
          var n = e.data;
          if (n === "/$") {
            if (t === 0) {
              Qe = un(e.nextSibling);
              break e;
            }
            t--;
          } else
            n !== "$" && n !== "$!" && n !== "$?" || t++;
        }
        e = e.nextSibling;
      }
      Qe = null;
    }
  } else
    Qe = Ye ? un(e.stateNode.nextSibling) : null;
  return !0;
}
function Bp() {
  for (var e = Qe; e; )
    e = un(e.nextSibling);
}
function pr() {
  Qe = Ye = null, ne = !1;
}
function mu(e) {
  xt === null ? xt = [e] : xt.push(e);
}
var Zy = Qt.ReactCurrentBatchConfig;
function jr(e, t, n) {
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
function of(e) {
  var t = e._init;
  return t(e._payload);
}
function Wp(e) {
  function t(p, c) {
    if (e) {
      var h = p.deletions;
      h === null ? (p.deletions = [c], p.flags |= 16) : h.push(c);
    }
  }
  function n(p, c) {
    if (!e)
      return null;
    for (; c !== null; )
      t(p, c), c = c.sibling;
    return null;
  }
  function r(p, c) {
    for (p = /* @__PURE__ */ new Map(); c !== null; )
      c.key !== null ? p.set(c.key, c) : p.set(c.index, c), c = c.sibling;
    return p;
  }
  function o(p, c) {
    return p = pn(p, c), p.index = 0, p.sibling = null, p;
  }
  function i(p, c, h) {
    return p.index = h, e ? (h = p.alternate, h !== null ? (h = h.index, h < c ? (p.flags |= 2, c) : h) : (p.flags |= 2, c)) : (p.flags |= 1048576, c);
  }
  function l(p) {
    return e && p.alternate === null && (p.flags |= 2), p;
  }
  function s(p, c, h, S) {
    return c === null || c.tag !== 6 ? (c = Os(h, p.mode, S), c.return = p, c) : (c = o(c, h), c.return = p, c);
  }
  function a(p, c, h, S) {
    var E = h.type;
    return E === Kn ? d(p, c, h.props.children, S, h.key) : c !== null && (c.elementType === E || typeof E == "object" && E !== null && E.$$typeof === Jt && of(E) === c.type) ? (S = o(c, h.props), S.ref = jr(p, c, h), S.return = p, S) : (S = ki(h.type, h.key, h.props, null, p.mode, S), S.ref = jr(p, c, h), S.return = p, S);
  }
  function u(p, c, h, S) {
    return c === null || c.tag !== 4 || c.stateNode.containerInfo !== h.containerInfo || c.stateNode.implementation !== h.implementation ? (c = Ms(h, p.mode, S), c.return = p, c) : (c = o(c, h.children || []), c.return = p, c);
  }
  function d(p, c, h, S, E) {
    return c === null || c.tag !== 7 ? (c = $n(h, p.mode, S, E), c.return = p, c) : (c = o(c, h), c.return = p, c);
  }
  function f(p, c, h) {
    if (typeof c == "string" && c !== "" || typeof c == "number")
      return c = Os("" + c, p.mode, h), c.return = p, c;
    if (typeof c == "object" && c !== null) {
      switch (c.$$typeof) {
        case Ho:
          return h = ki(c.type, c.key, c.props, null, p.mode, h), h.ref = jr(p, null, c), h.return = p, h;
        case Hn:
          return c = Ms(c, p.mode, h), c.return = p, c;
        case Jt:
          var S = c._init;
          return f(p, S(c._payload), h);
      }
      if (Wr(c) || Mr(c))
        return c = $n(c, p.mode, h, null), c.return = p, c;
      ni(p, c);
    }
    return null;
  }
  function m(p, c, h, S) {
    var E = c !== null ? c.key : null;
    if (typeof h == "string" && h !== "" || typeof h == "number")
      return E !== null ? null : s(p, c, "" + h, S);
    if (typeof h == "object" && h !== null) {
      switch (h.$$typeof) {
        case Ho:
          return h.key === E ? a(p, c, h, S) : null;
        case Hn:
          return h.key === E ? u(p, c, h, S) : null;
        case Jt:
          return E = h._init, m(
            p,
            c,
            E(h._payload),
            S
          );
      }
      if (Wr(h) || Mr(h))
        return E !== null ? null : d(p, c, h, S, null);
      ni(p, h);
    }
    return null;
  }
  function v(p, c, h, S, E) {
    if (typeof S == "string" && S !== "" || typeof S == "number")
      return p = p.get(h) || null, s(c, p, "" + S, E);
    if (typeof S == "object" && S !== null) {
      switch (S.$$typeof) {
        case Ho:
          return p = p.get(S.key === null ? h : S.key) || null, a(c, p, S, E);
        case Hn:
          return p = p.get(S.key === null ? h : S.key) || null, u(c, p, S, E);
        case Jt:
          var w = S._init;
          return v(p, c, h, w(S._payload), E);
      }
      if (Wr(S) || Mr(S))
        return p = p.get(h) || null, d(c, p, S, E, null);
      ni(c, S);
    }
    return null;
  }
  function g(p, c, h, S) {
    for (var E = null, w = null, x = c, $ = c = 0, N = null; x !== null && $ < h.length; $++) {
      x.index > $ ? (N = x, x = null) : N = x.sibling;
      var O = m(p, x, h[$], S);
      if (O === null) {
        x === null && (x = N);
        break;
      }
      e && x && O.alternate === null && t(p, x), c = i(O, c, $), w === null ? E = O : w.sibling = O, w = O, x = N;
    }
    if ($ === h.length)
      return n(p, x), ne && Sn(p, $), E;
    if (x === null) {
      for (; $ < h.length; $++)
        x = f(p, h[$], S), x !== null && (c = i(x, c, $), w === null ? E = x : w.sibling = x, w = x);
      return ne && Sn(p, $), E;
    }
    for (x = r(p, x); $ < h.length; $++)
      N = v(x, p, $, h[$], S), N !== null && (e && N.alternate !== null && x.delete(N.key === null ? $ : N.key), c = i(N, c, $), w === null ? E = N : w.sibling = N, w = N);
    return e && x.forEach(function(b) {
      return t(p, b);
    }), ne && Sn(p, $), E;
  }
  function y(p, c, h, S) {
    var E = Mr(h);
    if (typeof E != "function")
      throw Error(P(150));
    if (h = E.call(h), h == null)
      throw Error(P(151));
    for (var w = E = null, x = c, $ = c = 0, N = null, O = h.next(); x !== null && !O.done; $++, O = h.next()) {
      x.index > $ ? (N = x, x = null) : N = x.sibling;
      var b = m(p, x, O.value, S);
      if (b === null) {
        x === null && (x = N);
        break;
      }
      e && x && b.alternate === null && t(p, x), c = i(b, c, $), w === null ? E = b : w.sibling = b, w = b, x = N;
    }
    if (O.done)
      return n(
        p,
        x
      ), ne && Sn(p, $), E;
    if (x === null) {
      for (; !O.done; $++, O = h.next())
        O = f(p, O.value, S), O !== null && (c = i(O, c, $), w === null ? E = O : w.sibling = O, w = O);
      return ne && Sn(p, $), E;
    }
    for (x = r(p, x); !O.done; $++, O = h.next())
      O = v(x, p, $, O.value, S), O !== null && (e && O.alternate !== null && x.delete(O.key === null ? $ : O.key), c = i(O, c, $), w === null ? E = O : w.sibling = O, w = O);
    return e && x.forEach(function(A) {
      return t(p, A);
    }), ne && Sn(p, $), E;
  }
  function _(p, c, h, S) {
    if (typeof h == "object" && h !== null && h.type === Kn && h.key === null && (h = h.props.children), typeof h == "object" && h !== null) {
      switch (h.$$typeof) {
        case Ho:
          e: {
            for (var E = h.key, w = c; w !== null; ) {
              if (w.key === E) {
                if (E = h.type, E === Kn) {
                  if (w.tag === 7) {
                    n(p, w.sibling), c = o(w, h.props.children), c.return = p, p = c;
                    break e;
                  }
                } else if (w.elementType === E || typeof E == "object" && E !== null && E.$$typeof === Jt && of(E) === w.type) {
                  n(p, w.sibling), c = o(w, h.props), c.ref = jr(p, w, h), c.return = p, p = c;
                  break e;
                }
                n(p, w);
                break;
              } else
                t(p, w);
              w = w.sibling;
            }
            h.type === Kn ? (c = $n(h.props.children, p.mode, S, h.key), c.return = p, p = c) : (S = ki(h.type, h.key, h.props, null, p.mode, S), S.ref = jr(p, c, h), S.return = p, p = S);
          }
          return l(p);
        case Hn:
          e: {
            for (w = h.key; c !== null; ) {
              if (c.key === w)
                if (c.tag === 4 && c.stateNode.containerInfo === h.containerInfo && c.stateNode.implementation === h.implementation) {
                  n(p, c.sibling), c = o(c, h.children || []), c.return = p, p = c;
                  break e;
                } else {
                  n(p, c);
                  break;
                }
              else
                t(p, c);
              c = c.sibling;
            }
            c = Ms(h, p.mode, S), c.return = p, p = c;
          }
          return l(p);
        case Jt:
          return w = h._init, _(p, c, w(h._payload), S);
      }
      if (Wr(h))
        return g(p, c, h, S);
      if (Mr(h))
        return y(p, c, h, S);
      ni(p, h);
    }
    return typeof h == "string" && h !== "" || typeof h == "number" ? (h = "" + h, c !== null && c.tag === 6 ? (n(p, c.sibling), c = o(c, h), c.return = p, p = c) : (n(p, c), c = Os(h, p.mode, S), c.return = p, p = c), l(p)) : n(p, c);
  }
  return _;
}
var mr = Wp(!0), Up = Wp(!1), Wi = gn(null), Ui = null, er = null, hu = null;
function yu() {
  hu = er = Ui = null;
}
function gu(e) {
  var t = Wi.current;
  J(Wi), e._currentValue = t;
}
function va(e, t, n) {
  for (; e !== null; ) {
    var r = e.alternate;
    if ((e.childLanes & t) !== t ? (e.childLanes |= t, r !== null && (r.childLanes |= t)) : r !== null && (r.childLanes & t) !== t && (r.childLanes |= t), e === n)
      break;
    e = e.return;
  }
}
function sr(e, t) {
  Ui = e, hu = er = null, e = e.dependencies, e !== null && e.firstContext !== null && (e.lanes & t && (Be = !0), e.firstContext = null);
}
function ut(e) {
  var t = e._currentValue;
  if (hu !== e)
    if (e = { context: e, memoizedValue: t, next: null }, er === null) {
      if (Ui === null)
        throw Error(P(308));
      er = e, Ui.dependencies = { lanes: 0, firstContext: e };
    } else
      er = er.next = e;
  return t;
}
var En = null;
function vu(e) {
  En === null ? En = [e] : En.push(e);
}
function Vp(e, t, n, r) {
  var o = t.interleaved;
  return o === null ? (n.next = n, vu(t)) : (n.next = o.next, o.next = n), t.interleaved = n, Vt(e, r);
}
function Vt(e, t) {
  e.lanes |= t;
  var n = e.alternate;
  for (n !== null && (n.lanes |= t), n = e, e = e.return; e !== null; )
    e.childLanes |= t, n = e.alternate, n !== null && (n.childLanes |= t), n = e, e = e.return;
  return n.tag === 3 ? n.stateNode : null;
}
var en = !1;
function Su(e) {
  e.updateQueue = { baseState: e.memoizedState, firstBaseUpdate: null, lastBaseUpdate: null, shared: { pending: null, interleaved: null, lanes: 0 }, effects: null };
}
function Hp(e, t) {
  e = e.updateQueue, t.updateQueue === e && (t.updateQueue = { baseState: e.baseState, firstBaseUpdate: e.firstBaseUpdate, lastBaseUpdate: e.lastBaseUpdate, shared: e.shared, effects: e.effects });
}
function Bt(e, t) {
  return { eventTime: e, lane: t, tag: 0, payload: null, callback: null, next: null };
}
function cn(e, t, n) {
  var r = e.updateQueue;
  if (r === null)
    return null;
  if (r = r.shared, B & 2) {
    var o = r.pending;
    return o === null ? t.next = t : (t.next = o.next, o.next = t), r.pending = t, Vt(e, n);
  }
  return o = r.interleaved, o === null ? (t.next = t, vu(r)) : (t.next = o.next, o.next = t), r.interleaved = t, Vt(e, n);
}
function yi(e, t, n) {
  if (t = t.updateQueue, t !== null && (t = t.shared, (n & 4194240) !== 0)) {
    var r = t.lanes;
    r &= e.pendingLanes, n |= r, t.lanes = n, ou(e, n);
  }
}
function lf(e, t) {
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
  en = !1;
  var i = o.firstBaseUpdate, l = o.lastBaseUpdate, s = o.shared.pending;
  if (s !== null) {
    o.shared.pending = null;
    var a = s, u = a.next;
    a.next = null, l === null ? i = u : l.next = u, l = a;
    var d = e.alternate;
    d !== null && (d = d.updateQueue, s = d.lastBaseUpdate, s !== l && (s === null ? d.firstBaseUpdate = u : s.next = u, d.lastBaseUpdate = a));
  }
  if (i !== null) {
    var f = o.baseState;
    l = 0, d = u = a = null, s = i;
    do {
      var m = s.lane, v = s.eventTime;
      if ((r & m) === m) {
        d !== null && (d = d.next = {
          eventTime: v,
          lane: 0,
          tag: s.tag,
          payload: s.payload,
          callback: s.callback,
          next: null
        });
        e: {
          var g = e, y = s;
          switch (m = t, v = n, y.tag) {
            case 1:
              if (g = y.payload, typeof g == "function") {
                f = g.call(v, f, m);
                break e;
              }
              f = g;
              break e;
            case 3:
              g.flags = g.flags & -65537 | 128;
            case 0:
              if (g = y.payload, m = typeof g == "function" ? g.call(v, f, m) : g, m == null)
                break e;
              f = le({}, f, m);
              break e;
            case 2:
              en = !0;
          }
        }
        s.callback !== null && s.lane !== 0 && (e.flags |= 64, m = o.effects, m === null ? o.effects = [s] : m.push(s));
      } else
        v = { eventTime: v, lane: m, tag: s.tag, payload: s.payload, callback: s.callback, next: null }, d === null ? (u = d = v, a = f) : d = d.next = v, l |= m;
      if (s = s.next, s === null) {
        if (s = o.shared.pending, s === null)
          break;
        m = s, s = m.next, m.next = null, o.lastBaseUpdate = m, o.shared.pending = null;
      }
    } while (1);
    if (d === null && (a = f), o.baseState = a, o.firstBaseUpdate = u, o.lastBaseUpdate = d, t = o.shared.interleaved, t !== null) {
      o = t;
      do
        l |= o.lane, o = o.next;
      while (o !== t);
    } else
      i === null && (o.shared.lanes = 0);
    Nn |= l, e.lanes = l, e.memoizedState = f;
  }
}
function sf(e, t, n) {
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
var No = {}, zt = gn(No), ho = gn(No), yo = gn(No);
function _n(e) {
  if (e === No)
    throw Error(P(174));
  return e;
}
function xu(e, t) {
  switch (Y(yo, t), Y(ho, e), Y(zt, No), e = t.nodeType, e) {
    case 9:
    case 11:
      t = (t = t.documentElement) ? t.namespaceURI : Zs(null, "");
      break;
    default:
      e = e === 8 ? t.parentNode : t, t = e.namespaceURI || null, e = e.tagName, t = Zs(t, e);
  }
  J(zt), Y(zt, t);
}
function hr() {
  J(zt), J(ho), J(yo);
}
function Kp(e) {
  _n(yo.current);
  var t = _n(zt.current), n = Zs(t, e.type);
  t !== n && (Y(ho, e), Y(zt, n));
}
function wu(e) {
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
var Es = [];
function ku() {
  for (var e = 0; e < Es.length; e++)
    Es[e]._workInProgressVersionPrimary = null;
  Es.length = 0;
}
var gi = Qt.ReactCurrentDispatcher, _s = Qt.ReactCurrentBatchConfig, Mn = 0, ie = null, xe = null, ke = null, Ki = !1, Zr = !1, go = 0, Jy = 0;
function Oe() {
  throw Error(P(321));
}
function Cu(e, t) {
  if (t === null)
    return !1;
  for (var n = 0; n < t.length && n < e.length; n++)
    if (!Et(e[n], t[n]))
      return !1;
  return !0;
}
function Eu(e, t, n, r, o, i) {
  if (Mn = i, ie = t, t.memoizedState = null, t.updateQueue = null, t.lanes = 0, gi.current = e === null || e.memoizedState === null ? rg : og, e = n(r, o), Zr) {
    i = 0;
    do {
      if (Zr = !1, go = 0, 25 <= i)
        throw Error(P(301));
      i += 1, ke = xe = null, t.updateQueue = null, gi.current = ig, e = n(r, o);
    } while (Zr);
  }
  if (gi.current = Gi, t = xe !== null && xe.next !== null, Mn = 0, ke = xe = ie = null, Ki = !1, t)
    throw Error(P(300));
  return e;
}
function _u() {
  var e = go !== 0;
  return go = 0, e;
}
function $t() {
  var e = { memoizedState: null, baseState: null, baseQueue: null, queue: null, next: null };
  return ke === null ? ie.memoizedState = ke = e : ke = ke.next = e, ke;
}
function ct() {
  if (xe === null) {
    var e = ie.alternate;
    e = e !== null ? e.memoizedState : null;
  } else
    e = xe.next;
  var t = ke === null ? ie.memoizedState : ke.next;
  if (t !== null)
    ke = t, xe = e;
  else {
    if (e === null)
      throw Error(P(310));
    xe = e, e = { memoizedState: xe.memoizedState, baseState: xe.baseState, baseQueue: xe.baseQueue, queue: xe.queue, next: null }, ke === null ? ie.memoizedState = ke = e : ke = ke.next = e;
  }
  return ke;
}
function vo(e, t) {
  return typeof t == "function" ? t(e) : t;
}
function Ps(e) {
  var t = ct(), n = t.queue;
  if (n === null)
    throw Error(P(311));
  n.lastRenderedReducer = e;
  var r = xe, o = r.baseQueue, i = n.pending;
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
      var d = u.lane;
      if ((Mn & d) === d)
        a !== null && (a = a.next = { lane: 0, action: u.action, hasEagerState: u.hasEagerState, eagerState: u.eagerState, next: null }), r = u.hasEagerState ? u.eagerState : e(r, u.action);
      else {
        var f = {
          lane: d,
          action: u.action,
          hasEagerState: u.hasEagerState,
          eagerState: u.eagerState,
          next: null
        };
        a === null ? (s = a = f, l = r) : a = a.next = f, ie.lanes |= d, Nn |= d;
      }
      u = u.next;
    } while (u !== null && u !== i);
    a === null ? l = r : a.next = s, Et(r, t.memoizedState) || (Be = !0), t.memoizedState = r, t.baseState = l, t.baseQueue = a, n.lastRenderedState = r;
  }
  if (e = n.interleaved, e !== null) {
    o = e;
    do
      i = o.lane, ie.lanes |= i, Nn |= i, o = o.next;
    while (o !== e);
  } else
    o === null && (n.lanes = 0);
  return [t.memoizedState, n.dispatch];
}
function Ts(e) {
  var t = ct(), n = t.queue;
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
    Et(i, t.memoizedState) || (Be = !0), t.memoizedState = i, t.baseQueue === null && (t.baseState = i), n.lastRenderedState = i;
  }
  return [i, r];
}
function Gp() {
}
function Qp(e, t) {
  var n = ie, r = ct(), o = t(), i = !Et(r.memoizedState, o);
  if (i && (r.memoizedState = o, Be = !0), r = r.queue, Pu(qp.bind(null, n, r, e), [e]), r.getSnapshot !== t || i || ke !== null && ke.memoizedState.tag & 1) {
    if (n.flags |= 2048, So(9, Xp.bind(null, n, r, o, t), void 0, null), Ce === null)
      throw Error(P(349));
    Mn & 30 || Yp(n, t, o);
  }
  return o;
}
function Yp(e, t, n) {
  e.flags |= 16384, e = { getSnapshot: t, value: n }, t = ie.updateQueue, t === null ? (t = { lastEffect: null, stores: null }, ie.updateQueue = t, t.stores = [e]) : (n = t.stores, n === null ? t.stores = [e] : n.push(e));
}
function Xp(e, t, n, r) {
  t.value = n, t.getSnapshot = r, Zp(t) && Jp(e);
}
function qp(e, t, n) {
  return n(function() {
    Zp(t) && Jp(e);
  });
}
function Zp(e) {
  var t = e.getSnapshot;
  e = e.value;
  try {
    var n = t();
    return !Et(e, n);
  } catch {
    return !0;
  }
}
function Jp(e) {
  var t = Vt(e, 1);
  t !== null && Ct(t, e, 1, -1);
}
function af(e) {
  var t = $t();
  return typeof e == "function" && (e = e()), t.memoizedState = t.baseState = e, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: vo, lastRenderedState: e }, t.queue = e, e = e.dispatch = ng.bind(null, ie, e), [t.memoizedState, e];
}
function So(e, t, n, r) {
  return e = { tag: e, create: t, destroy: n, deps: r, next: null }, t = ie.updateQueue, t === null ? (t = { lastEffect: null, stores: null }, ie.updateQueue = t, t.lastEffect = e.next = e) : (n = t.lastEffect, n === null ? t.lastEffect = e.next = e : (r = n.next, n.next = e, e.next = r, t.lastEffect = e)), e;
}
function em() {
  return ct().memoizedState;
}
function vi(e, t, n, r) {
  var o = $t();
  ie.flags |= e, o.memoizedState = So(1 | t, n, void 0, r === void 0 ? null : r);
}
function ml(e, t, n, r) {
  var o = ct();
  r = r === void 0 ? null : r;
  var i = void 0;
  if (xe !== null) {
    var l = xe.memoizedState;
    if (i = l.destroy, r !== null && Cu(r, l.deps)) {
      o.memoizedState = So(t, n, i, r);
      return;
    }
  }
  ie.flags |= e, o.memoizedState = So(1 | t, n, i, r);
}
function uf(e, t) {
  return vi(8390656, 8, e, t);
}
function Pu(e, t) {
  return ml(2048, 8, e, t);
}
function tm(e, t) {
  return ml(4, 2, e, t);
}
function nm(e, t) {
  return ml(4, 4, e, t);
}
function rm(e, t) {
  if (typeof t == "function")
    return e = e(), t(e), function() {
      t(null);
    };
  if (t != null)
    return e = e(), t.current = e, function() {
      t.current = null;
    };
}
function om(e, t, n) {
  return n = n != null ? n.concat([e]) : null, ml(4, 4, rm.bind(null, t, e), n);
}
function Tu() {
}
function im(e, t) {
  var n = ct();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && Cu(t, r[1]) ? r[0] : (n.memoizedState = [e, t], e);
}
function lm(e, t) {
  var n = ct();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && Cu(t, r[1]) ? r[0] : (e = e(), n.memoizedState = [e, t], e);
}
function sm(e, t, n) {
  return Mn & 21 ? (Et(n, t) || (n = dp(), ie.lanes |= n, Nn |= n, e.baseState = !0), t) : (e.baseState && (e.baseState = !1, Be = !0), e.memoizedState = n);
}
function eg(e, t) {
  var n = K;
  K = n !== 0 && 4 > n ? n : 4, e(!0);
  var r = _s.transition;
  _s.transition = {};
  try {
    e(!1), t();
  } finally {
    K = n, _s.transition = r;
  }
}
function am() {
  return ct().memoizedState;
}
function tg(e, t, n) {
  var r = dn(e);
  if (n = { lane: r, action: n, hasEagerState: !1, eagerState: null, next: null }, um(e))
    cm(t, n);
  else if (n = Vp(e, t, n, r), n !== null) {
    var o = Ae();
    Ct(n, e, r, o), fm(n, t, r);
  }
}
function ng(e, t, n) {
  var r = dn(e), o = { lane: r, action: n, hasEagerState: !1, eagerState: null, next: null };
  if (um(e))
    cm(t, o);
  else {
    var i = e.alternate;
    if (e.lanes === 0 && (i === null || i.lanes === 0) && (i = t.lastRenderedReducer, i !== null))
      try {
        var l = t.lastRenderedState, s = i(l, n);
        if (o.hasEagerState = !0, o.eagerState = s, Et(s, l)) {
          var a = t.interleaved;
          a === null ? (o.next = o, vu(t)) : (o.next = a.next, a.next = o), t.interleaved = o;
          return;
        }
      } catch {
      } finally {
      }
    n = Vp(e, t, o, r), n !== null && (o = Ae(), Ct(n, e, r, o), fm(n, t, r));
  }
}
function um(e) {
  var t = e.alternate;
  return e === ie || t !== null && t === ie;
}
function cm(e, t) {
  Zr = Ki = !0;
  var n = e.pending;
  n === null ? t.next = t : (t.next = n.next, n.next = t), e.pending = t;
}
function fm(e, t, n) {
  if (n & 4194240) {
    var r = t.lanes;
    r &= e.pendingLanes, n |= r, t.lanes = n, ou(e, n);
  }
}
var Gi = { readContext: ut, useCallback: Oe, useContext: Oe, useEffect: Oe, useImperativeHandle: Oe, useInsertionEffect: Oe, useLayoutEffect: Oe, useMemo: Oe, useReducer: Oe, useRef: Oe, useState: Oe, useDebugValue: Oe, useDeferredValue: Oe, useTransition: Oe, useMutableSource: Oe, useSyncExternalStore: Oe, useId: Oe, unstable_isNewReconciler: !1 }, rg = { readContext: ut, useCallback: function(e, t) {
  return $t().memoizedState = [e, t === void 0 ? null : t], e;
}, useContext: ut, useEffect: uf, useImperativeHandle: function(e, t, n) {
  return n = n != null ? n.concat([e]) : null, vi(
    4194308,
    4,
    rm.bind(null, t, e),
    n
  );
}, useLayoutEffect: function(e, t) {
  return vi(4194308, 4, e, t);
}, useInsertionEffect: function(e, t) {
  return vi(4, 2, e, t);
}, useMemo: function(e, t) {
  var n = $t();
  return t = t === void 0 ? null : t, e = e(), n.memoizedState = [e, t], e;
}, useReducer: function(e, t, n) {
  var r = $t();
  return t = n !== void 0 ? n(t) : t, r.memoizedState = r.baseState = t, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: e, lastRenderedState: t }, r.queue = e, e = e.dispatch = tg.bind(null, ie, e), [r.memoizedState, e];
}, useRef: function(e) {
  var t = $t();
  return e = { current: e }, t.memoizedState = e;
}, useState: af, useDebugValue: Tu, useDeferredValue: function(e) {
  return $t().memoizedState = e;
}, useTransition: function() {
  var e = af(!1), t = e[0];
  return e = eg.bind(null, e[1]), $t().memoizedState = e, [t, e];
}, useMutableSource: function() {
}, useSyncExternalStore: function(e, t, n) {
  var r = ie, o = $t();
  if (ne) {
    if (n === void 0)
      throw Error(P(407));
    n = n();
  } else {
    if (n = t(), Ce === null)
      throw Error(P(349));
    Mn & 30 || Yp(r, t, n);
  }
  o.memoizedState = n;
  var i = { value: n, getSnapshot: t };
  return o.queue = i, uf(qp.bind(
    null,
    r,
    i,
    e
  ), [e]), r.flags |= 2048, So(9, Xp.bind(null, r, i, n, t), void 0, null), n;
}, useId: function() {
  var e = $t(), t = Ce.identifierPrefix;
  if (ne) {
    var n = bt, r = Ft;
    n = (r & ~(1 << 32 - kt(r) - 1)).toString(32) + n, t = ":" + t + "R" + n, n = go++, 0 < n && (t += "H" + n.toString(32)), t += ":";
  } else
    n = Jy++, t = ":" + t + "r" + n.toString(32) + ":";
  return e.memoizedState = t;
}, unstable_isNewReconciler: !1 }, og = {
  readContext: ut,
  useCallback: im,
  useContext: ut,
  useEffect: Pu,
  useImperativeHandle: om,
  useInsertionEffect: tm,
  useLayoutEffect: nm,
  useMemo: lm,
  useReducer: Ps,
  useRef: em,
  useState: function() {
    return Ps(vo);
  },
  useDebugValue: Tu,
  useDeferredValue: function(e) {
    var t = ct();
    return sm(t, xe.memoizedState, e);
  },
  useTransition: function() {
    var e = Ps(vo)[0], t = ct().memoizedState;
    return [e, t];
  },
  useMutableSource: Gp,
  useSyncExternalStore: Qp,
  useId: am,
  unstable_isNewReconciler: !1
}, ig = { readContext: ut, useCallback: im, useContext: ut, useEffect: Pu, useImperativeHandle: om, useInsertionEffect: tm, useLayoutEffect: nm, useMemo: lm, useReducer: Ts, useRef: em, useState: function() {
  return Ts(vo);
}, useDebugValue: Tu, useDeferredValue: function(e) {
  var t = ct();
  return xe === null ? t.memoizedState = e : sm(t, xe.memoizedState, e);
}, useTransition: function() {
  var e = Ts(vo)[0], t = ct().memoizedState;
  return [e, t];
}, useMutableSource: Gp, useSyncExternalStore: Qp, useId: am, unstable_isNewReconciler: !1 };
function vt(e, t) {
  if (e && e.defaultProps) {
    t = le({}, t), e = e.defaultProps;
    for (var n in e)
      t[n] === void 0 && (t[n] = e[n]);
    return t;
  }
  return t;
}
function Sa(e, t, n, r) {
  t = e.memoizedState, n = n(r, t), n = n == null ? t : le({}, t, n), e.memoizedState = n, e.lanes === 0 && (e.updateQueue.baseState = n);
}
var hl = { isMounted: function(e) {
  return (e = e._reactInternals) ? In(e) === e : !1;
}, enqueueSetState: function(e, t, n) {
  e = e._reactInternals;
  var r = Ae(), o = dn(e), i = Bt(r, o);
  i.payload = t, n != null && (i.callback = n), t = cn(e, i, o), t !== null && (Ct(t, e, o, r), yi(t, e, o));
}, enqueueReplaceState: function(e, t, n) {
  e = e._reactInternals;
  var r = Ae(), o = dn(e), i = Bt(r, o);
  i.tag = 1, i.payload = t, n != null && (i.callback = n), t = cn(e, i, o), t !== null && (Ct(t, e, o, r), yi(t, e, o));
}, enqueueForceUpdate: function(e, t) {
  e = e._reactInternals;
  var n = Ae(), r = dn(e), o = Bt(n, r);
  o.tag = 2, t != null && (o.callback = t), t = cn(e, o, r), t !== null && (Ct(t, e, r, n), yi(t, e, r));
} };
function cf(e, t, n, r, o, i, l) {
  return e = e.stateNode, typeof e.shouldComponentUpdate == "function" ? e.shouldComponentUpdate(r, i, l) : t.prototype && t.prototype.isPureReactComponent ? !co(n, r) || !co(o, i) : !0;
}
function dm(e, t, n) {
  var r = !1, o = hn, i = t.contextType;
  return typeof i == "object" && i !== null ? i = ut(i) : (o = Ue(t) ? Rn : Le.current, r = t.contextTypes, i = (r = r != null) ? dr(e, o) : hn), t = new t(n, i), e.memoizedState = t.state !== null && t.state !== void 0 ? t.state : null, t.updater = hl, e.stateNode = t, t._reactInternals = e, r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = o, e.__reactInternalMemoizedMaskedChildContext = i), t;
}
function ff(e, t, n, r) {
  e = t.state, typeof t.componentWillReceiveProps == "function" && t.componentWillReceiveProps(n, r), typeof t.UNSAFE_componentWillReceiveProps == "function" && t.UNSAFE_componentWillReceiveProps(n, r), t.state !== e && hl.enqueueReplaceState(t, t.state, null);
}
function xa(e, t, n, r) {
  var o = e.stateNode;
  o.props = n, o.state = e.memoizedState, o.refs = {}, Su(e);
  var i = t.contextType;
  typeof i == "object" && i !== null ? o.context = ut(i) : (i = Ue(t) ? Rn : Le.current, o.context = dr(e, i)), o.state = e.memoizedState, i = t.getDerivedStateFromProps, typeof i == "function" && (Sa(e, t, i, n), o.state = e.memoizedState), typeof t.getDerivedStateFromProps == "function" || typeof o.getSnapshotBeforeUpdate == "function" || typeof o.UNSAFE_componentWillMount != "function" && typeof o.componentWillMount != "function" || (t = o.state, typeof o.componentWillMount == "function" && o.componentWillMount(), typeof o.UNSAFE_componentWillMount == "function" && o.UNSAFE_componentWillMount(), t !== o.state && hl.enqueueReplaceState(o, o.state, null), Vi(e, n, o, r), o.state = e.memoizedState), typeof o.componentDidMount == "function" && (e.flags |= 4194308);
}
function yr(e, t) {
  try {
    var n = "", r = t;
    do
      n += z0(r), r = r.return;
    while (r);
    var o = n;
  } catch (i) {
    o = `
Error generating stack: ` + i.message + `
` + i.stack;
  }
  return { value: e, source: t, stack: o, digest: null };
}
function $s(e, t, n) {
  return { value: e, source: null, stack: n ?? null, digest: t ?? null };
}
function wa(e, t) {
  try {
    console.error(t.value);
  } catch (n) {
    setTimeout(function() {
      throw n;
    });
  }
}
var lg = typeof WeakMap == "function" ? WeakMap : Map;
function pm(e, t, n) {
  n = Bt(-1, n), n.tag = 3, n.payload = { element: null };
  var r = t.value;
  return n.callback = function() {
    Yi || (Yi = !0, Ma = r), wa(e, t);
  }, n;
}
function mm(e, t, n) {
  n = Bt(-1, n), n.tag = 3;
  var r = e.type.getDerivedStateFromError;
  if (typeof r == "function") {
    var o = t.value;
    n.payload = function() {
      return r(o);
    }, n.callback = function() {
      wa(e, t);
    };
  }
  var i = e.stateNode;
  return i !== null && typeof i.componentDidCatch == "function" && (n.callback = function() {
    wa(e, t), typeof r != "function" && (fn === null ? fn = /* @__PURE__ */ new Set([this]) : fn.add(this));
    var l = t.stack;
    this.componentDidCatch(t.value, { componentStack: l !== null ? l : "" });
  }), n;
}
function df(e, t, n) {
  var r = e.pingCache;
  if (r === null) {
    r = e.pingCache = new lg();
    var o = /* @__PURE__ */ new Set();
    r.set(t, o);
  } else
    o = r.get(t), o === void 0 && (o = /* @__PURE__ */ new Set(), r.set(t, o));
  o.has(n) || (o.add(n), e = xg.bind(null, e, t, n), t.then(e, e));
}
function pf(e) {
  do {
    var t;
    if ((t = e.tag === 13) && (t = e.memoizedState, t = t !== null ? t.dehydrated !== null : !0), t)
      return e;
    e = e.return;
  } while (e !== null);
  return null;
}
function mf(e, t, n, r, o) {
  return e.mode & 1 ? (e.flags |= 65536, e.lanes = o, e) : (e === t ? e.flags |= 65536 : (e.flags |= 128, n.flags |= 131072, n.flags &= -52805, n.tag === 1 && (n.alternate === null ? n.tag = 17 : (t = Bt(-1, 1), t.tag = 2, cn(n, t, 1))), n.lanes |= 1), e);
}
var sg = Qt.ReactCurrentOwner, Be = !1;
function je(e, t, n, r) {
  t.child = e === null ? Up(t, null, n, r) : mr(t, e.child, n, r);
}
function hf(e, t, n, r, o) {
  n = n.render;
  var i = t.ref;
  return sr(t, o), r = Eu(e, t, n, r, i, o), n = _u(), e !== null && !Be ? (t.updateQueue = e.updateQueue, t.flags &= -2053, e.lanes &= ~o, Ht(e, t, o)) : (ne && n && du(t), t.flags |= 1, je(e, t, r, o), t.child);
}
function yf(e, t, n, r, o) {
  if (e === null) {
    var i = n.type;
    return typeof i == "function" && !Iu(i) && i.defaultProps === void 0 && n.compare === null && n.defaultProps === void 0 ? (t.tag = 15, t.type = i, hm(e, t, i, r, o)) : (e = ki(n.type, null, r, t, t.mode, o), e.ref = t.ref, e.return = t, t.child = e);
  }
  if (i = e.child, !(e.lanes & o)) {
    var l = i.memoizedProps;
    if (n = n.compare, n = n !== null ? n : co, n(l, r) && e.ref === t.ref)
      return Ht(e, t, o);
  }
  return t.flags |= 1, e = pn(i, r), e.ref = t.ref, e.return = t, t.child = e;
}
function hm(e, t, n, r, o) {
  if (e !== null) {
    var i = e.memoizedProps;
    if (co(i, r) && e.ref === t.ref)
      if (Be = !1, t.pendingProps = r = i, (e.lanes & o) !== 0)
        e.flags & 131072 && (Be = !0);
      else
        return t.lanes = e.lanes, Ht(e, t, o);
  }
  return ka(e, t, n, r, o);
}
function ym(e, t, n) {
  var r = t.pendingProps, o = r.children, i = e !== null ? e.memoizedState : null;
  if (r.mode === "hidden")
    if (!(t.mode & 1))
      t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, Y(nr, Ke), Ke |= n;
    else {
      if (!(n & 1073741824))
        return e = i !== null ? i.baseLanes | n : n, t.lanes = t.childLanes = 1073741824, t.memoizedState = { baseLanes: e, cachePool: null, transitions: null }, t.updateQueue = null, Y(nr, Ke), Ke |= e, null;
      t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, r = i !== null ? i.baseLanes : n, Y(nr, Ke), Ke |= r;
    }
  else
    i !== null ? (r = i.baseLanes | n, t.memoizedState = null) : r = n, Y(nr, Ke), Ke |= r;
  return je(e, t, o, n), t.child;
}
function gm(e, t) {
  var n = t.ref;
  (e === null && n !== null || e !== null && e.ref !== n) && (t.flags |= 512, t.flags |= 2097152);
}
function ka(e, t, n, r, o) {
  var i = Ue(n) ? Rn : Le.current;
  return i = dr(t, i), sr(t, o), n = Eu(e, t, n, r, i, o), r = _u(), e !== null && !Be ? (t.updateQueue = e.updateQueue, t.flags &= -2053, e.lanes &= ~o, Ht(e, t, o)) : (ne && r && du(t), t.flags |= 1, je(e, t, n, o), t.child);
}
function gf(e, t, n, r, o) {
  if (Ue(n)) {
    var i = !0;
    Fi(t);
  } else
    i = !1;
  if (sr(t, o), t.stateNode === null)
    Si(e, t), dm(t, n, r), xa(t, n, r, o), r = !0;
  else if (e === null) {
    var l = t.stateNode, s = t.memoizedProps;
    l.props = s;
    var a = l.context, u = n.contextType;
    typeof u == "object" && u !== null ? u = ut(u) : (u = Ue(n) ? Rn : Le.current, u = dr(t, u));
    var d = n.getDerivedStateFromProps, f = typeof d == "function" || typeof l.getSnapshotBeforeUpdate == "function";
    f || typeof l.UNSAFE_componentWillReceiveProps != "function" && typeof l.componentWillReceiveProps != "function" || (s !== r || a !== u) && ff(t, l, r, u), en = !1;
    var m = t.memoizedState;
    l.state = m, Vi(t, r, l, o), a = t.memoizedState, s !== r || m !== a || We.current || en ? (typeof d == "function" && (Sa(t, n, d, r), a = t.memoizedState), (s = en || cf(t, n, s, r, m, a, u)) ? (f || typeof l.UNSAFE_componentWillMount != "function" && typeof l.componentWillMount != "function" || (typeof l.componentWillMount == "function" && l.componentWillMount(), typeof l.UNSAFE_componentWillMount == "function" && l.UNSAFE_componentWillMount()), typeof l.componentDidMount == "function" && (t.flags |= 4194308)) : (typeof l.componentDidMount == "function" && (t.flags |= 4194308), t.memoizedProps = r, t.memoizedState = a), l.props = r, l.state = a, l.context = u, r = s) : (typeof l.componentDidMount == "function" && (t.flags |= 4194308), r = !1);
  } else {
    l = t.stateNode, Hp(e, t), s = t.memoizedProps, u = t.type === t.elementType ? s : vt(t.type, s), l.props = u, f = t.pendingProps, m = l.context, a = n.contextType, typeof a == "object" && a !== null ? a = ut(a) : (a = Ue(n) ? Rn : Le.current, a = dr(t, a));
    var v = n.getDerivedStateFromProps;
    (d = typeof v == "function" || typeof l.getSnapshotBeforeUpdate == "function") || typeof l.UNSAFE_componentWillReceiveProps != "function" && typeof l.componentWillReceiveProps != "function" || (s !== f || m !== a) && ff(t, l, r, a), en = !1, m = t.memoizedState, l.state = m, Vi(t, r, l, o);
    var g = t.memoizedState;
    s !== f || m !== g || We.current || en ? (typeof v == "function" && (Sa(t, n, v, r), g = t.memoizedState), (u = en || cf(t, n, u, r, m, g, a) || !1) ? (d || typeof l.UNSAFE_componentWillUpdate != "function" && typeof l.componentWillUpdate != "function" || (typeof l.componentWillUpdate == "function" && l.componentWillUpdate(r, g, a), typeof l.UNSAFE_componentWillUpdate == "function" && l.UNSAFE_componentWillUpdate(r, g, a)), typeof l.componentDidUpdate == "function" && (t.flags |= 4), typeof l.getSnapshotBeforeUpdate == "function" && (t.flags |= 1024)) : (typeof l.componentDidUpdate != "function" || s === e.memoizedProps && m === e.memoizedState || (t.flags |= 4), typeof l.getSnapshotBeforeUpdate != "function" || s === e.memoizedProps && m === e.memoizedState || (t.flags |= 1024), t.memoizedProps = r, t.memoizedState = g), l.props = r, l.state = g, l.context = a, r = u) : (typeof l.componentDidUpdate != "function" || s === e.memoizedProps && m === e.memoizedState || (t.flags |= 4), typeof l.getSnapshotBeforeUpdate != "function" || s === e.memoizedProps && m === e.memoizedState || (t.flags |= 1024), r = !1);
  }
  return Ca(e, t, n, r, i, o);
}
function Ca(e, t, n, r, o, i) {
  gm(e, t);
  var l = (t.flags & 128) !== 0;
  if (!r && !l)
    return o && tf(t, n, !1), Ht(e, t, i);
  r = t.stateNode, sg.current = t;
  var s = l && typeof n.getDerivedStateFromError != "function" ? null : r.render();
  return t.flags |= 1, e !== null && l ? (t.child = mr(t, e.child, null, i), t.child = mr(t, null, s, i)) : je(e, t, s, i), t.memoizedState = r.state, o && tf(t, n, !0), t.child;
}
function vm(e) {
  var t = e.stateNode;
  t.pendingContext ? ef(e, t.pendingContext, t.pendingContext !== t.context) : t.context && ef(e, t.context, !1), xu(e, t.containerInfo);
}
function vf(e, t, n, r, o) {
  return pr(), mu(o), t.flags |= 256, je(e, t, n, r), t.child;
}
var Ea = { dehydrated: null, treeContext: null, retryLane: 0 };
function _a(e) {
  return { baseLanes: e, cachePool: null, transitions: null };
}
function Sm(e, t, n) {
  var r = t.pendingProps, o = re.current, i = !1, l = (t.flags & 128) !== 0, s;
  if ((s = l) || (s = e !== null && e.memoizedState === null ? !1 : (o & 2) !== 0), s ? (i = !0, t.flags &= -129) : (e === null || e.memoizedState !== null) && (o |= 1), Y(re, o & 1), e === null)
    return ga(t), e = t.memoizedState, e !== null && (e = e.dehydrated, e !== null) ? (t.mode & 1 ? e.data === "$!" ? t.lanes = 8 : t.lanes = 1073741824 : t.lanes = 1, null) : (l = r.children, e = r.fallback, i ? (r = t.mode, i = t.child, l = { mode: "hidden", children: l }, !(r & 1) && i !== null ? (i.childLanes = 0, i.pendingProps = l) : i = vl(l, r, 0, null), e = $n(e, r, n, null), i.return = t, e.return = t, i.sibling = e, t.child = i, t.child.memoizedState = _a(n), t.memoizedState = Ea, e) : $u(t, l));
  if (o = e.memoizedState, o !== null && (s = o.dehydrated, s !== null))
    return ag(e, t, l, r, s, o, n);
  if (i) {
    i = r.fallback, l = t.mode, o = e.child, s = o.sibling;
    var a = { mode: "hidden", children: r.children };
    return !(l & 1) && t.child !== o ? (r = t.child, r.childLanes = 0, r.pendingProps = a, t.deletions = null) : (r = pn(o, a), r.subtreeFlags = o.subtreeFlags & 14680064), s !== null ? i = pn(s, i) : (i = $n(i, l, n, null), i.flags |= 2), i.return = t, r.return = t, r.sibling = i, t.child = r, r = i, i = t.child, l = e.child.memoizedState, l = l === null ? _a(n) : { baseLanes: l.baseLanes | n, cachePool: null, transitions: l.transitions }, i.memoizedState = l, i.childLanes = e.childLanes & ~n, t.memoizedState = Ea, r;
  }
  return i = e.child, e = i.sibling, r = pn(i, { mode: "visible", children: r.children }), !(t.mode & 1) && (r.lanes = n), r.return = t, r.sibling = null, e !== null && (n = t.deletions, n === null ? (t.deletions = [e], t.flags |= 16) : n.push(e)), t.child = r, t.memoizedState = null, r;
}
function $u(e, t) {
  return t = vl({ mode: "visible", children: t }, e.mode, 0, null), t.return = e, e.child = t;
}
function ri(e, t, n, r) {
  return r !== null && mu(r), mr(t, e.child, null, n), e = $u(t, t.pendingProps.children), e.flags |= 2, t.memoizedState = null, e;
}
function ag(e, t, n, r, o, i, l) {
  if (n)
    return t.flags & 256 ? (t.flags &= -257, r = $s(Error(P(422))), ri(e, t, l, r)) : t.memoizedState !== null ? (t.child = e.child, t.flags |= 128, null) : (i = r.fallback, o = t.mode, r = vl({ mode: "visible", children: r.children }, o, 0, null), i = $n(i, o, l, null), i.flags |= 2, r.return = t, i.return = t, r.sibling = i, t.child = r, t.mode & 1 && mr(t, e.child, null, l), t.child.memoizedState = _a(l), t.memoizedState = Ea, i);
  if (!(t.mode & 1))
    return ri(e, t, l, null);
  if (o.data === "$!") {
    if (r = o.nextSibling && o.nextSibling.dataset, r)
      var s = r.dgst;
    return r = s, i = Error(P(419)), r = $s(i, r, void 0), ri(e, t, l, r);
  }
  if (s = (l & e.childLanes) !== 0, Be || s) {
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
      o = o & (r.suspendedLanes | l) ? 0 : o, o !== 0 && o !== i.retryLane && (i.retryLane = o, Vt(e, o), Ct(r, e, o, -1));
    }
    return Lu(), r = $s(Error(P(421))), ri(e, t, l, r);
  }
  return o.data === "$?" ? (t.flags |= 128, t.child = e.child, t = wg.bind(null, e), o._reactRetry = t, null) : (e = i.treeContext, Qe = un(o.nextSibling), Ye = t, ne = !0, xt = null, e !== null && (ot[it++] = Ft, ot[it++] = bt, ot[it++] = On, Ft = e.id, bt = e.overflow, On = t), t = $u(t, r.children), t.flags |= 4096, t);
}
function Sf(e, t, n) {
  e.lanes |= t;
  var r = e.alternate;
  r !== null && (r.lanes |= t), va(e.return, t, n);
}
function Rs(e, t, n, r, o) {
  var i = e.memoizedState;
  i === null ? e.memoizedState = { isBackwards: t, rendering: null, renderingStartTime: 0, last: r, tail: n, tailMode: o } : (i.isBackwards = t, i.rendering = null, i.renderingStartTime = 0, i.last = r, i.tail = n, i.tailMode = o);
}
function xm(e, t, n) {
  var r = t.pendingProps, o = r.revealOrder, i = r.tail;
  if (je(e, t, r.children, n), r = re.current, r & 2)
    r = r & 1 | 2, t.flags |= 128;
  else {
    if (e !== null && e.flags & 128)
      e:
        for (e = t.child; e !== null; ) {
          if (e.tag === 13)
            e.memoizedState !== null && Sf(e, n, t);
          else if (e.tag === 19)
            Sf(e, n, t);
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
  if (Y(re, r), !(t.mode & 1))
    t.memoizedState = null;
  else
    switch (o) {
      case "forwards":
        for (n = t.child, o = null; n !== null; )
          e = n.alternate, e !== null && Hi(e) === null && (o = n), n = n.sibling;
        n = o, n === null ? (o = t.child, t.child = null) : (o = n.sibling, n.sibling = null), Rs(t, !1, o, n, i);
        break;
      case "backwards":
        for (n = null, o = t.child, t.child = null; o !== null; ) {
          if (e = o.alternate, e !== null && Hi(e) === null) {
            t.child = o;
            break;
          }
          e = o.sibling, o.sibling = n, n = o, o = e;
        }
        Rs(t, !0, n, null, i);
        break;
      case "together":
        Rs(t, !1, null, null, void 0);
        break;
      default:
        t.memoizedState = null;
    }
  return t.child;
}
function Si(e, t) {
  !(t.mode & 1) && e !== null && (e.alternate = null, t.alternate = null, t.flags |= 2);
}
function Ht(e, t, n) {
  if (e !== null && (t.dependencies = e.dependencies), Nn |= t.lanes, !(n & t.childLanes))
    return null;
  if (e !== null && t.child !== e.child)
    throw Error(P(153));
  if (t.child !== null) {
    for (e = t.child, n = pn(e, e.pendingProps), t.child = n, n.return = t; e.sibling !== null; )
      e = e.sibling, n = n.sibling = pn(e, e.pendingProps), n.return = t;
    n.sibling = null;
  }
  return t.child;
}
function ug(e, t, n) {
  switch (t.tag) {
    case 3:
      vm(t), pr();
      break;
    case 5:
      Kp(t);
      break;
    case 1:
      Ue(t.type) && Fi(t);
      break;
    case 4:
      xu(t, t.stateNode.containerInfo);
      break;
    case 10:
      var r = t.type._context, o = t.memoizedProps.value;
      Y(Wi, r._currentValue), r._currentValue = o;
      break;
    case 13:
      if (r = t.memoizedState, r !== null)
        return r.dehydrated !== null ? (Y(re, re.current & 1), t.flags |= 128, null) : n & t.child.childLanes ? Sm(e, t, n) : (Y(re, re.current & 1), e = Ht(e, t, n), e !== null ? e.sibling : null);
      Y(re, re.current & 1);
      break;
    case 19:
      if (r = (n & t.childLanes) !== 0, e.flags & 128) {
        if (r)
          return xm(e, t, n);
        t.flags |= 128;
      }
      if (o = t.memoizedState, o !== null && (o.rendering = null, o.tail = null, o.lastEffect = null), Y(re, re.current), r)
        break;
      return null;
    case 22:
    case 23:
      return t.lanes = 0, ym(e, t, n);
  }
  return Ht(e, t, n);
}
var wm, Pa, km, Cm;
wm = function(e, t) {
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
Pa = function() {
};
km = function(e, t, n, r) {
  var o = e.memoizedProps;
  if (o !== r) {
    e = t.stateNode, _n(zt.current);
    var i = null;
    switch (n) {
      case "input":
        o = Qs(e, o), r = Qs(e, r), i = [];
        break;
      case "select":
        o = le({}, o, { value: void 0 }), r = le({}, r, { value: void 0 }), i = [];
        break;
      case "textarea":
        o = qs(e, o), r = qs(e, r), i = [];
        break;
      default:
        typeof o.onClick != "function" && typeof r.onClick == "function" && (e.onclick = Ai);
    }
    Js(n, r);
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
Cm = function(e, t, n, r) {
  n !== r && (t.flags |= 4);
};
function Ar(e, t) {
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
function cg(e, t, n) {
  var r = t.pendingProps;
  switch (pu(t), t.tag) {
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
      return Ue(t.type) && Di(), Me(t), null;
    case 3:
      return r = t.stateNode, hr(), J(We), J(Le), ku(), r.pendingContext && (r.context = r.pendingContext, r.pendingContext = null), (e === null || e.child === null) && (ti(t) ? t.flags |= 4 : e === null || e.memoizedState.isDehydrated && !(t.flags & 256) || (t.flags |= 1024, xt !== null && (La(xt), xt = null))), Pa(e, t), Me(t), null;
    case 5:
      wu(t);
      var o = _n(yo.current);
      if (n = t.type, e !== null && t.stateNode != null)
        km(e, t, n, r, o), e.ref !== t.ref && (t.flags |= 512, t.flags |= 2097152);
      else {
        if (!r) {
          if (t.stateNode === null)
            throw Error(P(166));
          return Me(t), null;
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
              for (o = 0; o < Vr.length; o++)
                Z(Vr[o], r);
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
              Tc(r, i), Z("invalid", r);
              break;
            case "select":
              r._wrapperState = { wasMultiple: !!i.multiple }, Z("invalid", r);
              break;
            case "textarea":
              Rc(r, i), Z("invalid", r);
          }
          Js(n, i), o = null;
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
              Ko(r), $c(r, i, !0);
              break;
            case "textarea":
              Ko(r), Oc(r);
              break;
            case "select":
            case "option":
              break;
            default:
              typeof i.onClick == "function" && (r.onclick = Ai);
          }
          r = o, t.updateQueue = r, r !== null && (t.flags |= 4);
        } else {
          l = o.nodeType === 9 ? o : o.ownerDocument, e === "http://www.w3.org/1999/xhtml" && (e = qd(n)), e === "http://www.w3.org/1999/xhtml" ? n === "script" ? (e = l.createElement("div"), e.innerHTML = "<script><\/script>", e = e.removeChild(e.firstChild)) : typeof r.is == "string" ? e = l.createElement(n, { is: r.is }) : (e = l.createElement(n), n === "select" && (l = e, r.multiple ? l.multiple = !0 : r.size && (l.size = r.size))) : e = l.createElementNS(e, n), e[Mt] = t, e[mo] = r, wm(e, t, !1, !1), t.stateNode = e;
          e: {
            switch (l = ea(n, r), n) {
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
                for (o = 0; o < Vr.length; o++)
                  Z(Vr[o], e);
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
                Tc(e, r), o = Qs(e, r), Z("invalid", e);
                break;
              case "option":
                o = r;
                break;
              case "select":
                e._wrapperState = { wasMultiple: !!r.multiple }, o = le({}, r, { value: void 0 }), Z("invalid", e);
                break;
              case "textarea":
                Rc(e, r), o = qs(e, r), Z("invalid", e);
                break;
              default:
                o = r;
            }
            Js(n, o), s = o;
            for (i in s)
              if (s.hasOwnProperty(i)) {
                var a = s[i];
                i === "style" ? ep(e, a) : i === "dangerouslySetInnerHTML" ? (a = a ? a.__html : void 0, a != null && Zd(e, a)) : i === "children" ? typeof a == "string" ? (n !== "textarea" || a !== "") && oo(e, a) : typeof a == "number" && oo(e, "" + a) : i !== "suppressContentEditableWarning" && i !== "suppressHydrationWarning" && i !== "autoFocus" && (ro.hasOwnProperty(i) ? a != null && i === "onScroll" && Z("scroll", e) : a != null && Za(e, i, a, l));
              }
            switch (n) {
              case "input":
                Ko(e), $c(e, r, !1);
                break;
              case "textarea":
                Ko(e), Oc(e);
                break;
              case "option":
                r.value != null && e.setAttribute("value", "" + mn(r.value));
                break;
              case "select":
                e.multiple = !!r.multiple, i = r.value, i != null ? rr(e, !!r.multiple, i, !1) : r.defaultValue != null && rr(
                  e,
                  !!r.multiple,
                  r.defaultValue,
                  !0
                );
                break;
              default:
                typeof o.onClick == "function" && (e.onclick = Ai);
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
        Cm(e, t, e.memoizedProps, r);
      else {
        if (typeof r != "string" && t.stateNode === null)
          throw Error(P(166));
        if (n = _n(yo.current), _n(zt.current), ti(t)) {
          if (r = t.stateNode, n = t.memoizedProps, r[Mt] = t, (i = r.nodeValue !== n) && (e = Ye, e !== null))
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
      return Me(t), null;
    case 13:
      if (J(re), r = t.memoizedState, e === null || e.memoizedState !== null && e.memoizedState.dehydrated !== null) {
        if (ne && Qe !== null && t.mode & 1 && !(t.flags & 128))
          Bp(), pr(), t.flags |= 98560, i = !1;
        else if (i = ti(t), r !== null && r.dehydrated !== null) {
          if (e === null) {
            if (!i)
              throw Error(P(318));
            if (i = t.memoizedState, i = i !== null ? i.dehydrated : null, !i)
              throw Error(P(317));
            i[Mt] = t;
          } else
            pr(), !(t.flags & 128) && (t.memoizedState = null), t.flags |= 4;
          Me(t), i = !1;
        } else
          xt !== null && (La(xt), xt = null), i = !0;
        if (!i)
          return t.flags & 65536 ? t : null;
      }
      return t.flags & 128 ? (t.lanes = n, t) : (r = r !== null, r !== (e !== null && e.memoizedState !== null) && r && (t.child.flags |= 8192, t.mode & 1 && (e === null || re.current & 1 ? we === 0 && (we = 3) : Lu())), t.updateQueue !== null && (t.flags |= 4), Me(t), null);
    case 4:
      return hr(), Pa(e, t), e === null && fo(t.stateNode.containerInfo), Me(t), null;
    case 10:
      return gu(t.type._context), Me(t), null;
    case 17:
      return Ue(t.type) && Di(), Me(t), null;
    case 19:
      if (J(re), i = t.memoizedState, i === null)
        return Me(t), null;
      if (r = (t.flags & 128) !== 0, l = i.rendering, l === null)
        if (r)
          Ar(i, !1);
        else {
          if (we !== 0 || e !== null && e.flags & 128)
            for (e = t.child; e !== null; ) {
              if (l = Hi(e), l !== null) {
                for (t.flags |= 128, Ar(i, !1), r = l.updateQueue, r !== null && (t.updateQueue = r, t.flags |= 4), t.subtreeFlags = 0, r = n, n = t.child; n !== null; )
                  i = n, e = r, i.flags &= 14680066, l = i.alternate, l === null ? (i.childLanes = 0, i.lanes = e, i.child = null, i.subtreeFlags = 0, i.memoizedProps = null, i.memoizedState = null, i.updateQueue = null, i.dependencies = null, i.stateNode = null) : (i.childLanes = l.childLanes, i.lanes = l.lanes, i.child = l.child, i.subtreeFlags = 0, i.deletions = null, i.memoizedProps = l.memoizedProps, i.memoizedState = l.memoizedState, i.updateQueue = l.updateQueue, i.type = l.type, e = l.dependencies, i.dependencies = e === null ? null : { lanes: e.lanes, firstContext: e.firstContext }), n = n.sibling;
                return Y(re, re.current & 1 | 2), t.child;
              }
              e = e.sibling;
            }
          i.tail !== null && fe() > gr && (t.flags |= 128, r = !0, Ar(i, !1), t.lanes = 4194304);
        }
      else {
        if (!r)
          if (e = Hi(l), e !== null) {
            if (t.flags |= 128, r = !0, n = e.updateQueue, n !== null && (t.updateQueue = n, t.flags |= 4), Ar(i, !0), i.tail === null && i.tailMode === "hidden" && !l.alternate && !ne)
              return Me(t), null;
          } else
            2 * fe() - i.renderingStartTime > gr && n !== 1073741824 && (t.flags |= 128, r = !0, Ar(i, !1), t.lanes = 4194304);
        i.isBackwards ? (l.sibling = t.child, t.child = l) : (n = i.last, n !== null ? n.sibling = l : t.child = l, i.last = l);
      }
      return i.tail !== null ? (t = i.tail, i.rendering = t, i.tail = t.sibling, i.renderingStartTime = fe(), t.sibling = null, n = re.current, Y(re, r ? n & 1 | 2 : n & 1), t) : (Me(t), null);
    case 22:
    case 23:
      return zu(), r = t.memoizedState !== null, e !== null && e.memoizedState !== null !== r && (t.flags |= 8192), r && t.mode & 1 ? Ke & 1073741824 && (Me(t), t.subtreeFlags & 6 && (t.flags |= 8192)) : Me(t), null;
    case 24:
      return null;
    case 25:
      return null;
  }
  throw Error(P(156, t.tag));
}
function fg(e, t) {
  switch (pu(t), t.tag) {
    case 1:
      return Ue(t.type) && Di(), e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, t) : null;
    case 3:
      return hr(), J(We), J(Le), ku(), e = t.flags, e & 65536 && !(e & 128) ? (t.flags = e & -65537 | 128, t) : null;
    case 5:
      return wu(t), null;
    case 13:
      if (J(re), e = t.memoizedState, e !== null && e.dehydrated !== null) {
        if (t.alternate === null)
          throw Error(P(340));
        pr();
      }
      return e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, t) : null;
    case 19:
      return J(re), null;
    case 4:
      return hr(), null;
    case 10:
      return gu(t.type._context), null;
    case 22:
    case 23:
      return zu(), null;
    case 24:
      return null;
    default:
      return null;
  }
}
var oi = !1, ze = !1, dg = typeof WeakSet == "function" ? WeakSet : Set, M = null;
function tr(e, t) {
  var n = e.ref;
  if (n !== null)
    if (typeof n == "function")
      try {
        n(null);
      } catch (r) {
        ce(e, t, r);
      }
    else
      n.current = null;
}
function Ta(e, t, n) {
  try {
    n();
  } catch (r) {
    ce(e, t, r);
  }
}
var xf = !1;
function pg(e, t) {
  if (ca = Li, e = $p(), fu(e)) {
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
          var l = 0, s = -1, a = -1, u = 0, d = 0, f = e, m = null;
          t:
            for (; ; ) {
              for (var v; f !== n || o !== 0 && f.nodeType !== 3 || (s = l + o), f !== i || r !== 0 && f.nodeType !== 3 || (a = l + r), f.nodeType === 3 && (l += f.nodeValue.length), (v = f.firstChild) !== null; )
                m = f, f = v;
              for (; ; ) {
                if (f === e)
                  break t;
                if (m === n && ++u === o && (s = l), m === i && ++d === r && (a = l), (v = f.nextSibling) !== null)
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
  for (fa = { focusedElem: e, selectionRange: n }, Li = !1, M = t; M !== null; )
    if (t = M, e = t.child, (t.subtreeFlags & 1028) !== 0 && e !== null)
      e.return = t, M = e;
    else
      for (; M !== null; ) {
        t = M;
        try {
          var g = t.alternate;
          if (t.flags & 1024)
            switch (t.tag) {
              case 0:
              case 11:
              case 15:
                break;
              case 1:
                if (g !== null) {
                  var y = g.memoizedProps, _ = g.memoizedState, p = t.stateNode, c = p.getSnapshotBeforeUpdate(t.elementType === t.type ? y : vt(t.type, y), _);
                  p.__reactInternalSnapshotBeforeUpdate = c;
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
          ce(t, t.return, S);
        }
        if (e = t.sibling, e !== null) {
          e.return = t.return, M = e;
          break;
        }
        M = t.return;
      }
  return g = xf, xf = !1, g;
}
function Jr(e, t, n) {
  var r = t.updateQueue;
  if (r = r !== null ? r.lastEffect : null, r !== null) {
    var o = r = r.next;
    do {
      if ((o.tag & e) === e) {
        var i = o.destroy;
        o.destroy = void 0, i !== void 0 && Ta(t, n, i);
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
function $a(e) {
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
function Em(e) {
  var t = e.alternate;
  t !== null && (e.alternate = null, Em(t)), e.child = null, e.deletions = null, e.sibling = null, e.tag === 5 && (t = e.stateNode, t !== null && (delete t[Mt], delete t[mo], delete t[ma], delete t[Yy], delete t[Xy])), e.stateNode = null, e.return = null, e.dependencies = null, e.memoizedProps = null, e.memoizedState = null, e.pendingProps = null, e.stateNode = null, e.updateQueue = null;
}
function _m(e) {
  return e.tag === 5 || e.tag === 3 || e.tag === 4;
}
function wf(e) {
  e:
    for (; ; ) {
      for (; e.sibling === null; ) {
        if (e.return === null || _m(e.return))
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
function Ra(e, t, n) {
  var r = e.tag;
  if (r === 5 || r === 6)
    e = e.stateNode, t ? n.nodeType === 8 ? n.parentNode.insertBefore(e, t) : n.insertBefore(e, t) : (n.nodeType === 8 ? (t = n.parentNode, t.insertBefore(e, n)) : (t = n, t.appendChild(e)), n = n._reactRootContainer, n != null || t.onclick !== null || (t.onclick = Ai));
  else if (r !== 4 && (e = e.child, e !== null))
    for (Ra(e, t, n), e = e.sibling; e !== null; )
      Ra(e, t, n), e = e.sibling;
}
function Oa(e, t, n) {
  var r = e.tag;
  if (r === 5 || r === 6)
    e = e.stateNode, t ? n.insertBefore(e, t) : n.appendChild(e);
  else if (r !== 4 && (e = e.child, e !== null))
    for (Oa(e, t, n), e = e.sibling; e !== null; )
      Oa(e, t, n), e = e.sibling;
}
var Pe = null, St = !1;
function qt(e, t, n) {
  for (n = n.child; n !== null; )
    Pm(e, t, n), n = n.sibling;
}
function Pm(e, t, n) {
  if (Nt && typeof Nt.onCommitFiberUnmount == "function")
    try {
      Nt.onCommitFiberUnmount(al, n);
    } catch {
    }
  switch (n.tag) {
    case 5:
      ze || tr(n, t);
    case 6:
      var r = Pe, o = St;
      Pe = null, qt(e, t, n), Pe = r, St = o, Pe !== null && (St ? (e = Pe, n = n.stateNode, e.nodeType === 8 ? e.parentNode.removeChild(n) : e.removeChild(n)) : Pe.removeChild(n.stateNode));
      break;
    case 18:
      Pe !== null && (St ? (e = Pe, n = n.stateNode, e.nodeType === 8 ? ks(e.parentNode, n) : e.nodeType === 1 && ks(e, n), ao(e)) : ks(Pe, n.stateNode));
      break;
    case 4:
      r = Pe, o = St, Pe = n.stateNode.containerInfo, St = !0, qt(e, t, n), Pe = r, St = o;
      break;
    case 0:
    case 11:
    case 14:
    case 15:
      if (!ze && (r = n.updateQueue, r !== null && (r = r.lastEffect, r !== null))) {
        o = r = r.next;
        do {
          var i = o, l = i.destroy;
          i = i.tag, l !== void 0 && (i & 2 || i & 4) && Ta(n, t, l), o = o.next;
        } while (o !== r);
      }
      qt(e, t, n);
      break;
    case 1:
      if (!ze && (tr(n, t), r = n.stateNode, typeof r.componentWillUnmount == "function"))
        try {
          r.props = n.memoizedProps, r.state = n.memoizedState, r.componentWillUnmount();
        } catch (s) {
          ce(n, t, s);
        }
      qt(e, t, n);
      break;
    case 21:
      qt(e, t, n);
      break;
    case 22:
      n.mode & 1 ? (ze = (r = ze) || n.memoizedState !== null, qt(e, t, n), ze = r) : qt(e, t, n);
      break;
    default:
      qt(e, t, n);
  }
}
function kf(e) {
  var t = e.updateQueue;
  if (t !== null) {
    e.updateQueue = null;
    var n = e.stateNode;
    n === null && (n = e.stateNode = new dg()), t.forEach(function(r) {
      var o = kg.bind(null, e, r);
      n.has(r) || (n.add(r), r.then(o, o));
    });
  }
}
function gt(e, t) {
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
        Pm(i, l, o), Pe = null, St = !1;
        var a = o.alternate;
        a !== null && (a.return = null), o.return = null;
      } catch (u) {
        ce(o, t, u);
      }
    }
  if (t.subtreeFlags & 12854)
    for (t = t.child; t !== null; )
      Tm(t, e), t = t.sibling;
}
function Tm(e, t) {
  var n = e.alternate, r = e.flags;
  switch (e.tag) {
    case 0:
    case 11:
    case 14:
    case 15:
      if (gt(t, e), Tt(e), r & 4) {
        try {
          Jr(3, e, e.return), yl(3, e);
        } catch (y) {
          ce(e, e.return, y);
        }
        try {
          Jr(5, e, e.return);
        } catch (y) {
          ce(e, e.return, y);
        }
      }
      break;
    case 1:
      gt(t, e), Tt(e), r & 512 && n !== null && tr(n, n.return);
      break;
    case 5:
      if (gt(t, e), Tt(e), r & 512 && n !== null && tr(n, n.return), e.flags & 32) {
        var o = e.stateNode;
        try {
          oo(o, "");
        } catch (y) {
          ce(e, e.return, y);
        }
      }
      if (r & 4 && (o = e.stateNode, o != null)) {
        var i = e.memoizedProps, l = n !== null ? n.memoizedProps : i, s = e.type, a = e.updateQueue;
        if (e.updateQueue = null, a !== null)
          try {
            s === "input" && i.type === "radio" && i.name != null && Yd(o, i), ea(s, l);
            var u = ea(s, i);
            for (l = 0; l < a.length; l += 2) {
              var d = a[l], f = a[l + 1];
              d === "style" ? ep(o, f) : d === "dangerouslySetInnerHTML" ? Zd(o, f) : d === "children" ? oo(o, f) : Za(o, d, f, u);
            }
            switch (s) {
              case "input":
                Ys(o, i);
                break;
              case "textarea":
                Xd(o, i);
                break;
              case "select":
                var m = o._wrapperState.wasMultiple;
                o._wrapperState.wasMultiple = !!i.multiple;
                var v = i.value;
                v != null ? rr(o, !!i.multiple, v, !1) : m !== !!i.multiple && (i.defaultValue != null ? rr(
                  o,
                  !!i.multiple,
                  i.defaultValue,
                  !0
                ) : rr(o, !!i.multiple, i.multiple ? [] : "", !1));
            }
            o[mo] = i;
          } catch (y) {
            ce(e, e.return, y);
          }
      }
      break;
    case 6:
      if (gt(t, e), Tt(e), r & 4) {
        if (e.stateNode === null)
          throw Error(P(162));
        o = e.stateNode, i = e.memoizedProps;
        try {
          o.nodeValue = i;
        } catch (y) {
          ce(e, e.return, y);
        }
      }
      break;
    case 3:
      if (gt(t, e), Tt(e), r & 4 && n !== null && n.memoizedState.isDehydrated)
        try {
          ao(t.containerInfo);
        } catch (y) {
          ce(e, e.return, y);
        }
      break;
    case 4:
      gt(t, e), Tt(e);
      break;
    case 13:
      gt(t, e), Tt(e), o = e.child, o.flags & 8192 && (i = o.memoizedState !== null, o.stateNode.isHidden = i, !i || o.alternate !== null && o.alternate.memoizedState !== null || (Mu = fe())), r & 4 && kf(e);
      break;
    case 22:
      if (d = n !== null && n.memoizedState !== null, e.mode & 1 ? (ze = (u = ze) || d, gt(t, e), ze = u) : gt(t, e), Tt(e), r & 8192) {
        if (u = e.memoizedState !== null, (e.stateNode.isHidden = u) && !d && e.mode & 1)
          for (M = e, d = e.child; d !== null; ) {
            for (f = M = d; M !== null; ) {
              switch (m = M, v = m.child, m.tag) {
                case 0:
                case 11:
                case 14:
                case 15:
                  Jr(4, m, m.return);
                  break;
                case 1:
                  tr(m, m.return);
                  var g = m.stateNode;
                  if (typeof g.componentWillUnmount == "function") {
                    r = m, n = m.return;
                    try {
                      t = r, g.props = t.memoizedProps, g.state = t.memoizedState, g.componentWillUnmount();
                    } catch (y) {
                      ce(r, n, y);
                    }
                  }
                  break;
                case 5:
                  tr(m, m.return);
                  break;
                case 22:
                  if (m.memoizedState !== null) {
                    Ef(f);
                    continue;
                  }
              }
              v !== null ? (v.return = m, M = v) : Ef(f);
            }
            d = d.sibling;
          }
        e:
          for (d = null, f = e; ; ) {
            if (f.tag === 5) {
              if (d === null) {
                d = f;
                try {
                  o = f.stateNode, u ? (i = o.style, typeof i.setProperty == "function" ? i.setProperty("display", "none", "important") : i.display = "none") : (s = f.stateNode, a = f.memoizedProps.style, l = a != null && a.hasOwnProperty("display") ? a.display : null, s.style.display = Jd("display", l));
                } catch (y) {
                  ce(e, e.return, y);
                }
              }
            } else if (f.tag === 6) {
              if (d === null)
                try {
                  f.stateNode.nodeValue = u ? "" : f.memoizedProps;
                } catch (y) {
                  ce(e, e.return, y);
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
              d === f && (d = null), f = f.return;
            }
            d === f && (d = null), f.sibling.return = f.return, f = f.sibling;
          }
      }
      break;
    case 19:
      gt(t, e), Tt(e), r & 4 && kf(e);
      break;
    case 21:
      break;
    default:
      gt(
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
          if (_m(n)) {
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
          var i = wf(e);
          Oa(e, i, o);
          break;
        case 3:
        case 4:
          var l = r.stateNode.containerInfo, s = wf(e);
          Ra(e, s, l);
          break;
        default:
          throw Error(P(161));
      }
    } catch (a) {
      ce(e, e.return, a);
    }
    e.flags &= -3;
  }
  t & 4096 && (e.flags &= -4097);
}
function mg(e, t, n) {
  M = e, $m(e);
}
function $m(e, t, n) {
  for (var r = (e.mode & 1) !== 0; M !== null; ) {
    var o = M, i = o.child;
    if (o.tag === 22 && r) {
      var l = o.memoizedState !== null || oi;
      if (!l) {
        var s = o.alternate, a = s !== null && s.memoizedState !== null || ze;
        s = oi;
        var u = ze;
        if (oi = l, (ze = a) && !u)
          for (M = o; M !== null; )
            l = M, a = l.child, l.tag === 22 && l.memoizedState !== null ? _f(o) : a !== null ? (a.return = l, M = a) : _f(o);
        for (; i !== null; )
          M = i, $m(i), i = i.sibling;
        M = o, oi = s, ze = u;
      }
      Cf(e);
    } else
      o.subtreeFlags & 8772 && i !== null ? (i.return = o, M = i) : Cf(e);
  }
}
function Cf(e) {
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
              ze || yl(5, t);
              break;
            case 1:
              var r = t.stateNode;
              if (t.flags & 4 && !ze)
                if (n === null)
                  r.componentDidMount();
                else {
                  var o = t.elementType === t.type ? n.memoizedProps : vt(t.type, n.memoizedProps);
                  r.componentDidUpdate(o, n.memoizedState, r.__reactInternalSnapshotBeforeUpdate);
                }
              var i = t.updateQueue;
              i !== null && sf(t, i, r);
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
                sf(t, l, n);
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
                  var d = u.memoizedState;
                  if (d !== null) {
                    var f = d.dehydrated;
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
        ze || t.flags & 512 && $a(t);
      } catch (m) {
        ce(t, t.return, m);
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
function Ef(e) {
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
function _f(e) {
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
            ce(t, n, a);
          }
          break;
        case 1:
          var r = t.stateNode;
          if (typeof r.componentDidMount == "function") {
            var o = t.return;
            try {
              r.componentDidMount();
            } catch (a) {
              ce(t, o, a);
            }
          }
          var i = t.return;
          try {
            $a(t);
          } catch (a) {
            ce(t, i, a);
          }
          break;
        case 5:
          var l = t.return;
          try {
            $a(t);
          } catch (a) {
            ce(t, l, a);
          }
      }
    } catch (a) {
      ce(t, t.return, a);
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
var hg = Math.ceil, Qi = Qt.ReactCurrentDispatcher, Ru = Qt.ReactCurrentOwner, at = Qt.ReactCurrentBatchConfig, B = 0, Ce = null, ge = null, $e = 0, Ke = 0, nr = gn(0), we = 0, xo = null, Nn = 0, gl = 0, Ou = 0, eo = null, be = null, Mu = 0, gr = 1 / 0, jt = null, Yi = !1, Ma = null, fn = null, ii = !1, on = null, Xi = 0, to = 0, Na = null, xi = -1, wi = 0;
function Ae() {
  return B & 6 ? fe() : xi !== -1 ? xi : xi = fe();
}
function dn(e) {
  return e.mode & 1 ? B & 2 && $e !== 0 ? $e & -$e : Zy.transition !== null ? (wi === 0 && (wi = dp()), wi) : (e = K, e !== 0 || (e = window.event, e = e === void 0 ? 16 : Sp(e.type)), e) : 1;
}
function Ct(e, t, n, r) {
  if (50 < to)
    throw to = 0, Na = null, Error(P(185));
  Ro(e, n, r), (!(B & 2) || e !== Ce) && (e === Ce && (!(B & 2) && (gl |= n), we === 4 && nn(e, $e)), Ve(e, r), n === 1 && B === 0 && !(t.mode & 1) && (gr = fe() + 500, pl && vn()));
}
function Ve(e, t) {
  var n = e.callbackNode;
  Z0(e, t);
  var r = zi(e, e === Ce ? $e : 0);
  if (r === 0)
    n !== null && zc(n), e.callbackNode = null, e.callbackPriority = 0;
  else if (t = r & -r, e.callbackPriority !== t) {
    if (n != null && zc(n), t === 1)
      e.tag === 0 ? qy(Pf.bind(null, e)) : Dp(Pf.bind(null, e)), Gy(function() {
        !(B & 6) && vn();
      }), n = null;
    else {
      switch (pp(r)) {
        case 1:
          n = ru;
          break;
        case 4:
          n = cp;
          break;
        case 16:
          n = Ni;
          break;
        case 536870912:
          n = fp;
          break;
        default:
          n = Ni;
      }
      n = jm(n, Rm.bind(null, e));
    }
    e.callbackPriority = t, e.callbackNode = n;
  }
}
function Rm(e, t) {
  if (xi = -1, wi = 0, B & 6)
    throw Error(P(327));
  var n = e.callbackNode;
  if (ar() && e.callbackNode !== n)
    return null;
  var r = zi(e, e === Ce ? $e : 0);
  if (r === 0)
    return null;
  if (r & 30 || r & e.expiredLanes || t)
    t = qi(e, r);
  else {
    t = r;
    var o = B;
    B |= 2;
    var i = Mm();
    (Ce !== e || $e !== t) && (jt = null, gr = fe() + 500, Tn(e, t));
    do
      try {
        vg();
        break;
      } catch (s) {
        Om(e, s);
      }
    while (1);
    yu(), Qi.current = i, B = o, ge !== null ? t = 0 : (Ce = null, $e = 0, t = we);
  }
  if (t !== 0) {
    if (t === 2 && (o = ia(e), o !== 0 && (r = o, t = za(e, o))), t === 1)
      throw n = xo, Tn(e, 0), nn(e, r), Ve(e, fe()), n;
    if (t === 6)
      nn(e, r);
    else {
      if (o = e.current.alternate, !(r & 30) && !yg(o) && (t = qi(e, r), t === 2 && (i = ia(e), i !== 0 && (r = i, t = za(e, i))), t === 1))
        throw n = xo, Tn(e, 0), nn(e, r), Ve(e, fe()), n;
      switch (e.finishedWork = o, e.finishedLanes = r, t) {
        case 0:
        case 1:
          throw Error(P(345));
        case 2:
          xn(e, be, jt);
          break;
        case 3:
          if (nn(e, r), (r & 130023424) === r && (t = Mu + 500 - fe(), 10 < t)) {
            if (zi(e, 0) !== 0)
              break;
            if (o = e.suspendedLanes, (o & r) !== r) {
              Ae(), e.pingedLanes |= e.suspendedLanes & o;
              break;
            }
            e.timeoutHandle = pa(xn.bind(null, e, be, jt), t);
            break;
          }
          xn(e, be, jt);
          break;
        case 4:
          if (nn(e, r), (r & 4194240) === r)
            break;
          for (t = e.eventTimes, o = -1; 0 < r; ) {
            var l = 31 - kt(r);
            i = 1 << l, l = t[l], l > o && (o = l), r &= ~i;
          }
          if (r = o, r = fe() - r, r = (120 > r ? 120 : 480 > r ? 480 : 1080 > r ? 1080 : 1920 > r ? 1920 : 3e3 > r ? 3e3 : 4320 > r ? 4320 : 1960 * hg(r / 1960)) - r, 10 < r) {
            e.timeoutHandle = pa(xn.bind(null, e, be, jt), r);
            break;
          }
          xn(e, be, jt);
          break;
        case 5:
          xn(e, be, jt);
          break;
        default:
          throw Error(P(329));
      }
    }
  }
  return Ve(e, fe()), e.callbackNode === n ? Rm.bind(null, e) : null;
}
function za(e, t) {
  var n = eo;
  return e.current.memoizedState.isDehydrated && (Tn(e, t).flags |= 256), e = qi(e, t), e !== 2 && (t = be, be = n, t !== null && La(t)), e;
}
function La(e) {
  be === null ? be = e : be.push.apply(be, e);
}
function yg(e) {
  for (var t = e; ; ) {
    if (t.flags & 16384) {
      var n = t.updateQueue;
      if (n !== null && (n = n.stores, n !== null))
        for (var r = 0; r < n.length; r++) {
          var o = n[r], i = o.getSnapshot;
          o = o.value;
          try {
            if (!Et(i(), o))
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
  for (t &= ~Ou, t &= ~gl, e.suspendedLanes |= t, e.pingedLanes &= ~t, e = e.expirationTimes; 0 < t; ) {
    var n = 31 - kt(t), r = 1 << n;
    e[n] = -1, t &= ~r;
  }
}
function Pf(e) {
  if (B & 6)
    throw Error(P(327));
  ar();
  var t = zi(e, 0);
  if (!(t & 1))
    return Ve(e, fe()), null;
  var n = qi(e, t);
  if (e.tag !== 0 && n === 2) {
    var r = ia(e);
    r !== 0 && (t = r, n = za(e, r));
  }
  if (n === 1)
    throw n = xo, Tn(e, 0), nn(e, t), Ve(e, fe()), n;
  if (n === 6)
    throw Error(P(345));
  return e.finishedWork = e.current.alternate, e.finishedLanes = t, xn(e, be, jt), Ve(e, fe()), null;
}
function Nu(e, t) {
  var n = B;
  B |= 1;
  try {
    return e(t);
  } finally {
    B = n, B === 0 && (gr = fe() + 500, pl && vn());
  }
}
function zn(e) {
  on !== null && on.tag === 0 && !(B & 6) && ar();
  var t = B;
  B |= 1;
  var n = at.transition, r = K;
  try {
    if (at.transition = null, K = 1, e)
      return e();
  } finally {
    K = r, at.transition = n, B = t, !(B & 6) && vn();
  }
}
function zu() {
  Ke = nr.current, J(nr);
}
function Tn(e, t) {
  e.finishedWork = null, e.finishedLanes = 0;
  var n = e.timeoutHandle;
  if (n !== -1 && (e.timeoutHandle = -1, Ky(n)), ge !== null)
    for (n = ge.return; n !== null; ) {
      var r = n;
      switch (pu(r), r.tag) {
        case 1:
          r = r.type.childContextTypes, r != null && Di();
          break;
        case 3:
          hr(), J(We), J(Le), ku();
          break;
        case 5:
          wu(r);
          break;
        case 4:
          hr();
          break;
        case 13:
          J(re);
          break;
        case 19:
          J(re);
          break;
        case 10:
          gu(r.type._context);
          break;
        case 22:
        case 23:
          zu();
      }
      n = n.return;
    }
  if (Ce = e, ge = e = pn(e.current, null), $e = Ke = t, we = 0, xo = null, Ou = gl = Nn = 0, be = eo = null, En !== null) {
    for (t = 0; t < En.length; t++)
      if (n = En[t], r = n.interleaved, r !== null) {
        n.interleaved = null;
        var o = r.next, i = n.pending;
        if (i !== null) {
          var l = i.next;
          i.next = o, r.next = l;
        }
        n.pending = r;
      }
    En = null;
  }
  return e;
}
function Om(e, t) {
  do {
    var n = ge;
    try {
      if (yu(), gi.current = Gi, Ki) {
        for (var r = ie.memoizedState; r !== null; ) {
          var o = r.queue;
          o !== null && (o.pending = null), r = r.next;
        }
        Ki = !1;
      }
      if (Mn = 0, ke = xe = ie = null, Zr = !1, go = 0, Ru.current = null, n === null || n.return === null) {
        we = 1, xo = t, ge = null;
        break;
      }
      e: {
        var i = e, l = n.return, s = n, a = t;
        if (t = $e, s.flags |= 32768, a !== null && typeof a == "object" && typeof a.then == "function") {
          var u = a, d = s, f = d.tag;
          if (!(d.mode & 1) && (f === 0 || f === 11 || f === 15)) {
            var m = d.alternate;
            m ? (d.updateQueue = m.updateQueue, d.memoizedState = m.memoizedState, d.lanes = m.lanes) : (d.updateQueue = null, d.memoizedState = null);
          }
          var v = pf(l);
          if (v !== null) {
            v.flags &= -257, mf(v, l, s, i, t), v.mode & 1 && df(i, u, t), t = v, a = u;
            var g = t.updateQueue;
            if (g === null) {
              var y = /* @__PURE__ */ new Set();
              y.add(a), t.updateQueue = y;
            } else
              g.add(a);
            break e;
          } else {
            if (!(t & 1)) {
              df(i, u, t), Lu();
              break e;
            }
            a = Error(P(426));
          }
        } else if (ne && s.mode & 1) {
          var _ = pf(l);
          if (_ !== null) {
            !(_.flags & 65536) && (_.flags |= 256), mf(_, l, s, i, t), mu(yr(a, s));
            break e;
          }
        }
        i = a = yr(a, s), we !== 4 && (we = 2), eo === null ? eo = [i] : eo.push(i), i = l;
        do {
          switch (i.tag) {
            case 3:
              i.flags |= 65536, t &= -t, i.lanes |= t;
              var p = pm(i, a, t);
              lf(i, p);
              break e;
            case 1:
              s = a;
              var c = i.type, h = i.stateNode;
              if (!(i.flags & 128) && (typeof c.getDerivedStateFromError == "function" || h !== null && typeof h.componentDidCatch == "function" && (fn === null || !fn.has(h)))) {
                i.flags |= 65536, t &= -t, i.lanes |= t;
                var S = mm(i, s, t);
                lf(i, S);
                break e;
              }
          }
          i = i.return;
        } while (i !== null);
      }
      zm(n);
    } catch (E) {
      t = E, ge === n && n !== null && (ge = n = n.return);
      continue;
    }
    break;
  } while (1);
}
function Mm() {
  var e = Qi.current;
  return Qi.current = Gi, e === null ? Gi : e;
}
function Lu() {
  (we === 0 || we === 3 || we === 2) && (we = 4), Ce === null || !(Nn & 268435455) && !(gl & 268435455) || nn(Ce, $e);
}
function qi(e, t) {
  var n = B;
  B |= 2;
  var r = Mm();
  (Ce !== e || $e !== t) && (jt = null, Tn(e, t));
  do
    try {
      gg();
      break;
    } catch (o) {
      Om(e, o);
    }
  while (1);
  if (yu(), B = n, Qi.current = r, ge !== null)
    throw Error(P(261));
  return Ce = null, $e = 0, we;
}
function gg() {
  for (; ge !== null; )
    Nm(ge);
}
function vg() {
  for (; ge !== null && !U0(); )
    Nm(ge);
}
function Nm(e) {
  var t = Im(e.alternate, e, Ke);
  e.memoizedProps = e.pendingProps, t === null ? zm(e) : ge = t, Ru.current = null;
}
function zm(e) {
  var t = e;
  do {
    var n = t.alternate;
    if (e = t.return, t.flags & 32768) {
      if (n = fg(n, t), n !== null) {
        n.flags &= 32767, ge = n;
        return;
      }
      if (e !== null)
        e.flags |= 32768, e.subtreeFlags = 0, e.deletions = null;
      else {
        we = 6, ge = null;
        return;
      }
    } else if (n = cg(n, t, Ke), n !== null) {
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
function xn(e, t, n) {
  var r = K, o = at.transition;
  try {
    at.transition = null, K = 1, Sg(e, t, n, r);
  } finally {
    at.transition = o, K = r;
  }
  return null;
}
function Sg(e, t, n, r) {
  do
    ar();
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
  if (J0(e, i), e === Ce && (ge = Ce = null, $e = 0), !(n.subtreeFlags & 2064) && !(n.flags & 2064) || ii || (ii = !0, jm(Ni, function() {
    return ar(), null;
  })), i = (n.flags & 15990) !== 0, n.subtreeFlags & 15990 || i) {
    i = at.transition, at.transition = null;
    var l = K;
    K = 1;
    var s = B;
    B |= 4, Ru.current = null, pg(e, n), Tm(n, e), Fy(fa), Li = !!ca, fa = ca = null, e.current = n, mg(n), V0(), B = s, K = l, at.transition = i;
  } else
    e.current = n;
  if (ii && (ii = !1, on = e, Xi = o), i = e.pendingLanes, i === 0 && (fn = null), G0(n.stateNode), Ve(e, fe()), t !== null)
    for (r = e.onRecoverableError, n = 0; n < t.length; n++)
      o = t[n], r(o.value, { componentStack: o.stack, digest: o.digest });
  if (Yi)
    throw Yi = !1, e = Ma, Ma = null, e;
  return Xi & 1 && e.tag !== 0 && ar(), i = e.pendingLanes, i & 1 ? e === Na ? to++ : (to = 0, Na = e) : to = 0, vn(), null;
}
function ar() {
  if (on !== null) {
    var e = pp(Xi), t = at.transition, n = K;
    try {
      if (at.transition = null, K = 16 > e ? 16 : e, on === null)
        var r = !1;
      else {
        if (e = on, on = null, Xi = 0, B & 6)
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
                  var d = M;
                  switch (d.tag) {
                    case 0:
                    case 11:
                    case 15:
                      Jr(8, d, i);
                  }
                  var f = d.child;
                  if (f !== null)
                    f.return = d, M = f;
                  else
                    for (; M !== null; ) {
                      d = M;
                      var m = d.sibling, v = d.return;
                      if (Em(d), d === u) {
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
              var g = i.alternate;
              if (g !== null) {
                var y = g.child;
                if (y !== null) {
                  g.child = null;
                  do {
                    var _ = y.sibling;
                    y.sibling = null, y = _;
                  } while (y !== null);
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
                      Jr(9, i, i.return);
                  }
                var p = i.sibling;
                if (p !== null) {
                  p.return = i.return, M = p;
                  break e;
                }
                M = i.return;
              }
        }
        var c = e.current;
        for (M = c; M !== null; ) {
          l = M;
          var h = l.child;
          if (l.subtreeFlags & 2064 && h !== null)
            h.return = l, M = h;
          else
            e:
              for (l = c; M !== null; ) {
                if (s = M, s.flags & 2048)
                  try {
                    switch (s.tag) {
                      case 0:
                      case 11:
                      case 15:
                        yl(9, s);
                    }
                  } catch (E) {
                    ce(s, s.return, E);
                  }
                if (s === l) {
                  M = null;
                  break e;
                }
                var S = s.sibling;
                if (S !== null) {
                  S.return = s.return, M = S;
                  break e;
                }
                M = s.return;
              }
        }
        if (B = o, vn(), Nt && typeof Nt.onPostCommitFiberRoot == "function")
          try {
            Nt.onPostCommitFiberRoot(al, e);
          } catch {
          }
        r = !0;
      }
      return r;
    } finally {
      K = n, at.transition = t;
    }
  }
  return !1;
}
function Tf(e, t, n) {
  t = yr(n, t), t = pm(e, t, 1), e = cn(e, t, 1), t = Ae(), e !== null && (Ro(e, 1, t), Ve(e, t));
}
function ce(e, t, n) {
  if (e.tag === 3)
    Tf(e, e, n);
  else
    for (; t !== null; ) {
      if (t.tag === 3) {
        Tf(t, e, n);
        break;
      } else if (t.tag === 1) {
        var r = t.stateNode;
        if (typeof t.type.getDerivedStateFromError == "function" || typeof r.componentDidCatch == "function" && (fn === null || !fn.has(r))) {
          e = yr(n, e), e = mm(t, e, 1), t = cn(t, e, 1), e = Ae(), t !== null && (Ro(t, 1, e), Ve(t, e));
          break;
        }
      }
      t = t.return;
    }
}
function xg(e, t, n) {
  var r = e.pingCache;
  r !== null && r.delete(t), t = Ae(), e.pingedLanes |= e.suspendedLanes & n, Ce === e && ($e & n) === n && (we === 4 || we === 3 && ($e & 130023424) === $e && 500 > fe() - Mu ? Tn(e, 0) : Ou |= n), Ve(e, t);
}
function Lm(e, t) {
  t === 0 && (e.mode & 1 ? (t = Yo, Yo <<= 1, !(Yo & 130023424) && (Yo = 4194304)) : t = 1);
  var n = Ae();
  e = Vt(e, t), e !== null && (Ro(e, t, n), Ve(e, n));
}
function wg(e) {
  var t = e.memoizedState, n = 0;
  t !== null && (n = t.retryLane), Lm(e, n);
}
function kg(e, t) {
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
  r !== null && r.delete(t), Lm(e, n);
}
var Im;
Im = function(e, t, n) {
  if (e !== null)
    if (e.memoizedProps !== t.pendingProps || We.current)
      Be = !0;
    else {
      if (!(e.lanes & n) && !(t.flags & 128))
        return Be = !1, ug(e, t, n);
      Be = !!(e.flags & 131072);
    }
  else
    Be = !1, ne && t.flags & 1048576 && Fp(t, Bi, t.index);
  switch (t.lanes = 0, t.tag) {
    case 2:
      var r = t.type;
      Si(e, t), e = t.pendingProps;
      var o = dr(t, Le.current);
      sr(t, n), o = Eu(null, t, r, e, o, n);
      var i = _u();
      return t.flags |= 1, typeof o == "object" && o !== null && typeof o.render == "function" && o.$$typeof === void 0 ? (t.tag = 1, t.memoizedState = null, t.updateQueue = null, Ue(r) ? (i = !0, Fi(t)) : i = !1, t.memoizedState = o.state !== null && o.state !== void 0 ? o.state : null, Su(t), o.updater = hl, t.stateNode = o, o._reactInternals = t, xa(t, r, e, n), t = Ca(null, t, r, !0, i, n)) : (t.tag = 0, ne && i && du(t), je(null, t, o, n), t = t.child), t;
    case 16:
      r = t.elementType;
      e: {
        switch (Si(e, t), e = t.pendingProps, o = r._init, r = o(r._payload), t.type = r, o = t.tag = Eg(r), e = vt(r, e), o) {
          case 0:
            t = ka(null, t, r, e, n);
            break e;
          case 1:
            t = gf(null, t, r, e, n);
            break e;
          case 11:
            t = hf(null, t, r, e, n);
            break e;
          case 14:
            t = yf(null, t, r, vt(r.type, e), n);
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
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : vt(r, o), ka(e, t, r, o, n);
    case 1:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : vt(r, o), gf(e, t, r, o, n);
    case 3:
      e: {
        if (vm(t), e === null)
          throw Error(P(387));
        r = t.pendingProps, i = t.memoizedState, o = i.element, Hp(e, t), Vi(t, r, null, n);
        var l = t.memoizedState;
        if (r = l.element, i.isDehydrated)
          if (i = { element: r, isDehydrated: !1, cache: l.cache, pendingSuspenseBoundaries: l.pendingSuspenseBoundaries, transitions: l.transitions }, t.updateQueue.baseState = i, t.memoizedState = i, t.flags & 256) {
            o = yr(Error(P(423)), t), t = vf(e, t, r, n, o);
            break e;
          } else if (r !== o) {
            o = yr(Error(P(424)), t), t = vf(e, t, r, n, o);
            break e;
          } else
            for (Qe = un(t.stateNode.containerInfo.firstChild), Ye = t, ne = !0, xt = null, n = Up(t, null, r, n), t.child = n; n; )
              n.flags = n.flags & -3 | 4096, n = n.sibling;
        else {
          if (pr(), r === o) {
            t = Ht(e, t, n);
            break e;
          }
          je(e, t, r, n);
        }
        t = t.child;
      }
      return t;
    case 5:
      return Kp(t), e === null && ga(t), r = t.type, o = t.pendingProps, i = e !== null ? e.memoizedProps : null, l = o.children, da(r, o) ? l = null : i !== null && da(r, i) && (t.flags |= 32), gm(e, t), je(e, t, l, n), t.child;
    case 6:
      return e === null && ga(t), null;
    case 13:
      return Sm(e, t, n);
    case 4:
      return xu(t, t.stateNode.containerInfo), r = t.pendingProps, e === null ? t.child = mr(t, null, r, n) : je(e, t, r, n), t.child;
    case 11:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : vt(r, o), hf(e, t, r, o, n);
    case 7:
      return je(e, t, t.pendingProps, n), t.child;
    case 8:
      return je(e, t, t.pendingProps.children, n), t.child;
    case 12:
      return je(e, t, t.pendingProps.children, n), t.child;
    case 10:
      e: {
        if (r = t.type._context, o = t.pendingProps, i = t.memoizedProps, l = o.value, Y(Wi, r._currentValue), r._currentValue = l, i !== null)
          if (Et(i.value, l)) {
            if (i.children === o.children && !We.current) {
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
                        var d = u.pending;
                        d === null ? a.next = a : (a.next = d.next, d.next = a), u.pending = a;
                      }
                    }
                    i.lanes |= n, a = i.alternate, a !== null && (a.lanes |= n), va(
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
                l.lanes |= n, s = l.alternate, s !== null && (s.lanes |= n), va(l, n, t), l = i.sibling;
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
        je(e, t, o.children, n), t = t.child;
      }
      return t;
    case 9:
      return o = t.type, r = t.pendingProps.children, sr(t, n), o = ut(o), r = r(o), t.flags |= 1, je(e, t, r, n), t.child;
    case 14:
      return r = t.type, o = vt(r, t.pendingProps), o = vt(r.type, o), yf(e, t, r, o, n);
    case 15:
      return hm(e, t, t.type, t.pendingProps, n);
    case 17:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : vt(r, o), Si(e, t), t.tag = 1, Ue(r) ? (e = !0, Fi(t)) : e = !1, sr(t, n), dm(t, r, o), xa(t, r, o, n), Ca(null, t, r, !0, e, n);
    case 19:
      return xm(e, t, n);
    case 22:
      return ym(e, t, n);
  }
  throw Error(P(156, t.tag));
};
function jm(e, t) {
  return up(e, t);
}
function Cg(e, t, n, r) {
  this.tag = e, this.key = n, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.ref = null, this.pendingProps = t, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = r, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
}
function st(e, t, n, r) {
  return new Cg(e, t, n, r);
}
function Iu(e) {
  return e = e.prototype, !(!e || !e.isReactComponent);
}
function Eg(e) {
  if (typeof e == "function")
    return Iu(e) ? 1 : 0;
  if (e != null) {
    if (e = e.$$typeof, e === eu)
      return 11;
    if (e === tu)
      return 14;
  }
  return 2;
}
function pn(e, t) {
  var n = e.alternate;
  return n === null ? (n = st(e.tag, t, e.key, e.mode), n.elementType = e.elementType, n.type = e.type, n.stateNode = e.stateNode, n.alternate = e, e.alternate = n) : (n.pendingProps = t, n.type = e.type, n.flags = 0, n.subtreeFlags = 0, n.deletions = null), n.flags = e.flags & 14680064, n.childLanes = e.childLanes, n.lanes = e.lanes, n.child = e.child, n.memoizedProps = e.memoizedProps, n.memoizedState = e.memoizedState, n.updateQueue = e.updateQueue, t = e.dependencies, n.dependencies = t === null ? null : { lanes: t.lanes, firstContext: t.firstContext }, n.sibling = e.sibling, n.index = e.index, n.ref = e.ref, n;
}
function ki(e, t, n, r, o, i) {
  var l = 2;
  if (r = e, typeof e == "function")
    Iu(e) && (l = 1);
  else if (typeof e == "string")
    l = 5;
  else
    e:
      switch (e) {
        case Kn:
          return $n(n.children, o, i, t);
        case Ja:
          l = 8, o |= 8;
          break;
        case Vs:
          return e = st(12, n, t, o | 2), e.elementType = Vs, e.lanes = i, e;
        case Hs:
          return e = st(13, n, t, o), e.elementType = Hs, e.lanes = i, e;
        case Ks:
          return e = st(19, n, t, o), e.elementType = Ks, e.lanes = i, e;
        case Kd:
          return vl(n, o, i, t);
        default:
          if (typeof e == "object" && e !== null)
            switch (e.$$typeof) {
              case Vd:
                l = 10;
                break e;
              case Hd:
                l = 9;
                break e;
              case eu:
                l = 11;
                break e;
              case tu:
                l = 14;
                break e;
              case Jt:
                l = 16, r = null;
                break e;
            }
          throw Error(P(130, e == null ? e : typeof e, ""));
      }
  return t = st(l, n, t, o), t.elementType = e, t.type = r, t.lanes = i, t;
}
function $n(e, t, n, r) {
  return e = st(7, e, r, t), e.lanes = n, e;
}
function vl(e, t, n, r) {
  return e = st(22, e, r, t), e.elementType = Kd, e.lanes = n, e.stateNode = { isHidden: !1 }, e;
}
function Os(e, t, n) {
  return e = st(6, e, null, t), e.lanes = n, e;
}
function Ms(e, t, n) {
  return t = st(4, e.children !== null ? e.children : [], e.key, t), t.lanes = n, t.stateNode = { containerInfo: e.containerInfo, pendingChildren: null, implementation: e.implementation }, t;
}
function _g(e, t, n, r, o) {
  this.tag = t, this.containerInfo = e, this.finishedWork = this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.pendingContext = this.context = null, this.callbackPriority = 0, this.eventTimes = fs(0), this.expirationTimes = fs(-1), this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = fs(0), this.identifierPrefix = r, this.onRecoverableError = o, this.mutableSourceEagerHydrationData = null;
}
function ju(e, t, n, r, o, i, l, s, a) {
  return e = new _g(e, t, n, s, a), t === 1 ? (t = 1, i === !0 && (t |= 8)) : t = 0, i = st(3, null, null, t), e.current = i, i.stateNode = e, i.memoizedState = { element: r, isDehydrated: n, cache: null, transitions: null, pendingSuspenseBoundaries: null }, Su(i), e;
}
function Pg(e, t, n) {
  var r = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
  return { $$typeof: Hn, key: r == null ? null : "" + r, children: e, containerInfo: t, implementation: n };
}
function Am(e) {
  if (!e)
    return hn;
  e = e._reactInternals;
  e: {
    if (In(e) !== e || e.tag !== 1)
      throw Error(P(170));
    var t = e;
    do {
      switch (t.tag) {
        case 3:
          t = t.stateNode.context;
          break e;
        case 1:
          if (Ue(t.type)) {
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
    if (Ue(n))
      return Ap(e, n, t);
  }
  return t;
}
function Dm(e, t, n, r, o, i, l, s, a) {
  return e = ju(n, r, !0, e, o, i, l, s, a), e.context = Am(null), n = e.current, r = Ae(), o = dn(n), i = Bt(r, o), i.callback = t ?? null, cn(n, i, o), e.current.lanes = o, Ro(e, o, r), Ve(e, r), e;
}
function Sl(e, t, n, r) {
  var o = t.current, i = Ae(), l = dn(o);
  return n = Am(n), t.context === null ? t.context = n : t.pendingContext = n, t = Bt(i, l), t.payload = { element: e }, r = r === void 0 ? null : r, r !== null && (t.callback = r), e = cn(o, t, l), e !== null && (Ct(e, o, l, i), yi(e, o, l)), l;
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
function $f(e, t) {
  if (e = e.memoizedState, e !== null && e.dehydrated !== null) {
    var n = e.retryLane;
    e.retryLane = n !== 0 && n < t ? n : t;
  }
}
function Au(e, t) {
  $f(e, t), (e = e.alternate) && $f(e, t);
}
function Tg() {
  return null;
}
var Fm = typeof reportError == "function" ? reportError : function(e) {
  console.error(e);
};
function Du(e) {
  this._internalRoot = e;
}
xl.prototype.render = Du.prototype.render = function(e) {
  var t = this._internalRoot;
  if (t === null)
    throw Error(P(409));
  Sl(e, t, null, null);
};
xl.prototype.unmount = Du.prototype.unmount = function() {
  var e = this._internalRoot;
  if (e !== null) {
    this._internalRoot = null;
    var t = e.containerInfo;
    zn(function() {
      Sl(null, e, null, null);
    }), t[Ut] = null;
  }
};
function xl(e) {
  this._internalRoot = e;
}
xl.prototype.unstable_scheduleHydration = function(e) {
  if (e) {
    var t = yp();
    e = { blockedOn: null, target: e, priority: t };
    for (var n = 0; n < tn.length && t !== 0 && t < tn[n].priority; n++)
      ;
    tn.splice(n, 0, e), n === 0 && vp(e);
  }
};
function Fu(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11);
}
function wl(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11 && (e.nodeType !== 8 || e.nodeValue !== " react-mount-point-unstable "));
}
function Rf() {
}
function $g(e, t, n, r, o) {
  if (o) {
    if (typeof r == "function") {
      var i = r;
      r = function() {
        var u = Zi(l);
        i.call(u);
      };
    }
    var l = Dm(t, r, e, 0, null, !1, !1, "", Rf);
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
  var a = ju(e, 0, !1, null, null, !1, !1, "", Rf);
  return e._reactRootContainer = a, e[Ut] = a.current, fo(e.nodeType === 8 ? e.parentNode : e), zn(function() {
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
        var a = Zi(l);
        s.call(a);
      };
    }
    Sl(t, l, e, o);
  } else
    l = $g(n, t, e, o, r);
  return Zi(l);
}
mp = function(e) {
  switch (e.tag) {
    case 3:
      var t = e.stateNode;
      if (t.current.memoizedState.isDehydrated) {
        var n = Ur(t.pendingLanes);
        n !== 0 && (ou(t, n | 1), Ve(t, fe()), !(B & 6) && (gr = fe() + 500, vn()));
      }
      break;
    case 13:
      zn(function() {
        var r = Vt(e, 1);
        if (r !== null) {
          var o = Ae();
          Ct(r, e, 1, o);
        }
      }), Au(e, 1);
  }
};
iu = function(e) {
  if (e.tag === 13) {
    var t = Vt(e, 134217728);
    if (t !== null) {
      var n = Ae();
      Ct(t, e, 134217728, n);
    }
    Au(e, 134217728);
  }
};
hp = function(e) {
  if (e.tag === 13) {
    var t = dn(e), n = Vt(e, t);
    if (n !== null) {
      var r = Ae();
      Ct(n, e, t, r);
    }
    Au(e, t);
  }
};
yp = function() {
  return K;
};
gp = function(e, t) {
  var n = K;
  try {
    return K = e, t();
  } finally {
    K = n;
  }
};
na = function(e, t, n) {
  switch (t) {
    case "input":
      if (Ys(e, n), t = n.name, n.type === "radio" && t != null) {
        for (n = e; n.parentNode; )
          n = n.parentNode;
        for (n = n.querySelectorAll("input[name=" + JSON.stringify("" + t) + '][type="radio"]'), t = 0; t < n.length; t++) {
          var r = n[t];
          if (r !== e && r.form === e.form) {
            var o = dl(r);
            if (!o)
              throw Error(P(90));
            Qd(r), Ys(r, o);
          }
        }
      }
      break;
    case "textarea":
      Xd(e, n);
      break;
    case "select":
      t = n.value, t != null && rr(e, !!n.multiple, t, !1);
  }
};
rp = Nu;
op = zn;
var Rg = { usingClientEntryPoint: !1, Events: [Mo, Xn, dl, tp, np, Nu] }, Dr = { findFiberByHostInstance: Cn, bundleType: 0, version: "18.3.1", rendererPackageName: "react-dom" }, Og = { bundleType: Dr.bundleType, version: Dr.version, rendererPackageName: Dr.rendererPackageName, rendererConfig: Dr.rendererConfig, overrideHookState: null, overrideHookStateDeletePath: null, overrideHookStateRenamePath: null, overrideProps: null, overridePropsDeletePath: null, overridePropsRenamePath: null, setErrorHandler: null, setSuspenseHandler: null, scheduleUpdate: null, currentDispatcherRef: Qt.ReactCurrentDispatcher, findHostInstanceByFiber: function(e) {
  return e = sp(e), e === null ? null : e.stateNode;
}, findFiberByHostInstance: Dr.findFiberByHostInstance || Tg, findHostInstancesForRefresh: null, scheduleRefresh: null, scheduleRoot: null, setRefreshHandler: null, getCurrentFiber: null, reconcilerVersion: "18.3.1-next-f1338f8080-20240426" };
if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u") {
  var li = __REACT_DEVTOOLS_GLOBAL_HOOK__;
  if (!li.isDisabled && li.supportsFiber)
    try {
      al = li.inject(Og), Nt = li;
    } catch {
    }
}
Ze.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = Rg;
Ze.createPortal = function(e, t) {
  var n = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
  if (!Fu(t))
    throw Error(P(200));
  return Pg(e, t, null, n);
};
Ze.createRoot = function(e, t) {
  if (!Fu(e))
    throw Error(P(299));
  var n = !1, r = "", o = Fm;
  return t != null && (t.unstable_strictMode === !0 && (n = !0), t.identifierPrefix !== void 0 && (r = t.identifierPrefix), t.onRecoverableError !== void 0 && (o = t.onRecoverableError)), t = ju(e, 1, !1, null, null, n, !1, r, o), e[Ut] = t.current, fo(e.nodeType === 8 ? e.parentNode : e), new Du(t);
};
Ze.findDOMNode = function(e) {
  if (e == null)
    return null;
  if (e.nodeType === 1)
    return e;
  var t = e._reactInternals;
  if (t === void 0)
    throw typeof e.render == "function" ? Error(P(188)) : (e = Object.keys(e).join(","), Error(P(268, e)));
  return e = sp(t), e = e === null ? null : e.stateNode, e;
};
Ze.flushSync = function(e) {
  return zn(e);
};
Ze.hydrate = function(e, t, n) {
  if (!wl(t))
    throw Error(P(200));
  return kl(null, e, t, !0, n);
};
Ze.hydrateRoot = function(e, t, n) {
  if (!Fu(e))
    throw Error(P(405));
  var r = n != null && n.hydratedSources || null, o = !1, i = "", l = Fm;
  if (n != null && (n.unstable_strictMode === !0 && (o = !0), n.identifierPrefix !== void 0 && (i = n.identifierPrefix), n.onRecoverableError !== void 0 && (l = n.onRecoverableError)), t = Dm(t, null, e, 1, n ?? null, o, !1, i, l), e[Ut] = t.current, fo(e), r)
    for (e = 0; e < r.length; e++)
      n = r[e], o = n._getVersion, o = o(n._source), t.mutableSourceEagerHydrationData == null ? t.mutableSourceEagerHydrationData = [n, o] : t.mutableSourceEagerHydrationData.push(
        n,
        o
      );
  return new xl(t);
};
Ze.render = function(e, t, n) {
  if (!wl(t))
    throw Error(P(200));
  return kl(null, e, t, !1, n);
};
Ze.unmountComponentAtNode = function(e) {
  if (!wl(e))
    throw Error(P(40));
  return e._reactRootContainer ? (zn(function() {
    kl(null, null, e, !1, function() {
      e._reactRootContainer = null, e[Ut] = null;
    });
  }), !0) : !1;
};
Ze.unstable_batchedUpdates = Nu;
Ze.unstable_renderSubtreeIntoContainer = function(e, t, n, r) {
  if (!wl(n))
    throw Error(P(200));
  if (e == null || e._reactInternals === void 0)
    throw Error(P(38));
  return kl(e, t, n, !1, r);
};
Ze.version = "18.3.1-next-f1338f8080-20240426";
function bm() {
  if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function"))
    try {
      __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(bm);
    } catch (e) {
      console.error(e);
    }
}
bm(), bd.exports = Ze;
var Bm = bd.exports;
const si = /* @__PURE__ */ $d(Bm);
var Of = Bm;
Ws.createRoot = Of.createRoot, Ws.hydrateRoot = Of.hydrateRoot;
function wo(e) {
  let t = "https://mui.com/production-error/?code=" + e;
  for (let n = 1; n < arguments.length; n += 1)
    t += "&args[]=" + encodeURIComponent(arguments[n]);
  return "Minified MUI error #" + e + "; visit " + t + " for the full message.";
}
const Mg = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: wo
}, Symbol.toStringTag, { value: "Module" })), vr = "$$material";
function k() {
  return k = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t];
      for (var r in n)
        ({}).hasOwnProperty.call(n, r) && (e[r] = n[r]);
    }
    return e;
  }, k.apply(null, arguments);
}
function H(e, t) {
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
var Ng = !1;
function zg(e) {
  if (e.sheet)
    return e.sheet;
  for (var t = 0; t < document.styleSheets.length; t++)
    if (document.styleSheets[t].ownerNode === e)
      return document.styleSheets[t];
}
function Lg(e) {
  var t = document.createElement("style");
  return t.setAttribute("data-emotion", e.key), e.nonce !== void 0 && t.setAttribute("nonce", e.nonce), t.appendChild(document.createTextNode("")), t.setAttribute("data-s", ""), t;
}
var Ig = /* @__PURE__ */ function() {
  function e(n) {
    var r = this;
    this._insertTag = function(o) {
      var i;
      r.tags.length === 0 ? r.insertionPoint ? i = r.insertionPoint.nextSibling : r.prepend ? i = r.container.firstChild : i = r.before : i = r.tags[r.tags.length - 1].nextSibling, r.container.insertBefore(o, i), r.tags.push(o);
    }, this.isSpeedy = n.speedy === void 0 ? !Ng : n.speedy, this.tags = [], this.ctr = 0, this.nonce = n.nonce, this.key = n.key, this.container = n.container, this.prepend = n.prepend, this.insertionPoint = n.insertionPoint, this.before = null;
  }
  var t = e.prototype;
  return t.hydrate = function(r) {
    r.forEach(this._insertTag);
  }, t.insert = function(r) {
    this.ctr % (this.isSpeedy ? 65e3 : 1) === 0 && this._insertTag(Lg(this));
    var o = this.tags[this.tags.length - 1];
    if (this.isSpeedy) {
      var i = zg(o);
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
}(), Ne = "-ms-", Ji = "-moz-", U = "-webkit-", Wm = "comm", bu = "rule", Bu = "decl", jg = "@import", Um = "@keyframes", Ag = "@layer", Dg = Math.abs, Cl = String.fromCharCode, Fg = Object.assign;
function bg(e, t) {
  return Te(e, 0) ^ 45 ? (((t << 2 ^ Te(e, 0)) << 2 ^ Te(e, 1)) << 2 ^ Te(e, 2)) << 2 ^ Te(e, 3) : 0;
}
function Vm(e) {
  return e.trim();
}
function Bg(e, t) {
  return (e = t.exec(e)) ? e[0] : e;
}
function V(e, t, n) {
  return e.replace(t, n);
}
function Ia(e, t) {
  return e.indexOf(t);
}
function Te(e, t) {
  return e.charCodeAt(t) | 0;
}
function ko(e, t, n) {
  return e.slice(t, n);
}
function Rt(e) {
  return e.length;
}
function Wu(e) {
  return e.length;
}
function ai(e, t) {
  return t.push(e), e;
}
function Wg(e, t) {
  return e.map(t).join("");
}
var El = 1, Sr = 1, Hm = 0, He = 0, ye = 0, Er = "";
function _l(e, t, n, r, o, i, l) {
  return { value: e, root: t, parent: n, type: r, props: o, children: i, line: El, column: Sr, length: l, return: "" };
}
function Fr(e, t) {
  return Fg(_l("", null, null, "", null, null, 0), e, { length: -e.length }, t);
}
function Ug() {
  return ye;
}
function Vg() {
  return ye = He > 0 ? Te(Er, --He) : 0, Sr--, ye === 10 && (Sr = 1, El--), ye;
}
function Xe() {
  return ye = He < Hm ? Te(Er, He++) : 0, Sr++, ye === 10 && (Sr = 1, El++), ye;
}
function Lt() {
  return Te(Er, He);
}
function Ci() {
  return He;
}
function zo(e, t) {
  return ko(Er, e, t);
}
function Co(e) {
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
function Km(e) {
  return El = Sr = 1, Hm = Rt(Er = e), He = 0, [];
}
function Gm(e) {
  return Er = "", e;
}
function Ei(e) {
  return Vm(zo(He - 1, ja(e === 91 ? e + 2 : e === 40 ? e + 1 : e)));
}
function Hg(e) {
  for (; (ye = Lt()) && ye < 33; )
    Xe();
  return Co(e) > 2 || Co(ye) > 3 ? "" : " ";
}
function Kg(e, t) {
  for (; --t && Xe() && !(ye < 48 || ye > 102 || ye > 57 && ye < 65 || ye > 70 && ye < 97); )
    ;
  return zo(e, Ci() + (t < 6 && Lt() == 32 && Xe() == 32));
}
function ja(e) {
  for (; Xe(); )
    switch (ye) {
      case e:
        return He;
      case 34:
      case 39:
        e !== 34 && e !== 39 && ja(ye);
        break;
      case 40:
        e === 41 && ja(e);
        break;
      case 92:
        Xe();
        break;
    }
  return He;
}
function Gg(e, t) {
  for (; Xe() && e + ye !== 47 + 10; )
    if (e + ye === 42 + 42 && Lt() === 47)
      break;
  return "/*" + zo(t, He - 1) + "*" + Cl(e === 47 ? e : Xe());
}
function Qg(e) {
  for (; !Co(Lt()); )
    Xe();
  return zo(e, He);
}
function Yg(e) {
  return Gm(_i("", null, null, null, [""], e = Km(e), 0, [0], e));
}
function _i(e, t, n, r, o, i, l, s, a) {
  for (var u = 0, d = 0, f = l, m = 0, v = 0, g = 0, y = 1, _ = 1, p = 1, c = 0, h = "", S = o, E = i, w = r, x = h; _; )
    switch (g = c, c = Xe()) {
      case 40:
        if (g != 108 && Te(x, f - 1) == 58) {
          Ia(x += V(Ei(c), "&", "&\f"), "&\f") != -1 && (p = -1);
          break;
        }
      case 34:
      case 39:
      case 91:
        x += Ei(c);
        break;
      case 9:
      case 10:
      case 13:
      case 32:
        x += Hg(g);
        break;
      case 92:
        x += Kg(Ci() - 1, 7);
        continue;
      case 47:
        switch (Lt()) {
          case 42:
          case 47:
            ai(Xg(Gg(Xe(), Ci()), t, n), a);
            break;
          default:
            x += "/";
        }
        break;
      case 123 * y:
        s[u++] = Rt(x) * p;
      case 125 * y:
      case 59:
      case 0:
        switch (c) {
          case 0:
          case 125:
            _ = 0;
          case 59 + d:
            p == -1 && (x = V(x, /\f/g, "")), v > 0 && Rt(x) - f && ai(v > 32 ? Nf(x + ";", r, n, f - 1) : Nf(V(x, " ", "") + ";", r, n, f - 2), a);
            break;
          case 59:
            x += ";";
          default:
            if (ai(w = Mf(x, t, n, u, d, o, s, h, S = [], E = [], f), i), c === 123)
              if (d === 0)
                _i(x, t, w, w, S, i, f, s, E);
              else
                switch (m === 99 && Te(x, 3) === 110 ? 100 : m) {
                  case 100:
                  case 108:
                  case 109:
                  case 115:
                    _i(e, w, w, r && ai(Mf(e, w, w, 0, 0, o, s, h, o, S = [], f), E), o, E, f, s, r ? S : E);
                    break;
                  default:
                    _i(x, w, w, w, [""], E, 0, s, E);
                }
        }
        u = d = v = 0, y = p = 1, h = x = "", f = l;
        break;
      case 58:
        f = 1 + Rt(x), v = g;
      default:
        if (y < 1) {
          if (c == 123)
            --y;
          else if (c == 125 && y++ == 0 && Vg() == 125)
            continue;
        }
        switch (x += Cl(c), c * y) {
          case 38:
            p = d > 0 ? 1 : (x += "\f", -1);
            break;
          case 44:
            s[u++] = (Rt(x) - 1) * p, p = 1;
            break;
          case 64:
            Lt() === 45 && (x += Ei(Xe())), m = Lt(), d = f = Rt(h = x += Qg(Ci())), c++;
            break;
          case 45:
            g === 45 && Rt(x) == 2 && (y = 0);
        }
    }
  return i;
}
function Mf(e, t, n, r, o, i, l, s, a, u, d) {
  for (var f = o - 1, m = o === 0 ? i : [""], v = Wu(m), g = 0, y = 0, _ = 0; g < r; ++g)
    for (var p = 0, c = ko(e, f + 1, f = Dg(y = l[g])), h = e; p < v; ++p)
      (h = Vm(y > 0 ? m[p] + " " + c : V(c, /&\f/g, m[p]))) && (a[_++] = h);
  return _l(e, t, n, o === 0 ? bu : s, a, u, d);
}
function Xg(e, t, n) {
  return _l(e, t, n, Wm, Cl(Ug()), ko(e, 2, -2), 0);
}
function Nf(e, t, n, r) {
  return _l(e, t, n, Bu, ko(e, 0, r), ko(e, r + 1, -1), r);
}
function ur(e, t) {
  for (var n = "", r = Wu(e), o = 0; o < r; o++)
    n += t(e[o], o, e, t) || "";
  return n;
}
function qg(e, t, n, r) {
  switch (e.type) {
    case Ag:
      if (e.children.length)
        break;
    case jg:
    case Bu:
      return e.return = e.return || e.value;
    case Wm:
      return "";
    case Um:
      return e.return = e.value + "{" + ur(e.children, r) + "}";
    case bu:
      e.value = e.props.join(",");
  }
  return Rt(n = ur(e.children, r)) ? e.return = e.value + "{" + n + "}" : "";
}
function Zg(e) {
  var t = Wu(e);
  return function(n, r, o, i) {
    for (var l = "", s = 0; s < t; s++)
      l += e[s](n, r, o, i) || "";
    return l;
  };
}
function Jg(e) {
  return function(t) {
    t.root || (t = t.return) && e(t);
  };
}
function Qm(e) {
  var t = /* @__PURE__ */ Object.create(null);
  return function(n) {
    return t[n] === void 0 && (t[n] = e(n)), t[n];
  };
}
var ev = function(t, n, r) {
  for (var o = 0, i = 0; o = i, i = Lt(), o === 38 && i === 12 && (n[r] = 1), !Co(i); )
    Xe();
  return zo(t, He);
}, tv = function(t, n) {
  var r = -1, o = 44;
  do
    switch (Co(o)) {
      case 0:
        o === 38 && Lt() === 12 && (n[r] = 1), t[r] += ev(He - 1, n, r);
        break;
      case 2:
        t[r] += Ei(o);
        break;
      case 4:
        if (o === 44) {
          t[++r] = Lt() === 58 ? "&\f" : "", n[r] = t[r].length;
          break;
        }
      default:
        t[r] += Cl(o);
    }
  while (o = Xe());
  return t;
}, nv = function(t, n) {
  return Gm(tv(Km(t), n));
}, zf = /* @__PURE__ */ new WeakMap(), rv = function(t) {
  if (!(t.type !== "rule" || !t.parent || // positive .length indicates that this rule contains pseudo
  // negative .length indicates that this rule has been already prefixed
  t.length < 1)) {
    for (var n = t.value, r = t.parent, o = t.column === r.column && t.line === r.line; r.type !== "rule"; )
      if (r = r.parent, !r)
        return;
    if (!(t.props.length === 1 && n.charCodeAt(0) !== 58 && !zf.get(r)) && !o) {
      zf.set(t, !0);
      for (var i = [], l = nv(n, i), s = r.props, a = 0, u = 0; a < l.length; a++)
        for (var d = 0; d < s.length; d++, u++)
          t.props[u] = i[a] ? l[a].replace(/&\f/g, s[d]) : s[d] + " " + l[a];
    }
  }
}, ov = function(t) {
  if (t.type === "decl") {
    var n = t.value;
    // charcode for l
    n.charCodeAt(0) === 108 && // charcode for b
    n.charCodeAt(2) === 98 && (t.return = "", t.value = "");
  }
};
function Ym(e, t) {
  switch (bg(e, t)) {
    case 5103:
      return U + "print-" + e + e;
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
      return U + e + e;
    case 5349:
    case 4246:
    case 4810:
    case 6968:
    case 2756:
      return U + e + Ji + e + Ne + e + e;
    case 6828:
    case 4268:
      return U + e + Ne + e + e;
    case 6165:
      return U + e + Ne + "flex-" + e + e;
    case 5187:
      return U + e + V(e, /(\w+).+(:[^]+)/, U + "box-$1$2" + Ne + "flex-$1$2") + e;
    case 5443:
      return U + e + Ne + "flex-item-" + V(e, /flex-|-self/, "") + e;
    case 4675:
      return U + e + Ne + "flex-line-pack" + V(e, /align-content|flex-|-self/, "") + e;
    case 5548:
      return U + e + Ne + V(e, "shrink", "negative") + e;
    case 5292:
      return U + e + Ne + V(e, "basis", "preferred-size") + e;
    case 6060:
      return U + "box-" + V(e, "-grow", "") + U + e + Ne + V(e, "grow", "positive") + e;
    case 4554:
      return U + V(e, /([^-])(transform)/g, "$1" + U + "$2") + e;
    case 6187:
      return V(V(V(e, /(zoom-|grab)/, U + "$1"), /(image-set)/, U + "$1"), e, "") + e;
    case 5495:
    case 3959:
      return V(e, /(image-set\([^]*)/, U + "$1$`$1");
    case 4968:
      return V(V(e, /(.+:)(flex-)?(.*)/, U + "box-pack:$3" + Ne + "flex-pack:$3"), /s.+-b[^;]+/, "justify") + U + e + e;
    case 4095:
    case 3583:
    case 4068:
    case 2532:
      return V(e, /(.+)-inline(.+)/, U + "$1$2") + e;
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
      if (Rt(e) - 1 - t > 6)
        switch (Te(e, t + 1)) {
          case 109:
            if (Te(e, t + 4) !== 45)
              break;
          case 102:
            return V(e, /(.+:)(.+)-([^]+)/, "$1" + U + "$2-$3$1" + Ji + (Te(e, t + 3) == 108 ? "$3" : "$2-$3")) + e;
          case 115:
            return ~Ia(e, "stretch") ? Ym(V(e, "stretch", "fill-available"), t) + e : e;
        }
      break;
    case 4949:
      if (Te(e, t + 1) !== 115)
        break;
    case 6444:
      switch (Te(e, Rt(e) - 3 - (~Ia(e, "!important") && 10))) {
        case 107:
          return V(e, ":", ":" + U) + e;
        case 101:
          return V(e, /(.+:)([^;!]+)(;|!.+)?/, "$1" + U + (Te(e, 14) === 45 ? "inline-" : "") + "box$3$1" + U + "$2$3$1" + Ne + "$2box$3") + e;
      }
      break;
    case 5936:
      switch (Te(e, t + 11)) {
        case 114:
          return U + e + Ne + V(e, /[svh]\w+-[tblr]{2}/, "tb") + e;
        case 108:
          return U + e + Ne + V(e, /[svh]\w+-[tblr]{2}/, "tb-rl") + e;
        case 45:
          return U + e + Ne + V(e, /[svh]\w+-[tblr]{2}/, "lr") + e;
      }
      return U + e + Ne + e + e;
  }
  return e;
}
var iv = function(t, n, r, o) {
  if (t.length > -1 && !t.return)
    switch (t.type) {
      case Bu:
        t.return = Ym(t.value, t.length);
        break;
      case Um:
        return ur([Fr(t, {
          value: V(t.value, "@", "@" + U)
        })], o);
      case bu:
        if (t.length)
          return Wg(t.props, function(i) {
            switch (Bg(i, /(::plac\w+|:read-\w+)/)) {
              case ":read-only":
              case ":read-write":
                return ur([Fr(t, {
                  props: [V(i, /:(read-\w+)/, ":" + Ji + "$1")]
                })], o);
              case "::placeholder":
                return ur([Fr(t, {
                  props: [V(i, /:(plac\w+)/, ":" + U + "input-$1")]
                }), Fr(t, {
                  props: [V(i, /:(plac\w+)/, ":" + Ji + "$1")]
                }), Fr(t, {
                  props: [V(i, /:(plac\w+)/, Ne + "input-$1")]
                })], o);
            }
            return "";
          });
    }
}, lv = [iv], Xm = function(t) {
  var n = t.key;
  if (n === "css") {
    var r = document.querySelectorAll("style[data-emotion]:not([data-s])");
    Array.prototype.forEach.call(r, function(y) {
      var _ = y.getAttribute("data-emotion");
      _.indexOf(" ") !== -1 && (document.head.appendChild(y), y.setAttribute("data-s", ""));
    });
  }
  var o = t.stylisPlugins || lv, i = {}, l, s = [];
  l = t.container || document.head, Array.prototype.forEach.call(
    // this means we will ignore elements which don't have a space in them which
    // means that the style elements we're looking at are only Emotion 11 server-rendered style elements
    document.querySelectorAll('style[data-emotion^="' + n + ' "]'),
    function(y) {
      for (var _ = y.getAttribute("data-emotion").split(" "), p = 1; p < _.length; p++)
        i[_[p]] = !0;
      s.push(y);
    }
  );
  var a, u = [rv, ov];
  {
    var d, f = [qg, Jg(function(y) {
      d.insert(y);
    })], m = Zg(u.concat(o, f)), v = function(_) {
      return ur(Yg(_), m);
    };
    a = function(_, p, c, h) {
      d = c, v(_ ? _ + "{" + p.styles + "}" : p.styles), h && (g.inserted[p.name] = !0);
    };
  }
  var g = {
    key: n,
    sheet: new Ig({
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
  return g.sheet.hydrate(s), g;
}, qm = { exports: {} }, G = {};
/** @license React v16.13.1
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ee = typeof Symbol == "function" && Symbol.for, Uu = Ee ? Symbol.for("react.element") : 60103, Vu = Ee ? Symbol.for("react.portal") : 60106, Pl = Ee ? Symbol.for("react.fragment") : 60107, Tl = Ee ? Symbol.for("react.strict_mode") : 60108, $l = Ee ? Symbol.for("react.profiler") : 60114, Rl = Ee ? Symbol.for("react.provider") : 60109, Ol = Ee ? Symbol.for("react.context") : 60110, Hu = Ee ? Symbol.for("react.async_mode") : 60111, Ml = Ee ? Symbol.for("react.concurrent_mode") : 60111, Nl = Ee ? Symbol.for("react.forward_ref") : 60112, zl = Ee ? Symbol.for("react.suspense") : 60113, sv = Ee ? Symbol.for("react.suspense_list") : 60120, Ll = Ee ? Symbol.for("react.memo") : 60115, Il = Ee ? Symbol.for("react.lazy") : 60116, av = Ee ? Symbol.for("react.block") : 60121, uv = Ee ? Symbol.for("react.fundamental") : 60117, cv = Ee ? Symbol.for("react.responder") : 60118, fv = Ee ? Symbol.for("react.scope") : 60119;
function et(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Uu:
        switch (e = e.type, e) {
          case Hu:
          case Ml:
          case Pl:
          case $l:
          case Tl:
          case zl:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Ol:
              case Nl:
              case Il:
              case Ll:
              case Rl:
                return e;
              default:
                return t;
            }
        }
      case Vu:
        return t;
    }
  }
}
function Zm(e) {
  return et(e) === Ml;
}
G.AsyncMode = Hu;
G.ConcurrentMode = Ml;
G.ContextConsumer = Ol;
G.ContextProvider = Rl;
G.Element = Uu;
G.ForwardRef = Nl;
G.Fragment = Pl;
G.Lazy = Il;
G.Memo = Ll;
G.Portal = Vu;
G.Profiler = $l;
G.StrictMode = Tl;
G.Suspense = zl;
G.isAsyncMode = function(e) {
  return Zm(e) || et(e) === Hu;
};
G.isConcurrentMode = Zm;
G.isContextConsumer = function(e) {
  return et(e) === Ol;
};
G.isContextProvider = function(e) {
  return et(e) === Rl;
};
G.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Uu;
};
G.isForwardRef = function(e) {
  return et(e) === Nl;
};
G.isFragment = function(e) {
  return et(e) === Pl;
};
G.isLazy = function(e) {
  return et(e) === Il;
};
G.isMemo = function(e) {
  return et(e) === Ll;
};
G.isPortal = function(e) {
  return et(e) === Vu;
};
G.isProfiler = function(e) {
  return et(e) === $l;
};
G.isStrictMode = function(e) {
  return et(e) === Tl;
};
G.isSuspense = function(e) {
  return et(e) === zl;
};
G.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === Pl || e === Ml || e === $l || e === Tl || e === zl || e === sv || typeof e == "object" && e !== null && (e.$$typeof === Il || e.$$typeof === Ll || e.$$typeof === Rl || e.$$typeof === Ol || e.$$typeof === Nl || e.$$typeof === uv || e.$$typeof === cv || e.$$typeof === fv || e.$$typeof === av);
};
G.typeOf = et;
qm.exports = G;
var dv = qm.exports, Jm = dv, pv = {
  $$typeof: !0,
  render: !0,
  defaultProps: !0,
  displayName: !0,
  propTypes: !0
}, mv = {
  $$typeof: !0,
  compare: !0,
  defaultProps: !0,
  displayName: !0,
  propTypes: !0,
  type: !0
}, eh = {};
eh[Jm.ForwardRef] = pv;
eh[Jm.Memo] = mv;
var hv = !0;
function th(e, t, n) {
  var r = "";
  return n.split(" ").forEach(function(o) {
    e[o] !== void 0 ? t.push(e[o] + ";") : o && (r += o + " ");
  }), r;
}
var Ku = function(t, n, r) {
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
  hv === !1) && t.registered[o] === void 0 && (t.registered[o] = n.styles);
}, Gu = function(t, n, r) {
  Ku(t, n, r);
  var o = t.key + "-" + n.name;
  if (t.inserted[n.name] === void 0) {
    var i = n;
    do
      t.insert(n === i ? "." + o : "", i, t.sheet, !0), i = i.next;
    while (i !== void 0);
  }
};
function yv(e) {
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
var gv = {
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
}, vv = !1, Sv = /[A-Z]|^ms/g, xv = /_EMO_([^_]+?)_([^]*?)_EMO_/g, nh = function(t) {
  return t.charCodeAt(1) === 45;
}, Lf = function(t) {
  return t != null && typeof t != "boolean";
}, Ns = /* @__PURE__ */ Qm(function(e) {
  return nh(e) ? e : e.replace(Sv, "-$&").toLowerCase();
}), If = function(t, n) {
  switch (t) {
    case "animation":
    case "animationName":
      if (typeof n == "string")
        return n.replace(xv, function(r, o, i) {
          return Ot = {
            name: o,
            styles: i,
            next: Ot
          }, o;
        });
  }
  return gv[t] !== 1 && !nh(t) && typeof n == "number" && n !== 0 ? n + "px" : n;
}, wv = "Component selectors can only be used in conjunction with @emotion/babel-plugin, the swc Emotion plugin, or another Emotion-aware compiler transform.";
function Eo(e, t, n) {
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
        return Ot = {
          name: o.name,
          styles: o.styles,
          next: Ot
        }, o.name;
      var i = n;
      if (i.styles !== void 0) {
        var l = i.next;
        if (l !== void 0)
          for (; l !== void 0; )
            Ot = {
              name: l.name,
              styles: l.styles,
              next: Ot
            }, l = l.next;
        var s = i.styles + ";";
        return s;
      }
      return kv(e, t, n);
    }
    case "function": {
      if (e !== void 0) {
        var a = Ot, u = n(e);
        return Ot = a, Eo(e, t, u);
      }
      break;
    }
  }
  var d = n;
  if (t == null)
    return d;
  var f = t[d];
  return f !== void 0 ? f : d;
}
function kv(e, t, n) {
  var r = "";
  if (Array.isArray(n))
    for (var o = 0; o < n.length; o++)
      r += Eo(e, t, n[o]) + ";";
  else
    for (var i in n) {
      var l = n[i];
      if (typeof l != "object") {
        var s = l;
        t != null && t[s] !== void 0 ? r += i + "{" + t[s] + "}" : Lf(s) && (r += Ns(i) + ":" + If(i, s) + ";");
      } else {
        if (i === "NO_COMPONENT_SELECTOR" && vv)
          throw new Error(wv);
        if (Array.isArray(l) && typeof l[0] == "string" && (t == null || t[l[0]] === void 0))
          for (var a = 0; a < l.length; a++)
            Lf(l[a]) && (r += Ns(i) + ":" + If(i, l[a]) + ";");
        else {
          var u = Eo(e, t, l);
          switch (i) {
            case "animation":
            case "animationName": {
              r += Ns(i) + ":" + u + ";";
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
var jf = /label:\s*([^\s;{]+)\s*(;|$)/g, Ot;
function Lo(e, t, n) {
  if (e.length === 1 && typeof e[0] == "object" && e[0] !== null && e[0].styles !== void 0)
    return e[0];
  var r = !0, o = "";
  Ot = void 0;
  var i = e[0];
  if (i == null || i.raw === void 0)
    r = !1, o += Eo(n, t, i);
  else {
    var l = i;
    o += l[0];
  }
  for (var s = 1; s < e.length; s++)
    if (o += Eo(n, t, e[s]), r) {
      var a = i;
      o += a[s];
    }
  jf.lastIndex = 0;
  for (var u = "", d; (d = jf.exec(o)) !== null; )
    u += "-" + d[1];
  var f = yv(o) + u;
  return {
    name: f,
    styles: o,
    next: Ot
  };
}
var Cv = function(t) {
  return t();
}, rh = Bs["useInsertionEffect"] ? Bs["useInsertionEffect"] : !1, oh = rh || Cv, Af = rh || C.useLayoutEffect, Ev = !1, ih = /* @__PURE__ */ C.createContext(
  // we're doing this to avoid preconstruct's dead code elimination in this one case
  // because this module is primarily intended for the browser and node
  // but it's also required in react native and similar environments sometimes
  // and we could have a special build just for that
  // but this is much easier and the native packages
  // might use a different theme context in the future anyway
  typeof HTMLElement < "u" ? /* @__PURE__ */ Xm({
    key: "css"
  }) : null
), _v = ih.Provider, Qu = function(t) {
  return /* @__PURE__ */ C.forwardRef(function(n, r) {
    var o = C.useContext(ih);
    return t(n, o, r);
  });
}, _r = /* @__PURE__ */ C.createContext({}), Yu = {}.hasOwnProperty, Aa = "__EMOTION_TYPE_PLEASE_DO_NOT_USE__", Pv = function(t, n) {
  var r = {};
  for (var o in n)
    Yu.call(n, o) && (r[o] = n[o]);
  return r[Aa] = t, r;
}, Tv = function(t) {
  var n = t.cache, r = t.serialized, o = t.isStringTag;
  return Ku(n, r, o), oh(function() {
    return Gu(n, r, o);
  }), null;
}, $v = /* @__PURE__ */ Qu(function(e, t, n) {
  var r = e.css;
  typeof r == "string" && t.registered[r] !== void 0 && (r = t.registered[r]);
  var o = e[Aa], i = [r], l = "";
  typeof e.className == "string" ? l = th(t.registered, i, e.className) : e.className != null && (l = e.className + " ");
  var s = Lo(i, void 0, C.useContext(_r));
  l += t.key + "-" + s.name;
  var a = {};
  for (var u in e)
    Yu.call(e, u) && u !== "css" && u !== Aa && !Ev && (a[u] = e[u]);
  return a.className = l, n && (a.ref = n), /* @__PURE__ */ C.createElement(C.Fragment, null, /* @__PURE__ */ C.createElement(Tv, {
    cache: t,
    serialized: s,
    isStringTag: typeof o == "string"
  }), /* @__PURE__ */ C.createElement(o, a));
}), Rv = $v, zs = { exports: {} }, Df;
function lh() {
  return Df || (Df = 1, function(e) {
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
  }(zs)), zs.exports;
}
lh();
var Ff = function(t, n) {
  var r = arguments;
  if (n == null || !Yu.call(n, "css"))
    return C.createElement.apply(void 0, r);
  var o = r.length, i = new Array(o);
  i[0] = Rv, i[1] = Pv(t, n);
  for (var l = 2; l < o; l++)
    i[l] = r[l];
  return C.createElement.apply(null, i);
};
(function(e) {
  var t;
  t || (t = e.JSX || (e.JSX = {}));
})(Ff || (Ff = {}));
var Ov = /* @__PURE__ */ Qu(function(e, t) {
  var n = e.styles, r = Lo([n], void 0, C.useContext(_r)), o = C.useRef();
  return Af(function() {
    var i = t.key + "-global", l = new t.sheet.constructor({
      key: i,
      nonce: t.sheet.nonce,
      container: t.sheet.container,
      speedy: t.sheet.isSpeedy
    }), s = !1, a = document.querySelector('style[data-emotion="' + i + " " + r.name + '"]');
    return t.sheet.tags.length && (l.before = t.sheet.tags[0]), a !== null && (s = !0, a.setAttribute("data-emotion", i), l.hydrate([a])), o.current = [l, s], function() {
      l.flush();
    };
  }, [t]), Af(function() {
    var i = o.current, l = i[0], s = i[1];
    if (s) {
      i[1] = !1;
      return;
    }
    if (r.next !== void 0 && Gu(t, r.next, !0), l.tags.length) {
      var a = l.tags[l.tags.length - 1].nextElementSibling;
      l.before = a, l.flush();
    }
    t.insert("", r, l, !1);
  }, [t, r.name]), null;
});
function jl() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  return Lo(t);
}
function Pr() {
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
var Mv = /^((children|dangerouslySetInnerHTML|key|ref|autoFocus|defaultValue|defaultChecked|innerHTML|suppressContentEditableWarning|suppressHydrationWarning|valueLink|abbr|accept|acceptCharset|accessKey|action|allow|allowUserMedia|allowPaymentRequest|allowFullScreen|allowTransparency|alt|async|autoComplete|autoPlay|capture|cellPadding|cellSpacing|challenge|charSet|checked|cite|classID|className|cols|colSpan|content|contentEditable|contextMenu|controls|controlsList|coords|crossOrigin|data|dateTime|decoding|default|defer|dir|disabled|disablePictureInPicture|disableRemotePlayback|download|draggable|encType|enterKeyHint|fetchpriority|fetchPriority|form|formAction|formEncType|formMethod|formNoValidate|formTarget|frameBorder|headers|height|hidden|high|href|hrefLang|htmlFor|httpEquiv|id|inputMode|integrity|is|keyParams|keyType|kind|label|lang|list|loading|loop|low|marginHeight|marginWidth|max|maxLength|media|mediaGroup|method|min|minLength|multiple|muted|name|nonce|noValidate|open|optimum|pattern|placeholder|playsInline|popover|popoverTarget|popoverTargetAction|poster|preload|profile|radioGroup|readOnly|referrerPolicy|rel|required|reversed|role|rows|rowSpan|sandbox|scope|scoped|scrolling|seamless|selected|shape|size|sizes|slot|span|spellCheck|src|srcDoc|srcLang|srcSet|start|step|style|summary|tabIndex|target|title|translate|type|useMap|value|width|wmode|wrap|about|datatype|inlist|prefix|property|resource|typeof|vocab|autoCapitalize|autoCorrect|autoSave|color|incremental|fallback|inert|itemProp|itemScope|itemType|itemID|itemRef|on|option|results|security|unselectable|accentHeight|accumulate|additive|alignmentBaseline|allowReorder|alphabetic|amplitude|arabicForm|ascent|attributeName|attributeType|autoReverse|azimuth|baseFrequency|baselineShift|baseProfile|bbox|begin|bias|by|calcMode|capHeight|clip|clipPathUnits|clipPath|clipRule|colorInterpolation|colorInterpolationFilters|colorProfile|colorRendering|contentScriptType|contentStyleType|cursor|cx|cy|d|decelerate|descent|diffuseConstant|direction|display|divisor|dominantBaseline|dur|dx|dy|edgeMode|elevation|enableBackground|end|exponent|externalResourcesRequired|fill|fillOpacity|fillRule|filter|filterRes|filterUnits|floodColor|floodOpacity|focusable|fontFamily|fontSize|fontSizeAdjust|fontStretch|fontStyle|fontVariant|fontWeight|format|from|fr|fx|fy|g1|g2|glyphName|glyphOrientationHorizontal|glyphOrientationVertical|glyphRef|gradientTransform|gradientUnits|hanging|horizAdvX|horizOriginX|ideographic|imageRendering|in|in2|intercept|k|k1|k2|k3|k4|kernelMatrix|kernelUnitLength|kerning|keyPoints|keySplines|keyTimes|lengthAdjust|letterSpacing|lightingColor|limitingConeAngle|local|markerEnd|markerMid|markerStart|markerHeight|markerUnits|markerWidth|mask|maskContentUnits|maskUnits|mathematical|mode|numOctaves|offset|opacity|operator|order|orient|orientation|origin|overflow|overlinePosition|overlineThickness|panose1|paintOrder|pathLength|patternContentUnits|patternTransform|patternUnits|pointerEvents|points|pointsAtX|pointsAtY|pointsAtZ|preserveAlpha|preserveAspectRatio|primitiveUnits|r|radius|refX|refY|renderingIntent|repeatCount|repeatDur|requiredExtensions|requiredFeatures|restart|result|rotate|rx|ry|scale|seed|shapeRendering|slope|spacing|specularConstant|specularExponent|speed|spreadMethod|startOffset|stdDeviation|stemh|stemv|stitchTiles|stopColor|stopOpacity|strikethroughPosition|strikethroughThickness|string|stroke|strokeDasharray|strokeDashoffset|strokeLinecap|strokeLinejoin|strokeMiterlimit|strokeOpacity|strokeWidth|surfaceScale|systemLanguage|tableValues|targetX|targetY|textAnchor|textDecoration|textRendering|textLength|to|transform|u1|u2|underlinePosition|underlineThickness|unicode|unicodeBidi|unicodeRange|unitsPerEm|vAlphabetic|vHanging|vIdeographic|vMathematical|values|vectorEffect|version|vertAdvY|vertOriginX|vertOriginY|viewBox|viewTarget|visibility|widths|wordSpacing|writingMode|x|xHeight|x1|x2|xChannelSelector|xlinkActuate|xlinkArcrole|xlinkHref|xlinkRole|xlinkShow|xlinkTitle|xlinkType|xmlBase|xmlns|xmlnsXlink|xmlLang|xmlSpace|y|y1|y2|yChannelSelector|z|zoomAndPan|for|class|autofocus)|(([Dd][Aa][Tt][Aa]|[Aa][Rr][Ii][Aa]|x)-.*))$/, Nv = /* @__PURE__ */ Qm(
  function(e) {
    return Mv.test(e) || e.charCodeAt(0) === 111 && e.charCodeAt(1) === 110 && e.charCodeAt(2) < 91;
  }
  /* Z+1 */
), zv = !1, Lv = Nv, Iv = function(t) {
  return t !== "theme";
}, bf = function(t) {
  return typeof t == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  t.charCodeAt(0) > 96 ? Lv : Iv;
}, Bf = function(t, n, r) {
  var o;
  if (n) {
    var i = n.shouldForwardProp;
    o = t.__emotion_forwardProp && i ? function(l) {
      return t.__emotion_forwardProp(l) && i(l);
    } : i;
  }
  return typeof o != "function" && r && (o = t.__emotion_forwardProp), o;
}, jv = function(t) {
  var n = t.cache, r = t.serialized, o = t.isStringTag;
  return Ku(n, r, o), oh(function() {
    return Gu(n, r, o);
  }), null;
}, Av = function e(t, n) {
  var r = t.__emotion_real === t, o = r && t.__emotion_base || t, i, l;
  n !== void 0 && (i = n.label, l = n.target);
  var s = Bf(t, n, r), a = s || bf(o), u = !a("as");
  return function() {
    var d = arguments, f = r && t.__emotion_styles !== void 0 ? t.__emotion_styles.slice(0) : [];
    if (i !== void 0 && f.push("label:" + i + ";"), d[0] == null || d[0].raw === void 0)
      f.push.apply(f, d);
    else {
      var m = d[0];
      f.push(m[0]);
      for (var v = d.length, g = 1; g < v; g++)
        f.push(d[g], m[g]);
    }
    var y = Qu(function(_, p, c) {
      var h = u && _.as || o, S = "", E = [], w = _;
      if (_.theme == null) {
        w = {};
        for (var x in _)
          w[x] = _[x];
        w.theme = C.useContext(_r);
      }
      typeof _.className == "string" ? S = th(p.registered, E, _.className) : _.className != null && (S = _.className + " ");
      var $ = Lo(f.concat(E), p.registered, w);
      S += p.key + "-" + $.name, l !== void 0 && (S += " " + l);
      var N = u && s === void 0 ? bf(h) : a, O = {};
      for (var b in _)
        u && b === "as" || N(b) && (O[b] = _[b]);
      return O.className = S, c && (O.ref = c), /* @__PURE__ */ C.createElement(C.Fragment, null, /* @__PURE__ */ C.createElement(jv, {
        cache: p,
        serialized: $,
        isStringTag: typeof h == "string"
      }), /* @__PURE__ */ C.createElement(h, O));
    });
    return y.displayName = i !== void 0 ? i : "Styled(" + (typeof o == "string" ? o : o.displayName || o.name || "Component") + ")", y.defaultProps = t.defaultProps, y.__emotion_real = y, y.__emotion_base = o, y.__emotion_styles = f, y.__emotion_forwardProp = s, Object.defineProperty(y, "toString", {
      value: function() {
        return l === void 0 && zv ? "NO_COMPONENT_SELECTOR" : "." + l;
      }
    }), y.withComponent = function(_, p) {
      var c = e(_, k({}, n, p, {
        shouldForwardProp: Bf(y, p, !0)
      }));
      return c.apply(void 0, f);
    }, y;
  };
}, Dv = [
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
], Da = Av.bind(null);
Dv.forEach(function(e) {
  Da[e] = Da(e);
});
function Fv(e, t) {
  const n = Xm({
    key: "css",
    prepend: e
  });
  if (t) {
    const r = n.insert;
    n.insert = (...o) => (o[1].styles.match(/^@layer\s+[^{]*$/) || (o[1].styles = `@layer mui {${o[1].styles}}`), r(...o));
  }
  return n;
}
const Ls = /* @__PURE__ */ new Map();
function bv(e) {
  const {
    injectFirst: t,
    enableCssLayer: n,
    children: r
  } = e, o = C.useMemo(() => {
    const i = `${t}-${n}`;
    if (typeof document == "object" && Ls.has(i))
      return Ls.get(i);
    const l = Fv(t, n);
    return Ls.set(i, l), l;
  }, [t, n]);
  return t || n ? /* @__PURE__ */ T.jsx(_v, {
    value: o,
    children: r
  }) : r;
}
function Bv(e) {
  return e == null || Object.keys(e).length === 0;
}
function sh(e) {
  const {
    styles: t,
    defaultTheme: n = {}
  } = e, r = typeof t == "function" ? (o) => t(Bv(o) ? n : o) : t;
  return /* @__PURE__ */ T.jsx(Ov, {
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
function Xu(e, t) {
  return Da(e, t);
}
const ah = (e, t) => {
  Array.isArray(e.__emotion_styles) && (e.__emotion_styles = t(e.__emotion_styles));
}, Wf = [];
function el(e) {
  return Wf[0] = e, Lo(Wf);
}
const Wv = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  GlobalStyles: sh,
  StyledEngineProvider: bv,
  ThemeContext: _r,
  css: jl,
  default: Xu,
  internal_processStyles: ah,
  internal_serializeStyles: el,
  keyframes: Pr
}, Symbol.toStringTag, { value: "Module" }));
function Dt(e) {
  if (typeof e != "object" || e === null)
    return !1;
  const t = Object.getPrototypeOf(e);
  return (t === null || t === Object.prototype || Object.getPrototypeOf(t) === null) && !(Symbol.toStringTag in e) && !(Symbol.iterator in e);
}
function uh(e) {
  if (/* @__PURE__ */ C.isValidElement(e) || !Dt(e))
    return e;
  const t = {};
  return Object.keys(e).forEach((n) => {
    t[n] = uh(e[n]);
  }), t;
}
function It(e, t, n = {
  clone: !0
}) {
  const r = n.clone ? k({}, e) : e;
  return Dt(e) && Dt(t) && Object.keys(t).forEach((o) => {
    /* @__PURE__ */ C.isValidElement(t[o]) ? r[o] = t[o] : Dt(t[o]) && // Avoid prototype pollution
    Object.prototype.hasOwnProperty.call(e, o) && Dt(e[o]) ? r[o] = It(e[o], t[o], n) : n.clone ? r[o] = Dt(t[o]) ? uh(t[o]) : t[o] : r[o] = t[o];
  }), r;
}
const Uv = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: It,
  isPlainObject: Dt
}, Symbol.toStringTag, { value: "Module" })), Vv = ["values", "unit", "step"], Hv = (e) => {
  const t = Object.keys(e).map((n) => ({
    key: n,
    val: e[n]
  })) || [];
  return t.sort((n, r) => n.val - r.val), t.reduce((n, r) => k({}, n, {
    [r.key]: r.val
  }), {});
};
function ch(e) {
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
  } = e, o = H(e, Vv), i = Hv(t), l = Object.keys(i);
  function s(m) {
    return `@media (min-width:${typeof t[m] == "number" ? t[m] : m}${n})`;
  }
  function a(m) {
    return `@media (max-width:${(typeof t[m] == "number" ? t[m] : m) - r / 100}${n})`;
  }
  function u(m, v) {
    const g = l.indexOf(v);
    return `@media (min-width:${typeof t[m] == "number" ? t[m] : m}${n}) and (max-width:${(g !== -1 && typeof t[l[g]] == "number" ? t[l[g]] : v) - r / 100}${n})`;
  }
  function d(m) {
    return l.indexOf(m) + 1 < l.length ? u(m, l[l.indexOf(m) + 1]) : s(m);
  }
  function f(m) {
    const v = l.indexOf(m);
    return v === 0 ? s(l[1]) : v === l.length - 1 ? a(l[v]) : u(m, l[l.indexOf(m) + 1]).replace("@media", "@media not all and");
  }
  return k({
    keys: l,
    values: i,
    up: s,
    down: a,
    between: u,
    only: d,
    not: f,
    unit: n
  }, o);
}
const Kv = {
  borderRadius: 4
}, Gv = Kv;
function no(e, t) {
  return t ? It(e, t, {
    clone: !1
    // No need to clone deep, it's way faster.
  }) : e;
}
const qu = {
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
}, Uf = {
  // Sorted ASC by size. That's important.
  // It can't be configured as it's used statically for propTypes.
  keys: ["xs", "sm", "md", "lg", "xl"],
  up: (e) => `@media (min-width:${qu[e]}px)`
};
function Kt(e, t, n) {
  const r = e.theme || {};
  if (Array.isArray(t)) {
    const i = r.breakpoints || Uf;
    return t.reduce((l, s, a) => (l[i.up(i.keys[a])] = n(t[a]), l), {});
  }
  if (typeof t == "object") {
    const i = r.breakpoints || Uf;
    return Object.keys(t).reduce((l, s) => {
      if (Object.keys(i.values || qu).indexOf(s) !== -1) {
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
function Qv(e = {}) {
  var t;
  return ((t = e.keys) == null ? void 0 : t.reduce((r, o) => {
    const i = e.up(o);
    return r[i] = {}, r;
  }, {})) || {};
}
function Vf(e, t) {
  return e.reduce((n, r) => {
    const o = n[r];
    return (!o || Object.keys(o).length === 0) && delete n[r], n;
  }, t);
}
function X(e) {
  if (typeof e != "string")
    throw new Error(wo(7));
  return e.charAt(0).toUpperCase() + e.slice(1);
}
const Yv = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: X
}, Symbol.toStringTag, { value: "Module" }));
function Al(e, t, n = !0) {
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
  return typeof e == "function" ? o = e(n) : Array.isArray(e) ? o = e[n] || r : o = Al(e, n) || r, t && (o = t(o, r, e)), o;
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
    const s = l[t], a = l.theme, u = Al(a, r) || {};
    return Kt(l, s, (f) => {
      let m = tl(u, o, f);
      return f === m && typeof f == "string" && (m = tl(u, o, `${t}${f === "default" ? "" : X(f)}`, f)), n === !1 ? m : {
        [n]: m
      };
    });
  };
  return i.propTypes = {}, i.filterProps = [t], i;
}
function Xv(e) {
  const t = {};
  return (n) => (t[n] === void 0 && (t[n] = e(n)), t[n]);
}
const qv = {
  m: "margin",
  p: "padding"
}, Zv = {
  t: "Top",
  r: "Right",
  b: "Bottom",
  l: "Left",
  x: ["Left", "Right"],
  y: ["Top", "Bottom"]
}, Hf = {
  marginX: "mx",
  marginY: "my",
  paddingX: "px",
  paddingY: "py"
}, Jv = Xv((e) => {
  if (e.length > 2)
    if (Hf[e])
      e = Hf[e];
    else
      return [e];
  const [t, n] = e.split(""), r = qv[t], o = Zv[n] || "";
  return Array.isArray(o) ? o.map((i) => r + i) : [r + o];
}), Zu = ["m", "mt", "mr", "mb", "ml", "mx", "my", "margin", "marginTop", "marginRight", "marginBottom", "marginLeft", "marginX", "marginY", "marginInline", "marginInlineStart", "marginInlineEnd", "marginBlock", "marginBlockStart", "marginBlockEnd"], Ju = ["p", "pt", "pr", "pb", "pl", "px", "py", "padding", "paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "paddingX", "paddingY", "paddingInline", "paddingInlineStart", "paddingInlineEnd", "paddingBlock", "paddingBlockStart", "paddingBlockEnd"];
[...Zu, ...Ju];
function Io(e, t, n, r) {
  var o;
  const i = (o = Al(e, t, !1)) != null ? o : n;
  return typeof i == "number" ? (l) => typeof l == "string" ? l : i * l : Array.isArray(i) ? (l) => typeof l == "string" ? l : i[l] : typeof i == "function" ? i : () => {
  };
}
function fh(e) {
  return Io(e, "spacing", 8);
}
function jo(e, t) {
  if (typeof t == "string" || t == null)
    return t;
  const n = Math.abs(t), r = e(n);
  return t >= 0 ? r : typeof r == "number" ? -r : `-${r}`;
}
function e1(e, t) {
  return (n) => e.reduce((r, o) => (r[o] = jo(t, n), r), {});
}
function t1(e, t, n, r) {
  if (t.indexOf(n) === -1)
    return null;
  const o = Jv(n), i = e1(o, r), l = e[n];
  return Kt(e, l, i);
}
function dh(e, t) {
  const n = fh(e.theme);
  return Object.keys(e).map((r) => t1(e, t, r, n)).reduce(no, {});
}
function ae(e) {
  return dh(e, Zu);
}
ae.propTypes = {};
ae.filterProps = Zu;
function ue(e) {
  return dh(e, Ju);
}
ue.propTypes = {};
ue.filterProps = Ju;
function n1(e = 8) {
  if (e.mui)
    return e;
  const t = fh({
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
function lt(e) {
  return typeof e != "number" ? e : `${e}px solid`;
}
function dt(e, t) {
  return de({
    prop: e,
    themeKey: "borders",
    transform: t
  });
}
const r1 = dt("border", lt), o1 = dt("borderTop", lt), i1 = dt("borderRight", lt), l1 = dt("borderBottom", lt), s1 = dt("borderLeft", lt), a1 = dt("borderColor"), u1 = dt("borderTopColor"), c1 = dt("borderRightColor"), f1 = dt("borderBottomColor"), d1 = dt("borderLeftColor"), p1 = dt("outline", lt), m1 = dt("outlineColor"), Fl = (e) => {
  if (e.borderRadius !== void 0 && e.borderRadius !== null) {
    const t = Io(e.theme, "shape.borderRadius", 4), n = (r) => ({
      borderRadius: jo(t, r)
    });
    return Kt(e, e.borderRadius, n);
  }
  return null;
};
Fl.propTypes = {};
Fl.filterProps = ["borderRadius"];
Dl(r1, o1, i1, l1, s1, a1, u1, c1, f1, d1, Fl, p1, m1);
const bl = (e) => {
  if (e.gap !== void 0 && e.gap !== null) {
    const t = Io(e.theme, "spacing", 8), n = (r) => ({
      gap: jo(t, r)
    });
    return Kt(e, e.gap, n);
  }
  return null;
};
bl.propTypes = {};
bl.filterProps = ["gap"];
const Bl = (e) => {
  if (e.columnGap !== void 0 && e.columnGap !== null) {
    const t = Io(e.theme, "spacing", 8), n = (r) => ({
      columnGap: jo(t, r)
    });
    return Kt(e, e.columnGap, n);
  }
  return null;
};
Bl.propTypes = {};
Bl.filterProps = ["columnGap"];
const Wl = (e) => {
  if (e.rowGap !== void 0 && e.rowGap !== null) {
    const t = Io(e.theme, "spacing", 8), n = (r) => ({
      rowGap: jo(t, r)
    });
    return Kt(e, e.rowGap, n);
  }
  return null;
};
Wl.propTypes = {};
Wl.filterProps = ["rowGap"];
const h1 = de({
  prop: "gridColumn"
}), y1 = de({
  prop: "gridRow"
}), g1 = de({
  prop: "gridAutoFlow"
}), v1 = de({
  prop: "gridAutoColumns"
}), S1 = de({
  prop: "gridAutoRows"
}), x1 = de({
  prop: "gridTemplateColumns"
}), w1 = de({
  prop: "gridTemplateRows"
}), k1 = de({
  prop: "gridTemplateAreas"
}), C1 = de({
  prop: "gridArea"
});
Dl(bl, Bl, Wl, h1, y1, g1, v1, S1, x1, w1, k1, C1);
function cr(e, t) {
  return t === "grey" ? t : e;
}
const E1 = de({
  prop: "color",
  themeKey: "palette",
  transform: cr
}), _1 = de({
  prop: "bgcolor",
  cssProperty: "backgroundColor",
  themeKey: "palette",
  transform: cr
}), P1 = de({
  prop: "backgroundColor",
  themeKey: "palette",
  transform: cr
});
Dl(E1, _1, P1);
function Ge(e) {
  return e <= 1 && e !== 0 ? `${e * 100}%` : e;
}
const T1 = de({
  prop: "width",
  transform: Ge
}), ec = (e) => {
  if (e.maxWidth !== void 0 && e.maxWidth !== null) {
    const t = (n) => {
      var r, o;
      const i = ((r = e.theme) == null || (r = r.breakpoints) == null || (r = r.values) == null ? void 0 : r[n]) || qu[n];
      return i ? ((o = e.theme) == null || (o = o.breakpoints) == null ? void 0 : o.unit) !== "px" ? {
        maxWidth: `${i}${e.theme.breakpoints.unit}`
      } : {
        maxWidth: i
      } : {
        maxWidth: Ge(n)
      };
    };
    return Kt(e, e.maxWidth, t);
  }
  return null;
};
ec.filterProps = ["maxWidth"];
const $1 = de({
  prop: "minWidth",
  transform: Ge
}), R1 = de({
  prop: "height",
  transform: Ge
}), O1 = de({
  prop: "maxHeight",
  transform: Ge
}), M1 = de({
  prop: "minHeight",
  transform: Ge
});
de({
  prop: "size",
  cssProperty: "width",
  transform: Ge
});
de({
  prop: "size",
  cssProperty: "height",
  transform: Ge
});
const N1 = de({
  prop: "boxSizing"
});
Dl(T1, ec, $1, R1, O1, M1, N1);
const z1 = {
  // borders
  border: {
    themeKey: "borders",
    transform: lt
  },
  borderTop: {
    themeKey: "borders",
    transform: lt
  },
  borderRight: {
    themeKey: "borders",
    transform: lt
  },
  borderBottom: {
    themeKey: "borders",
    transform: lt
  },
  borderLeft: {
    themeKey: "borders",
    transform: lt
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
    transform: lt
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
    transform: cr
  },
  bgcolor: {
    themeKey: "palette",
    cssProperty: "backgroundColor",
    transform: cr
  },
  backgroundColor: {
    themeKey: "palette",
    transform: cr
  },
  // spacing
  p: {
    style: ue
  },
  pt: {
    style: ue
  },
  pr: {
    style: ue
  },
  pb: {
    style: ue
  },
  pl: {
    style: ue
  },
  px: {
    style: ue
  },
  py: {
    style: ue
  },
  padding: {
    style: ue
  },
  paddingTop: {
    style: ue
  },
  paddingRight: {
    style: ue
  },
  paddingBottom: {
    style: ue
  },
  paddingLeft: {
    style: ue
  },
  paddingX: {
    style: ue
  },
  paddingY: {
    style: ue
  },
  paddingInline: {
    style: ue
  },
  paddingInlineStart: {
    style: ue
  },
  paddingInlineEnd: {
    style: ue
  },
  paddingBlock: {
    style: ue
  },
  paddingBlockStart: {
    style: ue
  },
  paddingBlockEnd: {
    style: ue
  },
  m: {
    style: ae
  },
  mt: {
    style: ae
  },
  mr: {
    style: ae
  },
  mb: {
    style: ae
  },
  ml: {
    style: ae
  },
  mx: {
    style: ae
  },
  my: {
    style: ae
  },
  margin: {
    style: ae
  },
  marginTop: {
    style: ae
  },
  marginRight: {
    style: ae
  },
  marginBottom: {
    style: ae
  },
  marginLeft: {
    style: ae
  },
  marginX: {
    style: ae
  },
  marginY: {
    style: ae
  },
  marginInline: {
    style: ae
  },
  marginInlineStart: {
    style: ae
  },
  marginInlineEnd: {
    style: ae
  },
  marginBlock: {
    style: ae
  },
  marginBlockStart: {
    style: ae
  },
  marginBlockEnd: {
    style: ae
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
    style: bl
  },
  rowGap: {
    style: Wl
  },
  columnGap: {
    style: Bl
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
    transform: Ge
  },
  maxWidth: {
    style: ec
  },
  minWidth: {
    transform: Ge
  },
  height: {
    transform: Ge
  },
  maxHeight: {
    transform: Ge
  },
  minHeight: {
    transform: Ge
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
}, Ao = z1;
function L1(...e) {
  const t = e.reduce((r, o) => r.concat(Object.keys(o)), []), n = new Set(t);
  return e.every((r) => n.size === Object.keys(r).length);
}
function I1(e, t) {
  return typeof e == "function" ? e(t) : e;
}
function ph() {
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
      transform: d,
      style: f
    } = s;
    if (r == null)
      return null;
    if (u === "typography" && r === "inherit")
      return {
        [n]: r
      };
    const m = Al(o, u) || {};
    return f ? f(l) : Kt(l, r, (g) => {
      let y = tl(m, d, g);
      return g === y && typeof g == "string" && (y = tl(m, d, `${n}${g === "default" ? "" : X(g)}`, g)), a === !1 ? y : {
        [a]: y
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
    const s = (r = i.unstable_sxConfig) != null ? r : Ao;
    function a(u) {
      let d = u;
      if (typeof u == "function")
        d = u(i);
      else if (typeof u != "object")
        return u;
      if (!d)
        return null;
      const f = Qv(i.breakpoints), m = Object.keys(f);
      let v = f;
      return Object.keys(d).forEach((g) => {
        const y = I1(d[g], i);
        if (y != null)
          if (typeof y == "object")
            if (s[g])
              v = no(v, e(g, y, i, s));
            else {
              const _ = Kt({
                theme: i
              }, y, (p) => ({
                [g]: p
              }));
              L1(_, y) ? v[g] = t({
                sx: y,
                theme: i,
                nested: !0
              }) : v = no(v, _);
            }
          else
            v = no(v, e(g, y, i, s));
      }), !l && i.modularCssLayers ? {
        "@layer sx": Vf(m, v)
      } : Vf(m, v);
    }
    return Array.isArray(o) ? o.map(a) : a(o);
  }
  return t;
}
const mh = ph();
mh.filterProps = ["sx"];
const Do = mh;
function hh(e, t) {
  const n = this;
  return n.vars && typeof n.getColorSchemeSelector == "function" ? {
    [n.getColorSchemeSelector(e).replace(/(\[[^\]]+\])/, "*:where($1)")]: t
  } : n.palette.mode === e ? t : {};
}
const j1 = ["breakpoints", "palette", "spacing", "shape"];
function Fo(e = {}, ...t) {
  const {
    breakpoints: n = {},
    palette: r = {},
    spacing: o,
    shape: i = {}
  } = e, l = H(e, j1), s = ch(n), a = n1(o);
  let u = It({
    breakpoints: s,
    direction: "ltr",
    components: {},
    // Inject component definitions.
    palette: k({
      mode: "light"
    }, r),
    spacing: a,
    shape: k({}, Gv, i)
  }, l);
  return u.applyStyles = hh, u = t.reduce((d, f) => It(d, f), u), u.unstable_sxConfig = k({}, Ao, l == null ? void 0 : l.unstable_sxConfig), u.unstable_sx = function(f) {
    return Do({
      sx: f,
      theme: this
    });
  }, u;
}
const A1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Fo,
  private_createBreakpoints: ch,
  unstable_applyStyles: hh
}, Symbol.toStringTag, { value: "Module" }));
function D1(e) {
  return Object.keys(e).length === 0;
}
function tc(e = null) {
  const t = C.useContext(_r);
  return !t || D1(t) ? e : t;
}
const F1 = Fo();
function Ul(e = F1) {
  return tc(e);
}
function Is(e) {
  const t = el(e);
  return e !== t && t.styles ? (t.styles.match(/^@layer\s+[^{]*$/) || (t.styles = `@layer global{${t.styles}}`), t) : e;
}
function yh({
  styles: e,
  themeId: t,
  defaultTheme: n = {}
}) {
  const r = Ul(n), o = t && r[t] || r;
  let i = typeof e == "function" ? e(o) : e;
  return o.modularCssLayers && (Array.isArray(i) ? i = i.map((l) => Is(typeof l == "function" ? l(o) : l)) : i = Is(i)), /* @__PURE__ */ T.jsx(sh, {
    styles: i
  });
}
const b1 = ["sx"], B1 = (e) => {
  var t, n;
  const r = {
    systemProps: {},
    otherProps: {}
  }, o = (t = e == null || (n = e.theme) == null ? void 0 : n.unstable_sxConfig) != null ? t : Ao;
  return Object.keys(e).forEach((i) => {
    o[i] ? r.systemProps[i] = e[i] : r.otherProps[i] = e[i];
  }), r;
};
function nc(e) {
  const {
    sx: t
  } = e, n = H(e, b1), {
    systemProps: r,
    otherProps: o
  } = B1(n);
  let i;
  return Array.isArray(t) ? i = [r, ...t] : typeof t == "function" ? i = (...l) => {
    const s = t(...l);
    return Dt(s) ? k({}, r, s) : r;
  } : i = k({}, r, t), k({}, o, {
    sx: i
  });
}
const W1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Do,
  extendSxProp: nc,
  unstable_createStyleFunctionSx: ph,
  unstable_defaultSxConfig: Ao
}, Symbol.toStringTag, { value: "Module" })), Kf = (e) => e, U1 = () => {
  let e = Kf;
  return {
    configure(t) {
      e = t;
    },
    generate(t) {
      return e(t);
    },
    reset() {
      e = Kf;
    }
  };
}, V1 = U1(), rc = V1;
function gh(e) {
  var t, n, r = "";
  if (typeof e == "string" || typeof e == "number")
    r += e;
  else if (typeof e == "object")
    if (Array.isArray(e)) {
      var o = e.length;
      for (t = 0; t < o; t++)
        e[t] && (n = gh(e[t])) && (r && (r += " "), r += n);
    } else
      for (n in e)
        e[n] && (r && (r += " "), r += n);
  return r;
}
function oe() {
  for (var e, t, n = 0, r = "", o = arguments.length; n < o; n++)
    (e = arguments[n]) && (t = gh(e)) && (r && (r += " "), r += t);
  return r;
}
const H1 = ["className", "component"];
function K1(e = {}) {
  const {
    themeId: t,
    defaultTheme: n,
    defaultClassName: r = "MuiBox-root",
    generateClassName: o
  } = e, i = Xu("div", {
    shouldForwardProp: (s) => s !== "theme" && s !== "sx" && s !== "as"
  })(Do);
  return /* @__PURE__ */ C.forwardRef(function(a, u) {
    const d = Ul(n), f = nc(a), {
      className: m,
      component: v = "div"
    } = f, g = H(f, H1);
    return /* @__PURE__ */ T.jsx(i, k({
      as: v,
      ref: u,
      className: oe(m, o ? o(r) : r),
      theme: t && d[t] || d
    }, g));
  });
}
const G1 = {
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
function pt(e, t, n = "Mui") {
  const r = G1[t];
  return r ? `${n}-${r}` : `${rc.generate(e)}-${t}`;
}
function mt(e, t, n = "Mui") {
  const r = {};
  return t.forEach((o) => {
    r[o] = pt(e, o, n);
  }), r;
}
var vh = { exports: {} }, Q = {};
/**
 * @license React
 * react-is.production.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var oc = Symbol.for("react.transitional.element"), ic = Symbol.for("react.portal"), Vl = Symbol.for("react.fragment"), Hl = Symbol.for("react.strict_mode"), Kl = Symbol.for("react.profiler"), Gl = Symbol.for("react.consumer"), Ql = Symbol.for("react.context"), Yl = Symbol.for("react.forward_ref"), Xl = Symbol.for("react.suspense"), ql = Symbol.for("react.suspense_list"), Zl = Symbol.for("react.memo"), Jl = Symbol.for("react.lazy"), Q1 = Symbol.for("react.view_transition"), Y1 = Symbol.for("react.client.reference");
function ht(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case oc:
        switch (e = e.type, e) {
          case Vl:
          case Kl:
          case Hl:
          case Xl:
          case ql:
          case Q1:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Ql:
              case Yl:
              case Jl:
              case Zl:
                return e;
              case Gl:
                return e;
              default:
                return t;
            }
        }
      case ic:
        return t;
    }
  }
}
Q.ContextConsumer = Gl;
Q.ContextProvider = Ql;
Q.Element = oc;
Q.ForwardRef = Yl;
Q.Fragment = Vl;
Q.Lazy = Jl;
Q.Memo = Zl;
Q.Portal = ic;
Q.Profiler = Kl;
Q.StrictMode = Hl;
Q.Suspense = Xl;
Q.SuspenseList = ql;
Q.isContextConsumer = function(e) {
  return ht(e) === Gl;
};
Q.isContextProvider = function(e) {
  return ht(e) === Ql;
};
Q.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === oc;
};
Q.isForwardRef = function(e) {
  return ht(e) === Yl;
};
Q.isFragment = function(e) {
  return ht(e) === Vl;
};
Q.isLazy = function(e) {
  return ht(e) === Jl;
};
Q.isMemo = function(e) {
  return ht(e) === Zl;
};
Q.isPortal = function(e) {
  return ht(e) === ic;
};
Q.isProfiler = function(e) {
  return ht(e) === Kl;
};
Q.isStrictMode = function(e) {
  return ht(e) === Hl;
};
Q.isSuspense = function(e) {
  return ht(e) === Xl;
};
Q.isSuspenseList = function(e) {
  return ht(e) === ql;
};
Q.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === Vl || e === Kl || e === Hl || e === Xl || e === ql || typeof e == "object" && e !== null && (e.$$typeof === Jl || e.$$typeof === Zl || e.$$typeof === Ql || e.$$typeof === Gl || e.$$typeof === Yl || e.$$typeof === Y1 || e.getModuleId !== void 0);
};
Q.typeOf = ht;
vh.exports = Q;
var Gf = vh.exports;
const X1 = /^\s*function(?:\s|\s*\/\*.*\*\/\s*)+([^(\s/]*)\s*/;
function Sh(e) {
  const t = `${e}`.match(X1);
  return t && t[1] || "";
}
function xh(e, t = "") {
  return e.displayName || e.name || Sh(e) || t;
}
function Qf(e, t, n) {
  const r = xh(t);
  return e.displayName || (r !== "" ? `${n}(${r})` : n);
}
function q1(e) {
  if (e != null) {
    if (typeof e == "string")
      return e;
    if (typeof e == "function")
      return xh(e, "Component");
    if (typeof e == "object")
      switch (e.$$typeof) {
        case Gf.ForwardRef:
          return Qf(e, e.render, "ForwardRef");
        case Gf.Memo:
          return Qf(e, e.type, "memo");
        default:
          return;
      }
  }
}
const Z1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: q1,
  getFunctionName: Sh
}, Symbol.toStringTag, { value: "Module" })), J1 = ["ownerState"], eS = ["variants"], tS = ["name", "slot", "skipVariantsResolver", "skipSx", "overridesResolver"];
function nS(e) {
  return Object.keys(e).length === 0;
}
function rS(e) {
  return typeof e == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  e.charCodeAt(0) > 96;
}
function js(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
function Yf(e, t) {
  return t && e && typeof e == "object" && e.styles && !e.styles.startsWith("@layer") && (e.styles = `@layer ${t}{${String(e.styles)}}`), e;
}
const oS = Fo(), iS = (e) => e && e.charAt(0).toLowerCase() + e.slice(1);
function ui({
  defaultTheme: e,
  theme: t,
  themeId: n
}) {
  return nS(t) ? e : t[n] || t;
}
function lS(e) {
  return e ? (t, n) => n[e] : null;
}
function Pi(e, t, n) {
  let {
    ownerState: r
  } = t, o = H(t, J1);
  const i = typeof e == "function" ? e(k({
    ownerState: r
  }, o)) : e;
  if (Array.isArray(i))
    return i.flatMap((l) => Pi(l, k({
      ownerState: r
    }, o), n));
  if (i && typeof i == "object" && Array.isArray(i.variants)) {
    const {
      variants: l = []
    } = i;
    let a = H(i, eS);
    return l.forEach((u) => {
      let d = !0;
      if (typeof u.props == "function" ? d = u.props(k({
        ownerState: r
      }, o, r)) : Object.keys(u.props).forEach((f) => {
        (r == null ? void 0 : r[f]) !== u.props[f] && o[f] !== u.props[f] && (d = !1);
      }), d) {
        Array.isArray(a) || (a = [a]);
        const f = typeof u.style == "function" ? u.style(k({
          ownerState: r
        }, o, r)) : u.style;
        a.push(n ? Yf(el(f), n) : f);
      }
    }), a;
  }
  return n ? Yf(el(i), n) : i;
}
function sS(e = {}) {
  const {
    themeId: t,
    defaultTheme: n = oS,
    rootShouldForwardProp: r = js,
    slotShouldForwardProp: o = js
  } = e, i = (l) => Do(k({}, l, {
    theme: ui(k({}, l, {
      defaultTheme: n,
      themeId: t
    }))
  }));
  return i.__mui_systemSx = !0, (l, s = {}) => {
    ah(l, (w) => w.filter((x) => !(x != null && x.__mui_systemSx)));
    const {
      name: a,
      slot: u,
      skipVariantsResolver: d,
      skipSx: f,
      // TODO v6: remove `lowercaseFirstLetter()` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      overridesResolver: m = lS(iS(u))
    } = s, v = H(s, tS), g = a && a.startsWith("Mui") || u ? "components" : "custom", y = d !== void 0 ? d : (
      // TODO v6: remove `Root` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      u && u !== "Root" && u !== "root" || !1
    ), _ = f || !1;
    let p, c = js;
    u === "Root" || u === "root" ? c = r : u ? c = o : rS(l) && (c = void 0);
    const h = Xu(l, k({
      shouldForwardProp: c,
      label: p
    }, v)), S = (w) => typeof w == "function" && w.__emotion_real !== w || Dt(w) ? (x) => {
      const $ = ui({
        theme: x.theme,
        defaultTheme: n,
        themeId: t
      });
      return Pi(w, k({}, x, {
        theme: $
      }), $.modularCssLayers ? g : void 0);
    } : w, E = (w, ...x) => {
      let $ = S(w);
      const N = x ? x.map(S) : [];
      a && m && N.push((A) => {
        const L = ui(k({}, A, {
          defaultTheme: n,
          themeId: t
        }));
        if (!L.components || !L.components[a] || !L.components[a].styleOverrides)
          return null;
        const W = L.components[a].styleOverrides, ee = {};
        return Object.entries(W).forEach(([ve, he]) => {
          ee[ve] = Pi(he, k({}, A, {
            theme: L
          }), L.modularCssLayers ? "theme" : void 0);
        }), m(A, ee);
      }), a && !y && N.push((A) => {
        var L;
        const W = ui(k({}, A, {
          defaultTheme: n,
          themeId: t
        })), ee = W == null || (L = W.components) == null || (L = L[a]) == null ? void 0 : L.variants;
        return Pi({
          variants: ee
        }, k({}, A, {
          theme: W
        }), W.modularCssLayers ? "theme" : void 0);
      }), _ || N.push(i);
      const O = N.length - x.length;
      if (Array.isArray(w) && O > 0) {
        const A = new Array(O).fill("");
        $ = [...w, ...A], $.raw = [...w.raw, ...A];
      }
      const b = h($, ...N);
      return l.muiName && (b.muiName = l.muiName), b;
    };
    return h.withConfig && (E.withConfig = h.withConfig), E;
  };
}
const aS = sS(), uS = aS;
function nl(e, t) {
  const n = k({}, t);
  return Object.keys(e).forEach((r) => {
    if (r.toString().match(/^(components|slots)$/))
      n[r] = k({}, e[r], n[r]);
    else if (r.toString().match(/^(componentsProps|slotProps)$/)) {
      const o = e[r] || {}, i = t[r];
      n[r] = {}, !i || !Object.keys(i) ? n[r] = o : !o || !Object.keys(o) ? n[r] = i : (n[r] = k({}, i), Object.keys(o).forEach((l) => {
        n[r][l] = nl(o[l], i[l]);
      }));
    } else
      n[r] === void 0 && (n[r] = e[r]);
  }), n;
}
function cS(e) {
  const {
    theme: t,
    name: n,
    props: r
  } = e;
  return !t || !t.components || !t.components[n] || !t.components[n].defaultProps ? r : nl(t.components[n].defaultProps, r);
}
function fS({
  props: e,
  name: t,
  defaultTheme: n,
  themeId: r
}) {
  let o = Ul(n);
  return r && (o = o[r] || o), cS({
    theme: o,
    name: t,
    props: e
  });
}
const dS = typeof window < "u" ? C.useLayoutEffect : C.useEffect, lc = dS;
function pS(e, t = Number.MIN_SAFE_INTEGER, n = Number.MAX_SAFE_INTEGER) {
  return Math.max(t, Math.min(e, n));
}
const mS = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: pS
}, Symbol.toStringTag, { value: "Module" }));
function hS(...e) {
  return e.reduce((t, n) => n == null ? t : function(...o) {
    t.apply(this, o), n.apply(this, o);
  }, () => {
  });
}
function yS(e, t = 166) {
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
function gS(e, t) {
  return () => null;
}
function vS(e, t) {
  var n, r;
  return /* @__PURE__ */ C.isValidElement(e) && t.indexOf(
    // For server components `muiName` is avaialble in element.type._payload.value.muiName
    // relevant info - https://github.com/facebook/react/blob/2807d781a08db8e9873687fccc25c0f12b4fb3d4/packages/react/src/ReactLazy.js#L45
    // eslint-disable-next-line no-underscore-dangle
    (n = e.type.muiName) != null ? n : (r = e.type) == null || (r = r._payload) == null || (r = r.value) == null ? void 0 : r.muiName
  ) !== -1;
}
function wh(e) {
  return e && e.ownerDocument || document;
}
function SS(e) {
  return wh(e).defaultView || window;
}
function xS(e, t) {
  return () => null;
}
function kh(e, t) {
  typeof e == "function" ? e(t) : e && (e.current = t);
}
let Xf = 0;
function wS(e) {
  const [t, n] = C.useState(e), r = e || t;
  return C.useEffect(() => {
    t == null && (Xf += 1, n(`mui-${Xf}`));
  }, [t]), r;
}
const qf = Bs["useId".toString()];
function Ch(e) {
  if (qf !== void 0) {
    const t = qf();
    return e ?? t;
  }
  return wS(e);
}
function kS(e, t, n, r, o) {
  return null;
}
function CS({
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
function Hr(e) {
  const t = C.useRef(e);
  return lc(() => {
    t.current = e;
  }), C.useRef((...n) => (
    // @ts-expect-error hide `this`
    (0, t.current)(...n)
  )).current;
}
function _o(...e) {
  return C.useMemo(() => e.every((t) => t == null) ? null : (t) => {
    e.forEach((n) => {
      kh(n, t);
    });
  }, e);
}
const Zf = {};
function ES(e, t) {
  const n = C.useRef(Zf);
  return n.current === Zf && (n.current = e(t)), n;
}
const _S = [];
function PS(e) {
  C.useEffect(e, _S);
}
class es {
  constructor() {
    this.currentId = null, this.clear = () => {
      this.currentId !== null && (clearTimeout(this.currentId), this.currentId = null);
    }, this.disposeEffect = () => this.clear;
  }
  static create() {
    return new es();
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
function Eh() {
  const e = ES(es.create).current;
  return PS(e.disposeEffect), e;
}
let ts = !0, Fa = !1;
const TS = new es(), $S = {
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
function RS(e) {
  const {
    type: t,
    tagName: n
  } = e;
  return !!(n === "INPUT" && $S[t] && !e.readOnly || n === "TEXTAREA" && !e.readOnly || e.isContentEditable);
}
function OS(e) {
  e.metaKey || e.altKey || e.ctrlKey || (ts = !0);
}
function As() {
  ts = !1;
}
function MS() {
  this.visibilityState === "hidden" && Fa && (ts = !0);
}
function NS(e) {
  e.addEventListener("keydown", OS, !0), e.addEventListener("mousedown", As, !0), e.addEventListener("pointerdown", As, !0), e.addEventListener("touchstart", As, !0), e.addEventListener("visibilitychange", MS, !0);
}
function zS(e) {
  const {
    target: t
  } = e;
  try {
    return t.matches(":focus-visible");
  } catch {
  }
  return ts || RS(t);
}
function _h() {
  const e = C.useCallback((o) => {
    o != null && NS(o.ownerDocument);
  }, []), t = C.useRef(!1);
  function n() {
    return t.current ? (Fa = !0, TS.start(100, () => {
      Fa = !1;
    }), t.current = !1, !0) : !1;
  }
  function r(o) {
    return zS(o) ? (t.current = !0, !0) : !1;
  }
  return {
    isFocusVisibleRef: t,
    onFocus: r,
    onBlur: n,
    ref: e
  };
}
function _t(e, t, n = void 0) {
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
function LS(e) {
  return typeof e == "string";
}
function IS(e, t, n) {
  return e === void 0 || LS(e) ? t : k({}, t, {
    ownerState: k({}, t.ownerState, n)
  });
}
function jS(e, t = []) {
  if (e === void 0)
    return {};
  const n = {};
  return Object.keys(e).filter((r) => r.match(/^on[A-Z]/) && typeof e[r] == "function" && !t.includes(r)).forEach((r) => {
    n[r] = e[r];
  }), n;
}
function Jf(e) {
  if (e === void 0)
    return {};
  const t = {};
  return Object.keys(e).filter((n) => !(n.match(/^on[A-Z]/) && typeof e[n] == "function")).forEach((n) => {
    t[n] = e[n];
  }), t;
}
function AS(e) {
  const {
    getSlotProps: t,
    additionalProps: n,
    externalSlotProps: r,
    externalForwardedProps: o,
    className: i
  } = e;
  if (!t) {
    const v = oe(n == null ? void 0 : n.className, i, o == null ? void 0 : o.className, r == null ? void 0 : r.className), g = k({}, n == null ? void 0 : n.style, o == null ? void 0 : o.style, r == null ? void 0 : r.style), y = k({}, n, o, r);
    return v.length > 0 && (y.className = v), Object.keys(g).length > 0 && (y.style = g), {
      props: y,
      internalRef: void 0
    };
  }
  const l = jS(k({}, o, r)), s = Jf(r), a = Jf(o), u = t(l), d = oe(u == null ? void 0 : u.className, n == null ? void 0 : n.className, i, o == null ? void 0 : o.className, r == null ? void 0 : r.className), f = k({}, u == null ? void 0 : u.style, n == null ? void 0 : n.style, o == null ? void 0 : o.style, r == null ? void 0 : r.style), m = k({}, u, n, a, s);
  return d.length > 0 && (m.className = d), Object.keys(f).length > 0 && (m.style = f), {
    props: m,
    internalRef: u.ref
  };
}
function DS(e, t, n) {
  return typeof e == "function" ? e(t, n) : e;
}
const FS = /* @__PURE__ */ C.createContext(null), Ph = FS;
function Th() {
  return C.useContext(Ph);
}
const bS = typeof Symbol == "function" && Symbol.for, BS = bS ? Symbol.for("mui.nested") : "__THEME_NESTED__";
function WS(e, t) {
  return typeof t == "function" ? t(e) : k({}, e, t);
}
function US(e) {
  const {
    children: t,
    theme: n
  } = e, r = Th(), o = C.useMemo(() => {
    const i = r === null ? n : WS(r, n);
    return i != null && (i[BS] = r !== null), i;
  }, [n, r]);
  return /* @__PURE__ */ T.jsx(Ph.Provider, {
    value: o,
    children: t
  });
}
const VS = ["value"], HS = /* @__PURE__ */ C.createContext();
function KS(e) {
  let {
    value: t
  } = e, n = H(e, VS);
  return /* @__PURE__ */ T.jsx(HS.Provider, k({
    value: t ?? !0
  }, n));
}
const $h = /* @__PURE__ */ C.createContext(void 0);
function GS({
  value: e,
  children: t
}) {
  return /* @__PURE__ */ T.jsx($h.Provider, {
    value: e,
    children: t
  });
}
function QS(e) {
  const {
    theme: t,
    name: n,
    props: r
  } = e;
  if (!t || !t.components || !t.components[n])
    return r;
  const o = t.components[n];
  return o.defaultProps ? nl(o.defaultProps, r) : !o.styleOverrides && !o.variants ? nl(o, r) : r;
}
function YS({
  props: e,
  name: t
}) {
  const n = C.useContext($h);
  return QS({
    props: e,
    name: t,
    theme: {
      components: n
    }
  });
}
function XS(e) {
  const t = tc(), n = Ch() || "", {
    modularCssLayers: r
  } = e;
  let o = "mui.global, mui.components, mui.theme, mui.custom, mui.sx";
  return !r || t !== null ? o = "" : typeof r == "string" ? o = r.replace(/mui(?!\.)/g, o) : o = `@layer ${o};`, lc(() => {
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
  }, [o, n]), o ? /* @__PURE__ */ T.jsx(yh, {
    styles: o
  }) : null;
}
const ed = {};
function td(e, t, n, r = !1) {
  return C.useMemo(() => {
    const o = e && t[e] || t;
    if (typeof n == "function") {
      const i = n(o), l = e ? k({}, t, {
        [e]: i
      }) : i;
      return r ? () => l : l;
    }
    return e ? k({}, t, {
      [e]: n
    }) : k({}, t, n);
  }, [e, t, n, r]);
}
function qS(e) {
  const {
    children: t,
    theme: n,
    themeId: r
  } = e, o = tc(ed), i = Th() || ed, l = td(r, o, n), s = td(r, i, n, !0), a = l.direction === "rtl", u = XS(l);
  return /* @__PURE__ */ T.jsx(US, {
    theme: s,
    children: /* @__PURE__ */ T.jsx(_r.Provider, {
      value: l,
      children: /* @__PURE__ */ T.jsx(KS, {
        value: a,
        children: /* @__PURE__ */ T.jsxs(GS, {
          value: l == null ? void 0 : l.components,
          children: [u, t]
        })
      })
    })
  });
}
const ZS = ["className", "component", "disableGutters", "fixed", "maxWidth", "classes"], JS = Fo(), ex = uS("div", {
  name: "MuiContainer",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[`maxWidth${X(String(n.maxWidth))}`], n.fixed && t.fixed, n.disableGutters && t.disableGutters];
  }
}), tx = (e) => fS({
  props: e,
  name: "MuiContainer",
  defaultTheme: JS
}), nx = (e, t) => {
  const n = (a) => pt(t, a), {
    classes: r,
    fixed: o,
    disableGutters: i,
    maxWidth: l
  } = e, s = {
    root: ["root", l && `maxWidth${X(String(l))}`, o && "fixed", i && "disableGutters"]
  };
  return _t(s, n, r);
};
function rx(e = {}) {
  const {
    // This will allow adding custom styled fn (for example for custom sx style function)
    createStyledComponent: t = ex,
    useThemeProps: n = tx,
    componentName: r = "MuiContainer"
  } = e, o = t(({
    theme: l,
    ownerState: s
  }) => k({
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
    const d = u, f = l.breakpoints.values[d];
    return f !== 0 && (a[l.breakpoints.up(d)] = {
      maxWidth: `${f}${l.breakpoints.unit}`
    }), a;
  }, {}), ({
    theme: l,
    ownerState: s
  }) => k({}, s.maxWidth === "xs" && {
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
      className: d,
      component: f = "div",
      disableGutters: m = !1,
      fixed: v = !1,
      maxWidth: g = "lg"
    } = u, y = H(u, ZS), _ = k({}, u, {
      component: f,
      disableGutters: m,
      fixed: v,
      maxWidth: g
    }), p = nx(_, r);
    return (
      // @ts-ignore theme is injected by the styled util
      /* @__PURE__ */ T.jsx(o, k({
        as: f,
        ownerState: _,
        className: oe(p.root, d),
        ref: a
      }, y))
    );
  });
}
function ox(e, t) {
  return k({
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
var pe = {}, Rh = { exports: {} };
(function(e) {
  function t(n) {
    return n && n.__esModule ? n : {
      default: n
    };
  }
  e.exports = t, e.exports.__esModule = !0, e.exports.default = e.exports;
})(Rh);
var sc = Rh.exports;
const ix = /* @__PURE__ */ Gt(Mg), lx = /* @__PURE__ */ Gt(mS);
var Oh = sc;
Object.defineProperty(pe, "__esModule", {
  value: !0
});
var rl = pe.alpha = Lh;
pe.blend = gx;
pe.colorChannel = void 0;
var ba = pe.darken = uc;
pe.decomposeColor = ft;
pe.emphasize = Ih;
var sx = pe.getContrastRatio = dx;
pe.getLuminance = ol;
pe.hexToRgb = Mh;
pe.hslToRgb = zh;
var Ba = pe.lighten = cc;
pe.private_safeAlpha = px;
pe.private_safeColorChannel = void 0;
pe.private_safeDarken = mx;
pe.private_safeEmphasize = yx;
pe.private_safeLighten = hx;
pe.recomposeColor = Tr;
pe.rgbToHex = fx;
var nd = Oh(ix), ax = Oh(lx);
function ac(e, t = 0, n = 1) {
  return (0, ax.default)(e, t, n);
}
function Mh(e) {
  e = e.slice(1);
  const t = new RegExp(`.{1,${e.length >= 6 ? 2 : 1}}`, "g");
  let n = e.match(t);
  return n && n[0].length === 1 && (n = n.map((r) => r + r)), n ? `rgb${n.length === 4 ? "a" : ""}(${n.map((r, o) => o < 3 ? parseInt(r, 16) : Math.round(parseInt(r, 16) / 255 * 1e3) / 1e3).join(", ")})` : "";
}
function ux(e) {
  const t = e.toString(16);
  return t.length === 1 ? `0${t}` : t;
}
function ft(e) {
  if (e.type)
    return e;
  if (e.charAt(0) === "#")
    return ft(Mh(e));
  const t = e.indexOf("("), n = e.substring(0, t);
  if (["rgb", "rgba", "hsl", "hsla", "color"].indexOf(n) === -1)
    throw new Error((0, nd.default)(9, e));
  let r = e.substring(t + 1, e.length - 1), o;
  if (n === "color") {
    if (r = r.split(" "), o = r.shift(), r.length === 4 && r[3].charAt(0) === "/" && (r[3] = r[3].slice(1)), ["srgb", "display-p3", "a98-rgb", "prophoto-rgb", "rec-2020"].indexOf(o) === -1)
      throw new Error((0, nd.default)(10, o));
  } else
    r = r.split(",");
  return r = r.map((i) => parseFloat(i)), {
    type: n,
    values: r,
    colorSpace: o
  };
}
const Nh = (e) => {
  const t = ft(e);
  return t.values.slice(0, 3).map((n, r) => t.type.indexOf("hsl") !== -1 && r !== 0 ? `${n}%` : n).join(" ");
};
pe.colorChannel = Nh;
const cx = (e, t) => {
  try {
    return Nh(e);
  } catch {
    return e;
  }
};
pe.private_safeColorChannel = cx;
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
function fx(e) {
  if (e.indexOf("#") === 0)
    return e;
  const {
    values: t
  } = ft(e);
  return `#${t.map((n, r) => ux(r === 3 ? Math.round(255 * n) : n)).join("")}`;
}
function zh(e) {
  e = ft(e);
  const {
    values: t
  } = e, n = t[0], r = t[1] / 100, o = t[2] / 100, i = r * Math.min(o, 1 - o), l = (u, d = (u + n / 30) % 12) => o - i * Math.max(Math.min(d - 3, 9 - d, 1), -1);
  let s = "rgb";
  const a = [Math.round(l(0) * 255), Math.round(l(8) * 255), Math.round(l(4) * 255)];
  return e.type === "hsla" && (s += "a", a.push(t[3])), Tr({
    type: s,
    values: a
  });
}
function ol(e) {
  e = ft(e);
  let t = e.type === "hsl" || e.type === "hsla" ? ft(zh(e)).values : e.values;
  return t = t.map((n) => (e.type !== "color" && (n /= 255), n <= 0.03928 ? n / 12.92 : ((n + 0.055) / 1.055) ** 2.4)), Number((0.2126 * t[0] + 0.7152 * t[1] + 0.0722 * t[2]).toFixed(3));
}
function dx(e, t) {
  const n = ol(e), r = ol(t);
  return (Math.max(n, r) + 0.05) / (Math.min(n, r) + 0.05);
}
function Lh(e, t) {
  return e = ft(e), t = ac(t), (e.type === "rgb" || e.type === "hsl") && (e.type += "a"), e.type === "color" ? e.values[3] = `/${t}` : e.values[3] = t, Tr(e);
}
function px(e, t, n) {
  try {
    return Lh(e, t);
  } catch {
    return e;
  }
}
function uc(e, t) {
  if (e = ft(e), t = ac(t), e.type.indexOf("hsl") !== -1)
    e.values[2] *= 1 - t;
  else if (e.type.indexOf("rgb") !== -1 || e.type.indexOf("color") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] *= 1 - t;
  return Tr(e);
}
function mx(e, t, n) {
  try {
    return uc(e, t);
  } catch {
    return e;
  }
}
function cc(e, t) {
  if (e = ft(e), t = ac(t), e.type.indexOf("hsl") !== -1)
    e.values[2] += (100 - e.values[2]) * t;
  else if (e.type.indexOf("rgb") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] += (255 - e.values[n]) * t;
  else if (e.type.indexOf("color") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] += (1 - e.values[n]) * t;
  return Tr(e);
}
function hx(e, t, n) {
  try {
    return cc(e, t);
  } catch {
    return e;
  }
}
function Ih(e, t = 0.15) {
  return ol(e) > 0.5 ? uc(e, t) : cc(e, t);
}
function yx(e, t, n) {
  try {
    return Ih(e, t);
  } catch {
    return e;
  }
}
function gx(e, t, n, r = 1) {
  const o = (a, u) => Math.round((a ** (1 / r) * (1 - n) + u ** (1 / r) * n) ** r), i = ft(e), l = ft(t), s = [o(i.values[0], l.values[0]), o(i.values[1], l.values[1]), o(i.values[2], l.values[2])];
  return Tr({
    type: "rgb",
    values: s
  });
}
const vx = {
  black: "#000",
  white: "#fff"
}, Po = vx, Sx = {
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
}, xx = Sx, wx = {
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
}, Dn = wx, kx = {
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
}, Fn = kx, Cx = {
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
}, br = Cx, Ex = {
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
}, bn = Ex, _x = {
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
}, Bn = _x, Px = {
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
}, Wn = Px, Tx = ["mode", "contrastThreshold", "tonalOffset"], rd = {
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
    paper: Po.white,
    default: Po.white
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
}, Ds = {
  text: {
    primary: Po.white,
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
    active: Po.white,
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
function od(e, t, n, r) {
  const o = r.light || r, i = r.dark || r * 1.5;
  e[t] || (e.hasOwnProperty(n) ? e[t] = e[n] : t === "light" ? e.light = Ba(e.main, o) : t === "dark" && (e.dark = ba(e.main, i)));
}
function $x(e = "light") {
  return e === "dark" ? {
    main: bn[200],
    light: bn[50],
    dark: bn[400]
  } : {
    main: bn[700],
    light: bn[400],
    dark: bn[800]
  };
}
function Rx(e = "light") {
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
function Ox(e = "light") {
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
function Mx(e = "light") {
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
function Nx(e = "light") {
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
function zx(e = "light") {
  return e === "dark" ? {
    main: br[400],
    light: br[300],
    dark: br[700]
  } : {
    main: "#ed6c02",
    // closest to orange[800] that pass 3:1.
    light: br[500],
    dark: br[900]
  };
}
function Lx(e) {
  const {
    mode: t = "light",
    contrastThreshold: n = 3,
    tonalOffset: r = 0.2
  } = e, o = H(e, Tx), i = e.primary || $x(t), l = e.secondary || Rx(t), s = e.error || Ox(t), a = e.info || Mx(t), u = e.success || Nx(t), d = e.warning || zx(t);
  function f(y) {
    return sx(y, Ds.text.primary) >= n ? Ds.text.primary : rd.text.primary;
  }
  const m = ({
    color: y,
    name: _,
    mainShade: p = 500,
    lightShade: c = 300,
    darkShade: h = 700
  }) => {
    if (y = k({}, y), !y.main && y[p] && (y.main = y[p]), !y.hasOwnProperty("main"))
      throw new Error(wo(11, _ ? ` (${_})` : "", p));
    if (typeof y.main != "string")
      throw new Error(wo(12, _ ? ` (${_})` : "", JSON.stringify(y.main)));
    return od(y, "light", c, r), od(y, "dark", h, r), y.contrastText || (y.contrastText = f(y.main)), y;
  }, v = {
    dark: Ds,
    light: rd
  };
  return It(k({
    // A collection of common colors.
    common: k({}, Po),
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
      color: d,
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
    grey: xx,
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
const Ix = ["fontFamily", "fontSize", "fontWeightLight", "fontWeightRegular", "fontWeightMedium", "fontWeightBold", "htmlFontSize", "allVariants", "pxToRem"];
function jx(e) {
  return Math.round(e * 1e5) / 1e5;
}
const id = {
  textTransform: "uppercase"
}, ld = '"Roboto", "Helvetica", "Arial", sans-serif';
function Ax(e, t) {
  const n = typeof t == "function" ? t(e) : t, {
    fontFamily: r = ld,
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
    allVariants: d,
    pxToRem: f
  } = n, m = H(n, Ix), v = o / 14, g = f || ((p) => `${p / u * v}rem`), y = (p, c, h, S, E) => k({
    fontFamily: r,
    fontWeight: p,
    fontSize: g(c),
    // Unitless following https://meyerweb.com/eric/thoughts/2006/02/08/unitless-line-heights/
    lineHeight: h
  }, r === ld ? {
    letterSpacing: `${jx(S / c)}em`
  } : {}, E, d), _ = {
    h1: y(i, 96, 1.167, -1.5),
    h2: y(i, 60, 1.2, -0.5),
    h3: y(l, 48, 1.167, 0),
    h4: y(l, 34, 1.235, 0.25),
    h5: y(l, 24, 1.334, 0),
    h6: y(s, 20, 1.6, 0.15),
    subtitle1: y(l, 16, 1.75, 0.15),
    subtitle2: y(s, 14, 1.57, 0.1),
    body1: y(l, 16, 1.5, 0.15),
    body2: y(l, 14, 1.43, 0.15),
    button: y(s, 14, 1.75, 0.4, id),
    caption: y(l, 12, 1.66, 0.4),
    overline: y(l, 12, 2.66, 1, id),
    // TODO v6: Remove handling of 'inherit' variant from the theme as it is already handled in Material UI's Typography component. Also, remember to remove the associated types.
    inherit: {
      fontFamily: "inherit",
      fontWeight: "inherit",
      fontSize: "inherit",
      lineHeight: "inherit",
      letterSpacing: "inherit"
    }
  };
  return It(k({
    htmlFontSize: u,
    pxToRem: g,
    fontFamily: r,
    fontSize: o,
    fontWeightLight: i,
    fontWeightRegular: l,
    fontWeightMedium: s,
    fontWeightBold: a
  }, _), m, {
    clone: !1
    // No need to clone deep
  });
}
const Dx = 0.2, Fx = 0.14, bx = 0.12;
function te(...e) {
  return [`${e[0]}px ${e[1]}px ${e[2]}px ${e[3]}px rgba(0,0,0,${Dx})`, `${e[4]}px ${e[5]}px ${e[6]}px ${e[7]}px rgba(0,0,0,${Fx})`, `${e[8]}px ${e[9]}px ${e[10]}px ${e[11]}px rgba(0,0,0,${bx})`].join(",");
}
const Bx = ["none", te(0, 2, 1, -1, 0, 1, 1, 0, 0, 1, 3, 0), te(0, 3, 1, -2, 0, 2, 2, 0, 0, 1, 5, 0), te(0, 3, 3, -2, 0, 3, 4, 0, 0, 1, 8, 0), te(0, 2, 4, -1, 0, 4, 5, 0, 0, 1, 10, 0), te(0, 3, 5, -1, 0, 5, 8, 0, 0, 1, 14, 0), te(0, 3, 5, -1, 0, 6, 10, 0, 0, 1, 18, 0), te(0, 4, 5, -2, 0, 7, 10, 1, 0, 2, 16, 1), te(0, 5, 5, -3, 0, 8, 10, 1, 0, 3, 14, 2), te(0, 5, 6, -3, 0, 9, 12, 1, 0, 3, 16, 2), te(0, 6, 6, -3, 0, 10, 14, 1, 0, 4, 18, 3), te(0, 6, 7, -4, 0, 11, 15, 1, 0, 4, 20, 3), te(0, 7, 8, -4, 0, 12, 17, 2, 0, 5, 22, 4), te(0, 7, 8, -4, 0, 13, 19, 2, 0, 5, 24, 4), te(0, 7, 9, -4, 0, 14, 21, 2, 0, 5, 26, 4), te(0, 8, 9, -5, 0, 15, 22, 2, 0, 6, 28, 5), te(0, 8, 10, -5, 0, 16, 24, 2, 0, 6, 30, 5), te(0, 8, 11, -5, 0, 17, 26, 2, 0, 6, 32, 5), te(0, 9, 11, -5, 0, 18, 28, 2, 0, 7, 34, 6), te(0, 9, 12, -6, 0, 19, 29, 2, 0, 7, 36, 6), te(0, 10, 13, -6, 0, 20, 31, 3, 0, 8, 38, 7), te(0, 10, 13, -6, 0, 21, 33, 3, 0, 8, 40, 7), te(0, 10, 14, -6, 0, 22, 35, 3, 0, 8, 42, 7), te(0, 11, 14, -7, 0, 23, 36, 3, 0, 9, 44, 8), te(0, 11, 15, -7, 0, 24, 38, 3, 0, 9, 46, 8)], Wx = Bx, Ux = ["duration", "easing", "delay"], Vx = {
  // This is the most common easing curve.
  easeInOut: "cubic-bezier(0.4, 0, 0.2, 1)",
  // Objects enter the screen at full velocity from off-screen and
  // slowly decelerate to a resting point.
  easeOut: "cubic-bezier(0.0, 0, 0.2, 1)",
  // Objects leave the screen at full velocity. They do not decelerate when off-screen.
  easeIn: "cubic-bezier(0.4, 0, 1, 1)",
  // The sharp curve is used by objects that may return to the screen at any time.
  sharp: "cubic-bezier(0.4, 0, 0.6, 1)"
}, jh = {
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
function sd(e) {
  return `${Math.round(e)}ms`;
}
function Hx(e) {
  if (!e)
    return 0;
  const t = e / 36;
  return Math.round((4 + 15 * t ** 0.25 + t / 5) * 10);
}
function Kx(e) {
  const t = k({}, Vx, e.easing), n = k({}, jh, e.duration);
  return k({
    getAutoHeightDuration: Hx,
    create: (o = ["all"], i = {}) => {
      const {
        duration: l = n.standard,
        easing: s = t.easeInOut,
        delay: a = 0
      } = i;
      return H(i, Ux), (Array.isArray(o) ? o : [o]).map((u) => `${u} ${typeof l == "string" ? l : sd(l)} ${s} ${typeof a == "string" ? a : sd(a)}`).join(",");
    }
  }, e, {
    easing: t,
    duration: n
  });
}
const Gx = {
  mobileStepper: 1e3,
  fab: 1050,
  speedDial: 1050,
  appBar: 1100,
  drawer: 1200,
  modal: 1300,
  snackbar: 1400,
  tooltip: 1500
}, Qx = Gx, Yx = ["breakpoints", "mixins", "spacing", "palette", "transitions", "typography", "shape"];
function fc(e = {}, ...t) {
  const {
    mixins: n = {},
    palette: r = {},
    transitions: o = {},
    typography: i = {}
  } = e, l = H(e, Yx);
  if (e.vars && // The error should throw only for the root theme creation because user is not allowed to use a custom node `vars`.
  // `generateCssVars` is the closest identifier for checking that the `options` is a result of `extendTheme` with CSS variables so that user can create new theme for nested ThemeProvider.
  e.generateCssVars === void 0)
    throw new Error(wo(18));
  const s = Lx(r), a = Fo(e);
  let u = It(a, {
    mixins: ox(a.breakpoints, n),
    palette: s,
    // Don't use [...shadows] until you've verified its transpiled code is not invoking the iterator protocol.
    shadows: Wx.slice(),
    typography: Ax(s, i),
    transitions: Kx(o),
    zIndex: k({}, Qx)
  });
  return u = It(u, l), u = t.reduce((d, f) => It(d, f), u), u.unstable_sxConfig = k({}, Ao, l == null ? void 0 : l.unstable_sxConfig), u.unstable_sx = function(f) {
    return Do({
      sx: f,
      theme: this
    });
  }, u;
}
const Xx = fc(), dc = Xx;
function qx() {
  const e = Ul(dc);
  return e[vr] || e;
}
var bo = {}, Fs = { exports: {} }, ad;
function Zx() {
  return ad || (ad = 1, function(e) {
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
  }(Fs)), Fs.exports;
}
const Jx = /* @__PURE__ */ Gt(Wv), ew = /* @__PURE__ */ Gt(Uv), tw = /* @__PURE__ */ Gt(Yv), nw = /* @__PURE__ */ Gt(Z1), rw = /* @__PURE__ */ Gt(A1), ow = /* @__PURE__ */ Gt(W1);
var $r = sc;
Object.defineProperty(bo, "__esModule", {
  value: !0
});
var iw = bo.default = vw;
bo.shouldForwardProp = Ti;
bo.systemDefaultTheme = void 0;
var nt = $r(lh()), Wa = $r(Zx()), il = dw(Jx), lw = ew;
$r(tw);
$r(nw);
var sw = $r(rw), aw = $r(ow);
const uw = ["ownerState"], cw = ["variants"], fw = ["name", "slot", "skipVariantsResolver", "skipSx", "overridesResolver"];
function Ah(e) {
  if (typeof WeakMap != "function")
    return null;
  var t = /* @__PURE__ */ new WeakMap(), n = /* @__PURE__ */ new WeakMap();
  return (Ah = function(r) {
    return r ? n : t;
  })(e);
}
function dw(e, t) {
  if (!t && e && e.__esModule)
    return e;
  if (e === null || typeof e != "object" && typeof e != "function")
    return { default: e };
  var n = Ah(t);
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
function pw(e) {
  return Object.keys(e).length === 0;
}
function mw(e) {
  return typeof e == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  e.charCodeAt(0) > 96;
}
function Ti(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
function ud(e, t) {
  return t && e && typeof e == "object" && e.styles && !e.styles.startsWith("@layer") && (e.styles = `@layer ${t}{${String(e.styles)}}`), e;
}
const hw = bo.systemDefaultTheme = (0, sw.default)(), yw = (e) => e && e.charAt(0).toLowerCase() + e.slice(1);
function ci({
  defaultTheme: e,
  theme: t,
  themeId: n
}) {
  return pw(t) ? e : t[n] || t;
}
function gw(e) {
  return e ? (t, n) => n[e] : null;
}
function $i(e, t, n) {
  let {
    ownerState: r
  } = t, o = (0, Wa.default)(t, uw);
  const i = typeof e == "function" ? e((0, nt.default)({
    ownerState: r
  }, o)) : e;
  if (Array.isArray(i))
    return i.flatMap((l) => $i(l, (0, nt.default)({
      ownerState: r
    }, o), n));
  if (i && typeof i == "object" && Array.isArray(i.variants)) {
    const {
      variants: l = []
    } = i;
    let a = (0, Wa.default)(i, cw);
    return l.forEach((u) => {
      let d = !0;
      if (typeof u.props == "function" ? d = u.props((0, nt.default)({
        ownerState: r
      }, o, r)) : Object.keys(u.props).forEach((f) => {
        (r == null ? void 0 : r[f]) !== u.props[f] && o[f] !== u.props[f] && (d = !1);
      }), d) {
        Array.isArray(a) || (a = [a]);
        const f = typeof u.style == "function" ? u.style((0, nt.default)({
          ownerState: r
        }, o, r)) : u.style;
        a.push(n ? ud((0, il.internal_serializeStyles)(f), n) : f);
      }
    }), a;
  }
  return n ? ud((0, il.internal_serializeStyles)(i), n) : i;
}
function vw(e = {}) {
  const {
    themeId: t,
    defaultTheme: n = hw,
    rootShouldForwardProp: r = Ti,
    slotShouldForwardProp: o = Ti
  } = e, i = (l) => (0, aw.default)((0, nt.default)({}, l, {
    theme: ci((0, nt.default)({}, l, {
      defaultTheme: n,
      themeId: t
    }))
  }));
  return i.__mui_systemSx = !0, (l, s = {}) => {
    (0, il.internal_processStyles)(l, (w) => w.filter((x) => !(x != null && x.__mui_systemSx)));
    const {
      name: a,
      slot: u,
      skipVariantsResolver: d,
      skipSx: f,
      // TODO v6: remove `lowercaseFirstLetter()` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      overridesResolver: m = gw(yw(u))
    } = s, v = (0, Wa.default)(s, fw), g = a && a.startsWith("Mui") || u ? "components" : "custom", y = d !== void 0 ? d : (
      // TODO v6: remove `Root` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      u && u !== "Root" && u !== "root" || !1
    ), _ = f || !1;
    let p, c = Ti;
    u === "Root" || u === "root" ? c = r : u ? c = o : mw(l) && (c = void 0);
    const h = (0, il.default)(l, (0, nt.default)({
      shouldForwardProp: c,
      label: p
    }, v)), S = (w) => typeof w == "function" && w.__emotion_real !== w || (0, lw.isPlainObject)(w) ? (x) => {
      const $ = ci({
        theme: x.theme,
        defaultTheme: n,
        themeId: t
      });
      return $i(w, (0, nt.default)({}, x, {
        theme: $
      }), $.modularCssLayers ? g : void 0);
    } : w, E = (w, ...x) => {
      let $ = S(w);
      const N = x ? x.map(S) : [];
      a && m && N.push((A) => {
        const L = ci((0, nt.default)({}, A, {
          defaultTheme: n,
          themeId: t
        }));
        if (!L.components || !L.components[a] || !L.components[a].styleOverrides)
          return null;
        const W = L.components[a].styleOverrides, ee = {};
        return Object.entries(W).forEach(([ve, he]) => {
          ee[ve] = $i(he, (0, nt.default)({}, A, {
            theme: L
          }), L.modularCssLayers ? "theme" : void 0);
        }), m(A, ee);
      }), a && !y && N.push((A) => {
        var L;
        const W = ci((0, nt.default)({}, A, {
          defaultTheme: n,
          themeId: t
        })), ee = W == null || (L = W.components) == null || (L = L[a]) == null ? void 0 : L.variants;
        return $i({
          variants: ee
        }, (0, nt.default)({}, A, {
          theme: W
        }), W.modularCssLayers ? "theme" : void 0);
      }), _ || N.push(i);
      const O = N.length - x.length;
      if (Array.isArray(w) && O > 0) {
        const A = new Array(O).fill("");
        $ = [...w, ...A], $.raw = [...w.raw, ...A];
      }
      const b = h($, ...N);
      return l.muiName && (b.muiName = l.muiName), b;
    };
    return h.withConfig && (E.withConfig = h.withConfig), E;
  };
}
function Sw(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
const xw = (e) => Sw(e) && e !== "classes", ww = xw, kw = iw({
  themeId: vr,
  defaultTheme: dc,
  rootShouldForwardProp: ww
}), me = kw, Cw = ["theme"];
function Ew(e) {
  let {
    theme: t
  } = e, n = H(e, Cw);
  const r = t[vr];
  let o = r || t;
  return typeof t != "function" && (r && !r.vars ? o = k({}, r, {
    vars: null
  }) : t && !t.vars && (o = k({}, t, {
    vars: null
  }))), /* @__PURE__ */ T.jsx(qS, k({}, n, {
    themeId: r ? vr : void 0,
    theme: o
  }));
}
const _w = (e) => {
  let t;
  return e < 1 ? t = 5.11916 * e ** 2 : t = 4.5 * Math.log(e + 1) + 2, (t / 100).toFixed(2);
}, cd = _w;
function tt(e) {
  return YS(e);
}
function Pw(e) {
  return /* @__PURE__ */ T.jsx(yh, k({}, e, {
    defaultTheme: dc,
    themeId: vr
  }));
}
const Tw = (e, t) => k({
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
}), $w = (e) => k({
  color: (e.vars || e).palette.text.primary
}, e.typography.body1, {
  backgroundColor: (e.vars || e).palette.background.default,
  "@media print": {
    // Save printer ink.
    backgroundColor: (e.vars || e).palette.common.white
  }
}), Rw = (e, t = !1) => {
  var n;
  const r = {};
  t && e.colorSchemes && Object.entries(e.colorSchemes).forEach(([l, s]) => {
    var a;
    r[e.getColorSchemeSelector(l).replace(/\s*&/, "")] = {
      colorScheme: (a = s.palette) == null ? void 0 : a.mode
    };
  });
  let o = k({
    html: Tw(e, t),
    "*, *::before, *::after": {
      boxSizing: "inherit"
    },
    "strong, b": {
      fontWeight: e.typography.fontWeightBold
    },
    body: k({
      margin: 0
    }, $w(e), {
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
function Ow(e) {
  const t = tt({
    props: e,
    name: "MuiCssBaseline"
  }), {
    children: n,
    enableColorScheme: r = !1
  } = t;
  return /* @__PURE__ */ T.jsxs(C.Fragment, {
    children: [/* @__PURE__ */ T.jsx(Pw, {
      styles: (o) => Rw(o, r)
    }), n]
  });
}
const Mw = rx({
  createStyledComponent: me("div", {
    name: "MuiContainer",
    slot: "Root",
    overridesResolver: (e, t) => {
      const {
        ownerState: n
      } = e;
      return [t.root, t[`maxWidth${X(String(n.maxWidth))}`], n.fixed && t.fixed, n.disableGutters && t.disableGutters];
    }
  }),
  useThemeProps: (e) => tt({
    props: e,
    name: "MuiContainer"
  })
}), Nw = Mw;
function zw(e) {
  return pt("MuiTypography", e);
}
mt("MuiTypography", ["root", "h1", "h2", "h3", "h4", "h5", "h6", "subtitle1", "subtitle2", "body1", "body2", "inherit", "button", "caption", "overline", "alignLeft", "alignRight", "alignCenter", "alignJustify", "noWrap", "gutterBottom", "paragraph"]);
const Lw = ["align", "className", "component", "gutterBottom", "noWrap", "paragraph", "variant", "variantMapping"], Iw = (e) => {
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
  return _t(s, zw, l);
}, jw = me("span", {
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
}) => k({
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
})), fd = {
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
}, Aw = {
  primary: "primary.main",
  textPrimary: "text.primary",
  secondary: "secondary.main",
  textSecondary: "text.secondary",
  error: "error.main"
}, Dw = (e) => Aw[e] || e, Fw = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = tt({
    props: t,
    name: "MuiTypography"
  }), o = Dw(r.color), i = nc(k({}, r, {
    color: o
  })), {
    align: l = "inherit",
    className: s,
    component: a,
    gutterBottom: u = !1,
    noWrap: d = !1,
    paragraph: f = !1,
    variant: m = "body1",
    variantMapping: v = fd
  } = i, g = H(i, Lw), y = k({}, i, {
    align: l,
    color: o,
    className: s,
    component: a,
    gutterBottom: u,
    noWrap: d,
    paragraph: f,
    variant: m,
    variantMapping: v
  }), _ = a || (f ? "p" : v[m] || fd[m]) || "span", p = Iw(y);
  return /* @__PURE__ */ T.jsx(jw, k({
    as: _,
    ref: n,
    ownerState: y,
    className: oe(p.root, s)
  }, g));
}), xr = Fw;
function bw(e) {
  return pt("MuiCircularProgress", e);
}
mt("MuiCircularProgress", ["root", "determinate", "indeterminate", "colorPrimary", "colorSecondary", "svg", "circle", "circleDeterminate", "circleIndeterminate", "circleDisableShrink"]);
const Bw = ["className", "color", "disableShrink", "size", "style", "thickness", "value", "variant"];
let ns = (e) => e, dd, pd, md, hd;
const Zt = 44, Ww = Pr(dd || (dd = ns`
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
`)), Uw = Pr(pd || (pd = ns`
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
`)), Vw = (e) => {
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
  return _t(i, bw, t);
}, Hw = me("span", {
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
}) => k({
  display: "inline-block"
}, e.variant === "determinate" && {
  transition: t.transitions.create("transform")
}, e.color !== "inherit" && {
  color: (t.vars || t).palette[e.color].main
}), ({
  ownerState: e
}) => e.variant === "indeterminate" && jl(md || (md = ns`
      animation: ${0} 1.4s linear infinite;
    `), Ww)), Kw = me("svg", {
  name: "MuiCircularProgress",
  slot: "Svg",
  overridesResolver: (e, t) => t.svg
})({
  display: "block"
  // Keeps the progress centered
}), Gw = me("circle", {
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
}) => k({
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
}) => e.variant === "indeterminate" && !e.disableShrink && jl(hd || (hd = ns`
      animation: ${0} 1.4s ease-in-out infinite;
    `), Uw)), Qw = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = tt({
    props: t,
    name: "MuiCircularProgress"
  }), {
    className: o,
    color: i = "primary",
    disableShrink: l = !1,
    size: s = 40,
    style: a,
    thickness: u = 3.6,
    value: d = 0,
    variant: f = "indeterminate"
  } = r, m = H(r, Bw), v = k({}, r, {
    color: i,
    disableShrink: l,
    size: s,
    thickness: u,
    value: d,
    variant: f
  }), g = Vw(v), y = {}, _ = {}, p = {};
  if (f === "determinate") {
    const c = 2 * Math.PI * ((Zt - u) / 2);
    y.strokeDasharray = c.toFixed(3), p["aria-valuenow"] = Math.round(d), y.strokeDashoffset = `${((100 - d) / 100 * c).toFixed(3)}px`, _.transform = "rotate(-90deg)";
  }
  return /* @__PURE__ */ T.jsx(Hw, k({
    className: oe(g.root, o),
    style: k({
      width: s,
      height: s
    }, _, a),
    ownerState: v,
    ref: n,
    role: "progressbar"
  }, p, m, {
    children: /* @__PURE__ */ T.jsx(Kw, {
      className: g.svg,
      ownerState: v,
      viewBox: `${Zt / 2} ${Zt / 2} ${Zt} ${Zt}`,
      children: /* @__PURE__ */ T.jsx(Gw, {
        className: g.circle,
        style: y,
        ownerState: v,
        cx: Zt,
        cy: Zt,
        r: (Zt - u) / 2,
        fill: "none",
        strokeWidth: u
      })
    })
  }));
}), Yw = Qw, Xw = ["className", "elementType", "ownerState", "externalForwardedProps", "getSlotOwnerState", "internalForwardedProps"], qw = ["component", "slots", "slotProps"], Zw = ["component"];
function yd(e, t) {
  const {
    className: n,
    elementType: r,
    ownerState: o,
    externalForwardedProps: i,
    getSlotOwnerState: l,
    internalForwardedProps: s
  } = t, a = H(t, Xw), {
    component: u,
    slots: d = {
      [e]: void 0
    },
    slotProps: f = {
      [e]: void 0
    }
  } = i, m = H(i, qw), v = d[e] || r, g = DS(f[e], o), y = AS(k({
    className: n
  }, a, {
    externalForwardedProps: e === "root" ? m : void 0,
    externalSlotProps: g
  })), {
    props: {
      component: _
    },
    internalRef: p
  } = y, c = H(y.props, Zw), h = _o(p, g == null ? void 0 : g.ref, t.ref), S = l ? l(c) : {}, E = k({}, o, S), w = e === "root" ? _ || u : _, x = IS(v, k({}, e === "root" && !u && !d[e] && s, e !== "root" && !d[e] && s, c, w && {
    as: w
  }, {
    ref: h
  }), E);
  return Object.keys(S).forEach(($) => {
    delete x[$];
  }), [v, x];
}
function Jw(e) {
  return pt("MuiPaper", e);
}
mt("MuiPaper", ["root", "rounded", "outlined", "elevation", "elevation0", "elevation1", "elevation2", "elevation3", "elevation4", "elevation5", "elevation6", "elevation7", "elevation8", "elevation9", "elevation10", "elevation11", "elevation12", "elevation13", "elevation14", "elevation15", "elevation16", "elevation17", "elevation18", "elevation19", "elevation20", "elevation21", "elevation22", "elevation23", "elevation24"]);
const e2 = ["className", "component", "elevation", "square", "variant"], t2 = (e) => {
  const {
    square: t,
    elevation: n,
    variant: r,
    classes: o
  } = e, i = {
    root: ["root", r, !t && "rounded", r === "elevation" && `elevation${n}`]
  };
  return _t(i, Jw, o);
}, n2 = me("div", {
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
  return k({
    backgroundColor: (e.vars || e).palette.background.paper,
    color: (e.vars || e).palette.text.primary,
    transition: e.transitions.create("box-shadow")
  }, !t.square && {
    borderRadius: e.shape.borderRadius
  }, t.variant === "outlined" && {
    border: `1px solid ${(e.vars || e).palette.divider}`
  }, t.variant === "elevation" && k({
    boxShadow: (e.vars || e).shadows[t.elevation]
  }, !e.vars && e.palette.mode === "dark" && {
    backgroundImage: `linear-gradient(${rl("#fff", cd(t.elevation))}, ${rl("#fff", cd(t.elevation))})`
  }, e.vars && {
    backgroundImage: (n = e.vars.overlays) == null ? void 0 : n[t.elevation]
  }));
}), r2 = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = tt({
    props: t,
    name: "MuiPaper"
  }), {
    className: o,
    component: i = "div",
    elevation: l = 1,
    square: s = !1,
    variant: a = "elevation"
  } = r, u = H(r, e2), d = k({}, r, {
    component: i,
    elevation: l,
    square: s,
    variant: a
  }), f = t2(d);
  return /* @__PURE__ */ T.jsx(n2, k({
    as: i,
    ownerState: d,
    className: oe(f.root, o),
    ref: n
  }, u));
}), Dh = r2;
function o2(e) {
  return pt("MuiAlert", e);
}
const i2 = mt("MuiAlert", ["root", "action", "icon", "message", "filled", "colorSuccess", "colorInfo", "colorWarning", "colorError", "filledSuccess", "filledInfo", "filledWarning", "filledError", "outlined", "outlinedSuccess", "outlinedInfo", "outlinedWarning", "outlinedError", "standard", "standardSuccess", "standardInfo", "standardWarning", "standardError"]), gd = i2;
function Ua(e, t) {
  return Ua = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, r) {
    return n.__proto__ = r, n;
  }, Ua(e, t);
}
function Fh(e, t) {
  e.prototype = Object.create(t.prototype), e.prototype.constructor = e, Ua(e, t);
}
const vd = {
  disabled: !1
}, ll = wt.createContext(null);
var l2 = function(t) {
  return t.scrollTop;
}, Kr = "unmounted", wn = "exited", kn = "entering", Vn = "entered", Va = "exiting", Yt = /* @__PURE__ */ function(e) {
  Fh(t, e);
  function t(r, o) {
    var i;
    i = e.call(this, r, o) || this;
    var l = o, s = l && !l.isMounting ? r.enter : r.appear, a;
    return i.appearStatus = null, r.in ? s ? (a = wn, i.appearStatus = kn) : a = Vn : r.unmountOnExit || r.mountOnEnter ? a = Kr : a = wn, i.state = {
      status: a
    }, i.nextCallback = null, i;
  }
  t.getDerivedStateFromProps = function(o, i) {
    var l = o.in;
    return l && i.status === Kr ? {
      status: wn
    } : null;
  };
  var n = t.prototype;
  return n.componentDidMount = function() {
    this.updateStatus(!0, this.appearStatus);
  }, n.componentDidUpdate = function(o) {
    var i = null;
    if (o !== this.props) {
      var l = this.state.status;
      this.props.in ? l !== kn && l !== Vn && (i = kn) : (l === kn || l === Vn) && (i = Va);
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
      if (this.cancelNextCallback(), i === kn) {
        if (this.props.unmountOnExit || this.props.mountOnEnter) {
          var l = this.props.nodeRef ? this.props.nodeRef.current : si.findDOMNode(this);
          l && l2(l);
        }
        this.performEnter(o);
      } else
        this.performExit();
    else
      this.props.unmountOnExit && this.state.status === wn && this.setState({
        status: Kr
      });
  }, n.performEnter = function(o) {
    var i = this, l = this.props.enter, s = this.context ? this.context.isMounting : o, a = this.props.nodeRef ? [s] : [si.findDOMNode(this), s], u = a[0], d = a[1], f = this.getTimeouts(), m = s ? f.appear : f.enter;
    if (!o && !l || vd.disabled) {
      this.safeSetState({
        status: Vn
      }, function() {
        i.props.onEntered(u);
      });
      return;
    }
    this.props.onEnter(u, d), this.safeSetState({
      status: kn
    }, function() {
      i.props.onEntering(u, d), i.onTransitionEnd(m, function() {
        i.safeSetState({
          status: Vn
        }, function() {
          i.props.onEntered(u, d);
        });
      });
    });
  }, n.performExit = function() {
    var o = this, i = this.props.exit, l = this.getTimeouts(), s = this.props.nodeRef ? void 0 : si.findDOMNode(this);
    if (!i || vd.disabled) {
      this.safeSetState({
        status: wn
      }, function() {
        o.props.onExited(s);
      });
      return;
    }
    this.props.onExit(s), this.safeSetState({
      status: Va
    }, function() {
      o.props.onExiting(s), o.onTransitionEnd(l.exit, function() {
        o.safeSetState({
          status: wn
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
    var l = this.props.nodeRef ? this.props.nodeRef.current : si.findDOMNode(this), s = o == null && !this.props.addEndListener;
    if (!l || s) {
      setTimeout(this.nextCallback, 0);
      return;
    }
    if (this.props.addEndListener) {
      var a = this.props.nodeRef ? [this.nextCallback] : [l, this.nextCallback], u = a[0], d = a[1];
      this.props.addEndListener(u, d);
    }
    o != null && setTimeout(this.nextCallback, o);
  }, n.render = function() {
    var o = this.state.status;
    if (o === Kr)
      return null;
    var i = this.props, l = i.children;
    i.in, i.mountOnEnter, i.unmountOnExit, i.appear, i.enter, i.exit, i.timeout, i.addEndListener, i.onEnter, i.onEntering, i.onEntered, i.onExit, i.onExiting, i.onExited, i.nodeRef;
    var s = H(i, ["children", "in", "mountOnEnter", "unmountOnExit", "appear", "enter", "exit", "timeout", "addEndListener", "onEnter", "onEntering", "onEntered", "onExit", "onExiting", "onExited", "nodeRef"]);
    return (
      // allows for nested Transitions
      /* @__PURE__ */ wt.createElement(ll.Provider, {
        value: null
      }, typeof l == "function" ? l(o, s) : wt.cloneElement(wt.Children.only(l), s))
    );
  }, t;
}(wt.Component);
Yt.contextType = ll;
Yt.propTypes = {};
function Un() {
}
Yt.defaultProps = {
  in: !1,
  mountOnEnter: !1,
  unmountOnExit: !1,
  appear: !1,
  enter: !0,
  exit: !0,
  onEnter: Un,
  onEntering: Un,
  onEntered: Un,
  onExit: Un,
  onExiting: Un,
  onExited: Un
};
Yt.UNMOUNTED = Kr;
Yt.EXITED = wn;
Yt.ENTERING = kn;
Yt.ENTERED = Vn;
Yt.EXITING = Va;
const s2 = Yt;
function a2(e) {
  if (e === void 0)
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function pc(e, t) {
  var n = function(i) {
    return t && C.isValidElement(i) ? t(i) : i;
  }, r = /* @__PURE__ */ Object.create(null);
  return e && C.Children.map(e, function(o) {
    return o;
  }).forEach(function(o) {
    r[o.key] = n(o);
  }), r;
}
function u2(e, t) {
  e = e || {}, t = t || {};
  function n(d) {
    return d in t ? t[d] : e[d];
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
function c2(e, t) {
  return pc(e.children, function(n) {
    return C.cloneElement(n, {
      onExited: t.bind(null, n),
      in: !0,
      appear: Pn(n, "appear", e),
      enter: Pn(n, "enter", e),
      exit: Pn(n, "exit", e)
    });
  });
}
function f2(e, t, n) {
  var r = pc(e.children), o = u2(t, r);
  return Object.keys(o).forEach(function(i) {
    var l = o[i];
    if (C.isValidElement(l)) {
      var s = i in t, a = i in r, u = t[i], d = C.isValidElement(u) && !u.props.in;
      a && (!s || d) ? o[i] = C.cloneElement(l, {
        onExited: n.bind(null, l),
        in: !0,
        exit: Pn(l, "exit", e),
        enter: Pn(l, "enter", e)
      }) : !a && s && !d ? o[i] = C.cloneElement(l, {
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
var d2 = Object.values || function(e) {
  return Object.keys(e).map(function(t) {
    return e[t];
  });
}, p2 = {
  component: "div",
  childFactory: function(t) {
    return t;
  }
}, mc = /* @__PURE__ */ function(e) {
  Fh(t, e);
  function t(r, o) {
    var i;
    i = e.call(this, r, o) || this;
    var l = i.handleExited.bind(a2(i));
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
      children: a ? c2(o, s) : f2(o, l, s),
      firstRender: !1
    };
  }, n.handleExited = function(o, i) {
    var l = pc(this.props.children);
    o.key in l || (o.props.onExited && o.props.onExited(i), this.mounted && this.setState(function(s) {
      var a = k({}, s.children);
      return delete a[o.key], {
        children: a
      };
    }));
  }, n.render = function() {
    var o = this.props, i = o.component, l = o.childFactory, s = H(o, ["component", "childFactory"]), a = this.state.contextValue, u = d2(this.state.children).map(l);
    return delete s.appear, delete s.enter, delete s.exit, i === null ? /* @__PURE__ */ wt.createElement(ll.Provider, {
      value: a
    }, u) : /* @__PURE__ */ wt.createElement(ll.Provider, {
      value: a
    }, /* @__PURE__ */ wt.createElement(i, s, u));
  }, t;
}(wt.Component);
mc.propTypes = {};
mc.defaultProps = p2;
const m2 = mc;
function h2(e) {
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
  } = e, [d, f] = C.useState(!1), m = oe(t, n.ripple, n.rippleVisible, r && n.ripplePulsate), v = {
    width: l,
    height: l,
    top: -(l / 2) + i,
    left: -(l / 2) + o
  }, g = oe(n.child, d && n.childLeaving, r && n.childPulsate);
  return !s && !d && f(!0), C.useEffect(() => {
    if (!s && a != null) {
      const y = setTimeout(a, u);
      return () => {
        clearTimeout(y);
      };
    }
  }, [a, s, u]), /* @__PURE__ */ T.jsx("span", {
    className: m,
    style: v,
    children: /* @__PURE__ */ T.jsx("span", {
      className: g
    })
  });
}
const y2 = mt("MuiTouchRipple", ["root", "ripple", "rippleVisible", "ripplePulsate", "child", "childLeaving", "childPulsate"]), rt = y2, g2 = ["center", "classes", "className"];
let rs = (e) => e, Sd, xd, wd, kd;
const Ha = 550, v2 = 80, S2 = Pr(Sd || (Sd = rs`
  0% {
    transform: scale(0);
    opacity: 0.1;
  }

  100% {
    transform: scale(1);
    opacity: 0.3;
  }
`)), x2 = Pr(xd || (xd = rs`
  0% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
`)), w2 = Pr(wd || (wd = rs`
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(0.92);
  }

  100% {
    transform: scale(1);
  }
`)), k2 = me("span", {
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
}), C2 = me(h2, {
  name: "MuiTouchRipple",
  slot: "Ripple"
})(kd || (kd = rs`
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
`), rt.rippleVisible, S2, Ha, ({
  theme: e
}) => e.transitions.easing.easeInOut, rt.ripplePulsate, ({
  theme: e
}) => e.transitions.duration.shorter, rt.child, rt.childLeaving, x2, Ha, ({
  theme: e
}) => e.transitions.easing.easeInOut, rt.childPulsate, w2, ({
  theme: e
}) => e.transitions.easing.easeInOut), E2 = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = tt({
    props: t,
    name: "MuiTouchRipple"
  }), {
    center: o = !1,
    classes: i = {},
    className: l
  } = r, s = H(r, g2), [a, u] = C.useState([]), d = C.useRef(0), f = C.useRef(null);
  C.useEffect(() => {
    f.current && (f.current(), f.current = null);
  }, [a]);
  const m = C.useRef(!1), v = Eh(), g = C.useRef(null), y = C.useRef(null), _ = C.useCallback((S) => {
    const {
      pulsate: E,
      rippleX: w,
      rippleY: x,
      rippleSize: $,
      cb: N
    } = S;
    u((O) => [...O, /* @__PURE__ */ T.jsx(C2, {
      classes: {
        ripple: oe(i.ripple, rt.ripple),
        rippleVisible: oe(i.rippleVisible, rt.rippleVisible),
        ripplePulsate: oe(i.ripplePulsate, rt.ripplePulsate),
        child: oe(i.child, rt.child),
        childLeaving: oe(i.childLeaving, rt.childLeaving),
        childPulsate: oe(i.childPulsate, rt.childPulsate)
      },
      timeout: Ha,
      pulsate: E,
      rippleX: w,
      rippleY: x,
      rippleSize: $
    }, d.current)]), d.current += 1, f.current = N;
  }, [i]), p = C.useCallback((S = {}, E = {}, w = () => {
  }) => {
    const {
      pulsate: x = !1,
      center: $ = o || E.pulsate,
      fakeElement: N = !1
      // For test purposes
    } = E;
    if ((S == null ? void 0 : S.type) === "mousedown" && m.current) {
      m.current = !1;
      return;
    }
    (S == null ? void 0 : S.type) === "touchstart" && (m.current = !0);
    const O = N ? null : y.current, b = O ? O.getBoundingClientRect() : {
      width: 0,
      height: 0,
      left: 0,
      top: 0
    };
    let A, L, W;
    if ($ || S === void 0 || S.clientX === 0 && S.clientY === 0 || !S.clientX && !S.touches)
      A = Math.round(b.width / 2), L = Math.round(b.height / 2);
    else {
      const {
        clientX: ee,
        clientY: ve
      } = S.touches && S.touches.length > 0 ? S.touches[0] : S;
      A = Math.round(ee - b.left), L = Math.round(ve - b.top);
    }
    if ($)
      W = Math.sqrt((2 * b.width ** 2 + b.height ** 2) / 3), W % 2 === 0 && (W += 1);
    else {
      const ee = Math.max(Math.abs((O ? O.clientWidth : 0) - A), A) * 2 + 2, ve = Math.max(Math.abs((O ? O.clientHeight : 0) - L), L) * 2 + 2;
      W = Math.sqrt(ee ** 2 + ve ** 2);
    }
    S != null && S.touches ? g.current === null && (g.current = () => {
      _({
        pulsate: x,
        rippleX: A,
        rippleY: L,
        rippleSize: W,
        cb: w
      });
    }, v.start(v2, () => {
      g.current && (g.current(), g.current = null);
    })) : _({
      pulsate: x,
      rippleX: A,
      rippleY: L,
      rippleSize: W,
      cb: w
    });
  }, [o, _, v]), c = C.useCallback(() => {
    p({}, {
      pulsate: !0
    });
  }, [p]), h = C.useCallback((S, E) => {
    if (v.clear(), (S == null ? void 0 : S.type) === "touchend" && g.current) {
      g.current(), g.current = null, v.start(0, () => {
        h(S, E);
      });
      return;
    }
    g.current = null, u((w) => w.length > 0 ? w.slice(1) : w), f.current = E;
  }, [v]);
  return C.useImperativeHandle(n, () => ({
    pulsate: c,
    start: p,
    stop: h
  }), [c, p, h]), /* @__PURE__ */ T.jsx(k2, k({
    className: oe(rt.root, i.root, l),
    ref: y
  }, s, {
    children: /* @__PURE__ */ T.jsx(m2, {
      component: null,
      exit: !0,
      children: a
    })
  }));
}), _2 = E2;
function P2(e) {
  return pt("MuiButtonBase", e);
}
const T2 = mt("MuiButtonBase", ["root", "disabled", "focusVisible"]), $2 = T2, R2 = ["action", "centerRipple", "children", "className", "component", "disabled", "disableRipple", "disableTouchRipple", "focusRipple", "focusVisibleClassName", "LinkComponent", "onBlur", "onClick", "onContextMenu", "onDragLeave", "onFocus", "onFocusVisible", "onKeyDown", "onKeyUp", "onMouseDown", "onMouseLeave", "onMouseUp", "onTouchEnd", "onTouchMove", "onTouchStart", "tabIndex", "TouchRippleProps", "touchRippleRef", "type"], O2 = (e) => {
  const {
    disabled: t,
    focusVisible: n,
    focusVisibleClassName: r,
    classes: o
  } = e, l = _t({
    root: ["root", t && "disabled", n && "focusVisible"]
  }, P2, o);
  return n && r && (l.root += ` ${r}`), l;
}, M2 = me("button", {
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
  [`&.${$2.disabled}`]: {
    pointerEvents: "none",
    // Disable link interactions
    cursor: "default"
  },
  "@media print": {
    colorAdjust: "exact"
  }
}), N2 = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = tt({
    props: t,
    name: "MuiButtonBase"
  }), {
    action: o,
    centerRipple: i = !1,
    children: l,
    className: s,
    component: a = "button",
    disabled: u = !1,
    disableRipple: d = !1,
    disableTouchRipple: f = !1,
    focusRipple: m = !1,
    LinkComponent: v = "a",
    onBlur: g,
    onClick: y,
    onContextMenu: _,
    onDragLeave: p,
    onFocus: c,
    onFocusVisible: h,
    onKeyDown: S,
    onKeyUp: E,
    onMouseDown: w,
    onMouseLeave: x,
    onMouseUp: $,
    onTouchEnd: N,
    onTouchMove: O,
    onTouchStart: b,
    tabIndex: A = 0,
    TouchRippleProps: L,
    touchRippleRef: W,
    type: ee
  } = r, ve = H(r, R2), he = C.useRef(null), R = C.useRef(null), z = _o(R, W), {
    isFocusVisibleRef: j,
    onFocus: q,
    onBlur: se,
    ref: Xt
  } = _h(), [_e, Pt] = C.useState(!1);
  u && _e && Pt(!1), C.useImperativeHandle(o, () => ({
    focusVisible: () => {
      Pt(!0), he.current.focus();
    }
  }), []);
  const [I, Se] = C.useState(!1);
  C.useEffect(() => {
    Se(!0);
  }, []);
  const yt = I && !d && !u;
  C.useEffect(() => {
    _e && m && !d && I && R.current.pulsate();
  }, [d, m, _e, I]);
  function Ie(D, Sc, n0 = f) {
    return Hr((xc) => (Sc && Sc(xc), !n0 && R.current && R.current[D](xc), !0));
  }
  const jn = Ie("start", w), Bo = Ie("stop", _), Vh = Ie("stop", p), Hh = Ie("stop", $), Kh = Ie("stop", (D) => {
    _e && D.preventDefault(), x && x(D);
  }), Gh = Ie("start", b), Qh = Ie("stop", N), Yh = Ie("stop", O), Xh = Ie("stop", (D) => {
    se(D), j.current === !1 && Pt(!1), g && g(D);
  }, !1), qh = Hr((D) => {
    he.current || (he.current = D.currentTarget), q(D), j.current === !0 && (Pt(!0), h && h(D)), c && c(D);
  }), os = () => {
    const D = he.current;
    return a && a !== "button" && !(D.tagName === "A" && D.href);
  }, is = C.useRef(!1), Zh = Hr((D) => {
    m && !is.current && _e && R.current && D.key === " " && (is.current = !0, R.current.stop(D, () => {
      R.current.start(D);
    })), D.target === D.currentTarget && os() && D.key === " " && D.preventDefault(), S && S(D), D.target === D.currentTarget && os() && D.key === "Enter" && !u && (D.preventDefault(), y && y(D));
  }), Jh = Hr((D) => {
    m && D.key === " " && R.current && _e && !D.defaultPrevented && (is.current = !1, R.current.stop(D, () => {
      R.current.pulsate(D);
    })), E && E(D), y && D.target === D.currentTarget && os() && D.key === " " && !D.defaultPrevented && y(D);
  });
  let Wo = a;
  Wo === "button" && (ve.href || ve.to) && (Wo = v);
  const Or = {};
  Wo === "button" ? (Or.type = ee === void 0 ? "button" : ee, Or.disabled = u) : (!ve.href && !ve.to && (Or.role = "button"), u && (Or["aria-disabled"] = u));
  const e0 = _o(n, Xt, he), vc = k({}, r, {
    centerRipple: i,
    component: a,
    disabled: u,
    disableRipple: d,
    disableTouchRipple: f,
    focusRipple: m,
    tabIndex: A,
    focusVisible: _e
  }), t0 = O2(vc);
  return /* @__PURE__ */ T.jsxs(M2, k({
    as: Wo,
    className: oe(t0.root, s),
    ownerState: vc,
    onBlur: Xh,
    onClick: y,
    onContextMenu: Bo,
    onFocus: qh,
    onKeyDown: Zh,
    onKeyUp: Jh,
    onMouseDown: jn,
    onMouseLeave: Kh,
    onMouseUp: Hh,
    onDragLeave: Vh,
    onTouchEnd: Qh,
    onTouchMove: Yh,
    onTouchStart: Gh,
    ref: e0,
    tabIndex: u ? -1 : A,
    type: ee
  }, Or, ve, {
    children: [l, yt ? (
      /* TouchRipple is only needed client-side, x2 boost on the server. */
      /* @__PURE__ */ T.jsx(_2, k({
        ref: z,
        center: i
      }, L))
    ) : null]
  }));
}), z2 = N2;
function L2(e) {
  return pt("MuiIconButton", e);
}
const I2 = mt("MuiIconButton", ["root", "disabled", "colorInherit", "colorPrimary", "colorSecondary", "colorError", "colorInfo", "colorSuccess", "colorWarning", "edgeStart", "edgeEnd", "sizeSmall", "sizeMedium", "sizeLarge"]), j2 = I2, A2 = ["edge", "children", "className", "color", "disabled", "disableFocusRipple", "size"], D2 = (e) => {
  const {
    classes: t,
    disabled: n,
    color: r,
    edge: o,
    size: i
  } = e, l = {
    root: ["root", n && "disabled", r !== "default" && `color${X(r)}`, o && `edge${X(o)}`, `size${X(i)}`]
  };
  return _t(l, L2, t);
}, F2 = me(z2, {
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
}) => k({
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
    backgroundColor: e.vars ? `rgba(${e.vars.palette.action.activeChannel} / ${e.vars.palette.action.hoverOpacity})` : rl(e.palette.action.active, e.palette.action.hoverOpacity),
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
  return k({}, t.color === "inherit" && {
    color: "inherit"
  }, t.color !== "inherit" && t.color !== "default" && k({
    color: r == null ? void 0 : r.main
  }, !t.disableRipple && {
    "&:hover": k({}, r && {
      backgroundColor: e.vars ? `rgba(${r.mainChannel} / ${e.vars.palette.action.hoverOpacity})` : rl(r.main, e.palette.action.hoverOpacity)
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
    [`&.${j2.disabled}`]: {
      backgroundColor: "transparent",
      color: (e.vars || e).palette.action.disabled
    }
  });
}), b2 = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = tt({
    props: t,
    name: "MuiIconButton"
  }), {
    edge: o = !1,
    children: i,
    className: l,
    color: s = "default",
    disabled: a = !1,
    disableFocusRipple: u = !1,
    size: d = "medium"
  } = r, f = H(r, A2), m = k({}, r, {
    edge: o,
    color: s,
    disabled: a,
    disableFocusRipple: u,
    size: d
  }), v = D2(m);
  return /* @__PURE__ */ T.jsx(F2, k({
    className: oe(v.root, l),
    centerRipple: !0,
    focusRipple: !u,
    disabled: a,
    ref: n
  }, f, {
    ownerState: m,
    children: i
  }));
}), bh = b2;
function B2(e) {
  return pt("MuiSvgIcon", e);
}
mt("MuiSvgIcon", ["root", "colorPrimary", "colorSecondary", "colorAction", "colorError", "colorDisabled", "fontSizeInherit", "fontSizeSmall", "fontSizeMedium", "fontSizeLarge"]);
const W2 = ["children", "className", "color", "component", "fontSize", "htmlColor", "inheritViewBox", "titleAccess", "viewBox"], U2 = (e) => {
  const {
    color: t,
    fontSize: n,
    classes: r
  } = e, o = {
    root: ["root", t !== "inherit" && `color${X(t)}`, `fontSize${X(n)}`]
  };
  return _t(o, B2, r);
}, V2 = me("svg", {
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
  var n, r, o, i, l, s, a, u, d, f, m, v, g;
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
      large: ((u = e.typography) == null || (d = u.pxToRem) == null ? void 0 : d.call(u, 35)) || "2.1875rem"
    }[t.fontSize],
    // TODO v5 deprecate, v6 remove for sx
    color: (f = (m = (e.vars || e).palette) == null || (m = m[t.color]) == null ? void 0 : m.main) != null ? f : {
      action: (v = (e.vars || e).palette) == null || (v = v.action) == null ? void 0 : v.active,
      disabled: (g = (e.vars || e).palette) == null || (g = g.action) == null ? void 0 : g.disabled,
      inherit: void 0
    }[t.color]
  };
}), Bh = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = tt({
    props: t,
    name: "MuiSvgIcon"
  }), {
    children: o,
    className: i,
    color: l = "inherit",
    component: s = "svg",
    fontSize: a = "medium",
    htmlColor: u,
    inheritViewBox: d = !1,
    titleAccess: f,
    viewBox: m = "0 0 24 24"
  } = r, v = H(r, W2), g = /* @__PURE__ */ C.isValidElement(o) && o.type === "svg", y = k({}, r, {
    color: l,
    component: s,
    fontSize: a,
    instanceFontSize: t.fontSize,
    inheritViewBox: d,
    viewBox: m,
    hasSvgAsChild: g
  }), _ = {};
  d || (_.viewBox = m);
  const p = U2(y);
  return /* @__PURE__ */ T.jsxs(V2, k({
    as: s,
    className: oe(p.root, i),
    focusable: "false",
    color: u,
    "aria-hidden": f ? void 0 : !0,
    role: f ? "img" : void 0,
    ref: n
  }, _, v, g && o.props, {
    ownerState: y,
    children: [g ? o.props.children : o, f ? /* @__PURE__ */ T.jsx("title", {
      children: f
    }) : null]
  }));
});
Bh.muiName = "SvgIcon";
const Cd = Bh;
function Rr(e, t) {
  function n(r, o) {
    return /* @__PURE__ */ T.jsx(Cd, k({
      "data-testid": `${t}Icon`,
      ref: o
    }, r, {
      children: e
    }));
  }
  return n.muiName = Cd.muiName, /* @__PURE__ */ C.memo(/* @__PURE__ */ C.forwardRef(n));
}
const H2 = Rr(/* @__PURE__ */ T.jsx("path", {
  d: "M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2, 4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0, 0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"
}), "SuccessOutlined"), K2 = Rr(/* @__PURE__ */ T.jsx("path", {
  d: "M12 5.99L19.53 19H4.47L12 5.99M12 2L1 21h22L12 2zm1 14h-2v2h2v-2zm0-6h-2v4h2v-4z"
}), "ReportProblemOutlined"), G2 = Rr(/* @__PURE__ */ T.jsx("path", {
  d: "M11 15h2v2h-2zm0-8h2v6h-2zm.99-5C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"
}), "ErrorOutline"), Q2 = Rr(/* @__PURE__ */ T.jsx("path", {
  d: "M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"
}), "InfoOutlined"), Y2 = Rr(/* @__PURE__ */ T.jsx("path", {
  d: "M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
}), "Close"), X2 = ["action", "children", "className", "closeText", "color", "components", "componentsProps", "icon", "iconMapping", "onClose", "role", "severity", "slotProps", "slots", "variant"], q2 = (e) => {
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
  return _t(i, o2, o);
}, Z2 = me(Dh, {
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
  const t = e.palette.mode === "light" ? ba : Ba, n = e.palette.mode === "light" ? Ba : ba;
  return k({}, e.typography.body2, {
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
        [`& .${gd.icon}`]: e.vars ? {
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
        [`& .${gd.icon}`]: e.vars ? {
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
      style: k({
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
}), J2 = me("div", {
  name: "MuiAlert",
  slot: "Icon",
  overridesResolver: (e, t) => t.icon
})({
  marginRight: 12,
  padding: "7px 0",
  display: "flex",
  fontSize: 22,
  opacity: 0.9
}), ek = me("div", {
  name: "MuiAlert",
  slot: "Message",
  overridesResolver: (e, t) => t.message
})({
  padding: "8px 0",
  minWidth: 0,
  overflow: "auto"
}), Ed = me("div", {
  name: "MuiAlert",
  slot: "Action",
  overridesResolver: (e, t) => t.action
})({
  display: "flex",
  alignItems: "flex-start",
  padding: "4px 0 0 16px",
  marginLeft: "auto",
  marginRight: -8
}), _d = {
  success: /* @__PURE__ */ T.jsx(H2, {
    fontSize: "inherit"
  }),
  warning: /* @__PURE__ */ T.jsx(K2, {
    fontSize: "inherit"
  }),
  error: /* @__PURE__ */ T.jsx(G2, {
    fontSize: "inherit"
  }),
  info: /* @__PURE__ */ T.jsx(Q2, {
    fontSize: "inherit"
  })
}, tk = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = tt({
    props: t,
    name: "MuiAlert"
  }), {
    action: o,
    children: i,
    className: l,
    closeText: s = "Close",
    color: a,
    components: u = {},
    componentsProps: d = {},
    icon: f,
    iconMapping: m = _d,
    onClose: v,
    role: g = "alert",
    severity: y = "success",
    slotProps: _ = {},
    slots: p = {},
    variant: c = "standard"
  } = r, h = H(r, X2), S = k({}, r, {
    color: a,
    severity: y,
    variant: c,
    colorSeverity: a || y
  }), E = q2(S), w = {
    slots: k({
      closeButton: u.CloseButton,
      closeIcon: u.CloseIcon
    }, p),
    slotProps: k({}, d, _)
  }, [x, $] = yd("closeButton", {
    elementType: bh,
    externalForwardedProps: w,
    ownerState: S
  }), [N, O] = yd("closeIcon", {
    elementType: Y2,
    externalForwardedProps: w,
    ownerState: S
  });
  return /* @__PURE__ */ T.jsxs(Z2, k({
    role: g,
    elevation: 0,
    ownerState: S,
    className: oe(E.root, l),
    ref: n
  }, h, {
    children: [f !== !1 ? /* @__PURE__ */ T.jsx(J2, {
      ownerState: S,
      className: E.icon,
      children: f || m[y] || _d[y]
    }) : null, /* @__PURE__ */ T.jsx(ek, {
      ownerState: S,
      className: E.message,
      children: i
    }), o != null ? /* @__PURE__ */ T.jsx(Ed, {
      ownerState: S,
      className: E.action,
      children: o
    }) : null, o == null && v ? /* @__PURE__ */ T.jsx(Ed, {
      ownerState: S,
      className: E.action,
      children: /* @__PURE__ */ T.jsx(x, k({
        size: "small",
        "aria-label": s,
        title: s,
        color: "inherit",
        onClick: v
      }, $, {
        children: /* @__PURE__ */ T.jsx(N, k({
          fontSize: "small"
        }, O))
      }))
    }) : null]
  }));
}), nk = tk, rk = mt("MuiBox", ["root"]), ok = rk, ik = fc(), lk = K1({
  themeId: vr,
  defaultTheme: ik,
  defaultClassName: ok.root,
  generateClassName: rc.generate
}), To = lk;
function sk(e) {
  return pt("MuiCard", e);
}
mt("MuiCard", ["root"]);
const ak = ["className", "raised"], uk = (e) => {
  const {
    classes: t
  } = e;
  return _t({
    root: ["root"]
  }, sk, t);
}, ck = me(Dh, {
  name: "MuiCard",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})(() => ({
  overflow: "hidden"
})), fk = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = tt({
    props: t,
    name: "MuiCard"
  }), {
    className: o,
    raised: i = !1
  } = r, l = H(r, ak), s = k({}, r, {
    raised: i
  }), a = uk(s);
  return /* @__PURE__ */ T.jsx(ck, k({
    className: oe(a.root, o),
    elevation: i ? 8 : void 0,
    ref: n,
    ownerState: s
  }, l));
}), hc = fk;
function dk(e) {
  return pt("MuiCardContent", e);
}
mt("MuiCardContent", ["root"]);
const pk = ["className", "component"], mk = (e) => {
  const {
    classes: t
  } = e;
  return _t({
    root: ["root"]
  }, dk, t);
}, hk = me("div", {
  name: "MuiCardContent",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})(() => ({
  padding: 16,
  "&:last-child": {
    paddingBottom: 24
  }
})), yk = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = tt({
    props: t,
    name: "MuiCardContent"
  }), {
    className: o,
    component: i = "div"
  } = r, l = H(r, pk), s = k({}, r, {
    component: i
  }), a = mk(s);
  return /* @__PURE__ */ T.jsx(hk, k({
    as: i,
    className: oe(a.root, o),
    ownerState: s,
    ref: n
  }, l));
}), yc = yk;
function Pd(e, t) {
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
const gk = {
  configure: (e) => {
    rc.configure(e);
  }
}, vk = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  capitalize: X,
  createChainedFunction: hS,
  createSvgIcon: Rr,
  debounce: yS,
  deprecatedPropType: gS,
  isMuiElement: vS,
  ownerDocument: wh,
  ownerWindow: SS,
  requirePropFactory: xS,
  setRef: kh,
  unstable_ClassNameGenerator: gk,
  unstable_useEnhancedEffect: lc,
  unstable_useId: Ch,
  unsupportedProp: kS,
  useControlled: CS,
  useEventCallback: Hr,
  useForkRef: _o,
  useIsFocusVisible: _h
}, Symbol.toStringTag, { value: "Module" }));
function Sk(e) {
  return pt("MuiCollapse", e);
}
mt("MuiCollapse", ["root", "horizontal", "vertical", "entered", "hidden", "wrapper", "wrapperInner"]);
const xk = ["addEndListener", "children", "className", "collapsedSize", "component", "easing", "in", "onEnter", "onEntered", "onEntering", "onExit", "onExited", "onExiting", "orientation", "style", "timeout", "TransitionComponent"], wk = (e) => {
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
  return _t(r, Sk, n);
}, kk = me("div", {
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
}) => k({
  height: 0,
  overflow: "hidden",
  transition: e.transitions.create("height")
}, t.orientation === "horizontal" && {
  height: "auto",
  width: 0,
  transition: e.transitions.create("width")
}, t.state === "entered" && k({
  height: "auto",
  overflow: "visible"
}, t.orientation === "horizontal" && {
  width: "auto"
}), t.state === "exited" && !t.in && t.collapsedSize === "0px" && {
  visibility: "hidden"
})), Ck = me("div", {
  name: "MuiCollapse",
  slot: "Wrapper",
  overridesResolver: (e, t) => t.wrapper
})(({
  ownerState: e
}) => k({
  // Hack to get children with a negative margin to not falsify the height computation.
  display: "flex",
  width: "100%"
}, e.orientation === "horizontal" && {
  width: "auto",
  height: "100%"
})), Ek = me("div", {
  name: "MuiCollapse",
  slot: "WrapperInner",
  overridesResolver: (e, t) => t.wrapperInner
})(({
  ownerState: e
}) => k({
  width: "100%"
}, e.orientation === "horizontal" && {
  width: "auto",
  height: "100%"
})), Wh = /* @__PURE__ */ C.forwardRef(function(t, n) {
  const r = tt({
    props: t,
    name: "MuiCollapse"
  }), {
    addEndListener: o,
    children: i,
    className: l,
    collapsedSize: s = "0px",
    component: a,
    easing: u,
    in: d,
    onEnter: f,
    onEntered: m,
    onEntering: v,
    onExit: g,
    onExited: y,
    onExiting: _,
    orientation: p = "vertical",
    style: c,
    timeout: h = jh.standard,
    // eslint-disable-next-line react/prop-types
    TransitionComponent: S = s2
  } = r, E = H(r, xk), w = k({}, r, {
    orientation: p,
    collapsedSize: s
  }), x = wk(w), $ = qx(), N = Eh(), O = C.useRef(null), b = C.useRef(), A = typeof s == "number" ? `${s}px` : s, L = p === "horizontal", W = L ? "width" : "height", ee = C.useRef(null), ve = _o(n, ee), he = (I) => (Se) => {
    if (I) {
      const yt = ee.current;
      Se === void 0 ? I(yt) : I(yt, Se);
    }
  }, R = () => O.current ? O.current[L ? "clientWidth" : "clientHeight"] : 0, z = he((I, Se) => {
    O.current && L && (O.current.style.position = "absolute"), I.style[W] = A, f && f(I, Se);
  }), j = he((I, Se) => {
    const yt = R();
    O.current && L && (O.current.style.position = "");
    const {
      duration: Ie,
      easing: jn
    } = Pd({
      style: c,
      timeout: h,
      easing: u
    }, {
      mode: "enter"
    });
    if (h === "auto") {
      const Bo = $.transitions.getAutoHeightDuration(yt);
      I.style.transitionDuration = `${Bo}ms`, b.current = Bo;
    } else
      I.style.transitionDuration = typeof Ie == "string" ? Ie : `${Ie}ms`;
    I.style[W] = `${yt}px`, I.style.transitionTimingFunction = jn, v && v(I, Se);
  }), q = he((I, Se) => {
    I.style[W] = "auto", m && m(I, Se);
  }), se = he((I) => {
    I.style[W] = `${R()}px`, g && g(I);
  }), Xt = he(y), _e = he((I) => {
    const Se = R(), {
      duration: yt,
      easing: Ie
    } = Pd({
      style: c,
      timeout: h,
      easing: u
    }, {
      mode: "exit"
    });
    if (h === "auto") {
      const jn = $.transitions.getAutoHeightDuration(Se);
      I.style.transitionDuration = `${jn}ms`, b.current = jn;
    } else
      I.style.transitionDuration = typeof yt == "string" ? yt : `${yt}ms`;
    I.style[W] = A, I.style.transitionTimingFunction = Ie, _ && _(I);
  }), Pt = (I) => {
    h === "auto" && N.start(b.current || 0, I), o && o(ee.current, I);
  };
  return /* @__PURE__ */ T.jsx(S, k({
    in: d,
    onEnter: z,
    onEntered: q,
    onEntering: j,
    onExit: se,
    onExited: Xt,
    onExiting: _e,
    addEndListener: Pt,
    nodeRef: ee,
    timeout: h === "auto" ? null : h
  }, E, {
    children: (I, Se) => /* @__PURE__ */ T.jsx(kk, k({
      as: a,
      className: oe(x.root, l, {
        entered: x.entered,
        exited: !d && A === "0px" && x.hidden
      }[I]),
      style: k({
        [L ? "minWidth" : "minHeight"]: A
      }, c),
      ref: ve
    }, Se, {
      // `ownerState` is set after `childProps` to override any existing `ownerState` property in `childProps`
      // that might have been forwarded from the Transition component.
      ownerState: k({}, w, {
        state: I
      }),
      children: /* @__PURE__ */ T.jsx(Ck, {
        ownerState: k({}, w, {
          state: I
        }),
        className: x.wrapper,
        ref: O,
        children: /* @__PURE__ */ T.jsx(Ek, {
          ownerState: k({}, w, {
            state: I
          }),
          className: x.wrapperInner,
          children: i
        })
      })
    }))
  }));
});
Wh.muiSupportAuto = !0;
const _k = Wh;
var gc = {}, bs = {};
const Pk = /* @__PURE__ */ Gt(vk);
var Td;
function Tk() {
  return Td || (Td = 1, function(e) {
    "use client";
    Object.defineProperty(e, "__esModule", {
      value: !0
    }), Object.defineProperty(e, "default", {
      enumerable: !0,
      get: function() {
        return t.createSvgIcon;
      }
    });
    var t = Pk;
  }(bs)), bs;
}
var $k = sc;
Object.defineProperty(gc, "__esModule", {
  value: !0
});
var Uh = gc.default = void 0, Rk = $k(Tk()), Ok = T;
Uh = gc.default = (0, Rk.default)(/* @__PURE__ */ (0, Ok.jsx)("path", {
  d: "M16.59 8.59 12 13.17 7.41 8.59 6 10l6 6 6-6z"
}), "ExpandMore");
const Mk = ({ devices: e }) => {
  const t = {
    Switches: e.filter((n) => {
      var r;
      return (r = n.model) == null ? void 0 : r.startsWith("MS");
    }),
    Wireless: e.filter((n) => {
      var r;
      return (r = n.model) == null ? void 0 : r.startsWith("MR");
    }),
    Cameras: e.filter((n) => {
      var r;
      return (r = n.model) == null ? void 0 : r.startsWith("MV");
    }),
    Routing: e.filter((n) => {
      var r;
      return (r = n.model) == null ? void 0 : r.startsWith("MX");
    })
  };
  return /* @__PURE__ */ T.jsx(To, { sx: { pl: 4, pt: 2 }, children: Object.entries(t).map(([n, r]) => r.length > 0 && /* @__PURE__ */ T.jsxs(To, { sx: { mb: 2 }, children: [
    /* @__PURE__ */ T.jsx(xr, { variant: "h6", children: n }),
    r.map((o) => /* @__PURE__ */ T.jsx(hc, { sx: { mb: 1, backgroundColor: "background.paper" }, children: /* @__PURE__ */ T.jsx(yc, { children: /* @__PURE__ */ T.jsx(xr, { children: o.name || o.mac }) }) }, o.serial))
  ] }, n)) });
}, Nk = me((e) => {
  const { expand: t, ...n } = e;
  return /* @__PURE__ */ T.jsx(bh, { ...n });
})(({ theme: e, expand: t }) => ({
  transform: t ? "rotate(180deg)" : "rotate(0deg)",
  marginLeft: "auto",
  transition: e.transitions.create("transform", {
    duration: e.transitions.duration.shortest
  })
})), zk = ({ data: e }) => {
  const { networks: t = [], devices: n = [] } = e, [r, o] = C.useState(!1), i = (l) => {
    o(r === l ? !1 : l);
  };
  return /* @__PURE__ */ T.jsx(To, { children: t.map((l) => {
    const s = n.filter((u) => u.networkId === l.id), a = r === l.id;
    return /* @__PURE__ */ T.jsxs(hc, { sx: { mb: 2 }, children: [
      /* @__PURE__ */ T.jsxs(
        To,
        {
          sx: { display: "flex", alignItems: "center", cursor: "pointer", p: 2 },
          onClick: () => i(l.id),
          children: [
            /* @__PURE__ */ T.jsx(xr, { variant: "h5", children: l.name }),
            /* @__PURE__ */ T.jsx(
              Nk,
              {
                expand: a,
                "aria-expanded": a,
                "aria-label": "show more",
                children: /* @__PURE__ */ T.jsx(Uh, {})
              }
            )
          ]
        }
      ),
      /* @__PURE__ */ T.jsx(_k, { in: a, timeout: "auto", unmountOnExit: !0, children: /* @__PURE__ */ T.jsx(yc, { children: /* @__PURE__ */ T.jsx(Mk, { devices: s }) }) })
    ] }, l.id);
  }) });
}, Lk = () => /* @__PURE__ */ T.jsx(hc, { sx: { mt: 4 }, children: /* @__PURE__ */ T.jsxs(yc, { children: [
  /* @__PURE__ */ T.jsx(xr, { variant: "h6", gutterBottom: !0, children: "Event Log" }),
  /* @__PURE__ */ T.jsx(xr, { children: "Integration-specific events will be displayed here." })
] }) });
const Ik = fc({
  palette: {
    mode: "dark"
  }
}), jk = ({ hass: e, config_entry_id: t }) => {
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
  }, [e, t]), /* @__PURE__ */ T.jsxs(Ew, { theme: Ik, children: [
    /* @__PURE__ */ T.jsx(Ow, {}),
    /* @__PURE__ */ T.jsxs(Nw, { maxWidth: "lg", sx: { mt: 4, mb: 4 }, children: [
      /* @__PURE__ */ T.jsx(xr, { variant: "h4", component: "h1", gutterBottom: !0, children: "Meraki Control" }),
      o && /* @__PURE__ */ T.jsx(To, { sx: { display: "flex", justifyContent: "center", p: 4 }, children: /* @__PURE__ */ T.jsx(Yw, {}) }),
      l && /* @__PURE__ */ T.jsx(nk, { severity: "error", sx: { mt: 2 }, children: l }),
      !o && !l && n && /* @__PURE__ */ T.jsxs(T.Fragment, { children: [
        /* @__PURE__ */ T.jsx(zk, { data: n }),
        /* @__PURE__ */ T.jsx(Lk, {})
      ] })
    ] })
  ] });
};
class Ak extends HTMLElement {
  constructor() {
    super(...arguments);
    Uo(this, "_root");
    Uo(this, "_hass");
    Uo(this, "_panel");
  }
  connectedCallback() {
    this._root = Ws.createRoot(this), this._render();
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
      /* @__PURE__ */ T.jsx(wt.StrictMode, { children: /* @__PURE__ */ T.jsx(jk, { hass: this._hass, config_entry_id: this._panel.config.config_entry_id }) })
    );
  }
}
customElements.define("meraki-panel", Ak);
