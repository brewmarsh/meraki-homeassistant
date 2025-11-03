function g0(e, t) {
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
function Md(e) {
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
var Nd = { exports: {} }, ll = {}, Id = { exports: {} }, b = {};
/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var zo = Symbol.for("react.element"), y0 = Symbol.for("react.portal"), v0 = Symbol.for("react.fragment"), x0 = Symbol.for("react.strict_mode"), S0 = Symbol.for("react.profiler"), w0 = Symbol.for("react.provider"), C0 = Symbol.for("react.context"), k0 = Symbol.for("react.forward_ref"), E0 = Symbol.for("react.suspense"), _0 = Symbol.for("react.memo"), $0 = Symbol.for("react.lazy"), kc = Symbol.iterator;
function P0(e) {
  return e === null || typeof e != "object" ? null : (e = kc && e[kc] || e["@@iterator"], typeof e == "function" ? e : null);
}
var Ld = { isMounted: function() {
  return !1;
}, enqueueForceUpdate: function() {
}, enqueueReplaceState: function() {
}, enqueueSetState: function() {
} }, zd = Object.assign, jd = {};
function Tr(e, t, n) {
  this.props = e, this.context = t, this.refs = jd, this.updater = n || Ld;
}
Tr.prototype.isReactComponent = {};
Tr.prototype.setState = function(e, t) {
  if (typeof e != "object" && typeof e != "function" && e != null)
    throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
  this.updater.enqueueSetState(this, e, t, "setState");
};
Tr.prototype.forceUpdate = function(e) {
  this.updater.enqueueForceUpdate(this, e, "forceUpdate");
};
function Ad() {
}
Ad.prototype = Tr.prototype;
function Za(e, t, n) {
  this.props = e, this.context = t, this.refs = jd, this.updater = n || Ld;
}
var qa = Za.prototype = new Ad();
qa.constructor = Za;
zd(qa, Tr.prototype);
qa.isPureReactComponent = !0;
var Ec = Array.isArray, bd = Object.prototype.hasOwnProperty, Ja = { current: null }, Dd = { key: !0, ref: !0, __self: !0, __source: !0 };
function Fd(e, t, n) {
  var r, o = {}, i = null, l = null;
  if (t != null)
    for (r in t.ref !== void 0 && (l = t.ref), t.key !== void 0 && (i = "" + t.key), t)
      bd.call(t, r) && !Dd.hasOwnProperty(r) && (o[r] = t[r]);
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
  return { $$typeof: zo, type: e, key: i, ref: l, props: o, _owner: Ja.current };
}
function T0(e, t) {
  return { $$typeof: zo, type: e.type, key: t, ref: e.ref, props: e.props, _owner: e._owner };
}
function eu(e) {
  return typeof e == "object" && e !== null && e.$$typeof === zo;
}
function R0(e) {
  var t = { "=": "=0", ":": "=2" };
  return "$" + e.replace(/[=:]/g, function(n) {
    return t[n];
  });
}
var _c = /\/+/g;
function us(e, t) {
  return typeof e == "object" && e !== null && e.key != null ? R0("" + e.key) : t.toString(36);
}
function mi(e, t, n, r, o) {
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
          case zo:
          case y0:
            l = !0;
        }
    }
  if (l)
    return l = e, o = o(l), e = r === "" ? "." + us(l, 0) : r, Ec(o) ? (n = "", e != null && (n = e.replace(_c, "$&/") + "/"), mi(o, t, n, "", function(u) {
      return u;
    })) : o != null && (eu(o) && (o = T0(o, n + (!o.key || l && l.key === o.key ? "" : ("" + o.key).replace(_c, "$&/") + "/") + e)), t.push(o)), 1;
  if (l = 0, r = r === "" ? "." : r + ":", Ec(e))
    for (var s = 0; s < e.length; s++) {
      i = e[s];
      var a = r + us(i, s);
      l += mi(i, t, n, a, o);
    }
  else if (a = P0(e), typeof a == "function")
    for (e = a.call(e), s = 0; !(i = e.next()).done; )
      i = i.value, a = r + us(i, s++), l += mi(i, t, n, a, o);
  else if (i === "object")
    throw t = String(e), Error("Objects are not valid as a React child (found: " + (t === "[object Object]" ? "object with keys {" + Object.keys(e).join(", ") + "}" : t) + "). If you meant to render a collection of children, use an array instead.");
  return l;
}
function Qo(e, t, n) {
  if (e == null)
    return e;
  var r = [], o = 0;
  return mi(e, r, "", "", function(i) {
    return t.call(n, i, o++);
  }), r;
}
function O0(e) {
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
var Ue = { current: null }, hi = { transition: null }, M0 = { ReactCurrentDispatcher: Ue, ReactCurrentBatchConfig: hi, ReactCurrentOwner: Ja };
function Bd() {
  throw Error("act(...) is not supported in production builds of React.");
}
b.Children = { map: Qo, forEach: function(e, t, n) {
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
  if (!eu(e))
    throw Error("React.Children.only expected to receive a single React element child.");
  return e;
} };
b.Component = Tr;
b.Fragment = v0;
b.Profiler = S0;
b.PureComponent = Za;
b.StrictMode = x0;
b.Suspense = E0;
b.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = M0;
b.act = Bd;
b.cloneElement = function(e, t, n) {
  if (e == null)
    throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + e + ".");
  var r = zd({}, e.props), o = e.key, i = e.ref, l = e._owner;
  if (t != null) {
    if (t.ref !== void 0 && (i = t.ref, l = Ja.current), t.key !== void 0 && (o = "" + t.key), e.type && e.type.defaultProps)
      var s = e.type.defaultProps;
    for (a in t)
      bd.call(t, a) && !Dd.hasOwnProperty(a) && (r[a] = t[a] === void 0 && s !== void 0 ? s[a] : t[a]);
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
  return { $$typeof: zo, type: e.type, key: o, ref: i, props: r, _owner: l };
};
b.createContext = function(e) {
  return e = { $$typeof: C0, _currentValue: e, _currentValue2: e, _threadCount: 0, Provider: null, Consumer: null, _defaultValue: null, _globalName: null }, e.Provider = { $$typeof: w0, _context: e }, e.Consumer = e;
};
b.createElement = Fd;
b.createFactory = function(e) {
  var t = Fd.bind(null, e);
  return t.type = e, t;
};
b.createRef = function() {
  return { current: null };
};
b.forwardRef = function(e) {
  return { $$typeof: k0, render: e };
};
b.isValidElement = eu;
b.lazy = function(e) {
  return { $$typeof: $0, _payload: { _status: -1, _result: e }, _init: O0 };
};
b.memo = function(e, t) {
  return { $$typeof: _0, type: e, compare: t === void 0 ? null : t };
};
b.startTransition = function(e) {
  var t = hi.transition;
  hi.transition = {};
  try {
    e();
  } finally {
    hi.transition = t;
  }
};
b.unstable_act = Bd;
b.useCallback = function(e, t) {
  return Ue.current.useCallback(e, t);
};
b.useContext = function(e) {
  return Ue.current.useContext(e);
};
b.useDebugValue = function() {
};
b.useDeferredValue = function(e) {
  return Ue.current.useDeferredValue(e);
};
b.useEffect = function(e, t) {
  return Ue.current.useEffect(e, t);
};
b.useId = function() {
  return Ue.current.useId();
};
b.useImperativeHandle = function(e, t, n) {
  return Ue.current.useImperativeHandle(e, t, n);
};
b.useInsertionEffect = function(e, t) {
  return Ue.current.useInsertionEffect(e, t);
};
b.useLayoutEffect = function(e, t) {
  return Ue.current.useLayoutEffect(e, t);
};
b.useMemo = function(e, t) {
  return Ue.current.useMemo(e, t);
};
b.useReducer = function(e, t, n) {
  return Ue.current.useReducer(e, t, n);
};
b.useRef = function(e) {
  return Ue.current.useRef(e);
};
b.useState = function(e) {
  return Ue.current.useState(e);
};
b.useSyncExternalStore = function(e, t, n) {
  return Ue.current.useSyncExternalStore(e, t, n);
};
b.useTransition = function() {
  return Ue.current.useTransition();
};
b.version = "18.3.1";
Id.exports = b;
var w = Id.exports;
const qe = /* @__PURE__ */ Md(w), Vs = /* @__PURE__ */ g0({
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
var N0 = w, I0 = Symbol.for("react.element"), L0 = Symbol.for("react.fragment"), z0 = Object.prototype.hasOwnProperty, j0 = N0.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, A0 = { key: !0, ref: !0, __self: !0, __source: !0 };
function Ud(e, t, n) {
  var r, o = {}, i = null, l = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (r in t)
    z0.call(t, r) && !A0.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps)
    for (r in t = e.defaultProps, t)
      o[r] === void 0 && (o[r] = t[r]);
  return { $$typeof: I0, type: e, key: i, ref: l, props: o, _owner: j0.current };
}
ll.Fragment = L0;
ll.jsx = Ud;
ll.jsxs = Ud;
Nd.exports = ll;
var k = Nd.exports, Hs = {}, Wd = { exports: {} }, rt = {}, Vd = { exports: {} }, Hd = {};
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
        var B = I - 1 >>> 1, ae = T[B];
        if (0 < o(ae, N))
          T[B] = N, T[I] = ae, I = B;
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
        for (var B = 0, ae = T.length, Zt = ae >>> 1; B < Zt; ) {
          var Pe = 2 * (B + 1) - 1, Tt = T[Pe], L = Pe + 1, xe = T[L];
          if (0 > o(Tt, I))
            L < ae && 0 > o(xe, Tt) ? (T[B] = xe, T[L] = I, B = L) : (T[B] = Tt, T[Pe] = I, B = Pe);
          else if (L < ae && 0 > o(xe, I))
            T[B] = xe, T[L] = I, B = L;
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
  var a = [], u = [], c = 1, d = null, p = 3, v = !1, y = !1, g = !1, $ = typeof setTimeout == "function" ? setTimeout : null, m = typeof clearTimeout == "function" ? clearTimeout : null, f = typeof setImmediate < "u" ? setImmediate : null;
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
        N !== null && de(x, N.startTime - T);
      }
  }
  function _(T, N) {
    y = !1, g && (g = !1, m(R), R = -1), v = !0;
    var I = p;
    try {
      for (h(N), d = n(a); d !== null && (!(d.expirationTime > N) || T && !D()); ) {
        var B = d.callback;
        if (typeof B == "function") {
          d.callback = null, p = d.priorityLevel;
          var ae = B(d.expirationTime <= N);
          N = e.unstable_now(), typeof ae == "function" ? d.callback = ae : d === n(a) && r(a), h(N);
        } else
          r(a);
        d = n(a);
      }
      if (d !== null)
        var Zt = !0;
      else {
        var Pe = n(u);
        Pe !== null && de(x, Pe.startTime - N), Zt = !1;
      }
      return Zt;
    } finally {
      d = null, p = I, v = !1;
    }
  }
  var E = !1, C = null, R = -1, z = 5, O = -1;
  function D() {
    return !(e.unstable_now() - O < z);
  }
  function F() {
    if (C !== null) {
      var T = e.unstable_now();
      O = T;
      var N = !0;
      try {
        N = C(!0, T);
      } finally {
        N ? A() : (E = !1, C = null);
      }
    } else
      E = !1;
  }
  var A;
  if (typeof f == "function")
    A = function() {
      f(F);
    };
  else if (typeof MessageChannel < "u") {
    var Y = new MessageChannel(), te = Y.port2;
    Y.port1.onmessage = F, A = function() {
      te.postMessage(null);
    };
  } else
    A = function() {
      $(F, 0);
    };
  function ge(T) {
    C = T, E || (E = !0, A());
  }
  function de(T, N) {
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
    return p;
  }, e.unstable_getFirstCallbackNode = function() {
    return n(a);
  }, e.unstable_next = function(T) {
    switch (p) {
      case 1:
      case 2:
      case 3:
        var N = 3;
        break;
      default:
        N = p;
    }
    var I = p;
    p = N;
    try {
      return T();
    } finally {
      p = I;
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
    var I = p;
    p = T;
    try {
      return N();
    } finally {
      p = I;
    }
  }, e.unstable_scheduleCallback = function(T, N, I) {
    var B = e.unstable_now();
    switch (typeof I == "object" && I !== null ? (I = I.delay, I = typeof I == "number" && 0 < I ? B + I : B) : I = B, T) {
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
    return ae = I + ae, T = { id: c++, callback: N, priorityLevel: T, startTime: I, expirationTime: ae, sortIndex: -1 }, I > B ? (T.sortIndex = I, t(u, T), n(a) === null && T === n(u) && (g ? (m(R), R = -1) : g = !0, de(x, I - B))) : (T.sortIndex = ae, t(a, T), y || v || (y = !0, ge(_))), T;
  }, e.unstable_shouldYield = D, e.unstable_wrapCallback = function(T) {
    var N = p;
    return function() {
      var I = p;
      p = N;
      try {
        return T.apply(this, arguments);
      } finally {
        p = I;
      }
    };
  };
})(Hd);
Vd.exports = Hd;
var b0 = Vd.exports;
/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var D0 = w, nt = b0;
function P(e) {
  for (var t = "https://reactjs.org/docs/error-decoder.html?invariant=" + e, n = 1; n < arguments.length; n++)
    t += "&args[]=" + encodeURIComponent(arguments[n]);
  return "Minified React error #" + e + "; visit " + t + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
}
var Gd = /* @__PURE__ */ new Set(), fo = {};
function jn(e, t) {
  gr(e, t), gr(e + "Capture", t);
}
function gr(e, t) {
  for (fo[e] = t, e = 0; e < t.length; e++)
    Gd.add(t[e]);
}
var Vt = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), Gs = Object.prototype.hasOwnProperty, F0 = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, $c = {}, Pc = {};
function B0(e) {
  return Gs.call(Pc, e) ? !0 : Gs.call($c, e) ? !1 : F0.test(e) ? Pc[e] = !0 : ($c[e] = !0, !1);
}
function U0(e, t, n, r) {
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
function W0(e, t, n, r) {
  if (t === null || typeof t > "u" || U0(e, t, n, r))
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
var Me = {};
"children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(e) {
  Me[e] = new We(e, 0, !1, e, null, !1, !1);
});
[["acceptCharset", "accept-charset"], ["className", "class"], ["htmlFor", "for"], ["httpEquiv", "http-equiv"]].forEach(function(e) {
  var t = e[0];
  Me[t] = new We(t, 1, !1, e[1], null, !1, !1);
});
["contentEditable", "draggable", "spellCheck", "value"].forEach(function(e) {
  Me[e] = new We(e, 2, !1, e.toLowerCase(), null, !1, !1);
});
["autoReverse", "externalResourcesRequired", "focusable", "preserveAlpha"].forEach(function(e) {
  Me[e] = new We(e, 2, !1, e, null, !1, !1);
});
"allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(e) {
  Me[e] = new We(e, 3, !1, e.toLowerCase(), null, !1, !1);
});
["checked", "multiple", "muted", "selected"].forEach(function(e) {
  Me[e] = new We(e, 3, !0, e, null, !1, !1);
});
["capture", "download"].forEach(function(e) {
  Me[e] = new We(e, 4, !1, e, null, !1, !1);
});
["cols", "rows", "size", "span"].forEach(function(e) {
  Me[e] = new We(e, 6, !1, e, null, !1, !1);
});
["rowSpan", "start"].forEach(function(e) {
  Me[e] = new We(e, 5, !1, e.toLowerCase(), null, !1, !1);
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
  Me[t] = new We(t, 1, !1, e, null, !1, !1);
});
"xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(e) {
  var t = e.replace(tu, nu);
  Me[t] = new We(t, 1, !1, e, "http://www.w3.org/1999/xlink", !1, !1);
});
["xml:base", "xml:lang", "xml:space"].forEach(function(e) {
  var t = e.replace(tu, nu);
  Me[t] = new We(t, 1, !1, e, "http://www.w3.org/XML/1998/namespace", !1, !1);
});
["tabIndex", "crossOrigin"].forEach(function(e) {
  Me[e] = new We(e, 1, !1, e.toLowerCase(), null, !1, !1);
});
Me.xlinkHref = new We("xlinkHref", 1, !1, "xlink:href", "http://www.w3.org/1999/xlink", !0, !1);
["src", "href", "action", "formAction"].forEach(function(e) {
  Me[e] = new We(e, 1, !1, e.toLowerCase(), null, !0, !0);
});
function ru(e, t, n, r) {
  var o = Me.hasOwnProperty(t) ? Me[t] : null;
  (o !== null ? o.type !== 0 : r || !(2 < t.length) || t[0] !== "o" && t[0] !== "O" || t[1] !== "n" && t[1] !== "N") && (W0(t, n, o, r) && (n = null), r || o === null ? B0(t) && (n === null ? e.removeAttribute(t) : e.setAttribute(t, "" + n)) : o.mustUseProperty ? e[o.propertyName] = n === null ? o.type === 3 ? !1 : "" : n : (t = o.attributeName, r = o.attributeNamespace, n === null ? e.removeAttribute(t) : (o = o.type, n = o === 3 || o === 4 && n === !0 ? "" : "" + n, r ? e.setAttributeNS(r, t, n) : e.setAttribute(t, n))));
}
var Yt = D0.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, Yo = Symbol.for("react.element"), Qn = Symbol.for("react.portal"), Yn = Symbol.for("react.fragment"), ou = Symbol.for("react.strict_mode"), Ks = Symbol.for("react.profiler"), Kd = Symbol.for("react.provider"), Qd = Symbol.for("react.context"), iu = Symbol.for("react.forward_ref"), Qs = Symbol.for("react.suspense"), Ys = Symbol.for("react.suspense_list"), lu = Symbol.for("react.memo"), en = Symbol.for("react.lazy"), Yd = Symbol.for("react.offscreen"), Tc = Symbol.iterator;
function br(e) {
  return e === null || typeof e != "object" ? null : (e = Tc && e[Tc] || e["@@iterator"], typeof e == "function" ? e : null);
}
var se = Object.assign, cs;
function Yr(e) {
  if (cs === void 0)
    try {
      throw Error();
    } catch (n) {
      var t = n.stack.trim().match(/\n( *(at )?)/);
      cs = t && t[1] || "";
    }
  return `
` + cs + e;
}
var fs = !1;
function ds(e, t) {
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
  return (e = e ? e.displayName || e.name : "") ? Yr(e) : "";
}
function V0(e) {
  switch (e.tag) {
    case 5:
      return Yr(e.type);
    case 16:
      return Yr("Lazy");
    case 13:
      return Yr("Suspense");
    case 19:
      return Yr("SuspenseList");
    case 0:
    case 2:
    case 15:
      return e = ds(e.type, !1), e;
    case 11:
      return e = ds(e.type.render, !1), e;
    case 1:
      return e = ds(e.type, !0), e;
    default:
      return "";
  }
}
function Xs(e) {
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
    case Ks:
      return "Profiler";
    case ou:
      return "StrictMode";
    case Qs:
      return "Suspense";
    case Ys:
      return "SuspenseList";
  }
  if (typeof e == "object")
    switch (e.$$typeof) {
      case Qd:
        return (e.displayName || "Context") + ".Consumer";
      case Kd:
        return (e._context.displayName || "Context") + ".Provider";
      case iu:
        var t = e.render;
        return e = e.displayName, e || (e = t.displayName || t.name || "", e = e !== "" ? "ForwardRef(" + e + ")" : "ForwardRef"), e;
      case lu:
        return t = e.displayName || null, t !== null ? t : Xs(e.type) || "Memo";
      case en:
        t = e._payload, e = e._init;
        try {
          return Xs(e(t));
        } catch {
        }
    }
  return null;
}
function H0(e) {
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
      return Xs(t);
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
function Xd(e) {
  var t = e.type;
  return (e = e.nodeName) && e.toLowerCase() === "input" && (t === "checkbox" || t === "radio");
}
function G0(e) {
  var t = Xd(e) ? "checked" : "value", n = Object.getOwnPropertyDescriptor(e.constructor.prototype, t), r = "" + e[t];
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
  e._valueTracker || (e._valueTracker = G0(e));
}
function Zd(e) {
  if (!e)
    return !1;
  var t = e._valueTracker;
  if (!t)
    return !0;
  var n = t.getValue(), r = "";
  return e && (r = Xd(e) ? e.checked ? "true" : "false" : e.value), e = r, e !== n ? (t.setValue(e), !0) : !1;
}
function Mi(e) {
  if (e = e || (typeof document < "u" ? document : void 0), typeof e > "u")
    return null;
  try {
    return e.activeElement || e.body;
  } catch {
    return e.body;
  }
}
function Zs(e, t) {
  var n = t.checked;
  return se({}, t, { defaultChecked: void 0, defaultValue: void 0, value: void 0, checked: n ?? e._wrapperState.initialChecked });
}
function Rc(e, t) {
  var n = t.defaultValue == null ? "" : t.defaultValue, r = t.checked != null ? t.checked : t.defaultChecked;
  n = gn(t.value != null ? t.value : n), e._wrapperState = { initialChecked: r, initialValue: n, controlled: t.type === "checkbox" || t.type === "radio" ? t.checked != null : t.value != null };
}
function qd(e, t) {
  t = t.checked, t != null && ru(e, "checked", t, !1);
}
function qs(e, t) {
  qd(e, t);
  var n = gn(t.value), r = t.type;
  if (n != null)
    r === "number" ? (n === 0 && e.value === "" || e.value != n) && (e.value = "" + n) : e.value !== "" + n && (e.value = "" + n);
  else if (r === "submit" || r === "reset") {
    e.removeAttribute("value");
    return;
  }
  t.hasOwnProperty("value") ? Js(e, t.type, n) : t.hasOwnProperty("defaultValue") && Js(e, t.type, gn(t.defaultValue)), t.checked == null && t.defaultChecked != null && (e.defaultChecked = !!t.defaultChecked);
}
function Oc(e, t, n) {
  if (t.hasOwnProperty("value") || t.hasOwnProperty("defaultValue")) {
    var r = t.type;
    if (!(r !== "submit" && r !== "reset" || t.value !== void 0 && t.value !== null))
      return;
    t = "" + e._wrapperState.initialValue, n || t === e.value || (e.value = t), e.defaultValue = t;
  }
  n = e.name, n !== "" && (e.name = ""), e.defaultChecked = !!e._wrapperState.initialChecked, n !== "" && (e.name = n);
}
function Js(e, t, n) {
  (t !== "number" || Mi(e.ownerDocument) !== e) && (n == null ? e.defaultValue = "" + e._wrapperState.initialValue : e.defaultValue !== "" + n && (e.defaultValue = "" + n));
}
var Xr = Array.isArray;
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
function ea(e, t) {
  if (t.dangerouslySetInnerHTML != null)
    throw Error(P(91));
  return se({}, t, { value: void 0, defaultValue: void 0, children: "" + e._wrapperState.initialValue });
}
function Mc(e, t) {
  var n = t.value;
  if (n == null) {
    if (n = t.children, t = t.defaultValue, n != null) {
      if (t != null)
        throw Error(P(92));
      if (Xr(n)) {
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
function Jd(e, t) {
  var n = gn(t.value), r = gn(t.defaultValue);
  n != null && (n = "" + n, n !== e.value && (e.value = n), t.defaultValue == null && e.defaultValue !== n && (e.defaultValue = n)), r != null && (e.defaultValue = "" + r);
}
function Nc(e) {
  var t = e.textContent;
  t === e._wrapperState.initialValue && t !== "" && t !== null && (e.value = t);
}
function ep(e) {
  switch (e) {
    case "svg":
      return "http://www.w3.org/2000/svg";
    case "math":
      return "http://www.w3.org/1998/Math/MathML";
    default:
      return "http://www.w3.org/1999/xhtml";
  }
}
function ta(e, t) {
  return e == null || e === "http://www.w3.org/1999/xhtml" ? ep(t) : e === "http://www.w3.org/2000/svg" && t === "foreignObject" ? "http://www.w3.org/1999/xhtml" : e;
}
var Zo, tp = function(e) {
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
function po(e, t) {
  if (t) {
    var n = e.firstChild;
    if (n && n === e.lastChild && n.nodeType === 3) {
      n.nodeValue = t;
      return;
    }
  }
  e.textContent = t;
}
var to = {
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
}, K0 = ["Webkit", "ms", "Moz", "O"];
Object.keys(to).forEach(function(e) {
  K0.forEach(function(t) {
    t = t + e.charAt(0).toUpperCase() + e.substring(1), to[t] = to[e];
  });
});
function np(e, t, n) {
  return t == null || typeof t == "boolean" || t === "" ? "" : n || typeof t != "number" || t === 0 || to.hasOwnProperty(e) && to[e] ? ("" + t).trim() : t + "px";
}
function rp(e, t) {
  e = e.style;
  for (var n in t)
    if (t.hasOwnProperty(n)) {
      var r = n.indexOf("--") === 0, o = np(n, t[n], r);
      n === "float" && (n = "cssFloat"), r ? e.setProperty(n, o) : e[n] = o;
    }
}
var Q0 = se({ menuitem: !0 }, { area: !0, base: !0, br: !0, col: !0, embed: !0, hr: !0, img: !0, input: !0, keygen: !0, link: !0, meta: !0, param: !0, source: !0, track: !0, wbr: !0 });
function na(e, t) {
  if (t) {
    if (Q0[e] && (t.children != null || t.dangerouslySetInnerHTML != null))
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
function ra(e, t) {
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
var oa = null;
function su(e) {
  return e = e.target || e.srcElement || window, e.correspondingUseElement && (e = e.correspondingUseElement), e.nodeType === 3 ? e.parentNode : e;
}
var ia = null, sr = null, ar = null;
function Ic(e) {
  if (e = bo(e)) {
    if (typeof ia != "function")
      throw Error(P(280));
    var t = e.stateNode;
    t && (t = fl(t), ia(e.stateNode, e.type, t));
  }
}
function op(e) {
  sr ? ar ? ar.push(e) : ar = [e] : sr = e;
}
function ip() {
  if (sr) {
    var e = sr, t = ar;
    if (ar = sr = null, Ic(e), t)
      for (e = 0; e < t.length; e++)
        Ic(t[e]);
  }
}
function lp(e, t) {
  return e(t);
}
function sp() {
}
var ps = !1;
function ap(e, t, n) {
  if (ps)
    return e(t, n);
  ps = !0;
  try {
    return lp(e, t, n);
  } finally {
    ps = !1, (sr !== null || ar !== null) && (sp(), ip());
  }
}
function mo(e, t) {
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
var la = !1;
if (Vt)
  try {
    var Dr = {};
    Object.defineProperty(Dr, "passive", { get: function() {
      la = !0;
    } }), window.addEventListener("test", Dr, Dr), window.removeEventListener("test", Dr, Dr);
  } catch {
    la = !1;
  }
function Y0(e, t, n, r, o, i, l, s, a) {
  var u = Array.prototype.slice.call(arguments, 3);
  try {
    t.apply(n, u);
  } catch (c) {
    this.onError(c);
  }
}
var no = !1, Ni = null, Ii = !1, sa = null, X0 = { onError: function(e) {
  no = !0, Ni = e;
} };
function Z0(e, t, n, r, o, i, l, s, a) {
  no = !1, Ni = null, Y0.apply(X0, arguments);
}
function q0(e, t, n, r, o, i, l, s, a) {
  if (Z0.apply(this, arguments), no) {
    if (no) {
      var u = Ni;
      no = !1, Ni = null;
    } else
      throw Error(P(198));
    Ii || (Ii = !0, sa = u);
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
function up(e) {
  if (e.tag === 13) {
    var t = e.memoizedState;
    if (t === null && (e = e.alternate, e !== null && (t = e.memoizedState)), t !== null)
      return t.dehydrated;
  }
  return null;
}
function Lc(e) {
  if (An(e) !== e)
    throw Error(P(188));
}
function J0(e) {
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
          return Lc(o), e;
        if (i === r)
          return Lc(o), t;
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
function cp(e) {
  return e = J0(e), e !== null ? fp(e) : null;
}
function fp(e) {
  if (e.tag === 5 || e.tag === 6)
    return e;
  for (e = e.child; e !== null; ) {
    var t = fp(e);
    if (t !== null)
      return t;
    e = e.sibling;
  }
  return null;
}
var dp = nt.unstable_scheduleCallback, zc = nt.unstable_cancelCallback, eg = nt.unstable_shouldYield, tg = nt.unstable_requestPaint, pe = nt.unstable_now, ng = nt.unstable_getCurrentPriorityLevel, au = nt.unstable_ImmediatePriority, pp = nt.unstable_UserBlockingPriority, Li = nt.unstable_NormalPriority, rg = nt.unstable_LowPriority, mp = nt.unstable_IdlePriority, sl = null, Lt = null;
function og(e) {
  if (Lt && typeof Lt.onCommitFiberRoot == "function")
    try {
      Lt.onCommitFiberRoot(sl, e, void 0, (e.current.flags & 128) === 128);
    } catch {
    }
}
var _t = Math.clz32 ? Math.clz32 : sg, ig = Math.log, lg = Math.LN2;
function sg(e) {
  return e >>>= 0, e === 0 ? 32 : 31 - (ig(e) / lg | 0) | 0;
}
var qo = 64, Jo = 4194304;
function Zr(e) {
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
    s !== 0 ? r = Zr(s) : (i &= l, i !== 0 && (r = Zr(i)));
  } else
    l = n & ~o, l !== 0 ? r = Zr(l) : i !== 0 && (r = Zr(i));
  if (r === 0)
    return 0;
  if (t !== 0 && t !== r && !(t & o) && (o = r & -r, i = t & -t, o >= i || o === 16 && (i & 4194240) !== 0))
    return t;
  if (r & 4 && (r |= n & 16), t = e.entangledLanes, t !== 0)
    for (e = e.entanglements, t &= r; 0 < t; )
      n = 31 - _t(t), o = 1 << n, r |= e[n], t &= ~o;
  return r;
}
function ag(e, t) {
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
function ug(e, t) {
  for (var n = e.suspendedLanes, r = e.pingedLanes, o = e.expirationTimes, i = e.pendingLanes; 0 < i; ) {
    var l = 31 - _t(i), s = 1 << l, a = o[l];
    a === -1 ? (!(s & n) || s & r) && (o[l] = ag(s, t)) : a <= t && (e.expiredLanes |= s), i &= ~s;
  }
}
function aa(e) {
  return e = e.pendingLanes & -1073741825, e !== 0 ? e : e & 1073741824 ? 1073741824 : 0;
}
function hp() {
  var e = qo;
  return qo <<= 1, !(qo & 4194240) && (qo = 64), e;
}
function ms(e) {
  for (var t = [], n = 0; 31 > n; n++)
    t.push(e);
  return t;
}
function jo(e, t, n) {
  e.pendingLanes |= t, t !== 536870912 && (e.suspendedLanes = 0, e.pingedLanes = 0), e = e.eventTimes, t = 31 - _t(t), e[t] = n;
}
function cg(e, t) {
  var n = e.pendingLanes & ~t;
  e.pendingLanes = t, e.suspendedLanes = 0, e.pingedLanes = 0, e.expiredLanes &= t, e.mutableReadLanes &= t, e.entangledLanes &= t, t = e.entanglements;
  var r = e.eventTimes;
  for (e = e.expirationTimes; 0 < n; ) {
    var o = 31 - _t(n), i = 1 << o;
    t[o] = 0, r[o] = -1, e[o] = -1, n &= ~i;
  }
}
function uu(e, t) {
  var n = e.entangledLanes |= t;
  for (e = e.entanglements; n; ) {
    var r = 31 - _t(n), o = 1 << r;
    o & t | e[r] & t && (e[r] |= t), n &= ~o;
  }
}
var K = 0;
function gp(e) {
  return e &= -e, 1 < e ? 4 < e ? e & 268435455 ? 16 : 536870912 : 4 : 1;
}
var yp, cu, vp, xp, Sp, ua = !1, ei = [], an = null, un = null, cn = null, ho = /* @__PURE__ */ new Map(), go = /* @__PURE__ */ new Map(), nn = [], fg = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
function jc(e, t) {
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
      ho.delete(t.pointerId);
      break;
    case "gotpointercapture":
    case "lostpointercapture":
      go.delete(t.pointerId);
  }
}
function Fr(e, t, n, r, o, i) {
  return e === null || e.nativeEvent !== i ? (e = { blockedOn: t, domEventName: n, eventSystemFlags: r, nativeEvent: i, targetContainers: [o] }, t !== null && (t = bo(t), t !== null && cu(t)), e) : (e.eventSystemFlags |= r, t = e.targetContainers, o !== null && t.indexOf(o) === -1 && t.push(o), e);
}
function dg(e, t, n, r, o) {
  switch (t) {
    case "focusin":
      return an = Fr(an, e, t, n, r, o), !0;
    case "dragenter":
      return un = Fr(un, e, t, n, r, o), !0;
    case "mouseover":
      return cn = Fr(cn, e, t, n, r, o), !0;
    case "pointerover":
      var i = o.pointerId;
      return ho.set(i, Fr(ho.get(i) || null, e, t, n, r, o)), !0;
    case "gotpointercapture":
      return i = o.pointerId, go.set(i, Fr(go.get(i) || null, e, t, n, r, o)), !0;
  }
  return !1;
}
function wp(e) {
  var t = _n(e.target);
  if (t !== null) {
    var n = An(t);
    if (n !== null) {
      if (t = n.tag, t === 13) {
        if (t = up(n), t !== null) {
          e.blockedOn = t, Sp(e.priority, function() {
            vp(n);
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
function gi(e) {
  if (e.blockedOn !== null)
    return !1;
  for (var t = e.targetContainers; 0 < t.length; ) {
    var n = ca(e.domEventName, e.eventSystemFlags, t[0], e.nativeEvent);
    if (n === null) {
      n = e.nativeEvent;
      var r = new n.constructor(n.type, n);
      oa = r, n.target.dispatchEvent(r), oa = null;
    } else
      return t = bo(n), t !== null && cu(t), e.blockedOn = n, !1;
    t.shift();
  }
  return !0;
}
function Ac(e, t, n) {
  gi(e) && n.delete(t);
}
function pg() {
  ua = !1, an !== null && gi(an) && (an = null), un !== null && gi(un) && (un = null), cn !== null && gi(cn) && (cn = null), ho.forEach(Ac), go.forEach(Ac);
}
function Br(e, t) {
  e.blockedOn === t && (e.blockedOn = null, ua || (ua = !0, nt.unstable_scheduleCallback(nt.unstable_NormalPriority, pg)));
}
function yo(e) {
  function t(o) {
    return Br(o, e);
  }
  if (0 < ei.length) {
    Br(ei[0], e);
    for (var n = 1; n < ei.length; n++) {
      var r = ei[n];
      r.blockedOn === e && (r.blockedOn = null);
    }
  }
  for (an !== null && Br(an, e), un !== null && Br(un, e), cn !== null && Br(cn, e), ho.forEach(t), go.forEach(t), n = 0; n < nn.length; n++)
    r = nn[n], r.blockedOn === e && (r.blockedOn = null);
  for (; 0 < nn.length && (n = nn[0], n.blockedOn === null); )
    wp(n), n.blockedOn === null && nn.shift();
}
var ur = Yt.ReactCurrentBatchConfig, ji = !0;
function mg(e, t, n, r) {
  var o = K, i = ur.transition;
  ur.transition = null;
  try {
    K = 1, fu(e, t, n, r);
  } finally {
    K = o, ur.transition = i;
  }
}
function hg(e, t, n, r) {
  var o = K, i = ur.transition;
  ur.transition = null;
  try {
    K = 4, fu(e, t, n, r);
  } finally {
    K = o, ur.transition = i;
  }
}
function fu(e, t, n, r) {
  if (ji) {
    var o = ca(e, t, n, r);
    if (o === null)
      Es(e, t, r, Ai, n), jc(e, r);
    else if (dg(o, e, t, n, r))
      r.stopPropagation();
    else if (jc(e, r), t & 4 && -1 < fg.indexOf(e)) {
      for (; o !== null; ) {
        var i = bo(o);
        if (i !== null && yp(i), i = ca(e, t, n, r), i === null && Es(e, t, r, Ai, n), i === o)
          break;
        o = i;
      }
      o !== null && r.stopPropagation();
    } else
      Es(e, t, r, null, n);
  }
}
var Ai = null;
function ca(e, t, n, r) {
  if (Ai = null, e = su(r), e = _n(e), e !== null)
    if (t = An(e), t === null)
      e = null;
    else if (n = t.tag, n === 13) {
      if (e = up(t), e !== null)
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
      switch (ng()) {
        case au:
          return 1;
        case pp:
          return 4;
        case Li:
        case rg:
          return 16;
        case mp:
          return 536870912;
        default:
          return 16;
      }
    default:
      return 16;
  }
}
var ln = null, du = null, yi = null;
function kp() {
  if (yi)
    return yi;
  var e, t = du, n = t.length, r, o = "value" in ln ? ln.value : ln.textContent, i = o.length;
  for (e = 0; e < n && t[e] === o[e]; e++)
    ;
  var l = n - e;
  for (r = 1; r <= l && t[n - r] === o[i - r]; r++)
    ;
  return yi = o.slice(e, 1 < r ? 1 - r : void 0);
}
function vi(e) {
  var t = e.keyCode;
  return "charCode" in e ? (e = e.charCode, e === 0 && t === 13 && (e = 13)) : e = t, e === 10 && (e = 13), 32 <= e || e === 13 ? e : 0;
}
function ti() {
  return !0;
}
function bc() {
  return !1;
}
function ot(e) {
  function t(n, r, o, i, l) {
    this._reactName = n, this._targetInst = o, this.type = r, this.nativeEvent = i, this.target = l, this.currentTarget = null;
    for (var s in e)
      e.hasOwnProperty(s) && (n = e[s], this[s] = n ? n(i) : i[s]);
    return this.isDefaultPrevented = (i.defaultPrevented != null ? i.defaultPrevented : i.returnValue === !1) ? ti : bc, this.isPropagationStopped = bc, this;
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
var Rr = { eventPhase: 0, bubbles: 0, cancelable: 0, timeStamp: function(e) {
  return e.timeStamp || Date.now();
}, defaultPrevented: 0, isTrusted: 0 }, pu = ot(Rr), Ao = se({}, Rr, { view: 0, detail: 0 }), gg = ot(Ao), hs, gs, Ur, al = se({}, Ao, { screenX: 0, screenY: 0, clientX: 0, clientY: 0, pageX: 0, pageY: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, getModifierState: mu, button: 0, buttons: 0, relatedTarget: function(e) {
  return e.relatedTarget === void 0 ? e.fromElement === e.srcElement ? e.toElement : e.fromElement : e.relatedTarget;
}, movementX: function(e) {
  return "movementX" in e ? e.movementX : (e !== Ur && (Ur && e.type === "mousemove" ? (hs = e.screenX - Ur.screenX, gs = e.screenY - Ur.screenY) : gs = hs = 0, Ur = e), hs);
}, movementY: function(e) {
  return "movementY" in e ? e.movementY : gs;
} }), Dc = ot(al), yg = se({}, al, { dataTransfer: 0 }), vg = ot(yg), xg = se({}, Ao, { relatedTarget: 0 }), ys = ot(xg), Sg = se({}, Rr, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }), wg = ot(Sg), Cg = se({}, Rr, { clipboardData: function(e) {
  return "clipboardData" in e ? e.clipboardData : window.clipboardData;
} }), kg = ot(Cg), Eg = se({}, Rr, { data: 0 }), Fc = ot(Eg), _g = {
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
}, $g = {
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
}, Pg = { Alt: "altKey", Control: "ctrlKey", Meta: "metaKey", Shift: "shiftKey" };
function Tg(e) {
  var t = this.nativeEvent;
  return t.getModifierState ? t.getModifierState(e) : (e = Pg[e]) ? !!t[e] : !1;
}
function mu() {
  return Tg;
}
var Rg = se({}, Ao, { key: function(e) {
  if (e.key) {
    var t = _g[e.key] || e.key;
    if (t !== "Unidentified")
      return t;
  }
  return e.type === "keypress" ? (e = vi(e), e === 13 ? "Enter" : String.fromCharCode(e)) : e.type === "keydown" || e.type === "keyup" ? $g[e.keyCode] || "Unidentified" : "";
}, code: 0, location: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, repeat: 0, locale: 0, getModifierState: mu, charCode: function(e) {
  return e.type === "keypress" ? vi(e) : 0;
}, keyCode: function(e) {
  return e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
}, which: function(e) {
  return e.type === "keypress" ? vi(e) : e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
} }), Og = ot(Rg), Mg = se({}, al, { pointerId: 0, width: 0, height: 0, pressure: 0, tangentialPressure: 0, tiltX: 0, tiltY: 0, twist: 0, pointerType: 0, isPrimary: 0 }), Bc = ot(Mg), Ng = se({}, Ao, { touches: 0, targetTouches: 0, changedTouches: 0, altKey: 0, metaKey: 0, ctrlKey: 0, shiftKey: 0, getModifierState: mu }), Ig = ot(Ng), Lg = se({}, Rr, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }), zg = ot(Lg), jg = se({}, al, {
  deltaX: function(e) {
    return "deltaX" in e ? e.deltaX : "wheelDeltaX" in e ? -e.wheelDeltaX : 0;
  },
  deltaY: function(e) {
    return "deltaY" in e ? e.deltaY : "wheelDeltaY" in e ? -e.wheelDeltaY : "wheelDelta" in e ? -e.wheelDelta : 0;
  },
  deltaZ: 0,
  deltaMode: 0
}), Ag = ot(jg), bg = [9, 13, 27, 32], hu = Vt && "CompositionEvent" in window, ro = null;
Vt && "documentMode" in document && (ro = document.documentMode);
var Dg = Vt && "TextEvent" in window && !ro, Ep = Vt && (!hu || ro && 8 < ro && 11 >= ro), Uc = String.fromCharCode(32), Wc = !1;
function _p(e, t) {
  switch (e) {
    case "keyup":
      return bg.indexOf(t.keyCode) !== -1;
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
function $p(e) {
  return e = e.detail, typeof e == "object" && "data" in e ? e.data : null;
}
var Xn = !1;
function Fg(e, t) {
  switch (e) {
    case "compositionend":
      return $p(t);
    case "keypress":
      return t.which !== 32 ? null : (Wc = !0, Uc);
    case "textInput":
      return e = t.data, e === Uc && Wc ? null : e;
    default:
      return null;
  }
}
function Bg(e, t) {
  if (Xn)
    return e === "compositionend" || !hu && _p(e, t) ? (e = kp(), yi = du = ln = null, Xn = !1, e) : null;
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
      return Ep && t.locale !== "ko" ? null : t.data;
    default:
      return null;
  }
}
var Ug = { color: !0, date: !0, datetime: !0, "datetime-local": !0, email: !0, month: !0, number: !0, password: !0, range: !0, search: !0, tel: !0, text: !0, time: !0, url: !0, week: !0 };
function Vc(e) {
  var t = e && e.nodeName && e.nodeName.toLowerCase();
  return t === "input" ? !!Ug[e.type] : t === "textarea";
}
function Pp(e, t, n, r) {
  op(r), t = bi(t, "onChange"), 0 < t.length && (n = new pu("onChange", "change", null, n, r), e.push({ event: n, listeners: t }));
}
var oo = null, vo = null;
function Wg(e) {
  bp(e, 0);
}
function ul(e) {
  var t = Jn(e);
  if (Zd(t))
    return e;
}
function Vg(e, t) {
  if (e === "change")
    return t;
}
var Tp = !1;
if (Vt) {
  var vs;
  if (Vt) {
    var xs = "oninput" in document;
    if (!xs) {
      var Hc = document.createElement("div");
      Hc.setAttribute("oninput", "return;"), xs = typeof Hc.oninput == "function";
    }
    vs = xs;
  } else
    vs = !1;
  Tp = vs && (!document.documentMode || 9 < document.documentMode);
}
function Gc() {
  oo && (oo.detachEvent("onpropertychange", Rp), vo = oo = null);
}
function Rp(e) {
  if (e.propertyName === "value" && ul(vo)) {
    var t = [];
    Pp(t, vo, e, su(e)), ap(Wg, t);
  }
}
function Hg(e, t, n) {
  e === "focusin" ? (Gc(), oo = t, vo = n, oo.attachEvent("onpropertychange", Rp)) : e === "focusout" && Gc();
}
function Gg(e) {
  if (e === "selectionchange" || e === "keyup" || e === "keydown")
    return ul(vo);
}
function Kg(e, t) {
  if (e === "click")
    return ul(t);
}
function Qg(e, t) {
  if (e === "input" || e === "change")
    return ul(t);
}
function Yg(e, t) {
  return e === t && (e !== 0 || 1 / e === 1 / t) || e !== e && t !== t;
}
var Pt = typeof Object.is == "function" ? Object.is : Yg;
function xo(e, t) {
  if (Pt(e, t))
    return !0;
  if (typeof e != "object" || e === null || typeof t != "object" || t === null)
    return !1;
  var n = Object.keys(e), r = Object.keys(t);
  if (n.length !== r.length)
    return !1;
  for (r = 0; r < n.length; r++) {
    var o = n[r];
    if (!Gs.call(t, o) || !Pt(e[o], t[o]))
      return !1;
  }
  return !0;
}
function Kc(e) {
  for (; e && e.firstChild; )
    e = e.firstChild;
  return e;
}
function Qc(e, t) {
  var n = Kc(e);
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
    n = Kc(n);
  }
}
function Op(e, t) {
  return e && t ? e === t ? !0 : e && e.nodeType === 3 ? !1 : t && t.nodeType === 3 ? Op(e, t.parentNode) : "contains" in e ? e.contains(t) : e.compareDocumentPosition ? !!(e.compareDocumentPosition(t) & 16) : !1 : !1;
}
function Mp() {
  for (var e = window, t = Mi(); t instanceof e.HTMLIFrameElement; ) {
    try {
      var n = typeof t.contentWindow.location.href == "string";
    } catch {
      n = !1;
    }
    if (n)
      e = t.contentWindow;
    else
      break;
    t = Mi(e.document);
  }
  return t;
}
function gu(e) {
  var t = e && e.nodeName && e.nodeName.toLowerCase();
  return t && (t === "input" && (e.type === "text" || e.type === "search" || e.type === "tel" || e.type === "url" || e.type === "password") || t === "textarea" || e.contentEditable === "true");
}
function Xg(e) {
  var t = Mp(), n = e.focusedElem, r = e.selectionRange;
  if (t !== n && n && n.ownerDocument && Op(n.ownerDocument.documentElement, n)) {
    if (r !== null && gu(n)) {
      if (t = r.start, e = r.end, e === void 0 && (e = t), "selectionStart" in n)
        n.selectionStart = t, n.selectionEnd = Math.min(e, n.value.length);
      else if (e = (t = n.ownerDocument || document) && t.defaultView || window, e.getSelection) {
        e = e.getSelection();
        var o = n.textContent.length, i = Math.min(r.start, o);
        r = r.end === void 0 ? i : Math.min(r.end, o), !e.extend && i > r && (o = r, r = i, i = o), o = Qc(n, i);
        var l = Qc(
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
var Zg = Vt && "documentMode" in document && 11 >= document.documentMode, Zn = null, fa = null, io = null, da = !1;
function Yc(e, t, n) {
  var r = n.window === n ? n.document : n.nodeType === 9 ? n : n.ownerDocument;
  da || Zn == null || Zn !== Mi(r) || (r = Zn, "selectionStart" in r && gu(r) ? r = { start: r.selectionStart, end: r.selectionEnd } : (r = (r.ownerDocument && r.ownerDocument.defaultView || window).getSelection(), r = { anchorNode: r.anchorNode, anchorOffset: r.anchorOffset, focusNode: r.focusNode, focusOffset: r.focusOffset }), io && xo(io, r) || (io = r, r = bi(fa, "onSelect"), 0 < r.length && (t = new pu("onSelect", "select", null, t, n), e.push({ event: t, listeners: r }), t.target = Zn)));
}
function ni(e, t) {
  var n = {};
  return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit" + e] = "webkit" + t, n["Moz" + e] = "moz" + t, n;
}
var qn = { animationend: ni("Animation", "AnimationEnd"), animationiteration: ni("Animation", "AnimationIteration"), animationstart: ni("Animation", "AnimationStart"), transitionend: ni("Transition", "TransitionEnd") }, Ss = {}, Np = {};
Vt && (Np = document.createElement("div").style, "AnimationEvent" in window || (delete qn.animationend.animation, delete qn.animationiteration.animation, delete qn.animationstart.animation), "TransitionEvent" in window || delete qn.transitionend.transition);
function cl(e) {
  if (Ss[e])
    return Ss[e];
  if (!qn[e])
    return e;
  var t = qn[e], n;
  for (n in t)
    if (t.hasOwnProperty(n) && n in Np)
      return Ss[e] = t[n];
  return e;
}
var Ip = cl("animationend"), Lp = cl("animationiteration"), zp = cl("animationstart"), jp = cl("transitionend"), Ap = /* @__PURE__ */ new Map(), Xc = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
function vn(e, t) {
  Ap.set(e, t), jn(t, [e]);
}
for (var ws = 0; ws < Xc.length; ws++) {
  var Cs = Xc[ws], qg = Cs.toLowerCase(), Jg = Cs[0].toUpperCase() + Cs.slice(1);
  vn(qg, "on" + Jg);
}
vn(Ip, "onAnimationEnd");
vn(Lp, "onAnimationIteration");
vn(zp, "onAnimationStart");
vn("dblclick", "onDoubleClick");
vn("focusin", "onFocus");
vn("focusout", "onBlur");
vn(jp, "onTransitionEnd");
gr("onMouseEnter", ["mouseout", "mouseover"]);
gr("onMouseLeave", ["mouseout", "mouseover"]);
gr("onPointerEnter", ["pointerout", "pointerover"]);
gr("onPointerLeave", ["pointerout", "pointerover"]);
jn("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" "));
jn("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));
jn("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]);
jn("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" "));
jn("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" "));
jn("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
var qr = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), ey = new Set("cancel close invalid load scroll toggle".split(" ").concat(qr));
function Zc(e, t, n) {
  var r = e.type || "unknown-event";
  e.currentTarget = n, q0(r, t, void 0, e), e.currentTarget = null;
}
function bp(e, t) {
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
          Zc(o, s, u), i = a;
        }
      else
        for (l = 0; l < r.length; l++) {
          if (s = r[l], a = s.instance, u = s.currentTarget, s = s.listener, a !== i && o.isPropagationStopped())
            break e;
          Zc(o, s, u), i = a;
        }
    }
  }
  if (Ii)
    throw e = sa, Ii = !1, sa = null, e;
}
function J(e, t) {
  var n = t[ya];
  n === void 0 && (n = t[ya] = /* @__PURE__ */ new Set());
  var r = e + "__bubble";
  n.has(r) || (Dp(t, e, 2, !1), n.add(r));
}
function ks(e, t, n) {
  var r = 0;
  t && (r |= 4), Dp(n, e, r, t);
}
var ri = "_reactListening" + Math.random().toString(36).slice(2);
function So(e) {
  if (!e[ri]) {
    e[ri] = !0, Gd.forEach(function(n) {
      n !== "selectionchange" && (ey.has(n) || ks(n, !1, e), ks(n, !0, e));
    });
    var t = e.nodeType === 9 ? e : e.ownerDocument;
    t === null || t[ri] || (t[ri] = !0, ks("selectionchange", !1, t));
  }
}
function Dp(e, t, n, r) {
  switch (Cp(t)) {
    case 1:
      var o = mg;
      break;
    case 4:
      o = hg;
      break;
    default:
      o = fu;
  }
  n = o.bind(null, t, n, e), o = void 0, !la || t !== "touchstart" && t !== "touchmove" && t !== "wheel" || (o = !0), r ? o !== void 0 ? e.addEventListener(t, n, { capture: !0, passive: o }) : e.addEventListener(t, n, !0) : o !== void 0 ? e.addEventListener(t, n, { passive: o }) : e.addEventListener(t, n, !1);
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
  ap(function() {
    var u = i, c = su(n), d = [];
    e: {
      var p = Ap.get(e);
      if (p !== void 0) {
        var v = pu, y = e;
        switch (e) {
          case "keypress":
            if (vi(n) === 0)
              break e;
          case "keydown":
          case "keyup":
            v = Og;
            break;
          case "focusin":
            y = "focus", v = ys;
            break;
          case "focusout":
            y = "blur", v = ys;
            break;
          case "beforeblur":
          case "afterblur":
            v = ys;
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
            v = Dc;
            break;
          case "drag":
          case "dragend":
          case "dragenter":
          case "dragexit":
          case "dragleave":
          case "dragover":
          case "dragstart":
          case "drop":
            v = vg;
            break;
          case "touchcancel":
          case "touchend":
          case "touchmove":
          case "touchstart":
            v = Ig;
            break;
          case Ip:
          case Lp:
          case zp:
            v = wg;
            break;
          case jp:
            v = zg;
            break;
          case "scroll":
            v = gg;
            break;
          case "wheel":
            v = Ag;
            break;
          case "copy":
          case "cut":
          case "paste":
            v = kg;
            break;
          case "gotpointercapture":
          case "lostpointercapture":
          case "pointercancel":
          case "pointerdown":
          case "pointermove":
          case "pointerout":
          case "pointerover":
          case "pointerup":
            v = Bc;
        }
        var g = (t & 4) !== 0, $ = !g && e === "scroll", m = g ? p !== null ? p + "Capture" : null : p;
        g = [];
        for (var f = u, h; f !== null; ) {
          h = f;
          var x = h.stateNode;
          if (h.tag === 5 && x !== null && (h = x, m !== null && (x = mo(f, m), x != null && g.push(wo(f, x, h)))), $)
            break;
          f = f.return;
        }
        0 < g.length && (p = new v(p, y, null, n, c), d.push({ event: p, listeners: g }));
      }
    }
    if (!(t & 7)) {
      e: {
        if (p = e === "mouseover" || e === "pointerover", v = e === "mouseout" || e === "pointerout", p && n !== oa && (y = n.relatedTarget || n.fromElement) && (_n(y) || y[Ht]))
          break e;
        if ((v || p) && (p = c.window === c ? c : (p = c.ownerDocument) ? p.defaultView || p.parentWindow : window, v ? (y = n.relatedTarget || n.toElement, v = u, y = y ? _n(y) : null, y !== null && ($ = An(y), y !== $ || y.tag !== 5 && y.tag !== 6) && (y = null)) : (v = null, y = u), v !== y)) {
          if (g = Dc, x = "onMouseLeave", m = "onMouseEnter", f = "mouse", (e === "pointerout" || e === "pointerover") && (g = Bc, x = "onPointerLeave", m = "onPointerEnter", f = "pointer"), $ = v == null ? p : Jn(v), h = y == null ? p : Jn(y), p = new g(x, f + "leave", v, n, c), p.target = $, p.relatedTarget = h, x = null, _n(c) === u && (g = new g(m, f + "enter", y, n, c), g.target = h, g.relatedTarget = $, x = g), $ = x, v && y)
            t: {
              for (g = v, m = y, f = 0, h = g; h; h = Dn(h))
                f++;
              for (h = 0, x = m; x; x = Dn(x))
                h++;
              for (; 0 < f - h; )
                g = Dn(g), f--;
              for (; 0 < h - f; )
                m = Dn(m), h--;
              for (; f--; ) {
                if (g === m || m !== null && g === m.alternate)
                  break t;
                g = Dn(g), m = Dn(m);
              }
              g = null;
            }
          else
            g = null;
          v !== null && qc(d, p, v, g, !1), y !== null && $ !== null && qc(d, $, y, g, !0);
        }
      }
      e: {
        if (p = u ? Jn(u) : window, v = p.nodeName && p.nodeName.toLowerCase(), v === "select" || v === "input" && p.type === "file")
          var _ = Vg;
        else if (Vc(p))
          if (Tp)
            _ = Qg;
          else {
            _ = Gg;
            var E = Hg;
          }
        else
          (v = p.nodeName) && v.toLowerCase() === "input" && (p.type === "checkbox" || p.type === "radio") && (_ = Kg);
        if (_ && (_ = _(e, u))) {
          Pp(d, _, n, c);
          break e;
        }
        E && E(e, p, u), e === "focusout" && (E = p._wrapperState) && E.controlled && p.type === "number" && Js(p, "number", p.value);
      }
      switch (E = u ? Jn(u) : window, e) {
        case "focusin":
          (Vc(E) || E.contentEditable === "true") && (Zn = E, fa = u, io = null);
          break;
        case "focusout":
          io = fa = Zn = null;
          break;
        case "mousedown":
          da = !0;
          break;
        case "contextmenu":
        case "mouseup":
        case "dragend":
          da = !1, Yc(d, n, c);
          break;
        case "selectionchange":
          if (Zg)
            break;
        case "keydown":
        case "keyup":
          Yc(d, n, c);
      }
      var C;
      if (hu)
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
        Xn ? _p(e, n) && (R = "onCompositionEnd") : e === "keydown" && n.keyCode === 229 && (R = "onCompositionStart");
      R && (Ep && n.locale !== "ko" && (Xn || R !== "onCompositionStart" ? R === "onCompositionEnd" && Xn && (C = kp()) : (ln = c, du = "value" in ln ? ln.value : ln.textContent, Xn = !0)), E = bi(u, R), 0 < E.length && (R = new Fc(R, e, null, n, c), d.push({ event: R, listeners: E }), C ? R.data = C : (C = $p(n), C !== null && (R.data = C)))), (C = Dg ? Fg(e, n) : Bg(e, n)) && (u = bi(u, "onBeforeInput"), 0 < u.length && (c = new Fc("onBeforeInput", "beforeinput", null, n, c), d.push({ event: c, listeners: u }), c.data = C));
    }
    bp(d, t);
  });
}
function wo(e, t, n) {
  return { instance: e, listener: t, currentTarget: n };
}
function bi(e, t) {
  for (var n = t + "Capture", r = []; e !== null; ) {
    var o = e, i = o.stateNode;
    o.tag === 5 && i !== null && (o = i, i = mo(e, n), i != null && r.unshift(wo(e, i, o)), i = mo(e, t), i != null && r.push(wo(e, i, o))), e = e.return;
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
function qc(e, t, n, r, o) {
  for (var i = t._reactName, l = []; n !== null && n !== r; ) {
    var s = n, a = s.alternate, u = s.stateNode;
    if (a !== null && a === r)
      break;
    s.tag === 5 && u !== null && (s = u, o ? (a = mo(n, i), a != null && l.unshift(wo(n, a, s))) : o || (a = mo(n, i), a != null && l.push(wo(n, a, s)))), n = n.return;
  }
  l.length !== 0 && e.push({ event: t, listeners: l });
}
var ty = /\r\n?/g, ny = /\u0000|\uFFFD/g;
function Jc(e) {
  return (typeof e == "string" ? e : "" + e).replace(ty, `
`).replace(ny, "");
}
function oi(e, t, n) {
  if (t = Jc(t), Jc(e) !== t && n)
    throw Error(P(425));
}
function Di() {
}
var pa = null, ma = null;
function ha(e, t) {
  return e === "textarea" || e === "noscript" || typeof t.children == "string" || typeof t.children == "number" || typeof t.dangerouslySetInnerHTML == "object" && t.dangerouslySetInnerHTML !== null && t.dangerouslySetInnerHTML.__html != null;
}
var ga = typeof setTimeout == "function" ? setTimeout : void 0, ry = typeof clearTimeout == "function" ? clearTimeout : void 0, ef = typeof Promise == "function" ? Promise : void 0, oy = typeof queueMicrotask == "function" ? queueMicrotask : typeof ef < "u" ? function(e) {
  return ef.resolve(null).then(e).catch(iy);
} : ga;
function iy(e) {
  setTimeout(function() {
    throw e;
  });
}
function _s(e, t) {
  var n = t, r = 0;
  do {
    var o = n.nextSibling;
    if (e.removeChild(n), o && o.nodeType === 8)
      if (n = o.data, n === "/$") {
        if (r === 0) {
          e.removeChild(o), yo(t);
          return;
        }
        r--;
      } else
        n !== "$" && n !== "$?" && n !== "$!" || r++;
    n = o;
  } while (n);
  yo(t);
}
function fn(e) {
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
function tf(e) {
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
var Or = Math.random().toString(36).slice(2), It = "__reactFiber$" + Or, Co = "__reactProps$" + Or, Ht = "__reactContainer$" + Or, ya = "__reactEvents$" + Or, ly = "__reactListeners$" + Or, sy = "__reactHandles$" + Or;
function _n(e) {
  var t = e[It];
  if (t)
    return t;
  for (var n = e.parentNode; n; ) {
    if (t = n[Ht] || n[It]) {
      if (n = t.alternate, t.child !== null || n !== null && n.child !== null)
        for (e = tf(e); e !== null; ) {
          if (n = e[It])
            return n;
          e = tf(e);
        }
      return t;
    }
    e = n, n = e.parentNode;
  }
  return null;
}
function bo(e) {
  return e = e[It] || e[Ht], !e || e.tag !== 5 && e.tag !== 6 && e.tag !== 13 && e.tag !== 3 ? null : e;
}
function Jn(e) {
  if (e.tag === 5 || e.tag === 6)
    return e.stateNode;
  throw Error(P(33));
}
function fl(e) {
  return e[Co] || null;
}
var va = [], er = -1;
function xn(e) {
  return { current: e };
}
function ee(e) {
  0 > er || (e.current = va[er], va[er] = null, er--);
}
function q(e, t) {
  er++, va[er] = e.current, e.current = t;
}
var yn = {}, Ae = xn(yn), Ge = xn(!1), Mn = yn;
function yr(e, t) {
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
function Ke(e) {
  return e = e.childContextTypes, e != null;
}
function Fi() {
  ee(Ge), ee(Ae);
}
function nf(e, t, n) {
  if (Ae.current !== yn)
    throw Error(P(168));
  q(Ae, t), q(Ge, n);
}
function Fp(e, t, n) {
  var r = e.stateNode;
  if (t = t.childContextTypes, typeof r.getChildContext != "function")
    return n;
  r = r.getChildContext();
  for (var o in r)
    if (!(o in t))
      throw Error(P(108, H0(e) || "Unknown", o));
  return se({}, n, r);
}
function Bi(e) {
  return e = (e = e.stateNode) && e.__reactInternalMemoizedMergedChildContext || yn, Mn = Ae.current, q(Ae, e), q(Ge, Ge.current), !0;
}
function rf(e, t, n) {
  var r = e.stateNode;
  if (!r)
    throw Error(P(169));
  n ? (e = Fp(e, t, Mn), r.__reactInternalMemoizedMergedChildContext = e, ee(Ge), ee(Ae), q(Ae, e)) : ee(Ge), q(Ge, n);
}
var Dt = null, dl = !1, $s = !1;
function Bp(e) {
  Dt === null ? Dt = [e] : Dt.push(e);
}
function ay(e) {
  dl = !0, Bp(e);
}
function Sn() {
  if (!$s && Dt !== null) {
    $s = !0;
    var e = 0, t = K;
    try {
      var n = Dt;
      for (K = 1; e < n.length; e++) {
        var r = n[e];
        do
          r = r(!0);
        while (r !== null);
      }
      Dt = null, dl = !1;
    } catch (o) {
      throw Dt !== null && (Dt = Dt.slice(e + 1)), dp(au, Sn), o;
    } finally {
      K = t, $s = !1;
    }
  }
  return null;
}
var tr = [], nr = 0, Ui = null, Wi = 0, at = [], ut = 0, Nn = null, Ft = 1, Bt = "";
function wn(e, t) {
  tr[nr++] = Wi, tr[nr++] = Ui, Ui = e, Wi = t;
}
function Up(e, t, n) {
  at[ut++] = Ft, at[ut++] = Bt, at[ut++] = Nn, Nn = e;
  var r = Ft;
  e = Bt;
  var o = 32 - _t(r) - 1;
  r &= ~(1 << o), n += 1;
  var i = 32 - _t(t) + o;
  if (30 < i) {
    var l = o - o % 5;
    i = (r & (1 << l) - 1).toString(32), r >>= l, o -= l, Ft = 1 << 32 - _t(t) + o | n << o | r, Bt = i + e;
  } else
    Ft = 1 << i | n << o | r, Bt = e;
}
function yu(e) {
  e.return !== null && (wn(e, 1), Up(e, 1, 0));
}
function vu(e) {
  for (; e === Ui; )
    Ui = tr[--nr], tr[nr] = null, Wi = tr[--nr], tr[nr] = null;
  for (; e === Nn; )
    Nn = at[--ut], at[ut] = null, Bt = at[--ut], at[ut] = null, Ft = at[--ut], at[ut] = null;
}
var et = null, Je = null, re = !1, Et = null;
function Wp(e, t) {
  var n = ft(5, null, null, 0);
  n.elementType = "DELETED", n.stateNode = t, n.return = e, t = e.deletions, t === null ? (e.deletions = [n], e.flags |= 16) : t.push(n);
}
function of(e, t) {
  switch (e.tag) {
    case 5:
      var n = e.type;
      return t = t.nodeType !== 1 || n.toLowerCase() !== t.nodeName.toLowerCase() ? null : t, t !== null ? (e.stateNode = t, et = e, Je = fn(t.firstChild), !0) : !1;
    case 6:
      return t = e.pendingProps === "" || t.nodeType !== 3 ? null : t, t !== null ? (e.stateNode = t, et = e, Je = null, !0) : !1;
    case 13:
      return t = t.nodeType !== 8 ? null : t, t !== null ? (n = Nn !== null ? { id: Ft, overflow: Bt } : null, e.memoizedState = { dehydrated: t, treeContext: n, retryLane: 1073741824 }, n = ft(18, null, null, 0), n.stateNode = t, n.return = e, e.child = n, et = e, Je = null, !0) : !1;
    default:
      return !1;
  }
}
function xa(e) {
  return (e.mode & 1) !== 0 && (e.flags & 128) === 0;
}
function Sa(e) {
  if (re) {
    var t = Je;
    if (t) {
      var n = t;
      if (!of(e, t)) {
        if (xa(e))
          throw Error(P(418));
        t = fn(n.nextSibling);
        var r = et;
        t && of(e, t) ? Wp(r, n) : (e.flags = e.flags & -4097 | 2, re = !1, et = e);
      }
    } else {
      if (xa(e))
        throw Error(P(418));
      e.flags = e.flags & -4097 | 2, re = !1, et = e;
    }
  }
}
function lf(e) {
  for (e = e.return; e !== null && e.tag !== 5 && e.tag !== 3 && e.tag !== 13; )
    e = e.return;
  et = e;
}
function ii(e) {
  if (e !== et)
    return !1;
  if (!re)
    return lf(e), re = !0, !1;
  var t;
  if ((t = e.tag !== 3) && !(t = e.tag !== 5) && (t = e.type, t = t !== "head" && t !== "body" && !ha(e.type, e.memoizedProps)), t && (t = Je)) {
    if (xa(e))
      throw Vp(), Error(P(418));
    for (; t; )
      Wp(e, t), t = fn(t.nextSibling);
  }
  if (lf(e), e.tag === 13) {
    if (e = e.memoizedState, e = e !== null ? e.dehydrated : null, !e)
      throw Error(P(317));
    e: {
      for (e = e.nextSibling, t = 0; e; ) {
        if (e.nodeType === 8) {
          var n = e.data;
          if (n === "/$") {
            if (t === 0) {
              Je = fn(e.nextSibling);
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
    Je = et ? fn(e.stateNode.nextSibling) : null;
  return !0;
}
function Vp() {
  for (var e = Je; e; )
    e = fn(e.nextSibling);
}
function vr() {
  Je = et = null, re = !1;
}
function xu(e) {
  Et === null ? Et = [e] : Et.push(e);
}
var uy = Yt.ReactCurrentBatchConfig;
function Wr(e, t, n) {
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
function sf(e) {
  var t = e._init;
  return t(e._payload);
}
function Hp(e) {
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
    return m = hn(m, f), m.index = 0, m.sibling = null, m;
  }
  function i(m, f, h) {
    return m.index = h, e ? (h = m.alternate, h !== null ? (h = h.index, h < f ? (m.flags |= 2, f) : h) : (m.flags |= 2, f)) : (m.flags |= 1048576, f);
  }
  function l(m) {
    return e && m.alternate === null && (m.flags |= 2), m;
  }
  function s(m, f, h, x) {
    return f === null || f.tag !== 6 ? (f = Is(h, m.mode, x), f.return = m, f) : (f = o(f, h), f.return = m, f);
  }
  function a(m, f, h, x) {
    var _ = h.type;
    return _ === Yn ? c(m, f, h.props.children, x, h.key) : f !== null && (f.elementType === _ || typeof _ == "object" && _ !== null && _.$$typeof === en && sf(_) === f.type) ? (x = o(f, h.props), x.ref = Wr(m, f, h), x.return = m, x) : (x = _i(h.type, h.key, h.props, null, m.mode, x), x.ref = Wr(m, f, h), x.return = m, x);
  }
  function u(m, f, h, x) {
    return f === null || f.tag !== 4 || f.stateNode.containerInfo !== h.containerInfo || f.stateNode.implementation !== h.implementation ? (f = Ls(h, m.mode, x), f.return = m, f) : (f = o(f, h.children || []), f.return = m, f);
  }
  function c(m, f, h, x, _) {
    return f === null || f.tag !== 7 ? (f = On(h, m.mode, x, _), f.return = m, f) : (f = o(f, h), f.return = m, f);
  }
  function d(m, f, h) {
    if (typeof f == "string" && f !== "" || typeof f == "number")
      return f = Is("" + f, m.mode, h), f.return = m, f;
    if (typeof f == "object" && f !== null) {
      switch (f.$$typeof) {
        case Yo:
          return h = _i(f.type, f.key, f.props, null, m.mode, h), h.ref = Wr(m, null, f), h.return = m, h;
        case Qn:
          return f = Ls(f, m.mode, h), f.return = m, f;
        case en:
          var x = f._init;
          return d(m, x(f._payload), h);
      }
      if (Xr(f) || br(f))
        return f = On(f, m.mode, h, null), f.return = m, f;
      li(m, f);
    }
    return null;
  }
  function p(m, f, h, x) {
    var _ = f !== null ? f.key : null;
    if (typeof h == "string" && h !== "" || typeof h == "number")
      return _ !== null ? null : s(m, f, "" + h, x);
    if (typeof h == "object" && h !== null) {
      switch (h.$$typeof) {
        case Yo:
          return h.key === _ ? a(m, f, h, x) : null;
        case Qn:
          return h.key === _ ? u(m, f, h, x) : null;
        case en:
          return _ = h._init, p(
            m,
            f,
            _(h._payload),
            x
          );
      }
      if (Xr(h) || br(h))
        return _ !== null ? null : c(m, f, h, x, null);
      li(m, h);
    }
    return null;
  }
  function v(m, f, h, x, _) {
    if (typeof x == "string" && x !== "" || typeof x == "number")
      return m = m.get(h) || null, s(f, m, "" + x, _);
    if (typeof x == "object" && x !== null) {
      switch (x.$$typeof) {
        case Yo:
          return m = m.get(x.key === null ? h : x.key) || null, a(f, m, x, _);
        case Qn:
          return m = m.get(x.key === null ? h : x.key) || null, u(f, m, x, _);
        case en:
          var E = x._init;
          return v(m, f, h, E(x._payload), _);
      }
      if (Xr(x) || br(x))
        return m = m.get(h) || null, c(f, m, x, _, null);
      li(f, x);
    }
    return null;
  }
  function y(m, f, h, x) {
    for (var _ = null, E = null, C = f, R = f = 0, z = null; C !== null && R < h.length; R++) {
      C.index > R ? (z = C, C = null) : z = C.sibling;
      var O = p(m, C, h[R], x);
      if (O === null) {
        C === null && (C = z);
        break;
      }
      e && C && O.alternate === null && t(m, C), f = i(O, f, R), E === null ? _ = O : E.sibling = O, E = O, C = z;
    }
    if (R === h.length)
      return n(m, C), re && wn(m, R), _;
    if (C === null) {
      for (; R < h.length; R++)
        C = d(m, h[R], x), C !== null && (f = i(C, f, R), E === null ? _ = C : E.sibling = C, E = C);
      return re && wn(m, R), _;
    }
    for (C = r(m, C); R < h.length; R++)
      z = v(C, m, R, h[R], x), z !== null && (e && z.alternate !== null && C.delete(z.key === null ? R : z.key), f = i(z, f, R), E === null ? _ = z : E.sibling = z, E = z);
    return e && C.forEach(function(D) {
      return t(m, D);
    }), re && wn(m, R), _;
  }
  function g(m, f, h, x) {
    var _ = br(h);
    if (typeof _ != "function")
      throw Error(P(150));
    if (h = _.call(h), h == null)
      throw Error(P(151));
    for (var E = _ = null, C = f, R = f = 0, z = null, O = h.next(); C !== null && !O.done; R++, O = h.next()) {
      C.index > R ? (z = C, C = null) : z = C.sibling;
      var D = p(m, C, O.value, x);
      if (D === null) {
        C === null && (C = z);
        break;
      }
      e && C && D.alternate === null && t(m, C), f = i(D, f, R), E === null ? _ = D : E.sibling = D, E = D, C = z;
    }
    if (O.done)
      return n(
        m,
        C
      ), re && wn(m, R), _;
    if (C === null) {
      for (; !O.done; R++, O = h.next())
        O = d(m, O.value, x), O !== null && (f = i(O, f, R), E === null ? _ = O : E.sibling = O, E = O);
      return re && wn(m, R), _;
    }
    for (C = r(m, C); !O.done; R++, O = h.next())
      O = v(C, m, R, O.value, x), O !== null && (e && O.alternate !== null && C.delete(O.key === null ? R : O.key), f = i(O, f, R), E === null ? _ = O : E.sibling = O, E = O);
    return e && C.forEach(function(F) {
      return t(m, F);
    }), re && wn(m, R), _;
  }
  function $(m, f, h, x) {
    if (typeof h == "object" && h !== null && h.type === Yn && h.key === null && (h = h.props.children), typeof h == "object" && h !== null) {
      switch (h.$$typeof) {
        case Yo:
          e: {
            for (var _ = h.key, E = f; E !== null; ) {
              if (E.key === _) {
                if (_ = h.type, _ === Yn) {
                  if (E.tag === 7) {
                    n(m, E.sibling), f = o(E, h.props.children), f.return = m, m = f;
                    break e;
                  }
                } else if (E.elementType === _ || typeof _ == "object" && _ !== null && _.$$typeof === en && sf(_) === E.type) {
                  n(m, E.sibling), f = o(E, h.props), f.ref = Wr(m, E, h), f.return = m, m = f;
                  break e;
                }
                n(m, E);
                break;
              } else
                t(m, E);
              E = E.sibling;
            }
            h.type === Yn ? (f = On(h.props.children, m.mode, x, h.key), f.return = m, m = f) : (x = _i(h.type, h.key, h.props, null, m.mode, x), x.ref = Wr(m, f, h), x.return = m, m = x);
          }
          return l(m);
        case Qn:
          e: {
            for (E = h.key; f !== null; ) {
              if (f.key === E)
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
            f = Ls(h, m.mode, x), f.return = m, m = f;
          }
          return l(m);
        case en:
          return E = h._init, $(m, f, E(h._payload), x);
      }
      if (Xr(h))
        return y(m, f, h, x);
      if (br(h))
        return g(m, f, h, x);
      li(m, h);
    }
    return typeof h == "string" && h !== "" || typeof h == "number" ? (h = "" + h, f !== null && f.tag === 6 ? (n(m, f.sibling), f = o(f, h), f.return = m, m = f) : (n(m, f), f = Is(h, m.mode, x), f.return = m, m = f), l(m)) : n(m, f);
  }
  return $;
}
var xr = Hp(!0), Gp = Hp(!1), Vi = xn(null), Hi = null, rr = null, Su = null;
function wu() {
  Su = rr = Hi = null;
}
function Cu(e) {
  var t = Vi.current;
  ee(Vi), e._currentValue = t;
}
function wa(e, t, n) {
  for (; e !== null; ) {
    var r = e.alternate;
    if ((e.childLanes & t) !== t ? (e.childLanes |= t, r !== null && (r.childLanes |= t)) : r !== null && (r.childLanes & t) !== t && (r.childLanes |= t), e === n)
      break;
    e = e.return;
  }
}
function cr(e, t) {
  Hi = e, Su = rr = null, e = e.dependencies, e !== null && e.firstContext !== null && (e.lanes & t && (He = !0), e.firstContext = null);
}
function mt(e) {
  var t = e._currentValue;
  if (Su !== e)
    if (e = { context: e, memoizedValue: t, next: null }, rr === null) {
      if (Hi === null)
        throw Error(P(308));
      rr = e, Hi.dependencies = { lanes: 0, firstContext: e };
    } else
      rr = rr.next = e;
  return t;
}
var $n = null;
function ku(e) {
  $n === null ? $n = [e] : $n.push(e);
}
function Kp(e, t, n, r) {
  var o = t.interleaved;
  return o === null ? (n.next = n, ku(t)) : (n.next = o.next, o.next = n), t.interleaved = n, Gt(e, r);
}
function Gt(e, t) {
  e.lanes |= t;
  var n = e.alternate;
  for (n !== null && (n.lanes |= t), n = e, e = e.return; e !== null; )
    e.childLanes |= t, n = e.alternate, n !== null && (n.childLanes |= t), n = e, e = e.return;
  return n.tag === 3 ? n.stateNode : null;
}
var tn = !1;
function Eu(e) {
  e.updateQueue = { baseState: e.memoizedState, firstBaseUpdate: null, lastBaseUpdate: null, shared: { pending: null, interleaved: null, lanes: 0 }, effects: null };
}
function Qp(e, t) {
  e = e.updateQueue, t.updateQueue === e && (t.updateQueue = { baseState: e.baseState, firstBaseUpdate: e.firstBaseUpdate, lastBaseUpdate: e.lastBaseUpdate, shared: e.shared, effects: e.effects });
}
function Wt(e, t) {
  return { eventTime: e, lane: t, tag: 0, payload: null, callback: null, next: null };
}
function dn(e, t, n) {
  var r = e.updateQueue;
  if (r === null)
    return null;
  if (r = r.shared, U & 2) {
    var o = r.pending;
    return o === null ? t.next = t : (t.next = o.next, o.next = t), r.pending = t, Gt(e, n);
  }
  return o = r.interleaved, o === null ? (t.next = t, ku(r)) : (t.next = o.next, o.next = t), r.interleaved = t, Gt(e, n);
}
function xi(e, t, n) {
  if (t = t.updateQueue, t !== null && (t = t.shared, (n & 4194240) !== 0)) {
    var r = t.lanes;
    r &= e.pendingLanes, n |= r, t.lanes = n, uu(e, n);
  }
}
function af(e, t) {
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
function Gi(e, t, n, r) {
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
          var y = e, g = s;
          switch (p = t, v = n, g.tag) {
            case 1:
              if (y = g.payload, typeof y == "function") {
                d = y.call(v, d, p);
                break e;
              }
              d = y;
              break e;
            case 3:
              y.flags = y.flags & -65537 | 128;
            case 0:
              if (y = g.payload, p = typeof y == "function" ? y.call(v, d, p) : y, p == null)
                break e;
              d = se({}, d, p);
              break e;
            case 2:
              tn = !0;
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
    Ln |= l, e.lanes = l, e.memoizedState = d;
  }
}
function uf(e, t, n) {
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
var Do = {}, zt = xn(Do), ko = xn(Do), Eo = xn(Do);
function Pn(e) {
  if (e === Do)
    throw Error(P(174));
  return e;
}
function _u(e, t) {
  switch (q(Eo, t), q(ko, e), q(zt, Do), e = t.nodeType, e) {
    case 9:
    case 11:
      t = (t = t.documentElement) ? t.namespaceURI : ta(null, "");
      break;
    default:
      e = e === 8 ? t.parentNode : t, t = e.namespaceURI || null, e = e.tagName, t = ta(t, e);
  }
  ee(zt), q(zt, t);
}
function Sr() {
  ee(zt), ee(ko), ee(Eo);
}
function Yp(e) {
  Pn(Eo.current);
  var t = Pn(zt.current), n = ta(t, e.type);
  t !== n && (q(ko, e), q(zt, n));
}
function $u(e) {
  ko.current === e && (ee(zt), ee(ko));
}
var oe = xn(0);
function Ki(e) {
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
var Ps = [];
function Pu() {
  for (var e = 0; e < Ps.length; e++)
    Ps[e]._workInProgressVersionPrimary = null;
  Ps.length = 0;
}
var Si = Yt.ReactCurrentDispatcher, Ts = Yt.ReactCurrentBatchConfig, In = 0, ie = null, Se = null, ke = null, Qi = !1, lo = !1, _o = 0, cy = 0;
function Ie() {
  throw Error(P(321));
}
function Tu(e, t) {
  if (t === null)
    return !1;
  for (var n = 0; n < t.length && n < e.length; n++)
    if (!Pt(e[n], t[n]))
      return !1;
  return !0;
}
function Ru(e, t, n, r, o, i) {
  if (In = i, ie = t, t.memoizedState = null, t.updateQueue = null, t.lanes = 0, Si.current = e === null || e.memoizedState === null ? my : hy, e = n(r, o), lo) {
    i = 0;
    do {
      if (lo = !1, _o = 0, 25 <= i)
        throw Error(P(301));
      i += 1, ke = Se = null, t.updateQueue = null, Si.current = gy, e = n(r, o);
    } while (lo);
  }
  if (Si.current = Yi, t = Se !== null && Se.next !== null, In = 0, ke = Se = ie = null, Qi = !1, t)
    throw Error(P(300));
  return e;
}
function Ou() {
  var e = _o !== 0;
  return _o = 0, e;
}
function Ot() {
  var e = { memoizedState: null, baseState: null, baseQueue: null, queue: null, next: null };
  return ke === null ? ie.memoizedState = ke = e : ke = ke.next = e, ke;
}
function ht() {
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
function $o(e, t) {
  return typeof t == "function" ? t(e) : t;
}
function Rs(e) {
  var t = ht(), n = t.queue;
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
      if ((In & c) === c)
        a !== null && (a = a.next = { lane: 0, action: u.action, hasEagerState: u.hasEagerState, eagerState: u.eagerState, next: null }), r = u.hasEagerState ? u.eagerState : e(r, u.action);
      else {
        var d = {
          lane: c,
          action: u.action,
          hasEagerState: u.hasEagerState,
          eagerState: u.eagerState,
          next: null
        };
        a === null ? (s = a = d, l = r) : a = a.next = d, ie.lanes |= c, Ln |= c;
      }
      u = u.next;
    } while (u !== null && u !== i);
    a === null ? l = r : a.next = s, Pt(r, t.memoizedState) || (He = !0), t.memoizedState = r, t.baseState = l, t.baseQueue = a, n.lastRenderedState = r;
  }
  if (e = n.interleaved, e !== null) {
    o = e;
    do
      i = o.lane, ie.lanes |= i, Ln |= i, o = o.next;
    while (o !== e);
  } else
    o === null && (n.lanes = 0);
  return [t.memoizedState, n.dispatch];
}
function Os(e) {
  var t = ht(), n = t.queue;
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
    Pt(i, t.memoizedState) || (He = !0), t.memoizedState = i, t.baseQueue === null && (t.baseState = i), n.lastRenderedState = i;
  }
  return [i, r];
}
function Xp() {
}
function Zp(e, t) {
  var n = ie, r = ht(), o = t(), i = !Pt(r.memoizedState, o);
  if (i && (r.memoizedState = o, He = !0), r = r.queue, Mu(em.bind(null, n, r, e), [e]), r.getSnapshot !== t || i || ke !== null && ke.memoizedState.tag & 1) {
    if (n.flags |= 2048, Po(9, Jp.bind(null, n, r, o, t), void 0, null), Ee === null)
      throw Error(P(349));
    In & 30 || qp(n, t, o);
  }
  return o;
}
function qp(e, t, n) {
  e.flags |= 16384, e = { getSnapshot: t, value: n }, t = ie.updateQueue, t === null ? (t = { lastEffect: null, stores: null }, ie.updateQueue = t, t.stores = [e]) : (n = t.stores, n === null ? t.stores = [e] : n.push(e));
}
function Jp(e, t, n, r) {
  t.value = n, t.getSnapshot = r, tm(t) && nm(e);
}
function em(e, t, n) {
  return n(function() {
    tm(t) && nm(e);
  });
}
function tm(e) {
  var t = e.getSnapshot;
  e = e.value;
  try {
    var n = t();
    return !Pt(e, n);
  } catch {
    return !0;
  }
}
function nm(e) {
  var t = Gt(e, 1);
  t !== null && $t(t, e, 1, -1);
}
function cf(e) {
  var t = Ot();
  return typeof e == "function" && (e = e()), t.memoizedState = t.baseState = e, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: $o, lastRenderedState: e }, t.queue = e, e = e.dispatch = py.bind(null, ie, e), [t.memoizedState, e];
}
function Po(e, t, n, r) {
  return e = { tag: e, create: t, destroy: n, deps: r, next: null }, t = ie.updateQueue, t === null ? (t = { lastEffect: null, stores: null }, ie.updateQueue = t, t.lastEffect = e.next = e) : (n = t.lastEffect, n === null ? t.lastEffect = e.next = e : (r = n.next, n.next = e, e.next = r, t.lastEffect = e)), e;
}
function rm() {
  return ht().memoizedState;
}
function wi(e, t, n, r) {
  var o = Ot();
  ie.flags |= e, o.memoizedState = Po(1 | t, n, void 0, r === void 0 ? null : r);
}
function pl(e, t, n, r) {
  var o = ht();
  r = r === void 0 ? null : r;
  var i = void 0;
  if (Se !== null) {
    var l = Se.memoizedState;
    if (i = l.destroy, r !== null && Tu(r, l.deps)) {
      o.memoizedState = Po(t, n, i, r);
      return;
    }
  }
  ie.flags |= e, o.memoizedState = Po(1 | t, n, i, r);
}
function ff(e, t) {
  return wi(8390656, 8, e, t);
}
function Mu(e, t) {
  return pl(2048, 8, e, t);
}
function om(e, t) {
  return pl(4, 2, e, t);
}
function im(e, t) {
  return pl(4, 4, e, t);
}
function lm(e, t) {
  if (typeof t == "function")
    return e = e(), t(e), function() {
      t(null);
    };
  if (t != null)
    return e = e(), t.current = e, function() {
      t.current = null;
    };
}
function sm(e, t, n) {
  return n = n != null ? n.concat([e]) : null, pl(4, 4, lm.bind(null, t, e), n);
}
function Nu() {
}
function am(e, t) {
  var n = ht();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && Tu(t, r[1]) ? r[0] : (n.memoizedState = [e, t], e);
}
function um(e, t) {
  var n = ht();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && Tu(t, r[1]) ? r[0] : (e = e(), n.memoizedState = [e, t], e);
}
function cm(e, t, n) {
  return In & 21 ? (Pt(n, t) || (n = hp(), ie.lanes |= n, Ln |= n, e.baseState = !0), t) : (e.baseState && (e.baseState = !1, He = !0), e.memoizedState = n);
}
function fy(e, t) {
  var n = K;
  K = n !== 0 && 4 > n ? n : 4, e(!0);
  var r = Ts.transition;
  Ts.transition = {};
  try {
    e(!1), t();
  } finally {
    K = n, Ts.transition = r;
  }
}
function fm() {
  return ht().memoizedState;
}
function dy(e, t, n) {
  var r = mn(e);
  if (n = { lane: r, action: n, hasEagerState: !1, eagerState: null, next: null }, dm(e))
    pm(t, n);
  else if (n = Kp(e, t, n, r), n !== null) {
    var o = Be();
    $t(n, e, r, o), mm(n, t, r);
  }
}
function py(e, t, n) {
  var r = mn(e), o = { lane: r, action: n, hasEagerState: !1, eagerState: null, next: null };
  if (dm(e))
    pm(t, o);
  else {
    var i = e.alternate;
    if (e.lanes === 0 && (i === null || i.lanes === 0) && (i = t.lastRenderedReducer, i !== null))
      try {
        var l = t.lastRenderedState, s = i(l, n);
        if (o.hasEagerState = !0, o.eagerState = s, Pt(s, l)) {
          var a = t.interleaved;
          a === null ? (o.next = o, ku(t)) : (o.next = a.next, a.next = o), t.interleaved = o;
          return;
        }
      } catch {
      } finally {
      }
    n = Kp(e, t, o, r), n !== null && (o = Be(), $t(n, e, r, o), mm(n, t, r));
  }
}
function dm(e) {
  var t = e.alternate;
  return e === ie || t !== null && t === ie;
}
function pm(e, t) {
  lo = Qi = !0;
  var n = e.pending;
  n === null ? t.next = t : (t.next = n.next, n.next = t), e.pending = t;
}
function mm(e, t, n) {
  if (n & 4194240) {
    var r = t.lanes;
    r &= e.pendingLanes, n |= r, t.lanes = n, uu(e, n);
  }
}
var Yi = { readContext: mt, useCallback: Ie, useContext: Ie, useEffect: Ie, useImperativeHandle: Ie, useInsertionEffect: Ie, useLayoutEffect: Ie, useMemo: Ie, useReducer: Ie, useRef: Ie, useState: Ie, useDebugValue: Ie, useDeferredValue: Ie, useTransition: Ie, useMutableSource: Ie, useSyncExternalStore: Ie, useId: Ie, unstable_isNewReconciler: !1 }, my = { readContext: mt, useCallback: function(e, t) {
  return Ot().memoizedState = [e, t === void 0 ? null : t], e;
}, useContext: mt, useEffect: ff, useImperativeHandle: function(e, t, n) {
  return n = n != null ? n.concat([e]) : null, wi(
    4194308,
    4,
    lm.bind(null, t, e),
    n
  );
}, useLayoutEffect: function(e, t) {
  return wi(4194308, 4, e, t);
}, useInsertionEffect: function(e, t) {
  return wi(4, 2, e, t);
}, useMemo: function(e, t) {
  var n = Ot();
  return t = t === void 0 ? null : t, e = e(), n.memoizedState = [e, t], e;
}, useReducer: function(e, t, n) {
  var r = Ot();
  return t = n !== void 0 ? n(t) : t, r.memoizedState = r.baseState = t, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: e, lastRenderedState: t }, r.queue = e, e = e.dispatch = dy.bind(null, ie, e), [r.memoizedState, e];
}, useRef: function(e) {
  var t = Ot();
  return e = { current: e }, t.memoizedState = e;
}, useState: cf, useDebugValue: Nu, useDeferredValue: function(e) {
  return Ot().memoizedState = e;
}, useTransition: function() {
  var e = cf(!1), t = e[0];
  return e = fy.bind(null, e[1]), Ot().memoizedState = e, [t, e];
}, useMutableSource: function() {
}, useSyncExternalStore: function(e, t, n) {
  var r = ie, o = Ot();
  if (re) {
    if (n === void 0)
      throw Error(P(407));
    n = n();
  } else {
    if (n = t(), Ee === null)
      throw Error(P(349));
    In & 30 || qp(r, t, n);
  }
  o.memoizedState = n;
  var i = { value: n, getSnapshot: t };
  return o.queue = i, ff(em.bind(
    null,
    r,
    i,
    e
  ), [e]), r.flags |= 2048, Po(9, Jp.bind(null, r, i, n, t), void 0, null), n;
}, useId: function() {
  var e = Ot(), t = Ee.identifierPrefix;
  if (re) {
    var n = Bt, r = Ft;
    n = (r & ~(1 << 32 - _t(r) - 1)).toString(32) + n, t = ":" + t + "R" + n, n = _o++, 0 < n && (t += "H" + n.toString(32)), t += ":";
  } else
    n = cy++, t = ":" + t + "r" + n.toString(32) + ":";
  return e.memoizedState = t;
}, unstable_isNewReconciler: !1 }, hy = {
  readContext: mt,
  useCallback: am,
  useContext: mt,
  useEffect: Mu,
  useImperativeHandle: sm,
  useInsertionEffect: om,
  useLayoutEffect: im,
  useMemo: um,
  useReducer: Rs,
  useRef: rm,
  useState: function() {
    return Rs($o);
  },
  useDebugValue: Nu,
  useDeferredValue: function(e) {
    var t = ht();
    return cm(t, Se.memoizedState, e);
  },
  useTransition: function() {
    var e = Rs($o)[0], t = ht().memoizedState;
    return [e, t];
  },
  useMutableSource: Xp,
  useSyncExternalStore: Zp,
  useId: fm,
  unstable_isNewReconciler: !1
}, gy = { readContext: mt, useCallback: am, useContext: mt, useEffect: Mu, useImperativeHandle: sm, useInsertionEffect: om, useLayoutEffect: im, useMemo: um, useReducer: Os, useRef: rm, useState: function() {
  return Os($o);
}, useDebugValue: Nu, useDeferredValue: function(e) {
  var t = ht();
  return Se === null ? t.memoizedState = e : cm(t, Se.memoizedState, e);
}, useTransition: function() {
  var e = Os($o)[0], t = ht().memoizedState;
  return [e, t];
}, useMutableSource: Xp, useSyncExternalStore: Zp, useId: fm, unstable_isNewReconciler: !1 };
function Ct(e, t) {
  if (e && e.defaultProps) {
    t = se({}, t), e = e.defaultProps;
    for (var n in e)
      t[n] === void 0 && (t[n] = e[n]);
    return t;
  }
  return t;
}
function Ca(e, t, n, r) {
  t = e.memoizedState, n = n(r, t), n = n == null ? t : se({}, t, n), e.memoizedState = n, e.lanes === 0 && (e.updateQueue.baseState = n);
}
var ml = { isMounted: function(e) {
  return (e = e._reactInternals) ? An(e) === e : !1;
}, enqueueSetState: function(e, t, n) {
  e = e._reactInternals;
  var r = Be(), o = mn(e), i = Wt(r, o);
  i.payload = t, n != null && (i.callback = n), t = dn(e, i, o), t !== null && ($t(t, e, o, r), xi(t, e, o));
}, enqueueReplaceState: function(e, t, n) {
  e = e._reactInternals;
  var r = Be(), o = mn(e), i = Wt(r, o);
  i.tag = 1, i.payload = t, n != null && (i.callback = n), t = dn(e, i, o), t !== null && ($t(t, e, o, r), xi(t, e, o));
}, enqueueForceUpdate: function(e, t) {
  e = e._reactInternals;
  var n = Be(), r = mn(e), o = Wt(n, r);
  o.tag = 2, t != null && (o.callback = t), t = dn(e, o, r), t !== null && ($t(t, e, r, n), xi(t, e, r));
} };
function df(e, t, n, r, o, i, l) {
  return e = e.stateNode, typeof e.shouldComponentUpdate == "function" ? e.shouldComponentUpdate(r, i, l) : t.prototype && t.prototype.isPureReactComponent ? !xo(n, r) || !xo(o, i) : !0;
}
function hm(e, t, n) {
  var r = !1, o = yn, i = t.contextType;
  return typeof i == "object" && i !== null ? i = mt(i) : (o = Ke(t) ? Mn : Ae.current, r = t.contextTypes, i = (r = r != null) ? yr(e, o) : yn), t = new t(n, i), e.memoizedState = t.state !== null && t.state !== void 0 ? t.state : null, t.updater = ml, e.stateNode = t, t._reactInternals = e, r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = o, e.__reactInternalMemoizedMaskedChildContext = i), t;
}
function pf(e, t, n, r) {
  e = t.state, typeof t.componentWillReceiveProps == "function" && t.componentWillReceiveProps(n, r), typeof t.UNSAFE_componentWillReceiveProps == "function" && t.UNSAFE_componentWillReceiveProps(n, r), t.state !== e && ml.enqueueReplaceState(t, t.state, null);
}
function ka(e, t, n, r) {
  var o = e.stateNode;
  o.props = n, o.state = e.memoizedState, o.refs = {}, Eu(e);
  var i = t.contextType;
  typeof i == "object" && i !== null ? o.context = mt(i) : (i = Ke(t) ? Mn : Ae.current, o.context = yr(e, i)), o.state = e.memoizedState, i = t.getDerivedStateFromProps, typeof i == "function" && (Ca(e, t, i, n), o.state = e.memoizedState), typeof t.getDerivedStateFromProps == "function" || typeof o.getSnapshotBeforeUpdate == "function" || typeof o.UNSAFE_componentWillMount != "function" && typeof o.componentWillMount != "function" || (t = o.state, typeof o.componentWillMount == "function" && o.componentWillMount(), typeof o.UNSAFE_componentWillMount == "function" && o.UNSAFE_componentWillMount(), t !== o.state && ml.enqueueReplaceState(o, o.state, null), Gi(e, n, o, r), o.state = e.memoizedState), typeof o.componentDidMount == "function" && (e.flags |= 4194308);
}
function wr(e, t) {
  try {
    var n = "", r = t;
    do
      n += V0(r), r = r.return;
    while (r);
    var o = n;
  } catch (i) {
    o = `
Error generating stack: ` + i.message + `
` + i.stack;
  }
  return { value: e, source: t, stack: o, digest: null };
}
function Ms(e, t, n) {
  return { value: e, source: null, stack: n ?? null, digest: t ?? null };
}
function Ea(e, t) {
  try {
    console.error(t.value);
  } catch (n) {
    setTimeout(function() {
      throw n;
    });
  }
}
var yy = typeof WeakMap == "function" ? WeakMap : Map;
function gm(e, t, n) {
  n = Wt(-1, n), n.tag = 3, n.payload = { element: null };
  var r = t.value;
  return n.callback = function() {
    Zi || (Zi = !0, La = r), Ea(e, t);
  }, n;
}
function ym(e, t, n) {
  n = Wt(-1, n), n.tag = 3;
  var r = e.type.getDerivedStateFromError;
  if (typeof r == "function") {
    var o = t.value;
    n.payload = function() {
      return r(o);
    }, n.callback = function() {
      Ea(e, t);
    };
  }
  var i = e.stateNode;
  return i !== null && typeof i.componentDidCatch == "function" && (n.callback = function() {
    Ea(e, t), typeof r != "function" && (pn === null ? pn = /* @__PURE__ */ new Set([this]) : pn.add(this));
    var l = t.stack;
    this.componentDidCatch(t.value, { componentStack: l !== null ? l : "" });
  }), n;
}
function mf(e, t, n) {
  var r = e.pingCache;
  if (r === null) {
    r = e.pingCache = new yy();
    var o = /* @__PURE__ */ new Set();
    r.set(t, o);
  } else
    o = r.get(t), o === void 0 && (o = /* @__PURE__ */ new Set(), r.set(t, o));
  o.has(n) || (o.add(n), e = My.bind(null, e, t, n), t.then(e, e));
}
function hf(e) {
  do {
    var t;
    if ((t = e.tag === 13) && (t = e.memoizedState, t = t !== null ? t.dehydrated !== null : !0), t)
      return e;
    e = e.return;
  } while (e !== null);
  return null;
}
function gf(e, t, n, r, o) {
  return e.mode & 1 ? (e.flags |= 65536, e.lanes = o, e) : (e === t ? e.flags |= 65536 : (e.flags |= 128, n.flags |= 131072, n.flags &= -52805, n.tag === 1 && (n.alternate === null ? n.tag = 17 : (t = Wt(-1, 1), t.tag = 2, dn(n, t, 1))), n.lanes |= 1), e);
}
var vy = Yt.ReactCurrentOwner, He = !1;
function Fe(e, t, n, r) {
  t.child = e === null ? Gp(t, null, n, r) : xr(t, e.child, n, r);
}
function yf(e, t, n, r, o) {
  n = n.render;
  var i = t.ref;
  return cr(t, o), r = Ru(e, t, n, r, i, o), n = Ou(), e !== null && !He ? (t.updateQueue = e.updateQueue, t.flags &= -2053, e.lanes &= ~o, Kt(e, t, o)) : (re && n && yu(t), t.flags |= 1, Fe(e, t, r, o), t.child);
}
function vf(e, t, n, r, o) {
  if (e === null) {
    var i = n.type;
    return typeof i == "function" && !Fu(i) && i.defaultProps === void 0 && n.compare === null && n.defaultProps === void 0 ? (t.tag = 15, t.type = i, vm(e, t, i, r, o)) : (e = _i(n.type, null, r, t, t.mode, o), e.ref = t.ref, e.return = t, t.child = e);
  }
  if (i = e.child, !(e.lanes & o)) {
    var l = i.memoizedProps;
    if (n = n.compare, n = n !== null ? n : xo, n(l, r) && e.ref === t.ref)
      return Kt(e, t, o);
  }
  return t.flags |= 1, e = hn(i, r), e.ref = t.ref, e.return = t, t.child = e;
}
function vm(e, t, n, r, o) {
  if (e !== null) {
    var i = e.memoizedProps;
    if (xo(i, r) && e.ref === t.ref)
      if (He = !1, t.pendingProps = r = i, (e.lanes & o) !== 0)
        e.flags & 131072 && (He = !0);
      else
        return t.lanes = e.lanes, Kt(e, t, o);
  }
  return _a(e, t, n, r, o);
}
function xm(e, t, n) {
  var r = t.pendingProps, o = r.children, i = e !== null ? e.memoizedState : null;
  if (r.mode === "hidden")
    if (!(t.mode & 1))
      t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, q(ir, Xe), Xe |= n;
    else {
      if (!(n & 1073741824))
        return e = i !== null ? i.baseLanes | n : n, t.lanes = t.childLanes = 1073741824, t.memoizedState = { baseLanes: e, cachePool: null, transitions: null }, t.updateQueue = null, q(ir, Xe), Xe |= e, null;
      t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, r = i !== null ? i.baseLanes : n, q(ir, Xe), Xe |= r;
    }
  else
    i !== null ? (r = i.baseLanes | n, t.memoizedState = null) : r = n, q(ir, Xe), Xe |= r;
  return Fe(e, t, o, n), t.child;
}
function Sm(e, t) {
  var n = t.ref;
  (e === null && n !== null || e !== null && e.ref !== n) && (t.flags |= 512, t.flags |= 2097152);
}
function _a(e, t, n, r, o) {
  var i = Ke(n) ? Mn : Ae.current;
  return i = yr(t, i), cr(t, o), n = Ru(e, t, n, r, i, o), r = Ou(), e !== null && !He ? (t.updateQueue = e.updateQueue, t.flags &= -2053, e.lanes &= ~o, Kt(e, t, o)) : (re && r && yu(t), t.flags |= 1, Fe(e, t, n, o), t.child);
}
function xf(e, t, n, r, o) {
  if (Ke(n)) {
    var i = !0;
    Bi(t);
  } else
    i = !1;
  if (cr(t, o), t.stateNode === null)
    Ci(e, t), hm(t, n, r), ka(t, n, r, o), r = !0;
  else if (e === null) {
    var l = t.stateNode, s = t.memoizedProps;
    l.props = s;
    var a = l.context, u = n.contextType;
    typeof u == "object" && u !== null ? u = mt(u) : (u = Ke(n) ? Mn : Ae.current, u = yr(t, u));
    var c = n.getDerivedStateFromProps, d = typeof c == "function" || typeof l.getSnapshotBeforeUpdate == "function";
    d || typeof l.UNSAFE_componentWillReceiveProps != "function" && typeof l.componentWillReceiveProps != "function" || (s !== r || a !== u) && pf(t, l, r, u), tn = !1;
    var p = t.memoizedState;
    l.state = p, Gi(t, r, l, o), a = t.memoizedState, s !== r || p !== a || Ge.current || tn ? (typeof c == "function" && (Ca(t, n, c, r), a = t.memoizedState), (s = tn || df(t, n, s, r, p, a, u)) ? (d || typeof l.UNSAFE_componentWillMount != "function" && typeof l.componentWillMount != "function" || (typeof l.componentWillMount == "function" && l.componentWillMount(), typeof l.UNSAFE_componentWillMount == "function" && l.UNSAFE_componentWillMount()), typeof l.componentDidMount == "function" && (t.flags |= 4194308)) : (typeof l.componentDidMount == "function" && (t.flags |= 4194308), t.memoizedProps = r, t.memoizedState = a), l.props = r, l.state = a, l.context = u, r = s) : (typeof l.componentDidMount == "function" && (t.flags |= 4194308), r = !1);
  } else {
    l = t.stateNode, Qp(e, t), s = t.memoizedProps, u = t.type === t.elementType ? s : Ct(t.type, s), l.props = u, d = t.pendingProps, p = l.context, a = n.contextType, typeof a == "object" && a !== null ? a = mt(a) : (a = Ke(n) ? Mn : Ae.current, a = yr(t, a));
    var v = n.getDerivedStateFromProps;
    (c = typeof v == "function" || typeof l.getSnapshotBeforeUpdate == "function") || typeof l.UNSAFE_componentWillReceiveProps != "function" && typeof l.componentWillReceiveProps != "function" || (s !== d || p !== a) && pf(t, l, r, a), tn = !1, p = t.memoizedState, l.state = p, Gi(t, r, l, o);
    var y = t.memoizedState;
    s !== d || p !== y || Ge.current || tn ? (typeof v == "function" && (Ca(t, n, v, r), y = t.memoizedState), (u = tn || df(t, n, u, r, p, y, a) || !1) ? (c || typeof l.UNSAFE_componentWillUpdate != "function" && typeof l.componentWillUpdate != "function" || (typeof l.componentWillUpdate == "function" && l.componentWillUpdate(r, y, a), typeof l.UNSAFE_componentWillUpdate == "function" && l.UNSAFE_componentWillUpdate(r, y, a)), typeof l.componentDidUpdate == "function" && (t.flags |= 4), typeof l.getSnapshotBeforeUpdate == "function" && (t.flags |= 1024)) : (typeof l.componentDidUpdate != "function" || s === e.memoizedProps && p === e.memoizedState || (t.flags |= 4), typeof l.getSnapshotBeforeUpdate != "function" || s === e.memoizedProps && p === e.memoizedState || (t.flags |= 1024), t.memoizedProps = r, t.memoizedState = y), l.props = r, l.state = y, l.context = a, r = u) : (typeof l.componentDidUpdate != "function" || s === e.memoizedProps && p === e.memoizedState || (t.flags |= 4), typeof l.getSnapshotBeforeUpdate != "function" || s === e.memoizedProps && p === e.memoizedState || (t.flags |= 1024), r = !1);
  }
  return $a(e, t, n, r, i, o);
}
function $a(e, t, n, r, o, i) {
  Sm(e, t);
  var l = (t.flags & 128) !== 0;
  if (!r && !l)
    return o && rf(t, n, !1), Kt(e, t, i);
  r = t.stateNode, vy.current = t;
  var s = l && typeof n.getDerivedStateFromError != "function" ? null : r.render();
  return t.flags |= 1, e !== null && l ? (t.child = xr(t, e.child, null, i), t.child = xr(t, null, s, i)) : Fe(e, t, s, i), t.memoizedState = r.state, o && rf(t, n, !0), t.child;
}
function wm(e) {
  var t = e.stateNode;
  t.pendingContext ? nf(e, t.pendingContext, t.pendingContext !== t.context) : t.context && nf(e, t.context, !1), _u(e, t.containerInfo);
}
function Sf(e, t, n, r, o) {
  return vr(), xu(o), t.flags |= 256, Fe(e, t, n, r), t.child;
}
var Pa = { dehydrated: null, treeContext: null, retryLane: 0 };
function Ta(e) {
  return { baseLanes: e, cachePool: null, transitions: null };
}
function Cm(e, t, n) {
  var r = t.pendingProps, o = oe.current, i = !1, l = (t.flags & 128) !== 0, s;
  if ((s = l) || (s = e !== null && e.memoizedState === null ? !1 : (o & 2) !== 0), s ? (i = !0, t.flags &= -129) : (e === null || e.memoizedState !== null) && (o |= 1), q(oe, o & 1), e === null)
    return Sa(t), e = t.memoizedState, e !== null && (e = e.dehydrated, e !== null) ? (t.mode & 1 ? e.data === "$!" ? t.lanes = 8 : t.lanes = 1073741824 : t.lanes = 1, null) : (l = r.children, e = r.fallback, i ? (r = t.mode, i = t.child, l = { mode: "hidden", children: l }, !(r & 1) && i !== null ? (i.childLanes = 0, i.pendingProps = l) : i = yl(l, r, 0, null), e = On(e, r, n, null), i.return = t, e.return = t, i.sibling = e, t.child = i, t.child.memoizedState = Ta(n), t.memoizedState = Pa, e) : Iu(t, l));
  if (o = e.memoizedState, o !== null && (s = o.dehydrated, s !== null))
    return xy(e, t, l, r, s, o, n);
  if (i) {
    i = r.fallback, l = t.mode, o = e.child, s = o.sibling;
    var a = { mode: "hidden", children: r.children };
    return !(l & 1) && t.child !== o ? (r = t.child, r.childLanes = 0, r.pendingProps = a, t.deletions = null) : (r = hn(o, a), r.subtreeFlags = o.subtreeFlags & 14680064), s !== null ? i = hn(s, i) : (i = On(i, l, n, null), i.flags |= 2), i.return = t, r.return = t, r.sibling = i, t.child = r, r = i, i = t.child, l = e.child.memoizedState, l = l === null ? Ta(n) : { baseLanes: l.baseLanes | n, cachePool: null, transitions: l.transitions }, i.memoizedState = l, i.childLanes = e.childLanes & ~n, t.memoizedState = Pa, r;
  }
  return i = e.child, e = i.sibling, r = hn(i, { mode: "visible", children: r.children }), !(t.mode & 1) && (r.lanes = n), r.return = t, r.sibling = null, e !== null && (n = t.deletions, n === null ? (t.deletions = [e], t.flags |= 16) : n.push(e)), t.child = r, t.memoizedState = null, r;
}
function Iu(e, t) {
  return t = yl({ mode: "visible", children: t }, e.mode, 0, null), t.return = e, e.child = t;
}
function si(e, t, n, r) {
  return r !== null && xu(r), xr(t, e.child, null, n), e = Iu(t, t.pendingProps.children), e.flags |= 2, t.memoizedState = null, e;
}
function xy(e, t, n, r, o, i, l) {
  if (n)
    return t.flags & 256 ? (t.flags &= -257, r = Ms(Error(P(422))), si(e, t, l, r)) : t.memoizedState !== null ? (t.child = e.child, t.flags |= 128, null) : (i = r.fallback, o = t.mode, r = yl({ mode: "visible", children: r.children }, o, 0, null), i = On(i, o, l, null), i.flags |= 2, r.return = t, i.return = t, r.sibling = i, t.child = r, t.mode & 1 && xr(t, e.child, null, l), t.child.memoizedState = Ta(l), t.memoizedState = Pa, i);
  if (!(t.mode & 1))
    return si(e, t, l, null);
  if (o.data === "$!") {
    if (r = o.nextSibling && o.nextSibling.dataset, r)
      var s = r.dgst;
    return r = s, i = Error(P(419)), r = Ms(i, r, void 0), si(e, t, l, r);
  }
  if (s = (l & e.childLanes) !== 0, He || s) {
    if (r = Ee, r !== null) {
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
      o = o & (r.suspendedLanes | l) ? 0 : o, o !== 0 && o !== i.retryLane && (i.retryLane = o, Gt(e, o), $t(r, e, o, -1));
    }
    return Du(), r = Ms(Error(P(421))), si(e, t, l, r);
  }
  return o.data === "$?" ? (t.flags |= 128, t.child = e.child, t = Ny.bind(null, e), o._reactRetry = t, null) : (e = i.treeContext, Je = fn(o.nextSibling), et = t, re = !0, Et = null, e !== null && (at[ut++] = Ft, at[ut++] = Bt, at[ut++] = Nn, Ft = e.id, Bt = e.overflow, Nn = t), t = Iu(t, r.children), t.flags |= 4096, t);
}
function wf(e, t, n) {
  e.lanes |= t;
  var r = e.alternate;
  r !== null && (r.lanes |= t), wa(e.return, t, n);
}
function Ns(e, t, n, r, o) {
  var i = e.memoizedState;
  i === null ? e.memoizedState = { isBackwards: t, rendering: null, renderingStartTime: 0, last: r, tail: n, tailMode: o } : (i.isBackwards = t, i.rendering = null, i.renderingStartTime = 0, i.last = r, i.tail = n, i.tailMode = o);
}
function km(e, t, n) {
  var r = t.pendingProps, o = r.revealOrder, i = r.tail;
  if (Fe(e, t, r.children, n), r = oe.current, r & 2)
    r = r & 1 | 2, t.flags |= 128;
  else {
    if (e !== null && e.flags & 128)
      e:
        for (e = t.child; e !== null; ) {
          if (e.tag === 13)
            e.memoizedState !== null && wf(e, n, t);
          else if (e.tag === 19)
            wf(e, n, t);
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
          e = n.alternate, e !== null && Ki(e) === null && (o = n), n = n.sibling;
        n = o, n === null ? (o = t.child, t.child = null) : (o = n.sibling, n.sibling = null), Ns(t, !1, o, n, i);
        break;
      case "backwards":
        for (n = null, o = t.child, t.child = null; o !== null; ) {
          if (e = o.alternate, e !== null && Ki(e) === null) {
            t.child = o;
            break;
          }
          e = o.sibling, o.sibling = n, n = o, o = e;
        }
        Ns(t, !0, n, null, i);
        break;
      case "together":
        Ns(t, !1, null, null, void 0);
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
    for (e = t.child, n = hn(e, e.pendingProps), t.child = n, n.return = t; e.sibling !== null; )
      e = e.sibling, n = n.sibling = hn(e, e.pendingProps), n.return = t;
    n.sibling = null;
  }
  return t.child;
}
function Sy(e, t, n) {
  switch (t.tag) {
    case 3:
      wm(t), vr();
      break;
    case 5:
      Yp(t);
      break;
    case 1:
      Ke(t.type) && Bi(t);
      break;
    case 4:
      _u(t, t.stateNode.containerInfo);
      break;
    case 10:
      var r = t.type._context, o = t.memoizedProps.value;
      q(Vi, r._currentValue), r._currentValue = o;
      break;
    case 13:
      if (r = t.memoizedState, r !== null)
        return r.dehydrated !== null ? (q(oe, oe.current & 1), t.flags |= 128, null) : n & t.child.childLanes ? Cm(e, t, n) : (q(oe, oe.current & 1), e = Kt(e, t, n), e !== null ? e.sibling : null);
      q(oe, oe.current & 1);
      break;
    case 19:
      if (r = (n & t.childLanes) !== 0, e.flags & 128) {
        if (r)
          return km(e, t, n);
        t.flags |= 128;
      }
      if (o = t.memoizedState, o !== null && (o.rendering = null, o.tail = null, o.lastEffect = null), q(oe, oe.current), r)
        break;
      return null;
    case 22:
    case 23:
      return t.lanes = 0, xm(e, t, n);
  }
  return Kt(e, t, n);
}
var Em, Ra, _m, $m;
Em = function(e, t) {
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
Ra = function() {
};
_m = function(e, t, n, r) {
  var o = e.memoizedProps;
  if (o !== r) {
    e = t.stateNode, Pn(zt.current);
    var i = null;
    switch (n) {
      case "input":
        o = Zs(e, o), r = Zs(e, r), i = [];
        break;
      case "select":
        o = se({}, o, { value: void 0 }), r = se({}, r, { value: void 0 }), i = [];
        break;
      case "textarea":
        o = ea(e, o), r = ea(e, r), i = [];
        break;
      default:
        typeof o.onClick != "function" && typeof r.onClick == "function" && (e.onclick = Di);
    }
    na(n, r);
    var l;
    n = null;
    for (u in o)
      if (!r.hasOwnProperty(u) && o.hasOwnProperty(u) && o[u] != null)
        if (u === "style") {
          var s = o[u];
          for (l in s)
            s.hasOwnProperty(l) && (n || (n = {}), n[l] = "");
        } else
          u !== "dangerouslySetInnerHTML" && u !== "children" && u !== "suppressContentEditableWarning" && u !== "suppressHydrationWarning" && u !== "autoFocus" && (fo.hasOwnProperty(u) ? i || (i = []) : (i = i || []).push(u, null));
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
          u === "dangerouslySetInnerHTML" ? (a = a ? a.__html : void 0, s = s ? s.__html : void 0, a != null && s !== a && (i = i || []).push(u, a)) : u === "children" ? typeof a != "string" && typeof a != "number" || (i = i || []).push(u, "" + a) : u !== "suppressContentEditableWarning" && u !== "suppressHydrationWarning" && (fo.hasOwnProperty(u) ? (a != null && u === "onScroll" && J("scroll", e), i || s === a || (i = [])) : (i = i || []).push(u, a));
    }
    n && (i = i || []).push("style", n);
    var u = i;
    (t.updateQueue = u) && (t.flags |= 4);
  }
};
$m = function(e, t, n, r) {
  n !== r && (t.flags |= 4);
};
function Vr(e, t) {
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
function Le(e) {
  var t = e.alternate !== null && e.alternate.child === e.child, n = 0, r = 0;
  if (t)
    for (var o = e.child; o !== null; )
      n |= o.lanes | o.childLanes, r |= o.subtreeFlags & 14680064, r |= o.flags & 14680064, o.return = e, o = o.sibling;
  else
    for (o = e.child; o !== null; )
      n |= o.lanes | o.childLanes, r |= o.subtreeFlags, r |= o.flags, o.return = e, o = o.sibling;
  return e.subtreeFlags |= r, e.childLanes = n, t;
}
function wy(e, t, n) {
  var r = t.pendingProps;
  switch (vu(t), t.tag) {
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
      return Le(t), null;
    case 1:
      return Ke(t.type) && Fi(), Le(t), null;
    case 3:
      return r = t.stateNode, Sr(), ee(Ge), ee(Ae), Pu(), r.pendingContext && (r.context = r.pendingContext, r.pendingContext = null), (e === null || e.child === null) && (ii(t) ? t.flags |= 4 : e === null || e.memoizedState.isDehydrated && !(t.flags & 256) || (t.flags |= 1024, Et !== null && (Aa(Et), Et = null))), Ra(e, t), Le(t), null;
    case 5:
      $u(t);
      var o = Pn(Eo.current);
      if (n = t.type, e !== null && t.stateNode != null)
        _m(e, t, n, r, o), e.ref !== t.ref && (t.flags |= 512, t.flags |= 2097152);
      else {
        if (!r) {
          if (t.stateNode === null)
            throw Error(P(166));
          return Le(t), null;
        }
        if (e = Pn(zt.current), ii(t)) {
          r = t.stateNode, n = t.type;
          var i = t.memoizedProps;
          switch (r[It] = t, r[Co] = i, e = (t.mode & 1) !== 0, n) {
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
              for (o = 0; o < qr.length; o++)
                J(qr[o], r);
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
              Rc(r, i), J("invalid", r);
              break;
            case "select":
              r._wrapperState = { wasMultiple: !!i.multiple }, J("invalid", r);
              break;
            case "textarea":
              Mc(r, i), J("invalid", r);
          }
          na(n, i), o = null;
          for (var l in i)
            if (i.hasOwnProperty(l)) {
              var s = i[l];
              l === "children" ? typeof s == "string" ? r.textContent !== s && (i.suppressHydrationWarning !== !0 && oi(r.textContent, s, e), o = ["children", s]) : typeof s == "number" && r.textContent !== "" + s && (i.suppressHydrationWarning !== !0 && oi(
                r.textContent,
                s,
                e
              ), o = ["children", "" + s]) : fo.hasOwnProperty(l) && s != null && l === "onScroll" && J("scroll", r);
            }
          switch (n) {
            case "input":
              Xo(r), Oc(r, i, !0);
              break;
            case "textarea":
              Xo(r), Nc(r);
              break;
            case "select":
            case "option":
              break;
            default:
              typeof i.onClick == "function" && (r.onclick = Di);
          }
          r = o, t.updateQueue = r, r !== null && (t.flags |= 4);
        } else {
          l = o.nodeType === 9 ? o : o.ownerDocument, e === "http://www.w3.org/1999/xhtml" && (e = ep(n)), e === "http://www.w3.org/1999/xhtml" ? n === "script" ? (e = l.createElement("div"), e.innerHTML = "<script><\/script>", e = e.removeChild(e.firstChild)) : typeof r.is == "string" ? e = l.createElement(n, { is: r.is }) : (e = l.createElement(n), n === "select" && (l = e, r.multiple ? l.multiple = !0 : r.size && (l.size = r.size))) : e = l.createElementNS(e, n), e[It] = t, e[Co] = r, Em(e, t, !1, !1), t.stateNode = e;
          e: {
            switch (l = ra(n, r), n) {
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
                for (o = 0; o < qr.length; o++)
                  J(qr[o], e);
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
                Rc(e, r), o = Zs(e, r), J("invalid", e);
                break;
              case "option":
                o = r;
                break;
              case "select":
                e._wrapperState = { wasMultiple: !!r.multiple }, o = se({}, r, { value: void 0 }), J("invalid", e);
                break;
              case "textarea":
                Mc(e, r), o = ea(e, r), J("invalid", e);
                break;
              default:
                o = r;
            }
            na(n, o), s = o;
            for (i in s)
              if (s.hasOwnProperty(i)) {
                var a = s[i];
                i === "style" ? rp(e, a) : i === "dangerouslySetInnerHTML" ? (a = a ? a.__html : void 0, a != null && tp(e, a)) : i === "children" ? typeof a == "string" ? (n !== "textarea" || a !== "") && po(e, a) : typeof a == "number" && po(e, "" + a) : i !== "suppressContentEditableWarning" && i !== "suppressHydrationWarning" && i !== "autoFocus" && (fo.hasOwnProperty(i) ? a != null && i === "onScroll" && J("scroll", e) : a != null && ru(e, i, a, l));
              }
            switch (n) {
              case "input":
                Xo(e), Oc(e, r, !1);
                break;
              case "textarea":
                Xo(e), Nc(e);
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
      return Le(t), null;
    case 6:
      if (e && t.stateNode != null)
        $m(e, t, e.memoizedProps, r);
      else {
        if (typeof r != "string" && t.stateNode === null)
          throw Error(P(166));
        if (n = Pn(Eo.current), Pn(zt.current), ii(t)) {
          if (r = t.stateNode, n = t.memoizedProps, r[It] = t, (i = r.nodeValue !== n) && (e = et, e !== null))
            switch (e.tag) {
              case 3:
                oi(r.nodeValue, n, (e.mode & 1) !== 0);
                break;
              case 5:
                e.memoizedProps.suppressHydrationWarning !== !0 && oi(r.nodeValue, n, (e.mode & 1) !== 0);
            }
          i && (t.flags |= 4);
        } else
          r = (n.nodeType === 9 ? n : n.ownerDocument).createTextNode(r), r[It] = t, t.stateNode = r;
      }
      return Le(t), null;
    case 13:
      if (ee(oe), r = t.memoizedState, e === null || e.memoizedState !== null && e.memoizedState.dehydrated !== null) {
        if (re && Je !== null && t.mode & 1 && !(t.flags & 128))
          Vp(), vr(), t.flags |= 98560, i = !1;
        else if (i = ii(t), r !== null && r.dehydrated !== null) {
          if (e === null) {
            if (!i)
              throw Error(P(318));
            if (i = t.memoizedState, i = i !== null ? i.dehydrated : null, !i)
              throw Error(P(317));
            i[It] = t;
          } else
            vr(), !(t.flags & 128) && (t.memoizedState = null), t.flags |= 4;
          Le(t), i = !1;
        } else
          Et !== null && (Aa(Et), Et = null), i = !0;
        if (!i)
          return t.flags & 65536 ? t : null;
      }
      return t.flags & 128 ? (t.lanes = n, t) : (r = r !== null, r !== (e !== null && e.memoizedState !== null) && r && (t.child.flags |= 8192, t.mode & 1 && (e === null || oe.current & 1 ? we === 0 && (we = 3) : Du())), t.updateQueue !== null && (t.flags |= 4), Le(t), null);
    case 4:
      return Sr(), Ra(e, t), e === null && So(t.stateNode.containerInfo), Le(t), null;
    case 10:
      return Cu(t.type._context), Le(t), null;
    case 17:
      return Ke(t.type) && Fi(), Le(t), null;
    case 19:
      if (ee(oe), i = t.memoizedState, i === null)
        return Le(t), null;
      if (r = (t.flags & 128) !== 0, l = i.rendering, l === null)
        if (r)
          Vr(i, !1);
        else {
          if (we !== 0 || e !== null && e.flags & 128)
            for (e = t.child; e !== null; ) {
              if (l = Ki(e), l !== null) {
                for (t.flags |= 128, Vr(i, !1), r = l.updateQueue, r !== null && (t.updateQueue = r, t.flags |= 4), t.subtreeFlags = 0, r = n, n = t.child; n !== null; )
                  i = n, e = r, i.flags &= 14680066, l = i.alternate, l === null ? (i.childLanes = 0, i.lanes = e, i.child = null, i.subtreeFlags = 0, i.memoizedProps = null, i.memoizedState = null, i.updateQueue = null, i.dependencies = null, i.stateNode = null) : (i.childLanes = l.childLanes, i.lanes = l.lanes, i.child = l.child, i.subtreeFlags = 0, i.deletions = null, i.memoizedProps = l.memoizedProps, i.memoizedState = l.memoizedState, i.updateQueue = l.updateQueue, i.type = l.type, e = l.dependencies, i.dependencies = e === null ? null : { lanes: e.lanes, firstContext: e.firstContext }), n = n.sibling;
                return q(oe, oe.current & 1 | 2), t.child;
              }
              e = e.sibling;
            }
          i.tail !== null && pe() > Cr && (t.flags |= 128, r = !0, Vr(i, !1), t.lanes = 4194304);
        }
      else {
        if (!r)
          if (e = Ki(l), e !== null) {
            if (t.flags |= 128, r = !0, n = e.updateQueue, n !== null && (t.updateQueue = n, t.flags |= 4), Vr(i, !0), i.tail === null && i.tailMode === "hidden" && !l.alternate && !re)
              return Le(t), null;
          } else
            2 * pe() - i.renderingStartTime > Cr && n !== 1073741824 && (t.flags |= 128, r = !0, Vr(i, !1), t.lanes = 4194304);
        i.isBackwards ? (l.sibling = t.child, t.child = l) : (n = i.last, n !== null ? n.sibling = l : t.child = l, i.last = l);
      }
      return i.tail !== null ? (t = i.tail, i.rendering = t, i.tail = t.sibling, i.renderingStartTime = pe(), t.sibling = null, n = oe.current, q(oe, r ? n & 1 | 2 : n & 1), t) : (Le(t), null);
    case 22:
    case 23:
      return bu(), r = t.memoizedState !== null, e !== null && e.memoizedState !== null !== r && (t.flags |= 8192), r && t.mode & 1 ? Xe & 1073741824 && (Le(t), t.subtreeFlags & 6 && (t.flags |= 8192)) : Le(t), null;
    case 24:
      return null;
    case 25:
      return null;
  }
  throw Error(P(156, t.tag));
}
function Cy(e, t) {
  switch (vu(t), t.tag) {
    case 1:
      return Ke(t.type) && Fi(), e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, t) : null;
    case 3:
      return Sr(), ee(Ge), ee(Ae), Pu(), e = t.flags, e & 65536 && !(e & 128) ? (t.flags = e & -65537 | 128, t) : null;
    case 5:
      return $u(t), null;
    case 13:
      if (ee(oe), e = t.memoizedState, e !== null && e.dehydrated !== null) {
        if (t.alternate === null)
          throw Error(P(340));
        vr();
      }
      return e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, t) : null;
    case 19:
      return ee(oe), null;
    case 4:
      return Sr(), null;
    case 10:
      return Cu(t.type._context), null;
    case 22:
    case 23:
      return bu(), null;
    case 24:
      return null;
    default:
      return null;
  }
}
var ai = !1, je = !1, ky = typeof WeakSet == "function" ? WeakSet : Set, M = null;
function or(e, t) {
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
function Oa(e, t, n) {
  try {
    n();
  } catch (r) {
    fe(e, t, r);
  }
}
var Cf = !1;
function Ey(e, t) {
  if (pa = ji, e = Mp(), gu(e)) {
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
  for (ma = { focusedElem: e, selectionRange: n }, ji = !1, M = t; M !== null; )
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
                  var g = y.memoizedProps, $ = y.memoizedState, m = t.stateNode, f = m.getSnapshotBeforeUpdate(t.elementType === t.type ? g : Ct(t.type, g), $);
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
function so(e, t, n) {
  var r = t.updateQueue;
  if (r = r !== null ? r.lastEffect : null, r !== null) {
    var o = r = r.next;
    do {
      if ((o.tag & e) === e) {
        var i = o.destroy;
        o.destroy = void 0, i !== void 0 && Oa(t, n, i);
      }
      o = o.next;
    } while (o !== r);
  }
}
function hl(e, t) {
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
function Ma(e) {
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
function Pm(e) {
  var t = e.alternate;
  t !== null && (e.alternate = null, Pm(t)), e.child = null, e.deletions = null, e.sibling = null, e.tag === 5 && (t = e.stateNode, t !== null && (delete t[It], delete t[Co], delete t[ya], delete t[ly], delete t[sy])), e.stateNode = null, e.return = null, e.dependencies = null, e.memoizedProps = null, e.memoizedState = null, e.pendingProps = null, e.stateNode = null, e.updateQueue = null;
}
function Tm(e) {
  return e.tag === 5 || e.tag === 3 || e.tag === 4;
}
function kf(e) {
  e:
    for (; ; ) {
      for (; e.sibling === null; ) {
        if (e.return === null || Tm(e.return))
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
function Na(e, t, n) {
  var r = e.tag;
  if (r === 5 || r === 6)
    e = e.stateNode, t ? n.nodeType === 8 ? n.parentNode.insertBefore(e, t) : n.insertBefore(e, t) : (n.nodeType === 8 ? (t = n.parentNode, t.insertBefore(e, n)) : (t = n, t.appendChild(e)), n = n._reactRootContainer, n != null || t.onclick !== null || (t.onclick = Di));
  else if (r !== 4 && (e = e.child, e !== null))
    for (Na(e, t, n), e = e.sibling; e !== null; )
      Na(e, t, n), e = e.sibling;
}
function Ia(e, t, n) {
  var r = e.tag;
  if (r === 5 || r === 6)
    e = e.stateNode, t ? n.insertBefore(e, t) : n.appendChild(e);
  else if (r !== 4 && (e = e.child, e !== null))
    for (Ia(e, t, n), e = e.sibling; e !== null; )
      Ia(e, t, n), e = e.sibling;
}
var Te = null, kt = !1;
function qt(e, t, n) {
  for (n = n.child; n !== null; )
    Rm(e, t, n), n = n.sibling;
}
function Rm(e, t, n) {
  if (Lt && typeof Lt.onCommitFiberUnmount == "function")
    try {
      Lt.onCommitFiberUnmount(sl, n);
    } catch {
    }
  switch (n.tag) {
    case 5:
      je || or(n, t);
    case 6:
      var r = Te, o = kt;
      Te = null, qt(e, t, n), Te = r, kt = o, Te !== null && (kt ? (e = Te, n = n.stateNode, e.nodeType === 8 ? e.parentNode.removeChild(n) : e.removeChild(n)) : Te.removeChild(n.stateNode));
      break;
    case 18:
      Te !== null && (kt ? (e = Te, n = n.stateNode, e.nodeType === 8 ? _s(e.parentNode, n) : e.nodeType === 1 && _s(e, n), yo(e)) : _s(Te, n.stateNode));
      break;
    case 4:
      r = Te, o = kt, Te = n.stateNode.containerInfo, kt = !0, qt(e, t, n), Te = r, kt = o;
      break;
    case 0:
    case 11:
    case 14:
    case 15:
      if (!je && (r = n.updateQueue, r !== null && (r = r.lastEffect, r !== null))) {
        o = r = r.next;
        do {
          var i = o, l = i.destroy;
          i = i.tag, l !== void 0 && (i & 2 || i & 4) && Oa(n, t, l), o = o.next;
        } while (o !== r);
      }
      qt(e, t, n);
      break;
    case 1:
      if (!je && (or(n, t), r = n.stateNode, typeof r.componentWillUnmount == "function"))
        try {
          r.props = n.memoizedProps, r.state = n.memoizedState, r.componentWillUnmount();
        } catch (s) {
          fe(n, t, s);
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
function Ef(e) {
  var t = e.updateQueue;
  if (t !== null) {
    e.updateQueue = null;
    var n = e.stateNode;
    n === null && (n = e.stateNode = new ky()), t.forEach(function(r) {
      var o = Iy.bind(null, e, r);
      n.has(r) || (n.add(r), r.then(o, o));
    });
  }
}
function wt(e, t) {
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
                Te = s.stateNode, kt = !1;
                break e;
              case 3:
                Te = s.stateNode.containerInfo, kt = !0;
                break e;
              case 4:
                Te = s.stateNode.containerInfo, kt = !0;
                break e;
            }
            s = s.return;
          }
        if (Te === null)
          throw Error(P(160));
        Rm(i, l, o), Te = null, kt = !1;
        var a = o.alternate;
        a !== null && (a.return = null), o.return = null;
      } catch (u) {
        fe(o, t, u);
      }
    }
  if (t.subtreeFlags & 12854)
    for (t = t.child; t !== null; )
      Om(t, e), t = t.sibling;
}
function Om(e, t) {
  var n = e.alternate, r = e.flags;
  switch (e.tag) {
    case 0:
    case 11:
    case 14:
    case 15:
      if (wt(t, e), Rt(e), r & 4) {
        try {
          so(3, e, e.return), hl(3, e);
        } catch (g) {
          fe(e, e.return, g);
        }
        try {
          so(5, e, e.return);
        } catch (g) {
          fe(e, e.return, g);
        }
      }
      break;
    case 1:
      wt(t, e), Rt(e), r & 512 && n !== null && or(n, n.return);
      break;
    case 5:
      if (wt(t, e), Rt(e), r & 512 && n !== null && or(n, n.return), e.flags & 32) {
        var o = e.stateNode;
        try {
          po(o, "");
        } catch (g) {
          fe(e, e.return, g);
        }
      }
      if (r & 4 && (o = e.stateNode, o != null)) {
        var i = e.memoizedProps, l = n !== null ? n.memoizedProps : i, s = e.type, a = e.updateQueue;
        if (e.updateQueue = null, a !== null)
          try {
            s === "input" && i.type === "radio" && i.name != null && qd(o, i), ra(s, l);
            var u = ra(s, i);
            for (l = 0; l < a.length; l += 2) {
              var c = a[l], d = a[l + 1];
              c === "style" ? rp(o, d) : c === "dangerouslySetInnerHTML" ? tp(o, d) : c === "children" ? po(o, d) : ru(o, c, d, u);
            }
            switch (s) {
              case "input":
                qs(o, i);
                break;
              case "textarea":
                Jd(o, i);
                break;
              case "select":
                var p = o._wrapperState.wasMultiple;
                o._wrapperState.wasMultiple = !!i.multiple;
                var v = i.value;
                v != null ? lr(o, !!i.multiple, v, !1) : p !== !!i.multiple && (i.defaultValue != null ? lr(
                  o,
                  !!i.multiple,
                  i.defaultValue,
                  !0
                ) : lr(o, !!i.multiple, i.multiple ? [] : "", !1));
            }
            o[Co] = i;
          } catch (g) {
            fe(e, e.return, g);
          }
      }
      break;
    case 6:
      if (wt(t, e), Rt(e), r & 4) {
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
      if (wt(t, e), Rt(e), r & 4 && n !== null && n.memoizedState.isDehydrated)
        try {
          yo(t.containerInfo);
        } catch (g) {
          fe(e, e.return, g);
        }
      break;
    case 4:
      wt(t, e), Rt(e);
      break;
    case 13:
      wt(t, e), Rt(e), o = e.child, o.flags & 8192 && (i = o.memoizedState !== null, o.stateNode.isHidden = i, !i || o.alternate !== null && o.alternate.memoizedState !== null || (ju = pe())), r & 4 && Ef(e);
      break;
    case 22:
      if (c = n !== null && n.memoizedState !== null, e.mode & 1 ? (je = (u = je) || c, wt(t, e), je = u) : wt(t, e), Rt(e), r & 8192) {
        if (u = e.memoizedState !== null, (e.stateNode.isHidden = u) && !c && e.mode & 1)
          for (M = e, c = e.child; c !== null; ) {
            for (d = M = c; M !== null; ) {
              switch (p = M, v = p.child, p.tag) {
                case 0:
                case 11:
                case 14:
                case 15:
                  so(4, p, p.return);
                  break;
                case 1:
                  or(p, p.return);
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
                  or(p, p.return);
                  break;
                case 22:
                  if (p.memoizedState !== null) {
                    $f(d);
                    continue;
                  }
              }
              v !== null ? (v.return = p, M = v) : $f(d);
            }
            c = c.sibling;
          }
        e:
          for (c = null, d = e; ; ) {
            if (d.tag === 5) {
              if (c === null) {
                c = d;
                try {
                  o = d.stateNode, u ? (i = o.style, typeof i.setProperty == "function" ? i.setProperty("display", "none", "important") : i.display = "none") : (s = d.stateNode, a = d.memoizedProps.style, l = a != null && a.hasOwnProperty("display") ? a.display : null, s.style.display = np("display", l));
                } catch (g) {
                  fe(e, e.return, g);
                }
              }
            } else if (d.tag === 6) {
              if (c === null)
                try {
                  d.stateNode.nodeValue = u ? "" : d.memoizedProps;
                } catch (g) {
                  fe(e, e.return, g);
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
      wt(t, e), Rt(e), r & 4 && Ef(e);
      break;
    case 21:
      break;
    default:
      wt(
        t,
        e
      ), Rt(e);
  }
}
function Rt(e) {
  var t = e.flags;
  if (t & 2) {
    try {
      e: {
        for (var n = e.return; n !== null; ) {
          if (Tm(n)) {
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
          r.flags & 32 && (po(o, ""), r.flags &= -33);
          var i = kf(e);
          Ia(e, i, o);
          break;
        case 3:
        case 4:
          var l = r.stateNode.containerInfo, s = kf(e);
          Na(e, s, l);
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
function _y(e, t, n) {
  M = e, Mm(e);
}
function Mm(e, t, n) {
  for (var r = (e.mode & 1) !== 0; M !== null; ) {
    var o = M, i = o.child;
    if (o.tag === 22 && r) {
      var l = o.memoizedState !== null || ai;
      if (!l) {
        var s = o.alternate, a = s !== null && s.memoizedState !== null || je;
        s = ai;
        var u = je;
        if (ai = l, (je = a) && !u)
          for (M = o; M !== null; )
            l = M, a = l.child, l.tag === 22 && l.memoizedState !== null ? Pf(o) : a !== null ? (a.return = l, M = a) : Pf(o);
        for (; i !== null; )
          M = i, Mm(i), i = i.sibling;
        M = o, ai = s, je = u;
      }
      _f(e);
    } else
      o.subtreeFlags & 8772 && i !== null ? (i.return = o, M = i) : _f(e);
  }
}
function _f(e) {
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
              je || hl(5, t);
              break;
            case 1:
              var r = t.stateNode;
              if (t.flags & 4 && !je)
                if (n === null)
                  r.componentDidMount();
                else {
                  var o = t.elementType === t.type ? n.memoizedProps : Ct(t.type, n.memoizedProps);
                  r.componentDidUpdate(o, n.memoizedState, r.__reactInternalSnapshotBeforeUpdate);
                }
              var i = t.updateQueue;
              i !== null && uf(t, i, r);
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
                uf(t, l, n);
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
                    d !== null && yo(d);
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
        je || t.flags & 512 && Ma(t);
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
function $f(e) {
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
function Pf(e) {
  for (; M !== null; ) {
    var t = M;
    try {
      switch (t.tag) {
        case 0:
        case 11:
        case 15:
          var n = t.return;
          try {
            hl(4, t);
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
            Ma(t);
          } catch (a) {
            fe(t, i, a);
          }
          break;
        case 5:
          var l = t.return;
          try {
            Ma(t);
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
var $y = Math.ceil, Xi = Yt.ReactCurrentDispatcher, Lu = Yt.ReactCurrentOwner, pt = Yt.ReactCurrentBatchConfig, U = 0, Ee = null, ve = null, Oe = 0, Xe = 0, ir = xn(0), we = 0, To = null, Ln = 0, gl = 0, zu = 0, ao = null, Ve = null, ju = 0, Cr = 1 / 0, bt = null, Zi = !1, La = null, pn = null, ui = !1, sn = null, qi = 0, uo = 0, za = null, ki = -1, Ei = 0;
function Be() {
  return U & 6 ? pe() : ki !== -1 ? ki : ki = pe();
}
function mn(e) {
  return e.mode & 1 ? U & 2 && Oe !== 0 ? Oe & -Oe : uy.transition !== null ? (Ei === 0 && (Ei = hp()), Ei) : (e = K, e !== 0 || (e = window.event, e = e === void 0 ? 16 : Cp(e.type)), e) : 1;
}
function $t(e, t, n, r) {
  if (50 < uo)
    throw uo = 0, za = null, Error(P(185));
  jo(e, n, r), (!(U & 2) || e !== Ee) && (e === Ee && (!(U & 2) && (gl |= n), we === 4 && rn(e, Oe)), Qe(e, r), n === 1 && U === 0 && !(t.mode & 1) && (Cr = pe() + 500, dl && Sn()));
}
function Qe(e, t) {
  var n = e.callbackNode;
  ug(e, t);
  var r = zi(e, e === Ee ? Oe : 0);
  if (r === 0)
    n !== null && zc(n), e.callbackNode = null, e.callbackPriority = 0;
  else if (t = r & -r, e.callbackPriority !== t) {
    if (n != null && zc(n), t === 1)
      e.tag === 0 ? ay(Tf.bind(null, e)) : Bp(Tf.bind(null, e)), oy(function() {
        !(U & 6) && Sn();
      }), n = null;
    else {
      switch (gp(r)) {
        case 1:
          n = au;
          break;
        case 4:
          n = pp;
          break;
        case 16:
          n = Li;
          break;
        case 536870912:
          n = mp;
          break;
        default:
          n = Li;
      }
      n = Dm(n, Nm.bind(null, e));
    }
    e.callbackPriority = t, e.callbackNode = n;
  }
}
function Nm(e, t) {
  if (ki = -1, Ei = 0, U & 6)
    throw Error(P(327));
  var n = e.callbackNode;
  if (fr() && e.callbackNode !== n)
    return null;
  var r = zi(e, e === Ee ? Oe : 0);
  if (r === 0)
    return null;
  if (r & 30 || r & e.expiredLanes || t)
    t = Ji(e, r);
  else {
    t = r;
    var o = U;
    U |= 2;
    var i = Lm();
    (Ee !== e || Oe !== t) && (bt = null, Cr = pe() + 500, Rn(e, t));
    do
      try {
        Ry();
        break;
      } catch (s) {
        Im(e, s);
      }
    while (1);
    wu(), Xi.current = i, U = o, ve !== null ? t = 0 : (Ee = null, Oe = 0, t = we);
  }
  if (t !== 0) {
    if (t === 2 && (o = aa(e), o !== 0 && (r = o, t = ja(e, o))), t === 1)
      throw n = To, Rn(e, 0), rn(e, r), Qe(e, pe()), n;
    if (t === 6)
      rn(e, r);
    else {
      if (o = e.current.alternate, !(r & 30) && !Py(o) && (t = Ji(e, r), t === 2 && (i = aa(e), i !== 0 && (r = i, t = ja(e, i))), t === 1))
        throw n = To, Rn(e, 0), rn(e, r), Qe(e, pe()), n;
      switch (e.finishedWork = o, e.finishedLanes = r, t) {
        case 0:
        case 1:
          throw Error(P(345));
        case 2:
          Cn(e, Ve, bt);
          break;
        case 3:
          if (rn(e, r), (r & 130023424) === r && (t = ju + 500 - pe(), 10 < t)) {
            if (zi(e, 0) !== 0)
              break;
            if (o = e.suspendedLanes, (o & r) !== r) {
              Be(), e.pingedLanes |= e.suspendedLanes & o;
              break;
            }
            e.timeoutHandle = ga(Cn.bind(null, e, Ve, bt), t);
            break;
          }
          Cn(e, Ve, bt);
          break;
        case 4:
          if (rn(e, r), (r & 4194240) === r)
            break;
          for (t = e.eventTimes, o = -1; 0 < r; ) {
            var l = 31 - _t(r);
            i = 1 << l, l = t[l], l > o && (o = l), r &= ~i;
          }
          if (r = o, r = pe() - r, r = (120 > r ? 120 : 480 > r ? 480 : 1080 > r ? 1080 : 1920 > r ? 1920 : 3e3 > r ? 3e3 : 4320 > r ? 4320 : 1960 * $y(r / 1960)) - r, 10 < r) {
            e.timeoutHandle = ga(Cn.bind(null, e, Ve, bt), r);
            break;
          }
          Cn(e, Ve, bt);
          break;
        case 5:
          Cn(e, Ve, bt);
          break;
        default:
          throw Error(P(329));
      }
    }
  }
  return Qe(e, pe()), e.callbackNode === n ? Nm.bind(null, e) : null;
}
function ja(e, t) {
  var n = ao;
  return e.current.memoizedState.isDehydrated && (Rn(e, t).flags |= 256), e = Ji(e, t), e !== 2 && (t = Ve, Ve = n, t !== null && Aa(t)), e;
}
function Aa(e) {
  Ve === null ? Ve = e : Ve.push.apply(Ve, e);
}
function Py(e) {
  for (var t = e; ; ) {
    if (t.flags & 16384) {
      var n = t.updateQueue;
      if (n !== null && (n = n.stores, n !== null))
        for (var r = 0; r < n.length; r++) {
          var o = n[r], i = o.getSnapshot;
          o = o.value;
          try {
            if (!Pt(i(), o))
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
  for (t &= ~zu, t &= ~gl, e.suspendedLanes |= t, e.pingedLanes &= ~t, e = e.expirationTimes; 0 < t; ) {
    var n = 31 - _t(t), r = 1 << n;
    e[n] = -1, t &= ~r;
  }
}
function Tf(e) {
  if (U & 6)
    throw Error(P(327));
  fr();
  var t = zi(e, 0);
  if (!(t & 1))
    return Qe(e, pe()), null;
  var n = Ji(e, t);
  if (e.tag !== 0 && n === 2) {
    var r = aa(e);
    r !== 0 && (t = r, n = ja(e, r));
  }
  if (n === 1)
    throw n = To, Rn(e, 0), rn(e, t), Qe(e, pe()), n;
  if (n === 6)
    throw Error(P(345));
  return e.finishedWork = e.current.alternate, e.finishedLanes = t, Cn(e, Ve, bt), Qe(e, pe()), null;
}
function Au(e, t) {
  var n = U;
  U |= 1;
  try {
    return e(t);
  } finally {
    U = n, U === 0 && (Cr = pe() + 500, dl && Sn());
  }
}
function zn(e) {
  sn !== null && sn.tag === 0 && !(U & 6) && fr();
  var t = U;
  U |= 1;
  var n = pt.transition, r = K;
  try {
    if (pt.transition = null, K = 1, e)
      return e();
  } finally {
    K = r, pt.transition = n, U = t, !(U & 6) && Sn();
  }
}
function bu() {
  Xe = ir.current, ee(ir);
}
function Rn(e, t) {
  e.finishedWork = null, e.finishedLanes = 0;
  var n = e.timeoutHandle;
  if (n !== -1 && (e.timeoutHandle = -1, ry(n)), ve !== null)
    for (n = ve.return; n !== null; ) {
      var r = n;
      switch (vu(r), r.tag) {
        case 1:
          r = r.type.childContextTypes, r != null && Fi();
          break;
        case 3:
          Sr(), ee(Ge), ee(Ae), Pu();
          break;
        case 5:
          $u(r);
          break;
        case 4:
          Sr();
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
          bu();
      }
      n = n.return;
    }
  if (Ee = e, ve = e = hn(e.current, null), Oe = Xe = t, we = 0, To = null, zu = gl = Ln = 0, Ve = ao = null, $n !== null) {
    for (t = 0; t < $n.length; t++)
      if (n = $n[t], r = n.interleaved, r !== null) {
        n.interleaved = null;
        var o = r.next, i = n.pending;
        if (i !== null) {
          var l = i.next;
          i.next = o, r.next = l;
        }
        n.pending = r;
      }
    $n = null;
  }
  return e;
}
function Im(e, t) {
  do {
    var n = ve;
    try {
      if (wu(), Si.current = Yi, Qi) {
        for (var r = ie.memoizedState; r !== null; ) {
          var o = r.queue;
          o !== null && (o.pending = null), r = r.next;
        }
        Qi = !1;
      }
      if (In = 0, ke = Se = ie = null, lo = !1, _o = 0, Lu.current = null, n === null || n.return === null) {
        we = 1, To = t, ve = null;
        break;
      }
      e: {
        var i = e, l = n.return, s = n, a = t;
        if (t = Oe, s.flags |= 32768, a !== null && typeof a == "object" && typeof a.then == "function") {
          var u = a, c = s, d = c.tag;
          if (!(c.mode & 1) && (d === 0 || d === 11 || d === 15)) {
            var p = c.alternate;
            p ? (c.updateQueue = p.updateQueue, c.memoizedState = p.memoizedState, c.lanes = p.lanes) : (c.updateQueue = null, c.memoizedState = null);
          }
          var v = hf(l);
          if (v !== null) {
            v.flags &= -257, gf(v, l, s, i, t), v.mode & 1 && mf(i, u, t), t = v, a = u;
            var y = t.updateQueue;
            if (y === null) {
              var g = /* @__PURE__ */ new Set();
              g.add(a), t.updateQueue = g;
            } else
              y.add(a);
            break e;
          } else {
            if (!(t & 1)) {
              mf(i, u, t), Du();
              break e;
            }
            a = Error(P(426));
          }
        } else if (re && s.mode & 1) {
          var $ = hf(l);
          if ($ !== null) {
            !($.flags & 65536) && ($.flags |= 256), gf($, l, s, i, t), xu(wr(a, s));
            break e;
          }
        }
        i = a = wr(a, s), we !== 4 && (we = 2), ao === null ? ao = [i] : ao.push(i), i = l;
        do {
          switch (i.tag) {
            case 3:
              i.flags |= 65536, t &= -t, i.lanes |= t;
              var m = gm(i, a, t);
              af(i, m);
              break e;
            case 1:
              s = a;
              var f = i.type, h = i.stateNode;
              if (!(i.flags & 128) && (typeof f.getDerivedStateFromError == "function" || h !== null && typeof h.componentDidCatch == "function" && (pn === null || !pn.has(h)))) {
                i.flags |= 65536, t &= -t, i.lanes |= t;
                var x = ym(i, s, t);
                af(i, x);
                break e;
              }
          }
          i = i.return;
        } while (i !== null);
      }
      jm(n);
    } catch (_) {
      t = _, ve === n && n !== null && (ve = n = n.return);
      continue;
    }
    break;
  } while (1);
}
function Lm() {
  var e = Xi.current;
  return Xi.current = Yi, e === null ? Yi : e;
}
function Du() {
  (we === 0 || we === 3 || we === 2) && (we = 4), Ee === null || !(Ln & 268435455) && !(gl & 268435455) || rn(Ee, Oe);
}
function Ji(e, t) {
  var n = U;
  U |= 2;
  var r = Lm();
  (Ee !== e || Oe !== t) && (bt = null, Rn(e, t));
  do
    try {
      Ty();
      break;
    } catch (o) {
      Im(e, o);
    }
  while (1);
  if (wu(), U = n, Xi.current = r, ve !== null)
    throw Error(P(261));
  return Ee = null, Oe = 0, we;
}
function Ty() {
  for (; ve !== null; )
    zm(ve);
}
function Ry() {
  for (; ve !== null && !eg(); )
    zm(ve);
}
function zm(e) {
  var t = bm(e.alternate, e, Xe);
  e.memoizedProps = e.pendingProps, t === null ? jm(e) : ve = t, Lu.current = null;
}
function jm(e) {
  var t = e;
  do {
    var n = t.alternate;
    if (e = t.return, t.flags & 32768) {
      if (n = Cy(n, t), n !== null) {
        n.flags &= 32767, ve = n;
        return;
      }
      if (e !== null)
        e.flags |= 32768, e.subtreeFlags = 0, e.deletions = null;
      else {
        we = 6, ve = null;
        return;
      }
    } else if (n = wy(n, t, Xe), n !== null) {
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
function Cn(e, t, n) {
  var r = K, o = pt.transition;
  try {
    pt.transition = null, K = 1, Oy(e, t, n, r);
  } finally {
    pt.transition = o, K = r;
  }
  return null;
}
function Oy(e, t, n, r) {
  do
    fr();
  while (sn !== null);
  if (U & 6)
    throw Error(P(327));
  n = e.finishedWork;
  var o = e.finishedLanes;
  if (n === null)
    return null;
  if (e.finishedWork = null, e.finishedLanes = 0, n === e.current)
    throw Error(P(177));
  e.callbackNode = null, e.callbackPriority = 0;
  var i = n.lanes | n.childLanes;
  if (cg(e, i), e === Ee && (ve = Ee = null, Oe = 0), !(n.subtreeFlags & 2064) && !(n.flags & 2064) || ui || (ui = !0, Dm(Li, function() {
    return fr(), null;
  })), i = (n.flags & 15990) !== 0, n.subtreeFlags & 15990 || i) {
    i = pt.transition, pt.transition = null;
    var l = K;
    K = 1;
    var s = U;
    U |= 4, Lu.current = null, Ey(e, n), Om(n, e), Xg(ma), ji = !!pa, ma = pa = null, e.current = n, _y(n), tg(), U = s, K = l, pt.transition = i;
  } else
    e.current = n;
  if (ui && (ui = !1, sn = e, qi = o), i = e.pendingLanes, i === 0 && (pn = null), og(n.stateNode), Qe(e, pe()), t !== null)
    for (r = e.onRecoverableError, n = 0; n < t.length; n++)
      o = t[n], r(o.value, { componentStack: o.stack, digest: o.digest });
  if (Zi)
    throw Zi = !1, e = La, La = null, e;
  return qi & 1 && e.tag !== 0 && fr(), i = e.pendingLanes, i & 1 ? e === za ? uo++ : (uo = 0, za = e) : uo = 0, Sn(), null;
}
function fr() {
  if (sn !== null) {
    var e = gp(qi), t = pt.transition, n = K;
    try {
      if (pt.transition = null, K = 16 > e ? 16 : e, sn === null)
        var r = !1;
      else {
        if (e = sn, sn = null, qi = 0, U & 6)
          throw Error(P(331));
        var o = U;
        for (U |= 4, M = e.current; M !== null; ) {
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
                      so(8, c, i);
                  }
                  var d = c.child;
                  if (d !== null)
                    d.return = c, M = d;
                  else
                    for (; M !== null; ) {
                      c = M;
                      var p = c.sibling, v = c.return;
                      if (Pm(c), c === u) {
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
                      so(9, i, i.return);
                  }
                var m = i.sibling;
                if (m !== null) {
                  m.return = i.return, M = m;
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
                        hl(9, s);
                    }
                  } catch (_) {
                    fe(s, s.return, _);
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
        if (U = o, Sn(), Lt && typeof Lt.onPostCommitFiberRoot == "function")
          try {
            Lt.onPostCommitFiberRoot(sl, e);
          } catch {
          }
        r = !0;
      }
      return r;
    } finally {
      K = n, pt.transition = t;
    }
  }
  return !1;
}
function Rf(e, t, n) {
  t = wr(n, t), t = gm(e, t, 1), e = dn(e, t, 1), t = Be(), e !== null && (jo(e, 1, t), Qe(e, t));
}
function fe(e, t, n) {
  if (e.tag === 3)
    Rf(e, e, n);
  else
    for (; t !== null; ) {
      if (t.tag === 3) {
        Rf(t, e, n);
        break;
      } else if (t.tag === 1) {
        var r = t.stateNode;
        if (typeof t.type.getDerivedStateFromError == "function" || typeof r.componentDidCatch == "function" && (pn === null || !pn.has(r))) {
          e = wr(n, e), e = ym(t, e, 1), t = dn(t, e, 1), e = Be(), t !== null && (jo(t, 1, e), Qe(t, e));
          break;
        }
      }
      t = t.return;
    }
}
function My(e, t, n) {
  var r = e.pingCache;
  r !== null && r.delete(t), t = Be(), e.pingedLanes |= e.suspendedLanes & n, Ee === e && (Oe & n) === n && (we === 4 || we === 3 && (Oe & 130023424) === Oe && 500 > pe() - ju ? Rn(e, 0) : zu |= n), Qe(e, t);
}
function Am(e, t) {
  t === 0 && (e.mode & 1 ? (t = Jo, Jo <<= 1, !(Jo & 130023424) && (Jo = 4194304)) : t = 1);
  var n = Be();
  e = Gt(e, t), e !== null && (jo(e, t, n), Qe(e, n));
}
function Ny(e) {
  var t = e.memoizedState, n = 0;
  t !== null && (n = t.retryLane), Am(e, n);
}
function Iy(e, t) {
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
  r !== null && r.delete(t), Am(e, n);
}
var bm;
bm = function(e, t, n) {
  if (e !== null)
    if (e.memoizedProps !== t.pendingProps || Ge.current)
      He = !0;
    else {
      if (!(e.lanes & n) && !(t.flags & 128))
        return He = !1, Sy(e, t, n);
      He = !!(e.flags & 131072);
    }
  else
    He = !1, re && t.flags & 1048576 && Up(t, Wi, t.index);
  switch (t.lanes = 0, t.tag) {
    case 2:
      var r = t.type;
      Ci(e, t), e = t.pendingProps;
      var o = yr(t, Ae.current);
      cr(t, n), o = Ru(null, t, r, e, o, n);
      var i = Ou();
      return t.flags |= 1, typeof o == "object" && o !== null && typeof o.render == "function" && o.$$typeof === void 0 ? (t.tag = 1, t.memoizedState = null, t.updateQueue = null, Ke(r) ? (i = !0, Bi(t)) : i = !1, t.memoizedState = o.state !== null && o.state !== void 0 ? o.state : null, Eu(t), o.updater = ml, t.stateNode = o, o._reactInternals = t, ka(t, r, e, n), t = $a(null, t, r, !0, i, n)) : (t.tag = 0, re && i && yu(t), Fe(null, t, o, n), t = t.child), t;
    case 16:
      r = t.elementType;
      e: {
        switch (Ci(e, t), e = t.pendingProps, o = r._init, r = o(r._payload), t.type = r, o = t.tag = zy(r), e = Ct(r, e), o) {
          case 0:
            t = _a(null, t, r, e, n);
            break e;
          case 1:
            t = xf(null, t, r, e, n);
            break e;
          case 11:
            t = yf(null, t, r, e, n);
            break e;
          case 14:
            t = vf(null, t, r, Ct(r.type, e), n);
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
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : Ct(r, o), _a(e, t, r, o, n);
    case 1:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : Ct(r, o), xf(e, t, r, o, n);
    case 3:
      e: {
        if (wm(t), e === null)
          throw Error(P(387));
        r = t.pendingProps, i = t.memoizedState, o = i.element, Qp(e, t), Gi(t, r, null, n);
        var l = t.memoizedState;
        if (r = l.element, i.isDehydrated)
          if (i = { element: r, isDehydrated: !1, cache: l.cache, pendingSuspenseBoundaries: l.pendingSuspenseBoundaries, transitions: l.transitions }, t.updateQueue.baseState = i, t.memoizedState = i, t.flags & 256) {
            o = wr(Error(P(423)), t), t = Sf(e, t, r, n, o);
            break e;
          } else if (r !== o) {
            o = wr(Error(P(424)), t), t = Sf(e, t, r, n, o);
            break e;
          } else
            for (Je = fn(t.stateNode.containerInfo.firstChild), et = t, re = !0, Et = null, n = Gp(t, null, r, n), t.child = n; n; )
              n.flags = n.flags & -3 | 4096, n = n.sibling;
        else {
          if (vr(), r === o) {
            t = Kt(e, t, n);
            break e;
          }
          Fe(e, t, r, n);
        }
        t = t.child;
      }
      return t;
    case 5:
      return Yp(t), e === null && Sa(t), r = t.type, o = t.pendingProps, i = e !== null ? e.memoizedProps : null, l = o.children, ha(r, o) ? l = null : i !== null && ha(r, i) && (t.flags |= 32), Sm(e, t), Fe(e, t, l, n), t.child;
    case 6:
      return e === null && Sa(t), null;
    case 13:
      return Cm(e, t, n);
    case 4:
      return _u(t, t.stateNode.containerInfo), r = t.pendingProps, e === null ? t.child = xr(t, null, r, n) : Fe(e, t, r, n), t.child;
    case 11:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : Ct(r, o), yf(e, t, r, o, n);
    case 7:
      return Fe(e, t, t.pendingProps, n), t.child;
    case 8:
      return Fe(e, t, t.pendingProps.children, n), t.child;
    case 12:
      return Fe(e, t, t.pendingProps.children, n), t.child;
    case 10:
      e: {
        if (r = t.type._context, o = t.pendingProps, i = t.memoizedProps, l = o.value, q(Vi, r._currentValue), r._currentValue = l, i !== null)
          if (Pt(i.value, l)) {
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
                    i.lanes |= n, a = i.alternate, a !== null && (a.lanes |= n), wa(
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
                l.lanes |= n, s = l.alternate, s !== null && (s.lanes |= n), wa(l, n, t), l = i.sibling;
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
      return o = t.type, r = t.pendingProps.children, cr(t, n), o = mt(o), r = r(o), t.flags |= 1, Fe(e, t, r, n), t.child;
    case 14:
      return r = t.type, o = Ct(r, t.pendingProps), o = Ct(r.type, o), vf(e, t, r, o, n);
    case 15:
      return vm(e, t, t.type, t.pendingProps, n);
    case 17:
      return r = t.type, o = t.pendingProps, o = t.elementType === r ? o : Ct(r, o), Ci(e, t), t.tag = 1, Ke(r) ? (e = !0, Bi(t)) : e = !1, cr(t, n), hm(t, r, o), ka(t, r, o, n), $a(null, t, r, !0, e, n);
    case 19:
      return km(e, t, n);
    case 22:
      return xm(e, t, n);
  }
  throw Error(P(156, t.tag));
};
function Dm(e, t) {
  return dp(e, t);
}
function Ly(e, t, n, r) {
  this.tag = e, this.key = n, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.ref = null, this.pendingProps = t, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = r, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
}
function ft(e, t, n, r) {
  return new Ly(e, t, n, r);
}
function Fu(e) {
  return e = e.prototype, !(!e || !e.isReactComponent);
}
function zy(e) {
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
function hn(e, t) {
  var n = e.alternate;
  return n === null ? (n = ft(e.tag, t, e.key, e.mode), n.elementType = e.elementType, n.type = e.type, n.stateNode = e.stateNode, n.alternate = e, e.alternate = n) : (n.pendingProps = t, n.type = e.type, n.flags = 0, n.subtreeFlags = 0, n.deletions = null), n.flags = e.flags & 14680064, n.childLanes = e.childLanes, n.lanes = e.lanes, n.child = e.child, n.memoizedProps = e.memoizedProps, n.memoizedState = e.memoizedState, n.updateQueue = e.updateQueue, t = e.dependencies, n.dependencies = t === null ? null : { lanes: t.lanes, firstContext: t.firstContext }, n.sibling = e.sibling, n.index = e.index, n.ref = e.ref, n;
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
        case Yn:
          return On(n.children, o, i, t);
        case ou:
          l = 8, o |= 8;
          break;
        case Ks:
          return e = ft(12, n, t, o | 2), e.elementType = Ks, e.lanes = i, e;
        case Qs:
          return e = ft(13, n, t, o), e.elementType = Qs, e.lanes = i, e;
        case Ys:
          return e = ft(19, n, t, o), e.elementType = Ys, e.lanes = i, e;
        case Yd:
          return yl(n, o, i, t);
        default:
          if (typeof e == "object" && e !== null)
            switch (e.$$typeof) {
              case Kd:
                l = 10;
                break e;
              case Qd:
                l = 9;
                break e;
              case iu:
                l = 11;
                break e;
              case lu:
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
function On(e, t, n, r) {
  return e = ft(7, e, r, t), e.lanes = n, e;
}
function yl(e, t, n, r) {
  return e = ft(22, e, r, t), e.elementType = Yd, e.lanes = n, e.stateNode = { isHidden: !1 }, e;
}
function Is(e, t, n) {
  return e = ft(6, e, null, t), e.lanes = n, e;
}
function Ls(e, t, n) {
  return t = ft(4, e.children !== null ? e.children : [], e.key, t), t.lanes = n, t.stateNode = { containerInfo: e.containerInfo, pendingChildren: null, implementation: e.implementation }, t;
}
function jy(e, t, n, r, o) {
  this.tag = t, this.containerInfo = e, this.finishedWork = this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.pendingContext = this.context = null, this.callbackPriority = 0, this.eventTimes = ms(0), this.expirationTimes = ms(-1), this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = ms(0), this.identifierPrefix = r, this.onRecoverableError = o, this.mutableSourceEagerHydrationData = null;
}
function Bu(e, t, n, r, o, i, l, s, a) {
  return e = new jy(e, t, n, s, a), t === 1 ? (t = 1, i === !0 && (t |= 8)) : t = 0, i = ft(3, null, null, t), e.current = i, i.stateNode = e, i.memoizedState = { element: r, isDehydrated: n, cache: null, transitions: null, pendingSuspenseBoundaries: null }, Eu(i), e;
}
function Ay(e, t, n) {
  var r = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
  return { $$typeof: Qn, key: r == null ? null : "" + r, children: e, containerInfo: t, implementation: n };
}
function Fm(e) {
  if (!e)
    return yn;
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
      return Fp(e, n, t);
  }
  return t;
}
function Bm(e, t, n, r, o, i, l, s, a) {
  return e = Bu(n, r, !0, e, o, i, l, s, a), e.context = Fm(null), n = e.current, r = Be(), o = mn(n), i = Wt(r, o), i.callback = t ?? null, dn(n, i, o), e.current.lanes = o, jo(e, o, r), Qe(e, r), e;
}
function vl(e, t, n, r) {
  var o = t.current, i = Be(), l = mn(o);
  return n = Fm(n), t.context === null ? t.context = n : t.pendingContext = n, t = Wt(i, l), t.payload = { element: e }, r = r === void 0 ? null : r, r !== null && (t.callback = r), e = dn(o, t, l), e !== null && ($t(e, o, l, i), xi(e, o, l)), l;
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
function Of(e, t) {
  if (e = e.memoizedState, e !== null && e.dehydrated !== null) {
    var n = e.retryLane;
    e.retryLane = n !== 0 && n < t ? n : t;
  }
}
function Uu(e, t) {
  Of(e, t), (e = e.alternate) && Of(e, t);
}
function by() {
  return null;
}
var Um = typeof reportError == "function" ? reportError : function(e) {
  console.error(e);
};
function Wu(e) {
  this._internalRoot = e;
}
xl.prototype.render = Wu.prototype.render = function(e) {
  var t = this._internalRoot;
  if (t === null)
    throw Error(P(409));
  vl(e, t, null, null);
};
xl.prototype.unmount = Wu.prototype.unmount = function() {
  var e = this._internalRoot;
  if (e !== null) {
    this._internalRoot = null;
    var t = e.containerInfo;
    zn(function() {
      vl(null, e, null, null);
    }), t[Ht] = null;
  }
};
function xl(e) {
  this._internalRoot = e;
}
xl.prototype.unstable_scheduleHydration = function(e) {
  if (e) {
    var t = xp();
    e = { blockedOn: null, target: e, priority: t };
    for (var n = 0; n < nn.length && t !== 0 && t < nn[n].priority; n++)
      ;
    nn.splice(n, 0, e), n === 0 && wp(e);
  }
};
function Vu(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11);
}
function Sl(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11 && (e.nodeType !== 8 || e.nodeValue !== " react-mount-point-unstable "));
}
function Mf() {
}
function Dy(e, t, n, r, o) {
  if (o) {
    if (typeof r == "function") {
      var i = r;
      r = function() {
        var u = el(l);
        i.call(u);
      };
    }
    var l = Bm(t, r, e, 0, null, !1, !1, "", Mf);
    return e._reactRootContainer = l, e[Ht] = l.current, So(e.nodeType === 8 ? e.parentNode : e), zn(), l;
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
  var a = Bu(e, 0, !1, null, null, !1, !1, "", Mf);
  return e._reactRootContainer = a, e[Ht] = a.current, So(e.nodeType === 8 ? e.parentNode : e), zn(function() {
    vl(t, a, n, r);
  }), a;
}
function wl(e, t, n, r, o) {
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
    vl(t, l, e, o);
  } else
    l = Dy(n, t, e, o, r);
  return el(l);
}
yp = function(e) {
  switch (e.tag) {
    case 3:
      var t = e.stateNode;
      if (t.current.memoizedState.isDehydrated) {
        var n = Zr(t.pendingLanes);
        n !== 0 && (uu(t, n | 1), Qe(t, pe()), !(U & 6) && (Cr = pe() + 500, Sn()));
      }
      break;
    case 13:
      zn(function() {
        var r = Gt(e, 1);
        if (r !== null) {
          var o = Be();
          $t(r, e, 1, o);
        }
      }), Uu(e, 1);
  }
};
cu = function(e) {
  if (e.tag === 13) {
    var t = Gt(e, 134217728);
    if (t !== null) {
      var n = Be();
      $t(t, e, 134217728, n);
    }
    Uu(e, 134217728);
  }
};
vp = function(e) {
  if (e.tag === 13) {
    var t = mn(e), n = Gt(e, t);
    if (n !== null) {
      var r = Be();
      $t(n, e, t, r);
    }
    Uu(e, t);
  }
};
xp = function() {
  return K;
};
Sp = function(e, t) {
  var n = K;
  try {
    return K = e, t();
  } finally {
    K = n;
  }
};
ia = function(e, t, n) {
  switch (t) {
    case "input":
      if (qs(e, n), t = n.name, n.type === "radio" && t != null) {
        for (n = e; n.parentNode; )
          n = n.parentNode;
        for (n = n.querySelectorAll("input[name=" + JSON.stringify("" + t) + '][type="radio"]'), t = 0; t < n.length; t++) {
          var r = n[t];
          if (r !== e && r.form === e.form) {
            var o = fl(r);
            if (!o)
              throw Error(P(90));
            Zd(r), qs(r, o);
          }
        }
      }
      break;
    case "textarea":
      Jd(e, n);
      break;
    case "select":
      t = n.value, t != null && lr(e, !!n.multiple, t, !1);
  }
};
lp = Au;
sp = zn;
var Fy = { usingClientEntryPoint: !1, Events: [bo, Jn, fl, op, ip, Au] }, Hr = { findFiberByHostInstance: _n, bundleType: 0, version: "18.3.1", rendererPackageName: "react-dom" }, By = { bundleType: Hr.bundleType, version: Hr.version, rendererPackageName: Hr.rendererPackageName, rendererConfig: Hr.rendererConfig, overrideHookState: null, overrideHookStateDeletePath: null, overrideHookStateRenamePath: null, overrideProps: null, overridePropsDeletePath: null, overridePropsRenamePath: null, setErrorHandler: null, setSuspenseHandler: null, scheduleUpdate: null, currentDispatcherRef: Yt.ReactCurrentDispatcher, findHostInstanceByFiber: function(e) {
  return e = cp(e), e === null ? null : e.stateNode;
}, findFiberByHostInstance: Hr.findFiberByHostInstance || by, findHostInstancesForRefresh: null, scheduleRefresh: null, scheduleRoot: null, setRefreshHandler: null, getCurrentFiber: null, reconcilerVersion: "18.3.1-next-f1338f8080-20240426" };
if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u") {
  var ci = __REACT_DEVTOOLS_GLOBAL_HOOK__;
  if (!ci.isDisabled && ci.supportsFiber)
    try {
      sl = ci.inject(By), Lt = ci;
    } catch {
    }
}
rt.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = Fy;
rt.createPortal = function(e, t) {
  var n = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
  if (!Vu(t))
    throw Error(P(200));
  return Ay(e, t, null, n);
};
rt.createRoot = function(e, t) {
  if (!Vu(e))
    throw Error(P(299));
  var n = !1, r = "", o = Um;
  return t != null && (t.unstable_strictMode === !0 && (n = !0), t.identifierPrefix !== void 0 && (r = t.identifierPrefix), t.onRecoverableError !== void 0 && (o = t.onRecoverableError)), t = Bu(e, 1, !1, null, null, n, !1, r, o), e[Ht] = t.current, So(e.nodeType === 8 ? e.parentNode : e), new Wu(t);
};
rt.findDOMNode = function(e) {
  if (e == null)
    return null;
  if (e.nodeType === 1)
    return e;
  var t = e._reactInternals;
  if (t === void 0)
    throw typeof e.render == "function" ? Error(P(188)) : (e = Object.keys(e).join(","), Error(P(268, e)));
  return e = cp(t), e = e === null ? null : e.stateNode, e;
};
rt.flushSync = function(e) {
  return zn(e);
};
rt.hydrate = function(e, t, n) {
  if (!Sl(t))
    throw Error(P(200));
  return wl(null, e, t, !0, n);
};
rt.hydrateRoot = function(e, t, n) {
  if (!Vu(e))
    throw Error(P(405));
  var r = n != null && n.hydratedSources || null, o = !1, i = "", l = Um;
  if (n != null && (n.unstable_strictMode === !0 && (o = !0), n.identifierPrefix !== void 0 && (i = n.identifierPrefix), n.onRecoverableError !== void 0 && (l = n.onRecoverableError)), t = Bm(t, null, e, 1, n ?? null, o, !1, i, l), e[Ht] = t.current, So(e), r)
    for (e = 0; e < r.length; e++)
      n = r[e], o = n._getVersion, o = o(n._source), t.mutableSourceEagerHydrationData == null ? t.mutableSourceEagerHydrationData = [n, o] : t.mutableSourceEagerHydrationData.push(
        n,
        o
      );
  return new xl(t);
};
rt.render = function(e, t, n) {
  if (!Sl(t))
    throw Error(P(200));
  return wl(null, e, t, !1, n);
};
rt.unmountComponentAtNode = function(e) {
  if (!Sl(e))
    throw Error(P(40));
  return e._reactRootContainer ? (zn(function() {
    wl(null, null, e, !1, function() {
      e._reactRootContainer = null, e[Ht] = null;
    });
  }), !0) : !1;
};
rt.unstable_batchedUpdates = Au;
rt.unstable_renderSubtreeIntoContainer = function(e, t, n, r) {
  if (!Sl(n))
    throw Error(P(200));
  if (e == null || e._reactInternals === void 0)
    throw Error(P(38));
  return wl(e, t, n, !1, r);
};
rt.version = "18.3.1-next-f1338f8080-20240426";
function Wm() {
  if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function"))
    try {
      __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(Wm);
    } catch (e) {
      console.error(e);
    }
}
Wm(), Wd.exports = rt;
var Vm = Wd.exports;
const fi = /* @__PURE__ */ Md(Vm);
var Nf = Vm;
Hs.createRoot = Nf.createRoot, Hs.hydrateRoot = Nf.hydrateRoot;
function Ro(e) {
  let t = "https://mui.com/production-error/?code=" + e;
  for (let n = 1; n < arguments.length; n += 1)
    t += "&args[]=" + encodeURIComponent(arguments[n]);
  return "Minified MUI error #" + e + "; visit " + t + " for the full message.";
}
const Uy = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Ro
}, Symbol.toStringTag, { value: "Module" })), kr = "$$material";
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
var Wy = !1;
function Vy(e) {
  if (e.sheet)
    return e.sheet;
  for (var t = 0; t < document.styleSheets.length; t++)
    if (document.styleSheets[t].ownerNode === e)
      return document.styleSheets[t];
}
function Hy(e) {
  var t = document.createElement("style");
  return t.setAttribute("data-emotion", e.key), e.nonce !== void 0 && t.setAttribute("nonce", e.nonce), t.appendChild(document.createTextNode("")), t.setAttribute("data-s", ""), t;
}
var Gy = /* @__PURE__ */ function() {
  function e(n) {
    var r = this;
    this._insertTag = function(o) {
      var i;
      r.tags.length === 0 ? r.insertionPoint ? i = r.insertionPoint.nextSibling : r.prepend ? i = r.container.firstChild : i = r.before : i = r.tags[r.tags.length - 1].nextSibling, r.container.insertBefore(o, i), r.tags.push(o);
    }, this.isSpeedy = n.speedy === void 0 ? !Wy : n.speedy, this.tags = [], this.ctr = 0, this.nonce = n.nonce, this.key = n.key, this.container = n.container, this.prepend = n.prepend, this.insertionPoint = n.insertionPoint, this.before = null;
  }
  var t = e.prototype;
  return t.hydrate = function(r) {
    r.forEach(this._insertTag);
  }, t.insert = function(r) {
    this.ctr % (this.isSpeedy ? 65e3 : 1) === 0 && this._insertTag(Hy(this));
    var o = this.tags[this.tags.length - 1];
    if (this.isSpeedy) {
      var i = Vy(o);
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
}(), ze = "-ms-", tl = "-moz-", V = "-webkit-", Hm = "comm", Hu = "rule", Gu = "decl", Ky = "@import", Gm = "@keyframes", Qy = "@layer", Yy = Math.abs, Cl = String.fromCharCode, Xy = Object.assign;
function Zy(e, t) {
  return Re(e, 0) ^ 45 ? (((t << 2 ^ Re(e, 0)) << 2 ^ Re(e, 1)) << 2 ^ Re(e, 2)) << 2 ^ Re(e, 3) : 0;
}
function Km(e) {
  return e.trim();
}
function qy(e, t) {
  return (e = t.exec(e)) ? e[0] : e;
}
function H(e, t, n) {
  return e.replace(t, n);
}
function ba(e, t) {
  return e.indexOf(t);
}
function Re(e, t) {
  return e.charCodeAt(t) | 0;
}
function Oo(e, t, n) {
  return e.slice(t, n);
}
function Mt(e) {
  return e.length;
}
function Ku(e) {
  return e.length;
}
function di(e, t) {
  return t.push(e), e;
}
function Jy(e, t) {
  return e.map(t).join("");
}
var kl = 1, Er = 1, Qm = 0, Ye = 0, ye = 0, Mr = "";
function El(e, t, n, r, o, i, l) {
  return { value: e, root: t, parent: n, type: r, props: o, children: i, line: kl, column: Er, length: l, return: "" };
}
function Gr(e, t) {
  return Xy(El("", null, null, "", null, null, 0), e, { length: -e.length }, t);
}
function ev() {
  return ye;
}
function tv() {
  return ye = Ye > 0 ? Re(Mr, --Ye) : 0, Er--, ye === 10 && (Er = 1, kl--), ye;
}
function tt() {
  return ye = Ye < Qm ? Re(Mr, Ye++) : 0, Er++, ye === 10 && (Er = 1, kl++), ye;
}
function jt() {
  return Re(Mr, Ye);
}
function $i() {
  return Ye;
}
function Fo(e, t) {
  return Oo(Mr, e, t);
}
function Mo(e) {
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
function Ym(e) {
  return kl = Er = 1, Qm = Mt(Mr = e), Ye = 0, [];
}
function Xm(e) {
  return Mr = "", e;
}
function Pi(e) {
  return Km(Fo(Ye - 1, Da(e === 91 ? e + 2 : e === 40 ? e + 1 : e)));
}
function nv(e) {
  for (; (ye = jt()) && ye < 33; )
    tt();
  return Mo(e) > 2 || Mo(ye) > 3 ? "" : " ";
}
function rv(e, t) {
  for (; --t && tt() && !(ye < 48 || ye > 102 || ye > 57 && ye < 65 || ye > 70 && ye < 97); )
    ;
  return Fo(e, $i() + (t < 6 && jt() == 32 && tt() == 32));
}
function Da(e) {
  for (; tt(); )
    switch (ye) {
      case e:
        return Ye;
      case 34:
      case 39:
        e !== 34 && e !== 39 && Da(ye);
        break;
      case 40:
        e === 41 && Da(e);
        break;
      case 92:
        tt();
        break;
    }
  return Ye;
}
function ov(e, t) {
  for (; tt() && e + ye !== 47 + 10; )
    if (e + ye === 42 + 42 && jt() === 47)
      break;
  return "/*" + Fo(t, Ye - 1) + "*" + Cl(e === 47 ? e : tt());
}
function iv(e) {
  for (; !Mo(jt()); )
    tt();
  return Fo(e, Ye);
}
function lv(e) {
  return Xm(Ti("", null, null, null, [""], e = Ym(e), 0, [0], e));
}
function Ti(e, t, n, r, o, i, l, s, a) {
  for (var u = 0, c = 0, d = l, p = 0, v = 0, y = 0, g = 1, $ = 1, m = 1, f = 0, h = "", x = o, _ = i, E = r, C = h; $; )
    switch (y = f, f = tt()) {
      case 40:
        if (y != 108 && Re(C, d - 1) == 58) {
          ba(C += H(Pi(f), "&", "&\f"), "&\f") != -1 && (m = -1);
          break;
        }
      case 34:
      case 39:
      case 91:
        C += Pi(f);
        break;
      case 9:
      case 10:
      case 13:
      case 32:
        C += nv(y);
        break;
      case 92:
        C += rv($i() - 1, 7);
        continue;
      case 47:
        switch (jt()) {
          case 42:
          case 47:
            di(sv(ov(tt(), $i()), t, n), a);
            break;
          default:
            C += "/";
        }
        break;
      case 123 * g:
        s[u++] = Mt(C) * m;
      case 125 * g:
      case 59:
      case 0:
        switch (f) {
          case 0:
          case 125:
            $ = 0;
          case 59 + c:
            m == -1 && (C = H(C, /\f/g, "")), v > 0 && Mt(C) - d && di(v > 32 ? Lf(C + ";", r, n, d - 1) : Lf(H(C, " ", "") + ";", r, n, d - 2), a);
            break;
          case 59:
            C += ";";
          default:
            if (di(E = If(C, t, n, u, c, o, s, h, x = [], _ = [], d), i), f === 123)
              if (c === 0)
                Ti(C, t, E, E, x, i, d, s, _);
              else
                switch (p === 99 && Re(C, 3) === 110 ? 100 : p) {
                  case 100:
                  case 108:
                  case 109:
                  case 115:
                    Ti(e, E, E, r && di(If(e, E, E, 0, 0, o, s, h, o, x = [], d), _), o, _, d, s, r ? x : _);
                    break;
                  default:
                    Ti(C, E, E, E, [""], _, 0, s, _);
                }
        }
        u = c = v = 0, g = m = 1, h = C = "", d = l;
        break;
      case 58:
        d = 1 + Mt(C), v = y;
      default:
        if (g < 1) {
          if (f == 123)
            --g;
          else if (f == 125 && g++ == 0 && tv() == 125)
            continue;
        }
        switch (C += Cl(f), f * g) {
          case 38:
            m = c > 0 ? 1 : (C += "\f", -1);
            break;
          case 44:
            s[u++] = (Mt(C) - 1) * m, m = 1;
            break;
          case 64:
            jt() === 45 && (C += Pi(tt())), p = jt(), c = d = Mt(h = C += iv($i())), f++;
            break;
          case 45:
            y === 45 && Mt(C) == 2 && (g = 0);
        }
    }
  return i;
}
function If(e, t, n, r, o, i, l, s, a, u, c) {
  for (var d = o - 1, p = o === 0 ? i : [""], v = Ku(p), y = 0, g = 0, $ = 0; y < r; ++y)
    for (var m = 0, f = Oo(e, d + 1, d = Yy(g = l[y])), h = e; m < v; ++m)
      (h = Km(g > 0 ? p[m] + " " + f : H(f, /&\f/g, p[m]))) && (a[$++] = h);
  return El(e, t, n, o === 0 ? Hu : s, a, u, c);
}
function sv(e, t, n) {
  return El(e, t, n, Hm, Cl(ev()), Oo(e, 2, -2), 0);
}
function Lf(e, t, n, r) {
  return El(e, t, n, Gu, Oo(e, 0, r), Oo(e, r + 1, -1), r);
}
function dr(e, t) {
  for (var n = "", r = Ku(e), o = 0; o < r; o++)
    n += t(e[o], o, e, t) || "";
  return n;
}
function av(e, t, n, r) {
  switch (e.type) {
    case Qy:
      if (e.children.length)
        break;
    case Ky:
    case Gu:
      return e.return = e.return || e.value;
    case Hm:
      return "";
    case Gm:
      return e.return = e.value + "{" + dr(e.children, r) + "}";
    case Hu:
      e.value = e.props.join(",");
  }
  return Mt(n = dr(e.children, r)) ? e.return = e.value + "{" + n + "}" : "";
}
function uv(e) {
  var t = Ku(e);
  return function(n, r, o, i) {
    for (var l = "", s = 0; s < t; s++)
      l += e[s](n, r, o, i) || "";
    return l;
  };
}
function cv(e) {
  return function(t) {
    t.root || (t = t.return) && e(t);
  };
}
function Zm(e) {
  var t = /* @__PURE__ */ Object.create(null);
  return function(n) {
    return t[n] === void 0 && (t[n] = e(n)), t[n];
  };
}
var fv = function(t, n, r) {
  for (var o = 0, i = 0; o = i, i = jt(), o === 38 && i === 12 && (n[r] = 1), !Mo(i); )
    tt();
  return Fo(t, Ye);
}, dv = function(t, n) {
  var r = -1, o = 44;
  do
    switch (Mo(o)) {
      case 0:
        o === 38 && jt() === 12 && (n[r] = 1), t[r] += fv(Ye - 1, n, r);
        break;
      case 2:
        t[r] += Pi(o);
        break;
      case 4:
        if (o === 44) {
          t[++r] = jt() === 58 ? "&\f" : "", n[r] = t[r].length;
          break;
        }
      default:
        t[r] += Cl(o);
    }
  while (o = tt());
  return t;
}, pv = function(t, n) {
  return Xm(dv(Ym(t), n));
}, zf = /* @__PURE__ */ new WeakMap(), mv = function(t) {
  if (!(t.type !== "rule" || !t.parent || // positive .length indicates that this rule contains pseudo
  // negative .length indicates that this rule has been already prefixed
  t.length < 1)) {
    for (var n = t.value, r = t.parent, o = t.column === r.column && t.line === r.line; r.type !== "rule"; )
      if (r = r.parent, !r)
        return;
    if (!(t.props.length === 1 && n.charCodeAt(0) !== 58 && !zf.get(r)) && !o) {
      zf.set(t, !0);
      for (var i = [], l = pv(n, i), s = r.props, a = 0, u = 0; a < l.length; a++)
        for (var c = 0; c < s.length; c++, u++)
          t.props[u] = i[a] ? l[a].replace(/&\f/g, s[c]) : s[c] + " " + l[a];
    }
  }
}, hv = function(t) {
  if (t.type === "decl") {
    var n = t.value;
    // charcode for l
    n.charCodeAt(0) === 108 && // charcode for b
    n.charCodeAt(2) === 98 && (t.return = "", t.value = "");
  }
};
function qm(e, t) {
  switch (Zy(e, t)) {
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
      if (Mt(e) - 1 - t > 6)
        switch (Re(e, t + 1)) {
          case 109:
            if (Re(e, t + 4) !== 45)
              break;
          case 102:
            return H(e, /(.+:)(.+)-([^]+)/, "$1" + V + "$2-$3$1" + tl + (Re(e, t + 3) == 108 ? "$3" : "$2-$3")) + e;
          case 115:
            return ~ba(e, "stretch") ? qm(H(e, "stretch", "fill-available"), t) + e : e;
        }
      break;
    case 4949:
      if (Re(e, t + 1) !== 115)
        break;
    case 6444:
      switch (Re(e, Mt(e) - 3 - (~ba(e, "!important") && 10))) {
        case 107:
          return H(e, ":", ":" + V) + e;
        case 101:
          return H(e, /(.+:)([^;!]+)(;|!.+)?/, "$1" + V + (Re(e, 14) === 45 ? "inline-" : "") + "box$3$1" + V + "$2$3$1" + ze + "$2box$3") + e;
      }
      break;
    case 5936:
      switch (Re(e, t + 11)) {
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
var gv = function(t, n, r, o) {
  if (t.length > -1 && !t.return)
    switch (t.type) {
      case Gu:
        t.return = qm(t.value, t.length);
        break;
      case Gm:
        return dr([Gr(t, {
          value: H(t.value, "@", "@" + V)
        })], o);
      case Hu:
        if (t.length)
          return Jy(t.props, function(i) {
            switch (qy(i, /(::plac\w+|:read-\w+)/)) {
              case ":read-only":
              case ":read-write":
                return dr([Gr(t, {
                  props: [H(i, /:(read-\w+)/, ":" + tl + "$1")]
                })], o);
              case "::placeholder":
                return dr([Gr(t, {
                  props: [H(i, /:(plac\w+)/, ":" + V + "input-$1")]
                }), Gr(t, {
                  props: [H(i, /:(plac\w+)/, ":" + tl + "$1")]
                }), Gr(t, {
                  props: [H(i, /:(plac\w+)/, ze + "input-$1")]
                })], o);
            }
            return "";
          });
    }
}, yv = [gv], Jm = function(t) {
  var n = t.key;
  if (n === "css") {
    var r = document.querySelectorAll("style[data-emotion]:not([data-s])");
    Array.prototype.forEach.call(r, function(g) {
      var $ = g.getAttribute("data-emotion");
      $.indexOf(" ") !== -1 && (document.head.appendChild(g), g.setAttribute("data-s", ""));
    });
  }
  var o = t.stylisPlugins || yv, i = {}, l, s = [];
  l = t.container || document.head, Array.prototype.forEach.call(
    // this means we will ignore elements which don't have a space in them which
    // means that the style elements we're looking at are only Emotion 11 server-rendered style elements
    document.querySelectorAll('style[data-emotion^="' + n + ' "]'),
    function(g) {
      for (var $ = g.getAttribute("data-emotion").split(" "), m = 1; m < $.length; m++)
        i[$[m]] = !0;
      s.push(g);
    }
  );
  var a, u = [mv, hv];
  {
    var c, d = [av, cv(function(g) {
      c.insert(g);
    })], p = uv(u.concat(o, d)), v = function($) {
      return dr(lv($), p);
    };
    a = function($, m, f, h) {
      c = f, v($ ? $ + "{" + m.styles + "}" : m.styles), h && (y.inserted[m.name] = !0);
    };
  }
  var y = {
    key: n,
    sheet: new Gy({
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
}, eh = { exports: {} }, Q = {};
/** @license React v16.13.1
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var _e = typeof Symbol == "function" && Symbol.for, Qu = _e ? Symbol.for("react.element") : 60103, Yu = _e ? Symbol.for("react.portal") : 60106, _l = _e ? Symbol.for("react.fragment") : 60107, $l = _e ? Symbol.for("react.strict_mode") : 60108, Pl = _e ? Symbol.for("react.profiler") : 60114, Tl = _e ? Symbol.for("react.provider") : 60109, Rl = _e ? Symbol.for("react.context") : 60110, Xu = _e ? Symbol.for("react.async_mode") : 60111, Ol = _e ? Symbol.for("react.concurrent_mode") : 60111, Ml = _e ? Symbol.for("react.forward_ref") : 60112, Nl = _e ? Symbol.for("react.suspense") : 60113, vv = _e ? Symbol.for("react.suspense_list") : 60120, Il = _e ? Symbol.for("react.memo") : 60115, Ll = _e ? Symbol.for("react.lazy") : 60116, xv = _e ? Symbol.for("react.block") : 60121, Sv = _e ? Symbol.for("react.fundamental") : 60117, wv = _e ? Symbol.for("react.responder") : 60118, Cv = _e ? Symbol.for("react.scope") : 60119;
function it(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Qu:
        switch (e = e.type, e) {
          case Xu:
          case Ol:
          case _l:
          case Pl:
          case $l:
          case Nl:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Rl:
              case Ml:
              case Ll:
              case Il:
              case Tl:
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
function th(e) {
  return it(e) === Ol;
}
Q.AsyncMode = Xu;
Q.ConcurrentMode = Ol;
Q.ContextConsumer = Rl;
Q.ContextProvider = Tl;
Q.Element = Qu;
Q.ForwardRef = Ml;
Q.Fragment = _l;
Q.Lazy = Ll;
Q.Memo = Il;
Q.Portal = Yu;
Q.Profiler = Pl;
Q.StrictMode = $l;
Q.Suspense = Nl;
Q.isAsyncMode = function(e) {
  return th(e) || it(e) === Xu;
};
Q.isConcurrentMode = th;
Q.isContextConsumer = function(e) {
  return it(e) === Rl;
};
Q.isContextProvider = function(e) {
  return it(e) === Tl;
};
Q.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Qu;
};
Q.isForwardRef = function(e) {
  return it(e) === Ml;
};
Q.isFragment = function(e) {
  return it(e) === _l;
};
Q.isLazy = function(e) {
  return it(e) === Ll;
};
Q.isMemo = function(e) {
  return it(e) === Il;
};
Q.isPortal = function(e) {
  return it(e) === Yu;
};
Q.isProfiler = function(e) {
  return it(e) === Pl;
};
Q.isStrictMode = function(e) {
  return it(e) === $l;
};
Q.isSuspense = function(e) {
  return it(e) === Nl;
};
Q.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === _l || e === Ol || e === Pl || e === $l || e === Nl || e === vv || typeof e == "object" && e !== null && (e.$$typeof === Ll || e.$$typeof === Il || e.$$typeof === Tl || e.$$typeof === Rl || e.$$typeof === Ml || e.$$typeof === Sv || e.$$typeof === wv || e.$$typeof === Cv || e.$$typeof === xv);
};
Q.typeOf = it;
eh.exports = Q;
var kv = eh.exports, nh = kv, Ev = {
  $$typeof: !0,
  render: !0,
  defaultProps: !0,
  displayName: !0,
  propTypes: !0
}, _v = {
  $$typeof: !0,
  compare: !0,
  defaultProps: !0,
  displayName: !0,
  propTypes: !0,
  type: !0
}, rh = {};
rh[nh.ForwardRef] = Ev;
rh[nh.Memo] = _v;
var $v = !0;
function oh(e, t, n) {
  var r = "";
  return n.split(" ").forEach(function(o) {
    e[o] !== void 0 ? t.push(e[o] + ";") : o && (r += o + " ");
  }), r;
}
var Zu = function(t, n, r) {
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
  $v === !1) && t.registered[o] === void 0 && (t.registered[o] = n.styles);
}, qu = function(t, n, r) {
  Zu(t, n, r);
  var o = t.key + "-" + n.name;
  if (t.inserted[n.name] === void 0) {
    var i = n;
    do
      t.insert(n === i ? "." + o : "", i, t.sheet, !0), i = i.next;
    while (i !== void 0);
  }
};
function Pv(e) {
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
var Tv = {
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
}, Rv = !1, Ov = /[A-Z]|^ms/g, Mv = /_EMO_([^_]+?)_([^]*?)_EMO_/g, ih = function(t) {
  return t.charCodeAt(1) === 45;
}, jf = function(t) {
  return t != null && typeof t != "boolean";
}, zs = /* @__PURE__ */ Zm(function(e) {
  return ih(e) ? e : e.replace(Ov, "-$&").toLowerCase();
}), Af = function(t, n) {
  switch (t) {
    case "animation":
    case "animationName":
      if (typeof n == "string")
        return n.replace(Mv, function(r, o, i) {
          return Nt = {
            name: o,
            styles: i,
            next: Nt
          }, o;
        });
  }
  return Tv[t] !== 1 && !ih(t) && typeof n == "number" && n !== 0 ? n + "px" : n;
}, Nv = "Component selectors can only be used in conjunction with @emotion/babel-plugin, the swc Emotion plugin, or another Emotion-aware compiler transform.";
function No(e, t, n) {
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
        return Nt = {
          name: o.name,
          styles: o.styles,
          next: Nt
        }, o.name;
      var i = n;
      if (i.styles !== void 0) {
        var l = i.next;
        if (l !== void 0)
          for (; l !== void 0; )
            Nt = {
              name: l.name,
              styles: l.styles,
              next: Nt
            }, l = l.next;
        var s = i.styles + ";";
        return s;
      }
      return Iv(e, t, n);
    }
    case "function": {
      if (e !== void 0) {
        var a = Nt, u = n(e);
        return Nt = a, No(e, t, u);
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
function Iv(e, t, n) {
  var r = "";
  if (Array.isArray(n))
    for (var o = 0; o < n.length; o++)
      r += No(e, t, n[o]) + ";";
  else
    for (var i in n) {
      var l = n[i];
      if (typeof l != "object") {
        var s = l;
        t != null && t[s] !== void 0 ? r += i + "{" + t[s] + "}" : jf(s) && (r += zs(i) + ":" + Af(i, s) + ";");
      } else {
        if (i === "NO_COMPONENT_SELECTOR" && Rv)
          throw new Error(Nv);
        if (Array.isArray(l) && typeof l[0] == "string" && (t == null || t[l[0]] === void 0))
          for (var a = 0; a < l.length; a++)
            jf(l[a]) && (r += zs(i) + ":" + Af(i, l[a]) + ";");
        else {
          var u = No(e, t, l);
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
var bf = /label:\s*([^\s;{]+)\s*(;|$)/g, Nt;
function Bo(e, t, n) {
  if (e.length === 1 && typeof e[0] == "object" && e[0] !== null && e[0].styles !== void 0)
    return e[0];
  var r = !0, o = "";
  Nt = void 0;
  var i = e[0];
  if (i == null || i.raw === void 0)
    r = !1, o += No(n, t, i);
  else {
    var l = i;
    o += l[0];
  }
  for (var s = 1; s < e.length; s++)
    if (o += No(n, t, e[s]), r) {
      var a = i;
      o += a[s];
    }
  bf.lastIndex = 0;
  for (var u = "", c; (c = bf.exec(o)) !== null; )
    u += "-" + c[1];
  var d = Pv(o) + u;
  return {
    name: d,
    styles: o,
    next: Nt
  };
}
var Lv = function(t) {
  return t();
}, lh = Vs["useInsertionEffect"] ? Vs["useInsertionEffect"] : !1, sh = lh || Lv, Df = lh || w.useLayoutEffect, zv = !1, ah = /* @__PURE__ */ w.createContext(
  // we're doing this to avoid preconstruct's dead code elimination in this one case
  // because this module is primarily intended for the browser and node
  // but it's also required in react native and similar environments sometimes
  // and we could have a special build just for that
  // but this is much easier and the native packages
  // might use a different theme context in the future anyway
  typeof HTMLElement < "u" ? /* @__PURE__ */ Jm({
    key: "css"
  }) : null
), jv = ah.Provider, Ju = function(t) {
  return /* @__PURE__ */ w.forwardRef(function(n, r) {
    var o = w.useContext(ah);
    return t(n, o, r);
  });
}, Nr = /* @__PURE__ */ w.createContext({}), ec = {}.hasOwnProperty, Fa = "__EMOTION_TYPE_PLEASE_DO_NOT_USE__", Av = function(t, n) {
  var r = {};
  for (var o in n)
    ec.call(n, o) && (r[o] = n[o]);
  return r[Fa] = t, r;
}, bv = function(t) {
  var n = t.cache, r = t.serialized, o = t.isStringTag;
  return Zu(n, r, o), sh(function() {
    return qu(n, r, o);
  }), null;
}, Dv = /* @__PURE__ */ Ju(function(e, t, n) {
  var r = e.css;
  typeof r == "string" && t.registered[r] !== void 0 && (r = t.registered[r]);
  var o = e[Fa], i = [r], l = "";
  typeof e.className == "string" ? l = oh(t.registered, i, e.className) : e.className != null && (l = e.className + " ");
  var s = Bo(i, void 0, w.useContext(Nr));
  l += t.key + "-" + s.name;
  var a = {};
  for (var u in e)
    ec.call(e, u) && u !== "css" && u !== Fa && !zv && (a[u] = e[u]);
  return a.className = l, n && (a.ref = n), /* @__PURE__ */ w.createElement(w.Fragment, null, /* @__PURE__ */ w.createElement(bv, {
    cache: t,
    serialized: s,
    isStringTag: typeof o == "string"
  }), /* @__PURE__ */ w.createElement(o, a));
}), Fv = Dv, js = { exports: {} }, Ff;
function uh() {
  return Ff || (Ff = 1, function(e) {
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
uh();
var Bf = function(t, n) {
  var r = arguments;
  if (n == null || !ec.call(n, "css"))
    return w.createElement.apply(void 0, r);
  var o = r.length, i = new Array(o);
  i[0] = Fv, i[1] = Av(t, n);
  for (var l = 2; l < o; l++)
    i[l] = r[l];
  return w.createElement.apply(null, i);
};
(function(e) {
  var t;
  t || (t = e.JSX || (e.JSX = {}));
})(Bf || (Bf = {}));
var Bv = /* @__PURE__ */ Ju(function(e, t) {
  var n = e.styles, r = Bo([n], void 0, w.useContext(Nr)), o = w.useRef();
  return Df(function() {
    var i = t.key + "-global", l = new t.sheet.constructor({
      key: i,
      nonce: t.sheet.nonce,
      container: t.sheet.container,
      speedy: t.sheet.isSpeedy
    }), s = !1, a = document.querySelector('style[data-emotion="' + i + " " + r.name + '"]');
    return t.sheet.tags.length && (l.before = t.sheet.tags[0]), a !== null && (s = !0, a.setAttribute("data-emotion", i), l.hydrate([a])), o.current = [l, s], function() {
      l.flush();
    };
  }, [t]), Df(function() {
    var i = o.current, l = i[0], s = i[1];
    if (s) {
      i[1] = !1;
      return;
    }
    if (r.next !== void 0 && qu(t, r.next, !0), l.tags.length) {
      var a = l.tags[l.tags.length - 1].nextElementSibling;
      l.before = a, l.flush();
    }
    t.insert("", r, l, !1);
  }, [t, r.name]), null;
});
function zl() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  return Bo(t);
}
function Ir() {
  var e = zl.apply(void 0, arguments), t = "animation-" + e.name;
  return {
    name: t,
    styles: "@keyframes " + t + "{" + e.styles + "}",
    anim: 1,
    toString: function() {
      return "_EMO_" + this.name + "_" + this.styles + "_EMO_";
    }
  };
}
var Uv = /^((children|dangerouslySetInnerHTML|key|ref|autoFocus|defaultValue|defaultChecked|innerHTML|suppressContentEditableWarning|suppressHydrationWarning|valueLink|abbr|accept|acceptCharset|accessKey|action|allow|allowUserMedia|allowPaymentRequest|allowFullScreen|allowTransparency|alt|async|autoComplete|autoPlay|capture|cellPadding|cellSpacing|challenge|charSet|checked|cite|classID|className|cols|colSpan|content|contentEditable|contextMenu|controls|controlsList|coords|crossOrigin|data|dateTime|decoding|default|defer|dir|disabled|disablePictureInPicture|disableRemotePlayback|download|draggable|encType|enterKeyHint|fetchpriority|fetchPriority|form|formAction|formEncType|formMethod|formNoValidate|formTarget|frameBorder|headers|height|hidden|high|href|hrefLang|htmlFor|httpEquiv|id|inputMode|integrity|is|keyParams|keyType|kind|label|lang|list|loading|loop|low|marginHeight|marginWidth|max|maxLength|media|mediaGroup|method|min|minLength|multiple|muted|name|nonce|noValidate|open|optimum|pattern|placeholder|playsInline|popover|popoverTarget|popoverTargetAction|poster|preload|profile|radioGroup|readOnly|referrerPolicy|rel|required|reversed|role|rows|rowSpan|sandbox|scope|scoped|scrolling|seamless|selected|shape|size|sizes|slot|span|spellCheck|src|srcDoc|srcLang|srcSet|start|step|style|summary|tabIndex|target|title|translate|type|useMap|value|width|wmode|wrap|about|datatype|inlist|prefix|property|resource|typeof|vocab|autoCapitalize|autoCorrect|autoSave|color|incremental|fallback|inert|itemProp|itemScope|itemType|itemID|itemRef|on|option|results|security|unselectable|accentHeight|accumulate|additive|alignmentBaseline|allowReorder|alphabetic|amplitude|arabicForm|ascent|attributeName|attributeType|autoReverse|azimuth|baseFrequency|baselineShift|baseProfile|bbox|begin|bias|by|calcMode|capHeight|clip|clipPathUnits|clipPath|clipRule|colorInterpolation|colorInterpolationFilters|colorProfile|colorRendering|contentScriptType|contentStyleType|cursor|cx|cy|d|decelerate|descent|diffuseConstant|direction|display|divisor|dominantBaseline|dur|dx|dy|edgeMode|elevation|enableBackground|end|exponent|externalResourcesRequired|fill|fillOpacity|fillRule|filter|filterRes|filterUnits|floodColor|floodOpacity|focusable|fontFamily|fontSize|fontSizeAdjust|fontStretch|fontStyle|fontVariant|fontWeight|format|from|fr|fx|fy|g1|g2|glyphName|glyphOrientationHorizontal|glyphOrientationVertical|glyphRef|gradientTransform|gradientUnits|hanging|horizAdvX|horizOriginX|ideographic|imageRendering|in|in2|intercept|k|k1|k2|k3|k4|kernelMatrix|kernelUnitLength|kerning|keyPoints|keySplines|keyTimes|lengthAdjust|letterSpacing|lightingColor|limitingConeAngle|local|markerEnd|markerMid|markerStart|markerHeight|markerUnits|markerWidth|mask|maskContentUnits|maskUnits|mathematical|mode|numOctaves|offset|opacity|operator|order|orient|orientation|origin|overflow|overlinePosition|overlineThickness|panose1|paintOrder|pathLength|patternContentUnits|patternTransform|patternUnits|pointerEvents|points|pointsAtX|pointsAtY|pointsAtZ|preserveAlpha|preserveAspectRatio|primitiveUnits|r|radius|refX|refY|renderingIntent|repeatCount|repeatDur|requiredExtensions|requiredFeatures|restart|result|rotate|rx|ry|scale|seed|shapeRendering|slope|spacing|specularConstant|specularExponent|speed|spreadMethod|startOffset|stdDeviation|stemh|stemv|stitchTiles|stopColor|stopOpacity|strikethroughPosition|strikethroughThickness|string|stroke|strokeDasharray|strokeDashoffset|strokeLinecap|strokeLinejoin|strokeMiterlimit|strokeOpacity|strokeWidth|surfaceScale|systemLanguage|tableValues|targetX|targetY|textAnchor|textDecoration|textRendering|textLength|to|transform|u1|u2|underlinePosition|underlineThickness|unicode|unicodeBidi|unicodeRange|unitsPerEm|vAlphabetic|vHanging|vIdeographic|vMathematical|values|vectorEffect|version|vertAdvY|vertOriginX|vertOriginY|viewBox|viewTarget|visibility|widths|wordSpacing|writingMode|x|xHeight|x1|x2|xChannelSelector|xlinkActuate|xlinkArcrole|xlinkHref|xlinkRole|xlinkShow|xlinkTitle|xlinkType|xmlBase|xmlns|xmlnsXlink|xmlLang|xmlSpace|y|y1|y2|yChannelSelector|z|zoomAndPan|for|class|autofocus)|(([Dd][Aa][Tt][Aa]|[Aa][Rr][Ii][Aa]|x)-.*))$/, Wv = /* @__PURE__ */ Zm(
  function(e) {
    return Uv.test(e) || e.charCodeAt(0) === 111 && e.charCodeAt(1) === 110 && e.charCodeAt(2) < 91;
  }
  /* Z+1 */
), Vv = !1, Hv = Wv, Gv = function(t) {
  return t !== "theme";
}, Uf = function(t) {
  return typeof t == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  t.charCodeAt(0) > 96 ? Hv : Gv;
}, Wf = function(t, n, r) {
  var o;
  if (n) {
    var i = n.shouldForwardProp;
    o = t.__emotion_forwardProp && i ? function(l) {
      return t.__emotion_forwardProp(l) && i(l);
    } : i;
  }
  return typeof o != "function" && r && (o = t.__emotion_forwardProp), o;
}, Kv = function(t) {
  var n = t.cache, r = t.serialized, o = t.isStringTag;
  return Zu(n, r, o), sh(function() {
    return qu(n, r, o);
  }), null;
}, Qv = function e(t, n) {
  var r = t.__emotion_real === t, o = r && t.__emotion_base || t, i, l;
  n !== void 0 && (i = n.label, l = n.target);
  var s = Wf(t, n, r), a = s || Uf(o), u = !a("as");
  return function() {
    var c = arguments, d = r && t.__emotion_styles !== void 0 ? t.__emotion_styles.slice(0) : [];
    if (i !== void 0 && d.push("label:" + i + ";"), c[0] == null || c[0].raw === void 0)
      d.push.apply(d, c);
    else {
      var p = c[0];
      d.push(p[0]);
      for (var v = c.length, y = 1; y < v; y++)
        d.push(c[y], p[y]);
    }
    var g = Ju(function($, m, f) {
      var h = u && $.as || o, x = "", _ = [], E = $;
      if ($.theme == null) {
        E = {};
        for (var C in $)
          E[C] = $[C];
        E.theme = w.useContext(Nr);
      }
      typeof $.className == "string" ? x = oh(m.registered, _, $.className) : $.className != null && (x = $.className + " ");
      var R = Bo(d.concat(_), m.registered, E);
      x += m.key + "-" + R.name, l !== void 0 && (x += " " + l);
      var z = u && s === void 0 ? Uf(h) : a, O = {};
      for (var D in $)
        u && D === "as" || z(D) && (O[D] = $[D]);
      return O.className = x, f && (O.ref = f), /* @__PURE__ */ w.createElement(w.Fragment, null, /* @__PURE__ */ w.createElement(Kv, {
        cache: m,
        serialized: R,
        isStringTag: typeof h == "string"
      }), /* @__PURE__ */ w.createElement(h, O));
    });
    return g.displayName = i !== void 0 ? i : "Styled(" + (typeof o == "string" ? o : o.displayName || o.name || "Component") + ")", g.defaultProps = t.defaultProps, g.__emotion_real = g, g.__emotion_base = o, g.__emotion_styles = d, g.__emotion_forwardProp = s, Object.defineProperty(g, "toString", {
      value: function() {
        return l === void 0 && Vv ? "NO_COMPONENT_SELECTOR" : "." + l;
      }
    }), g.withComponent = function($, m) {
      var f = e($, S({}, n, m, {
        shouldForwardProp: Wf(g, m, !0)
      }));
      return f.apply(void 0, d);
    }, g;
  };
}, Yv = [
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
], Ba = Qv.bind(null);
Yv.forEach(function(e) {
  Ba[e] = Ba(e);
});
function Xv(e, t) {
  const n = Jm({
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
function Zv(e) {
  const {
    injectFirst: t,
    enableCssLayer: n,
    children: r
  } = e, o = w.useMemo(() => {
    const i = `${t}-${n}`;
    if (typeof document == "object" && As.has(i))
      return As.get(i);
    const l = Xv(t, n);
    return As.set(i, l), l;
  }, [t, n]);
  return t || n ? /* @__PURE__ */ k.jsx(jv, {
    value: o,
    children: r
  }) : r;
}
function qv(e) {
  return e == null || Object.keys(e).length === 0;
}
function ch(e) {
  const {
    styles: t,
    defaultTheme: n = {}
  } = e, r = typeof t == "function" ? (o) => t(qv(o) ? n : o) : t;
  return /* @__PURE__ */ k.jsx(Bv, {
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
function fh(e, t) {
  return Ba(e, t);
}
const Jv = (e, t) => {
  Array.isArray(e.__emotion_styles) && (e.__emotion_styles = t(e.__emotion_styles));
}, Vf = [];
function dh(e) {
  return Vf[0] = e, Bo(Vf);
}
const e1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  GlobalStyles: ch,
  StyledEngineProvider: Zv,
  ThemeContext: Nr,
  css: zl,
  default: fh,
  internal_processStyles: Jv,
  internal_serializeStyles: dh,
  keyframes: Ir
}, Symbol.toStringTag, { value: "Module" }));
function on(e) {
  if (typeof e != "object" || e === null)
    return !1;
  const t = Object.getPrototypeOf(e);
  return (t === null || t === Object.prototype || Object.getPrototypeOf(t) === null) && !(Symbol.toStringTag in e) && !(Symbol.iterator in e);
}
function ph(e) {
  if (/* @__PURE__ */ w.isValidElement(e) || !on(e))
    return e;
  const t = {};
  return Object.keys(e).forEach((n) => {
    t[n] = ph(e[n]);
  }), t;
}
function At(e, t, n = {
  clone: !0
}) {
  const r = n.clone ? S({}, e) : e;
  return on(e) && on(t) && Object.keys(t).forEach((o) => {
    /* @__PURE__ */ w.isValidElement(t[o]) ? r[o] = t[o] : on(t[o]) && // Avoid prototype pollution
    Object.prototype.hasOwnProperty.call(e, o) && on(e[o]) ? r[o] = At(e[o], t[o], n) : n.clone ? r[o] = on(t[o]) ? ph(t[o]) : t[o] : r[o] = t[o];
  }), r;
}
const t1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: At,
  isPlainObject: on
}, Symbol.toStringTag, { value: "Module" })), n1 = ["values", "unit", "step"], r1 = (e) => {
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
  } = e, o = W(e, n1), i = r1(t), l = Object.keys(i);
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
  function d(p) {
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
    not: d,
    unit: n
  }, o);
}
const o1 = {
  borderRadius: 4
}, i1 = o1;
function co(e, t) {
  return t ? At(e, t, {
    clone: !1
    // No need to clone deep, it's way faster.
  }) : e;
}
const tc = {
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
}, Hf = {
  // Sorted ASC by size. That's important.
  // It can't be configured as it's used statically for propTypes.
  keys: ["xs", "sm", "md", "lg", "xl"],
  up: (e) => `@media (min-width:${tc[e]}px)`
};
function gt(e, t, n) {
  const r = e.theme || {};
  if (Array.isArray(t)) {
    const i = r.breakpoints || Hf;
    return t.reduce((l, s, a) => (l[i.up(i.keys[a])] = n(t[a]), l), {});
  }
  if (typeof t == "object") {
    const i = r.breakpoints || Hf;
    return Object.keys(t).reduce((l, s) => {
      if (Object.keys(i.values || tc).indexOf(s) !== -1) {
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
function l1(e = {}) {
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
function s1(e, t) {
  if (typeof e != "object")
    return {};
  const n = {}, r = Object.keys(t);
  return Array.isArray(e) ? r.forEach((o, i) => {
    i < e.length && (n[o] = !0);
  }) : r.forEach((o) => {
    e[o] != null && (n[o] = !0);
  }), n;
}
function jl({
  values: e,
  breakpoints: t,
  base: n
}) {
  const r = n || s1(e, t), o = Object.keys(r);
  if (o.length === 0)
    return e;
  let i;
  return o.reduce((l, s, a) => (Array.isArray(e) ? (l[s] = e[a] != null ? e[a] : e[i], i = a) : typeof e == "object" ? (l[s] = e[s] != null ? e[s] : e[i], i = s) : l[s] = e, l), {});
}
function le(e) {
  if (typeof e != "string")
    throw new Error(Ro(7));
  return e.charAt(0).toUpperCase() + e.slice(1);
}
const a1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: le
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
function nl(e, t, n, r = n) {
  let o;
  return typeof e == "function" ? o = e(n) : Array.isArray(e) ? o = e[n] || r : o = Al(e, n) || r, t && (o = t(o, r, e)), o;
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
    const s = l[t], a = l.theme, u = Al(a, r) || {};
    return gt(l, s, (d) => {
      let p = nl(u, o, d);
      return d === p && typeof d == "string" && (p = nl(u, o, `${t}${d === "default" ? "" : le(d)}`, d)), n === !1 ? p : {
        [n]: p
      };
    });
  };
  return i.propTypes = {}, i.filterProps = [t], i;
}
function u1(e) {
  const t = {};
  return (n) => (t[n] === void 0 && (t[n] = e(n)), t[n]);
}
const c1 = {
  m: "margin",
  p: "padding"
}, f1 = {
  t: "Top",
  r: "Right",
  b: "Bottom",
  l: "Left",
  x: ["Left", "Right"],
  y: ["Top", "Bottom"]
}, Kf = {
  marginX: "mx",
  marginY: "my",
  paddingX: "px",
  paddingY: "py"
}, d1 = u1((e) => {
  if (e.length > 2)
    if (Kf[e])
      e = Kf[e];
    else
      return [e];
  const [t, n] = e.split(""), r = c1[t], o = f1[n] || "";
  return Array.isArray(o) ? o.map((i) => r + i) : [r + o];
}), nc = ["m", "mt", "mr", "mb", "ml", "mx", "my", "margin", "marginTop", "marginRight", "marginBottom", "marginLeft", "marginX", "marginY", "marginInline", "marginInlineStart", "marginInlineEnd", "marginBlock", "marginBlockStart", "marginBlockEnd"], rc = ["p", "pt", "pr", "pb", "pl", "px", "py", "padding", "paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "paddingX", "paddingY", "paddingInline", "paddingInlineStart", "paddingInlineEnd", "paddingBlock", "paddingBlockStart", "paddingBlockEnd"];
[...nc, ...rc];
function Uo(e, t, n, r) {
  var o;
  const i = (o = Al(e, t, !1)) != null ? o : n;
  return typeof i == "number" ? (l) => typeof l == "string" ? l : i * l : Array.isArray(i) ? (l) => typeof l == "string" ? l : i[l] : typeof i == "function" ? i : () => {
  };
}
function hh(e) {
  return Uo(e, "spacing", 8);
}
function Wo(e, t) {
  if (typeof t == "string" || t == null)
    return t;
  const n = Math.abs(t), r = e(n);
  return t >= 0 ? r : typeof r == "number" ? -r : `-${r}`;
}
function p1(e, t) {
  return (n) => e.reduce((r, o) => (r[o] = Wo(t, n), r), {});
}
function m1(e, t, n, r) {
  if (t.indexOf(n) === -1)
    return null;
  const o = d1(n), i = p1(o, r), l = e[n];
  return gt(e, l, i);
}
function gh(e, t) {
  const n = hh(e.theme);
  return Object.keys(e).map((r) => m1(e, t, r, n)).reduce(co, {});
}
function ue(e) {
  return gh(e, nc);
}
ue.propTypes = {};
ue.filterProps = nc;
function ce(e) {
  return gh(e, rc);
}
ce.propTypes = {};
ce.filterProps = rc;
function h1(e = 8) {
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
function bl(...e) {
  const t = e.reduce((r, o) => (o.filterProps.forEach((i) => {
    r[i] = o;
  }), r), {}), n = (r) => Object.keys(r).reduce((o, i) => t[i] ? co(o, t[i](r)) : o, {});
  return n.propTypes = {}, n.filterProps = e.reduce((r, o) => r.concat(o.filterProps), []), n;
}
function ct(e) {
  return typeof e != "number" ? e : `${e}px solid`;
}
function vt(e, t) {
  return me({
    prop: e,
    themeKey: "borders",
    transform: t
  });
}
const g1 = vt("border", ct), y1 = vt("borderTop", ct), v1 = vt("borderRight", ct), x1 = vt("borderBottom", ct), S1 = vt("borderLeft", ct), w1 = vt("borderColor"), C1 = vt("borderTopColor"), k1 = vt("borderRightColor"), E1 = vt("borderBottomColor"), _1 = vt("borderLeftColor"), $1 = vt("outline", ct), P1 = vt("outlineColor"), Dl = (e) => {
  if (e.borderRadius !== void 0 && e.borderRadius !== null) {
    const t = Uo(e.theme, "shape.borderRadius", 4), n = (r) => ({
      borderRadius: Wo(t, r)
    });
    return gt(e, e.borderRadius, n);
  }
  return null;
};
Dl.propTypes = {};
Dl.filterProps = ["borderRadius"];
bl(g1, y1, v1, x1, S1, w1, C1, k1, E1, _1, Dl, $1, P1);
const Fl = (e) => {
  if (e.gap !== void 0 && e.gap !== null) {
    const t = Uo(e.theme, "spacing", 8), n = (r) => ({
      gap: Wo(t, r)
    });
    return gt(e, e.gap, n);
  }
  return null;
};
Fl.propTypes = {};
Fl.filterProps = ["gap"];
const Bl = (e) => {
  if (e.columnGap !== void 0 && e.columnGap !== null) {
    const t = Uo(e.theme, "spacing", 8), n = (r) => ({
      columnGap: Wo(t, r)
    });
    return gt(e, e.columnGap, n);
  }
  return null;
};
Bl.propTypes = {};
Bl.filterProps = ["columnGap"];
const Ul = (e) => {
  if (e.rowGap !== void 0 && e.rowGap !== null) {
    const t = Uo(e.theme, "spacing", 8), n = (r) => ({
      rowGap: Wo(t, r)
    });
    return gt(e, e.rowGap, n);
  }
  return null;
};
Ul.propTypes = {};
Ul.filterProps = ["rowGap"];
const T1 = me({
  prop: "gridColumn"
}), R1 = me({
  prop: "gridRow"
}), O1 = me({
  prop: "gridAutoFlow"
}), M1 = me({
  prop: "gridAutoColumns"
}), N1 = me({
  prop: "gridAutoRows"
}), I1 = me({
  prop: "gridTemplateColumns"
}), L1 = me({
  prop: "gridTemplateRows"
}), z1 = me({
  prop: "gridTemplateAreas"
}), j1 = me({
  prop: "gridArea"
});
bl(Fl, Bl, Ul, T1, R1, O1, M1, N1, I1, L1, z1, j1);
function pr(e, t) {
  return t === "grey" ? t : e;
}
const A1 = me({
  prop: "color",
  themeKey: "palette",
  transform: pr
}), b1 = me({
  prop: "bgcolor",
  cssProperty: "backgroundColor",
  themeKey: "palette",
  transform: pr
}), D1 = me({
  prop: "backgroundColor",
  themeKey: "palette",
  transform: pr
});
bl(A1, b1, D1);
function Ze(e) {
  return e <= 1 && e !== 0 ? `${e * 100}%` : e;
}
const F1 = me({
  prop: "width",
  transform: Ze
}), oc = (e) => {
  if (e.maxWidth !== void 0 && e.maxWidth !== null) {
    const t = (n) => {
      var r, o;
      const i = ((r = e.theme) == null || (r = r.breakpoints) == null || (r = r.values) == null ? void 0 : r[n]) || tc[n];
      return i ? ((o = e.theme) == null || (o = o.breakpoints) == null ? void 0 : o.unit) !== "px" ? {
        maxWidth: `${i}${e.theme.breakpoints.unit}`
      } : {
        maxWidth: i
      } : {
        maxWidth: Ze(n)
      };
    };
    return gt(e, e.maxWidth, t);
  }
  return null;
};
oc.filterProps = ["maxWidth"];
const B1 = me({
  prop: "minWidth",
  transform: Ze
}), U1 = me({
  prop: "height",
  transform: Ze
}), W1 = me({
  prop: "maxHeight",
  transform: Ze
}), V1 = me({
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
const H1 = me({
  prop: "boxSizing"
});
bl(F1, oc, B1, U1, W1, V1, H1);
const G1 = {
  // borders
  border: {
    themeKey: "borders",
    transform: ct
  },
  borderTop: {
    themeKey: "borders",
    transform: ct
  },
  borderRight: {
    themeKey: "borders",
    transform: ct
  },
  borderBottom: {
    themeKey: "borders",
    transform: ct
  },
  borderLeft: {
    themeKey: "borders",
    transform: ct
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
    transform: ct
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
    style: Fl
  },
  rowGap: {
    style: Ul
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
    transform: Ze
  },
  maxWidth: {
    style: oc
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
}, Vo = G1;
function K1(...e) {
  const t = e.reduce((r, o) => r.concat(Object.keys(o)), []), n = new Set(t);
  return e.every((r) => n.size === Object.keys(r).length);
}
function Q1(e, t) {
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
      style: d
    } = s;
    if (r == null)
      return null;
    if (u === "typography" && r === "inherit")
      return {
        [n]: r
      };
    const p = Al(o, u) || {};
    return d ? d(l) : gt(l, r, (y) => {
      let g = nl(p, c, y);
      return y === g && typeof y == "string" && (g = nl(p, c, `${n}${y === "default" ? "" : le(y)}`, y)), a === !1 ? g : {
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
    const s = (r = i.unstable_sxConfig) != null ? r : Vo;
    function a(u) {
      let c = u;
      if (typeof u == "function")
        c = u(i);
      else if (typeof u != "object")
        return u;
      if (!c)
        return null;
      const d = l1(i.breakpoints), p = Object.keys(d);
      let v = d;
      return Object.keys(c).forEach((y) => {
        const g = Q1(c[y], i);
        if (g != null)
          if (typeof g == "object")
            if (s[y])
              v = co(v, e(y, g, i, s));
            else {
              const $ = gt({
                theme: i
              }, g, (m) => ({
                [y]: m
              }));
              K1($, g) ? v[y] = t({
                sx: g,
                theme: i,
                nested: !0
              }) : v = co(v, $);
            }
          else
            v = co(v, e(y, g, i, s));
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
const Wl = vh;
function xh(e, t) {
  const n = this;
  return n.vars && typeof n.getColorSchemeSelector == "function" ? {
    [n.getColorSchemeSelector(e).replace(/(\[[^\]]+\])/, "*:where($1)")]: t
  } : n.palette.mode === e ? t : {};
}
const Y1 = ["breakpoints", "palette", "spacing", "shape"];
function ic(e = {}, ...t) {
  const {
    breakpoints: n = {},
    palette: r = {},
    spacing: o,
    shape: i = {}
  } = e, l = W(e, Y1), s = mh(n), a = h1(o);
  let u = At({
    breakpoints: s,
    direction: "ltr",
    components: {},
    // Inject component definitions.
    palette: S({
      mode: "light"
    }, r),
    spacing: a,
    shape: S({}, i1, i)
  }, l);
  return u.applyStyles = xh, u = t.reduce((c, d) => At(c, d), u), u.unstable_sxConfig = S({}, Vo, l == null ? void 0 : l.unstable_sxConfig), u.unstable_sx = function(d) {
    return Wl({
      sx: d,
      theme: this
    });
  }, u;
}
const X1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: ic,
  private_createBreakpoints: mh,
  unstable_applyStyles: xh
}, Symbol.toStringTag, { value: "Module" }));
function Z1(e) {
  return Object.keys(e).length === 0;
}
function lc(e = null) {
  const t = w.useContext(Nr);
  return !t || Z1(t) ? e : t;
}
const q1 = ic();
function sc(e = q1) {
  return lc(e);
}
function bs(e) {
  const t = dh(e);
  return e !== t && t.styles ? (t.styles.match(/^@layer\s+[^{]*$/) || (t.styles = `@layer global{${t.styles}}`), t) : e;
}
function Sh({
  styles: e,
  themeId: t,
  defaultTheme: n = {}
}) {
  const r = sc(n), o = t && r[t] || r;
  let i = typeof e == "function" ? e(o) : e;
  return o.modularCssLayers && (Array.isArray(i) ? i = i.map((l) => bs(typeof l == "function" ? l(o) : l)) : i = bs(i)), /* @__PURE__ */ k.jsx(ch, {
    styles: i
  });
}
const J1 = ["sx"], ex = (e) => {
  var t, n;
  const r = {
    systemProps: {},
    otherProps: {}
  }, o = (t = e == null || (n = e.theme) == null ? void 0 : n.unstable_sxConfig) != null ? t : Vo;
  return Object.keys(e).forEach((i) => {
    o[i] ? r.systemProps[i] = e[i] : r.otherProps[i] = e[i];
  }), r;
};
function Vl(e) {
  const {
    sx: t
  } = e, n = W(e, J1), {
    systemProps: r,
    otherProps: o
  } = ex(n);
  let i;
  return Array.isArray(t) ? i = [r, ...t] : typeof t == "function" ? i = (...l) => {
    const s = t(...l);
    return on(s) ? S({}, r, s) : r;
  } : i = S({}, r, t), S({}, o, {
    sx: i
  });
}
const tx = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Wl,
  extendSxProp: Vl,
  unstable_createStyleFunctionSx: yh,
  unstable_defaultSxConfig: Vo
}, Symbol.toStringTag, { value: "Module" })), Qf = (e) => e, nx = () => {
  let e = Qf;
  return {
    configure(t) {
      e = t;
    },
    generate(t) {
      return e(t);
    },
    reset() {
      e = Qf;
    }
  };
}, rx = nx(), ac = rx;
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
function G() {
  for (var e, t, n = 0, r = "", o = arguments.length; n < o; n++)
    (e = arguments[n]) && (t = wh(e)) && (r && (r += " "), r += t);
  return r;
}
const ox = ["className", "component"];
function ix(e = {}) {
  const {
    themeId: t,
    defaultTheme: n,
    defaultClassName: r = "MuiBox-root",
    generateClassName: o
  } = e, i = fh("div", {
    shouldForwardProp: (s) => s !== "theme" && s !== "sx" && s !== "as"
  })(Wl);
  return /* @__PURE__ */ w.forwardRef(function(a, u) {
    const c = sc(n), d = Vl(a), {
      className: p,
      component: v = "div"
    } = d, y = W(d, ox);
    return /* @__PURE__ */ k.jsx(i, S({
      as: v,
      ref: u,
      className: G(p, o ? o(r) : r),
      theme: t && c[t] || c
    }, y));
  });
}
const lx = {
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
function Ne(e, t, n = "Mui") {
  const r = lx[t];
  return r ? `${n}-${r}` : `${ac.generate(e)}-${t}`;
}
function Ce(e, t, n = "Mui") {
  const r = {};
  return t.forEach((o) => {
    r[o] = Ne(e, o, n);
  }), r;
}
var Ch = { exports: {} }, X = {};
/**
 * @license React
 * react-is.production.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var uc = Symbol.for("react.transitional.element"), cc = Symbol.for("react.portal"), Hl = Symbol.for("react.fragment"), Gl = Symbol.for("react.strict_mode"), Kl = Symbol.for("react.profiler"), Ql = Symbol.for("react.consumer"), Yl = Symbol.for("react.context"), Xl = Symbol.for("react.forward_ref"), Zl = Symbol.for("react.suspense"), ql = Symbol.for("react.suspense_list"), Jl = Symbol.for("react.memo"), es = Symbol.for("react.lazy"), sx = Symbol.for("react.view_transition"), ax = Symbol.for("react.client.reference");
function xt(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case uc:
        switch (e = e.type, e) {
          case Hl:
          case Kl:
          case Gl:
          case Zl:
          case ql:
          case sx:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Yl:
              case Xl:
              case es:
              case Jl:
                return e;
              case Ql:
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
X.ContextConsumer = Ql;
X.ContextProvider = Yl;
X.Element = uc;
X.ForwardRef = Xl;
X.Fragment = Hl;
X.Lazy = es;
X.Memo = Jl;
X.Portal = cc;
X.Profiler = Kl;
X.StrictMode = Gl;
X.Suspense = Zl;
X.SuspenseList = ql;
X.isContextConsumer = function(e) {
  return xt(e) === Ql;
};
X.isContextProvider = function(e) {
  return xt(e) === Yl;
};
X.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === uc;
};
X.isForwardRef = function(e) {
  return xt(e) === Xl;
};
X.isFragment = function(e) {
  return xt(e) === Hl;
};
X.isLazy = function(e) {
  return xt(e) === es;
};
X.isMemo = function(e) {
  return xt(e) === Jl;
};
X.isPortal = function(e) {
  return xt(e) === cc;
};
X.isProfiler = function(e) {
  return xt(e) === Kl;
};
X.isStrictMode = function(e) {
  return xt(e) === Gl;
};
X.isSuspense = function(e) {
  return xt(e) === Zl;
};
X.isSuspenseList = function(e) {
  return xt(e) === ql;
};
X.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === Hl || e === Kl || e === Gl || e === Zl || e === ql || typeof e == "object" && e !== null && (e.$$typeof === es || e.$$typeof === Jl || e.$$typeof === Yl || e.$$typeof === Ql || e.$$typeof === Xl || e.$$typeof === ax || e.getModuleId !== void 0);
};
X.typeOf = xt;
Ch.exports = X;
var Yf = Ch.exports;
const ux = /^\s*function(?:\s|\s*\/\*.*\*\/\s*)+([^(\s/]*)\s*/;
function kh(e) {
  const t = `${e}`.match(ux);
  return t && t[1] || "";
}
function Eh(e, t = "") {
  return e.displayName || e.name || kh(e) || t;
}
function Xf(e, t, n) {
  const r = Eh(t);
  return e.displayName || (r !== "" ? `${n}(${r})` : n);
}
function cx(e) {
  if (e != null) {
    if (typeof e == "string")
      return e;
    if (typeof e == "function")
      return Eh(e, "Component");
    if (typeof e == "object")
      switch (e.$$typeof) {
        case Yf.ForwardRef:
          return Xf(e, e.render, "ForwardRef");
        case Yf.Memo:
          return Xf(e, e.type, "memo");
        default:
          return;
      }
  }
}
const fx = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: cx,
  getFunctionName: kh
}, Symbol.toStringTag, { value: "Module" }));
function Ua(e, t) {
  const n = S({}, t);
  return Object.keys(e).forEach((r) => {
    if (r.toString().match(/^(components|slots)$/))
      n[r] = S({}, e[r], n[r]);
    else if (r.toString().match(/^(componentsProps|slotProps)$/)) {
      const o = e[r] || {}, i = t[r];
      n[r] = {}, !i || !Object.keys(i) ? n[r] = o : !o || !Object.keys(o) ? n[r] = i : (n[r] = S({}, i), Object.keys(o).forEach((l) => {
        n[r][l] = Ua(o[l], i[l]);
      }));
    } else
      n[r] === void 0 && (n[r] = e[r]);
  }), n;
}
const dx = typeof window < "u" ? w.useLayoutEffect : w.useEffect, ts = dx;
function px(e, t = Number.MIN_SAFE_INTEGER, n = Number.MAX_SAFE_INTEGER) {
  return Math.max(t, Math.min(e, n));
}
const mx = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: px
}, Symbol.toStringTag, { value: "Module" }));
function hx(...e) {
  return e.reduce((t, n) => n == null ? t : function(...o) {
    t.apply(this, o), n.apply(this, o);
  }, () => {
  });
}
function gx(e, t = 166) {
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
function yx(e, t) {
  return () => null;
}
function _h(e, t) {
  var n, r;
  return /* @__PURE__ */ w.isValidElement(e) && t.indexOf(
    // For server components `muiName` is avaialble in element.type._payload.value.muiName
    // relevant info - https://github.com/facebook/react/blob/2807d781a08db8e9873687fccc25c0f12b4fb3d4/packages/react/src/ReactLazy.js#L45
    // eslint-disable-next-line no-underscore-dangle
    (n = e.type.muiName) != null ? n : (r = e.type) == null || (r = r._payload) == null || (r = r.value) == null ? void 0 : r.muiName
  ) !== -1;
}
function $h(e) {
  return e && e.ownerDocument || document;
}
function vx(e) {
  return $h(e).defaultView || window;
}
function xx(e, t) {
  return () => null;
}
function Ph(e, t) {
  typeof e == "function" ? e(t) : e && (e.current = t);
}
let Zf = 0;
function Sx(e) {
  const [t, n] = w.useState(e), r = e || t;
  return w.useEffect(() => {
    t == null && (Zf += 1, n(`mui-${Zf}`));
  }, [t]), r;
}
const qf = Vs["useId".toString()];
function Th(e) {
  if (qf !== void 0) {
    const t = qf();
    return e ?? t;
  }
  return Sx(e);
}
function wx(e, t, n, r, o) {
  return null;
}
function Cx({
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
function Jr(e) {
  const t = w.useRef(e);
  return ts(() => {
    t.current = e;
  }), w.useRef((...n) => (
    // @ts-expect-error hide `this`
    (0, t.current)(...n)
  )).current;
}
function _r(...e) {
  return w.useMemo(() => e.every((t) => t == null) ? null : (t) => {
    e.forEach((n) => {
      Ph(n, t);
    });
  }, e);
}
const Jf = {};
function kx(e, t) {
  const n = w.useRef(Jf);
  return n.current === Jf && (n.current = e(t)), n;
}
const Ex = [];
function _x(e) {
  w.useEffect(e, Ex);
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
function Rh() {
  const e = kx(ns.create).current;
  return _x(e.disposeEffect), e;
}
let rs = !0, Wa = !1;
const $x = new ns(), Px = {
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
function Tx(e) {
  const {
    type: t,
    tagName: n
  } = e;
  return !!(n === "INPUT" && Px[t] && !e.readOnly || n === "TEXTAREA" && !e.readOnly || e.isContentEditable);
}
function Rx(e) {
  e.metaKey || e.altKey || e.ctrlKey || (rs = !0);
}
function Ds() {
  rs = !1;
}
function Ox() {
  this.visibilityState === "hidden" && Wa && (rs = !0);
}
function Mx(e) {
  e.addEventListener("keydown", Rx, !0), e.addEventListener("mousedown", Ds, !0), e.addEventListener("pointerdown", Ds, !0), e.addEventListener("touchstart", Ds, !0), e.addEventListener("visibilitychange", Ox, !0);
}
function Nx(e) {
  const {
    target: t
  } = e;
  try {
    return t.matches(":focus-visible");
  } catch {
  }
  return rs || Tx(t);
}
function Oh() {
  const e = w.useCallback((o) => {
    o != null && Mx(o.ownerDocument);
  }, []), t = w.useRef(!1);
  function n() {
    return t.current ? (Wa = !0, $x.start(100, () => {
      Wa = !1;
    }), t.current = !1, !0) : !1;
  }
  function r(o) {
    return Nx(o) ? (t.current = !0, !0) : !1;
  }
  return {
    isFocusVisibleRef: t,
    onFocus: r,
    onBlur: n,
    ref: e
  };
}
function be(e, t, n = void 0) {
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
function Va(e) {
  return typeof e == "string";
}
function Ix(e, t, n) {
  return e === void 0 || Va(e) ? t : S({}, t, {
    ownerState: S({}, t.ownerState, n)
  });
}
function Lx(e, t = []) {
  if (e === void 0)
    return {};
  const n = {};
  return Object.keys(e).filter((r) => r.match(/^on[A-Z]/) && typeof e[r] == "function" && !t.includes(r)).forEach((r) => {
    n[r] = e[r];
  }), n;
}
function ed(e) {
  if (e === void 0)
    return {};
  const t = {};
  return Object.keys(e).filter((n) => !(n.match(/^on[A-Z]/) && typeof e[n] == "function")).forEach((n) => {
    t[n] = e[n];
  }), t;
}
function zx(e) {
  const {
    getSlotProps: t,
    additionalProps: n,
    externalSlotProps: r,
    externalForwardedProps: o,
    className: i
  } = e;
  if (!t) {
    const v = G(n == null ? void 0 : n.className, i, o == null ? void 0 : o.className, r == null ? void 0 : r.className), y = S({}, n == null ? void 0 : n.style, o == null ? void 0 : o.style, r == null ? void 0 : r.style), g = S({}, n, o, r);
    return v.length > 0 && (g.className = v), Object.keys(y).length > 0 && (g.style = y), {
      props: g,
      internalRef: void 0
    };
  }
  const l = Lx(S({}, o, r)), s = ed(r), a = ed(o), u = t(l), c = G(u == null ? void 0 : u.className, n == null ? void 0 : n.className, i, o == null ? void 0 : o.className, r == null ? void 0 : r.className), d = S({}, u == null ? void 0 : u.style, n == null ? void 0 : n.style, o == null ? void 0 : o.style, r == null ? void 0 : r.style), p = S({}, u, n, a, s);
  return c.length > 0 && (p.className = c), Object.keys(d).length > 0 && (p.style = d), {
    props: p,
    internalRef: u.ref
  };
}
function jx(e, t, n) {
  return typeof e == "function" ? e(t, n) : e;
}
const Ax = /* @__PURE__ */ w.createContext(null), Mh = Ax;
function Nh() {
  return w.useContext(Mh);
}
const bx = typeof Symbol == "function" && Symbol.for, Dx = bx ? Symbol.for("mui.nested") : "__THEME_NESTED__";
function Fx(e, t) {
  return typeof t == "function" ? t(e) : S({}, e, t);
}
function Bx(e) {
  const {
    children: t,
    theme: n
  } = e, r = Nh(), o = w.useMemo(() => {
    const i = r === null ? n : Fx(r, n);
    return i != null && (i[Dx] = r !== null), i;
  }, [n, r]);
  return /* @__PURE__ */ k.jsx(Mh.Provider, {
    value: o,
    children: t
  });
}
const Ux = ["value"], Wx = /* @__PURE__ */ w.createContext();
function Vx(e) {
  let {
    value: t
  } = e, n = W(e, Ux);
  return /* @__PURE__ */ k.jsx(Wx.Provider, S({
    value: t ?? !0
  }, n));
}
const Ih = /* @__PURE__ */ w.createContext(void 0);
function Hx({
  value: e,
  children: t
}) {
  return /* @__PURE__ */ k.jsx(Ih.Provider, {
    value: e,
    children: t
  });
}
function Gx(e) {
  const {
    theme: t,
    name: n,
    props: r
  } = e;
  if (!t || !t.components || !t.components[n])
    return r;
  const o = t.components[n];
  return o.defaultProps ? Ua(o.defaultProps, r) : !o.styleOverrides && !o.variants ? Ua(o, r) : r;
}
function Kx({
  props: e,
  name: t
}) {
  const n = w.useContext(Ih);
  return Gx({
    props: e,
    name: t,
    theme: {
      components: n
    }
  });
}
function Qx(e) {
  const t = lc(), n = Th() || "", {
    modularCssLayers: r
  } = e;
  let o = "mui.global, mui.components, mui.theme, mui.custom, mui.sx";
  return !r || t !== null ? o = "" : typeof r == "string" ? o = r.replace(/mui(?!\.)/g, o) : o = `@layer ${o};`, ts(() => {
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
  }, [o, n]), o ? /* @__PURE__ */ k.jsx(Sh, {
    styles: o
  }) : null;
}
const td = {};
function nd(e, t, n, r = !1) {
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
function Yx(e) {
  const {
    children: t,
    theme: n,
    themeId: r
  } = e, o = lc(td), i = Nh() || td, l = nd(r, o, n), s = nd(r, i, n, !0), a = l.direction === "rtl", u = Qx(l);
  return /* @__PURE__ */ k.jsx(Bx, {
    theme: s,
    children: /* @__PURE__ */ k.jsx(Nr.Provider, {
      value: l,
      children: /* @__PURE__ */ k.jsx(Vx, {
        value: a,
        children: /* @__PURE__ */ k.jsxs(Hx, {
          value: l == null ? void 0 : l.components,
          children: [u, t]
        })
      })
    })
  });
}
function Xx(e, t) {
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
var he = {}, Lh = { exports: {} };
(function(e) {
  function t(n) {
    return n && n.__esModule ? n : {
      default: n
    };
  }
  e.exports = t, e.exports.__esModule = !0, e.exports.default = e.exports;
})(Lh);
var os = Lh.exports;
const Zx = /* @__PURE__ */ Qt(Uy), qx = /* @__PURE__ */ Qt(mx);
var zh = os;
Object.defineProperty(he, "__esModule", {
  value: !0
});
var Ut = he.alpha = Dh;
he.blend = uS;
he.colorChannel = void 0;
var Ha = he.darken = dc;
he.decomposeColor = yt;
he.emphasize = Fh;
var Jx = he.getContrastRatio = oS;
he.getLuminance = rl;
he.hexToRgb = jh;
he.hslToRgb = bh;
var Ga = he.lighten = pc;
he.private_safeAlpha = iS;
he.private_safeColorChannel = void 0;
he.private_safeDarken = lS;
he.private_safeEmphasize = aS;
he.private_safeLighten = sS;
he.recomposeColor = Lr;
he.rgbToHex = rS;
var rd = zh(Zx), eS = zh(qx);
function fc(e, t = 0, n = 1) {
  return (0, eS.default)(e, t, n);
}
function jh(e) {
  e = e.slice(1);
  const t = new RegExp(`.{1,${e.length >= 6 ? 2 : 1}}`, "g");
  let n = e.match(t);
  return n && n[0].length === 1 && (n = n.map((r) => r + r)), n ? `rgb${n.length === 4 ? "a" : ""}(${n.map((r, o) => o < 3 ? parseInt(r, 16) : Math.round(parseInt(r, 16) / 255 * 1e3) / 1e3).join(", ")})` : "";
}
function tS(e) {
  const t = e.toString(16);
  return t.length === 1 ? `0${t}` : t;
}
function yt(e) {
  if (e.type)
    return e;
  if (e.charAt(0) === "#")
    return yt(jh(e));
  const t = e.indexOf("("), n = e.substring(0, t);
  if (["rgb", "rgba", "hsl", "hsla", "color"].indexOf(n) === -1)
    throw new Error((0, rd.default)(9, e));
  let r = e.substring(t + 1, e.length - 1), o;
  if (n === "color") {
    if (r = r.split(" "), o = r.shift(), r.length === 4 && r[3].charAt(0) === "/" && (r[3] = r[3].slice(1)), ["srgb", "display-p3", "a98-rgb", "prophoto-rgb", "rec-2020"].indexOf(o) === -1)
      throw new Error((0, rd.default)(10, o));
  } else
    r = r.split(",");
  return r = r.map((i) => parseFloat(i)), {
    type: n,
    values: r,
    colorSpace: o
  };
}
const Ah = (e) => {
  const t = yt(e);
  return t.values.slice(0, 3).map((n, r) => t.type.indexOf("hsl") !== -1 && r !== 0 ? `${n}%` : n).join(" ");
};
he.colorChannel = Ah;
const nS = (e, t) => {
  try {
    return Ah(e);
  } catch {
    return e;
  }
};
he.private_safeColorChannel = nS;
function Lr(e) {
  const {
    type: t,
    colorSpace: n
  } = e;
  let {
    values: r
  } = e;
  return t.indexOf("rgb") !== -1 ? r = r.map((o, i) => i < 3 ? parseInt(o, 10) : o) : t.indexOf("hsl") !== -1 && (r[1] = `${r[1]}%`, r[2] = `${r[2]}%`), t.indexOf("color") !== -1 ? r = `${n} ${r.join(" ")}` : r = `${r.join(", ")}`, `${t}(${r})`;
}
function rS(e) {
  if (e.indexOf("#") === 0)
    return e;
  const {
    values: t
  } = yt(e);
  return `#${t.map((n, r) => tS(r === 3 ? Math.round(255 * n) : n)).join("")}`;
}
function bh(e) {
  e = yt(e);
  const {
    values: t
  } = e, n = t[0], r = t[1] / 100, o = t[2] / 100, i = r * Math.min(o, 1 - o), l = (u, c = (u + n / 30) % 12) => o - i * Math.max(Math.min(c - 3, 9 - c, 1), -1);
  let s = "rgb";
  const a = [Math.round(l(0) * 255), Math.round(l(8) * 255), Math.round(l(4) * 255)];
  return e.type === "hsla" && (s += "a", a.push(t[3])), Lr({
    type: s,
    values: a
  });
}
function rl(e) {
  e = yt(e);
  let t = e.type === "hsl" || e.type === "hsla" ? yt(bh(e)).values : e.values;
  return t = t.map((n) => (e.type !== "color" && (n /= 255), n <= 0.03928 ? n / 12.92 : ((n + 0.055) / 1.055) ** 2.4)), Number((0.2126 * t[0] + 0.7152 * t[1] + 0.0722 * t[2]).toFixed(3));
}
function oS(e, t) {
  const n = rl(e), r = rl(t);
  return (Math.max(n, r) + 0.05) / (Math.min(n, r) + 0.05);
}
function Dh(e, t) {
  return e = yt(e), t = fc(t), (e.type === "rgb" || e.type === "hsl") && (e.type += "a"), e.type === "color" ? e.values[3] = `/${t}` : e.values[3] = t, Lr(e);
}
function iS(e, t, n) {
  try {
    return Dh(e, t);
  } catch {
    return e;
  }
}
function dc(e, t) {
  if (e = yt(e), t = fc(t), e.type.indexOf("hsl") !== -1)
    e.values[2] *= 1 - t;
  else if (e.type.indexOf("rgb") !== -1 || e.type.indexOf("color") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] *= 1 - t;
  return Lr(e);
}
function lS(e, t, n) {
  try {
    return dc(e, t);
  } catch {
    return e;
  }
}
function pc(e, t) {
  if (e = yt(e), t = fc(t), e.type.indexOf("hsl") !== -1)
    e.values[2] += (100 - e.values[2]) * t;
  else if (e.type.indexOf("rgb") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] += (255 - e.values[n]) * t;
  else if (e.type.indexOf("color") !== -1)
    for (let n = 0; n < 3; n += 1)
      e.values[n] += (1 - e.values[n]) * t;
  return Lr(e);
}
function sS(e, t, n) {
  try {
    return pc(e, t);
  } catch {
    return e;
  }
}
function Fh(e, t = 0.15) {
  return rl(e) > 0.5 ? dc(e, t) : pc(e, t);
}
function aS(e, t, n) {
  try {
    return Fh(e, t);
  } catch {
    return e;
  }
}
function uS(e, t, n, r = 1) {
  const o = (a, u) => Math.round((a ** (1 / r) * (1 - n) + u ** (1 / r) * n) ** r), i = yt(e), l = yt(t), s = [o(i.values[0], l.values[0]), o(i.values[1], l.values[1]), o(i.values[2], l.values[2])];
  return Lr({
    type: "rgb",
    values: s
  });
}
const cS = {
  black: "#000",
  white: "#fff"
}, Io = cS, fS = {
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
}, dS = fS, pS = {
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
}, Fn = pS, mS = {
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
}, Bn = mS, hS = {
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
}, Kr = hS, gS = {
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
}, Un = gS, yS = {
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
}, Wn = yS, vS = {
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
}, Vn = vS, xS = ["mode", "contrastThreshold", "tonalOffset"], od = {
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
    paper: Io.white,
    default: Io.white
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
}, Fs = {
  text: {
    primary: Io.white,
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
    active: Io.white,
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
function id(e, t, n, r) {
  const o = r.light || r, i = r.dark || r * 1.5;
  e[t] || (e.hasOwnProperty(n) ? e[t] = e[n] : t === "light" ? e.light = Ga(e.main, o) : t === "dark" && (e.dark = Ha(e.main, i)));
}
function SS(e = "light") {
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
function wS(e = "light") {
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
function CS(e = "light") {
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
function kS(e = "light") {
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
function ES(e = "light") {
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
function _S(e = "light") {
  return e === "dark" ? {
    main: Kr[400],
    light: Kr[300],
    dark: Kr[700]
  } : {
    main: "#ed6c02",
    // closest to orange[800] that pass 3:1.
    light: Kr[500],
    dark: Kr[900]
  };
}
function $S(e) {
  const {
    mode: t = "light",
    contrastThreshold: n = 3,
    tonalOffset: r = 0.2
  } = e, o = W(e, xS), i = e.primary || SS(t), l = e.secondary || wS(t), s = e.error || CS(t), a = e.info || kS(t), u = e.success || ES(t), c = e.warning || _S(t);
  function d(g) {
    return Jx(g, Fs.text.primary) >= n ? Fs.text.primary : od.text.primary;
  }
  const p = ({
    color: g,
    name: $,
    mainShade: m = 500,
    lightShade: f = 300,
    darkShade: h = 700
  }) => {
    if (g = S({}, g), !g.main && g[m] && (g.main = g[m]), !g.hasOwnProperty("main"))
      throw new Error(Ro(11, $ ? ` (${$})` : "", m));
    if (typeof g.main != "string")
      throw new Error(Ro(12, $ ? ` (${$})` : "", JSON.stringify(g.main)));
    return id(g, "light", f, r), id(g, "dark", h, r), g.contrastText || (g.contrastText = d(g.main)), g;
  }, v = {
    dark: Fs,
    light: od
  };
  return At(S({
    // A collection of common colors.
    common: S({}, Io),
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
    grey: dS,
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
const PS = ["fontFamily", "fontSize", "fontWeightLight", "fontWeightRegular", "fontWeightMedium", "fontWeightBold", "htmlFontSize", "allVariants", "pxToRem"];
function TS(e) {
  return Math.round(e * 1e5) / 1e5;
}
const ld = {
  textTransform: "uppercase"
}, sd = '"Roboto", "Helvetica", "Arial", sans-serif';
function RS(e, t) {
  const n = typeof t == "function" ? t(e) : t, {
    fontFamily: r = sd,
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
  } = n, p = W(n, PS), v = o / 14, y = d || ((m) => `${m / u * v}rem`), g = (m, f, h, x, _) => S({
    fontFamily: r,
    fontWeight: m,
    fontSize: y(f),
    // Unitless following https://meyerweb.com/eric/thoughts/2006/02/08/unitless-line-heights/
    lineHeight: h
  }, r === sd ? {
    letterSpacing: `${TS(x / f)}em`
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
    button: g(s, 14, 1.75, 0.4, ld),
    caption: g(l, 12, 1.66, 0.4),
    overline: g(l, 12, 2.66, 1, ld),
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
  }, $), p, {
    clone: !1
    // No need to clone deep
  });
}
const OS = 0.2, MS = 0.14, NS = 0.12;
function ne(...e) {
  return [`${e[0]}px ${e[1]}px ${e[2]}px ${e[3]}px rgba(0,0,0,${OS})`, `${e[4]}px ${e[5]}px ${e[6]}px ${e[7]}px rgba(0,0,0,${MS})`, `${e[8]}px ${e[9]}px ${e[10]}px ${e[11]}px rgba(0,0,0,${NS})`].join(",");
}
const IS = ["none", ne(0, 2, 1, -1, 0, 1, 1, 0, 0, 1, 3, 0), ne(0, 3, 1, -2, 0, 2, 2, 0, 0, 1, 5, 0), ne(0, 3, 3, -2, 0, 3, 4, 0, 0, 1, 8, 0), ne(0, 2, 4, -1, 0, 4, 5, 0, 0, 1, 10, 0), ne(0, 3, 5, -1, 0, 5, 8, 0, 0, 1, 14, 0), ne(0, 3, 5, -1, 0, 6, 10, 0, 0, 1, 18, 0), ne(0, 4, 5, -2, 0, 7, 10, 1, 0, 2, 16, 1), ne(0, 5, 5, -3, 0, 8, 10, 1, 0, 3, 14, 2), ne(0, 5, 6, -3, 0, 9, 12, 1, 0, 3, 16, 2), ne(0, 6, 6, -3, 0, 10, 14, 1, 0, 4, 18, 3), ne(0, 6, 7, -4, 0, 11, 15, 1, 0, 4, 20, 3), ne(0, 7, 8, -4, 0, 12, 17, 2, 0, 5, 22, 4), ne(0, 7, 8, -4, 0, 13, 19, 2, 0, 5, 24, 4), ne(0, 7, 9, -4, 0, 14, 21, 2, 0, 5, 26, 4), ne(0, 8, 9, -5, 0, 15, 22, 2, 0, 6, 28, 5), ne(0, 8, 10, -5, 0, 16, 24, 2, 0, 6, 30, 5), ne(0, 8, 11, -5, 0, 17, 26, 2, 0, 6, 32, 5), ne(0, 9, 11, -5, 0, 18, 28, 2, 0, 7, 34, 6), ne(0, 9, 12, -6, 0, 19, 29, 2, 0, 7, 36, 6), ne(0, 10, 13, -6, 0, 20, 31, 3, 0, 8, 38, 7), ne(0, 10, 13, -6, 0, 21, 33, 3, 0, 8, 40, 7), ne(0, 10, 14, -6, 0, 22, 35, 3, 0, 8, 42, 7), ne(0, 11, 14, -7, 0, 23, 36, 3, 0, 9, 44, 8), ne(0, 11, 15, -7, 0, 24, 38, 3, 0, 9, 46, 8)], LS = IS, zS = ["duration", "easing", "delay"], jS = {
  // This is the most common easing curve.
  easeInOut: "cubic-bezier(0.4, 0, 0.2, 1)",
  // Objects enter the screen at full velocity from off-screen and
  // slowly decelerate to a resting point.
  easeOut: "cubic-bezier(0.0, 0, 0.2, 1)",
  // Objects leave the screen at full velocity. They do not decelerate when off-screen.
  easeIn: "cubic-bezier(0.4, 0, 1, 1)",
  // The sharp curve is used by objects that may return to the screen at any time.
  sharp: "cubic-bezier(0.4, 0, 0.6, 1)"
}, Bh = {
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
function ad(e) {
  return `${Math.round(e)}ms`;
}
function AS(e) {
  if (!e)
    return 0;
  const t = e / 36;
  return Math.round((4 + 15 * t ** 0.25 + t / 5) * 10);
}
function bS(e) {
  const t = S({}, jS, e.easing), n = S({}, Bh, e.duration);
  return S({
    getAutoHeightDuration: AS,
    create: (o = ["all"], i = {}) => {
      const {
        duration: l = n.standard,
        easing: s = t.easeInOut,
        delay: a = 0
      } = i;
      return W(i, zS), (Array.isArray(o) ? o : [o]).map((u) => `${u} ${typeof l == "string" ? l : ad(l)} ${s} ${typeof a == "string" ? a : ad(a)}`).join(",");
    }
  }, e, {
    easing: t,
    duration: n
  });
}
const DS = {
  mobileStepper: 1e3,
  fab: 1050,
  speedDial: 1050,
  appBar: 1100,
  drawer: 1200,
  modal: 1300,
  snackbar: 1400,
  tooltip: 1500
}, FS = DS, BS = ["breakpoints", "mixins", "spacing", "palette", "transitions", "typography", "shape"];
function mc(e = {}, ...t) {
  const {
    mixins: n = {},
    palette: r = {},
    transitions: o = {},
    typography: i = {}
  } = e, l = W(e, BS);
  if (e.vars && // The error should throw only for the root theme creation because user is not allowed to use a custom node `vars`.
  // `generateCssVars` is the closest identifier for checking that the `options` is a result of `extendTheme` with CSS variables so that user can create new theme for nested ThemeProvider.
  e.generateCssVars === void 0)
    throw new Error(Ro(18));
  const s = $S(r), a = ic(e);
  let u = At(a, {
    mixins: Xx(a.breakpoints, n),
    palette: s,
    // Don't use [...shadows] until you've verified its transpiled code is not invoking the iterator protocol.
    shadows: LS.slice(),
    typography: RS(s, i),
    transitions: bS(o),
    zIndex: S({}, FS)
  });
  return u = At(u, l), u = t.reduce((c, d) => At(c, d), u), u.unstable_sxConfig = S({}, Vo, l == null ? void 0 : l.unstable_sxConfig), u.unstable_sx = function(d) {
    return Wl({
      sx: d,
      theme: this
    });
  }, u;
}
const US = mc(), hc = US;
function Uh() {
  const e = sc(hc);
  return e[kr] || e;
}
var Ho = {}, Bs = { exports: {} }, ud;
function WS() {
  return ud || (ud = 1, function(e) {
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
  }(Bs)), Bs.exports;
}
const VS = /* @__PURE__ */ Qt(e1), HS = /* @__PURE__ */ Qt(t1), GS = /* @__PURE__ */ Qt(a1), KS = /* @__PURE__ */ Qt(fx), QS = /* @__PURE__ */ Qt(X1), YS = /* @__PURE__ */ Qt(tx);
var zr = os;
Object.defineProperty(Ho, "__esModule", {
  value: !0
});
var XS = Ho.default = uw;
Ho.shouldForwardProp = Ri;
Ho.systemDefaultTheme = void 0;
var lt = zr(uh()), Ka = zr(WS()), ol = rw(VS), ZS = HS;
zr(GS);
zr(KS);
var qS = zr(QS), JS = zr(YS);
const ew = ["ownerState"], tw = ["variants"], nw = ["name", "slot", "skipVariantsResolver", "skipSx", "overridesResolver"];
function Wh(e) {
  if (typeof WeakMap != "function")
    return null;
  var t = /* @__PURE__ */ new WeakMap(), n = /* @__PURE__ */ new WeakMap();
  return (Wh = function(r) {
    return r ? n : t;
  })(e);
}
function rw(e, t) {
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
function ow(e) {
  return Object.keys(e).length === 0;
}
function iw(e) {
  return typeof e == "string" && // 96 is one less than the char code
  // for "a" so this is checking that
  // it's a lowercase character
  e.charCodeAt(0) > 96;
}
function Ri(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
function cd(e, t) {
  return t && e && typeof e == "object" && e.styles && !e.styles.startsWith("@layer") && (e.styles = `@layer ${t}{${String(e.styles)}}`), e;
}
const lw = Ho.systemDefaultTheme = (0, qS.default)(), sw = (e) => e && e.charAt(0).toLowerCase() + e.slice(1);
function pi({
  defaultTheme: e,
  theme: t,
  themeId: n
}) {
  return ow(t) ? e : t[n] || t;
}
function aw(e) {
  return e ? (t, n) => n[e] : null;
}
function Oi(e, t, n) {
  let {
    ownerState: r
  } = t, o = (0, Ka.default)(t, ew);
  const i = typeof e == "function" ? e((0, lt.default)({
    ownerState: r
  }, o)) : e;
  if (Array.isArray(i))
    return i.flatMap((l) => Oi(l, (0, lt.default)({
      ownerState: r
    }, o), n));
  if (i && typeof i == "object" && Array.isArray(i.variants)) {
    const {
      variants: l = []
    } = i;
    let a = (0, Ka.default)(i, tw);
    return l.forEach((u) => {
      let c = !0;
      if (typeof u.props == "function" ? c = u.props((0, lt.default)({
        ownerState: r
      }, o, r)) : Object.keys(u.props).forEach((d) => {
        (r == null ? void 0 : r[d]) !== u.props[d] && o[d] !== u.props[d] && (c = !1);
      }), c) {
        Array.isArray(a) || (a = [a]);
        const d = typeof u.style == "function" ? u.style((0, lt.default)({
          ownerState: r
        }, o, r)) : u.style;
        a.push(n ? cd((0, ol.internal_serializeStyles)(d), n) : d);
      }
    }), a;
  }
  return n ? cd((0, ol.internal_serializeStyles)(i), n) : i;
}
function uw(e = {}) {
  const {
    themeId: t,
    defaultTheme: n = lw,
    rootShouldForwardProp: r = Ri,
    slotShouldForwardProp: o = Ri
  } = e, i = (l) => (0, JS.default)((0, lt.default)({}, l, {
    theme: pi((0, lt.default)({}, l, {
      defaultTheme: n,
      themeId: t
    }))
  }));
  return i.__mui_systemSx = !0, (l, s = {}) => {
    (0, ol.internal_processStyles)(l, (E) => E.filter((C) => !(C != null && C.__mui_systemSx)));
    const {
      name: a,
      slot: u,
      skipVariantsResolver: c,
      skipSx: d,
      // TODO v6: remove `lowercaseFirstLetter()` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      overridesResolver: p = aw(sw(u))
    } = s, v = (0, Ka.default)(s, nw), y = a && a.startsWith("Mui") || u ? "components" : "custom", g = c !== void 0 ? c : (
      // TODO v6: remove `Root` in the next major release
      // For more details: https://github.com/mui/material-ui/pull/37908
      u && u !== "Root" && u !== "root" || !1
    ), $ = d || !1;
    let m, f = Ri;
    u === "Root" || u === "root" ? f = r : u ? f = o : iw(l) && (f = void 0);
    const h = (0, ol.default)(l, (0, lt.default)({
      shouldForwardProp: f,
      label: m
    }, v)), x = (E) => typeof E == "function" && E.__emotion_real !== E || (0, ZS.isPlainObject)(E) ? (C) => {
      const R = pi({
        theme: C.theme,
        defaultTheme: n,
        themeId: t
      });
      return Oi(E, (0, lt.default)({}, C, {
        theme: R
      }), R.modularCssLayers ? y : void 0);
    } : E, _ = (E, ...C) => {
      let R = x(E);
      const z = C ? C.map(x) : [];
      a && p && z.push((F) => {
        const A = pi((0, lt.default)({}, F, {
          defaultTheme: n,
          themeId: t
        }));
        if (!A.components || !A.components[a] || !A.components[a].styleOverrides)
          return null;
        const Y = A.components[a].styleOverrides, te = {};
        return Object.entries(Y).forEach(([ge, de]) => {
          te[ge] = Oi(de, (0, lt.default)({}, F, {
            theme: A
          }), A.modularCssLayers ? "theme" : void 0);
        }), p(F, te);
      }), a && !g && z.push((F) => {
        var A;
        const Y = pi((0, lt.default)({}, F, {
          defaultTheme: n,
          themeId: t
        })), te = Y == null || (A = Y.components) == null || (A = A[a]) == null ? void 0 : A.variants;
        return Oi({
          variants: te
        }, (0, lt.default)({}, F, {
          theme: Y
        }), Y.modularCssLayers ? "theme" : void 0);
      }), $ || z.push(i);
      const O = z.length - C.length;
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
function cw(e) {
  return e !== "ownerState" && e !== "theme" && e !== "sx" && e !== "as";
}
const fw = (e) => cw(e) && e !== "classes", dw = fw, pw = XS({
  themeId: kr,
  defaultTheme: hc,
  rootShouldForwardProp: dw
}), Z = pw, mw = ["theme"];
function hw(e) {
  let {
    theme: t
  } = e, n = W(e, mw);
  const r = t[kr];
  let o = r || t;
  return typeof t != "function" && (r && !r.vars ? o = S({}, r, {
    vars: null
  }) : t && !t.vars && (o = S({}, t, {
    vars: null
  }))), /* @__PURE__ */ k.jsx(Yx, S({}, n, {
    themeId: r ? kr : void 0,
    theme: o
  }));
}
const gw = (e) => {
  let t;
  return e < 1 ? t = 5.11916 * e ** 2 : t = 4.5 * Math.log(e + 1) + 2, (t / 100).toFixed(2);
}, fd = gw;
function $e(e) {
  return Kx(e);
}
function yw(e) {
  return /* @__PURE__ */ k.jsx(Sh, S({}, e, {
    defaultTheme: hc,
    themeId: kr
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
  const t = $e({
    props: e,
    name: "MuiCssBaseline"
  }), {
    children: n,
    enableColorScheme: r = !1
  } = t;
  return /* @__PURE__ */ k.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ k.jsx(yw, {
      styles: (o) => Sw(o, r)
    }), n]
  });
}
function Cw(e) {
  return Ne("MuiCircularProgress", e);
}
Ce("MuiCircularProgress", ["root", "determinate", "indeterminate", "colorPrimary", "colorSecondary", "svg", "circle", "circleDeterminate", "circleIndeterminate", "circleDisableShrink"]);
const kw = ["className", "color", "disableShrink", "size", "style", "thickness", "value", "variant"];
let is = (e) => e, dd, pd, md, hd;
const Jt = 44, Ew = Ir(dd || (dd = is`
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
`)), _w = Ir(pd || (pd = is`
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
  return be(i, Cw, t);
}, Pw = Z("span", {
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
}) => e.variant === "indeterminate" && zl(md || (md = is`
      animation: ${0} 1.4s linear infinite;
    `), Ew)), Tw = Z("svg", {
  name: "MuiCircularProgress",
  slot: "Svg",
  overridesResolver: (e, t) => t.svg
})({
  display: "block"
  // Keeps the progress centered
}), Rw = Z("circle", {
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
}) => e.variant === "indeterminate" && !e.disableShrink && zl(hd || (hd = is`
      animation: ${0} 1.4s ease-in-out infinite;
    `), _w)), Ow = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = $e({
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
  } = r, p = W(r, kw), v = S({}, r, {
    color: i,
    disableShrink: l,
    size: s,
    thickness: u,
    value: c,
    variant: d
  }), y = $w(v), g = {}, $ = {}, m = {};
  if (d === "determinate") {
    const f = 2 * Math.PI * ((Jt - u) / 2);
    g.strokeDasharray = f.toFixed(3), m["aria-valuenow"] = Math.round(c), g.strokeDashoffset = `${((100 - c) / 100 * f).toFixed(3)}px`, $.transform = "rotate(-90deg)";
  }
  return /* @__PURE__ */ k.jsx(Pw, S({
    className: G(y.root, o),
    style: S({
      width: s,
      height: s
    }, $, a),
    ownerState: v,
    ref: n,
    role: "progressbar"
  }, m, p, {
    children: /* @__PURE__ */ k.jsx(Tw, {
      className: y.svg,
      ownerState: v,
      viewBox: `${Jt / 2} ${Jt / 2} ${Jt} ${Jt}`,
      children: /* @__PURE__ */ k.jsx(Rw, {
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
function gd(e, t) {
  const {
    className: n,
    elementType: r,
    ownerState: o,
    externalForwardedProps: i,
    getSlotOwnerState: l,
    internalForwardedProps: s
  } = t, a = W(t, Nw), {
    component: u,
    slots: c = {
      [e]: void 0
    },
    slotProps: d = {
      [e]: void 0
    }
  } = i, p = W(i, Iw), v = c[e] || r, y = jx(d[e], o), g = zx(S({
    className: n
  }, a, {
    externalForwardedProps: e === "root" ? p : void 0,
    externalSlotProps: y
  })), {
    props: {
      component: $
    },
    internalRef: m
  } = g, f = W(g.props, Lw), h = _r(m, y == null ? void 0 : y.ref, t.ref), x = l ? l(f) : {}, _ = S({}, o, x), E = e === "root" ? $ || u : $, C = Ix(v, S({}, e === "root" && !u && !c[e] && s, e !== "root" && !c[e] && s, f, E && {
    as: E
  }, {
    ref: h
  }), _);
  return Object.keys(x).forEach((R) => {
    delete C[R];
  }), [v, C];
}
function zw(e) {
  return Ne("MuiPaper", e);
}
Ce("MuiPaper", ["root", "rounded", "outlined", "elevation", "elevation0", "elevation1", "elevation2", "elevation3", "elevation4", "elevation5", "elevation6", "elevation7", "elevation8", "elevation9", "elevation10", "elevation11", "elevation12", "elevation13", "elevation14", "elevation15", "elevation16", "elevation17", "elevation18", "elevation19", "elevation20", "elevation21", "elevation22", "elevation23", "elevation24"]);
const jw = ["className", "component", "elevation", "square", "variant"], Aw = (e) => {
  const {
    square: t,
    elevation: n,
    variant: r,
    classes: o
  } = e, i = {
    root: ["root", r, !t && "rounded", r === "elevation" && `elevation${n}`]
  };
  return be(i, zw, o);
}, bw = Z("div", {
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
    backgroundImage: `linear-gradient(${Ut("#fff", fd(t.elevation))}, ${Ut("#fff", fd(t.elevation))})`
  }, e.vars && {
    backgroundImage: (n = e.vars.overlays) == null ? void 0 : n[t.elevation]
  }));
}), Dw = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = $e({
    props: t,
    name: "MuiPaper"
  }), {
    className: o,
    component: i = "div",
    elevation: l = 1,
    square: s = !1,
    variant: a = "elevation"
  } = r, u = W(r, jw), c = S({}, r, {
    component: i,
    elevation: l,
    square: s,
    variant: a
  }), d = Aw(c);
  return /* @__PURE__ */ k.jsx(bw, S({
    as: i,
    ownerState: c,
    className: G(d.root, o),
    ref: n
  }, u));
}), $r = Dw;
function Fw(e) {
  return Ne("MuiAlert", e);
}
const Bw = Ce("MuiAlert", ["root", "action", "icon", "message", "filled", "colorSuccess", "colorInfo", "colorWarning", "colorError", "filledSuccess", "filledInfo", "filledWarning", "filledError", "outlined", "outlinedSuccess", "outlinedInfo", "outlinedWarning", "outlinedError", "standard", "standardSuccess", "standardInfo", "standardWarning", "standardError"]), yd = Bw;
function Qa(e, t) {
  return Qa = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, r) {
    return n.__proto__ = r, n;
  }, Qa(e, t);
}
function Vh(e, t) {
  e.prototype = Object.create(t.prototype), e.prototype.constructor = e, Qa(e, t);
}
const vd = {
  disabled: !1
}, il = qe.createContext(null);
var Uw = function(t) {
  return t.scrollTop;
}, eo = "unmounted", kn = "exited", En = "entering", Gn = "entered", Ya = "exiting", Xt = /* @__PURE__ */ function(e) {
  Vh(t, e);
  function t(r, o) {
    var i;
    i = e.call(this, r, o) || this;
    var l = o, s = l && !l.isMounting ? r.enter : r.appear, a;
    return i.appearStatus = null, r.in ? s ? (a = kn, i.appearStatus = En) : a = Gn : r.unmountOnExit || r.mountOnEnter ? a = eo : a = kn, i.state = {
      status: a
    }, i.nextCallback = null, i;
  }
  t.getDerivedStateFromProps = function(o, i) {
    var l = o.in;
    return l && i.status === eo ? {
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
      this.props.in ? l !== En && l !== Gn && (i = En) : (l === En || l === Gn) && (i = Ya);
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
          var l = this.props.nodeRef ? this.props.nodeRef.current : fi.findDOMNode(this);
          l && Uw(l);
        }
        this.performEnter(o);
      } else
        this.performExit();
    else
      this.props.unmountOnExit && this.state.status === kn && this.setState({
        status: eo
      });
  }, n.performEnter = function(o) {
    var i = this, l = this.props.enter, s = this.context ? this.context.isMounting : o, a = this.props.nodeRef ? [s] : [fi.findDOMNode(this), s], u = a[0], c = a[1], d = this.getTimeouts(), p = s ? d.appear : d.enter;
    if (!o && !l || vd.disabled) {
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
      i.props.onEntering(u, c), i.onTransitionEnd(p, function() {
        i.safeSetState({
          status: Gn
        }, function() {
          i.props.onEntered(u, c);
        });
      });
    });
  }, n.performExit = function() {
    var o = this, i = this.props.exit, l = this.getTimeouts(), s = this.props.nodeRef ? void 0 : fi.findDOMNode(this);
    if (!i || vd.disabled) {
      this.safeSetState({
        status: kn
      }, function() {
        o.props.onExited(s);
      });
      return;
    }
    this.props.onExit(s), this.safeSetState({
      status: Ya
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
    if (o === eo)
      return null;
    var i = this.props, l = i.children;
    i.in, i.mountOnEnter, i.unmountOnExit, i.appear, i.enter, i.exit, i.timeout, i.addEndListener, i.onEnter, i.onEntering, i.onEntered, i.onExit, i.onExiting, i.onExited, i.nodeRef;
    var s = W(i, ["children", "in", "mountOnEnter", "unmountOnExit", "appear", "enter", "exit", "timeout", "addEndListener", "onEnter", "onEntering", "onEntered", "onExit", "onExiting", "onExited", "nodeRef"]);
    return (
      // allows for nested Transitions
      /* @__PURE__ */ qe.createElement(il.Provider, {
        value: null
      }, typeof l == "function" ? l(o, s) : qe.cloneElement(qe.Children.only(l), s))
    );
  }, t;
}(qe.Component);
Xt.contextType = il;
Xt.propTypes = {};
function Hn() {
}
Xt.defaultProps = {
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
Xt.UNMOUNTED = eo;
Xt.EXITED = kn;
Xt.ENTERING = En;
Xt.ENTERED = Gn;
Xt.EXITING = Ya;
const Ww = Xt;
function Vw(e) {
  if (e === void 0)
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function gc(e, t) {
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
function Tn(e, t, n) {
  return n[t] != null ? n[t] : e.props[t];
}
function Gw(e, t) {
  return gc(e.children, function(n) {
    return w.cloneElement(n, {
      onExited: t.bind(null, n),
      in: !0,
      appear: Tn(n, "appear", e),
      enter: Tn(n, "enter", e),
      exit: Tn(n, "exit", e)
    });
  });
}
function Kw(e, t, n) {
  var r = gc(e.children), o = Hw(t, r);
  return Object.keys(o).forEach(function(i) {
    var l = o[i];
    if (w.isValidElement(l)) {
      var s = i in t, a = i in r, u = t[i], c = w.isValidElement(u) && !u.props.in;
      a && (!s || c) ? o[i] = w.cloneElement(l, {
        onExited: n.bind(null, l),
        in: !0,
        exit: Tn(l, "exit", e),
        enter: Tn(l, "enter", e)
      }) : !a && s && !c ? o[i] = w.cloneElement(l, {
        in: !1
      }) : a && s && w.isValidElement(u) && (o[i] = w.cloneElement(l, {
        onExited: n.bind(null, l),
        in: u.props.in,
        exit: Tn(l, "exit", e),
        enter: Tn(l, "enter", e)
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
}, yc = /* @__PURE__ */ function(e) {
  Vh(t, e);
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
    var l = gc(this.props.children);
    o.key in l || (o.props.onExited && o.props.onExited(i), this.mounted && this.setState(function(s) {
      var a = S({}, s.children);
      return delete a[o.key], {
        children: a
      };
    }));
  }, n.render = function() {
    var o = this.props, i = o.component, l = o.childFactory, s = W(o, ["component", "childFactory"]), a = this.state.contextValue, u = Qw(this.state.children).map(l);
    return delete s.appear, delete s.enter, delete s.exit, i === null ? /* @__PURE__ */ qe.createElement(il.Provider, {
      value: a
    }, u) : /* @__PURE__ */ qe.createElement(il.Provider, {
      value: a
    }, /* @__PURE__ */ qe.createElement(i, s, u));
  }, t;
}(qe.Component);
yc.propTypes = {};
yc.defaultProps = Yw;
const Xw = yc;
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
  } = e, [c, d] = w.useState(!1), p = G(t, n.ripple, n.rippleVisible, r && n.ripplePulsate), v = {
    width: l,
    height: l,
    top: -(l / 2) + i,
    left: -(l / 2) + o
  }, y = G(n.child, c && n.childLeaving, r && n.childPulsate);
  return !s && !c && d(!0), w.useEffect(() => {
    if (!s && a != null) {
      const g = setTimeout(a, u);
      return () => {
        clearTimeout(g);
      };
    }
  }, [a, s, u]), /* @__PURE__ */ k.jsx("span", {
    className: p,
    style: v,
    children: /* @__PURE__ */ k.jsx("span", {
      className: y
    })
  });
}
const qw = Ce("MuiTouchRipple", ["root", "ripple", "rippleVisible", "ripplePulsate", "child", "childLeaving", "childPulsate"]), st = qw, Jw = ["center", "classes", "className"];
let ls = (e) => e, xd, Sd, wd, Cd;
const Xa = 550, e2 = 80, t2 = Ir(xd || (xd = ls`
  0% {
    transform: scale(0);
    opacity: 0.1;
  }

  100% {
    transform: scale(1);
    opacity: 0.3;
  }
`)), n2 = Ir(Sd || (Sd = ls`
  0% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
`)), r2 = Ir(wd || (wd = ls`
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(0.92);
  }

  100% {
    transform: scale(1);
  }
`)), o2 = Z("span", {
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
}), i2 = Z(Zw, {
  name: "MuiTouchRipple",
  slot: "Ripple"
})(Cd || (Cd = ls`
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
`), st.rippleVisible, t2, Xa, ({
  theme: e
}) => e.transitions.easing.easeInOut, st.ripplePulsate, ({
  theme: e
}) => e.transitions.duration.shorter, st.child, st.childLeaving, n2, Xa, ({
  theme: e
}) => e.transitions.easing.easeInOut, st.childPulsate, r2, ({
  theme: e
}) => e.transitions.easing.easeInOut), l2 = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = $e({
    props: t,
    name: "MuiTouchRipple"
  }), {
    center: o = !1,
    classes: i = {},
    className: l
  } = r, s = W(r, Jw), [a, u] = w.useState([]), c = w.useRef(0), d = w.useRef(null);
  w.useEffect(() => {
    d.current && (d.current(), d.current = null);
  }, [a]);
  const p = w.useRef(!1), v = Rh(), y = w.useRef(null), g = w.useRef(null), $ = w.useCallback((x) => {
    const {
      pulsate: _,
      rippleX: E,
      rippleY: C,
      rippleSize: R,
      cb: z
    } = x;
    u((O) => [...O, /* @__PURE__ */ k.jsx(i2, {
      classes: {
        ripple: G(i.ripple, st.ripple),
        rippleVisible: G(i.rippleVisible, st.rippleVisible),
        ripplePulsate: G(i.ripplePulsate, st.ripplePulsate),
        child: G(i.child, st.child),
        childLeaving: G(i.childLeaving, st.childLeaving),
        childPulsate: G(i.childPulsate, st.childPulsate)
      },
      timeout: Xa,
      pulsate: _,
      rippleX: E,
      rippleY: C,
      rippleSize: R
    }, c.current)]), c.current += 1, d.current = z;
  }, [i]), m = w.useCallback((x = {}, _ = {}, E = () => {
  }) => {
    const {
      pulsate: C = !1,
      center: R = o || _.pulsate,
      fakeElement: z = !1
      // For test purposes
    } = _;
    if ((x == null ? void 0 : x.type) === "mousedown" && p.current) {
      p.current = !1;
      return;
    }
    (x == null ? void 0 : x.type) === "touchstart" && (p.current = !0);
    const O = z ? null : g.current, D = O ? O.getBoundingClientRect() : {
      width: 0,
      height: 0,
      left: 0,
      top: 0
    };
    let F, A, Y;
    if (R || x === void 0 || x.clientX === 0 && x.clientY === 0 || !x.clientX && !x.touches)
      F = Math.round(D.width / 2), A = Math.round(D.height / 2);
    else {
      const {
        clientX: te,
        clientY: ge
      } = x.touches && x.touches.length > 0 ? x.touches[0] : x;
      F = Math.round(te - D.left), A = Math.round(ge - D.top);
    }
    if (R)
      Y = Math.sqrt((2 * D.width ** 2 + D.height ** 2) / 3), Y % 2 === 0 && (Y += 1);
    else {
      const te = Math.max(Math.abs((O ? O.clientWidth : 0) - F), F) * 2 + 2, ge = Math.max(Math.abs((O ? O.clientHeight : 0) - A), A) * 2 + 2;
      Y = Math.sqrt(te ** 2 + ge ** 2);
    }
    x != null && x.touches ? y.current === null && (y.current = () => {
      $({
        pulsate: C,
        rippleX: F,
        rippleY: A,
        rippleSize: Y,
        cb: E
      });
    }, v.start(e2, () => {
      y.current && (y.current(), y.current = null);
    })) : $({
      pulsate: C,
      rippleX: F,
      rippleY: A,
      rippleSize: Y,
      cb: E
    });
  }, [o, $, v]), f = w.useCallback(() => {
    m({}, {
      pulsate: !0
    });
  }, [m]), h = w.useCallback((x, _) => {
    if (v.clear(), (x == null ? void 0 : x.type) === "touchend" && y.current) {
      y.current(), y.current = null, v.start(0, () => {
        h(x, _);
      });
      return;
    }
    y.current = null, u((E) => E.length > 0 ? E.slice(1) : E), d.current = _;
  }, [v]);
  return w.useImperativeHandle(n, () => ({
    pulsate: f,
    start: m,
    stop: h
  }), [f, m, h]), /* @__PURE__ */ k.jsx(o2, S({
    className: G(st.root, i.root, l),
    ref: g
  }, s, {
    children: /* @__PURE__ */ k.jsx(Xw, {
      component: null,
      exit: !0,
      children: a
    })
  }));
}), s2 = l2;
function a2(e) {
  return Ne("MuiButtonBase", e);
}
const u2 = Ce("MuiButtonBase", ["root", "disabled", "focusVisible"]), c2 = u2, f2 = ["action", "centerRipple", "children", "className", "component", "disabled", "disableRipple", "disableTouchRipple", "focusRipple", "focusVisibleClassName", "LinkComponent", "onBlur", "onClick", "onContextMenu", "onDragLeave", "onFocus", "onFocusVisible", "onKeyDown", "onKeyUp", "onMouseDown", "onMouseLeave", "onMouseUp", "onTouchEnd", "onTouchMove", "onTouchStart", "tabIndex", "TouchRippleProps", "touchRippleRef", "type"], d2 = (e) => {
  const {
    disabled: t,
    focusVisible: n,
    focusVisibleClassName: r,
    classes: o
  } = e, l = be({
    root: ["root", t && "disabled", n && "focusVisible"]
  }, a2, o);
  return n && r && (l.root += ` ${r}`), l;
}, p2 = Z("button", {
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
  const r = $e({
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
    onBlur: y,
    onClick: g,
    onContextMenu: $,
    onDragLeave: m,
    onFocus: f,
    onFocusVisible: h,
    onKeyDown: x,
    onKeyUp: _,
    onMouseDown: E,
    onMouseLeave: C,
    onMouseUp: R,
    onTouchEnd: z,
    onTouchMove: O,
    onTouchStart: D,
    tabIndex: F = 0,
    TouchRippleProps: A,
    touchRippleRef: Y,
    type: te
  } = r, ge = W(r, f2), de = w.useRef(null), T = w.useRef(null), N = _r(T, Y), {
    isFocusVisibleRef: I,
    onFocus: B,
    onBlur: ae,
    ref: Zt
  } = Oh(), [Pe, Tt] = w.useState(!1);
  u && Pe && Tt(!1), w.useImperativeHandle(o, () => ({
    focusVisible: () => {
      Tt(!0), de.current.focus();
    }
  }), []);
  const [L, xe] = w.useState(!1);
  w.useEffect(() => {
    xe(!0);
  }, []);
  const St = L && !c && !u;
  w.useEffect(() => {
    Pe && p && !c && L && T.current.pulsate();
  }, [c, p, Pe, L]);
  function De(j, wc, h0 = d) {
    return Jr((Cc) => (wc && wc(Cc), !h0 && T.current && T.current[j](Cc), !0));
  }
  const bn = De("start", E), Go = De("stop", $), r0 = De("stop", m), o0 = De("stop", R), i0 = De("stop", (j) => {
    Pe && j.preventDefault(), C && C(j);
  }), l0 = De("start", D), s0 = De("stop", z), a0 = De("stop", O), u0 = De("stop", (j) => {
    ae(j), I.current === !1 && Tt(!1), y && y(j);
  }, !1), c0 = Jr((j) => {
    de.current || (de.current = j.currentTarget), B(j), I.current === !0 && (Tt(!0), h && h(j)), f && f(j);
  }), ss = () => {
    const j = de.current;
    return a && a !== "button" && !(j.tagName === "A" && j.href);
  }, as = w.useRef(!1), f0 = Jr((j) => {
    p && !as.current && Pe && T.current && j.key === " " && (as.current = !0, T.current.stop(j, () => {
      T.current.start(j);
    })), j.target === j.currentTarget && ss() && j.key === " " && j.preventDefault(), x && x(j), j.target === j.currentTarget && ss() && j.key === "Enter" && !u && (j.preventDefault(), g && g(j));
  }), d0 = Jr((j) => {
    p && j.key === " " && T.current && Pe && !j.defaultPrevented && (as.current = !1, T.current.stop(j, () => {
      T.current.pulsate(j);
    })), _ && _(j), g && j.target === j.currentTarget && ss() && j.key === " " && !j.defaultPrevented && g(j);
  });
  let Ko = a;
  Ko === "button" && (ge.href || ge.to) && (Ko = v);
  const Ar = {};
  Ko === "button" ? (Ar.type = te === void 0 ? "button" : te, Ar.disabled = u) : (!ge.href && !ge.to && (Ar.role = "button"), u && (Ar["aria-disabled"] = u));
  const p0 = _r(n, Zt, de), Sc = S({}, r, {
    centerRipple: i,
    component: a,
    disabled: u,
    disableRipple: c,
    disableTouchRipple: d,
    focusRipple: p,
    tabIndex: F,
    focusVisible: Pe
  }), m0 = d2(Sc);
  return /* @__PURE__ */ k.jsxs(p2, S({
    as: Ko,
    className: G(m0.root, s),
    ownerState: Sc,
    onBlur: u0,
    onClick: g,
    onContextMenu: Go,
    onFocus: c0,
    onKeyDown: f0,
    onKeyUp: d0,
    onMouseDown: bn,
    onMouseLeave: i0,
    onMouseUp: o0,
    onDragLeave: r0,
    onTouchEnd: s0,
    onTouchMove: a0,
    onTouchStart: l0,
    ref: p0,
    tabIndex: u ? -1 : F,
    type: te
  }, Ar, ge, {
    children: [l, St ? (
      /* TouchRipple is only needed client-side, x2 boost on the server. */
      /* @__PURE__ */ k.jsx(s2, S({
        ref: N,
        center: i
      }, A))
    ) : null]
  }));
}), Hh = m2;
function h2(e) {
  return Ne("MuiIconButton", e);
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
  return be(l, h2, t);
}, S2 = Z(Hh, {
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
    backgroundColor: e.vars ? `rgba(${e.vars.palette.action.activeChannel} / ${e.vars.palette.action.hoverOpacity})` : Ut(e.palette.action.active, e.palette.action.hoverOpacity),
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
      backgroundColor: e.vars ? `rgba(${r.mainChannel} / ${e.vars.palette.action.hoverOpacity})` : Ut(r.main, e.palette.action.hoverOpacity)
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
  const r = $e({
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
  } = r, d = W(r, v2), p = S({}, r, {
    edge: o,
    color: s,
    disabled: a,
    disableFocusRipple: u,
    size: c
  }), v = x2(p);
  return /* @__PURE__ */ k.jsx(S2, S({
    className: G(v.root, l),
    centerRipple: !0,
    focusRipple: !u,
    disabled: a,
    ref: n
  }, d, {
    ownerState: p,
    children: i
  }));
}), C2 = w2;
function k2(e) {
  return Ne("MuiSvgIcon", e);
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
  return be(o, k2, r);
}, $2 = Z("svg", {
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
  var n, r, o, i, l, s, a, u, c, d, p, v, y;
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
      disabled: (y = (e.vars || e).palette) == null || (y = y.action) == null ? void 0 : y.disabled,
      inherit: void 0
    }[t.color]
  };
}), Gh = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = $e({
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
  } = r, v = W(r, E2), y = /* @__PURE__ */ w.isValidElement(o) && o.type === "svg", g = S({}, r, {
    color: l,
    component: s,
    fontSize: a,
    instanceFontSize: t.fontSize,
    inheritViewBox: c,
    viewBox: p,
    hasSvgAsChild: y
  }), $ = {};
  c || ($.viewBox = p);
  const m = _2(g);
  return /* @__PURE__ */ k.jsxs($2, S({
    as: s,
    className: G(m.root, i),
    focusable: "false",
    color: u,
    "aria-hidden": d ? void 0 : !0,
    role: d ? "img" : void 0,
    ref: n
  }, $, v, y && o.props, {
    ownerState: g,
    children: [y ? o.props.children : o, d ? /* @__PURE__ */ k.jsx("title", {
      children: d
    }) : null]
  }));
});
Gh.muiName = "SvgIcon";
const kd = Gh;
function jr(e, t) {
  function n(r, o) {
    return /* @__PURE__ */ k.jsx(kd, S({
      "data-testid": `${t}Icon`,
      ref: o
    }, r, {
      children: e
    }));
  }
  return n.muiName = kd.muiName, /* @__PURE__ */ w.memo(/* @__PURE__ */ w.forwardRef(n));
}
const P2 = jr(/* @__PURE__ */ k.jsx("path", {
  d: "M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2, 4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0, 0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"
}), "SuccessOutlined"), T2 = jr(/* @__PURE__ */ k.jsx("path", {
  d: "M12 5.99L19.53 19H4.47L12 5.99M12 2L1 21h22L12 2zm1 14h-2v2h2v-2zm0-6h-2v4h2v-4z"
}), "ReportProblemOutlined"), R2 = jr(/* @__PURE__ */ k.jsx("path", {
  d: "M11 15h2v2h-2zm0-8h2v6h-2zm.99-5C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"
}), "ErrorOutline"), O2 = jr(/* @__PURE__ */ k.jsx("path", {
  d: "M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"
}), "InfoOutlined"), M2 = jr(/* @__PURE__ */ k.jsx("path", {
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
  return be(i, Fw, o);
}, L2 = Z($r, {
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
  const t = e.palette.mode === "light" ? Ha : Ga, n = e.palette.mode === "light" ? Ga : Ha;
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
        [`& .${yd.icon}`]: e.vars ? {
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
        [`& .${yd.icon}`]: e.vars ? {
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
}), z2 = Z("div", {
  name: "MuiAlert",
  slot: "Icon",
  overridesResolver: (e, t) => t.icon
})({
  marginRight: 12,
  padding: "7px 0",
  display: "flex",
  fontSize: 22,
  opacity: 0.9
}), j2 = Z("div", {
  name: "MuiAlert",
  slot: "Message",
  overridesResolver: (e, t) => t.message
})({
  padding: "8px 0",
  minWidth: 0,
  overflow: "auto"
}), Ed = Z("div", {
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
  success: /* @__PURE__ */ k.jsx(P2, {
    fontSize: "inherit"
  }),
  warning: /* @__PURE__ */ k.jsx(T2, {
    fontSize: "inherit"
  }),
  error: /* @__PURE__ */ k.jsx(R2, {
    fontSize: "inherit"
  }),
  info: /* @__PURE__ */ k.jsx(O2, {
    fontSize: "inherit"
  })
}, A2 = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = $e({
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
    iconMapping: p = _d,
    onClose: v,
    role: y = "alert",
    severity: g = "success",
    slotProps: $ = {},
    slots: m = {},
    variant: f = "standard"
  } = r, h = W(r, N2), x = S({}, r, {
    color: a,
    severity: g,
    variant: f,
    colorSeverity: a || g
  }), _ = I2(x), E = {
    slots: S({
      closeButton: u.CloseButton,
      closeIcon: u.CloseIcon
    }, m),
    slotProps: S({}, c, $)
  }, [C, R] = gd("closeButton", {
    elementType: C2,
    externalForwardedProps: E,
    ownerState: x
  }), [z, O] = gd("closeIcon", {
    elementType: M2,
    externalForwardedProps: E,
    ownerState: x
  });
  return /* @__PURE__ */ k.jsxs(L2, S({
    role: y,
    elevation: 0,
    ownerState: x,
    className: G(_.root, l),
    ref: n
  }, h, {
    children: [d !== !1 ? /* @__PURE__ */ k.jsx(z2, {
      ownerState: x,
      className: _.icon,
      children: d || p[g] || _d[g]
    }) : null, /* @__PURE__ */ k.jsx(j2, {
      ownerState: x,
      className: _.message,
      children: i
    }), o != null ? /* @__PURE__ */ k.jsx(Ed, {
      ownerState: x,
      className: _.action,
      children: o
    }) : null, o == null && v ? /* @__PURE__ */ k.jsx(Ed, {
      ownerState: x,
      className: _.action,
      children: /* @__PURE__ */ k.jsx(C, S({
        size: "small",
        "aria-label": s,
        title: s,
        color: "inherit",
        onClick: v
      }, R, {
        children: /* @__PURE__ */ k.jsx(z, S({
          fontSize: "small"
        }, O))
      }))
    }) : null]
  }));
}), b2 = A2, D2 = Ce("MuiBox", ["root"]), F2 = D2, B2 = mc(), U2 = ix({
  themeId: kr,
  defaultTheme: B2,
  defaultClassName: F2.root,
  generateClassName: ac.generate
}), Pr = U2, W2 = /* @__PURE__ */ w.createContext(), $d = W2;
function V2(e) {
  return Ne("MuiGrid", e);
}
const H2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], G2 = ["column-reverse", "column", "row-reverse", "row"], K2 = ["nowrap", "wrap-reverse", "wrap"], Qr = ["auto", !0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], Lo = Ce("MuiGrid", [
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
  ...Qr.map((e) => `grid-xs-${e}`),
  ...Qr.map((e) => `grid-sm-${e}`),
  ...Qr.map((e) => `grid-md-${e}`),
  ...Qr.map((e) => `grid-lg-${e}`),
  ...Qr.map((e) => `grid-xl-${e}`)
]), Q2 = ["className", "columns", "columnSpacing", "component", "container", "direction", "item", "rowSpacing", "spacing", "wrap", "zeroMinWidth"];
function mr(e) {
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
      const l = jl({
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
  const n = jl({
    values: t.direction,
    breakpoints: e.breakpoints.values
  });
  return gt({
    theme: e
  }, n, (r) => {
    const o = {
      flexDirection: r
    };
    return r.indexOf("column") === 0 && (o[`& > .${Lo.item}`] = {
      maxWidth: "none"
    }), o;
  });
}
function Kh({
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
    const i = jl({
      values: r,
      breakpoints: e.breakpoints.values
    });
    let l;
    typeof i == "object" && (l = Kh({
      breakpoints: e.breakpoints.values,
      values: i
    })), o = gt({
      theme: e
    }, i, (s, a) => {
      var u;
      const c = e.spacing(s);
      return c !== "0px" ? {
        marginTop: `-${mr(c)}`,
        [`& > .${Lo.item}`]: {
          paddingTop: mr(c)
        }
      } : (u = l) != null && u.includes(a) ? {} : {
        marginTop: 0,
        [`& > .${Lo.item}`]: {
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
    const i = jl({
      values: r,
      breakpoints: e.breakpoints.values
    });
    let l;
    typeof i == "object" && (l = Kh({
      breakpoints: e.breakpoints.values,
      values: i
    })), o = gt({
      theme: e
    }, i, (s, a) => {
      var u;
      const c = e.spacing(s);
      return c !== "0px" ? {
        width: `calc(100% + ${mr(c)})`,
        marginLeft: `-${mr(c)}`,
        [`& > .${Lo.item}`]: {
          paddingLeft: mr(c)
        }
      } : (u = l) != null && u.includes(a) ? {} : {
        width: "100%",
        marginLeft: 0,
        [`& > .${Lo.item}`]: {
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
const eC = Z("div", {
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
    const d = [];
    return u.forEach((p) => {
      const v = n[p];
      v && d.push(t[`grid-${p}-${String(v)}`]);
    }), [t.root, r && t.container, i && t.item, a && t.zeroMinWidth, ...c, o !== "row" && t[`direction-xs-${String(o)}`], s !== "wrap" && t[`wrap-xs-${String(s)}`], ...d];
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
  a.forEach((p) => {
    const v = e[p];
    v && c.push(`grid-${p}-${String(v)}`);
  });
  const d = {
    root: ["root", n && "container", o && "item", s && "zeroMinWidth", ...u, r !== "row" && `direction-xs-${String(r)}`, l !== "wrap" && `wrap-xs-${String(l)}`, ...c]
  };
  return be(d, V2, t);
}, rC = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = $e({
    props: t,
    name: "MuiGrid"
  }), {
    breakpoints: o
  } = Uh(), i = Vl(r), {
    className: l,
    columns: s,
    columnSpacing: a,
    component: u = "div",
    container: c = !1,
    direction: d = "row",
    item: p = !1,
    rowSpacing: v,
    spacing: y = 0,
    wrap: g = "wrap",
    zeroMinWidth: $ = !1
  } = i, m = W(i, Q2), f = v || y, h = a || y, x = w.useContext($d), _ = c ? s || 12 : x, E = {}, C = S({}, m);
  o.keys.forEach((O) => {
    m[O] != null && (E[O] = m[O], delete C[O]);
  });
  const R = S({}, i, {
    columns: _,
    container: c,
    direction: d,
    item: p,
    rowSpacing: f,
    columnSpacing: h,
    wrap: g,
    zeroMinWidth: $,
    spacing: y
  }, E, {
    breakpoints: o.keys
  }), z = nC(R);
  return /* @__PURE__ */ k.jsx($d.Provider, {
    value: _,
    children: /* @__PURE__ */ k.jsx(eC, S({
      ownerState: R,
      className: G(z.root, l),
      as: u,
      ref: n
    }, C))
  });
}), Us = rC;
function oC(e) {
  return Ne("MuiTypography", e);
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
  return be(s, oC, l);
}, sC = Z("span", {
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
})), Pd = {
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
  const r = $e({
    props: t,
    name: "MuiTypography"
  }), o = uC(r.color), i = Vl(S({}, r, {
    color: o
  })), {
    align: l = "inherit",
    className: s,
    component: a,
    gutterBottom: u = !1,
    noWrap: c = !1,
    paragraph: d = !1,
    variant: p = "body1",
    variantMapping: v = Pd
  } = i, y = W(i, iC), g = S({}, i, {
    align: l,
    color: o,
    className: s,
    component: a,
    gutterBottom: u,
    noWrap: c,
    paragraph: d,
    variant: p,
    variantMapping: v
  }), $ = a || (d ? "p" : v[p] || Pd[p]) || "span", m = lC(g);
  return /* @__PURE__ */ k.jsx(sC, S({
    as: $,
    ref: n,
    ownerState: g,
    className: G(m.root, s)
  }, y));
}), dt = cC, fC = () => /* @__PURE__ */ k.jsx(
  $r,
  {
    elevation: 2,
    sx: {
      p: 2,
      mb: 3,
      textAlign: "center"
    },
    children: /* @__PURE__ */ k.jsx(dt, { variant: "h4", component: "h1", children: "Meraki Integration Control" })
  }
), dC = /* @__PURE__ */ w.createContext({}), hr = dC;
function pC(e) {
  return Ne("MuiList", e);
}
Ce("MuiList", ["root", "padding", "dense", "subheader"]);
const mC = ["children", "className", "component", "dense", "disablePadding", "subheader"], hC = (e) => {
  const {
    classes: t,
    disablePadding: n,
    dense: r,
    subheader: o
  } = e;
  return be({
    root: ["root", !n && "padding", r && "dense", o && "subheader"]
  }, pC, t);
}, gC = Z("ul", {
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
  const r = $e({
    props: t,
    name: "MuiList"
  }), {
    children: o,
    className: i,
    component: l = "ul",
    dense: s = !1,
    disablePadding: a = !1,
    subheader: u
  } = r, c = W(r, mC), d = w.useMemo(() => ({
    dense: s
  }), [s]), p = S({}, r, {
    component: l,
    dense: s,
    disablePadding: a
  }), v = hC(p);
  return /* @__PURE__ */ k.jsx(hr.Provider, {
    value: d,
    children: /* @__PURE__ */ k.jsxs(gC, S({
      as: l,
      className: G(v.root, i),
      ref: n,
      ownerState: p
    }, c, {
      children: [u, o]
    }))
  });
}), Qh = yC;
function vC(e) {
  return Ne("MuiListItem", e);
}
const xC = Ce("MuiListItem", ["root", "container", "focusVisible", "dense", "alignItemsFlexStart", "disabled", "divider", "gutters", "padding", "button", "secondaryAction", "selected"]), Kn = xC, SC = Ce("MuiListItemButton", ["root", "focusVisible", "dense", "alignItemsFlexStart", "disabled", "divider", "gutters", "selected"]), wC = SC;
function CC(e) {
  return Ne("MuiListItemSecondaryAction", e);
}
Ce("MuiListItemSecondaryAction", ["root", "disableGutters"]);
const kC = ["className"], EC = (e) => {
  const {
    disableGutters: t,
    classes: n
  } = e;
  return be({
    root: ["root", t && "disableGutters"]
  }, CC, n);
}, _C = Z("div", {
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
})), Yh = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = $e({
    props: t,
    name: "MuiListItemSecondaryAction"
  }), {
    className: o
  } = r, i = W(r, kC), l = w.useContext(hr), s = S({}, r, {
    disableGutters: l.disableGutters
  }), a = EC(s);
  return /* @__PURE__ */ k.jsx(_C, S({
    className: G(a.root, o),
    ownerState: s,
    ref: n
  }, i));
});
Yh.muiName = "ListItemSecondaryAction";
const $C = Yh, PC = ["className"], TC = ["alignItems", "autoFocus", "button", "children", "className", "component", "components", "componentsProps", "ContainerComponent", "ContainerProps", "dense", "disabled", "disableGutters", "disablePadding", "divider", "focusVisibleClassName", "secondaryAction", "selected", "slotProps", "slots"], RC = (e, t) => {
  const {
    ownerState: n
  } = e;
  return [t.root, n.dense && t.dense, n.alignItems === "flex-start" && t.alignItemsFlexStart, n.divider && t.divider, !n.disableGutters && t.gutters, !n.disablePadding && t.padding, n.button && t.button, n.hasSecondaryAction && t.secondaryAction];
}, OC = (e) => {
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
  return be({
    root: ["root", o && "dense", !l && "gutters", !s && "padding", a && "divider", i && "disabled", n && "button", t === "flex-start" && "alignItemsFlexStart", u && "secondaryAction", c && "selected"],
    container: ["container"]
  }, vC, r);
}, MC = Z("div", {
  name: "MuiListItem",
  slot: "Root",
  overridesResolver: RC
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
  [`& > .${wC.root}`]: {
    paddingRight: 48
  }
}, {
  [`&.${Kn.focusVisible}`]: {
    backgroundColor: (e.vars || e).palette.action.focus
  },
  [`&.${Kn.selected}`]: {
    backgroundColor: e.vars ? `rgba(${e.vars.palette.primary.mainChannel} / ${e.vars.palette.action.selectedOpacity})` : Ut(e.palette.primary.main, e.palette.action.selectedOpacity),
    [`&.${Kn.focusVisible}`]: {
      backgroundColor: e.vars ? `rgba(${e.vars.palette.primary.mainChannel} / calc(${e.vars.palette.action.selectedOpacity} + ${e.vars.palette.action.focusOpacity}))` : Ut(e.palette.primary.main, e.palette.action.selectedOpacity + e.palette.action.focusOpacity)
    }
  },
  [`&.${Kn.disabled}`]: {
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
  [`&.${Kn.selected}:hover`]: {
    backgroundColor: e.vars ? `rgba(${e.vars.palette.primary.mainChannel} / calc(${e.vars.palette.action.selectedOpacity} + ${e.vars.palette.action.hoverOpacity}))` : Ut(e.palette.primary.main, e.palette.action.selectedOpacity + e.palette.action.hoverOpacity),
    // Reset on touch devices, it doesn't add specificity
    "@media (hover: none)": {
      backgroundColor: e.vars ? `rgba(${e.vars.palette.primary.mainChannel} / ${e.vars.palette.action.selectedOpacity})` : Ut(e.palette.primary.main, e.palette.action.selectedOpacity)
    }
  }
}, t.hasSecondaryAction && {
  // Add some space to avoid collision as `ListItemSecondaryAction`
  // is absolutely positioned.
  paddingRight: 48
})), NC = Z("li", {
  name: "MuiListItem",
  slot: "Container",
  overridesResolver: (e, t) => t.container
})({
  position: "relative"
}), IC = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = $e({
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
    componentsProps: d = {},
    ContainerComponent: p = "li",
    ContainerProps: {
      className: v
    } = {},
    dense: y = !1,
    disabled: g = !1,
    disableGutters: $ = !1,
    disablePadding: m = !1,
    divider: f = !1,
    focusVisibleClassName: h,
    secondaryAction: x,
    selected: _ = !1,
    slotProps: E = {},
    slots: C = {}
  } = r, R = W(r.ContainerProps, PC), z = W(r, TC), O = w.useContext(hr), D = w.useMemo(() => ({
    dense: y || O.dense || !1,
    alignItems: o,
    disableGutters: $
  }), [o, O.dense, y, $]), F = w.useRef(null);
  ts(() => {
    i && F.current && F.current.focus();
  }, [i]);
  const A = w.Children.toArray(s), Y = A.length && _h(A[A.length - 1], ["ListItemSecondaryAction"]), te = S({}, r, {
    alignItems: o,
    autoFocus: i,
    button: l,
    dense: D.dense,
    disabled: g,
    disableGutters: $,
    disablePadding: m,
    divider: f,
    hasSecondaryAction: Y,
    selected: _
  }), ge = OC(te), de = _r(F, n), T = C.root || c.Root || MC, N = E.root || d.root || {}, I = S({
    className: G(ge.root, N.className, a),
    disabled: g
  }, z);
  let B = u || "li";
  return l && (I.component = u || "div", I.focusVisibleClassName = G(Kn.focusVisible, h), B = Hh), Y ? (B = !I.component && !u ? "div" : B, p === "li" && (B === "li" ? B = "div" : I.component === "li" && (I.component = "div")), /* @__PURE__ */ k.jsx(hr.Provider, {
    value: D,
    children: /* @__PURE__ */ k.jsxs(NC, S({
      as: p,
      className: G(ge.container, v),
      ref: de,
      ownerState: te
    }, R, {
      children: [/* @__PURE__ */ k.jsx(T, S({}, N, !Va(T) && {
        as: B,
        ownerState: S({}, te, N.ownerState)
      }, I, {
        children: A
      })), A.pop()]
    }))
  })) : /* @__PURE__ */ k.jsx(hr.Provider, {
    value: D,
    children: /* @__PURE__ */ k.jsxs(T, S({}, N, {
      as: B,
      ref: de
    }, !Va(T) && {
      ownerState: S({}, te, N.ownerState)
    }, I, {
      children: [A, x && /* @__PURE__ */ k.jsx($C, {
        children: x
      })]
    }))
  });
}), Xh = IC;
function LC(e) {
  return Ne("MuiListItemText", e);
}
const zC = Ce("MuiListItemText", ["root", "multiline", "dense", "inset", "primary", "secondary"]), Td = zC, jC = ["children", "className", "disableTypography", "inset", "primary", "primaryTypographyProps", "secondary", "secondaryTypographyProps"], AC = (e) => {
  const {
    classes: t,
    inset: n,
    primary: r,
    secondary: o,
    dense: i
  } = e;
  return be({
    root: ["root", n && "inset", i && "dense", r && o && "multiline"],
    primary: ["primary"],
    secondary: ["secondary"]
  }, LC, t);
}, bC = Z("div", {
  name: "MuiListItemText",
  slot: "Root",
  overridesResolver: (e, t) => {
    const {
      ownerState: n
    } = e;
    return [{
      [`& .${Td.primary}`]: t.primary
    }, {
      [`& .${Td.secondary}`]: t.secondary
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
})), DC = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = $e({
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
    secondaryTypographyProps: d
  } = r, p = W(r, jC), {
    dense: v
  } = w.useContext(hr);
  let y = a ?? o, g = c;
  const $ = S({}, r, {
    disableTypography: l,
    inset: s,
    primary: !!y,
    secondary: !!g,
    dense: v
  }), m = AC($);
  return y != null && y.type !== dt && !l && (y = /* @__PURE__ */ k.jsx(dt, S({
    variant: v ? "body2" : "body1",
    className: m.primary,
    component: u != null && u.variant ? void 0 : "span",
    display: "block"
  }, u, {
    children: y
  }))), g != null && g.type !== dt && !l && (g = /* @__PURE__ */ k.jsx(dt, S({
    variant: "body2",
    className: m.secondary,
    color: "text.secondary",
    display: "block"
  }, d, {
    children: g
  }))), /* @__PURE__ */ k.jsxs(bC, S({
    className: G(m.root, i),
    ownerState: $,
    ref: n
  }, p, {
    children: [y, g]
  }));
}), Zh = DC;
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
const FC = {
  configure: (e) => {
    ac.configure(e);
  }
}, BC = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  capitalize: le,
  createChainedFunction: hx,
  createSvgIcon: jr,
  debounce: gx,
  deprecatedPropType: yx,
  isMuiElement: _h,
  ownerDocument: $h,
  ownerWindow: vx,
  requirePropFactory: xx,
  setRef: Ph,
  unstable_ClassNameGenerator: FC,
  unstable_useEnhancedEffect: ts,
  unstable_useId: Th,
  unsupportedProp: wx,
  useControlled: Cx,
  useEventCallback: Jr,
  useForkRef: _r,
  useIsFocusVisible: Oh
}, Symbol.toStringTag, { value: "Module" }));
function UC(e) {
  return Ne("MuiCollapse", e);
}
Ce("MuiCollapse", ["root", "horizontal", "vertical", "entered", "hidden", "wrapper", "wrapperInner"]);
const WC = ["addEndListener", "children", "className", "collapsedSize", "component", "easing", "in", "onEnter", "onEntered", "onEntering", "onExit", "onExited", "onExiting", "orientation", "style", "timeout", "TransitionComponent"], VC = (e) => {
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
  return be(r, UC, n);
}, HC = Z("div", {
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
})), GC = Z("div", {
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
})), KC = Z("div", {
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
  const r = $e({
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
    onEntered: p,
    onEntering: v,
    onExit: y,
    onExited: g,
    onExiting: $,
    orientation: m = "vertical",
    style: f,
    timeout: h = Bh.standard,
    // eslint-disable-next-line react/prop-types
    TransitionComponent: x = Ww
  } = r, _ = W(r, WC), E = S({}, r, {
    orientation: m,
    collapsedSize: s
  }), C = VC(E), R = Uh(), z = Rh(), O = w.useRef(null), D = w.useRef(), F = typeof s == "number" ? `${s}px` : s, A = m === "horizontal", Y = A ? "width" : "height", te = w.useRef(null), ge = _r(n, te), de = (L) => (xe) => {
    if (L) {
      const St = te.current;
      xe === void 0 ? L(St) : L(St, xe);
    }
  }, T = () => O.current ? O.current[A ? "clientWidth" : "clientHeight"] : 0, N = de((L, xe) => {
    O.current && A && (O.current.style.position = "absolute"), L.style[Y] = F, d && d(L, xe);
  }), I = de((L, xe) => {
    const St = T();
    O.current && A && (O.current.style.position = "");
    const {
      duration: De,
      easing: bn
    } = Rd({
      style: f,
      timeout: h,
      easing: u
    }, {
      mode: "enter"
    });
    if (h === "auto") {
      const Go = R.transitions.getAutoHeightDuration(St);
      L.style.transitionDuration = `${Go}ms`, D.current = Go;
    } else
      L.style.transitionDuration = typeof De == "string" ? De : `${De}ms`;
    L.style[Y] = `${St}px`, L.style.transitionTimingFunction = bn, v && v(L, xe);
  }), B = de((L, xe) => {
    L.style[Y] = "auto", p && p(L, xe);
  }), ae = de((L) => {
    L.style[Y] = `${T()}px`, y && y(L);
  }), Zt = de(g), Pe = de((L) => {
    const xe = T(), {
      duration: St,
      easing: De
    } = Rd({
      style: f,
      timeout: h,
      easing: u
    }, {
      mode: "exit"
    });
    if (h === "auto") {
      const bn = R.transitions.getAutoHeightDuration(xe);
      L.style.transitionDuration = `${bn}ms`, D.current = bn;
    } else
      L.style.transitionDuration = typeof St == "string" ? St : `${St}ms`;
    L.style[Y] = F, L.style.transitionTimingFunction = De, $ && $(L);
  }), Tt = (L) => {
    h === "auto" && z.start(D.current || 0, L), o && o(te.current, L);
  };
  return /* @__PURE__ */ k.jsx(x, S({
    in: c,
    onEnter: N,
    onEntered: B,
    onEntering: I,
    onExit: ae,
    onExited: Zt,
    onExiting: Pe,
    addEndListener: Tt,
    nodeRef: te,
    timeout: h === "auto" ? null : h
  }, _, {
    children: (L, xe) => /* @__PURE__ */ k.jsx(HC, S({
      as: a,
      className: G(C.root, l, {
        entered: C.entered,
        exited: !c && F === "0px" && C.hidden
      }[L]),
      style: S({
        [A ? "minWidth" : "minHeight"]: F
      }, f),
      ref: ge
    }, xe, {
      // `ownerState` is set after `childProps` to override any existing `ownerState` property in `childProps`
      // that might have been forwarded from the Transition component.
      ownerState: S({}, E, {
        state: L
      }),
      children: /* @__PURE__ */ k.jsx(GC, {
        ownerState: S({}, E, {
          state: L
        }),
        className: C.wrapper,
        ref: O,
        children: /* @__PURE__ */ k.jsx(KC, {
          ownerState: S({}, E, {
            state: L
          }),
          className: C.wrapperInner,
          children: i
        })
      })
    }))
  }));
});
qh.muiSupportAuto = !0;
const QC = qh;
var vc = {}, Ws = {};
const YC = /* @__PURE__ */ Qt(BC);
var Od;
function Jh() {
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
    var t = YC;
  }(Ws)), Ws;
}
var XC = os;
Object.defineProperty(vc, "__esModule", {
  value: !0
});
var e0 = vc.default = void 0, ZC = XC(Jh()), qC = k;
e0 = vc.default = (0, ZC.default)(/* @__PURE__ */ (0, qC.jsx)("path", {
  d: "m12 8-6 6 1.41 1.41L12 10.83l4.59 4.58L18 14z"
}), "ExpandLess");
var xc = {}, JC = os;
Object.defineProperty(xc, "__esModule", {
  value: !0
});
var t0 = xc.default = void 0, ek = JC(Jh()), tk = k;
t0 = xc.default = (0, ek.default)(/* @__PURE__ */ (0, tk.jsx)("path", {
  d: "M16.59 8.59 12 13.17 7.41 8.59 6 10l6 6 6-6z"
}), "ExpandMore");
function nk(e) {
  return Ne("MuiDivider", e);
}
Ce("MuiDivider", ["root", "absolute", "fullWidth", "inset", "middle", "flexItem", "light", "vertical", "withChildren", "withChildrenVertical", "textAlignRight", "textAlignLeft", "wrapper", "wrapperVertical"]);
const rk = ["absolute", "children", "className", "component", "flexItem", "light", "orientation", "role", "textAlign", "variant"], ok = (e) => {
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
  return be({
    root: ["root", t && "absolute", a, i && "light", l === "vertical" && "vertical", o && "flexItem", n && "withChildren", n && l === "vertical" && "withChildrenVertical", s === "right" && l !== "vertical" && "textAlignRight", s === "left" && l !== "vertical" && "textAlignLeft"],
    wrapper: ["wrapper", l === "vertical" && "wrapperVertical"]
  }, nk, r);
}, ik = Z("div", {
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
  borderColor: e.vars ? `rgba(${e.vars.palette.dividerChannel} / 0.08)` : Ut(e.palette.divider, 0.08)
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
})), lk = Z("span", {
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
})), n0 = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = $e({
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
    role: d = s !== "hr" ? "separator" : void 0,
    textAlign: p = "center",
    variant: v = "fullWidth"
  } = r, y = W(r, rk), g = S({}, r, {
    absolute: o,
    component: s,
    flexItem: a,
    light: u,
    orientation: c,
    role: d,
    textAlign: p,
    variant: v
  }), $ = ok(g);
  return /* @__PURE__ */ k.jsx(ik, S({
    as: s,
    className: G($.root, l),
    role: d,
    ref: n,
    ownerState: g
  }, y, {
    children: i ? /* @__PURE__ */ k.jsx(lk, {
      className: $.wrapper,
      ownerState: g,
      children: i
    }) : null
  }));
});
n0.muiSkipListHighlight = !0;
const sk = n0, ak = ({ devices: e }) => !e || e.length === 0 ? /* @__PURE__ */ k.jsx(dt, { variant: "body2", children: "No devices found in this network." }) : /* @__PURE__ */ k.jsxs(Pr, { sx: { mt: 2 }, children: [
  /* @__PURE__ */ k.jsx(dt, { variant: "h6", gutterBottom: !0, children: "Devices" }),
  /* @__PURE__ */ k.jsx($r, { elevation: 1, children: /* @__PURE__ */ k.jsx(Qh, { dense: !0, children: e.map((t, n) => /* @__PURE__ */ k.jsxs(qe.Fragment, { children: [
    /* @__PURE__ */ k.jsx(Xh, { children: /* @__PURE__ */ k.jsx(
      Zh,
      {
        primary: t.name || "Unnamed Device",
        secondary: /* @__PURE__ */ k.jsxs(k.Fragment, { children: [
          /* @__PURE__ */ k.jsxs(dt, { component: "span", variant: "body2", color: "text.primary", children: [
            "Model: ",
            t.model,
            " | Status: ",
            t.status
          ] }),
          /* @__PURE__ */ k.jsx("br", {}),
          t.lanIp && `IP: ${t.lanIp} | `,
          t.mac && `MAC: ${t.mac}`
        ] })
      }
    ) }),
    n < e.length - 1 && /* @__PURE__ */ k.jsx(sk, {})
  ] }, t.serial)) }) })
] }), uk = ({ data: e }) => {
  const [t, n] = w.useState(null), r = (l) => {
    n(t === l ? null : l);
  }, { networks: o, devices: i } = e;
  return !o || o.length === 0 ? /* @__PURE__ */ k.jsx(dt, { children: "No networks found." }) : /* @__PURE__ */ k.jsxs(Pr, { children: [
    /* @__PURE__ */ k.jsx(dt, { variant: "h5", gutterBottom: !0, children: "Networks" }),
    /* @__PURE__ */ k.jsx(Qh, { component: "nav", children: o.map((l) => /* @__PURE__ */ k.jsxs(qe.Fragment, { children: [
      /* @__PURE__ */ k.jsxs(Xh, { button: !0, onClick: () => r(l.id), children: [
        /* @__PURE__ */ k.jsx(Zh, { primary: l.name }),
        t === l.id ? /* @__PURE__ */ k.jsx(e0, {}) : /* @__PURE__ */ k.jsx(t0, {})
      ] }),
      /* @__PURE__ */ k.jsx(QC, { in: t === l.id, timeout: "auto", unmountOnExit: !0, children: /* @__PURE__ */ k.jsx(Pr, { sx: { pl: 4, py: 1 }, children: /* @__PURE__ */ k.jsx(ak, { devices: i.filter((s) => s.networkId === l.id) }) }) })
    ] }, l.id)) })
  ] });
};
function ck(e) {
  return Ne("MuiCard", e);
}
Ce("MuiCard", ["root"]);
const fk = ["className", "raised"], dk = (e) => {
  const {
    classes: t
  } = e;
  return be({
    root: ["root"]
  }, ck, t);
}, pk = Z($r, {
  name: "MuiCard",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})(() => ({
  overflow: "hidden"
})), mk = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = $e({
    props: t,
    name: "MuiCard"
  }), {
    className: o,
    raised: i = !1
  } = r, l = W(r, fk), s = S({}, r, {
    raised: i
  }), a = dk(s);
  return /* @__PURE__ */ k.jsx(pk, S({
    className: G(a.root, o),
    elevation: i ? 8 : void 0,
    ref: n,
    ownerState: s
  }, l));
}), hk = mk;
function gk(e) {
  return Ne("MuiCardContent", e);
}
Ce("MuiCardContent", ["root"]);
const yk = ["className", "component"], vk = (e) => {
  const {
    classes: t
  } = e;
  return be({
    root: ["root"]
  }, gk, t);
}, xk = Z("div", {
  name: "MuiCardContent",
  slot: "Root",
  overridesResolver: (e, t) => t.root
})(() => ({
  padding: 16,
  "&:last-child": {
    paddingBottom: 24
  }
})), Sk = /* @__PURE__ */ w.forwardRef(function(t, n) {
  const r = $e({
    props: t,
    name: "MuiCardContent"
  }), {
    className: o,
    component: i = "div"
  } = r, l = W(r, yk), s = S({}, r, {
    component: i
  }), a = vk(s);
  return /* @__PURE__ */ k.jsx(xk, S({
    as: i,
    className: G(a.root, o),
    ownerState: s,
    ref: n
  }, l));
}), wk = Sk, Ck = () => /* @__PURE__ */ k.jsxs(Pr, { sx: { mt: 4 }, children: [
  /* @__PURE__ */ k.jsx(dt, { variant: "h5", component: "h2", sx: { mb: 2 }, children: "Event Log" }),
  /* @__PURE__ */ k.jsx(
    hk,
    {
      sx: {
        borderRadius: 2,
        boxShadow: "none",
        border: "1px solid",
        borderColor: "divider"
      },
      children: /* @__PURE__ */ k.jsx(wk, { sx: { p: 2.5 }, children: /* @__PURE__ */ k.jsx(dt, { color: "text.secondary", children: "Integration-specific events will be displayed here." }) })
    }
  )
] }), kk = (e) => {
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
}, Ek = (e) => mc(kk(e));
const _k = ({ hass: e, config_entry_id: t }) => {
  const [n, r] = w.useState(null), [o, i] = w.useState(!0), [l, s] = w.useState(null), a = w.useMemo(() => {
    var u;
    return Ek(((u = e == null ? void 0 : e.themes) == null ? void 0 : u.darkMode) ?? !0);
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
  }, [e, t]), /* @__PURE__ */ k.jsxs(hw, { theme: a, children: [
    /* @__PURE__ */ k.jsx(ww, {}),
    /* @__PURE__ */ k.jsxs(Pr, { sx: { p: 3, backgroundColor: a.palette.background.default, minHeight: "100vh" }, children: [
      /* @__PURE__ */ k.jsx(fC, {}),
      o && /* @__PURE__ */ k.jsx(Pr, { sx: { display: "flex", justifyContent: "center", p: 4 }, children: /* @__PURE__ */ k.jsx(Mw, {}) }),
      l && /* @__PURE__ */ k.jsx(b2, { severity: "error", sx: { mt: 2 }, children: l }),
      !o && !l && n && /* @__PURE__ */ k.jsxs(Us, { container: !0, spacing: 3, children: [
        /* @__PURE__ */ k.jsx(Us, { item: !0, xs: 12, children: /* @__PURE__ */ k.jsx($r, { elevation: 2, sx: { p: 2 }, children: /* @__PURE__ */ k.jsx(uk, { data: n }) }) }),
        /* @__PURE__ */ k.jsx(Us, { item: !0, xs: 12, children: /* @__PURE__ */ k.jsx($r, { elevation: 2, sx: { p: 2 }, children: /* @__PURE__ */ k.jsx(Ck, {}) }) })
      ] })
    ] })
  ] });
};
class $k extends HTMLElement {
  connectedCallback() {
    const t = document.createElement("div");
    t.id = "root", this.appendChild(t);
    const n = this.hass, r = this.panel.config.config_entry_id;
    Hs.createRoot(t).render(
      /* @__PURE__ */ k.jsx(qe.StrictMode, { children: /* @__PURE__ */ k.jsx(_k, { hass: n, config_entry_id: r }) })
    );
  }
}
customElements.define("meraki-panel", $k);
