(function () {
  const t = document.createElement('link').relList;
  if (t && t.supports && t.supports('modulepreload')) return;
  for (const l of document.querySelectorAll('link[rel="modulepreload"]')) r(l);
  new MutationObserver((l) => {
    for (const a of l)
      if (a.type === 'childList')
        for (const o of a.addedNodes)
          o.tagName === 'LINK' && o.rel === 'modulepreload' && r(o);
  }).observe(document, { childList: !0, subtree: !0 });
  function n(l) {
    const a = {};
    return (
      l.integrity && (a.integrity = l.integrity),
      l.referrerPolicy && (a.referrerPolicy = l.referrerPolicy),
      l.crossOrigin === 'use-credentials'
        ? (a.credentials = 'include')
        : l.crossOrigin === 'anonymous'
        ? (a.credentials = 'omit')
        : (a.credentials = 'same-origin'),
      a
    );
  }
  function r(l) {
    if (l.ep) return;
    l.ep = !0;
    const a = n(l);
    fetch(l.href, a);
  }
})();
(function () {
  const e = document.createElement('link').relList;
  if (e && e.supports && e.supports('modulepreload')) return;
  for (const r of document.querySelectorAll('link[rel="modulepreload"]')) n(r);
  new MutationObserver((r) => {
    for (const l of r)
      if (l.type === 'childList')
        for (const a of l.addedNodes)
          a.tagName === 'LINK' && a.rel === 'modulepreload' && n(a);
  }).observe(document, { childList: !0, subtree: !0 });
  function t(r) {
    const l = {};
    return (
      r.integrity && (l.integrity = r.integrity),
      r.referrerPolicy && (l.referrerPolicy = r.referrerPolicy),
      r.crossOrigin === 'use-credentials'
        ? (l.credentials = 'include')
        : r.crossOrigin === 'anonymous'
        ? (l.credentials = 'omit')
        : (l.credentials = 'same-origin'),
      l
    );
  }
  function n(r) {
    if (r.ep) return;
    r.ep = !0;
    const l = t(r);
    fetch(r.href, l);
  }
})();
(function () {
  const e = document.createElement('link').relList;
  if (e && e.supports && e.supports('modulepreload')) return;
  for (const r of document.querySelectorAll('link[rel="modulepreload"]')) n(r);
  new MutationObserver((r) => {
    for (const l of r)
      if (l.type === 'childList')
        for (const a of l.addedNodes)
          a.tagName === 'LINK' && a.rel === 'modulepreload' && n(a);
  }).observe(document, { childList: !0, subtree: !0 });
  function t(r) {
    const l = {};
    return (
      r.integrity && (l.integrity = r.integrity),
      r.referrerPolicy && (l.referrerPolicy = r.referrerPolicy),
      r.crossOrigin === 'use-credentials'
        ? (l.credentials = 'include')
        : r.crossOrigin === 'anonymous'
        ? (l.credentials = 'omit')
        : (l.credentials = 'same-origin'),
      l
    );
  }
  function n(r) {
    if (r.ep) return;
    r.ep = !0;
    const l = t(r);
    fetch(r.href, l);
  }
})();
function nc(e) {
  return e &&
    e.__esModule &&
    Object.prototype.hasOwnProperty.call(e, 'default')
    ? e.default
    : e;
}
var $i = { exports: {} },
  el = {},
  Hi = { exports: {} },
  z = {};
/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */ var qn = Symbol.for('react.element'),
  rc = Symbol.for('react.portal'),
  lc = Symbol.for('react.fragment'),
  ac = Symbol.for('react.strict_mode'),
  oc = Symbol.for('react.profiler'),
  ic = Symbol.for('react.provider'),
  uc = Symbol.for('react.context'),
  sc = Symbol.for('react.forward_ref'),
  cc = Symbol.for('react.suspense'),
  fc = Symbol.for('react.memo'),
  dc = Symbol.for('react.lazy'),
  Ro = Symbol.iterator;
function pc(e) {
  return e === null || typeof e != 'object'
    ? null
    : ((e = (Ro && e[Ro]) || e['@@iterator']),
      typeof e == 'function' ? e : null);
}
var Bi = {
    isMounted: function () {
      return !1;
    },
    enqueueForceUpdate: function () {},
    enqueueReplaceState: function () {},
    enqueueSetState: function () {},
  },
  Wi = Object.assign,
  Qi = {};
function ln(e, t, n) {
  (this.props = e),
    (this.context = t),
    (this.refs = Qi),
    (this.updater = n || Bi);
}
ln.prototype.isReactComponent = {};
ln.prototype.setState = function (e, t) {
  if (typeof e != 'object' && typeof e != 'function' && e != null)
    throw Error(
      'setState(...): takes an object of state variables to update or a function which returns an object of state variables.'
    );
  this.updater.enqueueSetState(this, e, t, 'setState');
};
ln.prototype.forceUpdate = function (e) {
  this.updater.enqueueForceUpdate(this, e, 'forceUpdate');
};
function Xi() {}
Xi.prototype = ln.prototype;
function Ma(e, t, n) {
  (this.props = e),
    (this.context = t),
    (this.refs = Qi),
    (this.updater = n || Bi);
}
var Fa = (Ma.prototype = new Xi());
Fa.constructor = Ma;
Wi(Fa, ln.prototype);
Fa.isPureReactComponent = !0;
var Io = Array.isArray,
  qi = Object.prototype.hasOwnProperty,
  Ua = { current: null },
  Yi = { key: !0, ref: !0, __self: !0, __source: !0 };
function Ki(e, t, n) {
  var r,
    l = {},
    a = null,
    o = null;
  if (t != null)
    for (r in (t.ref !== void 0 && (o = t.ref),
    t.key !== void 0 && (a = '' + t.key),
    t))
      qi.call(t, r) && !Yi.hasOwnProperty(r) && (l[r] = t[r]);
  var u = arguments.length - 2;
  if (u === 1) l.children = n;
  else if (1 < u) {
    for (var i = Array(u), c = 0; c < u; c++) i[c] = arguments[c + 2];
    l.children = i;
  }
  if (e && e.defaultProps)
    for (r in ((u = e.defaultProps), u)) l[r] === void 0 && (l[r] = u[r]);
  return {
    $$typeof: qn,
    type: e,
    key: a,
    ref: o,
    props: l,
    _owner: Ua.current,
  };
}
function mc(e, t) {
  return {
    $$typeof: qn,
    type: e.type,
    key: t,
    ref: e.ref,
    props: e.props,
    _owner: e._owner,
  };
}
function Aa(e) {
  return typeof e == 'object' && e !== null && e.$$typeof === qn;
}
function hc(e) {
  var t = { '=': '=0', ':': '=2' };
  return (
    '$' +
    e.replace(/[=:]/g, function (n) {
      return t[n];
    })
  );
}
var Oo = /\/+/g;
function bl(e, t) {
  return typeof e == 'object' && e !== null && e.key != null
    ? hc('' + e.key)
    : t.toString(36);
}
function yr(e, t, n, r, l) {
  var a = typeof e;
  (a === 'undefined' || a === 'boolean') && (e = null);
  var o = !1;
  if (e === null) o = !0;
  else
    switch (a) {
      case 'string':
      case 'number':
        o = !0;
        break;
      case 'object':
        switch (e.$$typeof) {
          case qn:
          case rc:
            o = !0;
        }
    }
  if (o)
    return (
      (o = e),
      (l = l(o)),
      (e = r === '' ? '.' + bl(o, 0) : r),
      Io(l)
        ? ((n = ''),
          e != null && (n = e.replace(Oo, '$&/') + '/'),
          yr(l, t, n, '', function (c) {
            return c;
          }))
        : l != null &&
          (Aa(l) &&
            (l = mc(
              l,
              n +
                (!l.key || (o && o.key === l.key)
                  ? ''
                  : ('' + l.key).replace(Oo, '$&/') + '/') +
                e
            )),
          t.push(l)),
      1
    );
  if (((o = 0), (r = r === '' ? '.' : r + ':'), Io(e)))
    for (var u = 0; u < e.length; u++) {
      a = e[u];
      var i = r + bl(a, u);
      o += yr(a, t, n, i, l);
    }
  else if (((i = pc(e)), typeof i == 'function'))
    for (e = i.call(e), u = 0; !(a = e.next()).done; )
      (a = a.value), (i = r + bl(a, u++)), (o += yr(a, t, n, i, l));
  else if (a === 'object')
    throw (
      ((t = String(e)),
      Error(
        'Objects are not valid as a React child (found: ' +
          (t === '[object Object]'
            ? 'object with keys {' + Object.keys(e).join(', ') + '}'
            : t) +
          '). If you meant to render a collection of children, use an array instead.'
      ))
    );
  return o;
}
function tr(e, t, n) {
  if (e == null) return e;
  var r = [],
    l = 0;
  return (
    yr(e, r, '', '', function (a) {
      return t.call(n, a, l++);
    }),
    r
  );
}
function gc(e) {
  if (e._status === -1) {
    var t = e._result;
    (t = t()),
      t.then(
        function (n) {
          (e._status === 0 || e._status === -1) &&
            ((e._status = 1), (e._result = n));
        },
        function (n) {
          (e._status === 0 || e._status === -1) &&
            ((e._status = 2), (e._result = n));
        }
      ),
      e._status === -1 && ((e._status = 0), (e._result = t));
  }
  if (e._status === 1) return e._result.default;
  throw e._result;
}
var ue = { current: null },
  br = { transition: null },
  vc = {
    ReactCurrentDispatcher: ue,
    ReactCurrentBatchConfig: br,
    ReactCurrentOwner: Ua,
  };
function Gi() {
  throw Error('act(...) is not supported in production builds of React.');
}
z.Children = {
  map: tr,
  forEach: function (e, t, n) {
    tr(
      e,
      function () {
        t.apply(this, arguments);
      },
      n
    );
  },
  count: function (e) {
    var t = 0;
    return (
      tr(e, function () {
        t++;
      }),
      t
    );
  },
  toArray: function (e) {
    return (
      tr(e, function (t) {
        return t;
      }) || []
    );
  },
  only: function (e) {
    if (!Aa(e))
      throw Error(
        'React.Children.only expected to receive a single React element child.'
      );
    return e;
  },
};
z.Component = ln;
z.Fragment = lc;
z.Profiler = oc;
z.PureComponent = Ma;
z.StrictMode = ac;
z.Suspense = cc;
z.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = vc;
z.act = Gi;
z.cloneElement = function (e, t, n) {
  if (e == null)
    throw Error(
      'React.cloneElement(...): The argument must be a React element, but you passed ' +
        e +
        '.'
    );
  var r = Wi({}, e.props),
    l = e.key,
    a = e.ref,
    o = e._owner;
  if (t != null) {
    if (
      (t.ref !== void 0 && ((a = t.ref), (o = Ua.current)),
      t.key !== void 0 && (l = '' + t.key),
      e.type && e.type.defaultProps)
    )
      var u = e.type.defaultProps;
    for (i in t)
      qi.call(t, i) &&
        !Yi.hasOwnProperty(i) &&
        (r[i] = t[i] === void 0 && u !== void 0 ? u[i] : t[i]);
  }
  var i = arguments.length - 2;
  if (i === 1) r.children = n;
  else if (1 < i) {
    u = Array(i);
    for (var c = 0; c < i; c++) u[c] = arguments[c + 2];
    r.children = u;
  }
  return { $$typeof: qn, type: e.type, key: l, ref: a, props: r, _owner: o };
};
z.createContext = function (e) {
  return (
    (e = {
      $$typeof: uc,
      _currentValue: e,
      _currentValue2: e,
      _threadCount: 0,
      Provider: null,
      Consumer: null,
      _defaultValue: null,
      _globalName: null,
    }),
    (e.Provider = { $$typeof: ic, _context: e }),
    (e.Consumer = e)
  );
};
z.createElement = Ki;
z.createFactory = function (e) {
  var t = Ki.bind(null, e);
  return (t.type = e), t;
};
z.createRef = function () {
  return { current: null };
};
z.forwardRef = function (e) {
  return { $$typeof: sc, render: e };
};
z.isValidElement = Aa;
z.lazy = function (e) {
  return { $$typeof: dc, _payload: { _status: -1, _result: e }, _init: gc };
};
z.memo = function (e, t) {
  return { $$typeof: fc, type: e, compare: t === void 0 ? null : t };
};
z.startTransition = function (e) {
  var t = br.transition;
  br.transition = {};
  try {
    e();
  } finally {
    br.transition = t;
  }
};
z.unstable_act = Gi;
z.useCallback = function (e, t) {
  return ue.current.useCallback(e, t);
};
z.useContext = function (e) {
  return ue.current.useContext(e);
};
z.useDebugValue = function () {};
z.useDeferredValue = function (e) {
  return ue.current.useDeferredValue(e);
};
z.useEffect = function (e, t) {
  return ue.current.useEffect(e, t);
};
z.useId = function () {
  return ue.current.useId();
};
z.useImperativeHandle = function (e, t, n) {
  return ue.current.useImperativeHandle(e, t, n);
};
z.useInsertionEffect = function (e, t) {
  return ue.current.useInsertionEffect(e, t);
};
z.useLayoutEffect = function (e, t) {
  return ue.current.useLayoutEffect(e, t);
};
z.useMemo = function (e, t) {
  return ue.current.useMemo(e, t);
};
z.useReducer = function (e, t, n) {
  return ue.current.useReducer(e, t, n);
};
z.useRef = function (e) {
  return ue.current.useRef(e);
};
z.useState = function (e) {
  return ue.current.useState(e);
};
z.useSyncExternalStore = function (e, t, n) {
  return ue.current.useSyncExternalStore(e, t, n);
};
z.useTransition = function () {
  return ue.current.useTransition();
};
z.version = '18.3.1';
Hi.exports = z;
var Z = Hi.exports;
const yc = nc(Z);
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */ var bc = Z,
  wc = Symbol.for('react.element'),
  kc = Symbol.for('react.fragment'),
  xc = Object.prototype.hasOwnProperty,
  Sc = bc.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner,
  _c = { key: !0, ref: !0, __self: !0, __source: !0 };
function Ji(e, t, n) {
  var r,
    l = {},
    a = null,
    o = null;
  n !== void 0 && (a = '' + n),
    t.key !== void 0 && (a = '' + t.key),
    t.ref !== void 0 && (o = t.ref);
  for (r in t) xc.call(t, r) && !_c.hasOwnProperty(r) && (l[r] = t[r]);
  if (e && e.defaultProps)
    for (r in ((t = e.defaultProps), t)) l[r] === void 0 && (l[r] = t[r]);
  return {
    $$typeof: wc,
    type: e,
    key: a,
    ref: o,
    props: l,
    _owner: Sc.current,
  };
}
el.Fragment = kc;
el.jsx = Ji;
el.jsxs = Ji;
$i.exports = el;
var g = $i.exports,
  Wl = {},
  Zi = { exports: {} },
  be = {},
  eu = { exports: {} },
  tu = {};
/**
 * @license React
 * scheduler.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */ (function (e) {
  function t(S, P) {
    var L = S.length;
    S.push(P);
    e: for (; 0 < L; ) {
      var B = (L - 1) >>> 1,
        Y = S[B];
      if (0 < l(Y, P)) (S[B] = P), (S[L] = Y), (L = B);
      else break e;
    }
  }
  function n(S) {
    return S.length === 0 ? null : S[0];
  }
  function r(S) {
    if (S.length === 0) return null;
    var P = S[0],
      L = S.pop();
    if (L !== P) {
      S[0] = L;
      e: for (var B = 0, Y = S.length, Zn = Y >>> 1; B < Zn; ) {
        var gt = 2 * (B + 1) - 1,
          yl = S[gt],
          vt = gt + 1,
          er = S[vt];
        if (0 > l(yl, L))
          vt < Y && 0 > l(er, yl)
            ? ((S[B] = er), (S[vt] = L), (B = vt))
            : ((S[B] = yl), (S[gt] = L), (B = gt));
        else if (vt < Y && 0 > l(er, L)) (S[B] = er), (S[vt] = L), (B = vt);
        else break e;
      }
    }
    return P;
  }
  function l(S, P) {
    var L = S.sortIndex - P.sortIndex;
    return L !== 0 ? L : S.id - P.id;
  }
  if (typeof performance == 'object' && typeof performance.now == 'function') {
    var a = performance;
    e.unstable_now = function () {
      return a.now();
    };
  } else {
    var o = Date,
      u = o.now();
    e.unstable_now = function () {
      return o.now() - u;
    };
  }
  var i = [],
    c = [],
    m = 1,
    h = null,
    p = 3,
    w = !1,
    b = !1,
    k = !1,
    T = typeof setTimeout == 'function' ? setTimeout : null,
    d = typeof clearTimeout == 'function' ? clearTimeout : null,
    s = typeof setImmediate < 'u' ? setImmediate : null;
  typeof navigator < 'u' &&
    navigator.scheduling !== void 0 &&
    navigator.scheduling.isInputPending !== void 0 &&
    navigator.scheduling.isInputPending.bind(navigator.scheduling);
  function f(S) {
    for (var P = n(c); P !== null; ) {
      if (P.callback === null) r(c);
      else if (P.startTime <= S)
        r(c), (P.sortIndex = P.expirationTime), t(i, P);
      else break;
      P = n(c);
    }
  }
  function y(S) {
    if (((k = !1), f(S), !b))
      if (n(i) !== null) (b = !0), gl(_);
      else {
        var P = n(c);
        P !== null && vl(y, P.startTime - S);
      }
  }
  function _(S, P) {
    (b = !1), k && ((k = !1), d(C), (C = -1)), (w = !0);
    var L = p;
    try {
      for (
        f(P), h = n(i);
        h !== null && (!(h.expirationTime > P) || (S && !Ce()));

      ) {
        var B = h.callback;
        if (typeof B == 'function') {
          (h.callback = null), (p = h.priorityLevel);
          var Y = B(h.expirationTime <= P);
          (P = e.unstable_now()),
            typeof Y == 'function' ? (h.callback = Y) : h === n(i) && r(i),
            f(P);
        } else r(i);
        h = n(i);
      }
      if (h !== null) var Zn = !0;
      else {
        var gt = n(c);
        gt !== null && vl(y, gt.startTime - P), (Zn = !1);
      }
      return Zn;
    } finally {
      (h = null), (p = L), (w = !1);
    }
  }
  var E = !1,
    N = null,
    C = -1,
    H = 5,
    j = -1;
  function Ce() {
    return !(e.unstable_now() - j < H);
  }
  function un() {
    if (N !== null) {
      var S = e.unstable_now();
      j = S;
      var P = !0;
      try {
        P = N(!0, S);
      } finally {
        P ? sn() : ((E = !1), (N = null));
      }
    } else E = !1;
  }
  var sn;
  if (typeof s == 'function')
    sn = function () {
      s(un);
    };
  else if (typeof MessageChannel < 'u') {
    var To = new MessageChannel(),
      tc = To.port2;
    (To.port1.onmessage = un),
      (sn = function () {
        tc.postMessage(null);
      });
  } else
    sn = function () {
      T(un, 0);
    };
  function gl(S) {
    (N = S), E || ((E = !0), sn());
  }
  function vl(S, P) {
    C = T(function () {
      S(e.unstable_now());
    }, P);
  }
  (e.unstable_IdlePriority = 5),
    (e.unstable_ImmediatePriority = 1),
    (e.unstable_LowPriority = 4),
    (e.unstable_NormalPriority = 3),
    (e.unstable_Profiling = null),
    (e.unstable_UserBlockingPriority = 2),
    (e.unstable_cancelCallback = function (S) {
      S.callback = null;
    }),
    (e.unstable_continueExecution = function () {
      b || w || ((b = !0), gl(_));
    }),
    (e.unstable_forceFrameRate = function (S) {
      0 > S || 125 < S
        ? console.error(
            'forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported'
          )
        : (H = 0 < S ? Math.floor(1e3 / S) : 5);
    }),
    (e.unstable_getCurrentPriorityLevel = function () {
      return p;
    }),
    (e.unstable_getFirstCallbackNode = function () {
      return n(i);
    }),
    (e.unstable_next = function (S) {
      switch (p) {
        case 1:
        case 2:
        case 3:
          var P = 3;
          break;
        default:
          P = p;
      }
      var L = p;
      p = P;
      try {
        return S();
      } finally {
        p = L;
      }
    }),
    (e.unstable_pauseExecution = function () {}),
    (e.unstable_requestPaint = function () {}),
    (e.unstable_runWithPriority = function (S, P) {
      switch (S) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
          break;
        default:
          S = 3;
      }
      var L = p;
      p = S;
      try {
        return P();
      } finally {
        p = L;
      }
    }),
    (e.unstable_scheduleCallback = function (S, P, L) {
      var B = e.unstable_now();
      switch (
        (typeof L == 'object' && L !== null
          ? ((L = L.delay), (L = typeof L == 'number' && 0 < L ? B + L : B))
          : (L = B),
        S)
      ) {
        case 1:
          var Y = -1;
          break;
        case 2:
          Y = 250;
          break;
        case 5:
          Y = 1073741823;
          break;
        case 4:
          Y = 1e4;
          break;
        default:
          Y = 5e3;
      }
      return (
        (Y = L + Y),
        (S = {
          id: m++,
          callback: P,
          priorityLevel: S,
          startTime: L,
          expirationTime: Y,
          sortIndex: -1,
        }),
        L > B
          ? ((S.sortIndex = L),
            t(c, S),
            n(i) === null &&
              S === n(c) &&
              (k ? (d(C), (C = -1)) : (k = !0), vl(y, L - B)))
          : ((S.sortIndex = Y), t(i, S), b || w || ((b = !0), gl(_))),
        S
      );
    }),
    (e.unstable_shouldYield = Ce),
    (e.unstable_wrapCallback = function (S) {
      var P = p;
      return function () {
        var L = p;
        p = P;
        try {
          return S.apply(this, arguments);
        } finally {
          p = L;
        }
      };
    });
})(tu);
eu.exports = tu;
var Ec = eu.exports;
/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */ var Nc = Z,
  ye = Ec;
function v(e) {
  for (
    var t = 'https://reactjs.org/docs/error-decoder.html?invariant=' + e,
      n = 1;
    n < arguments.length;
    n++
  )
    t += '&args[]=' + encodeURIComponent(arguments[n]);
  return (
    'Minified React error #' +
    e +
    '; visit ' +
    t +
    ' for the full message or use the non-minified dev environment for full errors and additional helpful warnings.'
  );
}
var nu = new Set(),
  jn = {};
function zt(e, t) {
  Gt(e, t), Gt(e + 'Capture', t);
}
function Gt(e, t) {
  for (jn[e] = t, e = 0; e < t.length; e++) nu.add(t[e]);
}
var We = !(
    typeof window > 'u' ||
    typeof window.document > 'u' ||
    typeof window.document.createElement > 'u'
  ),
  Ql = Object.prototype.hasOwnProperty,
  Cc =
    /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/,
  Do = {},
  Mo = {};
