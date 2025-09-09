function ic(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var Ku = { exports: {} }, nl = {}, Yu = { exports: {} }, L = {};
/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Gt = Symbol.for("react.element"), oc = Symbol.for("react.portal"), uc = Symbol.for("react.fragment"), sc = Symbol.for("react.strict_mode"), ac = Symbol.for("react.profiler"), cc = Symbol.for("react.provider"), fc = Symbol.for("react.context"), dc = Symbol.for("react.forward_ref"), pc = Symbol.for("react.suspense"), mc = Symbol.for("react.memo"), hc = Symbol.for("react.lazy"), Oo = Symbol.iterator;
function vc(e) {
  return e === null || typeof e != "object" ? null : (e = Oo && e[Oo] || e["@@iterator"], typeof e == "function" ? e : null);
}
var Xu = { isMounted: function() {
  return !1;
}, enqueueForceUpdate: function() {
}, enqueueReplaceState: function() {
}, enqueueSetState: function() {
} }, Gu = Object.assign, Zu = {};
function it(e, n, t) {
  this.props = e, this.context = n, this.refs = Zu, this.updater = t || Xu;
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
function Ju() {
}
Ju.prototype = it.prototype;
function $i(e, n, t) {
  this.props = e, this.context = n, this.refs = Zu, this.updater = t || Xu;
}
var Ai = $i.prototype = new Ju();
Ai.constructor = $i;
Gu(Ai, it.prototype);
Ai.isPureReactComponent = !0;
var Io = Array.isArray, qu = Object.prototype.hasOwnProperty, Vi = { current: null }, bu = { key: !0, ref: !0, __self: !0, __source: !0 };
function es(e, n, t) {
  var r, l = {}, i = null, o = null;
  if (n != null)
    for (r in n.ref !== void 0 && (o = n.ref), n.key !== void 0 && (i = "" + n.key), n)
      qu.call(n, r) && !bu.hasOwnProperty(r) && (l[r] = n[r]);
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
  return { $$typeof: Gt, type: e, key: i, ref: o, props: l, _owner: Vi.current };
}
function yc(e, n) {
  return { $$typeof: Gt, type: e.type, key: n, ref: e.ref, props: e.props, _owner: e._owner };
}
function Bi(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Gt;
}
function gc(e) {
  var n = { "=": "=0", ":": "=2" };
  return "$" + e.replace(/[=:]/g, function(t) {
    return n[t];
  });
}
var Fo = /\/+/g;
function kl(e, n) {
  return typeof e == "object" && e !== null && e.key != null ? gc("" + e.key) : n.toString(36);
}
function wr(e, n, t, r, l) {
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
          case Gt:
          case oc:
            o = !0;
        }
    }
  if (o)
    return o = e, l = l(o), e = r === "" ? "." + kl(o, 0) : r, Io(l) ? (t = "", e != null && (t = e.replace(Fo, "$&/") + "/"), wr(l, n, t, "", function(c) {
      return c;
    })) : l != null && (Bi(l) && (l = yc(l, t + (!l.key || o && o.key === l.key ? "" : ("" + l.key).replace(Fo, "$&/") + "/") + e)), n.push(l)), 1;
  if (o = 0, r = r === "" ? "." : r + ":", Io(e))
    for (var u = 0; u < e.length; u++) {
      i = e[u];
      var s = r + kl(i, u);
      o += wr(i, n, t, s, l);
    }
  else if (s = vc(e), typeof s == "function")
    for (e = s.call(e), u = 0; !(i = e.next()).done; )
      i = i.value, s = r + kl(i, u++), o += wr(i, n, t, s, l);
  else if (i === "object")
    throw n = String(e), Error("Objects are not valid as a React child (found: " + (n === "[object Object]" ? "object with keys {" + Object.keys(e).join(", ") + "}" : n) + "). If you meant to render a collection of children, use an array instead.");
  return o;
}
function tr(e, n, t) {
  if (e == null)
    return e;
  var r = [], l = 0;
  return wr(e, r, "", "", function(i) {
    return n.call(t, i, l++);
  }), r;
}
function wc(e) {
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
var ue = { current: null }, kr = { transition: null }, kc = { ReactCurrentDispatcher: ue, ReactCurrentBatchConfig: kr, ReactCurrentOwner: Vi };
function ns() {
  throw Error("act(...) is not supported in production builds of React.");
}
L.Children = { map: tr, forEach: function(e, n, t) {
  tr(e, function() {
    n.apply(this, arguments);
  }, t);
}, count: function(e) {
  var n = 0;
  return tr(e, function() {
    n++;
  }), n;
}, toArray: function(e) {
  return tr(e, function(n) {
    return n;
  }) || [];
}, only: function(e) {
  if (!Bi(e))
    throw Error("React.Children.only expected to receive a single React element child.");
  return e;
} };
L.Component = it;
L.Fragment = uc;
L.Profiler = ac;
L.PureComponent = $i;
L.StrictMode = sc;
L.Suspense = pc;
L.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = kc;
L.act = ns;
L.cloneElement = function(e, n, t) {
  if (e == null)
    throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + e + ".");
  var r = Gu({}, e.props), l = e.key, i = e.ref, o = e._owner;
  if (n != null) {
    if (n.ref !== void 0 && (i = n.ref, o = Vi.current), n.key !== void 0 && (l = "" + n.key), e.type && e.type.defaultProps)
      var u = e.type.defaultProps;
    for (s in n)
      qu.call(n, s) && !bu.hasOwnProperty(s) && (r[s] = n[s] === void 0 && u !== void 0 ? u[s] : n[s]);
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
  return { $$typeof: Gt, type: e.type, key: l, ref: i, props: r, _owner: o };
};
L.createContext = function(e) {
  return e = { $$typeof: fc, _currentValue: e, _currentValue2: e, _threadCount: 0, Provider: null, Consumer: null, _defaultValue: null, _globalName: null }, e.Provider = { $$typeof: cc, _context: e }, e.Consumer = e;
};
L.createElement = es;
L.createFactory = function(e) {
  var n = es.bind(null, e);
  return n.type = e, n;
};
L.createRef = function() {
  return { current: null };
};
L.forwardRef = function(e) {
  return { $$typeof: dc, render: e };
};
L.isValidElement = Bi;
L.lazy = function(e) {
  return { $$typeof: hc, _payload: { _status: -1, _result: e }, _init: wc };
};
L.memo = function(e, n) {
  return { $$typeof: mc, type: e, compare: n === void 0 ? null : n };
};
L.startTransition = function(e) {
  var n = kr.transition;
  kr.transition = {};
  try {
    e();
  } finally {
    kr.transition = n;
  }
};
L.unstable_act = ns;
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
Yu.exports = L;
var kn = Yu.exports;
const Sc = /* @__PURE__ */ ic(kn);
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var xc = kn, Ec = Symbol.for("react.element"), Cc = Symbol.for("react.fragment"), _c = Object.prototype.hasOwnProperty, Nc = xc.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Pc = { key: !0, ref: !0, __self: !0, __source: !0 };
function ts(e, n, t) {
  var r, l = {}, i = null, o = null;
  t !== void 0 && (i = "" + t), n.key !== void 0 && (i = "" + n.key), n.ref !== void 0 && (o = n.ref);
  for (r in n)
    _c.call(n, r) && !Pc.hasOwnProperty(r) && (l[r] = n[r]);
  if (e && e.defaultProps)
    for (r in n = e.defaultProps, n)
      l[r] === void 0 && (l[r] = n[r]);
  return { $$typeof: Ec, type: e, key: i, ref: o, props: l, _owner: Nc.current };
}
nl.Fragment = Cc;
nl.jsx = ts;
nl.jsxs = ts;
Ku.exports = nl;
var C = Ku.exports, Kl = {}, rs = { exports: {} }, ge = {}, ls = { exports: {} }, is = {};
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
  function n(E, z) {
    var T = E.length;
    E.push(z);
    e:
      for (; 0 < T; ) {
        var H = T - 1 >>> 1, G = E[H];
        if (0 < l(G, z))
          E[H] = z, E[T] = G, T = H;
        else
          break e;
      }
  }
  function t(E) {
    return E.length === 0 ? null : E[0];
  }
  function r(E) {
    if (E.length === 0)
      return null;
    var z = E[0], T = E.pop();
    if (T !== z) {
      E[0] = T;
      e:
        for (var H = 0, G = E.length, er = G >>> 1; H < er; ) {
          var vn = 2 * (H + 1) - 1, wl = E[vn], yn = vn + 1, nr = E[yn];
          if (0 > l(wl, T))
            yn < G && 0 > l(nr, wl) ? (E[H] = nr, E[yn] = T, H = yn) : (E[H] = wl, E[vn] = T, H = vn);
          else if (yn < G && 0 > l(nr, T))
            E[H] = nr, E[yn] = T, H = yn;
          else
            break e;
        }
    }
    return z;
  }
  function l(E, z) {
    var T = E.sortIndex - z.sortIndex;
    return T !== 0 ? T : E.id - z.id;
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
  var s = [], c = [], h = 1, m = null, p = 3, g = !1, w = !1, k = !1, F = typeof setTimeout == "function" ? setTimeout : null, f = typeof clearTimeout == "function" ? clearTimeout : null, a = typeof setImmediate < "u" ? setImmediate : null;
  typeof navigator < "u" && navigator.scheduling !== void 0 && navigator.scheduling.isInputPending !== void 0 && navigator.scheduling.isInputPending.bind(navigator.scheduling);
  function d(E) {
    for (var z = t(c); z !== null; ) {
      if (z.callback === null)
        r(c);
      else if (z.startTime <= E)
        r(c), z.sortIndex = z.expirationTime, n(s, z);
      else
        break;
      z = t(c);
    }
  }
  function v(E) {
    if (k = !1, d(E), !w)
      if (t(s) !== null)
        w = !0, yl(x);
      else {
        var z = t(c);
        z !== null && gl(v, z.startTime - E);
      }
  }
  function x(E, z) {
    w = !1, k && (k = !1, f(P), P = -1), g = !0;
    var T = p;
    try {
      for (d(z), m = t(s); m !== null && (!(m.expirationTime > z) || E && !Ne()); ) {
        var H = m.callback;
        if (typeof H == "function") {
          m.callback = null, p = m.priorityLevel;
          var G = H(m.expirationTime <= z);
          z = e.unstable_now(), typeof G == "function" ? m.callback = G : m === t(s) && r(s), d(z);
        } else
          r(s);
        m = t(s);
      }
      if (m !== null)
        var er = !0;
      else {
        var vn = t(c);
        vn !== null && gl(v, vn.startTime - z), er = !1;
      }
      return er;
    } finally {
      m = null, p = T, g = !1;
    }
  }
  var _ = !1, N = null, P = -1, W = 5, j = -1;
  function Ne() {
    return !(e.unstable_now() - j < W);
  }
  function st() {
    if (N !== null) {
      var E = e.unstable_now();
      j = E;
      var z = !0;
      try {
        z = N(!0, E);
      } finally {
        z ? at() : (_ = !1, N = null);
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
    var Mo = new MessageChannel(), lc = Mo.port2;
    Mo.port1.onmessage = st, at = function() {
      lc.postMessage(null);
    };
  } else
    at = function() {
      F(st, 0);
    };
  function yl(E) {
    N = E, _ || (_ = !0, at());
  }
  function gl(E, z) {
    P = F(function() {
      E(e.unstable_now());
    }, z);
  }
  e.unstable_IdlePriority = 5, e.unstable_ImmediatePriority = 1, e.unstable_LowPriority = 4, e.unstable_NormalPriority = 3, e.unstable_Profiling = null, e.unstable_UserBlockingPriority = 2, e.unstable_cancelCallback = function(E) {
    E.callback = null;
  }, e.unstable_continueExecution = function() {
    w || g || (w = !0, yl(x));
  }, e.unstable_forceFrameRate = function(E) {
    0 > E || 125 < E ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : W = 0 < E ? Math.floor(1e3 / E) : 5;
  }, e.unstable_getCurrentPriorityLevel = function() {
    return p;
  }, e.unstable_getFirstCallbackNode = function() {
    return t(s);
  }, e.unstable_next = function(E) {
    switch (p) {
      case 1:
      case 2:
      case 3:
        var z = 3;
        break;
      default:
        z = p;
    }
    var T = p;
    p = z;
    try {
      return E();
    } finally {
      p = T;
    }
  }, e.unstable_pauseExecution = function() {
  }, e.unstable_requestPaint = function() {
  }, e.unstable_runWithPriority = function(E, z) {
    switch (E) {
      case 1:
      case 2:
      case 3:
      case 4:
      case 5:
        break;
      default:
        E = 3;
    }
    var T = p;
    p = E;
    try {
      return z();
    } finally {
      p = T;
    }
  }, e.unstable_scheduleCallback = function(E, z, T) {
    var H = e.unstable_now();
    switch (typeof T == "object" && T !== null ? (T = T.delay, T = typeof T == "number" && 0 < T ? H + T : H) : T = H, E) {
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
    return G = T + G, E = { id: h++, callback: z, priorityLevel: E, startTime: T, expirationTime: G, sortIndex: -1 }, T > H ? (E.sortIndex = T, n(c, E), t(s) === null && E === t(c) && (k ? (f(P), P = -1) : k = !0, gl(v, T - H))) : (E.sortIndex = G, n(s, E), w || g || (w = !0, yl(x))), E;
  }, e.unstable_shouldYield = Ne, e.unstable_wrapCallback = function(E) {
    var z = p;
    return function() {
      var T = p;
      p = z;
      try {
        return E.apply(this, arguments);
      } finally {
        p = T;
      }
    };
  };
})(is);
ls.exports = is;
var zc = ls.exports;
/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Tc = kn, ye = zc;
function y(e) {
  for (var n = "https://reactjs.org/docs/error-decoder.html?invariant=" + e, t = 1; t < arguments.length; t++)
    n += "&args[]=" + encodeURIComponent(arguments[t]);
  return "Minified React error #" + e + "; visit " + n + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
}
var os = /* @__PURE__ */ new Set(), Rt = {};
function jn(e, n) {
  qn(e, n), qn(e + "Capture", n);
}
function qn(e, n) {
  for (Rt[e] = n, e = 0; e < n.length; e++)
    os.add(n[e]);
}
var He = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), Yl = Object.prototype.hasOwnProperty, Lc = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, Uo = {}, $o = {};
function jc(e) {
  return Yl.call($o, e) ? !0 : Yl.call(Uo, e) ? !1 : Lc.test(e) ? $o[e] = !0 : (Uo[e] = !0, !1);
}
function Rc(e, n, t, r) {
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
function Dc(e, n, t, r) {
  if (n === null || typeof n > "u" || Rc(e, n, t, r))
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
var Wi = /[\-:]([a-z])/g;
function Hi(e) {
  return e[1].toUpperCase();
}
"accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(e) {
  var n = e.replace(
    Wi,
    Hi
  );
  ee[n] = new se(n, 1, !1, e, null, !1, !1);
});
"xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(e) {
  var n = e.replace(Wi, Hi);
  ee[n] = new se(n, 1, !1, e, "http://www.w3.org/1999/xlink", !1, !1);
});
["xml:base", "xml:lang", "xml:space"].forEach(function(e) {
  var n = e.replace(Wi, Hi);
  ee[n] = new se(n, 1, !1, e, "http://www.w3.org/XML/1998/namespace", !1, !1);
});
["tabIndex", "crossOrigin"].forEach(function(e) {
  ee[e] = new se(e, 1, !1, e.toLowerCase(), null, !1, !1);
});
ee.xlinkHref = new se("xlinkHref", 1, !1, "xlink:href", "http://www.w3.org/1999/xlink", !0, !1);
["src", "href", "action", "formAction"].forEach(function(e) {
  ee[e] = new se(e, 1, !1, e.toLowerCase(), null, !0, !0);
});
function Qi(e, n, t, r) {
  var l = ee.hasOwnProperty(n) ? ee[n] : null;
  (l !== null ? l.type !== 0 : r || !(2 < n.length) || n[0] !== "o" && n[0] !== "O" || n[1] !== "n" && n[1] !== "N") && (Dc(n, t, l, r) && (t = null), r || l === null ? jc(n) && (t === null ? e.removeAttribute(n) : e.setAttribute(n, "" + t)) : l.mustUseProperty ? e[l.propertyName] = t === null ? l.type === 3 ? !1 : "" : t : (n = l.attributeName, r = l.attributeNamespace, t === null ? e.removeAttribute(n) : (l = l.type, t = l === 3 || l === 4 && t === !0 ? "" : "" + t, r ? e.setAttributeNS(r, n, t) : e.setAttribute(n, t))));
}
var Xe = Tc.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, rr = Symbol.for("react.element"), Mn = Symbol.for("react.portal"), On = Symbol.for("react.fragment"), Ki = Symbol.for("react.strict_mode"), Xl = Symbol.for("react.profiler"), us = Symbol.for("react.provider"), ss = Symbol.for("react.context"), Yi = Symbol.for("react.forward_ref"), Gl = Symbol.for("react.suspense"), Zl = Symbol.for("react.suspense_list"), Xi = Symbol.for("react.memo"), Ze = Symbol.for("react.lazy"), as = Symbol.for("react.offscreen"), Ao = Symbol.iterator;
function ct(e) {
  return e === null || typeof e != "object" ? null : (e = Ao && e[Ao] || e["@@iterator"], typeof e == "function" ? e : null);
}
var V = Object.assign, Sl;
function wt(e) {
  if (Sl === void 0)
    try {
      throw Error();
    } catch (t) {
      var n = t.stack.trim().match(/\n( *(at )?)/);
      Sl = n && n[1] || "";
    }
  return `
` + Sl + e;
}
var xl = !1;
function El(e, n) {
  if (!e || xl)
    return "";
  xl = !0;
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
    xl = !1, Error.prepareStackTrace = t;
  }
  return (e = e ? e.displayName || e.name : "") ? wt(e) : "";
}
function Mc(e) {
  switch (e.tag) {
    case 5:
      return wt(e.type);
    case 16:
      return wt("Lazy");
    case 13:
      return wt("Suspense");
    case 19:
      return wt("SuspenseList");
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
function Jl(e) {
  if (e == null)
    return null;
  if (typeof e == "function")
    return e.displayName || e.name || null;
  if (typeof e == "string")
    return e;
  switch (e) {
    case On:
      return "Fragment";
    case Mn:
      return "Portal";
    case Xl:
      return "Profiler";
    case Ki:
      return "StrictMode";
    case Gl:
      return "Suspense";
    case Zl:
      return "SuspenseList";
  }
  if (typeof e == "object")
    switch (e.$$typeof) {
      case ss:
        return (e.displayName || "Context") + ".Consumer";
      case us:
        return (e._context.displayName || "Context") + ".Provider";
      case Yi:
        var n = e.render;
        return e = e.displayName, e || (e = n.displayName || n.name || "", e = e !== "" ? "ForwardRef(" + e + ")" : "ForwardRef"), e;
      case Xi:
        return n = e.displayName || null, n !== null ? n : Jl(e.type) || "Memo";
      case Ze:
        n = e._payload, e = e._init;
        try {
          return Jl(e(n));
        } catch {
        }
    }
  return null;
}
function Oc(e) {
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
      return Jl(n);
    case 8:
      return n === Ki ? "StrictMode" : "Mode";
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
function fn(e) {
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
function cs(e) {
  var n = e.type;
  return (e = e.nodeName) && e.toLowerCase() === "input" && (n === "checkbox" || n === "radio");
}
function Ic(e) {
  var n = cs(e) ? "checked" : "value", t = Object.getOwnPropertyDescriptor(e.constructor.prototype, n), r = "" + e[n];
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
function lr(e) {
  e._valueTracker || (e._valueTracker = Ic(e));
}
function fs(e) {
  if (!e)
    return !1;
  var n = e._valueTracker;
  if (!n)
    return !0;
  var t = n.getValue(), r = "";
  return e && (r = cs(e) ? e.checked ? "true" : "false" : e.value), e = r, e !== t ? (n.setValue(e), !0) : !1;
}
function jr(e) {
  if (e = e || (typeof document < "u" ? document : void 0), typeof e > "u")
    return null;
  try {
    return e.activeElement || e.body;
  } catch {
    return e.body;
  }
}
function ql(e, n) {
  var t = n.checked;
  return V({}, n, { defaultChecked: void 0, defaultValue: void 0, value: void 0, checked: t ?? e._wrapperState.initialChecked });
}
function Vo(e, n) {
  var t = n.defaultValue == null ? "" : n.defaultValue, r = n.checked != null ? n.checked : n.defaultChecked;
  t = fn(n.value != null ? n.value : t), e._wrapperState = { initialChecked: r, initialValue: t, controlled: n.type === "checkbox" || n.type === "radio" ? n.checked != null : n.value != null };
}
function ds(e, n) {
  n = n.checked, n != null && Qi(e, "checked", n, !1);
}
function bl(e, n) {
  ds(e, n);
  var t = fn(n.value), r = n.type;
  if (t != null)
    r === "number" ? (t === 0 && e.value === "" || e.value != t) && (e.value = "" + t) : e.value !== "" + t && (e.value = "" + t);
  else if (r === "submit" || r === "reset") {
    e.removeAttribute("value");
    return;
  }
  n.hasOwnProperty("value") ? ei(e, n.type, t) : n.hasOwnProperty("defaultValue") && ei(e, n.type, fn(n.defaultValue)), n.checked == null && n.defaultChecked != null && (e.defaultChecked = !!n.defaultChecked);
}
function Bo(e, n, t) {
  if (n.hasOwnProperty("value") || n.hasOwnProperty("defaultValue")) {
    var r = n.type;
    if (!(r !== "submit" && r !== "reset" || n.value !== void 0 && n.value !== null))
      return;
    n = "" + e._wrapperState.initialValue, t || n === e.value || (e.value = n), e.defaultValue = n;
  }
  t = e.name, t !== "" && (e.name = ""), e.defaultChecked = !!e._wrapperState.initialChecked, t !== "" && (e.name = t);
}
function ei(e, n, t) {
  (n !== "number" || jr(e.ownerDocument) !== e) && (t == null ? e.defaultValue = "" + e._wrapperState.initialValue : e.defaultValue !== "" + t && (e.defaultValue = "" + t));
}
var kt = Array.isArray;
function Kn(e, n, t, r) {
  if (e = e.options, n) {
    n = {};
    for (var l = 0; l < t.length; l++)
      n["$" + t[l]] = !0;
    for (t = 0; t < e.length; t++)
      l = n.hasOwnProperty("$" + e[t].value), e[t].selected !== l && (e[t].selected = l), l && r && (e[t].defaultSelected = !0);
  } else {
    for (t = "" + fn(t), n = null, l = 0; l < e.length; l++) {
      if (e[l].value === t) {
        e[l].selected = !0, r && (e[l].defaultSelected = !0);
        return;
      }
      n !== null || e[l].disabled || (n = e[l]);
    }
    n !== null && (n.selected = !0);
  }
}
function ni(e, n) {
  if (n.dangerouslySetInnerHTML != null)
    throw Error(y(91));
  return V({}, n, { value: void 0, defaultValue: void 0, children: "" + e._wrapperState.initialValue });
}
function Wo(e, n) {
  var t = n.value;
  if (t == null) {
    if (t = n.children, n = n.defaultValue, t != null) {
      if (n != null)
        throw Error(y(92));
      if (kt(t)) {
        if (1 < t.length)
          throw Error(y(93));
        t = t[0];
      }
      n = t;
    }
    n == null && (n = ""), t = n;
  }
  e._wrapperState = { initialValue: fn(t) };
}
function ps(e, n) {
  var t = fn(n.value), r = fn(n.defaultValue);
  t != null && (t = "" + t, t !== e.value && (e.value = t), n.defaultValue == null && e.defaultValue !== t && (e.defaultValue = t)), r != null && (e.defaultValue = "" + r);
}
function Ho(e) {
  var n = e.textContent;
  n === e._wrapperState.initialValue && n !== "" && n !== null && (e.value = n);
}
function ms(e) {
  switch (e) {
    case "svg":
      return "http://www.w3.org/2000/svg";
    case "math":
      return "http://www.w3.org/1998/Math/MathML";
    default:
      return "http://www.w3.org/1999/xhtml";
  }
}
function ti(e, n) {
  return e == null || e === "http://www.w3.org/1999/xhtml" ? ms(n) : e === "http://www.w3.org/2000/svg" && n === "foreignObject" ? "http://www.w3.org/1999/xhtml" : e;
}
var ir, hs = function(e) {
  return typeof MSApp < "u" && MSApp.execUnsafeLocalFunction ? function(n, t, r, l) {
    MSApp.execUnsafeLocalFunction(function() {
      return e(n, t, r, l);
    });
  } : e;
}(function(e, n) {
  if (e.namespaceURI !== "http://www.w3.org/2000/svg" || "innerHTML" in e)
    e.innerHTML = n;
  else {
    for (ir = ir || document.createElement("div"), ir.innerHTML = "<svg>" + n.valueOf().toString() + "</svg>", n = ir.firstChild; e.firstChild; )
      e.removeChild(e.firstChild);
    for (; n.firstChild; )
      e.appendChild(n.firstChild);
  }
});
function Dt(e, n) {
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
}, Fc = ["Webkit", "ms", "Moz", "O"];
Object.keys(Et).forEach(function(e) {
  Fc.forEach(function(n) {
    n = n + e.charAt(0).toUpperCase() + e.substring(1), Et[n] = Et[e];
  });
});
function vs(e, n, t) {
  return n == null || typeof n == "boolean" || n === "" ? "" : t || typeof n != "number" || n === 0 || Et.hasOwnProperty(e) && Et[e] ? ("" + n).trim() : n + "px";
}
function ys(e, n) {
  e = e.style;
  for (var t in n)
    if (n.hasOwnProperty(t)) {
      var r = t.indexOf("--") === 0, l = vs(t, n[t], r);
      t === "float" && (t = "cssFloat"), r ? e.setProperty(t, l) : e[t] = l;
    }
}
var Uc = V({ menuitem: !0 }, { area: !0, base: !0, br: !0, col: !0, embed: !0, hr: !0, img: !0, input: !0, keygen: !0, link: !0, meta: !0, param: !0, source: !0, track: !0, wbr: !0 });
function ri(e, n) {
  if (n) {
    if (Uc[e] && (n.children != null || n.dangerouslySetInnerHTML != null))
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
function li(e, n) {
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
var ii = null;
function Gi(e) {
  return e = e.target || e.srcElement || window, e.correspondingUseElement && (e = e.correspondingUseElement), e.nodeType === 3 ? e.parentNode : e;
}
var oi = null, Yn = null, Xn = null;
function Qo(e) {
  if (e = qt(e)) {
    if (typeof oi != "function")
      throw Error(y(280));
    var n = e.stateNode;
    n && (n = ol(n), oi(e.stateNode, e.type, n));
  }
}
function gs(e) {
  Yn ? Xn ? Xn.push(e) : Xn = [e] : Yn = e;
}
function ws() {
  if (Yn) {
    var e = Yn, n = Xn;
    if (Xn = Yn = null, Qo(e), n)
      for (e = 0; e < n.length; e++)
        Qo(n[e]);
  }
}
function ks(e, n) {
  return e(n);
}
function Ss() {
}
var Cl = !1;
function xs(e, n, t) {
  if (Cl)
    return e(n, t);
  Cl = !0;
  try {
    return ks(e, n, t);
  } finally {
    Cl = !1, (Yn !== null || Xn !== null) && (Ss(), ws());
  }
}
function Mt(e, n) {
  var t = e.stateNode;
  if (t === null)
    return null;
  var r = ol(t);
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
var ui = !1;
if (He)
  try {
    var ft = {};
    Object.defineProperty(ft, "passive", { get: function() {
      ui = !0;
    } }), window.addEventListener("test", ft, ft), window.removeEventListener("test", ft, ft);
  } catch {
    ui = !1;
  }
function $c(e, n, t, r, l, i, o, u, s) {
  var c = Array.prototype.slice.call(arguments, 3);
  try {
    n.apply(t, c);
  } catch (h) {
    this.onError(h);
  }
}
var Ct = !1, Rr = null, Dr = !1, si = null, Ac = { onError: function(e) {
  Ct = !0, Rr = e;
} };
function Vc(e, n, t, r, l, i, o, u, s) {
  Ct = !1, Rr = null, $c.apply(Ac, arguments);
}
function Bc(e, n, t, r, l, i, o, u, s) {
  if (Vc.apply(this, arguments), Ct) {
    if (Ct) {
      var c = Rr;
      Ct = !1, Rr = null;
    } else
      throw Error(y(198));
    Dr || (Dr = !0, si = c);
  }
}
function Rn(e) {
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
function Es(e) {
  if (e.tag === 13) {
    var n = e.memoizedState;
    if (n === null && (e = e.alternate, e !== null && (n = e.memoizedState)), n !== null)
      return n.dehydrated;
  }
  return null;
}
function Ko(e) {
  if (Rn(e) !== e)
    throw Error(y(188));
}
function Wc(e) {
  var n = e.alternate;
  if (!n) {
    if (n = Rn(e), n === null)
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
          return Ko(l), e;
        if (i === r)
          return Ko(l), n;
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
function Cs(e) {
  return e = Wc(e), e !== null ? _s(e) : null;
}
function _s(e) {
  if (e.tag === 5 || e.tag === 6)
    return e;
  for (e = e.child; e !== null; ) {
    var n = _s(e);
    if (n !== null)
      return n;
    e = e.sibling;
  }
  return null;
}
var Ns = ye.unstable_scheduleCallback, Yo = ye.unstable_cancelCallback, Hc = ye.unstable_shouldYield, Qc = ye.unstable_requestPaint, Q = ye.unstable_now, Kc = ye.unstable_getCurrentPriorityLevel, Zi = ye.unstable_ImmediatePriority, Ps = ye.unstable_UserBlockingPriority, Mr = ye.unstable_NormalPriority, Yc = ye.unstable_LowPriority, zs = ye.unstable_IdlePriority, tl = null, Fe = null;
function Xc(e) {
  if (Fe && typeof Fe.onCommitFiberRoot == "function")
    try {
      Fe.onCommitFiberRoot(tl, e, void 0, (e.current.flags & 128) === 128);
    } catch {
    }
}
var je = Math.clz32 ? Math.clz32 : Jc, Gc = Math.log, Zc = Math.LN2;
function Jc(e) {
  return e >>>= 0, e === 0 ? 32 : 31 - (Gc(e) / Zc | 0) | 0;
}
var or = 64, ur = 4194304;
function St(e) {
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
    u !== 0 ? r = St(u) : (i &= o, i !== 0 && (r = St(i)));
  } else
    o = t & ~l, o !== 0 ? r = St(o) : i !== 0 && (r = St(i));
  if (r === 0)
    return 0;
  if (n !== 0 && n !== r && !(n & l) && (l = r & -r, i = n & -n, l >= i || l === 16 && (i & 4194240) !== 0))
    return n;
  if (r & 4 && (r |= t & 16), n = e.entangledLanes, n !== 0)
    for (e = e.entanglements, n &= r; 0 < n; )
      t = 31 - je(n), l = 1 << t, r |= e[t], n &= ~l;
  return r;
}
function qc(e, n) {
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
function bc(e, n) {
  for (var t = e.suspendedLanes, r = e.pingedLanes, l = e.expirationTimes, i = e.pendingLanes; 0 < i; ) {
    var o = 31 - je(i), u = 1 << o, s = l[o];
    s === -1 ? (!(u & t) || u & r) && (l[o] = qc(u, n)) : s <= n && (e.expiredLanes |= u), i &= ~u;
  }
}
function ai(e) {
  return e = e.pendingLanes & -1073741825, e !== 0 ? e : e & 1073741824 ? 1073741824 : 0;
}
function Ts() {
  var e = or;
  return or <<= 1, !(or & 4194240) && (or = 64), e;
}
function _l(e) {
  for (var n = [], t = 0; 31 > t; t++)
    n.push(e);
  return n;
}
function Zt(e, n, t) {
  e.pendingLanes |= n, n !== 536870912 && (e.suspendedLanes = 0, e.pingedLanes = 0), e = e.eventTimes, n = 31 - je(n), e[n] = t;
}
function ef(e, n) {
  var t = e.pendingLanes & ~n;
  e.pendingLanes = n, e.suspendedLanes = 0, e.pingedLanes = 0, e.expiredLanes &= n, e.mutableReadLanes &= n, e.entangledLanes &= n, n = e.entanglements;
  var r = e.eventTimes;
  for (e = e.expirationTimes; 0 < t; ) {
    var l = 31 - je(t), i = 1 << l;
    n[l] = 0, r[l] = -1, e[l] = -1, t &= ~i;
  }
}
function Ji(e, n) {
  var t = e.entangledLanes |= n;
  for (e = e.entanglements; t; ) {
    var r = 31 - je(t), l = 1 << r;
    l & n | e[r] & n && (e[r] |= n), t &= ~l;
  }
}
var D = 0;
function Ls(e) {
  return e &= -e, 1 < e ? 4 < e ? e & 268435455 ? 16 : 536870912 : 4 : 1;
}
var js, qi, Rs, Ds, Ms, ci = !1, sr = [], tn = null, rn = null, ln = null, Ot = /* @__PURE__ */ new Map(), It = /* @__PURE__ */ new Map(), qe = [], nf = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
function Xo(e, n) {
  switch (e) {
    case "focusin":
    case "focusout":
      tn = null;
      break;
    case "dragenter":
    case "dragleave":
      rn = null;
      break;
    case "mouseover":
    case "mouseout":
      ln = null;
      break;
    case "pointerover":
    case "pointerout":
      Ot.delete(n.pointerId);
      break;
    case "gotpointercapture":
    case "lostpointercapture":
      It.delete(n.pointerId);
  }
}
function dt(e, n, t, r, l, i) {
  return e === null || e.nativeEvent !== i ? (e = { blockedOn: n, domEventName: t, eventSystemFlags: r, nativeEvent: i, targetContainers: [l] }, n !== null && (n = qt(n), n !== null && qi(n)), e) : (e.eventSystemFlags |= r, n = e.targetContainers, l !== null && n.indexOf(l) === -1 && n.push(l), e);
}
function tf(e, n, t, r, l) {
  switch (n) {
    case "focusin":
      return tn = dt(tn, e, n, t, r, l), !0;
    case "dragenter":
      return rn = dt(rn, e, n, t, r, l), !0;
    case "mouseover":
      return ln = dt(ln, e, n, t, r, l), !0;
    case "pointerover":
      var i = l.pointerId;
      return Ot.set(i, dt(Ot.get(i) || null, e, n, t, r, l)), !0;
    case "gotpointercapture":
      return i = l.pointerId, It.set(i, dt(It.get(i) || null, e, n, t, r, l)), !0;
  }
  return !1;
}
function Os(e) {
  var n = Sn(e.target);
  if (n !== null) {
    var t = Rn(n);
    if (t !== null) {
      if (n = t.tag, n === 13) {
        if (n = Es(t), n !== null) {
          e.blockedOn = n, Ms(e.priority, function() {
            Rs(t);
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
function Sr(e) {
  if (e.blockedOn !== null)
    return !1;
  for (var n = e.targetContainers; 0 < n.length; ) {
    var t = fi(e.domEventName, e.eventSystemFlags, n[0], e.nativeEvent);
    if (t === null) {
      t = e.nativeEvent;
      var r = new t.constructor(t.type, t);
      ii = r, t.target.dispatchEvent(r), ii = null;
    } else
      return n = qt(t), n !== null && qi(n), e.blockedOn = t, !1;
    n.shift();
  }
  return !0;
}
function Go(e, n, t) {
  Sr(e) && t.delete(n);
}
function rf() {
  ci = !1, tn !== null && Sr(tn) && (tn = null), rn !== null && Sr(rn) && (rn = null), ln !== null && Sr(ln) && (ln = null), Ot.forEach(Go), It.forEach(Go);
}
function pt(e, n) {
  e.blockedOn === n && (e.blockedOn = null, ci || (ci = !0, ye.unstable_scheduleCallback(ye.unstable_NormalPriority, rf)));
}
function Ft(e) {
  function n(l) {
    return pt(l, e);
  }
  if (0 < sr.length) {
    pt(sr[0], e);
    for (var t = 1; t < sr.length; t++) {
      var r = sr[t];
      r.blockedOn === e && (r.blockedOn = null);
    }
  }
  for (tn !== null && pt(tn, e), rn !== null && pt(rn, e), ln !== null && pt(ln, e), Ot.forEach(n), It.forEach(n), t = 0; t < qe.length; t++)
    r = qe[t], r.blockedOn === e && (r.blockedOn = null);
  for (; 0 < qe.length && (t = qe[0], t.blockedOn === null); )
    Os(t), t.blockedOn === null && qe.shift();
}
var Gn = Xe.ReactCurrentBatchConfig, Ir = !0;
function lf(e, n, t, r) {
  var l = D, i = Gn.transition;
  Gn.transition = null;
  try {
    D = 1, bi(e, n, t, r);
  } finally {
    D = l, Gn.transition = i;
  }
}
function of(e, n, t, r) {
  var l = D, i = Gn.transition;
  Gn.transition = null;
  try {
    D = 4, bi(e, n, t, r);
  } finally {
    D = l, Gn.transition = i;
  }
}
function bi(e, n, t, r) {
  if (Ir) {
    var l = fi(e, n, t, r);
    if (l === null)
      Ol(e, n, r, Fr, t), Xo(e, r);
    else if (tf(l, e, n, t, r))
      r.stopPropagation();
    else if (Xo(e, r), n & 4 && -1 < nf.indexOf(e)) {
      for (; l !== null; ) {
        var i = qt(l);
        if (i !== null && js(i), i = fi(e, n, t, r), i === null && Ol(e, n, r, Fr, t), i === l)
          break;
        l = i;
      }
      l !== null && r.stopPropagation();
    } else
      Ol(e, n, r, null, t);
  }
}
var Fr = null;
function fi(e, n, t, r) {
  if (Fr = null, e = Gi(r), e = Sn(e), e !== null)
    if (n = Rn(e), n === null)
      e = null;
    else if (t = n.tag, t === 13) {
      if (e = Es(n), e !== null)
        return e;
      e = null;
    } else if (t === 3) {
      if (n.stateNode.current.memoizedState.isDehydrated)
        return n.tag === 3 ? n.stateNode.containerInfo : null;
      e = null;
    } else
      n !== e && (e = null);
  return Fr = e, null;
}
function Is(e) {
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
      switch (Kc()) {
        case Zi:
          return 1;
        case Ps:
          return 4;
        case Mr:
        case Yc:
          return 16;
        case zs:
          return 536870912;
        default:
          return 16;
      }
    default:
      return 16;
  }
}
var en = null, eo = null, xr = null;
function Fs() {
  if (xr)
    return xr;
  var e, n = eo, t = n.length, r, l = "value" in en ? en.value : en.textContent, i = l.length;
  for (e = 0; e < t && n[e] === l[e]; e++)
    ;
  var o = t - e;
  for (r = 1; r <= o && n[t - r] === l[i - r]; r++)
    ;
  return xr = l.slice(e, 1 < r ? 1 - r : void 0);
}
function Er(e) {
  var n = e.keyCode;
  return "charCode" in e ? (e = e.charCode, e === 0 && n === 13 && (e = 13)) : e = n, e === 10 && (e = 13), 32 <= e || e === 13 ? e : 0;
}
function ar() {
  return !0;
}
function Zo() {
  return !1;
}
function we(e) {
  function n(t, r, l, i, o) {
    this._reactName = t, this._targetInst = l, this.type = r, this.nativeEvent = i, this.target = o, this.currentTarget = null;
    for (var u in e)
      e.hasOwnProperty(u) && (t = e[u], this[u] = t ? t(i) : i[u]);
    return this.isDefaultPrevented = (i.defaultPrevented != null ? i.defaultPrevented : i.returnValue === !1) ? ar : Zo, this.isPropagationStopped = Zo, this;
  }
  return V(n.prototype, { preventDefault: function() {
    this.defaultPrevented = !0;
    var t = this.nativeEvent;
    t && (t.preventDefault ? t.preventDefault() : typeof t.returnValue != "unknown" && (t.returnValue = !1), this.isDefaultPrevented = ar);
  }, stopPropagation: function() {
    var t = this.nativeEvent;
    t && (t.stopPropagation ? t.stopPropagation() : typeof t.cancelBubble != "unknown" && (t.cancelBubble = !0), this.isPropagationStopped = ar);
  }, persist: function() {
  }, isPersistent: ar }), n;
}
var ot = { eventPhase: 0, bubbles: 0, cancelable: 0, timeStamp: function(e) {
  return e.timeStamp || Date.now();
}, defaultPrevented: 0, isTrusted: 0 }, no = we(ot), Jt = V({}, ot, { view: 0, detail: 0 }), uf = we(Jt), Nl, Pl, mt, rl = V({}, Jt, { screenX: 0, screenY: 0, clientX: 0, clientY: 0, pageX: 0, pageY: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, getModifierState: to, button: 0, buttons: 0, relatedTarget: function(e) {
  return e.relatedTarget === void 0 ? e.fromElement === e.srcElement ? e.toElement : e.fromElement : e.relatedTarget;
}, movementX: function(e) {
  return "movementX" in e ? e.movementX : (e !== mt && (mt && e.type === "mousemove" ? (Nl = e.screenX - mt.screenX, Pl = e.screenY - mt.screenY) : Pl = Nl = 0, mt = e), Nl);
}, movementY: function(e) {
  return "movementY" in e ? e.movementY : Pl;
} }), Jo = we(rl), sf = V({}, rl, { dataTransfer: 0 }), af = we(sf), cf = V({}, Jt, { relatedTarget: 0 }), zl = we(cf), ff = V({}, ot, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }), df = we(ff), pf = V({}, ot, { clipboardData: function(e) {
  return "clipboardData" in e ? e.clipboardData : window.clipboardData;
} }), mf = we(pf), hf = V({}, ot, { data: 0 }), qo = we(hf), vf = {
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
}, yf = {
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
}, gf = { Alt: "altKey", Control: "ctrlKey", Meta: "metaKey", Shift: "shiftKey" };
function wf(e) {
  var n = this.nativeEvent;
  return n.getModifierState ? n.getModifierState(e) : (e = gf[e]) ? !!n[e] : !1;
}
function to() {
  return wf;
}
var kf = V({}, Jt, { key: function(e) {
  if (e.key) {
    var n = vf[e.key] || e.key;
    if (n !== "Unidentified")
      return n;
  }
  return e.type === "keypress" ? (e = Er(e), e === 13 ? "Enter" : String.fromCharCode(e)) : e.type === "keydown" || e.type === "keyup" ? yf[e.keyCode] || "Unidentified" : "";
}, code: 0, location: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, repeat: 0, locale: 0, getModifierState: to, charCode: function(e) {
  return e.type === "keypress" ? Er(e) : 0;
}, keyCode: function(e) {
  return e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
}, which: function(e) {
  return e.type === "keypress" ? Er(e) : e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
} }), Sf = we(kf), xf = V({}, rl, { pointerId: 0, width: 0, height: 0, pressure: 0, tangentialPressure: 0, tiltX: 0, tiltY: 0, twist: 0, pointerType: 0, isPrimary: 0 }), bo = we(xf), Ef = V({}, Jt, { touches: 0, targetTouches: 0, changedTouches: 0, altKey: 0, metaKey: 0, ctrlKey: 0, shiftKey: 0, getModifierState: to }), Cf = we(Ef), _f = V({}, ot, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }), Nf = we(_f), Pf = V({}, rl, {
  deltaX: function(e) {
    return "deltaX" in e ? e.deltaX : "wheelDeltaX" in e ? -e.wheelDeltaX : 0;
  },
  deltaY: function(e) {
    return "deltaY" in e ? e.deltaY : "wheelDeltaY" in e ? -e.wheelDeltaY : "wheelDelta" in e ? -e.wheelDelta : 0;
  },
  deltaZ: 0,
  deltaMode: 0
}), zf = we(Pf), Tf = [9, 13, 27, 32], ro = He && "CompositionEvent" in window, _t = null;
He && "documentMode" in document && (_t = document.documentMode);
var Lf = He && "TextEvent" in window && !_t, Us = He && (!ro || _t && 8 < _t && 11 >= _t), eu = String.fromCharCode(32), nu = !1;
function $s(e, n) {
  switch (e) {
    case "keyup":
      return Tf.indexOf(n.keyCode) !== -1;
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
function As(e) {
  return e = e.detail, typeof e == "object" && "data" in e ? e.data : null;
}
var In = !1;
function jf(e, n) {
  switch (e) {
    case "compositionend":
      return As(n);
    case "keypress":
      return n.which !== 32 ? null : (nu = !0, eu);
    case "textInput":
      return e = n.data, e === eu && nu ? null : e;
    default:
      return null;
  }
}
function Rf(e, n) {
  if (In)
    return e === "compositionend" || !ro && $s(e, n) ? (e = Fs(), xr = eo = en = null, In = !1, e) : null;
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
      return Us && n.locale !== "ko" ? null : n.data;
    default:
      return null;
  }
}
var Df = { color: !0, date: !0, datetime: !0, "datetime-local": !0, email: !0, month: !0, number: !0, password: !0, range: !0, search: !0, tel: !0, text: !0, time: !0, url: !0, week: !0 };
function tu(e) {
  var n = e && e.nodeName && e.nodeName.toLowerCase();
  return n === "input" ? !!Df[e.type] : n === "textarea";
}
function Vs(e, n, t, r) {
  gs(r), n = Ur(n, "onChange"), 0 < n.length && (t = new no("onChange", "change", null, t, r), e.push({ event: t, listeners: n }));
}
var Nt = null, Ut = null;
function Mf(e) {
  qs(e, 0);
}
function ll(e) {
  var n = $n(e);
  if (fs(n))
    return e;
}
function Of(e, n) {
  if (e === "change")
    return n;
}
var Bs = !1;
if (He) {
  var Tl;
  if (He) {
    var Ll = "oninput" in document;
    if (!Ll) {
      var ru = document.createElement("div");
      ru.setAttribute("oninput", "return;"), Ll = typeof ru.oninput == "function";
    }
    Tl = Ll;
  } else
    Tl = !1;
  Bs = Tl && (!document.documentMode || 9 < document.documentMode);
}
function lu() {
  Nt && (Nt.detachEvent("onpropertychange", Ws), Ut = Nt = null);
}
function Ws(e) {
  if (e.propertyName === "value" && ll(Ut)) {
    var n = [];
    Vs(n, Ut, e, Gi(e)), xs(Mf, n);
  }
}
function If(e, n, t) {
  e === "focusin" ? (lu(), Nt = n, Ut = t, Nt.attachEvent("onpropertychange", Ws)) : e === "focusout" && lu();
}
function Ff(e) {
  if (e === "selectionchange" || e === "keyup" || e === "keydown")
    return ll(Ut);
}
function Uf(e, n) {
  if (e === "click")
    return ll(n);
}
function $f(e, n) {
  if (e === "input" || e === "change")
    return ll(n);
}
function Af(e, n) {
  return e === n && (e !== 0 || 1 / e === 1 / n) || e !== e && n !== n;
}
var De = typeof Object.is == "function" ? Object.is : Af;
function $t(e, n) {
  if (De(e, n))
    return !0;
  if (typeof e != "object" || e === null || typeof n != "object" || n === null)
    return !1;
  var t = Object.keys(e), r = Object.keys(n);
  if (t.length !== r.length)
    return !1;
  for (r = 0; r < t.length; r++) {
    var l = t[r];
    if (!Yl.call(n, l) || !De(e[l], n[l]))
      return !1;
  }
  return !0;
}
function iu(e) {
  for (; e && e.firstChild; )
    e = e.firstChild;
  return e;
}
function ou(e, n) {
  var t = iu(e);
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
    t = iu(t);
  }
}
function Hs(e, n) {
  return e && n ? e === n ? !0 : e && e.nodeType === 3 ? !1 : n && n.nodeType === 3 ? Hs(e, n.parentNode) : "contains" in e ? e.contains(n) : e.compareDocumentPosition ? !!(e.compareDocumentPosition(n) & 16) : !1 : !1;
}
function Qs() {
  for (var e = window, n = jr(); n instanceof e.HTMLIFrameElement; ) {
    try {
      var t = typeof n.contentWindow.location.href == "string";
    } catch {
      t = !1;
    }
    if (t)
      e = n.contentWindow;
    else
      break;
    n = jr(e.document);
  }
  return n;
}
function lo(e) {
  var n = e && e.nodeName && e.nodeName.toLowerCase();
  return n && (n === "input" && (e.type === "text" || e.type === "search" || e.type === "tel" || e.type === "url" || e.type === "password") || n === "textarea" || e.contentEditable === "true");
}
function Vf(e) {
  var n = Qs(), t = e.focusedElem, r = e.selectionRange;
  if (n !== t && t && t.ownerDocument && Hs(t.ownerDocument.documentElement, t)) {
    if (r !== null && lo(t)) {
      if (n = r.start, e = r.end, e === void 0 && (e = n), "selectionStart" in t)
        t.selectionStart = n, t.selectionEnd = Math.min(e, t.value.length);
      else if (e = (n = t.ownerDocument || document) && n.defaultView || window, e.getSelection) {
        e = e.getSelection();
        var l = t.textContent.length, i = Math.min(r.start, l);
        r = r.end === void 0 ? i : Math.min(r.end, l), !e.extend && i > r && (l = r, r = i, i = l), l = ou(t, i);
        var o = ou(
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
var Bf = He && "documentMode" in document && 11 >= document.documentMode, Fn = null, di = null, Pt = null, pi = !1;
function uu(e, n, t) {
  var r = t.window === t ? t.document : t.nodeType === 9 ? t : t.ownerDocument;
  pi || Fn == null || Fn !== jr(r) || (r = Fn, "selectionStart" in r && lo(r) ? r = { start: r.selectionStart, end: r.selectionEnd } : (r = (r.ownerDocument && r.ownerDocument.defaultView || window).getSelection(), r = { anchorNode: r.anchorNode, anchorOffset: r.anchorOffset, focusNode: r.focusNode, focusOffset: r.focusOffset }), Pt && $t(Pt, r) || (Pt = r, r = Ur(di, "onSelect"), 0 < r.length && (n = new no("onSelect", "select", null, n, t), e.push({ event: n, listeners: r }), n.target = Fn)));
}
function cr(e, n) {
  var t = {};
  return t[e.toLowerCase()] = n.toLowerCase(), t["Webkit" + e] = "webkit" + n, t["Moz" + e] = "moz" + n, t;
}
var Un = { animationend: cr("Animation", "AnimationEnd"), animationiteration: cr("Animation", "AnimationIteration"), animationstart: cr("Animation", "AnimationStart"), transitionend: cr("Transition", "TransitionEnd") }, jl = {}, Ks = {};
He && (Ks = document.createElement("div").style, "AnimationEvent" in window || (delete Un.animationend.animation, delete Un.animationiteration.animation, delete Un.animationstart.animation), "TransitionEvent" in window || delete Un.transitionend.transition);
function il(e) {
  if (jl[e])
    return jl[e];
  if (!Un[e])
    return e;
  var n = Un[e], t;
  for (t in n)
    if (n.hasOwnProperty(t) && t in Ks)
      return jl[e] = n[t];
  return e;
}
var Ys = il("animationend"), Xs = il("animationiteration"), Gs = il("animationstart"), Zs = il("transitionend"), Js = /* @__PURE__ */ new Map(), su = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
function pn(e, n) {
  Js.set(e, n), jn(n, [e]);
}
for (var Rl = 0; Rl < su.length; Rl++) {
  var Dl = su[Rl], Wf = Dl.toLowerCase(), Hf = Dl[0].toUpperCase() + Dl.slice(1);
  pn(Wf, "on" + Hf);
}
pn(Ys, "onAnimationEnd");
pn(Xs, "onAnimationIteration");
pn(Gs, "onAnimationStart");
pn("dblclick", "onDoubleClick");
pn("focusin", "onFocus");
pn("focusout", "onBlur");
pn(Zs, "onTransitionEnd");
qn("onMouseEnter", ["mouseout", "mouseover"]);
qn("onMouseLeave", ["mouseout", "mouseover"]);
qn("onPointerEnter", ["pointerout", "pointerover"]);
qn("onPointerLeave", ["pointerout", "pointerover"]);
jn("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" "));
jn("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));
jn("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]);
jn("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" "));
jn("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" "));
jn("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
var xt = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), Qf = new Set("cancel close invalid load scroll toggle".split(" ").concat(xt));
function au(e, n, t) {
  var r = e.type || "unknown-event";
  e.currentTarget = t, Bc(r, n, void 0, e), e.currentTarget = null;
}
function qs(e, n) {
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
          au(l, u, c), i = s;
        }
      else
        for (o = 0; o < r.length; o++) {
          if (u = r[o], s = u.instance, c = u.currentTarget, u = u.listener, s !== i && l.isPropagationStopped())
            break e;
          au(l, u, c), i = s;
        }
    }
  }
  if (Dr)
    throw e = si, Dr = !1, si = null, e;
}
function O(e, n) {
  var t = n[gi];
  t === void 0 && (t = n[gi] = /* @__PURE__ */ new Set());
  var r = e + "__bubble";
  t.has(r) || (bs(n, e, 2, !1), t.add(r));
}
function Ml(e, n, t) {
  var r = 0;
  n && (r |= 4), bs(t, e, r, n);
}
var fr = "_reactListening" + Math.random().toString(36).slice(2);
function At(e) {
  if (!e[fr]) {
    e[fr] = !0, os.forEach(function(t) {
      t !== "selectionchange" && (Qf.has(t) || Ml(t, !1, e), Ml(t, !0, e));
    });
    var n = e.nodeType === 9 ? e : e.ownerDocument;
    n === null || n[fr] || (n[fr] = !0, Ml("selectionchange", !1, n));
  }
}
function bs(e, n, t, r) {
  switch (Is(n)) {
    case 1:
      var l = lf;
      break;
    case 4:
      l = of;
      break;
    default:
      l = bi;
  }
  t = l.bind(null, n, t, e), l = void 0, !ui || n !== "touchstart" && n !== "touchmove" && n !== "wheel" || (l = !0), r ? l !== void 0 ? e.addEventListener(n, t, { capture: !0, passive: l }) : e.addEventListener(n, t, !0) : l !== void 0 ? e.addEventListener(n, t, { passive: l }) : e.addEventListener(n, t, !1);
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
  xs(function() {
    var c = i, h = Gi(t), m = [];
    e: {
      var p = Js.get(e);
      if (p !== void 0) {
        var g = no, w = e;
        switch (e) {
          case "keypress":
            if (Er(t) === 0)
              break e;
          case "keydown":
          case "keyup":
            g = Sf;
            break;
          case "focusin":
            w = "focus", g = zl;
            break;
          case "focusout":
            w = "blur", g = zl;
            break;
          case "beforeblur":
          case "afterblur":
            g = zl;
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
            g = Jo;
            break;
          case "drag":
          case "dragend":
          case "dragenter":
          case "dragexit":
          case "dragleave":
          case "dragover":
          case "dragstart":
          case "drop":
            g = af;
            break;
          case "touchcancel":
          case "touchend":
          case "touchmove":
          case "touchstart":
            g = Cf;
            break;
          case Ys:
          case Xs:
          case Gs:
            g = df;
            break;
          case Zs:
            g = Nf;
            break;
          case "scroll":
            g = uf;
            break;
          case "wheel":
            g = zf;
            break;
          case "copy":
          case "cut":
          case "paste":
            g = mf;
            break;
          case "gotpointercapture":
          case "lostpointercapture":
          case "pointercancel":
          case "pointerdown":
          case "pointermove":
          case "pointerout":
          case "pointerover":
          case "pointerup":
            g = bo;
        }
        var k = (n & 4) !== 0, F = !k && e === "scroll", f = k ? p !== null ? p + "Capture" : null : p;
        k = [];
        for (var a = c, d; a !== null; ) {
          d = a;
          var v = d.stateNode;
          if (d.tag === 5 && v !== null && (d = v, f !== null && (v = Mt(a, f), v != null && k.push(Vt(a, v, d)))), F)
            break;
          a = a.return;
        }
        0 < k.length && (p = new g(p, w, null, t, h), m.push({ event: p, listeners: k }));
      }
    }
    if (!(n & 7)) {
      e: {
        if (p = e === "mouseover" || e === "pointerover", g = e === "mouseout" || e === "pointerout", p && t !== ii && (w = t.relatedTarget || t.fromElement) && (Sn(w) || w[Qe]))
          break e;
        if ((g || p) && (p = h.window === h ? h : (p = h.ownerDocument) ? p.defaultView || p.parentWindow : window, g ? (w = t.relatedTarget || t.toElement, g = c, w = w ? Sn(w) : null, w !== null && (F = Rn(w), w !== F || w.tag !== 5 && w.tag !== 6) && (w = null)) : (g = null, w = c), g !== w)) {
          if (k = Jo, v = "onMouseLeave", f = "onMouseEnter", a = "mouse", (e === "pointerout" || e === "pointerover") && (k = bo, v = "onPointerLeave", f = "onPointerEnter", a = "pointer"), F = g == null ? p : $n(g), d = w == null ? p : $n(w), p = new k(v, a + "leave", g, t, h), p.target = F, p.relatedTarget = d, v = null, Sn(h) === c && (k = new k(f, a + "enter", w, t, h), k.target = d, k.relatedTarget = F, v = k), F = v, g && w)
            n: {
              for (k = g, f = w, a = 0, d = k; d; d = Dn(d))
                a++;
              for (d = 0, v = f; v; v = Dn(v))
                d++;
              for (; 0 < a - d; )
                k = Dn(k), a--;
              for (; 0 < d - a; )
                f = Dn(f), d--;
              for (; a--; ) {
                if (k === f || f !== null && k === f.alternate)
                  break n;
                k = Dn(k), f = Dn(f);
              }
              k = null;
            }
          else
            k = null;
          g !== null && cu(m, p, g, k, !1), w !== null && F !== null && cu(m, F, w, k, !0);
        }
      }
      e: {
        if (p = c ? $n(c) : window, g = p.nodeName && p.nodeName.toLowerCase(), g === "select" || g === "input" && p.type === "file")
          var x = Of;
        else if (tu(p))
          if (Bs)
            x = $f;
          else {
            x = Ff;
            var _ = If;
          }
        else
          (g = p.nodeName) && g.toLowerCase() === "input" && (p.type === "checkbox" || p.type === "radio") && (x = Uf);
        if (x && (x = x(e, c))) {
          Vs(m, x, t, h);
          break e;
        }
        _ && _(e, p, c), e === "focusout" && (_ = p._wrapperState) && _.controlled && p.type === "number" && ei(p, "number", p.value);
      }
      switch (_ = c ? $n(c) : window, e) {
        case "focusin":
          (tu(_) || _.contentEditable === "true") && (Fn = _, di = c, Pt = null);
          break;
        case "focusout":
          Pt = di = Fn = null;
          break;
        case "mousedown":
          pi = !0;
          break;
        case "contextmenu":
        case "mouseup":
        case "dragend":
          pi = !1, uu(m, t, h);
          break;
        case "selectionchange":
          if (Bf)
            break;
        case "keydown":
        case "keyup":
          uu(m, t, h);
      }
      var N;
      if (ro)
        e: {
          switch (e) {
            case "compositionstart":
              var P = "onCompositionStart";
              break e;
            case "compositionend":
              P = "onCompositionEnd";
              break e;
            case "compositionupdate":
              P = "onCompositionUpdate";
              break e;
          }
          P = void 0;
        }
      else
        In ? $s(e, t) && (P = "onCompositionEnd") : e === "keydown" && t.keyCode === 229 && (P = "onCompositionStart");
      P && (Us && t.locale !== "ko" && (In || P !== "onCompositionStart" ? P === "onCompositionEnd" && In && (N = Fs()) : (en = h, eo = "value" in en ? en.value : en.textContent, In = !0)), _ = Ur(c, P), 0 < _.length && (P = new qo(P, e, null, t, h), m.push({ event: P, listeners: _ }), N ? P.data = N : (N = As(t), N !== null && (P.data = N)))), (N = Lf ? jf(e, t) : Rf(e, t)) && (c = Ur(c, "onBeforeInput"), 0 < c.length && (h = new qo("onBeforeInput", "beforeinput", null, t, h), m.push({ event: h, listeners: c }), h.data = N));
    }
    qs(m, n);
  });
}
function Vt(e, n, t) {
  return { instance: e, listener: n, currentTarget: t };
}
function Ur(e, n) {
  for (var t = n + "Capture", r = []; e !== null; ) {
    var l = e, i = l.stateNode;
    l.tag === 5 && i !== null && (l = i, i = Mt(e, t), i != null && r.unshift(Vt(e, i, l)), i = Mt(e, n), i != null && r.push(Vt(e, i, l))), e = e.return;
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
function cu(e, n, t, r, l) {
  for (var i = n._reactName, o = []; t !== null && t !== r; ) {
    var u = t, s = u.alternate, c = u.stateNode;
    if (s !== null && s === r)
      break;
    u.tag === 5 && c !== null && (u = c, l ? (s = Mt(t, i), s != null && o.unshift(Vt(t, s, u))) : l || (s = Mt(t, i), s != null && o.push(Vt(t, s, u)))), t = t.return;
  }
  o.length !== 0 && e.push({ event: n, listeners: o });
}
var Kf = /\r\n?/g, Yf = /\u0000|\uFFFD/g;
function fu(e) {
  return (typeof e == "string" ? e : "" + e).replace(Kf, `
`).replace(Yf, "");
}
function dr(e, n, t) {
  if (n = fu(n), fu(e) !== n && t)
    throw Error(y(425));
}
function $r() {
}
var mi = null, hi = null;
function vi(e, n) {
  return e === "textarea" || e === "noscript" || typeof n.children == "string" || typeof n.children == "number" || typeof n.dangerouslySetInnerHTML == "object" && n.dangerouslySetInnerHTML !== null && n.dangerouslySetInnerHTML.__html != null;
}
var yi = typeof setTimeout == "function" ? setTimeout : void 0, Xf = typeof clearTimeout == "function" ? clearTimeout : void 0, du = typeof Promise == "function" ? Promise : void 0, Gf = typeof queueMicrotask == "function" ? queueMicrotask : typeof du < "u" ? function(e) {
  return du.resolve(null).then(e).catch(Zf);
} : yi;
function Zf(e) {
  setTimeout(function() {
    throw e;
  });
}
function Il(e, n) {
  var t = n, r = 0;
  do {
    var l = t.nextSibling;
    if (e.removeChild(t), l && l.nodeType === 8)
      if (t = l.data, t === "/$") {
        if (r === 0) {
          e.removeChild(l), Ft(n);
          return;
        }
        r--;
      } else
        t !== "$" && t !== "$?" && t !== "$!" || r++;
    t = l;
  } while (t);
  Ft(n);
}
function on(e) {
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
function pu(e) {
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
var ut = Math.random().toString(36).slice(2), Ie = "__reactFiber$" + ut, Bt = "__reactProps$" + ut, Qe = "__reactContainer$" + ut, gi = "__reactEvents$" + ut, Jf = "__reactListeners$" + ut, qf = "__reactHandles$" + ut;
function Sn(e) {
  var n = e[Ie];
  if (n)
    return n;
  for (var t = e.parentNode; t; ) {
    if (n = t[Qe] || t[Ie]) {
      if (t = n.alternate, n.child !== null || t !== null && t.child !== null)
        for (e = pu(e); e !== null; ) {
          if (t = e[Ie])
            return t;
          e = pu(e);
        }
      return n;
    }
    e = t, t = e.parentNode;
  }
  return null;
}
function qt(e) {
  return e = e[Ie] || e[Qe], !e || e.tag !== 5 && e.tag !== 6 && e.tag !== 13 && e.tag !== 3 ? null : e;
}
function $n(e) {
  if (e.tag === 5 || e.tag === 6)
    return e.stateNode;
  throw Error(y(33));
}
function ol(e) {
  return e[Bt] || null;
}
var wi = [], An = -1;
function mn(e) {
  return { current: e };
}
function I(e) {
  0 > An || (e.current = wi[An], wi[An] = null, An--);
}
function M(e, n) {
  An++, wi[An] = e.current, e.current = n;
}
var dn = {}, le = mn(dn), fe = mn(!1), Nn = dn;
function bn(e, n) {
  var t = e.type.contextTypes;
  if (!t)
    return dn;
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
function Ar() {
  I(fe), I(le);
}
function mu(e, n, t) {
  if (le.current !== dn)
    throw Error(y(168));
  M(le, n), M(fe, t);
}
function ea(e, n, t) {
  var r = e.stateNode;
  if (n = n.childContextTypes, typeof r.getChildContext != "function")
    return t;
  r = r.getChildContext();
  for (var l in r)
    if (!(l in n))
      throw Error(y(108, Oc(e) || "Unknown", l));
  return V({}, t, r);
}
function Vr(e) {
  return e = (e = e.stateNode) && e.__reactInternalMemoizedMergedChildContext || dn, Nn = le.current, M(le, e), M(fe, fe.current), !0;
}
function hu(e, n, t) {
  var r = e.stateNode;
  if (!r)
    throw Error(y(169));
  t ? (e = ea(e, n, Nn), r.__reactInternalMemoizedMergedChildContext = e, I(fe), I(le), M(le, e)) : I(fe), M(fe, t);
}
var Ae = null, ul = !1, Fl = !1;
function na(e) {
  Ae === null ? Ae = [e] : Ae.push(e);
}
function bf(e) {
  ul = !0, na(e);
}
function hn() {
  if (!Fl && Ae !== null) {
    Fl = !0;
    var e = 0, n = D;
    try {
      var t = Ae;
      for (D = 1; e < t.length; e++) {
        var r = t[e];
        do
          r = r(!0);
        while (r !== null);
      }
      Ae = null, ul = !1;
    } catch (l) {
      throw Ae !== null && (Ae = Ae.slice(e + 1)), Ns(Zi, hn), l;
    } finally {
      D = n, Fl = !1;
    }
  }
  return null;
}
var Vn = [], Bn = 0, Br = null, Wr = 0, ke = [], Se = 0, Pn = null, Ve = 1, Be = "";
function gn(e, n) {
  Vn[Bn++] = Wr, Vn[Bn++] = Br, Br = e, Wr = n;
}
function ta(e, n, t) {
  ke[Se++] = Ve, ke[Se++] = Be, ke[Se++] = Pn, Pn = e;
  var r = Ve;
  e = Be;
  var l = 32 - je(r) - 1;
  r &= ~(1 << l), t += 1;
  var i = 32 - je(n) + l;
  if (30 < i) {
    var o = l - l % 5;
    i = (r & (1 << o) - 1).toString(32), r >>= o, l -= o, Ve = 1 << 32 - je(n) + l | t << l | r, Be = i + e;
  } else
    Ve = 1 << i | t << l | r, Be = e;
}
function io(e) {
  e.return !== null && (gn(e, 1), ta(e, 1, 0));
}
function oo(e) {
  for (; e === Br; )
    Br = Vn[--Bn], Vn[Bn] = null, Wr = Vn[--Bn], Vn[Bn] = null;
  for (; e === Pn; )
    Pn = ke[--Se], ke[Se] = null, Be = ke[--Se], ke[Se] = null, Ve = ke[--Se], ke[Se] = null;
}
var ve = null, he = null, U = !1, Le = null;
function ra(e, n) {
  var t = xe(5, null, null, 0);
  t.elementType = "DELETED", t.stateNode = n, t.return = e, n = e.deletions, n === null ? (e.deletions = [t], e.flags |= 16) : n.push(t);
}
function vu(e, n) {
  switch (e.tag) {
    case 5:
      var t = e.type;
      return n = n.nodeType !== 1 || t.toLowerCase() !== n.nodeName.toLowerCase() ? null : n, n !== null ? (e.stateNode = n, ve = e, he = on(n.firstChild), !0) : !1;
    case 6:
      return n = e.pendingProps === "" || n.nodeType !== 3 ? null : n, n !== null ? (e.stateNode = n, ve = e, he = null, !0) : !1;
    case 13:
      return n = n.nodeType !== 8 ? null : n, n !== null ? (t = Pn !== null ? { id: Ve, overflow: Be } : null, e.memoizedState = { dehydrated: n, treeContext: t, retryLane: 1073741824 }, t = xe(18, null, null, 0), t.stateNode = n, t.return = e, e.child = t, ve = e, he = null, !0) : !1;
    default:
      return !1;
  }
}
function ki(e) {
  return (e.mode & 1) !== 0 && (e.flags & 128) === 0;
}
function Si(e) {
  if (U) {
    var n = he;
    if (n) {
      var t = n;
      if (!vu(e, n)) {
        if (ki(e))
          throw Error(y(418));
        n = on(t.nextSibling);
        var r = ve;
        n && vu(e, n) ? ra(r, t) : (e.flags = e.flags & -4097 | 2, U = !1, ve = e);
      }
    } else {
      if (ki(e))
        throw Error(y(418));
      e.flags = e.flags & -4097 | 2, U = !1, ve = e;
    }
  }
}
function yu(e) {
  for (e = e.return; e !== null && e.tag !== 5 && e.tag !== 3 && e.tag !== 13; )
    e = e.return;
  ve = e;
}
function pr(e) {
  if (e !== ve)
    return !1;
  if (!U)
    return yu(e), U = !0, !1;
  var n;
  if ((n = e.tag !== 3) && !(n = e.tag !== 5) && (n = e.type, n = n !== "head" && n !== "body" && !vi(e.type, e.memoizedProps)), n && (n = he)) {
    if (ki(e))
      throw la(), Error(y(418));
    for (; n; )
      ra(e, n), n = on(n.nextSibling);
  }
  if (yu(e), e.tag === 13) {
    if (e = e.memoizedState, e = e !== null ? e.dehydrated : null, !e)
      throw Error(y(317));
    e: {
      for (e = e.nextSibling, n = 0; e; ) {
        if (e.nodeType === 8) {
          var t = e.data;
          if (t === "/$") {
            if (n === 0) {
              he = on(e.nextSibling);
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
    he = ve ? on(e.stateNode.nextSibling) : null;
  return !0;
}
function la() {
  for (var e = he; e; )
    e = on(e.nextSibling);
}
function et() {
  he = ve = null, U = !1;
}
function uo(e) {
  Le === null ? Le = [e] : Le.push(e);
}
var ed = Xe.ReactCurrentBatchConfig;
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
function mr(e, n) {
  throw e = Object.prototype.toString.call(n), Error(y(31, e === "[object Object]" ? "object with keys {" + Object.keys(n).join(", ") + "}" : e));
}
function gu(e) {
  var n = e._init;
  return n(e._payload);
}
function ia(e) {
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
    return f = cn(f, a), f.index = 0, f.sibling = null, f;
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
    var x = d.type;
    return x === On ? h(f, a, d.props.children, v, d.key) : a !== null && (a.elementType === x || typeof x == "object" && x !== null && x.$$typeof === Ze && gu(x) === a.type) ? (v = l(a, d.props), v.ref = ht(f, a, d), v.return = f, v) : (v = Lr(d.type, d.key, d.props, null, f.mode, v), v.ref = ht(f, a, d), v.return = f, v);
  }
  function c(f, a, d, v) {
    return a === null || a.tag !== 4 || a.stateNode.containerInfo !== d.containerInfo || a.stateNode.implementation !== d.implementation ? (a = Ql(d, f.mode, v), a.return = f, a) : (a = l(a, d.children || []), a.return = f, a);
  }
  function h(f, a, d, v, x) {
    return a === null || a.tag !== 7 ? (a = _n(d, f.mode, v, x), a.return = f, a) : (a = l(a, d), a.return = f, a);
  }
  function m(f, a, d) {
    if (typeof a == "string" && a !== "" || typeof a == "number")
      return a = Hl("" + a, f.mode, d), a.return = f, a;
    if (typeof a == "object" && a !== null) {
      switch (a.$$typeof) {
        case rr:
          return d = Lr(a.type, a.key, a.props, null, f.mode, d), d.ref = ht(f, null, a), d.return = f, d;
        case Mn:
          return a = Ql(a, f.mode, d), a.return = f, a;
        case Ze:
          var v = a._init;
          return m(f, v(a._payload), d);
      }
      if (kt(a) || ct(a))
        return a = _n(a, f.mode, d, null), a.return = f, a;
      mr(f, a);
    }
    return null;
  }
  function p(f, a, d, v) {
    var x = a !== null ? a.key : null;
    if (typeof d == "string" && d !== "" || typeof d == "number")
      return x !== null ? null : u(f, a, "" + d, v);
    if (typeof d == "object" && d !== null) {
      switch (d.$$typeof) {
        case rr:
          return d.key === x ? s(f, a, d, v) : null;
        case Mn:
          return d.key === x ? c(f, a, d, v) : null;
        case Ze:
          return x = d._init, p(
            f,
            a,
            x(d._payload),
            v
          );
      }
      if (kt(d) || ct(d))
        return x !== null ? null : h(f, a, d, v, null);
      mr(f, d);
    }
    return null;
  }
  function g(f, a, d, v, x) {
    if (typeof v == "string" && v !== "" || typeof v == "number")
      return f = f.get(d) || null, u(a, f, "" + v, x);
    if (typeof v == "object" && v !== null) {
      switch (v.$$typeof) {
        case rr:
          return f = f.get(v.key === null ? d : v.key) || null, s(a, f, v, x);
        case Mn:
          return f = f.get(v.key === null ? d : v.key) || null, c(a, f, v, x);
        case Ze:
          var _ = v._init;
          return g(f, a, d, _(v._payload), x);
      }
      if (kt(v) || ct(v))
        return f = f.get(d) || null, h(a, f, v, x, null);
      mr(a, v);
    }
    return null;
  }
  function w(f, a, d, v) {
    for (var x = null, _ = null, N = a, P = a = 0, W = null; N !== null && P < d.length; P++) {
      N.index > P ? (W = N, N = null) : W = N.sibling;
      var j = p(f, N, d[P], v);
      if (j === null) {
        N === null && (N = W);
        break;
      }
      e && N && j.alternate === null && n(f, N), a = i(j, a, P), _ === null ? x = j : _.sibling = j, _ = j, N = W;
    }
    if (P === d.length)
      return t(f, N), U && gn(f, P), x;
    if (N === null) {
      for (; P < d.length; P++)
        N = m(f, d[P], v), N !== null && (a = i(N, a, P), _ === null ? x = N : _.sibling = N, _ = N);
      return U && gn(f, P), x;
    }
    for (N = r(f, N); P < d.length; P++)
      W = g(N, f, P, d[P], v), W !== null && (e && W.alternate !== null && N.delete(W.key === null ? P : W.key), a = i(W, a, P), _ === null ? x = W : _.sibling = W, _ = W);
    return e && N.forEach(function(Ne) {
      return n(f, Ne);
    }), U && gn(f, P), x;
  }
  function k(f, a, d, v) {
    var x = ct(d);
    if (typeof x != "function")
      throw Error(y(150));
    if (d = x.call(d), d == null)
      throw Error(y(151));
    for (var _ = x = null, N = a, P = a = 0, W = null, j = d.next(); N !== null && !j.done; P++, j = d.next()) {
      N.index > P ? (W = N, N = null) : W = N.sibling;
      var Ne = p(f, N, j.value, v);
      if (Ne === null) {
        N === null && (N = W);
        break;
      }
      e && N && Ne.alternate === null && n(f, N), a = i(Ne, a, P), _ === null ? x = Ne : _.sibling = Ne, _ = Ne, N = W;
    }
    if (j.done)
      return t(
        f,
        N
      ), U && gn(f, P), x;
    if (N === null) {
      for (; !j.done; P++, j = d.next())
        j = m(f, j.value, v), j !== null && (a = i(j, a, P), _ === null ? x = j : _.sibling = j, _ = j);
      return U && gn(f, P), x;
    }
    for (N = r(f, N); !j.done; P++, j = d.next())
      j = g(N, f, P, j.value, v), j !== null && (e && j.alternate !== null && N.delete(j.key === null ? P : j.key), a = i(j, a, P), _ === null ? x = j : _.sibling = j, _ = j);
    return e && N.forEach(function(st) {
      return n(f, st);
    }), U && gn(f, P), x;
  }
  function F(f, a, d, v) {
    if (typeof d == "object" && d !== null && d.type === On && d.key === null && (d = d.props.children), typeof d == "object" && d !== null) {
      switch (d.$$typeof) {
        case rr:
          e: {
            for (var x = d.key, _ = a; _ !== null; ) {
              if (_.key === x) {
                if (x = d.type, x === On) {
                  if (_.tag === 7) {
                    t(f, _.sibling), a = l(_, d.props.children), a.return = f, f = a;
                    break e;
                  }
                } else if (_.elementType === x || typeof x == "object" && x !== null && x.$$typeof === Ze && gu(x) === _.type) {
                  t(f, _.sibling), a = l(_, d.props), a.ref = ht(f, _, d), a.return = f, f = a;
                  break e;
                }
                t(f, _);
                break;
              } else
                n(f, _);
              _ = _.sibling;
            }
            d.type === On ? (a = _n(d.props.children, f.mode, v, d.key), a.return = f, f = a) : (v = Lr(d.type, d.key, d.props, null, f.mode, v), v.ref = ht(f, a, d), v.return = f, f = v);
          }
          return o(f);
        case Mn:
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
            a = Ql(d, f.mode, v), a.return = f, f = a;
          }
          return o(f);
        case Ze:
          return _ = d._init, F(f, a, _(d._payload), v);
      }
      if (kt(d))
        return w(f, a, d, v);
      if (ct(d))
        return k(f, a, d, v);
      mr(f, d);
    }
    return typeof d == "string" && d !== "" || typeof d == "number" ? (d = "" + d, a !== null && a.tag === 6 ? (t(f, a.sibling), a = l(a, d), a.return = f, f = a) : (t(f, a), a = Hl(d, f.mode, v), a.return = f, f = a), o(f)) : t(f, a);
  }
  return F;
}
var nt = ia(!0), oa = ia(!1), Hr = mn(null), Qr = null, Wn = null, so = null;
function ao() {
  so = Wn = Qr = null;
}
function co(e) {
  var n = Hr.current;
  I(Hr), e._currentValue = n;
}
function xi(e, n, t) {
  for (; e !== null; ) {
    var r = e.alternate;
    if ((e.childLanes & n) !== n ? (e.childLanes |= n, r !== null && (r.childLanes |= n)) : r !== null && (r.childLanes & n) !== n && (r.childLanes |= n), e === t)
      break;
    e = e.return;
  }
}
function Zn(e, n) {
  Qr = e, so = Wn = null, e = e.dependencies, e !== null && e.firstContext !== null && (e.lanes & n && (ce = !0), e.firstContext = null);
}
function Ce(e) {
  var n = e._currentValue;
  if (so !== e)
    if (e = { context: e, memoizedValue: n, next: null }, Wn === null) {
      if (Qr === null)
        throw Error(y(308));
      Wn = e, Qr.dependencies = { lanes: 0, firstContext: e };
    } else
      Wn = Wn.next = e;
  return n;
}
var xn = null;
function fo(e) {
  xn === null ? xn = [e] : xn.push(e);
}
function ua(e, n, t, r) {
  var l = n.interleaved;
  return l === null ? (t.next = t, fo(n)) : (t.next = l.next, l.next = t), n.interleaved = t, Ke(e, r);
}
function Ke(e, n) {
  e.lanes |= n;
  var t = e.alternate;
  for (t !== null && (t.lanes |= n), t = e, e = e.return; e !== null; )
    e.childLanes |= n, t = e.alternate, t !== null && (t.childLanes |= n), t = e, e = e.return;
  return t.tag === 3 ? t.stateNode : null;
}
var Je = !1;
function po(e) {
  e.updateQueue = { baseState: e.memoizedState, firstBaseUpdate: null, lastBaseUpdate: null, shared: { pending: null, interleaved: null, lanes: 0 }, effects: null };
}
function sa(e, n) {
  e = e.updateQueue, n.updateQueue === e && (n.updateQueue = { baseState: e.baseState, firstBaseUpdate: e.firstBaseUpdate, lastBaseUpdate: e.lastBaseUpdate, shared: e.shared, effects: e.effects });
}
function We(e, n) {
  return { eventTime: e, lane: n, tag: 0, payload: null, callback: null, next: null };
}
function un(e, n, t) {
  var r = e.updateQueue;
  if (r === null)
    return null;
  if (r = r.shared, R & 2) {
    var l = r.pending;
    return l === null ? n.next = n : (n.next = l.next, l.next = n), r.pending = n, Ke(e, t);
  }
  return l = r.interleaved, l === null ? (n.next = n, fo(r)) : (n.next = l.next, l.next = n), r.interleaved = n, Ke(e, t);
}
function Cr(e, n, t) {
  if (n = n.updateQueue, n !== null && (n = n.shared, (t & 4194240) !== 0)) {
    var r = n.lanes;
    r &= e.pendingLanes, t |= r, n.lanes = t, Ji(e, t);
  }
}
function wu(e, n) {
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
function Kr(e, n, t, r) {
  var l = e.updateQueue;
  Je = !1;
  var i = l.firstBaseUpdate, o = l.lastBaseUpdate, u = l.shared.pending;
  if (u !== null) {
    l.shared.pending = null;
    var s = u, c = s.next;
    s.next = null, o === null ? i = c : o.next = c, o = s;
    var h = e.alternate;
    h !== null && (h = h.updateQueue, u = h.lastBaseUpdate, u !== o && (u === null ? h.firstBaseUpdate = c : u.next = c, h.lastBaseUpdate = s));
  }
  if (i !== null) {
    var m = l.baseState;
    o = 0, h = c = s = null, u = i;
    do {
      var p = u.lane, g = u.eventTime;
      if ((r & p) === p) {
        h !== null && (h = h.next = {
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
                m = w.call(g, m, p);
                break e;
              }
              m = w;
              break e;
            case 3:
              w.flags = w.flags & -65537 | 128;
            case 0:
              if (w = k.payload, p = typeof w == "function" ? w.call(g, m, p) : w, p == null)
                break e;
              m = V({}, m, p);
              break e;
            case 2:
              Je = !0;
          }
        }
        u.callback !== null && u.lane !== 0 && (e.flags |= 64, p = l.effects, p === null ? l.effects = [u] : p.push(u));
      } else
        g = { eventTime: g, lane: p, tag: u.tag, payload: u.payload, callback: u.callback, next: null }, h === null ? (c = h = g, s = m) : h = h.next = g, o |= p;
      if (u = u.next, u === null) {
        if (u = l.shared.pending, u === null)
          break;
        p = u, u = p.next, p.next = null, l.lastBaseUpdate = p, l.shared.pending = null;
      }
    } while (1);
    if (h === null && (s = m), l.baseState = s, l.firstBaseUpdate = c, l.lastBaseUpdate = h, n = l.shared.interleaved, n !== null) {
      l = n;
      do
        o |= l.lane, l = l.next;
      while (l !== n);
    } else
      i === null && (l.shared.lanes = 0);
    Tn |= o, e.lanes = o, e.memoizedState = m;
  }
}
function ku(e, n, t) {
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
var bt = {}, Ue = mn(bt), Wt = mn(bt), Ht = mn(bt);
function En(e) {
  if (e === bt)
    throw Error(y(174));
  return e;
}
function mo(e, n) {
  switch (M(Ht, n), M(Wt, e), M(Ue, bt), e = n.nodeType, e) {
    case 9:
    case 11:
      n = (n = n.documentElement) ? n.namespaceURI : ti(null, "");
      break;
    default:
      e = e === 8 ? n.parentNode : n, n = e.namespaceURI || null, e = e.tagName, n = ti(n, e);
  }
  I(Ue), M(Ue, n);
}
function tt() {
  I(Ue), I(Wt), I(Ht);
}
function aa(e) {
  En(Ht.current);
  var n = En(Ue.current), t = ti(n, e.type);
  n !== t && (M(Wt, e), M(Ue, t));
}
function ho(e) {
  Wt.current === e && (I(Ue), I(Wt));
}
var $ = mn(0);
function Yr(e) {
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
var Ul = [];
function vo() {
  for (var e = 0; e < Ul.length; e++)
    Ul[e]._workInProgressVersionPrimary = null;
  Ul.length = 0;
}
var _r = Xe.ReactCurrentDispatcher, $l = Xe.ReactCurrentBatchConfig, zn = 0, A = null, Y = null, Z = null, Xr = !1, zt = !1, Qt = 0, nd = 0;
function ne() {
  throw Error(y(321));
}
function yo(e, n) {
  if (n === null)
    return !1;
  for (var t = 0; t < n.length && t < e.length; t++)
    if (!De(e[t], n[t]))
      return !1;
  return !0;
}
function go(e, n, t, r, l, i) {
  if (zn = i, A = n, n.memoizedState = null, n.updateQueue = null, n.lanes = 0, _r.current = e === null || e.memoizedState === null ? id : od, e = t(r, l), zt) {
    i = 0;
    do {
      if (zt = !1, Qt = 0, 25 <= i)
        throw Error(y(301));
      i += 1, Z = Y = null, n.updateQueue = null, _r.current = ud, e = t(r, l);
    } while (zt);
  }
  if (_r.current = Gr, n = Y !== null && Y.next !== null, zn = 0, Z = Y = A = null, Xr = !1, n)
    throw Error(y(300));
  return e;
}
function wo() {
  var e = Qt !== 0;
  return Qt = 0, e;
}
function Oe() {
  var e = { memoizedState: null, baseState: null, baseQueue: null, queue: null, next: null };
  return Z === null ? A.memoizedState = Z = e : Z = Z.next = e, Z;
}
function _e() {
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
function Kt(e, n) {
  return typeof n == "function" ? n(e) : n;
}
function Al(e) {
  var n = _e(), t = n.queue;
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
      var h = c.lane;
      if ((zn & h) === h)
        s !== null && (s = s.next = { lane: 0, action: c.action, hasEagerState: c.hasEagerState, eagerState: c.eagerState, next: null }), r = c.hasEagerState ? c.eagerState : e(r, c.action);
      else {
        var m = {
          lane: h,
          action: c.action,
          hasEagerState: c.hasEagerState,
          eagerState: c.eagerState,
          next: null
        };
        s === null ? (u = s = m, o = r) : s = s.next = m, A.lanes |= h, Tn |= h;
      }
      c = c.next;
    } while (c !== null && c !== i);
    s === null ? o = r : s.next = u, De(r, n.memoizedState) || (ce = !0), n.memoizedState = r, n.baseState = o, n.baseQueue = s, t.lastRenderedState = r;
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
function Vl(e) {
  var n = _e(), t = n.queue;
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
    De(i, n.memoizedState) || (ce = !0), n.memoizedState = i, n.baseQueue === null && (n.baseState = i), t.lastRenderedState = i;
  }
  return [i, r];
}
function ca() {
}
function fa(e, n) {
  var t = A, r = _e(), l = n(), i = !De(r.memoizedState, l);
  if (i && (r.memoizedState = l, ce = !0), r = r.queue, ko(ma.bind(null, t, r, e), [e]), r.getSnapshot !== n || i || Z !== null && Z.memoizedState.tag & 1) {
    if (t.flags |= 2048, Yt(9, pa.bind(null, t, r, l, n), void 0, null), J === null)
      throw Error(y(349));
    zn & 30 || da(t, n, l);
  }
  return l;
}
function da(e, n, t) {
  e.flags |= 16384, e = { getSnapshot: n, value: t }, n = A.updateQueue, n === null ? (n = { lastEffect: null, stores: null }, A.updateQueue = n, n.stores = [e]) : (t = n.stores, t === null ? n.stores = [e] : t.push(e));
}
function pa(e, n, t, r) {
  n.value = t, n.getSnapshot = r, ha(n) && va(e);
}
function ma(e, n, t) {
  return t(function() {
    ha(n) && va(e);
  });
}
function ha(e) {
  var n = e.getSnapshot;
  e = e.value;
  try {
    var t = n();
    return !De(e, t);
  } catch {
    return !0;
  }
}
function va(e) {
  var n = Ke(e, 1);
  n !== null && Re(n, e, 1, -1);
}
function Su(e) {
  var n = Oe();
  return typeof e == "function" && (e = e()), n.memoizedState = n.baseState = e, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: Kt, lastRenderedState: e }, n.queue = e, e = e.dispatch = ld.bind(null, A, e), [n.memoizedState, e];
}
function Yt(e, n, t, r) {
  return e = { tag: e, create: n, destroy: t, deps: r, next: null }, n = A.updateQueue, n === null ? (n = { lastEffect: null, stores: null }, A.updateQueue = n, n.lastEffect = e.next = e) : (t = n.lastEffect, t === null ? n.lastEffect = e.next = e : (r = t.next, t.next = e, e.next = r, n.lastEffect = e)), e;
}
function ya() {
  return _e().memoizedState;
}
function Nr(e, n, t, r) {
  var l = Oe();
  A.flags |= e, l.memoizedState = Yt(1 | n, t, void 0, r === void 0 ? null : r);
}
function sl(e, n, t, r) {
  var l = _e();
  r = r === void 0 ? null : r;
  var i = void 0;
  if (Y !== null) {
    var o = Y.memoizedState;
    if (i = o.destroy, r !== null && yo(r, o.deps)) {
      l.memoizedState = Yt(n, t, i, r);
      return;
    }
  }
  A.flags |= e, l.memoizedState = Yt(1 | n, t, i, r);
}
function xu(e, n) {
  return Nr(8390656, 8, e, n);
}
function ko(e, n) {
  return sl(2048, 8, e, n);
}
function ga(e, n) {
  return sl(4, 2, e, n);
}
function wa(e, n) {
  return sl(4, 4, e, n);
}
function ka(e, n) {
  if (typeof n == "function")
    return e = e(), n(e), function() {
      n(null);
    };
  if (n != null)
    return e = e(), n.current = e, function() {
      n.current = null;
    };
}
function Sa(e, n, t) {
  return t = t != null ? t.concat([e]) : null, sl(4, 4, ka.bind(null, n, e), t);
}
function So() {
}
function xa(e, n) {
  var t = _e();
  n = n === void 0 ? null : n;
  var r = t.memoizedState;
  return r !== null && n !== null && yo(n, r[1]) ? r[0] : (t.memoizedState = [e, n], e);
}
function Ea(e, n) {
  var t = _e();
  n = n === void 0 ? null : n;
  var r = t.memoizedState;
  return r !== null && n !== null && yo(n, r[1]) ? r[0] : (e = e(), t.memoizedState = [e, n], e);
}
function Ca(e, n, t) {
  return zn & 21 ? (De(t, n) || (t = Ts(), A.lanes |= t, Tn |= t, e.baseState = !0), n) : (e.baseState && (e.baseState = !1, ce = !0), e.memoizedState = t);
}
function td(e, n) {
  var t = D;
  D = t !== 0 && 4 > t ? t : 4, e(!0);
  var r = $l.transition;
  $l.transition = {};
  try {
    e(!1), n();
  } finally {
    D = t, $l.transition = r;
  }
}
function _a() {
  return _e().memoizedState;
}
function rd(e, n, t) {
  var r = an(e);
  if (t = { lane: r, action: t, hasEagerState: !1, eagerState: null, next: null }, Na(e))
    Pa(n, t);
  else if (t = ua(e, n, t, r), t !== null) {
    var l = oe();
    Re(t, e, r, l), za(t, n, r);
  }
}
function ld(e, n, t) {
  var r = an(e), l = { lane: r, action: t, hasEagerState: !1, eagerState: null, next: null };
  if (Na(e))
    Pa(n, l);
  else {
    var i = e.alternate;
    if (e.lanes === 0 && (i === null || i.lanes === 0) && (i = n.lastRenderedReducer, i !== null))
      try {
        var o = n.lastRenderedState, u = i(o, t);
        if (l.hasEagerState = !0, l.eagerState = u, De(u, o)) {
          var s = n.interleaved;
          s === null ? (l.next = l, fo(n)) : (l.next = s.next, s.next = l), n.interleaved = l;
          return;
        }
      } catch {
      } finally {
      }
    t = ua(e, n, l, r), t !== null && (l = oe(), Re(t, e, r, l), za(t, n, r));
  }
}
function Na(e) {
  var n = e.alternate;
  return e === A || n !== null && n === A;
}
function Pa(e, n) {
  zt = Xr = !0;
  var t = e.pending;
  t === null ? n.next = n : (n.next = t.next, t.next = n), e.pending = n;
}
function za(e, n, t) {
  if (t & 4194240) {
    var r = n.lanes;
    r &= e.pendingLanes, t |= r, n.lanes = t, Ji(e, t);
  }
}
var Gr = { readContext: Ce, useCallback: ne, useContext: ne, useEffect: ne, useImperativeHandle: ne, useInsertionEffect: ne, useLayoutEffect: ne, useMemo: ne, useReducer: ne, useRef: ne, useState: ne, useDebugValue: ne, useDeferredValue: ne, useTransition: ne, useMutableSource: ne, useSyncExternalStore: ne, useId: ne, unstable_isNewReconciler: !1 }, id = { readContext: Ce, useCallback: function(e, n) {
  return Oe().memoizedState = [e, n === void 0 ? null : n], e;
}, useContext: Ce, useEffect: xu, useImperativeHandle: function(e, n, t) {
  return t = t != null ? t.concat([e]) : null, Nr(
    4194308,
    4,
    ka.bind(null, n, e),
    t
  );
}, useLayoutEffect: function(e, n) {
  return Nr(4194308, 4, e, n);
}, useInsertionEffect: function(e, n) {
  return Nr(4, 2, e, n);
}, useMemo: function(e, n) {
  var t = Oe();
  return n = n === void 0 ? null : n, e = e(), t.memoizedState = [e, n], e;
}, useReducer: function(e, n, t) {
  var r = Oe();
  return n = t !== void 0 ? t(n) : n, r.memoizedState = r.baseState = n, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: e, lastRenderedState: n }, r.queue = e, e = e.dispatch = rd.bind(null, A, e), [r.memoizedState, e];
}, useRef: function(e) {
  var n = Oe();
  return e = { current: e }, n.memoizedState = e;
}, useState: Su, useDebugValue: So, useDeferredValue: function(e) {
  return Oe().memoizedState = e;
}, useTransition: function() {
  var e = Su(!1), n = e[0];
  return e = td.bind(null, e[1]), Oe().memoizedState = e, [n, e];
}, useMutableSource: function() {
}, useSyncExternalStore: function(e, n, t) {
  var r = A, l = Oe();
  if (U) {
    if (t === void 0)
      throw Error(y(407));
    t = t();
  } else {
    if (t = n(), J === null)
      throw Error(y(349));
    zn & 30 || da(r, n, t);
  }
  l.memoizedState = t;
  var i = { value: t, getSnapshot: n };
  return l.queue = i, xu(ma.bind(
    null,
    r,
    i,
    e
  ), [e]), r.flags |= 2048, Yt(9, pa.bind(null, r, i, t, n), void 0, null), t;
}, useId: function() {
  var e = Oe(), n = J.identifierPrefix;
  if (U) {
    var t = Be, r = Ve;
    t = (r & ~(1 << 32 - je(r) - 1)).toString(32) + t, n = ":" + n + "R" + t, t = Qt++, 0 < t && (n += "H" + t.toString(32)), n += ":";
  } else
    t = nd++, n = ":" + n + "r" + t.toString(32) + ":";
  return e.memoizedState = n;
}, unstable_isNewReconciler: !1 }, od = {
  readContext: Ce,
  useCallback: xa,
  useContext: Ce,
  useEffect: ko,
  useImperativeHandle: Sa,
  useInsertionEffect: ga,
  useLayoutEffect: wa,
  useMemo: Ea,
  useReducer: Al,
  useRef: ya,
  useState: function() {
    return Al(Kt);
  },
  useDebugValue: So,
  useDeferredValue: function(e) {
    var n = _e();
    return Ca(n, Y.memoizedState, e);
  },
  useTransition: function() {
    var e = Al(Kt)[0], n = _e().memoizedState;
    return [e, n];
  },
  useMutableSource: ca,
  useSyncExternalStore: fa,
  useId: _a,
  unstable_isNewReconciler: !1
}, ud = { readContext: Ce, useCallback: xa, useContext: Ce, useEffect: ko, useImperativeHandle: Sa, useInsertionEffect: ga, useLayoutEffect: wa, useMemo: Ea, useReducer: Vl, useRef: ya, useState: function() {
  return Vl(Kt);
}, useDebugValue: So, useDeferredValue: function(e) {
  var n = _e();
  return Y === null ? n.memoizedState = e : Ca(n, Y.memoizedState, e);
}, useTransition: function() {
  var e = Vl(Kt)[0], n = _e().memoizedState;
  return [e, n];
}, useMutableSource: ca, useSyncExternalStore: fa, useId: _a, unstable_isNewReconciler: !1 };
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
var al = { isMounted: function(e) {
  return (e = e._reactInternals) ? Rn(e) === e : !1;
}, enqueueSetState: function(e, n, t) {
  e = e._reactInternals;
  var r = oe(), l = an(e), i = We(r, l);
  i.payload = n, t != null && (i.callback = t), n = un(e, i, l), n !== null && (Re(n, e, l, r), Cr(n, e, l));
}, enqueueReplaceState: function(e, n, t) {
  e = e._reactInternals;
  var r = oe(), l = an(e), i = We(r, l);
  i.tag = 1, i.payload = n, t != null && (i.callback = t), n = un(e, i, l), n !== null && (Re(n, e, l, r), Cr(n, e, l));
}, enqueueForceUpdate: function(e, n) {
  e = e._reactInternals;
  var t = oe(), r = an(e), l = We(t, r);
  l.tag = 2, n != null && (l.callback = n), n = un(e, l, r), n !== null && (Re(n, e, r, t), Cr(n, e, r));
} };
function Eu(e, n, t, r, l, i, o) {
  return e = e.stateNode, typeof e.shouldComponentUpdate == "function" ? e.shouldComponentUpdate(r, i, o) : n.prototype && n.prototype.isPureReactComponent ? !$t(t, r) || !$t(l, i) : !0;
}
function Ta(e, n, t) {
  var r = !1, l = dn, i = n.contextType;
  return typeof i == "object" && i !== null ? i = Ce(i) : (l = de(n) ? Nn : le.current, r = n.contextTypes, i = (r = r != null) ? bn(e, l) : dn), n = new n(t, i), e.memoizedState = n.state !== null && n.state !== void 0 ? n.state : null, n.updater = al, e.stateNode = n, n._reactInternals = e, r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = l, e.__reactInternalMemoizedMaskedChildContext = i), n;
}
function Cu(e, n, t, r) {
  e = n.state, typeof n.componentWillReceiveProps == "function" && n.componentWillReceiveProps(t, r), typeof n.UNSAFE_componentWillReceiveProps == "function" && n.UNSAFE_componentWillReceiveProps(t, r), n.state !== e && al.enqueueReplaceState(n, n.state, null);
}
function Ci(e, n, t, r) {
  var l = e.stateNode;
  l.props = t, l.state = e.memoizedState, l.refs = {}, po(e);
  var i = n.contextType;
  typeof i == "object" && i !== null ? l.context = Ce(i) : (i = de(n) ? Nn : le.current, l.context = bn(e, i)), l.state = e.memoizedState, i = n.getDerivedStateFromProps, typeof i == "function" && (Ei(e, n, i, t), l.state = e.memoizedState), typeof n.getDerivedStateFromProps == "function" || typeof l.getSnapshotBeforeUpdate == "function" || typeof l.UNSAFE_componentWillMount != "function" && typeof l.componentWillMount != "function" || (n = l.state, typeof l.componentWillMount == "function" && l.componentWillMount(), typeof l.UNSAFE_componentWillMount == "function" && l.UNSAFE_componentWillMount(), n !== l.state && al.enqueueReplaceState(l, l.state, null), Kr(e, t, l, r), l.state = e.memoizedState), typeof l.componentDidMount == "function" && (e.flags |= 4194308);
}
function rt(e, n) {
  try {
    var t = "", r = n;
    do
      t += Mc(r), r = r.return;
    while (r);
    var l = t;
  } catch (i) {
    l = `
Error generating stack: ` + i.message + `
` + i.stack;
  }
  return { value: e, source: n, stack: l, digest: null };
}
function Bl(e, n, t) {
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
var sd = typeof WeakMap == "function" ? WeakMap : Map;
function La(e, n, t) {
  t = We(-1, t), t.tag = 3, t.payload = { element: null };
  var r = n.value;
  return t.callback = function() {
    Jr || (Jr = !0, Oi = r), _i(e, n);
  }, t;
}
function ja(e, n, t) {
  t = We(-1, t), t.tag = 3;
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
    _i(e, n), typeof r != "function" && (sn === null ? sn = /* @__PURE__ */ new Set([this]) : sn.add(this));
    var o = n.stack;
    this.componentDidCatch(n.value, { componentStack: o !== null ? o : "" });
  }), t;
}
function _u(e, n, t) {
  var r = e.pingCache;
  if (r === null) {
    r = e.pingCache = new sd();
    var l = /* @__PURE__ */ new Set();
    r.set(n, l);
  } else
    l = r.get(n), l === void 0 && (l = /* @__PURE__ */ new Set(), r.set(n, l));
  l.has(t) || (l.add(t), e = xd.bind(null, e, n, t), n.then(e, e));
}
function Nu(e) {
  do {
    var n;
    if ((n = e.tag === 13) && (n = e.memoizedState, n = n !== null ? n.dehydrated !== null : !0), n)
      return e;
    e = e.return;
  } while (e !== null);
  return null;
}
function Pu(e, n, t, r, l) {
  return e.mode & 1 ? (e.flags |= 65536, e.lanes = l, e) : (e === n ? e.flags |= 65536 : (e.flags |= 128, t.flags |= 131072, t.flags &= -52805, t.tag === 1 && (t.alternate === null ? t.tag = 17 : (n = We(-1, 1), n.tag = 2, un(t, n, 1))), t.lanes |= 1), e);
}
var ad = Xe.ReactCurrentOwner, ce = !1;
function ie(e, n, t, r) {
  n.child = e === null ? oa(n, null, t, r) : nt(n, e.child, t, r);
}
function zu(e, n, t, r, l) {
  t = t.render;
  var i = n.ref;
  return Zn(n, l), r = go(e, n, t, r, i, l), t = wo(), e !== null && !ce ? (n.updateQueue = e.updateQueue, n.flags &= -2053, e.lanes &= ~l, Ye(e, n, l)) : (U && t && io(n), n.flags |= 1, ie(e, n, r, l), n.child);
}
function Tu(e, n, t, r, l) {
  if (e === null) {
    var i = t.type;
    return typeof i == "function" && !To(i) && i.defaultProps === void 0 && t.compare === null && t.defaultProps === void 0 ? (n.tag = 15, n.type = i, Ra(e, n, i, r, l)) : (e = Lr(t.type, null, r, n, n.mode, l), e.ref = n.ref, e.return = n, n.child = e);
  }
  if (i = e.child, !(e.lanes & l)) {
    var o = i.memoizedProps;
    if (t = t.compare, t = t !== null ? t : $t, t(o, r) && e.ref === n.ref)
      return Ye(e, n, l);
  }
  return n.flags |= 1, e = cn(i, r), e.ref = n.ref, e.return = n, n.child = e;
}
function Ra(e, n, t, r, l) {
  if (e !== null) {
    var i = e.memoizedProps;
    if ($t(i, r) && e.ref === n.ref)
      if (ce = !1, n.pendingProps = r = i, (e.lanes & l) !== 0)
        e.flags & 131072 && (ce = !0);
      else
        return n.lanes = e.lanes, Ye(e, n, l);
  }
  return Ni(e, n, t, r, l);
}
function Da(e, n, t) {
  var r = n.pendingProps, l = r.children, i = e !== null ? e.memoizedState : null;
  if (r.mode === "hidden")
    if (!(n.mode & 1))
      n.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, M(Qn, me), me |= t;
    else {
      if (!(t & 1073741824))
        return e = i !== null ? i.baseLanes | t : t, n.lanes = n.childLanes = 1073741824, n.memoizedState = { baseLanes: e, cachePool: null, transitions: null }, n.updateQueue = null, M(Qn, me), me |= e, null;
      n.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, r = i !== null ? i.baseLanes : t, M(Qn, me), me |= r;
    }
  else
    i !== null ? (r = i.baseLanes | t, n.memoizedState = null) : r = t, M(Qn, me), me |= r;
  return ie(e, n, l, t), n.child;
}
function Ma(e, n) {
  var t = n.ref;
  (e === null && t !== null || e !== null && e.ref !== t) && (n.flags |= 512, n.flags |= 2097152);
}
function Ni(e, n, t, r, l) {
  var i = de(t) ? Nn : le.current;
  return i = bn(n, i), Zn(n, l), t = go(e, n, t, r, i, l), r = wo(), e !== null && !ce ? (n.updateQueue = e.updateQueue, n.flags &= -2053, e.lanes &= ~l, Ye(e, n, l)) : (U && r && io(n), n.flags |= 1, ie(e, n, t, l), n.child);
}
function Lu(e, n, t, r, l) {
  if (de(t)) {
    var i = !0;
    Vr(n);
  } else
    i = !1;
  if (Zn(n, l), n.stateNode === null)
    Pr(e, n), Ta(n, t, r), Ci(n, t, r, l), r = !0;
  else if (e === null) {
    var o = n.stateNode, u = n.memoizedProps;
    o.props = u;
    var s = o.context, c = t.contextType;
    typeof c == "object" && c !== null ? c = Ce(c) : (c = de(t) ? Nn : le.current, c = bn(n, c));
    var h = t.getDerivedStateFromProps, m = typeof h == "function" || typeof o.getSnapshotBeforeUpdate == "function";
    m || typeof o.UNSAFE_componentWillReceiveProps != "function" && typeof o.componentWillReceiveProps != "function" || (u !== r || s !== c) && Cu(n, o, r, c), Je = !1;
    var p = n.memoizedState;
    o.state = p, Kr(n, r, o, l), s = n.memoizedState, u !== r || p !== s || fe.current || Je ? (typeof h == "function" && (Ei(n, t, h, r), s = n.memoizedState), (u = Je || Eu(n, t, u, r, p, s, c)) ? (m || typeof o.UNSAFE_componentWillMount != "function" && typeof o.componentWillMount != "function" || (typeof o.componentWillMount == "function" && o.componentWillMount(), typeof o.UNSAFE_componentWillMount == "function" && o.UNSAFE_componentWillMount()), typeof o.componentDidMount == "function" && (n.flags |= 4194308)) : (typeof o.componentDidMount == "function" && (n.flags |= 4194308), n.memoizedProps = r, n.memoizedState = s), o.props = r, o.state = s, o.context = c, r = u) : (typeof o.componentDidMount == "function" && (n.flags |= 4194308), r = !1);
  } else {
    o = n.stateNode, sa(e, n), u = n.memoizedProps, c = n.type === n.elementType ? u : ze(n.type, u), o.props = c, m = n.pendingProps, p = o.context, s = t.contextType, typeof s == "object" && s !== null ? s = Ce(s) : (s = de(t) ? Nn : le.current, s = bn(n, s));
    var g = t.getDerivedStateFromProps;
    (h = typeof g == "function" || typeof o.getSnapshotBeforeUpdate == "function") || typeof o.UNSAFE_componentWillReceiveProps != "function" && typeof o.componentWillReceiveProps != "function" || (u !== m || p !== s) && Cu(n, o, r, s), Je = !1, p = n.memoizedState, o.state = p, Kr(n, r, o, l);
    var w = n.memoizedState;
    u !== m || p !== w || fe.current || Je ? (typeof g == "function" && (Ei(n, t, g, r), w = n.memoizedState), (c = Je || Eu(n, t, c, r, p, w, s) || !1) ? (h || typeof o.UNSAFE_componentWillUpdate != "function" && typeof o.componentWillUpdate != "function" || (typeof o.componentWillUpdate == "function" && o.componentWillUpdate(r, w, s), typeof o.UNSAFE_componentWillUpdate == "function" && o.UNSAFE_componentWillUpdate(r, w, s)), typeof o.componentDidUpdate == "function" && (n.flags |= 4), typeof o.getSnapshotBeforeUpdate == "function" && (n.flags |= 1024)) : (typeof o.componentDidUpdate != "function" || u === e.memoizedProps && p === e.memoizedState || (n.flags |= 4), typeof o.getSnapshotBeforeUpdate != "function" || u === e.memoizedProps && p === e.memoizedState || (n.flags |= 1024), n.memoizedProps = r, n.memoizedState = w), o.props = r, o.state = w, o.context = s, r = c) : (typeof o.componentDidUpdate != "function" || u === e.memoizedProps && p === e.memoizedState || (n.flags |= 4), typeof o.getSnapshotBeforeUpdate != "function" || u === e.memoizedProps && p === e.memoizedState || (n.flags |= 1024), r = !1);
  }
  return Pi(e, n, t, r, i, l);
}
function Pi(e, n, t, r, l, i) {
  Ma(e, n);
  var o = (n.flags & 128) !== 0;
  if (!r && !o)
    return l && hu(n, t, !1), Ye(e, n, i);
  r = n.stateNode, ad.current = n;
  var u = o && typeof t.getDerivedStateFromError != "function" ? null : r.render();
  return n.flags |= 1, e !== null && o ? (n.child = nt(n, e.child, null, i), n.child = nt(n, null, u, i)) : ie(e, n, u, i), n.memoizedState = r.state, l && hu(n, t, !0), n.child;
}
function Oa(e) {
  var n = e.stateNode;
  n.pendingContext ? mu(e, n.pendingContext, n.pendingContext !== n.context) : n.context && mu(e, n.context, !1), mo(e, n.containerInfo);
}
function ju(e, n, t, r, l) {
  return et(), uo(l), n.flags |= 256, ie(e, n, t, r), n.child;
}
var zi = { dehydrated: null, treeContext: null, retryLane: 0 };
function Ti(e) {
  return { baseLanes: e, cachePool: null, transitions: null };
}
function Ia(e, n, t) {
  var r = n.pendingProps, l = $.current, i = !1, o = (n.flags & 128) !== 0, u;
  if ((u = o) || (u = e !== null && e.memoizedState === null ? !1 : (l & 2) !== 0), u ? (i = !0, n.flags &= -129) : (e === null || e.memoizedState !== null) && (l |= 1), M($, l & 1), e === null)
    return Si(n), e = n.memoizedState, e !== null && (e = e.dehydrated, e !== null) ? (n.mode & 1 ? e.data === "$!" ? n.lanes = 8 : n.lanes = 1073741824 : n.lanes = 1, null) : (o = r.children, e = r.fallback, i ? (r = n.mode, i = n.child, o = { mode: "hidden", children: o }, !(r & 1) && i !== null ? (i.childLanes = 0, i.pendingProps = o) : i = dl(o, r, 0, null), e = _n(e, r, t, null), i.return = n, e.return = n, i.sibling = e, n.child = i, n.child.memoizedState = Ti(t), n.memoizedState = zi, e) : xo(n, o));
  if (l = e.memoizedState, l !== null && (u = l.dehydrated, u !== null))
    return cd(e, n, o, r, u, l, t);
  if (i) {
    i = r.fallback, o = n.mode, l = e.child, u = l.sibling;
    var s = { mode: "hidden", children: r.children };
    return !(o & 1) && n.child !== l ? (r = n.child, r.childLanes = 0, r.pendingProps = s, n.deletions = null) : (r = cn(l, s), r.subtreeFlags = l.subtreeFlags & 14680064), u !== null ? i = cn(u, i) : (i = _n(i, o, t, null), i.flags |= 2), i.return = n, r.return = n, r.sibling = i, n.child = r, r = i, i = n.child, o = e.child.memoizedState, o = o === null ? Ti(t) : { baseLanes: o.baseLanes | t, cachePool: null, transitions: o.transitions }, i.memoizedState = o, i.childLanes = e.childLanes & ~t, n.memoizedState = zi, r;
  }
  return i = e.child, e = i.sibling, r = cn(i, { mode: "visible", children: r.children }), !(n.mode & 1) && (r.lanes = t), r.return = n, r.sibling = null, e !== null && (t = n.deletions, t === null ? (n.deletions = [e], n.flags |= 16) : t.push(e)), n.child = r, n.memoizedState = null, r;
}
function xo(e, n) {
  return n = dl({ mode: "visible", children: n }, e.mode, 0, null), n.return = e, e.child = n;
}
function hr(e, n, t, r) {
  return r !== null && uo(r), nt(n, e.child, null, t), e = xo(n, n.pendingProps.children), e.flags |= 2, n.memoizedState = null, e;
}
function cd(e, n, t, r, l, i, o) {
  if (t)
    return n.flags & 256 ? (n.flags &= -257, r = Bl(Error(y(422))), hr(e, n, o, r)) : n.memoizedState !== null ? (n.child = e.child, n.flags |= 128, null) : (i = r.fallback, l = n.mode, r = dl({ mode: "visible", children: r.children }, l, 0, null), i = _n(i, l, o, null), i.flags |= 2, r.return = n, i.return = n, r.sibling = i, n.child = r, n.mode & 1 && nt(n, e.child, null, o), n.child.memoizedState = Ti(o), n.memoizedState = zi, i);
  if (!(n.mode & 1))
    return hr(e, n, o, null);
  if (l.data === "$!") {
    if (r = l.nextSibling && l.nextSibling.dataset, r)
      var u = r.dgst;
    return r = u, i = Error(y(419)), r = Bl(i, r, void 0), hr(e, n, o, r);
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
      l = l & (r.suspendedLanes | o) ? 0 : l, l !== 0 && l !== i.retryLane && (i.retryLane = l, Ke(e, l), Re(r, e, l, -1));
    }
    return zo(), r = Bl(Error(y(421))), hr(e, n, o, r);
  }
  return l.data === "$?" ? (n.flags |= 128, n.child = e.child, n = Ed.bind(null, e), l._reactRetry = n, null) : (e = i.treeContext, he = on(l.nextSibling), ve = n, U = !0, Le = null, e !== null && (ke[Se++] = Ve, ke[Se++] = Be, ke[Se++] = Pn, Ve = e.id, Be = e.overflow, Pn = n), n = xo(n, r.children), n.flags |= 4096, n);
}
function Ru(e, n, t) {
  e.lanes |= n;
  var r = e.alternate;
  r !== null && (r.lanes |= n), xi(e.return, n, t);
}
function Wl(e, n, t, r, l) {
  var i = e.memoizedState;
  i === null ? e.memoizedState = { isBackwards: n, rendering: null, renderingStartTime: 0, last: r, tail: t, tailMode: l } : (i.isBackwards = n, i.rendering = null, i.renderingStartTime = 0, i.last = r, i.tail = t, i.tailMode = l);
}
function Fa(e, n, t) {
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
  if (M($, r), !(n.mode & 1))
    n.memoizedState = null;
  else
    switch (l) {
      case "forwards":
        for (t = n.child, l = null; t !== null; )
          e = t.alternate, e !== null && Yr(e) === null && (l = t), t = t.sibling;
        t = l, t === null ? (l = n.child, n.child = null) : (l = t.sibling, t.sibling = null), Wl(n, !1, l, t, i);
        break;
      case "backwards":
        for (t = null, l = n.child, n.child = null; l !== null; ) {
          if (e = l.alternate, e !== null && Yr(e) === null) {
            n.child = l;
            break;
          }
          e = l.sibling, l.sibling = t, t = l, l = e;
        }
        Wl(n, !0, t, null, i);
        break;
      case "together":
        Wl(n, !1, null, null, void 0);
        break;
      default:
        n.memoizedState = null;
    }
  return n.child;
}
function Pr(e, n) {
  !(n.mode & 1) && e !== null && (e.alternate = null, n.alternate = null, n.flags |= 2);
}
function Ye(e, n, t) {
  if (e !== null && (n.dependencies = e.dependencies), Tn |= n.lanes, !(t & n.childLanes))
    return null;
  if (e !== null && n.child !== e.child)
    throw Error(y(153));
  if (n.child !== null) {
    for (e = n.child, t = cn(e, e.pendingProps), n.child = t, t.return = n; e.sibling !== null; )
      e = e.sibling, t = t.sibling = cn(e, e.pendingProps), t.return = n;
    t.sibling = null;
  }
  return n.child;
}
function fd(e, n, t) {
  switch (n.tag) {
    case 3:
      Oa(n), et();
      break;
    case 5:
      aa(n);
      break;
    case 1:
      de(n.type) && Vr(n);
      break;
    case 4:
      mo(n, n.stateNode.containerInfo);
      break;
    case 10:
      var r = n.type._context, l = n.memoizedProps.value;
      M(Hr, r._currentValue), r._currentValue = l;
      break;
    case 13:
      if (r = n.memoizedState, r !== null)
        return r.dehydrated !== null ? (M($, $.current & 1), n.flags |= 128, null) : t & n.child.childLanes ? Ia(e, n, t) : (M($, $.current & 1), e = Ye(e, n, t), e !== null ? e.sibling : null);
      M($, $.current & 1);
      break;
    case 19:
      if (r = (t & n.childLanes) !== 0, e.flags & 128) {
        if (r)
          return Fa(e, n, t);
        n.flags |= 128;
      }
      if (l = n.memoizedState, l !== null && (l.rendering = null, l.tail = null, l.lastEffect = null), M($, $.current), r)
        break;
      return null;
    case 22:
    case 23:
      return n.lanes = 0, Da(e, n, t);
  }
  return Ye(e, n, t);
}
var Ua, Li, $a, Aa;
Ua = function(e, n) {
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
Li = function() {
};
$a = function(e, n, t, r) {
  var l = e.memoizedProps;
  if (l !== r) {
    e = n.stateNode, En(Ue.current);
    var i = null;
    switch (t) {
      case "input":
        l = ql(e, l), r = ql(e, r), i = [];
        break;
      case "select":
        l = V({}, l, { value: void 0 }), r = V({}, r, { value: void 0 }), i = [];
        break;
      case "textarea":
        l = ni(e, l), r = ni(e, r), i = [];
        break;
      default:
        typeof l.onClick != "function" && typeof r.onClick == "function" && (e.onclick = $r);
    }
    ri(t, r);
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
          c === "dangerouslySetInnerHTML" ? (s = s ? s.__html : void 0, u = u ? u.__html : void 0, s != null && u !== s && (i = i || []).push(c, s)) : c === "children" ? typeof s != "string" && typeof s != "number" || (i = i || []).push(c, "" + s) : c !== "suppressContentEditableWarning" && c !== "suppressHydrationWarning" && (Rt.hasOwnProperty(c) ? (s != null && c === "onScroll" && O("scroll", e), i || u === s || (i = [])) : (i = i || []).push(c, s));
    }
    t && (i = i || []).push("style", t);
    var c = i;
    (n.updateQueue = c) && (n.flags |= 4);
  }
};
Aa = function(e, n, t, r) {
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
function dd(e, n, t) {
  var r = n.pendingProps;
  switch (oo(n), n.tag) {
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
      return de(n.type) && Ar(), te(n), null;
    case 3:
      return r = n.stateNode, tt(), I(fe), I(le), vo(), r.pendingContext && (r.context = r.pendingContext, r.pendingContext = null), (e === null || e.child === null) && (pr(n) ? n.flags |= 4 : e === null || e.memoizedState.isDehydrated && !(n.flags & 256) || (n.flags |= 1024, Le !== null && (Ui(Le), Le = null))), Li(e, n), te(n), null;
    case 5:
      ho(n);
      var l = En(Ht.current);
      if (t = n.type, e !== null && n.stateNode != null)
        $a(e, n, t, r, l), e.ref !== n.ref && (n.flags |= 512, n.flags |= 2097152);
      else {
        if (!r) {
          if (n.stateNode === null)
            throw Error(y(166));
          return te(n), null;
        }
        if (e = En(Ue.current), pr(n)) {
          r = n.stateNode, t = n.type;
          var i = n.memoizedProps;
          switch (r[Ie] = n, r[Bt] = i, e = (n.mode & 1) !== 0, t) {
            case "dialog":
              O("cancel", r), O("close", r);
              break;
            case "iframe":
            case "object":
            case "embed":
              O("load", r);
              break;
            case "video":
            case "audio":
              for (l = 0; l < xt.length; l++)
                O(xt[l], r);
              break;
            case "source":
              O("error", r);
              break;
            case "img":
            case "image":
            case "link":
              O(
                "error",
                r
              ), O("load", r);
              break;
            case "details":
              O("toggle", r);
              break;
            case "input":
              Vo(r, i), O("invalid", r);
              break;
            case "select":
              r._wrapperState = { wasMultiple: !!i.multiple }, O("invalid", r);
              break;
            case "textarea":
              Wo(r, i), O("invalid", r);
          }
          ri(t, i), l = null;
          for (var o in i)
            if (i.hasOwnProperty(o)) {
              var u = i[o];
              o === "children" ? typeof u == "string" ? r.textContent !== u && (i.suppressHydrationWarning !== !0 && dr(r.textContent, u, e), l = ["children", u]) : typeof u == "number" && r.textContent !== "" + u && (i.suppressHydrationWarning !== !0 && dr(
                r.textContent,
                u,
                e
              ), l = ["children", "" + u]) : Rt.hasOwnProperty(o) && u != null && o === "onScroll" && O("scroll", r);
            }
          switch (t) {
            case "input":
              lr(r), Bo(r, i, !0);
              break;
            case "textarea":
              lr(r), Ho(r);
              break;
            case "select":
            case "option":
              break;
            default:
              typeof i.onClick == "function" && (r.onclick = $r);
          }
          r = l, n.updateQueue = r, r !== null && (n.flags |= 4);
        } else {
          o = l.nodeType === 9 ? l : l.ownerDocument, e === "http://www.w3.org/1999/xhtml" && (e = ms(t)), e === "http://www.w3.org/1999/xhtml" ? t === "script" ? (e = o.createElement("div"), e.innerHTML = "<script><\/script>", e = e.removeChild(e.firstChild)) : typeof r.is == "string" ? e = o.createElement(t, { is: r.is }) : (e = o.createElement(t), t === "select" && (o = e, r.multiple ? o.multiple = !0 : r.size && (o.size = r.size))) : e = o.createElementNS(e, t), e[Ie] = n, e[Bt] = r, Ua(e, n, !1, !1), n.stateNode = e;
          e: {
            switch (o = li(t, r), t) {
              case "dialog":
                O("cancel", e), O("close", e), l = r;
                break;
              case "iframe":
              case "object":
              case "embed":
                O("load", e), l = r;
                break;
              case "video":
              case "audio":
                for (l = 0; l < xt.length; l++)
                  O(xt[l], e);
                l = r;
                break;
              case "source":
                O("error", e), l = r;
                break;
              case "img":
              case "image":
              case "link":
                O(
                  "error",
                  e
                ), O("load", e), l = r;
                break;
              case "details":
                O("toggle", e), l = r;
                break;
              case "input":
                Vo(e, r), l = ql(e, r), O("invalid", e);
                break;
              case "option":
                l = r;
                break;
              case "select":
                e._wrapperState = { wasMultiple: !!r.multiple }, l = V({}, r, { value: void 0 }), O("invalid", e);
                break;
              case "textarea":
                Wo(e, r), l = ni(e, r), O("invalid", e);
                break;
              default:
                l = r;
            }
            ri(t, l), u = l;
            for (i in u)
              if (u.hasOwnProperty(i)) {
                var s = u[i];
                i === "style" ? ys(e, s) : i === "dangerouslySetInnerHTML" ? (s = s ? s.__html : void 0, s != null && hs(e, s)) : i === "children" ? typeof s == "string" ? (t !== "textarea" || s !== "") && Dt(e, s) : typeof s == "number" && Dt(e, "" + s) : i !== "suppressContentEditableWarning" && i !== "suppressHydrationWarning" && i !== "autoFocus" && (Rt.hasOwnProperty(i) ? s != null && i === "onScroll" && O("scroll", e) : s != null && Qi(e, i, s, o));
              }
            switch (t) {
              case "input":
                lr(e), Bo(e, r, !1);
                break;
              case "textarea":
                lr(e), Ho(e);
                break;
              case "option":
                r.value != null && e.setAttribute("value", "" + fn(r.value));
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
                typeof l.onClick == "function" && (e.onclick = $r);
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
        Aa(e, n, e.memoizedProps, r);
      else {
        if (typeof r != "string" && n.stateNode === null)
          throw Error(y(166));
        if (t = En(Ht.current), En(Ue.current), pr(n)) {
          if (r = n.stateNode, t = n.memoizedProps, r[Ie] = n, (i = r.nodeValue !== t) && (e = ve, e !== null))
            switch (e.tag) {
              case 3:
                dr(r.nodeValue, t, (e.mode & 1) !== 0);
                break;
              case 5:
                e.memoizedProps.suppressHydrationWarning !== !0 && dr(r.nodeValue, t, (e.mode & 1) !== 0);
            }
          i && (n.flags |= 4);
        } else
          r = (t.nodeType === 9 ? t : t.ownerDocument).createTextNode(r), r[Ie] = n, n.stateNode = r;
      }
      return te(n), null;
    case 13:
      if (I($), r = n.memoizedState, e === null || e.memoizedState !== null && e.memoizedState.dehydrated !== null) {
        if (U && he !== null && n.mode & 1 && !(n.flags & 128))
          la(), et(), n.flags |= 98560, i = !1;
        else if (i = pr(n), r !== null && r.dehydrated !== null) {
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
          Le !== null && (Ui(Le), Le = null), i = !0;
        if (!i)
          return n.flags & 65536 ? n : null;
      }
      return n.flags & 128 ? (n.lanes = t, n) : (r = r !== null, r !== (e !== null && e.memoizedState !== null) && r && (n.child.flags |= 8192, n.mode & 1 && (e === null || $.current & 1 ? X === 0 && (X = 3) : zo())), n.updateQueue !== null && (n.flags |= 4), te(n), null);
    case 4:
      return tt(), Li(e, n), e === null && At(n.stateNode.containerInfo), te(n), null;
    case 10:
      return co(n.type._context), te(n), null;
    case 17:
      return de(n.type) && Ar(), te(n), null;
    case 19:
      if (I($), i = n.memoizedState, i === null)
        return te(n), null;
      if (r = (n.flags & 128) !== 0, o = i.rendering, o === null)
        if (r)
          vt(i, !1);
        else {
          if (X !== 0 || e !== null && e.flags & 128)
            for (e = n.child; e !== null; ) {
              if (o = Yr(e), o !== null) {
                for (n.flags |= 128, vt(i, !1), r = o.updateQueue, r !== null && (n.updateQueue = r, n.flags |= 4), n.subtreeFlags = 0, r = t, t = n.child; t !== null; )
                  i = t, e = r, i.flags &= 14680066, o = i.alternate, o === null ? (i.childLanes = 0, i.lanes = e, i.child = null, i.subtreeFlags = 0, i.memoizedProps = null, i.memoizedState = null, i.updateQueue = null, i.dependencies = null, i.stateNode = null) : (i.childLanes = o.childLanes, i.lanes = o.lanes, i.child = o.child, i.subtreeFlags = 0, i.deletions = null, i.memoizedProps = o.memoizedProps, i.memoizedState = o.memoizedState, i.updateQueue = o.updateQueue, i.type = o.type, e = o.dependencies, i.dependencies = e === null ? null : { lanes: e.lanes, firstContext: e.firstContext }), t = t.sibling;
                return M($, $.current & 1 | 2), n.child;
              }
              e = e.sibling;
            }
          i.tail !== null && Q() > lt && (n.flags |= 128, r = !0, vt(i, !1), n.lanes = 4194304);
        }
      else {
        if (!r)
          if (e = Yr(o), e !== null) {
            if (n.flags |= 128, r = !0, t = e.updateQueue, t !== null && (n.updateQueue = t, n.flags |= 4), vt(i, !0), i.tail === null && i.tailMode === "hidden" && !o.alternate && !U)
              return te(n), null;
          } else
            2 * Q() - i.renderingStartTime > lt && t !== 1073741824 && (n.flags |= 128, r = !0, vt(i, !1), n.lanes = 4194304);
        i.isBackwards ? (o.sibling = n.child, n.child = o) : (t = i.last, t !== null ? t.sibling = o : n.child = o, i.last = o);
      }
      return i.tail !== null ? (n = i.tail, i.rendering = n, i.tail = n.sibling, i.renderingStartTime = Q(), n.sibling = null, t = $.current, M($, r ? t & 1 | 2 : t & 1), n) : (te(n), null);
    case 22:
    case 23:
      return Po(), r = n.memoizedState !== null, e !== null && e.memoizedState !== null !== r && (n.flags |= 8192), r && n.mode & 1 ? me & 1073741824 && (te(n), n.subtreeFlags & 6 && (n.flags |= 8192)) : te(n), null;
    case 24:
      return null;
    case 25:
      return null;
  }
  throw Error(y(156, n.tag));
}
function pd(e, n) {
  switch (oo(n), n.tag) {
    case 1:
      return de(n.type) && Ar(), e = n.flags, e & 65536 ? (n.flags = e & -65537 | 128, n) : null;
    case 3:
      return tt(), I(fe), I(le), vo(), e = n.flags, e & 65536 && !(e & 128) ? (n.flags = e & -65537 | 128, n) : null;
    case 5:
      return ho(n), null;
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
      return co(n.type._context), null;
    case 22:
    case 23:
      return Po(), null;
    case 24:
      return null;
    default:
      return null;
  }
}
var vr = !1, re = !1, md = typeof WeakSet == "function" ? WeakSet : Set, S = null;
function Hn(e, n) {
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
function ji(e, n, t) {
  try {
    t();
  } catch (r) {
    B(e, n, r);
  }
}
var Du = !1;
function hd(e, n) {
  if (mi = Ir, e = Qs(), lo(e)) {
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
          var o = 0, u = -1, s = -1, c = 0, h = 0, m = e, p = null;
          n:
            for (; ; ) {
              for (var g; m !== t || l !== 0 && m.nodeType !== 3 || (u = o + l), m !== i || r !== 0 && m.nodeType !== 3 || (s = o + r), m.nodeType === 3 && (o += m.nodeValue.length), (g = m.firstChild) !== null; )
                p = m, m = g;
              for (; ; ) {
                if (m === e)
                  break n;
                if (p === t && ++c === l && (u = o), p === i && ++h === r && (s = o), (g = m.nextSibling) !== null)
                  break;
                m = p, p = m.parentNode;
              }
              m = g;
            }
          t = u === -1 || s === -1 ? null : { start: u, end: s };
        } else
          t = null;
      }
    t = t || { start: 0, end: 0 };
  } else
    t = null;
  for (hi = { focusedElem: e, selectionRange: t }, Ir = !1, S = n; S !== null; )
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
  return w = Du, Du = !1, w;
}
function Tt(e, n, t) {
  var r = n.updateQueue;
  if (r = r !== null ? r.lastEffect : null, r !== null) {
    var l = r = r.next;
    do {
      if ((l.tag & e) === e) {
        var i = l.destroy;
        l.destroy = void 0, i !== void 0 && ji(n, t, i);
      }
      l = l.next;
    } while (l !== r);
  }
}
function cl(e, n) {
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
function Va(e) {
  var n = e.alternate;
  n !== null && (e.alternate = null, Va(n)), e.child = null, e.deletions = null, e.sibling = null, e.tag === 5 && (n = e.stateNode, n !== null && (delete n[Ie], delete n[Bt], delete n[gi], delete n[Jf], delete n[qf])), e.stateNode = null, e.return = null, e.dependencies = null, e.memoizedProps = null, e.memoizedState = null, e.pendingProps = null, e.stateNode = null, e.updateQueue = null;
}
function Ba(e) {
  return e.tag === 5 || e.tag === 3 || e.tag === 4;
}
function Mu(e) {
  e:
    for (; ; ) {
      for (; e.sibling === null; ) {
        if (e.return === null || Ba(e.return))
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
function Di(e, n, t) {
  var r = e.tag;
  if (r === 5 || r === 6)
    e = e.stateNode, n ? t.nodeType === 8 ? t.parentNode.insertBefore(e, n) : t.insertBefore(e, n) : (t.nodeType === 8 ? (n = t.parentNode, n.insertBefore(e, t)) : (n = t, n.appendChild(e)), t = t._reactRootContainer, t != null || n.onclick !== null || (n.onclick = $r));
  else if (r !== 4 && (e = e.child, e !== null))
    for (Di(e, n, t), e = e.sibling; e !== null; )
      Di(e, n, t), e = e.sibling;
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
    Wa(e, n, t), t = t.sibling;
}
function Wa(e, n, t) {
  if (Fe && typeof Fe.onCommitFiberUnmount == "function")
    try {
      Fe.onCommitFiberUnmount(tl, t);
    } catch {
    }
  switch (t.tag) {
    case 5:
      re || Hn(t, n);
    case 6:
      var r = q, l = Te;
      q = null, Ge(e, n, t), q = r, Te = l, q !== null && (Te ? (e = q, t = t.stateNode, e.nodeType === 8 ? e.parentNode.removeChild(t) : e.removeChild(t)) : q.removeChild(t.stateNode));
      break;
    case 18:
      q !== null && (Te ? (e = q, t = t.stateNode, e.nodeType === 8 ? Il(e.parentNode, t) : e.nodeType === 1 && Il(e, t), Ft(e)) : Il(q, t.stateNode));
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
          i = i.tag, o !== void 0 && (i & 2 || i & 4) && ji(t, n, o), l = l.next;
        } while (l !== r);
      }
      Ge(e, n, t);
      break;
    case 1:
      if (!re && (Hn(t, n), r = t.stateNode, typeof r.componentWillUnmount == "function"))
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
    t === null && (t = e.stateNode = new md()), n.forEach(function(r) {
      var l = Cd.bind(null, e, r);
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
        Wa(i, o, l), q = null, Te = !1;
        var s = l.alternate;
        s !== null && (s.return = null), l.return = null;
      } catch (c) {
        B(l, n, c);
      }
    }
  if (n.subtreeFlags & 12854)
    for (n = n.child; n !== null; )
      Ha(n, e), n = n.sibling;
}
function Ha(e, n) {
  var t = e.alternate, r = e.flags;
  switch (e.tag) {
    case 0:
    case 11:
    case 14:
    case 15:
      if (Pe(n, e), Me(e), r & 4) {
        try {
          Tt(3, e, e.return), cl(3, e);
        } catch (k) {
          B(e, e.return, k);
        }
        try {
          Tt(5, e, e.return);
        } catch (k) {
          B(e, e.return, k);
        }
      }
      break;
    case 1:
      Pe(n, e), Me(e), r & 512 && t !== null && Hn(t, t.return);
      break;
    case 5:
      if (Pe(n, e), Me(e), r & 512 && t !== null && Hn(t, t.return), e.flags & 32) {
        var l = e.stateNode;
        try {
          Dt(l, "");
        } catch (k) {
          B(e, e.return, k);
        }
      }
      if (r & 4 && (l = e.stateNode, l != null)) {
        var i = e.memoizedProps, o = t !== null ? t.memoizedProps : i, u = e.type, s = e.updateQueue;
        if (e.updateQueue = null, s !== null)
          try {
            u === "input" && i.type === "radio" && i.name != null && ds(l, i), li(u, o);
            var c = li(u, i);
            for (o = 0; o < s.length; o += 2) {
              var h = s[o], m = s[o + 1];
              h === "style" ? ys(l, m) : h === "dangerouslySetInnerHTML" ? hs(l, m) : h === "children" ? Dt(l, m) : Qi(l, h, m, c);
            }
            switch (u) {
              case "input":
                bl(l, i);
                break;
              case "textarea":
                ps(l, i);
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
            l[Bt] = i;
          } catch (k) {
            B(e, e.return, k);
          }
      }
      break;
    case 6:
      if (Pe(n, e), Me(e), r & 4) {
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
      if (Pe(n, e), Me(e), r & 4 && t !== null && t.memoizedState.isDehydrated)
        try {
          Ft(n.containerInfo);
        } catch (k) {
          B(e, e.return, k);
        }
      break;
    case 4:
      Pe(n, e), Me(e);
      break;
    case 13:
      Pe(n, e), Me(e), l = e.child, l.flags & 8192 && (i = l.memoizedState !== null, l.stateNode.isHidden = i, !i || l.alternate !== null && l.alternate.memoizedState !== null || (_o = Q())), r & 4 && Ou(e);
      break;
    case 22:
      if (h = t !== null && t.memoizedState !== null, e.mode & 1 ? (re = (c = re) || h, Pe(n, e), re = c) : Pe(n, e), Me(e), r & 8192) {
        if (c = e.memoizedState !== null, (e.stateNode.isHidden = c) && !h && e.mode & 1)
          for (S = e, h = e.child; h !== null; ) {
            for (m = S = h; S !== null; ) {
              switch (p = S, g = p.child, p.tag) {
                case 0:
                case 11:
                case 14:
                case 15:
                  Tt(4, p, p.return);
                  break;
                case 1:
                  Hn(p, p.return);
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
                  Hn(p, p.return);
                  break;
                case 22:
                  if (p.memoizedState !== null) {
                    Fu(m);
                    continue;
                  }
              }
              g !== null ? (g.return = p, S = g) : Fu(m);
            }
            h = h.sibling;
          }
        e:
          for (h = null, m = e; ; ) {
            if (m.tag === 5) {
              if (h === null) {
                h = m;
                try {
                  l = m.stateNode, c ? (i = l.style, typeof i.setProperty == "function" ? i.setProperty("display", "none", "important") : i.display = "none") : (u = m.stateNode, s = m.memoizedProps.style, o = s != null && s.hasOwnProperty("display") ? s.display : null, u.style.display = vs("display", o));
                } catch (k) {
                  B(e, e.return, k);
                }
              }
            } else if (m.tag === 6) {
              if (h === null)
                try {
                  m.stateNode.nodeValue = c ? "" : m.memoizedProps;
                } catch (k) {
                  B(e, e.return, k);
                }
            } else if ((m.tag !== 22 && m.tag !== 23 || m.memoizedState === null || m === e) && m.child !== null) {
              m.child.return = m, m = m.child;
              continue;
            }
            if (m === e)
              break e;
            for (; m.sibling === null; ) {
              if (m.return === null || m.return === e)
                break e;
              h === m && (h = null), m = m.return;
            }
            h === m && (h = null), m.sibling.return = m.return, m = m.sibling;
          }
      }
      break;
    case 19:
      Pe(n, e), Me(e), r & 4 && Ou(e);
      break;
    case 21:
      break;
    default:
      Pe(
        n,
        e
      ), Me(e);
  }
}
function Me(e) {
  var n = e.flags;
  if (n & 2) {
    try {
      e: {
        for (var t = e.return; t !== null; ) {
          if (Ba(t)) {
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
          r.flags & 32 && (Dt(l, ""), r.flags &= -33);
          var i = Mu(e);
          Mi(e, i, l);
          break;
        case 3:
        case 4:
          var o = r.stateNode.containerInfo, u = Mu(e);
          Di(e, u, o);
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
function vd(e, n, t) {
  S = e, Qa(e);
}
function Qa(e, n, t) {
  for (var r = (e.mode & 1) !== 0; S !== null; ) {
    var l = S, i = l.child;
    if (l.tag === 22 && r) {
      var o = l.memoizedState !== null || vr;
      if (!o) {
        var u = l.alternate, s = u !== null && u.memoizedState !== null || re;
        u = vr;
        var c = re;
        if (vr = o, (re = s) && !c)
          for (S = l; S !== null; )
            o = S, s = o.child, o.tag === 22 && o.memoizedState !== null ? Uu(l) : s !== null ? (s.return = o, S = s) : Uu(l);
        for (; i !== null; )
          S = i, Qa(i), i = i.sibling;
        S = l, vr = u, re = c;
      }
      Iu(e);
    } else
      l.subtreeFlags & 8772 && i !== null ? (i.return = l, S = i) : Iu(e);
  }
}
function Iu(e) {
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
              re || cl(5, n);
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
              i !== null && ku(n, i, r);
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
                ku(n, o, t);
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
                  var h = c.memoizedState;
                  if (h !== null) {
                    var m = h.dehydrated;
                    m !== null && Ft(m);
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
function Fu(e) {
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
function Uu(e) {
  for (; S !== null; ) {
    var n = S;
    try {
      switch (n.tag) {
        case 0:
        case 11:
        case 15:
          var t = n.return;
          try {
            cl(4, n);
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
var yd = Math.ceil, Zr = Xe.ReactCurrentDispatcher, Eo = Xe.ReactCurrentOwner, Ee = Xe.ReactCurrentBatchConfig, R = 0, J = null, K = null, b = 0, me = 0, Qn = mn(0), X = 0, Xt = null, Tn = 0, fl = 0, Co = 0, Lt = null, ae = null, _o = 0, lt = 1 / 0, $e = null, Jr = !1, Oi = null, sn = null, yr = !1, nn = null, qr = 0, jt = 0, Ii = null, zr = -1, Tr = 0;
function oe() {
  return R & 6 ? Q() : zr !== -1 ? zr : zr = Q();
}
function an(e) {
  return e.mode & 1 ? R & 2 && b !== 0 ? b & -b : ed.transition !== null ? (Tr === 0 && (Tr = Ts()), Tr) : (e = D, e !== 0 || (e = window.event, e = e === void 0 ? 16 : Is(e.type)), e) : 1;
}
function Re(e, n, t, r) {
  if (50 < jt)
    throw jt = 0, Ii = null, Error(y(185));
  Zt(e, t, r), (!(R & 2) || e !== J) && (e === J && (!(R & 2) && (fl |= t), X === 4 && be(e, b)), pe(e, r), t === 1 && R === 0 && !(n.mode & 1) && (lt = Q() + 500, ul && hn()));
}
function pe(e, n) {
  var t = e.callbackNode;
  bc(e, n);
  var r = Or(e, e === J ? b : 0);
  if (r === 0)
    t !== null && Yo(t), e.callbackNode = null, e.callbackPriority = 0;
  else if (n = r & -r, e.callbackPriority !== n) {
    if (t != null && Yo(t), n === 1)
      e.tag === 0 ? bf($u.bind(null, e)) : na($u.bind(null, e)), Gf(function() {
        !(R & 6) && hn();
      }), t = null;
    else {
      switch (Ls(r)) {
        case 1:
          t = Zi;
          break;
        case 4:
          t = Ps;
          break;
        case 16:
          t = Mr;
          break;
        case 536870912:
          t = zs;
          break;
        default:
          t = Mr;
      }
      t = ba(t, Ka.bind(null, e));
    }
    e.callbackPriority = n, e.callbackNode = t;
  }
}
function Ka(e, n) {
  if (zr = -1, Tr = 0, R & 6)
    throw Error(y(327));
  var t = e.callbackNode;
  if (Jn() && e.callbackNode !== t)
    return null;
  var r = Or(e, e === J ? b : 0);
  if (r === 0)
    return null;
  if (r & 30 || r & e.expiredLanes || n)
    n = br(e, r);
  else {
    n = r;
    var l = R;
    R |= 2;
    var i = Xa();
    (J !== e || b !== n) && ($e = null, lt = Q() + 500, Cn(e, n));
    do
      try {
        kd();
        break;
      } catch (u) {
        Ya(e, u);
      }
    while (1);
    ao(), Zr.current = i, R = l, K !== null ? n = 0 : (J = null, b = 0, n = X);
  }
  if (n !== 0) {
    if (n === 2 && (l = ai(e), l !== 0 && (r = l, n = Fi(e, l))), n === 1)
      throw t = Xt, Cn(e, 0), be(e, r), pe(e, Q()), t;
    if (n === 6)
      be(e, r);
    else {
      if (l = e.current.alternate, !(r & 30) && !gd(l) && (n = br(e, r), n === 2 && (i = ai(e), i !== 0 && (r = i, n = Fi(e, i))), n === 1))
        throw t = Xt, Cn(e, 0), be(e, r), pe(e, Q()), t;
      switch (e.finishedWork = l, e.finishedLanes = r, n) {
        case 0:
        case 1:
          throw Error(y(345));
        case 2:
          wn(e, ae, $e);
          break;
        case 3:
          if (be(e, r), (r & 130023424) === r && (n = _o + 500 - Q(), 10 < n)) {
            if (Or(e, 0) !== 0)
              break;
            if (l = e.suspendedLanes, (l & r) !== r) {
              oe(), e.pingedLanes |= e.suspendedLanes & l;
              break;
            }
            e.timeoutHandle = yi(wn.bind(null, e, ae, $e), n);
            break;
          }
          wn(e, ae, $e);
          break;
        case 4:
          if (be(e, r), (r & 4194240) === r)
            break;
          for (n = e.eventTimes, l = -1; 0 < r; ) {
            var o = 31 - je(r);
            i = 1 << o, o = n[o], o > l && (l = o), r &= ~i;
          }
          if (r = l, r = Q() - r, r = (120 > r ? 120 : 480 > r ? 480 : 1080 > r ? 1080 : 1920 > r ? 1920 : 3e3 > r ? 3e3 : 4320 > r ? 4320 : 1960 * yd(r / 1960)) - r, 10 < r) {
            e.timeoutHandle = yi(wn.bind(null, e, ae, $e), r);
            break;
          }
          wn(e, ae, $e);
          break;
        case 5:
          wn(e, ae, $e);
          break;
        default:
          throw Error(y(329));
      }
    }
  }
  return pe(e, Q()), e.callbackNode === t ? Ka.bind(null, e) : null;
}
function Fi(e, n) {
  var t = Lt;
  return e.current.memoizedState.isDehydrated && (Cn(e, n).flags |= 256), e = br(e, n), e !== 2 && (n = ae, ae = t, n !== null && Ui(n)), e;
}
function Ui(e) {
  ae === null ? ae = e : ae.push.apply(ae, e);
}
function gd(e) {
  for (var n = e; ; ) {
    if (n.flags & 16384) {
      var t = n.updateQueue;
      if (t !== null && (t = t.stores, t !== null))
        for (var r = 0; r < t.length; r++) {
          var l = t[r], i = l.getSnapshot;
          l = l.value;
          try {
            if (!De(i(), l))
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
  for (n &= ~Co, n &= ~fl, e.suspendedLanes |= n, e.pingedLanes &= ~n, e = e.expirationTimes; 0 < n; ) {
    var t = 31 - je(n), r = 1 << t;
    e[t] = -1, n &= ~r;
  }
}
function $u(e) {
  if (R & 6)
    throw Error(y(327));
  Jn();
  var n = Or(e, 0);
  if (!(n & 1))
    return pe(e, Q()), null;
  var t = br(e, n);
  if (e.tag !== 0 && t === 2) {
    var r = ai(e);
    r !== 0 && (n = r, t = Fi(e, r));
  }
  if (t === 1)
    throw t = Xt, Cn(e, 0), be(e, n), pe(e, Q()), t;
  if (t === 6)
    throw Error(y(345));
  return e.finishedWork = e.current.alternate, e.finishedLanes = n, wn(e, ae, $e), pe(e, Q()), null;
}
function No(e, n) {
  var t = R;
  R |= 1;
  try {
    return e(n);
  } finally {
    R = t, R === 0 && (lt = Q() + 500, ul && hn());
  }
}
function Ln(e) {
  nn !== null && nn.tag === 0 && !(R & 6) && Jn();
  var n = R;
  R |= 1;
  var t = Ee.transition, r = D;
  try {
    if (Ee.transition = null, D = 1, e)
      return e();
  } finally {
    D = r, Ee.transition = t, R = n, !(R & 6) && hn();
  }
}
function Po() {
  me = Qn.current, I(Qn);
}
function Cn(e, n) {
  e.finishedWork = null, e.finishedLanes = 0;
  var t = e.timeoutHandle;
  if (t !== -1 && (e.timeoutHandle = -1, Xf(t)), K !== null)
    for (t = K.return; t !== null; ) {
      var r = t;
      switch (oo(r), r.tag) {
        case 1:
          r = r.type.childContextTypes, r != null && Ar();
          break;
        case 3:
          tt(), I(fe), I(le), vo();
          break;
        case 5:
          ho(r);
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
          co(r.type._context);
          break;
        case 22:
        case 23:
          Po();
      }
      t = t.return;
    }
  if (J = e, K = e = cn(e.current, null), b = me = n, X = 0, Xt = null, Co = fl = Tn = 0, ae = Lt = null, xn !== null) {
    for (n = 0; n < xn.length; n++)
      if (t = xn[n], r = t.interleaved, r !== null) {
        t.interleaved = null;
        var l = r.next, i = t.pending;
        if (i !== null) {
          var o = i.next;
          i.next = l, r.next = o;
        }
        t.pending = r;
      }
    xn = null;
  }
  return e;
}
function Ya(e, n) {
  do {
    var t = K;
    try {
      if (ao(), _r.current = Gr, Xr) {
        for (var r = A.memoizedState; r !== null; ) {
          var l = r.queue;
          l !== null && (l.pending = null), r = r.next;
        }
        Xr = !1;
      }
      if (zn = 0, Z = Y = A = null, zt = !1, Qt = 0, Eo.current = null, t === null || t.return === null) {
        X = 1, Xt = n, K = null;
        break;
      }
      e: {
        var i = e, o = t.return, u = t, s = n;
        if (n = b, u.flags |= 32768, s !== null && typeof s == "object" && typeof s.then == "function") {
          var c = s, h = u, m = h.tag;
          if (!(h.mode & 1) && (m === 0 || m === 11 || m === 15)) {
            var p = h.alternate;
            p ? (h.updateQueue = p.updateQueue, h.memoizedState = p.memoizedState, h.lanes = p.lanes) : (h.updateQueue = null, h.memoizedState = null);
          }
          var g = Nu(o);
          if (g !== null) {
            g.flags &= -257, Pu(g, o, u, i, n), g.mode & 1 && _u(i, c, n), n = g, s = c;
            var w = n.updateQueue;
            if (w === null) {
              var k = /* @__PURE__ */ new Set();
              k.add(s), n.updateQueue = k;
            } else
              w.add(s);
            break e;
          } else {
            if (!(n & 1)) {
              _u(i, c, n), zo();
              break e;
            }
            s = Error(y(426));
          }
        } else if (U && u.mode & 1) {
          var F = Nu(o);
          if (F !== null) {
            !(F.flags & 65536) && (F.flags |= 256), Pu(F, o, u, i, n), uo(rt(s, u));
            break e;
          }
        }
        i = s = rt(s, u), X !== 4 && (X = 2), Lt === null ? Lt = [i] : Lt.push(i), i = o;
        do {
          switch (i.tag) {
            case 3:
              i.flags |= 65536, n &= -n, i.lanes |= n;
              var f = La(i, s, n);
              wu(i, f);
              break e;
            case 1:
              u = s;
              var a = i.type, d = i.stateNode;
              if (!(i.flags & 128) && (typeof a.getDerivedStateFromError == "function" || d !== null && typeof d.componentDidCatch == "function" && (sn === null || !sn.has(d)))) {
                i.flags |= 65536, n &= -n, i.lanes |= n;
                var v = ja(i, u, n);
                wu(i, v);
                break e;
              }
          }
          i = i.return;
        } while (i !== null);
      }
      Za(t);
    } catch (x) {
      n = x, K === t && t !== null && (K = t = t.return);
      continue;
    }
    break;
  } while (1);
}
function Xa() {
  var e = Zr.current;
  return Zr.current = Gr, e === null ? Gr : e;
}
function zo() {
  (X === 0 || X === 3 || X === 2) && (X = 4), J === null || !(Tn & 268435455) && !(fl & 268435455) || be(J, b);
}
function br(e, n) {
  var t = R;
  R |= 2;
  var r = Xa();
  (J !== e || b !== n) && ($e = null, Cn(e, n));
  do
    try {
      wd();
      break;
    } catch (l) {
      Ya(e, l);
    }
  while (1);
  if (ao(), R = t, Zr.current = r, K !== null)
    throw Error(y(261));
  return J = null, b = 0, X;
}
function wd() {
  for (; K !== null; )
    Ga(K);
}
function kd() {
  for (; K !== null && !Hc(); )
    Ga(K);
}
function Ga(e) {
  var n = qa(e.alternate, e, me);
  e.memoizedProps = e.pendingProps, n === null ? Za(e) : K = n, Eo.current = null;
}
function Za(e) {
  var n = e;
  do {
    var t = n.alternate;
    if (e = n.return, n.flags & 32768) {
      if (t = pd(t, n), t !== null) {
        t.flags &= 32767, K = t;
        return;
      }
      if (e !== null)
        e.flags |= 32768, e.subtreeFlags = 0, e.deletions = null;
      else {
        X = 6, K = null;
        return;
      }
    } else if (t = dd(t, n, me), t !== null) {
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
function wn(e, n, t) {
  var r = D, l = Ee.transition;
  try {
    Ee.transition = null, D = 1, Sd(e, n, t, r);
  } finally {
    Ee.transition = l, D = r;
  }
  return null;
}
function Sd(e, n, t, r) {
  do
    Jn();
  while (nn !== null);
  if (R & 6)
    throw Error(y(327));
  t = e.finishedWork;
  var l = e.finishedLanes;
  if (t === null)
    return null;
  if (e.finishedWork = null, e.finishedLanes = 0, t === e.current)
    throw Error(y(177));
  e.callbackNode = null, e.callbackPriority = 0;
  var i = t.lanes | t.childLanes;
  if (ef(e, i), e === J && (K = J = null, b = 0), !(t.subtreeFlags & 2064) && !(t.flags & 2064) || yr || (yr = !0, ba(Mr, function() {
    return Jn(), null;
  })), i = (t.flags & 15990) !== 0, t.subtreeFlags & 15990 || i) {
    i = Ee.transition, Ee.transition = null;
    var o = D;
    D = 1;
    var u = R;
    R |= 4, Eo.current = null, hd(e, t), Ha(t, e), Vf(hi), Ir = !!mi, hi = mi = null, e.current = t, vd(t), Qc(), R = u, D = o, Ee.transition = i;
  } else
    e.current = t;
  if (yr && (yr = !1, nn = e, qr = l), i = e.pendingLanes, i === 0 && (sn = null), Xc(t.stateNode), pe(e, Q()), n !== null)
    for (r = e.onRecoverableError, t = 0; t < n.length; t++)
      l = n[t], r(l.value, { componentStack: l.stack, digest: l.digest });
  if (Jr)
    throw Jr = !1, e = Oi, Oi = null, e;
  return qr & 1 && e.tag !== 0 && Jn(), i = e.pendingLanes, i & 1 ? e === Ii ? jt++ : (jt = 0, Ii = e) : jt = 0, hn(), null;
}
function Jn() {
  if (nn !== null) {
    var e = Ls(qr), n = Ee.transition, t = D;
    try {
      if (Ee.transition = null, D = 16 > e ? 16 : e, nn === null)
        var r = !1;
      else {
        if (e = nn, nn = null, qr = 0, R & 6)
          throw Error(y(331));
        var l = R;
        for (R |= 4, S = e.current; S !== null; ) {
          var i = S, o = i.child;
          if (S.flags & 16) {
            var u = i.deletions;
            if (u !== null) {
              for (var s = 0; s < u.length; s++) {
                var c = u[s];
                for (S = c; S !== null; ) {
                  var h = S;
                  switch (h.tag) {
                    case 0:
                    case 11:
                    case 15:
                      Tt(8, h, i);
                  }
                  var m = h.child;
                  if (m !== null)
                    m.return = h, S = m;
                  else
                    for (; S !== null; ) {
                      h = S;
                      var p = h.sibling, g = h.return;
                      if (Va(h), h === c) {
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
                      Tt(9, i, i.return);
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
                        cl(9, u);
                    }
                  } catch (x) {
                    B(u, u.return, x);
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
        if (R = l, hn(), Fe && typeof Fe.onPostCommitFiberRoot == "function")
          try {
            Fe.onPostCommitFiberRoot(tl, e);
          } catch {
          }
        r = !0;
      }
      return r;
    } finally {
      D = t, Ee.transition = n;
    }
  }
  return !1;
}
function Au(e, n, t) {
  n = rt(t, n), n = La(e, n, 1), e = un(e, n, 1), n = oe(), e !== null && (Zt(e, 1, n), pe(e, n));
}
function B(e, n, t) {
  if (e.tag === 3)
    Au(e, e, t);
  else
    for (; n !== null; ) {
      if (n.tag === 3) {
        Au(n, e, t);
        break;
      } else if (n.tag === 1) {
        var r = n.stateNode;
        if (typeof n.type.getDerivedStateFromError == "function" || typeof r.componentDidCatch == "function" && (sn === null || !sn.has(r))) {
          e = rt(t, e), e = ja(n, e, 1), n = un(n, e, 1), e = oe(), n !== null && (Zt(n, 1, e), pe(n, e));
          break;
        }
      }
      n = n.return;
    }
}
function xd(e, n, t) {
  var r = e.pingCache;
  r !== null && r.delete(n), n = oe(), e.pingedLanes |= e.suspendedLanes & t, J === e && (b & t) === t && (X === 4 || X === 3 && (b & 130023424) === b && 500 > Q() - _o ? Cn(e, 0) : Co |= t), pe(e, n);
}
function Ja(e, n) {
  n === 0 && (e.mode & 1 ? (n = ur, ur <<= 1, !(ur & 130023424) && (ur = 4194304)) : n = 1);
  var t = oe();
  e = Ke(e, n), e !== null && (Zt(e, n, t), pe(e, t));
}
function Ed(e) {
  var n = e.memoizedState, t = 0;
  n !== null && (t = n.retryLane), Ja(e, t);
}
function Cd(e, n) {
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
  r !== null && r.delete(n), Ja(e, t);
}
var qa;
qa = function(e, n, t) {
  if (e !== null)
    if (e.memoizedProps !== n.pendingProps || fe.current)
      ce = !0;
    else {
      if (!(e.lanes & t) && !(n.flags & 128))
        return ce = !1, fd(e, n, t);
      ce = !!(e.flags & 131072);
    }
  else
    ce = !1, U && n.flags & 1048576 && ta(n, Wr, n.index);
  switch (n.lanes = 0, n.tag) {
    case 2:
      var r = n.type;
      Pr(e, n), e = n.pendingProps;
      var l = bn(n, le.current);
      Zn(n, t), l = go(null, n, r, e, l, t);
      var i = wo();
      return n.flags |= 1, typeof l == "object" && l !== null && typeof l.render == "function" && l.$$typeof === void 0 ? (n.tag = 1, n.memoizedState = null, n.updateQueue = null, de(r) ? (i = !0, Vr(n)) : i = !1, n.memoizedState = l.state !== null && l.state !== void 0 ? l.state : null, po(n), l.updater = al, n.stateNode = l, l._reactInternals = n, Ci(n, r, e, t), n = Pi(null, n, r, !0, i, t)) : (n.tag = 0, U && i && io(n), ie(null, n, l, t), n = n.child), n;
    case 16:
      r = n.elementType;
      e: {
        switch (Pr(e, n), e = n.pendingProps, l = r._init, r = l(r._payload), n.type = r, l = n.tag = Nd(r), e = ze(r, e), l) {
          case 0:
            n = Ni(null, n, r, e, t);
            break e;
          case 1:
            n = Lu(null, n, r, e, t);
            break e;
          case 11:
            n = zu(null, n, r, e, t);
            break e;
          case 14:
            n = Tu(null, n, r, ze(r.type, e), t);
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
      return r = n.type, l = n.pendingProps, l = n.elementType === r ? l : ze(r, l), Ni(e, n, r, l, t);
    case 1:
      return r = n.type, l = n.pendingProps, l = n.elementType === r ? l : ze(r, l), Lu(e, n, r, l, t);
    case 3:
      e: {
        if (Oa(n), e === null)
          throw Error(y(387));
        r = n.pendingProps, i = n.memoizedState, l = i.element, sa(e, n), Kr(n, r, null, t);
        var o = n.memoizedState;
        if (r = o.element, i.isDehydrated)
          if (i = { element: r, isDehydrated: !1, cache: o.cache, pendingSuspenseBoundaries: o.pendingSuspenseBoundaries, transitions: o.transitions }, n.updateQueue.baseState = i, n.memoizedState = i, n.flags & 256) {
            l = rt(Error(y(423)), n), n = ju(e, n, r, t, l);
            break e;
          } else if (r !== l) {
            l = rt(Error(y(424)), n), n = ju(e, n, r, t, l);
            break e;
          } else
            for (he = on(n.stateNode.containerInfo.firstChild), ve = n, U = !0, Le = null, t = oa(n, null, r, t), n.child = t; t; )
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
      return aa(n), e === null && Si(n), r = n.type, l = n.pendingProps, i = e !== null ? e.memoizedProps : null, o = l.children, vi(r, l) ? o = null : i !== null && vi(r, i) && (n.flags |= 32), Ma(e, n), ie(e, n, o, t), n.child;
    case 6:
      return e === null && Si(n), null;
    case 13:
      return Ia(e, n, t);
    case 4:
      return mo(n, n.stateNode.containerInfo), r = n.pendingProps, e === null ? n.child = nt(n, null, r, t) : ie(e, n, r, t), n.child;
    case 11:
      return r = n.type, l = n.pendingProps, l = n.elementType === r ? l : ze(r, l), zu(e, n, r, l, t);
    case 7:
      return ie(e, n, n.pendingProps, t), n.child;
    case 8:
      return ie(e, n, n.pendingProps.children, t), n.child;
    case 12:
      return ie(e, n, n.pendingProps.children, t), n.child;
    case 10:
      e: {
        if (r = n.type._context, l = n.pendingProps, i = n.memoizedProps, o = l.value, M(Hr, r._currentValue), r._currentValue = o, i !== null)
          if (De(i.value, o)) {
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
                      s = We(-1, t & -t), s.tag = 2;
                      var c = i.updateQueue;
                      if (c !== null) {
                        c = c.shared;
                        var h = c.pending;
                        h === null ? s.next = s : (s.next = h.next, h.next = s), c.pending = s;
                      }
                    }
                    i.lanes |= t, s = i.alternate, s !== null && (s.lanes |= t), xi(
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
                o.lanes |= t, u = o.alternate, u !== null && (u.lanes |= t), xi(o, t, n), o = i.sibling;
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
      return l = n.type, r = n.pendingProps.children, Zn(n, t), l = Ce(l), r = r(l), n.flags |= 1, ie(e, n, r, t), n.child;
    case 14:
      return r = n.type, l = ze(r, n.pendingProps), l = ze(r.type, l), Tu(e, n, r, l, t);
    case 15:
      return Ra(e, n, n.type, n.pendingProps, t);
    case 17:
      return r = n.type, l = n.pendingProps, l = n.elementType === r ? l : ze(r, l), Pr(e, n), n.tag = 1, de(r) ? (e = !0, Vr(n)) : e = !1, Zn(n, t), Ta(n, r, l), Ci(n, r, l, t), Pi(null, n, r, !0, e, t);
    case 19:
      return Fa(e, n, t);
    case 22:
      return Da(e, n, t);
  }
  throw Error(y(156, n.tag));
};
function ba(e, n) {
  return Ns(e, n);
}
function _d(e, n, t, r) {
  this.tag = e, this.key = t, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.ref = null, this.pendingProps = n, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = r, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
}
function xe(e, n, t, r) {
  return new _d(e, n, t, r);
}
function To(e) {
  return e = e.prototype, !(!e || !e.isReactComponent);
}
function Nd(e) {
  if (typeof e == "function")
    return To(e) ? 1 : 0;
  if (e != null) {
    if (e = e.$$typeof, e === Yi)
      return 11;
    if (e === Xi)
      return 14;
  }
  return 2;
}
function cn(e, n) {
  var t = e.alternate;
  return t === null ? (t = xe(e.tag, n, e.key, e.mode), t.elementType = e.elementType, t.type = e.type, t.stateNode = e.stateNode, t.alternate = e, e.alternate = t) : (t.pendingProps = n, t.type = e.type, t.flags = 0, t.subtreeFlags = 0, t.deletions = null), t.flags = e.flags & 14680064, t.childLanes = e.childLanes, t.lanes = e.lanes, t.child = e.child, t.memoizedProps = e.memoizedProps, t.memoizedState = e.memoizedState, t.updateQueue = e.updateQueue, n = e.dependencies, t.dependencies = n === null ? null : { lanes: n.lanes, firstContext: n.firstContext }, t.sibling = e.sibling, t.index = e.index, t.ref = e.ref, t;
}
function Lr(e, n, t, r, l, i) {
  var o = 2;
  if (r = e, typeof e == "function")
    To(e) && (o = 1);
  else if (typeof e == "string")
    o = 5;
  else
    e:
      switch (e) {
        case On:
          return _n(t.children, l, i, n);
        case Ki:
          o = 8, l |= 8;
          break;
        case Xl:
          return e = xe(12, t, n, l | 2), e.elementType = Xl, e.lanes = i, e;
        case Gl:
          return e = xe(13, t, n, l), e.elementType = Gl, e.lanes = i, e;
        case Zl:
          return e = xe(19, t, n, l), e.elementType = Zl, e.lanes = i, e;
        case as:
          return dl(t, l, i, n);
        default:
          if (typeof e == "object" && e !== null)
            switch (e.$$typeof) {
              case us:
                o = 10;
                break e;
              case ss:
                o = 9;
                break e;
              case Yi:
                o = 11;
                break e;
              case Xi:
                o = 14;
                break e;
              case Ze:
                o = 16, r = null;
                break e;
            }
          throw Error(y(130, e == null ? e : typeof e, ""));
      }
  return n = xe(o, t, n, l), n.elementType = e, n.type = r, n.lanes = i, n;
}
function _n(e, n, t, r) {
  return e = xe(7, e, r, n), e.lanes = t, e;
}
function dl(e, n, t, r) {
  return e = xe(22, e, r, n), e.elementType = as, e.lanes = t, e.stateNode = { isHidden: !1 }, e;
}
function Hl(e, n, t) {
  return e = xe(6, e, null, n), e.lanes = t, e;
}
function Ql(e, n, t) {
  return n = xe(4, e.children !== null ? e.children : [], e.key, n), n.lanes = t, n.stateNode = { containerInfo: e.containerInfo, pendingChildren: null, implementation: e.implementation }, n;
}
function Pd(e, n, t, r, l) {
  this.tag = n, this.containerInfo = e, this.finishedWork = this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.pendingContext = this.context = null, this.callbackPriority = 0, this.eventTimes = _l(0), this.expirationTimes = _l(-1), this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = _l(0), this.identifierPrefix = r, this.onRecoverableError = l, this.mutableSourceEagerHydrationData = null;
}
function Lo(e, n, t, r, l, i, o, u, s) {
  return e = new Pd(e, n, t, u, s), n === 1 ? (n = 1, i === !0 && (n |= 8)) : n = 0, i = xe(3, null, null, n), e.current = i, i.stateNode = e, i.memoizedState = { element: r, isDehydrated: t, cache: null, transitions: null, pendingSuspenseBoundaries: null }, po(i), e;
}
function zd(e, n, t) {
  var r = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
  return { $$typeof: Mn, key: r == null ? null : "" + r, children: e, containerInfo: n, implementation: t };
}
function ec(e) {
  if (!e)
    return dn;
  e = e._reactInternals;
  e: {
    if (Rn(e) !== e || e.tag !== 1)
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
      return ea(e, t, n);
  }
  return n;
}
function nc(e, n, t, r, l, i, o, u, s) {
  return e = Lo(t, r, !0, e, l, i, o, u, s), e.context = ec(null), t = e.current, r = oe(), l = an(t), i = We(r, l), i.callback = n ?? null, un(t, i, l), e.current.lanes = l, Zt(e, l, r), pe(e, r), e;
}
function pl(e, n, t, r) {
  var l = n.current, i = oe(), o = an(l);
  return t = ec(t), n.context === null ? n.context = t : n.pendingContext = t, n = We(i, o), n.payload = { element: e }, r = r === void 0 ? null : r, r !== null && (n.callback = r), e = un(l, n, o), e !== null && (Re(e, l, o, i), Cr(e, l, o)), o;
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
function Vu(e, n) {
  if (e = e.memoizedState, e !== null && e.dehydrated !== null) {
    var t = e.retryLane;
    e.retryLane = t !== 0 && t < n ? t : n;
  }
}
function jo(e, n) {
  Vu(e, n), (e = e.alternate) && Vu(e, n);
}
function Td() {
  return null;
}
var tc = typeof reportError == "function" ? reportError : function(e) {
  console.error(e);
};
function Ro(e) {
  this._internalRoot = e;
}
ml.prototype.render = Ro.prototype.render = function(e) {
  var n = this._internalRoot;
  if (n === null)
    throw Error(y(409));
  pl(e, n, null, null);
};
ml.prototype.unmount = Ro.prototype.unmount = function() {
  var e = this._internalRoot;
  if (e !== null) {
    this._internalRoot = null;
    var n = e.containerInfo;
    Ln(function() {
      pl(null, e, null, null);
    }), n[Qe] = null;
  }
};
function ml(e) {
  this._internalRoot = e;
}
ml.prototype.unstable_scheduleHydration = function(e) {
  if (e) {
    var n = Ds();
    e = { blockedOn: null, target: e, priority: n };
    for (var t = 0; t < qe.length && n !== 0 && n < qe[t].priority; t++)
      ;
    qe.splice(t, 0, e), t === 0 && Os(e);
  }
};
function Do(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11);
}
function hl(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11 && (e.nodeType !== 8 || e.nodeValue !== " react-mount-point-unstable "));
}
function Bu() {
}
function Ld(e, n, t, r, l) {
  if (l) {
    if (typeof r == "function") {
      var i = r;
      r = function() {
        var c = el(o);
        i.call(c);
      };
    }
    var o = nc(n, r, e, 0, null, !1, !1, "", Bu);
    return e._reactRootContainer = o, e[Qe] = o.current, At(e.nodeType === 8 ? e.parentNode : e), Ln(), o;
  }
  for (; l = e.lastChild; )
    e.removeChild(l);
  if (typeof r == "function") {
    var u = r;
    r = function() {
      var c = el(s);
      u.call(c);
    };
  }
  var s = Lo(e, 0, !1, null, null, !1, !1, "", Bu);
  return e._reactRootContainer = s, e[Qe] = s.current, At(e.nodeType === 8 ? e.parentNode : e), Ln(function() {
    pl(n, s, t, r);
  }), s;
}
function vl(e, n, t, r, l) {
  var i = t._reactRootContainer;
  if (i) {
    var o = i;
    if (typeof l == "function") {
      var u = l;
      l = function() {
        var s = el(o);
        u.call(s);
      };
    }
    pl(n, o, e, l);
  } else
    o = Ld(t, n, e, l, r);
  return el(o);
}
js = function(e) {
  switch (e.tag) {
    case 3:
      var n = e.stateNode;
      if (n.current.memoizedState.isDehydrated) {
        var t = St(n.pendingLanes);
        t !== 0 && (Ji(n, t | 1), pe(n, Q()), !(R & 6) && (lt = Q() + 500, hn()));
      }
      break;
    case 13:
      Ln(function() {
        var r = Ke(e, 1);
        if (r !== null) {
          var l = oe();
          Re(r, e, 1, l);
        }
      }), jo(e, 1);
  }
};
qi = function(e) {
  if (e.tag === 13) {
    var n = Ke(e, 134217728);
    if (n !== null) {
      var t = oe();
      Re(n, e, 134217728, t);
    }
    jo(e, 134217728);
  }
};
Rs = function(e) {
  if (e.tag === 13) {
    var n = an(e), t = Ke(e, n);
    if (t !== null) {
      var r = oe();
      Re(t, e, n, r);
    }
    jo(e, n);
  }
};
Ds = function() {
  return D;
};
Ms = function(e, n) {
  var t = D;
  try {
    return D = e, n();
  } finally {
    D = t;
  }
};
oi = function(e, n, t) {
  switch (n) {
    case "input":
      if (bl(e, t), n = t.name, t.type === "radio" && n != null) {
        for (t = e; t.parentNode; )
          t = t.parentNode;
        for (t = t.querySelectorAll("input[name=" + JSON.stringify("" + n) + '][type="radio"]'), n = 0; n < t.length; n++) {
          var r = t[n];
          if (r !== e && r.form === e.form) {
            var l = ol(r);
            if (!l)
              throw Error(y(90));
            fs(r), bl(r, l);
          }
        }
      }
      break;
    case "textarea":
      ps(e, t);
      break;
    case "select":
      n = t.value, n != null && Kn(e, !!t.multiple, n, !1);
  }
};
ks = No;
Ss = Ln;
var jd = { usingClientEntryPoint: !1, Events: [qt, $n, ol, gs, ws, No] }, yt = { findFiberByHostInstance: Sn, bundleType: 0, version: "18.3.1", rendererPackageName: "react-dom" }, Rd = { bundleType: yt.bundleType, version: yt.version, rendererPackageName: yt.rendererPackageName, rendererConfig: yt.rendererConfig, overrideHookState: null, overrideHookStateDeletePath: null, overrideHookStateRenamePath: null, overrideProps: null, overridePropsDeletePath: null, overridePropsRenamePath: null, setErrorHandler: null, setSuspenseHandler: null, scheduleUpdate: null, currentDispatcherRef: Xe.ReactCurrentDispatcher, findHostInstanceByFiber: function(e) {
  return e = Cs(e), e === null ? null : e.stateNode;
}, findFiberByHostInstance: yt.findFiberByHostInstance || Td, findHostInstancesForRefresh: null, scheduleRefresh: null, scheduleRoot: null, setRefreshHandler: null, getCurrentFiber: null, reconcilerVersion: "18.3.1-next-f1338f8080-20240426" };
if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u") {
  var gr = __REACT_DEVTOOLS_GLOBAL_HOOK__;
  if (!gr.isDisabled && gr.supportsFiber)
    try {
      tl = gr.inject(Rd), Fe = gr;
    } catch {
    }
}
ge.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = jd;
ge.createPortal = function(e, n) {
  var t = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
  if (!Do(n))
    throw Error(y(200));
  return zd(e, n, null, t);
};
ge.createRoot = function(e, n) {
  if (!Do(e))
    throw Error(y(299));
  var t = !1, r = "", l = tc;
  return n != null && (n.unstable_strictMode === !0 && (t = !0), n.identifierPrefix !== void 0 && (r = n.identifierPrefix), n.onRecoverableError !== void 0 && (l = n.onRecoverableError)), n = Lo(e, 1, !1, null, null, t, !1, r, l), e[Qe] = n.current, At(e.nodeType === 8 ? e.parentNode : e), new Ro(n);
};
ge.findDOMNode = function(e) {
  if (e == null)
    return null;
  if (e.nodeType === 1)
    return e;
  var n = e._reactInternals;
  if (n === void 0)
    throw typeof e.render == "function" ? Error(y(188)) : (e = Object.keys(e).join(","), Error(y(268, e)));
  return e = Cs(n), e = e === null ? null : e.stateNode, e;
};
ge.flushSync = function(e) {
  return Ln(e);
};
ge.hydrate = function(e, n, t) {
  if (!hl(n))
    throw Error(y(200));
  return vl(null, e, n, !0, t);
};
ge.hydrateRoot = function(e, n, t) {
  if (!Do(e))
    throw Error(y(405));
  var r = t != null && t.hydratedSources || null, l = !1, i = "", o = tc;
  if (t != null && (t.unstable_strictMode === !0 && (l = !0), t.identifierPrefix !== void 0 && (i = t.identifierPrefix), t.onRecoverableError !== void 0 && (o = t.onRecoverableError)), n = nc(n, null, e, 1, t ?? null, l, !1, i, o), e[Qe] = n.current, At(e), r)
    for (e = 0; e < r.length; e++)
      t = r[e], l = t._getVersion, l = l(t._source), n.mutableSourceEagerHydrationData == null ? n.mutableSourceEagerHydrationData = [t, l] : n.mutableSourceEagerHydrationData.push(
        t,
        l
      );
  return new ml(n);
};
ge.render = function(e, n, t) {
  if (!hl(n))
    throw Error(y(200));
  return vl(null, e, n, !1, t);
};
ge.unmountComponentAtNode = function(e) {
  if (!hl(e))
    throw Error(y(40));
  return e._reactRootContainer ? (Ln(function() {
    vl(null, null, e, !1, function() {
      e._reactRootContainer = null, e[Qe] = null;
    });
  }), !0) : !1;
};
ge.unstable_batchedUpdates = No;
ge.unstable_renderSubtreeIntoContainer = function(e, n, t, r) {
  if (!hl(t))
    throw Error(y(200));
  if (e == null || e._reactInternals === void 0)
    throw Error(y(38));
  return vl(e, n, t, !1, r);
};
ge.version = "18.3.1-next-f1338f8080-20240426";
function rc() {
  if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function"))
    try {
      __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(rc);
    } catch (e) {
      console.error(e);
    }
}
rc(), rs.exports = ge;
var Dd = rs.exports, Wu = Dd;
Kl.createRoot = Wu.createRoot, Kl.hydrateRoot = Wu.hydrateRoot;
const gt = ({ title: e, value: n, icon: t }) => /* @__PURE__ */ C.jsxs("div", { className: "bg-white dark:bg-gray-800 rounded-lg shadow p-4 flex items-center", children: [
  /* @__PURE__ */ C.jsx("div", { className: "text-3xl mr-4", children: t }),
  /* @__PURE__ */ C.jsxs("div", { children: [
    /* @__PURE__ */ C.jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: e }),
    /* @__PURE__ */ C.jsx("p", { className: "text-2xl font-semibold text-gray-900 dark:text-white", children: n })
  ] })
] }), Md = ({ devices: e, setActiveView: n }) => /* @__PURE__ */ C.jsx("div", { className: "bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden", children: /* @__PURE__ */ C.jsxs("table", { className: "min-w-full", children: [
  /* @__PURE__ */ C.jsx("thead", { className: "bg-gray-50 dark:bg-gray-700", children: /* @__PURE__ */ C.jsxs("tr", { children: [
    /* @__PURE__ */ C.jsx("th", { className: "px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider", children: "Name" }),
    /* @__PURE__ */ C.jsx("th", { className: "px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider", children: "Status" }),
    /* @__PURE__ */ C.jsx("th", { className: "px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider", children: "Model" }),
    /* @__PURE__ */ C.jsx("th", { className: "px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider", children: "MAC Address" })
  ] }) }),
  /* @__PURE__ */ C.jsx("tbody", { className: "divide-y divide-gray-200 dark:divide-gray-600", children: e.map((t) => /* @__PURE__ */ C.jsxs("tr", { onClick: () => n({ view: "device", deviceId: t.serial }), className: "cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700", children: [
    /* @__PURE__ */ C.jsx("td", { className: "px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white", children: t.name || t.mac }),
    /* @__PURE__ */ C.jsx("td", { className: "px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300", children: t.status }),
    /* @__PURE__ */ C.jsx("td", { className: "px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300", children: t.model }),
    /* @__PURE__ */ C.jsx("td", { className: "px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300", children: t.mac })
  ] }, t.serial)) })
] }) }), Hu = ({ setActiveView: e, data: n }) => {
  if (!n)
    return /* @__PURE__ */ C.jsx("div", { children: "Loading dashboard..." });
  const { devices: t = [], ssids: r = [], networks: l = [] } = n, i = {
    totalDevices: t.length,
    wirelessAps: t.filter((o) => {
      var u;
      return (u = o.model) == null ? void 0 : u.startsWith("MR");
    }).length,
    switches: t.filter((o) => {
      var u;
      return (u = o.model) == null ? void 0 : u.startsWith("MS");
    }).length,
    cameras: t.filter((o) => {
      var u;
      return (u = o.model) == null ? void 0 : u.startsWith("MV");
    }).length,
    ssids: r.length
  };
  return /* @__PURE__ */ C.jsxs("div", { children: [
    /* @__PURE__ */ C.jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8", children: [
      /* @__PURE__ */ C.jsx(gt, { title: "Total Devices", value: i.totalDevices, icon: "📱" }),
      /* @__PURE__ */ C.jsx(gt, { title: "Wireless APs", value: i.wirelessAps, icon: "📡" }),
      /* @__PURE__ */ C.jsx(gt, { title: "Switches", value: i.switches, icon: "🔄" }),
      /* @__PURE__ */ C.jsx(gt, { title: "Cameras", value: i.cameras, icon: "📹" }),
      /* @__PURE__ */ C.jsx(gt, { title: "Virtual SSIDs", value: i.ssids, icon: "📶" })
    ] }),
    /* @__PURE__ */ C.jsx("h2", { className: "text-xl font-semibold mb-4", children: "Networks" }),
    /* @__PURE__ */ C.jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: l.map((o) => /* @__PURE__ */ C.jsx(
      "div",
      {
        "data-testid": "network-card",
        className: "bg-white dark:bg-gray-800 rounded-lg shadow p-4 cursor-pointer",
        style: { display: "block" },
        onClick: () => e({ view: "network", networkId: o.id }),
        children: /* @__PURE__ */ C.jsx("p", { className: "font-medium text-gray-900 dark:text-white", children: o.name })
      },
      o.id
    )) }),
    /* @__PURE__ */ C.jsx("h2", { className: "text-xl font-semibold mb-4 mt-8", children: "All Devices" }),
    /* @__PURE__ */ C.jsx(Md, { devices: t, setActiveView: e })
  ] });
}, Od = ({ activeView: e, setActiveView: n, data: t }) => {
  const r = t.devices.find((l) => l.serial === e.deviceId);
  return r ? /* @__PURE__ */ C.jsxs("div", { children: [
    /* @__PURE__ */ C.jsx("button", { onClick: () => n({ view: "dashboard" }), className: "mb-4", children: "← Back to Dashboard" }),
    /* @__PURE__ */ C.jsx("h2", { className: "text-xl font-semibold mb-4", children: "Device Details" }),
    /* @__PURE__ */ C.jsxs("p", { children: [
      "Name: ",
      r.name || r.mac
    ] }),
    /* @__PURE__ */ C.jsxs("p", { children: [
      "Status: ",
      r.status
    ] }),
    /* @__PURE__ */ C.jsxs("p", { children: [
      "Model: ",
      r.model
    ] }),
    /* @__PURE__ */ C.jsxs("p", { children: [
      "MAC Address: ",
      r.mac
    ] }),
    /* @__PURE__ */ C.jsxs("p", { children: [
      "Serial: ",
      r.serial
    ] })
  ] }) : /* @__PURE__ */ C.jsx("div", { children: "Device not found" });
}, Id = ({ activeView: e, setActiveView: n, data: t }) => {
  const r = t.networks.find((l) => l.id === e.networkId);
  return r ? /* @__PURE__ */ C.jsxs("div", { children: [
    /* @__PURE__ */ C.jsx("button", { onClick: () => n({ view: "dashboard" }), className: "mb-4", children: "← Back to Dashboard" }),
    /* @__PURE__ */ C.jsx("h2", { className: "text-xl font-semibold mb-4", children: "Network Information" }),
    /* @__PURE__ */ C.jsxs("p", { children: [
      "Name: ",
      r.name
    ] }),
    /* @__PURE__ */ C.jsxs("p", { children: [
      "ID: ",
      r.id
    ] }),
    /* @__PURE__ */ C.jsxs("p", { children: [
      "Product Types: ",
      r.product_types.join(", ")
    ] })
  ] }) : /* @__PURE__ */ C.jsx("div", { children: "Network not found" });
}, Fd = ({}) => {
  const [e] = kn.useState(null), [n] = kn.useState(!1), [t] = kn.useState(null), [r, l] = kn.useState({ view: "dashboard" });
  if (n)
    return /* @__PURE__ */ C.jsx("div", { className: "p-4", children: "Loading..." });
  if (t)
    return /* @__PURE__ */ C.jsxs("div", { className: "p-4 text-red-500", children: [
      "Error: ",
      t
    ] });
  const i = () => {
    switch (r.view) {
      case "dashboard":
        return /* @__PURE__ */ C.jsx(Hu, { setActiveView: l, data: e });
      case "device":
        return /* @__PURE__ */ C.jsx(Od, { activeView: r, setActiveView: l, data: e });
      case "network":
        return /* @__PURE__ */ C.jsx(Id, { activeView: r, setActiveView: l, data: e });
      default:
        return /* @__PURE__ */ C.jsx(Hu, { setActiveView: l, data: e });
    }
  };
  return /* @__PURE__ */ C.jsxs("div", { className: "p-4", children: [
    /* @__PURE__ */ C.jsx("h1", { className: "text-2xl font-bold mb-4", children: "Meraki HA Web UI" }),
    i()
  ] });
};
const Qu = document.getElementById("root");
Qu ? Kl.createRoot(Qu).render(
  /* @__PURE__ */ C.jsx(Sc.StrictMode, { children: /* @__PURE__ */ C.jsx(Fd, { hass: window.hass, config_entry_id: window.config_entry_id }) })
) : console.error("Root element not found");
