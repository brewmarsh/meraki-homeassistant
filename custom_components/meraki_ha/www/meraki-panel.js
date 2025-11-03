var o0 = Object.defineProperty;
var i0 = (e, t, n) => t in e ? o0(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var Ho = (e, t, n) => (i0(e, typeof t != "symbol" ? t + "" : t, n), n);
function l0(e, t) {
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
var Td = { exports: {} }, il = {}, Rd = { exports: {} }, A = {};
/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var No = Symbol.for("react.element"), s0 = Symbol.for("react.portal"), a0 = Symbol.for("react.fragment"), u0 = Symbol.for("react.strict_mode"), c0 = Symbol.for("react.profiler"), f0 = Symbol.for("react.provider"), d0 = Symbol.for("react.context"), p0 = Symbol.for("react.forward_ref"), m0 = Symbol.for("react.suspense"), h0 = Symbol.for("react.memo"), g0 = Symbol.for("react.lazy"), Sc = Symbol.iterator;
function y0(e) {
  return e === null || typeof e != "object" ? null : (e = Sc && e[Sc] || e["@@iterator"], typeof e == "function" ? e : null);
}
var Od = { isMounted: function() {
  return !1;
}, enqueueForceUpdate: function() {
}, enqueueReplaceState: function() {
}, enqueueSetState: function() {
} }, Md = Object.assign, Nd = {};
function Er(e, t, n) {
  this.props = e, this.context = t, this.refs = Nd, this.updater = n || Od;
}
Er.prototype.isReactComponent = {};
Er.prototype.setState = function(e, t) {
  if (typeof e != "object" && typeof e != "function" && e != null)
    throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
  this.updater.enqueueSetState(this, e, t, "setState");
};
Er.prototype.forceUpdate = function(e) {
  this.updater.enqueueForceUpdate(this, e, "forceUpdate");
};
function zd() {
}
zd.prototype = Er.prototype;
function Ga(e, t, n) {
  this.props = e, this.context = t, this.refs = Nd, this.updater = n || Od;
}
var Qa = Ga.prototype = new zd();
Qa.constructor = Ga;
Md(Qa, Er.prototype);
Qa.isPureReactComponent = !0;
var wc = Array.isArray, jd = Object.prototype.hasOwnProperty, Ya = { current: null }, Id = { key: !0, ref: !0, __self: !0, __source: !0 };
function Ld(e, t, n) {
  var r, o = {}, i = null, l = null;
  if (t != null)
    for (r in t.ref !== void 0 && (l = t.ref), t.key !== void 0 && (i = "" + t.key), t)
      jd.call(t, r) && !Id.hasOwnProperty(r) && (o[r] = t[r]);
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
  return { $$typeof: No, type: e, key: i, ref: l, props: o, _owner: Ya.current };
}
function v0(e, t) {
  return { $$typeof: No, type: e.type, key: t, ref: e.ref, props: e.props, _owner: e._owner };
}
function Xa(e) {
  return typeof e == "object" && e !== null && e.$$typeof === No;
}
function x0(e) {
  var t = { "=": "=0", ":": "=2" };
  return "$" + e.replace(/[=:]/g, function(n) {
    return t[n];
  });
}
var kc = /\/+/g;
function ss(e, t) {
  return typeof e == "object" && e !== null && e.key != null ? x0("" + e.key) : t.toString(36);
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
          case No:
          case s0:
            l = !0;
        }
    }
  if (l)
    return l = e, o = o(l), e = r === "" ? "." + ss(l, 0) : r, wc(o) ? (n = "", e != null && (n = e.replace(kc, "$&/") + "/"), di(o, t, n, "", function(u) {
      return u;
    })) : o != null && (Xa(o) && (o = v0(o, n + (!o.key || l && l.key === o.key ? "" : ("" + o.key).replace(kc, "$&/") + "/") + e)), t.push(o)), 1;
  if (l = 0, r = r === "" ? "." : r + ":", wc(e))
    for (var s = 0; s < e.length; s++) {
      i = e[s];
      var a = r + ss(i, s);
      l += di(i, t, n, a, o);
    }
  else if (a = y0(e), typeof a == "function")
    for (e = a.call(e), s = 0; !(i = e.next()).done; )
      i = i.value, a = r + ss(i, s++), l += di(i, t, n, a, o);
  else if (i === "object")
    throw t = String(e), Error("Objects are not valid as a React child (found: " + (t === "[object Object]" ? "object with keys {" + Object.keys(e).join(", ") + "}" : t) + "). If you meant to render a collection of children, use an array instead.");
  return l;
}
function Ko(e, t, n) {
  if (e == null)
    return e;
  var r = [], o = 0;
  return di(e, r, "", "", function(i) {
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
var De = { current: null }, pi = { transition: null }, w0 = { ReactCurrentDispatcher: De, ReactCurrentBatchConfig: pi, ReactCurrentOwner: Ya };
function Ad() {
  throw Error("act(...) is not supported in production builds of React.");
}
A.Children = { map: Ko, forEach: function(e, t, n) {
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
  if (!Xa(e))
    throw Error("React.Children.only expected to receive a single React element child.");
  return e;
} };
A.Component = Er;
A.Fragment = a0;
A.Profiler = c0;
A.PureComponent = Ga;
A.StrictMode = u0;
A.Suspense = m0;
A.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = w0;
A.act = Ad;
A.cloneElement = function(e, t, n) {
  if (e == null)
    throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + e + ".");
  var r = Md({}, e.props), o = e.key, i = e.ref, l = e._owner;
  if (t != null) {
    if (t.ref !== void 0 && (i = t.ref, l = Ya.current), t.key !== void 0 && (o = "" + t.key), e.type && e.type.defaultProps)
      var s = e.type.defaultProps;
    for (a in t)
      jd.call(t, a) && !Id.hasOwnProperty(a) && (r[a] = t[a] === void 0 && s !== void 0 ? s[a] : t[a]);
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
A.createContext = function(e) {
  return e = { $$typeof: d0, _currentValue: e, _currentValue2: e, _threadCount: 0, Provider: null, Consumer: null, _defaultValue: null, _globalName: null }, e.Provider = { $$typeof: f0, _context: e }, e.Consumer = e;
};
A.createElement = Ld;
A.createFactory = function(e) {
  var t = Ld.bind(null, e);
  return t.type = e, t;
};
A.createRef = function() {
  return { current: null };
};
A.forwardRef = function(e) {
  return { $$typeof: p0, render: e };
};
A.isValidElement = Xa;
A.lazy = function(e) {
  return { $$typeof: g0, _payload: { _status: -1, _result: e }, _init: S0 };
};
A.memo = function(e, t) {
  return { $$typeof: h0, type: e, compare: t === void 0 ? null : t };
};
A.startTransition = function(e) {
  var t = pi.transition;
  pi.transition = {};
  try {
    e();
  } finally {
    pi.transition = t;
  }
};
A.unstable_act = Ad;
A.useCallback = function(e, t) {
  return De.current.useCallback(e, t);
};
A.useContext = function(e) {
  return De.current.useContext(e);
};
A.useDebugValue = function() {
};
A.useDeferredValue = function(e) {
  return De.current.useDeferredValue(e);
};
A.useEffect = function(e, t) {
  return De.current.useEffect(e, t);
};
A.useId = function() {
  return De.current.useId();
};
A.useImperativeHandle = function(e, t, n) {
  return De.current.useImperativeHandle(e, t, n);
};
A.useInsertionEffect = function(e, t) {
  return De.current.useInsertionEffect(e, t);
};
A.useLayoutEffect = function(e, t) {
  return De.current.useLayoutEffect(e, t);
};
A.useMemo = function(e, t) {
  return De.current.useMemo(e, t);
};
A.useReducer = function(e, t, n) {
  return De.current.useReducer(e, t, n);
};
A.useRef = function(e) {
  return De.current.useRef(e);
};
A.useState = function(e) {
  return De.current.useState(e);
};
A.useSyncExternalStore = function(e, t, n) {
  return De.current.useSyncExternalStore(e, t, n);
};
A.useTransition = function() {
  return De.current.useTransition();
};
A.version = "18.3.1";
Rd.exports = A;
var k = Rd.exports;
const kt = /* @__PURE__ */ $d(k), Bs = /* @__PURE__ */ l0({
  __proto__: null,
  default: kt
}, [k]);
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var k0 = k, C0 = Symbol.for("react.element"), E0 = Symbol.for("react.fragment"), _0 = Object.prototype.hasOwnProperty, P0 = k0.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, $0 = { key: !0, ref: !0, __self: !0, __source: !0 };
function Dd(e, t, n) {
  var r, o = {}, i = null, l = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (r in t)
    _0.call(t, r) && !$0.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps)
    for (r in t = e.defaultProps, t)
      o[r] === void 0 && (o[r] = t[r]);
  return { $$typeof: C0, type: e, key: i, ref: l, props: o, _owner: P0.current };
}
il.Fragment = E0;
il.jsx = Dd;
il.jsxs = Dd;
Td.exports = il;
var _ = Td.exports, Ws = {}, Fd = { exports: {} }, qe = {}, bd = { exports: {} }, Bd = {};
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
    var j = R.length;
    R.push(N);
    e:
      for (; 0 < j; ) {
        var Y = j - 1 >>> 1, le = R[Y];
        if (0 < o(le, N))
          R[Y] = N, R[j] = le, j = Y;
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
    var N = R[0], j = R.pop();
    if (j !== N) {
      R[0] = j;
      e:
        for (var Y = 0, le = R.length, Xt = le >>> 1; Y < Xt; ) {
          var _e = 2 * (Y + 1) - 1, $t = R[_e], z = _e + 1, ye = R[z];
          if (0 > o($t, j))
            z < le && 0 > o(ye, $t) ? (R[Y] = ye, R[z] = j, Y = z) : (R[Y] = $t, R[_e] = j, Y = _e);
          else if (z < le && 0 > o(ye, j))
            R[Y] = ye, R[z] = j, Y = z;
          else
            break e;
        }
    }
    return N;
  }
  function o(R, N) {
    var j = R.sortIndex - N.sortIndex;
    return j !== 0 ? j : R.id - N.id;
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
  var a = [], u = [], c = 1, d = null, m = 3, v = !1, y = !1, g = !1, $ = typeof setTimeout == "function" ? setTimeout : null, p = typeof clearTimeout == "function" ? clearTimeout : null, f = typeof setImmediate < "u" ? setImmediate : null;
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
  function x(R) {
    if (g = !1, h(R), !y)
      if (n(a) !== null)
        y = !0, Ee(E);
      else {
        var N = n(u);
        N !== null && Se(x, N.startTime - R);
      }
  }
  function E(R, N) {
    y = !1, g && (g = !1, p(T), T = -1), v = !0;
    var j = m;
    try {
      for (h(N), d = n(a); d !== null && (!(d.expirationTime > N) || R && !F()); ) {
        var Y = d.callback;
        if (typeof Y == "function") {
          d.callback = null, m = d.priorityLevel;
          var le = Y(d.expirationTime <= N);
          N = e.unstable_now(), typeof le == "function" ? d.callback = le : d === n(a) && r(a), h(N);
        } else
          r(a);
        d = n(a);
      }
      if (d !== null)
        var Xt = !0;
      else {
        var _e = n(u);
        _e !== null && Se(x, _e.startTime - N), Xt = !1;
      }
      return Xt;
    } finally {
      d = null, m = j, v = !1;
    }
  }
  var w = !1, S = null, T = -1, I = 5, O = -1;
  function F() {
    return !(e.unstable_now() - O < I);
  }
  function U() {
    if (S !== null) {
      var R = e.unstable_now();
      O = R;
      var N = !0;
      try {
        N = S(!0, R);
      } finally {
        N ? b() : (w = !1, S = null);
      }
    } else
      w = !1;
  }
  var b;
  if (typeof f == "function")
    b = function() {
      f(U);
    };
  else if (typeof MessageChannel < "u") {
    var q = new MessageChannel(), ge = q.port2;
    q.port1.onmessage = U, b = function() {
      ge.postMessage(null);
    };
  } else
    b = function() {
      $(U, 0);
    };
  function Ee(R) {
    S = R, w || (w = !0, b());
  }
  function Se(R, N) {
    T = $(function() {
      R(e.unstable_now());
    }, N);
  }
  e.unstable_IdlePriority = 5, e.unstable_ImmediatePriority = 1, e.unstable_LowPriority = 4, e.unstable_NormalPriority = 3, e.unstable_Profiling = null, e.unstable_UserBlockingPriority = 2, e.unstable_cancelCallback = function(R) {
    R.callback = null;
  }, e.unstable_continueExecution = function() {
    y || v || (y = !0, Ee(E));
  }, e.unstable_forceFrameRate = function(R) {
    0 > R || 125 < R ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : I = 0 < R ? Math.floor(1e3 / R) : 5;
  }, e.unstable_getCurrentPriorityLevel = function() {
    return m;
  }, e.unstable_getFirstCallbackNode = function() {
    return n(a);
  }, e.unstable_next = function(R) {
    switch (m) {
      case 1:
      case 2:
      case 3:
        var N = 3;
        break;
      default:
        N = m;
    }
    var j = m;
    m = N;
    try {
      return R();
    } finally {
      m = j;
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
    var j = m;
    m = R;
    try {
      return N();
    } finally {
      m = j;
    }
  }, e.unstable_scheduleCallback = function(R, N, j) {
    var Y = e.unstable_now();
    switch (typeof j == "object" && j !== null ? (j = j.delay, j = typeof j == "number" && 0 < j ? Y + j : Y) : j = Y, R) {
      case 1:
        var le = -1;
        break;
      case 2:
        le = 250;
        break;
      case 5:
        le = 1073741823;
        break;
      case 4:
        le = 1e4;
        break;
      default:
        le = 5e3;
    }
    return le = j + le, R = { id: c++, callback: N, priorityLevel: R, startTime: j, expirationTime: le, sortIndex: -1 }, j > Y ? (R.sortIndex = j, t(u, R), n(a) === null && R === n(u) && (g ? (p(T), T = -1) : g = !0, Se(x, j - Y))) : (R.sortIndex = le, t(a, R), y || v || (y = !0, Ee(E))), R;
  }, e.unstable_shouldYield = F, e.unstable_wrapCallback = function(R) {
    var N = m;
    return function() {
      var j = m;
      m = N;
      try {
        return R.apply(this, arguments);
      } finally {
        m = j;
      }
    };
  };
})(Bd);
bd.exports = Bd;
var T0 = bd.exports;
/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var R0 = k, Ze = T0;
function P(e) {
  for (var t = "https://reactjs.org/docs/error-decoder.html?invariant=" + e, n = 1; n < arguments.length; n++)
    t += "&args[]=" + encodeURIComponent(arguments[n]);
  return "Minified React error #" + e + "; visit " + t + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
}
var Wd = /* @__PURE__ */ new Set(), so = {};
function An(e, t) {
  hr(e, t), hr(e + "Capture", t);
}
function hr(e, t) {
  for (so[e] = t, e = 0; e < t.length; e++)
    Wd.add(t[e]);
}
var Ut = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), Us = Object.prototype.hasOwnProperty, O0 = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, Cc = {}, Ec = {};
function M0(e) {
  return Us.call(Ec, e) ? !0 : Us.call(Cc, e) ? !1 : O0.test(e) ? Ec[e] = !0 : (Cc[e] = !0, !1);
}
function N0(e, t, n, r) {
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
function z0(e, t, n, r) {
  if (t === null || typeof t > "u" || N0(e, t, n, r))
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
var Za = /[\-:]([a-z])/g;
function qa(e) {
  return e[1].toUpperCase();
}
"accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(e) {
  var t = e.replace(
    Za,
    qa
  );
  Re[t] = new Fe(t, 1, !1, e, null, !1, !1);
});
"xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(e) {
  var t = e.replace(Za, qa);
  Re[t] = new Fe(t, 1, !1, e, "http://www.w3.org/1999/xlink", !1, !1);
});
["xml:base", "xml:lang", "xml:space"].forEach(function(e) {
  var t = e.replace(Za, qa);
  Re[t] = new Fe(t, 1, !1, e, "http://www.w3.org/XML/1998/namespace", !1, !1);
});
["tabIndex", "crossOrigin"].forEach(function(e) {
  Re[e] = new Fe(e, 1, !1, e.toLowerCase(), null, !1, !1);
});
Re.xlinkHref = new Fe("xlinkHref", 1, !1, "xlink:href", "http://www.w3.org/1999/xlink", !0, !1);
["src", "href", "action", "formAction"].forEach(function(e) {
  Re[e] = new Fe(e, 1, !1, e.toLowerCase(), null, !0, !0);
});
function Ja(e, t, n, r) {
  var o = Re.hasOwnProperty(t) ? Re[t] : null;
  (o !== null ? o.type !== 0 : r || !(2 < t.length) || t[0] !== "o" && t[0] !== "O" || t[1] !== "n" && t[1] !== "N") && (z0(t, n, o, r) && (n = null), r || o === null ? M0(t) && (n === null ? e.removeAttribute(t) : e.setAttribute(t, "" + n)) : o.mustUseProperty ? e[o.propertyName] = n === null ? o.type === 3 ? !1 : "" : n : (t = o.attributeName, r = o.attributeNamespace, n === null ? e.removeAttribute(t) : (o = o.type, n = o === 3 || o === 4 && n === !0 ? "" : "" + n, r ? e.setAttributeNS(r, t, n) : e.setAttribute(t, n))));
}
var Qt = R0.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, Go = Symbol.for("react.element"), Qn = Symbol.for("react.portal"), Yn = Symbol.for("react.fragment"), eu = Symbol.for("react.strict_mode"), Vs = Symbol.for("react.profiler"), Ud = Symbol.for("react.provider"), Vd = Symbol.for("react.context"), tu = Symbol.for("react.forward_ref"), Hs = Symbol.for("react.suspense"), Ks = Symbol.for("react.suspense_list"), nu = Symbol.for("react.memo"), Jt = Symbol.for("react.lazy"), Hd = Symbol.for("react.offscreen"), _c = Symbol.iterator;
function jr(e) {
  return e === null || typeof e != "object" ? null : (e = _c && e[_c] || e["@@iterator"], typeof e == "function" ? e : null);
}
var ie = Object.assign, as;
function Hr(e) {
  if (as === void 0)
    try {
      throw Error();
    } catch (n) {
      var t = n.stack.trim().match(/\n( *(at )?)/);
      as = t && t[1] || "";
    }
  return `
` + as + e;
}
var us = !1;
function cs(e, t) {
  if (!e || us)
    return "";
  us = !0;
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
    us = !1, Error.prepareStackTrace = n;
  }
  return (e = e ? e.displayName || e.name : "") ? Hr(e) : "";
}
function j0(e) {
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
      return e = cs(e.type, !1), e;
    case 11:
      return e = cs(e.type.render, !1), e;
    case 1:
      return e = cs(e.type, !0), e;
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
    case Yn:
      return "Fragment";
    case Qn:
      return "Portal";
    case Vs:
      return "Profiler";
    case eu:
      return "StrictMode";
    case Hs:
      return "Suspense";
    case Ks:
      return "SuspenseList";
  }
  if (typeof e == "object")
    switch (e.$$typeof) {
      case Vd:
        return (e.displayName || "Context") + ".Consumer";
      case Ud:
        return (e._context.displayName || "Context") + ".Provider";
      case tu:
        var t = e.render;
        return e = e.displayName, e || (e = t.displayName || t.name || "", e = e !== "" ? "ForwardRef(" + e + ")" : "ForwardRef"), e;
      case nu:
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
function I0(e) {
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
      return t === eu ? "StrictMode" : "Mode";
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
function gn(e) {
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
function Kd(e) {
  var t = e.type;
  return (e = e.nodeName) && e.toLowerCase() === "input" && (t === "checkbox" || t === "radio");
}
function L0(e) {
  var t = Kd(e) ? "checked" : "value", n = Object.getOwnPropertyDescriptor(e.constructor.prototype, t), r = "" + e[t];
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
  e._valueTracker || (e._valueTracker = L0(e));
}
function Gd(e) {
  if (!e)
    return !1;
  var t = e._valueTracker;
  if (!t)
    return !0;
  var n = t.getValue(), r = "";
  return e && (r = Kd(e) ? e.checked ? "true" : "false" : e.value), e = r, e !== n ? (t.setValue(e), !0) : !1;
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
  return ie({}, t, { defaultChecked: void 0, defaultValue: void 0, value: void 0, checked: n ?? e._wrapperState.initialChecked });
}
function Pc(e, t) {
  var n = t.defaultValue == null ? "" : t.defaultValue, r = t.checked != null ? t.checked : t.defaultChecked;
  n = gn(t.value != null ? t.value : n), e._wrapperState = { initialChecked: r, initialValue: n, controlled: t.type === "checkbox" || t.type === "radio" ? t.checked != null : t.value != null };
}
function Qd(e, t) {
  t = t.checked, t != null && Ja(e, "checked", t, !1);
}
function Ys(e, t) {
  Qd(e, t);
  var n = gn(t.value), r = t.type;
  if (n != null)
    r === "number" ? (n === 0 && e.value === "" || e.value != n) && (e.value = "" + n) : e.value !== "" + n && (e.value = "" + n);
  else if (r === "submit" || r === "reset") {
    e.removeAttribute("value");
    return;
  }
  t.hasOwnProperty("value") ? Xs(e, t.type, n) : t.hasOwnProperty("defaultValue") && Xs(e, t.type, gn(t.defaultValue)), t.checked == null && t.defaultChecked != null && (e.defaultChecked = !!t.defaultChecked);
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
var Kr = Array.isArray;
function lr(e, t, n, r) {
  if (e = e.options, t) {
    t = {};
    for (var o = 0; o < n.length; o++)
      t["$" + n[o]] = !0;
    for (n = 0; n < e.length; n++)
      o = t.hasOwnProperty("$" + e[n].value), e[n].selected !== o && (e[n].selected = o), o && r && (e[n].defaultSelected = !0);
  } else {
    for (n = "" + gn(n), t = null, o = 0; o < e.length; o++) {
      if (e[o].value === n) {
        e[o].selected = !0, r && (e[o].defaultSelected = !0);
        return;
      }
      t !== null || e[o].disabled || (t = e[o]);
    }
    t !== null && (t.selected = !0);
  }
}
function Zs(e, t) {
  if (t.dangerouslySetInnerHTML != null)
    throw Error(P(91));
  return ie({}, t, { value: void 0, defaultValue: void 0, children: "" + e._wrapperState.initialValue });
}
function Tc(e, t) {
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
  e._wrapperState = { initialValue: gn(n) };
}
function Yd(e, t) {
  var n = gn(t.value), r = gn(t.defaultValue);
  n != null && (n = "" + n, n !== e.value && (e.value = n), t.defaultValue == null && e.defaultValue !== n && (e.defaultValue = n)), r != null && (e.defaultValue = "" + r);
}
function Rc(e) {
  var t = e.textContent;
  t === e._wrapperState.initialValue && t !== "" && t !== null && (e.value = t);
}
function Xd(e) {
  switch (e) {
    case "svg":
      return "http://www.w3.org/2000/svg";
    case "math":
      return "http://www.w3.org/1998/Math/MathML";
    default:
      return "http://www.w3.org/1999/xhtml";
  }
}
function qs(e, t) {
  return e == null || e === "http://www.w3.org/1999/xhtml" ? Xd(t) : e === "http://www.w3.org/2000/svg" && t === "foreignObject" ? "http://www.w3.org/1999/xhtml" : e;
}
var Yo, Zd = function(e) {
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
function ao(e, t) {
  if (t) {
    var n = e.firstChild;
    if (n && n === e.lastChild && n.nodeType === 3) {
      n.nodeValue = t;
      return;
    }
  }
  e.textContent = t;
}
var Zr = {
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
}, A0 = ["Webkit", "ms", "Moz", "O"];
Object.keys(Zr).forEach(function(e) {
  A0.forEach(function(t) {
    t = t + e.charAt(0).toUpperCase() + e.substring(1), Zr[t] = Zr[e];
  });
});
function qd(e, t, n) {
  return t == null || typeof t == "boolean" || t === "" ? "" : n || typeof t != "number" || t === 0 || Zr.hasOwnProperty(e) && Zr[e] ? ("" + t).trim() : t + "px";
}
function Jd(e, t) {
  e = e.style;
  for (var n in t)
    if (t.hasOwnProperty(n)) {
      var r = n.indexOf("--") === 0, o = qd(n, t[n], r);
      n === "float" && (n = "cssFloat"), r ? e.setProperty(n, o) : e[n] = o;
    }
}
var D0 = ie({ menuitem: !0 }, { area: !0, base: !0, br: !0, col: !0, embed: !0, hr: !0, img: !0, input: !0, keygen: !0, link: !0, meta: !0, param: !0, source: !0, track: !0, wbr: !0 });
function Js(e, t) {
  if (t) {
    if (D0[e] && (t.children != null || t.dangerouslySetInnerHTML != null))
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
function ru(e) {
  return e = e.target || e.srcElement || window, e.correspondingUseElement && (e = e.correspondingUseElement), e.nodeType === 3 ? e.parentNode : e;
}
var na = null, sr = null, ar = null;
function Oc(e) {
  if (e = Io(e)) {
    if (typeof na != "function")
      throw Error(P(280));
    var t = e.stateNode;
    t && (t = cl(t), na(e.stateNode, e.type, t));
  }
}
function ep(e) {
  sr ? ar ? ar.push(e) : ar = [e] : sr = e;
}
function tp() {
  if (sr) {
    var e = sr, t = ar;
    if (ar = sr = null, Oc(e), t)
      for (e = 0; e < t.length; e++)
        Oc(t[e]);
  }
}
function np(e, t) {
  return e(t);
}
function rp() {
}
var fs = !1;
function op(e, t, n) {
  if (fs)
    return e(t, n);
  fs = !0;
  try {
    return np(e, t, n);
  } finally {
    fs = !1, (sr !== null || ar !== null) && (rp(), tp());
  }
}
function uo(e, t) {
  var n = e.stateNode;
  if (n === null)
    return null;
  var r = cl(n);
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
if (Ut)
  try {
    var Ir = {};
    Object.defineProperty(Ir, "passive", { get: function() {
      ra = !0;
    } }), window.addEventListener("test", Ir, Ir), window.removeEventListener("test", Ir, Ir);
  } catch {
    ra = !1;
  }
function F0(e, t, n, r, o, i, l, s, a) {
  var u = Array.prototype.slice.call(arguments, 3);
  try {
    t.apply(n, u);
  } catch (c) {
    this.onError(c);
  }
}
var qr = !1, Oi = null, Mi = !1, oa = null, b0 = { onError: function(e) {
  qr = !0, Oi = e;
} };
function B0(e, t, n, r, o, i, l, s, a) {
  qr = !1, Oi = null, F0.apply(b0, arguments);
}
function W0(e, t, n, r, o, i, l, s, a) {
  if (B0.apply(this, arguments), qr) {
    if (qr) {
      var u = Oi;
      qr = !1, Oi = null;
    } else
      throw Error(P(198));
    Mi || (Mi = !0, oa = u);
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
function ip(e) {
  if (e.tag === 13) {
    var t = e.memoizedState;
    if (t === null && (e = e.alternate, e !== null && (t = e.memoizedState)), t !== null)
      return t.dehydrated;
  }
  return null;
}
function Mc(e) {
  if (Dn(e) !== e)
    throw Error(P(188));
}
function U0(e) {
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
          return Mc(o), e;
        if (i === r)
          return Mc(o), t;
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
function lp(e) {
  return e = U0(e), e !== null ? sp(e) : null;
}
function sp(e) {
  if (e.tag === 5 || e.tag === 6)
    return e;
  for (e = e.child; e !== null; ) {
    var t = sp(e);
    if (t !== null)
      return t;
    e = e.sibling;
  }
  return null;
}
var ap = Ze.unstable_scheduleCallback, Nc = Ze.unstable_cancelCallback, V0 = Ze.unstable_shouldYield, H0 = Ze.unstable_requestPaint, ce = Ze.unstable_now, K0 = Ze.unstable_getCurrentPriorityLevel, ou = Ze.unstable_ImmediatePriority, up = Ze.unstable_UserBlockingPriority, Ni = Ze.unstable_NormalPriority, G0 = Ze.unstable_LowPriority, cp = Ze.unstable_IdlePriority, ll = null, zt = null;
function Q0(e) {
  if (zt && typeof zt.onCommitFiberRoot == "function")
    try {
      zt.onCommitFiberRoot(ll, e, void 0, (e.current.flags & 128) === 128);
    } catch {
    }
}
var Ct = Math.clz32 ? Math.clz32 : Z0, Y0 = Math.log, X0 = Math.LN2;
function Z0(e) {
  return e >>>= 0, e === 0 ? 32 : 31 - (Y0(e) / X0 | 0) | 0;
}
var Xo = 64, Zo = 4194304;
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
function zi(e, t) {
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
      n = 31 - Ct(t), o = 1 << n, r |= e[n], t &= ~o;
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
function J0(e, t) {
  for (var n = e.suspendedLanes, r = e.pingedLanes, o = e.expirationTimes, i = e.pendingLanes; 0 < i; ) {
    var l = 31 - Ct(i), s = 1 << l, a = o[l];
    a === -1 ? (!(s & n) || s & r) && (o[l] = q0(s, t)) : a <= t && (e.expiredLanes |= s), i &= ~s;
  }
}
function ia(e) {
  return e = e.pendingLanes & -1073741825, e !== 0 ? e : e & 1073741824 ? 1073741824 : 0;
}
function fp() {
  var e = Xo;
  return Xo <<= 1, !(Xo & 4194240) && (Xo = 64), e;
}
function ds(e) {
  for (var t = [], n = 0; 31 > n; n++)
    t.push(e);
  return t;
}
function zo(e, t, n) {
  e.pendingLanes |= t, t !== 536870912 && (e.suspendedLanes = 0, e.pingedLanes = 0), e = e.eventTimes, t = 31 - Ct(t), e[t] = n;
}
function eg(e, t) {
  var n = e.pendingLanes & ~t;
  e.pendingLanes = t, e.suspendedLanes = 0, e.pingedLanes = 0, e.expiredLanes &= t, e.mutableReadLanes &= t, e.entangledLanes &= t, t = e.entanglements;
  var r = e.eventTimes;
  for (e = e.expirationTimes; 0 < n; ) {
    var o = 31 - Ct(n), i = 1 << o;
    t[o] = 0, r[o] = -1, e[o] = -1, n &= ~i;
  }
}
function iu(e, t) {
  var n = e.entangledLanes |= t;
  for (e = e.entanglements; n; ) {
    var r = 31 - Ct(n), o = 1 << r;
    o & t | e[r] & t && (e[r] |= t), n &= ~o;
  }
}
var V = 0;
function dp(e) {
  return e &= -e, 1 < e ? 4 < e ? e & 268435455 ? 16 : 536870912 : 4 : 1;
}
var pp, lu, mp, hp, gp, la = !1, qo = [], sn = null, an = null, un = null, co = /* @__PURE__ */ new Map(), fo = /* @__PURE__ */ new Map(), tn = [], tg = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
function zc(e, t) {
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
      co.delete(t.pointerId);
      break;
    case "gotpointercapture":
    case "lostpointercapture":
      fo.delete(t.pointerId);
  }
}
function Lr(e, t, n, r, o, i) {
  return e === null || e.nativeEvent !== i ? (e = { blockedOn: t, domEventName: n, eventSystemFlags: r, nativeEvent: i, targetContainers: [o] }, t !== null && (t = Io(t), t !== null && lu(t)), e) : (e.eventSystemFlags |= r, t = e.targetContainers, o !== null && t.indexOf(o) === -1 && t.push(o), e);
}
function ng(e, t, n, r, o) {
  switch (t) {
    case "focusin":
      return sn = Lr(sn, e, t, n, r, o), !0;
    case "dragenter":
      return an = Lr(an, e, t, n, r, o), !0;
    case "mouseover":
      return un = Lr(un, e, t, n, r, o), !0;
    case "pointerover":
      var i = o.pointerId;
      return co.set(i, Lr(co.get(i) || null, e, t, n, r, o)), !0;
    case "gotpointercapture":
      return i = o.pointerId, fo.set(i, Lr(fo.get(i) || null, e, t, n, r, o)), !0;
  }
  return !1;
}
function yp(e) {
  var t = _n(e.target);
  if (t !== null) {
    var n = Dn(t);
    if (n !== null) {
      if (t = n.tag, t === 13) {
        if (t = ip(n), t !== null) {
          e.blockedOn = t, gp(e.priority, function() {
            mp(n);
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
function mi(e) {
  if (e.blockedOn !== null)
    return !1;
  for (var t = e.targetContainers; 0 < t.length; ) {
    var n = sa(e.domEventName, e.eventSystemFlags, t[0], e.nativeEvent);
    if (n === null) {
      n = e.nativeEvent;
      var r = new n.constructor(n.type, n);
      ta = r, n.target.dispatchEvent(r), ta = null;
    } else
      return t = Io(n), t !== null && lu(t), e.blockedOn = n, !1;
    t.shift();
  }
  return !0;
}
function jc(e, t, n) {
  mi(e) && n.delete(t);
}
function rg() {
  la = !1, sn !== null && mi(sn) && (sn = null), an !== null && mi(an) && (an = null), un !== null && mi(un) && (un = null), co.forEach(jc), fo.forEach(jc);
}
function Ar(e, t) {
  e.blockedOn === t && (e.blockedOn = null, la || (la = !0, Ze.unstable_scheduleCallback(Ze.unstable_NormalPriority, rg)));
}
function po(e) {
  function t(o) {
    return Ar(o, e);
  }
  if (0 < qo.length) {
    Ar(qo[0], e);
    for (var n = 1; n < qo.length; n++) {
      var r = qo[n];
      r.blockedOn === e && (r.blockedOn = null);
    }
  }
  for (sn !== null && Ar(sn, e), an !== null && Ar(an, e), un !== null && Ar(un, e), co.forEach(t), fo.forEach(t), n = 0; n < tn.length; n++)
    r = tn[n], r.blockedOn === e && (r.blockedOn = null);
  for (; 0 < tn.length && (n = tn[0], n.blockedOn === null); )
    yp(n), n.blockedOn === null && tn.shift();
}
var ur = Qt.ReactCurrentBatchConfig, ji = !0;
function og(e, t, n, r) {
  var o = V, i = ur.transition;
  ur.transition = null;
  try {
    V = 1, su(e, t, n, r);
  } finally {
    V = o, ur.transition = i;
  }
}
function ig(e, t, n, r) {
  var o = V, i = ur.transition;
  ur.transition = null;
  try {
    V = 4, su(e, t, n, r);
  } finally {
    V = o, ur.transition = i;
  }
}
function su(e, t, n, r) {
  if (ji) {
    var o = sa(e, t, n, r);
    if (o === null)
      ks(e, t, r, Ii, n), zc(e, r);
    else if (ng(o, e, t, n, r))
      r.stopPropagation();
    else if (zc(e, r), t & 4 && -1 < tg.indexOf(e)) {
      for (; o !== null; ) {
        var i = Io(o);
        if (i !== null && pp(i), i = sa(e, t, n, r), i === null && ks(e, t, r, Ii, n), i === o)
          break;
        o = i;
      }
      o !== null && r.stopPropagation();
    } else
      ks(e, t, r, null, n);
  }
}
var Ii = null;
function sa(e, t, n, r) {
  if (Ii = null, e = ru(r), e = _n(e), e !== null)
    if (t = Dn(e), t === null)
      e = null;
    else if (n = t.tag, n === 13) {
      if (e = ip(t), e !== null)
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
function vp(e) {
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
      switch (K0()) {
        case ou:
          return 1;
        case up:
          return 4;
        case Ni:
        case G0:
          return 16;
        case cp:
          return 536870912;
        default:
          return 16;
      }
    default:
      return 16;
  }
}
var on = null, au = null, hi = null;
function xp() {
  if (hi)
    return hi;
  var e, t = au, n = t.length, r, o = "value" in on ? on.value : on.textContent, i = o.length;
  for (e = 0; e < n && t[e] === o[e]; e++)
    ;
  var l = n - e;
  for (r = 1; r <= l && t[n - r] === o[i - r]; r++)
    ;
  return hi = o.slice(e, 1 < r ? 1 - r : void 0);
}
function gi(e) {
  var t = e.keyCode;
  return "charCode" in e ? (e = e.charCode, e === 0 && t === 13 && (e = 13)) : e = t, e === 10 && (e = 13), 32 <= e || e === 13 ? e : 0;
}
function Jo() {
  return !0;
}
function Ic() {
  return !1;
}
function Je(e) {
  function t(n, r, o, i, l) {
    this._reactName = n, this._targetInst = o, this.type = r, this.nativeEvent = i, this.target = l, this.currentTarget = null;
    for (var s in e)
      e.hasOwnProperty(s) && (n = e[s], this[s] = n ? n(i) : i[s]);
    return this.isDefaultPrevented = (i.defaultPrevented != null ? i.defaultPrevented : i.returnValue === !1) ? Jo : Ic, this.isPropagationStopped = Ic, this;
  }
  return ie(t.prototype, { preventDefault: function() {
    this.defaultPrevented = !0;
    var n = this.nativeEvent;
    n && (n.preventDefault ? n.preventDefault() : typeof n.returnValue != "unknown" && (n.returnValue = !1), this.isDefaultPrevented = Jo);
  }, stopPropagation: function() {
    var n = this.nativeEvent;
    n && (n.stopPropagation ? n.stopPropagation() : typeof n.cancelBubble != "unknown" && (n.cancelBubble = !0), this.isPropagationStopped = Jo);
  }, persist: function() {
  }, isPersistent: Jo }), t;
}
var _r = { eventPhase: 0, bubbles: 0, cancelable: 0, timeStamp: function(e) {
  return e.timeStamp || Date.now();
}, defaultPrevented: 0, isTrusted: 0 }, uu = Je(_r), jo = ie({}, _r, { view: 0, detail: 0 }), lg = Je(jo), ps, ms, Dr, sl = ie({}, jo, { screenX: 0, screenY: 0, clientX: 0, clientY: 0, pageX: 0, pageY: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, getModifierState: cu, button: 0, buttons: 0, relatedTarget: function(e) {
  return e.relatedTarget === void 0 ? e.fromElement === e.srcElement ? e.toElement : e.fromElement : e.relatedTarget;
}, movementX: function(e) {
  return "movementX" in e ? e.movementX : (e !== Dr && (Dr && e.type === "mousemove" ? (ps = e.screenX - Dr.screenX, ms = e.screenY - Dr.screenY) : ms = ps = 0, Dr = e), ps);
}, movementY: function(e) {
  return "movementY" in e ? e.movementY : ms;
} }), Lc = Je(sl), sg = ie({}, sl, { dataTransfer: 0 }), ag = Je(sg), ug = ie({}, jo, { relatedTarget: 0 }), hs = Je(ug), cg = ie({}, _r, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }), fg = Je(cg), dg = ie({}, _r, { clipboardData: function(e) {
  return "clipboardData" in e ? e.clipboardData : window.clipboardData;
} }), pg = Je(dg), mg = ie({}, _r, { data: 0 }), Ac = Je(mg), hg = {
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
}, gg = {
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
}, yg = { Alt: "altKey", Control: "ctrlKey", Meta: "metaKey", Shift: "shiftKey" };
function vg(e) {
  var t = this.nativeEvent;
  return t.getModifierState ? t.getModifierState(e) : (e = yg[e]) ? !!t[e] : !1;
}
function cu() {
  return vg;
}
var xg = ie({}, jo, { key: function(e) {
  if (e.key) {
    var t = hg[e.key] || e.key;
    if (t !== "Unidentified")
      return t;
  }
  return e.type === "keypress" ? (e = gi(e), e === 13 ? "Enter" : String.fromCharCode(e)) : e.type === "keydown" || e.type === "keyup" ? gg[e.keyCode] || "Unidentified" : "";
}, code: 0, location: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, repeat: 0, locale: 0, getModifierState: cu, charCode: function(e) {
  return e.type === "keypress" ? gi(e) : 0;
}, keyCode: function(e) {
  return e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
}, which: function(e) {
  return e.type === "keypress" ? gi(e) : e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
} }), Sg = Je(xg), wg = ie({}, sl, { pointerId: 0, width: 0, height: 0, pressure: 0, tangentialPressure: 0, tiltX: 0, tiltY: 0, twist: 0, pointerType: 0, isPrimary: 0 }), Dc = Je(wg), kg = ie({}, jo, { touches: 0, targetTouches: 0, changedTouches: 0, altKey: 0, metaKey: 0, ctrlKey: 0, shiftKey: 0, getModifierState: cu }), Cg = Je(kg), Eg = ie({}, _r, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }), _g = Je(Eg), Pg = ie({}, sl, {
  deltaX: function(e) {
    return "deltaX" in e ? e.deltaX : "wheelDeltaX" in e ? -e.wheelDeltaX : 0;
  },
  deltaY: function(e) {
    return "deltaY" in e ? e.deltaY : "wheelDeltaY" in e ? -e.wheelDeltaY : "wheelDelta" in e ? -e.wheelDelta : 0;
  },
  deltaZ: 0,
  deltaMode: 0
}), $g = Je(Pg), Tg = [9, 13, 27, 32], fu = Ut && "CompositionEvent" in window, Jr = null;
Ut && "documentMode" in document && (Jr = document.documentMode);
var Rg = Ut && "TextEvent" in window && !Jr, Sp = Ut && (!fu || Jr && 8 < Jr && 11 >= Jr), Fc = String.fromCharCode(32), bc = !1;
function wp(e, t) {
  switch (e) {
    case "keyup":
      return Tg.indexOf(t.keyCode) !== -1;
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
function kp(e) {
  return e = e.detail, typeof e == "object" && "data" in e ? e.data : null;
}
var Xn = !1;
function Og(e, t) {
  switch (e) {
    case "compositionend":
      return kp(t);
    case "keypress":
      return t.which !== 32 ? null : (bc = !0, Fc);
    case "textInput":
      return e = t.data, e === Fc && bc ? null : e;
    default:
      return null;
  }
}
function Mg(e, t) {
  if (Xn)
    return e === "compositionend" || !fu && wp(e, t) ? (e = xp(), hi = au = on = null, Xn = !1, e) : null;
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
      return Sp && t.locale !== "ko" ? null : t.data;
    default:
      return null;
  }
}
var Ng = { color: !0, date: !0, datetime: !0, "datetime-local": !0, email: !0, month: !0, number: !0, password: !0, range: !0, search: !0, tel: !0, text: !0, time: !0, url: !0, week: !0 };
function Bc(e) {
  var t = e && e.nodeName && e.nodeName.toLowerCase();
  return t === "input" ? !!Ng[e.type] : t === "textarea";
}
function Cp(e, t, n, r) {
  ep(r), t = Li(t, "onChange"), 0 < t.length && (n = new uu("onChange", "change", null, n, r), e.push({ event: n, listeners: t }));
}
var eo = null, mo = null;
function zg(e) {
  jp(e, 0);
}
function al(e) {
  var t = Jn(e);
  if (Gd(t))
    return e;
}
function jg(e, t) {
  if (e === "change")
    return t;
}
var Ep = !1;
if (Ut) {
  var gs;
  if (Ut) {
    var ys = "oninput" in document;
    if (!ys) {
      var Wc = document.createElement("div");
      Wc.setAttribute("oninput", "return;"), ys = typeof Wc.oninput == "function";
    }
    gs = ys;
  } else
    gs = !1;
  Ep = gs && (!document.documentMode || 9 < document.documentMode);
}
function Uc() {
  eo && (eo.detachEvent("onpropertychange", _p), mo = eo = null);
}
function _p(e) {
  if (e.propertyName === "value" && al(mo)) {
    var t = [];
    Cp(t, mo, e, ru(e)), op(zg, t);
  }
}
function Ig(e, t, n) {
  e === "focusin" ? (Uc(), eo = t, mo = n, eo.attachEvent("onpropertychange", _p)) : e === "focusout" && Uc();
}
function Lg(e) {
  if (e === "selectionchange" || e === "keyup" || e === "keydown")
    return al(mo);
}
function Ag(e, t) {
  if (e === "click")
    return al(t);
}
function Dg(e, t) {
  if (e === "input" || e === "change")
    return al(t);
}
function Fg(e, t) {
  return e === t && (e !== 0 || 1 / e === 1 / t) || e !== e && t !== t;
}
var _t = typeof Object.is == "function" ? Object.is : Fg;
function ho(e, t) {
  if (_t(e, t))
    return !0;
  if (typeof e != "object" || e === null || typeof t != "object" || t === null)
    return !1;
  var n = Object.keys(e), r = Object.keys(t);
  if (n.length !== r.length)
    return !1;
  for (r = 0; r < n.length; r++) {
    var o = n[r];
    if (!Us.call(t, o) || !_t(e[o], t[o]))
      return !1;
  }
  return !0;
}
function Vc(e) {
  for (; e && e.firstChild; )
    e = e.firstChild;
  return e;
}
function Hc(e, t) {
  var n = Vc(e);
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
    n = Vc(n);
  }
}
function Pp(e, t) {
  return e && t ? e === t ? !0 : e && e.nodeType === 3 ? !1 : t && t.nodeType === 3 ? Pp(e, t.parentNode) : "contains" in e ? e.contains(t) : e.compareDocumentPosition ? !!(e.compareDocumentPosition(t) & 16) : !1 : !1;
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
function du(e) {
  var t = e && e.nodeName && e.nodeName.toLowerCase();
  return t && (t === "input" && (e.type === "text" || e.type === "search" || e.type === "tel" || e.type === "url" || e.type === "password") || t === "textarea" || e.contentEditable === "true");
}
function bg(e) {
  var t = $p(), n = e.focusedElem, r = e.selectionRange;
  if (t !== n && n && n.ownerDocument && Pp(n.ownerDocument.documentElement, n)) {
    if (r !== null && du(n)) {
      if (t = r.start, e = r.end, e === void 0 && (e = t), "selectionStart" in n)
        n.selectionStart = t, n.selectionEnd = Math.min(e, n.value.length);
      else if (e = (t = n.ownerDocument || document) && t.defaultView || window, e.getSelection) {
        e = e.getSelection();
        var o = n.textContent.length, i = Math.min(r.start, o);
        r = r.end === void 0 ? i : Math.min(r.end, o), !e.extend && i > r && (o = r, r = i, i = o), o = Hc(n, i);
        var l = Hc(
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
var Bg = Ut && "documentMode" in document && 11 >= document.documentMode, Zn = null, aa = null, to = null, ua = !1;
function Kc(e, t, n) {
  var r = n.window === n ? n.document : n.nodeType === 9 ? n : n.ownerDocument;
  ua || Zn == null || Zn !== Ri(r) || (r = Zn, "selectionStart" in r && du(r) ? r = { start: r.selectionStart, end: r.selectionEnd } : (r = (r.ownerDocument && r.ownerDocument.defaultView || window).getSelection(), r = { anchorNode: r.anchorNode, anchorOffset: r.anchorOffset, focusNode: r.focusNode, focusOffset: r.focusOffset }), to && ho(to, r) || (to = r, r = Li(aa, "onSelect"), 0 < r.length && (t = new uu("onSelect", "select", null, t, n), e.push({ event: t, listeners: r }), t.target = Zn)));
}
function ei(e, t) {
  var n = {};
  return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit" + e] = "webkit" + t, n["Moz" + e] = "moz" + t, n;
}
var qn = { animationend: ei("Animation", "AnimationEnd"), animationiteration: ei("Animation", "AnimationIteration"), animationstart: ei("Animation", "AnimationStart"), transitionend: ei("Transition", "TransitionEnd") }, vs = {}, Tp = {};
Ut && (Tp = document.createElement("div").style, "AnimationEvent" in window || (delete qn.animationend.animation, delete qn.animationiteration.animation, delete qn.animationstart.animation), "TransitionEvent" in window || delete qn.transitionend.transition);
function ul(e) {
  if (vs[e])
    return vs[e];
  if (!qn[e])
    return e;
  var t = qn[e], n;
  for (n in t)
    if (t.hasOwnProperty(n) && n in Tp)
      return vs[e] = t[n];
  return e;
}
var Rp = ul("animationend"), Op = ul("animationiteration"), Mp = ul("animationstart"), Np = ul("transitionend"), zp = /* @__PURE__ */ new Map(), Gc = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
function vn(e, t) {
  zp.set(e, t), An(t, [e]);
}
for (var xs = 0; xs < Gc.length; xs++) {
  var Ss = Gc[xs], Wg = Ss.toLowerCase(), Ug = Ss[0].toUpperCase() + Ss.slice(1);
  vn(Wg, "on" + Ug);
}
vn(Rp, "onAnimationEnd");
vn(Op, "onAnimationIteration");
vn(Mp, "onAnimationStart");
vn("dblclick", "onDoubleClick");
vn("focusin", "onFocus");
vn("focusout", "onBlur");
vn(Np, "onTransitionEnd");
hr("onMouseEnter", ["mouseout", "mouseover"]);
hr("onMouseLeave", ["mouseout", "mouseover"]);
hr("onPointerEnter", ["pointerout", "pointerover"]);
hr("onPointerLeave", ["pointerout", "pointerover"]);
An("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" "));
An("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));
An("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]);
An("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" "));
An("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" "));
An("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
var Qr = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), Vg = new Set("cancel close invalid load scroll toggle".split(" ").concat(Qr));
function Qc(e, t, n) {
  var r = e.type || "unknown-event";
  e.currentTarget = n, W0(r, t, void 0, e), e.currentTarget = null;
}
function jp(e, t) {
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
          Qc(o, s, u), i = a;
        }
      else
        for (l = 0; l < r.length; l++) {
          if (s = r[l], a = s.instance, u = s.currentTarget, s = s.listener, a !== i && o.isPropagationStopped())
            break e;
          Qc(o, s, u), i = a;
        }
    }
  }
  if (Mi)
    throw e = oa, Mi = !1, oa = null, e;
}
function X(e, t) {
  var n = t[ma];
  n === void 0 && (n = t[ma] = /* @__PURE__ */ new Set());
  var r = e + "__bubble";
  n.has(r) || (Ip(t, e, 2, !1), n.add(r));
}
function ws(e, t, n) {
  var r = 0;
  t && (r |= 4), Ip(n, e, r, t);
}
var ti = "_reactListening" + Math.random().toString(36).slice(2);
function go(e) {
  if (!e[ti]) {
    e[ti] = !0, Wd.forEach(function(n) {
      n !== "selectionchange" && (Vg.has(n) || ws(n, !1, e), ws(n, !0, e));
    });
    var t = e.nodeType === 9 ? e : e.ownerDocument;
    t === null || t[ti] || (t[ti] = !0, ws("selectionchange", !1, t));
  }
}
function Ip(e, t, n, r) {
  switch (vp(t)) {
    case 1:
      var o = og;
      break;
    case 4:
      o = ig;
      break;
    default:
      o = su;
  }
  n = o.bind(null, t, n, e), o = void 0, !ra || t !== "touchstart" && t !== "touchmove" && t !== "wheel" || (o = !0), r ? o !== void 0 ? e.addEventListener(t, n, { capture: !0, passive: o }) : e.addEventListener(t, n, !0) : o !== void 0 ? e.addEventListener(t, n, { passive: o }) : e.addEventListener(t, n, !1);
}
function ks(e, t, n, r, o) {
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
            if (l = _n(s), l === null)
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
  op(function() {
    var u = i, c = ru(n), d = [];
    e: {
      var m = zp.get(e);
      if (m !== void 0) {
        var v = uu, y = e;
        switch (e) {
          case "keypress":
            if (gi(n) === 0)
              break e;
          case "keydown":
          case "keyup":
            v = Sg;
            break;
          case "focusin":
            y = "focus", v = hs;
            break;
          case "focusout":
            y = "blur", v = hs;
            break;
          case "beforeblur":
          case "afterblur":
            v = hs;
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
            v = Lc;
            break;
          case "drag":
          case "dragend":
          case "dragenter":
          case "dragexit":
          case "dragleave":
          case "dragover":
          case "dragstart":
          case "drop":
            v = ag;
            break;
          case "touchcancel":
          case "touchend":
          case "touchmove":
          case "touchstart":
            v = Cg;
            break;
          case Rp:
          case Op:
          case Mp:
            v = fg;
            break;
          case Np:
            v = _g;
            break;
          case "scroll":
            v = lg;
            break;
          case "wheel":
            v = $g;
            break;
          case "copy":
          case "cut":
          case "paste":
            v = pg;
            break;
          case "gotpointercapture":
          case "lostpointercapture":
          case "pointercancel":
          case "pointerdown":
          case "pointermove":
          case "pointerout":
          case "pointerover":
          case "pointerup":
            v = Dc;
        }
        var g = (t & 4) !== 0, $ = !g && e === "scroll", p = g ? m !== null ? m + "Capture" : null : m;
        g = [];
        for (var f = u, h; f !== null; ) {
          h = f;
          var x = h.stateNode;
          if (h.tag === 5 && x !== null && (h = x, p !== null && (x = uo(f, p), x != null && g.push(yo(f, x, h)))), $)
            break;
          f = f.return;
        }
        0 < g.length && (m = new v(m, y, null, n, c), d.push({ event: m, listeners: g }));
      }
    }
    if (!(t & 7)) {
      e: {
        if (m = e === "mouseover" || e === "pointerover", v = e === "mouseout" || e === "pointerout", m && n !== ta && (y = n.relatedTarget || n.fromElement) && (_n(y) || y[Vt]))
          break e;
        if ((v || m) && (m = c.window === c ? c : (m = c.ownerDocument) ? m.defaultView || m.parentWindow : window, v ? (y = n.relatedTarget || n.toElement, v = u, y = y ? _n(y) : null, y !== null && ($ = Dn(y), y !== $ || y.tag !== 5 && y.tag !== 6) && (y = null)) : (v = null, y = u), v !== y)) {
          if (g = Lc, x = "onMouseLeave", p = "onMouseEnter", f = "mouse", (e === "pointerout" || e === "pointerover") && (g = Dc, x = "onPointerLeave", p = "onPointerEnter", f = "pointer"), $ = v == null ? m : Jn(v), h = y == null ? m : Jn(y), m = new g(x, f + "leave", v, n, c), m.target = $, m.relatedTarget = h, x = null, _n(c) === u && (g = new g(p, f + "enter", y, n, c), g.target = h, g.relatedTarget = $, x = g), $ = x, v && y)
            t: {
              for (g = v, p = y, f = 0, h = g; h; h = bn(h))
                f++;
              for (h = 0, x = p; x; x = bn(x))
                h++;
              for (; 0 < f - h; )
                g = bn(g), f--;
              for (; 0 < h - f; )
                p = bn(p), h--;
              for (; f--; ) {
                if (g === p || p !== null && g === p.alternate)
                  break t;
                g = bn(g), p = bn(p);
              }
              g = null;
            }
          else
            g = null;
          v !== null && Yc(d, m, v, g, !1), y !== null && $ !== null && Yc(d, $, y, g, !0);
        }
      }
      e: {
        if (m = u ? Jn(u) : window, v = m.nodeName && m.nodeName.toLowerCase(), v === "select" || v === "input" && m.type === "file")
          var E = jg;
        else if (Bc(m))
          if (Ep)
            E = Dg;
          else {
            E = Lg;
            var w = Ig;
          }
        else
          (v = m.nodeName) && v.toLowerCase() === "input" && (m.type === "checkbox" || m.type === "radio") && (E = Ag);
        if (E && (E = E(e, u))) {
          Cp(d, E, n, c);
          break e;
        }
        w && w(e, m, u), e === "focusout" && (w = m._wrapperState) && w.controlled && m.type === "number" && Xs(m, "number", m.value);
      }
      switch (w = u ? Jn(u) : window, e) {
        case "focusin":
          (Bc(w) || w.contentEditable === "true") && (Zn = w, aa = u, to = null);
          break;
        case "focusout":
          to = aa = Zn = null;
          break;
        case "mousedown":
          ua = !0;
          break;
        case "contextmenu":
        case "mouseup":
        case "dragend":
          ua = !1, Kc(d, n, c);
          break;
        case "selectionchange":
          if (Bg)
            break;
        case "keydown":
        case "keyup":
          Kc(d, n, c);
      }
      var S;
      if (fu)
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
        Xn ? wp(e, n) && (T = "onCompositionEnd") : e === "keydown" && n.keyCode === 229 && (T = "onCompositionStart");
      T && (Sp && n.locale !== "ko" && (Xn || T !== "onCompositionStart" ? T === "onCompositionEnd" && Xn && (S = xp()) : (on = c, au = "value" in on ? on.value : on.textContent, Xn = !0)), w = Li(u, T), 0 < w.length && (T = new Ac(T, e, null, n, c), d.push({ event: T, listeners: w }), S ? T.data = S : (S = kp(n), S !== null && (T.data = S)))), (S = Rg ? Og(e, n) : Mg(e, n)) && (u = Li(u, "onBeforeInput"), 0 < u.length && (c = new Ac("onBeforeInput", "beforeinput", null, n, c), d.push({ event: c, listeners: u }), c.data = S));
    }
    jp(d, t);
  });
}
function yo(e, t, n) {
  return { instance: e, listener: t, currentTarget: n };
}
function Li(e, t) {
  for (var n = t + "Capture", r = []; e !== null; ) {
    var o = e, i = o.stateNode;
    o.tag === 5 && i !== null && (o = i, i = uo(e, n), i != null && r.unshift(yo(e, i, o)), i = uo(e, t), i != null && r.push(yo(e, i, o))), e = e.return;
  }
  return r;
}
function bn(e) {
  if (e === null)
    return null;
  do
    e = e.return;
  while (e && e.tag !== 5);
  return e || null;
}
function Yc(e, t, n, r, o) {
  for (var i = t._reactName, l = []; n !== null && n !== r; ) {
    var s = n, a = s.alternate, u = s.stateNode;
    if (a !== null && a === r)
      break;
    s.tag === 5 && u !== null && (s = u, o ? (a = uo(n, i), a != null && l.unshift(yo(n, a, s))) : o || (a = uo(n, i), a != null && l.push(yo(n, a, s)))), n = n.return;
  }
  l.length !== 0 && e.push({ event: t, listeners: l });
}
var Hg = /\r\n?/g, Kg = /\u0000|\uFFFD/g;
function Xc(e) {
  return (typeof e == "string" ? e : "" + e).replace(Hg, `
`).replace(Kg, "");
}
function ni(e, t, n) {
  if (t = Xc(t), Xc(e) !== t && n)
    throw Error(P(425));
}
function Ai() {
}
var ca = null, fa = null;
function da(e, t) {
  return e === "textarea" || e === "noscript" || typeof t.children == "string" || typeof t.children == "number" || typeof t.dangerouslySetInnerHTML == "object" && t.dangerouslySetInnerHTML !== null && t.dangerouslySetInnerHTML.__html != null;
}
var pa = typeof setTimeout == "function" ? setTimeout : void 0, Gg = typeof clearTimeout == "function" ? clearTimeout : void 0, Zc = typeof Promise == "function" ? Promise : void 0, Qg = typeof queueMicrotask == "function" ? queueMicrotask : typeof Zc < "u" ? function(e) {
  return Zc.resolve(null).then(e).catch(Yg);
} : pa;
function Yg(e) {
  setTimeout(function() {
    throw e;
  });
}
function Cs(e, t) {
  var n = t, r = 0;
  do {
    var o = n.nextSibling;
    if (e.removeChild(n), o && o.nodeType === 8)
      if (n = o.data, n === "/$") {
        if (r === 0) {
          e.removeChild(o), po(t);
          return;
        }
        r--;
      } else
        n !== "$" && n !== "$?" && n !== "$!" || r++;
    n = o;
  } while (n);
  po(t);
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
function qc(e) {
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
var Pr = Math.random().toString(36).slice(2), Nt = "__reactFiber$" + Pr, vo = "__reactProps$" + Pr, Vt = "__reactContainer$" + Pr, ma = "__reactEvents$" + Pr, Xg = "__reactListeners$" + Pr, Zg = "__reactHandles$" + Pr;
function _n(e) {
  var t = e[Nt];
  if (t)
    return t;
  for (var n = e.parentNode; n; ) {
    if (t = n[Vt] || n[Nt]) {
      if (n = t.alternate, t.child !== null || n !== null && n.child !== null)
        for (e = qc(e); e !== null; ) {
          if (n = e[Nt])
            return n;
          e = qc(e);
        }
      return t;
    }
    e = n, n = e.parentNode;
  }
  return null;
}
function Io(e) {
  return e = e[Nt] || e[Vt], !e || e.tag !== 5 && e.tag !== 6 && e.tag !== 13 && e.tag !== 3 ? null : e;
}
function Jn(e) {
  if (e.tag === 5 || e.tag === 6)
    return e.stateNode;
  throw Error(P(33));
}
function cl(e) {
  return e[vo] || null;
}
var ha = [], er = -1;
function xn(e) {
  return { current: e };
}
function Z(e) {
  0 > er || (e.current = ha[er], ha[er] = null, er--);
}
function Q(e, t) {
  er++, ha[er] = e.current, e.current = t;
}
var yn = {}, je = xn(yn), We = xn(!1), Nn = yn;
function gr(e, t) {
  var n = e.type.contextTypes;
  if (!n)
    return yn;
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
  Z(We), Z(je);
}
function Jc(e, t, n) {
  if (je.current !== yn)
    throw Error(P(168));
  Q(je, t), Q(We, n);
}
function Lp(e, t, n) {
  var r = e.stateNode;
  if (t = t.childContextTypes, typeof r.getChildContext != "function")
    return n;
  r = r.getChildContext();
  for (var o in r)
    if (!(o in t))
      throw Error(P(108, I0(e) || "Unknown", o));
  return ie({}, n, r);
}
function Fi(e) {
  return e = (e = e.stateNode) && e.__reactInternalMemoizedMergedChildContext || yn, Nn = je.current, Q(je, e), Q(We, We.current), !0;
}
function ef(e, t, n) {
  var r = e.stateNode;
  if (!r)
    throw Error(P(169));
  n ? (e = Lp(e, t, Nn), r.__reactInternalMemoizedMergedChildContext = e, Z(We), Z(je), Q(je, e)) : Z(We), Q(We, n);
}
var Dt = null, fl = !1, Es = !1;
function Ap(e) {
  Dt === null ? Dt = [e] : Dt.push(e);
}
function qg(e) {
  fl = !0, Ap(e);
}
function Sn() {
  if (!Es && Dt !== null) {
    Es = !0;
    var e = 0, t = V;
    try {
      var n = Dt;
      for (V = 1; e < n.length; e++) {
        var r = n[e];
        do
          r = r(!0);
        while (r !== null);
      }
      Dt = null, fl = !1;
    } catch (o) {
      throw Dt !== null && (Dt = Dt.slice(e + 1)), ap(ou, Sn), o;
    } finally {
      V = t, Es = !1;
    }
  }
  return null;
}
var tr = [], nr = 0, bi = null, Bi = 0, it = [], lt = 0, zn = null, Ft = 1, bt = "";
function wn(e, t) {
  tr[nr++] = Bi, tr[nr++] = bi, bi = e, Bi = t;
}
function Dp(e, t, n) {
  it[lt++] = Ft, it[lt++] = bt, it[lt++] = zn, zn = e;
  var r = Ft;
  e = bt;
  var o = 32 - Ct(r) - 1;
  r &= ~(1 << o), n += 1;
  var i = 32 - Ct(t) + o;
  if (30 < i) {
    var l = o - o % 5;
    i = (r & (1 << l) - 1).toString(32), r >>= l, o -= l, Ft = 1 << 32 - Ct(t) + o | n << o | r, bt = i + e;
  } else
    Ft = 1 << i | n << o | r, bt = e;
}
function pu(e) {
  e.return !== null && (wn(e, 1), Dp(e, 1, 0));
}
function mu(e) {
  for (; e === bi; )
    bi = tr[--nr], tr[nr] = null, Bi = tr[--nr], tr[nr] = null;
  for (; e === zn; )
    zn = it[--lt], it[lt] = null, bt = it[--lt], it[lt] = null, Ft = it[--lt], it[lt] = null;
}
var Ye = null, Qe = null, ee = !1, wt = null;
function Fp(e, t) {
  var n = at(5, null, null, 0);
  n.elementType = "DELETED", n.stateNode = t, n.return = e, t = e.deletions, t === null ? (e.deletions = [n], e.flags |= 16) : t.push(n);
}
function tf(e, t) {
  switch (e.tag) {
    case 5:
      var n = e.type;
      return t = t.nodeType !== 1 || n.toLowerCase() !== t.nodeName.toLowerCase() ? null : t, t !== null ? (e.stateNode = t, Ye = e, Qe = cn(t.firstChild), !0) : !1;
    case 6:
      return t = e.pendingProps === "" || t.nodeType !== 3 ? null : t, t !== null ? (e.stateNode = t, Ye = e, Qe = null, !0) : !1;
    case 13:
      return t = t.nodeType !== 8 ? null : t, t !== null ? (n = zn !== null ? { id: Ft, overflow: bt } : null, e.memoizedState = { dehydrated: t, treeContext: n, retryLane: 1073741824 }, n = at(18, null, null, 0), n.stateNode = t, n.return = e, e.child = n, Ye = e, Qe = null, !0) : !1;
    default:
      return !1;
  }
}
function ga(e) {
  return (e.mode & 1) !== 0 && (e.flags & 128) === 0;
}
function ya(e) {
  if (ee) {
    var t = Qe;
    if (t) {
      var n = t;
      if (!tf(e, t)) {
        if (ga(e))
          throw Error(P(418));
        t = cn(n.nextSibling);
        var r = Ye;
        t && tf(e, t) ? Fp(r, n) : (e.flags = e.flags & -4097 | 2, ee = !1, Ye = e);
      }
    } else {
      if (ga(e))
        throw Error(P(418));
      e.flags = e.flags & -4097 | 2, ee = !1, Ye = e;
    }
  }
}
function nf(e) {
  for (e = e.return; e !== null && e.tag !== 5 && e.tag !== 3 && e.tag !== 13; )
    e = e.return;
  Ye = e;
}
function ri(e) {
  if (e !== Ye)
    return !1;
  if (!ee)
    return nf(e), ee = !0, !1;
  var t;
  if ((t = e.tag !== 3) && !(t = e.tag !== 5) && (t = e.type, t = t !== "head" && t !== "body" && !da(e.type, e.memoizedProps)), t && (t = Qe)) {
    if (ga(e))
      throw bp(), Error(P(418));
    for (; t; )
      Fp(e, t), t = cn(t.nextSibling);
  }
  if (nf(e), e.tag === 13) {
    if (e = e.memoizedState, e = e !== null ? e.dehydrated : null, !e)
      throw Error(P(317));
    e: {
      for (e = e.nextSibling, t = 0; e; ) {
        if (e.nodeType === 8) {
          var n = e.data;
          if (n === "/$") {
            if (t === 0) {
              Qe = cn(e.nextSibling);
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
    Qe = Ye ? cn(e.stateNode.nextSibling) : null;
  return !0;
}
function bp() {
  for (var e = Qe; e; )
    e = cn(e.nextSibling);
}
function yr() {
  Qe = Ye = null, ee = !1;
}
function hu(e) {
  wt === null ? wt = [e] : wt.push(e);
}
var Jg = Qt.ReactCurrentBatchConfig;
function Fr(e, t, n) {
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
function rf(e) {
  var t = e._init;
  return t(e._payload);
}
function Bp(e) {
  function t(p, f) {
    if (e) {
      var h = p.deletions;
      h === null ? (p.deletions = [f], p.flags |= 16) : h.push(f);
    }
  }
  function n(p, f) {
    if (!e)
      return null;
    for (; f !== null; )
      t(p, f), f = f.sibling;
    return null;
  }
  function r(p, f) {
    for (p = /* @__PURE__ */ new Map(); f !== null; )
      f.key !== null ? p.set(f.key, f) : p.set(f.index, f), f = f.sibling;
    return p;
  }
  function o(p, f) {
    return p = mn(p, f), p.index = 0, p.sibling = null, p;
  }
  function i(p, f, h) {
    return p.index = h, e ? (h = p.alternate, h !== null ? (h = h.index, h < f ? (p.flags |= 2, f) : h) : (p.flags |= 2, f)) : (p.flags |= 1048576, f);
  }
  function l(p) {
    return e && p.alternate === null && (p.flags |= 2), p;
  }
  function s(p, f, h, x) {
    return f === null || f.tag !== 6 ? (f = Ms(h, p.mode, x), f.return = p, f) : (f = o(f, h), f.return = p, f);
  }
  function a(p, f, h, x) {
    var E = h.type;
    return E === Yn ? c(p, f, h.props.children, x, h.key) : f !== null && (f.elementType === E || typeof E == "object" && E !== null && E.$$typeof === Jt && rf(E) === f.type) ? (x = o(f, h.props), x.ref = Fr(p, f, h), x.return = p, x) : (x = Ci(h.type, h.key, h.props, null, p.mode, x), x.ref = Fr(p, f, h), x.return = p, x);
  }
  function u(p, f, h, x) {
    return f === null || f.tag !== 4 || f.stateNode.containerInfo !== h.containerInfo || f.stateNode.implementation !== h.implementation ? (f = Ns(h, p.mode, x), f.return = p, f) : (f = o(f, h.children || []), f.return = p, f);
  }
  function c(p, f, h, x, E) {
    return f === null || f.tag !== 7 ? (f = On(h, p.mode, x, E), f.return = p, f) : (f = o(f, h), f.return = p, f);
  }
  function d(p, f, h) {
    if (typeof f == "string" && f !== "" || typeof f == "number")
      return f = Ms("" + f, p.mode, h), f.return = p, f;
    if (typeof f == "object" && f !== null) {
      switch (f.$$typeof) {
        case Go:
          return h = Ci(f.type, f.key, f.props, null, p.mode, h), h.ref = Fr(p, null, f), h.return = p, h;
        case Qn:
          return f = Ns(f, p.mode, h), f.return = p, f;
        case Jt:
          var x = f._init;
          return d(p, x(f._payload), h);
      }
      if (Kr(f) || jr(f))
        return f = On(f, p.mode, h, null), f.return = p, f;
      oi(p, f);
    }
    return null;
  }
  function m(p, f, h, x) {
    var E = f !== null ? f.key : null;
    if (typeof h == "string" && h !== "" || typeof h == "number")
      return E !== null ? null : s(p, f, "" + h, x);
    if (typeof h == "object" && h !== null) {
      switch (h.$$typeof) {
        case Go:
          return h.key === E ? a(p, f, h, x) : null;
        case Qn:
          return h.key === E ? u(p, f, h, x) : null;
        case Jt:
          return E = h._init, m(
            p,
            f,
            E(h._payload),
            x
          );
      }
      if (Kr(h) || jr(h))
        return E !== null ? null : c(p, f, h, x, null);
      oi(p, h);
    }
    return null;
  }
  function v(p, f, h, x, E) {
    if (typeof x == "string" && x !== "" || typeof x == "number")
      return p = p.get(h) || null, s(f, p, "" + x, E);
    if (typeof x == "object" && x !== null) {
      switch (x.$$typeof) {
        case Go:
          return p = p.get(x.key === null ? h : x.key) || null, a(f, p, x, E);
        case Qn:
          return p = p.get(x.key === null ? h : x.key) || null, u(f, p, x, E);
        case Jt:
          var w = x._init;
          return v(p, f, h, w(x._payload), E);
      }
      if (Kr(x) || jr(x))
        return p = p.get(h) || null, c(f, p, x, E, null);
      oi(f, x);
    }
    return null;
  }
  function y(p, f, h, x) {
    for (var E = null, w = null, S = f, T = f = 0, I = null; S !== null && T < h.length; T++) {
      S.index > T ? (I = S, S = null) : I = S.sibling;
      var O = m(p, S, h[T], x);
      if (O === null) {
        S === null && (S = I);
        break;
      }
      e && S && O.alternate === null && t(p, S), f = i(O, f, T), w === null ? E = O : w.sibling = O, w = O, S = I;
    }
    if (T === h.length)
      return n(p, S), ee && wn(p, T), E;
    if (S === null) {
      for (; T < h.length; T++)
        S = d(p, h[T], x), S !== null && (f = i(S, f, T), w === null ? E = S : w.sibling = S, w = S);
      return ee && wn(p, T), E;
    }
    for (S = r(p, S); T < h.length; T++)
      I = v(S, p, T, h[T], x), I !== null && (e && I.alternate !== null && S.delete(I.key === null ? T : I.key), f = i(I, f, T), w === null ? E = I : w.sibling = I, w = I);
    return e && S.forEach(function(F) {
      return t(p, F);
    }), ee && wn(p, T), E;
  }
  function g(p, f, h, x) {
    var E = jr(h);
    if (typeof E != "function")
      throw Error(P(150));
    if (h = E.call(h), h == null)
      throw Error(P(151));
    for (var w = E = null, S = f, T = f = 0, I = null, O = h.next(); S !== null && !O.done; T++, O = h.next()) {
      S.index > T ? (I = S, S = null) : I = S.sibling;
      var F = m(p, S, O.value, x);
      if (F === null) {
        S === null && (S = I);
        break;
      }
      e && S && F.alternate === null && t(p, S), f = i(F, f, T), w === null ? E = F : w.sibling = F, w = F, S = I;
    }
    if (O.done)
      return n(
        p,
        S
      ), ee && wn(p, T), E;
    if (S === null) {
      for (; !O.done; T++, O = h.next())
        O = d(p, O.value, x), O !== null && (f = i(O, f, T), w === null ? E = O : w.sibling = O, w = O);
      return ee && wn(p, T), E;
    }
    for (S = r(p, S); !O.done; T++, O = h.next())
      O = v(S, p, T, O.value, x), O !== null && (e && O.alternate !== null && S.delete(O.key === null ? T : O.key), f = i(O, f, T), w === null ? E = O : w.sibling = O, w = O);
    return e && S.forEach(function(U) {
      return t(p, U);
    }), ee && wn(p, T), E;
  }
  function $(p, f, h, x) {
    if (typeof h == "object" && h !== null && h.type === Yn && h.key === null && (h = h.props.children), typeof h == "object" && h !== null) {
      switch (h.$$typeof) {
        case Go:
          e: {
            for (var E = h.key, w = f; w !== null; ) {
              if (w.key === E) {
                if (E = h.type, E === Yn) {
                  if (w.tag === 7) {
                    n(p, w.sibling), f = o(w, h.props.children), f.return = p, p = f;
                    break e;
                  }
                } else if (w.elementType === E || typeof E == "object" && E !== null && E.$$typeof === Jt && rf(E) === w.type) {
                  n(p, w.sibling), f = o(w, h.props), f.ref = Fr(p, w, h), f.return = p, p = f;
                  break e;
                }
                n(p, w);
                break;
              } else
                t(p, w);
              w = w.sibling;
            }
            h.type === Yn ? (f = On(h.props.children, p.mode, x, h.key), f.return = p, p = f) : (x = Ci(h.type, h.key, h.props, null, p.mode, x), x.ref = Fr(p, f, h), x.return = p, p = x);
          }
          return l(p);
        case Qn:
          e: {
            for (w = h.key; f !== null; ) {
              if (f.key === w)
                if (f.tag === 4 && f.stateNode.containerInfo === h.containerInfo && f.stateNode.implementation === h.implementation) {
                  n(p, f.sibling), f = o(f, h.children || []), f.return = p, p = f;
                  break e;
                } else {
                  n(p, f);
                  break;
                }
              else
                t(p, f);
              f = f.sibling;
            }
            f = Ns(h, p.mode, x), f.return = p, p = f;
          }
          return l(p);
        case Jt:
          return w = h._init, $(p, f, w(h._payload), x);
      }
      if (Kr(h))
        return y(p, f, h, x);
      if (jr(h))
        return g(p, f, h, x);
      oi(p, h);
    }
    return typeof h == "string" && h !== "" || typeof h == "number" ? (h = "" + h, f !== null && f.tag === 6 ? (n(p, f.sibling), f = o(f, h), f.return = p, p = f) : (n(p, f), f = Ms(h, p.mode, x), f.return = p, p = f), l(p)) : n(p, f);
  }
  return $;
}
var vr = Bp(!0), Wp = Bp(!1), Wi = xn(null), Ui = null, rr = null, gu = null;
function yu() {
  gu = rr = Ui = null;
}
function vu(e) {
  var t = Wi.current;
  Z(Wi), e._currentValue = t;
}
function va(e, t, n) {
  for (; e !== null; ) {
    var r = e.alternate;
    if ((e.childLanes & t) !== t ? (e.childLanes |= t, r !== null && (r.childLanes |= t)) : r !== null && (r.childLanes & t) !== t && (r.childLanes |= t), e === n)
      break;
    e = e.return;
  }
}
function cr(e, t) {
  Ui = e, gu = rr = null, e = e.dependencies, e !== null && e.firstContext !== null && (e.lanes & t && (Be = !0), e.firstContext = null);
}
function ct(e) {
  var t = e._currentValue;
  if (gu !== e)
    if (e = { context: e, memoizedValue: t, next: null }, rr === null) {
      if (Ui === null)
        throw Error(P(308));
      rr = e, Ui.dependencies = { lanes: 0, firstContext: e };
    } else
      rr = rr.next = e;
  return t;
}
var Pn = null;
function xu(e) {
  Pn === null ? Pn = [e] : Pn.push(e);
}
function Up(e, t, n, r) {
  var o = t.interleaved;
  return o === null ? (n.next = n, xu(t)) : (n.next = o.next, o.next = n), t.interleaved = n, Ht(e, r);
}
function Ht(e, t) {
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
function Vp(e, t) {
  e = e.updateQueue, t.updateQueue === e && (t.updateQueue = { baseState: e.baseState, firstBaseUpdate: e.firstBaseUpdate, lastBaseUpdate: e.lastBaseUpdate, shared: e.shared, effects: e.effects });
}
function Wt(e, t) {
  return { eventTime: e, lane: t, tag: 0, payload: null, callback: null, next: null };
}
function fn(e, t, n) {
  var r = e.updateQueue;
  if (r === null)
    return null;
  if (r = r.shared, D & 2) {
    var o = r.pending;
    return o === null ? t.next = t : (t.next = o.next, o.next = t), r.pending = t, Ht(e, n);
  }
  return o = r.interleaved, o === null ? (t.next = t, xu(r)) : (t.next = o.next, o.next = t), r.interleaved = t, Ht(e, n);
}
function yi(e, t, n) {
  if (t = t.updateQueue, t !== null && (t = t.shared, (n & 4194240) !== 0)) {
    var r = t.lanes;
    r &= e.pendingLanes, n |= r, t.lanes = n, iu(e, n);
  }
}
function of(e, t) {
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
    var c = e.alternate;
    c !== null && (c = c.updateQueue, s = c.lastBaseUpdate, s !== l && (s === null ? c.firstBaseUpdate = u : s.next = u, c.lastBaseUpdate = a));
  }
  if (i !== null) {
    var d = o.baseState;
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
                d = y.call(v, d, m);
                break e;
              }
              d = y;
              break e;
            case 3:
              y.flags = y.flags & -65537 | 128;
            case 0:
              if (y = g.payload, m = typeof y == "function" ? y.call(v, d, m) : y, m == null)
                break e;
              d = ie({}, d, m);
              break e;
            case 2:
              en = !0;
          }
        }
        s.callback !== null && s.lane !== 0 && (e.flags |= 64, m = o.effects, m === null ? o.effects = [s] : m.push(s));
      } else
        v = { eventTime: v, lane: m, tag: s.tag, payload: s.payload, callback: s.callback, next: null }, c === null ? (u = c = v, a = d) : c = c.next = v, l |= m;
      if (s = s.next, s === null) {
        if (s = o.shared.pending, s === null)
          break;
        m = s, s = m.next, m.next = null, o.lastBaseUpdate = m, o.shared.pending = null;
      }
    } while (1);
    if (c === null && (a = d), o.baseState = a, o.firstBaseUpdate = u, o.lastBaseUpdate = c, t = o.shared.interleaved, t !== null) {
      o = t;
      do
        l |= o.lane, o = o.next;
      while (o !== t);
    } else
      i === null && (o.shared.lanes = 0);
    In |= l, e.lanes = l, e.memoizedState = d;
  }
}
function lf(e, t, n) {
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
var Lo = {}, jt = xn(Lo), xo = xn(Lo), So = xn(Lo);
function $n(e) {
  if (e === Lo)
    throw Error(P(174));
  return e;
}
function wu(e, t) {
  switch (Q(So, t), Q(xo, e), Q(jt, Lo), e = t.nodeType, e) {
    case 9:
    case 11:
      t = (t = t.documentElement) ? t.namespaceURI : qs(null, "");
      break;
    default:
      e = e === 8 ? t.parentNode : t, t = e.namespaceURI || null, e = e.tagName, t = qs(t, e);
  }
  Z(jt), Q(jt, t);
}
function xr() {
  Z(jt), Z(xo), Z(So);
}
function Hp(e) {
  $n(So.current);
  var t = $n(jt.current), n = qs(t, e.type);
  t !== n && (Q(xo, e), Q(jt, n));
}
function ku(e) {
  xo.current === e && (Z(jt), Z(xo));
}
var te = xn(0);
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
var _s = [];
function Cu() {
  for (var e = 0; e < _s.length; e++)
    _s[e]._workInProgressVersionPrimary = null;
  _s.length = 0;
}
var vi = Qt.ReactCurrentDispatcher, Ps = Qt.ReactCurrentBatchConfig, jn = 0, re = null, ve = null, we = null, Ki = !1, no = !1, wo = 0, ey = 0;
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
function _u(e, t, n, r, o, i) {
  if (jn = i, re = t, t.memoizedState = null, t.updateQueue = null, t.lanes = 0, vi.current = e === null || e.memoizedState === null ? oy : iy, e = n(r, o), no) {
    i = 0;
    do {
      if (no = !1, wo = 0, 25 <= i)
        throw Error(P(301));
      i += 1, we = ve = null, t.updateQueue = null, vi.current = ly, e = n(r, o);
    } while (no);
  }
  if (vi.current = Gi, t = ve !== null && ve.next !== null, jn = 0, we = ve = re = null, Ki = !1, t)
    throw Error(P(300));
  return e;
}
function Pu() {
  var e = wo !== 0;
  return wo = 0, e;
}
function Rt() {
  var e = { memoizedState: null, baseState: null, baseQueue: null, queue: null, next: null };
  return we === null ? re.memoizedState = we = e : we = we.next = e, we;
}
function ft() {
  if (ve === null) {
    var e = re.alternate;
    e = e !== null ? e.memoizedState : null;
  } else
    e = ve.next;
  var t = we === null ? re.memoizedState : we.next;
  if (t !== null)
    we = t, ve = e;
  else {
    if (e === null)
      throw Error(P(310));
    ve = e, e = { memoizedState: ve.memoizedState, baseState: ve.baseState, baseQueue: ve.baseQueue, queue: ve.queue, next: null }, we === null ? re.memoizedState = we = e : we = we.next = e;
  }
  return we;
}
function ko(e, t) {
  return typeof t == "function" ? t(e) : t;
}
function $s(e) {
  var t = ft(), n = t.queue;
  if (n === null)
    throw Error(P(311));
  n.lastRenderedReducer = e;
  var r = ve, o = r.baseQueue, i = n.pending;
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
      if ((jn & c) === c)
        a !== null && (a = a.next = { lane: 0, action: u.action, hasEagerState: u.hasEagerState, eagerState: u.eagerState, next: null }), r = u.hasEagerState ? u.eagerState : e(r, u.action);
      else {
        var d = {
          lane: c,
          action: u.action,
          hasEagerState: u.hasEagerState,
          eagerState: u.eagerState,
          next: null
        };
        a === null ? (s = a = d, l = r) : a = a.next = d, re.lanes |= c, In |= c;
      }
      u = u.next;
    } while (u !== null && u !== i);
    a === null ? l = r : a.next = s, _t(r, t.memoizedState) || (Be = !0), t.memoizedState = r, t.baseState = l, t.baseQueue = a, n.lastRenderedState = r;
  }
  if (e = n.interleaved, e !== null) {
    o = e;
    do
      i = o.lane, re.lanes |= i, In |= i, o = o.next;
    while (o !== e);
  } else
    o === null && (n.lanes = 0);
  return [t.memoizedState, n.dispatch];
}
function Ts(e) {
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
    _t(i, t.memoizedState) || (Be = !0), t.memoizedState = i, t.baseQueue === null && (t.baseState = i), n.lastRenderedState = i;
  }
  return [i, r];
}
function Kp() {
}
function Gp(e, t) {
  var n = re, r = ft(), o = t(), i = !_t(r.memoizedState, o);
  if (i && (r.memoizedState = o, Be = !0), r = r.queue, $u(Xp.bind(null, n, r, e), [e]), r.getSnapshot !== t || i || we !== null && we.memoizedState.tag & 1) {
    if (n.flags |= 2048, Co(9, Yp.bind(null, n, r, o, t), void 0, null), ke === null)
      throw Error(P(349));
    jn & 30 || Qp(n, t, o);
  }
  return o;
}
function Qp(e, t, n) {
  e.flags |= 16384, e = { getSnapshot: t, value: n }, t = re.updateQueue, t === null ? (t = { lastEffect: null, stores: null }, re.updateQueue = t, t.stores = [e]) : (n = t.stores, n === null ? t.stores = [e] : n.push(e));
}
function Yp(e, t, n, r) {
  t.value = n, t.getSnapshot = r, Zp(t) && qp(e);
}
function Xp(e, t, n) {
  return n(function() {
    Zp(t) && qp(e);
  });
}
function Zp(e) {
  var t = e.getSnapshot;
  e = e.value;
  try {
    var n = t();
    return !_t(e, n);
  } catch {
    return !0;
  }
}
function qp(e) {
  var t = Ht(e, 1);
  t !== null && Et(t, e, 1, -1);
}
function sf(e) {
  var t = Rt();
  return typeof e == "function" && (e = e()), t.memoizedState = t.baseState = e, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: ko, lastRenderedState: e }, t.queue = e, e = e.dispatch = ry.bind(null, re, e), [t.memoizedState, e];
}
function Co(e, t, n, r) {
  return e = { tag: e, create: t, destroy: n, deps: r, next: null }, t = re.updateQueue, t === null ? (t = { lastEffect: null, stores: null }, re.updateQueue = t, t.lastEffect = e.next = e) : (n = t.lastEffect, n === null ? t.lastEffect = e.next = e : (r = n.next, n.next = e, e.next = r, t.lastEffect = e)), e;
}
function Jp() {
  return ft().memoizedState;
}
function xi(e, t, n, r) {
  var o = Rt();
  re.flags |= e, o.memoizedState = Co(1 | t, n, void 0, r === void 0 ? null : r);
}
function dl(e, t, n, r) {
  var o = ft();
  r = r === void 0 ? null : r;
  var i = void 0;
  if (ve !== null) {
    var l = ve.memoizedState;
    if (i = l.destroy, r !== null && Eu(r, l.deps)) {
      o.memoizedState = Co(t, n, i, r);
      return;
    }
  }
  re.flags |= e, o.memoizedState = Co(1 | t, n, i, r);
}
function af(e, t) {
  return xi(8390656, 8, e, t);
}
function $u(e, t) {
  return dl(2048, 8, e, t);
}
function em(e, t) {
  return dl(4, 2, e, t);
}
function tm(e, t) {
  return dl(4, 4, e, t);
}
function nm(e, t) {
  if (typeof t == "function")
    return e = e(), t(e), function() {
      t(null);
    };
  if (t != null)
    return e = e(), t.current = e, function() {
      t.current = null;
    };
}
function rm(e, t, n) {
  return n = n != null ? n.concat([e]) : null, dl(4, 4, nm.bind(null, t, e), n);
}
function Tu() {
}
function om(e, t) {
  var n = ft();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && Eu(t, r[1]) ? r[0] : (n.memoizedState = [e, t], e);
}
function im(e, t) {
  var n = ft();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && Eu(t, r[1]) ? r[0] : (e = e(), n.memoizedState = [e, t], e);
}
function lm(e, t, n) {
  return jn & 21 ? (_t(n, t) || (n = fp(), re.lanes |= n, In |= n, e.baseState = !0), t) : (e.baseState && (e.baseState = !1, Be = !0), e.memoizedState = n);
}
function ty(e, t) {
  var n = V;
  V = n !== 0 && 4 > n ? n : 4, e(!0);
  var r = Ps.transition;
  Ps.transition = {};
  try {
    e(!1), t();
  } finally {
    V = n, Ps.transition = r;
  }
}
function sm() {
  return ft().memoizedState;
}
function ny(e, t, n) {
  var r = pn(e);
  if (n = { lane: r, action: n, hasEagerState: !1, eagerState: null, next: null }, am(e))
    um(t, n);
  else if (n = Up(e, t, n, r), n !== null) {
    var o = Ae();
    Et(n, e, r, o), cm(n, t, r);
  }
}
function ry(e, t, n) {
  var r = pn(e), o = { lane: r, action: n, hasEagerState: !1, eagerState: null, next: null };
  if (am(e))
    um(t, o);
  else {
    var i = e.alternate;
    if (e.lanes === 0 && (i === null || i.lanes === 0) && (i = t.lastRenderedReducer, i !== null))
      try {
        var l = t.lastRenderedState, s = i(l, n);
        if (o.hasEagerState = !0, o.eagerState = s, _t(s, l)) {
          var a = t.interleaved;
          a === null ? (o.next = o, xu(t)) : (o.next = a.next, a.next = o), t.interleaved = o;
          return;
        }
      } catch {
      } finally {
      }
    n = Up(e, t, o, r), n !== null && (o = Ae(), Et(n, e, r, o), cm(n, t, r));
  }
}
function am(e) {
  var t = e.alternate;
  return e === re || t !== null && t === re;
}
function um(e, t) {
  no = Ki = !0;
  var n = e.pending;
  n === null ? t.next = t : (t.next = n.next, n.next = t), e.pending = t;
}
function cm(e, t, n) {
  if (n & 4194240) {
    var r = t.lanes;
    r &= e.pendingLanes, n |= r, t.lanes = n, iu(e, n);
  }
}
var Gi = { readContext: ct, useCallback: Oe, useContext: Oe, useEffect: Oe, useImperativeHandle: Oe, useInsertionEffect: Oe, useLayoutEffect: Oe, useMemo: Oe, useReducer: Oe, useRef: Oe, useState: Oe, useDebugValue: Oe, useDeferredValue: Oe, useTransition: Oe, useMutableSource: Oe, useSyncExternalStore: Oe, useId: Oe, unstable_isNewReconciler: !1 }, oy = { readContext: ct, useCallback: function(e, t) {
  return Rt().memoizedState = [e, t === void 0 ? null : t], e;
}, useContext: ct, useEffect: af, useImperativeHandle: function(e, t, n) {
  return n = n != null ? n.concat([e]) : null, xi(
    4194308,
    4,
    nm.bind(null, t, e),
    n
  );
}, useLayoutEffect: function(e, t) {
  return xi(4194308, 4, e, t);
}, useInsertionEffect: function(e, t) {
  return xi(4, 2, e, t);
}, useMemo: function(e, t) {
  var n = Rt();
  return t = t === void 0 ? null : t, e = e(), n.memoizedState = [e, t], e;
}, useReducer: function(e, t, n) {
  var r = Rt();
  return t = n !== void 0 ? n(t) : t, r.memoizedState = r.baseState = t, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: e, lastRenderedState: t }, r.queue = e, e = e.dispatch = ny.bind(null, re, e), [r.memoizedState, e];
}, useRef: function(e) {
  var t = Rt();
  return e = { current: e }, t.memoizedState = e;
}, useState: sf, useDebugValue: Tu, useDeferredValue: function(e) {
  return Rt().memoizedState = e;
}, useTransition: function() {
  var e = sf(!1), t = e[0];
  return e = ty.bind(null, e[1]), Rt().memoizedState = e, [t, e];
}, useMutableSource: function() {
}, useSyncExternalStore: function(e, t, n) {
  var r = re, o = Rt();
  if (ee) {
    if (n === void 0)
      throw Error(P(407));
    n = n();
  } else {
    if (n = t(), ke === null)
      throw Error(P(349));
    jn & 30 || Qp(r, t, n);
  }
  o.memoizedState = n;
  var i = { value: n, getSnapshot: t };
  return o.queue = i, af(Xp.bind(
    null,
    r,
    i,
    e
  ), [e]), r.flags |= 2048, Co(9, Yp.bind(null, r, i, n, t), void 0, null), n;
}, useId: function() {
  var e = Rt(), t = ke.identifierPrefix;
  if (ee) {
    var n = bt, r = Ft;
    n = (r & ~(1 << 32 - Ct(r) - 1)).toString(32) + n, t = ":" + t + "R" + n, n = wo++, 0 < n && (t += "H" + n.toString(32)), t += ":";
  } else
    n = ey++, t = ":" + t + "r" + n.toString(32) + ":";
  return e.memoizedState = t;
}, unstable_isNewReconciler: !1 }, iy = {
  readContext: ct,
  useCallback: om,
  useContext: ct,
  useEffect: $u,
  useImperativeHandle: rm,
  useInsertionEffect: em,
  useLayoutEffect: tm,
  useMemo: im,
  useReducer: $s,
  useRef: Jp,
  useState: function() {
    return $s(ko);
  },
  useDebugValue: Tu,
  useDeferredValue: function(e) {
    var t = ft();
    return lm(t, ve.memoizedState, e);
  },
  useTransition: function() {
    var e = $s(ko)[0], t = ft().memoizedState;
    return [e, t];
  },
  useMutableSource: Kp,
  useSyncExternalStore: Gp,
  useId: sm,
  unstable_isNewReconciler: !1
}, ly = { readContext: ct, useCallback: om, useContext: ct, useEffect: $u, useImperativeHandle: rm, useInsertionEffect: em, useLayoutEffect: tm, useMemo: im, useReducer: Ts, useRef: Jp, useState: function() {
  return Ts(ko);
}, useDebugValue: Tu, useDeferredValue: function(e) {
  var t = ft();
  return ve === null ? t.memoizedState = e : lm(t, ve.memoizedState, e);
}, useTransition: function() {
  var e = Ts(ko)[0], t = ft().memoizedState;
  return [e, t];
}, useMutableSource: Kp, useSyncExternalStore: Gp, useId: sm, unstable_isNewReconciler: !1 };
function xt(e, t) {
  if (e && e.defaultProps) {
    t = ie({}, t), e = e.defaultProps;
    for (var n in e)
      t[n] === void 0 && (t[n] = e[n]);
    return t;
  }
  return t;
}
function xa(e, t, n, r) {
  t = e.memoizedState, n = n(r, t), n = n == null ? t : ie({}, t, n), e.memoizedState = n, e.lanes === 0 && (e.updateQueue.baseState = n);
}
var pl = { isMounted: function(e) {
  return (e = e._reactInternals) ? Dn(e) === e : !1;
}, enqueueSetState: function(e, t, n) {
  e = e._reactInternals;
  var r = Ae(), o = pn(e), i = Wt(r, o);
  i.payload = t, n != null && (i.callback = n), t = fn(e, i, o), t !== null && (Et(t, e, o, r), yi(t, e, o));
}, enqueueReplaceState: function(e, t, n) {
  e = e._reactInternals;
  var r = Ae(), o = pn(e), i = Wt(r, o);
  i.tag = 1, i.payload = t, n != null && (i.callback = n), t = fn(e, i, o), t !== null && (Et(t, e, o, r), yi(t, e, o));
}, enqueueForceUpdate: function(e, t) {
  e = e._reactInternals;
  var n = Ae(), r = pn(e), o = Wt(n, r);
  o.tag = 2, t != null && (o.callback = t), t = fn(e, o, r), t !== null && (Et(t, e, r, n), yi(t, e, r));
} };
function uf(e, t, n, r, o, i, l) {
  return e = e.stateNode, typeof e.shouldComponentUpdate == "function" ? e.shouldComponentUpdate(r, i, l) : t.prototype && t.prototype.isPureReactComponent ? !ho(n, r) || !ho(o, i) : !0;
}
function fm(e, t, n) {
  var r = !1, o = yn, i = t.contextType;
  return typeof i == "object" && i !== null ? i = ct(i) : (o = Ue(t) ? Nn : je.current, r = t.contextTypes, i = (r = r != null) ? gr(e, o) : yn), t = new t(n, i), e.memoizedState = t.state !== null && t.state !== void 0 ? t.state : null, t.updater = pl, e.stateNode = t, t._reactInternals = e, r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = o, e.__reactInternalMemoizedMaskedChildContext = i), t;
}
function cf(e, t, n, r) {
  e = t.state, typeof t.componentWillReceiveProps == "function" && t.componentWillReceiveProps(n, r), typeof t.UNSAFE_componentWillReceiveProps == "function" && t.UNSAFE_componentWillReceiveProps(n, r), t.state !== e && pl.enqueueReplaceState(t, t.state, null);
}
function Sa(e, t, n, r) {
  var o = e.stateNode;
  o.props = n, o.state = e.memoizedState, o.refs = {}, Su(e);
  var i = t.contextType;
  typeof i == "object" && i !== null ? o.context = ct(i) : (i = Ue(t) ? Nn : je.current, o.context = gr(e, i)), o.state = e.memoizedState, i = t.getDerivedStateFromProps, typeof i == "function" && (xa(e, t, i, n), o.state = e.memoizedState), typeof t.getDerivedStateFromProps == "function" || typeof o.getSnapshotBeforeUpdate == "function" || typeof o.UNSAFE_componentWillMount != "function" && typeof o.componentWillMount != "function" || (t = o.state, typeof o.componentWillMount == "function" && o.componentWillMount(), typeof o.UNSAFE_componentWillMount == "function" && o.UNSAFE_componentWillMount(), t !== o.state && pl.enqueueReplaceState(o, o.state, null), Vi(e, n, o, r), o.state = e.memoizedState), typeof o.componentDidMount == "function" && (e.flags |= 4194308);
}
function Sr(e, t) {
  try {
    var n = "", r = t;
    do
      n += j0(r), r = r.return;
    while (r);
    var o = n;
  } catch (i) {
    o = `
Error generating stack: ` + i.message + `
` + i.stack;
  }
  return { value: e, source: t, stack: o, digest: null };
}
function Rs(e, t, n) {
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
var sy = typeof WeakMap == "function" ? WeakMap : Map;
function dm(e, t, n) {
  n = Wt(-1, n), n.tag = 3, n.payload = { element: null };
  var r = t.value;
  return n.callback = function() {
    Yi || (Yi = !0, Ma = r), wa(e, t);
  }, n;
}
function pm(e, t, n) {
  n = Wt(-1, n), n.tag = 3;
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
    wa(e, t), typeof r != "function" && (dn === null ? dn = /* @__PURE__ */ new Set([this]) : dn.add(this));
    var l = t.stack;
    this.componentDidCatch(t.value, { componentStack: l !== null ? l : "" });
  }), n;
}
function ff(e, t, n) {
  var r = e.pingCache;
  if (r === null) {
    r = e.pingCache = new sy();
    var o = /* @__PURE__ */ new Set();
    r.set(t, o);
  } else
    o = r.get(t), o === void 0 && (o = /* @__PURE__ */ new Set(), r.set(t, o));
  o.has(n) || (o.add(n), e = wy.bind(null, e, t, n), t.then(e, e));
}
function df(e) {
  do {
    var t;
    if ((t = e.tag === 13) && (t = e.memoizedState, t = t !== null ? t.dehydrated !== null : !0), t)
      return e;
    e = e.return;
  } while (e !== null);
  return null;
}
function pf(e, t, n, r, o) {
  return e.mode & 1 ? (e.flags |= 65536, e.lanes = o, e) : (e === t ? e.flags |= 65536 : (e.flags |= 128, n.flags |= 131072, n.flags &= -52805, n.tag === 1 && (n.alternate === null ? n.tag = 17 : (t = Wt(-1, 1), t.tag = 2, fn(n, t, 1))), n.lanes |= 1), e);
}
var ay = Qt.ReactCurrentOwner, Be = !1;
function Le(e, t, n, r) {
  t.child = e === null ? Wp(t, null, n, r) : vr(t, e.child, n, r);
}
function mf(e, t, n, r, o) {
  n = n.render;
  var i = t.ref;
  return cr(t, o), r = _u(e, t, n, r, i, o), n = Pu(), e !== null && !Be ? (t.updateQueue = e.updateQueue, t.flags &= -2053, e.lanes &= ~o, Kt(e, t, o)) : (ee && n && pu(t), t.flags |= 1, Le(e, t, r, o), t.child);
}
function hf(e, t, n, r, o) {
  if (e === null) {
    var i = n.type;
    return typeof i == "function" && !Lu(i) && i.defaultProps === void 0 && n.compare === null && n.defaultProps === void 0 ? (t.tag = 15, t.type = i, mm(e, t, i, r, o)) : (e = Ci(n.type, null, r, t, t.mode, o), e.ref = t.ref, e.return = t, t.child = e);
  }
  if (i = e.child, !(e.lanes & o)) {
    var l = i.memoizedProps;
    if (n = n.compare, n = n !== null ? n : ho, n(l, r) && e.ref === t.ref)
      return Kt(e, t, o);
  }
  return t.flags |= 1, e = mn(i, r), e.ref = t.ref, e.return = t, t.child = e;
}
function mm(e, t, n, r, o) {
  if (e !== null) {
    var i = e.memoizedProps;
    if (ho(i, r) && e.ref === t.ref)
      if (Be = !1, t.pendingProps = r = i, (e.lanes & o) !== 0)
        e.flags & 131072 && (Be = !0);
      else
        return t.lanes = e.lanes, Kt(e, t, o);
  }
  return ka(e, t, n, r, o);
}
function hm(e, t, n) {
  var r = t.pendingProps, o = r.children, i = e !== null ? e.memoizedState : null;
  if (r.mode === "hidden")
    if (!(t.mode & 1))
      t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, Q(ir, Ke), Ke |= n;
    else {
      if (!(n & 1073741824))
        return e = i !== null ? i.baseLanes | n : n, t.lanes = t.childLanes = 1073741824, t.memoizedState = { baseLanes: e, cachePool: null, transitions: null }, t.updateQueue = null, Q(ir, Ke), Ke |= e, null;
      t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, r = i !== null ? i.baseLanes : n, Q(ir, Ke), Ke |= r;
    }
  else
    i !== null ? (r = i.baseLanes | n, t.memoizedState = null) : r = n, Q(ir, Ke), Ke |= r;
  return Le(e, t, o, n), t.child;
}
function gm(e, t) {
  var n = t.ref;
  (e === null && n !== null || e !== null && e.ref !== n) && (t.flags |= 512, t.flags |= 2097152);
}
function ka(e, t, n, r, o) {
  var i = Ue(n) ? Nn : je.current;
  return i = gr(t, i), cr(t, o), n = _u(e, t, n, r, i, o), r = Pu(), e !== null && !Be ? (t.updateQueue = e.updateQueue, t.flags &= -2053, e.lanes &= ~o, Kt(e, t, o)) : (ee && r && pu(t), t.flags |= 1, Le(e, t, n, o), t.child);
}
function gf(e, t, n, r, o) {
  if (Ue(n)) {
    var i = !0;
    Fi(t);
  } else
    i = !1;
  if (cr(t, o), t.stateNode === null)
    Si(e, t), fm(t, n, r), Sa(t, n, r, o), r = !0;
  else if (e === null) {
    var l = t.stateNode, s = t.memoizedProps;
    l.props = s;
    var a = l.context, u = n.contextType;
    typeof u == "object" && u !== null ? u = ct(u) : (u = Ue(n) ? Nn : je.current, u = gr(t, u));
    var c = n.getDerivedStateFromProps, d = typeof c == "function" || typeof l.getSnapshotBeforeUpdate == "function";
    d || typeof l.UNSAFE_componentWillReceiveProps != "function" && typeof l.componentWillReceiveProps != "function" || (s !== r || a !== u) && cf(t, l, r, u), en = !1;
    var m = t.memoizedState;
    l.state = m, Vi(t, r, l, o), a = t.memoizedState, s !== r || m !== a || We.current || en ? (typeof c == "function" && (xa(t, n, c, r), a = t.memoizedState), (s = en || uf(t, n, s, r, m, a, u)) ? (d || typeof l.UNSAFE_componentWillMount != "function" && typeof l.componentWillMount != "function" || (typeof l.componentWillMount == "function" && l.componentWillMount(), typeof l.UNSAFE_componentWillMount == "function" && l.UNSAFE_componentWillMount()), typeof l.componentDidMount == "function" && (t.flags |= 4194308)) : (typeof l.componentDidMount == "function" && (t.flags |= 4194308), t.memoizedProps = r, t.memoizedState = a), l.props = r, l.state = a, l.context = u, r = s) : (typeof l.componentDidMount == "function" && (t.flags |= 4194308), r = !1);
  } else {
    l = t.stateNode, Vp(e, t), s = t.memoizedProps, u = t.type === t.elementType ? s : xt(t.type, s), l.props = u, d = t.pendingProps, m = l.context, a = n.contextType, typeof a == "object" && a !== null ? a = ct(a) : (a = Ue(n) ? Nn : je.current, a = gr(t, a));
    var v = n.getDerivedStateFromProps;
    (c = typeof v == "function" || typeof l.getSnapshotBeforeUpdate == "function") || typeof l.UNSAFE_componentWillReceiveProps != "function" && typeof l.componentWillReceiveProps != "function" || (s !== d || m !== a) && cf(t, l, r, a), en = !1, m = t.memoizedState, l.state = m, Vi(t, r, l, o);
    var y = t.memoizedState;
    s !== d || m !== y || We.current || en ? (typeof v == "function" && (xa(t, n, v, r), y = t.memoizedState), (u = en || uf(t, n, u, r, m, y, a) || !1) ? (c || typeof l.UNSAFE_componentWillUpdate != "function" && typeof l.componentWillUpdate != "function" || (typeof l.componentWillUpdate == "function" && l.componentWillUpdate(r, y, a), typeof l.UNSAFE_componentWillUpdate == "function" && l.UNSAFE_componentWillUpdate(r, y, a)), typeof l.componentDidUpdate == "function" && (t.flags |= 4), typeof l.getSnapshotBeforeUpdate == "function" && (t.flags |= 1024)) : (typeof l.componentDidUpdate != "function" || s === e.memoizedProps && m === e.memoizedState || (t.flags |= 4), typeof l.getSnapshotBeforeUpdate != "function" || s === e.memoizedProps && m === e.memoizedState || (t.flags |= 1024), t.memoizedProps = r, t.memoizedState = y), l.props = r, l.state = y, l.context = a, r = u) : (typeof l.componentDidUpdate != "function" || s === e.memoizedProps && m === e.memoizedState || (t.flags |= 4), typeof l.getSnapshotBeforeUpdate != "function" || s === e.memoizedProps && m === e.memoizedState || (t.flags |= 1024), r = !1);
  }
  return Ca(e, t, n, r, i, o);
}
function Ca(e, t, n, r, o, i) {
  gm(e, t);
  var l = (t.flags & 128) !== 0;
  if (!r && !l)
    return o && ef(t, n, !1), Kt(e, t, i);
  r = t.stateNode, ay.current = t;
  var s = l && typeof n.getDerivedStateFromError != "function" ? null : r.render();
  return t.flags |= 1, e !== null && l ? (t.child = vr(t, e.child, null, i), t.child = vr(t, null, s, i)) : Le(e, t, s, i), t.memoizedState = r.state, o && ef(t, n, !0), t.child;
}
function ym(e) {
  var t = e.stateNode;
  t.pendingContext ? Jc(e, t.pendingContext, t.pendingContext !== t.context) : t.context && Jc(e, t.context, !1), wu(e, t.containerInfo);
}
function yf(e, t, n, r, o) {
  return yr(), hu(o), t.flags |= 256, Le(e, t, n, r), t.child;
}
var Ea = { dehydrated: null, treeContext: null, retryLane: 0 };
function _a(e) {
  return { baseLanes: e, cachePool: null, transitions: null };
}
function vm(e, t, n) {
  var r = t.pendingProps, o = te.current, i = !1, l = (t.flags & 128) !== 0, s;
  if ((s = l) || (s = e !== null && e.memoizedState === null ? !1 : (o & 2) !== 0), s ? (i = !0, t.flags &= -129) : (e === null || e.memoizedState !== null) && (o |= 1), Q(te, o & 1), e === null)
    return ya(t), e = t.memoizedState, e !== null && (e = e.dehydrated, e !== null) ? (t.mode & 1 ? e.data === "$!" ? t.lanes = 8 : t.lanes = 1073741824 : t.lanes = 1, null) : (l = r.children, e = r.fallback, i ? (r = t.mode, i = t.child, l = { mode: "hidden", children: l }, !(r & 1) && i !== null ? (i.childLanes = 0, i.pendingProps = l) : i = gl(l, r, 0, null), e = On(e, r, n, null), i.return = t, e.return = t, i.sibling = e, t.child = i, t.child.memoizedState = _a(n), t.memoizedState = Ea, e) : Ru(t, l));
  if (o = e.memoizedState, o !== null && (s = o.dehydrated, s !== null))
    return uy(e, t, l, r, s, o, n);
  if (i) {
    i = r.fallback, l = t.mode, o = e.child, s = o.sibling;
    var a = { mode: "hidden", children: r.children };
    return !(l & 1) && t.child !== o ? (r = t.child, r.childLanes = 0, r.pendingProps = a, t.deletions = null) : (r = mn(o, a), r.subtreeFlags = o.subtreeFlags & 14680064), s !== null ? i = mn(s, i) : (i = On(i, l, n, null), i.flags |= 2), i.return = t, r.return = t, r.sibling = i, t.child = r, r = i, i = t.child, l = e.child.memoizedState, l = l === null ? _a(n) : { baseLanes: l.baseLanes | n, cachePool: null, transitions: l.transitions }, i.memoizedState = l, i.childLanes = e.childLanes & ~n, t.memoizedState = Ea, r;
  }
  return i = e.child, e = i.sibling, r = mn(i, { mode: "visible", children: r.children }), !(t.mode & 1) && (r.lanes = n), r.return = t, r.sibling = null, e !== null && (n = t.deletions, n === null ? (t.deletions = [e], t.flags |= 16) : n.push(e)), t.child = r, t.memoizedState = null, r;
}
function Ru(e, t) {
  return t = gl({ mode: "visible", children: t }, e.mode, 0, null), t.return = e, e.child = t;
}
function ii(e, t, n, r) {
  return r !== null && hu(r), vr(t, e.child, null, n), e = Ru(t, t.pendingProps.children), e.flags |= 2, t.memoizedState = null, e;
}
function uy(e, t, n, r, o, i, l) {
  if (n)
    return t.flags & 256 ? (t.flags &= -257, r = Rs(Error(P(422))), ii(e, t, l, r)) : t.memoizedState !== null ? (t.child = e.child, t.flags |= 128, null) : (i = r.fallback, o = t.mode, r = gl({ mode: "visible", children: r.children }, o, 0, null), i = On(i, o, l, null), i.flags |= 2, r.return = t, i.return = t, r.sibling = i, t.child = r, t.mode & 1 && vr(t, e.child, null, l), t.child.memoizedState = _a(l), t.memoizedState = Ea, i);
  if (!(t.mode & 1))
    return ii(e, t, l, null);
  if (o.data === "$!") {
    if (r = o.nextSibling && o.nextSibling.dataset, r)
      var s = r.dgst;
    return r = s, i = Error(P(419)), r = Rs(i, r, void 0), ii(e, t, l, r);
  }
  if (s = (l & e.childLanes) !== 0, Be || s) {
    if (r = ke, r !== null) {
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
      o = o & (r.suspendedLanes | l) ? 0 : o, o !== 0 && o !== i.retryLane && (i.retryLane = o, Ht(e, o), Et(r, e, o, -1));
    }
    return Iu(), r = Rs(Error(P(421))), ii(e, t, l, r);
  }
  return o.data === "$?" ? (t.flags |= 128, t.child = e.child, t = ky.bind(null, e), o._reactRetry = t, null) : (e = i.treeContext, Qe = cn(o.nextSibling), Ye = t, ee = !0, wt = null, e !== null && (it[lt++] = Ft, it[lt++] = bt, it[lt++] = zn, Ft = e.id, bt = e.overflow, zn = t), t = Ru(t, r.children), t.flags |= 4096, t);
}
function vf(e, t, n) {
  e.lanes |= t;
  var r = e.alternate;
  r !== null && (r.lanes |= t), va(e.return, t, n);
}
function Os(e, t, n, r, o) {
  var i = e.memoizedState;
  i === null ? e.memoizedState = { isBackwards: t, rendering: null, renderingStartTime: 0, last: r, tail: n, tailMode: o } : (i.isBackwards = t, i.rendering = null, i.renderingStartTime = 0, i.last = r, i.tail = n, i.tailMode = o);
}
function xm(e, t, n) {
  var r = t.pendingProps, o = r.revealOrder, i = r.tail;
  if (Le(e, t, r.children, n), r = te.current, r & 2)
    r = r & 1 | 2, t.flags |= 128;
  else {
    if (e !== null && e.flags & 128)
      e:
        for (e = t.child; e !== null; ) {
          if (e.tag === 13)
            e.memoizedState !== null && vf(e, n, t);
          else if (e.tag === 19)
            vf(e, n, t);
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
  if (Q(te, r), !(t.mode & 1))
    t.memoizedState = null;
  else
    switch (o) {
      case "forwards":
        for (n = t.child, o = null; n !== null; )
          e = n.alternate, e !== null && Hi(e) === null && (o = n), n = n.sibling;
        n = o, n === null ? (o = t.child, t.child = null) : (o = n.sibling, n.sibling = null), Os(t, !1, o, n, i);
        break;
      case "backwards":
        for (n = null, o = t.child, t.child = null; o !== null; ) {
          if (e = o.alternate, e !== null && Hi(e) === null) {
            t.child = o;
            break;
          }
          e = o.sibling, o.sibling = n, n = o, o = e;
        }
        Os(t, !0, n, null, i);
        break;
      case "together":
        Os(t, !1, null, null, void 0);
        break;
      default:
        t.memoizedState = null;
    }
  return t.child;
}
function Si(e, t) {
  !(t.mode & 1) && e !== null && (e.alternate = null, t.alternate = null, t.flags |= 2);
}
function Kt(e, t, n) {
  if (e !== null && (t.dependencies = e.dependencies), In |= t.lanes, !(n & t.childLanes))
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
function cy(e, t, n) {
  switch (t.tag) {
    case 3:
      ym(t), yr();
      break;
    case 5:
      Hp(t);
      break;
    case 1:
      Ue(t.type) && Fi(t);
      break;
    case 4:
      wu(t, t.stateNode.containerInfo);
      break;
    case 10:
      var r = t.type._context, o = t.memoizedProps.value;
      Q(Wi, r._currentValue), r._currentValue = o;
      break;
    case 13:
      if (r = t.memoizedState, r !== null)
        return r.dehydrated !== null ? (Q(te, te.current & 1), t.flags |= 128, null) : n & t.child.childLanes ? vm(e, t, n) : (Q(te, te.current & 1), e = Kt(e, t, n), e !== null ? e.sibling : null);
      Q(te, te.current & 1);
      break;
    case 19:
      if (r = (n & t.childLanes) !== 0, e.flags & 128) {
        if (r)
          return xm(e, t, n);
        t.flags |= 128;
      }
      if (o = t.memoizedState, o !== null && (o.rendering = null, o.tail = null, o.lastEffect = null), Q(te, te.current), r)
        break;
      return null;
    case 22:
    case 23:
      return t.lanes = 0, hm(e, t, n);
  }
  return Kt(e, t, n);
}
var Sm, Pa, wm, km;
Sm = function(e, t) {
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
wm = function(e, t, n, r) {
  var o = e.memoizedProps;
  if (o !== r) {
    e = t.stateNode, $n(jt.current);
    var i = null;
    switch (n) {
      case "input":
        o = Qs(e, o), r = Qs(e, r), i = [];
        break;
      case "select":
        o = ie({}, o, { value: void 0 }), r = ie({}, r, { value: void 0 }), i = [];
        break;
      case "textarea":
        o = Zs(e, o), r = Zs(e, r), i = [];
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
          u !== "dangerouslySetInnerHTML" && u !== "children" && u !== "suppressContentEditableWarning" && u !== "suppressHydrationWarning" && u !== "autoFocus" && (so.hasOwnProperty(u) ? i || (i = []) : (i = i || []).push(u, null));
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
          u === "dangerouslySetInnerHTML" ? (a = a ? a.__html : void 0, s = s ? s.__html : void 0, a != null && s !== a && (i = i || []).push(u, a)) : u === "children" ? typeof a != "string" && typeof a != "number" || (i = i || []).push(u, "" + a) : u !== "suppressContentEditableWarning" && u !== "suppressHydrationWarning" && (so.hasOwnProperty(u) ? (a != null && u === "onScroll" && X("scroll", e), i || s === a || (i = [])) : (i = i || []).push(u, a));
    }
    n && (i = i || []).push("style", n);
    var u = i;
    (t.updateQueue = u) && (t.flags |= 4);
  }
};
km = function(e, t, n, r) {
  n !== r && (t.flags |= 4);
};
function br(e, t) {
  if (!ee)
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
function fy(e, t, n) {
  var r = t.pendingProps;
  switch (mu(t), t.tag) {
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
      return r = t.stateNode, xr(), Z(We), Z(je), Cu(), r.pendingContext && (r.context = r.pendingContext, r.pendingContext = null), (e === null || e.child === null) && (ri(t) ? t.flags |= 4 : e === null || e.memoizedState.isDehydrated && !(t.flags & 256) || (t.flags |= 1024, wt !== null && (ja(wt), wt = null))), Pa(e, t), Me(t), null;
    case 5:
      ku(t);
      var o = $n(So.current);
      if (n = t.type, e !== null && t.stateNode != null)
        wm(e, t, n, r, o), e.ref !== t.ref && (t.flags |= 512, t.flags |= 2097152);
      else {
        if (!r) {
          if (t.stateNode === null)
            throw Error(P(166));
          return Me(t), null;
        }
        if (e = $n(jt.current), ri(t)) {
          r = t.stateNode, n = t.type;
          var i = t.memoizedProps;
          switch (r[Nt] = t, r[vo] = i, e = (t.mode & 1) !== 0, n) {
            case "dialog":
              X("cancel", r), X("close", r);
              break;
            case "iframe":
            case "object":
            case "embed":
              X("load", r);
              break;
            case "video":
            case "audio":
              for (o = 0; o < Qr.length; o++)
                X(Qr[o], r);
              break;
            case "source":
              X("error", r);
              break;
            case "img":
            case "image":
            case "link":
              X(
                "error",
                r
              ), X("load", r);
              break;
            case "details":
              X("toggle", r);
              break;
            case "input":
              Pc(r, i), X("invalid", r);
              break;
            case "select":
              r._wrapperState = { wasMultiple: !!i.multiple }, X("invalid", r);
              break;
            case "textarea":
              Tc(r, i), X("invalid", r);
          }
          Js(n, i), o = null;
          for (var l in i)
            if (i.hasOwnProperty(l)) {
              var s = i[l];
              l === "children" ? typeof s == "string" ? r.textContent !== s && (i.suppressHydrationWarning !== !0 && ni(r.textContent, s, e), o = ["children", s]) : typeof s == "number" && r.textContent !== "" + s && (i.suppressHydrationWarning !== !0 && ni(
                r.textContent,
                s,
                e
              ), o = ["children", "" + s]) : so.hasOwnProperty(l) && s != null && l === "onScroll" && X("scroll", r);
            }
          switch (n) {
            case "input":
              Qo(r), $c(r, i, !0);
              break;
            case "textarea":
              Qo(r), Rc(r);
              break;
            case "select":
            case "option":
              break;
            default:
              typeof i.onClick == "function" && (r.onclick = Ai);
          }
          r = o, t.updateQueue = r, r !== null && (t.flags |= 4);
        } else {
          l = o.nodeType === 9 ? o : o.ownerDocument, e === "http://www.w3.org/1999/xhtml" && (e = Xd(n)), e === "http://www.w3.org/1999/xhtml" ? n === "script" ? (e = l.createElement("div"), e.innerHTML = "<script><\/script>", e = e.removeChild(e.firstChild)) : typeof r.is == "string" ? e = l.createElement(n, { is: r.is }) : (e = l.createElement(n), n === "select" && (l = e, r.multiple ? l.multiple = !0 : r.size && (l.size = r.size))) : e = l.createElementNS(e, n), e[Nt] = t, e[vo] = r, Sm(e, t, !1, !1), t.stateNode = e;
          e: {
            switch (l = ea(n, r), n) {
              case "dialog":
                X("cancel", e), X("close", e), o = r;
                break;
              case "iframe":
              case "object":
              case "embed":
                X("load", e), o = r;
                break;
              case "video":
              case "audio":
                for (o = 0; o < Qr.length; o++)
                  X(Qr[o], e);
                o = r;
                break;
              case "source":
                X("error", e), o = r;
                break;
              case "img":
              case "image":
              case "link":
                X(
                  "error",
                  e
                ), X("load", e), o = r;
                break;
              case "details":
                X("toggle", e), o = r;
                break;
              case "input":
                Pc(e, r), o = Qs(e, r), X("invalid", e);
                break;
              case "option":
                o = r;
                break;
              case "select":
                e._wrapperState = { wasMultiple: !!r.multiple }, o = ie({}, r, { value: void 0 }), X("invalid", e);
                break;
              case "textarea":
                Tc(e, r), o = Zs(e, r), X("invalid", e);
                break;
              default:
                o = r;
            }
            Js(n, o), s = o;
            for (i in s)
              if (s.hasOwnProperty(i)) {
                var a = s[i];
                i === "style" ? Jd(e, a) : i === "dangerouslySetInnerHTML" ? (a = a ? a.__html : void 0, a != null && Zd(e, a)) : i === "children" ? typeof a == "string" ? (n !== "textarea" || a !== "") && ao(e, a) : typeof a == "number" && ao(e, "" + a) : i !== "suppressContentEditableWarning" && i !== "suppressHydrationWarning" && i !== "autoFocus" && (so.hasOwnProperty(i) ? a != null && i === "onScroll" && X("scroll", e) : a != null && Ja(e, i, a, l));
              }
            switch (n) {
              case "input":
                Qo(e), $c(e, r, !1);
                break;
              case "textarea":
                Qo(e), Rc(e);
                break;
              case "option":
                r.value != null && e.setAttribute("value", "" + gn(r.value));
                break;
              case "select":
                e.multiple = !!r.multiple, i = r.value, i != null ? lr(e, !!r.multiple, i, !1) : r.defaultValue != null && lr(
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
        km(e, t, e.memoizedProps, r);
      else {
        if (typeof r != "string" && t.stateNode === null)
          throw Error(P(166));
        if (n = $n(So.current), $n(jt.current), ri(t)) {
          if (r = t.stateNode, n = t.memoizedProps, r[Nt] = t, (i = r.nodeValue !== n) && (e = Ye, e !== null))
            switch (e.tag) {
              case 3:
                ni(r.nodeValue, n, (e.mode & 1) !== 0);
                break;
              case 5:
                e.memoizedProps.suppressHydrationWarning !== !0 && ni(r.nodeValue, n, (e.mode & 1) !== 0);
            }
          i && (t.flags |= 4);
        } else
          r = (n.nodeType === 9 ? n : n.ownerDocument).createTextNode(r), r[Nt] = t, t.stateNode = r;
      }
      return Me(t), null;
    case 13:
      if (Z(te), r = t.memoizedState, e === null || e.memoizedState !== null && e.memoizedState.dehydrated !== null) {
        if (ee && Qe !== null && t.mode & 1 && !(t.flags & 128))
          bp(), yr(), t.flags |= 98560, i = !1;
        else if (i = ri(t), r !== null && r.dehydrated !== null) {
          if (e === null) {
            if (!i)
              throw Error(P(318));
            if (i = t.memoizedState, i = i !== null ? i.dehydrated : null, !i)
              throw Error(P(317));
            i[Nt] = t;
          } else
            yr(), !(t.flags & 128) && (t.memoizedState = null), t.flags |= 4;
          Me(t), i = !1;
        } else
          wt !== null && (ja(wt), wt = null), i = !0;
        if (!i)
          return t.flags & 65536 ? t : null;
      }
      return t.flags & 128 ? (t.lanes = n, t) : (r = r !== null, r !== (e !== null && e.memoizedState !== null) && r && (t.child.flags |= 8192, t.mode & 1 && (e === null || te.current & 1 ? xe === 0 && (xe = 3) : Iu())), t.updateQueue !== null && (t.flags |= 4), Me(t), null);
    case 4:
      return xr(), Pa(e, t), e === null && go(t.stateNode.containerInfo), Me(t), null;
    case 10:
      return vu(t.type._context), Me(t), null;
    case 17:
      return Ue(t.type) && Di(), Me(t), null;
    case 19:
      if (Z(te), i = t.memoizedState, i === null)
        return Me(t), null;
      if (r = (t.flags & 128) !== 0, l = i.rendering, l === null)
        if (r)
          br(i, !1);
        else {
          if (xe !== 0 || e !== null && e.flags & 128)
            for (e = t.child; e !== null; ) {
              if (l = Hi(e), l !== null) {
                for (t.flags |= 128, br(i, !1), r = l.updateQueue, r !== null && (t.updateQueue = r, t.flags |= 4), t.subtreeFlags = 0, r = n, n = t.child; n !== null; )
                  i = n, e = r, i.flags &= 14680066, l = i.alternate, l === null ? (i.childLanes = 0, i.lanes = e, i.child = null, i.subtreeFlags = 0, i.memoizedProps = null, i.memoizedState = null, i.updateQueue = null, i.dependencies = null, i.stateNode = null) : (i.childLanes = l.childLanes, i.lanes = l.lanes, i.child = l.child, i.subtreeFlags = 0, i.deletions = null, i.memoizedProps = l.memoizedProps, i.memoizedState = l.memoizedState, i.updateQueue = l.updateQueue, i.type = l.type, e = l.dependencies, i.dependencies = e === null ? null : { lanes: e.lanes, firstContext: e.firstContext }), n = n.sibling;
                return Q(te, te.current & 1 | 2), t.child;
              }
              e = e.sibling;
            }
          i.tail !== null && ce() > wr && (t.flags |= 128, r = !0, br(i, !1), t.lanes = 4194304);
        }
      else {
        if (!r)
          if (e = Hi(l), e !== null) {
            if (t.flags |= 128, r = !0, n = e.updateQueue, n !== null && (t.updateQueue = n, t.flags |= 4), br(i, !0), i.tail === null && i.tailMode === "hidden" && !l.alternate && !ee)
              return Me(t), null;
          } else
            2 * ce() - i.renderingStartTime > wr && n !== 1073741824 && (t.flags |= 128, r = !0, br(i, !1), t.lanes = 4194304);
        i.isBackwards ? (l.sibling = t.child, t.child = l) : (n = i.last, n !== null ? n.sibling = l : t.child = l, i.last = l);
      }
      return i.tail !== null ? (t = i.tail, i.rendering = t, i.tail = t.sibling, i.renderingStartTime = ce(), t.sibling = null, n = te.current, Q(te, r ? n & 1 | 2 : n & 1), t) : (Me(t), null);
    case 22:
    case 23:
      return ju(), r = t.memoizedState !== null, e !== null && e.memoizedState !== null !== r && (t.flags |= 8192), r && t.mode & 1 ? Ke & 1073741824 && (Me(t), t.subtreeFlags & 6 && (t.flags |= 8192)) : Me(t), null;
    case 24:
      return null;
    case 25:
      return null;
  }
  throw Error(P(156, t.tag));
}
function dy(e, t) {
  switch (mu(t), t.tag) {
    case 1:
      return Ue(t.type) && Di(), e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, t) : null;
    case 3:
      return xr(), Z(We), Z(je), Cu(), e = t.flags, e & 65536 && !(e & 128) ? (t.flags = e & -65537 | 128, t) : null;
    case 5:
      return ku(t), null;
    case 13:
      if (Z(te), e = t.memoizedState, e !== null && e.dehydrated !== null) {
        if (t.alternate === null)
          throw Error(P(340));
        yr();
      }
      return e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, t) : null;
    case 19:
      return Z(te), null;
    case 4:
      return xr(), null;
    case 10:
      return vu(t.type._context), null;
    case 22:
    case 23:
      return ju(), null;
    case 24:
      return null;
    default:
      return null;
  }
}
var li = !1, ze = !1, py = typeof WeakSet == "function" ? WeakSet : Set, M = null;
function or(e, t) {
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
function $a(e, t, n) {
  try {
    n();
  } catch (r) {
    ue(e, t, r);
  }
}
var xf = !1;
function my(e, t) {
  if (ca = ji, e = $p(), du(e)) {
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
          var l = 0, s = -1, a = -1, u = 0, c = 0, d = e, m = null;
          t:
            for (; ; ) {
              for (var v; d !== n || o !== 0 && d.nodeType !== 3 || (s = l + o), d !== i || r !== 0 && d.nodeType !== 3 || (a = l + r), d.nodeType === 3 && (l += d.nodeValue.length), (v = d.firstChild) !== null; )
                m = d, d = v;
              for (; ; ) {
                if (d === e)
                  break t;
                if (m === n && ++u === o && (s = l), m === i && ++c === r && (a = l), (v = d.nextSibling) !== null)
                  break;
                d = m, m = d.parentNode;
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
  for (fa = { focusedElem: e, selectionRange: n }, ji = !1, M = t; M !== null; )
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
                  var g = y.memoizedProps, $ = y.memoizedState, p = t.stateNode, f = p.getSnapshotBeforeUpdate(t.elementType === t.type ? g : xt(t.type, g), $);
                  p.__reactInternalSnapshotBeforeUpdate = f;
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
          ue(t, t.return, x);
        }
        if (e = t.sibling, e !== null) {
          e.return = t.return, M = e;
          break;
        }
        M = t.return;
      }
  return y = xf, xf = !1, y;
}
function ro(e, t, n) {
  var r = t.updateQueue;
  if (r = r !== null ? r.lastEffect : null, r !== null) {
    var o = r = r.next;
    do {
      if ((o.tag & e) === e) {
        var i = o.destroy;
        o.destroy = void 0, i !== void 0 && $a(t, n, i);
      }
      o = o.next;
    } while (o !== r);
  }
}
function ml(e, t) {
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
function Ta(e) {
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
function Cm(e) {
  var t = e.alternate;
  t !== null && (e.alternate = null, Cm(t)), e.child = null, e.deletions = null, e.sibling = null, e.tag === 5 && (t = e.stateNode, t !== null && (delete t[Nt], delete t[vo], delete t[ma], delete t[Xg], delete t[Zg])), e.stateNode = null, e.return = null, e.dependencies = null, e.memoizedProps = null, e.memoizedState = null, e.pendingProps = null, e.stateNode = null, e.updateQueue = null;
}
function Em(e) {
  return e.tag === 5 || e.tag === 3 || e.tag === 4;
}
function Sf(e) {
  e:
    for (; ; ) {
      for (; e.sibling === null; ) {
        if (e.return === null || Em(e.return))
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
function Zt(e, t, n) {
  for (n = n.child; n !== null; )
    _m(e, t, n), n = n.sibling;
}
function _m(e, t, n) {
  if (zt && typeof zt.onCommitFiberUnmount == "function")
    try {
      zt.onCommitFiberUnmount(ll, n);
    } catch {
    }
  switch (n.tag) {
    case 5:
      ze || or(n, t);
    case 6:
      var r = Pe, o = St;
      Pe = null, Zt(e, t, n), Pe = r, St = o, Pe !== null && (St ? (e = Pe, n = n.stateNode, e.nodeType === 8 ? e.parentNode.removeChild(n) : e.removeChild(n)) : Pe.removeChild(n.stateNode));
      break;
    case 18:
      Pe !== null && (St ? (e = Pe, n = n.stateNode, e.nodeType === 8 ? Cs(e.parentNode, n) : e.nodeType === 1 && Cs(e, n), po(e)) : Cs(Pe, n.stateNode));
      break;
    case 4:
      r = Pe, o = St, Pe = n.stateNode.containerInfo, St = !0, Zt(e, t, n), Pe = r, St = o;
      break;
    case 0:
    case 11:
    case 14:
    case 15:
      if (!ze && (r = n.updateQueue, r !== null && (r = r.lastEffect, r !== null))) {
        o = r = r.next;
        do {
          var i = o, l = i.destroy;
          i = i.tag, l !== void 0 && (i & 2 || i & 4) && $a(n, t, l), o = o.next;
        } while (o !== r);
      }
      Zt(e, t, n);
      break;
    case 1:
      if (!ze && (or(n, t), r = n.stateNode, typeof r.componentWillUnmount == "function"))
        try {
          r.props = n.memoizedProps, r.state = n.memoizedState, r.componentWillUnmount();
        } catch (s) {
          ue(n, t, s);
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
function wf(e) {
  var t = e.updateQueue;
  if (t !== null) {
    e.updateQueue = null;
    var n = e.stateNode;
    n === null && (n = e.stateNode = new py()), t.forEach(function(r) {
      var o = Cy.bind(null, e, r);
      n.has(r) || (n.add(r), r.then(o, o));
    });
  }
}
function vt(e, t) {
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
        _m(i, l, o), Pe = null, St = !1;
        var a = o.alternate;
        a !== null && (a.return = null), o.return = null;
      } catch (u) {
        ue(o, t, u);
      }
    }
  if (t.subtreeFlags & 12854)
    for (t = t.child; t !== null; )
      Pm(t, e), t = t.sibling;
}
function Pm(e, t) {
  var n = e.alternate, r = e.flags;
  switch (e.tag) {
    case 0:
    case 11:
    case 14:
    case 15:
      if (vt(t, e), Tt(e), r & 4) {
        try {
          ro(3, e, e.return), ml(3, e);
        } catch (g) {
          ue(e, e.return, g);
        }
        try {
          ro(5, e, e.return);
        } catch (g) {
          ue(e, e.return, g);
        }
      }
      break;
    case 1:
      vt(t, e), Tt(e), r & 512 && n !== null && or(n, n.return);
      break;
    case 5:
      if (vt(t, e), Tt(e), r & 512 && n !== null && or(n, n.return), e.flags & 32) {
        var o = e.stateNode;
        try {
          ao(o, "");
        } catch (g) {
          ue(e, e.return, g);
        }
      }
      if (r & 4 && (o = e.stateNode, o != null)) {
        var i = e.memoizedProps, l = n !== null ? n.memoizedProps : i, s = e.type, a = e.updateQueue;
        if (e.updateQueue = null, a !== null)
          try {
            s === "input" && i.type === "radio" && i.name != null && Qd(o, i), ea(s, l);
            var u = ea(s, i);
            for (l = 0; l < a.length; l += 2) {
              var c = a[l], d = a[l + 1];
              c === "style" ? Jd(o, d) : c === "dangerouslySetInnerHTML" ? Zd(o, d) : c === "children" ? ao(o, d) : Ja(o, c, d, u);
            }
            switch (s) {
              case "input":
                Ys(o, i);
                break;
              case "textarea":
                Yd(o, i);
                break;
              case "select":
                var m = o._wrapperState.wasMultiple;
                o._wrapperState.wasMultiple = !!i.multiple;
                var v = i.value;
                v != null ? lr(o, !!i.multiple, v, !1) : m !== !!i.multiple && (i.defaultValue != null ? lr(
                  o,
                  !!i.multiple,
                  i.defaultValue,
                  !0
                ) : lr(o, !!i.multiple, i.multiple ? [] : "", !1));
            }
            o[vo] = i;
          } catch (g) {
            ue(e, e.return, g);
          }
      }
      break;
    case 6:
      if (vt(t, e), Tt(e), r & 4) {
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
      if (vt(t, e), Tt(e), r & 4 && n !== null && n.memoizedState.isDehydrated)
        try {
          po(t.containerInfo);
        } catch (g) {
          ue(e, e.return, g);
        }
      break;
    case 4:
      vt(t, e), Tt(e);
      break;
    case 13:
      vt(t, e), Tt(e), o = e.child, o.flags & 8192 && (i = o.memoizedState !== null, o.stateNode.isHidden = i, !i || o.alternate !== null && o.alternate.memoizedState !== null || (Nu = ce())), r & 4 && wf(e);
      break;
    case 22:
      if (c = n !== null && n.memoizedState !== null, e.mode & 1 ? (ze = (u = ze) || c, vt(t, e), ze = u) : vt(t, e), Tt(e), r & 8192) {
        if (u = e.memoizedState !== null, (e.stateNode.isHidden = u) && !c && e.mode & 1)
          for (M = e, c = e.child; c !== null; ) {
            for (d = M = c; M !== null; ) {
              switch (m = M, v = m.child, m.tag) {
                case 0:
                case 11:
                case 14:
                case 15:
                  ro(4, m, m.return);
                  break;
                case 1:
                  or(m, m.return);
                  var y = m.stateNode;
                  if (typeof y.componentWillUnmount == "function") {
                    r = m, n = m.return;
                    try {
                      t = r, y.props = t.memoizedProps, y.state = t.memoizedState, y.componentWillUnmount();
                    } catch (g) {
                      ue(r, n, g);
                    }
                  }
                  break;
                case 5:
                  or(m, m.return);
                  break;
                case 22:
                  if (m.memoizedState !== null) {
                    Cf(d);
                    continue;
                  }
              }
              v !== null ? (v.return = m, M = v) : Cf(d);
            }
            c = c.sibling;
          }
        e:
          for (c = null, d = e; ; ) {
            if (d.tag === 5) {
              if (c === null) {
                c = d;
                try {
                  o = d.stateNode, u ? (i = o.style, typeof i.setProperty == "function" ? i.setProperty("display", "none", "important") : i.display = "none") : (s = d.stateNode, a = d.memoizedProps.style, l = a != null && a.hasOwnProperty("display") ? a.display : null, s.style.display = qd("display", l));
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
      vt(t, e), Tt(e), r & 4 && wf(e);
      break;
    case 21:
      break;
    default:
      vt(
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
          if (Em(n)) {
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
          r.flags & 32 && (ao(o, ""), r.flags &= -33);
          var i = Sf(e);
          Oa(e, i, o);
          break;
        case 3:
        case 4:
          var l = r.stateNode.containerInfo, s = Sf(e);
          Ra(e, s, l);
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
function hy(e, t, n) {
  M = e, $m(e);
}
function $m(e, t, n) {
  for (var r = (e.mode & 1) !== 0; M !== null; ) {
    var o = M, i = o.child;
    if (o.tag === 22 && r) {
      var l = o.memoizedState !== null || li;
      if (!l) {
        var s = o.alternate, a = s !== null && s.memoizedState !== null || ze;
        s = li;
        var u = ze;
        if (li = l, (ze = a) && !u)
          for (M = o; M !== null; )
            l = M, a = l.child, l.tag === 22 && l.memoizedState !== null ? Ef(o) : a !== null ? (a.return = l, M = a) : Ef(o);
        for (; i !== null; )
          M = i, $m(i), i = i.sibling;
        M = o, li = s, ze = u;
      }
      kf(e);
    } else
      o.subtreeFlags & 8772 && i !== null ? (i.return = o, M = i) : kf(e);
  }
}
function kf(e) {
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
              ze || ml(5, t);
              break;
            case 1:
              var r = t.stateNode;
              if (t.flags & 4 && !ze)
                if (n === null)
                  r.componentDidMount();
                else {
                  var o = t.elementType === t.type ? n.memoizedProps : xt(t.type, n.memoizedProps);
                  r.componentDidUpdate(o, n.memoizedState, r.__reactInternalSnapshotBeforeUpdate);
                }
              var i = t.updateQueue;
              i !== null && lf(t, i, r);
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
                lf(t, l, n);
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
                    d !== null && po(d);
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
        ze || t.flags & 512 && Ta(t);
      } catch (m) {
        ue(t, t.return, m);
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
function Cf(e) {
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
function Ef(e) {
  for (; M !== null; ) {
    var t = M;
    try {
      switch (t.tag) {
        case 0:
        case 11:
        case 15:
          var n = t.return;
          try {
            ml(4, t);
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
            Ta(t);
          } catch (a) {
            ue(t, i, a);
          }
          break;
        case 5:
          var l = t.return;
          try {
            Ta(t);
          } catch (a) {
            ue(t, l, a);
          }
      }
    } catch (a) {
      ue(t, t.return, a);
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
var gy = Math.ceil, Qi = Qt.ReactCurrentDispatcher, Ou = Qt.ReactCurrentOwner, ut = Qt.ReactCurrentBatchConfig, D = 0, ke = null, he = null, Te = 0, Ke = 0, ir = xn(0), xe = 0, Eo = null, In = 0, hl = 0, Mu = 0, oo = null, be = null, Nu = 0, wr = 1 / 0, At = null, Yi = !1, Ma = null, dn = null, si = !1, ln = null, Xi = 0, io = 0, Na = null, wi = -1, ki = 0;
function Ae() {
  return D & 6 ? ce() : wi !== -1 ? wi : wi = ce();
}
function pn(e) {
  return e.mode & 1 ? D & 2 && Te !== 0 ? Te & -Te : Jg.transition !== null ? (ki === 0 && (ki = fp()), ki) : (e = V, e !== 0 || (e = window.event, e = e === void 0 ? 16 : vp(e.type)), e) : 1;
}
function Et(e, t, n, r) {
  if (50 < io)
    throw io = 0, Na = null, Error(P(185));
  zo(e, n, r), (!(D & 2) || e !== ke) && (e === ke && (!(D & 2) && (hl |= n), xe === 4 && nn(e, Te)), Ve(e, r), n === 1 && D === 0 && !(t.mode & 1) && (wr = ce() + 500, fl && Sn()));
}
function Ve(e, t) {
  var n = e.callbackNode;
  J0(e, t);
  var r = zi(e, e === ke ? Te : 0);
  if (r === 0)
    n !== null && Nc(n), e.callbackNode = null, e.callbackPriority = 0;
  else if (t = r & -r, e.callbackPriority !== t) {
    if (n != null && Nc(n), t === 1)
      e.tag === 0 ? qg(_f.bind(null, e)) : Ap(_f.bind(null, e)), Qg(function() {
        !(D & 6) && Sn();
      }), n = null;
    else {
      switch (dp(r)) {
        case 1:
          n = ou;
          break;
        case 4:
          n = up;
          break;
        case 16:
          n = Ni;
          break;
        case 536870912:
          n = cp;
          break;
        default:
          n = Ni;
      }
      n = Im(n, Tm.bind(null, e));
    }
    e.callbackPriority = t, e.callbackNode = n;
  }
}
function Tm(e, t) {
  if (wi = -1, ki = 0, D & 6)
    throw Error(P(327));
  var n = e.callbackNode;
  if (fr() && e.callbackNode !== n)
    return null;
  var r = zi(e, e === ke ? Te : 0);
  if (r === 0)
    return null;
  if (r & 30 || r & e.expiredLanes || t)
    t = Zi(e, r);
  else {
    t = r;
    var o = D;
    D |= 2;
    var i = Om();
    (ke !== e || Te !== t) && (At = null, wr = ce() + 500, Rn(e, t));
    do
      try {
        xy();
        break;
      } catch (s) {
        Rm(e, s);
      }
    while (1);
    yu(), Qi.current = i, D = o, he !== null ? t = 0 : (ke = null, Te = 0, t = xe);
  }
  if (t !== 0) {
    if (t === 2 && (o = ia(e), o !== 0 && (r = o, t = za(e, o))), t === 1)
      throw n = Eo, Rn(e, 0), nn(e, r), Ve(e, ce()), n;
    if (t === 6)
      nn(e, r);
    else {
      if (o = e.current.alternate, !(r & 30) && !yy(o) && (t = Zi(e, r), t === 2 && (i = ia(e), i !== 0 && (r = i, t = za(e, i))), t === 1))
        throw n = Eo, Rn(e, 0), nn(e, r), Ve(e, ce()), n;
      switch (e.finishedWork = o, e.finishedLanes = r, t) {
        case 0:
        case 1:
          throw Error(P(345));
        case 2:
          kn(e, be, At);
          break;
        case 3:
          if (nn(e, r), (r & 130023424) === r && (t = Nu + 500 - ce(), 10 < t)) {
            if (zi(e, 0) !== 0)
              break;
            if (o = e.suspendedLanes, (o & r) !== r) {
              Ae(), e.pingedLanes |= e.suspendedLanes & o;
              break;
            }
            e.timeoutHandle = pa(kn.bind(null, e, be, At), t);
            break;
          }
          kn(e, be, At);
          break;
        case 4:
          if (nn(e, r), (r & 4194240) === r)
            break;
          for (t = e.eventTimes, o = -1; 0 < r; ) {
            var l = 31 - Ct(r);
            i = 1 << l, l = t[l], l > o && (o = l), r &= ~i;
          }
          if (r = o, r = ce() - r, r = (120 > r ? 120 : 480 > r ? 480 : 1080 > r ? 1080 : 1920 > r ? 1920 : 3e3 > r ? 3e3 : 4320 > r ? 4320 : 1960 * gy(r / 1960)) - r, 10 < r) {
            e.timeoutHandle = pa(kn.bind(null, e, be, At), r);
            break;
          }
          kn(e, be, At);
          break;
        case 5:
          kn(e, be, At);
          break;
        default:
          throw Error(P(329));
      }
    }
  }
  return Ve(e, ce()), e.callbackNode === n ? Tm.bind(null, e) : null;
}
function za(e, t) {
  var n = oo;
  return e.current.memoizedState.isDehydrated && (Rn(e, t).flags |= 256), e = Zi(e, t), e !== 2 && (t = be, be = n, t !== null && ja(t)), e;
}
function ja(e) {
  be === null ? be = e : be.push.apply(be, e);
}
function yy(e) {
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
function nn(e, t) {
  for (t &= ~Mu, t &= ~hl, e.suspendedLanes |= t, e.pingedLanes &= ~t, e = e.expirationTimes; 0 < t; ) {
    var n = 31 - Ct(t), r = 1 << n;
    e[n] = -1, t &= ~r;
  }
}
function _f(e) {
  if (D & 6)
    throw Error(P(327));
  fr();
  var t = zi(e, 0);
  if (!(t & 1))
    return Ve(e, ce()), null;
  var n = Zi(e, t);
  if (e.tag !== 0 && n === 2) {
    var r = ia(e);
    r !== 0 && (t = r, n = za(e, r));
  }
  if (n === 1)
    throw n = Eo, Rn(e, 0), nn(e, t), Ve(e, ce()), n;
  if (n === 6)
    throw Error(P(345));
  return e.finishedWork = e.current.alternate, e.finishedLanes = t, kn(e, be, At), Ve(e, ce()), null;
}
function zu(e, t) {
  var n = D;
  D |= 1;
  try {
    return e(t);
  } finally {
    D = n, D === 0 && (wr = ce() + 500, fl && Sn());
  }
}
function Ln(e) {
  ln !== null && ln.tag === 0 && !(D & 6) && fr();
  var t = D;
  D |= 1;
  var n = ut.transition, r = V;
  try {
    if (ut.transition = null, V = 1, e)
      return e();
  } finally {
    V = r, ut.transition = n, D = t, !(D & 6) && Sn();
  }
}
function ju() {
  Ke = ir.current, Z(ir);
}
function Rn(e, t) {
  e.finishedWork = null, e.finishedLanes = 0;
  var n = e.timeoutHandle;
  if (n !== -1 && (e.timeoutHandle = -1, Gg(n)), he !== null)
    for (n = he.return; n !== null; ) {
      var r = n;
      switch (mu(r), r.tag) {
        case 1:
          r = r.type.childContextTypes, r != null && Di();
          break;
        case 3:
          xr(), Z(We), Z(je), Cu();
          break;
        case 5:
          ku(r);
          break;
        case 4:
          xr();
          break;
        case 13:
          Z(te);
          break;
        case 19:
          Z(te);
          break;
        case 10:
          vu(r.type._context);
          break;
        case 22:
        case 23:
          ju();
      }
      n = n.return;
    }
  if (ke = e, he = e = mn(e.current, null), Te = Ke = t, xe = 0, Eo = null, Mu = hl = In = 0, be = oo = null, Pn !== null) {
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
function Rm(e, t) {
  do {
    var n = he;
    try {
      if (yu(), vi.current = Gi, Ki) {
        for (var r = re.memoizedState; r !== null; ) {
          var o = r.queue;
          o !== null && (o.pending = null), r = r.next;
        }
        Ki = !1;
      }
      if (jn = 0, we = ve = re = null, no = !1, wo = 0, Ou.current = null, n === null || n.return === null) {
        xe = 1, Eo = t, he = null;
        break;
      }
      e: {
        var i = e, l = n.return, s = n, a = t;
        if (t = Te, s.flags |= 32768, a !== null && typeof a == "object" && typeof a.then == "function") {
          var u = a, c = s, d = c.tag;
          if (!(c.mode & 1) && (d === 0 || d === 11 || d === 15)) {
            var m = c.alternate;
            m ? (c.updateQueue = m.updateQueue, c.memoizedState = m.memoizedState, c.lanes = m.lanes) : (c.updateQueue = null, c.memoizedState = null);
          }
          var v = df(l);
          if (v !== null) {
            v.flags &= -257, pf(v, l, s, i, t), v.mode & 1 && ff(i, u, t), t = v, a = u;
            var y = t.updateQueue;
            if (y === null) {
              var g = /* @__PURE__ */ new Set();
              g.add(a), t.updateQueue = g;
            } else
              y.add(a);
            break e;
          } else {
            if (!(t & 1)) {
              ff(i, u, t), Iu();
              break e;
            }
            a = Error(P(426));
          }
        } else if (ee && s.mode & 1) {
          var $ = df(l);
          if ($ !== null) {
            !($.flags & 65536) && ($.flags |= 256), pf($, l, s, i, t), hu(Sr(a, s));
            break e;
          }
        }
        i = a = Sr(a, s), xe !== 4 && (xe = 2), oo === null ? oo = [i] : oo.push(i), i = l;
        do {
          switch (i.tag) {
            case 3:
              i.flags |= 65536, t &= -t, i.lanes |= t;
              var p = dm(i, a, t);
              of(i, p);
              break e;
            case 1:
              s = a;
              var f = i.type, h = i.stateNode;
              if (!(i.flags & 128) && (typeof f.getDerivedStateFromError == "function" || h !== null && typeof h.componentDidCatch == "function" && (dn === null || !dn.has(h)))) {
                i.flags |= 65536, t &= -t, i.lanes |= t;
                var x = pm(i, s, t);
                of(i, x);
                break e;
              }
          }
          i = i.return;
        } while (i !== null);
      }
      Nm(n);
    } catch (E) {
      t = E, he === n && n !== null && (he = n = n.return);
      continue;
    }
    break;
  } while (1);
}
function Om() {
  var e = Qi.current;
  return Qi.current = Gi, e === null ? Gi : e;
}
function Iu() {
  (xe === 0 || xe === 3 || xe === 2) && (xe = 4), ke === null || !(In & 268435455) && !(hl & 268435455) || nn(ke, Te);
}
function Zi(e, t) {
  var n = D;
  D |= 2;
  var r = Om();
  (ke !== e || Te !== t) && (At = null, Rn(e, t));
  do
    try {
      vy();
      break;
    } catch (o) {
      Rm(e, o);
    }
  while (1);
  if (yu(), D = n, Qi.current = r, he !== null)
    throw Error(P(261));
  return ke = null, Te = 0, xe;
}
function vy() {
  for (; he !== null; )
    Mm(he);
}
function xy() {
  for (; he !== null && !V0(); )
    Mm(he);
}
function Mm(e) {
  var t = jm(e.alternate, e, Ke);
  e.memoizedProps = e.pendingProps, t === null ? Nm(e) : he = t, Ou.current = null;
}
function Nm(e) {
  var t = e;
  do {
    var n = t.alternate;
    if (e = t.return, t.flags & 32768) {
      if (n = dy(n, t), n !== null) {
        n.flags &= 32767, he = n;
        return;
      }
      if (e !== null)
        e.flags |= 32768, e.subtreeFlags = 0, e.deletions = null;
      else {
        xe = 6, he = null;
        return;
      }
    } else if (n = fy(n, t, Ke), n !== null) {
      he = n;
      return;
    }
    if (t = t.sibling, t !== null) {
      he = t;
      return;
    }
    he = t = e;
  } while (t !== null);
  xe === 0 && (xe = 5);
}
function kn(e, t, n) {
  var r = V, o = ut.transition;
  try {
    ut.transition = null, V = 1, Sy(e, t, n, r);
  } finally {
    ut.transition = o, V = r;
  }
  return null;
}
function Sy(e, t, n, r) {
  do
    fr();
  while (ln !== null);
  if (D & 6)
    throw Error(P(327));
  n = e.finishedWork;
  var o = e.finishedLanes;
  if (n === null)
    return null;
  if (e.finishedWork = null, e.finishedLanes = 0, n === e.current)
    throw Error(P(177));
  e.callbackNode = null, e.callbackPriority = 0;
  var i = n.lanes | n.childLanes;
  if (eg(e, i), e === ke && (he = ke = null, Te = 0), !(n.subtreeFlags & 2064) && !(n.flags & 2064) || si || (si = !0, Im(Ni, function() {
    return fr(), null;
  })), i = (n.flags & 15990) !== 0, n.subtreeFlags & 15990 || i) {
    i = ut.transition, ut.transition = null;
    var l = V;
    V = 1;
    var s = D;
    D |= 4, Ou.current = null, my(e, n), Pm(n, e), bg(fa), ji = !!ca, fa = ca = null, e.current = n, hy(n), H0(), D = s, V = l, ut.transition = i;
  } else
    e.current = n;
  if (si && (si = !1, ln = e, Xi = o), i = e.pendingLanes, i === 0 && (dn = null), Q0(n.stateNode), Ve(e, ce()), t !== null)
    for (r = e.onRecoverableError, n = 0; n < t.length; n++)
      o = t[n], r(o.value, { componentStack: o.stack, digest: o.digest });
  if (Yi)
    throw Yi = !1, e = Ma, Ma = null, e;
  return Xi & 1 && e.tag !== 0 && fr(), i = e.pendingLanes, i & 1 ? e === Na ? io++ : (io = 0, Na = e) : io = 0, Sn(), null;
}
function fr() {
  if (ln !== null) {
    var e = dp(Xi), t = ut.transition, n = V;
    try {
      if (ut.transition = null, V = 16 > e ? 16 : e, ln === null)
        var r = !1;
      else {
        if (e = ln, ln = null, Xi = 0, D & 6)
          throw Error(P(331));
        var o = D;
        for (D |= 4, M = e.current; M !== null; ) {
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
                      ro(8, c, i);
                  }
                  var d = c.child;
                  if (d !== null)
                    d.return = c, M = d;
                  else
                    for (; M !== null; ) {
                      c = M;
                      var m = c.sibling, v = c.return;
                      if (Cm(c), c === u) {
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
                      ro(9, i, i.return);
                  }
                var p = i.sibling;
                if (p !== null) {
                  p.return = i.return, M = p;
                  break e;
                }
                M = i.return;
              }
        }
        var f = e.current;
        for (M = f; M !== null; ) {
          l = M;
          var h = l.child;
          if (l.subtreeFlags & 2064 && h !== null)
            h.return = l, M = h;
          else
            e:
              for (l = f; M !== null; ) {
                if (s = M, s.flags & 2048)
                  try {
                    switch (s.tag) {
                      case 0:
                      case 11:
                      case 15:
                        ml(9, s);
                    }
                  } catch (E) {
                    ue(s, s.return, E);
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
        if (D = o, Sn(), zt && typeof zt.onPostCommitFiberRoot == "function")
          try {
            zt.onPostCommitFiberRoot(ll, e);
          } catch {
          }
        r = !0;
      }
      return r;
    } finally {
      V = n, ut.transition = t;
    }
  }
  return !1;
}
function Pf(e, t, n) {
  t = Sr(n, t), t = dm(e, t, 1), e = fn(e, t, 1), t = Ae(), e !== null && (zo(e, 1, t), Ve(e, t));
}
function ue(e, t, n) {
  if (e.tag === 3)
    Pf(e, e, n);
  else
    for (; t !== null; ) {
      if (t.tag === 3) {
        Pf(t, e, n);
        break;
      } else if (t.tag === 1) {
        var r = t.stateNode;
        if (typeof t.type.getDerivedStateFromError == "function" || typeof r.componentDidCatch == "function" && (dn === null || !dn.has(r))) {
          e = Sr(n, e), e = pm(t, e, 1), t = fn(t, e, 1), e = Ae(), t !== null && (zo(t, 1, e), Ve(t, e));
          break;
        }
      }
      t = t.return;
    }
}
function wy(e, t, n) {
  var r = e.pingCache;
  r !== null && r.delete(t), t = Ae(), e.pingedLanes |= e.suspendedLanes & n, ke === e && (Te & n) === n && (xe === 4 || xe === 3 && (Te & 130023424) === Te && 500 > ce() - Nu ? Rn(e, 0) : Mu |= n), Ve(e, t);
}
function zm(e, t) {
  t === 0 && (e.mode & 1 ? (t = Zo, Zo <<= 1, !(Zo & 130023424) && (Zo = 4194304)) : t = 1);
  var n = Ae();
  e = Ht(e, t), e !== null && (zo(e, t, n), Ve(e, n));
}
function ky(e) {
  var t = e.memoizedState, n = 0;
  t !== null && (n = t.retryLane), zm(e, n);
}
function Cy(e, t) {
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
  r !== null && r.delete(t), zm(e, n);
}
var jm;
jm = function(e, t, n) {
  if (e !== null)
    if (e.memoizedProps !== t.pendingProps || We.current)
      Be = !0;
    else {
      if (!(e.lanes & n) && !(t.flags & 128))
        return Be = !1, cy(e, t, n);
      Be = !!(e.flags & 131072);
    }
  else
    Be = !1, ee && t.flags & 1048576 && Dp(t, Bi, t.index);
  switch (t.lanes = 0, t.tag) {
    case 2:
      var r = t.type;
      Si(e, t), e = t.pendingProps;
      var o = gr(t, je.current);
      cr(t, n), o = _u(null, t, r, e, o, n);
      var i = Pu();
      return t.flags |= 1, typeof o == "object" && o !== null && typeof o.render == "function" && o.$$typeof === void 0 ? (t.tag = 1, t.memoizedState = null, t.updateQueue = null, Ue(r) ? (i = !0, Fi(t)) : i = !1, t.memoizedState = o.state !== null && o.state !== void 0 ? o.state : null, Su(t), o.updater = pl, t.stateNode = o, o._reactInternals = t, Sa(t, r, e, n), t = Ca(null, t, r, !0, i, n)) : (t.tag = 0, ee && i && pu(t), Le(null, t, o, n), t = t.child), t;
    case 16:
      r = t.elementType;
      e: {
        switch (Si(e, t), e = t.pendingProps, o = r._init, r = o(r._payload), t.type = r, o = t.tag = _y(r), e = xt(r, e), o) {
          case 0:
            t = ka(null, t, r, e, n);
            break e;
          case 1:
            t = gf(null, t, r, e, n);
            break e;
          case 11:
            t = mf(null, t, r, e, n);
            break e;
          case 14:
            t = hf(null, t, r, xt(r.type, e), n);
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
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : xt(r, o), ka(e, t, r, o, n);
    case 1:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : xt(r, o), gf(e, t, r, o, n);
    case 3:
      e: {
        if (ym(t), e === null)
          throw Error(P(387));
        r = t.pendingProps, i = t.memoizedState, o = i.element, Vp(e, t), Vi(t, r, null, n);
        var l = t.memoizedState;
        if (r = l.element, i.isDehydrated)
          if (i = { element: r, isDehydrated: !1, cache: l.cache, pendingSuspenseBoundaries: l.pendingSuspenseBoundaries, transitions: l.transitions }, t.updateQueue.baseState = i, t.memoizedState = i, t.flags & 256) {
            o = Sr(Error(P(423)), t), t = yf(e, t, r, n, o);
            break e;
          } else if (r !== o) {
            o = Sr(Error(P(424)), t), t = yf(e, t, r, n, o);
            break e;
          } else
            for (Qe = cn(t.stateNode.containerInfo.firstChild), Ye = t, ee = !0, wt = null, n = Wp(t, null, r, n), t.child = n; n; )
              n.flags = n.flags & -3 | 4096, n = n.sibling;
        else {
          if (yr(), r === o) {
            t = Kt(e, t, n);
            break e;
          }
          Le(e, t, r, n);
        }
        t = t.child;
      }
      return t;
    case 5:
      return Hp(t), e === null && ya(t), r = t.type, o = t.pendingProps, i = e !== null ? e.memoizedProps : null, l = o.children, da(r, o) ? l = null : i !== null && da(r, i) && (t.flags |= 32), gm(e, t), Le(e, t, l, n), t.child;
    case 6:
      return e === null && ya(t), null;
    case 13:
      return vm(e, t, n);
    case 4:
      return wu(t, t.stateNode.containerInfo), r = t.pendingProps, e === null ? t.child = vr(t, null, r, n) : Le(e, t, r, n), t.child;
    case 11:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : xt(r, o), mf(e, t, r, o, n);
    case 7:
      return Le(e, t, t.pendingProps, n), t.child;
    case 8:
      return Le(e, t, t.pendingProps.children, n), t.child;
    case 12:
      return Le(e, t, t.pendingProps.children, n), t.child;
    case 10:
      e: {
        if (r = t.type._context, o = t.pendingProps, i = t.memoizedProps, l = o.value, Q(Wi, r._currentValue), r._currentValue = l, i !== null)
          if (_t(i.value, l)) {
            if (i.children === o.children && !We.current) {
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
        Le(e, t, o.children, n), t = t.child;
      }
      return t;
    case 9:
      return o = t.type, r = t.pendingProps.children, cr(t, n), o = ct(o), r = r(o), t.flags |= 1, Le(e, t, r, n), t.child;
    case 14:
      return r = t.type, o = xt(r, t.pendingProps), o = xt(r.type, o), hf(e, t, r, o, n);
    case 15:
      return mm(e, t, t.type, t.pendingProps, n);
    case 17:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : xt(r, o), Si(e, t), t.tag = 1, Ue(r) ? (e = !0, Fi(t)) : e = !1, cr(t, n), fm(t, r, o), Sa(t, r, o, n), Ca(null, t, r, !0, e, n);
    case 19:
      return xm(e, t, n);
    case 22:
      return hm(e, t, n);
  }
  throw Error(P(156, t.tag));
};
function Im(e, t) {
  return ap(e, t);
}
function Ey(e, t, n, r) {
  this.tag = e, this.key = n, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.ref = null, this.pendingProps = t, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = r, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
}
function at(e, t, n, r) {
  return new Ey(e, t, n, r);
}
function Lu(e) {
  return e = e.prototype, !(!e || !e.isReactComponent);
}
function _y(e) {
  if (typeof e == "function")
    return Lu(e) ? 1 : 0;
  if (e != null) {
    if (e = e.$$typeof, e === tu)
      return 11;
    if (e === nu)
      return 14;
  }
  return 2;
}
function mn(e, t) {
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
        case Yn:
          return On(n.children, o, i, t);
        case eu:
          l = 8, o |= 8;
          break;
        case Vs:
          return e = at(12, n, t, o | 2), e.elementType = Vs, e.lanes = i, e;
        case Hs:
          return e = at(13, n, t, o), e.elementType = Hs, e.lanes = i, e;
        case Ks:
          return e = at(19, n, t, o), e.elementType = Ks, e.lanes = i, e;
        case Hd:
          return gl(n, o, i, t);
        default:
          if (typeof e == "object" && e !== null)
            switch (e.$$typeof) {
              case Ud:
                l = 10;
                break e;
              case Vd:
                l = 9;
                break e;
              case tu:
                l = 11;
                break e;
              case nu:
                l = 14;
                break e;
              case Jt:
                l = 16, r = null;
                break e;
            }
          throw Error(P(130, e == null ? e : typeof e, ""));
      }
  return t = at(l, n, t, o), t.elementType = e, t.type = r, t.lanes = i, t;
}
function On(e, t, n, r) {
  return e = at(7, e, r, t), e.lanes = n, e;
}
function gl(e, t, n, r) {
  return e = at(22, e, r, t), e.elementType = Hd, e.lanes = n, e.stateNode = { isHidden: !1 }, e;
}
function Ms(e, t, n) {
  return e = at(6, e, null, t), e.lanes = n, e;
}
function Ns(e, t, n) {
  return t = at(4, e.children !== null ? e.children : [], e.key, t), t.lanes = n, t.stateNode = { containerInfo: e.containerInfo, pendingChildren: null, implementation: e.implementation }, t;
}
function Py(e, t, n, r, o) {
  this.tag = t, this.containerInfo = e, this.finishedWork = this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.pendingContext = this.context = null, this.callbackPriority = 0, this.eventTimes = ds(0), this.expirationTimes = ds(-1), this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = ds(0), this.identifierPrefix = r, this.onRecoverableError = o, this.mutableSourceEagerHydrationData = null;
}
function Au(e, t, n, r, o, i, l, s, a) {
  return e = new Py(e, t, n, s, a), t === 1 ? (t = 1, i === !0 && (t |= 8)) : t = 0, i = at(3, null, null, t), e.current = i, i.stateNode = e, i.memoizedState = { element: r, isDehydrated: n, cache: null, transitions: null, pendingSuspenseBoundaries: null }, Su(i), e;
}
function $y(e, t, n) {
  var r = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
  return { $$typeof: Qn, key: r == null ? null : "" + r, children: e, containerInfo: t, implementation: n };
}
function Lm(e) {
  if (!e)
    return yn;
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
      return Lp(e, n, t);
  }
  return t;
}
function Am(e, t, n, r, o, i, l, s, a) {
  return e = Au(n, r, !0, e, o, i, l, s, a), e.context = Lm(null), n = e.current, r = Ae(), o = pn(n), i = Wt(r, o), i.callback = t ?? null, fn(n, i, o), e.current.lanes = o, zo(e, o, r), Ve(e, r), e;
}
function yl(e, t, n, r) {
  var o = t.current, i = Ae(), l = pn(o);
  return n = Lm(n), t.context === null ? t.context = n : t.pendingContext = n, t = Wt(i, l), t.payload = { element: e }, r = r === void 0 ? null : r, r !== null && (t.callback = r), e = fn(o, t, l), e !== null && (Et(e, o, l, i), yi(e, o, l)), l;
}
function qi(e) {
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
function Du(e, t) {
  $f(e, t), (e = e.alternate) && $f(e, t);
}
function Ty() {
  return null;
}
var Dm = typeof reportError == "function" ? reportError : function(e) {
  console.error(e);
};
function Fu(e) {
  this._internalRoot = e;
}
vl.prototype.render = Fu.prototype.render = function(e) {
  var t = this._internalRoot;
  if (t === null)
    throw Error(P(409));
  yl(e, t, null, null);
};
vl.prototype.unmount = Fu.prototype.unmount = function() {
  var e = this._internalRoot;
  if (e !== null) {
    this._internalRoot = null;
    var t = e.containerInfo;
    Ln(function() {
      yl(null, e, null, null);
    }), t[Vt] = null;
  }
};
function vl(e) {
  this._internalRoot = e;
}
vl.prototype.unstable_scheduleHydration = function(e) {
  if (e) {
    var t = hp();
    e = { blockedOn: null, target: e, priority: t };
    for (var n = 0; n < tn.length && t !== 0 && t < tn[n].priority; n++)
      ;
    tn.splice(n, 0, e), n === 0 && yp(e);
  }
};
function bu(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11);
}
function xl(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11 && (e.nodeType !== 8 || e.nodeValue !== " react-mount-point-unstable "));
}
function Tf() {
}
function Ry(e, t, n, r, o) {
  if (o) {
    if (typeof r == "function") {
      var i = r;
      r = function() {
        var u = qi(l);
        i.call(u);
      };
    }
    var l = Am(t, r, e, 0, null, !1, !1, "", Tf);
    return e._reactRootContainer = l, e[Vt] = l.current, go(e.nodeType === 8 ? e.parentNode : e), Ln(), l;
  }
  for (; o = e.lastChild; )
    e.removeChild(o);
  if (typeof r == "function") {
    var s = r;
    r = function() {
      var u = qi(a);
      s.call(u);
    };
  }
  var a = Au(e, 0, !1, null, null, !1, !1, "", Tf);
  return e._reactRootContainer = a, e[Vt] = a.current, go(e.nodeType === 8 ? e.parentNode : e), Ln(function() {
    yl(t, a, n, r);
  }), a;
}
function Sl(e, t, n, r, o) {
  var i = n._reactRootContainer;
  if (i) {
    var l = i;
    if (typeof o == "function") {
      var s = o;
      o = function() {
        var a = qi(l);
        s.call(a);
      };
    }
    yl(t, l, e, o);
  } else
    l = Ry(n, t, e, o, r);
  return qi(l);
}
pp = function(e) {
  switch (e.tag) {
    case 3:
      var t = e.stateNode;
      if (t.current.memoizedState.isDehydrated) {
        var n = Gr(t.pendingLanes);
        n !== 0 && (iu(t, n | 1), Ve(t, ce()), !(D & 6) && (wr = ce() + 500, Sn()));
      }
      break;
    case 13:
      Ln(function() {
        var r = Ht(e, 1);
        if (r !== null) {
          var o = Ae();
          Et(r, e, 1, o);
        }
      }), Du(e, 1);
  }
};
lu = function(e) {
  if (e.tag === 13) {
    var t = Ht(e, 134217728);
    if (t !== null) {
      var n = Ae();
      Et(t, e, 134217728, n);
    }
    Du(e, 134217728);
  }
};
mp = function(e) {
  if (e.tag === 13) {
    var t = pn(e), n = Ht(e, t);
    if (n !== null) {
      var r = Ae();
      Et(n, e, t, r);
    }
    Du(e, t);
  }
};
hp = function() {
  return V;
};
gp = function(e, t) {
  var n = V;
  try {
    return V = e, t();
  } finally {
    V = n;
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
            var o = cl(r);
            if (!o)
              throw Error(P(90));
            Gd(r), Ys(r, o);
          }
        }
      }
      break;
    case "textarea":
      Yd(e, n);
      break;
    case "select":
      t = n.value, t != null && lr(e, !!n.multiple, t, !1);
  }
};
np = zu;
rp = Ln;
var Oy = { usingClientEntryPoint: !1, Events: [Io, Jn, cl, ep, tp, zu] }, Br = { findFiberByHostInstance: _n, bundleType: 0, version: "18.3.1", rendererPackageName: "react-dom" }, My = { bundleType: Br.bundleType, version: Br.version, rendererPackageName: Br.rendererPackageName, rendererConfig: Br.rendererConfig, overrideHookState: null, overrideHookStateDeletePath: null, overrideHookStateRenamePath: null, overrideProps: null, overridePropsDeletePath: null, overridePropsRenamePath: null, setErrorHandler: null, setSuspenseHandler: null, scheduleUpdate: null, currentDispatcherRef: Qt.ReactCurrentDispatcher, findHostInstanceByFiber: function(e) {
  return e = lp(e), e === null ? null : e.stateNode;
}, findFiberByHostInstance: Br.findFiberByHostInstance || Ty, findHostInstancesForRefresh: null, scheduleRefresh: null, scheduleRoot: null, setRefreshHandler: null, getCurrentFiber: null, reconcilerVersion: "18.3.1-next-f1338f8080-20240426" };
if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u") {
  var ai = __REACT_DEVTOOLS_GLOBAL_HOOK__;
  if (!ai.isDisabled && ai.supportsFiber)
    try {
      ll = ai.inject(My), zt = ai;
    } catch {
    }
}
qe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = Oy;
qe.createPortal = function(e, t) {
  var n = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
  if (!bu(t))
    throw Error(P(200));
  return $y(e, t, null, n);
};
qe.createRoot = function(e, t) {
  if (!bu(e))
    throw Error(P(299));
  var n = !1, r = "", o = Dm;
  return t != null && (t.unstable_strictMode === !0 && (n = !0), t.identifierPrefix !== void 0 && (r = t.identifierPrefix), t.onRecoverableError !== void 0 && (o = t.onRecoverableError)), t = Au(e, 1, !1, null, null, n, !1, r, o), e[Vt] = t.current, go(e.nodeType === 8 ? e.parentNode : e), new Fu(t);
};
qe.findDOMNode = function(e) {
  if (e == null)
    return null;
  if (e.nodeType === 1)
    return e;
  var t = e._reactInternals;
  if (t === void 0)
    throw typeof e.render == "function" ? Error(P(188)) : (e = Object.keys(e).join(","), Error(P(268, e)));
  return e = lp(t), e = e === null ? null : e.stateNode, e;
};
qe.flushSync = function(e) {
  return Ln(e);
};
qe.hydrate = function(e, t, n) {
  if (!xl(t))
    throw Error(P(200));
  return Sl(null, e, t, !0, n);
};
qe.hydrateRoot = function(e, t, n) {
  if (!bu(e))
    throw Error(P(405));
  var r = n != null && n.hydratedSources || null, o = !1, i = "", l = Dm;
  if (n != null && (n.unstable_strictMode === !0 && (o = !0), n.identifierPrefix !== void 0 && (i = n.identifierPrefix), n.onRecoverableError !== void 0 && (l = n.onRecoverableError)), t = Am(t, null, e, 1, n ?? null, o, !1, i, l), e[Vt] = t.current, go(e), r)
    for (e = 0; e < r.length; e++)
      n = r[e], o = n._getVersion, o = o(n._source), t.mutableSourceEagerHydrationData == null ? t.mutableSourceEagerHydrationData = [n, o] : t.mutableSourceEagerHydrationData.push(
        n,
        o
      );
  return new vl(t);
};
qe.render = function(e, t, n) {
  if (!xl(t))
    throw Error(P(200));
  return Sl(null, e, t, !1, n);
};
qe.unmountComponentAtNode = function(e) {
  if (!xl(e))
    throw Error(P(40));
  return e._reactRootContainer ? (Ln(function() {
    Sl(null, null, e, !1, function() {
      e._reactRootContainer = null, e[Vt] = null;
    });
  }), !0) : !1;
};
qe.unstable_batchedUpdates = zu;
qe.unstable_renderSubtreeIntoContainer = function(e, t, n, r) {
  if (!xl(n))
    throw Error(P(200));
  if (e == null || e._reactInternals === void 0)
    throw Error(P(38));
  return Sl(e, t, n, !1, r);
};
qe.version = "18.3.1-next-f1338f8080-20240426";
function Fm() {
  if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function"))
    try {
      __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(Fm);
    } catch (e) {
      console.error(e);
    }
}
Fm(), Fd.exports = qe;
var bm = Fd.exports;
const ui = /* @__PURE__ */ $d(bm);
var Rf = bm;
Ws.createRoot = Rf.createRoot, Ws.hydrateRoot = Rf.hydrateRoot;
function _o(e) {
  let t = "https://mui.com/production-error/?code=" + e;
  for (let n = 1; n < arguments.length; n += 1)
    t += "&args[]=" + encodeURIComponent(arguments[n]);
  return "Minified MUI error #" + e + "; visit " + t + " for the full message.";
}
const Ny = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: _o
}, Symbol.toStringTag, { value: "Module" })), kr = "$$material";
function C() {
  return C = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t];
      for (var r in n)
        ({}).hasOwnProperty.call(n, r) && (e[r] = n[r]);
    }
    return e;
  }, C.apply(null, arguments);
}
function K(e, t) {
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
var zy = !1;
function jy(e) {
  if (e.sheet)
    return e.sheet;
  for (var t = 0; t < document.styleSheets.length; t++)
    if (document.styleSheets[t].ownerNode === e)
      return document.styleSheets[t];
}
function Iy(e) {
  var t = document.createElement("style");
  return t.setAttribute("data-emotion", e.key), e.nonce !== void 0 && t.setAttribute("nonce", e.nonce), t.appendChild(document.createTextNode("")), t.setAttribute("data-s", ""), t;
}
var Ly = /* @__PURE__ */ function() {
  function e(n) {
    var r = this;
    this._insertTag = function(o) {
      var i;
      r.tags.length === 0 ? r.insertionPoint ? i = r.insertionPoint.nextSibling : r.prepend ? i = r.container.firstChild : i = r.before : i = r.tags[r.tags.length - 1].nextSibling, r.container.insertBefore(o, i), r.tags.push(o);
    }, this.isSpeedy = n.speedy === void 0 ? !zy : n.speedy, this.tags = [], this.ctr = 0, this.nonce = n.nonce, this.key = n.key, this.container = n.container, this.prepend = n.prepend, this.insertionPoint = n.insertionPoint, this.before = null;
  }
  var t = e.prototype;
  return t.hydrate = function(r) {
    r.forEach(this._insertTag);
  }, t.insert = function(r) {
    this.ctr % (this.isSpeedy ? 65e3 : 1) === 0 && this._insertTag(Iy(this));
    var o = this.tags[this.tags.length - 1];
    if (this.isSpeedy) {
      var i = jy(o);
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
}(), Ne = "-ms-", Ji = "-moz-", B = "-webkit-", Bm = "comm", Bu = "rule", Wu = "decl", Ay = "@import", Wm = "@keyframes", Dy = "@layer", Fy = Math.abs, wl = String.fromCharCode, by = Object.assign;
function By(e, t) {
  return $e(e, 0) ^ 45 ? (((t << 2 ^ $e(e, 0)) << 2 ^ $e(e, 1)) << 2 ^ $e(e, 2)) << 2 ^ $e(e, 3) : 0;
}
function Um(e) {
  return e.trim();
}
function Wy(e, t) {
  return (e = t.exec(e)) ? e[0] : e;
}
function W(e, t, n) {
  return e.replace(t, n);
}
function Ia(e, t) {
  return e.indexOf(t);
}
function $e(e, t) {
  return e.charCodeAt(t) | 0;
}
function Po(e, t, n) {
  return e.slice(t, n);
}
function Ot(e) {
  return e.length;
}
function Uu(e) {
  return e.length;
}
function ci(e, t) {
  return t.push(e), e;
}
function Uy(e, t) {
  return e.map(t).join("");
}
var kl = 1, Cr = 1, Vm = 0, He = 0, me = 0, $r = "";
function Cl(e, t, n, r, o, i, l) {
  return { value: e, root: t, parent: n, type: r, props: o, children: i, line: kl, column: Cr, length: l, return: "" };
}
function Wr(e, t) {
  return by(Cl("", null, null, "", null, null, 0), e, { length: -e.length }, t);
}
function Vy() {
  return me;
}
function Hy() {
  return me = He > 0 ? $e($r, --He) : 0, Cr--, me === 10 && (Cr = 1, kl--), me;
}
function Xe() {
  return me = He < Vm ? $e($r, He++) : 0, Cr++, me === 10 && (Cr = 1, kl++), me;
}
function It() {
  return $e($r, He);
}
function Ei() {
  return He;
}
function Ao(e, t) {
  return Po($r, e, t);
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
function Hm(e) {
  return kl = Cr = 1, Vm = Ot($r = e), He = 0, [];
}
function Km(e) {
  return $r = "", e;
}
function _i(e) {
  return Um(Ao(He - 1, La(e === 91 ? e + 2 : e === 40 ? e + 1 : e)));
}
function Ky(e) {
  for (; (me = It()) && me < 33; )
    Xe();
  return $o(e) > 2 || $o(me) > 3 ? "" : " ";
}
function Gy(e, t) {
  for (; --t && Xe() && !(me < 48 || me > 102 || me > 57 && me < 65 || me > 70 && me < 97); )
    ;
  return Ao(e, Ei() + (t < 6 && It() == 32 && Xe() == 32));
}
function La(e) {
  for (; Xe(); )
    switch (me) {
      case e:
        return He;
      case 34:
      case 39:
        e !== 34 && e !== 39 && La(me);
        break;
      case 40:
        e === 41 && La(e);
        break;
      case 92:
        Xe();
        break;
    }
  return He;
}
function Qy(e, t) {
  for (; Xe() && e + me !== 47 + 10; )
    if (e + me === 42 + 42 && It() === 47)
      break;
  return "/*" + Ao(t, He - 1) + "*" + wl(e === 47 ? e : Xe());
}
function Yy(e) {
  for (; !$o(It()); )
    Xe();
  return Ao(e, He);
}
function Xy(e) {
  return Km(Pi("", null, null, null, [""], e = Hm(e), 0, [0], e));
}
function Pi(e, t, n, r, o, i, l, s, a) {
  for (var u = 0, c = 0, d = l, m = 0, v = 0, y = 0, g = 1, $ = 1, p = 1, f = 0, h = "", x = o, E = i, w = r, S = h; $; )
    switch (y = f, f = Xe()) {
      case 40:
        if (y != 108 && $e(S, d - 1) == 58) {
          Ia(S += W(_i(f), "&", "&\f"), "&\f") != -1 && (p = -1);
          break;
        }
      case 34:
      case 39:
      case 91:
        S += _i(f);
        break;
      case 9:
      case 10:
      case 13:
      case 32:
        S += Ky(y);
        break;
      case 92:
        S += Gy(Ei() - 1, 7);
        continue;
      case 47:
        switch (It()) {
          case 42:
          case 47:
            ci(Zy(Qy(Xe(), Ei()), t, n), a);
            break;
          default:
            S += "/";
        }
        break;
      case 123 * g:
        s[u++] = Ot(S) * p;
      case 125 * g:
      case 59:
      case 0:
        switch (f) {
          case 0:
          case 125:
            $ = 0;
          case 59 + c:
            p == -1 && (S = W(S, /\f/g, "")), v > 0 && Ot(S) - d && ci(v > 32 ? Mf(S + ";", r, n, d - 1) : Mf(W(S, " ", "") + ";", r, n, d - 2), a);
            break;
          case 59:
            S += ";";
          default:
            if (ci(w = Of(S, t, n, u, c, o, s, h, x = [], E = [], d), i), f === 123)
              if (c === 0)
                Pi(S, t, w, w, x, i, d, s, E);
              else
                switch (m === 99 && $e(S, 3) === 110 ? 100 : m) {
                  case 100:
                  case 108:
                  case 109:
                  case 115:
                    Pi(e, w, w, r && ci(Of(e, w, w, 0, 0, o, s, h, o, x = [], d), E), o, E, d, s, r ? x : E);
                    break;
                  default:
                    Pi(S, w, w, w, [""], E, 0, s, E);
                }
        }
        u = c = v = 0, g = p = 1, h = S = "", d = l;
        break;
      case 58:
        d = 1 + Ot(S), v = y;
      default:
        if (g < 1) {
          if (f == 123)
            --g;
          else if (f == 125 && g++ == 0 && Hy() == 125)
            continue;
        }
        switch (S += wl(f), f * g) {
          case 38:
            p = c > 0 ? 1 : (S += "\f", -1);
            break;
          case 44:
            s[u++] = (Ot(S) - 1) * p, p = 1;
            break;
          case 64:
            It() === 45 && (S += _i(Xe())), m = It(), c = d = Ot(h = S += Yy(Ei())), f++;
            break;
          case 45:
            y === 45 && Ot(S) == 2 && (g = 0);
        }
    }
  return i;
}
function Of(e, t, n, r, o, i, l, s, a, u, c) {
  for (var d = o - 1, m = o === 0 ? i : [""], v = Uu(m), y = 0, g = 0, $ = 0; y < r; ++y)
    for (var p = 0, f = Po(e, d + 1, d = Fy(g = l[y])), h = e; p < v; ++p)
      (h = Um(g > 0 ? m[p] + " " + f : W(f, /&\f/g, m[p]))) && (a[$++] = h);
  return Cl(e, t, n, o === 0 ? Bu : s, a, u, c);
}
function Zy(e, t, n) {
  return Cl(e, t, n, Bm, wl(Vy()), Po(e, 2, -2), 0);
}
function Mf(e, t, n, r) {
  return Cl(e, t, n, Wu, Po(e, 0, r), Po(e, r + 1, -1), r);
}
function dr(e, t) {
  for (var n = "", r = Uu(e), o = 0; o < r; o++)
    n += t(e[o], o, e, t) || "";
  return n;
}
function qy(e, t, n, r) {
  switch (e.type) {
    case Dy:
      if (e.children.length)
        break;
    case Ay:
    case Wu:
      return e.return = e.return || e.value;
    case Bm:
      return "";
    case Wm:
      return e.return = e.value + "{" + dr(e.children, r) + "}";
    case Bu:
      e.value = e.props.join(",");
  }
  return Ot(n = dr(e.children, r)) ? e.return = e.value + "{" + n + "}" : "";
}
function Jy(e) {
  var t = Uu(e);
  return function(n, r, o, i) {
    for (var l = "", s = 0; s < t; s++)
      l += e[s](n, r, o, i) || "";
    return l;
  };
}
function ev(e) {
  return function(t) {
    t.root || (t = t.return) && e(t);
  };
}
function Gm(e) {
  var t = /* @__PURE__ */ Object.create(null);
  return function(n) {
    return t[n] === void 0 && (t[n] = e(n)), t[n];
  };
}
var tv = function(t, n, r) {
  for (var o = 0, i = 0; o = i, i = It(), o === 38 && i === 12 && (n[r] = 1), !$o(i); )
    Xe();
  return Ao(t, He);
}, nv = function(t, n) {
  var r = -1, o = 44;
  do
    switch ($o(o)) {
      case 0:
        o === 38 && It() === 12 && (n[r] = 1), t[r] += tv(He - 1, n, r);
        break;
      case 2:
        t[r] += _i(o);
        break;
      case 4:
        if (o === 44) {
          t[++r] = It() === 58 ? "&\f" : "", n[r] = t[r].length;
          break;
        }
      default:
        t[r] += wl(o);
    }
  while (o = Xe());
  return t;
}, rv = function(t, n) {
  return Km(nv(Hm(t), n));
}, Nf = /* @__PURE__ */ new WeakMap(), ov = function(t) {
  if (!(t.type !== "rule" || !t.parent || // positive .length indicates that this rule contains pseudo
  // negative .length indicates that this rule has been already prefixed
  t.length < 1)) {
    for (var n = t.value, r = t.parent, o = t.column === r.column && t.line === r.line; r.type !== "rule"; )
      if (r = r.parent, !r)
        return;
    if (!(t.props.length === 1 && n.charCodeAt(0) !== 58 && !Nf.get(r)) && !o) {
      Nf.set(t, !0);
      for (var i = [], l = rv(n, i), s = r.props, a = 0, u = 0; a < l.length; a++)
        for (var c = 0; c < s.length; c++, u++)
          t.props[u] = i[a] ? l[a].replace(/&\f/g, s[c]) : s[c] + " " + l[a];
    }
  }
}, iv = function(t) {
  if (t.type === "decl") {
    var n = t.value;
    // charcode for l
    n.charCodeAt(0) === 108 && // charcode for b
    n.charCodeAt(2) === 98 && (t.return = "", t.value = "");
  }
};
function Qm(e, t) {
  switch (By(e, t)) {
    case 5103:
      return B + "print-" + e + e;
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
      return B + e + e;
    case 5349:
    case 4246:
    case 4810:
    case 6968:
    case 2756:
      return B + e + Ji + e + Ne + e + e;
    case 6828:
    case 4268:
      return B + e + Ne + e + e;
    case 6165:
      return B + e + Ne + "flex-" + e + e;
    case 5187:
      return B + e + W(e, /(\w+).+(:[^]+)/, B + "box-$1$2" + Ne + "flex-$1$2") + e;
    case 5443:
      return B + e + Ne + "flex-item-" + W(e, /flex-|-self/, "") + e;
    case 4675:
      return B + e + Ne + "flex-line-pack" + W(e, /align-content|flex-|-self/, "") + e;
    case 5548:
      return B + e + Ne + W(e, "shrink", "negative") + e;
    case 5292:
      return B + e + Ne + W(e, "basis", "preferred-size") + e;
    case 6060:
      return B + "box-" + W(e, "-grow", "") + B + e + Ne + W(e, "grow", "positive") + e;
    case 4554:
      return B + W(e, /([^-])(transform)/g, "$1" + B + "$2") + e;
    case 6187:
      return W(W(W(e, /(zoom-|grab)/, B + "$1"), /(image-set)/, B + "$1"), e, "") + e;
    case 5495:
    case 3959:
      return W(e, /(image-set\([^]*)/, B + "$1$`$1");
    case 4968:
      return W(W(e, /(.+:)(flex-)?(.*)/, B + "box-pack:$3" + Ne + "flex-pack:$3"), /s.+-b[^;]+/, "justify") + B + e + e;
    case 4095:
    case 3583:
    case 4068:
    case 2532:
      return W(e, /(.+)-inline(.+)/, B + "$1$2") + e;
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
        switch ($e(e, t + 1)) {
          case 109:
            if ($e(e, t + 4) !== 45)
              break;
          case 102:
            return W(e, /(.+:)(.+)-([^]+)/, "$1" + B + "$2-$3$1" + Ji + ($e(e, t + 3) == 108 ? "$3" : "$2-$3")) + e;
          case 115:
            return ~Ia(e, "stretch") ? Qm(W(e, "stretch", "fill-available"), t) + e : e;
        }
      break;
    case 4949:
      if ($e(e, t + 1) !== 115)
        break;
    case 6444:
      switch ($e(e, Ot(e) - 3 - (~Ia(e, "!important") && 10))) {
        case 107:
          return W(e, ":", ":" + B) + e;
        case 101:
          return W(e, /(.+:)([^;!]+)(;|!.+)?/, "$1" + B + ($e(e, 14) === 45 ? "inline-" : "") + "box$3$1" + B + "$2$3$1" + Ne + "$2box$3") + e;
      }
      break;
    case 5936:
      switch ($e(e, t + 11)) {
        case 114:
          return B + e + Ne + W(e, /[svh]\w+-[tblr]{2}/, "tb") + e;
        case 108:
          return B + e + Ne + W(e, /[svh]\w+-[tblr]{2}/, "tb-rl") + e;
        case 45:
          return B + e + Ne + W(e, /[svh]\w+-[tblr]{2}/, "lr") + e;
      }
      return B + e + Ne + e + e;
  }
  return e;
}
var lv = function(t, n, r, o) {
  if (t.length > -1 && !t.return)
    switch (t.type) {
      case Wu:
        t.return = Qm(t.value, t.length);
        break;
      case Wm:
        return dr([Wr(t, {
          value: W(t.value, "@", "@" + B)
        })], o);
      case Bu:
        if (t.length)
          return Uy(t.props, function(i) {
            switch (Wy(i, /(::plac\w+|:read-\w+)/)) {
              case ":read-only":
              case ":read-write":
                return dr([Wr(t, {
                  props: [W(i, /:(read-\w+)/, ":" + Ji + "$1")]
                })], o);
              case "::placeholder":
                return dr([Wr(t, {
                  props: [W(i, /:(plac\w+)/, ":" + B + "input-$1")]
                }), Wr(t, {
                  props: [W(i, /:(plac\w+)/, ":" + Ji + "$1")]
                }), Wr(t, {
                  props: [W(i, /:(plac\w+)/, Ne + "input-$1")]
                })], o);
            }
            return "";
          });
    }
}, sv = [lv], Ym = function(t) {
  var n = t.key;
  if (n === "css") {
    var r = document.querySelectorAll("style[data-emotion]:not([data-s])");
    Array.prototype.forEach.call(r, function(g) {
      var $ = g.getAttribute("data-emotion");
      $.indexOf(" ") !== -1 && (document.head.appendChild(g), g.setAttribute("data-s", ""));
    });
  }
  var o = t.stylisPlugins || sv, i = {}, l, s = [];
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
  var a, u = [ov, iv];
  {
    var c, d = [qy, ev(function(g) {
      c.insert(g);
    })], m = Jy(u.concat(o, d)), v = function($) {
      return dr(Xy($), m);
    };
    a = function($, p, f, h) {
      c = f, v($ ? $ + "{" + p.styles + "}" : p.styles), h && (y.inserted[p.name] = !0);
    };
  }
  var y = {
    key: n,
    sheet: new Ly({
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
}, Xm = { exports: {} }, H = {};
/** @license React v16.13.1
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ce = typeof Symbol == "function" && Symbol.for, Vu = Ce ? Symbol.for("react.element") : 60103, Hu = Ce ? Symbol.for("react.portal") : 60106, El = Ce ? Symbol.for("react.fragment") : 60107, _l = Ce ? Symbol.for("react.strict_mode") : 60108, Pl = Ce ? Symbol.for("react.profiler") : 60114, $l = Ce ? Symbol.for("react.provider") : 60109, Tl = Ce ? Symbol.for("react.context") : 60110, Ku = Ce ? Symbol.for("react.async_mode") : 60111, Rl = Ce ? Symbol.for("react.concurrent_mode") : 60111, Ol = Ce ? Symbol.for("react.forward_ref") : 60112, Ml = Ce ? Symbol.for("react.suspense") : 60113, av = Ce ? Symbol.for("react.suspense_list") : 60120, Nl = Ce ? Symbol.for("react.memo") : 60115, zl = Ce ? Symbol.for("react.lazy") : 60116, uv = Ce ? Symbol.for("react.block") : 60121, cv = Ce ? Symbol.for("react.fundamental") : 60117, fv = Ce ? Symbol.for("react.responder") : 60118, dv = Ce ? Symbol.for("react.scope") : 60119;
function et(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Vu:
        switch (e = e.type, e) {
          case Ku:
          case Rl:
          case El:
          case Pl:
          case _l:
          case Ml:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Tl:
              case Ol:
              case zl:
              case Nl:
              case $l:
                return e;
              default:
                return t;
            }
        }
      case Hu:
        return t;
    }
  }
}
function Zm(e) {
  return et(e) === Rl;
}
H.AsyncMode = Ku;
H.ConcurrentMode = Rl;
H.ContextConsumer = Tl;
H.ContextProvider = $l;
H.Element = Vu;
H.ForwardRef = Ol;
H.Fragment = El;
H.Lazy = zl;
H.Memo = Nl;
H.Portal = Hu;
H.Profiler = Pl;
H.StrictMode = _l;
H.Suspense = Ml;
H.isAsyncMode = function(e) {
  return Zm(e) || et(e) === Ku;
};
H.isConcurrentMode = Zm;
H.isContextConsumer = function(e) {
  return et(e) === Tl;
};
H.isContextProvider = function(e) {
  return et(e) === $l;
};
H.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Vu;
};
H.isForwardRef = function(e) {
  return et(e) === Ol;
};
H.isFragment = function(e) {
  return et(e) === El;
};
H.isLazy = function(e) {
  return et(e) === zl;
};
H.isMemo = function(e) {
  return et(e) === Nl;
};
H.isPortal = function(e) {
  return et(e) === Hu;
};
H.isProfiler = function(e) {
  return et(e) === Pl;
};
H.isStrictMode = function(e) {
  return et(e) === _l;
};
H.isSuspense = function(e) {
  return et(e) === Ml;
};
H.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === El || e === Rl || e === Pl || e === _l || e === Ml || e === av || typeof e == "object" && e !== null && (e.$$typeof === zl || e.$$typeof === Nl || e.$$typeof === $l || e.$$typeof === Tl || e.$$typeof === Ol || e.$$typeof === cv || e.$$typeof === fv || e.$$typeof === dv || e.$$typeof === uv);
};
H.typeOf = et;
Xm.exports = H;
var pv = Xm.exports, qm = pv, mv = {
  $$typeof: !0,
  render: !0,
  defaultProps: !0,
  displayName: !0,
  propTypes: !0
}, hv = {
  $$typeof: !0,
  compare: !0,
  defaultProps: !0,
  displayName: !0,
  propTypes: !0,
  type: !0
}, Jm = {};
Jm[qm.ForwardRef] = mv;
Jm[qm.Memo] = hv;
var gv = !0;
function eh(e, t, n) {
  var r = "";
  return n.split(" ").forEach(function(o) {
    e[o] !== void 0 ? t.push(e[o] + ";") : o && (r += o + " ");
  }), r;
}
var Gu = function(t, n, r) {
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
  gv === !1) && t.registered[o] === void 0 && (t.registered[o] = n.styles);
}, Qu = function(t, n, r) {
  Gu(t, n, r);
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
var vv = {
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
}, xv = !1, Sv = /[A-Z]|^ms/g, wv = /_EMO_([^_]+?)_([^]*?)_EMO_/g, th = function(t) {
  return t.charCodeAt(1) === 45;
}, zf = function(t) {
  return t != null && typeof t != "boolean";
}, zs = /* @__PURE__ */ Gm(function(e) {
  return th(e) ? e : e.replace(Sv, "-$&").toLowerCase();
}), jf = function(t, n) {
  switch (t) {
    case "animation":
    case "animationName":
      if (typeof n == "string")
        return n.replace(wv, function(r, o, i) {
          return Mt = {
            name: o,
            styles: i,
            next: Mt
          }, o;
        });
  }
  return vv[t] !== 1 && !th(t) && typeof n == "number" && n !== 0 ? n + "px" : n;
}, kv = "Component selectors can only be used in conjunction with @emotion/babel-plugin, the swc Emotion plugin, or another Emotion-aware compiler transform.";
function To(e, t, n) {
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
      return Cv(e, t, n);
    }
    case "function": {
      if (e !== void 0) {
        var a = Mt, u = n(e);
        return Mt = a, To(e, t, u);
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
function Cv(e, t, n) {
  var r = "";
  if (Array.isArray(n))
    for (var o = 0; o < n.length; o++)
      r += To(e, t, n[o]) + ";";
  else
    for (var i in n) {
      var l = n[i];
      if (typeof l != "object") {
        var s = l;
        t != null && t[s] !== void 0 ? r += i + "{" + t[s] + "}" : zf(s) && (r += zs(i) + ":" + jf(i, s) + ";");
      } else {
        if (i === "NO_COMPONENT_SELECTOR" && xv)
          throw new Error(kv);
        if (Array.isArray(l) && typeof l[0] == "string" && (t == null || t[l[0]] === void 0))
          for (var a = 0; a < l.length; a++)
            zf(l[a]) && (r += zs(i) + ":" + jf(i, l[a]) + ";");
        else {
          var u = To(e, t, l);
          switch (i) {
            case "animation":
            case "animationName": {
              r += zs(i) + ":" + u + ";";
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
var If = /label:\s*([^\s;{]+)\s*(;|$)/g, Mt;
function Do(e, t, n) {
  if (e.length === 1 && typeof e[0] == "object" && e[0] !== null && e[0].styles !== void 0)
    return e[0];
  var r = !0, o = "";
  Mt = void 0;
  var i = e[0];
  if (i == null || i.raw === void 0)
    r = !1, o += To(n, t, i);
  else {
    var l = i;
    o += l[0];
  }
  for (var s = 1; s < e.length; s++)
    if (o += To(n, t, e[s]), r) {
      var a = i;
      o += a[s];
    }
  If.lastIndex = 0;
  for (var u = "", c; (c = If.exec(o)) !== null; )
    u += "-" + c[1];
  var d = yv(o) + u;
  return {
    name: d,
    styles: o,
    next: Mt
  };
}
var Ev = function(t) {
  return t();
}, nh = Bs["useInsertionEffect"] ? Bs["useInsertionEffect"] : !1, rh = nh || Ev, Lf = nh || k.useLayoutEffect, _v = !1, oh = /* @__PURE__ */ k.createContext(
  // we're doing this to avoid preconstruct's dead code elimination in this one case
  // because this module is primarily intended for the browser and node
  // but it's also required in react native and similar environments sometimes
  // and we could have a special build just for that
  // but this is much easier and the native packages
  // might use a different theme context in the future anyway
  typeof HTMLElement < "u" ? /* @__PURE__ */ Ym({
    key: "css"
  }) : null
), Pv = oh.Provider, Yu = function(t) {
  return /* @__PURE__ */ k.forwardRef(function(n, r) {
    var o = k.useContext(oh);
    return t(n, o, r);
  });
}, Tr = /* @__PURE__ */ k.createContext({}), Xu = {}.hasOwnProperty, Aa = "__EMOTION_TYPE_PLEASE_DO_NOT_USE__", $v = function(t, n) {
  var r = {};
  for (var o in n)
    Xu.call(n, o) && (r[o] = n[o]);
  return r[Aa] = t, r;
}, Tv = function(t) {
  var n = t.cache, r = t.serialized, o = t.isStringTag;
  return Gu(n, r, o), rh(function() {
    return Qu(n, r, o);
  }), null;
}, Rv = /* @__PURE__ */ Yu(function(e, t, n) {
  var r = e.css;
  typeof r == "string" && t.registered[r] !== void 0 && (r = t.registered[r]);
  var o = e[Aa], i = [r], l = "";
  typeof e.className == "string" ? l = eh(t.registered, i, e.className) : e.className != null && (l = e.className + " ");
  var s = Do(i, void 0, k.useContext(Tr));
  l += t.key + "-" + s.name;
  var a = {};
  for (var u in e)
    Xu.call(e, u) && u !== "css" && u !== Aa && !_v && (a[u] = e[u]);
  return a.className = l, n && (a.ref = n), /* @__PURE__ */ k.createElement(k.Fragment, null, /* @__PURE__ */ k.createElement(Tv, {
    cache: t,
    serialized: s,
    isStringTag: typeof o == "string"
  }), /* @__PURE__ */ k.createElement(o, a));
}), Ov = Rv, js = { exports: {} }, Af;
function ih() {
  return Af || (Af = 1, function(e) {
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
ih();
var Df = function(t, n) {
  var r = arguments;
  if (n == null || !Xu.call(n, "css"))
    return k.createElement.apply(void 0, r);
  var o = r.length, i = new Array(o);
  i[0] = Ov, i[1] = $v(t, n);
  for (var l = 2; l < o; l++)
    i[l] = r[l];
  return k.createElement.apply(null, i);
};
(function(e) {
  var t;
  t || (t = e.JSX || (e.JSX = {}));
})(Df || (Df = {}));
var Mv = /* @__PURE__ */ Yu(function(e, t) {
  var n = e.styles, r = Do([n], void 0, k.useContext(Tr)), o = k.useRef();
  return Lf(function() {
    var i = t.key + "-global", l = new t.sheet.constructor({
      key: i,
      nonce: t.sheet.nonce,
      container: t.sheet.container,
      speedy: t.sheet.isSpeedy
    }), s = !1, a = document.querySelector('style[data-emotion="' + i + " " + r.name + '"]');
    return t.sheet.tags.length && (l.before = t.sheet.tags[0]), a !== null && (s = !0, a.setAttribute("data-emotion", i), l.hydrate([a])), o.current = [l, s], function() {
      l.flush();
    };
  }, [t]), Lf(function() {
    var i = o.current, l = i[0], s = i[1];
    if (s) {
      i[1] = !1;
      return;
    }
    if (r.next !== void 0 && Qu(t, r.next, !0), l.tags.length) {
      var a = l.tags[l.tags.length - 1].nextElementSibling;
      l.before = a, l.flush();
    }
    t.insert("", r, l, !1);
  }, [t, r.name]), null;
});
function jl() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  return Do(t);
}
function Rr() {
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
var Nv = /^((children|dangerouslySetInnerHTML|key|ref|autoFocus|defaultValue|defaultChecked|innerHTML|suppressContentEditableWarning|suppressHydrationWarning|valueLink|abbr|accept|acceptCharset|accessKey|action|allow|allowUserMedia|allowPaymentRequest|allowFullScreen|allowTransparency|alt|async|autoComplete|autoPlay|capture|cellPadding|cellSpacing|challenge|charSet|checked|cite|classID|className|cols|colSpan|content|contentEditable|contextMenu|controls|controlsList|coords|crossOrigin|data|dateTime|decoding|default|defer|dir|disabled|disablePictureInPicture|disableRemotePlayback|download|draggable|encType|enterKeyHint|fetchpriority|fetchPriority|form|formAction|formEncType|formMethod|formNoValidate|formTarget|frameBorder|headers|height|hidden|high|href|hrefLang|htmlFor|httpEquiv|id|inputMode|integrity|is|keyParams|keyType|kind|label|lang|list|loading|loop|low|marginHeight|marginWidth|max|maxLength|media|mediaGroup|method|min|minLength|multiple|muted|name|nonce|noValidate|open|optimum|pattern|placeholder|playsInline|popover|popoverTarget|popoverTargetAction|poster|preload|profile|radioGroup|readOnly|referrerPolicy|rel|required|reversed|role|rows|rowSpan|sandbox|scope|scoped|scrolling|seamless|selected|shape|size|sizes|slot|span|spellCheck|src|srcDoc|srcLang|srcSet|start|step|style|summary|tabIndex|target|title|translate|type|useMap|value|width|wmode|wrap|about|datatype|inlist|prefix|property|resource|typeof|vocab|autoCapitalize|autoCorrect|autoSave|color|incremental|fallback|inert|itemProp|itemScope|itemType|itemID|itemRef|on|option|results|security|unselectable|accentHeight|accumulate|additive|alignmentBaseline|allowReorder|alphabetic|amplitude|arabicForm|ascent|attributeName|attributeType|autoReverse|azimuth|baseFrequency|baselineShift|baseProfile|bbox|begin|bias|by|calcMode|capHeight|clip|clipPathUnits|clipPath|clipRule|colorInterpolation|colorInterpolationFilters|colorProfile|colorRendering|contentScriptType|contentStyleType|cursor|cx|cy|d|decelerate|descent|diffuseConstant|direction|display|divisor|dominantBaseline|dur|dx|dy|edgeMode|elevation|enableBackground|end|exponent|externalResourcesRequired|fill|fillOpacity|fillRule|filter|filterRes|filterUnits|floodColor|floodOpacity|focusable|fontFamily|fontSize|fontSizeAdjust|fontStretch|fontStyle|fontVariant|fontWeight|format|from|fr|fx|fy|g1|g2|glyphName|glyphOrientationHorizontal|glyphOrientationVertical|glyphRef|gradientTransform|gradientUnits|hanging|horizAdvX|horizOriginX|ideographic|imageRendering|in|in2|intercept|k|k1|k2|k3|k4|kernelMatrix|kernelUnitLength|kerning|keyPoints|keySplines|keyTimes|lengthAdjust|letterSpacing|lightingColor|limitingConeAngle|local|markerEnd|markerMid|markerStart|markerHeight|markerUnits|markerWidth|mask|maskContentUnits|maskUnits|mathematical|mode|numOctaves|offset|opacity|operator|order|orient|orientation|origin|overflow|overlinePosition|overlineThickness|panose1|paintOrder|pathLength|patternContentUnits|patternTransform|patternUnits|pointerEvents|points|pointsAtX|pointsAtY|pointsAtZ|preserveAlpha|preserveAspectRatio|primitiveUnits|r|radius|refX|refY|renderingIntent|repeatCount|repeatDur|requiredExtensions|requiredFeatures|restart|result|rotate|rx|ry|scale|seed|shapeRendering|slope|spacing|specularConstant|specularExponent|speed|spreadMethod|startOffset|stdDeviation|stemh|stemv|stitchTiles|stopColor|stopOpacity|strikethroughPosition|strikethroughThickness|string|stroke|strokeDasharray|strokeDashoffset|strokeLinecap|strokeLinejoin|strokeMiterlimit|strokeOpacity|strokeWidth|surfaceScale|systemLanguage|tableValues|targetX|targetY|textAnchor|textDecoration|textRendering|textLength|to|transform|u1|u2|underlinePosition|underlineThickness|unicode|unicodeBidi|unicodeRange|unitsPerEm|vAlphabetic|vHanging|vIdeographic|vMathematical|values|vectorEffect|version|vertAdvY|vertOriginX|vertOriginY|viewBox|viewTarget|visibility|widths|wordSpacing|writingMode|x|xHeight|x1|x2|xChannelSelector|xlinkActuate|xlinkArcrole|xlinkHref|xlinkRole|xlinkShow|xlinkTitle|xlinkType|xmlBase|xmlns|xmlnsXlink|xmlLang|xmlSpace|y|y1|y2|yChannelSelector|z|zoomAndPan|for|class|autofocus)|(([Dd][Aa][Tt][Aa]|[Aa][Rr][Ii][Aa]|x)-.*))$/, zv = /* @__PURE__ */ Gm(
  function(e) {
    return Nv.test(e) || e.charCodeAt(0) === 111 && e.charCodeAt(1) === 110 && e.charCodeAt(2) < 91;
  }
  /* Z+1 */
), jv = !1, Iv = zv, Lv = function(t) {
  return t !== "theme";
}, Ff = function(t) {
  return typeof t == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  t.charCodeAt(0) > 96 ? Iv : Lv;
}, bf = function(t, n, r) {
  var o;
  if (n) {
    var i = n.shouldForwardProp;
    o = t.__emotion_forwardProp && i ? function(l) {
      return t.__emotion_forwardProp(l) && i(l);
    } : i;
  }
  return typeof o != "function" && r && (o = t.__emotion_forwardProp), o;
}, Av = function(t) {
  var n = t.cache, r = t.serialized, o = t.isStringTag;
  return Gu(n, r, o), rh(function() {
    return Qu(n, r, o);
  }), null;
}, Dv = function e(t, n) {
  var r = t.__emotion_real === t, o = r && t.__emotion_base || t, i, l;
  n !== void 0 && (i = n.label, l = n.target);
  var s = bf(t, n, r), a = s || Ff(o), u = !a("as");
  return function() {
    var c = arguments, d = r && t.__emotion_styles !== void 0 ? t.__emotion_styles.slice(0) : [];
    if (i !== void 0 && d.push("label:" + i + ";"), c[0] == null || c[0].raw === void 0)
      d.push.apply(d, c);
    else {
      var m = c[0];
      d.push(m[0]);
      for (var v = c.length, y = 1; y < v; y++)
        d.push(c[y], m[y]);
    }
    var g = Yu(function($, p, f) {
      var h = u && $.as || o, x = "", E = [], w = $;
      if ($.theme == null) {
        w = {};
        for (var S in $)
          w[S] = $[S];
        w.theme = k.useContext(Tr);
      }
      typeof $.className == "string" ? x = eh(p.registered, E, $.className) : $.className != null && (x = $.className + " ");
      var T = Do(d.concat(E), p.registered, w);
      x += p.key + "-" + T.name, l !== void 0 && (x += " " + l);
      var I = u && s === void 0 ? Ff(h) : a, O = {};
      for (var F in $)
        u && F === "as" || I(F) && (O[F] = $[F]);
      return O.className = x, f && (O.ref = f), /* @__PURE__ */ k.createElement(k.Fragment, null, /* @__PURE__ */ k.createElement(Av, {
        cache: p,
        serialized: T,
        isStringTag: typeof h == "string"
      }), /* @__PURE__ */ k.createElement(h, O));
    });
    return g.displayName = i !== void 0 ? i : "Styled(" + (typeof o == "string" ? o : o.displayName || o.name || "Component") + ")", g.defaultProps = t.defaultProps, g.__emotion_real = g, g.__emotion_base = o, g.__emotion_styles = d, g.__emotion_forwardProp = s, Object.defineProperty(g, "toString", {
      value: function() {
        return l === void 0 && jv ? "NO_COMPONENT_SELECTOR" : "." + l;
      }
    }), g.withComponent = function($, p) {
      var f = e($, C({}, n, p, {
        shouldForwardProp: bf(g, p, !0)
      }));
      return f.apply(void 0, d);
    }, g;
  };
}, Fv = [
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
], Da = Dv.bind(null);
Fv.forEach(function(e) {
  Da[e] = Da(e);
});
function bv(e, t) {
  const n = Ym({
    key: "css",
    prepend: e
  });
  if (t) {
    const r = n.insert;
    n.insert = (...o) => (o[1].styles.match(/^@layer\s+[^{]*$/) || (o[1].styles = `@layer mui {${o[1].styles}}`), r(...o));
  }
  return n;
}
const Is = /* @__PURE__ */ new Map();
function Bv(e) {
  const {
    injectFirst: t,
    enableCssLayer: n,
    children: r
  } = e, o = k.useMemo(() => {
    const i = `${t}-${n}`;
    if (typeof document == "object" && Is.has(i))
      return Is.get(i);
    const l = bv(t, n);
    return Is.set(i, l), l;
  }, [t, n]);
  return t || n ? /* @__PURE__ */ _.jsx(Pv, {
    value: o,
    children: r
  }) : r;
}
function Wv(e) {
  return e == null || Object.keys(e).length === 0;
}
function lh(e) {
  const {
    styles: t,
    defaultTheme: n = {}
  } = e, r = typeof t == "function" ? (o) => t(Wv(o) ? n : o) : t;
  return /* @__PURE__ */ _.jsx(Mv, {
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
function sh(e, t) {
  return Da(e, t);
}
const Uv = (e, t) => {
  Array.isArray(e.__emotion_styles) && (e.__emotion_styles = t(e.__emotion_styles));
}, Bf = [];
function ah(e) {
  return Bf[0] = e, Do(Bf);
}
const Vv = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  GlobalStyles: lh,
  StyledEngineProvider: Bv,
  ThemeContext: Tr,
  css: jl,
  default: sh,
  internal_processStyles: Uv,
  internal_serializeStyles: ah,
  keyframes: Rr
}, Symbol.toStringTag, { value: "Module" }));
function rn(e) {
  if (typeof e != "object" || e === null)
    return !1;
  const t = Object.getPrototypeOf(e);
  return (t === null || t === Object.prototype || Object.getPrototypeOf(t) === null) && !(Symbol.toStringTag in e) && !(Symbol.iterator in e);
}
function uh(e) {
  if (/* @__PURE__ */ k.isValidElement(e) || !rn(e))
    return e;
  const t = {};
  return Object.keys(e).forEach((n) => {
    t[n] = uh(e[n]);
  }), t;
}
function Lt(e, t, n = {
  clone: !0
}) {
  const r = n.clone ? C({}, e) : e;
  return rn(e) && rn(t) && Object.keys(t).forEach((o) => {
    /* @__PURE__ */ k.isValidElement(t[o]) ? r[o] = t[o] : rn(t[o]) && // Avoid prototype pollution
    Object.prototype.hasOwnProperty.call(e, o) && rn(e[o]) ? r[o] = Lt(e[o], t[o], n) : n.clone ? r[o] = rn(t[o]) ? uh(t[o]) : t[o] : r[o] = t[o];
  }), r;
}
const Hv = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Lt,
  isPlainObject: rn
}, Symbol.toStringTag, { value: "Module" })), Kv = ["values", "unit", "step"], Gv = (e) => {
  const t = Object.keys(e).map((n) => ({
    key: n,
    val: e[n]
  })) || [];
  return t.sort((n, r) => n.val - r.val), t.reduce((n, r) => C({}, n, {
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
  } = e, o = K(e, Kv), i = Gv(t), l = Object.keys(i);
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
  function d(m) {
    const v = l.indexOf(m);
    return v === 0 ? s(l[1]) : v === l.length - 1 ? a(l[v]) : u(m, l[l.indexOf(m) + 1]).replace("@media", "@media not all and");
  }
  return C({
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
const Qv = {
  borderRadius: 4
}, Yv = Qv;
function lo(e, t) {
  return t ? Lt(e, t, {
    clone: !1
    // No need to clone deep, it's way faster.
  }) : e;
}
const Zu = {
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
}, Wf = {
  // Sorted ASC by size. That's important.
  // It can't be configured as it's used statically for propTypes.
  keys: ["xs", "sm", "md", "lg", "xl"],
  up: (e) => `@media (min-width:${Zu[e]}px)`
};
function dt(e, t, n) {
  const r = e.theme || {};
  if (Array.isArray(t)) {
    const i = r.breakpoints || Wf;
    return t.reduce((l, s, a) => (l[i.up(i.keys[a])] = n(t[a]), l), {});
  }
  if (typeof t == "object") {
    const i = r.breakpoints || Wf;
    return Object.keys(t).reduce((l, s) => {
      if (Object.keys(i.values || Zu).indexOf(s) !== -1) {
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
function Xv(e = {}) {
  var t;
  return ((t = e.keys) == null ? void 0 : t.reduce((r, o) => {
    const i = e.up(o);
    return r[i] = {}, r;
  }, {})) || {};
}
function Uf(e, t) {
  return e.reduce((n, r) => {
    const o = n[r];
    return (!o || Object.keys(o).length === 0) && delete n[r], n;
  }, t);
}
function Zv(e, t) {
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
  const r = n || Zv(e, t), o = Object.keys(r);
  if (o.length === 0)
    return e;
  let i;
  return o.reduce((l, s, a) => (Array.isArray(e) ? (l[s] = e[a] != null ? e[a] : e[i], i = a) : typeof e == "object" ? (l[s] = e[s] != null ? e[s] : e[i], i = s) : l[s] = e, l), {});
}
function oe(e) {
  if (typeof e != "string")
    throw new Error(_o(7));
  return e.charAt(0).toUpperCase() + e.slice(1);
}
const qv = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: oe
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
function el(e, t, n, r = n) {
  let o;
  return typeof e == "function" ? o = e(n) : Array.isArray(e) ? o = e[n] || r : o = Ll(e, n) || r, t && (o = t(o, r, e)), o;
}
function fe(e) {
  const {
    prop: t,
    cssProperty: n = e.prop,
    themeKey: r,
    transform: o
  } = e, i = (l) => {
    if (l[t] == null)
      return null;
    const s = l[t], a = l.theme, u = Ll(a, r) || {};
    return dt(l, s, (d) => {
      let m = el(u, o, d);
      return d === m && typeof d == "string" && (m = el(u, o, `${t}${d === "default" ? "" : oe(d)}`, d)), n === !1 ? m : {
        [n]: m
      };
    });
  };
  return i.propTypes = {}, i.filterProps = [t], i;
}
function Jv(e) {
  const t = {};
  return (n) => (t[n] === void 0 && (t[n] = e(n)), t[n]);
}
const e1 = {
  m: "margin",
  p: "padding"
}, t1 = {
  t: "Top",
  r: "Right",
  b: "Bottom",
  l: "Left",
  x: ["Left", "Right"],
  y: ["Top", "Bottom"]
}, Vf = {
  marginX: "mx",
  marginY: "my",
  paddingX: "px",
  paddingY: "py"
}, n1 = Jv((e) => {
  if (e.length > 2)
    if (Vf[e])
      e = Vf[e];
    else
      return [e];
  const [t, n] = e.split(""), r = e1[t], o = t1[n] || "";
  return Array.isArray(o) ? o.map((i) => r + i) : [r + o];
}), qu = ["m", "mt", "mr", "mb", "ml", "mx", "my", "margin", "marginTop", "marginRight", "marginBottom", "marginLeft", "marginX", "marginY", "marginInline", "marginInlineStart", "marginInlineEnd", "marginBlock", "marginBlockStart", "marginBlockEnd"], Ju = ["p", "pt", "pr", "pb", "pl", "px", "py", "padding", "paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "paddingX", "paddingY", "paddingInline", "paddingInlineStart", "paddingInlineEnd", "paddingBlock", "paddingBlockStart", "paddingBlockEnd"];
[...qu, ...Ju];
function Fo(e, t, n, r) {
  var o;
  const i = (o = Ll(e, t, !1)) != null ? o : n;
  return typeof i == "number" ? (l) => typeof l == "string" ? l : i * l : Array.isArray(i) ? (l) => typeof l == "string" ? l : i[l] : typeof i == "function" ? i : () => {
  };
}
function fh(e) {
  return Fo(e, "spacing", 8);
}
function bo(e, t) {
  if (typeof t == "string" || t == null)
    return t;
  const n = Math.abs(t), r = e(n);
  return t >= 0 ? r : typeof r == "number" ? -r : `-${r}`;
}
function r1(e, t) {
  return (n) => e.reduce((r, o) => (r[o] = bo(t, n), r), {});
}
function o1(e, t, n, r) {
  if (t.indexOf(n) === -1)
    return null;
  const o = n1(n), i = r1(o, r), l = e[n];
  return dt(e, l, i);
}
function dh(e, t) {
  const n = fh(e.theme);
  return Object.keys(e).map((r) => o1(e, t, r, n)).reduce(lo, {});
}
function se(e) {
  return dh(e, qu);
}
se.propTypes = {};
se.filterProps = qu;
function ae(e) {
  return dh(e, Ju);
}
ae.propTypes = {};
ae.filterProps = Ju;
function i1(e = 8) {
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
function Al(...e) {
  const t = e.reduce((r, o) => (o.filterProps.forEach((i) => {
    r[i] = o;
  }), r), {}), n = (r) => Object.keys(r).reduce((o, i) => t[i] ? lo(o, t[i](r)) : o, {});
  return n.propTypes = {}, n.filterProps = e.reduce((r, o) => r.concat(o.filterProps), []), n;
}
function st(e) {
  return typeof e != "number" ? e : `${e}px solid`;
}
function mt(e, t) {
  return fe({
    prop: e,
    themeKey: "borders",
    transform: t
  });
}
const l1 = mt("border", st), s1 = mt("borderTop", st), a1 = mt("borderRight", st), u1 = mt("borderBottom", st), c1 = mt("borderLeft", st), f1 = mt("borderColor"), d1 = mt("borderTopColor"), p1 = mt("borderRightColor"), m1 = mt("borderBottomColor"), h1 = mt("borderLeftColor"), g1 = mt("outline", st), y1 = mt("outlineColor"), Dl = (e) => {
  if (e.borderRadius !== void 0 && e.borderRadius !== null) {
    const t = Fo(e.theme, "shape.borderRadius", 4), n = (r) => ({
      borderRadius: bo(t, r)
    });
    return dt(e, e.borderRadius, n);
  }
  return null;
};
Dl.propTypes = {};
Dl.filterProps = ["borderRadius"];
Al(l1, s1, a1, u1, c1, f1, d1, p1, m1, h1, Dl, g1, y1);
const Fl = (e) => {
  if (e.gap !== void 0 && e.gap !== null) {
    const t = Fo(e.theme, "spacing", 8), n = (r) => ({
      gap: bo(t, r)
    });
    return dt(e, e.gap, n);
  }
  return null;
};
Fl.propTypes = {};
Fl.filterProps = ["gap"];
const bl = (e) => {
  if (e.columnGap !== void 0 && e.columnGap !== null) {
    const t = Fo(e.theme, "spacing", 8), n = (r) => ({
      columnGap: bo(t, r)
    });
    return dt(e, e.columnGap, n);
  }
  return null;
};
bl.propTypes = {};
bl.filterProps = ["columnGap"];
const Bl = (e) => {
  if (e.rowGap !== void 0 && e.rowGap !== null) {
    const t = Fo(e.theme, "spacing", 8), n = (r) => ({
      rowGap: bo(t, r)
    });
    return dt(e, e.rowGap, n);
  }
  return null;
};
Bl.propTypes = {};
Bl.filterProps = ["rowGap"];
const v1 = fe({
  prop: "gridColumn"
}), x1 = fe({
  prop: "gridRow"
}), S1 = fe({
  prop: "gridAutoFlow"
}), w1 = fe({
  prop: "gridAutoColumns"
}), k1 = fe({
  prop: "gridAutoRows"
}), C1 = fe({
  prop: "gridTemplateColumns"
}), E1 = fe({
  prop: "gridTemplateRows"
}), _1 = fe({
  prop: "gridTemplateAreas"
}), P1 = fe({
  prop: "gridArea"
});
Al(Fl, bl, Bl, v1, x1, S1, w1, k1, C1, E1, _1, P1);
function pr(e, t) {
  return t === "grey" ? t : e;
}
const $1 = fe({
  prop: "color",
  themeKey: "palette",
  transform: pr
}), T1 = fe({
  prop: "bgcolor",
  cssProperty: "backgroundColor",
  themeKey: "palette",
  transform: pr
}), R1 = fe({
  prop: "backgroundColor",
  themeKey: "palette",
  transform: pr
});
Al($1, T1, R1);
function Ge(e) {
  return e <= 1 && e !== 0 ? `${e * 100}%` : e;
}
const O1 = fe({
  prop: "width",
  transform: Ge
}), ec = (e) => {
  if (e.maxWidth !== void 0 && e.maxWidth !== null) {
    const t = (n) => {
      var r, o;
      const i = ((r = e.theme) == null || (r = r.breakpoints) == null || (r = r.values) == null ? void 0 : r[n]) || Zu[n];
      return i ? ((o = e.theme) == null || (o = o.breakpoints) == null ? void 0 : o.unit) !== "px" ? {
        maxWidth: `${i}${e.theme.breakpoints.unit}`
      } : {
        maxWidth: i
      } : {
        maxWidth: Ge(n)
      };
    };
    return dt(e, e.maxWidth, t);
  }
  return null;
};
ec.filterProps = ["maxWidth"];
const M1 = fe({
  prop: "minWidth",
  transform: Ge
}), N1 = fe({
  prop: "height",
  transform: Ge
}), z1 = fe({
  prop: "maxHeight",
  transform: Ge
}), j1 = fe({
  prop: "minHeight",
  transform: Ge
});
fe({
  prop: "size",
  cssProperty: "width",
  transform: Ge
});
fe({
  prop: "size",
  cssProperty: "height",
  transform: Ge
});
const I1 = fe({
  prop: "boxSizing"
});
Al(O1, ec, M1, N1, z1, j1, I1);
const L1 = {
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
    style: Dl
  },
  // palette
  color: {
    themeKey: "palette",
    transform: pr
  },
  bgcolor: {
    themeKey: "palette",
    cssProperty: "backgroundColor",
    transform: pr
  },
  backgroundColor: {
    themeKey: "palette",
    transform: pr
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
    style: Fl
  },
  rowGap: {
    style: Bl
  },
  columnGap: {
    style: bl
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
}, Bo = L1;
function A1(...e) {
  const t = e.reduce((r, o) => r.concat(Object.keys(o)), []), n = new Set(t);
  return e.every((r) => n.size === Object.keys(r).length);
}
function D1(e, t) {
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
      transform: c,
      style: d
    } = s;
    if (r == null)
      return null;
    if (u === "typography" && r === "inherit")
      return {
        [n]: r
      };
    const m = Ll(o, u) || {};
    return d ? d(l) : dt(l, r, (y) => {
      let g = el(m, c, y);
      return y === g && typeof y == "string" && (g = el(m, c, `${n}${y === "default" ? "" : oe(y)}`, y)), a === !1 ? g : {
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
      const d = Xv(i.breakpoints), m = Object.keys(d);
      let v = d;
      return Object.keys(c).forEach((y) => {
        const g = D1(c[y], i);
        if (g != null)
          if (typeof g == "object")
            if (s[y])
              v = lo(v, e(y, g, i, s));
            else {
              const $ = dt({
                theme: i
              }, g, (p) => ({
                [y]: p
              }));
              A1($, g) ? v[y] = t({
                sx: g,
                theme: i,
                nested: !0
              }) : v = lo(v, $);
            }
          else
            v = lo(v, e(y, g, i, s));
      }), !l && i.modularCssLayers ? {
        "@layer sx": Uf(m, v)
      } : Uf(m, v);
    }
    return Array.isArray(o) ? o.map(a) : a(o);
  }
  return t;
}
const mh = ph();
mh.filterProps = ["sx"];
const Wl = mh;
function hh(e, t) {
  const n = this;
  return n.vars && typeof n.getColorSchemeSelector == "function" ? {
    [n.getColorSchemeSelector(e).replace(/(\[[^\]]+\])/, "*:where($1)")]: t
  } : n.palette.mode === e ? t : {};
}
const F1 = ["breakpoints", "palette", "spacing", "shape"];
function tc(e = {}, ...t) {
  const {
    breakpoints: n = {},
    palette: r = {},
    spacing: o,
    shape: i = {}
  } = e, l = K(e, F1), s = ch(n), a = i1(o);
  let u = Lt({
    breakpoints: s,
    direction: "ltr",
    components: {},
    // Inject component definitions.
    palette: C({
      mode: "light"
    }, r),
    spacing: a,
    shape: C({}, Yv, i)
  }, l);
  return u.applyStyles = hh, u = t.reduce((c, d) => Lt(c, d), u), u.unstable_sxConfig = C({}, Bo, l == null ? void 0 : l.unstable_sxConfig), u.unstable_sx = function(d) {
    return Wl({
      sx: d,
      theme: this
    });
  }, u;
}
const b1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: tc,
  private_createBreakpoints: ch,
  unstable_applyStyles: hh
}, Symbol.toStringTag, { value: "Module" }));
function B1(e) {
  return Object.keys(e).length === 0;
}
function nc(e = null) {
  const t = k.useContext(Tr);
  return !t || B1(t) ? e : t;
}
const W1 = tc();
function rc(e = W1) {
  return nc(e);
}
function Ls(e) {
  const t = ah(e);
  return e !== t && t.styles ? (t.styles.match(/^@layer\s+[^{]*$/) || (t.styles = `@layer global{${t.styles}}`), t) : e;
}
function gh({
  styles: e,
  themeId: t,
  defaultTheme: n = {}
}) {
  const r = rc(n), o = t && r[t] || r;
  let i = typeof e == "function" ? e(o) : e;
  return o.modularCssLayers && (Array.isArray(i) ? i = i.map((l) => Ls(typeof l == "function" ? l(o) : l)) : i = Ls(i)), /* @__PURE__ */ _.jsx(lh, {
    styles: i
  });
}
const U1 = ["sx"], V1 = (e) => {
  var t, n;
  const r = {
    systemProps: {},
    otherProps: {}
  }, o = (t = e == null || (n = e.theme) == null ? void 0 : n.unstable_sxConfig) != null ? t : Bo;
  return Object.keys(e).forEach((i) => {
    o[i] ? r.systemProps[i] = e[i] : r.otherProps[i] = e[i];
  }), r;
};
function Ul(e) {
  const {
    sx: t
  } = e, n = K(e, U1), {
    systemProps: r,
    otherProps: o
  } = V1(n);
  let i;
  return Array.isArray(t) ? i = [r, ...t] : typeof t == "function" ? i = (...l) => {
    const s = t(...l);
    return rn(s) ? C({}, r, s) : r;
  } : i = C({}, r, t), C({}, o, {
    sx: i
  });
}
const H1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Wl,
  extendSxProp: Ul,
  unstable_createStyleFunctionSx: ph,
  unstable_defaultSxConfig: Bo
}, Symbol.toStringTag, { value: "Module" })), Hf = (e) => e, K1 = () => {
  let e = Hf;
  return {
    configure(t) {
      e = t;
    },
    generate(t) {
      return e(t);
    },
    reset() {
      e = Hf;
    }
  };
}, G1 = K1(), oc = G1;
function yh(e) {
  var t, n, r = "";
  if (typeof e == "string" || typeof e == "number")
    r += e;
  else if (typeof e == "object")
    if (Array.isArray(e)) {
      var o = e.length;
      for (t = 0; t < o; t++)
        e[t] && (n = yh(e[t])) && (r && (r += " "), r += n);
    } else
      for (n in e)
        e[n] && (r && (r += " "), r += n);
  return r;
}
function ne() {
  for (var e, t, n = 0, r = "", o = arguments.length; n < o; n++)
    (e = arguments[n]) && (t = yh(e)) && (r && (r += " "), r += t);
  return r;
}
const Q1 = ["className", "component"];
function Y1(e = {}) {
  const {
    themeId: t,
    defaultTheme: n,
    defaultClassName: r = "MuiBox-root",
    generateClassName: o
  } = e, i = sh("div", {
    shouldForwardProp: (s) => s !== "theme" && s !== "sx" && s !== "as"
  })(Wl);
  return /* @__PURE__ */ k.forwardRef(function(a, u) {
    const c = rc(n), d = Ul(a), {
      className: m,
      component: v = "div"
    } = d, y = K(d, Q1);
    return /* @__PURE__ */ _.jsx(i, C({
      as: v,
      ref: u,
      className: ne(m, o ? o(r) : r),
      theme: t && c[t] || c
    }, y));
  });
}
const X1 = {
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
function ht(e, t, n = "Mui") {
  const r = X1[t];
  return r ? `${n}-${r}` : `${oc.generate(e)}-${t}`;
}
function tt(e, t, n = "Mui") {
  const r = {};
  return t.forEach((o) => {
    r[o] = ht(e, o, n);
  }), r;
}
var vh = { exports: {} }, G = {};
/**
 * @license React
 * react-is.production.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ic = Symbol.for("react.transitional.element"), lc = Symbol.for("react.portal"), Vl = Symbol.for("react.fragment"), Hl = Symbol.for("react.strict_mode"), Kl = Symbol.for("react.profiler"), Gl = Symbol.for("react.consumer"), Ql = Symbol.for("react.context"), Yl = Symbol.for("react.forward_ref"), Xl = Symbol.for("react.suspense"), Zl = Symbol.for("react.suspense_list"), ql = Symbol.for("react.memo"), Jl = Symbol.for("react.lazy"), Z1 = Symbol.for("react.view_transition"), q1 = Symbol.for("react.client.reference");
function gt(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case ic:
        switch (e = e.type, e) {
          case Vl:
          case Kl:
          case Hl:
          case Xl:
          case Zl:
          case Z1:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Ql:
              case Yl:
              case Jl:
              case ql:
                return e;
              case Gl:
                return e;
              default:
                return t;
            }
        }
      case lc:
        return t;
    }
  }
}
G.ContextConsumer = Gl;
G.ContextProvider = Ql;
G.Element = ic;
G.ForwardRef = Yl;
G.Fragment = Vl;
G.Lazy = Jl;
G.Memo = ql;
G.Portal = lc;
G.Profiler = Kl;
G.StrictMode = Hl;
G.Suspense = Xl;
G.SuspenseList = Zl;
G.isContextConsumer = function(e) {
  return gt(e) === Gl;
};
G.isContextProvider = function(e) {
  return gt(e) === Ql;
};
G.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === ic;
};
G.isForwardRef = function(e) {
  return gt(e) === Yl;
};
G.isFragment = function(e) {
  return gt(e) === Vl;
};
G.isLazy = function(e) {
  return gt(e) === Jl;
};
G.isMemo = function(e) {
  return gt(e) === ql;
};
G.isPortal = function(e) {
  return gt(e) === lc;
};
G.isProfiler = function(e) {
  return gt(e) === Kl;
};
G.isStrictMode = function(e) {
  return gt(e) === Hl;
};
G.isSuspense = function(e) {
  return gt(e) === Xl;
};
G.isSuspenseList = function(e) {
  return gt(e) === Zl;
};
G.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === Vl || e === Kl || e === Hl || e === Xl || e === Zl || typeof e == "object" && e !== null && (e.$$typeof === Jl || e.$$typeof === ql || e.$$typeof === Ql || e.$$typeof === Gl || e.$$typeof === Yl || e.$$typeof === q1 || e.getModuleId !== void 0);
};
G.typeOf = gt;
vh.exports = G;
var Kf = vh.exports;
const J1 = /^\s*function(?:\s|\s*\/\*.*\*\/\s*)+([^(\s/]*)\s*/;
function xh(e) {
  const t = `${e}`.match(J1);
  return t && t[1] || "";
}
function Sh(e, t = "") {
  return e.displayName || e.name || xh(e) || t;
}
function Gf(e, t, n) {
  const r = Sh(t);
  return e.displayName || (r !== "" ? `${n}(${r})` : n);
}
function ex(e) {
  if (e != null) {
    if (typeof e == "string")
      return e;
    if (typeof e == "function")
      return Sh(e, "Component");
    if (typeof e == "object")
      switch (e.$$typeof) {
        case Kf.ForwardRef:
          return Gf(e, e.render, "ForwardRef");
        case Kf.Memo:
          return Gf(e, e.type, "memo");
        default:
          return;
      }
  }
}
const tx = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: ex,
  getFunctionName: xh
}, Symbol.toStringTag, { value: "Module" }));
function Fa(e, t) {
  const n = C({}, t);
  return Object.keys(e).forEach((r) => {
    if (r.toString().match(/^(components|slots)$/))
      n[r] = C({}, e[r], n[r]);
    else if (r.toString().match(/^(componentsProps|slotProps)$/)) {
      const o = e[r] || {}, i = t[r];
      n[r] = {}, !i || !Object.keys(i) ? n[r] = o : !o || !Object.keys(o) ? n[r] = i : (n[r] = C({}, i), Object.keys(o).forEach((l) => {
        n[r][l] = Fa(o[l], i[l]);
      }));
    } else
      n[r] === void 0 && (n[r] = e[r]);
  }), n;
}
const nx = typeof window < "u" ? k.useLayoutEffect : k.useEffect, sc = nx;
function rx(e, t = Number.MIN_SAFE_INTEGER, n = Number.MAX_SAFE_INTEGER) {
  return Math.max(t, Math.min(e, n));
}
const ox = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: rx
}, Symbol.toStringTag, { value: "Module" }));
function ix(...e) {
  return e.reduce((t, n) => n == null ? t : function(...o) {
    t.apply(this, o), n.apply(this, o);
  }, () => {
  });
}
function lx(e, t = 166) {
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
function sx(e, t) {
  return () => null;
}
function ax(e, t) {
  var n, r;
  return /* @__PURE__ */ k.isValidElement(e) && t.indexOf(
    // For server components `muiName` is avaialble in element.type._payload.value.muiName
    // relevant info - https://github.com/facebook/react/blob/2807d781a08db8e9873687fccc25c0f12b4fb3d4/packages/react/src/ReactLazy.js#L45
    // eslint-disable-next-line no-underscore-dangle
    (n = e.type.muiName) != null ? n : (r = e.type) == null || (r = r._payload) == null || (r = r.value) == null ? void 0 : r.muiName
  ) !== -1;
}
function wh(e) {
  return e && e.ownerDocument || document;
}
function ux(e) {
  return wh(e).defaultView || window;
}
function cx(e, t) {
  return () => null;
}
function kh(e, t) {
  typeof e == "function" ? e(t) : e && (e.current = t);
}
let Qf = 0;
function fx(e) {
  const [t, n] = k.useState(e), r = e || t;
  return k.useEffect(() => {
    t == null && (Qf += 1, n(`mui-${Qf}`));
  }, [t]), r;
}
const Yf = Bs["useId".toString()];
function Ch(e) {
  if (Yf !== void 0) {
    const t = Yf();
    return e ?? t;
  }
  return fx(e);
}
function dx(e, t, n, r, o) {
  return null;
}
function px({
  controlled: e,
  default: t,
  name: n,
  state: r = "value"
}) {
  const {
    current: o
  } = k.useRef(e !== void 0), [i, l] = k.useState(t), s = o ? e : i, a = k.useCallback((u) => {
    o || l(u);
  }, []);
  return [s, a];
}
function Yr(e) {
  const t = k.useRef(e);
  return sc(() => {
    t.current = e;
  }), k.useRef((...n) => (
    // @ts-expect-error hide `this`
    (0, t.current)(...n)
  )).current;
}
function Ro(...e) {
  return k.useMemo(() => e.every((t) => t == null) ? null : (t) => {
    e.forEach((n) => {
      kh(n, t);
    });
  }, e);
}
const Xf = {};
function mx(e, t) {
  const n = k.useRef(Xf);
  return n.current === Xf && (n.current = e(t)), n;
}
const hx = [];
function gx(e) {
  k.useEffect(e, hx);
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
  const e = mx(es.create).current;
  return gx(e.disposeEffect), e;
}
let ts = !0, ba = !1;
const yx = new es(), vx = {
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
function xx(e) {
  const {
    type: t,
    tagName: n
  } = e;
  return !!(n === "INPUT" && vx[t] && !e.readOnly || n === "TEXTAREA" && !e.readOnly || e.isContentEditable);
}
function Sx(e) {
  e.metaKey || e.altKey || e.ctrlKey || (ts = !0);
}
function As() {
  ts = !1;
}
function wx() {
  this.visibilityState === "hidden" && ba && (ts = !0);
}
function kx(e) {
  e.addEventListener("keydown", Sx, !0), e.addEventListener("mousedown", As, !0), e.addEventListener("pointerdown", As, !0), e.addEventListener("touchstart", As, !0), e.addEventListener("visibilitychange", wx, !0);
}
function Cx(e) {
  const {
    target: t
  } = e;
  try {
    return t.matches(":focus-visible");
  } catch {
  }
  return ts || xx(t);
}
function _h() {
  const e = k.useCallback((o) => {
    o != null && kx(o.ownerDocument);
  }, []), t = k.useRef(!1);
  function n() {
    return t.current ? (ba = !0, yx.start(100, () => {
      ba = !1;
    }), t.current = !1, !0) : !1;
  }
  function r(o) {
    return Cx(o) ? (t.current = !0, !0) : !1;
  }
  return {
    isFocusVisibleRef: t,
    onFocus: r,
    onBlur: n,
    ref: e
  };
}
function Pt(e, t, n = void 0) {
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
function Ex(e) {
  return typeof e == "string";
}
function _x(e, t, n) {
  return e === void 0 || Ex(e) ? t : C({}, t, {
    ownerState: C({}, t.ownerState, n)
  });
}
function Px(e, t = []) {
  if (e === void 0)
    return {};
  const n = {};
  return Object.keys(e).filter((r) => r.match(/^on[A-Z]/) && typeof e[r] == "function" && !t.includes(r)).forEach((r) => {
    n[r] = e[r];
  }), n;
}
function Zf(e) {
  if (e === void 0)
    return {};
  const t = {};
  return Object.keys(e).filter((n) => !(n.match(/^on[A-Z]/) && typeof e[n] == "function")).forEach((n) => {
    t[n] = e[n];
  }), t;
}
function $x(e) {
  const {
    getSlotProps: t,
    additionalProps: n,
    externalSlotProps: r,
    externalForwardedProps: o,
    className: i
  } = e;
  if (!t) {
    const v = ne(n == null ? void 0 : n.className, i, o == null ? void 0 : o.className, r == null ? void 0 : r.className), y = C({}, n == null ? void 0 : n.style, o == null ? void 0 : o.style, r == null ? void 0 : r.style), g = C({}, n, o, r);
    return v.length > 0 && (g.className = v), Object.keys(y).length > 0 && (g.style = y), {
      props: g,
      internalRef: void 0
    };
  }
  const l = Px(C({}, o, r)), s = Zf(r), a = Zf(o), u = t(l), c = ne(u == null ? void 0 : u.className, n == null ? void 0 : n.className, i, o == null ? void 0 : o.className, r == null ? void 0 : r.className), d = C({}, u == null ? void 0 : u.style, n == null ? void 0 : n.style, o == null ? void 0 : o.style, r == null ? void 0 : r.style), m = C({}, u, n, a, s);
  return c.length > 0 && (m.className = c), Object.keys(d).length > 0 && (m.style = d), {
    props: m,
    internalRef: u.ref
  };
}
function Tx(e, t, n) {
  return typeof e == "function" ? e(t, n) : e;
}
const Rx = /* @__PURE__ */ k.createContext(null), Ph = Rx;
function $h() {
  return k.useContext(Ph);
}
const Ox = typeof Symbol == "function" && Symbol.for, Mx = Ox ? Symbol.for("mui.nested") : "__THEME_NESTED__";
function Nx(e, t) {
  return typeof t == "function" ? t(e) : C({}, e, t);
}
function zx(e) {
  const {
    children: t,
    theme: n
  } = e, r = $h(), o = k.useMemo(() => {
    const i = r === null ? n : Nx(r, n);
    return i != null && (i[Mx] = r !== null), i;
  }, [n, r]);
  return /* @__PURE__ */ _.jsx(Ph.Provider, {
    value: o,
    children: t
  });
}
const jx = ["value"], Ix = /* @__PURE__ */ k.createContext();
function Lx(e) {
  let {
    value: t
  } = e, n = K(e, jx);
  return /* @__PURE__ */ _.jsx(Ix.Provider, C({
    value: t ?? !0
  }, n));
}
const Th = /* @__PURE__ */ k.createContext(void 0);
function Ax({
  value: e,
  children: t
}) {
  return /* @__PURE__ */ _.jsx(Th.Provider, {
    value: e,
    children: t
  });
}
function Dx(e) {
  const {
    theme: t,
    name: n,
    props: r
  } = e;
  if (!t || !t.components || !t.components[n])
    return r;
  const o = t.components[n];
  return o.defaultProps ? Fa(o.defaultProps, r) : !o.styleOverrides && !o.variants ? Fa(o, r) : r;
}
function Fx({
  props: e,
  name: t
}) {
  const n = k.useContext(Th);
  return Dx({
    props: e,
    name: t,
    theme: {
      components: n
    }
  });
}
function bx(e) {
  const t = nc(), n = Ch() || "", {
    modularCssLayers: r
  } = e;
  let o = "mui.global, mui.components, mui.theme, mui.custom, mui.sx";
  return !r || t !== null ? o = "" : typeof r == "string" ? o = r.replace(/mui(?!\.)/g, o) : o = `@layer ${o};`, sc(() => {
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
  }, [o, n]), o ? /* @__PURE__ */ _.jsx(gh, {
    styles: o
  }) : null;
}
const qf = {};
function Jf(e, t, n, r = !1) {
  return k.useMemo(() => {
    const o = e && t[e] || t;
    if (typeof n == "function") {
      const i = n(o), l = e ? C({}, t, {
        [e]: i
      }) : i;
      return r ? () => l : l;
    }
    return e ? C({}, t, {
      [e]: n
    }) : C({}, t, n);
  }, [e, t, n, r]);
}
function Bx(e) {
  const {
    children: t,
    theme: n,
    themeId: r
  } = e, o = nc(qf), i = $h() || qf, l = Jf(r, o, n), s = Jf(r, i, n, !0), a = l.direction === "rtl", u = bx(l);
  return /* @__PURE__ */ _.jsx(zx, {
    theme: s,
    children: /* @__PURE__ */ _.jsx(Tr.Provider, {
      value: l,
      children: /* @__PURE__ */ _.jsx(Lx, {
        value: a,
        children: /* @__PURE__ */ _.jsxs(Ax, {
          value: l == null ? void 0 : l.components,
          children: [u, t]
        })
      })
    })
  });
}
function Wx(e, t) {
  return C({
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
var de = {}, Rh = { exports: {} };
(function(e) {
  function t(n) {
    return n && n.__esModule ? n : {
      default: n
    };
  }
  e.exports = t, e.exports.__esModule = !0, e.exports.default = e.exports;
})(Rh);
var ac = Rh.exports;
const Ux = /* @__PURE__ */ Gt(Ny), Vx = /* @__PURE__ */ Gt(ox);
var Oh = ac;
Object.defineProperty(de, "__esModule", {
  value: !0
});
var tl = de.alpha = jh;
de.blend = tS;
de.colorChannel = void 0;
var Ba = de.darken = cc;
de.decomposeColor = pt;
de.emphasize = Ih;
var Hx = de.getContrastRatio = Xx;
de.getLuminance = nl;
de.hexToRgb = Mh;
de.hslToRgb = zh;
var Wa = de.lighten = fc;
de.private_safeAlpha = Zx;
de.private_safeColorChannel = void 0;
de.private_safeDarken = qx;
de.private_safeEmphasize = eS;
de.private_safeLighten = Jx;
de.recomposeColor = Or;
de.rgbToHex = Yx;
var ed = Oh(Ux), Kx = Oh(Vx);
function uc(e, t = 0, n = 1) {
  return (0, Kx.default)(e, t, n);
}
function Mh(e) {
  e = e.slice(1);
  const t = new RegExp(`.{1,${e.length >= 6 ? 2 : 1}}`, "g");
  let n = e.match(t);
  return n && n[0].length === 1 && (n = n.map((r) => r + r)), n ? `rgb${n.length === 4 ? "a" : ""}(${n.map((r, o) => o < 3 ? parseInt(r, 16) : Math.round(parseInt(r, 16) / 255 * 1e3) / 1e3).join(", ")})` : "";
}
function Gx(e) {
  const t = e.toString(16);
  return t.length === 1 ? `0${t}` : t;
}
function pt(e) {
  if (e.type)
    return e;
  if (e.charAt(0) === "#")
    return pt(Mh(e));
  const t = e.indexOf("("), n = e.substring(0, t);
  if (["rgb", "rgba", "hsl", "hsla", "color"].indexOf(n) === -1)
    throw new Error((0, ed.default)(9, e));
  let r = e.substring(t + 1, e.length - 1), o;
  if (n === "color") {
    if (r = r.split(" "), o = r.shift(), r.length === 4 && r[3].charAt(0) === "/" && (r[3] = r[3].slice(1)), ["srgb", "display-p3", "a98-rgb", "prophoto-rgb", "rec-2020"].indexOf(o) === -1)
      throw new Error((0, ed.default)(10, o));
  } else
    r = r.split(",");
  return r = r.map((i) => parseFloat(i)), {
    type: n,
    values: r,
    colorSpace: o
  };
}
const Nh = (e) => {
  const t = pt(e);
  return t.values.slice(0, 3).map((n, r) => t.type.indexOf("hsl") !== -1 && r !== 0 ? `${n}%` : n).join(" ");
};
de.colorChannel = Nh;
const Qx = (e, t) => {
  try {
    return Nh(e);
  } catch {
    return e;
  }
};
de.private_safeColorChannel = Qx;
function Or(e) {
  const {
    type: t,
    colorSpace: n
  } = e;
  let {
    values: r
  } = e;
  return t.indexOf("rgb") !== -1 ? r = r.map((o, i) => i < 3 ? parseInt(o, 10) : o) : t.indexOf("hsl") !== -1 && (r[1] = `${r[1]}%`, r[2] = `${r[2]}%`), t.indexOf("color") !== -1 ? r = `${n} ${r.join(" ")}` : r = `${r.join(", ")}`, `${t}(${r})`;
}
function Yx(e) {
  if (e.indexOf("#") === 0)
    return e;
  const {
    values: t
  } = pt(e);
  return `#${t.map((n, r) => Gx(r === 3 ? Math.round(255 * n) : n)).join("")}`;
}
function zh(e) {
  e = pt(e);
  const {
    values: t
  } = e, n = t[0], r = t[1] / 100, o = t[2] / 100, i = r * Math.min(o, 1 - o), l = (u, c = (u + n / 30) % 12) => o - i * Math.max(Math.min(c - 3, 9 - c, 1), -1);
  let s = "rgb";
  const a = [Math.round(l(0) * 255), Math.round(l(8) * 255), Math.round(l(4) * 255)];
  return e.type === "hsla" && (s += "a", a.push(t[3])), Or({
    type: s,
    values: a
  });
}
function nl(e) {
  e = pt(e);
  let t = e.type === "hsl" || e.type === "hsla" ? pt(zh(e)).values : e.values;
  return t = t.map((n) => (e.type !== "color" && (n /= 255), n <= 0.03928 ? n / 12.92 : ((n + 0.055) / 1.055) ** 2.4)), Number((0.2126 * t[0] + 0.7152 * t[1] + 0.0722 * t[2]).toFixed(3));
}
function Xx(e, t) {
  const n = nl(e), r = nl(t);
  return (Math.max(n, r) + 0.05) / (Math.min(n, r) + 0.05);
}
function jh(e, t) {
  return e = pt(e), t = uc(t), (e.type === "rgb" || e.type === "hsl") && (e.type += "a"), e.type === "color" ? e.values[3] = `/${t}` : e.values[3] = t, Or(e);
}
function Zx(e, t, n) {
  try {
    return jh(e, t);
  } catch {
    return e;
  }
}
function cc(e, t) {
  if (e = pt(e), t = uc(t), e.type.indexOf("hsl") !== -1)
    e.values[2] *= 1 - t;
  else if (e.type.indexOf("rgb") !== -1 || e.type.indexOf("color") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] *= 1 - t;
  return Or(e);
}
function qx(e, t, n) {
  try {
    return cc(e, t);
  } catch {
    return e;
  }
}
function fc(e, t) {
  if (e = pt(e), t = uc(t), e.type.indexOf("hsl") !== -1)
    e.values[2] += (100 - e.values[2]) * t;
  else if (e.type.indexOf("rgb") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] += (255 - e.values[n]) * t;
  else if (e.type.indexOf("color") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] += (1 - e.values[n]) * t;
  return Or(e);
}
function Jx(e, t, n) {
  try {
    return fc(e, t);
  } catch {
    return e;
  }
}
function Ih(e, t = 0.15) {
  return nl(e) > 0.5 ? cc(e, t) : fc(e, t);
}
function eS(e, t, n) {
  try {
    return Ih(e, t);
  } catch {
    return e;
  }
}
function tS(e, t, n, r = 1) {
  const o = (a, u) => Math.round((a ** (1 / r) * (1 - n) + u ** (1 / r) * n) ** r), i = pt(e), l = pt(t), s = [o(i.values[0], l.values[0]), o(i.values[1], l.values[1]), o(i.values[2], l.values[2])];
  return Or({
    type: "rgb",
    values: s
  });
}
const nS = {
  black: "#000",
  white: "#fff"
}, Oo = nS, rS = {
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
}, oS = rS, iS = {
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
}, Bn = iS, lS = {
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
}, Wn = lS, sS = {
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
}, Ur = sS, aS = {
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
}, Un = aS, uS = {
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
}, Vn = uS, cS = {
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
}, Hn = cS, fS = ["mode", "contrastThreshold", "tonalOffset"], td = {
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
}, Ds = {
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
function nd(e, t, n, r) {
  const o = r.light || r, i = r.dark || r * 1.5;
  e[t] || (e.hasOwnProperty(n) ? e[t] = e[n] : t === "light" ? e.light = Wa(e.main, o) : t === "dark" && (e.dark = Ba(e.main, i)));
}
function dS(e = "light") {
  return e === "dark" ? {
    main: Un[200],
    light: Un[50],
    dark: Un[400]
  } : {
    main: Un[700],
    light: Un[400],
    dark: Un[800]
  };
}
function pS(e = "light") {
  return e === "dark" ? {
    main: Bn[200],
    light: Bn[50],
    dark: Bn[400]
  } : {
    main: Bn[500],
    light: Bn[300],
    dark: Bn[700]
  };
}
function mS(e = "light") {
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
function hS(e = "light") {
  return e === "dark" ? {
    main: Vn[400],
    light: Vn[300],
    dark: Vn[700]
  } : {
    main: Vn[700],
    light: Vn[500],
    dark: Vn[900]
  };
}
function gS(e = "light") {
  return e === "dark" ? {
    main: Hn[400],
    light: Hn[300],
    dark: Hn[700]
  } : {
    main: Hn[800],
    light: Hn[500],
    dark: Hn[900]
  };
}
function yS(e = "light") {
  return e === "dark" ? {
    main: Ur[400],
    light: Ur[300],
    dark: Ur[700]
  } : {
    main: "#ed6c02",
    // closest to orange[800] that pass 3:1.
    light: Ur[500],
    dark: Ur[900]
  };
}
function vS(e) {
  const {
    mode: t = "light",
    contrastThreshold: n = 3,
    tonalOffset: r = 0.2
  } = e, o = K(e, fS), i = e.primary || dS(t), l = e.secondary || pS(t), s = e.error || mS(t), a = e.info || hS(t), u = e.success || gS(t), c = e.warning || yS(t);
  function d(g) {
    return Hx(g, Ds.text.primary) >= n ? Ds.text.primary : td.text.primary;
  }
  const m = ({
    color: g,
    name: $,
    mainShade: p = 500,
    lightShade: f = 300,
    darkShade: h = 700
  }) => {
    if (g = C({}, g), !g.main && g[p] && (g.main = g[p]), !g.hasOwnProperty("main"))
      throw new Error(_o(11, $ ? ` (${$})` : "", p));
    if (typeof g.main != "string")
      throw new Error(_o(12, $ ? ` (${$})` : "", JSON.stringify(g.main)));
    return nd(g, "light", f, r), nd(g, "dark", h, r), g.contrastText || (g.contrastText = d(g.main)), g;
  }, v = {
    dark: Ds,
    light: td
  };
  return Lt(C({
    // A collection of common colors.
    common: C({}, Oo),
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
    grey: oS,
    // Used by `getContrastText()` to maximize the contrast between
    // the background and the text.
    contrastThreshold: n,
    // Takes a background color and returns the text color that maximizes the contrast.
    getContrastText: d,
    // Generate a rich color object.
    augmentColor: m,
    // Used by the functions below to shift a color's luminance by approximately
    // two indexes within its tonal palette.
    // E.g., shift from Red 500 to Red 300 or Red 700.
    tonalOffset: r
  }, v[t]), o);
}
const xS = ["fontFamily", "fontSize", "fontWeightLight", "fontWeightRegular", "fontWeightMedium", "fontWeightBold", "htmlFontSize", "allVariants", "pxToRem"];
function SS(e) {
  return Math.round(e * 1e5) / 1e5;
}
const rd = {
  textTransform: "uppercase"
}, od = '"Roboto", "Helvetica", "Arial", sans-serif';
function wS(e, t) {
  const n = typeof t == "function" ? t(e) : t, {
    fontFamily: r = od,
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
  } = n, m = K(n, xS), v = o / 14, y = d || ((p) => `${p / u * v}rem`), g = (p, f, h, x, E) => C({
    fontFamily: r,
    fontWeight: p,
    fontSize: y(f),
    // Unitless following https://meyerweb.com/eric/thoughts/2006/02/08/unitless-line-heights/
    lineHeight: h
  }, r === od ? {
    letterSpacing: `${SS(x / f)}em`
  } : {}, E, c), $ = {
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
    button: g(s, 14, 1.75, 0.4, rd),
    caption: g(l, 12, 1.66, 0.4),
    overline: g(l, 12, 2.66, 1, rd),
    // TODO v6: Remove handling of 'inherit' variant from the theme as it is already handled in Material UI's Typography component. Also, remember to remove the associated types.
    inherit: {
      fontFamily: "inherit",
      fontWeight: "inherit",
      fontSize: "inherit",
      lineHeight: "inherit",
      letterSpacing: "inherit"
    }
  };
  return Lt(C({
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
const kS = 0.2, CS = 0.14, ES = 0.12;
function J(...e) {
  return [`${e[0]}px ${e[1]}px ${e[2]}px ${e[3]}px rgba(0,0,0,${kS})`, `${e[4]}px ${e[5]}px ${e[6]}px ${e[7]}px rgba(0,0,0,${CS})`, `${e[8]}px ${e[9]}px ${e[10]}px ${e[11]}px rgba(0,0,0,${ES})`].join(",");
}
const _S = ["none", J(0, 2, 1, -1, 0, 1, 1, 0, 0, 1, 3, 0), J(0, 3, 1, -2, 0, 2, 2, 0, 0, 1, 5, 0), J(0, 3, 3, -2, 0, 3, 4, 0, 0, 1, 8, 0), J(0, 2, 4, -1, 0, 4, 5, 0, 0, 1, 10, 0), J(0, 3, 5, -1, 0, 5, 8, 0, 0, 1, 14, 0), J(0, 3, 5, -1, 0, 6, 10, 0, 0, 1, 18, 0), J(0, 4, 5, -2, 0, 7, 10, 1, 0, 2, 16, 1), J(0, 5, 5, -3, 0, 8, 10, 1, 0, 3, 14, 2), J(0, 5, 6, -3, 0, 9, 12, 1, 0, 3, 16, 2), J(0, 6, 6, -3, 0, 10, 14, 1, 0, 4, 18, 3), J(0, 6, 7, -4, 0, 11, 15, 1, 0, 4, 20, 3), J(0, 7, 8, -4, 0, 12, 17, 2, 0, 5, 22, 4), J(0, 7, 8, -4, 0, 13, 19, 2, 0, 5, 24, 4), J(0, 7, 9, -4, 0, 14, 21, 2, 0, 5, 26, 4), J(0, 8, 9, -5, 0, 15, 22, 2, 0, 6, 28, 5), J(0, 8, 10, -5, 0, 16, 24, 2, 0, 6, 30, 5), J(0, 8, 11, -5, 0, 17, 26, 2, 0, 6, 32, 5), J(0, 9, 11, -5, 0, 18, 28, 2, 0, 7, 34, 6), J(0, 9, 12, -6, 0, 19, 29, 2, 0, 7, 36, 6), J(0, 10, 13, -6, 0, 20, 31, 3, 0, 8, 38, 7), J(0, 10, 13, -6, 0, 21, 33, 3, 0, 8, 40, 7), J(0, 10, 14, -6, 0, 22, 35, 3, 0, 8, 42, 7), J(0, 11, 14, -7, 0, 23, 36, 3, 0, 9, 44, 8), J(0, 11, 15, -7, 0, 24, 38, 3, 0, 9, 46, 8)], PS = _S, $S = ["duration", "easing", "delay"], TS = {
  // This is the most common easing curve.
  easeInOut: "cubic-bezier(0.4, 0, 0.2, 1)",
  // Objects enter the screen at full velocity from off-screen and
  // slowly decelerate to a resting point.
  easeOut: "cubic-bezier(0.0, 0, 0.2, 1)",
  // Objects leave the screen at full velocity. They do not decelerate when off-screen.
  easeIn: "cubic-bezier(0.4, 0, 1, 1)",
  // The sharp curve is used by objects that may return to the screen at any time.
  sharp: "cubic-bezier(0.4, 0, 0.6, 1)"
}, Lh = {
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
function id(e) {
  return `${Math.round(e)}ms`;
}
function RS(e) {
  if (!e)
    return 0;
  const t = e / 36;
  return Math.round((4 + 15 * t ** 0.25 + t / 5) * 10);
}
function OS(e) {
  const t = C({}, TS, e.easing), n = C({}, Lh, e.duration);
  return C({
    getAutoHeightDuration: RS,
    create: (o = ["all"], i = {}) => {
      const {
        duration: l = n.standard,
        easing: s = t.easeInOut,
        delay: a = 0
      } = i;
      return K(i, $S), (Array.isArray(o) ? o : [o]).map((u) => `${u} ${typeof l == "string" ? l : id(l)} ${s} ${typeof a == "string" ? a : id(a)}`).join(",");
    }
  }, e, {
    easing: t,
    duration: n
  });
}
const MS = {
  mobileStepper: 1e3,
  fab: 1050,
  speedDial: 1050,
  appBar: 1100,
  drawer: 1200,
  modal: 1300,
  snackbar: 1400,
  tooltip: 1500
}, NS = MS, zS = ["breakpoints", "mixins", "spacing", "palette", "transitions", "typography", "shape"];
function dc(e = {}, ...t) {
  const {
    mixins: n = {},
    palette: r = {},
    transitions: o = {},
    typography: i = {}
  } = e, l = K(e, zS);
  if (e.vars && // The error should throw only for the root theme creation because user is not allowed to use a custom node `vars`.
  // `generateCssVars` is the closest identifier for checking that the `options` is a result of `extendTheme` with CSS variables so that user can create new theme for nested ThemeProvider.
  e.generateCssVars === void 0)
    throw new Error(_o(18));
  const s = vS(r), a = tc(e);
  let u = Lt(a, {
    mixins: Wx(a.breakpoints, n),
    palette: s,
    // Don't use [...shadows] until you've verified its transpiled code is not invoking the iterator protocol.
    shadows: PS.slice(),
    typography: wS(s, i),
    transitions: OS(o),
    zIndex: C({}, NS)
  });
  return u = Lt(u, l), u = t.reduce((c, d) => Lt(c, d), u), u.unstable_sxConfig = C({}, Bo, l == null ? void 0 : l.unstable_sxConfig), u.unstable_sx = function(d) {
    return Wl({
      sx: d,
      theme: this
    });
  }, u;
}
const jS = dc(), pc = jS;
function Ah() {
  const e = rc(pc);
  return e[kr] || e;
}
var Wo = {}, Fs = { exports: {} }, ld;
function IS() {
  return ld || (ld = 1, function(e) {
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
const LS = /* @__PURE__ */ Gt(Vv), AS = /* @__PURE__ */ Gt(Hv), DS = /* @__PURE__ */ Gt(qv), FS = /* @__PURE__ */ Gt(tx), bS = /* @__PURE__ */ Gt(b1), BS = /* @__PURE__ */ Gt(H1);
var Mr = ac;
Object.defineProperty(Wo, "__esModule", {
  value: !0
});
var WS = Wo.default = tw;
Wo.shouldForwardProp = $i;
Wo.systemDefaultTheme = void 0;
var rt = Mr(ih()), Ua = Mr(IS()), rl = YS(LS), US = AS;
Mr(DS);
Mr(FS);
var VS = Mr(bS), HS = Mr(BS);
const KS = ["ownerState"], GS = ["variants"], QS = ["name", "slot", "skipVariantsResolver", "skipSx", "overridesResolver"];
function Dh(e) {
  if (typeof WeakMap != "function")
    return null;
  var t = /* @__PURE__ */ new WeakMap(), n = /* @__PURE__ */ new WeakMap();
  return (Dh = function(r) {
    return r ? n : t;
  })(e);
}
function YS(e, t) {
  if (!t && e && e.__esModule)
    return e;
  if (e === null || typeof e != "object" && typeof e != "function")
    return { default: e };
  var n = Dh(t);
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
function XS(e) {
  return Object.keys(e).length === 0;
}
function ZS(e) {
  return typeof e == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  e.charCodeAt(0) > 96;
}
function $i(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
function sd(e, t) {
  return t && e && typeof e == "object" && e.styles && !e.styles.startsWith("@layer") && (e.styles = `@layer ${t}{${String(e.styles)}}`), e;
}
const qS = Wo.systemDefaultTheme = (0, VS.default)(), JS = (e) => e && e.charAt(0).toLowerCase() + e.slice(1);
function fi({
  defaultTheme: e,
  theme: t,
  themeId: n
}) {
  return XS(t) ? e : t[n] || t;
}
function ew(e) {
  return e ? (t, n) => n[e] : null;
}
function Ti(e, t, n) {
  let {
    ownerState: r
  } = t, o = (0, Ua.default)(t, KS);
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
    let a = (0, Ua.default)(i, GS);
    return l.forEach((u) => {
      let c = !0;
      if (typeof u.props == "function" ? c = u.props((0, rt.default)({
        ownerState: r
      }, o, r)) : Object.keys(u.props).forEach((d) => {
        (r == null ? void 0 : r[d]) !== u.props[d] && o[d] !== u.props[d] && (c = !1);
      }), c) {
        Array.isArray(a) || (a = [a]);
        const d = typeof u.style == "function" ? u.style((0, rt.default)({
          ownerState: r
        }, o, r)) : u.style;
        a.push(n ? sd((0, rl.internal_serializeStyles)(d), n) : d);
      }
    }), a;
  }
  return n ? sd((0, rl.internal_serializeStyles)(i), n) : i;
}
function tw(e = {}) {
  const {
    themeId: t,
    defaultTheme: n = qS,
    rootShouldForwardProp: r = $i,
    slotShouldForwardProp: o = $i
  } = e, i = (l) => (0, HS.default)((0, rt.default)({}, l, {
    theme: fi((0, rt.default)({}, l, {
      defaultTheme: n,
      themeId: t
    }))
  }));
  return i.__mui_systemSx = !0, (l, s = {}) => {
    (0, rl.internal_processStyles)(l, (w) => w.filter((S) => !(S != null && S.__mui_systemSx)));
    const {
      name: a,
      slot: u,
      skipVariantsResolver: c,
      skipSx: d,
      // TODO v6: remove `lowercaseFirstLetter()` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      overridesResolver: m = ew(JS(u))
    } = s, v = (0, Ua.default)(s, QS), y = a && a.startsWith("Mui") || u ? "components" : "custom", g = c !== void 0 ? c : (
      // TODO v6: remove `Root` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      u && u !== "Root" && u !== "root" || !1
    ), $ = d || !1;
    let p, f = $i;
    u === "Root" || u === "root" ? f = r : u ? f = o : ZS(l) && (f = void 0);
    const h = (0, rl.default)(l, (0, rt.default)({
      shouldForwardProp: f,
      label: p
    }, v)), x = (w) => typeof w == "function" && w.__emotion_real !== w || (0, US.isPlainObject)(w) ? (S) => {
      const T = fi({
        theme: S.theme,
        defaultTheme: n,
        themeId: t
      });
      return Ti(w, (0, rt.default)({}, S, {
        theme: T
      }), T.modularCssLayers ? y : void 0);
    } : w, E = (w, ...S) => {
      let T = x(w);
      const I = S ? S.map(x) : [];
      a && m && I.push((U) => {
        const b = fi((0, rt.default)({}, U, {
          defaultTheme: n,
          themeId: t
        }));
        if (!b.components || !b.components[a] || !b.components[a].styleOverrides)
          return null;
        const q = b.components[a].styleOverrides, ge = {};
        return Object.entries(q).forEach(([Ee, Se]) => {
          ge[Ee] = Ti(Se, (0, rt.default)({}, U, {
            theme: b
          }), b.modularCssLayers ? "theme" : void 0);
        }), m(U, ge);
      }), a && !g && I.push((U) => {
        var b;
        const q = fi((0, rt.default)({}, U, {
          defaultTheme: n,
          themeId: t
        })), ge = q == null || (b = q.components) == null || (b = b[a]) == null ? void 0 : b.variants;
        return Ti({
          variants: ge
        }, (0, rt.default)({}, U, {
          theme: q
        }), q.modularCssLayers ? "theme" : void 0);
      }), $ || I.push(i);
      const O = I.length - S.length;
      if (Array.isArray(w) && O > 0) {
        const U = new Array(O).fill("");
        T = [...w, ...U], T.raw = [...w.raw, ...U];
      }
      const F = h(T, ...I);
      return l.muiName && (F.muiName = l.muiName), F;
    };
    return h.withConfig && (E.withConfig = h.withConfig), E;
  };
}
function nw(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
const rw = (e) => nw(e) && e !== "classes", ow = rw, iw = WS({
  themeId: kr,
  defaultTheme: pc,
  rootShouldForwardProp: ow
}), pe = iw, lw = ["theme"];
function sw(e) {
  let {
    theme: t
  } = e, n = K(e, lw);
  const r = t[kr];
  let o = r || t;
  return typeof t != "function" && (r && !r.vars ? o = C({}, r, {
    vars: null
  }) : t && !t.vars && (o = C({}, t, {
    vars: null
  }))), /* @__PURE__ */ _.jsx(Bx, C({}, n, {
    themeId: r ? kr : void 0,
    theme: o
  }));
}
const aw = (e) => {
  let t;
  return e < 1 ? t = 5.11916 * e ** 2 : t = 4.5 * Math.log(e + 1) + 2, (t / 100).toFixed(2);
}, ad = aw;
function nt(e) {
  return Fx(e);
}
function uw(e) {
  return /* @__PURE__ */ _.jsx(gh, C({}, e, {
    defaultTheme: pc,
    themeId: kr
  }));
}
const cw = (e, t) => C({
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
}), fw = (e) => C({
  color: (e.vars || e).palette.text.primary
}, e.typography.body1, {
  backgroundColor: (e.vars || e).palette.background.default,
  "@media print": {
    // Save printer ink.
    backgroundColor: (e.vars || e).palette.common.white
  }
}), dw = (e, t = !1) => {
  var n;
  const r = {};
  t && e.colorSchemes && Object.entries(e.colorSchemes).forEach(([l, s]) => {
    var a;
    r[e.getColorSchemeSelector(l).replace(/\s*&/, "")] = {
      colorScheme: (a = s.palette) == null ? void 0 : a.mode
    };
  });
  let o = C({
    html: cw(e, t),
    "*, *::before, *::after": {
      boxSizing: "inherit"
    },
    "strong, b": {
      fontWeight: e.typography.fontWeightBold
    },
    body: C({
      margin: 0
    }, fw(e), {
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
function pw(e) {
  const t = nt({
    props: e,
    name: "MuiCssBaseline"
  }), {
    children: n,
    enableColorScheme: r = !1
  } = t;
  return /* @__PURE__ */ _.jsxs(k.Fragment, {
    children: [/* @__PURE__ */ _.jsx(uw, {
      styles: (o) => dw(o, r)
    }), n]
  });
}
function mw(e) {
  return ht("MuiCircularProgress", e);
}
tt("MuiCircularProgress", ["root", "determinate", "indeterminate", "colorPrimary", "colorSecondary", "svg", "circle", "circleDeterminate", "circleIndeterminate", "circleDisableShrink"]);
const hw = ["className", "color", "disableShrink", "size", "style", "thickness", "value", "variant"];
let ns = (e) => e, ud, cd, fd, dd;
const qt = 44, gw = Rr(ud || (ud = ns`
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
`)), yw = Rr(cd || (cd = ns`
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
`)), vw = (e) => {
  const {
    classes: t,
    variant: n,
    color: r,
    disableShrink: o
  } = e, i = {
    root: ["root", n, `color${oe(r)}`],
    svg: ["svg"],
    circle: ["circle", `circle${oe(n)}`, o && "circleDisableShrink"]
  };
  return Pt(i, mw, t);
}, xw = pe("span", {
  name: "MuiCircularProgress",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[n.variant], t[`color${oe(n.color)}`]];
  }
})(({
  ownerState: e,
  theme: t
}) => C({
  display: "inline-block"
}, e.variant === "determinate" && {
  transition: t.transitions.create("transform")
}, e.color !== "inherit" && {
  color: (t.vars || t).palette[e.color].main
}), ({
  ownerState: e
}) => e.variant === "indeterminate" && jl(fd || (fd = ns`
      animation: ${0} 1.4s linear infinite;
    `), gw)), Sw = pe("svg", {
  name: "MuiCircularProgress",
  slot: "Svg",
  overridesResolver: (e, t) => t.svg
})({
  display: "block"
  // Keeps the progress centered
}), ww = pe("circle", {
  name: "MuiCircularProgress",
  slot: "Circle",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.circle, t[`circle${oe(n.variant)}`], n.disableShrink && t.circleDisableShrink];
  }
})(({
  ownerState: e,
  theme: t
}) => C({
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
}) => e.variant === "indeterminate" && !e.disableShrink && jl(dd || (dd = ns`
      animation: ${0} 1.4s ease-in-out infinite;
    `), yw)), kw = /* @__PURE__ */ k.forwardRef(function(t, n) {
  const r = nt({
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
  } = r, m = K(r, hw), v = C({}, r, {
    color: i,
    disableShrink: l,
    size: s,
    thickness: u,
    value: c,
    variant: d
  }), y = vw(v), g = {}, $ = {}, p = {};
  if (d === "determinate") {
    const f = 2 * Math.PI * ((qt - u) / 2);
    g.strokeDasharray = f.toFixed(3), p["aria-valuenow"] = Math.round(c), g.strokeDashoffset = `${((100 - c) / 100 * f).toFixed(3)}px`, $.transform = "rotate(-90deg)";
  }
  return /* @__PURE__ */ _.jsx(xw, C({
    className: ne(y.root, o),
    style: C({
      width: s,
      height: s
    }, $, a),
    ownerState: v,
    ref: n,
    role: "progressbar"
  }, p, m, {
    children: /* @__PURE__ */ _.jsx(Sw, {
      className: y.svg,
      ownerState: v,
      viewBox: `${qt / 2} ${qt / 2} ${qt} ${qt}`,
      children: /* @__PURE__ */ _.jsx(ww, {
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
}), Cw = kw, Ew = ["className", "elementType", "ownerState", "externalForwardedProps", "getSlotOwnerState", "internalForwardedProps"], _w = ["component", "slots", "slotProps"], Pw = ["component"];
function pd(e, t) {
  const {
    className: n,
    elementType: r,
    ownerState: o,
    externalForwardedProps: i,
    getSlotOwnerState: l,
    internalForwardedProps: s
  } = t, a = K(t, Ew), {
    component: u,
    slots: c = {
      [e]: void 0
    },
    slotProps: d = {
      [e]: void 0
    }
  } = i, m = K(i, _w), v = c[e] || r, y = Tx(d[e], o), g = $x(C({
    className: n
  }, a, {
    externalForwardedProps: e === "root" ? m : void 0,
    externalSlotProps: y
  })), {
    props: {
      component: $
    },
    internalRef: p
  } = g, f = K(g.props, Pw), h = Ro(p, y == null ? void 0 : y.ref, t.ref), x = l ? l(f) : {}, E = C({}, o, x), w = e === "root" ? $ || u : $, S = _x(v, C({}, e === "root" && !u && !c[e] && s, e !== "root" && !c[e] && s, f, w && {
    as: w
  }, {
    ref: h
  }), E);
  return Object.keys(x).forEach((T) => {
    delete S[T];
  }), [v, S];
}
function $w(e) {
  return ht("MuiPaper", e);
}
tt("MuiPaper", ["root", "rounded", "outlined", "elevation", "elevation0", "elevation1", "elevation2", "elevation3", "elevation4", "elevation5", "elevation6", "elevation7", "elevation8", "elevation9", "elevation10", "elevation11", "elevation12", "elevation13", "elevation14", "elevation15", "elevation16", "elevation17", "elevation18", "elevation19", "elevation20", "elevation21", "elevation22", "elevation23", "elevation24"]);
const Tw = ["className", "component", "elevation", "square", "variant"], Rw = (e) => {
  const {
    square: t,
    elevation: n,
    variant: r,
    classes: o
  } = e, i = {
    root: ["root", r, !t && "rounded", r === "elevation" && `elevation${n}`]
  };
  return Pt(i, $w, o);
}, Ow = pe("div", {
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
  return C({
    backgroundColor: (e.vars || e).palette.background.paper,
    color: (e.vars || e).palette.text.primary,
    transition: e.transitions.create("box-shadow")
  }, !t.square && {
    borderRadius: e.shape.borderRadius
  }, t.variant === "outlined" && {
    border: `1px solid ${(e.vars || e).palette.divider}`
  }, t.variant === "elevation" && C({
    boxShadow: (e.vars || e).shadows[t.elevation]
  }, !e.vars && e.palette.mode === "dark" && {
    backgroundImage: `linear-gradient(${tl("#fff", ad(t.elevation))}, ${tl("#fff", ad(t.elevation))})`
  }, e.vars && {
    backgroundImage: (n = e.vars.overlays) == null ? void 0 : n[t.elevation]
  }));
}), Mw = /* @__PURE__ */ k.forwardRef(function(t, n) {
  const r = nt({
    props: t,
    name: "MuiPaper"
  }), {
    className: o,
    component: i = "div",
    elevation: l = 1,
    square: s = !1,
    variant: a = "elevation"
  } = r, u = K(r, Tw), c = C({}, r, {
    component: i,
    elevation: l,
    square: s,
    variant: a
  }), d = Rw(c);
  return /* @__PURE__ */ _.jsx(Ow, C({
    as: i,
    ownerState: c,
    className: ne(d.root, o),
    ref: n
  }, u));
}), rs = Mw;
function Nw(e) {
  return ht("MuiAlert", e);
}
const zw = tt("MuiAlert", ["root", "action", "icon", "message", "filled", "colorSuccess", "colorInfo", "colorWarning", "colorError", "filledSuccess", "filledInfo", "filledWarning", "filledError", "outlined", "outlinedSuccess", "outlinedInfo", "outlinedWarning", "outlinedError", "standard", "standardSuccess", "standardInfo", "standardWarning", "standardError"]), md = zw;
function Va(e, t) {
  return Va = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, r) {
    return n.__proto__ = r, n;
  }, Va(e, t);
}
function Fh(e, t) {
  e.prototype = Object.create(t.prototype), e.prototype.constructor = e, Va(e, t);
}
const hd = {
  disabled: !1
}, ol = kt.createContext(null);
var jw = function(t) {
  return t.scrollTop;
}, Xr = "unmounted", Cn = "exited", En = "entering", Gn = "entered", Ha = "exiting", Yt = /* @__PURE__ */ function(e) {
  Fh(t, e);
  function t(r, o) {
    var i;
    i = e.call(this, r, o) || this;
    var l = o, s = l && !l.isMounting ? r.enter : r.appear, a;
    return i.appearStatus = null, r.in ? s ? (a = Cn, i.appearStatus = En) : a = Gn : r.unmountOnExit || r.mountOnEnter ? a = Xr : a = Cn, i.state = {
      status: a
    }, i.nextCallback = null, i;
  }
  t.getDerivedStateFromProps = function(o, i) {
    var l = o.in;
    return l && i.status === Xr ? {
      status: Cn
    } : null;
  };
  var n = t.prototype;
  return n.componentDidMount = function() {
    this.updateStatus(!0, this.appearStatus);
  }, n.componentDidUpdate = function(o) {
    var i = null;
    if (o !== this.props) {
      var l = this.state.status;
      this.props.in ? l !== En && l !== Gn && (i = En) : (l === En || l === Gn) && (i = Ha);
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
      if (this.cancelNextCallback(), i === En) {
        if (this.props.unmountOnExit || this.props.mountOnEnter) {
          var l = this.props.nodeRef ? this.props.nodeRef.current : ui.findDOMNode(this);
          l && jw(l);
        }
        this.performEnter(o);
      } else
        this.performExit();
    else
      this.props.unmountOnExit && this.state.status === Cn && this.setState({
        status: Xr
      });
  }, n.performEnter = function(o) {
    var i = this, l = this.props.enter, s = this.context ? this.context.isMounting : o, a = this.props.nodeRef ? [s] : [ui.findDOMNode(this), s], u = a[0], c = a[1], d = this.getTimeouts(), m = s ? d.appear : d.enter;
    if (!o && !l || hd.disabled) {
      this.safeSetState({
        status: Gn
      }, function() {
        i.props.onEntered(u);
      });
      return;
    }
    this.props.onEnter(u, c), this.safeSetState({
      status: En
    }, function() {
      i.props.onEntering(u, c), i.onTransitionEnd(m, function() {
        i.safeSetState({
          status: Gn
        }, function() {
          i.props.onEntered(u, c);
        });
      });
    });
  }, n.performExit = function() {
    var o = this, i = this.props.exit, l = this.getTimeouts(), s = this.props.nodeRef ? void 0 : ui.findDOMNode(this);
    if (!i || hd.disabled) {
      this.safeSetState({
        status: Cn
      }, function() {
        o.props.onExited(s);
      });
      return;
    }
    this.props.onExit(s), this.safeSetState({
      status: Ha
    }, function() {
      o.props.onExiting(s), o.onTransitionEnd(l.exit, function() {
        o.safeSetState({
          status: Cn
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
    var l = this.props.nodeRef ? this.props.nodeRef.current : ui.findDOMNode(this), s = o == null && !this.props.addEndListener;
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
    if (o === Xr)
      return null;
    var i = this.props, l = i.children;
    i.in, i.mountOnEnter, i.unmountOnExit, i.appear, i.enter, i.exit, i.timeout, i.addEndListener, i.onEnter, i.onEntering, i.onEntered, i.onExit, i.onExiting, i.onExited, i.nodeRef;
    var s = K(i, ["children", "in", "mountOnEnter", "unmountOnExit", "appear", "enter", "exit", "timeout", "addEndListener", "onEnter", "onEntering", "onEntered", "onExit", "onExiting", "onExited", "nodeRef"]);
    return (
      // allows for nested Transitions
      /* @__PURE__ */ kt.createElement(ol.Provider, {
        value: null
      }, typeof l == "function" ? l(o, s) : kt.cloneElement(kt.Children.only(l), s))
    );
  }, t;
}(kt.Component);
Yt.contextType = ol;
Yt.propTypes = {};
function Kn() {
}
Yt.defaultProps = {
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
Yt.UNMOUNTED = Xr;
Yt.EXITED = Cn;
Yt.ENTERING = En;
Yt.ENTERED = Gn;
Yt.EXITING = Ha;
const Iw = Yt;
function Lw(e) {
  if (e === void 0)
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function mc(e, t) {
  var n = function(i) {
    return t && k.isValidElement(i) ? t(i) : i;
  }, r = /* @__PURE__ */ Object.create(null);
  return e && k.Children.map(e, function(o) {
    return o;
  }).forEach(function(o) {
    r[o.key] = n(o);
  }), r;
}
function Aw(e, t) {
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
function Tn(e, t, n) {
  return n[t] != null ? n[t] : e.props[t];
}
function Dw(e, t) {
  return mc(e.children, function(n) {
    return k.cloneElement(n, {
      onExited: t.bind(null, n),
      in: !0,
      appear: Tn(n, "appear", e),
      enter: Tn(n, "enter", e),
      exit: Tn(n, "exit", e)
    });
  });
}
function Fw(e, t, n) {
  var r = mc(e.children), o = Aw(t, r);
  return Object.keys(o).forEach(function(i) {
    var l = o[i];
    if (k.isValidElement(l)) {
      var s = i in t, a = i in r, u = t[i], c = k.isValidElement(u) && !u.props.in;
      a && (!s || c) ? o[i] = k.cloneElement(l, {
        onExited: n.bind(null, l),
        in: !0,
        exit: Tn(l, "exit", e),
        enter: Tn(l, "enter", e)
      }) : !a && s && !c ? o[i] = k.cloneElement(l, {
        in: !1
      }) : a && s && k.isValidElement(u) && (o[i] = k.cloneElement(l, {
        onExited: n.bind(null, l),
        in: u.props.in,
        exit: Tn(l, "exit", e),
        enter: Tn(l, "enter", e)
      }));
    }
  }), o;
}
var bw = Object.values || function(e) {
  return Object.keys(e).map(function(t) {
    return e[t];
  });
}, Bw = {
  component: "div",
  childFactory: function(t) {
    return t;
  }
}, hc = /* @__PURE__ */ function(e) {
  Fh(t, e);
  function t(r, o) {
    var i;
    i = e.call(this, r, o) || this;
    var l = i.handleExited.bind(Lw(i));
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
      children: a ? Dw(o, s) : Fw(o, l, s),
      firstRender: !1
    };
  }, n.handleExited = function(o, i) {
    var l = mc(this.props.children);
    o.key in l || (o.props.onExited && o.props.onExited(i), this.mounted && this.setState(function(s) {
      var a = C({}, s.children);
      return delete a[o.key], {
        children: a
      };
    }));
  }, n.render = function() {
    var o = this.props, i = o.component, l = o.childFactory, s = K(o, ["component", "childFactory"]), a = this.state.contextValue, u = bw(this.state.children).map(l);
    return delete s.appear, delete s.enter, delete s.exit, i === null ? /* @__PURE__ */ kt.createElement(ol.Provider, {
      value: a
    }, u) : /* @__PURE__ */ kt.createElement(ol.Provider, {
      value: a
    }, /* @__PURE__ */ kt.createElement(i, s, u));
  }, t;
}(kt.Component);
hc.propTypes = {};
hc.defaultProps = Bw;
const Ww = hc;
function Uw(e) {
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
  } = e, [c, d] = k.useState(!1), m = ne(t, n.ripple, n.rippleVisible, r && n.ripplePulsate), v = {
    width: l,
    height: l,
    top: -(l / 2) + i,
    left: -(l / 2) + o
  }, y = ne(n.child, c && n.childLeaving, r && n.childPulsate);
  return !s && !c && d(!0), k.useEffect(() => {
    if (!s && a != null) {
      const g = setTimeout(a, u);
      return () => {
        clearTimeout(g);
      };
    }
  }, [a, s, u]), /* @__PURE__ */ _.jsx("span", {
    className: m,
    style: v,
    children: /* @__PURE__ */ _.jsx("span", {
      className: y
    })
  });
}
const Vw = tt("MuiTouchRipple", ["root", "ripple", "rippleVisible", "ripplePulsate", "child", "childLeaving", "childPulsate"]), ot = Vw, Hw = ["center", "classes", "className"];
let os = (e) => e, gd, yd, vd, xd;
const Ka = 550, Kw = 80, Gw = Rr(gd || (gd = os`
  0% {
    transform: scale(0);
    opacity: 0.1;
  }

  100% {
    transform: scale(1);
    opacity: 0.3;
  }
`)), Qw = Rr(yd || (yd = os`
  0% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
`)), Yw = Rr(vd || (vd = os`
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(0.92);
  }

  100% {
    transform: scale(1);
  }
`)), Xw = pe("span", {
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
}), Zw = pe(Uw, {
  name: "MuiTouchRipple",
  slot: "Ripple"
})(xd || (xd = os`
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
`), ot.rippleVisible, Gw, Ka, ({
  theme: e
}) => e.transitions.easing.easeInOut, ot.ripplePulsate, ({
  theme: e
}) => e.transitions.duration.shorter, ot.child, ot.childLeaving, Qw, Ka, ({
  theme: e
}) => e.transitions.easing.easeInOut, ot.childPulsate, Yw, ({
  theme: e
}) => e.transitions.easing.easeInOut), qw = /* @__PURE__ */ k.forwardRef(function(t, n) {
  const r = nt({
    props: t,
    name: "MuiTouchRipple"
  }), {
    center: o = !1,
    classes: i = {},
    className: l
  } = r, s = K(r, Hw), [a, u] = k.useState([]), c = k.useRef(0), d = k.useRef(null);
  k.useEffect(() => {
    d.current && (d.current(), d.current = null);
  }, [a]);
  const m = k.useRef(!1), v = Eh(), y = k.useRef(null), g = k.useRef(null), $ = k.useCallback((x) => {
    const {
      pulsate: E,
      rippleX: w,
      rippleY: S,
      rippleSize: T,
      cb: I
    } = x;
    u((O) => [...O, /* @__PURE__ */ _.jsx(Zw, {
      classes: {
        ripple: ne(i.ripple, ot.ripple),
        rippleVisible: ne(i.rippleVisible, ot.rippleVisible),
        ripplePulsate: ne(i.ripplePulsate, ot.ripplePulsate),
        child: ne(i.child, ot.child),
        childLeaving: ne(i.childLeaving, ot.childLeaving),
        childPulsate: ne(i.childPulsate, ot.childPulsate)
      },
      timeout: Ka,
      pulsate: E,
      rippleX: w,
      rippleY: S,
      rippleSize: T
    }, c.current)]), c.current += 1, d.current = I;
  }, [i]), p = k.useCallback((x = {}, E = {}, w = () => {
  }) => {
    const {
      pulsate: S = !1,
      center: T = o || E.pulsate,
      fakeElement: I = !1
      // For test purposes
    } = E;
    if ((x == null ? void 0 : x.type) === "mousedown" && m.current) {
      m.current = !1;
      return;
    }
    (x == null ? void 0 : x.type) === "touchstart" && (m.current = !0);
    const O = I ? null : g.current, F = O ? O.getBoundingClientRect() : {
      width: 0,
      height: 0,
      left: 0,
      top: 0
    };
    let U, b, q;
    if (T || x === void 0 || x.clientX === 0 && x.clientY === 0 || !x.clientX && !x.touches)
      U = Math.round(F.width / 2), b = Math.round(F.height / 2);
    else {
      const {
        clientX: ge,
        clientY: Ee
      } = x.touches && x.touches.length > 0 ? x.touches[0] : x;
      U = Math.round(ge - F.left), b = Math.round(Ee - F.top);
    }
    if (T)
      q = Math.sqrt((2 * F.width ** 2 + F.height ** 2) / 3), q % 2 === 0 && (q += 1);
    else {
      const ge = Math.max(Math.abs((O ? O.clientWidth : 0) - U), U) * 2 + 2, Ee = Math.max(Math.abs((O ? O.clientHeight : 0) - b), b) * 2 + 2;
      q = Math.sqrt(ge ** 2 + Ee ** 2);
    }
    x != null && x.touches ? y.current === null && (y.current = () => {
      $({
        pulsate: S,
        rippleX: U,
        rippleY: b,
        rippleSize: q,
        cb: w
      });
    }, v.start(Kw, () => {
      y.current && (y.current(), y.current = null);
    })) : $({
      pulsate: S,
      rippleX: U,
      rippleY: b,
      rippleSize: q,
      cb: w
    });
  }, [o, $, v]), f = k.useCallback(() => {
    p({}, {
      pulsate: !0
    });
  }, [p]), h = k.useCallback((x, E) => {
    if (v.clear(), (x == null ? void 0 : x.type) === "touchend" && y.current) {
      y.current(), y.current = null, v.start(0, () => {
        h(x, E);
      });
      return;
    }
    y.current = null, u((w) => w.length > 0 ? w.slice(1) : w), d.current = E;
  }, [v]);
  return k.useImperativeHandle(n, () => ({
    pulsate: f,
    start: p,
    stop: h
  }), [f, p, h]), /* @__PURE__ */ _.jsx(Xw, C({
    className: ne(ot.root, i.root, l),
    ref: g
  }, s, {
    children: /* @__PURE__ */ _.jsx(Ww, {
      component: null,
      exit: !0,
      children: a
    })
  }));
}), Jw = qw;
function e2(e) {
  return ht("MuiButtonBase", e);
}
const t2 = tt("MuiButtonBase", ["root", "disabled", "focusVisible"]), n2 = t2, r2 = ["action", "centerRipple", "children", "className", "component", "disabled", "disableRipple", "disableTouchRipple", "focusRipple", "focusVisibleClassName", "LinkComponent", "onBlur", "onClick", "onContextMenu", "onDragLeave", "onFocus", "onFocusVisible", "onKeyDown", "onKeyUp", "onMouseDown", "onMouseLeave", "onMouseUp", "onTouchEnd", "onTouchMove", "onTouchStart", "tabIndex", "TouchRippleProps", "touchRippleRef", "type"], o2 = (e) => {
  const {
    disabled: t,
    focusVisible: n,
    focusVisibleClassName: r,
    classes: o
  } = e, l = Pt({
    root: ["root", t && "disabled", n && "focusVisible"]
  }, e2, o);
  return n && r && (l.root += ` ${r}`), l;
}, i2 = pe("button", {
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
  [`&.${n2.disabled}`]: {
    pointerEvents: "none",
    // Disable link interactions
    cursor: "default"
  },
  "@media print": {
    colorAdjust: "exact"
  }
}), l2 = /* @__PURE__ */ k.forwardRef(function(t, n) {
  const r = nt({
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
    focusRipple: m = !1,
    LinkComponent: v = "a",
    onBlur: y,
    onClick: g,
    onContextMenu: $,
    onDragLeave: p,
    onFocus: f,
    onFocusVisible: h,
    onKeyDown: x,
    onKeyUp: E,
    onMouseDown: w,
    onMouseLeave: S,
    onMouseUp: T,
    onTouchEnd: I,
    onTouchMove: O,
    onTouchStart: F,
    tabIndex: U = 0,
    TouchRippleProps: b,
    touchRippleRef: q,
    type: ge
  } = r, Ee = K(r, r2), Se = k.useRef(null), R = k.useRef(null), N = Ro(R, q), {
    isFocusVisibleRef: j,
    onFocus: Y,
    onBlur: le,
    ref: Xt
  } = _h(), [_e, $t] = k.useState(!1);
  u && _e && $t(!1), k.useImperativeHandle(o, () => ({
    focusVisible: () => {
      $t(!0), Se.current.focus();
    }
  }), []);
  const [z, ye] = k.useState(!1);
  k.useEffect(() => {
    ye(!0);
  }, []);
  const yt = z && !c && !u;
  k.useEffect(() => {
    _e && m && !c && z && R.current.pulsate();
  }, [c, m, _e, z]);
  function Ie(L, vc, r0 = d) {
    return Yr((xc) => (vc && vc(xc), !r0 && R.current && R.current[L](xc), !0));
  }
  const Fn = Ie("start", w), Uo = Ie("stop", $), Hh = Ie("stop", p), Kh = Ie("stop", T), Gh = Ie("stop", (L) => {
    _e && L.preventDefault(), S && S(L);
  }), Qh = Ie("start", F), Yh = Ie("stop", I), Xh = Ie("stop", O), Zh = Ie("stop", (L) => {
    le(L), j.current === !1 && $t(!1), y && y(L);
  }, !1), qh = Yr((L) => {
    Se.current || (Se.current = L.currentTarget), Y(L), j.current === !0 && ($t(!0), h && h(L)), f && f(L);
  }), is = () => {
    const L = Se.current;
    return a && a !== "button" && !(L.tagName === "A" && L.href);
  }, ls = k.useRef(!1), Jh = Yr((L) => {
    m && !ls.current && _e && R.current && L.key === " " && (ls.current = !0, R.current.stop(L, () => {
      R.current.start(L);
    })), L.target === L.currentTarget && is() && L.key === " " && L.preventDefault(), x && x(L), L.target === L.currentTarget && is() && L.key === "Enter" && !u && (L.preventDefault(), g && g(L));
  }), e0 = Yr((L) => {
    m && L.key === " " && R.current && _e && !L.defaultPrevented && (ls.current = !1, R.current.stop(L, () => {
      R.current.pulsate(L);
    })), E && E(L), g && L.target === L.currentTarget && is() && L.key === " " && !L.defaultPrevented && g(L);
  });
  let Vo = a;
  Vo === "button" && (Ee.href || Ee.to) && (Vo = v);
  const zr = {};
  Vo === "button" ? (zr.type = ge === void 0 ? "button" : ge, zr.disabled = u) : (!Ee.href && !Ee.to && (zr.role = "button"), u && (zr["aria-disabled"] = u));
  const t0 = Ro(n, Xt, Se), yc = C({}, r, {
    centerRipple: i,
    component: a,
    disabled: u,
    disableRipple: c,
    disableTouchRipple: d,
    focusRipple: m,
    tabIndex: U,
    focusVisible: _e
  }), n0 = o2(yc);
  return /* @__PURE__ */ _.jsxs(i2, C({
    as: Vo,
    className: ne(n0.root, s),
    ownerState: yc,
    onBlur: Zh,
    onClick: g,
    onContextMenu: Uo,
    onFocus: qh,
    onKeyDown: Jh,
    onKeyUp: e0,
    onMouseDown: Fn,
    onMouseLeave: Gh,
    onMouseUp: Kh,
    onDragLeave: Hh,
    onTouchEnd: Yh,
    onTouchMove: Xh,
    onTouchStart: Qh,
    ref: t0,
    tabIndex: u ? -1 : U,
    type: ge
  }, zr, Ee, {
    children: [l, yt ? (
      /* TouchRipple is only needed client-side, x2 boost on the server. */
      /* @__PURE__ */ _.jsx(Jw, C({
        ref: N,
        center: i
      }, b))
    ) : null]
  }));
}), s2 = l2;
function a2(e) {
  return ht("MuiIconButton", e);
}
const u2 = tt("MuiIconButton", ["root", "disabled", "colorInherit", "colorPrimary", "colorSecondary", "colorError", "colorInfo", "colorSuccess", "colorWarning", "edgeStart", "edgeEnd", "sizeSmall", "sizeMedium", "sizeLarge"]), c2 = u2, f2 = ["edge", "children", "className", "color", "disabled", "disableFocusRipple", "size"], d2 = (e) => {
  const {
    classes: t,
    disabled: n,
    color: r,
    edge: o,
    size: i
  } = e, l = {
    root: ["root", n && "disabled", r !== "default" && `color${oe(r)}`, o && `edge${oe(o)}`, `size${oe(i)}`]
  };
  return Pt(l, a2, t);
}, p2 = pe(s2, {
  name: "MuiIconButton",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.color !== "default" && t[`color${oe(n.color)}`], n.edge && t[`edge${oe(n.edge)}`], t[`size${oe(n.size)}`]];
  }
})(({
  theme: e,
  ownerState: t
}) => C({
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
    backgroundColor: e.vars ? `rgba(${e.vars.palette.action.activeChannel} / ${e.vars.palette.action.hoverOpacity})` : tl(e.palette.action.active, e.palette.action.hoverOpacity),
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
  return C({}, t.color === "inherit" && {
    color: "inherit"
  }, t.color !== "inherit" && t.color !== "default" && C({
    color: r == null ? void 0 : r.main
  }, !t.disableRipple && {
    "&:hover": C({}, r && {
      backgroundColor: e.vars ? `rgba(${r.mainChannel} / ${e.vars.palette.action.hoverOpacity})` : tl(r.main, e.palette.action.hoverOpacity)
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
    [`&.${c2.disabled}`]: {
      backgroundColor: "transparent",
      color: (e.vars || e).palette.action.disabled
    }
  });
}), m2 = /* @__PURE__ */ k.forwardRef(function(t, n) {
  const r = nt({
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
  } = r, d = K(r, f2), m = C({}, r, {
    edge: o,
    color: s,
    disabled: a,
    disableFocusRipple: u,
    size: c
  }), v = d2(m);
  return /* @__PURE__ */ _.jsx(p2, C({
    className: ne(v.root, l),
    centerRipple: !0,
    focusRipple: !u,
    disabled: a,
    ref: n
  }, d, {
    ownerState: m,
    children: i
  }));
}), bh = m2;
function h2(e) {
  return ht("MuiSvgIcon", e);
}
tt("MuiSvgIcon", ["root", "colorPrimary", "colorSecondary", "colorAction", "colorError", "colorDisabled", "fontSizeInherit", "fontSizeSmall", "fontSizeMedium", "fontSizeLarge"]);
const g2 = ["children", "className", "color", "component", "fontSize", "htmlColor", "inheritViewBox", "titleAccess", "viewBox"], y2 = (e) => {
  const {
    color: t,
    fontSize: n,
    classes: r
  } = e, o = {
    root: ["root", t !== "inherit" && `color${oe(t)}`, `fontSize${oe(n)}`]
  };
  return Pt(o, h2, r);
}, v2 = pe("svg", {
  name: "MuiSvgIcon",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.color !== "inherit" && t[`color${oe(n.color)}`], t[`fontSize${oe(n.fontSize)}`]];
  }
})(({
  theme: e,
  ownerState: t
}) => {
  var n, r, o, i, l, s, a, u, c, d, m, v, y;
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
    color: (d = (m = (e.vars || e).palette) == null || (m = m[t.color]) == null ? void 0 : m.main) != null ? d : {
      action: (v = (e.vars || e).palette) == null || (v = v.action) == null ? void 0 : v.active,
      disabled: (y = (e.vars || e).palette) == null || (y = y.action) == null ? void 0 : y.disabled,
      inherit: void 0
    }[t.color]
  };
}), Bh = /* @__PURE__ */ k.forwardRef(function(t, n) {
  const r = nt({
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
    viewBox: m = "0 0 24 24"
  } = r, v = K(r, g2), y = /* @__PURE__ */ k.isValidElement(o) && o.type === "svg", g = C({}, r, {
    color: l,
    component: s,
    fontSize: a,
    instanceFontSize: t.fontSize,
    inheritViewBox: c,
    viewBox: m,
    hasSvgAsChild: y
  }), $ = {};
  c || ($.viewBox = m);
  const p = y2(g);
  return /* @__PURE__ */ _.jsxs(v2, C({
    as: s,
    className: ne(p.root, i),
    focusable: "false",
    color: u,
    "aria-hidden": d ? void 0 : !0,
    role: d ? "img" : void 0,
    ref: n
  }, $, v, y && o.props, {
    ownerState: g,
    children: [y ? o.props.children : o, d ? /* @__PURE__ */ _.jsx("title", {
      children: d
    }) : null]
  }));
});
Bh.muiName = "SvgIcon";
const Sd = Bh;
function Nr(e, t) {
  function n(r, o) {
    return /* @__PURE__ */ _.jsx(Sd, C({
      "data-testid": `${t}Icon`,
      ref: o
    }, r, {
      children: e
    }));
  }
  return n.muiName = Sd.muiName, /* @__PURE__ */ k.memo(/* @__PURE__ */ k.forwardRef(n));
}
const x2 = Nr(/* @__PURE__ */ _.jsx("path", {
  d: "M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2, 4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0, 0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"
}), "SuccessOutlined"), S2 = Nr(/* @__PURE__ */ _.jsx("path", {
  d: "M12 5.99L19.53 19H4.47L12 5.99M12 2L1 21h22L12 2zm1 14h-2v2h2v-2zm0-6h-2v4h2v-4z"
}), "ReportProblemOutlined"), w2 = Nr(/* @__PURE__ */ _.jsx("path", {
  d: "M11 15h2v2h-2zm0-8h2v6h-2zm.99-5C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"
}), "ErrorOutline"), k2 = Nr(/* @__PURE__ */ _.jsx("path", {
  d: "M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"
}), "InfoOutlined"), C2 = Nr(/* @__PURE__ */ _.jsx("path", {
  d: "M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
}), "Close"), E2 = ["action", "children", "className", "closeText", "color", "components", "componentsProps", "icon", "iconMapping", "onClose", "role", "severity", "slotProps", "slots", "variant"], _2 = (e) => {
  const {
    variant: t,
    color: n,
    severity: r,
    classes: o
  } = e, i = {
    root: ["root", `color${oe(n || r)}`, `${t}${oe(n || r)}`, `${t}`],
    icon: ["icon"],
    message: ["message"],
    action: ["action"]
  };
  return Pt(i, Nw, o);
}, P2 = pe(rs, {
  name: "MuiAlert",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, t[n.variant], t[`${n.variant}${oe(n.color || n.severity)}`]];
  }
})(({
  theme: e
}) => {
  const t = e.palette.mode === "light" ? Ba : Wa, n = e.palette.mode === "light" ? Wa : Ba;
  return C({}, e.typography.body2, {
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
        [`& .${md.icon}`]: e.vars ? {
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
        [`& .${md.icon}`]: e.vars ? {
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
      style: C({
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
}), $2 = pe("div", {
  name: "MuiAlert",
  slot: "Icon",
  overridesResolver: (e, t) => t.icon
})({
  marginRight: 12,
  padding: "7px 0",
  display: "flex",
  fontSize: 22,
  opacity: 0.9
}), T2 = pe("div", {
  name: "MuiAlert",
  slot: "Message",
  overridesResolver: (e, t) => t.message
})({
  padding: "8px 0",
  minWidth: 0,
  overflow: "auto"
}), wd = pe("div", {
  name: "MuiAlert",
  slot: "Action",
  overridesResolver: (e, t) => t.action
})({
  display: "flex",
  alignItems: "flex-start",
  padding: "4px 0 0 16px",
  marginLeft: "auto",
  marginRight: -8
}), kd = {
  success: /* @__PURE__ */ _.jsx(x2, {
    fontSize: "inherit"
  }),
  warning: /* @__PURE__ */ _.jsx(S2, {
    fontSize: "inherit"
  }),
  error: /* @__PURE__ */ _.jsx(w2, {
    fontSize: "inherit"
  }),
  info: /* @__PURE__ */ _.jsx(k2, {
    fontSize: "inherit"
  })
}, R2 = /* @__PURE__ */ k.forwardRef(function(t, n) {
  const r = nt({
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
    iconMapping: m = kd,
    onClose: v,
    role: y = "alert",
    severity: g = "success",
    slotProps: $ = {},
    slots: p = {},
    variant: f = "standard"
  } = r, h = K(r, E2), x = C({}, r, {
    color: a,
    severity: g,
    variant: f,
    colorSeverity: a || g
  }), E = _2(x), w = {
    slots: C({
      closeButton: u.CloseButton,
      closeIcon: u.CloseIcon
    }, p),
    slotProps: C({}, c, $)
  }, [S, T] = pd("closeButton", {
    elementType: bh,
    externalForwardedProps: w,
    ownerState: x
  }), [I, O] = pd("closeIcon", {
    elementType: C2,
    externalForwardedProps: w,
    ownerState: x
  });
  return /* @__PURE__ */ _.jsxs(P2, C({
    role: y,
    elevation: 0,
    ownerState: x,
    className: ne(E.root, l),
    ref: n
  }, h, {
    children: [d !== !1 ? /* @__PURE__ */ _.jsx($2, {
      ownerState: x,
      className: E.icon,
      children: d || m[g] || kd[g]
    }) : null, /* @__PURE__ */ _.jsx(T2, {
      ownerState: x,
      className: E.message,
      children: i
    }), o != null ? /* @__PURE__ */ _.jsx(wd, {
      ownerState: x,
      className: E.action,
      children: o
    }) : null, o == null && v ? /* @__PURE__ */ _.jsx(wd, {
      ownerState: x,
      className: E.action,
      children: /* @__PURE__ */ _.jsx(S, C({
        size: "small",
        "aria-label": s,
        title: s,
        color: "inherit",
        onClick: v
      }, T, {
        children: /* @__PURE__ */ _.jsx(I, C({
          fontSize: "small"
        }, O))
      }))
    }) : null]
  }));
}), O2 = R2, M2 = tt("MuiBox", ["root"]), N2 = M2, z2 = dc(), j2 = Y1({
  themeId: kr,
  defaultTheme: z2,
  defaultClassName: N2.root,
  generateClassName: oc.generate
}), Mn = j2, I2 = /* @__PURE__ */ k.createContext(), Cd = I2;
function L2(e) {
  return ht("MuiGrid", e);
}
const A2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], D2 = ["column-reverse", "column", "row-reverse", "row"], F2 = ["nowrap", "wrap-reverse", "wrap"], Vr = ["auto", !0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], Mo = tt("MuiGrid", [
  "root",
  "container",
  "item",
  "zeroMinWidth",
  // spacings
  ...A2.map((e) => `spacing-xs-${e}`),
  // direction values
  ...D2.map((e) => `direction-xs-${e}`),
  // wrap values
  ...F2.map((e) => `wrap-xs-${e}`),
  // grid sizes for all breakpoints
  ...Vr.map((e) => `grid-xs-${e}`),
  ...Vr.map((e) => `grid-sm-${e}`),
  ...Vr.map((e) => `grid-md-${e}`),
  ...Vr.map((e) => `grid-lg-${e}`),
  ...Vr.map((e) => `grid-xl-${e}`)
]), b2 = ["className", "columns", "columnSpacing", "component", "container", "direction", "item", "rowSpacing", "spacing", "wrap", "zeroMinWidth"];
function mr(e) {
  const t = parseFloat(e);
  return `${t}${String(e).replace(String(t), "") || "px"}`;
}
function B2({
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
          const d = `calc(${a} + ${mr(c)})`;
          u = {
            flexBasis: d,
            maxWidth: d
          };
        }
      }
      i = C({
        flexBasis: a,
        flexGrow: 0,
        maxWidth: a
      }, u);
    }
    return e.breakpoints.values[o] === 0 ? Object.assign(r, i) : r[e.breakpoints.up(o)] = i, r;
  }, {});
}
function W2({
  theme: e,
  ownerState: t
}) {
  const n = Il({
    values: t.direction,
    breakpoints: e.breakpoints.values
  });
  return dt({
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
function Wh({
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
function U2({
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
    typeof i == "object" && (l = Wh({
      breakpoints: e.breakpoints.values,
      values: i
    })), o = dt({
      theme: e
    }, i, (s, a) => {
      var u;
      const c = e.spacing(s);
      return c !== "0px" ? {
        marginTop: `-${mr(c)}`,
        [`& > .${Mo.item}`]: {
          paddingTop: mr(c)
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
function V2({
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
    typeof i == "object" && (l = Wh({
      breakpoints: e.breakpoints.values,
      values: i
    })), o = dt({
      theme: e
    }, i, (s, a) => {
      var u;
      const c = e.spacing(s);
      return c !== "0px" ? {
        width: `calc(100% + ${mr(c)})`,
        marginLeft: `-${mr(c)}`,
        [`& > .${Mo.item}`]: {
          paddingLeft: mr(c)
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
function H2(e, t, n = {}) {
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
const K2 = pe("div", {
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
    r && (c = H2(l, u, t));
    const d = [];
    return u.forEach((m) => {
      const v = n[m];
      v && d.push(t[`grid-${m}-${String(v)}`]);
    }), [t.root, r && t.container, i && t.item, a && t.zeroMinWidth, ...c, o !== "row" && t[`direction-xs-${String(o)}`], s !== "wrap" && t[`wrap-xs-${String(s)}`], ...d];
  }
})(({
  ownerState: e
}) => C({
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
}), W2, U2, V2, B2);
function G2(e, t) {
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
const Q2 = (e) => {
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
  n && (u = G2(i, a));
  const c = [];
  a.forEach((m) => {
    const v = e[m];
    v && c.push(`grid-${m}-${String(v)}`);
  });
  const d = {
    root: ["root", n && "container", o && "item", s && "zeroMinWidth", ...u, r !== "row" && `direction-xs-${String(r)}`, l !== "wrap" && `wrap-xs-${String(l)}`, ...c]
  };
  return Pt(d, L2, t);
}, Y2 = /* @__PURE__ */ k.forwardRef(function(t, n) {
  const r = nt({
    props: t,
    name: "MuiGrid"
  }), {
    breakpoints: o
  } = Ah(), i = Ul(r), {
    className: l,
    columns: s,
    columnSpacing: a,
    component: u = "div",
    container: c = !1,
    direction: d = "row",
    item: m = !1,
    rowSpacing: v,
    spacing: y = 0,
    wrap: g = "wrap",
    zeroMinWidth: $ = !1
  } = i, p = K(i, b2), f = v || y, h = a || y, x = k.useContext(Cd), E = c ? s || 12 : x, w = {}, S = C({}, p);
  o.keys.forEach((O) => {
    p[O] != null && (w[O] = p[O], delete S[O]);
  });
  const T = C({}, i, {
    columns: E,
    container: c,
    direction: d,
    item: m,
    rowSpacing: f,
    columnSpacing: h,
    wrap: g,
    zeroMinWidth: $,
    spacing: y
  }, w, {
    breakpoints: o.keys
  }), I = Q2(T);
  return /* @__PURE__ */ _.jsx(Cd.Provider, {
    value: E,
    children: /* @__PURE__ */ _.jsx(K2, C({
      ownerState: T,
      className: ne(I.root, l),
      as: u,
      ref: n
    }, S))
  });
}), Bt = Y2;
function X2(e) {
  return ht("MuiTypography", e);
}
tt("MuiTypography", ["root", "h1", "h2", "h3", "h4", "h5", "h6", "subtitle1", "subtitle2", "body1", "body2", "inherit", "button", "caption", "overline", "alignLeft", "alignRight", "alignCenter", "alignJustify", "noWrap", "gutterBottom", "paragraph"]);
const Z2 = ["align", "className", "component", "gutterBottom", "noWrap", "paragraph", "variant", "variantMapping"], q2 = (e) => {
  const {
    align: t,
    gutterBottom: n,
    noWrap: r,
    paragraph: o,
    variant: i,
    classes: l
  } = e, s = {
    root: ["root", i, e.align !== "inherit" && `align${oe(t)}`, n && "gutterBottom", r && "noWrap", o && "paragraph"]
  };
  return Pt(s, X2, l);
}, J2 = pe("span", {
  name: "MuiTypography",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [t.root, n.variant && t[n.variant], n.align !== "inherit" && t[`align${oe(n.align)}`], n.noWrap && t.noWrap, n.gutterBottom && t.gutterBottom, n.paragraph && t.paragraph];
  }
})(({
  theme: e,
  ownerState: t
}) => C({
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
})), Ed = {
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
}, ek = {
  primary: "primary.main",
  textPrimary: "text.primary",
  secondary: "secondary.main",
  textSecondary: "text.secondary",
  error: "error.main"
}, tk = (e) => ek[e] || e, nk = /* @__PURE__ */ k.forwardRef(function(t, n) {
  const r = nt({
    props: t,
    name: "MuiTypography"
  }), o = tk(r.color), i = Ul(C({}, r, {
    color: o
  })), {
    align: l = "inherit",
    className: s,
    component: a,
    gutterBottom: u = !1,
    noWrap: c = !1,
    paragraph: d = !1,
    variant: m = "body1",
    variantMapping: v = Ed
  } = i, y = K(i, Z2), g = C({}, i, {
    align: l,
    color: o,
    className: s,
    component: a,
    gutterBottom: u,
    noWrap: c,
    paragraph: d,
    variant: m,
    variantMapping: v
  }), $ = a || (d ? "p" : v[m] || Ed[m]) || "span", p = q2(g);
  return /* @__PURE__ */ _.jsx(J2, C({
    as: $,
    ref: n,
    ownerState: g,
    className: ne(p.root, s)
  }, y));
}), hn = nk, rk = () => /* @__PURE__ */ _.jsx(Mn, { sx: {
  backgroundColor: "background.paper",
  p: 2.5,
  borderBottom: "1px solid",
  borderColor: "divider"
}, children: /* @__PURE__ */ _.jsx(hn, { variant: "h4", component: "h1", children: "Meraki Integration Control" }) });
function _d(e, t) {
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
const ok = {
  configure: (e) => {
    oc.configure(e);
  }
}, ik = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  capitalize: oe,
  createChainedFunction: ix,
  createSvgIcon: Nr,
  debounce: lx,
  deprecatedPropType: sx,
  isMuiElement: ax,
  ownerDocument: wh,
  ownerWindow: ux,
  requirePropFactory: cx,
  setRef: kh,
  unstable_ClassNameGenerator: ok,
  unstable_useEnhancedEffect: sc,
  unstable_useId: Ch,
  unsupportedProp: dx,
  useControlled: px,
  useEventCallback: Yr,
  useForkRef: Ro,
  useIsFocusVisible: _h
}, Symbol.toStringTag, { value: "Module" }));
function lk(e) {
  return ht("MuiCollapse", e);
}
tt("MuiCollapse", ["root", "horizontal", "vertical", "entered", "hidden", "wrapper", "wrapperInner"]);
const sk = ["addEndListener", "children", "className", "collapsedSize", "component", "easing", "in", "onEnter", "onEntered", "onEntering", "onExit", "onExited", "onExiting", "orientation", "style", "timeout", "TransitionComponent"], ak = (e) => {
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
  return Pt(r, lk, n);
}, uk = pe("div", {
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
}) => C({
  height: 0,
  overflow: "hidden",
  transition: e.transitions.create("height")
}, t.orientation === "horizontal" && {
  height: "auto",
  width: 0,
  transition: e.transitions.create("width")
}, t.state === "entered" && C({
  height: "auto",
  overflow: "visible"
}, t.orientation === "horizontal" && {
  width: "auto"
}), t.state === "exited" && !t.in && t.collapsedSize === "0px" && {
  visibility: "hidden"
})), ck = pe("div", {
  name: "MuiCollapse",
  slot: "Wrapper",
  overridesResolver: (e, t) => t.wrapper
})(({
  ownerState: e
}) => C({
  // Hack to get children with a negative margin to not falsify the height computation.
  display: "flex",
  width: "100%"
}, e.orientation === "horizontal" && {
  width: "auto",
  height: "100%"
})), fk = pe("div", {
  name: "MuiCollapse",
  slot: "WrapperInner",
  overridesResolver: (e, t) => t.wrapperInner
})(({
  ownerState: e
}) => C({
  width: "100%"
}, e.orientation === "horizontal" && {
  width: "auto",
  height: "100%"
})), Uh = /* @__PURE__ */ k.forwardRef(function(t, n) {
  const r = nt({
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
    onEnter: d,
    onEntered: m,
    onEntering: v,
    onExit: y,
    onExited: g,
    onExiting: $,
    orientation: p = "vertical",
    style: f,
    timeout: h = Lh.standard,
    // eslint-disable-next-line react/prop-types
    TransitionComponent: x = Iw
  } = r, E = K(r, sk), w = C({}, r, {
    orientation: p,
    collapsedSize: s
  }), S = ak(w), T = Ah(), I = Eh(), O = k.useRef(null), F = k.useRef(), U = typeof s == "number" ? `${s}px` : s, b = p === "horizontal", q = b ? "width" : "height", ge = k.useRef(null), Ee = Ro(n, ge), Se = (z) => (ye) => {
    if (z) {
      const yt = ge.current;
      ye === void 0 ? z(yt) : z(yt, ye);
    }
  }, R = () => O.current ? O.current[b ? "clientWidth" : "clientHeight"] : 0, N = Se((z, ye) => {
    O.current && b && (O.current.style.position = "absolute"), z.style[q] = U, d && d(z, ye);
  }), j = Se((z, ye) => {
    const yt = R();
    O.current && b && (O.current.style.position = "");
    const {
      duration: Ie,
      easing: Fn
    } = _d({
      style: f,
      timeout: h,
      easing: u
    }, {
      mode: "enter"
    });
    if (h === "auto") {
      const Uo = T.transitions.getAutoHeightDuration(yt);
      z.style.transitionDuration = `${Uo}ms`, F.current = Uo;
    } else
      z.style.transitionDuration = typeof Ie == "string" ? Ie : `${Ie}ms`;
    z.style[q] = `${yt}px`, z.style.transitionTimingFunction = Fn, v && v(z, ye);
  }), Y = Se((z, ye) => {
    z.style[q] = "auto", m && m(z, ye);
  }), le = Se((z) => {
    z.style[q] = `${R()}px`, y && y(z);
  }), Xt = Se(g), _e = Se((z) => {
    const ye = R(), {
      duration: yt,
      easing: Ie
    } = _d({
      style: f,
      timeout: h,
      easing: u
    }, {
      mode: "exit"
    });
    if (h === "auto") {
      const Fn = T.transitions.getAutoHeightDuration(ye);
      z.style.transitionDuration = `${Fn}ms`, F.current = Fn;
    } else
      z.style.transitionDuration = typeof yt == "string" ? yt : `${yt}ms`;
    z.style[q] = U, z.style.transitionTimingFunction = Ie, $ && $(z);
  }), $t = (z) => {
    h === "auto" && I.start(F.current || 0, z), o && o(ge.current, z);
  };
  return /* @__PURE__ */ _.jsx(x, C({
    in: c,
    onEnter: N,
    onEntered: Y,
    onEntering: j,
    onExit: le,
    onExited: Xt,
    onExiting: _e,
    addEndListener: $t,
    nodeRef: ge,
    timeout: h === "auto" ? null : h
  }, E, {
    children: (z, ye) => /* @__PURE__ */ _.jsx(uk, C({
      as: a,
      className: ne(S.root, l, {
        entered: S.entered,
        exited: !c && U === "0px" && S.hidden
      }[z]),
      style: C({
        [b ? "minWidth" : "minHeight"]: U
      }, f),
      ref: Ee
    }, ye, {
      // `ownerState` is set after `childProps` to override any existing `ownerState` property in `childProps`
      // that might have been forwarded from the Transition component.
      ownerState: C({}, w, {
        state: z
      }),
      children: /* @__PURE__ */ _.jsx(ck, {
        ownerState: C({}, w, {
          state: z
        }),
        className: S.wrapper,
        ref: O,
        children: /* @__PURE__ */ _.jsx(fk, {
          ownerState: C({}, w, {
            state: z
          }),
          className: S.wrapperInner,
          children: i
        })
      })
    }))
  }));
});
Uh.muiSupportAuto = !0;
const dk = Uh;
var gc = {}, bs = {};
const pk = /* @__PURE__ */ Gt(ik);
var Pd;
function mk() {
  return Pd || (Pd = 1, function(e) {
    "use client";
    Object.defineProperty(e, "__esModule", {
      value: !0
    }), Object.defineProperty(e, "default", {
      enumerable: !0,
      get: function() {
        return t.createSvgIcon;
      }
    });
    var t = pk;
  }(bs)), bs;
}
var hk = ac;
Object.defineProperty(gc, "__esModule", {
  value: !0
});
var Vh = gc.default = void 0, gk = hk(mk()), yk = _;
Vh = gc.default = (0, gk.default)(/* @__PURE__ */ (0, yk.jsx)("path", {
  d: "M16.59 8.59 12 13.17 7.41 8.59 6 10l6 6 6-6z"
}), "ExpandMore");
const vk = ({ devices: e }) => {
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
  return /* @__PURE__ */ _.jsx(Bt, { container: !0, spacing: 2, children: n.map(([r, o]) => /* @__PURE__ */ _.jsxs(Bt, { item: !0, xs: 12, children: [
    /* @__PURE__ */ _.jsx(hn, { variant: "h6", sx: { mb: 1, color: "text.secondary" }, children: r }),
    /* @__PURE__ */ _.jsx(Bt, { container: !0, spacing: 2, children: o.map((i) => /* @__PURE__ */ _.jsx(Bt, { item: !0, xs: 12, sm: 6, md: 4, children: /* @__PURE__ */ _.jsxs(
      rs,
      {
        sx: {
          p: 2,
          borderRadius: 1,
          backgroundColor: "action.hover"
        },
        children: [
          /* @__PURE__ */ _.jsx(hn, { variant: "body1", sx: { fontWeight: 500 }, children: i.name || "Unnamed Device" }),
          /* @__PURE__ */ _.jsxs(hn, { variant: "body2", color: "text.secondary", children: [
            i.model,
            " (",
            i.mac,
            ")"
          ] })
        ]
      }
    ) }, i.serial)) })
  ] }, r)) });
}, xk = pe((e) => {
  const { expand: t, ...n } = e;
  return /* @__PURE__ */ _.jsx(bh, { ...n });
})(({ theme: e, expand: t }) => ({
  transform: t ? "rotate(180deg)" : "rotate(0deg)",
  marginLeft: "auto",
  color: e.palette.text.secondary,
  transition: e.transitions.create("transform", {
    duration: e.transitions.duration.shortest
  })
})), Sk = ({ data: e }) => {
  const { networks: t = [], devices: n = [] } = e, [r, o] = k.useState(!1), i = (l) => {
    o(r === l ? !1 : l);
  };
  return /* @__PURE__ */ _.jsxs(rs, { sx: { p: 2, backgroundColor: "background.paper", borderRadius: 2 }, children: [
    /* @__PURE__ */ _.jsx(hn, { variant: "h5", sx: { mb: 2, color: "text.primary" }, children: "Networks" }),
    /* @__PURE__ */ _.jsx(Bt, { container: !0, spacing: 2, children: t.map((l) => {
      const s = n.filter((u) => u.networkId === l.id), a = r === l.id;
      return /* @__PURE__ */ _.jsxs(Bt, { item: !0, xs: 12, children: [
        /* @__PURE__ */ _.jsxs(
          Mn,
          {
            sx: {
              display: "flex",
              alignItems: "center",
              cursor: "pointer",
              p: 2,
              borderRadius: 1,
              backgroundColor: "action.hover",
              "&:hover": {
                backgroundColor: "action.selected"
              }
            },
            onClick: () => i(l.id),
            children: [
              /* @__PURE__ */ _.jsx(hn, { variant: "h6", component: "div", sx: { flexGrow: 1 }, children: l.name }),
              /* @__PURE__ */ _.jsx(
                xk,
                {
                  expand: a,
                  "aria-expanded": a,
                  "aria-label": "show more",
                  children: /* @__PURE__ */ _.jsx(Vh, {})
                }
              )
            ]
          }
        ),
        /* @__PURE__ */ _.jsx(dk, { in: a, timeout: "auto", unmountOnExit: !0, children: /* @__PURE__ */ _.jsx(Mn, { sx: { p: 2, borderTop: "1px solid", borderColor: "divider" }, children: /* @__PURE__ */ _.jsx(vk, { devices: s }) }) })
      ] }, l.id);
    }) })
  ] });
};
function wk(e) {
  return ht("MuiCard", e);
}
tt("MuiCard", ["root"]);
const kk = ["className", "raised"], Ck = (e) => {
  const {
    classes: t
  } = e;
  return Pt({
    root: ["root"]
  }, wk, t);
}, Ek = pe(rs, {
  name: "MuiCard",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})(() => ({
  overflow: "hidden"
})), _k = /* @__PURE__ */ k.forwardRef(function(t, n) {
  const r = nt({
    props: t,
    name: "MuiCard"
  }), {
    className: o,
    raised: i = !1
  } = r, l = K(r, kk), s = C({}, r, {
    raised: i
  }), a = Ck(s);
  return /* @__PURE__ */ _.jsx(Ek, C({
    className: ne(a.root, o),
    elevation: i ? 8 : void 0,
    ref: n,
    ownerState: s
  }, l));
}), Pk = _k;
function $k(e) {
  return ht("MuiCardContent", e);
}
tt("MuiCardContent", ["root"]);
const Tk = ["className", "component"], Rk = (e) => {
  const {
    classes: t
  } = e;
  return Pt({
    root: ["root"]
  }, $k, t);
}, Ok = pe("div", {
  name: "MuiCardContent",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})(() => ({
  padding: 16,
  "&:last-child": {
    paddingBottom: 24
  }
})), Mk = /* @__PURE__ */ k.forwardRef(function(t, n) {
  const r = nt({
    props: t,
    name: "MuiCardContent"
  }), {
    className: o,
    component: i = "div"
  } = r, l = K(r, Tk), s = C({}, r, {
    component: i
  }), a = Rk(s);
  return /* @__PURE__ */ _.jsx(Ok, C({
    as: i,
    className: ne(a.root, o),
    ownerState: s,
    ref: n
  }, l));
}), Nk = Mk, zk = () => /* @__PURE__ */ _.jsxs(Mn, { sx: { mt: 4 }, children: [
  /* @__PURE__ */ _.jsx(hn, { variant: "h5", component: "h2", sx: { mb: 2 }, children: "Event Log" }),
  /* @__PURE__ */ _.jsx(
    Pk,
    {
      sx: {
        borderRadius: 2,
        boxShadow: "none",
        border: "1px solid",
        borderColor: "divider"
      },
      children: /* @__PURE__ */ _.jsx(Nk, { sx: { p: 2.5 }, children: /* @__PURE__ */ _.jsx(hn, { color: "text.secondary", children: "Integration-specific events will be displayed here." }) })
    }
  )
] }), jk = (e) => {
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
}, Ik = (e) => dc(jk(e));
const Lk = ({ hass: e, config_entry_id: t }) => {
  const [n, r] = k.useState(null), [o, i] = k.useState(!0), [l, s] = k.useState(null), a = k.useMemo(() => {
    var u;
    return Ik(((u = e == null ? void 0 : e.themes) == null ? void 0 : u.darkMode) ?? !0);
  }, [e]);
  return k.useEffect(() => {
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
  }, [e, t]), /* @__PURE__ */ _.jsxs(sw, { theme: a, children: [
    /* @__PURE__ */ _.jsx(pw, {}),
    /* @__PURE__ */ _.jsxs(Mn, { sx: { display: "flex", flexDirection: "column", height: "100vh", backgroundColor: a.palette.background.default }, children: [
      /* @__PURE__ */ _.jsx(rk, {}),
      /* @__PURE__ */ _.jsxs(Mn, { sx: { flexGrow: 1, p: 3, overflow: "auto" }, children: [
        o && /* @__PURE__ */ _.jsx(Mn, { sx: { display: "flex", justifyContent: "center", p: 4 }, children: /* @__PURE__ */ _.jsx(Cw, {}) }),
        l && /* @__PURE__ */ _.jsx(O2, { severity: "error", sx: { mt: 2 }, children: l }),
        !o && !l && n && /* @__PURE__ */ _.jsxs(Bt, { container: !0, spacing: 3, children: [
          /* @__PURE__ */ _.jsx(Bt, { item: !0, xs: 12, md: 8, children: /* @__PURE__ */ _.jsx(Sk, { data: n }) }),
          /* @__PURE__ */ _.jsx(Bt, { item: !0, xs: 12, md: 4, children: /* @__PURE__ */ _.jsx(zk, {}) })
        ] })
      ] })
    ] })
  ] });
};
class Ak extends HTMLElement {
  constructor() {
    super(...arguments);
    Ho(this, "_root");
    Ho(this, "_hass");
    Ho(this, "_panel");
  }
  connectedCallback() {
    this._root || (this._root = Ws.createRoot(this)), this._render();
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
      /* @__PURE__ */ _.jsx(kt.StrictMode, { children: /* @__PURE__ */ _.jsx(Lk, { hass: this._hass, config_entry_id: this._panel.config.config_entry_id }) })
    );
  }
}
customElements.define("meraki-panel", Ak);
