var Cp = Object.defineProperty;
var _p = (Vt, rt, ut) =>
  rt in Vt
    ? Cp(Vt, rt, { enumerable: !0, configurable: !0, writable: !0, value: ut })
    : (Vt[rt] = ut);
var Wt = (Vt, rt, ut) => _p(Vt, typeof rt != 'symbol' ? rt + '' : rt, ut);
(function () {
  'use strict';
  function Vt(e) {
    return e &&
      e.__esModule &&
      Object.prototype.hasOwnProperty.call(e, 'default')
      ? e.default
      : e;
  }
  var rt = { exports: {} },
    ut = {},
    la = { exports: {} },
    F = {};
  /**
   * @license React
   * react.production.min.js
   *
   * Copyright (c) Facebook, Inc. and its affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   */ var br = Symbol.for('react.element'),
    Mc = Symbol.for('react.portal'),
    Dc = Symbol.for('react.fragment'),
    Rc = Symbol.for('react.strict_mode'),
    Ic = Symbol.for('react.profiler'),
    bc = Symbol.for('react.provider'),
    Fc = Symbol.for('react.context'),
    Oc = Symbol.for('react.forward_ref'),
    Uc = Symbol.for('react.suspense'),
    $c = Symbol.for('react.memo'),
    Ac = Symbol.for('react.lazy'),
    ia = Symbol.iterator;
  function Wc(e) {
    return e === null || typeof e != 'object'
      ? null
      : ((e = (ia && e[ia]) || e['@@iterator']),
        typeof e == 'function' ? e : null);
  }
  var sa = {
      isMounted: function () {
        return !1;
      },
      enqueueForceUpdate: function () {},
      enqueueReplaceState: function () {},
      enqueueSetState: function () {},
    },
    aa = Object.assign,
    oa = {};
  function sr(e, t, r) {
    (this.props = e),
      (this.context = t),
      (this.refs = oa),
      (this.updater = r || sa);
  }
  (sr.prototype.isReactComponent = {}),
    (sr.prototype.setState = function (e, t) {
      if (typeof e != 'object' && typeof e != 'function' && e != null)
        throw Error(
          'setState(...): takes an object of state variables to update or a function which returns an object of state variables.'
        );
      this.updater.enqueueSetState(this, e, t, 'setState');
    }),
    (sr.prototype.forceUpdate = function (e) {
      this.updater.enqueueForceUpdate(this, e, 'forceUpdate');
    });
  function ua() {}
  ua.prototype = sr.prototype;
  function Vl(e, t, r) {
    (this.props = e),
      (this.context = t),
      (this.refs = oa),
      (this.updater = r || sa);
  }
  var Bl = (Vl.prototype = new ua());
  (Bl.constructor = Vl), aa(Bl, sr.prototype), (Bl.isPureReactComponent = !0);
  var ca = Array.isArray,
    da = Object.prototype.hasOwnProperty,
    Hl = { current: null },
    fa = { key: !0, ref: !0, __self: !0, __source: !0 };
  function pa(e, t, r) {
    var n,
      l = {},
      i = null,
      a = null;
    if (t != null)
      for (n in (t.ref !== void 0 && (a = t.ref),
      t.key !== void 0 && (i = '' + t.key),
      t))
        da.call(t, n) && !fa.hasOwnProperty(n) && (l[n] = t[n]);
    var u = arguments.length - 2;
    if (u === 1) l.children = r;
    else if (1 < u) {
      for (var o = Array(u), d = 0; d < u; d++) o[d] = arguments[d + 2];
      l.children = o;
    }
    if (e && e.defaultProps)
      for (n in ((u = e.defaultProps), u)) l[n] === void 0 && (l[n] = u[n]);
    return {
      $$typeof: br,
      type: e,
      key: i,
      ref: a,
      props: l,
      _owner: Hl.current,
    };
  }
  function Vc(e, t) {
    return {
      $$typeof: br,
      type: e.type,
      key: t,
      ref: e.ref,
      props: e.props,
      _owner: e._owner,
    };
  }
  function Ql(e) {
    return typeof e == 'object' && e !== null && e.$$typeof === br;
  }
  function Bc(e) {
    var t = { '=': '=0', ':': '=2' };
    return (
      '$' +
      e.replace(/[=:]/g, function (r) {
        return t[r];
      })
    );
  }
  var ma = /\/+/g;
  function Kl(e, t) {
    return typeof e == 'object' && e !== null && e.key != null
      ? Bc('' + e.key)
      : t.toString(36);
  }
  function En(e, t, r, n, l) {
    var i = typeof e;
    (i === 'undefined' || i === 'boolean') && (e = null);
    var a = !1;
    if (e === null) a = !0;
    else
      switch (i) {
        case 'string':
        case 'number':
          a = !0;
          break;
        case 'object':
          switch (e.$$typeof) {
            case br:
            case Mc:
              a = !0;
          }
      }
    if (a)
      return (
        (a = e),
        (l = l(a)),
        (e = n === '' ? '.' + Kl(a, 0) : n),
        ca(l)
          ? ((r = ''),
            e != null && (r = e.replace(ma, '$&/') + '/'),
            En(l, t, r, '', function (d) {
              return d;
            }))
          : l != null &&
            (Ql(l) &&
              (l = Vc(
                l,
                r +
                  (!l.key || (a && a.key === l.key)
                    ? ''
                    : ('' + l.key).replace(ma, '$&/') + '/') +
                  e
              )),
            t.push(l)),
        1
      );
    if (((a = 0), (n = n === '' ? '.' : n + ':'), ca(e)))
      for (var u = 0; u < e.length; u++) {
        i = e[u];
        var o = n + Kl(i, u);
        a += En(i, t, r, o, l);
      }
    else if (((o = Wc(e)), typeof o == 'function'))
      for (e = o.call(e), u = 0; !(i = e.next()).done; )
        (i = i.value), (o = n + Kl(i, u++)), (a += En(i, t, r, o, l));
    else if (i === 'object')
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
    return a;
  }
  function zn(e, t, r) {
    if (e == null) return e;
    var n = [],
      l = 0;
    return (
      En(e, n, '', '', function (i) {
        return t.call(r, i, l++);
      }),
      n
    );
  }
  function Hc(e) {
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
  var ke = { current: null },
    Pn = { transition: null },
    Qc = {
      ReactCurrentDispatcher: ke,
      ReactCurrentBatchConfig: Pn,
      ReactCurrentOwner: Hl,
    };
  function ha() {
    throw Error('act(...) is not supported in production builds of React.');
  }
  (F.Children = {
    map: zn,
    forEach: function (e, t, r) {
      zn(
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
        zn(e, function () {
          t++;
        }),
        t
      );
    },
    toArray: function (e) {
      return (
        zn(e, function (t) {
          return t;
        }) || []
      );
    },
    only: function (e) {
      if (!Ql(e))
        throw Error(
          'React.Children.only expected to receive a single React element child.'
        );
      return e;
    },
  }),
    (F.Component = sr),
    (F.Fragment = Dc),
    (F.Profiler = Ic),
    (F.PureComponent = Vl),
    (F.StrictMode = Rc),
    (F.Suspense = Uc),
    (F.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = Qc),
    (F.act = ha),
    (F.cloneElement = function (e, t, r) {
      if (e == null)
        throw Error(
          'React.cloneElement(...): The argument must be a React element, but you passed ' +
            e +
            '.'
        );
      var n = aa({}, e.props),
        l = e.key,
        i = e.ref,
        a = e._owner;
      if (t != null) {
        if (
          (t.ref !== void 0 && ((i = t.ref), (a = Hl.current)),
          t.key !== void 0 && (l = '' + t.key),
          e.type && e.type.defaultProps)
        )
          var u = e.type.defaultProps;
        for (o in t)
          da.call(t, o) &&
            !fa.hasOwnProperty(o) &&
            (n[o] = t[o] === void 0 && u !== void 0 ? u[o] : t[o]);
      }
      var o = arguments.length - 2;
      if (o === 1) n.children = r;
      else if (1 < o) {
        u = Array(o);
        for (var d = 0; d < o; d++) u[d] = arguments[d + 2];
        n.children = u;
      }
      return {
        $$typeof: br,
        type: e.type,
        key: l,
        ref: i,
        props: n,
        _owner: a,
      };
    }),
    (F.createContext = function (e) {
      return (
        (e = {
          $$typeof: Fc,
          _currentValue: e,
          _currentValue2: e,
          _threadCount: 0,
          Provider: null,
          Consumer: null,
          _defaultValue: null,
          _globalName: null,
        }),
        (e.Provider = { $$typeof: bc, _context: e }),
        (e.Consumer = e)
      );
    }),
    (F.createElement = pa),
    (F.createFactory = function (e) {
      var t = pa.bind(null, e);
      return (t.type = e), t;
    }),
    (F.createRef = function () {
      return { current: null };
    }),
    (F.forwardRef = function (e) {
      return { $$typeof: Oc, render: e };
    }),
    (F.isValidElement = Ql),
    (F.lazy = function (e) {
      return {
        $$typeof: Ac,
        _payload: { _status: -1, _result: e },
        _init: Hc,
      };
    }),
    (F.memo = function (e, t) {
      return { $$typeof: $c, type: e, compare: t === void 0 ? null : t };
    }),
    (F.startTransition = function (e) {
      var t = Pn.transition;
      Pn.transition = {};
      try {
        e();
      } finally {
        Pn.transition = t;
      }
    }),
    (F.unstable_act = ha),
    (F.useCallback = function (e, t) {
      return ke.current.useCallback(e, t);
    }),
    (F.useContext = function (e) {
      return ke.current.useContext(e);
    }),
    (F.useDebugValue = function () {}),
    (F.useDeferredValue = function (e) {
      return ke.current.useDeferredValue(e);
    }),
    (F.useEffect = function (e, t) {
      return ke.current.useEffect(e, t);
    }),
    (F.useId = function () {
      return ke.current.useId();
    }),
    (F.useImperativeHandle = function (e, t, r) {
      return ke.current.useImperativeHandle(e, t, r);
    }),
    (F.useInsertionEffect = function (e, t) {
      return ke.current.useInsertionEffect(e, t);
    }),
    (F.useLayoutEffect = function (e, t) {
      return ke.current.useLayoutEffect(e, t);
    }),
    (F.useMemo = function (e, t) {
      return ke.current.useMemo(e, t);
    }),
    (F.useReducer = function (e, t, r) {
      return ke.current.useReducer(e, t, r);
    }),
    (F.useRef = function (e) {
      return ke.current.useRef(e);
    }),
    (F.useState = function (e) {
      return ke.current.useState(e);
    }),
    (F.useSyncExternalStore = function (e, t, r) {
      return ke.current.useSyncExternalStore(e, t, r);
    }),
    (F.useTransition = function () {
      return ke.current.useTransition();
    }),
    (F.version = '18.3.1'),
    (la.exports = F);
  var A = la.exports;
  const Fe = Vt(A);
  /**
   * @license React
   * react-jsx-runtime.production.min.js
   *
   * Copyright (c) Facebook, Inc. and its affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   */ var Kc = A,
    Yc = Symbol.for('react.element'),
    Gc = Symbol.for('react.fragment'),
    Xc = Object.prototype.hasOwnProperty,
    Zc =
      Kc.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner,
    Jc = { key: !0, ref: !0, __self: !0, __source: !0 };
  function ga(e, t, r) {
    var n,
      l = {},
      i = null,
      a = null;
    r !== void 0 && (i = '' + r),
      t.key !== void 0 && (i = '' + t.key),
      t.ref !== void 0 && (a = t.ref);
    for (n in t) Xc.call(t, n) && !Jc.hasOwnProperty(n) && (l[n] = t[n]);
    if (e && e.defaultProps)
      for (n in ((t = e.defaultProps), t)) l[n] === void 0 && (l[n] = t[n]);
    return {
      $$typeof: Yc,
      type: e,
      key: i,
      ref: a,
      props: l,
      _owner: Zc.current,
    };
  }
  (ut.Fragment = Gc), (ut.jsx = ga), (ut.jsxs = ga), (rt.exports = ut);
  var s = rt.exports,
    Yl = {},
    va = { exports: {} },
    Te = {},
    xa = { exports: {} },
    ya = {};
  /**
   * @license React
   * scheduler.production.min.js
   *
   * Copyright (c) Facebook, Inc. and its affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   */ (function (e) {
    function t(E, D) {
      var I = E.length;
      E.push(D);
      e: for (; 0 < I; ) {
        var U = (I - 1) >>> 1,
          Z = E[U];
        if (0 < l(Z, D)) (E[U] = D), (E[I] = Z), (I = U);
        else break e;
      }
    }
    function r(E) {
      return E.length === 0 ? null : E[0];
    }
    function n(E) {
      if (E.length === 0) return null;
      var D = E[0],
        I = E.pop();
      if (I !== D) {
        E[0] = I;
        e: for (var U = 0, Z = E.length, $t = Z >>> 1; U < $t; ) {
          var oe = 2 * (U + 1) - 1,
            O = E[oe],
            ee = oe + 1,
            et = E[ee];
          if (0 > l(O, I))
            ee < Z && 0 > l(et, O)
              ? ((E[U] = et), (E[ee] = I), (U = ee))
              : ((E[U] = O), (E[oe] = I), (U = oe));
          else if (ee < Z && 0 > l(et, I)) (E[U] = et), (E[ee] = I), (U = ee);
          else break e;
        }
      }
      return D;
    }
    function l(E, D) {
      var I = E.sortIndex - D.sortIndex;
      return I !== 0 ? I : E.id - D.id;
    }
    if (
      typeof performance == 'object' &&
      typeof performance.now == 'function'
    ) {
      var i = performance;
      e.unstable_now = function () {
        return i.now();
      };
    } else {
      var a = Date,
        u = a.now();
      e.unstable_now = function () {
        return a.now() - u;
      };
    }
    var o = [],
      d = [],
      v = 1,
      g = null,
      m = 3,
      h = !1,
      y = !1,
      k = !1,
      M = typeof setTimeout == 'function' ? setTimeout : null,
      f = typeof clearTimeout == 'function' ? clearTimeout : null,
      c = typeof setImmediate < 'u' ? setImmediate : null;
    typeof navigator < 'u' &&
      navigator.scheduling !== void 0 &&
      navigator.scheduling.isInputPending !== void 0 &&
      navigator.scheduling.isInputPending.bind(navigator.scheduling);
    function p(E) {
      for (var D = r(d); D !== null; ) {
        if (D.callback === null) n(d);
        else if (D.startTime <= E)
          n(d), (D.sortIndex = D.expirationTime), t(o, D);
        else break;
        D = r(d);
      }
    }
    function w(E) {
      if (((k = !1), p(E), !y))
        if (r(o) !== null) (y = !0), qe(z);
        else {
          var D = r(d);
          D !== null && ot(w, D.startTime - E);
        }
    }
    function z(E, D) {
      (y = !1), k && ((k = !1), f(P), (P = -1)), (h = !0);
      var I = m;
      try {
        for (
          p(D), g = r(o);
          g !== null && (!(g.expirationTime > D) || (E && !xe()));

        ) {
          var U = g.callback;
          if (typeof U == 'function') {
            (g.callback = null), (m = g.priorityLevel);
            var Z = U(g.expirationTime <= D);
            (D = e.unstable_now()),
              typeof Z == 'function' ? (g.callback = Z) : g === r(o) && n(o),
              p(D);
          } else n(o);
          g = r(o);
        }
        if (g !== null) var $t = !0;
        else {
          var oe = r(d);
          oe !== null && ot(w, oe.startTime - D), ($t = !1);
        }
        return $t;
      } finally {
        (g = null), (m = I), (h = !1);
      }
    }
    var S = !1,
      C = null,
      P = -1,
      W = 5,
      R = -1;
    function xe() {
      return !(e.unstable_now() - R < W);
    }
    function fe() {
      if (C !== null) {
        var E = e.unstable_now();
        R = E;
        var D = !0;
        try {
          D = C(!0, E);
        } finally {
          D ? Le() : ((S = !1), (C = null));
        }
      } else S = !1;
    }
    var Le;
    if (typeof c == 'function')
      Le = function () {
        c(fe);
      };
    else if (typeof MessageChannel < 'u') {
      var ir = new MessageChannel(),
        le = ir.port2;
      (ir.port1.onmessage = fe),
        (Le = function () {
          le.postMessage(null);
        });
    } else
      Le = function () {
        M(fe, 0);
      };
    function qe(E) {
      (C = E), S || ((S = !0), Le());
    }
    function ot(E, D) {
      P = M(function () {
        E(e.unstable_now());
      }, D);
    }
    (e.unstable_IdlePriority = 5),
      (e.unstable_ImmediatePriority = 1),
      (e.unstable_LowPriority = 4),
      (e.unstable_NormalPriority = 3),
      (e.unstable_Profiling = null),
      (e.unstable_UserBlockingPriority = 2),
      (e.unstable_cancelCallback = function (E) {
        E.callback = null;
      }),
      (e.unstable_continueExecution = function () {
        y || h || ((y = !0), qe(z));
      }),
      (e.unstable_forceFrameRate = function (E) {
        0 > E || 125 < E
          ? console.error(
              'forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported'
            )
          : (W = 0 < E ? Math.floor(1e3 / E) : 5);
      }),
      (e.unstable_getCurrentPriorityLevel = function () {
        return m;
      }),
      (e.unstable_getFirstCallbackNode = function () {
        return r(o);
      }),
      (e.unstable_next = function (E) {
        switch (m) {
          case 1:
          case 2:
          case 3:
            var D = 3;
            break;
          default:
            D = m;
        }
        var I = m;
        m = D;
        try {
          return E();
        } finally {
          m = I;
        }
      }),
      (e.unstable_pauseExecution = function () {}),
      (e.unstable_requestPaint = function () {}),
      (e.unstable_runWithPriority = function (E, D) {
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
        var I = m;
        m = E;
        try {
          return D();
        } finally {
          m = I;
        }
      }),
      (e.unstable_scheduleCallback = function (E, D, I) {
        var U = e.unstable_now();
        switch (
          (typeof I == 'object' && I !== null
            ? ((I = I.delay), (I = typeof I == 'number' && 0 < I ? U + I : U))
            : (I = U),
          E)
        ) {
          case 1:
            var Z = -1;
            break;
          case 2:
            Z = 250;
            break;
          case 5:
            Z = 1073741823;
            break;
          case 4:
            Z = 1e4;
            break;
          default:
            Z = 5e3;
        }
        return (
          (Z = I + Z),
          (E = {
            id: v++,
            callback: D,
            priorityLevel: E,
            startTime: I,
            expirationTime: Z,
            sortIndex: -1,
          }),
          I > U
            ? ((E.sortIndex = I),
              t(d, E),
              r(o) === null &&
                E === r(d) &&
                (k ? (f(P), (P = -1)) : (k = !0), ot(w, I - U)))
            : ((E.sortIndex = Z), t(o, E), y || h || ((y = !0), qe(z))),
          E
        );
      }),
      (e.unstable_shouldYield = xe),
      (e.unstable_wrapCallback = function (E) {
        var D = m;
        return function () {
          var I = m;
          m = D;
          try {
            return E.apply(this, arguments);
          } finally {
            m = I;
          }
        };
      });
  })(ya),
    (xa.exports = ya);
  var qc = xa.exports;
  /**
   * @license React
   * react-dom.production.min.js
   *
   * Copyright (c) Facebook, Inc. and its affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   */ var ed = A,
    Me = qc;
  function j(e) {
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
  var wa = new Set(),
    Fr = {};
  function Bt(e, t) {
    ar(e, t), ar(e + 'Capture', t);
  }
  function ar(e, t) {
    for (Fr[e] = t, e = 0; e < t.length; e++) wa.add(t[e]);
  }
  var ct = !(
      typeof window > 'u' ||
      typeof window.document > 'u' ||
      typeof window.document.createElement > 'u'
    ),
    Gl = Object.prototype.hasOwnProperty,
    td =
      /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/,
    ka = {},
    Sa = {};
  function rd(e) {
    return Gl.call(Sa, e)
      ? !0
      : Gl.call(ka, e)
      ? !1
      : td.test(e)
      ? (Sa[e] = !0)
      : ((ka[e] = !0), !1);
  }
  function nd(e, t, r, n) {
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
  function ld(e, t, r, n) {
    if (t === null || typeof t > 'u' || nd(e, t, r, n)) return !0;
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
  function Se(e, t, r, n, l, i, a) {
    (this.acceptsBooleans = t === 2 || t === 3 || t === 4),
      (this.attributeName = n),
      (this.attributeNamespace = l),
      (this.mustUseProperty = r),
      (this.propertyName = e),
      (this.type = t),
      (this.sanitizeURL = i),
      (this.removeEmptyString = a);
  }
  var ue = {};
  'children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style'
    .split(' ')
    .forEach(function (e) {
      ue[e] = new Se(e, 0, !1, e, null, !1, !1);
    }),
    [
      ['acceptCharset', 'accept-charset'],
      ['className', 'class'],
      ['htmlFor', 'for'],
      ['httpEquiv', 'http-equiv'],
    ].forEach(function (e) {
      var t = e[0];
      ue[t] = new Se(t, 1, !1, e[1], null, !1, !1);
    }),
    ['contentEditable', 'draggable', 'spellCheck', 'value'].forEach(
      function (e) {
        ue[e] = new Se(e, 2, !1, e.toLowerCase(), null, !1, !1);
      }
    ),
    [
      'autoReverse',
      'externalResourcesRequired',
      'focusable',
      'preserveAlpha',
    ].forEach(function (e) {
      ue[e] = new Se(e, 2, !1, e, null, !1, !1);
    }),
    'allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope'
      .split(' ')
      .forEach(function (e) {
        ue[e] = new Se(e, 3, !1, e.toLowerCase(), null, !1, !1);
      }),
    ['checked', 'multiple', 'muted', 'selected'].forEach(function (e) {
      ue[e] = new Se(e, 3, !0, e, null, !1, !1);
    }),
    ['capture', 'download'].forEach(function (e) {
      ue[e] = new Se(e, 4, !1, e, null, !1, !1);
    }),
    ['cols', 'rows', 'size', 'span'].forEach(function (e) {
      ue[e] = new Se(e, 6, !1, e, null, !1, !1);
    }),
    ['rowSpan', 'start'].forEach(function (e) {
      ue[e] = new Se(e, 5, !1, e.toLowerCase(), null, !1, !1);
    });
  var Xl = /[\-:]([a-z])/g;
  function Zl(e) {
    return e[1].toUpperCase();
  }
  'accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height'
    .split(' ')
    .forEach(function (e) {
      var t = e.replace(Xl, Zl);
      ue[t] = new Se(t, 1, !1, e, null, !1, !1);
    }),
    'xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type'
      .split(' ')
      .forEach(function (e) {
        var t = e.replace(Xl, Zl);
        ue[t] = new Se(t, 1, !1, e, 'http://www.w3.org/1999/xlink', !1, !1);
      }),
    ['xml:base', 'xml:lang', 'xml:space'].forEach(function (e) {
      var t = e.replace(Xl, Zl);
      ue[t] = new Se(
        t,
        1,
        !1,
        e,
        'http://www.w3.org/XML/1998/namespace',
        !1,
        !1
      );
    }),
    ['tabIndex', 'crossOrigin'].forEach(function (e) {
      ue[e] = new Se(e, 1, !1, e.toLowerCase(), null, !1, !1);
    }),
    (ue.xlinkHref = new Se(
      'xlinkHref',
      1,
      !1,
      'xlink:href',
      'http://www.w3.org/1999/xlink',
      !0,
      !1
    )),
    ['src', 'href', 'action', 'formAction'].forEach(function (e) {
      ue[e] = new Se(e, 1, !1, e.toLowerCase(), null, !0, !0);
    });
  function Jl(e, t, r, n) {
    var l = ue.hasOwnProperty(t) ? ue[t] : null;
    (l !== null
      ? l.type !== 0
      : n ||
        !(2 < t.length) ||
        (t[0] !== 'o' && t[0] !== 'O') ||
        (t[1] !== 'n' && t[1] !== 'N')) &&
      (ld(t, r, l, n) && (r = null),
      n || l === null
        ? rd(t) &&
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
  var dt = ed.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED,
    Ln = Symbol.for('react.element'),
    or = Symbol.for('react.portal'),
    ur = Symbol.for('react.fragment'),
    ql = Symbol.for('react.strict_mode'),
    ei = Symbol.for('react.profiler'),
    ja = Symbol.for('react.provider'),
    Na = Symbol.for('react.context'),
    ti = Symbol.for('react.forward_ref'),
    ri = Symbol.for('react.suspense'),
    ni = Symbol.for('react.suspense_list'),
    li = Symbol.for('react.memo'),
    wt = Symbol.for('react.lazy'),
    Ca = Symbol.for('react.offscreen'),
    _a = Symbol.iterator;
  function Or(e) {
    return e === null || typeof e != 'object'
      ? null
      : ((e = (_a && e[_a]) || e['@@iterator']),
        typeof e == 'function' ? e : null);
  }
  var Y = Object.assign,
    ii;
  function Ur(e) {
    if (ii === void 0)
      try {
        throw Error();
      } catch (r) {
        var t = r.stack.trim().match(/\n( *(at )?)/);
        ii = (t && t[1]) || '';
      }
    return (
      `
` +
      ii +
      e
    );
  }
  var si = !1;
  function ai(e, t) {
    if (!e || si) return '';
    si = !0;
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
          } catch (d) {
            var n = d;
          }
          Reflect.construct(e, [], t);
        } else {
          try {
            t.call();
          } catch (d) {
            n = d;
          }
          e.call(t.prototype);
        }
      else {
        try {
          throw Error();
        } catch (d) {
          n = d;
        }
        e();
      }
    } catch (d) {
      if (d && n && typeof d.stack == 'string') {
        for (
          var l = d.stack.split(`
`),
            i = n.stack.split(`
`),
            a = l.length - 1,
            u = i.length - 1;
          1 <= a && 0 <= u && l[a] !== i[u];

        )
          u--;
        for (; 1 <= a && 0 <= u; a--, u--)
          if (l[a] !== i[u]) {
            if (a !== 1 || u !== 1)
              do
                if ((a--, u--, 0 > u || l[a] !== i[u])) {
                  var o =
                    `
` + l[a].replace(' at new ', ' at ');
                  return (
                    e.displayName &&
                      o.includes('<anonymous>') &&
                      (o = o.replace('<anonymous>', e.displayName)),
                    o
                  );
                }
              while (1 <= a && 0 <= u);
            break;
          }
      }
    } finally {
      (si = !1), (Error.prepareStackTrace = r);
    }
    return (e = e ? e.displayName || e.name : '') ? Ur(e) : '';
  }
  function id(e) {
    switch (e.tag) {
      case 5:
        return Ur(e.type);
      case 16:
        return Ur('Lazy');
      case 13:
        return Ur('Suspense');
      case 19:
        return Ur('SuspenseList');
      case 0:
      case 2:
      case 15:
        return (e = ai(e.type, !1)), e;
      case 11:
        return (e = ai(e.type.render, !1)), e;
      case 1:
        return (e = ai(e.type, !0)), e;
      default:
        return '';
    }
  }
  function oi(e) {
    if (e == null) return null;
    if (typeof e == 'function') return e.displayName || e.name || null;
    if (typeof e == 'string') return e;
    switch (e) {
      case ur:
        return 'Fragment';
      case or:
        return 'Portal';
      case ei:
        return 'Profiler';
      case ql:
        return 'StrictMode';
      case ri:
        return 'Suspense';
      case ni:
        return 'SuspenseList';
    }
    if (typeof e == 'object')
      switch (e.$$typeof) {
        case Na:
          return (e.displayName || 'Context') + '.Consumer';
        case ja:
          return (e._context.displayName || 'Context') + '.Provider';
        case ti:
          var t = e.render;
          return (
            (e = e.displayName),
            e ||
              ((e = t.displayName || t.name || ''),
              (e = e !== '' ? 'ForwardRef(' + e + ')' : 'ForwardRef')),
            e
          );
        case li:
          return (
            (t = e.displayName || null), t !== null ? t : oi(e.type) || 'Memo'
          );
        case wt:
          (t = e._payload), (e = e._init);
          try {
            return oi(e(t));
          } catch {}
      }
    return null;
  }
  function sd(e) {
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
        return oi(t);
      case 8:
        return t === ql ? 'StrictMode' : 'Mode';
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
  function kt(e) {
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
  function Ea(e) {
    var t = e.type;
    return (
      (e = e.nodeName) &&
      e.toLowerCase() === 'input' &&
      (t === 'checkbox' || t === 'radio')
    );
  }
  function ad(e) {
    var t = Ea(e) ? 'checked' : 'value',
      r = Object.getOwnPropertyDescriptor(e.constructor.prototype, t),
      n = '' + e[t];
    if (
      !e.hasOwnProperty(t) &&
      typeof r < 'u' &&
      typeof r.get == 'function' &&
      typeof r.set == 'function'
    ) {
      var l = r.get,
        i = r.set;
      return (
        Object.defineProperty(e, t, {
          configurable: !0,
          get: function () {
            return l.call(this);
          },
          set: function (a) {
            (n = '' + a), i.call(this, a);
          },
        }),
        Object.defineProperty(e, t, { enumerable: r.enumerable }),
        {
          getValue: function () {
            return n;
          },
          setValue: function (a) {
            n = '' + a;
          },
          stopTracking: function () {
            (e._valueTracker = null), delete e[t];
          },
        }
      );
    }
  }
  function Tn(e) {
    e._valueTracker || (e._valueTracker = ad(e));
  }
  function za(e) {
    if (!e) return !1;
    var t = e._valueTracker;
    if (!t) return !0;
    var r = t.getValue(),
      n = '';
    return (
      e && (n = Ea(e) ? (e.checked ? 'true' : 'false') : e.value),
      (e = n),
      e !== r ? (t.setValue(e), !0) : !1
    );
  }
  function Mn(e) {
    if (
      ((e = e || (typeof document < 'u' ? document : void 0)), typeof e > 'u')
    )
      return null;
    try {
      return e.activeElement || e.body;
    } catch {
      return e.body;
    }
  }
  function ui(e, t) {
    var r = t.checked;
    return Y({}, t, {
      defaultChecked: void 0,
      defaultValue: void 0,
      value: void 0,
      checked: r ?? e._wrapperState.initialChecked,
    });
  }
  function Pa(e, t) {
    var r = t.defaultValue == null ? '' : t.defaultValue,
      n = t.checked != null ? t.checked : t.defaultChecked;
    (r = kt(t.value != null ? t.value : r)),
      (e._wrapperState = {
        initialChecked: n,
        initialValue: r,
        controlled:
          t.type === 'checkbox' || t.type === 'radio'
            ? t.checked != null
            : t.value != null,
      });
  }
  function La(e, t) {
    (t = t.checked), t != null && Jl(e, 'checked', t, !1);
  }
  function ci(e, t) {
    La(e, t);
    var r = kt(t.value),
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
      ? di(e, t.type, r)
      : t.hasOwnProperty('defaultValue') && di(e, t.type, kt(t.defaultValue)),
      t.checked == null &&
        t.defaultChecked != null &&
        (e.defaultChecked = !!t.defaultChecked);
  }
  function Ta(e, t, r) {
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
  function di(e, t, r) {
    (t !== 'number' || Mn(e.ownerDocument) !== e) &&
      (r == null
        ? (e.defaultValue = '' + e._wrapperState.initialValue)
        : e.defaultValue !== '' + r && (e.defaultValue = '' + r));
  }
  var $r = Array.isArray;
  function cr(e, t, r, n) {
    if (((e = e.options), t)) {
      t = {};
      for (var l = 0; l < r.length; l++) t['$' + r[l]] = !0;
      for (r = 0; r < e.length; r++)
        (l = t.hasOwnProperty('$' + e[r].value)),
          e[r].selected !== l && (e[r].selected = l),
          l && n && (e[r].defaultSelected = !0);
    } else {
      for (r = '' + kt(r), t = null, l = 0; l < e.length; l++) {
        if (e[l].value === r) {
          (e[l].selected = !0), n && (e[l].defaultSelected = !0);
          return;
        }
        t !== null || e[l].disabled || (t = e[l]);
      }
      t !== null && (t.selected = !0);
    }
  }
  function fi(e, t) {
    if (t.dangerouslySetInnerHTML != null) throw Error(j(91));
    return Y({}, t, {
      value: void 0,
      defaultValue: void 0,
      children: '' + e._wrapperState.initialValue,
    });
  }
  function Ma(e, t) {
    var r = t.value;
    if (r == null) {
      if (((r = t.children), (t = t.defaultValue), r != null)) {
        if (t != null) throw Error(j(92));
        if ($r(r)) {
          if (1 < r.length) throw Error(j(93));
          r = r[0];
        }
        t = r;
      }
      t == null && (t = ''), (r = t);
    }
    e._wrapperState = { initialValue: kt(r) };
  }
  function Da(e, t) {
    var r = kt(t.value),
      n = kt(t.defaultValue);
    r != null &&
      ((r = '' + r),
      r !== e.value && (e.value = r),
      t.defaultValue == null && e.defaultValue !== r && (e.defaultValue = r)),
      n != null && (e.defaultValue = '' + n);
  }
  function Ra(e) {
    var t = e.textContent;
    t === e._wrapperState.initialValue &&
      t !== '' &&
      t !== null &&
      (e.value = t);
  }
  function Ia(e) {
    switch (e) {
      case 'svg':
        return 'http://www.w3.org/2000/svg';
      case 'math':
        return 'http://www.w3.org/1998/Math/MathML';
      default:
        return 'http://www.w3.org/1999/xhtml';
    }
  }
  function pi(e, t) {
    return e == null || e === 'http://www.w3.org/1999/xhtml'
      ? Ia(t)
      : e === 'http://www.w3.org/2000/svg' && t === 'foreignObject'
      ? 'http://www.w3.org/1999/xhtml'
      : e;
  }
  var Dn,
    ba = (function (e) {
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
          Dn = Dn || document.createElement('div'),
            Dn.innerHTML = '<svg>' + t.valueOf().toString() + '</svg>',
            t = Dn.firstChild;
          e.firstChild;

        )
          e.removeChild(e.firstChild);
        for (; t.firstChild; ) e.appendChild(t.firstChild);
      }
    });
  function Ar(e, t) {
    if (t) {
      var r = e.firstChild;
      if (r && r === e.lastChild && r.nodeType === 3) {
        r.nodeValue = t;
        return;
      }
    }
    e.textContent = t;
  }
  var Wr = {
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
    od = ['Webkit', 'ms', 'Moz', 'O'];
  Object.keys(Wr).forEach(function (e) {
    od.forEach(function (t) {
      (t = t + e.charAt(0).toUpperCase() + e.substring(1)), (Wr[t] = Wr[e]);
    });
  });
  function Fa(e, t, r) {
    return t == null || typeof t == 'boolean' || t === ''
      ? ''
      : r || typeof t != 'number' || t === 0 || (Wr.hasOwnProperty(e) && Wr[e])
      ? ('' + t).trim()
      : t + 'px';
  }
  function Oa(e, t) {
    e = e.style;
    for (var r in t)
      if (t.hasOwnProperty(r)) {
        var n = r.indexOf('--') === 0,
          l = Fa(r, t[r], n);
        r === 'float' && (r = 'cssFloat'),
          n ? e.setProperty(r, l) : (e[r] = l);
      }
  }
  var ud = Y(
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
  function mi(e, t) {
    if (t) {
      if (ud[e] && (t.children != null || t.dangerouslySetInnerHTML != null))
        throw Error(j(137, e));
      if (t.dangerouslySetInnerHTML != null) {
        if (t.children != null) throw Error(j(60));
        if (
          typeof t.dangerouslySetInnerHTML != 'object' ||
          !('__html' in t.dangerouslySetInnerHTML)
        )
          throw Error(j(61));
      }
      if (t.style != null && typeof t.style != 'object') throw Error(j(62));
    }
  }
  function hi(e, t) {
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
  var gi = null;
  function vi(e) {
    return (
      (e = e.target || e.srcElement || window),
      e.correspondingUseElement && (e = e.correspondingUseElement),
      e.nodeType === 3 ? e.parentNode : e
    );
  }
  var xi = null,
    dr = null,
    fr = null;
  function Ua(e) {
    if ((e = dn(e))) {
      if (typeof xi != 'function') throw Error(j(280));
      var t = e.stateNode;
      t && ((t = rl(t)), xi(e.stateNode, e.type, t));
    }
  }
  function $a(e) {
    dr ? (fr ? fr.push(e) : (fr = [e])) : (dr = e);
  }
  function Aa() {
    if (dr) {
      var e = dr,
        t = fr;
      if (((fr = dr = null), Ua(e), t))
        for (e = 0; e < t.length; e++) Ua(t[e]);
    }
  }
  function Wa(e, t) {
    return e(t);
  }
  function Va() {}
  var yi = !1;
  function Ba(e, t, r) {
    if (yi) return e(t, r);
    yi = !0;
    try {
      return Wa(e, t, r);
    } finally {
      (yi = !1), (dr !== null || fr !== null) && (Va(), Aa());
    }
  }
  function Vr(e, t) {
    var r = e.stateNode;
    if (r === null) return null;
    var n = rl(r);
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
    if (r && typeof r != 'function') throw Error(j(231, t, typeof r));
    return r;
  }
  var wi = !1;
  if (ct)
    try {
      var Br = {};
      Object.defineProperty(Br, 'passive', {
        get: function () {
          wi = !0;
        },
      }),
        window.addEventListener('test', Br, Br),
        window.removeEventListener('test', Br, Br);
    } catch {
      wi = !1;
    }
  function cd(e, t, r, n, l, i, a, u, o) {
    var d = Array.prototype.slice.call(arguments, 3);
    try {
      t.apply(r, d);
    } catch (v) {
      this.onError(v);
    }
  }
  var Hr = !1,
    Rn = null,
    In = !1,
    ki = null,
    dd = {
      onError: function (e) {
        (Hr = !0), (Rn = e);
      },
    };
  function fd(e, t, r, n, l, i, a, u, o) {
    (Hr = !1), (Rn = null), cd.apply(dd, arguments);
  }
  function pd(e, t, r, n, l, i, a, u, o) {
    if ((fd.apply(this, arguments), Hr)) {
      if (Hr) {
        var d = Rn;
        (Hr = !1), (Rn = null);
      } else throw Error(j(198));
      In || ((In = !0), (ki = d));
    }
  }
  function Ht(e) {
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
  function Ha(e) {
    if (e.tag === 13) {
      var t = e.memoizedState;
      if (
        (t === null &&
          ((e = e.alternate), e !== null && (t = e.memoizedState)),
        t !== null)
      )
        return t.dehydrated;
    }
    return null;
  }
  function Qa(e) {
    if (Ht(e) !== e) throw Error(j(188));
  }
  function md(e) {
    var t = e.alternate;
    if (!t) {
      if (((t = Ht(e)), t === null)) throw Error(j(188));
      return t !== e ? null : e;
    }
    for (var r = e, n = t; ; ) {
      var l = r.return;
      if (l === null) break;
      var i = l.alternate;
      if (i === null) {
        if (((n = l.return), n !== null)) {
          r = n;
          continue;
        }
        break;
      }
      if (l.child === i.child) {
        for (i = l.child; i; ) {
          if (i === r) return Qa(l), e;
          if (i === n) return Qa(l), t;
          i = i.sibling;
        }
        throw Error(j(188));
      }
      if (r.return !== n.return) (r = l), (n = i);
      else {
        for (var a = !1, u = l.child; u; ) {
          if (u === r) {
            (a = !0), (r = l), (n = i);
            break;
          }
          if (u === n) {
            (a = !0), (n = l), (r = i);
            break;
          }
          u = u.sibling;
        }
        if (!a) {
          for (u = i.child; u; ) {
            if (u === r) {
              (a = !0), (r = i), (n = l);
              break;
            }
            if (u === n) {
              (a = !0), (n = i), (r = l);
              break;
            }
            u = u.sibling;
          }
          if (!a) throw Error(j(189));
        }
      }
      if (r.alternate !== n) throw Error(j(190));
    }
    if (r.tag !== 3) throw Error(j(188));
    return r.stateNode.current === r ? e : t;
  }
  function Ka(e) {
    return (e = md(e)), e !== null ? Ya(e) : null;
  }
  function Ya(e) {
    if (e.tag === 5 || e.tag === 6) return e;
    for (e = e.child; e !== null; ) {
      var t = Ya(e);
      if (t !== null) return t;
      e = e.sibling;
    }
    return null;
  }
  var Ga = Me.unstable_scheduleCallback,
    Xa = Me.unstable_cancelCallback,
    hd = Me.unstable_shouldYield,
    gd = Me.unstable_requestPaint,
    q = Me.unstable_now,
    vd = Me.unstable_getCurrentPriorityLevel,
    Si = Me.unstable_ImmediatePriority,
    Za = Me.unstable_UserBlockingPriority,
    bn = Me.unstable_NormalPriority,
    xd = Me.unstable_LowPriority,
    Ja = Me.unstable_IdlePriority,
    Fn = null,
    nt = null;
  function yd(e) {
    if (nt && typeof nt.onCommitFiberRoot == 'function')
      try {
        nt.onCommitFiberRoot(Fn, e, void 0, (e.current.flags & 128) === 128);
      } catch {}
  }
  var He = Math.clz32 ? Math.clz32 : Sd,
    wd = Math.log,
    kd = Math.LN2;
  function Sd(e) {
    return (e >>>= 0), e === 0 ? 32 : (31 - ((wd(e) / kd) | 0)) | 0;
  }
  var On = 64,
    Un = 4194304;
  function Qr(e) {
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
  function $n(e, t) {
    var r = e.pendingLanes;
    if (r === 0) return 0;
    var n = 0,
      l = e.suspendedLanes,
      i = e.pingedLanes,
      a = r & 268435455;
    if (a !== 0) {
      var u = a & ~l;
      u !== 0 ? (n = Qr(u)) : ((i &= a), i !== 0 && (n = Qr(i)));
    } else (a = r & ~l), a !== 0 ? (n = Qr(a)) : i !== 0 && (n = Qr(i));
    if (n === 0) return 0;
    if (
      t !== 0 &&
      t !== n &&
      !(t & l) &&
      ((l = n & -n), (i = t & -t), l >= i || (l === 16 && (i & 4194240) !== 0))
    )
      return t;
    if ((n & 4 && (n |= r & 16), (t = e.entangledLanes), t !== 0))
      for (e = e.entanglements, t &= n; 0 < t; )
        (r = 31 - He(t)), (l = 1 << r), (n |= e[r]), (t &= ~l);
    return n;
  }
  function jd(e, t) {
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
  function Nd(e, t) {
    for (
      var r = e.suspendedLanes,
        n = e.pingedLanes,
        l = e.expirationTimes,
        i = e.pendingLanes;
      0 < i;

    ) {
      var a = 31 - He(i),
        u = 1 << a,
        o = l[a];
      o === -1
        ? (!(u & r) || u & n) && (l[a] = jd(u, t))
        : o <= t && (e.expiredLanes |= u),
        (i &= ~u);
    }
  }
  function ji(e) {
    return (
      (e = e.pendingLanes & -1073741825),
      e !== 0 ? e : e & 1073741824 ? 1073741824 : 0
    );
  }
  function qa() {
    var e = On;
    return (On <<= 1), !(On & 4194240) && (On = 64), e;
  }
  function Ni(e) {
    for (var t = [], r = 0; 31 > r; r++) t.push(e);
    return t;
  }
  function Kr(e, t, r) {
    (e.pendingLanes |= t),
      t !== 536870912 && ((e.suspendedLanes = 0), (e.pingedLanes = 0)),
      (e = e.eventTimes),
      (t = 31 - He(t)),
      (e[t] = r);
  }
  function Cd(e, t) {
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
      var l = 31 - He(r),
        i = 1 << l;
      (t[l] = 0), (n[l] = -1), (e[l] = -1), (r &= ~i);
    }
  }
  function Ci(e, t) {
    var r = (e.entangledLanes |= t);
    for (e = e.entanglements; r; ) {
      var n = 31 - He(r),
        l = 1 << n;
      (l & t) | (e[n] & t) && (e[n] |= t), (r &= ~l);
    }
  }
  var V = 0;
  function eo(e) {
    return (
      (e &= -e), 1 < e ? (4 < e ? (e & 268435455 ? 16 : 536870912) : 4) : 1
    );
  }
  var to,
    _i,
    ro,
    no,
    lo,
    Ei = !1,
    An = [],
    St = null,
    jt = null,
    Nt = null,
    Yr = new Map(),
    Gr = new Map(),
    Ct = [],
    _d =
      'mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit'.split(
        ' '
      );
  function io(e, t) {
    switch (e) {
      case 'focusin':
      case 'focusout':
        St = null;
        break;
      case 'dragenter':
      case 'dragleave':
        jt = null;
        break;
      case 'mouseover':
      case 'mouseout':
        Nt = null;
        break;
      case 'pointerover':
      case 'pointerout':
        Yr.delete(t.pointerId);
        break;
      case 'gotpointercapture':
      case 'lostpointercapture':
        Gr.delete(t.pointerId);
    }
  }
  function Xr(e, t, r, n, l, i) {
    return e === null || e.nativeEvent !== i
      ? ((e = {
          blockedOn: t,
          domEventName: r,
          eventSystemFlags: n,
          nativeEvent: i,
          targetContainers: [l],
        }),
        t !== null && ((t = dn(t)), t !== null && _i(t)),
        e)
      : ((e.eventSystemFlags |= n),
        (t = e.targetContainers),
        l !== null && t.indexOf(l) === -1 && t.push(l),
        e);
  }
  function Ed(e, t, r, n, l) {
    switch (t) {
      case 'focusin':
        return (St = Xr(St, e, t, r, n, l)), !0;
      case 'dragenter':
        return (jt = Xr(jt, e, t, r, n, l)), !0;
      case 'mouseover':
        return (Nt = Xr(Nt, e, t, r, n, l)), !0;
      case 'pointerover':
        var i = l.pointerId;
        return Yr.set(i, Xr(Yr.get(i) || null, e, t, r, n, l)), !0;
      case 'gotpointercapture':
        return (
          (i = l.pointerId),
          Gr.set(i, Xr(Gr.get(i) || null, e, t, r, n, l)),
          !0
        );
    }
    return !1;
  }
  function so(e) {
    var t = Qt(e.target);
    if (t !== null) {
      var r = Ht(t);
      if (r !== null) {
        if (((t = r.tag), t === 13)) {
          if (((t = Ha(r)), t !== null)) {
            (e.blockedOn = t),
              lo(e.priority, function () {
                ro(r);
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
  function Wn(e) {
    if (e.blockedOn !== null) return !1;
    for (var t = e.targetContainers; 0 < t.length; ) {
      var r = Pi(e.domEventName, e.eventSystemFlags, t[0], e.nativeEvent);
      if (r === null) {
        r = e.nativeEvent;
        var n = new r.constructor(r.type, r);
        (gi = n), r.target.dispatchEvent(n), (gi = null);
      } else return (t = dn(r)), t !== null && _i(t), (e.blockedOn = r), !1;
      t.shift();
    }
    return !0;
  }
  function ao(e, t, r) {
    Wn(e) && r.delete(t);
  }
  function zd() {
    (Ei = !1),
      St !== null && Wn(St) && (St = null),
      jt !== null && Wn(jt) && (jt = null),
      Nt !== null && Wn(Nt) && (Nt = null),
      Yr.forEach(ao),
      Gr.forEach(ao);
  }
  function Zr(e, t) {
    e.blockedOn === t &&
      ((e.blockedOn = null),
      Ei ||
        ((Ei = !0),
        Me.unstable_scheduleCallback(Me.unstable_NormalPriority, zd)));
  }
  function Jr(e) {
    function t(l) {
      return Zr(l, e);
    }
    if (0 < An.length) {
      Zr(An[0], e);
      for (var r = 1; r < An.length; r++) {
        var n = An[r];
        n.blockedOn === e && (n.blockedOn = null);
      }
    }
    for (
      St !== null && Zr(St, e),
        jt !== null && Zr(jt, e),
        Nt !== null && Zr(Nt, e),
        Yr.forEach(t),
        Gr.forEach(t),
        r = 0;
      r < Ct.length;
      r++
    )
      (n = Ct[r]), n.blockedOn === e && (n.blockedOn = null);
    for (; 0 < Ct.length && ((r = Ct[0]), r.blockedOn === null); )
      so(r), r.blockedOn === null && Ct.shift();
  }
  var pr = dt.ReactCurrentBatchConfig,
    Vn = !0;
  function Pd(e, t, r, n) {
    var l = V,
      i = pr.transition;
    pr.transition = null;
    try {
      (V = 1), zi(e, t, r, n);
    } finally {
      (V = l), (pr.transition = i);
    }
  }
  function Ld(e, t, r, n) {
    var l = V,
      i = pr.transition;
    pr.transition = null;
    try {
      (V = 4), zi(e, t, r, n);
    } finally {
      (V = l), (pr.transition = i);
    }
  }
  function zi(e, t, r, n) {
    if (Vn) {
      var l = Pi(e, t, r, n);
      if (l === null) Qi(e, t, n, Bn, r), io(e, n);
      else if (Ed(l, e, t, r, n)) n.stopPropagation();
      else if ((io(e, n), t & 4 && -1 < _d.indexOf(e))) {
        for (; l !== null; ) {
          var i = dn(l);
          if (
            (i !== null && to(i),
            (i = Pi(e, t, r, n)),
            i === null && Qi(e, t, n, Bn, r),
            i === l)
          )
            break;
          l = i;
        }
        l !== null && n.stopPropagation();
      } else Qi(e, t, n, null, r);
    }
  }
  var Bn = null;
  function Pi(e, t, r, n) {
    if (((Bn = null), (e = vi(n)), (e = Qt(e)), e !== null))
      if (((t = Ht(e)), t === null)) e = null;
      else if (((r = t.tag), r === 13)) {
        if (((e = Ha(t)), e !== null)) return e;
        e = null;
      } else if (r === 3) {
        if (t.stateNode.current.memoizedState.isDehydrated)
          return t.tag === 3 ? t.stateNode.containerInfo : null;
        e = null;
      } else t !== e && (e = null);
    return (Bn = e), null;
  }
  function oo(e) {
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
        switch (vd()) {
          case Si:
            return 1;
          case Za:
            return 4;
          case bn:
          case xd:
            return 16;
          case Ja:
            return 536870912;
          default:
            return 16;
        }
      default:
        return 16;
    }
  }
  var _t = null,
    Li = null,
    Hn = null;
  function uo() {
    if (Hn) return Hn;
    var e,
      t = Li,
      r = t.length,
      n,
      l = 'value' in _t ? _t.value : _t.textContent,
      i = l.length;
    for (e = 0; e < r && t[e] === l[e]; e++);
    var a = r - e;
    for (n = 1; n <= a && t[r - n] === l[i - n]; n++);
    return (Hn = l.slice(e, 1 < n ? 1 - n : void 0));
  }
  function Qn(e) {
    var t = e.keyCode;
    return (
      'charCode' in e
        ? ((e = e.charCode), e === 0 && t === 13 && (e = 13))
        : (e = t),
      e === 10 && (e = 13),
      32 <= e || e === 13 ? e : 0
    );
  }
  function Kn() {
    return !0;
  }
  function co() {
    return !1;
  }
  function De(e) {
    function t(r, n, l, i, a) {
      (this._reactName = r),
        (this._targetInst = l),
        (this.type = n),
        (this.nativeEvent = i),
        (this.target = a),
        (this.currentTarget = null);
      for (var u in e)
        e.hasOwnProperty(u) && ((r = e[u]), (this[u] = r ? r(i) : i[u]));
      return (
        (this.isDefaultPrevented = (
          i.defaultPrevented != null
            ? i.defaultPrevented
            : i.returnValue === !1
        )
          ? Kn
          : co),
        (this.isPropagationStopped = co),
        this
      );
    }
    return (
      Y(t.prototype, {
        preventDefault: function () {
          this.defaultPrevented = !0;
          var r = this.nativeEvent;
          r &&
            (r.preventDefault
              ? r.preventDefault()
              : typeof r.returnValue != 'unknown' && (r.returnValue = !1),
            (this.isDefaultPrevented = Kn));
        },
        stopPropagation: function () {
          var r = this.nativeEvent;
          r &&
            (r.stopPropagation
              ? r.stopPropagation()
              : typeof r.cancelBubble != 'unknown' && (r.cancelBubble = !0),
            (this.isPropagationStopped = Kn));
        },
        persist: function () {},
        isPersistent: Kn,
      }),
      t
    );
  }
  var mr = {
      eventPhase: 0,
      bubbles: 0,
      cancelable: 0,
      timeStamp: function (e) {
        return e.timeStamp || Date.now();
      },
      defaultPrevented: 0,
      isTrusted: 0,
    },
    Ti = De(mr),
    qr = Y({}, mr, { view: 0, detail: 0 }),
    Td = De(qr),
    Mi,
    Di,
    en,
    Yn = Y({}, qr, {
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
      getModifierState: Ii,
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
          : (e !== en &&
              (en && e.type === 'mousemove'
                ? ((Mi = e.screenX - en.screenX),
                  (Di = e.screenY - en.screenY))
                : (Di = Mi = 0),
              (en = e)),
            Mi);
      },
      movementY: function (e) {
        return 'movementY' in e ? e.movementY : Di;
      },
    }),
    fo = De(Yn),
    Md = Y({}, Yn, { dataTransfer: 0 }),
    Dd = De(Md),
    Rd = Y({}, qr, { relatedTarget: 0 }),
    Ri = De(Rd),
    Id = Y({}, mr, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }),
    bd = De(Id),
    Fd = Y({}, mr, {
      clipboardData: function (e) {
        return 'clipboardData' in e ? e.clipboardData : window.clipboardData;
      },
    }),
    Od = De(Fd),
    Ud = Y({}, mr, { data: 0 }),
    po = De(Ud),
    $d = {
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
    Ad = {
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
    Wd = {
      Alt: 'altKey',
      Control: 'ctrlKey',
      Meta: 'metaKey',
      Shift: 'shiftKey',
    };
  function Vd(e) {
    var t = this.nativeEvent;
    return t.getModifierState
      ? t.getModifierState(e)
      : (e = Wd[e])
      ? !!t[e]
      : !1;
  }
  function Ii() {
    return Vd;
  }
  var Bd = Y({}, qr, {
      key: function (e) {
        if (e.key) {
          var t = $d[e.key] || e.key;
          if (t !== 'Unidentified') return t;
        }
        return e.type === 'keypress'
          ? ((e = Qn(e)), e === 13 ? 'Enter' : String.fromCharCode(e))
          : e.type === 'keydown' || e.type === 'keyup'
          ? Ad[e.keyCode] || 'Unidentified'
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
      getModifierState: Ii,
      charCode: function (e) {
        return e.type === 'keypress' ? Qn(e) : 0;
      },
      keyCode: function (e) {
        return e.type === 'keydown' || e.type === 'keyup' ? e.keyCode : 0;
      },
      which: function (e) {
        return e.type === 'keypress'
          ? Qn(e)
          : e.type === 'keydown' || e.type === 'keyup'
          ? e.keyCode
          : 0;
      },
    }),
    Hd = De(Bd),
    Qd = Y({}, Yn, {
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
    mo = De(Qd),
    Kd = Y({}, qr, {
      touches: 0,
      targetTouches: 0,
      changedTouches: 0,
      altKey: 0,
      metaKey: 0,
      ctrlKey: 0,
      shiftKey: 0,
      getModifierState: Ii,
    }),
    Yd = De(Kd),
    Gd = Y({}, mr, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }),
    Xd = De(Gd),
    Zd = Y({}, Yn, {
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
    Jd = De(Zd),
    qd = [9, 13, 27, 32],
    bi = ct && 'CompositionEvent' in window,
    tn = null;
  ct && 'documentMode' in document && (tn = document.documentMode);
  var ef = ct && 'TextEvent' in window && !tn,
    ho = ct && (!bi || (tn && 8 < tn && 11 >= tn)),
    go = ' ',
    vo = !1;
  function xo(e, t) {
    switch (e) {
      case 'keyup':
        return qd.indexOf(t.keyCode) !== -1;
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
  function yo(e) {
    return (e = e.detail), typeof e == 'object' && 'data' in e ? e.data : null;
  }
  var hr = !1;
  function tf(e, t) {
    switch (e) {
      case 'compositionend':
        return yo(t);
      case 'keypress':
        return t.which !== 32 ? null : ((vo = !0), go);
      case 'textInput':
        return (e = t.data), e === go && vo ? null : e;
      default:
        return null;
    }
  }
  function rf(e, t) {
    if (hr)
      return e === 'compositionend' || (!bi && xo(e, t))
        ? ((e = uo()), (Hn = Li = _t = null), (hr = !1), e)
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
        return ho && t.locale !== 'ko' ? null : t.data;
      default:
        return null;
    }
  }
  var nf = {
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
  function wo(e) {
    var t = e && e.nodeName && e.nodeName.toLowerCase();
    return t === 'input' ? !!nf[e.type] : t === 'textarea';
  }
  function ko(e, t, r, n) {
    $a(n),
      (t = qn(t, 'onChange')),
      0 < t.length &&
        ((r = new Ti('onChange', 'change', null, r, n)),
        e.push({ event: r, listeners: t }));
  }
  var rn = null,
    nn = null;
  function lf(e) {
    Uo(e, 0);
  }
  function Gn(e) {
    var t = wr(e);
    if (za(t)) return e;
  }
  function sf(e, t) {
    if (e === 'change') return t;
  }
  var So = !1;
  if (ct) {
    var Fi;
    if (ct) {
      var Oi = 'oninput' in document;
      if (!Oi) {
        var jo = document.createElement('div');
        jo.setAttribute('oninput', 'return;'),
          (Oi = typeof jo.oninput == 'function');
      }
      Fi = Oi;
    } else Fi = !1;
    So = Fi && (!document.documentMode || 9 < document.documentMode);
  }
  function No() {
    rn && (rn.detachEvent('onpropertychange', Co), (nn = rn = null));
  }
  function Co(e) {
    if (e.propertyName === 'value' && Gn(nn)) {
      var t = [];
      ko(t, nn, e, vi(e)), Ba(lf, t);
    }
  }
  function af(e, t, r) {
    e === 'focusin'
      ? (No(), (rn = t), (nn = r), rn.attachEvent('onpropertychange', Co))
      : e === 'focusout' && No();
  }
  function of(e) {
    if (e === 'selectionchange' || e === 'keyup' || e === 'keydown')
      return Gn(nn);
  }
  function uf(e, t) {
    if (e === 'click') return Gn(t);
  }
  function cf(e, t) {
    if (e === 'input' || e === 'change') return Gn(t);
  }
  function df(e, t) {
    return (e === t && (e !== 0 || 1 / e === 1 / t)) || (e !== e && t !== t);
  }
  var Qe = typeof Object.is == 'function' ? Object.is : df;
  function ln(e, t) {
    if (Qe(e, t)) return !0;
    if (
      typeof e != 'object' ||
      e === null ||
      typeof t != 'object' ||
      t === null
    )
      return !1;
    var r = Object.keys(e),
      n = Object.keys(t);
    if (r.length !== n.length) return !1;
    for (n = 0; n < r.length; n++) {
      var l = r[n];
      if (!Gl.call(t, l) || !Qe(e[l], t[l])) return !1;
    }
    return !0;
  }
  function _o(e) {
    for (; e && e.firstChild; ) e = e.firstChild;
    return e;
  }
  function Eo(e, t) {
    var r = _o(e);
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
      r = _o(r);
    }
  }
  function zo(e, t) {
    return e && t
      ? e === t
        ? !0
        : e && e.nodeType === 3
        ? !1
        : t && t.nodeType === 3
        ? zo(e, t.parentNode)
        : 'contains' in e
        ? e.contains(t)
        : e.compareDocumentPosition
        ? !!(e.compareDocumentPosition(t) & 16)
        : !1
      : !1;
  }
  function Po() {
    for (var e = window, t = Mn(); t instanceof e.HTMLIFrameElement; ) {
      try {
        var r = typeof t.contentWindow.location.href == 'string';
      } catch {
        r = !1;
      }
      if (r) e = t.contentWindow;
      else break;
      t = Mn(e.document);
    }
    return t;
  }
  function Ui(e) {
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
  function ff(e) {
    var t = Po(),
      r = e.focusedElem,
      n = e.selectionRange;
    if (
      t !== r &&
      r &&
      r.ownerDocument &&
      zo(r.ownerDocument.documentElement, r)
    ) {
      if (n !== null && Ui(r)) {
        if (
          ((t = n.start),
          (e = n.end),
          e === void 0 && (e = t),
          'selectionStart' in r)
        )
          (r.selectionStart = t),
            (r.selectionEnd = Math.min(e, r.value.length));
        else if (
          ((e =
            ((t = r.ownerDocument || document) && t.defaultView) || window),
          e.getSelection)
        ) {
          e = e.getSelection();
          var l = r.textContent.length,
            i = Math.min(n.start, l);
          (n = n.end === void 0 ? i : Math.min(n.end, l)),
            !e.extend && i > n && ((l = n), (n = i), (i = l)),
            (l = Eo(r, i));
          var a = Eo(r, n);
          l &&
            a &&
            (e.rangeCount !== 1 ||
              e.anchorNode !== l.node ||
              e.anchorOffset !== l.offset ||
              e.focusNode !== a.node ||
              e.focusOffset !== a.offset) &&
            ((t = t.createRange()),
            t.setStart(l.node, l.offset),
            e.removeAllRanges(),
            i > n
              ? (e.addRange(t), e.extend(a.node, a.offset))
              : (t.setEnd(a.node, a.offset), e.addRange(t)));
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
  var pf = ct && 'documentMode' in document && 11 >= document.documentMode,
    gr = null,
    $i = null,
    sn = null,
    Ai = !1;
  function Lo(e, t, r) {
    var n =
      r.window === r ? r.document : r.nodeType === 9 ? r : r.ownerDocument;
    Ai ||
      gr == null ||
      gr !== Mn(n) ||
      ((n = gr),
      'selectionStart' in n && Ui(n)
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
      (sn && ln(sn, n)) ||
        ((sn = n),
        (n = qn($i, 'onSelect')),
        0 < n.length &&
          ((t = new Ti('onSelect', 'select', null, t, r)),
          e.push({ event: t, listeners: n }),
          (t.target = gr))));
  }
  function Xn(e, t) {
    var r = {};
    return (
      (r[e.toLowerCase()] = t.toLowerCase()),
      (r['Webkit' + e] = 'webkit' + t),
      (r['Moz' + e] = 'moz' + t),
      r
    );
  }
  var vr = {
      animationend: Xn('Animation', 'AnimationEnd'),
      animationiteration: Xn('Animation', 'AnimationIteration'),
      animationstart: Xn('Animation', 'AnimationStart'),
      transitionend: Xn('Transition', 'TransitionEnd'),
    },
    Wi = {},
    To = {};
  ct &&
    ((To = document.createElement('div').style),
    'AnimationEvent' in window ||
      (delete vr.animationend.animation,
      delete vr.animationiteration.animation,
      delete vr.animationstart.animation),
    'TransitionEvent' in window || delete vr.transitionend.transition);
  function Zn(e) {
    if (Wi[e]) return Wi[e];
    if (!vr[e]) return e;
    var t = vr[e],
      r;
    for (r in t) if (t.hasOwnProperty(r) && r in To) return (Wi[e] = t[r]);
    return e;
  }
  var Mo = Zn('animationend'),
    Do = Zn('animationiteration'),
    Ro = Zn('animationstart'),
    Io = Zn('transitionend'),
    bo = new Map(),
    Fo =
      'abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel'.split(
        ' '
      );
  function Et(e, t) {
    bo.set(e, t), Bt(t, [e]);
  }
  for (var Vi = 0; Vi < Fo.length; Vi++) {
    var Bi = Fo[Vi],
      mf = Bi.toLowerCase(),
      hf = Bi[0].toUpperCase() + Bi.slice(1);
    Et(mf, 'on' + hf);
  }
  Et(Mo, 'onAnimationEnd'),
    Et(Do, 'onAnimationIteration'),
    Et(Ro, 'onAnimationStart'),
    Et('dblclick', 'onDoubleClick'),
    Et('focusin', 'onFocus'),
    Et('focusout', 'onBlur'),
    Et(Io, 'onTransitionEnd'),
    ar('onMouseEnter', ['mouseout', 'mouseover']),
    ar('onMouseLeave', ['mouseout', 'mouseover']),
    ar('onPointerEnter', ['pointerout', 'pointerover']),
    ar('onPointerLeave', ['pointerout', 'pointerover']),
    Bt(
      'onChange',
      'change click focusin focusout input keydown keyup selectionchange'.split(
        ' '
      )
    ),
    Bt(
      'onSelect',
      'focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange'.split(
        ' '
      )
    ),
    Bt('onBeforeInput', ['compositionend', 'keypress', 'textInput', 'paste']),
    Bt(
      'onCompositionEnd',
      'compositionend focusout keydown keypress keyup mousedown'.split(' ')
    ),
    Bt(
      'onCompositionStart',
      'compositionstart focusout keydown keypress keyup mousedown'.split(' ')
    ),
    Bt(
      'onCompositionUpdate',
      'compositionupdate focusout keydown keypress keyup mousedown'.split(' ')
    );
  var an =
      'abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting'.split(
        ' '
      ),
    gf = new Set(
      'cancel close invalid load scroll toggle'.split(' ').concat(an)
    );
  function Oo(e, t, r) {
    var n = e.type || 'unknown-event';
    (e.currentTarget = r), pd(n, t, void 0, e), (e.currentTarget = null);
  }
  function Uo(e, t) {
    t = (t & 4) !== 0;
    for (var r = 0; r < e.length; r++) {
      var n = e[r],
        l = n.event;
      n = n.listeners;
      e: {
        var i = void 0;
        if (t)
          for (var a = n.length - 1; 0 <= a; a--) {
            var u = n[a],
              o = u.instance,
              d = u.currentTarget;
            if (((u = u.listener), o !== i && l.isPropagationStopped()))
              break e;
            Oo(l, u, d), (i = o);
          }
        else
          for (a = 0; a < n.length; a++) {
            if (
              ((u = n[a]),
              (o = u.instance),
              (d = u.currentTarget),
              (u = u.listener),
              o !== i && l.isPropagationStopped())
            )
              break e;
            Oo(l, u, d), (i = o);
          }
      }
    }
    if (In) throw ((e = ki), (In = !1), (ki = null), e);
  }
  function H(e, t) {
    var r = t[Ji];
    r === void 0 && (r = t[Ji] = new Set());
    var n = e + '__bubble';
    r.has(n) || ($o(t, e, 2, !1), r.add(n));
  }
  function Hi(e, t, r) {
    var n = 0;
    t && (n |= 4), $o(r, e, n, t);
  }
  var Jn = '_reactListening' + Math.random().toString(36).slice(2);
  function on(e) {
    if (!e[Jn]) {
      (e[Jn] = !0),
        wa.forEach(function (r) {
          r !== 'selectionchange' && (gf.has(r) || Hi(r, !1, e), Hi(r, !0, e));
        });
      var t = e.nodeType === 9 ? e : e.ownerDocument;
      t === null || t[Jn] || ((t[Jn] = !0), Hi('selectionchange', !1, t));
    }
  }
  function $o(e, t, r, n) {
    switch (oo(t)) {
      case 1:
        var l = Pd;
        break;
      case 4:
        l = Ld;
        break;
      default:
        l = zi;
    }
    (r = l.bind(null, t, r, e)),
      (l = void 0),
      !wi ||
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
  function Qi(e, t, r, n, l) {
    var i = n;
    if (!(t & 1) && !(t & 2) && n !== null)
      e: for (;;) {
        if (n === null) return;
        var a = n.tag;
        if (a === 3 || a === 4) {
          var u = n.stateNode.containerInfo;
          if (u === l || (u.nodeType === 8 && u.parentNode === l)) break;
          if (a === 4)
            for (a = n.return; a !== null; ) {
              var o = a.tag;
              if (
                (o === 3 || o === 4) &&
                ((o = a.stateNode.containerInfo),
                o === l || (o.nodeType === 8 && o.parentNode === l))
              )
                return;
              a = a.return;
            }
          for (; u !== null; ) {
            if (((a = Qt(u)), a === null)) return;
            if (((o = a.tag), o === 5 || o === 6)) {
              n = i = a;
              continue e;
            }
            u = u.parentNode;
          }
        }
        n = n.return;
      }
    Ba(function () {
      var d = i,
        v = vi(r),
        g = [];
      e: {
        var m = bo.get(e);
        if (m !== void 0) {
          var h = Ti,
            y = e;
          switch (e) {
            case 'keypress':
              if (Qn(r) === 0) break e;
            case 'keydown':
            case 'keyup':
              h = Hd;
              break;
            case 'focusin':
              (y = 'focus'), (h = Ri);
              break;
            case 'focusout':
              (y = 'blur'), (h = Ri);
              break;
            case 'beforeblur':
            case 'afterblur':
              h = Ri;
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
              h = fo;
              break;
            case 'drag':
            case 'dragend':
            case 'dragenter':
            case 'dragexit':
            case 'dragleave':
            case 'dragover':
            case 'dragstart':
            case 'drop':
              h = Dd;
              break;
            case 'touchcancel':
            case 'touchend':
            case 'touchmove':
            case 'touchstart':
              h = Yd;
              break;
            case Mo:
            case Do:
            case Ro:
              h = bd;
              break;
            case Io:
              h = Xd;
              break;
            case 'scroll':
              h = Td;
              break;
            case 'wheel':
              h = Jd;
              break;
            case 'copy':
            case 'cut':
            case 'paste':
              h = Od;
              break;
            case 'gotpointercapture':
            case 'lostpointercapture':
            case 'pointercancel':
            case 'pointerdown':
            case 'pointermove':
            case 'pointerout':
            case 'pointerover':
            case 'pointerup':
              h = mo;
          }
          var k = (t & 4) !== 0,
            M = !k && e === 'scroll',
            f = k ? (m !== null ? m + 'Capture' : null) : m;
          k = [];
          for (var c = d, p; c !== null; ) {
            p = c;
            var w = p.stateNode;
            if (
              (p.tag === 5 &&
                w !== null &&
                ((p = w),
                f !== null &&
                  ((w = Vr(c, f)), w != null && k.push(un(c, w, p)))),
              M)
            )
              break;
            c = c.return;
          }
          0 < k.length &&
            ((m = new h(m, y, null, r, v)),
            g.push({ event: m, listeners: k }));
        }
      }
      if (!(t & 7)) {
        e: {
          if (
            ((m = e === 'mouseover' || e === 'pointerover'),
            (h = e === 'mouseout' || e === 'pointerout'),
            m &&
              r !== gi &&
              (y = r.relatedTarget || r.fromElement) &&
              (Qt(y) || y[ft]))
          )
            break e;
          if (
            (h || m) &&
            ((m =
              v.window === v
                ? v
                : (m = v.ownerDocument)
                ? m.defaultView || m.parentWindow
                : window),
            h
              ? ((y = r.relatedTarget || r.toElement),
                (h = d),
                (y = y ? Qt(y) : null),
                y !== null &&
                  ((M = Ht(y)), y !== M || (y.tag !== 5 && y.tag !== 6)) &&
                  (y = null))
              : ((h = null), (y = d)),
            h !== y)
          ) {
            if (
              ((k = fo),
              (w = 'onMouseLeave'),
              (f = 'onMouseEnter'),
              (c = 'mouse'),
              (e === 'pointerout' || e === 'pointerover') &&
                ((k = mo),
                (w = 'onPointerLeave'),
                (f = 'onPointerEnter'),
                (c = 'pointer')),
              (M = h == null ? m : wr(h)),
              (p = y == null ? m : wr(y)),
              (m = new k(w, c + 'leave', h, r, v)),
              (m.target = M),
              (m.relatedTarget = p),
              (w = null),
              Qt(v) === d &&
                ((k = new k(f, c + 'enter', y, r, v)),
                (k.target = p),
                (k.relatedTarget = M),
                (w = k)),
              (M = w),
              h && y)
            )
              t: {
                for (k = h, f = y, c = 0, p = k; p; p = xr(p)) c++;
                for (p = 0, w = f; w; w = xr(w)) p++;
                for (; 0 < c - p; ) (k = xr(k)), c--;
                for (; 0 < p - c; ) (f = xr(f)), p--;
                for (; c--; ) {
                  if (k === f || (f !== null && k === f.alternate)) break t;
                  (k = xr(k)), (f = xr(f));
                }
                k = null;
              }
            else k = null;
            h !== null && Ao(g, m, h, k, !1),
              y !== null && M !== null && Ao(g, M, y, k, !0);
          }
        }
        e: {
          if (
            ((m = d ? wr(d) : window),
            (h = m.nodeName && m.nodeName.toLowerCase()),
            h === 'select' || (h === 'input' && m.type === 'file'))
          )
            var z = sf;
          else if (wo(m))
            if (So) z = cf;
            else {
              z = of;
              var S = af;
            }
          else
            (h = m.nodeName) &&
              h.toLowerCase() === 'input' &&
              (m.type === 'checkbox' || m.type === 'radio') &&
              (z = uf);
          if (z && (z = z(e, d))) {
            ko(g, z, r, v);
            break e;
          }
          S && S(e, m, d),
            e === 'focusout' &&
              (S = m._wrapperState) &&
              S.controlled &&
              m.type === 'number' &&
              di(m, 'number', m.value);
        }
        switch (((S = d ? wr(d) : window), e)) {
          case 'focusin':
            (wo(S) || S.contentEditable === 'true') &&
              ((gr = S), ($i = d), (sn = null));
            break;
          case 'focusout':
            sn = $i = gr = null;
            break;
          case 'mousedown':
            Ai = !0;
            break;
          case 'contextmenu':
          case 'mouseup':
          case 'dragend':
            (Ai = !1), Lo(g, r, v);
            break;
          case 'selectionchange':
            if (pf) break;
          case 'keydown':
          case 'keyup':
            Lo(g, r, v);
        }
        var C;
        if (bi)
          e: {
            switch (e) {
              case 'compositionstart':
                var P = 'onCompositionStart';
                break e;
              case 'compositionend':
                P = 'onCompositionEnd';
                break e;
              case 'compositionupdate':
                P = 'onCompositionUpdate';
                break e;
            }
            P = void 0;
          }
        else
          hr
            ? xo(e, r) && (P = 'onCompositionEnd')
            : e === 'keydown' &&
              r.keyCode === 229 &&
              (P = 'onCompositionStart');
        P &&
          (ho &&
            r.locale !== 'ko' &&
            (hr || P !== 'onCompositionStart'
              ? P === 'onCompositionEnd' && hr && (C = uo())
              : ((_t = v),
                (Li = 'value' in _t ? _t.value : _t.textContent),
                (hr = !0))),
          (S = qn(d, P)),
          0 < S.length &&
            ((P = new po(P, e, null, r, v)),
            g.push({ event: P, listeners: S }),
            C ? (P.data = C) : ((C = yo(r)), C !== null && (P.data = C)))),
          (C = ef ? tf(e, r) : rf(e, r)) &&
            ((d = qn(d, 'onBeforeInput')),
            0 < d.length &&
              ((v = new po('onBeforeInput', 'beforeinput', null, r, v)),
              g.push({ event: v, listeners: d }),
              (v.data = C)));
      }
      Uo(g, t);
    });
  }
  function un(e, t, r) {
    return { instance: e, listener: t, currentTarget: r };
  }
  function qn(e, t) {
    for (var r = t + 'Capture', n = []; e !== null; ) {
      var l = e,
        i = l.stateNode;
      l.tag === 5 &&
        i !== null &&
        ((l = i),
        (i = Vr(e, r)),
        i != null && n.unshift(un(e, i, l)),
        (i = Vr(e, t)),
        i != null && n.push(un(e, i, l))),
        (e = e.return);
    }
    return n;
  }
  function xr(e) {
    if (e === null) return null;
    do e = e.return;
    while (e && e.tag !== 5);
    return e || null;
  }
  function Ao(e, t, r, n, l) {
    for (var i = t._reactName, a = []; r !== null && r !== n; ) {
      var u = r,
        o = u.alternate,
        d = u.stateNode;
      if (o !== null && o === n) break;
      u.tag === 5 &&
        d !== null &&
        ((u = d),
        l
          ? ((o = Vr(r, i)), o != null && a.unshift(un(r, o, u)))
          : l || ((o = Vr(r, i)), o != null && a.push(un(r, o, u)))),
        (r = r.return);
    }
    a.length !== 0 && e.push({ event: t, listeners: a });
  }
  var vf = /\r\n?/g,
    xf = /\u0000|\uFFFD/g;
  function Wo(e) {
    return (typeof e == 'string' ? e : '' + e)
      .replace(
        vf,
        `
`
      )
      .replace(xf, '');
  }
  function el(e, t, r) {
    if (((t = Wo(t)), Wo(e) !== t && r)) throw Error(j(425));
  }
  function tl() {}
  var Ki = null,
    Yi = null;
  function Gi(e, t) {
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
  var Xi = typeof setTimeout == 'function' ? setTimeout : void 0,
    yf = typeof clearTimeout == 'function' ? clearTimeout : void 0,
    Vo = typeof Promise == 'function' ? Promise : void 0,
    wf =
      typeof queueMicrotask == 'function'
        ? queueMicrotask
        : typeof Vo < 'u'
        ? function (e) {
            return Vo.resolve(null).then(e).catch(kf);
          }
        : Xi;
  function kf(e) {
    setTimeout(function () {
      throw e;
    });
  }
  function Zi(e, t) {
    var r = t,
      n = 0;
    do {
      var l = r.nextSibling;
      if ((e.removeChild(r), l && l.nodeType === 8))
        if (((r = l.data), r === '/$')) {
          if (n === 0) {
            e.removeChild(l), Jr(t);
            return;
          }
          n--;
        } else (r !== '$' && r !== '$?' && r !== '$!') || n++;
      r = l;
    } while (r);
    Jr(t);
  }
  function zt(e) {
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
  function Bo(e) {
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
  var yr = Math.random().toString(36).slice(2),
    lt = '__reactFiber$' + yr,
    cn = '__reactProps$' + yr,
    ft = '__reactContainer$' + yr,
    Ji = '__reactEvents$' + yr,
    Sf = '__reactListeners$' + yr,
    jf = '__reactHandles$' + yr;
  function Qt(e) {
    var t = e[lt];
    if (t) return t;
    for (var r = e.parentNode; r; ) {
      if ((t = r[ft] || r[lt])) {
        if (
          ((r = t.alternate),
          t.child !== null || (r !== null && r.child !== null))
        )
          for (e = Bo(e); e !== null; ) {
            if ((r = e[lt])) return r;
            e = Bo(e);
          }
        return t;
      }
      (e = r), (r = e.parentNode);
    }
    return null;
  }
  function dn(e) {
    return (
      (e = e[lt] || e[ft]),
      !e || (e.tag !== 5 && e.tag !== 6 && e.tag !== 13 && e.tag !== 3)
        ? null
        : e
    );
  }
  function wr(e) {
    if (e.tag === 5 || e.tag === 6) return e.stateNode;
    throw Error(j(33));
  }
  function rl(e) {
    return e[cn] || null;
  }
  var qi = [],
    kr = -1;
  function Pt(e) {
    return { current: e };
  }
  function Q(e) {
    0 > kr || ((e.current = qi[kr]), (qi[kr] = null), kr--);
  }
  function B(e, t) {
    kr++, (qi[kr] = e.current), (e.current = t);
  }
  var Lt = {},
    me = Pt(Lt),
    Ce = Pt(!1),
    Kt = Lt;
  function Sr(e, t) {
    var r = e.type.contextTypes;
    if (!r) return Lt;
    var n = e.stateNode;
    if (n && n.__reactInternalMemoizedUnmaskedChildContext === t)
      return n.__reactInternalMemoizedMaskedChildContext;
    var l = {},
      i;
    for (i in r) l[i] = t[i];
    return (
      n &&
        ((e = e.stateNode),
        (e.__reactInternalMemoizedUnmaskedChildContext = t),
        (e.__reactInternalMemoizedMaskedChildContext = l)),
      l
    );
  }
  function _e(e) {
    return (e = e.childContextTypes), e != null;
  }
  function nl() {
    Q(Ce), Q(me);
  }
  function Ho(e, t, r) {
    if (me.current !== Lt) throw Error(j(168));
    B(me, t), B(Ce, r);
  }
  function Qo(e, t, r) {
    var n = e.stateNode;
    if (((t = t.childContextTypes), typeof n.getChildContext != 'function'))
      return r;
    n = n.getChildContext();
    for (var l in n) if (!(l in t)) throw Error(j(108, sd(e) || 'Unknown', l));
    return Y({}, r, n);
  }
  function ll(e) {
    return (
      (e =
        ((e = e.stateNode) && e.__reactInternalMemoizedMergedChildContext) ||
        Lt),
      (Kt = me.current),
      B(me, e),
      B(Ce, Ce.current),
      !0
    );
  }
  function Ko(e, t, r) {
    var n = e.stateNode;
    if (!n) throw Error(j(169));
    r
      ? ((e = Qo(e, t, Kt)),
        (n.__reactInternalMemoizedMergedChildContext = e),
        Q(Ce),
        Q(me),
        B(me, e))
      : Q(Ce),
      B(Ce, r);
  }
  var pt = null,
    il = !1,
    es = !1;
  function Yo(e) {
    pt === null ? (pt = [e]) : pt.push(e);
  }
  function Nf(e) {
    (il = !0), Yo(e);
  }
  function Tt() {
    if (!es && pt !== null) {
      es = !0;
      var e = 0,
        t = V;
      try {
        var r = pt;
        for (V = 1; e < r.length; e++) {
          var n = r[e];
          do n = n(!0);
          while (n !== null);
        }
        (pt = null), (il = !1);
      } catch (l) {
        throw (pt !== null && (pt = pt.slice(e + 1)), Ga(Si, Tt), l);
      } finally {
        (V = t), (es = !1);
      }
    }
    return null;
  }
  var jr = [],
    Nr = 0,
    sl = null,
    al = 0,
    Oe = [],
    Ue = 0,
    Yt = null,
    mt = 1,
    ht = '';
  function Gt(e, t) {
    (jr[Nr++] = al), (jr[Nr++] = sl), (sl = e), (al = t);
  }
  function Go(e, t, r) {
    (Oe[Ue++] = mt), (Oe[Ue++] = ht), (Oe[Ue++] = Yt), (Yt = e);
    var n = mt;
    e = ht;
    var l = 32 - He(n) - 1;
    (n &= ~(1 << l)), (r += 1);
    var i = 32 - He(t) + l;
    if (30 < i) {
      var a = l - (l % 5);
      (i = (n & ((1 << a) - 1)).toString(32)),
        (n >>= a),
        (l -= a),
        (mt = (1 << (32 - He(t) + l)) | (r << l) | n),
        (ht = i + e);
    } else (mt = (1 << i) | (r << l) | n), (ht = e);
  }
  function ts(e) {
    e.return !== null && (Gt(e, 1), Go(e, 1, 0));
  }
  function rs(e) {
    for (; e === sl; )
      (sl = jr[--Nr]), (jr[Nr] = null), (al = jr[--Nr]), (jr[Nr] = null);
    for (; e === Yt; )
      (Yt = Oe[--Ue]),
        (Oe[Ue] = null),
        (ht = Oe[--Ue]),
        (Oe[Ue] = null),
        (mt = Oe[--Ue]),
        (Oe[Ue] = null);
  }
  var Re = null,
    Ie = null,
    K = !1,
    Ke = null;
  function Xo(e, t) {
    var r = Ve(5, null, null, 0);
    (r.elementType = 'DELETED'),
      (r.stateNode = t),
      (r.return = e),
      (t = e.deletions),
      t === null ? ((e.deletions = [r]), (e.flags |= 16)) : t.push(r);
  }
  function Zo(e, t) {
    switch (e.tag) {
      case 5:
        var r = e.type;
        return (
          (t =
            t.nodeType !== 1 || r.toLowerCase() !== t.nodeName.toLowerCase()
              ? null
              : t),
          t !== null
            ? ((e.stateNode = t), (Re = e), (Ie = zt(t.firstChild)), !0)
            : !1
        );
      case 6:
        return (
          (t = e.pendingProps === '' || t.nodeType !== 3 ? null : t),
          t !== null ? ((e.stateNode = t), (Re = e), (Ie = null), !0) : !1
        );
      case 13:
        return (
          (t = t.nodeType !== 8 ? null : t),
          t !== null
            ? ((r = Yt !== null ? { id: mt, overflow: ht } : null),
              (e.memoizedState = {
                dehydrated: t,
                treeContext: r,
                retryLane: 1073741824,
              }),
              (r = Ve(18, null, null, 0)),
              (r.stateNode = t),
              (r.return = e),
              (e.child = r),
              (Re = e),
              (Ie = null),
              !0)
            : !1
        );
      default:
        return !1;
    }
  }
  function ns(e) {
    return (e.mode & 1) !== 0 && (e.flags & 128) === 0;
  }
  function ls(e) {
    if (K) {
      var t = Ie;
      if (t) {
        var r = t;
        if (!Zo(e, t)) {
          if (ns(e)) throw Error(j(418));
          t = zt(r.nextSibling);
          var n = Re;
          t && Zo(e, t)
            ? Xo(n, r)
            : ((e.flags = (e.flags & -4097) | 2), (K = !1), (Re = e));
        }
      } else {
        if (ns(e)) throw Error(j(418));
        (e.flags = (e.flags & -4097) | 2), (K = !1), (Re = e);
      }
    }
  }
  function Jo(e) {
    for (
      e = e.return;
      e !== null && e.tag !== 5 && e.tag !== 3 && e.tag !== 13;

    )
      e = e.return;
    Re = e;
  }
  function ol(e) {
    if (e !== Re) return !1;
    if (!K) return Jo(e), (K = !0), !1;
    var t;
    if (
      ((t = e.tag !== 3) &&
        !(t = e.tag !== 5) &&
        ((t = e.type),
        (t = t !== 'head' && t !== 'body' && !Gi(e.type, e.memoizedProps))),
      t && (t = Ie))
    ) {
      if (ns(e)) throw (qo(), Error(j(418)));
      for (; t; ) Xo(e, t), (t = zt(t.nextSibling));
    }
    if ((Jo(e), e.tag === 13)) {
      if (((e = e.memoizedState), (e = e !== null ? e.dehydrated : null), !e))
        throw Error(j(317));
      e: {
        for (e = e.nextSibling, t = 0; e; ) {
          if (e.nodeType === 8) {
            var r = e.data;
            if (r === '/$') {
              if (t === 0) {
                Ie = zt(e.nextSibling);
                break e;
              }
              t--;
            } else (r !== '$' && r !== '$!' && r !== '$?') || t++;
          }
          e = e.nextSibling;
        }
        Ie = null;
      }
    } else Ie = Re ? zt(e.stateNode.nextSibling) : null;
    return !0;
  }
  function qo() {
    for (var e = Ie; e; ) e = zt(e.nextSibling);
  }
  function Cr() {
    (Ie = Re = null), (K = !1);
  }
  function is(e) {
    Ke === null ? (Ke = [e]) : Ke.push(e);
  }
  var Cf = dt.ReactCurrentBatchConfig;
  function fn(e, t, r) {
    if (
      ((e = r.ref),
      e !== null && typeof e != 'function' && typeof e != 'object')
    ) {
      if (r._owner) {
        if (((r = r._owner), r)) {
          if (r.tag !== 1) throw Error(j(309));
          var n = r.stateNode;
        }
        if (!n) throw Error(j(147, e));
        var l = n,
          i = '' + e;
        return t !== null &&
          t.ref !== null &&
          typeof t.ref == 'function' &&
          t.ref._stringRef === i
          ? t.ref
          : ((t = function (a) {
              var u = l.refs;
              a === null ? delete u[i] : (u[i] = a);
            }),
            (t._stringRef = i),
            t);
      }
      if (typeof e != 'string') throw Error(j(284));
      if (!r._owner) throw Error(j(290, e));
    }
    return e;
  }
  function ul(e, t) {
    throw (
      ((e = Object.prototype.toString.call(t)),
      Error(
        j(
          31,
          e === '[object Object]'
            ? 'object with keys {' + Object.keys(t).join(', ') + '}'
            : e
        )
      ))
    );
  }
  function eu(e) {
    var t = e._init;
    return t(e._payload);
  }
  function tu(e) {
    function t(f, c) {
      if (e) {
        var p = f.deletions;
        p === null ? ((f.deletions = [c]), (f.flags |= 16)) : p.push(c);
      }
    }
    function r(f, c) {
      if (!e) return null;
      for (; c !== null; ) t(f, c), (c = c.sibling);
      return null;
    }
    function n(f, c) {
      for (f = new Map(); c !== null; )
        c.key !== null ? f.set(c.key, c) : f.set(c.index, c), (c = c.sibling);
      return f;
    }
    function l(f, c) {
      return (f = Ut(f, c)), (f.index = 0), (f.sibling = null), f;
    }
    function i(f, c, p) {
      return (
        (f.index = p),
        e
          ? ((p = f.alternate),
            p !== null
              ? ((p = p.index), p < c ? ((f.flags |= 2), c) : p)
              : ((f.flags |= 2), c))
          : ((f.flags |= 1048576), c)
      );
    }
    function a(f) {
      return e && f.alternate === null && (f.flags |= 2), f;
    }
    function u(f, c, p, w) {
      return c === null || c.tag !== 6
        ? ((c = Xs(p, f.mode, w)), (c.return = f), c)
        : ((c = l(c, p)), (c.return = f), c);
    }
    function o(f, c, p, w) {
      var z = p.type;
      return z === ur
        ? v(f, c, p.props.children, w, p.key)
        : c !== null &&
          (c.elementType === z ||
            (typeof z == 'object' &&
              z !== null &&
              z.$$typeof === wt &&
              eu(z) === c.type))
        ? ((w = l(c, p.props)), (w.ref = fn(f, c, p)), (w.return = f), w)
        : ((w = Dl(p.type, p.key, p.props, null, f.mode, w)),
          (w.ref = fn(f, c, p)),
          (w.return = f),
          w);
    }
    function d(f, c, p, w) {
      return c === null ||
        c.tag !== 4 ||
        c.stateNode.containerInfo !== p.containerInfo ||
        c.stateNode.implementation !== p.implementation
        ? ((c = Zs(p, f.mode, w)), (c.return = f), c)
        : ((c = l(c, p.children || [])), (c.return = f), c);
    }
    function v(f, c, p, w, z) {
      return c === null || c.tag !== 7
        ? ((c = nr(p, f.mode, w, z)), (c.return = f), c)
        : ((c = l(c, p)), (c.return = f), c);
    }
    function g(f, c, p) {
      if ((typeof c == 'string' && c !== '') || typeof c == 'number')
        return (c = Xs('' + c, f.mode, p)), (c.return = f), c;
      if (typeof c == 'object' && c !== null) {
        switch (c.$$typeof) {
          case Ln:
            return (
              (p = Dl(c.type, c.key, c.props, null, f.mode, p)),
              (p.ref = fn(f, null, c)),
              (p.return = f),
              p
            );
          case or:
            return (c = Zs(c, f.mode, p)), (c.return = f), c;
          case wt:
            var w = c._init;
            return g(f, w(c._payload), p);
        }
        if ($r(c) || Or(c))
          return (c = nr(c, f.mode, p, null)), (c.return = f), c;
        ul(f, c);
      }
      return null;
    }
    function m(f, c, p, w) {
      var z = c !== null ? c.key : null;
      if ((typeof p == 'string' && p !== '') || typeof p == 'number')
        return z !== null ? null : u(f, c, '' + p, w);
      if (typeof p == 'object' && p !== null) {
        switch (p.$$typeof) {
          case Ln:
            return p.key === z ? o(f, c, p, w) : null;
          case or:
            return p.key === z ? d(f, c, p, w) : null;
          case wt:
            return (z = p._init), m(f, c, z(p._payload), w);
        }
        if ($r(p) || Or(p)) return z !== null ? null : v(f, c, p, w, null);
        ul(f, p);
      }
      return null;
    }
    function h(f, c, p, w, z) {
      if ((typeof w == 'string' && w !== '') || typeof w == 'number')
        return (f = f.get(p) || null), u(c, f, '' + w, z);
      if (typeof w == 'object' && w !== null) {
        switch (w.$$typeof) {
          case Ln:
            return (
              (f = f.get(w.key === null ? p : w.key) || null), o(c, f, w, z)
            );
          case or:
            return (
              (f = f.get(w.key === null ? p : w.key) || null), d(c, f, w, z)
            );
          case wt:
            var S = w._init;
            return h(f, c, p, S(w._payload), z);
        }
        if ($r(w) || Or(w)) return (f = f.get(p) || null), v(c, f, w, z, null);
        ul(c, w);
      }
      return null;
    }
    function y(f, c, p, w) {
      for (
        var z = null, S = null, C = c, P = (c = 0), W = null;
        C !== null && P < p.length;
        P++
      ) {
        C.index > P ? ((W = C), (C = null)) : (W = C.sibling);
        var R = m(f, C, p[P], w);
        if (R === null) {
          C === null && (C = W);
          break;
        }
        e && C && R.alternate === null && t(f, C),
          (c = i(R, c, P)),
          S === null ? (z = R) : (S.sibling = R),
          (S = R),
          (C = W);
      }
      if (P === p.length) return r(f, C), K && Gt(f, P), z;
      if (C === null) {
        for (; P < p.length; P++)
          (C = g(f, p[P], w)),
            C !== null &&
              ((c = i(C, c, P)),
              S === null ? (z = C) : (S.sibling = C),
              (S = C));
        return K && Gt(f, P), z;
      }
      for (C = n(f, C); P < p.length; P++)
        (W = h(C, f, P, p[P], w)),
          W !== null &&
            (e && W.alternate !== null && C.delete(W.key === null ? P : W.key),
            (c = i(W, c, P)),
            S === null ? (z = W) : (S.sibling = W),
            (S = W));
      return (
        e &&
          C.forEach(function (xe) {
            return t(f, xe);
          }),
        K && Gt(f, P),
        z
      );
    }
    function k(f, c, p, w) {
      var z = Or(p);
      if (typeof z != 'function') throw Error(j(150));
      if (((p = z.call(p)), p == null)) throw Error(j(151));
      for (
        var S = (z = null), C = c, P = (c = 0), W = null, R = p.next();
        C !== null && !R.done;
        P++, R = p.next()
      ) {
        C.index > P ? ((W = C), (C = null)) : (W = C.sibling);
        var xe = m(f, C, R.value, w);
        if (xe === null) {
          C === null && (C = W);
          break;
        }
        e && C && xe.alternate === null && t(f, C),
          (c = i(xe, c, P)),
          S === null ? (z = xe) : (S.sibling = xe),
          (S = xe),
          (C = W);
      }
      if (R.done) return r(f, C), K && Gt(f, P), z;
      if (C === null) {
        for (; !R.done; P++, R = p.next())
          (R = g(f, R.value, w)),
            R !== null &&
              ((c = i(R, c, P)),
              S === null ? (z = R) : (S.sibling = R),
              (S = R));
        return K && Gt(f, P), z;
      }
      for (C = n(f, C); !R.done; P++, R = p.next())
        (R = h(C, f, P, R.value, w)),
          R !== null &&
            (e && R.alternate !== null && C.delete(R.key === null ? P : R.key),
            (c = i(R, c, P)),
            S === null ? (z = R) : (S.sibling = R),
            (S = R));
      return (
        e &&
          C.forEach(function (fe) {
            return t(f, fe);
          }),
        K && Gt(f, P),
        z
      );
    }
    function M(f, c, p, w) {
      if (
        (typeof p == 'object' &&
          p !== null &&
          p.type === ur &&
          p.key === null &&
          (p = p.props.children),
        typeof p == 'object' && p !== null)
      ) {
        switch (p.$$typeof) {
          case Ln:
            e: {
              for (var z = p.key, S = c; S !== null; ) {
                if (S.key === z) {
                  if (((z = p.type), z === ur)) {
                    if (S.tag === 7) {
                      r(f, S.sibling),
                        (c = l(S, p.props.children)),
                        (c.return = f),
                        (f = c);
                      break e;
                    }
                  } else if (
                    S.elementType === z ||
                    (typeof z == 'object' &&
                      z !== null &&
                      z.$$typeof === wt &&
                      eu(z) === S.type)
                  ) {
                    r(f, S.sibling),
                      (c = l(S, p.props)),
                      (c.ref = fn(f, S, p)),
                      (c.return = f),
                      (f = c);
                    break e;
                  }
                  r(f, S);
                  break;
                } else t(f, S);
                S = S.sibling;
              }
              p.type === ur
                ? ((c = nr(p.props.children, f.mode, w, p.key)),
                  (c.return = f),
                  (f = c))
                : ((w = Dl(p.type, p.key, p.props, null, f.mode, w)),
                  (w.ref = fn(f, c, p)),
                  (w.return = f),
                  (f = w));
            }
            return a(f);
          case or:
            e: {
              for (S = p.key; c !== null; ) {
                if (c.key === S)
                  if (
                    c.tag === 4 &&
                    c.stateNode.containerInfo === p.containerInfo &&
                    c.stateNode.implementation === p.implementation
                  ) {
                    r(f, c.sibling),
                      (c = l(c, p.children || [])),
                      (c.return = f),
                      (f = c);
                    break e;
                  } else {
                    r(f, c);
                    break;
                  }
                else t(f, c);
                c = c.sibling;
              }
              (c = Zs(p, f.mode, w)), (c.return = f), (f = c);
            }
            return a(f);
          case wt:
            return (S = p._init), M(f, c, S(p._payload), w);
        }
        if ($r(p)) return y(f, c, p, w);
        if (Or(p)) return k(f, c, p, w);
        ul(f, p);
      }
      return (typeof p == 'string' && p !== '') || typeof p == 'number'
        ? ((p = '' + p),
          c !== null && c.tag === 6
            ? (r(f, c.sibling), (c = l(c, p)), (c.return = f), (f = c))
            : (r(f, c), (c = Xs(p, f.mode, w)), (c.return = f), (f = c)),
          a(f))
        : r(f, c);
    }
    return M;
  }
  var _r = tu(!0),
    ru = tu(!1),
    cl = Pt(null),
    dl = null,
    Er = null,
    ss = null;
  function as() {
    ss = Er = dl = null;
  }
  function os(e) {
    var t = cl.current;
    Q(cl), (e._currentValue = t);
  }
  function us(e, t, r) {
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
  function zr(e, t) {
    (dl = e),
      (ss = Er = null),
      (e = e.dependencies),
      e !== null &&
        e.firstContext !== null &&
        (e.lanes & t && (Ee = !0), (e.firstContext = null));
  }
  function $e(e) {
    var t = e._currentValue;
    if (ss !== e)
      if (((e = { context: e, memoizedValue: t, next: null }), Er === null)) {
        if (dl === null) throw Error(j(308));
        (Er = e), (dl.dependencies = { lanes: 0, firstContext: e });
      } else Er = Er.next = e;
    return t;
  }
  var Xt = null;
  function cs(e) {
    Xt === null ? (Xt = [e]) : Xt.push(e);
  }
  function nu(e, t, r, n) {
    var l = t.interleaved;
    return (
      l === null ? ((r.next = r), cs(t)) : ((r.next = l.next), (l.next = r)),
      (t.interleaved = r),
      gt(e, n)
    );
  }
  function gt(e, t) {
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
  var Mt = !1;
  function ds(e) {
    e.updateQueue = {
      baseState: e.memoizedState,
      firstBaseUpdate: null,
      lastBaseUpdate: null,
      shared: { pending: null, interleaved: null, lanes: 0 },
      effects: null,
    };
  }
  function lu(e, t) {
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
  function vt(e, t) {
    return {
      eventTime: e,
      lane: t,
      tag: 0,
      payload: null,
      callback: null,
      next: null,
    };
  }
  function Dt(e, t, r) {
    var n = e.updateQueue;
    if (n === null) return null;
    if (((n = n.shared), $ & 2)) {
      var l = n.pending;
      return (
        l === null ? (t.next = t) : ((t.next = l.next), (l.next = t)),
        (n.pending = t),
        gt(e, r)
      );
    }
    return (
      (l = n.interleaved),
      l === null ? ((t.next = t), cs(n)) : ((t.next = l.next), (l.next = t)),
      (n.interleaved = t),
      gt(e, r)
    );
  }
  function fl(e, t, r) {
    if (
      ((t = t.updateQueue),
      t !== null && ((t = t.shared), (r & 4194240) !== 0))
    ) {
      var n = t.lanes;
      (n &= e.pendingLanes), (r |= n), (t.lanes = r), Ci(e, r);
    }
  }
  function iu(e, t) {
    var r = e.updateQueue,
      n = e.alternate;
    if (n !== null && ((n = n.updateQueue), r === n)) {
      var l = null,
        i = null;
      if (((r = r.firstBaseUpdate), r !== null)) {
        do {
          var a = {
            eventTime: r.eventTime,
            lane: r.lane,
            tag: r.tag,
            payload: r.payload,
            callback: r.callback,
            next: null,
          };
          i === null ? (l = i = a) : (i = i.next = a), (r = r.next);
        } while (r !== null);
        i === null ? (l = i = t) : (i = i.next = t);
      } else l = i = t;
      (r = {
        baseState: n.baseState,
        firstBaseUpdate: l,
        lastBaseUpdate: i,
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
  function pl(e, t, r, n) {
    var l = e.updateQueue;
    Mt = !1;
    var i = l.firstBaseUpdate,
      a = l.lastBaseUpdate,
      u = l.shared.pending;
    if (u !== null) {
      l.shared.pending = null;
      var o = u,
        d = o.next;
      (o.next = null), a === null ? (i = d) : (a.next = d), (a = o);
      var v = e.alternate;
      v !== null &&
        ((v = v.updateQueue),
        (u = v.lastBaseUpdate),
        u !== a &&
          (u === null ? (v.firstBaseUpdate = d) : (u.next = d),
          (v.lastBaseUpdate = o)));
    }
    if (i !== null) {
      var g = l.baseState;
      (a = 0), (v = d = o = null), (u = i);
      do {
        var m = u.lane,
          h = u.eventTime;
        if ((n & m) === m) {
          v !== null &&
            (v = v.next =
              {
                eventTime: h,
                lane: 0,
                tag: u.tag,
                payload: u.payload,
                callback: u.callback,
                next: null,
              });
          e: {
            var y = e,
              k = u;
            switch (((m = t), (h = r), k.tag)) {
              case 1:
                if (((y = k.payload), typeof y == 'function')) {
                  g = y.call(h, g, m);
                  break e;
                }
                g = y;
                break e;
              case 3:
                y.flags = (y.flags & -65537) | 128;
              case 0:
                if (
                  ((y = k.payload),
                  (m = typeof y == 'function' ? y.call(h, g, m) : y),
                  m == null)
                )
                  break e;
                g = Y({}, g, m);
                break e;
              case 2:
                Mt = !0;
            }
          }
          u.callback !== null &&
            u.lane !== 0 &&
            ((e.flags |= 64),
            (m = l.effects),
            m === null ? (l.effects = [u]) : m.push(u));
        } else
          (h = {
            eventTime: h,
            lane: m,
            tag: u.tag,
            payload: u.payload,
            callback: u.callback,
            next: null,
          }),
            v === null ? ((d = v = h), (o = g)) : (v = v.next = h),
            (a |= m);
        if (((u = u.next), u === null)) {
          if (((u = l.shared.pending), u === null)) break;
          (m = u),
            (u = m.next),
            (m.next = null),
            (l.lastBaseUpdate = m),
            (l.shared.pending = null);
        }
      } while (!0);
      if (
        (v === null && (o = g),
        (l.baseState = o),
        (l.firstBaseUpdate = d),
        (l.lastBaseUpdate = v),
        (t = l.shared.interleaved),
        t !== null)
      ) {
        l = t;
        do (a |= l.lane), (l = l.next);
        while (l !== t);
      } else i === null && (l.shared.lanes = 0);
      (qt |= a), (e.lanes = a), (e.memoizedState = g);
    }
  }
  function su(e, t, r) {
    if (((e = t.effects), (t.effects = null), e !== null))
      for (t = 0; t < e.length; t++) {
        var n = e[t],
          l = n.callback;
        if (l !== null) {
          if (((n.callback = null), (n = r), typeof l != 'function'))
            throw Error(j(191, l));
          l.call(n);
        }
      }
  }
  var pn = {},
    it = Pt(pn),
    mn = Pt(pn),
    hn = Pt(pn);
  function Zt(e) {
    if (e === pn) throw Error(j(174));
    return e;
  }
  function fs(e, t) {
    switch ((B(hn, t), B(mn, e), B(it, pn), (e = t.nodeType), e)) {
      case 9:
      case 11:
        t = (t = t.documentElement) ? t.namespaceURI : pi(null, '');
        break;
      default:
        (e = e === 8 ? t.parentNode : t),
          (t = e.namespaceURI || null),
          (e = e.tagName),
          (t = pi(t, e));
    }
    Q(it), B(it, t);
  }
  function Pr() {
    Q(it), Q(mn), Q(hn);
  }
  function au(e) {
    Zt(hn.current);
    var t = Zt(it.current),
      r = pi(t, e.type);
    t !== r && (B(mn, e), B(it, r));
  }
  function ps(e) {
    mn.current === e && (Q(it), Q(mn));
  }
  var G = Pt(0);
  function ml(e) {
    for (var t = e; t !== null; ) {
      if (t.tag === 13) {
        var r = t.memoizedState;
        if (
          r !== null &&
          ((r = r.dehydrated),
          r === null || r.data === '$?' || r.data === '$!')
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
  var ms = [];
  function hs() {
    for (var e = 0; e < ms.length; e++)
      ms[e]._workInProgressVersionPrimary = null;
    ms.length = 0;
  }
  var hl = dt.ReactCurrentDispatcher,
    gs = dt.ReactCurrentBatchConfig,
    Jt = 0,
    X = null,
    re = null,
    se = null,
    gl = !1,
    gn = !1,
    vn = 0,
    _f = 0;
  function he() {
    throw Error(j(321));
  }
  function vs(e, t) {
    if (t === null) return !1;
    for (var r = 0; r < t.length && r < e.length; r++)
      if (!Qe(e[r], t[r])) return !1;
    return !0;
  }
  function xs(e, t, r, n, l, i) {
    if (
      ((Jt = i),
      (X = t),
      (t.memoizedState = null),
      (t.updateQueue = null),
      (t.lanes = 0),
      (hl.current = e === null || e.memoizedState === null ? Lf : Tf),
      (e = r(n, l)),
      gn)
    ) {
      i = 0;
      do {
        if (((gn = !1), (vn = 0), 25 <= i)) throw Error(j(301));
        (i += 1),
          (se = re = null),
          (t.updateQueue = null),
          (hl.current = Mf),
          (e = r(n, l));
      } while (gn);
    }
    if (
      ((hl.current = yl),
      (t = re !== null && re.next !== null),
      (Jt = 0),
      (se = re = X = null),
      (gl = !1),
      t)
    )
      throw Error(j(300));
    return e;
  }
  function ys() {
    var e = vn !== 0;
    return (vn = 0), e;
  }
  function st() {
    var e = {
      memoizedState: null,
      baseState: null,
      baseQueue: null,
      queue: null,
      next: null,
    };
    return se === null ? (X.memoizedState = se = e) : (se = se.next = e), se;
  }
  function Ae() {
    if (re === null) {
      var e = X.alternate;
      e = e !== null ? e.memoizedState : null;
    } else e = re.next;
    var t = se === null ? X.memoizedState : se.next;
    if (t !== null) (se = t), (re = e);
    else {
      if (e === null) throw Error(j(310));
      (re = e),
        (e = {
          memoizedState: re.memoizedState,
          baseState: re.baseState,
          baseQueue: re.baseQueue,
          queue: re.queue,
          next: null,
        }),
        se === null ? (X.memoizedState = se = e) : (se = se.next = e);
    }
    return se;
  }
  function xn(e, t) {
    return typeof t == 'function' ? t(e) : t;
  }
  function ws(e) {
    var t = Ae(),
      r = t.queue;
    if (r === null) throw Error(j(311));
    r.lastRenderedReducer = e;
    var n = re,
      l = n.baseQueue,
      i = r.pending;
    if (i !== null) {
      if (l !== null) {
        var a = l.next;
        (l.next = i.next), (i.next = a);
      }
      (n.baseQueue = l = i), (r.pending = null);
    }
    if (l !== null) {
      (i = l.next), (n = n.baseState);
      var u = (a = null),
        o = null,
        d = i;
      do {
        var v = d.lane;
        if ((Jt & v) === v)
          o !== null &&
            (o = o.next =
              {
                lane: 0,
                action: d.action,
                hasEagerState: d.hasEagerState,
                eagerState: d.eagerState,
                next: null,
              }),
            (n = d.hasEagerState ? d.eagerState : e(n, d.action));
        else {
          var g = {
            lane: v,
            action: d.action,
            hasEagerState: d.hasEagerState,
            eagerState: d.eagerState,
            next: null,
          };
          o === null ? ((u = o = g), (a = n)) : (o = o.next = g),
            (X.lanes |= v),
            (qt |= v);
        }
        d = d.next;
      } while (d !== null && d !== i);
      o === null ? (a = n) : (o.next = u),
        Qe(n, t.memoizedState) || (Ee = !0),
        (t.memoizedState = n),
        (t.baseState = a),
        (t.baseQueue = o),
        (r.lastRenderedState = n);
    }
    if (((e = r.interleaved), e !== null)) {
      l = e;
      do (i = l.lane), (X.lanes |= i), (qt |= i), (l = l.next);
      while (l !== e);
    } else l === null && (r.lanes = 0);
    return [t.memoizedState, r.dispatch];
  }
  function ks(e) {
    var t = Ae(),
      r = t.queue;
    if (r === null) throw Error(j(311));
    r.lastRenderedReducer = e;
    var n = r.dispatch,
      l = r.pending,
      i = t.memoizedState;
    if (l !== null) {
      r.pending = null;
      var a = (l = l.next);
      do (i = e(i, a.action)), (a = a.next);
      while (a !== l);
      Qe(i, t.memoizedState) || (Ee = !0),
        (t.memoizedState = i),
        t.baseQueue === null && (t.baseState = i),
        (r.lastRenderedState = i);
    }
    return [i, n];
  }
  function ou() {}
  function uu(e, t) {
    var r = X,
      n = Ae(),
      l = t(),
      i = !Qe(n.memoizedState, l);
    if (
      (i && ((n.memoizedState = l), (Ee = !0)),
      (n = n.queue),
      Ss(fu.bind(null, r, n, e), [e]),
      n.getSnapshot !== t || i || (se !== null && se.memoizedState.tag & 1))
    ) {
      if (
        ((r.flags |= 2048),
        yn(9, du.bind(null, r, n, l, t), void 0, null),
        ae === null)
      )
        throw Error(j(349));
      Jt & 30 || cu(r, t, l);
    }
    return l;
  }
  function cu(e, t, r) {
    (e.flags |= 16384),
      (e = { getSnapshot: t, value: r }),
      (t = X.updateQueue),
      t === null
        ? ((t = { lastEffect: null, stores: null }),
          (X.updateQueue = t),
          (t.stores = [e]))
        : ((r = t.stores), r === null ? (t.stores = [e]) : r.push(e));
  }
  function du(e, t, r, n) {
    (t.value = r), (t.getSnapshot = n), pu(t) && mu(e);
  }
  function fu(e, t, r) {
    return r(function () {
      pu(t) && mu(e);
    });
  }
  function pu(e) {
    var t = e.getSnapshot;
    e = e.value;
    try {
      var r = t();
      return !Qe(e, r);
    } catch {
      return !0;
    }
  }
  function mu(e) {
    var t = gt(e, 1);
    t !== null && Ze(t, e, 1, -1);
  }
  function hu(e) {
    var t = st();
    return (
      typeof e == 'function' && (e = e()),
      (t.memoizedState = t.baseState = e),
      (e = {
        pending: null,
        interleaved: null,
        lanes: 0,
        dispatch: null,
        lastRenderedReducer: xn,
        lastRenderedState: e,
      }),
      (t.queue = e),
      (e = e.dispatch = Pf.bind(null, X, e)),
      [t.memoizedState, e]
    );
  }
  function yn(e, t, r, n) {
    return (
      (e = { tag: e, create: t, destroy: r, deps: n, next: null }),
      (t = X.updateQueue),
      t === null
        ? ((t = { lastEffect: null, stores: null }),
          (X.updateQueue = t),
          (t.lastEffect = e.next = e))
        : ((r = t.lastEffect),
          r === null
            ? (t.lastEffect = e.next = e)
            : ((n = r.next), (r.next = e), (e.next = n), (t.lastEffect = e))),
      e
    );
  }
  function gu() {
    return Ae().memoizedState;
  }
  function vl(e, t, r, n) {
    var l = st();
    (X.flags |= e),
      (l.memoizedState = yn(1 | t, r, void 0, n === void 0 ? null : n));
  }
  function xl(e, t, r, n) {
    var l = Ae();
    n = n === void 0 ? null : n;
    var i = void 0;
    if (re !== null) {
      var a = re.memoizedState;
      if (((i = a.destroy), n !== null && vs(n, a.deps))) {
        l.memoizedState = yn(t, r, i, n);
        return;
      }
    }
    (X.flags |= e), (l.memoizedState = yn(1 | t, r, i, n));
  }
  function vu(e, t) {
    return vl(8390656, 8, e, t);
  }
  function Ss(e, t) {
    return xl(2048, 8, e, t);
  }
  function xu(e, t) {
    return xl(4, 2, e, t);
  }
  function yu(e, t) {
    return xl(4, 4, e, t);
  }
  function wu(e, t) {
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
  function ku(e, t, r) {
    return (
      (r = r != null ? r.concat([e]) : null), xl(4, 4, wu.bind(null, t, e), r)
    );
  }
  function js() {}
  function Su(e, t) {
    var r = Ae();
    t = t === void 0 ? null : t;
    var n = r.memoizedState;
    return n !== null && t !== null && vs(t, n[1])
      ? n[0]
      : ((r.memoizedState = [e, t]), e);
  }
  function ju(e, t) {
    var r = Ae();
    t = t === void 0 ? null : t;
    var n = r.memoizedState;
    return n !== null && t !== null && vs(t, n[1])
      ? n[0]
      : ((e = e()), (r.memoizedState = [e, t]), e);
  }
  function Nu(e, t, r) {
    return Jt & 21
      ? (Qe(r, t) ||
          ((r = qa()), (X.lanes |= r), (qt |= r), (e.baseState = !0)),
        t)
      : (e.baseState && ((e.baseState = !1), (Ee = !0)),
        (e.memoizedState = r));
  }
  function Ef(e, t) {
    var r = V;
    (V = r !== 0 && 4 > r ? r : 4), e(!0);
    var n = gs.transition;
    gs.transition = {};
    try {
      e(!1), t();
    } finally {
      (V = r), (gs.transition = n);
    }
  }
  function Cu() {
    return Ae().memoizedState;
  }
  function zf(e, t, r) {
    var n = Ft(e);
    if (
      ((r = {
        lane: n,
        action: r,
        hasEagerState: !1,
        eagerState: null,
        next: null,
      }),
      _u(e))
    )
      Eu(t, r);
    else if (((r = nu(e, t, r, n)), r !== null)) {
      var l = Ne();
      Ze(r, e, n, l), zu(r, t, n);
    }
  }
  function Pf(e, t, r) {
    var n = Ft(e),
      l = {
        lane: n,
        action: r,
        hasEagerState: !1,
        eagerState: null,
        next: null,
      };
    if (_u(e)) Eu(t, l);
    else {
      var i = e.alternate;
      if (
        e.lanes === 0 &&
        (i === null || i.lanes === 0) &&
        ((i = t.lastRenderedReducer), i !== null)
      )
        try {
          var a = t.lastRenderedState,
            u = i(a, r);
          if (((l.hasEagerState = !0), (l.eagerState = u), Qe(u, a))) {
            var o = t.interleaved;
            o === null
              ? ((l.next = l), cs(t))
              : ((l.next = o.next), (o.next = l)),
              (t.interleaved = l);
            return;
          }
        } catch {
        } finally {
        }
      (r = nu(e, t, l, n)),
        r !== null && ((l = Ne()), Ze(r, e, n, l), zu(r, t, n));
    }
  }
  function _u(e) {
    var t = e.alternate;
    return e === X || (t !== null && t === X);
  }
  function Eu(e, t) {
    gn = gl = !0;
    var r = e.pending;
    r === null ? (t.next = t) : ((t.next = r.next), (r.next = t)),
      (e.pending = t);
  }
  function zu(e, t, r) {
    if (r & 4194240) {
      var n = t.lanes;
      (n &= e.pendingLanes), (r |= n), (t.lanes = r), Ci(e, r);
    }
  }
  var yl = {
      readContext: $e,
      useCallback: he,
      useContext: he,
      useEffect: he,
      useImperativeHandle: he,
      useInsertionEffect: he,
      useLayoutEffect: he,
      useMemo: he,
      useReducer: he,
      useRef: he,
      useState: he,
      useDebugValue: he,
      useDeferredValue: he,
      useTransition: he,
      useMutableSource: he,
      useSyncExternalStore: he,
      useId: he,
      unstable_isNewReconciler: !1,
    },
    Lf = {
      readContext: $e,
      useCallback: function (e, t) {
        return (st().memoizedState = [e, t === void 0 ? null : t]), e;
      },
      useContext: $e,
      useEffect: vu,
      useImperativeHandle: function (e, t, r) {
        return (
          (r = r != null ? r.concat([e]) : null),
          vl(4194308, 4, wu.bind(null, t, e), r)
        );
      },
      useLayoutEffect: function (e, t) {
        return vl(4194308, 4, e, t);
      },
      useInsertionEffect: function (e, t) {
        return vl(4, 2, e, t);
      },
      useMemo: function (e, t) {
        var r = st();
        return (
          (t = t === void 0 ? null : t),
          (e = e()),
          (r.memoizedState = [e, t]),
          e
        );
      },
      useReducer: function (e, t, r) {
        var n = st();
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
          (e = e.dispatch = zf.bind(null, X, e)),
          [n.memoizedState, e]
        );
      },
      useRef: function (e) {
        var t = st();
        return (e = { current: e }), (t.memoizedState = e);
      },
      useState: hu,
      useDebugValue: js,
      useDeferredValue: function (e) {
        return (st().memoizedState = e);
      },
      useTransition: function () {
        var e = hu(!1),
          t = e[0];
        return (e = Ef.bind(null, e[1])), (st().memoizedState = e), [t, e];
      },
      useMutableSource: function () {},
      useSyncExternalStore: function (e, t, r) {
        var n = X,
          l = st();
        if (K) {
          if (r === void 0) throw Error(j(407));
          r = r();
        } else {
          if (((r = t()), ae === null)) throw Error(j(349));
          Jt & 30 || cu(n, t, r);
        }
        l.memoizedState = r;
        var i = { value: r, getSnapshot: t };
        return (
          (l.queue = i),
          vu(fu.bind(null, n, i, e), [e]),
          (n.flags |= 2048),
          yn(9, du.bind(null, n, i, r, t), void 0, null),
          r
        );
      },
      useId: function () {
        var e = st(),
          t = ae.identifierPrefix;
        if (K) {
          var r = ht,
            n = mt;
          (r = (n & ~(1 << (32 - He(n) - 1))).toString(32) + r),
            (t = ':' + t + 'R' + r),
            (r = vn++),
            0 < r && (t += 'H' + r.toString(32)),
            (t += ':');
        } else (r = _f++), (t = ':' + t + 'r' + r.toString(32) + ':');
        return (e.memoizedState = t);
      },
      unstable_isNewReconciler: !1,
    },
    Tf = {
      readContext: $e,
      useCallback: Su,
      useContext: $e,
      useEffect: Ss,
      useImperativeHandle: ku,
      useInsertionEffect: xu,
      useLayoutEffect: yu,
      useMemo: ju,
      useReducer: ws,
      useRef: gu,
      useState: function () {
        return ws(xn);
      },
      useDebugValue: js,
      useDeferredValue: function (e) {
        var t = Ae();
        return Nu(t, re.memoizedState, e);
      },
      useTransition: function () {
        var e = ws(xn)[0],
          t = Ae().memoizedState;
        return [e, t];
      },
      useMutableSource: ou,
      useSyncExternalStore: uu,
      useId: Cu,
      unstable_isNewReconciler: !1,
    },
    Mf = {
      readContext: $e,
      useCallback: Su,
      useContext: $e,
      useEffect: Ss,
      useImperativeHandle: ku,
      useInsertionEffect: xu,
      useLayoutEffect: yu,
      useMemo: ju,
      useReducer: ks,
      useRef: gu,
      useState: function () {
        return ks(xn);
      },
      useDebugValue: js,
      useDeferredValue: function (e) {
        var t = Ae();
        return re === null
          ? (t.memoizedState = e)
          : Nu(t, re.memoizedState, e);
      },
      useTransition: function () {
        var e = ks(xn)[0],
          t = Ae().memoizedState;
        return [e, t];
      },
      useMutableSource: ou,
      useSyncExternalStore: uu,
      useId: Cu,
      unstable_isNewReconciler: !1,
    };
  function Ye(e, t) {
    if (e && e.defaultProps) {
      (t = Y({}, t)), (e = e.defaultProps);
      for (var r in e) t[r] === void 0 && (t[r] = e[r]);
      return t;
    }
    return t;
  }
  function Ns(e, t, r, n) {
    (t = e.memoizedState),
      (r = r(n, t)),
      (r = r == null ? t : Y({}, t, r)),
      (e.memoizedState = r),
      e.lanes === 0 && (e.updateQueue.baseState = r);
  }
  var wl = {
    isMounted: function (e) {
      return (e = e._reactInternals) ? Ht(e) === e : !1;
    },
    enqueueSetState: function (e, t, r) {
      e = e._reactInternals;
      var n = Ne(),
        l = Ft(e),
        i = vt(n, l);
      (i.payload = t),
        r != null && (i.callback = r),
        (t = Dt(e, i, l)),
        t !== null && (Ze(t, e, l, n), fl(t, e, l));
    },
    enqueueReplaceState: function (e, t, r) {
      e = e._reactInternals;
      var n = Ne(),
        l = Ft(e),
        i = vt(n, l);
      (i.tag = 1),
        (i.payload = t),
        r != null && (i.callback = r),
        (t = Dt(e, i, l)),
        t !== null && (Ze(t, e, l, n), fl(t, e, l));
    },
    enqueueForceUpdate: function (e, t) {
      e = e._reactInternals;
      var r = Ne(),
        n = Ft(e),
        l = vt(r, n);
      (l.tag = 2),
        t != null && (l.callback = t),
        (t = Dt(e, l, n)),
        t !== null && (Ze(t, e, n, r), fl(t, e, n));
    },
  };
  function Pu(e, t, r, n, l, i, a) {
    return (
      (e = e.stateNode),
      typeof e.shouldComponentUpdate == 'function'
        ? e.shouldComponentUpdate(n, i, a)
        : t.prototype && t.prototype.isPureReactComponent
        ? !ln(r, n) || !ln(l, i)
        : !0
    );
  }
  function Lu(e, t, r) {
    var n = !1,
      l = Lt,
      i = t.contextType;
    return (
      typeof i == 'object' && i !== null
        ? (i = $e(i))
        : ((l = _e(t) ? Kt : me.current),
          (n = t.contextTypes),
          (i = (n = n != null) ? Sr(e, l) : Lt)),
      (t = new t(r, i)),
      (e.memoizedState =
        t.state !== null && t.state !== void 0 ? t.state : null),
      (t.updater = wl),
      (e.stateNode = t),
      (t._reactInternals = e),
      n &&
        ((e = e.stateNode),
        (e.__reactInternalMemoizedUnmaskedChildContext = l),
        (e.__reactInternalMemoizedMaskedChildContext = i)),
      t
    );
  }
  function Tu(e, t, r, n) {
    (e = t.state),
      typeof t.componentWillReceiveProps == 'function' &&
        t.componentWillReceiveProps(r, n),
      typeof t.UNSAFE_componentWillReceiveProps == 'function' &&
        t.UNSAFE_componentWillReceiveProps(r, n),
      t.state !== e && wl.enqueueReplaceState(t, t.state, null);
  }
  function Cs(e, t, r, n) {
    var l = e.stateNode;
    (l.props = r), (l.state = e.memoizedState), (l.refs = {}), ds(e);
    var i = t.contextType;
    typeof i == 'object' && i !== null
      ? (l.context = $e(i))
      : ((i = _e(t) ? Kt : me.current), (l.context = Sr(e, i))),
      (l.state = e.memoizedState),
      (i = t.getDerivedStateFromProps),
      typeof i == 'function' && (Ns(e, t, i, r), (l.state = e.memoizedState)),
      typeof t.getDerivedStateFromProps == 'function' ||
        typeof l.getSnapshotBeforeUpdate == 'function' ||
        (typeof l.UNSAFE_componentWillMount != 'function' &&
          typeof l.componentWillMount != 'function') ||
        ((t = l.state),
        typeof l.componentWillMount == 'function' && l.componentWillMount(),
        typeof l.UNSAFE_componentWillMount == 'function' &&
          l.UNSAFE_componentWillMount(),
        t !== l.state && wl.enqueueReplaceState(l, l.state, null),
        pl(e, r, l, n),
        (l.state = e.memoizedState)),
      typeof l.componentDidMount == 'function' && (e.flags |= 4194308);
  }
  function Lr(e, t) {
    try {
      var r = '',
        n = t;
      do (r += id(n)), (n = n.return);
      while (n);
      var l = r;
    } catch (i) {
      l =
        `
Error generating stack: ` +
        i.message +
        `
` +
        i.stack;
    }
    return { value: e, source: t, stack: l, digest: null };
  }
  function _s(e, t, r) {
    return { value: e, source: null, stack: r ?? null, digest: t ?? null };
  }
  function Es(e, t) {
    try {
      console.error(t.value);
    } catch (r) {
      setTimeout(function () {
        throw r;
      });
    }
  }
  var Df = typeof WeakMap == 'function' ? WeakMap : Map;
  function Mu(e, t, r) {
    (r = vt(-1, r)), (r.tag = 3), (r.payload = { element: null });
    var n = t.value;
    return (
      (r.callback = function () {
        El || ((El = !0), (Ws = n)), Es(e, t);
      }),
      r
    );
  }
  function Du(e, t, r) {
    (r = vt(-1, r)), (r.tag = 3);
    var n = e.type.getDerivedStateFromError;
    if (typeof n == 'function') {
      var l = t.value;
      (r.payload = function () {
        return n(l);
      }),
        (r.callback = function () {
          Es(e, t);
        });
    }
    var i = e.stateNode;
    return (
      i !== null &&
        typeof i.componentDidCatch == 'function' &&
        (r.callback = function () {
          Es(e, t),
            typeof n != 'function' &&
              (It === null ? (It = new Set([this])) : It.add(this));
          var a = t.stack;
          this.componentDidCatch(t.value, {
            componentStack: a !== null ? a : '',
          });
        }),
      r
    );
  }
  function Ru(e, t, r) {
    var n = e.pingCache;
    if (n === null) {
      n = e.pingCache = new Df();
      var l = new Set();
      n.set(t, l);
    } else (l = n.get(t)), l === void 0 && ((l = new Set()), n.set(t, l));
    l.has(r) || (l.add(r), (e = Kf.bind(null, e, t, r)), t.then(e, e));
  }
  function Iu(e) {
    do {
      var t;
      if (
        ((t = e.tag === 13) &&
          ((t = e.memoizedState),
          (t = t !== null ? t.dehydrated !== null : !0)),
        t)
      )
        return e;
      e = e.return;
    } while (e !== null);
    return null;
  }
  function bu(e, t, r, n, l) {
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
                : ((t = vt(-1, 1)), (t.tag = 2), Dt(r, t, 1))),
            (r.lanes |= 1)),
        e);
  }
  var Rf = dt.ReactCurrentOwner,
    Ee = !1;
  function je(e, t, r, n) {
    t.child = e === null ? ru(t, null, r, n) : _r(t, e.child, r, n);
  }
  function Fu(e, t, r, n, l) {
    r = r.render;
    var i = t.ref;
    return (
      zr(t, l),
      (n = xs(e, t, r, n, i, l)),
      (r = ys()),
      e !== null && !Ee
        ? ((t.updateQueue = e.updateQueue),
          (t.flags &= -2053),
          (e.lanes &= ~l),
          xt(e, t, l))
        : (K && r && ts(t), (t.flags |= 1), je(e, t, n, l), t.child)
    );
  }
  function Ou(e, t, r, n, l) {
    if (e === null) {
      var i = r.type;
      return typeof i == 'function' &&
        !Gs(i) &&
        i.defaultProps === void 0 &&
        r.compare === null &&
        r.defaultProps === void 0
        ? ((t.tag = 15), (t.type = i), Uu(e, t, i, n, l))
        : ((e = Dl(r.type, null, n, t, t.mode, l)),
          (e.ref = t.ref),
          (e.return = t),
          (t.child = e));
    }
    if (((i = e.child), !(e.lanes & l))) {
      var a = i.memoizedProps;
      if (
        ((r = r.compare),
        (r = r !== null ? r : ln),
        r(a, n) && e.ref === t.ref)
      )
        return xt(e, t, l);
    }
    return (
      (t.flags |= 1),
      (e = Ut(i, n)),
      (e.ref = t.ref),
      (e.return = t),
      (t.child = e)
    );
  }
  function Uu(e, t, r, n, l) {
    if (e !== null) {
      var i = e.memoizedProps;
      if (ln(i, n) && e.ref === t.ref)
        if (((Ee = !1), (t.pendingProps = n = i), (e.lanes & l) !== 0))
          e.flags & 131072 && (Ee = !0);
        else return (t.lanes = e.lanes), xt(e, t, l);
    }
    return zs(e, t, r, n, l);
  }
  function $u(e, t, r) {
    var n = t.pendingProps,
      l = n.children,
      i = e !== null ? e.memoizedState : null;
    if (n.mode === 'hidden')
      if (!(t.mode & 1))
        (t.memoizedState = {
          baseLanes: 0,
          cachePool: null,
          transitions: null,
        }),
          B(Mr, be),
          (be |= r);
      else {
        if (!(r & 1073741824))
          return (
            (e = i !== null ? i.baseLanes | r : r),
            (t.lanes = t.childLanes = 1073741824),
            (t.memoizedState = {
              baseLanes: e,
              cachePool: null,
              transitions: null,
            }),
            (t.updateQueue = null),
            B(Mr, be),
            (be |= e),
            null
          );
        (t.memoizedState = {
          baseLanes: 0,
          cachePool: null,
          transitions: null,
        }),
          (n = i !== null ? i.baseLanes : r),
          B(Mr, be),
          (be |= n);
      }
    else
      i !== null ? ((n = i.baseLanes | r), (t.memoizedState = null)) : (n = r),
        B(Mr, be),
        (be |= n);
    return je(e, t, l, r), t.child;
  }
  function Au(e, t) {
    var r = t.ref;
    ((e === null && r !== null) || (e !== null && e.ref !== r)) &&
      ((t.flags |= 512), (t.flags |= 2097152));
  }
  function zs(e, t, r, n, l) {
    var i = _e(r) ? Kt : me.current;
    return (
      (i = Sr(t, i)),
      zr(t, l),
      (r = xs(e, t, r, n, i, l)),
      (n = ys()),
      e !== null && !Ee
        ? ((t.updateQueue = e.updateQueue),
          (t.flags &= -2053),
          (e.lanes &= ~l),
          xt(e, t, l))
        : (K && n && ts(t), (t.flags |= 1), je(e, t, r, l), t.child)
    );
  }
  function Wu(e, t, r, n, l) {
    if (_e(r)) {
      var i = !0;
      ll(t);
    } else i = !1;
    if ((zr(t, l), t.stateNode === null))
      Sl(e, t), Lu(t, r, n), Cs(t, r, n, l), (n = !0);
    else if (e === null) {
      var a = t.stateNode,
        u = t.memoizedProps;
      a.props = u;
      var o = a.context,
        d = r.contextType;
      typeof d == 'object' && d !== null
        ? (d = $e(d))
        : ((d = _e(r) ? Kt : me.current), (d = Sr(t, d)));
      var v = r.getDerivedStateFromProps,
        g =
          typeof v == 'function' ||
          typeof a.getSnapshotBeforeUpdate == 'function';
      g ||
        (typeof a.UNSAFE_componentWillReceiveProps != 'function' &&
          typeof a.componentWillReceiveProps != 'function') ||
        ((u !== n || o !== d) && Tu(t, a, n, d)),
        (Mt = !1);
      var m = t.memoizedState;
      (a.state = m),
        pl(t, n, a, l),
        (o = t.memoizedState),
        u !== n || m !== o || Ce.current || Mt
          ? (typeof v == 'function' && (Ns(t, r, v, n), (o = t.memoizedState)),
            (u = Mt || Pu(t, r, u, n, m, o, d))
              ? (g ||
                  (typeof a.UNSAFE_componentWillMount != 'function' &&
                    typeof a.componentWillMount != 'function') ||
                  (typeof a.componentWillMount == 'function' &&
                    a.componentWillMount(),
                  typeof a.UNSAFE_componentWillMount == 'function' &&
                    a.UNSAFE_componentWillMount()),
                typeof a.componentDidMount == 'function' &&
                  (t.flags |= 4194308))
              : (typeof a.componentDidMount == 'function' &&
                  (t.flags |= 4194308),
                (t.memoizedProps = n),
                (t.memoizedState = o)),
            (a.props = n),
            (a.state = o),
            (a.context = d),
            (n = u))
          : (typeof a.componentDidMount == 'function' && (t.flags |= 4194308),
            (n = !1));
    } else {
      (a = t.stateNode),
        lu(e, t),
        (u = t.memoizedProps),
        (d = t.type === t.elementType ? u : Ye(t.type, u)),
        (a.props = d),
        (g = t.pendingProps),
        (m = a.context),
        (o = r.contextType),
        typeof o == 'object' && o !== null
          ? (o = $e(o))
          : ((o = _e(r) ? Kt : me.current), (o = Sr(t, o)));
      var h = r.getDerivedStateFromProps;
      (v =
        typeof h == 'function' ||
        typeof a.getSnapshotBeforeUpdate == 'function') ||
        (typeof a.UNSAFE_componentWillReceiveProps != 'function' &&
          typeof a.componentWillReceiveProps != 'function') ||
        ((u !== g || m !== o) && Tu(t, a, n, o)),
        (Mt = !1),
        (m = t.memoizedState),
        (a.state = m),
        pl(t, n, a, l);
      var y = t.memoizedState;
      u !== g || m !== y || Ce.current || Mt
        ? (typeof h == 'function' && (Ns(t, r, h, n), (y = t.memoizedState)),
          (d = Mt || Pu(t, r, d, n, m, y, o) || !1)
            ? (v ||
                (typeof a.UNSAFE_componentWillUpdate != 'function' &&
                  typeof a.componentWillUpdate != 'function') ||
                (typeof a.componentWillUpdate == 'function' &&
                  a.componentWillUpdate(n, y, o),
                typeof a.UNSAFE_componentWillUpdate == 'function' &&
                  a.UNSAFE_componentWillUpdate(n, y, o)),
              typeof a.componentDidUpdate == 'function' && (t.flags |= 4),
              typeof a.getSnapshotBeforeUpdate == 'function' &&
                (t.flags |= 1024))
            : (typeof a.componentDidUpdate != 'function' ||
                (u === e.memoizedProps && m === e.memoizedState) ||
                (t.flags |= 4),
              typeof a.getSnapshotBeforeUpdate != 'function' ||
                (u === e.memoizedProps && m === e.memoizedState) ||
                (t.flags |= 1024),
              (t.memoizedProps = n),
              (t.memoizedState = y)),
          (a.props = n),
          (a.state = y),
          (a.context = o),
          (n = d))
        : (typeof a.componentDidUpdate != 'function' ||
            (u === e.memoizedProps && m === e.memoizedState) ||
            (t.flags |= 4),
          typeof a.getSnapshotBeforeUpdate != 'function' ||
            (u === e.memoizedProps && m === e.memoizedState) ||
            (t.flags |= 1024),
          (n = !1));
    }
    return Ps(e, t, r, n, i, l);
  }
  function Ps(e, t, r, n, l, i) {
    Au(e, t);
    var a = (t.flags & 128) !== 0;
    if (!n && !a) return l && Ko(t, r, !1), xt(e, t, i);
    (n = t.stateNode), (Rf.current = t);
    var u =
      a && typeof r.getDerivedStateFromError != 'function' ? null : n.render();
    return (
      (t.flags |= 1),
      e !== null && a
        ? ((t.child = _r(t, e.child, null, i)), (t.child = _r(t, null, u, i)))
        : je(e, t, u, i),
      (t.memoizedState = n.state),
      l && Ko(t, r, !0),
      t.child
    );
  }
  function Vu(e) {
    var t = e.stateNode;
    t.pendingContext
      ? Ho(e, t.pendingContext, t.pendingContext !== t.context)
      : t.context && Ho(e, t.context, !1),
      fs(e, t.containerInfo);
  }
  function Bu(e, t, r, n, l) {
    return Cr(), is(l), (t.flags |= 256), je(e, t, r, n), t.child;
  }
  var Ls = { dehydrated: null, treeContext: null, retryLane: 0 };
  function Ts(e) {
    return { baseLanes: e, cachePool: null, transitions: null };
  }
  function Hu(e, t, r) {
    var n = t.pendingProps,
      l = G.current,
      i = !1,
      a = (t.flags & 128) !== 0,
      u;
    if (
      ((u = a) ||
        (u = e !== null && e.memoizedState === null ? !1 : (l & 2) !== 0),
      u
        ? ((i = !0), (t.flags &= -129))
        : (e === null || e.memoizedState !== null) && (l |= 1),
      B(G, l & 1),
      e === null)
    )
      return (
        ls(t),
        (e = t.memoizedState),
        e !== null && ((e = e.dehydrated), e !== null)
          ? (t.mode & 1
              ? e.data === '$!'
                ? (t.lanes = 8)
                : (t.lanes = 1073741824)
              : (t.lanes = 1),
            null)
          : ((a = n.children),
            (e = n.fallback),
            i
              ? ((n = t.mode),
                (i = t.child),
                (a = { mode: 'hidden', children: a }),
                !(n & 1) && i !== null
                  ? ((i.childLanes = 0), (i.pendingProps = a))
                  : (i = Rl(a, n, 0, null)),
                (e = nr(e, n, r, null)),
                (i.return = t),
                (e.return = t),
                (i.sibling = e),
                (t.child = i),
                (t.child.memoizedState = Ts(r)),
                (t.memoizedState = Ls),
                e)
              : Ms(t, a))
      );
    if (
      ((l = e.memoizedState), l !== null && ((u = l.dehydrated), u !== null))
    )
      return If(e, t, a, n, u, l, r);
    if (i) {
      (i = n.fallback), (a = t.mode), (l = e.child), (u = l.sibling);
      var o = { mode: 'hidden', children: n.children };
      return (
        !(a & 1) && t.child !== l
          ? ((n = t.child),
            (n.childLanes = 0),
            (n.pendingProps = o),
            (t.deletions = null))
          : ((n = Ut(l, o)), (n.subtreeFlags = l.subtreeFlags & 14680064)),
        u !== null
          ? (i = Ut(u, i))
          : ((i = nr(i, a, r, null)), (i.flags |= 2)),
        (i.return = t),
        (n.return = t),
        (n.sibling = i),
        (t.child = n),
        (n = i),
        (i = t.child),
        (a = e.child.memoizedState),
        (a =
          a === null
            ? Ts(r)
            : {
                baseLanes: a.baseLanes | r,
                cachePool: null,
                transitions: a.transitions,
              }),
        (i.memoizedState = a),
        (i.childLanes = e.childLanes & ~r),
        (t.memoizedState = Ls),
        n
      );
    }
    return (
      (i = e.child),
      (e = i.sibling),
      (n = Ut(i, { mode: 'visible', children: n.children })),
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
  function Ms(e, t) {
    return (
      (t = Rl({ mode: 'visible', children: t }, e.mode, 0, null)),
      (t.return = e),
      (e.child = t)
    );
  }
  function kl(e, t, r, n) {
    return (
      n !== null && is(n),
      _r(t, e.child, null, r),
      (e = Ms(t, t.pendingProps.children)),
      (e.flags |= 2),
      (t.memoizedState = null),
      e
    );
  }
  function If(e, t, r, n, l, i, a) {
    if (r)
      return t.flags & 256
        ? ((t.flags &= -257), (n = _s(Error(j(422)))), kl(e, t, a, n))
        : t.memoizedState !== null
        ? ((t.child = e.child), (t.flags |= 128), null)
        : ((i = n.fallback),
          (l = t.mode),
          (n = Rl({ mode: 'visible', children: n.children }, l, 0, null)),
          (i = nr(i, l, a, null)),
          (i.flags |= 2),
          (n.return = t),
          (i.return = t),
          (n.sibling = i),
          (t.child = n),
          t.mode & 1 && _r(t, e.child, null, a),
          (t.child.memoizedState = Ts(a)),
          (t.memoizedState = Ls),
          i);
    if (!(t.mode & 1)) return kl(e, t, a, null);
    if (l.data === '$!') {
      if (((n = l.nextSibling && l.nextSibling.dataset), n)) var u = n.dgst;
      return (
        (n = u), (i = Error(j(419))), (n = _s(i, n, void 0)), kl(e, t, a, n)
      );
    }
    if (((u = (a & e.childLanes) !== 0), Ee || u)) {
      if (((n = ae), n !== null)) {
        switch (a & -a) {
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
        (l = l & (n.suspendedLanes | a) ? 0 : l),
          l !== 0 &&
            l !== i.retryLane &&
            ((i.retryLane = l), gt(e, l), Ze(n, e, l, -1));
      }
      return Ys(), (n = _s(Error(j(421)))), kl(e, t, a, n);
    }
    return l.data === '$?'
      ? ((t.flags |= 128),
        (t.child = e.child),
        (t = Yf.bind(null, e)),
        (l._reactRetry = t),
        null)
      : ((e = i.treeContext),
        (Ie = zt(l.nextSibling)),
        (Re = t),
        (K = !0),
        (Ke = null),
        e !== null &&
          ((Oe[Ue++] = mt),
          (Oe[Ue++] = ht),
          (Oe[Ue++] = Yt),
          (mt = e.id),
          (ht = e.overflow),
          (Yt = t)),
        (t = Ms(t, n.children)),
        (t.flags |= 4096),
        t);
  }
  function Qu(e, t, r) {
    e.lanes |= t;
    var n = e.alternate;
    n !== null && (n.lanes |= t), us(e.return, t, r);
  }
  function Ds(e, t, r, n, l) {
    var i = e.memoizedState;
    i === null
      ? (e.memoizedState = {
          isBackwards: t,
          rendering: null,
          renderingStartTime: 0,
          last: n,
          tail: r,
          tailMode: l,
        })
      : ((i.isBackwards = t),
        (i.rendering = null),
        (i.renderingStartTime = 0),
        (i.last = n),
        (i.tail = r),
        (i.tailMode = l));
  }
  function Ku(e, t, r) {
    var n = t.pendingProps,
      l = n.revealOrder,
      i = n.tail;
    if ((je(e, t, n.children, r), (n = G.current), n & 2))
      (n = (n & 1) | 2), (t.flags |= 128);
    else {
      if (e !== null && e.flags & 128)
        e: for (e = t.child; e !== null; ) {
          if (e.tag === 13) e.memoizedState !== null && Qu(e, r, t);
          else if (e.tag === 19) Qu(e, r, t);
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
    if ((B(G, n), !(t.mode & 1))) t.memoizedState = null;
    else
      switch (l) {
        case 'forwards':
          for (r = t.child, l = null; r !== null; )
            (e = r.alternate),
              e !== null && ml(e) === null && (l = r),
              (r = r.sibling);
          (r = l),
            r === null
              ? ((l = t.child), (t.child = null))
              : ((l = r.sibling), (r.sibling = null)),
            Ds(t, !1, l, r, i);
          break;
        case 'backwards':
          for (r = null, l = t.child, t.child = null; l !== null; ) {
            if (((e = l.alternate), e !== null && ml(e) === null)) {
              t.child = l;
              break;
            }
            (e = l.sibling), (l.sibling = r), (r = l), (l = e);
          }
          Ds(t, !0, r, null, i);
          break;
        case 'together':
          Ds(t, !1, null, null, void 0);
          break;
        default:
          t.memoizedState = null;
      }
    return t.child;
  }
  function Sl(e, t) {
    !(t.mode & 1) &&
      e !== null &&
      ((e.alternate = null), (t.alternate = null), (t.flags |= 2));
  }
  function xt(e, t, r) {
    if (
      (e !== null && (t.dependencies = e.dependencies),
      (qt |= t.lanes),
      !(r & t.childLanes))
    )
      return null;
    if (e !== null && t.child !== e.child) throw Error(j(153));
    if (t.child !== null) {
      for (
        e = t.child, r = Ut(e, e.pendingProps), t.child = r, r.return = t;
        e.sibling !== null;

      )
        (e = e.sibling),
          (r = r.sibling = Ut(e, e.pendingProps)),
          (r.return = t);
      r.sibling = null;
    }
    return t.child;
  }
  function bf(e, t, r) {
    switch (t.tag) {
      case 3:
        Vu(t), Cr();
        break;
      case 5:
        au(t);
        break;
      case 1:
        _e(t.type) && ll(t);
        break;
      case 4:
        fs(t, t.stateNode.containerInfo);
        break;
      case 10:
        var n = t.type._context,
          l = t.memoizedProps.value;
        B(cl, n._currentValue), (n._currentValue = l);
        break;
      case 13:
        if (((n = t.memoizedState), n !== null))
          return n.dehydrated !== null
            ? (B(G, G.current & 1), (t.flags |= 128), null)
            : r & t.child.childLanes
            ? Hu(e, t, r)
            : (B(G, G.current & 1),
              (e = xt(e, t, r)),
              e !== null ? e.sibling : null);
        B(G, G.current & 1);
        break;
      case 19:
        if (((n = (r & t.childLanes) !== 0), e.flags & 128)) {
          if (n) return Ku(e, t, r);
          t.flags |= 128;
        }
        if (
          ((l = t.memoizedState),
          l !== null &&
            ((l.rendering = null), (l.tail = null), (l.lastEffect = null)),
          B(G, G.current),
          n)
        )
          break;
        return null;
      case 22:
      case 23:
        return (t.lanes = 0), $u(e, t, r);
    }
    return xt(e, t, r);
  }
  var Yu, Rs, Gu, Xu;
  (Yu = function (e, t) {
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
  }),
    (Rs = function () {}),
    (Gu = function (e, t, r, n) {
      var l = e.memoizedProps;
      if (l !== n) {
        (e = t.stateNode), Zt(it.current);
        var i = null;
        switch (r) {
          case 'input':
            (l = ui(e, l)), (n = ui(e, n)), (i = []);
            break;
          case 'select':
            (l = Y({}, l, { value: void 0 })),
              (n = Y({}, n, { value: void 0 })),
              (i = []);
            break;
          case 'textarea':
            (l = fi(e, l)), (n = fi(e, n)), (i = []);
            break;
          default:
            typeof l.onClick != 'function' &&
              typeof n.onClick == 'function' &&
              (e.onclick = tl);
        }
        mi(r, n);
        var a;
        r = null;
        for (d in l)
          if (!n.hasOwnProperty(d) && l.hasOwnProperty(d) && l[d] != null)
            if (d === 'style') {
              var u = l[d];
              for (a in u) u.hasOwnProperty(a) && (r || (r = {}), (r[a] = ''));
            } else
              d !== 'dangerouslySetInnerHTML' &&
                d !== 'children' &&
                d !== 'suppressContentEditableWarning' &&
                d !== 'suppressHydrationWarning' &&
                d !== 'autoFocus' &&
                (Fr.hasOwnProperty(d)
                  ? i || (i = [])
                  : (i = i || []).push(d, null));
        for (d in n) {
          var o = n[d];
          if (
            ((u = l != null ? l[d] : void 0),
            n.hasOwnProperty(d) && o !== u && (o != null || u != null))
          )
            if (d === 'style')
              if (u) {
                for (a in u)
                  !u.hasOwnProperty(a) ||
                    (o && o.hasOwnProperty(a)) ||
                    (r || (r = {}), (r[a] = ''));
                for (a in o)
                  o.hasOwnProperty(a) &&
                    u[a] !== o[a] &&
                    (r || (r = {}), (r[a] = o[a]));
              } else r || (i || (i = []), i.push(d, r)), (r = o);
            else
              d === 'dangerouslySetInnerHTML'
                ? ((o = o ? o.__html : void 0),
                  (u = u ? u.__html : void 0),
                  o != null && u !== o && (i = i || []).push(d, o))
                : d === 'children'
                ? (typeof o != 'string' && typeof o != 'number') ||
                  (i = i || []).push(d, '' + o)
                : d !== 'suppressContentEditableWarning' &&
                  d !== 'suppressHydrationWarning' &&
                  (Fr.hasOwnProperty(d)
                    ? (o != null && d === 'onScroll' && H('scroll', e),
                      i || u === o || (i = []))
                    : (i = i || []).push(d, o));
        }
        r && (i = i || []).push('style', r);
        var d = i;
        (t.updateQueue = d) && (t.flags |= 4);
      }
    }),
    (Xu = function (e, t, r, n) {
      r !== n && (t.flags |= 4);
    });
  function wn(e, t) {
    if (!K)
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
  function ge(e) {
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
  function Ff(e, t, r) {
    var n = t.pendingProps;
    switch ((rs(t), t.tag)) {
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
        return ge(t), null;
      case 1:
        return _e(t.type) && nl(), ge(t), null;
      case 3:
        return (
          (n = t.stateNode),
          Pr(),
          Q(Ce),
          Q(me),
          hs(),
          n.pendingContext &&
            ((n.context = n.pendingContext), (n.pendingContext = null)),
          (e === null || e.child === null) &&
            (ol(t)
              ? (t.flags |= 4)
              : e === null ||
                (e.memoizedState.isDehydrated && !(t.flags & 256)) ||
                ((t.flags |= 1024), Ke !== null && (Hs(Ke), (Ke = null)))),
          Rs(e, t),
          ge(t),
          null
        );
      case 5:
        ps(t);
        var l = Zt(hn.current);
        if (((r = t.type), e !== null && t.stateNode != null))
          Gu(e, t, r, n, l),
            e.ref !== t.ref && ((t.flags |= 512), (t.flags |= 2097152));
        else {
          if (!n) {
            if (t.stateNode === null) throw Error(j(166));
            return ge(t), null;
          }
          if (((e = Zt(it.current)), ol(t))) {
            (n = t.stateNode), (r = t.type);
            var i = t.memoizedProps;
            switch (((n[lt] = t), (n[cn] = i), (e = (t.mode & 1) !== 0), r)) {
              case 'dialog':
                H('cancel', n), H('close', n);
                break;
              case 'iframe':
              case 'object':
              case 'embed':
                H('load', n);
                break;
              case 'video':
              case 'audio':
                for (l = 0; l < an.length; l++) H(an[l], n);
                break;
              case 'source':
                H('error', n);
                break;
              case 'img':
              case 'image':
              case 'link':
                H('error', n), H('load', n);
                break;
              case 'details':
                H('toggle', n);
                break;
              case 'input':
                Pa(n, i), H('invalid', n);
                break;
              case 'select':
                (n._wrapperState = { wasMultiple: !!i.multiple }),
                  H('invalid', n);
                break;
              case 'textarea':
                Ma(n, i), H('invalid', n);
            }
            mi(r, i), (l = null);
            for (var a in i)
              if (i.hasOwnProperty(a)) {
                var u = i[a];
                a === 'children'
                  ? typeof u == 'string'
                    ? n.textContent !== u &&
                      (i.suppressHydrationWarning !== !0 &&
                        el(n.textContent, u, e),
                      (l = ['children', u]))
                    : typeof u == 'number' &&
                      n.textContent !== '' + u &&
                      (i.suppressHydrationWarning !== !0 &&
                        el(n.textContent, u, e),
                      (l = ['children', '' + u]))
                  : Fr.hasOwnProperty(a) &&
                    u != null &&
                    a === 'onScroll' &&
                    H('scroll', n);
              }
            switch (r) {
              case 'input':
                Tn(n), Ta(n, i, !0);
                break;
              case 'textarea':
                Tn(n), Ra(n);
                break;
              case 'select':
              case 'option':
                break;
              default:
                typeof i.onClick == 'function' && (n.onclick = tl);
            }
            (n = l), (t.updateQueue = n), n !== null && (t.flags |= 4);
          } else {
            (a = l.nodeType === 9 ? l : l.ownerDocument),
              e === 'http://www.w3.org/1999/xhtml' && (e = Ia(r)),
              e === 'http://www.w3.org/1999/xhtml'
                ? r === 'script'
                  ? ((e = a.createElement('div')),
                    (e.innerHTML = '<script></script>'),
                    (e = e.removeChild(e.firstChild)))
                  : typeof n.is == 'string'
                  ? (e = a.createElement(r, { is: n.is }))
                  : ((e = a.createElement(r)),
                    r === 'select' &&
                      ((a = e),
                      n.multiple
                        ? (a.multiple = !0)
                        : n.size && (a.size = n.size)))
                : (e = a.createElementNS(e, r)),
              (e[lt] = t),
              (e[cn] = n),
              Yu(e, t, !1, !1),
              (t.stateNode = e);
            e: {
              switch (((a = hi(r, n)), r)) {
                case 'dialog':
                  H('cancel', e), H('close', e), (l = n);
                  break;
                case 'iframe':
                case 'object':
                case 'embed':
                  H('load', e), (l = n);
                  break;
                case 'video':
                case 'audio':
                  for (l = 0; l < an.length; l++) H(an[l], e);
                  l = n;
                  break;
                case 'source':
                  H('error', e), (l = n);
                  break;
                case 'img':
                case 'image':
                case 'link':
                  H('error', e), H('load', e), (l = n);
                  break;
                case 'details':
                  H('toggle', e), (l = n);
                  break;
                case 'input':
                  Pa(e, n), (l = ui(e, n)), H('invalid', e);
                  break;
                case 'option':
                  l = n;
                  break;
                case 'select':
                  (e._wrapperState = { wasMultiple: !!n.multiple }),
                    (l = Y({}, n, { value: void 0 })),
                    H('invalid', e);
                  break;
                case 'textarea':
                  Ma(e, n), (l = fi(e, n)), H('invalid', e);
                  break;
                default:
                  l = n;
              }
              mi(r, l), (u = l);
              for (i in u)
                if (u.hasOwnProperty(i)) {
                  var o = u[i];
                  i === 'style'
                    ? Oa(e, o)
                    : i === 'dangerouslySetInnerHTML'
                    ? ((o = o ? o.__html : void 0), o != null && ba(e, o))
                    : i === 'children'
                    ? typeof o == 'string'
                      ? (r !== 'textarea' || o !== '') && Ar(e, o)
                      : typeof o == 'number' && Ar(e, '' + o)
                    : i !== 'suppressContentEditableWarning' &&
                      i !== 'suppressHydrationWarning' &&
                      i !== 'autoFocus' &&
                      (Fr.hasOwnProperty(i)
                        ? o != null && i === 'onScroll' && H('scroll', e)
                        : o != null && Jl(e, i, o, a));
                }
              switch (r) {
                case 'input':
                  Tn(e), Ta(e, n, !1);
                  break;
                case 'textarea':
                  Tn(e), Ra(e);
                  break;
                case 'option':
                  n.value != null && e.setAttribute('value', '' + kt(n.value));
                  break;
                case 'select':
                  (e.multiple = !!n.multiple),
                    (i = n.value),
                    i != null
                      ? cr(e, !!n.multiple, i, !1)
                      : n.defaultValue != null &&
                        cr(e, !!n.multiple, n.defaultValue, !0);
                  break;
                default:
                  typeof l.onClick == 'function' && (e.onclick = tl);
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
        return ge(t), null;
      case 6:
        if (e && t.stateNode != null) Xu(e, t, e.memoizedProps, n);
        else {
          if (typeof n != 'string' && t.stateNode === null)
            throw Error(j(166));
          if (((r = Zt(hn.current)), Zt(it.current), ol(t))) {
            if (
              ((n = t.stateNode),
              (r = t.memoizedProps),
              (n[lt] = t),
              (i = n.nodeValue !== r) && ((e = Re), e !== null))
            )
              switch (e.tag) {
                case 3:
                  el(n.nodeValue, r, (e.mode & 1) !== 0);
                  break;
                case 5:
                  e.memoizedProps.suppressHydrationWarning !== !0 &&
                    el(n.nodeValue, r, (e.mode & 1) !== 0);
              }
            i && (t.flags |= 4);
          } else
            (n = (r.nodeType === 9 ? r : r.ownerDocument).createTextNode(n)),
              (n[lt] = t),
              (t.stateNode = n);
        }
        return ge(t), null;
      case 13:
        if (
          (Q(G),
          (n = t.memoizedState),
          e === null ||
            (e.memoizedState !== null && e.memoizedState.dehydrated !== null))
        ) {
          if (K && Ie !== null && t.mode & 1 && !(t.flags & 128))
            qo(), Cr(), (t.flags |= 98560), (i = !1);
          else if (((i = ol(t)), n !== null && n.dehydrated !== null)) {
            if (e === null) {
              if (!i) throw Error(j(318));
              if (
                ((i = t.memoizedState),
                (i = i !== null ? i.dehydrated : null),
                !i)
              )
                throw Error(j(317));
              i[lt] = t;
            } else
              Cr(),
                !(t.flags & 128) && (t.memoizedState = null),
                (t.flags |= 4);
            ge(t), (i = !1);
          } else Ke !== null && (Hs(Ke), (Ke = null)), (i = !0);
          if (!i) return t.flags & 65536 ? t : null;
        }
        return t.flags & 128
          ? ((t.lanes = r), t)
          : ((n = n !== null),
            n !== (e !== null && e.memoizedState !== null) &&
              n &&
              ((t.child.flags |= 8192),
              t.mode & 1 &&
                (e === null || G.current & 1 ? ne === 0 && (ne = 3) : Ys())),
            t.updateQueue !== null && (t.flags |= 4),
            ge(t),
            null);
      case 4:
        return (
          Pr(),
          Rs(e, t),
          e === null && on(t.stateNode.containerInfo),
          ge(t),
          null
        );
      case 10:
        return os(t.type._context), ge(t), null;
      case 17:
        return _e(t.type) && nl(), ge(t), null;
      case 19:
        if ((Q(G), (i = t.memoizedState), i === null)) return ge(t), null;
        if (((n = (t.flags & 128) !== 0), (a = i.rendering), a === null))
          if (n) wn(i, !1);
          else {
            if (ne !== 0 || (e !== null && e.flags & 128))
              for (e = t.child; e !== null; ) {
                if (((a = ml(e)), a !== null)) {
                  for (
                    t.flags |= 128,
                      wn(i, !1),
                      n = a.updateQueue,
                      n !== null && ((t.updateQueue = n), (t.flags |= 4)),
                      t.subtreeFlags = 0,
                      n = r,
                      r = t.child;
                    r !== null;

                  )
                    (i = r),
                      (e = n),
                      (i.flags &= 14680066),
                      (a = i.alternate),
                      a === null
                        ? ((i.childLanes = 0),
                          (i.lanes = e),
                          (i.child = null),
                          (i.subtreeFlags = 0),
                          (i.memoizedProps = null),
                          (i.memoizedState = null),
                          (i.updateQueue = null),
                          (i.dependencies = null),
                          (i.stateNode = null))
                        : ((i.childLanes = a.childLanes),
                          (i.lanes = a.lanes),
                          (i.child = a.child),
                          (i.subtreeFlags = 0),
                          (i.deletions = null),
                          (i.memoizedProps = a.memoizedProps),
                          (i.memoizedState = a.memoizedState),
                          (i.updateQueue = a.updateQueue),
                          (i.type = a.type),
                          (e = a.dependencies),
                          (i.dependencies =
                            e === null
                              ? null
                              : {
                                  lanes: e.lanes,
                                  firstContext: e.firstContext,
                                })),
                      (r = r.sibling);
                  return B(G, (G.current & 1) | 2), t.child;
                }
                e = e.sibling;
              }
            i.tail !== null &&
              q() > Dr &&
              ((t.flags |= 128), (n = !0), wn(i, !1), (t.lanes = 4194304));
          }
        else {
          if (!n)
            if (((e = ml(a)), e !== null)) {
              if (
                ((t.flags |= 128),
                (n = !0),
                (r = e.updateQueue),
                r !== null && ((t.updateQueue = r), (t.flags |= 4)),
                wn(i, !0),
                i.tail === null &&
                  i.tailMode === 'hidden' &&
                  !a.alternate &&
                  !K)
              )
                return ge(t), null;
            } else
              2 * q() - i.renderingStartTime > Dr &&
                r !== 1073741824 &&
                ((t.flags |= 128), (n = !0), wn(i, !1), (t.lanes = 4194304));
          i.isBackwards
            ? ((a.sibling = t.child), (t.child = a))
            : ((r = i.last),
              r !== null ? (r.sibling = a) : (t.child = a),
              (i.last = a));
        }
        return i.tail !== null
          ? ((t = i.tail),
            (i.rendering = t),
            (i.tail = t.sibling),
            (i.renderingStartTime = q()),
            (t.sibling = null),
            (r = G.current),
            B(G, n ? (r & 1) | 2 : r & 1),
            t)
          : (ge(t), null);
      case 22:
      case 23:
        return (
          Ks(),
          (n = t.memoizedState !== null),
          e !== null && (e.memoizedState !== null) !== n && (t.flags |= 8192),
          n && t.mode & 1
            ? be & 1073741824 &&
              (ge(t), t.subtreeFlags & 6 && (t.flags |= 8192))
            : ge(t),
          null
        );
      case 24:
        return null;
      case 25:
        return null;
    }
    throw Error(j(156, t.tag));
  }
  function Of(e, t) {
    switch ((rs(t), t.tag)) {
      case 1:
        return (
          _e(t.type) && nl(),
          (e = t.flags),
          e & 65536 ? ((t.flags = (e & -65537) | 128), t) : null
        );
      case 3:
        return (
          Pr(),
          Q(Ce),
          Q(me),
          hs(),
          (e = t.flags),
          e & 65536 && !(e & 128) ? ((t.flags = (e & -65537) | 128), t) : null
        );
      case 5:
        return ps(t), null;
      case 13:
        if (
          (Q(G), (e = t.memoizedState), e !== null && e.dehydrated !== null)
        ) {
          if (t.alternate === null) throw Error(j(340));
          Cr();
        }
        return (
          (e = t.flags), e & 65536 ? ((t.flags = (e & -65537) | 128), t) : null
        );
      case 19:
        return Q(G), null;
      case 4:
        return Pr(), null;
      case 10:
        return os(t.type._context), null;
      case 22:
      case 23:
        return Ks(), null;
      case 24:
        return null;
      default:
        return null;
    }
  }
  var jl = !1,
    ve = !1,
    Uf = typeof WeakSet == 'function' ? WeakSet : Set,
    L = null;
  function Tr(e, t) {
    var r = e.ref;
    if (r !== null)
      if (typeof r == 'function')
        try {
          r(null);
        } catch (n) {
          J(e, t, n);
        }
      else r.current = null;
  }
  function Is(e, t, r) {
    try {
      r();
    } catch (n) {
      J(e, t, n);
    }
  }
  var Zu = !1;
  function $f(e, t) {
    if (((Ki = Vn), (e = Po()), Ui(e))) {
      if ('selectionStart' in e)
        var r = { start: e.selectionStart, end: e.selectionEnd };
      else
        e: {
          r = ((r = e.ownerDocument) && r.defaultView) || window;
          var n = r.getSelection && r.getSelection();
          if (n && n.rangeCount !== 0) {
            r = n.anchorNode;
            var l = n.anchorOffset,
              i = n.focusNode;
            n = n.focusOffset;
            try {
              r.nodeType, i.nodeType;
            } catch {
              r = null;
              break e;
            }
            var a = 0,
              u = -1,
              o = -1,
              d = 0,
              v = 0,
              g = e,
              m = null;
            t: for (;;) {
              for (
                var h;
                g !== r || (l !== 0 && g.nodeType !== 3) || (u = a + l),
                  g !== i || (n !== 0 && g.nodeType !== 3) || (o = a + n),
                  g.nodeType === 3 && (a += g.nodeValue.length),
                  (h = g.firstChild) !== null;

              )
                (m = g), (g = h);
              for (;;) {
                if (g === e) break t;
                if (
                  (m === r && ++d === l && (u = a),
                  m === i && ++v === n && (o = a),
                  (h = g.nextSibling) !== null)
                )
                  break;
                (g = m), (m = g.parentNode);
              }
              g = h;
            }
            r = u === -1 || o === -1 ? null : { start: u, end: o };
          } else r = null;
        }
      r = r || { start: 0, end: 0 };
    } else r = null;
    for (
      Yi = { focusedElem: e, selectionRange: r }, Vn = !1, L = t;
      L !== null;

    )
      if (
        ((t = L), (e = t.child), (t.subtreeFlags & 1028) !== 0 && e !== null)
      )
        (e.return = t), (L = e);
      else
        for (; L !== null; ) {
          t = L;
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
                    var k = y.memoizedProps,
                      M = y.memoizedState,
                      f = t.stateNode,
                      c = f.getSnapshotBeforeUpdate(
                        t.elementType === t.type ? k : Ye(t.type, k),
                        M
                      );
                    f.__reactInternalSnapshotBeforeUpdate = c;
                  }
                  break;
                case 3:
                  var p = t.stateNode.containerInfo;
                  p.nodeType === 1
                    ? (p.textContent = '')
                    : p.nodeType === 9 &&
                      p.documentElement &&
                      p.removeChild(p.documentElement);
                  break;
                case 5:
                case 6:
                case 4:
                case 17:
                  break;
                default:
                  throw Error(j(163));
              }
          } catch (w) {
            J(t, t.return, w);
          }
          if (((e = t.sibling), e !== null)) {
            (e.return = t.return), (L = e);
            break;
          }
          L = t.return;
        }
    return (y = Zu), (Zu = !1), y;
  }
  function kn(e, t, r) {
    var n = t.updateQueue;
    if (((n = n !== null ? n.lastEffect : null), n !== null)) {
      var l = (n = n.next);
      do {
        if ((l.tag & e) === e) {
          var i = l.destroy;
          (l.destroy = void 0), i !== void 0 && Is(t, r, i);
        }
        l = l.next;
      } while (l !== n);
    }
  }
  function Nl(e, t) {
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
  function bs(e) {
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
  function Ju(e) {
    var t = e.alternate;
    t !== null && ((e.alternate = null), Ju(t)),
      (e.child = null),
      (e.deletions = null),
      (e.sibling = null),
      e.tag === 5 &&
        ((t = e.stateNode),
        t !== null &&
          (delete t[lt],
          delete t[cn],
          delete t[Ji],
          delete t[Sf],
          delete t[jf])),
      (e.stateNode = null),
      (e.return = null),
      (e.dependencies = null),
      (e.memoizedProps = null),
      (e.memoizedState = null),
      (e.pendingProps = null),
      (e.stateNode = null),
      (e.updateQueue = null);
  }
  function qu(e) {
    return e.tag === 5 || e.tag === 3 || e.tag === 4;
  }
  function ec(e) {
    e: for (;;) {
      for (; e.sibling === null; ) {
        if (e.return === null || qu(e.return)) return null;
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
  function Fs(e, t, r) {
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
            r != null || t.onclick !== null || (t.onclick = tl));
    else if (n !== 4 && ((e = e.child), e !== null))
      for (Fs(e, t, r), e = e.sibling; e !== null; )
        Fs(e, t, r), (e = e.sibling);
  }
  function Os(e, t, r) {
    var n = e.tag;
    if (n === 5 || n === 6)
      (e = e.stateNode), t ? r.insertBefore(e, t) : r.appendChild(e);
    else if (n !== 4 && ((e = e.child), e !== null))
      for (Os(e, t, r), e = e.sibling; e !== null; )
        Os(e, t, r), (e = e.sibling);
  }
  var ce = null,
    Ge = !1;
  function Rt(e, t, r) {
    for (r = r.child; r !== null; ) tc(e, t, r), (r = r.sibling);
  }
  function tc(e, t, r) {
    if (nt && typeof nt.onCommitFiberUnmount == 'function')
      try {
        nt.onCommitFiberUnmount(Fn, r);
      } catch {}
    switch (r.tag) {
      case 5:
        ve || Tr(r, t);
      case 6:
        var n = ce,
          l = Ge;
        (ce = null),
          Rt(e, t, r),
          (ce = n),
          (Ge = l),
          ce !== null &&
            (Ge
              ? ((e = ce),
                (r = r.stateNode),
                e.nodeType === 8
                  ? e.parentNode.removeChild(r)
                  : e.removeChild(r))
              : ce.removeChild(r.stateNode));
        break;
      case 18:
        ce !== null &&
          (Ge
            ? ((e = ce),
              (r = r.stateNode),
              e.nodeType === 8
                ? Zi(e.parentNode, r)
                : e.nodeType === 1 && Zi(e, r),
              Jr(e))
            : Zi(ce, r.stateNode));
        break;
      case 4:
        (n = ce),
          (l = Ge),
          (ce = r.stateNode.containerInfo),
          (Ge = !0),
          Rt(e, t, r),
          (ce = n),
          (Ge = l);
        break;
      case 0:
      case 11:
      case 14:
      case 15:
        if (
          !ve &&
          ((n = r.updateQueue), n !== null && ((n = n.lastEffect), n !== null))
        ) {
          l = n = n.next;
          do {
            var i = l,
              a = i.destroy;
            (i = i.tag),
              a !== void 0 && (i & 2 || i & 4) && Is(r, t, a),
              (l = l.next);
          } while (l !== n);
        }
        Rt(e, t, r);
        break;
      case 1:
        if (
          !ve &&
          (Tr(r, t),
          (n = r.stateNode),
          typeof n.componentWillUnmount == 'function')
        )
          try {
            (n.props = r.memoizedProps),
              (n.state = r.memoizedState),
              n.componentWillUnmount();
          } catch (u) {
            J(r, t, u);
          }
        Rt(e, t, r);
        break;
      case 21:
        Rt(e, t, r);
        break;
      case 22:
        r.mode & 1
          ? ((ve = (n = ve) || r.memoizedState !== null),
            Rt(e, t, r),
            (ve = n))
          : Rt(e, t, r);
        break;
      default:
        Rt(e, t, r);
    }
  }
  function rc(e) {
    var t = e.updateQueue;
    if (t !== null) {
      e.updateQueue = null;
      var r = e.stateNode;
      r === null && (r = e.stateNode = new Uf()),
        t.forEach(function (n) {
          var l = Gf.bind(null, e, n);
          r.has(n) || (r.add(n), n.then(l, l));
        });
    }
  }
  function Xe(e, t) {
    var r = t.deletions;
    if (r !== null)
      for (var n = 0; n < r.length; n++) {
        var l = r[n];
        try {
          var i = e,
            a = t,
            u = a;
          e: for (; u !== null; ) {
            switch (u.tag) {
              case 5:
                (ce = u.stateNode), (Ge = !1);
                break e;
              case 3:
                (ce = u.stateNode.containerInfo), (Ge = !0);
                break e;
              case 4:
                (ce = u.stateNode.containerInfo), (Ge = !0);
                break e;
            }
            u = u.return;
          }
          if (ce === null) throw Error(j(160));
          tc(i, a, l), (ce = null), (Ge = !1);
          var o = l.alternate;
          o !== null && (o.return = null), (l.return = null);
        } catch (d) {
          J(l, t, d);
        }
      }
    if (t.subtreeFlags & 12854)
      for (t = t.child; t !== null; ) nc(t, e), (t = t.sibling);
  }
  function nc(e, t) {
    var r = e.alternate,
      n = e.flags;
    switch (e.tag) {
      case 0:
      case 11:
      case 14:
      case 15:
        if ((Xe(t, e), at(e), n & 4)) {
          try {
            kn(3, e, e.return), Nl(3, e);
          } catch (k) {
            J(e, e.return, k);
          }
          try {
            kn(5, e, e.return);
          } catch (k) {
            J(e, e.return, k);
          }
        }
        break;
      case 1:
        Xe(t, e), at(e), n & 512 && r !== null && Tr(r, r.return);
        break;
      case 5:
        if (
          (Xe(t, e),
          at(e),
          n & 512 && r !== null && Tr(r, r.return),
          e.flags & 32)
        ) {
          var l = e.stateNode;
          try {
            Ar(l, '');
          } catch (k) {
            J(e, e.return, k);
          }
        }
        if (n & 4 && ((l = e.stateNode), l != null)) {
          var i = e.memoizedProps,
            a = r !== null ? r.memoizedProps : i,
            u = e.type,
            o = e.updateQueue;
          if (((e.updateQueue = null), o !== null))
            try {
              u === 'input' &&
                i.type === 'radio' &&
                i.name != null &&
                La(l, i),
                hi(u, a);
              var d = hi(u, i);
              for (a = 0; a < o.length; a += 2) {
                var v = o[a],
                  g = o[a + 1];
                v === 'style'
                  ? Oa(l, g)
                  : v === 'dangerouslySetInnerHTML'
                  ? ba(l, g)
                  : v === 'children'
                  ? Ar(l, g)
                  : Jl(l, v, g, d);
              }
              switch (u) {
                case 'input':
                  ci(l, i);
                  break;
                case 'textarea':
                  Da(l, i);
                  break;
                case 'select':
                  var m = l._wrapperState.wasMultiple;
                  l._wrapperState.wasMultiple = !!i.multiple;
                  var h = i.value;
                  h != null
                    ? cr(l, !!i.multiple, h, !1)
                    : m !== !!i.multiple &&
                      (i.defaultValue != null
                        ? cr(l, !!i.multiple, i.defaultValue, !0)
                        : cr(l, !!i.multiple, i.multiple ? [] : '', !1));
              }
              l[cn] = i;
            } catch (k) {
              J(e, e.return, k);
            }
        }
        break;
      case 6:
        if ((Xe(t, e), at(e), n & 4)) {
          if (e.stateNode === null) throw Error(j(162));
          (l = e.stateNode), (i = e.memoizedProps);
          try {
            l.nodeValue = i;
          } catch (k) {
            J(e, e.return, k);
          }
        }
        break;
      case 3:
        if (
          (Xe(t, e),
          at(e),
          n & 4 && r !== null && r.memoizedState.isDehydrated)
        )
          try {
            Jr(t.containerInfo);
          } catch (k) {
            J(e, e.return, k);
          }
        break;
      case 4:
        Xe(t, e), at(e);
        break;
      case 13:
        Xe(t, e),
          at(e),
          (l = e.child),
          l.flags & 8192 &&
            ((i = l.memoizedState !== null),
            (l.stateNode.isHidden = i),
            !i ||
              (l.alternate !== null && l.alternate.memoizedState !== null) ||
              (As = q())),
          n & 4 && rc(e);
        break;
      case 22:
        if (
          ((v = r !== null && r.memoizedState !== null),
          e.mode & 1 ? ((ve = (d = ve) || v), Xe(t, e), (ve = d)) : Xe(t, e),
          at(e),
          n & 8192)
        ) {
          if (
            ((d = e.memoizedState !== null),
            (e.stateNode.isHidden = d) && !v && e.mode & 1)
          )
            for (L = e, v = e.child; v !== null; ) {
              for (g = L = v; L !== null; ) {
                switch (((m = L), (h = m.child), m.tag)) {
                  case 0:
                  case 11:
                  case 14:
                  case 15:
                    kn(4, m, m.return);
                    break;
                  case 1:
                    Tr(m, m.return);
                    var y = m.stateNode;
                    if (typeof y.componentWillUnmount == 'function') {
                      (n = m), (r = m.return);
                      try {
                        (t = n),
                          (y.props = t.memoizedProps),
                          (y.state = t.memoizedState),
                          y.componentWillUnmount();
                      } catch (k) {
                        J(n, r, k);
                      }
                    }
                    break;
                  case 5:
                    Tr(m, m.return);
                    break;
                  case 22:
                    if (m.memoizedState !== null) {
                      sc(g);
                      continue;
                    }
                }
                h !== null ? ((h.return = m), (L = h)) : sc(g);
              }
              v = v.sibling;
            }
          e: for (v = null, g = e; ; ) {
            if (g.tag === 5) {
              if (v === null) {
                v = g;
                try {
                  (l = g.stateNode),
                    d
                      ? ((i = l.style),
                        typeof i.setProperty == 'function'
                          ? i.setProperty('display', 'none', 'important')
                          : (i.display = 'none'))
                      : ((u = g.stateNode),
                        (o = g.memoizedProps.style),
                        (a =
                          o != null && o.hasOwnProperty('display')
                            ? o.display
                            : null),
                        (u.style.display = Fa('display', a)));
                } catch (k) {
                  J(e, e.return, k);
                }
              }
            } else if (g.tag === 6) {
              if (v === null)
                try {
                  g.stateNode.nodeValue = d ? '' : g.memoizedProps;
                } catch (k) {
                  J(e, e.return, k);
                }
            } else if (
              ((g.tag !== 22 && g.tag !== 23) ||
                g.memoizedState === null ||
                g === e) &&
              g.child !== null
            ) {
              (g.child.return = g), (g = g.child);
              continue;
            }
            if (g === e) break e;
            for (; g.sibling === null; ) {
              if (g.return === null || g.return === e) break e;
              v === g && (v = null), (g = g.return);
            }
            v === g && (v = null),
              (g.sibling.return = g.return),
              (g = g.sibling);
          }
        }
        break;
      case 19:
        Xe(t, e), at(e), n & 4 && rc(e);
        break;
      case 21:
        break;
      default:
        Xe(t, e), at(e);
    }
  }
  function at(e) {
    var t = e.flags;
    if (t & 2) {
      try {
        e: {
          for (var r = e.return; r !== null; ) {
            if (qu(r)) {
              var n = r;
              break e;
            }
            r = r.return;
          }
          throw Error(j(160));
        }
        switch (n.tag) {
          case 5:
            var l = n.stateNode;
            n.flags & 32 && (Ar(l, ''), (n.flags &= -33));
            var i = ec(e);
            Os(e, i, l);
            break;
          case 3:
          case 4:
            var a = n.stateNode.containerInfo,
              u = ec(e);
            Fs(e, u, a);
            break;
          default:
            throw Error(j(161));
        }
      } catch (o) {
        J(e, e.return, o);
      }
      e.flags &= -3;
    }
    t & 4096 && (e.flags &= -4097);
  }
  function Af(e, t, r) {
    (L = e), lc(e);
  }
  function lc(e, t, r) {
    for (var n = (e.mode & 1) !== 0; L !== null; ) {
      var l = L,
        i = l.child;
      if (l.tag === 22 && n) {
        var a = l.memoizedState !== null || jl;
        if (!a) {
          var u = l.alternate,
            o = (u !== null && u.memoizedState !== null) || ve;
          u = jl;
          var d = ve;
          if (((jl = a), (ve = o) && !d))
            for (L = l; L !== null; )
              (a = L),
                (o = a.child),
                a.tag === 22 && a.memoizedState !== null
                  ? ac(l)
                  : o !== null
                  ? ((o.return = a), (L = o))
                  : ac(l);
          for (; i !== null; ) (L = i), lc(i), (i = i.sibling);
          (L = l), (jl = u), (ve = d);
        }
        ic(e);
      } else
        l.subtreeFlags & 8772 && i !== null
          ? ((i.return = l), (L = i))
          : ic(e);
    }
  }
  function ic(e) {
    for (; L !== null; ) {
      var t = L;
      if (t.flags & 8772) {
        var r = t.alternate;
        try {
          if (t.flags & 8772)
            switch (t.tag) {
              case 0:
              case 11:
              case 15:
                ve || Nl(5, t);
                break;
              case 1:
                var n = t.stateNode;
                if (t.flags & 4 && !ve)
                  if (r === null) n.componentDidMount();
                  else {
                    var l =
                      t.elementType === t.type
                        ? r.memoizedProps
                        : Ye(t.type, r.memoizedProps);
                    n.componentDidUpdate(
                      l,
                      r.memoizedState,
                      n.__reactInternalSnapshotBeforeUpdate
                    );
                  }
                var i = t.updateQueue;
                i !== null && su(t, i, n);
                break;
              case 3:
                var a = t.updateQueue;
                if (a !== null) {
                  if (((r = null), t.child !== null))
                    switch (t.child.tag) {
                      case 5:
                        r = t.child.stateNode;
                        break;
                      case 1:
                        r = t.child.stateNode;
                    }
                  su(t, a, r);
                }
                break;
              case 5:
                var u = t.stateNode;
                if (r === null && t.flags & 4) {
                  r = u;
                  var o = t.memoizedProps;
                  switch (t.type) {
                    case 'button':
                    case 'input':
                    case 'select':
                    case 'textarea':
                      o.autoFocus && r.focus();
                      break;
                    case 'img':
                      o.src && (r.src = o.src);
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
                  var d = t.alternate;
                  if (d !== null) {
                    var v = d.memoizedState;
                    if (v !== null) {
                      var g = v.dehydrated;
                      g !== null && Jr(g);
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
                throw Error(j(163));
            }
          ve || (t.flags & 512 && bs(t));
        } catch (m) {
          J(t, t.return, m);
        }
      }
      if (t === e) {
        L = null;
        break;
      }
      if (((r = t.sibling), r !== null)) {
        (r.return = t.return), (L = r);
        break;
      }
      L = t.return;
    }
  }
  function sc(e) {
    for (; L !== null; ) {
      var t = L;
      if (t === e) {
        L = null;
        break;
      }
      var r = t.sibling;
      if (r !== null) {
        (r.return = t.return), (L = r);
        break;
      }
      L = t.return;
    }
  }
  function ac(e) {
    for (; L !== null; ) {
      var t = L;
      try {
        switch (t.tag) {
          case 0:
          case 11:
          case 15:
            var r = t.return;
            try {
              Nl(4, t);
            } catch (o) {
              J(t, r, o);
            }
            break;
          case 1:
            var n = t.stateNode;
            if (typeof n.componentDidMount == 'function') {
              var l = t.return;
              try {
                n.componentDidMount();
              } catch (o) {
                J(t, l, o);
              }
            }
            var i = t.return;
            try {
              bs(t);
            } catch (o) {
              J(t, i, o);
            }
            break;
          case 5:
            var a = t.return;
            try {
              bs(t);
            } catch (o) {
              J(t, a, o);
            }
        }
      } catch (o) {
        J(t, t.return, o);
      }
      if (t === e) {
        L = null;
        break;
      }
      var u = t.sibling;
      if (u !== null) {
        (u.return = t.return), (L = u);
        break;
      }
      L = t.return;
    }
  }
  var Wf = Math.ceil,
    Cl = dt.ReactCurrentDispatcher,
    Us = dt.ReactCurrentOwner,
    We = dt.ReactCurrentBatchConfig,
    $ = 0,
    ae = null,
    te = null,
    de = 0,
    be = 0,
    Mr = Pt(0),
    ne = 0,
    Sn = null,
    qt = 0,
    _l = 0,
    $s = 0,
    jn = null,
    ze = null,
    As = 0,
    Dr = 1 / 0,
    yt = null,
    El = !1,
    Ws = null,
    It = null,
    zl = !1,
    bt = null,
    Pl = 0,
    Nn = 0,
    Vs = null,
    Ll = -1,
    Tl = 0;
  function Ne() {
    return $ & 6 ? q() : Ll !== -1 ? Ll : (Ll = q());
  }
  function Ft(e) {
    return e.mode & 1
      ? $ & 2 && de !== 0
        ? de & -de
        : Cf.transition !== null
        ? (Tl === 0 && (Tl = qa()), Tl)
        : ((e = V),
          e !== 0 ||
            ((e = window.event), (e = e === void 0 ? 16 : oo(e.type))),
          e)
      : 1;
  }
  function Ze(e, t, r, n) {
    if (50 < Nn) throw ((Nn = 0), (Vs = null), Error(j(185)));
    Kr(e, r, n),
      (!($ & 2) || e !== ae) &&
        (e === ae && (!($ & 2) && (_l |= r), ne === 4 && Ot(e, de)),
        Pe(e, n),
        r === 1 && $ === 0 && !(t.mode & 1) && ((Dr = q() + 500), il && Tt()));
  }
  function Pe(e, t) {
    var r = e.callbackNode;
    Nd(e, t);
    var n = $n(e, e === ae ? de : 0);
    if (n === 0)
      r !== null && Xa(r), (e.callbackNode = null), (e.callbackPriority = 0);
    else if (((t = n & -n), e.callbackPriority !== t)) {
      if ((r != null && Xa(r), t === 1))
        e.tag === 0 ? Nf(uc.bind(null, e)) : Yo(uc.bind(null, e)),
          wf(function () {
            !($ & 6) && Tt();
          }),
          (r = null);
      else {
        switch (eo(n)) {
          case 1:
            r = Si;
            break;
          case 4:
            r = Za;
            break;
          case 16:
            r = bn;
            break;
          case 536870912:
            r = Ja;
            break;
          default:
            r = bn;
        }
        r = vc(r, oc.bind(null, e));
      }
      (e.callbackPriority = t), (e.callbackNode = r);
    }
  }
  function oc(e, t) {
    if (((Ll = -1), (Tl = 0), $ & 6)) throw Error(j(327));
    var r = e.callbackNode;
    if (Rr() && e.callbackNode !== r) return null;
    var n = $n(e, e === ae ? de : 0);
    if (n === 0) return null;
    if (n & 30 || n & e.expiredLanes || t) t = Ml(e, n);
    else {
      t = n;
      var l = $;
      $ |= 2;
      var i = dc();
      (ae !== e || de !== t) && ((yt = null), (Dr = q() + 500), tr(e, t));
      do
        try {
          Hf();
          break;
        } catch (u) {
          cc(e, u);
        }
      while (!0);
      as(),
        (Cl.current = i),
        ($ = l),
        te !== null ? (t = 0) : ((ae = null), (de = 0), (t = ne));
    }
    if (t !== 0) {
      if (
        (t === 2 && ((l = ji(e)), l !== 0 && ((n = l), (t = Bs(e, l)))),
        t === 1)
      )
        throw ((r = Sn), tr(e, 0), Ot(e, n), Pe(e, q()), r);
      if (t === 6) Ot(e, n);
      else {
        if (
          ((l = e.current.alternate),
          !(n & 30) &&
            !Vf(l) &&
            ((t = Ml(e, n)),
            t === 2 && ((i = ji(e)), i !== 0 && ((n = i), (t = Bs(e, i)))),
            t === 1))
        )
          throw ((r = Sn), tr(e, 0), Ot(e, n), Pe(e, q()), r);
        switch (((e.finishedWork = l), (e.finishedLanes = n), t)) {
          case 0:
          case 1:
            throw Error(j(345));
          case 2:
            rr(e, ze, yt);
            break;
          case 3:
            if (
              (Ot(e, n),
              (n & 130023424) === n && ((t = As + 500 - q()), 10 < t))
            ) {
              if ($n(e, 0) !== 0) break;
              if (((l = e.suspendedLanes), (l & n) !== n)) {
                Ne(), (e.pingedLanes |= e.suspendedLanes & l);
                break;
              }
              e.timeoutHandle = Xi(rr.bind(null, e, ze, yt), t);
              break;
            }
            rr(e, ze, yt);
            break;
          case 4:
            if ((Ot(e, n), (n & 4194240) === n)) break;
            for (t = e.eventTimes, l = -1; 0 < n; ) {
              var a = 31 - He(n);
              (i = 1 << a), (a = t[a]), a > l && (l = a), (n &= ~i);
            }
            if (
              ((n = l),
              (n = q() - n),
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
                  : 1960 * Wf(n / 1960)) - n),
              10 < n)
            ) {
              e.timeoutHandle = Xi(rr.bind(null, e, ze, yt), n);
              break;
            }
            rr(e, ze, yt);
            break;
          case 5:
            rr(e, ze, yt);
            break;
          default:
            throw Error(j(329));
        }
      }
    }
    return Pe(e, q()), e.callbackNode === r ? oc.bind(null, e) : null;
  }
  function Bs(e, t) {
    var r = jn;
    return (
      e.current.memoizedState.isDehydrated && (tr(e, t).flags |= 256),
      (e = Ml(e, t)),
      e !== 2 && ((t = ze), (ze = r), t !== null && Hs(t)),
      e
    );
  }
  function Hs(e) {
    ze === null ? (ze = e) : ze.push.apply(ze, e);
  }
  function Vf(e) {
    for (var t = e; ; ) {
      if (t.flags & 16384) {
        var r = t.updateQueue;
        if (r !== null && ((r = r.stores), r !== null))
          for (var n = 0; n < r.length; n++) {
            var l = r[n],
              i = l.getSnapshot;
            l = l.value;
            try {
              if (!Qe(i(), l)) return !1;
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
  function Ot(e, t) {
    for (
      t &= ~$s,
        t &= ~_l,
        e.suspendedLanes |= t,
        e.pingedLanes &= ~t,
        e = e.expirationTimes;
      0 < t;

    ) {
      var r = 31 - He(t),
        n = 1 << r;
      (e[r] = -1), (t &= ~n);
    }
  }
  function uc(e) {
    if ($ & 6) throw Error(j(327));
    Rr();
    var t = $n(e, 0);
    if (!(t & 1)) return Pe(e, q()), null;
    var r = Ml(e, t);
    if (e.tag !== 0 && r === 2) {
      var n = ji(e);
      n !== 0 && ((t = n), (r = Bs(e, n)));
    }
    if (r === 1) throw ((r = Sn), tr(e, 0), Ot(e, t), Pe(e, q()), r);
    if (r === 6) throw Error(j(345));
    return (
      (e.finishedWork = e.current.alternate),
      (e.finishedLanes = t),
      rr(e, ze, yt),
      Pe(e, q()),
      null
    );
  }
  function Qs(e, t) {
    var r = $;
    $ |= 1;
    try {
      return e(t);
    } finally {
      ($ = r), $ === 0 && ((Dr = q() + 500), il && Tt());
    }
  }
  function er(e) {
    bt !== null && bt.tag === 0 && !($ & 6) && Rr();
    var t = $;
    $ |= 1;
    var r = We.transition,
      n = V;
    try {
      if (((We.transition = null), (V = 1), e)) return e();
    } finally {
      (V = n), (We.transition = r), ($ = t), !($ & 6) && Tt();
    }
  }
  function Ks() {
    (be = Mr.current), Q(Mr);
  }
  function tr(e, t) {
    (e.finishedWork = null), (e.finishedLanes = 0);
    var r = e.timeoutHandle;
    if ((r !== -1 && ((e.timeoutHandle = -1), yf(r)), te !== null))
      for (r = te.return; r !== null; ) {
        var n = r;
        switch ((rs(n), n.tag)) {
          case 1:
            (n = n.type.childContextTypes), n != null && nl();
            break;
          case 3:
            Pr(), Q(Ce), Q(me), hs();
            break;
          case 5:
            ps(n);
            break;
          case 4:
            Pr();
            break;
          case 13:
            Q(G);
            break;
          case 19:
            Q(G);
            break;
          case 10:
            os(n.type._context);
            break;
          case 22:
          case 23:
            Ks();
        }
        r = r.return;
      }
    if (
      ((ae = e),
      (te = e = Ut(e.current, null)),
      (de = be = t),
      (ne = 0),
      (Sn = null),
      ($s = _l = qt = 0),
      (ze = jn = null),
      Xt !== null)
    ) {
      for (t = 0; t < Xt.length; t++)
        if (((r = Xt[t]), (n = r.interleaved), n !== null)) {
          r.interleaved = null;
          var l = n.next,
            i = r.pending;
          if (i !== null) {
            var a = i.next;
            (i.next = l), (n.next = a);
          }
          r.pending = n;
        }
      Xt = null;
    }
    return e;
  }
  function cc(e, t) {
    do {
      var r = te;
      try {
        if ((as(), (hl.current = yl), gl)) {
          for (var n = X.memoizedState; n !== null; ) {
            var l = n.queue;
            l !== null && (l.pending = null), (n = n.next);
          }
          gl = !1;
        }
        if (
          ((Jt = 0),
          (se = re = X = null),
          (gn = !1),
          (vn = 0),
          (Us.current = null),
          r === null || r.return === null)
        ) {
          (ne = 1), (Sn = t), (te = null);
          break;
        }
        e: {
          var i = e,
            a = r.return,
            u = r,
            o = t;
          if (
            ((t = de),
            (u.flags |= 32768),
            o !== null && typeof o == 'object' && typeof o.then == 'function')
          ) {
            var d = o,
              v = u,
              g = v.tag;
            if (!(v.mode & 1) && (g === 0 || g === 11 || g === 15)) {
              var m = v.alternate;
              m
                ? ((v.updateQueue = m.updateQueue),
                  (v.memoizedState = m.memoizedState),
                  (v.lanes = m.lanes))
                : ((v.updateQueue = null), (v.memoizedState = null));
            }
            var h = Iu(a);
            if (h !== null) {
              (h.flags &= -257),
                bu(h, a, u, i, t),
                h.mode & 1 && Ru(i, d, t),
                (t = h),
                (o = d);
              var y = t.updateQueue;
              if (y === null) {
                var k = new Set();
                k.add(o), (t.updateQueue = k);
              } else y.add(o);
              break e;
            } else {
              if (!(t & 1)) {
                Ru(i, d, t), Ys();
                break e;
              }
              o = Error(j(426));
            }
          } else if (K && u.mode & 1) {
            var M = Iu(a);
            if (M !== null) {
              !(M.flags & 65536) && (M.flags |= 256),
                bu(M, a, u, i, t),
                is(Lr(o, u));
              break e;
            }
          }
          (i = o = Lr(o, u)),
            ne !== 4 && (ne = 2),
            jn === null ? (jn = [i]) : jn.push(i),
            (i = a);
          do {
            switch (i.tag) {
              case 3:
                (i.flags |= 65536), (t &= -t), (i.lanes |= t);
                var f = Mu(i, o, t);
                iu(i, f);
                break e;
              case 1:
                u = o;
                var c = i.type,
                  p = i.stateNode;
                if (
                  !(i.flags & 128) &&
                  (typeof c.getDerivedStateFromError == 'function' ||
                    (p !== null &&
                      typeof p.componentDidCatch == 'function' &&
                      (It === null || !It.has(p))))
                ) {
                  (i.flags |= 65536), (t &= -t), (i.lanes |= t);
                  var w = Du(i, u, t);
                  iu(i, w);
                  break e;
                }
            }
            i = i.return;
          } while (i !== null);
        }
        pc(r);
      } catch (z) {
        (t = z), te === r && r !== null && (te = r = r.return);
        continue;
      }
      break;
    } while (!0);
  }
  function dc() {
    var e = Cl.current;
    return (Cl.current = yl), e === null ? yl : e;
  }
  function Ys() {
    (ne === 0 || ne === 3 || ne === 2) && (ne = 4),
      ae === null || (!(qt & 268435455) && !(_l & 268435455)) || Ot(ae, de);
  }
  function Ml(e, t) {
    var r = $;
    $ |= 2;
    var n = dc();
    (ae !== e || de !== t) && ((yt = null), tr(e, t));
    do
      try {
        Bf();
        break;
      } catch (l) {
        cc(e, l);
      }
    while (!0);
    if ((as(), ($ = r), (Cl.current = n), te !== null)) throw Error(j(261));
    return (ae = null), (de = 0), ne;
  }
  function Bf() {
    for (; te !== null; ) fc(te);
  }
  function Hf() {
    for (; te !== null && !hd(); ) fc(te);
  }
  function fc(e) {
    var t = gc(e.alternate, e, be);
    (e.memoizedProps = e.pendingProps),
      t === null ? pc(e) : (te = t),
      (Us.current = null);
  }
  function pc(e) {
    var t = e;
    do {
      var r = t.alternate;
      if (((e = t.return), t.flags & 32768)) {
        if (((r = Of(r, t)), r !== null)) {
          (r.flags &= 32767), (te = r);
          return;
        }
        if (e !== null)
          (e.flags |= 32768), (e.subtreeFlags = 0), (e.deletions = null);
        else {
          (ne = 6), (te = null);
          return;
        }
      } else if (((r = Ff(r, t, be)), r !== null)) {
        te = r;
        return;
      }
      if (((t = t.sibling), t !== null)) {
        te = t;
        return;
      }
      te = t = e;
    } while (t !== null);
    ne === 0 && (ne = 5);
  }
  function rr(e, t, r) {
    var n = V,
      l = We.transition;
    try {
      (We.transition = null), (V = 1), Qf(e, t, r, n);
    } finally {
      (We.transition = l), (V = n);
    }
    return null;
  }
  function Qf(e, t, r, n) {
    do Rr();
    while (bt !== null);
    if ($ & 6) throw Error(j(327));
    r = e.finishedWork;
    var l = e.finishedLanes;
    if (r === null) return null;
    if (((e.finishedWork = null), (e.finishedLanes = 0), r === e.current))
      throw Error(j(177));
    (e.callbackNode = null), (e.callbackPriority = 0);
    var i = r.lanes | r.childLanes;
    if (
      (Cd(e, i),
      e === ae && ((te = ae = null), (de = 0)),
      (!(r.subtreeFlags & 2064) && !(r.flags & 2064)) ||
        zl ||
        ((zl = !0),
        vc(bn, function () {
          return Rr(), null;
        })),
      (i = (r.flags & 15990) !== 0),
      r.subtreeFlags & 15990 || i)
    ) {
      (i = We.transition), (We.transition = null);
      var a = V;
      V = 1;
      var u = $;
      ($ |= 4),
        (Us.current = null),
        $f(e, r),
        nc(r, e),
        ff(Yi),
        (Vn = !!Ki),
        (Yi = Ki = null),
        (e.current = r),
        Af(r),
        gd(),
        ($ = u),
        (V = a),
        (We.transition = i);
    } else e.current = r;
    if (
      (zl && ((zl = !1), (bt = e), (Pl = l)),
      (i = e.pendingLanes),
      i === 0 && (It = null),
      yd(r.stateNode),
      Pe(e, q()),
      t !== null)
    )
      for (n = e.onRecoverableError, r = 0; r < t.length; r++)
        (l = t[r]), n(l.value, { componentStack: l.stack, digest: l.digest });
    if (El) throw ((El = !1), (e = Ws), (Ws = null), e);
    return (
      Pl & 1 && e.tag !== 0 && Rr(),
      (i = e.pendingLanes),
      i & 1 ? (e === Vs ? Nn++ : ((Nn = 0), (Vs = e))) : (Nn = 0),
      Tt(),
      null
    );
  }
  function Rr() {
    if (bt !== null) {
      var e = eo(Pl),
        t = We.transition,
        r = V;
      try {
        if (((We.transition = null), (V = 16 > e ? 16 : e), bt === null))
          var n = !1;
        else {
          if (((e = bt), (bt = null), (Pl = 0), $ & 6)) throw Error(j(331));
          var l = $;
          for ($ |= 4, L = e.current; L !== null; ) {
            var i = L,
              a = i.child;
            if (L.flags & 16) {
              var u = i.deletions;
              if (u !== null) {
                for (var o = 0; o < u.length; o++) {
                  var d = u[o];
                  for (L = d; L !== null; ) {
                    var v = L;
                    switch (v.tag) {
                      case 0:
                      case 11:
                      case 15:
                        kn(8, v, i);
                    }
                    var g = v.child;
                    if (g !== null) (g.return = v), (L = g);
                    else
                      for (; L !== null; ) {
                        v = L;
                        var m = v.sibling,
                          h = v.return;
                        if ((Ju(v), v === d)) {
                          L = null;
                          break;
                        }
                        if (m !== null) {
                          (m.return = h), (L = m);
                          break;
                        }
                        L = h;
                      }
                  }
                }
                var y = i.alternate;
                if (y !== null) {
                  var k = y.child;
                  if (k !== null) {
                    y.child = null;
                    do {
                      var M = k.sibling;
                      (k.sibling = null), (k = M);
                    } while (k !== null);
                  }
                }
                L = i;
              }
            }
            if (i.subtreeFlags & 2064 && a !== null) (a.return = i), (L = a);
            else
              e: for (; L !== null; ) {
                if (((i = L), i.flags & 2048))
                  switch (i.tag) {
                    case 0:
                    case 11:
                    case 15:
                      kn(9, i, i.return);
                  }
                var f = i.sibling;
                if (f !== null) {
                  (f.return = i.return), (L = f);
                  break e;
                }
                L = i.return;
              }
          }
          var c = e.current;
          for (L = c; L !== null; ) {
            a = L;
            var p = a.child;
            if (a.subtreeFlags & 2064 && p !== null) (p.return = a), (L = p);
            else
              e: for (a = c; L !== null; ) {
                if (((u = L), u.flags & 2048))
                  try {
                    switch (u.tag) {
                      case 0:
                      case 11:
                      case 15:
                        Nl(9, u);
                    }
                  } catch (z) {
                    J(u, u.return, z);
                  }
                if (u === a) {
                  L = null;
                  break e;
                }
                var w = u.sibling;
                if (w !== null) {
                  (w.return = u.return), (L = w);
                  break e;
                }
                L = u.return;
              }
          }
          if (
            (($ = l),
            Tt(),
            nt && typeof nt.onPostCommitFiberRoot == 'function')
          )
            try {
              nt.onPostCommitFiberRoot(Fn, e);
            } catch {}
          n = !0;
        }
        return n;
      } finally {
        (V = r), (We.transition = t);
      }
    }
    return !1;
  }
  function mc(e, t, r) {
    (t = Lr(r, t)),
      (t = Mu(e, t, 1)),
      (e = Dt(e, t, 1)),
      (t = Ne()),
      e !== null && (Kr(e, 1, t), Pe(e, t));
  }
  function J(e, t, r) {
    if (e.tag === 3) mc(e, e, r);
    else
      for (; t !== null; ) {
        if (t.tag === 3) {
          mc(t, e, r);
          break;
        } else if (t.tag === 1) {
          var n = t.stateNode;
          if (
            typeof t.type.getDerivedStateFromError == 'function' ||
            (typeof n.componentDidCatch == 'function' &&
              (It === null || !It.has(n)))
          ) {
            (e = Lr(r, e)),
              (e = Du(t, e, 1)),
              (t = Dt(t, e, 1)),
              (e = Ne()),
              t !== null && (Kr(t, 1, e), Pe(t, e));
            break;
          }
        }
        t = t.return;
      }
  }
  function Kf(e, t, r) {
    var n = e.pingCache;
    n !== null && n.delete(t),
      (t = Ne()),
      (e.pingedLanes |= e.suspendedLanes & r),
      ae === e &&
        (de & r) === r &&
        (ne === 4 || (ne === 3 && (de & 130023424) === de && 500 > q() - As)
          ? tr(e, 0)
          : ($s |= r)),
      Pe(e, t);
  }
  function hc(e, t) {
    t === 0 &&
      (e.mode & 1
        ? ((t = Un), (Un <<= 1), !(Un & 130023424) && (Un = 4194304))
        : (t = 1));
    var r = Ne();
    (e = gt(e, t)), e !== null && (Kr(e, t, r), Pe(e, r));
  }
  function Yf(e) {
    var t = e.memoizedState,
      r = 0;
    t !== null && (r = t.retryLane), hc(e, r);
  }
  function Gf(e, t) {
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
        throw Error(j(314));
    }
    n !== null && n.delete(t), hc(e, r);
  }
  var gc;
  gc = function (e, t, r) {
    if (e !== null)
      if (e.memoizedProps !== t.pendingProps || Ce.current) Ee = !0;
      else {
        if (!(e.lanes & r) && !(t.flags & 128)) return (Ee = !1), bf(e, t, r);
        Ee = !!(e.flags & 131072);
      }
    else (Ee = !1), K && t.flags & 1048576 && Go(t, al, t.index);
    switch (((t.lanes = 0), t.tag)) {
      case 2:
        var n = t.type;
        Sl(e, t), (e = t.pendingProps);
        var l = Sr(t, me.current);
        zr(t, r), (l = xs(null, t, n, e, l, r));
        var i = ys();
        return (
          (t.flags |= 1),
          typeof l == 'object' &&
          l !== null &&
          typeof l.render == 'function' &&
          l.$$typeof === void 0
            ? ((t.tag = 1),
              (t.memoizedState = null),
              (t.updateQueue = null),
              _e(n) ? ((i = !0), ll(t)) : (i = !1),
              (t.memoizedState =
                l.state !== null && l.state !== void 0 ? l.state : null),
              ds(t),
              (l.updater = wl),
              (t.stateNode = l),
              (l._reactInternals = t),
              Cs(t, n, e, r),
              (t = Ps(null, t, n, !0, i, r)))
            : ((t.tag = 0), K && i && ts(t), je(null, t, l, r), (t = t.child)),
          t
        );
      case 16:
        n = t.elementType;
        e: {
          switch (
            (Sl(e, t),
            (e = t.pendingProps),
            (l = n._init),
            (n = l(n._payload)),
            (t.type = n),
            (l = t.tag = Zf(n)),
            (e = Ye(n, e)),
            l)
          ) {
            case 0:
              t = zs(null, t, n, e, r);
              break e;
            case 1:
              t = Wu(null, t, n, e, r);
              break e;
            case 11:
              t = Fu(null, t, n, e, r);
              break e;
            case 14:
              t = Ou(null, t, n, Ye(n.type, e), r);
              break e;
          }
          throw Error(j(306, n, ''));
        }
        return t;
      case 0:
        return (
          (n = t.type),
          (l = t.pendingProps),
          (l = t.elementType === n ? l : Ye(n, l)),
          zs(e, t, n, l, r)
        );
      case 1:
        return (
          (n = t.type),
          (l = t.pendingProps),
          (l = t.elementType === n ? l : Ye(n, l)),
          Wu(e, t, n, l, r)
        );
      case 3:
        e: {
          if ((Vu(t), e === null)) throw Error(j(387));
          (n = t.pendingProps),
            (i = t.memoizedState),
            (l = i.element),
            lu(e, t),
            pl(t, n, null, r);
          var a = t.memoizedState;
          if (((n = a.element), i.isDehydrated))
            if (
              ((i = {
                element: n,
                isDehydrated: !1,
                cache: a.cache,
                pendingSuspenseBoundaries: a.pendingSuspenseBoundaries,
                transitions: a.transitions,
              }),
              (t.updateQueue.baseState = i),
              (t.memoizedState = i),
              t.flags & 256)
            ) {
              (l = Lr(Error(j(423)), t)), (t = Bu(e, t, n, r, l));
              break e;
            } else if (n !== l) {
              (l = Lr(Error(j(424)), t)), (t = Bu(e, t, n, r, l));
              break e;
            } else
              for (
                Ie = zt(t.stateNode.containerInfo.firstChild),
                  Re = t,
                  K = !0,
                  Ke = null,
                  r = ru(t, null, n, r),
                  t.child = r;
                r;

              )
                (r.flags = (r.flags & -3) | 4096), (r = r.sibling);
          else {
            if ((Cr(), n === l)) {
              t = xt(e, t, r);
              break e;
            }
            je(e, t, n, r);
          }
          t = t.child;
        }
        return t;
      case 5:
        return (
          au(t),
          e === null && ls(t),
          (n = t.type),
          (l = t.pendingProps),
          (i = e !== null ? e.memoizedProps : null),
          (a = l.children),
          Gi(n, l) ? (a = null) : i !== null && Gi(n, i) && (t.flags |= 32),
          Au(e, t),
          je(e, t, a, r),
          t.child
        );
      case 6:
        return e === null && ls(t), null;
      case 13:
        return Hu(e, t, r);
      case 4:
        return (
          fs(t, t.stateNode.containerInfo),
          (n = t.pendingProps),
          e === null ? (t.child = _r(t, null, n, r)) : je(e, t, n, r),
          t.child
        );
      case 11:
        return (
          (n = t.type),
          (l = t.pendingProps),
          (l = t.elementType === n ? l : Ye(n, l)),
          Fu(e, t, n, l, r)
        );
      case 7:
        return je(e, t, t.pendingProps, r), t.child;
      case 8:
        return je(e, t, t.pendingProps.children, r), t.child;
      case 12:
        return je(e, t, t.pendingProps.children, r), t.child;
      case 10:
        e: {
          if (
            ((n = t.type._context),
            (l = t.pendingProps),
            (i = t.memoizedProps),
            (a = l.value),
            B(cl, n._currentValue),
            (n._currentValue = a),
            i !== null)
          )
            if (Qe(i.value, a)) {
              if (i.children === l.children && !Ce.current) {
                t = xt(e, t, r);
                break e;
              }
            } else
              for (i = t.child, i !== null && (i.return = t); i !== null; ) {
                var u = i.dependencies;
                if (u !== null) {
                  a = i.child;
                  for (var o = u.firstContext; o !== null; ) {
                    if (o.context === n) {
                      if (i.tag === 1) {
                        (o = vt(-1, r & -r)), (o.tag = 2);
                        var d = i.updateQueue;
                        if (d !== null) {
                          d = d.shared;
                          var v = d.pending;
                          v === null
                            ? (o.next = o)
                            : ((o.next = v.next), (v.next = o)),
                            (d.pending = o);
                        }
                      }
                      (i.lanes |= r),
                        (o = i.alternate),
                        o !== null && (o.lanes |= r),
                        us(i.return, r, t),
                        (u.lanes |= r);
                      break;
                    }
                    o = o.next;
                  }
                } else if (i.tag === 10)
                  a = i.type === t.type ? null : i.child;
                else if (i.tag === 18) {
                  if (((a = i.return), a === null)) throw Error(j(341));
                  (a.lanes |= r),
                    (u = a.alternate),
                    u !== null && (u.lanes |= r),
                    us(a, r, t),
                    (a = i.sibling);
                } else a = i.child;
                if (a !== null) a.return = i;
                else
                  for (a = i; a !== null; ) {
                    if (a === t) {
                      a = null;
                      break;
                    }
                    if (((i = a.sibling), i !== null)) {
                      (i.return = a.return), (a = i);
                      break;
                    }
                    a = a.return;
                  }
                i = a;
              }
          je(e, t, l.children, r), (t = t.child);
        }
        return t;
      case 9:
        return (
          (l = t.type),
          (n = t.pendingProps.children),
          zr(t, r),
          (l = $e(l)),
          (n = n(l)),
          (t.flags |= 1),
          je(e, t, n, r),
          t.child
        );
      case 14:
        return (
          (n = t.type),
          (l = Ye(n, t.pendingProps)),
          (l = Ye(n.type, l)),
          Ou(e, t, n, l, r)
        );
      case 15:
        return Uu(e, t, t.type, t.pendingProps, r);
      case 17:
        return (
          (n = t.type),
          (l = t.pendingProps),
          (l = t.elementType === n ? l : Ye(n, l)),
          Sl(e, t),
          (t.tag = 1),
          _e(n) ? ((e = !0), ll(t)) : (e = !1),
          zr(t, r),
          Lu(t, n, l),
          Cs(t, n, l, r),
          Ps(null, t, n, !0, e, r)
        );
      case 19:
        return Ku(e, t, r);
      case 22:
        return $u(e, t, r);
    }
    throw Error(j(156, t.tag));
  };
  function vc(e, t) {
    return Ga(e, t);
  }
  function Xf(e, t, r, n) {
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
  function Ve(e, t, r, n) {
    return new Xf(e, t, r, n);
  }
  function Gs(e) {
    return (e = e.prototype), !(!e || !e.isReactComponent);
  }
  function Zf(e) {
    if (typeof e == 'function') return Gs(e) ? 1 : 0;
    if (e != null) {
      if (((e = e.$$typeof), e === ti)) return 11;
      if (e === li) return 14;
    }
    return 2;
  }
  function Ut(e, t) {
    var r = e.alternate;
    return (
      r === null
        ? ((r = Ve(e.tag, t, e.key, e.mode)),
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
  function Dl(e, t, r, n, l, i) {
    var a = 2;
    if (((n = e), typeof e == 'function')) Gs(e) && (a = 1);
    else if (typeof e == 'string') a = 5;
    else
      e: switch (e) {
        case ur:
          return nr(r.children, l, i, t);
        case ql:
          (a = 8), (l |= 8);
          break;
        case ei:
          return (
            (e = Ve(12, r, t, l | 2)), (e.elementType = ei), (e.lanes = i), e
          );
        case ri:
          return (e = Ve(13, r, t, l)), (e.elementType = ri), (e.lanes = i), e;
        case ni:
          return (e = Ve(19, r, t, l)), (e.elementType = ni), (e.lanes = i), e;
        case Ca:
          return Rl(r, l, i, t);
        default:
          if (typeof e == 'object' && e !== null)
            switch (e.$$typeof) {
              case ja:
                a = 10;
                break e;
              case Na:
                a = 9;
                break e;
              case ti:
                a = 11;
                break e;
              case li:
                a = 14;
                break e;
              case wt:
                (a = 16), (n = null);
                break e;
            }
          throw Error(j(130, e == null ? e : typeof e, ''));
      }
    return (
      (t = Ve(a, r, t, l)), (t.elementType = e), (t.type = n), (t.lanes = i), t
    );
  }
  function nr(e, t, r, n) {
    return (e = Ve(7, e, n, t)), (e.lanes = r), e;
  }
  function Rl(e, t, r, n) {
    return (
      (e = Ve(22, e, n, t)),
      (e.elementType = Ca),
      (e.lanes = r),
      (e.stateNode = { isHidden: !1 }),
      e
    );
  }
  function Xs(e, t, r) {
    return (e = Ve(6, e, null, t)), (e.lanes = r), e;
  }
  function Zs(e, t, r) {
    return (
      (t = Ve(4, e.children !== null ? e.children : [], e.key, t)),
      (t.lanes = r),
      (t.stateNode = {
        containerInfo: e.containerInfo,
        pendingChildren: null,
        implementation: e.implementation,
      }),
      t
    );
  }
  function Jf(e, t, r, n, l) {
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
      (this.eventTimes = Ni(0)),
      (this.expirationTimes = Ni(-1)),
      (this.entangledLanes =
        this.finishedLanes =
        this.mutableReadLanes =
        this.expiredLanes =
        this.pingedLanes =
        this.suspendedLanes =
        this.pendingLanes =
          0),
      (this.entanglements = Ni(0)),
      (this.identifierPrefix = n),
      (this.onRecoverableError = l),
      (this.mutableSourceEagerHydrationData = null);
  }
  function Js(e, t, r, n, l, i, a, u, o) {
    return (
      (e = new Jf(e, t, r, u, o)),
      t === 1 ? ((t = 1), i === !0 && (t |= 8)) : (t = 0),
      (i = Ve(3, null, null, t)),
      (e.current = i),
      (i.stateNode = e),
      (i.memoizedState = {
        element: n,
        isDehydrated: r,
        cache: null,
        transitions: null,
        pendingSuspenseBoundaries: null,
      }),
      ds(i),
      e
    );
  }
  function qf(e, t, r) {
    var n =
      3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
    return {
      $$typeof: or,
      key: n == null ? null : '' + n,
      children: e,
      containerInfo: t,
      implementation: r,
    };
  }
  function xc(e) {
    if (!e) return Lt;
    e = e._reactInternals;
    e: {
      if (Ht(e) !== e || e.tag !== 1) throw Error(j(170));
      var t = e;
      do {
        switch (t.tag) {
          case 3:
            t = t.stateNode.context;
            break e;
          case 1:
            if (_e(t.type)) {
              t = t.stateNode.__reactInternalMemoizedMergedChildContext;
              break e;
            }
        }
        t = t.return;
      } while (t !== null);
      throw Error(j(171));
    }
    if (e.tag === 1) {
      var r = e.type;
      if (_e(r)) return Qo(e, r, t);
    }
    return t;
  }
  function yc(e, t, r, n, l, i, a, u, o) {
    return (
      (e = Js(r, n, !0, e, l, i, a, u, o)),
      (e.context = xc(null)),
      (r = e.current),
      (n = Ne()),
      (l = Ft(r)),
      (i = vt(n, l)),
      (i.callback = t ?? null),
      Dt(r, i, l),
      (e.current.lanes = l),
      Kr(e, l, n),
      Pe(e, n),
      e
    );
  }
  function Il(e, t, r, n) {
    var l = t.current,
      i = Ne(),
      a = Ft(l);
    return (
      (r = xc(r)),
      t.context === null ? (t.context = r) : (t.pendingContext = r),
      (t = vt(i, a)),
      (t.payload = { element: e }),
      (n = n === void 0 ? null : n),
      n !== null && (t.callback = n),
      (e = Dt(l, t, a)),
      e !== null && (Ze(e, l, a, i), fl(e, l, a)),
      a
    );
  }
  function bl(e) {
    if (((e = e.current), !e.child)) return null;
    switch (e.child.tag) {
      case 5:
        return e.child.stateNode;
      default:
        return e.child.stateNode;
    }
  }
  function wc(e, t) {
    if (((e = e.memoizedState), e !== null && e.dehydrated !== null)) {
      var r = e.retryLane;
      e.retryLane = r !== 0 && r < t ? r : t;
    }
  }
  function qs(e, t) {
    wc(e, t), (e = e.alternate) && wc(e, t);
  }
  function ep() {
    return null;
  }
  var kc =
    typeof reportError == 'function'
      ? reportError
      : function (e) {
          console.error(e);
        };
  function ea(e) {
    this._internalRoot = e;
  }
  (Fl.prototype.render = ea.prototype.render =
    function (e) {
      var t = this._internalRoot;
      if (t === null) throw Error(j(409));
      Il(e, t, null, null);
    }),
    (Fl.prototype.unmount = ea.prototype.unmount =
      function () {
        var e = this._internalRoot;
        if (e !== null) {
          this._internalRoot = null;
          var t = e.containerInfo;
          er(function () {
            Il(null, e, null, null);
          }),
            (t[ft] = null);
        }
      });
  function Fl(e) {
    this._internalRoot = e;
  }
  Fl.prototype.unstable_scheduleHydration = function (e) {
    if (e) {
      var t = no();
      e = { blockedOn: null, target: e, priority: t };
      for (var r = 0; r < Ct.length && t !== 0 && t < Ct[r].priority; r++);
      Ct.splice(r, 0, e), r === 0 && so(e);
    }
  };
  function ta(e) {
    return !(
      !e ||
      (e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11)
    );
  }
  function Ol(e) {
    return !(
      !e ||
      (e.nodeType !== 1 &&
        e.nodeType !== 9 &&
        e.nodeType !== 11 &&
        (e.nodeType !== 8 || e.nodeValue !== ' react-mount-point-unstable '))
    );
  }
  function Sc() {}
  function tp(e, t, r, n, l) {
    if (l) {
      if (typeof n == 'function') {
        var i = n;
        n = function () {
          var d = bl(a);
          i.call(d);
        };
      }
      var a = yc(t, n, e, 0, null, !1, !1, '', Sc);
      return (
        (e._reactRootContainer = a),
        (e[ft] = a.current),
        on(e.nodeType === 8 ? e.parentNode : e),
        er(),
        a
      );
    }
    for (; (l = e.lastChild); ) e.removeChild(l);
    if (typeof n == 'function') {
      var u = n;
      n = function () {
        var d = bl(o);
        u.call(d);
      };
    }
    var o = Js(e, 0, !1, null, null, !1, !1, '', Sc);
    return (
      (e._reactRootContainer = o),
      (e[ft] = o.current),
      on(e.nodeType === 8 ? e.parentNode : e),
      er(function () {
        Il(t, o, r, n);
      }),
      o
    );
  }
  function Ul(e, t, r, n, l) {
    var i = r._reactRootContainer;
    if (i) {
      var a = i;
      if (typeof l == 'function') {
        var u = l;
        l = function () {
          var o = bl(a);
          u.call(o);
        };
      }
      Il(t, a, e, l);
    } else a = tp(r, t, e, l, n);
    return bl(a);
  }
  (to = function (e) {
    switch (e.tag) {
      case 3:
        var t = e.stateNode;
        if (t.current.memoizedState.isDehydrated) {
          var r = Qr(t.pendingLanes);
          r !== 0 &&
            (Ci(t, r | 1), Pe(t, q()), !($ & 6) && ((Dr = q() + 500), Tt()));
        }
        break;
      case 13:
        er(function () {
          var n = gt(e, 1);
          if (n !== null) {
            var l = Ne();
            Ze(n, e, 1, l);
          }
        }),
          qs(e, 1);
    }
  }),
    (_i = function (e) {
      if (e.tag === 13) {
        var t = gt(e, 134217728);
        if (t !== null) {
          var r = Ne();
          Ze(t, e, 134217728, r);
        }
        qs(e, 134217728);
      }
    }),
    (ro = function (e) {
      if (e.tag === 13) {
        var t = Ft(e),
          r = gt(e, t);
        if (r !== null) {
          var n = Ne();
          Ze(r, e, t, n);
        }
        qs(e, t);
      }
    }),
    (no = function () {
      return V;
    }),
    (lo = function (e, t) {
      var r = V;
      try {
        return (V = e), t();
      } finally {
        V = r;
      }
    }),
    (xi = function (e, t, r) {
      switch (t) {
        case 'input':
          if ((ci(e, r), (t = r.name), r.type === 'radio' && t != null)) {
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
                var l = rl(n);
                if (!l) throw Error(j(90));
                za(n), ci(n, l);
              }
            }
          }
          break;
        case 'textarea':
          Da(e, r);
          break;
        case 'select':
          (t = r.value), t != null && cr(e, !!r.multiple, t, !1);
      }
    }),
    (Wa = Qs),
    (Va = er);
  var rp = { usingClientEntryPoint: !1, Events: [dn, wr, rl, $a, Aa, Qs] },
    Cn = {
      findFiberByHostInstance: Qt,
      bundleType: 0,
      version: '18.3.1',
      rendererPackageName: 'react-dom',
    },
    np = {
      bundleType: Cn.bundleType,
      version: Cn.version,
      rendererPackageName: Cn.rendererPackageName,
      rendererConfig: Cn.rendererConfig,
      overrideHookState: null,
      overrideHookStateDeletePath: null,
      overrideHookStateRenamePath: null,
      overrideProps: null,
      overridePropsDeletePath: null,
      overridePropsRenamePath: null,
      setErrorHandler: null,
      setSuspenseHandler: null,
      scheduleUpdate: null,
      currentDispatcherRef: dt.ReactCurrentDispatcher,
      findHostInstanceByFiber: function (e) {
        return (e = Ka(e)), e === null ? null : e.stateNode;
      },
      findFiberByHostInstance: Cn.findFiberByHostInstance || ep,
      findHostInstancesForRefresh: null,
      scheduleRefresh: null,
      scheduleRoot: null,
      setRefreshHandler: null,
      getCurrentFiber: null,
      reconcilerVersion: '18.3.1-next-f1338f8080-20240426',
    };
  if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < 'u') {
    var $l = __REACT_DEVTOOLS_GLOBAL_HOOK__;
    if (!$l.isDisabled && $l.supportsFiber)
      try {
        (Fn = $l.inject(np)), (nt = $l);
      } catch {}
  }
  (Te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = rp),
    (Te.createPortal = function (e, t) {
      var r =
        2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
      if (!ta(t)) throw Error(j(200));
      return qf(e, t, null, r);
    }),
    (Te.createRoot = function (e, t) {
      if (!ta(e)) throw Error(j(299));
      var r = !1,
        n = '',
        l = kc;
      return (
        t != null &&
          (t.unstable_strictMode === !0 && (r = !0),
          t.identifierPrefix !== void 0 && (n = t.identifierPrefix),
          t.onRecoverableError !== void 0 && (l = t.onRecoverableError)),
        (t = Js(e, 1, !1, null, null, r, !1, n, l)),
        (e[ft] = t.current),
        on(e.nodeType === 8 ? e.parentNode : e),
        new ea(t)
      );
    }),
    (Te.findDOMNode = function (e) {
      if (e == null) return null;
      if (e.nodeType === 1) return e;
      var t = e._reactInternals;
      if (t === void 0)
        throw typeof e.render == 'function'
          ? Error(j(188))
          : ((e = Object.keys(e).join(',')), Error(j(268, e)));
      return (e = Ka(t)), (e = e === null ? null : e.stateNode), e;
    }),
    (Te.flushSync = function (e) {
      return er(e);
    }),
    (Te.hydrate = function (e, t, r) {
      if (!Ol(t)) throw Error(j(200));
      return Ul(null, e, t, !0, r);
    }),
    (Te.hydrateRoot = function (e, t, r) {
      if (!ta(e)) throw Error(j(405));
      var n = (r != null && r.hydratedSources) || null,
        l = !1,
        i = '',
        a = kc;
      if (
        (r != null &&
          (r.unstable_strictMode === !0 && (l = !0),
          r.identifierPrefix !== void 0 && (i = r.identifierPrefix),
          r.onRecoverableError !== void 0 && (a = r.onRecoverableError)),
        (t = yc(t, null, e, 1, r ?? null, l, !1, i, a)),
        (e[ft] = t.current),
        on(e),
        n)
      )
        for (e = 0; e < n.length; e++)
          (r = n[e]),
            (l = r._getVersion),
            (l = l(r._source)),
            t.mutableSourceEagerHydrationData == null
              ? (t.mutableSourceEagerHydrationData = [r, l])
              : t.mutableSourceEagerHydrationData.push(r, l);
      return new Fl(t);
    }),
    (Te.render = function (e, t, r) {
      if (!Ol(t)) throw Error(j(200));
      return Ul(null, e, t, !1, r);
    }),
    (Te.unmountComponentAtNode = function (e) {
      if (!Ol(e)) throw Error(j(40));
      return e._reactRootContainer
        ? (er(function () {
            Ul(null, null, e, !1, function () {
              (e._reactRootContainer = null), (e[ft] = null);
            });
          }),
          !0)
        : !1;
    }),
    (Te.unstable_batchedUpdates = Qs),
    (Te.unstable_renderSubtreeIntoContainer = function (e, t, r, n) {
      if (!Ol(r)) throw Error(j(200));
      if (e == null || e._reactInternals === void 0) throw Error(j(38));
      return Ul(e, t, r, !1, n);
    }),
    (Te.version = '18.3.1-next-f1338f8080-20240426');
  function jc() {
    if (
      !(
        typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > 'u' ||
        typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != 'function'
      )
    )
      try {
        __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(jc);
      } catch (e) {
        console.error(e);
      }
  }
  jc(), (va.exports = Te);
  var lp = va.exports,
    Nc = lp;
  (Yl.createRoot = Nc.createRoot), (Yl.hydrateRoot = Nc.hydrateRoot);
  const Al = ({
      title: e,
      value: t,
      icon: r,
      variant: n = 'default',
      onClick: l,
      clickable: i = !1,
    }) => {
      const a = n === 'default' ? '' : n,
        u = l || i;
      return s.jsxs('div', {
        className: `stat-card ${u ? 'clickable' : ''}`,
        onClick: l,
        style: {
          cursor: u ? 'pointer' : 'default',
          transition: 'transform 0.2s, box-shadow 0.2s',
        },
        onMouseEnter: (o) => {
          u &&
            ((o.currentTarget.style.transform = 'translateY(-2px)'),
            (o.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)'));
        },
        onMouseLeave: (o) => {
          u &&
            ((o.currentTarget.style.transform = 'translateY(0)'),
            (o.currentTarget.style.boxShadow = ''));
        },
        children: [
          s.jsx('div', { className: 'label', children: e }),
          s.jsxs('div', {
            className: `value ${a}`,
            children: [
              r &&
                s.jsx('span', { style: { marginRight: '8px' }, children: r }),
              t,
            ],
          }),
        ],
      });
    },
    Cc = [
      { value: 'all', label: 'All Types', icon: '📱' },
      { value: 'switch', label: 'Switches', icon: '⚡' },
      { value: 'camera', label: 'Cameras', icon: '📹' },
      { value: 'wireless', label: 'Wireless', icon: '📶' },
      { value: 'sensor', label: 'Sensors', icon: '🌡️' },
      { value: 'appliance', label: 'Appliances', icon: '🔒' },
    ],
    ip = [
      { value: 'all', label: 'All Status' },
      { value: 'online', label: 'Online' },
      { value: 'offline', label: 'Offline' },
      { value: 'alerting', label: 'Alerting' },
      { value: 'dormant', label: 'Dormant' },
    ],
    sp = ({
      setActiveView: e,
      data: t,
      hass: r,
      defaultViewMode: n = 'network',
      defaultDeviceTypeFilter: l = 'all',
      defaultStatusFilter: i = 'all',
      temperatureUnit: a = 'celsius',
    }) => {
      const [u, o] = A.useState(new Set()),
        [d, v] = A.useState(
          new Set(['switch', 'camera', 'wireless', 'sensor', 'appliance'])
        ),
        [g, m] = A.useState(l || 'all'),
        [h, y] = A.useState(i || 'all'),
        [k, M] = A.useState(n || 'network'),
        f = A.useRef(!1);
      if (
        (A.useEffect(() => {
          if (!f.current && t != null && t.networks) {
            const N = t.networks.map((T) => T.id);
            N.length > 0 && N.length <= 3 && (o(new Set(N)), (f.current = !0));
          }
        }, [t == null ? void 0 : t.networks]),
        !t)
      )
        return s.jsxs('div', {
          className: 'loading-container',
          children: [
            s.jsx('div', { className: 'loading-spinner' }),
            s.jsx('div', {
              className: 'loading-text',
              children: 'Loading dashboard...',
            }),
          ],
        });
      const {
          devices: c = [],
          networks: p = [],
          ssids: w = [],
          clients: z = [],
          scan_interval: S = 60,
          last_updated: C,
        } = t,
        [P, W] = A.useState(null),
        R = A.useRef(null);
      A.useEffect(() => {
        if (!C || !S) {
          W(null);
          return;
        }
        const N = () => {
          const b = new Date(C).getTime() + S * 1e3,
            ye = Date.now(),
            we = Math.max(0, Math.floor((b - ye) / 1e3));
          W(we);
        };
        return (
          N(),
          (R.current = setInterval(N, 1e3)),
          () => {
            R.current && clearInterval(R.current);
          }
        );
      }, [C, S]);
      const xe = (N) => {
          const T = new Date(N),
            b = new Date();
          return T.toDateString() === b.toDateString()
            ? T.toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
              })
            : T.toLocaleString([], {
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
              });
        },
        fe = (N) =>
          N <= 0
            ? 'refreshing...'
            : N < 60
            ? `${N}s`
            : `${Math.floor(N / 60)}m ${N % 60}s`,
        Le = (N) => {
          var ye, we;
          const T = ((ye = N.model) == null ? void 0 : ye.toUpperCase()) || '',
            b =
              ((we = N.productType) == null ? void 0 : we.toLowerCase()) || '';
          return T.startsWith('MS') || b === 'switch'
            ? 'switch'
            : T.startsWith('MV') || b === 'camera'
            ? 'camera'
            : T.startsWith('MR') || b === 'wireless'
            ? 'wireless'
            : T.startsWith('MT') || b === 'sensor'
            ? 'sensor'
            : T.startsWith('MX') || T.startsWith('Z') || b === 'appliance'
            ? 'appliance'
            : 'all';
        },
        le = ((N) =>
          N.filter((T) => {
            var b;
            return !(
              (g !== 'all' && Le(T) !== g) ||
              (h !== 'all' &&
                ((b = T.status) == null ? void 0 : b.toLowerCase()) !== h)
            );
          }))(c),
        qe = c.filter((N) => {
          var T;
          return (
            ((T = N.status) == null ? void 0 : T.toLowerCase()) === 'online'
          );
        }).length,
        ot = z.length || 0,
        E = w.filter((N) => N.enabled).length,
        D = (N) => {
          o((T) => {
            const b = new Set(T);
            return b.has(N) ? b.delete(N) : b.add(N), b;
          });
        },
        I = (N) => {
          v((T) => {
            const b = new Set(T);
            return b.has(N) ? b.delete(N) : b.add(N), b;
          });
        },
        U = (N) => {
          const T = Le(N);
          return {
            switch: '⚡',
            camera: '📹',
            wireless: '📶',
            sensor: '🌡️',
            appliance: '🔒',
            all: '📱',
          }[T];
        },
        Z = (N) => Le(N),
        $t = (N) => {
          var b, ye, we;
          const T = Le(N);
          if (T === 'switch')
            return `${
              ((b = N.ports_statuses) == null
                ? void 0
                : b.filter((Be) => {
                    var At;
                    return (
                      ((At = Be.status) == null
                        ? void 0
                        : At.toLowerCase()) === 'connected'
                    );
                  }).length) || 0
            } ports active`;
          if (T === 'camera')
            return ((ye = N.status) == null ? void 0 : ye.toLowerCase()) ===
              'online'
              ? 'Recording'
              : 'Offline';
          if (T === 'wireless')
            return `${
              z.filter((Be) => Be.recentDeviceSerial === N.serial).length
            } clients`;
          if (T === 'sensor') {
            if (
              ((we = N.readings) == null ? void 0 : we.temperature) != null
            ) {
              const ie = N.readings.temperature,
                Be =
                  a === 'fahrenheit'
                    ? ((ie * 9) / 5 + 32).toFixed(1)
                    : ie.toFixed(1),
                At = a === 'fahrenheit' ? '°F' : '°C',
                Ir = N.readings.humidity ?? '--';
              return `${Be}${At} / ${Ir}%`;
            }
            return 'Active';
          }
          return '';
        },
        oe = (N) => le.filter((T) => T.networkId === N),
        O = (N) => w.filter((T) => T.networkId === N),
        ee = (N) => le.filter((T) => Le(T) === N),
        et = async (N) => {
          if (!(!(r != null && r.callService) || !N.entity_id))
            try {
              await r.callService(
                'switch',
                N.enabled ? 'turn_off' : 'turn_on',
                { entity_id: N.entity_id }
              );
            } catch (T) {
              console.error('Failed to toggle SSID:', T);
            }
        },
        _n = (N) =>
          s.jsxs('table', {
            className: 'device-table',
            children: [
              s.jsx('thead', {
                children: s.jsxs('tr', {
                  children: [
                    s.jsx('th', { children: 'Device' }),
                    s.jsx('th', { children: 'Model' }),
                    s.jsx('th', { children: 'Status' }),
                    s.jsx('th', { children: 'IP Address' }),
                    s.jsx('th', { children: 'Details' }),
                  ],
                }),
              }),
              s.jsxs('tbody', {
                children: [
                  N.map((T) => {
                    var b;
                    return s.jsxs(
                      'tr',
                      {
                        className: 'device-row',
                        onClick: () =>
                          e({ view: 'device', deviceId: T.serial }),
                        children: [
                          s.jsx('td', {
                            children: s.jsxs('div', {
                              className: 'device-name-cell',
                              children: [
                                s.jsx('div', {
                                  className: `device-icon ${Z(T)}`,
                                  children: U(T),
                                }),
                                s.jsx('span', {
                                  className: 'name',
                                  children: T.name || T.serial,
                                }),
                              ],
                            }),
                          }),
                          s.jsx('td', {
                            className: 'device-model',
                            children: T.model || '—',
                          }),
                          s.jsx('td', {
                            children: s.jsxs('div', {
                              className: `status-badge ${
                                (b = T.status) == null
                                  ? void 0
                                  : b.toLowerCase()
                              }`,
                              children: [
                                s.jsx('div', { className: 'status-dot' }),
                                s.jsx('span', {
                                  children: T.status || 'Unknown',
                                }),
                              ],
                            }),
                          }),
                          s.jsx('td', {
                            className: 'device-model',
                            children: T.lanIp || '—',
                          }),
                          s.jsx('td', {
                            children: s.jsx('span', {
                              className: 'detail-badge',
                              children: $t(T) || '—',
                            }),
                          }),
                        ],
                      },
                      T.serial
                    );
                  }),
                  N.length === 0 &&
                    s.jsx('tr', {
                      children: s.jsx('td', {
                        colSpan: 5,
                        style: {
                          textAlign: 'center',
                          color: 'var(--text-muted)',
                        },
                        children: 'No devices match your filters',
                      }),
                    }),
                ],
              }),
            ],
          });
      return s.jsxs('div', {
        children: [
          C &&
            s.jsxs('div', {
              style: {
                display: 'flex',
                justifyContent: 'flex-end',
                alignItems: 'center',
                gap: '16px',
                marginBottom: '12px',
                fontSize: '12px',
                color: 'var(--text-muted)',
                opacity: 0.8,
              },
              children: [
                s.jsxs('span', {
                  style: { display: 'flex', alignItems: 'center', gap: '4px' },
                  children: [
                    s.jsx('span', {
                      style: { fontSize: '10px' },
                      children: '🔄',
                    }),
                    'Last: ',
                    xe(C),
                  ],
                }),
                P !== null &&
                  s.jsxs('span', {
                    style: {
                      display: 'flex',
                      alignItems: 'center',
                      gap: '4px',
                    },
                    children: [
                      s.jsx('span', {
                        style: { fontSize: '10px' },
                        children: '⏱️',
                      }),
                      'Next: ',
                      fe(P),
                    ],
                  }),
              ],
            }),
          s.jsxs('div', {
            className: 'stats-grid',
            children: [
              s.jsx(Al, { title: 'Total Devices', value: c.length }),
              s.jsx(Al, { title: 'Online', value: qe, variant: 'success' }),
              s.jsx(Al, {
                title: 'Connected Clients',
                value: ot,
                onClick: () => e({ view: 'clients' }),
                clickable: !0,
              }),
              s.jsx(Al, { title: 'Active SSIDs', value: E }),
            ],
          }),
          s.jsxs('div', {
            className: 'filter-controls',
            children: [
              s.jsxs('div', {
                className: 'view-mode-toggle',
                style: {
                  display: 'flex',
                  gap: '4px',
                  background: 'var(--bg-secondary)',
                  borderRadius: 'var(--radius-md)',
                  padding: '4px',
                },
                children: [
                  s.jsx('button', {
                    onClick: () => M('network'),
                    style: {
                      padding: '8px 16px',
                      borderRadius: 'var(--radius-sm)',
                      border: 'none',
                      background:
                        k === 'network' ? 'var(--primary)' : 'transparent',
                      color:
                        k === 'network' ? 'white' : 'var(--text-secondary)',
                      cursor: 'pointer',
                      fontWeight: 500,
                      fontSize: '13px',
                    },
                    children: '🌐 By Network',
                  }),
                  s.jsx('button', {
                    onClick: () => M('type'),
                    style: {
                      padding: '8px 16px',
                      borderRadius: 'var(--radius-sm)',
                      border: 'none',
                      background:
                        k === 'type' ? 'var(--primary)' : 'transparent',
                      color: k === 'type' ? 'white' : 'var(--text-secondary)',
                      cursor: 'pointer',
                      fontWeight: 500,
                      fontSize: '13px',
                    },
                    children: '📦 By Type',
                  }),
                ],
              }),
              s.jsx('select', {
                value: g,
                onChange: (N) => m(N.target.value),
                style: {
                  padding: '8px 12px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border)',
                  background: 'var(--bg-secondary)',
                  color: 'var(--text-primary)',
                  fontSize: '13px',
                  cursor: 'pointer',
                },
                children: Cc.map((N) =>
                  s.jsxs(
                    'option',
                    { value: N.value, children: [N.icon, ' ', N.label] },
                    N.value
                  )
                ),
              }),
              s.jsx('select', {
                value: h,
                onChange: (N) => y(N.target.value),
                style: {
                  padding: '8px 12px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border)',
                  background: 'var(--bg-secondary)',
                  color: 'var(--text-primary)',
                  fontSize: '13px',
                  cursor: 'pointer',
                },
                children: ip.map((N) =>
                  s.jsx(
                    'option',
                    { value: N.value, children: N.label },
                    N.value
                  )
                ),
              }),
              (g !== 'all' || h !== 'all') &&
                s.jsxs('button', {
                  onClick: () => {
                    m('all'), y('all');
                  },
                  style: {
                    padding: '8px 12px',
                    borderRadius: 'var(--radius-md)',
                    border: 'none',
                    background: 'var(--warning)',
                    color: 'white',
                    fontSize: '12px',
                    cursor: 'pointer',
                    fontWeight: 500,
                  },
                  children: [
                    '✕ Clear Filters (',
                    le.length,
                    '/',
                    c.length,
                    ')',
                  ],
                }),
            ],
          }),
          k === 'network' &&
            p.map((N) => {
              const T = oe(N.id),
                b = O(N.id),
                ye = T.filter((ie) => {
                  var Be;
                  return (
                    ((Be = ie.status) == null ? void 0 : Be.toLowerCase()) ===
                    'online'
                  );
                }).length,
                we = u.has(N.id);
              return s.jsxs(
                'div',
                {
                  className: 'network-card',
                  children: [
                    s.jsxs('div', {
                      className: 'network-header',
                      onClick: () => D(N.id),
                      children: [
                        s.jsxs('div', {
                          className: 'title',
                          children: [
                            s.jsx('span', {
                              className: 'network-icon',
                              children: '🌐',
                            }),
                            s.jsx('h2', { children: N.name }),
                            s.jsxs('span', {
                              className: 'badge',
                              children: [ye, '/', T.length, ' online'],
                            }),
                          ],
                        }),
                        s.jsx('span', {
                          className: `expand-icon ${we ? 'expanded' : ''}`,
                          children: '▼',
                        }),
                      ],
                    }),
                    we &&
                      s.jsxs(s.Fragment, {
                        children: [
                          _n(T),
                          b.length > 0 &&
                            s.jsxs('div', {
                              className: 'ssid-section',
                              children: [
                                s.jsxs('h3', {
                                  children: [
                                    s.jsx('span', { children: '📶' }),
                                    'Wireless Networks',
                                  ],
                                }),
                                s.jsx('div', {
                                  className: 'ssid-list',
                                  children: b.map((ie) =>
                                    s.jsxs(
                                      'div',
                                      {
                                        className: 'ssid-item',
                                        children: [
                                          s.jsx('span', {
                                            className: 'icon',
                                            children: ie.enabled ? '🔒' : '📶',
                                          }),
                                          s.jsx('span', {
                                            className: 'name',
                                            children: ie.name,
                                          }),
                                          s.jsx('span', {
                                            className: 'clients',
                                            children: '— clients',
                                          }),
                                          s.jsx('div', {
                                            className: `toggle ${
                                              ie.enabled ? 'active' : ''
                                            }`,
                                            onClick: (Be) => {
                                              Be.stopPropagation(), et(ie);
                                            },
                                          }),
                                        ],
                                      },
                                      `${ie.networkId}-${ie.number}`
                                    )
                                  ),
                                }),
                              ],
                            }),
                        ],
                      }),
                  ],
                },
                N.id
              );
            }),
          k === 'type' &&
            Cc.filter((N) => N.value !== 'all').map((N) => {
              const T = ee(N.value);
              if (T.length === 0 && g !== 'all') return null;
              const b = T.filter((we) => {
                  var ie;
                  return (
                    ((ie = we.status) == null ? void 0 : ie.toLowerCase()) ===
                    'online'
                  );
                }).length,
                ye = d.has(N.value);
              return s.jsxs(
                'div',
                {
                  className: 'network-card',
                  children: [
                    s.jsxs('div', {
                      className: 'network-header',
                      onClick: () => I(N.value),
                      children: [
                        s.jsxs('div', {
                          className: 'title',
                          children: [
                            s.jsx('span', {
                              className: 'network-icon',
                              children: N.icon,
                            }),
                            s.jsx('h2', { children: N.label }),
                            s.jsxs('span', {
                              className: 'badge',
                              children: [b, '/', T.length, ' online'],
                            }),
                          ],
                        }),
                        s.jsx('span', {
                          className: `expand-icon ${ye ? 'expanded' : ''}`,
                          children: '▼',
                        }),
                      ],
                    }),
                    ye && _n(T),
                  ],
                },
                N.value
              );
            }),
          k === 'network' &&
            p.length === 0 &&
            le.length > 0 &&
            s.jsxs('div', {
              className: 'network-card',
              children: [
                s.jsx('div', {
                  className: 'network-header',
                  children: s.jsxs('div', {
                    className: 'title',
                    children: [
                      s.jsx('span', {
                        className: 'network-icon',
                        children: '🌐',
                      }),
                      s.jsx('h2', { children: 'All Devices' }),
                      s.jsxs('span', {
                        className: 'badge',
                        children: [qe, ' online'],
                      }),
                    ],
                  }),
                }),
                _n(le),
              ],
            }),
          le.length === 0 &&
            s.jsxs('div', {
              className: 'empty-state',
              children: [
                s.jsx('div', { className: 'icon', children: '📡' }),
                s.jsx('h3', { children: 'No Devices Found' }),
                s.jsx('p', {
                  children:
                    g !== 'all' || h !== 'all'
                      ? 'No devices match your current filters.'
                      : 'Your Meraki devices will appear here once discovered.',
                }),
              ],
            }),
        ],
      });
    },
    ap = ({ deviceName: e, model: t, ports: r }) => {
      var g, m, h, y, k, M, f, c, p, w, z;
      const [n, l] = A.useState(null),
        i = (S) =>
          S >= 1e6
            ? `${(S / 1e6).toFixed(1)} GB`
            : S >= 1e3
            ? `${(S / 1e3).toFixed(1)} MB`
            : `${S} KB`,
        a = (S) =>
          S >= 1e3 ? `${(S / 1e3).toFixed(1)} Mbps` : `${S.toFixed(1)} Kbps`,
        u = (S) => {
          var C;
          return (
            ((C = S.status) == null ? void 0 : C.toLowerCase()) === 'connected'
          );
        },
        o = (S) => {
          var C, P;
          return (
            ((C = S.poe) == null ? void 0 : C.isAllocated) === !0 ||
            ((P = S.poe) == null ? void 0 : P.enabled) === !0
          );
        },
        d = r.filter(u).length,
        v = r.filter(o).length;
      return s.jsxs('div', {
        className: 'info-card',
        children: [
          s.jsxs('h3', {
            children: [s.jsx('span', { children: '⚡' }), ' Port Status'],
          }),
          s.jsxs('div', {
            className: 'port-visualization',
            children: [
              s.jsxs('div', {
                className: 'switch-chassis',
                children: [
                  s.jsxs('div', {
                    className: 'switch-label',
                    children: [
                      s.jsxs('span', { children: ['Cisco Meraki ', t] }),
                      s.jsxs('span', {
                        children: [d, ' of ', r.length, ' connected'],
                      }),
                    ],
                  }),
                  s.jsx('div', {
                    className: 'ports-row',
                    children: r.map((S) =>
                      s.jsxs(
                        'div',
                        {
                          className: `port ${u(S) ? 'connected' : ''} ${
                            (n == null ? void 0 : n.portId) === S.portId
                              ? 'selected'
                              : ''
                          }`,
                          onClick: () => l(S),
                          title: `Port ${S.portId}${
                            S.clientName ? ` - ${S.clientName}` : ''
                          }`,
                          children: [
                            s.jsx('span', {
                              className: 'num',
                              children: S.portId,
                            }),
                            o(S) &&
                              s.jsx('span', {
                                className: 'poe',
                                children: '⚡',
                              }),
                          ],
                        },
                        S.portId
                      )
                    ),
                  }),
                ],
              }),
              s.jsxs('div', {
                className: 'port-legend',
                children: [
                  s.jsxs('span', {
                    children: [
                      s.jsx('div', { className: 'dot connected' }),
                      'Connected (',
                      d,
                      ')',
                    ],
                  }),
                  s.jsxs('span', {
                    children: [
                      s.jsx('div', { className: 'dot disconnected' }),
                      'Disconnected (',
                      r.length - d,
                      ')',
                    ],
                  }),
                  s.jsxs('span', { children: ['⚡ PoE Active (', v, ')'] }),
                ],
              }),
            ],
          }),
          n &&
            s.jsxs('div', {
              className: 'port-details',
              children: [
                s.jsxs('h4', {
                  children: [
                    s.jsx('span', {
                      style: {
                        color: u(n) ? 'var(--success)' : 'var(--text-muted)',
                      },
                      children: '🔌',
                    }),
                    'Port ',
                    n.portId,
                    ' - ',
                    n.status || 'Unknown',
                    n.isUplink &&
                      s.jsx('span', {
                        style: {
                          marginLeft: '8px',
                          fontSize: '12px',
                          color: 'var(--primary)',
                        },
                        children: '↑ Uplink',
                      }),
                  ],
                }),
                (((g = n.errors) == null ? void 0 : g.length) ||
                  ((m = n.warnings) == null ? void 0 : m.length)) &&
                  s.jsxs('div', {
                    style: { marginBottom: '12px' },
                    children: [
                      (h = n.errors) == null
                        ? void 0
                        : h.map((S, C) =>
                            s.jsxs(
                              'div',
                              {
                                style: {
                                  color: 'var(--error)',
                                  fontSize: '13px',
                                  display: 'flex',
                                  alignItems: 'center',
                                  gap: '6px',
                                },
                                children: [
                                  s.jsx('span', { children: '🚨' }),
                                  ' ',
                                  S,
                                ],
                              },
                              `err-${C}`
                            )
                          ),
                      (y = n.warnings) == null
                        ? void 0
                        : y.map((S, C) =>
                            s.jsxs(
                              'div',
                              {
                                style: {
                                  color: 'var(--warning)',
                                  fontSize: '13px',
                                  display: 'flex',
                                  alignItems: 'center',
                                  gap: '6px',
                                },
                                children: [
                                  s.jsx('span', { children: '⚠️' }),
                                  ' ',
                                  S,
                                ],
                              },
                              `warn-${C}`
                            )
                          ),
                    ],
                  }),
                u(n) &&
                  n.clientName &&
                  s.jsxs('div', {
                    className: 'client-info',
                    children: [
                      s.jsx('div', {
                        className: 'client-avatar',
                        children: '💻',
                      }),
                      s.jsxs('div', {
                        className: 'client-details',
                        children: [
                          s.jsx('div', {
                            className: 'name',
                            children: n.clientName,
                          }),
                          s.jsx('div', {
                            className: 'mac',
                            children: n.clientMac || 'Unknown MAC',
                          }),
                        ],
                      }),
                    ],
                  }),
                s.jsxs('div', {
                  className: 'port-stats',
                  children: [
                    s.jsxs('div', {
                      className: 'port-stat',
                      children: [
                        s.jsx('div', {
                          className: 'label',
                          children: 'Speed',
                        }),
                        s.jsx('div', {
                          className: 'value',
                          children: n.speed || '—',
                        }),
                      ],
                    }),
                    s.jsxs('div', {
                      className: 'port-stat',
                      children: [
                        s.jsx('div', {
                          className: 'label',
                          children: 'Duplex',
                        }),
                        s.jsx('div', {
                          className: 'value',
                          children: n.duplex || '—',
                        }),
                      ],
                    }),
                    s.jsxs('div', {
                      className: 'port-stat',
                      children: [
                        s.jsx('div', {
                          className: 'label',
                          children: 'Live Traffic',
                        }),
                        s.jsx('div', {
                          className: 'value',
                          children:
                            ((k = n.trafficInKbps) == null
                              ? void 0
                              : k.total) != null
                              ? a(n.trafficInKbps.total)
                              : '—',
                        }),
                      ],
                    }),
                    s.jsxs('div', {
                      className: 'port-stat',
                      children: [
                        s.jsx('div', {
                          className: 'label',
                          children: 'Total Usage',
                        }),
                        s.jsx('div', {
                          className: 'value',
                          children:
                            ((M = n.usageInKb) == null ? void 0 : M.total) !=
                            null
                              ? i(n.usageInKb.total)
                              : '—',
                        }),
                      ],
                    }),
                    s.jsxs('div', {
                      className: 'port-stat',
                      children: [
                        s.jsx('div', {
                          className: 'label',
                          children: 'PoE Energy',
                        }),
                        s.jsx('div', {
                          className: 'value',
                          style: { color: 'var(--warning)' },
                          children:
                            n.powerUsageInWh != null
                              ? `${n.powerUsageInWh.toFixed(1)} Wh`
                              : '—',
                        }),
                      ],
                    }),
                    s.jsxs('div', {
                      className: 'port-stat',
                      children: [
                        s.jsx('div', { className: 'label', children: 'VLAN' }),
                        s.jsx('div', {
                          className: 'value',
                          children: n.vlan || '—',
                        }),
                      ],
                    }),
                    s.jsxs('div', {
                      className: 'port-stat',
                      children: [
                        s.jsx('div', {
                          className: 'label',
                          children: 'Clients',
                        }),
                        s.jsx('div', {
                          className: 'value',
                          children: n.clientCount ?? '—',
                        }),
                      ],
                    }),
                  ],
                }),
                (((f = n.lldp) == null ? void 0 : f.systemName) ||
                  ((c = n.cdp) == null ? void 0 : c.deviceId)) &&
                  s.jsxs('div', {
                    style: {
                      marginTop: '16px',
                      padding: '12px',
                      background: 'var(--bg-primary)',
                      borderRadius: 'var(--radius-sm)',
                    },
                    children: [
                      s.jsx('h5', {
                        style: {
                          margin: '0 0 8px 0',
                          fontSize: '13px',
                          color: 'var(--text-muted)',
                        },
                        children: '🔗 Neighbor Discovery',
                      }),
                      ((p = n.lldp) == null ? void 0 : p.systemName) &&
                        s.jsxs('div', {
                          style: { marginBottom: '8px' },
                          children: [
                            s.jsx('div', {
                              style: {
                                fontSize: '11px',
                                color: 'var(--text-muted)',
                                textTransform: 'uppercase',
                              },
                              children: 'LLDP',
                            }),
                            s.jsx('div', {
                              style: { fontSize: '14px', fontWeight: 500 },
                              children: n.lldp.systemName,
                            }),
                            n.lldp.portId &&
                              s.jsxs('div', {
                                style: {
                                  fontSize: '12px',
                                  color: 'var(--text-secondary)',
                                },
                                children: [
                                  'Port: ',
                                  n.lldp.portId,
                                  ' ',
                                  n.lldp.portDescription &&
                                    `(${n.lldp.portDescription})`,
                                ],
                              }),
                            n.lldp.managementAddress &&
                              s.jsx('div', {
                                style: {
                                  fontSize: '12px',
                                  color: 'var(--text-secondary)',
                                  fontFamily: 'monospace',
                                },
                                children: n.lldp.managementAddress,
                              }),
                          ],
                        }),
                      ((w = n.cdp) == null ? void 0 : w.deviceId) &&
                        s.jsxs('div', {
                          children: [
                            s.jsx('div', {
                              style: {
                                fontSize: '11px',
                                color: 'var(--text-muted)',
                                textTransform: 'uppercase',
                              },
                              children: 'CDP',
                            }),
                            s.jsx('div', {
                              style: { fontSize: '14px', fontWeight: 500 },
                              children: n.cdp.deviceId,
                            }),
                            n.cdp.platform &&
                              s.jsx('div', {
                                style: {
                                  fontSize: '12px',
                                  color: 'var(--text-secondary)',
                                },
                                children: n.cdp.platform,
                              }),
                            n.cdp.portId &&
                              s.jsxs('div', {
                                style: {
                                  fontSize: '12px',
                                  color: 'var(--text-secondary)',
                                },
                                children: ['Port: ', n.cdp.portId],
                              }),
                            n.cdp.managementAddress &&
                              s.jsx('div', {
                                style: {
                                  fontSize: '12px',
                                  color: 'var(--text-secondary)',
                                  fontFamily: 'monospace',
                                },
                                children: n.cdp.managementAddress,
                              }),
                          ],
                        }),
                    ],
                  }),
                ((z = n.securePort) == null ? void 0 : z.enabled) &&
                  s.jsxs('div', {
                    style: {
                      marginTop: '12px',
                      fontSize: '13px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '6px',
                    },
                    children: [
                      s.jsx('span', { children: '🔒' }),
                      s.jsxs('span', {
                        style: {
                          color: n.securePort.active
                            ? 'var(--success)'
                            : 'var(--text-muted)',
                        },
                        children: [
                          'SecurePort:',
                          ' ',
                          n.securePort.authenticationStatus ||
                            (n.securePort.active ? 'Active' : 'Inactive'),
                        ],
                      }),
                    ],
                  }),
              ],
            }),
          !n &&
            s.jsx('div', {
              style: {
                textAlign: 'center',
                padding: '20px',
                color: 'var(--text-muted)',
                fontSize: '14px',
              },
              children: 'Click a port to view details',
            }),
        ],
      });
    },
    lr = ({
      type: e,
      value: t,
      unit: r,
      min: n,
      max: l,
      status: i = 'normal',
      temperatureUnit: a = 'celsius',
    }) => {
      const u = () => {
          switch (e) {
            case 'temperature':
              return '🌡️';
            case 'humidity':
              return '💧';
            case 'water':
              return '🌊';
            case 'door':
              return '🚪';
            case 'tvoc':
              return '🌬️';
            case 'pm25':
              return '🌫️';
            case 'noise':
              return '🔊';
            case 'battery':
              return '🔋';
            case 'co2':
              return '💨';
            case 'indoorAirQuality':
              return '🍃';
            default:
              return '📊';
          }
        },
        o = () => {
          switch (e) {
            case 'temperature':
              return 'Temperature';
            case 'humidity':
              return 'Humidity';
            case 'water':
              return 'Water Detection';
            case 'door':
              return 'Door Status';
            case 'tvoc':
              return 'TVOC';
            case 'pm25':
              return 'PM2.5';
            case 'noise':
              return 'Noise Level';
            case 'battery':
              return 'Battery';
            case 'co2':
              return 'CO₂';
            case 'indoorAirQuality':
              return 'Air Quality';
            default:
              return e;
          }
        },
        d = () => {
          switch (e) {
            case 'temperature':
              return a === 'fahrenheit' ? '°F' : '°C';
            case 'humidity':
              return '%';
            case 'tvoc':
              return 'ppb';
            case 'pm25':
              return 'µg/m³';
            case 'noise':
              return 'dB';
            case 'battery':
              return '%';
            case 'co2':
              return 'ppm';
            case 'indoorAirQuality':
              return '';
            default:
              return '';
          }
        },
        v = () =>
          e === 'temperature' && a === 'fahrenheit' ? (t * 9) / 5 + 32 : t,
        g = () => {
          if (n !== void 0 && l !== void 0)
            return e === 'temperature' && a === 'fahrenheit'
              ? { min: (n * 9) / 5 + 32, max: (l * 9) / 5 + 32 }
              : { min: n, max: l };
          switch (e) {
            case 'temperature':
              return a === 'fahrenheit'
                ? { min: 32, max: 122 }
                : { min: 0, max: 50 };
            case 'humidity':
            case 'battery':
              return { min: 0, max: 100 };
            case 'tvoc':
              return { min: 0, max: 1e3 };
            case 'pm25':
              return { min: 0, max: 150 };
            case 'noise':
              return { min: 20, max: 100 };
            case 'co2':
              return { min: 400, max: 2e3 };
            case 'indoorAirQuality':
              return { min: 0, max: 100 };
            default:
              return { min: 0, max: 100 };
          }
        },
        m = () => {
          switch (i) {
            case 'normal':
              return e === 'humidity'
                ? 'Optimal humidity'
                : e === 'indoorAirQuality'
                ? 'Good air quality'
                : e === 'co2'
                ? 'Normal CO₂'
                : 'Within normal range';
            case 'warning':
              return 'Above threshold';
            case 'critical':
              return 'Critical level!';
            default:
              return '';
          }
        },
        h = () => {
          const p = g(),
            w = v();
          return p.max === p.min
            ? 0
            : Math.min(
                100,
                Math.max(0, ((w - p.min) / (p.max - p.min)) * 100)
              );
        },
        y = () => {
          switch (e) {
            case 'temperature':
              return 'temp';
            case 'humidity':
              return 'humidity';
            case 'tvoc':
            case 'pm25':
            case 'co2':
            case 'indoorAirQuality':
              return 'air-quality';
            case 'noise':
              return 'noise';
            case 'battery':
              return 'battery';
            default:
              return 'default';
          }
        },
        k = r || d(),
        M = h(),
        f = v(),
        c = g();
      return s.jsxs('div', {
        className: `reading-card ${e}`,
        children: [
          s.jsx('div', {
            className: 'icon-wrapper',
            children: s.jsx('span', {
              style: { fontSize: '36px' },
              children: u(),
            }),
          }),
          s.jsx('div', { className: 'reading-label', children: o() }),
          s.jsxs('div', {
            className: 'reading-value',
            children: [
              typeof f == 'number' ? f.toFixed(1) : f,
              s.jsx('span', { className: 'reading-unit', children: k }),
            ],
          }),
          s.jsxs('div', {
            className: 'reading-status',
            children: [
              i === 'normal' && s.jsx('span', { children: '✅' }),
              i === 'warning' && s.jsx('span', { children: '⚠️' }),
              i === 'critical' && s.jsx('span', { children: '🚨' }),
              m(),
            ],
          }),
          s.jsx('div', {
            className: 'gauge-wrapper',
            children: s.jsx('div', {
              className: `gauge-fill ${y()}`,
              style: { width: `${M}%` },
            }),
          }),
          s.jsxs('div', {
            className: 'gauge-labels',
            children: [
              s.jsxs('span', { children: [c.min.toFixed(0), k] }),
              s.jsxs('span', {
                children: [((c.max + c.min) / 2).toFixed(0), k],
              }),
              s.jsxs('span', { children: [c.max.toFixed(0), k] }),
            ],
          }),
        ],
      });
    },
    Je = ({
      icon: e,
      label: t,
      value: r,
      unit: n = '',
      secondaryValue: l,
      gauge: i,
      status: a = 'normal',
      statusMessage: u,
      onClick: o,
    }) => {
      const d = () => {
          switch (a) {
            case 'normal':
              return '✅';
            case 'warning':
              return '⚠️';
            case 'critical':
              return '🚨';
            case 'inactive':
              return '⏸️';
            default:
              return '';
          }
        },
        v = () => {
          if (!i || typeof r != 'number') return 0;
          const { min: M, max: f } = i;
          return f === M
            ? 0
            : Math.min(100, Math.max(0, ((r - M) / (f - M)) * 100));
        },
        g = () => {
          if (!(i != null && i.color))
            switch (a) {
              case 'normal':
                return 'success';
              case 'warning':
                return 'warning';
              case 'critical':
                return 'error';
              default:
                return 'primary';
            }
          return i.color;
        },
        m = () => `metric-icon-wrapper metric-icon-${g()}`,
        h = () =>
          typeof r == 'number'
            ? Number.isInteger(r)
              ? r.toString()
              : r.toFixed(1)
            : r,
        y = v(),
        k = (i == null ? void 0 : i.showLabels) !== !1 && i;
      return s.jsxs('div', {
        className: `metric-card ${o ? 'clickable' : ''}`,
        onClick: o,
        role: o ? 'button' : void 0,
        tabIndex: o ? 0 : void 0,
        children: [
          s.jsx('div', {
            className: m(),
            children: s.jsx('span', { className: 'metric-icon', children: e }),
          }),
          s.jsx('div', { className: 'metric-label', children: t }),
          s.jsxs('div', {
            className: 'metric-value',
            children: [
              h(),
              n && s.jsx('span', { className: 'metric-unit', children: n }),
            ],
          }),
          l && s.jsx('div', { className: 'metric-secondary', children: l }),
          u &&
            s.jsxs('div', {
              className: `metric-status metric-status-${a}`,
              children: [s.jsx('span', { children: d() }), u],
            }),
          i &&
            s.jsxs(s.Fragment, {
              children: [
                s.jsx('div', {
                  className: 'metric-gauge-wrapper',
                  children: s.jsx('div', {
                    className: `metric-gauge-fill metric-gauge-${g()}`,
                    style: { width: `${y}%` },
                  }),
                }),
                k &&
                  s.jsxs('div', {
                    className: 'metric-gauge-labels',
                    children: [
                      s.jsxs('span', { children: [i.min, n] }),
                      s.jsxs('span', { children: [i.max, n] }),
                    ],
                  }),
              ],
            }),
        ],
      });
    },
    op = ({
      activeView: e,
      setActiveView: t,
      data: r,
      hass: n,
      configEntryId: l,
      cameraLinkIntegration: i,
      configEntryOptions: a,
    }) => {
      const u = (a == null ? void 0 : a.temperature_unit) || 'celsius',
        o = r.devices.find((x) => x.serial === e.deviceId),
        d = (r.clients || []).filter(
          (x) => x.recentDeviceSerial === (o == null ? void 0 : o.serial)
        ),
        [v, g] = Fe.useState(null),
        [m, h] = Fe.useState(!1),
        [y, k] = Fe.useState(null),
        [M, f] = Fe.useState([]),
        [c, p] = Fe.useState(''),
        [w, z] = Fe.useState(!1),
        [S, C] = Fe.useState(!1),
        [P, W] = Fe.useState(null),
        [R, xe] = Fe.useState(!1),
        fe = A.useRef(n);
      fe.current = n;
      const Le = A.useRef(null);
      if (!o)
        return s.jsxs('div', {
          children: [
            s.jsx('button', {
              onClick: () => t({ view: 'dashboard' }),
              className: 'back-button',
              children: '← Back to Dashboard',
            }),
            s.jsxs('div', {
              className: 'empty-state',
              children: [
                s.jsx('div', { className: 'icon', children: '❓' }),
                s.jsx('h3', { children: 'Device Not Found' }),
                s.jsx('p', {
                  children: 'The requested device could not be found.',
                }),
              ],
            }),
          ],
        });
      const {
          name: ir,
          model: le = '',
          serial: qe,
          firmware: ot,
          status: E,
          lanIp: D,
          mac: I,
          productType: U,
          status_messages: Z = [],
          entities: $t = [],
          ports_statuses: oe = [],
          readings: O,
          uptime: ee,
          lastReportedAt: et,
        } = o,
        _n = () => {
          const x = le.toUpperCase(),
            _ = (U == null ? void 0 : U.toLowerCase()) || '';
          return x.startsWith('MS') || _ === 'switch'
            ? '⚡'
            : x.startsWith('MV') || _ === 'camera'
            ? '📹'
            : x.startsWith('MR') || _ === 'wireless'
            ? '📶'
            : x.startsWith('MT') || _ === 'sensor'
            ? '🌡️'
            : x.startsWith('MX') || x.startsWith('Z') || _ === 'appliance'
            ? '🔒'
            : '📱';
        },
        N = () => {
          const x = le.toUpperCase(),
            _ = (U == null ? void 0 : U.toLowerCase()) || '';
          return x.startsWith('MS') || _ === 'switch'
            ? 'switch'
            : x.startsWith('MV') || _ === 'camera'
            ? 'camera'
            : x.startsWith('MR') || _ === 'wireless'
            ? 'wireless'
            : x.startsWith('MT') || _ === 'sensor'
            ? 'sensor'
            : x.startsWith('MX') || x.startsWith('Z') || _ === 'appliance'
            ? 'appliance'
            : '';
        },
        T = le.toUpperCase().startsWith('MS') || U === 'switch',
        b = le.toUpperCase().startsWith('MT') || U === 'sensor',
        ye = le.toUpperCase().startsWith('MV') || U === 'camera',
        we = le.toUpperCase().startsWith('MR') || U === 'wireless',
        ie =
          le.toUpperCase().startsWith('MX') ||
          le.toUpperCase().startsWith('Z') ||
          U === 'appliance',
        Be = [
          'temperature',
          'humidity',
          'battery',
          'tvoc',
          'pm25',
          'pm2_5',
          'co2',
          'noise',
          'indoor_air_quality',
          'air_quality',
          'voc',
        ],
        At = $t.filter((x) => {
          const _ = x.name.toLowerCase(),
            pe = x.entity_id.toLowerCase();
          return !Be.some((tt) => _.includes(tt) || pe.includes(tt));
        }),
        Ir = (x) => {
          if (!x) return null;
          const _ = Math.floor(x / 86400),
            pe = Math.floor((x % 86400) / 3600);
          if (_ > 0) return `${_}d ${pe}h`;
          const tt = Math.floor((x % 3600) / 60);
          return `${pe}h ${tt}m`;
        },
        ra = (x) => (x ? Math.floor(x / 86400) : 0),
        zc = (x) => {
          if (!x) return 'Just now';
          const _ = new Date(x),
            pe = new Date();
          return _.toDateString() === pe.toDateString()
            ? _.toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
              })
            : _.toLocaleString([], {
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
              });
        },
        Pc = (x) => {
          const _ = new CustomEvent('hass-more-info', {
            bubbles: !0,
            composed: !0,
            detail: { entityId: x },
          });
          document.body.dispatchEvent(_);
        },
        Lc = async () => {
          const x = fe.current;
          if (!(!x || !l || !o)) {
            h(!0);
            try {
              const _ = await x.callWS({
                type: 'meraki_ha/get_camera_snapshot',
                config_entry_id: l,
                serial: o.serial,
              });
              _ != null && _.url && g(_.url);
            } catch (_) {
              console.error('Failed to fetch snapshot:', _);
            } finally {
              h(!1);
            }
          }
        },
        yp = async () => {
          const x = fe.current;
          if (!(!x || !l || !o))
            try {
              const _ = await x.callWS({
                type: 'meraki_ha/get_camera_stream_url',
                config_entry_id: l,
                serial: o.serial,
                stream_source: 'cloud',
              });
              _ != null && _.url && k(_.url);
            } catch (_) {
              console.error('Failed to fetch cloud video URL:', _);
            }
        },
        wp = () => {
          y && window.open(y, '_blank', 'noopener,noreferrer');
        },
        kp = async () => {
          const x = fe.current;
          if (x)
            try {
              const _ = await x.callWS({
                type: 'meraki_ha/get_available_cameras',
                integration_filter: i || '',
              });
              _ != null && _.cameras && f(_.cameras);
            } catch (_) {
              console.error('Failed to fetch available cameras:', _);
            }
        },
        Sp = async () => {
          const x = fe.current;
          if (!(!x || !l || !o))
            try {
              const _ = await x.callWS({
                type: 'meraki_ha/get_camera_mappings',
                config_entry_id: l,
              });
              _ != null &&
                _.mappings &&
                _.mappings[o.serial] &&
                p(_.mappings[o.serial]);
            } catch (_) {
              console.error('Failed to fetch camera mappings:', _);
            }
        },
        jp = async (x) => {
          const _ = fe.current;
          if (!(!_ || !l || !o))
            try {
              await _.callWS({
                type: 'meraki_ha/set_camera_mapping',
                config_entry_id: l,
                serial: o.serial,
                linked_entity_id: x,
              }),
                p(x),
                z(!1),
                S && x && (W(null), setTimeout(() => na(), 100));
            } catch (pe) {
              console.error('Failed to save camera mapping:', pe);
            }
        },
        na = async () => {
          const x = fe.current;
          if (!(!x || !c)) {
            xe(!0);
            try {
              const _ = await x.callWS({
                type: 'auth/sign_path',
                path: `/api/camera_proxy/${c}`,
                expires: 30,
              });
              _ != null && _.path && W(_.path);
            } catch (_) {
              console.error('Failed to get signed camera URL:', _), W(null);
            } finally {
              xe(!1);
            }
          }
        };
      Fe.useEffect(() => {
        var pe;
        const x =
            o &&
            (((pe = o.model) == null
              ? void 0
              : pe.toUpperCase().startsWith('MV')) ||
              o.productType === 'camera'),
          _ = o == null ? void 0 : o.serial;
        x &&
          _ &&
          l &&
          fe.current &&
          Le.current !== _ &&
          ((Le.current = _), Lc(), yp(), Sp(), kp());
      }, [o == null ? void 0 : o.serial, l]),
        Fe.useEffect(() => {
          S && c && fe.current && na();
        }, [S, c]);
      const Np = oe.reduce((x, _) => x + (_.powerUsageInWh || 0), 0),
        Tc = oe.reduce((x, _) => x + (_.clientCount || 0), 0);
      return s.jsxs('div', {
        children: [
          s.jsx('button', {
            onClick: () => t({ view: 'dashboard' }),
            className: 'back-button',
            children: '← Back to Dashboard',
          }),
          s.jsxs('div', {
            className: 'device-header',
            children: [
              s.jsx('div', {
                className: `device-icon ${N()}`,
                children: _n(),
              }),
              s.jsxs('div', {
                className: 'device-info',
                children: [
                  s.jsx('h1', { children: ir || qe }),
                  s.jsxs('div', {
                    className: 'meta',
                    children: [
                      s.jsxs('span', {
                        children: [
                          s.jsx('strong', { children: 'Model:' }),
                          ' ',
                          le,
                        ],
                      }),
                      s.jsxs('span', {
                        children: [
                          s.jsx('strong', { children: 'Serial:' }),
                          ' ',
                          qe,
                        ],
                      }),
                      ot &&
                        s.jsxs('span', {
                          children: [
                            s.jsx('strong', { children: 'Firmware:' }),
                            ' ',
                            ot,
                          ],
                        }),
                      D &&
                        s.jsxs('span', {
                          children: [
                            s.jsx('strong', { children: 'IP:' }),
                            ' ',
                            D,
                          ],
                        }),
                      I &&
                        s.jsxs('span', {
                          children: [
                            s.jsx('strong', { children: 'MAC:' }),
                            ' ',
                            s.jsx('span', {
                              style: { fontFamily: 'monospace' },
                              children: I,
                            }),
                          ],
                        }),
                      b &&
                        (O == null ? void 0 : O.battery) != null &&
                        s.jsxs('span', {
                          children: [
                            s.jsx('strong', { children: 'Battery:' }),
                            ' ',
                            s.jsxs('span', {
                              style: {
                                color:
                                  O.battery > 20
                                    ? 'var(--success)'
                                    : 'var(--warning)',
                              },
                              children: [O.battery, '%'],
                            }),
                          ],
                        }),
                    ],
                  }),
                  et &&
                    s.jsx('div', {
                      className: 'meta',
                      style: { marginTop: '4px', fontSize: '12px' },
                      children: s.jsxs('span', {
                        style: { color: 'var(--text-muted)' },
                        children: ['Last updated: ', zc(et)],
                      }),
                    }),
                ],
              }),
              s.jsxs('div', {
                className: `status-pill ${
                  E == null ? void 0 : E.toLowerCase()
                }`,
                children: [s.jsx('div', { className: 'dot' }), E || 'Unknown'],
              }),
            ],
          }),
          T &&
            oe.length > 0 &&
            s.jsxs('div', {
              className: 'metric-cards-grid',
              children: [
                s.jsx(Je, {
                  icon: '⚡',
                  label: 'PoE Energy',
                  value: Np,
                  unit: 'Wh',
                  gauge: { min: 0, max: 500, color: 'warning' },
                  status: 'normal',
                  statusMessage: 'Active',
                }),
                s.jsx(Je, {
                  icon: '👥',
                  label: 'Connected Clients',
                  value: Tc,
                  gauge: { min: 0, max: Math.max(50, Tc), color: 'info' },
                  status: 'normal',
                }),
                ee != null &&
                  s.jsx(Je, {
                    icon: '⏱️',
                    label: 'Uptime',
                    value: ra(ee),
                    unit: ' days',
                    secondaryValue: Ir(ee) || void 0,
                    status: 'normal',
                    statusMessage: 'Running',
                  }),
                s.jsx(Je, {
                  icon: '🔌',
                  label: 'Connected Ports',
                  value: oe.filter((x) => {
                    var _;
                    return (
                      ((_ = x.status) == null ? void 0 : _.toLowerCase()) ===
                      'connected'
                    );
                  }).length,
                  secondaryValue: `of ${oe.length} total`,
                  gauge: { min: 0, max: oe.length, color: 'success' },
                  status: 'normal',
                }),
              ],
            }),
          we &&
            s.jsxs('div', {
              className: 'metric-cards-grid',
              children: [
                s.jsx(Je, {
                  icon: '👥',
                  label: 'Connected Clients',
                  value: d.length,
                  gauge: {
                    min: 0,
                    max: Math.max(50, d.length),
                    color: 'info',
                  },
                  status: 'normal',
                }),
                o.basicServiceSets &&
                  s.jsx(Je, {
                    icon: '📶',
                    label: 'Active SSIDs',
                    value: o.basicServiceSets.filter((x) => x.enabled).length,
                    secondaryValue: `of ${o.basicServiceSets.length} total`,
                    gauge: {
                      min: 0,
                      max: o.basicServiceSets.length || 1,
                      color: 'success',
                    },
                    status: 'normal',
                  }),
                ee != null &&
                  s.jsx(Je, {
                    icon: '⏱️',
                    label: 'Uptime',
                    value: ra(ee),
                    unit: ' days',
                    secondaryValue: Ir(ee) || void 0,
                    status: 'normal',
                    statusMessage: 'Running',
                  }),
              ],
            }),
          ie &&
            s.jsxs('div', {
              className: 'metric-cards-grid',
              children: [
                s.jsx(Je, {
                  icon: '🌐',
                  label: 'WAN Status',
                  value: E === 'online' ? 'Online' : 'Offline',
                  status: E === 'online' ? 'normal' : 'critical',
                  statusMessage: E === 'online' ? 'Connected' : 'Disconnected',
                }),
                ee != null &&
                  s.jsx(Je, {
                    icon: '⏱️',
                    label: 'Uptime',
                    value: ra(ee),
                    unit: ' days',
                    secondaryValue: Ir(ee) || void 0,
                    status: 'normal',
                    statusMessage: 'Running',
                  }),
              ],
            }),
          ye &&
            s.jsxs('div', {
              className: 'metric-cards-grid',
              children: [
                s.jsx(Je, {
                  icon: '🔴',
                  label: 'Recording',
                  value: E === 'online' ? 'Active' : 'Inactive',
                  status: E === 'online' ? 'normal' : 'inactive',
                  statusMessage:
                    E === 'online' ? 'Recording to cloud' : 'Camera offline',
                }),
                s.jsx(Je, {
                  icon: '👁️',
                  label: 'Motion Detection',
                  value: 'Enabled',
                  status: 'normal',
                  statusMessage: 'Monitoring',
                }),
              ],
            }),
          s.jsx('div', {
            className: 'cards-grid',
            children:
              !T &&
              !b &&
              s.jsxs('div', {
                className: 'info-card',
                children: [
                  s.jsxs('div', {
                    style: {
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      marginBottom: '16px',
                    },
                    children: [
                      s.jsx('h3', {
                        style: { margin: 0 },
                        children: 'ℹ️ Device Information',
                      }),
                      et &&
                        s.jsxs('span', {
                          style: {
                            fontSize: '11px',
                            color: 'var(--text-muted)',
                            fontWeight: 400,
                          },
                          children: ['Updated: ', zc(et)],
                        }),
                    ],
                  }),
                  s.jsxs('div', {
                    className: 'info-grid',
                    children: [
                      D &&
                        s.jsxs('div', {
                          className: 'info-item',
                          children: [
                            s.jsx('div', {
                              className: 'label',
                              children: 'LAN IP',
                            }),
                            s.jsx('div', { className: 'value', children: D }),
                          ],
                        }),
                      I &&
                        s.jsxs('div', {
                          className: 'info-item',
                          children: [
                            s.jsx('div', {
                              className: 'label',
                              children: 'MAC Address',
                            }),
                            s.jsx('div', {
                              className: 'value mono',
                              children: I,
                            }),
                          ],
                        }),
                      ot &&
                        s.jsxs('div', {
                          className: 'info-item',
                          children: [
                            s.jsx('div', {
                              className: 'label',
                              children: 'Firmware',
                            }),
                            s.jsx('div', { className: 'value', children: ot }),
                          ],
                        }),
                      ee != null &&
                        !we &&
                        !ie &&
                        s.jsxs('div', {
                          className: 'info-item',
                          children: [
                            s.jsx('div', {
                              className: 'label',
                              children: 'Uptime',
                            }),
                            s.jsx('div', {
                              className: 'value',
                              children: Ir(ee),
                            }),
                          ],
                        }),
                    ],
                  }),
                ],
              }),
          }),
          T &&
            oe.length > 0 &&
            s.jsx(ap, { deviceName: ir || qe, model: le, ports: oe }),
          b &&
            O &&
            s.jsxs('div', {
              className: 'readings-grid',
              children: [
                O.temperature != null &&
                  s.jsx(lr, {
                    type: 'temperature',
                    value: O.temperature,
                    temperatureUnit: u,
                    status: 'normal',
                  }),
                O.humidity != null &&
                  s.jsx(lr, {
                    type: 'humidity',
                    value: O.humidity,
                    status: 'normal',
                  }),
                O.indoorAirQuality != null &&
                  s.jsx(lr, {
                    type: 'indoorAirQuality',
                    value: O.indoorAirQuality,
                    status:
                      O.indoorAirQuality >= 70
                        ? 'normal'
                        : O.indoorAirQuality >= 50
                        ? 'warning'
                        : 'critical',
                  }),
                O.tvoc != null &&
                  s.jsx(lr, {
                    type: 'tvoc',
                    value: O.tvoc,
                    status:
                      O.tvoc <= 400
                        ? 'normal'
                        : O.tvoc <= 800
                        ? 'warning'
                        : 'critical',
                  }),
                O.pm25 != null &&
                  s.jsx(lr, {
                    type: 'pm25',
                    value: O.pm25,
                    status:
                      O.pm25 <= 35
                        ? 'normal'
                        : O.pm25 <= 75
                        ? 'warning'
                        : 'critical',
                  }),
                O.co2 != null &&
                  s.jsx(lr, {
                    type: 'co2',
                    value: O.co2,
                    status:
                      O.co2 <= 1e3
                        ? 'normal'
                        : O.co2 <= 2e3
                        ? 'warning'
                        : 'critical',
                  }),
                O.noise != null &&
                  s.jsx(lr, {
                    type: 'noise',
                    value: O.noise,
                    status:
                      O.noise <= 60
                        ? 'normal'
                        : O.noise <= 80
                        ? 'warning'
                        : 'critical',
                  }),
              ],
            }),
          Z.length > 0 &&
            s.jsxs('div', {
              className: 'info-card',
              style: { borderLeft: '4px solid var(--warning)' },
              children: [
                s.jsx('h3', { children: '⚠️ Status Messages' }),
                s.jsx('ul', {
                  style: {
                    margin: 0,
                    paddingLeft: '20px',
                    color: 'var(--text-secondary)',
                  },
                  children: Z.map((x, _) =>
                    s.jsx(
                      'li',
                      { style: { marginBottom: '8px' }, children: x },
                      _
                    )
                  ),
                }),
              ],
            }),
          At.length > 0 &&
            s.jsxs('div', {
              className: 'info-card',
              children: [
                s.jsxs('h3', { children: ['🔗 Entities (', At.length, ')'] }),
                s.jsxs('table', {
                  className: 'device-table',
                  children: [
                    s.jsx('thead', {
                      children: s.jsxs('tr', {
                        children: [
                          s.jsx('th', { children: 'Name' }),
                          s.jsx('th', { children: 'Entity ID' }),
                          s.jsx('th', { children: 'State' }),
                        ],
                      }),
                    }),
                    s.jsx('tbody', {
                      children: At.map((x) =>
                        s.jsxs(
                          'tr',
                          {
                            className: 'device-row',
                            onClick: () => Pc(x.entity_id),
                            children: [
                              s.jsx('td', { children: x.name }),
                              s.jsx('td', {
                                style: {
                                  fontFamily: 'monospace',
                                  fontSize: '13px',
                                  color: 'var(--text-muted)',
                                },
                                children: x.entity_id,
                              }),
                              s.jsx('td', {
                                children: s.jsx('span', {
                                  className: 'detail-badge',
                                  children: x.state,
                                }),
                              }),
                            ],
                          },
                          x.entity_id
                        )
                      ),
                    }),
                  ],
                }),
              ],
            }),
          d.length > 0 &&
            s.jsxs('div', {
              className: 'info-card',
              children: [
                s.jsxs('h3', {
                  children: ['👥 Connected Clients (', d.length, ')'],
                }),
                s.jsxs('table', {
                  className: 'device-table',
                  children: [
                    s.jsx('thead', {
                      children: s.jsxs('tr', {
                        children: [
                          s.jsx('th', { children: 'Client' }),
                          s.jsx('th', { children: 'IP Address' }),
                          s.jsx('th', { children: 'Connection' }),
                        ],
                      }),
                    }),
                    s.jsx('tbody', {
                      children: d.slice(0, 10).map((x) => {
                        var _, pe, tt;
                        return s.jsxs(
                          'tr',
                          {
                            className: 'device-row',
                            onClick: () =>
                              t({ view: 'clients', clientId: x.id }),
                            style: { cursor: 'pointer' },
                            children: [
                              s.jsx('td', {
                                children: s.jsxs('div', {
                                  style: {
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '10px',
                                  },
                                  children: [
                                    s.jsx('span', {
                                      style: { fontSize: '18px' },
                                      children:
                                        ((_ = x.os) != null &&
                                          _.toLowerCase().includes('ios')) ||
                                        ((pe = x.manufacturer) != null &&
                                          pe.toLowerCase().includes('apple'))
                                          ? '📱'
                                          : (tt = x.os) != null &&
                                            tt
                                              .toLowerCase()
                                              .includes('windows')
                                          ? '💻'
                                          : '🔌',
                                    }),
                                    s.jsxs('div', {
                                      children: [
                                        s.jsx('div', {
                                          style: { fontWeight: 500 },
                                          children: x.description || x.mac,
                                        }),
                                        x.manufacturer &&
                                          s.jsx('div', {
                                            style: {
                                              fontSize: '12px',
                                              color: 'var(--text-muted)',
                                            },
                                            children: x.manufacturer,
                                          }),
                                      ],
                                    }),
                                  ],
                                }),
                              }),
                              x.ip &&
                                s.jsx('td', {
                                  style: {
                                    fontFamily: 'monospace',
                                    fontSize: '13px',
                                  },
                                  children: x.ip,
                                }),
                              !x.ip && s.jsx('td', {}),
                              s.jsx('td', {
                                children:
                                  (x.ssid || x.switchport) &&
                                  s.jsx('span', {
                                    className: 'detail-badge',
                                    children: x.ssid || x.switchport,
                                  }),
                              }),
                            ],
                          },
                          x.id || x.mac
                        );
                      }),
                    }),
                  ],
                }),
                d.length > 10 &&
                  s.jsxs('div', {
                    style: {
                      textAlign: 'center',
                      padding: '12px',
                      color: 'var(--text-muted)',
                      fontSize: '13px',
                    },
                    children: [
                      'Showing 10 of ',
                      d.length,
                      ' clients •',
                      ' ',
                      s.jsx('button', {
                        onClick: () => t({ view: 'clients' }),
                        style: {
                          background: 'none',
                          border: 'none',
                          color: 'var(--primary)',
                          cursor: 'pointer',
                          fontWeight: 500,
                          fontSize: '13px',
                        },
                        children: 'View All Clients',
                      }),
                    ],
                  }),
              ],
            }),
          ye &&
            s.jsxs('div', {
              className: 'info-card',
              children: [
                s.jsxs('div', {
                  style: {
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: '16px',
                  },
                  children: [
                    s.jsx('h3', {
                      style: { margin: 0 },
                      children: '📹 Camera',
                    }),
                    s.jsx('button', {
                      onClick: () => z(!w),
                      style: {
                        padding: '6px 12px',
                        borderRadius: 'var(--radius-sm)',
                        border: '1px solid var(--border)',
                        background: 'var(--bg-secondary)',
                        color: 'var(--text-secondary)',
                        cursor: 'pointer',
                        fontSize: '13px',
                      },
                      children: '⚙️ Link Camera',
                    }),
                  ],
                }),
                w &&
                  s.jsxs('div', {
                    style: {
                      background: 'var(--bg-primary)',
                      borderRadius: 'var(--radius-md)',
                      padding: '16px',
                      marginBottom: '16px',
                      border: '1px solid var(--border)',
                    },
                    children: [
                      s.jsx('h4', {
                        style: { margin: '0 0 12px 0', fontSize: '14px' },
                        children:
                          '🔗 Link to External Camera (e.g., Blue Iris)',
                      }),
                      s.jsx('p', {
                        style: {
                          fontSize: '13px',
                          color: 'var(--text-muted)',
                          marginBottom: '12px',
                        },
                        children:
                          'Link this Meraki camera to another camera entity in Home Assistant. Useful when RTSP goes to an NVR (like Blue Iris) first.',
                      }),
                      s.jsxs('div', {
                        style: {
                          display: 'flex',
                          gap: '8px',
                          flexWrap: 'wrap',
                        },
                        children: [
                          s.jsxs('select', {
                            value: c,
                            onChange: (x) => p(x.target.value),
                            style: {
                              flex: 1,
                              minWidth: '200px',
                              padding: '8px 12px',
                              borderRadius: 'var(--radius-sm)',
                              border: '1px solid var(--border)',
                              background: 'var(--bg-secondary)',
                              color: 'var(--text-primary)',
                              fontSize: '14px',
                            },
                            children: [
                              s.jsx('option', {
                                value: '',
                                children: '-- No linked camera --',
                              }),
                              M.map((x) =>
                                s.jsxs(
                                  'option',
                                  {
                                    value: x.entity_id,
                                    children: [
                                      x.friendly_name,
                                      ' (',
                                      x.entity_id,
                                      ')',
                                    ],
                                  },
                                  x.entity_id
                                )
                              ),
                            ],
                          }),
                          s.jsx('button', {
                            onClick: () => jp(c),
                            style: {
                              padding: '8px 16px',
                              borderRadius: 'var(--radius-sm)',
                              border: 'none',
                              background: 'var(--primary)',
                              color: 'white',
                              cursor: 'pointer',
                              fontWeight: 500,
                            },
                            children: 'Save',
                          }),
                        ],
                      }),
                      c &&
                        s.jsxs('p', {
                          style: {
                            fontSize: '12px',
                            color: 'var(--success)',
                            marginTop: '8px',
                            marginBottom: 0,
                          },
                          children: ['✓ Linked to: ', c],
                        }),
                    ],
                  }),
                c &&
                  s.jsxs('div', {
                    style: {
                      display: 'flex',
                      gap: '4px',
                      marginBottom: '16px',
                      background: 'var(--bg-primary)',
                      borderRadius: 'var(--radius-md)',
                      padding: '4px',
                    },
                    children: [
                      s.jsx('button', {
                        onClick: () => C(!1),
                        style: {
                          flex: 1,
                          padding: '8px 16px',
                          borderRadius: 'var(--radius-sm)',
                          border: 'none',
                          background: S ? 'transparent' : 'var(--primary)',
                          color: S ? 'var(--text-secondary)' : 'white',
                          cursor: 'pointer',
                          fontWeight: 500,
                          transition: 'all 0.2s',
                        },
                        children: '📷 Meraki Snapshot',
                      }),
                      s.jsx('button', {
                        onClick: () => C(!0),
                        style: {
                          flex: 1,
                          padding: '8px 16px',
                          borderRadius: 'var(--radius-sm)',
                          border: 'none',
                          background: S ? 'var(--primary)' : 'transparent',
                          color: S ? 'white' : 'var(--text-secondary)',
                          cursor: 'pointer',
                          fontWeight: 500,
                          transition: 'all 0.2s',
                        },
                        children: '🎬 Linked Camera',
                      }),
                    ],
                  }),
                s.jsx('div', {
                  style: {
                    background: 'var(--bg-primary)',
                    borderRadius: 'var(--radius-md)',
                    padding: '16px',
                    textAlign: 'center',
                    marginBottom: '16px',
                  },
                  children:
                    S && c
                      ? s.jsxs('div', {
                          children: [
                            R
                              ? s.jsx('div', {
                                  style: {
                                    padding: '40px',
                                    color: 'var(--text-muted)',
                                  },
                                  children: '⏳ Loading camera...',
                                })
                              : P
                              ? s.jsx('img', {
                                  src: P,
                                  alt: `Linked camera: ${c}`,
                                  style: {
                                    maxWidth: '100%',
                                    borderRadius: 'var(--radius-md)',
                                    marginBottom: '12px',
                                  },
                                  onError: () => {
                                    console.error(
                                      'Failed to load linked camera image'
                                    ),
                                      W(null);
                                  },
                                })
                              : s.jsx('div', {
                                  style: {
                                    padding: '40px',
                                    color: 'var(--text-muted)',
                                  },
                                  children: '📹 Unable to load camera feed',
                                }),
                            s.jsxs('div', {
                              style: {
                                display: 'flex',
                                gap: '12px',
                                justifyContent: 'center',
                                flexWrap: 'wrap',
                                marginTop: '12px',
                              },
                              children: [
                                s.jsx('button', {
                                  onClick: () => na(),
                                  disabled: R,
                                  style: {
                                    padding: '10px 20px',
                                    borderRadius: 'var(--radius-md)',
                                    border: 'none',
                                    background: 'var(--primary)',
                                    color: 'white',
                                    cursor: R ? 'wait' : 'pointer',
                                    fontWeight: 500,
                                  },
                                  children: R ? '⏳ Loading...' : '🔄 Refresh',
                                }),
                                s.jsx('button', {
                                  onClick: () => Pc(c),
                                  style: {
                                    padding: '10px 20px',
                                    borderRadius: 'var(--radius-md)',
                                    border: '1px solid var(--border)',
                                    background: 'var(--bg-secondary)',
                                    color: 'var(--text-primary)',
                                    cursor: 'pointer',
                                    fontWeight: 500,
                                  },
                                  children: '📺 Open Camera Entity',
                                }),
                              ],
                            }),
                            s.jsxs('p', {
                              style: {
                                fontSize: '12px',
                                color: 'var(--text-muted)',
                                marginTop: '12px',
                                marginBottom: 0,
                              },
                              children: ['Viewing: ', c],
                            }),
                          ],
                        })
                      : s.jsxs(s.Fragment, {
                          children: [
                            v
                              ? s.jsx('img', {
                                  src: v,
                                  alt: `${ir || qe} snapshot`,
                                  style: {
                                    maxWidth: '100%',
                                    borderRadius: 'var(--radius-md)',
                                    marginBottom: '12px',
                                  },
                                })
                              : s.jsx('div', {
                                  style: {
                                    padding: '40px',
                                    color: 'var(--text-muted)',
                                    fontSize: '48px',
                                  },
                                  children: '📹',
                                }),
                            s.jsxs('div', {
                              style: {
                                display: 'flex',
                                gap: '12px',
                                justifyContent: 'center',
                                flexWrap: 'wrap',
                                marginTop: '12px',
                              },
                              children: [
                                s.jsx('button', {
                                  onClick: Lc,
                                  disabled: m,
                                  style: {
                                    padding: '10px 20px',
                                    borderRadius: 'var(--radius-md)',
                                    border: 'none',
                                    background: 'var(--primary)',
                                    color: 'white',
                                    cursor: m ? 'wait' : 'pointer',
                                    fontWeight: 500,
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '8px',
                                  },
                                  children: m
                                    ? '⏳ Loading...'
                                    : '📷 Refresh Snapshot',
                                }),
                                y &&
                                  s.jsx('button', {
                                    onClick: wp,
                                    style: {
                                      padding: '10px 20px',
                                      borderRadius: 'var(--radius-md)',
                                      border: '1px solid var(--border)',
                                      background: 'var(--bg-secondary)',
                                      color: 'var(--text-primary)',
                                      cursor: 'pointer',
                                      fontWeight: 500,
                                      display: 'flex',
                                      alignItems: 'center',
                                      gap: '8px',
                                    },
                                    children: '🌐 Open in Meraki Dashboard',
                                  }),
                              ],
                            }),
                          ],
                        }),
                }),
                s.jsxs('div', {
                  style: {
                    fontSize: '13px',
                    color: 'var(--text-muted)',
                    textAlign: 'center',
                  },
                  children: [
                    s.jsxs('p', {
                      style: { margin: '0 0 8px 0' },
                      children: [
                        '💡 ',
                        s.jsx('strong', { children: 'RTSP Streaming:' }),
                        ' Enable in Meraki Dashboard → Camera Settings → External RTSP',
                      ],
                    }),
                    s.jsx('p', {
                      style: { margin: 0 },
                      children:
                        'For live streaming in Home Assistant dashboards, use the camera entity',
                    }),
                  ],
                }),
              ],
            }),
          we &&
            s.jsxs('div', {
              className: 'info-card',
              children: [
                s.jsx('h3', { children: '📶 Wireless Access Point' }),
                o.basicServiceSets && o.basicServiceSets.length > 0
                  ? s.jsxs('div', {
                      children: [
                        s.jsxs('table', {
                          className: 'device-table',
                          style: { marginTop: '16px' },
                          children: [
                            s.jsx('thead', {
                              children: s.jsxs('tr', {
                                children: [
                                  s.jsx('th', { children: 'SSID' }),
                                  s.jsx('th', { children: 'Band' }),
                                  s.jsx('th', { children: 'Channel' }),
                                  s.jsx('th', { children: 'Width' }),
                                  s.jsx('th', { children: 'Power' }),
                                  s.jsx('th', { children: 'Status' }),
                                ],
                              }),
                            }),
                            s.jsx('tbody', {
                              children: o.basicServiceSets
                                .filter((x) => x.enabled)
                                .map((x, _) => {
                                  var pe, tt;
                                  return s.jsxs(
                                    'tr',
                                    {
                                      children: [
                                        s.jsxs('td', {
                                          children: [
                                            s.jsx('div', {
                                              style: { fontWeight: 500 },
                                              children:
                                                x.ssidName ||
                                                `SSID ${x.ssidNumber}`,
                                            }),
                                            x.bssid &&
                                              s.jsx('div', {
                                                style: {
                                                  fontSize: '11px',
                                                  color: 'var(--text-muted)',
                                                  fontFamily: 'monospace',
                                                },
                                                children: x.bssid,
                                              }),
                                          ],
                                        }),
                                        s.jsx('td', {
                                          children: s.jsx('span', {
                                            className: 'detail-badge',
                                            style: {
                                              background:
                                                (pe = x.band) != null &&
                                                pe.includes('2.4')
                                                  ? 'rgba(245, 158, 11, 0.15)'
                                                  : 'rgba(6, 182, 212, 0.15)',
                                              color:
                                                (tt = x.band) != null &&
                                                tt.includes('2.4')
                                                  ? 'var(--warning)'
                                                  : 'var(--primary)',
                                            },
                                            children: x.band,
                                          }),
                                        }),
                                        s.jsx('td', { children: x.channel }),
                                        s.jsx('td', {
                                          children: x.channelWidth,
                                        }),
                                        s.jsx('td', {
                                          style: { color: 'var(--warning)' },
                                          children: x.power,
                                        }),
                                        s.jsx('td', {
                                          children: s.jsxs('span', {
                                            style: {
                                              display: 'inline-flex',
                                              alignItems: 'center',
                                              gap: '6px',
                                              color: x.broadcasting
                                                ? 'var(--success)'
                                                : 'var(--text-muted)',
                                            },
                                            children: [
                                              s.jsx('span', {
                                                style: {
                                                  width: '8px',
                                                  height: '8px',
                                                  borderRadius: '50%',
                                                  background: x.broadcasting
                                                    ? 'var(--success)'
                                                    : 'var(--text-muted)',
                                                  boxShadow: x.broadcasting
                                                    ? '0 0 8px var(--success)'
                                                    : 'none',
                                                },
                                              }),
                                              x.broadcasting
                                                ? 'Broadcasting'
                                                : 'Off',
                                            ],
                                          }),
                                        }),
                                      ],
                                    },
                                    `bss-${_}`
                                  );
                                }),
                            }),
                          ],
                        }),
                        o.basicServiceSets.filter((x) => !x.enabled).length >
                          0 &&
                          s.jsxs('div', {
                            style: {
                              marginTop: '12px',
                              fontSize: '13px',
                              color: 'var(--text-muted)',
                            },
                            children: [
                              o.basicServiceSets.filter((x) => !x.enabled)
                                .length,
                              ' ',
                              'disabled SSIDs not shown',
                            ],
                          }),
                      ],
                    })
                  : s.jsxs('div', {
                      className: 'info-grid',
                      children: [
                        s.jsxs('div', {
                          className: 'info-item',
                          children: [
                            s.jsx('div', {
                              className: 'label',
                              children: 'Connected Clients',
                            }),
                            s.jsx('div', {
                              className: 'value primary',
                              children: d.length,
                            }),
                          ],
                        }),
                        s.jsxs('div', {
                          className: 'info-item',
                          children: [
                            s.jsx('div', {
                              className: 'label',
                              children: 'Radio Bands',
                            }),
                            s.jsx('div', {
                              className: 'value',
                              children: '2.4 GHz / 5 GHz',
                            }),
                          ],
                        }),
                      ],
                    }),
              ],
            }),
        ],
      });
    },
    up = ({ clients: e, setActiveView: t, onBack: r }) => {
      var g;
      const [n, l] = A.useState(''),
        [i, a] = A.useState(null),
        u = e.filter((m) => {
          var y, k, M, f, c, p;
          const h = n.toLowerCase();
          return (
            ((y = m.description) == null
              ? void 0
              : y.toLowerCase().includes(h)) ||
            ((k = m.mac) == null ? void 0 : k.toLowerCase().includes(h)) ||
            ((M = m.ip) == null ? void 0 : M.toLowerCase().includes(h)) ||
            ((f = m.manufacturer) == null
              ? void 0
              : f.toLowerCase().includes(h)) ||
            ((c = m.user) == null ? void 0 : c.toLowerCase().includes(h)) ||
            ((p = m.os) == null ? void 0 : p.toLowerCase().includes(h))
          );
        }),
        o = (m) => {
          if (m === 0) return '0 B';
          const h = 1024,
            y = ['B', 'KB', 'MB', 'GB', 'TB'],
            k = Math.floor(Math.log(m) / Math.log(h));
          return parseFloat((m / Math.pow(h, k)).toFixed(2)) + ' ' + y[k];
        },
        d = (m) => (m ? new Date(m).toLocaleString() : '—'),
        v = (m) => {
          var k, M;
          const h = ((k = m.os) == null ? void 0 : k.toLowerCase()) || '',
            y =
              ((M = m.manufacturer) == null ? void 0 : M.toLowerCase()) || '';
          return h.includes('ios') ||
            y.includes('apple') ||
            h.includes('android')
            ? '📱'
            : h.includes('windows')
            ? '💻'
            : h.includes('mac')
            ? '🖥️'
            : h.includes('linux')
            ? '🐧'
            : y.includes('amazon') ||
              y.includes('roku') ||
              y.includes('samsung')
            ? '📺'
            : '🔌';
        };
      return i
        ? s.jsxs('div', {
            children: [
              s.jsx('button', {
                onClick: () => a(null),
                className: 'back-button',
                children: '← Back to Clients',
              }),
              s.jsxs('div', {
                className: 'device-header',
                children: [
                  s.jsx('div', { className: 'device-icon', children: v(i) }),
                  s.jsxs('div', {
                    className: 'device-info',
                    children: [
                      s.jsx('h1', { children: i.description || i.mac }),
                      s.jsxs('div', {
                        className: 'meta',
                        children: [
                          s.jsxs('span', {
                            children: [
                              s.jsx('strong', { children: 'MAC:' }),
                              ' ',
                              i.mac,
                            ],
                          }),
                          i.ip &&
                            s.jsxs('span', {
                              children: [
                                s.jsx('strong', { children: 'IP:' }),
                                ' ',
                                i.ip,
                              ],
                            }),
                          i.manufacturer &&
                            s.jsxs('span', {
                              children: [
                                s.jsx('strong', { children: 'Manufacturer:' }),
                                ' ',
                                i.manufacturer,
                              ],
                            }),
                        ],
                      }),
                    ],
                  }),
                  s.jsxs('div', {
                    className: `status-pill ${
                      ((g = i.status) == null ? void 0 : g.toLowerCase()) ||
                      'online'
                    }`,
                    children: [
                      s.jsx('div', { className: 'dot' }),
                      i.status || 'Online',
                    ],
                  }),
                ],
              }),
              s.jsxs('div', {
                className: 'cards-grid',
                children: [
                  s.jsxs('div', {
                    className: 'info-card',
                    children: [
                      s.jsx('h3', { children: '📋 Client Information' }),
                      s.jsxs('div', {
                        className: 'info-grid',
                        children: [
                          s.jsxs('div', {
                            className: 'info-item',
                            children: [
                              s.jsx('div', {
                                className: 'label',
                                children: 'Description',
                              }),
                              s.jsx('div', {
                                className: 'value',
                                children: i.description || '—',
                              }),
                            ],
                          }),
                          s.jsxs('div', {
                            className: 'info-item',
                            children: [
                              s.jsx('div', {
                                className: 'label',
                                children: 'User',
                              }),
                              s.jsx('div', {
                                className: 'value',
                                children: i.user || '—',
                              }),
                            ],
                          }),
                          s.jsxs('div', {
                            className: 'info-item',
                            children: [
                              s.jsx('div', {
                                className: 'label',
                                children: 'Operating System',
                              }),
                              s.jsx('div', {
                                className: 'value',
                                children: i.os || '—',
                              }),
                            ],
                          }),
                          s.jsxs('div', {
                            className: 'info-item',
                            children: [
                              s.jsx('div', {
                                className: 'label',
                                children: 'Manufacturer',
                              }),
                              s.jsx('div', {
                                className: 'value',
                                children: i.manufacturer || '—',
                              }),
                            ],
                          }),
                        ],
                      }),
                    ],
                  }),
                  s.jsxs('div', {
                    className: 'info-card',
                    children: [
                      s.jsx('h3', { children: '🌐 Network Information' }),
                      s.jsxs('div', {
                        className: 'info-grid',
                        children: [
                          s.jsxs('div', {
                            className: 'info-item',
                            children: [
                              s.jsx('div', {
                                className: 'label',
                                children: 'IP Address',
                              }),
                              s.jsx('div', {
                                className: 'value mono',
                                children: i.ip || '—',
                              }),
                            ],
                          }),
                          s.jsxs('div', {
                            className: 'info-item',
                            children: [
                              s.jsx('div', {
                                className: 'label',
                                children: 'IPv6 Address',
                              }),
                              s.jsx('div', {
                                className: 'value mono',
                                style: { fontSize: '11px' },
                                children: i.ip6 || '—',
                              }),
                            ],
                          }),
                          s.jsxs('div', {
                            className: 'info-item',
                            children: [
                              s.jsx('div', {
                                className: 'label',
                                children: 'VLAN',
                              }),
                              s.jsx('div', {
                                className: 'value',
                                children: i.vlan || '—',
                              }),
                            ],
                          }),
                          s.jsxs('div', {
                            className: 'info-item',
                            children: [
                              s.jsx('div', {
                                className: 'label',
                                children: 'SSID',
                              }),
                              s.jsx('div', {
                                className: 'value',
                                children: i.ssid || '—',
                              }),
                            ],
                          }),
                        ],
                      }),
                    ],
                  }),
                  s.jsxs('div', {
                    className: 'info-card',
                    children: [
                      s.jsx('h3', { children: '📊 Usage Statistics' }),
                      s.jsxs('div', {
                        className: 'info-grid',
                        children: [
                          s.jsxs('div', {
                            className: 'info-item',
                            children: [
                              s.jsx('div', {
                                className: 'label',
                                children: 'Data Sent',
                              }),
                              s.jsx('div', {
                                className: 'value success',
                                children: i.usage ? o(i.usage.sent) : '—',
                              }),
                            ],
                          }),
                          s.jsxs('div', {
                            className: 'info-item',
                            children: [
                              s.jsx('div', {
                                className: 'label',
                                children: 'Data Received',
                              }),
                              s.jsx('div', {
                                className: 'value primary',
                                children: i.usage ? o(i.usage.recv) : '—',
                              }),
                            ],
                          }),
                          s.jsxs('div', {
                            className: 'info-item',
                            children: [
                              s.jsx('div', {
                                className: 'label',
                                children: 'First Seen',
                              }),
                              s.jsx('div', {
                                className: 'value',
                                children: d(i.firstSeen),
                              }),
                            ],
                          }),
                          s.jsxs('div', {
                            className: 'info-item',
                            children: [
                              s.jsx('div', {
                                className: 'label',
                                children: 'Last Seen',
                              }),
                              s.jsx('div', {
                                className: 'value',
                                children: d(i.lastSeen),
                              }),
                            ],
                          }),
                        ],
                      }),
                    ],
                  }),
                  s.jsxs('div', {
                    className: 'info-card',
                    children: [
                      s.jsx('h3', { children: '🔗 Connected To' }),
                      s.jsxs('div', {
                        className: 'info-grid',
                        children: [
                          s.jsxs('div', {
                            className: 'info-item',
                            children: [
                              s.jsx('div', {
                                className: 'label',
                                children: 'Device',
                              }),
                              s.jsx('div', {
                                className: 'value',
                                children:
                                  i.recentDeviceName ||
                                  i.recentDeviceSerial ||
                                  '—',
                              }),
                            ],
                          }),
                          s.jsxs('div', {
                            className: 'info-item',
                            children: [
                              s.jsx('div', {
                                className: 'label',
                                children: 'Switch Port',
                              }),
                              s.jsx('div', {
                                className: 'value',
                                children: i.switchport || '—',
                              }),
                            ],
                          }),
                        ],
                      }),
                      i.recentDeviceSerial &&
                        s.jsx('button', {
                          onClick: () =>
                            t({
                              view: 'device',
                              deviceId: i.recentDeviceSerial,
                            }),
                          style: {
                            marginTop: '12px',
                            padding: '8px 16px',
                            borderRadius: 'var(--radius-md)',
                            border: 'none',
                            background: 'var(--primary)',
                            color: 'white',
                            cursor: 'pointer',
                            fontWeight: 500,
                          },
                          children: 'View Device',
                        }),
                    ],
                  }),
                ],
              }),
            ],
          })
        : s.jsxs('div', {
            children: [
              s.jsx('button', {
                onClick: r,
                className: 'back-button',
                children: '← Back to Dashboard',
              }),
              s.jsxs('div', {
                className: 'device-header',
                children: [
                  s.jsx('div', {
                    className: 'device-icon',
                    style: {
                      background: 'linear-gradient(135deg, #667eea, #764ba2)',
                    },
                    children: '👥',
                  }),
                  s.jsxs('div', {
                    className: 'device-info',
                    children: [
                      s.jsx('h1', { children: 'Connected Clients' }),
                      s.jsx('div', {
                        className: 'meta',
                        children: s.jsxs('span', {
                          children: [e.length, ' total clients'],
                        }),
                      }),
                    ],
                  }),
                ],
              }),
              s.jsx('div', {
                style: { marginBottom: '20px' },
                children: s.jsx('input', {
                  type: 'text',
                  placeholder:
                    'Search clients by name, MAC, IP, manufacturer...',
                  value: n,
                  onChange: (m) => l(m.target.value),
                  style: {
                    width: '100%',
                    padding: '12px 16px',
                    borderRadius: 'var(--radius-md)',
                    border: '1px solid var(--border)',
                    background: 'var(--bg-secondary)',
                    color: 'var(--text-primary)',
                    fontSize: '14px',
                  },
                }),
              }),
              s.jsx('div', {
                className: 'network-card',
                children: s.jsxs('table', {
                  className: 'device-table',
                  children: [
                    s.jsx('thead', {
                      children: s.jsxs('tr', {
                        children: [
                          s.jsx('th', { children: 'Client' }),
                          s.jsx('th', { children: 'IP Address' }),
                          s.jsx('th', { children: 'MAC Address' }),
                          s.jsx('th', { children: 'Manufacturer' }),
                          s.jsx('th', { children: 'SSID / Port' }),
                          s.jsx('th', { children: 'Usage' }),
                        ],
                      }),
                    }),
                    s.jsxs('tbody', {
                      children: [
                        u.map((m) =>
                          s.jsxs(
                            'tr',
                            {
                              className: 'device-row',
                              onClick: () => a(m),
                              children: [
                                s.jsx('td', {
                                  children: s.jsxs('div', {
                                    className: 'device-name-cell',
                                    children: [
                                      s.jsx('div', {
                                        className: 'device-icon',
                                        style: { fontSize: '20px' },
                                        children: v(m),
                                      }),
                                      s.jsxs('div', {
                                        children: [
                                          s.jsx('span', {
                                            className: 'name',
                                            children: m.description || m.mac,
                                          }),
                                          m.os &&
                                            s.jsx('div', {
                                              style: {
                                                fontSize: '12px',
                                                color: 'var(--text-muted)',
                                              },
                                              children: m.os,
                                            }),
                                        ],
                                      }),
                                    ],
                                  }),
                                }),
                                s.jsx('td', {
                                  className: 'device-model',
                                  children: m.ip || '—',
                                }),
                                s.jsx('td', {
                                  className: 'device-model',
                                  style: {
                                    fontFamily: 'monospace',
                                    fontSize: '12px',
                                  },
                                  children: m.mac,
                                }),
                                s.jsx('td', {
                                  className: 'device-model',
                                  children: m.manufacturer || '—',
                                }),
                                s.jsx('td', {
                                  children: s.jsx('span', {
                                    className: 'detail-badge',
                                    children: m.ssid || m.switchport || '—',
                                  }),
                                }),
                                s.jsx('td', {
                                  children: m.usage
                                    ? s.jsxs('span', {
                                        style: { fontSize: '12px' },
                                        children: [
                                          '↑',
                                          o(m.usage.sent),
                                          ' ↓',
                                          o(m.usage.recv),
                                        ],
                                      })
                                    : '—',
                                }),
                              ],
                            },
                            m.id || m.mac
                          )
                        ),
                        u.length === 0 &&
                          s.jsx('tr', {
                            children: s.jsx('td', {
                              colSpan: 6,
                              style: {
                                textAlign: 'center',
                                color: 'var(--text-muted)',
                                padding: '40px',
                              },
                              children: n
                                ? 'No clients match your search'
                                : 'No clients found',
                            }),
                          }),
                      ],
                    }),
                  ],
                }),
              }),
            ],
          });
    },
    cp = ({ hass: e, options: t, configEntryId: r, onClose: n }) => {
      const [l, i] = A.useState(t),
        [a, u] = A.useState(!1),
        o = (h) => {
          i((y) => ({ ...y, [h]: !y[h] }));
        },
        d = async () => {
          u(!0);
          try {
            e
              ? await e.callWS({
                  type: 'meraki_ha/update_options',
                  config_entry_id: r,
                  options: l,
                })
              : console.log('Saving options (dev):', l);
          } catch (h) {
            console.error('Failed to save options:', h),
              alert('Failed to save settings.');
          } finally {
            u(!1), n(), window.location.reload();
          }
        },
        v = [
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
        ],
        g = (h, y, k) => {
          const M = parseFloat(k);
          i((f) => {
            var c;
            return {
              ...f,
              sensor_ranges: {
                ...(f.sensor_ranges || {}),
                [h]: {
                  ...(((c = f.sensor_ranges) == null ? void 0 : c[h]) || {}),
                  [y]: isNaN(M) ? void 0 : M,
                },
              },
            };
          });
        },
        m = [
          {
            key: 'temperature',
            label: 'Temperature',
            unit: '°',
            defaultMin: 32,
            defaultMax: 100,
          },
          {
            key: 'humidity',
            label: 'Humidity',
            unit: '%',
            defaultMin: 0,
            defaultMax: 100,
          },
          {
            key: 'co2',
            label: 'CO₂',
            unit: 'ppm',
            defaultMin: 300,
            defaultMax: 2e3,
          },
          {
            key: 'tvoc',
            label: 'TVOC',
            unit: 'ppb',
            defaultMin: 0,
            defaultMax: 1e3,
          },
          {
            key: 'pm25',
            label: 'PM2.5',
            unit: 'µg/m³',
            defaultMin: 0,
            defaultMax: 150,
          },
          {
            key: 'noise',
            label: 'Noise',
            unit: 'dB',
            defaultMin: 30,
            defaultMax: 100,
          },
        ];
      return s.jsx('div', {
        className:
          'fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center z-50 p-4',
        children: s.jsxs('ha-card', {
          class:
            'p-6 w-full max-w-2xl bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 shadow-lg rounded-lg',
          style: {
            maxHeight: '90vh',
            display: 'flex',
            flexDirection: 'column',
          },
          children: [
            s.jsxs('div', {
              className: 'card-header flex justify-between items-center mb-4',
              children: [
                s.jsx('h2', {
                  className: 'text-xl font-bold',
                  children: 'Integration Settings',
                }),
                s.jsx('button', {
                  onClick: n,
                  className: 'text-gray-500 hover:text-gray-700',
                  children: s.jsx('ha-icon', { icon: 'mdi:close' }),
                }),
              ],
            }),
            s.jsxs('div', {
              className: 'card-content overflow-y-auto',
              style: { flex: 1 },
              children: [
                s.jsx('h3', {
                  className:
                    'text-lg font-semibold mb-3 text-gray-700 dark:text-gray-300',
                  children: 'Entity Settings',
                }),
                s.jsx('div', {
                  className: 'space-y-3 mb-6',
                  children: v.map((h) =>
                    s.jsxs(
                      'div',
                      {
                        className:
                          'flex items-center justify-between p-2 border-b border-gray-200 dark:border-gray-700',
                        children: [
                          s.jsxs('div', {
                            className: 'flex flex-col',
                            children: [
                              s.jsx('span', {
                                className: 'font-medium',
                                children: h.label,
                              }),
                              s.jsx('span', {
                                className:
                                  'text-sm text-gray-500 dark:text-gray-400',
                                children: h.description,
                              }),
                            ],
                          }),
                          s.jsx('ha-switch', {
                            checked: l[h.key] !== !1,
                            onClick: (y) => {
                              y.stopPropagation(), o(h.key);
                            },
                          }),
                        ],
                      },
                      h.key
                    )
                  ),
                }),
                s.jsx('h3', {
                  className:
                    'text-lg font-semibold mb-3 text-gray-700 dark:text-gray-300',
                  children: 'Sensor Gauge Ranges',
                }),
                s.jsx('p', {
                  className: 'text-sm text-gray-500 dark:text-gray-400 mb-4',
                  children:
                    'Customize the min/max values for sensor gauge displays. Leave empty for defaults.',
                }),
                s.jsx('div', {
                  className: 'grid grid-cols-1 md:grid-cols-2 gap-4 mb-6',
                  children: m.map((h) => {
                    var k;
                    const y =
                      ((k = l.sensor_ranges) == null ? void 0 : k[h.key]) ||
                      {};
                    return s.jsxs(
                      'div',
                      {
                        className:
                          'p-3 bg-gray-50 dark:bg-gray-700 rounded-lg',
                        children: [
                          s.jsxs('div', {
                            className: 'font-medium mb-2',
                            children: [h.label, ' (', h.unit, ')'],
                          }),
                          s.jsxs('div', {
                            className: 'flex gap-3',
                            children: [
                              s.jsxs('div', {
                                className: 'flex-1',
                                children: [
                                  s.jsx('label', {
                                    className:
                                      'text-xs text-gray-500 dark:text-gray-400',
                                    children: 'Min',
                                  }),
                                  s.jsx('input', {
                                    type: 'number',
                                    className:
                                      'w-full px-2 py-1 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm',
                                    placeholder: String(h.defaultMin),
                                    value: y.min ?? '',
                                    onChange: (M) =>
                                      g(h.key, 'min', M.target.value),
                                  }),
                                ],
                              }),
                              s.jsxs('div', {
                                className: 'flex-1',
                                children: [
                                  s.jsx('label', {
                                    className:
                                      'text-xs text-gray-500 dark:text-gray-400',
                                    children: 'Max',
                                  }),
                                  s.jsx('input', {
                                    type: 'number',
                                    className:
                                      'w-full px-2 py-1 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm',
                                    placeholder: String(h.defaultMax),
                                    value: y.max ?? '',
                                    onChange: (M) =>
                                      g(h.key, 'max', M.target.value),
                                  }),
                                ],
                              }),
                            ],
                          }),
                        ],
                      },
                      h.key
                    );
                  }),
                }),
              ],
            }),
            s.jsxs('div', {
              className:
                'card-actions flex justify-end mt-4 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700',
              children: [
                s.jsx('button', {
                  onClick: n,
                  className:
                    'px-4 py-2 rounded border border-gray-300 text-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700',
                  disabled: a,
                  children: 'Cancel',
                }),
                s.jsx('button', {
                  onClick: d,
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
    dp = {
      '--primary-color': '#03a9f4',
      '--accent-color': '#ff9800',
      '--primary-text-color': '#f1f5f9',
      '--secondary-text-color': '#94a3b8',
      '--disabled-text-color': '#64748b',
      '--primary-background-color': '#0f172a',
      '--secondary-background-color': '#1e293b',
      '--card-background-color': '#1e293b',
      '--divider-color': '#334155',
      '--tertiary-background-color': '#334155',
      '--success-color': '#10b981',
      '--warning-color': '#f59e0b',
      '--error-color': '#ef4444',
    },
    fp = {
      '--primary-color': '#03a9f4',
      '--accent-color': '#ff9800',
      '--primary-text-color': '#1e293b',
      '--secondary-text-color': '#475569',
      '--disabled-text-color': '#64748b',
      '--primary-background-color': '#f1f5f9',
      '--secondary-background-color': '#ffffff',
      '--card-background-color': '#ffffff',
      '--divider-color': '#cbd5e1',
      '--tertiary-background-color': '#e2e8f0',
      '--success-color': '#10b981',
      '--warning-color': '#f59e0b',
      '--error-color': '#ef4444',
    };
  function pp(e) {
    const t = getComputedStyle(document.documentElement)
      .getPropertyValue(e)
      .trim();
    if (t) return t;
    try {
      if (window.parent && window.parent !== window) {
        const r = getComputedStyle(window.parent.document.documentElement)
          .getPropertyValue(e)
          .trim();
        if (r) return r;
      }
    } catch {}
    return null;
  }
  function mp(e) {
    const t = e ? dp : fp,
      r = {};
    for (const [n, l] of Object.entries(t)) r[n] = pp(n) || l;
    return r;
  }
  function hp(e) {
    var l;
    const t =
        ((l = e == null ? void 0 : e.themes) == null ? void 0 : l.darkMode) ??
        !0,
      r = A.useMemo(() => mp(t), [t]),
      n = A.useMemo(() => {
        const i = {};
        for (const [a, u] of Object.entries(r)) i[a] = u;
        return (
          (i['--text-primary'] = r['--primary-text-color']),
          (i['--text-secondary'] = r['--secondary-text-color']),
          (i['--text-muted'] = r['--disabled-text-color']),
          (i['--bg-primary'] = r['--primary-background-color']),
          (i['--bg-secondary'] = r['--secondary-background-color']),
          (i['--bg-tertiary'] = r['--tertiary-background-color']),
          (i['--card-bg'] = r['--card-background-color']),
          (i['--card-border'] = r['--divider-color']),
          (i['--primary'] = r['--primary-color']),
          (i['--success'] = r['--success-color']),
          (i['--warning'] = r['--warning-color']),
          (i['--error'] = r['--error-color']),
          i
        );
      }, [r]);
    return (
      A.useEffect(() => {
        const i = document.documentElement;
        for (const [a, u] of Object.entries(r)) i.style.setProperty(a, u);
        i.style.setProperty('--text-primary', r['--primary-text-color']),
          i.style.setProperty('--text-secondary', r['--secondary-text-color']),
          i.style.setProperty('--text-muted', r['--disabled-text-color']),
          i.style.setProperty('--bg-primary', r['--primary-background-color']),
          i.style.setProperty(
            '--bg-secondary',
            r['--secondary-background-color']
          ),
          i.style.setProperty(
            '--bg-tertiary',
            r['--tertiary-background-color']
          ),
          i.style.setProperty('--card-bg', r['--card-background-color']),
          i.style.setProperty('--card-border', r['--divider-color']),
          i.style.setProperty('--primary', r['--primary-color']),
          i.style.setProperty('--success', r['--success-color']),
          i.style.setProperty('--warning', r['--warning-color']),
          i.style.setProperty('--error', r['--error-color']);
      }, [r]),
      { isDarkMode: t, themeVars: r, style: n }
    );
  }
  const _c = () =>
      s.jsxs('div', {
        className: 'loading-container',
        children: [
          s.jsx('div', { className: 'loading-spinner' }),
          s.jsx('span', {
            className: 'loading-text',
            children: 'Loading Meraki data...',
          }),
        ],
      }),
    gp = ({ message: e, onRetry: t }) =>
      s.jsxs('div', {
        className: 'error-container',
        children: [
          s.jsx('span', { className: 'error-icon', children: '⚠️' }),
          s.jsxs('div', {
            className: 'error-content',
            children: [
              s.jsx('h3', { children: 'Error Loading Data' }),
              s.jsx('p', { children: e }),
              t &&
                s.jsx('button', {
                  onClick: t,
                  className: 'retry-button',
                  children: 'Retry',
                }),
            ],
          }),
        ],
      }),
    Wl = ({ version: e, onSettingsClick: t }) =>
      s.jsxs('div', {
        className: 'meraki-header',
        children: [
          s.jsx('div', { className: 'logo', children: '🌐' }),
          s.jsx('h1', { children: 'Meraki Dashboard' }),
          e && s.jsxs('span', { className: 'version', children: ['v', e] }),
          s.jsx('div', {
            style: { marginLeft: 'auto', display: 'flex', gap: '8px' },
            children:
              t &&
              s.jsx('button', {
                onClick: t,
                className: 'settings-btn',
                title: 'Settings',
                style: {
                  background: 'var(--bg-tertiary)',
                  border: '1px solid var(--card-border)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '8px 12px',
                  color: 'var(--text-secondary)',
                  cursor: 'pointer',
                  fontSize: '14px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  transition: 'var(--transition)',
                },
                children: '⚙️ Settings',
              }),
          }),
        ],
      }),
    vp = ({ hass: e, panel: t, narrow: r }) => {
      var z, S;
      const [n, l] = A.useState(null),
        [i, a] = A.useState(!0),
        [u, o] = A.useState(null),
        [d, v] = A.useState({ view: 'dashboard' }),
        [g, m] = A.useState(!1),
        { style: h } = hp(e),
        y = A.useRef(e);
      y.current = e;
      const k = A.useRef(!1),
        M =
          (z = t == null ? void 0 : t.config) == null
            ? void 0
            : z.config_entry_id,
        f = A.useCallback(async () => {
          const C = y.current;
          if (!(!C || !M)) {
            a(!0), o(null);
            try {
              const P = await C.callWS({
                type: 'meraki_ha/get_config',
                config_entry_id: M,
              });
              if (P.networks && P.enabled_networks) {
                const W = P.networks.map((R) => ({
                  ...R,
                  is_enabled: P.enabled_networks.includes(R.id),
                }));
                P.networks = W;
              }
              l(P), (k.current = !0);
            } catch (P) {
              console.error('Failed to fetch Meraki data:', P),
                o(
                  P instanceof Error
                    ? P.message
                    : 'Failed to fetch data from Meraki integration'
                );
            } finally {
              a(!1);
            }
          }
        }, [M]);
      if (
        (A.useEffect(() => {
          e && M && !k.current && f();
        }, [e, M, f]),
        !e)
      )
        return s.jsxs('div', {
          className: 'meraki-panel',
          style: h,
          children: [
            s.jsx(_c, {}),
            s.jsx('p', {
              style: {
                textAlign: 'center',
                color: 'var(--text-secondary)',
                marginTop: '16px',
              },
              children: 'Waiting for Home Assistant connection...',
            }),
          ],
        });
      if (i)
        return s.jsxs('div', {
          className: 'meraki-panel',
          style: h,
          children: [s.jsx(Wl, {}), s.jsx(_c, {})],
        });
      if (u)
        return s.jsxs('div', {
          className: 'meraki-panel',
          style: h,
          children: [s.jsx(Wl, {}), s.jsx(gp, { message: u, onRetry: f })],
        });
      if (!n)
        return s.jsxs('div', {
          className: 'meraki-panel',
          style: h,
          children: [
            s.jsx(Wl, {}),
            s.jsxs('div', {
              className: 'empty-state',
              children: [
                s.jsx('div', { className: 'icon', children: '📡' }),
                s.jsx('h3', { children: 'No Data Available' }),
                s.jsx('p', {
                  children: 'Could not load Meraki data. Please try again.',
                }),
              ],
            }),
          ],
        });
      const c =
          ((S = n.networks) == null
            ? void 0
            : S.filter((C) => C.is_enabled)) || [],
        p = { ...n, networks: c },
        w = () => {
          switch (d.view) {
            case 'clients':
              return s.jsx(up, {
                clients: n.clients || [],
                setActiveView: v,
                onBack: () => v({ view: 'dashboard' }),
              });
            case 'device':
              return s.jsx(op, {
                activeView: d,
                setActiveView: v,
                data: n,
                hass: e,
                configEntryId: M,
                cameraLinkIntegration: n.camera_link_integration,
                configEntryOptions: { temperature_unit: n.temperature_unit },
              });
            default:
              return s.jsx(sp, {
                data: p,
                setActiveView: v,
                hass: e,
                defaultViewMode: n.dashboard_view_mode,
                defaultDeviceTypeFilter: n.dashboard_device_type_filter,
                defaultStatusFilter: n.dashboard_status_filter,
                temperatureUnit: n.temperature_unit,
              });
          }
        };
      return s.jsxs('div', {
        className: 'meraki-panel',
        style: h,
        children: [
          s.jsx(Wl, { version: n.version, onSettingsClick: () => m(!0) }),
          w(),
          g &&
            M &&
            s.jsx(cp, {
              hass: e,
              options: n,
              configEntryId: M,
              onClose: () => m(!1),
            }),
        ],
      });
    },
    Ec =
      '@import"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap";:root{--primary: #03a9f4;--primary-dark: #0288d1;--primary-light: rgba(3, 169, 244, .15);--success: #10b981;--success-light: rgba(16, 185, 129, .15);--warning: #f59e0b;--warning-light: rgba(245, 158, 11, .15);--error: #ef4444;--error-light: rgba(239, 68, 68, .15);--bg-primary: #0f172a;--bg-secondary: #1e293b;--bg-tertiary: #334155;--card-bg: #1e293b;--card-border: #334155;--text-primary: #f1f5f9;--text-secondary: #94a3b8;--text-muted: #64748b;--radius-sm: 8px;--radius-md: 12px;--radius-lg: 16px;--radius-xl: 20px;--shadow-sm: 0 1px 2px rgba(0, 0, 0, .3);--shadow-md: 0 4px 6px rgba(0, 0, 0, .3);--shadow-lg: 0 10px 25px rgba(0, 0, 0, .4);--transition: all .2s ease;--switch-color: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);--camera-color: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%);--wireless-color: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);--sensor-color: linear-gradient(135deg, #10b981 0%, #059669 100%);--appliance-color: linear-gradient(135deg, #f59e0b 0%, #d97706 100%)}*{box-sizing:border-box;margin:0;padding:0}.meraki-panel{font-family:var( --paper-font-body1_-_font-family, "Inter", -apple-system, BlinkMacSystemFont, sans-serif );background:var(--bg-primary);min-height:100vh;color:var(--text-primary);padding:24px;max-width:1600px;margin:0 auto;width:100%}.meraki-header{display:flex;align-items:center;gap:16px;margin-bottom:32px}.meraki-header .logo{width:48px;height:48px;background:linear-gradient(135deg,var(--primary) 0%,#06b6d4 100%);border-radius:var(--radius-md);display:flex;align-items:center;justify-content:center;font-size:24px;box-shadow:var(--shadow-md)}.meraki-header h1{font-size:28px;font-weight:600;background:linear-gradient(90deg,#fff 0%,var(--text-secondary) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}.meraki-header .version{font-size:12px;color:var(--text-muted);background:var(--bg-tertiary);padding:4px 10px;border-radius:12px}.nav-tabs{display:flex;gap:8px;margin-bottom:24px;background:var(--card-bg);padding:6px;border-radius:var(--radius-lg);border:1px solid var(--card-border)}.nav-tab{padding:10px 20px;border:none;background:transparent;color:var(--text-secondary);font-size:14px;font-weight:500;border-radius:var(--radius-sm);cursor:pointer;transition:var(--transition);font-family:inherit}.nav-tab:hover{color:var(--text-primary);background:var(--bg-tertiary)}.nav-tab.active{background:var(--primary);color:#fff}.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;margin-bottom:24px}.stat-card{background:var(--card-bg);border:1px solid var(--card-border);border-radius:var(--radius-lg);padding:20px;transition:var(--transition)}.stat-card:hover{border-color:var(--primary);transform:translateY(-2px);box-shadow:var(--shadow-lg)}.stat-card .label{font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px;font-weight:500;opacity:.7}.stat-card .value{font-size:32px;font-weight:700;color:var(--primary);text-shadow:0 0 1px currentColor}.stat-card .value.success{color:var(--success)!important}.stat-card .value.warning{color:var(--warning)!important}.stat-card .value.error{color:var(--error)!important}.stat-card .value.default{color:var(--text-primary)!important;font-weight:600}.network-card{background:var(--card-bg);border:1px solid var(--card-border);border-radius:var(--radius-lg);overflow:hidden;margin-bottom:24px}.network-header{display:flex;align-items:center;justify-content:space-between;padding:20px 24px;border-bottom:1px solid var(--card-border);background:var(--bg-secondary);cursor:pointer;transition:var(--transition)}.network-header:hover{background:var(--bg-tertiary)}.network-header .title{display:flex;align-items:center;gap:12px}.network-header .network-icon{color:var(--primary);font-size:24px}.network-header h2{font-size:20px;font-weight:600;margin:0}.network-header .badge{background:var(--success);color:#fff;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:500}.network-header .expand-icon{color:var(--text-secondary);transition:transform .2s}.network-header .expand-icon.expanded{transform:rotate(180deg)}.device-table{width:100%;border-collapse:collapse}.device-table th{text-align:left;padding:16px 24px;font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid var(--card-border)}.device-table td{padding:16px 24px;border-bottom:1px solid var(--card-border);vertical-align:middle}.device-table tr:last-child td{border-bottom:none}.device-table tr:hover td{background:var(--bg-secondary)}.device-table th:first-child,.device-table td:first-child{position:sticky;left:0;background:var(--card-bg);z-index:1}.device-row{cursor:pointer;transition:var(--transition)}.device-name-cell{display:flex;align-items:center;gap:12px}.device-icon{width:40px;height:40px;border-radius:var(--radius-sm);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0}.device-icon.switch{background:var(--switch-color)}.device-icon.camera{background:var(--camera-color)}.device-icon.wireless{background:var(--wireless-color)}.device-icon.sensor{background:var(--sensor-color)}.device-icon.appliance{background:var(--appliance-color)}.device-name-cell .name{font-weight:500;color:var(--text-primary)}.device-model{color:var(--text-secondary);font-size:14px}.status-badge{display:inline-flex;align-items:center;gap:6px;font-weight:500;font-size:14px}.status-dot{width:8px;height:8px;border-radius:50%}.status-badge.online .status-dot{background:var(--success);box-shadow:0 0 8px var(--success)}.status-badge.online{color:var(--success)}.status-badge.offline .status-dot{background:var(--error);box-shadow:0 0 8px var(--error)}.status-badge.offline{color:var(--error)}.status-badge.alerting .status-dot{background:var(--warning);box-shadow:0 0 8px var(--warning)}.status-badge.alerting{color:var(--warning)}.detail-badge{background:var(--bg-tertiary);color:var(--text-primary);border:1px solid var(--card-border);padding:4px 10px;border-radius:6px;font-size:13px;font-weight:500}.ssid-section{padding:20px 24px;border-top:1px solid var(--card-border)}.ssid-section h3{font-size:14px;color:var(--text-muted);margin-bottom:16px;display:flex;align-items:center;gap:8px;font-weight:500}.ssid-list{display:flex;gap:12px;flex-wrap:wrap}.ssid-item{background:var(--bg-secondary);border:1px solid var(--card-border);border-radius:var(--radius-sm);padding:12px 16px;display:flex;align-items:center;gap:10px;transition:var(--transition)}.ssid-item:hover{border-color:var(--primary);background:var(--bg-tertiary)}.ssid-item .icon{color:var(--primary);font-size:20px}.ssid-item .name{font-weight:500}.ssid-item .clients{color:var(--text-muted);font-size:13px}.toggle{width:44px;height:24px;background:var(--bg-tertiary);border-radius:12px;position:relative;cursor:pointer;transition:var(--transition)}.toggle.active{background:var(--success)}.toggle:after{content:"";position:absolute;width:20px;height:20px;background:#fff;border-radius:50%;top:2px;left:2px;box-shadow:var(--shadow-sm);transition:left .2s}.toggle.active:after{left:22px}.back-button{display:inline-flex;align-items:center;gap:8px;color:var(--primary);font-weight:500;margin-bottom:24px;background:none;border:none;font-size:14px;cursor:pointer;padding:0;font-family:inherit}.back-button:hover{text-decoration:underline}.device-header{display:flex;align-items:flex-start;gap:24px;margin-bottom:32px}.device-header .device-icon{width:72px;height:72px;border-radius:var(--radius-xl);display:flex;align-items:center;justify-content:center;font-size:32px;flex-shrink:0}.device-header .device-info h1{font-size:28px;font-weight:600;margin-bottom:8px;color:var(--text-primary)}.device-header .device-info .meta{display:flex;gap:24px;color:var(--text-secondary);font-size:14px;flex-wrap:wrap}.device-header .device-info .meta span strong{color:var(--text-muted);font-weight:400;margin-right:4px}.device-header .status-pill{display:inline-flex;align-items:center;gap:6px;background:var(--success-light);color:var(--success);padding:6px 14px;border-radius:20px;font-weight:500;font-size:14px;margin-left:auto}.device-header .status-pill .dot{width:8px;height:8px;background:var(--success);border-radius:50%;box-shadow:0 0 8px var(--success)}.cards-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:24px;margin-bottom:24px}.info-card{background:var(--card-bg);border:1px solid var(--card-border);border-radius:var(--radius-lg);padding:24px}.info-card h3{font-size:14px;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:20px;display:flex;align-items:center;gap:8px;font-weight:600}.info-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}.info-item .label{font-size:11px;color:var(--text-muted);margin-bottom:6px;text-transform:uppercase;letter-spacing:.5px;font-weight:500;opacity:.7}.info-item .value{font-size:16px;font-weight:600;color:var(--text-primary);opacity:1}.info-item .value.primary{color:var(--primary)!important}.info-item .value.success{color:var(--success)!important}.info-item .value.warning{color:var(--warning)!important}.info-item .value.error{color:var(--error)!important}.info-item .value.mono{font-family:SF Mono,Monaco,Consolas,monospace;font-size:14px}.port-visualization{background:var(--bg-primary);border-radius:var(--radius-md);padding:24px;margin-bottom:24px}.switch-chassis{background:var(--bg-tertiary);border-radius:var(--radius-sm);padding:16px 20px;display:flex;flex-direction:column;gap:12px;border:2px solid var(--card-border)}.switch-label{display:flex;justify-content:space-between;align-items:center;font-size:12px;color:var(--text-secondary)}.ports-row{display:flex;gap:6px;flex-wrap:wrap}.port{width:40px;height:32px;background:var(--bg-primary);border-radius:4px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;position:relative;border:2px solid var(--card-border);transition:var(--transition)}.port:hover{transform:translateY(-2px);border-color:var(--primary)}.port.connected{background:#10b98133;border-color:var(--success)}.port.connected:before{content:"";width:6px;height:6px;background:var(--success);border-radius:50%;box-shadow:0 0 6px var(--success)}.port.selected{border-color:var(--primary);box-shadow:0 0 12px var(--primary)}.port .num{font-size:9px;color:var(--text-muted);position:absolute;bottom:2px}.port .poe{position:absolute;top:-8px;right:-4px;font-size:12px;color:var(--warning);text-shadow:0 0 4px var(--warning)}.port-legend{display:flex;gap:24px;margin-top:16px;font-size:13px;color:var(--text-muted)}.port-legend span{display:flex;align-items:center;gap:6px}.port-legend .dot{width:10px;height:10px;border-radius:50%}.port-legend .dot.connected{background:var(--success)}.port-legend .dot.disconnected{background:var(--text-muted)}.port-details{background:var(--card-bg);border:1px solid var(--card-border);border-radius:var(--radius-lg);padding:20px;margin-top:16px}.port-details h4{font-size:16px;margin-bottom:16px;display:flex;align-items:center;gap:8px}.client-info{background:var(--primary-light);border-radius:var(--radius-sm);padding:16px;display:flex;align-items:center;gap:16px}.client-avatar{width:48px;height:48px;background:linear-gradient(135deg,var(--primary) 0%,#06b6d4 100%);border-radius:var(--radius-md);display:flex;align-items:center;justify-content:center;font-size:24px}.client-details .name{font-weight:600;margin-bottom:4px}.client-details .mac{font-size:13px;color:var(--text-muted);font-family:monospace}.port-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(100px,1fr));gap:16px;margin-top:16px}.port-stat .label{font-size:11px;color:var(--text-muted);text-transform:uppercase}.port-stat .value{font-size:18px;font-weight:600;color:var(--text-primary)}.readings-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:24px;margin-bottom:24px}.reading-card{background:var(--card-bg);border:1px solid var(--card-border);border-radius:var(--radius-lg);padding:32px;text-align:center}.reading-card .icon-wrapper{width:80px;height:80px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 20px;font-size:36px}.reading-card.temperature .icon-wrapper{background:#f9731626;color:#f97316}.reading-card.humidity .icon-wrapper{background:#06b6d426;color:#06b6d4}.reading-card.tvoc .icon-wrapper,.reading-card.pm25 .icon-wrapper,.reading-card.co2 .icon-wrapper{background:#84cc1626;color:#84cc16}.reading-card.indoorAirQuality .icon-wrapper{background:#22c55e26;color:#22c55e}.reading-card.noise .icon-wrapper{background:#8b5cf626;color:#8b5cf6}.reading-card .reading-label{font-size:14px;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px;margin-bottom:12px}.reading-card .reading-value{font-size:48px;font-weight:700;line-height:1;margin-bottom:8px}.reading-card.temperature .reading-value{color:#f97316}.reading-card.humidity .reading-value{color:#06b6d4}.reading-card.tvoc .reading-value,.reading-card.pm25 .reading-value,.reading-card.co2 .reading-value{color:#84cc16}.reading-card.indoorAirQuality .reading-value{color:#22c55e}.reading-card.noise .reading-value{color:#8b5cf6}.reading-card .reading-unit{font-size:24px;font-weight:400;opacity:.7}.reading-card .reading-status{font-size:14px;color:var(--success);display:flex;align-items:center;justify-content:center;gap:6px;margin-top:16px}.gauge-wrapper{width:100%;height:8px;background:var(--bg-tertiary);border-radius:4px;margin-top:20px;overflow:hidden}.gauge-fill{height:100%;border-radius:4px;transition:width .5s ease}.gauge-fill.temp{background:linear-gradient(90deg,#22c55e,#eab308,#ef4444)}.gauge-fill.humidity{background:#06b6d4}.gauge-fill.air-quality{background:linear-gradient(90deg,#22c55e,#84cc16,#eab308,#f97316,#ef4444)}.gauge-fill.noise{background:linear-gradient(90deg,#22c55e,#06b6d4,#8b5cf6)}.gauge-fill.battery{background:linear-gradient(90deg,#ef4444,#eab308,#22c55e 50%,#22c55e)}.gauge-fill.default{background:var(--text-muted)}.gauge-labels{display:flex;justify-content:space-between;font-size:11px;color:var(--text-muted);margin-top:6px}.loading-container{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:64px}.loading-spinner{width:48px;height:48px;border:3px solid var(--card-border);border-top-color:var(--primary);border-radius:50%;animation:spin 1s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}.loading-text{margin-top:16px;color:var(--text-secondary);font-size:14px}.error-container{background:var(--error-light);border:1px solid rgba(239,68,68,.3);border-radius:var(--radius-md);padding:20px;display:flex;align-items:flex-start;gap:16px}.error-icon{color:var(--error);font-size:24px;flex-shrink:0}.error-content h3{margin:0 0 8px;font-size:16px;color:var(--error)}.error-content p{margin:0;font-size:14px;color:var(--text-primary)}.retry-button{margin-top:16px;padding:10px 20px;background:var(--error);color:#fff;border:none;border-radius:var(--radius-sm);font-size:14px;font-weight:500;cursor:pointer;transition:var(--transition);font-family:inherit}.retry-button:hover{background:#dc2626;transform:translateY(-1px)}.empty-state{text-align:center;padding:64px 24px;color:var(--text-secondary)}.empty-state .icon{font-size:64px;opacity:.3;margin-bottom:16px}.empty-state h3{font-size:18px;margin-bottom:8px;color:var(--text-primary)}.empty-state p{font-size:14px}.metric-card{background:var(--card-bg);border:1px solid var(--card-border);border-radius:var(--radius-lg);padding:24px;text-align:center;transition:var(--transition)}.metric-card.clickable{cursor:pointer}.metric-card.clickable:hover{border-color:var(--primary);transform:translateY(-2px);box-shadow:var(--shadow-lg)}.metric-icon-wrapper{width:64px;height:64px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 16px}.metric-icon{font-size:28px}.metric-icon-primary{background:var(--primary-light);color:var(--primary)}.metric-icon-success{background:var(--success-light);color:var(--success)}.metric-icon-warning{background:var(--warning-light);color:var(--warning)}.metric-icon-error{background:var(--error-light);color:var(--error)}.metric-icon-info{background:#06b6d426;color:#06b6d4}.metric-icon-purple{background:#8b5cf626;color:#8b5cf6}.metric-label{font-size:12px;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;font-weight:500}.metric-value{font-size:36px;font-weight:700;line-height:1;margin-bottom:4px;color:var(--text-primary)}.metric-unit{font-size:18px;font-weight:400;opacity:.7;margin-left:2px}.metric-secondary{font-size:14px;color:var(--text-secondary);margin-bottom:8px}.metric-status{font-size:13px;display:flex;align-items:center;justify-content:center;gap:6px;margin-top:12px}.metric-status-normal{color:var(--success)}.metric-status-warning{color:var(--warning)}.metric-status-critical{color:var(--error)}.metric-status-inactive{color:var(--text-muted)}.metric-gauge-wrapper{width:100%;height:6px;background:var(--bg-tertiary);border-radius:3px;margin-top:16px;overflow:hidden}.metric-gauge-fill{height:100%;border-radius:3px;transition:width .5s ease}.metric-gauge-primary{background:var(--primary)}.metric-gauge-success{background:var(--success)}.metric-gauge-warning{background:linear-gradient(90deg,var(--success) 0%,var(--warning) 100%)}.metric-gauge-error{background:linear-gradient(90deg,var(--warning) 0%,var(--error) 100%)}.metric-gauge-info{background:#06b6d4}.metric-gauge-purple{background:#8b5cf6}.metric-gauge-labels{display:flex;justify-content:space-between;font-size:10px;color:var(--text-muted);margin-top:4px}.metric-cards-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin-bottom:24px}@media (max-width: 768px){.metric-cards-grid{grid-template-columns:repeat(2,1fr)}.metric-card{padding:16px}.metric-icon-wrapper{width:48px;height:48px;margin-bottom:12px}.metric-icon{font-size:22px}.metric-value{font-size:28px}.metric-unit{font-size:14px}}@media (max-width: 480px){.metric-cards-grid{grid-template-columns:1fr 1fr;gap:12px}.metric-card{padding:12px}.metric-value{font-size:24px}.metric-label{font-size:10px}}.text-primary{color:var(--primary)}.text-success{color:var(--success)}.text-warning{color:var(--warning)}.text-error{color:var(--error)}.text-muted{color:var(--text-muted)}.font-mono{font-family:monospace}.font-medium{font-weight:500}.font-semibold{font-weight:600}.font-bold{font-weight:700}.table-wrapper{width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch}.filter-controls{display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap;align-items:center}@media (max-width: 640px){.filter-controls{flex-direction:column;align-items:stretch;gap:8px}.filter-controls select,.filter-controls button{width:100%}.view-mode-toggle{order:-1;width:100%}.view-mode-toggle button{flex:1}}@media (max-width: 1024px){.info-grid{grid-template-columns:1fr 1fr}.port-stats{grid-template-columns:repeat(3,1fr)}}@media (max-width: 768px){.meraki-panel{padding:16px}.meraki-header h1{font-size:22px}.meraki-header .version{display:none}.stats-grid{grid-template-columns:repeat(2,1fr)}.info-card{overflow-x:auto}.device-table{min-width:500px}.device-table th,.device-table td{padding:12px 16px;font-size:13px;white-space:nowrap}.device-table th:first-child,.device-table td:first-child{white-space:normal;min-width:150px}.device-header{flex-direction:column;gap:16px}.device-header .status-pill{margin-left:0}.cards-grid,.info-grid{grid-template-columns:1fr}.port-stats{grid-template-columns:repeat(2,1fr)}.port-details{padding:16px}.client-info{flex-direction:column;text-align:center;gap:12px}.readings-grid{grid-template-columns:1fr}.reading-card{padding:24px}.reading-card .reading-value{font-size:36px}.nav-tabs{flex-wrap:wrap}.nav-tab{padding:8px 14px;font-size:13px}}@media (max-width: 480px){.meraki-panel{padding:12px}.meraki-header{gap:12px}.meraki-header .logo{width:40px;height:40px;font-size:20px}.meraki-header h1{font-size:18px}.stats-grid{grid-template-columns:1fr 1fr;gap:12px}.stat-card{padding:16px}.stat-card .value{font-size:24px}.device-table th,.device-table td{padding:10px 12px;font-size:12px}.device-icon{width:32px;height:32px;font-size:14px}.device-name-cell{gap:8px}.device-name-cell .name{font-size:14px}.device-model{font-size:12px}.info-card{padding:16px}.info-card h3{font-size:13px;margin-bottom:16px}.port-stats{grid-template-columns:1fr 1fr;gap:12px}.port-stat .value{font-size:16px}.switch-chassis{padding:12px 16px}.port{width:32px;height:28px}.port .num{font-size:8px}.port-legend{flex-wrap:wrap;gap:12px;font-size:12px}.back-button{font-size:13px}}';
  class xp extends HTMLElement {
    constructor() {
      super(...arguments);
      Wt(this, '_hass', null);
      Wt(this, '_panel', null);
      Wt(this, '_narrow', !1);
      Wt(this, '_route', null);
      Wt(this, '_root', null);
      Wt(this, '_mountPoint', null);
      Wt(this, '_styleEl', null);
    }
    connectedCallback() {
      if (
        ((this._styleEl = document.createElement('style')),
        (this._styleEl.textContent = Ec),
        this.appendChild(this._styleEl),
        !document.getElementById('meraki-panel-styles'))
      ) {
        const r = document.createElement('style');
        (r.id = 'meraki-panel-styles'),
          (r.textContent = Ec),
          document.head.appendChild(r);
      }
      (this._mountPoint = document.createElement('div')),
        (this._mountPoint.id = 'meraki-panel-root'),
        (this._mountPoint.style.height = '100%'),
        (this._mountPoint.style.width = '100%'),
        this.appendChild(this._mountPoint),
        (this._root = Yl.createRoot(this._mountPoint)),
        this._render();
    }
    disconnectedCallback() {
      this._root && (this._root.unmount(), (this._root = null)),
        this._mountPoint &&
          (this._mountPoint.remove(), (this._mountPoint = null)),
        this._styleEl && (this._styleEl.remove(), (this._styleEl = null));
    }
    set hass(r) {
      (this._hass = r), this._render();
    }
    get hass() {
      return this._hass;
    }
    set panel(r) {
      (this._panel = r), this._render();
    }
    get panel() {
      return this._panel;
    }
    set narrow(r) {
      (this._narrow = r), this._render();
    }
    get narrow() {
      return this._narrow;
    }
    set route(r) {
      (this._route = r), this._render();
    }
    get route() {
      return this._route;
    }
    _render() {
      !this._root ||
        !this._hass ||
        this._root.render(
          s.jsx(Fe.StrictMode, {
            children: s.jsx(vp, {
              hass: this._hass,
              panel: this._panel,
              narrow: this._narrow,
              route: this._route,
            }),
          })
        );
    }
  }
  customElements.get('meraki-panel') ||
    customElements.define('meraki-panel', xp);
})();
//# sourceMappingURL=meraki-panel.js.map
