function tc(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var Hu = { exports: {} }, el = {}, Wu = { exports: {} }, L = {};
/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Xt = Symbol.for("react.element"), rc = Symbol.for("react.portal"), lc = Symbol.for("react.fragment"), ic = Symbol.for("react.strict_mode"), oc = Symbol.for("react.profiler"), uc = Symbol.for("react.provider"), sc = Symbol.for("react.context"), ac = Symbol.for("react.forward_ref"), cc = Symbol.for("react.suspense"), fc = Symbol.for("react.memo"), dc = Symbol.for("react.lazy"), Oo = Symbol.iterator;
function pc(e) {
  return e === null || typeof e != "object" ? null : (e = Oo && e[Oo] || e["@@iterator"], typeof e == "function" ? e : null);
}
var Qu = { isMounted: function() {
  return !1;
}, enqueueForceUpdate: function() {
}, enqueueReplaceState: function() {
}, enqueueSetState: function() {
} }, Ku = Object.assign, Yu = {};
function it(e, n, t) {
  this.props = e, this.context = n, this.refs = Yu, this.updater = t || Qu;
}
it.prototype.isReactComponent = {};
it.prototype.setState = function(e, n) {
  if (typeof e != "object" && typeof e != "function" && e != null)
    throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
  this.updater.enqueueSetState(this, e, n, "setState");
};
it.prototype.forceUpdate = function(e) {
  this.updater.enqueueForceUpdate(this, e, "forceUpdate");
};
function Xu() {
}
Xu.prototype = it.prototype;
function Ui(e, n, t) {
  this.props = e, this.context = n, this.refs = Yu, this.updater = t || Qu;
}
var $i = Ui.prototype = new Xu();
$i.constructor = Ui;
Ku($i, it.prototype);
$i.isPureReactComponent = !0;
var Do = Array.isArray, Gu = Object.prototype.hasOwnProperty, Ai = { current: null }, Zu = { key: !0, ref: !0, __self: !0, __source: !0 };
function Ju(e, n, t) {
  var r, l = {}, i = null, o = null;
  if (n != null)
    for (r in n.ref !== void 0 && (o = n.ref), n.key !== void 0 && (i = "" + n.key), n)
      Gu.call(n, r) && !Zu.hasOwnProperty(r) && (l[r] = n[r]);
  var u = arguments.length - 2;
  if (u === 1)
    l.children = t;
  else if (1 < u) {
    for (var s = Array(u), c = 0; c < u; c++)
      s[c] = arguments[c + 2];
    l.children = s;
  }
  if (e && e.defaultProps)
    for (r in u = e.defaultProps, u)
      l[r] === void 0 && (l[r] = u[r]);
  return { $$typeof: Xt, type: e, key: i, ref: o, props: l, _owner: Ai.current };
}
function mc(e, n) {
  return { $$typeof: Xt, type: e.type, key: n, ref: e.ref, props: e.props, _owner: e._owner };
}
function Vi(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Xt;
}
function hc(e) {
  var n = { "=": "=0", ":": "=2" };
  return "$" + e.replace(/[=:]/g, function(t) {
    return n[t];
  });
}
var Io = /\/+/g;
function wl(e, n) {
  return typeof e == "object" && e !== null && e.key != null ? hc("" + e.key) : n.toString(36);
}
function gr(e, n, t, r, l) {
  var i = typeof e;
  (i === "undefined" || i === "boolean") && (e = null);
  var o = !1;
  if (e === null)
    o = !0;
  else
    switch (i) {
      case "string":
      case "number":
        o = !0;
        break;
      case "object":
        switch (e.$$typeof) {
          case Xt:
          case rc:
            o = !0;
        }
    }
  if (o)
    return o = e, l = l(o), e = r === "" ? "." + wl(o, 0) : r, Do(l) ? (t = "", e != null && (t = e.replace(Io, "$&/") + "/"), gr(l, n, t, "", function(c) {
      return c;
    })) : l != null && (Vi(l) && (l = mc(l, t + (!l.key || o && o.key === l.key ? "" : ("" + l.key).replace(Io, "$&/") + "/") + e)), n.push(l)), 1;
  if (o = 0, r = r === "" ? "." : r + ":", Do(e))
    for (var u = 0; u < e.length; u++) {
      i = e[u];
      var s = r + wl(i, u);
      o += gr(i, n, t, s, l);
    }
  else if (s = pc(e), typeof s == "function")
    for (e = s.call(e), u = 0; !(i = e.next()).done; )
      i = i.value, s = r + wl(i, u++), o += gr(i, n, t, s, l);
  else if (i === "object")
    throw n = String(e), Error("Objects are not valid as a React child (found: " + (n === "[object Object]" ? "object with keys {" + Object.keys(e).join(", ") + "}" : n) + "). If you meant to render a collection of children, use an array instead.");
  return o;
}
function nr(e, n, t) {
  if (e == null)
    return e;
  var r = [], l = 0;
  return gr(e, r, "", "", function(i) {
    return n.call(t, i, l++);
  }), r;
}
function vc(e) {
  if (e._status === -1) {
    var n = e._result;
    n = n(), n.then(function(t) {
      (e._status === 0 || e._status === -1) && (e._status = 1, e._result = t);
    }, function(t) {
      (e._status === 0 || e._status === -1) && (e._status = 2, e._result = t);
    }), e._status === -1 && (e._status = 0, e._result = n);
  }
  if (e._status === 1)
    return e._result.default;
  throw e._result;
}
var ue = { current: null }, wr = { transition: null }, yc = { ReactCurrentDispatcher: ue, ReactCurrentBatchConfig: wr, ReactCurrentOwner: Ai };
function qu() {
  throw Error("act(...) is not supported in production builds of React.");
}
L.Children = { map: nr, forEach: function(e, n, t) {
  nr(e, function() {
    n.apply(this, arguments);
  }, t);
}, count: function(e) {
  var n = 0;
  return nr(e, function() {
    n++;
  }), n;
}, toArray: function(e) {
  return nr(e, function(n) {
    return n;
  }) || [];
}, only: function(e) {
  if (!Vi(e))
    throw Error("React.Children.only expected to receive a single React element child.");
  return e;
} };
L.Component = it;
L.Fragment = lc;
L.Profiler = oc;
L.PureComponent = Ui;
L.StrictMode = ic;
L.Suspense = cc;
L.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = yc;
L.act = qu;
L.cloneElement = function(e, n, t) {
  if (e == null)
    throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + e + ".");
  var r = Ku({}, e.props), l = e.key, i = e.ref, o = e._owner;
  if (n != null) {
    if (n.ref !== void 0 && (i = n.ref, o = Ai.current), n.key !== void 0 && (l = "" + n.key), e.type && e.type.defaultProps)
      var u = e.type.defaultProps;
    for (s in n)
      Gu.call(n, s) && !Zu.hasOwnProperty(s) && (r[s] = n[s] === void 0 && u !== void 0 ? u[s] : n[s]);
  }
  var s = arguments.length - 2;
  if (s === 1)
    r.children = t;
  else if (1 < s) {
    u = Array(s);
    for (var c = 0; c < s; c++)
      u[c] = arguments[c + 2];
    r.children = u;
  }
  return { $$typeof: Xt, type: e.type, key: l, ref: i, props: r, _owner: o };
};
L.createContext = function(e) {
  return e = { $$typeof: sc, _currentValue: e, _currentValue2: e, _threadCount: 0, Provider: null, Consumer: null, _defaultValue: null, _globalName: null }, e.Provider = { $$typeof: uc, _context: e }, e.Consumer = e;
};
L.createElement = Ju;
L.createFactory = function(e) {
  var n = Ju.bind(null, e);
  return n.type = e, n;
};
L.createRef = function() {
  return { current: null };
};
L.forwardRef = function(e) {
  return { $$typeof: ac, render: e };
};
L.isValidElement = Vi;
L.lazy = function(e) {
  return { $$typeof: dc, _payload: { _status: -1, _result: e }, _init: vc };
};
L.memo = function(e, n) {
  return { $$typeof: fc, type: e, compare: n === void 0 ? null : n };
};
L.startTransition = function(e) {
  var n = wr.transition;
  wr.transition = {};
  try {
    e();
  } finally {
    wr.transition = n;
  }
};
L.unstable_act = qu;
L.useCallback = function(e, n) {
  return ue.current.useCallback(e, n);
};
L.useContext = function(e) {
  return ue.current.useContext(e);
};
L.useDebugValue = function() {
};
L.useDeferredValue = function(e) {
  return ue.current.useDeferredValue(e);
};
L.useEffect = function(e, n) {
  return ue.current.useEffect(e, n);
};
L.useId = function() {
  return ue.current.useId();
};
L.useImperativeHandle = function(e, n, t) {
  return ue.current.useImperativeHandle(e, n, t);
};
L.useInsertionEffect = function(e, n) {
  return ue.current.useInsertionEffect(e, n);
};
L.useLayoutEffect = function(e, n) {
  return ue.current.useLayoutEffect(e, n);
};
L.useMemo = function(e, n) {
  return ue.current.useMemo(e, n);
};
L.useReducer = function(e, n, t) {
  return ue.current.useReducer(e, n, t);
};
L.useRef = function(e) {
  return ue.current.useRef(e);
};
L.useState = function(e) {
  return ue.current.useState(e);
};
L.useSyncExternalStore = function(e, n, t) {
  return ue.current.useSyncExternalStore(e, n, t);
};
L.useTransition = function() {
  return ue.current.useTransition();
};
L.version = "18.3.1";
Wu.exports = L;
var en = Wu.exports;
const gc = /* @__PURE__ */ tc(en);
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var wc = en, kc = Symbol.for("react.element"), Sc = Symbol.for("react.fragment"), Ec = Object.prototype.hasOwnProperty, xc = wc.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, _c = { key: !0, ref: !0, __self: !0, __source: !0 };
function bu(e, n, t) {
  var r, l = {}, i = null, o = null;
  t !== void 0 && (i = "" + t), n.key !== void 0 && (i = "" + n.key), n.ref !== void 0 && (o = n.ref);
  for (r in n)
    Ec.call(n, r) && !_c.hasOwnProperty(r) && (l[r] = n[r]);
  if (e && e.defaultProps)
    for (r in n = e.defaultProps, n)
      l[r] === void 0 && (l[r] = n[r]);
  return { $$typeof: kc, type: e, key: i, ref: o, props: l, _owner: xc.current };
}
el.Fragment = Sc;
el.jsx = bu;
el.jsxs = bu;
Hu.exports = el;
var T = Hu.exports, Ql = {}, es = { exports: {} }, ge = {}, ns = { exports: {} }, ts = {};
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
  function n(x, P) {
    var z = x.length;
    x.push(P);
    e:
      for (; 0 < z; ) {
        var W = z - 1 >>> 1, G = x[W];
        if (0 < l(G, P))
          x[W] = P, x[z] = G, z = W;
        else
          break e;
      }
  }
  function t(x) {
    return x.length === 0 ? null : x[0];
  }
  function r(x) {
    if (x.length === 0)
      return null;
    var P = x[0], z = x.pop();
    if (z !== P) {
      x[0] = z;
      e:
        for (var W = 0, G = x.length, bt = G >>> 1; W < bt; ) {
          var yn = 2 * (W + 1) - 1, gl = x[yn], gn = yn + 1, er = x[gn];
          if (0 > l(gl, z))
            gn < G && 0 > l(er, gl) ? (x[W] = er, x[gn] = z, W = gn) : (x[W] = gl, x[yn] = z, W = yn);
          else if (gn < G && 0 > l(er, z))
            x[W] = er, x[gn] = z, W = gn;
          else
            break e;
        }
    }
    return P;
  }
  function l(x, P) {
    var z = x.sortIndex - P.sortIndex;
    return z !== 0 ? z : x.id - P.id;
  }
  if (typeof performance == "object" && typeof performance.now == "function") {
    var i = performance;
    e.unstable_now = function() {
      return i.now();
    };
  } else {
    var o = Date, u = o.now();
    e.unstable_now = function() {
      return o.now() - u;
    };
  }
  var s = [], c = [], m = 1, h = null, p = 3, g = !1, w = !1, k = !1, F = typeof setTimeout == "function" ? setTimeout : null, f = typeof clearTimeout == "function" ? clearTimeout : null, a = typeof setImmediate < "u" ? setImmediate : null;
  typeof navigator < "u" && navigator.scheduling !== void 0 && navigator.scheduling.isInputPending !== void 0 && navigator.scheduling.isInputPending.bind(navigator.scheduling);
  function d(x) {
    for (var P = t(c); P !== null; ) {
      if (P.callback === null)
        r(c);
      else if (P.startTime <= x)
        r(c), P.sortIndex = P.expirationTime, n(s, P);
      else
        break;
      P = t(c);
    }
  }
  function v(x) {
    if (k = !1, d(x), !w)
      if (t(s) !== null)
        w = !0, vl(E);
      else {
        var P = t(c);
        P !== null && yl(v, P.startTime - x);
      }
  }
  function E(x, P) {
    w = !1, k && (k = !1, f(N), N = -1), g = !0;
    var z = p;
    try {
      for (d(P), h = t(s); h !== null && (!(h.expirationTime > P) || x && !Ne()); ) {
        var W = h.callback;
        if (typeof W == "function") {
          h.callback = null, p = h.priorityLevel;
          var G = W(h.expirationTime <= P);
          P = e.unstable_now(), typeof G == "function" ? h.callback = G : h === t(s) && r(s), d(P);
        } else
          r(s);
        h = t(s);
      }
      if (h !== null)
        var bt = !0;
      else {
        var yn = t(c);
        yn !== null && yl(v, yn.startTime - P), bt = !1;
      }
      return bt;
    } finally {
      h = null, p = z, g = !1;
    }
  }
  var _ = !1, C = null, N = -1, H = 5, R = -1;
  function Ne() {
    return !(e.unstable_now() - R < H);
  }
  function st() {
    if (C !== null) {
      var x = e.unstable_now();
      R = x;
      var P = !0;
      try {
        P = C(!0, x);
      } finally {
        P ? at() : (_ = !1, C = null);
      }
    } else
      _ = !1;
  }
  var at;
  if (typeof a == "function")
    at = function() {
      a(st);
    };
  else if (typeof MessageChannel < "u") {
    var Mo = new MessageChannel(), nc = Mo.port2;
    Mo.port1.onmessage = st, at = function() {
      nc.postMessage(null);
    };
  } else
    at = function() {
      F(st, 0);
    };
  function vl(x) {
    C = x, _ || (_ = !0, at());
  }
  function yl(x, P) {
    N = F(function() {
      x(e.unstable_now());
    }, P);
  }
  e.unstable_IdlePriority = 5, e.unstable_ImmediatePriority = 1, e.unstable_LowPriority = 4, e.unstable_NormalPriority = 3, e.unstable_Profiling = null, e.unstable_UserBlockingPriority = 2, e.unstable_cancelCallback = function(x) {
    x.callback = null;
  }, e.unstable_continueExecution = function() {
    w || g || (w = !0, vl(E));
  }, e.unstable_forceFrameRate = function(x) {
    0 > x || 125 < x ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : H = 0 < x ? Math.floor(1e3 / x) : 5;
  }, e.unstable_getCurrentPriorityLevel = function() {
    return p;
  }, e.unstable_getFirstCallbackNode = function() {
    return t(s);
  }, e.unstable_next = function(x) {
    switch (p) {
      case 1:
      case 2:
      case 3:
        var P = 3;
        break;
      default:
        P = p;
    }
    var z = p;
    p = P;
    try {
      return x();
    } finally {
      p = z;
    }
  }, e.unstable_pauseExecution = function() {
  }, e.unstable_requestPaint = function() {
  }, e.unstable_runWithPriority = function(x, P) {
    switch (x) {
      case 1:
      case 2:
      case 3:
      case 4:
      case 5:
        break;
      default:
        x = 3;
    }
    var z = p;
    p = x;
    try {
      return P();
    } finally {
      p = z;
    }
  }, e.unstable_scheduleCallback = function(x, P, z) {
    var W = e.unstable_now();
    switch (typeof z == "object" && z !== null ? (z = z.delay, z = typeof z == "number" && 0 < z ? W + z : W) : z = W, x) {
      case 1:
        var G = -1;
        break;
      case 2:
        G = 250;
        break;
      case 5:
        G = 1073741823;
        break;
      case 4:
        G = 1e4;
        break;
      default:
        G = 5e3;
    }
    return G = z + G, x = { id: m++, callback: P, priorityLevel: x, startTime: z, expirationTime: G, sortIndex: -1 }, z > W ? (x.sortIndex = z, n(c, x), t(s) === null && x === t(c) && (k ? (f(N), N = -1) : k = !0, yl(v, z - W))) : (x.sortIndex = G, n(s, x), w || g || (w = !0, vl(E))), x;
  }, e.unstable_shouldYield = Ne, e.unstable_wrapCallback = function(x) {
    var P = p;
    return function() {
      var z = p;
      p = P;
      try {
        return x.apply(this, arguments);
      } finally {
        p = z;
      }
    };
  };
})(ts);
ns.exports = ts;
var Cc = ns.exports;
/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Nc = en, ye = Cc;
function y(e) {
  for (var n = "https://reactjs.org/docs/error-decoder.html?invariant=" + e, t = 1; t < arguments.length; t++)
    n += "&args[]=" + encodeURIComponent(arguments[t]);
  return "Minified React error #" + e + "; visit " + n + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
}
var rs = /* @__PURE__ */ new Set(), Rt = {};
function Rn(e, n) {
  qn(e, n), qn(e + "Capture", n);
}
function qn(e, n) {
  for (Rt[e] = n, e = 0; e < n.length; e++)
    rs.add(n[e]);
}
var We = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), Kl = Object.prototype.hasOwnProperty, Pc = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, Fo = {}, Uo = {};
function zc(e) {
  return Kl.call(Uo, e) ? !0 : Kl.call(Fo, e) ? !1 : Pc.test(e) ? Uo[e] = !0 : (Fo[e] = !0, !1);
}
function Tc(e, n, t, r) {
  if (t !== null && t.type === 0)
    return !1;
  switch (typeof n) {
    case "function":
    case "symbol":
      return !0;
    case "boolean":
      return r ? !1 : t !== null ? !t.acceptsBooleans : (e = e.toLowerCase().slice(0, 5), e !== "data-" && e !== "aria-");
    default:
      return !1;
  }
}
function Lc(e, n, t, r) {
  if (n === null || typeof n > "u" || Tc(e, n, t, r))
    return !0;
  if (r)
    return !1;
  if (t !== null)
    switch (t.type) {
      case 3:
        return !n;
      case 4:
        return n === !1;
      case 5:
        return isNaN(n);
      case 6:
        return isNaN(n) || 1 > n;
    }
  return !1;
}
function se(e, n, t, r, l, i, o) {
  this.acceptsBooleans = n === 2 || n === 3 || n === 4, this.attributeName = r, this.attributeNamespace = l, this.mustUseProperty = t, this.propertyName = e, this.type = n, this.sanitizeURL = i, this.removeEmptyString = o;
}
var ee = {};
"children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(e) {
  ee[e] = new se(e, 0, !1, e, null, !1, !1);
});
[["acceptCharset", "accept-charset"], ["className", "class"], ["htmlFor", "for"], ["httpEquiv", "http-equiv"]].forEach(function(e) {
  var n = e[0];
  ee[n] = new se(n, 1, !1, e[1], null, !1, !1);
});
["contentEditable", "draggable", "spellCheck", "value"].forEach(function(e) {
  ee[e] = new se(e, 2, !1, e.toLowerCase(), null, !1, !1);
});
["autoReverse", "externalResourcesRequired", "focusable", "preserveAlpha"].forEach(function(e) {
  ee[e] = new se(e, 2, !1, e, null, !1, !1);
});
"allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(e) {
  ee[e] = new se(e, 3, !1, e.toLowerCase(), null, !1, !1);
});
["checked", "multiple", "muted", "selected"].forEach(function(e) {
  ee[e] = new se(e, 3, !0, e, null, !1, !1);
});
["capture", "download"].forEach(function(e) {
  ee[e] = new se(e, 4, !1, e, null, !1, !1);
});
["cols", "rows", "size", "span"].forEach(function(e) {
  ee[e] = new se(e, 6, !1, e, null, !1, !1);
});
["rowSpan", "start"].forEach(function(e) {
  ee[e] = new se(e, 5, !1, e.toLowerCase(), null, !1, !1);
});
var Bi = /[\-:]([a-z])/g;
function Hi(e) {
  return e[1].toUpperCase();
}
"accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(e) {
  var n = e.replace(
    Bi,
    Hi
  );
  ee[n] = new se(n, 1, !1, e, null, !1, !1);
});
"xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(e) {
  var n = e.replace(Bi, Hi);
  ee[n] = new se(n, 1, !1, e, "http://www.w3.org/1999/xlink", !1, !1);
});
["xml:base", "xml:lang", "xml:space"].forEach(function(e) {
  var n = e.replace(Bi, Hi);
  ee[n] = new se(n, 1, !1, e, "http://www.w3.org/XML/1998/namespace", !1, !1);
});
["tabIndex", "crossOrigin"].forEach(function(e) {
  ee[e] = new se(e, 1, !1, e.toLowerCase(), null, !1, !1);
});
ee.xlinkHref = new se("xlinkHref", 1, !1, "xlink:href", "http://www.w3.org/1999/xlink", !0, !1);
["src", "href", "action", "formAction"].forEach(function(e) {
  ee[e] = new se(e, 1, !1, e.toLowerCase(), null, !0, !0);
});
function Wi(e, n, t, r) {
  var l = ee.hasOwnProperty(n) ? ee[n] : null;
  (l !== null ? l.type !== 0 : r || !(2 < n.length) || n[0] !== "o" && n[0] !== "O" || n[1] !== "n" && n[1] !== "N") && (Lc(n, t, l, r) && (t = null), r || l === null ? zc(n) && (t === null ? e.removeAttribute(n) : e.setAttribute(n, "" + t)) : l.mustUseProperty ? e[l.propertyName] = t === null ? l.type === 3 ? !1 : "" : t : (n = l.attributeName, r = l.attributeNamespace, t === null ? e.removeAttribute(n) : (l = l.type, t = l === 3 || l === 4 && t === !0 ? "" : "" + t, r ? e.setAttributeNS(r, n, t) : e.setAttribute(n, t))));
}
var Xe = Nc.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, tr = Symbol.for("react.element"), On = Symbol.for("react.portal"), Dn = Symbol.for("react.fragment"), Qi = Symbol.for("react.strict_mode"), Yl = Symbol.for("react.profiler"), ls = Symbol.for("react.provider"), is = Symbol.for("react.context"), Ki = Symbol.for("react.forward_ref"), Xl = Symbol.for("react.suspense"), Gl = Symbol.for("react.suspense_list"), Yi = Symbol.for("react.memo"), Ze = Symbol.for("react.lazy"), os = Symbol.for("react.offscreen"), $o = Symbol.iterator;
function ct(e) {
  return e === null || typeof e != "object" ? null : (e = $o && e[$o] || e["@@iterator"], typeof e == "function" ? e : null);
}
var V = Object.assign, kl;
function gt(e) {
  if (kl === void 0)
    try {
      throw Error();
    } catch (t) {
      var n = t.stack.trim().match(/\n( *(at )?)/);
      kl = n && n[1] || "";
    }
  return `
` + kl + e;
}
var Sl = !1;
function El(e, n) {
  if (!e || Sl)
    return "";
  Sl = !0;
  var t = Error.prepareStackTrace;
  Error.prepareStackTrace = void 0;
  try {
    if (n)
      if (n = function() {
        throw Error();
      }, Object.defineProperty(n.prototype, "props", { set: function() {
        throw Error();
      } }), typeof Reflect == "object" && Reflect.construct) {
        try {
          Reflect.construct(n, []);
        } catch (c) {
          var r = c;
        }
        Reflect.construct(e, [], n);
      } else {
        try {
          n.call();
        } catch (c) {
          r = c;
        }
        e.call(n.prototype);
      }
    else {
      try {
        throw Error();
      } catch (c) {
        r = c;
      }
      e();
    }
  } catch (c) {
    if (c && r && typeof c.stack == "string") {
      for (var l = c.stack.split(`
`), i = r.stack.split(`
`), o = l.length - 1, u = i.length - 1; 1 <= o && 0 <= u && l[o] !== i[u]; )
        u--;
      for (; 1 <= o && 0 <= u; o--, u--)
        if (l[o] !== i[u]) {
          if (o !== 1 || u !== 1)
            do
              if (o--, u--, 0 > u || l[o] !== i[u]) {
                var s = `
` + l[o].replace(" at new ", " at ");
                return e.displayName && s.includes("<anonymous>") && (s = s.replace("<anonymous>", e.displayName)), s;
              }
            while (1 <= o && 0 <= u);
          break;
        }
    }
  } finally {
    Sl = !1, Error.prepareStackTrace = t;
  }
  return (e = e ? e.displayName || e.name : "") ? gt(e) : "";
}
function Rc(e) {
  switch (e.tag) {
    case 5:
      return gt(e.type);
    case 16:
      return gt("Lazy");
    case 13:
      return gt("Suspense");
    case 19:
      return gt("SuspenseList");
    case 0:
    case 2:
    case 15:
      return e = El(e.type, !1), e;
    case 11:
      return e = El(e.type.render, !1), e;
    case 1:
      return e = El(e.type, !0), e;
    default:
      return "";
  }
}
function Zl(e) {
  if (e == null)
    return null;
  if (typeof e == "function")
    return e.displayName || e.name || null;
  if (typeof e == "string")
    return e;
  switch (e) {
    case Dn:
      return "Fragment";
    case On:
      return "Portal";
    case Yl:
      return "Profiler";
    case Qi:
      return "StrictMode";
    case Xl:
      return "Suspense";
    case Gl:
      return "SuspenseList";
  }
  if (typeof e == "object")
    switch (e.$$typeof) {
      case is:
        return (e.displayName || "Context") + ".Consumer";
      case ls:
        return (e._context.displayName || "Context") + ".Provider";
      case Ki:
        var n = e.render;
        return e = e.displayName, e || (e = n.displayName || n.name || "", e = e !== "" ? "ForwardRef(" + e + ")" : "ForwardRef"), e;
      case Yi:
        return n = e.displayName || null, n !== null ? n : Zl(e.type) || "Memo";
      case Ze:
        n = e._payload, e = e._init;
        try {
          return Zl(e(n));
        } catch {
        }
    }
  return null;
}
function jc(e) {
  var n = e.type;
  switch (e.tag) {
    case 24:
      return "Cache";
    case 9:
      return (n.displayName || "Context") + ".Consumer";
    case 10:
      return (n._context.displayName || "Context") + ".Provider";
    case 18:
      return "DehydratedFragment";
    case 11:
      return e = n.render, e = e.displayName || e.name || "", n.displayName || (e !== "" ? "ForwardRef(" + e + ")" : "ForwardRef");
    case 7:
      return "Fragment";
    case 5:
      return n;
    case 4:
      return "Portal";
    case 3:
      return "Root";
    case 6:
      return "Text";
    case 16:
      return Zl(n);
    case 8:
      return n === Qi ? "StrictMode" : "Mode";
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
      if (typeof n == "function")
        return n.displayName || n.name || null;
      if (typeof n == "string")
        return n;
  }
  return null;
}
function dn(e) {
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
function us(e) {
  var n = e.type;
  return (e = e.nodeName) && e.toLowerCase() === "input" && (n === "checkbox" || n === "radio");
}
function Mc(e) {
  var n = us(e) ? "checked" : "value", t = Object.getOwnPropertyDescriptor(e.constructor.prototype, n), r = "" + e[n];
  if (!e.hasOwnProperty(n) && typeof t < "u" && typeof t.get == "function" && typeof t.set == "function") {
    var l = t.get, i = t.set;
    return Object.defineProperty(e, n, { configurable: !0, get: function() {
      return l.call(this);
    }, set: function(o) {
      r = "" + o, i.call(this, o);
    } }), Object.defineProperty(e, n, { enumerable: t.enumerable }), { getValue: function() {
      return r;
    }, setValue: function(o) {
      r = "" + o;
    }, stopTracking: function() {
      e._valueTracker = null, delete e[n];
    } };
  }
}
function rr(e) {
  e._valueTracker || (e._valueTracker = Mc(e));
}
function ss(e) {
  if (!e)
    return !1;
  var n = e._valueTracker;
  if (!n)
    return !0;
  var t = n.getValue(), r = "";
  return e && (r = us(e) ? e.checked ? "true" : "false" : e.value), e = r, e !== t ? (n.setValue(e), !0) : !1;
}
function Lr(e) {
  if (e = e || (typeof document < "u" ? document : void 0), typeof e > "u")
    return null;
  try {
    return e.activeElement || e.body;
  } catch {
    return e.body;
  }
}
function Jl(e, n) {
  var t = n.checked;
  return V({}, n, { defaultChecked: void 0, defaultValue: void 0, value: void 0, checked: t ?? e._wrapperState.initialChecked });
}
function Ao(e, n) {
  var t = n.defaultValue == null ? "" : n.defaultValue, r = n.checked != null ? n.checked : n.defaultChecked;
  t = dn(n.value != null ? n.value : t), e._wrapperState = { initialChecked: r, initialValue: t, controlled: n.type === "checkbox" || n.type === "radio" ? n.checked != null : n.value != null };
}
function as(e, n) {
  n = n.checked, n != null && Wi(e, "checked", n, !1);
}
function ql(e, n) {
  as(e, n);
  var t = dn(n.value), r = n.type;
  if (t != null)
    r === "number" ? (t === 0 && e.value === "" || e.value != t) && (e.value = "" + t) : e.value !== "" + t && (e.value = "" + t);
  else if (r === "submit" || r === "reset") {
    e.removeAttribute("value");
    return;
  }
  n.hasOwnProperty("value") ? bl(e, n.type, t) : n.hasOwnProperty("defaultValue") && bl(e, n.type, dn(n.defaultValue)), n.checked == null && n.defaultChecked != null && (e.defaultChecked = !!n.defaultChecked);
}
function Vo(e, n, t) {
  if (n.hasOwnProperty("value") || n.hasOwnProperty("defaultValue")) {
    var r = n.type;
    if (!(r !== "submit" && r !== "reset" || n.value !== void 0 && n.value !== null))
      return;
    n = "" + e._wrapperState.initialValue, t || n === e.value || (e.value = n), e.defaultValue = n;
  }
  t = e.name, t !== "" && (e.name = ""), e.defaultChecked = !!e._wrapperState.initialChecked, t !== "" && (e.name = t);
}
function bl(e, n, t) {
  (n !== "number" || Lr(e.ownerDocument) !== e) && (t == null ? e.defaultValue = "" + e._wrapperState.initialValue : e.defaultValue !== "" + t && (e.defaultValue = "" + t));
}
var wt = Array.isArray;
function Kn(e, n, t, r) {
  if (e = e.options, n) {
    n = {};
    for (var l = 0; l < t.length; l++)
      n["$" + t[l]] = !0;
    for (t = 0; t < e.length; t++)
      l = n.hasOwnProperty("$" + e[t].value), e[t].selected !== l && (e[t].selected = l), l && r && (e[t].defaultSelected = !0);
  } else {
    for (t = "" + dn(t), n = null, l = 0; l < e.length; l++) {
      if (e[l].value === t) {
        e[l].selected = !0, r && (e[l].defaultSelected = !0);
        return;
      }
      n !== null || e[l].disabled || (n = e[l]);
    }
    n !== null && (n.selected = !0);
  }
}
function ei(e, n) {
  if (n.dangerouslySetInnerHTML != null)
    throw Error(y(91));
  return V({}, n, { value: void 0, defaultValue: void 0, children: "" + e._wrapperState.initialValue });
}
function Bo(e, n) {
  var t = n.value;
  if (t == null) {
    if (t = n.children, n = n.defaultValue, t != null) {
      if (n != null)
        throw Error(y(92));
      if (wt(t)) {
        if (1 < t.length)
          throw Error(y(93));
        t = t[0];
      }
      n = t;
    }
    n == null && (n = ""), t = n;
  }
  e._wrapperState = { initialValue: dn(t) };
}
function cs(e, n) {
  var t = dn(n.value), r = dn(n.defaultValue);
  t != null && (t = "" + t, t !== e.value && (e.value = t), n.defaultValue == null && e.defaultValue !== t && (e.defaultValue = t)), r != null && (e.defaultValue = "" + r);
}
function Ho(e) {
  var n = e.textContent;
  n === e._wrapperState.initialValue && n !== "" && n !== null && (e.value = n);
}
function fs(e) {
  switch (e) {
    case "svg":
      return "http://www.w3.org/2000/svg";
    case "math":
      return "http://www.w3.org/1998/Math/MathML";
    default:
      return "http://www.w3.org/1999/xhtml";
  }
}
function ni(e, n) {
  return e == null || e === "http://www.w3.org/1999/xhtml" ? fs(n) : e === "http://www.w3.org/2000/svg" && n === "foreignObject" ? "http://www.w3.org/1999/xhtml" : e;
}
var lr, ds = function(e) {
  return typeof MSApp < "u" && MSApp.execUnsafeLocalFunction ? function(n, t, r, l) {
    MSApp.execUnsafeLocalFunction(function() {
      return e(n, t, r, l);
    });
  } : e;
}(function(e, n) {
  if (e.namespaceURI !== "http://www.w3.org/2000/svg" || "innerHTML" in e)
    e.innerHTML = n;
  else {
    for (lr = lr || document.createElement("div"), lr.innerHTML = "<svg>" + n.valueOf().toString() + "</svg>", n = lr.firstChild; e.firstChild; )
      e.removeChild(e.firstChild);
    for (; n.firstChild; )
      e.appendChild(n.firstChild);
  }
});
function jt(e, n) {
  if (n) {
    var t = e.firstChild;
    if (t && t === e.lastChild && t.nodeType === 3) {
      t.nodeValue = n;
      return;
    }
  }
  e.textContent = n;
}
var Et = {
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
}, Oc = ["Webkit", "ms", "Moz", "O"];
Object.keys(Et).forEach(function(e) {
  Oc.forEach(function(n) {
    n = n + e.charAt(0).toUpperCase() + e.substring(1), Et[n] = Et[e];
  });
});
function ps(e, n, t) {
  return n == null || typeof n == "boolean" || n === "" ? "" : t || typeof n != "number" || n === 0 || Et.hasOwnProperty(e) && Et[e] ? ("" + n).trim() : n + "px";
}
function ms(e, n) {
  e = e.style;
  for (var t in n)
    if (n.hasOwnProperty(t)) {
      var r = t.indexOf("--") === 0, l = ps(t, n[t], r);
      t === "float" && (t = "cssFloat"), r ? e.setProperty(t, l) : e[t] = l;
    }
}
var Dc = V({ menuitem: !0 }, { area: !0, base: !0, br: !0, col: !0, embed: !0, hr: !0, img: !0, input: !0, keygen: !0, link: !0, meta: !0, param: !0, source: !0, track: !0, wbr: !0 });
function ti(e, n) {
  if (n) {
    if (Dc[e] && (n.children != null || n.dangerouslySetInnerHTML != null))
      throw Error(y(137, e));
    if (n.dangerouslySetInnerHTML != null) {
      if (n.children != null)
        throw Error(y(60));
      if (typeof n.dangerouslySetInnerHTML != "object" || !("__html" in n.dangerouslySetInnerHTML))
        throw Error(y(61));
    }
    if (n.style != null && typeof n.style != "object")
      throw Error(y(62));
  }
}
function ri(e, n) {
  if (e.indexOf("-") === -1)
    return typeof n.is == "string";
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
var li = null;
function Xi(e) {
  return e = e.target || e.srcElement || window, e.correspondingUseElement && (e = e.correspondingUseElement), e.nodeType === 3 ? e.parentNode : e;
}
var ii = null, Yn = null, Xn = null;
function Wo(e) {
  if (e = Jt(e)) {
    if (typeof ii != "function")
      throw Error(y(280));
    var n = e.stateNode;
    n && (n = il(n), ii(e.stateNode, e.type, n));
  }
}
function hs(e) {
  Yn ? Xn ? Xn.push(e) : Xn = [e] : Yn = e;
}
function vs() {
  if (Yn) {
    var e = Yn, n = Xn;
    if (Xn = Yn = null, Wo(e), n)
      for (e = 0; e < n.length; e++)
        Wo(n[e]);
  }
}
function ys(e, n) {
  return e(n);
}
function gs() {
}
var xl = !1;
function ws(e, n, t) {
  if (xl)
    return e(n, t);
  xl = !0;
  try {
    return ys(e, n, t);
  } finally {
    xl = !1, (Yn !== null || Xn !== null) && (gs(), vs());
  }
}
function Mt(e, n) {
  var t = e.stateNode;
  if (t === null)
    return null;
  var r = il(t);
  if (r === null)
    return null;
  t = r[n];
  e:
    switch (n) {
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
  if (t && typeof t != "function")
    throw Error(y(231, n, typeof t));
  return t;
}
var oi = !1;
if (We)
  try {
    var ft = {};
    Object.defineProperty(ft, "passive", { get: function() {
      oi = !0;
    } }), window.addEventListener("test", ft, ft), window.removeEventListener("test", ft, ft);
  } catch {
    oi = !1;
  }
function Ic(e, n, t, r, l, i, o, u, s) {
  var c = Array.prototype.slice.call(arguments, 3);
  try {
    n.apply(t, c);
  } catch (m) {
    this.onError(m);
  }
}
var xt = !1, Rr = null, jr = !1, ui = null, Fc = { onError: function(e) {
  xt = !0, Rr = e;
} };
function Uc(e, n, t, r, l, i, o, u, s) {
  xt = !1, Rr = null, Ic.apply(Fc, arguments);
}
function $c(e, n, t, r, l, i, o, u, s) {
  if (Uc.apply(this, arguments), xt) {
    if (xt) {
      var c = Rr;
      xt = !1, Rr = null;
    } else
      throw Error(y(198));
    jr || (jr = !0, ui = c);
  }
}
function jn(e) {
  var n = e, t = e;
  if (e.alternate)
    for (; n.return; )
      n = n.return;
  else {
    e = n;
    do
      n = e, n.flags & 4098 && (t = n.return), e = n.return;
    while (e);
  }
  return n.tag === 3 ? t : null;
}
function ks(e) {
  if (e.tag === 13) {
    var n = e.memoizedState;
    if (n === null && (e = e.alternate, e !== null && (n = e.memoizedState)), n !== null)
      return n.dehydrated;
  }
  return null;
}
function Qo(e) {
  if (jn(e) !== e)
    throw Error(y(188));
}
function Ac(e) {
  var n = e.alternate;
  if (!n) {
    if (n = jn(e), n === null)
      throw Error(y(188));
    return n !== e ? null : e;
  }
  for (var t = e, r = n; ; ) {
    var l = t.return;
    if (l === null)
      break;
    var i = l.alternate;
    if (i === null) {
      if (r = l.return, r !== null) {
        t = r;
        continue;
      }
      break;
    }
    if (l.child === i.child) {
      for (i = l.child; i; ) {
        if (i === t)
          return Qo(l), e;
        if (i === r)
          return Qo(l), n;
        i = i.sibling;
      }
      throw Error(y(188));
    }
    if (t.return !== r.return)
      t = l, r = i;
    else {
      for (var o = !1, u = l.child; u; ) {
        if (u === t) {
          o = !0, t = l, r = i;
          break;
        }
        if (u === r) {
          o = !0, r = l, t = i;
          break;
        }
        u = u.sibling;
      }
      if (!o) {
        for (u = i.child; u; ) {
          if (u === t) {
            o = !0, t = i, r = l;
            break;
          }
          if (u === r) {
            o = !0, r = i, t = l;
            break;
          }
          u = u.sibling;
        }
        if (!o)
          throw Error(y(189));
      }
    }
    if (t.alternate !== r)
      throw Error(y(190));
  }
  if (t.tag !== 3)
    throw Error(y(188));
  return t.stateNode.current === t ? e : n;
}
function Ss(e) {
  return e = Ac(e), e !== null ? Es(e) : null;
}
function Es(e) {
  if (e.tag === 5 || e.tag === 6)
    return e;
  for (e = e.child; e !== null; ) {
    var n = Es(e);
    if (n !== null)
      return n;
    e = e.sibling;
  }
  return null;
}
var xs = ye.unstable_scheduleCallback, Ko = ye.unstable_cancelCallback, Vc = ye.unstable_shouldYield, Bc = ye.unstable_requestPaint, Q = ye.unstable_now, Hc = ye.unstable_getCurrentPriorityLevel, Gi = ye.unstable_ImmediatePriority, _s = ye.unstable_UserBlockingPriority, Mr = ye.unstable_NormalPriority, Wc = ye.unstable_LowPriority, Cs = ye.unstable_IdlePriority, nl = null, Fe = null;
function Qc(e) {
  if (Fe && typeof Fe.onCommitFiberRoot == "function")
    try {
      Fe.onCommitFiberRoot(nl, e, void 0, (e.current.flags & 128) === 128);
    } catch {
    }
}
var Re = Math.clz32 ? Math.clz32 : Xc, Kc = Math.log, Yc = Math.LN2;
function Xc(e) {
  return e >>>= 0, e === 0 ? 32 : 31 - (Kc(e) / Yc | 0) | 0;
}
var ir = 64, or = 4194304;
function kt(e) {
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
function Or(e, n) {
  var t = e.pendingLanes;
  if (t === 0)
    return 0;
  var r = 0, l = e.suspendedLanes, i = e.pingedLanes, o = t & 268435455;
  if (o !== 0) {
    var u = o & ~l;
    u !== 0 ? r = kt(u) : (i &= o, i !== 0 && (r = kt(i)));
  } else
    o = t & ~l, o !== 0 ? r = kt(o) : i !== 0 && (r = kt(i));
  if (r === 0)
    return 0;
  if (n !== 0 && n !== r && !(n & l) && (l = r & -r, i = n & -n, l >= i || l === 16 && (i & 4194240) !== 0))
    return n;
  if (r & 4 && (r |= t & 16), n = e.entangledLanes, n !== 0)
    for (e = e.entanglements, n &= r; 0 < n; )
      t = 31 - Re(n), l = 1 << t, r |= e[t], n &= ~l;
  return r;
}
function Gc(e, n) {
  switch (e) {
    case 1:
    case 2:
    case 4:
      return n + 250;
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
      return n + 5e3;
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
function Zc(e, n) {
  for (var t = e.suspendedLanes, r = e.pingedLanes, l = e.expirationTimes, i = e.pendingLanes; 0 < i; ) {
    var o = 31 - Re(i), u = 1 << o, s = l[o];
    s === -1 ? (!(u & t) || u & r) && (l[o] = Gc(u, n)) : s <= n && (e.expiredLanes |= u), i &= ~u;
  }
}
function si(e) {
  return e = e.pendingLanes & -1073741825, e !== 0 ? e : e & 1073741824 ? 1073741824 : 0;
}
function Ns() {
  var e = ir;
  return ir <<= 1, !(ir & 4194240) && (ir = 64), e;
}
function _l(e) {
  for (var n = [], t = 0; 31 > t; t++)
    n.push(e);
  return n;
}
function Gt(e, n, t) {
  e.pendingLanes |= n, n !== 536870912 && (e.suspendedLanes = 0, e.pingedLanes = 0), e = e.eventTimes, n = 31 - Re(n), e[n] = t;
}
function Jc(e, n) {
  var t = e.pendingLanes & ~n;
  e.pendingLanes = n, e.suspendedLanes = 0, e.pingedLanes = 0, e.expiredLanes &= n, e.mutableReadLanes &= n, e.entangledLanes &= n, n = e.entanglements;
  var r = e.eventTimes;
  for (e = e.expirationTimes; 0 < t; ) {
    var l = 31 - Re(t), i = 1 << l;
    n[l] = 0, r[l] = -1, e[l] = -1, t &= ~i;
  }
}
function Zi(e, n) {
  var t = e.entangledLanes |= n;
  for (e = e.entanglements; t; ) {
    var r = 31 - Re(t), l = 1 << r;
    l & n | e[r] & n && (e[r] |= n), t &= ~l;
  }
}
var M = 0;
function Ps(e) {
  return e &= -e, 1 < e ? 4 < e ? e & 268435455 ? 16 : 536870912 : 4 : 1;
}
var zs, Ji, Ts, Ls, Rs, ai = !1, ur = [], rn = null, ln = null, on = null, Ot = /* @__PURE__ */ new Map(), Dt = /* @__PURE__ */ new Map(), qe = [], qc = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
function Yo(e, n) {
  switch (e) {
    case "focusin":
    case "focusout":
      rn = null;
      break;
    case "dragenter":
    case "dragleave":
      ln = null;
      break;
    case "mouseover":
    case "mouseout":
      on = null;
      break;
    case "pointerover":
    case "pointerout":
      Ot.delete(n.pointerId);
      break;
    case "gotpointercapture":
    case "lostpointercapture":
      Dt.delete(n.pointerId);
  }
}
function dt(e, n, t, r, l, i) {
  return e === null || e.nativeEvent !== i ? (e = { blockedOn: n, domEventName: t, eventSystemFlags: r, nativeEvent: i, targetContainers: [l] }, n !== null && (n = Jt(n), n !== null && Ji(n)), e) : (e.eventSystemFlags |= r, n = e.targetContainers, l !== null && n.indexOf(l) === -1 && n.push(l), e);
}
function bc(e, n, t, r, l) {
  switch (n) {
    case "focusin":
      return rn = dt(rn, e, n, t, r, l), !0;
    case "dragenter":
      return ln = dt(ln, e, n, t, r, l), !0;
    case "mouseover":
      return on = dt(on, e, n, t, r, l), !0;
    case "pointerover":
      var i = l.pointerId;
      return Ot.set(i, dt(Ot.get(i) || null, e, n, t, r, l)), !0;
    case "gotpointercapture":
      return i = l.pointerId, Dt.set(i, dt(Dt.get(i) || null, e, n, t, r, l)), !0;
  }
  return !1;
}
function js(e) {
  var n = Sn(e.target);
  if (n !== null) {
    var t = jn(n);
    if (t !== null) {
      if (n = t.tag, n === 13) {
        if (n = ks(t), n !== null) {
          e.blockedOn = n, Rs(e.priority, function() {
            Ts(t);
          });
          return;
        }
      } else if (n === 3 && t.stateNode.current.memoizedState.isDehydrated) {
        e.blockedOn = t.tag === 3 ? t.stateNode.containerInfo : null;
        return;
      }
    }
  }
  e.blockedOn = null;
}
function kr(e) {
  if (e.blockedOn !== null)
    return !1;
  for (var n = e.targetContainers; 0 < n.length; ) {
    var t = ci(e.domEventName, e.eventSystemFlags, n[0], e.nativeEvent);
    if (t === null) {
      t = e.nativeEvent;
      var r = new t.constructor(t.type, t);
      li = r, t.target.dispatchEvent(r), li = null;
    } else
      return n = Jt(t), n !== null && Ji(n), e.blockedOn = t, !1;
    n.shift();
  }
  return !0;
}
function Xo(e, n, t) {
  kr(e) && t.delete(n);
}
function ef() {
  ai = !1, rn !== null && kr(rn) && (rn = null), ln !== null && kr(ln) && (ln = null), on !== null && kr(on) && (on = null), Ot.forEach(Xo), Dt.forEach(Xo);
}
function pt(e, n) {
  e.blockedOn === n && (e.blockedOn = null, ai || (ai = !0, ye.unstable_scheduleCallback(ye.unstable_NormalPriority, ef)));
}
function It(e) {
  function n(l) {
    return pt(l, e);
  }
  if (0 < ur.length) {
    pt(ur[0], e);
    for (var t = 1; t < ur.length; t++) {
      var r = ur[t];
      r.blockedOn === e && (r.blockedOn = null);
    }
  }
  for (rn !== null && pt(rn, e), ln !== null && pt(ln, e), on !== null && pt(on, e), Ot.forEach(n), Dt.forEach(n), t = 0; t < qe.length; t++)
    r = qe[t], r.blockedOn === e && (r.blockedOn = null);
  for (; 0 < qe.length && (t = qe[0], t.blockedOn === null); )
    js(t), t.blockedOn === null && qe.shift();
}
var Gn = Xe.ReactCurrentBatchConfig, Dr = !0;
function nf(e, n, t, r) {
  var l = M, i = Gn.transition;
  Gn.transition = null;
  try {
    M = 1, qi(e, n, t, r);
  } finally {
    M = l, Gn.transition = i;
  }
}
function tf(e, n, t, r) {
  var l = M, i = Gn.transition;
  Gn.transition = null;
  try {
    M = 4, qi(e, n, t, r);
  } finally {
    M = l, Gn.transition = i;
  }
}
function qi(e, n, t, r) {
  if (Dr) {
    var l = ci(e, n, t, r);
    if (l === null)
      Ol(e, n, r, Ir, t), Yo(e, r);
    else if (bc(l, e, n, t, r))
      r.stopPropagation();
    else if (Yo(e, r), n & 4 && -1 < qc.indexOf(e)) {
      for (; l !== null; ) {
        var i = Jt(l);
        if (i !== null && zs(i), i = ci(e, n, t, r), i === null && Ol(e, n, r, Ir, t), i === l)
          break;
        l = i;
      }
      l !== null && r.stopPropagation();
    } else
      Ol(e, n, r, null, t);
  }
}
var Ir = null;
function ci(e, n, t, r) {
  if (Ir = null, e = Xi(r), e = Sn(e), e !== null)
    if (n = jn(e), n === null)
      e = null;
    else if (t = n.tag, t === 13) {
      if (e = ks(n), e !== null)
        return e;
      e = null;
    } else if (t === 3) {
      if (n.stateNode.current.memoizedState.isDehydrated)
        return n.tag === 3 ? n.stateNode.containerInfo : null;
      e = null;
    } else
      n !== e && (e = null);
  return Ir = e, null;
}
function Ms(e) {
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
      switch (Hc()) {
        case Gi:
          return 1;
        case _s:
          return 4;
        case Mr:
        case Wc:
          return 16;
        case Cs:
          return 536870912;
        default:
          return 16;
      }
    default:
      return 16;
  }
}
var nn = null, bi = null, Sr = null;
function Os() {
  if (Sr)
    return Sr;
  var e, n = bi, t = n.length, r, l = "value" in nn ? nn.value : nn.textContent, i = l.length;
  for (e = 0; e < t && n[e] === l[e]; e++)
    ;
  var o = t - e;
  for (r = 1; r <= o && n[t - r] === l[i - r]; r++)
    ;
  return Sr = l.slice(e, 1 < r ? 1 - r : void 0);
}
function Er(e) {
  var n = e.keyCode;
  return "charCode" in e ? (e = e.charCode, e === 0 && n === 13 && (e = 13)) : e = n, e === 10 && (e = 13), 32 <= e || e === 13 ? e : 0;
}
function sr() {
  return !0;
}
function Go() {
  return !1;
}
function we(e) {
  function n(t, r, l, i, o) {
    this._reactName = t, this._targetInst = l, this.type = r, this.nativeEvent = i, this.target = o, this.currentTarget = null;
    for (var u in e)
      e.hasOwnProperty(u) && (t = e[u], this[u] = t ? t(i) : i[u]);
    return this.isDefaultPrevented = (i.defaultPrevented != null ? i.defaultPrevented : i.returnValue === !1) ? sr : Go, this.isPropagationStopped = Go, this;
  }
  return V(n.prototype, { preventDefault: function() {
    this.defaultPrevented = !0;
    var t = this.nativeEvent;
    t && (t.preventDefault ? t.preventDefault() : typeof t.returnValue != "unknown" && (t.returnValue = !1), this.isDefaultPrevented = sr);
  }, stopPropagation: function() {
    var t = this.nativeEvent;
    t && (t.stopPropagation ? t.stopPropagation() : typeof t.cancelBubble != "unknown" && (t.cancelBubble = !0), this.isPropagationStopped = sr);
  }, persist: function() {
  }, isPersistent: sr }), n;
}
var ot = { eventPhase: 0, bubbles: 0, cancelable: 0, timeStamp: function(e) {
  return e.timeStamp || Date.now();
}, defaultPrevented: 0, isTrusted: 0 }, eo = we(ot), Zt = V({}, ot, { view: 0, detail: 0 }), rf = we(Zt), Cl, Nl, mt, tl = V({}, Zt, { screenX: 0, screenY: 0, clientX: 0, clientY: 0, pageX: 0, pageY: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, getModifierState: no, button: 0, buttons: 0, relatedTarget: function(e) {
  return e.relatedTarget === void 0 ? e.fromElement === e.srcElement ? e.toElement : e.fromElement : e.relatedTarget;
}, movementX: function(e) {
  return "movementX" in e ? e.movementX : (e !== mt && (mt && e.type === "mousemove" ? (Cl = e.screenX - mt.screenX, Nl = e.screenY - mt.screenY) : Nl = Cl = 0, mt = e), Cl);
}, movementY: function(e) {
  return "movementY" in e ? e.movementY : Nl;
} }), Zo = we(tl), lf = V({}, tl, { dataTransfer: 0 }), of = we(lf), uf = V({}, Zt, { relatedTarget: 0 }), Pl = we(uf), sf = V({}, ot, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }), af = we(sf), cf = V({}, ot, { clipboardData: function(e) {
  return "clipboardData" in e ? e.clipboardData : window.clipboardData;
} }), ff = we(cf), df = V({}, ot, { data: 0 }), Jo = we(df), pf = {
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
}, mf = {
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
}, hf = { Alt: "altKey", Control: "ctrlKey", Meta: "metaKey", Shift: "shiftKey" };
function vf(e) {
  var n = this.nativeEvent;
  return n.getModifierState ? n.getModifierState(e) : (e = hf[e]) ? !!n[e] : !1;
}
function no() {
  return vf;
}
var yf = V({}, Zt, { key: function(e) {
  if (e.key) {
    var n = pf[e.key] || e.key;
    if (n !== "Unidentified")
      return n;
  }
  return e.type === "keypress" ? (e = Er(e), e === 13 ? "Enter" : String.fromCharCode(e)) : e.type === "keydown" || e.type === "keyup" ? mf[e.keyCode] || "Unidentified" : "";
}, code: 0, location: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, repeat: 0, locale: 0, getModifierState: no, charCode: function(e) {
  return e.type === "keypress" ? Er(e) : 0;
}, keyCode: function(e) {
  return e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
}, which: function(e) {
  return e.type === "keypress" ? Er(e) : e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
} }), gf = we(yf), wf = V({}, tl, { pointerId: 0, width: 0, height: 0, pressure: 0, tangentialPressure: 0, tiltX: 0, tiltY: 0, twist: 0, pointerType: 0, isPrimary: 0 }), qo = we(wf), kf = V({}, Zt, { touches: 0, targetTouches: 0, changedTouches: 0, altKey: 0, metaKey: 0, ctrlKey: 0, shiftKey: 0, getModifierState: no }), Sf = we(kf), Ef = V({}, ot, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }), xf = we(Ef), _f = V({}, tl, {
  deltaX: function(e) {
    return "deltaX" in e ? e.deltaX : "wheelDeltaX" in e ? -e.wheelDeltaX : 0;
  },
  deltaY: function(e) {
    return "deltaY" in e ? e.deltaY : "wheelDeltaY" in e ? -e.wheelDeltaY : "wheelDelta" in e ? -e.wheelDelta : 0;
  },
  deltaZ: 0,
  deltaMode: 0
}), Cf = we(_f), Nf = [9, 13, 27, 32], to = We && "CompositionEvent" in window, _t = null;
We && "documentMode" in document && (_t = document.documentMode);
var Pf = We && "TextEvent" in window && !_t, Ds = We && (!to || _t && 8 < _t && 11 >= _t), bo = String.fromCharCode(32), eu = !1;
function Is(e, n) {
  switch (e) {
    case "keyup":
      return Nf.indexOf(n.keyCode) !== -1;
    case "keydown":
      return n.keyCode !== 229;
    case "keypress":
    case "mousedown":
    case "focusout":
      return !0;
    default:
      return !1;
  }
}
function Fs(e) {
  return e = e.detail, typeof e == "object" && "data" in e ? e.data : null;
}
var In = !1;
function zf(e, n) {
  switch (e) {
    case "compositionend":
      return Fs(n);
    case "keypress":
      return n.which !== 32 ? null : (eu = !0, bo);
    case "textInput":
      return e = n.data, e === bo && eu ? null : e;
    default:
      return null;
  }
}
function Tf(e, n) {
  if (In)
    return e === "compositionend" || !to && Is(e, n) ? (e = Os(), Sr = bi = nn = null, In = !1, e) : null;
  switch (e) {
    case "paste":
      return null;
    case "keypress":
      if (!(n.ctrlKey || n.altKey || n.metaKey) || n.ctrlKey && n.altKey) {
        if (n.char && 1 < n.char.length)
          return n.char;
        if (n.which)
          return String.fromCharCode(n.which);
      }
      return null;
    case "compositionend":
      return Ds && n.locale !== "ko" ? null : n.data;
    default:
      return null;
  }
}
var Lf = { color: !0, date: !0, datetime: !0, "datetime-local": !0, email: !0, month: !0, number: !0, password: !0, range: !0, search: !0, tel: !0, text: !0, time: !0, url: !0, week: !0 };
function nu(e) {
  var n = e && e.nodeName && e.nodeName.toLowerCase();
  return n === "input" ? !!Lf[e.type] : n === "textarea";
}
function Us(e, n, t, r) {
  hs(r), n = Fr(n, "onChange"), 0 < n.length && (t = new eo("onChange", "change", null, t, r), e.push({ event: t, listeners: n }));
}
var Ct = null, Ft = null;
function Rf(e) {
  Gs(e, 0);
}
function rl(e) {
  var n = $n(e);
  if (ss(n))
    return e;
}
function jf(e, n) {
  if (e === "change")
    return n;
}
var $s = !1;
if (We) {
  var zl;
  if (We) {
    var Tl = "oninput" in document;
    if (!Tl) {
      var tu = document.createElement("div");
      tu.setAttribute("oninput", "return;"), Tl = typeof tu.oninput == "function";
    }
    zl = Tl;
  } else
    zl = !1;
  $s = zl && (!document.documentMode || 9 < document.documentMode);
}
function ru() {
  Ct && (Ct.detachEvent("onpropertychange", As), Ft = Ct = null);
}
function As(e) {
  if (e.propertyName === "value" && rl(Ft)) {
    var n = [];
    Us(n, Ft, e, Xi(e)), ws(Rf, n);
  }
}
function Mf(e, n, t) {
  e === "focusin" ? (ru(), Ct = n, Ft = t, Ct.attachEvent("onpropertychange", As)) : e === "focusout" && ru();
}
function Of(e) {
  if (e === "selectionchange" || e === "keyup" || e === "keydown")
    return rl(Ft);
}
function Df(e, n) {
  if (e === "click")
    return rl(n);
}
function If(e, n) {
  if (e === "input" || e === "change")
    return rl(n);
}
function Ff(e, n) {
  return e === n && (e !== 0 || 1 / e === 1 / n) || e !== e && n !== n;
}
var Me = typeof Object.is == "function" ? Object.is : Ff;
function Ut(e, n) {
  if (Me(e, n))
    return !0;
  if (typeof e != "object" || e === null || typeof n != "object" || n === null)
    return !1;
  var t = Object.keys(e), r = Object.keys(n);
  if (t.length !== r.length)
    return !1;
  for (r = 0; r < t.length; r++) {
    var l = t[r];
    if (!Kl.call(n, l) || !Me(e[l], n[l]))
      return !1;
  }
  return !0;
}
function lu(e) {
  for (; e && e.firstChild; )
    e = e.firstChild;
  return e;
}
function iu(e, n) {
  var t = lu(e);
  e = 0;
  for (var r; t; ) {
    if (t.nodeType === 3) {
      if (r = e + t.textContent.length, e <= n && r >= n)
        return { node: t, offset: n - e };
      e = r;
    }
    e: {
      for (; t; ) {
        if (t.nextSibling) {
          t = t.nextSibling;
          break e;
        }
        t = t.parentNode;
      }
      t = void 0;
    }
    t = lu(t);
  }
}
function Vs(e, n) {
  return e && n ? e === n ? !0 : e && e.nodeType === 3 ? !1 : n && n.nodeType === 3 ? Vs(e, n.parentNode) : "contains" in e ? e.contains(n) : e.compareDocumentPosition ? !!(e.compareDocumentPosition(n) & 16) : !1 : !1;
}
function Bs() {
  for (var e = window, n = Lr(); n instanceof e.HTMLIFrameElement; ) {
    try {
      var t = typeof n.contentWindow.location.href == "string";
    } catch {
      t = !1;
    }
    if (t)
      e = n.contentWindow;
    else
      break;
    n = Lr(e.document);
  }
  return n;
}
function ro(e) {
  var n = e && e.nodeName && e.nodeName.toLowerCase();
  return n && (n === "input" && (e.type === "text" || e.type === "search" || e.type === "tel" || e.type === "url" || e.type === "password") || n === "textarea" || e.contentEditable === "true");
}
function Uf(e) {
  var n = Bs(), t = e.focusedElem, r = e.selectionRange;
  if (n !== t && t && t.ownerDocument && Vs(t.ownerDocument.documentElement, t)) {
    if (r !== null && ro(t)) {
      if (n = r.start, e = r.end, e === void 0 && (e = n), "selectionStart" in t)
        t.selectionStart = n, t.selectionEnd = Math.min(e, t.value.length);
      else if (e = (n = t.ownerDocument || document) && n.defaultView || window, e.getSelection) {
        e = e.getSelection();
        var l = t.textContent.length, i = Math.min(r.start, l);
        r = r.end === void 0 ? i : Math.min(r.end, l), !e.extend && i > r && (l = r, r = i, i = l), l = iu(t, i);
        var o = iu(
          t,
          r
        );
        l && o && (e.rangeCount !== 1 || e.anchorNode !== l.node || e.anchorOffset !== l.offset || e.focusNode !== o.node || e.focusOffset !== o.offset) && (n = n.createRange(), n.setStart(l.node, l.offset), e.removeAllRanges(), i > r ? (e.addRange(n), e.extend(o.node, o.offset)) : (n.setEnd(o.node, o.offset), e.addRange(n)));
      }
    }
    for (n = [], e = t; e = e.parentNode; )
      e.nodeType === 1 && n.push({ element: e, left: e.scrollLeft, top: e.scrollTop });
    for (typeof t.focus == "function" && t.focus(), t = 0; t < n.length; t++)
      e = n[t], e.element.scrollLeft = e.left, e.element.scrollTop = e.top;
  }
}
var $f = We && "documentMode" in document && 11 >= document.documentMode, Fn = null, fi = null, Nt = null, di = !1;
function ou(e, n, t) {
  var r = t.window === t ? t.document : t.nodeType === 9 ? t : t.ownerDocument;
  di || Fn == null || Fn !== Lr(r) || (r = Fn, "selectionStart" in r && ro(r) ? r = { start: r.selectionStart, end: r.selectionEnd } : (r = (r.ownerDocument && r.ownerDocument.defaultView || window).getSelection(), r = { anchorNode: r.anchorNode, anchorOffset: r.anchorOffset, focusNode: r.focusNode, focusOffset: r.focusOffset }), Nt && Ut(Nt, r) || (Nt = r, r = Fr(fi, "onSelect"), 0 < r.length && (n = new eo("onSelect", "select", null, n, t), e.push({ event: n, listeners: r }), n.target = Fn)));
}
function ar(e, n) {
  var t = {};
  return t[e.toLowerCase()] = n.toLowerCase(), t["Webkit" + e] = "webkit" + n, t["Moz" + e] = "moz" + n, t;
}
var Un = { animationend: ar("Animation", "AnimationEnd"), animationiteration: ar("Animation", "AnimationIteration"), animationstart: ar("Animation", "AnimationStart"), transitionend: ar("Transition", "TransitionEnd") }, Ll = {}, Hs = {};
We && (Hs = document.createElement("div").style, "AnimationEvent" in window || (delete Un.animationend.animation, delete Un.animationiteration.animation, delete Un.animationstart.animation), "TransitionEvent" in window || delete Un.transitionend.transition);
function ll(e) {
  if (Ll[e])
    return Ll[e];
  if (!Un[e])
    return e;
  var n = Un[e], t;
  for (t in n)
    if (n.hasOwnProperty(t) && t in Hs)
      return Ll[e] = n[t];
  return e;
}
var Ws = ll("animationend"), Qs = ll("animationiteration"), Ks = ll("animationstart"), Ys = ll("transitionend"), Xs = /* @__PURE__ */ new Map(), uu = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
function mn(e, n) {
  Xs.set(e, n), Rn(n, [e]);
}
for (var Rl = 0; Rl < uu.length; Rl++) {
  var jl = uu[Rl], Af = jl.toLowerCase(), Vf = jl[0].toUpperCase() + jl.slice(1);
  mn(Af, "on" + Vf);
}
mn(Ws, "onAnimationEnd");
mn(Qs, "onAnimationIteration");
mn(Ks, "onAnimationStart");
mn("dblclick", "onDoubleClick");
mn("focusin", "onFocus");
mn("focusout", "onBlur");
mn(Ys, "onTransitionEnd");
qn("onMouseEnter", ["mouseout", "mouseover"]);
qn("onMouseLeave", ["mouseout", "mouseover"]);
qn("onPointerEnter", ["pointerout", "pointerover"]);
qn("onPointerLeave", ["pointerout", "pointerover"]);
Rn("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" "));
Rn("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));
Rn("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]);
Rn("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" "));
Rn("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" "));
Rn("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
var St = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), Bf = new Set("cancel close invalid load scroll toggle".split(" ").concat(St));
function su(e, n, t) {
  var r = e.type || "unknown-event";
  e.currentTarget = t, $c(r, n, void 0, e), e.currentTarget = null;
}
function Gs(e, n) {
  n = (n & 4) !== 0;
  for (var t = 0; t < e.length; t++) {
    var r = e[t], l = r.event;
    r = r.listeners;
    e: {
      var i = void 0;
      if (n)
        for (var o = r.length - 1; 0 <= o; o--) {
          var u = r[o], s = u.instance, c = u.currentTarget;
          if (u = u.listener, s !== i && l.isPropagationStopped())
            break e;
          su(l, u, c), i = s;
        }
      else
        for (o = 0; o < r.length; o++) {
          if (u = r[o], s = u.instance, c = u.currentTarget, u = u.listener, s !== i && l.isPropagationStopped())
            break e;
          su(l, u, c), i = s;
        }
    }
  }
  if (jr)
    throw e = ui, jr = !1, ui = null, e;
}
function D(e, n) {
  var t = n[yi];
  t === void 0 && (t = n[yi] = /* @__PURE__ */ new Set());
  var r = e + "__bubble";
  t.has(r) || (Zs(n, e, 2, !1), t.add(r));
}
function Ml(e, n, t) {
  var r = 0;
  n && (r |= 4), Zs(t, e, r, n);
}
var cr = "_reactListening" + Math.random().toString(36).slice(2);
function $t(e) {
  if (!e[cr]) {
    e[cr] = !0, rs.forEach(function(t) {
      t !== "selectionchange" && (Bf.has(t) || Ml(t, !1, e), Ml(t, !0, e));
    });
    var n = e.nodeType === 9 ? e : e.ownerDocument;
    n === null || n[cr] || (n[cr] = !0, Ml("selectionchange", !1, n));
  }
}
function Zs(e, n, t, r) {
  switch (Ms(n)) {
    case 1:
      var l = nf;
      break;
    case 4:
      l = tf;
      break;
    default:
      l = qi;
  }
  t = l.bind(null, n, t, e), l = void 0, !oi || n !== "touchstart" && n !== "touchmove" && n !== "wheel" || (l = !0), r ? l !== void 0 ? e.addEventListener(n, t, { capture: !0, passive: l }) : e.addEventListener(n, t, !0) : l !== void 0 ? e.addEventListener(n, t, { passive: l }) : e.addEventListener(n, t, !1);
}
function Ol(e, n, t, r, l) {
  var i = r;
  if (!(n & 1) && !(n & 2) && r !== null)
    e:
      for (; ; ) {
        if (r === null)
          return;
        var o = r.tag;
        if (o === 3 || o === 4) {
          var u = r.stateNode.containerInfo;
          if (u === l || u.nodeType === 8 && u.parentNode === l)
            break;
          if (o === 4)
            for (o = r.return; o !== null; ) {
              var s = o.tag;
              if ((s === 3 || s === 4) && (s = o.stateNode.containerInfo, s === l || s.nodeType === 8 && s.parentNode === l))
                return;
              o = o.return;
            }
          for (; u !== null; ) {
            if (o = Sn(u), o === null)
              return;
            if (s = o.tag, s === 5 || s === 6) {
              r = i = o;
              continue e;
            }
            u = u.parentNode;
          }
        }
        r = r.return;
      }
  ws(function() {
    var c = i, m = Xi(t), h = [];
    e: {
      var p = Xs.get(e);
      if (p !== void 0) {
        var g = eo, w = e;
        switch (e) {
          case "keypress":
            if (Er(t) === 0)
              break e;
          case "keydown":
          case "keyup":
            g = gf;
            break;
          case "focusin":
            w = "focus", g = Pl;
            break;
          case "focusout":
            w = "blur", g = Pl;
            break;
          case "beforeblur":
          case "afterblur":
            g = Pl;
            break;
          case "click":
            if (t.button === 2)
              break e;
          case "auxclick":
          case "dblclick":
          case "mousedown":
          case "mousemove":
          case "mouseup":
          case "mouseout":
          case "mouseover":
          case "contextmenu":
            g = Zo;
            break;
          case "drag":
          case "dragend":
          case "dragenter":
          case "dragexit":
          case "dragleave":
          case "dragover":
          case "dragstart":
          case "drop":
            g = of;
            break;
          case "touchcancel":
          case "touchend":
          case "touchmove":
          case "touchstart":
            g = Sf;
            break;
          case Ws:
          case Qs:
          case Ks:
            g = af;
            break;
          case Ys:
            g = xf;
            break;
          case "scroll":
            g = rf;
            break;
          case "wheel":
            g = Cf;
            break;
          case "copy":
          case "cut":
          case "paste":
            g = ff;
            break;
          case "gotpointercapture":
          case "lostpointercapture":
          case "pointercancel":
          case "pointerdown":
          case "pointermove":
          case "pointerout":
          case "pointerover":
          case "pointerup":
            g = qo;
        }
        var k = (n & 4) !== 0, F = !k && e === "scroll", f = k ? p !== null ? p + "Capture" : null : p;
        k = [];
        for (var a = c, d; a !== null; ) {
          d = a;
          var v = d.stateNode;
          if (d.tag === 5 && v !== null && (d = v, f !== null && (v = Mt(a, f), v != null && k.push(At(a, v, d)))), F)
            break;
          a = a.return;
        }
        0 < k.length && (p = new g(p, w, null, t, m), h.push({ event: p, listeners: k }));
      }
    }
    if (!(n & 7)) {
      e: {
        if (p = e === "mouseover" || e === "pointerover", g = e === "mouseout" || e === "pointerout", p && t !== li && (w = t.relatedTarget || t.fromElement) && (Sn(w) || w[Qe]))
          break e;
        if ((g || p) && (p = m.window === m ? m : (p = m.ownerDocument) ? p.defaultView || p.parentWindow : window, g ? (w = t.relatedTarget || t.toElement, g = c, w = w ? Sn(w) : null, w !== null && (F = jn(w), w !== F || w.tag !== 5 && w.tag !== 6) && (w = null)) : (g = null, w = c), g !== w)) {
          if (k = Zo, v = "onMouseLeave", f = "onMouseEnter", a = "mouse", (e === "pointerout" || e === "pointerover") && (k = qo, v = "onPointerLeave", f = "onPointerEnter", a = "pointer"), F = g == null ? p : $n(g), d = w == null ? p : $n(w), p = new k(v, a + "leave", g, t, m), p.target = F, p.relatedTarget = d, v = null, Sn(m) === c && (k = new k(f, a + "enter", w, t, m), k.target = d, k.relatedTarget = F, v = k), F = v, g && w)
            n: {
              for (k = g, f = w, a = 0, d = k; d; d = Mn(d))
                a++;
              for (d = 0, v = f; v; v = Mn(v))
                d++;
              for (; 0 < a - d; )
                k = Mn(k), a--;
              for (; 0 < d - a; )
                f = Mn(f), d--;
              for (; a--; ) {
                if (k === f || f !== null && k === f.alternate)
                  break n;
                k = Mn(k), f = Mn(f);
              }
              k = null;
            }
          else
            k = null;
          g !== null && au(h, p, g, k, !1), w !== null && F !== null && au(h, F, w, k, !0);
        }
      }
      e: {
        if (p = c ? $n(c) : window, g = p.nodeName && p.nodeName.toLowerCase(), g === "select" || g === "input" && p.type === "file")
          var E = jf;
        else if (nu(p))
          if ($s)
            E = If;
          else {
            E = Of;
            var _ = Mf;
          }
        else
          (g = p.nodeName) && g.toLowerCase() === "input" && (p.type === "checkbox" || p.type === "radio") && (E = Df);
        if (E && (E = E(e, c))) {
          Us(h, E, t, m);
          break e;
        }
        _ && _(e, p, c), e === "focusout" && (_ = p._wrapperState) && _.controlled && p.type === "number" && bl(p, "number", p.value);
      }
      switch (_ = c ? $n(c) : window, e) {
        case "focusin":
          (nu(_) || _.contentEditable === "true") && (Fn = _, fi = c, Nt = null);
          break;
        case "focusout":
          Nt = fi = Fn = null;
          break;
        case "mousedown":
          di = !0;
          break;
        case "contextmenu":
        case "mouseup":
        case "dragend":
          di = !1, ou(h, t, m);
          break;
        case "selectionchange":
          if ($f)
            break;
        case "keydown":
        case "keyup":
          ou(h, t, m);
      }
      var C;
      if (to)
        e: {
          switch (e) {
            case "compositionstart":
              var N = "onCompositionStart";
              break e;
            case "compositionend":
              N = "onCompositionEnd";
              break e;
            case "compositionupdate":
              N = "onCompositionUpdate";
              break e;
          }
          N = void 0;
        }
      else
        In ? Is(e, t) && (N = "onCompositionEnd") : e === "keydown" && t.keyCode === 229 && (N = "onCompositionStart");
      N && (Ds && t.locale !== "ko" && (In || N !== "onCompositionStart" ? N === "onCompositionEnd" && In && (C = Os()) : (nn = m, bi = "value" in nn ? nn.value : nn.textContent, In = !0)), _ = Fr(c, N), 0 < _.length && (N = new Jo(N, e, null, t, m), h.push({ event: N, listeners: _ }), C ? N.data = C : (C = Fs(t), C !== null && (N.data = C)))), (C = Pf ? zf(e, t) : Tf(e, t)) && (c = Fr(c, "onBeforeInput"), 0 < c.length && (m = new Jo("onBeforeInput", "beforeinput", null, t, m), h.push({ event: m, listeners: c }), m.data = C));
    }
    Gs(h, n);
  });
}
function At(e, n, t) {
  return { instance: e, listener: n, currentTarget: t };
}
function Fr(e, n) {
  for (var t = n + "Capture", r = []; e !== null; ) {
    var l = e, i = l.stateNode;
    l.tag === 5 && i !== null && (l = i, i = Mt(e, t), i != null && r.unshift(At(e, i, l)), i = Mt(e, n), i != null && r.push(At(e, i, l))), e = e.return;
  }
  return r;
}
function Mn(e) {
  if (e === null)
    return null;
  do
    e = e.return;
  while (e && e.tag !== 5);
  return e || null;
}
function au(e, n, t, r, l) {
  for (var i = n._reactName, o = []; t !== null && t !== r; ) {
    var u = t, s = u.alternate, c = u.stateNode;
    if (s !== null && s === r)
      break;
    u.tag === 5 && c !== null && (u = c, l ? (s = Mt(t, i), s != null && o.unshift(At(t, s, u))) : l || (s = Mt(t, i), s != null && o.push(At(t, s, u)))), t = t.return;
  }
  o.length !== 0 && e.push({ event: n, listeners: o });
}
var Hf = /\r\n?/g, Wf = /\u0000|\uFFFD/g;
function cu(e) {
  return (typeof e == "string" ? e : "" + e).replace(Hf, `
`).replace(Wf, "");
}
function fr(e, n, t) {
  if (n = cu(n), cu(e) !== n && t)
    throw Error(y(425));
}
function Ur() {
}
var pi = null, mi = null;
function hi(e, n) {
  return e === "textarea" || e === "noscript" || typeof n.children == "string" || typeof n.children == "number" || typeof n.dangerouslySetInnerHTML == "object" && n.dangerouslySetInnerHTML !== null && n.dangerouslySetInnerHTML.__html != null;
}
var vi = typeof setTimeout == "function" ? setTimeout : void 0, Qf = typeof clearTimeout == "function" ? clearTimeout : void 0, fu = typeof Promise == "function" ? Promise : void 0, Kf = typeof queueMicrotask == "function" ? queueMicrotask : typeof fu < "u" ? function(e) {
  return fu.resolve(null).then(e).catch(Yf);
} : vi;
function Yf(e) {
  setTimeout(function() {
    throw e;
  });
}
function Dl(e, n) {
  var t = n, r = 0;
  do {
    var l = t.nextSibling;
    if (e.removeChild(t), l && l.nodeType === 8)
      if (t = l.data, t === "/$") {
        if (r === 0) {
          e.removeChild(l), It(n);
          return;
        }
        r--;
      } else
        t !== "$" && t !== "$?" && t !== "$!" || r++;
    t = l;
  } while (t);
  It(n);
}
function un(e) {
  for (; e != null; e = e.nextSibling) {
    var n = e.nodeType;
    if (n === 1 || n === 3)
      break;
    if (n === 8) {
      if (n = e.data, n === "$" || n === "$!" || n === "$?")
        break;
      if (n === "/$")
        return null;
    }
  }
  return e;
}
function du(e) {
  e = e.previousSibling;
  for (var n = 0; e; ) {
    if (e.nodeType === 8) {
      var t = e.data;
      if (t === "$" || t === "$!" || t === "$?") {
        if (n === 0)
          return e;
        n--;
      } else
        t === "/$" && n++;
    }
    e = e.previousSibling;
  }
  return null;
}
var ut = Math.random().toString(36).slice(2), Ie = "__reactFiber$" + ut, Vt = "__reactProps$" + ut, Qe = "__reactContainer$" + ut, yi = "__reactEvents$" + ut, Xf = "__reactListeners$" + ut, Gf = "__reactHandles$" + ut;
function Sn(e) {
  var n = e[Ie];
  if (n)
    return n;
  for (var t = e.parentNode; t; ) {
    if (n = t[Qe] || t[Ie]) {
      if (t = n.alternate, n.child !== null || t !== null && t.child !== null)
        for (e = du(e); e !== null; ) {
          if (t = e[Ie])
            return t;
          e = du(e);
        }
      return n;
    }
    e = t, t = e.parentNode;
  }
  return null;
}
function Jt(e) {
  return e = e[Ie] || e[Qe], !e || e.tag !== 5 && e.tag !== 6 && e.tag !== 13 && e.tag !== 3 ? null : e;
}
function $n(e) {
  if (e.tag === 5 || e.tag === 6)
    return e.stateNode;
  throw Error(y(33));
}
function il(e) {
  return e[Vt] || null;
}
var gi = [], An = -1;
function hn(e) {
  return { current: e };
}
function I(e) {
  0 > An || (e.current = gi[An], gi[An] = null, An--);
}
function O(e, n) {
  An++, gi[An] = e.current, e.current = n;
}
var pn = {}, le = hn(pn), fe = hn(!1), Nn = pn;
function bn(e, n) {
  var t = e.type.contextTypes;
  if (!t)
    return pn;
  var r = e.stateNode;
  if (r && r.__reactInternalMemoizedUnmaskedChildContext === n)
    return r.__reactInternalMemoizedMaskedChildContext;
  var l = {}, i;
  for (i in t)
    l[i] = n[i];
  return r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = n, e.__reactInternalMemoizedMaskedChildContext = l), l;
}
function de(e) {
  return e = e.childContextTypes, e != null;
}
function $r() {
  I(fe), I(le);
}
function pu(e, n, t) {
  if (le.current !== pn)
    throw Error(y(168));
  O(le, n), O(fe, t);
}
function Js(e, n, t) {
  var r = e.stateNode;
  if (n = n.childContextTypes, typeof r.getChildContext != "function")
    return t;
  r = r.getChildContext();
  for (var l in r)
    if (!(l in n))
      throw Error(y(108, jc(e) || "Unknown", l));
  return V({}, t, r);
}
function Ar(e) {
  return e = (e = e.stateNode) && e.__reactInternalMemoizedMergedChildContext || pn, Nn = le.current, O(le, e), O(fe, fe.current), !0;
}
function mu(e, n, t) {
  var r = e.stateNode;
  if (!r)
    throw Error(y(169));
  t ? (e = Js(e, n, Nn), r.__reactInternalMemoizedMergedChildContext = e, I(fe), I(le), O(le, e)) : I(fe), O(fe, t);
}
var Ae = null, ol = !1, Il = !1;
function qs(e) {
  Ae === null ? Ae = [e] : Ae.push(e);
}
function Zf(e) {
  ol = !0, qs(e);
}
function vn() {
  if (!Il && Ae !== null) {
    Il = !0;
    var e = 0, n = M;
    try {
      var t = Ae;
      for (M = 1; e < t.length; e++) {
        var r = t[e];
        do
          r = r(!0);
        while (r !== null);
      }
      Ae = null, ol = !1;
    } catch (l) {
      throw Ae !== null && (Ae = Ae.slice(e + 1)), xs(Gi, vn), l;
    } finally {
      M = n, Il = !1;
    }
  }
  return null;
}
var Vn = [], Bn = 0, Vr = null, Br = 0, ke = [], Se = 0, Pn = null, Ve = 1, Be = "";
function wn(e, n) {
  Vn[Bn++] = Br, Vn[Bn++] = Vr, Vr = e, Br = n;
}
function bs(e, n, t) {
  ke[Se++] = Ve, ke[Se++] = Be, ke[Se++] = Pn, Pn = e;
  var r = Ve;
  e = Be;
  var l = 32 - Re(r) - 1;
  r &= ~(1 << l), t += 1;
  var i = 32 - Re(n) + l;
  if (30 < i) {
    var o = l - l % 5;
    i = (r & (1 << o) - 1).toString(32), r >>= o, l -= o, Ve = 1 << 32 - Re(n) + l | t << l | r, Be = i + e;
  } else
    Ve = 1 << i | t << l | r, Be = e;
}
function lo(e) {
  e.return !== null && (wn(e, 1), bs(e, 1, 0));
}
function io(e) {
  for (; e === Vr; )
    Vr = Vn[--Bn], Vn[Bn] = null, Br = Vn[--Bn], Vn[Bn] = null;
  for (; e === Pn; )
    Pn = ke[--Se], ke[Se] = null, Be = ke[--Se], ke[Se] = null, Ve = ke[--Se], ke[Se] = null;
}
var ve = null, he = null, U = !1, Le = null;
function ea(e, n) {
  var t = Ee(5, null, null, 0);
  t.elementType = "DELETED", t.stateNode = n, t.return = e, n = e.deletions, n === null ? (e.deletions = [t], e.flags |= 16) : n.push(t);
}
function hu(e, n) {
  switch (e.tag) {
    case 5:
      var t = e.type;
      return n = n.nodeType !== 1 || t.toLowerCase() !== n.nodeName.toLowerCase() ? null : n, n !== null ? (e.stateNode = n, ve = e, he = un(n.firstChild), !0) : !1;
    case 6:
      return n = e.pendingProps === "" || n.nodeType !== 3 ? null : n, n !== null ? (e.stateNode = n, ve = e, he = null, !0) : !1;
    case 13:
      return n = n.nodeType !== 8 ? null : n, n !== null ? (t = Pn !== null ? { id: Ve, overflow: Be } : null, e.memoizedState = { dehydrated: n, treeContext: t, retryLane: 1073741824 }, t = Ee(18, null, null, 0), t.stateNode = n, t.return = e, e.child = t, ve = e, he = null, !0) : !1;
    default:
      return !1;
  }
}
function wi(e) {
  return (e.mode & 1) !== 0 && (e.flags & 128) === 0;
}
function ki(e) {
  if (U) {
    var n = he;
    if (n) {
      var t = n;
      if (!hu(e, n)) {
        if (wi(e))
          throw Error(y(418));
        n = un(t.nextSibling);
        var r = ve;
        n && hu(e, n) ? ea(r, t) : (e.flags = e.flags & -4097 | 2, U = !1, ve = e);
      }
    } else {
      if (wi(e))
        throw Error(y(418));
      e.flags = e.flags & -4097 | 2, U = !1, ve = e;
    }
  }
}
function vu(e) {
  for (e = e.return; e !== null && e.tag !== 5 && e.tag !== 3 && e.tag !== 13; )
    e = e.return;
  ve = e;
}
function dr(e) {
  if (e !== ve)
    return !1;
  if (!U)
    return vu(e), U = !0, !1;
  var n;
  if ((n = e.tag !== 3) && !(n = e.tag !== 5) && (n = e.type, n = n !== "head" && n !== "body" && !hi(e.type, e.memoizedProps)), n && (n = he)) {
    if (wi(e))
      throw na(), Error(y(418));
    for (; n; )
      ea(e, n), n = un(n.nextSibling);
  }
  if (vu(e), e.tag === 13) {
    if (e = e.memoizedState, e = e !== null ? e.dehydrated : null, !e)
      throw Error(y(317));
    e: {
      for (e = e.nextSibling, n = 0; e; ) {
        if (e.nodeType === 8) {
          var t = e.data;
          if (t === "/$") {
            if (n === 0) {
              he = un(e.nextSibling);
              break e;
            }
            n--;
          } else
            t !== "$" && t !== "$!" && t !== "$?" || n++;
        }
        e = e.nextSibling;
      }
      he = null;
    }
  } else
    he = ve ? un(e.stateNode.nextSibling) : null;
  return !0;
}
function na() {
  for (var e = he; e; )
    e = un(e.nextSibling);
}
function et() {
  he = ve = null, U = !1;
}
function oo(e) {
  Le === null ? Le = [e] : Le.push(e);
}
var Jf = Xe.ReactCurrentBatchConfig;
function ht(e, n, t) {
  if (e = t.ref, e !== null && typeof e != "function" && typeof e != "object") {
    if (t._owner) {
      if (t = t._owner, t) {
        if (t.tag !== 1)
          throw Error(y(309));
        var r = t.stateNode;
      }
      if (!r)
        throw Error(y(147, e));
      var l = r, i = "" + e;
      return n !== null && n.ref !== null && typeof n.ref == "function" && n.ref._stringRef === i ? n.ref : (n = function(o) {
        var u = l.refs;
        o === null ? delete u[i] : u[i] = o;
      }, n._stringRef = i, n);
    }
    if (typeof e != "string")
      throw Error(y(284));
    if (!t._owner)
      throw Error(y(290, e));
  }
  return e;
}
function pr(e, n) {
  throw e = Object.prototype.toString.call(n), Error(y(31, e === "[object Object]" ? "object with keys {" + Object.keys(n).join(", ") + "}" : e));
}
function yu(e) {
  var n = e._init;
  return n(e._payload);
}
function ta(e) {
  function n(f, a) {
    if (e) {
      var d = f.deletions;
      d === null ? (f.deletions = [a], f.flags |= 16) : d.push(a);
    }
  }
  function t(f, a) {
    if (!e)
      return null;
    for (; a !== null; )
      n(f, a), a = a.sibling;
    return null;
  }
  function r(f, a) {
    for (f = /* @__PURE__ */ new Map(); a !== null; )
      a.key !== null ? f.set(a.key, a) : f.set(a.index, a), a = a.sibling;
    return f;
  }
  function l(f, a) {
    return f = fn(f, a), f.index = 0, f.sibling = null, f;
  }
  function i(f, a, d) {
    return f.index = d, e ? (d = f.alternate, d !== null ? (d = d.index, d < a ? (f.flags |= 2, a) : d) : (f.flags |= 2, a)) : (f.flags |= 1048576, a);
  }
  function o(f) {
    return e && f.alternate === null && (f.flags |= 2), f;
  }
  function u(f, a, d, v) {
    return a === null || a.tag !== 6 ? (a = Hl(d, f.mode, v), a.return = f, a) : (a = l(a, d), a.return = f, a);
  }
  function s(f, a, d, v) {
    var E = d.type;
    return E === Dn ? m(f, a, d.props.children, v, d.key) : a !== null && (a.elementType === E || typeof E == "object" && E !== null && E.$$typeof === Ze && yu(E) === a.type) ? (v = l(a, d.props), v.ref = ht(f, a, d), v.return = f, v) : (v = Tr(d.type, d.key, d.props, null, f.mode, v), v.ref = ht(f, a, d), v.return = f, v);
  }
  function c(f, a, d, v) {
    return a === null || a.tag !== 4 || a.stateNode.containerInfo !== d.containerInfo || a.stateNode.implementation !== d.implementation ? (a = Wl(d, f.mode, v), a.return = f, a) : (a = l(a, d.children || []), a.return = f, a);
  }
  function m(f, a, d, v, E) {
    return a === null || a.tag !== 7 ? (a = Cn(d, f.mode, v, E), a.return = f, a) : (a = l(a, d), a.return = f, a);
  }
  function h(f, a, d) {
    if (typeof a == "string" && a !== "" || typeof a == "number")
      return a = Hl("" + a, f.mode, d), a.return = f, a;
    if (typeof a == "object" && a !== null) {
      switch (a.$$typeof) {
        case tr:
          return d = Tr(a.type, a.key, a.props, null, f.mode, d), d.ref = ht(f, null, a), d.return = f, d;
        case On:
          return a = Wl(a, f.mode, d), a.return = f, a;
        case Ze:
          var v = a._init;
          return h(f, v(a._payload), d);
      }
      if (wt(a) || ct(a))
        return a = Cn(a, f.mode, d, null), a.return = f, a;
      pr(f, a);
    }
    return null;
  }
  function p(f, a, d, v) {
    var E = a !== null ? a.key : null;
    if (typeof d == "string" && d !== "" || typeof d == "number")
      return E !== null ? null : u(f, a, "" + d, v);
    if (typeof d == "object" && d !== null) {
      switch (d.$$typeof) {
        case tr:
          return d.key === E ? s(f, a, d, v) : null;
        case On:
          return d.key === E ? c(f, a, d, v) : null;
        case Ze:
          return E = d._init, p(
            f,
            a,
            E(d._payload),
            v
          );
      }
      if (wt(d) || ct(d))
        return E !== null ? null : m(f, a, d, v, null);
      pr(f, d);
    }
    return null;
  }
  function g(f, a, d, v, E) {
    if (typeof v == "string" && v !== "" || typeof v == "number")
      return f = f.get(d) || null, u(a, f, "" + v, E);
    if (typeof v == "object" && v !== null) {
      switch (v.$$typeof) {
        case tr:
          return f = f.get(v.key === null ? d : v.key) || null, s(a, f, v, E);
        case On:
          return f = f.get(v.key === null ? d : v.key) || null, c(a, f, v, E);
        case Ze:
          var _ = v._init;
          return g(f, a, d, _(v._payload), E);
      }
      if (wt(v) || ct(v))
        return f = f.get(d) || null, m(a, f, v, E, null);
      pr(a, v);
    }
    return null;
  }
  function w(f, a, d, v) {
    for (var E = null, _ = null, C = a, N = a = 0, H = null; C !== null && N < d.length; N++) {
      C.index > N ? (H = C, C = null) : H = C.sibling;
      var R = p(f, C, d[N], v);
      if (R === null) {
        C === null && (C = H);
        break;
      }
      e && C && R.alternate === null && n(f, C), a = i(R, a, N), _ === null ? E = R : _.sibling = R, _ = R, C = H;
    }
    if (N === d.length)
      return t(f, C), U && wn(f, N), E;
    if (C === null) {
      for (; N < d.length; N++)
        C = h(f, d[N], v), C !== null && (a = i(C, a, N), _ === null ? E = C : _.sibling = C, _ = C);
      return U && wn(f, N), E;
    }
    for (C = r(f, C); N < d.length; N++)
      H = g(C, f, N, d[N], v), H !== null && (e && H.alternate !== null && C.delete(H.key === null ? N : H.key), a = i(H, a, N), _ === null ? E = H : _.sibling = H, _ = H);
    return e && C.forEach(function(Ne) {
      return n(f, Ne);
    }), U && wn(f, N), E;
  }
  function k(f, a, d, v) {
    var E = ct(d);
    if (typeof E != "function")
      throw Error(y(150));
    if (d = E.call(d), d == null)
      throw Error(y(151));
    for (var _ = E = null, C = a, N = a = 0, H = null, R = d.next(); C !== null && !R.done; N++, R = d.next()) {
      C.index > N ? (H = C, C = null) : H = C.sibling;
      var Ne = p(f, C, R.value, v);
      if (Ne === null) {
        C === null && (C = H);
        break;
      }
      e && C && Ne.alternate === null && n(f, C), a = i(Ne, a, N), _ === null ? E = Ne : _.sibling = Ne, _ = Ne, C = H;
    }
    if (R.done)
      return t(
        f,
        C
      ), U && wn(f, N), E;
    if (C === null) {
      for (; !R.done; N++, R = d.next())
        R = h(f, R.value, v), R !== null && (a = i(R, a, N), _ === null ? E = R : _.sibling = R, _ = R);
      return U && wn(f, N), E;
    }
    for (C = r(f, C); !R.done; N++, R = d.next())
      R = g(C, f, N, R.value, v), R !== null && (e && R.alternate !== null && C.delete(R.key === null ? N : R.key), a = i(R, a, N), _ === null ? E = R : _.sibling = R, _ = R);
    return e && C.forEach(function(st) {
      return n(f, st);
    }), U && wn(f, N), E;
  }
  function F(f, a, d, v) {
    if (typeof d == "object" && d !== null && d.type === Dn && d.key === null && (d = d.props.children), typeof d == "object" && d !== null) {
      switch (d.$$typeof) {
        case tr:
          e: {
            for (var E = d.key, _ = a; _ !== null; ) {
              if (_.key === E) {
                if (E = d.type, E === Dn) {
                  if (_.tag === 7) {
                    t(f, _.sibling), a = l(_, d.props.children), a.return = f, f = a;
                    break e;
                  }
                } else if (_.elementType === E || typeof E == "object" && E !== null && E.$$typeof === Ze && yu(E) === _.type) {
                  t(f, _.sibling), a = l(_, d.props), a.ref = ht(f, _, d), a.return = f, f = a;
                  break e;
                }
                t(f, _);
                break;
              } else
                n(f, _);
              _ = _.sibling;
            }
            d.type === Dn ? (a = Cn(d.props.children, f.mode, v, d.key), a.return = f, f = a) : (v = Tr(d.type, d.key, d.props, null, f.mode, v), v.ref = ht(f, a, d), v.return = f, f = v);
          }
          return o(f);
        case On:
          e: {
            for (_ = d.key; a !== null; ) {
              if (a.key === _)
                if (a.tag === 4 && a.stateNode.containerInfo === d.containerInfo && a.stateNode.implementation === d.implementation) {
                  t(f, a.sibling), a = l(a, d.children || []), a.return = f, f = a;
                  break e;
                } else {
                  t(f, a);
                  break;
                }
              else
                n(f, a);
              a = a.sibling;
            }
            a = Wl(d, f.mode, v), a.return = f, f = a;
          }
          return o(f);
        case Ze:
          return _ = d._init, F(f, a, _(d._payload), v);
      }
      if (wt(d))
        return w(f, a, d, v);
      if (ct(d))
        return k(f, a, d, v);
      pr(f, d);
    }
    return typeof d == "string" && d !== "" || typeof d == "number" ? (d = "" + d, a !== null && a.tag === 6 ? (t(f, a.sibling), a = l(a, d), a.return = f, f = a) : (t(f, a), a = Hl(d, f.mode, v), a.return = f, f = a), o(f)) : t(f, a);
  }
  return F;
}
var nt = ta(!0), ra = ta(!1), Hr = hn(null), Wr = null, Hn = null, uo = null;
function so() {
  uo = Hn = Wr = null;
}
function ao(e) {
  var n = Hr.current;
  I(Hr), e._currentValue = n;
}
function Si(e, n, t) {
  for (; e !== null; ) {
    var r = e.alternate;
    if ((e.childLanes & n) !== n ? (e.childLanes |= n, r !== null && (r.childLanes |= n)) : r !== null && (r.childLanes & n) !== n && (r.childLanes |= n), e === t)
      break;
    e = e.return;
  }
}
function Zn(e, n) {
  Wr = e, uo = Hn = null, e = e.dependencies, e !== null && e.firstContext !== null && (e.lanes & n && (ce = !0), e.firstContext = null);
}
function _e(e) {
  var n = e._currentValue;
  if (uo !== e)
    if (e = { context: e, memoizedValue: n, next: null }, Hn === null) {
      if (Wr === null)
        throw Error(y(308));
      Hn = e, Wr.dependencies = { lanes: 0, firstContext: e };
    } else
      Hn = Hn.next = e;
  return n;
}
var En = null;
function co(e) {
  En === null ? En = [e] : En.push(e);
}
function la(e, n, t, r) {
  var l = n.interleaved;
  return l === null ? (t.next = t, co(n)) : (t.next = l.next, l.next = t), n.interleaved = t, Ke(e, r);
}
function Ke(e, n) {
  e.lanes |= n;
  var t = e.alternate;
  for (t !== null && (t.lanes |= n), t = e, e = e.return; e !== null; )
    e.childLanes |= n, t = e.alternate, t !== null && (t.childLanes |= n), t = e, e = e.return;
  return t.tag === 3 ? t.stateNode : null;
}
var Je = !1;
function fo(e) {
  e.updateQueue = { baseState: e.memoizedState, firstBaseUpdate: null, lastBaseUpdate: null, shared: { pending: null, interleaved: null, lanes: 0 }, effects: null };
}
function ia(e, n) {
  e = e.updateQueue, n.updateQueue === e && (n.updateQueue = { baseState: e.baseState, firstBaseUpdate: e.firstBaseUpdate, lastBaseUpdate: e.lastBaseUpdate, shared: e.shared, effects: e.effects });
}
function He(e, n) {
  return { eventTime: e, lane: n, tag: 0, payload: null, callback: null, next: null };
}
function sn(e, n, t) {
  var r = e.updateQueue;
  if (r === null)
    return null;
  if (r = r.shared, j & 2) {
    var l = r.pending;
    return l === null ? n.next = n : (n.next = l.next, l.next = n), r.pending = n, Ke(e, t);
  }
  return l = r.interleaved, l === null ? (n.next = n, co(r)) : (n.next = l.next, l.next = n), r.interleaved = n, Ke(e, t);
}
function xr(e, n, t) {
  if (n = n.updateQueue, n !== null && (n = n.shared, (t & 4194240) !== 0)) {
    var r = n.lanes;
    r &= e.pendingLanes, t |= r, n.lanes = t, Zi(e, t);
  }
}
function gu(e, n) {
  var t = e.updateQueue, r = e.alternate;
  if (r !== null && (r = r.updateQueue, t === r)) {
    var l = null, i = null;
    if (t = t.firstBaseUpdate, t !== null) {
      do {
        var o = { eventTime: t.eventTime, lane: t.lane, tag: t.tag, payload: t.payload, callback: t.callback, next: null };
        i === null ? l = i = o : i = i.next = o, t = t.next;
      } while (t !== null);
      i === null ? l = i = n : i = i.next = n;
    } else
      l = i = n;
    t = { baseState: r.baseState, firstBaseUpdate: l, lastBaseUpdate: i, shared: r.shared, effects: r.effects }, e.updateQueue = t;
    return;
  }
  e = t.lastBaseUpdate, e === null ? t.firstBaseUpdate = n : e.next = n, t.lastBaseUpdate = n;
}
function Qr(e, n, t, r) {
  var l = e.updateQueue;
  Je = !1;
  var i = l.firstBaseUpdate, o = l.lastBaseUpdate, u = l.shared.pending;
  if (u !== null) {
    l.shared.pending = null;
    var s = u, c = s.next;
    s.next = null, o === null ? i = c : o.next = c, o = s;
    var m = e.alternate;
    m !== null && (m = m.updateQueue, u = m.lastBaseUpdate, u !== o && (u === null ? m.firstBaseUpdate = c : u.next = c, m.lastBaseUpdate = s));
  }
  if (i !== null) {
    var h = l.baseState;
    o = 0, m = c = s = null, u = i;
    do {
      var p = u.lane, g = u.eventTime;
      if ((r & p) === p) {
        m !== null && (m = m.next = {
          eventTime: g,
          lane: 0,
          tag: u.tag,
          payload: u.payload,
          callback: u.callback,
          next: null
        });
        e: {
          var w = e, k = u;
          switch (p = n, g = t, k.tag) {
            case 1:
              if (w = k.payload, typeof w == "function") {
                h = w.call(g, h, p);
                break e;
              }
              h = w;
              break e;
            case 3:
              w.flags = w.flags & -65537 | 128;
            case 0:
              if (w = k.payload, p = typeof w == "function" ? w.call(g, h, p) : w, p == null)
                break e;
              h = V({}, h, p);
              break e;
            case 2:
              Je = !0;
          }
        }
        u.callback !== null && u.lane !== 0 && (e.flags |= 64, p = l.effects, p === null ? l.effects = [u] : p.push(u));
      } else
        g = { eventTime: g, lane: p, tag: u.tag, payload: u.payload, callback: u.callback, next: null }, m === null ? (c = m = g, s = h) : m = m.next = g, o |= p;
      if (u = u.next, u === null) {
        if (u = l.shared.pending, u === null)
          break;
        p = u, u = p.next, p.next = null, l.lastBaseUpdate = p, l.shared.pending = null;
      }
    } while (1);
    if (m === null && (s = h), l.baseState = s, l.firstBaseUpdate = c, l.lastBaseUpdate = m, n = l.shared.interleaved, n !== null) {
      l = n;
      do
        o |= l.lane, l = l.next;
      while (l !== n);
    } else
      i === null && (l.shared.lanes = 0);
    Tn |= o, e.lanes = o, e.memoizedState = h;
  }
}
function wu(e, n, t) {
  if (e = n.effects, n.effects = null, e !== null)
    for (n = 0; n < e.length; n++) {
      var r = e[n], l = r.callback;
      if (l !== null) {
        if (r.callback = null, r = t, typeof l != "function")
          throw Error(y(191, l));
        l.call(r);
      }
    }
}
var qt = {}, Ue = hn(qt), Bt = hn(qt), Ht = hn(qt);
function xn(e) {
  if (e === qt)
    throw Error(y(174));
  return e;
}
function po(e, n) {
  switch (O(Ht, n), O(Bt, e), O(Ue, qt), e = n.nodeType, e) {
    case 9:
    case 11:
      n = (n = n.documentElement) ? n.namespaceURI : ni(null, "");
      break;
    default:
      e = e === 8 ? n.parentNode : n, n = e.namespaceURI || null, e = e.tagName, n = ni(n, e);
  }
  I(Ue), O(Ue, n);
}
function tt() {
  I(Ue), I(Bt), I(Ht);
}
function oa(e) {
  xn(Ht.current);
  var n = xn(Ue.current), t = ni(n, e.type);
  n !== t && (O(Bt, e), O(Ue, t));
}
function mo(e) {
  Bt.current === e && (I(Ue), I(Bt));
}
var $ = hn(0);
function Kr(e) {
  for (var n = e; n !== null; ) {
    if (n.tag === 13) {
      var t = n.memoizedState;
      if (t !== null && (t = t.dehydrated, t === null || t.data === "$?" || t.data === "$!"))
        return n;
    } else if (n.tag === 19 && n.memoizedProps.revealOrder !== void 0) {
      if (n.flags & 128)
        return n;
    } else if (n.child !== null) {
      n.child.return = n, n = n.child;
      continue;
    }
    if (n === e)
      break;
    for (; n.sibling === null; ) {
      if (n.return === null || n.return === e)
        return null;
      n = n.return;
    }
    n.sibling.return = n.return, n = n.sibling;
  }
  return null;
}
var Fl = [];
function ho() {
  for (var e = 0; e < Fl.length; e++)
    Fl[e]._workInProgressVersionPrimary = null;
  Fl.length = 0;
}
var _r = Xe.ReactCurrentDispatcher, Ul = Xe.ReactCurrentBatchConfig, zn = 0, A = null, Y = null, Z = null, Yr = !1, Pt = !1, Wt = 0, qf = 0;
function ne() {
  throw Error(y(321));
}
function vo(e, n) {
  if (n === null)
    return !1;
  for (var t = 0; t < n.length && t < e.length; t++)
    if (!Me(e[t], n[t]))
      return !1;
  return !0;
}
function yo(e, n, t, r, l, i) {
  if (zn = i, A = n, n.memoizedState = null, n.updateQueue = null, n.lanes = 0, _r.current = e === null || e.memoizedState === null ? td : rd, e = t(r, l), Pt) {
    i = 0;
    do {
      if (Pt = !1, Wt = 0, 25 <= i)
        throw Error(y(301));
      i += 1, Z = Y = null, n.updateQueue = null, _r.current = ld, e = t(r, l);
    } while (Pt);
  }
  if (_r.current = Xr, n = Y !== null && Y.next !== null, zn = 0, Z = Y = A = null, Yr = !1, n)
    throw Error(y(300));
  return e;
}
function go() {
  var e = Wt !== 0;
  return Wt = 0, e;
}
function De() {
  var e = { memoizedState: null, baseState: null, baseQueue: null, queue: null, next: null };
  return Z === null ? A.memoizedState = Z = e : Z = Z.next = e, Z;
}
function Ce() {
  if (Y === null) {
    var e = A.alternate;
    e = e !== null ? e.memoizedState : null;
  } else
    e = Y.next;
  var n = Z === null ? A.memoizedState : Z.next;
  if (n !== null)
    Z = n, Y = e;
  else {
    if (e === null)
      throw Error(y(310));
    Y = e, e = { memoizedState: Y.memoizedState, baseState: Y.baseState, baseQueue: Y.baseQueue, queue: Y.queue, next: null }, Z === null ? A.memoizedState = Z = e : Z = Z.next = e;
  }
  return Z;
}
function Qt(e, n) {
  return typeof n == "function" ? n(e) : n;
}
function $l(e) {
  var n = Ce(), t = n.queue;
  if (t === null)
    throw Error(y(311));
  t.lastRenderedReducer = e;
  var r = Y, l = r.baseQueue, i = t.pending;
  if (i !== null) {
    if (l !== null) {
      var o = l.next;
      l.next = i.next, i.next = o;
    }
    r.baseQueue = l = i, t.pending = null;
  }
  if (l !== null) {
    i = l.next, r = r.baseState;
    var u = o = null, s = null, c = i;
    do {
      var m = c.lane;
      if ((zn & m) === m)
        s !== null && (s = s.next = { lane: 0, action: c.action, hasEagerState: c.hasEagerState, eagerState: c.eagerState, next: null }), r = c.hasEagerState ? c.eagerState : e(r, c.action);
      else {
        var h = {
          lane: m,
          action: c.action,
          hasEagerState: c.hasEagerState,
          eagerState: c.eagerState,
          next: null
        };
        s === null ? (u = s = h, o = r) : s = s.next = h, A.lanes |= m, Tn |= m;
      }
      c = c.next;
    } while (c !== null && c !== i);
    s === null ? o = r : s.next = u, Me(r, n.memoizedState) || (ce = !0), n.memoizedState = r, n.baseState = o, n.baseQueue = s, t.lastRenderedState = r;
  }
  if (e = t.interleaved, e !== null) {
    l = e;
    do
      i = l.lane, A.lanes |= i, Tn |= i, l = l.next;
    while (l !== e);
  } else
    l === null && (t.lanes = 0);
  return [n.memoizedState, t.dispatch];
}
function Al(e) {
  var n = Ce(), t = n.queue;
  if (t === null)
    throw Error(y(311));
  t.lastRenderedReducer = e;
  var r = t.dispatch, l = t.pending, i = n.memoizedState;
  if (l !== null) {
    t.pending = null;
    var o = l = l.next;
    do
      i = e(i, o.action), o = o.next;
    while (o !== l);
    Me(i, n.memoizedState) || (ce = !0), n.memoizedState = i, n.baseQueue === null && (n.baseState = i), t.lastRenderedState = i;
  }
  return [i, r];
}
function ua() {
}
function sa(e, n) {
  var t = A, r = Ce(), l = n(), i = !Me(r.memoizedState, l);
  if (i && (r.memoizedState = l, ce = !0), r = r.queue, wo(fa.bind(null, t, r, e), [e]), r.getSnapshot !== n || i || Z !== null && Z.memoizedState.tag & 1) {
    if (t.flags |= 2048, Kt(9, ca.bind(null, t, r, l, n), void 0, null), J === null)
      throw Error(y(349));
    zn & 30 || aa(t, n, l);
  }
  return l;
}
function aa(e, n, t) {
  e.flags |= 16384, e = { getSnapshot: n, value: t }, n = A.updateQueue, n === null ? (n = { lastEffect: null, stores: null }, A.updateQueue = n, n.stores = [e]) : (t = n.stores, t === null ? n.stores = [e] : t.push(e));
}
function ca(e, n, t, r) {
  n.value = t, n.getSnapshot = r, da(n) && pa(e);
}
function fa(e, n, t) {
  return t(function() {
    da(n) && pa(e);
  });
}
function da(e) {
  var n = e.getSnapshot;
  e = e.value;
  try {
    var t = n();
    return !Me(e, t);
  } catch {
    return !0;
  }
}
function pa(e) {
  var n = Ke(e, 1);
  n !== null && je(n, e, 1, -1);
}
function ku(e) {
  var n = De();
  return typeof e == "function" && (e = e()), n.memoizedState = n.baseState = e, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: Qt, lastRenderedState: e }, n.queue = e, e = e.dispatch = nd.bind(null, A, e), [n.memoizedState, e];
}
function Kt(e, n, t, r) {
  return e = { tag: e, create: n, destroy: t, deps: r, next: null }, n = A.updateQueue, n === null ? (n = { lastEffect: null, stores: null }, A.updateQueue = n, n.lastEffect = e.next = e) : (t = n.lastEffect, t === null ? n.lastEffect = e.next = e : (r = t.next, t.next = e, e.next = r, n.lastEffect = e)), e;
}
function ma() {
  return Ce().memoizedState;
}
function Cr(e, n, t, r) {
  var l = De();
  A.flags |= e, l.memoizedState = Kt(1 | n, t, void 0, r === void 0 ? null : r);
}
function ul(e, n, t, r) {
  var l = Ce();
  r = r === void 0 ? null : r;
  var i = void 0;
  if (Y !== null) {
    var o = Y.memoizedState;
    if (i = o.destroy, r !== null && vo(r, o.deps)) {
      l.memoizedState = Kt(n, t, i, r);
      return;
    }
  }
  A.flags |= e, l.memoizedState = Kt(1 | n, t, i, r);
}
function Su(e, n) {
  return Cr(8390656, 8, e, n);
}
function wo(e, n) {
  return ul(2048, 8, e, n);
}
function ha(e, n) {
  return ul(4, 2, e, n);
}
function va(e, n) {
  return ul(4, 4, e, n);
}
function ya(e, n) {
  if (typeof n == "function")
    return e = e(), n(e), function() {
      n(null);
    };
  if (n != null)
    return e = e(), n.current = e, function() {
      n.current = null;
    };
}
function ga(e, n, t) {
  return t = t != null ? t.concat([e]) : null, ul(4, 4, ya.bind(null, n, e), t);
}
function ko() {
}
function wa(e, n) {
  var t = Ce();
  n = n === void 0 ? null : n;
  var r = t.memoizedState;
  return r !== null && n !== null && vo(n, r[1]) ? r[0] : (t.memoizedState = [e, n], e);
}
function ka(e, n) {
  var t = Ce();
  n = n === void 0 ? null : n;
  var r = t.memoizedState;
  return r !== null && n !== null && vo(n, r[1]) ? r[0] : (e = e(), t.memoizedState = [e, n], e);
}
function Sa(e, n, t) {
  return zn & 21 ? (Me(t, n) || (t = Ns(), A.lanes |= t, Tn |= t, e.baseState = !0), n) : (e.baseState && (e.baseState = !1, ce = !0), e.memoizedState = t);
}
function bf(e, n) {
  var t = M;
  M = t !== 0 && 4 > t ? t : 4, e(!0);
  var r = Ul.transition;
  Ul.transition = {};
  try {
    e(!1), n();
  } finally {
    M = t, Ul.transition = r;
  }
}
function Ea() {
  return Ce().memoizedState;
}
function ed(e, n, t) {
  var r = cn(e);
  if (t = { lane: r, action: t, hasEagerState: !1, eagerState: null, next: null }, xa(e))
    _a(n, t);
  else if (t = la(e, n, t, r), t !== null) {
    var l = oe();
    je(t, e, r, l), Ca(t, n, r);
  }
}
function nd(e, n, t) {
  var r = cn(e), l = { lane: r, action: t, hasEagerState: !1, eagerState: null, next: null };
  if (xa(e))
    _a(n, l);
  else {
    var i = e.alternate;
    if (e.lanes === 0 && (i === null || i.lanes === 0) && (i = n.lastRenderedReducer, i !== null))
      try {
        var o = n.lastRenderedState, u = i(o, t);
        if (l.hasEagerState = !0, l.eagerState = u, Me(u, o)) {
          var s = n.interleaved;
          s === null ? (l.next = l, co(n)) : (l.next = s.next, s.next = l), n.interleaved = l;
          return;
        }
      } catch {
      } finally {
      }
    t = la(e, n, l, r), t !== null && (l = oe(), je(t, e, r, l), Ca(t, n, r));
  }
}
function xa(e) {
  var n = e.alternate;
  return e === A || n !== null && n === A;
}
function _a(e, n) {
  Pt = Yr = !0;
  var t = e.pending;
  t === null ? n.next = n : (n.next = t.next, t.next = n), e.pending = n;
}
function Ca(e, n, t) {
  if (t & 4194240) {
    var r = n.lanes;
    r &= e.pendingLanes, t |= r, n.lanes = t, Zi(e, t);
  }
}
var Xr = { readContext: _e, useCallback: ne, useContext: ne, useEffect: ne, useImperativeHandle: ne, useInsertionEffect: ne, useLayoutEffect: ne, useMemo: ne, useReducer: ne, useRef: ne, useState: ne, useDebugValue: ne, useDeferredValue: ne, useTransition: ne, useMutableSource: ne, useSyncExternalStore: ne, useId: ne, unstable_isNewReconciler: !1 }, td = { readContext: _e, useCallback: function(e, n) {
  return De().memoizedState = [e, n === void 0 ? null : n], e;
}, useContext: _e, useEffect: Su, useImperativeHandle: function(e, n, t) {
  return t = t != null ? t.concat([e]) : null, Cr(
    4194308,
    4,
    ya.bind(null, n, e),
    t
  );
}, useLayoutEffect: function(e, n) {
  return Cr(4194308, 4, e, n);
}, useInsertionEffect: function(e, n) {
  return Cr(4, 2, e, n);
}, useMemo: function(e, n) {
  var t = De();
  return n = n === void 0 ? null : n, e = e(), t.memoizedState = [e, n], e;
}, useReducer: function(e, n, t) {
  var r = De();
  return n = t !== void 0 ? t(n) : n, r.memoizedState = r.baseState = n, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: e, lastRenderedState: n }, r.queue = e, e = e.dispatch = ed.bind(null, A, e), [r.memoizedState, e];
}, useRef: function(e) {
  var n = De();
  return e = { current: e }, n.memoizedState = e;
}, useState: ku, useDebugValue: ko, useDeferredValue: function(e) {
  return De().memoizedState = e;
}, useTransition: function() {
  var e = ku(!1), n = e[0];
  return e = bf.bind(null, e[1]), De().memoizedState = e, [n, e];
}, useMutableSource: function() {
}, useSyncExternalStore: function(e, n, t) {
  var r = A, l = De();
  if (U) {
    if (t === void 0)
      throw Error(y(407));
    t = t();
  } else {
    if (t = n(), J === null)
      throw Error(y(349));
    zn & 30 || aa(r, n, t);
  }
  l.memoizedState = t;
  var i = { value: t, getSnapshot: n };
  return l.queue = i, Su(fa.bind(
    null,
    r,
    i,
    e
  ), [e]), r.flags |= 2048, Kt(9, ca.bind(null, r, i, t, n), void 0, null), t;
}, useId: function() {
  var e = De(), n = J.identifierPrefix;
  if (U) {
    var t = Be, r = Ve;
    t = (r & ~(1 << 32 - Re(r) - 1)).toString(32) + t, n = ":" + n + "R" + t, t = Wt++, 0 < t && (n += "H" + t.toString(32)), n += ":";
  } else
    t = qf++, n = ":" + n + "r" + t.toString(32) + ":";
  return e.memoizedState = n;
}, unstable_isNewReconciler: !1 }, rd = {
  readContext: _e,
  useCallback: wa,
  useContext: _e,
  useEffect: wo,
  useImperativeHandle: ga,
  useInsertionEffect: ha,
  useLayoutEffect: va,
  useMemo: ka,
  useReducer: $l,
  useRef: ma,
  useState: function() {
    return $l(Qt);
  },
  useDebugValue: ko,
  useDeferredValue: function(e) {
    var n = Ce();
    return Sa(n, Y.memoizedState, e);
  },
  useTransition: function() {
    var e = $l(Qt)[0], n = Ce().memoizedState;
    return [e, n];
  },
  useMutableSource: ua,
  useSyncExternalStore: sa,
  useId: Ea,
  unstable_isNewReconciler: !1
}, ld = { readContext: _e, useCallback: wa, useContext: _e, useEffect: wo, useImperativeHandle: ga, useInsertionEffect: ha, useLayoutEffect: va, useMemo: ka, useReducer: Al, useRef: ma, useState: function() {
  return Al(Qt);
}, useDebugValue: ko, useDeferredValue: function(e) {
  var n = Ce();
  return Y === null ? n.memoizedState = e : Sa(n, Y.memoizedState, e);
}, useTransition: function() {
  var e = Al(Qt)[0], n = Ce().memoizedState;
  return [e, n];
}, useMutableSource: ua, useSyncExternalStore: sa, useId: Ea, unstable_isNewReconciler: !1 };
function ze(e, n) {
  if (e && e.defaultProps) {
    n = V({}, n), e = e.defaultProps;
    for (var t in e)
      n[t] === void 0 && (n[t] = e[t]);
    return n;
  }
  return n;
}
function Ei(e, n, t, r) {
  n = e.memoizedState, t = t(r, n), t = t == null ? n : V({}, n, t), e.memoizedState = t, e.lanes === 0 && (e.updateQueue.baseState = t);
}
var sl = { isMounted: function(e) {
  return (e = e._reactInternals) ? jn(e) === e : !1;
}, enqueueSetState: function(e, n, t) {
  e = e._reactInternals;
  var r = oe(), l = cn(e), i = He(r, l);
  i.payload = n, t != null && (i.callback = t), n = sn(e, i, l), n !== null && (je(n, e, l, r), xr(n, e, l));
}, enqueueReplaceState: function(e, n, t) {
  e = e._reactInternals;
  var r = oe(), l = cn(e), i = He(r, l);
  i.tag = 1, i.payload = n, t != null && (i.callback = t), n = sn(e, i, l), n !== null && (je(n, e, l, r), xr(n, e, l));
}, enqueueForceUpdate: function(e, n) {
  e = e._reactInternals;
  var t = oe(), r = cn(e), l = He(t, r);
  l.tag = 2, n != null && (l.callback = n), n = sn(e, l, r), n !== null && (je(n, e, r, t), xr(n, e, r));
} };
function Eu(e, n, t, r, l, i, o) {
  return e = e.stateNode, typeof e.shouldComponentUpdate == "function" ? e.shouldComponentUpdate(r, i, o) : n.prototype && n.prototype.isPureReactComponent ? !Ut(t, r) || !Ut(l, i) : !0;
}
function Na(e, n, t) {
  var r = !1, l = pn, i = n.contextType;
  return typeof i == "object" && i !== null ? i = _e(i) : (l = de(n) ? Nn : le.current, r = n.contextTypes, i = (r = r != null) ? bn(e, l) : pn), n = new n(t, i), e.memoizedState = n.state !== null && n.state !== void 0 ? n.state : null, n.updater = sl, e.stateNode = n, n._reactInternals = e, r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = l, e.__reactInternalMemoizedMaskedChildContext = i), n;
}
function xu(e, n, t, r) {
  e = n.state, typeof n.componentWillReceiveProps == "function" && n.componentWillReceiveProps(t, r), typeof n.UNSAFE_componentWillReceiveProps == "function" && n.UNSAFE_componentWillReceiveProps(t, r), n.state !== e && sl.enqueueReplaceState(n, n.state, null);
}
function xi(e, n, t, r) {
  var l = e.stateNode;
  l.props = t, l.state = e.memoizedState, l.refs = {}, fo(e);
  var i = n.contextType;
  typeof i == "object" && i !== null ? l.context = _e(i) : (i = de(n) ? Nn : le.current, l.context = bn(e, i)), l.state = e.memoizedState, i = n.getDerivedStateFromProps, typeof i == "function" && (Ei(e, n, i, t), l.state = e.memoizedState), typeof n.getDerivedStateFromProps == "function" || typeof l.getSnapshotBeforeUpdate == "function" || typeof l.UNSAFE_componentWillMount != "function" && typeof l.componentWillMount != "function" || (n = l.state, typeof l.componentWillMount == "function" && l.componentWillMount(), typeof l.UNSAFE_componentWillMount == "function" && l.UNSAFE_componentWillMount(), n !== l.state && sl.enqueueReplaceState(l, l.state, null), Qr(e, t, l, r), l.state = e.memoizedState), typeof l.componentDidMount == "function" && (e.flags |= 4194308);
}
function rt(e, n) {
  try {
    var t = "", r = n;
    do
      t += Rc(r), r = r.return;
    while (r);
    var l = t;
  } catch (i) {
    l = `
Error generating stack: ` + i.message + `
` + i.stack;
  }
  return { value: e, source: n, stack: l, digest: null };
}
function Vl(e, n, t) {
  return { value: e, source: null, stack: t ?? null, digest: n ?? null };
}
function _i(e, n) {
  try {
    console.error(n.value);
  } catch (t) {
    setTimeout(function() {
      throw t;
    });
  }
}
var id = typeof WeakMap == "function" ? WeakMap : Map;
function Pa(e, n, t) {
  t = He(-1, t), t.tag = 3, t.payload = { element: null };
  var r = n.value;
  return t.callback = function() {
    Zr || (Zr = !0, Oi = r), _i(e, n);
  }, t;
}
function za(e, n, t) {
  t = He(-1, t), t.tag = 3;
  var r = e.type.getDerivedStateFromError;
  if (typeof r == "function") {
    var l = n.value;
    t.payload = function() {
      return r(l);
    }, t.callback = function() {
      _i(e, n);
    };
  }
  var i = e.stateNode;
  return i !== null && typeof i.componentDidCatch == "function" && (t.callback = function() {
    _i(e, n), typeof r != "function" && (an === null ? an = /* @__PURE__ */ new Set([this]) : an.add(this));
    var o = n.stack;
    this.componentDidCatch(n.value, { componentStack: o !== null ? o : "" });
  }), t;
}
function _u(e, n, t) {
  var r = e.pingCache;
  if (r === null) {
    r = e.pingCache = new id();
    var l = /* @__PURE__ */ new Set();
    r.set(n, l);
  } else
    l = r.get(n), l === void 0 && (l = /* @__PURE__ */ new Set(), r.set(n, l));
  l.has(t) || (l.add(t), e = wd.bind(null, e, n, t), n.then(e, e));
}
function Cu(e) {
  do {
    var n;
    if ((n = e.tag === 13) && (n = e.memoizedState, n = n !== null ? n.dehydrated !== null : !0), n)
      return e;
    e = e.return;
  } while (e !== null);
  return null;
}
function Nu(e, n, t, r, l) {
  return e.mode & 1 ? (e.flags |= 65536, e.lanes = l, e) : (e === n ? e.flags |= 65536 : (e.flags |= 128, t.flags |= 131072, t.flags &= -52805, t.tag === 1 && (t.alternate === null ? t.tag = 17 : (n = He(-1, 1), n.tag = 2, sn(t, n, 1))), t.lanes |= 1), e);
}
var od = Xe.ReactCurrentOwner, ce = !1;
function ie(e, n, t, r) {
  n.child = e === null ? ra(n, null, t, r) : nt(n, e.child, t, r);
}
function Pu(e, n, t, r, l) {
  t = t.render;
  var i = n.ref;
  return Zn(n, l), r = yo(e, n, t, r, i, l), t = go(), e !== null && !ce ? (n.updateQueue = e.updateQueue, n.flags &= -2053, e.lanes &= ~l, Ye(e, n, l)) : (U && t && lo(n), n.flags |= 1, ie(e, n, r, l), n.child);
}
function zu(e, n, t, r, l) {
  if (e === null) {
    var i = t.type;
    return typeof i == "function" && !zo(i) && i.defaultProps === void 0 && t.compare === null && t.defaultProps === void 0 ? (n.tag = 15, n.type = i, Ta(e, n, i, r, l)) : (e = Tr(t.type, null, r, n, n.mode, l), e.ref = n.ref, e.return = n, n.child = e);
  }
  if (i = e.child, !(e.lanes & l)) {
    var o = i.memoizedProps;
    if (t = t.compare, t = t !== null ? t : Ut, t(o, r) && e.ref === n.ref)
      return Ye(e, n, l);
  }
  return n.flags |= 1, e = fn(i, r), e.ref = n.ref, e.return = n, n.child = e;
}
function Ta(e, n, t, r, l) {
  if (e !== null) {
    var i = e.memoizedProps;
    if (Ut(i, r) && e.ref === n.ref)
      if (ce = !1, n.pendingProps = r = i, (e.lanes & l) !== 0)
        e.flags & 131072 && (ce = !0);
      else
        return n.lanes = e.lanes, Ye(e, n, l);
  }
  return Ci(e, n, t, r, l);
}
function La(e, n, t) {
  var r = n.pendingProps, l = r.children, i = e !== null ? e.memoizedState : null;
  if (r.mode === "hidden")
    if (!(n.mode & 1))
      n.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, O(Qn, me), me |= t;
    else {
      if (!(t & 1073741824))
        return e = i !== null ? i.baseLanes | t : t, n.lanes = n.childLanes = 1073741824, n.memoizedState = { baseLanes: e, cachePool: null, transitions: null }, n.updateQueue = null, O(Qn, me), me |= e, null;
      n.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, r = i !== null ? i.baseLanes : t, O(Qn, me), me |= r;
    }
  else
    i !== null ? (r = i.baseLanes | t, n.memoizedState = null) : r = t, O(Qn, me), me |= r;
  return ie(e, n, l, t), n.child;
}
function Ra(e, n) {
  var t = n.ref;
  (e === null && t !== null || e !== null && e.ref !== t) && (n.flags |= 512, n.flags |= 2097152);
}
function Ci(e, n, t, r, l) {
  var i = de(t) ? Nn : le.current;
  return i = bn(n, i), Zn(n, l), t = yo(e, n, t, r, i, l), r = go(), e !== null && !ce ? (n.updateQueue = e.updateQueue, n.flags &= -2053, e.lanes &= ~l, Ye(e, n, l)) : (U && r && lo(n), n.flags |= 1, ie(e, n, t, l), n.child);
}
function Tu(e, n, t, r, l) {
  if (de(t)) {
    var i = !0;
    Ar(n);
  } else
    i = !1;
  if (Zn(n, l), n.stateNode === null)
    Nr(e, n), Na(n, t, r), xi(n, t, r, l), r = !0;
  else if (e === null) {
    var o = n.stateNode, u = n.memoizedProps;
    o.props = u;
    var s = o.context, c = t.contextType;
    typeof c == "object" && c !== null ? c = _e(c) : (c = de(t) ? Nn : le.current, c = bn(n, c));
    var m = t.getDerivedStateFromProps, h = typeof m == "function" || typeof o.getSnapshotBeforeUpdate == "function";
    h || typeof o.UNSAFE_componentWillReceiveProps != "function" && typeof o.componentWillReceiveProps != "function" || (u !== r || s !== c) && xu(n, o, r, c), Je = !1;
    var p = n.memoizedState;
    o.state = p, Qr(n, r, o, l), s = n.memoizedState, u !== r || p !== s || fe.current || Je ? (typeof m == "function" && (Ei(n, t, m, r), s = n.memoizedState), (u = Je || Eu(n, t, u, r, p, s, c)) ? (h || typeof o.UNSAFE_componentWillMount != "function" && typeof o.componentWillMount != "function" || (typeof o.componentWillMount == "function" && o.componentWillMount(), typeof o.UNSAFE_componentWillMount == "function" && o.UNSAFE_componentWillMount()), typeof o.componentDidMount == "function" && (n.flags |= 4194308)) : (typeof o.componentDidMount == "function" && (n.flags |= 4194308), n.memoizedProps = r, n.memoizedState = s), o.props = r, o.state = s, o.context = c, r = u) : (typeof o.componentDidMount == "function" && (n.flags |= 4194308), r = !1);
  } else {
    o = n.stateNode, ia(e, n), u = n.memoizedProps, c = n.type === n.elementType ? u : ze(n.type, u), o.props = c, h = n.pendingProps, p = o.context, s = t.contextType, typeof s == "object" && s !== null ? s = _e(s) : (s = de(t) ? Nn : le.current, s = bn(n, s));
    var g = t.getDerivedStateFromProps;
    (m = typeof g == "function" || typeof o.getSnapshotBeforeUpdate == "function") || typeof o.UNSAFE_componentWillReceiveProps != "function" && typeof o.componentWillReceiveProps != "function" || (u !== h || p !== s) && xu(n, o, r, s), Je = !1, p = n.memoizedState, o.state = p, Qr(n, r, o, l);
    var w = n.memoizedState;
    u !== h || p !== w || fe.current || Je ? (typeof g == "function" && (Ei(n, t, g, r), w = n.memoizedState), (c = Je || Eu(n, t, c, r, p, w, s) || !1) ? (m || typeof o.UNSAFE_componentWillUpdate != "function" && typeof o.componentWillUpdate != "function" || (typeof o.componentWillUpdate == "function" && o.componentWillUpdate(r, w, s), typeof o.UNSAFE_componentWillUpdate == "function" && o.UNSAFE_componentWillUpdate(r, w, s)), typeof o.componentDidUpdate == "function" && (n.flags |= 4), typeof o.getSnapshotBeforeUpdate == "function" && (n.flags |= 1024)) : (typeof o.componentDidUpdate != "function" || u === e.memoizedProps && p === e.memoizedState || (n.flags |= 4), typeof o.getSnapshotBeforeUpdate != "function" || u === e.memoizedProps && p === e.memoizedState || (n.flags |= 1024), n.memoizedProps = r, n.memoizedState = w), o.props = r, o.state = w, o.context = s, r = c) : (typeof o.componentDidUpdate != "function" || u === e.memoizedProps && p === e.memoizedState || (n.flags |= 4), typeof o.getSnapshotBeforeUpdate != "function" || u === e.memoizedProps && p === e.memoizedState || (n.flags |= 1024), r = !1);
  }
  return Ni(e, n, t, r, i, l);
}
function Ni(e, n, t, r, l, i) {
  Ra(e, n);
  var o = (n.flags & 128) !== 0;
  if (!r && !o)
    return l && mu(n, t, !1), Ye(e, n, i);
  r = n.stateNode, od.current = n;
  var u = o && typeof t.getDerivedStateFromError != "function" ? null : r.render();
  return n.flags |= 1, e !== null && o ? (n.child = nt(n, e.child, null, i), n.child = nt(n, null, u, i)) : ie(e, n, u, i), n.memoizedState = r.state, l && mu(n, t, !0), n.child;
}
function ja(e) {
  var n = e.stateNode;
  n.pendingContext ? pu(e, n.pendingContext, n.pendingContext !== n.context) : n.context && pu(e, n.context, !1), po(e, n.containerInfo);
}
function Lu(e, n, t, r, l) {
  return et(), oo(l), n.flags |= 256, ie(e, n, t, r), n.child;
}
var Pi = { dehydrated: null, treeContext: null, retryLane: 0 };
function zi(e) {
  return { baseLanes: e, cachePool: null, transitions: null };
}
function Ma(e, n, t) {
  var r = n.pendingProps, l = $.current, i = !1, o = (n.flags & 128) !== 0, u;
  if ((u = o) || (u = e !== null && e.memoizedState === null ? !1 : (l & 2) !== 0), u ? (i = !0, n.flags &= -129) : (e === null || e.memoizedState !== null) && (l |= 1), O($, l & 1), e === null)
    return ki(n), e = n.memoizedState, e !== null && (e = e.dehydrated, e !== null) ? (n.mode & 1 ? e.data === "$!" ? n.lanes = 8 : n.lanes = 1073741824 : n.lanes = 1, null) : (o = r.children, e = r.fallback, i ? (r = n.mode, i = n.child, o = { mode: "hidden", children: o }, !(r & 1) && i !== null ? (i.childLanes = 0, i.pendingProps = o) : i = fl(o, r, 0, null), e = Cn(e, r, t, null), i.return = n, e.return = n, i.sibling = e, n.child = i, n.child.memoizedState = zi(t), n.memoizedState = Pi, e) : So(n, o));
  if (l = e.memoizedState, l !== null && (u = l.dehydrated, u !== null))
    return ud(e, n, o, r, u, l, t);
  if (i) {
    i = r.fallback, o = n.mode, l = e.child, u = l.sibling;
    var s = { mode: "hidden", children: r.children };
    return !(o & 1) && n.child !== l ? (r = n.child, r.childLanes = 0, r.pendingProps = s, n.deletions = null) : (r = fn(l, s), r.subtreeFlags = l.subtreeFlags & 14680064), u !== null ? i = fn(u, i) : (i = Cn(i, o, t, null), i.flags |= 2), i.return = n, r.return = n, r.sibling = i, n.child = r, r = i, i = n.child, o = e.child.memoizedState, o = o === null ? zi(t) : { baseLanes: o.baseLanes | t, cachePool: null, transitions: o.transitions }, i.memoizedState = o, i.childLanes = e.childLanes & ~t, n.memoizedState = Pi, r;
  }
  return i = e.child, e = i.sibling, r = fn(i, { mode: "visible", children: r.children }), !(n.mode & 1) && (r.lanes = t), r.return = n, r.sibling = null, e !== null && (t = n.deletions, t === null ? (n.deletions = [e], n.flags |= 16) : t.push(e)), n.child = r, n.memoizedState = null, r;
}
function So(e, n) {
  return n = fl({ mode: "visible", children: n }, e.mode, 0, null), n.return = e, e.child = n;
}
function mr(e, n, t, r) {
  return r !== null && oo(r), nt(n, e.child, null, t), e = So(n, n.pendingProps.children), e.flags |= 2, n.memoizedState = null, e;
}
function ud(e, n, t, r, l, i, o) {
  if (t)
    return n.flags & 256 ? (n.flags &= -257, r = Vl(Error(y(422))), mr(e, n, o, r)) : n.memoizedState !== null ? (n.child = e.child, n.flags |= 128, null) : (i = r.fallback, l = n.mode, r = fl({ mode: "visible", children: r.children }, l, 0, null), i = Cn(i, l, o, null), i.flags |= 2, r.return = n, i.return = n, r.sibling = i, n.child = r, n.mode & 1 && nt(n, e.child, null, o), n.child.memoizedState = zi(o), n.memoizedState = Pi, i);
  if (!(n.mode & 1))
    return mr(e, n, o, null);
  if (l.data === "$!") {
    if (r = l.nextSibling && l.nextSibling.dataset, r)
      var u = r.dgst;
    return r = u, i = Error(y(419)), r = Vl(i, r, void 0), mr(e, n, o, r);
  }
  if (u = (o & e.childLanes) !== 0, ce || u) {
    if (r = J, r !== null) {
      switch (o & -o) {
        case 4:
          l = 2;
          break;
        case 16:
          l = 8;
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
          l = 32;
          break;
        case 536870912:
          l = 268435456;
          break;
        default:
          l = 0;
      }
      l = l & (r.suspendedLanes | o) ? 0 : l, l !== 0 && l !== i.retryLane && (i.retryLane = l, Ke(e, l), je(r, e, l, -1));
    }
    return Po(), r = Vl(Error(y(421))), mr(e, n, o, r);
  }
  return l.data === "$?" ? (n.flags |= 128, n.child = e.child, n = kd.bind(null, e), l._reactRetry = n, null) : (e = i.treeContext, he = un(l.nextSibling), ve = n, U = !0, Le = null, e !== null && (ke[Se++] = Ve, ke[Se++] = Be, ke[Se++] = Pn, Ve = e.id, Be = e.overflow, Pn = n), n = So(n, r.children), n.flags |= 4096, n);
}
function Ru(e, n, t) {
  e.lanes |= n;
  var r = e.alternate;
  r !== null && (r.lanes |= n), Si(e.return, n, t);
}
function Bl(e, n, t, r, l) {
  var i = e.memoizedState;
  i === null ? e.memoizedState = { isBackwards: n, rendering: null, renderingStartTime: 0, last: r, tail: t, tailMode: l } : (i.isBackwards = n, i.rendering = null, i.renderingStartTime = 0, i.last = r, i.tail = t, i.tailMode = l);
}
function Oa(e, n, t) {
  var r = n.pendingProps, l = r.revealOrder, i = r.tail;
  if (ie(e, n, r.children, t), r = $.current, r & 2)
    r = r & 1 | 2, n.flags |= 128;
  else {
    if (e !== null && e.flags & 128)
      e:
        for (e = n.child; e !== null; ) {
          if (e.tag === 13)
            e.memoizedState !== null && Ru(e, t, n);
          else if (e.tag === 19)
            Ru(e, t, n);
          else if (e.child !== null) {
            e.child.return = e, e = e.child;
            continue;
          }
          if (e === n)
            break e;
          for (; e.sibling === null; ) {
            if (e.return === null || e.return === n)
              break e;
            e = e.return;
          }
          e.sibling.return = e.return, e = e.sibling;
        }
    r &= 1;
  }
  if (O($, r), !(n.mode & 1))
    n.memoizedState = null;
  else
    switch (l) {
      case "forwards":
        for (t = n.child, l = null; t !== null; )
          e = t.alternate, e !== null && Kr(e) === null && (l = t), t = t.sibling;
        t = l, t === null ? (l = n.child, n.child = null) : (l = t.sibling, t.sibling = null), Bl(n, !1, l, t, i);
        break;
      case "backwards":
        for (t = null, l = n.child, n.child = null; l !== null; ) {
          if (e = l.alternate, e !== null && Kr(e) === null) {
            n.child = l;
            break;
          }
          e = l.sibling, l.sibling = t, t = l, l = e;
        }
        Bl(n, !0, t, null, i);
        break;
      case "together":
        Bl(n, !1, null, null, void 0);
        break;
      default:
        n.memoizedState = null;
    }
  return n.child;
}
function Nr(e, n) {
  !(n.mode & 1) && e !== null && (e.alternate = null, n.alternate = null, n.flags |= 2);
}
function Ye(e, n, t) {
  if (e !== null && (n.dependencies = e.dependencies), Tn |= n.lanes, !(t & n.childLanes))
    return null;
  if (e !== null && n.child !== e.child)
    throw Error(y(153));
  if (n.child !== null) {
    for (e = n.child, t = fn(e, e.pendingProps), n.child = t, t.return = n; e.sibling !== null; )
      e = e.sibling, t = t.sibling = fn(e, e.pendingProps), t.return = n;
    t.sibling = null;
  }
  return n.child;
}
function sd(e, n, t) {
  switch (n.tag) {
    case 3:
      ja(n), et();
      break;
    case 5:
      oa(n);
      break;
    case 1:
      de(n.type) && Ar(n);
      break;
    case 4:
      po(n, n.stateNode.containerInfo);
      break;
    case 10:
      var r = n.type._context, l = n.memoizedProps.value;
      O(Hr, r._currentValue), r._currentValue = l;
      break;
    case 13:
      if (r = n.memoizedState, r !== null)
        return r.dehydrated !== null ? (O($, $.current & 1), n.flags |= 128, null) : t & n.child.childLanes ? Ma(e, n, t) : (O($, $.current & 1), e = Ye(e, n, t), e !== null ? e.sibling : null);
      O($, $.current & 1);
      break;
    case 19:
      if (r = (t & n.childLanes) !== 0, e.flags & 128) {
        if (r)
          return Oa(e, n, t);
        n.flags |= 128;
      }
      if (l = n.memoizedState, l !== null && (l.rendering = null, l.tail = null, l.lastEffect = null), O($, $.current), r)
        break;
      return null;
    case 22:
    case 23:
      return n.lanes = 0, La(e, n, t);
  }
  return Ye(e, n, t);
}
var Da, Ti, Ia, Fa;
Da = function(e, n) {
  for (var t = n.child; t !== null; ) {
    if (t.tag === 5 || t.tag === 6)
      e.appendChild(t.stateNode);
    else if (t.tag !== 4 && t.child !== null) {
      t.child.return = t, t = t.child;
      continue;
    }
    if (t === n)
      break;
    for (; t.sibling === null; ) {
      if (t.return === null || t.return === n)
        return;
      t = t.return;
    }
    t.sibling.return = t.return, t = t.sibling;
  }
};
Ti = function() {
};
Ia = function(e, n, t, r) {
  var l = e.memoizedProps;
  if (l !== r) {
    e = n.stateNode, xn(Ue.current);
    var i = null;
    switch (t) {
      case "input":
        l = Jl(e, l), r = Jl(e, r), i = [];
        break;
      case "select":
        l = V({}, l, { value: void 0 }), r = V({}, r, { value: void 0 }), i = [];
        break;
      case "textarea":
        l = ei(e, l), r = ei(e, r), i = [];
        break;
      default:
        typeof l.onClick != "function" && typeof r.onClick == "function" && (e.onclick = Ur);
    }
    ti(t, r);
    var o;
    t = null;
    for (c in l)
      if (!r.hasOwnProperty(c) && l.hasOwnProperty(c) && l[c] != null)
        if (c === "style") {
          var u = l[c];
          for (o in u)
            u.hasOwnProperty(o) && (t || (t = {}), t[o] = "");
        } else
          c !== "dangerouslySetInnerHTML" && c !== "children" && c !== "suppressContentEditableWarning" && c !== "suppressHydrationWarning" && c !== "autoFocus" && (Rt.hasOwnProperty(c) ? i || (i = []) : (i = i || []).push(c, null));
    for (c in r) {
      var s = r[c];
      if (u = l != null ? l[c] : void 0, r.hasOwnProperty(c) && s !== u && (s != null || u != null))
        if (c === "style")
          if (u) {
            for (o in u)
              !u.hasOwnProperty(o) || s && s.hasOwnProperty(o) || (t || (t = {}), t[o] = "");
            for (o in s)
              s.hasOwnProperty(o) && u[o] !== s[o] && (t || (t = {}), t[o] = s[o]);
          } else
            t || (i || (i = []), i.push(
              c,
              t
            )), t = s;
        else
          c === "dangerouslySetInnerHTML" ? (s = s ? s.__html : void 0, u = u ? u.__html : void 0, s != null && u !== s && (i = i || []).push(c, s)) : c === "children" ? typeof s != "string" && typeof s != "number" || (i = i || []).push(c, "" + s) : c !== "suppressContentEditableWarning" && c !== "suppressHydrationWarning" && (Rt.hasOwnProperty(c) ? (s != null && c === "onScroll" && D("scroll", e), i || u === s || (i = [])) : (i = i || []).push(c, s));
    }
    t && (i = i || []).push("style", t);
    var c = i;
    (n.updateQueue = c) && (n.flags |= 4);
  }
};
Fa = function(e, n, t, r) {
  t !== r && (n.flags |= 4);
};
function vt(e, n) {
  if (!U)
    switch (e.tailMode) {
      case "hidden":
        n = e.tail;
        for (var t = null; n !== null; )
          n.alternate !== null && (t = n), n = n.sibling;
        t === null ? e.tail = null : t.sibling = null;
        break;
      case "collapsed":
        t = e.tail;
        for (var r = null; t !== null; )
          t.alternate !== null && (r = t), t = t.sibling;
        r === null ? n || e.tail === null ? e.tail = null : e.tail.sibling = null : r.sibling = null;
    }
}
function te(e) {
  var n = e.alternate !== null && e.alternate.child === e.child, t = 0, r = 0;
  if (n)
    for (var l = e.child; l !== null; )
      t |= l.lanes | l.childLanes, r |= l.subtreeFlags & 14680064, r |= l.flags & 14680064, l.return = e, l = l.sibling;
  else
    for (l = e.child; l !== null; )
      t |= l.lanes | l.childLanes, r |= l.subtreeFlags, r |= l.flags, l.return = e, l = l.sibling;
  return e.subtreeFlags |= r, e.childLanes = t, n;
}
function ad(e, n, t) {
  var r = n.pendingProps;
  switch (io(n), n.tag) {
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
      return te(n), null;
    case 1:
      return de(n.type) && $r(), te(n), null;
    case 3:
      return r = n.stateNode, tt(), I(fe), I(le), ho(), r.pendingContext && (r.context = r.pendingContext, r.pendingContext = null), (e === null || e.child === null) && (dr(n) ? n.flags |= 4 : e === null || e.memoizedState.isDehydrated && !(n.flags & 256) || (n.flags |= 1024, Le !== null && (Fi(Le), Le = null))), Ti(e, n), te(n), null;
    case 5:
      mo(n);
      var l = xn(Ht.current);
      if (t = n.type, e !== null && n.stateNode != null)
        Ia(e, n, t, r, l), e.ref !== n.ref && (n.flags |= 512, n.flags |= 2097152);
      else {
        if (!r) {
          if (n.stateNode === null)
            throw Error(y(166));
          return te(n), null;
        }
        if (e = xn(Ue.current), dr(n)) {
          r = n.stateNode, t = n.type;
          var i = n.memoizedProps;
          switch (r[Ie] = n, r[Vt] = i, e = (n.mode & 1) !== 0, t) {
            case "dialog":
              D("cancel", r), D("close", r);
              break;
            case "iframe":
            case "object":
            case "embed":
              D("load", r);
              break;
            case "video":
            case "audio":
              for (l = 0; l < St.length; l++)
                D(St[l], r);
              break;
            case "source":
              D("error", r);
              break;
            case "img":
            case "image":
            case "link":
              D(
                "error",
                r
              ), D("load", r);
              break;
            case "details":
              D("toggle", r);
              break;
            case "input":
              Ao(r, i), D("invalid", r);
              break;
            case "select":
              r._wrapperState = { wasMultiple: !!i.multiple }, D("invalid", r);
              break;
            case "textarea":
              Bo(r, i), D("invalid", r);
          }
          ti(t, i), l = null;
          for (var o in i)
            if (i.hasOwnProperty(o)) {
              var u = i[o];
              o === "children" ? typeof u == "string" ? r.textContent !== u && (i.suppressHydrationWarning !== !0 && fr(r.textContent, u, e), l = ["children", u]) : typeof u == "number" && r.textContent !== "" + u && (i.suppressHydrationWarning !== !0 && fr(
                r.textContent,
                u,
                e
              ), l = ["children", "" + u]) : Rt.hasOwnProperty(o) && u != null && o === "onScroll" && D("scroll", r);
            }
          switch (t) {
            case "input":
              rr(r), Vo(r, i, !0);
              break;
            case "textarea":
              rr(r), Ho(r);
              break;
            case "select":
            case "option":
              break;
            default:
              typeof i.onClick == "function" && (r.onclick = Ur);
          }
          r = l, n.updateQueue = r, r !== null && (n.flags |= 4);
        } else {
          o = l.nodeType === 9 ? l : l.ownerDocument, e === "http://www.w3.org/1999/xhtml" && (e = fs(t)), e === "http://www.w3.org/1999/xhtml" ? t === "script" ? (e = o.createElement("div"), e.innerHTML = "<script><\/script>", e = e.removeChild(e.firstChild)) : typeof r.is == "string" ? e = o.createElement(t, { is: r.is }) : (e = o.createElement(t), t === "select" && (o = e, r.multiple ? o.multiple = !0 : r.size && (o.size = r.size))) : e = o.createElementNS(e, t), e[Ie] = n, e[Vt] = r, Da(e, n, !1, !1), n.stateNode = e;
          e: {
            switch (o = ri(t, r), t) {
              case "dialog":
                D("cancel", e), D("close", e), l = r;
                break;
              case "iframe":
              case "object":
              case "embed":
                D("load", e), l = r;
                break;
              case "video":
              case "audio":
                for (l = 0; l < St.length; l++)
                  D(St[l], e);
                l = r;
                break;
              case "source":
                D("error", e), l = r;
                break;
              case "img":
              case "image":
              case "link":
                D(
                  "error",
                  e
                ), D("load", e), l = r;
                break;
              case "details":
                D("toggle", e), l = r;
                break;
              case "input":
                Ao(e, r), l = Jl(e, r), D("invalid", e);
                break;
              case "option":
                l = r;
                break;
              case "select":
                e._wrapperState = { wasMultiple: !!r.multiple }, l = V({}, r, { value: void 0 }), D("invalid", e);
                break;
              case "textarea":
                Bo(e, r), l = ei(e, r), D("invalid", e);
                break;
              default:
                l = r;
            }
            ti(t, l), u = l;
            for (i in u)
              if (u.hasOwnProperty(i)) {
                var s = u[i];
                i === "style" ? ms(e, s) : i === "dangerouslySetInnerHTML" ? (s = s ? s.__html : void 0, s != null && ds(e, s)) : i === "children" ? typeof s == "string" ? (t !== "textarea" || s !== "") && jt(e, s) : typeof s == "number" && jt(e, "" + s) : i !== "suppressContentEditableWarning" && i !== "suppressHydrationWarning" && i !== "autoFocus" && (Rt.hasOwnProperty(i) ? s != null && i === "onScroll" && D("scroll", e) : s != null && Wi(e, i, s, o));
              }
            switch (t) {
              case "input":
                rr(e), Vo(e, r, !1);
                break;
              case "textarea":
                rr(e), Ho(e);
                break;
              case "option":
                r.value != null && e.setAttribute("value", "" + dn(r.value));
                break;
              case "select":
                e.multiple = !!r.multiple, i = r.value, i != null ? Kn(e, !!r.multiple, i, !1) : r.defaultValue != null && Kn(
                  e,
                  !!r.multiple,
                  r.defaultValue,
                  !0
                );
                break;
              default:
                typeof l.onClick == "function" && (e.onclick = Ur);
            }
            switch (t) {
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
          r && (n.flags |= 4);
        }
        n.ref !== null && (n.flags |= 512, n.flags |= 2097152);
      }
      return te(n), null;
    case 6:
      if (e && n.stateNode != null)
        Fa(e, n, e.memoizedProps, r);
      else {
        if (typeof r != "string" && n.stateNode === null)
          throw Error(y(166));
        if (t = xn(Ht.current), xn(Ue.current), dr(n)) {
          if (r = n.stateNode, t = n.memoizedProps, r[Ie] = n, (i = r.nodeValue !== t) && (e = ve, e !== null))
            switch (e.tag) {
              case 3:
                fr(r.nodeValue, t, (e.mode & 1) !== 0);
                break;
              case 5:
                e.memoizedProps.suppressHydrationWarning !== !0 && fr(r.nodeValue, t, (e.mode & 1) !== 0);
            }
          i && (n.flags |= 4);
        } else
          r = (t.nodeType === 9 ? t : t.ownerDocument).createTextNode(r), r[Ie] = n, n.stateNode = r;
      }
      return te(n), null;
    case 13:
      if (I($), r = n.memoizedState, e === null || e.memoizedState !== null && e.memoizedState.dehydrated !== null) {
        if (U && he !== null && n.mode & 1 && !(n.flags & 128))
          na(), et(), n.flags |= 98560, i = !1;
        else if (i = dr(n), r !== null && r.dehydrated !== null) {
          if (e === null) {
            if (!i)
              throw Error(y(318));
            if (i = n.memoizedState, i = i !== null ? i.dehydrated : null, !i)
              throw Error(y(317));
            i[Ie] = n;
          } else
            et(), !(n.flags & 128) && (n.memoizedState = null), n.flags |= 4;
          te(n), i = !1;
        } else
          Le !== null && (Fi(Le), Le = null), i = !0;
        if (!i)
          return n.flags & 65536 ? n : null;
      }
      return n.flags & 128 ? (n.lanes = t, n) : (r = r !== null, r !== (e !== null && e.memoizedState !== null) && r && (n.child.flags |= 8192, n.mode & 1 && (e === null || $.current & 1 ? X === 0 && (X = 3) : Po())), n.updateQueue !== null && (n.flags |= 4), te(n), null);
    case 4:
      return tt(), Ti(e, n), e === null && $t(n.stateNode.containerInfo), te(n), null;
    case 10:
      return ao(n.type._context), te(n), null;
    case 17:
      return de(n.type) && $r(), te(n), null;
    case 19:
      if (I($), i = n.memoizedState, i === null)
        return te(n), null;
      if (r = (n.flags & 128) !== 0, o = i.rendering, o === null)
        if (r)
          vt(i, !1);
        else {
          if (X !== 0 || e !== null && e.flags & 128)
            for (e = n.child; e !== null; ) {
              if (o = Kr(e), o !== null) {
                for (n.flags |= 128, vt(i, !1), r = o.updateQueue, r !== null && (n.updateQueue = r, n.flags |= 4), n.subtreeFlags = 0, r = t, t = n.child; t !== null; )
                  i = t, e = r, i.flags &= 14680066, o = i.alternate, o === null ? (i.childLanes = 0, i.lanes = e, i.child = null, i.subtreeFlags = 0, i.memoizedProps = null, i.memoizedState = null, i.updateQueue = null, i.dependencies = null, i.stateNode = null) : (i.childLanes = o.childLanes, i.lanes = o.lanes, i.child = o.child, i.subtreeFlags = 0, i.deletions = null, i.memoizedProps = o.memoizedProps, i.memoizedState = o.memoizedState, i.updateQueue = o.updateQueue, i.type = o.type, e = o.dependencies, i.dependencies = e === null ? null : { lanes: e.lanes, firstContext: e.firstContext }), t = t.sibling;
                return O($, $.current & 1 | 2), n.child;
              }
              e = e.sibling;
            }
          i.tail !== null && Q() > lt && (n.flags |= 128, r = !0, vt(i, !1), n.lanes = 4194304);
        }
      else {
        if (!r)
          if (e = Kr(o), e !== null) {
            if (n.flags |= 128, r = !0, t = e.updateQueue, t !== null && (n.updateQueue = t, n.flags |= 4), vt(i, !0), i.tail === null && i.tailMode === "hidden" && !o.alternate && !U)
              return te(n), null;
          } else
            2 * Q() - i.renderingStartTime > lt && t !== 1073741824 && (n.flags |= 128, r = !0, vt(i, !1), n.lanes = 4194304);
        i.isBackwards ? (o.sibling = n.child, n.child = o) : (t = i.last, t !== null ? t.sibling = o : n.child = o, i.last = o);
      }
      return i.tail !== null ? (n = i.tail, i.rendering = n, i.tail = n.sibling, i.renderingStartTime = Q(), n.sibling = null, t = $.current, O($, r ? t & 1 | 2 : t & 1), n) : (te(n), null);
    case 22:
    case 23:
      return No(), r = n.memoizedState !== null, e !== null && e.memoizedState !== null !== r && (n.flags |= 8192), r && n.mode & 1 ? me & 1073741824 && (te(n), n.subtreeFlags & 6 && (n.flags |= 8192)) : te(n), null;
    case 24:
      return null;
    case 25:
      return null;
  }
  throw Error(y(156, n.tag));
}
function cd(e, n) {
  switch (io(n), n.tag) {
    case 1:
      return de(n.type) && $r(), e = n.flags, e & 65536 ? (n.flags = e & -65537 | 128, n) : null;
    case 3:
      return tt(), I(fe), I(le), ho(), e = n.flags, e & 65536 && !(e & 128) ? (n.flags = e & -65537 | 128, n) : null;
    case 5:
      return mo(n), null;
    case 13:
      if (I($), e = n.memoizedState, e !== null && e.dehydrated !== null) {
        if (n.alternate === null)
          throw Error(y(340));
        et();
      }
      return e = n.flags, e & 65536 ? (n.flags = e & -65537 | 128, n) : null;
    case 19:
      return I($), null;
    case 4:
      return tt(), null;
    case 10:
      return ao(n.type._context), null;
    case 22:
    case 23:
      return No(), null;
    case 24:
      return null;
    default:
      return null;
  }
}
var hr = !1, re = !1, fd = typeof WeakSet == "function" ? WeakSet : Set, S = null;
function Wn(e, n) {
  var t = e.ref;
  if (t !== null)
    if (typeof t == "function")
      try {
        t(null);
      } catch (r) {
        B(e, n, r);
      }
    else
      t.current = null;
}
function Li(e, n, t) {
  try {
    t();
  } catch (r) {
    B(e, n, r);
  }
}
var ju = !1;
function dd(e, n) {
  if (pi = Dr, e = Bs(), ro(e)) {
    if ("selectionStart" in e)
      var t = { start: e.selectionStart, end: e.selectionEnd };
    else
      e: {
        t = (t = e.ownerDocument) && t.defaultView || window;
        var r = t.getSelection && t.getSelection();
        if (r && r.rangeCount !== 0) {
          t = r.anchorNode;
          var l = r.anchorOffset, i = r.focusNode;
          r = r.focusOffset;
          try {
            t.nodeType, i.nodeType;
          } catch {
            t = null;
            break e;
          }
          var o = 0, u = -1, s = -1, c = 0, m = 0, h = e, p = null;
          n:
            for (; ; ) {
              for (var g; h !== t || l !== 0 && h.nodeType !== 3 || (u = o + l), h !== i || r !== 0 && h.nodeType !== 3 || (s = o + r), h.nodeType === 3 && (o += h.nodeValue.length), (g = h.firstChild) !== null; )
                p = h, h = g;
              for (; ; ) {
                if (h === e)
                  break n;
                if (p === t && ++c === l && (u = o), p === i && ++m === r && (s = o), (g = h.nextSibling) !== null)
                  break;
                h = p, p = h.parentNode;
              }
              h = g;
            }
          t = u === -1 || s === -1 ? null : { start: u, end: s };
        } else
          t = null;
      }
    t = t || { start: 0, end: 0 };
  } else
    t = null;
  for (mi = { focusedElem: e, selectionRange: t }, Dr = !1, S = n; S !== null; )
    if (n = S, e = n.child, (n.subtreeFlags & 1028) !== 0 && e !== null)
      e.return = n, S = e;
    else
      for (; S !== null; ) {
        n = S;
        try {
          var w = n.alternate;
          if (n.flags & 1024)
            switch (n.tag) {
              case 0:
              case 11:
              case 15:
                break;
              case 1:
                if (w !== null) {
                  var k = w.memoizedProps, F = w.memoizedState, f = n.stateNode, a = f.getSnapshotBeforeUpdate(n.elementType === n.type ? k : ze(n.type, k), F);
                  f.__reactInternalSnapshotBeforeUpdate = a;
                }
                break;
              case 3:
                var d = n.stateNode.containerInfo;
                d.nodeType === 1 ? d.textContent = "" : d.nodeType === 9 && d.documentElement && d.removeChild(d.documentElement);
                break;
              case 5:
              case 6:
              case 4:
              case 17:
                break;
              default:
                throw Error(y(163));
            }
        } catch (v) {
          B(n, n.return, v);
        }
        if (e = n.sibling, e !== null) {
          e.return = n.return, S = e;
          break;
        }
        S = n.return;
      }
  return w = ju, ju = !1, w;
}
function zt(e, n, t) {
  var r = n.updateQueue;
  if (r = r !== null ? r.lastEffect : null, r !== null) {
    var l = r = r.next;
    do {
      if ((l.tag & e) === e) {
        var i = l.destroy;
        l.destroy = void 0, i !== void 0 && Li(n, t, i);
      }
      l = l.next;
    } while (l !== r);
  }
}
function al(e, n) {
  if (n = n.updateQueue, n = n !== null ? n.lastEffect : null, n !== null) {
    var t = n = n.next;
    do {
      if ((t.tag & e) === e) {
        var r = t.create;
        t.destroy = r();
      }
      t = t.next;
    } while (t !== n);
  }
}
function Ri(e) {
  var n = e.ref;
  if (n !== null) {
    var t = e.stateNode;
    switch (e.tag) {
      case 5:
        e = t;
        break;
      default:
        e = t;
    }
    typeof n == "function" ? n(e) : n.current = e;
  }
}
function Ua(e) {
  var n = e.alternate;
  n !== null && (e.alternate = null, Ua(n)), e.child = null, e.deletions = null, e.sibling = null, e.tag === 5 && (n = e.stateNode, n !== null && (delete n[Ie], delete n[Vt], delete n[yi], delete n[Xf], delete n[Gf])), e.stateNode = null, e.return = null, e.dependencies = null, e.memoizedProps = null, e.memoizedState = null, e.pendingProps = null, e.stateNode = null, e.updateQueue = null;
}
function $a(e) {
  return e.tag === 5 || e.tag === 3 || e.tag === 4;
}
function Mu(e) {
  e:
    for (; ; ) {
      for (; e.sibling === null; ) {
        if (e.return === null || $a(e.return))
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
function ji(e, n, t) {
  var r = e.tag;
  if (r === 5 || r === 6)
    e = e.stateNode, n ? t.nodeType === 8 ? t.parentNode.insertBefore(e, n) : t.insertBefore(e, n) : (t.nodeType === 8 ? (n = t.parentNode, n.insertBefore(e, t)) : (n = t, n.appendChild(e)), t = t._reactRootContainer, t != null || n.onclick !== null || (n.onclick = Ur));
  else if (r !== 4 && (e = e.child, e !== null))
    for (ji(e, n, t), e = e.sibling; e !== null; )
      ji(e, n, t), e = e.sibling;
}
function Mi(e, n, t) {
  var r = e.tag;
  if (r === 5 || r === 6)
    e = e.stateNode, n ? t.insertBefore(e, n) : t.appendChild(e);
  else if (r !== 4 && (e = e.child, e !== null))
    for (Mi(e, n, t), e = e.sibling; e !== null; )
      Mi(e, n, t), e = e.sibling;
}
var q = null, Te = !1;
function Ge(e, n, t) {
  for (t = t.child; t !== null; )
    Aa(e, n, t), t = t.sibling;
}
function Aa(e, n, t) {
  if (Fe && typeof Fe.onCommitFiberUnmount == "function")
    try {
      Fe.onCommitFiberUnmount(nl, t);
    } catch {
    }
  switch (t.tag) {
    case 5:
      re || Wn(t, n);
    case 6:
      var r = q, l = Te;
      q = null, Ge(e, n, t), q = r, Te = l, q !== null && (Te ? (e = q, t = t.stateNode, e.nodeType === 8 ? e.parentNode.removeChild(t) : e.removeChild(t)) : q.removeChild(t.stateNode));
      break;
    case 18:
      q !== null && (Te ? (e = q, t = t.stateNode, e.nodeType === 8 ? Dl(e.parentNode, t) : e.nodeType === 1 && Dl(e, t), It(e)) : Dl(q, t.stateNode));
      break;
    case 4:
      r = q, l = Te, q = t.stateNode.containerInfo, Te = !0, Ge(e, n, t), q = r, Te = l;
      break;
    case 0:
    case 11:
    case 14:
    case 15:
      if (!re && (r = t.updateQueue, r !== null && (r = r.lastEffect, r !== null))) {
        l = r = r.next;
        do {
          var i = l, o = i.destroy;
          i = i.tag, o !== void 0 && (i & 2 || i & 4) && Li(t, n, o), l = l.next;
        } while (l !== r);
      }
      Ge(e, n, t);
      break;
    case 1:
      if (!re && (Wn(t, n), r = t.stateNode, typeof r.componentWillUnmount == "function"))
        try {
          r.props = t.memoizedProps, r.state = t.memoizedState, r.componentWillUnmount();
        } catch (u) {
          B(t, n, u);
        }
      Ge(e, n, t);
      break;
    case 21:
      Ge(e, n, t);
      break;
    case 22:
      t.mode & 1 ? (re = (r = re) || t.memoizedState !== null, Ge(e, n, t), re = r) : Ge(e, n, t);
      break;
    default:
      Ge(e, n, t);
  }
}
function Ou(e) {
  var n = e.updateQueue;
  if (n !== null) {
    e.updateQueue = null;
    var t = e.stateNode;
    t === null && (t = e.stateNode = new fd()), n.forEach(function(r) {
      var l = Sd.bind(null, e, r);
      t.has(r) || (t.add(r), r.then(l, l));
    });
  }
}
function Pe(e, n) {
  var t = n.deletions;
  if (t !== null)
    for (var r = 0; r < t.length; r++) {
      var l = t[r];
      try {
        var i = e, o = n, u = o;
        e:
          for (; u !== null; ) {
            switch (u.tag) {
              case 5:
                q = u.stateNode, Te = !1;
                break e;
              case 3:
                q = u.stateNode.containerInfo, Te = !0;
                break e;
              case 4:
                q = u.stateNode.containerInfo, Te = !0;
                break e;
            }
            u = u.return;
          }
        if (q === null)
          throw Error(y(160));
        Aa(i, o, l), q = null, Te = !1;
        var s = l.alternate;
        s !== null && (s.return = null), l.return = null;
      } catch (c) {
        B(l, n, c);
      }
    }
  if (n.subtreeFlags & 12854)
    for (n = n.child; n !== null; )
      Va(n, e), n = n.sibling;
}
function Va(e, n) {
  var t = e.alternate, r = e.flags;
  switch (e.tag) {
    case 0:
    case 11:
    case 14:
    case 15:
      if (Pe(n, e), Oe(e), r & 4) {
        try {
          zt(3, e, e.return), al(3, e);
        } catch (k) {
          B(e, e.return, k);
        }
        try {
          zt(5, e, e.return);
        } catch (k) {
          B(e, e.return, k);
        }
      }
      break;
    case 1:
      Pe(n, e), Oe(e), r & 512 && t !== null && Wn(t, t.return);
      break;
    case 5:
      if (Pe(n, e), Oe(e), r & 512 && t !== null && Wn(t, t.return), e.flags & 32) {
        var l = e.stateNode;
        try {
          jt(l, "");
        } catch (k) {
          B(e, e.return, k);
        }
      }
      if (r & 4 && (l = e.stateNode, l != null)) {
        var i = e.memoizedProps, o = t !== null ? t.memoizedProps : i, u = e.type, s = e.updateQueue;
        if (e.updateQueue = null, s !== null)
          try {
            u === "input" && i.type === "radio" && i.name != null && as(l, i), ri(u, o);
            var c = ri(u, i);
            for (o = 0; o < s.length; o += 2) {
              var m = s[o], h = s[o + 1];
              m === "style" ? ms(l, h) : m === "dangerouslySetInnerHTML" ? ds(l, h) : m === "children" ? jt(l, h) : Wi(l, m, h, c);
            }
            switch (u) {
              case "input":
                ql(l, i);
                break;
              case "textarea":
                cs(l, i);
                break;
              case "select":
                var p = l._wrapperState.wasMultiple;
                l._wrapperState.wasMultiple = !!i.multiple;
                var g = i.value;
                g != null ? Kn(l, !!i.multiple, g, !1) : p !== !!i.multiple && (i.defaultValue != null ? Kn(
                  l,
                  !!i.multiple,
                  i.defaultValue,
                  !0
                ) : Kn(l, !!i.multiple, i.multiple ? [] : "", !1));
            }
            l[Vt] = i;
          } catch (k) {
            B(e, e.return, k);
          }
      }
      break;
    case 6:
      if (Pe(n, e), Oe(e), r & 4) {
        if (e.stateNode === null)
          throw Error(y(162));
        l = e.stateNode, i = e.memoizedProps;
        try {
          l.nodeValue = i;
        } catch (k) {
          B(e, e.return, k);
        }
      }
      break;
    case 3:
      if (Pe(n, e), Oe(e), r & 4 && t !== null && t.memoizedState.isDehydrated)
        try {
          It(n.containerInfo);
        } catch (k) {
          B(e, e.return, k);
        }
      break;
    case 4:
      Pe(n, e), Oe(e);
      break;
    case 13:
      Pe(n, e), Oe(e), l = e.child, l.flags & 8192 && (i = l.memoizedState !== null, l.stateNode.isHidden = i, !i || l.alternate !== null && l.alternate.memoizedState !== null || (_o = Q())), r & 4 && Ou(e);
      break;
    case 22:
      if (m = t !== null && t.memoizedState !== null, e.mode & 1 ? (re = (c = re) || m, Pe(n, e), re = c) : Pe(n, e), Oe(e), r & 8192) {
        if (c = e.memoizedState !== null, (e.stateNode.isHidden = c) && !m && e.mode & 1)
          for (S = e, m = e.child; m !== null; ) {
            for (h = S = m; S !== null; ) {
              switch (p = S, g = p.child, p.tag) {
                case 0:
                case 11:
                case 14:
                case 15:
                  zt(4, p, p.return);
                  break;
                case 1:
                  Wn(p, p.return);
                  var w = p.stateNode;
                  if (typeof w.componentWillUnmount == "function") {
                    r = p, t = p.return;
                    try {
                      n = r, w.props = n.memoizedProps, w.state = n.memoizedState, w.componentWillUnmount();
                    } catch (k) {
                      B(r, t, k);
                    }
                  }
                  break;
                case 5:
                  Wn(p, p.return);
                  break;
                case 22:
                  if (p.memoizedState !== null) {
                    Iu(h);
                    continue;
                  }
              }
              g !== null ? (g.return = p, S = g) : Iu(h);
            }
            m = m.sibling;
          }
        e:
          for (m = null, h = e; ; ) {
            if (h.tag === 5) {
              if (m === null) {
                m = h;
                try {
                  l = h.stateNode, c ? (i = l.style, typeof i.setProperty == "function" ? i.setProperty("display", "none", "important") : i.display = "none") : (u = h.stateNode, s = h.memoizedProps.style, o = s != null && s.hasOwnProperty("display") ? s.display : null, u.style.display = ps("display", o));
                } catch (k) {
                  B(e, e.return, k);
                }
              }
            } else if (h.tag === 6) {
              if (m === null)
                try {
                  h.stateNode.nodeValue = c ? "" : h.memoizedProps;
                } catch (k) {
                  B(e, e.return, k);
                }
            } else if ((h.tag !== 22 && h.tag !== 23 || h.memoizedState === null || h === e) && h.child !== null) {
              h.child.return = h, h = h.child;
              continue;
            }
            if (h === e)
              break e;
            for (; h.sibling === null; ) {
              if (h.return === null || h.return === e)
                break e;
              m === h && (m = null), h = h.return;
            }
            m === h && (m = null), h.sibling.return = h.return, h = h.sibling;
          }
      }
      break;
    case 19:
      Pe(n, e), Oe(e), r & 4 && Ou(e);
      break;
    case 21:
      break;
    default:
      Pe(
        n,
        e
      ), Oe(e);
  }
}
function Oe(e) {
  var n = e.flags;
  if (n & 2) {
    try {
      e: {
        for (var t = e.return; t !== null; ) {
          if ($a(t)) {
            var r = t;
            break e;
          }
          t = t.return;
        }
        throw Error(y(160));
      }
      switch (r.tag) {
        case 5:
          var l = r.stateNode;
          r.flags & 32 && (jt(l, ""), r.flags &= -33);
          var i = Mu(e);
          Mi(e, i, l);
          break;
        case 3:
        case 4:
          var o = r.stateNode.containerInfo, u = Mu(e);
          ji(e, u, o);
          break;
        default:
          throw Error(y(161));
      }
    } catch (s) {
      B(e, e.return, s);
    }
    e.flags &= -3;
  }
  n & 4096 && (e.flags &= -4097);
}
function pd(e, n, t) {
  S = e, Ba(e);
}
function Ba(e, n, t) {
  for (var r = (e.mode & 1) !== 0; S !== null; ) {
    var l = S, i = l.child;
    if (l.tag === 22 && r) {
      var o = l.memoizedState !== null || hr;
      if (!o) {
        var u = l.alternate, s = u !== null && u.memoizedState !== null || re;
        u = hr;
        var c = re;
        if (hr = o, (re = s) && !c)
          for (S = l; S !== null; )
            o = S, s = o.child, o.tag === 22 && o.memoizedState !== null ? Fu(l) : s !== null ? (s.return = o, S = s) : Fu(l);
        for (; i !== null; )
          S = i, Ba(i), i = i.sibling;
        S = l, hr = u, re = c;
      }
      Du(e);
    } else
      l.subtreeFlags & 8772 && i !== null ? (i.return = l, S = i) : Du(e);
  }
}
function Du(e) {
  for (; S !== null; ) {
    var n = S;
    if (n.flags & 8772) {
      var t = n.alternate;
      try {
        if (n.flags & 8772)
          switch (n.tag) {
            case 0:
            case 11:
            case 15:
              re || al(5, n);
              break;
            case 1:
              var r = n.stateNode;
              if (n.flags & 4 && !re)
                if (t === null)
                  r.componentDidMount();
                else {
                  var l = n.elementType === n.type ? t.memoizedProps : ze(n.type, t.memoizedProps);
                  r.componentDidUpdate(l, t.memoizedState, r.__reactInternalSnapshotBeforeUpdate);
                }
              var i = n.updateQueue;
              i !== null && wu(n, i, r);
              break;
            case 3:
              var o = n.updateQueue;
              if (o !== null) {
                if (t = null, n.child !== null)
                  switch (n.child.tag) {
                    case 5:
                      t = n.child.stateNode;
                      break;
                    case 1:
                      t = n.child.stateNode;
                  }
                wu(n, o, t);
              }
              break;
            case 5:
              var u = n.stateNode;
              if (t === null && n.flags & 4) {
                t = u;
                var s = n.memoizedProps;
                switch (n.type) {
                  case "button":
                  case "input":
                  case "select":
                  case "textarea":
                    s.autoFocus && t.focus();
                    break;
                  case "img":
                    s.src && (t.src = s.src);
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
              if (n.memoizedState === null) {
                var c = n.alternate;
                if (c !== null) {
                  var m = c.memoizedState;
                  if (m !== null) {
                    var h = m.dehydrated;
                    h !== null && It(h);
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
              throw Error(y(163));
          }
        re || n.flags & 512 && Ri(n);
      } catch (p) {
        B(n, n.return, p);
      }
    }
    if (n === e) {
      S = null;
      break;
    }
    if (t = n.sibling, t !== null) {
      t.return = n.return, S = t;
      break;
    }
    S = n.return;
  }
}
function Iu(e) {
  for (; S !== null; ) {
    var n = S;
    if (n === e) {
      S = null;
      break;
    }
    var t = n.sibling;
    if (t !== null) {
      t.return = n.return, S = t;
      break;
    }
    S = n.return;
  }
}
function Fu(e) {
  for (; S !== null; ) {
    var n = S;
    try {
      switch (n.tag) {
        case 0:
        case 11:
        case 15:
          var t = n.return;
          try {
            al(4, n);
          } catch (s) {
            B(n, t, s);
          }
          break;
        case 1:
          var r = n.stateNode;
          if (typeof r.componentDidMount == "function") {
            var l = n.return;
            try {
              r.componentDidMount();
            } catch (s) {
              B(n, l, s);
            }
          }
          var i = n.return;
          try {
            Ri(n);
          } catch (s) {
            B(n, i, s);
          }
          break;
        case 5:
          var o = n.return;
          try {
            Ri(n);
          } catch (s) {
            B(n, o, s);
          }
      }
    } catch (s) {
      B(n, n.return, s);
    }
    if (n === e) {
      S = null;
      break;
    }
    var u = n.sibling;
    if (u !== null) {
      u.return = n.return, S = u;
      break;
    }
    S = n.return;
  }
}
var md = Math.ceil, Gr = Xe.ReactCurrentDispatcher, Eo = Xe.ReactCurrentOwner, xe = Xe.ReactCurrentBatchConfig, j = 0, J = null, K = null, b = 0, me = 0, Qn = hn(0), X = 0, Yt = null, Tn = 0, cl = 0, xo = 0, Tt = null, ae = null, _o = 0, lt = 1 / 0, $e = null, Zr = !1, Oi = null, an = null, vr = !1, tn = null, Jr = 0, Lt = 0, Di = null, Pr = -1, zr = 0;
function oe() {
  return j & 6 ? Q() : Pr !== -1 ? Pr : Pr = Q();
}
function cn(e) {
  return e.mode & 1 ? j & 2 && b !== 0 ? b & -b : Jf.transition !== null ? (zr === 0 && (zr = Ns()), zr) : (e = M, e !== 0 || (e = window.event, e = e === void 0 ? 16 : Ms(e.type)), e) : 1;
}
function je(e, n, t, r) {
  if (50 < Lt)
    throw Lt = 0, Di = null, Error(y(185));
  Gt(e, t, r), (!(j & 2) || e !== J) && (e === J && (!(j & 2) && (cl |= t), X === 4 && be(e, b)), pe(e, r), t === 1 && j === 0 && !(n.mode & 1) && (lt = Q() + 500, ol && vn()));
}
function pe(e, n) {
  var t = e.callbackNode;
  Zc(e, n);
  var r = Or(e, e === J ? b : 0);
  if (r === 0)
    t !== null && Ko(t), e.callbackNode = null, e.callbackPriority = 0;
  else if (n = r & -r, e.callbackPriority !== n) {
    if (t != null && Ko(t), n === 1)
      e.tag === 0 ? Zf(Uu.bind(null, e)) : qs(Uu.bind(null, e)), Kf(function() {
        !(j & 6) && vn();
      }), t = null;
    else {
      switch (Ps(r)) {
        case 1:
          t = Gi;
          break;
        case 4:
          t = _s;
          break;
        case 16:
          t = Mr;
          break;
        case 536870912:
          t = Cs;
          break;
        default:
          t = Mr;
      }
      t = Za(t, Ha.bind(null, e));
    }
    e.callbackPriority = n, e.callbackNode = t;
  }
}
function Ha(e, n) {
  if (Pr = -1, zr = 0, j & 6)
    throw Error(y(327));
  var t = e.callbackNode;
  if (Jn() && e.callbackNode !== t)
    return null;
  var r = Or(e, e === J ? b : 0);
  if (r === 0)
    return null;
  if (r & 30 || r & e.expiredLanes || n)
    n = qr(e, r);
  else {
    n = r;
    var l = j;
    j |= 2;
    var i = Qa();
    (J !== e || b !== n) && ($e = null, lt = Q() + 500, _n(e, n));
    do
      try {
        yd();
        break;
      } catch (u) {
        Wa(e, u);
      }
    while (1);
    so(), Gr.current = i, j = l, K !== null ? n = 0 : (J = null, b = 0, n = X);
  }
  if (n !== 0) {
    if (n === 2 && (l = si(e), l !== 0 && (r = l, n = Ii(e, l))), n === 1)
      throw t = Yt, _n(e, 0), be(e, r), pe(e, Q()), t;
    if (n === 6)
      be(e, r);
    else {
      if (l = e.current.alternate, !(r & 30) && !hd(l) && (n = qr(e, r), n === 2 && (i = si(e), i !== 0 && (r = i, n = Ii(e, i))), n === 1))
        throw t = Yt, _n(e, 0), be(e, r), pe(e, Q()), t;
      switch (e.finishedWork = l, e.finishedLanes = r, n) {
        case 0:
        case 1:
          throw Error(y(345));
        case 2:
          kn(e, ae, $e);
          break;
        case 3:
          if (be(e, r), (r & 130023424) === r && (n = _o + 500 - Q(), 10 < n)) {
            if (Or(e, 0) !== 0)
              break;
            if (l = e.suspendedLanes, (l & r) !== r) {
              oe(), e.pingedLanes |= e.suspendedLanes & l;
              break;
            }
            e.timeoutHandle = vi(kn.bind(null, e, ae, $e), n);
            break;
          }
          kn(e, ae, $e);
          break;
        case 4:
          if (be(e, r), (r & 4194240) === r)
            break;
          for (n = e.eventTimes, l = -1; 0 < r; ) {
            var o = 31 - Re(r);
            i = 1 << o, o = n[o], o > l && (l = o), r &= ~i;
          }
          if (r = l, r = Q() - r, r = (120 > r ? 120 : 480 > r ? 480 : 1080 > r ? 1080 : 1920 > r ? 1920 : 3e3 > r ? 3e3 : 4320 > r ? 4320 : 1960 * md(r / 1960)) - r, 10 < r) {
            e.timeoutHandle = vi(kn.bind(null, e, ae, $e), r);
            break;
          }
          kn(e, ae, $e);
          break;
        case 5:
          kn(e, ae, $e);
          break;
        default:
          throw Error(y(329));
      }
    }
  }
  return pe(e, Q()), e.callbackNode === t ? Ha.bind(null, e) : null;
}
function Ii(e, n) {
  var t = Tt;
  return e.current.memoizedState.isDehydrated && (_n(e, n).flags |= 256), e = qr(e, n), e !== 2 && (n = ae, ae = t, n !== null && Fi(n)), e;
}
function Fi(e) {
  ae === null ? ae = e : ae.push.apply(ae, e);
}
function hd(e) {
  for (var n = e; ; ) {
    if (n.flags & 16384) {
      var t = n.updateQueue;
      if (t !== null && (t = t.stores, t !== null))
        for (var r = 0; r < t.length; r++) {
          var l = t[r], i = l.getSnapshot;
          l = l.value;
          try {
            if (!Me(i(), l))
              return !1;
          } catch {
            return !1;
          }
        }
    }
    if (t = n.child, n.subtreeFlags & 16384 && t !== null)
      t.return = n, n = t;
    else {
      if (n === e)
        break;
      for (; n.sibling === null; ) {
        if (n.return === null || n.return === e)
          return !0;
        n = n.return;
      }
      n.sibling.return = n.return, n = n.sibling;
    }
  }
  return !0;
}
function be(e, n) {
  for (n &= ~xo, n &= ~cl, e.suspendedLanes |= n, e.pingedLanes &= ~n, e = e.expirationTimes; 0 < n; ) {
    var t = 31 - Re(n), r = 1 << t;
    e[t] = -1, n &= ~r;
  }
}
function Uu(e) {
  if (j & 6)
    throw Error(y(327));
  Jn();
  var n = Or(e, 0);
  if (!(n & 1))
    return pe(e, Q()), null;
  var t = qr(e, n);
  if (e.tag !== 0 && t === 2) {
    var r = si(e);
    r !== 0 && (n = r, t = Ii(e, r));
  }
  if (t === 1)
    throw t = Yt, _n(e, 0), be(e, n), pe(e, Q()), t;
  if (t === 6)
    throw Error(y(345));
  return e.finishedWork = e.current.alternate, e.finishedLanes = n, kn(e, ae, $e), pe(e, Q()), null;
}
function Co(e, n) {
  var t = j;
  j |= 1;
  try {
    return e(n);
  } finally {
    j = t, j === 0 && (lt = Q() + 500, ol && vn());
  }
}
function Ln(e) {
  tn !== null && tn.tag === 0 && !(j & 6) && Jn();
  var n = j;
  j |= 1;
  var t = xe.transition, r = M;
  try {
    if (xe.transition = null, M = 1, e)
      return e();
  } finally {
    M = r, xe.transition = t, j = n, !(j & 6) && vn();
  }
}
function No() {
  me = Qn.current, I(Qn);
}
function _n(e, n) {
  e.finishedWork = null, e.finishedLanes = 0;
  var t = e.timeoutHandle;
  if (t !== -1 && (e.timeoutHandle = -1, Qf(t)), K !== null)
    for (t = K.return; t !== null; ) {
      var r = t;
      switch (io(r), r.tag) {
        case 1:
          r = r.type.childContextTypes, r != null && $r();
          break;
        case 3:
          tt(), I(fe), I(le), ho();
          break;
        case 5:
          mo(r);
          break;
        case 4:
          tt();
          break;
        case 13:
          I($);
          break;
        case 19:
          I($);
          break;
        case 10:
          ao(r.type._context);
          break;
        case 22:
        case 23:
          No();
      }
      t = t.return;
    }
  if (J = e, K = e = fn(e.current, null), b = me = n, X = 0, Yt = null, xo = cl = Tn = 0, ae = Tt = null, En !== null) {
    for (n = 0; n < En.length; n++)
      if (t = En[n], r = t.interleaved, r !== null) {
        t.interleaved = null;
        var l = r.next, i = t.pending;
        if (i !== null) {
          var o = i.next;
          i.next = l, r.next = o;
        }
        t.pending = r;
      }
    En = null;
  }
  return e;
}
function Wa(e, n) {
  do {
    var t = K;
    try {
      if (so(), _r.current = Xr, Yr) {
        for (var r = A.memoizedState; r !== null; ) {
          var l = r.queue;
          l !== null && (l.pending = null), r = r.next;
        }
        Yr = !1;
      }
      if (zn = 0, Z = Y = A = null, Pt = !1, Wt = 0, Eo.current = null, t === null || t.return === null) {
        X = 1, Yt = n, K = null;
        break;
      }
      e: {
        var i = e, o = t.return, u = t, s = n;
        if (n = b, u.flags |= 32768, s !== null && typeof s == "object" && typeof s.then == "function") {
          var c = s, m = u, h = m.tag;
          if (!(m.mode & 1) && (h === 0 || h === 11 || h === 15)) {
            var p = m.alternate;
            p ? (m.updateQueue = p.updateQueue, m.memoizedState = p.memoizedState, m.lanes = p.lanes) : (m.updateQueue = null, m.memoizedState = null);
          }
          var g = Cu(o);
          if (g !== null) {
            g.flags &= -257, Nu(g, o, u, i, n), g.mode & 1 && _u(i, c, n), n = g, s = c;
            var w = n.updateQueue;
            if (w === null) {
              var k = /* @__PURE__ */ new Set();
              k.add(s), n.updateQueue = k;
            } else
              w.add(s);
            break e;
          } else {
            if (!(n & 1)) {
              _u(i, c, n), Po();
              break e;
            }
            s = Error(y(426));
          }
        } else if (U && u.mode & 1) {
          var F = Cu(o);
          if (F !== null) {
            !(F.flags & 65536) && (F.flags |= 256), Nu(F, o, u, i, n), oo(rt(s, u));
            break e;
          }
        }
        i = s = rt(s, u), X !== 4 && (X = 2), Tt === null ? Tt = [i] : Tt.push(i), i = o;
        do {
          switch (i.tag) {
            case 3:
              i.flags |= 65536, n &= -n, i.lanes |= n;
              var f = Pa(i, s, n);
              gu(i, f);
              break e;
            case 1:
              u = s;
              var a = i.type, d = i.stateNode;
              if (!(i.flags & 128) && (typeof a.getDerivedStateFromError == "function" || d !== null && typeof d.componentDidCatch == "function" && (an === null || !an.has(d)))) {
                i.flags |= 65536, n &= -n, i.lanes |= n;
                var v = za(i, u, n);
                gu(i, v);
                break e;
              }
          }
          i = i.return;
        } while (i !== null);
      }
      Ya(t);
    } catch (E) {
      n = E, K === t && t !== null && (K = t = t.return);
      continue;
    }
    break;
  } while (1);
}
function Qa() {
  var e = Gr.current;
  return Gr.current = Xr, e === null ? Xr : e;
}
function Po() {
  (X === 0 || X === 3 || X === 2) && (X = 4), J === null || !(Tn & 268435455) && !(cl & 268435455) || be(J, b);
}
function qr(e, n) {
  var t = j;
  j |= 2;
  var r = Qa();
  (J !== e || b !== n) && ($e = null, _n(e, n));
  do
    try {
      vd();
      break;
    } catch (l) {
      Wa(e, l);
    }
  while (1);
  if (so(), j = t, Gr.current = r, K !== null)
    throw Error(y(261));
  return J = null, b = 0, X;
}
function vd() {
  for (; K !== null; )
    Ka(K);
}
function yd() {
  for (; K !== null && !Vc(); )
    Ka(K);
}
function Ka(e) {
  var n = Ga(e.alternate, e, me);
  e.memoizedProps = e.pendingProps, n === null ? Ya(e) : K = n, Eo.current = null;
}
function Ya(e) {
  var n = e;
  do {
    var t = n.alternate;
    if (e = n.return, n.flags & 32768) {
      if (t = cd(t, n), t !== null) {
        t.flags &= 32767, K = t;
        return;
      }
      if (e !== null)
        e.flags |= 32768, e.subtreeFlags = 0, e.deletions = null;
      else {
        X = 6, K = null;
        return;
      }
    } else if (t = ad(t, n, me), t !== null) {
      K = t;
      return;
    }
    if (n = n.sibling, n !== null) {
      K = n;
      return;
    }
    K = n = e;
  } while (n !== null);
  X === 0 && (X = 5);
}
function kn(e, n, t) {
  var r = M, l = xe.transition;
  try {
    xe.transition = null, M = 1, gd(e, n, t, r);
  } finally {
    xe.transition = l, M = r;
  }
  return null;
}
function gd(e, n, t, r) {
  do
    Jn();
  while (tn !== null);
  if (j & 6)
    throw Error(y(327));
  t = e.finishedWork;
  var l = e.finishedLanes;
  if (t === null)
    return null;
  if (e.finishedWork = null, e.finishedLanes = 0, t === e.current)
    throw Error(y(177));
  e.callbackNode = null, e.callbackPriority = 0;
  var i = t.lanes | t.childLanes;
  if (Jc(e, i), e === J && (K = J = null, b = 0), !(t.subtreeFlags & 2064) && !(t.flags & 2064) || vr || (vr = !0, Za(Mr, function() {
    return Jn(), null;
  })), i = (t.flags & 15990) !== 0, t.subtreeFlags & 15990 || i) {
    i = xe.transition, xe.transition = null;
    var o = M;
    M = 1;
    var u = j;
    j |= 4, Eo.current = null, dd(e, t), Va(t, e), Uf(mi), Dr = !!pi, mi = pi = null, e.current = t, pd(t), Bc(), j = u, M = o, xe.transition = i;
  } else
    e.current = t;
  if (vr && (vr = !1, tn = e, Jr = l), i = e.pendingLanes, i === 0 && (an = null), Qc(t.stateNode), pe(e, Q()), n !== null)
    for (r = e.onRecoverableError, t = 0; t < n.length; t++)
      l = n[t], r(l.value, { componentStack: l.stack, digest: l.digest });
  if (Zr)
    throw Zr = !1, e = Oi, Oi = null, e;
  return Jr & 1 && e.tag !== 0 && Jn(), i = e.pendingLanes, i & 1 ? e === Di ? Lt++ : (Lt = 0, Di = e) : Lt = 0, vn(), null;
}
function Jn() {
  if (tn !== null) {
    var e = Ps(Jr), n = xe.transition, t = M;
    try {
      if (xe.transition = null, M = 16 > e ? 16 : e, tn === null)
        var r = !1;
      else {
        if (e = tn, tn = null, Jr = 0, j & 6)
          throw Error(y(331));
        var l = j;
        for (j |= 4, S = e.current; S !== null; ) {
          var i = S, o = i.child;
          if (S.flags & 16) {
            var u = i.deletions;
            if (u !== null) {
              for (var s = 0; s < u.length; s++) {
                var c = u[s];
                for (S = c; S !== null; ) {
                  var m = S;
                  switch (m.tag) {
                    case 0:
                    case 11:
                    case 15:
                      zt(8, m, i);
                  }
                  var h = m.child;
                  if (h !== null)
                    h.return = m, S = h;
                  else
                    for (; S !== null; ) {
                      m = S;
                      var p = m.sibling, g = m.return;
                      if (Ua(m), m === c) {
                        S = null;
                        break;
                      }
                      if (p !== null) {
                        p.return = g, S = p;
                        break;
                      }
                      S = g;
                    }
                }
              }
              var w = i.alternate;
              if (w !== null) {
                var k = w.child;
                if (k !== null) {
                  w.child = null;
                  do {
                    var F = k.sibling;
                    k.sibling = null, k = F;
                  } while (k !== null);
                }
              }
              S = i;
            }
          }
          if (i.subtreeFlags & 2064 && o !== null)
            o.return = i, S = o;
          else
            e:
              for (; S !== null; ) {
                if (i = S, i.flags & 2048)
                  switch (i.tag) {
                    case 0:
                    case 11:
                    case 15:
                      zt(9, i, i.return);
                  }
                var f = i.sibling;
                if (f !== null) {
                  f.return = i.return, S = f;
                  break e;
                }
                S = i.return;
              }
        }
        var a = e.current;
        for (S = a; S !== null; ) {
          o = S;
          var d = o.child;
          if (o.subtreeFlags & 2064 && d !== null)
            d.return = o, S = d;
          else
            e:
              for (o = a; S !== null; ) {
                if (u = S, u.flags & 2048)
                  try {
                    switch (u.tag) {
                      case 0:
                      case 11:
                      case 15:
                        al(9, u);
                    }
                  } catch (E) {
                    B(u, u.return, E);
                  }
                if (u === o) {
                  S = null;
                  break e;
                }
                var v = u.sibling;
                if (v !== null) {
                  v.return = u.return, S = v;
                  break e;
                }
                S = u.return;
              }
        }
        if (j = l, vn(), Fe && typeof Fe.onPostCommitFiberRoot == "function")
          try {
            Fe.onPostCommitFiberRoot(nl, e);
          } catch {
          }
        r = !0;
      }
      return r;
    } finally {
      M = t, xe.transition = n;
    }
  }
  return !1;
}
function $u(e, n, t) {
  n = rt(t, n), n = Pa(e, n, 1), e = sn(e, n, 1), n = oe(), e !== null && (Gt(e, 1, n), pe(e, n));
}
function B(e, n, t) {
  if (e.tag === 3)
    $u(e, e, t);
  else
    for (; n !== null; ) {
      if (n.tag === 3) {
        $u(n, e, t);
        break;
      } else if (n.tag === 1) {
        var r = n.stateNode;
        if (typeof n.type.getDerivedStateFromError == "function" || typeof r.componentDidCatch == "function" && (an === null || !an.has(r))) {
          e = rt(t, e), e = za(n, e, 1), n = sn(n, e, 1), e = oe(), n !== null && (Gt(n, 1, e), pe(n, e));
          break;
        }
      }
      n = n.return;
    }
}
function wd(e, n, t) {
  var r = e.pingCache;
  r !== null && r.delete(n), n = oe(), e.pingedLanes |= e.suspendedLanes & t, J === e && (b & t) === t && (X === 4 || X === 3 && (b & 130023424) === b && 500 > Q() - _o ? _n(e, 0) : xo |= t), pe(e, n);
}
function Xa(e, n) {
  n === 0 && (e.mode & 1 ? (n = or, or <<= 1, !(or & 130023424) && (or = 4194304)) : n = 1);
  var t = oe();
  e = Ke(e, n), e !== null && (Gt(e, n, t), pe(e, t));
}
function kd(e) {
  var n = e.memoizedState, t = 0;
  n !== null && (t = n.retryLane), Xa(e, t);
}
function Sd(e, n) {
  var t = 0;
  switch (e.tag) {
    case 13:
      var r = e.stateNode, l = e.memoizedState;
      l !== null && (t = l.retryLane);
      break;
    case 19:
      r = e.stateNode;
      break;
    default:
      throw Error(y(314));
  }
  r !== null && r.delete(n), Xa(e, t);
}
var Ga;
Ga = function(e, n, t) {
  if (e !== null)
    if (e.memoizedProps !== n.pendingProps || fe.current)
      ce = !0;
    else {
      if (!(e.lanes & t) && !(n.flags & 128))
        return ce = !1, sd(e, n, t);
      ce = !!(e.flags & 131072);
    }
  else
    ce = !1, U && n.flags & 1048576 && bs(n, Br, n.index);
  switch (n.lanes = 0, n.tag) {
    case 2:
      var r = n.type;
      Nr(e, n), e = n.pendingProps;
      var l = bn(n, le.current);
      Zn(n, t), l = yo(null, n, r, e, l, t);
      var i = go();
      return n.flags |= 1, typeof l == "object" && l !== null && typeof l.render == "function" && l.$$typeof === void 0 ? (n.tag = 1, n.memoizedState = null, n.updateQueue = null, de(r) ? (i = !0, Ar(n)) : i = !1, n.memoizedState = l.state !== null && l.state !== void 0 ? l.state : null, fo(n), l.updater = sl, n.stateNode = l, l._reactInternals = n, xi(n, r, e, t), n = Ni(null, n, r, !0, i, t)) : (n.tag = 0, U && i && lo(n), ie(null, n, l, t), n = n.child), n;
    case 16:
      r = n.elementType;
      e: {
        switch (Nr(e, n), e = n.pendingProps, l = r._init, r = l(r._payload), n.type = r, l = n.tag = xd(r), e = ze(r, e), l) {
          case 0:
            n = Ci(null, n, r, e, t);
            break e;
          case 1:
            n = Tu(null, n, r, e, t);
            break e;
          case 11:
            n = Pu(null, n, r, e, t);
            break e;
          case 14:
            n = zu(null, n, r, ze(r.type, e), t);
            break e;
        }
        throw Error(y(
          306,
          r,
          ""
        ));
      }
      return n;
    case 0:
      return r = n.type, l = n.pendingProps, l = n.elementType === r ? l : ze(r, l), Ci(e, n, r, l, t);
    case 1:
      return r = n.type, l = n.pendingProps, l = n.elementType === r ? l : ze(r, l), Tu(e, n, r, l, t);
    case 3:
      e: {
        if (ja(n), e === null)
          throw Error(y(387));
        r = n.pendingProps, i = n.memoizedState, l = i.element, ia(e, n), Qr(n, r, null, t);
        var o = n.memoizedState;
        if (r = o.element, i.isDehydrated)
          if (i = { element: r, isDehydrated: !1, cache: o.cache, pendingSuspenseBoundaries: o.pendingSuspenseBoundaries, transitions: o.transitions }, n.updateQueue.baseState = i, n.memoizedState = i, n.flags & 256) {
            l = rt(Error(y(423)), n), n = Lu(e, n, r, t, l);
            break e;
          } else if (r !== l) {
            l = rt(Error(y(424)), n), n = Lu(e, n, r, t, l);
            break e;
          } else
            for (he = un(n.stateNode.containerInfo.firstChild), ve = n, U = !0, Le = null, t = ra(n, null, r, t), n.child = t; t; )
              t.flags = t.flags & -3 | 4096, t = t.sibling;
        else {
          if (et(), r === l) {
            n = Ye(e, n, t);
            break e;
          }
          ie(e, n, r, t);
        }
        n = n.child;
      }
      return n;
    case 5:
      return oa(n), e === null && ki(n), r = n.type, l = n.pendingProps, i = e !== null ? e.memoizedProps : null, o = l.children, hi(r, l) ? o = null : i !== null && hi(r, i) && (n.flags |= 32), Ra(e, n), ie(e, n, o, t), n.child;
    case 6:
      return e === null && ki(n), null;
    case 13:
      return Ma(e, n, t);
    case 4:
      return po(n, n.stateNode.containerInfo), r = n.pendingProps, e === null ? n.child = nt(n, null, r, t) : ie(e, n, r, t), n.child;
    case 11:
      return r = n.type, l = n.pendingProps, l = n.elementType === r ? l : ze(r, l), Pu(e, n, r, l, t);
    case 7:
      return ie(e, n, n.pendingProps, t), n.child;
    case 8:
      return ie(e, n, n.pendingProps.children, t), n.child;
    case 12:
      return ie(e, n, n.pendingProps.children, t), n.child;
    case 10:
      e: {
        if (r = n.type._context, l = n.pendingProps, i = n.memoizedProps, o = l.value, O(Hr, r._currentValue), r._currentValue = o, i !== null)
          if (Me(i.value, o)) {
            if (i.children === l.children && !fe.current) {
              n = Ye(e, n, t);
              break e;
            }
          } else
            for (i = n.child, i !== null && (i.return = n); i !== null; ) {
              var u = i.dependencies;
              if (u !== null) {
                o = i.child;
                for (var s = u.firstContext; s !== null; ) {
                  if (s.context === r) {
                    if (i.tag === 1) {
                      s = He(-1, t & -t), s.tag = 2;
                      var c = i.updateQueue;
                      if (c !== null) {
                        c = c.shared;
                        var m = c.pending;
                        m === null ? s.next = s : (s.next = m.next, m.next = s), c.pending = s;
                      }
                    }
                    i.lanes |= t, s = i.alternate, s !== null && (s.lanes |= t), Si(
                      i.return,
                      t,
                      n
                    ), u.lanes |= t;
                    break;
                  }
                  s = s.next;
                }
              } else if (i.tag === 10)
                o = i.type === n.type ? null : i.child;
              else if (i.tag === 18) {
                if (o = i.return, o === null)
                  throw Error(y(341));
                o.lanes |= t, u = o.alternate, u !== null && (u.lanes |= t), Si(o, t, n), o = i.sibling;
              } else
                o = i.child;
              if (o !== null)
                o.return = i;
              else
                for (o = i; o !== null; ) {
                  if (o === n) {
                    o = null;
                    break;
                  }
                  if (i = o.sibling, i !== null) {
                    i.return = o.return, o = i;
                    break;
                  }
                  o = o.return;
                }
              i = o;
            }
        ie(e, n, l.children, t), n = n.child;
      }
      return n;
    case 9:
      return l = n.type, r = n.pendingProps.children, Zn(n, t), l = _e(l), r = r(l), n.flags |= 1, ie(e, n, r, t), n.child;
    case 14:
      return r = n.type, l = ze(r, n.pendingProps), l = ze(r.type, l), zu(e, n, r, l, t);
    case 15:
      return Ta(e, n, n.type, n.pendingProps, t);
    case 17:
      return r = n.type, l = n.pendingProps, l = n.elementType === r ? l : ze(r, l), Nr(e, n), n.tag = 1, de(r) ? (e = !0, Ar(n)) : e = !1, Zn(n, t), Na(n, r, l), xi(n, r, l, t), Ni(null, n, r, !0, e, t);
    case 19:
      return Oa(e, n, t);
    case 22:
      return La(e, n, t);
  }
  throw Error(y(156, n.tag));
};
function Za(e, n) {
  return xs(e, n);
}
function Ed(e, n, t, r) {
  this.tag = e, this.key = t, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.ref = null, this.pendingProps = n, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = r, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
}
function Ee(e, n, t, r) {
  return new Ed(e, n, t, r);
}
function zo(e) {
  return e = e.prototype, !(!e || !e.isReactComponent);
}
function xd(e) {
  if (typeof e == "function")
    return zo(e) ? 1 : 0;
  if (e != null) {
    if (e = e.$$typeof, e === Ki)
      return 11;
    if (e === Yi)
      return 14;
  }
  return 2;
}
function fn(e, n) {
  var t = e.alternate;
  return t === null ? (t = Ee(e.tag, n, e.key, e.mode), t.elementType = e.elementType, t.type = e.type, t.stateNode = e.stateNode, t.alternate = e, e.alternate = t) : (t.pendingProps = n, t.type = e.type, t.flags = 0, t.subtreeFlags = 0, t.deletions = null), t.flags = e.flags & 14680064, t.childLanes = e.childLanes, t.lanes = e.lanes, t.child = e.child, t.memoizedProps = e.memoizedProps, t.memoizedState = e.memoizedState, t.updateQueue = e.updateQueue, n = e.dependencies, t.dependencies = n === null ? null : { lanes: n.lanes, firstContext: n.firstContext }, t.sibling = e.sibling, t.index = e.index, t.ref = e.ref, t;
}
function Tr(e, n, t, r, l, i) {
  var o = 2;
  if (r = e, typeof e == "function")
    zo(e) && (o = 1);
  else if (typeof e == "string")
    o = 5;
  else
    e:
      switch (e) {
        case Dn:
          return Cn(t.children, l, i, n);
        case Qi:
          o = 8, l |= 8;
          break;
        case Yl:
          return e = Ee(12, t, n, l | 2), e.elementType = Yl, e.lanes = i, e;
        case Xl:
          return e = Ee(13, t, n, l), e.elementType = Xl, e.lanes = i, e;
        case Gl:
          return e = Ee(19, t, n, l), e.elementType = Gl, e.lanes = i, e;
        case os:
          return fl(t, l, i, n);
        default:
          if (typeof e == "object" && e !== null)
            switch (e.$$typeof) {
              case ls:
                o = 10;
                break e;
              case is:
                o = 9;
                break e;
              case Ki:
                o = 11;
                break e;
              case Yi:
                o = 14;
                break e;
              case Ze:
                o = 16, r = null;
                break e;
            }
          throw Error(y(130, e == null ? e : typeof e, ""));
      }
  return n = Ee(o, t, n, l), n.elementType = e, n.type = r, n.lanes = i, n;
}
function Cn(e, n, t, r) {
  return e = Ee(7, e, r, n), e.lanes = t, e;
}
function fl(e, n, t, r) {
  return e = Ee(22, e, r, n), e.elementType = os, e.lanes = t, e.stateNode = { isHidden: !1 }, e;
}
function Hl(e, n, t) {
  return e = Ee(6, e, null, n), e.lanes = t, e;
}
function Wl(e, n, t) {
  return n = Ee(4, e.children !== null ? e.children : [], e.key, n), n.lanes = t, n.stateNode = { containerInfo: e.containerInfo, pendingChildren: null, implementation: e.implementation }, n;
}
function _d(e, n, t, r, l) {
  this.tag = n, this.containerInfo = e, this.finishedWork = this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.pendingContext = this.context = null, this.callbackPriority = 0, this.eventTimes = _l(0), this.expirationTimes = _l(-1), this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = _l(0), this.identifierPrefix = r, this.onRecoverableError = l, this.mutableSourceEagerHydrationData = null;
}
function To(e, n, t, r, l, i, o, u, s) {
  return e = new _d(e, n, t, u, s), n === 1 ? (n = 1, i === !0 && (n |= 8)) : n = 0, i = Ee(3, null, null, n), e.current = i, i.stateNode = e, i.memoizedState = { element: r, isDehydrated: t, cache: null, transitions: null, pendingSuspenseBoundaries: null }, fo(i), e;
}
function Cd(e, n, t) {
  var r = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
  return { $$typeof: On, key: r == null ? null : "" + r, children: e, containerInfo: n, implementation: t };
}
function Ja(e) {
  if (!e)
    return pn;
  e = e._reactInternals;
  e: {
    if (jn(e) !== e || e.tag !== 1)
      throw Error(y(170));
    var n = e;
    do {
      switch (n.tag) {
        case 3:
          n = n.stateNode.context;
          break e;
        case 1:
          if (de(n.type)) {
            n = n.stateNode.__reactInternalMemoizedMergedChildContext;
            break e;
          }
      }
      n = n.return;
    } while (n !== null);
    throw Error(y(171));
  }
  if (e.tag === 1) {
    var t = e.type;
    if (de(t))
      return Js(e, t, n);
  }
  return n;
}
function qa(e, n, t, r, l, i, o, u, s) {
  return e = To(t, r, !0, e, l, i, o, u, s), e.context = Ja(null), t = e.current, r = oe(), l = cn(t), i = He(r, l), i.callback = n ?? null, sn(t, i, l), e.current.lanes = l, Gt(e, l, r), pe(e, r), e;
}
function dl(e, n, t, r) {
  var l = n.current, i = oe(), o = cn(l);
  return t = Ja(t), n.context === null ? n.context = t : n.pendingContext = t, n = He(i, o), n.payload = { element: e }, r = r === void 0 ? null : r, r !== null && (n.callback = r), e = sn(l, n, o), e !== null && (je(e, l, o, i), xr(e, l, o)), o;
}
function br(e) {
  if (e = e.current, !e.child)
    return null;
  switch (e.child.tag) {
    case 5:
      return e.child.stateNode;
    default:
      return e.child.stateNode;
  }
}
function Au(e, n) {
  if (e = e.memoizedState, e !== null && e.dehydrated !== null) {
    var t = e.retryLane;
    e.retryLane = t !== 0 && t < n ? t : n;
  }
}
function Lo(e, n) {
  Au(e, n), (e = e.alternate) && Au(e, n);
}
function Nd() {
  return null;
}
var ba = typeof reportError == "function" ? reportError : function(e) {
  console.error(e);
};
function Ro(e) {
  this._internalRoot = e;
}
pl.prototype.render = Ro.prototype.render = function(e) {
  var n = this._internalRoot;
  if (n === null)
    throw Error(y(409));
  dl(e, n, null, null);
};
pl.prototype.unmount = Ro.prototype.unmount = function() {
  var e = this._internalRoot;
  if (e !== null) {
    this._internalRoot = null;
    var n = e.containerInfo;
    Ln(function() {
      dl(null, e, null, null);
    }), n[Qe] = null;
  }
};
function pl(e) {
  this._internalRoot = e;
}
pl.prototype.unstable_scheduleHydration = function(e) {
  if (e) {
    var n = Ls();
    e = { blockedOn: null, target: e, priority: n };
    for (var t = 0; t < qe.length && n !== 0 && n < qe[t].priority; t++)
      ;
    qe.splice(t, 0, e), t === 0 && js(e);
  }
};
function jo(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11);
}
function ml(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11 && (e.nodeType !== 8 || e.nodeValue !== " react-mount-point-unstable "));
}
function Vu() {
}
function Pd(e, n, t, r, l) {
  if (l) {
    if (typeof r == "function") {
      var i = r;
      r = function() {
        var c = br(o);
        i.call(c);
      };
    }
    var o = qa(n, r, e, 0, null, !1, !1, "", Vu);
    return e._reactRootContainer = o, e[Qe] = o.current, $t(e.nodeType === 8 ? e.parentNode : e), Ln(), o;
  }
  for (; l = e.lastChild; )
    e.removeChild(l);
  if (typeof r == "function") {
    var u = r;
    r = function() {
      var c = br(s);
      u.call(c);
    };
  }
  var s = To(e, 0, !1, null, null, !1, !1, "", Vu);
  return e._reactRootContainer = s, e[Qe] = s.current, $t(e.nodeType === 8 ? e.parentNode : e), Ln(function() {
    dl(n, s, t, r);
  }), s;
}
function hl(e, n, t, r, l) {
  var i = t._reactRootContainer;
  if (i) {
    var o = i;
    if (typeof l == "function") {
      var u = l;
      l = function() {
        var s = br(o);
        u.call(s);
      };
    }
    dl(n, o, e, l);
  } else
    o = Pd(t, n, e, l, r);
  return br(o);
}
zs = function(e) {
  switch (e.tag) {
    case 3:
      var n = e.stateNode;
      if (n.current.memoizedState.isDehydrated) {
        var t = kt(n.pendingLanes);
        t !== 0 && (Zi(n, t | 1), pe(n, Q()), !(j & 6) && (lt = Q() + 500, vn()));
      }
      break;
    case 13:
      Ln(function() {
        var r = Ke(e, 1);
        if (r !== null) {
          var l = oe();
          je(r, e, 1, l);
        }
      }), Lo(e, 1);
  }
};
Ji = function(e) {
  if (e.tag === 13) {
    var n = Ke(e, 134217728);
    if (n !== null) {
      var t = oe();
      je(n, e, 134217728, t);
    }
    Lo(e, 134217728);
  }
};
Ts = function(e) {
  if (e.tag === 13) {
    var n = cn(e), t = Ke(e, n);
    if (t !== null) {
      var r = oe();
      je(t, e, n, r);
    }
    Lo(e, n);
  }
};
Ls = function() {
  return M;
};
Rs = function(e, n) {
  var t = M;
  try {
    return M = e, n();
  } finally {
    M = t;
  }
};
ii = function(e, n, t) {
  switch (n) {
    case "input":
      if (ql(e, t), n = t.name, t.type === "radio" && n != null) {
        for (t = e; t.parentNode; )
          t = t.parentNode;
        for (t = t.querySelectorAll("input[name=" + JSON.stringify("" + n) + '][type="radio"]'), n = 0; n < t.length; n++) {
          var r = t[n];
          if (r !== e && r.form === e.form) {
            var l = il(r);
            if (!l)
              throw Error(y(90));
            ss(r), ql(r, l);
          }
        }
      }
      break;
    case "textarea":
      cs(e, t);
      break;
    case "select":
      n = t.value, n != null && Kn(e, !!t.multiple, n, !1);
  }
};
ys = Co;
gs = Ln;
var zd = { usingClientEntryPoint: !1, Events: [Jt, $n, il, hs, vs, Co] }, yt = { findFiberByHostInstance: Sn, bundleType: 0, version: "18.3.1", rendererPackageName: "react-dom" }, Td = { bundleType: yt.bundleType, version: yt.version, rendererPackageName: yt.rendererPackageName, rendererConfig: yt.rendererConfig, overrideHookState: null, overrideHookStateDeletePath: null, overrideHookStateRenamePath: null, overrideProps: null, overridePropsDeletePath: null, overridePropsRenamePath: null, setErrorHandler: null, setSuspenseHandler: null, scheduleUpdate: null, currentDispatcherRef: Xe.ReactCurrentDispatcher, findHostInstanceByFiber: function(e) {
  return e = Ss(e), e === null ? null : e.stateNode;
}, findFiberByHostInstance: yt.findFiberByHostInstance || Nd, findHostInstancesForRefresh: null, scheduleRefresh: null, scheduleRoot: null, setRefreshHandler: null, getCurrentFiber: null, reconcilerVersion: "18.3.1-next-f1338f8080-20240426" };
if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u") {
  var yr = __REACT_DEVTOOLS_GLOBAL_HOOK__;
  if (!yr.isDisabled && yr.supportsFiber)
    try {
      nl = yr.inject(Td), Fe = yr;
    } catch {
    }
}
ge.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = zd;
ge.createPortal = function(e, n) {
  var t = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
  if (!jo(n))
    throw Error(y(200));
  return Cd(e, n, null, t);
};
ge.createRoot = function(e, n) {
  if (!jo(e))
    throw Error(y(299));
  var t = !1, r = "", l = ba;
  return n != null && (n.unstable_strictMode === !0 && (t = !0), n.identifierPrefix !== void 0 && (r = n.identifierPrefix), n.onRecoverableError !== void 0 && (l = n.onRecoverableError)), n = To(e, 1, !1, null, null, t, !1, r, l), e[Qe] = n.current, $t(e.nodeType === 8 ? e.parentNode : e), new Ro(n);
};
ge.findDOMNode = function(e) {
  if (e == null)
    return null;
  if (e.nodeType === 1)
    return e;
  var n = e._reactInternals;
  if (n === void 0)
    throw typeof e.render == "function" ? Error(y(188)) : (e = Object.keys(e).join(","), Error(y(268, e)));
  return e = Ss(n), e = e === null ? null : e.stateNode, e;
};
ge.flushSync = function(e) {
  return Ln(e);
};
ge.hydrate = function(e, n, t) {
  if (!ml(n))
    throw Error(y(200));
  return hl(null, e, n, !0, t);
};
ge.hydrateRoot = function(e, n, t) {
  if (!jo(e))
    throw Error(y(405));
  var r = t != null && t.hydratedSources || null, l = !1, i = "", o = ba;
  if (t != null && (t.unstable_strictMode === !0 && (l = !0), t.identifierPrefix !== void 0 && (i = t.identifierPrefix), t.onRecoverableError !== void 0 && (o = t.onRecoverableError)), n = qa(n, null, e, 1, t ?? null, l, !1, i, o), e[Qe] = n.current, $t(e), r)
    for (e = 0; e < r.length; e++)
      t = r[e], l = t._getVersion, l = l(t._source), n.mutableSourceEagerHydrationData == null ? n.mutableSourceEagerHydrationData = [t, l] : n.mutableSourceEagerHydrationData.push(
        t,
        l
      );
  return new pl(n);
};
ge.render = function(e, n, t) {
  if (!ml(n))
    throw Error(y(200));
  return hl(null, e, n, !1, t);
};
ge.unmountComponentAtNode = function(e) {
  if (!ml(e))
    throw Error(y(40));
  return e._reactRootContainer ? (Ln(function() {
    hl(null, null, e, !1, function() {
      e._reactRootContainer = null, e[Qe] = null;
    });
  }), !0) : !1;
};
ge.unstable_batchedUpdates = Co;
ge.unstable_renderSubtreeIntoContainer = function(e, n, t, r) {
  if (!ml(t))
    throw Error(y(200));
  if (e == null || e._reactInternals === void 0)
    throw Error(y(38));
  return hl(e, n, t, !1, r);
};
ge.version = "18.3.1-next-f1338f8080-20240426";
function ec() {
  if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function"))
    try {
      __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(ec);
    } catch (e) {
      console.error(e);
    }
}
ec(), es.exports = ge;
var Ld = es.exports, Bu = Ld;
Ql.createRoot = Bu.createRoot, Ql.hydrateRoot = Bu.hydrateRoot;
const Rd = () => /* @__PURE__ */ T.jsx("div", { style: { padding: "16px", marginBottom: "24px", textAlign: "center" }, children: /* @__PURE__ */ T.jsx("h1", { children: "Meraki Integration Control" }) }), jd = (e) => e.startsWith("GS") ? "Switches" : e.startsWith("GR") ? "Access Points" : e.startsWith("MT") ? "Sensors" : e.startsWith("MS") ? "Switches" : e.startsWith("MV") ? "Cameras" : e.startsWith("MX") ? "Routers" : e.startsWith("MR") ? "Access Points" : "Other", Md = ({ deviceType: e, devices: n }) => {
  const t = {
    padding: "12px",
    marginBottom: "12px",
    borderRadius: "var(--ha-card-border-radius, 4px)",
    backgroundColor: "var(--secondary-background-color)",
    textAlign: "center"
  }, r = n.filter((l) => l.status === "online").length;
  switch (e) {
    case "Cameras":
    case "Switches":
    case "Access Points":
    case "Sensors":
      return /* @__PURE__ */ T.jsxs("div", { style: t, children: [
        /* @__PURE__ */ T.jsxs("strong", { children: [
          r,
          " / ",
          n.length
        ] }),
        " ",
        e,
        " Online"
      ] });
    case "Routers":
      const l = n.some((i) => i.status === "online");
      return /* @__PURE__ */ T.jsxs("div", { style: t, children: [
        "Gateway Status: ",
        /* @__PURE__ */ T.jsx("strong", { children: l ? "Online" : "Offline" })
      ] });
    default:
      return null;
  }
}, Od = ({ devices: e }) => {
  if (!e || e.length === 0)
    return /* @__PURE__ */ T.jsx("p", { children: "No devices found in this network." });
  const n = e.reduce((t, r) => {
    const l = jd(r.model);
    return t[l] || (t[l] = []), t[l].push(r), t;
  }, {});
  return /* @__PURE__ */ T.jsx("div", { className: "device-list", style: { display: "flex", flexDirection: "column", gap: "16px" }, children: Object.entries(n).map(([t, r]) => /* @__PURE__ */ T.jsxs("div", { className: "device-group", children: [
    /* @__PURE__ */ T.jsx(Md, { deviceType: t, devices: r }),
    r.map((l) => /* @__PURE__ */ T.jsxs("div", { className: "device-item", style: { marginBottom: "8px" }, children: [
      /* @__PURE__ */ T.jsx("p", { style: { margin: 0 }, children: /* @__PURE__ */ T.jsx(
        "strong",
        {
          onClick: () => l.entity_id && window.dispatchEvent(
            new CustomEvent("hass-more-info", {
              bubbles: !0,
              composed: !0,
              detail: { entityId: l.entity_id }
            })
          ),
          style: {
            cursor: l.entity_id ? "pointer" : "default",
            color: l.entity_id ? "var(--primary-color)" : void 0
          },
          title: l.entity_id || "",
          children: l.name || "Unnamed Device"
        }
      ) }),
      /* @__PURE__ */ T.jsxs("p", { style: { margin: 0, fontSize: "var(--secondary-text-size)" }, children: [
        "Model: ",
        l.model,
        " | Status: ",
        l.status
      ] }),
      /* @__PURE__ */ T.jsxs("p", { style: { margin: 0, fontSize: "var(--secondary-text-size)" }, children: [
        l.lanIp && `IP: ${l.lanIp} | `,
        l.mac && `MAC: ${l.mac}`
      ] })
    ] }, l.serial))
  ] }, t)) });
}, Dd = ({ data: e, hass: n }) => {
  const [t, r] = en.useState(null), l = (m) => {
    r(t === m ? null : m);
  }, { networks: i, devices: o, enabled_networks: u, config_entry_id: s } = e;
  if (!i || i.length === 0)
    return /* @__PURE__ */ T.jsx("p", { children: "No networks found." });
  const c = async (m, h) => {
    const p = h ? [...u, m] : u.filter((g) => g !== m);
    try {
      await n.connection.sendMessagePromise({
        type: "meraki_ha/update_enabled_networks",
        config_entry_id: s,
        enabled_networks: p
      });
    } catch (g) {
      console.error("Error updating enabled networks:", g);
    }
  };
  return /* @__PURE__ */ T.jsx("div", { style: { display: "flex", flexDirection: "column", gap: "16px" }, children: i.map((m) => {
    const h = t === m.id;
    return /* @__PURE__ */ T.jsxs("ha-card", { children: [
      /* @__PURE__ */ T.jsxs(
        "div",
        {
          className: "card-header",
          onClick: () => l(m.id),
          style: { display: "flex", alignItems: "center", cursor: "pointer", padding: "16px" },
          children: [
            /* @__PURE__ */ T.jsxs("span", { children: [
              "[Network] ",
              m.name
            ] }),
            /* @__PURE__ */ T.jsx("ha-icon", { style: { marginLeft: "8px" }, icon: h ? "mdi:chevron-up" : "mdi:chevron-down" }),
            /* @__PURE__ */ T.jsx("div", { style: { marginLeft: "auto" }, children: /* @__PURE__ */ T.jsx(
              "ha-switch",
              {
                checked: u == null || u.includes(m.id),
                onchange: (p) => c(m.id, p.target.checked)
              }
            ) })
          ]
        }
      ),
      h && /* @__PURE__ */ T.jsx("div", { className: "card-content", children: /* @__PURE__ */ T.jsx(
        Od,
        {
          devices: o.filter((p) => p.networkId === m.id)
        }
      ) })
    ] }, m.id);
  }) });
}, Id = () => /* @__PURE__ */ T.jsx("div", { className: "card-content", children: /* @__PURE__ */ T.jsx("p", { children: "Integration-specific events will be displayed here." }) }), Fd = ({ hass: e, config_entry_id: n }) => {
  const [t, r] = en.useState(null), [l, i] = en.useState(!0), [o, u] = en.useState(null);
  return en.useEffect(() => {
    if (!e || !e.connection) {
      u("Home Assistant connection object not found."), i(!1);
      return;
    }
    (async () => {
      try {
        const c = await e.connection.sendMessagePromise({
          type: "meraki_ha/get_config",
          config_entry_id: n
        });
        r(c);
      } catch (c) {
        console.error("Error fetching Meraki data:", c), u(`Failed to fetch Meraki data: ${c.message || "Unknown error"}`);
      } finally {
        i(!1);
      }
    })();
  }, [e, n]), /* @__PURE__ */ T.jsxs("div", { children: [
    /* @__PURE__ */ T.jsx(Rd, {}),
    l && /* @__PURE__ */ T.jsx("p", { children: "Loading..." }),
    o && /* @__PURE__ */ T.jsxs("p", { children: [
      "Error: ",
      o
    ] }),
    !l && !o && t && /* @__PURE__ */ T.jsxs(T.Fragment, { children: [
      /* @__PURE__ */ T.jsx(Dd, { data: t, hass: e }),
      /* @__PURE__ */ T.jsx("ha-card", { header: "Event Log", children: /* @__PURE__ */ T.jsx(Id, {}) })
    ] })
  ] });
};
class Ud extends HTMLElement {
  connectedCallback() {
    const n = this.attachShadow({ mode: "open" }), t = document.createElement("div");
    t.id = "root", n.appendChild(t);
    const r = this.hass, l = this.panel.config.config_entry_id;
    Ql.createRoot(t).render(
      /* @__PURE__ */ T.jsx(gc.StrictMode, { children: /* @__PURE__ */ T.jsx(Fd, { hass: r, config_entry_id: l }) })
    );
  }
}
customElements.get("meraki-panel") || customElements.define("meraki-panel", Ud);
