(function () {
  const t = document.createElement('link').relList;
  if (t && t.supports && t.supports('modulepreload')) return;
  for (const a of document.querySelectorAll('link[rel="modulepreload"]')) r(a);
  new MutationObserver((a) => {
    for (const l of a)
      if (l.type === 'childList')
        for (const o of l.addedNodes)
          o.tagName === 'LINK' && o.rel === 'modulepreload' && r(o);
  }).observe(document, { childList: !0, subtree: !0 });
  function n(a) {
    const l = {};
    return (
      a.integrity && (l.integrity = a.integrity),
      a.referrerPolicy && (l.referrerPolicy = a.referrerPolicy),
      a.crossOrigin === 'use-credentials'
        ? (l.credentials = 'include')
        : a.crossOrigin === 'anonymous'
        ? (l.credentials = 'omit')
        : (l.credentials = 'same-origin'),
      l
    );
  }
  function r(a) {
    if (a.ep) return;
    a.ep = !0;
    const l = n(a);
    fetch(a.href, l);
  }
})();
(function () {
  const e = document.createElement('link').relList;
  if (e && e.supports && e.supports('modulepreload')) return;
  for (const r of document.querySelectorAll('link[rel="modulepreload"]')) n(r);
  new MutationObserver((r) => {
    for (const a of r)
      if (a.type === 'childList')
        for (const l of a.addedNodes)
          l.tagName === 'LINK' && l.rel === 'modulepreload' && n(l);
  }).observe(document, { childList: !0, subtree: !0 });
  function t(r) {
    const a = {};
    return (
      r.integrity && (a.integrity = r.integrity),
      r.referrerPolicy && (a.referrerPolicy = r.referrerPolicy),
      r.crossOrigin === 'use-credentials'
        ? (a.credentials = 'include')
        : r.crossOrigin === 'anonymous'
        ? (a.credentials = 'omit')
        : (a.credentials = 'same-origin'),
      a
    );
  }
  function n(r) {
    if (r.ep) return;
    r.ep = !0;
    const a = t(r);
    fetch(r.href, a);
  }
})();
(function () {
  const e = document.createElement('link').relList;
  if (e && e.supports && e.supports('modulepreload')) return;
  for (const r of document.querySelectorAll('link[rel="modulepreload"]')) n(r);
  new MutationObserver((r) => {
    for (const a of r)
      if (a.type === 'childList')
        for (const l of a.addedNodes)
          l.tagName === 'LINK' && l.rel === 'modulepreload' && n(l);
  }).observe(document, { childList: !0, subtree: !0 });
  function t(r) {
    const a = {};
    return (
      r.integrity && (a.integrity = r.integrity),
      r.referrerPolicy && (a.referrerPolicy = r.referrerPolicy),
      r.crossOrigin === 'use-credentials'
        ? (a.credentials = 'include')
        : r.crossOrigin === 'anonymous'
        ? (a.credentials = 'omit')
        : (a.credentials = 'same-origin'),
      a
    );
  }
  function n(r) {
    if (r.ep) return;
    r.ep = !0;
    const a = t(r);
    fetch(r.href, a);
  }
})();
(function () {
  const e = document.createElement('link').relList;
  if (e && e.supports && e.supports('modulepreload')) return;
  for (const r of document.querySelectorAll('link[rel="modulepreload"]')) n(r);
  new MutationObserver((r) => {
    for (const a of r)
      if (a.type === 'childList')
        for (const l of a.addedNodes)
          l.tagName === 'LINK' && l.rel === 'modulepreload' && n(l);
  }).observe(document, { childList: !0, subtree: !0 });
  function t(r) {
    const a = {};
    return (
      r.integrity && (a.integrity = r.integrity),
      r.referrerPolicy && (a.referrerPolicy = r.referrerPolicy),
      r.crossOrigin === 'use-credentials'
        ? (a.credentials = 'include')
        : r.crossOrigin === 'anonymous'
        ? (a.credentials = 'omit')
        : (a.credentials = 'same-origin'),
      a
    );
  }
  function n(r) {
    if (r.ep) return;
    r.ep = !0;
    const a = t(r);
    fetch(r.href, a);
  }
})();
(function () {
  const e = document.createElement('link').relList;
  if (e && e.supports && e.supports('modulepreload')) return;
  for (const r of document.querySelectorAll('link[rel="modulepreload"]')) n(r);
  new MutationObserver((r) => {
    for (const a of r)
      if (a.type === 'childList')
        for (const l of a.addedNodes)
          l.tagName === 'LINK' && l.rel === 'modulepreload' && n(l);
  }).observe(document, { childList: !0, subtree: !0 });
  function t(r) {
    const a = {};
    return (
      r.integrity && (a.integrity = r.integrity),
      r.referrerPolicy && (a.referrerPolicy = r.referrerPolicy),
      r.crossOrigin === 'use-credentials'
        ? (a.credentials = 'include')
        : r.crossOrigin === 'anonymous'
        ? (a.credentials = 'omit')
        : (a.credentials = 'same-origin'),
      a
    );
  }
  function n(r) {
    if (r.ep) return;
    r.ep = !0;
    const a = t(r);
    fetch(r.href, a);
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
  ea = {},
  Hi = { exports: {} },
  L = {};
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
  ac = Symbol.for('react.fragment'),
  lc = Symbol.for('react.strict_mode'),
  oc = Symbol.for('react.profiler'),
  ic = Symbol.for('react.provider'),
  uc = Symbol.for('react.context'),
  sc = Symbol.for('react.forward_ref'),
  cc = Symbol.for('react.suspense'),
  dc = Symbol.for('react.memo'),
  fc = Symbol.for('react.lazy'),
  To = Symbol.iterator;
function pc(e) {
  return e === null || typeof e != 'object'
    ? null
    : ((e = (To && e[To]) || e['@@iterator']),
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
function an(e, t, n) {
  (this.props = e),
    (this.context = t),
    (this.refs = Qi),
    (this.updater = n || Bi);
}
an.prototype.isReactComponent = {};
an.prototype.setState = function (e, t) {
  if (typeof e != 'object' && typeof e != 'function' && e != null)
    throw Error(
      'setState(...): takes an object of state variables to update or a function which returns an object of state variables.'
    );
  this.updater.enqueueSetState(this, e, t, 'setState');
};
an.prototype.forceUpdate = function (e) {
  this.updater.enqueueForceUpdate(this, e, 'forceUpdate');
};
function Xi() {}
Xi.prototype = an.prototype;
function Dl(e, t, n) {
  (this.props = e),
    (this.context = t),
    (this.refs = Qi),
    (this.updater = n || Bi);
}
var Fl = (Dl.prototype = new Xi());
Fl.constructor = Dl;
Wi(Fl, an.prototype);
Fl.isPureReactComponent = !0;
var Ro = Array.isArray,
  qi = Object.prototype.hasOwnProperty,
  Ul = { current: null },
  Yi = { key: !0, ref: !0, __self: !0, __source: !0 };
function Ki(e, t, n) {
  var r,
    a = {},
    l = null,
    o = null;
  if (t != null)
    for (r in (t.ref !== void 0 && (o = t.ref),
    t.key !== void 0 && (l = '' + t.key),
    t))
      qi.call(t, r) && !Yi.hasOwnProperty(r) && (a[r] = t[r]);
  var u = arguments.length - 2;
  if (u === 1) a.children = n;
  else if (1 < u) {
    for (var i = Array(u), c = 0; c < u; c++) i[c] = arguments[c + 2];
    a.children = i;
  }
  if (e && e.defaultProps)
    for (r in ((u = e.defaultProps), u)) a[r] === void 0 && (a[r] = u[r]);
  return {
    $$typeof: qn,
    type: e,
    key: l,
    ref: o,
    props: a,
    _owner: Ul.current,
  };
}
function hc(e, t) {
  return {
    $$typeof: qn,
    type: e.type,
    key: t,
    ref: e.ref,
    props: e.props,
    _owner: e._owner,
  };
}
function Al(e) {
  return typeof e == 'object' && e !== null && e.$$typeof === qn;
}
function mc(e) {
  var t = { '=': '=0', ':': '=2' };
  return (
    '$' +
    e.replace(/[=:]/g, function (n) {
      return t[n];
    })
  );
}
var Io = /\/+/g;
function va(e, t) {
  return typeof e == 'object' && e !== null && e.key != null
    ? mc('' + e.key)
    : t.toString(36);
}
function yr(e, t, n, r, a) {
  var l = typeof e;
  (l === 'undefined' || l === 'boolean') && (e = null);
  var o = !1;
  if (e === null) o = !0;
  else
    switch (l) {
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
      (a = a(o)),
      (e = r === '' ? '.' + va(o, 0) : r),
      Ro(a)
        ? ((n = ''),
          e != null && (n = e.replace(Io, '$&/') + '/'),
          yr(a, t, n, '', function (c) {
            return c;
          }))
        : a != null &&
          (Al(a) &&
            (a = hc(
              a,
              n +
                (!a.key || (o && o.key === a.key)
                  ? ''
                  : ('' + a.key).replace(Io, '$&/') + '/') +
                e
            )),
          t.push(a)),
      1
    );
  if (((o = 0), (r = r === '' ? '.' : r + ':'), Ro(e)))
    for (var u = 0; u < e.length; u++) {
      l = e[u];
      var i = r + va(l, u);
      o += yr(l, t, n, i, a);
    }
  else if (((i = pc(e)), typeof i == 'function'))
    for (e = i.call(e), u = 0; !(l = e.next()).done; )
      (l = l.value), (i = r + va(l, u++)), (o += yr(l, t, n, i, a));
  else if (l === 'object')
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
    a = 0;
  return (
    yr(e, r, '', '', function (l) {
      return t.call(n, l, a++);
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
  vr = { transition: null },
  bc = {
    ReactCurrentDispatcher: ue,
    ReactCurrentBatchConfig: vr,
    ReactCurrentOwner: Ul,
  };
function Gi() {
  throw Error('act(...) is not supported in production builds of React.');
}
L.Children = {
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
    if (!Al(e))
      throw Error(
        'React.Children.only expected to receive a single React element child.'
      );
    return e;
  },
};
L.Component = an;
L.Fragment = ac;
L.Profiler = oc;
L.PureComponent = Dl;
L.StrictMode = lc;
L.Suspense = cc;
L.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = bc;
L.act = Gi;
L.cloneElement = function (e, t, n) {
  if (e == null)
    throw Error(
      'React.cloneElement(...): The argument must be a React element, but you passed ' +
        e +
        '.'
    );
  var r = Wi({}, e.props),
    a = e.key,
    l = e.ref,
    o = e._owner;
  if (t != null) {
    if (
      (t.ref !== void 0 && ((l = t.ref), (o = Ul.current)),
      t.key !== void 0 && (a = '' + t.key),
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
  return { $$typeof: qn, type: e.type, key: a, ref: l, props: r, _owner: o };
};
L.createContext = function (e) {
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
L.createElement = Ki;
L.createFactory = function (e) {
  var t = Ki.bind(null, e);
  return (t.type = e), t;
};
L.createRef = function () {
  return { current: null };
};
L.forwardRef = function (e) {
  return { $$typeof: sc, render: e };
};
L.isValidElement = Al;
L.lazy = function (e) {
  return { $$typeof: fc, _payload: { _status: -1, _result: e }, _init: gc };
};
L.memo = function (e, t) {
  return { $$typeof: dc, type: e, compare: t === void 0 ? null : t };
};
L.startTransition = function (e) {
  var t = vr.transition;
  vr.transition = {};
  try {
    e();
  } finally {
    vr.transition = t;
  }
};
L.unstable_act = Gi;
L.useCallback = function (e, t) {
  return ue.current.useCallback(e, t);
};
L.useContext = function (e) {
  return ue.current.useContext(e);
};
L.useDebugValue = function () {};
L.useDeferredValue = function (e) {
  return ue.current.useDeferredValue(e);
};
L.useEffect = function (e, t) {
  return ue.current.useEffect(e, t);
};
L.useId = function () {
  return ue.current.useId();
};
L.useImperativeHandle = function (e, t, n) {
  return ue.current.useImperativeHandle(e, t, n);
};
L.useInsertionEffect = function (e, t) {
  return ue.current.useInsertionEffect(e, t);
};
L.useLayoutEffect = function (e, t) {
  return ue.current.useLayoutEffect(e, t);
};
L.useMemo = function (e, t) {
  return ue.current.useMemo(e, t);
};
L.useReducer = function (e, t, n) {
  return ue.current.useReducer(e, t, n);
};
L.useRef = function (e) {
  return ue.current.useRef(e);
};
L.useState = function (e) {
  return ue.current.useState(e);
};
L.useSyncExternalStore = function (e, t, n) {
  return ue.current.useSyncExternalStore(e, t, n);
};
L.useTransition = function () {
  return ue.current.useTransition();
};
L.version = '18.3.1';
Hi.exports = L;
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
 */ var vc = Z,
  wc = Symbol.for('react.element'),
  kc = Symbol.for('react.fragment'),
  xc = Object.prototype.hasOwnProperty,
  Sc = vc.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner,
  _c = { key: !0, ref: !0, __self: !0, __source: !0 };
function Ji(e, t, n) {
  var r,
    a = {},
    l = null,
    o = null;
  n !== void 0 && (l = '' + n),
    t.key !== void 0 && (l = '' + t.key),
    t.ref !== void 0 && (o = t.ref);
  for (r in t) xc.call(t, r) && !_c.hasOwnProperty(r) && (a[r] = t[r]);
  if (e && e.defaultProps)
    for (r in ((t = e.defaultProps), t)) a[r] === void 0 && (a[r] = t[r]);
  return {
    $$typeof: wc,
    type: e,
    key: l,
    ref: o,
    props: a,
    _owner: Sc.current,
  };
}
ea.Fragment = kc;
ea.jsx = Ji;
ea.jsxs = Ji;
$i.exports = ea;
var g = $i.exports,
  Wa = {},
  Zi = { exports: {} },
  ve = {},
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
  function t(S, z) {
    var P = S.length;
    S.push(z);
    e: for (; 0 < P; ) {
      var B = (P - 1) >>> 1,
        Y = S[B];
      if (0 < a(Y, z)) (S[B] = z), (S[P] = Y), (P = B);
      else break e;
    }
  }
  function n(S) {
    return S.length === 0 ? null : S[0];
  }
  function r(S) {
    if (S.length === 0) return null;
    var z = S[0],
      P = S.pop();
    if (P !== z) {
      S[0] = P;
      e: for (var B = 0, Y = S.length, Zn = Y >>> 1; B < Zn; ) {
        var gt = 2 * (B + 1) - 1,
          ya = S[gt],
          bt = gt + 1,
          er = S[bt];
        if (0 > a(ya, P))
          bt < Y && 0 > a(er, ya)
            ? ((S[B] = er), (S[bt] = P), (B = bt))
            : ((S[B] = ya), (S[gt] = P), (B = gt));
        else if (bt < Y && 0 > a(er, P)) (S[B] = er), (S[bt] = P), (B = bt);
        else break e;
      }
    }
    return z;
  }
  function a(S, z) {
    var P = S.sortIndex - z.sortIndex;
    return P !== 0 ? P : S.id - z.id;
  }
  if (typeof performance == 'object' && typeof performance.now == 'function') {
    var l = performance;
    e.unstable_now = function () {
      return l.now();
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
    h = 1,
    m = null,
    p = 3,
    w = !1,
    v = !1,
    k = !1,
    M = typeof setTimeout == 'function' ? setTimeout : null,
    f = typeof clearTimeout == 'function' ? clearTimeout : null,
    s = typeof setImmediate < 'u' ? setImmediate : null;
  typeof navigator < 'u' &&
    navigator.scheduling !== void 0 &&
    navigator.scheduling.isInputPending !== void 0 &&
    navigator.scheduling.isInputPending.bind(navigator.scheduling);
  function d(S) {
    for (var z = n(c); z !== null; ) {
      if (z.callback === null) r(c);
      else if (z.startTime <= S)
        r(c), (z.sortIndex = z.expirationTime), t(i, z);
      else break;
      z = n(c);
    }
  }
  function y(S) {
    if (((k = !1), d(S), !v))
      if (n(i) !== null) (v = !0), ga(_);
      else {
        var z = n(c);
        z !== null && ba(y, z.startTime - S);
      }
  }
  function _(S, z) {
    (v = !1), k && ((k = !1), f(C), (C = -1)), (w = !0);
    var P = p;
    try {
      for (
        d(z), m = n(i);
        m !== null && (!(m.expirationTime > z) || (S && !Ce()));

      ) {
        var B = m.callback;
        if (typeof B == 'function') {
          (m.callback = null), (p = m.priorityLevel);
          var Y = B(m.expirationTime <= z);
          (z = e.unstable_now()),
            typeof Y == 'function' ? (m.callback = Y) : m === n(i) && r(i),
            d(z);
        } else r(i);
        m = n(i);
      }
      if (m !== null) var Zn = !0;
      else {
        var gt = n(c);
        gt !== null && ba(y, gt.startTime - z), (Zn = !1);
      }
      return Zn;
    } finally {
      (m = null), (p = P), (w = !1);
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
      var z = !0;
      try {
        z = N(!0, S);
      } finally {
        z ? sn() : ((E = !1), (N = null));
      }
    } else E = !1;
  }
  var sn;
  if (typeof s == 'function')
    sn = function () {
      s(un);
    };
  else if (typeof MessageChannel < 'u') {
    var Mo = new MessageChannel(),
      tc = Mo.port2;
    (Mo.port1.onmessage = un),
      (sn = function () {
        tc.postMessage(null);
      });
  } else
    sn = function () {
      M(un, 0);
    };
  function ga(S) {
    (N = S), E || ((E = !0), sn());
  }
  function ba(S, z) {
    C = M(function () {
      S(e.unstable_now());
    }, z);
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
      v || w || ((v = !0), ga(_));
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
          var z = 3;
          break;
        default:
          z = p;
      }
      var P = p;
      p = z;
      try {
        return S();
      } finally {
        p = P;
      }
    }),
    (e.unstable_pauseExecution = function () {}),
    (e.unstable_requestPaint = function () {}),
    (e.unstable_runWithPriority = function (S, z) {
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
      var P = p;
      p = S;
      try {
        return z();
      } finally {
        p = P;
      }
    }),
    (e.unstable_scheduleCallback = function (S, z, P) {
      var B = e.unstable_now();
      switch (
        (typeof P == 'object' && P !== null
          ? ((P = P.delay), (P = typeof P == 'number' && 0 < P ? B + P : B))
          : (P = B),
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
        (Y = P + Y),
        (S = {
          id: h++,
          callback: z,
          priorityLevel: S,
          startTime: P,
          expirationTime: Y,
          sortIndex: -1,
        }),
        P > B
          ? ((S.sortIndex = P),
            t(c, S),
            n(i) === null &&
              S === n(c) &&
              (k ? (f(C), (C = -1)) : (k = !0), ba(y, P - B)))
          : ((S.sortIndex = Y), t(i, S), v || w || ((v = !0), ga(_))),
        S
      );
    }),
    (e.unstable_shouldYield = Ce),
    (e.unstable_wrapCallback = function (S) {
      var z = p;
      return function () {
        var P = p;
        p = z;
        try {
          return S.apply(this, arguments);
        } finally {
          p = P;
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
function b(e) {
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
function Lt(e, t) {
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
  Qa = Object.prototype.hasOwnProperty,
  Cc =
    /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/,
  Oo = {},
  Do = {};
function zc(e) {
  return Qa.call(Do, e)
    ? !0
    : Qa.call(Oo, e)
    ? !1
    : Cc.test(e)
    ? (Do[e] = !0)
    : ((Oo[e] = !0), !1);
}
function Pc(e, t, n, r) {
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
function Lc(e, t, n, r) {
  if (t === null || typeof t > 'u' || Pc(e, t, n, r)) return !0;
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
function se(e, t, n, r, a, l, o) {
  (this.acceptsBooleans = t === 2 || t === 3 || t === 4),
    (this.attributeName = r),
    (this.attributeNamespace = a),
    (this.mustUseProperty = n),
    (this.propertyName = e),
    (this.type = t),
    (this.sanitizeURL = l),
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
var Vl = /[\-:]([a-z])/g;
function $l(e) {
  return e[1].toUpperCase();
}
'accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height'
  .split(' ')
  .forEach(function (e) {
    var t = e.replace(Vl, $l);
    te[t] = new se(t, 1, !1, e, null, !1, !1);
  });
'xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type'
  .split(' ')
  .forEach(function (e) {
    var t = e.replace(Vl, $l);
    te[t] = new se(t, 1, !1, e, 'http://www.w3.org/1999/xlink', !1, !1);
  });
['xml:base', 'xml:lang', 'xml:space'].forEach(function (e) {
  var t = e.replace(Vl, $l);
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
function Hl(e, t, n, r) {
  var a = te.hasOwnProperty(t) ? te[t] : null;
  (a !== null
    ? a.type !== 0
    : r ||
      !(2 < t.length) ||
      (t[0] !== 'o' && t[0] !== 'O') ||
      (t[1] !== 'n' && t[1] !== 'N')) &&
    (Lc(t, n, a, r) && (n = null),
    r || a === null
      ? zc(t) &&
        (n === null ? e.removeAttribute(t) : e.setAttribute(t, '' + n))
      : a.mustUseProperty
      ? (e[a.propertyName] = n === null ? (a.type === 3 ? !1 : '') : n)
      : ((t = a.attributeName),
        (r = a.attributeNamespace),
        n === null
          ? e.removeAttribute(t)
          : ((a = a.type),
            (n = a === 3 || (a === 4 && n === !0) ? '' : '' + n),
            r ? e.setAttributeNS(r, t, n) : e.setAttribute(t, n))));
}
var Ye = Nc.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED,
  nr = Symbol.for('react.element'),
  Tt = Symbol.for('react.portal'),
  Rt = Symbol.for('react.fragment'),
  Bl = Symbol.for('react.strict_mode'),
  Xa = Symbol.for('react.profiler'),
  ru = Symbol.for('react.provider'),
  au = Symbol.for('react.context'),
  Wl = Symbol.for('react.forward_ref'),
  qa = Symbol.for('react.suspense'),
  Ya = Symbol.for('react.suspense_list'),
  Ql = Symbol.for('react.memo'),
  Ge = Symbol.for('react.lazy'),
  lu = Symbol.for('react.offscreen'),
  Fo = Symbol.iterator;
function cn(e) {
  return e === null || typeof e != 'object'
    ? null
    : ((e = (Fo && e[Fo]) || e['@@iterator']),
      typeof e == 'function' ? e : null);
}
var V = Object.assign,
  wa;
function yn(e) {
  if (wa === void 0)
    try {
      throw Error();
    } catch (n) {
      var t = n.stack.trim().match(/\n( *(at )?)/);
      wa = (t && t[1]) || '';
    }
  return (
    `
` +
    wa +
    e
  );
}
var ka = !1;
function xa(e, t) {
  if (!e || ka) return '';
  ka = !0;
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
        var a = c.stack.split(`
`),
          l = r.stack.split(`
`),
          o = a.length - 1,
          u = l.length - 1;
        1 <= o && 0 <= u && a[o] !== l[u];

      )
        u--;
      for (; 1 <= o && 0 <= u; o--, u--)
        if (a[o] !== l[u]) {
          if (o !== 1 || u !== 1)
            do
              if ((o--, u--, 0 > u || a[o] !== l[u])) {
                var i =
                  `
` + a[o].replace(' at new ', ' at ');
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
    (ka = !1), (Error.prepareStackTrace = n);
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
      return (e = xa(e.type, !1)), e;
    case 11:
      return (e = xa(e.type.render, !1)), e;
    case 1:
      return (e = xa(e.type, !0)), e;
    default:
      return '';
  }
}
function Ka(e) {
  if (e == null) return null;
  if (typeof e == 'function') return e.displayName || e.name || null;
  if (typeof e == 'string') return e;
  switch (e) {
    case Rt:
      return 'Fragment';
    case Tt:
      return 'Portal';
    case Xa:
      return 'Profiler';
    case Bl:
      return 'StrictMode';
    case qa:
      return 'Suspense';
    case Ya:
      return 'SuspenseList';
  }
  if (typeof e == 'object')
    switch (e.$$typeof) {
      case au:
        return (e.displayName || 'Context') + '.Consumer';
      case ru:
        return (e._context.displayName || 'Context') + '.Provider';
      case Wl:
        var t = e.render;
        return (
          (e = e.displayName),
          e ||
            ((e = t.displayName || t.name || ''),
            (e = e !== '' ? 'ForwardRef(' + e + ')' : 'ForwardRef')),
          e
        );
      case Ql:
        return (
          (t = e.displayName || null), t !== null ? t : Ka(e.type) || 'Memo'
        );
      case Ge:
        (t = e._payload), (e = e._init);
        try {
          return Ka(e(t));
        } catch {}
    }
  return null;
}
function Mc(e) {
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
      return Ka(t);
    case 8:
      return t === Bl ? 'StrictMode' : 'Mode';
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
function dt(e) {
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
function Tc(e) {
  var t = ou(e) ? 'checked' : 'value',
    n = Object.getOwnPropertyDescriptor(e.constructor.prototype, t),
    r = '' + e[t];
  if (
    !e.hasOwnProperty(t) &&
    typeof n < 'u' &&
    typeof n.get == 'function' &&
    typeof n.set == 'function'
  ) {
    var a = n.get,
      l = n.set;
    return (
      Object.defineProperty(e, t, {
        configurable: !0,
        get: function () {
          return a.call(this);
        },
        set: function (o) {
          (r = '' + o), l.call(this, o);
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
  e._valueTracker || (e._valueTracker = Tc(e));
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
function Lr(e) {
  if (((e = e || (typeof document < 'u' ? document : void 0)), typeof e > 'u'))
    return null;
  try {
    return e.activeElement || e.body;
  } catch {
    return e.body;
  }
}
function Ga(e, t) {
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
  (n = dt(t.value != null ? t.value : n)),
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
  (t = t.checked), t != null && Hl(e, 'checked', t, !1);
}
function Ja(e, t) {
  uu(e, t);
  var n = dt(t.value),
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
    ? Za(e, t.type, n)
    : t.hasOwnProperty('defaultValue') && Za(e, t.type, dt(t.defaultValue)),
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
function Za(e, t, n) {
  (t !== 'number' || Lr(e.ownerDocument) !== e) &&
    (n == null
      ? (e.defaultValue = '' + e._wrapperState.initialValue)
      : e.defaultValue !== '' + n && (e.defaultValue = '' + n));
}
var vn = Array.isArray;
function Wt(e, t, n, r) {
  if (((e = e.options), t)) {
    t = {};
    for (var a = 0; a < n.length; a++) t['$' + n[a]] = !0;
    for (n = 0; n < e.length; n++)
      (a = t.hasOwnProperty('$' + e[n].value)),
        e[n].selected !== a && (e[n].selected = a),
        a && r && (e[n].defaultSelected = !0);
  } else {
    for (n = '' + dt(n), t = null, a = 0; a < e.length; a++) {
      if (e[a].value === n) {
        (e[a].selected = !0), r && (e[a].defaultSelected = !0);
        return;
      }
      t !== null || e[a].disabled || (t = e[a]);
    }
    t !== null && (t.selected = !0);
  }
}
function el(e, t) {
  if (t.dangerouslySetInnerHTML != null) throw Error(b(91));
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
      if (t != null) throw Error(b(92));
      if (vn(n)) {
        if (1 < n.length) throw Error(b(93));
        n = n[0];
      }
      t = n;
    }
    t == null && (t = ''), (n = t);
  }
  e._wrapperState = { initialValue: dt(n) };
}
function su(e, t) {
  var n = dt(t.value),
    r = dt(t.defaultValue);
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
function tl(e, t) {
  return e == null || e === 'http://www.w3.org/1999/xhtml'
    ? cu(t)
    : e === 'http://www.w3.org/2000/svg' && t === 'foreignObject'
    ? 'http://www.w3.org/1999/xhtml'
    : e;
}
var ar,
  du = (function (e) {
    return typeof MSApp < 'u' && MSApp.execUnsafeLocalFunction
      ? function (t, n, r, a) {
          MSApp.execUnsafeLocalFunction(function () {
            return e(t, n, r, a);
          });
        }
      : e;
  })(function (e, t) {
    if (e.namespaceURI !== 'http://www.w3.org/2000/svg' || 'innerHTML' in e)
      e.innerHTML = t;
    else {
      for (
        ar = ar || document.createElement('div'),
          ar.innerHTML = '<svg>' + t.valueOf().toString() + '</svg>',
          t = ar.firstChild;
        e.firstChild;

      )
        e.removeChild(e.firstChild);
      for (; t.firstChild; ) e.appendChild(t.firstChild);
    }
  });
function Mn(e, t) {
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
  Rc = ['Webkit', 'ms', 'Moz', 'O'];
Object.keys(xn).forEach(function (e) {
  Rc.forEach(function (t) {
    (t = t + e.charAt(0).toUpperCase() + e.substring(1)), (xn[t] = xn[e]);
  });
});
function fu(e, t, n) {
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
        a = fu(n, t[n], r);
      n === 'float' && (n = 'cssFloat'), r ? e.setProperty(n, a) : (e[n] = a);
    }
}
var Ic = V(
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
function nl(e, t) {
  if (t) {
    if (Ic[e] && (t.children != null || t.dangerouslySetInnerHTML != null))
      throw Error(b(137, e));
    if (t.dangerouslySetInnerHTML != null) {
      if (t.children != null) throw Error(b(60));
      if (
        typeof t.dangerouslySetInnerHTML != 'object' ||
        !('__html' in t.dangerouslySetInnerHTML)
      )
        throw Error(b(61));
    }
    if (t.style != null && typeof t.style != 'object') throw Error(b(62));
  }
}
function rl(e, t) {
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
var al = null;
function Xl(e) {
  return (
    (e = e.target || e.srcElement || window),
    e.correspondingUseElement && (e = e.correspondingUseElement),
    e.nodeType === 3 ? e.parentNode : e
  );
}
var ll = null,
  Qt = null,
  Xt = null;
function Ho(e) {
  if ((e = Gn(e))) {
    if (typeof ll != 'function') throw Error(b(280));
    var t = e.stateNode;
    t && ((t = la(t)), ll(e.stateNode, e.type, t));
  }
}
function hu(e) {
  Qt ? (Xt ? Xt.push(e) : (Xt = [e])) : (Qt = e);
}
function mu() {
  if (Qt) {
    var e = Qt,
      t = Xt;
    if (((Xt = Qt = null), Ho(e), t)) for (e = 0; e < t.length; e++) Ho(t[e]);
  }
}
function gu(e, t) {
  return e(t);
}
function bu() {}
var Sa = !1;
function yu(e, t, n) {
  if (Sa) return e(t, n);
  Sa = !0;
  try {
    return gu(e, t, n);
  } finally {
    (Sa = !1), (Qt !== null || Xt !== null) && (bu(), mu());
  }
}
function Tn(e, t) {
  var n = e.stateNode;
  if (n === null) return null;
  var r = la(n);
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
  if (n && typeof n != 'function') throw Error(b(231, t, typeof n));
  return n;
}
var ol = !1;
if (We)
  try {
    var dn = {};
    Object.defineProperty(dn, 'passive', {
      get: function () {
        ol = !0;
      },
    }),
      window.addEventListener('test', dn, dn),
      window.removeEventListener('test', dn, dn);
  } catch {
    ol = !1;
  }
function Oc(e, t, n, r, a, l, o, u, i) {
  var c = Array.prototype.slice.call(arguments, 3);
  try {
    t.apply(n, c);
  } catch (h) {
    this.onError(h);
  }
}
var Sn = !1,
  jr = null,
  Mr = !1,
  il = null,
  Dc = {
    onError: function (e) {
      (Sn = !0), (jr = e);
    },
  };
function Fc(e, t, n, r, a, l, o, u, i) {
  (Sn = !1), (jr = null), Oc.apply(Dc, arguments);
}
function Uc(e, t, n, r, a, l, o, u, i) {
  if ((Fc.apply(this, arguments), Sn)) {
    if (Sn) {
      var c = jr;
      (Sn = !1), (jr = null);
    } else throw Error(b(198));
    Mr || ((Mr = !0), (il = c));
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
function vu(e) {
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
  if (jt(e) !== e) throw Error(b(188));
}
function Ac(e) {
  var t = e.alternate;
  if (!t) {
    if (((t = jt(e)), t === null)) throw Error(b(188));
    return t !== e ? null : e;
  }
  for (var n = e, r = t; ; ) {
    var a = n.return;
    if (a === null) break;
    var l = a.alternate;
    if (l === null) {
      if (((r = a.return), r !== null)) {
        n = r;
        continue;
      }
      break;
    }
    if (a.child === l.child) {
      for (l = a.child; l; ) {
        if (l === n) return Bo(a), e;
        if (l === r) return Bo(a), t;
        l = l.sibling;
      }
      throw Error(b(188));
    }
    if (n.return !== r.return) (n = a), (r = l);
    else {
      for (var o = !1, u = a.child; u; ) {
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
      if (!o) {
        for (u = l.child; u; ) {
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
        if (!o) throw Error(b(189));
      }
    }
    if (n.alternate !== r) throw Error(b(190));
  }
  if (n.tag !== 3) throw Error(b(188));
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
  ql = ye.unstable_ImmediatePriority,
  Su = ye.unstable_UserBlockingPriority,
  Tr = ye.unstable_NormalPriority,
  Bc = ye.unstable_LowPriority,
  _u = ye.unstable_IdlePriority,
  ta = null,
  Fe = null;
function Wc(e) {
  if (Fe && typeof Fe.onCommitFiberRoot == 'function')
    try {
      Fe.onCommitFiberRoot(ta, e, void 0, (e.current.flags & 128) === 128);
    } catch {}
}
var Me = Math.clz32 ? Math.clz32 : qc,
  Qc = Math.log,
  Xc = Math.LN2;
function qc(e) {
  return (e >>>= 0), e === 0 ? 32 : (31 - ((Qc(e) / Xc) | 0)) | 0;
}
var lr = 64,
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
function Rr(e, t) {
  var n = e.pendingLanes;
  if (n === 0) return 0;
  var r = 0,
    a = e.suspendedLanes,
    l = e.pingedLanes,
    o = n & 268435455;
  if (o !== 0) {
    var u = o & ~a;
    u !== 0 ? (r = wn(u)) : ((l &= o), l !== 0 && (r = wn(l)));
  } else (o = n & ~a), o !== 0 ? (r = wn(o)) : l !== 0 && (r = wn(l));
  if (r === 0) return 0;
  if (
    t !== 0 &&
    t !== r &&
    !(t & a) &&
    ((a = r & -r), (l = t & -t), a >= l || (a === 16 && (l & 4194240) !== 0))
  )
    return t;
  if ((r & 4 && (r |= n & 16), (t = e.entangledLanes), t !== 0))
    for (e = e.entanglements, t &= r; 0 < t; )
      (n = 31 - Me(t)), (a = 1 << n), (r |= e[n]), (t &= ~a);
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
      a = e.expirationTimes,
      l = e.pendingLanes;
    0 < l;

  ) {
    var o = 31 - Me(l),
      u = 1 << o,
      i = a[o];
    i === -1
      ? (!(u & n) || u & r) && (a[o] = Yc(u, t))
      : i <= t && (e.expiredLanes |= u),
      (l &= ~u);
  }
}
function ul(e) {
  return (
    (e = e.pendingLanes & -1073741825),
    e !== 0 ? e : e & 1073741824 ? 1073741824 : 0
  );
}
function Eu() {
  var e = lr;
  return (lr <<= 1), !(lr & 4194240) && (lr = 64), e;
}
function _a(e) {
  for (var t = [], n = 0; 31 > n; n++) t.push(e);
  return t;
}
function Yn(e, t, n) {
  (e.pendingLanes |= t),
    t !== 536870912 && ((e.suspendedLanes = 0), (e.pingedLanes = 0)),
    (e = e.eventTimes),
    (t = 31 - Me(t)),
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
    var a = 31 - Me(n),
      l = 1 << a;
    (t[a] = 0), (r[a] = -1), (e[a] = -1), (n &= ~l);
  }
}
function Yl(e, t) {
  var n = (e.entangledLanes |= t);
  for (e = e.entanglements; n; ) {
    var r = 31 - Me(n),
      a = 1 << r;
    (a & t) | (e[r] & t) && (e[r] |= t), (n &= ~a);
  }
}
var R = 0;
function Nu(e) {
  return (e &= -e), 1 < e ? (4 < e ? (e & 268435455 ? 16 : 536870912) : 4) : 1;
}
var Cu,
  Kl,
  zu,
  Pu,
  Lu,
  sl = !1,
  ir = [],
  rt = null,
  at = null,
  lt = null,
  Rn = new Map(),
  In = new Map(),
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
      at = null;
      break;
    case 'mouseover':
    case 'mouseout':
      lt = null;
      break;
    case 'pointerover':
    case 'pointerout':
      Rn.delete(t.pointerId);
      break;
    case 'gotpointercapture':
    case 'lostpointercapture':
      In.delete(t.pointerId);
  }
}
function fn(e, t, n, r, a, l) {
  return e === null || e.nativeEvent !== l
    ? ((e = {
        blockedOn: t,
        domEventName: n,
        eventSystemFlags: r,
        nativeEvent: l,
        targetContainers: [a],
      }),
      t !== null && ((t = Gn(t)), t !== null && Kl(t)),
      e)
    : ((e.eventSystemFlags |= r),
      (t = e.targetContainers),
      a !== null && t.indexOf(a) === -1 && t.push(a),
      e);
}
function Zc(e, t, n, r, a) {
  switch (t) {
    case 'focusin':
      return (rt = fn(rt, e, t, n, r, a)), !0;
    case 'dragenter':
      return (at = fn(at, e, t, n, r, a)), !0;
    case 'mouseover':
      return (lt = fn(lt, e, t, n, r, a)), !0;
    case 'pointerover':
      var l = a.pointerId;
      return Rn.set(l, fn(Rn.get(l) || null, e, t, n, r, a)), !0;
    case 'gotpointercapture':
      return (
        (l = a.pointerId), In.set(l, fn(In.get(l) || null, e, t, n, r, a)), !0
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
        if (((t = vu(n)), t !== null)) {
          (e.blockedOn = t),
            Lu(e.priority, function () {
              zu(n);
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
    var n = cl(e.domEventName, e.eventSystemFlags, t[0], e.nativeEvent);
    if (n === null) {
      n = e.nativeEvent;
      var r = new n.constructor(n.type, n);
      (al = r), n.target.dispatchEvent(r), (al = null);
    } else return (t = Gn(n)), t !== null && Kl(t), (e.blockedOn = n), !1;
    t.shift();
  }
  return !0;
}
function Xo(e, t, n) {
  wr(e) && n.delete(t);
}
function ed() {
  (sl = !1),
    rt !== null && wr(rt) && (rt = null),
    at !== null && wr(at) && (at = null),
    lt !== null && wr(lt) && (lt = null),
    Rn.forEach(Xo),
    In.forEach(Xo);
}
function pn(e, t) {
  e.blockedOn === t &&
    ((e.blockedOn = null),
    sl ||
      ((sl = !0),
      ye.unstable_scheduleCallback(ye.unstable_NormalPriority, ed)));
}
function On(e) {
  function t(a) {
    return pn(a, e);
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
      at !== null && pn(at, e),
      lt !== null && pn(lt, e),
      Rn.forEach(t),
      In.forEach(t),
      n = 0;
    n < Ze.length;
    n++
  )
    (r = Ze[n]), r.blockedOn === e && (r.blockedOn = null);
  for (; 0 < Ze.length && ((n = Ze[0]), n.blockedOn === null); )
    ju(n), n.blockedOn === null && Ze.shift();
}
var qt = Ye.ReactCurrentBatchConfig,
  Ir = !0;
function td(e, t, n, r) {
  var a = R,
    l = qt.transition;
  qt.transition = null;
  try {
    (R = 1), Gl(e, t, n, r);
  } finally {
    (R = a), (qt.transition = l);
  }
}
function nd(e, t, n, r) {
  var a = R,
    l = qt.transition;
  qt.transition = null;
  try {
    (R = 4), Gl(e, t, n, r);
  } finally {
    (R = a), (qt.transition = l);
  }
}
function Gl(e, t, n, r) {
  if (Ir) {
    var a = cl(e, t, n, r);
    if (a === null) Ra(e, t, r, Or, n), Qo(e, r);
    else if (Zc(a, e, t, n, r)) r.stopPropagation();
    else if ((Qo(e, r), t & 4 && -1 < Jc.indexOf(e))) {
      for (; a !== null; ) {
        var l = Gn(a);
        if (
          (l !== null && Cu(l),
          (l = cl(e, t, n, r)),
          l === null && Ra(e, t, r, Or, n),
          l === a)
        )
          break;
        a = l;
      }
      a !== null && r.stopPropagation();
    } else Ra(e, t, r, null, n);
  }
}
var Or = null;
function cl(e, t, n, r) {
  if (((Or = null), (e = Xl(r)), (e = wt(e)), e !== null))
    if (((t = jt(e)), t === null)) e = null;
    else if (((n = t.tag), n === 13)) {
      if (((e = vu(t)), e !== null)) return e;
      e = null;
    } else if (n === 3) {
      if (t.stateNode.current.memoizedState.isDehydrated)
        return t.tag === 3 ? t.stateNode.containerInfo : null;
      e = null;
    } else t !== e && (e = null);
  return (Or = e), null;
}
function Mu(e) {
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
        case ql:
          return 1;
        case Su:
          return 4;
        case Tr:
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
  Jl = null,
  kr = null;
function Tu() {
  if (kr) return kr;
  var e,
    t = Jl,
    n = t.length,
    r,
    a = 'value' in tt ? tt.value : tt.textContent,
    l = a.length;
  for (e = 0; e < n && t[e] === a[e]; e++);
  var o = n - e;
  for (r = 1; r <= o && t[n - r] === a[l - r]; r++);
  return (kr = a.slice(e, 1 < r ? 1 - r : void 0));
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
  function t(n, r, a, l, o) {
    (this._reactName = n),
      (this._targetInst = a),
      (this.type = r),
      (this.nativeEvent = l),
      (this.target = o),
      (this.currentTarget = null);
    for (var u in e)
      e.hasOwnProperty(u) && ((n = e[u]), (this[u] = n ? n(l) : l[u]));
    return (
      (this.isDefaultPrevented = (
        l.defaultPrevented != null ? l.defaultPrevented : l.returnValue === !1
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
var ln = {
    eventPhase: 0,
    bubbles: 0,
    cancelable: 0,
    timeStamp: function (e) {
      return e.timeStamp || Date.now();
    },
    defaultPrevented: 0,
    isTrusted: 0,
  },
  Zl = we(ln),
  Kn = V({}, ln, { view: 0, detail: 0 }),
  rd = we(Kn),
  Ea,
  Na,
  hn,
  na = V({}, Kn, {
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
        : (e !== hn &&
            (hn && e.type === 'mousemove'
              ? ((Ea = e.screenX - hn.screenX), (Na = e.screenY - hn.screenY))
              : (Na = Ea = 0),
            (hn = e)),
          Ea);
    },
    movementY: function (e) {
      return 'movementY' in e ? e.movementY : Na;
    },
  }),
  Yo = we(na),
  ad = V({}, na, { dataTransfer: 0 }),
  ld = we(ad),
  od = V({}, Kn, { relatedTarget: 0 }),
  Ca = we(od),
  id = V({}, ln, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }),
  ud = we(id),
  sd = V({}, ln, {
    clipboardData: function (e) {
      return 'clipboardData' in e ? e.clipboardData : window.clipboardData;
    },
  }),
  cd = we(sd),
  dd = V({}, ln, { data: 0 }),
  Ko = we(dd),
  fd = {
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
  pd = {
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
  hd = {
    Alt: 'altKey',
    Control: 'ctrlKey',
    Meta: 'metaKey',
    Shift: 'shiftKey',
  };
function md(e) {
  var t = this.nativeEvent;
  return t.getModifierState
    ? t.getModifierState(e)
    : (e = hd[e])
    ? !!t[e]
    : !1;
}
function eo() {
  return md;
}
var gd = V({}, Kn, {
    key: function (e) {
      if (e.key) {
        var t = fd[e.key] || e.key;
        if (t !== 'Unidentified') return t;
      }
      return e.type === 'keypress'
        ? ((e = xr(e)), e === 13 ? 'Enter' : String.fromCharCode(e))
        : e.type === 'keydown' || e.type === 'keyup'
        ? pd[e.keyCode] || 'Unidentified'
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
  bd = we(gd),
  yd = V({}, na, {
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
  Go = we(yd),
  vd = V({}, Kn, {
    touches: 0,
    targetTouches: 0,
    changedTouches: 0,
    altKey: 0,
    metaKey: 0,
    ctrlKey: 0,
    shiftKey: 0,
    getModifierState: eo,
  }),
  wd = we(vd),
  kd = V({}, ln, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }),
  xd = we(kd),
  Sd = V({}, na, {
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
  _d = we(Sd),
  Ed = [9, 13, 27, 32],
  to = We && 'CompositionEvent' in window,
  _n = null;
We && 'documentMode' in document && (_n = document.documentMode);
var Nd = We && 'TextEvent' in window && !_n,
  Ru = We && (!to || (_n && 8 < _n && 11 >= _n)),
  Jo = ' ',
  Zo = !1;
function Iu(e, t) {
  switch (e) {
    case 'keyup':
      return Ed.indexOf(t.keyCode) !== -1;
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
function Ou(e) {
  return (e = e.detail), typeof e == 'object' && 'data' in e ? e.data : null;
}
var It = !1;
function Cd(e, t) {
  switch (e) {
    case 'compositionend':
      return Ou(t);
    case 'keypress':
      return t.which !== 32 ? null : ((Zo = !0), Jo);
    case 'textInput':
      return (e = t.data), e === Jo && Zo ? null : e;
    default:
      return null;
  }
}
function zd(e, t) {
  if (It)
    return e === 'compositionend' || (!to && Iu(e, t))
      ? ((e = Tu()), (kr = Jl = tt = null), (It = !1), e)
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
      return Ru && t.locale !== 'ko' ? null : t.data;
    default:
      return null;
  }
}
var Pd = {
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
  return t === 'input' ? !!Pd[e.type] : t === 'textarea';
}
function Du(e, t, n, r) {
  hu(r),
    (t = Dr(t, 'onChange')),
    0 < t.length &&
      ((n = new Zl('onChange', 'change', null, n, r)),
      e.push({ event: n, listeners: t }));
}
var En = null,
  Dn = null;
function Ld(e) {
  qu(e, 0);
}
function ra(e) {
  var t = Ft(e);
  if (iu(t)) return e;
}
function jd(e, t) {
  if (e === 'change') return t;
}
var Fu = !1;
if (We) {
  var za;
  if (We) {
    var Pa = 'oninput' in document;
    if (!Pa) {
      var ti = document.createElement('div');
      ti.setAttribute('oninput', 'return;'),
        (Pa = typeof ti.oninput == 'function');
    }
    za = Pa;
  } else za = !1;
  Fu = za && (!document.documentMode || 9 < document.documentMode);
}
function ni() {
  En && (En.detachEvent('onpropertychange', Uu), (Dn = En = null));
}
function Uu(e) {
  if (e.propertyName === 'value' && ra(Dn)) {
    var t = [];
    Du(t, Dn, e, Xl(e)), yu(Ld, t);
  }
}
function Md(e, t, n) {
  e === 'focusin'
    ? (ni(), (En = t), (Dn = n), En.attachEvent('onpropertychange', Uu))
    : e === 'focusout' && ni();
}
function Td(e) {
  if (e === 'selectionchange' || e === 'keyup' || e === 'keydown')
    return ra(Dn);
}
function Rd(e, t) {
  if (e === 'click') return ra(t);
}
function Id(e, t) {
  if (e === 'input' || e === 'change') return ra(t);
}
function Od(e, t) {
  return (e === t && (e !== 0 || 1 / e === 1 / t)) || (e !== e && t !== t);
}
var Re = typeof Object.is == 'function' ? Object.is : Od;
function Fn(e, t) {
  if (Re(e, t)) return !0;
  if (typeof e != 'object' || e === null || typeof t != 'object' || t === null)
    return !1;
  var n = Object.keys(e),
    r = Object.keys(t);
  if (n.length !== r.length) return !1;
  for (r = 0; r < n.length; r++) {
    var a = n[r];
    if (!Qa.call(t, a) || !Re(e[a], t[a])) return !1;
  }
  return !0;
}
function ri(e) {
  for (; e && e.firstChild; ) e = e.firstChild;
  return e;
}
function ai(e, t) {
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
  for (var e = window, t = Lr(); t instanceof e.HTMLIFrameElement; ) {
    try {
      var n = typeof t.contentWindow.location.href == 'string';
    } catch {
      n = !1;
    }
    if (n) e = t.contentWindow;
    else break;
    t = Lr(e.document);
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
function Dd(e) {
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
        var a = n.textContent.length,
          l = Math.min(r.start, a);
        (r = r.end === void 0 ? l : Math.min(r.end, a)),
          !e.extend && l > r && ((a = r), (r = l), (l = a)),
          (a = ai(n, l));
        var o = ai(n, r);
        a &&
          o &&
          (e.rangeCount !== 1 ||
            e.anchorNode !== a.node ||
            e.anchorOffset !== a.offset ||
            e.focusNode !== o.node ||
            e.focusOffset !== o.offset) &&
          ((t = t.createRange()),
          t.setStart(a.node, a.offset),
          e.removeAllRanges(),
          l > r
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
var Fd = We && 'documentMode' in document && 11 >= document.documentMode,
  Ot = null,
  dl = null,
  Nn = null,
  fl = !1;
function li(e, t, n) {
  var r = n.window === n ? n.document : n.nodeType === 9 ? n : n.ownerDocument;
  fl ||
    Ot == null ||
    Ot !== Lr(r) ||
    ((r = Ot),
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
      (r = Dr(dl, 'onSelect')),
      0 < r.length &&
        ((t = new Zl('onSelect', 'select', null, t, n)),
        e.push({ event: t, listeners: r }),
        (t.target = Ot))));
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
var Dt = {
    animationend: sr('Animation', 'AnimationEnd'),
    animationiteration: sr('Animation', 'AnimationIteration'),
    animationstart: sr('Animation', 'AnimationStart'),
    transitionend: sr('Transition', 'TransitionEnd'),
  },
  La = {},
  $u = {};
We &&
  (($u = document.createElement('div').style),
  'AnimationEvent' in window ||
    (delete Dt.animationend.animation,
    delete Dt.animationiteration.animation,
    delete Dt.animationstart.animation),
  'TransitionEvent' in window || delete Dt.transitionend.transition);
function aa(e) {
  if (La[e]) return La[e];
  if (!Dt[e]) return e;
  var t = Dt[e],
    n;
  for (n in t) if (t.hasOwnProperty(n) && n in $u) return (La[e] = t[n]);
  return e;
}
var Hu = aa('animationend'),
  Bu = aa('animationiteration'),
  Wu = aa('animationstart'),
  Qu = aa('transitionend'),
  Xu = new Map(),
  oi =
    'abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel'.split(
      ' '
    );
function pt(e, t) {
  Xu.set(e, t), Lt(t, [e]);
}
for (var ja = 0; ja < oi.length; ja++) {
  var Ma = oi[ja],
    Ud = Ma.toLowerCase(),
    Ad = Ma[0].toUpperCase() + Ma.slice(1);
  pt(Ud, 'on' + Ad);
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
Lt(
  'onChange',
  'change click focusin focusout input keydown keyup selectionchange'.split(
    ' '
  )
);
Lt(
  'onSelect',
  'focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange'.split(
    ' '
  )
);
Lt('onBeforeInput', ['compositionend', 'keypress', 'textInput', 'paste']);
Lt(
  'onCompositionEnd',
  'compositionend focusout keydown keypress keyup mousedown'.split(' ')
);
Lt(
  'onCompositionStart',
  'compositionstart focusout keydown keypress keyup mousedown'.split(' ')
);
Lt(
  'onCompositionUpdate',
  'compositionupdate focusout keydown keypress keyup mousedown'.split(' ')
);
var kn =
    'abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting'.split(
      ' '
    ),
  Vd = new Set(
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
      a = r.event;
    r = r.listeners;
    e: {
      var l = void 0;
      if (t)
        for (var o = r.length - 1; 0 <= o; o--) {
          var u = r[o],
            i = u.instance,
            c = u.currentTarget;
          if (((u = u.listener), i !== l && a.isPropagationStopped())) break e;
          ii(a, u, c), (l = i);
        }
      else
        for (o = 0; o < r.length; o++) {
          if (
            ((u = r[o]),
            (i = u.instance),
            (c = u.currentTarget),
            (u = u.listener),
            i !== l && a.isPropagationStopped())
          )
            break e;
          ii(a, u, c), (l = i);
        }
    }
  }
  if (Mr) throw ((e = il), (Mr = !1), (il = null), e);
}
function O(e, t) {
  var n = t[bl];
  n === void 0 && (n = t[bl] = new Set());
  var r = e + '__bubble';
  n.has(r) || (Yu(t, e, 2, !1), n.add(r));
}
function Ta(e, t, n) {
  var r = 0;
  t && (r |= 4), Yu(n, e, r, t);
}
var cr = '_reactListening' + Math.random().toString(36).slice(2);
function Un(e) {
  if (!e[cr]) {
    (e[cr] = !0),
      nu.forEach(function (n) {
        n !== 'selectionchange' && (Vd.has(n) || Ta(n, !1, e), Ta(n, !0, e));
      });
    var t = e.nodeType === 9 ? e : e.ownerDocument;
    t === null || t[cr] || ((t[cr] = !0), Ta('selectionchange', !1, t));
  }
}
function Yu(e, t, n, r) {
  switch (Mu(t)) {
    case 1:
      var a = td;
      break;
    case 4:
      a = nd;
      break;
    default:
      a = Gl;
  }
  (n = a.bind(null, t, n, e)),
    (a = void 0),
    !ol ||
      (t !== 'touchstart' && t !== 'touchmove' && t !== 'wheel') ||
      (a = !0),
    r
      ? a !== void 0
        ? e.addEventListener(t, n, { capture: !0, passive: a })
        : e.addEventListener(t, n, !0)
      : a !== void 0
      ? e.addEventListener(t, n, { passive: a })
      : e.addEventListener(t, n, !1);
}
function Ra(e, t, n, r, a) {
  var l = r;
  if (!(t & 1) && !(t & 2) && r !== null)
    e: for (;;) {
      if (r === null) return;
      var o = r.tag;
      if (o === 3 || o === 4) {
        var u = r.stateNode.containerInfo;
        if (u === a || (u.nodeType === 8 && u.parentNode === a)) break;
        if (o === 4)
          for (o = r.return; o !== null; ) {
            var i = o.tag;
            if (
              (i === 3 || i === 4) &&
              ((i = o.stateNode.containerInfo),
              i === a || (i.nodeType === 8 && i.parentNode === a))
            )
              return;
            o = o.return;
          }
        for (; u !== null; ) {
          if (((o = wt(u)), o === null)) return;
          if (((i = o.tag), i === 5 || i === 6)) {
            r = l = o;
            continue e;
          }
          u = u.parentNode;
        }
      }
      r = r.return;
    }
  yu(function () {
    var c = l,
      h = Xl(n),
      m = [];
    e: {
      var p = Xu.get(e);
      if (p !== void 0) {
        var w = Zl,
          v = e;
        switch (e) {
          case 'keypress':
            if (xr(n) === 0) break e;
          case 'keydown':
          case 'keyup':
            w = bd;
            break;
          case 'focusin':
            (v = 'focus'), (w = Ca);
            break;
          case 'focusout':
            (v = 'blur'), (w = Ca);
            break;
          case 'beforeblur':
          case 'afterblur':
            w = Ca;
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
            w = ld;
            break;
          case 'touchcancel':
          case 'touchend':
          case 'touchmove':
          case 'touchstart':
            w = wd;
            break;
          case Hu:
          case Bu:
          case Wu:
            w = ud;
            break;
          case Qu:
            w = xd;
            break;
          case 'scroll':
            w = rd;
            break;
          case 'wheel':
            w = _d;
            break;
          case 'copy':
          case 'cut':
          case 'paste':
            w = cd;
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
          M = !k && e === 'scroll',
          f = k ? (p !== null ? p + 'Capture' : null) : p;
        k = [];
        for (var s = c, d; s !== null; ) {
          d = s;
          var y = d.stateNode;
          if (
            (d.tag === 5 &&
              y !== null &&
              ((d = y),
              f !== null &&
                ((y = Tn(s, f)), y != null && k.push(An(s, y, d)))),
            M)
          )
            break;
          s = s.return;
        }
        0 < k.length &&
          ((p = new w(p, v, null, n, h)), m.push({ event: p, listeners: k }));
      }
    }
    if (!(t & 7)) {
      e: {
        if (
          ((p = e === 'mouseover' || e === 'pointerover'),
          (w = e === 'mouseout' || e === 'pointerout'),
          p &&
            n !== al &&
            (v = n.relatedTarget || n.fromElement) &&
            (wt(v) || v[Qe]))
        )
          break e;
        if (
          (w || p) &&
          ((p =
            h.window === h
              ? h
              : (p = h.ownerDocument)
              ? p.defaultView || p.parentWindow
              : window),
          w
            ? ((v = n.relatedTarget || n.toElement),
              (w = c),
              (v = v ? wt(v) : null),
              v !== null &&
                ((M = jt(v)), v !== M || (v.tag !== 5 && v.tag !== 6)) &&
                (v = null))
            : ((w = null), (v = c)),
          w !== v)
        ) {
          if (
            ((k = Yo),
            (y = 'onMouseLeave'),
            (f = 'onMouseEnter'),
            (s = 'mouse'),
            (e === 'pointerout' || e === 'pointerover') &&
              ((k = Go),
              (y = 'onPointerLeave'),
              (f = 'onPointerEnter'),
              (s = 'pointer')),
            (M = w == null ? p : Ft(w)),
            (d = v == null ? p : Ft(v)),
            (p = new k(y, s + 'leave', w, n, h)),
            (p.target = M),
            (p.relatedTarget = d),
            (y = null),
            wt(h) === c &&
              ((k = new k(f, s + 'enter', v, n, h)),
              (k.target = d),
              (k.relatedTarget = M),
              (y = k)),
            (M = y),
            w && v)
          )
            t: {
              for (k = w, f = v, s = 0, d = k; d; d = Mt(d)) s++;
              for (d = 0, y = f; y; y = Mt(y)) d++;
              for (; 0 < s - d; ) (k = Mt(k)), s--;
              for (; 0 < d - s; ) (f = Mt(f)), d--;
              for (; s--; ) {
                if (k === f || (f !== null && k === f.alternate)) break t;
                (k = Mt(k)), (f = Mt(f));
              }
              k = null;
            }
          else k = null;
          w !== null && ui(m, p, w, k, !1),
            v !== null && M !== null && ui(m, M, v, k, !0);
        }
      }
      e: {
        if (
          ((p = c ? Ft(c) : window),
          (w = p.nodeName && p.nodeName.toLowerCase()),
          w === 'select' || (w === 'input' && p.type === 'file'))
        )
          var _ = jd;
        else if (ei(p))
          if (Fu) _ = Id;
          else {
            _ = Td;
            var E = Md;
          }
        else
          (w = p.nodeName) &&
            w.toLowerCase() === 'input' &&
            (p.type === 'checkbox' || p.type === 'radio') &&
            (_ = Rd);
        if (_ && (_ = _(e, c))) {
          Du(m, _, n, h);
          break e;
        }
        E && E(e, p, c),
          e === 'focusout' &&
            (E = p._wrapperState) &&
            E.controlled &&
            p.type === 'number' &&
            Za(p, 'number', p.value);
      }
      switch (((E = c ? Ft(c) : window), e)) {
        case 'focusin':
          (ei(E) || E.contentEditable === 'true') &&
            ((Ot = E), (dl = c), (Nn = null));
          break;
        case 'focusout':
          Nn = dl = Ot = null;
          break;
        case 'mousedown':
          fl = !0;
          break;
        case 'contextmenu':
        case 'mouseup':
        case 'dragend':
          (fl = !1), li(m, n, h);
          break;
        case 'selectionchange':
          if (Fd) break;
        case 'keydown':
        case 'keyup':
          li(m, n, h);
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
        It
          ? Iu(e, n) && (C = 'onCompositionEnd')
          : e === 'keydown' && n.keyCode === 229 && (C = 'onCompositionStart');
      C &&
        (Ru &&
          n.locale !== 'ko' &&
          (It || C !== 'onCompositionStart'
            ? C === 'onCompositionEnd' && It && (N = Tu())
            : ((tt = h),
              (Jl = 'value' in tt ? tt.value : tt.textContent),
              (It = !0))),
        (E = Dr(c, C)),
        0 < E.length &&
          ((C = new Ko(C, e, null, n, h)),
          m.push({ event: C, listeners: E }),
          N ? (C.data = N) : ((N = Ou(n)), N !== null && (C.data = N)))),
        (N = Nd ? Cd(e, n) : zd(e, n)) &&
          ((c = Dr(c, 'onBeforeInput')),
          0 < c.length &&
            ((h = new Ko('onBeforeInput', 'beforeinput', null, n, h)),
            m.push({ event: h, listeners: c }),
            (h.data = N)));
    }
    qu(m, t);
  });
}
function An(e, t, n) {
  return { instance: e, listener: t, currentTarget: n };
}
function Dr(e, t) {
  for (var n = t + 'Capture', r = []; e !== null; ) {
    var a = e,
      l = a.stateNode;
    a.tag === 5 &&
      l !== null &&
      ((a = l),
      (l = Tn(e, n)),
      l != null && r.unshift(An(e, l, a)),
      (l = Tn(e, t)),
      l != null && r.push(An(e, l, a))),
      (e = e.return);
  }
  return r;
}
function Mt(e) {
  if (e === null) return null;
  do e = e.return;
  while (e && e.tag !== 5);
  return e || null;
}
function ui(e, t, n, r, a) {
  for (var l = t._reactName, o = []; n !== null && n !== r; ) {
    var u = n,
      i = u.alternate,
      c = u.stateNode;
    if (i !== null && i === r) break;
    u.tag === 5 &&
      c !== null &&
      ((u = c),
      a
        ? ((i = Tn(n, l)), i != null && o.unshift(An(n, i, u)))
        : a || ((i = Tn(n, l)), i != null && o.push(An(n, i, u)))),
      (n = n.return);
  }
  o.length !== 0 && e.push({ event: t, listeners: o });
}
var $d = /\r\n?/g,
  Hd = /\u0000|\uFFFD/g;
function si(e) {
  return (typeof e == 'string' ? e : '' + e)
    .replace(
      $d,
      `
`
    )
    .replace(Hd, '');
}
function dr(e, t, n) {
  if (((t = si(t)), si(e) !== t && n)) throw Error(b(425));
}
function Fr() {}
var pl = null,
  hl = null;
function ml(e, t) {
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
var gl = typeof setTimeout == 'function' ? setTimeout : void 0,
  Bd = typeof clearTimeout == 'function' ? clearTimeout : void 0,
  ci = typeof Promise == 'function' ? Promise : void 0,
  Wd =
    typeof queueMicrotask == 'function'
      ? queueMicrotask
      : typeof ci < 'u'
      ? function (e) {
          return ci.resolve(null).then(e).catch(Qd);
        }
      : gl;
function Qd(e) {
  setTimeout(function () {
    throw e;
  });
}
function Ia(e, t) {
  var n = t,
    r = 0;
  do {
    var a = n.nextSibling;
    if ((e.removeChild(n), a && a.nodeType === 8))
      if (((n = a.data), n === '/$')) {
        if (r === 0) {
          e.removeChild(a), On(t);
          return;
        }
        r--;
      } else (n !== '$' && n !== '$?' && n !== '$!') || r++;
    n = a;
  } while (n);
  On(t);
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
function di(e) {
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
  De = '__reactFiber$' + on,
  Vn = '__reactProps$' + on,
  Qe = '__reactContainer$' + on,
  bl = '__reactEvents$' + on,
  Xd = '__reactListeners$' + on,
  qd = '__reactHandles$' + on;
function wt(e) {
  var t = e[De];
  if (t) return t;
  for (var n = e.parentNode; n; ) {
    if ((t = n[Qe] || n[De])) {
      if (
        ((n = t.alternate),
        t.child !== null || (n !== null && n.child !== null))
      )
        for (e = di(e); e !== null; ) {
          if ((n = e[De])) return n;
          e = di(e);
        }
      return t;
    }
    (e = n), (n = e.parentNode);
  }
  return null;
}
function Gn(e) {
  return (
    (e = e[De] || e[Qe]),
    !e || (e.tag !== 5 && e.tag !== 6 && e.tag !== 13 && e.tag !== 3)
      ? null
      : e
  );
}
function Ft(e) {
  if (e.tag === 5 || e.tag === 6) return e.stateNode;
  throw Error(b(33));
}
function la(e) {
  return e[Vn] || null;
}
var yl = [],
  Ut = -1;
function ht(e) {
  return { current: e };
}
function D(e) {
  0 > Ut || ((e.current = yl[Ut]), (yl[Ut] = null), Ut--);
}
function I(e, t) {
  Ut++, (yl[Ut] = e.current), (e.current = t);
}
var ft = {},
  le = ht(ft),
  fe = ht(!1),
  Et = ft;
function Jt(e, t) {
  var n = e.type.contextTypes;
  if (!n) return ft;
  var r = e.stateNode;
  if (r && r.__reactInternalMemoizedUnmaskedChildContext === t)
    return r.__reactInternalMemoizedMaskedChildContext;
  var a = {},
    l;
  for (l in n) a[l] = t[l];
  return (
    r &&
      ((e = e.stateNode),
      (e.__reactInternalMemoizedUnmaskedChildContext = t),
      (e.__reactInternalMemoizedMaskedChildContext = a)),
    a
  );
}
function pe(e) {
  return (e = e.childContextTypes), e != null;
}
function Ur() {
  D(fe), D(le);
}
function fi(e, t, n) {
  if (le.current !== ft) throw Error(b(168));
  I(le, t), I(fe, n);
}
function Ku(e, t, n) {
  var r = e.stateNode;
  if (((t = t.childContextTypes), typeof r.getChildContext != 'function'))
    return n;
  r = r.getChildContext();
  for (var a in r) if (!(a in t)) throw Error(b(108, Mc(e) || 'Unknown', a));
  return V({}, n, r);
}
function Ar(e) {
  return (
    (e =
      ((e = e.stateNode) && e.__reactInternalMemoizedMergedChildContext) ||
      ft),
    (Et = le.current),
    I(le, e),
    I(fe, fe.current),
    !0
  );
}
function pi(e, t, n) {
  var r = e.stateNode;
  if (!r) throw Error(b(169));
  n
    ? ((e = Ku(e, t, Et)),
      (r.__reactInternalMemoizedMergedChildContext = e),
      D(fe),
      D(le),
      I(le, e))
    : D(fe),
    I(fe, n);
}
var Ve = null,
  oa = !1,
  Oa = !1;
function Gu(e) {
  Ve === null ? (Ve = [e]) : Ve.push(e);
}
function Yd(e) {
  (oa = !0), Gu(e);
}
function mt() {
  if (!Oa && Ve !== null) {
    Oa = !0;
    var e = 0,
      t = R;
    try {
      var n = Ve;
      for (R = 1; e < n.length; e++) {
        var r = n[e];
        do r = r(!0);
        while (r !== null);
      }
      (Ve = null), (oa = !1);
    } catch (a) {
      throw (Ve !== null && (Ve = Ve.slice(e + 1)), xu(ql, mt), a);
    } finally {
      (R = t), (Oa = !1);
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
  var a = 32 - Me(r) - 1;
  (r &= ~(1 << a)), (n += 1);
  var l = 32 - Me(t) + a;
  if (30 < l) {
    var o = a - (a % 5);
    (l = (r & ((1 << o) - 1)).toString(32)),
      (r >>= o),
      (a -= o),
      ($e = (1 << (32 - Me(t) + a)) | (n << a) | r),
      (He = l + e);
  } else ($e = (1 << l) | (n << a) | r), (He = e);
}
function ro(e) {
  e.return !== null && (yt(e, 1), Ju(e, 1, 0));
}
function ao(e) {
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
var be = null,
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
function hi(e, t) {
  switch (e.tag) {
    case 5:
      var n = e.type;
      return (
        (t =
          t.nodeType !== 1 || n.toLowerCase() !== t.nodeName.toLowerCase()
            ? null
            : t),
        t !== null
          ? ((e.stateNode = t), (be = e), (ge = ot(t.firstChild)), !0)
          : !1
      );
    case 6:
      return (
        (t = e.pendingProps === '' || t.nodeType !== 3 ? null : t),
        t !== null ? ((e.stateNode = t), (be = e), (ge = null), !0) : !1
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
            (be = e),
            (ge = null),
            !0)
          : !1
      );
    default:
      return !1;
  }
}
function vl(e) {
  return (e.mode & 1) !== 0 && (e.flags & 128) === 0;
}
function wl(e) {
  if (F) {
    var t = ge;
    if (t) {
      var n = t;
      if (!hi(e, t)) {
        if (vl(e)) throw Error(b(418));
        t = ot(n.nextSibling);
        var r = be;
        t && hi(e, t)
          ? Zu(r, n)
          : ((e.flags = (e.flags & -4097) | 2), (F = !1), (be = e));
      }
    } else {
      if (vl(e)) throw Error(b(418));
      (e.flags = (e.flags & -4097) | 2), (F = !1), (be = e);
    }
  }
}
function mi(e) {
  for (
    e = e.return;
    e !== null && e.tag !== 5 && e.tag !== 3 && e.tag !== 13;

  )
    e = e.return;
  be = e;
}
function fr(e) {
  if (e !== be) return !1;
  if (!F) return mi(e), (F = !0), !1;
  var t;
  if (
    ((t = e.tag !== 3) &&
      !(t = e.tag !== 5) &&
      ((t = e.type),
      (t = t !== 'head' && t !== 'body' && !ml(e.type, e.memoizedProps))),
    t && (t = ge))
  ) {
    if (vl(e)) throw (es(), Error(b(418)));
    for (; t; ) Zu(e, t), (t = ot(t.nextSibling));
  }
  if ((mi(e), e.tag === 13)) {
    if (((e = e.memoizedState), (e = e !== null ? e.dehydrated : null), !e))
      throw Error(b(317));
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
  } else ge = be ? ot(e.stateNode.nextSibling) : null;
  return !0;
}
function es() {
  for (var e = ge; e; ) e = ot(e.nextSibling);
}
function Zt() {
  (ge = be = null), (F = !1);
}
function lo(e) {
  je === null ? (je = [e]) : je.push(e);
}
var Kd = Ye.ReactCurrentBatchConfig;
function mn(e, t, n) {
  if (
    ((e = n.ref), e !== null && typeof e != 'function' && typeof e != 'object')
  ) {
    if (n._owner) {
      if (((n = n._owner), n)) {
        if (n.tag !== 1) throw Error(b(309));
        var r = n.stateNode;
      }
      if (!r) throw Error(b(147, e));
      var a = r,
        l = '' + e;
      return t !== null &&
        t.ref !== null &&
        typeof t.ref == 'function' &&
        t.ref._stringRef === l
        ? t.ref
        : ((t = function (o) {
            var u = a.refs;
            o === null ? delete u[l] : (u[l] = o);
          }),
          (t._stringRef = l),
          t);
    }
    if (typeof e != 'string') throw Error(b(284));
    if (!n._owner) throw Error(b(290, e));
  }
  return e;
}
function pr(e, t) {
  throw (
    ((e = Object.prototype.toString.call(t)),
    Error(
      b(
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
  function t(f, s) {
    if (e) {
      var d = f.deletions;
      d === null ? ((f.deletions = [s]), (f.flags |= 16)) : d.push(s);
    }
  }
  function n(f, s) {
    if (!e) return null;
    for (; s !== null; ) t(f, s), (s = s.sibling);
    return null;
  }
  function r(f, s) {
    for (f = new Map(); s !== null; )
      s.key !== null ? f.set(s.key, s) : f.set(s.index, s), (s = s.sibling);
    return f;
  }
  function a(f, s) {
    return (f = ct(f, s)), (f.index = 0), (f.sibling = null), f;
  }
  function l(f, s, d) {
    return (
      (f.index = d),
      e
        ? ((d = f.alternate),
          d !== null
            ? ((d = d.index), d < s ? ((f.flags |= 2), s) : d)
            : ((f.flags |= 2), s))
        : ((f.flags |= 1048576), s)
    );
  }
  function o(f) {
    return e && f.alternate === null && (f.flags |= 2), f;
  }
  function u(f, s, d, y) {
    return s === null || s.tag !== 6
      ? ((s = Ha(d, f.mode, y)), (s.return = f), s)
      : ((s = a(s, d)), (s.return = f), s);
  }
  function i(f, s, d, y) {
    var _ = d.type;
    return _ === Rt
      ? h(f, s, d.props.children, y, d.key)
      : s !== null &&
        (s.elementType === _ ||
          (typeof _ == 'object' &&
            _ !== null &&
            _.$$typeof === Ge &&
            gi(_) === s.type))
      ? ((y = a(s, d.props)), (y.ref = mn(f, s, d)), (y.return = f), y)
      : ((y = Pr(d.type, d.key, d.props, null, f.mode, y)),
        (y.ref = mn(f, s, d)),
        (y.return = f),
        y);
  }
  function c(f, s, d, y) {
    return s === null ||
      s.tag !== 4 ||
      s.stateNode.containerInfo !== d.containerInfo ||
      s.stateNode.implementation !== d.implementation
      ? ((s = Ba(d, f.mode, y)), (s.return = f), s)
      : ((s = a(s, d.children || [])), (s.return = f), s);
  }
  function h(f, s, d, y, _) {
    return s === null || s.tag !== 7
      ? ((s = _t(d, f.mode, y, _)), (s.return = f), s)
      : ((s = a(s, d)), (s.return = f), s);
  }
  function m(f, s, d) {
    if ((typeof s == 'string' && s !== '') || typeof s == 'number')
      return (s = Ha('' + s, f.mode, d)), (s.return = f), s;
    if (typeof s == 'object' && s !== null) {
      switch (s.$$typeof) {
        case nr:
          return (
            (d = Pr(s.type, s.key, s.props, null, f.mode, d)),
            (d.ref = mn(f, null, s)),
            (d.return = f),
            d
          );
        case Tt:
          return (s = Ba(s, f.mode, d)), (s.return = f), s;
        case Ge:
          var y = s._init;
          return m(f, y(s._payload), d);
      }
      if (vn(s) || cn(s))
        return (s = _t(s, f.mode, d, null)), (s.return = f), s;
      pr(f, s);
    }
    return null;
  }
  function p(f, s, d, y) {
    var _ = s !== null ? s.key : null;
    if ((typeof d == 'string' && d !== '') || typeof d == 'number')
      return _ !== null ? null : u(f, s, '' + d, y);
    if (typeof d == 'object' && d !== null) {
      switch (d.$$typeof) {
        case nr:
          return d.key === _ ? i(f, s, d, y) : null;
        case Tt:
          return d.key === _ ? c(f, s, d, y) : null;
        case Ge:
          return (_ = d._init), p(f, s, _(d._payload), y);
      }
      if (vn(d) || cn(d)) return _ !== null ? null : h(f, s, d, y, null);
      pr(f, d);
    }
    return null;
  }
  function w(f, s, d, y, _) {
    if ((typeof y == 'string' && y !== '') || typeof y == 'number')
      return (f = f.get(d) || null), u(s, f, '' + y, _);
    if (typeof y == 'object' && y !== null) {
      switch (y.$$typeof) {
        case nr:
          return (
            (f = f.get(y.key === null ? d : y.key) || null), i(s, f, y, _)
          );
        case Tt:
          return (
            (f = f.get(y.key === null ? d : y.key) || null), c(s, f, y, _)
          );
        case Ge:
          var E = y._init;
          return w(f, s, d, E(y._payload), _);
      }
      if (vn(y) || cn(y)) return (f = f.get(d) || null), h(s, f, y, _, null);
      pr(s, y);
    }
    return null;
  }
  function v(f, s, d, y) {
    for (
      var _ = null, E = null, N = s, C = (s = 0), H = null;
      N !== null && C < d.length;
      C++
    ) {
      N.index > C ? ((H = N), (N = null)) : (H = N.sibling);
      var j = p(f, N, d[C], y);
      if (j === null) {
        N === null && (N = H);
        break;
      }
      e && N && j.alternate === null && t(f, N),
        (s = l(j, s, C)),
        E === null ? (_ = j) : (E.sibling = j),
        (E = j),
        (N = H);
    }
    if (C === d.length) return n(f, N), F && yt(f, C), _;
    if (N === null) {
      for (; C < d.length; C++)
        (N = m(f, d[C], y)),
          N !== null &&
            ((s = l(N, s, C)),
            E === null ? (_ = N) : (E.sibling = N),
            (E = N));
      return F && yt(f, C), _;
    }
    for (N = r(f, N); C < d.length; C++)
      (H = w(N, f, C, d[C], y)),
        H !== null &&
          (e && H.alternate !== null && N.delete(H.key === null ? C : H.key),
          (s = l(H, s, C)),
          E === null ? (_ = H) : (E.sibling = H),
          (E = H));
    return (
      e &&
        N.forEach(function (Ce) {
          return t(f, Ce);
        }),
      F && yt(f, C),
      _
    );
  }
  function k(f, s, d, y) {
    var _ = cn(d);
    if (typeof _ != 'function') throw Error(b(150));
    if (((d = _.call(d)), d == null)) throw Error(b(151));
    for (
      var E = (_ = null), N = s, C = (s = 0), H = null, j = d.next();
      N !== null && !j.done;
      C++, j = d.next()
    ) {
      N.index > C ? ((H = N), (N = null)) : (H = N.sibling);
      var Ce = p(f, N, j.value, y);
      if (Ce === null) {
        N === null && (N = H);
        break;
      }
      e && N && Ce.alternate === null && t(f, N),
        (s = l(Ce, s, C)),
        E === null ? (_ = Ce) : (E.sibling = Ce),
        (E = Ce),
        (N = H);
    }
    if (j.done) return n(f, N), F && yt(f, C), _;
    if (N === null) {
      for (; !j.done; C++, j = d.next())
        (j = m(f, j.value, y)),
          j !== null &&
            ((s = l(j, s, C)),
            E === null ? (_ = j) : (E.sibling = j),
            (E = j));
      return F && yt(f, C), _;
    }
    for (N = r(f, N); !j.done; C++, j = d.next())
      (j = w(N, f, C, j.value, y)),
        j !== null &&
          (e && j.alternate !== null && N.delete(j.key === null ? C : j.key),
          (s = l(j, s, C)),
          E === null ? (_ = j) : (E.sibling = j),
          (E = j));
    return (
      e &&
        N.forEach(function (un) {
          return t(f, un);
        }),
      F && yt(f, C),
      _
    );
  }
  function M(f, s, d, y) {
    if (
      (typeof d == 'object' &&
        d !== null &&
        d.type === Rt &&
        d.key === null &&
        (d = d.props.children),
      typeof d == 'object' && d !== null)
    ) {
      switch (d.$$typeof) {
        case nr:
          e: {
            for (var _ = d.key, E = s; E !== null; ) {
              if (E.key === _) {
                if (((_ = d.type), _ === Rt)) {
                  if (E.tag === 7) {
                    n(f, E.sibling),
                      (s = a(E, d.props.children)),
                      (s.return = f),
                      (f = s);
                    break e;
                  }
                } else if (
                  E.elementType === _ ||
                  (typeof _ == 'object' &&
                    _ !== null &&
                    _.$$typeof === Ge &&
                    gi(_) === E.type)
                ) {
                  n(f, E.sibling),
                    (s = a(E, d.props)),
                    (s.ref = mn(f, E, d)),
                    (s.return = f),
                    (f = s);
                  break e;
                }
                n(f, E);
                break;
              } else t(f, E);
              E = E.sibling;
            }
            d.type === Rt
              ? ((s = _t(d.props.children, f.mode, y, d.key)),
                (s.return = f),
                (f = s))
              : ((y = Pr(d.type, d.key, d.props, null, f.mode, y)),
                (y.ref = mn(f, s, d)),
                (y.return = f),
                (f = y));
          }
          return o(f);
        case Tt:
          e: {
            for (E = d.key; s !== null; ) {
              if (s.key === E)
                if (
                  s.tag === 4 &&
                  s.stateNode.containerInfo === d.containerInfo &&
                  s.stateNode.implementation === d.implementation
                ) {
                  n(f, s.sibling),
                    (s = a(s, d.children || [])),
                    (s.return = f),
                    (f = s);
                  break e;
                } else {
                  n(f, s);
                  break;
                }
              else t(f, s);
              s = s.sibling;
            }
            (s = Ba(d, f.mode, y)), (s.return = f), (f = s);
          }
          return o(f);
        case Ge:
          return (E = d._init), M(f, s, E(d._payload), y);
      }
      if (vn(d)) return v(f, s, d, y);
      if (cn(d)) return k(f, s, d, y);
      pr(f, d);
    }
    return (typeof d == 'string' && d !== '') || typeof d == 'number'
      ? ((d = '' + d),
        s !== null && s.tag === 6
          ? (n(f, s.sibling), (s = a(s, d)), (s.return = f), (f = s))
          : (n(f, s), (s = Ha(d, f.mode, y)), (s.return = f), (f = s)),
        o(f))
      : n(f, s);
  }
  return M;
}
var en = ts(!0),
  ns = ts(!1),
  Hr = ht(null),
  Br = null,
  $t = null,
  oo = null;
function io() {
  oo = $t = Br = null;
}
function uo(e) {
  var t = Hr.current;
  D(Hr), (e._currentValue = t);
}
function kl(e, t, n) {
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
      (e.lanes & t && (de = !0), (e.firstContext = null));
}
function Ee(e) {
  var t = e._currentValue;
  if (oo !== e)
    if (((e = { context: e, memoizedValue: t, next: null }), $t === null)) {
      if (Br === null) throw Error(b(308));
      ($t = e), (Br.dependencies = { lanes: 0, firstContext: e });
    } else $t = $t.next = e;
  return t;
}
var kt = null;
function so(e) {
  kt === null ? (kt = [e]) : kt.push(e);
}
function rs(e, t, n, r) {
  var a = t.interleaved;
  return (
    a === null ? ((n.next = n), so(t)) : ((n.next = a.next), (a.next = n)),
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
function as(e, t) {
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
  if (((r = r.shared), T & 2)) {
    var a = r.pending;
    return (
      a === null ? (t.next = t) : ((t.next = a.next), (a.next = t)),
      (r.pending = t),
      Xe(e, n)
    );
  }
  return (
    (a = r.interleaved),
    a === null ? ((t.next = t), so(r)) : ((t.next = a.next), (a.next = t)),
    (r.interleaved = t),
    Xe(e, n)
  );
}
function Sr(e, t, n) {
  if (
    ((t = t.updateQueue), t !== null && ((t = t.shared), (n & 4194240) !== 0))
  ) {
    var r = t.lanes;
    (r &= e.pendingLanes), (n |= r), (t.lanes = n), Yl(e, n);
  }
}
function bi(e, t) {
  var n = e.updateQueue,
    r = e.alternate;
  if (r !== null && ((r = r.updateQueue), n === r)) {
    var a = null,
      l = null;
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
        l === null ? (a = l = o) : (l = l.next = o), (n = n.next);
      } while (n !== null);
      l === null ? (a = l = t) : (l = l.next = t);
    } else a = l = t;
    (n = {
      baseState: r.baseState,
      firstBaseUpdate: a,
      lastBaseUpdate: l,
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
  var a = e.updateQueue;
  Je = !1;
  var l = a.firstBaseUpdate,
    o = a.lastBaseUpdate,
    u = a.shared.pending;
  if (u !== null) {
    a.shared.pending = null;
    var i = u,
      c = i.next;
    (i.next = null), o === null ? (l = c) : (o.next = c), (o = i);
    var h = e.alternate;
    h !== null &&
      ((h = h.updateQueue),
      (u = h.lastBaseUpdate),
      u !== o &&
        (u === null ? (h.firstBaseUpdate = c) : (u.next = c),
        (h.lastBaseUpdate = i)));
  }
  if (l !== null) {
    var m = a.baseState;
    (o = 0), (h = c = i = null), (u = l);
    do {
      var p = u.lane,
        w = u.eventTime;
      if ((r & p) === p) {
        h !== null &&
          (h = h.next =
            {
              eventTime: w,
              lane: 0,
              tag: u.tag,
              payload: u.payload,
              callback: u.callback,
              next: null,
            });
        e: {
          var v = e,
            k = u;
          switch (((p = t), (w = n), k.tag)) {
            case 1:
              if (((v = k.payload), typeof v == 'function')) {
                m = v.call(w, m, p);
                break e;
              }
              m = v;
              break e;
            case 3:
              v.flags = (v.flags & -65537) | 128;
            case 0:
              if (
                ((v = k.payload),
                (p = typeof v == 'function' ? v.call(w, m, p) : v),
                p == null)
              )
                break e;
              m = V({}, m, p);
              break e;
            case 2:
              Je = !0;
          }
        }
        u.callback !== null &&
          u.lane !== 0 &&
          ((e.flags |= 64),
          (p = a.effects),
          p === null ? (a.effects = [u]) : p.push(u));
      } else
        (w = {
          eventTime: w,
          lane: p,
          tag: u.tag,
          payload: u.payload,
          callback: u.callback,
          next: null,
        }),
          h === null ? ((c = h = w), (i = m)) : (h = h.next = w),
          (o |= p);
      if (((u = u.next), u === null)) {
        if (((u = a.shared.pending), u === null)) break;
        (p = u),
          (u = p.next),
          (p.next = null),
          (a.lastBaseUpdate = p),
          (a.shared.pending = null);
      }
    } while (!0);
    if (
      (h === null && (i = m),
      (a.baseState = i),
      (a.firstBaseUpdate = c),
      (a.lastBaseUpdate = h),
      (t = a.shared.interleaved),
      t !== null)
    ) {
      a = t;
      do (o |= a.lane), (a = a.next);
      while (a !== t);
    } else l === null && (a.shared.lanes = 0);
    (zt |= o), (e.lanes = o), (e.memoizedState = m);
  }
}
function yi(e, t, n) {
  if (((e = t.effects), (t.effects = null), e !== null))
    for (t = 0; t < e.length; t++) {
      var r = e[t],
        a = r.callback;
      if (a !== null) {
        if (((r.callback = null), (r = n), typeof a != 'function'))
          throw Error(b(191, a));
        a.call(r);
      }
    }
}
var Jn = {},
  Ue = ht(Jn),
  $n = ht(Jn),
  Hn = ht(Jn);
function xt(e) {
  if (e === Jn) throw Error(b(174));
  return e;
}
function fo(e, t) {
  switch ((I(Hn, t), I($n, e), I(Ue, Jn), (e = t.nodeType), e)) {
    case 9:
    case 11:
      t = (t = t.documentElement) ? t.namespaceURI : tl(null, '');
      break;
    default:
      (e = e === 8 ? t.parentNode : t),
        (t = e.namespaceURI || null),
        (e = e.tagName),
        (t = tl(t, e));
  }
  D(Ue), I(Ue, t);
}
function tn() {
  D(Ue), D($n), D(Hn);
}
function ls(e) {
  xt(Hn.current);
  var t = xt(Ue.current),
    n = tl(t, e.type);
  t !== n && (I($n, e), I(Ue, n));
}
function po(e) {
  $n.current === e && (D(Ue), D($n));
}
var U = ht(0);
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
var Da = [];
function ho() {
  for (var e = 0; e < Da.length; e++)
    Da[e]._workInProgressVersionPrimary = null;
  Da.length = 0;
}
var _r = Ye.ReactCurrentDispatcher,
  Fa = Ye.ReactCurrentBatchConfig,
  Ct = 0,
  A = null,
  X = null,
  K = null,
  Xr = !1,
  Cn = !1,
  Bn = 0,
  Gd = 0;
function ne() {
  throw Error(b(321));
}
function mo(e, t) {
  if (t === null) return !1;
  for (var n = 0; n < t.length && n < e.length; n++)
    if (!Re(e[n], t[n])) return !1;
  return !0;
}
function go(e, t, n, r, a, l) {
  if (
    ((Ct = l),
    (A = t),
    (t.memoizedState = null),
    (t.updateQueue = null),
    (t.lanes = 0),
    (_r.current = e === null || e.memoizedState === null ? tf : nf),
    (e = n(r, a)),
    Cn)
  ) {
    l = 0;
    do {
      if (((Cn = !1), (Bn = 0), 25 <= l)) throw Error(b(301));
      (l += 1),
        (K = X = null),
        (t.updateQueue = null),
        (_r.current = rf),
        (e = n(r, a));
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
    throw Error(b(300));
  return e;
}
function bo() {
  var e = Bn !== 0;
  return (Bn = 0), e;
}
function Oe() {
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
    if (e === null) throw Error(b(310));
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
function Ua(e) {
  var t = Ne(),
    n = t.queue;
  if (n === null) throw Error(b(311));
  n.lastRenderedReducer = e;
  var r = X,
    a = r.baseQueue,
    l = n.pending;
  if (l !== null) {
    if (a !== null) {
      var o = a.next;
      (a.next = l.next), (l.next = o);
    }
    (r.baseQueue = a = l), (n.pending = null);
  }
  if (a !== null) {
    (l = a.next), (r = r.baseState);
    var u = (o = null),
      i = null,
      c = l;
    do {
      var h = c.lane;
      if ((Ct & h) === h)
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
        var m = {
          lane: h,
          action: c.action,
          hasEagerState: c.hasEagerState,
          eagerState: c.eagerState,
          next: null,
        };
        i === null ? ((u = i = m), (o = r)) : (i = i.next = m),
          (A.lanes |= h),
          (zt |= h);
      }
      c = c.next;
    } while (c !== null && c !== l);
    i === null ? (o = r) : (i.next = u),
      Re(r, t.memoizedState) || (de = !0),
      (t.memoizedState = r),
      (t.baseState = o),
      (t.baseQueue = i),
      (n.lastRenderedState = r);
  }
  if (((e = n.interleaved), e !== null)) {
    a = e;
    do (l = a.lane), (A.lanes |= l), (zt |= l), (a = a.next);
    while (a !== e);
  } else a === null && (n.lanes = 0);
  return [t.memoizedState, n.dispatch];
}
function Aa(e) {
  var t = Ne(),
    n = t.queue;
  if (n === null) throw Error(b(311));
  n.lastRenderedReducer = e;
  var r = n.dispatch,
    a = n.pending,
    l = t.memoizedState;
  if (a !== null) {
    n.pending = null;
    var o = (a = a.next);
    do (l = e(l, o.action)), (o = o.next);
    while (o !== a);
    Re(l, t.memoizedState) || (de = !0),
      (t.memoizedState = l),
      t.baseQueue === null && (t.baseState = l),
      (n.lastRenderedState = l);
  }
  return [l, r];
}
function os() {}
function is(e, t) {
  var n = A,
    r = Ne(),
    a = t(),
    l = !Re(r.memoizedState, a);
  if (
    (l && ((r.memoizedState = a), (de = !0)),
    (r = r.queue),
    yo(cs.bind(null, n, r, e), [e]),
    r.getSnapshot !== t || l || (K !== null && K.memoizedState.tag & 1))
  ) {
    if (
      ((n.flags |= 2048),
      Qn(9, ss.bind(null, n, r, a, t), void 0, null),
      G === null)
    )
      throw Error(b(349));
    Ct & 30 || us(n, t, a);
  }
  return a;
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
  (t.value = n), (t.getSnapshot = r), ds(t) && fs(e);
}
function cs(e, t, n) {
  return n(function () {
    ds(t) && fs(e);
  });
}
function ds(e) {
  var t = e.getSnapshot;
  e = e.value;
  try {
    var n = t();
    return !Re(e, n);
  } catch {
    return !0;
  }
}
function fs(e) {
  var t = Xe(e, 1);
  t !== null && Te(t, e, 1, -1);
}
function vi(e) {
  var t = Oe();
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
    (e = e.dispatch = ef.bind(null, A, e)),
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
  var a = Oe();
  (A.flags |= e),
    (a.memoizedState = Qn(1 | t, n, void 0, r === void 0 ? null : r));
}
function ia(e, t, n, r) {
  var a = Ne();
  r = r === void 0 ? null : r;
  var l = void 0;
  if (X !== null) {
    var o = X.memoizedState;
    if (((l = o.destroy), r !== null && mo(r, o.deps))) {
      a.memoizedState = Qn(t, n, l, r);
      return;
    }
  }
  (A.flags |= e), (a.memoizedState = Qn(1 | t, n, l, r));
}
function wi(e, t) {
  return Er(8390656, 8, e, t);
}
function yo(e, t) {
  return ia(2048, 8, e, t);
}
function hs(e, t) {
  return ia(4, 2, e, t);
}
function ms(e, t) {
  return ia(4, 4, e, t);
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
function bs(e, t, n) {
  return (
    (n = n != null ? n.concat([e]) : null), ia(4, 4, gs.bind(null, t, e), n)
  );
}
function vo() {}
function ys(e, t) {
  var n = Ne();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && mo(t, r[1])
    ? r[0]
    : ((n.memoizedState = [e, t]), e);
}
function vs(e, t) {
  var n = Ne();
  t = t === void 0 ? null : t;
  var r = n.memoizedState;
  return r !== null && t !== null && mo(t, r[1])
    ? r[0]
    : ((e = e()), (n.memoizedState = [e, t]), e);
}
function ws(e, t, n) {
  return Ct & 21
    ? (Re(n, t) || ((n = Eu()), (A.lanes |= n), (zt |= n), (e.baseState = !0)),
      t)
    : (e.baseState && ((e.baseState = !1), (de = !0)), (e.memoizedState = n));
}
function Jd(e, t) {
  var n = R;
  (R = n !== 0 && 4 > n ? n : 4), e(!0);
  var r = Fa.transition;
  Fa.transition = {};
  try {
    e(!1), t();
  } finally {
    (R = n), (Fa.transition = r);
  }
}
function ks() {
  return Ne().memoizedState;
}
function Zd(e, t, n) {
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
    var a = ie();
    Te(n, e, r, a), _s(n, t, r);
  }
}
function ef(e, t, n) {
  var r = st(e),
    a = {
      lane: r,
      action: n,
      hasEagerState: !1,
      eagerState: null,
      next: null,
    };
  if (xs(e)) Ss(t, a);
  else {
    var l = e.alternate;
    if (
      e.lanes === 0 &&
      (l === null || l.lanes === 0) &&
      ((l = t.lastRenderedReducer), l !== null)
    )
      try {
        var o = t.lastRenderedState,
          u = l(o, n);
        if (((a.hasEagerState = !0), (a.eagerState = u), Re(u, o))) {
          var i = t.interleaved;
          i === null
            ? ((a.next = a), so(t))
            : ((a.next = i.next), (i.next = a)),
            (t.interleaved = a);
          return;
        }
      } catch {
      } finally {
      }
    (n = rs(e, t, a, r)),
      n !== null && ((a = ie()), Te(n, e, r, a), _s(n, t, r));
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
    (r &= e.pendingLanes), (n |= r), (t.lanes = n), Yl(e, n);
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
  tf = {
    readContext: Ee,
    useCallback: function (e, t) {
      return (Oe().memoizedState = [e, t === void 0 ? null : t]), e;
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
      var n = Oe();
      return (
        (t = t === void 0 ? null : t), (e = e()), (n.memoizedState = [e, t]), e
      );
    },
    useReducer: function (e, t, n) {
      var r = Oe();
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
        (e = e.dispatch = Zd.bind(null, A, e)),
        [r.memoizedState, e]
      );
    },
    useRef: function (e) {
      var t = Oe();
      return (e = { current: e }), (t.memoizedState = e);
    },
    useState: vi,
    useDebugValue: vo,
    useDeferredValue: function (e) {
      return (Oe().memoizedState = e);
    },
    useTransition: function () {
      var e = vi(!1),
        t = e[0];
      return (e = Jd.bind(null, e[1])), (Oe().memoizedState = e), [t, e];
    },
    useMutableSource: function () {},
    useSyncExternalStore: function (e, t, n) {
      var r = A,
        a = Oe();
      if (F) {
        if (n === void 0) throw Error(b(407));
        n = n();
      } else {
        if (((n = t()), G === null)) throw Error(b(349));
        Ct & 30 || us(r, t, n);
      }
      a.memoizedState = n;
      var l = { value: n, getSnapshot: t };
      return (
        (a.queue = l),
        wi(cs.bind(null, r, l, e), [e]),
        (r.flags |= 2048),
        Qn(9, ss.bind(null, r, l, n, t), void 0, null),
        n
      );
    },
    useId: function () {
      var e = Oe(),
        t = G.identifierPrefix;
      if (F) {
        var n = He,
          r = $e;
        (n = (r & ~(1 << (32 - Me(r) - 1))).toString(32) + n),
          (t = ':' + t + 'R' + n),
          (n = Bn++),
          0 < n && (t += 'H' + n.toString(32)),
          (t += ':');
      } else (n = Gd++), (t = ':' + t + 'r' + n.toString(32) + ':');
      return (e.memoizedState = t);
    },
    unstable_isNewReconciler: !1,
  },
  nf = {
    readContext: Ee,
    useCallback: ys,
    useContext: Ee,
    useEffect: yo,
    useImperativeHandle: bs,
    useInsertionEffect: hs,
    useLayoutEffect: ms,
    useMemo: vs,
    useReducer: Ua,
    useRef: ps,
    useState: function () {
      return Ua(Wn);
    },
    useDebugValue: vo,
    useDeferredValue: function (e) {
      var t = Ne();
      return ws(t, X.memoizedState, e);
    },
    useTransition: function () {
      var e = Ua(Wn)[0],
        t = Ne().memoizedState;
      return [e, t];
    },
    useMutableSource: os,
    useSyncExternalStore: is,
    useId: ks,
    unstable_isNewReconciler: !1,
  },
  rf = {
    readContext: Ee,
    useCallback: ys,
    useContext: Ee,
    useEffect: yo,
    useImperativeHandle: bs,
    useInsertionEffect: hs,
    useLayoutEffect: ms,
    useMemo: vs,
    useReducer: Aa,
    useRef: ps,
    useState: function () {
      return Aa(Wn);
    },
    useDebugValue: vo,
    useDeferredValue: function (e) {
      var t = Ne();
      return X === null ? (t.memoizedState = e) : ws(t, X.memoizedState, e);
    },
    useTransition: function () {
      var e = Aa(Wn)[0],
        t = Ne().memoizedState;
      return [e, t];
    },
    useMutableSource: os,
    useSyncExternalStore: is,
    useId: ks,
    unstable_isNewReconciler: !1,
  };
function Pe(e, t) {
  if (e && e.defaultProps) {
    (t = V({}, t)), (e = e.defaultProps);
    for (var n in e) t[n] === void 0 && (t[n] = e[n]);
    return t;
  }
  return t;
}
function xl(e, t, n, r) {
  (t = e.memoizedState),
    (n = n(r, t)),
    (n = n == null ? t : V({}, t, n)),
    (e.memoizedState = n),
    e.lanes === 0 && (e.updateQueue.baseState = n);
}
var ua = {
  isMounted: function (e) {
    return (e = e._reactInternals) ? jt(e) === e : !1;
  },
  enqueueSetState: function (e, t, n) {
    e = e._reactInternals;
    var r = ie(),
      a = st(e),
      l = Be(r, a);
    (l.payload = t),
      n != null && (l.callback = n),
      (t = it(e, l, a)),
      t !== null && (Te(t, e, a, r), Sr(t, e, a));
  },
  enqueueReplaceState: function (e, t, n) {
    e = e._reactInternals;
    var r = ie(),
      a = st(e),
      l = Be(r, a);
    (l.tag = 1),
      (l.payload = t),
      n != null && (l.callback = n),
      (t = it(e, l, a)),
      t !== null && (Te(t, e, a, r), Sr(t, e, a));
  },
  enqueueForceUpdate: function (e, t) {
    e = e._reactInternals;
    var n = ie(),
      r = st(e),
      a = Be(n, r);
    (a.tag = 2),
      t != null && (a.callback = t),
      (t = it(e, a, r)),
      t !== null && (Te(t, e, r, n), Sr(t, e, r));
  },
};
function ki(e, t, n, r, a, l, o) {
  return (
    (e = e.stateNode),
    typeof e.shouldComponentUpdate == 'function'
      ? e.shouldComponentUpdate(r, l, o)
      : t.prototype && t.prototype.isPureReactComponent
      ? !Fn(n, r) || !Fn(a, l)
      : !0
  );
}
function Es(e, t, n) {
  var r = !1,
    a = ft,
    l = t.contextType;
  return (
    typeof l == 'object' && l !== null
      ? (l = Ee(l))
      : ((a = pe(t) ? Et : le.current),
        (r = t.contextTypes),
        (l = (r = r != null) ? Jt(e, a) : ft)),
    (t = new t(n, l)),
    (e.memoizedState =
      t.state !== null && t.state !== void 0 ? t.state : null),
    (t.updater = ua),
    (e.stateNode = t),
    (t._reactInternals = e),
    r &&
      ((e = e.stateNode),
      (e.__reactInternalMemoizedUnmaskedChildContext = a),
      (e.__reactInternalMemoizedMaskedChildContext = l)),
    t
  );
}
function xi(e, t, n, r) {
  (e = t.state),
    typeof t.componentWillReceiveProps == 'function' &&
      t.componentWillReceiveProps(n, r),
    typeof t.UNSAFE_componentWillReceiveProps == 'function' &&
      t.UNSAFE_componentWillReceiveProps(n, r),
    t.state !== e && ua.enqueueReplaceState(t, t.state, null);
}
function Sl(e, t, n, r) {
  var a = e.stateNode;
  (a.props = n), (a.state = e.memoizedState), (a.refs = {}), co(e);
  var l = t.contextType;
  typeof l == 'object' && l !== null
    ? (a.context = Ee(l))
    : ((l = pe(t) ? Et : le.current), (a.context = Jt(e, l))),
    (a.state = e.memoizedState),
    (l = t.getDerivedStateFromProps),
    typeof l == 'function' && (xl(e, t, l, n), (a.state = e.memoizedState)),
    typeof t.getDerivedStateFromProps == 'function' ||
      typeof a.getSnapshotBeforeUpdate == 'function' ||
      (typeof a.UNSAFE_componentWillMount != 'function' &&
        typeof a.componentWillMount != 'function') ||
      ((t = a.state),
      typeof a.componentWillMount == 'function' && a.componentWillMount(),
      typeof a.UNSAFE_componentWillMount == 'function' &&
        a.UNSAFE_componentWillMount(),
      t !== a.state && ua.enqueueReplaceState(a, a.state, null),
      Wr(e, n, a, r),
      (a.state = e.memoizedState)),
    typeof a.componentDidMount == 'function' && (e.flags |= 4194308);
}
function nn(e, t) {
  try {
    var n = '',
      r = t;
    do (n += jc(r)), (r = r.return);
    while (r);
    var a = n;
  } catch (l) {
    a =
      `
Error generating stack: ` +
      l.message +
      `
` +
      l.stack;
  }
  return { value: e, source: t, stack: a, digest: null };
}
function Va(e, t, n) {
  return { value: e, source: null, stack: n ?? null, digest: t ?? null };
}
function _l(e, t) {
  try {
    console.error(t.value);
  } catch (n) {
    setTimeout(function () {
      throw n;
    });
  }
}
var af = typeof WeakMap == 'function' ? WeakMap : Map;
function Ns(e, t, n) {
  (n = Be(-1, n)), (n.tag = 3), (n.payload = { element: null });
  var r = t.value;
  return (
    (n.callback = function () {
      Kr || ((Kr = !0), (Tl = r)), _l(e, t);
    }),
    n
  );
}
function Cs(e, t, n) {
  (n = Be(-1, n)), (n.tag = 3);
  var r = e.type.getDerivedStateFromError;
  if (typeof r == 'function') {
    var a = t.value;
    (n.payload = function () {
      return r(a);
    }),
      (n.callback = function () {
        _l(e, t);
      });
  }
  var l = e.stateNode;
  return (
    l !== null &&
      typeof l.componentDidCatch == 'function' &&
      (n.callback = function () {
        _l(e, t),
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
    r = e.pingCache = new af();
    var a = new Set();
    r.set(t, a);
  } else (a = r.get(t)), a === void 0 && ((a = new Set()), r.set(t, a));
  a.has(n) || (a.add(n), (e = vf.bind(null, e, t, n)), t.then(e, e));
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
function Ei(e, t, n, r, a) {
  return e.mode & 1
    ? ((e.flags |= 65536), (e.lanes = a), e)
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
var lf = Ye.ReactCurrentOwner,
  de = !1;
function oe(e, t, n, r) {
  t.child = e === null ? ns(t, null, n, r) : en(t, e.child, n, r);
}
function Ni(e, t, n, r, a) {
  n = n.render;
  var l = t.ref;
  return (
    Yt(t, a),
    (r = go(e, t, n, r, l, a)),
    (n = bo()),
    e !== null && !de
      ? ((t.updateQueue = e.updateQueue),
        (t.flags &= -2053),
        (e.lanes &= ~a),
        qe(e, t, a))
      : (F && n && ro(t), (t.flags |= 1), oe(e, t, r, a), t.child)
  );
}
function Ci(e, t, n, r, a) {
  if (e === null) {
    var l = n.type;
    return typeof l == 'function' &&
      !Co(l) &&
      l.defaultProps === void 0 &&
      n.compare === null &&
      n.defaultProps === void 0
      ? ((t.tag = 15), (t.type = l), zs(e, t, l, r, a))
      : ((e = Pr(n.type, null, r, t, t.mode, a)),
        (e.ref = t.ref),
        (e.return = t),
        (t.child = e));
  }
  if (((l = e.child), !(e.lanes & a))) {
    var o = l.memoizedProps;
    if (
      ((n = n.compare), (n = n !== null ? n : Fn), n(o, r) && e.ref === t.ref)
    )
      return qe(e, t, a);
  }
  return (
    (t.flags |= 1),
    (e = ct(l, r)),
    (e.ref = t.ref),
    (e.return = t),
    (t.child = e)
  );
}
function zs(e, t, n, r, a) {
  if (e !== null) {
    var l = e.memoizedProps;
    if (Fn(l, r) && e.ref === t.ref)
      if (((de = !1), (t.pendingProps = r = l), (e.lanes & a) !== 0))
        e.flags & 131072 && (de = !0);
      else return (t.lanes = e.lanes), qe(e, t, a);
  }
  return El(e, t, n, r, a);
}
function Ps(e, t, n) {
  var r = t.pendingProps,
    a = r.children,
    l = e !== null ? e.memoizedState : null;
  if (r.mode === 'hidden')
    if (!(t.mode & 1))
      (t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }),
        I(Bt, me),
        (me |= n);
    else {
      if (!(n & 1073741824))
        return (
          (e = l !== null ? l.baseLanes | n : n),
          (t.lanes = t.childLanes = 1073741824),
          (t.memoizedState = {
            baseLanes: e,
            cachePool: null,
            transitions: null,
          }),
          (t.updateQueue = null),
          I(Bt, me),
          (me |= e),
          null
        );
      (t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }),
        (r = l !== null ? l.baseLanes : n),
        I(Bt, me),
        (me |= r);
    }
  else
    l !== null ? ((r = l.baseLanes | n), (t.memoizedState = null)) : (r = n),
      I(Bt, me),
      (me |= r);
  return oe(e, t, a, n), t.child;
}
function Ls(e, t) {
  var n = t.ref;
  ((e === null && n !== null) || (e !== null && e.ref !== n)) &&
    ((t.flags |= 512), (t.flags |= 2097152));
}
function El(e, t, n, r, a) {
  var l = pe(n) ? Et : le.current;
  return (
    (l = Jt(t, l)),
    Yt(t, a),
    (n = go(e, t, n, r, l, a)),
    (r = bo()),
    e !== null && !de
      ? ((t.updateQueue = e.updateQueue),
        (t.flags &= -2053),
        (e.lanes &= ~a),
        qe(e, t, a))
      : (F && r && ro(t), (t.flags |= 1), oe(e, t, n, a), t.child)
  );
}
function zi(e, t, n, r, a) {
  if (pe(n)) {
    var l = !0;
    Ar(t);
  } else l = !1;
  if ((Yt(t, a), t.stateNode === null))
    Nr(e, t), Es(t, n, r), Sl(t, n, r, a), (r = !0);
  else if (e === null) {
    var o = t.stateNode,
      u = t.memoizedProps;
    o.props = u;
    var i = o.context,
      c = n.contextType;
    typeof c == 'object' && c !== null
      ? (c = Ee(c))
      : ((c = pe(n) ? Et : le.current), (c = Jt(t, c)));
    var h = n.getDerivedStateFromProps,
      m =
        typeof h == 'function' ||
        typeof o.getSnapshotBeforeUpdate == 'function';
    m ||
      (typeof o.UNSAFE_componentWillReceiveProps != 'function' &&
        typeof o.componentWillReceiveProps != 'function') ||
      ((u !== r || i !== c) && xi(t, o, r, c)),
      (Je = !1);
    var p = t.memoizedState;
    (o.state = p),
      Wr(t, r, o, a),
      (i = t.memoizedState),
      u !== r || p !== i || fe.current || Je
        ? (typeof h == 'function' && (xl(t, n, h, r), (i = t.memoizedState)),
          (u = Je || ki(t, n, u, r, p, i, c))
            ? (m ||
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
      as(e, t),
      (u = t.memoizedProps),
      (c = t.type === t.elementType ? u : Pe(t.type, u)),
      (o.props = c),
      (m = t.pendingProps),
      (p = o.context),
      (i = n.contextType),
      typeof i == 'object' && i !== null
        ? (i = Ee(i))
        : ((i = pe(n) ? Et : le.current), (i = Jt(t, i)));
    var w = n.getDerivedStateFromProps;
    (h =
      typeof w == 'function' ||
      typeof o.getSnapshotBeforeUpdate == 'function') ||
      (typeof o.UNSAFE_componentWillReceiveProps != 'function' &&
        typeof o.componentWillReceiveProps != 'function') ||
      ((u !== m || p !== i) && xi(t, o, r, i)),
      (Je = !1),
      (p = t.memoizedState),
      (o.state = p),
      Wr(t, r, o, a);
    var v = t.memoizedState;
    u !== m || p !== v || fe.current || Je
      ? (typeof w == 'function' && (xl(t, n, w, r), (v = t.memoizedState)),
        (c = Je || ki(t, n, c, r, p, v, i) || !1)
          ? (h ||
              (typeof o.UNSAFE_componentWillUpdate != 'function' &&
                typeof o.componentWillUpdate != 'function') ||
              (typeof o.componentWillUpdate == 'function' &&
                o.componentWillUpdate(r, v, i),
              typeof o.UNSAFE_componentWillUpdate == 'function' &&
                o.UNSAFE_componentWillUpdate(r, v, i)),
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
            (t.memoizedState = v)),
        (o.props = r),
        (o.state = v),
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
  return Nl(e, t, n, r, l, a);
}
function Nl(e, t, n, r, a, l) {
  Ls(e, t);
  var o = (t.flags & 128) !== 0;
  if (!r && !o) return a && pi(t, n, !1), qe(e, t, l);
  (r = t.stateNode), (lf.current = t);
  var u =
    o && typeof n.getDerivedStateFromError != 'function' ? null : r.render();
  return (
    (t.flags |= 1),
    e !== null && o
      ? ((t.child = en(t, e.child, null, l)), (t.child = en(t, null, u, l)))
      : oe(e, t, u, l),
    (t.memoizedState = r.state),
    a && pi(t, n, !0),
    t.child
  );
}
function js(e) {
  var t = e.stateNode;
  t.pendingContext
    ? fi(e, t.pendingContext, t.pendingContext !== t.context)
    : t.context && fi(e, t.context, !1),
    fo(e, t.containerInfo);
}
function Pi(e, t, n, r, a) {
  return Zt(), lo(a), (t.flags |= 256), oe(e, t, n, r), t.child;
}
var Cl = { dehydrated: null, treeContext: null, retryLane: 0 };
function zl(e) {
  return { baseLanes: e, cachePool: null, transitions: null };
}
function Ms(e, t, n) {
  var r = t.pendingProps,
    a = U.current,
    l = !1,
    o = (t.flags & 128) !== 0,
    u;
  if (
    ((u = o) ||
      (u = e !== null && e.memoizedState === null ? !1 : (a & 2) !== 0),
    u
      ? ((l = !0), (t.flags &= -129))
      : (e === null || e.memoizedState !== null) && (a |= 1),
    I(U, a & 1),
    e === null)
  )
    return (
      wl(t),
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
          l
            ? ((r = t.mode),
              (l = t.child),
              (o = { mode: 'hidden', children: o }),
              !(r & 1) && l !== null
                ? ((l.childLanes = 0), (l.pendingProps = o))
                : (l = da(o, r, 0, null)),
              (e = _t(e, r, n, null)),
              (l.return = t),
              (e.return = t),
              (l.sibling = e),
              (t.child = l),
              (t.child.memoizedState = zl(n)),
              (t.memoizedState = Cl),
              e)
            : wo(t, o))
    );
  if (((a = e.memoizedState), a !== null && ((u = a.dehydrated), u !== null)))
    return of(e, t, o, r, u, a, n);
  if (l) {
    (l = r.fallback), (o = t.mode), (a = e.child), (u = a.sibling);
    var i = { mode: 'hidden', children: r.children };
    return (
      !(o & 1) && t.child !== a
        ? ((r = t.child),
          (r.childLanes = 0),
          (r.pendingProps = i),
          (t.deletions = null))
        : ((r = ct(a, i)), (r.subtreeFlags = a.subtreeFlags & 14680064)),
      u !== null ? (l = ct(u, l)) : ((l = _t(l, o, n, null)), (l.flags |= 2)),
      (l.return = t),
      (r.return = t),
      (r.sibling = l),
      (t.child = r),
      (r = l),
      (l = t.child),
      (o = e.child.memoizedState),
      (o =
        o === null
          ? zl(n)
          : {
              baseLanes: o.baseLanes | n,
              cachePool: null,
              transitions: o.transitions,
            }),
      (l.memoizedState = o),
      (l.childLanes = e.childLanes & ~n),
      (t.memoizedState = Cl),
      r
    );
  }
  return (
    (l = e.child),
    (e = l.sibling),
    (r = ct(l, { mode: 'visible', children: r.children })),
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
    (t = da({ mode: 'visible', children: t }, e.mode, 0, null)),
    (t.return = e),
    (e.child = t)
  );
}
function hr(e, t, n, r) {
  return (
    r !== null && lo(r),
    en(t, e.child, null, n),
    (e = wo(t, t.pendingProps.children)),
    (e.flags |= 2),
    (t.memoizedState = null),
    e
  );
}
function of(e, t, n, r, a, l, o) {
  if (n)
    return t.flags & 256
      ? ((t.flags &= -257), (r = Va(Error(b(422)))), hr(e, t, o, r))
      : t.memoizedState !== null
      ? ((t.child = e.child), (t.flags |= 128), null)
      : ((l = r.fallback),
        (a = t.mode),
        (r = da({ mode: 'visible', children: r.children }, a, 0, null)),
        (l = _t(l, a, o, null)),
        (l.flags |= 2),
        (r.return = t),
        (l.return = t),
        (r.sibling = l),
        (t.child = r),
        t.mode & 1 && en(t, e.child, null, o),
        (t.child.memoizedState = zl(o)),
        (t.memoizedState = Cl),
        l);
  if (!(t.mode & 1)) return hr(e, t, o, null);
  if (a.data === '$!') {
    if (((r = a.nextSibling && a.nextSibling.dataset), r)) var u = r.dgst;
    return (
      (r = u), (l = Error(b(419))), (r = Va(l, r, void 0)), hr(e, t, o, r)
    );
  }
  if (((u = (o & e.childLanes) !== 0), de || u)) {
    if (((r = G), r !== null)) {
      switch (o & -o) {
        case 4:
          a = 2;
          break;
        case 16:
          a = 8;
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
          a = 32;
          break;
        case 536870912:
          a = 268435456;
          break;
        default:
          a = 0;
      }
      (a = a & (r.suspendedLanes | o) ? 0 : a),
        a !== 0 &&
          a !== l.retryLane &&
          ((l.retryLane = a), Xe(e, a), Te(r, e, a, -1));
    }
    return No(), (r = Va(Error(b(421)))), hr(e, t, o, r);
  }
  return a.data === '$?'
    ? ((t.flags |= 128),
      (t.child = e.child),
      (t = wf.bind(null, e)),
      (a._reactRetry = t),
      null)
    : ((e = l.treeContext),
      (ge = ot(a.nextSibling)),
      (be = t),
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
function Li(e, t, n) {
  e.lanes |= t;
  var r = e.alternate;
  r !== null && (r.lanes |= t), kl(e.return, t, n);
}
function $a(e, t, n, r, a) {
  var l = e.memoizedState;
  l === null
    ? (e.memoizedState = {
        isBackwards: t,
        rendering: null,
        renderingStartTime: 0,
        last: r,
        tail: n,
        tailMode: a,
      })
    : ((l.isBackwards = t),
      (l.rendering = null),
      (l.renderingStartTime = 0),
      (l.last = r),
      (l.tail = n),
      (l.tailMode = a));
}
function Ts(e, t, n) {
  var r = t.pendingProps,
    a = r.revealOrder,
    l = r.tail;
  if ((oe(e, t, r.children, n), (r = U.current), r & 2))
    (r = (r & 1) | 2), (t.flags |= 128);
  else {
    if (e !== null && e.flags & 128)
      e: for (e = t.child; e !== null; ) {
        if (e.tag === 13) e.memoizedState !== null && Li(e, n, t);
        else if (e.tag === 19) Li(e, n, t);
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
  if ((I(U, r), !(t.mode & 1))) t.memoizedState = null;
  else
    switch (a) {
      case 'forwards':
        for (n = t.child, a = null; n !== null; )
          (e = n.alternate),
            e !== null && Qr(e) === null && (a = n),
            (n = n.sibling);
        (n = a),
          n === null
            ? ((a = t.child), (t.child = null))
            : ((a = n.sibling), (n.sibling = null)),
          $a(t, !1, a, n, l);
        break;
      case 'backwards':
        for (n = null, a = t.child, t.child = null; a !== null; ) {
          if (((e = a.alternate), e !== null && Qr(e) === null)) {
            t.child = a;
            break;
          }
          (e = a.sibling), (a.sibling = n), (n = a), (a = e);
        }
        $a(t, !0, n, null, l);
        break;
      case 'together':
        $a(t, !1, null, null, void 0);
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
    (zt |= t.lanes),
    !(n & t.childLanes))
  )
    return null;
  if (e !== null && t.child !== e.child) throw Error(b(153));
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
function uf(e, t, n) {
  switch (t.tag) {
    case 3:
      js(t), Zt();
      break;
    case 5:
      ls(t);
      break;
    case 1:
      pe(t.type) && Ar(t);
      break;
    case 4:
      fo(t, t.stateNode.containerInfo);
      break;
    case 10:
      var r = t.type._context,
        a = t.memoizedProps.value;
      I(Hr, r._currentValue), (r._currentValue = a);
      break;
    case 13:
      if (((r = t.memoizedState), r !== null))
        return r.dehydrated !== null
          ? (I(U, U.current & 1), (t.flags |= 128), null)
          : n & t.child.childLanes
          ? Ms(e, t, n)
          : (I(U, U.current & 1),
            (e = qe(e, t, n)),
            e !== null ? e.sibling : null);
      I(U, U.current & 1);
      break;
    case 19:
      if (((r = (n & t.childLanes) !== 0), e.flags & 128)) {
        if (r) return Ts(e, t, n);
        t.flags |= 128;
      }
      if (
        ((a = t.memoizedState),
        a !== null &&
          ((a.rendering = null), (a.tail = null), (a.lastEffect = null)),
        I(U, U.current),
        r)
      )
        break;
      return null;
    case 22:
    case 23:
      return (t.lanes = 0), Ps(e, t, n);
  }
  return qe(e, t, n);
}
var Rs, Pl, Is, Os;
Rs = function (e, t) {
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
Pl = function () {};
Is = function (e, t, n, r) {
  var a = e.memoizedProps;
  if (a !== r) {
    (e = t.stateNode), xt(Ue.current);
    var l = null;
    switch (n) {
      case 'input':
        (a = Ga(e, a)), (r = Ga(e, r)), (l = []);
        break;
      case 'select':
        (a = V({}, a, { value: void 0 })),
          (r = V({}, r, { value: void 0 })),
          (l = []);
        break;
      case 'textarea':
        (a = el(e, a)), (r = el(e, r)), (l = []);
        break;
      default:
        typeof a.onClick != 'function' &&
          typeof r.onClick == 'function' &&
          (e.onclick = Fr);
    }
    nl(n, r);
    var o;
    n = null;
    for (c in a)
      if (!r.hasOwnProperty(c) && a.hasOwnProperty(c) && a[c] != null)
        if (c === 'style') {
          var u = a[c];
          for (o in u) u.hasOwnProperty(o) && (n || (n = {}), (n[o] = ''));
        } else
          c !== 'dangerouslySetInnerHTML' &&
            c !== 'children' &&
            c !== 'suppressContentEditableWarning' &&
            c !== 'suppressHydrationWarning' &&
            c !== 'autoFocus' &&
            (jn.hasOwnProperty(c)
              ? l || (l = [])
              : (l = l || []).push(c, null));
    for (c in r) {
      var i = r[c];
      if (
        ((u = a != null ? a[c] : void 0),
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
          } else n || (l || (l = []), l.push(c, n)), (n = i);
        else
          c === 'dangerouslySetInnerHTML'
            ? ((i = i ? i.__html : void 0),
              (u = u ? u.__html : void 0),
              i != null && u !== i && (l = l || []).push(c, i))
            : c === 'children'
            ? (typeof i != 'string' && typeof i != 'number') ||
              (l = l || []).push(c, '' + i)
            : c !== 'suppressContentEditableWarning' &&
              c !== 'suppressHydrationWarning' &&
              (jn.hasOwnProperty(c)
                ? (i != null && c === 'onScroll' && O('scroll', e),
                  l || u === i || (l = []))
                : (l = l || []).push(c, i));
    }
    n && (l = l || []).push('style', n);
    var c = l;
    (t.updateQueue = c) && (t.flags |= 4);
  }
};
Os = function (e, t, n, r) {
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
    for (var a = e.child; a !== null; )
      (n |= a.lanes | a.childLanes),
        (r |= a.subtreeFlags & 14680064),
        (r |= a.flags & 14680064),
        (a.return = e),
        (a = a.sibling);
  else
    for (a = e.child; a !== null; )
      (n |= a.lanes | a.childLanes),
        (r |= a.subtreeFlags),
        (r |= a.flags),
        (a.return = e),
        (a = a.sibling);
  return (e.subtreeFlags |= r), (e.childLanes = n), t;
}
function sf(e, t, n) {
  var r = t.pendingProps;
  switch ((ao(t), t.tag)) {
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
        D(fe),
        D(le),
        ho(),
        r.pendingContext &&
          ((r.context = r.pendingContext), (r.pendingContext = null)),
        (e === null || e.child === null) &&
          (fr(t)
            ? (t.flags |= 4)
            : e === null ||
              (e.memoizedState.isDehydrated && !(t.flags & 256)) ||
              ((t.flags |= 1024), je !== null && (Ol(je), (je = null)))),
        Pl(e, t),
        re(t),
        null
      );
    case 5:
      po(t);
      var a = xt(Hn.current);
      if (((n = t.type), e !== null && t.stateNode != null))
        Is(e, t, n, r, a),
          e.ref !== t.ref && ((t.flags |= 512), (t.flags |= 2097152));
      else {
        if (!r) {
          if (t.stateNode === null) throw Error(b(166));
          return re(t), null;
        }
        if (((e = xt(Ue.current)), fr(t))) {
          (r = t.stateNode), (n = t.type);
          var l = t.memoizedProps;
          switch (((r[De] = t), (r[Vn] = l), (e = (t.mode & 1) !== 0), n)) {
            case 'dialog':
              O('cancel', r), O('close', r);
              break;
            case 'iframe':
            case 'object':
            case 'embed':
              O('load', r);
              break;
            case 'video':
            case 'audio':
              for (a = 0; a < kn.length; a++) O(kn[a], r);
              break;
            case 'source':
              O('error', r);
              break;
            case 'img':
            case 'image':
            case 'link':
              O('error', r), O('load', r);
              break;
            case 'details':
              O('toggle', r);
              break;
            case 'input':
              Uo(r, l), O('invalid', r);
              break;
            case 'select':
              (r._wrapperState = { wasMultiple: !!l.multiple }),
                O('invalid', r);
              break;
            case 'textarea':
              Vo(r, l), O('invalid', r);
          }
          nl(n, l), (a = null);
          for (var o in l)
            if (l.hasOwnProperty(o)) {
              var u = l[o];
              o === 'children'
                ? typeof u == 'string'
                  ? r.textContent !== u &&
                    (l.suppressHydrationWarning !== !0 &&
                      dr(r.textContent, u, e),
                    (a = ['children', u]))
                  : typeof u == 'number' &&
                    r.textContent !== '' + u &&
                    (l.suppressHydrationWarning !== !0 &&
                      dr(r.textContent, u, e),
                    (a = ['children', '' + u]))
                : jn.hasOwnProperty(o) &&
                  u != null &&
                  o === 'onScroll' &&
                  O('scroll', r);
            }
          switch (n) {
            case 'input':
              rr(r), Ao(r, l, !0);
              break;
            case 'textarea':
              rr(r), $o(r);
              break;
            case 'select':
            case 'option':
              break;
            default:
              typeof l.onClick == 'function' && (r.onclick = Fr);
          }
          (r = a), (t.updateQueue = r), r !== null && (t.flags |= 4);
        } else {
          (o = a.nodeType === 9 ? a : a.ownerDocument),
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
            (e[De] = t),
            (e[Vn] = r),
            Rs(e, t, !1, !1),
            (t.stateNode = e);
          e: {
            switch (((o = rl(n, r)), n)) {
              case 'dialog':
                O('cancel', e), O('close', e), (a = r);
                break;
              case 'iframe':
              case 'object':
              case 'embed':
                O('load', e), (a = r);
                break;
              case 'video':
              case 'audio':
                for (a = 0; a < kn.length; a++) O(kn[a], e);
                a = r;
                break;
              case 'source':
                O('error', e), (a = r);
                break;
              case 'img':
              case 'image':
              case 'link':
                O('error', e), O('load', e), (a = r);
                break;
              case 'details':
                O('toggle', e), (a = r);
                break;
              case 'input':
                Uo(e, r), (a = Ga(e, r)), O('invalid', e);
                break;
              case 'option':
                a = r;
                break;
              case 'select':
                (e._wrapperState = { wasMultiple: !!r.multiple }),
                  (a = V({}, r, { value: void 0 })),
                  O('invalid', e);
                break;
              case 'textarea':
                Vo(e, r), (a = el(e, r)), O('invalid', e);
                break;
              default:
                a = r;
            }
            nl(n, a), (u = a);
            for (l in u)
              if (u.hasOwnProperty(l)) {
                var i = u[l];
                l === 'style'
                  ? pu(e, i)
                  : l === 'dangerouslySetInnerHTML'
                  ? ((i = i ? i.__html : void 0), i != null && du(e, i))
                  : l === 'children'
                  ? typeof i == 'string'
                    ? (n !== 'textarea' || i !== '') && Mn(e, i)
                    : typeof i == 'number' && Mn(e, '' + i)
                  : l !== 'suppressContentEditableWarning' &&
                    l !== 'suppressHydrationWarning' &&
                    l !== 'autoFocus' &&
                    (jn.hasOwnProperty(l)
                      ? i != null && l === 'onScroll' && O('scroll', e)
                      : i != null && Hl(e, l, i, o));
              }
            switch (n) {
              case 'input':
                rr(e), Ao(e, r, !1);
                break;
              case 'textarea':
                rr(e), $o(e);
                break;
              case 'option':
                r.value != null && e.setAttribute('value', '' + dt(r.value));
                break;
              case 'select':
                (e.multiple = !!r.multiple),
                  (l = r.value),
                  l != null
                    ? Wt(e, !!r.multiple, l, !1)
                    : r.defaultValue != null &&
                      Wt(e, !!r.multiple, r.defaultValue, !0);
                break;
              default:
                typeof a.onClick == 'function' && (e.onclick = Fr);
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
      if (e && t.stateNode != null) Os(e, t, e.memoizedProps, r);
      else {
        if (typeof r != 'string' && t.stateNode === null) throw Error(b(166));
        if (((n = xt(Hn.current)), xt(Ue.current), fr(t))) {
          if (
            ((r = t.stateNode),
            (n = t.memoizedProps),
            (r[De] = t),
            (l = r.nodeValue !== n) && ((e = be), e !== null))
          )
            switch (e.tag) {
              case 3:
                dr(r.nodeValue, n, (e.mode & 1) !== 0);
                break;
              case 5:
                e.memoizedProps.suppressHydrationWarning !== !0 &&
                  dr(r.nodeValue, n, (e.mode & 1) !== 0);
            }
          l && (t.flags |= 4);
        } else
          (r = (n.nodeType === 9 ? n : n.ownerDocument).createTextNode(r)),
            (r[De] = t),
            (t.stateNode = r);
      }
      return re(t), null;
    case 13:
      if (
        (D(U),
        (r = t.memoizedState),
        e === null ||
          (e.memoizedState !== null && e.memoizedState.dehydrated !== null))
      ) {
        if (F && ge !== null && t.mode & 1 && !(t.flags & 128))
          es(), Zt(), (t.flags |= 98560), (l = !1);
        else if (((l = fr(t)), r !== null && r.dehydrated !== null)) {
          if (e === null) {
            if (!l) throw Error(b(318));
            if (
              ((l = t.memoizedState),
              (l = l !== null ? l.dehydrated : null),
              !l)
            )
              throw Error(b(317));
            l[De] = t;
          } else
            Zt(), !(t.flags & 128) && (t.memoizedState = null), (t.flags |= 4);
          re(t), (l = !1);
        } else je !== null && (Ol(je), (je = null)), (l = !0);
        if (!l) return t.flags & 65536 ? t : null;
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
        Pl(e, t),
        e === null && Un(t.stateNode.containerInfo),
        re(t),
        null
      );
    case 10:
      return uo(t.type._context), re(t), null;
    case 17:
      return pe(t.type) && Ur(), re(t), null;
    case 19:
      if ((D(U), (l = t.memoizedState), l === null)) return re(t), null;
      if (((r = (t.flags & 128) !== 0), (o = l.rendering), o === null))
        if (r) gn(l, !1);
        else {
          if (q !== 0 || (e !== null && e.flags & 128))
            for (e = t.child; e !== null; ) {
              if (((o = Qr(e)), o !== null)) {
                for (
                  t.flags |= 128,
                    gn(l, !1),
                    r = o.updateQueue,
                    r !== null && ((t.updateQueue = r), (t.flags |= 4)),
                    t.subtreeFlags = 0,
                    r = n,
                    n = t.child;
                  n !== null;

                )
                  (l = n),
                    (e = r),
                    (l.flags &= 14680066),
                    (o = l.alternate),
                    o === null
                      ? ((l.childLanes = 0),
                        (l.lanes = e),
                        (l.child = null),
                        (l.subtreeFlags = 0),
                        (l.memoizedProps = null),
                        (l.memoizedState = null),
                        (l.updateQueue = null),
                        (l.dependencies = null),
                        (l.stateNode = null))
                      : ((l.childLanes = o.childLanes),
                        (l.lanes = o.lanes),
                        (l.child = o.child),
                        (l.subtreeFlags = 0),
                        (l.deletions = null),
                        (l.memoizedProps = o.memoizedProps),
                        (l.memoizedState = o.memoizedState),
                        (l.updateQueue = o.updateQueue),
                        (l.type = o.type),
                        (e = o.dependencies),
                        (l.dependencies =
                          e === null
                            ? null
                            : {
                                lanes: e.lanes,
                                firstContext: e.firstContext,
                              })),
                    (n = n.sibling);
                return I(U, (U.current & 1) | 2), t.child;
              }
              e = e.sibling;
            }
          l.tail !== null &&
            W() > rn &&
            ((t.flags |= 128), (r = !0), gn(l, !1), (t.lanes = 4194304));
        }
      else {
        if (!r)
          if (((e = Qr(o)), e !== null)) {
            if (
              ((t.flags |= 128),
              (r = !0),
              (n = e.updateQueue),
              n !== null && ((t.updateQueue = n), (t.flags |= 4)),
              gn(l, !0),
              l.tail === null && l.tailMode === 'hidden' && !o.alternate && !F)
            )
              return re(t), null;
          } else
            2 * W() - l.renderingStartTime > rn &&
              n !== 1073741824 &&
              ((t.flags |= 128), (r = !0), gn(l, !1), (t.lanes = 4194304));
        l.isBackwards
          ? ((o.sibling = t.child), (t.child = o))
          : ((n = l.last),
            n !== null ? (n.sibling = o) : (t.child = o),
            (l.last = o));
      }
      return l.tail !== null
        ? ((t = l.tail),
          (l.rendering = t),
          (l.tail = t.sibling),
          (l.renderingStartTime = W()),
          (t.sibling = null),
          (n = U.current),
          I(U, r ? (n & 1) | 2 : n & 1),
          t)
        : (re(t), null);
    case 22:
    case 23:
      return (
        Eo(),
        (r = t.memoizedState !== null),
        e !== null && (e.memoizedState !== null) !== r && (t.flags |= 8192),
        r && t.mode & 1
          ? me & 1073741824 && (re(t), t.subtreeFlags & 6 && (t.flags |= 8192))
          : re(t),
        null
      );
    case 24:
      return null;
    case 25:
      return null;
  }
  throw Error(b(156, t.tag));
}
function cf(e, t) {
  switch ((ao(t), t.tag)) {
    case 1:
      return (
        pe(t.type) && Ur(),
        (e = t.flags),
        e & 65536 ? ((t.flags = (e & -65537) | 128), t) : null
      );
    case 3:
      return (
        tn(),
        D(fe),
        D(le),
        ho(),
        (e = t.flags),
        e & 65536 && !(e & 128) ? ((t.flags = (e & -65537) | 128), t) : null
      );
    case 5:
      return po(t), null;
    case 13:
      if ((D(U), (e = t.memoizedState), e !== null && e.dehydrated !== null)) {
        if (t.alternate === null) throw Error(b(340));
        Zt();
      }
      return (
        (e = t.flags), e & 65536 ? ((t.flags = (e & -65537) | 128), t) : null
      );
    case 19:
      return D(U), null;
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
var mr = !1,
  ae = !1,
  df = typeof WeakSet == 'function' ? WeakSet : Set,
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
function Ds(e, t, n) {
  try {
    n();
  } catch (r) {
    $(e, t, r);
  }
}
var ji = !1;
function ff(e, t) {
  if (((pl = Ir), (e = Vu()), no(e))) {
    if ('selectionStart' in e)
      var n = { start: e.selectionStart, end: e.selectionEnd };
    else
      e: {
        n = ((n = e.ownerDocument) && n.defaultView) || window;
        var r = n.getSelection && n.getSelection();
        if (r && r.rangeCount !== 0) {
          n = r.anchorNode;
          var a = r.anchorOffset,
            l = r.focusNode;
          r = r.focusOffset;
          try {
            n.nodeType, l.nodeType;
          } catch {
            n = null;
            break e;
          }
          var o = 0,
            u = -1,
            i = -1,
            c = 0,
            h = 0,
            m = e,
            p = null;
          t: for (;;) {
            for (
              var w;
              m !== n || (a !== 0 && m.nodeType !== 3) || (u = o + a),
                m !== l || (r !== 0 && m.nodeType !== 3) || (i = o + r),
                m.nodeType === 3 && (o += m.nodeValue.length),
                (w = m.firstChild) !== null;

            )
              (p = m), (m = w);
            for (;;) {
              if (m === e) break t;
              if (
                (p === n && ++c === a && (u = o),
                p === l && ++h === r && (i = o),
                (w = m.nextSibling) !== null)
              )
                break;
              (m = p), (p = m.parentNode);
            }
            m = w;
          }
          n = u === -1 || i === -1 ? null : { start: u, end: i };
        } else n = null;
      }
    n = n || { start: 0, end: 0 };
  } else n = null;
  for (
    hl = { focusedElem: e, selectionRange: n }, Ir = !1, x = t;
    x !== null;

  )
    if (((t = x), (e = t.child), (t.subtreeFlags & 1028) !== 0 && e !== null))
      (e.return = t), (x = e);
    else
      for (; x !== null; ) {
        t = x;
        try {
          var v = t.alternate;
          if (t.flags & 1024)
            switch (t.tag) {
              case 0:
              case 11:
              case 15:
                break;
              case 1:
                if (v !== null) {
                  var k = v.memoizedProps,
                    M = v.memoizedState,
                    f = t.stateNode,
                    s = f.getSnapshotBeforeUpdate(
                      t.elementType === t.type ? k : Pe(t.type, k),
                      M
                    );
                  f.__reactInternalSnapshotBeforeUpdate = s;
                }
                break;
              case 3:
                var d = t.stateNode.containerInfo;
                d.nodeType === 1
                  ? (d.textContent = '')
                  : d.nodeType === 9 &&
                    d.documentElement &&
                    d.removeChild(d.documentElement);
                break;
              case 5:
              case 6:
              case 4:
              case 17:
                break;
              default:
                throw Error(b(163));
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
  return (v = ji), (ji = !1), v;
}
function zn(e, t, n) {
  var r = t.updateQueue;
  if (((r = r !== null ? r.lastEffect : null), r !== null)) {
    var a = (r = r.next);
    do {
      if ((a.tag & e) === e) {
        var l = a.destroy;
        (a.destroy = void 0), l !== void 0 && Ds(t, n, l);
      }
      a = a.next;
    } while (a !== r);
  }
}
function sa(e, t) {
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
function Ll(e) {
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
        (delete t[De],
        delete t[Vn],
        delete t[bl],
        delete t[Xd],
        delete t[qd])),
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
function Mi(e) {
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
function jl(e, t, n) {
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
    for (jl(e, t, n), e = e.sibling; e !== null; )
      jl(e, t, n), (e = e.sibling);
}
function Ml(e, t, n) {
  var r = e.tag;
  if (r === 5 || r === 6)
    (e = e.stateNode), t ? n.insertBefore(e, t) : n.appendChild(e);
  else if (r !== 4 && ((e = e.child), e !== null))
    for (Ml(e, t, n), e = e.sibling; e !== null; )
      Ml(e, t, n), (e = e.sibling);
}
var J = null,
  Le = !1;
function Ke(e, t, n) {
  for (n = n.child; n !== null; ) As(e, t, n), (n = n.sibling);
}
function As(e, t, n) {
  if (Fe && typeof Fe.onCommitFiberUnmount == 'function')
    try {
      Fe.onCommitFiberUnmount(ta, n);
    } catch {}
  switch (n.tag) {
    case 5:
      ae || Ht(n, t);
    case 6:
      var r = J,
        a = Le;
      (J = null),
        Ke(e, t, n),
        (J = r),
        (Le = a),
        J !== null &&
          (Le
            ? ((e = J),
              (n = n.stateNode),
              e.nodeType === 8
                ? e.parentNode.removeChild(n)
                : e.removeChild(n))
            : J.removeChild(n.stateNode));
      break;
    case 18:
      J !== null &&
        (Le
          ? ((e = J),
            (n = n.stateNode),
            e.nodeType === 8
              ? Ia(e.parentNode, n)
              : e.nodeType === 1 && Ia(e, n),
            On(e))
          : Ia(J, n.stateNode));
      break;
    case 4:
      (r = J),
        (a = Le),
        (J = n.stateNode.containerInfo),
        (Le = !0),
        Ke(e, t, n),
        (J = r),
        (Le = a);
      break;
    case 0:
    case 11:
    case 14:
    case 15:
      if (
        !ae &&
        ((r = n.updateQueue), r !== null && ((r = r.lastEffect), r !== null))
      ) {
        a = r = r.next;
        do {
          var l = a,
            o = l.destroy;
          (l = l.tag),
            o !== void 0 && (l & 2 || l & 4) && Ds(n, t, o),
            (a = a.next);
        } while (a !== r);
      }
      Ke(e, t, n);
      break;
    case 1:
      if (
        !ae &&
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
        ? ((ae = (r = ae) || n.memoizedState !== null), Ke(e, t, n), (ae = r))
        : Ke(e, t, n);
      break;
    default:
      Ke(e, t, n);
  }
}
function Ti(e) {
  var t = e.updateQueue;
  if (t !== null) {
    e.updateQueue = null;
    var n = e.stateNode;
    n === null && (n = e.stateNode = new df()),
      t.forEach(function (r) {
        var a = kf.bind(null, e, r);
        n.has(r) || (n.add(r), r.then(a, a));
      });
  }
}
function ze(e, t) {
  var n = t.deletions;
  if (n !== null)
    for (var r = 0; r < n.length; r++) {
      var a = n[r];
      try {
        var l = e,
          o = t,
          u = o;
        e: for (; u !== null; ) {
          switch (u.tag) {
            case 5:
              (J = u.stateNode), (Le = !1);
              break e;
            case 3:
              (J = u.stateNode.containerInfo), (Le = !0);
              break e;
            case 4:
              (J = u.stateNode.containerInfo), (Le = !0);
              break e;
          }
          u = u.return;
        }
        if (J === null) throw Error(b(160));
        As(l, o, a), (J = null), (Le = !1);
        var i = a.alternate;
        i !== null && (i.return = null), (a.return = null);
      } catch (c) {
        $(a, t, c);
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
      if ((ze(t, e), Ie(e), r & 4)) {
        try {
          zn(3, e, e.return), sa(3, e);
        } catch (k) {
          $(e, e.return, k);
        }
        try {
          zn(5, e, e.return);
        } catch (k) {
          $(e, e.return, k);
        }
      }
      break;
    case 1:
      ze(t, e), Ie(e), r & 512 && n !== null && Ht(n, n.return);
      break;
    case 5:
      if (
        (ze(t, e),
        Ie(e),
        r & 512 && n !== null && Ht(n, n.return),
        e.flags & 32)
      ) {
        var a = e.stateNode;
        try {
          Mn(a, '');
        } catch (k) {
          $(e, e.return, k);
        }
      }
      if (r & 4 && ((a = e.stateNode), a != null)) {
        var l = e.memoizedProps,
          o = n !== null ? n.memoizedProps : l,
          u = e.type,
          i = e.updateQueue;
        if (((e.updateQueue = null), i !== null))
          try {
            u === 'input' && l.type === 'radio' && l.name != null && uu(a, l),
              rl(u, o);
            var c = rl(u, l);
            for (o = 0; o < i.length; o += 2) {
              var h = i[o],
                m = i[o + 1];
              h === 'style'
                ? pu(a, m)
                : h === 'dangerouslySetInnerHTML'
                ? du(a, m)
                : h === 'children'
                ? Mn(a, m)
                : Hl(a, h, m, c);
            }
            switch (u) {
              case 'input':
                Ja(a, l);
                break;
              case 'textarea':
                su(a, l);
                break;
              case 'select':
                var p = a._wrapperState.wasMultiple;
                a._wrapperState.wasMultiple = !!l.multiple;
                var w = l.value;
                w != null
                  ? Wt(a, !!l.multiple, w, !1)
                  : p !== !!l.multiple &&
                    (l.defaultValue != null
                      ? Wt(a, !!l.multiple, l.defaultValue, !0)
                      : Wt(a, !!l.multiple, l.multiple ? [] : '', !1));
            }
            a[Vn] = l;
          } catch (k) {
            $(e, e.return, k);
          }
      }
      break;
    case 6:
      if ((ze(t, e), Ie(e), r & 4)) {
        if (e.stateNode === null) throw Error(b(162));
        (a = e.stateNode), (l = e.memoizedProps);
        try {
          a.nodeValue = l;
        } catch (k) {
          $(e, e.return, k);
        }
      }
      break;
    case 3:
      if (
        (ze(t, e), Ie(e), r & 4 && n !== null && n.memoizedState.isDehydrated)
      )
        try {
          On(t.containerInfo);
        } catch (k) {
          $(e, e.return, k);
        }
      break;
    case 4:
      ze(t, e), Ie(e);
      break;
    case 13:
      ze(t, e),
        Ie(e),
        (a = e.child),
        a.flags & 8192 &&
          ((l = a.memoizedState !== null),
          (a.stateNode.isHidden = l),
          !l ||
            (a.alternate !== null && a.alternate.memoizedState !== null) ||
            (So = W())),
        r & 4 && Ti(e);
      break;
    case 22:
      if (
        ((h = n !== null && n.memoizedState !== null),
        e.mode & 1 ? ((ae = (c = ae) || h), ze(t, e), (ae = c)) : ze(t, e),
        Ie(e),
        r & 8192)
      ) {
        if (
          ((c = e.memoizedState !== null),
          (e.stateNode.isHidden = c) && !h && e.mode & 1)
        )
          for (x = e, h = e.child; h !== null; ) {
            for (m = x = h; x !== null; ) {
              switch (((p = x), (w = p.child), p.tag)) {
                case 0:
                case 11:
                case 14:
                case 15:
                  zn(4, p, p.return);
                  break;
                case 1:
                  Ht(p, p.return);
                  var v = p.stateNode;
                  if (typeof v.componentWillUnmount == 'function') {
                    (r = p), (n = p.return);
                    try {
                      (t = r),
                        (v.props = t.memoizedProps),
                        (v.state = t.memoizedState),
                        v.componentWillUnmount();
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
                    Ii(m);
                    continue;
                  }
              }
              w !== null ? ((w.return = p), (x = w)) : Ii(m);
            }
            h = h.sibling;
          }
        e: for (h = null, m = e; ; ) {
          if (m.tag === 5) {
            if (h === null) {
              h = m;
              try {
                (a = m.stateNode),
                  c
                    ? ((l = a.style),
                      typeof l.setProperty == 'function'
                        ? l.setProperty('display', 'none', 'important')
                        : (l.display = 'none'))
                    : ((u = m.stateNode),
                      (i = m.memoizedProps.style),
                      (o =
                        i != null && i.hasOwnProperty('display')
                          ? i.display
                          : null),
                      (u.style.display = fu('display', o)));
              } catch (k) {
                $(e, e.return, k);
              }
            }
          } else if (m.tag === 6) {
            if (h === null)
              try {
                m.stateNode.nodeValue = c ? '' : m.memoizedProps;
              } catch (k) {
                $(e, e.return, k);
              }
          } else if (
            ((m.tag !== 22 && m.tag !== 23) ||
              m.memoizedState === null ||
              m === e) &&
            m.child !== null
          ) {
            (m.child.return = m), (m = m.child);
            continue;
          }
          if (m === e) break e;
          for (; m.sibling === null; ) {
            if (m.return === null || m.return === e) break e;
            h === m && (h = null), (m = m.return);
          }
          h === m && (h = null),
            (m.sibling.return = m.return),
            (m = m.sibling);
        }
      }
      break;
    case 19:
      ze(t, e), Ie(e), r & 4 && Ti(e);
      break;
    case 21:
      break;
    default:
      ze(t, e), Ie(e);
  }
}
function Ie(e) {
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
        throw Error(b(160));
      }
      switch (r.tag) {
        case 5:
          var a = r.stateNode;
          r.flags & 32 && (Mn(a, ''), (r.flags &= -33));
          var l = Mi(e);
          Ml(e, l, a);
          break;
        case 3:
        case 4:
          var o = r.stateNode.containerInfo,
            u = Mi(e);
          jl(e, u, o);
          break;
        default:
          throw Error(b(161));
      }
    } catch (i) {
      $(e, e.return, i);
    }
    e.flags &= -3;
  }
  t & 4096 && (e.flags &= -4097);
}
function pf(e, t, n) {
  (x = e), $s(e);
}
function $s(e, t, n) {
  for (var r = (e.mode & 1) !== 0; x !== null; ) {
    var a = x,
      l = a.child;
    if (a.tag === 22 && r) {
      var o = a.memoizedState !== null || mr;
      if (!o) {
        var u = a.alternate,
          i = (u !== null && u.memoizedState !== null) || ae;
        u = mr;
        var c = ae;
        if (((mr = o), (ae = i) && !c))
          for (x = a; x !== null; )
            (o = x),
              (i = o.child),
              o.tag === 22 && o.memoizedState !== null
                ? Oi(a)
                : i !== null
                ? ((i.return = o), (x = i))
                : Oi(a);
        for (; l !== null; ) (x = l), $s(l), (l = l.sibling);
        (x = a), (mr = u), (ae = c);
      }
      Ri(e);
    } else
      a.subtreeFlags & 8772 && l !== null ? ((l.return = a), (x = l)) : Ri(e);
  }
}
function Ri(e) {
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
              ae || sa(5, t);
              break;
            case 1:
              var r = t.stateNode;
              if (t.flags & 4 && !ae)
                if (n === null) r.componentDidMount();
                else {
                  var a =
                    t.elementType === t.type
                      ? n.memoizedProps
                      : Pe(t.type, n.memoizedProps);
                  r.componentDidUpdate(
                    a,
                    n.memoizedState,
                    r.__reactInternalSnapshotBeforeUpdate
                  );
                }
              var l = t.updateQueue;
              l !== null && yi(t, l, r);
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
                  var h = c.memoizedState;
                  if (h !== null) {
                    var m = h.dehydrated;
                    m !== null && On(m);
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
              throw Error(b(163));
          }
        ae || (t.flags & 512 && Ll(t));
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
function Ii(e) {
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
function Oi(e) {
  for (; x !== null; ) {
    var t = x;
    try {
      switch (t.tag) {
        case 0:
        case 11:
        case 15:
          var n = t.return;
          try {
            sa(4, t);
          } catch (i) {
            $(t, n, i);
          }
          break;
        case 1:
          var r = t.stateNode;
          if (typeof r.componentDidMount == 'function') {
            var a = t.return;
            try {
              r.componentDidMount();
            } catch (i) {
              $(t, a, i);
            }
          }
          var l = t.return;
          try {
            Ll(t);
          } catch (i) {
            $(t, l, i);
          }
          break;
        case 5:
          var o = t.return;
          try {
            Ll(t);
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
var hf = Math.ceil,
  Yr = Ye.ReactCurrentDispatcher,
  ko = Ye.ReactCurrentOwner,
  _e = Ye.ReactCurrentBatchConfig,
  T = 0,
  G = null,
  Q = null,
  ee = 0,
  me = 0,
  Bt = ht(0),
  q = 0,
  Xn = null,
  zt = 0,
  ca = 0,
  xo = 0,
  Pn = null,
  ce = null,
  So = 0,
  rn = 1 / 0,
  Ae = null,
  Kr = !1,
  Tl = null,
  ut = null,
  gr = !1,
  nt = null,
  Gr = 0,
  Ln = 0,
  Rl = null,
  Cr = -1,
  zr = 0;
function ie() {
  return T & 6 ? W() : Cr !== -1 ? Cr : (Cr = W());
}
function st(e) {
  return e.mode & 1
    ? T & 2 && ee !== 0
      ? ee & -ee
      : Kd.transition !== null
      ? (zr === 0 && (zr = Eu()), zr)
      : ((e = R),
        e !== 0 || ((e = window.event), (e = e === void 0 ? 16 : Mu(e.type))),
        e)
    : 1;
}
function Te(e, t, n, r) {
  if (50 < Ln) throw ((Ln = 0), (Rl = null), Error(b(185)));
  Yn(e, n, r),
    (!(T & 2) || e !== G) &&
      (e === G && (!(T & 2) && (ca |= n), q === 4 && et(e, ee)),
      he(e, r),
      n === 1 && T === 0 && !(t.mode & 1) && ((rn = W() + 500), oa && mt()));
}
function he(e, t) {
  var n = e.callbackNode;
  Kc(e, t);
  var r = Rr(e, e === G ? ee : 0);
  if (r === 0)
    n !== null && Wo(n), (e.callbackNode = null), (e.callbackPriority = 0);
  else if (((t = r & -r), e.callbackPriority !== t)) {
    if ((n != null && Wo(n), t === 1))
      e.tag === 0 ? Yd(Di.bind(null, e)) : Gu(Di.bind(null, e)),
        Wd(function () {
          !(T & 6) && mt();
        }),
        (n = null);
    else {
      switch (Nu(r)) {
        case 1:
          n = ql;
          break;
        case 4:
          n = Su;
          break;
        case 16:
          n = Tr;
          break;
        case 536870912:
          n = _u;
          break;
        default:
          n = Tr;
      }
      n = Ks(n, Hs.bind(null, e));
    }
    (e.callbackPriority = t), (e.callbackNode = n);
  }
}
function Hs(e, t) {
  if (((Cr = -1), (zr = 0), T & 6)) throw Error(b(327));
  var n = e.callbackNode;
  if (Kt() && e.callbackNode !== n) return null;
  var r = Rr(e, e === G ? ee : 0);
  if (r === 0) return null;
  if (r & 30 || r & e.expiredLanes || t) t = Jr(e, r);
  else {
    t = r;
    var a = T;
    T |= 2;
    var l = Ws();
    (G !== e || ee !== t) && ((Ae = null), (rn = W() + 500), St(e, t));
    do
      try {
        bf();
        break;
      } catch (u) {
        Bs(e, u);
      }
    while (!0);
    io(),
      (Yr.current = l),
      (T = a),
      Q !== null ? (t = 0) : ((G = null), (ee = 0), (t = q));
  }
  if (t !== 0) {
    if (
      (t === 2 && ((a = ul(e)), a !== 0 && ((r = a), (t = Il(e, a)))), t === 1)
    )
      throw ((n = Xn), St(e, 0), et(e, r), he(e, W()), n);
    if (t === 6) et(e, r);
    else {
      if (
        ((a = e.current.alternate),
        !(r & 30) &&
          !mf(a) &&
          ((t = Jr(e, r)),
          t === 2 && ((l = ul(e)), l !== 0 && ((r = l), (t = Il(e, l)))),
          t === 1))
      )
        throw ((n = Xn), St(e, 0), et(e, r), he(e, W()), n);
      switch (((e.finishedWork = a), (e.finishedLanes = r), t)) {
        case 0:
        case 1:
          throw Error(b(345));
        case 2:
          vt(e, ce, Ae);
          break;
        case 3:
          if (
            (et(e, r), (r & 130023424) === r && ((t = So + 500 - W()), 10 < t))
          ) {
            if (Rr(e, 0) !== 0) break;
            if (((a = e.suspendedLanes), (a & r) !== r)) {
              ie(), (e.pingedLanes |= e.suspendedLanes & a);
              break;
            }
            e.timeoutHandle = gl(vt.bind(null, e, ce, Ae), t);
            break;
          }
          vt(e, ce, Ae);
          break;
        case 4:
          if ((et(e, r), (r & 4194240) === r)) break;
          for (t = e.eventTimes, a = -1; 0 < r; ) {
            var o = 31 - Me(r);
            (l = 1 << o), (o = t[o]), o > a && (a = o), (r &= ~l);
          }
          if (
            ((r = a),
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
                : 1960 * hf(r / 1960)) - r),
            10 < r)
          ) {
            e.timeoutHandle = gl(vt.bind(null, e, ce, Ae), r);
            break;
          }
          vt(e, ce, Ae);
          break;
        case 5:
          vt(e, ce, Ae);
          break;
        default:
          throw Error(b(329));
      }
    }
  }
  return he(e, W()), e.callbackNode === n ? Hs.bind(null, e) : null;
}
function Il(e, t) {
  var n = Pn;
  return (
    e.current.memoizedState.isDehydrated && (St(e, t).flags |= 256),
    (e = Jr(e, t)),
    e !== 2 && ((t = ce), (ce = n), t !== null && Ol(t)),
    e
  );
}
function Ol(e) {
  ce === null ? (ce = e) : ce.push.apply(ce, e);
}
function mf(e) {
  for (var t = e; ; ) {
    if (t.flags & 16384) {
      var n = t.updateQueue;
      if (n !== null && ((n = n.stores), n !== null))
        for (var r = 0; r < n.length; r++) {
          var a = n[r],
            l = a.getSnapshot;
          a = a.value;
          try {
            if (!Re(l(), a)) return !1;
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
      t &= ~ca,
      e.suspendedLanes |= t,
      e.pingedLanes &= ~t,
      e = e.expirationTimes;
    0 < t;

  ) {
    var n = 31 - Me(t),
      r = 1 << n;
    (e[n] = -1), (t &= ~r);
  }
}
function Di(e) {
  if (T & 6) throw Error(b(327));
  Kt();
  var t = Rr(e, 0);
  if (!(t & 1)) return he(e, W()), null;
  var n = Jr(e, t);
  if (e.tag !== 0 && n === 2) {
    var r = ul(e);
    r !== 0 && ((t = r), (n = Il(e, r)));
  }
  if (n === 1) throw ((n = Xn), St(e, 0), et(e, t), he(e, W()), n);
  if (n === 6) throw Error(b(345));
  return (
    (e.finishedWork = e.current.alternate),
    (e.finishedLanes = t),
    vt(e, ce, Ae),
    he(e, W()),
    null
  );
}
function _o(e, t) {
  var n = T;
  T |= 1;
  try {
    return e(t);
  } finally {
    (T = n), T === 0 && ((rn = W() + 500), oa && mt());
  }
}
function Pt(e) {
  nt !== null && nt.tag === 0 && !(T & 6) && Kt();
  var t = T;
  T |= 1;
  var n = _e.transition,
    r = R;
  try {
    if (((_e.transition = null), (R = 1), e)) return e();
  } finally {
    (R = r), (_e.transition = n), (T = t), !(T & 6) && mt();
  }
}
function Eo() {
  (me = Bt.current), D(Bt);
}
function St(e, t) {
  (e.finishedWork = null), (e.finishedLanes = 0);
  var n = e.timeoutHandle;
  if ((n !== -1 && ((e.timeoutHandle = -1), Bd(n)), Q !== null))
    for (n = Q.return; n !== null; ) {
      var r = n;
      switch ((ao(r), r.tag)) {
        case 1:
          (r = r.type.childContextTypes), r != null && Ur();
          break;
        case 3:
          tn(), D(fe), D(le), ho();
          break;
        case 5:
          po(r);
          break;
        case 4:
          tn();
          break;
        case 13:
          D(U);
          break;
        case 19:
          D(U);
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
    (ee = me = t),
    (q = 0),
    (Xn = null),
    (xo = ca = zt = 0),
    (ce = Pn = null),
    kt !== null)
  ) {
    for (t = 0; t < kt.length; t++)
      if (((n = kt[t]), (r = n.interleaved), r !== null)) {
        n.interleaved = null;
        var a = r.next,
          l = n.pending;
        if (l !== null) {
          var o = l.next;
          (l.next = a), (r.next = o);
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
          var a = r.queue;
          a !== null && (a.pending = null), (r = r.next);
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
        var l = e,
          o = n.return,
          u = n,
          i = t;
        if (
          ((t = ee),
          (u.flags |= 32768),
          i !== null && typeof i == 'object' && typeof i.then == 'function')
        ) {
          var c = i,
            h = u,
            m = h.tag;
          if (!(h.mode & 1) && (m === 0 || m === 11 || m === 15)) {
            var p = h.alternate;
            p
              ? ((h.updateQueue = p.updateQueue),
                (h.memoizedState = p.memoizedState),
                (h.lanes = p.lanes))
              : ((h.updateQueue = null), (h.memoizedState = null));
          }
          var w = _i(o);
          if (w !== null) {
            (w.flags &= -257),
              Ei(w, o, u, l, t),
              w.mode & 1 && Si(l, c, t),
              (t = w),
              (i = c);
            var v = t.updateQueue;
            if (v === null) {
              var k = new Set();
              k.add(i), (t.updateQueue = k);
            } else v.add(i);
            break e;
          } else {
            if (!(t & 1)) {
              Si(l, c, t), No();
              break e;
            }
            i = Error(b(426));
          }
        } else if (F && u.mode & 1) {
          var M = _i(o);
          if (M !== null) {
            !(M.flags & 65536) && (M.flags |= 256),
              Ei(M, o, u, l, t),
              lo(nn(i, u));
            break e;
          }
        }
        (l = i = nn(i, u)),
          q !== 4 && (q = 2),
          Pn === null ? (Pn = [l]) : Pn.push(l),
          (l = o);
        do {
          switch (l.tag) {
            case 3:
              (l.flags |= 65536), (t &= -t), (l.lanes |= t);
              var f = Ns(l, i, t);
              bi(l, f);
              break e;
            case 1:
              u = i;
              var s = l.type,
                d = l.stateNode;
              if (
                !(l.flags & 128) &&
                (typeof s.getDerivedStateFromError == 'function' ||
                  (d !== null &&
                    typeof d.componentDidCatch == 'function' &&
                    (ut === null || !ut.has(d))))
              ) {
                (l.flags |= 65536), (t &= -t), (l.lanes |= t);
                var y = Cs(l, u, t);
                bi(l, y);
                break e;
              }
          }
          l = l.return;
        } while (l !== null);
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
    G === null || (!(zt & 268435455) && !(ca & 268435455)) || et(G, ee);
}
function Jr(e, t) {
  var n = T;
  T |= 2;
  var r = Ws();
  (G !== e || ee !== t) && ((Ae = null), St(e, t));
  do
    try {
      gf();
      break;
    } catch (a) {
      Bs(e, a);
    }
  while (!0);
  if ((io(), (T = n), (Yr.current = r), Q !== null)) throw Error(b(261));
  return (G = null), (ee = 0), q;
}
function gf() {
  for (; Q !== null; ) Qs(Q);
}
function bf() {
  for (; Q !== null && !Vc(); ) Qs(Q);
}
function Qs(e) {
  var t = Ys(e.alternate, e, me);
  (e.memoizedProps = e.pendingProps),
    t === null ? Xs(e) : (Q = t),
    (ko.current = null);
}
function Xs(e) {
  var t = e;
  do {
    var n = t.alternate;
    if (((e = t.return), t.flags & 32768)) {
      if (((n = cf(n, t)), n !== null)) {
        (n.flags &= 32767), (Q = n);
        return;
      }
      if (e !== null)
        (e.flags |= 32768), (e.subtreeFlags = 0), (e.deletions = null);
      else {
        (q = 6), (Q = null);
        return;
      }
    } else if (((n = sf(n, t, me)), n !== null)) {
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
function vt(e, t, n) {
  var r = R,
    a = _e.transition;
  try {
    (_e.transition = null), (R = 1), yf(e, t, n, r);
  } finally {
    (_e.transition = a), (R = r);
  }
  return null;
}
function yf(e, t, n, r) {
  do Kt();
  while (nt !== null);
  if (T & 6) throw Error(b(327));
  n = e.finishedWork;
  var a = e.finishedLanes;
  if (n === null) return null;
  if (((e.finishedWork = null), (e.finishedLanes = 0), n === e.current))
    throw Error(b(177));
  (e.callbackNode = null), (e.callbackPriority = 0);
  var l = n.lanes | n.childLanes;
  if (
    (Gc(e, l),
    e === G && ((Q = G = null), (ee = 0)),
    (!(n.subtreeFlags & 2064) && !(n.flags & 2064)) ||
      gr ||
      ((gr = !0),
      Ks(Tr, function () {
        return Kt(), null;
      })),
    (l = (n.flags & 15990) !== 0),
    n.subtreeFlags & 15990 || l)
  ) {
    (l = _e.transition), (_e.transition = null);
    var o = R;
    R = 1;
    var u = T;
    (T |= 4),
      (ko.current = null),
      ff(e, n),
      Vs(n, e),
      Dd(hl),
      (Ir = !!pl),
      (hl = pl = null),
      (e.current = n),
      pf(n),
      $c(),
      (T = u),
      (R = o),
      (_e.transition = l);
  } else e.current = n;
  if (
    (gr && ((gr = !1), (nt = e), (Gr = a)),
    (l = e.pendingLanes),
    l === 0 && (ut = null),
    Wc(n.stateNode),
    he(e, W()),
    t !== null)
  )
    for (r = e.onRecoverableError, n = 0; n < t.length; n++)
      (a = t[n]), r(a.value, { componentStack: a.stack, digest: a.digest });
  if (Kr) throw ((Kr = !1), (e = Tl), (Tl = null), e);
  return (
    Gr & 1 && e.tag !== 0 && Kt(),
    (l = e.pendingLanes),
    l & 1 ? (e === Rl ? Ln++ : ((Ln = 0), (Rl = e))) : (Ln = 0),
    mt(),
    null
  );
}
function Kt() {
  if (nt !== null) {
    var e = Nu(Gr),
      t = _e.transition,
      n = R;
    try {
      if (((_e.transition = null), (R = 16 > e ? 16 : e), nt === null))
        var r = !1;
      else {
        if (((e = nt), (nt = null), (Gr = 0), T & 6)) throw Error(b(331));
        var a = T;
        for (T |= 4, x = e.current; x !== null; ) {
          var l = x,
            o = l.child;
          if (x.flags & 16) {
            var u = l.deletions;
            if (u !== null) {
              for (var i = 0; i < u.length; i++) {
                var c = u[i];
                for (x = c; x !== null; ) {
                  var h = x;
                  switch (h.tag) {
                    case 0:
                    case 11:
                    case 15:
                      zn(8, h, l);
                  }
                  var m = h.child;
                  if (m !== null) (m.return = h), (x = m);
                  else
                    for (; x !== null; ) {
                      h = x;
                      var p = h.sibling,
                        w = h.return;
                      if ((Fs(h), h === c)) {
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
              var v = l.alternate;
              if (v !== null) {
                var k = v.child;
                if (k !== null) {
                  v.child = null;
                  do {
                    var M = k.sibling;
                    (k.sibling = null), (k = M);
                  } while (k !== null);
                }
              }
              x = l;
            }
          }
          if (l.subtreeFlags & 2064 && o !== null) (o.return = l), (x = o);
          else
            e: for (; x !== null; ) {
              if (((l = x), l.flags & 2048))
                switch (l.tag) {
                  case 0:
                  case 11:
                  case 15:
                    zn(9, l, l.return);
                }
              var f = l.sibling;
              if (f !== null) {
                (f.return = l.return), (x = f);
                break e;
              }
              x = l.return;
            }
        }
        var s = e.current;
        for (x = s; x !== null; ) {
          o = x;
          var d = o.child;
          if (o.subtreeFlags & 2064 && d !== null) (d.return = o), (x = d);
          else
            e: for (o = s; x !== null; ) {
              if (((u = x), u.flags & 2048))
                try {
                  switch (u.tag) {
                    case 0:
                    case 11:
                    case 15:
                      sa(9, u);
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
          ((T = a), mt(), Fe && typeof Fe.onPostCommitFiberRoot == 'function')
        )
          try {
            Fe.onPostCommitFiberRoot(ta, e);
          } catch {}
        r = !0;
      }
      return r;
    } finally {
      (R = n), (_e.transition = t);
    }
  }
  return !1;
}
function Fi(e, t, n) {
  (t = nn(n, t)),
    (t = Ns(e, t, 1)),
    (e = it(e, t, 1)),
    (t = ie()),
    e !== null && (Yn(e, 1, t), he(e, t));
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
            t !== null && (Yn(t, 1, e), he(t, e));
          break;
        }
      }
      t = t.return;
    }
}
function vf(e, t, n) {
  var r = e.pingCache;
  r !== null && r.delete(t),
    (t = ie()),
    (e.pingedLanes |= e.suspendedLanes & n),
    G === e &&
      (ee & n) === n &&
      (q === 4 || (q === 3 && (ee & 130023424) === ee && 500 > W() - So)
        ? St(e, 0)
        : (xo |= n)),
    he(e, t);
}
function qs(e, t) {
  t === 0 &&
    (e.mode & 1
      ? ((t = or), (or <<= 1), !(or & 130023424) && (or = 4194304))
      : (t = 1));
  var n = ie();
  (e = Xe(e, t)), e !== null && (Yn(e, t, n), he(e, n));
}
function wf(e) {
  var t = e.memoizedState,
    n = 0;
  t !== null && (n = t.retryLane), qs(e, n);
}
function kf(e, t) {
  var n = 0;
  switch (e.tag) {
    case 13:
      var r = e.stateNode,
        a = e.memoizedState;
      a !== null && (n = a.retryLane);
      break;
    case 19:
      r = e.stateNode;
      break;
    default:
      throw Error(b(314));
  }
  r !== null && r.delete(t), qs(e, n);
}
var Ys;
Ys = function (e, t, n) {
  if (e !== null)
    if (e.memoizedProps !== t.pendingProps || fe.current) de = !0;
    else {
      if (!(e.lanes & n) && !(t.flags & 128)) return (de = !1), uf(e, t, n);
      de = !!(e.flags & 131072);
    }
  else (de = !1), F && t.flags & 1048576 && Ju(t, $r, t.index);
  switch (((t.lanes = 0), t.tag)) {
    case 2:
      var r = t.type;
      Nr(e, t), (e = t.pendingProps);
      var a = Jt(t, le.current);
      Yt(t, n), (a = go(null, t, r, e, a, n));
      var l = bo();
      return (
        (t.flags |= 1),
        typeof a == 'object' &&
        a !== null &&
        typeof a.render == 'function' &&
        a.$$typeof === void 0
          ? ((t.tag = 1),
            (t.memoizedState = null),
            (t.updateQueue = null),
            pe(r) ? ((l = !0), Ar(t)) : (l = !1),
            (t.memoizedState =
              a.state !== null && a.state !== void 0 ? a.state : null),
            co(t),
            (a.updater = ua),
            (t.stateNode = a),
            (a._reactInternals = t),
            Sl(t, r, e, n),
            (t = Nl(null, t, r, !0, l, n)))
          : ((t.tag = 0), F && l && ro(t), oe(null, t, a, n), (t = t.child)),
        t
      );
    case 16:
      r = t.elementType;
      e: {
        switch (
          (Nr(e, t),
          (e = t.pendingProps),
          (a = r._init),
          (r = a(r._payload)),
          (t.type = r),
          (a = t.tag = Sf(r)),
          (e = Pe(r, e)),
          a)
        ) {
          case 0:
            t = El(null, t, r, e, n);
            break e;
          case 1:
            t = zi(null, t, r, e, n);
            break e;
          case 11:
            t = Ni(null, t, r, e, n);
            break e;
          case 14:
            t = Ci(null, t, r, Pe(r.type, e), n);
            break e;
        }
        throw Error(b(306, r, ''));
      }
      return t;
    case 0:
      return (
        (r = t.type),
        (a = t.pendingProps),
        (a = t.elementType === r ? a : Pe(r, a)),
        El(e, t, r, a, n)
      );
    case 1:
      return (
        (r = t.type),
        (a = t.pendingProps),
        (a = t.elementType === r ? a : Pe(r, a)),
        zi(e, t, r, a, n)
      );
    case 3:
      e: {
        if ((js(t), e === null)) throw Error(b(387));
        (r = t.pendingProps),
          (l = t.memoizedState),
          (a = l.element),
          as(e, t),
          Wr(t, r, null, n);
        var o = t.memoizedState;
        if (((r = o.element), l.isDehydrated))
          if (
            ((l = {
              element: r,
              isDehydrated: !1,
              cache: o.cache,
              pendingSuspenseBoundaries: o.pendingSuspenseBoundaries,
              transitions: o.transitions,
            }),
            (t.updateQueue.baseState = l),
            (t.memoizedState = l),
            t.flags & 256)
          ) {
            (a = nn(Error(b(423)), t)), (t = Pi(e, t, r, n, a));
            break e;
          } else if (r !== a) {
            (a = nn(Error(b(424)), t)), (t = Pi(e, t, r, n, a));
            break e;
          } else
            for (
              ge = ot(t.stateNode.containerInfo.firstChild),
                be = t,
                F = !0,
                je = null,
                n = ns(t, null, r, n),
                t.child = n;
              n;

            )
              (n.flags = (n.flags & -3) | 4096), (n = n.sibling);
        else {
          if ((Zt(), r === a)) {
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
        ls(t),
        e === null && wl(t),
        (r = t.type),
        (a = t.pendingProps),
        (l = e !== null ? e.memoizedProps : null),
        (o = a.children),
        ml(r, a) ? (o = null) : l !== null && ml(r, l) && (t.flags |= 32),
        Ls(e, t),
        oe(e, t, o, n),
        t.child
      );
    case 6:
      return e === null && wl(t), null;
    case 13:
      return Ms(e, t, n);
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
        (a = t.pendingProps),
        (a = t.elementType === r ? a : Pe(r, a)),
        Ni(e, t, r, a, n)
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
          (a = t.pendingProps),
          (l = t.memoizedProps),
          (o = a.value),
          I(Hr, r._currentValue),
          (r._currentValue = o),
          l !== null)
        )
          if (Re(l.value, o)) {
            if (l.children === a.children && !fe.current) {
              t = qe(e, t, n);
              break e;
            }
          } else
            for (l = t.child, l !== null && (l.return = t); l !== null; ) {
              var u = l.dependencies;
              if (u !== null) {
                o = l.child;
                for (var i = u.firstContext; i !== null; ) {
                  if (i.context === r) {
                    if (l.tag === 1) {
                      (i = Be(-1, n & -n)), (i.tag = 2);
                      var c = l.updateQueue;
                      if (c !== null) {
                        c = c.shared;
                        var h = c.pending;
                        h === null
                          ? (i.next = i)
                          : ((i.next = h.next), (h.next = i)),
                          (c.pending = i);
                      }
                    }
                    (l.lanes |= n),
                      (i = l.alternate),
                      i !== null && (i.lanes |= n),
                      kl(l.return, n, t),
                      (u.lanes |= n);
                    break;
                  }
                  i = i.next;
                }
              } else if (l.tag === 10) o = l.type === t.type ? null : l.child;
              else if (l.tag === 18) {
                if (((o = l.return), o === null)) throw Error(b(341));
                (o.lanes |= n),
                  (u = o.alternate),
                  u !== null && (u.lanes |= n),
                  kl(o, n, t),
                  (o = l.sibling);
              } else o = l.child;
              if (o !== null) o.return = l;
              else
                for (o = l; o !== null; ) {
                  if (o === t) {
                    o = null;
                    break;
                  }
                  if (((l = o.sibling), l !== null)) {
                    (l.return = o.return), (o = l);
                    break;
                  }
                  o = o.return;
                }
              l = o;
            }
        oe(e, t, a.children, n), (t = t.child);
      }
      return t;
    case 9:
      return (
        (a = t.type),
        (r = t.pendingProps.children),
        Yt(t, n),
        (a = Ee(a)),
        (r = r(a)),
        (t.flags |= 1),
        oe(e, t, r, n),
        t.child
      );
    case 14:
      return (
        (r = t.type),
        (a = Pe(r, t.pendingProps)),
        (a = Pe(r.type, a)),
        Ci(e, t, r, a, n)
      );
    case 15:
      return zs(e, t, t.type, t.pendingProps, n);
    case 17:
      return (
        (r = t.type),
        (a = t.pendingProps),
        (a = t.elementType === r ? a : Pe(r, a)),
        Nr(e, t),
        (t.tag = 1),
        pe(r) ? ((e = !0), Ar(t)) : (e = !1),
        Yt(t, n),
        Es(t, r, a),
        Sl(t, r, a, n),
        Nl(null, t, r, !0, e, n)
      );
    case 19:
      return Ts(e, t, n);
    case 22:
      return Ps(e, t, n);
  }
  throw Error(b(156, t.tag));
};
function Ks(e, t) {
  return xu(e, t);
}
function xf(e, t, n, r) {
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
  return new xf(e, t, n, r);
}
function Co(e) {
  return (e = e.prototype), !(!e || !e.isReactComponent);
}
function Sf(e) {
  if (typeof e == 'function') return Co(e) ? 1 : 0;
  if (e != null) {
    if (((e = e.$$typeof), e === Wl)) return 11;
    if (e === Ql) return 14;
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
function Pr(e, t, n, r, a, l) {
  var o = 2;
  if (((r = e), typeof e == 'function')) Co(e) && (o = 1);
  else if (typeof e == 'string') o = 5;
  else
    e: switch (e) {
      case Rt:
        return _t(n.children, a, l, t);
      case Bl:
        (o = 8), (a |= 8);
        break;
      case Xa:
        return (
          (e = Se(12, n, t, a | 2)), (e.elementType = Xa), (e.lanes = l), e
        );
      case qa:
        return (e = Se(13, n, t, a)), (e.elementType = qa), (e.lanes = l), e;
      case Ya:
        return (e = Se(19, n, t, a)), (e.elementType = Ya), (e.lanes = l), e;
      case lu:
        return da(n, a, l, t);
      default:
        if (typeof e == 'object' && e !== null)
          switch (e.$$typeof) {
            case ru:
              o = 10;
              break e;
            case au:
              o = 9;
              break e;
            case Wl:
              o = 11;
              break e;
            case Ql:
              o = 14;
              break e;
            case Ge:
              (o = 16), (r = null);
              break e;
          }
        throw Error(b(130, e == null ? e : typeof e, ''));
    }
  return (
    (t = Se(o, n, t, a)), (t.elementType = e), (t.type = r), (t.lanes = l), t
  );
}
function _t(e, t, n, r) {
  return (e = Se(7, e, r, t)), (e.lanes = n), e;
}
function da(e, t, n, r) {
  return (
    (e = Se(22, e, r, t)),
    (e.elementType = lu),
    (e.lanes = n),
    (e.stateNode = { isHidden: !1 }),
    e
  );
}
function Ha(e, t, n) {
  return (e = Se(6, e, null, t)), (e.lanes = n), e;
}
function Ba(e, t, n) {
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
function _f(e, t, n, r, a) {
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
    (this.eventTimes = _a(0)),
    (this.expirationTimes = _a(-1)),
    (this.entangledLanes =
      this.finishedLanes =
      this.mutableReadLanes =
      this.expiredLanes =
      this.pingedLanes =
      this.suspendedLanes =
      this.pendingLanes =
        0),
    (this.entanglements = _a(0)),
    (this.identifierPrefix = r),
    (this.onRecoverableError = a),
    (this.mutableSourceEagerHydrationData = null);
}
function zo(e, t, n, r, a, l, o, u, i) {
  return (
    (e = new _f(e, t, n, u, i)),
    t === 1 ? ((t = 1), l === !0 && (t |= 8)) : (t = 0),
    (l = Se(3, null, null, t)),
    (e.current = l),
    (l.stateNode = e),
    (l.memoizedState = {
      element: r,
      isDehydrated: n,
      cache: null,
      transitions: null,
      pendingSuspenseBoundaries: null,
    }),
    co(l),
    e
  );
}
function Ef(e, t, n) {
  var r =
    3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
  return {
    $$typeof: Tt,
    key: r == null ? null : '' + r,
    children: e,
    containerInfo: t,
    implementation: n,
  };
}
function Gs(e) {
  if (!e) return ft;
  e = e._reactInternals;
  e: {
    if (jt(e) !== e || e.tag !== 1) throw Error(b(170));
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
    throw Error(b(171));
  }
  if (e.tag === 1) {
    var n = e.type;
    if (pe(n)) return Ku(e, n, t);
  }
  return t;
}
function Js(e, t, n, r, a, l, o, u, i) {
  return (
    (e = zo(n, r, !0, e, a, l, o, u, i)),
    (e.context = Gs(null)),
    (n = e.current),
    (r = ie()),
    (a = st(n)),
    (l = Be(r, a)),
    (l.callback = t ?? null),
    it(n, l, a),
    (e.current.lanes = a),
    Yn(e, a, r),
    he(e, r),
    e
  );
}
function fa(e, t, n, r) {
  var a = t.current,
    l = ie(),
    o = st(a);
  return (
    (n = Gs(n)),
    t.context === null ? (t.context = n) : (t.pendingContext = n),
    (t = Be(l, o)),
    (t.payload = { element: e }),
    (r = r === void 0 ? null : r),
    r !== null && (t.callback = r),
    (e = it(a, t, o)),
    e !== null && (Te(e, a, o, l), Sr(e, a, o)),
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
function Po(e, t) {
  Ui(e, t), (e = e.alternate) && Ui(e, t);
}
function Nf() {
  return null;
}
var Zs =
  typeof reportError == 'function'
    ? reportError
    : function (e) {
        console.error(e);
      };
function Lo(e) {
  this._internalRoot = e;
}
pa.prototype.render = Lo.prototype.render = function (e) {
  var t = this._internalRoot;
  if (t === null) throw Error(b(409));
  fa(e, t, null, null);
};
pa.prototype.unmount = Lo.prototype.unmount = function () {
  var e = this._internalRoot;
  if (e !== null) {
    this._internalRoot = null;
    var t = e.containerInfo;
    Pt(function () {
      fa(null, e, null, null);
    }),
      (t[Qe] = null);
  }
};
function pa(e) {
  this._internalRoot = e;
}
pa.prototype.unstable_scheduleHydration = function (e) {
  if (e) {
    var t = Pu();
    e = { blockedOn: null, target: e, priority: t };
    for (var n = 0; n < Ze.length && t !== 0 && t < Ze[n].priority; n++);
    Ze.splice(n, 0, e), n === 0 && ju(e);
  }
};
function jo(e) {
  return !(!e || (e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11));
}
function ha(e) {
  return !(
    !e ||
    (e.nodeType !== 1 &&
      e.nodeType !== 9 &&
      e.nodeType !== 11 &&
      (e.nodeType !== 8 || e.nodeValue !== ' react-mount-point-unstable '))
  );
}
function Ai() {}
function Cf(e, t, n, r, a) {
  if (a) {
    if (typeof r == 'function') {
      var l = r;
      r = function () {
        var c = Zr(o);
        l.call(c);
      };
    }
    var o = Js(t, r, e, 0, null, !1, !1, '', Ai);
    return (
      (e._reactRootContainer = o),
      (e[Qe] = o.current),
      Un(e.nodeType === 8 ? e.parentNode : e),
      Pt(),
      o
    );
  }
  for (; (a = e.lastChild); ) e.removeChild(a);
  if (typeof r == 'function') {
    var u = r;
    r = function () {
      var c = Zr(i);
      u.call(c);
    };
  }
  var i = zo(e, 0, !1, null, null, !1, !1, '', Ai);
  return (
    (e._reactRootContainer = i),
    (e[Qe] = i.current),
    Un(e.nodeType === 8 ? e.parentNode : e),
    Pt(function () {
      fa(t, i, n, r);
    }),
    i
  );
}
function ma(e, t, n, r, a) {
  var l = n._reactRootContainer;
  if (l) {
    var o = l;
    if (typeof a == 'function') {
      var u = a;
      a = function () {
        var i = Zr(o);
        u.call(i);
      };
    }
    fa(t, o, e, a);
  } else o = Cf(n, t, e, a, r);
  return Zr(o);
}
Cu = function (e) {
  switch (e.tag) {
    case 3:
      var t = e.stateNode;
      if (t.current.memoizedState.isDehydrated) {
        var n = wn(t.pendingLanes);
        n !== 0 &&
          (Yl(t, n | 1), he(t, W()), !(T & 6) && ((rn = W() + 500), mt()));
      }
      break;
    case 13:
      Pt(function () {
        var r = Xe(e, 1);
        if (r !== null) {
          var a = ie();
          Te(r, e, 1, a);
        }
      }),
        Po(e, 1);
  }
};
Kl = function (e) {
  if (e.tag === 13) {
    var t = Xe(e, 134217728);
    if (t !== null) {
      var n = ie();
      Te(t, e, 134217728, n);
    }
    Po(e, 134217728);
  }
};
zu = function (e) {
  if (e.tag === 13) {
    var t = st(e),
      n = Xe(e, t);
    if (n !== null) {
      var r = ie();
      Te(n, e, t, r);
    }
    Po(e, t);
  }
};
Pu = function () {
  return R;
};
Lu = function (e, t) {
  var n = R;
  try {
    return (R = e), t();
  } finally {
    R = n;
  }
};
ll = function (e, t, n) {
  switch (t) {
    case 'input':
      if ((Ja(e, n), (t = n.name), n.type === 'radio' && t != null)) {
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
            var a = la(r);
            if (!a) throw Error(b(90));
            iu(r), Ja(r, a);
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
bu = Pt;
var zf = { usingClientEntryPoint: !1, Events: [Gn, Ft, la, hu, mu, _o] },
  bn = {
    findFiberByHostInstance: wt,
    bundleType: 0,
    version: '18.3.1',
    rendererPackageName: 'react-dom',
  },
  Pf = {
    bundleType: bn.bundleType,
    version: bn.version,
    rendererPackageName: bn.rendererPackageName,
    rendererConfig: bn.rendererConfig,
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
    findFiberByHostInstance: bn.findFiberByHostInstance || Nf,
    findHostInstancesForRefresh: null,
    scheduleRefresh: null,
    scheduleRoot: null,
    setRefreshHandler: null,
    getCurrentFiber: null,
    reconcilerVersion: '18.3.1-next-f1338f8080-20240426',
  };
if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < 'u') {
  var br = __REACT_DEVTOOLS_GLOBAL_HOOK__;
  if (!br.isDisabled && br.supportsFiber)
    try {
      (ta = br.inject(Pf)), (Fe = br);
    } catch {}
}
ve.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = zf;
ve.createPortal = function (e, t) {
  var n =
    2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
  if (!jo(t)) throw Error(b(200));
  return Ef(e, t, null, n);
};
ve.createRoot = function (e, t) {
  if (!jo(e)) throw Error(b(299));
  var n = !1,
    r = '',
    a = Zs;
  return (
    t != null &&
      (t.unstable_strictMode === !0 && (n = !0),
      t.identifierPrefix !== void 0 && (r = t.identifierPrefix),
      t.onRecoverableError !== void 0 && (a = t.onRecoverableError)),
    (t = zo(e, 1, !1, null, null, n, !1, r, a)),
    (e[Qe] = t.current),
    Un(e.nodeType === 8 ? e.parentNode : e),
    new Lo(t)
  );
};
ve.findDOMNode = function (e) {
  if (e == null) return null;
  if (e.nodeType === 1) return e;
  var t = e._reactInternals;
  if (t === void 0)
    throw typeof e.render == 'function'
      ? Error(b(188))
      : ((e = Object.keys(e).join(',')), Error(b(268, e)));
  return (e = wu(t)), (e = e === null ? null : e.stateNode), e;
};
ve.flushSync = function (e) {
  return Pt(e);
};
ve.hydrate = function (e, t, n) {
  if (!ha(t)) throw Error(b(200));
  return ma(null, e, t, !0, n);
};
ve.hydrateRoot = function (e, t, n) {
  if (!jo(e)) throw Error(b(405));
  var r = (n != null && n.hydratedSources) || null,
    a = !1,
    l = '',
    o = Zs;
  if (
    (n != null &&
      (n.unstable_strictMode === !0 && (a = !0),
      n.identifierPrefix !== void 0 && (l = n.identifierPrefix),
      n.onRecoverableError !== void 0 && (o = n.onRecoverableError)),
    (t = Js(t, null, e, 1, n ?? null, a, !1, l, o)),
    (e[Qe] = t.current),
    Un(e),
    r)
  )
    for (e = 0; e < r.length; e++)
      (n = r[e]),
        (a = n._getVersion),
        (a = a(n._source)),
        t.mutableSourceEagerHydrationData == null
          ? (t.mutableSourceEagerHydrationData = [n, a])
          : t.mutableSourceEagerHydrationData.push(n, a);
  return new pa(t);
};
ve.render = function (e, t, n) {
  if (!ha(t)) throw Error(b(200));
  return ma(null, e, t, !1, n);
};
ve.unmountComponentAtNode = function (e) {
  if (!ha(e)) throw Error(b(40));
  return e._reactRootContainer
    ? (Pt(function () {
        ma(null, null, e, !1, function () {
          (e._reactRootContainer = null), (e[Qe] = null);
        });
      }),
      !0)
    : !1;
};
ve.unstable_batchedUpdates = _o;
ve.unstable_renderSubtreeIntoContainer = function (e, t, n, r) {
  if (!ha(n)) throw Error(b(200));
  if (e == null || e._reactInternals === void 0) throw Error(b(38));
  return ma(e, t, n, !1, r);
};
ve.version = '18.3.1-next-f1338f8080-20240426';
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
ec(), (Zi.exports = ve);
var Lf = Zi.exports,
  Vi = Lf;
(Wa.createRoot = Vi.createRoot), (Wa.hydrateRoot = Vi.hydrateRoot);
const jf = ({ devices: e, setActiveView: t }) => {
    const [n, r] = Z.useState(''),
      a = (i) => {
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
      l = e.filter((i) => {
        var c, h;
        return (
          ((c = i.name) == null
            ? void 0
            : c.toLowerCase().includes(n.toLowerCase())) ||
          ((h = i.serial) == null
            ? void 0
            : h.toLowerCase().includes(n.toLowerCase()))
        );
      }),
      o = (i, c) => {
        i.preventDefault(), i.stopPropagation();
        const h = new CustomEvent('hass-more-info', {
          bubbles: !0,
          composed: !0,
          detail: { entityId: c },
        });
        i.currentTarget.dispatchEvent(h);
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
                children: l.map((i) => {
                  var c;
                  const h =
                    (c = i.model) != null && c.startsWith('MV') && i.lanIp
                      ? `rtsp://${i.lanIp}:9000/live`
                      : null;
                  return g.jsxs(
                    'tr',
                    {
                      className:
                        'border-b border-light-border dark:border-dark-border hover:bg-light-hover dark:hover:bg-dark-hover cursor-pointer',
                      onClick: (m) => {
                        i.entity_id ? o(m, i.entity_id) : u(m, i.serial);
                      },
                      children: [
                        g.jsx('td', {
                          className: 'p-4',
                          children: g.jsxs('div', {
                            style: { display: 'flex', alignItems: 'center' },
                            children: [
                              g.jsx('ha-icon', {
                                icon: a(i.model),
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
                          children: h
                            ? g.jsx('a', {
                                href: h,
                                className:
                                  'text-blue-500 hover:text-blue-700 underline',
                                onClick: (m) => m.stopPropagation(),
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
                            onClick: (m) => u(m, i.serial),
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
  Mf = ({ ssids: e }) =>
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
  Tf = ({ networkId: e }) => {
    const [t, n] = Z.useState([]),
      [r, a] = Z.useState(!1),
      [l, o] = Z.useState(null);
    return (
      Z.useEffect(() => {
        (async () => {
          var u;
          if (e) {
            a(!0), o(null);
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
                  a(!1);
                return;
              }
              const i =
                ((u = document.querySelector('meraki-panel')) == null
                  ? void 0
                  : u.hass) || window.hass;
              if (!i) throw new Error('Hass connection not available');
              const c = window.CONFIG_ENTRY_ID,
                h = await i.connection.sendMessagePromise({
                  type: 'meraki_ha/get_network_events',
                  config_entry_id: c,
                  network_id: e,
                  per_page: 10,
                });
              h && h.events ? n(h.events) : n([]);
            } catch (i) {
              console.error('Error fetching events:', i),
                o(i.message || 'Failed to fetch events');
            } finally {
              a(!1);
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
              l &&
                g.jsxs('p', {
                  className: 'text-red-500',
                  children: ['Error: ', l],
                }),
              !r &&
                !l &&
                t.length === 0 &&
                g.jsx('p', { children: 'No events found.' }),
              !r &&
                !l &&
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
  Rf = ({ data: e, onToggle: t, setActiveView: n }) => {
    const [r, a] = Z.useState(null),
      l = (i) => {
        a(r === i ? null : i);
      },
      { networks: o, devices: u } = e;
    return !o || o.length === 0
      ? g.jsx('p', { children: 'No networks found.' })
      : g.jsx('div', {
          style: { display: 'flex', flexDirection: 'column', gap: '16px' },
          children: o.map((i) => {
            const c = r === i.id,
              h = i.ssids ? i.ssids.filter((p) => p.enabled).length : 0,
              m = i.ssids ? i.ssids.length : 0;
            return g.jsxs(
              'ha-card',
              {
                children: [
                  g.jsxs('div', {
                    className: 'card-header',
                    onClick: () => l(i.id),
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
                        g.jsx(jf, {
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
                                  h,
                                  ' / ',
                                  m,
                                  ' SSIDs Enabled',
                                ],
                              }),
                              g.jsx(Mf, { ssids: i.ssids }),
                            ],
                          }),
                        g.jsx(Tf, { networkId: i.id }),
                      ],
                    }),
                ],
              },
              i.id
            );
          }),
        });
  },
  If = ({ activeView: e, setActiveView: t, data: n }) => {
    const r = n.devices.find((m) => m.serial === e.deviceId);
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
      name: a,
      model: l,
      serial: o,
      firmware: u,
      status: i,
      status_messages: c = [],
      entities: h = [],
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
            g.jsx('h2', { className: 'text-2xl font-bold mb-2', children: a }),
            g.jsxs('div', {
              className: 'grid grid-cols-1 md:grid-cols-3 gap-4 text-sm',
              children: [
                g.jsxs('div', {
                  children: [g.jsx('strong', { children: 'Model:' }), ' ', l],
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
                  children: c.map((m, p) =>
                    g.jsx('li', { className: 'mb-1', children: m }, p)
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
                    children: h.map((m) =>
                      g.jsxs(
                        'tr',
                        {
                          className:
                            'border-b border-light-border dark:border-dark-border last:border-b-0',
                          children: [
                            g.jsx('td', {
                              className: 'p-4',
                              children: m.name,
                            }),
                            g.jsx('td', {
                              className: 'p-4',
                              children: m.entity_id,
                            }),
                            g.jsx('td', {
                              className: 'p-4',
                              children: m.state,
                            }),
                          ],
                        },
                        m.entity_id
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
  Of = ({ options: e, configEntryId: t, onClose: n }) => {
    const [r, a] = Z.useState(e),
      [l, o] = Z.useState(!1),
      u = (h) => {
        a((m) => ({ ...m, [h]: !m[h] }));
      },
      i = async () => {
        o(!0);
        try {
          const h = window.hass;
          h && h.connection
            ? await h.connection.sendMessagePromise({
                type: 'meraki_ha/update_options',
                config_entry_id: t,
                options: r,
              })
            : console.log('Saving options:', r);
        } catch (h) {
          console.error('Failed to save options:', h),
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
            children: c.map((h) =>
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
                          children: h.label,
                        }),
                        g.jsx('span', {
                          className:
                            'text-sm text-gray-500 dark:text-gray-400',
                          children: h.description,
                        }),
                      ],
                    }),
                    g.jsx('ha-switch', {
                      checked: r[h.key] !== !1,
                      onClick: (m) => {
                        m.stopPropagation(), u(h.key);
                      },
                    }),
                  ],
                },
                h.key
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
                disabled: l,
                children: 'Cancel',
              }),
              g.jsx('button', {
                onClick: i,
                className:
                  'px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50',
                disabled: l,
                children: l ? 'Saving...' : 'Save & Reload',
              }),
            ],
          }),
        ],
      }),
    });
  },
  Df = () => {
    const [e, t] = Z.useState(null),
      [n, r] = Z.useState(!0),
      [a, l] = Z.useState(null),
      [o, u] = Z.useState({ view: 'dashboard', deviceId: void 0 }),
      [i, c] = Z.useState(!1),
      h = () => {
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
          const M = window.hass;
          M && M.auth && M.auth.accessToken && (p = M.auth.accessToken);
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
            l('No access token provided.'), r(!1);
            return;
          }
        const w = `${
            window.HA_URL
              ? window.HA_URL.replace(/^http/, 'ws')
              : window.location.protocol === 'https:'
              ? 'wss://' + window.location.host
              : 'ws://' + window.location.host
          }/api/websocket`,
          v = new WebSocket(w);
        let k = 1;
        return (
          (v.onopen = () => {
            console.log('WebSocket connection established'),
              v.send(JSON.stringify({ type: 'auth', access_token: p }));
          }),
          (v.onmessage = (M) => {
            var f, s;
            const d = JSON.parse(M.data);
            d.type === 'auth_ok'
              ? (console.log('Authenticated successfully'),
                v.send(
                  JSON.stringify({
                    id: k,
                    type: 'meraki_ha/get_config',
                    config_entry_id: window.CONFIG_ENTRY_ID,
                  })
                ))
              : d.type === 'auth_invalid'
              ? (console.error('Authentication failed:', d.message),
                l('Authentication failed. Please check your token.'),
                r(!1),
                localStorage.removeItem('meraki_ha_llat'))
              : d.id === k &&
                (d.type === 'result'
                  ? (d.success
                      ? t(d.result)
                      : (console.error(
                          'Failed to fetch Meraki data:',
                          d.error
                        ),
                        l(
                          `Failed to fetch Meraki data: ${
                            (f = d.error) == null ? void 0 : f.message
                          }`
                        )),
                    r(!1))
                  : d.type === 'result' &&
                    d.success === !1 &&
                    (console.error('Failed to fetch Meraki data:', d.error),
                    l(
                      `Failed to fetch Meraki data: ${
                        (s = d.error) == null ? void 0 : s.message
                      }`
                    ),
                    r(!1)));
          }),
          (v.onerror = (M) => {
            console.error('WebSocket error:', M);
          }),
          () => {
            v.readyState === 1 && v.close();
          }
        );
      };
    if (
      (Z.useEffect(() => {
        h();
      }, []),
      n)
    )
      return g.jsx('div', { className: 'p-4', children: 'Loading...' });
    if (a)
      return g.jsxs('div', {
        className: 'p-4 text-red-500',
        children: ['Error: ', a],
      });
    const m = (p, w) => {
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
          ? g.jsx(Rf, { data: e, onToggle: m, setActiveView: u })
          : g.jsx(If, { activeView: o, setActiveView: u, data: e }),
        i &&
          e &&
          g.jsx(Of, {
            options: e.options || {},
            configEntryId: window.CONFIG_ENTRY_ID || e.config_entry_id,
            onClose: () => c(!1),
          }),
      ],
    });
  },
  Ff =
    '*,:before,:after{--tw-border-spacing-x: 0;--tw-border-spacing-y: 0;--tw-translate-x: 0;--tw-translate-y: 0;--tw-rotate: 0;--tw-skew-x: 0;--tw-skew-y: 0;--tw-scale-x: 1;--tw-scale-y: 1;--tw-pan-x: ;--tw-pan-y: ;--tw-pinch-zoom: ;--tw-scroll-snap-strictness: proximity;--tw-gradient-from-position: ;--tw-gradient-via-position: ;--tw-gradient-to-position: ;--tw-ordinal: ;--tw-slashed-zero: ;--tw-numeric-figure: ;--tw-numeric-spacing: ;--tw-numeric-fraction: ;--tw-ring-inset: ;--tw-ring-offset-width: 0px;--tw-ring-offset-color: #fff;--tw-ring-color: rgb(59 130 246 / .5);--tw-ring-offset-shadow: 0 0 #0000;--tw-ring-shadow: 0 0 #0000;--tw-shadow: 0 0 #0000;--tw-shadow-colored: 0 0 #0000;--tw-blur: ;--tw-brightness: ;--tw-contrast: ;--tw-grayscale: ;--tw-hue-rotate: ;--tw-invert: ;--tw-saturate: ;--tw-sepia: ;--tw-drop-shadow: ;--tw-backdrop-blur: ;--tw-backdrop-brightness: ;--tw-backdrop-contrast: ;--tw-backdrop-grayscale: ;--tw-backdrop-hue-rotate: ;--tw-backdrop-invert: ;--tw-backdrop-opacity: ;--tw-backdrop-saturate: ;--tw-backdrop-sepia: ;--tw-contain-size: ;--tw-contain-layout: ;--tw-contain-paint: ;--tw-contain-style: }::backdrop{--tw-border-spacing-x: 0;--tw-border-spacing-y: 0;--tw-translate-x: 0;--tw-translate-y: 0;--tw-rotate: 0;--tw-skew-x: 0;--tw-skew-y: 0;--tw-scale-x: 1;--tw-scale-y: 1;--tw-pan-x: ;--tw-pan-y: ;--tw-pinch-zoom: ;--tw-scroll-snap-strictness: proximity;--tw-gradient-from-position: ;--tw-gradient-via-position: ;--tw-gradient-to-position: ;--tw-ordinal: ;--tw-slashed-zero: ;--tw-numeric-figure: ;--tw-numeric-spacing: ;--tw-numeric-fraction: ;--tw-ring-inset: ;--tw-ring-offset-width: 0px;--tw-ring-offset-color: #fff;--tw-ring-color: rgb(59 130 246 / .5);--tw-ring-offset-shadow: 0 0 #0000;--tw-ring-shadow: 0 0 #0000;--tw-shadow: 0 0 #0000;--tw-shadow-colored: 0 0 #0000;--tw-blur: ;--tw-brightness: ;--tw-contrast: ;--tw-grayscale: ;--tw-hue-rotate: ;--tw-invert: ;--tw-saturate: ;--tw-sepia: ;--tw-drop-shadow: ;--tw-backdrop-blur: ;--tw-backdrop-brightness: ;--tw-backdrop-contrast: ;--tw-backdrop-grayscale: ;--tw-backdrop-hue-rotate: ;--tw-backdrop-invert: ;--tw-backdrop-opacity: ;--tw-backdrop-saturate: ;--tw-backdrop-sepia: ;--tw-contain-size: ;--tw-contain-layout: ;--tw-contain-paint: ;--tw-contain-style: }*,:before,:after{box-sizing:border-box;border-width:0;border-style:solid;border-color:#e5e7eb}:before,:after{--tw-content: ""}html,:host{line-height:1.5;-webkit-text-size-adjust:100%;-moz-tab-size:4;-o-tab-size:4;tab-size:4;font-family:ui-sans-serif,system-ui,sans-serif,"Apple Color Emoji","Segoe UI Emoji",Segoe UI Symbol,"Noto Color Emoji";font-feature-settings:normal;font-variation-settings:normal;-webkit-tap-highlight-color:transparent}body{margin:0;line-height:inherit}hr{height:0;color:inherit;border-top-width:1px}abbr:where([title]){-webkit-text-decoration:underline dotted;text-decoration:underline dotted}h1,h2,h3,h4,h5,h6{font-size:inherit;font-weight:inherit}a{color:inherit;text-decoration:inherit}b,strong{font-weight:bolder}code,kbd,samp,pre{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace;font-feature-settings:normal;font-variation-settings:normal;font-size:1em}small{font-size:80%}sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline}sub{bottom:-.25em}sup{top:-.5em}table{text-indent:0;border-color:inherit;border-collapse:collapse}button,input,optgroup,select,textarea{font-family:inherit;font-feature-settings:inherit;font-variation-settings:inherit;font-size:100%;font-weight:inherit;line-height:inherit;letter-spacing:inherit;color:inherit;margin:0;padding:0}button,select{text-transform:none}button,input:where([type=button]),input:where([type=reset]),input:where([type=submit]){-webkit-appearance:button;background-color:transparent;background-image:none}:-moz-focusring{outline:auto}:-moz-ui-invalid{box-shadow:none}progress{vertical-align:baseline}::-webkit-inner-spin-button,::-webkit-outer-spin-button{height:auto}[type=search]{-webkit-appearance:textfield;outline-offset:-2px}::-webkit-search-decoration{-webkit-appearance:none}::-webkit-file-upload-button{-webkit-appearance:button;font:inherit}summary{display:list-item}blockquote,dl,dd,h1,h2,h3,h4,h5,h6,hr,figure,p,pre{margin:0}fieldset{margin:0;padding:0}legend{padding:0}ol,ul,menu{list-style:none;margin:0;padding:0}dialog{padding:0}textarea{resize:vertical}input::-moz-placeholder,textarea::-moz-placeholder{opacity:1;color:#9ca3af}input::placeholder,textarea::placeholder{opacity:1;color:#9ca3af}button,[role=button]{cursor:pointer}:disabled{cursor:default}img,svg,video,canvas,audio,iframe,embed,object{display:block;vertical-align:middle}img,video{max-width:100%;height:auto}[hidden]:where(:not([hidden=until-found])){display:none}.fixed{position:fixed}.relative{position:relative}.inset-0{top:0;right:0;bottom:0;left:0}.z-50{z-index:50}.mb-1{margin-bottom:.25rem}.mb-2{margin-bottom:.5rem}.mb-4{margin-bottom:1rem}.mb-8{margin-bottom:2rem}.mr-4{margin-right:1rem}.mt-4{margin-top:1rem}.mt-6{margin-top:1.5rem}.block{display:block}.inline{display:inline}.flex{display:flex}.table{display:table}.grid{display:grid}.h-full{height:100%}.max-h-96{max-height:24rem}.w-16{width:4rem}.w-full{width:100%}.min-w-full{min-width:100%}.max-w-md{max-width:28rem}.cursor-pointer{cursor:pointer}.grid-cols-1{grid-template-columns:repeat(1,minmax(0,1fr))}.flex-col{flex-direction:column}.items-center{align-items:center}.justify-end{justify-content:flex-end}.justify-center{justify-content:center}.justify-between{justify-content:space-between}.gap-4{gap:1rem}.space-y-4>:not([hidden])~:not([hidden]){--tw-space-y-reverse: 0;margin-top:calc(1rem * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(1rem * var(--tw-space-y-reverse))}.overflow-x-auto{overflow-x:auto}.overflow-y-auto{overflow-y:auto}.whitespace-nowrap{white-space:nowrap}.rounded{border-radius:.25rem}.rounded-full{border-radius:9999px}.rounded-lg{border-radius:.5rem}.border{border-width:1px}.border-b{border-bottom-width:1px}.border-l-4{border-left-width:4px}.border-gray-200{--tw-border-opacity: 1;border-color:rgb(229 231 235 / var(--tw-border-opacity, 1))}.border-gray-300{--tw-border-opacity: 1;border-color:rgb(209 213 219 / var(--tw-border-opacity, 1))}.border-light-border{--tw-border-opacity: 1;border-color:rgb(222 226 230 / var(--tw-border-opacity, 1))}.border-yellow-500{--tw-border-opacity: 1;border-color:rgb(234 179 8 / var(--tw-border-opacity, 1))}.bg-blue-600{--tw-bg-opacity: 1;background-color:rgb(37 99 235 / var(--tw-bg-opacity, 1))}.bg-gray-50{--tw-bg-opacity: 1;background-color:rgb(249 250 251 / var(--tw-bg-opacity, 1))}.bg-gray-600{--tw-bg-opacity: 1;background-color:rgb(75 85 99 / var(--tw-bg-opacity, 1))}.bg-light-background{--tw-bg-opacity: 1;background-color:rgb(248 249 250 / var(--tw-bg-opacity, 1))}.bg-light-card,.bg-white{--tw-bg-opacity: 1;background-color:rgb(255 255 255 / var(--tw-bg-opacity, 1))}.bg-yellow-100{--tw-bg-opacity: 1;background-color:rgb(254 249 195 / var(--tw-bg-opacity, 1))}.bg-opacity-50{--tw-bg-opacity: .5}.p-2{padding:.5rem}.p-3{padding:.75rem}.p-4{padding:1rem}.p-6{padding:1.5rem}.px-4{padding-left:1rem;padding-right:1rem}.py-2{padding-top:.5rem;padding-bottom:.5rem}.text-left{text-align:left}.text-center{text-align:center}.text-2xl{font-size:1.5rem;line-height:2rem}.text-lg{font-size:1.125rem;line-height:1.75rem}.text-sm{font-size:.875rem;line-height:1.25rem}.text-xl{font-size:1.25rem;line-height:1.75rem}.font-bold{font-weight:700}.font-medium{font-weight:500}.font-semibold{font-weight:600}.capitalize{text-transform:capitalize}.text-blue-500{--tw-text-opacity: 1;color:rgb(59 130 246 / var(--tw-text-opacity, 1))}.text-cisco-blue{--tw-text-opacity: 1;color:rgb(0 188 235 / var(--tw-text-opacity, 1))}.text-dark-text{--tw-text-opacity: 1;color:rgb(232 234 237 / var(--tw-text-opacity, 1))}.text-gray-400{--tw-text-opacity: 1;color:rgb(156 163 175 / var(--tw-text-opacity, 1))}.text-gray-500{--tw-text-opacity: 1;color:rgb(107 114 128 / var(--tw-text-opacity, 1))}.text-gray-700{--tw-text-opacity: 1;color:rgb(55 65 81 / var(--tw-text-opacity, 1))}.text-gray-900{--tw-text-opacity: 1;color:rgb(17 24 39 / var(--tw-text-opacity, 1))}.text-red-500{--tw-text-opacity: 1;color:rgb(239 68 68 / var(--tw-text-opacity, 1))}.text-white{--tw-text-opacity: 1;color:rgb(255 255 255 / var(--tw-text-opacity, 1))}.text-yellow-700{--tw-text-opacity: 1;color:rgb(161 98 7 / var(--tw-text-opacity, 1))}.underline{text-decoration-line:underline}.shadow-lg{--tw-shadow: 0 10px 15px -3px rgb(0 0 0 / .1), 0 4px 6px -4px rgb(0 0 0 / .1);--tw-shadow-colored: 0 10px 15px -3px var(--tw-shadow-color), 0 4px 6px -4px var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000),var(--tw-ring-shadow, 0 0 #0000),var(--tw-shadow)}.shadow-md{--tw-shadow: 0 4px 6px -1px rgb(0 0 0 / .1), 0 2px 4px -2px rgb(0 0 0 / .1);--tw-shadow-colored: 0 4px 6px -1px var(--tw-shadow-color), 0 2px 4px -2px var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000),var(--tw-ring-shadow, 0 0 #0000),var(--tw-shadow)}.filter{filter:var(--tw-blur) var(--tw-brightness) var(--tw-contrast) var(--tw-grayscale) var(--tw-hue-rotate) var(--tw-invert) var(--tw-saturate) var(--tw-sepia) var(--tw-drop-shadow)}.transition-colors{transition-property:color,background-color,border-color,text-decoration-color,fill,stroke;transition-timing-function:cubic-bezier(.4,0,.2,1);transition-duration:.15s}.transition-shadow{transition-property:box-shadow;transition-timing-function:cubic-bezier(.4,0,.2,1);transition-duration:.15s}.duration-200{transition-duration:.2s}.last\\:border-b-0:last-child{border-bottom-width:0px}.hover\\:bg-blue-700:hover{--tw-bg-opacity: 1;background-color:rgb(29 78 216 / var(--tw-bg-opacity, 1))}.hover\\:bg-gray-100:hover{--tw-bg-opacity: 1;background-color:rgb(243 244 246 / var(--tw-bg-opacity, 1))}.hover\\:bg-gray-200:hover{--tw-bg-opacity: 1;background-color:rgb(229 231 235 / var(--tw-bg-opacity, 1))}.hover\\:bg-gray-50:hover{--tw-bg-opacity: 1;background-color:rgb(249 250 251 / var(--tw-bg-opacity, 1))}.hover\\:text-blue-700:hover{--tw-text-opacity: 1;color:rgb(29 78 216 / var(--tw-text-opacity, 1))}.hover\\:text-gray-700:hover{--tw-text-opacity: 1;color:rgb(55 65 81 / var(--tw-text-opacity, 1))}.hover\\:underline:hover{text-decoration-line:underline}.disabled\\:opacity-50:disabled{opacity:.5}.dark\\:border-dark-border:is(.dark *){--tw-border-opacity: 1;border-color:rgb(60 64 67 / var(--tw-border-opacity, 1))}.dark\\:border-gray-600:is(.dark *){--tw-border-opacity: 1;border-color:rgb(75 85 99 / var(--tw-border-opacity, 1))}.dark\\:border-gray-700:is(.dark *){--tw-border-opacity: 1;border-color:rgb(55 65 81 / var(--tw-border-opacity, 1))}.dark\\:bg-dark-background:is(.dark *){--tw-bg-opacity: 1;background-color:rgb(18 18 18 / var(--tw-bg-opacity, 1))}.dark\\:bg-dark-card:is(.dark *){--tw-bg-opacity: 1;background-color:rgb(30 30 30 / var(--tw-bg-opacity, 1))}.dark\\:bg-gray-800:is(.dark *){--tw-bg-opacity: 1;background-color:rgb(31 41 55 / var(--tw-bg-opacity, 1))}.dark\\:bg-yellow-900:is(.dark *){--tw-bg-opacity: 1;background-color:rgb(113 63 18 / var(--tw-bg-opacity, 1))}.dark\\:text-gray-100:is(.dark *){--tw-text-opacity: 1;color:rgb(243 244 246 / var(--tw-text-opacity, 1))}.dark\\:text-gray-300:is(.dark *){--tw-text-opacity: 1;color:rgb(209 213 219 / var(--tw-text-opacity, 1))}.dark\\:text-gray-400:is(.dark *){--tw-text-opacity: 1;color:rgb(156 163 175 / var(--tw-text-opacity, 1))}.dark\\:text-light-text:is(.dark *){--tw-text-opacity: 1;color:rgb(33 37 41 / var(--tw-text-opacity, 1))}.dark\\:text-yellow-200:is(.dark *){--tw-text-opacity: 1;color:rgb(254 240 138 / var(--tw-text-opacity, 1))}.dark\\:hover\\:bg-gray-700:hover:is(.dark *){--tw-bg-opacity: 1;background-color:rgb(55 65 81 / var(--tw-bg-opacity, 1))}@media (min-width: 768px){.md\\:grid-cols-2{grid-template-columns:repeat(2,minmax(0,1fr))}.md\\:grid-cols-3{grid-template-columns:repeat(3,minmax(0,1fr))}}@media (min-width: 1024px){.lg\\:grid-cols-5{grid-template-columns:repeat(5,minmax(0,1fr))}}';
class Uf extends HTMLElement {
  connectedCallback() {
    if (!this.shadowRoot) {
      this.attachShadow({ mode: 'open' });
      const t = document.createElement('div');
      t.id = 'root';
      const n = document.createElement('style');
      (n.textContent = Ff),
        this.shadowRoot.appendChild(n),
        this.shadowRoot.appendChild(t),
        Wa.createRoot(t).render(
          g.jsx(yc.StrictMode, { children: g.jsx(Df, {}) })
        );
    }
  }
}
customElements.get('meraki-panel') ||
  customElements.define('meraki-panel', Uf);
