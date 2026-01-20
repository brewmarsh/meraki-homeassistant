(function () {
  const t = document.createElement('link').relList;
  if (t && t.supports && t.supports('modulepreload')) return;
  for (const l of document.querySelectorAll('link[rel="modulepreload"]')) n(l);
  new MutationObserver((l) => {
    for (const a of l)
      if (a.type === 'childList')
        for (const u of a.addedNodes)
          u.tagName === 'LINK' && u.rel === 'modulepreload' && n(u);
  }).observe(document, { childList: !0, subtree: !0 });
  function r(l) {
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
  function n(l) {
    if (l.ep) return;
    l.ep = !0;
    const a = r(l);
    fetch(l.href, a);
  }
})();
(function () {
  const e = document.createElement('link').relList;
  if (e && e.supports && e.supports('modulepreload')) return;
  for (const n of document.querySelectorAll('link[rel="modulepreload"]')) r(n);
  new MutationObserver((n) => {
    for (const l of n)
      if (l.type === 'childList')
        for (const a of l.addedNodes)
          a.tagName === 'LINK' && a.rel === 'modulepreload' && r(a);
  }).observe(document, { childList: !0, subtree: !0 });
  function t(n) {
    const l = {};
    return (
      n.integrity && (l.integrity = n.integrity),
      n.referrerPolicy && (l.referrerPolicy = n.referrerPolicy),
      n.crossOrigin === 'use-credentials'
        ? (l.credentials = 'include')
        : n.crossOrigin === 'anonymous'
          ? (l.credentials = 'omit')
          : (l.credentials = 'same-origin'),
      l
    );
  }
  function r(n) {
    if (n.ep) return;
    n.ep = !0;
    const l = t(n);
    fetch(n.href, l);
  }
})();
(function () {
  const e = document.createElement('link').relList;
  if (e && e.supports && e.supports('modulepreload')) return;
  for (const n of document.querySelectorAll('link[rel="modulepreload"]')) r(n);
  new MutationObserver((n) => {
    for (const l of n)
      if (l.type === 'childList')
        for (const a of l.addedNodes)
          a.tagName === 'LINK' && a.rel === 'modulepreload' && r(a);
  }).observe(document, { childList: !0, subtree: !0 });
  function t(n) {
    const l = {};
    return (
      n.integrity && (l.integrity = n.integrity),
      n.referrerPolicy && (l.referrerPolicy = n.referrerPolicy),
      n.crossOrigin === 'use-credentials'
        ? (l.credentials = 'include')
        : n.crossOrigin === 'anonymous'
          ? (l.credentials = 'omit')
          : (l.credentials = 'same-origin'),
      l
    );
  }
  function r(n) {
    if (n.ep) return;
    n.ep = !0;
    const l = t(n);
    fetch(n.href, l);
  }
})();
function rc(e) {
  return e &&
    e.__esModule &&
    Object.prototype.hasOwnProperty.call(e, 'default')
    ? e.default
    : e;
}
var $o = { exports: {} },
  el = {},
  Bo = { exports: {} },
  L = {};
/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */ var qr = Symbol.for('react.element'),
  nc = Symbol.for('react.portal'),
  lc = Symbol.for('react.fragment'),
  ac = Symbol.for('react.strict_mode'),
  uc = Symbol.for('react.profiler'),
  oc = Symbol.for('react.provider'),
  ic = Symbol.for('react.context'),
  sc = Symbol.for('react.forward_ref'),
  cc = Symbol.for('react.suspense'),
  fc = Symbol.for('react.memo'),
  dc = Symbol.for('react.lazy'),
  Ru = Symbol.iterator;
function pc(e) {
  return e === null || typeof e != 'object'
    ? null
    : ((e = (Ru && e[Ru]) || e['@@iterator']),
      typeof e == 'function' ? e : null);
}
var Qo = {
    isMounted: function () {
      return !1;
    },
    enqueueForceUpdate: function () {},
    enqueueReplaceState: function () {},
    enqueueSetState: function () {},
  },
  Ho = Object.assign,
  Wo = {};
function lr(e, t, r) {
  (this.props = e),
    (this.context = t),
    (this.refs = Wo),
    (this.updater = r || Qo);
}
lr.prototype.isReactComponent = {};
lr.prototype.setState = function (e, t) {
  if (typeof e != 'object' && typeof e != 'function' && e != null)
    throw Error(
      'setState(...): takes an object of state variables to update or a function which returns an object of state variables.'
    );
  this.updater.enqueueSetState(this, e, t, 'setState');
};
lr.prototype.forceUpdate = function (e) {
  this.updater.enqueueForceUpdate(this, e, 'forceUpdate');
};
function qo() {}
qo.prototype = lr.prototype;
function Da(e, t, r) {
  (this.props = e),
    (this.context = t),
    (this.refs = Wo),
    (this.updater = r || Qo);
}
var ja = (Da.prototype = new qo());
ja.constructor = Da;
Ho(ja, lr.prototype);
ja.isPureReactComponent = !0;
var Ou = Array.isArray,
  Ko = Object.prototype.hasOwnProperty,
  Ua = { current: null },
  Yo = { key: !0, ref: !0, __self: !0, __source: !0 };
function Go(e, t, r) {
  var n,
    l = {},
    a = null,
    u = null;
  if (t != null)
    for (n in (t.ref !== void 0 && (u = t.ref),
    t.key !== void 0 && (a = '' + t.key),
    t))
      Ko.call(t, n) && !Yo.hasOwnProperty(n) && (l[n] = t[n]);
  var o = arguments.length - 2;
  if (o === 1) l.children = r;
  else if (1 < o) {
    for (var i = Array(o), c = 0; c < o; c++) i[c] = arguments[c + 2];
    l.children = i;
  }
  if (e && e.defaultProps)
    for (n in ((o = e.defaultProps), o)) l[n] === void 0 && (l[n] = o[n]);
  return {
    $$typeof: qr,
    type: e,
    key: a,
    ref: u,
    props: l,
    _owner: Ua.current,
  };
}
function mc(e, t) {
  return {
    $$typeof: qr,
    type: e.type,
    key: t,
    ref: e.ref,
    props: e.props,
    _owner: e._owner,
  };
}
function Aa(e) {
  return typeof e == 'object' && e !== null && e.$$typeof === qr;
}
function hc(e) {
  var t = { '=': '=0', ':': '=2' };
  return (
    '$' +
    e.replace(/[=:]/g, function (r) {
      return t[r];
    })
  );
}
var Mu = /\/+/g;
function bl(e, t) {
  return typeof e == 'object' && e !== null && e.key != null
    ? hc('' + e.key)
    : t.toString(36);
}
function yn(e, t, r, n, l) {
  var a = typeof e;
  (a === 'undefined' || a === 'boolean') && (e = null);
  var u = !1;
  if (e === null) u = !0;
  else
    switch (a) {
      case 'string':
      case 'number':
        u = !0;
        break;
      case 'object':
        switch (e.$$typeof) {
          case qr:
          case nc:
            u = !0;
        }
    }
  if (u)
    return (
      (u = e),
      (l = l(u)),
      (e = n === '' ? '.' + bl(u, 0) : n),
      Ou(l)
        ? ((r = ''),
          e != null && (r = e.replace(Mu, '$&/') + '/'),
          yn(l, t, r, '', function (c) {
            return c;
          }))
        : l != null &&
          (Aa(l) &&
            (l = mc(
              l,
              r +
                (!l.key || (u && u.key === l.key)
                  ? ''
                  : ('' + l.key).replace(Mu, '$&/') + '/') +
                e
            )),
          t.push(l)),
      1
    );
  if (((u = 0), (n = n === '' ? '.' : n + ':'), Ou(e)))
    for (var o = 0; o < e.length; o++) {
      a = e[o];
      var i = n + bl(a, o);
      u += yn(a, t, r, i, l);
    }
  else if (((i = pc(e)), typeof i == 'function'))
    for (e = i.call(e), o = 0; !(a = e.next()).done; )
      (a = a.value), (i = n + bl(a, o++)), (u += yn(a, t, r, i, l));
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
  return u;
}
function en(e, t, r) {
  if (e == null) return e;
  var n = [],
    l = 0;
  return (
    yn(e, n, '', '', function (a) {
      return t.call(r, a, l++);
    }),
    n
  );
}
function gc(e) {
  if (e._status === -1) {
    var t = e._result;
    (t = t()),
      t.then(
        function (r) {
          (e._status === 0 || e._status === -1) &&
            ((e._status = 1), (e._result = r));
        },
        function (r) {
          (e._status === 0 || e._status === -1) &&
            ((e._status = 2), (e._result = r));
        }
      ),
      e._status === -1 && ((e._status = 0), (e._result = t));
  }
  if (e._status === 1) return e._result.default;
  throw e._result;
}
var oe = { current: null },
  bn = { transition: null },
  vc = {
    ReactCurrentDispatcher: oe,
    ReactCurrentBatchConfig: bn,
    ReactCurrentOwner: Ua,
  };
function Xo() {
  throw Error('act(...) is not supported in production builds of React.');
}
L.Children = {
  map: en,
  forEach: function (e, t, r) {
    en(
      e,
      function () {
        t.apply(this, arguments);
      },
      r
    );
  },
  count: function (e) {
    var t = 0;
    return (
      en(e, function () {
        t++;
      }),
      t
    );
  },
  toArray: function (e) {
    return (
      en(e, function (t) {
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
L.Component = lr;
L.Fragment = lc;
L.Profiler = uc;
L.PureComponent = Da;
L.StrictMode = ac;
L.Suspense = cc;
L.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = vc;
L.act = Xo;
L.cloneElement = function (e, t, r) {
  if (e == null)
    throw Error(
      'React.cloneElement(...): The argument must be a React element, but you passed ' +
        e +
        '.'
    );
  var n = Ho({}, e.props),
    l = e.key,
    a = e.ref,
    u = e._owner;
  if (t != null) {
    if (
      (t.ref !== void 0 && ((a = t.ref), (u = Ua.current)),
      t.key !== void 0 && (l = '' + t.key),
      e.type && e.type.defaultProps)
    )
      var o = e.type.defaultProps;
    for (i in t)
      Ko.call(t, i) &&
        !Yo.hasOwnProperty(i) &&
        (n[i] = t[i] === void 0 && o !== void 0 ? o[i] : t[i]);
  }
  var i = arguments.length - 2;
  if (i === 1) n.children = r;
  else if (1 < i) {
    o = Array(i);
    for (var c = 0; c < i; c++) o[c] = arguments[c + 2];
    n.children = o;
  }
  return { $$typeof: qr, type: e.type, key: l, ref: a, props: n, _owner: u };
};
L.createContext = function (e) {
  return (
    (e = {
      $$typeof: ic,
      _currentValue: e,
      _currentValue2: e,
      _threadCount: 0,
      Provider: null,
      Consumer: null,
      _defaultValue: null,
      _globalName: null,
    }),
    (e.Provider = { $$typeof: oc, _context: e }),
    (e.Consumer = e)
  );
};
L.createElement = Go;
L.createFactory = function (e) {
  var t = Go.bind(null, e);
  return (t.type = e), t;
};
L.createRef = function () {
  return { current: null };
};
L.forwardRef = function (e) {
  return { $$typeof: sc, render: e };
};
L.isValidElement = Aa;
L.lazy = function (e) {
  return { $$typeof: dc, _payload: { _status: -1, _result: e }, _init: gc };
};
L.memo = function (e, t) {
  return { $$typeof: fc, type: e, compare: t === void 0 ? null : t };
};
L.startTransition = function (e) {
  var t = bn.transition;
  bn.transition = {};
  try {
    e();
  } finally {
    bn.transition = t;
  }
};
L.unstable_act = Xo;
L.useCallback = function (e, t) {
  return oe.current.useCallback(e, t);
};
L.useContext = function (e) {
  return oe.current.useContext(e);
};
L.useDebugValue = function () {};
L.useDeferredValue = function (e) {
  return oe.current.useDeferredValue(e);
};
L.useEffect = function (e, t) {
  return oe.current.useEffect(e, t);
};
L.useId = function () {
  return oe.current.useId();
};
L.useImperativeHandle = function (e, t, r) {
  return oe.current.useImperativeHandle(e, t, r);
};
L.useInsertionEffect = function (e, t) {
  return oe.current.useInsertionEffect(e, t);
};
L.useLayoutEffect = function (e, t) {
  return oe.current.useLayoutEffect(e, t);
};
L.useMemo = function (e, t) {
  return oe.current.useMemo(e, t);
};
L.useReducer = function (e, t, r) {
  return oe.current.useReducer(e, t, r);
};
L.useRef = function (e) {
  return oe.current.useRef(e);
};
L.useState = function (e) {
  return oe.current.useState(e);
};
L.useSyncExternalStore = function (e, t, r) {
  return oe.current.useSyncExternalStore(e, t, r);
};
L.useTransition = function () {
  return oe.current.useTransition();
};
L.version = '18.3.1';
Bo.exports = L;
var et = Bo.exports;
const yc = rc(et);
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */ var bc = et,
  kc = Symbol.for('react.element'),
  wc = Symbol.for('react.fragment'),
  Sc = Object.prototype.hasOwnProperty,
  xc = bc.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner,
  Ec = { key: !0, ref: !0, __self: !0, __source: !0 };
function Zo(e, t, r) {
  var n,
    l = {},
    a = null,
    u = null;
  r !== void 0 && (a = '' + r),
    t.key !== void 0 && (a = '' + t.key),
    t.ref !== void 0 && (u = t.ref);
  for (n in t) Sc.call(t, n) && !Ec.hasOwnProperty(n) && (l[n] = t[n]);
  if (e && e.defaultProps)
    for (n in ((t = e.defaultProps), t)) l[n] === void 0 && (l[n] = t[n]);
  return {
    $$typeof: kc,
    type: e,
    key: a,
    ref: u,
    props: l,
    _owner: xc.current,
  };
}
el.Fragment = wc;
el.jsx = Zo;
el.jsxs = Zo;
$o.exports = el;
var P = $o.exports,
  Hl = {},
  Jo = { exports: {} },
  ye = {},
  ei = { exports: {} },
  ti = {};
/**
 * @license React
 * scheduler.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */ (function (e) {
  function t(S, N) {
    var z = S.length;
    S.push(N);
    e: for (; 0 < z; ) {
      var Q = (z - 1) >>> 1,
        Y = S[Q];
      if (0 < l(Y, N)) (S[Q] = N), (S[z] = Y), (z = Q);
      else break e;
    }
  }
  function r(S) {
    return S.length === 0 ? null : S[0];
  }
  function n(S) {
    if (S.length === 0) return null;
    var N = S[0],
      z = S.pop();
    if (z !== N) {
      S[0] = z;
      e: for (var Q = 0, Y = S.length, Zr = Y >>> 1; Q < Zr; ) {
        var gt = 2 * (Q + 1) - 1,
          yl = S[gt],
          vt = gt + 1,
          Jr = S[vt];
        if (0 > l(yl, z))
          vt < Y && 0 > l(Jr, yl)
            ? ((S[Q] = Jr), (S[vt] = z), (Q = vt))
            : ((S[Q] = yl), (S[gt] = z), (Q = gt));
        else if (vt < Y && 0 > l(Jr, z)) (S[Q] = Jr), (S[vt] = z), (Q = vt);
        else break e;
      }
    }
    return N;
  }
  function l(S, N) {
    var z = S.sortIndex - N.sortIndex;
    return z !== 0 ? z : S.id - N.id;
  }
  if (typeof performance == 'object' && typeof performance.now == 'function') {
    var a = performance;
    e.unstable_now = function () {
      return a.now();
    };
  } else {
    var u = Date,
      o = u.now();
    e.unstable_now = function () {
      return u.now() - o;
    };
  }
  var i = [],
    c = [],
    h = 1,
    m = null,
    p = 3,
    y = !1,
    b = !1,
    k = !1,
    D = typeof setTimeout == 'function' ? setTimeout : null,
    f = typeof clearTimeout == 'function' ? clearTimeout : null,
    s = typeof setImmediate < 'u' ? setImmediate : null;
  typeof navigator < 'u' &&
    navigator.scheduling !== void 0 &&
    navigator.scheduling.isInputPending !== void 0 &&
    navigator.scheduling.isInputPending.bind(navigator.scheduling);
  function d(S) {
    for (var N = r(c); N !== null; ) {
      if (N.callback === null) n(c);
      else if (N.startTime <= S)
        n(c), (N.sortIndex = N.expirationTime), t(i, N);
      else break;
      N = r(c);
    }
  }
  function v(S) {
    if (((k = !1), d(S), !b))
      if (r(i) !== null) (b = !0), gl(x);
      else {
        var N = r(c);
        N !== null && vl(v, N.startTime - S);
      }
  }
  function x(S, N) {
    (b = !1), k && ((k = !1), f(C), (C = -1)), (y = !0);
    var z = p;
    try {
      for (
        d(N), m = r(i);
        m !== null && (!(m.expirationTime > N) || (S && !Ce()));

      ) {
        var Q = m.callback;
        if (typeof Q == 'function') {
          (m.callback = null), (p = m.priorityLevel);
          var Y = Q(m.expirationTime <= N);
          (N = e.unstable_now()),
            typeof Y == 'function' ? (m.callback = Y) : m === r(i) && n(i),
            d(N);
        } else n(i);
        m = r(i);
      }
      if (m !== null) var Zr = !0;
      else {
        var gt = r(c);
        gt !== null && vl(v, gt.startTime - N), (Zr = !1);
      }
      return Zr;
    } finally {
      (m = null), (p = z), (y = !1);
    }
  }
  var E = !1,
    _ = null,
    C = -1,
    B = 5,
    T = -1;
  function Ce() {
    return !(e.unstable_now() - T < B);
  }
  function or() {
    if (_ !== null) {
      var S = e.unstable_now();
      T = S;
      var N = !0;
      try {
        N = _(!0, S);
      } finally {
        N ? ir() : ((E = !1), (_ = null));
      }
    } else E = !1;
  }
  var ir;
  if (typeof s == 'function')
    ir = function () {
      s(or);
    };
  else if (typeof MessageChannel < 'u') {
    var Tu = new MessageChannel(),
      tc = Tu.port2;
    (Tu.port1.onmessage = or),
      (ir = function () {
        tc.postMessage(null);
      });
  } else
    ir = function () {
      D(or, 0);
    };
  function gl(S) {
    (_ = S), E || ((E = !0), ir());
  }
  function vl(S, N) {
    C = D(function () {
      S(e.unstable_now());
    }, N);
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
      b || y || ((b = !0), gl(x));
    }),
    (e.unstable_forceFrameRate = function (S) {
      0 > S || 125 < S
        ? console.error(
            'forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported'
          )
        : (B = 0 < S ? Math.floor(1e3 / S) : 5);
    }),
    (e.unstable_getCurrentPriorityLevel = function () {
      return p;
    }),
    (e.unstable_getFirstCallbackNode = function () {
      return r(i);
    }),
    (e.unstable_next = function (S) {
      switch (p) {
        case 1:
        case 2:
        case 3:
          var N = 3;
          break;
        default:
          N = p;
      }
      var z = p;
      p = N;
      try {
        return S();
      } finally {
        p = z;
      }
    }),
    (e.unstable_pauseExecution = function () {}),
    (e.unstable_requestPaint = function () {}),
    (e.unstable_runWithPriority = function (S, N) {
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
      var z = p;
      p = S;
      try {
        return N();
      } finally {
        p = z;
      }
    }),
    (e.unstable_scheduleCallback = function (S, N, z) {
      var Q = e.unstable_now();
      switch (
        (typeof z == 'object' && z !== null
          ? ((z = z.delay), (z = typeof z == 'number' && 0 < z ? Q + z : Q))
          : (z = Q),
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
        (Y = z + Y),
        (S = {
          id: h++,
          callback: N,
          priorityLevel: S,
          startTime: z,
          expirationTime: Y,
          sortIndex: -1,
        }),
        z > Q
          ? ((S.sortIndex = z),
            t(c, S),
            r(i) === null &&
              S === r(c) &&
              (k ? (f(C), (C = -1)) : (k = !0), vl(v, z - Q)))
          : ((S.sortIndex = Y), t(i, S), b || y || ((b = !0), gl(x))),
        S
      );
    }),
    (e.unstable_shouldYield = Ce),
    (e.unstable_wrapCallback = function (S) {
      var N = p;
      return function () {
        var z = p;
        p = N;
        try {
          return S.apply(this, arguments);
        } finally {
          p = z;
        }
      };
    });
})(ti);
ei.exports = ti;
var _c = ei.exports;
/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */ var Cc = et,
  ve = _c;
function g(e) {
  for (
    var t = 'https://reactjs.org/docs/error-decoder.html?invariant=' + e,
      r = 1;
    r < arguments.length;
    r++
  )
    t += '&args[]=' + encodeURIComponent(arguments[r]);
  return (
    'Minified React error #' +
    e +
    '; visit ' +
    t +
    ' for the full message or use the non-minified dev environment for full errors and additional helpful warnings.'
  );
}
var ri = new Set(),
  Lr = {};
function Lt(e, t) {
  Xt(e, t), Xt(e + 'Capture', t);
}
function Xt(e, t) {
  for (Lr[e] = t, e = 0; e < t.length; e++) ri.add(t[e]);
}
var Qe = !(
    typeof window > 'u' ||
    typeof window.document > 'u' ||
    typeof window.document.createElement > 'u'
  ),
  Wl = Object.prototype.hasOwnProperty,
  Pc =
    /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/,
  Fu = {},
  Iu = {};
function Nc(e) {
  return Wl.call(Iu, e)
    ? !0
    : Wl.call(Fu, e)
      ? !1
      : Pc.test(e)
        ? (Iu[e] = !0)
        : ((Fu[e] = !0), !1);
}
function zc(e, t, r, n) {
  if (r !== null && r.type === 0) return !1;
  switch (typeof t) {
    case 'function':
    case 'symbol':
      return !0;
    case 'boolean':
      return n
        ? !1
        : r !== null
          ? !r.acceptsBooleans
          : ((e = e.toLowerCase().slice(0, 5)),
            e !== 'data-' && e !== 'aria-');
    default:
      return !1;
  }
}
function Lc(e, t, r, n) {
  if (t === null || typeof t > 'u' || zc(e, t, r, n)) return !0;
  if (n) return !1;
  if (r !== null)
    switch (r.type) {
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
function ie(e, t, r, n, l, a, u) {
  (this.acceptsBooleans = t === 2 || t === 3 || t === 4),
    (this.attributeName = n),
    (this.attributeNamespace = l),
    (this.mustUseProperty = r),
    (this.propertyName = e),
    (this.type = t),
    (this.sanitizeURL = a),
    (this.removeEmptyString = u);
}
var ee = {};
'children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style'
  .split(' ')
  .forEach(function (e) {
    ee[e] = new ie(e, 0, !1, e, null, !1, !1);
  });
[
  ['acceptCharset', 'accept-charset'],
  ['className', 'class'],
  ['htmlFor', 'for'],
  ['httpEquiv', 'http-equiv'],
].forEach(function (e) {
  var t = e[0];
  ee[t] = new ie(t, 1, !1, e[1], null, !1, !1);
});
['contentEditable', 'draggable', 'spellCheck', 'value'].forEach(function (e) {
  ee[e] = new ie(e, 2, !1, e.toLowerCase(), null, !1, !1);
});
[
  'autoReverse',
  'externalResourcesRequired',
  'focusable',
  'preserveAlpha',
].forEach(function (e) {
  ee[e] = new ie(e, 2, !1, e, null, !1, !1);
});
'allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope'
  .split(' ')
  .forEach(function (e) {
    ee[e] = new ie(e, 3, !1, e.toLowerCase(), null, !1, !1);
  });
['checked', 'multiple', 'muted', 'selected'].forEach(function (e) {
  ee[e] = new ie(e, 3, !0, e, null, !1, !1);
});
['capture', 'download'].forEach(function (e) {
  ee[e] = new ie(e, 4, !1, e, null, !1, !1);
});
['cols', 'rows', 'size', 'span'].forEach(function (e) {
  ee[e] = new ie(e, 6, !1, e, null, !1, !1);
});
['rowSpan', 'start'].forEach(function (e) {
  ee[e] = new ie(e, 5, !1, e.toLowerCase(), null, !1, !1);
});
var Va = /[\-:]([a-z])/g;
function $a(e) {
  return e[1].toUpperCase();
}
'accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height'
  .split(' ')
  .forEach(function (e) {
    var t = e.replace(Va, $a);
    ee[t] = new ie(t, 1, !1, e, null, !1, !1);
  });
'xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type'
  .split(' ')
  .forEach(function (e) {
    var t = e.replace(Va, $a);
    ee[t] = new ie(t, 1, !1, e, 'http://www.w3.org/1999/xlink', !1, !1);
  });
['xml:base', 'xml:lang', 'xml:space'].forEach(function (e) {
  var t = e.replace(Va, $a);
  ee[t] = new ie(t, 1, !1, e, 'http://www.w3.org/XML/1998/namespace', !1, !1);
});
['tabIndex', 'crossOrigin'].forEach(function (e) {
  ee[e] = new ie(e, 1, !1, e.toLowerCase(), null, !1, !1);
});
ee.xlinkHref = new ie(
  'xlinkHref',
  1,
  !1,
  'xlink:href',
  'http://www.w3.org/1999/xlink',
  !0,
  !1
);
['src', 'href', 'action', 'formAction'].forEach(function (e) {
  ee[e] = new ie(e, 1, !1, e.toLowerCase(), null, !0, !0);
});
function Ba(e, t, r, n) {
  var l = ee.hasOwnProperty(t) ? ee[t] : null;
  (l !== null
    ? l.type !== 0
    : n ||
      !(2 < t.length) ||
      (t[0] !== 'o' && t[0] !== 'O') ||
      (t[1] !== 'n' && t[1] !== 'N')) &&
    (Lc(t, r, l, n) && (r = null),
    n || l === null
      ? Nc(t) &&
        (r === null ? e.removeAttribute(t) : e.setAttribute(t, '' + r))
      : l.mustUseProperty
        ? (e[l.propertyName] = r === null ? (l.type === 3 ? !1 : '') : r)
        : ((t = l.attributeName),
          (n = l.attributeNamespace),
          r === null
            ? e.removeAttribute(t)
            : ((l = l.type),
              (r = l === 3 || (l === 4 && r === !0) ? '' : '' + r),
              n ? e.setAttributeNS(n, t, r) : e.setAttribute(t, r))));
}
var Ke = Cc.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED,
  tn = Symbol.for('react.element'),
  Ot = Symbol.for('react.portal'),
  Mt = Symbol.for('react.fragment'),
  Qa = Symbol.for('react.strict_mode'),
  ql = Symbol.for('react.profiler'),
  ni = Symbol.for('react.provider'),
  li = Symbol.for('react.context'),
  Ha = Symbol.for('react.forward_ref'),
  Kl = Symbol.for('react.suspense'),
  Yl = Symbol.for('react.suspense_list'),
  Wa = Symbol.for('react.memo'),
  Ge = Symbol.for('react.lazy'),
  ai = Symbol.for('react.offscreen'),
  Du = Symbol.iterator;
function sr(e) {
  return e === null || typeof e != 'object'
    ? null
    : ((e = (Du && e[Du]) || e['@@iterator']),
      typeof e == 'function' ? e : null);
}
var V = Object.assign,
  kl;
function vr(e) {
  if (kl === void 0)
    try {
      throw Error();
    } catch (r) {
      var t = r.stack.trim().match(/\n( *(at )?)/);
      kl = (t && t[1]) || '';
    }
  return (
    `
` +
    kl +
    e
  );
}
var wl = !1;
function Sl(e, t) {
  if (!e || wl) return '';
  wl = !0;
  var r = Error.prepareStackTrace;
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
          var n = c;
        }
        Reflect.construct(e, [], t);
      } else {
        try {
          t.call();
        } catch (c) {
          n = c;
        }
        e.call(t.prototype);
      }
    else {
      try {
        throw Error();
      } catch (c) {
        n = c;
      }
      e();
    }
  } catch (c) {
    if (c && n && typeof c.stack == 'string') {
      for (
        var l = c.stack.split(`
`),
          a = n.stack.split(`
`),
          u = l.length - 1,
          o = a.length - 1;
        1 <= u && 0 <= o && l[u] !== a[o];

      )
        o--;
      for (; 1 <= u && 0 <= o; u--, o--)
        if (l[u] !== a[o]) {
          if (u !== 1 || o !== 1)
            do
              if ((u--, o--, 0 > o || l[u] !== a[o])) {
                var i =
                  `
` + l[u].replace(' at new ', ' at ');
                return (
                  e.displayName &&
                    i.includes('<anonymous>') &&
                    (i = i.replace('<anonymous>', e.displayName)),
                  i
                );
              }
            while (1 <= u && 0 <= o);
          break;
        }
    }
  } finally {
    (wl = !1), (Error.prepareStackTrace = r);
  }
  return (e = e ? e.displayName || e.name : '') ? vr(e) : '';
}
function Tc(e) {
  switch (e.tag) {
    case 5:
      return vr(e.type);
    case 16:
      return vr('Lazy');
    case 13:
      return vr('Suspense');
    case 19:
      return vr('SuspenseList');
    case 0:
    case 2:
    case 15:
      return (e = Sl(e.type, !1)), e;
    case 11:
      return (e = Sl(e.type.render, !1)), e;
    case 1:
      return (e = Sl(e.type, !0)), e;
    default:
      return '';
  }
}
function Gl(e) {
  if (e == null) return null;
  if (typeof e == 'function') return e.displayName || e.name || null;
  if (typeof e == 'string') return e;
  switch (e) {
    case Mt:
      return 'Fragment';
    case Ot:
      return 'Portal';
    case ql:
      return 'Profiler';
    case Qa:
      return 'StrictMode';
    case Kl:
      return 'Suspense';
    case Yl:
      return 'SuspenseList';
  }
  if (typeof e == 'object')
    switch (e.$$typeof) {
      case li:
        return (e.displayName || 'Context') + '.Consumer';
      case ni:
        return (e._context.displayName || 'Context') + '.Provider';
      case Ha:
        var t = e.render;
        return (
          (e = e.displayName),
          e ||
            ((e = t.displayName || t.name || ''),
            (e = e !== '' ? 'ForwardRef(' + e + ')' : 'ForwardRef')),
          e
        );
      case Wa:
        return (
          (t = e.displayName || null), t !== null ? t : Gl(e.type) || 'Memo'
        );
      case Ge:
        (t = e._payload), (e = e._init);
        try {
          return Gl(e(t));
        } catch {}
    }
  return null;
}
function Rc(e) {
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
      return Gl(t);
    case 8:
      return t === Qa ? 'StrictMode' : 'Mode';
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
function ui(e) {
  var t = e.type;
  return (
    (e = e.nodeName) &&
    e.toLowerCase() === 'input' &&
    (t === 'checkbox' || t === 'radio')
  );
}
function Oc(e) {
  var t = ui(e) ? 'checked' : 'value',
    r = Object.getOwnPropertyDescriptor(e.constructor.prototype, t),
    n = '' + e[t];
  if (
    !e.hasOwnProperty(t) &&
    typeof r < 'u' &&
    typeof r.get == 'function' &&
    typeof r.set == 'function'
  ) {
    var l = r.get,
      a = r.set;
    return (
      Object.defineProperty(e, t, {
        configurable: !0,
        get: function () {
          return l.call(this);
        },
        set: function (u) {
          (n = '' + u), a.call(this, u);
        },
      }),
      Object.defineProperty(e, t, { enumerable: r.enumerable }),
      {
        getValue: function () {
          return n;
        },
        setValue: function (u) {
          n = '' + u;
        },
        stopTracking: function () {
          (e._valueTracker = null), delete e[t];
        },
      }
    );
  }
}
function rn(e) {
  e._valueTracker || (e._valueTracker = Oc(e));
}
function oi(e) {
  if (!e) return !1;
  var t = e._valueTracker;
  if (!t) return !0;
  var r = t.getValue(),
    n = '';
  return (
    e && (n = ui(e) ? (e.checked ? 'true' : 'false') : e.value),
    (e = n),
    e !== r ? (t.setValue(e), !0) : !1
  );
}
function Ln(e) {
  if (((e = e || (typeof document < 'u' ? document : void 0)), typeof e > 'u'))
    return null;
  try {
    return e.activeElement || e.body;
  } catch {
    return e.body;
  }
}
function Xl(e, t) {
  var r = t.checked;
  return V({}, t, {
    defaultChecked: void 0,
    defaultValue: void 0,
    value: void 0,
    checked: r ?? e._wrapperState.initialChecked,
  });
}
function ju(e, t) {
  var r = t.defaultValue == null ? '' : t.defaultValue,
    n = t.checked != null ? t.checked : t.defaultChecked;
  (r = ft(t.value != null ? t.value : r)),
    (e._wrapperState = {
      initialChecked: n,
      initialValue: r,
      controlled:
        t.type === 'checkbox' || t.type === 'radio'
          ? t.checked != null
          : t.value != null,
    });
}
function ii(e, t) {
  (t = t.checked), t != null && Ba(e, 'checked', t, !1);
}
function Zl(e, t) {
  ii(e, t);
  var r = ft(t.value),
    n = t.type;
  if (r != null)
    n === 'number'
      ? ((r === 0 && e.value === '') || e.value != r) && (e.value = '' + r)
      : e.value !== '' + r && (e.value = '' + r);
  else if (n === 'submit' || n === 'reset') {
    e.removeAttribute('value');
    return;
  }
  t.hasOwnProperty('value')
    ? Jl(e, t.type, r)
    : t.hasOwnProperty('defaultValue') && Jl(e, t.type, ft(t.defaultValue)),
    t.checked == null &&
      t.defaultChecked != null &&
      (e.defaultChecked = !!t.defaultChecked);
}
function Uu(e, t, r) {
  if (t.hasOwnProperty('value') || t.hasOwnProperty('defaultValue')) {
    var n = t.type;
    if (
      !(
        (n !== 'submit' && n !== 'reset') ||
        (t.value !== void 0 && t.value !== null)
      )
    )
      return;
    (t = '' + e._wrapperState.initialValue),
      r || t === e.value || (e.value = t),
      (e.defaultValue = t);
  }
  (r = e.name),
    r !== '' && (e.name = ''),
    (e.defaultChecked = !!e._wrapperState.initialChecked),
    r !== '' && (e.name = r);
}
function Jl(e, t, r) {
  (t !== 'number' || Ln(e.ownerDocument) !== e) &&
    (r == null
      ? (e.defaultValue = '' + e._wrapperState.initialValue)
      : e.defaultValue !== '' + r && (e.defaultValue = '' + r));
}
var yr = Array.isArray;
function Ht(e, t, r, n) {
  if (((e = e.options), t)) {
    t = {};
    for (var l = 0; l < r.length; l++) t['$' + r[l]] = !0;
    for (r = 0; r < e.length; r++)
      (l = t.hasOwnProperty('$' + e[r].value)),
        e[r].selected !== l && (e[r].selected = l),
        l && n && (e[r].defaultSelected = !0);
  } else {
    for (r = '' + ft(r), t = null, l = 0; l < e.length; l++) {
      if (e[l].value === r) {
        (e[l].selected = !0), n && (e[l].defaultSelected = !0);
        return;
      }
      t !== null || e[l].disabled || (t = e[l]);
    }
    t !== null && (t.selected = !0);
  }
}
function ea(e, t) {
  if (t.dangerouslySetInnerHTML != null) throw Error(g(91));
  return V({}, t, {
    value: void 0,
    defaultValue: void 0,
    children: '' + e._wrapperState.initialValue,
  });
}
function Au(e, t) {
  var r = t.value;
  if (r == null) {
    if (((r = t.children), (t = t.defaultValue), r != null)) {
      if (t != null) throw Error(g(92));
      if (yr(r)) {
        if (1 < r.length) throw Error(g(93));
        r = r[0];
      }
      t = r;
    }
    t == null && (t = ''), (r = t);
  }
  e._wrapperState = { initialValue: ft(r) };
}
function si(e, t) {
  var r = ft(t.value),
    n = ft(t.defaultValue);
  r != null &&
    ((r = '' + r),
    r !== e.value && (e.value = r),
    t.defaultValue == null && e.defaultValue !== r && (e.defaultValue = r)),
    n != null && (e.defaultValue = '' + n);
}
function Vu(e) {
  var t = e.textContent;
  t === e._wrapperState.initialValue &&
    t !== '' &&
    t !== null &&
    (e.value = t);
}
function ci(e) {
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
    ? ci(t)
    : e === 'http://www.w3.org/2000/svg' && t === 'foreignObject'
      ? 'http://www.w3.org/1999/xhtml'
      : e;
}
var nn,
  fi = (function (e) {
    return typeof MSApp < 'u' && MSApp.execUnsafeLocalFunction
      ? function (t, r, n, l) {
          MSApp.execUnsafeLocalFunction(function () {
            return e(t, r, n, l);
          });
        }
      : e;
  })(function (e, t) {
    if (e.namespaceURI !== 'http://www.w3.org/2000/svg' || 'innerHTML' in e)
      e.innerHTML = t;
    else {
      for (
        nn = nn || document.createElement('div'),
          nn.innerHTML = '<svg>' + t.valueOf().toString() + '</svg>',
          t = nn.firstChild;
        e.firstChild;

      )
        e.removeChild(e.firstChild);
      for (; t.firstChild; ) e.appendChild(t.firstChild);
    }
  });
function Tr(e, t) {
  if (t) {
    var r = e.firstChild;
    if (r && r === e.lastChild && r.nodeType === 3) {
      r.nodeValue = t;
      return;
    }
  }
  e.textContent = t;
}
var wr = {
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
  Mc = ['Webkit', 'ms', 'Moz', 'O'];
Object.keys(wr).forEach(function (e) {
  Mc.forEach(function (t) {
    (t = t + e.charAt(0).toUpperCase() + e.substring(1)), (wr[t] = wr[e]);
  });
});
function di(e, t, r) {
  return t == null || typeof t == 'boolean' || t === ''
    ? ''
    : r || typeof t != 'number' || t === 0 || (wr.hasOwnProperty(e) && wr[e])
      ? ('' + t).trim()
      : t + 'px';
}
function pi(e, t) {
  e = e.style;
  for (var r in t)
    if (t.hasOwnProperty(r)) {
      var n = r.indexOf('--') === 0,
        l = di(r, t[r], n);
      r === 'float' && (r = 'cssFloat'), n ? e.setProperty(r, l) : (e[r] = l);
    }
}
var Fc = V(
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
function ra(e, t) {
  if (t) {
    if (Fc[e] && (t.children != null || t.dangerouslySetInnerHTML != null))
      throw Error(g(137, e));
    if (t.dangerouslySetInnerHTML != null) {
      if (t.children != null) throw Error(g(60));
      if (
        typeof t.dangerouslySetInnerHTML != 'object' ||
        !('__html' in t.dangerouslySetInnerHTML)
      )
        throw Error(g(61));
    }
    if (t.style != null && typeof t.style != 'object') throw Error(g(62));
  }
}
function na(e, t) {
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
function qa(e) {
  return (
    (e = e.target || e.srcElement || window),
    e.correspondingUseElement && (e = e.correspondingUseElement),
    e.nodeType === 3 ? e.parentNode : e
  );
}
var aa = null,
  Wt = null,
  qt = null;
function $u(e) {
  if ((e = Gr(e))) {
    if (typeof aa != 'function') throw Error(g(280));
    var t = e.stateNode;
    t && ((t = al(t)), aa(e.stateNode, e.type, t));
  }
}
function mi(e) {
  Wt ? (qt ? qt.push(e) : (qt = [e])) : (Wt = e);
}
function hi() {
  if (Wt) {
    var e = Wt,
      t = qt;
    if (((qt = Wt = null), $u(e), t)) for (e = 0; e < t.length; e++) $u(t[e]);
  }
}
function gi(e, t) {
  return e(t);
}
function vi() {}
var xl = !1;
function yi(e, t, r) {
  if (xl) return e(t, r);
  xl = !0;
  try {
    return gi(e, t, r);
  } finally {
    (xl = !1), (Wt !== null || qt !== null) && (vi(), hi());
  }
}
function Rr(e, t) {
  var r = e.stateNode;
  if (r === null) return null;
  var n = al(r);
  if (n === null) return null;
  r = n[t];
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
      (n = !n.disabled) ||
        ((e = e.type),
        (n = !(
          e === 'button' ||
          e === 'input' ||
          e === 'select' ||
          e === 'textarea'
        ))),
        (e = !n);
      break e;
    default:
      e = !1;
  }
  if (e) return null;
  if (r && typeof r != 'function') throw Error(g(231, t, typeof r));
  return r;
}
var ua = !1;
if (Qe)
  try {
    var cr = {};
    Object.defineProperty(cr, 'passive', {
      get: function () {
        ua = !0;
      },
    }),
      window.addEventListener('test', cr, cr),
      window.removeEventListener('test', cr, cr);
  } catch {
    ua = !1;
  }
function Ic(e, t, r, n, l, a, u, o, i) {
  var c = Array.prototype.slice.call(arguments, 3);
  try {
    t.apply(r, c);
  } catch (h) {
    this.onError(h);
  }
}
var Sr = !1,
  Tn = null,
  Rn = !1,
  oa = null,
  Dc = {
    onError: function (e) {
      (Sr = !0), (Tn = e);
    },
  };
function jc(e, t, r, n, l, a, u, o, i) {
  (Sr = !1), (Tn = null), Ic.apply(Dc, arguments);
}
function Uc(e, t, r, n, l, a, u, o, i) {
  if ((jc.apply(this, arguments), Sr)) {
    if (Sr) {
      var c = Tn;
      (Sr = !1), (Tn = null);
    } else throw Error(g(198));
    Rn || ((Rn = !0), (oa = c));
  }
}
function Tt(e) {
  var t = e,
    r = e;
  if (e.alternate) for (; t.return; ) t = t.return;
  else {
    e = t;
    do (t = e), t.flags & 4098 && (r = t.return), (e = t.return);
    while (e);
  }
  return t.tag === 3 ? r : null;
}
function bi(e) {
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
function Bu(e) {
  if (Tt(e) !== e) throw Error(g(188));
}
function Ac(e) {
  var t = e.alternate;
  if (!t) {
    if (((t = Tt(e)), t === null)) throw Error(g(188));
    return t !== e ? null : e;
  }
  for (var r = e, n = t; ; ) {
    var l = r.return;
    if (l === null) break;
    var a = l.alternate;
    if (a === null) {
      if (((n = l.return), n !== null)) {
        r = n;
        continue;
      }
      break;
    }
    if (l.child === a.child) {
      for (a = l.child; a; ) {
        if (a === r) return Bu(l), e;
        if (a === n) return Bu(l), t;
        a = a.sibling;
      }
      throw Error(g(188));
    }
    if (r.return !== n.return) (r = l), (n = a);
    else {
      for (var u = !1, o = l.child; o; ) {
        if (o === r) {
          (u = !0), (r = l), (n = a);
          break;
        }
        if (o === n) {
          (u = !0), (n = l), (r = a);
          break;
        }
        o = o.sibling;
      }
      if (!u) {
        for (o = a.child; o; ) {
          if (o === r) {
            (u = !0), (r = a), (n = l);
            break;
          }
          if (o === n) {
            (u = !0), (n = a), (r = l);
            break;
          }
          o = o.sibling;
        }
        if (!u) throw Error(g(189));
      }
    }
    if (r.alternate !== n) throw Error(g(190));
  }
  if (r.tag !== 3) throw Error(g(188));
  return r.stateNode.current === r ? e : t;
}
function ki(e) {
  return (e = Ac(e)), e !== null ? wi(e) : null;
}
function wi(e) {
  if (e.tag === 5 || e.tag === 6) return e;
  for (e = e.child; e !== null; ) {
    var t = wi(e);
    if (t !== null) return t;
    e = e.sibling;
  }
  return null;
}
var Si = ve.unstable_scheduleCallback,
  Qu = ve.unstable_cancelCallback,
  Vc = ve.unstable_shouldYield,
  $c = ve.unstable_requestPaint,
  H = ve.unstable_now,
  Bc = ve.unstable_getCurrentPriorityLevel,
  Ka = ve.unstable_ImmediatePriority,
  xi = ve.unstable_UserBlockingPriority,
  On = ve.unstable_NormalPriority,
  Qc = ve.unstable_LowPriority,
  Ei = ve.unstable_IdlePriority,
  tl = null,
  De = null;
function Hc(e) {
  if (De && typeof De.onCommitFiberRoot == 'function')
    try {
      De.onCommitFiberRoot(tl, e, void 0, (e.current.flags & 128) === 128);
    } catch {}
}
var Te = Math.clz32 ? Math.clz32 : Kc,
  Wc = Math.log,
  qc = Math.LN2;
function Kc(e) {
  return (e >>>= 0), e === 0 ? 32 : (31 - ((Wc(e) / qc) | 0)) | 0;
}
var ln = 64,
  an = 4194304;
function br(e) {
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
function Mn(e, t) {
  var r = e.pendingLanes;
  if (r === 0) return 0;
  var n = 0,
    l = e.suspendedLanes,
    a = e.pingedLanes,
    u = r & 268435455;
  if (u !== 0) {
    var o = u & ~l;
    o !== 0 ? (n = br(o)) : ((a &= u), a !== 0 && (n = br(a)));
  } else (u = r & ~l), u !== 0 ? (n = br(u)) : a !== 0 && (n = br(a));
  if (n === 0) return 0;
  if (
    t !== 0 &&
    t !== n &&
    !(t & l) &&
    ((l = n & -n), (a = t & -t), l >= a || (l === 16 && (a & 4194240) !== 0))
  )
    return t;
  if ((n & 4 && (n |= r & 16), (t = e.entangledLanes), t !== 0))
    for (e = e.entanglements, t &= n; 0 < t; )
      (r = 31 - Te(t)), (l = 1 << r), (n |= e[r]), (t &= ~l);
  return n;
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
function Gc(e, t) {
  for (
    var r = e.suspendedLanes,
      n = e.pingedLanes,
      l = e.expirationTimes,
      a = e.pendingLanes;
    0 < a;

  ) {
    var u = 31 - Te(a),
      o = 1 << u,
      i = l[u];
    i === -1
      ? (!(o & r) || o & n) && (l[u] = Yc(o, t))
      : i <= t && (e.expiredLanes |= o),
      (a &= ~o);
  }
}
function ia(e) {
  return (
    (e = e.pendingLanes & -1073741825),
    e !== 0 ? e : e & 1073741824 ? 1073741824 : 0
  );
}
function _i() {
  var e = ln;
  return (ln <<= 1), !(ln & 4194240) && (ln = 64), e;
}
function El(e) {
  for (var t = [], r = 0; 31 > r; r++) t.push(e);
  return t;
}
function Kr(e, t, r) {
  (e.pendingLanes |= t),
    t !== 536870912 && ((e.suspendedLanes = 0), (e.pingedLanes = 0)),
    (e = e.eventTimes),
    (t = 31 - Te(t)),
    (e[t] = r);
}
function Xc(e, t) {
  var r = e.pendingLanes & ~t;
  (e.pendingLanes = t),
    (e.suspendedLanes = 0),
    (e.pingedLanes = 0),
    (e.expiredLanes &= t),
    (e.mutableReadLanes &= t),
    (e.entangledLanes &= t),
    (t = e.entanglements);
  var n = e.eventTimes;
  for (e = e.expirationTimes; 0 < r; ) {
    var l = 31 - Te(r),
      a = 1 << l;
    (t[l] = 0), (n[l] = -1), (e[l] = -1), (r &= ~a);
  }
}
function Ya(e, t) {
  var r = (e.entangledLanes |= t);
  for (e = e.entanglements; r; ) {
    var n = 31 - Te(r),
      l = 1 << n;
    (l & t) | (e[n] & t) && (e[n] |= t), (r &= ~l);
  }
}
var O = 0;
function Ci(e) {
  return (e &= -e), 1 < e ? (4 < e ? (e & 268435455 ? 16 : 536870912) : 4) : 1;
}
var Pi,
  Ga,
  Ni,
  zi,
  Li,
  sa = !1,
  un = [],
  nt = null,
  lt = null,
  at = null,
  Or = new Map(),
  Mr = new Map(),
  Ze = [],
  Zc =
    'mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit'.split(
      ' '
    );
function Hu(e, t) {
  switch (e) {
    case 'focusin':
    case 'focusout':
      nt = null;
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
      Or.delete(t.pointerId);
      break;
    case 'gotpointercapture':
    case 'lostpointercapture':
      Mr.delete(t.pointerId);
  }
}
function fr(e, t, r, n, l, a) {
  return e === null || e.nativeEvent !== a
    ? ((e = {
        blockedOn: t,
        domEventName: r,
        eventSystemFlags: n,
        nativeEvent: a,
        targetContainers: [l],
      }),
      t !== null && ((t = Gr(t)), t !== null && Ga(t)),
      e)
    : ((e.eventSystemFlags |= n),
      (t = e.targetContainers),
      l !== null && t.indexOf(l) === -1 && t.push(l),
      e);
}
function Jc(e, t, r, n, l) {
  switch (t) {
    case 'focusin':
      return (nt = fr(nt, e, t, r, n, l)), !0;
    case 'dragenter':
      return (lt = fr(lt, e, t, r, n, l)), !0;
    case 'mouseover':
      return (at = fr(at, e, t, r, n, l)), !0;
    case 'pointerover':
      var a = l.pointerId;
      return Or.set(a, fr(Or.get(a) || null, e, t, r, n, l)), !0;
    case 'gotpointercapture':
      return (
        (a = l.pointerId), Mr.set(a, fr(Mr.get(a) || null, e, t, r, n, l)), !0
      );
  }
  return !1;
}
function Ti(e) {
  var t = kt(e.target);
  if (t !== null) {
    var r = Tt(t);
    if (r !== null) {
      if (((t = r.tag), t === 13)) {
        if (((t = bi(r)), t !== null)) {
          (e.blockedOn = t),
            Li(e.priority, function () {
              Ni(r);
            });
          return;
        }
      } else if (t === 3 && r.stateNode.current.memoizedState.isDehydrated) {
        e.blockedOn = r.tag === 3 ? r.stateNode.containerInfo : null;
        return;
      }
    }
  }
  e.blockedOn = null;
}
function kn(e) {
  if (e.blockedOn !== null) return !1;
  for (var t = e.targetContainers; 0 < t.length; ) {
    var r = ca(e.domEventName, e.eventSystemFlags, t[0], e.nativeEvent);
    if (r === null) {
      r = e.nativeEvent;
      var n = new r.constructor(r.type, r);
      (la = n), r.target.dispatchEvent(n), (la = null);
    } else return (t = Gr(r)), t !== null && Ga(t), (e.blockedOn = r), !1;
    t.shift();
  }
  return !0;
}
function Wu(e, t, r) {
  kn(e) && r.delete(t);
}
function ef() {
  (sa = !1),
    nt !== null && kn(nt) && (nt = null),
    lt !== null && kn(lt) && (lt = null),
    at !== null && kn(at) && (at = null),
    Or.forEach(Wu),
    Mr.forEach(Wu);
}
function dr(e, t) {
  e.blockedOn === t &&
    ((e.blockedOn = null),
    sa ||
      ((sa = !0),
      ve.unstable_scheduleCallback(ve.unstable_NormalPriority, ef)));
}
function Fr(e) {
  function t(l) {
    return dr(l, e);
  }
  if (0 < un.length) {
    dr(un[0], e);
    for (var r = 1; r < un.length; r++) {
      var n = un[r];
      n.blockedOn === e && (n.blockedOn = null);
    }
  }
  for (
    nt !== null && dr(nt, e),
      lt !== null && dr(lt, e),
      at !== null && dr(at, e),
      Or.forEach(t),
      Mr.forEach(t),
      r = 0;
    r < Ze.length;
    r++
  )
    (n = Ze[r]), n.blockedOn === e && (n.blockedOn = null);
  for (; 0 < Ze.length && ((r = Ze[0]), r.blockedOn === null); )
    Ti(r), r.blockedOn === null && Ze.shift();
}
var Kt = Ke.ReactCurrentBatchConfig,
  Fn = !0;
function tf(e, t, r, n) {
  var l = O,
    a = Kt.transition;
  Kt.transition = null;
  try {
    (O = 1), Xa(e, t, r, n);
  } finally {
    (O = l), (Kt.transition = a);
  }
}
function rf(e, t, r, n) {
  var l = O,
    a = Kt.transition;
  Kt.transition = null;
  try {
    (O = 4), Xa(e, t, r, n);
  } finally {
    (O = l), (Kt.transition = a);
  }
}
function Xa(e, t, r, n) {
  if (Fn) {
    var l = ca(e, t, r, n);
    if (l === null) Ml(e, t, n, In, r), Hu(e, n);
    else if (Jc(l, e, t, r, n)) n.stopPropagation();
    else if ((Hu(e, n), t & 4 && -1 < Zc.indexOf(e))) {
      for (; l !== null; ) {
        var a = Gr(l);
        if (
          (a !== null && Pi(a),
          (a = ca(e, t, r, n)),
          a === null && Ml(e, t, n, In, r),
          a === l)
        )
          break;
        l = a;
      }
      l !== null && n.stopPropagation();
    } else Ml(e, t, n, null, r);
  }
}
var In = null;
function ca(e, t, r, n) {
  if (((In = null), (e = qa(n)), (e = kt(e)), e !== null))
    if (((t = Tt(e)), t === null)) e = null;
    else if (((r = t.tag), r === 13)) {
      if (((e = bi(t)), e !== null)) return e;
      e = null;
    } else if (r === 3) {
      if (t.stateNode.current.memoizedState.isDehydrated)
        return t.tag === 3 ? t.stateNode.containerInfo : null;
      e = null;
    } else t !== e && (e = null);
  return (In = e), null;
}
function Ri(e) {
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
      switch (Bc()) {
        case Ka:
          return 1;
        case xi:
          return 4;
        case On:
        case Qc:
          return 16;
        case Ei:
          return 536870912;
        default:
          return 16;
      }
    default:
      return 16;
  }
}
var tt = null,
  Za = null,
  wn = null;
function Oi() {
  if (wn) return wn;
  var e,
    t = Za,
    r = t.length,
    n,
    l = 'value' in tt ? tt.value : tt.textContent,
    a = l.length;
  for (e = 0; e < r && t[e] === l[e]; e++);
  var u = r - e;
  for (n = 1; n <= u && t[r - n] === l[a - n]; n++);
  return (wn = l.slice(e, 1 < n ? 1 - n : void 0));
}
function Sn(e) {
  var t = e.keyCode;
  return (
    'charCode' in e
      ? ((e = e.charCode), e === 0 && t === 13 && (e = 13))
      : (e = t),
    e === 10 && (e = 13),
    32 <= e || e === 13 ? e : 0
  );
}
function on() {
  return !0;
}
function qu() {
  return !1;
}
function be(e) {
  function t(r, n, l, a, u) {
    (this._reactName = r),
      (this._targetInst = l),
      (this.type = n),
      (this.nativeEvent = a),
      (this.target = u),
      (this.currentTarget = null);
    for (var o in e)
      e.hasOwnProperty(o) && ((r = e[o]), (this[o] = r ? r(a) : a[o]));
    return (
      (this.isDefaultPrevented = (
        a.defaultPrevented != null ? a.defaultPrevented : a.returnValue === !1
      )
        ? on
        : qu),
      (this.isPropagationStopped = qu),
      this
    );
  }
  return (
    V(t.prototype, {
      preventDefault: function () {
        this.defaultPrevented = !0;
        var r = this.nativeEvent;
        r &&
          (r.preventDefault
            ? r.preventDefault()
            : typeof r.returnValue != 'unknown' && (r.returnValue = !1),
          (this.isDefaultPrevented = on));
      },
      stopPropagation: function () {
        var r = this.nativeEvent;
        r &&
          (r.stopPropagation
            ? r.stopPropagation()
            : typeof r.cancelBubble != 'unknown' && (r.cancelBubble = !0),
          (this.isPropagationStopped = on));
      },
      persist: function () {},
      isPersistent: on,
    }),
    t
  );
}
var ar = {
    eventPhase: 0,
    bubbles: 0,
    cancelable: 0,
    timeStamp: function (e) {
      return e.timeStamp || Date.now();
    },
    defaultPrevented: 0,
    isTrusted: 0,
  },
  Ja = be(ar),
  Yr = V({}, ar, { view: 0, detail: 0 }),
  nf = be(Yr),
  _l,
  Cl,
  pr,
  rl = V({}, Yr, {
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
    getModifierState: eu,
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
        : (e !== pr &&
            (pr && e.type === 'mousemove'
              ? ((_l = e.screenX - pr.screenX), (Cl = e.screenY - pr.screenY))
              : (Cl = _l = 0),
            (pr = e)),
          _l);
    },
    movementY: function (e) {
      return 'movementY' in e ? e.movementY : Cl;
    },
  }),
  Ku = be(rl),
  lf = V({}, rl, { dataTransfer: 0 }),
  af = be(lf),
  uf = V({}, Yr, { relatedTarget: 0 }),
  Pl = be(uf),
  of = V({}, ar, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }),
  sf = be(of),
  cf = V({}, ar, {
    clipboardData: function (e) {
      return 'clipboardData' in e ? e.clipboardData : window.clipboardData;
    },
  }),
  ff = be(cf),
  df = V({}, ar, { data: 0 }),
  Yu = be(df),
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
function eu() {
  return gf;
}
var vf = V({}, Yr, {
    key: function (e) {
      if (e.key) {
        var t = pf[e.key] || e.key;
        if (t !== 'Unidentified') return t;
      }
      return e.type === 'keypress'
        ? ((e = Sn(e)), e === 13 ? 'Enter' : String.fromCharCode(e))
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
    getModifierState: eu,
    charCode: function (e) {
      return e.type === 'keypress' ? Sn(e) : 0;
    },
    keyCode: function (e) {
      return e.type === 'keydown' || e.type === 'keyup' ? e.keyCode : 0;
    },
    which: function (e) {
      return e.type === 'keypress'
        ? Sn(e)
        : e.type === 'keydown' || e.type === 'keyup'
          ? e.keyCode
          : 0;
    },
  }),
  yf = be(vf),
  bf = V({}, rl, {
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
  Gu = be(bf),
  kf = V({}, Yr, {
    touches: 0,
    targetTouches: 0,
    changedTouches: 0,
    altKey: 0,
    metaKey: 0,
    ctrlKey: 0,
    shiftKey: 0,
    getModifierState: eu,
  }),
  wf = be(kf),
  Sf = V({}, ar, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }),
  xf = be(Sf),
  Ef = V({}, rl, {
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
  _f = be(Ef),
  Cf = [9, 13, 27, 32],
  tu = Qe && 'CompositionEvent' in window,
  xr = null;
Qe && 'documentMode' in document && (xr = document.documentMode);
var Pf = Qe && 'TextEvent' in window && !xr,
  Mi = Qe && (!tu || (xr && 8 < xr && 11 >= xr)),
  Xu = ' ',
  Zu = !1;
function Fi(e, t) {
  switch (e) {
    case 'keyup':
      return Cf.indexOf(t.keyCode) !== -1;
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
function Ii(e) {
  return (e = e.detail), typeof e == 'object' && 'data' in e ? e.data : null;
}
var Ft = !1;
function Nf(e, t) {
  switch (e) {
    case 'compositionend':
      return Ii(t);
    case 'keypress':
      return t.which !== 32 ? null : ((Zu = !0), Xu);
    case 'textInput':
      return (e = t.data), e === Xu && Zu ? null : e;
    default:
      return null;
  }
}
function zf(e, t) {
  if (Ft)
    return e === 'compositionend' || (!tu && Fi(e, t))
      ? ((e = Oi()), (wn = Za = tt = null), (Ft = !1), e)
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
      return Mi && t.locale !== 'ko' ? null : t.data;
    default:
      return null;
  }
}
var Lf = {
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
function Ju(e) {
  var t = e && e.nodeName && e.nodeName.toLowerCase();
  return t === 'input' ? !!Lf[e.type] : t === 'textarea';
}
function Di(e, t, r, n) {
  mi(n),
    (t = Dn(t, 'onChange')),
    0 < t.length &&
      ((r = new Ja('onChange', 'change', null, r, n)),
      e.push({ event: r, listeners: t }));
}
var Er = null,
  Ir = null;
function Tf(e) {
  Ki(e, 0);
}
function nl(e) {
  var t = jt(e);
  if (oi(t)) return e;
}
function Rf(e, t) {
  if (e === 'change') return t;
}
var ji = !1;
if (Qe) {
  var Nl;
  if (Qe) {
    var zl = 'oninput' in document;
    if (!zl) {
      var eo = document.createElement('div');
      eo.setAttribute('oninput', 'return;'),
        (zl = typeof eo.oninput == 'function');
    }
    Nl = zl;
  } else Nl = !1;
  ji = Nl && (!document.documentMode || 9 < document.documentMode);
}
function to() {
  Er && (Er.detachEvent('onpropertychange', Ui), (Ir = Er = null));
}
function Ui(e) {
  if (e.propertyName === 'value' && nl(Ir)) {
    var t = [];
    Di(t, Ir, e, qa(e)), yi(Tf, t);
  }
}
function Of(e, t, r) {
  e === 'focusin'
    ? (to(), (Er = t), (Ir = r), Er.attachEvent('onpropertychange', Ui))
    : e === 'focusout' && to();
}
function Mf(e) {
  if (e === 'selectionchange' || e === 'keyup' || e === 'keydown')
    return nl(Ir);
}
function Ff(e, t) {
  if (e === 'click') return nl(t);
}
function If(e, t) {
  if (e === 'input' || e === 'change') return nl(t);
}
function Df(e, t) {
  return (e === t && (e !== 0 || 1 / e === 1 / t)) || (e !== e && t !== t);
}
var Oe = typeof Object.is == 'function' ? Object.is : Df;
function Dr(e, t) {
  if (Oe(e, t)) return !0;
  if (typeof e != 'object' || e === null || typeof t != 'object' || t === null)
    return !1;
  var r = Object.keys(e),
    n = Object.keys(t);
  if (r.length !== n.length) return !1;
  for (n = 0; n < r.length; n++) {
    var l = r[n];
    if (!Wl.call(t, l) || !Oe(e[l], t[l])) return !1;
  }
  return !0;
}
function ro(e) {
  for (; e && e.firstChild; ) e = e.firstChild;
  return e;
}
function no(e, t) {
  var r = ro(e);
  e = 0;
  for (var n; r; ) {
    if (r.nodeType === 3) {
      if (((n = e + r.textContent.length), e <= t && n >= t))
        return { node: r, offset: t - e };
      e = n;
    }
    e: {
      for (; r; ) {
        if (r.nextSibling) {
          r = r.nextSibling;
          break e;
        }
        r = r.parentNode;
      }
      r = void 0;
    }
    r = ro(r);
  }
}
function Ai(e, t) {
  return e && t
    ? e === t
      ? !0
      : e && e.nodeType === 3
        ? !1
        : t && t.nodeType === 3
          ? Ai(e, t.parentNode)
          : 'contains' in e
            ? e.contains(t)
            : e.compareDocumentPosition
              ? !!(e.compareDocumentPosition(t) & 16)
              : !1
    : !1;
}
function Vi() {
  for (var e = window, t = Ln(); t instanceof e.HTMLIFrameElement; ) {
    try {
      var r = typeof t.contentWindow.location.href == 'string';
    } catch {
      r = !1;
    }
    if (r) e = t.contentWindow;
    else break;
    t = Ln(e.document);
  }
  return t;
}
function ru(e) {
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
function jf(e) {
  var t = Vi(),
    r = e.focusedElem,
    n = e.selectionRange;
  if (
    t !== r &&
    r &&
    r.ownerDocument &&
    Ai(r.ownerDocument.documentElement, r)
  ) {
    if (n !== null && ru(r)) {
      if (
        ((t = n.start),
        (e = n.end),
        e === void 0 && (e = t),
        'selectionStart' in r)
      )
        (r.selectionStart = t), (r.selectionEnd = Math.min(e, r.value.length));
      else if (
        ((e = ((t = r.ownerDocument || document) && t.defaultView) || window),
        e.getSelection)
      ) {
        e = e.getSelection();
        var l = r.textContent.length,
          a = Math.min(n.start, l);
        (n = n.end === void 0 ? a : Math.min(n.end, l)),
          !e.extend && a > n && ((l = n), (n = a), (a = l)),
          (l = no(r, a));
        var u = no(r, n);
        l &&
          u &&
          (e.rangeCount !== 1 ||
            e.anchorNode !== l.node ||
            e.anchorOffset !== l.offset ||
            e.focusNode !== u.node ||
            e.focusOffset !== u.offset) &&
          ((t = t.createRange()),
          t.setStart(l.node, l.offset),
          e.removeAllRanges(),
          a > n
            ? (e.addRange(t), e.extend(u.node, u.offset))
            : (t.setEnd(u.node, u.offset), e.addRange(t)));
      }
    }
    for (t = [], e = r; (e = e.parentNode); )
      e.nodeType === 1 &&
        t.push({ element: e, left: e.scrollLeft, top: e.scrollTop });
    for (typeof r.focus == 'function' && r.focus(), r = 0; r < t.length; r++)
      (e = t[r]),
        (e.element.scrollLeft = e.left),
        (e.element.scrollTop = e.top);
  }
}
var Uf = Qe && 'documentMode' in document && 11 >= document.documentMode,
  It = null,
  fa = null,
  _r = null,
  da = !1;
function lo(e, t, r) {
  var n = r.window === r ? r.document : r.nodeType === 9 ? r : r.ownerDocument;
  da ||
    It == null ||
    It !== Ln(n) ||
    ((n = It),
    'selectionStart' in n && ru(n)
      ? (n = { start: n.selectionStart, end: n.selectionEnd })
      : ((n = (
          (n.ownerDocument && n.ownerDocument.defaultView) ||
          window
        ).getSelection()),
        (n = {
          anchorNode: n.anchorNode,
          anchorOffset: n.anchorOffset,
          focusNode: n.focusNode,
          focusOffset: n.focusOffset,
        })),
    (_r && Dr(_r, n)) ||
      ((_r = n),
      (n = Dn(fa, 'onSelect')),
      0 < n.length &&
        ((t = new Ja('onSelect', 'select', null, t, r)),
        e.push({ event: t, listeners: n }),
        (t.target = It))));
}
function sn(e, t) {
  var r = {};
  return (
    (r[e.toLowerCase()] = t.toLowerCase()),
    (r['Webkit' + e] = 'webkit' + t),
    (r['Moz' + e] = 'moz' + t),
    r
  );
}
var Dt = {
    animationend: sn('Animation', 'AnimationEnd'),
    animationiteration: sn('Animation', 'AnimationIteration'),
    animationstart: sn('Animation', 'AnimationStart'),
    transitionend: sn('Transition', 'TransitionEnd'),
  },
  Ll = {},
  $i = {};
Qe &&
  (($i = document.createElement('div').style),
  'AnimationEvent' in window ||
    (delete Dt.animationend.animation,
    delete Dt.animationiteration.animation,
    delete Dt.animationstart.animation),
  'TransitionEvent' in window || delete Dt.transitionend.transition);
function ll(e) {
  if (Ll[e]) return Ll[e];
  if (!Dt[e]) return e;
  var t = Dt[e],
    r;
  for (r in t) if (t.hasOwnProperty(r) && r in $i) return (Ll[e] = t[r]);
  return e;
}
var Bi = ll('animationend'),
  Qi = ll('animationiteration'),
  Hi = ll('animationstart'),
  Wi = ll('transitionend'),
  qi = new Map(),
  ao =
    'abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel'.split(
      ' '
    );
function pt(e, t) {
  qi.set(e, t), Lt(t, [e]);
}
for (var Tl = 0; Tl < ao.length; Tl++) {
  var Rl = ao[Tl],
    Af = Rl.toLowerCase(),
    Vf = Rl[0].toUpperCase() + Rl.slice(1);
  pt(Af, 'on' + Vf);
}
pt(Bi, 'onAnimationEnd');
pt(Qi, 'onAnimationIteration');
pt(Hi, 'onAnimationStart');
pt('dblclick', 'onDoubleClick');
pt('focusin', 'onFocus');
pt('focusout', 'onBlur');
pt(Wi, 'onTransitionEnd');
Xt('onMouseEnter', ['mouseout', 'mouseover']);
Xt('onMouseLeave', ['mouseout', 'mouseover']);
Xt('onPointerEnter', ['pointerout', 'pointerover']);
Xt('onPointerLeave', ['pointerout', 'pointerover']);
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
var kr =
    'abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting'.split(
      ' '
    ),
  $f = new Set(
    'cancel close invalid load scroll toggle'.split(' ').concat(kr)
  );
function uo(e, t, r) {
  var n = e.type || 'unknown-event';
  (e.currentTarget = r), Uc(n, t, void 0, e), (e.currentTarget = null);
}
function Ki(e, t) {
  t = (t & 4) !== 0;
  for (var r = 0; r < e.length; r++) {
    var n = e[r],
      l = n.event;
    n = n.listeners;
    e: {
      var a = void 0;
      if (t)
        for (var u = n.length - 1; 0 <= u; u--) {
          var o = n[u],
            i = o.instance,
            c = o.currentTarget;
          if (((o = o.listener), i !== a && l.isPropagationStopped())) break e;
          uo(l, o, c), (a = i);
        }
      else
        for (u = 0; u < n.length; u++) {
          if (
            ((o = n[u]),
            (i = o.instance),
            (c = o.currentTarget),
            (o = o.listener),
            i !== a && l.isPropagationStopped())
          )
            break e;
          uo(l, o, c), (a = i);
        }
    }
  }
  if (Rn) throw ((e = oa), (Rn = !1), (oa = null), e);
}
function F(e, t) {
  var r = t[va];
  r === void 0 && (r = t[va] = new Set());
  var n = e + '__bubble';
  r.has(n) || (Yi(t, e, 2, !1), r.add(n));
}
function Ol(e, t, r) {
  var n = 0;
  t && (n |= 4), Yi(r, e, n, t);
}
var cn = '_reactListening' + Math.random().toString(36).slice(2);
function jr(e) {
  if (!e[cn]) {
    (e[cn] = !0),
      ri.forEach(function (r) {
        r !== 'selectionchange' && ($f.has(r) || Ol(r, !1, e), Ol(r, !0, e));
      });
    var t = e.nodeType === 9 ? e : e.ownerDocument;
    t === null || t[cn] || ((t[cn] = !0), Ol('selectionchange', !1, t));
  }
}
function Yi(e, t, r, n) {
  switch (Ri(t)) {
    case 1:
      var l = tf;
      break;
    case 4:
      l = rf;
      break;
    default:
      l = Xa;
  }
  (r = l.bind(null, t, r, e)),
    (l = void 0),
    !ua ||
      (t !== 'touchstart' && t !== 'touchmove' && t !== 'wheel') ||
      (l = !0),
    n
      ? l !== void 0
        ? e.addEventListener(t, r, { capture: !0, passive: l })
        : e.addEventListener(t, r, !0)
      : l !== void 0
        ? e.addEventListener(t, r, { passive: l })
        : e.addEventListener(t, r, !1);
}
function Ml(e, t, r, n, l) {
  var a = n;
  if (!(t & 1) && !(t & 2) && n !== null)
    e: for (;;) {
      if (n === null) return;
      var u = n.tag;
      if (u === 3 || u === 4) {
        var o = n.stateNode.containerInfo;
        if (o === l || (o.nodeType === 8 && o.parentNode === l)) break;
        if (u === 4)
          for (u = n.return; u !== null; ) {
            var i = u.tag;
            if (
              (i === 3 || i === 4) &&
              ((i = u.stateNode.containerInfo),
              i === l || (i.nodeType === 8 && i.parentNode === l))
            )
              return;
            u = u.return;
          }
        for (; o !== null; ) {
          if (((u = kt(o)), u === null)) return;
          if (((i = u.tag), i === 5 || i === 6)) {
            n = a = u;
            continue e;
          }
          o = o.parentNode;
        }
      }
      n = n.return;
    }
  yi(function () {
    var c = a,
      h = qa(r),
      m = [];
    e: {
      var p = qi.get(e);
      if (p !== void 0) {
        var y = Ja,
          b = e;
        switch (e) {
          case 'keypress':
            if (Sn(r) === 0) break e;
          case 'keydown':
          case 'keyup':
            y = yf;
            break;
          case 'focusin':
            (b = 'focus'), (y = Pl);
            break;
          case 'focusout':
            (b = 'blur'), (y = Pl);
            break;
          case 'beforeblur':
          case 'afterblur':
            y = Pl;
            break;
          case 'click':
            if (r.button === 2) break e;
          case 'auxclick':
          case 'dblclick':
          case 'mousedown':
          case 'mousemove':
          case 'mouseup':
          case 'mouseout':
          case 'mouseover':
          case 'contextmenu':
            y = Ku;
            break;
          case 'drag':
          case 'dragend':
          case 'dragenter':
          case 'dragexit':
          case 'dragleave':
          case 'dragover':
          case 'dragstart':
          case 'drop':
            y = af;
            break;
          case 'touchcancel':
          case 'touchend':
          case 'touchmove':
          case 'touchstart':
            y = wf;
            break;
          case Bi:
          case Qi:
          case Hi:
            y = sf;
            break;
          case Wi:
            y = xf;
            break;
          case 'scroll':
            y = nf;
            break;
          case 'wheel':
            y = _f;
            break;
          case 'copy':
          case 'cut':
          case 'paste':
            y = ff;
            break;
          case 'gotpointercapture':
          case 'lostpointercapture':
          case 'pointercancel':
          case 'pointerdown':
          case 'pointermove':
          case 'pointerout':
          case 'pointerover':
          case 'pointerup':
            y = Gu;
        }
        var k = (t & 4) !== 0,
          D = !k && e === 'scroll',
          f = k ? (p !== null ? p + 'Capture' : null) : p;
        k = [];
        for (var s = c, d; s !== null; ) {
          d = s;
          var v = d.stateNode;
          if (
            (d.tag === 5 &&
              v !== null &&
              ((d = v),
              f !== null &&
                ((v = Rr(s, f)), v != null && k.push(Ur(s, v, d)))),
            D)
          )
            break;
          s = s.return;
        }
        0 < k.length &&
          ((p = new y(p, b, null, r, h)), m.push({ event: p, listeners: k }));
      }
    }
    if (!(t & 7)) {
      e: {
        if (
          ((p = e === 'mouseover' || e === 'pointerover'),
          (y = e === 'mouseout' || e === 'pointerout'),
          p &&
            r !== la &&
            (b = r.relatedTarget || r.fromElement) &&
            (kt(b) || b[He]))
        )
          break e;
        if (
          (y || p) &&
          ((p =
            h.window === h
              ? h
              : (p = h.ownerDocument)
                ? p.defaultView || p.parentWindow
                : window),
          y
            ? ((b = r.relatedTarget || r.toElement),
              (y = c),
              (b = b ? kt(b) : null),
              b !== null &&
                ((D = Tt(b)), b !== D || (b.tag !== 5 && b.tag !== 6)) &&
                (b = null))
            : ((y = null), (b = c)),
          y !== b)
        ) {
          if (
            ((k = Ku),
            (v = 'onMouseLeave'),
            (f = 'onMouseEnter'),
            (s = 'mouse'),
            (e === 'pointerout' || e === 'pointerover') &&
              ((k = Gu),
              (v = 'onPointerLeave'),
              (f = 'onPointerEnter'),
              (s = 'pointer')),
            (D = y == null ? p : jt(y)),
            (d = b == null ? p : jt(b)),
            (p = new k(v, s + 'leave', y, r, h)),
            (p.target = D),
            (p.relatedTarget = d),
            (v = null),
            kt(h) === c &&
              ((k = new k(f, s + 'enter', b, r, h)),
              (k.target = d),
              (k.relatedTarget = D),
              (v = k)),
            (D = v),
            y && b)
          )
            t: {
              for (k = y, f = b, s = 0, d = k; d; d = Rt(d)) s++;
              for (d = 0, v = f; v; v = Rt(v)) d++;
              for (; 0 < s - d; ) (k = Rt(k)), s--;
              for (; 0 < d - s; ) (f = Rt(f)), d--;
              for (; s--; ) {
                if (k === f || (f !== null && k === f.alternate)) break t;
                (k = Rt(k)), (f = Rt(f));
              }
              k = null;
            }
          else k = null;
          y !== null && oo(m, p, y, k, !1),
            b !== null && D !== null && oo(m, D, b, k, !0);
        }
      }
      e: {
        if (
          ((p = c ? jt(c) : window),
          (y = p.nodeName && p.nodeName.toLowerCase()),
          y === 'select' || (y === 'input' && p.type === 'file'))
        )
          var x = Rf;
        else if (Ju(p))
          if (ji) x = If;
          else {
            x = Mf;
            var E = Of;
          }
        else
          (y = p.nodeName) &&
            y.toLowerCase() === 'input' &&
            (p.type === 'checkbox' || p.type === 'radio') &&
            (x = Ff);
        if (x && (x = x(e, c))) {
          Di(m, x, r, h);
          break e;
        }
        E && E(e, p, c),
          e === 'focusout' &&
            (E = p._wrapperState) &&
            E.controlled &&
            p.type === 'number' &&
            Jl(p, 'number', p.value);
      }
      switch (((E = c ? jt(c) : window), e)) {
        case 'focusin':
          (Ju(E) || E.contentEditable === 'true') &&
            ((It = E), (fa = c), (_r = null));
          break;
        case 'focusout':
          _r = fa = It = null;
          break;
        case 'mousedown':
          da = !0;
          break;
        case 'contextmenu':
        case 'mouseup':
        case 'dragend':
          (da = !1), lo(m, r, h);
          break;
        case 'selectionchange':
          if (Uf) break;
        case 'keydown':
        case 'keyup':
          lo(m, r, h);
      }
      var _;
      if (tu)
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
        Ft
          ? Fi(e, r) && (C = 'onCompositionEnd')
          : e === 'keydown' && r.keyCode === 229 && (C = 'onCompositionStart');
      C &&
        (Mi &&
          r.locale !== 'ko' &&
          (Ft || C !== 'onCompositionStart'
            ? C === 'onCompositionEnd' && Ft && (_ = Oi())
            : ((tt = h),
              (Za = 'value' in tt ? tt.value : tt.textContent),
              (Ft = !0))),
        (E = Dn(c, C)),
        0 < E.length &&
          ((C = new Yu(C, e, null, r, h)),
          m.push({ event: C, listeners: E }),
          _ ? (C.data = _) : ((_ = Ii(r)), _ !== null && (C.data = _)))),
        (_ = Pf ? Nf(e, r) : zf(e, r)) &&
          ((c = Dn(c, 'onBeforeInput')),
          0 < c.length &&
            ((h = new Yu('onBeforeInput', 'beforeinput', null, r, h)),
            m.push({ event: h, listeners: c }),
            (h.data = _)));
    }
    Ki(m, t);
  });
}
function Ur(e, t, r) {
  return { instance: e, listener: t, currentTarget: r };
}
function Dn(e, t) {
  for (var r = t + 'Capture', n = []; e !== null; ) {
    var l = e,
      a = l.stateNode;
    l.tag === 5 &&
      a !== null &&
      ((l = a),
      (a = Rr(e, r)),
      a != null && n.unshift(Ur(e, a, l)),
      (a = Rr(e, t)),
      a != null && n.push(Ur(e, a, l))),
      (e = e.return);
  }
  return n;
}
function Rt(e) {
  if (e === null) return null;
  do e = e.return;
  while (e && e.tag !== 5);
  return e || null;
}
function oo(e, t, r, n, l) {
  for (var a = t._reactName, u = []; r !== null && r !== n; ) {
    var o = r,
      i = o.alternate,
      c = o.stateNode;
    if (i !== null && i === n) break;
    o.tag === 5 &&
      c !== null &&
      ((o = c),
      l
        ? ((i = Rr(r, a)), i != null && u.unshift(Ur(r, i, o)))
        : l || ((i = Rr(r, a)), i != null && u.push(Ur(r, i, o)))),
      (r = r.return);
  }
  u.length !== 0 && e.push({ event: t, listeners: u });
}
var Bf = /\r\n?/g,
  Qf = /\u0000|\uFFFD/g;
function io(e) {
  return (typeof e == 'string' ? e : '' + e)
    .replace(
      Bf,
      `
`
    )
    .replace(Qf, '');
}
function fn(e, t, r) {
  if (((t = io(t)), io(e) !== t && r)) throw Error(g(425));
}
function jn() {}
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
  Hf = typeof clearTimeout == 'function' ? clearTimeout : void 0,
  so = typeof Promise == 'function' ? Promise : void 0,
  Wf =
    typeof queueMicrotask == 'function'
      ? queueMicrotask
      : typeof so < 'u'
        ? function (e) {
            return so.resolve(null).then(e).catch(qf);
          }
        : ga;
function qf(e) {
  setTimeout(function () {
    throw e;
  });
}
function Fl(e, t) {
  var r = t,
    n = 0;
  do {
    var l = r.nextSibling;
    if ((e.removeChild(r), l && l.nodeType === 8))
      if (((r = l.data), r === '/$')) {
        if (n === 0) {
          e.removeChild(l), Fr(t);
          return;
        }
        n--;
      } else (r !== '$' && r !== '$?' && r !== '$!') || n++;
    r = l;
  } while (r);
  Fr(t);
}
function ut(e) {
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
function co(e) {
  e = e.previousSibling;
  for (var t = 0; e; ) {
    if (e.nodeType === 8) {
      var r = e.data;
      if (r === '$' || r === '$!' || r === '$?') {
        if (t === 0) return e;
        t--;
      } else r === '/$' && t++;
    }
    e = e.previousSibling;
  }
  return null;
}
var ur = Math.random().toString(36).slice(2),
  Ie = '__reactFiber$' + ur,
  Ar = '__reactProps$' + ur,
  He = '__reactContainer$' + ur,
  va = '__reactEvents$' + ur,
  Kf = '__reactListeners$' + ur,
  Yf = '__reactHandles$' + ur;
function kt(e) {
  var t = e[Ie];
  if (t) return t;
  for (var r = e.parentNode; r; ) {
    if ((t = r[He] || r[Ie])) {
      if (
        ((r = t.alternate),
        t.child !== null || (r !== null && r.child !== null))
      )
        for (e = co(e); e !== null; ) {
          if ((r = e[Ie])) return r;
          e = co(e);
        }
      return t;
    }
    (e = r), (r = e.parentNode);
  }
  return null;
}
function Gr(e) {
  return (
    (e = e[Ie] || e[He]),
    !e || (e.tag !== 5 && e.tag !== 6 && e.tag !== 13 && e.tag !== 3)
      ? null
      : e
  );
}
function jt(e) {
  if (e.tag === 5 || e.tag === 6) return e.stateNode;
  throw Error(g(33));
}
function al(e) {
  return e[Ar] || null;
}
var ya = [],
  Ut = -1;
function mt(e) {
  return { current: e };
}
function I(e) {
  0 > Ut || ((e.current = ya[Ut]), (ya[Ut] = null), Ut--);
}
function M(e, t) {
  Ut++, (ya[Ut] = e.current), (e.current = t);
}
var dt = {},
  le = mt(dt),
  fe = mt(!1),
  _t = dt;
function Zt(e, t) {
  var r = e.type.contextTypes;
  if (!r) return dt;
  var n = e.stateNode;
  if (n && n.__reactInternalMemoizedUnmaskedChildContext === t)
    return n.__reactInternalMemoizedMaskedChildContext;
  var l = {},
    a;
  for (a in r) l[a] = t[a];
  return (
    n &&
      ((e = e.stateNode),
      (e.__reactInternalMemoizedUnmaskedChildContext = t),
      (e.__reactInternalMemoizedMaskedChildContext = l)),
    l
  );
}
function de(e) {
  return (e = e.childContextTypes), e != null;
}
function Un() {
  I(fe), I(le);
}
function fo(e, t, r) {
  if (le.current !== dt) throw Error(g(168));
  M(le, t), M(fe, r);
}
function Gi(e, t, r) {
  var n = e.stateNode;
  if (((t = t.childContextTypes), typeof n.getChildContext != 'function'))
    return r;
  n = n.getChildContext();
  for (var l in n) if (!(l in t)) throw Error(g(108, Rc(e) || 'Unknown', l));
  return V({}, r, n);
}
function An(e) {
  return (
    (e =
      ((e = e.stateNode) && e.__reactInternalMemoizedMergedChildContext) ||
      dt),
    (_t = le.current),
    M(le, e),
    M(fe, fe.current),
    !0
  );
}
function po(e, t, r) {
  var n = e.stateNode;
  if (!n) throw Error(g(169));
  r
    ? ((e = Gi(e, t, _t)),
      (n.__reactInternalMemoizedMergedChildContext = e),
      I(fe),
      I(le),
      M(le, e))
    : I(fe),
    M(fe, r);
}
var Ae = null,
  ul = !1,
  Il = !1;
function Xi(e) {
  Ae === null ? (Ae = [e]) : Ae.push(e);
}
function Gf(e) {
  (ul = !0), Xi(e);
}
function ht() {
  if (!Il && Ae !== null) {
    Il = !0;
    var e = 0,
      t = O;
    try {
      var r = Ae;
      for (O = 1; e < r.length; e++) {
        var n = r[e];
        do n = n(!0);
        while (n !== null);
      }
      (Ae = null), (ul = !1);
    } catch (l) {
      throw (Ae !== null && (Ae = Ae.slice(e + 1)), Si(Ka, ht), l);
    } finally {
      (O = t), (Il = !1);
    }
  }
  return null;
}
var At = [],
  Vt = 0,
  Vn = null,
  $n = 0,
  ke = [],
  we = 0,
  Ct = null,
  Ve = 1,
  $e = '';
function yt(e, t) {
  (At[Vt++] = $n), (At[Vt++] = Vn), (Vn = e), ($n = t);
}
function Zi(e, t, r) {
  (ke[we++] = Ve), (ke[we++] = $e), (ke[we++] = Ct), (Ct = e);
  var n = Ve;
  e = $e;
  var l = 32 - Te(n) - 1;
  (n &= ~(1 << l)), (r += 1);
  var a = 32 - Te(t) + l;
  if (30 < a) {
    var u = l - (l % 5);
    (a = (n & ((1 << u) - 1)).toString(32)),
      (n >>= u),
      (l -= u),
      (Ve = (1 << (32 - Te(t) + l)) | (r << l) | n),
      ($e = a + e);
  } else (Ve = (1 << a) | (r << l) | n), ($e = e);
}
function nu(e) {
  e.return !== null && (yt(e, 1), Zi(e, 1, 0));
}
function lu(e) {
  for (; e === Vn; )
    (Vn = At[--Vt]), (At[Vt] = null), ($n = At[--Vt]), (At[Vt] = null);
  for (; e === Ct; )
    (Ct = ke[--we]),
      (ke[we] = null),
      ($e = ke[--we]),
      (ke[we] = null),
      (Ve = ke[--we]),
      (ke[we] = null);
}
var ge = null,
  he = null,
  j = !1,
  Le = null;
function Ji(e, t) {
  var r = Se(5, null, null, 0);
  (r.elementType = 'DELETED'),
    (r.stateNode = t),
    (r.return = e),
    (t = e.deletions),
    t === null ? ((e.deletions = [r]), (e.flags |= 16)) : t.push(r);
}
function mo(e, t) {
  switch (e.tag) {
    case 5:
      var r = e.type;
      return (
        (t =
          t.nodeType !== 1 || r.toLowerCase() !== t.nodeName.toLowerCase()
            ? null
            : t),
        t !== null
          ? ((e.stateNode = t), (ge = e), (he = ut(t.firstChild)), !0)
          : !1
      );
    case 6:
      return (
        (t = e.pendingProps === '' || t.nodeType !== 3 ? null : t),
        t !== null ? ((e.stateNode = t), (ge = e), (he = null), !0) : !1
      );
    case 13:
      return (
        (t = t.nodeType !== 8 ? null : t),
        t !== null
          ? ((r = Ct !== null ? { id: Ve, overflow: $e } : null),
            (e.memoizedState = {
              dehydrated: t,
              treeContext: r,
              retryLane: 1073741824,
            }),
            (r = Se(18, null, null, 0)),
            (r.stateNode = t),
            (r.return = e),
            (e.child = r),
            (ge = e),
            (he = null),
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
function ka(e) {
  if (j) {
    var t = he;
    if (t) {
      var r = t;
      if (!mo(e, t)) {
        if (ba(e)) throw Error(g(418));
        t = ut(r.nextSibling);
        var n = ge;
        t && mo(e, t)
          ? Ji(n, r)
          : ((e.flags = (e.flags & -4097) | 2), (j = !1), (ge = e));
      }
    } else {
      if (ba(e)) throw Error(g(418));
      (e.flags = (e.flags & -4097) | 2), (j = !1), (ge = e);
    }
  }
}
function ho(e) {
  for (
    e = e.return;
    e !== null && e.tag !== 5 && e.tag !== 3 && e.tag !== 13;

  )
    e = e.return;
  ge = e;
}
function dn(e) {
  if (e !== ge) return !1;
  if (!j) return ho(e), (j = !0), !1;
  var t;
  if (
    ((t = e.tag !== 3) &&
      !(t = e.tag !== 5) &&
      ((t = e.type),
      (t = t !== 'head' && t !== 'body' && !ha(e.type, e.memoizedProps))),
    t && (t = he))
  ) {
    if (ba(e)) throw (es(), Error(g(418)));
    for (; t; ) Ji(e, t), (t = ut(t.nextSibling));
  }
  if ((ho(e), e.tag === 13)) {
    if (((e = e.memoizedState), (e = e !== null ? e.dehydrated : null), !e))
      throw Error(g(317));
    e: {
      for (e = e.nextSibling, t = 0; e; ) {
        if (e.nodeType === 8) {
          var r = e.data;
          if (r === '/$') {
            if (t === 0) {
              he = ut(e.nextSibling);
              break e;
            }
            t--;
          } else (r !== '$' && r !== '$!' && r !== '$?') || t++;
        }
        e = e.nextSibling;
      }
      he = null;
    }
  } else he = ge ? ut(e.stateNode.nextSibling) : null;
  return !0;
}
function es() {
  for (var e = he; e; ) e = ut(e.nextSibling);
}
function Jt() {
  (he = ge = null), (j = !1);
}
function au(e) {
  Le === null ? (Le = [e]) : Le.push(e);
}
var Xf = Ke.ReactCurrentBatchConfig;
function mr(e, t, r) {
  if (
    ((e = r.ref), e !== null && typeof e != 'function' && typeof e != 'object')
  ) {
    if (r._owner) {
      if (((r = r._owner), r)) {
        if (r.tag !== 1) throw Error(g(309));
        var n = r.stateNode;
      }
      if (!n) throw Error(g(147, e));
      var l = n,
        a = '' + e;
      return t !== null &&
        t.ref !== null &&
        typeof t.ref == 'function' &&
        t.ref._stringRef === a
        ? t.ref
        : ((t = function (u) {
            var o = l.refs;
            u === null ? delete o[a] : (o[a] = u);
          }),
          (t._stringRef = a),
          t);
    }
    if (typeof e != 'string') throw Error(g(284));
    if (!r._owner) throw Error(g(290, e));
  }
  return e;
}
function pn(e, t) {
  throw (
    ((e = Object.prototype.toString.call(t)),
    Error(
      g(
        31,
        e === '[object Object]'
          ? 'object with keys {' + Object.keys(t).join(', ') + '}'
          : e
      )
    ))
  );
}
function go(e) {
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
  function r(f, s) {
    if (!e) return null;
    for (; s !== null; ) t(f, s), (s = s.sibling);
    return null;
  }
  function n(f, s) {
    for (f = new Map(); s !== null; )
      s.key !== null ? f.set(s.key, s) : f.set(s.index, s), (s = s.sibling);
    return f;
  }
  function l(f, s) {
    return (f = ct(f, s)), (f.index = 0), (f.sibling = null), f;
  }
  function a(f, s, d) {
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
  function u(f) {
    return e && f.alternate === null && (f.flags |= 2), f;
  }
  function o(f, s, d, v) {
    return s === null || s.tag !== 6
      ? ((s = Bl(d, f.mode, v)), (s.return = f), s)
      : ((s = l(s, d)), (s.return = f), s);
  }
  function i(f, s, d, v) {
    var x = d.type;
    return x === Mt
      ? h(f, s, d.props.children, v, d.key)
      : s !== null &&
          (s.elementType === x ||
            (typeof x == 'object' &&
              x !== null &&
              x.$$typeof === Ge &&
              go(x) === s.type))
        ? ((v = l(s, d.props)), (v.ref = mr(f, s, d)), (v.return = f), v)
        : ((v = zn(d.type, d.key, d.props, null, f.mode, v)),
          (v.ref = mr(f, s, d)),
          (v.return = f),
          v);
  }
  function c(f, s, d, v) {
    return s === null ||
      s.tag !== 4 ||
      s.stateNode.containerInfo !== d.containerInfo ||
      s.stateNode.implementation !== d.implementation
      ? ((s = Ql(d, f.mode, v)), (s.return = f), s)
      : ((s = l(s, d.children || [])), (s.return = f), s);
  }
  function h(f, s, d, v, x) {
    return s === null || s.tag !== 7
      ? ((s = Et(d, f.mode, v, x)), (s.return = f), s)
      : ((s = l(s, d)), (s.return = f), s);
  }
  function m(f, s, d) {
    if ((typeof s == 'string' && s !== '') || typeof s == 'number')
      return (s = Bl('' + s, f.mode, d)), (s.return = f), s;
    if (typeof s == 'object' && s !== null) {
      switch (s.$$typeof) {
        case tn:
          return (
            (d = zn(s.type, s.key, s.props, null, f.mode, d)),
            (d.ref = mr(f, null, s)),
            (d.return = f),
            d
          );
        case Ot:
          return (s = Ql(s, f.mode, d)), (s.return = f), s;
        case Ge:
          var v = s._init;
          return m(f, v(s._payload), d);
      }
      if (yr(s) || sr(s))
        return (s = Et(s, f.mode, d, null)), (s.return = f), s;
      pn(f, s);
    }
    return null;
  }
  function p(f, s, d, v) {
    var x = s !== null ? s.key : null;
    if ((typeof d == 'string' && d !== '') || typeof d == 'number')
      return x !== null ? null : o(f, s, '' + d, v);
    if (typeof d == 'object' && d !== null) {
      switch (d.$$typeof) {
        case tn:
          return d.key === x ? i(f, s, d, v) : null;
        case Ot:
          return d.key === x ? c(f, s, d, v) : null;
        case Ge:
          return (x = d._init), p(f, s, x(d._payload), v);
      }
      if (yr(d) || sr(d)) return x !== null ? null : h(f, s, d, v, null);
      pn(f, d);
    }
    return null;
  }
  function y(f, s, d, v, x) {
    if ((typeof v == 'string' && v !== '') || typeof v == 'number')
      return (f = f.get(d) || null), o(s, f, '' + v, x);
    if (typeof v == 'object' && v !== null) {
      switch (v.$$typeof) {
        case tn:
          return (
            (f = f.get(v.key === null ? d : v.key) || null), i(s, f, v, x)
          );
        case Ot:
          return (
            (f = f.get(v.key === null ? d : v.key) || null), c(s, f, v, x)
          );
        case Ge:
          var E = v._init;
          return y(f, s, d, E(v._payload), x);
      }
      if (yr(v) || sr(v)) return (f = f.get(d) || null), h(s, f, v, x, null);
      pn(s, v);
    }
    return null;
  }
  function b(f, s, d, v) {
    for (
      var x = null, E = null, _ = s, C = (s = 0), B = null;
      _ !== null && C < d.length;
      C++
    ) {
      _.index > C ? ((B = _), (_ = null)) : (B = _.sibling);
      var T = p(f, _, d[C], v);
      if (T === null) {
        _ === null && (_ = B);
        break;
      }
      e && _ && T.alternate === null && t(f, _),
        (s = a(T, s, C)),
        E === null ? (x = T) : (E.sibling = T),
        (E = T),
        (_ = B);
    }
    if (C === d.length) return r(f, _), j && yt(f, C), x;
    if (_ === null) {
      for (; C < d.length; C++)
        (_ = m(f, d[C], v)),
          _ !== null &&
            ((s = a(_, s, C)),
            E === null ? (x = _) : (E.sibling = _),
            (E = _));
      return j && yt(f, C), x;
    }
    for (_ = n(f, _); C < d.length; C++)
      (B = y(_, f, C, d[C], v)),
        B !== null &&
          (e && B.alternate !== null && _.delete(B.key === null ? C : B.key),
          (s = a(B, s, C)),
          E === null ? (x = B) : (E.sibling = B),
          (E = B));
    return (
      e &&
        _.forEach(function (Ce) {
          return t(f, Ce);
        }),
      j && yt(f, C),
      x
    );
  }
  function k(f, s, d, v) {
    var x = sr(d);
    if (typeof x != 'function') throw Error(g(150));
    if (((d = x.call(d)), d == null)) throw Error(g(151));
    for (
      var E = (x = null), _ = s, C = (s = 0), B = null, T = d.next();
      _ !== null && !T.done;
      C++, T = d.next()
    ) {
      _.index > C ? ((B = _), (_ = null)) : (B = _.sibling);
      var Ce = p(f, _, T.value, v);
      if (Ce === null) {
        _ === null && (_ = B);
        break;
      }
      e && _ && Ce.alternate === null && t(f, _),
        (s = a(Ce, s, C)),
        E === null ? (x = Ce) : (E.sibling = Ce),
        (E = Ce),
        (_ = B);
    }
    if (T.done) return r(f, _), j && yt(f, C), x;
    if (_ === null) {
      for (; !T.done; C++, T = d.next())
        (T = m(f, T.value, v)),
          T !== null &&
            ((s = a(T, s, C)),
            E === null ? (x = T) : (E.sibling = T),
            (E = T));
      return j && yt(f, C), x;
    }
    for (_ = n(f, _); !T.done; C++, T = d.next())
      (T = y(_, f, C, T.value, v)),
        T !== null &&
          (e && T.alternate !== null && _.delete(T.key === null ? C : T.key),
          (s = a(T, s, C)),
          E === null ? (x = T) : (E.sibling = T),
          (E = T));
    return (
      e &&
        _.forEach(function (or) {
          return t(f, or);
        }),
      j && yt(f, C),
      x
    );
  }
  function D(f, s, d, v) {
    if (
      (typeof d == 'object' &&
        d !== null &&
        d.type === Mt &&
        d.key === null &&
        (d = d.props.children),
      typeof d == 'object' && d !== null)
    ) {
      switch (d.$$typeof) {
        case tn:
          e: {
            for (var x = d.key, E = s; E !== null; ) {
              if (E.key === x) {
                if (((x = d.type), x === Mt)) {
                  if (E.tag === 7) {
                    r(f, E.sibling),
                      (s = l(E, d.props.children)),
                      (s.return = f),
                      (f = s);
                    break e;
                  }
                } else if (
                  E.elementType === x ||
                  (typeof x == 'object' &&
                    x !== null &&
                    x.$$typeof === Ge &&
                    go(x) === E.type)
                ) {
                  r(f, E.sibling),
                    (s = l(E, d.props)),
                    (s.ref = mr(f, E, d)),
                    (s.return = f),
                    (f = s);
                  break e;
                }
                r(f, E);
                break;
              } else t(f, E);
              E = E.sibling;
            }
            d.type === Mt
              ? ((s = Et(d.props.children, f.mode, v, d.key)),
                (s.return = f),
                (f = s))
              : ((v = zn(d.type, d.key, d.props, null, f.mode, v)),
                (v.ref = mr(f, s, d)),
                (v.return = f),
                (f = v));
          }
          return u(f);
        case Ot:
          e: {
            for (E = d.key; s !== null; ) {
              if (s.key === E)
                if (
                  s.tag === 4 &&
                  s.stateNode.containerInfo === d.containerInfo &&
                  s.stateNode.implementation === d.implementation
                ) {
                  r(f, s.sibling),
                    (s = l(s, d.children || [])),
                    (s.return = f),
                    (f = s);
                  break e;
                } else {
                  r(f, s);
                  break;
                }
              else t(f, s);
              s = s.sibling;
            }
            (s = Ql(d, f.mode, v)), (s.return = f), (f = s);
          }
          return u(f);
        case Ge:
          return (E = d._init), D(f, s, E(d._payload), v);
      }
      if (yr(d)) return b(f, s, d, v);
      if (sr(d)) return k(f, s, d, v);
      pn(f, d);
    }
    return (typeof d == 'string' && d !== '') || typeof d == 'number'
      ? ((d = '' + d),
        s !== null && s.tag === 6
          ? (r(f, s.sibling), (s = l(s, d)), (s.return = f), (f = s))
          : (r(f, s), (s = Bl(d, f.mode, v)), (s.return = f), (f = s)),
        u(f))
      : r(f, s);
  }
  return D;
}
var er = ts(!0),
  rs = ts(!1),
  Bn = mt(null),
  Qn = null,
  $t = null,
  uu = null;
function ou() {
  uu = $t = Qn = null;
}
function iu(e) {
  var t = Bn.current;
  I(Bn), (e._currentValue = t);
}
function wa(e, t, r) {
  for (; e !== null; ) {
    var n = e.alternate;
    if (
      ((e.childLanes & t) !== t
        ? ((e.childLanes |= t), n !== null && (n.childLanes |= t))
        : n !== null && (n.childLanes & t) !== t && (n.childLanes |= t),
      e === r)
    )
      break;
    e = e.return;
  }
}
function Yt(e, t) {
  (Qn = e),
    (uu = $t = null),
    (e = e.dependencies),
    e !== null &&
      e.firstContext !== null &&
      (e.lanes & t && (ce = !0), (e.firstContext = null));
}
function Ee(e) {
  var t = e._currentValue;
  if (uu !== e)
    if (((e = { context: e, memoizedValue: t, next: null }), $t === null)) {
      if (Qn === null) throw Error(g(308));
      ($t = e), (Qn.dependencies = { lanes: 0, firstContext: e });
    } else $t = $t.next = e;
  return t;
}
var wt = null;
function su(e) {
  wt === null ? (wt = [e]) : wt.push(e);
}
function ns(e, t, r, n) {
  var l = t.interleaved;
  return (
    l === null ? ((r.next = r), su(t)) : ((r.next = l.next), (l.next = r)),
    (t.interleaved = r),
    We(e, n)
  );
}
function We(e, t) {
  e.lanes |= t;
  var r = e.alternate;
  for (r !== null && (r.lanes |= t), r = e, e = e.return; e !== null; )
    (e.childLanes |= t),
      (r = e.alternate),
      r !== null && (r.childLanes |= t),
      (r = e),
      (e = e.return);
  return r.tag === 3 ? r.stateNode : null;
}
var Xe = !1;
function cu(e) {
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
function ot(e, t, r) {
  var n = e.updateQueue;
  if (n === null) return null;
  if (((n = n.shared), R & 2)) {
    var l = n.pending;
    return (
      l === null ? (t.next = t) : ((t.next = l.next), (l.next = t)),
      (n.pending = t),
      We(e, r)
    );
  }
  return (
    (l = n.interleaved),
    l === null ? ((t.next = t), su(n)) : ((t.next = l.next), (l.next = t)),
    (n.interleaved = t),
    We(e, r)
  );
}
function xn(e, t, r) {
  if (
    ((t = t.updateQueue), t !== null && ((t = t.shared), (r & 4194240) !== 0))
  ) {
    var n = t.lanes;
    (n &= e.pendingLanes), (r |= n), (t.lanes = r), Ya(e, r);
  }
}
function vo(e, t) {
  var r = e.updateQueue,
    n = e.alternate;
  if (n !== null && ((n = n.updateQueue), r === n)) {
    var l = null,
      a = null;
    if (((r = r.firstBaseUpdate), r !== null)) {
      do {
        var u = {
          eventTime: r.eventTime,
          lane: r.lane,
          tag: r.tag,
          payload: r.payload,
          callback: r.callback,
          next: null,
        };
        a === null ? (l = a = u) : (a = a.next = u), (r = r.next);
      } while (r !== null);
      a === null ? (l = a = t) : (a = a.next = t);
    } else l = a = t;
    (r = {
      baseState: n.baseState,
      firstBaseUpdate: l,
      lastBaseUpdate: a,
      shared: n.shared,
      effects: n.effects,
    }),
      (e.updateQueue = r);
    return;
  }
  (e = r.lastBaseUpdate),
    e === null ? (r.firstBaseUpdate = t) : (e.next = t),
    (r.lastBaseUpdate = t);
}
function Hn(e, t, r, n) {
  var l = e.updateQueue;
  Xe = !1;
  var a = l.firstBaseUpdate,
    u = l.lastBaseUpdate,
    o = l.shared.pending;
  if (o !== null) {
    l.shared.pending = null;
    var i = o,
      c = i.next;
    (i.next = null), u === null ? (a = c) : (u.next = c), (u = i);
    var h = e.alternate;
    h !== null &&
      ((h = h.updateQueue),
      (o = h.lastBaseUpdate),
      o !== u &&
        (o === null ? (h.firstBaseUpdate = c) : (o.next = c),
        (h.lastBaseUpdate = i)));
  }
  if (a !== null) {
    var m = l.baseState;
    (u = 0), (h = c = i = null), (o = a);
    do {
      var p = o.lane,
        y = o.eventTime;
      if ((n & p) === p) {
        h !== null &&
          (h = h.next =
            {
              eventTime: y,
              lane: 0,
              tag: o.tag,
              payload: o.payload,
              callback: o.callback,
              next: null,
            });
        e: {
          var b = e,
            k = o;
          switch (((p = t), (y = r), k.tag)) {
            case 1:
              if (((b = k.payload), typeof b == 'function')) {
                m = b.call(y, m, p);
                break e;
              }
              m = b;
              break e;
            case 3:
              b.flags = (b.flags & -65537) | 128;
            case 0:
              if (
                ((b = k.payload),
                (p = typeof b == 'function' ? b.call(y, m, p) : b),
                p == null)
              )
                break e;
              m = V({}, m, p);
              break e;
            case 2:
              Xe = !0;
          }
        }
        o.callback !== null &&
          o.lane !== 0 &&
          ((e.flags |= 64),
          (p = l.effects),
          p === null ? (l.effects = [o]) : p.push(o));
      } else
        (y = {
          eventTime: y,
          lane: p,
          tag: o.tag,
          payload: o.payload,
          callback: o.callback,
          next: null,
        }),
          h === null ? ((c = h = y), (i = m)) : (h = h.next = y),
          (u |= p);
      if (((o = o.next), o === null)) {
        if (((o = l.shared.pending), o === null)) break;
        (p = o),
          (o = p.next),
          (p.next = null),
          (l.lastBaseUpdate = p),
          (l.shared.pending = null);
      }
    } while (!0);
    if (
      (h === null && (i = m),
      (l.baseState = i),
      (l.firstBaseUpdate = c),
      (l.lastBaseUpdate = h),
      (t = l.shared.interleaved),
      t !== null)
    ) {
      l = t;
      do (u |= l.lane), (l = l.next);
      while (l !== t);
    } else a === null && (l.shared.lanes = 0);
    (Nt |= u), (e.lanes = u), (e.memoizedState = m);
  }
}
function yo(e, t, r) {
  if (((e = t.effects), (t.effects = null), e !== null))
    for (t = 0; t < e.length; t++) {
      var n = e[t],
        l = n.callback;
      if (l !== null) {
        if (((n.callback = null), (n = r), typeof l != 'function'))
          throw Error(g(191, l));
        l.call(n);
      }
    }
}
var Xr = {},
  je = mt(Xr),
  Vr = mt(Xr),
  $r = mt(Xr);
function St(e) {
  if (e === Xr) throw Error(g(174));
  return e;
}
function fu(e, t) {
  switch ((M($r, t), M(Vr, e), M(je, Xr), (e = t.nodeType), e)) {
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
  I(je), M(je, t);
}
function tr() {
  I(je), I(Vr), I($r);
}
function as(e) {
  St($r.current);
  var t = St(je.current),
    r = ta(t, e.type);
  t !== r && (M(Vr, e), M(je, r));
}
function du(e) {
  Vr.current === e && (I(je), I(Vr));
}
var U = mt(0);
function Wn(e) {
  for (var t = e; t !== null; ) {
    if (t.tag === 13) {
      var r = t.memoizedState;
      if (
        r !== null &&
        ((r = r.dehydrated), r === null || r.data === '$?' || r.data === '$!')
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
var Dl = [];
function pu() {
  for (var e = 0; e < Dl.length; e++)
    Dl[e]._workInProgressVersionPrimary = null;
  Dl.length = 0;
}
var En = Ke.ReactCurrentDispatcher,
  jl = Ke.ReactCurrentBatchConfig,
  Pt = 0,
  A = null,
  q = null,
  G = null,
  qn = !1,
  Cr = !1,
  Br = 0,
  Zf = 0;
function te() {
  throw Error(g(321));
}
function mu(e, t) {
  if (t === null) return !1;
  for (var r = 0; r < t.length && r < e.length; r++)
    if (!Oe(e[r], t[r])) return !1;
  return !0;
}
function hu(e, t, r, n, l, a) {
  if (
    ((Pt = a),
    (A = t),
    (t.memoizedState = null),
    (t.updateQueue = null),
    (t.lanes = 0),
    (En.current = e === null || e.memoizedState === null ? rd : nd),
    (e = r(n, l)),
    Cr)
  ) {
    a = 0;
    do {
      if (((Cr = !1), (Br = 0), 25 <= a)) throw Error(g(301));
      (a += 1),
        (G = q = null),
        (t.updateQueue = null),
        (En.current = ld),
        (e = r(n, l));
    } while (Cr);
  }
  if (
    ((En.current = Kn),
    (t = q !== null && q.next !== null),
    (Pt = 0),
    (G = q = A = null),
    (qn = !1),
    t)
  )
    throw Error(g(300));
  return e;
}
function gu() {
  var e = Br !== 0;
  return (Br = 0), e;
}
function Fe() {
  var e = {
    memoizedState: null,
    baseState: null,
    baseQueue: null,
    queue: null,
    next: null,
  };
  return G === null ? (A.memoizedState = G = e) : (G = G.next = e), G;
}
function _e() {
  if (q === null) {
    var e = A.alternate;
    e = e !== null ? e.memoizedState : null;
  } else e = q.next;
  var t = G === null ? A.memoizedState : G.next;
  if (t !== null) (G = t), (q = e);
  else {
    if (e === null) throw Error(g(310));
    (q = e),
      (e = {
        memoizedState: q.memoizedState,
        baseState: q.baseState,
        baseQueue: q.baseQueue,
        queue: q.queue,
        next: null,
      }),
      G === null ? (A.memoizedState = G = e) : (G = G.next = e);
  }
  return G;
}
function Qr(e, t) {
  return typeof t == 'function' ? t(e) : t;
}
function Ul(e) {
  var t = _e(),
    r = t.queue;
  if (r === null) throw Error(g(311));
  r.lastRenderedReducer = e;
  var n = q,
    l = n.baseQueue,
    a = r.pending;
  if (a !== null) {
    if (l !== null) {
      var u = l.next;
      (l.next = a.next), (a.next = u);
    }
    (n.baseQueue = l = a), (r.pending = null);
  }
  if (l !== null) {
    (a = l.next), (n = n.baseState);
    var o = (u = null),
      i = null,
      c = a;
    do {
      var h = c.lane;
      if ((Pt & h) === h)
        i !== null &&
          (i = i.next =
            {
              lane: 0,
              action: c.action,
              hasEagerState: c.hasEagerState,
              eagerState: c.eagerState,
              next: null,
            }),
          (n = c.hasEagerState ? c.eagerState : e(n, c.action));
      else {
        var m = {
          lane: h,
          action: c.action,
          hasEagerState: c.hasEagerState,
          eagerState: c.eagerState,
          next: null,
        };
        i === null ? ((o = i = m), (u = n)) : (i = i.next = m),
          (A.lanes |= h),
          (Nt |= h);
      }
      c = c.next;
    } while (c !== null && c !== a);
    i === null ? (u = n) : (i.next = o),
      Oe(n, t.memoizedState) || (ce = !0),
      (t.memoizedState = n),
      (t.baseState = u),
      (t.baseQueue = i),
      (r.lastRenderedState = n);
  }
  if (((e = r.interleaved), e !== null)) {
    l = e;
    do (a = l.lane), (A.lanes |= a), (Nt |= a), (l = l.next);
    while (l !== e);
  } else l === null && (r.lanes = 0);
  return [t.memoizedState, r.dispatch];
}
function Al(e) {
  var t = _e(),
    r = t.queue;
  if (r === null) throw Error(g(311));
  r.lastRenderedReducer = e;
  var n = r.dispatch,
    l = r.pending,
    a = t.memoizedState;
  if (l !== null) {
    r.pending = null;
    var u = (l = l.next);
    do (a = e(a, u.action)), (u = u.next);
    while (u !== l);
    Oe(a, t.memoizedState) || (ce = !0),
      (t.memoizedState = a),
      t.baseQueue === null && (t.baseState = a),
      (r.lastRenderedState = a);
  }
  return [a, n];
}
function us() {}
function os(e, t) {
  var r = A,
    n = _e(),
    l = t(),
    a = !Oe(n.memoizedState, l);
  if (
    (a && ((n.memoizedState = l), (ce = !0)),
    (n = n.queue),
    vu(cs.bind(null, r, n, e), [e]),
    n.getSnapshot !== t || a || (G !== null && G.memoizedState.tag & 1))
  ) {
    if (
      ((r.flags |= 2048),
      Hr(9, ss.bind(null, r, n, l, t), void 0, null),
      X === null)
    )
      throw Error(g(349));
    Pt & 30 || is(r, t, l);
  }
  return l;
}
function is(e, t, r) {
  (e.flags |= 16384),
    (e = { getSnapshot: t, value: r }),
    (t = A.updateQueue),
    t === null
      ? ((t = { lastEffect: null, stores: null }),
        (A.updateQueue = t),
        (t.stores = [e]))
      : ((r = t.stores), r === null ? (t.stores = [e]) : r.push(e));
}
function ss(e, t, r, n) {
  (t.value = r), (t.getSnapshot = n), fs(t) && ds(e);
}
function cs(e, t, r) {
  return r(function () {
    fs(t) && ds(e);
  });
}
function fs(e) {
  var t = e.getSnapshot;
  e = e.value;
  try {
    var r = t();
    return !Oe(e, r);
  } catch {
    return !0;
  }
}
function ds(e) {
  var t = We(e, 1);
  t !== null && Re(t, e, 1, -1);
}
function bo(e) {
  var t = Fe();
  return (
    typeof e == 'function' && (e = e()),
    (t.memoizedState = t.baseState = e),
    (e = {
      pending: null,
      interleaved: null,
      lanes: 0,
      dispatch: null,
      lastRenderedReducer: Qr,
      lastRenderedState: e,
    }),
    (t.queue = e),
    (e = e.dispatch = td.bind(null, A, e)),
    [t.memoizedState, e]
  );
}
function Hr(e, t, r, n) {
  return (
    (e = { tag: e, create: t, destroy: r, deps: n, next: null }),
    (t = A.updateQueue),
    t === null
      ? ((t = { lastEffect: null, stores: null }),
        (A.updateQueue = t),
        (t.lastEffect = e.next = e))
      : ((r = t.lastEffect),
        r === null
          ? (t.lastEffect = e.next = e)
          : ((n = r.next), (r.next = e), (e.next = n), (t.lastEffect = e))),
    e
  );
}
function ps() {
  return _e().memoizedState;
}
function _n(e, t, r, n) {
  var l = Fe();
  (A.flags |= e),
    (l.memoizedState = Hr(1 | t, r, void 0, n === void 0 ? null : n));
}
function ol(e, t, r, n) {
  var l = _e();
  n = n === void 0 ? null : n;
  var a = void 0;
  if (q !== null) {
    var u = q.memoizedState;
    if (((a = u.destroy), n !== null && mu(n, u.deps))) {
      l.memoizedState = Hr(t, r, a, n);
      return;
    }
  }
  (A.flags |= e), (l.memoizedState = Hr(1 | t, r, a, n));
}
function ko(e, t) {
  return _n(8390656, 8, e, t);
}
function vu(e, t) {
  return ol(2048, 8, e, t);
}
function ms(e, t) {
  return ol(4, 2, e, t);
}
function hs(e, t) {
  return ol(4, 4, e, t);
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
function vs(e, t, r) {
  return (
    (r = r != null ? r.concat([e]) : null), ol(4, 4, gs.bind(null, t, e), r)
  );
}
function yu() {}
function ys(e, t) {
  var r = _e();
  t = t === void 0 ? null : t;
  var n = r.memoizedState;
  return n !== null && t !== null && mu(t, n[1])
    ? n[0]
    : ((r.memoizedState = [e, t]), e);
}
function bs(e, t) {
  var r = _e();
  t = t === void 0 ? null : t;
  var n = r.memoizedState;
  return n !== null && t !== null && mu(t, n[1])
    ? n[0]
    : ((e = e()), (r.memoizedState = [e, t]), e);
}
function ks(e, t, r) {
  return Pt & 21
    ? (Oe(r, t) || ((r = _i()), (A.lanes |= r), (Nt |= r), (e.baseState = !0)),
      t)
    : (e.baseState && ((e.baseState = !1), (ce = !0)), (e.memoizedState = r));
}
function Jf(e, t) {
  var r = O;
  (O = r !== 0 && 4 > r ? r : 4), e(!0);
  var n = jl.transition;
  jl.transition = {};
  try {
    e(!1), t();
  } finally {
    (O = r), (jl.transition = n);
  }
}
function ws() {
  return _e().memoizedState;
}
function ed(e, t, r) {
  var n = st(e);
  if (
    ((r = {
      lane: n,
      action: r,
      hasEagerState: !1,
      eagerState: null,
      next: null,
    }),
    Ss(e))
  )
    xs(t, r);
  else if (((r = ns(e, t, r, n)), r !== null)) {
    var l = ue();
    Re(r, e, n, l), Es(r, t, n);
  }
}
function td(e, t, r) {
  var n = st(e),
    l = {
      lane: n,
      action: r,
      hasEagerState: !1,
      eagerState: null,
      next: null,
    };
  if (Ss(e)) xs(t, l);
  else {
    var a = e.alternate;
    if (
      e.lanes === 0 &&
      (a === null || a.lanes === 0) &&
      ((a = t.lastRenderedReducer), a !== null)
    )
      try {
        var u = t.lastRenderedState,
          o = a(u, r);
        if (((l.hasEagerState = !0), (l.eagerState = o), Oe(o, u))) {
          var i = t.interleaved;
          i === null
            ? ((l.next = l), su(t))
            : ((l.next = i.next), (i.next = l)),
            (t.interleaved = l);
          return;
        }
      } catch {
      } finally {
      }
    (r = ns(e, t, l, n)),
      r !== null && ((l = ue()), Re(r, e, n, l), Es(r, t, n));
  }
}
function Ss(e) {
  var t = e.alternate;
  return e === A || (t !== null && t === A);
}
function xs(e, t) {
  Cr = qn = !0;
  var r = e.pending;
  r === null ? (t.next = t) : ((t.next = r.next), (r.next = t)),
    (e.pending = t);
}
function Es(e, t, r) {
  if (r & 4194240) {
    var n = t.lanes;
    (n &= e.pendingLanes), (r |= n), (t.lanes = r), Ya(e, r);
  }
}
var Kn = {
    readContext: Ee,
    useCallback: te,
    useContext: te,
    useEffect: te,
    useImperativeHandle: te,
    useInsertionEffect: te,
    useLayoutEffect: te,
    useMemo: te,
    useReducer: te,
    useRef: te,
    useState: te,
    useDebugValue: te,
    useDeferredValue: te,
    useTransition: te,
    useMutableSource: te,
    useSyncExternalStore: te,
    useId: te,
    unstable_isNewReconciler: !1,
  },
  rd = {
    readContext: Ee,
    useCallback: function (e, t) {
      return (Fe().memoizedState = [e, t === void 0 ? null : t]), e;
    },
    useContext: Ee,
    useEffect: ko,
    useImperativeHandle: function (e, t, r) {
      return (
        (r = r != null ? r.concat([e]) : null),
        _n(4194308, 4, gs.bind(null, t, e), r)
      );
    },
    useLayoutEffect: function (e, t) {
      return _n(4194308, 4, e, t);
    },
    useInsertionEffect: function (e, t) {
      return _n(4, 2, e, t);
    },
    useMemo: function (e, t) {
      var r = Fe();
      return (
        (t = t === void 0 ? null : t), (e = e()), (r.memoizedState = [e, t]), e
      );
    },
    useReducer: function (e, t, r) {
      var n = Fe();
      return (
        (t = r !== void 0 ? r(t) : t),
        (n.memoizedState = n.baseState = t),
        (e = {
          pending: null,
          interleaved: null,
          lanes: 0,
          dispatch: null,
          lastRenderedReducer: e,
          lastRenderedState: t,
        }),
        (n.queue = e),
        (e = e.dispatch = ed.bind(null, A, e)),
        [n.memoizedState, e]
      );
    },
    useRef: function (e) {
      var t = Fe();
      return (e = { current: e }), (t.memoizedState = e);
    },
    useState: bo,
    useDebugValue: yu,
    useDeferredValue: function (e) {
      return (Fe().memoizedState = e);
    },
    useTransition: function () {
      var e = bo(!1),
        t = e[0];
      return (e = Jf.bind(null, e[1])), (Fe().memoizedState = e), [t, e];
    },
    useMutableSource: function () {},
    useSyncExternalStore: function (e, t, r) {
      var n = A,
        l = Fe();
      if (j) {
        if (r === void 0) throw Error(g(407));
        r = r();
      } else {
        if (((r = t()), X === null)) throw Error(g(349));
        Pt & 30 || is(n, t, r);
      }
      l.memoizedState = r;
      var a = { value: r, getSnapshot: t };
      return (
        (l.queue = a),
        ko(cs.bind(null, n, a, e), [e]),
        (n.flags |= 2048),
        Hr(9, ss.bind(null, n, a, r, t), void 0, null),
        r
      );
    },
    useId: function () {
      var e = Fe(),
        t = X.identifierPrefix;
      if (j) {
        var r = $e,
          n = Ve;
        (r = (n & ~(1 << (32 - Te(n) - 1))).toString(32) + r),
          (t = ':' + t + 'R' + r),
          (r = Br++),
          0 < r && (t += 'H' + r.toString(32)),
          (t += ':');
      } else (r = Zf++), (t = ':' + t + 'r' + r.toString(32) + ':');
      return (e.memoizedState = t);
    },
    unstable_isNewReconciler: !1,
  },
  nd = {
    readContext: Ee,
    useCallback: ys,
    useContext: Ee,
    useEffect: vu,
    useImperativeHandle: vs,
    useInsertionEffect: ms,
    useLayoutEffect: hs,
    useMemo: bs,
    useReducer: Ul,
    useRef: ps,
    useState: function () {
      return Ul(Qr);
    },
    useDebugValue: yu,
    useDeferredValue: function (e) {
      var t = _e();
      return ks(t, q.memoizedState, e);
    },
    useTransition: function () {
      var e = Ul(Qr)[0],
        t = _e().memoizedState;
      return [e, t];
    },
    useMutableSource: us,
    useSyncExternalStore: os,
    useId: ws,
    unstable_isNewReconciler: !1,
  },
  ld = {
    readContext: Ee,
    useCallback: ys,
    useContext: Ee,
    useEffect: vu,
    useImperativeHandle: vs,
    useInsertionEffect: ms,
    useLayoutEffect: hs,
    useMemo: bs,
    useReducer: Al,
    useRef: ps,
    useState: function () {
      return Al(Qr);
    },
    useDebugValue: yu,
    useDeferredValue: function (e) {
      var t = _e();
      return q === null ? (t.memoizedState = e) : ks(t, q.memoizedState, e);
    },
    useTransition: function () {
      var e = Al(Qr)[0],
        t = _e().memoizedState;
      return [e, t];
    },
    useMutableSource: us,
    useSyncExternalStore: os,
    useId: ws,
    unstable_isNewReconciler: !1,
  };
function Ne(e, t) {
  if (e && e.defaultProps) {
    (t = V({}, t)), (e = e.defaultProps);
    for (var r in e) t[r] === void 0 && (t[r] = e[r]);
    return t;
  }
  return t;
}
function Sa(e, t, r, n) {
  (t = e.memoizedState),
    (r = r(n, t)),
    (r = r == null ? t : V({}, t, r)),
    (e.memoizedState = r),
    e.lanes === 0 && (e.updateQueue.baseState = r);
}
var il = {
  isMounted: function (e) {
    return (e = e._reactInternals) ? Tt(e) === e : !1;
  },
  enqueueSetState: function (e, t, r) {
    e = e._reactInternals;
    var n = ue(),
      l = st(e),
      a = Be(n, l);
    (a.payload = t),
      r != null && (a.callback = r),
      (t = ot(e, a, l)),
      t !== null && (Re(t, e, l, n), xn(t, e, l));
  },
  enqueueReplaceState: function (e, t, r) {
    e = e._reactInternals;
    var n = ue(),
      l = st(e),
      a = Be(n, l);
    (a.tag = 1),
      (a.payload = t),
      r != null && (a.callback = r),
      (t = ot(e, a, l)),
      t !== null && (Re(t, e, l, n), xn(t, e, l));
  },
  enqueueForceUpdate: function (e, t) {
    e = e._reactInternals;
    var r = ue(),
      n = st(e),
      l = Be(r, n);
    (l.tag = 2),
      t != null && (l.callback = t),
      (t = ot(e, l, n)),
      t !== null && (Re(t, e, n, r), xn(t, e, n));
  },
};
function wo(e, t, r, n, l, a, u) {
  return (
    (e = e.stateNode),
    typeof e.shouldComponentUpdate == 'function'
      ? e.shouldComponentUpdate(n, a, u)
      : t.prototype && t.prototype.isPureReactComponent
        ? !Dr(r, n) || !Dr(l, a)
        : !0
  );
}
function _s(e, t, r) {
  var n = !1,
    l = dt,
    a = t.contextType;
  return (
    typeof a == 'object' && a !== null
      ? (a = Ee(a))
      : ((l = de(t) ? _t : le.current),
        (n = t.contextTypes),
        (a = (n = n != null) ? Zt(e, l) : dt)),
    (t = new t(r, a)),
    (e.memoizedState =
      t.state !== null && t.state !== void 0 ? t.state : null),
    (t.updater = il),
    (e.stateNode = t),
    (t._reactInternals = e),
    n &&
      ((e = e.stateNode),
      (e.__reactInternalMemoizedUnmaskedChildContext = l),
      (e.__reactInternalMemoizedMaskedChildContext = a)),
    t
  );
}
function So(e, t, r, n) {
  (e = t.state),
    typeof t.componentWillReceiveProps == 'function' &&
      t.componentWillReceiveProps(r, n),
    typeof t.UNSAFE_componentWillReceiveProps == 'function' &&
      t.UNSAFE_componentWillReceiveProps(r, n),
    t.state !== e && il.enqueueReplaceState(t, t.state, null);
}
function xa(e, t, r, n) {
  var l = e.stateNode;
  (l.props = r), (l.state = e.memoizedState), (l.refs = {}), cu(e);
  var a = t.contextType;
  typeof a == 'object' && a !== null
    ? (l.context = Ee(a))
    : ((a = de(t) ? _t : le.current), (l.context = Zt(e, a))),
    (l.state = e.memoizedState),
    (a = t.getDerivedStateFromProps),
    typeof a == 'function' && (Sa(e, t, a, r), (l.state = e.memoizedState)),
    typeof t.getDerivedStateFromProps == 'function' ||
      typeof l.getSnapshotBeforeUpdate == 'function' ||
      (typeof l.UNSAFE_componentWillMount != 'function' &&
        typeof l.componentWillMount != 'function') ||
      ((t = l.state),
      typeof l.componentWillMount == 'function' && l.componentWillMount(),
      typeof l.UNSAFE_componentWillMount == 'function' &&
        l.UNSAFE_componentWillMount(),
      t !== l.state && il.enqueueReplaceState(l, l.state, null),
      Hn(e, r, l, n),
      (l.state = e.memoizedState)),
    typeof l.componentDidMount == 'function' && (e.flags |= 4194308);
}
function rr(e, t) {
  try {
    var r = '',
      n = t;
    do (r += Tc(n)), (n = n.return);
    while (n);
    var l = r;
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
function Vl(e, t, r) {
  return { value: e, source: null, stack: r ?? null, digest: t ?? null };
}
function Ea(e, t) {
  try {
    console.error(t.value);
  } catch (r) {
    setTimeout(function () {
      throw r;
    });
  }
}
var ad = typeof WeakMap == 'function' ? WeakMap : Map;
function Cs(e, t, r) {
  (r = Be(-1, r)), (r.tag = 3), (r.payload = { element: null });
  var n = t.value;
  return (
    (r.callback = function () {
      Gn || ((Gn = !0), (Oa = n)), Ea(e, t);
    }),
    r
  );
}
function Ps(e, t, r) {
  (r = Be(-1, r)), (r.tag = 3);
  var n = e.type.getDerivedStateFromError;
  if (typeof n == 'function') {
    var l = t.value;
    (r.payload = function () {
      return n(l);
    }),
      (r.callback = function () {
        Ea(e, t);
      });
  }
  var a = e.stateNode;
  return (
    a !== null &&
      typeof a.componentDidCatch == 'function' &&
      (r.callback = function () {
        Ea(e, t),
          typeof n != 'function' &&
            (it === null ? (it = new Set([this])) : it.add(this));
        var u = t.stack;
        this.componentDidCatch(t.value, {
          componentStack: u !== null ? u : '',
        });
      }),
    r
  );
}
function xo(e, t, r) {
  var n = e.pingCache;
  if (n === null) {
    n = e.pingCache = new ad();
    var l = new Set();
    n.set(t, l);
  } else (l = n.get(t)), l === void 0 && ((l = new Set()), n.set(t, l));
  l.has(r) || (l.add(r), (e = bd.bind(null, e, t, r)), t.then(e, e));
}
function Eo(e) {
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
function _o(e, t, r, n, l) {
  return e.mode & 1
    ? ((e.flags |= 65536), (e.lanes = l), e)
    : (e === t
        ? (e.flags |= 65536)
        : ((e.flags |= 128),
          (r.flags |= 131072),
          (r.flags &= -52805),
          r.tag === 1 &&
            (r.alternate === null
              ? (r.tag = 17)
              : ((t = Be(-1, 1)), (t.tag = 2), ot(r, t, 1))),
          (r.lanes |= 1)),
      e);
}
var ud = Ke.ReactCurrentOwner,
  ce = !1;
function ae(e, t, r, n) {
  t.child = e === null ? rs(t, null, r, n) : er(t, e.child, r, n);
}
function Co(e, t, r, n, l) {
  r = r.render;
  var a = t.ref;
  return (
    Yt(t, l),
    (n = hu(e, t, r, n, a, l)),
    (r = gu()),
    e !== null && !ce
      ? ((t.updateQueue = e.updateQueue),
        (t.flags &= -2053),
        (e.lanes &= ~l),
        qe(e, t, l))
      : (j && r && nu(t), (t.flags |= 1), ae(e, t, n, l), t.child)
  );
}
function Po(e, t, r, n, l) {
  if (e === null) {
    var a = r.type;
    return typeof a == 'function' &&
      !Cu(a) &&
      a.defaultProps === void 0 &&
      r.compare === null &&
      r.defaultProps === void 0
      ? ((t.tag = 15), (t.type = a), Ns(e, t, a, n, l))
      : ((e = zn(r.type, null, n, t, t.mode, l)),
        (e.ref = t.ref),
        (e.return = t),
        (t.child = e));
  }
  if (((a = e.child), !(e.lanes & l))) {
    var u = a.memoizedProps;
    if (
      ((r = r.compare), (r = r !== null ? r : Dr), r(u, n) && e.ref === t.ref)
    )
      return qe(e, t, l);
  }
  return (
    (t.flags |= 1),
    (e = ct(a, n)),
    (e.ref = t.ref),
    (e.return = t),
    (t.child = e)
  );
}
function Ns(e, t, r, n, l) {
  if (e !== null) {
    var a = e.memoizedProps;
    if (Dr(a, n) && e.ref === t.ref)
      if (((ce = !1), (t.pendingProps = n = a), (e.lanes & l) !== 0))
        e.flags & 131072 && (ce = !0);
      else return (t.lanes = e.lanes), qe(e, t, l);
  }
  return _a(e, t, r, n, l);
}
function zs(e, t, r) {
  var n = t.pendingProps,
    l = n.children,
    a = e !== null ? e.memoizedState : null;
  if (n.mode === 'hidden')
    if (!(t.mode & 1))
      (t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }),
        M(Qt, me),
        (me |= r);
    else {
      if (!(r & 1073741824))
        return (
          (e = a !== null ? a.baseLanes | r : r),
          (t.lanes = t.childLanes = 1073741824),
          (t.memoizedState = {
            baseLanes: e,
            cachePool: null,
            transitions: null,
          }),
          (t.updateQueue = null),
          M(Qt, me),
          (me |= e),
          null
        );
      (t.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }),
        (n = a !== null ? a.baseLanes : r),
        M(Qt, me),
        (me |= n);
    }
  else
    a !== null ? ((n = a.baseLanes | r), (t.memoizedState = null)) : (n = r),
      M(Qt, me),
      (me |= n);
  return ae(e, t, l, r), t.child;
}
function Ls(e, t) {
  var r = t.ref;
  ((e === null && r !== null) || (e !== null && e.ref !== r)) &&
    ((t.flags |= 512), (t.flags |= 2097152));
}
function _a(e, t, r, n, l) {
  var a = de(r) ? _t : le.current;
  return (
    (a = Zt(t, a)),
    Yt(t, l),
    (r = hu(e, t, r, n, a, l)),
    (n = gu()),
    e !== null && !ce
      ? ((t.updateQueue = e.updateQueue),
        (t.flags &= -2053),
        (e.lanes &= ~l),
        qe(e, t, l))
      : (j && n && nu(t), (t.flags |= 1), ae(e, t, r, l), t.child)
  );
}
function No(e, t, r, n, l) {
  if (de(r)) {
    var a = !0;
    An(t);
  } else a = !1;
  if ((Yt(t, l), t.stateNode === null))
    Cn(e, t), _s(t, r, n), xa(t, r, n, l), (n = !0);
  else if (e === null) {
    var u = t.stateNode,
      o = t.memoizedProps;
    u.props = o;
    var i = u.context,
      c = r.contextType;
    typeof c == 'object' && c !== null
      ? (c = Ee(c))
      : ((c = de(r) ? _t : le.current), (c = Zt(t, c)));
    var h = r.getDerivedStateFromProps,
      m =
        typeof h == 'function' ||
        typeof u.getSnapshotBeforeUpdate == 'function';
    m ||
      (typeof u.UNSAFE_componentWillReceiveProps != 'function' &&
        typeof u.componentWillReceiveProps != 'function') ||
      ((o !== n || i !== c) && So(t, u, n, c)),
      (Xe = !1);
    var p = t.memoizedState;
    (u.state = p),
      Hn(t, n, u, l),
      (i = t.memoizedState),
      o !== n || p !== i || fe.current || Xe
        ? (typeof h == 'function' && (Sa(t, r, h, n), (i = t.memoizedState)),
          (o = Xe || wo(t, r, o, n, p, i, c))
            ? (m ||
                (typeof u.UNSAFE_componentWillMount != 'function' &&
                  typeof u.componentWillMount != 'function') ||
                (typeof u.componentWillMount == 'function' &&
                  u.componentWillMount(),
                typeof u.UNSAFE_componentWillMount == 'function' &&
                  u.UNSAFE_componentWillMount()),
              typeof u.componentDidMount == 'function' && (t.flags |= 4194308))
            : (typeof u.componentDidMount == 'function' &&
                (t.flags |= 4194308),
              (t.memoizedProps = n),
              (t.memoizedState = i)),
          (u.props = n),
          (u.state = i),
          (u.context = c),
          (n = o))
        : (typeof u.componentDidMount == 'function' && (t.flags |= 4194308),
          (n = !1));
  } else {
    (u = t.stateNode),
      ls(e, t),
      (o = t.memoizedProps),
      (c = t.type === t.elementType ? o : Ne(t.type, o)),
      (u.props = c),
      (m = t.pendingProps),
      (p = u.context),
      (i = r.contextType),
      typeof i == 'object' && i !== null
        ? (i = Ee(i))
        : ((i = de(r) ? _t : le.current), (i = Zt(t, i)));
    var y = r.getDerivedStateFromProps;
    (h =
      typeof y == 'function' ||
      typeof u.getSnapshotBeforeUpdate == 'function') ||
      (typeof u.UNSAFE_componentWillReceiveProps != 'function' &&
        typeof u.componentWillReceiveProps != 'function') ||
      ((o !== m || p !== i) && So(t, u, n, i)),
      (Xe = !1),
      (p = t.memoizedState),
      (u.state = p),
      Hn(t, n, u, l);
    var b = t.memoizedState;
    o !== m || p !== b || fe.current || Xe
      ? (typeof y == 'function' && (Sa(t, r, y, n), (b = t.memoizedState)),
        (c = Xe || wo(t, r, c, n, p, b, i) || !1)
          ? (h ||
              (typeof u.UNSAFE_componentWillUpdate != 'function' &&
                typeof u.componentWillUpdate != 'function') ||
              (typeof u.componentWillUpdate == 'function' &&
                u.componentWillUpdate(n, b, i),
              typeof u.UNSAFE_componentWillUpdate == 'function' &&
                u.UNSAFE_componentWillUpdate(n, b, i)),
            typeof u.componentDidUpdate == 'function' && (t.flags |= 4),
            typeof u.getSnapshotBeforeUpdate == 'function' &&
              (t.flags |= 1024))
          : (typeof u.componentDidUpdate != 'function' ||
              (o === e.memoizedProps && p === e.memoizedState) ||
              (t.flags |= 4),
            typeof u.getSnapshotBeforeUpdate != 'function' ||
              (o === e.memoizedProps && p === e.memoizedState) ||
              (t.flags |= 1024),
            (t.memoizedProps = n),
            (t.memoizedState = b)),
        (u.props = n),
        (u.state = b),
        (u.context = i),
        (n = c))
      : (typeof u.componentDidUpdate != 'function' ||
          (o === e.memoizedProps && p === e.memoizedState) ||
          (t.flags |= 4),
        typeof u.getSnapshotBeforeUpdate != 'function' ||
          (o === e.memoizedProps && p === e.memoizedState) ||
          (t.flags |= 1024),
        (n = !1));
  }
  return Ca(e, t, r, n, a, l);
}
function Ca(e, t, r, n, l, a) {
  Ls(e, t);
  var u = (t.flags & 128) !== 0;
  if (!n && !u) return l && po(t, r, !1), qe(e, t, a);
  (n = t.stateNode), (ud.current = t);
  var o =
    u && typeof r.getDerivedStateFromError != 'function' ? null : n.render();
  return (
    (t.flags |= 1),
    e !== null && u
      ? ((t.child = er(t, e.child, null, a)), (t.child = er(t, null, o, a)))
      : ae(e, t, o, a),
    (t.memoizedState = n.state),
    l && po(t, r, !0),
    t.child
  );
}
function Ts(e) {
  var t = e.stateNode;
  t.pendingContext
    ? fo(e, t.pendingContext, t.pendingContext !== t.context)
    : t.context && fo(e, t.context, !1),
    fu(e, t.containerInfo);
}
function zo(e, t, r, n, l) {
  return Jt(), au(l), (t.flags |= 256), ae(e, t, r, n), t.child;
}
var Pa = { dehydrated: null, treeContext: null, retryLane: 0 };
function Na(e) {
  return { baseLanes: e, cachePool: null, transitions: null };
}
function Rs(e, t, r) {
  var n = t.pendingProps,
    l = U.current,
    a = !1,
    u = (t.flags & 128) !== 0,
    o;
  if (
    ((o = u) ||
      (o = e !== null && e.memoizedState === null ? !1 : (l & 2) !== 0),
    o
      ? ((a = !0), (t.flags &= -129))
      : (e === null || e.memoizedState !== null) && (l |= 1),
    M(U, l & 1),
    e === null)
  )
    return (
      ka(t),
      (e = t.memoizedState),
      e !== null && ((e = e.dehydrated), e !== null)
        ? (t.mode & 1
            ? e.data === '$!'
              ? (t.lanes = 8)
              : (t.lanes = 1073741824)
            : (t.lanes = 1),
          null)
        : ((u = n.children),
          (e = n.fallback),
          a
            ? ((n = t.mode),
              (a = t.child),
              (u = { mode: 'hidden', children: u }),
              !(n & 1) && a !== null
                ? ((a.childLanes = 0), (a.pendingProps = u))
                : (a = fl(u, n, 0, null)),
              (e = Et(e, n, r, null)),
              (a.return = t),
              (e.return = t),
              (a.sibling = e),
              (t.child = a),
              (t.child.memoizedState = Na(r)),
              (t.memoizedState = Pa),
              e)
            : bu(t, u))
    );
  if (((l = e.memoizedState), l !== null && ((o = l.dehydrated), o !== null)))
    return od(e, t, u, n, o, l, r);
  if (a) {
    (a = n.fallback), (u = t.mode), (l = e.child), (o = l.sibling);
    var i = { mode: 'hidden', children: n.children };
    return (
      !(u & 1) && t.child !== l
        ? ((n = t.child),
          (n.childLanes = 0),
          (n.pendingProps = i),
          (t.deletions = null))
        : ((n = ct(l, i)), (n.subtreeFlags = l.subtreeFlags & 14680064)),
      o !== null ? (a = ct(o, a)) : ((a = Et(a, u, r, null)), (a.flags |= 2)),
      (a.return = t),
      (n.return = t),
      (n.sibling = a),
      (t.child = n),
      (n = a),
      (a = t.child),
      (u = e.child.memoizedState),
      (u =
        u === null
          ? Na(r)
          : {
              baseLanes: u.baseLanes | r,
              cachePool: null,
              transitions: u.transitions,
            }),
      (a.memoizedState = u),
      (a.childLanes = e.childLanes & ~r),
      (t.memoizedState = Pa),
      n
    );
  }
  return (
    (a = e.child),
    (e = a.sibling),
    (n = ct(a, { mode: 'visible', children: n.children })),
    !(t.mode & 1) && (n.lanes = r),
    (n.return = t),
    (n.sibling = null),
    e !== null &&
      ((r = t.deletions),
      r === null ? ((t.deletions = [e]), (t.flags |= 16)) : r.push(e)),
    (t.child = n),
    (t.memoizedState = null),
    n
  );
}
function bu(e, t) {
  return (
    (t = fl({ mode: 'visible', children: t }, e.mode, 0, null)),
    (t.return = e),
    (e.child = t)
  );
}
function mn(e, t, r, n) {
  return (
    n !== null && au(n),
    er(t, e.child, null, r),
    (e = bu(t, t.pendingProps.children)),
    (e.flags |= 2),
    (t.memoizedState = null),
    e
  );
}
function od(e, t, r, n, l, a, u) {
  if (r)
    return t.flags & 256
      ? ((t.flags &= -257), (n = Vl(Error(g(422)))), mn(e, t, u, n))
      : t.memoizedState !== null
        ? ((t.child = e.child), (t.flags |= 128), null)
        : ((a = n.fallback),
          (l = t.mode),
          (n = fl({ mode: 'visible', children: n.children }, l, 0, null)),
          (a = Et(a, l, u, null)),
          (a.flags |= 2),
          (n.return = t),
          (a.return = t),
          (n.sibling = a),
          (t.child = n),
          t.mode & 1 && er(t, e.child, null, u),
          (t.child.memoizedState = Na(u)),
          (t.memoizedState = Pa),
          a);
  if (!(t.mode & 1)) return mn(e, t, u, null);
  if (l.data === '$!') {
    if (((n = l.nextSibling && l.nextSibling.dataset), n)) var o = n.dgst;
    return (
      (n = o), (a = Error(g(419))), (n = Vl(a, n, void 0)), mn(e, t, u, n)
    );
  }
  if (((o = (u & e.childLanes) !== 0), ce || o)) {
    if (((n = X), n !== null)) {
      switch (u & -u) {
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
      (l = l & (n.suspendedLanes | u) ? 0 : l),
        l !== 0 &&
          l !== a.retryLane &&
          ((a.retryLane = l), We(e, l), Re(n, e, l, -1));
    }
    return _u(), (n = Vl(Error(g(421)))), mn(e, t, u, n);
  }
  return l.data === '$?'
    ? ((t.flags |= 128),
      (t.child = e.child),
      (t = kd.bind(null, e)),
      (l._reactRetry = t),
      null)
    : ((e = a.treeContext),
      (he = ut(l.nextSibling)),
      (ge = t),
      (j = !0),
      (Le = null),
      e !== null &&
        ((ke[we++] = Ve),
        (ke[we++] = $e),
        (ke[we++] = Ct),
        (Ve = e.id),
        ($e = e.overflow),
        (Ct = t)),
      (t = bu(t, n.children)),
      (t.flags |= 4096),
      t);
}
function Lo(e, t, r) {
  e.lanes |= t;
  var n = e.alternate;
  n !== null && (n.lanes |= t), wa(e.return, t, r);
}
function $l(e, t, r, n, l) {
  var a = e.memoizedState;
  a === null
    ? (e.memoizedState = {
        isBackwards: t,
        rendering: null,
        renderingStartTime: 0,
        last: n,
        tail: r,
        tailMode: l,
      })
    : ((a.isBackwards = t),
      (a.rendering = null),
      (a.renderingStartTime = 0),
      (a.last = n),
      (a.tail = r),
      (a.tailMode = l));
}
function Os(e, t, r) {
  var n = t.pendingProps,
    l = n.revealOrder,
    a = n.tail;
  if ((ae(e, t, n.children, r), (n = U.current), n & 2))
    (n = (n & 1) | 2), (t.flags |= 128);
  else {
    if (e !== null && e.flags & 128)
      e: for (e = t.child; e !== null; ) {
        if (e.tag === 13) e.memoizedState !== null && Lo(e, r, t);
        else if (e.tag === 19) Lo(e, r, t);
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
    n &= 1;
  }
  if ((M(U, n), !(t.mode & 1))) t.memoizedState = null;
  else
    switch (l) {
      case 'forwards':
        for (r = t.child, l = null; r !== null; )
          (e = r.alternate),
            e !== null && Wn(e) === null && (l = r),
            (r = r.sibling);
        (r = l),
          r === null
            ? ((l = t.child), (t.child = null))
            : ((l = r.sibling), (r.sibling = null)),
          $l(t, !1, l, r, a);
        break;
      case 'backwards':
        for (r = null, l = t.child, t.child = null; l !== null; ) {
          if (((e = l.alternate), e !== null && Wn(e) === null)) {
            t.child = l;
            break;
          }
          (e = l.sibling), (l.sibling = r), (r = l), (l = e);
        }
        $l(t, !0, r, null, a);
        break;
      case 'together':
        $l(t, !1, null, null, void 0);
        break;
      default:
        t.memoizedState = null;
    }
  return t.child;
}
function Cn(e, t) {
  !(t.mode & 1) &&
    e !== null &&
    ((e.alternate = null), (t.alternate = null), (t.flags |= 2));
}
function qe(e, t, r) {
  if (
    (e !== null && (t.dependencies = e.dependencies),
    (Nt |= t.lanes),
    !(r & t.childLanes))
  )
    return null;
  if (e !== null && t.child !== e.child) throw Error(g(153));
  if (t.child !== null) {
    for (
      e = t.child, r = ct(e, e.pendingProps), t.child = r, r.return = t;
      e.sibling !== null;

    )
      (e = e.sibling), (r = r.sibling = ct(e, e.pendingProps)), (r.return = t);
    r.sibling = null;
  }
  return t.child;
}
function id(e, t, r) {
  switch (t.tag) {
    case 3:
      Ts(t), Jt();
      break;
    case 5:
      as(t);
      break;
    case 1:
      de(t.type) && An(t);
      break;
    case 4:
      fu(t, t.stateNode.containerInfo);
      break;
    case 10:
      var n = t.type._context,
        l = t.memoizedProps.value;
      M(Bn, n._currentValue), (n._currentValue = l);
      break;
    case 13:
      if (((n = t.memoizedState), n !== null))
        return n.dehydrated !== null
          ? (M(U, U.current & 1), (t.flags |= 128), null)
          : r & t.child.childLanes
            ? Rs(e, t, r)
            : (M(U, U.current & 1),
              (e = qe(e, t, r)),
              e !== null ? e.sibling : null);
      M(U, U.current & 1);
      break;
    case 19:
      if (((n = (r & t.childLanes) !== 0), e.flags & 128)) {
        if (n) return Os(e, t, r);
        t.flags |= 128;
      }
      if (
        ((l = t.memoizedState),
        l !== null &&
          ((l.rendering = null), (l.tail = null), (l.lastEffect = null)),
        M(U, U.current),
        n)
      )
        break;
      return null;
    case 22:
    case 23:
      return (t.lanes = 0), zs(e, t, r);
  }
  return qe(e, t, r);
}
var Ms, za, Fs, Is;
Ms = function (e, t) {
  for (var r = t.child; r !== null; ) {
    if (r.tag === 5 || r.tag === 6) e.appendChild(r.stateNode);
    else if (r.tag !== 4 && r.child !== null) {
      (r.child.return = r), (r = r.child);
      continue;
    }
    if (r === t) break;
    for (; r.sibling === null; ) {
      if (r.return === null || r.return === t) return;
      r = r.return;
    }
    (r.sibling.return = r.return), (r = r.sibling);
  }
};
za = function () {};
Fs = function (e, t, r, n) {
  var l = e.memoizedProps;
  if (l !== n) {
    (e = t.stateNode), St(je.current);
    var a = null;
    switch (r) {
      case 'input':
        (l = Xl(e, l)), (n = Xl(e, n)), (a = []);
        break;
      case 'select':
        (l = V({}, l, { value: void 0 })),
          (n = V({}, n, { value: void 0 })),
          (a = []);
        break;
      case 'textarea':
        (l = ea(e, l)), (n = ea(e, n)), (a = []);
        break;
      default:
        typeof l.onClick != 'function' &&
          typeof n.onClick == 'function' &&
          (e.onclick = jn);
    }
    ra(r, n);
    var u;
    r = null;
    for (c in l)
      if (!n.hasOwnProperty(c) && l.hasOwnProperty(c) && l[c] != null)
        if (c === 'style') {
          var o = l[c];
          for (u in o) o.hasOwnProperty(u) && (r || (r = {}), (r[u] = ''));
        } else
          c !== 'dangerouslySetInnerHTML' &&
            c !== 'children' &&
            c !== 'suppressContentEditableWarning' &&
            c !== 'suppressHydrationWarning' &&
            c !== 'autoFocus' &&
            (Lr.hasOwnProperty(c)
              ? a || (a = [])
              : (a = a || []).push(c, null));
    for (c in n) {
      var i = n[c];
      if (
        ((o = l != null ? l[c] : void 0),
        n.hasOwnProperty(c) && i !== o && (i != null || o != null))
      )
        if (c === 'style')
          if (o) {
            for (u in o)
              !o.hasOwnProperty(u) ||
                (i && i.hasOwnProperty(u)) ||
                (r || (r = {}), (r[u] = ''));
            for (u in i)
              i.hasOwnProperty(u) &&
                o[u] !== i[u] &&
                (r || (r = {}), (r[u] = i[u]));
          } else r || (a || (a = []), a.push(c, r)), (r = i);
        else
          c === 'dangerouslySetInnerHTML'
            ? ((i = i ? i.__html : void 0),
              (o = o ? o.__html : void 0),
              i != null && o !== i && (a = a || []).push(c, i))
            : c === 'children'
              ? (typeof i != 'string' && typeof i != 'number') ||
                (a = a || []).push(c, '' + i)
              : c !== 'suppressContentEditableWarning' &&
                c !== 'suppressHydrationWarning' &&
                (Lr.hasOwnProperty(c)
                  ? (i != null && c === 'onScroll' && F('scroll', e),
                    a || o === i || (a = []))
                  : (a = a || []).push(c, i));
    }
    r && (a = a || []).push('style', r);
    var c = a;
    (t.updateQueue = c) && (t.flags |= 4);
  }
};
Is = function (e, t, r, n) {
  r !== n && (t.flags |= 4);
};
function hr(e, t) {
  if (!j)
    switch (e.tailMode) {
      case 'hidden':
        t = e.tail;
        for (var r = null; t !== null; )
          t.alternate !== null && (r = t), (t = t.sibling);
        r === null ? (e.tail = null) : (r.sibling = null);
        break;
      case 'collapsed':
        r = e.tail;
        for (var n = null; r !== null; )
          r.alternate !== null && (n = r), (r = r.sibling);
        n === null
          ? t || e.tail === null
            ? (e.tail = null)
            : (e.tail.sibling = null)
          : (n.sibling = null);
    }
}
function re(e) {
  var t = e.alternate !== null && e.alternate.child === e.child,
    r = 0,
    n = 0;
  if (t)
    for (var l = e.child; l !== null; )
      (r |= l.lanes | l.childLanes),
        (n |= l.subtreeFlags & 14680064),
        (n |= l.flags & 14680064),
        (l.return = e),
        (l = l.sibling);
  else
    for (l = e.child; l !== null; )
      (r |= l.lanes | l.childLanes),
        (n |= l.subtreeFlags),
        (n |= l.flags),
        (l.return = e),
        (l = l.sibling);
  return (e.subtreeFlags |= n), (e.childLanes = r), t;
}
function sd(e, t, r) {
  var n = t.pendingProps;
  switch ((lu(t), t.tag)) {
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
      return de(t.type) && Un(), re(t), null;
    case 3:
      return (
        (n = t.stateNode),
        tr(),
        I(fe),
        I(le),
        pu(),
        n.pendingContext &&
          ((n.context = n.pendingContext), (n.pendingContext = null)),
        (e === null || e.child === null) &&
          (dn(t)
            ? (t.flags |= 4)
            : e === null ||
              (e.memoizedState.isDehydrated && !(t.flags & 256)) ||
              ((t.flags |= 1024), Le !== null && (Ia(Le), (Le = null)))),
        za(e, t),
        re(t),
        null
      );
    case 5:
      du(t);
      var l = St($r.current);
      if (((r = t.type), e !== null && t.stateNode != null))
        Fs(e, t, r, n, l),
          e.ref !== t.ref && ((t.flags |= 512), (t.flags |= 2097152));
      else {
        if (!n) {
          if (t.stateNode === null) throw Error(g(166));
          return re(t), null;
        }
        if (((e = St(je.current)), dn(t))) {
          (n = t.stateNode), (r = t.type);
          var a = t.memoizedProps;
          switch (((n[Ie] = t), (n[Ar] = a), (e = (t.mode & 1) !== 0), r)) {
            case 'dialog':
              F('cancel', n), F('close', n);
              break;
            case 'iframe':
            case 'object':
            case 'embed':
              F('load', n);
              break;
            case 'video':
            case 'audio':
              for (l = 0; l < kr.length; l++) F(kr[l], n);
              break;
            case 'source':
              F('error', n);
              break;
            case 'img':
            case 'image':
            case 'link':
              F('error', n), F('load', n);
              break;
            case 'details':
              F('toggle', n);
              break;
            case 'input':
              ju(n, a), F('invalid', n);
              break;
            case 'select':
              (n._wrapperState = { wasMultiple: !!a.multiple }),
                F('invalid', n);
              break;
            case 'textarea':
              Au(n, a), F('invalid', n);
          }
          ra(r, a), (l = null);
          for (var u in a)
            if (a.hasOwnProperty(u)) {
              var o = a[u];
              u === 'children'
                ? typeof o == 'string'
                  ? n.textContent !== o &&
                    (a.suppressHydrationWarning !== !0 &&
                      fn(n.textContent, o, e),
                    (l = ['children', o]))
                  : typeof o == 'number' &&
                    n.textContent !== '' + o &&
                    (a.suppressHydrationWarning !== !0 &&
                      fn(n.textContent, o, e),
                    (l = ['children', '' + o]))
                : Lr.hasOwnProperty(u) &&
                  o != null &&
                  u === 'onScroll' &&
                  F('scroll', n);
            }
          switch (r) {
            case 'input':
              rn(n), Uu(n, a, !0);
              break;
            case 'textarea':
              rn(n), Vu(n);
              break;
            case 'select':
            case 'option':
              break;
            default:
              typeof a.onClick == 'function' && (n.onclick = jn);
          }
          (n = l), (t.updateQueue = n), n !== null && (t.flags |= 4);
        } else {
          (u = l.nodeType === 9 ? l : l.ownerDocument),
            e === 'http://www.w3.org/1999/xhtml' && (e = ci(r)),
            e === 'http://www.w3.org/1999/xhtml'
              ? r === 'script'
                ? ((e = u.createElement('div')),
                  (e.innerHTML = '<script><\/script>'),
                  (e = e.removeChild(e.firstChild)))
                : typeof n.is == 'string'
                  ? (e = u.createElement(r, { is: n.is }))
                  : ((e = u.createElement(r)),
                    r === 'select' &&
                      ((u = e),
                      n.multiple
                        ? (u.multiple = !0)
                        : n.size && (u.size = n.size)))
              : (e = u.createElementNS(e, r)),
            (e[Ie] = t),
            (e[Ar] = n),
            Ms(e, t, !1, !1),
            (t.stateNode = e);
          e: {
            switch (((u = na(r, n)), r)) {
              case 'dialog':
                F('cancel', e), F('close', e), (l = n);
                break;
              case 'iframe':
              case 'object':
              case 'embed':
                F('load', e), (l = n);
                break;
              case 'video':
              case 'audio':
                for (l = 0; l < kr.length; l++) F(kr[l], e);
                l = n;
                break;
              case 'source':
                F('error', e), (l = n);
                break;
              case 'img':
              case 'image':
              case 'link':
                F('error', e), F('load', e), (l = n);
                break;
              case 'details':
                F('toggle', e), (l = n);
                break;
              case 'input':
                ju(e, n), (l = Xl(e, n)), F('invalid', e);
                break;
              case 'option':
                l = n;
                break;
              case 'select':
                (e._wrapperState = { wasMultiple: !!n.multiple }),
                  (l = V({}, n, { value: void 0 })),
                  F('invalid', e);
                break;
              case 'textarea':
                Au(e, n), (l = ea(e, n)), F('invalid', e);
                break;
              default:
                l = n;
            }
            ra(r, l), (o = l);
            for (a in o)
              if (o.hasOwnProperty(a)) {
                var i = o[a];
                a === 'style'
                  ? pi(e, i)
                  : a === 'dangerouslySetInnerHTML'
                    ? ((i = i ? i.__html : void 0), i != null && fi(e, i))
                    : a === 'children'
                      ? typeof i == 'string'
                        ? (r !== 'textarea' || i !== '') && Tr(e, i)
                        : typeof i == 'number' && Tr(e, '' + i)
                      : a !== 'suppressContentEditableWarning' &&
                        a !== 'suppressHydrationWarning' &&
                        a !== 'autoFocus' &&
                        (Lr.hasOwnProperty(a)
                          ? i != null && a === 'onScroll' && F('scroll', e)
                          : i != null && Ba(e, a, i, u));
              }
            switch (r) {
              case 'input':
                rn(e), Uu(e, n, !1);
                break;
              case 'textarea':
                rn(e), Vu(e);
                break;
              case 'option':
                n.value != null && e.setAttribute('value', '' + ft(n.value));
                break;
              case 'select':
                (e.multiple = !!n.multiple),
                  (a = n.value),
                  a != null
                    ? Ht(e, !!n.multiple, a, !1)
                    : n.defaultValue != null &&
                      Ht(e, !!n.multiple, n.defaultValue, !0);
                break;
              default:
                typeof l.onClick == 'function' && (e.onclick = jn);
            }
            switch (r) {
              case 'button':
              case 'input':
              case 'select':
              case 'textarea':
                n = !!n.autoFocus;
                break e;
              case 'img':
                n = !0;
                break e;
              default:
                n = !1;
            }
          }
          n && (t.flags |= 4);
        }
        t.ref !== null && ((t.flags |= 512), (t.flags |= 2097152));
      }
      return re(t), null;
    case 6:
      if (e && t.stateNode != null) Is(e, t, e.memoizedProps, n);
      else {
        if (typeof n != 'string' && t.stateNode === null) throw Error(g(166));
        if (((r = St($r.current)), St(je.current), dn(t))) {
          if (
            ((n = t.stateNode),
            (r = t.memoizedProps),
            (n[Ie] = t),
            (a = n.nodeValue !== r) && ((e = ge), e !== null))
          )
            switch (e.tag) {
              case 3:
                fn(n.nodeValue, r, (e.mode & 1) !== 0);
                break;
              case 5:
                e.memoizedProps.suppressHydrationWarning !== !0 &&
                  fn(n.nodeValue, r, (e.mode & 1) !== 0);
            }
          a && (t.flags |= 4);
        } else
          (n = (r.nodeType === 9 ? r : r.ownerDocument).createTextNode(n)),
            (n[Ie] = t),
            (t.stateNode = n);
      }
      return re(t), null;
    case 13:
      if (
        (I(U),
        (n = t.memoizedState),
        e === null ||
          (e.memoizedState !== null && e.memoizedState.dehydrated !== null))
      ) {
        if (j && he !== null && t.mode & 1 && !(t.flags & 128))
          es(), Jt(), (t.flags |= 98560), (a = !1);
        else if (((a = dn(t)), n !== null && n.dehydrated !== null)) {
          if (e === null) {
            if (!a) throw Error(g(318));
            if (
              ((a = t.memoizedState),
              (a = a !== null ? a.dehydrated : null),
              !a)
            )
              throw Error(g(317));
            a[Ie] = t;
          } else
            Jt(), !(t.flags & 128) && (t.memoizedState = null), (t.flags |= 4);
          re(t), (a = !1);
        } else Le !== null && (Ia(Le), (Le = null)), (a = !0);
        if (!a) return t.flags & 65536 ? t : null;
      }
      return t.flags & 128
        ? ((t.lanes = r), t)
        : ((n = n !== null),
          n !== (e !== null && e.memoizedState !== null) &&
            n &&
            ((t.child.flags |= 8192),
            t.mode & 1 &&
              (e === null || U.current & 1 ? K === 0 && (K = 3) : _u())),
          t.updateQueue !== null && (t.flags |= 4),
          re(t),
          null);
    case 4:
      return (
        tr(),
        za(e, t),
        e === null && jr(t.stateNode.containerInfo),
        re(t),
        null
      );
    case 10:
      return iu(t.type._context), re(t), null;
    case 17:
      return de(t.type) && Un(), re(t), null;
    case 19:
      if ((I(U), (a = t.memoizedState), a === null)) return re(t), null;
      if (((n = (t.flags & 128) !== 0), (u = a.rendering), u === null))
        if (n) hr(a, !1);
        else {
          if (K !== 0 || (e !== null && e.flags & 128))
            for (e = t.child; e !== null; ) {
              if (((u = Wn(e)), u !== null)) {
                for (
                  t.flags |= 128,
                    hr(a, !1),
                    n = u.updateQueue,
                    n !== null && ((t.updateQueue = n), (t.flags |= 4)),
                    t.subtreeFlags = 0,
                    n = r,
                    r = t.child;
                  r !== null;

                )
                  (a = r),
                    (e = n),
                    (a.flags &= 14680066),
                    (u = a.alternate),
                    u === null
                      ? ((a.childLanes = 0),
                        (a.lanes = e),
                        (a.child = null),
                        (a.subtreeFlags = 0),
                        (a.memoizedProps = null),
                        (a.memoizedState = null),
                        (a.updateQueue = null),
                        (a.dependencies = null),
                        (a.stateNode = null))
                      : ((a.childLanes = u.childLanes),
                        (a.lanes = u.lanes),
                        (a.child = u.child),
                        (a.subtreeFlags = 0),
                        (a.deletions = null),
                        (a.memoizedProps = u.memoizedProps),
                        (a.memoizedState = u.memoizedState),
                        (a.updateQueue = u.updateQueue),
                        (a.type = u.type),
                        (e = u.dependencies),
                        (a.dependencies =
                          e === null
                            ? null
                            : {
                                lanes: e.lanes,
                                firstContext: e.firstContext,
                              })),
                    (r = r.sibling);
                return M(U, (U.current & 1) | 2), t.child;
              }
              e = e.sibling;
            }
          a.tail !== null &&
            H() > nr &&
            ((t.flags |= 128), (n = !0), hr(a, !1), (t.lanes = 4194304));
        }
      else {
        if (!n)
          if (((e = Wn(u)), e !== null)) {
            if (
              ((t.flags |= 128),
              (n = !0),
              (r = e.updateQueue),
              r !== null && ((t.updateQueue = r), (t.flags |= 4)),
              hr(a, !0),
              a.tail === null && a.tailMode === 'hidden' && !u.alternate && !j)
            )
              return re(t), null;
          } else
            2 * H() - a.renderingStartTime > nr &&
              r !== 1073741824 &&
              ((t.flags |= 128), (n = !0), hr(a, !1), (t.lanes = 4194304));
        a.isBackwards
          ? ((u.sibling = t.child), (t.child = u))
          : ((r = a.last),
            r !== null ? (r.sibling = u) : (t.child = u),
            (a.last = u));
      }
      return a.tail !== null
        ? ((t = a.tail),
          (a.rendering = t),
          (a.tail = t.sibling),
          (a.renderingStartTime = H()),
          (t.sibling = null),
          (r = U.current),
          M(U, n ? (r & 1) | 2 : r & 1),
          t)
        : (re(t), null);
    case 22:
    case 23:
      return (
        Eu(),
        (n = t.memoizedState !== null),
        e !== null && (e.memoizedState !== null) !== n && (t.flags |= 8192),
        n && t.mode & 1
          ? me & 1073741824 && (re(t), t.subtreeFlags & 6 && (t.flags |= 8192))
          : re(t),
        null
      );
    case 24:
      return null;
    case 25:
      return null;
  }
  throw Error(g(156, t.tag));
}
function cd(e, t) {
  switch ((lu(t), t.tag)) {
    case 1:
      return (
        de(t.type) && Un(),
        (e = t.flags),
        e & 65536 ? ((t.flags = (e & -65537) | 128), t) : null
      );
    case 3:
      return (
        tr(),
        I(fe),
        I(le),
        pu(),
        (e = t.flags),
        e & 65536 && !(e & 128) ? ((t.flags = (e & -65537) | 128), t) : null
      );
    case 5:
      return du(t), null;
    case 13:
      if ((I(U), (e = t.memoizedState), e !== null && e.dehydrated !== null)) {
        if (t.alternate === null) throw Error(g(340));
        Jt();
      }
      return (
        (e = t.flags), e & 65536 ? ((t.flags = (e & -65537) | 128), t) : null
      );
    case 19:
      return I(U), null;
    case 4:
      return tr(), null;
    case 10:
      return iu(t.type._context), null;
    case 22:
    case 23:
      return Eu(), null;
    case 24:
      return null;
    default:
      return null;
  }
}
var hn = !1,
  ne = !1,
  fd = typeof WeakSet == 'function' ? WeakSet : Set,
  w = null;
function Bt(e, t) {
  var r = e.ref;
  if (r !== null)
    if (typeof r == 'function')
      try {
        r(null);
      } catch (n) {
        $(e, t, n);
      }
    else r.current = null;
}
function Ds(e, t, r) {
  try {
    r();
  } catch (n) {
    $(e, t, n);
  }
}
var To = !1;
function dd(e, t) {
  if (((pa = Fn), (e = Vi()), ru(e))) {
    if ('selectionStart' in e)
      var r = { start: e.selectionStart, end: e.selectionEnd };
    else
      e: {
        r = ((r = e.ownerDocument) && r.defaultView) || window;
        var n = r.getSelection && r.getSelection();
        if (n && n.rangeCount !== 0) {
          r = n.anchorNode;
          var l = n.anchorOffset,
            a = n.focusNode;
          n = n.focusOffset;
          try {
            r.nodeType, a.nodeType;
          } catch {
            r = null;
            break e;
          }
          var u = 0,
            o = -1,
            i = -1,
            c = 0,
            h = 0,
            m = e,
            p = null;
          t: for (;;) {
            for (
              var y;
              m !== r || (l !== 0 && m.nodeType !== 3) || (o = u + l),
                m !== a || (n !== 0 && m.nodeType !== 3) || (i = u + n),
                m.nodeType === 3 && (u += m.nodeValue.length),
                (y = m.firstChild) !== null;

            )
              (p = m), (m = y);
            for (;;) {
              if (m === e) break t;
              if (
                (p === r && ++c === l && (o = u),
                p === a && ++h === n && (i = u),
                (y = m.nextSibling) !== null)
              )
                break;
              (m = p), (p = m.parentNode);
            }
            m = y;
          }
          r = o === -1 || i === -1 ? null : { start: o, end: i };
        } else r = null;
      }
    r = r || { start: 0, end: 0 };
  } else r = null;
  for (
    ma = { focusedElem: e, selectionRange: r }, Fn = !1, w = t;
    w !== null;

  )
    if (((t = w), (e = t.child), (t.subtreeFlags & 1028) !== 0 && e !== null))
      (e.return = t), (w = e);
    else
      for (; w !== null; ) {
        t = w;
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
                    D = b.memoizedState,
                    f = t.stateNode,
                    s = f.getSnapshotBeforeUpdate(
                      t.elementType === t.type ? k : Ne(t.type, k),
                      D
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
                throw Error(g(163));
            }
        } catch (v) {
          $(t, t.return, v);
        }
        if (((e = t.sibling), e !== null)) {
          (e.return = t.return), (w = e);
          break;
        }
        w = t.return;
      }
  return (b = To), (To = !1), b;
}
function Pr(e, t, r) {
  var n = t.updateQueue;
  if (((n = n !== null ? n.lastEffect : null), n !== null)) {
    var l = (n = n.next);
    do {
      if ((l.tag & e) === e) {
        var a = l.destroy;
        (l.destroy = void 0), a !== void 0 && Ds(t, r, a);
      }
      l = l.next;
    } while (l !== n);
  }
}
function sl(e, t) {
  if (
    ((t = t.updateQueue), (t = t !== null ? t.lastEffect : null), t !== null)
  ) {
    var r = (t = t.next);
    do {
      if ((r.tag & e) === e) {
        var n = r.create;
        r.destroy = n();
      }
      r = r.next;
    } while (r !== t);
  }
}
function La(e) {
  var t = e.ref;
  if (t !== null) {
    var r = e.stateNode;
    switch (e.tag) {
      case 5:
        e = r;
        break;
      default:
        e = r;
    }
    typeof t == 'function' ? t(e) : (t.current = e);
  }
}
function js(e) {
  var t = e.alternate;
  t !== null && ((e.alternate = null), js(t)),
    (e.child = null),
    (e.deletions = null),
    (e.sibling = null),
    e.tag === 5 &&
      ((t = e.stateNode),
      t !== null &&
        (delete t[Ie],
        delete t[Ar],
        delete t[va],
        delete t[Kf],
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
function Ro(e) {
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
function Ta(e, t, r) {
  var n = e.tag;
  if (n === 5 || n === 6)
    (e = e.stateNode),
      t
        ? r.nodeType === 8
          ? r.parentNode.insertBefore(e, t)
          : r.insertBefore(e, t)
        : (r.nodeType === 8
            ? ((t = r.parentNode), t.insertBefore(e, r))
            : ((t = r), t.appendChild(e)),
          (r = r._reactRootContainer),
          r != null || t.onclick !== null || (t.onclick = jn));
  else if (n !== 4 && ((e = e.child), e !== null))
    for (Ta(e, t, r), e = e.sibling; e !== null; )
      Ta(e, t, r), (e = e.sibling);
}
function Ra(e, t, r) {
  var n = e.tag;
  if (n === 5 || n === 6)
    (e = e.stateNode), t ? r.insertBefore(e, t) : r.appendChild(e);
  else if (n !== 4 && ((e = e.child), e !== null))
    for (Ra(e, t, r), e = e.sibling; e !== null; )
      Ra(e, t, r), (e = e.sibling);
}
var Z = null,
  ze = !1;
function Ye(e, t, r) {
  for (r = r.child; r !== null; ) As(e, t, r), (r = r.sibling);
}
function As(e, t, r) {
  if (De && typeof De.onCommitFiberUnmount == 'function')
    try {
      De.onCommitFiberUnmount(tl, r);
    } catch {}
  switch (r.tag) {
    case 5:
      ne || Bt(r, t);
    case 6:
      var n = Z,
        l = ze;
      (Z = null),
        Ye(e, t, r),
        (Z = n),
        (ze = l),
        Z !== null &&
          (ze
            ? ((e = Z),
              (r = r.stateNode),
              e.nodeType === 8
                ? e.parentNode.removeChild(r)
                : e.removeChild(r))
            : Z.removeChild(r.stateNode));
      break;
    case 18:
      Z !== null &&
        (ze
          ? ((e = Z),
            (r = r.stateNode),
            e.nodeType === 8
              ? Fl(e.parentNode, r)
              : e.nodeType === 1 && Fl(e, r),
            Fr(e))
          : Fl(Z, r.stateNode));
      break;
    case 4:
      (n = Z),
        (l = ze),
        (Z = r.stateNode.containerInfo),
        (ze = !0),
        Ye(e, t, r),
        (Z = n),
        (ze = l);
      break;
    case 0:
    case 11:
    case 14:
    case 15:
      if (
        !ne &&
        ((n = r.updateQueue), n !== null && ((n = n.lastEffect), n !== null))
      ) {
        l = n = n.next;
        do {
          var a = l,
            u = a.destroy;
          (a = a.tag),
            u !== void 0 && (a & 2 || a & 4) && Ds(r, t, u),
            (l = l.next);
        } while (l !== n);
      }
      Ye(e, t, r);
      break;
    case 1:
      if (
        !ne &&
        (Bt(r, t),
        (n = r.stateNode),
        typeof n.componentWillUnmount == 'function')
      )
        try {
          (n.props = r.memoizedProps),
            (n.state = r.memoizedState),
            n.componentWillUnmount();
        } catch (o) {
          $(r, t, o);
        }
      Ye(e, t, r);
      break;
    case 21:
      Ye(e, t, r);
      break;
    case 22:
      r.mode & 1
        ? ((ne = (n = ne) || r.memoizedState !== null), Ye(e, t, r), (ne = n))
        : Ye(e, t, r);
      break;
    default:
      Ye(e, t, r);
  }
}
function Oo(e) {
  var t = e.updateQueue;
  if (t !== null) {
    e.updateQueue = null;
    var r = e.stateNode;
    r === null && (r = e.stateNode = new fd()),
      t.forEach(function (n) {
        var l = wd.bind(null, e, n);
        r.has(n) || (r.add(n), n.then(l, l));
      });
  }
}
function Pe(e, t) {
  var r = t.deletions;
  if (r !== null)
    for (var n = 0; n < r.length; n++) {
      var l = r[n];
      try {
        var a = e,
          u = t,
          o = u;
        e: for (; o !== null; ) {
          switch (o.tag) {
            case 5:
              (Z = o.stateNode), (ze = !1);
              break e;
            case 3:
              (Z = o.stateNode.containerInfo), (ze = !0);
              break e;
            case 4:
              (Z = o.stateNode.containerInfo), (ze = !0);
              break e;
          }
          o = o.return;
        }
        if (Z === null) throw Error(g(160));
        As(a, u, l), (Z = null), (ze = !1);
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
  var r = e.alternate,
    n = e.flags;
  switch (e.tag) {
    case 0:
    case 11:
    case 14:
    case 15:
      if ((Pe(t, e), Me(e), n & 4)) {
        try {
          Pr(3, e, e.return), sl(3, e);
        } catch (k) {
          $(e, e.return, k);
        }
        try {
          Pr(5, e, e.return);
        } catch (k) {
          $(e, e.return, k);
        }
      }
      break;
    case 1:
      Pe(t, e), Me(e), n & 512 && r !== null && Bt(r, r.return);
      break;
    case 5:
      if (
        (Pe(t, e),
        Me(e),
        n & 512 && r !== null && Bt(r, r.return),
        e.flags & 32)
      ) {
        var l = e.stateNode;
        try {
          Tr(l, '');
        } catch (k) {
          $(e, e.return, k);
        }
      }
      if (n & 4 && ((l = e.stateNode), l != null)) {
        var a = e.memoizedProps,
          u = r !== null ? r.memoizedProps : a,
          o = e.type,
          i = e.updateQueue;
        if (((e.updateQueue = null), i !== null))
          try {
            o === 'input' && a.type === 'radio' && a.name != null && ii(l, a),
              na(o, u);
            var c = na(o, a);
            for (u = 0; u < i.length; u += 2) {
              var h = i[u],
                m = i[u + 1];
              h === 'style'
                ? pi(l, m)
                : h === 'dangerouslySetInnerHTML'
                  ? fi(l, m)
                  : h === 'children'
                    ? Tr(l, m)
                    : Ba(l, h, m, c);
            }
            switch (o) {
              case 'input':
                Zl(l, a);
                break;
              case 'textarea':
                si(l, a);
                break;
              case 'select':
                var p = l._wrapperState.wasMultiple;
                l._wrapperState.wasMultiple = !!a.multiple;
                var y = a.value;
                y != null
                  ? Ht(l, !!a.multiple, y, !1)
                  : p !== !!a.multiple &&
                    (a.defaultValue != null
                      ? Ht(l, !!a.multiple, a.defaultValue, !0)
                      : Ht(l, !!a.multiple, a.multiple ? [] : '', !1));
            }
            l[Ar] = a;
          } catch (k) {
            $(e, e.return, k);
          }
      }
      break;
    case 6:
      if ((Pe(t, e), Me(e), n & 4)) {
        if (e.stateNode === null) throw Error(g(162));
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
        (Pe(t, e), Me(e), n & 4 && r !== null && r.memoizedState.isDehydrated)
      )
        try {
          Fr(t.containerInfo);
        } catch (k) {
          $(e, e.return, k);
        }
      break;
    case 4:
      Pe(t, e), Me(e);
      break;
    case 13:
      Pe(t, e),
        Me(e),
        (l = e.child),
        l.flags & 8192 &&
          ((a = l.memoizedState !== null),
          (l.stateNode.isHidden = a),
          !a ||
            (l.alternate !== null && l.alternate.memoizedState !== null) ||
            (Su = H())),
        n & 4 && Oo(e);
      break;
    case 22:
      if (
        ((h = r !== null && r.memoizedState !== null),
        e.mode & 1 ? ((ne = (c = ne) || h), Pe(t, e), (ne = c)) : Pe(t, e),
        Me(e),
        n & 8192)
      ) {
        if (
          ((c = e.memoizedState !== null),
          (e.stateNode.isHidden = c) && !h && e.mode & 1)
        )
          for (w = e, h = e.child; h !== null; ) {
            for (m = w = h; w !== null; ) {
              switch (((p = w), (y = p.child), p.tag)) {
                case 0:
                case 11:
                case 14:
                case 15:
                  Pr(4, p, p.return);
                  break;
                case 1:
                  Bt(p, p.return);
                  var b = p.stateNode;
                  if (typeof b.componentWillUnmount == 'function') {
                    (n = p), (r = p.return);
                    try {
                      (t = n),
                        (b.props = t.memoizedProps),
                        (b.state = t.memoizedState),
                        b.componentWillUnmount();
                    } catch (k) {
                      $(n, r, k);
                    }
                  }
                  break;
                case 5:
                  Bt(p, p.return);
                  break;
                case 22:
                  if (p.memoizedState !== null) {
                    Fo(m);
                    continue;
                  }
              }
              y !== null ? ((y.return = p), (w = y)) : Fo(m);
            }
            h = h.sibling;
          }
        e: for (h = null, m = e; ; ) {
          if (m.tag === 5) {
            if (h === null) {
              h = m;
              try {
                (l = m.stateNode),
                  c
                    ? ((a = l.style),
                      typeof a.setProperty == 'function'
                        ? a.setProperty('display', 'none', 'important')
                        : (a.display = 'none'))
                    : ((o = m.stateNode),
                      (i = m.memoizedProps.style),
                      (u =
                        i != null && i.hasOwnProperty('display')
                          ? i.display
                          : null),
                      (o.style.display = di('display', u)));
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
      Pe(t, e), Me(e), n & 4 && Oo(e);
      break;
    case 21:
      break;
    default:
      Pe(t, e), Me(e);
  }
}
function Me(e) {
  var t = e.flags;
  if (t & 2) {
    try {
      e: {
        for (var r = e.return; r !== null; ) {
          if (Us(r)) {
            var n = r;
            break e;
          }
          r = r.return;
        }
        throw Error(g(160));
      }
      switch (n.tag) {
        case 5:
          var l = n.stateNode;
          n.flags & 32 && (Tr(l, ''), (n.flags &= -33));
          var a = Ro(e);
          Ra(e, a, l);
          break;
        case 3:
        case 4:
          var u = n.stateNode.containerInfo,
            o = Ro(e);
          Ta(e, o, u);
          break;
        default:
          throw Error(g(161));
      }
    } catch (i) {
      $(e, e.return, i);
    }
    e.flags &= -3;
  }
  t & 4096 && (e.flags &= -4097);
}
function pd(e, t, r) {
  (w = e), $s(e);
}
function $s(e, t, r) {
  for (var n = (e.mode & 1) !== 0; w !== null; ) {
    var l = w,
      a = l.child;
    if (l.tag === 22 && n) {
      var u = l.memoizedState !== null || hn;
      if (!u) {
        var o = l.alternate,
          i = (o !== null && o.memoizedState !== null) || ne;
        o = hn;
        var c = ne;
        if (((hn = u), (ne = i) && !c))
          for (w = l; w !== null; )
            (u = w),
              (i = u.child),
              u.tag === 22 && u.memoizedState !== null
                ? Io(l)
                : i !== null
                  ? ((i.return = u), (w = i))
                  : Io(l);
        for (; a !== null; ) (w = a), $s(a), (a = a.sibling);
        (w = l), (hn = o), (ne = c);
      }
      Mo(e);
    } else
      l.subtreeFlags & 8772 && a !== null ? ((a.return = l), (w = a)) : Mo(e);
  }
}
function Mo(e) {
  for (; w !== null; ) {
    var t = w;
    if (t.flags & 8772) {
      var r = t.alternate;
      try {
        if (t.flags & 8772)
          switch (t.tag) {
            case 0:
            case 11:
            case 15:
              ne || sl(5, t);
              break;
            case 1:
              var n = t.stateNode;
              if (t.flags & 4 && !ne)
                if (r === null) n.componentDidMount();
                else {
                  var l =
                    t.elementType === t.type
                      ? r.memoizedProps
                      : Ne(t.type, r.memoizedProps);
                  n.componentDidUpdate(
                    l,
                    r.memoizedState,
                    n.__reactInternalSnapshotBeforeUpdate
                  );
                }
              var a = t.updateQueue;
              a !== null && yo(t, a, n);
              break;
            case 3:
              var u = t.updateQueue;
              if (u !== null) {
                if (((r = null), t.child !== null))
                  switch (t.child.tag) {
                    case 5:
                      r = t.child.stateNode;
                      break;
                    case 1:
                      r = t.child.stateNode;
                  }
                yo(t, u, r);
              }
              break;
            case 5:
              var o = t.stateNode;
              if (r === null && t.flags & 4) {
                r = o;
                var i = t.memoizedProps;
                switch (t.type) {
                  case 'button':
                  case 'input':
                  case 'select':
                  case 'textarea':
                    i.autoFocus && r.focus();
                    break;
                  case 'img':
                    i.src && (r.src = i.src);
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
                    m !== null && Fr(m);
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
              throw Error(g(163));
          }
        ne || (t.flags & 512 && La(t));
      } catch (p) {
        $(t, t.return, p);
      }
    }
    if (t === e) {
      w = null;
      break;
    }
    if (((r = t.sibling), r !== null)) {
      (r.return = t.return), (w = r);
      break;
    }
    w = t.return;
  }
}
function Fo(e) {
  for (; w !== null; ) {
    var t = w;
    if (t === e) {
      w = null;
      break;
    }
    var r = t.sibling;
    if (r !== null) {
      (r.return = t.return), (w = r);
      break;
    }
    w = t.return;
  }
}
function Io(e) {
  for (; w !== null; ) {
    var t = w;
    try {
      switch (t.tag) {
        case 0:
        case 11:
        case 15:
          var r = t.return;
          try {
            sl(4, t);
          } catch (i) {
            $(t, r, i);
          }
          break;
        case 1:
          var n = t.stateNode;
          if (typeof n.componentDidMount == 'function') {
            var l = t.return;
            try {
              n.componentDidMount();
            } catch (i) {
              $(t, l, i);
            }
          }
          var a = t.return;
          try {
            La(t);
          } catch (i) {
            $(t, a, i);
          }
          break;
        case 5:
          var u = t.return;
          try {
            La(t);
          } catch (i) {
            $(t, u, i);
          }
      }
    } catch (i) {
      $(t, t.return, i);
    }
    if (t === e) {
      w = null;
      break;
    }
    var o = t.sibling;
    if (o !== null) {
      (o.return = t.return), (w = o);
      break;
    }
    w = t.return;
  }
}
var md = Math.ceil,
  Yn = Ke.ReactCurrentDispatcher,
  ku = Ke.ReactCurrentOwner,
  xe = Ke.ReactCurrentBatchConfig,
  R = 0,
  X = null,
  W = null,
  J = 0,
  me = 0,
  Qt = mt(0),
  K = 0,
  Wr = null,
  Nt = 0,
  cl = 0,
  wu = 0,
  Nr = null,
  se = null,
  Su = 0,
  nr = 1 / 0,
  Ue = null,
  Gn = !1,
  Oa = null,
  it = null,
  gn = !1,
  rt = null,
  Xn = 0,
  zr = 0,
  Ma = null,
  Pn = -1,
  Nn = 0;
function ue() {
  return R & 6 ? H() : Pn !== -1 ? Pn : (Pn = H());
}
function st(e) {
  return e.mode & 1
    ? R & 2 && J !== 0
      ? J & -J
      : Xf.transition !== null
        ? (Nn === 0 && (Nn = _i()), Nn)
        : ((e = O),
          e !== 0 ||
            ((e = window.event), (e = e === void 0 ? 16 : Ri(e.type))),
          e)
    : 1;
}
function Re(e, t, r, n) {
  if (50 < zr) throw ((zr = 0), (Ma = null), Error(g(185)));
  Kr(e, r, n),
    (!(R & 2) || e !== X) &&
      (e === X && (!(R & 2) && (cl |= r), K === 4 && Je(e, J)),
      pe(e, n),
      r === 1 && R === 0 && !(t.mode & 1) && ((nr = H() + 500), ul && ht()));
}
function pe(e, t) {
  var r = e.callbackNode;
  Gc(e, t);
  var n = Mn(e, e === X ? J : 0);
  if (n === 0)
    r !== null && Qu(r), (e.callbackNode = null), (e.callbackPriority = 0);
  else if (((t = n & -n), e.callbackPriority !== t)) {
    if ((r != null && Qu(r), t === 1))
      e.tag === 0 ? Gf(Do.bind(null, e)) : Xi(Do.bind(null, e)),
        Wf(function () {
          !(R & 6) && ht();
        }),
        (r = null);
    else {
      switch (Ci(n)) {
        case 1:
          r = Ka;
          break;
        case 4:
          r = xi;
          break;
        case 16:
          r = On;
          break;
        case 536870912:
          r = Ei;
          break;
        default:
          r = On;
      }
      r = Gs(r, Bs.bind(null, e));
    }
    (e.callbackPriority = t), (e.callbackNode = r);
  }
}
function Bs(e, t) {
  if (((Pn = -1), (Nn = 0), R & 6)) throw Error(g(327));
  var r = e.callbackNode;
  if (Gt() && e.callbackNode !== r) return null;
  var n = Mn(e, e === X ? J : 0);
  if (n === 0) return null;
  if (n & 30 || n & e.expiredLanes || t) t = Zn(e, n);
  else {
    t = n;
    var l = R;
    R |= 2;
    var a = Hs();
    (X !== e || J !== t) && ((Ue = null), (nr = H() + 500), xt(e, t));
    do
      try {
        vd();
        break;
      } catch (o) {
        Qs(e, o);
      }
    while (!0);
    ou(),
      (Yn.current = a),
      (R = l),
      W !== null ? (t = 0) : ((X = null), (J = 0), (t = K));
  }
  if (t !== 0) {
    if (
      (t === 2 && ((l = ia(e)), l !== 0 && ((n = l), (t = Fa(e, l)))), t === 1)
    )
      throw ((r = Wr), xt(e, 0), Je(e, n), pe(e, H()), r);
    if (t === 6) Je(e, n);
    else {
      if (
        ((l = e.current.alternate),
        !(n & 30) &&
          !hd(l) &&
          ((t = Zn(e, n)),
          t === 2 && ((a = ia(e)), a !== 0 && ((n = a), (t = Fa(e, a)))),
          t === 1))
      )
        throw ((r = Wr), xt(e, 0), Je(e, n), pe(e, H()), r);
      switch (((e.finishedWork = l), (e.finishedLanes = n), t)) {
        case 0:
        case 1:
          throw Error(g(345));
        case 2:
          bt(e, se, Ue);
          break;
        case 3:
          if (
            (Je(e, n), (n & 130023424) === n && ((t = Su + 500 - H()), 10 < t))
          ) {
            if (Mn(e, 0) !== 0) break;
            if (((l = e.suspendedLanes), (l & n) !== n)) {
              ue(), (e.pingedLanes |= e.suspendedLanes & l);
              break;
            }
            e.timeoutHandle = ga(bt.bind(null, e, se, Ue), t);
            break;
          }
          bt(e, se, Ue);
          break;
        case 4:
          if ((Je(e, n), (n & 4194240) === n)) break;
          for (t = e.eventTimes, l = -1; 0 < n; ) {
            var u = 31 - Te(n);
            (a = 1 << u), (u = t[u]), u > l && (l = u), (n &= ~a);
          }
          if (
            ((n = l),
            (n = H() - n),
            (n =
              (120 > n
                ? 120
                : 480 > n
                  ? 480
                  : 1080 > n
                    ? 1080
                    : 1920 > n
                      ? 1920
                      : 3e3 > n
                        ? 3e3
                        : 4320 > n
                          ? 4320
                          : 1960 * md(n / 1960)) - n),
            10 < n)
          ) {
            e.timeoutHandle = ga(bt.bind(null, e, se, Ue), n);
            break;
          }
          bt(e, se, Ue);
          break;
        case 5:
          bt(e, se, Ue);
          break;
        default:
          throw Error(g(329));
      }
    }
  }
  return pe(e, H()), e.callbackNode === r ? Bs.bind(null, e) : null;
}
function Fa(e, t) {
  var r = Nr;
  return (
    e.current.memoizedState.isDehydrated && (xt(e, t).flags |= 256),
    (e = Zn(e, t)),
    e !== 2 && ((t = se), (se = r), t !== null && Ia(t)),
    e
  );
}
function Ia(e) {
  se === null ? (se = e) : se.push.apply(se, e);
}
function hd(e) {
  for (var t = e; ; ) {
    if (t.flags & 16384) {
      var r = t.updateQueue;
      if (r !== null && ((r = r.stores), r !== null))
        for (var n = 0; n < r.length; n++) {
          var l = r[n],
            a = l.getSnapshot;
          l = l.value;
          try {
            if (!Oe(a(), l)) return !1;
          } catch {
            return !1;
          }
        }
    }
    if (((r = t.child), t.subtreeFlags & 16384 && r !== null))
      (r.return = t), (t = r);
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
function Je(e, t) {
  for (
    t &= ~wu,
      t &= ~cl,
      e.suspendedLanes |= t,
      e.pingedLanes &= ~t,
      e = e.expirationTimes;
    0 < t;

  ) {
    var r = 31 - Te(t),
      n = 1 << r;
    (e[r] = -1), (t &= ~n);
  }
}
function Do(e) {
  if (R & 6) throw Error(g(327));
  Gt();
  var t = Mn(e, 0);
  if (!(t & 1)) return pe(e, H()), null;
  var r = Zn(e, t);
  if (e.tag !== 0 && r === 2) {
    var n = ia(e);
    n !== 0 && ((t = n), (r = Fa(e, n)));
  }
  if (r === 1) throw ((r = Wr), xt(e, 0), Je(e, t), pe(e, H()), r);
  if (r === 6) throw Error(g(345));
  return (
    (e.finishedWork = e.current.alternate),
    (e.finishedLanes = t),
    bt(e, se, Ue),
    pe(e, H()),
    null
  );
}
function xu(e, t) {
  var r = R;
  R |= 1;
  try {
    return e(t);
  } finally {
    (R = r), R === 0 && ((nr = H() + 500), ul && ht());
  }
}
function zt(e) {
  rt !== null && rt.tag === 0 && !(R & 6) && Gt();
  var t = R;
  R |= 1;
  var r = xe.transition,
    n = O;
  try {
    if (((xe.transition = null), (O = 1), e)) return e();
  } finally {
    (O = n), (xe.transition = r), (R = t), !(R & 6) && ht();
  }
}
function Eu() {
  (me = Qt.current), I(Qt);
}
function xt(e, t) {
  (e.finishedWork = null), (e.finishedLanes = 0);
  var r = e.timeoutHandle;
  if ((r !== -1 && ((e.timeoutHandle = -1), Hf(r)), W !== null))
    for (r = W.return; r !== null; ) {
      var n = r;
      switch ((lu(n), n.tag)) {
        case 1:
          (n = n.type.childContextTypes), n != null && Un();
          break;
        case 3:
          tr(), I(fe), I(le), pu();
          break;
        case 5:
          du(n);
          break;
        case 4:
          tr();
          break;
        case 13:
          I(U);
          break;
        case 19:
          I(U);
          break;
        case 10:
          iu(n.type._context);
          break;
        case 22:
        case 23:
          Eu();
      }
      r = r.return;
    }
  if (
    ((X = e),
    (W = e = ct(e.current, null)),
    (J = me = t),
    (K = 0),
    (Wr = null),
    (wu = cl = Nt = 0),
    (se = Nr = null),
    wt !== null)
  ) {
    for (t = 0; t < wt.length; t++)
      if (((r = wt[t]), (n = r.interleaved), n !== null)) {
        r.interleaved = null;
        var l = n.next,
          a = r.pending;
        if (a !== null) {
          var u = a.next;
          (a.next = l), (n.next = u);
        }
        r.pending = n;
      }
    wt = null;
  }
  return e;
}
function Qs(e, t) {
  do {
    var r = W;
    try {
      if ((ou(), (En.current = Kn), qn)) {
        for (var n = A.memoizedState; n !== null; ) {
          var l = n.queue;
          l !== null && (l.pending = null), (n = n.next);
        }
        qn = !1;
      }
      if (
        ((Pt = 0),
        (G = q = A = null),
        (Cr = !1),
        (Br = 0),
        (ku.current = null),
        r === null || r.return === null)
      ) {
        (K = 1), (Wr = t), (W = null);
        break;
      }
      e: {
        var a = e,
          u = r.return,
          o = r,
          i = t;
        if (
          ((t = J),
          (o.flags |= 32768),
          i !== null && typeof i == 'object' && typeof i.then == 'function')
        ) {
          var c = i,
            h = o,
            m = h.tag;
          if (!(h.mode & 1) && (m === 0 || m === 11 || m === 15)) {
            var p = h.alternate;
            p
              ? ((h.updateQueue = p.updateQueue),
                (h.memoizedState = p.memoizedState),
                (h.lanes = p.lanes))
              : ((h.updateQueue = null), (h.memoizedState = null));
          }
          var y = Eo(u);
          if (y !== null) {
            (y.flags &= -257),
              _o(y, u, o, a, t),
              y.mode & 1 && xo(a, c, t),
              (t = y),
              (i = c);
            var b = t.updateQueue;
            if (b === null) {
              var k = new Set();
              k.add(i), (t.updateQueue = k);
            } else b.add(i);
            break e;
          } else {
            if (!(t & 1)) {
              xo(a, c, t), _u();
              break e;
            }
            i = Error(g(426));
          }
        } else if (j && o.mode & 1) {
          var D = Eo(u);
          if (D !== null) {
            !(D.flags & 65536) && (D.flags |= 256),
              _o(D, u, o, a, t),
              au(rr(i, o));
            break e;
          }
        }
        (a = i = rr(i, o)),
          K !== 4 && (K = 2),
          Nr === null ? (Nr = [a]) : Nr.push(a),
          (a = u);
        do {
          switch (a.tag) {
            case 3:
              (a.flags |= 65536), (t &= -t), (a.lanes |= t);
              var f = Cs(a, i, t);
              vo(a, f);
              break e;
            case 1:
              o = i;
              var s = a.type,
                d = a.stateNode;
              if (
                !(a.flags & 128) &&
                (typeof s.getDerivedStateFromError == 'function' ||
                  (d !== null &&
                    typeof d.componentDidCatch == 'function' &&
                    (it === null || !it.has(d))))
              ) {
                (a.flags |= 65536), (t &= -t), (a.lanes |= t);
                var v = Ps(a, o, t);
                vo(a, v);
                break e;
              }
          }
          a = a.return;
        } while (a !== null);
      }
      qs(r);
    } catch (x) {
      (t = x), W === r && r !== null && (W = r = r.return);
      continue;
    }
    break;
  } while (!0);
}
function Hs() {
  var e = Yn.current;
  return (Yn.current = Kn), e === null ? Kn : e;
}
function _u() {
  (K === 0 || K === 3 || K === 2) && (K = 4),
    X === null || (!(Nt & 268435455) && !(cl & 268435455)) || Je(X, J);
}
function Zn(e, t) {
  var r = R;
  R |= 2;
  var n = Hs();
  (X !== e || J !== t) && ((Ue = null), xt(e, t));
  do
    try {
      gd();
      break;
    } catch (l) {
      Qs(e, l);
    }
  while (!0);
  if ((ou(), (R = r), (Yn.current = n), W !== null)) throw Error(g(261));
  return (X = null), (J = 0), K;
}
function gd() {
  for (; W !== null; ) Ws(W);
}
function vd() {
  for (; W !== null && !Vc(); ) Ws(W);
}
function Ws(e) {
  var t = Ys(e.alternate, e, me);
  (e.memoizedProps = e.pendingProps),
    t === null ? qs(e) : (W = t),
    (ku.current = null);
}
function qs(e) {
  var t = e;
  do {
    var r = t.alternate;
    if (((e = t.return), t.flags & 32768)) {
      if (((r = cd(r, t)), r !== null)) {
        (r.flags &= 32767), (W = r);
        return;
      }
      if (e !== null)
        (e.flags |= 32768), (e.subtreeFlags = 0), (e.deletions = null);
      else {
        (K = 6), (W = null);
        return;
      }
    } else if (((r = sd(r, t, me)), r !== null)) {
      W = r;
      return;
    }
    if (((t = t.sibling), t !== null)) {
      W = t;
      return;
    }
    W = t = e;
  } while (t !== null);
  K === 0 && (K = 5);
}
function bt(e, t, r) {
  var n = O,
    l = xe.transition;
  try {
    (xe.transition = null), (O = 1), yd(e, t, r, n);
  } finally {
    (xe.transition = l), (O = n);
  }
  return null;
}
function yd(e, t, r, n) {
  do Gt();
  while (rt !== null);
  if (R & 6) throw Error(g(327));
  r = e.finishedWork;
  var l = e.finishedLanes;
  if (r === null) return null;
  if (((e.finishedWork = null), (e.finishedLanes = 0), r === e.current))
    throw Error(g(177));
  (e.callbackNode = null), (e.callbackPriority = 0);
  var a = r.lanes | r.childLanes;
  if (
    (Xc(e, a),
    e === X && ((W = X = null), (J = 0)),
    (!(r.subtreeFlags & 2064) && !(r.flags & 2064)) ||
      gn ||
      ((gn = !0),
      Gs(On, function () {
        return Gt(), null;
      })),
    (a = (r.flags & 15990) !== 0),
    r.subtreeFlags & 15990 || a)
  ) {
    (a = xe.transition), (xe.transition = null);
    var u = O;
    O = 1;
    var o = R;
    (R |= 4),
      (ku.current = null),
      dd(e, r),
      Vs(r, e),
      jf(ma),
      (Fn = !!pa),
      (ma = pa = null),
      (e.current = r),
      pd(r),
      $c(),
      (R = o),
      (O = u),
      (xe.transition = a);
  } else e.current = r;
  if (
    (gn && ((gn = !1), (rt = e), (Xn = l)),
    (a = e.pendingLanes),
    a === 0 && (it = null),
    Hc(r.stateNode),
    pe(e, H()),
    t !== null)
  )
    for (n = e.onRecoverableError, r = 0; r < t.length; r++)
      (l = t[r]), n(l.value, { componentStack: l.stack, digest: l.digest });
  if (Gn) throw ((Gn = !1), (e = Oa), (Oa = null), e);
  return (
    Xn & 1 && e.tag !== 0 && Gt(),
    (a = e.pendingLanes),
    a & 1 ? (e === Ma ? zr++ : ((zr = 0), (Ma = e))) : (zr = 0),
    ht(),
    null
  );
}
function Gt() {
  if (rt !== null) {
    var e = Ci(Xn),
      t = xe.transition,
      r = O;
    try {
      if (((xe.transition = null), (O = 16 > e ? 16 : e), rt === null))
        var n = !1;
      else {
        if (((e = rt), (rt = null), (Xn = 0), R & 6)) throw Error(g(331));
        var l = R;
        for (R |= 4, w = e.current; w !== null; ) {
          var a = w,
            u = a.child;
          if (w.flags & 16) {
            var o = a.deletions;
            if (o !== null) {
              for (var i = 0; i < o.length; i++) {
                var c = o[i];
                for (w = c; w !== null; ) {
                  var h = w;
                  switch (h.tag) {
                    case 0:
                    case 11:
                    case 15:
                      Pr(8, h, a);
                  }
                  var m = h.child;
                  if (m !== null) (m.return = h), (w = m);
                  else
                    for (; w !== null; ) {
                      h = w;
                      var p = h.sibling,
                        y = h.return;
                      if ((js(h), h === c)) {
                        w = null;
                        break;
                      }
                      if (p !== null) {
                        (p.return = y), (w = p);
                        break;
                      }
                      w = y;
                    }
                }
              }
              var b = a.alternate;
              if (b !== null) {
                var k = b.child;
                if (k !== null) {
                  b.child = null;
                  do {
                    var D = k.sibling;
                    (k.sibling = null), (k = D);
                  } while (k !== null);
                }
              }
              w = a;
            }
          }
          if (a.subtreeFlags & 2064 && u !== null) (u.return = a), (w = u);
          else
            e: for (; w !== null; ) {
              if (((a = w), a.flags & 2048))
                switch (a.tag) {
                  case 0:
                  case 11:
                  case 15:
                    Pr(9, a, a.return);
                }
              var f = a.sibling;
              if (f !== null) {
                (f.return = a.return), (w = f);
                break e;
              }
              w = a.return;
            }
        }
        var s = e.current;
        for (w = s; w !== null; ) {
          u = w;
          var d = u.child;
          if (u.subtreeFlags & 2064 && d !== null) (d.return = u), (w = d);
          else
            e: for (u = s; w !== null; ) {
              if (((o = w), o.flags & 2048))
                try {
                  switch (o.tag) {
                    case 0:
                    case 11:
                    case 15:
                      sl(9, o);
                  }
                } catch (x) {
                  $(o, o.return, x);
                }
              if (o === u) {
                w = null;
                break e;
              }
              var v = o.sibling;
              if (v !== null) {
                (v.return = o.return), (w = v);
                break e;
              }
              w = o.return;
            }
        }
        if (
          ((R = l), ht(), De && typeof De.onPostCommitFiberRoot == 'function')
        )
          try {
            De.onPostCommitFiberRoot(tl, e);
          } catch {}
        n = !0;
      }
      return n;
    } finally {
      (O = r), (xe.transition = t);
    }
  }
  return !1;
}
function jo(e, t, r) {
  (t = rr(r, t)),
    (t = Cs(e, t, 1)),
    (e = ot(e, t, 1)),
    (t = ue()),
    e !== null && (Kr(e, 1, t), pe(e, t));
}
function $(e, t, r) {
  if (e.tag === 3) jo(e, e, r);
  else
    for (; t !== null; ) {
      if (t.tag === 3) {
        jo(t, e, r);
        break;
      } else if (t.tag === 1) {
        var n = t.stateNode;
        if (
          typeof t.type.getDerivedStateFromError == 'function' ||
          (typeof n.componentDidCatch == 'function' &&
            (it === null || !it.has(n)))
        ) {
          (e = rr(r, e)),
            (e = Ps(t, e, 1)),
            (t = ot(t, e, 1)),
            (e = ue()),
            t !== null && (Kr(t, 1, e), pe(t, e));
          break;
        }
      }
      t = t.return;
    }
}
function bd(e, t, r) {
  var n = e.pingCache;
  n !== null && n.delete(t),
    (t = ue()),
    (e.pingedLanes |= e.suspendedLanes & r),
    X === e &&
      (J & r) === r &&
      (K === 4 || (K === 3 && (J & 130023424) === J && 500 > H() - Su)
        ? xt(e, 0)
        : (wu |= r)),
    pe(e, t);
}
function Ks(e, t) {
  t === 0 &&
    (e.mode & 1
      ? ((t = an), (an <<= 1), !(an & 130023424) && (an = 4194304))
      : (t = 1));
  var r = ue();
  (e = We(e, t)), e !== null && (Kr(e, t, r), pe(e, r));
}
function kd(e) {
  var t = e.memoizedState,
    r = 0;
  t !== null && (r = t.retryLane), Ks(e, r);
}
function wd(e, t) {
  var r = 0;
  switch (e.tag) {
    case 13:
      var n = e.stateNode,
        l = e.memoizedState;
      l !== null && (r = l.retryLane);
      break;
    case 19:
      n = e.stateNode;
      break;
    default:
      throw Error(g(314));
  }
  n !== null && n.delete(t), Ks(e, r);
}
var Ys;
Ys = function (e, t, r) {
  if (e !== null)
    if (e.memoizedProps !== t.pendingProps || fe.current) ce = !0;
    else {
      if (!(e.lanes & r) && !(t.flags & 128)) return (ce = !1), id(e, t, r);
      ce = !!(e.flags & 131072);
    }
  else (ce = !1), j && t.flags & 1048576 && Zi(t, $n, t.index);
  switch (((t.lanes = 0), t.tag)) {
    case 2:
      var n = t.type;
      Cn(e, t), (e = t.pendingProps);
      var l = Zt(t, le.current);
      Yt(t, r), (l = hu(null, t, n, e, l, r));
      var a = gu();
      return (
        (t.flags |= 1),
        typeof l == 'object' &&
        l !== null &&
        typeof l.render == 'function' &&
        l.$$typeof === void 0
          ? ((t.tag = 1),
            (t.memoizedState = null),
            (t.updateQueue = null),
            de(n) ? ((a = !0), An(t)) : (a = !1),
            (t.memoizedState =
              l.state !== null && l.state !== void 0 ? l.state : null),
            cu(t),
            (l.updater = il),
            (t.stateNode = l),
            (l._reactInternals = t),
            xa(t, n, e, r),
            (t = Ca(null, t, n, !0, a, r)))
          : ((t.tag = 0), j && a && nu(t), ae(null, t, l, r), (t = t.child)),
        t
      );
    case 16:
      n = t.elementType;
      e: {
        switch (
          (Cn(e, t),
          (e = t.pendingProps),
          (l = n._init),
          (n = l(n._payload)),
          (t.type = n),
          (l = t.tag = xd(n)),
          (e = Ne(n, e)),
          l)
        ) {
          case 0:
            t = _a(null, t, n, e, r);
            break e;
          case 1:
            t = No(null, t, n, e, r);
            break e;
          case 11:
            t = Co(null, t, n, e, r);
            break e;
          case 14:
            t = Po(null, t, n, Ne(n.type, e), r);
            break e;
        }
        throw Error(g(306, n, ''));
      }
      return t;
    case 0:
      return (
        (n = t.type),
        (l = t.pendingProps),
        (l = t.elementType === n ? l : Ne(n, l)),
        _a(e, t, n, l, r)
      );
    case 1:
      return (
        (n = t.type),
        (l = t.pendingProps),
        (l = t.elementType === n ? l : Ne(n, l)),
        No(e, t, n, l, r)
      );
    case 3:
      e: {
        if ((Ts(t), e === null)) throw Error(g(387));
        (n = t.pendingProps),
          (a = t.memoizedState),
          (l = a.element),
          ls(e, t),
          Hn(t, n, null, r);
        var u = t.memoizedState;
        if (((n = u.element), a.isDehydrated))
          if (
            ((a = {
              element: n,
              isDehydrated: !1,
              cache: u.cache,
              pendingSuspenseBoundaries: u.pendingSuspenseBoundaries,
              transitions: u.transitions,
            }),
            (t.updateQueue.baseState = a),
            (t.memoizedState = a),
            t.flags & 256)
          ) {
            (l = rr(Error(g(423)), t)), (t = zo(e, t, n, r, l));
            break e;
          } else if (n !== l) {
            (l = rr(Error(g(424)), t)), (t = zo(e, t, n, r, l));
            break e;
          } else
            for (
              he = ut(t.stateNode.containerInfo.firstChild),
                ge = t,
                j = !0,
                Le = null,
                r = rs(t, null, n, r),
                t.child = r;
              r;

            )
              (r.flags = (r.flags & -3) | 4096), (r = r.sibling);
        else {
          if ((Jt(), n === l)) {
            t = qe(e, t, r);
            break e;
          }
          ae(e, t, n, r);
        }
        t = t.child;
      }
      return t;
    case 5:
      return (
        as(t),
        e === null && ka(t),
        (n = t.type),
        (l = t.pendingProps),
        (a = e !== null ? e.memoizedProps : null),
        (u = l.children),
        ha(n, l) ? (u = null) : a !== null && ha(n, a) && (t.flags |= 32),
        Ls(e, t),
        ae(e, t, u, r),
        t.child
      );
    case 6:
      return e === null && ka(t), null;
    case 13:
      return Rs(e, t, r);
    case 4:
      return (
        fu(t, t.stateNode.containerInfo),
        (n = t.pendingProps),
        e === null ? (t.child = er(t, null, n, r)) : ae(e, t, n, r),
        t.child
      );
    case 11:
      return (
        (n = t.type),
        (l = t.pendingProps),
        (l = t.elementType === n ? l : Ne(n, l)),
        Co(e, t, n, l, r)
      );
    case 7:
      return ae(e, t, t.pendingProps, r), t.child;
    case 8:
      return ae(e, t, t.pendingProps.children, r), t.child;
    case 12:
      return ae(e, t, t.pendingProps.children, r), t.child;
    case 10:
      e: {
        if (
          ((n = t.type._context),
          (l = t.pendingProps),
          (a = t.memoizedProps),
          (u = l.value),
          M(Bn, n._currentValue),
          (n._currentValue = u),
          a !== null)
        )
          if (Oe(a.value, u)) {
            if (a.children === l.children && !fe.current) {
              t = qe(e, t, r);
              break e;
            }
          } else
            for (a = t.child, a !== null && (a.return = t); a !== null; ) {
              var o = a.dependencies;
              if (o !== null) {
                u = a.child;
                for (var i = o.firstContext; i !== null; ) {
                  if (i.context === n) {
                    if (a.tag === 1) {
                      (i = Be(-1, r & -r)), (i.tag = 2);
                      var c = a.updateQueue;
                      if (c !== null) {
                        c = c.shared;
                        var h = c.pending;
                        h === null
                          ? (i.next = i)
                          : ((i.next = h.next), (h.next = i)),
                          (c.pending = i);
                      }
                    }
                    (a.lanes |= r),
                      (i = a.alternate),
                      i !== null && (i.lanes |= r),
                      wa(a.return, r, t),
                      (o.lanes |= r);
                    break;
                  }
                  i = i.next;
                }
              } else if (a.tag === 10) u = a.type === t.type ? null : a.child;
              else if (a.tag === 18) {
                if (((u = a.return), u === null)) throw Error(g(341));
                (u.lanes |= r),
                  (o = u.alternate),
                  o !== null && (o.lanes |= r),
                  wa(u, r, t),
                  (u = a.sibling);
              } else u = a.child;
              if (u !== null) u.return = a;
              else
                for (u = a; u !== null; ) {
                  if (u === t) {
                    u = null;
                    break;
                  }
                  if (((a = u.sibling), a !== null)) {
                    (a.return = u.return), (u = a);
                    break;
                  }
                  u = u.return;
                }
              a = u;
            }
        ae(e, t, l.children, r), (t = t.child);
      }
      return t;
    case 9:
      return (
        (l = t.type),
        (n = t.pendingProps.children),
        Yt(t, r),
        (l = Ee(l)),
        (n = n(l)),
        (t.flags |= 1),
        ae(e, t, n, r),
        t.child
      );
    case 14:
      return (
        (n = t.type),
        (l = Ne(n, t.pendingProps)),
        (l = Ne(n.type, l)),
        Po(e, t, n, l, r)
      );
    case 15:
      return Ns(e, t, t.type, t.pendingProps, r);
    case 17:
      return (
        (n = t.type),
        (l = t.pendingProps),
        (l = t.elementType === n ? l : Ne(n, l)),
        Cn(e, t),
        (t.tag = 1),
        de(n) ? ((e = !0), An(t)) : (e = !1),
        Yt(t, r),
        _s(t, n, l),
        xa(t, n, l, r),
        Ca(null, t, n, !0, e, r)
      );
    case 19:
      return Os(e, t, r);
    case 22:
      return zs(e, t, r);
  }
  throw Error(g(156, t.tag));
};
function Gs(e, t) {
  return Si(e, t);
}
function Sd(e, t, r, n) {
  (this.tag = e),
    (this.key = r),
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
    (this.mode = n),
    (this.subtreeFlags = this.flags = 0),
    (this.deletions = null),
    (this.childLanes = this.lanes = 0),
    (this.alternate = null);
}
function Se(e, t, r, n) {
  return new Sd(e, t, r, n);
}
function Cu(e) {
  return (e = e.prototype), !(!e || !e.isReactComponent);
}
function xd(e) {
  if (typeof e == 'function') return Cu(e) ? 1 : 0;
  if (e != null) {
    if (((e = e.$$typeof), e === Ha)) return 11;
    if (e === Wa) return 14;
  }
  return 2;
}
function ct(e, t) {
  var r = e.alternate;
  return (
    r === null
      ? ((r = Se(e.tag, t, e.key, e.mode)),
        (r.elementType = e.elementType),
        (r.type = e.type),
        (r.stateNode = e.stateNode),
        (r.alternate = e),
        (e.alternate = r))
      : ((r.pendingProps = t),
        (r.type = e.type),
        (r.flags = 0),
        (r.subtreeFlags = 0),
        (r.deletions = null)),
    (r.flags = e.flags & 14680064),
    (r.childLanes = e.childLanes),
    (r.lanes = e.lanes),
    (r.child = e.child),
    (r.memoizedProps = e.memoizedProps),
    (r.memoizedState = e.memoizedState),
    (r.updateQueue = e.updateQueue),
    (t = e.dependencies),
    (r.dependencies =
      t === null ? null : { lanes: t.lanes, firstContext: t.firstContext }),
    (r.sibling = e.sibling),
    (r.index = e.index),
    (r.ref = e.ref),
    r
  );
}
function zn(e, t, r, n, l, a) {
  var u = 2;
  if (((n = e), typeof e == 'function')) Cu(e) && (u = 1);
  else if (typeof e == 'string') u = 5;
  else
    e: switch (e) {
      case Mt:
        return Et(r.children, l, a, t);
      case Qa:
        (u = 8), (l |= 8);
        break;
      case ql:
        return (
          (e = Se(12, r, t, l | 2)), (e.elementType = ql), (e.lanes = a), e
        );
      case Kl:
        return (e = Se(13, r, t, l)), (e.elementType = Kl), (e.lanes = a), e;
      case Yl:
        return (e = Se(19, r, t, l)), (e.elementType = Yl), (e.lanes = a), e;
      case ai:
        return fl(r, l, a, t);
      default:
        if (typeof e == 'object' && e !== null)
          switch (e.$$typeof) {
            case ni:
              u = 10;
              break e;
            case li:
              u = 9;
              break e;
            case Ha:
              u = 11;
              break e;
            case Wa:
              u = 14;
              break e;
            case Ge:
              (u = 16), (n = null);
              break e;
          }
        throw Error(g(130, e == null ? e : typeof e, ''));
    }
  return (
    (t = Se(u, r, t, l)), (t.elementType = e), (t.type = n), (t.lanes = a), t
  );
}
function Et(e, t, r, n) {
  return (e = Se(7, e, n, t)), (e.lanes = r), e;
}
function fl(e, t, r, n) {
  return (
    (e = Se(22, e, n, t)),
    (e.elementType = ai),
    (e.lanes = r),
    (e.stateNode = { isHidden: !1 }),
    e
  );
}
function Bl(e, t, r) {
  return (e = Se(6, e, null, t)), (e.lanes = r), e;
}
function Ql(e, t, r) {
  return (
    (t = Se(4, e.children !== null ? e.children : [], e.key, t)),
    (t.lanes = r),
    (t.stateNode = {
      containerInfo: e.containerInfo,
      pendingChildren: null,
      implementation: e.implementation,
    }),
    t
  );
}
function Ed(e, t, r, n, l) {
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
    (this.eventTimes = El(0)),
    (this.expirationTimes = El(-1)),
    (this.entangledLanes =
      this.finishedLanes =
      this.mutableReadLanes =
      this.expiredLanes =
      this.pingedLanes =
      this.suspendedLanes =
      this.pendingLanes =
        0),
    (this.entanglements = El(0)),
    (this.identifierPrefix = n),
    (this.onRecoverableError = l),
    (this.mutableSourceEagerHydrationData = null);
}
function Pu(e, t, r, n, l, a, u, o, i) {
  return (
    (e = new Ed(e, t, r, o, i)),
    t === 1 ? ((t = 1), a === !0 && (t |= 8)) : (t = 0),
    (a = Se(3, null, null, t)),
    (e.current = a),
    (a.stateNode = e),
    (a.memoizedState = {
      element: n,
      isDehydrated: r,
      cache: null,
      transitions: null,
      pendingSuspenseBoundaries: null,
    }),
    cu(a),
    e
  );
}
function _d(e, t, r) {
  var n =
    3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
  return {
    $$typeof: Ot,
    key: n == null ? null : '' + n,
    children: e,
    containerInfo: t,
    implementation: r,
  };
}
function Xs(e) {
  if (!e) return dt;
  e = e._reactInternals;
  e: {
    if (Tt(e) !== e || e.tag !== 1) throw Error(g(170));
    var t = e;
    do {
      switch (t.tag) {
        case 3:
          t = t.stateNode.context;
          break e;
        case 1:
          if (de(t.type)) {
            t = t.stateNode.__reactInternalMemoizedMergedChildContext;
            break e;
          }
      }
      t = t.return;
    } while (t !== null);
    throw Error(g(171));
  }
  if (e.tag === 1) {
    var r = e.type;
    if (de(r)) return Gi(e, r, t);
  }
  return t;
}
function Zs(e, t, r, n, l, a, u, o, i) {
  return (
    (e = Pu(r, n, !0, e, l, a, u, o, i)),
    (e.context = Xs(null)),
    (r = e.current),
    (n = ue()),
    (l = st(r)),
    (a = Be(n, l)),
    (a.callback = t ?? null),
    ot(r, a, l),
    (e.current.lanes = l),
    Kr(e, l, n),
    pe(e, n),
    e
  );
}
function dl(e, t, r, n) {
  var l = t.current,
    a = ue(),
    u = st(l);
  return (
    (r = Xs(r)),
    t.context === null ? (t.context = r) : (t.pendingContext = r),
    (t = Be(a, u)),
    (t.payload = { element: e }),
    (n = n === void 0 ? null : n),
    n !== null && (t.callback = n),
    (e = ot(l, t, u)),
    e !== null && (Re(e, l, u, a), xn(e, l, u)),
    u
  );
}
function Jn(e) {
  if (((e = e.current), !e.child)) return null;
  switch (e.child.tag) {
    case 5:
      return e.child.stateNode;
    default:
      return e.child.stateNode;
  }
}
function Uo(e, t) {
  if (((e = e.memoizedState), e !== null && e.dehydrated !== null)) {
    var r = e.retryLane;
    e.retryLane = r !== 0 && r < t ? r : t;
  }
}
function Nu(e, t) {
  Uo(e, t), (e = e.alternate) && Uo(e, t);
}
function Cd() {
  return null;
}
var Js =
  typeof reportError == 'function'
    ? reportError
    : function (e) {
        console.error(e);
      };
function zu(e) {
  this._internalRoot = e;
}
pl.prototype.render = zu.prototype.render = function (e) {
  var t = this._internalRoot;
  if (t === null) throw Error(g(409));
  dl(e, t, null, null);
};
pl.prototype.unmount = zu.prototype.unmount = function () {
  var e = this._internalRoot;
  if (e !== null) {
    this._internalRoot = null;
    var t = e.containerInfo;
    zt(function () {
      dl(null, e, null, null);
    }),
      (t[He] = null);
  }
};
function pl(e) {
  this._internalRoot = e;
}
pl.prototype.unstable_scheduleHydration = function (e) {
  if (e) {
    var t = zi();
    e = { blockedOn: null, target: e, priority: t };
    for (var r = 0; r < Ze.length && t !== 0 && t < Ze[r].priority; r++);
    Ze.splice(r, 0, e), r === 0 && Ti(e);
  }
};
function Lu(e) {
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
function Ao() {}
function Pd(e, t, r, n, l) {
  if (l) {
    if (typeof n == 'function') {
      var a = n;
      n = function () {
        var c = Jn(u);
        a.call(c);
      };
    }
    var u = Zs(t, n, e, 0, null, !1, !1, '', Ao);
    return (
      (e._reactRootContainer = u),
      (e[He] = u.current),
      jr(e.nodeType === 8 ? e.parentNode : e),
      zt(),
      u
    );
  }
  for (; (l = e.lastChild); ) e.removeChild(l);
  if (typeof n == 'function') {
    var o = n;
    n = function () {
      var c = Jn(i);
      o.call(c);
    };
  }
  var i = Pu(e, 0, !1, null, null, !1, !1, '', Ao);
  return (
    (e._reactRootContainer = i),
    (e[He] = i.current),
    jr(e.nodeType === 8 ? e.parentNode : e),
    zt(function () {
      dl(t, i, r, n);
    }),
    i
  );
}
function hl(e, t, r, n, l) {
  var a = r._reactRootContainer;
  if (a) {
    var u = a;
    if (typeof l == 'function') {
      var o = l;
      l = function () {
        var i = Jn(u);
        o.call(i);
      };
    }
    dl(t, u, e, l);
  } else u = Pd(r, t, e, l, n);
  return Jn(u);
}
Pi = function (e) {
  switch (e.tag) {
    case 3:
      var t = e.stateNode;
      if (t.current.memoizedState.isDehydrated) {
        var r = br(t.pendingLanes);
        r !== 0 &&
          (Ya(t, r | 1), pe(t, H()), !(R & 6) && ((nr = H() + 500), ht()));
      }
      break;
    case 13:
      zt(function () {
        var n = We(e, 1);
        if (n !== null) {
          var l = ue();
          Re(n, e, 1, l);
        }
      }),
        Nu(e, 1);
  }
};
Ga = function (e) {
  if (e.tag === 13) {
    var t = We(e, 134217728);
    if (t !== null) {
      var r = ue();
      Re(t, e, 134217728, r);
    }
    Nu(e, 134217728);
  }
};
Ni = function (e) {
  if (e.tag === 13) {
    var t = st(e),
      r = We(e, t);
    if (r !== null) {
      var n = ue();
      Re(r, e, t, n);
    }
    Nu(e, t);
  }
};
zi = function () {
  return O;
};
Li = function (e, t) {
  var r = O;
  try {
    return (O = e), t();
  } finally {
    O = r;
  }
};
aa = function (e, t, r) {
  switch (t) {
    case 'input':
      if ((Zl(e, r), (t = r.name), r.type === 'radio' && t != null)) {
        for (r = e; r.parentNode; ) r = r.parentNode;
        for (
          r = r.querySelectorAll(
            'input[name=' + JSON.stringify('' + t) + '][type="radio"]'
          ),
            t = 0;
          t < r.length;
          t++
        ) {
          var n = r[t];
          if (n !== e && n.form === e.form) {
            var l = al(n);
            if (!l) throw Error(g(90));
            oi(n), Zl(n, l);
          }
        }
      }
      break;
    case 'textarea':
      si(e, r);
      break;
    case 'select':
      (t = r.value), t != null && Ht(e, !!r.multiple, t, !1);
  }
};
gi = xu;
vi = zt;
var Nd = { usingClientEntryPoint: !1, Events: [Gr, jt, al, mi, hi, xu] },
  gr = {
    findFiberByHostInstance: kt,
    bundleType: 0,
    version: '18.3.1',
    rendererPackageName: 'react-dom',
  },
  zd = {
    bundleType: gr.bundleType,
    version: gr.version,
    rendererPackageName: gr.rendererPackageName,
    rendererConfig: gr.rendererConfig,
    overrideHookState: null,
    overrideHookStateDeletePath: null,
    overrideHookStateRenamePath: null,
    overrideProps: null,
    overridePropsDeletePath: null,
    overridePropsRenamePath: null,
    setErrorHandler: null,
    setSuspenseHandler: null,
    scheduleUpdate: null,
    currentDispatcherRef: Ke.ReactCurrentDispatcher,
    findHostInstanceByFiber: function (e) {
      return (e = ki(e)), e === null ? null : e.stateNode;
    },
    findFiberByHostInstance: gr.findFiberByHostInstance || Cd,
    findHostInstancesForRefresh: null,
    scheduleRefresh: null,
    scheduleRoot: null,
    setRefreshHandler: null,
    getCurrentFiber: null,
    reconcilerVersion: '18.3.1-next-f1338f8080-20240426',
  };
if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < 'u') {
  var vn = __REACT_DEVTOOLS_GLOBAL_HOOK__;
  if (!vn.isDisabled && vn.supportsFiber)
    try {
      (tl = vn.inject(zd)), (De = vn);
    } catch {}
}
ye.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = Nd;
ye.createPortal = function (e, t) {
  var r =
    2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
  if (!Lu(t)) throw Error(g(200));
  return _d(e, t, null, r);
};
ye.createRoot = function (e, t) {
  if (!Lu(e)) throw Error(g(299));
  var r = !1,
    n = '',
    l = Js;
  return (
    t != null &&
      (t.unstable_strictMode === !0 && (r = !0),
      t.identifierPrefix !== void 0 && (n = t.identifierPrefix),
      t.onRecoverableError !== void 0 && (l = t.onRecoverableError)),
    (t = Pu(e, 1, !1, null, null, r, !1, n, l)),
    (e[He] = t.current),
    jr(e.nodeType === 8 ? e.parentNode : e),
    new zu(t)
  );
};
ye.findDOMNode = function (e) {
  if (e == null) return null;
  if (e.nodeType === 1) return e;
  var t = e._reactInternals;
  if (t === void 0)
    throw typeof e.render == 'function'
      ? Error(g(188))
      : ((e = Object.keys(e).join(',')), Error(g(268, e)));
  return (e = ki(t)), (e = e === null ? null : e.stateNode), e;
};
ye.flushSync = function (e) {
  return zt(e);
};
ye.hydrate = function (e, t, r) {
  if (!ml(t)) throw Error(g(200));
  return hl(null, e, t, !0, r);
};
ye.hydrateRoot = function (e, t, r) {
  if (!Lu(e)) throw Error(g(405));
  var n = (r != null && r.hydratedSources) || null,
    l = !1,
    a = '',
    u = Js;
  if (
    (r != null &&
      (r.unstable_strictMode === !0 && (l = !0),
      r.identifierPrefix !== void 0 && (a = r.identifierPrefix),
      r.onRecoverableError !== void 0 && (u = r.onRecoverableError)),
    (t = Zs(t, null, e, 1, r ?? null, l, !1, a, u)),
    (e[He] = t.current),
    jr(e),
    n)
  )
    for (e = 0; e < n.length; e++)
      (r = n[e]),
        (l = r._getVersion),
        (l = l(r._source)),
        t.mutableSourceEagerHydrationData == null
          ? (t.mutableSourceEagerHydrationData = [r, l])
          : t.mutableSourceEagerHydrationData.push(r, l);
  return new pl(t);
};
ye.render = function (e, t, r) {
  if (!ml(t)) throw Error(g(200));
  return hl(null, e, t, !1, r);
};
ye.unmountComponentAtNode = function (e) {
  if (!ml(e)) throw Error(g(40));
  return e._reactRootContainer
    ? (zt(function () {
        hl(null, null, e, !1, function () {
          (e._reactRootContainer = null), (e[He] = null);
        });
      }),
      !0)
    : !1;
};
ye.unstable_batchedUpdates = xu;
ye.unstable_renderSubtreeIntoContainer = function (e, t, r, n) {
  if (!ml(r)) throw Error(g(200));
  if (e == null || e._reactInternals === void 0) throw Error(g(38));
  return hl(e, t, r, !1, n);
};
ye.version = '18.3.1-next-f1338f8080-20240426';
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
ec(), (Jo.exports = ye);
var Ld = Jo.exports,
  Vo = Ld;
(Hl.createRoot = Vo.createRoot), (Hl.hydrateRoot = Vo.hydrateRoot);
const Td = () =>
    P.jsx('div', {
      style: { padding: '16px', marginBottom: '24px', textAlign: 'center' },
      children: P.jsx('h1', { children: 'Meraki Integration Control' }),
    }),
  Rd = (e) =>
    e.startsWith('GS')
      ? 'Switches'
      : e.startsWith('GR')
        ? 'Access Points'
        : e.startsWith('MT')
          ? 'Sensors'
          : e.startsWith('MS')
            ? 'Switches'
            : e.startsWith('MV')
              ? 'Cameras'
              : e.startsWith('MX')
                ? 'Routers'
                : e.startsWith('MR')
                  ? 'Access Points'
                  : 'Other',
  Od = ({ deviceType: e, devices: t }) => {
    const r = {
        padding: '12px',
        marginBottom: '12px',
        borderRadius: 'var(--ha-card-border-radius, 4px)',
        backgroundColor: 'var(--secondary-background-color)',
        textAlign: 'center',
      },
      n = t.filter((l) => l.status === 'online').length;
    switch (e) {
      case 'Cameras':
      case 'Switches':
      case 'Access Points':
      case 'Sensors':
        return P.jsxs('div', {
          style: r,
          children: [
            P.jsxs('strong', { children: [n, ' / ', t.length] }),
            ' ',
            e,
            ' Online',
          ],
        });
      case 'Routers':
        const l = t.some((a) => a.status === 'online');
        return P.jsxs('div', {
          style: r,
          children: [
            'Gateway Status: ',
            P.jsx('strong', { children: l ? 'Online' : 'Offline' }),
          ],
        });
      default:
        return null;
    }
  },
  Md = ({ devices: e }) => {
    if (!e || e.length === 0)
      return P.jsx('p', { children: 'No devices found in this network.' });
    const t = e.reduce((r, n) => {
      const l = Rd(n.model);
      return r[l] || (r[l] = []), r[l].push(n), r;
    }, {});
    return P.jsx('div', {
      className: 'device-list',
      style: { display: 'flex', flexDirection: 'column', gap: '16px' },
      children: Object.entries(t).map(([r, n]) =>
        P.jsxs(
          'div',
          {
            className: 'device-group',
            children: [
              P.jsx(Od, { deviceType: r, devices: n }),
              n.map((l) =>
                P.jsxs(
                  'div',
                  {
                    className: 'device-item',
                    style: { marginBottom: '8px' },
                    children: [
                      P.jsx('p', {
                        style: { margin: 0 },
                        children: P.jsx('strong', {
                          onClick: () =>
                            l.entity_id &&
                            window.dispatchEvent(
                              new CustomEvent('hass-more-info', {
                                bubbles: !0,
                                composed: !0,
                                detail: { entityId: l.entity_id },
                              })
                            ),
                          style: {
                            cursor: l.entity_id ? 'pointer' : 'default',
                            color: l.entity_id
                              ? 'var(--primary-color)'
                              : void 0,
                          },
                          title: l.entity_id || '',
                          children: l.name || 'Unnamed Device',
                        }),
                      }),
                      P.jsxs('p', {
                        style: {
                          margin: 0,
                          fontSize: 'var(--secondary-text-size)',
                        },
                        children: [
                          'Model: ',
                          l.model,
                          ' | Status: ',
                          l.status,
                        ],
                      }),
                      P.jsxs('p', {
                        style: {
                          margin: 0,
                          fontSize: 'var(--secondary-text-size)',
                        },
                        children: [
                          l.lanIp && `IP: ${l.lanIp} | `,
                          l.mac && `MAC: ${l.mac}`,
                        ],
                      }),
                    ],
                  },
                  l.serial
                )
              ),
            ],
          },
          r
        )
      ),
    });
  },
  Fd = ({ data: e, onToggle: t }) => {
    const [r, n] = et.useState(null),
      l = (o) => {
        n(r === o ? null : o);
      },
      { networks: a, devices: u } = e;
    return !a || a.length === 0
      ? P.jsx('p', { children: 'No networks found.' })
      : P.jsx('div', {
          style: { display: 'flex', flexDirection: 'column', gap: '16px' },
          children: a.map((o) => {
            const i = r === o.id;
            return P.jsxs(
              'ha-card',
              {
                children: [
                  P.jsxs('div', {
                    className: 'card-header',
                    onClick: () => l(o.id),
                    style: {
                      display: 'flex',
                      alignItems: 'center',
                      cursor: 'pointer',
                      padding: '16px',
                    },
                    children: [
                      P.jsxs('span', { children: ['[Network] ', o.name] }),
                      P.jsx('ha-icon', {
                        style: { marginLeft: '8px' },
                        icon: i ? 'mdi:chevron-up' : 'mdi:chevron-down',
                      }),
                      P.jsxs('div', {
                        style: {
                          marginLeft: 'auto',
                          display: 'flex',
                          alignItems: 'center',
                        },
                        children: [
                          P.jsx('span', {
                            style: { marginRight: '8px' },
                            children: 'Track in',
                          }),
                          P.jsx('ha-icon', {
                            icon: 'hass:home-assistant',
                            style: {
                              color: 'var(--primary-color)',
                              marginRight: '8px',
                            },
                          }),
                          P.jsx('ha-switch', {
                            checked: o.is_enabled,
                            onchange: (c) => t(o.id, c.target.checked),
                          }),
                        ],
                      }),
                    ],
                  }),
                  i &&
                    o.is_enabled &&
                    P.jsx('div', {
                      className: 'card-content',
                      children: P.jsx(Md, {
                        devices: u.filter((c) => c.networkId === o.id),
                      }),
                    }),
                ],
              },
              o.id
            );
          }),
        });
  },
  Id = () =>
    P.jsx('div', {
      className: 'card-content',
      children: P.jsx('p', {
        children: 'Integration-specific events will be displayed here.',
      }),
    }),
  Dd = ({ hass: e, config_entry_id: t }) => {
    const [r, n] = et.useState(null),
      [l, a] = et.useState(!0),
      [u, o] = et.useState(null);
    et.useEffect(() => {
      if (!e || !e.connection) {
        o('Home Assistant connection object not found.'), a(!1);
        return;
      }
      (async () => {
        try {
          const c = await e.connection.sendMessagePromise({
            type: 'meraki_ha/get_config',
            config_entry_id: t,
          });
          n(c);
        } catch (c) {
          console.error('Error fetching Meraki data:', c),
            o(`Failed to fetch Meraki data: ${c.message || 'Unknown error'}`);
        } finally {
          a(!1);
        }
      })();
    }, [e, t]);
    const i = async (c, h) => {
      if (!r) return;
      const m = h
          ? [...r.enabled_networks, c]
          : r.enabled_networks.filter((y) => y !== c),
        p = r.networks.map((y) => (y.id === c ? { ...y, is_enabled: h } : y));
      n({ ...r, networks: p, enabled_networks: m });
      try {
        await e.connection.sendMessagePromise({
          type: 'meraki_ha/update_enabled_networks',
          config_entry_id: t,
          enabled_networks: m,
        });
      } catch (y) {
        console.error('Error updating enabled networks:', y), n(r);
      }
    };
    return P.jsxs('div', {
      children: [
        P.jsx(Td, {}),
        l && P.jsx('p', { children: 'Loading...' }),
        u && P.jsxs('p', { children: ['Error: ', u] }),
        !l &&
          !u &&
          r &&
          P.jsxs(P.Fragment, {
            children: [
              P.jsx(Fd, { data: r, onToggle: i }),
              P.jsx('ha-card', {
                header: 'Event Log',
                children: P.jsx(Id, {}),
              }),
              P.jsx('div', {
                style: { textAlign: 'center', marginTop: '16px' },
                children: P.jsxs('p', { children: ['Version: ', r.version] }),
              }),
            ],
          }),
      ],
    });
  };
class jd extends HTMLElement {
  connectedCallback() {
    const t = this.attachShadow({ mode: 'open' }),
      r = document.createElement('div');
    (r.id = 'root'), t.appendChild(r);
    const n = this.hass,
      l = this.panel.config.config_entry_id;
    Hl.createRoot(r).render(
      P.jsx(yc.StrictMode, {
        children: P.jsx(Dd, { hass: n, config_entry_id: l }),
      })
    );
  }
}
customElements.get('meraki-panel') ||
  customElements.define('meraki-panel', jd);