function Pc(e) {
  return Ql.call(Mo, e)
    ? !0
    : Ql.call(Do, e)
    ? !1
    : Cc.test(e)
    ? (Mo[e] = !0)
    : ((Do[e] = !0), !1);
}
function Lc(e, t, n, r) {
  if (n !== null && n.type === 0) return !1;
  switch (typeof t) {
    case 'function':
    case 'symbol':
      return !0;
    case 'boolean':
      return r
        ? !1
        : n !== null
        ? !n.acceptsBooleans
        : ((e = e.toLowerCase().slice(0, 5)), e !== 'data-' && e !== 'aria-');
    default:
      return !1;
  }
}
function zc(e, t, n, r) {
  if (t === null || typeof t > 'u' || Lc(e, t, n, r)) return !0;
  if (r) return !1;
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
function se(e, t, n, r, l, a, o) {
  (this.acceptsBooleans = t === 2 || t === 3 || t === 4),
    (this.attributeName = r),
    (this.attributeNamespace = l),
    (this.mustUseProperty = n),
    (this.propertyName = e),
    (this.type = t),
    (this.sanitizeURL = a),
    (this.removeEmptyString = o);
}
var te = {};
'children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style'
  .split(' ')
  .forEach(function (e) {
    te[e] = new se(e, 0, !1, e, null, !1, !1);
  });
[
  ['acceptCharset', 'accept-charset'],
  ['className', 'class'],
  ['htmlFor', 'for'],
  ['httpEquiv', 'http-equiv'],
].forEach(function (e) {
  var t = e[0];
  te[t] = new se(t, 1, !1, e[1], null, !1, !1);
});
['contentEditable', 'draggable', 'spellCheck', 'value'].forEach(function (e) {
  te[e] = new se(e, 2, !1, e.toLowerCase(), null, !1, !1);
});
[
  'autoReverse',
  'externalResourcesRequired',
  'focusable',
  'preserveAlpha',
].forEach(function (e) {
  te[e] = new se(e, 2, !1, e, null, !1, !1);
});
'allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope'
  .split(' ')
  .forEach(function (e) {
    te[e] = new se(e, 3, !1, e.toLowerCase(), null, !1, !1);
  });
['checked', 'multiple', 'muted', 'selected'].forEach(function (e) {
  te[e] = new se(e, 3, !0, e, null, !1, !1);
});
['capture', 'download'].forEach(function (e) {
  te[e] = new se(e, 4, !1, e, null, !1, !1);
});
['cols', 'rows', 'size', 'span'].forEach(function (e) {
  te[e] = new se(e, 6, !1, e, null, !1, !1);
});
['rowSpan', 'start'].forEach(function (e) {
  te[e] = new se(e, 5, !1, e.toLowerCase(), null, !1, !1);
});
var Va = /[\-:]([a-z])/g;
function $a(e) {
  return e[1].toUpperCase();
}
'accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height'
  .split(' ')
  .forEach(function (e) {
    var t = e.replace(Va, $a);
    te[t] = new se(t, 1, !1, e, null, !1, !1);
  });
'xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type'
  .split(' ')
  .forEach(function (e) {
    var t = e.replace(Va, $a);
    te[t] = new se(t, 1, !1, e, 'http://www.w3.org/1999/xlink', !1, !1);
  });
['xml:base', 'xml:lang', 'xml:space'].forEach(function (e) {
  var t = e.replace(Va, $a);
  te[t] = new se(t, 1, !1, e, 'http://www.w3.org/XML/1998/namespace', !1, !1);
});
['tabIndex', 'crossOrigin'].forEach(function (e) {
  te[e] = new se(e, 1, !1, e.toLowerCase(), null, !1, !1);
});
te.xlinkHref = new se(
  'xlinkHref',
  1,
  !1,
  'xlink:href',
  'http://www.w3.org/1999/xlink',
  !0,
  !1
);
['src', 'href', 'action', 'formAction'].forEach(function (e) {
  te[e] = new se(e, 1, !1, e.toLowerCase(), null, !0, !0);
});
function Ha(e, t, n, r) {
  var l = te.hasOwnProperty(t) ? te[t] : null;
  (l !== null
    ? l.type !== 0
    : r ||
      !(2 < t.length) ||
      (t[0] !== 'o' && t[0] !== 'O') ||
      (t[1] !== 'n' && t[1] !== 'N')) &&
    (zc(t, n, l, r) && (n = null),
    r || l === null
      ? Pc(t) &&
        (n === null ? e.removeAttribute(t) : e.setAttribute(t, '' + n))
      : l.mustUseProperty
      ? (e[l.propertyName] = n === null ? (l.type === 3 ? !1 : '') : n)
      : ((t = l.attributeName),
        (r = l.attributeNamespace),
        n === null
          ? e.removeAttribute(t)
          : ((l = l.type),
            (n = l === 3 || (l === 4 && n === !0) ? '' : '' + n),
            r ? e.setAttributeNS(r, t, n) : e.setAttribute(t, n))));
}
var Ye = Nc.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED,
  nr = Symbol.for('react.element'),
  Rt = Symbol.for('react.portal'),
  It = Symbol.for('react.fragment'),
  Ba = Symbol.for('react.strict_mode'),
  Xl = Symbol.for('react.profiler'),
  ru = Symbol.for('react.provider'),
  lu = Symbol.for('react.context'),
  Wa = Symbol.for('react.forward_ref'),
  ql = Symbol.for('react.suspense'),
  Yl = Symbol.for('react.suspense_list'),
  Qa = Symbol.for('react.memo'),
  Ge = Symbol.for('react.lazy'),
  au = Symbol.for('react.offscreen'),
  Fo = Symbol.iterator;
function cn(e) {
  return e === null || typeof e != 'object'
    ? null
    : ((e = (Fo && e[Fo]) || e['@@iterator']),
      typeof e == 'function' ? e : null);
}
var V = Object.assign,
  wl;
function yn(e) {
  if (wl === void 0)
    try {
      throw Error();
    } catch (n) {
      var t = n.stack.trim().match(/\n( *(at )?)/);
      wl = (t && t[1]) || '';
    }
  return (
    `
` +
    wl +
    e
  );
}
var kl = !1;
function xl(e, t) {
  if (!e || kl) return '';
  kl = !0;
  var n = Error.prepareStackTrace;
  Error.prepareStackTrace = void 0;
  try {
    if (t)
      if (
        ((t = function () {
          throw Error();
        }),
        Object.defineProperty(t.prototype, 'props', {
          set: function () {
            throw Error();
          },
        }),
        typeof Reflect == 'object' && Reflect.construct)
      ) {
        try {
          Reflect.construct(t, []);
        } catch (c) {
          var r = c;
        }
        Reflect.construct(e, [], t);
      } else {
        try {
          t.call();
        } catch (c) {
          r = c;
        }
        e.call(t.prototype);
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
    if (c && r && typeof c.stack == 'string') {
      for (
        var l = c.stack.split(`
`),
          a = r.stack.split(`
`),
          o = l.length - 1,
          u = a.length - 1;
        1 <= o && 0 <= u && l[o] !== a[u];

      )
        u--;
      for (; 1 <= o && 0 <= u; o--, u--)
        if (l[o] !== a[u]) {
          if (o !== 1 || u !== 1)
            do
              if ((o--, u--, 0 > u || l[o] !== a[u])) {
                var i =
                  `
` + l[o].replace(' at new ', ' at ');
                return (
                  e.displayName &&
                    i.includes('<anonymous>') &&
                    (i = i.replace('<anonymous>', e.displayName)),
                  i
                );
              }
            while (1 <= o && 0 <= u);
          break;
        }
    }
  } finally {
    (kl = !1), (Error.prepareStackTrace = n);
  }
  return (e = e ? e.displayName || e.name : '') ? yn(e) : '';
}
function jc(e) {
  switch (e.tag) {
    case 5:
      return yn(e.type);
    case 16:
      return yn('Lazy');
    case 13:
      return yn('Suspense');
    case 19:
      return yn('SuspenseList');
    case 0:
    case 2:
    case 15:
      return (e = xl(e.type, !1)), e;
    case 11:
      return (e = xl(e.type.render, !1)), e;
    case 1:
      return (e = xl(e.type, !0)), e;
    default:
      return '';
  }
}
function Kl(e) {
  if (e == null) return null;
  if (typeof e == 'function') return e.displayName || e.name || null;
  if (typeof e == 'string') return e;
  switch (e) {
    case It:
      return 'Fragment';
    case Rt:
      return 'Portal';
    case Xl:
      return 'Profiler';
    case Ba:
      return 'StrictMode';
    case ql:
      return 'Suspense';
    case Yl:
      return 'SuspenseList';
  }
  if (typeof e == 'object')
    switch (e.$$typeof) {
      case lu:
        return (e.displayName || 'Context') + '.Consumer';
      case ru:
        return (e._context.displayName || 'Context') + '.Provider';
      case Wa:
        var t = e.render;
        return (
          (e = e.displayName),
          e ||
            ((e = t.displayName || t.name || ''),
            (e = e !== '' ? 'ForwardRef(' + e + ')' : 'ForwardRef')),
          e
        );
      case Qa:
        return (
          (t = e.displayName || null), t !== null ? t : Kl(e.type) || 'Memo'
        );
      case Ge:
        (t = e._payload), (e = e._init);
        try {
          return Kl(e(t));
        } catch {}
    }
  return null;
}
function Tc(e) {
  var t = e.type;
  switch (e.tag) {
    case 24:
      return 'Cache';
    case 9:
      return (t.displayName || 'Context') + '.Consumer';
    case 10:
      return (t._context.displayName || 'Context') + '.Provider';
    case 18:
      return 'DehydratedFragment';
    case 11:
      return (
        (e = t.render),
        (e = e.displayName || e.name || ''),
        t.displayName || (e !== '' ? 'ForwardRef(' + e + ')' : 'ForwardRef')
      );
    case 7:
      return 'Fragment';
    case 5:
      return t;
    case 4:
      return 'Portal';
    case 3:
      return 'Root';
    case 6:
      return 'Text';
    case 16:
      return Kl(t);
    case 8:
      return t === Ba ? 'StrictMode' : 'Mode';
    case 22:
      return 'Offscreen';
    case 12:
      return 'Profiler';
    case 21:
      return 'Scope';
    case 13:
      return 'Suspense';
    case 19:
      return 'SuspenseList';
    case 25:
      return 'TracingMarker';
    case 1:
    case 0:
    case 17:
    case 2:
    case 14:
    case 15:
      if (typeof t == 'function') return t.displayName || t.name || null;
      if (typeof t == 'string') return t;
  }
  return null;
}
function ft(e) {
  switch (typeof e) {
    case 'boolean':
    case 'number':
    case 'string':
    case 'undefined':
      return e;
    case 'object':
      return e;
    default:
      return '';
  }
}
function ou(e) {
  var t = e.type;
  return (
    (e = e.nodeName) &&
    e.toLowerCase() === 'input' &&
    (t === 'checkbox' || t === 'radio')
  );
}
function Rc(e) {
  var t = ou(e) ? 'checked' : 'value',
    n = Object.getOwnPropertyDescriptor(e.constructor.prototype, t),
    r = '' + e[t];
  if (
    !e.hasOwnProperty(t) &&
    typeof n < 'u' &&
    typeof n.get == 'function' &&
    typeof n.set == 'function'
  ) {
    var l = n.get,
      a = n.set;
    return (
      Object.defineProperty(e, t, {
        configurable: !0,
        get: function () {
          return l.call(this);
        },
        set: function (o) {
          (r = '' + o), a.call(this, o);
        },
      }),
      Object.defineProperty(e, t, { enumerable: n.enumerable }),
      {
        getValue: function () {
          return r;
        },
        setValue: function (o) {
          r = '' + o;
        },
        stopTracking: function () {
          (e._valueTracker = null), delete e[t];
        },
      }
    );
  }
}
function rr(e) {
  e._valueTracker || (e._valueTracker = Rc(e));
}
function iu(e) {
  if (!e) return !1;
  var t = e._valueTracker;
  if (!t) return !0;
  var n = t.getValue(),
    r = '';
  return (
    e && (r = ou(e) ? (e.checked ? 'true' : 'false') : e.value),
    (e = r),
    e !== n ? (t.setValue(e), !0) : !1
  );
}
function zr(e) {
  if (((e = e || (typeof document < 'u' ? document : void 0)), typeof e > 'u'))
    return null;
  try {
    return e.activeElement || e.body;
  } catch {
    return e.body;
  }
}
function Gl(e, t) {
  var n = t.checked;
  return V({}, t, {
    defaultChecked: void 0,
    defaultValue: void 0,
    value: void 0,
    checked: n ?? e._wrapperState.initialChecked,
  });
}
function Uo(e, t) {
  var n = t.defaultValue == null ? '' : t.defaultValue,
    r = t.checked != null ? t.checked : t.defaultChecked;
  (n = ft(t.value != null ? t.value : n)),
    (e._wrapperState = {
      initialChecked: r,
      initialValue: n,
      controlled:
        t.type === 'checkbox' || t.type === 'radio'
          ? t.checked != null
          : t.value != null,
    });
}
function uu(e, t) {
  (t = t.checked), t != null && Ha(e, 'checked', t, !1);
}
function Jl(e, t) {
  uu(e, t);
  var n = ft(t.value),
    r = t.type;
  if (n != null)
    r === 'number'
      ? ((n === 0 && e.value === '') || e.value != n) && (e.value = '' + n)
      : e.value !== '' + n && (e.value = '' + n);
  else if (r === 'submit' || r === 'reset') {
    e.removeAttribute('value');
    return;
  }
  t.hasOwnProperty('value')
    ? Zl(e, t.type, n)
    : t.hasOwnProperty('defaultValue') && Zl(e, t.type, ft(t.defaultValue)),
    t.checked == null &&
      t.defaultChecked != null &&
      (e.defaultChecked = !!t.defaultChecked);
}
function Ao(e, t, n) {
  if (t.hasOwnProperty('value') || t.hasOwnProperty('defaultValue')) {
    var r = t.type;
    if (
      !(
        (r !== 'submit' && r !== 'reset') ||
        (t.value !== void 0 && t.value !== null)
      )
    )
      return;
    (t = '' + e._wrapperState.initialValue),
      n || t === e.value || (e.value = t),
      (e.defaultValue = t);
  }
  (n = e.name),
    n !== '' && (e.name = ''),
    (e.defaultChecked = !!e._wrapperState.initialChecked),
    n !== '' && (e.name = n);
}
function Zl(e, t, n) {
  (t !== 'number' || zr(e.ownerDocument) !== e) &&
    (n == null
      ? (e.defaultValue = '' + e._wrapperState.initialValue)
      : e.defaultValue !== '' + n && (e.defaultValue = '' + n));
}
var bn = Array.isArray;
function Wt(e, t, n, r) {
  if (((e = e.options), t)) {
    t = {};
    for (var l = 0; l < n.length; l++) t['$' + n[l]] = !0;
    for (n = 0; n < e.length; n++)
      (l = t.hasOwnProperty('$' + e[n].value)),
        e[n].selected !== l && (e[n].selected = l),
        l && r && (e[n].defaultSelected = !0);
  } else {
    for (n = '' + ft(n), t = null, l = 0; l < e.length; l++) {
      if (e[l].value === n) {
        (e[l].selected = !0), r && (e[l].defaultSelected = !0);
        return;
      }
      t !== null || e[l].disabled || (t = e[l]);
    }
    t !== null && (t.selected = !0);
  }
}
function ea(e, t) {
  if (t.dangerouslySetInnerHTML != null) throw Error(v(91));
  return V({}, t, {
    value: void 0,
    defaultValue: void 0,
    children: '' + e._wrapperState.initialValue,
  });
}
function Vo(e, t) {
  var n = t.value;
  if (n == null) {
    if (((n = t.children), (t = t.defaultValue), n != null)) {
      if (t != null) throw Error(v(92));
      if (bn(n)) {
        if (1 < n.length) throw Error(v(93));
        n = n[0];
      }
      t = n;
    }
    t == null && (t = ''), (n = t);
  }
  e._wrapperState = { initialValue: ft(n) };
}
function su(e, t) {
  var n = ft(t.value),
    r = ft(t.defaultValue);
  n != null &&
    ((n = '' + n),
    n !== e.value && (e.value = n),
    t.defaultValue == null && e.defaultValue !== n && (e.defaultValue = n)),
    r != null && (e.defaultValue = '' + r);
}
function $o(e) {
  var t = e.textContent;
  t === e._wrapperState.initialValue &&
    t !== '' &&
    t !== null &&
    (e.value = t);
}
function cu(e) {
  switch (e) {
    case 'svg':
      return 'http://www.w3.org/2000/svg';
    case 'math':
      return 'http://www.w3.org/1998/Math/MathML';
    default:
      return 'http://www.w3.org/1999/xhtml';
  }
}
function ta(e, t) {
  return e == null || e === 'http://www.w3.org/1999/xhtml'
    ? cu(t)
    : e === 'http://www.w3.org/2000/svg' && t === 'foreignObject'
    ? 'http://www.w3.org/1999/xhtml'
    : e;
}
var lr,
  fu = (function (e) {
    return typeof MSApp < 'u' && MSApp.execUnsafeLocalFunction
      ? function (t, n, r, l) {
          MSApp.execUnsafeLocalFunction(function () {
            return e(t, n, r, l);
          });
        }
      : e;
  })(function (e, t) {
    if (e.namespaceURI !== 'http://www.w3.org/2000/svg' || 'innerHTML' in e)
      e.innerHTML = t;
    else {
      for (
        lr = lr || document.createElement('div'),
          lr.innerHTML = '<svg>' + t.valueOf().toString() + '</svg>',
          t = lr.firstChild;
        e.firstChild;

      )
        e.removeChild(e.firstChild);
      for (; t.firstChild; ) e.appendChild(t.firstChild);
    }
  });
function Tn(e, t) {
  if (t) {
    var n = e.firstChild;
    if (n && n === e.lastChild && n.nodeType === 3) {
      n.nodeValue = t;
      return;
    }
  }
  e.textContent = t;
}
var xn = {
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
    strokeWidth: !0,
  },
  Ic = ['Webkit', 'ms', 'Moz', 'O'];
Object.keys(xn).forEach(function (e) {
  Ic.forEach(function (t) {
    (t = t + e.charAt(0).toUpperCase() + e.substring(1)), (xn[t] = xn[e]);
  });
});
function du(e, t, n) {
  return t == null || typeof t == 'boolean' || t === ''
    ? ''
    : n || typeof t != 'number' || t === 0 || (xn.hasOwnProperty(e) && xn[e])
    ? ('' + t).trim()
    : t + 'px';
}
function pu(e, t) {
  e = e.style;
  for (var n in t)
    if (t.hasOwnProperty(n)) {
      var r = n.indexOf('--') === 0,
        l = du(n, t[n], r);
      n === 'float' && (n = 'cssFloat'), r ? e.setProperty(n, l) : (e[n] = l);
    }
}
var Oc = V(
  { menuitem: !0 },
  {
    area: !0,
    base: !0,
    br: !0,
    col: !0,
    embed: !0,
    hr: !0,
    img: !0,
    input: !0,
    keygen: !0,
    link: !0,
    meta: !0,
    param: !0,
    source: !0,
    track: !0,
    wbr: !0,
  }
);
function na(e, t) {
  if (t) {
    if (Oc[e] && (t.children != null || t.dangerouslySetInnerHTML != null))
      throw Error(v(137, e));
    if (t.dangerouslySetInnerHTML != null) {
      if (t.children != null) throw Error(v(60));
      if (
        typeof t.dangerouslySetInnerHTML != 'object' ||
        !('__html' in t.dangerouslySetInnerHTML)
      )
        throw Error(v(61));
    }
    if (t.style != null && typeof t.style != 'object') throw Error(v(62));
  }
}
function ra(e, t) {
  if (e.indexOf('-') === -1) return typeof t.is == 'string';
  switch (e) {
    case 'annotation-xml':
    case 'color-profile':
    case 'font-face':
    case 'font-face-src':
    case 'font-face-uri':
    case 'font-face-format':
    case 'font-face-name':
    case 'missing-glyph':
      return !1;
    default:
      return !0;
  }
}
var la = null;
function Xa(e) {
  return (
    (e = e.target || e.srcElement || window),
    e.correspondingUseElement && (e = e.correspondingUseElement),
    e.nodeType === 3 ? e.parentNode : e
  );
}
var aa = null,
  Qt = null,
  Xt = null;
function Ho(e) {
  if ((e = Gn(e))) {
    if (typeof aa != 'function') throw Error(v(280));
    var t = e.stateNode;
    t && ((t = al(t)), aa(e.stateNode, e.type, t));
  }
}
function mu(e) {
  Qt ? (Xt ? Xt.push(e) : (Xt = [e])) : (Qt = e);
}
function hu() {
  if (Qt) {
    var e = Qt,
      t = Xt;
    if (((Xt = Qt = null), Ho(e), t)) for (e = 0; e < t.length; e++) Ho(t[e]);
  }
}
function gu(e, t) {
  return e(t);
}
function vu() {}
var Sl = !1;
function yu(e, t, n) {
  if (Sl) return e(t, n);
  Sl = !0;
  try {
    return gu(e, t, n);
  } finally {
    (Sl = !1), (Qt !== null || Xt !== null) && (vu(), hu());
  }
}
function Rn(e, t) {
  var n = e.stateNode;
  if (n === null) return null;
  var r = al(n);
  if (r === null) return null;
  n = r[t];
  e: switch (t) {
    case 'onClick':
    case 'onClickCapture':
    case 'onDoubleClick':
    case 'onDoubleClickCapture':
    case 'onMouseDown':
    case 'onMouseDownCapture':
    case 'onMouseMove':
    case 'onMouseMoveCapture':
    case 'onMouseUp':
    case 'onMouseUpCapture':
    case 'onMouseEnter':
      (r = !r.disabled) ||
        ((e = e.type),
        (r = !(
          e === 'button' ||
          e === 'input' ||
          e === 'select' ||
          e === 'textarea'
        ))),
        (e = !r);
      break e;
    default:
      e = !1;
  }
  if (e) return null;
  if (n && typeof n != 'function') throw Error(v(231, t, typeof n));
  return n;
}
var oa = !1;
if (We)
  try {
    var fn = {};
    Object.defineProperty(fn, 'passive', {
      get: function () {
        oa = !0;
      },
    }),
      window.addEventListener('test', fn, fn),
      window.removeEventListener('test', fn, fn);
  } catch {
    oa = !1;
  }
function Dc(e, t, n, r, l, a, o, u, i) {
  var c = Array.prototype.slice.call(arguments, 3);
  try {
    t.apply(n, c);
  } catch (m) {
    this.onError(m);
  }
}
var Sn = !1,
  jr = null,
  Tr = !1,
  ia = null,
  Mc = {
    onError: function (e) {
      (Sn = !0), (jr = e);
    },
  };
function Fc(e, t, n, r, l, a, o, u, i) {
  (Sn = !1), (jr = null), Dc.apply(Mc, arguments);
}
function Uc(e, t, n, r, l, a, o, u, i) {
  if ((Fc.apply(this, arguments), Sn)) {
    if (Sn) {
      var c = jr;
      (Sn = !1), (jr = null);
    } else throw Error(v(198));
    Tr || ((Tr = !0), (ia = c));
  }
}
function jt(e) {
  var t = e,
    n = e;
  if (e.alternate) for (; t.return; ) t = t.return;
  else {
    e = t;
    do (t = e), t.flags & 4098 && (n = t.return), (e = t.return);
    while (e);
  }
  return t.tag === 3 ? n : null;
}
function bu(e) {
  if (e.tag === 13) {
    var t = e.memoizedState;
    if (
      (t === null && ((e = e.alternate), e !== null && (t = e.memoizedState)),
      t !== null)
    )
      return t.dehydrated;
  }
  return null;
}
function Bo(e) {
  if (jt(e) !== e) throw Error(v(188));
}
function Ac(e) {
  var t = e.alternate;
  if (!t) {
    if (((t = jt(e)), t === null)) throw Error(v(188));
    return t !== e ? null : e;
  }
  for (var n = e, r = t; ; ) {
    var l = n.return;
    if (l === null) break;
    var a = l.alternate;
    if (a === null) {
      if (((r = l.return), r !== null)) {
        n = r;
        continue;
      }
      break;
    }
    if (l.child === a.child) {
      for (a = l.child; a; ) {
        if (a === n) return Bo(l), e;
        if (a === r) return Bo(l), t;
        a = a.sibling;
      }
      throw Error(v(188));
    }
    if (n.return !== r.return) (n = l), (r = a);
    else {
      for (var o = !1, u = l.child; u; ) {
        if (u === n) {
          (o = !0), (n = l), (r = a);
          break;
        }
        if (u === r) {
          (o = !0), (r = l), (n = a);
          break;
        }
        u = u.sibling;
      }
      if (!o) {
        for (u = a.child; u; ) {
          if (u === n) {
            (o = !0), (n = a), (r = l);
            break;
          }
          if (u === r) {
            (o = !0), (r = a), (n = l);
            break;
          }
          u = u.sibling;
        }
        if (!o) throw Error(v(189));
      }
    }
    if (n.alternate !== r) throw Error(v(190));
  }
  if (n.tag !== 3) throw Error(v(188));
  return n.stateNode.current === n ? e : t;
}
function wu(e) {
  return (e = Ac(e)), e !== null ? ku(e) : null;
}
function ku(e) {
  if (e.tag === 5 || e.tag === 6) return e;
  for (e = e.child; e !== null; ) {
    var t = ku(e);
    if (t !== null) return t;
    e = e.sibling;
  }
  return null;
}
var xu = ye.unstable_scheduleCallback,
  Wo = ye.unstable_cancelCallback,
  Vc = ye.unstable_shouldYield,
  $c = ye.unstable_requestPaint,
  W = ye.unstable_now,
  Hc = ye.unstable_getCurrentPriorityLevel,
  qa = ye.unstable_ImmediatePriority,
  Su = ye.unstable_UserBlockingPriority,
  Rr = ye.unstable_NormalPriority,
  Bc = ye.unstable_LowPriority,
  _u = ye.unstable_IdlePriority,
  tl = null,
  Fe = null;
function Wc(e) {
  if (Fe && typeof Fe.onCommitFiberRoot == 'function')
    try {
      Fe.onCommitFiberRoot(tl, e, void 0, (e.current.flags & 128) === 128);
    } catch {}
}
var Te = Math.clz32 ? Math.clz32 : qc,
  Qc = Math.log,
  Xc = Math.LN2;
function qc(e) {
  return (e >>>= 0), e === 0 ? 32 : (31 - ((Qc(e) / Xc) | 0)) | 0;
}
var ar = 64,
  or = 4194304;
function wn(e) {
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
function Ir(e, t) {
  var n = e.pendingLanes;
  if (n === 0) return 0;
  var r = 0,
    l = e.suspendedLanes,
    a = e.pingedLanes,
    o = n & 268435455;
  if (o !== 0) {
    var u = o & ~l;
    u !== 0 ? (r = wn(u)) : ((a &= o), a !== 0 && (r = wn(a)));
  } else (o = n & ~l), o !== 0 ? (r = wn(o)) : a !== 0 && (r = wn(a));
  if (r === 0) return 0;
  if (
    t !== 0 &&
    t !== r &&
    !(t & l) &&
    ((l = r & -r), (a = t & -t), l >= a || (l === 16 && (a & 4194240) !== 0))
  )
    return t;
  if ((r & 4 && (r |= n & 16), (t = e.entangledLanes), t !== 0))
    for (e = e.entanglements, t &= r; 0 < t; )
      (n = 31 - Te(t)), (l = 1 << n), (r |= e[n]), (t &= ~l);
  return r;
}
function Yc(e, t) {
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
function Kc(e, t) {
  for (
    var n = e.suspendedLanes,
      r = e.pingedLanes,
      l = e.expirationTimes,
      a = e.pendingLanes;
    0 < a;

  ) {
    var o = 31 - Te(a),
      u = 1 << o,
      i = l[o];
    i === -1
      ? (!(u & n) || u & r) && (l[o] = Yc(u, t))
      : i <= t && (e.expiredLanes |= u),
      (a &= ~u);
  }
}
function ua(e) {
  return (
    (e = e.pendingLanes & -1073741825),
    e !== 0 ? e : e & 1073741824 ? 1073741824 : 0
  );
}
function Eu() {
  var e = ar;
  return (ar <<= 1), !(ar & 4194240) && (ar = 64), e;
}
function _l(e) {
  for (var t = [], n = 0; 31 > n; n++) t.push(e);
  return t;
}
function Yn(e, t, n) {
  (e.pendingLanes |= t),
    t !== 536870912 && ((e.suspendedLanes = 0), (e.pingedLanes = 0)),
    (e = e.eventTimes),
    (t = 31 - Te(t)),
    (e[t] = n);
}
function Gc(e, t) {
  var n = e.pendingLanes & ~t;
  (e.pendingLanes = t),
    (e.suspendedLanes = 0),
    (e.pingedLanes = 0),
    (e.expiredLanes &= t),
    (e.mutableReadLanes &= t),
    (e.entangledLanes &= t),
    (t = e.entanglements);
  var r = e.eventTimes;
  for (e = e.expirationTimes; 0 < n; ) {
    var l = 31 - Te(n),
      a = 1 << l;
    (t[l] = 0), (r[l] = -1), (e[l] = -1), (n &= ~a);
  }
}
function Ya(e, t) {
  var n = (e.entangledLanes |= t);
  for (e = e.entanglements; n; ) {
    var r = 31 - Te(n),
      l = 1 << r;
    (l & t) | (e[r] & t) && (e[r] |= t), (n &= ~l);
  }
}
var I = 0;
function Nu(e) {
  return (e &= -e), 1 < e ? (4 < e ? (e & 268435455 ? 16 : 536870912) : 4) : 1;
}
var Cu,
  Ka,
  Pu,
  Lu,
  zu,
  sa = !1,
  ir = [],
  rt = null,
  lt = null,
  at = null,
  In = new Map(),
  On = new Map(),
  Ze = [],
  Jc =
    'mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit'.split(
      ' '
    );
function Qo(e, t) {
  switch (e) {
    case 'focusin':
    case 'focusout':
      rt = null;
      break;
    case 'dragenter':
    case 'dragleave':
      lt = null;
      break;
    case 'mouseover':
    case 'mouseout':
      at = null;
      break;
    case 'pointerover':
    case 'pointerout':
      In.delete(t.pointerId);
      break;
    case 'gotpointercapture':
    case 'lostpointercapture':
      On.delete(t.pointerId);
  }
}
function dn(e, t, n, r, l, a) {
  return e === null || e.nativeEvent !== a
    ? ((e = {
        blockedOn: t,
        domEventName: n,
        eventSystemFlags: r,
        nativeEvent: a,
        targetContainers: [l],
      }),
      t !== null && ((t = Gn(t)), t !== null && Ka(t)),
      e)
    : ((e.eventSystemFlags |= r),
      (t = e.targetContainers),
      l !== null && t.indexOf(l) === -1 && t.push(l),
      e);
}
function Zc(e, t, n, r, l) {
  switch (t) {
    case 'focusin':
      return (rt = dn(rt, e, t, n, r, l)), !0;
    case 'dragenter':
      return (lt = dn(lt, e, t, n, r, l)), !0;
    case 'mouseover':
      return (at = dn(at, e, t, n, r, l)), !0;
    case 'pointerover':
      var a = l.pointerId;
      return In.set(a, dn(In.get(a) || null, e, t, n, r, l)), !0;
    case 'gotpointercapture':
      return (
        (a = l.pointerId), On.set(a, dn(On.get(a) || null, e, t, n, r, l)), !0
      );
  }
  return !1;
}
function ju(e) {
  var t = wt(e.target);
  if (t !== null) {
    var n = jt(t);
    if (n !== null) {
      if (((t = n.tag), t === 13)) {
        if (((t = bu(n)), t !== null)) {
          (e.blockedOn = t),
            zu(e.priority, function () {
              Pu(n);
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
function wr(e) {
  if (e.blockedOn !== null) return !1;
  for (var t = e.targetContainers; 0 < t.length; ) {
    var n = ca(e.domEventName, e.eventSystemFlags, t[0], e.nativeEvent);
    if (n === null) {
      n = e.nativeEvent;
      var r = new n.constructor(n.type, n);
      (la = r), n.target.dispatchEvent(r), (la = null);
    } else return (t = Gn(n)), t !== null && Ka(t), (e.blockedOn = n), !1;
    t.shift();
  }
  return !0;
}
function Xo(e, t, n) {
  wr(e) && n.delete(t);
}
function ef() {
  (sa = !1),
    rt !== null && wr(rt) && (rt = null),
    lt !== null && wr(lt) && (lt = null),
    at !== null && wr(at) && (at = null),
    In.forEach(Xo),
    On.forEach(Xo);
}
function pn(e, t) {
  e.blockedOn === t &&
    ((e.blockedOn = null),
    sa ||
      ((sa = !0),
      ye.unstable_scheduleCallback(ye.unstable_NormalPriority, ef)));
}
function Dn(e) {
  function t(l) {
    return pn(l, e);
  }
  if (0 < ir.length) {
    pn(ir[0], e);
    for (var n = 1; n < ir.length; n++) {
      var r = ir[n];
      r.blockedOn === e && (r.blockedOn = null);
    }
  }
  for (
    rt !== null && pn(rt, e),
      lt !== null && pn(lt, e),
      at !== null && pn(at, e),
      In.forEach(t),
      On.forEach(t),
      n = 0;
    n < Ze.length;
    n++
  )
    (r = Ze[n]), r.blockedOn === e && (r.blockedOn = null);
  for (; 0 < Ze.length && ((n = Ze[0]), n.blockedOn === null); )
    ju(n), n.blockedOn === null && Ze.shift();
}
var qt = Ye.ReactCurrentBatchConfig,
  Or = !0;
function tf(e, t, n, r) {
  var l = I,
    a = qt.transition;
  qt.transition = null;
  try {
    (I = 1), Ga(e, t, n, r);
  } finally {
    (I = l), (qt.transition = a);
  }
}
function nf(e, t, n, r) {
  var l = I,
    a = qt.transition;
  qt.transition = null;
  try {
    (I = 4), Ga(e, t, n, r);
  } finally {
    (I = l), (qt.transition = a);
  }
}
function Ga(e, t, n, r) {
  if (Or) {
    var l = ca(e, t, n, r);
    if (l === null) Il(e, t, r, Dr, n), Qo(e, r);
    else if (Zc(l, e, t, n, r)) r.stopPropagation();
    else if ((Qo(e, r), t & 4 && -1 < Jc.indexOf(e))) {
      for (; l !== null; ) {
        var a = Gn(l);
        if (
          (a !== null && Cu(a),
          (a = ca(e, t, n, r)),
          a === null && Il(e, t, r, Dr, n),
          a === l)
        )
          break;
        l = a;
      }
      l !== null && r.stopPropagation();
    } else Il(e, t, r, null, n);
  }
}
var Dr = null;
function ca(e, t, n, r) {
  if (((Dr = null), (e = Xa(r)), (e = wt(e)), e !== null))
    if (((t = jt(e)), t === null)) e = null;
    else if (((n = t.tag), n === 13)) {
      if (((e = bu(t)), e !== null)) return e;
      e = null;
    } else if (n === 3) {
      if (t.stateNode.current.memoizedState.isDehydrated)
        return t.tag === 3 ? t.stateNode.containerInfo : null;
      e = null;
    } else t !== e && (e = null);
  return (Dr = e), null;
}
function Tu(e) {
  switch (e) {
    case 'cancel':
    case 'click':
    case 'close':
    case 'contextmenu':
    case 'copy':
    case 'cut':
    case 'auxclick':
    case 'dblclick':
    case 'dragend':
    case 'dragstart':
    case 'drop':
    case 'focusin':
    case 'focusout':
    case 'input':
    case 'invalid':
    case 'keydown':
    case 'keypress':
    case 'keyup':
    case 'mousedown':
    case 'mouseup':
    case 'paste':
    case 'pause':
    case 'play':
    case 'pointercancel':
    case 'pointerdown':
    case 'pointerup':
    case 'ratechange':
    case 'reset':
    case 'resize':
    case 'seeked':
    case 'submit':
    case 'touchcancel':
    case 'touchend':
    case 'touchstart':
    case 'volumechange':
    case 'change':
    case 'selectionchange':
    case 'textInput':
    case 'compositionstart':
    case 'compositionend':
    case 'compositionupdate':
    case 'beforeblur':
    case 'afterblur':
    case 'beforeinput':
    case 'blur':
    case 'fullscreenchange':
    case 'focus':
    case 'hashchange':
    case 'popstate':
    case 'select':
    case 'selectstart':
      return 1;
    case 'drag':
    case 'dragenter':
    case 'dragexit':
    case 'dragleave':
    case 'dragover':
    case 'mousemove':
    case 'mouseout':
    case 'mouseover':
    case 'pointermove':
    case 'pointerout':
    case 'pointerover':
    case 'scroll':
    case 'toggle':
    case 'touchmove':
    case 'wheel':
    case 'mouseenter':
    case 'mouseleave':
    case 'pointerenter':
    case 'pointerleave':
      return 4;
    case 'message':
      switch (Hc()) {
        case qa:
          return 1;
        case Su:
          return 4;
        case Rr:
        case Bc:
          return 16;
        case _u:
          return 536870912;
        default:
          return 16;
      }
    default:
      return 16;
  }
}
var tt = null,
  Ja = null,
  kr = null;
function Ru() {
  if (kr) return kr;
  var e,
    t = Ja,
    n = t.length,
    r,
    l = 'value' in tt ? tt.value : tt.textContent,
    a = l.length;
  for (e = 0; e < n && t[e] === l[e]; e++);
  var o = n - e;
  for (r = 1; r <= o && t[n - r] === l[a - r]; r++);
  return (kr = l.slice(e, 1 < r ? 1 - r : void 0));
}
function xr(e) {
  var t = e.keyCode;
  return (
    'charCode' in e
      ? ((e = e.charCode), e === 0 && t === 13 && (e = 13))
      : (e = t),
    e === 10 && (e = 13),
    32 <= e || e === 13 ? e : 0
  );
}
function ur() {
  return !0;
}
function qo() {
  return !1;
}
function we(e) {
  function t(n, r, l, a, o) {
    (this._reactName = n),
      (this._targetInst = l),
      (this.type = r),
      (this.nativeEvent = a),
      (this.target = o),
      (this.currentTarget = null);
    for (var u in e)
      e.hasOwnProperty(u) && ((n = e[u]), (this[u] = n ? n(a) : a[u]));
    return (
      (this.isDefaultPrevented = (
        a.defaultPrevented != null ? a.defaultPrevented : a.returnValue === !1
      )
        ? ur
        : qo),
      (this.isPropagationStopped = qo),
      this
    );
  }
  return (
    V(t.prototype, {
      preventDefault: function () {
        this.defaultPrevented = !0;
        var n = this.nativeEvent;
        n &&
          (n.preventDefault
            ? n.preventDefault()
            : typeof n.returnValue != 'unknown' && (n.returnValue = !1),
          (this.isDefaultPrevented = ur));
      },
      stopPropagation: function () {
        var n = this.nativeEvent;
        n &&
          (n.stopPropagation
            ? n.stopPropagation()
            : typeof n.cancelBubble != 'unknown' && (n.cancelBubble = !0),
          (this.isPropagationStopped = ur));
      },
      persist: function () {},
      isPersistent: ur,
    }),
    t
  );
}
var an = {
    eventPhase: 0,
    bubbles: 0,
    cancelable: 0,
    timeStamp: function (e) {
      return e.timeStamp || Date.now();
    },
    defaultPrevented: 0,
    isTrusted: 0,
  },
  Za = we(an),
  Kn = V({}, an, { view: 0, detail: 0 }),
  rf = we(Kn),
  El,
  Nl,
  mn,
  nl = V({}, Kn, {
    screenX: 0,
    screenY: 0,
    clientX: 0,
    clientY: 0,
    pageX: 0,
    pageY: 0,
    ctrlKey: 0,
    shiftKey: 0,
    altKey: 0,
    metaKey: 0,
    getModifierState: eo,
    button: 0,
    buttons: 0,
    relatedTarget: function (e) {
      return e.relatedTarget === void 0
        ? e.fromElement === e.srcElement
          ? e.toElement
          : e.fromElement
        : e.relatedTarget;
    },
    movementX: function (e) {
      return 'movementX' in e
        ? e.movementX
        : (e !== mn &&
            (mn && e.type === 'mousemove'
              ? ((El = e.screenX - mn.screenX), (Nl = e.screenY - mn.screenY))
              : (Nl = El = 0),
            (mn = e)),
          El);
    },
    movementY: function (e) {
      return 'movementY' in e ? e.movementY : Nl;
    },
  }),
  Yo = we(nl),
  lf = V({}, nl, { dataTransfer: 0 }),
  af = we(lf),
  of = V({}, Kn, { relatedTarget: 0 }),
  Cl = we(of),
  uf = V({}, an, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }),
  sf = we(uf),
  cf = V({}, an, {
    clipboardData: function (e) {
      return 'clipboardData' in e ? e.clipboardData : window.clipboardData;
    },
  }),
  ff = we(cf),
  df = V({}, an, { data: 0 }),
  Ko = we(df),
  pf = {
    Esc: 'Escape',
    Spacebar: ' ',
    Left: 'ArrowLeft',
    Up: 'ArrowUp',
    Right: 'ArrowRight',
    Down: 'ArrowDown',
    Del: 'Delete',
    Win: 'OS',
    Menu: 'ContextMenu',
    Apps: 'ContextMenu',
    Scroll: 'ScrollLock',
    MozPrintableKey: 'Unidentified',
  },
  mf = {
    8: 'Backspace',
    9: 'Tab',
    12: 'Clear',
    13: 'Enter',
    16: 'Shift',
    17: 'Control',
    18: 'Alt',
    19: 'Pause',
    20: 'CapsLock',
    27: 'Escape',
    32: ' ',
    33: 'PageUp',
    34: 'PageDown',
    35: 'End',
    36: 'Home',
    37: 'ArrowLeft',
    38: 'ArrowUp',
    39: 'ArrowRight',
    40: 'ArrowDown',
    45: 'Insert',
    46: 'Delete',
    112: 'F1',
    113: 'F2',
    114: 'F3',
    115: 'F4',
    116: 'F5',
    117: 'F6',
    118: 'F7',
    119: 'F8',
    120: 'F9',
    121: 'F10',
    122: 'F11',
    123: 'F12',
    144: 'NumLock',
    145: 'ScrollLock',
    224: 'Meta',
  },
  hf = {
    Alt: 'altKey',
    Control: 'ctrlKey',
    Meta: 'metaKey',
    Shift: 'shiftKey',
  };
function gf(e) {
  var t = this.nativeEvent;
  return t.getModifierState
    ? t.getModifierState(e)
    : (e = hf[e])
    ? !!t[e]
    : !1;
}
function eo() {
  return gf;
}
var vf = V({}, Kn, {
    key: function (e) {
      if (e.key) {
        var t = pf[e.key] || e.key;
        if (t !== 'Unidentified') return t;
      }
      return e.type === 'keypress'
        ? ((e = xr(e)), e === 13 ? 'Enter' : String.fromCharCode(e))
        : e.type === 'keydown' || e.type === 'keyup'
        ? mf[e.keyCode] || 'Unidentified'
        : '';
    },
    code: 0,
    location: 0,
    ctrlKey: 0,
    shiftKey: 0,
    altKey: 0,
    metaKey: 0,
    repeat: 0,
    locale: 0,
    getModifierState: eo,
    charCode: function (e) {
      return e.type === 'keypress' ? xr(e) : 0;
    },
    keyCode: function (e) {
      return e.type === 'keydown' || e.type === 'keyup' ? e.keyCode : 0;
    },
    which: function (e) {
      return e.type === 'keypress'
        ? xr(e)
        : e.type === 'keydown' || e.type === 'keyup'
        ? e.keyCode
        : 0;
    },
  }),
  yf = we(vf),
  bf = V({}, nl, {
    pointerId: 0,
    width: 0,
    height: 0,
    pressure: 0,
    tangentialPressure: 0,
    tiltX: 0,
    tiltY: 0,
    twist: 0,
    pointerType: 0,
    isPrimary: 0,
  }),
  Go = we(bf),
  wf = V({}, Kn, {
    touches: 0,
    targetTouches: 0,
    changedTouches: 0,
    altKey: 0,
    metaKey: 0,
    ctrlKey: 0,
    shiftKey: 0,
    getModifierState: eo,
  }),
  kf = we(wf),
  xf = V({}, an, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }),
  Sf = we(xf),
  _f = V({}, nl, {
    deltaX: function (e) {
      return 'deltaX' in e
        ? e.deltaX
        : 'wheelDeltaX' in e
        ? -e.wheelDeltaX
        : 0;
    },
    deltaY: function (e) {
      return 'deltaY' in e
        ? e.deltaY
        : 'wheelDeltaY' in e
        ? -e.wheelDeltaY
        : 'wheelDelta' in e
        ? -e.wheelDelta
        : 0;
    },
    deltaZ: 0,
    deltaMode: 0,
  }),
  Ef = we(_f),
  Nf = [9, 13, 27, 32],
  to = We && 'CompositionEvent' in window,
  _n = null;
We && 'documentMode' in document && (_n = document.documentMode);
var Cf = We && 'TextEvent' in window && !_n,
  Iu = We && (!to || (_n && 8 < _n && 11 >= _n)),
  Jo = ' ',
  Zo = !1;
function Ou(e, t) {
  switch (e) {
    case 'keyup':
      return Nf.indexOf(t.keyCode) !== -1;
    case 'keydown':
      return t.keyCode !== 229;
    case 'keypress':
    case 'mousedown':
    case 'focusout':
      return !0;
    default:
      return !1;
  }
}
function Du(e) {
  return (e = e.detail), typeof e == 'object' && 'data' in e ? e.data : null;
}
var Ot = !1;
function Pf(e, t) {
  switch (e) {
    case 'compositionend':
      return Du(t);
    case 'keypress':
      return t.which !== 32 ? null : ((Zo = !0), Jo);
    case 'textInput':
      return (e = t.data), e === Jo && Zo ? null : e;
    default:
      return null;
  }
}
function Lf(e, t) {
  if (Ot)
    return e === 'compositionend' || (!to && Ou(e, t))
      ? ((e = Ru()), (kr = Ja = tt = null), (Ot = !1), e)
      : null;
  switch (e) {
    case 'paste':
      return null;
    case 'keypress':
      if (!(t.ctrlKey || t.altKey || t.metaKey) || (t.ctrlKey && t.altKey)) {
        if (t.char && 1 < t.char.length) return t.char;
        if (t.which) return String.fromCharCode(t.which);
      }
      return null;
    case 'compositionend':
      return Iu && t.locale !== 'ko' ? null : t.data;
    default:
      return null;
  }
}
var zf = {
  color: !0,
  date: !0,
  datetime: !0,
  'datetime-local': !0,
  email: !0,
  month: !0,
  number: !0,
  password: !0,
  range: !0,
  search: !0,
  tel: !0,
  text: !0,
  time: !0,
  url: !0,
  week: !0,
};
function ei(e) {
  var t = e && e.nodeName && e.nodeName.toLowerCase();
  return t === 'input' ? !!zf[e.type] : t === 'textarea';
}
function Mu(e, t, n, r) {
  mu(r),
    (t = Mr(t, 'onChange')),
    0 < t.length &&
      ((n = new Za('onChange', 'change', null, n, r)),
      e.push({ event: n, listeners: t }));
}
var En = null,
  Mn = null;
function jf(e) {
  qu(e, 0);
}
function rl(e) {
  var t = Ft(e);
  if (iu(t)) return e;
}
function Tf(e, t) {
  if (e === 'change') return t;
}
var Fu = !1;
if (We) {
  var Pl;
  if (We) {
    var Ll = 'oninput' in document;
    if (!Ll) {
      var ti = document.createElement('div');
      ti.setAttribute('oninput', 'return;'),
        (Ll = typeof ti.oninput == 'function');
    }
    Pl = Ll;
  } else Pl = !1;
  Fu = Pl && (!document.documentMode || 9 < document.documentMode);
}
function ni() {
  En && (En.detachEvent('onpropertychange', Uu), (Mn = En = null));
}
function Uu(e) {
  if (e.propertyName === 'value' && rl(Mn)) {
    var t = [];
    Mu(t, Mn, e, Xa(e)), yu(jf, t);
  }
}
function Rf(e, t, n) {
  e === 'focusin'
    ? (ni(), (En = t), (Mn = n), En.attachEvent('onpropertychange', Uu))
    : e === 'focusout' && ni();
}
function If(e) {
  if (e === 'selectionchange' || e === 'keyup' || e === 'keydown')
    return rl(Mn);
}
function Of(e, t) {
  if (e === 'click') return rl(t);
}
function Df(e, t) {
  if (e === 'input' || e === 'change') return rl(t);
}
function Mf(e, t) {
  return (e === t && (e !== 0 || 1 / e === 1 / t)) || (e !== e && t !== t);
}
var Ie = typeof Object.is == 'function' ? Object.is : Mf;
function Fn(e, t) {
  if (Ie(e, t)) return !0;
  if (typeof e != 'object' || e === null || typeof t != 'object' || t === null)
    return !1;
  var n = Object.keys(e),
    r = Object.keys(t);
  if (n.length !== r.length) return !1;
  for (r = 0; r < n.length; r++) {
    var l = n[r];
    if (!Ql.call(t, l) || !Ie(e[l], t[l])) return !1;
  }
  return !0;
}
function ri(e) {
  for (; e && e.firstChild; ) e = e.firstChild;
  return e;
}
function li(e, t) {
  var n = ri(e);
  e = 0;
  for (var r; n; ) {
    if (n.nodeType === 3) {
      if (((r = e + n.textContent.length), e <= t && r >= t))
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
    n = ri(n);
  }
}
function Au(e, t) {
  return e && t
    ? e === t
      ? !0
      : e && e.nodeType === 3
      ? !1
      : t && t.nodeType === 3
      ? Au(e, t.parentNode)
      : 'contains' in e
      ? e.contains(t)
      : e.compareDocumentPosition
      ? !!(e.compareDocumentPosition(t) & 16)
      : !1
    : !1;
}
function Vu() {
  for (var e = window, t = zr(); t instanceof e.HTMLIFrameElement; ) {
    try {
      var n = typeof t.contentWindow.location.href == 'string';
    } catch {
      n = !1;
    }
    if (n) e = t.contentWindow;
    else break;
    t = zr(e.document);
  }
  return t;
}
function no(e) {
  var t = e && e.nodeName && e.nodeName.toLowerCase();
  return (
    t &&
    ((t === 'input' &&
      (e.type === 'text' ||
        e.type === 'search' ||
        e.type === 'tel' ||
        e.type === 'url' ||
        e.type === 'password')) ||
      t === 'textarea' ||
      e.contentEditable === 'true')
  );
}
function Ff(e) {
  var t = Vu(),
    n = e.focusedElem,
    r = e.selectionRange;
  if (
    t !== n &&
    n &&
    n.ownerDocument &&
    Au(n.ownerDocument.documentElement, n)
  ) {
    if (r !== null && no(n)) {
      if (
        ((t = r.start),
        (e = r.end),
        e === void 0 && (e = t),
        'selectionStart' in n)
      )
        (n.selectionStart = t), (n.selectionEnd = Math.min(e, n.value.length));
      else if (
        ((e = ((t = n.ownerDocument || document) && t.defaultView) || window),
        e.getSelection)
      ) {
        e = e.getSelection();
        var l = n.textContent.length,
          a = Math.min(r.start, l);
        (r = r.end === void 0 ? a : Math.min(r.end, l)),
          !e.extend && a > r && ((l = r), (r = a), (a = l)),
          (l = li(n, a));
        var o = li(n, r);
        l &&
          o &&
          (e.rangeCount !== 1 ||
            e.anchorNode !== l.node ||
            e.anchorOffset !== l.offset ||
            e.focusNode !== o.node ||
            e.focusOffset !== o.offset) &&
          ((t = t.createRange()),
          t.setStart(l.node, l.offset),
          e.removeAllRanges(),
          a > r
            ? (e.addRange(t), e.extend(o.node, o.offset))
            : (t.setEnd(o.node, o.offset), e.addRange(t)));
      }
    }
    for (t = [], e = n; (e = e.parentNode); )
      e.nodeType === 1 &&
        t.push({ element: e, left: e.scrollLeft, top: e.scrollTop });
    for (typeof n.focus == 'function' && n.focus(), n = 0; n < t.length; n++)
      (e = t[n]),
        (e.element.scrollLeft = e.left),
        (e.element.scrollTop = e.top);
  }
}
var Uf = We && 'documentMode' in document && 11 >= document.documentMode,
  Dt = null,
  fa = null,
  Nn = null,
  da = !1;
function ai(e, t, n) {
  var r = n.window === n ? n.document : n.nodeType === 9 ? n : n.ownerDocument;
  da ||
    Dt == null ||
    Dt !== zr(r) ||
    ((r = Dt),
    'selectionStart' in r && no(r)
      ? (r = { start: r.selectionStart, end: r.selectionEnd })
      : ((r = (
          (r.ownerDocument && r.ownerDocument.defaultView) ||
          window
        ).getSelection()),
        (r = {
          anchorNode: r.anchorNode,
          anchorOffset: r.anchorOffset,
          focusNode: r.focusNode,
          focusOffset: r.focusOffset,
        })),
    (Nn && Fn(Nn, r)) ||
      ((Nn = r),
      (r = Mr(fa, 'onSelect')),
      0 < r.length &&
        ((t = new Za('onSelect', 'select', null, t, n)),
        e.push({ event: t, listeners: r }),
        (t.target = Dt))));
}
function sr(e, t) {
  var n = {};
  return (
    (n[e.toLowerCase()] = t.toLowerCase()),
    (n['Webkit' + e] = 'webkit' + t),
    (n['Moz' + e] = 'moz' + t),
    n
  );
}
var Mt = {
    animationend: sr('Animation', 'AnimationEnd'),
    animationiteration: sr('Animation', 'AnimationIteration'),
    animationstart: sr('Animation', 'AnimationStart'),
    transitionend: sr('Transition', 'TransitionEnd'),
  },
  zl = {},
  $u = {};
We &&
  (($u = document.createElement('div').style),
  'AnimationEvent' in window ||
    (delete Mt.animationend.animation,
    delete Mt.animationiteration.animation,
    delete Mt.animationstart.animation),
  'TransitionEvent' in window || delete Mt.transitionend.transition);
function ll(e) {
  if (zl[e]) return zl[e];
  if (!Mt[e]) return e;
  var t = Mt[e],
    n;
  for (n in t) if (t.hasOwnProperty(n) && n in $u) return (zl[e] = t[n]);
  return e;
}
var Hu = ll('animationend'),
  Bu = ll('animationiteration'),
  Wu = ll('animationstart'),
  Qu = ll('transitionend'),
  Xu = new Map(),
  oi =
    'abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel'.split(
      ' '
    );
function pt(e, t) {
  Xu.set(e, t), zt(t, [e]);
}
for (var jl = 0; jl < oi.length; jl++) {
  var Tl = oi[jl],
    Af = Tl.toLowerCase(),
    Vf = Tl[0].toUpperCase() + Tl.slice(1);
  pt(Af, 'on' + Vf);
}
pt(Hu, 'onAnimationEnd');
pt(Bu, 'onAnimationIteration');
pt(Wu, 'onAnimationStart');
pt('dblclick', 'onDoubleClick');
pt('focusin', 'onFocus');
pt('focusout', 'onBlur');
pt(Qu, 'onTransitionEnd');
Gt('onMouseEnter', ['mouseout', 'mouseover']);
Gt('onMouseLeave', ['mouseout', 'mouseover']);
Gt('onPointerEnter', ['pointerout', 'pointerover']);
Gt('onPointerLeave', ['pointerout', 'pointerover']);
zt(
  'onChange',
  'change click focusin focusout input keydown keyup selectionchange'.split(
    ' '
  )
);
zt(
  'onSelect',
  'focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange'.split(
    ' '
  )
);
zt('onBeforeInput', ['compositionend', 'keypress', 'textInput', 'paste']);
zt(
  'onCompositionEnd',
  'compositionend focusout keydown keypress keyup mousedown'.split(' ')
);
zt(
  'onCompositionStart',
  'compositionstart focusout keydown keypress keyup mousedown'.split(' ')
);
zt(
  'onCompositionUpdate',
  'compositionupdate focusout keydown keypress keyup mousedown'.split(' ')
);
var kn =
    'abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting'.split(
      ' '
    ),
  $f = new Set(
    'cancel close invalid load scroll toggle'.split(' ').concat(kn)
  );
function ii(e, t, n) {
  var r = e.type || 'unknown-event';
  (e.currentTarget = n), Uc(r, t, void 0, e), (e.currentTarget = null);
}
function qu(e, t) {
  t = (t & 4) !== 0;
  for (var n = 0; n < e.length; n++) {
    var r = e[n],
      l = r.event;
    r = r.listeners;
    e: {
      var a = void 0;
      if (t)
        for (var o = r.length - 1; 0 <= o; o--) {
          var u = r[o],
            i = u.instance,
            c = u.currentTarget;
          if (((u = u.listener), i !== a && l.isPropagationStopped())) break e;
          ii(l, u, c), (a = i);
        }
      else
        for (o = 0; o < r.length; o++) {
          if (
            ((u = r[o]),
            (i = u.instance),
            (c = u.currentTarget),
            (u = u.listener),
            i !== a && l.isPropagationStopped())
          )
            break e;
          ii(l, u, c), (a = i);
        }
    }
  }
  if (Tr) throw ((e = ia), (Tr = !1), (ia = null), e);
}
function D(e, t) {
  var n = t[va];
  n === void 0 && (n = t[va] = new Set());
  var r = e + '__bubble';
  n.has(r) || (Yu(t, e, 2, !1), n.add(r));
}
function Rl(e, t, n) {
  var r = 0;
  t && (r |= 4), Yu(n, e, r, t);
}
var cr = '_reactListening' + Math.random().toString(36).slice(2);
function Un(e) {
  if (!e[cr]) {
    (e[cr] = !0),
      nu.forEach(function (n) {
        n !== 'selectionchange' && ($f.has(n) || Rl(n, !1, e), Rl(n, !0, e));
      });
    var t = e.nodeType === 9 ? e : e.ownerDocument;
    t === null || t[cr] || ((t[cr] = !0), Rl('selectionchange', !1, t));
  }
}
function Yu(e, t, n, r) {
  switch (Tu(t)) {
    case 1:
      var l = tf;
      break;
    case 4:
      l = nf;
      break;
    default:
      l = Ga;
  }
  (n = l.bind(null, t, n, e)),
    (l = void 0),
    !oa ||
      (t !== 'touchstart' && t !== 'touchmove' && t !== 'wheel') ||
      (l = !0),
    r
      ? l !== void 0
        ? e.addEventListener(t, n, { capture: !0, passive: l })
        : e.addEventListener(t, n, !0)
      : l !== void 0
      ? e.addEventListener(t, n, { passive: l })
      : e.addEventListener(t, n, !1);
}
function Il(e, t, n, r, l) {
  var a = r;
  if (!(t & 1) && !(t & 2) && r !== null)
    e: for (;;) {
      if (r === null) return;
      var o = r.tag;
      if (o === 3 || o === 4) {
        var u = r.stateNode.containerInfo;
        if (u === l || (u.nodeType === 8 && u.parentNode === l)) break;
        if (o === 4)
          for (o = r.return; o !== null; ) {
            var i = o.tag;
            if (
              (i === 3 || i === 4) &&
              ((i = o.stateNode.containerInfo),
              i === l || (i.nodeType === 8 && i.parentNode === l))
            )
              return;
            o = o.return;
          }
        for (; u !== null; ) {
          if (((o = wt(u)), o === null)) return;
          if (((i = o.tag), i === 5 || i === 6)) {
            r = a = o;
            continue e;
          }
          u = u.parentNode;
        }
      }
      r = r.return;
    }
  yu(function () {
    var c = a,
      m = Xa(n),
      h = [];
    e: {
      var p = Xu.get(e);
      if (p !== void 0) {
        var w = Za,
          b = e;
        switch (e) {
          case 'keypress':
            if (xr(n) === 0) break e;
          case 'keydown':
          case 'keyup':
            w = yf;
            break;
          case 'focusin':
            (b = 'focus'), (w = Cl);
            break;
          case 'focusout':
            (b = 'blur'), (w = Cl);
            break;
          case 'beforeblur':
          case 'afterblur':
            w = Cl;
            break;
          case 'click':
            if (n.button === 2) break e;
          case 'auxclick':
          case 'dblclick':
          case 'mousedown':
          case 'mousemove':
          case 'mouseup':
          case 'mouseout':
          case 'mouseover':
          case 'contextmenu':
            w = Yo;
            break;
          case 'drag':
          case 'dragend':
          case 'dragenter':
          case 'dragexit':
          case 'dragleave':
          case 'dragover':
          case 'dragstart':
          case 'drop':
            w = af;
            break;
          case 'touchcancel':
          case 'touchend':
          case 'touchmove':
          case 'touchstart':
            w = kf;
            break;
          case Hu:
          case Bu:
          case Wu:
            w = sf;
            break;
          case Qu:
            w = Sf;
            break;
          case 'scroll':
            w = rf;
            break;
          case 'wheel':
            w = Ef;
            break;
          case 'copy':
          case 'cut':
          case 'paste':
            w = ff;
            break;
          case 'gotpointercapture':
          case 'lostpointercapture':
          case 'pointercancel':
          case 'pointerdown':
          case 'pointermove':
          case 'pointerout':
          case 'pointerover':
          case 'pointerup':
            w = Go;
        }
        var k = (t & 4) !== 0,
          T = !k && e === 'scroll',
          d = k ? (p !== null ? p + 'Capture' : null) : p;
        k = [];
        for (var s = c, f; s !== null; ) {
          f = s;
          var y = f.stateNode;
          if (
            (f.tag === 5 &&
              y !== null &&
              ((f = y),
              d !== null &&
                ((y = Rn(s, d)), y != null && k.push(An(s, y, f)))),
            T)
          )
            break;
          s = s.return;
        }
        0 < k.length &&
          ((p = new w(p, b, null, n, m)), h.push({ event: p, listeners: k }));
      }
    }
    if (!(t & 7)) {
      e: {
        if (
          ((p = e === 'mouseover' || e === 'pointerover'),
          (w = e === 'mouseout' || e === 'pointerout'),
          p &&
            n !== la &&
            (b = n.relatedTarget || n.fromElement) &&
            (wt(b) || b[Qe]))
        )
          break e;
        if (
          (w || p) &&
          ((p =
            m.window === m
              ? m
              : (p = m.ownerDocument)
              ? p.defaultView || p.parentWindow
              : window),
          w
            ? ((b = n.relatedTarget || n.toElement),
              (w = c),
              (b = b ? wt(b) : null),
              b !== null &&
                ((T = jt(b)), b !== T || (b.tag !== 5 && b.tag !== 6)) &&
                (b = null))
            : ((w = null), (b = c)),
          w !== b)
        ) {
          if (
            ((k = Yo),
            (y = 'onMouseLeave'),
            (d = 'onMouseEnter'),
            (s = 'mouse'),
            (e === 'pointerout' || e === 'pointerover') &&
              ((k = Go),
              (y = 'onPointerLeave'),
              (d = 'onPointerEnter'),
              (s = 'pointer')),
            (T = w == null ? p : Ft(w)),
            (f = b == null ? p : Ft(b)),
            (p = new k(y, s + 'leave', w, n, m)),
            (p.target = T),
            (p.relatedTarget = f),
            (y = null),
            wt(m) === c &&
              ((k = new k(d, s + 'enter', b, n, m)),
              (k.target = f),
              (k.relatedTarget = T),
              (y = k)),
            (T = y),
            w && b)
          )
            t: {
              for (k = w, d = b, s = 0, f = k; f; f = Tt(f)) s++;
              for (f = 0, y = d; y; y = Tt(y)) f++;
              for (; 0 < s - f; ) (k = Tt(k)), s--;
              for (; 0 < f - s; ) (d = Tt(d)), f--;
              for (; s--; ) {
                if (k === d || (d !== null && k === d.alternate)) break t;
                (k = Tt(k)), (d = Tt(d));
              }
              k = null;
            }
          else k = null;
          w !== null && ui(h, p, w, k, !1),
            b !== null && T !== null && ui(h, T, b, k, !0);
        }
      }
      e: {
        if (
          ((p = c ? Ft(c) : window),
          (w = p.nodeName && p.nodeName.toLowerCase()),
          w === 'select' || (w === 'input' && p.type === 'file'))
        )
          var _ = Tf;
        else if (ei(p))
          if (Fu) _ = Df;
          else {
            _ = If;
            var E = Rf;
          }
        else
          (w = p.nodeName) &&
            w.toLowerCase() === 'input' &&
            (p.type === 'checkbox' || p.type === 'radio') &&
            (_ = Of);
        if (_ && (_ = _(e, c))) {
          Mu(h, _, n, m);
          break e;
        }
        E && E(e, p, c),
          e === 'focusout' &&
            (E = p._wrapperState) &&
            E.controlled &&
            p.type === 'number' &&
            Zl(p, 'number', p.value);
      }
      switch (((E = c ? Ft(c) : window), e)) {
        case 'focusin':
          (ei(E) || E.contentEditable === 'true') &&
            ((Dt = E), (fa = c), (Nn = null));
          break;
        case 'focusout':
          Nn = fa = Dt = null;
          break;
        case 'mousedown':
          da = !0;
          break;
        case 'contextmenu':
        case 'mouseup':
        case 'dragend':
          (da = !1), ai(h, n, m);
          break;
        case 'selectionchange':
          if (Uf) break;
        case 'keydown':
        case 'keyup':
          ai(h, n, m);
      }
      var N;
      if (to)
        e: {
          switch (e) {
            case 'compositionstart':
              var C = 'onCompositionStart';
              break e;
            case 'compositionend':
              C = 'onCompositionEnd';
              break e;
            case 'compositionupdate':
              C = 'onCompositionUpdate';
              break e;
          }
          C = void 0;
        }
      else
        Ot
          ? Ou(e, n) && (C = 'onCompositionEnd')
          : e === 'keydown' && n.keyCode === 229 && (C = 'onCompositionStart');
      C &&
        (Iu &&
          n.locale !== 'ko' &&
          (Ot || C !== 'onCompositionStart'
            ? C === 'onCompositionEnd' && Ot && (N = Ru())
            : ((tt = m),
              (Ja = 'value' in tt ? tt.value : tt.textContent),
              (Ot = !0))),
        (E = Mr(c, C)),
        0 < E.length &&
          ((C = new Ko(C, e, null, n, m)),
          h.push({ event: C, listeners: E }),
          N ? (C.data = N) : ((N = Du(n)), N !== null && (C.data = N)))),
        (N = Cf ? Pf(e, n) : Lf(e, n)) &&
          ((c = Mr(c, 'onBeforeInput')),
          0 < c.length &&
            ((m = new Ko('onBeforeInput', 'beforeinput', null, n, m)),
            h.push({ event: m, listeners: c }),
            (m.data = N)));
    }
    qu(h, t);
  });
}
function An(e, t, n) {
  return { instance: e, listener: t, currentTarget: n };
}
function Mr(e, t) {
  for (var n = t + 'Capture', r = []; e !== null; ) {
    var l = e,
      a = l.stateNode;
    l.tag === 5 &&
      a !== null &&
      ((l = a),
      (a = Rn(e, n)),
      a != null && r.unshift(An(e, a, l)),
      (a = Rn(e, t)),
      a != null && r.push(An(e, a, l))),
      (e = e.return);
  }
  return r;
}
function Tt(e) {
  if (e === null) return null;
  do e = e.return;
  while (e && e.tag !== 5);
  return e || null;
}
function ui(e, t, n, r, l) {
  for (var a = t._reactName, o = []; n !== null && n !== r; ) {
    var u = n,
      i = u.alternate,
      c = u.stateNode;
    if (i !== null && i === r) break;
    u.tag === 5 &&
      c !== null &&
      ((u = c),
      l
        ? ((i = Rn(n, a)), i != null && o.unshift(An(n, i, u)))
        : l || ((i = Rn(n, a)), i != null && o.push(An(n, i, u)))),
      (n = n.return);
  }
  o.length !== 0 && e.push({ event: t, listeners: o });
}
var Hf = /\r\n?/g,
  Bf = /\u0000|\uFFFD/g;
function si(e) {
  return (typeof e == 'string' ? e : '' + e)
    .replace(
      Hf,
      `
`
    )
    .replace(Bf, '');
}
function fr(e, t, n) {
  if (((t = si(t)), si(e) !== t && n)) throw Error(v(425));
}
function Fr() {}
var pa = null,
  ma = null;
function ha(e, t) {
  return (
    e === 'textarea' ||
    e === 'noscript' ||
    typeof t.children == 'string' ||
    typeof t.children == 'number' ||
    (typeof t.dangerouslySetInnerHTML == 'object' &&
      t.dangerouslySetInnerHTML !== null &&
      t.dangerouslySetInnerHTML.__html != null)
  );
}
var ga = typeof setTimeout == 'function' ? setTimeout : void 0,
  Wf = typeof clearTimeout == 'function' ? clearTimeout : void 0,
  ci = typeof Promise == 'function' ? Promise : void 0,
  Qf =
    typeof queueMicrotask == 'function'
      ? queueMicrotask
      : typeof ci < 'u'
      ? function (e) {
          return ci.resolve(null).then(e).catch(Xf);
        }
      : ga;
function Xf(e) {
  setTimeout(function () {
    throw e;
  });
}
function Ol(e, t) {
  var n = t,
    r = 0;
  do {
    var l = n.nextSibling;
    if ((e.removeChild(n), l && l.nodeType === 8))
      if (((n = l.data), n === '/$')) {
        if (r === 0) {
          e.removeChild(l), Dn(t);
          return;
        }
        r--;
      } else (n !== '$' && n !== '$?' && n !== '$!') || r++;
    n = l;
  } while (n);
  Dn(t);
}
function ot(e) {
  for (; e != null; e = e.nextSibling) {
    var t = e.nodeType;
    if (t === 1 || t === 3) break;
    if (t === 8) {
      if (((t = e.data), t === '$' || t === '$!' || t === '$?')) break;
      if (t === '/$') return null;
    }
  }
  return e;
}
function fi(e) {
  e = e.previousSibling;
  for (var t = 0; e; ) {
    if (e.nodeType === 8) {
      var n = e.data;
      if (n === '$' || n === '$!' || n === '$?') {
        if (t === 0) return e;
        t--;
      } else n === '/$' && t++;
    }
    e = e.previousSibling;
  }
  return null;
}
var on = Math.random().toString(36).slice(2),
  Me = '__reactFiber$' + on,
  Vn = '__reactProps$' + on,
  Qe = '__reactContainer$' + on,
  va = '__reactEvents$' + on,
  qf = '__reactListeners$' + on,
  Yf = '__reactHandles$' + on;
function wt(e) {
  var t = e[Me];
  if (t) return t;
  for (var n = e.parentNode; n; ) {
    if ((t = n[Qe] || n[Me])) {
      if (
        ((n = t.alternate),
        t.child !== null || (n !== null && n.child !== null))
      )
        for (e = fi(e); e !== null; ) {
          if ((n = e[Me])) return n;
          e = fi(e);
        }
      return t;
    }
    (e = n), (n = e.parentNode);
  }
  return null;
}
function Gn(e) {
  return (
    (e = e[Me] || e[Qe]),
    !e || (e.tag !== 5 && e.tag !== 6 && e.tag !== 13 && e.tag !== 3)
      ? null
      : e
  );
}
function Ft(e) {
  if (e.tag === 5 || e.tag === 6) return e.stateNode;
  throw Error(v(33));
}
function al(e) {
  return e[Vn] || null;
}
var ya = [],
  Ut = -1;
function mt(e) {
  return { current: e };
}
function M(e) {
  0 > Ut || ((e.current = ya[Ut]), (ya[Ut] = null), Ut--);
}
function O(e, t) {
  Ut++, (ya[Ut] = e.current), (e.current = t);
}
var dt = {},
  ae = mt(dt),
  de = mt(!1),
  Et = dt;
function Jt(e, t) {
  var n = e.type.contextTypes;
  if (!n) return dt;
  var r = e.stateNode;
  if (r && r.__reactInternalMemoizedUnmaskedChildContext === t)
    return r.__reactInternalMemoizedMaskedChildContext;
  var l = {},
    a;
  for (a in n) l[a] = t[a];
  return (
    r &&
      ((e = e.stateNode),
      (e.__reactInternalMemoizedUnmaskedChildContext = t),
      (e.__reactInternalMemoizedMaskedChildContext = l)),
    l
  );
}
function pe(e) {
  return (e = e.childContextTypes), e != null;
}
function Ur() {
  M(de), M(ae);
}
function di(e, t, n) {
  if (ae.current !== dt) throw Error(v(168));
  O(ae, t), O(de, n);
}
function Ku(e, t, n) {
  var r = e.stateNode;
  if (((t = t.childContextTypes), typeof r.getChildContext != 'function'))
    return n;
  r = r.getChildContext();
  for (var l in r) if (!(l in t)) throw Error(v(108, Tc(e) || 'Unknown', l));
  return V({}, n, r);
}
function Ar(e) {
  return (
    (e =
      ((e = e.stateNode) && e.__reactInternalMemoizedMergedChildContext) ||
      dt),
    (Et = ae.current),
    O(ae, e),
    O(de, de.current),
    !0
  );
}
function pi(e, t, n) {
  var r = e.stateNode;
  if (!r) throw Error(v(169));
  n
    ? ((e = Ku(e, t, Et)),
      (r.__reactInternalMemoizedMergedChildContext = e),
      M(de),
      M(ae),
      O(ae, e))
    : M(de),
    O(de, n);
}
var Ve = null,
  ol = !1,
  Dl = !1;
function Gu(e) {
  Ve === null ? (Ve = [e]) : Ve.push(e);
}
function Kf(e) {
  (ol = !0), Gu(e);
}
function ht() {
  if (!Dl && Ve !== null) {
    Dl = !0;
    var e = 0,
      t = I;
    try {
      var n = Ve;
      for (I = 1; e < n.length; e++) {
        var r = n[e];
        do r = r(!0);
        while (r !== null);
      }
      (Ve = null), (ol = !1);
    } catch (l) {
      throw (Ve !== null && (Ve = Ve.slice(e + 1)), xu(qa, ht), l);
    } finally {
      (I = t), (Dl = !1);
    }
  }
  return null;
}
var At = [],
  Vt = 0,
  Vr = null,
  $r = 0,
  ke = [],
  xe = 0,
  Nt = null,
  $e = 1,
  He = '';
function yt(e, t) {
  (At[Vt++] = $r), (At[Vt++] = Vr), (Vr = e), ($r = t);
}
function Ju(e, t, n) {
  (ke[xe++] = $e), (ke[xe++] = He), (ke[xe++] = Nt), (Nt = e);
  var r = $e;
  e = He;
  var l = 32 - Te(r) - 1;
  (r &= ~(1 << l)), (n += 1);
  var a = 32 - Te(t) + l;
  if (30 < a) {
    var o = l - (l % 5);
    (a = (r & ((1 << o) - 1)).toString(32)),
      (r >>= o),
      (l -= o),
      ($e = (1 << (32 - Te(t) + l)) | (n << l) | r),
      (He = a + e);
  } else ($e = (1 << a) | (n << l) | r), (He = e);
}
function ro(e) {
  e.return !== null && (yt(e, 1), Ju(e, 1, 0));
}
function lo(e) {
  for (; e === Vr; )
    (Vr = At[--Vt]), (At[Vt] = null), ($r = At[--Vt]), (At[Vt] = null);
  for (; e === Nt; )
    (Nt = ke[--xe]),
      (ke[xe] = null),
      (He = ke[--xe]),
      (ke[xe] = null),
      ($e = ke[--xe]),
      (ke[xe] = null);
}
var ve = null,
  ge = null,
  F = !1,
  je = null;
function Zu(e, t) {
  var n = Se(5, null, null, 0);
  (n.elementType = 'DELETED'),
    (n.stateNode = t),
    (n.return = e),
    (t = e.deletions),
    t === null ? ((e.deletions = [n]), (e.flags |= 16)) : t.push(n);
}
function mi(e, t) {
  switch (e.tag) {
    case 5:
      var n = e.type;
      return (
        (t =
          t.nodeType !== 1 || n.toLowerCase() !== t.nodeName.toLowerCase()
            ? null
            : t),
        t !== null
          ? ((e.stateNode = t), (ve = e), (ge = ot(t.firstChild)), !0)
          : !1
      );
    case 6:
      return (
        (t = e.pendingProps === '' || t.nodeType !== 3 ? null : t),
        t !== null ? ((e.stateNode = t), (ve = e), (ge = null), !0) : !1
      );
    case 13:
      return (
        (t = t.nodeType !== 8 ? null : t),
        t !== null
          ? ((n = Nt !== null ? { id: $e, overflow: He } : null),
            (e.memoizedState = {
              dehydrated: t,
              treeContext: n,
              retryLane: 1073741824,
            }),
            (n = Se(18, null, null, 0)),
            (n.stateNode = t),
            (n.return = e),
            (e.child = n),
            (ve = e),
            (ge = null),
            !0)
          : !1
      );
    default:
      return !1;
  }
}
function ba(e) {
  return (e.mode & 1) !== 0 && (e.flags & 128) === 0;
}
function wa(e) {
  if (F) {
    var t = ge;
    if (t) {
      var n = t;
      if (!mi(e, t)) {
        if (ba(e)) throw Error(v(418));
        t = ot(n.nextSibling);
        var r = ve;
        t && mi(e, t)
          ? Zu(r, n)
          : ((e.flags = (e.flags & -4097) | 2), (F = !1), (ve = e));
      }
    } else {
      if (ba(e)) throw Error(v(418));
      (e.flags = (e.flags & -4097) | 2), (F = !1), (ve = e);
    }
  }
}
function hi(e) {
  for (
    e = e.return;
    e !== null && e.tag !== 5 && e.tag !== 3 && e.tag !== 13;

  )
    e = e.return;
  ve = e;
}
function dr(e) {
  if (e !== ve) return !1;
  if (!F) return hi(e), (F = !0), !1;
  var t;
  if (
    ((t = e.tag !== 3) &&
      !(t = e.tag !== 5) &&
      ((t = e.type),
      (t = t !== 'head' && t !== 'body' && !ha(e.type, e.memoizedProps))),
    t && (t = ge))
  ) {
    if (ba(e)) throw (es(), Error(v(418)));
    for (; t; ) Zu(e, t), (t = ot(t.nextSibling));
  }
  if ((hi(e), e.tag === 13)) {
    if (((e = e.memoizedState), (e = e !== null ? e.dehydrated : null), !e))
      throw Error(v(317));
    e: {
      for (e = e.nextSibling, t = 0; e; ) {
        if (e.nodeType === 8) {
          var n = e.data;
          if (n === '/$') {
            if (t === 0) {
              ge = ot(e.nextSibling);
              break e;
            }
            t--;
          } else (n !== '$' && n !== '$!' && n !== '$?') || t++;
        }
        e = e.nextSibling;
      }
      ge = null;
    }
  } else ge = ve ? ot(e.stateNode.nextSibling) : null;
  return !0;
}
function es() {
  for (var e = ge; e; ) e = ot(e.nextSibling);
}
function Zt() {
  (ge = ve = null), (F = !1);
}
function ao(e) {
  je === null ? (je = [e]) : je.push(e);
}
var Gf = Ye.ReactCurrentBatchConfig;
function hn(e, t, n) {
  if (
    ((e = n.ref), e !== null && typeof e != 'function' && typeof e != 'object')
  ) {
    if (n._owner) {
      if (((n = n._owner), n)) {
        if (n.tag !== 1) throw Error(v(309));
        var r = n.stateNode;
      }
      if (!r) throw Error(v(147, e));
      var l = r,
        a = '' + e;
      return t !== null &&
        t.ref !== null &&
        typeof t.ref == 'function' &&
        t.ref._stringRef === a
        ? t.ref
        : ((t = function (o) {
            var u = l.refs;
            o === null ? delete u[a] : (u[a] = o);
          }),
          (t._stringRef = a),
          t);
    }
    if (typeof e != 'string') throw Error(v(284));
    if (!n._owner) throw Error(v(290, e));
  }
  return e;
}
function pr(e, t) {
  throw (
    ((e = Object.prototype.toString.call(t)),
    Error(
      v(
        31,
        e === '[object Object]'
          ? 'object with keys {' + Object.keys(t).join(', ') + '}'
          : e
      )
    ))
  );
}
function gi(e) {
  var t = e._init;
  return t(e._payload);
}
function ts(e) {
  function t(d, s) {
    if (e) {
      var f = d.deletions;
      f === null ? ((d.deletions = [s]), (d.flags |= 16)) : f.push(s);
    }
  }
  function n(d, s) {
    if (!e) return null;
    for (; s !== null; ) t(d, s), (s = s.sibling);
    return null;
  }
  function r(d, s) {
    for (d = new Map(); s !== null; )
      s.key !== null ? d.set(s.key, s) : d.set(s.index, s), (s = s.sibling);
    return d;
  }
  function l(d, s) {
    return (d = ct(d, s)), (d.index = 0), (d.sibling = null), d;
  }
  function a(d, s, f) {
    return (
      (d.index = f),
      e
        ? ((f = d.alternate),
          f !== null
            ? ((f = f.index), f < s ? ((d.flags |= 2), s) : f)
            : ((d.flags |= 2), s))
        : ((d.flags |= 1048576), s)
    );
  }
  function o(d) {
    return e && d.alternate === null && (d.flags |= 2), d;
  }
  function u(d, s, f, y) {
    return s === null || s.tag !== 6
      ? ((s = Hl(f, d.mode, y)), (s.return = d), s)
      : ((s = l(s, f)), (s.return = d), s);
  }
  function i(d, s, f, y) {
    var _ = f.type;
    return _ === It
      ? m(d, s, f.props.children, y, f.key)
      : s !== null &&
        (s.elementType === _ ||
          (typeof _ == 'object' &&
            _ !== null &&
            _.$$typeof === Ge &&
            gi(_) === s.type))
      ? ((y = l(s, f.props)), (y.ref = hn(d, s, f)), (y.return = d), y)
      : ((y = Lr(f.type, f.key, f.props, null, d.mode, y)),
        (y.ref = hn(d, s, f)),
        (y.return = d),
        y);
  }
  function c(d, s, f, y) {
    return s === null ||
      s.tag !== 4 ||
      s.stateNode.containerInfo !== f.containerInfo ||
      s.stateNode.implementation !== f.implementation
      ? ((s = Bl(f, d.mode, y)), (s.return = d), s)
      : ((s = l(s, f.children || [])), (s.return = d), s);
  }
  function m(d, s, f, y, _) {
    return s === null || s.tag !== 7
      ? ((s = _t(f, d.mode, y, _)), (s.return = d), s)
      : ((s = l(s, f)), (s.return = d), s);
  }
  function h(d, s, f) {
    if ((typeof s == 'string' && s !== '') || typeof s == 'number')
      return (s = Hl('' + s, d.mode, f)), (s.return = d), s;
    if (typeof s == 'object' && s !== null) {
      switch (s.$$typeof) {
        case nr:
          return (
            (f = Lr(s.type, s.key, s.props, null, d.mode, f)),
            (f.ref = hn(d, null, s)),
            (f.return = d),
            f
          );
        case Rt:
          return (s = Bl(s, d.mode, f)), (s.return = d), s;
        case Ge:
          var y = s._init;
          return h(d, y(s._payload), f);
      }
      if (bn(s) || cn(s))
        return (s = _t(s, d.mode, f, null)), (s.return = d), s;
      pr(d, s);
    }
    return null;
  }
  function p(d, s, f, y) {
    var _ = s !== null ? s.key : null;
    if ((typeof f == 'string' && f !== '') || typeof f == 'number')
      return _ !== null ? null : u(d, s, '' + f, y);
    if (typeof f == 'object' && f !== null) {
      switch (f.$$typeof) {
        case nr:
          return f.key === _ ? i(d, s, f, y) : null;
        case Rt:
          return f.key === _ ? c(d, s, f, y) : null;
        case Ge:
          return (_ = f._init), p(d, s, _(f._payload), y);
      }
      if (bn(f) || cn(f)) return _ !== null ? null : m(d, s, f, y, null);
      pr(d, f);
    }
    return null;
  }
  function w(d, s, f, y, _) {
    if ((typeof y == 'string' && y !== '') || typeof y == 'number')
      return (d = d.get(f) || null), u(s, d, '' + y, _);
    if (typeof y == 'object' && y !== null) {
      switch (y.$$typeof) {
        case nr:
          return (
            (d = d.get(y.key === null ? f : y.key) || null), i(s, d, y, _)
          );
        case Rt:
          return (
            (d = d.get(y.key === null ? f : y.key) || null), c(s, d, y, _)
          );
        case Ge:
          var E = y._init;
          return w(d, s, f, E(y._payload), _);
      }
      if (bn(y) || cn(y)) return (d = d.get(f) || null), m(s, d, y, _, null);
      pr(s, y);
    }
    return null;
  }
  function b(d, s, f, y) {
    for (
      var _ = null, E = null, N = s, C = (s = 0), H = null;
      N !== null && C < f.length;
      C++
    ) {
      N.index > C ? ((H = N), (N = null)) : (H = N.sibling);
      var j = p(d, N, f[C], y);
      if (j === null) {
        N === null && (N = H);
        break;
      }
      e && N && j.alternate === null && t(d, N),
        (s = a(j, s, C)),
        E === null ? (_ = j) : (E.sibling = j),
        (E = j),
        (N = H);
    }
    if (C === f.length) return n(d, N), F && yt(d, C), _;
    if (N === null) {
      for (; C < f.length; C++)
        (N = h(d, f[C], y)),
          N !== null &&
            ((s = a(N, s, C)),
            E === null ? (_ = N) : (E.sibling = N),
            (E = N));
      return F && yt(d, C), _;
    }
    for (N = r(d, N); C < f.length; C++)
      (H = w(N, d, C, f[C], y)),
        H !== null &&
          (e && H.alternate !== null && N.delete(H.key === null ? C : H.key),
          (s = a(H, s, C)),
          E === null ? (_ = H) : (E.sibling = H),
          (E = H));
    return (
      e &&
        N.forEach(function (Ce) {
          return t(d, Ce);
        }),
      F && yt(d, C),
      _
    );
  }
  function k(d, s, f, y) {
    var _ = cn(f);
    if (typeof _ != 'function') throw Error(v(150));
    if (((f = _.call(f)), f == null)) throw Error(v(151));
    for (
      var E = (_ = null), N = s, C = (s = 0), H = null, j = f.next();
      N !== null && !j.done;
      C++, j = f.next()
    ) {
      N.index > C ? ((H = N), (N = null)) : (H = N.sibling);
      var Ce = p(d, N, j.value, y);
      if (Ce === null) {
        N === null && (N = H);
        break;
      }
      e && N && Ce.alternate === null && t(d, N),
        (s = a(Ce, s, C)),
        E === null ? (_ = Ce) : (E.sibling = Ce),
        (E = Ce),
        (N = H);
    }
    if (j.done) return n(d, N), F && yt(d, C), _;
    if (N === null) {
      for (; !j.done; C++, j = f.next())
        (j = h(d, j.value, y)),
          j !== null &&
            ((s = a(j, s, C)),
            E === null ? (_ = j) : (E.sibling = j),
            (E = j));
      return F && yt(d, C), _;
    }
    for (N = r(d, N); !j.done; C++, j = f.next())
      (j = w(N, d, C, j.value, y)),
        j !== null &&
          (e && j.alternate !== null && N.delete(j.key === null ? C : j.key),
          (s = a(j, s, C)),
          E === null ? (_ = j) : (E.sibling = j),
          (E = j));
    return (
      e &&
        N.forEach(function (un) {
          return t(d, un);
        }),
      F && yt(d, C),
      _
    );
  }
  function T(d, s, f, y) {
    if (
      (typeof f == 'object' &&
        f !== null &&
        f.type === It &&
        f.key === null &&
        (f = f.props.children),
      typeof f == 'object' && f !== null)
    ) {
      switch (f.$$typeof) {
        case nr:
          e: {
            for (var _ = f.key, E = s; E !== null; ) {
              if (E.key === _) {
                if (((_ = f.type), _ === It)) {
                  if (E.tag === 7) {
                    n(d, E.sibling),
                      (s = l(E, f.props.children)),
                      (s.return = d),
                      (d = s);
                    break e;
                  }
                } else if (
                  E.elementType === _ ||
                  (typeof _ == 'object' &&
                    _ !== null &&
                    _.$$typeof === Ge &&
                    gi(_) === E.type)
                ) {
                  n(d, E.sibling),
                    (s = l(E, f.props)),
                    (s.ref = hn(d, E, f)),
                    (s.return = d),
                    (d = s);
                  break e;
                }
                n(d, E);
                break;
              } else t(d, E);
              E = E.sibling;
            }
            f.type === It
              ? ((s = _t(f.props.children, d.mode, y, f.key)),
                (s.return = d),
                (d = s))
              : ((y = Lr(f.type, f.key, f.props, null, d.mode, y)),
                (y.ref = hn(d, s, f)),
                (y.return = d),
                (d = y));
          }
          return o(d);
        case Rt:
          e: {
            for (E = f.key; s !== null; ) {
              if (s.key === E)
                if (
                  s.tag === 4 &&
                  s.stateNode.containerInfo === f.containerInfo &&
                  s.stateNode.implementation === f.implementation
                ) {
                  n(d, s.sibling),
                    (s = l(s, f.children || [])),
                    (s.return = d),
                    (d = s);
                  break e;
                } else {
                  n(d, s);
                  break;
                }
              else t(d, s);
              s = s.sibling;
            }
            (s = Bl(f, d.mode, y)), (s.return = d), (d = s);
          }
          return o(d);
        case Ge:
          return (E = f._init), T(d, s, E(f._payload), y);
      }
      if (bn(f)) return b(d, s, f, y);
      if (cn(f)) return k(d, s, f, y);
      pr(d, f);
    }
    return (typeof f == 'string' && f !== '') || typeof f == 'number'
      ? ((f = '' + f),
        s !== null && s.tag === 6
          ? (n(d, s.sibling), (s = l(s, f)), (s.return = d), (d = s))
          : (n(d, s), (s = Hl(f, d.mode, y)), (s.return = d), (d = s)),
        o(d))
      : n(d, s);
  }
  return T;
}
var en = ts(!0),
  ns = ts(!1),
  Hr = mt(null),
  Br = null,
  $t = null,
  oo = null;
function io() {
  oo = $t = Br = null;
}
function uo(e) {
  var t = Hr.current;
  M(Hr), (e._currentValue = t);
}
function ka(e, t, n) {
  for (; e !== null; ) {
    var r = e.alternate;
    if (
      ((e.childLanes & t) !== t
        ? ((e.childLanes |= t), r !== null && (r.childLanes |= t))
        : r !== null && (r.childLanes & t) !== t && (r.childLanes |= t),
      e === n)
    )
      break;
    e = e.return;
  }
}
function Yt(e, t) {
  (Br = e),
    (oo = $t = null),
    (e = e.dependencies),
    e !== null &&
      e.firstContext !== null &&
      (e.lanes & t && (fe = !0), (e.firstContext = null));
}
function Ee(e) {
  var t = e._currentValue;
  if (oo !== e)
    if (((e = { context: e, memoizedValue: t, next: null }), $t === null)) {
      if (Br === null) throw Error(v(308));
      ($t = e), (Br.dependencies = { lanes: 0, firstContext: e });
    } else $t = $t.next = e;
  return t;
}
var kt = null;
function so(e) {
  kt === null ? (kt = [e]) : kt.push(e);
}
function rs(e, t, n, r) {
  var l = t.interleaved;
  return (
    l === null ? ((n.next = n), so(t)) : ((n.next = l.next), (l.next = n)),
    (t.interleaved = n),
    Xe(e, r)
  );
}
function Xe(e, t) {
  e.lanes |= t;
  var n = e.alternate;
  for (n !== null && (n.lanes |= t), n = e, e = e.return; e !== null; )
    (e.childLanes |= t),
      (n = e.alternate),
      n !== null && (n.childLanes |= t),
      (n = e),
      (e = e.return);
  return n.tag === 3 ? n.stateNode : null;
}
var Je = !1;
function co(e) {
  e.updateQueue = {
    baseState: e.memoizedState,
    firstBaseUpdate: null,
    lastBaseUpdate: null,
    shared: { pending: null, interleaved: null, lanes: 0 },
    effects: null,
  };
}
function ls(e, t) {
  (e = e.updateQueue),
    t.updateQueue === e &&
      (t.updateQueue = {
        baseState: e.baseState,
        firstBaseUpdate: e.firstBaseUpdate,
        lastBaseUpdate: e.lastBaseUpdate,
        shared: e.shared,
        effects: e.effects,
      });
}
function Be(e, t) {
  return {
    eventTime: e,
    lane: t,
    tag: 0,
    payload: null,
    callback: null,
    next: null,
  };
}
function it(e, t, n) {
  var r = e.updateQueue;
  if (r === null) return null;
  if (((r = r.shared), R & 2)) {
    var l = r.pending;
    return (
      l === null ? (t.next = t) : ((t.next = l.next), (l.next = t)),
      (r.pending = t),
      Xe(e, n)
    );
  }
  return (
    (l = r.interleaved),
    l === null ? ((t.next = t), so(r)) : ((t.next = l.next), (l.next = t)),
    (r.interleaved = t),
    Xe(e, n)
  );
}
function Sr(e, t, n) {
  if (
    ((t = t.updateQueue), t !== null && ((t = t.shared), (n & 4194240) !== 0))
  ) {
    var r = t.lanes;
    (r &= e.pendingLanes), (n |= r), (t.lanes = n), Ya(e, n);
  }
}
function vi(e, t) {
  var n = e.updateQueue,
    r = e.alternate;
  if (r !== null && ((r = r.updateQueue), n === r)) {
    var l = null,
      a = null;
    if (((n = n.firstBaseUpdate), n !== null)) {
      do {
        var o = {
          eventTime: n.eventTime,
          lane: n.lane,
          tag: n.tag,
          payload: n.payload,
          callback: n.callback,
          next: null,
        };
        a === null ? (l = a = o) : (a = a.next = o), (n = n.next);
      } while (n !== null);
      a === null ? (l = a = t) : (a = a.next = t);
    } else l = a = t;
    (n = {
      baseState: r.baseState,
      firstBaseUpdate: l,
      lastBaseUpdate: a,
      shared: r.shared,
      effects: r.effects,
    }),
      (e.updateQueue = n);
    return;
  }
  (e = n.lastBaseUpdate),
    e === null ? (n.firstBaseUpdate = t) : (e.next = t),
    (n.lastBaseUpdate = t);
}
function Wr(e, t, n, r) {
  var l = e.updateQueue;
  Je = !1;
  var a = l.firstBaseUpdate,
    o = l.lastBaseUpdate,
    u = l.shared.pending;
  if (u !== null) {
    l.shared.pending = null;
    var i = u,
      c = i.next;
    (i.next = null), o === null ? (a = c) : (o.next = c), (o = i);
    var m = e.alternate;
    m !== null &&
      ((m = m.updateQueue),
      (u = m.lastBaseUpdate),
      u !== o &&
        (u === null ? (m.firstBaseUpdate = c) : (u.next = c),
        (m.lastBaseUpdate = i)));
  }
  if (a !== null) {
    var h = l.baseState;
    (o = 0), (m = c = i = null), (u = a);
    do {
      var p = u.lane,
        w = u.eventTime;
      if ((r & p) === p) {
        m !== null &&
          (m = m.next =
            {
              eventTime: w,
              lane: 0,
              tag: u.tag,
              payload: u.payload,
              callback: u.callback,
              next: null,
            });
        e: {
          var b = e,
            k = u;
          switch (((p = t), (w = n), k.tag)) {
            case 1:
              if (((b = k.payload), typeof b == 'function')) {
                h = b.call(w, h, p);
                break e;
              }
              h = b;
              break e;
            case 3:
              b.flags = (b.flags & -65537) | 128;
            case 0:
              if (
                ((b = k.payload),
                (p = typeof b == 'function' ? b.call(w, h, p) : b),
                p == null)
              )
                break e;
              h = V({}, h, p);
              break e;
            case 2:
              Je = !0;
          }
        }
        u.callback !== null &&
          u.lane !== 0 &&
          ((e.flags |= 64),
          (p = l.effects),
          p === null ? (l.effects = [u]) : p.push(u));
      } else
        (w = {
          eventTime: w,
          lane: p,
          tag: u.tag,
          payload: u.payload,
          callback: u.callback,
          next: null,
        }),
          m === null ? ((c = m = w), (i = h)) : (m = m.next = w),
          (o |= p);
      if (((u = u.next), u === null)) {
        if (((u = l.shared.pending), u === null)) break;
        (p = u),
          (u = p.next),
          (p.next = null),
          (l.lastBaseUpdate = p),
          (l.shared.pending = null);
      }
    } while (!0);
    if (
      (m === null && (i = h),
      (l.baseState = i),
      (l.firstBaseUpdate = c),
      (l.lastBaseUpdate = m),
      (t = l.shared.interleaved),
      t !== null)
    ) {
      l = t;
      do (o |= l.lane), (l = l.next);
      while (l !== t);
    } else a === null && (l.shared.lanes = 0);
    (Pt |= o), (e.lanes = o), (e.memoizedState = h);
  }
}
function yi(e, t, n) {
  if (((e = t.effects), (t.effects = null), e !== null))
    for (t = 0; t < e.length; t++) {
      var r = e[t],
        l = r.callback;
      if (l !== null) {
        if (((r.callback = null), (r = n), typeof l != 'function'))
          throw Error(v(191, l));
        l.call(r);
      }
    }
}
var Jn = {},
  Ue = mt(Jn),
  $n = mt(Jn),
  Hn = mt(Jn);
function xt(e) {
  if (e === Jn) throw Error(v(174));
  return e;
}
function fo(e, t) {
  switch ((O(Hn, t), O($n, e), O(Ue, Jn), (e = t.nodeType), e)) {
    case 9:
    case 11:
      t = (t = t.documentElement) ? t.namespaceURI : ta(null, '');
      break;
    default:
      (e = e === 8 ? t.parentNode : t),
        (t = e.namespaceURI || null),
        (e = e.tagName),
        (t = ta(t, e));
  }
  M(Ue), O(Ue, t);
}
function tn() {
  M(Ue), M($n), M(Hn);
}
function as(e) {
  xt(Hn.current);
  var t = xt(Ue.current),
    n = ta(t, e.type);
  t !== n && (O($n, e), O(Ue, n));
}
function po(e) {
  $n.current === e && (M(Ue), M($n));
}
var U = mt(0);
function Qr(e) {
  for (var t = e; t !== null; ) {
    if (t.tag === 13) {
      var n = t.memoizedState;
      if (
        n !== null &&
        ((n = n.dehydrated), n === null || n.data === '$?' || n.data === '$!')
      )
        return t;
    } else if (t.tag === 19 && t.memoizedProps.revealOrder !== void 0) {
      if (t.flags & 128) return t;
    } else if (t.child !== null) {
      (t.child.return = t), (t = t.child);
      continue;
    }
    if (t === e) break;
    for (; t.sibling === null; ) {
      if (t.return === null || t.return === e) return null;
      t = t.return;
    }
    (t.sibling.return = t.return), (t = t.sibling);
  }
  return null;
}
var Ml = [];
function mo() {
  for (var e = 0; e < Ml.length; e++)
    Ml[e]._workInProgressVersionPrimary = null;
  Ml.length = 0;
}
var _r = Ye.ReactCurrentDispatcher,
  Fl = Ye.ReactCurrentBatchConfig,
  Ct = 0,
  A = null,
  X = null,
  K = null,
  Xr = !1,
  Cn = !1,
  Bn = 0,
  Jf = 0;
function ne() {
  throw Error(v(321));
}
function ho(e, t) {
  if (t === null) return !1;
  for (var n = 0; n < t.length && n < e.length; n++)
    if (!Ie(e[n], t[n])) return !1;
  return !0;
}
function go(e, t, n, r, l, a) {
  if (
    ((Ct = a),
    (A = t),
    (t.memoizedState = null),
    (t.updateQueue = null),
    (t.lanes = 0),
    (_r.current = e === null || e.memoizedState === null ? nd : rd),
    (e = n(r, l)),
    Cn)
  ) {
    a = 0;
    do {
      if (((Cn = !1), (Bn = 0), 25 <= a)) throw Error(v(301));
      (a += 1),
        (K = X = null),
        (t.updateQueue = null),
        (_r.current = ld),
        (e = n(r, l));
    } while (Cn);
  }
  if (
    ((_r.current = qr),
    (t = X !== null && X.next !== null),
    (Ct = 0),
    (K = X = A = null),
    (Xr = !1),
    t)
  )
    throw Error(v(300));
  return e;
}
function vo() {
  var e = Bn !== 0;
  return (Bn = 0), e;
}
function De() {
  var e = {
    memoizedState: null,
    baseState: null,
    baseQueue: null,
    queue: null,
    next: null,
  };
  return K === null ? (A.memoizedState = K = e) : (K = K.next = e), K;
}
function Ne() {
  if (X === null) {
    var e = A.alternate;
    e = e !== null ? e.memoizedState : null;
  } else e = X.next;
  var t = K === null ? A.memoizedState : K.next;
  if (t !== null) (K = t), (X = e);
  else {
    if (e === null) throw Error(v(310));
    (X = e),
      (e = {
        memoizedState: X.memoizedState,
        baseState: X.baseState,
        baseQueue: X.baseQueue,
        queue: X.queue,
        next: null,
      }),
      K === null ? (A.memoizedState = K = e) : (K = K.next = e);
  }
  return K;
}
function Wn(e, t) {
  return typeof t == 'function' ? t(e) : t;
}
function Ul(e) {
  var t = Ne(),
    n = t.queue;
  if (n === null) throw Error(v(311));
  n.lastRenderedReducer = e;
  var r = X,
    l = r.baseQueue,
    a = n.pending;
  if (a !== null) {
    if (l !== null) {
      var o = l.next;
      (l.next = a.next), (a.next = o);
    }
    (r.baseQueue = l = a), (n.pending = null);
  }
  if (l !== null) {
    (a = l.next), (r = r.baseState);
    var u = (o = null),
      i = null,
      c = a;
    do {
      var m = c.lane;
      if ((Ct & m) === m)
        i !== null &&
          (i = i.next =
            {
              lane: 0,
              action: c.action,
              hasEagerState: c.hasEagerState,
              eagerState: c.eagerState,
              next: null,
            }),
          (r = c.hasEagerState ? c.eagerState : e(r, c.action));
      else {
        var h = {
          lane: m,
          action: c.action,
          hasEagerState: c.hasEagerState,
          eagerState: c.eagerState,
          next: null,
        };
        i === null ? ((u = i = h), (o = r)) : (i = i.next = h),
          (A.lanes |= m),
          (Pt |= m);
      }
      c = c.next;
    } while (c !== null && c !== a);
    i === null ? (o = r) : (i.next = u),
      Ie(r, t.memoizedState) || (fe = !0),
      (t.memoizedState = r),
      (t.baseState = o),
      (t.baseQueue = i),
      (n.lastRenderedState = r);
  }
  if (((e = n.interleaved), e !== null)) {
    l = e;
    do (a = l.lane), (A.lanes |= a), (Pt |= a), (l = l.next);
    while (l !== e);
  } else l === null && (n.lanes = 0);
  return [t.memoizedState, n.dispatch];
}
function Al(e) {
  var t = Ne(),
    n = t.queue;
  if (n === null) throw Error(v(311));
  n.lastRenderedReducer = e;
  var r = n.dispatch,
    l = n.pending,
    a = t.memoizedState;
  if (l !== null) {
    n.pending = null;
    var o = (l = l.next);
    do (a = e(a, o.action)), (o = o.next);
    while (o !== l);
    Ie(a, t.memoizedState) || (fe = !0),
      (t.memoizedState = a),
      t.baseQueue === null && (t.baseState = a),
      (n.lastRenderedState = a);
  }
  return [a, r];
}
function os() {}
function is(e, t) {
  var n = A,
    r = Ne(),
    l = t(),
    a = !Ie(r.memoizedState, l);
  if (
    (a && ((r.memoizedState = l), (fe = !0)),
    (r = r.queue),
    yo(cs.bind(null, n, r, e), [e]),
    r.getSnapshot !== t || a || (K !== null && K.memoizedState.tag & 1))
  ) {
    if (
      ((n.flags |= 2048),
      Qn(9, ss.bind(null, n, r, l, t), void 0, null),
      G === null)
    )
      throw Error(v(349));
    Ct & 30 || us(n, t, l);
  }
  return l;
}
function us(e, t, n) {
  (e.flags |= 16384),
    (e = { getSnapshot: t, value: n }),
    (t = A.updateQueue),
    t === null
      ? ((t = { lastEffect: null, stores: null }),
        (A.updateQueue = t),
        (t.stores = [e]))
      : ((n = t.stores), n === null ? (t.stores = [e]) : n.push(e));
}
function ss(e, t, n, r) {
  (t.value = n), (t.getSnapshot = r), fs(t) && ds(e);
}
function cs(e, t, n) {
  return n(function () {
    fs(t) && ds(e);
  });
}
function fs(e) {
  var t = e.getSnapshot;
  e = e.value;
  try {
    var n = t();
    return !Ie(e, n);
  } catch {
    return !0;
  }
}
function ds(e) {
  var t = Xe(e, 1);
  t !== null && Re(t, e, 1, -1);
}
function bi(e) {
  var t = De();
  return (
    typeof e == 'function' && (e = e()),
    (t.memoizedState = t.baseState = e),
    (e = {
      pending: null,
      interleaved: null,
      lanes: 0,
      dispatch: null,
      lastRenderedReducer: Wn,
      lastRenderedState: e,
    }),
    (t.queue = e),
    (e = e.dispatch = td.bind(null, A, e)),
    [t.memoizedState, e]
  );
}
function Qn(e, t, n, r) {
  return (
    (e = { tag: e, create: t, destroy: n, deps: r, next: null }),
    (t = A.updateQueue),
    t === null
      ? ((t = { lastEffect: null, stores: null }),
        (A.updateQueue = t),
        (t.lastEffect = e.next = e))
      : ((n = t.lastEffect),
        n === null
          ? (t.lastEffect = e.next = e)
          : ((r = n.next), (n.next = e), (e.next = r), (t.lastEffect = e))),
    e
  );
}
function ps() {
  return Ne().memoizedState;
}
function Er(e, t, n, r) {
  var l = De();
  (A.flags |= e),
    (l.memoizedState = Qn(1 | t, n, void 0, r === void 0 ? null : r));
}
function il(e, t, n, r) {
  var l = Ne();
  r = r === void 0 ? null : r;
  var a = void 0;
  if (X !== null) {
    var o = X.memoizedState;
    if (((a = o.destroy), r !== null && ho(r, o.deps))) {
      l.memoizedState = Qn(t, n, a, r);
      return;
    }
  }
  (A.flags |= e), (l.memoizedState = Qn(1 | t, n, a, r));
}
function wi(e, t) {
  return Er(8390656, 8, e, t);
}
function yo(e, t) {
  return il(2048, 8, e, t);
}
function ms(e, t) {
  return il(4, 2, e, t);
}
function hs(e, t) {
  return il(4, 4, e, t);
}
function gs(e, t) {
  if (typeof t == 'function')
    return (
      (e = e()),
      t(e),
      function () {
        t(null);
      }
    );
  if (t != null)
    return (
      (e = e()),
      (t.current = e),
      function () {
        t.current = null;
      }
    );
}
function vs(e, t, n) {
  return (
    (n = n != null ? n.concat([e]) : null), il(4, 4, gs.bind(null, t, e), n)
  );
}
function bo() {}
function ys(e, t) {
  var n = Ne();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && ho(t, r[1])
    ? r[0]
    : ((n.memoizedState = [e, t]), e);
}
function bs(e, t) {
  var n = Ne();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && ho(t, r[1])
    ? r[0]
    : ((e = e()), (n.memoizedState = [e, t]), e);
}
function ws(e, t, n) {
  return Ct & 21
    ? (Ie(n, t) || ((n = Eu()), (A.lanes |= n), (Pt |= n), (e.baseState = !0)),
      t)
    : (e.baseState && ((e.baseState = !1), (fe = !0)), (e.memoizedState = n));
}
function Zf(e, t) {
  var n = I;
  (I = n !== 0 && 4 > n ? n : 4), e(!0);
  var r = Fl.transition;
  Fl.transition = {};
  try {
    e(!1), t();
  } finally {
    (I = n), (Fl.transition = r);
  }
}
function ks() {
  return Ne().memoizedState;
}
function ed(e, t, n) {
  var r = st(e);
  if (
    ((n = {
      lane: r,
      action: n,
      hasEagerState: !1,
      eagerState: null,
      next: null,
    }),
    xs(e))
  )
    Ss(t, n);
  else if (((n = rs(e, t, n, r)), n !== null)) {
    var l = ie();
    Re(n, e, r, l), _s(n, t, r);
  }
}
function td(e, t, n) {
  var r = st(e),
    l = {
      lane: r,
      action: n,
      hasEagerState: !1,
      eagerState: null,
      next: null,
    };
  if (xs(e)) Ss(t, l);
  else {
    var a = e.alternate;
    if (
      e.lanes === 0 &&
      (a === null || a.lanes === 0) &&
      ((a = t.lastRenderedReducer), a !== null)
    )
      try {
        var o = t.lastRenderedState,
          u = a(o, n);
        if (((l.hasEagerState = !0), (l.eagerState = u), Ie(u, o))) {
          var i = t.interleaved;
          i === null
            ? ((l.next = l), so(t))
            : ((l.next = i.next), (i.next = l)),
            (t.interleaved = l);
          return;
        }
      } catch {
      } finally {
      }
    (n = rs(e, t, l, r)),
      n !== null && ((l = ie()), Re(n, e, r, l), _s(n, t, r));
  }
}
function xs(e) {
  var t = e.alternate;
  return e === A || (t !== null && t === A);
}
function Ss(e, t) {
  Cn = Xr = !0;
  var n = e.pending;
  n === null ? (t.next = t) : ((t.next = n.next), (n.next = t)),
    (e.pending = t);
}
function _s(e, t, n) {
  if (n & 4194240) {
    var r = t.lanes;
    (r &= e.pendingLanes), (n |= r), (t.lanes = n), Ya(e, n);
  }
}
var qr = {
    readContext: Ee,
    useCallback: ne,
    useContext: ne,
    useEffect: ne,
    useImperativeHandle: ne,
    useInsertionEffect: ne,
    useLayoutEffect: ne,
    useMemo: ne,
    useReducer: ne,
    useRef: ne,
    useState: ne,
    useDebugValue: ne,
    useDeferredValue: ne,
    useTransition: ne,
    useMutableSource: ne,
    useSyncExternalStore: ne,
    useId: ne,
    unstable_isNewReconciler: !1,
  },
  nd = {
    readContext: Ee,
    useCallback: function (e, t) {
      return (De().memoizedState = [e, t === void 0 ? null : t]), e;
    },
    useContext: Ee,
    useEffect: wi,
    useImperativeHandle: function (e, t, n) {
      return (
        (n = n != null ? n.concat([e]) : null),
        Er(4194308, 4, gs.bind(null, t, e), n)
      );
    },
    useLayoutEffect: function (e, t) {
      return Er(4194308, 4, e, t);
    },
    useInsertionEffect: function (e, t) {
      return Er(4, 2, e, t);
    },
    useMemo: function (e, t) {
      var n = De();
      return (
        (t = t === void 0 ? null : t), (e = e()), (n.memoizedState = [e, t]), e
      );
    },
    useReducer: function (e, t, n) {
      var r = De();
      return (
        (t = n !== void 0 ? n(t) : t),
        (r.memoizedState = r.baseState = t),
        (e = {
          pending: null,
          interleaved: null,
          lanes: 0,
          dispatch: null,
          lastRenderedReducer: e,
          lastRenderedState: t,
        }),
        (r.queue = e),
        (e = e.dispatch = ed.bind(null, A, e)),
        [r.memoizedState, e]
      );
    },
    useRef: function (e) {
      var t = De();
      return (e = { current: e }), (t.memoizedState = e);
    },
    useState: bi,
    useDebugValue: bo,
    useDeferredValue: function (e) {
      return (De().memoizedState = e);
    },
    useTransition: function () {
      var e = bi(!1),
        t = e[0];
      return (e = Zf.bind(null, e[1])), (De().memoizedState = e), [t, e];
    },
    useMutableSource: function () {},
    useSyncExternalStore: function (e, t, n) {
      var r = A,
        l = De();
      if (F) {
        if (n === void 0) throw Error(v(407));
        n = n();
      } else {
        if (((n = t()), G === null)) throw Error(v(349));
        Ct & 30 || us(r, t, n);
      }
      l.memoizedState = n;
      var a = { value: n, getSnapshot: t };
      return (
        (l.queue = a),
        wi(cs.bind(null, r, a, e), [e]),
        (r.flags |= 2048),
        Qn(9, ss.bind(null, r, a, n, t), void 0, null),
        n
      );
    },
    useId: function () {
      var e = De(),
        t = G.identifierPrefix;
      if (F) {
        var n = He,
          r = $e;
        (n = (r & ~(1 << (32 - Te(r) - 1))).toString(32) + n),
          (t = ':' + t + 'R' + n),
          (n = Bn++),
          0 < n && (t += 'H' + n.toString(32)),
          (t += ':');
      } else (n = Jf++), (t = ':' + t + 'r' + n.toString(32) + ':');
      return (e.memoizedState = t);
    },
    unstable_isNewReconciler: !1,
  },
  rd = {
    readContext: Ee,
    useCallback: ys,
    useContext: Ee,
    useEffect: yo,
    useImperativeHandle: vs,
    useInsertionEffect: ms,
    useLayoutEffect: hs,
    useMemo: bs,
    useReducer: Ul,
    useRef: ps,
    useState: function () {
      return Ul(Wn);
    },
    useDebugValue: bo,
    useDeferredValue: function (e) {
      var t = Ne();
      return ws(t, X.memoizedState, e);
    },
    useTransition: function () {
      var e = Ul(Wn)[0],
        t = Ne().memoizedState;
      return [e, t];
    },
    useMutableSource: os,
    useSyncExternalStore: is,
    useId: ks,
    unstable_isNewReconciler: !1,
  },
  ld = {
    readContext: Ee,
    useCallback: ys,
    useContext: Ee,
    useEffect: yo,
    useImperativeHandle: vs,
    useInsertionEffect: ms,
    useLayoutEffect: hs,
    useMemo: bs,
    useReducer: Al,
    useRef: ps,
    useState: function () {
      return Al(Wn);
    },
    useDebugValue: bo,
    useDeferredValue: function (e) {
      var t = Ne();
      return X === null ? (t.memoizedState = e) : ws(t, X.memoizedState, e);
    },
    useTransition: function () {
      var e = Al(Wn)[0],
        t = Ne().memoizedState;
      return [e, t];
    },
    useMutableSource: os,
    useSyncExternalStore: is,
    useId: ks,
    unstable_isNewReconciler: !1,
  };
function Le(e, t) {
  if (e && e.defaultProps) {
    (t = V({}, t)), (e = e.defaultProps);
    for (var n in e) t[n] === void 0 && (t[n] = e[n]);
    return t;
  }
  return t;
}
function xa(e, t, n, r) {
  (t = e.memoizedState),
    (n = n(r, t)),
    (n = n == null ? t : V({}, t, n)),
    (e.memoizedState = n),
    e.lanes === 0 && (e.updateQueue.baseState = n);
}
var ul = {
  isMounted: function (e) {
    return (e = e._reactInternals) ? jt(e) === e : !1;
  },
  enqueueSetState: function (e, t, n) {
    e = e._reactInternals;
    var r = ie(),
      l = st(e),
      a = Be(r, l);
    (a.payload = t),
      n != null && (a.callback = n),
      (t = it(e, a, l)),
      t !== null && (Re(t, e, l, r), Sr(t, e, l));
  },
  enqueueReplaceState: function (e, t, n) {
    e = e._reactInternals;
    var r = ie(),
      l = st(e),
      a = Be(r, l);
    (a.tag = 1),
      (a.payload = t),
      n != null && (a.callback = n),
      (t = it(e, a, l)),
      t !== null && (Re(t, e, l, r), Sr(t, e, l));
  },
  enqueueForceUpdate: function (e, t) {
    e = e._reactInternals;
    var n = ie(),
      r = st(e),
      l = Be(n, r);
    (l.tag = 2),
      t != null && (l.callback = t),
      (t = it(e, l, r)),
      t !== null && (Re(t, e, r, n), Sr(t, e, r));
  },
};
function ki(e, t, n, r, l, a, o) {
  return (
    (e = e.stateNode),
    typeof e.shouldComponentUpdate == 'function'
      ? e.shouldComponentUpdate(r, a, o)
      : t.prototype && t.prototype.isPureReactComponent
      ? !Fn(n, r) || !Fn(l, a)
      : !0
  );
}
function Es(e, t, n) {
  var r = !1,
    l = dt,
    a = t.contextType;
  return (
    typeof a == 'object' && a !== null
      ? (a = Ee(a))
      : ((l = pe(t) ? Et : ae.current),
        (r = t.contextTypes),
        (a = (r = r != null) ? Jt(e, l) : dt)),
    (t = new t(n, a)),
    (e.memoizedState =
      t.state !== null && t.state !== void 0 ? t.state : null),
    (t.updater = ul),
    (e.stateNode = t),
    (t._reactInternals = e),
    r &&
      ((e = e.stateNode),
      (e.__reactInternalMemoizedUnmaskedChildContext = l),
      (e.__reactInternalMemoizedMaskedChildContext = a)),
    t
  );
}
function xi(e, t, n, r) {
  (e = t.state),
    typeof t.componentWillReceiveProps == 'function' &&
      t.componentWillReceiveProps(n, r),
    typeof t.UNSAFE_componentWillReceiveProps == 'function' &&
      t.UNSAFE_componentWillReceiveProps(n, r),
    t.state !== e && ul.enqueueReplaceState(t, t.state, null);
}
function Sa(e, t, n, r) {
  var l = e.stateNode;
  (l.props = n), (l.state = e.memoizedState), (l.refs = {}), co(e);
  var a = t.contextType;
  typeof a == 'object' && a !== null
    ? (l.context = Ee(a))
    : ((a = pe(t) ? Et : ae.current), (l.context = Jt(e, a))),
    (l.state = e.memoizedState),
    (a = t.getDerivedStateFromProps),
    typeof a == 'function' && (xa(e, t, a, n), (l.state = e.memoizedState)),
    typeof t.getDerivedStateFromProps == 'function' ||
      typeof l.getSnapshotBeforeUpdate == 'function' ||
      (typeof l.UNSAFE_componentWillMount != 'function' &&
        typeof l.componentWillMount != 'function') ||
      ((t = l.state),
      typeof l.componentWillMount == 'function' && l.componentWillMount(),
      typeof l.UNSAFE_componentWillMount == 'function' &&
        l.UNSAFE_componentWillMount(),
      t !== l.state && ul.enqueueReplaceState(l, l.state, null),
      Wr(e, n, l, r),
      (l.state = e.memoizedState)),
    typeof l.componentDidMount == 'function' && (e.flags |= 4194308);
}
function nn(e, t) {
  try {
    var n = '',
      r = t;
    do (n += jc(r)), (r = r.return);
    while (r);
    var l = n;
  } catch (a) {
    l =
      `
Error generating stack: ` +
      a.message +
      `
` +
      a.stack;
  }
  return { value: e, source: t, stack: l, digest: null };
}
function Vl(e, t, n) {
  return { value: e, source: null, stack: n ?? null, digest: t ?? null };
}
function _a(e, t) {
  try {
    console.error(t.value);
  } catch (n) {
    setTimeout(function () {
      throw n;
    });
  }
}
var ad = typeof WeakMap == 'function' ? WeakMap : Map;
function Ns(e, t, n) {
  (n = Be(-1, n)), (n.tag = 3), (n.payload = { element: null });
  var r = t.value;
  return (
    (n.callback = function () {
      Kr || ((Kr = !0), (Ra = r)), _a(e, t);
    }),
    n
  );
}
function Cs(e, t, n) {
  (n = Be(-1, n)), (n.tag = 3);
  var r = e.type.getDerivedStateFromError;
  if (typeof r == 'function') {
    var l = t.value;
    (n.payload = function () {
      return r(l);
    }),
      (n.callback = function () {
        _a(e, t);
      });
  }
  var a = e.stateNode;
  return (
    a !== null &&
      typeof a.componentDidCatch == 'function' &&
      (n.callback = function () {
        _a(e, t),
          typeof r != 'function' &&
            (ut === null ? (ut = new Set([this])) : ut.add(this));
        var o = t.stack;
        this.componentDidCatch(t.value, {
          componentStack: o !== null ? o : '',
        });
      }),
    n
  );
}
function Si(e, t, n) {
  var r = e.pingCache;
  if (r === null) {
    r = e.pingCache = new ad();
    var l = new Set();
    r.set(t, l);
  } else (l = r.get(t)), l === void 0 && ((l = new Set()), r.set(t, l));
  l.has(n) || (l.add(n), (e = bd.bind(null, e, t, n)), t.then(e, e));
}
function _i(e) {
  do {
    var t;
    if (
      ((t = e.tag === 13) &&
        ((t = e.memoizedState), (t = t !== null ? t.dehydrated !== null : !0)),
      t)
    )
      return e;
    e = e.return;
  } while (e !== null);
  return null;
}
function Ei(e, t, n, r, l) {
  return e.mode & 1
    ? ((e.flags |= 65536), (e.lanes = l), e)
    : (e === t
        ? (e.flags |= 65536)
        : ((e.flags |= 128),
          (n.flags |= 131072),
          (n.flags &= -52805),
          n.tag === 1 &&
            (n.alternate === null
              ? (n.tag = 17)
              : ((t = Be(-1, 1)), (t.tag = 2), it(n, t, 1))),
          (n.lanes |= 1)),
      e);
}
var od = Ye.ReactCurrentOwner,
  fe = !1;
function oe(e, t, n, r) {
  t.child = e === null ? ns(t, null, n, r) : en(t, e.child, n, r);
}
function Ni(e, t, n, r, l) {
  n = n.render;
  var a = t.ref;
  return (
    Yt(t, l),
    (r = go(e, t, n, r, a, l)),
    (n = vo()),
    e !== null && !fe
      ? ((t.updateQueue = e.updateQueue),
        (t.flags &= -2053),
        (e.lanes &= ~l),
        qe(e, t, l))
      : (F && n && ro(t), (t.flags |= 1), oe(e, t, r, l), t.child)
  );
}
function Ci(e, t, n, r, l) {
  if (e === null) {
    var a = n.type;
    return typeof a == 'function' &&
      !Co(a) &&
      a.defaultProps === void 0 &&
      n.compare === null &&
      n.defaultProps === void 0
      ? ((t.tag = 15), (t.type = a), Ps(e, t, a, r, l))
      : ((e = Lr(n.type, null, r, t, t.mode, l)),
        (e.ref = t.ref),
        (e.return = t),
        (t.child = e));
  }
  if (((a = e.child), !(e.lanes & l))) {
    var o = a.memoizedProps;
    if (
      ((n = n.compare), (n = n !== null ? n : Fn), n(o, r) && e.ref === t.ref)
    )
      return qe(e, t, l);
  }
  return (
    (t.flags |= 1),
    (e = ct(a, r)),
    (e.ref = t.ref),
    (e.return = t),
    (t.child = e)
  );
}
function Ps(e, t, n, r, l) {
  if (e !== null) {
    var a = e.memoizedProps;
    if (Fn(a, r) && e.ref === t.ref)
      if (((fe = !1), (t.pendingProps = r = a), (e.lanes & l) !== 0))
        e.flags & 131072 && (fe = !0);
      else return (t.lanes = e.lanes), qe(e, t, l);
  }
  return Ea(e, t, n, r, l);
}
function Ls(e, t, n) {
  var r = t.pendingProps,
    l = r.children,
    a = e !== null ? e.memoizedState : null;
  if (r.mode === 'hidden')
    if (!(t.mode & 1))
      (t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }),
        O(Bt, he),
        (he |= n);
    else {
      if (!(n & 1073741824))
        return (
          (e = a !== null ? a.baseLanes | n : n),
          (t.lanes = t.childLanes = 1073741824),
          (t.memoizedState = {
            baseLanes: e,
            cachePool: null,
            transitions: null,
          }),
          (t.updateQueue = null),
          O(Bt, he),
          (he |= e),
          null
        );
      (t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }),
        (r = a !== null ? a.baseLanes : n),
        O(Bt, he),
        (he |= r);
    }
  else
    a !== null ? ((r = a.baseLanes | n), (t.memoizedState = null)) : (r = n),
      O(Bt, he),
      (he |= r);
  return oe(e, t, l, n), t.child;
}
function zs(e, t) {
  var n = t.ref;
  ((e === null && n !== null) || (e !== null && e.ref !== n)) &&
    ((t.flags |= 512), (t.flags |= 2097152));
}
function Ea(e, t, n, r, l) {
  var a = pe(n) ? Et : ae.current;
  return (
    (a = Jt(t, a)),
    Yt(t, l),
    (n = go(e, t, n, r, a, l)),
    (r = vo()),
    e !== null && !fe
      ? ((t.updateQueue = e.updateQueue),
        (t.flags &= -2053),
        (e.lanes &= ~l),
        qe(e, t, l))
      : (F && r && ro(t), (t.flags |= 1), oe(e, t, n, l), t.child)
  );
}
function Pi(e, t, n, r, l) {
  if (pe(n)) {
    var a = !0;
    Ar(t);
  } else a = !1;
  if ((Yt(t, l), t.stateNode === null))
    Nr(e, t), Es(t, n, r), Sa(t, n, r, l), (r = !0);
  else if (e === null) {
    var o = t.stateNode,
      u = t.memoizedProps;
    o.props = u;
    var i = o.context,
      c = n.contextType;
    typeof c == 'object' && c !== null
      ? (c = Ee(c))
      : ((c = pe(n) ? Et : ae.current), (c = Jt(t, c)));
    var m = n.getDerivedStateFromProps,
      h =
        typeof m == 'function' ||
        typeof o.getSnapshotBeforeUpdate == 'function';
    h ||
      (typeof o.UNSAFE_componentWillReceiveProps != 'function' &&
        typeof o.componentWillReceiveProps != 'function') ||
      ((u !== r || i !== c) && xi(t, o, r, c)),
      (Je = !1);
    var p = t.memoizedState;
    (o.state = p),
      Wr(t, r, o, l),
      (i = t.memoizedState),
      u !== r || p !== i || de.current || Je
        ? (typeof m == 'function' && (xa(t, n, m, r), (i = t.memoizedState)),
          (u = Je || ki(t, n, u, r, p, i, c))
            ? (h ||
                (typeof o.UNSAFE_componentWillMount != 'function' &&
                  typeof o.componentWillMount != 'function') ||
                (typeof o.componentWillMount == 'function' &&
                  o.componentWillMount(),
                typeof o.UNSAFE_componentWillMount == 'function' &&
                  o.UNSAFE_componentWillMount()),
              typeof o.componentDidMount == 'function' && (t.flags |= 4194308))
            : (typeof o.componentDidMount == 'function' &&
                (t.flags |= 4194308),
              (t.memoizedProps = r),
              (t.memoizedState = i)),
          (o.props = r),
          (o.state = i),
          (o.context = c),
          (r = u))
        : (typeof o.componentDidMount == 'function' && (t.flags |= 4194308),
          (r = !1));
  } else {
    (o = t.stateNode),
      ls(e, t),
      (u = t.memoizedProps),
      (c = t.type === t.elementType ? u : Le(t.type, u)),
      (o.props = c),
      (h = t.pendingProps),
      (p = o.context),
      (i = n.contextType),
      typeof i == 'object' && i !== null
        ? (i = Ee(i))
        : ((i = pe(n) ? Et : ae.current), (i = Jt(t, i)));
    var w = n.getDerivedStateFromProps;
    (m =
      typeof w == 'function' ||
      typeof o.getSnapshotBeforeUpdate == 'function') ||
      (typeof o.UNSAFE_componentWillReceiveProps != 'function' &&
        typeof o.componentWillReceiveProps != 'function') ||
      ((u !== h || p !== i) && xi(t, o, r, i)),
      (Je = !1),
      (p = t.memoizedState),
      (o.state = p),
      Wr(t, r, o, l);
    var b = t.memoizedState;
    u !== h || p !== b || de.current || Je
      ? (typeof w == 'function' && (xa(t, n, w, r), (b = t.memoizedState)),
        (c = Je || ki(t, n, c, r, p, b, i) || !1)
          ? (m ||
              (typeof o.UNSAFE_componentWillUpdate != 'function' &&
                typeof o.componentWillUpdate != 'function') ||
              (typeof o.componentWillUpdate == 'function' &&
                o.componentWillUpdate(r, b, i),
              typeof o.UNSAFE_componentWillUpdate == 'function' &&
                o.UNSAFE_componentWillUpdate(r, b, i)),
            typeof o.componentDidUpdate == 'function' && (t.flags |= 4),
            typeof o.getSnapshotBeforeUpdate == 'function' &&
              (t.flags |= 1024))
          : (typeof o.componentDidUpdate != 'function' ||
              (u === e.memoizedProps && p === e.memoizedState) ||
              (t.flags |= 4),
            typeof o.getSnapshotBeforeUpdate != 'function' ||
              (u === e.memoizedProps && p === e.memoizedState) ||
              (t.flags |= 1024),
            (t.memoizedProps = r),
            (t.memoizedState = b)),
        (o.props = r),
        (o.state = b),
        (o.context = i),
        (r = c))
      : (typeof o.componentDidUpdate != 'function' ||
          (u === e.memoizedProps && p === e.memoizedState) ||
          (t.flags |= 4),
        typeof o.getSnapshotBeforeUpdate != 'function' ||
          (u === e.memoizedProps && p === e.memoizedState) ||
          (t.flags |= 1024),
        (r = !1));
  }
  return Na(e, t, n, r, a, l);
}
function Na(e, t, n, r, l, a) {
  zs(e, t);
  var o = (t.flags & 128) !== 0;
  if (!r && !o) return l && pi(t, n, !1), qe(e, t, a);
  (r = t.stateNode), (od.current = t);
  var u =
    o && typeof n.getDerivedStateFromError != 'function' ? null : r.render();
  return (
    (t.flags |= 1),
    e !== null && o
      ? ((t.child = en(t, e.child, null, a)), (t.child = en(t, null, u, a)))
      : oe(e, t, u, a),
    (t.memoizedState = r.state),
    l && pi(t, n, !0),
    t.child
  );
}
function js(e) {
  var t = e.stateNode;
  t.pendingContext
    ? di(e, t.pendingContext, t.pendingContext !== t.context)
    : t.context && di(e, t.context, !1),
    fo(e, t.containerInfo);
}
function Li(e, t, n, r, l) {
  return Zt(), ao(l), (t.flags |= 256), oe(e, t, n, r), t.child;
}
var Ca = { dehydrated: null, treeContext: null, retryLane: 0 };
function Pa(e) {
  return { baseLanes: e, cachePool: null, transitions: null };
}
function Ts(e, t, n) {
  var r = t.pendingProps,
    l = U.current,
    a = !1,
    o = (t.flags & 128) !== 0,
    u;
  if (
    ((u = o) ||
      (u = e !== null && e.memoizedState === null ? !1 : (l & 2) !== 0),
    u
      ? ((a = !0), (t.flags &= -129))
      : (e === null || e.memoizedState !== null) && (l |= 1),
    O(U, l & 1),
    e === null)
  )
    return (
      wa(t),
      (e = t.memoizedState),
      e !== null && ((e = e.dehydrated), e !== null)
        ? (t.mode & 1
            ? e.data === '$!'
              ? (t.lanes = 8)
              : (t.lanes = 1073741824)
            : (t.lanes = 1),
          null)
        : ((o = r.children),
          (e = r.fallback),
          a
            ? ((r = t.mode),
              (a = t.child),
              (o = { mode: 'hidden', children: o }),
              !(r & 1) && a !== null
                ? ((a.childLanes = 0), (a.pendingProps = o))
                : (a = fl(o, r, 0, null)),
              (e = _t(e, r, n, null)),
              (a.return = t),
              (e.return = t),
              (a.sibling = e),
              (t.child = a),
              (t.child.memoizedState = Pa(n)),
              (t.memoizedState = Ca),
              e)
            : wo(t, o))
    );
  if (((l = e.memoizedState), l !== null && ((u = l.dehydrated), u !== null)))
    return id(e, t, o, r, u, l, n);
  if (a) {
    (a = r.fallback), (o = t.mode), (l = e.child), (u = l.sibling);
    var i = { mode: 'hidden', children: r.children };
    return (
      !(o & 1) && t.child !== l
        ? ((r = t.child),
          (r.childLanes = 0),
          (r.pendingProps = i),
          (t.deletions = null))
        : ((r = ct(l, i)), (r.subtreeFlags = l.subtreeFlags & 14680064)),
      u !== null ? (a = ct(u, a)) : ((a = _t(a, o, n, null)), (a.flags |= 2)),
      (a.return = t),
      (r.return = t),
      (r.sibling = a),
      (t.child = r),
      (r = a),
      (a = t.child),
      (o = e.child.memoizedState),
      (o =
        o === null
          ? Pa(n)
          : {
              baseLanes: o.baseLanes | n,
              cachePool: null,
              transitions: o.transitions,
            }),
      (a.memoizedState = o),
      (a.childLanes = e.childLanes & ~n),
      (t.memoizedState = Ca),
      r
    );
  }
  return (
    (a = e.child),
    (e = a.sibling),
    (r = ct(a, { mode: 'visible', children: r.children })),
    !(t.mode & 1) && (r.lanes = n),
    (r.return = t),
    (r.sibling = null),
    e !== null &&
      ((n = t.deletions),
      n === null ? ((t.deletions = [e]), (t.flags |= 16)) : n.push(e)),
    (t.child = r),
    (t.memoizedState = null),
    r
  );
}
function wo(e, t) {
  return (
    (t = fl({ mode: 'visible', children: t }, e.mode, 0, null)),
    (t.return = e),
    (e.child = t)
  );
}
function mr(e, t, n, r) {
  return (
    r !== null && ao(r),
    en(t, e.child, null, n),
    (e = wo(t, t.pendingProps.children)),
    (e.flags |= 2),
    (t.memoizedState = null),
    e
  );
}
function id(e, t, n, r, l, a, o) {
  if (n)
    return t.flags & 256
      ? ((t.flags &= -257), (r = Vl(Error(v(422)))), mr(e, t, o, r))
      : t.memoizedState !== null
      ? ((t.child = e.child), (t.flags |= 128), null)
      : ((a = r.fallback),
        (l = t.mode),
        (r = fl({ mode: 'visible', children: r.children }, l, 0, null)),
        (a = _t(a, l, o, null)),
        (a.flags |= 2),
        (r.return = t),
        (a.return = t),
        (r.sibling = a),
        (t.child = r),
        t.mode & 1 && en(t, e.child, null, o),
        (t.child.memoizedState = Pa(o)),
        (t.memoizedState = Ca),
        a);
  if (!(t.mode & 1)) return mr(e, t, o, null);
  if (l.data === '$!') {
    if (((r = l.nextSibling && l.nextSibling.dataset), r)) var u = r.dgst;
    return (
      (r = u), (a = Error(v(419))), (r = Vl(a, r, void 0)), mr(e, t, o, r)
    );
  }
  if (((u = (o & e.childLanes) !== 0), fe || u)) {
    if (((r = G), r !== null)) {
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
      (l = l & (r.suspendedLanes | o) ? 0 : l),
        l !== 0 &&
          l !== a.retryLane &&
          ((a.retryLane = l), Xe(e, l), Re(r, e, l, -1));
    }
    return No(), (r = Vl(Error(v(421)))), mr(e, t, o, r);
  }
  return l.data === '$?'
    ? ((t.flags |= 128),
      (t.child = e.child),
      (t = wd.bind(null, e)),
      (l._reactRetry = t),
      null)
    : ((e = a.treeContext),
      (ge = ot(l.nextSibling)),
      (ve = t),
      (F = !0),
      (je = null),
      e !== null &&
        ((ke[xe++] = $e),
        (ke[xe++] = He),
        (ke[xe++] = Nt),
        ($e = e.id),
        (He = e.overflow),
        (Nt = t)),
      (t = wo(t, r.children)),
      (t.flags |= 4096),
      t);
}
function zi(e, t, n) {
  e.lanes |= t;
  var r = e.alternate;
  r !== null && (r.lanes |= t), ka(e.return, t, n);
}
function $l(e, t, n, r, l) {
  var a = e.memoizedState;
  a === null
    ? (e.memoizedState = {
        isBackwards: t,
        rendering: null,
        renderingStartTime: 0,
        last: r,
        tail: n,
        tailMode: l,
      })
    : ((a.isBackwards = t),
      (a.rendering = null),
      (a.renderingStartTime = 0),
      (a.last = r),
      (a.tail = n),
      (a.tailMode = l));
}
function Rs(e, t, n) {
  var r = t.pendingProps,
    l = r.revealOrder,
    a = r.tail;
  if ((oe(e, t, r.children, n), (r = U.current), r & 2))
    (r = (r & 1) | 2), (t.flags |= 128);
  else {
    if (e !== null && e.flags & 128)
      e: for (e = t.child; e !== null; ) {
        if (e.tag === 13) e.memoizedState !== null && zi(e, n, t);
        else if (e.tag === 19) zi(e, n, t);
        else if (e.child !== null) {
          (e.child.return = e), (e = e.child);
          continue;
        }
        if (e === t) break e;
        for (; e.sibling === null; ) {
          if (e.return === null || e.return === t) break e;
          e = e.return;
        }
        (e.sibling.return = e.return), (e = e.sibling);
      }
    r &= 1;
  }
  if ((O(U, r), !(t.mode & 1))) t.memoizedState = null;
  else
    switch (l) {
      case 'forwards':
        for (n = t.child, l = null; n !== null; )
          (e = n.alternate),
            e !== null && Qr(e) === null && (l = n),
            (n = n.sibling);
        (n = l),
          n === null
            ? ((l = t.child), (t.child = null))
            : ((l = n.sibling), (n.sibling = null)),
          $l(t, !1, l, n, a);
        break;
      case 'backwards':
        for (n = null, l = t.child, t.child = null; l !== null; ) {
          if (((e = l.alternate), e !== null && Qr(e) === null)) {
            t.child = l;
            break;
          }
          (e = l.sibling), (l.sibling = n), (n = l), (l = e);
        }
        $l(t, !0, n, null, a);
        break;
      case 'together':
        $l(t, !1, null, null, void 0);
        break;
      default:
        t.memoizedState = null;
    }
  return t.child;
}
function Nr(e, t) {
  !(t.mode & 1) &&
    e !== null &&
    ((e.alternate = null), (t.alternate = null), (t.flags |= 2));
}
function qe(e, t, n) {
  if (
    (e !== null && (t.dependencies = e.dependencies),
    (Pt |= t.lanes),
    !(n & t.childLanes))
  )
    return null;
  if (e !== null && t.child !== e.child) throw Error(v(153));
  if (t.child !== null) {
    for (
      e = t.child, n = ct(e, e.pendingProps), t.child = n, n.return = t;
      e.sibling !== null;

    )
      (e = e.sibling), (n = n.sibling = ct(e, e.pendingProps)), (n.return = t);
    n.sibling = null;
  }
  return t.child;
}
function ud(e, t, n) {
  switch (t.tag) {
    case 3:
      js(t), Zt();
      break;
    case 5:
      as(t);
      break;
    case 1:
      pe(t.type) && Ar(t);
      break;
    case 4:
      fo(t, t.stateNode.containerInfo);
      break;
    case 10:
      var r = t.type._context,
        l = t.memoizedProps.value;
      O(Hr, r._currentValue), (r._currentValue = l);
      break;
    case 13:
      if (((r = t.memoizedState), r !== null))
        return r.dehydrated !== null
          ? (O(U, U.current & 1), (t.flags |= 128), null)
          : n & t.child.childLanes
          ? Ts(e, t, n)
          : (O(U, U.current & 1),
            (e = qe(e, t, n)),
            e !== null ? e.sibling : null);
      O(U, U.current & 1);
      break;
    case 19:
      if (((r = (n & t.childLanes) !== 0), e.flags & 128)) {
        if (r) return Rs(e, t, n);
        t.flags |= 128;
      }
      if (
        ((l = t.memoizedState),
        l !== null &&
          ((l.rendering = null), (l.tail = null), (l.lastEffect = null)),
        O(U, U.current),
        r)
      )
        break;
      return null;
    case 22:
    case 23:
      return (t.lanes = 0), Ls(e, t, n);
  }
  return qe(e, t, n);
}
var Is, La, Os, Ds;
Is = function (e, t) {
  for (var n = t.child; n !== null; ) {
    if (n.tag === 5 || n.tag === 6) e.appendChild(n.stateNode);
    else if (n.tag !== 4 && n.child !== null) {
      (n.child.return = n), (n = n.child);
      continue;
    }
    if (n === t) break;
    for (; n.sibling === null; ) {
      if (n.return === null || n.return === t) return;
      n = n.return;
    }
    (n.sibling.return = n.return), (n = n.sibling);
  }
};
La = function () {};
Os = function (e, t, n, r) {
  var l = e.memoizedProps;
  if (l !== r) {
    (e = t.stateNode), xt(Ue.current);
    var a = null;
    switch (n) {
      case 'input':
        (l = Gl(e, l)), (r = Gl(e, r)), (a = []);
        break;
      case 'select':
        (l = V({}, l, { value: void 0 })),
          (r = V({}, r, { value: void 0 })),
          (a = []);
        break;
      case 'textarea':
        (l = ea(e, l)), (r = ea(e, r)), (a = []);
        break;
      default:
        typeof l.onClick != 'function' &&
          typeof r.onClick == 'function' &&
          (e.onclick = Fr);
    }
    na(n, r);
    var o;
    n = null;
    for (c in l)
      if (!r.hasOwnProperty(c) && l.hasOwnProperty(c) && l[c] != null)
        if (c === 'style') {
          var u = l[c];
          for (o in u) u.hasOwnProperty(o) && (n || (n = {}), (n[o] = ''));
        } else
          c !== 'dangerouslySetInnerHTML' &&
            c !== 'children' &&
            c !== 'suppressContentEditableWarning' &&
            c !== 'suppressHydrationWarning' &&
            c !== 'autoFocus' &&
            (jn.hasOwnProperty(c)
              ? a || (a = [])
              : (a = a || []).push(c, null));
    for (c in r) {
      var i = r[c];
      if (
        ((u = l != null ? l[c] : void 0),
        r.hasOwnProperty(c) && i !== u && (i != null || u != null))
      )
        if (c === 'style')
          if (u) {
            for (o in u)
              !u.hasOwnProperty(o) ||
                (i && i.hasOwnProperty(o)) ||
                (n || (n = {}), (n[o] = ''));
            for (o in i)
              i.hasOwnProperty(o) &&
                u[o] !== i[o] &&
                (n || (n = {}), (n[o] = i[o]));
          } else n || (a || (a = []), a.push(c, n)), (n = i);
        else
          c === 'dangerouslySetInnerHTML'
            ? ((i = i ? i.__html : void 0),
              (u = u ? u.__html : void 0),
              i != null && u !== i && (a = a || []).push(c, i))
            : c === 'children'
            ? (typeof i != 'string' && typeof i != 'number') ||
              (a = a || []).push(c, '' + i)
            : c !== 'suppressContentEditableWarning' &&
              c !== 'suppressHydrationWarning' &&
              (jn.hasOwnProperty(c)
                ? (i != null && c === 'onScroll' && D('scroll', e),
                  a || u === i || (a = []))
                : (a = a || []).push(c, i));
    }
    n && (a = a || []).push('style', n);
    var c = a;
    (t.updateQueue = c) && (t.flags |= 4);
  }
};
Ds = function (e, t, n, r) {
  n !== r && (t.flags |= 4);
};
function gn(e, t) {
  if (!F)
    switch (e.tailMode) {
      case 'hidden':
        t = e.tail;
        for (var n = null; t !== null; )
          t.alternate !== null && (n = t), (t = t.sibling);
        n === null ? (e.tail = null) : (n.sibling = null);
        break;
      case 'collapsed':
        n = e.tail;
        for (var r = null; n !== null; )
          n.alternate !== null && (r = n), (n = n.sibling);
        r === null
          ? t || e.tail === null
            ? (e.tail = null)
            : (e.tail.sibling = null)
          : (r.sibling = null);
    }
}
function re(e) {
  var t = e.alternate !== null && e.alternate.child === e.child,
    n = 0,
    r = 0;
  if (t)
    for (var l = e.child; l !== null; )
      (n |= l.lanes | l.childLanes),
        (r |= l.subtreeFlags & 14680064),
        (r |= l.flags & 14680064),
        (l.return = e),
        (l = l.sibling);
  else
    for (l = e.child; l !== null; )
      (n |= l.lanes | l.childLanes),
        (r |= l.subtreeFlags),
        (r |= l.flags),
        (l.return = e),
        (l = l.sibling);
  return (e.subtreeFlags |= r), (e.childLanes = n), t;
}
function sd(e, t, n) {
  var r = t.pendingProps;
  switch ((lo(t), t.tag)) {
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
      return re(t), null;
    case 1:
      return pe(t.type) && Ur(), re(t), null;
    case 3:
      return (
        (r = t.stateNode),
        tn(),
        M(de),
        M(ae),
        mo(),
        r.pendingContext &&
          ((r.context = r.pendingContext), (r.pendingContext = null)),
        (e === null || e.child === null) &&
          (dr(t)
            ? (t.flags |= 4)
            : e === null ||
              (e.memoizedState.isDehydrated && !(t.flags & 256)) ||
              ((t.flags |= 1024), je !== null && (Da(je), (je = null)))),
        La(e, t),
        re(t),
        null
      );
    case 5:
      po(t);
      var l = xt(Hn.current);
      if (((n = t.type), e !== null && t.stateNode != null))
        Os(e, t, n, r, l),
          e.ref !== t.ref && ((t.flags |= 512), (t.flags |= 2097152));
      else {
        if (!r) {
          if (t.stateNode === null) throw Error(v(166));
          return re(t), null;
        }
        if (((e = xt(Ue.current)), dr(t))) {
          (r = t.stateNode), (n = t.type);
          var a = t.memoizedProps;
          switch (((r[Me] = t), (r[Vn] = a), (e = (t.mode & 1) !== 0), n)) {
            case 'dialog':
              D('cancel', r), D('close', r);
              break;
            case 'iframe':
            case 'object':
            case 'embed':
              D('load', r);
              break;
            case 'video':
            case 'audio':
              for (l = 0; l < kn.length; l++) D(kn[l], r);
              break;
            case 'source':
              D('error', r);
              break;
            case 'img':
            case 'image':
            case 'link':
              D('error', r), D('load', r);
              break;
            case 'details':
              D('toggle', r);
              break;
            case 'input':
              Uo(r, a), D('invalid', r);
              break;
            case 'select':
              (r._wrapperState = { wasMultiple: !!a.multiple }),
                D('invalid', r);
              break;
            case 'textarea':
              Vo(r, a), D('invalid', r);
          }
          na(n, a), (l = null);
          for (var o in a)
            if (a.hasOwnProperty(o)) {
              var u = a[o];
              o === 'children'
                ? typeof u == 'string'
                  ? r.textContent !== u &&
                    (a.suppressHydrationWarning !== !0 &&
                      fr(r.textContent, u, e),
                    (l = ['children', u]))
                  : typeof u == 'number' &&
                    r.textContent !== '' + u &&
                    (a.suppressHydrationWarning !== !0 &&
                      fr(r.textContent, u, e),
                    (l = ['children', '' + u]))
                : jn.hasOwnProperty(o) &&
                  u != null &&
                  o === 'onScroll' &&
                  D('scroll', r);
            }
          switch (n) {
            case 'input':
              rr(r), Ao(r, a, !0);
              break;
            case 'textarea':
              rr(r), $o(r);
              break;
            case 'select':
            case 'option':
              break;
            default:
              typeof a.onClick == 'function' && (r.onclick = Fr);
          }
          (r = l), (t.updateQueue = r), r !== null && (t.flags |= 4);
        } else {
          (o = l.nodeType === 9 ? l : l.ownerDocument),
            e === 'http://www.w3.org/1999/xhtml' && (e = cu(n)),
            e === 'http://www.w3.org/1999/xhtml'
              ? n === 'script'
                ? ((e = o.createElement('div')),
                  (e.innerHTML = '<script></script>'),
                  (e = e.removeChild(e.firstChild)))
                : typeof r.is == 'string'
                ? (e = o.createElement(n, { is: r.is }))
                : ((e = o.createElement(n)),
                  n === 'select' &&
                    ((o = e),
                    r.multiple
                      ? (o.multiple = !0)
                      : r.size && (o.size = r.size)))
              : (e = o.createElementNS(e, n)),
            (e[Me] = t),
            (e[Vn] = r),
            Is(e, t, !1, !1),
            (t.stateNode = e);
          e: {
            switch (((o = ra(n, r)), n)) {
              case 'dialog':
                D('cancel', e), D('close', e), (l = r);
                break;
              case 'iframe':
              case 'object':
              case 'embed':
                D('load', e), (l = r);
                break;
              case 'video':
              case 'audio':
                for (l = 0; l < kn.length; l++) D(kn[l], e);
                l = r;
                break;
              case 'source':
                D('error', e), (l = r);
                break;
              case 'img':
              case 'image':
              case 'link':
                D('error', e), D('load', e), (l = r);
                break;
              case 'details':
                D('toggle', e), (l = r);
                break;
              case 'input':
                Uo(e, r), (l = Gl(e, r)), D('invalid', e);
                break;
              case 'option':
                l = r;
                break;
              case 'select':
                (e._wrapperState = { wasMultiple: !!r.multiple }),
                  (l = V({}, r, { value: void 0 })),
                  D('invalid', e);
                break;
              case 'textarea':
                Vo(e, r), (l = ea(e, r)), D('invalid', e);
                break;
              default:
                l = r;
            }
            na(n, l), (u = l);
            for (a in u)
              if (u.hasOwnProperty(a)) {
                var i = u[a];
                a === 'style'
                  ? pu(e, i)
                  : a === 'dangerouslySetInnerHTML'
                  ? ((i = i ? i.__html : void 0), i != null && fu(e, i))
                  : a === 'children'
                  ? typeof i == 'string'
                    ? (n !== 'textarea' || i !== '') && Tn(e, i)
                    : typeof i == 'number' && Tn(e, '' + i)
                  : a !== 'suppressContentEditableWarning' &&
                    a !== 'suppressHydrationWarning' &&
                    a !== 'autoFocus' &&
                    (jn.hasOwnProperty(a)
                      ? i != null && a === 'onScroll' && D('scroll', e)
                      : i != null && Ha(e, a, i, o));
              }
            switch (n) {
              case 'input':
                rr(e), Ao(e, r, !1);
                break;
              case 'textarea':
                rr(e), $o(e);
                break;
              case 'option':
                r.value != null && e.setAttribute('value', '' + ft(r.value));
                break;
              case 'select':
                (e.multiple = !!r.multiple),
                  (a = r.value),
                  a != null
                    ? Wt(e, !!r.multiple, a, !1)
                    : r.defaultValue != null &&
                      Wt(e, !!r.multiple, r.defaultValue, !0);
                break;
              default:
                typeof l.onClick == 'function' && (e.onclick = Fr);
            }
            switch (n) {
              case 'button':
              case 'input':
              case 'select':
              case 'textarea':
                r = !!r.autoFocus;
                break e;
              case 'img':
                r = !0;
                break e;
              default:
                r = !1;
            }
          }
          r && (t.flags |= 4);
        }
        t.ref !== null && ((t.flags |= 512), (t.flags |= 2097152));
      }
      return re(t), null;
    case 6:
      if (e && t.stateNode != null) Ds(e, t, e.memoizedProps, r);
      else {
        if (typeof r != 'string' && t.stateNode === null) throw Error(v(166));
        if (((n = xt(Hn.current)), xt(Ue.current), dr(t))) {
          if (
            ((r = t.stateNode),
            (n = t.memoizedProps),
            (r[Me] = t),
            (a = r.nodeValue !== n) && ((e = ve), e !== null))
          )
            switch (e.tag) {
              case 3:
                fr(r.nodeValue, n, (e.mode & 1) !== 0);
                break;
              case 5:
                e.memoizedProps.suppressHydrationWarning !== !0 &&
                  fr(r.nodeValue, n, (e.mode & 1) !== 0);
            }
          a && (t.flags |= 4);
        } else
          (r = (n.nodeType === 9 ? n : n.ownerDocument).createTextNode(r)),
            (r[Me] = t),
            (t.stateNode = r);
      }
      return re(t), null;
    case 13:
      if (
        (M(U),
        (r = t.memoizedState),
        e === null ||
          (e.memoizedState !== null && e.memoizedState.dehydrated !== null))
      ) {
        if (F && ge !== null && t.mode & 1 && !(t.flags & 128))
          es(), Zt(), (t.flags |= 98560), (a = !1);
        else if (((a = dr(t)), r !== null && r.dehydrated !== null)) {
          if (e === null) {
            if (!a) throw Error(v(318));
            if (
              ((a = t.memoizedState),
              (a = a !== null ? a.dehydrated : null),
              !a)
            )
              throw Error(v(317));
            a[Me] = t;
          } else
            Zt(), !(t.flags & 128) && (t.memoizedState = null), (t.flags |= 4);
          re(t), (a = !1);
        } else je !== null && (Da(je), (je = null)), (a = !0);
        if (!a) return t.flags & 65536 ? t : null;
      }
      return t.flags & 128
        ? ((t.lanes = n), t)
        : ((r = r !== null),
          r !== (e !== null && e.memoizedState !== null) &&
            r &&
            ((t.child.flags |= 8192),
            t.mode & 1 &&
              (e === null || U.current & 1 ? q === 0 && (q = 3) : No())),
          t.updateQueue !== null && (t.flags |= 4),
          re(t),
          null);
    case 4:
      return (
        tn(),
        La(e, t),
        e === null && Un(t.stateNode.containerInfo),
        re(t),
        null
      );
    case 10:
      return uo(t.type._context), re(t), null;
    case 17:
      return pe(t.type) && Ur(), re(t), null;
    case 19:
      if ((M(U), (a = t.memoizedState), a === null)) return re(t), null;
      if (((r = (t.flags & 128) !== 0), (o = a.rendering), o === null))
        if (r) gn(a, !1);
        else {
          if (q !== 0 || (e !== null && e.flags & 128))
            for (e = t.child; e !== null; ) {
              if (((o = Qr(e)), o !== null)) {
                for (
                  t.flags |= 128,
                    gn(a, !1),
                    r = o.updateQueue,
                    r !== null && ((t.updateQueue = r), (t.flags |= 4)),
                    t.subtreeFlags = 0,
                    r = n,
                    n = t.child;
                  n !== null;

                )
                  (a = n),
                    (e = r),
                    (a.flags &= 14680066),
                    (o = a.alternate),
                    o === null
                      ? ((a.childLanes = 0),
                        (a.lanes = e),
                        (a.child = null),
                        (a.subtreeFlags = 0),
                        (a.memoizedProps = null),
                        (a.memoizedState = null),
                        (a.updateQueue = null),
                        (a.dependencies = null),
                        (a.stateNode = null))
                      : ((a.childLanes = o.childLanes),
                        (a.lanes = o.lanes),
                        (a.child = o.child),
                        (a.subtreeFlags = 0),
                        (a.deletions = null),
                        (a.memoizedProps = o.memoizedProps),
                        (a.memoizedState = o.memoizedState),
                        (a.updateQueue = o.updateQueue),
                        (a.type = o.type),
                        (e = o.dependencies),
                        (a.dependencies =
                          e === null
                            ? null
                            : {
                                lanes: e.lanes,
                                firstContext: e.firstContext,
                              })),
                    (n = n.sibling);
                return O(U, (U.current & 1) | 2), t.child;
              }
              e = e.sibling;
            }
          a.tail !== null &&
            W() > rn &&
            ((t.flags |= 128), (r = !0), gn(a, !1), (t.lanes = 4194304));
        }
      else {
        if (!r)
          if (((e = Qr(o)), e !== null)) {
            if (
              ((t.flags |= 128),
              (r = !0),
              (n = e.updateQueue),
              n !== null && ((t.updateQueue = n), (t.flags |= 4)),
              gn(a, !0),
              a.tail === null && a.tailMode === 'hidden' && !o.alternate && !F)
            )
              return re(t), null;
          } else
            2 * W() - a.renderingStartTime > rn &&
              n !== 1073741824 &&
              ((t.flags |= 128), (r = !0), gn(a, !1), (t.lanes = 4194304));
        a.isBackwards
          ? ((o.sibling = t.child), (t.child = o))
          : ((n = a.last),
            n !== null ? (n.sibling = o) : (t.child = o),
            (a.last = o));
      }
      return a.tail !== null
        ? ((t = a.tail),
          (a.rendering = t),
          (a.tail = t.sibling),
          (a.renderingStartTime = W()),
          (t.sibling = null),
          (n = U.current),
          O(U, r ? (n & 1) | 2 : n & 1),
          t)
        : (re(t), null);
    case 22:
    case 23:
      return (
        Eo(),
        (r = t.memoizedState !== null),
        e !== null && (e.memoizedState !== null) !== r && (t.flags |= 8192),
        r && t.mode & 1
          ? he & 1073741824 && (re(t), t.subtreeFlags & 6 && (t.flags |= 8192))
          : re(t),
        null
      );
    case 24:
      return null;
    case 25:
      return null;
  }
  throw Error(v(156, t.tag));
}
function cd(e, t) {
  switch ((lo(t), t.tag)) {
    case 1:
      return (
        pe(t.type) && Ur(),
        (e = t.flags),
        e & 65536 ? ((t.flags = (e & -65537) | 128), t) : null
      );
    case 3:
      return (
        tn(),
        M(de),
        M(ae),
        mo(),
        (e = t.flags),
        e & 65536 && !(e & 128) ? ((t.flags = (e & -65537) | 128), t) : null
      );
    case 5:
      return po(t), null;
    case 13:
      if ((M(U), (e = t.memoizedState), e !== null && e.dehydrated !== null)) {
        if (t.alternate === null) throw Error(v(340));
        Zt();
      }
      return (
        (e = t.flags), e & 65536 ? ((t.flags = (e & -65537) | 128), t) : null
      );
    case 19:
      return M(U), null;
    case 4:
      return tn(), null;
    case 10:
      return uo(t.type._context), null;
    case 22:
    case 23:
      return Eo(), null;
    case 24:
      return null;
    default:
      return null;
  }
}
var hr = !1,
  le = !1,
  fd = typeof WeakSet == 'function' ? WeakSet : Set,
  x = null;
function Ht(e, t) {
  var n = e.ref;
  if (n !== null)
    if (typeof n == 'function')
      try {
        n(null);
      } catch (r) {
        $(e, t, r);
      }
    else n.current = null;
}
function Ms(e, t, n) {
  try {
    n();
  } catch (r) {
    $(e, t, r);
  }
}
var ji = !1;
function dd(e, t) {
  if (((pa = Or), (e = Vu()), no(e))) {
    if ('selectionStart' in e)
      var n = { start: e.selectionStart, end: e.selectionEnd };
    else
      e: {
        n = ((n = e.ownerDocument) && n.defaultView) || window;
        var r = n.getSelection && n.getSelection();
        if (r && r.rangeCount !== 0) {
          n = r.anchorNode;
          var l = r.anchorOffset,
            a = r.focusNode;
          r = r.focusOffset;
          try {
            n.nodeType, a.nodeType;
          } catch {
            n = null;
            break e;
          }
          var o = 0,
            u = -1,
            i = -1,
            c = 0,
            m = 0,
            h = e,
            p = null;
          t: for (;;) {
            for (
              var w;
              h !== n || (l !== 0 && h.nodeType !== 3) || (u = o + l),
                h !== a || (r !== 0 && h.nodeType !== 3) || (i = o + r),
                h.nodeType === 3 && (o += h.nodeValue.length),
                (w = h.firstChild) !== null;

            )
              (p = h), (h = w);
            for (;;) {
              if (h === e) break t;
              if (
                (p === n && ++c === l && (u = o),
                p === a && ++m === r && (i = o),
                (w = h.nextSibling) !== null)
              )
                break;
              (h = p), (p = h.parentNode);
            }
            h = w;
          }
          n = u === -1 || i === -1 ? null : { start: u, end: i };
        } else n = null;
      }
    n = n || { start: 0, end: 0 };
  } else n = null;
  for (
    ma = { focusedElem: e, selectionRange: n }, Or = !1, x = t;
    x !== null;

  )
    if (((t = x), (e = t.child), (t.subtreeFlags & 1028) !== 0 && e !== null))
      (e.return = t), (x = e);
    else
      for (; x !== null; ) {
        t = x;
        try {
          var b = t.alternate;
          if (t.flags & 1024)
            switch (t.tag) {
              case 0:
              case 11:
              case 15:
                break;
              case 1:
                if (b !== null) {
                  var k = b.memoizedProps,
                    T = b.memoizedState,
                    d = t.stateNode,
                    s = d.getSnapshotBeforeUpdate(
                      t.elementType === t.type ? k : Le(t.type, k),
                      T
                    );
                  d.__reactInternalSnapshotBeforeUpdate = s;
                }
                break;
              case 3:
                var f = t.stateNode.containerInfo;
                f.nodeType === 1
                  ? (f.textContent = '')
                  : f.nodeType === 9 &&
                    f.documentElement &&
                    f.removeChild(f.documentElement);
                break;
              case 5:
              case 6:
              case 4:
              case 17:
                break;
              default:
                throw Error(v(163));
            }
        } catch (y) {
          $(t, t.return, y);
        }
        if (((e = t.sibling), e !== null)) {
          (e.return = t.return), (x = e);
          break;
        }
        x = t.return;
      }
  return (b = ji), (ji = !1), b;
}
function Pn(e, t, n) {
  var r = t.updateQueue;
  if (((r = r !== null ? r.lastEffect : null), r !== null)) {
    var l = (r = r.next);
    do {
      if ((l.tag & e) === e) {
        var a = l.destroy;
        (l.destroy = void 0), a !== void 0 && Ms(t, n, a);
      }
      l = l.next;
    } while (l !== r);
  }
}
function sl(e, t) {
  if (
    ((t = t.updateQueue), (t = t !== null ? t.lastEffect : null), t !== null)
  ) {
    var n = (t = t.next);
    do {
      if ((n.tag & e) === e) {
        var r = n.create;
        n.destroy = r();
      }
      n = n.next;
    } while (n !== t);
  }
}
function za(e) {
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
    typeof t == 'function' ? t(e) : (t.current = e);
  }
}
function Fs(e) {
  var t = e.alternate;
  t !== null && ((e.alternate = null), Fs(t)),
    (e.child = null),
    (e.deletions = null),
    (e.sibling = null),
    e.tag === 5 &&
      ((t = e.stateNode),
      t !== null &&
        (delete t[Me],
        delete t[Vn],
        delete t[va],
        delete t[qf],
        delete t[Yf])),
    (e.stateNode = null),
    (e.return = null),
    (e.dependencies = null),
    (e.memoizedProps = null),
    (e.memoizedState = null),
    (e.pendingProps = null),
    (e.stateNode = null),
    (e.updateQueue = null);
}
function Us(e) {
  return e.tag === 5 || e.tag === 3 || e.tag === 4;
}
function Ti(e) {
  e: for (;;) {
    for (; e.sibling === null; ) {
      if (e.return === null || Us(e.return)) return null;
      e = e.return;
    }
    for (
      e.sibling.return = e.return, e = e.sibling;
      e.tag !== 5 && e.tag !== 6 && e.tag !== 18;

    ) {
      if (e.flags & 2 || e.child === null || e.tag === 4) continue e;
      (e.child.return = e), (e = e.child);
    }
    if (!(e.flags & 2)) return e.stateNode;
  }
}
function ja(e, t, n) {
  var r = e.tag;
  if (r === 5 || r === 6)
    (e = e.stateNode),
      t
        ? n.nodeType === 8
          ? n.parentNode.insertBefore(e, t)
          : n.insertBefore(e, t)
        : (n.nodeType === 8
            ? ((t = n.parentNode), t.insertBefore(e, n))
            : ((t = n), t.appendChild(e)),
          (n = n._reactRootContainer),
          n != null || t.onclick !== null || (t.onclick = Fr));
  else if (r !== 4 && ((e = e.child), e !== null))
    for (ja(e, t, n), e = e.sibling; e !== null; )
      ja(e, t, n), (e = e.sibling);
}
function Ta(e, t, n) {
  var r = e.tag;
  if (r === 5 || r === 6)
    (e = e.stateNode), t ? n.insertBefore(e, t) : n.appendChild(e);
  else if (r !== 4 && ((e = e.child), e !== null))
    for (Ta(e, t, n), e = e.sibling; e !== null; )
      Ta(e, t, n), (e = e.sibling);
}
var J = null,
  ze = !1;
function Ke(e, t, n) {
  for (n = n.child; n !== null; ) As(e, t, n), (n = n.sibling);
}
function As(e, t, n) {
  if (Fe && typeof Fe.onCommitFiberUnmount == 'function')
    try {
      Fe.onCommitFiberUnmount(tl, n);
    } catch {}
  switch (n.tag) {
    case 5:
      le || Ht(n, t);
    case 6:
      var r = J,
        l = ze;
      (J = null),
        Ke(e, t, n),
        (J = r),
        (ze = l),
        J !== null &&
          (ze
            ? ((e = J),
              (n = n.stateNode),
              e.nodeType === 8
                ? e.parentNode.removeChild(n)
                : e.removeChild(n))
            : J.removeChild(n.stateNode));
      break;
    case 18:
      J !== null &&
        (ze
          ? ((e = J),
            (n = n.stateNode),
            e.nodeType === 8
              ? Ol(e.parentNode, n)
              : e.nodeType === 1 && Ol(e, n),
            Dn(e))
          : Ol(J, n.stateNode));
      break;
    case 4:
      (r = J),
        (l = ze),
        (J = n.stateNode.containerInfo),
        (ze = !0),
        Ke(e, t, n),
        (J = r),
        (ze = l);
      break;
    case 0:
    case 11:
    case 14:
    case 15:
      if (
        !le &&
        ((r = n.updateQueue), r !== null && ((r = r.lastEffect), r !== null))
      ) {
        l = r = r.next;
        do {
          var a = l,
            o = a.destroy;
          (a = a.tag),
            o !== void 0 && (a & 2 || a & 4) && Ms(n, t, o),
            (l = l.next);
        } while (l !== r);
      }
      Ke(e, t, n);
      break;
    case 1:
      if (
        !le &&
        (Ht(n, t),
        (r = n.stateNode),
        typeof r.componentWillUnmount == 'function')
      )
        try {
          (r.props = n.memoizedProps),
            (r.state = n.memoizedState),
            r.componentWillUnmount();
        } catch (u) {
          $(n, t, u);
        }
      Ke(e, t, n);
      break;
    case 21:
      Ke(e, t, n);
      break;
    case 22:
      n.mode & 1
        ? ((le = (r = le) || n.memoizedState !== null), Ke(e, t, n), (le = r))
        : Ke(e, t, n);
      break;
    default:
      Ke(e, t, n);
  }
}
function Ri(e) {
  var t = e.updateQueue;
  if (t !== null) {
    e.updateQueue = null;
    var n = e.stateNode;
    n === null && (n = e.stateNode = new fd()),
      t.forEach(function (r) {
        var l = kd.bind(null, e, r);
        n.has(r) || (n.add(r), r.then(l, l));
      });
  }
}
function Pe(e, t) {
  var n = t.deletions;
  if (n !== null)
    for (var r = 0; r < n.length; r++) {
      var l = n[r];
      try {
        var a = e,
          o = t,
          u = o;
        e: for (; u !== null; ) {
          switch (u.tag) {
            case 5:
              (J = u.stateNode), (ze = !1);
              break e;
            case 3:
              (J = u.stateNode.containerInfo), (ze = !0);
              break e;
            case 4:
              (J = u.stateNode.containerInfo), (ze = !0);
              break e;
          }
          u = u.return;
        }
        if (J === null) throw Error(v(160));
        As(a, o, l), (J = null), (ze = !1);
        var i = l.alternate;
        i !== null && (i.return = null), (l.return = null);
      } catch (c) {
        $(l, t, c);
      }
    }
  if (t.subtreeFlags & 12854)
    for (t = t.child; t !== null; ) Vs(t, e), (t = t.sibling);
}
function Vs(e, t) {
  var n = e.alternate,
    r = e.flags;
  switch (e.tag) {
    case 0:
    case 11:
    case 14:
    case 15:
      if ((Pe(t, e), Oe(e), r & 4)) {
        try {
          Pn(3, e, e.return), sl(3, e);
        } catch (k) {
          $(e, e.return, k);
        }
        try {
          Pn(5, e, e.return);
        } catch (k) {
          $(e, e.return, k);
        }
      }
      break;
    case 1:
      Pe(t, e), Oe(e), r & 512 && n !== null && Ht(n, n.return);
      break;
    case 5:
      if (
        (Pe(t, e),
        Oe(e),
        r & 512 && n !== null && Ht(n, n.return),
        e.flags & 32)
      ) {
        var l = e.stateNode;
        try {
          Tn(l, '');
        } catch (k) {
          $(e, e.return, k);
        }
      }
      if (r & 4 && ((l = e.stateNode), l != null)) {
        var a = e.memoizedProps,
          o = n !== null ? n.memoizedProps : a,
          u = e.type,
          i = e.updateQueue;
        if (((e.updateQueue = null), i !== null))
          try {
            u === 'input' && a.type === 'radio' && a.name != null && uu(l, a),
              ra(u, o);
            var c = ra(u, a);
            for (o = 0; o < i.length; o += 2) {
              var m = i[o],
                h = i[o + 1];
              m === 'style'
                ? pu(l, h)
                : m === 'dangerouslySetInnerHTML'
                ? fu(l, h)
                : m === 'children'
                ? Tn(l, h)
                : Ha(l, m, h, c);
            }
            switch (u) {
              case 'input':
                Jl(l, a);
                break;
              case 'textarea':
                su(l, a);
                break;
              case 'select':
                var p = l._wrapperState.wasMultiple;
                l._wrapperState.wasMultiple = !!a.multiple;
                var w = a.value;
                w != null
                  ? Wt(l, !!a.multiple, w, !1)
                  : p !== !!a.multiple &&
                    (a.defaultValue != null
                      ? Wt(l, !!a.multiple, a.defaultValue, !0)
                      : Wt(l, !!a.multiple, a.multiple ? [] : '', !1));
            }
            l[Vn] = a;
          } catch (k) {
            $(e, e.return, k);
          }
      }
      break;
    case 6:
      if ((Pe(t, e), Oe(e), r & 4)) {
        if (e.stateNode === null) throw Error(v(162));
        (l = e.stateNode), (a = e.memoizedProps);
        try {
          l.nodeValue = a;
        } catch (k) {
          $(e, e.return, k);
        }
      }
      break;
    case 3:
      if (
        (Pe(t, e), Oe(e), r & 4 && n !== null && n.memoizedState.isDehydrated)
      )
        try {
          Dn(t.containerInfo);
        } catch (k) {
          $(e, e.return, k);
        }
      break;
    case 4:
      Pe(t, e), Oe(e);
      break;
    case 13:
      Pe(t, e),
        Oe(e),
        (l = e.child),
        l.flags & 8192 &&
          ((a = l.memoizedState !== null),
          (l.stateNode.isHidden = a),
          !a ||
            (l.alternate !== null && l.alternate.memoizedState !== null) ||
            (So = W())),
        r & 4 && Ri(e);
      break;
    case 22:
      if (
        ((m = n !== null && n.memoizedState !== null),
        e.mode & 1 ? ((le = (c = le) || m), Pe(t, e), (le = c)) : Pe(t, e),
        Oe(e),
        r & 8192)
      ) {
        if (
          ((c = e.memoizedState !== null),
          (e.stateNode.isHidden = c) && !m && e.mode & 1)
        )
          for (x = e, m = e.child; m !== null; ) {
            for (h = x = m; x !== null; ) {
              switch (((p = x), (w = p.child), p.tag)) {
                case 0:
                case 11:
                case 14:
                case 15:
                  Pn(4, p, p.return);
                  break;
                case 1:
                  Ht(p, p.return);
                  var b = p.stateNode;
                  if (typeof b.componentWillUnmount == 'function') {
                    (r = p), (n = p.return);
                    try {
                      (t = r),
                        (b.props = t.memoizedProps),
                        (b.state = t.memoizedState),
                        b.componentWillUnmount();
                    } catch (k) {
                      $(r, n, k);
                    }
                  }
                  break;
                case 5:
                  Ht(p, p.return);
                  break;
                case 22:
                  if (p.memoizedState !== null) {
                    Oi(h);
                    continue;
                  }
              }
              w !== null ? ((w.return = p), (x = w)) : Oi(h);
            }
            m = m.sibling;
          }
        e: for (m = null, h = e; ; ) {
          if (h.tag === 5) {
            if (m === null) {
              m = h;
              try {
                (l = h.stateNode),
                  c
                    ? ((a = l.style),
                      typeof a.setProperty == 'function'
                        ? a.setProperty('display', 'none', 'important')
                        : (a.display = 'none'))
                    : ((u = h.stateNode),
                      (i = h.memoizedProps.style),
                      (o =
                        i != null && i.hasOwnProperty('display')
                          ? i.display
                          : null),
                      (u.style.display = du('display', o)));
              } catch (k) {
                $(e, e.return, k);
              }
            }
          } else if (h.tag === 6) {
            if (m === null)
              try {
                h.stateNode.nodeValue = c ? '' : h.memoizedProps;
              } catch (k) {
                $(e, e.return, k);
              }
          } else if (
            ((h.tag !== 22 && h.tag !== 23) ||
              h.memoizedState === null ||
              h === e) &&
            h.child !== null
          ) {
            (h.child.return = h), (h = h.child);
            continue;
          }
          if (h === e) break e;
          for (; h.sibling === null; ) {
            if (h.return === null || h.return === e) break e;
            m === h && (m = null), (h = h.return);
          }
          m === h && (m = null),
            (h.sibling.return = h.return),
            (h = h.sibling);
        }
      }
      break;
    case 19:
      Pe(t, e), Oe(e), r & 4 && Ri(e);
      break;
    case 21:
      break;
    default:
      Pe(t, e), Oe(e);
  }
}
function Oe(e) {
  var t = e.flags;
  if (t & 2) {
    try {
      e: {
        for (var n = e.return; n !== null; ) {
          if (Us(n)) {
            var r = n;
            break e;
          }
          n = n.return;
        }
        throw Error(v(160));
      }
      switch (r.tag) {
        case 5:
          var l = r.stateNode;
          r.flags & 32 && (Tn(l, ''), (r.flags &= -33));
          var a = Ti(e);
          Ta(e, a, l);
          break;
        case 3:
        case 4:
          var o = r.stateNode.containerInfo,
            u = Ti(e);
          ja(e, u, o);
          break;
        default:
          throw Error(v(161));
      }
    } catch (i) {
      $(e, e.return, i);
    }
    e.flags &= -3;
  }
  t & 4096 && (e.flags &= -4097);
}
function pd(e, t, n) {
  (x = e), $s(e);
}
function $s(e, t, n) {
  for (var r = (e.mode & 1) !== 0; x !== null; ) {
    var l = x,
      a = l.child;
    if (l.tag === 22 && r) {
      var o = l.memoizedState !== null || hr;
      if (!o) {
        var u = l.alternate,
          i = (u !== null && u.memoizedState !== null) || le;
        u = hr;
        var c = le;
        if (((hr = o), (le = i) && !c))
          for (x = l; x !== null; )
            (o = x),
              (i = o.child),
              o.tag === 22 && o.memoizedState !== null
                ? Di(l)
                : i !== null
                ? ((i.return = o), (x = i))
                : Di(l);
        for (; a !== null; ) (x = a), $s(a), (a = a.sibling);
        (x = l), (hr = u), (le = c);
      }
      Ii(e);
    } else
      l.subtreeFlags & 8772 && a !== null ? ((a.return = l), (x = a)) : Ii(e);
  }
}
function Ii(e) {
  for (; x !== null; ) {
    var t = x;
    if (t.flags & 8772) {
      var n = t.alternate;
      try {
        if (t.flags & 8772)
          switch (t.tag) {
            case 0:
            case 11:
            case 15:
              le || sl(5, t);
              break;
            case 1:
              var r = t.stateNode;
              if (t.flags & 4 && !le)
                if (n === null) r.componentDidMount();
                else {
                  var l =
                    t.elementType === t.type
                      ? n.memoizedProps
                      : Le(t.type, n.memoizedProps);
                  r.componentDidUpdate(
                    l,
                    n.memoizedState,
                    r.__reactInternalSnapshotBeforeUpdate
                  );
                }
              var a = t.updateQueue;
              a !== null && yi(t, a, r);
              break;
            case 3:
              var o = t.updateQueue;
              if (o !== null) {
                if (((n = null), t.child !== null))
                  switch (t.child.tag) {
                    case 5:
                      n = t.child.stateNode;
                      break;
                    case 1:
                      n = t.child.stateNode;
                  }
                yi(t, o, n);
              }
              break;
            case 5:
              var u = t.stateNode;
              if (n === null && t.flags & 4) {
                n = u;
                var i = t.memoizedProps;
                switch (t.type) {
                  case 'button':
                  case 'input':
                  case 'select':
                  case 'textarea':
                    i.autoFocus && n.focus();
                    break;
                  case 'img':
                    i.src && (n.src = i.src);
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
                var c = t.alternate;
                if (c !== null) {
                  var m = c.memoizedState;
                  if (m !== null) {
                    var h = m.dehydrated;
                    h !== null && Dn(h);
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
              throw Error(v(163));
          }
        le || (t.flags & 512 && za(t));
      } catch (p) {
        $(t, t.return, p);
      }
    }
    if (t === e) {
      x = null;
      break;
    }
    if (((n = t.sibling), n !== null)) {
      (n.return = t.return), (x = n);
      break;
    }
    x = t.return;
  }
}
function Oi(e) {
  for (; x !== null; ) {
    var t = x;
    if (t === e) {
      x = null;
      break;
    }
    var n = t.sibling;
    if (n !== null) {
      (n.return = t.return), (x = n);
      break;
    }
    x = t.return;
  }
}
function Di(e) {
  for (; x !== null; ) {
    var t = x;
    try {
      switch (t.tag) {
        case 0:
        case 11:
        case 15:
          var n = t.return;
          try {
            sl(4, t);
          } catch (i) {
            $(t, n, i);
          }
          break;
        case 1:
          var r = t.stateNode;
          if (typeof r.componentDidMount == 'function') {
            var l = t.return;
            try {
              r.componentDidMount();
            } catch (i) {
              $(t, l, i);
            }
          }
          var a = t.return;
          try {
            za(t);
          } catch (i) {
            $(t, a, i);
          }
          break;
        case 5:
          var o = t.return;
          try {
            za(t);
          } catch (i) {
            $(t, o, i);
          }
      }
    } catch (i) {
      $(t, t.return, i);
    }
    if (t === e) {
      x = null;
      break;
    }
    var u = t.sibling;
    if (u !== null) {
      (u.return = t.return), (x = u);
      break;
    }
    x = t.return;
  }
}
var md = Math.ceil,
  Yr = Ye.ReactCurrentDispatcher,
  ko = Ye.ReactCurrentOwner,
  _e = Ye.ReactCurrentBatchConfig,
  R = 0,
  G = null,
  Q = null,
  ee = 0,
  he = 0,
  Bt = mt(0),
  q = 0,
  Xn = null,
  Pt = 0,
  cl = 0,
  xo = 0,
  Ln = null,
  ce = null,
  So = 0,
  rn = 1 / 0,
  Ae = null,
  Kr = !1,
  Ra = null,
  ut = null,
  gr = !1,
  nt = null,
  Gr = 0,
  zn = 0,
  Ia = null,
  Cr = -1,
  Pr = 0;
function ie() {
  return R & 6 ? W() : Cr !== -1 ? Cr : (Cr = W());
}
function st(e) {
  return e.mode & 1
    ? R & 2 && ee !== 0
      ? ee & -ee
      : Gf.transition !== null
      ? (Pr === 0 && (Pr = Eu()), Pr)
      : ((e = I),
        e !== 0 || ((e = window.event), (e = e === void 0 ? 16 : Tu(e.type))),
        e)
    : 1;
}
function Re(e, t, n, r) {
  if (50 < zn) throw ((zn = 0), (Ia = null), Error(v(185)));
  Yn(e, n, r),
    (!(R & 2) || e !== G) &&
      (e === G && (!(R & 2) && (cl |= n), q === 4 && et(e, ee)),
      me(e, r),
      n === 1 && R === 0 && !(t.mode & 1) && ((rn = W() + 500), ol && ht()));
}
function me(e, t) {
  var n = e.callbackNode;
  Kc(e, t);
  var r = Ir(e, e === G ? ee : 0);
  if (r === 0)
    n !== null && Wo(n), (e.callbackNode = null), (e.callbackPriority = 0);
  else if (((t = r & -r), e.callbackPriority !== t)) {
    if ((n != null && Wo(n), t === 1))
      e.tag === 0 ? Kf(Mi.bind(null, e)) : Gu(Mi.bind(null, e)),
        Qf(function () {
          !(R & 6) && ht();
        }),
        (n = null);
    else {
      switch (Nu(r)) {
        case 1:
          n = qa;
          break;
        case 4:
          n = Su;
          break;
        case 16:
          n = Rr;
          break;
        case 536870912:
          n = _u;
          break;
        default:
          n = Rr;
      }
      n = Ks(n, Hs.bind(null, e));
    }
    (e.callbackPriority = t), (e.callbackNode = n);
  }
}
function Hs(e, t) {
  if (((Cr = -1), (Pr = 0), R & 6)) throw Error(v(327));
  var n = e.callbackNode;
  if (Kt() && e.callbackNode !== n) return null;
  var r = Ir(e, e === G ? ee : 0);
  if (r === 0) return null;
  if (r & 30 || r & e.expiredLanes || t) t = Jr(e, r);
  else {
    t = r;
    var l = R;
    R |= 2;
    var a = Ws();
    (G !== e || ee !== t) && ((Ae = null), (rn = W() + 500), St(e, t));
    do
      try {
        vd();
        break;
      } catch (u) {
        Bs(e, u);
      }
    while (!0);
    io(),
      (Yr.current = a),
      (R = l),
      Q !== null ? (t = 0) : ((G = null), (ee = 0), (t = q));
  }
  if (t !== 0) {
    if (
      (t === 2 && ((l = ua(e)), l !== 0 && ((r = l), (t = Oa(e, l)))), t === 1)
    )
      throw ((n = Xn), St(e, 0), et(e, r), me(e, W()), n);
    if (t === 6) et(e, r);
    else {
      if (
        ((l = e.current.alternate),
        !(r & 30) &&
          !hd(l) &&
          ((t = Jr(e, r)),
          t === 2 && ((a = ua(e)), a !== 0 && ((r = a), (t = Oa(e, a)))),
          t === 1))
      )
        throw ((n = Xn), St(e, 0), et(e, r), me(e, W()), n);
      switch (((e.finishedWork = l), (e.finishedLanes = r), t)) {
        case 0:
        case 1:
          throw Error(v(345));
        case 2:
          bt(e, ce, Ae);
          break;
        case 3:
          if (
            (et(e, r), (r & 130023424) === r && ((t = So + 500 - W()), 10 < t))
          ) {
            if (Ir(e, 0) !== 0) break;
            if (((l = e.suspendedLanes), (l & r) !== r)) {
              ie(), (e.pingedLanes |= e.suspendedLanes & l);
              break;
            }
            e.timeoutHandle = ga(bt.bind(null, e, ce, Ae), t);
            break;
          }
          bt(e, ce, Ae);
          break;
        case 4:
          if ((et(e, r), (r & 4194240) === r)) break;
          for (t = e.eventTimes, l = -1; 0 < r; ) {
            var o = 31 - Te(r);
            (a = 1 << o), (o = t[o]), o > l && (l = o), (r &= ~a);
          }
          if (
            ((r = l),
            (r = W() - r),
            (r =
              (120 > r
                ? 120
                : 480 > r
                ? 480
                : 1080 > r
                ? 1080
                : 1920 > r
                ? 1920
                : 3e3 > r
                ? 3e3
                : 4320 > r
                ? 4320
                : 1960 * md(r / 1960)) - r),
            10 < r)
          ) {
            e.timeoutHandle = ga(bt.bind(null, e, ce, Ae), r);
            break;
          }
          bt(e, ce, Ae);
          break;
        case 5:
          bt(e, ce, Ae);
          break;
        default:
          throw Error(v(329));
      }
    }
  }
  return me(e, W()), e.callbackNode === n ? Hs.bind(null, e) : null;
}
function Oa(e, t) {
  var n = Ln;
  return (
    e.current.memoizedState.isDehydrated && (St(e, t).flags |= 256),
    (e = Jr(e, t)),
    e !== 2 && ((t = ce), (ce = n), t !== null && Da(t)),
    e
  );
}
function Da(e) {
  ce === null ? (ce = e) : ce.push.apply(ce, e);
}
function hd(e) {
  for (var t = e; ; ) {
    if (t.flags & 16384) {
      var n = t.updateQueue;
      if (n !== null && ((n = n.stores), n !== null))
        for (var r = 0; r < n.length; r++) {
          var l = n[r],
            a = l.getSnapshot;
          l = l.value;
          try {
            if (!Ie(a(), l)) return !1;
          } catch {
            return !1;
          }
        }
    }
    if (((n = t.child), t.subtreeFlags & 16384 && n !== null))
      (n.return = t), (t = n);
    else {
      if (t === e) break;
      for (; t.sibling === null; ) {
        if (t.return === null || t.return === e) return !0;
        t = t.return;
      }
      (t.sibling.return = t.return), (t = t.sibling);
    }
  }
  return !0;
}
function et(e, t) {
  for (
    t &= ~xo,
      t &= ~cl,
      e.suspendedLanes |= t,
      e.pingedLanes &= ~t,
      e = e.expirationTimes;
    0 < t;

  ) {
    var n = 31 - Te(t),
      r = 1 << n;
    (e[n] = -1), (t &= ~r);
  }
}
function Mi(e) {
  if (R & 6) throw Error(v(327));
  Kt();
  var t = Ir(e, 0);
  if (!(t & 1)) return me(e, W()), null;
  var n = Jr(e, t);
  if (e.tag !== 0 && n === 2) {
    var r = ua(e);
    r !== 0 && ((t = r), (n = Oa(e, r)));
  }
  if (n === 1) throw ((n = Xn), St(e, 0), et(e, t), me(e, W()), n);
  if (n === 6) throw Error(v(345));
  return (
    (e.finishedWork = e.current.alternate),
    (e.finishedLanes = t),
    bt(e, ce, Ae),
    me(e, W()),
    null
  );
}
function _o(e, t) {
  var n = R;
  R |= 1;
  try {
    return e(t);
  } finally {
    (R = n), R === 0 && ((rn = W() + 500), ol && ht());
  }
}
function Lt(e) {
  nt !== null && nt.tag === 0 && !(R & 6) && Kt();
  var t = R;
  R |= 1;
  var n = _e.transition,
    r = I;
  try {
    if (((_e.transition = null), (I = 1), e)) return e();
  } finally {
    (I = r), (_e.transition = n), (R = t), !(R & 6) && ht();
  }
}
function Eo() {
  (he = Bt.current), M(Bt);
}
function St(e, t) {
  (e.finishedWork = null), (e.finishedLanes = 0);
  var n = e.timeoutHandle;
  if ((n !== -1 && ((e.timeoutHandle = -1), Wf(n)), Q !== null))
    for (n = Q.return; n !== null; ) {
      var r = n;
      switch ((lo(r), r.tag)) {
        case 1:
          (r = r.type.childContextTypes), r != null && Ur();
          break;
        case 3:
          tn(), M(de), M(ae), mo();
          break;
        case 5:
          po(r);
          break;
        case 4:
          tn();
          break;
        case 13:
          M(U);
          break;
        case 19:
          M(U);
          break;
        case 10:
          uo(r.type._context);
          break;
        case 22:
        case 23:
          Eo();
      }
      n = n.return;
    }
  if (
    ((G = e),
    (Q = e = ct(e.current, null)),
    (ee = he = t),
    (q = 0),
    (Xn = null),
    (xo = cl = Pt = 0),
    (ce = Ln = null),
    kt !== null)
  ) {
    for (t = 0; t < kt.length; t++)
      if (((n = kt[t]), (r = n.interleaved), r !== null)) {
        n.interleaved = null;
        var l = r.next,
          a = n.pending;
        if (a !== null) {
          var o = a.next;
          (a.next = l), (r.next = o);
        }
        n.pending = r;
      }
    kt = null;
  }
  return e;
}
function Bs(e, t) {
  do {
    var n = Q;
    try {
      if ((io(), (_r.current = qr), Xr)) {
        for (var r = A.memoizedState; r !== null; ) {
          var l = r.queue;
          l !== null && (l.pending = null), (r = r.next);
        }
        Xr = !1;
      }
      if (
        ((Ct = 0),
        (K = X = A = null),
        (Cn = !1),
        (Bn = 0),
        (ko.current = null),
        n === null || n.return === null)
      ) {
        (q = 1), (Xn = t), (Q = null);
        break;
      }
      e: {
        var a = e,
          o = n.return,
          u = n,
          i = t;
        if (
          ((t = ee),
          (u.flags |= 32768),
          i !== null && typeof i == 'object' && typeof i.then == 'function')
        ) {
          var c = i,
            m = u,
            h = m.tag;
          if (!(m.mode & 1) && (h === 0 || h === 11 || h === 15)) {
            var p = m.alternate;
            p
              ? ((m.updateQueue = p.updateQueue),
                (m.memoizedState = p.memoizedState),
                (m.lanes = p.lanes))
              : ((m.updateQueue = null), (m.memoizedState = null));
          }
          var w = _i(o);
          if (w !== null) {
            (w.flags &= -257),
              Ei(w, o, u, a, t),
              w.mode & 1 && Si(a, c, t),
              (t = w),
              (i = c);
            var b = t.updateQueue;
            if (b === null) {
              var k = new Set();
              k.add(i), (t.updateQueue = k);
            } else b.add(i);
            break e;
          } else {
            if (!(t & 1)) {
              Si(a, c, t), No();
              break e;
            }
            i = Error(v(426));
          }
        } else if (F && u.mode & 1) {
          var T = _i(o);
          if (T !== null) {
            !(T.flags & 65536) && (T.flags |= 256),
              Ei(T, o, u, a, t),
              ao(nn(i, u));
            break e;
          }
        }
        (a = i = nn(i, u)),
          q !== 4 && (q = 2),
          Ln === null ? (Ln = [a]) : Ln.push(a),
          (a = o);
        do {
          switch (a.tag) {
            case 3:
              (a.flags |= 65536), (t &= -t), (a.lanes |= t);
              var d = Ns(a, i, t);
              vi(a, d);
              break e;
            case 1:
              u = i;
              var s = a.type,
                f = a.stateNode;
              if (
                !(a.flags & 128) &&
                (typeof s.getDerivedStateFromError == 'function' ||
                  (f !== null &&
                    typeof f.componentDidCatch == 'function' &&
                    (ut === null || !ut.has(f))))
              ) {
                (a.flags |= 65536), (t &= -t), (a.lanes |= t);
                var y = Cs(a, u, t);
                vi(a, y);
                break e;
              }
          }
          a = a.return;
        } while (a !== null);
      }
      Xs(n);
    } catch (_) {
      (t = _), Q === n && n !== null && (Q = n = n.return);
      continue;
    }
    break;
  } while (!0);
}
function Ws() {
  var e = Yr.current;
  return (Yr.current = qr), e === null ? qr : e;
}
function No() {
  (q === 0 || q === 3 || q === 2) && (q = 4),
    G === null || (!(Pt & 268435455) && !(cl & 268435455)) || et(G, ee);
}
function Jr(e, t) {
  var n = R;
  R |= 2;
  var r = Ws();
  (G !== e || ee !== t) && ((Ae = null), St(e, t));
  do
    try {
      gd();
      break;
    } catch (l) {
      Bs(e, l);
    }
  while (!0);
  if ((io(), (R = n), (Yr.current = r), Q !== null)) throw Error(v(261));
  return (G = null), (ee = 0), q;
}
function gd() {
  for (; Q !== null; ) Qs(Q);
}
function vd() {
  for (; Q !== null && !Vc(); ) Qs(Q);
}
function Qs(e) {
  var t = Ys(e.alternate, e, he);
  (e.memoizedProps = e.pendingProps),
    t === null ? Xs(e) : (Q = t),
    (ko.current = null);
}
function Xs(e) {
  var t = e;
  do {
    var n = t.alternate;
    if (((e = t.return), t.flags & 32768)) {
      if (((n = cd(n, t)), n !== null)) {
        (n.flags &= 32767), (Q = n);
        return;
      }
      if (e !== null)
        (e.flags |= 32768), (e.subtreeFlags = 0), (e.deletions = null);
      else {
        (q = 6), (Q = null);
        return;
      }
    } else if (((n = sd(n, t, he)), n !== null)) {
      Q = n;
      return;
    }
    if (((t = t.sibling), t !== null)) {
      Q = t;
      return;
    }
    Q = t = e;
  } while (t !== null);
  q === 0 && (q = 5);
}
function bt(e, t, n) {
  var r = I,
    l = _e.transition;
  try {
    (_e.transition = null), (I = 1), yd(e, t, n, r);
  } finally {
    (_e.transition = l), (I = r);
  }
  return null;
}
function yd(e, t, n, r) {
  do Kt();
  while (nt !== null);
  if (R & 6) throw Error(v(327));
  n = e.finishedWork;
  var l = e.finishedLanes;
  if (n === null) return null;
  if (((e.finishedWork = null), (e.finishedLanes = 0), n === e.current))
    throw Error(v(177));
  (e.callbackNode = null), (e.callbackPriority = 0);
  var a = n.lanes | n.childLanes;
  if (
    (Gc(e, a),
    e === G && ((Q = G = null), (ee = 0)),
    (!(n.subtreeFlags & 2064) && !(n.flags & 2064)) ||
      gr ||
      ((gr = !0),
      Ks(Rr, function () {
        return Kt(), null;
      })),
    (a = (n.flags & 15990) !== 0),
    n.subtreeFlags & 15990 || a)
  ) {
    (a = _e.transition), (_e.transition = null);
    var o = I;
    I = 1;
    var u = R;
    (R |= 4),
      (ko.current = null),
      dd(e, n),
      Vs(n, e),
      Ff(ma),
      (Or = !!pa),
      (ma = pa = null),
      (e.current = n),
      pd(n),
      $c(),
      (R = u),
      (I = o),
      (_e.transition = a);
  } else e.current = n;
  if (
    (gr && ((gr = !1), (nt = e), (Gr = l)),
    (a = e.pendingLanes),
    a === 0 && (ut = null),
    Wc(n.stateNode),
    me(e, W()),
    t !== null)
  )
    for (r = e.onRecoverableError, n = 0; n < t.length; n++)
      (l = t[n]), r(l.value, { componentStack: l.stack, digest: l.digest });
  if (Kr) throw ((Kr = !1), (e = Ra), (Ra = null), e);
  return (
    Gr & 1 && e.tag !== 0 && Kt(),
    (a = e.pendingLanes),
    a & 1 ? (e === Ia ? zn++ : ((zn = 0), (Ia = e))) : (zn = 0),
    ht(),
    null
  );
}
function Kt() {
  if (nt !== null) {
    var e = Nu(Gr),
      t = _e.transition,
      n = I;
    try {
      if (((_e.transition = null), (I = 16 > e ? 16 : e), nt === null))
        var r = !1;
      else {
        if (((e = nt), (nt = null), (Gr = 0), R & 6)) throw Error(v(331));
        var l = R;
        for (R |= 4, x = e.current; x !== null; ) {
          var a = x,
            o = a.child;
          if (x.flags & 16) {
            var u = a.deletions;
            if (u !== null) {
              for (var i = 0; i < u.length; i++) {
                var c = u[i];
                for (x = c; x !== null; ) {
                  var m = x;
                  switch (m.tag) {
                    case 0:
                    case 11:
                    case 15:
                      Pn(8, m, a);
                  }
                  var h = m.child;
                  if (h !== null) (h.return = m), (x = h);
                  else
                    for (; x !== null; ) {
                      m = x;
                      var p = m.sibling,
                        w = m.return;
                      if ((Fs(m), m === c)) {
                        x = null;
                        break;
                      }
                      if (p !== null) {
                        (p.return = w), (x = p);
                        break;
                      }
                      x = w;
                    }
                }
              }
              var b = a.alternate;
              if (b !== null) {
                var k = b.child;
                if (k !== null) {
                  b.child = null;
                  do {
                    var T = k.sibling;
                    (k.sibling = null), (k = T);
                  } while (k !== null);
                }
              }
              x = a;
            }
          }
          if (a.subtreeFlags & 2064 && o !== null) (o.return = a), (x = o);
          else
            e: for (; x !== null; ) {
              if (((a = x), a.flags & 2048))
                switch (a.tag) {
                  case 0:
                  case 11:
                  case 15:
                    Pn(9, a, a.return);
                }
              var d = a.sibling;
              if (d !== null) {
                (d.return = a.return), (x = d);
                break e;
              }
              x = a.return;
            }
        }
        var s = e.current;
        for (x = s; x !== null; ) {
          o = x;
          var f = o.child;
          if (o.subtreeFlags & 2064 && f !== null) (f.return = o), (x = f);
          else
            e: for (o = s; x !== null; ) {
              if (((u = x), u.flags & 2048))
                try {
                  switch (u.tag) {
                    case 0:
                    case 11:
                    case 15:
                      sl(9, u);
                  }
                } catch (_) {
                  $(u, u.return, _);
                }
              if (u === o) {
                x = null;
                break e;
              }
              var y = u.sibling;
              if (y !== null) {
                (y.return = u.return), (x = y);
                break e;
              }
              x = u.return;
            }
        }
        if (
          ((R = l), ht(), Fe && typeof Fe.onPostCommitFiberRoot == 'function')
        )
          try {
            Fe.onPostCommitFiberRoot(tl, e);
          } catch {}
        r = !0;
      }
      return r;
    } finally {
      (I = n), (_e.transition = t);
    }
  }
  return !1;
}
function Fi(e, t, n) {
  (t = nn(n, t)),
    (t = Ns(e, t, 1)),
    (e = it(e, t, 1)),
    (t = ie()),
    e !== null && (Yn(e, 1, t), me(e, t));
}
function $(e, t, n) {
  if (e.tag === 3) Fi(e, e, n);
  else
    for (; t !== null; ) {
      if (t.tag === 3) {
        Fi(t, e, n);
        break;
      } else if (t.tag === 1) {
        var r = t.stateNode;
        if (
          typeof t.type.getDerivedStateFromError == 'function' ||
          (typeof r.componentDidCatch == 'function' &&
            (ut === null || !ut.has(r)))
        ) {
          (e = nn(n, e)),
            (e = Cs(t, e, 1)),
            (t = it(t, e, 1)),
            (e = ie()),
            t !== null && (Yn(t, 1, e), me(t, e));
          break;
        }
      }
      t = t.return;
    }
}
function bd(e, t, n) {
  var r = e.pingCache;
  r !== null && r.delete(t),
    (t = ie()),
    (e.pingedLanes |= e.suspendedLanes & n),
    G === e &&
      (ee & n) === n &&
      (q === 4 || (q === 3 && (ee & 130023424) === ee && 500 > W() - So)
        ? St(e, 0)
        : (xo |= n)),
    me(e, t);
}
function qs(e, t) {
  t === 0 &&
    (e.mode & 1
      ? ((t = or), (or <<= 1), !(or & 130023424) && (or = 4194304))
      : (t = 1));
  var n = ie();
  (e = Xe(e, t)), e !== null && (Yn(e, t, n), me(e, n));
}
function wd(e) {
  var t = e.memoizedState,
    n = 0;
  t !== null && (n = t.retryLane), qs(e, n);
}
function kd(e, t) {
  var n = 0;
  switch (e.tag) {
    case 13:
      var r = e.stateNode,
        l = e.memoizedState;
      l !== null && (n = l.retryLane);
      break;
    case 19:
      r = e.stateNode;
      break;
    default:
      throw Error(v(314));
  }
  r !== null && r.delete(t), qs(e, n);
}
var Ys;
Ys = function (e, t, n) {
  if (e !== null)
    if (e.memoizedProps !== t.pendingProps || de.current) fe = !0;
    else {
      if (!(e.lanes & n) && !(t.flags & 128)) return (fe = !1), ud(e, t, n);
      fe = !!(e.flags & 131072);
    }
  else (fe = !1), F && t.flags & 1048576 && Ju(t, $r, t.index);
  switch (((t.lanes = 0), t.tag)) {
    case 2:
      var r = t.type;
      Nr(e, t), (e = t.pendingProps);
      var l = Jt(t, ae.current);
      Yt(t, n), (l = go(null, t, r, e, l, n));
      var a = vo();
      return (
        (t.flags |= 1),
        typeof l == 'object' &&
        l !== null &&
        typeof l.render == 'function' &&
        l.$$typeof === void 0
          ? ((t.tag = 1),
            (t.memoizedState = null),
            (t.updateQueue = null),
            pe(r) ? ((a = !0), Ar(t)) : (a = !1),
            (t.memoizedState =
              l.state !== null && l.state !== void 0 ? l.state : null),
            co(t),
            (l.updater = ul),
            (t.stateNode = l),
            (l._reactInternals = t),
            Sa(t, r, e, n),
            (t = Na(null, t, r, !0, a, n)))
          : ((t.tag = 0), F && a && ro(t), oe(null, t, l, n), (t = t.child)),
        t
      );
    case 16:
      r = t.elementType;
      e: {
        switch (
          (Nr(e, t),
          (e = t.pendingProps),
          (l = r._init),
          (r = l(r._payload)),
          (t.type = r),
          (l = t.tag = Sd(r)),
          (e = Le(r, e)),
          l)
        ) {
          case 0:
            t = Ea(null, t, r, e, n);
            break e;
          case 1:
            t = Pi(null, t, r, e, n);
            break e;
          case 11:
            t = Ni(null, t, r, e, n);
            break e;
          case 14:
            t = Ci(null, t, r, Le(r.type, e), n);
            break e;
        }
        throw Error(v(306, r, ''));
      }
      return t;
    case 0:
      return (
        (r = t.type),
        (l = t.pendingProps),
        (l = t.elementType === r ? l : Le(r, l)),
        Ea(e, t, r, l, n)
      );
    case 1:
      return (
        (r = t.type),
        (l = t.pendingProps),
        (l = t.elementType === r ? l : Le(r, l)),
        Pi(e, t, r, l, n)
      );
    case 3:
      e: {
        if ((js(t), e === null)) throw Error(v(387));
        (r = t.pendingProps),
          (a = t.memoizedState),
          (l = a.element),
          ls(e, t),
          Wr(t, r, null, n);
        var o = t.memoizedState;
        if (((r = o.element), a.isDehydrated))
          if (
            ((a = {
              element: r,
              isDehydrated: !1,
              cache: o.cache,
              pendingSuspenseBoundaries: o.pendingSuspenseBoundaries,
              transitions: o.transitions,
            }),
            (t.updateQueue.baseState = a),
            (t.memoizedState = a),
            t.flags & 256)
          ) {
            (l = nn(Error(v(423)), t)), (t = Li(e, t, r, n, l));
            break e;
          } else if (r !== l) {
            (l = nn(Error(v(424)), t)), (t = Li(e, t, r, n, l));
            break e;
          } else
            for (
              ge = ot(t.stateNode.containerInfo.firstChild),
                ve = t,
                F = !0,
                je = null,
                n = ns(t, null, r, n),
                t.child = n;
              n;

            )
              (n.flags = (n.flags & -3) | 4096), (n = n.sibling);
        else {
          if ((Zt(), r === l)) {
            t = qe(e, t, n);
            break e;
          }
          oe(e, t, r, n);
        }
        t = t.child;
      }
      return t;
    case 5:
      return (
        as(t),
        e === null && wa(t),
        (r = t.type),
        (l = t.pendingProps),
        (a = e !== null ? e.memoizedProps : null),
        (o = l.children),
        ha(r, l) ? (o = null) : a !== null && ha(r, a) && (t.flags |= 32),
        zs(e, t),
        oe(e, t, o, n),
        t.child
      );
    case 6:
      return e === null && wa(t), null;
    case 13:
      return Ts(e, t, n);
    case 4:
      return (
        fo(t, t.stateNode.containerInfo),
        (r = t.pendingProps),
        e === null ? (t.child = en(t, null, r, n)) : oe(e, t, r, n),
        t.child
      );
    case 11:
      return (
        (r = t.type),
        (l = t.pendingProps),
        (l = t.elementType === r ? l : Le(r, l)),
        Ni(e, t, r, l, n)
      );
    case 7:
      return oe(e, t, t.pendingProps, n), t.child;
    case 8:
      return oe(e, t, t.pendingProps.children, n), t.child;
    case 12:
      return oe(e, t, t.pendingProps.children, n), t.child;
    case 10:
      e: {
        if (
          ((r = t.type._context),
          (l = t.pendingProps),
          (a = t.memoizedProps),
          (o = l.value),
          O(Hr, r._currentValue),
          (r._currentValue = o),
          a !== null)
        )
          if (Ie(a.value, o)) {
            if (a.children === l.children && !de.current) {
              t = qe(e, t, n);
              break e;
            }
          } else
            for (a = t.child, a !== null && (a.return = t); a !== null; ) {
              var u = a.dependencies;
              if (u !== null) {
                o = a.child;
                for (var i = u.firstContext; i !== null; ) {
                  if (i.context === r) {
                    if (a.tag === 1) {
                      (i = Be(-1, n & -n)), (i.tag = 2);
                      var c = a.updateQueue;
                      if (c !== null) {
                        c = c.shared;
                        var m = c.pending;
                        m === null
                          ? (i.next = i)
                          : ((i.next = m.next), (m.next = i)),
                          (c.pending = i);
                      }
                    }
                    (a.lanes |= n),
                      (i = a.alternate),
                      i !== null && (i.lanes |= n),
                      ka(a.return, n, t),
                      (u.lanes |= n);
                    break;
                  }
                  i = i.next;
                }
              } else if (a.tag === 10) o = a.type === t.type ? null : a.child;
              else if (a.tag === 18) {
                if (((o = a.return), o === null)) throw Error(v(341));
                (o.lanes |= n),
                  (u = o.alternate),
                  u !== null && (u.lanes |= n),
                  ka(o, n, t),
                  (o = a.sibling);
              } else o = a.child;
              if (o !== null) o.return = a;
              else
                for (o = a; o !== null; ) {
                  if (o === t) {
                    o = null;
                    break;
                  }
                  if (((a = o.sibling), a !== null)) {
                    (a.return = o.return), (o = a);
                    break;
                  }
                  o = o.return;
                }
              a = o;
            }
        oe(e, t, l.children, n), (t = t.child);
      }
      return t;
    case 9:
      return (
        (l = t.type),
        (r = t.pendingProps.children),
        Yt(t, n),
        (l = Ee(l)),
        (r = r(l)),
        (t.flags |= 1),
        oe(e, t, r, n),
        t.child
      );
    case 14:
      return (
        (r = t.type),
        (l = Le(r, t.pendingProps)),
        (l = Le(r.type, l)),
        Ci(e, t, r, l, n)
      );
    case 15:
      return Ps(e, t, t.type, t.pendingProps, n);
    case 17:
      return (
        (r = t.type),
        (l = t.pendingProps),
        (l = t.elementType === r ? l : Le(r, l)),
        Nr(e, t),
        (t.tag = 1),
        pe(r) ? ((e = !0), Ar(t)) : (e = !1),
        Yt(t, n),
        Es(t, r, l),
        Sa(t, r, l, n),
        Na(null, t, r, !0, e, n)
      );
    case 19:
      return Rs(e, t, n);
    case 22:
      return Ls(e, t, n);
  }
  throw Error(v(156, t.tag));
};
function Ks(e, t) {
  return xu(e, t);
}
function xd(e, t, n, r) {
  (this.tag = e),
    (this.key = n),
    (this.sibling =
      this.child =
      this.return =
      this.stateNode =
      this.type =
      this.elementType =
        null),
    (this.index = 0),
    (this.ref = null),
    (this.pendingProps = t),
    (this.dependencies =
      this.memoizedState =
      this.updateQueue =
      this.memoizedProps =
        null),
    (this.mode = r),
    (this.subtreeFlags = this.flags = 0),
    (this.deletions = null),
    (this.childLanes = this.lanes = 0),
    (this.alternate = null);
}
function Se(e, t, n, r) {
  return new xd(e, t, n, r);
}
function Co(e) {
  return (e = e.prototype), !(!e || !e.isReactComponent);
}
function Sd(e) {
  if (typeof e == 'function') return Co(e) ? 1 : 0;
  if (e != null) {
    if (((e = e.$$typeof), e === Wa)) return 11;
    if (e === Qa) return 14;
  }
  return 2;
}
function ct(e, t) {
  var n = e.alternate;
  return (
    n === null
      ? ((n = Se(e.tag, t, e.key, e.mode)),
        (n.elementType = e.elementType),
        (n.type = e.type),
        (n.stateNode = e.stateNode),
        (n.alternate = e),
        (e.alternate = n))
      : ((n.pendingProps = t),
        (n.type = e.type),
        (n.flags = 0),
        (n.subtreeFlags = 0),
        (n.deletions = null)),
    (n.flags = e.flags & 14680064),
    (n.childLanes = e.childLanes),
    (n.lanes = e.lanes),
    (n.child = e.child),
    (n.memoizedProps = e.memoizedProps),
    (n.memoizedState = e.memoizedState),
    (n.updateQueue = e.updateQueue),
    (t = e.dependencies),
    (n.dependencies =
      t === null ? null : { lanes: t.lanes, firstContext: t.firstContext }),
    (n.sibling = e.sibling),
    (n.index = e.index),
    (n.ref = e.ref),
    n
  );
}
function Lr(e, t, n, r, l, a) {
  var o = 2;
  if (((r = e), typeof e == 'function')) Co(e) && (o = 1);
  else if (typeof e == 'string') o = 5;
  else
    e: switch (e) {
      case It:
        return _t(n.children, l, a, t);
      case Ba:
        (o = 8), (l |= 8);
        break;
      case Xl:
        return (
          (e = Se(12, n, t, l | 2)), (e.elementType = Xl), (e.lanes = a), e
        );
      case ql:
        return (e = Se(13, n, t, l)), (e.elementType = ql), (e.lanes = a), e;
      case Yl:
        return (e = Se(19, n, t, l)), (e.elementType = Yl), (e.lanes = a), e;
      case au:
        return fl(n, l, a, t);
      default:
        if (typeof e == 'object' && e !== null)
          switch (e.$$typeof) {
            case ru:
              o = 10;
              break e;
            case lu:
              o = 9;
              break e;
            case Wa:
              o = 11;
              break e;
            case Qa:
              o = 14;
              break e;
            case Ge:
              (o = 16), (r = null);
              break e;
          }
        throw Error(v(130, e == null ? e : typeof e, ''));
    }
  return (
    (t = Se(o, n, t, l)), (t.elementType = e), (t.type = r), (t.lanes = a), t
  );
}
function _t(e, t, n, r) {
  return (e = Se(7, e, r, t)), (e.lanes = n), e;
}
function fl(e, t, n, r) {
  return (
    (e = Se(22, e, r, t)),
    (e.elementType = au),
    (e.lanes = n),
    (e.stateNode = { isHidden: !1 }),
    e
  );
}
function Hl(e, t, n) {
  return (e = Se(6, e, null, t)), (e.lanes = n), e;
}
function Bl(e, t, n) {
  return (
    (t = Se(4, e.children !== null ? e.children : [], e.key, t)),
    (t.lanes = n),
    (t.stateNode = {
      containerInfo: e.containerInfo,
      pendingChildren: null,
      implementation: e.implementation,
    }),
    t
  );
}
function _d(e, t, n, r, l) {
  (this.tag = t),
    (this.containerInfo = e),
    (this.finishedWork =
      this.pingCache =
      this.current =
      this.pendingChildren =
        null),
    (this.timeoutHandle = -1),
    (this.callbackNode = this.pendingContext = this.context = null),
    (this.callbackPriority = 0),
    (this.eventTimes = _l(0)),
    (this.expirationTimes = _l(-1)),
    (this.entangledLanes =
      this.finishedLanes =
      this.mutableReadLanes =
      this.expiredLanes =
      this.pingedLanes =
      this.suspendedLanes =
      this.pendingLanes =
        0),
    (this.entanglements = _l(0)),
    (this.identifierPrefix = r),
    (this.onRecoverableError = l),
    (this.mutableSourceEagerHydrationData = null);
}
function Po(e, t, n, r, l, a, o, u, i) {
  return (
    (e = new _d(e, t, n, u, i)),
    t === 1 ? ((t = 1), a === !0 && (t |= 8)) : (t = 0),
    (a = Se(3, null, null, t)),
    (e.current = a),
    (a.stateNode = e),
    (a.memoizedState = {
      element: r,
      isDehydrated: n,
      cache: null,
      transitions: null,
      pendingSuspenseBoundaries: null,
    }),
    co(a),
    e
  );
}
function Ed(e, t, n) {
  var r =
    3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
  return {
    $$typeof: Rt,
    key: r == null ? null : '' + r,
    children: e,
    containerInfo: t,
    implementation: n,
  };
}
function Gs(e) {
  if (!e) return dt;
  e = e._reactInternals;
  e: {
    if (jt(e) !== e || e.tag !== 1) throw Error(v(170));
    var t = e;
    do {
      switch (t.tag) {
        case 3:
          t = t.stateNode.context;
          break e;
        case 1:
          if (pe(t.type)) {
            t = t.stateNode.__reactInternalMemoizedMergedChildContext;
            break e;
          }
      }
      t = t.return;
    } while (t !== null);
    throw Error(v(171));
  }
  if (e.tag === 1) {
    var n = e.type;
    if (pe(n)) return Ku(e, n, t);
  }
  return t;
}
function Js(e, t, n, r, l, a, o, u, i) {
  return (
    (e = Po(n, r, !0, e, l, a, o, u, i)),
    (e.context = Gs(null)),
    (n = e.current),
    (r = ie()),
    (l = st(n)),
    (a = Be(r, l)),
    (a.callback = t ?? null),
    it(n, a, l),
    (e.current.lanes = l),
    Yn(e, l, r),
    me(e, r),
    e
  );
}
function dl(e, t, n, r) {
  var l = t.current,
    a = ie(),
    o = st(l);
  return (
    (n = Gs(n)),
    t.context === null ? (t.context = n) : (t.pendingContext = n),
    (t = Be(a, o)),
    (t.payload = { element: e }),
    (r = r === void 0 ? null : r),
    r !== null && (t.callback = r),
    (e = it(l, t, o)),
    e !== null && (Re(e, l, o, a), Sr(e, l, o)),
    o
  );
}
function Zr(e) {
  if (((e = e.current), !e.child)) return null;
  switch (e.child.tag) {
    case 5:
      return e.child.stateNode;
    default:
      return e.child.stateNode;
  }
}
function Ui(e, t) {
  if (((e = e.memoizedState), e !== null && e.dehydrated !== null)) {
    var n = e.retryLane;
    e.retryLane = n !== 0 && n < t ? n : t;
  }
}
function Lo(e, t) {
  Ui(e, t), (e = e.alternate) && Ui(e, t);
}
function Nd() {
  return null;
}
var Zs =
  typeof reportError == 'function'
    ? reportError
    : function (e) {
        console.error(e);
      };
function zo(e) {
  this._internalRoot = e;
}
pl.prototype.render = zo.prototype.render = function (e) {
  var t = this._internalRoot;
  if (t === null) throw Error(v(409));
  dl(e, t, null, null);
};
pl.prototype.unmount = zo.prototype.unmount = function () {
  var e = this._internalRoot;
  if (e !== null) {
    this._internalRoot = null;
    var t = e.containerInfo;
    Lt(function () {
      dl(null, e, null, null);
    }),
      (t[Qe] = null);
  }
};
function pl(e) {
  this._internalRoot = e;
}
pl.prototype.unstable_scheduleHydration = function (e) {
  if (e) {
    var t = Lu();
    e = { blockedOn: null, target: e, priority: t };
    for (var n = 0; n < Ze.length && t !== 0 && t < Ze[n].priority; n++);
    Ze.splice(n, 0, e), n === 0 && ju(e);
  }
};
function jo(e) {
  return !(!e || (e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11));
}
function ml(e) {
  return !(
    !e ||
    (e.nodeType !== 1 &&
      e.nodeType !== 9 &&
      e.nodeType !== 11 &&
      (e.nodeType !== 8 || e.nodeValue !== ' react-mount-point-unstable '))
  );
}
function Ai() {}
function Cd(e, t, n, r, l) {
  if (l) {
    if (typeof r == 'function') {
      var a = r;
      r = function () {
        var c = Zr(o);
        a.call(c);
      };
    }
    var o = Js(t, r, e, 0, null, !1, !1, '', Ai);
    return (
      (e._reactRootContainer = o),
      (e[Qe] = o.current),
      Un(e.nodeType === 8 ? e.parentNode : e),
      Lt(),
      o
    );
  }
  for (; (l = e.lastChild); ) e.removeChild(l);
  if (typeof r == 'function') {
    var u = r;
    r = function () {
      var c = Zr(i);
      u.call(c);
    };
  }
  var i = Po(e, 0, !1, null, null, !1, !1, '', Ai);
  return (
    (e._reactRootContainer = i),
    (e[Qe] = i.current),
    Un(e.nodeType === 8 ? e.parentNode : e),
    Lt(function () {
      dl(t, i, n, r);
    }),
    i
  );
}
function hl(e, t, n, r, l) {
  var a = n._reactRootContainer;
  if (a) {
    var o = a;
    if (typeof l == 'function') {
      var u = l;
      l = function () {
        var i = Zr(o);
        u.call(i);
      };
    }
    dl(t, o, e, l);
  } else o = Cd(n, t, e, l, r);
  return Zr(o);
}
Cu = function (e) {
  switch (e.tag) {
    case 3:
      var t = e.stateNode;
      if (t.current.memoizedState.isDehydrated) {
        var n = wn(t.pendingLanes);
        n !== 0 &&
          (Ya(t, n | 1), me(t, W()), !(R & 6) && ((rn = W() + 500), ht()));
      }
      break;
    case 13:
      Lt(function () {
        var r = Xe(e, 1);
        if (r !== null) {
          var l = ie();
          Re(r, e, 1, l);
        }
      }),
        Lo(e, 1);
  }
};
Ka = function (e) {
  if (e.tag === 13) {
    var t = Xe(e, 134217728);
    if (t !== null) {
      var n = ie();
      Re(t, e, 134217728, n);
    }
    Lo(e, 134217728);
  }
};
Pu = function (e) {
  if (e.tag === 13) {
    var t = st(e),
      n = Xe(e, t);
    if (n !== null) {
      var r = ie();
      Re(n, e, t, r);
    }
    Lo(e, t);
  }
};
Lu = function () {
  return I;
};
zu = function (e, t) {
  var n = I;
  try {
    return (I = e), t();
  } finally {
    I = n;
  }
};
aa = function (e, t, n) {
  switch (t) {
    case 'input':
      if ((Jl(e, n), (t = n.name), n.type === 'radio' && t != null)) {
        for (n = e; n.parentNode; ) n = n.parentNode;
        for (
          n = n.querySelectorAll(
            'input[name=' + JSON.stringify('' + t) + '][type="radio"]'
          ),
            t = 0;
          t < n.length;
          t++
        ) {
          var r = n[t];
          if (r !== e && r.form === e.form) {
            var l = al(r);
            if (!l) throw Error(v(90));
            iu(r), Jl(r, l);
          }
        }
      }
      break;
    case 'textarea':
      su(e, n);
      break;
    case 'select':
      (t = n.value), t != null && Wt(e, !!n.multiple, t, !1);
  }
};
gu = _o;
vu = Lt;
var Pd = { usingClientEntryPoint: !1, Events: [Gn, Ft, al, mu, hu, _o] },
  vn = {
    findFiberByHostInstance: wt,
    bundleType: 0,
    version: '18.3.1',
    rendererPackageName: 'react-dom',
  },
  Ld = {
    bundleType: vn.bundleType,
    version: vn.version,
    rendererPackageName: vn.rendererPackageName,
    rendererConfig: vn.rendererConfig,
    overrideHookState: null,
    overrideHookStateDeletePath: null,
    overrideHookStateRenamePath: null,
    overrideProps: null,
    overridePropsDeletePath: null,
    overridePropsRenamePath: null,
    setErrorHandler: null,
    setSuspenseHandler: null,
    scheduleUpdate: null,
    currentDispatcherRef: Ye.ReactCurrentDispatcher,
    findHostInstanceByFiber: function (e) {
      return (e = wu(e)), e === null ? null : e.stateNode;
    },
    findFiberByHostInstance: vn.findFiberByHostInstance || Nd,
    findHostInstancesForRefresh: null,
    scheduleRefresh: null,
    scheduleRoot: null,
    setRefreshHandler: null,
    getCurrentFiber: null,
    reconcilerVersion: '18.3.1-next-f1338f8080-20240426',
  };
if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < 'u') {
  var vr = __REACT_DEVTOOLS_GLOBAL_HOOK__;
  if (!vr.isDisabled && vr.supportsFiber)
    try {
      (tl = vr.inject(Ld)), (Fe = vr);
    } catch {}
}
be.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = Pd;
be.createPortal = function (e, t) {
  var n =
    2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
  if (!jo(t)) throw Error(v(200));
  return Ed(e, t, null, n);
};
be.createRoot = function (e, t) {
  if (!jo(e)) throw Error(v(299));
  var n = !1,
    r = '',
    l = Zs;
  return (
    t != null &&
      (t.unstable_strictMode === !0 && (n = !0),
      t.identifierPrefix !== void 0 && (r = t.identifierPrefix),
      t.onRecoverableError !== void 0 && (l = t.onRecoverableError)),
    (t = Po(e, 1, !1, null, null, n, !1, r, l)),
    (e[Qe] = t.current),
    Un(e.nodeType === 8 ? e.parentNode : e),
    new zo(t)
  );
};
be.findDOMNode = function (e) {
  if (e == null) return null;
  if (e.nodeType === 1) return e;
  var t = e._reactInternals;
  if (t === void 0)
    throw typeof e.render == 'function'
      ? Error(v(188))
      : ((e = Object.keys(e).join(',')), Error(v(268, e)));
  return (e = wu(t)), (e = e === null ? null : e.stateNode), e;
};
be.flushSync = function (e) {
  return Lt(e);
};
be.hydrate = function (e, t, n) {
  if (!ml(t)) throw Error(v(200));
  return hl(null, e, t, !0, n);
};
be.hydrateRoot = function (e, t, n) {
  if (!jo(e)) throw Error(v(405));
  var r = (n != null && n.hydratedSources) || null,
    l = !1,
    a = '',
    o = Zs;
  if (
    (n != null &&
      (n.unstable_strictMode === !0 && (l = !0),
      n.identifierPrefix !== void 0 && (a = n.identifierPrefix),
      n.onRecoverableError !== void 0 && (o = n.onRecoverableError)),
    (t = Js(t, null, e, 1, n ?? null, l, !1, a, o)),
    (e[Qe] = t.current),
    Un(e),
    r)
  )
    for (e = 0; e < r.length; e++)
      (n = r[e]),
        (l = n._getVersion),
        (l = l(n._source)),
        t.mutableSourceEagerHydrationData == null
          ? (t.mutableSourceEagerHydrationData = [n, l])
          : t.mutableSourceEagerHydrationData.push(n, l);
  return new pl(t);
};
be.render = function (e, t, n) {
  if (!ml(t)) throw Error(v(200));
  return hl(null, e, t, !1, n);
};
be.unmountComponentAtNode = function (e) {
  if (!ml(e)) throw Error(v(40));
  return e._reactRootContainer
    ? (Lt(function () {
        hl(null, null, e, !1, function () {
          (e._reactRootContainer = null), (e[Qe] = null);
        });
      }),
      !0)
    : !1;
};
be.unstable_batchedUpdates = _o;
be.unstable_renderSubtreeIntoContainer = function (e, t, n, r) {
  if (!ml(n)) throw Error(v(200));
  if (e == null || e._reactInternals === void 0) throw Error(v(38));
  return hl(e, t, n, !1, r);
};
be.version = '18.3.1-next-f1338f8080-20240426';
function ec() {
  if (
    !(
      typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > 'u' ||
      typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != 'function'
    )
  )
    try {
      __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(ec);
    } catch (e) {
      console.error(e);
    }
}
ec(), (Zi.exports = be);
var zd = Zi.exports,
  Vi = zd;
(Wl.createRoot = Vi.createRoot), (Wl.hydrateRoot = Vi.hydrateRoot);
const jd = ({ devices: e, setActiveView: t }) => {
    const [n, r] = Z.useState(''),
      l = (i) => {
        const c = (i == null ? void 0 : i.toUpperCase()) || '';
        return c.startsWith('MR')
          ? 'mdi:wifi'
          : c.startsWith('MS')
          ? 'mdi:lan'
          : c.startsWith('MV')
          ? 'mdi:cctv'
          : c.startsWith('MX')
          ? 'mdi:shield-check'
          : c.startsWith('MG')
          ? 'mdi:signal-cellular-outline'
          : c.startsWith('MT')
          ? 'mdi:thermometer'
          : c.startsWith('Z')
          ? 'mdi:router-wireless'
          : 'mdi:help-circle';
      },
      a = e.filter((i) => {
        var c, m;
        return (
          ((c = i.name) == null
            ? void 0
            : c.toLowerCase().includes(n.toLowerCase())) ||
          ((m = i.serial) == null
            ? void 0
            : m.toLowerCase().includes(n.toLowerCase()))
        );
      }),
      o = (i, c) => {
        i.preventDefault(), i.stopPropagation();
        const m = new CustomEvent('hass-more-info', {
          bubbles: !0,
          composed: !0,
          detail: { entityId: c },
        });
        i.currentTarget.dispatchEvent(m);
      },
      u = (i, c) => {
        i.preventDefault(),
          i.stopPropagation(),
          t({ view: 'device', deviceId: c });
      };
    return g.jsxs('div', {
      className: 'bg-light-card dark:bg-dark-card p-4 rounded-lg shadow-md',
      children: [
        g.jsx('input', {
          type: 'text',
          placeholder: 'Search by name or serial...',
          className:
            'w-full p-2 mb-4 border rounded-lg bg-light-background dark:bg-dark-background dark:border-gray-600',
          value: n,
          onChange: (i) => r(i.target.value),
        }),
        g.jsx('div', {
          className: 'overflow-x-auto',
          children: g.jsxs('table', {
            className: 'min-w-full',
            children: [
              g.jsx('thead', {
                children: g.jsxs('tr', {
                  className:
                    'border-b border-light-border dark:border-dark-border',
                  children: [
                    g.jsx('th', {
                      className: 'text-left p-4 font-semibold',
                      children: 'Name',
                    }),
                    g.jsx('th', {
                      className: 'text-left p-4 font-semibold',
                      children: 'Model',
                    }),
                    g.jsx('th', {
                      className: 'text-left p-4 font-semibold',
                      children: 'Status',
                    }),
                    g.jsx('th', {
                      className: 'text-left p-4 font-semibold',
                      children: 'RTSP',
                    }),
                    g.jsx('th', {
                      className: 'text-center p-4 font-semibold w-16',
                      children: 'Details',
                    }),
                  ],
                }),
              }),
              g.jsx('tbody', {
                children: a.map((i) => {
                  var c;
                  const m =
                    (c = i.model) != null && c.startsWith('MV') && i.lanIp
                      ? `rtsp://${i.lanIp}:9000/live`
                      : null;
                  return g.jsxs(
                    'tr',
                    {
                      className:
                        'border-b border-light-border dark:border-dark-border hover:bg-light-hover dark:hover:bg-dark-hover cursor-pointer',
                      onClick: (h) => {
                        i.entity_id ? o(h, i.entity_id) : u(h, i.serial);
                      },
                      children: [
                        g.jsx('td', {
                          className: 'p-4',
                          children: g.jsxs('div', {
                            style: { display: 'flex', alignItems: 'center' },
                            children: [
                              g.jsx('ha-icon', {
                                icon: l(i.model),
                                style: { marginRight: '8px' },
                              }),
                              g.jsx('span', {
                                className: 'font-medium',
                                children: i.name || 'N/A',
                              }),
                            ],
                          }),
                        }),
                        g.jsx('td', {
                          className: 'p-4',
                          children: i.model || 'N/A',
                        }),
                        g.jsx('td', {
                          className: 'p-4 capitalize',
                          children: i.status || 'N/A',
                        }),
                        g.jsx('td', {
                          className: 'p-4',
                          children: m
                            ? g.jsx('a', {
                                href: m,
                                className:
                                  'text-blue-500 hover:text-blue-700 underline',
                                onClick: (h) => h.stopPropagation(),
                                children: 'Stream Link',
                              })
                            : g.jsx('span', {
                                className: 'text-gray-400',
                                children: '-',
                              }),
                        }),
                        g.jsx('td', {
                          className: 'p-4 text-center',
                          children: g.jsx('button', {
                            onClick: (h) => u(h, i.serial),
                            className:
                              'p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-500 transition-colors',
                            title: 'View Details',
                            children: g.jsx('ha-icon', {
                              icon: 'mdi:information-outline',
                            }),
                          }),
                        }),
                      ],
                    },
                    i.serial
                  );
                }),
              }),
            ],
          }),
        }),
      ],
    });
  },
  Td = ({ ssids: e }) =>
    !e || e.length === 0
      ? null
      : g.jsx('div', {
          style: {
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
            gap: '16px',
            padding: '16px',
          },
          children: e.map((t) =>
            g.jsx(
              'ha-card',
              {
                children: g.jsxs('div', {
                  className: 'card-content',
                  style: {
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '8px',
                  },
                  children: [
                    g.jsxs('div', {
                      style: {
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                      },
                      children: [
                        g.jsx('span', {
                          style: { fontWeight: 'bold' },
                          children: t.name,
                        }),
                        g.jsx('ha-icon', {
                          icon: t.enabled ? 'mdi:wifi' : 'mdi:wifi-off',
                          style: {
                            color: t.enabled
                              ? 'var(--primary-color)'
                              : 'var(--disabled-text-color)',
                          },
                        }),
                      ],
                    }),
                    g.jsx('span', {
                      children: t.enabled ? 'Enabled' : 'Disabled',
                    }),
                  ],
                }),
              },
              t.number
            )
          ),
        }),
  Rd = ({ networkId: e }) => {
    const [t, n] = Z.useState([]),
      [r, l] = Z.useState(!1),
      [a, o] = Z.useState(null);
    return (
      Z.useEffect(() => {
        (async () => {
          var u;
          if (e) {
            l(!0), o(null);
            try {
              if (window.location.hostname === 'localhost') {
                n([
                  {
                    occurredAt: new Date().toISOString(),
                    type: 'client_connect',
                    description: 'Client connected',
                    clientDescription: 'iPhone',
                  },
                  {
                    occurredAt: new Date(Date.now() - 36e5).toISOString(),
                    type: 'device_online',
                    description: 'Device came online',
                    deviceName: 'Living Room AP',
                  },
                ]),
                  l(!1);
                return;
              }
              const i =
                ((u = document.querySelector('meraki-panel')) == null
                  ? void 0
                  : u.hass) || window.hass;
              if (!i) throw new Error('Hass connection not available');
              const c = window.CONFIG_ENTRY_ID,
                m = await i.connection.sendMessagePromise({
                  type: 'meraki_ha/get_network_events',
                  config_entry_id: c,
                  network_id: e,
                  per_page: 10,
                });
              m && m.events ? n(m.events) : n([]);
            } catch (i) {
              console.error('Error fetching events:', i),
                o(i.message || 'Failed to fetch events');
            } finally {
              l(!1);
            }
          }
        })();
      }, [e]),
      e
        ? g.jsxs('div', {
            className: 'mt-4',
            children: [
              g.jsx('h3', {
                className: 'text-lg font-semibold mb-2',
                children: 'Recent Events',
              }),
              r && g.jsx('p', { children: 'Loading events...' }),
              a &&
                g.jsxs('p', {
                  className: 'text-red-500',
                  children: ['Error: ', a],
                }),
              !r &&
                !a &&
                t.length === 0 &&
                g.jsx('p', { children: 'No events found.' }),
              !r &&
                !a &&
                t.length > 0 &&
                g.jsx('div', {
                  className:
                    'overflow-x-auto bg-light-card dark:bg-dark-card rounded-lg shadow-md',
                  children: g.jsxs('table', {
                    className: 'min-w-full text-sm',
                    children: [
                      g.jsx('thead', {
                        children: g.jsxs('tr', {
                          className:
                            'border-b border-light-border dark:border-dark-border bg-gray-50 dark:bg-gray-800',
                          children: [
                            g.jsx('th', {
                              className: 'text-left p-3 font-medium',
                              children: 'Time',
                            }),
                            g.jsx('th', {
                              className: 'text-left p-3 font-medium',
                              children: 'Type',
                            }),
                            g.jsx('th', {
                              className: 'text-left p-3 font-medium',
                              children: 'Description',
                            }),
                            g.jsx('th', {
                              className: 'text-left p-3 font-medium',
                              children: 'Source',
                            }),
                          ],
                        }),
                      }),
                      g.jsx('tbody', {
                        children: t.map((u, i) =>
                          g.jsxs(
                            'tr',
                            {
                              className:
                                'border-b border-light-border dark:border-dark-border hover:bg-gray-50 dark:hover:bg-gray-700',
                              children: [
                                g.jsx('td', {
                                  className: 'p-3 whitespace-nowrap',
                                  children: new Date(
                                    u.occurredAt
                                  ).toLocaleString(),
                                }),
                                g.jsx('td', {
                                  className: 'p-3',
                                  children: u.type,
                                }),
                                g.jsx('td', {
                                  className: 'p-3',
                                  children: u.description,
                                }),
                                g.jsx('td', {
                                  className: 'p-3',
                                  children:
                                    u.clientDescription ||
                                    u.deviceName ||
                                    u.clientId ||
                                    u.deviceSerial ||
                                    '-',
                                }),
                              ],
                            },
                            i
                          )
                        ),
                      }),
                    ],
                  }),
                }),
            ],
          })
        : g.jsx('div', {
            className: 'p-4 text-gray-500',
            children: 'Select a network to view events.',
          })
    );
  },
  Id = ({ data: e, onToggle: t, setActiveView: n }) => {
    const [r, l] = Z.useState(null),
      a = (i) => {
        l(r === i ? null : i);
      },
      { networks: o, devices: u } = e;
    return !o || o.length === 0
      ? g.jsx('p', { children: 'No networks found.' })
      : g.jsx('div', {
          style: { display: 'flex', flexDirection: 'column', gap: '16px' },
          children: o.map((i) => {
            const c = r === i.id,
              m = i.ssids ? i.ssids.filter((p) => p.enabled).length : 0,
              h = i.ssids ? i.ssids.length : 0;
            return g.jsxs(
              'ha-card',
              {
                children: [
                  g.jsxs('div', {
                    className: 'card-header',
                    onClick: () => a(i.id),
                    style: {
                      display: 'flex',
                      alignItems: 'center',
                      cursor: 'pointer',
                      padding: '16px',
                    },
                    children: [
                      g.jsxs('span', { children: ['[Network] ', i.name] }),
                      g.jsx('ha-icon', {
                        style: { marginLeft: '8px' },
                        icon: c ? 'mdi:chevron-up' : 'mdi:chevron-down',
                      }),
                      g.jsxs('div', {
                        style: {
                          marginLeft: 'auto',
                          display: 'flex',
                          alignItems: 'center',
                        },
                        children: [
                          g.jsx('span', {
                            style: { marginRight: '8px' },
                            children: 'Track in',
                          }),
                          g.jsx('ha-icon', {
                            icon: 'hass:home-assistant',
                            style: {
                              color: 'var(--primary-color)',
                              marginRight: '8px',
                            },
                          }),
                          g.jsx('ha-switch', {
                            checked: i.is_enabled,
                            onchange: (p) => t(i.id, p.target.checked),
                          }),
                        ],
                      }),
                    ],
                  }),
                  c &&
                    i.is_enabled &&
                    g.jsxs('div', {
                      className: 'card-content',
                      children: [
                        g.jsx(jd, {
                          devices: u.filter((p) => p.networkId === i.id),
                          setActiveView: n,
                        }),
                        i.ssids &&
                          i.ssids.length > 0 &&
                          g.jsxs(g.Fragment, {
                            children: [
                              g.jsxs('div', {
                                className: 'hero-indicator',
                                style: { padding: '0 16px 16px' },
                                children: [
                                  g.jsx('ha-icon', { icon: 'mdi:wifi' }),
                                  m,
                                  ' / ',
                                  h,
                                  ' SSIDs Enabled',
                                ],
                              }),
                              g.jsx(Td, { ssids: i.ssids }),
                            ],
                          }),
                        g.jsx(Rd, { networkId: i.id }),
                      ],
                    }),
                ],
              },
              i.id
            );
          }),
        });
  },
  Od = ({ activeView: e, setActiveView: t, data: n }) => {
    const r = n.devices.find((h) => h.serial === e.deviceId);
    if (!r)
      return g.jsxs('div', {
        children: [
          g.jsx('button', {
            onClick: () => t({ view: 'dashboard' }),
            className: 'text-blue-500 mb-4',
            children: '← Back to Dashboard',
          }),
          g.jsx('p', { children: 'Device not found.' }),
        ],
      });
    const {
      name: l,
      model: a,
      serial: o,
      firmware: u,
      status: i,
      status_messages: c = [],
      entities: m = [],
    } = r;
    return g.jsxs('div', {
      children: [
        g.jsx('button', {
          onClick: () => t({ view: 'dashboard' }),
          className: 'text-blue-500 mb-4 hover:underline',
          children: '← Back to Dashboard',
        }),
        g.jsxs('div', {
          className:
            'bg-light-card dark:bg-dark-card p-6 rounded-lg shadow-md mb-8',
          children: [
            g.jsx('h2', { className: 'text-2xl font-bold mb-2', children: l }),
            g.jsxs('div', {
              className: 'grid grid-cols-1 md:grid-cols-3 gap-4 text-sm',
              children: [
                g.jsxs('div', {
                  children: [g.jsx('strong', { children: 'Model:' }), ' ', a],
                }),
                g.jsxs('div', {
                  children: [g.jsx('strong', { children: 'Serial:' }), ' ', o],
                }),
                g.jsxs('div', {
                  children: [
                    g.jsx('strong', { children: 'Firmware:' }),
                    ' ',
                    u,
                  ],
                }),
                g.jsxs('div', {
                  children: [
                    g.jsx('strong', { children: 'Status:' }),
                    ' ',
                    g.jsx('span', { className: 'capitalize', children: i }),
                  ],
                }),
              ],
            }),
          ],
        }),
        c.length > 0 &&
          g.jsxs('div', {
            className: 'mb-8',
            children: [
              g.jsx('h3', {
                className: 'text-xl font-semibold mb-2',
                children: 'Status Messages',
              }),
              g.jsx('div', {
                className:
                  'bg-yellow-100 dark:bg-yellow-900 border-l-4 border-yellow-500 text-yellow-700 dark:text-yellow-200 p-4 rounded-lg',
                children: g.jsx('ul', {
                  children: c.map((h, p) =>
                    g.jsx('li', { className: 'mb-1', children: h }, p)
                  ),
                }),
              }),
            ],
          }),
        g.jsxs('div', {
          children: [
            g.jsx('h3', {
              className: 'text-xl font-semibold mb-4',
              children: 'Entities',
            }),
            g.jsx('div', {
              className:
                'overflow-x-auto bg-light-card dark:bg-dark-card p-4 rounded-lg shadow-md',
              children: g.jsxs('table', {
                className: 'min-w-full',
                children: [
                  g.jsx('thead', {
                    children: g.jsxs('tr', {
                      className:
                        'border-b border-light-border dark:border-dark-border',
                      children: [
                        g.jsx('th', {
                          className: 'text-left p-4 font-semibold',
                          children: 'Name',
                        }),
                        g.jsx('th', {
                          className: 'text-left p-4 font-semibold',
                          children: 'Entity ID',
                        }),
                        g.jsx('th', {
                          className: 'text-left p-4 font-semibold',
                          children: 'State',
                        }),
                      ],
                    }),
                  }),
                  g.jsx('tbody', {
                    children: m.map((h) =>
                      g.jsxs(
                        'tr',
                        {
                          className:
                            'border-b border-light-border dark:border-dark-border last:border-b-0',
                          children: [
                            g.jsx('td', {
                              className: 'p-4',
                              children: h.name,
                            }),
                            g.jsx('td', {
                              className: 'p-4',
                              children: h.entity_id,
                            }),
                            g.jsx('td', {
                              className: 'p-4',
                              children: h.state,
                            }),
                          ],
                        },
                        h.entity_id
                      )
                    ),
                  }),
                ],
              }),
            }),
          ],
        }),
      ],
    });
  },
  Dd = ({ options: e, configEntryId: t, onClose: n }) => {
    const [r, l] = Z.useState(e),
      [a, o] = Z.useState(!1),
      u = (m) => {
        l((h) => ({ ...h, [m]: !h[m] }));
      },
      i = async () => {
        o(!0);
        try {
          const m = window.hass;
          m && m.connection
            ? await m.connection.sendMessagePromise({
                type: 'meraki_ha/update_options',
                config_entry_id: t,
                options: r,
              })
            : console.log('Saving options:', r);
        } catch (m) {
          console.error('Failed to save options:', m),
            alert('Failed to save settings.');
        } finally {
          o(!1), n(), window.location.reload();
        }
      },
      c = [
        {
          key: 'enable_device_status',
          label: 'Device & Entity Model',
          description: 'Enable basic device status and entity modeling.',
        },
        {
          key: 'enable_org_sensors',
          label: 'Organization-Wide Sensors',
          description:
            'Enable sensors that aggregate data across the entire organization.',
        },
        {
          key: 'enable_camera_entities',
          label: 'Camera Entities & Sensors',
          description:
            'Enable cameras and their associated sensors (motion, analytics).',
        },
        {
          key: 'enable_device_sensors',
          label: 'Physical Device Sensors',
          description:
            'Enable sensors for physical device metrics (e.g. MT sensors).',
        },
        {
          key: 'enable_network_sensors',
          label: 'Network Sensors',
          description: 'Enable network-level sensors and switches.',
        },
        {
          key: 'enable_vlan_sensors',
          label: 'VLAN Sensors',
          description: 'Enable VLAN status monitoring.',
        },
        {
          key: 'enable_port_sensors',
          label: 'Appliance Port Sensors',
          description:
            'Enable sensors for switch ports and appliance uplinks.',
        },
        {
          key: 'enable_ssid_sensors',
          label: 'SSID Sensors',
          description: 'Enable sensors and switches for SSIDs.',
        },
      ];
    return g.jsx('div', {
      className:
        'fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center z-50',
      children: g.jsxs('ha-card', {
        class:
          'p-6 w-full max-w-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 shadow-lg rounded-lg',
        children: [
          g.jsxs('div', {
            className: 'card-header flex justify-between items-center mb-4',
            children: [
              g.jsx('h2', {
                className: 'text-xl font-bold',
                children: 'Integration Settings',
              }),
              g.jsx('button', {
                onClick: n,
                className: 'text-gray-500 hover:text-gray-700',
                children: g.jsx('ha-icon', { icon: 'mdi:close' }),
              }),
            ],
          }),
          g.jsx('div', {
            className: 'card-content space-y-4 max-h-96 overflow-y-auto',
            children: c.map((m) =>
              g.jsxs(
                'div',
                {
                  className:
                    'flex items-center justify-between p-2 border-b border-gray-200 dark:border-gray-700',
                  children: [
                    g.jsxs('div', {
                      className: 'flex flex-col',
                      children: [
                        g.jsx('span', {
                          className: 'font-medium',
                          children: m.label,
                        }),
                        g.jsx('span', {
                          className:
                            'text-sm text-gray-500 dark:text-gray-400',
                          children: m.description,
                        }),
                      ],
                    }),
                    g.jsx('ha-switch', {
                      checked: r[m.key] !== !1,
                      onClick: (h) => {
                        h.stopPropagation(), u(m.key);
                      },
                    }),
                  ],
                },
                m.key
              )
            ),
          }),
          g.jsxs('div', {
            className: 'card-actions flex justify-end mt-6 gap-4',
            children: [
              g.jsx('button', {
                onClick: n,
                className:
                  'px-4 py-2 rounded border border-gray-300 text-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700',
                disabled: a,
                children: 'Cancel',
              }),
              g.jsx('button', {
                onClick: i,
                className:
                  'px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50',
                disabled: a,
                children: a ? 'Saving...' : 'Save & Reload',
              }),
            ],
          }),
        ],
      }),
    });
  },
  Md = () => {
    const [e, t] = Z.useState(null),
      [n, r] = Z.useState(!0),
      [l, a] = Z.useState(null),
      [o, u] = Z.useState({ view: 'dashboard', deviceId: void 0 }),
      [i, c] = Z.useState(!1),
      m = () => {
        if (window.location.hostname === 'localhost') {
          t({
            networks: [
              {
                id: 'N_12345',
                name: 'Main Office',
                is_enabled: !0,
                ssids: [],
              },
            ],
            devices: [
              {
                name: 'Living Room AP',
                model: 'MR33',
                serial: 'Q2JD-XXXX-XXXX',
                status: 'online',
                entity_id: 'switch.living_room_ap',
                networkId: 'N_12345',
              },
              {
                name: 'Office Switch',
                model: 'MS220-8P',
                serial: 'Q2HD-XXXX-XXXX',
                status: 'online',
                entity_id: 'switch.office_switch',
                networkId: 'N_12345',
              },
              {
                name: 'Front Door Camera',
                model: 'MV12',
                serial: 'Q2FD-XXXX-XXXX',
                status: 'online',
                lanIp: '192.168.1.100',
                entity_id: 'camera.front_door_camera',
                networkId: 'N_12345',
              },
            ],
            ssids: [],
            options: {
              enable_device_status: !0,
              enable_org_sensors: !0,
              enable_camera_entities: !0,
              enable_device_sensors: !0,
              enable_network_sensors: !0,
              enable_vlan_sensors: !0,
              enable_port_sensors: !0,
              enable_ssid_sensors: !0,
            },
          }),
            r(!1);
          return;
        }
        let p = localStorage.getItem('meraki_ha_llat');
        if (!p) {
          const T = window.hass;
          T && T.auth && T.auth.accessToken && (p = T.auth.accessToken);
        }
        if (!p)
          if (
            ((p = prompt(
              'Please enter your Home Assistant Long-Lived Access Token:'
            )),
            p)
          )
            localStorage.setItem('meraki_ha_llat', p);
          else {
            a('No access token provided.'), r(!1);
            return;
          }
        const w = `${
            window.HA_URL
              ? window.HA_URL.replace(/^http/, 'ws')
              : window.location.protocol === 'https:'
              ? 'wss://' + window.location.host
              : 'ws://' + window.location.host
          }/api/websocket`,
          b = new WebSocket(w);
        let k = 1;
        return (
          (b.onopen = () => {
            console.log('WebSocket connection established'),
              b.send(JSON.stringify({ type: 'auth', access_token: p }));
          }),
          (b.onmessage = (T) => {
            var d, s;
            const f = JSON.parse(T.data);
            f.type === 'auth_ok'
              ? (console.log('Authenticated successfully'),
                b.send(
                  JSON.stringify({
                    id: k,
                    type: 'meraki_ha/get_config',
                    config_entry_id: window.CONFIG_ENTRY_ID,
                  })
                ))
              : f.type === 'auth_invalid'
              ? (console.error('Authentication failed:', f.message),
                a('Authentication failed. Please check your token.'),
                r(!1),
                localStorage.removeItem('meraki_ha_llat'))
              : f.id === k &&
                (f.type === 'result'
                  ? (f.success
                      ? t(f.result)
                      : (console.error(
                          'Failed to fetch Meraki data:',
                          f.error
                        ),
                        a(
                          `Failed to fetch Meraki data: ${
                            (d = f.error) == null ? void 0 : d.message
                          }`
                        )),
                    r(!1))
                  : f.type === 'result' &&
                    f.success === !1 &&
                    (console.error('Failed to fetch Meraki data:', f.error),
                    a(
                      `Failed to fetch Meraki data: ${
                        (s = f.error) == null ? void 0 : s.message
                      }`
                    ),
                    r(!1)));
          }),
          (b.onerror = (T) => {
            console.error('WebSocket error:', T);
          }),
          () => {
            b.readyState === 1 && b.close();
          }
        );
      };
    if (
      (Z.useEffect(() => {
        m();
      }, []),
      n)
    )
      return g.jsx('div', { className: 'p-4', children: 'Loading...' });
    if (l)
      return g.jsxs('div', {
        className: 'p-4 text-red-500',
        children: ['Error: ', l],
      });
    const h = (p, w) => {
      console.log(`Toggled network ${p} to ${w}`);
    };
    return g.jsxs('div', {
      className: 'p-4 relative',
      children: [
        g.jsxs('div', {
          className: 'flex justify-between items-center mb-4',
          children: [
            g.jsx('h1', {
              className: 'text-2xl font-bold',
              children: 'Meraki HA Web UI',
            }),
            g.jsx('button', {
              onClick: () => c(!0),
              className:
                'p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700',
              title: 'Settings',
              children: g.jsx('ha-icon', { icon: 'mdi:cog' }),
            }),
          ],
        }),
        o.view === 'dashboard'
          ? g.jsx(Id, { data: e, onToggle: h, setActiveView: u })
          : g.jsx(Od, { activeView: o, setActiveView: u, data: e }),
        i &&
          e &&
          g.jsx(Dd, {
            options: e.options || {},
            configEntryId: window.CONFIG_ENTRY_ID || e.config_entry_id,
            onClose: () => c(!1),
          }),
      ],
    });
  };
Wl.createRoot(document.getElementById('root')).render(
  g.jsx(yc.StrictMode, { children: g.jsx(Md, {}) })
);
