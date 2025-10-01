var Z_ = Object.defineProperty;
var J_ = (Q, B, k) => B in Q ? Z_(Q, B, { enumerable: !0, configurable: !0, writable: !0, value: k }) : Q[B] = k;
var Pm = (Q, B, k) => (J_(Q, typeof B != "symbol" ? B + "" : B, k), k);
function ek(Q) {
  return Q && Q.__esModule && Object.prototype.hasOwnProperty.call(Q, "default") ? Q.default : Q;
}
var h0 = { exports: {} }, Qp = {}, m0 = { exports: {} }, Tt = {};
/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var J1;
function tk() {
  if (J1)
    return Tt;
  J1 = 1;
  var Q = Symbol.for("react.element"), B = Symbol.for("react.portal"), k = Symbol.for("react.fragment"), Ze = Symbol.for("react.strict_mode"), Dt = Symbol.for("react.profiler"), $e = Symbol.for("react.provider"), S = Symbol.for("react.context"), ut = Symbol.for("react.forward_ref"), de = Symbol.for("react.suspense"), se = Symbol.for("react.memo"), nt = Symbol.for("react.lazy"), re = Symbol.iterator;
  function pe(_) {
    return _ === null || typeof _ != "object" ? null : (_ = re && _[re] || _["@@iterator"], typeof _ == "function" ? _ : null);
  }
  var ue = { isMounted: function() {
    return !1;
  }, enqueueForceUpdate: function() {
  }, enqueueReplaceState: function() {
  }, enqueueSetState: function() {
  } }, Ye = Object.assign, bt = {};
  function ht(_, V, Ue) {
    this.props = _, this.context = V, this.refs = bt, this.updater = Ue || ue;
  }
  ht.prototype.isReactComponent = {}, ht.prototype.setState = function(_, V) {
    if (typeof _ != "object" && typeof _ != "function" && _ != null)
      throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
    this.updater.enqueueSetState(this, _, V, "setState");
  }, ht.prototype.forceUpdate = function(_) {
    this.updater.enqueueForceUpdate(this, _, "forceUpdate");
  };
  function pn() {
  }
  pn.prototype = ht.prototype;
  function ot(_, V, Ue) {
    this.props = _, this.context = V, this.refs = bt, this.updater = Ue || ue;
  }
  var qe = ot.prototype = new pn();
  qe.constructor = ot, Ye(qe, ht.prototype), qe.isPureReactComponent = !0;
  var mt = Array.isArray, Oe = Object.prototype.hasOwnProperty, ft = { current: null }, Ve = { key: !0, ref: !0, __self: !0, __source: !0 };
  function rn(_, V, Ue) {
    var Pe, rt = {}, tt = null, St = null;
    if (V != null)
      for (Pe in V.ref !== void 0 && (St = V.ref), V.key !== void 0 && (tt = "" + V.key), V)
        Oe.call(V, Pe) && !Ve.hasOwnProperty(Pe) && (rt[Pe] = V[Pe]);
    var st = arguments.length - 2;
    if (st === 1)
      rt.children = Ue;
    else if (1 < st) {
      for (var ct = Array(st), en = 0; en < st; en++)
        ct[en] = arguments[en + 2];
      rt.children = ct;
    }
    if (_ && _.defaultProps)
      for (Pe in st = _.defaultProps, st)
        rt[Pe] === void 0 && (rt[Pe] = st[Pe]);
    return { $$typeof: Q, type: _, key: tt, ref: St, props: rt, _owner: ft.current };
  }
  function _n(_, V) {
    return { $$typeof: Q, type: _.type, key: V, ref: _.ref, props: _.props, _owner: _._owner };
  }
  function Wt(_) {
    return typeof _ == "object" && _ !== null && _.$$typeof === Q;
  }
  function Ot(_) {
    var V = { "=": "=0", ":": "=2" };
    return "$" + _.replace(/[=:]/g, function(Ue) {
      return V[Ue];
    });
  }
  var Cn = /\/+/g;
  function ze(_, V) {
    return typeof _ == "object" && _ !== null && _.key != null ? Ot("" + _.key) : V.toString(36);
  }
  function Je(_, V, Ue, Pe, rt) {
    var tt = typeof _;
    (tt === "undefined" || tt === "boolean") && (_ = null);
    var St = !1;
    if (_ === null)
      St = !0;
    else
      switch (tt) {
        case "string":
        case "number":
          St = !0;
          break;
        case "object":
          switch (_.$$typeof) {
            case Q:
            case B:
              St = !0;
          }
      }
    if (St)
      return St = _, rt = rt(St), _ = Pe === "" ? "." + ze(St, 0) : Pe, mt(rt) ? (Ue = "", _ != null && (Ue = _.replace(Cn, "$&/") + "/"), Je(rt, V, Ue, "", function(en) {
        return en;
      })) : rt != null && (Wt(rt) && (rt = _n(rt, Ue + (!rt.key || St && St.key === rt.key ? "" : ("" + rt.key).replace(Cn, "$&/") + "/") + _)), V.push(rt)), 1;
    if (St = 0, Pe = Pe === "" ? "." : Pe + ":", mt(_))
      for (var st = 0; st < _.length; st++) {
        tt = _[st];
        var ct = Pe + ze(tt, st);
        St += Je(tt, V, Ue, ct, rt);
      }
    else if (ct = pe(_), typeof ct == "function")
      for (_ = ct.call(_), st = 0; !(tt = _.next()).done; )
        tt = tt.value, ct = Pe + ze(tt, st++), St += Je(tt, V, Ue, ct, rt);
    else if (tt === "object")
      throw V = String(_), Error("Objects are not valid as a React child (found: " + (V === "[object Object]" ? "object with keys {" + Object.keys(_).join(", ") + "}" : V) + "). If you meant to render a collection of children, use an array instead.");
    return St;
  }
  function Ft(_, V, Ue) {
    if (_ == null)
      return _;
    var Pe = [], rt = 0;
    return Je(_, Pe, "", "", function(tt) {
      return V.call(Ue, tt, rt++);
    }), Pe;
  }
  function _t(_) {
    if (_._status === -1) {
      var V = _._result;
      V = V(), V.then(function(Ue) {
        (_._status === 0 || _._status === -1) && (_._status = 1, _._result = Ue);
      }, function(Ue) {
        (_._status === 0 || _._status === -1) && (_._status = 2, _._result = Ue);
      }), _._status === -1 && (_._status = 0, _._result = V);
    }
    if (_._status === 1)
      return _._result.default;
    throw _._result;
  }
  var me = { current: null }, J = { transition: null }, be = { ReactCurrentDispatcher: me, ReactCurrentBatchConfig: J, ReactCurrentOwner: ft };
  function ae() {
    throw Error("act(...) is not supported in production builds of React.");
  }
  return Tt.Children = { map: Ft, forEach: function(_, V, Ue) {
    Ft(_, function() {
      V.apply(this, arguments);
    }, Ue);
  }, count: function(_) {
    var V = 0;
    return Ft(_, function() {
      V++;
    }), V;
  }, toArray: function(_) {
    return Ft(_, function(V) {
      return V;
    }) || [];
  }, only: function(_) {
    if (!Wt(_))
      throw Error("React.Children.only expected to receive a single React element child.");
    return _;
  } }, Tt.Component = ht, Tt.Fragment = k, Tt.Profiler = Dt, Tt.PureComponent = ot, Tt.StrictMode = Ze, Tt.Suspense = de, Tt.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = be, Tt.act = ae, Tt.cloneElement = function(_, V, Ue) {
    if (_ == null)
      throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + _ + ".");
    var Pe = Ye({}, _.props), rt = _.key, tt = _.ref, St = _._owner;
    if (V != null) {
      if (V.ref !== void 0 && (tt = V.ref, St = ft.current), V.key !== void 0 && (rt = "" + V.key), _.type && _.type.defaultProps)
        var st = _.type.defaultProps;
      for (ct in V)
        Oe.call(V, ct) && !Ve.hasOwnProperty(ct) && (Pe[ct] = V[ct] === void 0 && st !== void 0 ? st[ct] : V[ct]);
    }
    var ct = arguments.length - 2;
    if (ct === 1)
      Pe.children = Ue;
    else if (1 < ct) {
      st = Array(ct);
      for (var en = 0; en < ct; en++)
        st[en] = arguments[en + 2];
      Pe.children = st;
    }
    return { $$typeof: Q, type: _.type, key: rt, ref: tt, props: Pe, _owner: St };
  }, Tt.createContext = function(_) {
    return _ = { $$typeof: S, _currentValue: _, _currentValue2: _, _threadCount: 0, Provider: null, Consumer: null, _defaultValue: null, _globalName: null }, _.Provider = { $$typeof: $e, _context: _ }, _.Consumer = _;
  }, Tt.createElement = rn, Tt.createFactory = function(_) {
    var V = rn.bind(null, _);
    return V.type = _, V;
  }, Tt.createRef = function() {
    return { current: null };
  }, Tt.forwardRef = function(_) {
    return { $$typeof: ut, render: _ };
  }, Tt.isValidElement = Wt, Tt.lazy = function(_) {
    return { $$typeof: nt, _payload: { _status: -1, _result: _ }, _init: _t };
  }, Tt.memo = function(_, V) {
    return { $$typeof: se, type: _, compare: V === void 0 ? null : V };
  }, Tt.startTransition = function(_) {
    var V = J.transition;
    J.transition = {};
    try {
      _();
    } finally {
      J.transition = V;
    }
  }, Tt.unstable_act = ae, Tt.useCallback = function(_, V) {
    return me.current.useCallback(_, V);
  }, Tt.useContext = function(_) {
    return me.current.useContext(_);
  }, Tt.useDebugValue = function() {
  }, Tt.useDeferredValue = function(_) {
    return me.current.useDeferredValue(_);
  }, Tt.useEffect = function(_, V) {
    return me.current.useEffect(_, V);
  }, Tt.useId = function() {
    return me.current.useId();
  }, Tt.useImperativeHandle = function(_, V, Ue) {
    return me.current.useImperativeHandle(_, V, Ue);
  }, Tt.useInsertionEffect = function(_, V) {
    return me.current.useInsertionEffect(_, V);
  }, Tt.useLayoutEffect = function(_, V) {
    return me.current.useLayoutEffect(_, V);
  }, Tt.useMemo = function(_, V) {
    return me.current.useMemo(_, V);
  }, Tt.useReducer = function(_, V, Ue) {
    return me.current.useReducer(_, V, Ue);
  }, Tt.useRef = function(_) {
    return me.current.useRef(_);
  }, Tt.useState = function(_) {
    return me.current.useState(_);
  }, Tt.useSyncExternalStore = function(_, V, Ue) {
    return me.current.useSyncExternalStore(_, V, Ue);
  }, Tt.useTransition = function() {
    return me.current.useTransition();
  }, Tt.version = "18.3.1", Tt;
}
var Xp = { exports: {} };
/**
 * @license React
 * react.development.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
Xp.exports;
var eR;
function nk() {
  return eR || (eR = 1, function(Q, B) {
    process.env.NODE_ENV !== "production" && function() {
      typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart(new Error());
      var k = "18.3.1", Ze = Symbol.for("react.element"), Dt = Symbol.for("react.portal"), $e = Symbol.for("react.fragment"), S = Symbol.for("react.strict_mode"), ut = Symbol.for("react.profiler"), de = Symbol.for("react.provider"), se = Symbol.for("react.context"), nt = Symbol.for("react.forward_ref"), re = Symbol.for("react.suspense"), pe = Symbol.for("react.suspense_list"), ue = Symbol.for("react.memo"), Ye = Symbol.for("react.lazy"), bt = Symbol.for("react.offscreen"), ht = Symbol.iterator, pn = "@@iterator";
      function ot(h) {
        if (h === null || typeof h != "object")
          return null;
        var C = ht && h[ht] || h[pn];
        return typeof C == "function" ? C : null;
      }
      var qe = {
        /**
         * @internal
         * @type {ReactComponent}
         */
        current: null
      }, mt = {
        transition: null
      }, Oe = {
        current: null,
        // Used to reproduce behavior of `batchedUpdates` in legacy mode.
        isBatchingLegacy: !1,
        didScheduleLegacyUpdate: !1
      }, ft = {
        /**
         * @internal
         * @type {ReactComponent}
         */
        current: null
      }, Ve = {}, rn = null;
      function _n(h) {
        rn = h;
      }
      Ve.setExtraStackFrame = function(h) {
        rn = h;
      }, Ve.getCurrentStack = null, Ve.getStackAddendum = function() {
        var h = "";
        rn && (h += rn);
        var C = Ve.getCurrentStack;
        return C && (h += C() || ""), h;
      };
      var Wt = !1, Ot = !1, Cn = !1, ze = !1, Je = !1, Ft = {
        ReactCurrentDispatcher: qe,
        ReactCurrentBatchConfig: mt,
        ReactCurrentOwner: ft
      };
      Ft.ReactDebugCurrentFrame = Ve, Ft.ReactCurrentActQueue = Oe;
      function _t(h) {
        {
          for (var C = arguments.length, z = new Array(C > 1 ? C - 1 : 0), j = 1; j < C; j++)
            z[j - 1] = arguments[j];
          J("warn", h, z);
        }
      }
      function me(h) {
        {
          for (var C = arguments.length, z = new Array(C > 1 ? C - 1 : 0), j = 1; j < C; j++)
            z[j - 1] = arguments[j];
          J("error", h, z);
        }
      }
      function J(h, C, z) {
        {
          var j = Ft.ReactDebugCurrentFrame, K = j.getStackAddendum();
          K !== "" && (C += "%s", z = z.concat([K]));
          var je = z.map(function(ie) {
            return String(ie);
          });
          je.unshift("Warning: " + C), Function.prototype.apply.call(console[h], console, je);
        }
      }
      var be = {};
      function ae(h, C) {
        {
          var z = h.constructor, j = z && (z.displayName || z.name) || "ReactClass", K = j + "." + C;
          if (be[K])
            return;
          me("Can't call %s on a component that is not yet mounted. This is a no-op, but it might indicate a bug in your application. Instead, assign to `this.state` directly or define a `state = {};` class property with the desired state in the %s component.", C, j), be[K] = !0;
        }
      }
      var _ = {
        /**
         * Checks whether or not this composite component is mounted.
         * @param {ReactClass} publicInstance The instance we want to test.
         * @return {boolean} True if mounted, false otherwise.
         * @protected
         * @final
         */
        isMounted: function(h) {
          return !1;
        },
        /**
         * Forces an update. This should only be invoked when it is known with
         * certainty that we are **not** in a DOM transaction.
         *
         * You may want to call this when you know that some deeper aspect of the
         * component's state has changed but `setState` was not called.
         *
         * This will not invoke `shouldComponentUpdate`, but it will invoke
         * `componentWillUpdate` and `componentDidUpdate`.
         *
         * @param {ReactClass} publicInstance The instance that should rerender.
         * @param {?function} callback Called after component is updated.
         * @param {?string} callerName name of the calling function in the public API.
         * @internal
         */
        enqueueForceUpdate: function(h, C, z) {
          ae(h, "forceUpdate");
        },
        /**
         * Replaces all of the state. Always use this or `setState` to mutate state.
         * You should treat `this.state` as immutable.
         *
         * There is no guarantee that `this.state` will be immediately updated, so
         * accessing `this.state` after calling this method may return the old value.
         *
         * @param {ReactClass} publicInstance The instance that should rerender.
         * @param {object} completeState Next state.
         * @param {?function} callback Called after component is updated.
         * @param {?string} callerName name of the calling function in the public API.
         * @internal
         */
        enqueueReplaceState: function(h, C, z, j) {
          ae(h, "replaceState");
        },
        /**
         * Sets a subset of the state. This only exists because _pendingState is
         * internal. This provides a merging strategy that is not available to deep
         * properties which is confusing. TODO: Expose pendingState or don't use it
         * during the merge.
         *
         * @param {ReactClass} publicInstance The instance that should rerender.
         * @param {object} partialState Next partial state to be merged with state.
         * @param {?function} callback Called after component is updated.
         * @param {?string} Name of the calling function in the public API.
         * @internal
         */
        enqueueSetState: function(h, C, z, j) {
          ae(h, "setState");
        }
      }, V = Object.assign, Ue = {};
      Object.freeze(Ue);
      function Pe(h, C, z) {
        this.props = h, this.context = C, this.refs = Ue, this.updater = z || _;
      }
      Pe.prototype.isReactComponent = {}, Pe.prototype.setState = function(h, C) {
        if (typeof h != "object" && typeof h != "function" && h != null)
          throw new Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
        this.updater.enqueueSetState(this, h, C, "setState");
      }, Pe.prototype.forceUpdate = function(h) {
        this.updater.enqueueForceUpdate(this, h, "forceUpdate");
      };
      {
        var rt = {
          isMounted: ["isMounted", "Instead, make sure to clean up subscriptions and pending requests in componentWillUnmount to prevent memory leaks."],
          replaceState: ["replaceState", "Refactor your code to use setState instead (see https://github.com/facebook/react/issues/3236)."]
        }, tt = function(h, C) {
          Object.defineProperty(Pe.prototype, h, {
            get: function() {
              _t("%s(...) is deprecated in plain JavaScript React classes. %s", C[0], C[1]);
            }
          });
        };
        for (var St in rt)
          rt.hasOwnProperty(St) && tt(St, rt[St]);
      }
      function st() {
      }
      st.prototype = Pe.prototype;
      function ct(h, C, z) {
        this.props = h, this.context = C, this.refs = Ue, this.updater = z || _;
      }
      var en = ct.prototype = new st();
      en.constructor = ct, V(en, Pe.prototype), en.isPureReactComponent = !0;
      function hr() {
        var h = {
          current: null
        };
        return Object.seal(h), h;
      }
      var Br = Array.isArray;
      function vn(h) {
        return Br(h);
      }
      function Wn(h) {
        {
          var C = typeof Symbol == "function" && Symbol.toStringTag, z = C && h[Symbol.toStringTag] || h.constructor.name || "Object";
          return z;
        }
      }
      function Vn(h) {
        try {
          return zn(h), !1;
        } catch {
          return !0;
        }
      }
      function zn(h) {
        return "" + h;
      }
      function kn(h) {
        if (Vn(h))
          return me("The provided key is an unsupported type %s. This value must be coerced to a string before before using it here.", Wn(h)), zn(h);
      }
      function $r(h, C, z) {
        var j = h.displayName;
        if (j)
          return j;
        var K = C.displayName || C.name || "";
        return K !== "" ? z + "(" + K + ")" : z;
      }
      function Yr(h) {
        return h.displayName || "Context";
      }
      function Gn(h) {
        if (h == null)
          return null;
        if (typeof h.tag == "number" && me("Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue."), typeof h == "function")
          return h.displayName || h.name || null;
        if (typeof h == "string")
          return h;
        switch (h) {
          case $e:
            return "Fragment";
          case Dt:
            return "Portal";
          case ut:
            return "Profiler";
          case S:
            return "StrictMode";
          case re:
            return "Suspense";
          case pe:
            return "SuspenseList";
        }
        if (typeof h == "object")
          switch (h.$$typeof) {
            case se:
              var C = h;
              return Yr(C) + ".Consumer";
            case de:
              var z = h;
              return Yr(z._context) + ".Provider";
            case nt:
              return $r(h, h.render, "ForwardRef");
            case ue:
              var j = h.displayName || null;
              return j !== null ? j : Gn(h.type) || "Memo";
            case Ye: {
              var K = h, je = K._payload, ie = K._init;
              try {
                return Gn(ie(je));
              } catch {
                return null;
              }
            }
          }
        return null;
      }
      var mr = Object.prototype.hasOwnProperty, Ir = {
        key: !0,
        ref: !0,
        __self: !0,
        __source: !0
      }, yr, da, rr;
      rr = {};
      function Qr(h) {
        if (mr.call(h, "ref")) {
          var C = Object.getOwnPropertyDescriptor(h, "ref").get;
          if (C && C.isReactWarning)
            return !1;
        }
        return h.ref !== void 0;
      }
      function hn(h) {
        if (mr.call(h, "key")) {
          var C = Object.getOwnPropertyDescriptor(h, "key").get;
          if (C && C.isReactWarning)
            return !1;
        }
        return h.key !== void 0;
      }
      function wr(h, C) {
        var z = function() {
          yr || (yr = !0, me("%s: `key` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://reactjs.org/link/special-props)", C));
        };
        z.isReactWarning = !0, Object.defineProperty(h, "key", {
          get: z,
          configurable: !0
        });
      }
      function fi(h, C) {
        var z = function() {
          da || (da = !0, me("%s: `ref` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://reactjs.org/link/special-props)", C));
        };
        z.isReactWarning = !0, Object.defineProperty(h, "ref", {
          get: z,
          configurable: !0
        });
      }
      function pa(h) {
        if (typeof h.ref == "string" && ft.current && h.__self && ft.current.stateNode !== h.__self) {
          var C = Gn(ft.current.type);
          rr[C] || (me('Component "%s" contains the string ref "%s". Support for string refs will be removed in a future major release. This case cannot be automatically converted to an arrow function. We ask you to manually fix this case by using useRef() or createRef() instead. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-string-ref', C, h.ref), rr[C] = !0);
        }
      }
      var ee = function(h, C, z, j, K, je, ie) {
        var Ne = {
          // This tag allows us to uniquely identify this as a React Element
          $$typeof: Ze,
          // Built-in properties that belong on the element
          type: h,
          key: C,
          ref: z,
          props: ie,
          // Record the component responsible for creating this element.
          _owner: je
        };
        return Ne._store = {}, Object.defineProperty(Ne._store, "validated", {
          configurable: !1,
          enumerable: !1,
          writable: !0,
          value: !1
        }), Object.defineProperty(Ne, "_self", {
          configurable: !1,
          enumerable: !1,
          writable: !1,
          value: j
        }), Object.defineProperty(Ne, "_source", {
          configurable: !1,
          enumerable: !1,
          writable: !1,
          value: K
        }), Object.freeze && (Object.freeze(Ne.props), Object.freeze(Ne)), Ne;
      };
      function _e(h, C, z) {
        var j, K = {}, je = null, ie = null, Ne = null, pt = null;
        if (C != null) {
          Qr(C) && (ie = C.ref, pa(C)), hn(C) && (kn(C.key), je = "" + C.key), Ne = C.__self === void 0 ? null : C.__self, pt = C.__source === void 0 ? null : C.__source;
          for (j in C)
            mr.call(C, j) && !Ir.hasOwnProperty(j) && (K[j] = C[j]);
        }
        var kt = arguments.length - 2;
        if (kt === 1)
          K.children = z;
        else if (kt > 1) {
          for (var Kt = Array(kt), Qt = 0; Qt < kt; Qt++)
            Kt[Qt] = arguments[Qt + 2];
          Object.freeze && Object.freeze(Kt), K.children = Kt;
        }
        if (h && h.defaultProps) {
          var Zt = h.defaultProps;
          for (j in Zt)
            K[j] === void 0 && (K[j] = Zt[j]);
        }
        if (je || ie) {
          var tn = typeof h == "function" ? h.displayName || h.name || "Unknown" : h;
          je && wr(K, tn), ie && fi(K, tn);
        }
        return ee(h, je, ie, Ne, pt, ft.current, K);
      }
      function at(h, C) {
        var z = ee(h.type, C, h.ref, h._self, h._source, h._owner, h.props);
        return z;
      }
      function At(h, C, z) {
        if (h == null)
          throw new Error("React.cloneElement(...): The argument must be a React element, but you passed " + h + ".");
        var j, K = V({}, h.props), je = h.key, ie = h.ref, Ne = h._self, pt = h._source, kt = h._owner;
        if (C != null) {
          Qr(C) && (ie = C.ref, kt = ft.current), hn(C) && (kn(C.key), je = "" + C.key);
          var Kt;
          h.type && h.type.defaultProps && (Kt = h.type.defaultProps);
          for (j in C)
            mr.call(C, j) && !Ir.hasOwnProperty(j) && (C[j] === void 0 && Kt !== void 0 ? K[j] = Kt[j] : K[j] = C[j]);
        }
        var Qt = arguments.length - 2;
        if (Qt === 1)
          K.children = z;
        else if (Qt > 1) {
          for (var Zt = Array(Qt), tn = 0; tn < Qt; tn++)
            Zt[tn] = arguments[tn + 2];
          K.children = Zt;
        }
        return ee(h.type, je, ie, Ne, pt, kt, K);
      }
      function Ht(h) {
        return typeof h == "object" && h !== null && h.$$typeof === Ze;
      }
      var Dn = ".", mn = ":";
      function gr(h) {
        var C = /[=:]/g, z = {
          "=": "=0",
          ":": "=2"
        }, j = h.replace(C, function(K) {
          return z[K];
        });
        return "$" + j;
      }
      var It = !1, br = /\/+/g;
      function Vt(h) {
        return h.replace(br, "$&/");
      }
      function Pt(h, C) {
        return typeof h == "object" && h !== null && h.key != null ? (kn(h.key), gr("" + h.key)) : C.toString(36);
      }
      function Ja(h, C, z, j, K) {
        var je = typeof h;
        (je === "undefined" || je === "boolean") && (h = null);
        var ie = !1;
        if (h === null)
          ie = !0;
        else
          switch (je) {
            case "string":
            case "number":
              ie = !0;
              break;
            case "object":
              switch (h.$$typeof) {
                case Ze:
                case Dt:
                  ie = !0;
              }
          }
        if (ie) {
          var Ne = h, pt = K(Ne), kt = j === "" ? Dn + Pt(Ne, 0) : j;
          if (vn(pt)) {
            var Kt = "";
            kt != null && (Kt = Vt(kt) + "/"), Ja(pt, C, Kt, "", function(If) {
              return If;
            });
          } else
            pt != null && (Ht(pt) && (pt.key && (!Ne || Ne.key !== pt.key) && kn(pt.key), pt = at(
              pt,
              // Keep both the (mapped) and old keys if they differ, just as
              // traverseAllChildren used to do for objects as children
              z + // $FlowFixMe Flow incorrectly thinks React.Portal doesn't have a key
              (pt.key && (!Ne || Ne.key !== pt.key) ? (
                // $FlowFixMe Flow incorrectly thinks existing element's key can be a number
                // eslint-disable-next-line react-internal/safe-string-coercion
                Vt("" + pt.key) + "/"
              ) : "") + kt
            )), C.push(pt));
          return 1;
        }
        var Qt, Zt, tn = 0, Rt = j === "" ? Dn : j + mn;
        if (vn(h))
          for (var Ai = 0; Ai < h.length; Ai++)
            Qt = h[Ai], Zt = Rt + Pt(Qt, Ai), tn += Ja(Qt, C, z, Zt, K);
        else {
          var Yu = ot(h);
          if (typeof Yu == "function") {
            var Xo = h;
            Yu === Xo.entries && (It || _t("Using Maps as children is not supported. Use an array of keyed ReactElements instead."), It = !0);
            for (var Yf = Yu.call(Xo), ri, Ko = 0; !(ri = Yf.next()).done; )
              Qt = ri.value, Zt = Rt + Pt(Qt, Ko++), tn += Ja(Qt, C, z, Zt, K);
          } else if (je === "object") {
            var Zo = String(h);
            throw new Error("Objects are not valid as a React child (found: " + (Zo === "[object Object]" ? "object with keys {" + Object.keys(h).join(", ") + "}" : Zo) + "). If you meant to render a collection of children, use an array instead.");
          }
        }
        return tn;
      }
      function ka(h, C, z) {
        if (h == null)
          return h;
        var j = [], K = 0;
        return Ja(h, j, "", "", function(je) {
          return C.call(z, je, K++);
        }), j;
      }
      function ol(h) {
        var C = 0;
        return ka(h, function() {
          C++;
        }), C;
      }
      function Wl(h, C, z) {
        ka(h, function() {
          C.apply(this, arguments);
        }, z);
      }
      function Nu(h) {
        return ka(h, function(C) {
          return C;
        }) || [];
      }
      function Mi(h) {
        if (!Ht(h))
          throw new Error("React.Children.only expected to receive a single React element child.");
        return h;
      }
      function sl(h) {
        var C = {
          $$typeof: se,
          // As a workaround to support multiple concurrent renderers, we categorize
          // some renderers as primary and others as secondary. We only expect
          // there to be two concurrent renderers at most: React Native (primary) and
          // Fabric (secondary); React DOM (primary) and React ART (secondary).
          // Secondary renderers store their context values on separate fields.
          _currentValue: h,
          _currentValue2: h,
          // Used to track how many concurrent renderers this context currently
          // supports within in a single renderer. Such as parallel server rendering.
          _threadCount: 0,
          // These are circular
          Provider: null,
          Consumer: null,
          // Add these to use same hidden class in VM as ServerContext
          _defaultValue: null,
          _globalName: null
        };
        C.Provider = {
          $$typeof: de,
          _context: C
        };
        var z = !1, j = !1, K = !1;
        {
          var je = {
            $$typeof: se,
            _context: C
          };
          Object.defineProperties(je, {
            Provider: {
              get: function() {
                return j || (j = !0, me("Rendering <Context.Consumer.Provider> is not supported and will be removed in a future major release. Did you mean to render <Context.Provider> instead?")), C.Provider;
              },
              set: function(ie) {
                C.Provider = ie;
              }
            },
            _currentValue: {
              get: function() {
                return C._currentValue;
              },
              set: function(ie) {
                C._currentValue = ie;
              }
            },
            _currentValue2: {
              get: function() {
                return C._currentValue2;
              },
              set: function(ie) {
                C._currentValue2 = ie;
              }
            },
            _threadCount: {
              get: function() {
                return C._threadCount;
              },
              set: function(ie) {
                C._threadCount = ie;
              }
            },
            Consumer: {
              get: function() {
                return z || (z = !0, me("Rendering <Context.Consumer.Consumer> is not supported and will be removed in a future major release. Did you mean to render <Context.Consumer> instead?")), C.Consumer;
              }
            },
            displayName: {
              get: function() {
                return C.displayName;
              },
              set: function(ie) {
                K || (_t("Setting `displayName` on Context.Consumer has no effect. You should set it directly on the context with Context.displayName = '%s'.", ie), K = !0);
              }
            }
          }), C.Consumer = je;
        }
        return C._currentRenderer = null, C._currentRenderer2 = null, C;
      }
      var va = -1, di = 0, ha = 1, ei = 2;
      function _r(h) {
        if (h._status === va) {
          var C = h._result, z = C();
          if (z.then(function(je) {
            if (h._status === di || h._status === va) {
              var ie = h;
              ie._status = ha, ie._result = je;
            }
          }, function(je) {
            if (h._status === di || h._status === va) {
              var ie = h;
              ie._status = ei, ie._result = je;
            }
          }), h._status === va) {
            var j = h;
            j._status = di, j._result = z;
          }
        }
        if (h._status === ha) {
          var K = h._result;
          return K === void 0 && me(`lazy: Expected the result of a dynamic import() call. Instead received: %s

Your code should look like:
  const MyComponent = lazy(() => import('./MyComponent'))

Did you accidentally put curly braces around the import?`, K), "default" in K || me(`lazy: Expected the result of a dynamic import() call. Instead received: %s

Your code should look like:
  const MyComponent = lazy(() => import('./MyComponent'))`, K), K.default;
        } else
          throw h._result;
      }
      function ma(h) {
        var C = {
          // We use these fields to store the result.
          _status: va,
          _result: h
        }, z = {
          $$typeof: Ye,
          _payload: C,
          _init: _r
        };
        {
          var j, K;
          Object.defineProperties(z, {
            defaultProps: {
              configurable: !0,
              get: function() {
                return j;
              },
              set: function(je) {
                me("React.lazy(...): It is not supported to assign `defaultProps` to a lazy component import. Either specify them where the component is defined, or create a wrapping component around it."), j = je, Object.defineProperty(z, "defaultProps", {
                  enumerable: !0
                });
              }
            },
            propTypes: {
              configurable: !0,
              get: function() {
                return K;
              },
              set: function(je) {
                me("React.lazy(...): It is not supported to assign `propTypes` to a lazy component import. Either specify them where the component is defined, or create a wrapping component around it."), K = je, Object.defineProperty(z, "propTypes", {
                  enumerable: !0
                });
              }
            }
          });
        }
        return z;
      }
      function pi(h) {
        h != null && h.$$typeof === ue ? me("forwardRef requires a render function but received a `memo` component. Instead of forwardRef(memo(...)), use memo(forwardRef(...)).") : typeof h != "function" ? me("forwardRef requires a render function but was given %s.", h === null ? "null" : typeof h) : h.length !== 0 && h.length !== 2 && me("forwardRef render functions accept exactly two parameters: props and ref. %s", h.length === 1 ? "Did you forget to use the ref parameter?" : "Any additional parameter will be undefined."), h != null && (h.defaultProps != null || h.propTypes != null) && me("forwardRef render functions do not support propTypes or defaultProps. Did you accidentally pass a React component?");
        var C = {
          $$typeof: nt,
          render: h
        };
        {
          var z;
          Object.defineProperty(C, "displayName", {
            enumerable: !1,
            configurable: !0,
            get: function() {
              return z;
            },
            set: function(j) {
              z = j, !h.name && !h.displayName && (h.displayName = j);
            }
          });
        }
        return C;
      }
      var vi;
      vi = Symbol.for("react.module.reference");
      function R(h) {
        return !!(typeof h == "string" || typeof h == "function" || h === $e || h === ut || Je || h === S || h === re || h === pe || ze || h === bt || Wt || Ot || Cn || typeof h == "object" && h !== null && (h.$$typeof === Ye || h.$$typeof === ue || h.$$typeof === de || h.$$typeof === se || h.$$typeof === nt || // This needs to include all possible module reference object
        // types supported by any Flight configuration anywhere since
        // we don't know which Flight build this will end up being used
        // with.
        h.$$typeof === vi || h.getModuleId !== void 0));
      }
      function Y(h, C) {
        R(h) || me("memo: The first argument must be a component. Instead received: %s", h === null ? "null" : typeof h);
        var z = {
          $$typeof: ue,
          type: h,
          compare: C === void 0 ? null : C
        };
        {
          var j;
          Object.defineProperty(z, "displayName", {
            enumerable: !1,
            configurable: !0,
            get: function() {
              return j;
            },
            set: function(K) {
              j = K, !h.name && !h.displayName && (h.displayName = K);
            }
          });
        }
        return z;
      }
      function q() {
        var h = qe.current;
        return h === null && me(`Invalid hook call. Hooks can only be called inside of the body of a function component. This could happen for one of the following reasons:
1. You might have mismatching versions of React and the renderer (such as React DOM)
2. You might be breaking the Rules of Hooks
3. You might have more than one copy of React in the same app
See https://reactjs.org/link/invalid-hook-call for tips about how to debug and fix this problem.`), h;
      }
      function Te(h) {
        var C = q();
        if (h._context !== void 0) {
          var z = h._context;
          z.Consumer === h ? me("Calling useContext(Context.Consumer) is not supported, may cause bugs, and will be removed in a future major release. Did you mean to call useContext(Context) instead?") : z.Provider === h && me("Calling useContext(Context.Provider) is not supported. Did you mean to call useContext(Context) instead?");
        }
        return C.useContext(h);
      }
      function dt(h) {
        var C = q();
        return C.useState(h);
      }
      function Et(h, C, z) {
        var j = q();
        return j.useReducer(h, C, z);
      }
      function Ae(h) {
        var C = q();
        return C.useRef(h);
      }
      function it(h, C) {
        var z = q();
        return z.useEffect(h, C);
      }
      function Un(h, C) {
        var z = q();
        return z.useInsertionEffect(h, C);
      }
      function Xt(h, C) {
        var z = q();
        return z.useLayoutEffect(h, C);
      }
      function an(h, C) {
        var z = q();
        return z.useCallback(h, C);
      }
      function Sr(h, C) {
        var z = q();
        return z.useMemo(h, C);
      }
      function hi(h, C, z) {
        var j = q();
        return j.useImperativeHandle(h, C, z);
      }
      function Lt(h, C) {
        {
          var z = q();
          return z.useDebugValue(h, C);
        }
      }
      function qn() {
        var h = q();
        return h.useTransition();
      }
      function kr(h) {
        var C = q();
        return C.useDeferredValue(h);
      }
      function lt() {
        var h = q();
        return h.useId();
      }
      function Da(h, C, z) {
        var j = q();
        return j.useSyncExternalStore(h, C, z);
      }
      var cl = 0, zu, fl, Wr, Qo, Dr, Wo, Go;
      function Zs() {
      }
      Zs.__reactDisabledLog = !0;
      function Uu() {
        {
          if (cl === 0) {
            zu = console.log, fl = console.info, Wr = console.warn, Qo = console.error, Dr = console.group, Wo = console.groupCollapsed, Go = console.groupEnd;
            var h = {
              configurable: !0,
              enumerable: !0,
              value: Zs,
              writable: !0
            };
            Object.defineProperties(console, {
              info: h,
              log: h,
              warn: h,
              error: h,
              group: h,
              groupCollapsed: h,
              groupEnd: h
            });
          }
          cl++;
        }
      }
      function dl() {
        {
          if (cl--, cl === 0) {
            var h = {
              configurable: !0,
              enumerable: !0,
              writable: !0
            };
            Object.defineProperties(console, {
              log: V({}, h, {
                value: zu
              }),
              info: V({}, h, {
                value: fl
              }),
              warn: V({}, h, {
                value: Wr
              }),
              error: V({}, h, {
                value: Qo
              }),
              group: V({}, h, {
                value: Dr
              }),
              groupCollapsed: V({}, h, {
                value: Wo
              }),
              groupEnd: V({}, h, {
                value: Go
              })
            });
          }
          cl < 0 && me("disabledDepth fell below zero. This is a bug in React. Please file an issue.");
        }
      }
      var ti = Ft.ReactCurrentDispatcher, Or;
      function pl(h, C, z) {
        {
          if (Or === void 0)
            try {
              throw Error();
            } catch (K) {
              var j = K.stack.trim().match(/\n( *(at )?)/);
              Or = j && j[1] || "";
            }
          return `
` + Or + h;
        }
      }
      var vl = !1, hl;
      {
        var Au = typeof WeakMap == "function" ? WeakMap : Map;
        hl = new Au();
      }
      function ju(h, C) {
        if (!h || vl)
          return "";
        {
          var z = hl.get(h);
          if (z !== void 0)
            return z;
        }
        var j;
        vl = !0;
        var K = Error.prepareStackTrace;
        Error.prepareStackTrace = void 0;
        var je;
        je = ti.current, ti.current = null, Uu();
        try {
          if (C) {
            var ie = function() {
              throw Error();
            };
            if (Object.defineProperty(ie.prototype, "props", {
              set: function() {
                throw Error();
              }
            }), typeof Reflect == "object" && Reflect.construct) {
              try {
                Reflect.construct(ie, []);
              } catch (Rt) {
                j = Rt;
              }
              Reflect.construct(h, [], ie);
            } else {
              try {
                ie.call();
              } catch (Rt) {
                j = Rt;
              }
              h.call(ie.prototype);
            }
          } else {
            try {
              throw Error();
            } catch (Rt) {
              j = Rt;
            }
            h();
          }
        } catch (Rt) {
          if (Rt && j && typeof Rt.stack == "string") {
            for (var Ne = Rt.stack.split(`
`), pt = j.stack.split(`
`), kt = Ne.length - 1, Kt = pt.length - 1; kt >= 1 && Kt >= 0 && Ne[kt] !== pt[Kt]; )
              Kt--;
            for (; kt >= 1 && Kt >= 0; kt--, Kt--)
              if (Ne[kt] !== pt[Kt]) {
                if (kt !== 1 || Kt !== 1)
                  do
                    if (kt--, Kt--, Kt < 0 || Ne[kt] !== pt[Kt]) {
                      var Qt = `
` + Ne[kt].replace(" at new ", " at ");
                      return h.displayName && Qt.includes("<anonymous>") && (Qt = Qt.replace("<anonymous>", h.displayName)), typeof h == "function" && hl.set(h, Qt), Qt;
                    }
                  while (kt >= 1 && Kt >= 0);
                break;
              }
          }
        } finally {
          vl = !1, ti.current = je, dl(), Error.prepareStackTrace = K;
        }
        var Zt = h ? h.displayName || h.name : "", tn = Zt ? pl(Zt) : "";
        return typeof h == "function" && hl.set(h, tn), tn;
      }
      function Ni(h, C, z) {
        return ju(h, !1);
      }
      function $f(h) {
        var C = h.prototype;
        return !!(C && C.isReactComponent);
      }
      function mi(h, C, z) {
        if (h == null)
          return "";
        if (typeof h == "function")
          return ju(h, $f(h));
        if (typeof h == "string")
          return pl(h);
        switch (h) {
          case re:
            return pl("Suspense");
          case pe:
            return pl("SuspenseList");
        }
        if (typeof h == "object")
          switch (h.$$typeof) {
            case nt:
              return Ni(h.render);
            case ue:
              return mi(h.type, C, z);
            case Ye: {
              var j = h, K = j._payload, je = j._init;
              try {
                return mi(je(K), C, z);
              } catch {
              }
            }
          }
        return "";
      }
      var Mt = {}, Fu = Ft.ReactDebugCurrentFrame;
      function Gl(h) {
        if (h) {
          var C = h._owner, z = mi(h.type, h._source, C ? C.type : null);
          Fu.setExtraStackFrame(z);
        } else
          Fu.setExtraStackFrame(null);
      }
      function Hu(h, C, z, j, K) {
        {
          var je = Function.call.bind(mr);
          for (var ie in h)
            if (je(h, ie)) {
              var Ne = void 0;
              try {
                if (typeof h[ie] != "function") {
                  var pt = Error((j || "React class") + ": " + z + " type `" + ie + "` is invalid; it must be a function, usually from the `prop-types` package, but received `" + typeof h[ie] + "`.This often happens because of typos such as `PropTypes.function` instead of `PropTypes.func`.");
                  throw pt.name = "Invariant Violation", pt;
                }
                Ne = h[ie](C, ie, j, z, null, "SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED");
              } catch (kt) {
                Ne = kt;
              }
              Ne && !(Ne instanceof Error) && (Gl(K), me("%s: type specification of %s `%s` is invalid; the type checker function must return `null` or an `Error` but returned a %s. You may have forgotten to pass an argument to the type checker creator (arrayOf, instanceOf, objectOf, oneOf, oneOfType, and shape all require an argument).", j || "React class", z, ie, typeof Ne), Gl(null)), Ne instanceof Error && !(Ne.message in Mt) && (Mt[Ne.message] = !0, Gl(K), me("Failed %s type: %s", z, Ne.message), Gl(null));
            }
        }
      }
      function Ct(h) {
        if (h) {
          var C = h._owner, z = mi(h.type, h._source, C ? C.type : null);
          _n(z);
        } else
          _n(null);
      }
      var Vu;
      Vu = !1;
      function Pu() {
        if (ft.current) {
          var h = Gn(ft.current.type);
          if (h)
            return `

Check the render method of \`` + h + "`.";
        }
        return "";
      }
      function We(h) {
        if (h !== void 0) {
          var C = h.fileName.replace(/^.*[\\\/]/, ""), z = h.lineNumber;
          return `

Check your code at ` + C + ":" + z + ".";
        }
        return "";
      }
      function ql(h) {
        return h != null ? We(h.__source) : "";
      }
      var yn = {};
      function Gr(h) {
        var C = Pu();
        if (!C) {
          var z = typeof h == "string" ? h : h.displayName || h.name;
          z && (C = `

Check the top-level render call using <` + z + ">.");
        }
        return C;
      }
      function Lr(h, C) {
        if (!(!h._store || h._store.validated || h.key != null)) {
          h._store.validated = !0;
          var z = Gr(C);
          if (!yn[z]) {
            yn[z] = !0;
            var j = "";
            h && h._owner && h._owner !== ft.current && (j = " It was passed a child from " + Gn(h._owner.type) + "."), Ct(h), me('Each child in a list should have a unique "key" prop.%s%s See https://reactjs.org/link/warning-keys for more information.', z, j), Ct(null);
          }
        }
      }
      function ml(h, C) {
        if (typeof h == "object") {
          if (vn(h))
            for (var z = 0; z < h.length; z++) {
              var j = h[z];
              Ht(j) && Lr(j, C);
            }
          else if (Ht(h))
            h._store && (h._store.validated = !0);
          else if (h) {
            var K = ot(h);
            if (typeof K == "function" && K !== h.entries)
              for (var je = K.call(h), ie; !(ie = je.next()).done; )
                Ht(ie.value) && Lr(ie.value, C);
          }
        }
      }
      function Rn(h) {
        {
          var C = h.type;
          if (C == null || typeof C == "string")
            return;
          var z;
          if (typeof C == "function")
            z = C.propTypes;
          else if (typeof C == "object" && (C.$$typeof === nt || // Note: Memo only checks outer props here.
          // Inner props are checked in the reconciler.
          C.$$typeof === ue))
            z = C.propTypes;
          else
            return;
          if (z) {
            var j = Gn(C);
            Hu(z, h.props, "prop", j, h);
          } else if (C.PropTypes !== void 0 && !Vu) {
            Vu = !0;
            var K = Gn(C);
            me("Component %s declared `PropTypes` instead of `propTypes`. Did you misspell the property assignment?", K || "Unknown");
          }
          typeof C.getDefaultProps == "function" && !C.getDefaultProps.isReactClassApproved && me("getDefaultProps is only used on classic React.createClass definitions. Use a static property named `defaultProps` instead.");
        }
      }
      function Bt(h) {
        {
          for (var C = Object.keys(h.props), z = 0; z < C.length; z++) {
            var j = C[z];
            if (j !== "children" && j !== "key") {
              Ct(h), me("Invalid prop `%s` supplied to `React.Fragment`. React.Fragment can only have `key` and `children` props.", j), Ct(null);
              break;
            }
          }
          h.ref !== null && (Ct(h), me("Invalid attribute `ref` supplied to `React.Fragment`."), Ct(null));
        }
      }
      function Js(h, C, z) {
        var j = R(h);
        if (!j) {
          var K = "";
          (h === void 0 || typeof h == "object" && h !== null && Object.keys(h).length === 0) && (K += " You likely forgot to export your component from the file it's defined in, or you might have mixed up default and named imports.");
          var je = ql(C);
          je ? K += je : K += Pu();
          var ie;
          h === null ? ie = "null" : vn(h) ? ie = "array" : h !== void 0 && h.$$typeof === Ze ? (ie = "<" + (Gn(h.type) || "Unknown") + " />", K = " Did you accidentally export a JSX literal instead of a component?") : ie = typeof h, me("React.createElement: type is invalid -- expected a string (for built-in components) or a class/function (for composite components) but got: %s.%s", ie, K);
        }
        var Ne = _e.apply(this, arguments);
        if (Ne == null)
          return Ne;
        if (j)
          for (var pt = 2; pt < arguments.length; pt++)
            ml(arguments[pt], h);
        return h === $e ? Bt(Ne) : Rn(Ne), Ne;
      }
      var qr = !1;
      function Xn(h) {
        var C = Js.bind(null, h);
        return C.type = h, qr || (qr = !0, _t("React.createFactory() is deprecated and will be removed in a future major release. Consider using JSX or use React.createElement() directly instead.")), Object.defineProperty(C, "type", {
          enumerable: !1,
          get: function() {
            return _t("Factory.type is deprecated. Access the class directly before passing it to createFactory."), Object.defineProperty(this, "type", {
              value: h
            }), h;
          }
        }), C;
      }
      function yi(h, C, z) {
        for (var j = At.apply(this, arguments), K = 2; K < arguments.length; K++)
          ml(arguments[K], j.type);
        return Rn(j), j;
      }
      function ec(h, C) {
        var z = mt.transition;
        mt.transition = {};
        var j = mt.transition;
        mt.transition._updatedFibers = /* @__PURE__ */ new Set();
        try {
          h();
        } finally {
          if (mt.transition = z, z === null && j._updatedFibers) {
            var K = j._updatedFibers.size;
            K > 10 && _t("Detected a large number of updates inside startTransition. If this is due to a subscription please re-write it to use React provided hooks. Otherwise concurrent mode guarantees are off the table."), j._updatedFibers.clear();
          }
        }
      }
      var zi = !1, yl = null;
      function tc(h) {
        if (yl === null)
          try {
            var C = ("require" + Math.random()).slice(0, 7), z = Q && Q[C];
            yl = z.call(Q, "timers").setImmediate;
          } catch {
            yl = function(K) {
              zi === !1 && (zi = !0, typeof MessageChannel > "u" && me("This browser does not have a MessageChannel implementation, so enqueuing tasks via await act(async () => ...) will fail. Please file an issue at https://github.com/facebook/react/issues if you encounter this warning."));
              var je = new MessageChannel();
              je.port1.onmessage = K, je.port2.postMessage(void 0);
            };
          }
        return yl(h);
      }
      var Oa = 0, gl = !1;
      function Ui(h) {
        {
          var C = Oa;
          Oa++, Oe.current === null && (Oe.current = []);
          var z = Oe.isBatchingLegacy, j;
          try {
            if (Oe.isBatchingLegacy = !0, j = h(), !z && Oe.didScheduleLegacyUpdate) {
              var K = Oe.current;
              K !== null && (Oe.didScheduleLegacyUpdate = !1, El(K));
            }
          } catch (Zt) {
            throw La(C), Zt;
          } finally {
            Oe.isBatchingLegacy = z;
          }
          if (j !== null && typeof j == "object" && typeof j.then == "function") {
            var je = j, ie = !1, Ne = {
              then: function(Zt, tn) {
                ie = !0, je.then(function(Rt) {
                  La(C), Oa === 0 ? Bu(Rt, Zt, tn) : Zt(Rt);
                }, function(Rt) {
                  La(C), tn(Rt);
                });
              }
            };
            return !gl && typeof Promise < "u" && Promise.resolve().then(function() {
            }).then(function() {
              ie || (gl = !0, me("You called act(async () => ...) without await. This could lead to unexpected testing behaviour, interleaving multiple act calls and mixing their scopes. You should - await act(async () => ...);"));
            }), Ne;
          } else {
            var pt = j;
            if (La(C), Oa === 0) {
              var kt = Oe.current;
              kt !== null && (El(kt), Oe.current = null);
              var Kt = {
                then: function(Zt, tn) {
                  Oe.current === null ? (Oe.current = [], Bu(pt, Zt, tn)) : Zt(pt);
                }
              };
              return Kt;
            } else {
              var Qt = {
                then: function(Zt, tn) {
                  Zt(pt);
                }
              };
              return Qt;
            }
          }
        }
      }
      function La(h) {
        h !== Oa - 1 && me("You seem to have overlapping act() calls, this is not supported. Be sure to await previous act() calls before making a new one. "), Oa = h;
      }
      function Bu(h, C, z) {
        {
          var j = Oe.current;
          if (j !== null)
            try {
              El(j), tc(function() {
                j.length === 0 ? (Oe.current = null, C(h)) : Bu(h, C, z);
              });
            } catch (K) {
              z(K);
            }
          else
            C(h);
        }
      }
      var Sl = !1;
      function El(h) {
        if (!Sl) {
          Sl = !0;
          var C = 0;
          try {
            for (; C < h.length; C++) {
              var z = h[C];
              do
                z = z(!0);
              while (z !== null);
            }
            h.length = 0;
          } catch (j) {
            throw h = h.slice(C + 1), j;
          } finally {
            Sl = !1;
          }
        }
      }
      var Xl = Js, $u = yi, qo = Xn, ni = {
        map: ka,
        forEach: Wl,
        count: ol,
        toArray: Nu,
        only: Mi
      };
      B.Children = ni, B.Component = Pe, B.Fragment = $e, B.Profiler = ut, B.PureComponent = ct, B.StrictMode = S, B.Suspense = re, B.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = Ft, B.act = Ui, B.cloneElement = $u, B.createContext = sl, B.createElement = Xl, B.createFactory = qo, B.createRef = hr, B.forwardRef = pi, B.isValidElement = Ht, B.lazy = ma, B.memo = Y, B.startTransition = ec, B.unstable_act = Ui, B.useCallback = an, B.useContext = Te, B.useDebugValue = Lt, B.useDeferredValue = kr, B.useEffect = it, B.useId = lt, B.useImperativeHandle = hi, B.useInsertionEffect = Un, B.useLayoutEffect = Xt, B.useMemo = Sr, B.useReducer = Et, B.useRef = Ae, B.useState = dt, B.useSyncExternalStore = Da, B.useTransition = qn, B.version = k, typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop(new Error());
    }();
  }(Xp, Xp.exports)), Xp.exports;
}
process.env.NODE_ENV === "production" ? m0.exports = tk() : m0.exports = nk();
var Ql = m0.exports;
const rk = /* @__PURE__ */ ek(Ql);
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var tR;
function ak() {
  if (tR)
    return Qp;
  tR = 1;
  var Q = Ql, B = Symbol.for("react.element"), k = Symbol.for("react.fragment"), Ze = Object.prototype.hasOwnProperty, Dt = Q.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, $e = { key: !0, ref: !0, __self: !0, __source: !0 };
  function S(ut, de, se) {
    var nt, re = {}, pe = null, ue = null;
    se !== void 0 && (pe = "" + se), de.key !== void 0 && (pe = "" + de.key), de.ref !== void 0 && (ue = de.ref);
    for (nt in de)
      Ze.call(de, nt) && !$e.hasOwnProperty(nt) && (re[nt] = de[nt]);
    if (ut && ut.defaultProps)
      for (nt in de = ut.defaultProps, de)
        re[nt] === void 0 && (re[nt] = de[nt]);
    return { $$typeof: B, type: ut, key: pe, ref: ue, props: re, _owner: Dt.current };
  }
  return Qp.Fragment = k, Qp.jsx = S, Qp.jsxs = S, Qp;
}
var Wp = {};
/**
 * @license React
 * react-jsx-runtime.development.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var nR;
function ik() {
  return nR || (nR = 1, process.env.NODE_ENV !== "production" && function() {
    var Q = Ql, B = Symbol.for("react.element"), k = Symbol.for("react.portal"), Ze = Symbol.for("react.fragment"), Dt = Symbol.for("react.strict_mode"), $e = Symbol.for("react.profiler"), S = Symbol.for("react.provider"), ut = Symbol.for("react.context"), de = Symbol.for("react.forward_ref"), se = Symbol.for("react.suspense"), nt = Symbol.for("react.suspense_list"), re = Symbol.for("react.memo"), pe = Symbol.for("react.lazy"), ue = Symbol.for("react.offscreen"), Ye = Symbol.iterator, bt = "@@iterator";
    function ht(R) {
      if (R === null || typeof R != "object")
        return null;
      var Y = Ye && R[Ye] || R[bt];
      return typeof Y == "function" ? Y : null;
    }
    var pn = Q.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;
    function ot(R) {
      {
        for (var Y = arguments.length, q = new Array(Y > 1 ? Y - 1 : 0), Te = 1; Te < Y; Te++)
          q[Te - 1] = arguments[Te];
        qe("error", R, q);
      }
    }
    function qe(R, Y, q) {
      {
        var Te = pn.ReactDebugCurrentFrame, dt = Te.getStackAddendum();
        dt !== "" && (Y += "%s", q = q.concat([dt]));
        var Et = q.map(function(Ae) {
          return String(Ae);
        });
        Et.unshift("Warning: " + Y), Function.prototype.apply.call(console[R], console, Et);
      }
    }
    var mt = !1, Oe = !1, ft = !1, Ve = !1, rn = !1, _n;
    _n = Symbol.for("react.module.reference");
    function Wt(R) {
      return !!(typeof R == "string" || typeof R == "function" || R === Ze || R === $e || rn || R === Dt || R === se || R === nt || Ve || R === ue || mt || Oe || ft || typeof R == "object" && R !== null && (R.$$typeof === pe || R.$$typeof === re || R.$$typeof === S || R.$$typeof === ut || R.$$typeof === de || // This needs to include all possible module reference object
      // types supported by any Flight configuration anywhere since
      // we don't know which Flight build this will end up being used
      // with.
      R.$$typeof === _n || R.getModuleId !== void 0));
    }
    function Ot(R, Y, q) {
      var Te = R.displayName;
      if (Te)
        return Te;
      var dt = Y.displayName || Y.name || "";
      return dt !== "" ? q + "(" + dt + ")" : q;
    }
    function Cn(R) {
      return R.displayName || "Context";
    }
    function ze(R) {
      if (R == null)
        return null;
      if (typeof R.tag == "number" && ot("Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue."), typeof R == "function")
        return R.displayName || R.name || null;
      if (typeof R == "string")
        return R;
      switch (R) {
        case Ze:
          return "Fragment";
        case k:
          return "Portal";
        case $e:
          return "Profiler";
        case Dt:
          return "StrictMode";
        case se:
          return "Suspense";
        case nt:
          return "SuspenseList";
      }
      if (typeof R == "object")
        switch (R.$$typeof) {
          case ut:
            var Y = R;
            return Cn(Y) + ".Consumer";
          case S:
            var q = R;
            return Cn(q._context) + ".Provider";
          case de:
            return Ot(R, R.render, "ForwardRef");
          case re:
            var Te = R.displayName || null;
            return Te !== null ? Te : ze(R.type) || "Memo";
          case pe: {
            var dt = R, Et = dt._payload, Ae = dt._init;
            try {
              return ze(Ae(Et));
            } catch {
              return null;
            }
          }
        }
      return null;
    }
    var Je = Object.assign, Ft = 0, _t, me, J, be, ae, _, V;
    function Ue() {
    }
    Ue.__reactDisabledLog = !0;
    function Pe() {
      {
        if (Ft === 0) {
          _t = console.log, me = console.info, J = console.warn, be = console.error, ae = console.group, _ = console.groupCollapsed, V = console.groupEnd;
          var R = {
            configurable: !0,
            enumerable: !0,
            value: Ue,
            writable: !0
          };
          Object.defineProperties(console, {
            info: R,
            log: R,
            warn: R,
            error: R,
            group: R,
            groupCollapsed: R,
            groupEnd: R
          });
        }
        Ft++;
      }
    }
    function rt() {
      {
        if (Ft--, Ft === 0) {
          var R = {
            configurable: !0,
            enumerable: !0,
            writable: !0
          };
          Object.defineProperties(console, {
            log: Je({}, R, {
              value: _t
            }),
            info: Je({}, R, {
              value: me
            }),
            warn: Je({}, R, {
              value: J
            }),
            error: Je({}, R, {
              value: be
            }),
            group: Je({}, R, {
              value: ae
            }),
            groupCollapsed: Je({}, R, {
              value: _
            }),
            groupEnd: Je({}, R, {
              value: V
            })
          });
        }
        Ft < 0 && ot("disabledDepth fell below zero. This is a bug in React. Please file an issue.");
      }
    }
    var tt = pn.ReactCurrentDispatcher, St;
    function st(R, Y, q) {
      {
        if (St === void 0)
          try {
            throw Error();
          } catch (dt) {
            var Te = dt.stack.trim().match(/\n( *(at )?)/);
            St = Te && Te[1] || "";
          }
        return `
` + St + R;
      }
    }
    var ct = !1, en;
    {
      var hr = typeof WeakMap == "function" ? WeakMap : Map;
      en = new hr();
    }
    function Br(R, Y) {
      if (!R || ct)
        return "";
      {
        var q = en.get(R);
        if (q !== void 0)
          return q;
      }
      var Te;
      ct = !0;
      var dt = Error.prepareStackTrace;
      Error.prepareStackTrace = void 0;
      var Et;
      Et = tt.current, tt.current = null, Pe();
      try {
        if (Y) {
          var Ae = function() {
            throw Error();
          };
          if (Object.defineProperty(Ae.prototype, "props", {
            set: function() {
              throw Error();
            }
          }), typeof Reflect == "object" && Reflect.construct) {
            try {
              Reflect.construct(Ae, []);
            } catch (qn) {
              Te = qn;
            }
            Reflect.construct(R, [], Ae);
          } else {
            try {
              Ae.call();
            } catch (qn) {
              Te = qn;
            }
            R.call(Ae.prototype);
          }
        } else {
          try {
            throw Error();
          } catch (qn) {
            Te = qn;
          }
          R();
        }
      } catch (qn) {
        if (qn && Te && typeof qn.stack == "string") {
          for (var it = qn.stack.split(`
`), Un = Te.stack.split(`
`), Xt = it.length - 1, an = Un.length - 1; Xt >= 1 && an >= 0 && it[Xt] !== Un[an]; )
            an--;
          for (; Xt >= 1 && an >= 0; Xt--, an--)
            if (it[Xt] !== Un[an]) {
              if (Xt !== 1 || an !== 1)
                do
                  if (Xt--, an--, an < 0 || it[Xt] !== Un[an]) {
                    var Sr = `
` + it[Xt].replace(" at new ", " at ");
                    return R.displayName && Sr.includes("<anonymous>") && (Sr = Sr.replace("<anonymous>", R.displayName)), typeof R == "function" && en.set(R, Sr), Sr;
                  }
                while (Xt >= 1 && an >= 0);
              break;
            }
        }
      } finally {
        ct = !1, tt.current = Et, rt(), Error.prepareStackTrace = dt;
      }
      var hi = R ? R.displayName || R.name : "", Lt = hi ? st(hi) : "";
      return typeof R == "function" && en.set(R, Lt), Lt;
    }
    function vn(R, Y, q) {
      return Br(R, !1);
    }
    function Wn(R) {
      var Y = R.prototype;
      return !!(Y && Y.isReactComponent);
    }
    function Vn(R, Y, q) {
      if (R == null)
        return "";
      if (typeof R == "function")
        return Br(R, Wn(R));
      if (typeof R == "string")
        return st(R);
      switch (R) {
        case se:
          return st("Suspense");
        case nt:
          return st("SuspenseList");
      }
      if (typeof R == "object")
        switch (R.$$typeof) {
          case de:
            return vn(R.render);
          case re:
            return Vn(R.type, Y, q);
          case pe: {
            var Te = R, dt = Te._payload, Et = Te._init;
            try {
              return Vn(Et(dt), Y, q);
            } catch {
            }
          }
        }
      return "";
    }
    var zn = Object.prototype.hasOwnProperty, kn = {}, $r = pn.ReactDebugCurrentFrame;
    function Yr(R) {
      if (R) {
        var Y = R._owner, q = Vn(R.type, R._source, Y ? Y.type : null);
        $r.setExtraStackFrame(q);
      } else
        $r.setExtraStackFrame(null);
    }
    function Gn(R, Y, q, Te, dt) {
      {
        var Et = Function.call.bind(zn);
        for (var Ae in R)
          if (Et(R, Ae)) {
            var it = void 0;
            try {
              if (typeof R[Ae] != "function") {
                var Un = Error((Te || "React class") + ": " + q + " type `" + Ae + "` is invalid; it must be a function, usually from the `prop-types` package, but received `" + typeof R[Ae] + "`.This often happens because of typos such as `PropTypes.function` instead of `PropTypes.func`.");
                throw Un.name = "Invariant Violation", Un;
              }
              it = R[Ae](Y, Ae, Te, q, null, "SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED");
            } catch (Xt) {
              it = Xt;
            }
            it && !(it instanceof Error) && (Yr(dt), ot("%s: type specification of %s `%s` is invalid; the type checker function must return `null` or an `Error` but returned a %s. You may have forgotten to pass an argument to the type checker creator (arrayOf, instanceOf, objectOf, oneOf, oneOfType, and shape all require an argument).", Te || "React class", q, Ae, typeof it), Yr(null)), it instanceof Error && !(it.message in kn) && (kn[it.message] = !0, Yr(dt), ot("Failed %s type: %s", q, it.message), Yr(null));
          }
      }
    }
    var mr = Array.isArray;
    function Ir(R) {
      return mr(R);
    }
    function yr(R) {
      {
        var Y = typeof Symbol == "function" && Symbol.toStringTag, q = Y && R[Symbol.toStringTag] || R.constructor.name || "Object";
        return q;
      }
    }
    function da(R) {
      try {
        return rr(R), !1;
      } catch {
        return !0;
      }
    }
    function rr(R) {
      return "" + R;
    }
    function Qr(R) {
      if (da(R))
        return ot("The provided key is an unsupported type %s. This value must be coerced to a string before before using it here.", yr(R)), rr(R);
    }
    var hn = pn.ReactCurrentOwner, wr = {
      key: !0,
      ref: !0,
      __self: !0,
      __source: !0
    }, fi, pa, ee;
    ee = {};
    function _e(R) {
      if (zn.call(R, "ref")) {
        var Y = Object.getOwnPropertyDescriptor(R, "ref").get;
        if (Y && Y.isReactWarning)
          return !1;
      }
      return R.ref !== void 0;
    }
    function at(R) {
      if (zn.call(R, "key")) {
        var Y = Object.getOwnPropertyDescriptor(R, "key").get;
        if (Y && Y.isReactWarning)
          return !1;
      }
      return R.key !== void 0;
    }
    function At(R, Y) {
      if (typeof R.ref == "string" && hn.current && Y && hn.current.stateNode !== Y) {
        var q = ze(hn.current.type);
        ee[q] || (ot('Component "%s" contains the string ref "%s". Support for string refs will be removed in a future major release. This case cannot be automatically converted to an arrow function. We ask you to manually fix this case by using useRef() or createRef() instead. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-string-ref', ze(hn.current.type), R.ref), ee[q] = !0);
      }
    }
    function Ht(R, Y) {
      {
        var q = function() {
          fi || (fi = !0, ot("%s: `key` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://reactjs.org/link/special-props)", Y));
        };
        q.isReactWarning = !0, Object.defineProperty(R, "key", {
          get: q,
          configurable: !0
        });
      }
    }
    function Dn(R, Y) {
      {
        var q = function() {
          pa || (pa = !0, ot("%s: `ref` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://reactjs.org/link/special-props)", Y));
        };
        q.isReactWarning = !0, Object.defineProperty(R, "ref", {
          get: q,
          configurable: !0
        });
      }
    }
    var mn = function(R, Y, q, Te, dt, Et, Ae) {
      var it = {
        // This tag allows us to uniquely identify this as a React Element
        $$typeof: B,
        // Built-in properties that belong on the element
        type: R,
        key: Y,
        ref: q,
        props: Ae,
        // Record the component responsible for creating this element.
        _owner: Et
      };
      return it._store = {}, Object.defineProperty(it._store, "validated", {
        configurable: !1,
        enumerable: !1,
        writable: !0,
        value: !1
      }), Object.defineProperty(it, "_self", {
        configurable: !1,
        enumerable: !1,
        writable: !1,
        value: Te
      }), Object.defineProperty(it, "_source", {
        configurable: !1,
        enumerable: !1,
        writable: !1,
        value: dt
      }), Object.freeze && (Object.freeze(it.props), Object.freeze(it)), it;
    };
    function gr(R, Y, q, Te, dt) {
      {
        var Et, Ae = {}, it = null, Un = null;
        q !== void 0 && (Qr(q), it = "" + q), at(Y) && (Qr(Y.key), it = "" + Y.key), _e(Y) && (Un = Y.ref, At(Y, dt));
        for (Et in Y)
          zn.call(Y, Et) && !wr.hasOwnProperty(Et) && (Ae[Et] = Y[Et]);
        if (R && R.defaultProps) {
          var Xt = R.defaultProps;
          for (Et in Xt)
            Ae[Et] === void 0 && (Ae[Et] = Xt[Et]);
        }
        if (it || Un) {
          var an = typeof R == "function" ? R.displayName || R.name || "Unknown" : R;
          it && Ht(Ae, an), Un && Dn(Ae, an);
        }
        return mn(R, it, Un, dt, Te, hn.current, Ae);
      }
    }
    var It = pn.ReactCurrentOwner, br = pn.ReactDebugCurrentFrame;
    function Vt(R) {
      if (R) {
        var Y = R._owner, q = Vn(R.type, R._source, Y ? Y.type : null);
        br.setExtraStackFrame(q);
      } else
        br.setExtraStackFrame(null);
    }
    var Pt;
    Pt = !1;
    function Ja(R) {
      return typeof R == "object" && R !== null && R.$$typeof === B;
    }
    function ka() {
      {
        if (It.current) {
          var R = ze(It.current.type);
          if (R)
            return `

Check the render method of \`` + R + "`.";
        }
        return "";
      }
    }
    function ol(R) {
      {
        if (R !== void 0) {
          var Y = R.fileName.replace(/^.*[\\\/]/, ""), q = R.lineNumber;
          return `

Check your code at ` + Y + ":" + q + ".";
        }
        return "";
      }
    }
    var Wl = {};
    function Nu(R) {
      {
        var Y = ka();
        if (!Y) {
          var q = typeof R == "string" ? R : R.displayName || R.name;
          q && (Y = `

Check the top-level render call using <` + q + ">.");
        }
        return Y;
      }
    }
    function Mi(R, Y) {
      {
        if (!R._store || R._store.validated || R.key != null)
          return;
        R._store.validated = !0;
        var q = Nu(Y);
        if (Wl[q])
          return;
        Wl[q] = !0;
        var Te = "";
        R && R._owner && R._owner !== It.current && (Te = " It was passed a child from " + ze(R._owner.type) + "."), Vt(R), ot('Each child in a list should have a unique "key" prop.%s%s See https://reactjs.org/link/warning-keys for more information.', q, Te), Vt(null);
      }
    }
    function sl(R, Y) {
      {
        if (typeof R != "object")
          return;
        if (Ir(R))
          for (var q = 0; q < R.length; q++) {
            var Te = R[q];
            Ja(Te) && Mi(Te, Y);
          }
        else if (Ja(R))
          R._store && (R._store.validated = !0);
        else if (R) {
          var dt = ht(R);
          if (typeof dt == "function" && dt !== R.entries)
            for (var Et = dt.call(R), Ae; !(Ae = Et.next()).done; )
              Ja(Ae.value) && Mi(Ae.value, Y);
        }
      }
    }
    function va(R) {
      {
        var Y = R.type;
        if (Y == null || typeof Y == "string")
          return;
        var q;
        if (typeof Y == "function")
          q = Y.propTypes;
        else if (typeof Y == "object" && (Y.$$typeof === de || // Note: Memo only checks outer props here.
        // Inner props are checked in the reconciler.
        Y.$$typeof === re))
          q = Y.propTypes;
        else
          return;
        if (q) {
          var Te = ze(Y);
          Gn(q, R.props, "prop", Te, R);
        } else if (Y.PropTypes !== void 0 && !Pt) {
          Pt = !0;
          var dt = ze(Y);
          ot("Component %s declared `PropTypes` instead of `propTypes`. Did you misspell the property assignment?", dt || "Unknown");
        }
        typeof Y.getDefaultProps == "function" && !Y.getDefaultProps.isReactClassApproved && ot("getDefaultProps is only used on classic React.createClass definitions. Use a static property named `defaultProps` instead.");
      }
    }
    function di(R) {
      {
        for (var Y = Object.keys(R.props), q = 0; q < Y.length; q++) {
          var Te = Y[q];
          if (Te !== "children" && Te !== "key") {
            Vt(R), ot("Invalid prop `%s` supplied to `React.Fragment`. React.Fragment can only have `key` and `children` props.", Te), Vt(null);
            break;
          }
        }
        R.ref !== null && (Vt(R), ot("Invalid attribute `ref` supplied to `React.Fragment`."), Vt(null));
      }
    }
    var ha = {};
    function ei(R, Y, q, Te, dt, Et) {
      {
        var Ae = Wt(R);
        if (!Ae) {
          var it = "";
          (R === void 0 || typeof R == "object" && R !== null && Object.keys(R).length === 0) && (it += " You likely forgot to export your component from the file it's defined in, or you might have mixed up default and named imports.");
          var Un = ol(dt);
          Un ? it += Un : it += ka();
          var Xt;
          R === null ? Xt = "null" : Ir(R) ? Xt = "array" : R !== void 0 && R.$$typeof === B ? (Xt = "<" + (ze(R.type) || "Unknown") + " />", it = " Did you accidentally export a JSX literal instead of a component?") : Xt = typeof R, ot("React.jsx: type is invalid -- expected a string (for built-in components) or a class/function (for composite components) but got: %s.%s", Xt, it);
        }
        var an = gr(R, Y, q, dt, Et);
        if (an == null)
          return an;
        if (Ae) {
          var Sr = Y.children;
          if (Sr !== void 0)
            if (Te)
              if (Ir(Sr)) {
                for (var hi = 0; hi < Sr.length; hi++)
                  sl(Sr[hi], R);
                Object.freeze && Object.freeze(Sr);
              } else
                ot("React.jsx: Static children should always be an array. You are likely explicitly calling React.jsxs or React.jsxDEV. Use the Babel transform instead.");
            else
              sl(Sr, R);
        }
        if (zn.call(Y, "key")) {
          var Lt = ze(R), qn = Object.keys(Y).filter(function(Da) {
            return Da !== "key";
          }), kr = qn.length > 0 ? "{key: someKey, " + qn.join(": ..., ") + ": ...}" : "{key: someKey}";
          if (!ha[Lt + kr]) {
            var lt = qn.length > 0 ? "{" + qn.join(": ..., ") + ": ...}" : "{}";
            ot(`A props object containing a "key" prop is being spread into JSX:
  let props = %s;
  <%s {...props} />
React keys must be passed directly to JSX without using spread:
  let props = %s;
  <%s key={someKey} {...props} />`, kr, Lt, lt, Lt), ha[Lt + kr] = !0;
          }
        }
        return R === Ze ? di(an) : va(an), an;
      }
    }
    function _r(R, Y, q) {
      return ei(R, Y, q, !0);
    }
    function ma(R, Y, q) {
      return ei(R, Y, q, !1);
    }
    var pi = ma, vi = _r;
    Wp.Fragment = Ze, Wp.jsx = pi, Wp.jsxs = vi;
  }()), Wp;
}
process.env.NODE_ENV === "production" ? h0.exports = ak() : h0.exports = ik();
var De = h0.exports, Kp = {}, y0 = { exports: {} }, Ka = {}, Bm = { exports: {} }, p0 = {};
/**
 * @license React
 * scheduler.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var rR;
function lk() {
  return rR || (rR = 1, function(Q) {
    function B(J, be) {
      var ae = J.length;
      J.push(be);
      e:
        for (; 0 < ae; ) {
          var _ = ae - 1 >>> 1, V = J[_];
          if (0 < Dt(V, be))
            J[_] = be, J[ae] = V, ae = _;
          else
            break e;
        }
    }
    function k(J) {
      return J.length === 0 ? null : J[0];
    }
    function Ze(J) {
      if (J.length === 0)
        return null;
      var be = J[0], ae = J.pop();
      if (ae !== be) {
        J[0] = ae;
        e:
          for (var _ = 0, V = J.length, Ue = V >>> 1; _ < Ue; ) {
            var Pe = 2 * (_ + 1) - 1, rt = J[Pe], tt = Pe + 1, St = J[tt];
            if (0 > Dt(rt, ae))
              tt < V && 0 > Dt(St, rt) ? (J[_] = St, J[tt] = ae, _ = tt) : (J[_] = rt, J[Pe] = ae, _ = Pe);
            else if (tt < V && 0 > Dt(St, ae))
              J[_] = St, J[tt] = ae, _ = tt;
            else
              break e;
          }
      }
      return be;
    }
    function Dt(J, be) {
      var ae = J.sortIndex - be.sortIndex;
      return ae !== 0 ? ae : J.id - be.id;
    }
    if (typeof performance == "object" && typeof performance.now == "function") {
      var $e = performance;
      Q.unstable_now = function() {
        return $e.now();
      };
    } else {
      var S = Date, ut = S.now();
      Q.unstable_now = function() {
        return S.now() - ut;
      };
    }
    var de = [], se = [], nt = 1, re = null, pe = 3, ue = !1, Ye = !1, bt = !1, ht = typeof setTimeout == "function" ? setTimeout : null, pn = typeof clearTimeout == "function" ? clearTimeout : null, ot = typeof setImmediate < "u" ? setImmediate : null;
    typeof navigator < "u" && navigator.scheduling !== void 0 && navigator.scheduling.isInputPending !== void 0 && navigator.scheduling.isInputPending.bind(navigator.scheduling);
    function qe(J) {
      for (var be = k(se); be !== null; ) {
        if (be.callback === null)
          Ze(se);
        else if (be.startTime <= J)
          Ze(se), be.sortIndex = be.expirationTime, B(de, be);
        else
          break;
        be = k(se);
      }
    }
    function mt(J) {
      if (bt = !1, qe(J), !Ye)
        if (k(de) !== null)
          Ye = !0, _t(Oe);
        else {
          var be = k(se);
          be !== null && me(mt, be.startTime - J);
        }
    }
    function Oe(J, be) {
      Ye = !1, bt && (bt = !1, pn(rn), rn = -1), ue = !0;
      var ae = pe;
      try {
        for (qe(be), re = k(de); re !== null && (!(re.expirationTime > be) || J && !Ot()); ) {
          var _ = re.callback;
          if (typeof _ == "function") {
            re.callback = null, pe = re.priorityLevel;
            var V = _(re.expirationTime <= be);
            be = Q.unstable_now(), typeof V == "function" ? re.callback = V : re === k(de) && Ze(de), qe(be);
          } else
            Ze(de);
          re = k(de);
        }
        if (re !== null)
          var Ue = !0;
        else {
          var Pe = k(se);
          Pe !== null && me(mt, Pe.startTime - be), Ue = !1;
        }
        return Ue;
      } finally {
        re = null, pe = ae, ue = !1;
      }
    }
    var ft = !1, Ve = null, rn = -1, _n = 5, Wt = -1;
    function Ot() {
      return !(Q.unstable_now() - Wt < _n);
    }
    function Cn() {
      if (Ve !== null) {
        var J = Q.unstable_now();
        Wt = J;
        var be = !0;
        try {
          be = Ve(!0, J);
        } finally {
          be ? ze() : (ft = !1, Ve = null);
        }
      } else
        ft = !1;
    }
    var ze;
    if (typeof ot == "function")
      ze = function() {
        ot(Cn);
      };
    else if (typeof MessageChannel < "u") {
      var Je = new MessageChannel(), Ft = Je.port2;
      Je.port1.onmessage = Cn, ze = function() {
        Ft.postMessage(null);
      };
    } else
      ze = function() {
        ht(Cn, 0);
      };
    function _t(J) {
      Ve = J, ft || (ft = !0, ze());
    }
    function me(J, be) {
      rn = ht(function() {
        J(Q.unstable_now());
      }, be);
    }
    Q.unstable_IdlePriority = 5, Q.unstable_ImmediatePriority = 1, Q.unstable_LowPriority = 4, Q.unstable_NormalPriority = 3, Q.unstable_Profiling = null, Q.unstable_UserBlockingPriority = 2, Q.unstable_cancelCallback = function(J) {
      J.callback = null;
    }, Q.unstable_continueExecution = function() {
      Ye || ue || (Ye = !0, _t(Oe));
    }, Q.unstable_forceFrameRate = function(J) {
      0 > J || 125 < J ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : _n = 0 < J ? Math.floor(1e3 / J) : 5;
    }, Q.unstable_getCurrentPriorityLevel = function() {
      return pe;
    }, Q.unstable_getFirstCallbackNode = function() {
      return k(de);
    }, Q.unstable_next = function(J) {
      switch (pe) {
        case 1:
        case 2:
        case 3:
          var be = 3;
          break;
        default:
          be = pe;
      }
      var ae = pe;
      pe = be;
      try {
        return J();
      } finally {
        pe = ae;
      }
    }, Q.unstable_pauseExecution = function() {
    }, Q.unstable_requestPaint = function() {
    }, Q.unstable_runWithPriority = function(J, be) {
      switch (J) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
          break;
        default:
          J = 3;
      }
      var ae = pe;
      pe = J;
      try {
        return be();
      } finally {
        pe = ae;
      }
    }, Q.unstable_scheduleCallback = function(J, be, ae) {
      var _ = Q.unstable_now();
      switch (typeof ae == "object" && ae !== null ? (ae = ae.delay, ae = typeof ae == "number" && 0 < ae ? _ + ae : _) : ae = _, J) {
        case 1:
          var V = -1;
          break;
        case 2:
          V = 250;
          break;
        case 5:
          V = 1073741823;
          break;
        case 4:
          V = 1e4;
          break;
        default:
          V = 5e3;
      }
      return V = ae + V, J = { id: nt++, callback: be, priorityLevel: J, startTime: ae, expirationTime: V, sortIndex: -1 }, ae > _ ? (J.sortIndex = ae, B(se, J), k(de) === null && J === k(se) && (bt ? (pn(rn), rn = -1) : bt = !0, me(mt, ae - _))) : (J.sortIndex = V, B(de, J), Ye || ue || (Ye = !0, _t(Oe))), J;
    }, Q.unstable_shouldYield = Ot, Q.unstable_wrapCallback = function(J) {
      var be = pe;
      return function() {
        var ae = pe;
        pe = be;
        try {
          return J.apply(this, arguments);
        } finally {
          pe = ae;
        }
      };
    };
  }(p0)), p0;
}
var v0 = {};
/**
 * @license React
 * scheduler.development.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var aR;
function uk() {
  return aR || (aR = 1, function(Q) {
    process.env.NODE_ENV !== "production" && function() {
      typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart(new Error());
      var B = !1, k = !1, Ze = 5;
      function Dt(ee, _e) {
        var at = ee.length;
        ee.push(_e), ut(ee, _e, at);
      }
      function $e(ee) {
        return ee.length === 0 ? null : ee[0];
      }
      function S(ee) {
        if (ee.length === 0)
          return null;
        var _e = ee[0], at = ee.pop();
        return at !== _e && (ee[0] = at, de(ee, at, 0)), _e;
      }
      function ut(ee, _e, at) {
        for (var At = at; At > 0; ) {
          var Ht = At - 1 >>> 1, Dn = ee[Ht];
          if (se(Dn, _e) > 0)
            ee[Ht] = _e, ee[At] = Dn, At = Ht;
          else
            return;
        }
      }
      function de(ee, _e, at) {
        for (var At = at, Ht = ee.length, Dn = Ht >>> 1; At < Dn; ) {
          var mn = (At + 1) * 2 - 1, gr = ee[mn], It = mn + 1, br = ee[It];
          if (se(gr, _e) < 0)
            It < Ht && se(br, gr) < 0 ? (ee[At] = br, ee[It] = _e, At = It) : (ee[At] = gr, ee[mn] = _e, At = mn);
          else if (It < Ht && se(br, _e) < 0)
            ee[At] = br, ee[It] = _e, At = It;
          else
            return;
        }
      }
      function se(ee, _e) {
        var at = ee.sortIndex - _e.sortIndex;
        return at !== 0 ? at : ee.id - _e.id;
      }
      var nt = 1, re = 2, pe = 3, ue = 4, Ye = 5;
      function bt(ee, _e) {
      }
      var ht = typeof performance == "object" && typeof performance.now == "function";
      if (ht) {
        var pn = performance;
        Q.unstable_now = function() {
          return pn.now();
        };
      } else {
        var ot = Date, qe = ot.now();
        Q.unstable_now = function() {
          return ot.now() - qe;
        };
      }
      var mt = 1073741823, Oe = -1, ft = 250, Ve = 5e3, rn = 1e4, _n = mt, Wt = [], Ot = [], Cn = 1, ze = null, Je = pe, Ft = !1, _t = !1, me = !1, J = typeof setTimeout == "function" ? setTimeout : null, be = typeof clearTimeout == "function" ? clearTimeout : null, ae = typeof setImmediate < "u" ? setImmediate : null;
      typeof navigator < "u" && navigator.scheduling !== void 0 && navigator.scheduling.isInputPending !== void 0 && navigator.scheduling.isInputPending.bind(navigator.scheduling);
      function _(ee) {
        for (var _e = $e(Ot); _e !== null; ) {
          if (_e.callback === null)
            S(Ot);
          else if (_e.startTime <= ee)
            S(Ot), _e.sortIndex = _e.expirationTime, Dt(Wt, _e);
          else
            return;
          _e = $e(Ot);
        }
      }
      function V(ee) {
        if (me = !1, _(ee), !_t)
          if ($e(Wt) !== null)
            _t = !0, Qr(Ue);
          else {
            var _e = $e(Ot);
            _e !== null && hn(V, _e.startTime - ee);
          }
      }
      function Ue(ee, _e) {
        _t = !1, me && (me = !1, wr()), Ft = !0;
        var at = Je;
        try {
          var At;
          if (!k)
            return Pe(ee, _e);
        } finally {
          ze = null, Je = at, Ft = !1;
        }
      }
      function Pe(ee, _e) {
        var at = _e;
        for (_(at), ze = $e(Wt); ze !== null && !B && !(ze.expirationTime > at && (!ee || Yr())); ) {
          var At = ze.callback;
          if (typeof At == "function") {
            ze.callback = null, Je = ze.priorityLevel;
            var Ht = ze.expirationTime <= at, Dn = At(Ht);
            at = Q.unstable_now(), typeof Dn == "function" ? ze.callback = Dn : ze === $e(Wt) && S(Wt), _(at);
          } else
            S(Wt);
          ze = $e(Wt);
        }
        if (ze !== null)
          return !0;
        var mn = $e(Ot);
        return mn !== null && hn(V, mn.startTime - at), !1;
      }
      function rt(ee, _e) {
        switch (ee) {
          case nt:
          case re:
          case pe:
          case ue:
          case Ye:
            break;
          default:
            ee = pe;
        }
        var at = Je;
        Je = ee;
        try {
          return _e();
        } finally {
          Je = at;
        }
      }
      function tt(ee) {
        var _e;
        switch (Je) {
          case nt:
          case re:
          case pe:
            _e = pe;
            break;
          default:
            _e = Je;
            break;
        }
        var at = Je;
        Je = _e;
        try {
          return ee();
        } finally {
          Je = at;
        }
      }
      function St(ee) {
        var _e = Je;
        return function() {
          var at = Je;
          Je = _e;
          try {
            return ee.apply(this, arguments);
          } finally {
            Je = at;
          }
        };
      }
      function st(ee, _e, at) {
        var At = Q.unstable_now(), Ht;
        if (typeof at == "object" && at !== null) {
          var Dn = at.delay;
          typeof Dn == "number" && Dn > 0 ? Ht = At + Dn : Ht = At;
        } else
          Ht = At;
        var mn;
        switch (ee) {
          case nt:
            mn = Oe;
            break;
          case re:
            mn = ft;
            break;
          case Ye:
            mn = _n;
            break;
          case ue:
            mn = rn;
            break;
          case pe:
          default:
            mn = Ve;
            break;
        }
        var gr = Ht + mn, It = {
          id: Cn++,
          callback: _e,
          priorityLevel: ee,
          startTime: Ht,
          expirationTime: gr,
          sortIndex: -1
        };
        return Ht > At ? (It.sortIndex = Ht, Dt(Ot, It), $e(Wt) === null && It === $e(Ot) && (me ? wr() : me = !0, hn(V, Ht - At))) : (It.sortIndex = gr, Dt(Wt, It), !_t && !Ft && (_t = !0, Qr(Ue))), It;
      }
      function ct() {
      }
      function en() {
        !_t && !Ft && (_t = !0, Qr(Ue));
      }
      function hr() {
        return $e(Wt);
      }
      function Br(ee) {
        ee.callback = null;
      }
      function vn() {
        return Je;
      }
      var Wn = !1, Vn = null, zn = -1, kn = Ze, $r = -1;
      function Yr() {
        var ee = Q.unstable_now() - $r;
        return !(ee < kn);
      }
      function Gn() {
      }
      function mr(ee) {
        if (ee < 0 || ee > 125) {
          console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported");
          return;
        }
        ee > 0 ? kn = Math.floor(1e3 / ee) : kn = Ze;
      }
      var Ir = function() {
        if (Vn !== null) {
          var ee = Q.unstable_now();
          $r = ee;
          var _e = !0, at = !0;
          try {
            at = Vn(_e, ee);
          } finally {
            at ? yr() : (Wn = !1, Vn = null);
          }
        } else
          Wn = !1;
      }, yr;
      if (typeof ae == "function")
        yr = function() {
          ae(Ir);
        };
      else if (typeof MessageChannel < "u") {
        var da = new MessageChannel(), rr = da.port2;
        da.port1.onmessage = Ir, yr = function() {
          rr.postMessage(null);
        };
      } else
        yr = function() {
          J(Ir, 0);
        };
      function Qr(ee) {
        Vn = ee, Wn || (Wn = !0, yr());
      }
      function hn(ee, _e) {
        zn = J(function() {
          ee(Q.unstable_now());
        }, _e);
      }
      function wr() {
        be(zn), zn = -1;
      }
      var fi = Gn, pa = null;
      Q.unstable_IdlePriority = Ye, Q.unstable_ImmediatePriority = nt, Q.unstable_LowPriority = ue, Q.unstable_NormalPriority = pe, Q.unstable_Profiling = pa, Q.unstable_UserBlockingPriority = re, Q.unstable_cancelCallback = Br, Q.unstable_continueExecution = en, Q.unstable_forceFrameRate = mr, Q.unstable_getCurrentPriorityLevel = vn, Q.unstable_getFirstCallbackNode = hr, Q.unstable_next = tt, Q.unstable_pauseExecution = ct, Q.unstable_requestPaint = fi, Q.unstable_runWithPriority = rt, Q.unstable_scheduleCallback = st, Q.unstable_shouldYield = Yr, Q.unstable_wrapCallback = St, typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop(new Error());
    }();
  }(v0)), v0;
}
var iR;
function oR() {
  return iR || (iR = 1, process.env.NODE_ENV === "production" ? Bm.exports = lk() : Bm.exports = uk()), Bm.exports;
}
/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var lR;
function ok() {
  if (lR)
    return Ka;
  lR = 1;
  var Q = Ql, B = oR();
  function k(n) {
    for (var r = "https://reactjs.org/docs/error-decoder.html?invariant=" + n, l = 1; l < arguments.length; l++)
      r += "&args[]=" + encodeURIComponent(arguments[l]);
    return "Minified React error #" + n + "; visit " + r + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
  }
  var Ze = /* @__PURE__ */ new Set(), Dt = {};
  function $e(n, r) {
    S(n, r), S(n + "Capture", r);
  }
  function S(n, r) {
    for (Dt[n] = r, n = 0; n < r.length; n++)
      Ze.add(r[n]);
  }
  var ut = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), de = Object.prototype.hasOwnProperty, se = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, nt = {}, re = {};
  function pe(n) {
    return de.call(re, n) ? !0 : de.call(nt, n) ? !1 : se.test(n) ? re[n] = !0 : (nt[n] = !0, !1);
  }
  function ue(n, r, l, o) {
    if (l !== null && l.type === 0)
      return !1;
    switch (typeof r) {
      case "function":
      case "symbol":
        return !0;
      case "boolean":
        return o ? !1 : l !== null ? !l.acceptsBooleans : (n = n.toLowerCase().slice(0, 5), n !== "data-" && n !== "aria-");
      default:
        return !1;
    }
  }
  function Ye(n, r, l, o) {
    if (r === null || typeof r > "u" || ue(n, r, l, o))
      return !0;
    if (o)
      return !1;
    if (l !== null)
      switch (l.type) {
        case 3:
          return !r;
        case 4:
          return r === !1;
        case 5:
          return isNaN(r);
        case 6:
          return isNaN(r) || 1 > r;
      }
    return !1;
  }
  function bt(n, r, l, o, c, d, m) {
    this.acceptsBooleans = r === 2 || r === 3 || r === 4, this.attributeName = o, this.attributeNamespace = c, this.mustUseProperty = l, this.propertyName = n, this.type = r, this.sanitizeURL = d, this.removeEmptyString = m;
  }
  var ht = {};
  "children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(n) {
    ht[n] = new bt(n, 0, !1, n, null, !1, !1);
  }), [["acceptCharset", "accept-charset"], ["className", "class"], ["htmlFor", "for"], ["httpEquiv", "http-equiv"]].forEach(function(n) {
    var r = n[0];
    ht[r] = new bt(r, 1, !1, n[1], null, !1, !1);
  }), ["contentEditable", "draggable", "spellCheck", "value"].forEach(function(n) {
    ht[n] = new bt(n, 2, !1, n.toLowerCase(), null, !1, !1);
  }), ["autoReverse", "externalResourcesRequired", "focusable", "preserveAlpha"].forEach(function(n) {
    ht[n] = new bt(n, 2, !1, n, null, !1, !1);
  }), "allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(n) {
    ht[n] = new bt(n, 3, !1, n.toLowerCase(), null, !1, !1);
  }), ["checked", "multiple", "muted", "selected"].forEach(function(n) {
    ht[n] = new bt(n, 3, !0, n, null, !1, !1);
  }), ["capture", "download"].forEach(function(n) {
    ht[n] = new bt(n, 4, !1, n, null, !1, !1);
  }), ["cols", "rows", "size", "span"].forEach(function(n) {
    ht[n] = new bt(n, 6, !1, n, null, !1, !1);
  }), ["rowSpan", "start"].forEach(function(n) {
    ht[n] = new bt(n, 5, !1, n.toLowerCase(), null, !1, !1);
  });
  var pn = /[\-:]([a-z])/g;
  function ot(n) {
    return n[1].toUpperCase();
  }
  "accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(n) {
    var r = n.replace(
      pn,
      ot
    );
    ht[r] = new bt(r, 1, !1, n, null, !1, !1);
  }), "xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(n) {
    var r = n.replace(pn, ot);
    ht[r] = new bt(r, 1, !1, n, "http://www.w3.org/1999/xlink", !1, !1);
  }), ["xml:base", "xml:lang", "xml:space"].forEach(function(n) {
    var r = n.replace(pn, ot);
    ht[r] = new bt(r, 1, !1, n, "http://www.w3.org/XML/1998/namespace", !1, !1);
  }), ["tabIndex", "crossOrigin"].forEach(function(n) {
    ht[n] = new bt(n, 1, !1, n.toLowerCase(), null, !1, !1);
  }), ht.xlinkHref = new bt("xlinkHref", 1, !1, "xlink:href", "http://www.w3.org/1999/xlink", !0, !1), ["src", "href", "action", "formAction"].forEach(function(n) {
    ht[n] = new bt(n, 1, !1, n.toLowerCase(), null, !0, !0);
  });
  function qe(n, r, l, o) {
    var c = ht.hasOwnProperty(r) ? ht[r] : null;
    (c !== null ? c.type !== 0 : o || !(2 < r.length) || r[0] !== "o" && r[0] !== "O" || r[1] !== "n" && r[1] !== "N") && (Ye(r, l, c, o) && (l = null), o || c === null ? pe(r) && (l === null ? n.removeAttribute(r) : n.setAttribute(r, "" + l)) : c.mustUseProperty ? n[c.propertyName] = l === null ? c.type === 3 ? !1 : "" : l : (r = c.attributeName, o = c.attributeNamespace, l === null ? n.removeAttribute(r) : (c = c.type, l = c === 3 || c === 4 && l === !0 ? "" : "" + l, o ? n.setAttributeNS(o, r, l) : n.setAttribute(r, l))));
  }
  var mt = Q.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, Oe = Symbol.for("react.element"), ft = Symbol.for("react.portal"), Ve = Symbol.for("react.fragment"), rn = Symbol.for("react.strict_mode"), _n = Symbol.for("react.profiler"), Wt = Symbol.for("react.provider"), Ot = Symbol.for("react.context"), Cn = Symbol.for("react.forward_ref"), ze = Symbol.for("react.suspense"), Je = Symbol.for("react.suspense_list"), Ft = Symbol.for("react.memo"), _t = Symbol.for("react.lazy"), me = Symbol.for("react.offscreen"), J = Symbol.iterator;
  function be(n) {
    return n === null || typeof n != "object" ? null : (n = J && n[J] || n["@@iterator"], typeof n == "function" ? n : null);
  }
  var ae = Object.assign, _;
  function V(n) {
    if (_ === void 0)
      try {
        throw Error();
      } catch (l) {
        var r = l.stack.trim().match(/\n( *(at )?)/);
        _ = r && r[1] || "";
      }
    return `
` + _ + n;
  }
  var Ue = !1;
  function Pe(n, r) {
    if (!n || Ue)
      return "";
    Ue = !0;
    var l = Error.prepareStackTrace;
    Error.prepareStackTrace = void 0;
    try {
      if (r)
        if (r = function() {
          throw Error();
        }, Object.defineProperty(r.prototype, "props", { set: function() {
          throw Error();
        } }), typeof Reflect == "object" && Reflect.construct) {
          try {
            Reflect.construct(r, []);
          } catch (U) {
            var o = U;
          }
          Reflect.construct(n, [], r);
        } else {
          try {
            r.call();
          } catch (U) {
            o = U;
          }
          n.call(r.prototype);
        }
      else {
        try {
          throw Error();
        } catch (U) {
          o = U;
        }
        n();
      }
    } catch (U) {
      if (U && o && typeof U.stack == "string") {
        for (var c = U.stack.split(`
`), d = o.stack.split(`
`), m = c.length - 1, E = d.length - 1; 1 <= m && 0 <= E && c[m] !== d[E]; )
          E--;
        for (; 1 <= m && 0 <= E; m--, E--)
          if (c[m] !== d[E]) {
            if (m !== 1 || E !== 1)
              do
                if (m--, E--, 0 > E || c[m] !== d[E]) {
                  var T = `
` + c[m].replace(" at new ", " at ");
                  return n.displayName && T.includes("<anonymous>") && (T = T.replace("<anonymous>", n.displayName)), T;
                }
              while (1 <= m && 0 <= E);
            break;
          }
      }
    } finally {
      Ue = !1, Error.prepareStackTrace = l;
    }
    return (n = n ? n.displayName || n.name : "") ? V(n) : "";
  }
  function rt(n) {
    switch (n.tag) {
      case 5:
        return V(n.type);
      case 16:
        return V("Lazy");
      case 13:
        return V("Suspense");
      case 19:
        return V("SuspenseList");
      case 0:
      case 2:
      case 15:
        return n = Pe(n.type, !1), n;
      case 11:
        return n = Pe(n.type.render, !1), n;
      case 1:
        return n = Pe(n.type, !0), n;
      default:
        return "";
    }
  }
  function tt(n) {
    if (n == null)
      return null;
    if (typeof n == "function")
      return n.displayName || n.name || null;
    if (typeof n == "string")
      return n;
    switch (n) {
      case Ve:
        return "Fragment";
      case ft:
        return "Portal";
      case _n:
        return "Profiler";
      case rn:
        return "StrictMode";
      case ze:
        return "Suspense";
      case Je:
        return "SuspenseList";
    }
    if (typeof n == "object")
      switch (n.$$typeof) {
        case Ot:
          return (n.displayName || "Context") + ".Consumer";
        case Wt:
          return (n._context.displayName || "Context") + ".Provider";
        case Cn:
          var r = n.render;
          return n = n.displayName, n || (n = r.displayName || r.name || "", n = n !== "" ? "ForwardRef(" + n + ")" : "ForwardRef"), n;
        case Ft:
          return r = n.displayName || null, r !== null ? r : tt(n.type) || "Memo";
        case _t:
          r = n._payload, n = n._init;
          try {
            return tt(n(r));
          } catch {
          }
      }
    return null;
  }
  function St(n) {
    var r = n.type;
    switch (n.tag) {
      case 24:
        return "Cache";
      case 9:
        return (r.displayName || "Context") + ".Consumer";
      case 10:
        return (r._context.displayName || "Context") + ".Provider";
      case 18:
        return "DehydratedFragment";
      case 11:
        return n = r.render, n = n.displayName || n.name || "", r.displayName || (n !== "" ? "ForwardRef(" + n + ")" : "ForwardRef");
      case 7:
        return "Fragment";
      case 5:
        return r;
      case 4:
        return "Portal";
      case 3:
        return "Root";
      case 6:
        return "Text";
      case 16:
        return tt(r);
      case 8:
        return r === rn ? "StrictMode" : "Mode";
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
        if (typeof r == "function")
          return r.displayName || r.name || null;
        if (typeof r == "string")
          return r;
    }
    return null;
  }
  function st(n) {
    switch (typeof n) {
      case "boolean":
      case "number":
      case "string":
      case "undefined":
        return n;
      case "object":
        return n;
      default:
        return "";
    }
  }
  function ct(n) {
    var r = n.type;
    return (n = n.nodeName) && n.toLowerCase() === "input" && (r === "checkbox" || r === "radio");
  }
  function en(n) {
    var r = ct(n) ? "checked" : "value", l = Object.getOwnPropertyDescriptor(n.constructor.prototype, r), o = "" + n[r];
    if (!n.hasOwnProperty(r) && typeof l < "u" && typeof l.get == "function" && typeof l.set == "function") {
      var c = l.get, d = l.set;
      return Object.defineProperty(n, r, { configurable: !0, get: function() {
        return c.call(this);
      }, set: function(m) {
        o = "" + m, d.call(this, m);
      } }), Object.defineProperty(n, r, { enumerable: l.enumerable }), { getValue: function() {
        return o;
      }, setValue: function(m) {
        o = "" + m;
      }, stopTracking: function() {
        n._valueTracker = null, delete n[r];
      } };
    }
  }
  function hr(n) {
    n._valueTracker || (n._valueTracker = en(n));
  }
  function Br(n) {
    if (!n)
      return !1;
    var r = n._valueTracker;
    if (!r)
      return !0;
    var l = r.getValue(), o = "";
    return n && (o = ct(n) ? n.checked ? "true" : "false" : n.value), n = o, n !== l ? (r.setValue(n), !0) : !1;
  }
  function vn(n) {
    if (n = n || (typeof document < "u" ? document : void 0), typeof n > "u")
      return null;
    try {
      return n.activeElement || n.body;
    } catch {
      return n.body;
    }
  }
  function Wn(n, r) {
    var l = r.checked;
    return ae({}, r, { defaultChecked: void 0, defaultValue: void 0, value: void 0, checked: l ?? n._wrapperState.initialChecked });
  }
  function Vn(n, r) {
    var l = r.defaultValue == null ? "" : r.defaultValue, o = r.checked != null ? r.checked : r.defaultChecked;
    l = st(r.value != null ? r.value : l), n._wrapperState = { initialChecked: o, initialValue: l, controlled: r.type === "checkbox" || r.type === "radio" ? r.checked != null : r.value != null };
  }
  function zn(n, r) {
    r = r.checked, r != null && qe(n, "checked", r, !1);
  }
  function kn(n, r) {
    zn(n, r);
    var l = st(r.value), o = r.type;
    if (l != null)
      o === "number" ? (l === 0 && n.value === "" || n.value != l) && (n.value = "" + l) : n.value !== "" + l && (n.value = "" + l);
    else if (o === "submit" || o === "reset") {
      n.removeAttribute("value");
      return;
    }
    r.hasOwnProperty("value") ? Yr(n, r.type, l) : r.hasOwnProperty("defaultValue") && Yr(n, r.type, st(r.defaultValue)), r.checked == null && r.defaultChecked != null && (n.defaultChecked = !!r.defaultChecked);
  }
  function $r(n, r, l) {
    if (r.hasOwnProperty("value") || r.hasOwnProperty("defaultValue")) {
      var o = r.type;
      if (!(o !== "submit" && o !== "reset" || r.value !== void 0 && r.value !== null))
        return;
      r = "" + n._wrapperState.initialValue, l || r === n.value || (n.value = r), n.defaultValue = r;
    }
    l = n.name, l !== "" && (n.name = ""), n.defaultChecked = !!n._wrapperState.initialChecked, l !== "" && (n.name = l);
  }
  function Yr(n, r, l) {
    (r !== "number" || vn(n.ownerDocument) !== n) && (l == null ? n.defaultValue = "" + n._wrapperState.initialValue : n.defaultValue !== "" + l && (n.defaultValue = "" + l));
  }
  var Gn = Array.isArray;
  function mr(n, r, l, o) {
    if (n = n.options, r) {
      r = {};
      for (var c = 0; c < l.length; c++)
        r["$" + l[c]] = !0;
      for (l = 0; l < n.length; l++)
        c = r.hasOwnProperty("$" + n[l].value), n[l].selected !== c && (n[l].selected = c), c && o && (n[l].defaultSelected = !0);
    } else {
      for (l = "" + st(l), r = null, c = 0; c < n.length; c++) {
        if (n[c].value === l) {
          n[c].selected = !0, o && (n[c].defaultSelected = !0);
          return;
        }
        r !== null || n[c].disabled || (r = n[c]);
      }
      r !== null && (r.selected = !0);
    }
  }
  function Ir(n, r) {
    if (r.dangerouslySetInnerHTML != null)
      throw Error(k(91));
    return ae({}, r, { value: void 0, defaultValue: void 0, children: "" + n._wrapperState.initialValue });
  }
  function yr(n, r) {
    var l = r.value;
    if (l == null) {
      if (l = r.children, r = r.defaultValue, l != null) {
        if (r != null)
          throw Error(k(92));
        if (Gn(l)) {
          if (1 < l.length)
            throw Error(k(93));
          l = l[0];
        }
        r = l;
      }
      r == null && (r = ""), l = r;
    }
    n._wrapperState = { initialValue: st(l) };
  }
  function da(n, r) {
    var l = st(r.value), o = st(r.defaultValue);
    l != null && (l = "" + l, l !== n.value && (n.value = l), r.defaultValue == null && n.defaultValue !== l && (n.defaultValue = l)), o != null && (n.defaultValue = "" + o);
  }
  function rr(n) {
    var r = n.textContent;
    r === n._wrapperState.initialValue && r !== "" && r !== null && (n.value = r);
  }
  function Qr(n) {
    switch (n) {
      case "svg":
        return "http://www.w3.org/2000/svg";
      case "math":
        return "http://www.w3.org/1998/Math/MathML";
      default:
        return "http://www.w3.org/1999/xhtml";
    }
  }
  function hn(n, r) {
    return n == null || n === "http://www.w3.org/1999/xhtml" ? Qr(r) : n === "http://www.w3.org/2000/svg" && r === "foreignObject" ? "http://www.w3.org/1999/xhtml" : n;
  }
  var wr, fi = function(n) {
    return typeof MSApp < "u" && MSApp.execUnsafeLocalFunction ? function(r, l, o, c) {
      MSApp.execUnsafeLocalFunction(function() {
        return n(r, l, o, c);
      });
    } : n;
  }(function(n, r) {
    if (n.namespaceURI !== "http://www.w3.org/2000/svg" || "innerHTML" in n)
      n.innerHTML = r;
    else {
      for (wr = wr || document.createElement("div"), wr.innerHTML = "<svg>" + r.valueOf().toString() + "</svg>", r = wr.firstChild; n.firstChild; )
        n.removeChild(n.firstChild);
      for (; r.firstChild; )
        n.appendChild(r.firstChild);
    }
  });
  function pa(n, r) {
    if (r) {
      var l = n.firstChild;
      if (l && l === n.lastChild && l.nodeType === 3) {
        l.nodeValue = r;
        return;
      }
    }
    n.textContent = r;
  }
  var ee = {
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
  }, _e = ["Webkit", "ms", "Moz", "O"];
  Object.keys(ee).forEach(function(n) {
    _e.forEach(function(r) {
      r = r + n.charAt(0).toUpperCase() + n.substring(1), ee[r] = ee[n];
    });
  });
  function at(n, r, l) {
    return r == null || typeof r == "boolean" || r === "" ? "" : l || typeof r != "number" || r === 0 || ee.hasOwnProperty(n) && ee[n] ? ("" + r).trim() : r + "px";
  }
  function At(n, r) {
    n = n.style;
    for (var l in r)
      if (r.hasOwnProperty(l)) {
        var o = l.indexOf("--") === 0, c = at(l, r[l], o);
        l === "float" && (l = "cssFloat"), o ? n.setProperty(l, c) : n[l] = c;
      }
  }
  var Ht = ae({ menuitem: !0 }, { area: !0, base: !0, br: !0, col: !0, embed: !0, hr: !0, img: !0, input: !0, keygen: !0, link: !0, meta: !0, param: !0, source: !0, track: !0, wbr: !0 });
  function Dn(n, r) {
    if (r) {
      if (Ht[n] && (r.children != null || r.dangerouslySetInnerHTML != null))
        throw Error(k(137, n));
      if (r.dangerouslySetInnerHTML != null) {
        if (r.children != null)
          throw Error(k(60));
        if (typeof r.dangerouslySetInnerHTML != "object" || !("__html" in r.dangerouslySetInnerHTML))
          throw Error(k(61));
      }
      if (r.style != null && typeof r.style != "object")
        throw Error(k(62));
    }
  }
  function mn(n, r) {
    if (n.indexOf("-") === -1)
      return typeof r.is == "string";
    switch (n) {
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
  var gr = null;
  function It(n) {
    return n = n.target || n.srcElement || window, n.correspondingUseElement && (n = n.correspondingUseElement), n.nodeType === 3 ? n.parentNode : n;
  }
  var br = null, Vt = null, Pt = null;
  function Ja(n) {
    if (n = ss(n)) {
      if (typeof br != "function")
        throw Error(k(280));
      var r = n.stateNode;
      r && (r = Le(r), br(n.stateNode, n.type, r));
    }
  }
  function ka(n) {
    Vt ? Pt ? Pt.push(n) : Pt = [n] : Vt = n;
  }
  function ol() {
    if (Vt) {
      var n = Vt, r = Pt;
      if (Pt = Vt = null, Ja(n), r)
        for (n = 0; n < r.length; n++)
          Ja(r[n]);
    }
  }
  function Wl(n, r) {
    return n(r);
  }
  function Nu() {
  }
  var Mi = !1;
  function sl(n, r, l) {
    if (Mi)
      return n(r, l);
    Mi = !0;
    try {
      return Wl(n, r, l);
    } finally {
      Mi = !1, (Vt !== null || Pt !== null) && (Nu(), ol());
    }
  }
  function va(n, r) {
    var l = n.stateNode;
    if (l === null)
      return null;
    var o = Le(l);
    if (o === null)
      return null;
    l = o[r];
    e:
      switch (r) {
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
          (o = !o.disabled) || (n = n.type, o = !(n === "button" || n === "input" || n === "select" || n === "textarea")), n = !o;
          break e;
        default:
          n = !1;
      }
    if (n)
      return null;
    if (l && typeof l != "function")
      throw Error(k(231, r, typeof l));
    return l;
  }
  var di = !1;
  if (ut)
    try {
      var ha = {};
      Object.defineProperty(ha, "passive", { get: function() {
        di = !0;
      } }), window.addEventListener("test", ha, ha), window.removeEventListener("test", ha, ha);
    } catch {
      di = !1;
    }
  function ei(n, r, l, o, c, d, m, E, T) {
    var U = Array.prototype.slice.call(arguments, 3);
    try {
      r.apply(l, U);
    } catch (W) {
      this.onError(W);
    }
  }
  var _r = !1, ma = null, pi = !1, vi = null, R = { onError: function(n) {
    _r = !0, ma = n;
  } };
  function Y(n, r, l, o, c, d, m, E, T) {
    _r = !1, ma = null, ei.apply(R, arguments);
  }
  function q(n, r, l, o, c, d, m, E, T) {
    if (Y.apply(this, arguments), _r) {
      if (_r) {
        var U = ma;
        _r = !1, ma = null;
      } else
        throw Error(k(198));
      pi || (pi = !0, vi = U);
    }
  }
  function Te(n) {
    var r = n, l = n;
    if (n.alternate)
      for (; r.return; )
        r = r.return;
    else {
      n = r;
      do
        r = n, r.flags & 4098 && (l = r.return), n = r.return;
      while (n);
    }
    return r.tag === 3 ? l : null;
  }
  function dt(n) {
    if (n.tag === 13) {
      var r = n.memoizedState;
      if (r === null && (n = n.alternate, n !== null && (r = n.memoizedState)), r !== null)
        return r.dehydrated;
    }
    return null;
  }
  function Et(n) {
    if (Te(n) !== n)
      throw Error(k(188));
  }
  function Ae(n) {
    var r = n.alternate;
    if (!r) {
      if (r = Te(n), r === null)
        throw Error(k(188));
      return r !== n ? null : n;
    }
    for (var l = n, o = r; ; ) {
      var c = l.return;
      if (c === null)
        break;
      var d = c.alternate;
      if (d === null) {
        if (o = c.return, o !== null) {
          l = o;
          continue;
        }
        break;
      }
      if (c.child === d.child) {
        for (d = c.child; d; ) {
          if (d === l)
            return Et(c), n;
          if (d === o)
            return Et(c), r;
          d = d.sibling;
        }
        throw Error(k(188));
      }
      if (l.return !== o.return)
        l = c, o = d;
      else {
        for (var m = !1, E = c.child; E; ) {
          if (E === l) {
            m = !0, l = c, o = d;
            break;
          }
          if (E === o) {
            m = !0, o = c, l = d;
            break;
          }
          E = E.sibling;
        }
        if (!m) {
          for (E = d.child; E; ) {
            if (E === l) {
              m = !0, l = d, o = c;
              break;
            }
            if (E === o) {
              m = !0, o = d, l = c;
              break;
            }
            E = E.sibling;
          }
          if (!m)
            throw Error(k(189));
        }
      }
      if (l.alternate !== o)
        throw Error(k(190));
    }
    if (l.tag !== 3)
      throw Error(k(188));
    return l.stateNode.current === l ? n : r;
  }
  function it(n) {
    return n = Ae(n), n !== null ? Un(n) : null;
  }
  function Un(n) {
    if (n.tag === 5 || n.tag === 6)
      return n;
    for (n = n.child; n !== null; ) {
      var r = Un(n);
      if (r !== null)
        return r;
      n = n.sibling;
    }
    return null;
  }
  var Xt = B.unstable_scheduleCallback, an = B.unstable_cancelCallback, Sr = B.unstable_shouldYield, hi = B.unstable_requestPaint, Lt = B.unstable_now, qn = B.unstable_getCurrentPriorityLevel, kr = B.unstable_ImmediatePriority, lt = B.unstable_UserBlockingPriority, Da = B.unstable_NormalPriority, cl = B.unstable_LowPriority, zu = B.unstable_IdlePriority, fl = null, Wr = null;
  function Qo(n) {
    if (Wr && typeof Wr.onCommitFiberRoot == "function")
      try {
        Wr.onCommitFiberRoot(fl, n, void 0, (n.current.flags & 128) === 128);
      } catch {
      }
  }
  var Dr = Math.clz32 ? Math.clz32 : Zs, Wo = Math.log, Go = Math.LN2;
  function Zs(n) {
    return n >>>= 0, n === 0 ? 32 : 31 - (Wo(n) / Go | 0) | 0;
  }
  var Uu = 64, dl = 4194304;
  function ti(n) {
    switch (n & -n) {
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
        return n & 4194240;
      case 4194304:
      case 8388608:
      case 16777216:
      case 33554432:
      case 67108864:
        return n & 130023424;
      case 134217728:
        return 134217728;
      case 268435456:
        return 268435456;
      case 536870912:
        return 536870912;
      case 1073741824:
        return 1073741824;
      default:
        return n;
    }
  }
  function Or(n, r) {
    var l = n.pendingLanes;
    if (l === 0)
      return 0;
    var o = 0, c = n.suspendedLanes, d = n.pingedLanes, m = l & 268435455;
    if (m !== 0) {
      var E = m & ~c;
      E !== 0 ? o = ti(E) : (d &= m, d !== 0 && (o = ti(d)));
    } else
      m = l & ~c, m !== 0 ? o = ti(m) : d !== 0 && (o = ti(d));
    if (o === 0)
      return 0;
    if (r !== 0 && r !== o && !(r & c) && (c = o & -o, d = r & -r, c >= d || c === 16 && (d & 4194240) !== 0))
      return r;
    if (o & 4 && (o |= l & 16), r = n.entangledLanes, r !== 0)
      for (n = n.entanglements, r &= o; 0 < r; )
        l = 31 - Dr(r), c = 1 << l, o |= n[l], r &= ~c;
    return o;
  }
  function pl(n, r) {
    switch (n) {
      case 1:
      case 2:
      case 4:
        return r + 250;
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
        return r + 5e3;
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
  function vl(n, r) {
    for (var l = n.suspendedLanes, o = n.pingedLanes, c = n.expirationTimes, d = n.pendingLanes; 0 < d; ) {
      var m = 31 - Dr(d), E = 1 << m, T = c[m];
      T === -1 ? (!(E & l) || E & o) && (c[m] = pl(E, r)) : T <= r && (n.expiredLanes |= E), d &= ~E;
    }
  }
  function hl(n) {
    return n = n.pendingLanes & -1073741825, n !== 0 ? n : n & 1073741824 ? 1073741824 : 0;
  }
  function Au() {
    var n = Uu;
    return Uu <<= 1, !(Uu & 4194240) && (Uu = 64), n;
  }
  function ju(n) {
    for (var r = [], l = 0; 31 > l; l++)
      r.push(n);
    return r;
  }
  function Ni(n, r, l) {
    n.pendingLanes |= r, r !== 536870912 && (n.suspendedLanes = 0, n.pingedLanes = 0), n = n.eventTimes, r = 31 - Dr(r), n[r] = l;
  }
  function $f(n, r) {
    var l = n.pendingLanes & ~r;
    n.pendingLanes = r, n.suspendedLanes = 0, n.pingedLanes = 0, n.expiredLanes &= r, n.mutableReadLanes &= r, n.entangledLanes &= r, r = n.entanglements;
    var o = n.eventTimes;
    for (n = n.expirationTimes; 0 < l; ) {
      var c = 31 - Dr(l), d = 1 << c;
      r[c] = 0, o[c] = -1, n[c] = -1, l &= ~d;
    }
  }
  function mi(n, r) {
    var l = n.entangledLanes |= r;
    for (n = n.entanglements; l; ) {
      var o = 31 - Dr(l), c = 1 << o;
      c & r | n[o] & r && (n[o] |= r), l &= ~c;
    }
  }
  var Mt = 0;
  function Fu(n) {
    return n &= -n, 1 < n ? 4 < n ? n & 268435455 ? 16 : 536870912 : 4 : 1;
  }
  var Gl, Hu, Ct, Vu, Pu, We = !1, ql = [], yn = null, Gr = null, Lr = null, ml = /* @__PURE__ */ new Map(), Rn = /* @__PURE__ */ new Map(), Bt = [], Js = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
  function qr(n, r) {
    switch (n) {
      case "focusin":
      case "focusout":
        yn = null;
        break;
      case "dragenter":
      case "dragleave":
        Gr = null;
        break;
      case "mouseover":
      case "mouseout":
        Lr = null;
        break;
      case "pointerover":
      case "pointerout":
        ml.delete(r.pointerId);
        break;
      case "gotpointercapture":
      case "lostpointercapture":
        Rn.delete(r.pointerId);
    }
  }
  function Xn(n, r, l, o, c, d) {
    return n === null || n.nativeEvent !== d ? (n = { blockedOn: r, domEventName: l, eventSystemFlags: o, nativeEvent: d, targetContainers: [c] }, r !== null && (r = ss(r), r !== null && Hu(r)), n) : (n.eventSystemFlags |= o, r = n.targetContainers, c !== null && r.indexOf(c) === -1 && r.push(c), n);
  }
  function yi(n, r, l, o, c) {
    switch (r) {
      case "focusin":
        return yn = Xn(yn, n, r, l, o, c), !0;
      case "dragenter":
        return Gr = Xn(Gr, n, r, l, o, c), !0;
      case "mouseover":
        return Lr = Xn(Lr, n, r, l, o, c), !0;
      case "pointerover":
        var d = c.pointerId;
        return ml.set(d, Xn(ml.get(d) || null, n, r, l, o, c)), !0;
      case "gotpointercapture":
        return d = c.pointerId, Rn.set(d, Xn(Rn.get(d) || null, n, r, l, o, c)), !0;
    }
    return !1;
  }
  function ec(n) {
    var r = Na(n.target);
    if (r !== null) {
      var l = Te(r);
      if (l !== null) {
        if (r = l.tag, r === 13) {
          if (r = dt(l), r !== null) {
            n.blockedOn = r, Pu(n.priority, function() {
              Ct(l);
            });
            return;
          }
        } else if (r === 3 && l.stateNode.current.memoizedState.isDehydrated) {
          n.blockedOn = l.tag === 3 ? l.stateNode.containerInfo : null;
          return;
        }
      }
    }
    n.blockedOn = null;
  }
  function zi(n) {
    if (n.blockedOn !== null)
      return !1;
    for (var r = n.targetContainers; 0 < r.length; ) {
      var l = $u(n.domEventName, n.eventSystemFlags, r[0], n.nativeEvent);
      if (l === null) {
        l = n.nativeEvent;
        var o = new l.constructor(l.type, l);
        gr = o, l.target.dispatchEvent(o), gr = null;
      } else
        return r = ss(l), r !== null && Hu(r), n.blockedOn = l, !1;
      r.shift();
    }
    return !0;
  }
  function yl(n, r, l) {
    zi(n) && l.delete(r);
  }
  function tc() {
    We = !1, yn !== null && zi(yn) && (yn = null), Gr !== null && zi(Gr) && (Gr = null), Lr !== null && zi(Lr) && (Lr = null), ml.forEach(yl), Rn.forEach(yl);
  }
  function Oa(n, r) {
    n.blockedOn === r && (n.blockedOn = null, We || (We = !0, B.unstable_scheduleCallback(B.unstable_NormalPriority, tc)));
  }
  function gl(n) {
    function r(c) {
      return Oa(c, n);
    }
    if (0 < ql.length) {
      Oa(ql[0], n);
      for (var l = 1; l < ql.length; l++) {
        var o = ql[l];
        o.blockedOn === n && (o.blockedOn = null);
      }
    }
    for (yn !== null && Oa(yn, n), Gr !== null && Oa(Gr, n), Lr !== null && Oa(Lr, n), ml.forEach(r), Rn.forEach(r), l = 0; l < Bt.length; l++)
      o = Bt[l], o.blockedOn === n && (o.blockedOn = null);
    for (; 0 < Bt.length && (l = Bt[0], l.blockedOn === null); )
      ec(l), l.blockedOn === null && Bt.shift();
  }
  var Ui = mt.ReactCurrentBatchConfig, La = !0;
  function Bu(n, r, l, o) {
    var c = Mt, d = Ui.transition;
    Ui.transition = null;
    try {
      Mt = 1, El(n, r, l, o);
    } finally {
      Mt = c, Ui.transition = d;
    }
  }
  function Sl(n, r, l, o) {
    var c = Mt, d = Ui.transition;
    Ui.transition = null;
    try {
      Mt = 4, El(n, r, l, o);
    } finally {
      Mt = c, Ui.transition = d;
    }
  }
  function El(n, r, l, o) {
    if (La) {
      var c = $u(n, r, l, o);
      if (c === null)
        cc(n, r, o, Xl, l), qr(n, o);
      else if (yi(c, n, r, l, o))
        o.stopPropagation();
      else if (qr(n, o), r & 4 && -1 < Js.indexOf(n)) {
        for (; c !== null; ) {
          var d = ss(c);
          if (d !== null && Gl(d), d = $u(n, r, l, o), d === null && cc(n, r, o, Xl, l), d === c)
            break;
          c = d;
        }
        c !== null && o.stopPropagation();
      } else
        cc(n, r, o, null, l);
    }
  }
  var Xl = null;
  function $u(n, r, l, o) {
    if (Xl = null, n = It(o), n = Na(n), n !== null)
      if (r = Te(n), r === null)
        n = null;
      else if (l = r.tag, l === 13) {
        if (n = dt(r), n !== null)
          return n;
        n = null;
      } else if (l === 3) {
        if (r.stateNode.current.memoizedState.isDehydrated)
          return r.tag === 3 ? r.stateNode.containerInfo : null;
        n = null;
      } else
        r !== n && (n = null);
    return Xl = n, null;
  }
  function qo(n) {
    switch (n) {
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
        switch (qn()) {
          case kr:
            return 1;
          case lt:
            return 4;
          case Da:
          case cl:
            return 16;
          case zu:
            return 536870912;
          default:
            return 16;
        }
      default:
        return 16;
    }
  }
  var ni = null, h = null, C = null;
  function z() {
    if (C)
      return C;
    var n, r = h, l = r.length, o, c = "value" in ni ? ni.value : ni.textContent, d = c.length;
    for (n = 0; n < l && r[n] === c[n]; n++)
      ;
    var m = l - n;
    for (o = 1; o <= m && r[l - o] === c[d - o]; o++)
      ;
    return C = c.slice(n, 1 < o ? 1 - o : void 0);
  }
  function j(n) {
    var r = n.keyCode;
    return "charCode" in n ? (n = n.charCode, n === 0 && r === 13 && (n = 13)) : n = r, n === 10 && (n = 13), 32 <= n || n === 13 ? n : 0;
  }
  function K() {
    return !0;
  }
  function je() {
    return !1;
  }
  function ie(n) {
    function r(l, o, c, d, m) {
      this._reactName = l, this._targetInst = c, this.type = o, this.nativeEvent = d, this.target = m, this.currentTarget = null;
      for (var E in n)
        n.hasOwnProperty(E) && (l = n[E], this[E] = l ? l(d) : d[E]);
      return this.isDefaultPrevented = (d.defaultPrevented != null ? d.defaultPrevented : d.returnValue === !1) ? K : je, this.isPropagationStopped = je, this;
    }
    return ae(r.prototype, { preventDefault: function() {
      this.defaultPrevented = !0;
      var l = this.nativeEvent;
      l && (l.preventDefault ? l.preventDefault() : typeof l.returnValue != "unknown" && (l.returnValue = !1), this.isDefaultPrevented = K);
    }, stopPropagation: function() {
      var l = this.nativeEvent;
      l && (l.stopPropagation ? l.stopPropagation() : typeof l.cancelBubble != "unknown" && (l.cancelBubble = !0), this.isPropagationStopped = K);
    }, persist: function() {
    }, isPersistent: K }), r;
  }
  var Ne = { eventPhase: 0, bubbles: 0, cancelable: 0, timeStamp: function(n) {
    return n.timeStamp || Date.now();
  }, defaultPrevented: 0, isTrusted: 0 }, pt = ie(Ne), kt = ae({}, Ne, { view: 0, detail: 0 }), Kt = ie(kt), Qt, Zt, tn, Rt = ae({}, kt, { screenX: 0, screenY: 0, clientX: 0, clientY: 0, pageX: 0, pageY: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, getModifierState: Gf, button: 0, buttons: 0, relatedTarget: function(n) {
    return n.relatedTarget === void 0 ? n.fromElement === n.srcElement ? n.toElement : n.fromElement : n.relatedTarget;
  }, movementX: function(n) {
    return "movementX" in n ? n.movementX : (n !== tn && (tn && n.type === "mousemove" ? (Qt = n.screenX - tn.screenX, Zt = n.screenY - tn.screenY) : Zt = Qt = 0, tn = n), Qt);
  }, movementY: function(n) {
    return "movementY" in n ? n.movementY : Zt;
  } }), Ai = ie(Rt), Yu = ae({}, Rt, { dataTransfer: 0 }), Xo = ie(Yu), Yf = ae({}, kt, { relatedTarget: 0 }), ri = ie(Yf), Ko = ae({}, Ne, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }), Zo = ie(Ko), If = ae({}, Ne, { clipboardData: function(n) {
    return "clipboardData" in n ? n.clipboardData : window.clipboardData;
  } }), Ym = ie(If), Im = ae({}, Ne, { data: 0 }), Qf = ie(Im), Wf = {
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
  }, Zp = {
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
  }, Jp = { Alt: "altKey", Control: "ctrlKey", Meta: "metaKey", Shift: "shiftKey" };
  function ev(n) {
    var r = this.nativeEvent;
    return r.getModifierState ? r.getModifierState(n) : (n = Jp[n]) ? !!r[n] : !1;
  }
  function Gf() {
    return ev;
  }
  var ji = ae({}, kt, { key: function(n) {
    if (n.key) {
      var r = Wf[n.key] || n.key;
      if (r !== "Unidentified")
        return r;
    }
    return n.type === "keypress" ? (n = j(n), n === 13 ? "Enter" : String.fromCharCode(n)) : n.type === "keydown" || n.type === "keyup" ? Zp[n.keyCode] || "Unidentified" : "";
  }, code: 0, location: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, repeat: 0, locale: 0, getModifierState: Gf, charCode: function(n) {
    return n.type === "keypress" ? j(n) : 0;
  }, keyCode: function(n) {
    return n.type === "keydown" || n.type === "keyup" ? n.keyCode : 0;
  }, which: function(n) {
    return n.type === "keypress" ? j(n) : n.type === "keydown" || n.type === "keyup" ? n.keyCode : 0;
  } }), Qm = ie(ji), qf = ae({}, Rt, { pointerId: 0, width: 0, height: 0, pressure: 0, tangentialPressure: 0, tiltX: 0, tiltY: 0, twist: 0, pointerType: 0, isPrimary: 0 }), nc = ie(qf), Xf = ae({}, kt, { touches: 0, targetTouches: 0, changedTouches: 0, altKey: 0, metaKey: 0, ctrlKey: 0, shiftKey: 0, getModifierState: Gf }), Wm = ie(Xf), rc = ae({}, Ne, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }), tv = ie(rc), Xr = ae({}, Rt, {
    deltaX: function(n) {
      return "deltaX" in n ? n.deltaX : "wheelDeltaX" in n ? -n.wheelDeltaX : 0;
    },
    deltaY: function(n) {
      return "deltaY" in n ? n.deltaY : "wheelDeltaY" in n ? -n.wheelDeltaY : "wheelDelta" in n ? -n.wheelDelta : 0;
    },
    deltaZ: 0,
    deltaMode: 0
  }), Fi = ie(Xr), An = [9, 13, 27, 32], ai = ut && "CompositionEvent" in window, Kl = null;
  ut && "documentMode" in document && (Kl = document.documentMode);
  var ac = ut && "TextEvent" in window && !Kl, nv = ut && (!ai || Kl && 8 < Kl && 11 >= Kl), Iu = String.fromCharCode(32), rv = !1;
  function av(n, r) {
    switch (n) {
      case "keyup":
        return An.indexOf(r.keyCode) !== -1;
      case "keydown":
        return r.keyCode !== 229;
      case "keypress":
      case "mousedown":
      case "focusout":
        return !0;
      default:
        return !1;
    }
  }
  function ic(n) {
    return n = n.detail, typeof n == "object" && "data" in n ? n.data : null;
  }
  var Qu = !1;
  function Gm(n, r) {
    switch (n) {
      case "compositionend":
        return ic(r);
      case "keypress":
        return r.which !== 32 ? null : (rv = !0, Iu);
      case "textInput":
        return n = r.data, n === Iu && rv ? null : n;
      default:
        return null;
    }
  }
  function qm(n, r) {
    if (Qu)
      return n === "compositionend" || !ai && av(n, r) ? (n = z(), C = h = ni = null, Qu = !1, n) : null;
    switch (n) {
      case "paste":
        return null;
      case "keypress":
        if (!(r.ctrlKey || r.altKey || r.metaKey) || r.ctrlKey && r.altKey) {
          if (r.char && 1 < r.char.length)
            return r.char;
          if (r.which)
            return String.fromCharCode(r.which);
        }
        return null;
      case "compositionend":
        return nv && r.locale !== "ko" ? null : r.data;
      default:
        return null;
    }
  }
  var iv = { color: !0, date: !0, datetime: !0, "datetime-local": !0, email: !0, month: !0, number: !0, password: !0, range: !0, search: !0, tel: !0, text: !0, time: !0, url: !0, week: !0 };
  function lv(n) {
    var r = n && n.nodeName && n.nodeName.toLowerCase();
    return r === "input" ? !!iv[n.type] : r === "textarea";
  }
  function uv(n, r, l, o) {
    ka(o), r = ls(r, "onChange"), 0 < r.length && (l = new pt("onChange", "change", null, l, o), n.push({ event: l, listeners: r }));
  }
  var Jo = null, Wu = null;
  function Gu(n) {
    sc(n, 0);
  }
  function qu(n) {
    var r = Ku(n);
    if (Br(r))
      return n;
  }
  function ov(n, r) {
    if (n === "change")
      return r;
  }
  var Kf = !1;
  if (ut) {
    var Zf;
    if (ut) {
      var Jf = "oninput" in document;
      if (!Jf) {
        var sv = document.createElement("div");
        sv.setAttribute("oninput", "return;"), Jf = typeof sv.oninput == "function";
      }
      Zf = Jf;
    } else
      Zf = !1;
    Kf = Zf && (!document.documentMode || 9 < document.documentMode);
  }
  function cv() {
    Jo && (Jo.detachEvent("onpropertychange", fv), Wu = Jo = null);
  }
  function fv(n) {
    if (n.propertyName === "value" && qu(Wu)) {
      var r = [];
      uv(r, Wu, n, It(n)), sl(Gu, r);
    }
  }
  function Xm(n, r, l) {
    n === "focusin" ? (cv(), Jo = r, Wu = l, Jo.attachEvent("onpropertychange", fv)) : n === "focusout" && cv();
  }
  function Km(n) {
    if (n === "selectionchange" || n === "keyup" || n === "keydown")
      return qu(Wu);
  }
  function Zm(n, r) {
    if (n === "click")
      return qu(r);
  }
  function dv(n, r) {
    if (n === "input" || n === "change")
      return qu(r);
  }
  function Jm(n, r) {
    return n === r && (n !== 0 || 1 / n === 1 / r) || n !== n && r !== r;
  }
  var Ma = typeof Object.is == "function" ? Object.is : Jm;
  function es(n, r) {
    if (Ma(n, r))
      return !0;
    if (typeof n != "object" || n === null || typeof r != "object" || r === null)
      return !1;
    var l = Object.keys(n), o = Object.keys(r);
    if (l.length !== o.length)
      return !1;
    for (o = 0; o < l.length; o++) {
      var c = l[o];
      if (!de.call(r, c) || !Ma(n[c], r[c]))
        return !1;
    }
    return !0;
  }
  function pv(n) {
    for (; n && n.firstChild; )
      n = n.firstChild;
    return n;
  }
  function vv(n, r) {
    var l = pv(n);
    n = 0;
    for (var o; l; ) {
      if (l.nodeType === 3) {
        if (o = n + l.textContent.length, n <= r && o >= r)
          return { node: l, offset: r - n };
        n = o;
      }
      e: {
        for (; l; ) {
          if (l.nextSibling) {
            l = l.nextSibling;
            break e;
          }
          l = l.parentNode;
        }
        l = void 0;
      }
      l = pv(l);
    }
  }
  function hv(n, r) {
    return n && r ? n === r ? !0 : n && n.nodeType === 3 ? !1 : r && r.nodeType === 3 ? hv(n, r.parentNode) : "contains" in n ? n.contains(r) : n.compareDocumentPosition ? !!(n.compareDocumentPosition(r) & 16) : !1 : !1;
  }
  function lc() {
    for (var n = window, r = vn(); r instanceof n.HTMLIFrameElement; ) {
      try {
        var l = typeof r.contentWindow.location.href == "string";
      } catch {
        l = !1;
      }
      if (l)
        n = r.contentWindow;
      else
        break;
      r = vn(n.document);
    }
    return r;
  }
  function Hi(n) {
    var r = n && n.nodeName && n.nodeName.toLowerCase();
    return r && (r === "input" && (n.type === "text" || n.type === "search" || n.type === "tel" || n.type === "url" || n.type === "password") || r === "textarea" || n.contentEditable === "true");
  }
  function uc(n) {
    var r = lc(), l = n.focusedElem, o = n.selectionRange;
    if (r !== l && l && l.ownerDocument && hv(l.ownerDocument.documentElement, l)) {
      if (o !== null && Hi(l)) {
        if (r = o.start, n = o.end, n === void 0 && (n = r), "selectionStart" in l)
          l.selectionStart = r, l.selectionEnd = Math.min(n, l.value.length);
        else if (n = (r = l.ownerDocument || document) && r.defaultView || window, n.getSelection) {
          n = n.getSelection();
          var c = l.textContent.length, d = Math.min(o.start, c);
          o = o.end === void 0 ? d : Math.min(o.end, c), !n.extend && d > o && (c = o, o = d, d = c), c = vv(l, d);
          var m = vv(
            l,
            o
          );
          c && m && (n.rangeCount !== 1 || n.anchorNode !== c.node || n.anchorOffset !== c.offset || n.focusNode !== m.node || n.focusOffset !== m.offset) && (r = r.createRange(), r.setStart(c.node, c.offset), n.removeAllRanges(), d > o ? (n.addRange(r), n.extend(m.node, m.offset)) : (r.setEnd(m.node, m.offset), n.addRange(r)));
        }
      }
      for (r = [], n = l; n = n.parentNode; )
        n.nodeType === 1 && r.push({ element: n, left: n.scrollLeft, top: n.scrollTop });
      for (typeof l.focus == "function" && l.focus(), l = 0; l < r.length; l++)
        n = r[l], n.element.scrollLeft = n.left, n.element.scrollTop = n.top;
    }
  }
  var mv = ut && "documentMode" in document && 11 >= document.documentMode, ii = null, ed = null, ts = null, td = !1;
  function yv(n, r, l) {
    var o = l.window === l ? l.document : l.nodeType === 9 ? l : l.ownerDocument;
    td || ii == null || ii !== vn(o) || (o = ii, "selectionStart" in o && Hi(o) ? o = { start: o.selectionStart, end: o.selectionEnd } : (o = (o.ownerDocument && o.ownerDocument.defaultView || window).getSelection(), o = { anchorNode: o.anchorNode, anchorOffset: o.anchorOffset, focusNode: o.focusNode, focusOffset: o.focusOffset }), ts && es(ts, o) || (ts = o, o = ls(ed, "onSelect"), 0 < o.length && (r = new pt("onSelect", "select", null, r, l), n.push({ event: r, listeners: o }), r.target = ii)));
  }
  function oc(n, r) {
    var l = {};
    return l[n.toLowerCase()] = r.toLowerCase(), l["Webkit" + n] = "webkit" + r, l["Moz" + n] = "moz" + r, l;
  }
  var Zl = { animationend: oc("Animation", "AnimationEnd"), animationiteration: oc("Animation", "AnimationIteration"), animationstart: oc("Animation", "AnimationStart"), transitionend: oc("Transition", "TransitionEnd") }, nd = {}, rd = {};
  ut && (rd = document.createElement("div").style, "AnimationEvent" in window || (delete Zl.animationend.animation, delete Zl.animationiteration.animation, delete Zl.animationstart.animation), "TransitionEvent" in window || delete Zl.transitionend.transition);
  function Kn(n) {
    if (nd[n])
      return nd[n];
    if (!Zl[n])
      return n;
    var r = Zl[n], l;
    for (l in r)
      if (r.hasOwnProperty(l) && l in rd)
        return nd[n] = r[l];
    return n;
  }
  var ad = Kn("animationend"), gv = Kn("animationiteration"), Sv = Kn("animationstart"), Ev = Kn("transitionend"), Cv = /* @__PURE__ */ new Map(), Rv = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
  function Vi(n, r) {
    Cv.set(n, r), $e(r, [n]);
  }
  for (var ns = 0; ns < Rv.length; ns++) {
    var Jl = Rv[ns], ey = Jl.toLowerCase(), rs = Jl[0].toUpperCase() + Jl.slice(1);
    Vi(ey, "on" + rs);
  }
  Vi(ad, "onAnimationEnd"), Vi(gv, "onAnimationIteration"), Vi(Sv, "onAnimationStart"), Vi("dblclick", "onDoubleClick"), Vi("focusin", "onFocus"), Vi("focusout", "onBlur"), Vi(Ev, "onTransitionEnd"), S("onMouseEnter", ["mouseout", "mouseover"]), S("onMouseLeave", ["mouseout", "mouseover"]), S("onPointerEnter", ["pointerout", "pointerover"]), S("onPointerLeave", ["pointerout", "pointerover"]), $e("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" ")), $e("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" ")), $e("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]), $e("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" ")), $e("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" ")), $e("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
  var as = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), ty = new Set("cancel close invalid load scroll toggle".split(" ").concat(as));
  function Tv(n, r, l) {
    var o = n.type || "unknown-event";
    n.currentTarget = l, q(o, r, void 0, n), n.currentTarget = null;
  }
  function sc(n, r) {
    r = (r & 4) !== 0;
    for (var l = 0; l < n.length; l++) {
      var o = n[l], c = o.event;
      o = o.listeners;
      e: {
        var d = void 0;
        if (r)
          for (var m = o.length - 1; 0 <= m; m--) {
            var E = o[m], T = E.instance, U = E.currentTarget;
            if (E = E.listener, T !== d && c.isPropagationStopped())
              break e;
            Tv(c, E, U), d = T;
          }
        else
          for (m = 0; m < o.length; m++) {
            if (E = o[m], T = E.instance, U = E.currentTarget, E = E.listener, T !== d && c.isPropagationStopped())
              break e;
            Tv(c, E, U), d = T;
          }
      }
    }
    if (pi)
      throw n = vi, pi = !1, vi = null, n;
  }
  function Jt(n, r) {
    var l = r[fd];
    l === void 0 && (l = r[fd] = /* @__PURE__ */ new Set());
    var o = n + "__bubble";
    l.has(o) || (xv(r, n, 2, !1), l.add(o));
  }
  function Cl(n, r, l) {
    var o = 0;
    r && (o |= 4), xv(l, n, o, r);
  }
  var Pi = "_reactListening" + Math.random().toString(36).slice(2);
  function Xu(n) {
    if (!n[Pi]) {
      n[Pi] = !0, Ze.forEach(function(l) {
        l !== "selectionchange" && (ty.has(l) || Cl(l, !1, n), Cl(l, !0, n));
      });
      var r = n.nodeType === 9 ? n : n.ownerDocument;
      r === null || r[Pi] || (r[Pi] = !0, Cl("selectionchange", !1, r));
    }
  }
  function xv(n, r, l, o) {
    switch (qo(r)) {
      case 1:
        var c = Bu;
        break;
      case 4:
        c = Sl;
        break;
      default:
        c = El;
    }
    l = c.bind(null, r, l, n), c = void 0, !di || r !== "touchstart" && r !== "touchmove" && r !== "wheel" || (c = !0), o ? c !== void 0 ? n.addEventListener(r, l, { capture: !0, passive: c }) : n.addEventListener(r, l, !0) : c !== void 0 ? n.addEventListener(r, l, { passive: c }) : n.addEventListener(r, l, !1);
  }
  function cc(n, r, l, o, c) {
    var d = o;
    if (!(r & 1) && !(r & 2) && o !== null)
      e:
        for (; ; ) {
          if (o === null)
            return;
          var m = o.tag;
          if (m === 3 || m === 4) {
            var E = o.stateNode.containerInfo;
            if (E === c || E.nodeType === 8 && E.parentNode === c)
              break;
            if (m === 4)
              for (m = o.return; m !== null; ) {
                var T = m.tag;
                if ((T === 3 || T === 4) && (T = m.stateNode.containerInfo, T === c || T.nodeType === 8 && T.parentNode === c))
                  return;
                m = m.return;
              }
            for (; E !== null; ) {
              if (m = Na(E), m === null)
                return;
              if (T = m.tag, T === 5 || T === 6) {
                o = d = m;
                continue e;
              }
              E = E.parentNode;
            }
          }
          o = o.return;
        }
    sl(function() {
      var U = d, W = It(l), G = [];
      e: {
        var I = Cv.get(n);
        if (I !== void 0) {
          var ce = pt, ye = n;
          switch (n) {
            case "keypress":
              if (j(l) === 0)
                break e;
            case "keydown":
            case "keyup":
              ce = Qm;
              break;
            case "focusin":
              ye = "focus", ce = ri;
              break;
            case "focusout":
              ye = "blur", ce = ri;
              break;
            case "beforeblur":
            case "afterblur":
              ce = ri;
              break;
            case "click":
              if (l.button === 2)
                break e;
            case "auxclick":
            case "dblclick":
            case "mousedown":
            case "mousemove":
            case "mouseup":
            case "mouseout":
            case "mouseover":
            case "contextmenu":
              ce = Ai;
              break;
            case "drag":
            case "dragend":
            case "dragenter":
            case "dragexit":
            case "dragleave":
            case "dragover":
            case "dragstart":
            case "drop":
              ce = Xo;
              break;
            case "touchcancel":
            case "touchend":
            case "touchmove":
            case "touchstart":
              ce = Wm;
              break;
            case ad:
            case gv:
            case Sv:
              ce = Zo;
              break;
            case Ev:
              ce = tv;
              break;
            case "scroll":
              ce = Kt;
              break;
            case "wheel":
              ce = Fi;
              break;
            case "copy":
            case "cut":
            case "paste":
              ce = Ym;
              break;
            case "gotpointercapture":
            case "lostpointercapture":
            case "pointercancel":
            case "pointerdown":
            case "pointermove":
            case "pointerout":
            case "pointerover":
            case "pointerup":
              ce = nc;
          }
          var Ee = (r & 4) !== 0, Mn = !Ee && n === "scroll", D = Ee ? I !== null ? I + "Capture" : null : I;
          Ee = [];
          for (var w = U, M; w !== null; ) {
            M = w;
            var Z = M.stateNode;
            if (M.tag === 5 && Z !== null && (M = Z, D !== null && (Z = va(w, D), Z != null && Ee.push(is(w, Z, M)))), Mn)
              break;
            w = w.return;
          }
          0 < Ee.length && (I = new ce(I, ye, null, l, W), G.push({ event: I, listeners: Ee }));
        }
      }
      if (!(r & 7)) {
        e: {
          if (I = n === "mouseover" || n === "pointerover", ce = n === "mouseout" || n === "pointerout", I && l !== gr && (ye = l.relatedTarget || l.fromElement) && (Na(ye) || ye[Bi]))
            break e;
          if ((ce || I) && (I = W.window === W ? W : (I = W.ownerDocument) ? I.defaultView || I.parentWindow : window, ce ? (ye = l.relatedTarget || l.toElement, ce = U, ye = ye ? Na(ye) : null, ye !== null && (Mn = Te(ye), ye !== Mn || ye.tag !== 5 && ye.tag !== 6) && (ye = null)) : (ce = null, ye = U), ce !== ye)) {
            if (Ee = Ai, Z = "onMouseLeave", D = "onMouseEnter", w = "mouse", (n === "pointerout" || n === "pointerover") && (Ee = nc, Z = "onPointerLeave", D = "onPointerEnter", w = "pointer"), Mn = ce == null ? I : Ku(ce), M = ye == null ? I : Ku(ye), I = new Ee(Z, w + "leave", ce, l, W), I.target = Mn, I.relatedTarget = M, Z = null, Na(W) === U && (Ee = new Ee(D, w + "enter", ye, l, W), Ee.target = M, Ee.relatedTarget = Mn, Z = Ee), Mn = Z, ce && ye)
              t: {
                for (Ee = ce, D = ye, w = 0, M = Ee; M; M = eu(M))
                  w++;
                for (M = 0, Z = D; Z; Z = eu(Z))
                  M++;
                for (; 0 < w - M; )
                  Ee = eu(Ee), w--;
                for (; 0 < M - w; )
                  D = eu(D), M--;
                for (; w--; ) {
                  if (Ee === D || D !== null && Ee === D.alternate)
                    break t;
                  Ee = eu(Ee), D = eu(D);
                }
                Ee = null;
              }
            else
              Ee = null;
            ce !== null && id(G, I, ce, Ee, !1), ye !== null && Mn !== null && id(G, Mn, ye, Ee, !0);
          }
        }
        e: {
          if (I = U ? Ku(U) : window, ce = I.nodeName && I.nodeName.toLowerCase(), ce === "select" || ce === "input" && I.type === "file")
            var Re = ov;
          else if (lv(I))
            if (Kf)
              Re = dv;
            else {
              Re = Km;
              var Fe = Xm;
            }
          else
            (ce = I.nodeName) && ce.toLowerCase() === "input" && (I.type === "checkbox" || I.type === "radio") && (Re = Zm);
          if (Re && (Re = Re(n, U))) {
            uv(G, Re, l, W);
            break e;
          }
          Fe && Fe(n, I, U), n === "focusout" && (Fe = I._wrapperState) && Fe.controlled && I.type === "number" && Yr(I, "number", I.value);
        }
        switch (Fe = U ? Ku(U) : window, n) {
          case "focusin":
            (lv(Fe) || Fe.contentEditable === "true") && (ii = Fe, ed = U, ts = null);
            break;
          case "focusout":
            ts = ed = ii = null;
            break;
          case "mousedown":
            td = !0;
            break;
          case "contextmenu":
          case "mouseup":
          case "dragend":
            td = !1, yv(G, l, W);
            break;
          case "selectionchange":
            if (mv)
              break;
          case "keydown":
          case "keyup":
            yv(G, l, W);
        }
        var ge;
        if (ai)
          e: {
            switch (n) {
              case "compositionstart":
                var He = "onCompositionStart";
                break e;
              case "compositionend":
                He = "onCompositionEnd";
                break e;
              case "compositionupdate":
                He = "onCompositionUpdate";
                break e;
            }
            He = void 0;
          }
        else
          Qu ? av(n, l) && (He = "onCompositionEnd") : n === "keydown" && l.keyCode === 229 && (He = "onCompositionStart");
        He && (nv && l.locale !== "ko" && (Qu || He !== "onCompositionStart" ? He === "onCompositionEnd" && Qu && (ge = z()) : (ni = W, h = "value" in ni ? ni.value : ni.textContent, Qu = !0)), Fe = ls(U, He), 0 < Fe.length && (He = new Qf(He, n, null, l, W), G.push({ event: He, listeners: Fe }), ge ? He.data = ge : (ge = ic(l), ge !== null && (He.data = ge)))), (ge = ac ? Gm(n, l) : qm(n, l)) && (U = ls(U, "onBeforeInput"), 0 < U.length && (W = new Qf("onBeforeInput", "beforeinput", null, l, W), G.push({ event: W, listeners: U }), W.data = ge));
      }
      sc(G, r);
    });
  }
  function is(n, r, l) {
    return { instance: n, listener: r, currentTarget: l };
  }
  function ls(n, r) {
    for (var l = r + "Capture", o = []; n !== null; ) {
      var c = n, d = c.stateNode;
      c.tag === 5 && d !== null && (c = d, d = va(n, l), d != null && o.unshift(is(n, d, c)), d = va(n, r), d != null && o.push(is(n, d, c))), n = n.return;
    }
    return o;
  }
  function eu(n) {
    if (n === null)
      return null;
    do
      n = n.return;
    while (n && n.tag !== 5);
    return n || null;
  }
  function id(n, r, l, o, c) {
    for (var d = r._reactName, m = []; l !== null && l !== o; ) {
      var E = l, T = E.alternate, U = E.stateNode;
      if (T !== null && T === o)
        break;
      E.tag === 5 && U !== null && (E = U, c ? (T = va(l, d), T != null && m.unshift(is(l, T, E))) : c || (T = va(l, d), T != null && m.push(is(l, T, E)))), l = l.return;
    }
    m.length !== 0 && n.push({ event: r, listeners: m });
  }
  var ld = /\r\n?/g, ny = /\u0000|\uFFFD/g;
  function ud(n) {
    return (typeof n == "string" ? n : "" + n).replace(ld, `
`).replace(ny, "");
  }
  function fc(n, r, l) {
    if (r = ud(r), ud(n) !== r && l)
      throw Error(k(425));
  }
  function dc() {
  }
  var od = null, tu = null;
  function us(n, r) {
    return n === "textarea" || n === "noscript" || typeof r.children == "string" || typeof r.children == "number" || typeof r.dangerouslySetInnerHTML == "object" && r.dangerouslySetInnerHTML !== null && r.dangerouslySetInnerHTML.__html != null;
  }
  var nu = typeof setTimeout == "function" ? setTimeout : void 0, wv = typeof clearTimeout == "function" ? clearTimeout : void 0, sd = typeof Promise == "function" ? Promise : void 0, cd = typeof queueMicrotask == "function" ? queueMicrotask : typeof sd < "u" ? function(n) {
    return sd.resolve(null).then(n).catch(ry);
  } : nu;
  function ry(n) {
    setTimeout(function() {
      throw n;
    });
  }
  function Rl(n, r) {
    var l = r, o = 0;
    do {
      var c = l.nextSibling;
      if (n.removeChild(l), c && c.nodeType === 8)
        if (l = c.data, l === "/$") {
          if (o === 0) {
            n.removeChild(c), gl(r);
            return;
          }
          o--;
        } else
          l !== "$" && l !== "$?" && l !== "$!" || o++;
      l = c;
    } while (l);
    gl(r);
  }
  function li(n) {
    for (; n != null; n = n.nextSibling) {
      var r = n.nodeType;
      if (r === 1 || r === 3)
        break;
      if (r === 8) {
        if (r = n.data, r === "$" || r === "$!" || r === "$?")
          break;
        if (r === "/$")
          return null;
      }
    }
    return n;
  }
  function os(n) {
    n = n.previousSibling;
    for (var r = 0; n; ) {
      if (n.nodeType === 8) {
        var l = n.data;
        if (l === "$" || l === "$!" || l === "$?") {
          if (r === 0)
            return n;
          r--;
        } else
          l === "/$" && r++;
      }
      n = n.previousSibling;
    }
    return null;
  }
  var Tl = Math.random().toString(36).slice(2), gi = "__reactFiber$" + Tl, ru = "__reactProps$" + Tl, Bi = "__reactContainer$" + Tl, fd = "__reactEvents$" + Tl, ay = "__reactListeners$" + Tl, dd = "__reactHandles$" + Tl;
  function Na(n) {
    var r = n[gi];
    if (r)
      return r;
    for (var l = n.parentNode; l; ) {
      if (r = l[Bi] || l[gi]) {
        if (l = r.alternate, r.child !== null || l !== null && l.child !== null)
          for (n = os(n); n !== null; ) {
            if (l = n[gi])
              return l;
            n = os(n);
          }
        return r;
      }
      n = l, l = n.parentNode;
    }
    return null;
  }
  function ss(n) {
    return n = n[gi] || n[Bi], !n || n.tag !== 5 && n.tag !== 6 && n.tag !== 13 && n.tag !== 3 ? null : n;
  }
  function Ku(n) {
    if (n.tag === 5 || n.tag === 6)
      return n.stateNode;
    throw Error(k(33));
  }
  function Le(n) {
    return n[ru] || null;
  }
  var xl = [], ln = -1;
  function et(n) {
    return { current: n };
  }
  function jt(n) {
    0 > ln || (n.current = xl[ln], xl[ln] = null, ln--);
  }
  function $t(n, r) {
    ln++, xl[ln] = n.current, n.current = r;
  }
  var Si = {}, Ie = et(Si), Tn = et(!1), Kr = Si;
  function za(n, r) {
    var l = n.type.contextTypes;
    if (!l)
      return Si;
    var o = n.stateNode;
    if (o && o.__reactInternalMemoizedUnmaskedChildContext === r)
      return o.__reactInternalMemoizedMaskedChildContext;
    var c = {}, d;
    for (d in l)
      c[d] = r[d];
    return o && (n = n.stateNode, n.__reactInternalMemoizedUnmaskedChildContext = r, n.__reactInternalMemoizedMaskedChildContext = c), c;
  }
  function cn(n) {
    return n = n.childContextTypes, n != null;
  }
  function Ua() {
    jt(Tn), jt(Ie);
  }
  function wl(n, r, l) {
    if (Ie.current !== Si)
      throw Error(k(168));
    $t(Ie, r), $t(Tn, l);
  }
  function cs(n, r, l) {
    var o = n.stateNode;
    if (r = r.childContextTypes, typeof o.getChildContext != "function")
      return l;
    o = o.getChildContext();
    for (var c in o)
      if (!(c in r))
        throw Error(k(108, St(n) || "Unknown", c));
    return ae({}, l, o);
  }
  function pc(n) {
    return n = (n = n.stateNode) && n.__reactInternalMemoizedMergedChildContext || Si, Kr = Ie.current, $t(Ie, n), $t(Tn, Tn.current), !0;
  }
  function bv(n, r, l) {
    var o = n.stateNode;
    if (!o)
      throw Error(k(169));
    l ? (n = cs(n, r, Kr), o.__reactInternalMemoizedMergedChildContext = n, jt(Tn), jt(Ie), $t(Ie, n)) : jt(Tn), $t(Tn, l);
  }
  var ya = null, Zn = !1, fs = !1;
  function pd(n) {
    ya === null ? ya = [n] : ya.push(n);
  }
  function vd(n) {
    Zn = !0, pd(n);
  }
  function Zr() {
    if (!fs && ya !== null) {
      fs = !0;
      var n = 0, r = Mt;
      try {
        var l = ya;
        for (Mt = 1; n < l.length; n++) {
          var o = l[n];
          do
            o = o(!0);
          while (o !== null);
        }
        ya = null, Zn = !1;
      } catch (c) {
        throw ya !== null && (ya = ya.slice(n + 1)), Xt(kr, Zr), c;
      } finally {
        Mt = r, fs = !1;
      }
    }
    return null;
  }
  var bl = [], Jr = 0, au = null, Zu = 0, ea = [], Er = 0, Aa = null, ar = 1, $i = "";
  function ga(n, r) {
    bl[Jr++] = Zu, bl[Jr++] = au, au = n, Zu = r;
  }
  function hd(n, r, l) {
    ea[Er++] = ar, ea[Er++] = $i, ea[Er++] = Aa, Aa = n;
    var o = ar;
    n = $i;
    var c = 32 - Dr(o) - 1;
    o &= ~(1 << c), l += 1;
    var d = 32 - Dr(r) + c;
    if (30 < d) {
      var m = c - c % 5;
      d = (o & (1 << m) - 1).toString(32), o >>= m, c -= m, ar = 1 << 32 - Dr(r) + c | l << c | o, $i = d + n;
    } else
      ar = 1 << d | l << c | o, $i = n;
  }
  function vc(n) {
    n.return !== null && (ga(n, 1), hd(n, 1, 0));
  }
  function md(n) {
    for (; n === au; )
      au = bl[--Jr], bl[Jr] = null, Zu = bl[--Jr], bl[Jr] = null;
    for (; n === Aa; )
      Aa = ea[--Er], ea[Er] = null, $i = ea[--Er], ea[Er] = null, ar = ea[--Er], ea[Er] = null;
  }
  var Sa = null, ta = null, un = !1, ja = null;
  function yd(n, r) {
    var l = Ia(5, null, null, 0);
    l.elementType = "DELETED", l.stateNode = r, l.return = n, r = n.deletions, r === null ? (n.deletions = [l], n.flags |= 16) : r.push(l);
  }
  function _v(n, r) {
    switch (n.tag) {
      case 5:
        var l = n.type;
        return r = r.nodeType !== 1 || l.toLowerCase() !== r.nodeName.toLowerCase() ? null : r, r !== null ? (n.stateNode = r, Sa = n, ta = li(r.firstChild), !0) : !1;
      case 6:
        return r = n.pendingProps === "" || r.nodeType !== 3 ? null : r, r !== null ? (n.stateNode = r, Sa = n, ta = null, !0) : !1;
      case 13:
        return r = r.nodeType !== 8 ? null : r, r !== null ? (l = Aa !== null ? { id: ar, overflow: $i } : null, n.memoizedState = { dehydrated: r, treeContext: l, retryLane: 1073741824 }, l = Ia(18, null, null, 0), l.stateNode = r, l.return = n, n.child = l, Sa = n, ta = null, !0) : !1;
      default:
        return !1;
    }
  }
  function hc(n) {
    return (n.mode & 1) !== 0 && (n.flags & 128) === 0;
  }
  function mc(n) {
    if (un) {
      var r = ta;
      if (r) {
        var l = r;
        if (!_v(n, r)) {
          if (hc(n))
            throw Error(k(418));
          r = li(l.nextSibling);
          var o = Sa;
          r && _v(n, r) ? yd(o, l) : (n.flags = n.flags & -4097 | 2, un = !1, Sa = n);
        }
      } else {
        if (hc(n))
          throw Error(k(418));
        n.flags = n.flags & -4097 | 2, un = !1, Sa = n;
      }
    }
  }
  function kv(n) {
    for (n = n.return; n !== null && n.tag !== 5 && n.tag !== 3 && n.tag !== 13; )
      n = n.return;
    Sa = n;
  }
  function yc(n) {
    if (n !== Sa)
      return !1;
    if (!un)
      return kv(n), un = !0, !1;
    var r;
    if ((r = n.tag !== 3) && !(r = n.tag !== 5) && (r = n.type, r = r !== "head" && r !== "body" && !us(n.type, n.memoizedProps)), r && (r = ta)) {
      if (hc(n))
        throw Dv(), Error(k(418));
      for (; r; )
        yd(n, r), r = li(r.nextSibling);
    }
    if (kv(n), n.tag === 13) {
      if (n = n.memoizedState, n = n !== null ? n.dehydrated : null, !n)
        throw Error(k(317));
      e: {
        for (n = n.nextSibling, r = 0; n; ) {
          if (n.nodeType === 8) {
            var l = n.data;
            if (l === "/$") {
              if (r === 0) {
                ta = li(n.nextSibling);
                break e;
              }
              r--;
            } else
              l !== "$" && l !== "$!" && l !== "$?" || r++;
          }
          n = n.nextSibling;
        }
        ta = null;
      }
    } else
      ta = Sa ? li(n.stateNode.nextSibling) : null;
    return !0;
  }
  function Dv() {
    for (var n = ta; n; )
      n = li(n.nextSibling);
  }
  function gn() {
    ta = Sa = null, un = !1;
  }
  function gd(n) {
    ja === null ? ja = [n] : ja.push(n);
  }
  var gc = mt.ReactCurrentBatchConfig;
  function iu(n, r, l) {
    if (n = l.ref, n !== null && typeof n != "function" && typeof n != "object") {
      if (l._owner) {
        if (l = l._owner, l) {
          if (l.tag !== 1)
            throw Error(k(309));
          var o = l.stateNode;
        }
        if (!o)
          throw Error(k(147, n));
        var c = o, d = "" + n;
        return r !== null && r.ref !== null && typeof r.ref == "function" && r.ref._stringRef === d ? r.ref : (r = function(m) {
          var E = c.refs;
          m === null ? delete E[d] : E[d] = m;
        }, r._stringRef = d, r);
      }
      if (typeof n != "string")
        throw Error(k(284));
      if (!l._owner)
        throw Error(k(290, n));
    }
    return n;
  }
  function Ei(n, r) {
    throw n = Object.prototype.toString.call(r), Error(k(31, n === "[object Object]" ? "object with keys {" + Object.keys(r).join(", ") + "}" : n));
  }
  function Ov(n) {
    var r = n._init;
    return r(n._payload);
  }
  function Sc(n) {
    function r(D, w) {
      if (n) {
        var M = D.deletions;
        M === null ? (D.deletions = [w], D.flags |= 16) : M.push(w);
      }
    }
    function l(D, w) {
      if (!n)
        return null;
      for (; w !== null; )
        r(D, w), w = w.sibling;
      return null;
    }
    function o(D, w) {
      for (D = /* @__PURE__ */ new Map(); w !== null; )
        w.key !== null ? D.set(w.key, w) : D.set(w.index, w), w = w.sibling;
      return D;
    }
    function c(D, w) {
      return D = zl(D, w), D.index = 0, D.sibling = null, D;
    }
    function d(D, w, M) {
      return D.index = M, n ? (M = D.alternate, M !== null ? (M = M.index, M < w ? (D.flags |= 2, w) : M) : (D.flags |= 2, w)) : (D.flags |= 1048576, w);
    }
    function m(D) {
      return n && D.alternate === null && (D.flags |= 2), D;
    }
    function E(D, w, M, Z) {
      return w === null || w.tag !== 6 ? (w = uf(M, D.mode, Z), w.return = D, w) : (w = c(w, M), w.return = D, w);
    }
    function T(D, w, M, Z) {
      var Re = M.type;
      return Re === Ve ? W(D, w, M.props.children, Z, M.key) : w !== null && (w.elementType === Re || typeof Re == "object" && Re !== null && Re.$$typeof === _t && Ov(Re) === w.type) ? (Z = c(w, M.props), Z.ref = iu(D, w, M), Z.return = D, Z) : (Z = af(M.type, M.key, M.props, null, D.mode, Z), Z.ref = iu(D, w, M), Z.return = D, Z);
    }
    function U(D, w, M, Z) {
      return w === null || w.tag !== 4 || w.stateNode.containerInfo !== M.containerInfo || w.stateNode.implementation !== M.implementation ? (w = Ds(M, D.mode, Z), w.return = D, w) : (w = c(w, M.children || []), w.return = D, w);
    }
    function W(D, w, M, Z, Re) {
      return w === null || w.tag !== 7 ? (w = Eu(M, D.mode, Z, Re), w.return = D, w) : (w = c(w, M), w.return = D, w);
    }
    function G(D, w, M) {
      if (typeof w == "string" && w !== "" || typeof w == "number")
        return w = uf("" + w, D.mode, M), w.return = D, w;
      if (typeof w == "object" && w !== null) {
        switch (w.$$typeof) {
          case Oe:
            return M = af(w.type, w.key, w.props, null, D.mode, M), M.ref = iu(D, null, w), M.return = D, M;
          case ft:
            return w = Ds(w, D.mode, M), w.return = D, w;
          case _t:
            var Z = w._init;
            return G(D, Z(w._payload), M);
        }
        if (Gn(w) || be(w))
          return w = Eu(w, D.mode, M, null), w.return = D, w;
        Ei(D, w);
      }
      return null;
    }
    function I(D, w, M, Z) {
      var Re = w !== null ? w.key : null;
      if (typeof M == "string" && M !== "" || typeof M == "number")
        return Re !== null ? null : E(D, w, "" + M, Z);
      if (typeof M == "object" && M !== null) {
        switch (M.$$typeof) {
          case Oe:
            return M.key === Re ? T(D, w, M, Z) : null;
          case ft:
            return M.key === Re ? U(D, w, M, Z) : null;
          case _t:
            return Re = M._init, I(
              D,
              w,
              Re(M._payload),
              Z
            );
        }
        if (Gn(M) || be(M))
          return Re !== null ? null : W(D, w, M, Z, null);
        Ei(D, M);
      }
      return null;
    }
    function ce(D, w, M, Z, Re) {
      if (typeof Z == "string" && Z !== "" || typeof Z == "number")
        return D = D.get(M) || null, E(w, D, "" + Z, Re);
      if (typeof Z == "object" && Z !== null) {
        switch (Z.$$typeof) {
          case Oe:
            return D = D.get(Z.key === null ? M : Z.key) || null, T(w, D, Z, Re);
          case ft:
            return D = D.get(Z.key === null ? M : Z.key) || null, U(w, D, Z, Re);
          case _t:
            var Fe = Z._init;
            return ce(D, w, M, Fe(Z._payload), Re);
        }
        if (Gn(Z) || be(Z))
          return D = D.get(M) || null, W(w, D, Z, Re, null);
        Ei(w, Z);
      }
      return null;
    }
    function ye(D, w, M, Z) {
      for (var Re = null, Fe = null, ge = w, He = w = 0, In = null; ge !== null && He < M.length; He++) {
        ge.index > He ? (In = ge, ge = null) : In = ge.sibling;
        var Nt = I(D, ge, M[He], Z);
        if (Nt === null) {
          ge === null && (ge = In);
          break;
        }
        n && ge && Nt.alternate === null && r(D, ge), w = d(Nt, w, He), Fe === null ? Re = Nt : Fe.sibling = Nt, Fe = Nt, ge = In;
      }
      if (He === M.length)
        return l(D, ge), un && ga(D, He), Re;
      if (ge === null) {
        for (; He < M.length; He++)
          ge = G(D, M[He], Z), ge !== null && (w = d(ge, w, He), Fe === null ? Re = ge : Fe.sibling = ge, Fe = ge);
        return un && ga(D, He), Re;
      }
      for (ge = o(D, ge); He < M.length; He++)
        In = ce(ge, D, He, M[He], Z), In !== null && (n && In.alternate !== null && ge.delete(In.key === null ? He : In.key), w = d(In, w, He), Fe === null ? Re = In : Fe.sibling = In, Fe = In);
      return n && ge.forEach(function(Xi) {
        return r(D, Xi);
      }), un && ga(D, He), Re;
    }
    function Ee(D, w, M, Z) {
      var Re = be(M);
      if (typeof Re != "function")
        throw Error(k(150));
      if (M = Re.call(M), M == null)
        throw Error(k(151));
      for (var Fe = Re = null, ge = w, He = w = 0, In = null, Nt = M.next(); ge !== null && !Nt.done; He++, Nt = M.next()) {
        ge.index > He ? (In = ge, ge = null) : In = ge.sibling;
        var Xi = I(D, ge, Nt.value, Z);
        if (Xi === null) {
          ge === null && (ge = In);
          break;
        }
        n && ge && Xi.alternate === null && r(D, ge), w = d(Xi, w, He), Fe === null ? Re = Xi : Fe.sibling = Xi, Fe = Xi, ge = In;
      }
      if (Nt.done)
        return l(
          D,
          ge
        ), un && ga(D, He), Re;
      if (ge === null) {
        for (; !Nt.done; He++, Nt = M.next())
          Nt = G(D, Nt.value, Z), Nt !== null && (w = d(Nt, w, He), Fe === null ? Re = Nt : Fe.sibling = Nt, Fe = Nt);
        return un && ga(D, He), Re;
      }
      for (ge = o(D, ge); !Nt.done; He++, Nt = M.next())
        Nt = ce(ge, D, He, Nt.value, Z), Nt !== null && (n && Nt.alternate !== null && ge.delete(Nt.key === null ? He : Nt.key), w = d(Nt, w, He), Fe === null ? Re = Nt : Fe.sibling = Nt, Fe = Nt);
      return n && ge.forEach(function(Ry) {
        return r(D, Ry);
      }), un && ga(D, He), Re;
    }
    function Mn(D, w, M, Z) {
      if (typeof M == "object" && M !== null && M.type === Ve && M.key === null && (M = M.props.children), typeof M == "object" && M !== null) {
        switch (M.$$typeof) {
          case Oe:
            e: {
              for (var Re = M.key, Fe = w; Fe !== null; ) {
                if (Fe.key === Re) {
                  if (Re = M.type, Re === Ve) {
                    if (Fe.tag === 7) {
                      l(D, Fe.sibling), w = c(Fe, M.props.children), w.return = D, D = w;
                      break e;
                    }
                  } else if (Fe.elementType === Re || typeof Re == "object" && Re !== null && Re.$$typeof === _t && Ov(Re) === Fe.type) {
                    l(D, Fe.sibling), w = c(Fe, M.props), w.ref = iu(D, Fe, M), w.return = D, D = w;
                    break e;
                  }
                  l(D, Fe);
                  break;
                } else
                  r(D, Fe);
                Fe = Fe.sibling;
              }
              M.type === Ve ? (w = Eu(M.props.children, D.mode, Z, M.key), w.return = D, D = w) : (Z = af(M.type, M.key, M.props, null, D.mode, Z), Z.ref = iu(D, w, M), Z.return = D, D = Z);
            }
            return m(D);
          case ft:
            e: {
              for (Fe = M.key; w !== null; ) {
                if (w.key === Fe)
                  if (w.tag === 4 && w.stateNode.containerInfo === M.containerInfo && w.stateNode.implementation === M.implementation) {
                    l(D, w.sibling), w = c(w, M.children || []), w.return = D, D = w;
                    break e;
                  } else {
                    l(D, w);
                    break;
                  }
                else
                  r(D, w);
                w = w.sibling;
              }
              w = Ds(M, D.mode, Z), w.return = D, D = w;
            }
            return m(D);
          case _t:
            return Fe = M._init, Mn(D, w, Fe(M._payload), Z);
        }
        if (Gn(M))
          return ye(D, w, M, Z);
        if (be(M))
          return Ee(D, w, M, Z);
        Ei(D, M);
      }
      return typeof M == "string" && M !== "" || typeof M == "number" ? (M = "" + M, w !== null && w.tag === 6 ? (l(D, w.sibling), w = c(w, M), w.return = D, D = w) : (l(D, w), w = uf(M, D.mode, Z), w.return = D, D = w), m(D)) : l(D, w);
    }
    return Mn;
  }
  var Ju = Sc(!0), Lv = Sc(!1), Yi = et(null), Pn = null, te = null, Fa = null;
  function Ea() {
    Fa = te = Pn = null;
  }
  function Sd(n) {
    var r = Yi.current;
    jt(Yi), n._currentValue = r;
  }
  function Ed(n, r, l) {
    for (; n !== null; ) {
      var o = n.alternate;
      if ((n.childLanes & r) !== r ? (n.childLanes |= r, o !== null && (o.childLanes |= r)) : o !== null && (o.childLanes & r) !== r && (o.childLanes |= r), n === l)
        break;
      n = n.return;
    }
  }
  function eo(n, r) {
    Pn = n, Fa = te = null, n = n.dependencies, n !== null && n.firstContext !== null && (n.lanes & r && (aa = !0), n.firstContext = null);
  }
  function Ha(n) {
    var r = n._currentValue;
    if (Fa !== n)
      if (n = { context: n, memoizedValue: r, next: null }, te === null) {
        if (Pn === null)
          throw Error(k(308));
        te = n, Pn.dependencies = { lanes: 0, firstContext: n };
      } else
        te = te.next = n;
    return r;
  }
  var lu = null;
  function jn(n) {
    lu === null ? lu = [n] : lu.push(n);
  }
  function Mv(n, r, l, o) {
    var c = r.interleaved;
    return c === null ? (l.next = l, jn(r)) : (l.next = c.next, c.next = l), r.interleaved = l, Ii(n, o);
  }
  function Ii(n, r) {
    n.lanes |= r;
    var l = n.alternate;
    for (l !== null && (l.lanes |= r), l = n, n = n.return; n !== null; )
      n.childLanes |= r, l = n.alternate, l !== null && (l.childLanes |= r), l = n, n = n.return;
    return l.tag === 3 ? l.stateNode : null;
  }
  var _l = !1;
  function Ec(n) {
    n.updateQueue = { baseState: n.memoizedState, firstBaseUpdate: null, lastBaseUpdate: null, shared: { pending: null, interleaved: null, lanes: 0 }, effects: null };
  }
  function to(n, r) {
    n = n.updateQueue, r.updateQueue === n && (r.updateQueue = { baseState: n.baseState, firstBaseUpdate: n.firstBaseUpdate, lastBaseUpdate: n.lastBaseUpdate, shared: n.shared, effects: n.effects });
  }
  function na(n, r) {
    return { eventTime: n, lane: r, tag: 0, payload: null, callback: null, next: null };
  }
  function kl(n, r, l) {
    var o = n.updateQueue;
    if (o === null)
      return null;
    if (o = o.shared, yt & 2) {
      var c = o.pending;
      return c === null ? r.next = r : (r.next = c.next, c.next = r), o.pending = r, Ii(n, l);
    }
    return c = o.interleaved, c === null ? (r.next = r, jn(o)) : (r.next = c.next, c.next = r), o.interleaved = r, Ii(n, l);
  }
  function Cc(n, r, l) {
    if (r = r.updateQueue, r !== null && (r = r.shared, (l & 4194240) !== 0)) {
      var o = r.lanes;
      o &= n.pendingLanes, l |= o, r.lanes = l, mi(n, l);
    }
  }
  function Nv(n, r) {
    var l = n.updateQueue, o = n.alternate;
    if (o !== null && (o = o.updateQueue, l === o)) {
      var c = null, d = null;
      if (l = l.firstBaseUpdate, l !== null) {
        do {
          var m = { eventTime: l.eventTime, lane: l.lane, tag: l.tag, payload: l.payload, callback: l.callback, next: null };
          d === null ? c = d = m : d = d.next = m, l = l.next;
        } while (l !== null);
        d === null ? c = d = r : d = d.next = r;
      } else
        c = d = r;
      l = { baseState: o.baseState, firstBaseUpdate: c, lastBaseUpdate: d, shared: o.shared, effects: o.effects }, n.updateQueue = l;
      return;
    }
    n = l.lastBaseUpdate, n === null ? l.firstBaseUpdate = r : n.next = r, l.lastBaseUpdate = r;
  }
  function Rc(n, r, l, o) {
    var c = n.updateQueue;
    _l = !1;
    var d = c.firstBaseUpdate, m = c.lastBaseUpdate, E = c.shared.pending;
    if (E !== null) {
      c.shared.pending = null;
      var T = E, U = T.next;
      T.next = null, m === null ? d = U : m.next = U, m = T;
      var W = n.alternate;
      W !== null && (W = W.updateQueue, E = W.lastBaseUpdate, E !== m && (E === null ? W.firstBaseUpdate = U : E.next = U, W.lastBaseUpdate = T));
    }
    if (d !== null) {
      var G = c.baseState;
      m = 0, W = U = T = null, E = d;
      do {
        var I = E.lane, ce = E.eventTime;
        if ((o & I) === I) {
          W !== null && (W = W.next = {
            eventTime: ce,
            lane: 0,
            tag: E.tag,
            payload: E.payload,
            callback: E.callback,
            next: null
          });
          e: {
            var ye = n, Ee = E;
            switch (I = r, ce = l, Ee.tag) {
              case 1:
                if (ye = Ee.payload, typeof ye == "function") {
                  G = ye.call(ce, G, I);
                  break e;
                }
                G = ye;
                break e;
              case 3:
                ye.flags = ye.flags & -65537 | 128;
              case 0:
                if (ye = Ee.payload, I = typeof ye == "function" ? ye.call(ce, G, I) : ye, I == null)
                  break e;
                G = ae({}, G, I);
                break e;
              case 2:
                _l = !0;
            }
          }
          E.callback !== null && E.lane !== 0 && (n.flags |= 64, I = c.effects, I === null ? c.effects = [E] : I.push(E));
        } else
          ce = { eventTime: ce, lane: I, tag: E.tag, payload: E.payload, callback: E.callback, next: null }, W === null ? (U = W = ce, T = G) : W = W.next = ce, m |= I;
        if (E = E.next, E === null) {
          if (E = c.shared.pending, E === null)
            break;
          I = E, E = I.next, I.next = null, c.lastBaseUpdate = I, c.shared.pending = null;
        }
      } while (1);
      if (W === null && (T = G), c.baseState = T, c.firstBaseUpdate = U, c.lastBaseUpdate = W, r = c.shared.interleaved, r !== null) {
        c = r;
        do
          m |= c.lane, c = c.next;
        while (c !== r);
      } else
        d === null && (c.shared.lanes = 0);
      mu |= m, n.lanes = m, n.memoizedState = G;
    }
  }
  function zv(n, r, l) {
    if (n = r.effects, r.effects = null, n !== null)
      for (r = 0; r < n.length; r++) {
        var o = n[r], c = o.callback;
        if (c !== null) {
          if (o.callback = null, o = l, typeof c != "function")
            throw Error(k(191, c));
          c.call(o);
        }
      }
  }
  var ds = {}, ui = et(ds), no = et(ds), ps = et(ds);
  function uu(n) {
    if (n === ds)
      throw Error(k(174));
    return n;
  }
  function Cd(n, r) {
    switch ($t(ps, r), $t(no, n), $t(ui, ds), n = r.nodeType, n) {
      case 9:
      case 11:
        r = (r = r.documentElement) ? r.namespaceURI : hn(null, "");
        break;
      default:
        n = n === 8 ? r.parentNode : r, r = n.namespaceURI || null, n = n.tagName, r = hn(r, n);
    }
    jt(ui), $t(ui, r);
  }
  function ro() {
    jt(ui), jt(no), jt(ps);
  }
  function Uv(n) {
    uu(ps.current);
    var r = uu(ui.current), l = hn(r, n.type);
    r !== l && ($t(no, n), $t(ui, l));
  }
  function Rd(n) {
    no.current === n && (jt(ui), jt(no));
  }
  var fn = et(0);
  function Tc(n) {
    for (var r = n; r !== null; ) {
      if (r.tag === 13) {
        var l = r.memoizedState;
        if (l !== null && (l = l.dehydrated, l === null || l.data === "$?" || l.data === "$!"))
          return r;
      } else if (r.tag === 19 && r.memoizedProps.revealOrder !== void 0) {
        if (r.flags & 128)
          return r;
      } else if (r.child !== null) {
        r.child.return = r, r = r.child;
        continue;
      }
      if (r === n)
        break;
      for (; r.sibling === null; ) {
        if (r.return === null || r.return === n)
          return null;
        r = r.return;
      }
      r.sibling.return = r.return, r = r.sibling;
    }
    return null;
  }
  var xc = [];
  function Td() {
    for (var n = 0; n < xc.length; n++)
      xc[n]._workInProgressVersionPrimary = null;
    xc.length = 0;
  }
  var wc = mt.ReactCurrentDispatcher, vs = mt.ReactCurrentBatchConfig, Ce = 0, xe = null, Qe = null, vt = null, Ca = !1, ao = !1, hs = 0, iy = 0;
  function Cr() {
    throw Error(k(321));
  }
  function ms(n, r) {
    if (r === null)
      return !1;
    for (var l = 0; l < r.length && l < n.length; l++)
      if (!Ma(n[l], r[l]))
        return !1;
    return !0;
  }
  function $(n, r, l, o, c, d) {
    if (Ce = d, xe = r, r.memoizedState = null, r.updateQueue = null, r.lanes = 0, wc.current = n === null || n.memoizedState === null ? ly : nn, n = l(o, c), ao) {
      d = 0;
      do {
        if (ao = !1, hs = 0, 25 <= d)
          throw Error(k(301));
        d += 1, vt = Qe = null, r.updateQueue = null, wc.current = Vc, n = l(o, c);
      } while (ao);
    }
    if (wc.current = Rr, r = Qe !== null && Qe.next !== null, Ce = 0, vt = Qe = xe = null, Ca = !1, r)
      throw Error(k(300));
    return n;
  }
  function Fn() {
    var n = hs !== 0;
    return hs = 0, n;
  }
  function ke() {
    var n = { memoizedState: null, baseState: null, baseQueue: null, queue: null, next: null };
    return vt === null ? xe.memoizedState = vt = n : vt = vt.next = n, vt;
  }
  function ir() {
    if (Qe === null) {
      var n = xe.alternate;
      n = n !== null ? n.memoizedState : null;
    } else
      n = Qe.next;
    var r = vt === null ? xe.memoizedState : vt.next;
    if (r !== null)
      vt = r, Qe = n;
    else {
      if (n === null)
        throw Error(k(310));
      Qe = n, n = { memoizedState: Qe.memoizedState, baseState: Qe.baseState, baseQueue: Qe.baseQueue, queue: Qe.queue, next: null }, vt === null ? xe.memoizedState = vt = n : vt = vt.next = n;
    }
    return vt;
  }
  function Ra(n, r) {
    return typeof r == "function" ? r(n) : r;
  }
  function Qi(n) {
    var r = ir(), l = r.queue;
    if (l === null)
      throw Error(k(311));
    l.lastRenderedReducer = n;
    var o = Qe, c = o.baseQueue, d = l.pending;
    if (d !== null) {
      if (c !== null) {
        var m = c.next;
        c.next = d.next, d.next = m;
      }
      o.baseQueue = c = d, l.pending = null;
    }
    if (c !== null) {
      d = c.next, o = o.baseState;
      var E = m = null, T = null, U = d;
      do {
        var W = U.lane;
        if ((Ce & W) === W)
          T !== null && (T = T.next = { lane: 0, action: U.action, hasEagerState: U.hasEagerState, eagerState: U.eagerState, next: null }), o = U.hasEagerState ? U.eagerState : n(o, U.action);
        else {
          var G = {
            lane: W,
            action: U.action,
            hasEagerState: U.hasEagerState,
            eagerState: U.eagerState,
            next: null
          };
          T === null ? (E = T = G, m = o) : T = T.next = G, xe.lanes |= W, mu |= W;
        }
        U = U.next;
      } while (U !== null && U !== d);
      T === null ? m = o : T.next = E, Ma(o, r.memoizedState) || (aa = !0), r.memoizedState = o, r.baseState = m, r.baseQueue = T, l.lastRenderedState = o;
    }
    if (n = l.interleaved, n !== null) {
      c = n;
      do
        d = c.lane, xe.lanes |= d, mu |= d, c = c.next;
      while (c !== n);
    } else
      c === null && (l.lanes = 0);
    return [r.memoizedState, l.dispatch];
  }
  function Va(n) {
    var r = ir(), l = r.queue;
    if (l === null)
      throw Error(k(311));
    l.lastRenderedReducer = n;
    var o = l.dispatch, c = l.pending, d = r.memoizedState;
    if (c !== null) {
      l.pending = null;
      var m = c = c.next;
      do
        d = n(d, m.action), m = m.next;
      while (m !== c);
      Ma(d, r.memoizedState) || (aa = !0), r.memoizedState = d, r.baseQueue === null && (r.baseState = d), l.lastRenderedState = d;
    }
    return [d, o];
  }
  function io() {
  }
  function ou(n, r) {
    var l = xe, o = ir(), c = r(), d = !Ma(o.memoizedState, c);
    if (d && (o.memoizedState = c, aa = !0), o = o.queue, ys(_c.bind(null, l, o, n), [n]), o.getSnapshot !== r || d || vt !== null && vt.memoizedState.tag & 1) {
      if (l.flags |= 2048, su(9, bc.bind(null, l, o, c, r), void 0, null), wn === null)
        throw Error(k(349));
      Ce & 30 || lo(l, r, c);
    }
    return c;
  }
  function lo(n, r, l) {
    n.flags |= 16384, n = { getSnapshot: r, value: l }, r = xe.updateQueue, r === null ? (r = { lastEffect: null, stores: null }, xe.updateQueue = r, r.stores = [n]) : (l = r.stores, l === null ? r.stores = [n] : l.push(n));
  }
  function bc(n, r, l, o) {
    r.value = l, r.getSnapshot = o, kc(r) && Dc(n);
  }
  function _c(n, r, l) {
    return l(function() {
      kc(r) && Dc(n);
    });
  }
  function kc(n) {
    var r = n.getSnapshot;
    n = n.value;
    try {
      var l = r();
      return !Ma(n, l);
    } catch {
      return !0;
    }
  }
  function Dc(n) {
    var r = Ii(n, 1);
    r !== null && Sn(r, n, 1, -1);
  }
  function Oc(n) {
    var r = ke();
    return typeof n == "function" && (n = n()), r.memoizedState = r.baseState = n, n = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: Ra, lastRenderedState: n }, r.queue = n, n = n.dispatch = gs.bind(null, xe, n), [r.memoizedState, n];
  }
  function su(n, r, l, o) {
    return n = { tag: n, create: r, destroy: l, deps: o, next: null }, r = xe.updateQueue, r === null ? (r = { lastEffect: null, stores: null }, xe.updateQueue = r, r.lastEffect = n.next = n) : (l = r.lastEffect, l === null ? r.lastEffect = n.next = n : (o = l.next, l.next = n, n.next = o, r.lastEffect = n)), n;
  }
  function Lc() {
    return ir().memoizedState;
  }
  function uo(n, r, l, o) {
    var c = ke();
    xe.flags |= n, c.memoizedState = su(1 | r, l, void 0, o === void 0 ? null : o);
  }
  function oo(n, r, l, o) {
    var c = ir();
    o = o === void 0 ? null : o;
    var d = void 0;
    if (Qe !== null) {
      var m = Qe.memoizedState;
      if (d = m.destroy, o !== null && ms(o, m.deps)) {
        c.memoizedState = su(r, l, d, o);
        return;
      }
    }
    xe.flags |= n, c.memoizedState = su(1 | r, l, d, o);
  }
  function Mc(n, r) {
    return uo(8390656, 8, n, r);
  }
  function ys(n, r) {
    return oo(2048, 8, n, r);
  }
  function Nc(n, r) {
    return oo(4, 2, n, r);
  }
  function zc(n, r) {
    return oo(4, 4, n, r);
  }
  function Uc(n, r) {
    if (typeof r == "function")
      return n = n(), r(n), function() {
        r(null);
      };
    if (r != null)
      return n = n(), r.current = n, function() {
        r.current = null;
      };
  }
  function Ac(n, r, l) {
    return l = l != null ? l.concat([n]) : null, oo(4, 4, Uc.bind(null, r, n), l);
  }
  function so() {
  }
  function cu(n, r) {
    var l = ir();
    r = r === void 0 ? null : r;
    var o = l.memoizedState;
    return o !== null && r !== null && ms(r, o[1]) ? o[0] : (l.memoizedState = [n, r], n);
  }
  function jc(n, r) {
    var l = ir();
    r = r === void 0 ? null : r;
    var o = l.memoizedState;
    return o !== null && r !== null && ms(r, o[1]) ? o[0] : (n = n(), l.memoizedState = [n, r], n);
  }
  function Fc(n, r, l) {
    return Ce & 21 ? (Ma(l, r) || (l = Au(), xe.lanes |= l, mu |= l, n.baseState = !0), r) : (n.baseState && (n.baseState = !1, aa = !0), n.memoizedState = l);
  }
  function xd(n, r) {
    var l = Mt;
    Mt = l !== 0 && 4 > l ? l : 4, n(!0);
    var o = vs.transition;
    vs.transition = {};
    try {
      n(!1), r();
    } finally {
      Mt = l, vs.transition = o;
    }
  }
  function Hc() {
    return ir().memoizedState;
  }
  function Av(n, r, l) {
    var o = qi(n);
    if (l = { lane: o, action: l, hasEagerState: !1, eagerState: null, next: null }, wd(n))
      co(r, l);
    else if (l = Mv(n, r, l, o), l !== null) {
      var c = tr();
      Sn(l, n, o, c), Dl(l, r, o);
    }
  }
  function gs(n, r, l) {
    var o = qi(n), c = { lane: o, action: l, hasEagerState: !1, eagerState: null, next: null };
    if (wd(n))
      co(r, c);
    else {
      var d = n.alternate;
      if (n.lanes === 0 && (d === null || d.lanes === 0) && (d = r.lastRenderedReducer, d !== null))
        try {
          var m = r.lastRenderedState, E = d(m, l);
          if (c.hasEagerState = !0, c.eagerState = E, Ma(E, m)) {
            var T = r.interleaved;
            T === null ? (c.next = c, jn(r)) : (c.next = T.next, T.next = c), r.interleaved = c;
            return;
          }
        } catch {
        } finally {
        }
      l = Mv(n, r, c, o), l !== null && (c = tr(), Sn(l, n, o, c), Dl(l, r, o));
    }
  }
  function wd(n) {
    var r = n.alternate;
    return n === xe || r !== null && r === xe;
  }
  function co(n, r) {
    ao = Ca = !0;
    var l = n.pending;
    l === null ? r.next = r : (r.next = l.next, l.next = r), n.pending = r;
  }
  function Dl(n, r, l) {
    if (l & 4194240) {
      var o = r.lanes;
      o &= n.pendingLanes, l |= o, r.lanes = l, mi(n, l);
    }
  }
  var Rr = { readContext: Ha, useCallback: Cr, useContext: Cr, useEffect: Cr, useImperativeHandle: Cr, useInsertionEffect: Cr, useLayoutEffect: Cr, useMemo: Cr, useReducer: Cr, useRef: Cr, useState: Cr, useDebugValue: Cr, useDeferredValue: Cr, useTransition: Cr, useMutableSource: Cr, useSyncExternalStore: Cr, useId: Cr, unstable_isNewReconciler: !1 }, ly = { readContext: Ha, useCallback: function(n, r) {
    return ke().memoizedState = [n, r === void 0 ? null : r], n;
  }, useContext: Ha, useEffect: Mc, useImperativeHandle: function(n, r, l) {
    return l = l != null ? l.concat([n]) : null, uo(
      4194308,
      4,
      Uc.bind(null, r, n),
      l
    );
  }, useLayoutEffect: function(n, r) {
    return uo(4194308, 4, n, r);
  }, useInsertionEffect: function(n, r) {
    return uo(4, 2, n, r);
  }, useMemo: function(n, r) {
    var l = ke();
    return r = r === void 0 ? null : r, n = n(), l.memoizedState = [n, r], n;
  }, useReducer: function(n, r, l) {
    var o = ke();
    return r = l !== void 0 ? l(r) : r, o.memoizedState = o.baseState = r, n = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: n, lastRenderedState: r }, o.queue = n, n = n.dispatch = Av.bind(null, xe, n), [o.memoizedState, n];
  }, useRef: function(n) {
    var r = ke();
    return n = { current: n }, r.memoizedState = n;
  }, useState: Oc, useDebugValue: so, useDeferredValue: function(n) {
    return ke().memoizedState = n;
  }, useTransition: function() {
    var n = Oc(!1), r = n[0];
    return n = xd.bind(null, n[1]), ke().memoizedState = n, [r, n];
  }, useMutableSource: function() {
  }, useSyncExternalStore: function(n, r, l) {
    var o = xe, c = ke();
    if (un) {
      if (l === void 0)
        throw Error(k(407));
      l = l();
    } else {
      if (l = r(), wn === null)
        throw Error(k(349));
      Ce & 30 || lo(o, r, l);
    }
    c.memoizedState = l;
    var d = { value: l, getSnapshot: r };
    return c.queue = d, Mc(_c.bind(
      null,
      o,
      d,
      n
    ), [n]), o.flags |= 2048, su(9, bc.bind(null, o, d, l, r), void 0, null), l;
  }, useId: function() {
    var n = ke(), r = wn.identifierPrefix;
    if (un) {
      var l = $i, o = ar;
      l = (o & ~(1 << 32 - Dr(o) - 1)).toString(32) + l, r = ":" + r + "R" + l, l = hs++, 0 < l && (r += "H" + l.toString(32)), r += ":";
    } else
      l = iy++, r = ":" + r + "r" + l.toString(32) + ":";
    return n.memoizedState = r;
  }, unstable_isNewReconciler: !1 }, nn = {
    readContext: Ha,
    useCallback: cu,
    useContext: Ha,
    useEffect: ys,
    useImperativeHandle: Ac,
    useInsertionEffect: Nc,
    useLayoutEffect: zc,
    useMemo: jc,
    useReducer: Qi,
    useRef: Lc,
    useState: function() {
      return Qi(Ra);
    },
    useDebugValue: so,
    useDeferredValue: function(n) {
      var r = ir();
      return Fc(r, Qe.memoizedState, n);
    },
    useTransition: function() {
      var n = Qi(Ra)[0], r = ir().memoizedState;
      return [n, r];
    },
    useMutableSource: io,
    useSyncExternalStore: ou,
    useId: Hc,
    unstable_isNewReconciler: !1
  }, Vc = { readContext: Ha, useCallback: cu, useContext: Ha, useEffect: ys, useImperativeHandle: Ac, useInsertionEffect: Nc, useLayoutEffect: zc, useMemo: jc, useReducer: Va, useRef: Lc, useState: function() {
    return Va(Ra);
  }, useDebugValue: so, useDeferredValue: function(n) {
    var r = ir();
    return Qe === null ? r.memoizedState = n : Fc(r, Qe.memoizedState, n);
  }, useTransition: function() {
    var n = Va(Ra)[0], r = ir().memoizedState;
    return [n, r];
  }, useMutableSource: io, useSyncExternalStore: ou, useId: Hc, unstable_isNewReconciler: !1 };
  function ra(n, r) {
    if (n && n.defaultProps) {
      r = ae({}, r), n = n.defaultProps;
      for (var l in n)
        r[l] === void 0 && (r[l] = n[l]);
      return r;
    }
    return r;
  }
  function fu(n, r, l, o) {
    r = n.memoizedState, l = l(o, r), l = l == null ? r : ae({}, r, l), n.memoizedState = l, n.lanes === 0 && (n.updateQueue.baseState = l);
  }
  var du = { isMounted: function(n) {
    return (n = n._reactInternals) ? Te(n) === n : !1;
  }, enqueueSetState: function(n, r, l) {
    n = n._reactInternals;
    var o = tr(), c = qi(n), d = na(o, c);
    d.payload = r, l != null && (d.callback = l), r = kl(n, d, c), r !== null && (Sn(r, n, c, o), Cc(r, n, c));
  }, enqueueReplaceState: function(n, r, l) {
    n = n._reactInternals;
    var o = tr(), c = qi(n), d = na(o, c);
    d.tag = 1, d.payload = r, l != null && (d.callback = l), r = kl(n, d, c), r !== null && (Sn(r, n, c, o), Cc(r, n, c));
  }, enqueueForceUpdate: function(n, r) {
    n = n._reactInternals;
    var l = tr(), o = qi(n), c = na(l, o);
    c.tag = 2, r != null && (c.callback = r), r = kl(n, c, o), r !== null && (Sn(r, n, o, l), Cc(r, n, o));
  } };
  function jv(n, r, l, o, c, d, m) {
    return n = n.stateNode, typeof n.shouldComponentUpdate == "function" ? n.shouldComponentUpdate(o, d, m) : r.prototype && r.prototype.isPureReactComponent ? !es(l, o) || !es(c, d) : !0;
  }
  function Fv(n, r, l) {
    var o = !1, c = Si, d = r.contextType;
    return typeof d == "object" && d !== null ? d = Ha(d) : (c = cn(r) ? Kr : Ie.current, o = r.contextTypes, d = (o = o != null) ? za(n, c) : Si), r = new r(l, d), n.memoizedState = r.state !== null && r.state !== void 0 ? r.state : null, r.updater = du, n.stateNode = r, r._reactInternals = n, o && (n = n.stateNode, n.__reactInternalMemoizedUnmaskedChildContext = c, n.__reactInternalMemoizedMaskedChildContext = d), r;
  }
  function Hv(n, r, l, o) {
    n = r.state, typeof r.componentWillReceiveProps == "function" && r.componentWillReceiveProps(l, o), typeof r.UNSAFE_componentWillReceiveProps == "function" && r.UNSAFE_componentWillReceiveProps(l, o), r.state !== n && du.enqueueReplaceState(r, r.state, null);
  }
  function bd(n, r, l, o) {
    var c = n.stateNode;
    c.props = l, c.state = n.memoizedState, c.refs = {}, Ec(n);
    var d = r.contextType;
    typeof d == "object" && d !== null ? c.context = Ha(d) : (d = cn(r) ? Kr : Ie.current, c.context = za(n, d)), c.state = n.memoizedState, d = r.getDerivedStateFromProps, typeof d == "function" && (fu(n, r, d, l), c.state = n.memoizedState), typeof r.getDerivedStateFromProps == "function" || typeof c.getSnapshotBeforeUpdate == "function" || typeof c.UNSAFE_componentWillMount != "function" && typeof c.componentWillMount != "function" || (r = c.state, typeof c.componentWillMount == "function" && c.componentWillMount(), typeof c.UNSAFE_componentWillMount == "function" && c.UNSAFE_componentWillMount(), r !== c.state && du.enqueueReplaceState(c, c.state, null), Rc(n, l, c, o), c.state = n.memoizedState), typeof c.componentDidMount == "function" && (n.flags |= 4194308);
  }
  function Ol(n, r) {
    try {
      var l = "", o = r;
      do
        l += rt(o), o = o.return;
      while (o);
      var c = l;
    } catch (d) {
      c = `
Error generating stack: ` + d.message + `
` + d.stack;
    }
    return { value: n, source: r, stack: c, digest: null };
  }
  function _d(n, r, l) {
    return { value: n, source: null, stack: l ?? null, digest: r ?? null };
  }
  function Ss(n, r) {
    try {
      console.error(r.value);
    } catch (l) {
      setTimeout(function() {
        throw l;
      });
    }
  }
  var Vv = typeof WeakMap == "function" ? WeakMap : Map;
  function Pv(n, r, l) {
    l = na(-1, l), l.tag = 3, l.payload = { element: null };
    var o = r.value;
    return l.callback = function() {
      Zc || (Zc = !0, Ad = o), Ss(n, r);
    }, l;
  }
  function Bv(n, r, l) {
    l = na(-1, l), l.tag = 3;
    var o = n.type.getDerivedStateFromError;
    if (typeof o == "function") {
      var c = r.value;
      l.payload = function() {
        return o(c);
      }, l.callback = function() {
        Ss(n, r);
      };
    }
    var d = n.stateNode;
    return d !== null && typeof d.componentDidCatch == "function" && (l.callback = function() {
      Ss(n, r), typeof o != "function" && ($a === null ? $a = /* @__PURE__ */ new Set([this]) : $a.add(this));
      var m = r.stack;
      this.componentDidCatch(r.value, { componentStack: m !== null ? m : "" });
    }), l;
  }
  function Es(n, r, l) {
    var o = n.pingCache;
    if (o === null) {
      o = n.pingCache = new Vv();
      var c = /* @__PURE__ */ new Set();
      o.set(r, c);
    } else
      c = o.get(r), c === void 0 && (c = /* @__PURE__ */ new Set(), o.set(r, c));
    c.has(l) || (c.add(l), n = my.bind(null, n, r, l), r.then(n, n));
  }
  function $v(n) {
    do {
      var r;
      if ((r = n.tag === 13) && (r = n.memoizedState, r = r !== null ? r.dehydrated !== null : !0), r)
        return n;
      n = n.return;
    } while (n !== null);
    return null;
  }
  function kd(n, r, l, o, c) {
    return n.mode & 1 ? (n.flags |= 65536, n.lanes = c, n) : (n === r ? n.flags |= 65536 : (n.flags |= 128, l.flags |= 131072, l.flags &= -52805, l.tag === 1 && (l.alternate === null ? l.tag = 17 : (r = na(-1, 1), r.tag = 2, kl(l, r, 1))), l.lanes |= 1), n);
  }
  var Yv = mt.ReactCurrentOwner, aa = !1;
  function On(n, r, l, o) {
    r.child = n === null ? Lv(r, null, l, o) : Ju(r, n.child, l, o);
  }
  function fo(n, r, l, o, c) {
    l = l.render;
    var d = r.ref;
    return eo(r, c), o = $(n, r, l, o, d, c), l = Fn(), n !== null && !aa ? (r.updateQueue = n.updateQueue, r.flags &= -2053, n.lanes &= ~c, Ln(n, r, c)) : (un && l && vc(r), r.flags |= 1, On(n, r, o, c), r.child);
  }
  function Ll(n, r, l, o, c) {
    if (n === null) {
      var d = l.type;
      return typeof d == "function" && !Pd(d) && d.defaultProps === void 0 && l.compare === null && l.defaultProps === void 0 ? (r.tag = 15, r.type = d, Pc(n, r, d, o, c)) : (n = af(l.type, null, o, r, r.mode, c), n.ref = r.ref, n.return = r, r.child = n);
    }
    if (d = n.child, !(n.lanes & c)) {
      var m = d.memoizedProps;
      if (l = l.compare, l = l !== null ? l : es, l(m, o) && n.ref === r.ref)
        return Ln(n, r, c);
    }
    return r.flags |= 1, n = zl(d, o), n.ref = r.ref, n.return = r, r.child = n;
  }
  function Pc(n, r, l, o, c) {
    if (n !== null) {
      var d = n.memoizedProps;
      if (es(d, o) && n.ref === r.ref)
        if (aa = !1, r.pendingProps = o = d, (n.lanes & c) !== 0)
          n.flags & 131072 && (aa = !0);
        else
          return r.lanes = n.lanes, Ln(n, r, c);
    }
    return Ke(n, r, l, o, c);
  }
  function ia(n, r, l) {
    var o = r.pendingProps, c = o.children, d = n !== null ? n.memoizedState : null;
    if (o.mode === "hidden")
      if (!(r.mode & 1))
        r.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, $t(Ro, la), la |= l;
      else {
        if (!(l & 1073741824))
          return n = d !== null ? d.baseLanes | l : l, r.lanes = r.childLanes = 1073741824, r.memoizedState = { baseLanes: n, cachePool: null, transitions: null }, r.updateQueue = null, $t(Ro, la), la |= n, null;
        r.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, o = d !== null ? d.baseLanes : l, $t(Ro, la), la |= o;
      }
    else
      d !== null ? (o = d.baseLanes | l, r.memoizedState = null) : o = l, $t(Ro, la), la |= o;
    return On(n, r, c, l), r.child;
  }
  function pu(n, r) {
    var l = r.ref;
    (n === null && l !== null || n !== null && n.ref !== l) && (r.flags |= 512, r.flags |= 2097152);
  }
  function Ke(n, r, l, o, c) {
    var d = cn(l) ? Kr : Ie.current;
    return d = za(r, d), eo(r, c), l = $(n, r, l, o, d, c), o = Fn(), n !== null && !aa ? (r.updateQueue = n.updateQueue, r.flags &= -2053, n.lanes &= ~c, Ln(n, r, c)) : (un && o && vc(r), r.flags |= 1, On(n, r, l, c), r.child);
  }
  function Cs(n, r, l, o, c) {
    if (cn(l)) {
      var d = !0;
      pc(r);
    } else
      d = !1;
    if (eo(r, c), r.stateNode === null)
      Ts(n, r), Fv(r, l, o), bd(r, l, o, c), o = !0;
    else if (n === null) {
      var m = r.stateNode, E = r.memoizedProps;
      m.props = E;
      var T = m.context, U = l.contextType;
      typeof U == "object" && U !== null ? U = Ha(U) : (U = cn(l) ? Kr : Ie.current, U = za(r, U));
      var W = l.getDerivedStateFromProps, G = typeof W == "function" || typeof m.getSnapshotBeforeUpdate == "function";
      G || typeof m.UNSAFE_componentWillReceiveProps != "function" && typeof m.componentWillReceiveProps != "function" || (E !== o || T !== U) && Hv(r, m, o, U), _l = !1;
      var I = r.memoizedState;
      m.state = I, Rc(r, o, m, c), T = r.memoizedState, E !== o || I !== T || Tn.current || _l ? (typeof W == "function" && (fu(r, l, W, o), T = r.memoizedState), (E = _l || jv(r, l, E, o, I, T, U)) ? (G || typeof m.UNSAFE_componentWillMount != "function" && typeof m.componentWillMount != "function" || (typeof m.componentWillMount == "function" && m.componentWillMount(), typeof m.UNSAFE_componentWillMount == "function" && m.UNSAFE_componentWillMount()), typeof m.componentDidMount == "function" && (r.flags |= 4194308)) : (typeof m.componentDidMount == "function" && (r.flags |= 4194308), r.memoizedProps = o, r.memoizedState = T), m.props = o, m.state = T, m.context = U, o = E) : (typeof m.componentDidMount == "function" && (r.flags |= 4194308), o = !1);
    } else {
      m = r.stateNode, to(n, r), E = r.memoizedProps, U = r.type === r.elementType ? E : ra(r.type, E), m.props = U, G = r.pendingProps, I = m.context, T = l.contextType, typeof T == "object" && T !== null ? T = Ha(T) : (T = cn(l) ? Kr : Ie.current, T = za(r, T));
      var ce = l.getDerivedStateFromProps;
      (W = typeof ce == "function" || typeof m.getSnapshotBeforeUpdate == "function") || typeof m.UNSAFE_componentWillReceiveProps != "function" && typeof m.componentWillReceiveProps != "function" || (E !== G || I !== T) && Hv(r, m, o, T), _l = !1, I = r.memoizedState, m.state = I, Rc(r, o, m, c);
      var ye = r.memoizedState;
      E !== G || I !== ye || Tn.current || _l ? (typeof ce == "function" && (fu(r, l, ce, o), ye = r.memoizedState), (U = _l || jv(r, l, U, o, I, ye, T) || !1) ? (W || typeof m.UNSAFE_componentWillUpdate != "function" && typeof m.componentWillUpdate != "function" || (typeof m.componentWillUpdate == "function" && m.componentWillUpdate(o, ye, T), typeof m.UNSAFE_componentWillUpdate == "function" && m.UNSAFE_componentWillUpdate(o, ye, T)), typeof m.componentDidUpdate == "function" && (r.flags |= 4), typeof m.getSnapshotBeforeUpdate == "function" && (r.flags |= 1024)) : (typeof m.componentDidUpdate != "function" || E === n.memoizedProps && I === n.memoizedState || (r.flags |= 4), typeof m.getSnapshotBeforeUpdate != "function" || E === n.memoizedProps && I === n.memoizedState || (r.flags |= 1024), r.memoizedProps = o, r.memoizedState = ye), m.props = o, m.state = ye, m.context = T, o = U) : (typeof m.componentDidUpdate != "function" || E === n.memoizedProps && I === n.memoizedState || (r.flags |= 4), typeof m.getSnapshotBeforeUpdate != "function" || E === n.memoizedProps && I === n.memoizedState || (r.flags |= 1024), o = !1);
    }
    return Bc(n, r, l, o, d, c);
  }
  function Bc(n, r, l, o, c, d) {
    pu(n, r);
    var m = (r.flags & 128) !== 0;
    if (!o && !m)
      return c && bv(r, l, !1), Ln(n, r, d);
    o = r.stateNode, Yv.current = r;
    var E = m && typeof l.getDerivedStateFromError != "function" ? null : o.render();
    return r.flags |= 1, n !== null && m ? (r.child = Ju(r, n.child, null, d), r.child = Ju(r, null, E, d)) : On(n, r, E, d), r.memoizedState = o.state, c && bv(r, l, !0), r.child;
  }
  function uy(n) {
    var r = n.stateNode;
    r.pendingContext ? wl(n, r.pendingContext, r.pendingContext !== r.context) : r.context && wl(n, r.context, !1), Cd(n, r.containerInfo);
  }
  function Iv(n, r, l, o, c) {
    return gn(), gd(c), r.flags |= 256, On(n, r, l, o), r.child;
  }
  var Rs = { dehydrated: null, treeContext: null, retryLane: 0 };
  function vu(n) {
    return { baseLanes: n, cachePool: null, transitions: null };
  }
  function Qv(n, r, l) {
    var o = r.pendingProps, c = fn.current, d = !1, m = (r.flags & 128) !== 0, E;
    if ((E = m) || (E = n !== null && n.memoizedState === null ? !1 : (c & 2) !== 0), E ? (d = !0, r.flags &= -129) : (n === null || n.memoizedState !== null) && (c |= 1), $t(fn, c & 1), n === null)
      return mc(r), n = r.memoizedState, n !== null && (n = n.dehydrated, n !== null) ? (r.mode & 1 ? n.data === "$!" ? r.lanes = 8 : r.lanes = 1073741824 : r.lanes = 1, null) : (m = o.children, n = o.fallback, d ? (o = r.mode, d = r.child, m = { mode: "hidden", children: m }, !(o & 1) && d !== null ? (d.childLanes = 0, d.pendingProps = m) : d = lf(m, o, 0, null), n = Eu(n, o, l, null), d.return = r, n.return = r, d.sibling = n, r.child = d, r.child.memoizedState = vu(l), r.memoizedState = Rs, n) : $c(r, m));
    if (c = n.memoizedState, c !== null && (E = c.dehydrated, E !== null))
      return Dd(n, r, m, o, E, c, l);
    if (d) {
      d = o.fallback, m = r.mode, c = n.child, E = c.sibling;
      var T = { mode: "hidden", children: o.children };
      return !(m & 1) && r.child !== c ? (o = r.child, o.childLanes = 0, o.pendingProps = T, r.deletions = null) : (o = zl(c, T), o.subtreeFlags = c.subtreeFlags & 14680064), E !== null ? d = zl(E, d) : (d = Eu(d, m, l, null), d.flags |= 2), d.return = r, o.return = r, o.sibling = d, r.child = o, o = d, d = r.child, m = n.child.memoizedState, m = m === null ? vu(l) : { baseLanes: m.baseLanes | l, cachePool: null, transitions: m.transitions }, d.memoizedState = m, d.childLanes = n.childLanes & ~l, r.memoizedState = Rs, o;
    }
    return d = n.child, n = d.sibling, o = zl(d, { mode: "visible", children: o.children }), !(r.mode & 1) && (o.lanes = l), o.return = r, o.sibling = null, n !== null && (l = r.deletions, l === null ? (r.deletions = [n], r.flags |= 16) : l.push(n)), r.child = o, r.memoizedState = null, o;
  }
  function $c(n, r) {
    return r = lf({ mode: "visible", children: r }, n.mode, 0, null), r.return = n, n.child = r;
  }
  function Yc(n, r, l, o) {
    return o !== null && gd(o), Ju(r, n.child, null, l), n = $c(r, r.pendingProps.children), n.flags |= 2, r.memoizedState = null, n;
  }
  function Dd(n, r, l, o, c, d, m) {
    if (l)
      return r.flags & 256 ? (r.flags &= -257, o = _d(Error(k(422))), Yc(n, r, m, o)) : r.memoizedState !== null ? (r.child = n.child, r.flags |= 128, null) : (d = o.fallback, c = r.mode, o = lf({ mode: "visible", children: o.children }, c, 0, null), d = Eu(d, c, m, null), d.flags |= 2, o.return = r, d.return = r, o.sibling = d, r.child = o, r.mode & 1 && Ju(r, n.child, null, m), r.child.memoizedState = vu(m), r.memoizedState = Rs, d);
    if (!(r.mode & 1))
      return Yc(n, r, m, null);
    if (c.data === "$!") {
      if (o = c.nextSibling && c.nextSibling.dataset, o)
        var E = o.dgst;
      return o = E, d = Error(k(419)), o = _d(d, o, void 0), Yc(n, r, m, o);
    }
    if (E = (m & n.childLanes) !== 0, aa || E) {
      if (o = wn, o !== null) {
        switch (m & -m) {
          case 4:
            c = 2;
            break;
          case 16:
            c = 8;
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
            c = 32;
            break;
          case 536870912:
            c = 268435456;
            break;
          default:
            c = 0;
        }
        c = c & (o.suspendedLanes | m) ? 0 : c, c !== 0 && c !== d.retryLane && (d.retryLane = c, Ii(n, c), Sn(o, n, c, -1));
      }
      return ks(), o = _d(Error(k(421))), Yc(n, r, m, o);
    }
    return c.data === "$?" ? (r.flags |= 128, r.child = n.child, r = Vd.bind(null, n), c._reactRetry = r, null) : (n = d.treeContext, ta = li(c.nextSibling), Sa = r, un = !0, ja = null, n !== null && (ea[Er++] = ar, ea[Er++] = $i, ea[Er++] = Aa, ar = n.id, $i = n.overflow, Aa = r), r = $c(r, o.children), r.flags |= 4096, r);
  }
  function Wv(n, r, l) {
    n.lanes |= r;
    var o = n.alternate;
    o !== null && (o.lanes |= r), Ed(n.return, r, l);
  }
  function Ic(n, r, l, o, c) {
    var d = n.memoizedState;
    d === null ? n.memoizedState = { isBackwards: r, rendering: null, renderingStartTime: 0, last: o, tail: l, tailMode: c } : (d.isBackwards = r, d.rendering = null, d.renderingStartTime = 0, d.last = o, d.tail = l, d.tailMode = c);
  }
  function Od(n, r, l) {
    var o = r.pendingProps, c = o.revealOrder, d = o.tail;
    if (On(n, r, o.children, l), o = fn.current, o & 2)
      o = o & 1 | 2, r.flags |= 128;
    else {
      if (n !== null && n.flags & 128)
        e:
          for (n = r.child; n !== null; ) {
            if (n.tag === 13)
              n.memoizedState !== null && Wv(n, l, r);
            else if (n.tag === 19)
              Wv(n, l, r);
            else if (n.child !== null) {
              n.child.return = n, n = n.child;
              continue;
            }
            if (n === r)
              break e;
            for (; n.sibling === null; ) {
              if (n.return === null || n.return === r)
                break e;
              n = n.return;
            }
            n.sibling.return = n.return, n = n.sibling;
          }
      o &= 1;
    }
    if ($t(fn, o), !(r.mode & 1))
      r.memoizedState = null;
    else
      switch (c) {
        case "forwards":
          for (l = r.child, c = null; l !== null; )
            n = l.alternate, n !== null && Tc(n) === null && (c = l), l = l.sibling;
          l = c, l === null ? (c = r.child, r.child = null) : (c = l.sibling, l.sibling = null), Ic(r, !1, c, l, d);
          break;
        case "backwards":
          for (l = null, c = r.child, r.child = null; c !== null; ) {
            if (n = c.alternate, n !== null && Tc(n) === null) {
              r.child = c;
              break;
            }
            n = c.sibling, c.sibling = l, l = c, c = n;
          }
          Ic(r, !0, l, null, d);
          break;
        case "together":
          Ic(r, !1, null, null, void 0);
          break;
        default:
          r.memoizedState = null;
      }
    return r.child;
  }
  function Ts(n, r) {
    !(r.mode & 1) && n !== null && (n.alternate = null, r.alternate = null, r.flags |= 2);
  }
  function Ln(n, r, l) {
    if (n !== null && (r.dependencies = n.dependencies), mu |= r.lanes, !(l & r.childLanes))
      return null;
    if (n !== null && r.child !== n.child)
      throw Error(k(153));
    if (r.child !== null) {
      for (n = r.child, l = zl(n, n.pendingProps), r.child = l, l.return = r; n.sibling !== null; )
        n = n.sibling, l = l.sibling = zl(n, n.pendingProps), l.return = r;
      l.sibling = null;
    }
    return r.child;
  }
  function Wi(n, r, l) {
    switch (r.tag) {
      case 3:
        uy(r), gn();
        break;
      case 5:
        Uv(r);
        break;
      case 1:
        cn(r.type) && pc(r);
        break;
      case 4:
        Cd(r, r.stateNode.containerInfo);
        break;
      case 10:
        var o = r.type._context, c = r.memoizedProps.value;
        $t(Yi, o._currentValue), o._currentValue = c;
        break;
      case 13:
        if (o = r.memoizedState, o !== null)
          return o.dehydrated !== null ? ($t(fn, fn.current & 1), r.flags |= 128, null) : l & r.child.childLanes ? Qv(n, r, l) : ($t(fn, fn.current & 1), n = Ln(n, r, l), n !== null ? n.sibling : null);
        $t(fn, fn.current & 1);
        break;
      case 19:
        if (o = (l & r.childLanes) !== 0, n.flags & 128) {
          if (o)
            return Od(n, r, l);
          r.flags |= 128;
        }
        if (c = r.memoizedState, c !== null && (c.rendering = null, c.tail = null, c.lastEffect = null), $t(fn, fn.current), o)
          break;
        return null;
      case 22:
      case 23:
        return r.lanes = 0, ia(n, r, l);
    }
    return Ln(n, r, l);
  }
  var Ci, po, vo, Pa;
  Ci = function(n, r) {
    for (var l = r.child; l !== null; ) {
      if (l.tag === 5 || l.tag === 6)
        n.appendChild(l.stateNode);
      else if (l.tag !== 4 && l.child !== null) {
        l.child.return = l, l = l.child;
        continue;
      }
      if (l === r)
        break;
      for (; l.sibling === null; ) {
        if (l.return === null || l.return === r)
          return;
        l = l.return;
      }
      l.sibling.return = l.return, l = l.sibling;
    }
  }, po = function() {
  }, vo = function(n, r, l, o) {
    var c = n.memoizedProps;
    if (c !== o) {
      n = r.stateNode, uu(ui.current);
      var d = null;
      switch (l) {
        case "input":
          c = Wn(n, c), o = Wn(n, o), d = [];
          break;
        case "select":
          c = ae({}, c, { value: void 0 }), o = ae({}, o, { value: void 0 }), d = [];
          break;
        case "textarea":
          c = Ir(n, c), o = Ir(n, o), d = [];
          break;
        default:
          typeof c.onClick != "function" && typeof o.onClick == "function" && (n.onclick = dc);
      }
      Dn(l, o);
      var m;
      l = null;
      for (U in c)
        if (!o.hasOwnProperty(U) && c.hasOwnProperty(U) && c[U] != null)
          if (U === "style") {
            var E = c[U];
            for (m in E)
              E.hasOwnProperty(m) && (l || (l = {}), l[m] = "");
          } else
            U !== "dangerouslySetInnerHTML" && U !== "children" && U !== "suppressContentEditableWarning" && U !== "suppressHydrationWarning" && U !== "autoFocus" && (Dt.hasOwnProperty(U) ? d || (d = []) : (d = d || []).push(U, null));
      for (U in o) {
        var T = o[U];
        if (E = c != null ? c[U] : void 0, o.hasOwnProperty(U) && T !== E && (T != null || E != null))
          if (U === "style")
            if (E) {
              for (m in E)
                !E.hasOwnProperty(m) || T && T.hasOwnProperty(m) || (l || (l = {}), l[m] = "");
              for (m in T)
                T.hasOwnProperty(m) && E[m] !== T[m] && (l || (l = {}), l[m] = T[m]);
            } else
              l || (d || (d = []), d.push(
                U,
                l
              )), l = T;
          else
            U === "dangerouslySetInnerHTML" ? (T = T ? T.__html : void 0, E = E ? E.__html : void 0, T != null && E !== T && (d = d || []).push(U, T)) : U === "children" ? typeof T != "string" && typeof T != "number" || (d = d || []).push(U, "" + T) : U !== "suppressContentEditableWarning" && U !== "suppressHydrationWarning" && (Dt.hasOwnProperty(U) ? (T != null && U === "onScroll" && Jt("scroll", n), d || E === T || (d = [])) : (d = d || []).push(U, T));
      }
      l && (d = d || []).push("style", l);
      var U = d;
      (r.updateQueue = U) && (r.flags |= 4);
    }
  }, Pa = function(n, r, l, o) {
    l !== o && (r.flags |= 4);
  };
  function xn(n, r) {
    if (!un)
      switch (n.tailMode) {
        case "hidden":
          r = n.tail;
          for (var l = null; r !== null; )
            r.alternate !== null && (l = r), r = r.sibling;
          l === null ? n.tail = null : l.sibling = null;
          break;
        case "collapsed":
          l = n.tail;
          for (var o = null; l !== null; )
            l.alternate !== null && (o = l), l = l.sibling;
          o === null ? r || n.tail === null ? n.tail = null : n.tail.sibling = null : o.sibling = null;
      }
  }
  function Tr(n) {
    var r = n.alternate !== null && n.alternate.child === n.child, l = 0, o = 0;
    if (r)
      for (var c = n.child; c !== null; )
        l |= c.lanes | c.childLanes, o |= c.subtreeFlags & 14680064, o |= c.flags & 14680064, c.return = n, c = c.sibling;
    else
      for (c = n.child; c !== null; )
        l |= c.lanes | c.childLanes, o |= c.subtreeFlags, o |= c.flags, c.return = n, c = c.sibling;
    return n.subtreeFlags |= o, n.childLanes = l, r;
  }
  function oy(n, r, l) {
    var o = r.pendingProps;
    switch (md(r), r.tag) {
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
        return Tr(r), null;
      case 1:
        return cn(r.type) && Ua(), Tr(r), null;
      case 3:
        return o = r.stateNode, ro(), jt(Tn), jt(Ie), Td(), o.pendingContext && (o.context = o.pendingContext, o.pendingContext = null), (n === null || n.child === null) && (yc(r) ? r.flags |= 4 : n === null || n.memoizedState.isDehydrated && !(r.flags & 256) || (r.flags |= 1024, ja !== null && (jd(ja), ja = null))), po(n, r), Tr(r), null;
      case 5:
        Rd(r);
        var c = uu(ps.current);
        if (l = r.type, n !== null && r.stateNode != null)
          vo(n, r, l, o, c), n.ref !== r.ref && (r.flags |= 512, r.flags |= 2097152);
        else {
          if (!o) {
            if (r.stateNode === null)
              throw Error(k(166));
            return Tr(r), null;
          }
          if (n = uu(ui.current), yc(r)) {
            o = r.stateNode, l = r.type;
            var d = r.memoizedProps;
            switch (o[gi] = r, o[ru] = d, n = (r.mode & 1) !== 0, l) {
              case "dialog":
                Jt("cancel", o), Jt("close", o);
                break;
              case "iframe":
              case "object":
              case "embed":
                Jt("load", o);
                break;
              case "video":
              case "audio":
                for (c = 0; c < as.length; c++)
                  Jt(as[c], o);
                break;
              case "source":
                Jt("error", o);
                break;
              case "img":
              case "image":
              case "link":
                Jt(
                  "error",
                  o
                ), Jt("load", o);
                break;
              case "details":
                Jt("toggle", o);
                break;
              case "input":
                Vn(o, d), Jt("invalid", o);
                break;
              case "select":
                o._wrapperState = { wasMultiple: !!d.multiple }, Jt("invalid", o);
                break;
              case "textarea":
                yr(o, d), Jt("invalid", o);
            }
            Dn(l, d), c = null;
            for (var m in d)
              if (d.hasOwnProperty(m)) {
                var E = d[m];
                m === "children" ? typeof E == "string" ? o.textContent !== E && (d.suppressHydrationWarning !== !0 && fc(o.textContent, E, n), c = ["children", E]) : typeof E == "number" && o.textContent !== "" + E && (d.suppressHydrationWarning !== !0 && fc(
                  o.textContent,
                  E,
                  n
                ), c = ["children", "" + E]) : Dt.hasOwnProperty(m) && E != null && m === "onScroll" && Jt("scroll", o);
              }
            switch (l) {
              case "input":
                hr(o), $r(o, d, !0);
                break;
              case "textarea":
                hr(o), rr(o);
                break;
              case "select":
              case "option":
                break;
              default:
                typeof d.onClick == "function" && (o.onclick = dc);
            }
            o = c, r.updateQueue = o, o !== null && (r.flags |= 4);
          } else {
            m = c.nodeType === 9 ? c : c.ownerDocument, n === "http://www.w3.org/1999/xhtml" && (n = Qr(l)), n === "http://www.w3.org/1999/xhtml" ? l === "script" ? (n = m.createElement("div"), n.innerHTML = "<script><\/script>", n = n.removeChild(n.firstChild)) : typeof o.is == "string" ? n = m.createElement(l, { is: o.is }) : (n = m.createElement(l), l === "select" && (m = n, o.multiple ? m.multiple = !0 : o.size && (m.size = o.size))) : n = m.createElementNS(n, l), n[gi] = r, n[ru] = o, Ci(n, r, !1, !1), r.stateNode = n;
            e: {
              switch (m = mn(l, o), l) {
                case "dialog":
                  Jt("cancel", n), Jt("close", n), c = o;
                  break;
                case "iframe":
                case "object":
                case "embed":
                  Jt("load", n), c = o;
                  break;
                case "video":
                case "audio":
                  for (c = 0; c < as.length; c++)
                    Jt(as[c], n);
                  c = o;
                  break;
                case "source":
                  Jt("error", n), c = o;
                  break;
                case "img":
                case "image":
                case "link":
                  Jt(
                    "error",
                    n
                  ), Jt("load", n), c = o;
                  break;
                case "details":
                  Jt("toggle", n), c = o;
                  break;
                case "input":
                  Vn(n, o), c = Wn(n, o), Jt("invalid", n);
                  break;
                case "option":
                  c = o;
                  break;
                case "select":
                  n._wrapperState = { wasMultiple: !!o.multiple }, c = ae({}, o, { value: void 0 }), Jt("invalid", n);
                  break;
                case "textarea":
                  yr(n, o), c = Ir(n, o), Jt("invalid", n);
                  break;
                default:
                  c = o;
              }
              Dn(l, c), E = c;
              for (d in E)
                if (E.hasOwnProperty(d)) {
                  var T = E[d];
                  d === "style" ? At(n, T) : d === "dangerouslySetInnerHTML" ? (T = T ? T.__html : void 0, T != null && fi(n, T)) : d === "children" ? typeof T == "string" ? (l !== "textarea" || T !== "") && pa(n, T) : typeof T == "number" && pa(n, "" + T) : d !== "suppressContentEditableWarning" && d !== "suppressHydrationWarning" && d !== "autoFocus" && (Dt.hasOwnProperty(d) ? T != null && d === "onScroll" && Jt("scroll", n) : T != null && qe(n, d, T, m));
                }
              switch (l) {
                case "input":
                  hr(n), $r(n, o, !1);
                  break;
                case "textarea":
                  hr(n), rr(n);
                  break;
                case "option":
                  o.value != null && n.setAttribute("value", "" + st(o.value));
                  break;
                case "select":
                  n.multiple = !!o.multiple, d = o.value, d != null ? mr(n, !!o.multiple, d, !1) : o.defaultValue != null && mr(
                    n,
                    !!o.multiple,
                    o.defaultValue,
                    !0
                  );
                  break;
                default:
                  typeof c.onClick == "function" && (n.onclick = dc);
              }
              switch (l) {
                case "button":
                case "input":
                case "select":
                case "textarea":
                  o = !!o.autoFocus;
                  break e;
                case "img":
                  o = !0;
                  break e;
                default:
                  o = !1;
              }
            }
            o && (r.flags |= 4);
          }
          r.ref !== null && (r.flags |= 512, r.flags |= 2097152);
        }
        return Tr(r), null;
      case 6:
        if (n && r.stateNode != null)
          Pa(n, r, n.memoizedProps, o);
        else {
          if (typeof o != "string" && r.stateNode === null)
            throw Error(k(166));
          if (l = uu(ps.current), uu(ui.current), yc(r)) {
            if (o = r.stateNode, l = r.memoizedProps, o[gi] = r, (d = o.nodeValue !== l) && (n = Sa, n !== null))
              switch (n.tag) {
                case 3:
                  fc(o.nodeValue, l, (n.mode & 1) !== 0);
                  break;
                case 5:
                  n.memoizedProps.suppressHydrationWarning !== !0 && fc(o.nodeValue, l, (n.mode & 1) !== 0);
              }
            d && (r.flags |= 4);
          } else
            o = (l.nodeType === 9 ? l : l.ownerDocument).createTextNode(o), o[gi] = r, r.stateNode = o;
        }
        return Tr(r), null;
      case 13:
        if (jt(fn), o = r.memoizedState, n === null || n.memoizedState !== null && n.memoizedState.dehydrated !== null) {
          if (un && ta !== null && r.mode & 1 && !(r.flags & 128))
            Dv(), gn(), r.flags |= 98560, d = !1;
          else if (d = yc(r), o !== null && o.dehydrated !== null) {
            if (n === null) {
              if (!d)
                throw Error(k(318));
              if (d = r.memoizedState, d = d !== null ? d.dehydrated : null, !d)
                throw Error(k(317));
              d[gi] = r;
            } else
              gn(), !(r.flags & 128) && (r.memoizedState = null), r.flags |= 4;
            Tr(r), d = !1;
          } else
            ja !== null && (jd(ja), ja = null), d = !0;
          if (!d)
            return r.flags & 65536 ? r : null;
        }
        return r.flags & 128 ? (r.lanes = l, r) : (o = o !== null, o !== (n !== null && n.memoizedState !== null) && o && (r.child.flags |= 8192, r.mode & 1 && (n === null || fn.current & 1 ? $n === 0 && ($n = 3) : ks())), r.updateQueue !== null && (r.flags |= 4), Tr(r), null);
      case 4:
        return ro(), po(n, r), n === null && Xu(r.stateNode.containerInfo), Tr(r), null;
      case 10:
        return Sd(r.type._context), Tr(r), null;
      case 17:
        return cn(r.type) && Ua(), Tr(r), null;
      case 19:
        if (jt(fn), d = r.memoizedState, d === null)
          return Tr(r), null;
        if (o = (r.flags & 128) !== 0, m = d.rendering, m === null)
          if (o)
            xn(d, !1);
          else {
            if ($n !== 0 || n !== null && n.flags & 128)
              for (n = r.child; n !== null; ) {
                if (m = Tc(n), m !== null) {
                  for (r.flags |= 128, xn(d, !1), o = m.updateQueue, o !== null && (r.updateQueue = o, r.flags |= 4), r.subtreeFlags = 0, o = l, l = r.child; l !== null; )
                    d = l, n = o, d.flags &= 14680066, m = d.alternate, m === null ? (d.childLanes = 0, d.lanes = n, d.child = null, d.subtreeFlags = 0, d.memoizedProps = null, d.memoizedState = null, d.updateQueue = null, d.dependencies = null, d.stateNode = null) : (d.childLanes = m.childLanes, d.lanes = m.lanes, d.child = m.child, d.subtreeFlags = 0, d.deletions = null, d.memoizedProps = m.memoizedProps, d.memoizedState = m.memoizedState, d.updateQueue = m.updateQueue, d.type = m.type, n = m.dependencies, d.dependencies = n === null ? null : { lanes: n.lanes, firstContext: n.firstContext }), l = l.sibling;
                  return $t(fn, fn.current & 1 | 2), r.child;
                }
                n = n.sibling;
              }
            d.tail !== null && Lt() > xo && (r.flags |= 128, o = !0, xn(d, !1), r.lanes = 4194304);
          }
        else {
          if (!o)
            if (n = Tc(m), n !== null) {
              if (r.flags |= 128, o = !0, l = n.updateQueue, l !== null && (r.updateQueue = l, r.flags |= 4), xn(d, !0), d.tail === null && d.tailMode === "hidden" && !m.alternate && !un)
                return Tr(r), null;
            } else
              2 * Lt() - d.renderingStartTime > xo && l !== 1073741824 && (r.flags |= 128, o = !0, xn(d, !1), r.lanes = 4194304);
          d.isBackwards ? (m.sibling = r.child, r.child = m) : (l = d.last, l !== null ? l.sibling = m : r.child = m, d.last = m);
        }
        return d.tail !== null ? (r = d.tail, d.rendering = r, d.tail = r.sibling, d.renderingStartTime = Lt(), r.sibling = null, l = fn.current, $t(fn, o ? l & 1 | 2 : l & 1), r) : (Tr(r), null);
      case 22:
      case 23:
        return nf(), o = r.memoizedState !== null, n !== null && n.memoizedState !== null !== o && (r.flags |= 8192), o && r.mode & 1 ? la & 1073741824 && (Tr(r), r.subtreeFlags & 6 && (r.flags |= 8192)) : Tr(r), null;
      case 24:
        return null;
      case 25:
        return null;
    }
    throw Error(k(156, r.tag));
  }
  function sy(n, r) {
    switch (md(r), r.tag) {
      case 1:
        return cn(r.type) && Ua(), n = r.flags, n & 65536 ? (r.flags = n & -65537 | 128, r) : null;
      case 3:
        return ro(), jt(Tn), jt(Ie), Td(), n = r.flags, n & 65536 && !(n & 128) ? (r.flags = n & -65537 | 128, r) : null;
      case 5:
        return Rd(r), null;
      case 13:
        if (jt(fn), n = r.memoizedState, n !== null && n.dehydrated !== null) {
          if (r.alternate === null)
            throw Error(k(340));
          gn();
        }
        return n = r.flags, n & 65536 ? (r.flags = n & -65537 | 128, r) : null;
      case 19:
        return jt(fn), null;
      case 4:
        return ro(), null;
      case 10:
        return Sd(r.type._context), null;
      case 22:
      case 23:
        return nf(), null;
      case 24:
        return null;
      default:
        return null;
    }
  }
  var ho = !1, lr = !1, Qc = typeof WeakSet == "function" ? WeakSet : Set, he = null;
  function mo(n, r) {
    var l = n.ref;
    if (l !== null)
      if (typeof l == "function")
        try {
          l(null);
        } catch (o) {
          bn(n, r, o);
        }
      else
        l.current = null;
  }
  function Ld(n, r, l) {
    try {
      l();
    } catch (o) {
      bn(n, r, o);
    }
  }
  var Wc = !1;
  function cy(n, r) {
    if (od = La, n = lc(), Hi(n)) {
      if ("selectionStart" in n)
        var l = { start: n.selectionStart, end: n.selectionEnd };
      else
        e: {
          l = (l = n.ownerDocument) && l.defaultView || window;
          var o = l.getSelection && l.getSelection();
          if (o && o.rangeCount !== 0) {
            l = o.anchorNode;
            var c = o.anchorOffset, d = o.focusNode;
            o = o.focusOffset;
            try {
              l.nodeType, d.nodeType;
            } catch {
              l = null;
              break e;
            }
            var m = 0, E = -1, T = -1, U = 0, W = 0, G = n, I = null;
            t:
              for (; ; ) {
                for (var ce; G !== l || c !== 0 && G.nodeType !== 3 || (E = m + c), G !== d || o !== 0 && G.nodeType !== 3 || (T = m + o), G.nodeType === 3 && (m += G.nodeValue.length), (ce = G.firstChild) !== null; )
                  I = G, G = ce;
                for (; ; ) {
                  if (G === n)
                    break t;
                  if (I === l && ++U === c && (E = m), I === d && ++W === o && (T = m), (ce = G.nextSibling) !== null)
                    break;
                  G = I, I = G.parentNode;
                }
                G = ce;
              }
            l = E === -1 || T === -1 ? null : { start: E, end: T };
          } else
            l = null;
        }
      l = l || { start: 0, end: 0 };
    } else
      l = null;
    for (tu = { focusedElem: n, selectionRange: l }, La = !1, he = r; he !== null; )
      if (r = he, n = r.child, (r.subtreeFlags & 1028) !== 0 && n !== null)
        n.return = r, he = n;
      else
        for (; he !== null; ) {
          r = he;
          try {
            var ye = r.alternate;
            if (r.flags & 1024)
              switch (r.tag) {
                case 0:
                case 11:
                case 15:
                  break;
                case 1:
                  if (ye !== null) {
                    var Ee = ye.memoizedProps, Mn = ye.memoizedState, D = r.stateNode, w = D.getSnapshotBeforeUpdate(r.elementType === r.type ? Ee : ra(r.type, Ee), Mn);
                    D.__reactInternalSnapshotBeforeUpdate = w;
                  }
                  break;
                case 3:
                  var M = r.stateNode.containerInfo;
                  M.nodeType === 1 ? M.textContent = "" : M.nodeType === 9 && M.documentElement && M.removeChild(M.documentElement);
                  break;
                case 5:
                case 6:
                case 4:
                case 17:
                  break;
                default:
                  throw Error(k(163));
              }
          } catch (Z) {
            bn(r, r.return, Z);
          }
          if (n = r.sibling, n !== null) {
            n.return = r.return, he = n;
            break;
          }
          he = r.return;
        }
    return ye = Wc, Wc = !1, ye;
  }
  function yo(n, r, l) {
    var o = r.updateQueue;
    if (o = o !== null ? o.lastEffect : null, o !== null) {
      var c = o = o.next;
      do {
        if ((c.tag & n) === n) {
          var d = c.destroy;
          c.destroy = void 0, d !== void 0 && Ld(r, l, d);
        }
        c = c.next;
      } while (c !== o);
    }
  }
  function Gc(n, r) {
    if (r = r.updateQueue, r = r !== null ? r.lastEffect : null, r !== null) {
      var l = r = r.next;
      do {
        if ((l.tag & n) === n) {
          var o = l.create;
          l.destroy = o();
        }
        l = l.next;
      } while (l !== r);
    }
  }
  function qc(n) {
    var r = n.ref;
    if (r !== null) {
      var l = n.stateNode;
      switch (n.tag) {
        case 5:
          n = l;
          break;
        default:
          n = l;
      }
      typeof r == "function" ? r(n) : r.current = n;
    }
  }
  function Gv(n) {
    var r = n.alternate;
    r !== null && (n.alternate = null, Gv(r)), n.child = null, n.deletions = null, n.sibling = null, n.tag === 5 && (r = n.stateNode, r !== null && (delete r[gi], delete r[ru], delete r[fd], delete r[ay], delete r[dd])), n.stateNode = null, n.return = null, n.dependencies = null, n.memoizedProps = null, n.memoizedState = null, n.pendingProps = null, n.stateNode = null, n.updateQueue = null;
  }
  function Md(n) {
    return n.tag === 5 || n.tag === 3 || n.tag === 4;
  }
  function qv(n) {
    e:
      for (; ; ) {
        for (; n.sibling === null; ) {
          if (n.return === null || Md(n.return))
            return null;
          n = n.return;
        }
        for (n.sibling.return = n.return, n = n.sibling; n.tag !== 5 && n.tag !== 6 && n.tag !== 18; ) {
          if (n.flags & 2 || n.child === null || n.tag === 4)
            continue e;
          n.child.return = n, n = n.child;
        }
        if (!(n.flags & 2))
          return n.stateNode;
      }
  }
  function xs(n, r, l) {
    var o = n.tag;
    if (o === 5 || o === 6)
      n = n.stateNode, r ? l.nodeType === 8 ? l.parentNode.insertBefore(n, r) : l.insertBefore(n, r) : (l.nodeType === 8 ? (r = l.parentNode, r.insertBefore(n, l)) : (r = l, r.appendChild(n)), l = l._reactRootContainer, l != null || r.onclick !== null || (r.onclick = dc));
    else if (o !== 4 && (n = n.child, n !== null))
      for (xs(n, r, l), n = n.sibling; n !== null; )
        xs(n, r, l), n = n.sibling;
  }
  function go(n, r, l) {
    var o = n.tag;
    if (o === 5 || o === 6)
      n = n.stateNode, r ? l.insertBefore(n, r) : l.appendChild(n);
    else if (o !== 4 && (n = n.child, n !== null))
      for (go(n, r, l), n = n.sibling; n !== null; )
        go(n, r, l), n = n.sibling;
  }
  var dn = null, Jn = !1;
  function Mr(n, r, l) {
    for (l = l.child; l !== null; )
      So(n, r, l), l = l.sibling;
  }
  function So(n, r, l) {
    if (Wr && typeof Wr.onCommitFiberUnmount == "function")
      try {
        Wr.onCommitFiberUnmount(fl, l);
      } catch {
      }
    switch (l.tag) {
      case 5:
        lr || mo(l, r);
      case 6:
        var o = dn, c = Jn;
        dn = null, Mr(n, r, l), dn = o, Jn = c, dn !== null && (Jn ? (n = dn, l = l.stateNode, n.nodeType === 8 ? n.parentNode.removeChild(l) : n.removeChild(l)) : dn.removeChild(l.stateNode));
        break;
      case 18:
        dn !== null && (Jn ? (n = dn, l = l.stateNode, n.nodeType === 8 ? Rl(n.parentNode, l) : n.nodeType === 1 && Rl(n, l), gl(n)) : Rl(dn, l.stateNode));
        break;
      case 4:
        o = dn, c = Jn, dn = l.stateNode.containerInfo, Jn = !0, Mr(n, r, l), dn = o, Jn = c;
        break;
      case 0:
      case 11:
      case 14:
      case 15:
        if (!lr && (o = l.updateQueue, o !== null && (o = o.lastEffect, o !== null))) {
          c = o = o.next;
          do {
            var d = c, m = d.destroy;
            d = d.tag, m !== void 0 && (d & 2 || d & 4) && Ld(l, r, m), c = c.next;
          } while (c !== o);
        }
        Mr(n, r, l);
        break;
      case 1:
        if (!lr && (mo(l, r), o = l.stateNode, typeof o.componentWillUnmount == "function"))
          try {
            o.props = l.memoizedProps, o.state = l.memoizedState, o.componentWillUnmount();
          } catch (E) {
            bn(l, r, E);
          }
        Mr(n, r, l);
        break;
      case 21:
        Mr(n, r, l);
        break;
      case 22:
        l.mode & 1 ? (lr = (o = lr) || l.memoizedState !== null, Mr(n, r, l), lr = o) : Mr(n, r, l);
        break;
      default:
        Mr(n, r, l);
    }
  }
  function Eo(n) {
    var r = n.updateQueue;
    if (r !== null) {
      n.updateQueue = null;
      var l = n.stateNode;
      l === null && (l = n.stateNode = new Qc()), r.forEach(function(o) {
        var c = yy.bind(null, n, o);
        l.has(o) || (l.add(o), o.then(c, c));
      });
    }
  }
  function er(n, r) {
    var l = r.deletions;
    if (l !== null)
      for (var o = 0; o < l.length; o++) {
        var c = l[o];
        try {
          var d = n, m = r, E = m;
          e:
            for (; E !== null; ) {
              switch (E.tag) {
                case 5:
                  dn = E.stateNode, Jn = !1;
                  break e;
                case 3:
                  dn = E.stateNode.containerInfo, Jn = !0;
                  break e;
                case 4:
                  dn = E.stateNode.containerInfo, Jn = !0;
                  break e;
              }
              E = E.return;
            }
          if (dn === null)
            throw Error(k(160));
          So(d, m, c), dn = null, Jn = !1;
          var T = c.alternate;
          T !== null && (T.return = null), c.return = null;
        } catch (U) {
          bn(c, r, U);
        }
      }
    if (r.subtreeFlags & 12854)
      for (r = r.child; r !== null; )
        Xv(r, n), r = r.sibling;
  }
  function Xv(n, r) {
    var l = n.alternate, o = n.flags;
    switch (n.tag) {
      case 0:
      case 11:
      case 14:
      case 15:
        if (er(r, n), Ri(n), o & 4) {
          try {
            yo(3, n, n.return), Gc(3, n);
          } catch (Ee) {
            bn(n, n.return, Ee);
          }
          try {
            yo(5, n, n.return);
          } catch (Ee) {
            bn(n, n.return, Ee);
          }
        }
        break;
      case 1:
        er(r, n), Ri(n), o & 512 && l !== null && mo(l, l.return);
        break;
      case 5:
        if (er(r, n), Ri(n), o & 512 && l !== null && mo(l, l.return), n.flags & 32) {
          var c = n.stateNode;
          try {
            pa(c, "");
          } catch (Ee) {
            bn(n, n.return, Ee);
          }
        }
        if (o & 4 && (c = n.stateNode, c != null)) {
          var d = n.memoizedProps, m = l !== null ? l.memoizedProps : d, E = n.type, T = n.updateQueue;
          if (n.updateQueue = null, T !== null)
            try {
              E === "input" && d.type === "radio" && d.name != null && zn(c, d), mn(E, m);
              var U = mn(E, d);
              for (m = 0; m < T.length; m += 2) {
                var W = T[m], G = T[m + 1];
                W === "style" ? At(c, G) : W === "dangerouslySetInnerHTML" ? fi(c, G) : W === "children" ? pa(c, G) : qe(c, W, G, U);
              }
              switch (E) {
                case "input":
                  kn(c, d);
                  break;
                case "textarea":
                  da(c, d);
                  break;
                case "select":
                  var I = c._wrapperState.wasMultiple;
                  c._wrapperState.wasMultiple = !!d.multiple;
                  var ce = d.value;
                  ce != null ? mr(c, !!d.multiple, ce, !1) : I !== !!d.multiple && (d.defaultValue != null ? mr(
                    c,
                    !!d.multiple,
                    d.defaultValue,
                    !0
                  ) : mr(c, !!d.multiple, d.multiple ? [] : "", !1));
              }
              c[ru] = d;
            } catch (Ee) {
              bn(n, n.return, Ee);
            }
        }
        break;
      case 6:
        if (er(r, n), Ri(n), o & 4) {
          if (n.stateNode === null)
            throw Error(k(162));
          c = n.stateNode, d = n.memoizedProps;
          try {
            c.nodeValue = d;
          } catch (Ee) {
            bn(n, n.return, Ee);
          }
        }
        break;
      case 3:
        if (er(r, n), Ri(n), o & 4 && l !== null && l.memoizedState.isDehydrated)
          try {
            gl(r.containerInfo);
          } catch (Ee) {
            bn(n, n.return, Ee);
          }
        break;
      case 4:
        er(r, n), Ri(n);
        break;
      case 13:
        er(r, n), Ri(n), c = n.child, c.flags & 8192 && (d = c.memoizedState !== null, c.stateNode.isHidden = d, !d || c.alternate !== null && c.alternate.memoizedState !== null || (Kc = Lt())), o & 4 && Eo(n);
        break;
      case 22:
        if (W = l !== null && l.memoizedState !== null, n.mode & 1 ? (lr = (U = lr) || W, er(r, n), lr = U) : er(r, n), Ri(n), o & 8192) {
          if (U = n.memoizedState !== null, (n.stateNode.isHidden = U) && !W && n.mode & 1)
            for (he = n, W = n.child; W !== null; ) {
              for (G = he = W; he !== null; ) {
                switch (I = he, ce = I.child, I.tag) {
                  case 0:
                  case 11:
                  case 14:
                  case 15:
                    yo(4, I, I.return);
                    break;
                  case 1:
                    mo(I, I.return);
                    var ye = I.stateNode;
                    if (typeof ye.componentWillUnmount == "function") {
                      o = I, l = I.return;
                      try {
                        r = o, ye.props = r.memoizedProps, ye.state = r.memoizedState, ye.componentWillUnmount();
                      } catch (Ee) {
                        bn(o, l, Ee);
                      }
                    }
                    break;
                  case 5:
                    mo(I, I.return);
                    break;
                  case 22:
                    if (I.memoizedState !== null) {
                      Kv(G);
                      continue;
                    }
                }
                ce !== null ? (ce.return = I, he = ce) : Kv(G);
              }
              W = W.sibling;
            }
          e:
            for (W = null, G = n; ; ) {
              if (G.tag === 5) {
                if (W === null) {
                  W = G;
                  try {
                    c = G.stateNode, U ? (d = c.style, typeof d.setProperty == "function" ? d.setProperty("display", "none", "important") : d.display = "none") : (E = G.stateNode, T = G.memoizedProps.style, m = T != null && T.hasOwnProperty("display") ? T.display : null, E.style.display = at("display", m));
                  } catch (Ee) {
                    bn(n, n.return, Ee);
                  }
                }
              } else if (G.tag === 6) {
                if (W === null)
                  try {
                    G.stateNode.nodeValue = U ? "" : G.memoizedProps;
                  } catch (Ee) {
                    bn(n, n.return, Ee);
                  }
              } else if ((G.tag !== 22 && G.tag !== 23 || G.memoizedState === null || G === n) && G.child !== null) {
                G.child.return = G, G = G.child;
                continue;
              }
              if (G === n)
                break e;
              for (; G.sibling === null; ) {
                if (G.return === null || G.return === n)
                  break e;
                W === G && (W = null), G = G.return;
              }
              W === G && (W = null), G.sibling.return = G.return, G = G.sibling;
            }
        }
        break;
      case 19:
        er(r, n), Ri(n), o & 4 && Eo(n);
        break;
      case 21:
        break;
      default:
        er(
          r,
          n
        ), Ri(n);
    }
  }
  function Ri(n) {
    var r = n.flags;
    if (r & 2) {
      try {
        e: {
          for (var l = n.return; l !== null; ) {
            if (Md(l)) {
              var o = l;
              break e;
            }
            l = l.return;
          }
          throw Error(k(160));
        }
        switch (o.tag) {
          case 5:
            var c = o.stateNode;
            o.flags & 32 && (pa(c, ""), o.flags &= -33);
            var d = qv(n);
            go(n, d, c);
            break;
          case 3:
          case 4:
            var m = o.stateNode.containerInfo, E = qv(n);
            xs(n, E, m);
            break;
          default:
            throw Error(k(161));
        }
      } catch (T) {
        bn(n, n.return, T);
      }
      n.flags &= -3;
    }
    r & 4096 && (n.flags &= -4097);
  }
  function fy(n, r, l) {
    he = n, Nd(n);
  }
  function Nd(n, r, l) {
    for (var o = (n.mode & 1) !== 0; he !== null; ) {
      var c = he, d = c.child;
      if (c.tag === 22 && o) {
        var m = c.memoizedState !== null || ho;
        if (!m) {
          var E = c.alternate, T = E !== null && E.memoizedState !== null || lr;
          E = ho;
          var U = lr;
          if (ho = m, (lr = T) && !U)
            for (he = c; he !== null; )
              m = he, T = m.child, m.tag === 22 && m.memoizedState !== null ? zd(c) : T !== null ? (T.return = m, he = T) : zd(c);
          for (; d !== null; )
            he = d, Nd(d), d = d.sibling;
          he = c, ho = E, lr = U;
        }
        Co(n);
      } else
        c.subtreeFlags & 8772 && d !== null ? (d.return = c, he = d) : Co(n);
    }
  }
  function Co(n) {
    for (; he !== null; ) {
      var r = he;
      if (r.flags & 8772) {
        var l = r.alternate;
        try {
          if (r.flags & 8772)
            switch (r.tag) {
              case 0:
              case 11:
              case 15:
                lr || Gc(5, r);
                break;
              case 1:
                var o = r.stateNode;
                if (r.flags & 4 && !lr)
                  if (l === null)
                    o.componentDidMount();
                  else {
                    var c = r.elementType === r.type ? l.memoizedProps : ra(r.type, l.memoizedProps);
                    o.componentDidUpdate(c, l.memoizedState, o.__reactInternalSnapshotBeforeUpdate);
                  }
                var d = r.updateQueue;
                d !== null && zv(r, d, o);
                break;
              case 3:
                var m = r.updateQueue;
                if (m !== null) {
                  if (l = null, r.child !== null)
                    switch (r.child.tag) {
                      case 5:
                        l = r.child.stateNode;
                        break;
                      case 1:
                        l = r.child.stateNode;
                    }
                  zv(r, m, l);
                }
                break;
              case 5:
                var E = r.stateNode;
                if (l === null && r.flags & 4) {
                  l = E;
                  var T = r.memoizedProps;
                  switch (r.type) {
                    case "button":
                    case "input":
                    case "select":
                    case "textarea":
                      T.autoFocus && l.focus();
                      break;
                    case "img":
                      T.src && (l.src = T.src);
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
                if (r.memoizedState === null) {
                  var U = r.alternate;
                  if (U !== null) {
                    var W = U.memoizedState;
                    if (W !== null) {
                      var G = W.dehydrated;
                      G !== null && gl(G);
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
                throw Error(k(163));
            }
          lr || r.flags & 512 && qc(r);
        } catch (I) {
          bn(r, r.return, I);
        }
      }
      if (r === n) {
        he = null;
        break;
      }
      if (l = r.sibling, l !== null) {
        l.return = r.return, he = l;
        break;
      }
      he = r.return;
    }
  }
  function Kv(n) {
    for (; he !== null; ) {
      var r = he;
      if (r === n) {
        he = null;
        break;
      }
      var l = r.sibling;
      if (l !== null) {
        l.return = r.return, he = l;
        break;
      }
      he = r.return;
    }
  }
  function zd(n) {
    for (; he !== null; ) {
      var r = he;
      try {
        switch (r.tag) {
          case 0:
          case 11:
          case 15:
            var l = r.return;
            try {
              Gc(4, r);
            } catch (T) {
              bn(r, l, T);
            }
            break;
          case 1:
            var o = r.stateNode;
            if (typeof o.componentDidMount == "function") {
              var c = r.return;
              try {
                o.componentDidMount();
              } catch (T) {
                bn(r, c, T);
              }
            }
            var d = r.return;
            try {
              qc(r);
            } catch (T) {
              bn(r, d, T);
            }
            break;
          case 5:
            var m = r.return;
            try {
              qc(r);
            } catch (T) {
              bn(r, m, T);
            }
        }
      } catch (T) {
        bn(r, r.return, T);
      }
      if (r === n) {
        he = null;
        break;
      }
      var E = r.sibling;
      if (E !== null) {
        E.return = r.return, he = E;
        break;
      }
      he = r.return;
    }
  }
  var dy = Math.ceil, hu = mt.ReactCurrentDispatcher, Xc = mt.ReactCurrentOwner, Ba = mt.ReactCurrentBatchConfig, yt = 0, wn = null, on = null, Bn = 0, la = 0, Ro = et(0), $n = 0, ws = null, mu = 0, To = 0, Ud = 0, Ml = null, xr = null, Kc = 0, xo = 1 / 0, Gi = null, Zc = !1, Ad = null, $a = null, wo = !1, Ya = null, Jc = 0, bs = 0, ef = null, _s = -1, yu = 0;
  function tr() {
    return yt & 6 ? Lt() : _s !== -1 ? _s : _s = Lt();
  }
  function qi(n) {
    return n.mode & 1 ? yt & 2 && Bn !== 0 ? Bn & -Bn : gc.transition !== null ? (yu === 0 && (yu = Au()), yu) : (n = Mt, n !== 0 || (n = window.event, n = n === void 0 ? 16 : qo(n.type)), n) : 1;
  }
  function Sn(n, r, l, o) {
    if (50 < bs)
      throw bs = 0, ef = null, Error(k(185));
    Ni(n, l, o), (!(yt & 2) || n !== wn) && (n === wn && (!(yt & 2) && (To |= l), $n === 4 && Ti(n, Bn)), Yn(n, o), l === 1 && yt === 0 && !(r.mode & 1) && (xo = Lt() + 500, Zn && Zr()));
  }
  function Yn(n, r) {
    var l = n.callbackNode;
    vl(n, r);
    var o = Or(n, n === wn ? Bn : 0);
    if (o === 0)
      l !== null && an(l), n.callbackNode = null, n.callbackPriority = 0;
    else if (r = o & -o, n.callbackPriority !== r) {
      if (l != null && an(l), r === 1)
        n.tag === 0 ? vd(bo.bind(null, n)) : pd(bo.bind(null, n)), cd(function() {
          !(yt & 6) && Zr();
        }), l = null;
      else {
        switch (Fu(o)) {
          case 1:
            l = kr;
            break;
          case 4:
            l = lt;
            break;
          case 16:
            l = Da;
            break;
          case 536870912:
            l = zu;
            break;
          default:
            l = Da;
        }
        l = ih(l, tf.bind(null, n));
      }
      n.callbackPriority = r, n.callbackNode = l;
    }
  }
  function tf(n, r) {
    if (_s = -1, yu = 0, yt & 6)
      throw Error(k(327));
    var l = n.callbackNode;
    if (_o() && n.callbackNode !== l)
      return null;
    var o = Or(n, n === wn ? Bn : 0);
    if (o === 0)
      return null;
    if (o & 30 || o & n.expiredLanes || r)
      r = rf(n, o);
    else {
      r = o;
      var c = yt;
      yt |= 2;
      var d = Jv();
      (wn !== n || Bn !== r) && (Gi = null, xo = Lt() + 500, Su(n, r));
      do
        try {
          vy();
          break;
        } catch (E) {
          Zv(n, E);
        }
      while (1);
      Ea(), hu.current = d, yt = c, on !== null ? r = 0 : (wn = null, Bn = 0, r = $n);
    }
    if (r !== 0) {
      if (r === 2 && (c = hl(n), c !== 0 && (o = c, r = gu(n, c))), r === 1)
        throw l = ws, Su(n, 0), Ti(n, o), Yn(n, Lt()), l;
      if (r === 6)
        Ti(n, o);
      else {
        if (c = n.current.alternate, !(o & 30) && !Fd(c) && (r = rf(n, o), r === 2 && (d = hl(n), d !== 0 && (o = d, r = gu(n, d))), r === 1))
          throw l = ws, Su(n, 0), Ti(n, o), Yn(n, Lt()), l;
        switch (n.finishedWork = c, n.finishedLanes = o, r) {
          case 0:
          case 1:
            throw Error(k(345));
          case 2:
            Nl(n, xr, Gi);
            break;
          case 3:
            if (Ti(n, o), (o & 130023424) === o && (r = Kc + 500 - Lt(), 10 < r)) {
              if (Or(n, 0) !== 0)
                break;
              if (c = n.suspendedLanes, (c & o) !== o) {
                tr(), n.pingedLanes |= n.suspendedLanes & c;
                break;
              }
              n.timeoutHandle = nu(Nl.bind(null, n, xr, Gi), r);
              break;
            }
            Nl(n, xr, Gi);
            break;
          case 4:
            if (Ti(n, o), (o & 4194240) === o)
              break;
            for (r = n.eventTimes, c = -1; 0 < o; ) {
              var m = 31 - Dr(o);
              d = 1 << m, m = r[m], m > c && (c = m), o &= ~d;
            }
            if (o = c, o = Lt() - o, o = (120 > o ? 120 : 480 > o ? 480 : 1080 > o ? 1080 : 1920 > o ? 1920 : 3e3 > o ? 3e3 : 4320 > o ? 4320 : 1960 * dy(o / 1960)) - o, 10 < o) {
              n.timeoutHandle = nu(Nl.bind(null, n, xr, Gi), o);
              break;
            }
            Nl(n, xr, Gi);
            break;
          case 5:
            Nl(n, xr, Gi);
            break;
          default:
            throw Error(k(329));
        }
      }
    }
    return Yn(n, Lt()), n.callbackNode === l ? tf.bind(null, n) : null;
  }
  function gu(n, r) {
    var l = Ml;
    return n.current.memoizedState.isDehydrated && (Su(n, r).flags |= 256), n = rf(n, r), n !== 2 && (r = xr, xr = l, r !== null && jd(r)), n;
  }
  function jd(n) {
    xr === null ? xr = n : xr.push.apply(xr, n);
  }
  function Fd(n) {
    for (var r = n; ; ) {
      if (r.flags & 16384) {
        var l = r.updateQueue;
        if (l !== null && (l = l.stores, l !== null))
          for (var o = 0; o < l.length; o++) {
            var c = l[o], d = c.getSnapshot;
            c = c.value;
            try {
              if (!Ma(d(), c))
                return !1;
            } catch {
              return !1;
            }
          }
      }
      if (l = r.child, r.subtreeFlags & 16384 && l !== null)
        l.return = r, r = l;
      else {
        if (r === n)
          break;
        for (; r.sibling === null; ) {
          if (r.return === null || r.return === n)
            return !0;
          r = r.return;
        }
        r.sibling.return = r.return, r = r.sibling;
      }
    }
    return !0;
  }
  function Ti(n, r) {
    for (r &= ~Ud, r &= ~To, n.suspendedLanes |= r, n.pingedLanes &= ~r, n = n.expirationTimes; 0 < r; ) {
      var l = 31 - Dr(r), o = 1 << l;
      n[l] = -1, r &= ~o;
    }
  }
  function bo(n) {
    if (yt & 6)
      throw Error(k(327));
    _o();
    var r = Or(n, 0);
    if (!(r & 1))
      return Yn(n, Lt()), null;
    var l = rf(n, r);
    if (n.tag !== 0 && l === 2) {
      var o = hl(n);
      o !== 0 && (r = o, l = gu(n, o));
    }
    if (l === 1)
      throw l = ws, Su(n, 0), Ti(n, r), Yn(n, Lt()), l;
    if (l === 6)
      throw Error(k(345));
    return n.finishedWork = n.current.alternate, n.finishedLanes = r, Nl(n, xr, Gi), Yn(n, Lt()), null;
  }
  function Hd(n, r) {
    var l = yt;
    yt |= 1;
    try {
      return n(r);
    } finally {
      yt = l, yt === 0 && (xo = Lt() + 500, Zn && Zr());
    }
  }
  function xi(n) {
    Ya !== null && Ya.tag === 0 && !(yt & 6) && _o();
    var r = yt;
    yt |= 1;
    var l = Ba.transition, o = Mt;
    try {
      if (Ba.transition = null, Mt = 1, n)
        return n();
    } finally {
      Mt = o, Ba.transition = l, yt = r, !(yt & 6) && Zr();
    }
  }
  function nf() {
    la = Ro.current, jt(Ro);
  }
  function Su(n, r) {
    n.finishedWork = null, n.finishedLanes = 0;
    var l = n.timeoutHandle;
    if (l !== -1 && (n.timeoutHandle = -1, wv(l)), on !== null)
      for (l = on.return; l !== null; ) {
        var o = l;
        switch (md(o), o.tag) {
          case 1:
            o = o.type.childContextTypes, o != null && Ua();
            break;
          case 3:
            ro(), jt(Tn), jt(Ie), Td();
            break;
          case 5:
            Rd(o);
            break;
          case 4:
            ro();
            break;
          case 13:
            jt(fn);
            break;
          case 19:
            jt(fn);
            break;
          case 10:
            Sd(o.type._context);
            break;
          case 22:
          case 23:
            nf();
        }
        l = l.return;
      }
    if (wn = n, on = n = zl(n.current, null), Bn = la = r, $n = 0, ws = null, Ud = To = mu = 0, xr = Ml = null, lu !== null) {
      for (r = 0; r < lu.length; r++)
        if (l = lu[r], o = l.interleaved, o !== null) {
          l.interleaved = null;
          var c = o.next, d = l.pending;
          if (d !== null) {
            var m = d.next;
            d.next = c, o.next = m;
          }
          l.pending = o;
        }
      lu = null;
    }
    return n;
  }
  function Zv(n, r) {
    do {
      var l = on;
      try {
        if (Ea(), wc.current = Rr, Ca) {
          for (var o = xe.memoizedState; o !== null; ) {
            var c = o.queue;
            c !== null && (c.pending = null), o = o.next;
          }
          Ca = !1;
        }
        if (Ce = 0, vt = Qe = xe = null, ao = !1, hs = 0, Xc.current = null, l === null || l.return === null) {
          $n = 1, ws = r, on = null;
          break;
        }
        e: {
          var d = n, m = l.return, E = l, T = r;
          if (r = Bn, E.flags |= 32768, T !== null && typeof T == "object" && typeof T.then == "function") {
            var U = T, W = E, G = W.tag;
            if (!(W.mode & 1) && (G === 0 || G === 11 || G === 15)) {
              var I = W.alternate;
              I ? (W.updateQueue = I.updateQueue, W.memoizedState = I.memoizedState, W.lanes = I.lanes) : (W.updateQueue = null, W.memoizedState = null);
            }
            var ce = $v(m);
            if (ce !== null) {
              ce.flags &= -257, kd(ce, m, E, d, r), ce.mode & 1 && Es(d, U, r), r = ce, T = U;
              var ye = r.updateQueue;
              if (ye === null) {
                var Ee = /* @__PURE__ */ new Set();
                Ee.add(T), r.updateQueue = Ee;
              } else
                ye.add(T);
              break e;
            } else {
              if (!(r & 1)) {
                Es(d, U, r), ks();
                break e;
              }
              T = Error(k(426));
            }
          } else if (un && E.mode & 1) {
            var Mn = $v(m);
            if (Mn !== null) {
              !(Mn.flags & 65536) && (Mn.flags |= 256), kd(Mn, m, E, d, r), gd(Ol(T, E));
              break e;
            }
          }
          d = T = Ol(T, E), $n !== 4 && ($n = 2), Ml === null ? Ml = [d] : Ml.push(d), d = m;
          do {
            switch (d.tag) {
              case 3:
                d.flags |= 65536, r &= -r, d.lanes |= r;
                var D = Pv(d, T, r);
                Nv(d, D);
                break e;
              case 1:
                E = T;
                var w = d.type, M = d.stateNode;
                if (!(d.flags & 128) && (typeof w.getDerivedStateFromError == "function" || M !== null && typeof M.componentDidCatch == "function" && ($a === null || !$a.has(M)))) {
                  d.flags |= 65536, r &= -r, d.lanes |= r;
                  var Z = Bv(d, E, r);
                  Nv(d, Z);
                  break e;
                }
            }
            d = d.return;
          } while (d !== null);
        }
        th(l);
      } catch (Re) {
        r = Re, on === l && l !== null && (on = l = l.return);
        continue;
      }
      break;
    } while (1);
  }
  function Jv() {
    var n = hu.current;
    return hu.current = Rr, n === null ? Rr : n;
  }
  function ks() {
    ($n === 0 || $n === 3 || $n === 2) && ($n = 4), wn === null || !(mu & 268435455) && !(To & 268435455) || Ti(wn, Bn);
  }
  function rf(n, r) {
    var l = yt;
    yt |= 2;
    var o = Jv();
    (wn !== n || Bn !== r) && (Gi = null, Su(n, r));
    do
      try {
        py();
        break;
      } catch (c) {
        Zv(n, c);
      }
    while (1);
    if (Ea(), yt = l, hu.current = o, on !== null)
      throw Error(k(261));
    return wn = null, Bn = 0, $n;
  }
  function py() {
    for (; on !== null; )
      eh(on);
  }
  function vy() {
    for (; on !== null && !Sr(); )
      eh(on);
  }
  function eh(n) {
    var r = ah(n.alternate, n, la);
    n.memoizedProps = n.pendingProps, r === null ? th(n) : on = r, Xc.current = null;
  }
  function th(n) {
    var r = n;
    do {
      var l = r.alternate;
      if (n = r.return, r.flags & 32768) {
        if (l = sy(l, r), l !== null) {
          l.flags &= 32767, on = l;
          return;
        }
        if (n !== null)
          n.flags |= 32768, n.subtreeFlags = 0, n.deletions = null;
        else {
          $n = 6, on = null;
          return;
        }
      } else if (l = oy(l, r, la), l !== null) {
        on = l;
        return;
      }
      if (r = r.sibling, r !== null) {
        on = r;
        return;
      }
      on = r = n;
    } while (r !== null);
    $n === 0 && ($n = 5);
  }
  function Nl(n, r, l) {
    var o = Mt, c = Ba.transition;
    try {
      Ba.transition = null, Mt = 1, hy(n, r, l, o);
    } finally {
      Ba.transition = c, Mt = o;
    }
    return null;
  }
  function hy(n, r, l, o) {
    do
      _o();
    while (Ya !== null);
    if (yt & 6)
      throw Error(k(327));
    l = n.finishedWork;
    var c = n.finishedLanes;
    if (l === null)
      return null;
    if (n.finishedWork = null, n.finishedLanes = 0, l === n.current)
      throw Error(k(177));
    n.callbackNode = null, n.callbackPriority = 0;
    var d = l.lanes | l.childLanes;
    if ($f(n, d), n === wn && (on = wn = null, Bn = 0), !(l.subtreeFlags & 2064) && !(l.flags & 2064) || wo || (wo = !0, ih(Da, function() {
      return _o(), null;
    })), d = (l.flags & 15990) !== 0, l.subtreeFlags & 15990 || d) {
      d = Ba.transition, Ba.transition = null;
      var m = Mt;
      Mt = 1;
      var E = yt;
      yt |= 4, Xc.current = null, cy(n, l), Xv(l, n), uc(tu), La = !!od, tu = od = null, n.current = l, fy(l), hi(), yt = E, Mt = m, Ba.transition = d;
    } else
      n.current = l;
    if (wo && (wo = !1, Ya = n, Jc = c), d = n.pendingLanes, d === 0 && ($a = null), Qo(l.stateNode), Yn(n, Lt()), r !== null)
      for (o = n.onRecoverableError, l = 0; l < r.length; l++)
        c = r[l], o(c.value, { componentStack: c.stack, digest: c.digest });
    if (Zc)
      throw Zc = !1, n = Ad, Ad = null, n;
    return Jc & 1 && n.tag !== 0 && _o(), d = n.pendingLanes, d & 1 ? n === ef ? bs++ : (bs = 0, ef = n) : bs = 0, Zr(), null;
  }
  function _o() {
    if (Ya !== null) {
      var n = Fu(Jc), r = Ba.transition, l = Mt;
      try {
        if (Ba.transition = null, Mt = 16 > n ? 16 : n, Ya === null)
          var o = !1;
        else {
          if (n = Ya, Ya = null, Jc = 0, yt & 6)
            throw Error(k(331));
          var c = yt;
          for (yt |= 4, he = n.current; he !== null; ) {
            var d = he, m = d.child;
            if (he.flags & 16) {
              var E = d.deletions;
              if (E !== null) {
                for (var T = 0; T < E.length; T++) {
                  var U = E[T];
                  for (he = U; he !== null; ) {
                    var W = he;
                    switch (W.tag) {
                      case 0:
                      case 11:
                      case 15:
                        yo(8, W, d);
                    }
                    var G = W.child;
                    if (G !== null)
                      G.return = W, he = G;
                    else
                      for (; he !== null; ) {
                        W = he;
                        var I = W.sibling, ce = W.return;
                        if (Gv(W), W === U) {
                          he = null;
                          break;
                        }
                        if (I !== null) {
                          I.return = ce, he = I;
                          break;
                        }
                        he = ce;
                      }
                  }
                }
                var ye = d.alternate;
                if (ye !== null) {
                  var Ee = ye.child;
                  if (Ee !== null) {
                    ye.child = null;
                    do {
                      var Mn = Ee.sibling;
                      Ee.sibling = null, Ee = Mn;
                    } while (Ee !== null);
                  }
                }
                he = d;
              }
            }
            if (d.subtreeFlags & 2064 && m !== null)
              m.return = d, he = m;
            else
              e:
                for (; he !== null; ) {
                  if (d = he, d.flags & 2048)
                    switch (d.tag) {
                      case 0:
                      case 11:
                      case 15:
                        yo(9, d, d.return);
                    }
                  var D = d.sibling;
                  if (D !== null) {
                    D.return = d.return, he = D;
                    break e;
                  }
                  he = d.return;
                }
          }
          var w = n.current;
          for (he = w; he !== null; ) {
            m = he;
            var M = m.child;
            if (m.subtreeFlags & 2064 && M !== null)
              M.return = m, he = M;
            else
              e:
                for (m = w; he !== null; ) {
                  if (E = he, E.flags & 2048)
                    try {
                      switch (E.tag) {
                        case 0:
                        case 11:
                        case 15:
                          Gc(9, E);
                      }
                    } catch (Re) {
                      bn(E, E.return, Re);
                    }
                  if (E === m) {
                    he = null;
                    break e;
                  }
                  var Z = E.sibling;
                  if (Z !== null) {
                    Z.return = E.return, he = Z;
                    break e;
                  }
                  he = E.return;
                }
          }
          if (yt = c, Zr(), Wr && typeof Wr.onPostCommitFiberRoot == "function")
            try {
              Wr.onPostCommitFiberRoot(fl, n);
            } catch {
            }
          o = !0;
        }
        return o;
      } finally {
        Mt = l, Ba.transition = r;
      }
    }
    return !1;
  }
  function nh(n, r, l) {
    r = Ol(l, r), r = Pv(n, r, 1), n = kl(n, r, 1), r = tr(), n !== null && (Ni(n, 1, r), Yn(n, r));
  }
  function bn(n, r, l) {
    if (n.tag === 3)
      nh(n, n, l);
    else
      for (; r !== null; ) {
        if (r.tag === 3) {
          nh(r, n, l);
          break;
        } else if (r.tag === 1) {
          var o = r.stateNode;
          if (typeof r.type.getDerivedStateFromError == "function" || typeof o.componentDidCatch == "function" && ($a === null || !$a.has(o))) {
            n = Ol(l, n), n = Bv(r, n, 1), r = kl(r, n, 1), n = tr(), r !== null && (Ni(r, 1, n), Yn(r, n));
            break;
          }
        }
        r = r.return;
      }
  }
  function my(n, r, l) {
    var o = n.pingCache;
    o !== null && o.delete(r), r = tr(), n.pingedLanes |= n.suspendedLanes & l, wn === n && (Bn & l) === l && ($n === 4 || $n === 3 && (Bn & 130023424) === Bn && 500 > Lt() - Kc ? Su(n, 0) : Ud |= l), Yn(n, r);
  }
  function rh(n, r) {
    r === 0 && (n.mode & 1 ? (r = dl, dl <<= 1, !(dl & 130023424) && (dl = 4194304)) : r = 1);
    var l = tr();
    n = Ii(n, r), n !== null && (Ni(n, r, l), Yn(n, l));
  }
  function Vd(n) {
    var r = n.memoizedState, l = 0;
    r !== null && (l = r.retryLane), rh(n, l);
  }
  function yy(n, r) {
    var l = 0;
    switch (n.tag) {
      case 13:
        var o = n.stateNode, c = n.memoizedState;
        c !== null && (l = c.retryLane);
        break;
      case 19:
        o = n.stateNode;
        break;
      default:
        throw Error(k(314));
    }
    o !== null && o.delete(r), rh(n, l);
  }
  var ah;
  ah = function(n, r, l) {
    if (n !== null)
      if (n.memoizedProps !== r.pendingProps || Tn.current)
        aa = !0;
      else {
        if (!(n.lanes & l) && !(r.flags & 128))
          return aa = !1, Wi(n, r, l);
        aa = !!(n.flags & 131072);
      }
    else
      aa = !1, un && r.flags & 1048576 && hd(r, Zu, r.index);
    switch (r.lanes = 0, r.tag) {
      case 2:
        var o = r.type;
        Ts(n, r), n = r.pendingProps;
        var c = za(r, Ie.current);
        eo(r, l), c = $(null, r, o, n, c, l);
        var d = Fn();
        return r.flags |= 1, typeof c == "object" && c !== null && typeof c.render == "function" && c.$$typeof === void 0 ? (r.tag = 1, r.memoizedState = null, r.updateQueue = null, cn(o) ? (d = !0, pc(r)) : d = !1, r.memoizedState = c.state !== null && c.state !== void 0 ? c.state : null, Ec(r), c.updater = du, r.stateNode = c, c._reactInternals = r, bd(r, o, n, l), r = Bc(null, r, o, !0, d, l)) : (r.tag = 0, un && d && vc(r), On(null, r, c, l), r = r.child), r;
      case 16:
        o = r.elementType;
        e: {
          switch (Ts(n, r), n = r.pendingProps, c = o._init, o = c(o._payload), r.type = o, c = r.tag = gy(o), n = ra(o, n), c) {
            case 0:
              r = Ke(null, r, o, n, l);
              break e;
            case 1:
              r = Cs(null, r, o, n, l);
              break e;
            case 11:
              r = fo(null, r, o, n, l);
              break e;
            case 14:
              r = Ll(null, r, o, ra(o.type, n), l);
              break e;
          }
          throw Error(k(
            306,
            o,
            ""
          ));
        }
        return r;
      case 0:
        return o = r.type, c = r.pendingProps, c = r.elementType === o ? c : ra(o, c), Ke(n, r, o, c, l);
      case 1:
        return o = r.type, c = r.pendingProps, c = r.elementType === o ? c : ra(o, c), Cs(n, r, o, c, l);
      case 3:
        e: {
          if (uy(r), n === null)
            throw Error(k(387));
          o = r.pendingProps, d = r.memoizedState, c = d.element, to(n, r), Rc(r, o, null, l);
          var m = r.memoizedState;
          if (o = m.element, d.isDehydrated)
            if (d = { element: o, isDehydrated: !1, cache: m.cache, pendingSuspenseBoundaries: m.pendingSuspenseBoundaries, transitions: m.transitions }, r.updateQueue.baseState = d, r.memoizedState = d, r.flags & 256) {
              c = Ol(Error(k(423)), r), r = Iv(n, r, o, l, c);
              break e;
            } else if (o !== c) {
              c = Ol(Error(k(424)), r), r = Iv(n, r, o, l, c);
              break e;
            } else
              for (ta = li(r.stateNode.containerInfo.firstChild), Sa = r, un = !0, ja = null, l = Lv(r, null, o, l), r.child = l; l; )
                l.flags = l.flags & -3 | 4096, l = l.sibling;
          else {
            if (gn(), o === c) {
              r = Ln(n, r, l);
              break e;
            }
            On(n, r, o, l);
          }
          r = r.child;
        }
        return r;
      case 5:
        return Uv(r), n === null && mc(r), o = r.type, c = r.pendingProps, d = n !== null ? n.memoizedProps : null, m = c.children, us(o, c) ? m = null : d !== null && us(o, d) && (r.flags |= 32), pu(n, r), On(n, r, m, l), r.child;
      case 6:
        return n === null && mc(r), null;
      case 13:
        return Qv(n, r, l);
      case 4:
        return Cd(r, r.stateNode.containerInfo), o = r.pendingProps, n === null ? r.child = Ju(r, null, o, l) : On(n, r, o, l), r.child;
      case 11:
        return o = r.type, c = r.pendingProps, c = r.elementType === o ? c : ra(o, c), fo(n, r, o, c, l);
      case 7:
        return On(n, r, r.pendingProps, l), r.child;
      case 8:
        return On(n, r, r.pendingProps.children, l), r.child;
      case 12:
        return On(n, r, r.pendingProps.children, l), r.child;
      case 10:
        e: {
          if (o = r.type._context, c = r.pendingProps, d = r.memoizedProps, m = c.value, $t(Yi, o._currentValue), o._currentValue = m, d !== null)
            if (Ma(d.value, m)) {
              if (d.children === c.children && !Tn.current) {
                r = Ln(n, r, l);
                break e;
              }
            } else
              for (d = r.child, d !== null && (d.return = r); d !== null; ) {
                var E = d.dependencies;
                if (E !== null) {
                  m = d.child;
                  for (var T = E.firstContext; T !== null; ) {
                    if (T.context === o) {
                      if (d.tag === 1) {
                        T = na(-1, l & -l), T.tag = 2;
                        var U = d.updateQueue;
                        if (U !== null) {
                          U = U.shared;
                          var W = U.pending;
                          W === null ? T.next = T : (T.next = W.next, W.next = T), U.pending = T;
                        }
                      }
                      d.lanes |= l, T = d.alternate, T !== null && (T.lanes |= l), Ed(
                        d.return,
                        l,
                        r
                      ), E.lanes |= l;
                      break;
                    }
                    T = T.next;
                  }
                } else if (d.tag === 10)
                  m = d.type === r.type ? null : d.child;
                else if (d.tag === 18) {
                  if (m = d.return, m === null)
                    throw Error(k(341));
                  m.lanes |= l, E = m.alternate, E !== null && (E.lanes |= l), Ed(m, l, r), m = d.sibling;
                } else
                  m = d.child;
                if (m !== null)
                  m.return = d;
                else
                  for (m = d; m !== null; ) {
                    if (m === r) {
                      m = null;
                      break;
                    }
                    if (d = m.sibling, d !== null) {
                      d.return = m.return, m = d;
                      break;
                    }
                    m = m.return;
                  }
                d = m;
              }
          On(n, r, c.children, l), r = r.child;
        }
        return r;
      case 9:
        return c = r.type, o = r.pendingProps.children, eo(r, l), c = Ha(c), o = o(c), r.flags |= 1, On(n, r, o, l), r.child;
      case 14:
        return o = r.type, c = ra(o, r.pendingProps), c = ra(o.type, c), Ll(n, r, o, c, l);
      case 15:
        return Pc(n, r, r.type, r.pendingProps, l);
      case 17:
        return o = r.type, c = r.pendingProps, c = r.elementType === o ? c : ra(o, c), Ts(n, r), r.tag = 1, cn(o) ? (n = !0, pc(r)) : n = !1, eo(r, l), Fv(r, o, c), bd(r, o, c, l), Bc(null, r, o, !0, n, l);
      case 19:
        return Od(n, r, l);
      case 22:
        return ia(n, r, l);
    }
    throw Error(k(156, r.tag));
  };
  function ih(n, r) {
    return Xt(n, r);
  }
  function lh(n, r, l, o) {
    this.tag = n, this.key = l, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.ref = null, this.pendingProps = r, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = o, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
  }
  function Ia(n, r, l, o) {
    return new lh(n, r, l, o);
  }
  function Pd(n) {
    return n = n.prototype, !(!n || !n.isReactComponent);
  }
  function gy(n) {
    if (typeof n == "function")
      return Pd(n) ? 1 : 0;
    if (n != null) {
      if (n = n.$$typeof, n === Cn)
        return 11;
      if (n === Ft)
        return 14;
    }
    return 2;
  }
  function zl(n, r) {
    var l = n.alternate;
    return l === null ? (l = Ia(n.tag, r, n.key, n.mode), l.elementType = n.elementType, l.type = n.type, l.stateNode = n.stateNode, l.alternate = n, n.alternate = l) : (l.pendingProps = r, l.type = n.type, l.flags = 0, l.subtreeFlags = 0, l.deletions = null), l.flags = n.flags & 14680064, l.childLanes = n.childLanes, l.lanes = n.lanes, l.child = n.child, l.memoizedProps = n.memoizedProps, l.memoizedState = n.memoizedState, l.updateQueue = n.updateQueue, r = n.dependencies, l.dependencies = r === null ? null : { lanes: r.lanes, firstContext: r.firstContext }, l.sibling = n.sibling, l.index = n.index, l.ref = n.ref, l;
  }
  function af(n, r, l, o, c, d) {
    var m = 2;
    if (o = n, typeof n == "function")
      Pd(n) && (m = 1);
    else if (typeof n == "string")
      m = 5;
    else
      e:
        switch (n) {
          case Ve:
            return Eu(l.children, c, d, r);
          case rn:
            m = 8, c |= 8;
            break;
          case _n:
            return n = Ia(12, l, r, c | 2), n.elementType = _n, n.lanes = d, n;
          case ze:
            return n = Ia(13, l, r, c), n.elementType = ze, n.lanes = d, n;
          case Je:
            return n = Ia(19, l, r, c), n.elementType = Je, n.lanes = d, n;
          case me:
            return lf(l, c, d, r);
          default:
            if (typeof n == "object" && n !== null)
              switch (n.$$typeof) {
                case Wt:
                  m = 10;
                  break e;
                case Ot:
                  m = 9;
                  break e;
                case Cn:
                  m = 11;
                  break e;
                case Ft:
                  m = 14;
                  break e;
                case _t:
                  m = 16, o = null;
                  break e;
              }
            throw Error(k(130, n == null ? n : typeof n, ""));
        }
    return r = Ia(m, l, r, c), r.elementType = n, r.type = o, r.lanes = d, r;
  }
  function Eu(n, r, l, o) {
    return n = Ia(7, n, o, r), n.lanes = l, n;
  }
  function lf(n, r, l, o) {
    return n = Ia(22, n, o, r), n.elementType = me, n.lanes = l, n.stateNode = { isHidden: !1 }, n;
  }
  function uf(n, r, l) {
    return n = Ia(6, n, null, r), n.lanes = l, n;
  }
  function Ds(n, r, l) {
    return r = Ia(4, n.children !== null ? n.children : [], n.key, r), r.lanes = l, r.stateNode = { containerInfo: n.containerInfo, pendingChildren: null, implementation: n.implementation }, r;
  }
  function Os(n, r, l, o, c) {
    this.tag = r, this.containerInfo = n, this.finishedWork = this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.pendingContext = this.context = null, this.callbackPriority = 0, this.eventTimes = ju(0), this.expirationTimes = ju(-1), this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = ju(0), this.identifierPrefix = o, this.onRecoverableError = c, this.mutableSourceEagerHydrationData = null;
  }
  function Bd(n, r, l, o, c, d, m, E, T) {
    return n = new Os(n, r, l, E, T), r === 1 ? (r = 1, d === !0 && (r |= 8)) : r = 0, d = Ia(3, null, null, r), n.current = d, d.stateNode = n, d.memoizedState = { element: o, isDehydrated: l, cache: null, transitions: null, pendingSuspenseBoundaries: null }, Ec(d), n;
  }
  function uh(n, r, l) {
    var o = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
    return { $$typeof: ft, key: o == null ? null : "" + o, children: n, containerInfo: r, implementation: l };
  }
  function $d(n) {
    if (!n)
      return Si;
    n = n._reactInternals;
    e: {
      if (Te(n) !== n || n.tag !== 1)
        throw Error(k(170));
      var r = n;
      do {
        switch (r.tag) {
          case 3:
            r = r.stateNode.context;
            break e;
          case 1:
            if (cn(r.type)) {
              r = r.stateNode.__reactInternalMemoizedMergedChildContext;
              break e;
            }
        }
        r = r.return;
      } while (r !== null);
      throw Error(k(171));
    }
    if (n.tag === 1) {
      var l = n.type;
      if (cn(l))
        return cs(n, l, r);
    }
    return r;
  }
  function Yd(n, r, l, o, c, d, m, E, T) {
    return n = Bd(l, o, !0, n, c, d, m, E, T), n.context = $d(null), l = n.current, o = tr(), c = qi(l), d = na(o, c), d.callback = r ?? null, kl(l, d, c), n.current.lanes = c, Ni(n, c, o), Yn(n, o), n;
  }
  function of(n, r, l, o) {
    var c = r.current, d = tr(), m = qi(c);
    return l = $d(l), r.context === null ? r.context = l : r.pendingContext = l, r = na(d, m), r.payload = { element: n }, o = o === void 0 ? null : o, o !== null && (r.callback = o), n = kl(c, r, m), n !== null && (Sn(n, c, m, d), Cc(n, c, m)), m;
  }
  function Ls(n) {
    if (n = n.current, !n.child)
      return null;
    switch (n.child.tag) {
      case 5:
        return n.child.stateNode;
      default:
        return n.child.stateNode;
    }
  }
  function oh(n, r) {
    if (n = n.memoizedState, n !== null && n.dehydrated !== null) {
      var l = n.retryLane;
      n.retryLane = l !== 0 && l < r ? l : r;
    }
  }
  function Id(n, r) {
    oh(n, r), (n = n.alternate) && oh(n, r);
  }
  function Sy() {
    return null;
  }
  var Qd = typeof reportError == "function" ? reportError : function(n) {
    console.error(n);
  };
  function sf(n) {
    this._internalRoot = n;
  }
  Ms.prototype.render = sf.prototype.render = function(n) {
    var r = this._internalRoot;
    if (r === null)
      throw Error(k(409));
    of(n, r, null, null);
  }, Ms.prototype.unmount = sf.prototype.unmount = function() {
    var n = this._internalRoot;
    if (n !== null) {
      this._internalRoot = null;
      var r = n.containerInfo;
      xi(function() {
        of(null, n, null, null);
      }), r[Bi] = null;
    }
  };
  function Ms(n) {
    this._internalRoot = n;
  }
  Ms.prototype.unstable_scheduleHydration = function(n) {
    if (n) {
      var r = Vu();
      n = { blockedOn: null, target: n, priority: r };
      for (var l = 0; l < Bt.length && r !== 0 && r < Bt[l].priority; l++)
        ;
      Bt.splice(l, 0, n), l === 0 && ec(n);
    }
  };
  function Ul(n) {
    return !(!n || n.nodeType !== 1 && n.nodeType !== 9 && n.nodeType !== 11);
  }
  function cf(n) {
    return !(!n || n.nodeType !== 1 && n.nodeType !== 9 && n.nodeType !== 11 && (n.nodeType !== 8 || n.nodeValue !== " react-mount-point-unstable "));
  }
  function sh() {
  }
  function Ey(n, r, l, o, c) {
    if (c) {
      if (typeof o == "function") {
        var d = o;
        o = function() {
          var U = Ls(m);
          d.call(U);
        };
      }
      var m = Yd(r, o, n, 0, null, !1, !1, "", sh);
      return n._reactRootContainer = m, n[Bi] = m.current, Xu(n.nodeType === 8 ? n.parentNode : n), xi(), m;
    }
    for (; c = n.lastChild; )
      n.removeChild(c);
    if (typeof o == "function") {
      var E = o;
      o = function() {
        var U = Ls(T);
        E.call(U);
      };
    }
    var T = Bd(n, 0, !1, null, null, !1, !1, "", sh);
    return n._reactRootContainer = T, n[Bi] = T.current, Xu(n.nodeType === 8 ? n.parentNode : n), xi(function() {
      of(r, T, l, o);
    }), T;
  }
  function ff(n, r, l, o, c) {
    var d = l._reactRootContainer;
    if (d) {
      var m = d;
      if (typeof c == "function") {
        var E = c;
        c = function() {
          var T = Ls(m);
          E.call(T);
        };
      }
      of(r, m, n, c);
    } else
      m = Ey(l, r, n, c, o);
    return Ls(m);
  }
  Gl = function(n) {
    switch (n.tag) {
      case 3:
        var r = n.stateNode;
        if (r.current.memoizedState.isDehydrated) {
          var l = ti(r.pendingLanes);
          l !== 0 && (mi(r, l | 1), Yn(r, Lt()), !(yt & 6) && (xo = Lt() + 500, Zr()));
        }
        break;
      case 13:
        xi(function() {
          var o = Ii(n, 1);
          if (o !== null) {
            var c = tr();
            Sn(o, n, 1, c);
          }
        }), Id(n, 1);
    }
  }, Hu = function(n) {
    if (n.tag === 13) {
      var r = Ii(n, 134217728);
      if (r !== null) {
        var l = tr();
        Sn(r, n, 134217728, l);
      }
      Id(n, 134217728);
    }
  }, Ct = function(n) {
    if (n.tag === 13) {
      var r = qi(n), l = Ii(n, r);
      if (l !== null) {
        var o = tr();
        Sn(l, n, r, o);
      }
      Id(n, r);
    }
  }, Vu = function() {
    return Mt;
  }, Pu = function(n, r) {
    var l = Mt;
    try {
      return Mt = n, r();
    } finally {
      Mt = l;
    }
  }, br = function(n, r, l) {
    switch (r) {
      case "input":
        if (kn(n, l), r = l.name, l.type === "radio" && r != null) {
          for (l = n; l.parentNode; )
            l = l.parentNode;
          for (l = l.querySelectorAll("input[name=" + JSON.stringify("" + r) + '][type="radio"]'), r = 0; r < l.length; r++) {
            var o = l[r];
            if (o !== n && o.form === n.form) {
              var c = Le(o);
              if (!c)
                throw Error(k(90));
              Br(o), kn(o, c);
            }
          }
        }
        break;
      case "textarea":
        da(n, l);
        break;
      case "select":
        r = l.value, r != null && mr(n, !!l.multiple, r, !1);
    }
  }, Wl = Hd, Nu = xi;
  var Cy = { usingClientEntryPoint: !1, Events: [ss, Ku, Le, ka, ol, Hd] }, Ns = { findFiberByHostInstance: Na, bundleType: 0, version: "18.3.1", rendererPackageName: "react-dom" }, ch = { bundleType: Ns.bundleType, version: Ns.version, rendererPackageName: Ns.rendererPackageName, rendererConfig: Ns.rendererConfig, overrideHookState: null, overrideHookStateDeletePath: null, overrideHookStateRenamePath: null, overrideProps: null, overridePropsDeletePath: null, overridePropsRenamePath: null, setErrorHandler: null, setSuspenseHandler: null, scheduleUpdate: null, currentDispatcherRef: mt.ReactCurrentDispatcher, findHostInstanceByFiber: function(n) {
    return n = it(n), n === null ? null : n.stateNode;
  }, findFiberByHostInstance: Ns.findFiberByHostInstance || Sy, findHostInstancesForRefresh: null, scheduleRefresh: null, scheduleRoot: null, setRefreshHandler: null, getCurrentFiber: null, reconcilerVersion: "18.3.1-next-f1338f8080-20240426" };
  if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u") {
    var df = __REACT_DEVTOOLS_GLOBAL_HOOK__;
    if (!df.isDisabled && df.supportsFiber)
      try {
        fl = df.inject(ch), Wr = df;
      } catch {
      }
  }
  return Ka.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = Cy, Ka.createPortal = function(n, r) {
    var l = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
    if (!Ul(r))
      throw Error(k(200));
    return uh(n, r, null, l);
  }, Ka.createRoot = function(n, r) {
    if (!Ul(n))
      throw Error(k(299));
    var l = !1, o = "", c = Qd;
    return r != null && (r.unstable_strictMode === !0 && (l = !0), r.identifierPrefix !== void 0 && (o = r.identifierPrefix), r.onRecoverableError !== void 0 && (c = r.onRecoverableError)), r = Bd(n, 1, !1, null, null, l, !1, o, c), n[Bi] = r.current, Xu(n.nodeType === 8 ? n.parentNode : n), new sf(r);
  }, Ka.findDOMNode = function(n) {
    if (n == null)
      return null;
    if (n.nodeType === 1)
      return n;
    var r = n._reactInternals;
    if (r === void 0)
      throw typeof n.render == "function" ? Error(k(188)) : (n = Object.keys(n).join(","), Error(k(268, n)));
    return n = it(r), n = n === null ? null : n.stateNode, n;
  }, Ka.flushSync = function(n) {
    return xi(n);
  }, Ka.hydrate = function(n, r, l) {
    if (!cf(r))
      throw Error(k(200));
    return ff(null, n, r, !0, l);
  }, Ka.hydrateRoot = function(n, r, l) {
    if (!Ul(n))
      throw Error(k(405));
    var o = l != null && l.hydratedSources || null, c = !1, d = "", m = Qd;
    if (l != null && (l.unstable_strictMode === !0 && (c = !0), l.identifierPrefix !== void 0 && (d = l.identifierPrefix), l.onRecoverableError !== void 0 && (m = l.onRecoverableError)), r = Yd(r, null, n, 1, l ?? null, c, !1, d, m), n[Bi] = r.current, Xu(n), o)
      for (n = 0; n < o.length; n++)
        l = o[n], c = l._getVersion, c = c(l._source), r.mutableSourceEagerHydrationData == null ? r.mutableSourceEagerHydrationData = [l, c] : r.mutableSourceEagerHydrationData.push(
          l,
          c
        );
    return new Ms(r);
  }, Ka.render = function(n, r, l) {
    if (!cf(r))
      throw Error(k(200));
    return ff(null, n, r, !1, l);
  }, Ka.unmountComponentAtNode = function(n) {
    if (!cf(n))
      throw Error(k(40));
    return n._reactRootContainer ? (xi(function() {
      ff(null, null, n, !1, function() {
        n._reactRootContainer = null, n[Bi] = null;
      });
    }), !0) : !1;
  }, Ka.unstable_batchedUpdates = Hd, Ka.unstable_renderSubtreeIntoContainer = function(n, r, l, o) {
    if (!cf(l))
      throw Error(k(200));
    if (n == null || n._reactInternals === void 0)
      throw Error(k(38));
    return ff(n, r, l, !1, o);
  }, Ka.version = "18.3.1-next-f1338f8080-20240426", Ka;
}
var Za = {};
/**
 * @license React
 * react-dom.development.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var uR;
function sk() {
  return uR || (uR = 1, process.env.NODE_ENV !== "production" && function() {
    typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart(new Error());
    var Q = Ql, B = oR(), k = Q.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, Ze = !1;
    function Dt(e) {
      Ze = e;
    }
    function $e(e) {
      if (!Ze) {
        for (var t = arguments.length, a = new Array(t > 1 ? t - 1 : 0), i = 1; i < t; i++)
          a[i - 1] = arguments[i];
        ut("warn", e, a);
      }
    }
    function S(e) {
      if (!Ze) {
        for (var t = arguments.length, a = new Array(t > 1 ? t - 1 : 0), i = 1; i < t; i++)
          a[i - 1] = arguments[i];
        ut("error", e, a);
      }
    }
    function ut(e, t, a) {
      {
        var i = k.ReactDebugCurrentFrame, u = i.getStackAddendum();
        u !== "" && (t += "%s", a = a.concat([u]));
        var s = a.map(function(f) {
          return String(f);
        });
        s.unshift("Warning: " + t), Function.prototype.apply.call(console[e], console, s);
      }
    }
    var de = 0, se = 1, nt = 2, re = 3, pe = 4, ue = 5, Ye = 6, bt = 7, ht = 8, pn = 9, ot = 10, qe = 11, mt = 12, Oe = 13, ft = 14, Ve = 15, rn = 16, _n = 17, Wt = 18, Ot = 19, Cn = 21, ze = 22, Je = 23, Ft = 24, _t = 25, me = !0, J = !1, be = !1, ae = !1, _ = !1, V = !0, Ue = !1, Pe = !0, rt = !0, tt = !0, St = !0, st = /* @__PURE__ */ new Set(), ct = {}, en = {};
    function hr(e, t) {
      Br(e, t), Br(e + "Capture", t);
    }
    function Br(e, t) {
      ct[e] && S("EventRegistry: More than one plugin attempted to publish the same registration name, `%s`.", e), ct[e] = t;
      {
        var a = e.toLowerCase();
        en[a] = e, e === "onDoubleClick" && (en.ondblclick = e);
      }
      for (var i = 0; i < t.length; i++)
        st.add(t[i]);
    }
    var vn = typeof window < "u" && typeof window.document < "u" && typeof window.document.createElement < "u", Wn = Object.prototype.hasOwnProperty;
    function Vn(e) {
      {
        var t = typeof Symbol == "function" && Symbol.toStringTag, a = t && e[Symbol.toStringTag] || e.constructor.name || "Object";
        return a;
      }
    }
    function zn(e) {
      try {
        return kn(e), !1;
      } catch {
        return !0;
      }
    }
    function kn(e) {
      return "" + e;
    }
    function $r(e, t) {
      if (zn(e))
        return S("The provided `%s` attribute is an unsupported type %s. This value must be coerced to a string before before using it here.", t, Vn(e)), kn(e);
    }
    function Yr(e) {
      if (zn(e))
        return S("The provided key is an unsupported type %s. This value must be coerced to a string before before using it here.", Vn(e)), kn(e);
    }
    function Gn(e, t) {
      if (zn(e))
        return S("The provided `%s` prop is an unsupported type %s. This value must be coerced to a string before before using it here.", t, Vn(e)), kn(e);
    }
    function mr(e, t) {
      if (zn(e))
        return S("The provided `%s` CSS property is an unsupported type %s. This value must be coerced to a string before before using it here.", t, Vn(e)), kn(e);
    }
    function Ir(e) {
      if (zn(e))
        return S("The provided HTML markup uses a value of unsupported type %s. This value must be coerced to a string before before using it here.", Vn(e)), kn(e);
    }
    function yr(e) {
      if (zn(e))
        return S("Form field values (value, checked, defaultValue, or defaultChecked props) must be strings, not %s. This value must be coerced to a string before before using it here.", Vn(e)), kn(e);
    }
    var da = 0, rr = 1, Qr = 2, hn = 3, wr = 4, fi = 5, pa = 6, ee = ":A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD", _e = ee + "\\-.0-9\\u00B7\\u0300-\\u036F\\u203F-\\u2040", at = new RegExp("^[" + ee + "][" + _e + "]*$"), At = {}, Ht = {};
    function Dn(e) {
      return Wn.call(Ht, e) ? !0 : Wn.call(At, e) ? !1 : at.test(e) ? (Ht[e] = !0, !0) : (At[e] = !0, S("Invalid attribute name: `%s`", e), !1);
    }
    function mn(e, t, a) {
      return t !== null ? t.type === da : a ? !1 : e.length > 2 && (e[0] === "o" || e[0] === "O") && (e[1] === "n" || e[1] === "N");
    }
    function gr(e, t, a, i) {
      if (a !== null && a.type === da)
        return !1;
      switch (typeof t) {
        case "function":
        case "symbol":
          return !0;
        case "boolean": {
          if (i)
            return !1;
          if (a !== null)
            return !a.acceptsBooleans;
          var u = e.toLowerCase().slice(0, 5);
          return u !== "data-" && u !== "aria-";
        }
        default:
          return !1;
      }
    }
    function It(e, t, a, i) {
      if (t === null || typeof t > "u" || gr(e, t, a, i))
        return !0;
      if (i)
        return !1;
      if (a !== null)
        switch (a.type) {
          case hn:
            return !t;
          case wr:
            return t === !1;
          case fi:
            return isNaN(t);
          case pa:
            return isNaN(t) || t < 1;
        }
      return !1;
    }
    function br(e) {
      return Pt.hasOwnProperty(e) ? Pt[e] : null;
    }
    function Vt(e, t, a, i, u, s, f) {
      this.acceptsBooleans = t === Qr || t === hn || t === wr, this.attributeName = i, this.attributeNamespace = u, this.mustUseProperty = a, this.propertyName = e, this.type = t, this.sanitizeURL = s, this.removeEmptyString = f;
    }
    var Pt = {}, Ja = [
      "children",
      "dangerouslySetInnerHTML",
      // TODO: This prevents the assignment of defaultValue to regular
      // elements (not just inputs). Now that ReactDOMInput assigns to the
      // defaultValue property -- do we need this?
      "defaultValue",
      "defaultChecked",
      "innerHTML",
      "suppressContentEditableWarning",
      "suppressHydrationWarning",
      "style"
    ];
    Ja.forEach(function(e) {
      Pt[e] = new Vt(
        e,
        da,
        !1,
        // mustUseProperty
        e,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [["acceptCharset", "accept-charset"], ["className", "class"], ["htmlFor", "for"], ["httpEquiv", "http-equiv"]].forEach(function(e) {
      var t = e[0], a = e[1];
      Pt[t] = new Vt(
        t,
        rr,
        !1,
        // mustUseProperty
        a,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), ["contentEditable", "draggable", "spellCheck", "value"].forEach(function(e) {
      Pt[e] = new Vt(
        e,
        Qr,
        !1,
        // mustUseProperty
        e.toLowerCase(),
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), ["autoReverse", "externalResourcesRequired", "focusable", "preserveAlpha"].forEach(function(e) {
      Pt[e] = new Vt(
        e,
        Qr,
        !1,
        // mustUseProperty
        e,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "allowFullScreen",
      "async",
      // Note: there is a special case that prevents it from being written to the DOM
      // on the client side because the browsers are inconsistent. Instead we call focus().
      "autoFocus",
      "autoPlay",
      "controls",
      "default",
      "defer",
      "disabled",
      "disablePictureInPicture",
      "disableRemotePlayback",
      "formNoValidate",
      "hidden",
      "loop",
      "noModule",
      "noValidate",
      "open",
      "playsInline",
      "readOnly",
      "required",
      "reversed",
      "scoped",
      "seamless",
      // Microdata
      "itemScope"
    ].forEach(function(e) {
      Pt[e] = new Vt(
        e,
        hn,
        !1,
        // mustUseProperty
        e.toLowerCase(),
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "checked",
      // Note: `option.selected` is not updated if `select.multiple` is
      // disabled with `removeAttribute`. We have special logic for handling this.
      "multiple",
      "muted",
      "selected"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      Pt[e] = new Vt(
        e,
        hn,
        !0,
        // mustUseProperty
        e,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "capture",
      "download"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      Pt[e] = new Vt(
        e,
        wr,
        !1,
        // mustUseProperty
        e,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "cols",
      "rows",
      "size",
      "span"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      Pt[e] = new Vt(
        e,
        pa,
        !1,
        // mustUseProperty
        e,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), ["rowSpan", "start"].forEach(function(e) {
      Pt[e] = new Vt(
        e,
        fi,
        !1,
        // mustUseProperty
        e.toLowerCase(),
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    });
    var ka = /[\-\:]([a-z])/g, ol = function(e) {
      return e[1].toUpperCase();
    };
    [
      "accent-height",
      "alignment-baseline",
      "arabic-form",
      "baseline-shift",
      "cap-height",
      "clip-path",
      "clip-rule",
      "color-interpolation",
      "color-interpolation-filters",
      "color-profile",
      "color-rendering",
      "dominant-baseline",
      "enable-background",
      "fill-opacity",
      "fill-rule",
      "flood-color",
      "flood-opacity",
      "font-family",
      "font-size",
      "font-size-adjust",
      "font-stretch",
      "font-style",
      "font-variant",
      "font-weight",
      "glyph-name",
      "glyph-orientation-horizontal",
      "glyph-orientation-vertical",
      "horiz-adv-x",
      "horiz-origin-x",
      "image-rendering",
      "letter-spacing",
      "lighting-color",
      "marker-end",
      "marker-mid",
      "marker-start",
      "overline-position",
      "overline-thickness",
      "paint-order",
      "panose-1",
      "pointer-events",
      "rendering-intent",
      "shape-rendering",
      "stop-color",
      "stop-opacity",
      "strikethrough-position",
      "strikethrough-thickness",
      "stroke-dasharray",
      "stroke-dashoffset",
      "stroke-linecap",
      "stroke-linejoin",
      "stroke-miterlimit",
      "stroke-opacity",
      "stroke-width",
      "text-anchor",
      "text-decoration",
      "text-rendering",
      "underline-position",
      "underline-thickness",
      "unicode-bidi",
      "unicode-range",
      "units-per-em",
      "v-alphabetic",
      "v-hanging",
      "v-ideographic",
      "v-mathematical",
      "vector-effect",
      "vert-adv-y",
      "vert-origin-x",
      "vert-origin-y",
      "word-spacing",
      "writing-mode",
      "xmlns:xlink",
      "x-height"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      var t = e.replace(ka, ol);
      Pt[t] = new Vt(
        t,
        rr,
        !1,
        // mustUseProperty
        e,
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "xlink:actuate",
      "xlink:arcrole",
      "xlink:role",
      "xlink:show",
      "xlink:title",
      "xlink:type"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      var t = e.replace(ka, ol);
      Pt[t] = new Vt(
        t,
        rr,
        !1,
        // mustUseProperty
        e,
        "http://www.w3.org/1999/xlink",
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "xml:base",
      "xml:lang",
      "xml:space"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      var t = e.replace(ka, ol);
      Pt[t] = new Vt(
        t,
        rr,
        !1,
        // mustUseProperty
        e,
        "http://www.w3.org/XML/1998/namespace",
        !1,
        // sanitizeURL
        !1
      );
    }), ["tabIndex", "crossOrigin"].forEach(function(e) {
      Pt[e] = new Vt(
        e,
        rr,
        !1,
        // mustUseProperty
        e.toLowerCase(),
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    });
    var Wl = "xlinkHref";
    Pt[Wl] = new Vt(
      "xlinkHref",
      rr,
      !1,
      // mustUseProperty
      "xlink:href",
      "http://www.w3.org/1999/xlink",
      !0,
      // sanitizeURL
      !1
    ), ["src", "href", "action", "formAction"].forEach(function(e) {
      Pt[e] = new Vt(
        e,
        rr,
        !1,
        // mustUseProperty
        e.toLowerCase(),
        // attributeName
        null,
        // attributeNamespace
        !0,
        // sanitizeURL
        !0
      );
    });
    var Nu = /^[\u0000-\u001F ]*j[\r\n\t]*a[\r\n\t]*v[\r\n\t]*a[\r\n\t]*s[\r\n\t]*c[\r\n\t]*r[\r\n\t]*i[\r\n\t]*p[\r\n\t]*t[\r\n\t]*\:/i, Mi = !1;
    function sl(e) {
      !Mi && Nu.test(e) && (Mi = !0, S("A future version of React will block javascript: URLs as a security precaution. Use event handlers instead if you can. If you need to generate unsafe HTML try using dangerouslySetInnerHTML instead. React was passed %s.", JSON.stringify(e)));
    }
    function va(e, t, a, i) {
      if (i.mustUseProperty) {
        var u = i.propertyName;
        return e[u];
      } else {
        $r(a, t), i.sanitizeURL && sl("" + a);
        var s = i.attributeName, f = null;
        if (i.type === wr) {
          if (e.hasAttribute(s)) {
            var p = e.getAttribute(s);
            return p === "" ? !0 : It(t, a, i, !1) ? p : p === "" + a ? a : p;
          }
        } else if (e.hasAttribute(s)) {
          if (It(t, a, i, !1))
            return e.getAttribute(s);
          if (i.type === hn)
            return a;
          f = e.getAttribute(s);
        }
        return It(t, a, i, !1) ? f === null ? a : f : f === "" + a ? a : f;
      }
    }
    function di(e, t, a, i) {
      {
        if (!Dn(t))
          return;
        if (!e.hasAttribute(t))
          return a === void 0 ? void 0 : null;
        var u = e.getAttribute(t);
        return $r(a, t), u === "" + a ? a : u;
      }
    }
    function ha(e, t, a, i) {
      var u = br(t);
      if (!mn(t, u, i)) {
        if (It(t, a, u, i) && (a = null), i || u === null) {
          if (Dn(t)) {
            var s = t;
            a === null ? e.removeAttribute(s) : ($r(a, t), e.setAttribute(s, "" + a));
          }
          return;
        }
        var f = u.mustUseProperty;
        if (f) {
          var p = u.propertyName;
          if (a === null) {
            var v = u.type;
            e[p] = v === hn ? !1 : "";
          } else
            e[p] = a;
          return;
        }
        var y = u.attributeName, g = u.attributeNamespace;
        if (a === null)
          e.removeAttribute(y);
        else {
          var b = u.type, x;
          b === hn || b === wr && a === !0 ? x = "" : ($r(a, y), x = "" + a, u.sanitizeURL && sl(x.toString())), g ? e.setAttributeNS(g, y, x) : e.setAttribute(y, x);
        }
      }
    }
    var ei = Symbol.for("react.element"), _r = Symbol.for("react.portal"), ma = Symbol.for("react.fragment"), pi = Symbol.for("react.strict_mode"), vi = Symbol.for("react.profiler"), R = Symbol.for("react.provider"), Y = Symbol.for("react.context"), q = Symbol.for("react.forward_ref"), Te = Symbol.for("react.suspense"), dt = Symbol.for("react.suspense_list"), Et = Symbol.for("react.memo"), Ae = Symbol.for("react.lazy"), it = Symbol.for("react.scope"), Un = Symbol.for("react.debug_trace_mode"), Xt = Symbol.for("react.offscreen"), an = Symbol.for("react.legacy_hidden"), Sr = Symbol.for("react.cache"), hi = Symbol.for("react.tracing_marker"), Lt = Symbol.iterator, qn = "@@iterator";
    function kr(e) {
      if (e === null || typeof e != "object")
        return null;
      var t = Lt && e[Lt] || e[qn];
      return typeof t == "function" ? t : null;
    }
    var lt = Object.assign, Da = 0, cl, zu, fl, Wr, Qo, Dr, Wo;
    function Go() {
    }
    Go.__reactDisabledLog = !0;
    function Zs() {
      {
        if (Da === 0) {
          cl = console.log, zu = console.info, fl = console.warn, Wr = console.error, Qo = console.group, Dr = console.groupCollapsed, Wo = console.groupEnd;
          var e = {
            configurable: !0,
            enumerable: !0,
            value: Go,
            writable: !0
          };
          Object.defineProperties(console, {
            info: e,
            log: e,
            warn: e,
            error: e,
            group: e,
            groupCollapsed: e,
            groupEnd: e
          });
        }
        Da++;
      }
    }
    function Uu() {
      {
        if (Da--, Da === 0) {
          var e = {
            configurable: !0,
            enumerable: !0,
            writable: !0
          };
          Object.defineProperties(console, {
            log: lt({}, e, {
              value: cl
            }),
            info: lt({}, e, {
              value: zu
            }),
            warn: lt({}, e, {
              value: fl
            }),
            error: lt({}, e, {
              value: Wr
            }),
            group: lt({}, e, {
              value: Qo
            }),
            groupCollapsed: lt({}, e, {
              value: Dr
            }),
            groupEnd: lt({}, e, {
              value: Wo
            })
          });
        }
        Da < 0 && S("disabledDepth fell below zero. This is a bug in React. Please file an issue.");
      }
    }
    var dl = k.ReactCurrentDispatcher, ti;
    function Or(e, t, a) {
      {
        if (ti === void 0)
          try {
            throw Error();
          } catch (u) {
            var i = u.stack.trim().match(/\n( *(at )?)/);
            ti = i && i[1] || "";
          }
        return `
` + ti + e;
      }
    }
    var pl = !1, vl;
    {
      var hl = typeof WeakMap == "function" ? WeakMap : Map;
      vl = new hl();
    }
    function Au(e, t) {
      if (!e || pl)
        return "";
      {
        var a = vl.get(e);
        if (a !== void 0)
          return a;
      }
      var i;
      pl = !0;
      var u = Error.prepareStackTrace;
      Error.prepareStackTrace = void 0;
      var s;
      s = dl.current, dl.current = null, Zs();
      try {
        if (t) {
          var f = function() {
            throw Error();
          };
          if (Object.defineProperty(f.prototype, "props", {
            set: function() {
              throw Error();
            }
          }), typeof Reflect == "object" && Reflect.construct) {
            try {
              Reflect.construct(f, []);
            } catch (A) {
              i = A;
            }
            Reflect.construct(e, [], f);
          } else {
            try {
              f.call();
            } catch (A) {
              i = A;
            }
            e.call(f.prototype);
          }
        } else {
          try {
            throw Error();
          } catch (A) {
            i = A;
          }
          e();
        }
      } catch (A) {
        if (A && i && typeof A.stack == "string") {
          for (var p = A.stack.split(`
`), v = i.stack.split(`
`), y = p.length - 1, g = v.length - 1; y >= 1 && g >= 0 && p[y] !== v[g]; )
            g--;
          for (; y >= 1 && g >= 0; y--, g--)
            if (p[y] !== v[g]) {
              if (y !== 1 || g !== 1)
                do
                  if (y--, g--, g < 0 || p[y] !== v[g]) {
                    var b = `
` + p[y].replace(" at new ", " at ");
                    return e.displayName && b.includes("<anonymous>") && (b = b.replace("<anonymous>", e.displayName)), typeof e == "function" && vl.set(e, b), b;
                  }
                while (y >= 1 && g >= 0);
              break;
            }
        }
      } finally {
        pl = !1, dl.current = s, Uu(), Error.prepareStackTrace = u;
      }
      var x = e ? e.displayName || e.name : "", N = x ? Or(x) : "";
      return typeof e == "function" && vl.set(e, N), N;
    }
    function ju(e, t, a) {
      return Au(e, !0);
    }
    function Ni(e, t, a) {
      return Au(e, !1);
    }
    function $f(e) {
      var t = e.prototype;
      return !!(t && t.isReactComponent);
    }
    function mi(e, t, a) {
      if (e == null)
        return "";
      if (typeof e == "function")
        return Au(e, $f(e));
      if (typeof e == "string")
        return Or(e);
      switch (e) {
        case Te:
          return Or("Suspense");
        case dt:
          return Or("SuspenseList");
      }
      if (typeof e == "object")
        switch (e.$$typeof) {
          case q:
            return Ni(e.render);
          case Et:
            return mi(e.type, t, a);
          case Ae: {
            var i = e, u = i._payload, s = i._init;
            try {
              return mi(s(u), t, a);
            } catch {
            }
          }
        }
      return "";
    }
    function Mt(e) {
      switch (e._debugOwner && e._debugOwner.type, e._debugSource, e.tag) {
        case ue:
          return Or(e.type);
        case rn:
          return Or("Lazy");
        case Oe:
          return Or("Suspense");
        case Ot:
          return Or("SuspenseList");
        case de:
        case nt:
        case Ve:
          return Ni(e.type);
        case qe:
          return Ni(e.type.render);
        case se:
          return ju(e.type);
        default:
          return "";
      }
    }
    function Fu(e) {
      try {
        var t = "", a = e;
        do
          t += Mt(a), a = a.return;
        while (a);
        return t;
      } catch (i) {
        return `
Error generating stack: ` + i.message + `
` + i.stack;
      }
    }
    function Gl(e, t, a) {
      var i = e.displayName;
      if (i)
        return i;
      var u = t.displayName || t.name || "";
      return u !== "" ? a + "(" + u + ")" : a;
    }
    function Hu(e) {
      return e.displayName || "Context";
    }
    function Ct(e) {
      if (e == null)
        return null;
      if (typeof e.tag == "number" && S("Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue."), typeof e == "function")
        return e.displayName || e.name || null;
      if (typeof e == "string")
        return e;
      switch (e) {
        case ma:
          return "Fragment";
        case _r:
          return "Portal";
        case vi:
          return "Profiler";
        case pi:
          return "StrictMode";
        case Te:
          return "Suspense";
        case dt:
          return "SuspenseList";
      }
      if (typeof e == "object")
        switch (e.$$typeof) {
          case Y:
            var t = e;
            return Hu(t) + ".Consumer";
          case R:
            var a = e;
            return Hu(a._context) + ".Provider";
          case q:
            return Gl(e, e.render, "ForwardRef");
          case Et:
            var i = e.displayName || null;
            return i !== null ? i : Ct(e.type) || "Memo";
          case Ae: {
            var u = e, s = u._payload, f = u._init;
            try {
              return Ct(f(s));
            } catch {
              return null;
            }
          }
        }
      return null;
    }
    function Vu(e, t, a) {
      var i = t.displayName || t.name || "";
      return e.displayName || (i !== "" ? a + "(" + i + ")" : a);
    }
    function Pu(e) {
      return e.displayName || "Context";
    }
    function We(e) {
      var t = e.tag, a = e.type;
      switch (t) {
        case Ft:
          return "Cache";
        case pn:
          var i = a;
          return Pu(i) + ".Consumer";
        case ot:
          var u = a;
          return Pu(u._context) + ".Provider";
        case Wt:
          return "DehydratedFragment";
        case qe:
          return Vu(a, a.render, "ForwardRef");
        case bt:
          return "Fragment";
        case ue:
          return a;
        case pe:
          return "Portal";
        case re:
          return "Root";
        case Ye:
          return "Text";
        case rn:
          return Ct(a);
        case ht:
          return a === pi ? "StrictMode" : "Mode";
        case ze:
          return "Offscreen";
        case mt:
          return "Profiler";
        case Cn:
          return "Scope";
        case Oe:
          return "Suspense";
        case Ot:
          return "SuspenseList";
        case _t:
          return "TracingMarker";
        case se:
        case de:
        case _n:
        case nt:
        case ft:
        case Ve:
          if (typeof a == "function")
            return a.displayName || a.name || null;
          if (typeof a == "string")
            return a;
          break;
      }
      return null;
    }
    var ql = k.ReactDebugCurrentFrame, yn = null, Gr = !1;
    function Lr() {
      {
        if (yn === null)
          return null;
        var e = yn._debugOwner;
        if (e !== null && typeof e < "u")
          return We(e);
      }
      return null;
    }
    function ml() {
      return yn === null ? "" : Fu(yn);
    }
    function Rn() {
      ql.getCurrentStack = null, yn = null, Gr = !1;
    }
    function Bt(e) {
      ql.getCurrentStack = e === null ? null : ml, yn = e, Gr = !1;
    }
    function Js() {
      return yn;
    }
    function qr(e) {
      Gr = e;
    }
    function Xn(e) {
      return "" + e;
    }
    function yi(e) {
      switch (typeof e) {
        case "boolean":
        case "number":
        case "string":
        case "undefined":
          return e;
        case "object":
          return yr(e), e;
        default:
          return "";
      }
    }
    var ec = {
      button: !0,
      checkbox: !0,
      image: !0,
      hidden: !0,
      radio: !0,
      reset: !0,
      submit: !0
    };
    function zi(e, t) {
      ec[t.type] || t.onChange || t.onInput || t.readOnly || t.disabled || t.value == null || S("You provided a `value` prop to a form field without an `onChange` handler. This will render a read-only field. If the field should be mutable use `defaultValue`. Otherwise, set either `onChange` or `readOnly`."), t.onChange || t.readOnly || t.disabled || t.checked == null || S("You provided a `checked` prop to a form field without an `onChange` handler. This will render a read-only field. If the field should be mutable use `defaultChecked`. Otherwise, set either `onChange` or `readOnly`.");
    }
    function yl(e) {
      var t = e.type, a = e.nodeName;
      return a && a.toLowerCase() === "input" && (t === "checkbox" || t === "radio");
    }
    function tc(e) {
      return e._valueTracker;
    }
    function Oa(e) {
      e._valueTracker = null;
    }
    function gl(e) {
      var t = "";
      return e && (yl(e) ? t = e.checked ? "true" : "false" : t = e.value), t;
    }
    function Ui(e) {
      var t = yl(e) ? "checked" : "value", a = Object.getOwnPropertyDescriptor(e.constructor.prototype, t);
      yr(e[t]);
      var i = "" + e[t];
      if (!(e.hasOwnProperty(t) || typeof a > "u" || typeof a.get != "function" || typeof a.set != "function")) {
        var u = a.get, s = a.set;
        Object.defineProperty(e, t, {
          configurable: !0,
          get: function() {
            return u.call(this);
          },
          set: function(p) {
            yr(p), i = "" + p, s.call(this, p);
          }
        }), Object.defineProperty(e, t, {
          enumerable: a.enumerable
        });
        var f = {
          getValue: function() {
            return i;
          },
          setValue: function(p) {
            yr(p), i = "" + p;
          },
          stopTracking: function() {
            Oa(e), delete e[t];
          }
        };
        return f;
      }
    }
    function La(e) {
      tc(e) || (e._valueTracker = Ui(e));
    }
    function Bu(e) {
      if (!e)
        return !1;
      var t = tc(e);
      if (!t)
        return !0;
      var a = t.getValue(), i = gl(e);
      return i !== a ? (t.setValue(i), !0) : !1;
    }
    function Sl(e) {
      if (e = e || (typeof document < "u" ? document : void 0), typeof e > "u")
        return null;
      try {
        return e.activeElement || e.body;
      } catch {
        return e.body;
      }
    }
    var El = !1, Xl = !1, $u = !1, qo = !1;
    function ni(e) {
      var t = e.type === "checkbox" || e.type === "radio";
      return t ? e.checked != null : e.value != null;
    }
    function h(e, t) {
      var a = e, i = t.checked, u = lt({}, t, {
        defaultChecked: void 0,
        defaultValue: void 0,
        value: void 0,
        checked: i ?? a._wrapperState.initialChecked
      });
      return u;
    }
    function C(e, t) {
      zi("input", t), t.checked !== void 0 && t.defaultChecked !== void 0 && !Xl && (S("%s contains an input of type %s with both checked and defaultChecked props. Input elements must be either controlled or uncontrolled (specify either the checked prop, or the defaultChecked prop, but not both). Decide between using a controlled or uncontrolled input element and remove one of these props. More info: https://reactjs.org/link/controlled-components", Lr() || "A component", t.type), Xl = !0), t.value !== void 0 && t.defaultValue !== void 0 && !El && (S("%s contains an input of type %s with both value and defaultValue props. Input elements must be either controlled or uncontrolled (specify either the value prop, or the defaultValue prop, but not both). Decide between using a controlled or uncontrolled input element and remove one of these props. More info: https://reactjs.org/link/controlled-components", Lr() || "A component", t.type), El = !0);
      var a = e, i = t.defaultValue == null ? "" : t.defaultValue;
      a._wrapperState = {
        initialChecked: t.checked != null ? t.checked : t.defaultChecked,
        initialValue: yi(t.value != null ? t.value : i),
        controlled: ni(t)
      };
    }
    function z(e, t) {
      var a = e, i = t.checked;
      i != null && ha(a, "checked", i, !1);
    }
    function j(e, t) {
      var a = e;
      {
        var i = ni(t);
        !a._wrapperState.controlled && i && !qo && (S("A component is changing an uncontrolled input to be controlled. This is likely caused by the value changing from undefined to a defined value, which should not happen. Decide between using a controlled or uncontrolled input element for the lifetime of the component. More info: https://reactjs.org/link/controlled-components"), qo = !0), a._wrapperState.controlled && !i && !$u && (S("A component is changing a controlled input to be uncontrolled. This is likely caused by the value changing from a defined to undefined, which should not happen. Decide between using a controlled or uncontrolled input element for the lifetime of the component. More info: https://reactjs.org/link/controlled-components"), $u = !0);
      }
      z(e, t);
      var u = yi(t.value), s = t.type;
      if (u != null)
        s === "number" ? (u === 0 && a.value === "" || // We explicitly want to coerce to number here if possible.
        // eslint-disable-next-line
        a.value != u) && (a.value = Xn(u)) : a.value !== Xn(u) && (a.value = Xn(u));
      else if (s === "submit" || s === "reset") {
        a.removeAttribute("value");
        return;
      }
      t.hasOwnProperty("value") ? Ne(a, t.type, u) : t.hasOwnProperty("defaultValue") && Ne(a, t.type, yi(t.defaultValue)), t.checked == null && t.defaultChecked != null && (a.defaultChecked = !!t.defaultChecked);
    }
    function K(e, t, a) {
      var i = e;
      if (t.hasOwnProperty("value") || t.hasOwnProperty("defaultValue")) {
        var u = t.type, s = u === "submit" || u === "reset";
        if (s && (t.value === void 0 || t.value === null))
          return;
        var f = Xn(i._wrapperState.initialValue);
        a || f !== i.value && (i.value = f), i.defaultValue = f;
      }
      var p = i.name;
      p !== "" && (i.name = ""), i.defaultChecked = !i.defaultChecked, i.defaultChecked = !!i._wrapperState.initialChecked, p !== "" && (i.name = p);
    }
    function je(e, t) {
      var a = e;
      j(a, t), ie(a, t);
    }
    function ie(e, t) {
      var a = t.name;
      if (t.type === "radio" && a != null) {
        for (var i = e; i.parentNode; )
          i = i.parentNode;
        $r(a, "name");
        for (var u = i.querySelectorAll("input[name=" + JSON.stringify("" + a) + '][type="radio"]'), s = 0; s < u.length; s++) {
          var f = u[s];
          if (!(f === e || f.form !== e.form)) {
            var p = _h(f);
            if (!p)
              throw new Error("ReactDOMInput: Mixing React and non-React radio inputs with the same `name` is not supported.");
            Bu(f), j(f, p);
          }
        }
      }
    }
    function Ne(e, t, a) {
      // Focused number inputs synchronize on blur. See ChangeEventPlugin.js
      (t !== "number" || Sl(e.ownerDocument) !== e) && (a == null ? e.defaultValue = Xn(e._wrapperState.initialValue) : e.defaultValue !== Xn(a) && (e.defaultValue = Xn(a)));
    }
    var pt = !1, kt = !1, Kt = !1;
    function Qt(e, t) {
      t.value == null && (typeof t.children == "object" && t.children !== null ? Q.Children.forEach(t.children, function(a) {
        a != null && (typeof a == "string" || typeof a == "number" || kt || (kt = !0, S("Cannot infer the option value of complex children. Pass a `value` prop or use a plain string as children to <option>.")));
      }) : t.dangerouslySetInnerHTML != null && (Kt || (Kt = !0, S("Pass a `value` prop if you set dangerouslyInnerHTML so React knows which value should be selected.")))), t.selected != null && !pt && (S("Use the `defaultValue` or `value` props on <select> instead of setting `selected` on <option>."), pt = !0);
    }
    function Zt(e, t) {
      t.value != null && e.setAttribute("value", Xn(yi(t.value)));
    }
    var tn = Array.isArray;
    function Rt(e) {
      return tn(e);
    }
    var Ai;
    Ai = !1;
    function Yu() {
      var e = Lr();
      return e ? `

Check the render method of \`` + e + "`." : "";
    }
    var Xo = ["value", "defaultValue"];
    function Yf(e) {
      {
        zi("select", e);
        for (var t = 0; t < Xo.length; t++) {
          var a = Xo[t];
          if (e[a] != null) {
            var i = Rt(e[a]);
            e.multiple && !i ? S("The `%s` prop supplied to <select> must be an array if `multiple` is true.%s", a, Yu()) : !e.multiple && i && S("The `%s` prop supplied to <select> must be a scalar value if `multiple` is false.%s", a, Yu());
          }
        }
      }
    }
    function ri(e, t, a, i) {
      var u = e.options;
      if (t) {
        for (var s = a, f = {}, p = 0; p < s.length; p++)
          f["$" + s[p]] = !0;
        for (var v = 0; v < u.length; v++) {
          var y = f.hasOwnProperty("$" + u[v].value);
          u[v].selected !== y && (u[v].selected = y), y && i && (u[v].defaultSelected = !0);
        }
      } else {
        for (var g = Xn(yi(a)), b = null, x = 0; x < u.length; x++) {
          if (u[x].value === g) {
            u[x].selected = !0, i && (u[x].defaultSelected = !0);
            return;
          }
          b === null && !u[x].disabled && (b = u[x]);
        }
        b !== null && (b.selected = !0);
      }
    }
    function Ko(e, t) {
      return lt({}, t, {
        value: void 0
      });
    }
    function Zo(e, t) {
      var a = e;
      Yf(t), a._wrapperState = {
        wasMultiple: !!t.multiple
      }, t.value !== void 0 && t.defaultValue !== void 0 && !Ai && (S("Select elements must be either controlled or uncontrolled (specify either the value prop, or the defaultValue prop, but not both). Decide between using a controlled or uncontrolled select element and remove one of these props. More info: https://reactjs.org/link/controlled-components"), Ai = !0);
    }
    function If(e, t) {
      var a = e;
      a.multiple = !!t.multiple;
      var i = t.value;
      i != null ? ri(a, !!t.multiple, i, !1) : t.defaultValue != null && ri(a, !!t.multiple, t.defaultValue, !0);
    }
    function Ym(e, t) {
      var a = e, i = a._wrapperState.wasMultiple;
      a._wrapperState.wasMultiple = !!t.multiple;
      var u = t.value;
      u != null ? ri(a, !!t.multiple, u, !1) : i !== !!t.multiple && (t.defaultValue != null ? ri(a, !!t.multiple, t.defaultValue, !0) : ri(a, !!t.multiple, t.multiple ? [] : "", !1));
    }
    function Im(e, t) {
      var a = e, i = t.value;
      i != null && ri(a, !!t.multiple, i, !1);
    }
    var Qf = !1;
    function Wf(e, t) {
      var a = e;
      if (t.dangerouslySetInnerHTML != null)
        throw new Error("`dangerouslySetInnerHTML` does not make sense on <textarea>.");
      var i = lt({}, t, {
        value: void 0,
        defaultValue: void 0,
        children: Xn(a._wrapperState.initialValue)
      });
      return i;
    }
    function Zp(e, t) {
      var a = e;
      zi("textarea", t), t.value !== void 0 && t.defaultValue !== void 0 && !Qf && (S("%s contains a textarea with both value and defaultValue props. Textarea elements must be either controlled or uncontrolled (specify either the value prop, or the defaultValue prop, but not both). Decide between using a controlled or uncontrolled textarea and remove one of these props. More info: https://reactjs.org/link/controlled-components", Lr() || "A component"), Qf = !0);
      var i = t.value;
      if (i == null) {
        var u = t.children, s = t.defaultValue;
        if (u != null) {
          S("Use the `defaultValue` or `value` props instead of setting children on <textarea>.");
          {
            if (s != null)
              throw new Error("If you supply `defaultValue` on a <textarea>, do not pass children.");
            if (Rt(u)) {
              if (u.length > 1)
                throw new Error("<textarea> can only have at most one child.");
              u = u[0];
            }
            s = u;
          }
        }
        s == null && (s = ""), i = s;
      }
      a._wrapperState = {
        initialValue: yi(i)
      };
    }
    function Jp(e, t) {
      var a = e, i = yi(t.value), u = yi(t.defaultValue);
      if (i != null) {
        var s = Xn(i);
        s !== a.value && (a.value = s), t.defaultValue == null && a.defaultValue !== s && (a.defaultValue = s);
      }
      u != null && (a.defaultValue = Xn(u));
    }
    function ev(e, t) {
      var a = e, i = a.textContent;
      i === a._wrapperState.initialValue && i !== "" && i !== null && (a.value = i);
    }
    function Gf(e, t) {
      Jp(e, t);
    }
    var ji = "http://www.w3.org/1999/xhtml", Qm = "http://www.w3.org/1998/Math/MathML", qf = "http://www.w3.org/2000/svg";
    function nc(e) {
      switch (e) {
        case "svg":
          return qf;
        case "math":
          return Qm;
        default:
          return ji;
      }
    }
    function Xf(e, t) {
      return e == null || e === ji ? nc(t) : e === qf && t === "foreignObject" ? ji : e;
    }
    var Wm = function(e) {
      return typeof MSApp < "u" && MSApp.execUnsafeLocalFunction ? function(t, a, i, u) {
        MSApp.execUnsafeLocalFunction(function() {
          return e(t, a, i, u);
        });
      } : e;
    }, rc, tv = Wm(function(e, t) {
      if (e.namespaceURI === qf && !("innerHTML" in e)) {
        rc = rc || document.createElement("div"), rc.innerHTML = "<svg>" + t.valueOf().toString() + "</svg>";
        for (var a = rc.firstChild; e.firstChild; )
          e.removeChild(e.firstChild);
        for (; a.firstChild; )
          e.appendChild(a.firstChild);
        return;
      }
      e.innerHTML = t;
    }), Xr = 1, Fi = 3, An = 8, ai = 9, Kl = 11, ac = function(e, t) {
      if (t) {
        var a = e.firstChild;
        if (a && a === e.lastChild && a.nodeType === Fi) {
          a.nodeValue = t;
          return;
        }
      }
      e.textContent = t;
    }, nv = {
      animation: ["animationDelay", "animationDirection", "animationDuration", "animationFillMode", "animationIterationCount", "animationName", "animationPlayState", "animationTimingFunction"],
      background: ["backgroundAttachment", "backgroundClip", "backgroundColor", "backgroundImage", "backgroundOrigin", "backgroundPositionX", "backgroundPositionY", "backgroundRepeat", "backgroundSize"],
      backgroundPosition: ["backgroundPositionX", "backgroundPositionY"],
      border: ["borderBottomColor", "borderBottomStyle", "borderBottomWidth", "borderImageOutset", "borderImageRepeat", "borderImageSlice", "borderImageSource", "borderImageWidth", "borderLeftColor", "borderLeftStyle", "borderLeftWidth", "borderRightColor", "borderRightStyle", "borderRightWidth", "borderTopColor", "borderTopStyle", "borderTopWidth"],
      borderBlockEnd: ["borderBlockEndColor", "borderBlockEndStyle", "borderBlockEndWidth"],
      borderBlockStart: ["borderBlockStartColor", "borderBlockStartStyle", "borderBlockStartWidth"],
      borderBottom: ["borderBottomColor", "borderBottomStyle", "borderBottomWidth"],
      borderColor: ["borderBottomColor", "borderLeftColor", "borderRightColor", "borderTopColor"],
      borderImage: ["borderImageOutset", "borderImageRepeat", "borderImageSlice", "borderImageSource", "borderImageWidth"],
      borderInlineEnd: ["borderInlineEndColor", "borderInlineEndStyle", "borderInlineEndWidth"],
      borderInlineStart: ["borderInlineStartColor", "borderInlineStartStyle", "borderInlineStartWidth"],
      borderLeft: ["borderLeftColor", "borderLeftStyle", "borderLeftWidth"],
      borderRadius: ["borderBottomLeftRadius", "borderBottomRightRadius", "borderTopLeftRadius", "borderTopRightRadius"],
      borderRight: ["borderRightColor", "borderRightStyle", "borderRightWidth"],
      borderStyle: ["borderBottomStyle", "borderLeftStyle", "borderRightStyle", "borderTopStyle"],
      borderTop: ["borderTopColor", "borderTopStyle", "borderTopWidth"],
      borderWidth: ["borderBottomWidth", "borderLeftWidth", "borderRightWidth", "borderTopWidth"],
      columnRule: ["columnRuleColor", "columnRuleStyle", "columnRuleWidth"],
      columns: ["columnCount", "columnWidth"],
      flex: ["flexBasis", "flexGrow", "flexShrink"],
      flexFlow: ["flexDirection", "flexWrap"],
      font: ["fontFamily", "fontFeatureSettings", "fontKerning", "fontLanguageOverride", "fontSize", "fontSizeAdjust", "fontStretch", "fontStyle", "fontVariant", "fontVariantAlternates", "fontVariantCaps", "fontVariantEastAsian", "fontVariantLigatures", "fontVariantNumeric", "fontVariantPosition", "fontWeight", "lineHeight"],
      fontVariant: ["fontVariantAlternates", "fontVariantCaps", "fontVariantEastAsian", "fontVariantLigatures", "fontVariantNumeric", "fontVariantPosition"],
      gap: ["columnGap", "rowGap"],
      grid: ["gridAutoColumns", "gridAutoFlow", "gridAutoRows", "gridTemplateAreas", "gridTemplateColumns", "gridTemplateRows"],
      gridArea: ["gridColumnEnd", "gridColumnStart", "gridRowEnd", "gridRowStart"],
      gridColumn: ["gridColumnEnd", "gridColumnStart"],
      gridColumnGap: ["columnGap"],
      gridGap: ["columnGap", "rowGap"],
      gridRow: ["gridRowEnd", "gridRowStart"],
      gridRowGap: ["rowGap"],
      gridTemplate: ["gridTemplateAreas", "gridTemplateColumns", "gridTemplateRows"],
      listStyle: ["listStyleImage", "listStylePosition", "listStyleType"],
      margin: ["marginBottom", "marginLeft", "marginRight", "marginTop"],
      marker: ["markerEnd", "markerMid", "markerStart"],
      mask: ["maskClip", "maskComposite", "maskImage", "maskMode", "maskOrigin", "maskPositionX", "maskPositionY", "maskRepeat", "maskSize"],
      maskPosition: ["maskPositionX", "maskPositionY"],
      outline: ["outlineColor", "outlineStyle", "outlineWidth"],
      overflow: ["overflowX", "overflowY"],
      padding: ["paddingBottom", "paddingLeft", "paddingRight", "paddingTop"],
      placeContent: ["alignContent", "justifyContent"],
      placeItems: ["alignItems", "justifyItems"],
      placeSelf: ["alignSelf", "justifySelf"],
      textDecoration: ["textDecorationColor", "textDecorationLine", "textDecorationStyle"],
      textEmphasis: ["textEmphasisColor", "textEmphasisStyle"],
      transition: ["transitionDelay", "transitionDuration", "transitionProperty", "transitionTimingFunction"],
      wordWrap: ["overflowWrap"]
    }, Iu = {
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
      // SVG-related properties
      fillOpacity: !0,
      floodOpacity: !0,
      stopOpacity: !0,
      strokeDasharray: !0,
      strokeDashoffset: !0,
      strokeMiterlimit: !0,
      strokeOpacity: !0,
      strokeWidth: !0
    };
    function rv(e, t) {
      return e + t.charAt(0).toUpperCase() + t.substring(1);
    }
    var av = ["Webkit", "ms", "Moz", "O"];
    Object.keys(Iu).forEach(function(e) {
      av.forEach(function(t) {
        Iu[rv(t, e)] = Iu[e];
      });
    });
    function ic(e, t, a) {
      var i = t == null || typeof t == "boolean" || t === "";
      return i ? "" : !a && typeof t == "number" && t !== 0 && !(Iu.hasOwnProperty(e) && Iu[e]) ? t + "px" : (mr(t, e), ("" + t).trim());
    }
    var Qu = /([A-Z])/g, Gm = /^ms-/;
    function qm(e) {
      return e.replace(Qu, "-$1").toLowerCase().replace(Gm, "-ms-");
    }
    var iv = function() {
    };
    {
      var lv = /^(?:webkit|moz|o)[A-Z]/, uv = /^-ms-/, Jo = /-(.)/g, Wu = /;\s*$/, Gu = {}, qu = {}, ov = !1, Kf = !1, Zf = function(e) {
        return e.replace(Jo, function(t, a) {
          return a.toUpperCase();
        });
      }, Jf = function(e) {
        Gu.hasOwnProperty(e) && Gu[e] || (Gu[e] = !0, S(
          "Unsupported style property %s. Did you mean %s?",
          e,
          // As Andi Smith suggests
          // (http://www.andismith.com/blog/2012/02/modernizr-prefixed/), an `-ms` prefix
          // is converted to lowercase `ms`.
          Zf(e.replace(uv, "ms-"))
        ));
      }, sv = function(e) {
        Gu.hasOwnProperty(e) && Gu[e] || (Gu[e] = !0, S("Unsupported vendor-prefixed style property %s. Did you mean %s?", e, e.charAt(0).toUpperCase() + e.slice(1)));
      }, cv = function(e, t) {
        qu.hasOwnProperty(t) && qu[t] || (qu[t] = !0, S(`Style property values shouldn't contain a semicolon. Try "%s: %s" instead.`, e, t.replace(Wu, "")));
      }, fv = function(e, t) {
        ov || (ov = !0, S("`NaN` is an invalid value for the `%s` css style property.", e));
      }, Xm = function(e, t) {
        Kf || (Kf = !0, S("`Infinity` is an invalid value for the `%s` css style property.", e));
      };
      iv = function(e, t) {
        e.indexOf("-") > -1 ? Jf(e) : lv.test(e) ? sv(e) : Wu.test(t) && cv(e, t), typeof t == "number" && (isNaN(t) ? fv(e, t) : isFinite(t) || Xm(e, t));
      };
    }
    var Km = iv;
    function Zm(e) {
      {
        var t = "", a = "";
        for (var i in e)
          if (e.hasOwnProperty(i)) {
            var u = e[i];
            if (u != null) {
              var s = i.indexOf("--") === 0;
              t += a + (s ? i : qm(i)) + ":", t += ic(i, u, s), a = ";";
            }
          }
        return t || null;
      }
    }
    function dv(e, t) {
      var a = e.style;
      for (var i in t)
        if (t.hasOwnProperty(i)) {
          var u = i.indexOf("--") === 0;
          u || Km(i, t[i]);
          var s = ic(i, t[i], u);
          i === "float" && (i = "cssFloat"), u ? a.setProperty(i, s) : a[i] = s;
        }
    }
    function Jm(e) {
      return e == null || typeof e == "boolean" || e === "";
    }
    function Ma(e) {
      var t = {};
      for (var a in e)
        for (var i = nv[a] || [a], u = 0; u < i.length; u++)
          t[i[u]] = a;
      return t;
    }
    function es(e, t) {
      {
        if (!t)
          return;
        var a = Ma(e), i = Ma(t), u = {};
        for (var s in a) {
          var f = a[s], p = i[s];
          if (p && f !== p) {
            var v = f + "," + p;
            if (u[v])
              continue;
            u[v] = !0, S("%s a style property during rerender (%s) when a conflicting property is set (%s) can lead to styling bugs. To avoid this, don't mix shorthand and non-shorthand properties for the same value; instead, replace the shorthand with separate values.", Jm(e[f]) ? "Removing" : "Updating", f, p);
          }
        }
      }
    }
    var pv = {
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
      wbr: !0
      // NOTE: menuitem's close tag should be omitted, but that causes problems.
    }, vv = lt({
      menuitem: !0
    }, pv), hv = "__html";
    function lc(e, t) {
      if (t) {
        if (vv[e] && (t.children != null || t.dangerouslySetInnerHTML != null))
          throw new Error(e + " is a void element tag and must neither have `children` nor use `dangerouslySetInnerHTML`.");
        if (t.dangerouslySetInnerHTML != null) {
          if (t.children != null)
            throw new Error("Can only set one of `children` or `props.dangerouslySetInnerHTML`.");
          if (typeof t.dangerouslySetInnerHTML != "object" || !(hv in t.dangerouslySetInnerHTML))
            throw new Error("`props.dangerouslySetInnerHTML` must be in the form `{__html: ...}`. Please visit https://reactjs.org/link/dangerously-set-inner-html for more information.");
        }
        if (!t.suppressContentEditableWarning && t.contentEditable && t.children != null && S("A component is `contentEditable` and contains `children` managed by React. It is now your responsibility to guarantee that none of those nodes are unexpectedly modified or duplicated. This is probably not intentional."), t.style != null && typeof t.style != "object")
          throw new Error("The `style` prop expects a mapping from style properties to values, not a string. For example, style={{marginRight: spacing + 'em'}} when using JSX.");
      }
    }
    function Hi(e, t) {
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
    var uc = {
      // HTML
      accept: "accept",
      acceptcharset: "acceptCharset",
      "accept-charset": "acceptCharset",
      accesskey: "accessKey",
      action: "action",
      allowfullscreen: "allowFullScreen",
      alt: "alt",
      as: "as",
      async: "async",
      autocapitalize: "autoCapitalize",
      autocomplete: "autoComplete",
      autocorrect: "autoCorrect",
      autofocus: "autoFocus",
      autoplay: "autoPlay",
      autosave: "autoSave",
      capture: "capture",
      cellpadding: "cellPadding",
      cellspacing: "cellSpacing",
      challenge: "challenge",
      charset: "charSet",
      checked: "checked",
      children: "children",
      cite: "cite",
      class: "className",
      classid: "classID",
      classname: "className",
      cols: "cols",
      colspan: "colSpan",
      content: "content",
      contenteditable: "contentEditable",
      contextmenu: "contextMenu",
      controls: "controls",
      controlslist: "controlsList",
      coords: "coords",
      crossorigin: "crossOrigin",
      dangerouslysetinnerhtml: "dangerouslySetInnerHTML",
      data: "data",
      datetime: "dateTime",
      default: "default",
      defaultchecked: "defaultChecked",
      defaultvalue: "defaultValue",
      defer: "defer",
      dir: "dir",
      disabled: "disabled",
      disablepictureinpicture: "disablePictureInPicture",
      disableremoteplayback: "disableRemotePlayback",
      download: "download",
      draggable: "draggable",
      enctype: "encType",
      enterkeyhint: "enterKeyHint",
      for: "htmlFor",
      form: "form",
      formmethod: "formMethod",
      formaction: "formAction",
      formenctype: "formEncType",
      formnovalidate: "formNoValidate",
      formtarget: "formTarget",
      frameborder: "frameBorder",
      headers: "headers",
      height: "height",
      hidden: "hidden",
      high: "high",
      href: "href",
      hreflang: "hrefLang",
      htmlfor: "htmlFor",
      httpequiv: "httpEquiv",
      "http-equiv": "httpEquiv",
      icon: "icon",
      id: "id",
      imagesizes: "imageSizes",
      imagesrcset: "imageSrcSet",
      innerhtml: "innerHTML",
      inputmode: "inputMode",
      integrity: "integrity",
      is: "is",
      itemid: "itemID",
      itemprop: "itemProp",
      itemref: "itemRef",
      itemscope: "itemScope",
      itemtype: "itemType",
      keyparams: "keyParams",
      keytype: "keyType",
      kind: "kind",
      label: "label",
      lang: "lang",
      list: "list",
      loop: "loop",
      low: "low",
      manifest: "manifest",
      marginwidth: "marginWidth",
      marginheight: "marginHeight",
      max: "max",
      maxlength: "maxLength",
      media: "media",
      mediagroup: "mediaGroup",
      method: "method",
      min: "min",
      minlength: "minLength",
      multiple: "multiple",
      muted: "muted",
      name: "name",
      nomodule: "noModule",
      nonce: "nonce",
      novalidate: "noValidate",
      open: "open",
      optimum: "optimum",
      pattern: "pattern",
      placeholder: "placeholder",
      playsinline: "playsInline",
      poster: "poster",
      preload: "preload",
      profile: "profile",
      radiogroup: "radioGroup",
      readonly: "readOnly",
      referrerpolicy: "referrerPolicy",
      rel: "rel",
      required: "required",
      reversed: "reversed",
      role: "role",
      rows: "rows",
      rowspan: "rowSpan",
      sandbox: "sandbox",
      scope: "scope",
      scoped: "scoped",
      scrolling: "scrolling",
      seamless: "seamless",
      selected: "selected",
      shape: "shape",
      size: "size",
      sizes: "sizes",
      span: "span",
      spellcheck: "spellCheck",
      src: "src",
      srcdoc: "srcDoc",
      srclang: "srcLang",
      srcset: "srcSet",
      start: "start",
      step: "step",
      style: "style",
      summary: "summary",
      tabindex: "tabIndex",
      target: "target",
      title: "title",
      type: "type",
      usemap: "useMap",
      value: "value",
      width: "width",
      wmode: "wmode",
      wrap: "wrap",
      // SVG
      about: "about",
      accentheight: "accentHeight",
      "accent-height": "accentHeight",
      accumulate: "accumulate",
      additive: "additive",
      alignmentbaseline: "alignmentBaseline",
      "alignment-baseline": "alignmentBaseline",
      allowreorder: "allowReorder",
      alphabetic: "alphabetic",
      amplitude: "amplitude",
      arabicform: "arabicForm",
      "arabic-form": "arabicForm",
      ascent: "ascent",
      attributename: "attributeName",
      attributetype: "attributeType",
      autoreverse: "autoReverse",
      azimuth: "azimuth",
      basefrequency: "baseFrequency",
      baselineshift: "baselineShift",
      "baseline-shift": "baselineShift",
      baseprofile: "baseProfile",
      bbox: "bbox",
      begin: "begin",
      bias: "bias",
      by: "by",
      calcmode: "calcMode",
      capheight: "capHeight",
      "cap-height": "capHeight",
      clip: "clip",
      clippath: "clipPath",
      "clip-path": "clipPath",
      clippathunits: "clipPathUnits",
      cliprule: "clipRule",
      "clip-rule": "clipRule",
      color: "color",
      colorinterpolation: "colorInterpolation",
      "color-interpolation": "colorInterpolation",
      colorinterpolationfilters: "colorInterpolationFilters",
      "color-interpolation-filters": "colorInterpolationFilters",
      colorprofile: "colorProfile",
      "color-profile": "colorProfile",
      colorrendering: "colorRendering",
      "color-rendering": "colorRendering",
      contentscripttype: "contentScriptType",
      contentstyletype: "contentStyleType",
      cursor: "cursor",
      cx: "cx",
      cy: "cy",
      d: "d",
      datatype: "datatype",
      decelerate: "decelerate",
      descent: "descent",
      diffuseconstant: "diffuseConstant",
      direction: "direction",
      display: "display",
      divisor: "divisor",
      dominantbaseline: "dominantBaseline",
      "dominant-baseline": "dominantBaseline",
      dur: "dur",
      dx: "dx",
      dy: "dy",
      edgemode: "edgeMode",
      elevation: "elevation",
      enablebackground: "enableBackground",
      "enable-background": "enableBackground",
      end: "end",
      exponent: "exponent",
      externalresourcesrequired: "externalResourcesRequired",
      fill: "fill",
      fillopacity: "fillOpacity",
      "fill-opacity": "fillOpacity",
      fillrule: "fillRule",
      "fill-rule": "fillRule",
      filter: "filter",
      filterres: "filterRes",
      filterunits: "filterUnits",
      floodopacity: "floodOpacity",
      "flood-opacity": "floodOpacity",
      floodcolor: "floodColor",
      "flood-color": "floodColor",
      focusable: "focusable",
      fontfamily: "fontFamily",
      "font-family": "fontFamily",
      fontsize: "fontSize",
      "font-size": "fontSize",
      fontsizeadjust: "fontSizeAdjust",
      "font-size-adjust": "fontSizeAdjust",
      fontstretch: "fontStretch",
      "font-stretch": "fontStretch",
      fontstyle: "fontStyle",
      "font-style": "fontStyle",
      fontvariant: "fontVariant",
      "font-variant": "fontVariant",
      fontweight: "fontWeight",
      "font-weight": "fontWeight",
      format: "format",
      from: "from",
      fx: "fx",
      fy: "fy",
      g1: "g1",
      g2: "g2",
      glyphname: "glyphName",
      "glyph-name": "glyphName",
      glyphorientationhorizontal: "glyphOrientationHorizontal",
      "glyph-orientation-horizontal": "glyphOrientationHorizontal",
      glyphorientationvertical: "glyphOrientationVertical",
      "glyph-orientation-vertical": "glyphOrientationVertical",
      glyphref: "glyphRef",
      gradienttransform: "gradientTransform",
      gradientunits: "gradientUnits",
      hanging: "hanging",
      horizadvx: "horizAdvX",
      "horiz-adv-x": "horizAdvX",
      horizoriginx: "horizOriginX",
      "horiz-origin-x": "horizOriginX",
      ideographic: "ideographic",
      imagerendering: "imageRendering",
      "image-rendering": "imageRendering",
      in2: "in2",
      in: "in",
      inlist: "inlist",
      intercept: "intercept",
      k1: "k1",
      k2: "k2",
      k3: "k3",
      k4: "k4",
      k: "k",
      kernelmatrix: "kernelMatrix",
      kernelunitlength: "kernelUnitLength",
      kerning: "kerning",
      keypoints: "keyPoints",
      keysplines: "keySplines",
      keytimes: "keyTimes",
      lengthadjust: "lengthAdjust",
      letterspacing: "letterSpacing",
      "letter-spacing": "letterSpacing",
      lightingcolor: "lightingColor",
      "lighting-color": "lightingColor",
      limitingconeangle: "limitingConeAngle",
      local: "local",
      markerend: "markerEnd",
      "marker-end": "markerEnd",
      markerheight: "markerHeight",
      markermid: "markerMid",
      "marker-mid": "markerMid",
      markerstart: "markerStart",
      "marker-start": "markerStart",
      markerunits: "markerUnits",
      markerwidth: "markerWidth",
      mask: "mask",
      maskcontentunits: "maskContentUnits",
      maskunits: "maskUnits",
      mathematical: "mathematical",
      mode: "mode",
      numoctaves: "numOctaves",
      offset: "offset",
      opacity: "opacity",
      operator: "operator",
      order: "order",
      orient: "orient",
      orientation: "orientation",
      origin: "origin",
      overflow: "overflow",
      overlineposition: "overlinePosition",
      "overline-position": "overlinePosition",
      overlinethickness: "overlineThickness",
      "overline-thickness": "overlineThickness",
      paintorder: "paintOrder",
      "paint-order": "paintOrder",
      panose1: "panose1",
      "panose-1": "panose1",
      pathlength: "pathLength",
      patterncontentunits: "patternContentUnits",
      patterntransform: "patternTransform",
      patternunits: "patternUnits",
      pointerevents: "pointerEvents",
      "pointer-events": "pointerEvents",
      points: "points",
      pointsatx: "pointsAtX",
      pointsaty: "pointsAtY",
      pointsatz: "pointsAtZ",
      prefix: "prefix",
      preservealpha: "preserveAlpha",
      preserveaspectratio: "preserveAspectRatio",
      primitiveunits: "primitiveUnits",
      property: "property",
      r: "r",
      radius: "radius",
      refx: "refX",
      refy: "refY",
      renderingintent: "renderingIntent",
      "rendering-intent": "renderingIntent",
      repeatcount: "repeatCount",
      repeatdur: "repeatDur",
      requiredextensions: "requiredExtensions",
      requiredfeatures: "requiredFeatures",
      resource: "resource",
      restart: "restart",
      result: "result",
      results: "results",
      rotate: "rotate",
      rx: "rx",
      ry: "ry",
      scale: "scale",
      security: "security",
      seed: "seed",
      shaperendering: "shapeRendering",
      "shape-rendering": "shapeRendering",
      slope: "slope",
      spacing: "spacing",
      specularconstant: "specularConstant",
      specularexponent: "specularExponent",
      speed: "speed",
      spreadmethod: "spreadMethod",
      startoffset: "startOffset",
      stddeviation: "stdDeviation",
      stemh: "stemh",
      stemv: "stemv",
      stitchtiles: "stitchTiles",
      stopcolor: "stopColor",
      "stop-color": "stopColor",
      stopopacity: "stopOpacity",
      "stop-opacity": "stopOpacity",
      strikethroughposition: "strikethroughPosition",
      "strikethrough-position": "strikethroughPosition",
      strikethroughthickness: "strikethroughThickness",
      "strikethrough-thickness": "strikethroughThickness",
      string: "string",
      stroke: "stroke",
      strokedasharray: "strokeDasharray",
      "stroke-dasharray": "strokeDasharray",
      strokedashoffset: "strokeDashoffset",
      "stroke-dashoffset": "strokeDashoffset",
      strokelinecap: "strokeLinecap",
      "stroke-linecap": "strokeLinecap",
      strokelinejoin: "strokeLinejoin",
      "stroke-linejoin": "strokeLinejoin",
      strokemiterlimit: "strokeMiterlimit",
      "stroke-miterlimit": "strokeMiterlimit",
      strokewidth: "strokeWidth",
      "stroke-width": "strokeWidth",
      strokeopacity: "strokeOpacity",
      "stroke-opacity": "strokeOpacity",
      suppresscontenteditablewarning: "suppressContentEditableWarning",
      suppresshydrationwarning: "suppressHydrationWarning",
      surfacescale: "surfaceScale",
      systemlanguage: "systemLanguage",
      tablevalues: "tableValues",
      targetx: "targetX",
      targety: "targetY",
      textanchor: "textAnchor",
      "text-anchor": "textAnchor",
      textdecoration: "textDecoration",
      "text-decoration": "textDecoration",
      textlength: "textLength",
      textrendering: "textRendering",
      "text-rendering": "textRendering",
      to: "to",
      transform: "transform",
      typeof: "typeof",
      u1: "u1",
      u2: "u2",
      underlineposition: "underlinePosition",
      "underline-position": "underlinePosition",
      underlinethickness: "underlineThickness",
      "underline-thickness": "underlineThickness",
      unicode: "unicode",
      unicodebidi: "unicodeBidi",
      "unicode-bidi": "unicodeBidi",
      unicoderange: "unicodeRange",
      "unicode-range": "unicodeRange",
      unitsperem: "unitsPerEm",
      "units-per-em": "unitsPerEm",
      unselectable: "unselectable",
      valphabetic: "vAlphabetic",
      "v-alphabetic": "vAlphabetic",
      values: "values",
      vectoreffect: "vectorEffect",
      "vector-effect": "vectorEffect",
      version: "version",
      vertadvy: "vertAdvY",
      "vert-adv-y": "vertAdvY",
      vertoriginx: "vertOriginX",
      "vert-origin-x": "vertOriginX",
      vertoriginy: "vertOriginY",
      "vert-origin-y": "vertOriginY",
      vhanging: "vHanging",
      "v-hanging": "vHanging",
      videographic: "vIdeographic",
      "v-ideographic": "vIdeographic",
      viewbox: "viewBox",
      viewtarget: "viewTarget",
      visibility: "visibility",
      vmathematical: "vMathematical",
      "v-mathematical": "vMathematical",
      vocab: "vocab",
      widths: "widths",
      wordspacing: "wordSpacing",
      "word-spacing": "wordSpacing",
      writingmode: "writingMode",
      "writing-mode": "writingMode",
      x1: "x1",
      x2: "x2",
      x: "x",
      xchannelselector: "xChannelSelector",
      xheight: "xHeight",
      "x-height": "xHeight",
      xlinkactuate: "xlinkActuate",
      "xlink:actuate": "xlinkActuate",
      xlinkarcrole: "xlinkArcrole",
      "xlink:arcrole": "xlinkArcrole",
      xlinkhref: "xlinkHref",
      "xlink:href": "xlinkHref",
      xlinkrole: "xlinkRole",
      "xlink:role": "xlinkRole",
      xlinkshow: "xlinkShow",
      "xlink:show": "xlinkShow",
      xlinktitle: "xlinkTitle",
      "xlink:title": "xlinkTitle",
      xlinktype: "xlinkType",
      "xlink:type": "xlinkType",
      xmlbase: "xmlBase",
      "xml:base": "xmlBase",
      xmllang: "xmlLang",
      "xml:lang": "xmlLang",
      xmlns: "xmlns",
      "xml:space": "xmlSpace",
      xmlnsxlink: "xmlnsXlink",
      "xmlns:xlink": "xmlnsXlink",
      xmlspace: "xmlSpace",
      y1: "y1",
      y2: "y2",
      y: "y",
      ychannelselector: "yChannelSelector",
      z: "z",
      zoomandpan: "zoomAndPan"
    }, mv = {
      "aria-current": 0,
      // state
      "aria-description": 0,
      "aria-details": 0,
      "aria-disabled": 0,
      // state
      "aria-hidden": 0,
      // state
      "aria-invalid": 0,
      // state
      "aria-keyshortcuts": 0,
      "aria-label": 0,
      "aria-roledescription": 0,
      // Widget Attributes
      "aria-autocomplete": 0,
      "aria-checked": 0,
      "aria-expanded": 0,
      "aria-haspopup": 0,
      "aria-level": 0,
      "aria-modal": 0,
      "aria-multiline": 0,
      "aria-multiselectable": 0,
      "aria-orientation": 0,
      "aria-placeholder": 0,
      "aria-pressed": 0,
      "aria-readonly": 0,
      "aria-required": 0,
      "aria-selected": 0,
      "aria-sort": 0,
      "aria-valuemax": 0,
      "aria-valuemin": 0,
      "aria-valuenow": 0,
      "aria-valuetext": 0,
      // Live Region Attributes
      "aria-atomic": 0,
      "aria-busy": 0,
      "aria-live": 0,
      "aria-relevant": 0,
      // Drag-and-Drop Attributes
      "aria-dropeffect": 0,
      "aria-grabbed": 0,
      // Relationship Attributes
      "aria-activedescendant": 0,
      "aria-colcount": 0,
      "aria-colindex": 0,
      "aria-colspan": 0,
      "aria-controls": 0,
      "aria-describedby": 0,
      "aria-errormessage": 0,
      "aria-flowto": 0,
      "aria-labelledby": 0,
      "aria-owns": 0,
      "aria-posinset": 0,
      "aria-rowcount": 0,
      "aria-rowindex": 0,
      "aria-rowspan": 0,
      "aria-setsize": 0
    }, ii = {}, ed = new RegExp("^(aria)-[" + _e + "]*$"), ts = new RegExp("^(aria)[A-Z][" + _e + "]*$");
    function td(e, t) {
      {
        if (Wn.call(ii, t) && ii[t])
          return !0;
        if (ts.test(t)) {
          var a = "aria-" + t.slice(4).toLowerCase(), i = mv.hasOwnProperty(a) ? a : null;
          if (i == null)
            return S("Invalid ARIA attribute `%s`. ARIA attributes follow the pattern aria-* and must be lowercase.", t), ii[t] = !0, !0;
          if (t !== i)
            return S("Invalid ARIA attribute `%s`. Did you mean `%s`?", t, i), ii[t] = !0, !0;
        }
        if (ed.test(t)) {
          var u = t.toLowerCase(), s = mv.hasOwnProperty(u) ? u : null;
          if (s == null)
            return ii[t] = !0, !1;
          if (t !== s)
            return S("Unknown ARIA attribute `%s`. Did you mean `%s`?", t, s), ii[t] = !0, !0;
        }
      }
      return !0;
    }
    function yv(e, t) {
      {
        var a = [];
        for (var i in t) {
          var u = td(e, i);
          u || a.push(i);
        }
        var s = a.map(function(f) {
          return "`" + f + "`";
        }).join(", ");
        a.length === 1 ? S("Invalid aria prop %s on <%s> tag. For details, see https://reactjs.org/link/invalid-aria-props", s, e) : a.length > 1 && S("Invalid aria props %s on <%s> tag. For details, see https://reactjs.org/link/invalid-aria-props", s, e);
      }
    }
    function oc(e, t) {
      Hi(e, t) || yv(e, t);
    }
    var Zl = !1;
    function nd(e, t) {
      {
        if (e !== "input" && e !== "textarea" && e !== "select")
          return;
        t != null && t.value === null && !Zl && (Zl = !0, e === "select" && t.multiple ? S("`value` prop on `%s` should not be null. Consider using an empty array when `multiple` is set to `true` to clear the component or `undefined` for uncontrolled components.", e) : S("`value` prop on `%s` should not be null. Consider using an empty string to clear the component or `undefined` for uncontrolled components.", e));
      }
    }
    var rd = function() {
    };
    {
      var Kn = {}, ad = /^on./, gv = /^on[^A-Z]/, Sv = new RegExp("^(aria)-[" + _e + "]*$"), Ev = new RegExp("^(aria)[A-Z][" + _e + "]*$");
      rd = function(e, t, a, i) {
        if (Wn.call(Kn, t) && Kn[t])
          return !0;
        var u = t.toLowerCase();
        if (u === "onfocusin" || u === "onfocusout")
          return S("React uses onFocus and onBlur instead of onFocusIn and onFocusOut. All React events are normalized to bubble, so onFocusIn and onFocusOut are not needed/supported by React."), Kn[t] = !0, !0;
        if (i != null) {
          var s = i.registrationNameDependencies, f = i.possibleRegistrationNames;
          if (s.hasOwnProperty(t))
            return !0;
          var p = f.hasOwnProperty(u) ? f[u] : null;
          if (p != null)
            return S("Invalid event handler property `%s`. Did you mean `%s`?", t, p), Kn[t] = !0, !0;
          if (ad.test(t))
            return S("Unknown event handler property `%s`. It will be ignored.", t), Kn[t] = !0, !0;
        } else if (ad.test(t))
          return gv.test(t) && S("Invalid event handler property `%s`. React events use the camelCase naming convention, for example `onClick`.", t), Kn[t] = !0, !0;
        if (Sv.test(t) || Ev.test(t))
          return !0;
        if (u === "innerhtml")
          return S("Directly setting property `innerHTML` is not permitted. For more information, lookup documentation on `dangerouslySetInnerHTML`."), Kn[t] = !0, !0;
        if (u === "aria")
          return S("The `aria` attribute is reserved for future use in React. Pass individual `aria-` attributes instead."), Kn[t] = !0, !0;
        if (u === "is" && a !== null && a !== void 0 && typeof a != "string")
          return S("Received a `%s` for a string attribute `is`. If this is expected, cast the value to a string.", typeof a), Kn[t] = !0, !0;
        if (typeof a == "number" && isNaN(a))
          return S("Received NaN for the `%s` attribute. If this is expected, cast the value to a string.", t), Kn[t] = !0, !0;
        var v = br(t), y = v !== null && v.type === da;
        if (uc.hasOwnProperty(u)) {
          var g = uc[u];
          if (g !== t)
            return S("Invalid DOM property `%s`. Did you mean `%s`?", t, g), Kn[t] = !0, !0;
        } else if (!y && t !== u)
          return S("React does not recognize the `%s` prop on a DOM element. If you intentionally want it to appear in the DOM as a custom attribute, spell it as lowercase `%s` instead. If you accidentally passed it from a parent component, remove it from the DOM element.", t, u), Kn[t] = !0, !0;
        return typeof a == "boolean" && gr(t, a, v, !1) ? (a ? S('Received `%s` for a non-boolean attribute `%s`.\n\nIf you want to write it to the DOM, pass a string instead: %s="%s" or %s={value.toString()}.', a, t, t, a, t) : S('Received `%s` for a non-boolean attribute `%s`.\n\nIf you want to write it to the DOM, pass a string instead: %s="%s" or %s={value.toString()}.\n\nIf you used to conditionally omit it with %s={condition && value}, pass %s={condition ? value : undefined} instead.', a, t, t, a, t, t, t), Kn[t] = !0, !0) : y ? !0 : gr(t, a, v, !1) ? (Kn[t] = !0, !1) : ((a === "false" || a === "true") && v !== null && v.type === hn && (S("Received the string `%s` for the boolean attribute `%s`. %s Did you mean %s={%s}?", a, t, a === "false" ? "The browser will interpret it as a truthy value." : 'Although this works, it will not work as expected if you pass the string "false".', t, a), Kn[t] = !0), !0);
      };
    }
    var Cv = function(e, t, a) {
      {
        var i = [];
        for (var u in t) {
          var s = rd(e, u, t[u], a);
          s || i.push(u);
        }
        var f = i.map(function(p) {
          return "`" + p + "`";
        }).join(", ");
        i.length === 1 ? S("Invalid value for prop %s on <%s> tag. Either remove it from the element, or pass a string or number value to keep it in the DOM. For details, see https://reactjs.org/link/attribute-behavior ", f, e) : i.length > 1 && S("Invalid values for props %s on <%s> tag. Either remove them from the element, or pass a string or number value to keep them in the DOM. For details, see https://reactjs.org/link/attribute-behavior ", f, e);
      }
    };
    function Rv(e, t, a) {
      Hi(e, t) || Cv(e, t, a);
    }
    var Vi = 1, ns = 2, Jl = 4, ey = Vi | ns | Jl, rs = null;
    function as(e) {
      rs !== null && S("Expected currently replaying event to be null. This error is likely caused by a bug in React. Please file an issue."), rs = e;
    }
    function ty() {
      rs === null && S("Expected currently replaying event to not be null. This error is likely caused by a bug in React. Please file an issue."), rs = null;
    }
    function Tv(e) {
      return e === rs;
    }
    function sc(e) {
      var t = e.target || e.srcElement || window;
      return t.correspondingUseElement && (t = t.correspondingUseElement), t.nodeType === Fi ? t.parentNode : t;
    }
    var Jt = null, Cl = null, Pi = null;
    function Xu(e) {
      var t = Oo(e);
      if (t) {
        if (typeof Jt != "function")
          throw new Error("setRestoreImplementation() needs to be called to handle a target for controlled events. This error is likely caused by a bug in React. Please file an issue.");
        var a = t.stateNode;
        if (a) {
          var i = _h(a);
          Jt(t.stateNode, t.type, i);
        }
      }
    }
    function xv(e) {
      Jt = e;
    }
    function cc(e) {
      Cl ? Pi ? Pi.push(e) : Pi = [e] : Cl = e;
    }
    function is() {
      return Cl !== null || Pi !== null;
    }
    function ls() {
      if (Cl) {
        var e = Cl, t = Pi;
        if (Cl = null, Pi = null, Xu(e), t)
          for (var a = 0; a < t.length; a++)
            Xu(t[a]);
      }
    }
    var eu = function(e, t) {
      return e(t);
    }, id = function() {
    }, ld = !1;
    function ny() {
      var e = is();
      e && (id(), ls());
    }
    function ud(e, t, a) {
      if (ld)
        return e(t, a);
      ld = !0;
      try {
        return eu(e, t, a);
      } finally {
        ld = !1, ny();
      }
    }
    function fc(e, t, a) {
      eu = e, id = a;
    }
    function dc(e) {
      return e === "button" || e === "input" || e === "select" || e === "textarea";
    }
    function od(e, t, a) {
      switch (e) {
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
          return !!(a.disabled && dc(t));
        default:
          return !1;
      }
    }
    function tu(e, t) {
      var a = e.stateNode;
      if (a === null)
        return null;
      var i = _h(a);
      if (i === null)
        return null;
      var u = i[t];
      if (od(t, e.type, i))
        return null;
      if (u && typeof u != "function")
        throw new Error("Expected `" + t + "` listener to be a function, instead got a value of `" + typeof u + "` type.");
      return u;
    }
    var us = !1;
    if (vn)
      try {
        var nu = {};
        Object.defineProperty(nu, "passive", {
          get: function() {
            us = !0;
          }
        }), window.addEventListener("test", nu, nu), window.removeEventListener("test", nu, nu);
      } catch {
        us = !1;
      }
    function wv(e, t, a, i, u, s, f, p, v) {
      var y = Array.prototype.slice.call(arguments, 3);
      try {
        t.apply(a, y);
      } catch (g) {
        this.onError(g);
      }
    }
    var sd = wv;
    if (typeof window < "u" && typeof window.dispatchEvent == "function" && typeof document < "u" && typeof document.createEvent == "function") {
      var cd = document.createElement("react");
      sd = function(t, a, i, u, s, f, p, v, y) {
        if (typeof document > "u" || document === null)
          throw new Error("The `document` global was defined when React was initialized, but is not defined anymore. This can happen in a test environment if a component schedules an update from an asynchronous callback, but the test has already finished running. To solve this, you can either unmount the component at the end of your test (and ensure that any asynchronous operations get canceled in `componentWillUnmount`), or you can change the test itself to be asynchronous.");
        var g = document.createEvent("Event"), b = !1, x = !0, N = window.event, A = Object.getOwnPropertyDescriptor(window, "event");
        function F() {
          cd.removeEventListener(H, Me, !1), typeof window.event < "u" && window.hasOwnProperty("event") && (window.event = N);
        }
        var le = Array.prototype.slice.call(arguments, 3);
        function Me() {
          b = !0, F(), a.apply(i, le), x = !1;
        }
        var we, wt = !1, gt = !1;
        function O(L) {
          if (we = L.error, wt = !0, we === null && L.colno === 0 && L.lineno === 0 && (gt = !0), L.defaultPrevented && we != null && typeof we == "object")
            try {
              we._suppressLogging = !0;
            } catch {
            }
        }
        var H = "react-" + (t || "invokeguardedcallback");
        if (window.addEventListener("error", O), cd.addEventListener(H, Me, !1), g.initEvent(H, !1, !1), cd.dispatchEvent(g), A && Object.defineProperty(window, "event", A), b && x && (wt ? gt && (we = new Error("A cross-origin error was thrown. React doesn't have access to the actual error object in development. See https://reactjs.org/link/crossorigin-error for more information.")) : we = new Error(`An error was thrown inside one of your components, but React doesn't know what it was. This is likely due to browser flakiness. React does its best to preserve the "Pause on exceptions" behavior of the DevTools, which requires some DEV-mode only tricks. It's possible that these don't work in your browser. Try triggering the error in production mode, or switching to a modern browser. If you suspect that this is actually an issue with React, please file an issue.`), this.onError(we)), window.removeEventListener("error", O), !b)
          return F(), wv.apply(this, arguments);
      };
    }
    var ry = sd, Rl = !1, li = null, os = !1, Tl = null, gi = {
      onError: function(e) {
        Rl = !0, li = e;
      }
    };
    function ru(e, t, a, i, u, s, f, p, v) {
      Rl = !1, li = null, ry.apply(gi, arguments);
    }
    function Bi(e, t, a, i, u, s, f, p, v) {
      if (ru.apply(this, arguments), Rl) {
        var y = dd();
        os || (os = !0, Tl = y);
      }
    }
    function fd() {
      if (os) {
        var e = Tl;
        throw os = !1, Tl = null, e;
      }
    }
    function ay() {
      return Rl;
    }
    function dd() {
      if (Rl) {
        var e = li;
        return Rl = !1, li = null, e;
      } else
        throw new Error("clearCaughtError was called but no error was captured. This error is likely caused by a bug in React. Please file an issue.");
    }
    function Na(e) {
      return e._reactInternals;
    }
    function ss(e) {
      return e._reactInternals !== void 0;
    }
    function Ku(e, t) {
      e._reactInternals = t;
    }
    var Le = (
      /*                      */
      0
    ), xl = (
      /*                */
      1
    ), ln = (
      /*                    */
      2
    ), et = (
      /*                       */
      4
    ), jt = (
      /*                */
      16
    ), $t = (
      /*                 */
      32
    ), Si = (
      /*                     */
      64
    ), Ie = (
      /*                   */
      128
    ), Tn = (
      /*            */
      256
    ), Kr = (
      /*                          */
      512
    ), za = (
      /*                     */
      1024
    ), cn = (
      /*                      */
      2048
    ), Ua = (
      /*                    */
      4096
    ), wl = (
      /*                   */
      8192
    ), cs = (
      /*             */
      16384
    ), pc = cn | et | Si | Kr | za | cs, bv = (
      /*               */
      32767
    ), ya = (
      /*                   */
      32768
    ), Zn = (
      /*                */
      65536
    ), fs = (
      /* */
      131072
    ), pd = (
      /*                       */
      1048576
    ), vd = (
      /*                    */
      2097152
    ), Zr = (
      /*                 */
      4194304
    ), bl = (
      /*                */
      8388608
    ), Jr = (
      /*               */
      16777216
    ), au = (
      /*              */
      33554432
    ), Zu = (
      // TODO: Remove Update flag from before mutation phase by re-landing Visibility
      // flag logic (see #20043)
      et | za | 0
    ), ea = ln | et | jt | $t | Kr | Ua | wl, Er = et | Si | Kr | wl, Aa = cn | jt, ar = Zr | bl | vd, $i = k.ReactCurrentOwner;
    function ga(e) {
      var t = e, a = e;
      if (e.alternate)
        for (; t.return; )
          t = t.return;
      else {
        var i = t;
        do
          t = i, (t.flags & (ln | Ua)) !== Le && (a = t.return), i = t.return;
        while (i);
      }
      return t.tag === re ? a : null;
    }
    function hd(e) {
      if (e.tag === Oe) {
        var t = e.memoizedState;
        if (t === null) {
          var a = e.alternate;
          a !== null && (t = a.memoizedState);
        }
        if (t !== null)
          return t.dehydrated;
      }
      return null;
    }
    function vc(e) {
      return e.tag === re ? e.stateNode.containerInfo : null;
    }
    function md(e) {
      return ga(e) === e;
    }
    function Sa(e) {
      {
        var t = $i.current;
        if (t !== null && t.tag === se) {
          var a = t, i = a.stateNode;
          i._warnedAboutRefsInRender || S("%s is accessing isMounted inside its render() function. render() should be a pure function of props and state. It should never access something that requires stale data from the previous render, such as refs. Move this logic to componentDidMount and componentDidUpdate instead.", We(a) || "A component"), i._warnedAboutRefsInRender = !0;
        }
      }
      var u = Na(e);
      return u ? ga(u) === u : !1;
    }
    function ta(e) {
      if (ga(e) !== e)
        throw new Error("Unable to find node on an unmounted component.");
    }
    function un(e) {
      var t = e.alternate;
      if (!t) {
        var a = ga(e);
        if (a === null)
          throw new Error("Unable to find node on an unmounted component.");
        return a !== e ? null : e;
      }
      for (var i = e, u = t; ; ) {
        var s = i.return;
        if (s === null)
          break;
        var f = s.alternate;
        if (f === null) {
          var p = s.return;
          if (p !== null) {
            i = u = p;
            continue;
          }
          break;
        }
        if (s.child === f.child) {
          for (var v = s.child; v; ) {
            if (v === i)
              return ta(s), e;
            if (v === u)
              return ta(s), t;
            v = v.sibling;
          }
          throw new Error("Unable to find node on an unmounted component.");
        }
        if (i.return !== u.return)
          i = s, u = f;
        else {
          for (var y = !1, g = s.child; g; ) {
            if (g === i) {
              y = !0, i = s, u = f;
              break;
            }
            if (g === u) {
              y = !0, u = s, i = f;
              break;
            }
            g = g.sibling;
          }
          if (!y) {
            for (g = f.child; g; ) {
              if (g === i) {
                y = !0, i = f, u = s;
                break;
              }
              if (g === u) {
                y = !0, u = f, i = s;
                break;
              }
              g = g.sibling;
            }
            if (!y)
              throw new Error("Child was not found in either parent set. This indicates a bug in React related to the return pointer. Please file an issue.");
          }
        }
        if (i.alternate !== u)
          throw new Error("Return fibers should always be each others' alternates. This error is likely caused by a bug in React. Please file an issue.");
      }
      if (i.tag !== re)
        throw new Error("Unable to find node on an unmounted component.");
      return i.stateNode.current === i ? e : t;
    }
    function ja(e) {
      var t = un(e);
      return t !== null ? yd(t) : null;
    }
    function yd(e) {
      if (e.tag === ue || e.tag === Ye)
        return e;
      for (var t = e.child; t !== null; ) {
        var a = yd(t);
        if (a !== null)
          return a;
        t = t.sibling;
      }
      return null;
    }
    function _v(e) {
      var t = un(e);
      return t !== null ? hc(t) : null;
    }
    function hc(e) {
      if (e.tag === ue || e.tag === Ye)
        return e;
      for (var t = e.child; t !== null; ) {
        if (t.tag !== pe) {
          var a = hc(t);
          if (a !== null)
            return a;
        }
        t = t.sibling;
      }
      return null;
    }
    var mc = B.unstable_scheduleCallback, kv = B.unstable_cancelCallback, yc = B.unstable_shouldYield, Dv = B.unstable_requestPaint, gn = B.unstable_now, gd = B.unstable_getCurrentPriorityLevel, gc = B.unstable_ImmediatePriority, iu = B.unstable_UserBlockingPriority, Ei = B.unstable_NormalPriority, Ov = B.unstable_LowPriority, Sc = B.unstable_IdlePriority, Ju = B.unstable_yieldValue, Lv = B.unstable_setDisableYieldValue, Yi = null, Pn = null, te = null, Fa = !1, Ea = typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u";
    function Sd(e) {
      if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u")
        return !1;
      var t = __REACT_DEVTOOLS_GLOBAL_HOOK__;
      if (t.isDisabled)
        return !0;
      if (!t.supportsFiber)
        return S("The installed version of React DevTools is too old and will not work with the current version of React. Please update React DevTools. https://reactjs.org/link/react-devtools"), !0;
      try {
        rt && (e = lt({}, e, {
          getLaneLabelMap: Ii,
          injectProfilingHooks: Mv
        })), Yi = t.inject(e), Pn = t;
      } catch (a) {
        S("React instrumentation encountered an error: %s.", a);
      }
      return !!t.checkDCE;
    }
    function Ed(e, t) {
      if (Pn && typeof Pn.onScheduleFiberRoot == "function")
        try {
          Pn.onScheduleFiberRoot(Yi, e, t);
        } catch (a) {
          Fa || (Fa = !0, S("React instrumentation encountered an error: %s", a));
        }
    }
    function eo(e, t) {
      if (Pn && typeof Pn.onCommitFiberRoot == "function")
        try {
          var a = (e.current.flags & Ie) === Ie;
          if (tt) {
            var i;
            switch (t) {
              case Ln:
                i = gc;
                break;
              case Wi:
                i = iu;
                break;
              case Ci:
                i = Ei;
                break;
              case po:
                i = Sc;
                break;
              default:
                i = Ei;
                break;
            }
            Pn.onCommitFiberRoot(Yi, e, i, a);
          }
        } catch (u) {
          Fa || (Fa = !0, S("React instrumentation encountered an error: %s", u));
        }
    }
    function Ha(e) {
      if (Pn && typeof Pn.onPostCommitFiberRoot == "function")
        try {
          Pn.onPostCommitFiberRoot(Yi, e);
        } catch (t) {
          Fa || (Fa = !0, S("React instrumentation encountered an error: %s", t));
        }
    }
    function lu(e) {
      if (Pn && typeof Pn.onCommitFiberUnmount == "function")
        try {
          Pn.onCommitFiberUnmount(Yi, e);
        } catch (t) {
          Fa || (Fa = !0, S("React instrumentation encountered an error: %s", t));
        }
    }
    function jn(e) {
      if (typeof Ju == "function" && (Lv(e), Dt(e)), Pn && typeof Pn.setStrictMode == "function")
        try {
          Pn.setStrictMode(Yi, e);
        } catch (t) {
          Fa || (Fa = !0, S("React instrumentation encountered an error: %s", t));
        }
    }
    function Mv(e) {
      te = e;
    }
    function Ii() {
      {
        for (var e = /* @__PURE__ */ new Map(), t = 1, a = 0; a < ms; a++) {
          var i = ly(t);
          e.set(t, i), t *= 2;
        }
        return e;
      }
    }
    function _l(e) {
      te !== null && typeof te.markCommitStarted == "function" && te.markCommitStarted(e);
    }
    function Ec() {
      te !== null && typeof te.markCommitStopped == "function" && te.markCommitStopped();
    }
    function to(e) {
      te !== null && typeof te.markComponentRenderStarted == "function" && te.markComponentRenderStarted(e);
    }
    function na() {
      te !== null && typeof te.markComponentRenderStopped == "function" && te.markComponentRenderStopped();
    }
    function kl(e) {
      te !== null && typeof te.markComponentPassiveEffectMountStarted == "function" && te.markComponentPassiveEffectMountStarted(e);
    }
    function Cc() {
      te !== null && typeof te.markComponentPassiveEffectMountStopped == "function" && te.markComponentPassiveEffectMountStopped();
    }
    function Nv(e) {
      te !== null && typeof te.markComponentPassiveEffectUnmountStarted == "function" && te.markComponentPassiveEffectUnmountStarted(e);
    }
    function Rc() {
      te !== null && typeof te.markComponentPassiveEffectUnmountStopped == "function" && te.markComponentPassiveEffectUnmountStopped();
    }
    function zv(e) {
      te !== null && typeof te.markComponentLayoutEffectMountStarted == "function" && te.markComponentLayoutEffectMountStarted(e);
    }
    function ds() {
      te !== null && typeof te.markComponentLayoutEffectMountStopped == "function" && te.markComponentLayoutEffectMountStopped();
    }
    function ui(e) {
      te !== null && typeof te.markComponentLayoutEffectUnmountStarted == "function" && te.markComponentLayoutEffectUnmountStarted(e);
    }
    function no() {
      te !== null && typeof te.markComponentLayoutEffectUnmountStopped == "function" && te.markComponentLayoutEffectUnmountStopped();
    }
    function ps(e, t, a) {
      te !== null && typeof te.markComponentErrored == "function" && te.markComponentErrored(e, t, a);
    }
    function uu(e, t, a) {
      te !== null && typeof te.markComponentSuspended == "function" && te.markComponentSuspended(e, t, a);
    }
    function Cd(e) {
      te !== null && typeof te.markLayoutEffectsStarted == "function" && te.markLayoutEffectsStarted(e);
    }
    function ro() {
      te !== null && typeof te.markLayoutEffectsStopped == "function" && te.markLayoutEffectsStopped();
    }
    function Uv(e) {
      te !== null && typeof te.markPassiveEffectsStarted == "function" && te.markPassiveEffectsStarted(e);
    }
    function Rd() {
      te !== null && typeof te.markPassiveEffectsStopped == "function" && te.markPassiveEffectsStopped();
    }
    function fn(e) {
      te !== null && typeof te.markRenderStarted == "function" && te.markRenderStarted(e);
    }
    function Tc() {
      te !== null && typeof te.markRenderYielded == "function" && te.markRenderYielded();
    }
    function xc() {
      te !== null && typeof te.markRenderStopped == "function" && te.markRenderStopped();
    }
    function Td(e) {
      te !== null && typeof te.markRenderScheduled == "function" && te.markRenderScheduled(e);
    }
    function wc(e, t) {
      te !== null && typeof te.markForceUpdateScheduled == "function" && te.markForceUpdateScheduled(e, t);
    }
    function vs(e, t) {
      te !== null && typeof te.markStateUpdateScheduled == "function" && te.markStateUpdateScheduled(e, t);
    }
    var Ce = (
      /*                         */
      0
    ), xe = (
      /*                 */
      1
    ), Qe = (
      /*                    */
      2
    ), vt = (
      /*               */
      8
    ), Ca = (
      /*              */
      16
    ), ao = Math.clz32 ? Math.clz32 : Cr, hs = Math.log, iy = Math.LN2;
    function Cr(e) {
      var t = e >>> 0;
      return t === 0 ? 32 : 31 - (hs(t) / iy | 0) | 0;
    }
    var ms = 31, $ = (
      /*                        */
      0
    ), Fn = (
      /*                          */
      0
    ), ke = (
      /*                        */
      1
    ), ir = (
      /*    */
      2
    ), Ra = (
      /*             */
      4
    ), Qi = (
      /*            */
      8
    ), Va = (
      /*                     */
      16
    ), io = (
      /*                */
      32
    ), ou = (
      /*                       */
      4194240
    ), lo = (
      /*                        */
      64
    ), bc = (
      /*                        */
      128
    ), _c = (
      /*                        */
      256
    ), kc = (
      /*                        */
      512
    ), Dc = (
      /*                        */
      1024
    ), Oc = (
      /*                        */
      2048
    ), su = (
      /*                        */
      4096
    ), Lc = (
      /*                        */
      8192
    ), uo = (
      /*                        */
      16384
    ), oo = (
      /*                       */
      32768
    ), Mc = (
      /*                       */
      65536
    ), ys = (
      /*                       */
      131072
    ), Nc = (
      /*                       */
      262144
    ), zc = (
      /*                       */
      524288
    ), Uc = (
      /*                       */
      1048576
    ), Ac = (
      /*                       */
      2097152
    ), so = (
      /*                            */
      130023424
    ), cu = (
      /*                             */
      4194304
    ), jc = (
      /*                             */
      8388608
    ), Fc = (
      /*                             */
      16777216
    ), xd = (
      /*                             */
      33554432
    ), Hc = (
      /*                             */
      67108864
    ), Av = cu, gs = (
      /*          */
      134217728
    ), wd = (
      /*                          */
      268435455
    ), co = (
      /*               */
      268435456
    ), Dl = (
      /*                        */
      536870912
    ), Rr = (
      /*                   */
      1073741824
    );
    function ly(e) {
      {
        if (e & ke)
          return "Sync";
        if (e & ir)
          return "InputContinuousHydration";
        if (e & Ra)
          return "InputContinuous";
        if (e & Qi)
          return "DefaultHydration";
        if (e & Va)
          return "Default";
        if (e & io)
          return "TransitionHydration";
        if (e & ou)
          return "Transition";
        if (e & so)
          return "Retry";
        if (e & gs)
          return "SelectiveHydration";
        if (e & co)
          return "IdleHydration";
        if (e & Dl)
          return "Idle";
        if (e & Rr)
          return "Offscreen";
      }
    }
    var nn = -1, Vc = lo, ra = cu;
    function fu(e) {
      switch (On(e)) {
        case ke:
          return ke;
        case ir:
          return ir;
        case Ra:
          return Ra;
        case Qi:
          return Qi;
        case Va:
          return Va;
        case io:
          return io;
        case lo:
        case bc:
        case _c:
        case kc:
        case Dc:
        case Oc:
        case su:
        case Lc:
        case uo:
        case oo:
        case Mc:
        case ys:
        case Nc:
        case zc:
        case Uc:
        case Ac:
          return e & ou;
        case cu:
        case jc:
        case Fc:
        case xd:
        case Hc:
          return e & so;
        case gs:
          return gs;
        case co:
          return co;
        case Dl:
          return Dl;
        case Rr:
          return Rr;
        default:
          return S("Should have found matching lanes. This is a bug in React."), e;
      }
    }
    function du(e, t) {
      var a = e.pendingLanes;
      if (a === $)
        return $;
      var i = $, u = e.suspendedLanes, s = e.pingedLanes, f = a & wd;
      if (f !== $) {
        var p = f & ~u;
        if (p !== $)
          i = fu(p);
        else {
          var v = f & s;
          v !== $ && (i = fu(v));
        }
      } else {
        var y = a & ~u;
        y !== $ ? i = fu(y) : s !== $ && (i = fu(s));
      }
      if (i === $)
        return $;
      if (t !== $ && t !== i && // If we already suspended with a delay, then interrupting is fine. Don't
      // bother waiting until the root is complete.
      (t & u) === $) {
        var g = On(i), b = On(t);
        if (
          // Tests whether the next lane is equal or lower priority than the wip
          // one. This works because the bits decrease in priority as you go left.
          g >= b || // Default priority updates should not interrupt transition updates. The
          // only difference between default updates and transition updates is that
          // default updates do not support refresh transitions.
          g === Va && (b & ou) !== $
        )
          return t;
      }
      (i & Ra) !== $ && (i |= a & Va);
      var x = e.entangledLanes;
      if (x !== $)
        for (var N = e.entanglements, A = i & x; A > 0; ) {
          var F = Ll(A), le = 1 << F;
          i |= N[F], A &= ~le;
        }
      return i;
    }
    function jv(e, t) {
      for (var a = e.eventTimes, i = nn; t > 0; ) {
        var u = Ll(t), s = 1 << u, f = a[u];
        f > i && (i = f), t &= ~s;
      }
      return i;
    }
    function Fv(e, t) {
      switch (e) {
        case ke:
        case ir:
        case Ra:
          return t + 250;
        case Qi:
        case Va:
        case io:
        case lo:
        case bc:
        case _c:
        case kc:
        case Dc:
        case Oc:
        case su:
        case Lc:
        case uo:
        case oo:
        case Mc:
        case ys:
        case Nc:
        case zc:
        case Uc:
        case Ac:
          return t + 5e3;
        case cu:
        case jc:
        case Fc:
        case xd:
        case Hc:
          return nn;
        case gs:
        case co:
        case Dl:
        case Rr:
          return nn;
        default:
          return S("Should have found matching lanes. This is a bug in React."), nn;
      }
    }
    function Hv(e, t) {
      for (var a = e.pendingLanes, i = e.suspendedLanes, u = e.pingedLanes, s = e.expirationTimes, f = a; f > 0; ) {
        var p = Ll(f), v = 1 << p, y = s[p];
        y === nn ? ((v & i) === $ || (v & u) !== $) && (s[p] = Fv(v, t)) : y <= t && (e.expiredLanes |= v), f &= ~v;
      }
    }
    function bd(e) {
      return fu(e.pendingLanes);
    }
    function Ol(e) {
      var t = e.pendingLanes & ~Rr;
      return t !== $ ? t : t & Rr ? Rr : $;
    }
    function _d(e) {
      return (e & ke) !== $;
    }
    function Ss(e) {
      return (e & wd) !== $;
    }
    function Vv(e) {
      return (e & so) === e;
    }
    function Pv(e) {
      var t = ke | Ra | Va;
      return (e & t) === $;
    }
    function Bv(e) {
      return (e & ou) === e;
    }
    function Es(e, t) {
      var a = ir | Ra | Qi | Va;
      return (t & a) !== $;
    }
    function $v(e, t) {
      return (t & e.expiredLanes) !== $;
    }
    function kd(e) {
      return (e & ou) !== $;
    }
    function Yv() {
      var e = Vc;
      return Vc <<= 1, (Vc & ou) === $ && (Vc = lo), e;
    }
    function aa() {
      var e = ra;
      return ra <<= 1, (ra & so) === $ && (ra = cu), e;
    }
    function On(e) {
      return e & -e;
    }
    function fo(e) {
      return On(e);
    }
    function Ll(e) {
      return 31 - ao(e);
    }
    function Pc(e) {
      return Ll(e);
    }
    function ia(e, t) {
      return (e & t) !== $;
    }
    function pu(e, t) {
      return (e & t) === t;
    }
    function Ke(e, t) {
      return e | t;
    }
    function Cs(e, t) {
      return e & ~t;
    }
    function Bc(e, t) {
      return e & t;
    }
    function uy(e) {
      return e;
    }
    function Iv(e, t) {
      return e !== Fn && e < t ? e : t;
    }
    function Rs(e) {
      for (var t = [], a = 0; a < ms; a++)
        t.push(e);
      return t;
    }
    function vu(e, t, a) {
      e.pendingLanes |= t, t !== Dl && (e.suspendedLanes = $, e.pingedLanes = $);
      var i = e.eventTimes, u = Pc(t);
      i[u] = a;
    }
    function Qv(e, t) {
      e.suspendedLanes |= t, e.pingedLanes &= ~t;
      for (var a = e.expirationTimes, i = t; i > 0; ) {
        var u = Ll(i), s = 1 << u;
        a[u] = nn, i &= ~s;
      }
    }
    function $c(e, t, a) {
      e.pingedLanes |= e.suspendedLanes & t;
    }
    function Yc(e, t) {
      var a = e.pendingLanes & ~t;
      e.pendingLanes = t, e.suspendedLanes = $, e.pingedLanes = $, e.expiredLanes &= t, e.mutableReadLanes &= t, e.entangledLanes &= t;
      for (var i = e.entanglements, u = e.eventTimes, s = e.expirationTimes, f = a; f > 0; ) {
        var p = Ll(f), v = 1 << p;
        i[p] = $, u[p] = nn, s[p] = nn, f &= ~v;
      }
    }
    function Dd(e, t) {
      for (var a = e.entangledLanes |= t, i = e.entanglements, u = a; u; ) {
        var s = Ll(u), f = 1 << s;
        // Is this one of the newly entangled lanes?
        f & t | // Is this lane transitively entangled with the newly entangled lanes?
        i[s] & t && (i[s] |= t), u &= ~f;
      }
    }
    function Wv(e, t) {
      var a = On(t), i;
      switch (a) {
        case Ra:
          i = ir;
          break;
        case Va:
          i = Qi;
          break;
        case lo:
        case bc:
        case _c:
        case kc:
        case Dc:
        case Oc:
        case su:
        case Lc:
        case uo:
        case oo:
        case Mc:
        case ys:
        case Nc:
        case zc:
        case Uc:
        case Ac:
        case cu:
        case jc:
        case Fc:
        case xd:
        case Hc:
          i = io;
          break;
        case Dl:
          i = co;
          break;
        default:
          i = Fn;
          break;
      }
      return (i & (e.suspendedLanes | t)) !== Fn ? Fn : i;
    }
    function Ic(e, t, a) {
      if (Ea)
        for (var i = e.pendingUpdatersLaneMap; a > 0; ) {
          var u = Pc(a), s = 1 << u, f = i[u];
          f.add(t), a &= ~s;
        }
    }
    function Od(e, t) {
      if (Ea)
        for (var a = e.pendingUpdatersLaneMap, i = e.memoizedUpdaters; t > 0; ) {
          var u = Pc(t), s = 1 << u, f = a[u];
          f.size > 0 && (f.forEach(function(p) {
            var v = p.alternate;
            (v === null || !i.has(v)) && i.add(p);
          }), f.clear()), t &= ~s;
        }
    }
    function Ts(e, t) {
      return null;
    }
    var Ln = ke, Wi = Ra, Ci = Va, po = Dl, vo = Fn;
    function Pa() {
      return vo;
    }
    function xn(e) {
      vo = e;
    }
    function Tr(e, t) {
      var a = vo;
      try {
        return vo = e, t();
      } finally {
        vo = a;
      }
    }
    function oy(e, t) {
      return e !== 0 && e < t ? e : t;
    }
    function sy(e, t) {
      return e === 0 || e > t ? e : t;
    }
    function ho(e, t) {
      return e !== 0 && e < t;
    }
    function lr(e) {
      var t = On(e);
      return ho(Ln, t) ? ho(Wi, t) ? Ss(t) ? Ci : po : Wi : Ln;
    }
    function Qc(e) {
      var t = e.current.memoizedState;
      return t.isDehydrated;
    }
    var he;
    function mo(e) {
      he = e;
    }
    function Ld(e) {
      he(e);
    }
    var Wc;
    function cy(e) {
      Wc = e;
    }
    var yo;
    function Gc(e) {
      yo = e;
    }
    var qc;
    function Gv(e) {
      qc = e;
    }
    var Md;
    function qv(e) {
      Md = e;
    }
    var xs = !1, go = [], dn = null, Jn = null, Mr = null, So = /* @__PURE__ */ new Map(), Eo = /* @__PURE__ */ new Map(), er = [], Xv = [
      "mousedown",
      "mouseup",
      "touchcancel",
      "touchend",
      "touchstart",
      "auxclick",
      "dblclick",
      "pointercancel",
      "pointerdown",
      "pointerup",
      "dragend",
      "dragstart",
      "drop",
      "compositionend",
      "compositionstart",
      "keydown",
      "keypress",
      "keyup",
      "input",
      "textInput",
      // Intentionally camelCase
      "copy",
      "cut",
      "paste",
      "click",
      "change",
      "contextmenu",
      "reset",
      "submit"
    ];
    function Ri(e) {
      return Xv.indexOf(e) > -1;
    }
    function fy(e, t, a, i, u) {
      return {
        blockedOn: e,
        domEventName: t,
        eventSystemFlags: a,
        nativeEvent: u,
        targetContainers: [i]
      };
    }
    function Nd(e, t) {
      switch (e) {
        case "focusin":
        case "focusout":
          dn = null;
          break;
        case "dragenter":
        case "dragleave":
          Jn = null;
          break;
        case "mouseover":
        case "mouseout":
          Mr = null;
          break;
        case "pointerover":
        case "pointerout": {
          var a = t.pointerId;
          So.delete(a);
          break;
        }
        case "gotpointercapture":
        case "lostpointercapture": {
          var i = t.pointerId;
          Eo.delete(i);
          break;
        }
      }
    }
    function Co(e, t, a, i, u, s) {
      if (e === null || e.nativeEvent !== s) {
        var f = fy(t, a, i, u, s);
        if (t !== null) {
          var p = Oo(t);
          p !== null && Wc(p);
        }
        return f;
      }
      e.eventSystemFlags |= i;
      var v = e.targetContainers;
      return u !== null && v.indexOf(u) === -1 && v.push(u), e;
    }
    function Kv(e, t, a, i, u) {
      switch (t) {
        case "focusin": {
          var s = u;
          return dn = Co(dn, e, t, a, i, s), !0;
        }
        case "dragenter": {
          var f = u;
          return Jn = Co(Jn, e, t, a, i, f), !0;
        }
        case "mouseover": {
          var p = u;
          return Mr = Co(Mr, e, t, a, i, p), !0;
        }
        case "pointerover": {
          var v = u, y = v.pointerId;
          return So.set(y, Co(So.get(y) || null, e, t, a, i, v)), !0;
        }
        case "gotpointercapture": {
          var g = u, b = g.pointerId;
          return Eo.set(b, Co(Eo.get(b) || null, e, t, a, i, g)), !0;
        }
      }
      return !1;
    }
    function zd(e) {
      var t = As(e.target);
      if (t !== null) {
        var a = ga(t);
        if (a !== null) {
          var i = a.tag;
          if (i === Oe) {
            var u = hd(a);
            if (u !== null) {
              e.blockedOn = u, Md(e.priority, function() {
                yo(a);
              });
              return;
            }
          } else if (i === re) {
            var s = a.stateNode;
            if (Qc(s)) {
              e.blockedOn = vc(a);
              return;
            }
          }
        }
      }
      e.blockedOn = null;
    }
    function dy(e) {
      for (var t = qc(), a = {
        blockedOn: null,
        target: e,
        priority: t
      }, i = 0; i < er.length && ho(t, er[i].priority); i++)
        ;
      er.splice(i, 0, a), i === 0 && zd(a);
    }
    function hu(e) {
      if (e.blockedOn !== null)
        return !1;
      for (var t = e.targetContainers; t.length > 0; ) {
        var a = t[0], i = xr(e.domEventName, e.eventSystemFlags, a, e.nativeEvent);
        if (i === null) {
          var u = e.nativeEvent, s = new u.constructor(u.type, u);
          as(s), u.target.dispatchEvent(s), ty();
        } else {
          var f = Oo(i);
          return f !== null && Wc(f), e.blockedOn = i, !1;
        }
        t.shift();
      }
      return !0;
    }
    function Xc(e, t, a) {
      hu(e) && a.delete(t);
    }
    function Ba() {
      xs = !1, dn !== null && hu(dn) && (dn = null), Jn !== null && hu(Jn) && (Jn = null), Mr !== null && hu(Mr) && (Mr = null), So.forEach(Xc), Eo.forEach(Xc);
    }
    function yt(e, t) {
      e.blockedOn === t && (e.blockedOn = null, xs || (xs = !0, B.unstable_scheduleCallback(B.unstable_NormalPriority, Ba)));
    }
    function wn(e) {
      if (go.length > 0) {
        yt(go[0], e);
        for (var t = 1; t < go.length; t++) {
          var a = go[t];
          a.blockedOn === e && (a.blockedOn = null);
        }
      }
      dn !== null && yt(dn, e), Jn !== null && yt(Jn, e), Mr !== null && yt(Mr, e);
      var i = function(p) {
        return yt(p, e);
      };
      So.forEach(i), Eo.forEach(i);
      for (var u = 0; u < er.length; u++) {
        var s = er[u];
        s.blockedOn === e && (s.blockedOn = null);
      }
      for (; er.length > 0; ) {
        var f = er[0];
        if (f.blockedOn !== null)
          break;
        zd(f), f.blockedOn === null && er.shift();
      }
    }
    var on = k.ReactCurrentBatchConfig, Bn = !0;
    function la(e) {
      Bn = !!e;
    }
    function Ro() {
      return Bn;
    }
    function $n(e, t, a) {
      var i = Kc(t), u;
      switch (i) {
        case Ln:
          u = ws;
          break;
        case Wi:
          u = mu;
          break;
        case Ci:
        default:
          u = To;
          break;
      }
      return u.bind(null, t, a, e);
    }
    function ws(e, t, a, i) {
      var u = Pa(), s = on.transition;
      on.transition = null;
      try {
        xn(Ln), To(e, t, a, i);
      } finally {
        xn(u), on.transition = s;
      }
    }
    function mu(e, t, a, i) {
      var u = Pa(), s = on.transition;
      on.transition = null;
      try {
        xn(Wi), To(e, t, a, i);
      } finally {
        xn(u), on.transition = s;
      }
    }
    function To(e, t, a, i) {
      Bn && Ud(e, t, a, i);
    }
    function Ud(e, t, a, i) {
      var u = xr(e, t, a, i);
      if (u === null) {
        Dy(e, t, i, Ml, a), Nd(e, i);
        return;
      }
      if (Kv(u, e, t, a, i)) {
        i.stopPropagation();
        return;
      }
      if (Nd(e, i), t & Jl && Ri(e)) {
        for (; u !== null; ) {
          var s = Oo(u);
          s !== null && Ld(s);
          var f = xr(e, t, a, i);
          if (f === null && Dy(e, t, i, Ml, a), f === u)
            break;
          u = f;
        }
        u !== null && i.stopPropagation();
        return;
      }
      Dy(e, t, i, null, a);
    }
    var Ml = null;
    function xr(e, t, a, i) {
      Ml = null;
      var u = sc(i), s = As(u);
      if (s !== null) {
        var f = ga(s);
        if (f === null)
          s = null;
        else {
          var p = f.tag;
          if (p === Oe) {
            var v = hd(f);
            if (v !== null)
              return v;
            s = null;
          } else if (p === re) {
            var y = f.stateNode;
            if (Qc(y))
              return vc(f);
            s = null;
          } else
            f !== s && (s = null);
        }
      }
      return Ml = s, null;
    }
    function Kc(e) {
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
          return Ln;
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
          return Wi;
        case "message": {
          var t = gd();
          switch (t) {
            case gc:
              return Ln;
            case iu:
              return Wi;
            case Ei:
            case Ov:
              return Ci;
            case Sc:
              return po;
            default:
              return Ci;
          }
        }
        default:
          return Ci;
      }
    }
    function xo(e, t, a) {
      return e.addEventListener(t, a, !1), a;
    }
    function Gi(e, t, a) {
      return e.addEventListener(t, a, !0), a;
    }
    function Zc(e, t, a, i) {
      return e.addEventListener(t, a, {
        capture: !0,
        passive: i
      }), a;
    }
    function Ad(e, t, a, i) {
      return e.addEventListener(t, a, {
        passive: i
      }), a;
    }
    var $a = null, wo = null, Ya = null;
    function Jc(e) {
      return $a = e, wo = _s(), !0;
    }
    function bs() {
      $a = null, wo = null, Ya = null;
    }
    function ef() {
      if (Ya)
        return Ya;
      var e, t = wo, a = t.length, i, u = _s(), s = u.length;
      for (e = 0; e < a && t[e] === u[e]; e++)
        ;
      var f = a - e;
      for (i = 1; i <= f && t[a - i] === u[s - i]; i++)
        ;
      var p = i > 1 ? 1 - i : void 0;
      return Ya = u.slice(e, p), Ya;
    }
    function _s() {
      return "value" in $a ? $a.value : $a.textContent;
    }
    function yu(e) {
      var t, a = e.keyCode;
      return "charCode" in e ? (t = e.charCode, t === 0 && a === 13 && (t = 13)) : t = a, t === 10 && (t = 13), t >= 32 || t === 13 ? t : 0;
    }
    function tr() {
      return !0;
    }
    function qi() {
      return !1;
    }
    function Sn(e) {
      function t(a, i, u, s, f) {
        this._reactName = a, this._targetInst = u, this.type = i, this.nativeEvent = s, this.target = f, this.currentTarget = null;
        for (var p in e)
          if (e.hasOwnProperty(p)) {
            var v = e[p];
            v ? this[p] = v(s) : this[p] = s[p];
          }
        var y = s.defaultPrevented != null ? s.defaultPrevented : s.returnValue === !1;
        return y ? this.isDefaultPrevented = tr : this.isDefaultPrevented = qi, this.isPropagationStopped = qi, this;
      }
      return lt(t.prototype, {
        preventDefault: function() {
          this.defaultPrevented = !0;
          var a = this.nativeEvent;
          a && (a.preventDefault ? a.preventDefault() : typeof a.returnValue != "unknown" && (a.returnValue = !1), this.isDefaultPrevented = tr);
        },
        stopPropagation: function() {
          var a = this.nativeEvent;
          a && (a.stopPropagation ? a.stopPropagation() : typeof a.cancelBubble != "unknown" && (a.cancelBubble = !0), this.isPropagationStopped = tr);
        },
        /**
         * We release all dispatched `SyntheticEvent`s after each event loop, adding
         * them back into the pool. This allows a way to hold onto a reference that
         * won't be added back into the pool.
         */
        persist: function() {
        },
        /**
         * Checks if this event should be released back into the pool.
         *
         * @return {boolean} True if this should not be released, false otherwise.
         */
        isPersistent: tr
      }), t;
    }
    var Yn = {
      eventPhase: 0,
      bubbles: 0,
      cancelable: 0,
      timeStamp: function(e) {
        return e.timeStamp || Date.now();
      },
      defaultPrevented: 0,
      isTrusted: 0
    }, tf = Sn(Yn), gu = lt({}, Yn, {
      view: 0,
      detail: 0
    }), jd = Sn(gu), Fd, Ti, bo;
    function Hd(e) {
      e !== bo && (bo && e.type === "mousemove" ? (Fd = e.screenX - bo.screenX, Ti = e.screenY - bo.screenY) : (Fd = 0, Ti = 0), bo = e);
    }
    var xi = lt({}, gu, {
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
      getModifierState: Vd,
      button: 0,
      buttons: 0,
      relatedTarget: function(e) {
        return e.relatedTarget === void 0 ? e.fromElement === e.srcElement ? e.toElement : e.fromElement : e.relatedTarget;
      },
      movementX: function(e) {
        return "movementX" in e ? e.movementX : (Hd(e), Fd);
      },
      movementY: function(e) {
        return "movementY" in e ? e.movementY : Ti;
      }
    }), nf = Sn(xi), Su = lt({}, xi, {
      dataTransfer: 0
    }), Zv = Sn(Su), Jv = lt({}, gu, {
      relatedTarget: 0
    }), ks = Sn(Jv), rf = lt({}, Yn, {
      animationName: 0,
      elapsedTime: 0,
      pseudoElement: 0
    }), py = Sn(rf), vy = lt({}, Yn, {
      clipboardData: function(e) {
        return "clipboardData" in e ? e.clipboardData : window.clipboardData;
      }
    }), eh = Sn(vy), th = lt({}, Yn, {
      data: 0
    }), Nl = Sn(th), hy = Nl, _o = {
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
    }, nh = {
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
    };
    function bn(e) {
      if (e.key) {
        var t = _o[e.key] || e.key;
        if (t !== "Unidentified")
          return t;
      }
      if (e.type === "keypress") {
        var a = yu(e);
        return a === 13 ? "Enter" : String.fromCharCode(a);
      }
      return e.type === "keydown" || e.type === "keyup" ? nh[e.keyCode] || "Unidentified" : "";
    }
    var my = {
      Alt: "altKey",
      Control: "ctrlKey",
      Meta: "metaKey",
      Shift: "shiftKey"
    };
    function rh(e) {
      var t = this, a = t.nativeEvent;
      if (a.getModifierState)
        return a.getModifierState(e);
      var i = my[e];
      return i ? !!a[i] : !1;
    }
    function Vd(e) {
      return rh;
    }
    var yy = lt({}, gu, {
      key: bn,
      code: 0,
      location: 0,
      ctrlKey: 0,
      shiftKey: 0,
      altKey: 0,
      metaKey: 0,
      repeat: 0,
      locale: 0,
      getModifierState: Vd,
      // Legacy Interface
      charCode: function(e) {
        return e.type === "keypress" ? yu(e) : 0;
      },
      keyCode: function(e) {
        return e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
      },
      which: function(e) {
        return e.type === "keypress" ? yu(e) : e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
      }
    }), ah = Sn(yy), ih = lt({}, xi, {
      pointerId: 0,
      width: 0,
      height: 0,
      pressure: 0,
      tangentialPressure: 0,
      tiltX: 0,
      tiltY: 0,
      twist: 0,
      pointerType: 0,
      isPrimary: 0
    }), lh = Sn(ih), Ia = lt({}, gu, {
      touches: 0,
      targetTouches: 0,
      changedTouches: 0,
      altKey: 0,
      metaKey: 0,
      ctrlKey: 0,
      shiftKey: 0,
      getModifierState: Vd
    }), Pd = Sn(Ia), gy = lt({}, Yn, {
      propertyName: 0,
      elapsedTime: 0,
      pseudoElement: 0
    }), zl = Sn(gy), af = lt({}, xi, {
      deltaX: function(e) {
        return "deltaX" in e ? e.deltaX : (
          // Fallback to `wheelDeltaX` for Webkit and normalize (right is positive).
          "wheelDeltaX" in e ? -e.wheelDeltaX : 0
        );
      },
      deltaY: function(e) {
        return "deltaY" in e ? e.deltaY : (
          // Fallback to `wheelDeltaY` for Webkit and normalize (down is positive).
          "wheelDeltaY" in e ? -e.wheelDeltaY : (
            // Fallback to `wheelDelta` for IE<9 and normalize (down is positive).
            "wheelDelta" in e ? -e.wheelDelta : 0
          )
        );
      },
      deltaZ: 0,
      // Browsers without "deltaMode" is reporting in raw wheel delta where one
      // notch on the scroll is always +/- 120, roughly equivalent to pixels.
      // A good approximation of DOM_DELTA_LINE (1) is 5% of viewport size or
      // ~40 pixels, for DOM_DELTA_SCREEN (2) it is 87.5% of viewport size.
      deltaMode: 0
    }), Eu = Sn(af), lf = [9, 13, 27, 32], uf = 229, Ds = vn && "CompositionEvent" in window, Os = null;
    vn && "documentMode" in document && (Os = document.documentMode);
    var Bd = vn && "TextEvent" in window && !Os, uh = vn && (!Ds || Os && Os > 8 && Os <= 11), $d = 32, Yd = String.fromCharCode($d);
    function of() {
      hr("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]), hr("onCompositionEnd", ["compositionend", "focusout", "keydown", "keypress", "keyup", "mousedown"]), hr("onCompositionStart", ["compositionstart", "focusout", "keydown", "keypress", "keyup", "mousedown"]), hr("onCompositionUpdate", ["compositionupdate", "focusout", "keydown", "keypress", "keyup", "mousedown"]);
    }
    var Ls = !1;
    function oh(e) {
      return (e.ctrlKey || e.altKey || e.metaKey) && // ctrlKey && altKey is equivalent to AltGr, and is not a command.
      !(e.ctrlKey && e.altKey);
    }
    function Id(e) {
      switch (e) {
        case "compositionstart":
          return "onCompositionStart";
        case "compositionend":
          return "onCompositionEnd";
        case "compositionupdate":
          return "onCompositionUpdate";
      }
    }
    function Sy(e, t) {
      return e === "keydown" && t.keyCode === uf;
    }
    function Qd(e, t) {
      switch (e) {
        case "keyup":
          return lf.indexOf(t.keyCode) !== -1;
        case "keydown":
          return t.keyCode !== uf;
        case "keypress":
        case "mousedown":
        case "focusout":
          return !0;
        default:
          return !1;
      }
    }
    function sf(e) {
      var t = e.detail;
      return typeof t == "object" && "data" in t ? t.data : null;
    }
    function Ms(e) {
      return e.locale === "ko";
    }
    var Ul = !1;
    function cf(e, t, a, i, u) {
      var s, f;
      if (Ds ? s = Id(t) : Ul ? Qd(t, i) && (s = "onCompositionEnd") : Sy(t, i) && (s = "onCompositionStart"), !s)
        return null;
      uh && !Ms(i) && (!Ul && s === "onCompositionStart" ? Ul = Jc(u) : s === "onCompositionEnd" && Ul && (f = ef()));
      var p = vh(a, s);
      if (p.length > 0) {
        var v = new Nl(s, t, null, i, u);
        if (e.push({
          event: v,
          listeners: p
        }), f)
          v.data = f;
        else {
          var y = sf(i);
          y !== null && (v.data = y);
        }
      }
    }
    function sh(e, t) {
      switch (e) {
        case "compositionend":
          return sf(t);
        case "keypress":
          var a = t.which;
          return a !== $d ? null : (Ls = !0, Yd);
        case "textInput":
          var i = t.data;
          return i === Yd && Ls ? null : i;
        default:
          return null;
      }
    }
    function Ey(e, t) {
      if (Ul) {
        if (e === "compositionend" || !Ds && Qd(e, t)) {
          var a = ef();
          return bs(), Ul = !1, a;
        }
        return null;
      }
      switch (e) {
        case "paste":
          return null;
        case "keypress":
          if (!oh(t)) {
            if (t.char && t.char.length > 1)
              return t.char;
            if (t.which)
              return String.fromCharCode(t.which);
          }
          return null;
        case "compositionend":
          return uh && !Ms(t) ? null : t.data;
        default:
          return null;
      }
    }
    function ff(e, t, a, i, u) {
      var s;
      if (Bd ? s = sh(t, i) : s = Ey(t, i), !s)
        return null;
      var f = vh(a, "onBeforeInput");
      if (f.length > 0) {
        var p = new hy("onBeforeInput", "beforeinput", null, i, u);
        e.push({
          event: p,
          listeners: f
        }), p.data = s;
      }
    }
    function Cy(e, t, a, i, u, s, f) {
      cf(e, t, a, i, u), ff(e, t, a, i, u);
    }
    var Ns = {
      color: !0,
      date: !0,
      datetime: !0,
      "datetime-local": !0,
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
      week: !0
    };
    function ch(e) {
      var t = e && e.nodeName && e.nodeName.toLowerCase();
      return t === "input" ? !!Ns[e.type] : t === "textarea";
    }
    /**
     * Checks if an event is supported in the current execution environment.
     *
     * NOTE: This will not work correctly for non-generic events such as `change`,
     * `reset`, `load`, `error`, and `select`.
     *
     * Borrows from Modernizr.
     *
     * @param {string} eventNameSuffix Event name, e.g. "click".
     * @return {boolean} True if the event is supported.
     * @internal
     * @license Modernizr 3.0.0pre (Custom Build) | MIT
     */
    function df(e) {
      if (!vn)
        return !1;
      var t = "on" + e, a = t in document;
      if (!a) {
        var i = document.createElement("div");
        i.setAttribute(t, "return;"), a = typeof i[t] == "function";
      }
      return a;
    }
    function n() {
      hr("onChange", ["change", "click", "focusin", "focusout", "input", "keydown", "keyup", "selectionchange"]);
    }
    function r(e, t, a, i) {
      cc(i);
      var u = vh(t, "onChange");
      if (u.length > 0) {
        var s = new tf("onChange", "change", null, a, i);
        e.push({
          event: s,
          listeners: u
        });
      }
    }
    var l = null, o = null;
    function c(e) {
      var t = e.nodeName && e.nodeName.toLowerCase();
      return t === "select" || t === "input" && e.type === "file";
    }
    function d(e) {
      var t = [];
      r(t, o, e, sc(e)), ud(m, t);
    }
    function m(e) {
      O0(e, 0);
    }
    function E(e) {
      var t = gf(e);
      if (Bu(t))
        return e;
    }
    function T(e, t) {
      if (e === "change")
        return t;
    }
    var U = !1;
    vn && (U = df("input") && (!document.documentMode || document.documentMode > 9));
    function W(e, t) {
      l = e, o = t, l.attachEvent("onpropertychange", I);
    }
    function G() {
      l && (l.detachEvent("onpropertychange", I), l = null, o = null);
    }
    function I(e) {
      e.propertyName === "value" && E(o) && d(e);
    }
    function ce(e, t, a) {
      e === "focusin" ? (G(), W(t, a)) : e === "focusout" && G();
    }
    function ye(e, t) {
      if (e === "selectionchange" || e === "keyup" || e === "keydown")
        return E(o);
    }
    function Ee(e) {
      var t = e.nodeName;
      return t && t.toLowerCase() === "input" && (e.type === "checkbox" || e.type === "radio");
    }
    function Mn(e, t) {
      if (e === "click")
        return E(t);
    }
    function D(e, t) {
      if (e === "input" || e === "change")
        return E(t);
    }
    function w(e) {
      var t = e._wrapperState;
      !t || !t.controlled || e.type !== "number" || Ne(e, "number", e.value);
    }
    function M(e, t, a, i, u, s, f) {
      var p = a ? gf(a) : window, v, y;
      if (c(p) ? v = T : ch(p) ? U ? v = D : (v = ye, y = ce) : Ee(p) && (v = Mn), v) {
        var g = v(t, a);
        if (g) {
          r(e, g, i, u);
          return;
        }
      }
      y && y(t, p, a), t === "focusout" && w(p);
    }
    function Z() {
      Br("onMouseEnter", ["mouseout", "mouseover"]), Br("onMouseLeave", ["mouseout", "mouseover"]), Br("onPointerEnter", ["pointerout", "pointerover"]), Br("onPointerLeave", ["pointerout", "pointerover"]);
    }
    function Re(e, t, a, i, u, s, f) {
      var p = t === "mouseover" || t === "pointerover", v = t === "mouseout" || t === "pointerout";
      if (p && !Tv(i)) {
        var y = i.relatedTarget || i.fromElement;
        if (y && (As(y) || lp(y)))
          return;
      }
      if (!(!v && !p)) {
        var g;
        if (u.window === u)
          g = u;
        else {
          var b = u.ownerDocument;
          b ? g = b.defaultView || b.parentWindow : g = window;
        }
        var x, N;
        if (v) {
          var A = i.relatedTarget || i.toElement;
          if (x = a, N = A ? As(A) : null, N !== null) {
            var F = ga(N);
            (N !== F || N.tag !== ue && N.tag !== Ye) && (N = null);
          }
        } else
          x = null, N = a;
        if (x !== N) {
          var le = nf, Me = "onMouseLeave", we = "onMouseEnter", wt = "mouse";
          (t === "pointerout" || t === "pointerover") && (le = lh, Me = "onPointerLeave", we = "onPointerEnter", wt = "pointer");
          var gt = x == null ? g : gf(x), O = N == null ? g : gf(N), H = new le(Me, wt + "leave", x, i, u);
          H.target = gt, H.relatedTarget = O;
          var L = null, X = As(u);
          if (X === a) {
            var ve = new le(we, wt + "enter", N, i, u);
            ve.target = O, ve.relatedTarget = gt, L = ve;
          }
          OR(e, H, L, x, N);
        }
      }
    }
    function Fe(e, t) {
      return e === t && (e !== 0 || 1 / e === 1 / t) || e !== e && t !== t;
    }
    var ge = typeof Object.is == "function" ? Object.is : Fe;
    function He(e, t) {
      if (ge(e, t))
        return !0;
      if (typeof e != "object" || e === null || typeof t != "object" || t === null)
        return !1;
      var a = Object.keys(e), i = Object.keys(t);
      if (a.length !== i.length)
        return !1;
      for (var u = 0; u < a.length; u++) {
        var s = a[u];
        if (!Wn.call(t, s) || !ge(e[s], t[s]))
          return !1;
      }
      return !0;
    }
    function In(e) {
      for (; e && e.firstChild; )
        e = e.firstChild;
      return e;
    }
    function Nt(e) {
      for (; e; ) {
        if (e.nextSibling)
          return e.nextSibling;
        e = e.parentNode;
      }
    }
    function Xi(e, t) {
      for (var a = In(e), i = 0, u = 0; a; ) {
        if (a.nodeType === Fi) {
          if (u = i + a.textContent.length, i <= t && u >= t)
            return {
              node: a,
              offset: t - i
            };
          i = u;
        }
        a = In(Nt(a));
      }
    }
    function Ry(e) {
      var t = e.ownerDocument, a = t && t.defaultView || window, i = a.getSelection && a.getSelection();
      if (!i || i.rangeCount === 0)
        return null;
      var u = i.anchorNode, s = i.anchorOffset, f = i.focusNode, p = i.focusOffset;
      try {
        u.nodeType, f.nodeType;
      } catch {
        return null;
      }
      return cR(e, u, s, f, p);
    }
    function cR(e, t, a, i, u) {
      var s = 0, f = -1, p = -1, v = 0, y = 0, g = e, b = null;
      e:
        for (; ; ) {
          for (var x = null; g === t && (a === 0 || g.nodeType === Fi) && (f = s + a), g === i && (u === 0 || g.nodeType === Fi) && (p = s + u), g.nodeType === Fi && (s += g.nodeValue.length), (x = g.firstChild) !== null; )
            b = g, g = x;
          for (; ; ) {
            if (g === e)
              break e;
            if (b === t && ++v === a && (f = s), b === i && ++y === u && (p = s), (x = g.nextSibling) !== null)
              break;
            g = b, b = g.parentNode;
          }
          g = x;
        }
      return f === -1 || p === -1 ? null : {
        start: f,
        end: p
      };
    }
    function fR(e, t) {
      var a = e.ownerDocument || document, i = a && a.defaultView || window;
      if (i.getSelection) {
        var u = i.getSelection(), s = e.textContent.length, f = Math.min(t.start, s), p = t.end === void 0 ? f : Math.min(t.end, s);
        if (!u.extend && f > p) {
          var v = p;
          p = f, f = v;
        }
        var y = Xi(e, f), g = Xi(e, p);
        if (y && g) {
          if (u.rangeCount === 1 && u.anchorNode === y.node && u.anchorOffset === y.offset && u.focusNode === g.node && u.focusOffset === g.offset)
            return;
          var b = a.createRange();
          b.setStart(y.node, y.offset), u.removeAllRanges(), f > p ? (u.addRange(b), u.extend(g.node, g.offset)) : (b.setEnd(g.node, g.offset), u.addRange(b));
        }
      }
    }
    function g0(e) {
      return e && e.nodeType === Fi;
    }
    function S0(e, t) {
      return !e || !t ? !1 : e === t ? !0 : g0(e) ? !1 : g0(t) ? S0(e, t.parentNode) : "contains" in e ? e.contains(t) : e.compareDocumentPosition ? !!(e.compareDocumentPosition(t) & 16) : !1;
    }
    function dR(e) {
      return e && e.ownerDocument && S0(e.ownerDocument.documentElement, e);
    }
    function pR(e) {
      try {
        return typeof e.contentWindow.location.href == "string";
      } catch {
        return !1;
      }
    }
    function E0() {
      for (var e = window, t = Sl(); t instanceof e.HTMLIFrameElement; ) {
        if (pR(t))
          e = t.contentWindow;
        else
          return t;
        t = Sl(e.document);
      }
      return t;
    }
    function Ty(e) {
      var t = e && e.nodeName && e.nodeName.toLowerCase();
      return t && (t === "input" && (e.type === "text" || e.type === "search" || e.type === "tel" || e.type === "url" || e.type === "password") || t === "textarea" || e.contentEditable === "true");
    }
    function vR() {
      var e = E0();
      return {
        focusedElem: e,
        selectionRange: Ty(e) ? mR(e) : null
      };
    }
    function hR(e) {
      var t = E0(), a = e.focusedElem, i = e.selectionRange;
      if (t !== a && dR(a)) {
        i !== null && Ty(a) && yR(a, i);
        for (var u = [], s = a; s = s.parentNode; )
          s.nodeType === Xr && u.push({
            element: s,
            left: s.scrollLeft,
            top: s.scrollTop
          });
        typeof a.focus == "function" && a.focus();
        for (var f = 0; f < u.length; f++) {
          var p = u[f];
          p.element.scrollLeft = p.left, p.element.scrollTop = p.top;
        }
      }
    }
    function mR(e) {
      var t;
      return "selectionStart" in e ? t = {
        start: e.selectionStart,
        end: e.selectionEnd
      } : t = Ry(e), t || {
        start: 0,
        end: 0
      };
    }
    function yR(e, t) {
      var a = t.start, i = t.end;
      i === void 0 && (i = a), "selectionStart" in e ? (e.selectionStart = a, e.selectionEnd = Math.min(i, e.value.length)) : fR(e, t);
    }
    var gR = vn && "documentMode" in document && document.documentMode <= 11;
    function SR() {
      hr("onSelect", ["focusout", "contextmenu", "dragend", "focusin", "keydown", "keyup", "mousedown", "mouseup", "selectionchange"]);
    }
    var pf = null, xy = null, Wd = null, wy = !1;
    function ER(e) {
      if ("selectionStart" in e && Ty(e))
        return {
          start: e.selectionStart,
          end: e.selectionEnd
        };
      var t = e.ownerDocument && e.ownerDocument.defaultView || window, a = t.getSelection();
      return {
        anchorNode: a.anchorNode,
        anchorOffset: a.anchorOffset,
        focusNode: a.focusNode,
        focusOffset: a.focusOffset
      };
    }
    function CR(e) {
      return e.window === e ? e.document : e.nodeType === ai ? e : e.ownerDocument;
    }
    function C0(e, t, a) {
      var i = CR(a);
      if (!(wy || pf == null || pf !== Sl(i))) {
        var u = ER(pf);
        if (!Wd || !He(Wd, u)) {
          Wd = u;
          var s = vh(xy, "onSelect");
          if (s.length > 0) {
            var f = new tf("onSelect", "select", null, t, a);
            e.push({
              event: f,
              listeners: s
            }), f.target = pf;
          }
        }
      }
    }
    function RR(e, t, a, i, u, s, f) {
      var p = a ? gf(a) : window;
      switch (t) {
        case "focusin":
          (ch(p) || p.contentEditable === "true") && (pf = p, xy = a, Wd = null);
          break;
        case "focusout":
          pf = null, xy = null, Wd = null;
          break;
        case "mousedown":
          wy = !0;
          break;
        case "contextmenu":
        case "mouseup":
        case "dragend":
          wy = !1, C0(e, i, u);
          break;
        case "selectionchange":
          if (gR)
            break;
        case "keydown":
        case "keyup":
          C0(e, i, u);
      }
    }
    function fh(e, t) {
      var a = {};
      return a[e.toLowerCase()] = t.toLowerCase(), a["Webkit" + e] = "webkit" + t, a["Moz" + e] = "moz" + t, a;
    }
    var vf = {
      animationend: fh("Animation", "AnimationEnd"),
      animationiteration: fh("Animation", "AnimationIteration"),
      animationstart: fh("Animation", "AnimationStart"),
      transitionend: fh("Transition", "TransitionEnd")
    }, by = {}, R0 = {};
    vn && (R0 = document.createElement("div").style, "AnimationEvent" in window || (delete vf.animationend.animation, delete vf.animationiteration.animation, delete vf.animationstart.animation), "TransitionEvent" in window || delete vf.transitionend.transition);
    function dh(e) {
      if (by[e])
        return by[e];
      if (!vf[e])
        return e;
      var t = vf[e];
      for (var a in t)
        if (t.hasOwnProperty(a) && a in R0)
          return by[e] = t[a];
      return e;
    }
    var T0 = dh("animationend"), x0 = dh("animationiteration"), w0 = dh("animationstart"), b0 = dh("transitionend"), _0 = /* @__PURE__ */ new Map(), k0 = ["abort", "auxClick", "cancel", "canPlay", "canPlayThrough", "click", "close", "contextMenu", "copy", "cut", "drag", "dragEnd", "dragEnter", "dragExit", "dragLeave", "dragOver", "dragStart", "drop", "durationChange", "emptied", "encrypted", "ended", "error", "gotPointerCapture", "input", "invalid", "keyDown", "keyPress", "keyUp", "load", "loadedData", "loadedMetadata", "loadStart", "lostPointerCapture", "mouseDown", "mouseMove", "mouseOut", "mouseOver", "mouseUp", "paste", "pause", "play", "playing", "pointerCancel", "pointerDown", "pointerMove", "pointerOut", "pointerOver", "pointerUp", "progress", "rateChange", "reset", "resize", "seeked", "seeking", "stalled", "submit", "suspend", "timeUpdate", "touchCancel", "touchEnd", "touchStart", "volumeChange", "scroll", "toggle", "touchMove", "waiting", "wheel"];
    function ko(e, t) {
      _0.set(e, t), hr(t, [e]);
    }
    function TR() {
      for (var e = 0; e < k0.length; e++) {
        var t = k0[e], a = t.toLowerCase(), i = t[0].toUpperCase() + t.slice(1);
        ko(a, "on" + i);
      }
      ko(T0, "onAnimationEnd"), ko(x0, "onAnimationIteration"), ko(w0, "onAnimationStart"), ko("dblclick", "onDoubleClick"), ko("focusin", "onFocus"), ko("focusout", "onBlur"), ko(b0, "onTransitionEnd");
    }
    function xR(e, t, a, i, u, s, f) {
      var p = _0.get(t);
      if (p !== void 0) {
        var v = tf, y = t;
        switch (t) {
          case "keypress":
            if (yu(i) === 0)
              return;
          case "keydown":
          case "keyup":
            v = ah;
            break;
          case "focusin":
            y = "focus", v = ks;
            break;
          case "focusout":
            y = "blur", v = ks;
            break;
          case "beforeblur":
          case "afterblur":
            v = ks;
            break;
          case "click":
            if (i.button === 2)
              return;
          case "auxclick":
          case "dblclick":
          case "mousedown":
          case "mousemove":
          case "mouseup":
          case "mouseout":
          case "mouseover":
          case "contextmenu":
            v = nf;
            break;
          case "drag":
          case "dragend":
          case "dragenter":
          case "dragexit":
          case "dragleave":
          case "dragover":
          case "dragstart":
          case "drop":
            v = Zv;
            break;
          case "touchcancel":
          case "touchend":
          case "touchmove":
          case "touchstart":
            v = Pd;
            break;
          case T0:
          case x0:
          case w0:
            v = py;
            break;
          case b0:
            v = zl;
            break;
          case "scroll":
            v = jd;
            break;
          case "wheel":
            v = Eu;
            break;
          case "copy":
          case "cut":
          case "paste":
            v = eh;
            break;
          case "gotpointercapture":
          case "lostpointercapture":
          case "pointercancel":
          case "pointerdown":
          case "pointermove":
          case "pointerout":
          case "pointerover":
          case "pointerup":
            v = lh;
            break;
        }
        var g = (s & Jl) !== 0;
        {
          var b = !g && // TODO: ideally, we'd eventually add all events from
          // nonDelegatedEvents list in DOMPluginEventSystem.
          // Then we can remove this special list.
          // This is a breaking change that can wait until React 18.
          t === "scroll", x = kR(a, p, i.type, g, b);
          if (x.length > 0) {
            var N = new v(p, y, null, i, u);
            e.push({
              event: N,
              listeners: x
            });
          }
        }
      }
    }
    TR(), Z(), n(), SR(), of();
    function wR(e, t, a, i, u, s, f) {
      xR(e, t, a, i, u, s);
      var p = (s & ey) === 0;
      p && (Re(e, t, a, i, u), M(e, t, a, i, u), RR(e, t, a, i, u), Cy(e, t, a, i, u));
    }
    var Gd = ["abort", "canplay", "canplaythrough", "durationchange", "emptied", "encrypted", "ended", "error", "loadeddata", "loadedmetadata", "loadstart", "pause", "play", "playing", "progress", "ratechange", "resize", "seeked", "seeking", "stalled", "suspend", "timeupdate", "volumechange", "waiting"], _y = new Set(["cancel", "close", "invalid", "load", "scroll", "toggle"].concat(Gd));
    function D0(e, t, a) {
      var i = e.type || "unknown-event";
      e.currentTarget = a, Bi(i, t, void 0, e), e.currentTarget = null;
    }
    function bR(e, t, a) {
      var i;
      if (a)
        for (var u = t.length - 1; u >= 0; u--) {
          var s = t[u], f = s.instance, p = s.currentTarget, v = s.listener;
          if (f !== i && e.isPropagationStopped())
            return;
          D0(e, v, p), i = f;
        }
      else
        for (var y = 0; y < t.length; y++) {
          var g = t[y], b = g.instance, x = g.currentTarget, N = g.listener;
          if (b !== i && e.isPropagationStopped())
            return;
          D0(e, N, x), i = b;
        }
    }
    function O0(e, t) {
      for (var a = (t & Jl) !== 0, i = 0; i < e.length; i++) {
        var u = e[i], s = u.event, f = u.listeners;
        bR(s, f, a);
      }
      fd();
    }
    function _R(e, t, a, i, u) {
      var s = sc(a), f = [];
      wR(f, e, i, a, s, t), O0(f, t);
    }
    function En(e, t) {
      _y.has(e) || S('Did not expect a listenToNonDelegatedEvent() call for "%s". This is a bug in React. Please file an issue.', e);
      var a = !1, i = rx(t), u = LR(e, a);
      i.has(u) || (L0(t, e, ns, a), i.add(u));
    }
    function ky(e, t, a) {
      _y.has(e) && !t && S('Did not expect a listenToNativeEvent() call for "%s" in the bubble phase. This is a bug in React. Please file an issue.', e);
      var i = 0;
      t && (i |= Jl), L0(a, e, i, t);
    }
    var ph = "_reactListening" + Math.random().toString(36).slice(2);
    function qd(e) {
      if (!e[ph]) {
        e[ph] = !0, st.forEach(function(a) {
          a !== "selectionchange" && (_y.has(a) || ky(a, !1, e), ky(a, !0, e));
        });
        var t = e.nodeType === ai ? e : e.ownerDocument;
        t !== null && (t[ph] || (t[ph] = !0, ky("selectionchange", !1, t)));
      }
    }
    function L0(e, t, a, i, u) {
      var s = $n(e, t, a), f = void 0;
      us && (t === "touchstart" || t === "touchmove" || t === "wheel") && (f = !0), e = e, i ? f !== void 0 ? Zc(e, t, s, f) : Gi(e, t, s) : f !== void 0 ? Ad(e, t, s, f) : xo(e, t, s);
    }
    function M0(e, t) {
      return e === t || e.nodeType === An && e.parentNode === t;
    }
    function Dy(e, t, a, i, u) {
      var s = i;
      if (!(t & Vi) && !(t & ns)) {
        var f = u;
        if (i !== null) {
          var p = i;
          e:
            for (; ; ) {
              if (p === null)
                return;
              var v = p.tag;
              if (v === re || v === pe) {
                var y = p.stateNode.containerInfo;
                if (M0(y, f))
                  break;
                if (v === pe)
                  for (var g = p.return; g !== null; ) {
                    var b = g.tag;
                    if (b === re || b === pe) {
                      var x = g.stateNode.containerInfo;
                      if (M0(x, f))
                        return;
                    }
                    g = g.return;
                  }
                for (; y !== null; ) {
                  var N = As(y);
                  if (N === null)
                    return;
                  var A = N.tag;
                  if (A === ue || A === Ye) {
                    p = s = N;
                    continue e;
                  }
                  y = y.parentNode;
                }
              }
              p = p.return;
            }
        }
      }
      ud(function() {
        return _R(e, t, a, s);
      });
    }
    function Xd(e, t, a) {
      return {
        instance: e,
        listener: t,
        currentTarget: a
      };
    }
    function kR(e, t, a, i, u, s) {
      for (var f = t !== null ? t + "Capture" : null, p = i ? f : t, v = [], y = e, g = null; y !== null; ) {
        var b = y, x = b.stateNode, N = b.tag;
        if (N === ue && x !== null && (g = x, p !== null)) {
          var A = tu(y, p);
          A != null && v.push(Xd(y, A, g));
        }
        if (u)
          break;
        y = y.return;
      }
      return v;
    }
    function vh(e, t) {
      for (var a = t + "Capture", i = [], u = e; u !== null; ) {
        var s = u, f = s.stateNode, p = s.tag;
        if (p === ue && f !== null) {
          var v = f, y = tu(u, a);
          y != null && i.unshift(Xd(u, y, v));
          var g = tu(u, t);
          g != null && i.push(Xd(u, g, v));
        }
        u = u.return;
      }
      return i;
    }
    function hf(e) {
      if (e === null)
        return null;
      do
        e = e.return;
      while (e && e.tag !== ue);
      return e || null;
    }
    function DR(e, t) {
      for (var a = e, i = t, u = 0, s = a; s; s = hf(s))
        u++;
      for (var f = 0, p = i; p; p = hf(p))
        f++;
      for (; u - f > 0; )
        a = hf(a), u--;
      for (; f - u > 0; )
        i = hf(i), f--;
      for (var v = u; v--; ) {
        if (a === i || i !== null && a === i.alternate)
          return a;
        a = hf(a), i = hf(i);
      }
      return null;
    }
    function N0(e, t, a, i, u) {
      for (var s = t._reactName, f = [], p = a; p !== null && p !== i; ) {
        var v = p, y = v.alternate, g = v.stateNode, b = v.tag;
        if (y !== null && y === i)
          break;
        if (b === ue && g !== null) {
          var x = g;
          if (u) {
            var N = tu(p, s);
            N != null && f.unshift(Xd(p, N, x));
          } else if (!u) {
            var A = tu(p, s);
            A != null && f.push(Xd(p, A, x));
          }
        }
        p = p.return;
      }
      f.length !== 0 && e.push({
        event: t,
        listeners: f
      });
    }
    function OR(e, t, a, i, u) {
      var s = i && u ? DR(i, u) : null;
      i !== null && N0(e, t, i, s, !1), u !== null && a !== null && N0(e, a, u, s, !0);
    }
    function LR(e, t) {
      return e + "__" + (t ? "capture" : "bubble");
    }
    var Qa = !1, Kd = "dangerouslySetInnerHTML", hh = "suppressContentEditableWarning", Do = "suppressHydrationWarning", z0 = "autoFocus", zs = "children", Us = "style", mh = "__html", Oy, yh, Zd, U0, gh, A0, j0;
    Oy = {
      // There are working polyfills for <dialog>. Let people use it.
      dialog: !0,
      // Electron ships a custom <webview> tag to display external web content in
      // an isolated frame and process.
      // This tag is not present in non Electron environments such as JSDom which
      // is often used for testing purposes.
      // @see https://electronjs.org/docs/api/webview-tag
      webview: !0
    }, yh = function(e, t) {
      oc(e, t), nd(e, t), Rv(e, t, {
        registrationNameDependencies: ct,
        possibleRegistrationNames: en
      });
    }, A0 = vn && !document.documentMode, Zd = function(e, t, a) {
      if (!Qa) {
        var i = Sh(a), u = Sh(t);
        u !== i && (Qa = !0, S("Prop `%s` did not match. Server: %s Client: %s", e, JSON.stringify(u), JSON.stringify(i)));
      }
    }, U0 = function(e) {
      if (!Qa) {
        Qa = !0;
        var t = [];
        e.forEach(function(a) {
          t.push(a);
        }), S("Extra attributes from the server: %s", t);
      }
    }, gh = function(e, t) {
      t === !1 ? S("Expected `%s` listener to be a function, instead got `false`.\n\nIf you used to conditionally omit it with %s={condition && value}, pass %s={condition ? value : undefined} instead.", e, e, e) : S("Expected `%s` listener to be a function, instead got a value of `%s` type.", e, typeof t);
    }, j0 = function(e, t) {
      var a = e.namespaceURI === ji ? e.ownerDocument.createElement(e.tagName) : e.ownerDocument.createElementNS(e.namespaceURI, e.tagName);
      return a.innerHTML = t, a.innerHTML;
    };
    var MR = /\r\n?/g, NR = /\u0000|\uFFFD/g;
    function Sh(e) {
      Ir(e);
      var t = typeof e == "string" ? e : "" + e;
      return t.replace(MR, `
`).replace(NR, "");
    }
    function Eh(e, t, a, i) {
      var u = Sh(t), s = Sh(e);
      if (s !== u && (i && (Qa || (Qa = !0, S('Text content did not match. Server: "%s" Client: "%s"', s, u))), a && me))
        throw new Error("Text content does not match server-rendered HTML.");
    }
    function F0(e) {
      return e.nodeType === ai ? e : e.ownerDocument;
    }
    function zR() {
    }
    function Ch(e) {
      e.onclick = zR;
    }
    function UR(e, t, a, i, u) {
      for (var s in i)
        if (i.hasOwnProperty(s)) {
          var f = i[s];
          if (s === Us)
            f && Object.freeze(f), dv(t, f);
          else if (s === Kd) {
            var p = f ? f[mh] : void 0;
            p != null && tv(t, p);
          } else if (s === zs)
            if (typeof f == "string") {
              var v = e !== "textarea" || f !== "";
              v && ac(t, f);
            } else
              typeof f == "number" && ac(t, "" + f);
          else
            s === hh || s === Do || s === z0 || (ct.hasOwnProperty(s) ? f != null && (typeof f != "function" && gh(s, f), s === "onScroll" && En("scroll", t)) : f != null && ha(t, s, f, u));
        }
    }
    function AR(e, t, a, i) {
      for (var u = 0; u < t.length; u += 2) {
        var s = t[u], f = t[u + 1];
        s === Us ? dv(e, f) : s === Kd ? tv(e, f) : s === zs ? ac(e, f) : ha(e, s, f, i);
      }
    }
    function jR(e, t, a, i) {
      var u, s = F0(a), f, p = i;
      if (p === ji && (p = nc(e)), p === ji) {
        if (u = Hi(e, t), !u && e !== e.toLowerCase() && S("<%s /> is using incorrect casing. Use PascalCase for React components, or lowercase for HTML elements.", e), e === "script") {
          var v = s.createElement("div");
          v.innerHTML = "<script><\/script>";
          var y = v.firstChild;
          f = v.removeChild(y);
        } else if (typeof t.is == "string")
          f = s.createElement(e, {
            is: t.is
          });
        else if (f = s.createElement(e), e === "select") {
          var g = f;
          t.multiple ? g.multiple = !0 : t.size && (g.size = t.size);
        }
      } else
        f = s.createElementNS(p, e);
      return p === ji && !u && Object.prototype.toString.call(f) === "[object HTMLUnknownElement]" && !Wn.call(Oy, e) && (Oy[e] = !0, S("The tag <%s> is unrecognized in this browser. If you meant to render a React component, start its name with an uppercase letter.", e)), f;
    }
    function FR(e, t) {
      return F0(t).createTextNode(e);
    }
    function HR(e, t, a, i) {
      var u = Hi(t, a);
      yh(t, a);
      var s;
      switch (t) {
        case "dialog":
          En("cancel", e), En("close", e), s = a;
          break;
        case "iframe":
        case "object":
        case "embed":
          En("load", e), s = a;
          break;
        case "video":
        case "audio":
          for (var f = 0; f < Gd.length; f++)
            En(Gd[f], e);
          s = a;
          break;
        case "source":
          En("error", e), s = a;
          break;
        case "img":
        case "image":
        case "link":
          En("error", e), En("load", e), s = a;
          break;
        case "details":
          En("toggle", e), s = a;
          break;
        case "input":
          C(e, a), s = h(e, a), En("invalid", e);
          break;
        case "option":
          Qt(e, a), s = a;
          break;
        case "select":
          Zo(e, a), s = Ko(e, a), En("invalid", e);
          break;
        case "textarea":
          Zp(e, a), s = Wf(e, a), En("invalid", e);
          break;
        default:
          s = a;
      }
      switch (lc(t, s), UR(t, e, i, s, u), t) {
        case "input":
          La(e), K(e, a, !1);
          break;
        case "textarea":
          La(e), ev(e);
          break;
        case "option":
          Zt(e, a);
          break;
        case "select":
          If(e, a);
          break;
        default:
          typeof s.onClick == "function" && Ch(e);
          break;
      }
    }
    function VR(e, t, a, i, u) {
      yh(t, i);
      var s = null, f, p;
      switch (t) {
        case "input":
          f = h(e, a), p = h(e, i), s = [];
          break;
        case "select":
          f = Ko(e, a), p = Ko(e, i), s = [];
          break;
        case "textarea":
          f = Wf(e, a), p = Wf(e, i), s = [];
          break;
        default:
          f = a, p = i, typeof f.onClick != "function" && typeof p.onClick == "function" && Ch(e);
          break;
      }
      lc(t, p);
      var v, y, g = null;
      for (v in f)
        if (!(p.hasOwnProperty(v) || !f.hasOwnProperty(v) || f[v] == null))
          if (v === Us) {
            var b = f[v];
            for (y in b)
              b.hasOwnProperty(y) && (g || (g = {}), g[y] = "");
          } else
            v === Kd || v === zs || v === hh || v === Do || v === z0 || (ct.hasOwnProperty(v) ? s || (s = []) : (s = s || []).push(v, null));
      for (v in p) {
        var x = p[v], N = f != null ? f[v] : void 0;
        if (!(!p.hasOwnProperty(v) || x === N || x == null && N == null))
          if (v === Us)
            if (x && Object.freeze(x), N) {
              for (y in N)
                N.hasOwnProperty(y) && (!x || !x.hasOwnProperty(y)) && (g || (g = {}), g[y] = "");
              for (y in x)
                x.hasOwnProperty(y) && N[y] !== x[y] && (g || (g = {}), g[y] = x[y]);
            } else
              g || (s || (s = []), s.push(v, g)), g = x;
          else if (v === Kd) {
            var A = x ? x[mh] : void 0, F = N ? N[mh] : void 0;
            A != null && F !== A && (s = s || []).push(v, A);
          } else
            v === zs ? (typeof x == "string" || typeof x == "number") && (s = s || []).push(v, "" + x) : v === hh || v === Do || (ct.hasOwnProperty(v) ? (x != null && (typeof x != "function" && gh(v, x), v === "onScroll" && En("scroll", e)), !s && N !== x && (s = [])) : (s = s || []).push(v, x));
      }
      return g && (es(g, p[Us]), (s = s || []).push(Us, g)), s;
    }
    function PR(e, t, a, i, u) {
      a === "input" && u.type === "radio" && u.name != null && z(e, u);
      var s = Hi(a, i), f = Hi(a, u);
      switch (AR(e, t, s, f), a) {
        case "input":
          j(e, u);
          break;
        case "textarea":
          Jp(e, u);
          break;
        case "select":
          Ym(e, u);
          break;
      }
    }
    function BR(e) {
      {
        var t = e.toLowerCase();
        return uc.hasOwnProperty(t) && uc[t] || null;
      }
    }
    function $R(e, t, a, i, u, s, f) {
      var p, v;
      switch (p = Hi(t, a), yh(t, a), t) {
        case "dialog":
          En("cancel", e), En("close", e);
          break;
        case "iframe":
        case "object":
        case "embed":
          En("load", e);
          break;
        case "video":
        case "audio":
          for (var y = 0; y < Gd.length; y++)
            En(Gd[y], e);
          break;
        case "source":
          En("error", e);
          break;
        case "img":
        case "image":
        case "link":
          En("error", e), En("load", e);
          break;
        case "details":
          En("toggle", e);
          break;
        case "input":
          C(e, a), En("invalid", e);
          break;
        case "option":
          Qt(e, a);
          break;
        case "select":
          Zo(e, a), En("invalid", e);
          break;
        case "textarea":
          Zp(e, a), En("invalid", e);
          break;
      }
      lc(t, a);
      {
        v = /* @__PURE__ */ new Set();
        for (var g = e.attributes, b = 0; b < g.length; b++) {
          var x = g[b].name.toLowerCase();
          switch (x) {
            case "value":
              break;
            case "checked":
              break;
            case "selected":
              break;
            default:
              v.add(g[b].name);
          }
        }
      }
      var N = null;
      for (var A in a)
        if (a.hasOwnProperty(A)) {
          var F = a[A];
          if (A === zs)
            typeof F == "string" ? e.textContent !== F && (a[Do] !== !0 && Eh(e.textContent, F, s, f), N = [zs, F]) : typeof F == "number" && e.textContent !== "" + F && (a[Do] !== !0 && Eh(e.textContent, F, s, f), N = [zs, "" + F]);
          else if (ct.hasOwnProperty(A))
            F != null && (typeof F != "function" && gh(A, F), A === "onScroll" && En("scroll", e));
          else if (f && // Convince Flow we've calculated it (it's DEV-only in this method.)
          typeof p == "boolean") {
            var le = void 0, Me = p && Ue ? null : br(A);
            if (a[Do] !== !0) {
              if (!(A === hh || A === Do || // Controlled attributes are not validated
              // TODO: Only ignore them on controlled tags.
              A === "value" || A === "checked" || A === "selected")) {
                if (A === Kd) {
                  var we = e.innerHTML, wt = F ? F[mh] : void 0;
                  if (wt != null) {
                    var gt = j0(e, wt);
                    gt !== we && Zd(A, we, gt);
                  }
                } else if (A === Us) {
                  if (v.delete(A), A0) {
                    var O = Zm(F);
                    le = e.getAttribute("style"), O !== le && Zd(A, le, O);
                  }
                } else if (p && !Ue)
                  v.delete(A.toLowerCase()), le = di(e, A, F), F !== le && Zd(A, le, F);
                else if (!mn(A, Me, p) && !It(A, F, Me, p)) {
                  var H = !1;
                  if (Me !== null)
                    v.delete(Me.attributeName), le = va(e, A, F, Me);
                  else {
                    var L = i;
                    if (L === ji && (L = nc(t)), L === ji)
                      v.delete(A.toLowerCase());
                    else {
                      var X = BR(A);
                      X !== null && X !== A && (H = !0, v.delete(X)), v.delete(A);
                    }
                    le = di(e, A, F);
                  }
                  var ve = Ue;
                  !ve && F !== le && !H && Zd(A, le, F);
                }
              }
            }
          }
        }
      switch (f && // $FlowFixMe - Should be inferred as not undefined.
      v.size > 0 && a[Do] !== !0 && U0(v), t) {
        case "input":
          La(e), K(e, a, !0);
          break;
        case "textarea":
          La(e), ev(e);
          break;
        case "select":
        case "option":
          break;
        default:
          typeof a.onClick == "function" && Ch(e);
          break;
      }
      return N;
    }
    function YR(e, t, a) {
      var i = e.nodeValue !== t;
      return i;
    }
    function Ly(e, t) {
      {
        if (Qa)
          return;
        Qa = !0, S("Did not expect server HTML to contain a <%s> in <%s>.", t.nodeName.toLowerCase(), e.nodeName.toLowerCase());
      }
    }
    function My(e, t) {
      {
        if (Qa)
          return;
        Qa = !0, S('Did not expect server HTML to contain the text node "%s" in <%s>.', t.nodeValue, e.nodeName.toLowerCase());
      }
    }
    function Ny(e, t, a) {
      {
        if (Qa)
          return;
        Qa = !0, S("Expected server HTML to contain a matching <%s> in <%s>.", t, e.nodeName.toLowerCase());
      }
    }
    function zy(e, t) {
      {
        if (t === "" || Qa)
          return;
        Qa = !0, S('Expected server HTML to contain a matching text node for "%s" in <%s>.', t, e.nodeName.toLowerCase());
      }
    }
    function IR(e, t, a) {
      switch (t) {
        case "input":
          je(e, a);
          return;
        case "textarea":
          Gf(e, a);
          return;
        case "select":
          Im(e, a);
          return;
      }
    }
    var Jd = function() {
    }, ep = function() {
    };
    {
      var QR = ["address", "applet", "area", "article", "aside", "base", "basefont", "bgsound", "blockquote", "body", "br", "button", "caption", "center", "col", "colgroup", "dd", "details", "dir", "div", "dl", "dt", "embed", "fieldset", "figcaption", "figure", "footer", "form", "frame", "frameset", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "iframe", "img", "input", "isindex", "li", "link", "listing", "main", "marquee", "menu", "menuitem", "meta", "nav", "noembed", "noframes", "noscript", "object", "ol", "p", "param", "plaintext", "pre", "script", "section", "select", "source", "style", "summary", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "title", "tr", "track", "ul", "wbr", "xmp"], H0 = [
        "applet",
        "caption",
        "html",
        "table",
        "td",
        "th",
        "marquee",
        "object",
        "template",
        // https://html.spec.whatwg.org/multipage/syntax.html#html-integration-point
        // TODO: Distinguish by namespace here -- for <title>, including it here
        // errs on the side of fewer warnings
        "foreignObject",
        "desc",
        "title"
      ], WR = H0.concat(["button"]), GR = ["dd", "dt", "li", "option", "optgroup", "p", "rp", "rt"], V0 = {
        current: null,
        formTag: null,
        aTagInScope: null,
        buttonTagInScope: null,
        nobrTagInScope: null,
        pTagInButtonScope: null,
        listItemTagAutoclosing: null,
        dlItemTagAutoclosing: null
      };
      ep = function(e, t) {
        var a = lt({}, e || V0), i = {
          tag: t
        };
        return H0.indexOf(t) !== -1 && (a.aTagInScope = null, a.buttonTagInScope = null, a.nobrTagInScope = null), WR.indexOf(t) !== -1 && (a.pTagInButtonScope = null), QR.indexOf(t) !== -1 && t !== "address" && t !== "div" && t !== "p" && (a.listItemTagAutoclosing = null, a.dlItemTagAutoclosing = null), a.current = i, t === "form" && (a.formTag = i), t === "a" && (a.aTagInScope = i), t === "button" && (a.buttonTagInScope = i), t === "nobr" && (a.nobrTagInScope = i), t === "p" && (a.pTagInButtonScope = i), t === "li" && (a.listItemTagAutoclosing = i), (t === "dd" || t === "dt") && (a.dlItemTagAutoclosing = i), a;
      };
      var qR = function(e, t) {
        switch (t) {
          case "select":
            return e === "option" || e === "optgroup" || e === "#text";
          case "optgroup":
            return e === "option" || e === "#text";
          case "option":
            return e === "#text";
          case "tr":
            return e === "th" || e === "td" || e === "style" || e === "script" || e === "template";
          case "tbody":
          case "thead":
          case "tfoot":
            return e === "tr" || e === "style" || e === "script" || e === "template";
          case "colgroup":
            return e === "col" || e === "template";
          case "table":
            return e === "caption" || e === "colgroup" || e === "tbody" || e === "tfoot" || e === "thead" || e === "style" || e === "script" || e === "template";
          case "head":
            return e === "base" || e === "basefont" || e === "bgsound" || e === "link" || e === "meta" || e === "title" || e === "noscript" || e === "noframes" || e === "style" || e === "script" || e === "template";
          case "html":
            return e === "head" || e === "body" || e === "frameset";
          case "frameset":
            return e === "frame";
          case "#document":
            return e === "html";
        }
        switch (e) {
          case "h1":
          case "h2":
          case "h3":
          case "h4":
          case "h5":
          case "h6":
            return t !== "h1" && t !== "h2" && t !== "h3" && t !== "h4" && t !== "h5" && t !== "h6";
          case "rp":
          case "rt":
            return GR.indexOf(t) === -1;
          case "body":
          case "caption":
          case "col":
          case "colgroup":
          case "frameset":
          case "frame":
          case "head":
          case "html":
          case "tbody":
          case "td":
          case "tfoot":
          case "th":
          case "thead":
          case "tr":
            return t == null;
        }
        return !0;
      }, XR = function(e, t) {
        switch (e) {
          case "address":
          case "article":
          case "aside":
          case "blockquote":
          case "center":
          case "details":
          case "dialog":
          case "dir":
          case "div":
          case "dl":
          case "fieldset":
          case "figcaption":
          case "figure":
          case "footer":
          case "header":
          case "hgroup":
          case "main":
          case "menu":
          case "nav":
          case "ol":
          case "p":
          case "section":
          case "summary":
          case "ul":
          case "pre":
          case "listing":
          case "table":
          case "hr":
          case "xmp":
          case "h1":
          case "h2":
          case "h3":
          case "h4":
          case "h5":
          case "h6":
            return t.pTagInButtonScope;
          case "form":
            return t.formTag || t.pTagInButtonScope;
          case "li":
            return t.listItemTagAutoclosing;
          case "dd":
          case "dt":
            return t.dlItemTagAutoclosing;
          case "button":
            return t.buttonTagInScope;
          case "a":
            return t.aTagInScope;
          case "nobr":
            return t.nobrTagInScope;
        }
        return null;
      }, P0 = {};
      Jd = function(e, t, a) {
        a = a || V0;
        var i = a.current, u = i && i.tag;
        t != null && (e != null && S("validateDOMNesting: when childText is passed, childTag should be null"), e = "#text");
        var s = qR(e, u) ? null : i, f = s ? null : XR(e, a), p = s || f;
        if (p) {
          var v = p.tag, y = !!s + "|" + e + "|" + v;
          if (!P0[y]) {
            P0[y] = !0;
            var g = e, b = "";
            if (e === "#text" ? /\S/.test(t) ? g = "Text nodes" : (g = "Whitespace text nodes", b = " Make sure you don't have any extra whitespace between tags on each line of your source code.") : g = "<" + e + ">", s) {
              var x = "";
              v === "table" && e === "tr" && (x += " Add a <tbody>, <thead> or <tfoot> to your code to match the DOM tree generated by the browser."), S("validateDOMNesting(...): %s cannot appear as a child of <%s>.%s%s", g, v, b, x);
            } else
              S("validateDOMNesting(...): %s cannot appear as a descendant of <%s>.", g, v);
          }
        }
      };
    }
    var Rh = "suppressHydrationWarning", Th = "$", xh = "/$", tp = "$?", np = "$!", KR = "style", Uy = null, Ay = null;
    function ZR(e) {
      var t, a, i = e.nodeType;
      switch (i) {
        case ai:
        case Kl: {
          t = i === ai ? "#document" : "#fragment";
          var u = e.documentElement;
          a = u ? u.namespaceURI : Xf(null, "");
          break;
        }
        default: {
          var s = i === An ? e.parentNode : e, f = s.namespaceURI || null;
          t = s.tagName, a = Xf(f, t);
          break;
        }
      }
      {
        var p = t.toLowerCase(), v = ep(null, p);
        return {
          namespace: a,
          ancestorInfo: v
        };
      }
    }
    function JR(e, t, a) {
      {
        var i = e, u = Xf(i.namespace, t), s = ep(i.ancestorInfo, t);
        return {
          namespace: u,
          ancestorInfo: s
        };
      }
    }
    function yk(e) {
      return e;
    }
    function eT(e) {
      Uy = Ro(), Ay = vR();
      var t = null;
      return la(!1), t;
    }
    function tT(e) {
      hR(Ay), la(Uy), Uy = null, Ay = null;
    }
    function nT(e, t, a, i, u) {
      var s;
      {
        var f = i;
        if (Jd(e, null, f.ancestorInfo), typeof t.children == "string" || typeof t.children == "number") {
          var p = "" + t.children, v = ep(f.ancestorInfo, e);
          Jd(null, p, v);
        }
        s = f.namespace;
      }
      var y = jR(e, t, a, s);
      return ip(u, y), Yy(y, t), y;
    }
    function rT(e, t) {
      e.appendChild(t);
    }
    function aT(e, t, a, i, u) {
      switch (HR(e, t, a, i), t) {
        case "button":
        case "input":
        case "select":
        case "textarea":
          return !!a.autoFocus;
        case "img":
          return !0;
        default:
          return !1;
      }
    }
    function iT(e, t, a, i, u, s) {
      {
        var f = s;
        if (typeof i.children != typeof a.children && (typeof i.children == "string" || typeof i.children == "number")) {
          var p = "" + i.children, v = ep(f.ancestorInfo, t);
          Jd(null, p, v);
        }
      }
      return VR(e, t, a, i);
    }
    function jy(e, t) {
      return e === "textarea" || e === "noscript" || typeof t.children == "string" || typeof t.children == "number" || typeof t.dangerouslySetInnerHTML == "object" && t.dangerouslySetInnerHTML !== null && t.dangerouslySetInnerHTML.__html != null;
    }
    function lT(e, t, a, i) {
      {
        var u = a;
        Jd(null, e, u.ancestorInfo);
      }
      var s = FR(e, t);
      return ip(i, s), s;
    }
    function uT() {
      var e = window.event;
      return e === void 0 ? Ci : Kc(e.type);
    }
    var Fy = typeof setTimeout == "function" ? setTimeout : void 0, oT = typeof clearTimeout == "function" ? clearTimeout : void 0, Hy = -1, B0 = typeof Promise == "function" ? Promise : void 0, sT = typeof queueMicrotask == "function" ? queueMicrotask : typeof B0 < "u" ? function(e) {
      return B0.resolve(null).then(e).catch(cT);
    } : Fy;
    function cT(e) {
      setTimeout(function() {
        throw e;
      });
    }
    function fT(e, t, a, i) {
      switch (t) {
        case "button":
        case "input":
        case "select":
        case "textarea":
          a.autoFocus && e.focus();
          return;
        case "img": {
          a.src && (e.src = a.src);
          return;
        }
      }
    }
    function dT(e, t, a, i, u, s) {
      PR(e, t, a, i, u), Yy(e, u);
    }
    function $0(e) {
      ac(e, "");
    }
    function pT(e, t, a) {
      e.nodeValue = a;
    }
    function vT(e, t) {
      e.appendChild(t);
    }
    function hT(e, t) {
      var a;
      e.nodeType === An ? (a = e.parentNode, a.insertBefore(t, e)) : (a = e, a.appendChild(t));
      var i = e._reactRootContainer;
      i == null && a.onclick === null && Ch(a);
    }
    function mT(e, t, a) {
      e.insertBefore(t, a);
    }
    function yT(e, t, a) {
      e.nodeType === An ? e.parentNode.insertBefore(t, a) : e.insertBefore(t, a);
    }
    function gT(e, t) {
      e.removeChild(t);
    }
    function ST(e, t) {
      e.nodeType === An ? e.parentNode.removeChild(t) : e.removeChild(t);
    }
    function Vy(e, t) {
      var a = t, i = 0;
      do {
        var u = a.nextSibling;
        if (e.removeChild(a), u && u.nodeType === An) {
          var s = u.data;
          if (s === xh)
            if (i === 0) {
              e.removeChild(u), wn(t);
              return;
            } else
              i--;
          else
            (s === Th || s === tp || s === np) && i++;
        }
        a = u;
      } while (a);
      wn(t);
    }
    function ET(e, t) {
      e.nodeType === An ? Vy(e.parentNode, t) : e.nodeType === Xr && Vy(e, t), wn(e);
    }
    function CT(e) {
      e = e;
      var t = e.style;
      typeof t.setProperty == "function" ? t.setProperty("display", "none", "important") : t.display = "none";
    }
    function RT(e) {
      e.nodeValue = "";
    }
    function TT(e, t) {
      e = e;
      var a = t[KR], i = a != null && a.hasOwnProperty("display") ? a.display : null;
      e.style.display = ic("display", i);
    }
    function xT(e, t) {
      e.nodeValue = t;
    }
    function wT(e) {
      e.nodeType === Xr ? e.textContent = "" : e.nodeType === ai && e.documentElement && e.removeChild(e.documentElement);
    }
    function bT(e, t, a) {
      return e.nodeType !== Xr || t.toLowerCase() !== e.nodeName.toLowerCase() ? null : e;
    }
    function _T(e, t) {
      return t === "" || e.nodeType !== Fi ? null : e;
    }
    function kT(e) {
      return e.nodeType !== An ? null : e;
    }
    function Y0(e) {
      return e.data === tp;
    }
    function Py(e) {
      return e.data === np;
    }
    function DT(e) {
      var t = e.nextSibling && e.nextSibling.dataset, a, i, u;
      return t && (a = t.dgst, i = t.msg, u = t.stck), {
        message: i,
        digest: a,
        stack: u
      };
    }
    function OT(e, t) {
      e._reactRetry = t;
    }
    function wh(e) {
      for (; e != null; e = e.nextSibling) {
        var t = e.nodeType;
        if (t === Xr || t === Fi)
          break;
        if (t === An) {
          var a = e.data;
          if (a === Th || a === np || a === tp)
            break;
          if (a === xh)
            return null;
        }
      }
      return e;
    }
    function rp(e) {
      return wh(e.nextSibling);
    }
    function LT(e) {
      return wh(e.firstChild);
    }
    function MT(e) {
      return wh(e.firstChild);
    }
    function NT(e) {
      return wh(e.nextSibling);
    }
    function zT(e, t, a, i, u, s, f) {
      ip(s, e), Yy(e, a);
      var p;
      {
        var v = u;
        p = v.namespace;
      }
      var y = (s.mode & xe) !== Ce;
      return $R(e, t, a, p, i, y, f);
    }
    function UT(e, t, a, i) {
      return ip(a, e), a.mode & xe, YR(e, t);
    }
    function AT(e, t) {
      ip(t, e);
    }
    function jT(e) {
      for (var t = e.nextSibling, a = 0; t; ) {
        if (t.nodeType === An) {
          var i = t.data;
          if (i === xh) {
            if (a === 0)
              return rp(t);
            a--;
          } else
            (i === Th || i === np || i === tp) && a++;
        }
        t = t.nextSibling;
      }
      return null;
    }
    function I0(e) {
      for (var t = e.previousSibling, a = 0; t; ) {
        if (t.nodeType === An) {
          var i = t.data;
          if (i === Th || i === np || i === tp) {
            if (a === 0)
              return t;
            a--;
          } else
            i === xh && a++;
        }
        t = t.previousSibling;
      }
      return null;
    }
    function FT(e) {
      wn(e);
    }
    function HT(e) {
      wn(e);
    }
    function VT(e) {
      return e !== "head" && e !== "body";
    }
    function PT(e, t, a, i) {
      var u = !0;
      Eh(t.nodeValue, a, i, u);
    }
    function BT(e, t, a, i, u, s) {
      if (t[Rh] !== !0) {
        var f = !0;
        Eh(i.nodeValue, u, s, f);
      }
    }
    function $T(e, t) {
      t.nodeType === Xr ? Ly(e, t) : t.nodeType === An || My(e, t);
    }
    function YT(e, t) {
      {
        var a = e.parentNode;
        a !== null && (t.nodeType === Xr ? Ly(a, t) : t.nodeType === An || My(a, t));
      }
    }
    function IT(e, t, a, i, u) {
      (u || t[Rh] !== !0) && (i.nodeType === Xr ? Ly(a, i) : i.nodeType === An || My(a, i));
    }
    function QT(e, t, a) {
      Ny(e, t);
    }
    function WT(e, t) {
      zy(e, t);
    }
    function GT(e, t, a) {
      {
        var i = e.parentNode;
        i !== null && Ny(i, t);
      }
    }
    function qT(e, t) {
      {
        var a = e.parentNode;
        a !== null && zy(a, t);
      }
    }
    function XT(e, t, a, i, u, s) {
      (s || t[Rh] !== !0) && Ny(a, i);
    }
    function KT(e, t, a, i, u) {
      (u || t[Rh] !== !0) && zy(a, i);
    }
    function ZT(e) {
      S("An error occurred during hydration. The server HTML was replaced with client content in <%s>.", e.nodeName.toLowerCase());
    }
    function JT(e) {
      qd(e);
    }
    var mf = Math.random().toString(36).slice(2), yf = "__reactFiber$" + mf, By = "__reactProps$" + mf, ap = "__reactContainer$" + mf, $y = "__reactEvents$" + mf, ex = "__reactListeners$" + mf, tx = "__reactHandles$" + mf;
    function nx(e) {
      delete e[yf], delete e[By], delete e[$y], delete e[ex], delete e[tx];
    }
    function ip(e, t) {
      t[yf] = e;
    }
    function bh(e, t) {
      t[ap] = e;
    }
    function Q0(e) {
      e[ap] = null;
    }
    function lp(e) {
      return !!e[ap];
    }
    function As(e) {
      var t = e[yf];
      if (t)
        return t;
      for (var a = e.parentNode; a; ) {
        if (t = a[ap] || a[yf], t) {
          var i = t.alternate;
          if (t.child !== null || i !== null && i.child !== null)
            for (var u = I0(e); u !== null; ) {
              var s = u[yf];
              if (s)
                return s;
              u = I0(u);
            }
          return t;
        }
        e = a, a = e.parentNode;
      }
      return null;
    }
    function Oo(e) {
      var t = e[yf] || e[ap];
      return t && (t.tag === ue || t.tag === Ye || t.tag === Oe || t.tag === re) ? t : null;
    }
    function gf(e) {
      if (e.tag === ue || e.tag === Ye)
        return e.stateNode;
      throw new Error("getNodeFromInstance: Invalid argument.");
    }
    function _h(e) {
      return e[By] || null;
    }
    function Yy(e, t) {
      e[By] = t;
    }
    function rx(e) {
      var t = e[$y];
      return t === void 0 && (t = e[$y] = /* @__PURE__ */ new Set()), t;
    }
    var W0 = {}, G0 = k.ReactDebugCurrentFrame;
    function kh(e) {
      if (e) {
        var t = e._owner, a = mi(e.type, e._source, t ? t.type : null);
        G0.setExtraStackFrame(a);
      } else
        G0.setExtraStackFrame(null);
    }
    function Ki(e, t, a, i, u) {
      {
        var s = Function.call.bind(Wn);
        for (var f in e)
          if (s(e, f)) {
            var p = void 0;
            try {
              if (typeof e[f] != "function") {
                var v = Error((i || "React class") + ": " + a + " type `" + f + "` is invalid; it must be a function, usually from the `prop-types` package, but received `" + typeof e[f] + "`.This often happens because of typos such as `PropTypes.function` instead of `PropTypes.func`.");
                throw v.name = "Invariant Violation", v;
              }
              p = e[f](t, f, i, a, null, "SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED");
            } catch (y) {
              p = y;
            }
            p && !(p instanceof Error) && (kh(u), S("%s: type specification of %s `%s` is invalid; the type checker function must return `null` or an `Error` but returned a %s. You may have forgotten to pass an argument to the type checker creator (arrayOf, instanceOf, objectOf, oneOf, oneOfType, and shape all require an argument).", i || "React class", a, f, typeof p), kh(null)), p instanceof Error && !(p.message in W0) && (W0[p.message] = !0, kh(u), S("Failed %s type: %s", a, p.message), kh(null));
          }
      }
    }
    var Iy = [], Dh;
    Dh = [];
    var Cu = -1;
    function Lo(e) {
      return {
        current: e
      };
    }
    function ua(e, t) {
      if (Cu < 0) {
        S("Unexpected pop.");
        return;
      }
      t !== Dh[Cu] && S("Unexpected Fiber popped."), e.current = Iy[Cu], Iy[Cu] = null, Dh[Cu] = null, Cu--;
    }
    function oa(e, t, a) {
      Cu++, Iy[Cu] = e.current, Dh[Cu] = a, e.current = t;
    }
    var Qy;
    Qy = {};
    var oi = {};
    Object.freeze(oi);
    var Ru = Lo(oi), Al = Lo(!1), Wy = oi;
    function Sf(e, t, a) {
      return a && jl(t) ? Wy : Ru.current;
    }
    function q0(e, t, a) {
      {
        var i = e.stateNode;
        i.__reactInternalMemoizedUnmaskedChildContext = t, i.__reactInternalMemoizedMaskedChildContext = a;
      }
    }
    function Ef(e, t) {
      {
        var a = e.type, i = a.contextTypes;
        if (!i)
          return oi;
        var u = e.stateNode;
        if (u && u.__reactInternalMemoizedUnmaskedChildContext === t)
          return u.__reactInternalMemoizedMaskedChildContext;
        var s = {};
        for (var f in i)
          s[f] = t[f];
        {
          var p = We(e) || "Unknown";
          Ki(i, s, "context", p);
        }
        return u && q0(e, t, s), s;
      }
    }
    function Oh() {
      return Al.current;
    }
    function jl(e) {
      {
        var t = e.childContextTypes;
        return t != null;
      }
    }
    function Lh(e) {
      ua(Al, e), ua(Ru, e);
    }
    function Gy(e) {
      ua(Al, e), ua(Ru, e);
    }
    function X0(e, t, a) {
      {
        if (Ru.current !== oi)
          throw new Error("Unexpected context found on stack. This error is likely caused by a bug in React. Please file an issue.");
        oa(Ru, t, e), oa(Al, a, e);
      }
    }
    function K0(e, t, a) {
      {
        var i = e.stateNode, u = t.childContextTypes;
        if (typeof i.getChildContext != "function") {
          {
            var s = We(e) || "Unknown";
            Qy[s] || (Qy[s] = !0, S("%s.childContextTypes is specified but there is no getChildContext() method on the instance. You can either define getChildContext() on %s or remove childContextTypes from it.", s, s));
          }
          return a;
        }
        var f = i.getChildContext();
        for (var p in f)
          if (!(p in u))
            throw new Error((We(e) || "Unknown") + '.getChildContext(): key "' + p + '" is not defined in childContextTypes.');
        {
          var v = We(e) || "Unknown";
          Ki(u, f, "child context", v);
        }
        return lt({}, a, f);
      }
    }
    function Mh(e) {
      {
        var t = e.stateNode, a = t && t.__reactInternalMemoizedMergedChildContext || oi;
        return Wy = Ru.current, oa(Ru, a, e), oa(Al, Al.current, e), !0;
      }
    }
    function Z0(e, t, a) {
      {
        var i = e.stateNode;
        if (!i)
          throw new Error("Expected to have an instance by this point. This error is likely caused by a bug in React. Please file an issue.");
        if (a) {
          var u = K0(e, t, Wy);
          i.__reactInternalMemoizedMergedChildContext = u, ua(Al, e), ua(Ru, e), oa(Ru, u, e), oa(Al, a, e);
        } else
          ua(Al, e), oa(Al, a, e);
      }
    }
    function ax(e) {
      {
        if (!md(e) || e.tag !== se)
          throw new Error("Expected subtree parent to be a mounted class component. This error is likely caused by a bug in React. Please file an issue.");
        var t = e;
        do {
          switch (t.tag) {
            case re:
              return t.stateNode.context;
            case se: {
              var a = t.type;
              if (jl(a))
                return t.stateNode.__reactInternalMemoizedMergedChildContext;
              break;
            }
          }
          t = t.return;
        } while (t !== null);
        throw new Error("Found unexpected detached subtree parent. This error is likely caused by a bug in React. Please file an issue.");
      }
    }
    var Mo = 0, Nh = 1, Tu = null, qy = !1, Xy = !1;
    function J0(e) {
      Tu === null ? Tu = [e] : Tu.push(e);
    }
    function ix(e) {
      qy = !0, J0(e);
    }
    function eE() {
      qy && No();
    }
    function No() {
      if (!Xy && Tu !== null) {
        Xy = !0;
        var e = 0, t = Pa();
        try {
          var a = !0, i = Tu;
          for (xn(Ln); e < i.length; e++) {
            var u = i[e];
            do
              u = u(a);
            while (u !== null);
          }
          Tu = null, qy = !1;
        } catch (s) {
          throw Tu !== null && (Tu = Tu.slice(e + 1)), mc(gc, No), s;
        } finally {
          xn(t), Xy = !1;
        }
      }
      return null;
    }
    var Cf = [], Rf = 0, zh = null, Uh = 0, wi = [], bi = 0, js = null, xu = 1, wu = "";
    function lx(e) {
      return Hs(), (e.flags & pd) !== Le;
    }
    function ux(e) {
      return Hs(), Uh;
    }
    function ox() {
      var e = wu, t = xu, a = t & ~sx(t);
      return a.toString(32) + e;
    }
    function Fs(e, t) {
      Hs(), Cf[Rf++] = Uh, Cf[Rf++] = zh, zh = e, Uh = t;
    }
    function tE(e, t, a) {
      Hs(), wi[bi++] = xu, wi[bi++] = wu, wi[bi++] = js, js = e;
      var i = xu, u = wu, s = Ah(i) - 1, f = i & ~(1 << s), p = a + 1, v = Ah(t) + s;
      if (v > 30) {
        var y = s - s % 5, g = (1 << y) - 1, b = (f & g).toString(32), x = f >> y, N = s - y, A = Ah(t) + N, F = p << N, le = F | x, Me = b + u;
        xu = 1 << A | le, wu = Me;
      } else {
        var we = p << s, wt = we | f, gt = u;
        xu = 1 << v | wt, wu = gt;
      }
    }
    function Ky(e) {
      Hs();
      var t = e.return;
      if (t !== null) {
        var a = 1, i = 0;
        Fs(e, a), tE(e, a, i);
      }
    }
    function Ah(e) {
      return 32 - ao(e);
    }
    function sx(e) {
      return 1 << Ah(e) - 1;
    }
    function Zy(e) {
      for (; e === zh; )
        zh = Cf[--Rf], Cf[Rf] = null, Uh = Cf[--Rf], Cf[Rf] = null;
      for (; e === js; )
        js = wi[--bi], wi[bi] = null, wu = wi[--bi], wi[bi] = null, xu = wi[--bi], wi[bi] = null;
    }
    function cx() {
      return Hs(), js !== null ? {
        id: xu,
        overflow: wu
      } : null;
    }
    function fx(e, t) {
      Hs(), wi[bi++] = xu, wi[bi++] = wu, wi[bi++] = js, xu = t.id, wu = t.overflow, js = e;
    }
    function Hs() {
      zr() || S("Expected to be hydrating. This is a bug in React. Please file an issue.");
    }
    var Nr = null, _i = null, Zi = !1, Vs = !1, zo = null;
    function dx() {
      Zi && S("We should not be hydrating here. This is a bug in React. Please file a bug.");
    }
    function nE() {
      Vs = !0;
    }
    function px() {
      return Vs;
    }
    function vx(e) {
      var t = e.stateNode.containerInfo;
      return _i = MT(t), Nr = e, Zi = !0, zo = null, Vs = !1, !0;
    }
    function hx(e, t, a) {
      return _i = NT(t), Nr = e, Zi = !0, zo = null, Vs = !1, a !== null && fx(e, a), !0;
    }
    function rE(e, t) {
      switch (e.tag) {
        case re: {
          $T(e.stateNode.containerInfo, t);
          break;
        }
        case ue: {
          var a = (e.mode & xe) !== Ce;
          IT(
            e.type,
            e.memoizedProps,
            e.stateNode,
            t,
            // TODO: Delete this argument when we remove the legacy root API.
            a
          );
          break;
        }
        case Oe: {
          var i = e.memoizedState;
          i.dehydrated !== null && YT(i.dehydrated, t);
          break;
        }
      }
    }
    function aE(e, t) {
      rE(e, t);
      var a = S_();
      a.stateNode = t, a.return = e;
      var i = e.deletions;
      i === null ? (e.deletions = [a], e.flags |= jt) : i.push(a);
    }
    function Jy(e, t) {
      {
        if (Vs)
          return;
        switch (e.tag) {
          case re: {
            var a = e.stateNode.containerInfo;
            switch (t.tag) {
              case ue:
                var i = t.type;
                t.pendingProps, QT(a, i);
                break;
              case Ye:
                var u = t.pendingProps;
                WT(a, u);
                break;
            }
            break;
          }
          case ue: {
            var s = e.type, f = e.memoizedProps, p = e.stateNode;
            switch (t.tag) {
              case ue: {
                var v = t.type, y = t.pendingProps, g = (e.mode & xe) !== Ce;
                XT(
                  s,
                  f,
                  p,
                  v,
                  y,
                  // TODO: Delete this argument when we remove the legacy root API.
                  g
                );
                break;
              }
              case Ye: {
                var b = t.pendingProps, x = (e.mode & xe) !== Ce;
                KT(
                  s,
                  f,
                  p,
                  b,
                  // TODO: Delete this argument when we remove the legacy root API.
                  x
                );
                break;
              }
            }
            break;
          }
          case Oe: {
            var N = e.memoizedState, A = N.dehydrated;
            if (A !== null)
              switch (t.tag) {
                case ue:
                  var F = t.type;
                  t.pendingProps, GT(A, F);
                  break;
                case Ye:
                  var le = t.pendingProps;
                  qT(A, le);
                  break;
              }
            break;
          }
          default:
            return;
        }
      }
    }
    function iE(e, t) {
      t.flags = t.flags & ~Ua | ln, Jy(e, t);
    }
    function lE(e, t) {
      switch (e.tag) {
        case ue: {
          var a = e.type;
          e.pendingProps;
          var i = bT(t, a);
          return i !== null ? (e.stateNode = i, Nr = e, _i = LT(i), !0) : !1;
        }
        case Ye: {
          var u = e.pendingProps, s = _T(t, u);
          return s !== null ? (e.stateNode = s, Nr = e, _i = null, !0) : !1;
        }
        case Oe: {
          var f = kT(t);
          if (f !== null) {
            var p = {
              dehydrated: f,
              treeContext: cx(),
              retryLane: Rr
            };
            e.memoizedState = p;
            var v = E_(f);
            return v.return = e, e.child = v, Nr = e, _i = null, !0;
          }
          return !1;
        }
        default:
          return !1;
      }
    }
    function eg(e) {
      return (e.mode & xe) !== Ce && (e.flags & Ie) === Le;
    }
    function tg(e) {
      throw new Error("Hydration failed because the initial UI does not match what was rendered on the server.");
    }
    function ng(e) {
      if (Zi) {
        var t = _i;
        if (!t) {
          eg(e) && (Jy(Nr, e), tg()), iE(Nr, e), Zi = !1, Nr = e;
          return;
        }
        var a = t;
        if (!lE(e, t)) {
          eg(e) && (Jy(Nr, e), tg()), t = rp(a);
          var i = Nr;
          if (!t || !lE(e, t)) {
            iE(Nr, e), Zi = !1, Nr = e;
            return;
          }
          aE(i, a);
        }
      }
    }
    function mx(e, t, a) {
      var i = e.stateNode, u = !Vs, s = zT(i, e.type, e.memoizedProps, t, a, e, u);
      return e.updateQueue = s, s !== null;
    }
    function yx(e) {
      var t = e.stateNode, a = e.memoizedProps, i = UT(t, a, e);
      if (i) {
        var u = Nr;
        if (u !== null)
          switch (u.tag) {
            case re: {
              var s = u.stateNode.containerInfo, f = (u.mode & xe) !== Ce;
              PT(
                s,
                t,
                a,
                // TODO: Delete this argument when we remove the legacy root API.
                f
              );
              break;
            }
            case ue: {
              var p = u.type, v = u.memoizedProps, y = u.stateNode, g = (u.mode & xe) !== Ce;
              BT(
                p,
                v,
                y,
                t,
                a,
                // TODO: Delete this argument when we remove the legacy root API.
                g
              );
              break;
            }
          }
      }
      return i;
    }
    function gx(e) {
      var t = e.memoizedState, a = t !== null ? t.dehydrated : null;
      if (!a)
        throw new Error("Expected to have a hydrated suspense instance. This error is likely caused by a bug in React. Please file an issue.");
      AT(a, e);
    }
    function Sx(e) {
      var t = e.memoizedState, a = t !== null ? t.dehydrated : null;
      if (!a)
        throw new Error("Expected to have a hydrated suspense instance. This error is likely caused by a bug in React. Please file an issue.");
      return jT(a);
    }
    function uE(e) {
      for (var t = e.return; t !== null && t.tag !== ue && t.tag !== re && t.tag !== Oe; )
        t = t.return;
      Nr = t;
    }
    function jh(e) {
      if (e !== Nr)
        return !1;
      if (!Zi)
        return uE(e), Zi = !0, !1;
      if (e.tag !== re && (e.tag !== ue || VT(e.type) && !jy(e.type, e.memoizedProps))) {
        var t = _i;
        if (t)
          if (eg(e))
            oE(e), tg();
          else
            for (; t; )
              aE(e, t), t = rp(t);
      }
      return uE(e), e.tag === Oe ? _i = Sx(e) : _i = Nr ? rp(e.stateNode) : null, !0;
    }
    function Ex() {
      return Zi && _i !== null;
    }
    function oE(e) {
      for (var t = _i; t; )
        rE(e, t), t = rp(t);
    }
    function Tf() {
      Nr = null, _i = null, Zi = !1, Vs = !1;
    }
    function sE() {
      zo !== null && (n1(zo), zo = null);
    }
    function zr() {
      return Zi;
    }
    function rg(e) {
      zo === null ? zo = [e] : zo.push(e);
    }
    var Cx = k.ReactCurrentBatchConfig, Rx = null;
    function Tx() {
      return Cx.transition;
    }
    var Ji = {
      recordUnsafeLifecycleWarnings: function(e, t) {
      },
      flushPendingUnsafeLifecycleWarnings: function() {
      },
      recordLegacyContextWarning: function(e, t) {
      },
      flushLegacyContextWarning: function() {
      },
      discardPendingWarnings: function() {
      }
    };
    {
      var xx = function(e) {
        for (var t = null, a = e; a !== null; )
          a.mode & vt && (t = a), a = a.return;
        return t;
      }, Ps = function(e) {
        var t = [];
        return e.forEach(function(a) {
          t.push(a);
        }), t.sort().join(", ");
      }, up = [], op = [], sp = [], cp = [], fp = [], dp = [], Bs = /* @__PURE__ */ new Set();
      Ji.recordUnsafeLifecycleWarnings = function(e, t) {
        Bs.has(e.type) || (typeof t.componentWillMount == "function" && // Don't warn about react-lifecycles-compat polyfilled components.
        t.componentWillMount.__suppressDeprecationWarning !== !0 && up.push(e), e.mode & vt && typeof t.UNSAFE_componentWillMount == "function" && op.push(e), typeof t.componentWillReceiveProps == "function" && t.componentWillReceiveProps.__suppressDeprecationWarning !== !0 && sp.push(e), e.mode & vt && typeof t.UNSAFE_componentWillReceiveProps == "function" && cp.push(e), typeof t.componentWillUpdate == "function" && t.componentWillUpdate.__suppressDeprecationWarning !== !0 && fp.push(e), e.mode & vt && typeof t.UNSAFE_componentWillUpdate == "function" && dp.push(e));
      }, Ji.flushPendingUnsafeLifecycleWarnings = function() {
        var e = /* @__PURE__ */ new Set();
        up.length > 0 && (up.forEach(function(x) {
          e.add(We(x) || "Component"), Bs.add(x.type);
        }), up = []);
        var t = /* @__PURE__ */ new Set();
        op.length > 0 && (op.forEach(function(x) {
          t.add(We(x) || "Component"), Bs.add(x.type);
        }), op = []);
        var a = /* @__PURE__ */ new Set();
        sp.length > 0 && (sp.forEach(function(x) {
          a.add(We(x) || "Component"), Bs.add(x.type);
        }), sp = []);
        var i = /* @__PURE__ */ new Set();
        cp.length > 0 && (cp.forEach(function(x) {
          i.add(We(x) || "Component"), Bs.add(x.type);
        }), cp = []);
        var u = /* @__PURE__ */ new Set();
        fp.length > 0 && (fp.forEach(function(x) {
          u.add(We(x) || "Component"), Bs.add(x.type);
        }), fp = []);
        var s = /* @__PURE__ */ new Set();
        if (dp.length > 0 && (dp.forEach(function(x) {
          s.add(We(x) || "Component"), Bs.add(x.type);
        }), dp = []), t.size > 0) {
          var f = Ps(t);
          S(`Using UNSAFE_componentWillMount in strict mode is not recommended and may indicate bugs in your code. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move code with side effects to componentDidMount, and set initial state in the constructor.

Please update the following components: %s`, f);
        }
        if (i.size > 0) {
          var p = Ps(i);
          S(`Using UNSAFE_componentWillReceiveProps in strict mode is not recommended and may indicate bugs in your code. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move data fetching code or side effects to componentDidUpdate.
* If you're updating state whenever props change, refactor your code to use memoization techniques or move it to static getDerivedStateFromProps. Learn more at: https://reactjs.org/link/derived-state

Please update the following components: %s`, p);
        }
        if (s.size > 0) {
          var v = Ps(s);
          S(`Using UNSAFE_componentWillUpdate in strict mode is not recommended and may indicate bugs in your code. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move data fetching code or side effects to componentDidUpdate.

Please update the following components: %s`, v);
        }
        if (e.size > 0) {
          var y = Ps(e);
          $e(`componentWillMount has been renamed, and is not recommended for use. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move code with side effects to componentDidMount, and set initial state in the constructor.
* Rename componentWillMount to UNSAFE_componentWillMount to suppress this warning in non-strict mode. In React 18.x, only the UNSAFE_ name will work. To rename all deprecated lifecycles to their new names, you can run \`npx react-codemod rename-unsafe-lifecycles\` in your project source folder.

Please update the following components: %s`, y);
        }
        if (a.size > 0) {
          var g = Ps(a);
          $e(`componentWillReceiveProps has been renamed, and is not recommended for use. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move data fetching code or side effects to componentDidUpdate.
* If you're updating state whenever props change, refactor your code to use memoization techniques or move it to static getDerivedStateFromProps. Learn more at: https://reactjs.org/link/derived-state
* Rename componentWillReceiveProps to UNSAFE_componentWillReceiveProps to suppress this warning in non-strict mode. In React 18.x, only the UNSAFE_ name will work. To rename all deprecated lifecycles to their new names, you can run \`npx react-codemod rename-unsafe-lifecycles\` in your project source folder.

Please update the following components: %s`, g);
        }
        if (u.size > 0) {
          var b = Ps(u);
          $e(`componentWillUpdate has been renamed, and is not recommended for use. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move data fetching code or side effects to componentDidUpdate.
* Rename componentWillUpdate to UNSAFE_componentWillUpdate to suppress this warning in non-strict mode. In React 18.x, only the UNSAFE_ name will work. To rename all deprecated lifecycles to their new names, you can run \`npx react-codemod rename-unsafe-lifecycles\` in your project source folder.

Please update the following components: %s`, b);
        }
      };
      var Fh = /* @__PURE__ */ new Map(), cE = /* @__PURE__ */ new Set();
      Ji.recordLegacyContextWarning = function(e, t) {
        var a = xx(e);
        if (a === null) {
          S("Expected to find a StrictMode component in a strict mode tree. This error is likely caused by a bug in React. Please file an issue.");
          return;
        }
        if (!cE.has(e.type)) {
          var i = Fh.get(a);
          (e.type.contextTypes != null || e.type.childContextTypes != null || t !== null && typeof t.getChildContext == "function") && (i === void 0 && (i = [], Fh.set(a, i)), i.push(e));
        }
      }, Ji.flushLegacyContextWarning = function() {
        Fh.forEach(function(e, t) {
          if (e.length !== 0) {
            var a = e[0], i = /* @__PURE__ */ new Set();
            e.forEach(function(s) {
              i.add(We(s) || "Component"), cE.add(s.type);
            });
            var u = Ps(i);
            try {
              Bt(a), S(`Legacy context API has been detected within a strict-mode tree.

The old API will be supported in all 16.x releases, but applications using it should migrate to the new version.

Please update the following components: %s

Learn more about this warning here: https://reactjs.org/link/legacy-context`, u);
            } finally {
              Rn();
            }
          }
        });
      }, Ji.discardPendingWarnings = function() {
        up = [], op = [], sp = [], cp = [], fp = [], dp = [], Fh = /* @__PURE__ */ new Map();
      };
    }
    var ag, ig, lg, ug, og, fE = function(e, t) {
    };
    ag = !1, ig = !1, lg = {}, ug = {}, og = {}, fE = function(e, t) {
      if (!(e === null || typeof e != "object") && !(!e._store || e._store.validated || e.key != null)) {
        if (typeof e._store != "object")
          throw new Error("React Component in warnForMissingKey should have a _store. This error is likely caused by a bug in React. Please file an issue.");
        e._store.validated = !0;
        var a = We(t) || "Component";
        ug[a] || (ug[a] = !0, S('Each child in a list should have a unique "key" prop. See https://reactjs.org/link/warning-keys for more information.'));
      }
    };
    function wx(e) {
      return e.prototype && e.prototype.isReactComponent;
    }
    function pp(e, t, a) {
      var i = a.ref;
      if (i !== null && typeof i != "function" && typeof i != "object") {
        if ((e.mode & vt || Pe) && // We warn in ReactElement.js if owner and self are equal for string refs
        // because these cannot be automatically converted to an arrow function
        // using a codemod. Therefore, we don't have to warn about string refs again.
        !(a._owner && a._self && a._owner.stateNode !== a._self) && // Will already throw with "Function components cannot have string refs"
        !(a._owner && a._owner.tag !== se) && // Will already warn with "Function components cannot be given refs"
        !(typeof a.type == "function" && !wx(a.type)) && // Will already throw with "Element ref was specified as a string (someStringRef) but no owner was set"
        a._owner) {
          var u = We(e) || "Component";
          lg[u] || (S('Component "%s" contains the string ref "%s". Support for string refs will be removed in a future major release. We recommend using useRef() or createRef() instead. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-string-ref', u, i), lg[u] = !0);
        }
        if (a._owner) {
          var s = a._owner, f;
          if (s) {
            var p = s;
            if (p.tag !== se)
              throw new Error("Function components cannot have string refs. We recommend using useRef() instead. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-string-ref");
            f = p.stateNode;
          }
          if (!f)
            throw new Error("Missing owner for string ref " + i + ". This error is likely caused by a bug in React. Please file an issue.");
          var v = f;
          Gn(i, "ref");
          var y = "" + i;
          if (t !== null && t.ref !== null && typeof t.ref == "function" && t.ref._stringRef === y)
            return t.ref;
          var g = function(b) {
            var x = v.refs;
            b === null ? delete x[y] : x[y] = b;
          };
          return g._stringRef = y, g;
        } else {
          if (typeof i != "string")
            throw new Error("Expected ref to be a function, a string, an object returned by React.createRef(), or null.");
          if (!a._owner)
            throw new Error("Element ref was specified as a string (" + i + `) but no owner was set. This could happen for one of the following reasons:
1. You may be adding a ref to a function component
2. You may be adding a ref to a component that was not created inside a component's render method
3. You have multiple copies of React loaded
See https://reactjs.org/link/refs-must-have-owner for more information.`);
        }
      }
      return i;
    }
    function Hh(e, t) {
      var a = Object.prototype.toString.call(t);
      throw new Error("Objects are not valid as a React child (found: " + (a === "[object Object]" ? "object with keys {" + Object.keys(t).join(", ") + "}" : a) + "). If you meant to render a collection of children, use an array instead.");
    }
    function Vh(e) {
      {
        var t = We(e) || "Component";
        if (og[t])
          return;
        og[t] = !0, S("Functions are not valid as a React child. This may happen if you return a Component instead of <Component /> from render. Or maybe you meant to call this function rather than return it.");
      }
    }
    function dE(e) {
      var t = e._payload, a = e._init;
      return a(t);
    }
    function pE(e) {
      function t(O, H) {
        if (e) {
          var L = O.deletions;
          L === null ? (O.deletions = [H], O.flags |= jt) : L.push(H);
        }
      }
      function a(O, H) {
        if (!e)
          return null;
        for (var L = H; L !== null; )
          t(O, L), L = L.sibling;
        return null;
      }
      function i(O, H) {
        for (var L = /* @__PURE__ */ new Map(), X = H; X !== null; )
          X.key !== null ? L.set(X.key, X) : L.set(X.index, X), X = X.sibling;
        return L;
      }
      function u(O, H) {
        var L = Ks(O, H);
        return L.index = 0, L.sibling = null, L;
      }
      function s(O, H, L) {
        if (O.index = L, !e)
          return O.flags |= pd, H;
        var X = O.alternate;
        if (X !== null) {
          var ve = X.index;
          return ve < H ? (O.flags |= ln, H) : ve;
        } else
          return O.flags |= ln, H;
      }
      function f(O) {
        return e && O.alternate === null && (O.flags |= ln), O;
      }
      function p(O, H, L, X) {
        if (H === null || H.tag !== Ye) {
          var ve = r0(L, O.mode, X);
          return ve.return = O, ve;
        } else {
          var oe = u(H, L);
          return oe.return = O, oe;
        }
      }
      function v(O, H, L, X) {
        var ve = L.type;
        if (ve === ma)
          return g(O, H, L.props.children, X, L.key);
        if (H !== null && (H.elementType === ve || // Keep this check inline so it only runs on the false path:
        g1(H, L) || // Lazy types should reconcile their resolved type.
        // We need to do this after the Hot Reloading check above,
        // because hot reloading has different semantics than prod because
        // it doesn't resuspend. So we can't let the call below suspend.
        typeof ve == "object" && ve !== null && ve.$$typeof === Ae && dE(ve) === H.type)) {
          var oe = u(H, L.props);
          return oe.ref = pp(O, H, L), oe.return = O, oe._debugSource = L._source, oe._debugOwner = L._owner, oe;
        }
        var Be = n0(L, O.mode, X);
        return Be.ref = pp(O, H, L), Be.return = O, Be;
      }
      function y(O, H, L, X) {
        if (H === null || H.tag !== pe || H.stateNode.containerInfo !== L.containerInfo || H.stateNode.implementation !== L.implementation) {
          var ve = a0(L, O.mode, X);
          return ve.return = O, ve;
        } else {
          var oe = u(H, L.children || []);
          return oe.return = O, oe;
        }
      }
      function g(O, H, L, X, ve) {
        if (H === null || H.tag !== bt) {
          var oe = Io(L, O.mode, X, ve);
          return oe.return = O, oe;
        } else {
          var Be = u(H, L);
          return Be.return = O, Be;
        }
      }
      function b(O, H, L) {
        if (typeof H == "string" && H !== "" || typeof H == "number") {
          var X = r0("" + H, O.mode, L);
          return X.return = O, X;
        }
        if (typeof H == "object" && H !== null) {
          switch (H.$$typeof) {
            case ei: {
              var ve = n0(H, O.mode, L);
              return ve.ref = pp(O, null, H), ve.return = O, ve;
            }
            case _r: {
              var oe = a0(H, O.mode, L);
              return oe.return = O, oe;
            }
            case Ae: {
              var Be = H._payload, Xe = H._init;
              return b(O, Xe(Be), L);
            }
          }
          if (Rt(H) || kr(H)) {
            var qt = Io(H, O.mode, L, null);
            return qt.return = O, qt;
          }
          Hh(O, H);
        }
        return typeof H == "function" && Vh(O), null;
      }
      function x(O, H, L, X) {
        var ve = H !== null ? H.key : null;
        if (typeof L == "string" && L !== "" || typeof L == "number")
          return ve !== null ? null : p(O, H, "" + L, X);
        if (typeof L == "object" && L !== null) {
          switch (L.$$typeof) {
            case ei:
              return L.key === ve ? v(O, H, L, X) : null;
            case _r:
              return L.key === ve ? y(O, H, L, X) : null;
            case Ae: {
              var oe = L._payload, Be = L._init;
              return x(O, H, Be(oe), X);
            }
          }
          if (Rt(L) || kr(L))
            return ve !== null ? null : g(O, H, L, X, null);
          Hh(O, L);
        }
        return typeof L == "function" && Vh(O), null;
      }
      function N(O, H, L, X, ve) {
        if (typeof X == "string" && X !== "" || typeof X == "number") {
          var oe = O.get(L) || null;
          return p(H, oe, "" + X, ve);
        }
        if (typeof X == "object" && X !== null) {
          switch (X.$$typeof) {
            case ei: {
              var Be = O.get(X.key === null ? L : X.key) || null;
              return v(H, Be, X, ve);
            }
            case _r: {
              var Xe = O.get(X.key === null ? L : X.key) || null;
              return y(H, Xe, X, ve);
            }
            case Ae:
              var qt = X._payload, zt = X._init;
              return N(O, H, L, zt(qt), ve);
          }
          if (Rt(X) || kr(X)) {
            var Qn = O.get(L) || null;
            return g(H, Qn, X, ve, null);
          }
          Hh(H, X);
        }
        return typeof X == "function" && Vh(H), null;
      }
      function A(O, H, L) {
        {
          if (typeof O != "object" || O === null)
            return H;
          switch (O.$$typeof) {
            case ei:
            case _r:
              fE(O, L);
              var X = O.key;
              if (typeof X != "string")
                break;
              if (H === null) {
                H = /* @__PURE__ */ new Set(), H.add(X);
                break;
              }
              if (!H.has(X)) {
                H.add(X);
                break;
              }
              S("Encountered two children with the same key, `%s`. Keys should be unique so that components maintain their identity across updates. Non-unique keys may cause children to be duplicated and/or omitted — the behavior is unsupported and could change in a future version.", X);
              break;
            case Ae:
              var ve = O._payload, oe = O._init;
              A(oe(ve), H, L);
              break;
          }
        }
        return H;
      }
      function F(O, H, L, X) {
        for (var ve = null, oe = 0; oe < L.length; oe++) {
          var Be = L[oe];
          ve = A(Be, ve, O);
        }
        for (var Xe = null, qt = null, zt = H, Qn = 0, Ut = 0, Hn = null; zt !== null && Ut < L.length; Ut++) {
          zt.index > Ut ? (Hn = zt, zt = null) : Hn = zt.sibling;
          var ca = x(O, zt, L[Ut], X);
          if (ca === null) {
            zt === null && (zt = Hn);
            break;
          }
          e && zt && ca.alternate === null && t(O, zt), Qn = s(ca, Qn, Ut), qt === null ? Xe = ca : qt.sibling = ca, qt = ca, zt = Hn;
        }
        if (Ut === L.length) {
          if (a(O, zt), zr()) {
            var Pr = Ut;
            Fs(O, Pr);
          }
          return Xe;
        }
        if (zt === null) {
          for (; Ut < L.length; Ut++) {
            var ci = b(O, L[Ut], X);
            ci !== null && (Qn = s(ci, Qn, Ut), qt === null ? Xe = ci : qt.sibling = ci, qt = ci);
          }
          if (zr()) {
            var ba = Ut;
            Fs(O, ba);
          }
          return Xe;
        }
        for (var _a = i(O, zt); Ut < L.length; Ut++) {
          var fa = N(_a, O, Ut, L[Ut], X);
          fa !== null && (e && fa.alternate !== null && _a.delete(fa.key === null ? Ut : fa.key), Qn = s(fa, Qn, Ut), qt === null ? Xe = fa : qt.sibling = fa, qt = fa);
        }
        if (e && _a.forEach(function(Bf) {
          return t(O, Bf);
        }), zr()) {
          var Mu = Ut;
          Fs(O, Mu);
        }
        return Xe;
      }
      function le(O, H, L, X) {
        var ve = kr(L);
        if (typeof ve != "function")
          throw new Error("An object is not an iterable. This error is likely caused by a bug in React. Please file an issue.");
        {
          typeof Symbol == "function" && // $FlowFixMe Flow doesn't know about toStringTag
          L[Symbol.toStringTag] === "Generator" && (ig || S("Using Generators as children is unsupported and will likely yield unexpected results because enumerating a generator mutates it. You may convert it to an array with `Array.from()` or the `[...spread]` operator before rendering. Keep in mind you might need to polyfill these features for older browsers."), ig = !0), L.entries === ve && (ag || S("Using Maps as children is not supported. Use an array of keyed ReactElements instead."), ag = !0);
          var oe = ve.call(L);
          if (oe)
            for (var Be = null, Xe = oe.next(); !Xe.done; Xe = oe.next()) {
              var qt = Xe.value;
              Be = A(qt, Be, O);
            }
        }
        var zt = ve.call(L);
        if (zt == null)
          throw new Error("An iterable object provided no iterator.");
        for (var Qn = null, Ut = null, Hn = H, ca = 0, Pr = 0, ci = null, ba = zt.next(); Hn !== null && !ba.done; Pr++, ba = zt.next()) {
          Hn.index > Pr ? (ci = Hn, Hn = null) : ci = Hn.sibling;
          var _a = x(O, Hn, ba.value, X);
          if (_a === null) {
            Hn === null && (Hn = ci);
            break;
          }
          e && Hn && _a.alternate === null && t(O, Hn), ca = s(_a, ca, Pr), Ut === null ? Qn = _a : Ut.sibling = _a, Ut = _a, Hn = ci;
        }
        if (ba.done) {
          if (a(O, Hn), zr()) {
            var fa = Pr;
            Fs(O, fa);
          }
          return Qn;
        }
        if (Hn === null) {
          for (; !ba.done; Pr++, ba = zt.next()) {
            var Mu = b(O, ba.value, X);
            Mu !== null && (ca = s(Mu, ca, Pr), Ut === null ? Qn = Mu : Ut.sibling = Mu, Ut = Mu);
          }
          if (zr()) {
            var Bf = Pr;
            Fs(O, Bf);
          }
          return Qn;
        }
        for (var Ip = i(O, Hn); !ba.done; Pr++, ba = zt.next()) {
          var Il = N(Ip, O, Pr, ba.value, X);
          Il !== null && (e && Il.alternate !== null && Ip.delete(Il.key === null ? Pr : Il.key), ca = s(Il, ca, Pr), Ut === null ? Qn = Il : Ut.sibling = Il, Ut = Il);
        }
        if (e && Ip.forEach(function(K_) {
          return t(O, K_);
        }), zr()) {
          var X_ = Pr;
          Fs(O, X_);
        }
        return Qn;
      }
      function Me(O, H, L, X) {
        if (H !== null && H.tag === Ye) {
          a(O, H.sibling);
          var ve = u(H, L);
          return ve.return = O, ve;
        }
        a(O, H);
        var oe = r0(L, O.mode, X);
        return oe.return = O, oe;
      }
      function we(O, H, L, X) {
        for (var ve = L.key, oe = H; oe !== null; ) {
          if (oe.key === ve) {
            var Be = L.type;
            if (Be === ma) {
              if (oe.tag === bt) {
                a(O, oe.sibling);
                var Xe = u(oe, L.props.children);
                return Xe.return = O, Xe._debugSource = L._source, Xe._debugOwner = L._owner, Xe;
              }
            } else if (oe.elementType === Be || // Keep this check inline so it only runs on the false path:
            g1(oe, L) || // Lazy types should reconcile their resolved type.
            // We need to do this after the Hot Reloading check above,
            // because hot reloading has different semantics than prod because
            // it doesn't resuspend. So we can't let the call below suspend.
            typeof Be == "object" && Be !== null && Be.$$typeof === Ae && dE(Be) === oe.type) {
              a(O, oe.sibling);
              var qt = u(oe, L.props);
              return qt.ref = pp(O, oe, L), qt.return = O, qt._debugSource = L._source, qt._debugOwner = L._owner, qt;
            }
            a(O, oe);
            break;
          } else
            t(O, oe);
          oe = oe.sibling;
        }
        if (L.type === ma) {
          var zt = Io(L.props.children, O.mode, X, L.key);
          return zt.return = O, zt;
        } else {
          var Qn = n0(L, O.mode, X);
          return Qn.ref = pp(O, H, L), Qn.return = O, Qn;
        }
      }
      function wt(O, H, L, X) {
        for (var ve = L.key, oe = H; oe !== null; ) {
          if (oe.key === ve)
            if (oe.tag === pe && oe.stateNode.containerInfo === L.containerInfo && oe.stateNode.implementation === L.implementation) {
              a(O, oe.sibling);
              var Be = u(oe, L.children || []);
              return Be.return = O, Be;
            } else {
              a(O, oe);
              break;
            }
          else
            t(O, oe);
          oe = oe.sibling;
        }
        var Xe = a0(L, O.mode, X);
        return Xe.return = O, Xe;
      }
      function gt(O, H, L, X) {
        var ve = typeof L == "object" && L !== null && L.type === ma && L.key === null;
        if (ve && (L = L.props.children), typeof L == "object" && L !== null) {
          switch (L.$$typeof) {
            case ei:
              return f(we(O, H, L, X));
            case _r:
              return f(wt(O, H, L, X));
            case Ae:
              var oe = L._payload, Be = L._init;
              return gt(O, H, Be(oe), X);
          }
          if (Rt(L))
            return F(O, H, L, X);
          if (kr(L))
            return le(O, H, L, X);
          Hh(O, L);
        }
        return typeof L == "string" && L !== "" || typeof L == "number" ? f(Me(O, H, "" + L, X)) : (typeof L == "function" && Vh(O), a(O, H));
      }
      return gt;
    }
    var xf = pE(!0), vE = pE(!1);
    function bx(e, t) {
      if (e !== null && t.child !== e.child)
        throw new Error("Resuming work not yet implemented.");
      if (t.child !== null) {
        var a = t.child, i = Ks(a, a.pendingProps);
        for (t.child = i, i.return = t; a.sibling !== null; )
          a = a.sibling, i = i.sibling = Ks(a, a.pendingProps), i.return = t;
        i.sibling = null;
      }
    }
    function _x(e, t) {
      for (var a = e.child; a !== null; )
        v_(a, t), a = a.sibling;
    }
    var sg = Lo(null), cg;
    cg = {};
    var Ph = null, wf = null, fg = null, Bh = !1;
    function $h() {
      Ph = null, wf = null, fg = null, Bh = !1;
    }
    function hE() {
      Bh = !0;
    }
    function mE() {
      Bh = !1;
    }
    function yE(e, t, a) {
      oa(sg, t._currentValue, e), t._currentValue = a, t._currentRenderer !== void 0 && t._currentRenderer !== null && t._currentRenderer !== cg && S("Detected multiple renderers concurrently rendering the same context provider. This is currently unsupported."), t._currentRenderer = cg;
    }
    function dg(e, t) {
      var a = sg.current;
      ua(sg, t), e._currentValue = a;
    }
    function pg(e, t, a) {
      for (var i = e; i !== null; ) {
        var u = i.alternate;
        if (pu(i.childLanes, t) ? u !== null && !pu(u.childLanes, t) && (u.childLanes = Ke(u.childLanes, t)) : (i.childLanes = Ke(i.childLanes, t), u !== null && (u.childLanes = Ke(u.childLanes, t))), i === a)
          break;
        i = i.return;
      }
      i !== a && S("Expected to find the propagation root when scheduling context work. This error is likely caused by a bug in React. Please file an issue.");
    }
    function kx(e, t, a) {
      Dx(e, t, a);
    }
    function Dx(e, t, a) {
      var i = e.child;
      for (i !== null && (i.return = e); i !== null; ) {
        var u = void 0, s = i.dependencies;
        if (s !== null) {
          u = i.child;
          for (var f = s.firstContext; f !== null; ) {
            if (f.context === t) {
              if (i.tag === se) {
                var p = fo(a), v = bu(nn, p);
                v.tag = Ih;
                var y = i.updateQueue;
                if (y !== null) {
                  var g = y.shared, b = g.pending;
                  b === null ? v.next = v : (v.next = b.next, b.next = v), g.pending = v;
                }
              }
              i.lanes = Ke(i.lanes, a);
              var x = i.alternate;
              x !== null && (x.lanes = Ke(x.lanes, a)), pg(i.return, a, e), s.lanes = Ke(s.lanes, a);
              break;
            }
            f = f.next;
          }
        } else if (i.tag === ot)
          u = i.type === e.type ? null : i.child;
        else if (i.tag === Wt) {
          var N = i.return;
          if (N === null)
            throw new Error("We just came from a parent so we must have had a parent. This is a bug in React.");
          N.lanes = Ke(N.lanes, a);
          var A = N.alternate;
          A !== null && (A.lanes = Ke(A.lanes, a)), pg(N, a, e), u = i.sibling;
        } else
          u = i.child;
        if (u !== null)
          u.return = i;
        else
          for (u = i; u !== null; ) {
            if (u === e) {
              u = null;
              break;
            }
            var F = u.sibling;
            if (F !== null) {
              F.return = u.return, u = F;
              break;
            }
            u = u.return;
          }
        i = u;
      }
    }
    function bf(e, t) {
      Ph = e, wf = null, fg = null;
      var a = e.dependencies;
      if (a !== null) {
        var i = a.firstContext;
        i !== null && (ia(a.lanes, t) && kp(), a.firstContext = null);
      }
    }
    function nr(e) {
      Bh && S("Context can only be read while React is rendering. In classes, you can read it in the render method or getDerivedStateFromProps. In function components, you can read it directly in the function body, but not inside Hooks like useReducer() or useMemo().");
      var t = e._currentValue;
      if (fg !== e) {
        var a = {
          context: e,
          memoizedValue: t,
          next: null
        };
        if (wf === null) {
          if (Ph === null)
            throw new Error("Context can only be read while React is rendering. In classes, you can read it in the render method or getDerivedStateFromProps. In function components, you can read it directly in the function body, but not inside Hooks like useReducer() or useMemo().");
          wf = a, Ph.dependencies = {
            lanes: $,
            firstContext: a
          };
        } else
          wf = wf.next = a;
      }
      return t;
    }
    var $s = null;
    function vg(e) {
      $s === null ? $s = [e] : $s.push(e);
    }
    function Ox() {
      if ($s !== null) {
        for (var e = 0; e < $s.length; e++) {
          var t = $s[e], a = t.interleaved;
          if (a !== null) {
            t.interleaved = null;
            var i = a.next, u = t.pending;
            if (u !== null) {
              var s = u.next;
              u.next = i, a.next = s;
            }
            t.pending = a;
          }
        }
        $s = null;
      }
    }
    function gE(e, t, a, i) {
      var u = t.interleaved;
      return u === null ? (a.next = a, vg(t)) : (a.next = u.next, u.next = a), t.interleaved = a, Yh(e, i);
    }
    function Lx(e, t, a, i) {
      var u = t.interleaved;
      u === null ? (a.next = a, vg(t)) : (a.next = u.next, u.next = a), t.interleaved = a;
    }
    function Mx(e, t, a, i) {
      var u = t.interleaved;
      return u === null ? (a.next = a, vg(t)) : (a.next = u.next, u.next = a), t.interleaved = a, Yh(e, i);
    }
    function Wa(e, t) {
      return Yh(e, t);
    }
    var Nx = Yh;
    function Yh(e, t) {
      e.lanes = Ke(e.lanes, t);
      var a = e.alternate;
      a !== null && (a.lanes = Ke(a.lanes, t)), a === null && (e.flags & (ln | Ua)) !== Le && v1(e);
      for (var i = e, u = e.return; u !== null; )
        u.childLanes = Ke(u.childLanes, t), a = u.alternate, a !== null ? a.childLanes = Ke(a.childLanes, t) : (u.flags & (ln | Ua)) !== Le && v1(e), i = u, u = u.return;
      if (i.tag === re) {
        var s = i.stateNode;
        return s;
      } else
        return null;
    }
    var SE = 0, EE = 1, Ih = 2, hg = 3, Qh = !1, mg, Wh;
    mg = !1, Wh = null;
    function yg(e) {
      var t = {
        baseState: e.memoizedState,
        firstBaseUpdate: null,
        lastBaseUpdate: null,
        shared: {
          pending: null,
          interleaved: null,
          lanes: $
        },
        effects: null
      };
      e.updateQueue = t;
    }
    function CE(e, t) {
      var a = t.updateQueue, i = e.updateQueue;
      if (a === i) {
        var u = {
          baseState: i.baseState,
          firstBaseUpdate: i.firstBaseUpdate,
          lastBaseUpdate: i.lastBaseUpdate,
          shared: i.shared,
          effects: i.effects
        };
        t.updateQueue = u;
      }
    }
    function bu(e, t) {
      var a = {
        eventTime: e,
        lane: t,
        tag: SE,
        payload: null,
        callback: null,
        next: null
      };
      return a;
    }
    function Uo(e, t, a) {
      var i = e.updateQueue;
      if (i === null)
        return null;
      var u = i.shared;
      if (Wh === u && !mg && (S("An update (setState, replaceState, or forceUpdate) was scheduled from inside an update function. Update functions should be pure, with zero side-effects. Consider using componentDidUpdate or a callback."), mg = !0), Lb()) {
        var s = u.pending;
        return s === null ? t.next = t : (t.next = s.next, s.next = t), u.pending = t, Nx(e, a);
      } else
        return Mx(e, u, t, a);
    }
    function Gh(e, t, a) {
      var i = t.updateQueue;
      if (i !== null) {
        var u = i.shared;
        if (kd(a)) {
          var s = u.lanes;
          s = Bc(s, e.pendingLanes);
          var f = Ke(s, a);
          u.lanes = f, Dd(e, f);
        }
      }
    }
    function gg(e, t) {
      var a = e.updateQueue, i = e.alternate;
      if (i !== null) {
        var u = i.updateQueue;
        if (a === u) {
          var s = null, f = null, p = a.firstBaseUpdate;
          if (p !== null) {
            var v = p;
            do {
              var y = {
                eventTime: v.eventTime,
                lane: v.lane,
                tag: v.tag,
                payload: v.payload,
                callback: v.callback,
                next: null
              };
              f === null ? s = f = y : (f.next = y, f = y), v = v.next;
            } while (v !== null);
            f === null ? s = f = t : (f.next = t, f = t);
          } else
            s = f = t;
          a = {
            baseState: u.baseState,
            firstBaseUpdate: s,
            lastBaseUpdate: f,
            shared: u.shared,
            effects: u.effects
          }, e.updateQueue = a;
          return;
        }
      }
      var g = a.lastBaseUpdate;
      g === null ? a.firstBaseUpdate = t : g.next = t, a.lastBaseUpdate = t;
    }
    function zx(e, t, a, i, u, s) {
      switch (a.tag) {
        case EE: {
          var f = a.payload;
          if (typeof f == "function") {
            hE();
            var p = f.call(s, i, u);
            {
              if (e.mode & vt) {
                jn(!0);
                try {
                  f.call(s, i, u);
                } finally {
                  jn(!1);
                }
              }
              mE();
            }
            return p;
          }
          return f;
        }
        case hg:
          e.flags = e.flags & ~Zn | Ie;
        case SE: {
          var v = a.payload, y;
          if (typeof v == "function") {
            hE(), y = v.call(s, i, u);
            {
              if (e.mode & vt) {
                jn(!0);
                try {
                  v.call(s, i, u);
                } finally {
                  jn(!1);
                }
              }
              mE();
            }
          } else
            y = v;
          return y == null ? i : lt({}, i, y);
        }
        case Ih:
          return Qh = !0, i;
      }
      return i;
    }
    function qh(e, t, a, i) {
      var u = e.updateQueue;
      Qh = !1, Wh = u.shared;
      var s = u.firstBaseUpdate, f = u.lastBaseUpdate, p = u.shared.pending;
      if (p !== null) {
        u.shared.pending = null;
        var v = p, y = v.next;
        v.next = null, f === null ? s = y : f.next = y, f = v;
        var g = e.alternate;
        if (g !== null) {
          var b = g.updateQueue, x = b.lastBaseUpdate;
          x !== f && (x === null ? b.firstBaseUpdate = y : x.next = y, b.lastBaseUpdate = v);
        }
      }
      if (s !== null) {
        var N = u.baseState, A = $, F = null, le = null, Me = null, we = s;
        do {
          var wt = we.lane, gt = we.eventTime;
          if (pu(i, wt)) {
            if (Me !== null) {
              var H = {
                eventTime: gt,
                // This update is going to be committed so we never want uncommit
                // it. Using NoLane works because 0 is a subset of all bitmasks, so
                // this will never be skipped by the check above.
                lane: Fn,
                tag: we.tag,
                payload: we.payload,
                callback: we.callback,
                next: null
              };
              Me = Me.next = H;
            }
            N = zx(e, u, we, N, t, a);
            var L = we.callback;
            if (L !== null && // If the update was already committed, we should not queue its
            // callback again.
            we.lane !== Fn) {
              e.flags |= Si;
              var X = u.effects;
              X === null ? u.effects = [we] : X.push(we);
            }
          } else {
            var O = {
              eventTime: gt,
              lane: wt,
              tag: we.tag,
              payload: we.payload,
              callback: we.callback,
              next: null
            };
            Me === null ? (le = Me = O, F = N) : Me = Me.next = O, A = Ke(A, wt);
          }
          if (we = we.next, we === null) {
            if (p = u.shared.pending, p === null)
              break;
            var ve = p, oe = ve.next;
            ve.next = null, we = oe, u.lastBaseUpdate = ve, u.shared.pending = null;
          }
        } while (!0);
        Me === null && (F = N), u.baseState = F, u.firstBaseUpdate = le, u.lastBaseUpdate = Me;
        var Be = u.shared.interleaved;
        if (Be !== null) {
          var Xe = Be;
          do
            A = Ke(A, Xe.lane), Xe = Xe.next;
          while (Xe !== Be);
        } else
          s === null && (u.shared.lanes = $);
        Vp(A), e.lanes = A, e.memoizedState = N;
      }
      Wh = null;
    }
    function Ux(e, t) {
      if (typeof e != "function")
        throw new Error("Invalid argument passed as callback. Expected a function. Instead " + ("received: " + e));
      e.call(t);
    }
    function RE() {
      Qh = !1;
    }
    function Xh() {
      return Qh;
    }
    function TE(e, t, a) {
      var i = t.effects;
      if (t.effects = null, i !== null)
        for (var u = 0; u < i.length; u++) {
          var s = i[u], f = s.callback;
          f !== null && (s.callback = null, Ux(f, a));
        }
    }
    var vp = {}, Ao = Lo(vp), hp = Lo(vp), Kh = Lo(vp);
    function Zh(e) {
      if (e === vp)
        throw new Error("Expected host context to exist. This error is likely caused by a bug in React. Please file an issue.");
      return e;
    }
    function xE() {
      var e = Zh(Kh.current);
      return e;
    }
    function Sg(e, t) {
      oa(Kh, t, e), oa(hp, e, e), oa(Ao, vp, e);
      var a = ZR(t);
      ua(Ao, e), oa(Ao, a, e);
    }
    function _f(e) {
      ua(Ao, e), ua(hp, e), ua(Kh, e);
    }
    function Eg() {
      var e = Zh(Ao.current);
      return e;
    }
    function wE(e) {
      Zh(Kh.current);
      var t = Zh(Ao.current), a = JR(t, e.type);
      t !== a && (oa(hp, e, e), oa(Ao, a, e));
    }
    function Cg(e) {
      hp.current === e && (ua(Ao, e), ua(hp, e));
    }
    var Ax = 0, bE = 1, _E = 1, mp = 2, el = Lo(Ax);
    function Rg(e, t) {
      return (e & t) !== 0;
    }
    function kf(e) {
      return e & bE;
    }
    function Tg(e, t) {
      return e & bE | t;
    }
    function jx(e, t) {
      return e | t;
    }
    function jo(e, t) {
      oa(el, t, e);
    }
    function Df(e) {
      ua(el, e);
    }
    function Fx(e, t) {
      var a = e.memoizedState;
      return a !== null ? a.dehydrated !== null : (e.memoizedProps, !0);
    }
    function Jh(e) {
      for (var t = e; t !== null; ) {
        if (t.tag === Oe) {
          var a = t.memoizedState;
          if (a !== null) {
            var i = a.dehydrated;
            if (i === null || Y0(i) || Py(i))
              return t;
          }
        } else if (t.tag === Ot && // revealOrder undefined can't be trusted because it don't
        // keep track of whether it suspended or not.
        t.memoizedProps.revealOrder !== void 0) {
          var u = (t.flags & Ie) !== Le;
          if (u)
            return t;
        } else if (t.child !== null) {
          t.child.return = t, t = t.child;
          continue;
        }
        if (t === e)
          return null;
        for (; t.sibling === null; ) {
          if (t.return === null || t.return === e)
            return null;
          t = t.return;
        }
        t.sibling.return = t.return, t = t.sibling;
      }
      return null;
    }
    var Ga = (
      /*   */
      0
    ), ur = (
      /* */
      1
    ), Fl = (
      /*  */
      2
    ), or = (
      /*    */
      4
    ), Ur = (
      /*   */
      8
    ), xg = [];
    function wg() {
      for (var e = 0; e < xg.length; e++) {
        var t = xg[e];
        t._workInProgressVersionPrimary = null;
      }
      xg.length = 0;
    }
    function Hx(e, t) {
      var a = t._getVersion, i = a(t._source);
      e.mutableSourceEagerHydrationData == null ? e.mutableSourceEagerHydrationData = [t, i] : e.mutableSourceEagerHydrationData.push(t, i);
    }
    var fe = k.ReactCurrentDispatcher, yp = k.ReactCurrentBatchConfig, bg, Of;
    bg = /* @__PURE__ */ new Set();
    var Ys = $, Gt = null, sr = null, cr = null, em = !1, gp = !1, Sp = 0, Vx = 0, Px = 25, P = null, ki = null, Fo = -1, _g = !1;
    function Yt() {
      {
        var e = P;
        ki === null ? ki = [e] : ki.push(e);
      }
    }
    function ne() {
      {
        var e = P;
        ki !== null && (Fo++, ki[Fo] !== e && Bx(e));
      }
    }
    function Lf(e) {
      e != null && !Rt(e) && S("%s received a final argument that is not an array (instead, received `%s`). When specified, the final argument must be an array.", P, typeof e);
    }
    function Bx(e) {
      {
        var t = We(Gt);
        if (!bg.has(t) && (bg.add(t), ki !== null)) {
          for (var a = "", i = 30, u = 0; u <= Fo; u++) {
            for (var s = ki[u], f = u === Fo ? e : s, p = u + 1 + ". " + s; p.length < i; )
              p += " ";
            p += f + `
`, a += p;
          }
          S(`React has detected a change in the order of Hooks called by %s. This will lead to bugs and errors if not fixed. For more information, read the Rules of Hooks: https://reactjs.org/link/rules-of-hooks

   Previous render            Next render
   ------------------------------------------------------
%s   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
`, t, a);
        }
      }
    }
    function sa() {
      throw new Error(`Invalid hook call. Hooks can only be called inside of the body of a function component. This could happen for one of the following reasons:
1. You might have mismatching versions of React and the renderer (such as React DOM)
2. You might be breaking the Rules of Hooks
3. You might have more than one copy of React in the same app
See https://reactjs.org/link/invalid-hook-call for tips about how to debug and fix this problem.`);
    }
    function kg(e, t) {
      if (_g)
        return !1;
      if (t === null)
        return S("%s received a final argument during this render, but not during the previous render. Even though the final argument is optional, its type cannot change between renders.", P), !1;
      e.length !== t.length && S(`The final argument passed to %s changed size between renders. The order and size of this array must remain constant.

Previous: %s
Incoming: %s`, P, "[" + t.join(", ") + "]", "[" + e.join(", ") + "]");
      for (var a = 0; a < t.length && a < e.length; a++)
        if (!ge(e[a], t[a]))
          return !1;
      return !0;
    }
    function Mf(e, t, a, i, u, s) {
      Ys = s, Gt = t, ki = e !== null ? e._debugHookTypes : null, Fo = -1, _g = e !== null && e.type !== t.type, t.memoizedState = null, t.updateQueue = null, t.lanes = $, e !== null && e.memoizedState !== null ? fe.current = qE : ki !== null ? fe.current = GE : fe.current = WE;
      var f = a(i, u);
      if (gp) {
        var p = 0;
        do {
          if (gp = !1, Sp = 0, p >= Px)
            throw new Error("Too many re-renders. React limits the number of renders to prevent an infinite loop.");
          p += 1, _g = !1, sr = null, cr = null, t.updateQueue = null, Fo = -1, fe.current = XE, f = a(i, u);
        } while (gp);
      }
      fe.current = pm, t._debugHookTypes = ki;
      var v = sr !== null && sr.next !== null;
      if (Ys = $, Gt = null, sr = null, cr = null, P = null, ki = null, Fo = -1, e !== null && (e.flags & ar) !== (t.flags & ar) && // Disable this warning in legacy mode, because legacy Suspense is weird
      // and creates false positives. To make this work in legacy mode, we'd
      // need to mark fibers that commit in an incomplete state, somehow. For
      // now I'll disable the warning that most of the bugs that would trigger
      // it are either exclusive to concurrent mode or exist in both.
      (e.mode & xe) !== Ce && S("Internal React error: Expected static flag was missing. Please notify the React team."), em = !1, v)
        throw new Error("Rendered fewer hooks than expected. This may be caused by an accidental early return statement.");
      return f;
    }
    function Nf() {
      var e = Sp !== 0;
      return Sp = 0, e;
    }
    function kE(e, t, a) {
      t.updateQueue = e.updateQueue, (t.mode & Ca) !== Ce ? t.flags &= ~(au | Jr | cn | et) : t.flags &= ~(cn | et), e.lanes = Cs(e.lanes, a);
    }
    function DE() {
      if (fe.current = pm, em) {
        for (var e = Gt.memoizedState; e !== null; ) {
          var t = e.queue;
          t !== null && (t.pending = null), e = e.next;
        }
        em = !1;
      }
      Ys = $, Gt = null, sr = null, cr = null, ki = null, Fo = -1, P = null, BE = !1, gp = !1, Sp = 0;
    }
    function Hl() {
      var e = {
        memoizedState: null,
        baseState: null,
        baseQueue: null,
        queue: null,
        next: null
      };
      return cr === null ? Gt.memoizedState = cr = e : cr = cr.next = e, cr;
    }
    function Di() {
      var e;
      if (sr === null) {
        var t = Gt.alternate;
        t !== null ? e = t.memoizedState : e = null;
      } else
        e = sr.next;
      var a;
      if (cr === null ? a = Gt.memoizedState : a = cr.next, a !== null)
        cr = a, a = cr.next, sr = e;
      else {
        if (e === null)
          throw new Error("Rendered more hooks than during the previous render.");
        sr = e;
        var i = {
          memoizedState: sr.memoizedState,
          baseState: sr.baseState,
          baseQueue: sr.baseQueue,
          queue: sr.queue,
          next: null
        };
        cr === null ? Gt.memoizedState = cr = i : cr = cr.next = i;
      }
      return cr;
    }
    function OE() {
      return {
        lastEffect: null,
        stores: null
      };
    }
    function Dg(e, t) {
      return typeof t == "function" ? t(e) : t;
    }
    function Og(e, t, a) {
      var i = Hl(), u;
      a !== void 0 ? u = a(t) : u = t, i.memoizedState = i.baseState = u;
      var s = {
        pending: null,
        interleaved: null,
        lanes: $,
        dispatch: null,
        lastRenderedReducer: e,
        lastRenderedState: u
      };
      i.queue = s;
      var f = s.dispatch = Qx.bind(null, Gt, s);
      return [i.memoizedState, f];
    }
    function Lg(e, t, a) {
      var i = Di(), u = i.queue;
      if (u === null)
        throw new Error("Should have a queue. This is likely a bug in React. Please file an issue.");
      u.lastRenderedReducer = e;
      var s = sr, f = s.baseQueue, p = u.pending;
      if (p !== null) {
        if (f !== null) {
          var v = f.next, y = p.next;
          f.next = y, p.next = v;
        }
        s.baseQueue !== f && S("Internal error: Expected work-in-progress queue to be a clone. This is a bug in React."), s.baseQueue = f = p, u.pending = null;
      }
      if (f !== null) {
        var g = f.next, b = s.baseState, x = null, N = null, A = null, F = g;
        do {
          var le = F.lane;
          if (pu(Ys, le)) {
            if (A !== null) {
              var we = {
                // This update is going to be committed so we never want uncommit
                // it. Using NoLane works because 0 is a subset of all bitmasks, so
                // this will never be skipped by the check above.
                lane: Fn,
                action: F.action,
                hasEagerState: F.hasEagerState,
                eagerState: F.eagerState,
                next: null
              };
              A = A.next = we;
            }
            if (F.hasEagerState)
              b = F.eagerState;
            else {
              var wt = F.action;
              b = e(b, wt);
            }
          } else {
            var Me = {
              lane: le,
              action: F.action,
              hasEagerState: F.hasEagerState,
              eagerState: F.eagerState,
              next: null
            };
            A === null ? (N = A = Me, x = b) : A = A.next = Me, Gt.lanes = Ke(Gt.lanes, le), Vp(le);
          }
          F = F.next;
        } while (F !== null && F !== g);
        A === null ? x = b : A.next = N, ge(b, i.memoizedState) || kp(), i.memoizedState = b, i.baseState = x, i.baseQueue = A, u.lastRenderedState = b;
      }
      var gt = u.interleaved;
      if (gt !== null) {
        var O = gt;
        do {
          var H = O.lane;
          Gt.lanes = Ke(Gt.lanes, H), Vp(H), O = O.next;
        } while (O !== gt);
      } else
        f === null && (u.lanes = $);
      var L = u.dispatch;
      return [i.memoizedState, L];
    }
    function Mg(e, t, a) {
      var i = Di(), u = i.queue;
      if (u === null)
        throw new Error("Should have a queue. This is likely a bug in React. Please file an issue.");
      u.lastRenderedReducer = e;
      var s = u.dispatch, f = u.pending, p = i.memoizedState;
      if (f !== null) {
        u.pending = null;
        var v = f.next, y = v;
        do {
          var g = y.action;
          p = e(p, g), y = y.next;
        } while (y !== v);
        ge(p, i.memoizedState) || kp(), i.memoizedState = p, i.baseQueue === null && (i.baseState = p), u.lastRenderedState = p;
      }
      return [p, s];
    }
    function gk(e, t, a) {
    }
    function Sk(e, t, a) {
    }
    function Ng(e, t, a) {
      var i = Gt, u = Hl(), s, f = zr();
      if (f) {
        if (a === void 0)
          throw new Error("Missing getServerSnapshot, which is required for server-rendered content. Will revert to client rendering.");
        s = a(), Of || s !== a() && (S("The result of getServerSnapshot should be cached to avoid an infinite loop"), Of = !0);
      } else {
        if (s = t(), !Of) {
          var p = t();
          ge(s, p) || (S("The result of getSnapshot should be cached to avoid an infinite loop"), Of = !0);
        }
        var v = Mm();
        if (v === null)
          throw new Error("Expected a work-in-progress root. This is a bug in React. Please file an issue.");
        Es(v, Ys) || LE(i, t, s);
      }
      u.memoizedState = s;
      var y = {
        value: s,
        getSnapshot: t
      };
      return u.queue = y, im(NE.bind(null, i, y, e), [e]), i.flags |= cn, Ep(ur | Ur, ME.bind(null, i, y, s, t), void 0, null), s;
    }
    function tm(e, t, a) {
      var i = Gt, u = Di(), s = t();
      if (!Of) {
        var f = t();
        ge(s, f) || (S("The result of getSnapshot should be cached to avoid an infinite loop"), Of = !0);
      }
      var p = u.memoizedState, v = !ge(p, s);
      v && (u.memoizedState = s, kp());
      var y = u.queue;
      if (Rp(NE.bind(null, i, y, e), [e]), y.getSnapshot !== t || v || // Check if the susbcribe function changed. We can save some memory by
      // checking whether we scheduled a subscription effect above.
      cr !== null && cr.memoizedState.tag & ur) {
        i.flags |= cn, Ep(ur | Ur, ME.bind(null, i, y, s, t), void 0, null);
        var g = Mm();
        if (g === null)
          throw new Error("Expected a work-in-progress root. This is a bug in React. Please file an issue.");
        Es(g, Ys) || LE(i, t, s);
      }
      return s;
    }
    function LE(e, t, a) {
      e.flags |= cs;
      var i = {
        getSnapshot: t,
        value: a
      }, u = Gt.updateQueue;
      if (u === null)
        u = OE(), Gt.updateQueue = u, u.stores = [i];
      else {
        var s = u.stores;
        s === null ? u.stores = [i] : s.push(i);
      }
    }
    function ME(e, t, a, i) {
      t.value = a, t.getSnapshot = i, zE(t) && UE(e);
    }
    function NE(e, t, a) {
      var i = function() {
        zE(t) && UE(e);
      };
      return a(i);
    }
    function zE(e) {
      var t = e.getSnapshot, a = e.value;
      try {
        var i = t();
        return !ge(a, i);
      } catch {
        return !0;
      }
    }
    function UE(e) {
      var t = Wa(e, ke);
      t !== null && vr(t, e, ke, nn);
    }
    function nm(e) {
      var t = Hl();
      typeof e == "function" && (e = e()), t.memoizedState = t.baseState = e;
      var a = {
        pending: null,
        interleaved: null,
        lanes: $,
        dispatch: null,
        lastRenderedReducer: Dg,
        lastRenderedState: e
      };
      t.queue = a;
      var i = a.dispatch = Wx.bind(null, Gt, a);
      return [t.memoizedState, i];
    }
    function zg(e) {
      return Lg(Dg);
    }
    function Ug(e) {
      return Mg(Dg);
    }
    function Ep(e, t, a, i) {
      var u = {
        tag: e,
        create: t,
        destroy: a,
        deps: i,
        // Circular
        next: null
      }, s = Gt.updateQueue;
      if (s === null)
        s = OE(), Gt.updateQueue = s, s.lastEffect = u.next = u;
      else {
        var f = s.lastEffect;
        if (f === null)
          s.lastEffect = u.next = u;
        else {
          var p = f.next;
          f.next = u, u.next = p, s.lastEffect = u;
        }
      }
      return u;
    }
    function Ag(e) {
      var t = Hl();
      {
        var a = {
          current: e
        };
        return t.memoizedState = a, a;
      }
    }
    function rm(e) {
      var t = Di();
      return t.memoizedState;
    }
    function Cp(e, t, a, i) {
      var u = Hl(), s = i === void 0 ? null : i;
      Gt.flags |= e, u.memoizedState = Ep(ur | t, a, void 0, s);
    }
    function am(e, t, a, i) {
      var u = Di(), s = i === void 0 ? null : i, f = void 0;
      if (sr !== null) {
        var p = sr.memoizedState;
        if (f = p.destroy, s !== null) {
          var v = p.deps;
          if (kg(s, v)) {
            u.memoizedState = Ep(t, a, f, s);
            return;
          }
        }
      }
      Gt.flags |= e, u.memoizedState = Ep(ur | t, a, f, s);
    }
    function im(e, t) {
      return (Gt.mode & Ca) !== Ce ? Cp(au | cn | bl, Ur, e, t) : Cp(cn | bl, Ur, e, t);
    }
    function Rp(e, t) {
      return am(cn, Ur, e, t);
    }
    function jg(e, t) {
      return Cp(et, Fl, e, t);
    }
    function lm(e, t) {
      return am(et, Fl, e, t);
    }
    function Fg(e, t) {
      var a = et;
      return a |= Zr, (Gt.mode & Ca) !== Ce && (a |= Jr), Cp(a, or, e, t);
    }
    function um(e, t) {
      return am(et, or, e, t);
    }
    function AE(e, t) {
      if (typeof t == "function") {
        var a = t, i = e();
        return a(i), function() {
          a(null);
        };
      } else if (t != null) {
        var u = t;
        u.hasOwnProperty("current") || S("Expected useImperativeHandle() first argument to either be a ref callback or React.createRef() object. Instead received: %s.", "an object with keys {" + Object.keys(u).join(", ") + "}");
        var s = e();
        return u.current = s, function() {
          u.current = null;
        };
      }
    }
    function Hg(e, t, a) {
      typeof t != "function" && S("Expected useImperativeHandle() second argument to be a function that creates a handle. Instead received: %s.", t !== null ? typeof t : "null");
      var i = a != null ? a.concat([e]) : null, u = et;
      return u |= Zr, (Gt.mode & Ca) !== Ce && (u |= Jr), Cp(u, or, AE.bind(null, t, e), i);
    }
    function om(e, t, a) {
      typeof t != "function" && S("Expected useImperativeHandle() second argument to be a function that creates a handle. Instead received: %s.", t !== null ? typeof t : "null");
      var i = a != null ? a.concat([e]) : null;
      return am(et, or, AE.bind(null, t, e), i);
    }
    function $x(e, t) {
    }
    var sm = $x;
    function Vg(e, t) {
      var a = Hl(), i = t === void 0 ? null : t;
      return a.memoizedState = [e, i], e;
    }
    function cm(e, t) {
      var a = Di(), i = t === void 0 ? null : t, u = a.memoizedState;
      if (u !== null && i !== null) {
        var s = u[1];
        if (kg(i, s))
          return u[0];
      }
      return a.memoizedState = [e, i], e;
    }
    function Pg(e, t) {
      var a = Hl(), i = t === void 0 ? null : t, u = e();
      return a.memoizedState = [u, i], u;
    }
    function fm(e, t) {
      var a = Di(), i = t === void 0 ? null : t, u = a.memoizedState;
      if (u !== null && i !== null) {
        var s = u[1];
        if (kg(i, s))
          return u[0];
      }
      var f = e();
      return a.memoizedState = [f, i], f;
    }
    function Bg(e) {
      var t = Hl();
      return t.memoizedState = e, e;
    }
    function jE(e) {
      var t = Di(), a = sr, i = a.memoizedState;
      return HE(t, i, e);
    }
    function FE(e) {
      var t = Di();
      if (sr === null)
        return t.memoizedState = e, e;
      var a = sr.memoizedState;
      return HE(t, a, e);
    }
    function HE(e, t, a) {
      var i = !Pv(Ys);
      if (i) {
        if (!ge(a, t)) {
          var u = Yv();
          Gt.lanes = Ke(Gt.lanes, u), Vp(u), e.baseState = !0;
        }
        return t;
      } else
        return e.baseState && (e.baseState = !1, kp()), e.memoizedState = a, a;
    }
    function Yx(e, t, a) {
      var i = Pa();
      xn(oy(i, Wi)), e(!0);
      var u = yp.transition;
      yp.transition = {};
      var s = yp.transition;
      yp.transition._updatedFibers = /* @__PURE__ */ new Set();
      try {
        e(!1), t();
      } finally {
        if (xn(i), yp.transition = u, u === null && s._updatedFibers) {
          var f = s._updatedFibers.size;
          f > 10 && $e("Detected a large number of updates inside startTransition. If this is due to a subscription please re-write it to use React provided hooks. Otherwise concurrent mode guarantees are off the table."), s._updatedFibers.clear();
        }
      }
    }
    function $g() {
      var e = nm(!1), t = e[0], a = e[1], i = Yx.bind(null, a), u = Hl();
      return u.memoizedState = i, [t, i];
    }
    function VE() {
      var e = zg(), t = e[0], a = Di(), i = a.memoizedState;
      return [t, i];
    }
    function PE() {
      var e = Ug(), t = e[0], a = Di(), i = a.memoizedState;
      return [t, i];
    }
    var BE = !1;
    function Ix() {
      return BE;
    }
    function Yg() {
      var e = Hl(), t = Mm(), a = t.identifierPrefix, i;
      if (zr()) {
        var u = ox();
        i = ":" + a + "R" + u;
        var s = Sp++;
        s > 0 && (i += "H" + s.toString(32)), i += ":";
      } else {
        var f = Vx++;
        i = ":" + a + "r" + f.toString(32) + ":";
      }
      return e.memoizedState = i, i;
    }
    function dm() {
      var e = Di(), t = e.memoizedState;
      return t;
    }
    function Qx(e, t, a) {
      typeof arguments[3] == "function" && S("State updates from the useState() and useReducer() Hooks don't support the second callback argument. To execute a side effect after rendering, declare it in the component body with useEffect().");
      var i = $o(e), u = {
        lane: i,
        action: a,
        hasEagerState: !1,
        eagerState: null,
        next: null
      };
      if ($E(e))
        YE(t, u);
      else {
        var s = gE(e, t, u, i);
        if (s !== null) {
          var f = wa();
          vr(s, e, i, f), IE(s, t, i);
        }
      }
      QE(e, i);
    }
    function Wx(e, t, a) {
      typeof arguments[3] == "function" && S("State updates from the useState() and useReducer() Hooks don't support the second callback argument. To execute a side effect after rendering, declare it in the component body with useEffect().");
      var i = $o(e), u = {
        lane: i,
        action: a,
        hasEagerState: !1,
        eagerState: null,
        next: null
      };
      if ($E(e))
        YE(t, u);
      else {
        var s = e.alternate;
        if (e.lanes === $ && (s === null || s.lanes === $)) {
          var f = t.lastRenderedReducer;
          if (f !== null) {
            var p;
            p = fe.current, fe.current = tl;
            try {
              var v = t.lastRenderedState, y = f(v, a);
              if (u.hasEagerState = !0, u.eagerState = y, ge(y, v)) {
                Lx(e, t, u, i);
                return;
              }
            } catch {
            } finally {
              fe.current = p;
            }
          }
        }
        var g = gE(e, t, u, i);
        if (g !== null) {
          var b = wa();
          vr(g, e, i, b), IE(g, t, i);
        }
      }
      QE(e, i);
    }
    function $E(e) {
      var t = e.alternate;
      return e === Gt || t !== null && t === Gt;
    }
    function YE(e, t) {
      gp = em = !0;
      var a = e.pending;
      a === null ? t.next = t : (t.next = a.next, a.next = t), e.pending = t;
    }
    function IE(e, t, a) {
      if (kd(a)) {
        var i = t.lanes;
        i = Bc(i, e.pendingLanes);
        var u = Ke(i, a);
        t.lanes = u, Dd(e, u);
      }
    }
    function QE(e, t, a) {
      vs(e, t);
    }
    var pm = {
      readContext: nr,
      useCallback: sa,
      useContext: sa,
      useEffect: sa,
      useImperativeHandle: sa,
      useInsertionEffect: sa,
      useLayoutEffect: sa,
      useMemo: sa,
      useReducer: sa,
      useRef: sa,
      useState: sa,
      useDebugValue: sa,
      useDeferredValue: sa,
      useTransition: sa,
      useMutableSource: sa,
      useSyncExternalStore: sa,
      useId: sa,
      unstable_isNewReconciler: J
    }, WE = null, GE = null, qE = null, XE = null, Vl = null, tl = null, vm = null;
    {
      var Ig = function() {
        S("Context can only be read while React is rendering. In classes, you can read it in the render method or getDerivedStateFromProps. In function components, you can read it directly in the function body, but not inside Hooks like useReducer() or useMemo().");
      }, Ge = function() {
        S("Do not call Hooks inside useEffect(...), useMemo(...), or other built-in Hooks. You can only call Hooks at the top level of your React function. For more information, see https://reactjs.org/link/rules-of-hooks");
      };
      WE = {
        readContext: function(e) {
          return nr(e);
        },
        useCallback: function(e, t) {
          return P = "useCallback", Yt(), Lf(t), Vg(e, t);
        },
        useContext: function(e) {
          return P = "useContext", Yt(), nr(e);
        },
        useEffect: function(e, t) {
          return P = "useEffect", Yt(), Lf(t), im(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return P = "useImperativeHandle", Yt(), Lf(a), Hg(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return P = "useInsertionEffect", Yt(), Lf(t), jg(e, t);
        },
        useLayoutEffect: function(e, t) {
          return P = "useLayoutEffect", Yt(), Lf(t), Fg(e, t);
        },
        useMemo: function(e, t) {
          P = "useMemo", Yt(), Lf(t);
          var a = fe.current;
          fe.current = Vl;
          try {
            return Pg(e, t);
          } finally {
            fe.current = a;
          }
        },
        useReducer: function(e, t, a) {
          P = "useReducer", Yt();
          var i = fe.current;
          fe.current = Vl;
          try {
            return Og(e, t, a);
          } finally {
            fe.current = i;
          }
        },
        useRef: function(e) {
          return P = "useRef", Yt(), Ag(e);
        },
        useState: function(e) {
          P = "useState", Yt();
          var t = fe.current;
          fe.current = Vl;
          try {
            return nm(e);
          } finally {
            fe.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return P = "useDebugValue", Yt(), void 0;
        },
        useDeferredValue: function(e) {
          return P = "useDeferredValue", Yt(), Bg(e);
        },
        useTransition: function() {
          return P = "useTransition", Yt(), $g();
        },
        useMutableSource: function(e, t, a) {
          return P = "useMutableSource", Yt(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return P = "useSyncExternalStore", Yt(), Ng(e, t, a);
        },
        useId: function() {
          return P = "useId", Yt(), Yg();
        },
        unstable_isNewReconciler: J
      }, GE = {
        readContext: function(e) {
          return nr(e);
        },
        useCallback: function(e, t) {
          return P = "useCallback", ne(), Vg(e, t);
        },
        useContext: function(e) {
          return P = "useContext", ne(), nr(e);
        },
        useEffect: function(e, t) {
          return P = "useEffect", ne(), im(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return P = "useImperativeHandle", ne(), Hg(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return P = "useInsertionEffect", ne(), jg(e, t);
        },
        useLayoutEffect: function(e, t) {
          return P = "useLayoutEffect", ne(), Fg(e, t);
        },
        useMemo: function(e, t) {
          P = "useMemo", ne();
          var a = fe.current;
          fe.current = Vl;
          try {
            return Pg(e, t);
          } finally {
            fe.current = a;
          }
        },
        useReducer: function(e, t, a) {
          P = "useReducer", ne();
          var i = fe.current;
          fe.current = Vl;
          try {
            return Og(e, t, a);
          } finally {
            fe.current = i;
          }
        },
        useRef: function(e) {
          return P = "useRef", ne(), Ag(e);
        },
        useState: function(e) {
          P = "useState", ne();
          var t = fe.current;
          fe.current = Vl;
          try {
            return nm(e);
          } finally {
            fe.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return P = "useDebugValue", ne(), void 0;
        },
        useDeferredValue: function(e) {
          return P = "useDeferredValue", ne(), Bg(e);
        },
        useTransition: function() {
          return P = "useTransition", ne(), $g();
        },
        useMutableSource: function(e, t, a) {
          return P = "useMutableSource", ne(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return P = "useSyncExternalStore", ne(), Ng(e, t, a);
        },
        useId: function() {
          return P = "useId", ne(), Yg();
        },
        unstable_isNewReconciler: J
      }, qE = {
        readContext: function(e) {
          return nr(e);
        },
        useCallback: function(e, t) {
          return P = "useCallback", ne(), cm(e, t);
        },
        useContext: function(e) {
          return P = "useContext", ne(), nr(e);
        },
        useEffect: function(e, t) {
          return P = "useEffect", ne(), Rp(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return P = "useImperativeHandle", ne(), om(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return P = "useInsertionEffect", ne(), lm(e, t);
        },
        useLayoutEffect: function(e, t) {
          return P = "useLayoutEffect", ne(), um(e, t);
        },
        useMemo: function(e, t) {
          P = "useMemo", ne();
          var a = fe.current;
          fe.current = tl;
          try {
            return fm(e, t);
          } finally {
            fe.current = a;
          }
        },
        useReducer: function(e, t, a) {
          P = "useReducer", ne();
          var i = fe.current;
          fe.current = tl;
          try {
            return Lg(e, t, a);
          } finally {
            fe.current = i;
          }
        },
        useRef: function(e) {
          return P = "useRef", ne(), rm();
        },
        useState: function(e) {
          P = "useState", ne();
          var t = fe.current;
          fe.current = tl;
          try {
            return zg(e);
          } finally {
            fe.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return P = "useDebugValue", ne(), sm();
        },
        useDeferredValue: function(e) {
          return P = "useDeferredValue", ne(), jE(e);
        },
        useTransition: function() {
          return P = "useTransition", ne(), VE();
        },
        useMutableSource: function(e, t, a) {
          return P = "useMutableSource", ne(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return P = "useSyncExternalStore", ne(), tm(e, t);
        },
        useId: function() {
          return P = "useId", ne(), dm();
        },
        unstable_isNewReconciler: J
      }, XE = {
        readContext: function(e) {
          return nr(e);
        },
        useCallback: function(e, t) {
          return P = "useCallback", ne(), cm(e, t);
        },
        useContext: function(e) {
          return P = "useContext", ne(), nr(e);
        },
        useEffect: function(e, t) {
          return P = "useEffect", ne(), Rp(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return P = "useImperativeHandle", ne(), om(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return P = "useInsertionEffect", ne(), lm(e, t);
        },
        useLayoutEffect: function(e, t) {
          return P = "useLayoutEffect", ne(), um(e, t);
        },
        useMemo: function(e, t) {
          P = "useMemo", ne();
          var a = fe.current;
          fe.current = vm;
          try {
            return fm(e, t);
          } finally {
            fe.current = a;
          }
        },
        useReducer: function(e, t, a) {
          P = "useReducer", ne();
          var i = fe.current;
          fe.current = vm;
          try {
            return Mg(e, t, a);
          } finally {
            fe.current = i;
          }
        },
        useRef: function(e) {
          return P = "useRef", ne(), rm();
        },
        useState: function(e) {
          P = "useState", ne();
          var t = fe.current;
          fe.current = vm;
          try {
            return Ug(e);
          } finally {
            fe.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return P = "useDebugValue", ne(), sm();
        },
        useDeferredValue: function(e) {
          return P = "useDeferredValue", ne(), FE(e);
        },
        useTransition: function() {
          return P = "useTransition", ne(), PE();
        },
        useMutableSource: function(e, t, a) {
          return P = "useMutableSource", ne(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return P = "useSyncExternalStore", ne(), tm(e, t);
        },
        useId: function() {
          return P = "useId", ne(), dm();
        },
        unstable_isNewReconciler: J
      }, Vl = {
        readContext: function(e) {
          return Ig(), nr(e);
        },
        useCallback: function(e, t) {
          return P = "useCallback", Ge(), Yt(), Vg(e, t);
        },
        useContext: function(e) {
          return P = "useContext", Ge(), Yt(), nr(e);
        },
        useEffect: function(e, t) {
          return P = "useEffect", Ge(), Yt(), im(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return P = "useImperativeHandle", Ge(), Yt(), Hg(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return P = "useInsertionEffect", Ge(), Yt(), jg(e, t);
        },
        useLayoutEffect: function(e, t) {
          return P = "useLayoutEffect", Ge(), Yt(), Fg(e, t);
        },
        useMemo: function(e, t) {
          P = "useMemo", Ge(), Yt();
          var a = fe.current;
          fe.current = Vl;
          try {
            return Pg(e, t);
          } finally {
            fe.current = a;
          }
        },
        useReducer: function(e, t, a) {
          P = "useReducer", Ge(), Yt();
          var i = fe.current;
          fe.current = Vl;
          try {
            return Og(e, t, a);
          } finally {
            fe.current = i;
          }
        },
        useRef: function(e) {
          return P = "useRef", Ge(), Yt(), Ag(e);
        },
        useState: function(e) {
          P = "useState", Ge(), Yt();
          var t = fe.current;
          fe.current = Vl;
          try {
            return nm(e);
          } finally {
            fe.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return P = "useDebugValue", Ge(), Yt(), void 0;
        },
        useDeferredValue: function(e) {
          return P = "useDeferredValue", Ge(), Yt(), Bg(e);
        },
        useTransition: function() {
          return P = "useTransition", Ge(), Yt(), $g();
        },
        useMutableSource: function(e, t, a) {
          return P = "useMutableSource", Ge(), Yt(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return P = "useSyncExternalStore", Ge(), Yt(), Ng(e, t, a);
        },
        useId: function() {
          return P = "useId", Ge(), Yt(), Yg();
        },
        unstable_isNewReconciler: J
      }, tl = {
        readContext: function(e) {
          return Ig(), nr(e);
        },
        useCallback: function(e, t) {
          return P = "useCallback", Ge(), ne(), cm(e, t);
        },
        useContext: function(e) {
          return P = "useContext", Ge(), ne(), nr(e);
        },
        useEffect: function(e, t) {
          return P = "useEffect", Ge(), ne(), Rp(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return P = "useImperativeHandle", Ge(), ne(), om(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return P = "useInsertionEffect", Ge(), ne(), lm(e, t);
        },
        useLayoutEffect: function(e, t) {
          return P = "useLayoutEffect", Ge(), ne(), um(e, t);
        },
        useMemo: function(e, t) {
          P = "useMemo", Ge(), ne();
          var a = fe.current;
          fe.current = tl;
          try {
            return fm(e, t);
          } finally {
            fe.current = a;
          }
        },
        useReducer: function(e, t, a) {
          P = "useReducer", Ge(), ne();
          var i = fe.current;
          fe.current = tl;
          try {
            return Lg(e, t, a);
          } finally {
            fe.current = i;
          }
        },
        useRef: function(e) {
          return P = "useRef", Ge(), ne(), rm();
        },
        useState: function(e) {
          P = "useState", Ge(), ne();
          var t = fe.current;
          fe.current = tl;
          try {
            return zg(e);
          } finally {
            fe.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return P = "useDebugValue", Ge(), ne(), sm();
        },
        useDeferredValue: function(e) {
          return P = "useDeferredValue", Ge(), ne(), jE(e);
        },
        useTransition: function() {
          return P = "useTransition", Ge(), ne(), VE();
        },
        useMutableSource: function(e, t, a) {
          return P = "useMutableSource", Ge(), ne(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return P = "useSyncExternalStore", Ge(), ne(), tm(e, t);
        },
        useId: function() {
          return P = "useId", Ge(), ne(), dm();
        },
        unstable_isNewReconciler: J
      }, vm = {
        readContext: function(e) {
          return Ig(), nr(e);
        },
        useCallback: function(e, t) {
          return P = "useCallback", Ge(), ne(), cm(e, t);
        },
        useContext: function(e) {
          return P = "useContext", Ge(), ne(), nr(e);
        },
        useEffect: function(e, t) {
          return P = "useEffect", Ge(), ne(), Rp(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return P = "useImperativeHandle", Ge(), ne(), om(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return P = "useInsertionEffect", Ge(), ne(), lm(e, t);
        },
        useLayoutEffect: function(e, t) {
          return P = "useLayoutEffect", Ge(), ne(), um(e, t);
        },
        useMemo: function(e, t) {
          P = "useMemo", Ge(), ne();
          var a = fe.current;
          fe.current = tl;
          try {
            return fm(e, t);
          } finally {
            fe.current = a;
          }
        },
        useReducer: function(e, t, a) {
          P = "useReducer", Ge(), ne();
          var i = fe.current;
          fe.current = tl;
          try {
            return Mg(e, t, a);
          } finally {
            fe.current = i;
          }
        },
        useRef: function(e) {
          return P = "useRef", Ge(), ne(), rm();
        },
        useState: function(e) {
          P = "useState", Ge(), ne();
          var t = fe.current;
          fe.current = tl;
          try {
            return Ug(e);
          } finally {
            fe.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return P = "useDebugValue", Ge(), ne(), sm();
        },
        useDeferredValue: function(e) {
          return P = "useDeferredValue", Ge(), ne(), FE(e);
        },
        useTransition: function() {
          return P = "useTransition", Ge(), ne(), PE();
        },
        useMutableSource: function(e, t, a) {
          return P = "useMutableSource", Ge(), ne(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return P = "useSyncExternalStore", Ge(), ne(), tm(e, t);
        },
        useId: function() {
          return P = "useId", Ge(), ne(), dm();
        },
        unstable_isNewReconciler: J
      };
    }
    var Ho = B.unstable_now, KE = 0, hm = -1, Tp = -1, mm = -1, Qg = !1, ym = !1;
    function ZE() {
      return Qg;
    }
    function Gx() {
      ym = !0;
    }
    function qx() {
      Qg = !1, ym = !1;
    }
    function Xx() {
      Qg = ym, ym = !1;
    }
    function JE() {
      return KE;
    }
    function eC() {
      KE = Ho();
    }
    function Wg(e) {
      Tp = Ho(), e.actualStartTime < 0 && (e.actualStartTime = Ho());
    }
    function tC(e) {
      Tp = -1;
    }
    function gm(e, t) {
      if (Tp >= 0) {
        var a = Ho() - Tp;
        e.actualDuration += a, t && (e.selfBaseDuration = a), Tp = -1;
      }
    }
    function Pl(e) {
      if (hm >= 0) {
        var t = Ho() - hm;
        hm = -1;
        for (var a = e.return; a !== null; ) {
          switch (a.tag) {
            case re:
              var i = a.stateNode;
              i.effectDuration += t;
              return;
            case mt:
              var u = a.stateNode;
              u.effectDuration += t;
              return;
          }
          a = a.return;
        }
      }
    }
    function Gg(e) {
      if (mm >= 0) {
        var t = Ho() - mm;
        mm = -1;
        for (var a = e.return; a !== null; ) {
          switch (a.tag) {
            case re:
              var i = a.stateNode;
              i !== null && (i.passiveEffectDuration += t);
              return;
            case mt:
              var u = a.stateNode;
              u !== null && (u.passiveEffectDuration += t);
              return;
          }
          a = a.return;
        }
      }
    }
    function Bl() {
      hm = Ho();
    }
    function qg() {
      mm = Ho();
    }
    function Xg(e) {
      for (var t = e.child; t; )
        e.actualDuration += t.actualDuration, t = t.sibling;
    }
    function nl(e, t) {
      if (e && e.defaultProps) {
        var a = lt({}, t), i = e.defaultProps;
        for (var u in i)
          a[u] === void 0 && (a[u] = i[u]);
        return a;
      }
      return t;
    }
    var Kg = {}, Zg, Jg, eS, tS, nS, nC, Sm, rS, aS, iS, xp;
    {
      Zg = /* @__PURE__ */ new Set(), Jg = /* @__PURE__ */ new Set(), eS = /* @__PURE__ */ new Set(), tS = /* @__PURE__ */ new Set(), rS = /* @__PURE__ */ new Set(), nS = /* @__PURE__ */ new Set(), aS = /* @__PURE__ */ new Set(), iS = /* @__PURE__ */ new Set(), xp = /* @__PURE__ */ new Set();
      var rC = /* @__PURE__ */ new Set();
      Sm = function(e, t) {
        if (!(e === null || typeof e == "function")) {
          var a = t + "_" + e;
          rC.has(a) || (rC.add(a), S("%s(...): Expected the last optional `callback` argument to be a function. Instead received: %s.", t, e));
        }
      }, nC = function(e, t) {
        if (t === void 0) {
          var a = Ct(e) || "Component";
          nS.has(a) || (nS.add(a), S("%s.getDerivedStateFromProps(): A valid state object (or null) must be returned. You have returned undefined.", a));
        }
      }, Object.defineProperty(Kg, "_processChildContext", {
        enumerable: !1,
        value: function() {
          throw new Error("_processChildContext is not available in React 16+. This likely means you have multiple copies of React and are attempting to nest a React 15 tree inside a React 16 tree using unstable_renderSubtreeIntoContainer, which isn't supported. Try to make sure you have only one copy of React (and ideally, switch to ReactDOM.createPortal).");
        }
      }), Object.freeze(Kg);
    }
    function lS(e, t, a, i) {
      var u = e.memoizedState, s = a(i, u);
      {
        if (e.mode & vt) {
          jn(!0);
          try {
            s = a(i, u);
          } finally {
            jn(!1);
          }
        }
        nC(t, s);
      }
      var f = s == null ? u : lt({}, u, s);
      if (e.memoizedState = f, e.lanes === $) {
        var p = e.updateQueue;
        p.baseState = f;
      }
    }
    var uS = {
      isMounted: Sa,
      enqueueSetState: function(e, t, a) {
        var i = Na(e), u = wa(), s = $o(i), f = bu(u, s);
        f.payload = t, a != null && (Sm(a, "setState"), f.callback = a);
        var p = Uo(i, f, s);
        p !== null && (vr(p, i, s, u), Gh(p, i, s)), vs(i, s);
      },
      enqueueReplaceState: function(e, t, a) {
        var i = Na(e), u = wa(), s = $o(i), f = bu(u, s);
        f.tag = EE, f.payload = t, a != null && (Sm(a, "replaceState"), f.callback = a);
        var p = Uo(i, f, s);
        p !== null && (vr(p, i, s, u), Gh(p, i, s)), vs(i, s);
      },
      enqueueForceUpdate: function(e, t) {
        var a = Na(e), i = wa(), u = $o(a), s = bu(i, u);
        s.tag = Ih, t != null && (Sm(t, "forceUpdate"), s.callback = t);
        var f = Uo(a, s, u);
        f !== null && (vr(f, a, u, i), Gh(f, a, u)), wc(a, u);
      }
    };
    function aC(e, t, a, i, u, s, f) {
      var p = e.stateNode;
      if (typeof p.shouldComponentUpdate == "function") {
        var v = p.shouldComponentUpdate(i, s, f);
        {
          if (e.mode & vt) {
            jn(!0);
            try {
              v = p.shouldComponentUpdate(i, s, f);
            } finally {
              jn(!1);
            }
          }
          v === void 0 && S("%s.shouldComponentUpdate(): Returned undefined instead of a boolean value. Make sure to return true or false.", Ct(t) || "Component");
        }
        return v;
      }
      return t.prototype && t.prototype.isPureReactComponent ? !He(a, i) || !He(u, s) : !0;
    }
    function Kx(e, t, a) {
      var i = e.stateNode;
      {
        var u = Ct(t) || "Component", s = i.render;
        s || (t.prototype && typeof t.prototype.render == "function" ? S("%s(...): No `render` method found on the returned component instance: did you accidentally return an object from the constructor?", u) : S("%s(...): No `render` method found on the returned component instance: you may have forgotten to define `render`.", u)), i.getInitialState && !i.getInitialState.isReactClassApproved && !i.state && S("getInitialState was defined on %s, a plain JavaScript class. This is only supported for classes created using React.createClass. Did you mean to define a state property instead?", u), i.getDefaultProps && !i.getDefaultProps.isReactClassApproved && S("getDefaultProps was defined on %s, a plain JavaScript class. This is only supported for classes created using React.createClass. Use a static property to define defaultProps instead.", u), i.propTypes && S("propTypes was defined as an instance property on %s. Use a static property to define propTypes instead.", u), i.contextType && S("contextType was defined as an instance property on %s. Use a static property to define contextType instead.", u), t.childContextTypes && !xp.has(t) && // Strict Mode has its own warning for legacy context, so we can skip
        // this one.
        (e.mode & vt) === Ce && (xp.add(t), S(`%s uses the legacy childContextTypes API which is no longer supported and will be removed in the next major release. Use React.createContext() instead

.Learn more about this warning here: https://reactjs.org/link/legacy-context`, u)), t.contextTypes && !xp.has(t) && // Strict Mode has its own warning for legacy context, so we can skip
        // this one.
        (e.mode & vt) === Ce && (xp.add(t), S(`%s uses the legacy contextTypes API which is no longer supported and will be removed in the next major release. Use React.createContext() with static contextType instead.

Learn more about this warning here: https://reactjs.org/link/legacy-context`, u)), i.contextTypes && S("contextTypes was defined as an instance property on %s. Use a static property to define contextTypes instead.", u), t.contextType && t.contextTypes && !aS.has(t) && (aS.add(t), S("%s declares both contextTypes and contextType static properties. The legacy contextTypes property will be ignored.", u)), typeof i.componentShouldUpdate == "function" && S("%s has a method called componentShouldUpdate(). Did you mean shouldComponentUpdate()? The name is phrased as a question because the function is expected to return a value.", u), t.prototype && t.prototype.isPureReactComponent && typeof i.shouldComponentUpdate < "u" && S("%s has a method called shouldComponentUpdate(). shouldComponentUpdate should not be used when extending React.PureComponent. Please extend React.Component if shouldComponentUpdate is used.", Ct(t) || "A pure component"), typeof i.componentDidUnmount == "function" && S("%s has a method called componentDidUnmount(). But there is no such lifecycle method. Did you mean componentWillUnmount()?", u), typeof i.componentDidReceiveProps == "function" && S("%s has a method called componentDidReceiveProps(). But there is no such lifecycle method. If you meant to update the state in response to changing props, use componentWillReceiveProps(). If you meant to fetch data or run side-effects or mutations after React has updated the UI, use componentDidUpdate().", u), typeof i.componentWillRecieveProps == "function" && S("%s has a method called componentWillRecieveProps(). Did you mean componentWillReceiveProps()?", u), typeof i.UNSAFE_componentWillRecieveProps == "function" && S("%s has a method called UNSAFE_componentWillRecieveProps(). Did you mean UNSAFE_componentWillReceiveProps()?", u);
        var f = i.props !== a;
        i.props !== void 0 && f && S("%s(...): When calling super() in `%s`, make sure to pass up the same props that your component's constructor was passed.", u, u), i.defaultProps && S("Setting defaultProps as an instance property on %s is not supported and will be ignored. Instead, define defaultProps as a static property on %s.", u, u), typeof i.getSnapshotBeforeUpdate == "function" && typeof i.componentDidUpdate != "function" && !eS.has(t) && (eS.add(t), S("%s: getSnapshotBeforeUpdate() should be used with componentDidUpdate(). This component defines getSnapshotBeforeUpdate() only.", Ct(t))), typeof i.getDerivedStateFromProps == "function" && S("%s: getDerivedStateFromProps() is defined as an instance method and will be ignored. Instead, declare it as a static method.", u), typeof i.getDerivedStateFromError == "function" && S("%s: getDerivedStateFromError() is defined as an instance method and will be ignored. Instead, declare it as a static method.", u), typeof t.getSnapshotBeforeUpdate == "function" && S("%s: getSnapshotBeforeUpdate() is defined as a static method and will be ignored. Instead, declare it as an instance method.", u);
        var p = i.state;
        p && (typeof p != "object" || Rt(p)) && S("%s.state: must be set to an object or null", u), typeof i.getChildContext == "function" && typeof t.childContextTypes != "object" && S("%s.getChildContext(): childContextTypes must be defined in order to use getChildContext().", u);
      }
    }
    function iC(e, t) {
      t.updater = uS, e.stateNode = t, Ku(t, e), t._reactInternalInstance = Kg;
    }
    function lC(e, t, a) {
      var i = !1, u = oi, s = oi, f = t.contextType;
      if ("contextType" in t) {
        var p = (
          // Allow null for conditional declaration
          f === null || f !== void 0 && f.$$typeof === Y && f._context === void 0
        );
        if (!p && !iS.has(t)) {
          iS.add(t);
          var v = "";
          f === void 0 ? v = " However, it is set to undefined. This can be caused by a typo or by mixing up named and default imports. This can also happen due to a circular dependency, so try moving the createContext() call to a separate file." : typeof f != "object" ? v = " However, it is set to a " + typeof f + "." : f.$$typeof === R ? v = " Did you accidentally pass the Context.Provider instead?" : f._context !== void 0 ? v = " Did you accidentally pass the Context.Consumer instead?" : v = " However, it is set to an object with keys {" + Object.keys(f).join(", ") + "}.", S("%s defines an invalid contextType. contextType should point to the Context object returned by React.createContext().%s", Ct(t) || "Component", v);
        }
      }
      if (typeof f == "object" && f !== null)
        s = nr(f);
      else {
        u = Sf(e, t, !0);
        var y = t.contextTypes;
        i = y != null, s = i ? Ef(e, u) : oi;
      }
      var g = new t(a, s);
      if (e.mode & vt) {
        jn(!0);
        try {
          g = new t(a, s);
        } finally {
          jn(!1);
        }
      }
      var b = e.memoizedState = g.state !== null && g.state !== void 0 ? g.state : null;
      iC(e, g);
      {
        if (typeof t.getDerivedStateFromProps == "function" && b === null) {
          var x = Ct(t) || "Component";
          Jg.has(x) || (Jg.add(x), S("`%s` uses `getDerivedStateFromProps` but its initial state is %s. This is not recommended. Instead, define the initial state by assigning an object to `this.state` in the constructor of `%s`. This ensures that `getDerivedStateFromProps` arguments have a consistent shape.", x, g.state === null ? "null" : "undefined", x));
        }
        if (typeof t.getDerivedStateFromProps == "function" || typeof g.getSnapshotBeforeUpdate == "function") {
          var N = null, A = null, F = null;
          if (typeof g.componentWillMount == "function" && g.componentWillMount.__suppressDeprecationWarning !== !0 ? N = "componentWillMount" : typeof g.UNSAFE_componentWillMount == "function" && (N = "UNSAFE_componentWillMount"), typeof g.componentWillReceiveProps == "function" && g.componentWillReceiveProps.__suppressDeprecationWarning !== !0 ? A = "componentWillReceiveProps" : typeof g.UNSAFE_componentWillReceiveProps == "function" && (A = "UNSAFE_componentWillReceiveProps"), typeof g.componentWillUpdate == "function" && g.componentWillUpdate.__suppressDeprecationWarning !== !0 ? F = "componentWillUpdate" : typeof g.UNSAFE_componentWillUpdate == "function" && (F = "UNSAFE_componentWillUpdate"), N !== null || A !== null || F !== null) {
            var le = Ct(t) || "Component", Me = typeof t.getDerivedStateFromProps == "function" ? "getDerivedStateFromProps()" : "getSnapshotBeforeUpdate()";
            tS.has(le) || (tS.add(le), S(`Unsafe legacy lifecycles will not be called for components using new component APIs.

%s uses %s but also contains the following legacy lifecycles:%s%s%s

The above lifecycles should be removed. Learn more about this warning here:
https://reactjs.org/link/unsafe-component-lifecycles`, le, Me, N !== null ? `
  ` + N : "", A !== null ? `
  ` + A : "", F !== null ? `
  ` + F : ""));
          }
        }
      }
      return i && q0(e, u, s), g;
    }
    function Zx(e, t) {
      var a = t.state;
      typeof t.componentWillMount == "function" && t.componentWillMount(), typeof t.UNSAFE_componentWillMount == "function" && t.UNSAFE_componentWillMount(), a !== t.state && (S("%s.componentWillMount(): Assigning directly to this.state is deprecated (except inside a component's constructor). Use setState instead.", We(e) || "Component"), uS.enqueueReplaceState(t, t.state, null));
    }
    function uC(e, t, a, i) {
      var u = t.state;
      if (typeof t.componentWillReceiveProps == "function" && t.componentWillReceiveProps(a, i), typeof t.UNSAFE_componentWillReceiveProps == "function" && t.UNSAFE_componentWillReceiveProps(a, i), t.state !== u) {
        {
          var s = We(e) || "Component";
          Zg.has(s) || (Zg.add(s), S("%s.componentWillReceiveProps(): Assigning directly to this.state is deprecated (except inside a component's constructor). Use setState instead.", s));
        }
        uS.enqueueReplaceState(t, t.state, null);
      }
    }
    function oS(e, t, a, i) {
      Kx(e, t, a);
      var u = e.stateNode;
      u.props = a, u.state = e.memoizedState, u.refs = {}, yg(e);
      var s = t.contextType;
      if (typeof s == "object" && s !== null)
        u.context = nr(s);
      else {
        var f = Sf(e, t, !0);
        u.context = Ef(e, f);
      }
      {
        if (u.state === a) {
          var p = Ct(t) || "Component";
          rS.has(p) || (rS.add(p), S("%s: It is not recommended to assign props directly to state because updates to props won't be reflected in state. In most cases, it is better to use props directly.", p));
        }
        e.mode & vt && Ji.recordLegacyContextWarning(e, u), Ji.recordUnsafeLifecycleWarnings(e, u);
      }
      u.state = e.memoizedState;
      var v = t.getDerivedStateFromProps;
      if (typeof v == "function" && (lS(e, t, v, a), u.state = e.memoizedState), typeof t.getDerivedStateFromProps != "function" && typeof u.getSnapshotBeforeUpdate != "function" && (typeof u.UNSAFE_componentWillMount == "function" || typeof u.componentWillMount == "function") && (Zx(e, u), qh(e, a, u, i), u.state = e.memoizedState), typeof u.componentDidMount == "function") {
        var y = et;
        y |= Zr, (e.mode & Ca) !== Ce && (y |= Jr), e.flags |= y;
      }
    }
    function Jx(e, t, a, i) {
      var u = e.stateNode, s = e.memoizedProps;
      u.props = s;
      var f = u.context, p = t.contextType, v = oi;
      if (typeof p == "object" && p !== null)
        v = nr(p);
      else {
        var y = Sf(e, t, !0);
        v = Ef(e, y);
      }
      var g = t.getDerivedStateFromProps, b = typeof g == "function" || typeof u.getSnapshotBeforeUpdate == "function";
      !b && (typeof u.UNSAFE_componentWillReceiveProps == "function" || typeof u.componentWillReceiveProps == "function") && (s !== a || f !== v) && uC(e, u, a, v), RE();
      var x = e.memoizedState, N = u.state = x;
      if (qh(e, a, u, i), N = e.memoizedState, s === a && x === N && !Oh() && !Xh()) {
        if (typeof u.componentDidMount == "function") {
          var A = et;
          A |= Zr, (e.mode & Ca) !== Ce && (A |= Jr), e.flags |= A;
        }
        return !1;
      }
      typeof g == "function" && (lS(e, t, g, a), N = e.memoizedState);
      var F = Xh() || aC(e, t, s, a, x, N, v);
      if (F) {
        if (!b && (typeof u.UNSAFE_componentWillMount == "function" || typeof u.componentWillMount == "function") && (typeof u.componentWillMount == "function" && u.componentWillMount(), typeof u.UNSAFE_componentWillMount == "function" && u.UNSAFE_componentWillMount()), typeof u.componentDidMount == "function") {
          var le = et;
          le |= Zr, (e.mode & Ca) !== Ce && (le |= Jr), e.flags |= le;
        }
      } else {
        if (typeof u.componentDidMount == "function") {
          var Me = et;
          Me |= Zr, (e.mode & Ca) !== Ce && (Me |= Jr), e.flags |= Me;
        }
        e.memoizedProps = a, e.memoizedState = N;
      }
      return u.props = a, u.state = N, u.context = v, F;
    }
    function ew(e, t, a, i, u) {
      var s = t.stateNode;
      CE(e, t);
      var f = t.memoizedProps, p = t.type === t.elementType ? f : nl(t.type, f);
      s.props = p;
      var v = t.pendingProps, y = s.context, g = a.contextType, b = oi;
      if (typeof g == "object" && g !== null)
        b = nr(g);
      else {
        var x = Sf(t, a, !0);
        b = Ef(t, x);
      }
      var N = a.getDerivedStateFromProps, A = typeof N == "function" || typeof s.getSnapshotBeforeUpdate == "function";
      !A && (typeof s.UNSAFE_componentWillReceiveProps == "function" || typeof s.componentWillReceiveProps == "function") && (f !== v || y !== b) && uC(t, s, i, b), RE();
      var F = t.memoizedState, le = s.state = F;
      if (qh(t, i, s, u), le = t.memoizedState, f === v && F === le && !Oh() && !Xh() && !be)
        return typeof s.componentDidUpdate == "function" && (f !== e.memoizedProps || F !== e.memoizedState) && (t.flags |= et), typeof s.getSnapshotBeforeUpdate == "function" && (f !== e.memoizedProps || F !== e.memoizedState) && (t.flags |= za), !1;
      typeof N == "function" && (lS(t, a, N, i), le = t.memoizedState);
      var Me = Xh() || aC(t, a, p, i, F, le, b) || // TODO: In some cases, we'll end up checking if context has changed twice,
      // both before and after `shouldComponentUpdate` has been called. Not ideal,
      // but I'm loath to refactor this function. This only happens for memoized
      // components so it's not that common.
      be;
      return Me ? (!A && (typeof s.UNSAFE_componentWillUpdate == "function" || typeof s.componentWillUpdate == "function") && (typeof s.componentWillUpdate == "function" && s.componentWillUpdate(i, le, b), typeof s.UNSAFE_componentWillUpdate == "function" && s.UNSAFE_componentWillUpdate(i, le, b)), typeof s.componentDidUpdate == "function" && (t.flags |= et), typeof s.getSnapshotBeforeUpdate == "function" && (t.flags |= za)) : (typeof s.componentDidUpdate == "function" && (f !== e.memoizedProps || F !== e.memoizedState) && (t.flags |= et), typeof s.getSnapshotBeforeUpdate == "function" && (f !== e.memoizedProps || F !== e.memoizedState) && (t.flags |= za), t.memoizedProps = i, t.memoizedState = le), s.props = i, s.state = le, s.context = b, Me;
    }
    function Is(e, t) {
      return {
        value: e,
        source: t,
        stack: Fu(t),
        digest: null
      };
    }
    function sS(e, t, a) {
      return {
        value: e,
        source: null,
        stack: a ?? null,
        digest: t ?? null
      };
    }
    function tw(e, t) {
      return !0;
    }
    function cS(e, t) {
      try {
        var a = tw(e, t);
        if (a === !1)
          return;
        var i = t.value, u = t.source, s = t.stack, f = s !== null ? s : "";
        if (i != null && i._suppressLogging) {
          if (e.tag === se)
            return;
          console.error(i);
        }
        var p = u ? We(u) : null, v = p ? "The above error occurred in the <" + p + "> component:" : "The above error occurred in one of your React components:", y;
        if (e.tag === re)
          y = `Consider adding an error boundary to your tree to customize error handling behavior.
Visit https://reactjs.org/link/error-boundaries to learn more about error boundaries.`;
        else {
          var g = We(e) || "Anonymous";
          y = "React will try to recreate this component tree from scratch " + ("using the error boundary you provided, " + g + ".");
        }
        var b = v + `
` + f + `

` + ("" + y);
        console.error(b);
      } catch (x) {
        setTimeout(function() {
          throw x;
        });
      }
    }
    var nw = typeof WeakMap == "function" ? WeakMap : Map;
    function oC(e, t, a) {
      var i = bu(nn, a);
      i.tag = hg, i.payload = {
        element: null
      };
      var u = t.value;
      return i.callback = function() {
        Gb(u), cS(e, t);
      }, i;
    }
    function fS(e, t, a) {
      var i = bu(nn, a);
      i.tag = hg;
      var u = e.type.getDerivedStateFromError;
      if (typeof u == "function") {
        var s = t.value;
        i.payload = function() {
          return u(s);
        }, i.callback = function() {
          S1(e), cS(e, t);
        };
      }
      var f = e.stateNode;
      return f !== null && typeof f.componentDidCatch == "function" && (i.callback = function() {
        S1(e), cS(e, t), typeof u != "function" && Qb(this);
        var v = t.value, y = t.stack;
        this.componentDidCatch(v, {
          componentStack: y !== null ? y : ""
        }), typeof u != "function" && (ia(e.lanes, ke) || S("%s: Error boundaries should implement getDerivedStateFromError(). In that method, return a state update to display an error message or fallback UI.", We(e) || "Unknown"));
      }), i;
    }
    function sC(e, t, a) {
      var i = e.pingCache, u;
      if (i === null ? (i = e.pingCache = new nw(), u = /* @__PURE__ */ new Set(), i.set(t, u)) : (u = i.get(t), u === void 0 && (u = /* @__PURE__ */ new Set(), i.set(t, u))), !u.has(a)) {
        u.add(a);
        var s = qb.bind(null, e, t, a);
        Ea && Pp(e, a), t.then(s, s);
      }
    }
    function rw(e, t, a, i) {
      var u = e.updateQueue;
      if (u === null) {
        var s = /* @__PURE__ */ new Set();
        s.add(a), e.updateQueue = s;
      } else
        u.add(a);
    }
    function aw(e, t) {
      var a = e.tag;
      if ((e.mode & xe) === Ce && (a === de || a === qe || a === Ve)) {
        var i = e.alternate;
        i ? (e.updateQueue = i.updateQueue, e.memoizedState = i.memoizedState, e.lanes = i.lanes) : (e.updateQueue = null, e.memoizedState = null);
      }
    }
    function cC(e) {
      var t = e;
      do {
        if (t.tag === Oe && Fx(t))
          return t;
        t = t.return;
      } while (t !== null);
      return null;
    }
    function fC(e, t, a, i, u) {
      if ((e.mode & xe) === Ce) {
        if (e === t)
          e.flags |= Zn;
        else {
          if (e.flags |= Ie, a.flags |= fs, a.flags &= ~(pc | ya), a.tag === se) {
            var s = a.alternate;
            if (s === null)
              a.tag = _n;
            else {
              var f = bu(nn, ke);
              f.tag = Ih, Uo(a, f, ke);
            }
          }
          a.lanes = Ke(a.lanes, ke);
        }
        return e;
      }
      return e.flags |= Zn, e.lanes = u, e;
    }
    function iw(e, t, a, i, u) {
      if (a.flags |= ya, Ea && Pp(e, u), i !== null && typeof i == "object" && typeof i.then == "function") {
        var s = i;
        aw(a), zr() && a.mode & xe && nE();
        var f = cC(t);
        if (f !== null) {
          f.flags &= ~Tn, fC(f, t, a, e, u), f.mode & xe && sC(e, s, u), rw(f, e, s);
          return;
        } else {
          if (!_d(u)) {
            sC(e, s, u), YS();
            return;
          }
          var p = new Error("A component suspended while responding to synchronous input. This will cause the UI to be replaced with a loading indicator. To fix, updates that suspend should be wrapped with startTransition.");
          i = p;
        }
      } else if (zr() && a.mode & xe) {
        nE();
        var v = cC(t);
        if (v !== null) {
          (v.flags & Zn) === Le && (v.flags |= Tn), fC(v, t, a, e, u), rg(Is(i, a));
          return;
        }
      }
      i = Is(i, a), Fb(i);
      var y = t;
      do {
        switch (y.tag) {
          case re: {
            var g = i;
            y.flags |= Zn;
            var b = fo(u);
            y.lanes = Ke(y.lanes, b);
            var x = oC(y, g, b);
            gg(y, x);
            return;
          }
          case se:
            var N = i, A = y.type, F = y.stateNode;
            if ((y.flags & Ie) === Le && (typeof A.getDerivedStateFromError == "function" || F !== null && typeof F.componentDidCatch == "function" && !c1(F))) {
              y.flags |= Zn;
              var le = fo(u);
              y.lanes = Ke(y.lanes, le);
              var Me = fS(y, N, le);
              gg(y, Me);
              return;
            }
            break;
        }
        y = y.return;
      } while (y !== null);
    }
    function lw() {
      return null;
    }
    var wp = k.ReactCurrentOwner, rl = !1, dS, bp, pS, vS, hS, Qs, mS, Em, _p;
    dS = {}, bp = {}, pS = {}, vS = {}, hS = {}, Qs = !1, mS = {}, Em = {}, _p = {};
    function Ta(e, t, a, i) {
      e === null ? t.child = vE(t, null, a, i) : t.child = xf(t, e.child, a, i);
    }
    function uw(e, t, a, i) {
      t.child = xf(t, e.child, null, i), t.child = xf(t, null, a, i);
    }
    function dC(e, t, a, i, u) {
      if (t.type !== t.elementType) {
        var s = a.propTypes;
        s && Ki(
          s,
          i,
          // Resolved props
          "prop",
          Ct(a)
        );
      }
      var f = a.render, p = t.ref, v, y;
      bf(t, u), to(t);
      {
        if (wp.current = t, qr(!0), v = Mf(e, t, f, i, p, u), y = Nf(), t.mode & vt) {
          jn(!0);
          try {
            v = Mf(e, t, f, i, p, u), y = Nf();
          } finally {
            jn(!1);
          }
        }
        qr(!1);
      }
      return na(), e !== null && !rl ? (kE(e, t, u), _u(e, t, u)) : (zr() && y && Ky(t), t.flags |= xl, Ta(e, t, v, u), t.child);
    }
    function pC(e, t, a, i, u) {
      if (e === null) {
        var s = a.type;
        if (d_(s) && a.compare === null && // SimpleMemoComponent codepath doesn't resolve outer props either.
        a.defaultProps === void 0) {
          var f = s;
          return f = Pf(s), t.tag = Ve, t.type = f, SS(t, s), vC(e, t, f, i, u);
        }
        {
          var p = s.propTypes;
          if (p && Ki(
            p,
            i,
            // Resolved props
            "prop",
            Ct(s)
          ), a.defaultProps !== void 0) {
            var v = Ct(s) || "Unknown";
            _p[v] || (S("%s: Support for defaultProps will be removed from memo components in a future major release. Use JavaScript default parameters instead.", v), _p[v] = !0);
          }
        }
        var y = t0(a.type, null, i, t, t.mode, u);
        return y.ref = t.ref, y.return = t, t.child = y, y;
      }
      {
        var g = a.type, b = g.propTypes;
        b && Ki(
          b,
          i,
          // Resolved props
          "prop",
          Ct(g)
        );
      }
      var x = e.child, N = wS(e, u);
      if (!N) {
        var A = x.memoizedProps, F = a.compare;
        if (F = F !== null ? F : He, F(A, i) && e.ref === t.ref)
          return _u(e, t, u);
      }
      t.flags |= xl;
      var le = Ks(x, i);
      return le.ref = t.ref, le.return = t, t.child = le, le;
    }
    function vC(e, t, a, i, u) {
      if (t.type !== t.elementType) {
        var s = t.elementType;
        if (s.$$typeof === Ae) {
          var f = s, p = f._payload, v = f._init;
          try {
            s = v(p);
          } catch {
            s = null;
          }
          var y = s && s.propTypes;
          y && Ki(
            y,
            i,
            // Resolved (SimpleMemoComponent has no defaultProps)
            "prop",
            Ct(s)
          );
        }
      }
      if (e !== null) {
        var g = e.memoizedProps;
        if (He(g, i) && e.ref === t.ref && // Prevent bailout if the implementation changed due to hot reload.
        t.type === e.type)
          if (rl = !1, t.pendingProps = i = g, wS(e, u))
            (e.flags & fs) !== Le && (rl = !0);
          else
            return t.lanes = e.lanes, _u(e, t, u);
      }
      return yS(e, t, a, i, u);
    }
    function hC(e, t, a) {
      var i = t.pendingProps, u = i.children, s = e !== null ? e.memoizedState : null;
      if (i.mode === "hidden" || ae)
        if ((t.mode & xe) === Ce) {
          var f = {
            baseLanes: $,
            cachePool: null,
            transitions: null
          };
          t.memoizedState = f, Nm(t, a);
        } else if (ia(a, Rr)) {
          var b = {
            baseLanes: $,
            cachePool: null,
            transitions: null
          };
          t.memoizedState = b;
          var x = s !== null ? s.baseLanes : a;
          Nm(t, x);
        } else {
          var p = null, v;
          if (s !== null) {
            var y = s.baseLanes;
            v = Ke(y, a);
          } else
            v = a;
          t.lanes = t.childLanes = Rr;
          var g = {
            baseLanes: v,
            cachePool: p,
            transitions: null
          };
          return t.memoizedState = g, t.updateQueue = null, Nm(t, v), null;
        }
      else {
        var N;
        s !== null ? (N = Ke(s.baseLanes, a), t.memoizedState = null) : N = a, Nm(t, N);
      }
      return Ta(e, t, u, a), t.child;
    }
    function ow(e, t, a) {
      var i = t.pendingProps;
      return Ta(e, t, i, a), t.child;
    }
    function sw(e, t, a) {
      var i = t.pendingProps.children;
      return Ta(e, t, i, a), t.child;
    }
    function cw(e, t, a) {
      {
        t.flags |= et;
        {
          var i = t.stateNode;
          i.effectDuration = 0, i.passiveEffectDuration = 0;
        }
      }
      var u = t.pendingProps, s = u.children;
      return Ta(e, t, s, a), t.child;
    }
    function mC(e, t) {
      var a = t.ref;
      (e === null && a !== null || e !== null && e.ref !== a) && (t.flags |= Kr, t.flags |= vd);
    }
    function yS(e, t, a, i, u) {
      if (t.type !== t.elementType) {
        var s = a.propTypes;
        s && Ki(
          s,
          i,
          // Resolved props
          "prop",
          Ct(a)
        );
      }
      var f;
      {
        var p = Sf(t, a, !0);
        f = Ef(t, p);
      }
      var v, y;
      bf(t, u), to(t);
      {
        if (wp.current = t, qr(!0), v = Mf(e, t, a, i, f, u), y = Nf(), t.mode & vt) {
          jn(!0);
          try {
            v = Mf(e, t, a, i, f, u), y = Nf();
          } finally {
            jn(!1);
          }
        }
        qr(!1);
      }
      return na(), e !== null && !rl ? (kE(e, t, u), _u(e, t, u)) : (zr() && y && Ky(t), t.flags |= xl, Ta(e, t, v, u), t.child);
    }
    function yC(e, t, a, i, u) {
      {
        switch (__(t)) {
          case !1: {
            var s = t.stateNode, f = t.type, p = new f(t.memoizedProps, s.context), v = p.state;
            s.updater.enqueueSetState(s, v, null);
            break;
          }
          case !0: {
            t.flags |= Ie, t.flags |= Zn;
            var y = new Error("Simulated error coming from DevTools"), g = fo(u);
            t.lanes = Ke(t.lanes, g);
            var b = fS(t, Is(y, t), g);
            gg(t, b);
            break;
          }
        }
        if (t.type !== t.elementType) {
          var x = a.propTypes;
          x && Ki(
            x,
            i,
            // Resolved props
            "prop",
            Ct(a)
          );
        }
      }
      var N;
      jl(a) ? (N = !0, Mh(t)) : N = !1, bf(t, u);
      var A = t.stateNode, F;
      A === null ? (Rm(e, t), lC(t, a, i), oS(t, a, i, u), F = !0) : e === null ? F = Jx(t, a, i, u) : F = ew(e, t, a, i, u);
      var le = gS(e, t, a, F, N, u);
      {
        var Me = t.stateNode;
        F && Me.props !== i && (Qs || S("It looks like %s is reassigning its own `this.props` while rendering. This is not supported and can lead to confusing bugs.", We(t) || "a component"), Qs = !0);
      }
      return le;
    }
    function gS(e, t, a, i, u, s) {
      mC(e, t);
      var f = (t.flags & Ie) !== Le;
      if (!i && !f)
        return u && Z0(t, a, !1), _u(e, t, s);
      var p = t.stateNode;
      wp.current = t;
      var v;
      if (f && typeof a.getDerivedStateFromError != "function")
        v = null, tC();
      else {
        to(t);
        {
          if (qr(!0), v = p.render(), t.mode & vt) {
            jn(!0);
            try {
              p.render();
            } finally {
              jn(!1);
            }
          }
          qr(!1);
        }
        na();
      }
      return t.flags |= xl, e !== null && f ? uw(e, t, v, s) : Ta(e, t, v, s), t.memoizedState = p.state, u && Z0(t, a, !0), t.child;
    }
    function gC(e) {
      var t = e.stateNode;
      t.pendingContext ? X0(e, t.pendingContext, t.pendingContext !== t.context) : t.context && X0(e, t.context, !1), Sg(e, t.containerInfo);
    }
    function fw(e, t, a) {
      if (gC(t), e === null)
        throw new Error("Should have a current fiber. This is a bug in React.");
      var i = t.pendingProps, u = t.memoizedState, s = u.element;
      CE(e, t), qh(t, i, null, a);
      var f = t.memoizedState;
      t.stateNode;
      var p = f.element;
      if (u.isDehydrated) {
        var v = {
          element: p,
          isDehydrated: !1,
          cache: f.cache,
          pendingSuspenseBoundaries: f.pendingSuspenseBoundaries,
          transitions: f.transitions
        }, y = t.updateQueue;
        if (y.baseState = v, t.memoizedState = v, t.flags & Tn) {
          var g = Is(new Error("There was an error while hydrating. Because the error happened outside of a Suspense boundary, the entire root will switch to client rendering."), t);
          return SC(e, t, p, a, g);
        } else if (p !== s) {
          var b = Is(new Error("This root received an early update, before anything was able hydrate. Switched the entire root to client rendering."), t);
          return SC(e, t, p, a, b);
        } else {
          vx(t);
          var x = vE(t, null, p, a);
          t.child = x;
          for (var N = x; N; )
            N.flags = N.flags & ~ln | Ua, N = N.sibling;
        }
      } else {
        if (Tf(), p === s)
          return _u(e, t, a);
        Ta(e, t, p, a);
      }
      return t.child;
    }
    function SC(e, t, a, i, u) {
      return Tf(), rg(u), t.flags |= Tn, Ta(e, t, a, i), t.child;
    }
    function dw(e, t, a) {
      wE(t), e === null && ng(t);
      var i = t.type, u = t.pendingProps, s = e !== null ? e.memoizedProps : null, f = u.children, p = jy(i, u);
      return p ? f = null : s !== null && jy(i, s) && (t.flags |= $t), mC(e, t), Ta(e, t, f, a), t.child;
    }
    function pw(e, t) {
      return e === null && ng(t), null;
    }
    function vw(e, t, a, i) {
      Rm(e, t);
      var u = t.pendingProps, s = a, f = s._payload, p = s._init, v = p(f);
      t.type = v;
      var y = t.tag = p_(v), g = nl(v, u), b;
      switch (y) {
        case de:
          return SS(t, v), t.type = v = Pf(v), b = yS(null, t, v, g, i), b;
        case se:
          return t.type = v = qS(v), b = yC(null, t, v, g, i), b;
        case qe:
          return t.type = v = XS(v), b = dC(null, t, v, g, i), b;
        case ft: {
          if (t.type !== t.elementType) {
            var x = v.propTypes;
            x && Ki(
              x,
              g,
              // Resolved for outer only
              "prop",
              Ct(v)
            );
          }
          return b = pC(
            null,
            t,
            v,
            nl(v.type, g),
            // The inner type can have defaults too
            i
          ), b;
        }
      }
      var N = "";
      throw v !== null && typeof v == "object" && v.$$typeof === Ae && (N = " Did you wrap a component in React.lazy() more than once?"), new Error("Element type is invalid. Received a promise that resolves to: " + v + ". " + ("Lazy element type must resolve to a class or function." + N));
    }
    function hw(e, t, a, i, u) {
      Rm(e, t), t.tag = se;
      var s;
      return jl(a) ? (s = !0, Mh(t)) : s = !1, bf(t, u), lC(t, a, i), oS(t, a, i, u), gS(null, t, a, !0, s, u);
    }
    function mw(e, t, a, i) {
      Rm(e, t);
      var u = t.pendingProps, s;
      {
        var f = Sf(t, a, !1);
        s = Ef(t, f);
      }
      bf(t, i);
      var p, v;
      to(t);
      {
        if (a.prototype && typeof a.prototype.render == "function") {
          var y = Ct(a) || "Unknown";
          dS[y] || (S("The <%s /> component appears to have a render method, but doesn't extend React.Component. This is likely to cause errors. Change %s to extend React.Component instead.", y, y), dS[y] = !0);
        }
        t.mode & vt && Ji.recordLegacyContextWarning(t, null), qr(!0), wp.current = t, p = Mf(null, t, a, u, s, i), v = Nf(), qr(!1);
      }
      if (na(), t.flags |= xl, typeof p == "object" && p !== null && typeof p.render == "function" && p.$$typeof === void 0) {
        var g = Ct(a) || "Unknown";
        bp[g] || (S("The <%s /> component appears to be a function component that returns a class instance. Change %s to a class that extends React.Component instead. If you can't use a class try assigning the prototype on the function as a workaround. `%s.prototype = React.Component.prototype`. Don't use an arrow function since it cannot be called with `new` by React.", g, g, g), bp[g] = !0);
      }
      if (
        // Run these checks in production only if the flag is off.
        // Eventually we'll delete this branch altogether.
        typeof p == "object" && p !== null && typeof p.render == "function" && p.$$typeof === void 0
      ) {
        {
          var b = Ct(a) || "Unknown";
          bp[b] || (S("The <%s /> component appears to be a function component that returns a class instance. Change %s to a class that extends React.Component instead. If you can't use a class try assigning the prototype on the function as a workaround. `%s.prototype = React.Component.prototype`. Don't use an arrow function since it cannot be called with `new` by React.", b, b, b), bp[b] = !0);
        }
        t.tag = se, t.memoizedState = null, t.updateQueue = null;
        var x = !1;
        return jl(a) ? (x = !0, Mh(t)) : x = !1, t.memoizedState = p.state !== null && p.state !== void 0 ? p.state : null, yg(t), iC(t, p), oS(t, a, u, i), gS(null, t, a, !0, x, i);
      } else {
        if (t.tag = de, t.mode & vt) {
          jn(!0);
          try {
            p = Mf(null, t, a, u, s, i), v = Nf();
          } finally {
            jn(!1);
          }
        }
        return zr() && v && Ky(t), Ta(null, t, p, i), SS(t, a), t.child;
      }
    }
    function SS(e, t) {
      {
        if (t && t.childContextTypes && S("%s(...): childContextTypes cannot be defined on a function component.", t.displayName || t.name || "Component"), e.ref !== null) {
          var a = "", i = Lr();
          i && (a += `

Check the render method of \`` + i + "`.");
          var u = i || "", s = e._debugSource;
          s && (u = s.fileName + ":" + s.lineNumber), hS[u] || (hS[u] = !0, S("Function components cannot be given refs. Attempts to access this ref will fail. Did you mean to use React.forwardRef()?%s", a));
        }
        if (t.defaultProps !== void 0) {
          var f = Ct(t) || "Unknown";
          _p[f] || (S("%s: Support for defaultProps will be removed from function components in a future major release. Use JavaScript default parameters instead.", f), _p[f] = !0);
        }
        if (typeof t.getDerivedStateFromProps == "function") {
          var p = Ct(t) || "Unknown";
          vS[p] || (S("%s: Function components do not support getDerivedStateFromProps.", p), vS[p] = !0);
        }
        if (typeof t.contextType == "object" && t.contextType !== null) {
          var v = Ct(t) || "Unknown";
          pS[v] || (S("%s: Function components do not support contextType.", v), pS[v] = !0);
        }
      }
    }
    var ES = {
      dehydrated: null,
      treeContext: null,
      retryLane: Fn
    };
    function CS(e) {
      return {
        baseLanes: e,
        cachePool: lw(),
        transitions: null
      };
    }
    function yw(e, t) {
      var a = null;
      return {
        baseLanes: Ke(e.baseLanes, t),
        cachePool: a,
        transitions: e.transitions
      };
    }
    function gw(e, t, a, i) {
      if (t !== null) {
        var u = t.memoizedState;
        if (u === null)
          return !1;
      }
      return Rg(e, mp);
    }
    function Sw(e, t) {
      return Cs(e.childLanes, t);
    }
    function EC(e, t, a) {
      var i = t.pendingProps;
      k_(t) && (t.flags |= Ie);
      var u = el.current, s = !1, f = (t.flags & Ie) !== Le;
      if (f || gw(u, e) ? (s = !0, t.flags &= ~Ie) : (e === null || e.memoizedState !== null) && (u = jx(u, _E)), u = kf(u), jo(t, u), e === null) {
        ng(t);
        var p = t.memoizedState;
        if (p !== null) {
          var v = p.dehydrated;
          if (v !== null)
            return xw(t, v);
        }
        var y = i.children, g = i.fallback;
        if (s) {
          var b = Ew(t, y, g, a), x = t.child;
          return x.memoizedState = CS(a), t.memoizedState = ES, b;
        } else
          return RS(t, y);
      } else {
        var N = e.memoizedState;
        if (N !== null) {
          var A = N.dehydrated;
          if (A !== null)
            return ww(e, t, f, i, A, N, a);
        }
        if (s) {
          var F = i.fallback, le = i.children, Me = Rw(e, t, le, F, a), we = t.child, wt = e.child.memoizedState;
          return we.memoizedState = wt === null ? CS(a) : yw(wt, a), we.childLanes = Sw(e, a), t.memoizedState = ES, Me;
        } else {
          var gt = i.children, O = Cw(e, t, gt, a);
          return t.memoizedState = null, O;
        }
      }
    }
    function RS(e, t, a) {
      var i = e.mode, u = {
        mode: "visible",
        children: t
      }, s = TS(u, i);
      return s.return = e, e.child = s, s;
    }
    function Ew(e, t, a, i) {
      var u = e.mode, s = e.child, f = {
        mode: "hidden",
        children: t
      }, p, v;
      return (u & xe) === Ce && s !== null ? (p = s, p.childLanes = $, p.pendingProps = f, e.mode & Qe && (p.actualDuration = 0, p.actualStartTime = -1, p.selfBaseDuration = 0, p.treeBaseDuration = 0), v = Io(a, u, i, null)) : (p = TS(f, u), v = Io(a, u, i, null)), p.return = e, v.return = e, p.sibling = v, e.child = p, v;
    }
    function TS(e, t, a) {
      return C1(e, t, $, null);
    }
    function CC(e, t) {
      return Ks(e, t);
    }
    function Cw(e, t, a, i) {
      var u = e.child, s = u.sibling, f = CC(u, {
        mode: "visible",
        children: a
      });
      if ((t.mode & xe) === Ce && (f.lanes = i), f.return = t, f.sibling = null, s !== null) {
        var p = t.deletions;
        p === null ? (t.deletions = [s], t.flags |= jt) : p.push(s);
      }
      return t.child = f, f;
    }
    function Rw(e, t, a, i, u) {
      var s = t.mode, f = e.child, p = f.sibling, v = {
        mode: "hidden",
        children: a
      }, y;
      if (
        // In legacy mode, we commit the primary tree as if it successfully
        // completed, even though it's in an inconsistent state.
        (s & xe) === Ce && // Make sure we're on the second pass, i.e. the primary child fragment was
        // already cloned. In legacy mode, the only case where this isn't true is
        // when DevTools forces us to display a fallback; we skip the first render
        // pass entirely and go straight to rendering the fallback. (In Concurrent
        // Mode, SuspenseList can also trigger this scenario, but this is a legacy-
        // only codepath.)
        t.child !== f
      ) {
        var g = t.child;
        y = g, y.childLanes = $, y.pendingProps = v, t.mode & Qe && (y.actualDuration = 0, y.actualStartTime = -1, y.selfBaseDuration = f.selfBaseDuration, y.treeBaseDuration = f.treeBaseDuration), t.deletions = null;
      } else
        y = CC(f, v), y.subtreeFlags = f.subtreeFlags & ar;
      var b;
      return p !== null ? b = Ks(p, i) : (b = Io(i, s, u, null), b.flags |= ln), b.return = t, y.return = t, y.sibling = b, t.child = y, b;
    }
    function Cm(e, t, a, i) {
      i !== null && rg(i), xf(t, e.child, null, a);
      var u = t.pendingProps, s = u.children, f = RS(t, s);
      return f.flags |= ln, t.memoizedState = null, f;
    }
    function Tw(e, t, a, i, u) {
      var s = t.mode, f = {
        mode: "visible",
        children: a
      }, p = TS(f, s), v = Io(i, s, u, null);
      return v.flags |= ln, p.return = t, v.return = t, p.sibling = v, t.child = p, (t.mode & xe) !== Ce && xf(t, e.child, null, u), v;
    }
    function xw(e, t, a) {
      return (e.mode & xe) === Ce ? (S("Cannot hydrate Suspense in legacy mode. Switch from ReactDOM.hydrate(element, container) to ReactDOMClient.hydrateRoot(container, <App />).render(element) or remove the Suspense components from the server rendered components."), e.lanes = ke) : Py(t) ? e.lanes = Qi : e.lanes = Rr, null;
    }
    function ww(e, t, a, i, u, s, f) {
      if (a)
        if (t.flags & Tn) {
          t.flags &= ~Tn;
          var O = sS(new Error("There was an error while hydrating this Suspense boundary. Switched to client rendering."));
          return Cm(e, t, f, O);
        } else {
          if (t.memoizedState !== null)
            return t.child = e.child, t.flags |= Ie, null;
          var H = i.children, L = i.fallback, X = Tw(e, t, H, L, f), ve = t.child;
          return ve.memoizedState = CS(f), t.memoizedState = ES, X;
        }
      else {
        if (dx(), (t.mode & xe) === Ce)
          return Cm(
            e,
            t,
            f,
            // TODO: When we delete legacy mode, we should make this error argument
            // required — every concurrent mode path that causes hydration to
            // de-opt to client rendering should have an error message.
            null
          );
        if (Py(u)) {
          var p, v, y;
          {
            var g = DT(u);
            p = g.digest, v = g.message, y = g.stack;
          }
          var b;
          v ? b = new Error(v) : b = new Error("The server could not finish this Suspense boundary, likely due to an error during server rendering. Switched to client rendering.");
          var x = sS(b, p, y);
          return Cm(e, t, f, x);
        }
        var N = ia(f, e.childLanes);
        if (rl || N) {
          var A = Mm();
          if (A !== null) {
            var F = Wv(A, f);
            if (F !== Fn && F !== s.retryLane) {
              s.retryLane = F;
              var le = nn;
              Wa(e, F), vr(A, e, F, le);
            }
          }
          YS();
          var Me = sS(new Error("This Suspense boundary received an update before it finished hydrating. This caused the boundary to switch to client rendering. The usual way to fix this is to wrap the original update in startTransition."));
          return Cm(e, t, f, Me);
        } else if (Y0(u)) {
          t.flags |= Ie, t.child = e.child;
          var we = Xb.bind(null, e);
          return OT(u, we), null;
        } else {
          hx(t, u, s.treeContext);
          var wt = i.children, gt = RS(t, wt);
          return gt.flags |= Ua, gt;
        }
      }
    }
    function RC(e, t, a) {
      e.lanes = Ke(e.lanes, t);
      var i = e.alternate;
      i !== null && (i.lanes = Ke(i.lanes, t)), pg(e.return, t, a);
    }
    function bw(e, t, a) {
      for (var i = t; i !== null; ) {
        if (i.tag === Oe) {
          var u = i.memoizedState;
          u !== null && RC(i, a, e);
        } else if (i.tag === Ot)
          RC(i, a, e);
        else if (i.child !== null) {
          i.child.return = i, i = i.child;
          continue;
        }
        if (i === e)
          return;
        for (; i.sibling === null; ) {
          if (i.return === null || i.return === e)
            return;
          i = i.return;
        }
        i.sibling.return = i.return, i = i.sibling;
      }
    }
    function _w(e) {
      for (var t = e, a = null; t !== null; ) {
        var i = t.alternate;
        i !== null && Jh(i) === null && (a = t), t = t.sibling;
      }
      return a;
    }
    function kw(e) {
      if (e !== void 0 && e !== "forwards" && e !== "backwards" && e !== "together" && !mS[e])
        if (mS[e] = !0, typeof e == "string")
          switch (e.toLowerCase()) {
            case "together":
            case "forwards":
            case "backwards": {
              S('"%s" is not a valid value for revealOrder on <SuspenseList />. Use lowercase "%s" instead.', e, e.toLowerCase());
              break;
            }
            case "forward":
            case "backward": {
              S('"%s" is not a valid value for revealOrder on <SuspenseList />. React uses the -s suffix in the spelling. Use "%ss" instead.', e, e.toLowerCase());
              break;
            }
            default:
              S('"%s" is not a supported revealOrder on <SuspenseList />. Did you mean "together", "forwards" or "backwards"?', e);
              break;
          }
        else
          S('%s is not a supported value for revealOrder on <SuspenseList />. Did you mean "together", "forwards" or "backwards"?', e);
    }
    function Dw(e, t) {
      e !== void 0 && !Em[e] && (e !== "collapsed" && e !== "hidden" ? (Em[e] = !0, S('"%s" is not a supported value for tail on <SuspenseList />. Did you mean "collapsed" or "hidden"?', e)) : t !== "forwards" && t !== "backwards" && (Em[e] = !0, S('<SuspenseList tail="%s" /> is only valid if revealOrder is "forwards" or "backwards". Did you mean to specify revealOrder="forwards"?', e)));
    }
    function TC(e, t) {
      {
        var a = Rt(e), i = !a && typeof kr(e) == "function";
        if (a || i) {
          var u = a ? "array" : "iterable";
          return S("A nested %s was passed to row #%s in <SuspenseList />. Wrap it in an additional SuspenseList to configure its revealOrder: <SuspenseList revealOrder=...> ... <SuspenseList revealOrder=...>{%s}</SuspenseList> ... </SuspenseList>", u, t, u), !1;
        }
      }
      return !0;
    }
    function Ow(e, t) {
      if ((t === "forwards" || t === "backwards") && e !== void 0 && e !== null && e !== !1)
        if (Rt(e)) {
          for (var a = 0; a < e.length; a++)
            if (!TC(e[a], a))
              return;
        } else {
          var i = kr(e);
          if (typeof i == "function") {
            var u = i.call(e);
            if (u)
              for (var s = u.next(), f = 0; !s.done; s = u.next()) {
                if (!TC(s.value, f))
                  return;
                f++;
              }
          } else
            S('A single row was passed to a <SuspenseList revealOrder="%s" />. This is not useful since it needs multiple rows. Did you mean to pass multiple children or an array?', t);
        }
    }
    function xS(e, t, a, i, u) {
      var s = e.memoizedState;
      s === null ? e.memoizedState = {
        isBackwards: t,
        rendering: null,
        renderingStartTime: 0,
        last: i,
        tail: a,
        tailMode: u
      } : (s.isBackwards = t, s.rendering = null, s.renderingStartTime = 0, s.last = i, s.tail = a, s.tailMode = u);
    }
    function xC(e, t, a) {
      var i = t.pendingProps, u = i.revealOrder, s = i.tail, f = i.children;
      kw(u), Dw(s, u), Ow(f, u), Ta(e, t, f, a);
      var p = el.current, v = Rg(p, mp);
      if (v)
        p = Tg(p, mp), t.flags |= Ie;
      else {
        var y = e !== null && (e.flags & Ie) !== Le;
        y && bw(t, t.child, a), p = kf(p);
      }
      if (jo(t, p), (t.mode & xe) === Ce)
        t.memoizedState = null;
      else
        switch (u) {
          case "forwards": {
            var g = _w(t.child), b;
            g === null ? (b = t.child, t.child = null) : (b = g.sibling, g.sibling = null), xS(
              t,
              !1,
              // isBackwards
              b,
              g,
              s
            );
            break;
          }
          case "backwards": {
            var x = null, N = t.child;
            for (t.child = null; N !== null; ) {
              var A = N.alternate;
              if (A !== null && Jh(A) === null) {
                t.child = N;
                break;
              }
              var F = N.sibling;
              N.sibling = x, x = N, N = F;
            }
            xS(
              t,
              !0,
              // isBackwards
              x,
              null,
              // last
              s
            );
            break;
          }
          case "together": {
            xS(
              t,
              !1,
              // isBackwards
              null,
              // tail
              null,
              // last
              void 0
            );
            break;
          }
          default:
            t.memoizedState = null;
        }
      return t.child;
    }
    function Lw(e, t, a) {
      Sg(t, t.stateNode.containerInfo);
      var i = t.pendingProps;
      return e === null ? t.child = xf(t, null, i, a) : Ta(e, t, i, a), t.child;
    }
    var wC = !1;
    function Mw(e, t, a) {
      var i = t.type, u = i._context, s = t.pendingProps, f = t.memoizedProps, p = s.value;
      {
        "value" in s || wC || (wC = !0, S("The `value` prop is required for the `<Context.Provider>`. Did you misspell it or forget to pass it?"));
        var v = t.type.propTypes;
        v && Ki(v, s, "prop", "Context.Provider");
      }
      if (yE(t, u, p), f !== null) {
        var y = f.value;
        if (ge(y, p)) {
          if (f.children === s.children && !Oh())
            return _u(e, t, a);
        } else
          kx(t, u, a);
      }
      var g = s.children;
      return Ta(e, t, g, a), t.child;
    }
    var bC = !1;
    function Nw(e, t, a) {
      var i = t.type;
      i._context === void 0 ? i !== i.Consumer && (bC || (bC = !0, S("Rendering <Context> directly is not supported and will be removed in a future major release. Did you mean to render <Context.Consumer> instead?"))) : i = i._context;
      var u = t.pendingProps, s = u.children;
      typeof s != "function" && S("A context consumer was rendered with multiple children, or a child that isn't a function. A context consumer expects a single child that is a function. If you did pass a function, make sure there is no trailing or leading whitespace around it."), bf(t, a);
      var f = nr(i);
      to(t);
      var p;
      return wp.current = t, qr(!0), p = s(f), qr(!1), na(), t.flags |= xl, Ta(e, t, p, a), t.child;
    }
    function kp() {
      rl = !0;
    }
    function Rm(e, t) {
      (t.mode & xe) === Ce && e !== null && (e.alternate = null, t.alternate = null, t.flags |= ln);
    }
    function _u(e, t, a) {
      return e !== null && (t.dependencies = e.dependencies), tC(), Vp(t.lanes), ia(a, t.childLanes) ? (bx(e, t), t.child) : null;
    }
    function zw(e, t, a) {
      {
        var i = t.return;
        if (i === null)
          throw new Error("Cannot swap the root fiber.");
        if (e.alternate = null, t.alternate = null, a.index = t.index, a.sibling = t.sibling, a.return = t.return, a.ref = t.ref, t === i.child)
          i.child = a;
        else {
          var u = i.child;
          if (u === null)
            throw new Error("Expected parent to have a child.");
          for (; u.sibling !== t; )
            if (u = u.sibling, u === null)
              throw new Error("Expected to find the previous sibling.");
          u.sibling = a;
        }
        var s = i.deletions;
        return s === null ? (i.deletions = [e], i.flags |= jt) : s.push(e), a.flags |= ln, a;
      }
    }
    function wS(e, t) {
      var a = e.lanes;
      return !!ia(a, t);
    }
    function Uw(e, t, a) {
      switch (t.tag) {
        case re:
          gC(t), t.stateNode, Tf();
          break;
        case ue:
          wE(t);
          break;
        case se: {
          var i = t.type;
          jl(i) && Mh(t);
          break;
        }
        case pe:
          Sg(t, t.stateNode.containerInfo);
          break;
        case ot: {
          var u = t.memoizedProps.value, s = t.type._context;
          yE(t, s, u);
          break;
        }
        case mt:
          {
            var f = ia(a, t.childLanes);
            f && (t.flags |= et);
            {
              var p = t.stateNode;
              p.effectDuration = 0, p.passiveEffectDuration = 0;
            }
          }
          break;
        case Oe: {
          var v = t.memoizedState;
          if (v !== null) {
            if (v.dehydrated !== null)
              return jo(t, kf(el.current)), t.flags |= Ie, null;
            var y = t.child, g = y.childLanes;
            if (ia(a, g))
              return EC(e, t, a);
            jo(t, kf(el.current));
            var b = _u(e, t, a);
            return b !== null ? b.sibling : null;
          } else
            jo(t, kf(el.current));
          break;
        }
        case Ot: {
          var x = (e.flags & Ie) !== Le, N = ia(a, t.childLanes);
          if (x) {
            if (N)
              return xC(e, t, a);
            t.flags |= Ie;
          }
          var A = t.memoizedState;
          if (A !== null && (A.rendering = null, A.tail = null, A.lastEffect = null), jo(t, el.current), N)
            break;
          return null;
        }
        case ze:
        case Je:
          return t.lanes = $, hC(e, t, a);
      }
      return _u(e, t, a);
    }
    function _C(e, t, a) {
      if (t._debugNeedsRemount && e !== null)
        return zw(e, t, t0(t.type, t.key, t.pendingProps, t._debugOwner || null, t.mode, t.lanes));
      if (e !== null) {
        var i = e.memoizedProps, u = t.pendingProps;
        if (i !== u || Oh() || // Force a re-render if the implementation changed due to hot reload:
        t.type !== e.type)
          rl = !0;
        else {
          var s = wS(e, a);
          if (!s && // If this is the second pass of an error or suspense boundary, there
          // may not be work scheduled on `current`, so we check for this flag.
          (t.flags & Ie) === Le)
            return rl = !1, Uw(e, t, a);
          (e.flags & fs) !== Le ? rl = !0 : rl = !1;
        }
      } else if (rl = !1, zr() && lx(t)) {
        var f = t.index, p = ux();
        tE(t, p, f);
      }
      switch (t.lanes = $, t.tag) {
        case nt:
          return mw(e, t, t.type, a);
        case rn: {
          var v = t.elementType;
          return vw(e, t, v, a);
        }
        case de: {
          var y = t.type, g = t.pendingProps, b = t.elementType === y ? g : nl(y, g);
          return yS(e, t, y, b, a);
        }
        case se: {
          var x = t.type, N = t.pendingProps, A = t.elementType === x ? N : nl(x, N);
          return yC(e, t, x, A, a);
        }
        case re:
          return fw(e, t, a);
        case ue:
          return dw(e, t, a);
        case Ye:
          return pw(e, t);
        case Oe:
          return EC(e, t, a);
        case pe:
          return Lw(e, t, a);
        case qe: {
          var F = t.type, le = t.pendingProps, Me = t.elementType === F ? le : nl(F, le);
          return dC(e, t, F, Me, a);
        }
        case bt:
          return ow(e, t, a);
        case ht:
          return sw(e, t, a);
        case mt:
          return cw(e, t, a);
        case ot:
          return Mw(e, t, a);
        case pn:
          return Nw(e, t, a);
        case ft: {
          var we = t.type, wt = t.pendingProps, gt = nl(we, wt);
          if (t.type !== t.elementType) {
            var O = we.propTypes;
            O && Ki(
              O,
              gt,
              // Resolved for outer only
              "prop",
              Ct(we)
            );
          }
          return gt = nl(we.type, gt), pC(e, t, we, gt, a);
        }
        case Ve:
          return vC(e, t, t.type, t.pendingProps, a);
        case _n: {
          var H = t.type, L = t.pendingProps, X = t.elementType === H ? L : nl(H, L);
          return hw(e, t, H, X, a);
        }
        case Ot:
          return xC(e, t, a);
        case Cn:
          break;
        case ze:
          return hC(e, t, a);
      }
      throw new Error("Unknown unit of work tag (" + t.tag + "). This error is likely caused by a bug in React. Please file an issue.");
    }
    function zf(e) {
      e.flags |= et;
    }
    function kC(e) {
      e.flags |= Kr, e.flags |= vd;
    }
    var DC, bS, OC, LC;
    DC = function(e, t, a, i) {
      for (var u = t.child; u !== null; ) {
        if (u.tag === ue || u.tag === Ye)
          rT(e, u.stateNode);
        else if (u.tag !== pe) {
          if (u.child !== null) {
            u.child.return = u, u = u.child;
            continue;
          }
        }
        if (u === t)
          return;
        for (; u.sibling === null; ) {
          if (u.return === null || u.return === t)
            return;
          u = u.return;
        }
        u.sibling.return = u.return, u = u.sibling;
      }
    }, bS = function(e, t) {
    }, OC = function(e, t, a, i, u) {
      var s = e.memoizedProps;
      if (s !== i) {
        var f = t.stateNode, p = Eg(), v = iT(f, a, s, i, u, p);
        t.updateQueue = v, v && zf(t);
      }
    }, LC = function(e, t, a, i) {
      a !== i && zf(t);
    };
    function Dp(e, t) {
      if (!zr())
        switch (e.tailMode) {
          case "hidden": {
            for (var a = e.tail, i = null; a !== null; )
              a.alternate !== null && (i = a), a = a.sibling;
            i === null ? e.tail = null : i.sibling = null;
            break;
          }
          case "collapsed": {
            for (var u = e.tail, s = null; u !== null; )
              u.alternate !== null && (s = u), u = u.sibling;
            s === null ? !t && e.tail !== null ? e.tail.sibling = null : e.tail = null : s.sibling = null;
            break;
          }
        }
    }
    function Ar(e) {
      var t = e.alternate !== null && e.alternate.child === e.child, a = $, i = Le;
      if (t) {
        if ((e.mode & Qe) !== Ce) {
          for (var v = e.selfBaseDuration, y = e.child; y !== null; )
            a = Ke(a, Ke(y.lanes, y.childLanes)), i |= y.subtreeFlags & ar, i |= y.flags & ar, v += y.treeBaseDuration, y = y.sibling;
          e.treeBaseDuration = v;
        } else
          for (var g = e.child; g !== null; )
            a = Ke(a, Ke(g.lanes, g.childLanes)), i |= g.subtreeFlags & ar, i |= g.flags & ar, g.return = e, g = g.sibling;
        e.subtreeFlags |= i;
      } else {
        if ((e.mode & Qe) !== Ce) {
          for (var u = e.actualDuration, s = e.selfBaseDuration, f = e.child; f !== null; )
            a = Ke(a, Ke(f.lanes, f.childLanes)), i |= f.subtreeFlags, i |= f.flags, u += f.actualDuration, s += f.treeBaseDuration, f = f.sibling;
          e.actualDuration = u, e.treeBaseDuration = s;
        } else
          for (var p = e.child; p !== null; )
            a = Ke(a, Ke(p.lanes, p.childLanes)), i |= p.subtreeFlags, i |= p.flags, p.return = e, p = p.sibling;
        e.subtreeFlags |= i;
      }
      return e.childLanes = a, t;
    }
    function Aw(e, t, a) {
      if (Ex() && (t.mode & xe) !== Ce && (t.flags & Ie) === Le)
        return oE(t), Tf(), t.flags |= Tn | ya | Zn, !1;
      var i = jh(t);
      if (a !== null && a.dehydrated !== null)
        if (e === null) {
          if (!i)
            throw new Error("A dehydrated suspense component was completed without a hydrated node. This is probably a bug in React.");
          if (gx(t), Ar(t), (t.mode & Qe) !== Ce) {
            var u = a !== null;
            if (u) {
              var s = t.child;
              s !== null && (t.treeBaseDuration -= s.treeBaseDuration);
            }
          }
          return !1;
        } else {
          if (Tf(), (t.flags & Ie) === Le && (t.memoizedState = null), t.flags |= et, Ar(t), (t.mode & Qe) !== Ce) {
            var f = a !== null;
            if (f) {
              var p = t.child;
              p !== null && (t.treeBaseDuration -= p.treeBaseDuration);
            }
          }
          return !1;
        }
      else
        return sE(), !0;
    }
    function MC(e, t, a) {
      var i = t.pendingProps;
      switch (Zy(t), t.tag) {
        case nt:
        case rn:
        case Ve:
        case de:
        case qe:
        case bt:
        case ht:
        case mt:
        case pn:
        case ft:
          return Ar(t), null;
        case se: {
          var u = t.type;
          return jl(u) && Lh(t), Ar(t), null;
        }
        case re: {
          var s = t.stateNode;
          if (_f(t), Gy(t), wg(), s.pendingContext && (s.context = s.pendingContext, s.pendingContext = null), e === null || e.child === null) {
            var f = jh(t);
            if (f)
              zf(t);
            else if (e !== null) {
              var p = e.memoizedState;
              // Check if this is a client root
              (!p.isDehydrated || // Check if we reverted to client rendering (e.g. due to an error)
              (t.flags & Tn) !== Le) && (t.flags |= za, sE());
            }
          }
          return bS(e, t), Ar(t), null;
        }
        case ue: {
          Cg(t);
          var v = xE(), y = t.type;
          if (e !== null && t.stateNode != null)
            OC(e, t, y, i, v), e.ref !== t.ref && kC(t);
          else {
            if (!i) {
              if (t.stateNode === null)
                throw new Error("We must have new props for new mounts. This error is likely caused by a bug in React. Please file an issue.");
              return Ar(t), null;
            }
            var g = Eg(), b = jh(t);
            if (b)
              mx(t, v, g) && zf(t);
            else {
              var x = nT(y, i, v, g, t);
              DC(x, t, !1, !1), t.stateNode = x, aT(x, y, i, v) && zf(t);
            }
            t.ref !== null && kC(t);
          }
          return Ar(t), null;
        }
        case Ye: {
          var N = i;
          if (e && t.stateNode != null) {
            var A = e.memoizedProps;
            LC(e, t, A, N);
          } else {
            if (typeof N != "string" && t.stateNode === null)
              throw new Error("We must have new props for new mounts. This error is likely caused by a bug in React. Please file an issue.");
            var F = xE(), le = Eg(), Me = jh(t);
            Me ? yx(t) && zf(t) : t.stateNode = lT(N, F, le, t);
          }
          return Ar(t), null;
        }
        case Oe: {
          Df(t);
          var we = t.memoizedState;
          if (e === null || e.memoizedState !== null && e.memoizedState.dehydrated !== null) {
            var wt = Aw(e, t, we);
            if (!wt)
              return t.flags & Zn ? t : null;
          }
          if ((t.flags & Ie) !== Le)
            return t.lanes = a, (t.mode & Qe) !== Ce && Xg(t), t;
          var gt = we !== null, O = e !== null && e.memoizedState !== null;
          if (gt !== O && gt) {
            var H = t.child;
            if (H.flags |= wl, (t.mode & xe) !== Ce) {
              var L = e === null && (t.memoizedProps.unstable_avoidThisFallback !== !0 || !_);
              L || Rg(el.current, _E) ? jb() : YS();
            }
          }
          var X = t.updateQueue;
          if (X !== null && (t.flags |= et), Ar(t), (t.mode & Qe) !== Ce && gt) {
            var ve = t.child;
            ve !== null && (t.treeBaseDuration -= ve.treeBaseDuration);
          }
          return null;
        }
        case pe:
          return _f(t), bS(e, t), e === null && JT(t.stateNode.containerInfo), Ar(t), null;
        case ot:
          var oe = t.type._context;
          return dg(oe, t), Ar(t), null;
        case _n: {
          var Be = t.type;
          return jl(Be) && Lh(t), Ar(t), null;
        }
        case Ot: {
          Df(t);
          var Xe = t.memoizedState;
          if (Xe === null)
            return Ar(t), null;
          var qt = (t.flags & Ie) !== Le, zt = Xe.rendering;
          if (zt === null)
            if (qt)
              Dp(Xe, !1);
            else {
              var Qn = Hb() && (e === null || (e.flags & Ie) === Le);
              if (!Qn)
                for (var Ut = t.child; Ut !== null; ) {
                  var Hn = Jh(Ut);
                  if (Hn !== null) {
                    qt = !0, t.flags |= Ie, Dp(Xe, !1);
                    var ca = Hn.updateQueue;
                    return ca !== null && (t.updateQueue = ca, t.flags |= et), t.subtreeFlags = Le, _x(t, a), jo(t, Tg(el.current, mp)), t.child;
                  }
                  Ut = Ut.sibling;
                }
              Xe.tail !== null && gn() > JC() && (t.flags |= Ie, qt = !0, Dp(Xe, !1), t.lanes = Av);
            }
          else {
            if (!qt) {
              var Pr = Jh(zt);
              if (Pr !== null) {
                t.flags |= Ie, qt = !0;
                var ci = Pr.updateQueue;
                if (ci !== null && (t.updateQueue = ci, t.flags |= et), Dp(Xe, !0), Xe.tail === null && Xe.tailMode === "hidden" && !zt.alternate && !zr())
                  return Ar(t), null;
              } else
                // The time it took to render last row is greater than the remaining
                // time we have to render. So rendering one more row would likely
                // exceed it.
                gn() * 2 - Xe.renderingStartTime > JC() && a !== Rr && (t.flags |= Ie, qt = !0, Dp(Xe, !1), t.lanes = Av);
            }
            if (Xe.isBackwards)
              zt.sibling = t.child, t.child = zt;
            else {
              var ba = Xe.last;
              ba !== null ? ba.sibling = zt : t.child = zt, Xe.last = zt;
            }
          }
          if (Xe.tail !== null) {
            var _a = Xe.tail;
            Xe.rendering = _a, Xe.tail = _a.sibling, Xe.renderingStartTime = gn(), _a.sibling = null;
            var fa = el.current;
            return qt ? fa = Tg(fa, mp) : fa = kf(fa), jo(t, fa), _a;
          }
          return Ar(t), null;
        }
        case Cn:
          break;
        case ze:
        case Je: {
          $S(t);
          var Mu = t.memoizedState, Bf = Mu !== null;
          if (e !== null) {
            var Ip = e.memoizedState, Il = Ip !== null;
            Il !== Bf && // LegacyHidden doesn't do any hiding — it only pre-renders.
            !ae && (t.flags |= wl);
          }
          return !Bf || (t.mode & xe) === Ce ? Ar(t) : ia(Yl, Rr) && (Ar(t), t.subtreeFlags & (ln | et) && (t.flags |= wl)), null;
        }
        case Ft:
          return null;
        case _t:
          return null;
      }
      throw new Error("Unknown unit of work tag (" + t.tag + "). This error is likely caused by a bug in React. Please file an issue.");
    }
    function jw(e, t, a) {
      switch (Zy(t), t.tag) {
        case se: {
          var i = t.type;
          jl(i) && Lh(t);
          var u = t.flags;
          return u & Zn ? (t.flags = u & ~Zn | Ie, (t.mode & Qe) !== Ce && Xg(t), t) : null;
        }
        case re: {
          t.stateNode, _f(t), Gy(t), wg();
          var s = t.flags;
          return (s & Zn) !== Le && (s & Ie) === Le ? (t.flags = s & ~Zn | Ie, t) : null;
        }
        case ue:
          return Cg(t), null;
        case Oe: {
          Df(t);
          var f = t.memoizedState;
          if (f !== null && f.dehydrated !== null) {
            if (t.alternate === null)
              throw new Error("Threw in newly mounted dehydrated component. This is likely a bug in React. Please file an issue.");
            Tf();
          }
          var p = t.flags;
          return p & Zn ? (t.flags = p & ~Zn | Ie, (t.mode & Qe) !== Ce && Xg(t), t) : null;
        }
        case Ot:
          return Df(t), null;
        case pe:
          return _f(t), null;
        case ot:
          var v = t.type._context;
          return dg(v, t), null;
        case ze:
        case Je:
          return $S(t), null;
        case Ft:
          return null;
        default:
          return null;
      }
    }
    function NC(e, t, a) {
      switch (Zy(t), t.tag) {
        case se: {
          var i = t.type.childContextTypes;
          i != null && Lh(t);
          break;
        }
        case re: {
          t.stateNode, _f(t), Gy(t), wg();
          break;
        }
        case ue: {
          Cg(t);
          break;
        }
        case pe:
          _f(t);
          break;
        case Oe:
          Df(t);
          break;
        case Ot:
          Df(t);
          break;
        case ot:
          var u = t.type._context;
          dg(u, t);
          break;
        case ze:
        case Je:
          $S(t);
          break;
      }
    }
    var zC = null;
    zC = /* @__PURE__ */ new Set();
    var Tm = !1, jr = !1, Fw = typeof WeakSet == "function" ? WeakSet : Set, Se = null, Uf = null, Af = null;
    function Hw(e) {
      ru(null, function() {
        throw e;
      }), dd();
    }
    var Vw = function(e, t) {
      if (t.props = e.memoizedProps, t.state = e.memoizedState, e.mode & Qe)
        try {
          Bl(), t.componentWillUnmount();
        } finally {
          Pl(e);
        }
      else
        t.componentWillUnmount();
    };
    function UC(e, t) {
      try {
        Vo(or, e);
      } catch (a) {
        sn(e, t, a);
      }
    }
    function _S(e, t, a) {
      try {
        Vw(e, a);
      } catch (i) {
        sn(e, t, i);
      }
    }
    function Pw(e, t, a) {
      try {
        a.componentDidMount();
      } catch (i) {
        sn(e, t, i);
      }
    }
    function AC(e, t) {
      try {
        FC(e);
      } catch (a) {
        sn(e, t, a);
      }
    }
    function jf(e, t) {
      var a = e.ref;
      if (a !== null)
        if (typeof a == "function") {
          var i;
          try {
            if (tt && St && e.mode & Qe)
              try {
                Bl(), i = a(null);
              } finally {
                Pl(e);
              }
            else
              i = a(null);
          } catch (u) {
            sn(e, t, u);
          }
          typeof i == "function" && S("Unexpected return value from a callback ref in %s. A callback ref should not return a function.", We(e));
        } else
          a.current = null;
    }
    function xm(e, t, a) {
      try {
        a();
      } catch (i) {
        sn(e, t, i);
      }
    }
    var jC = !1;
    function Bw(e, t) {
      eT(e.containerInfo), Se = t, $w();
      var a = jC;
      return jC = !1, a;
    }
    function $w() {
      for (; Se !== null; ) {
        var e = Se, t = e.child;
        (e.subtreeFlags & Zu) !== Le && t !== null ? (t.return = e, Se = t) : Yw();
      }
    }
    function Yw() {
      for (; Se !== null; ) {
        var e = Se;
        Bt(e);
        try {
          Iw(e);
        } catch (a) {
          sn(e, e.return, a);
        }
        Rn();
        var t = e.sibling;
        if (t !== null) {
          t.return = e.return, Se = t;
          return;
        }
        Se = e.return;
      }
    }
    function Iw(e) {
      var t = e.alternate, a = e.flags;
      if ((a & za) !== Le) {
        switch (Bt(e), e.tag) {
          case de:
          case qe:
          case Ve:
            break;
          case se: {
            if (t !== null) {
              var i = t.memoizedProps, u = t.memoizedState, s = e.stateNode;
              e.type === e.elementType && !Qs && (s.props !== e.memoizedProps && S("Expected %s props to match memoized props before getSnapshotBeforeUpdate. This might either be because of a bug in React, or because a component reassigns its own `this.props`. Please file an issue.", We(e) || "instance"), s.state !== e.memoizedState && S("Expected %s state to match memoized state before getSnapshotBeforeUpdate. This might either be because of a bug in React, or because a component reassigns its own `this.state`. Please file an issue.", We(e) || "instance"));
              var f = s.getSnapshotBeforeUpdate(e.elementType === e.type ? i : nl(e.type, i), u);
              {
                var p = zC;
                f === void 0 && !p.has(e.type) && (p.add(e.type), S("%s.getSnapshotBeforeUpdate(): A snapshot value (or null) must be returned. You have returned undefined.", We(e)));
              }
              s.__reactInternalSnapshotBeforeUpdate = f;
            }
            break;
          }
          case re: {
            {
              var v = e.stateNode;
              wT(v.containerInfo);
            }
            break;
          }
          case ue:
          case Ye:
          case pe:
          case _n:
            break;
          default:
            throw new Error("This unit of work tag should not have side-effects. This error is likely caused by a bug in React. Please file an issue.");
        }
        Rn();
      }
    }
    function al(e, t, a) {
      var i = t.updateQueue, u = i !== null ? i.lastEffect : null;
      if (u !== null) {
        var s = u.next, f = s;
        do {
          if ((f.tag & e) === e) {
            var p = f.destroy;
            f.destroy = void 0, p !== void 0 && ((e & Ur) !== Ga ? Nv(t) : (e & or) !== Ga && ui(t), (e & Fl) !== Ga && Bp(!0), xm(t, a, p), (e & Fl) !== Ga && Bp(!1), (e & Ur) !== Ga ? Rc() : (e & or) !== Ga && no());
          }
          f = f.next;
        } while (f !== s);
      }
    }
    function Vo(e, t) {
      var a = t.updateQueue, i = a !== null ? a.lastEffect : null;
      if (i !== null) {
        var u = i.next, s = u;
        do {
          if ((s.tag & e) === e) {
            (e & Ur) !== Ga ? kl(t) : (e & or) !== Ga && zv(t);
            var f = s.create;
            (e & Fl) !== Ga && Bp(!0), s.destroy = f(), (e & Fl) !== Ga && Bp(!1), (e & Ur) !== Ga ? Cc() : (e & or) !== Ga && ds();
            {
              var p = s.destroy;
              if (p !== void 0 && typeof p != "function") {
                var v = void 0;
                (s.tag & or) !== Le ? v = "useLayoutEffect" : (s.tag & Fl) !== Le ? v = "useInsertionEffect" : v = "useEffect";
                var y = void 0;
                p === null ? y = " You returned null. If your effect does not require clean up, return undefined (or nothing)." : typeof p.then == "function" ? y = `

It looks like you wrote ` + v + `(async () => ...) or returned a Promise. Instead, write the async function inside your effect and call it immediately:

` + v + `(() => {
  async function fetchData() {
    // You can await here
    const response = await MyAPI.getData(someId);
    // ...
  }
  fetchData();
}, [someId]); // Or [] if effect doesn't need props or state

Learn more about data fetching with Hooks: https://reactjs.org/link/hooks-data-fetching` : y = " You returned: " + p, S("%s must not return anything besides a function, which is used for clean-up.%s", v, y);
              }
            }
          }
          s = s.next;
        } while (s !== u);
      }
    }
    function Qw(e, t) {
      if ((t.flags & et) !== Le)
        switch (t.tag) {
          case mt: {
            var a = t.stateNode.passiveEffectDuration, i = t.memoizedProps, u = i.id, s = i.onPostCommit, f = JE(), p = t.alternate === null ? "mount" : "update";
            ZE() && (p = "nested-update"), typeof s == "function" && s(u, p, a, f);
            var v = t.return;
            e:
              for (; v !== null; ) {
                switch (v.tag) {
                  case re:
                    var y = v.stateNode;
                    y.passiveEffectDuration += a;
                    break e;
                  case mt:
                    var g = v.stateNode;
                    g.passiveEffectDuration += a;
                    break e;
                }
                v = v.return;
              }
            break;
          }
        }
    }
    function Ww(e, t, a, i) {
      if ((a.flags & Er) !== Le)
        switch (a.tag) {
          case de:
          case qe:
          case Ve: {
            if (!jr)
              if (a.mode & Qe)
                try {
                  Bl(), Vo(or | ur, a);
                } finally {
                  Pl(a);
                }
              else
                Vo(or | ur, a);
            break;
          }
          case se: {
            var u = a.stateNode;
            if (a.flags & et && !jr)
              if (t === null)
                if (a.type === a.elementType && !Qs && (u.props !== a.memoizedProps && S("Expected %s props to match memoized props before componentDidMount. This might either be because of a bug in React, or because a component reassigns its own `this.props`. Please file an issue.", We(a) || "instance"), u.state !== a.memoizedState && S("Expected %s state to match memoized state before componentDidMount. This might either be because of a bug in React, or because a component reassigns its own `this.state`. Please file an issue.", We(a) || "instance")), a.mode & Qe)
                  try {
                    Bl(), u.componentDidMount();
                  } finally {
                    Pl(a);
                  }
                else
                  u.componentDidMount();
              else {
                var s = a.elementType === a.type ? t.memoizedProps : nl(a.type, t.memoizedProps), f = t.memoizedState;
                if (a.type === a.elementType && !Qs && (u.props !== a.memoizedProps && S("Expected %s props to match memoized props before componentDidUpdate. This might either be because of a bug in React, or because a component reassigns its own `this.props`. Please file an issue.", We(a) || "instance"), u.state !== a.memoizedState && S("Expected %s state to match memoized state before componentDidUpdate. This might either be because of a bug in React, or because a component reassigns its own `this.state`. Please file an issue.", We(a) || "instance")), a.mode & Qe)
                  try {
                    Bl(), u.componentDidUpdate(s, f, u.__reactInternalSnapshotBeforeUpdate);
                  } finally {
                    Pl(a);
                  }
                else
                  u.componentDidUpdate(s, f, u.__reactInternalSnapshotBeforeUpdate);
              }
            var p = a.updateQueue;
            p !== null && (a.type === a.elementType && !Qs && (u.props !== a.memoizedProps && S("Expected %s props to match memoized props before processing the update queue. This might either be because of a bug in React, or because a component reassigns its own `this.props`. Please file an issue.", We(a) || "instance"), u.state !== a.memoizedState && S("Expected %s state to match memoized state before processing the update queue. This might either be because of a bug in React, or because a component reassigns its own `this.state`. Please file an issue.", We(a) || "instance")), TE(a, p, u));
            break;
          }
          case re: {
            var v = a.updateQueue;
            if (v !== null) {
              var y = null;
              if (a.child !== null)
                switch (a.child.tag) {
                  case ue:
                    y = a.child.stateNode;
                    break;
                  case se:
                    y = a.child.stateNode;
                    break;
                }
              TE(a, v, y);
            }
            break;
          }
          case ue: {
            var g = a.stateNode;
            if (t === null && a.flags & et) {
              var b = a.type, x = a.memoizedProps;
              fT(g, b, x);
            }
            break;
          }
          case Ye:
            break;
          case pe:
            break;
          case mt: {
            {
              var N = a.memoizedProps, A = N.onCommit, F = N.onRender, le = a.stateNode.effectDuration, Me = JE(), we = t === null ? "mount" : "update";
              ZE() && (we = "nested-update"), typeof F == "function" && F(a.memoizedProps.id, we, a.actualDuration, a.treeBaseDuration, a.actualStartTime, Me);
              {
                typeof A == "function" && A(a.memoizedProps.id, we, le, Me), Yb(a);
                var wt = a.return;
                e:
                  for (; wt !== null; ) {
                    switch (wt.tag) {
                      case re:
                        var gt = wt.stateNode;
                        gt.effectDuration += le;
                        break e;
                      case mt:
                        var O = wt.stateNode;
                        O.effectDuration += le;
                        break e;
                    }
                    wt = wt.return;
                  }
              }
            }
            break;
          }
          case Oe: {
            tb(e, a);
            break;
          }
          case Ot:
          case _n:
          case Cn:
          case ze:
          case Je:
          case _t:
            break;
          default:
            throw new Error("This unit of work tag should not have side-effects. This error is likely caused by a bug in React. Please file an issue.");
        }
      jr || a.flags & Kr && FC(a);
    }
    function Gw(e) {
      switch (e.tag) {
        case de:
        case qe:
        case Ve: {
          if (e.mode & Qe)
            try {
              Bl(), UC(e, e.return);
            } finally {
              Pl(e);
            }
          else
            UC(e, e.return);
          break;
        }
        case se: {
          var t = e.stateNode;
          typeof t.componentDidMount == "function" && Pw(e, e.return, t), AC(e, e.return);
          break;
        }
        case ue: {
          AC(e, e.return);
          break;
        }
      }
    }
    function qw(e, t) {
      for (var a = null, i = e; ; ) {
        if (i.tag === ue) {
          if (a === null) {
            a = i;
            try {
              var u = i.stateNode;
              t ? CT(u) : TT(i.stateNode, i.memoizedProps);
            } catch (f) {
              sn(e, e.return, f);
            }
          }
        } else if (i.tag === Ye) {
          if (a === null)
            try {
              var s = i.stateNode;
              t ? RT(s) : xT(s, i.memoizedProps);
            } catch (f) {
              sn(e, e.return, f);
            }
        } else if (!((i.tag === ze || i.tag === Je) && i.memoizedState !== null && i !== e)) {
          if (i.child !== null) {
            i.child.return = i, i = i.child;
            continue;
          }
        }
        if (i === e)
          return;
        for (; i.sibling === null; ) {
          if (i.return === null || i.return === e)
            return;
          a === i && (a = null), i = i.return;
        }
        a === i && (a = null), i.sibling.return = i.return, i = i.sibling;
      }
    }
    function FC(e) {
      var t = e.ref;
      if (t !== null) {
        var a = e.stateNode, i;
        switch (e.tag) {
          case ue:
            i = a;
            break;
          default:
            i = a;
        }
        if (typeof t == "function") {
          var u;
          if (e.mode & Qe)
            try {
              Bl(), u = t(i);
            } finally {
              Pl(e);
            }
          else
            u = t(i);
          typeof u == "function" && S("Unexpected return value from a callback ref in %s. A callback ref should not return a function.", We(e));
        } else
          t.hasOwnProperty("current") || S("Unexpected ref object provided for %s. Use either a ref-setter function or React.createRef().", We(e)), t.current = i;
      }
    }
    function Xw(e) {
      var t = e.alternate;
      t !== null && (t.return = null), e.return = null;
    }
    function HC(e) {
      var t = e.alternate;
      t !== null && (e.alternate = null, HC(t));
      {
        if (e.child = null, e.deletions = null, e.sibling = null, e.tag === ue) {
          var a = e.stateNode;
          a !== null && nx(a);
        }
        e.stateNode = null, e._debugOwner = null, e.return = null, e.dependencies = null, e.memoizedProps = null, e.memoizedState = null, e.pendingProps = null, e.stateNode = null, e.updateQueue = null;
      }
    }
    function Kw(e) {
      for (var t = e.return; t !== null; ) {
        if (VC(t))
          return t;
        t = t.return;
      }
      throw new Error("Expected to find a host parent. This error is likely caused by a bug in React. Please file an issue.");
    }
    function VC(e) {
      return e.tag === ue || e.tag === re || e.tag === pe;
    }
    function PC(e) {
      var t = e;
      e:
        for (; ; ) {
          for (; t.sibling === null; ) {
            if (t.return === null || VC(t.return))
              return null;
            t = t.return;
          }
          for (t.sibling.return = t.return, t = t.sibling; t.tag !== ue && t.tag !== Ye && t.tag !== Wt; ) {
            if (t.flags & ln || t.child === null || t.tag === pe)
              continue e;
            t.child.return = t, t = t.child;
          }
          if (!(t.flags & ln))
            return t.stateNode;
        }
    }
    function Zw(e) {
      var t = Kw(e);
      switch (t.tag) {
        case ue: {
          var a = t.stateNode;
          t.flags & $t && ($0(a), t.flags &= ~$t);
          var i = PC(e);
          DS(e, i, a);
          break;
        }
        case re:
        case pe: {
          var u = t.stateNode.containerInfo, s = PC(e);
          kS(e, s, u);
          break;
        }
        default:
          throw new Error("Invalid host parent fiber. This error is likely caused by a bug in React. Please file an issue.");
      }
    }
    function kS(e, t, a) {
      var i = e.tag, u = i === ue || i === Ye;
      if (u) {
        var s = e.stateNode;
        t ? yT(a, s, t) : hT(a, s);
      } else if (i !== pe) {
        var f = e.child;
        if (f !== null) {
          kS(f, t, a);
          for (var p = f.sibling; p !== null; )
            kS(p, t, a), p = p.sibling;
        }
      }
    }
    function DS(e, t, a) {
      var i = e.tag, u = i === ue || i === Ye;
      if (u) {
        var s = e.stateNode;
        t ? mT(a, s, t) : vT(a, s);
      } else if (i !== pe) {
        var f = e.child;
        if (f !== null) {
          DS(f, t, a);
          for (var p = f.sibling; p !== null; )
            DS(p, t, a), p = p.sibling;
        }
      }
    }
    var Fr = null, il = !1;
    function Jw(e, t, a) {
      {
        var i = t;
        e:
          for (; i !== null; ) {
            switch (i.tag) {
              case ue: {
                Fr = i.stateNode, il = !1;
                break e;
              }
              case re: {
                Fr = i.stateNode.containerInfo, il = !0;
                break e;
              }
              case pe: {
                Fr = i.stateNode.containerInfo, il = !0;
                break e;
              }
            }
            i = i.return;
          }
        if (Fr === null)
          throw new Error("Expected to find a host parent. This error is likely caused by a bug in React. Please file an issue.");
        BC(e, t, a), Fr = null, il = !1;
      }
      Xw(a);
    }
    function Po(e, t, a) {
      for (var i = a.child; i !== null; )
        BC(e, t, i), i = i.sibling;
    }
    function BC(e, t, a) {
      switch (lu(a), a.tag) {
        case ue:
          jr || jf(a, t);
        case Ye: {
          {
            var i = Fr, u = il;
            Fr = null, Po(e, t, a), Fr = i, il = u, Fr !== null && (il ? ST(Fr, a.stateNode) : gT(Fr, a.stateNode));
          }
          return;
        }
        case Wt: {
          Fr !== null && (il ? ET(Fr, a.stateNode) : Vy(Fr, a.stateNode));
          return;
        }
        case pe: {
          {
            var s = Fr, f = il;
            Fr = a.stateNode.containerInfo, il = !0, Po(e, t, a), Fr = s, il = f;
          }
          return;
        }
        case de:
        case qe:
        case ft:
        case Ve: {
          if (!jr) {
            var p = a.updateQueue;
            if (p !== null) {
              var v = p.lastEffect;
              if (v !== null) {
                var y = v.next, g = y;
                do {
                  var b = g, x = b.destroy, N = b.tag;
                  x !== void 0 && ((N & Fl) !== Ga ? xm(a, t, x) : (N & or) !== Ga && (ui(a), a.mode & Qe ? (Bl(), xm(a, t, x), Pl(a)) : xm(a, t, x), no())), g = g.next;
                } while (g !== y);
              }
            }
          }
          Po(e, t, a);
          return;
        }
        case se: {
          if (!jr) {
            jf(a, t);
            var A = a.stateNode;
            typeof A.componentWillUnmount == "function" && _S(a, t, A);
          }
          Po(e, t, a);
          return;
        }
        case Cn: {
          Po(e, t, a);
          return;
        }
        case ze: {
          if (
            // TODO: Remove this dead flag
            a.mode & xe
          ) {
            var F = jr;
            jr = F || a.memoizedState !== null, Po(e, t, a), jr = F;
          } else
            Po(e, t, a);
          break;
        }
        default: {
          Po(e, t, a);
          return;
        }
      }
    }
    function eb(e) {
      e.memoizedState;
    }
    function tb(e, t) {
      var a = t.memoizedState;
      if (a === null) {
        var i = t.alternate;
        if (i !== null) {
          var u = i.memoizedState;
          if (u !== null) {
            var s = u.dehydrated;
            s !== null && HT(s);
          }
        }
      }
    }
    function $C(e) {
      var t = e.updateQueue;
      if (t !== null) {
        e.updateQueue = null;
        var a = e.stateNode;
        a === null && (a = e.stateNode = new Fw()), t.forEach(function(i) {
          var u = Kb.bind(null, e, i);
          if (!a.has(i)) {
            if (a.add(i), Ea)
              if (Uf !== null && Af !== null)
                Pp(Af, Uf);
              else
                throw Error("Expected finished root and lanes to be set. This is a bug in React.");
            i.then(u, u);
          }
        });
      }
    }
    function nb(e, t, a) {
      Uf = a, Af = e, Bt(t), YC(t, e), Bt(t), Uf = null, Af = null;
    }
    function ll(e, t, a) {
      var i = t.deletions;
      if (i !== null)
        for (var u = 0; u < i.length; u++) {
          var s = i[u];
          try {
            Jw(e, t, s);
          } catch (v) {
            sn(s, t, v);
          }
        }
      var f = Js();
      if (t.subtreeFlags & ea)
        for (var p = t.child; p !== null; )
          Bt(p), YC(p, e), p = p.sibling;
      Bt(f);
    }
    function YC(e, t, a) {
      var i = e.alternate, u = e.flags;
      switch (e.tag) {
        case de:
        case qe:
        case ft:
        case Ve: {
          if (ll(t, e), $l(e), u & et) {
            try {
              al(Fl | ur, e, e.return), Vo(Fl | ur, e);
            } catch (Be) {
              sn(e, e.return, Be);
            }
            if (e.mode & Qe) {
              try {
                Bl(), al(or | ur, e, e.return);
              } catch (Be) {
                sn(e, e.return, Be);
              }
              Pl(e);
            } else
              try {
                al(or | ur, e, e.return);
              } catch (Be) {
                sn(e, e.return, Be);
              }
          }
          return;
        }
        case se: {
          ll(t, e), $l(e), u & Kr && i !== null && jf(i, i.return);
          return;
        }
        case ue: {
          ll(t, e), $l(e), u & Kr && i !== null && jf(i, i.return);
          {
            if (e.flags & $t) {
              var s = e.stateNode;
              try {
                $0(s);
              } catch (Be) {
                sn(e, e.return, Be);
              }
            }
            if (u & et) {
              var f = e.stateNode;
              if (f != null) {
                var p = e.memoizedProps, v = i !== null ? i.memoizedProps : p, y = e.type, g = e.updateQueue;
                if (e.updateQueue = null, g !== null)
                  try {
                    dT(f, g, y, v, p, e);
                  } catch (Be) {
                    sn(e, e.return, Be);
                  }
              }
            }
          }
          return;
        }
        case Ye: {
          if (ll(t, e), $l(e), u & et) {
            if (e.stateNode === null)
              throw new Error("This should have a text node initialized. This error is likely caused by a bug in React. Please file an issue.");
            var b = e.stateNode, x = e.memoizedProps, N = i !== null ? i.memoizedProps : x;
            try {
              pT(b, N, x);
            } catch (Be) {
              sn(e, e.return, Be);
            }
          }
          return;
        }
        case re: {
          if (ll(t, e), $l(e), u & et && i !== null) {
            var A = i.memoizedState;
            if (A.isDehydrated)
              try {
                FT(t.containerInfo);
              } catch (Be) {
                sn(e, e.return, Be);
              }
          }
          return;
        }
        case pe: {
          ll(t, e), $l(e);
          return;
        }
        case Oe: {
          ll(t, e), $l(e);
          var F = e.child;
          if (F.flags & wl) {
            var le = F.stateNode, Me = F.memoizedState, we = Me !== null;
            if (le.isHidden = we, we) {
              var wt = F.alternate !== null && F.alternate.memoizedState !== null;
              wt || Ab();
            }
          }
          if (u & et) {
            try {
              eb(e);
            } catch (Be) {
              sn(e, e.return, Be);
            }
            $C(e);
          }
          return;
        }
        case ze: {
          var gt = i !== null && i.memoizedState !== null;
          if (
            // TODO: Remove this dead flag
            e.mode & xe
          ) {
            var O = jr;
            jr = O || gt, ll(t, e), jr = O;
          } else
            ll(t, e);
          if ($l(e), u & wl) {
            var H = e.stateNode, L = e.memoizedState, X = L !== null, ve = e;
            if (H.isHidden = X, X && !gt && (ve.mode & xe) !== Ce) {
              Se = ve;
              for (var oe = ve.child; oe !== null; )
                Se = oe, ab(oe), oe = oe.sibling;
            }
            qw(ve, X);
          }
          return;
        }
        case Ot: {
          ll(t, e), $l(e), u & et && $C(e);
          return;
        }
        case Cn:
          return;
        default: {
          ll(t, e), $l(e);
          return;
        }
      }
    }
    function $l(e) {
      var t = e.flags;
      if (t & ln) {
        try {
          Zw(e);
        } catch (a) {
          sn(e, e.return, a);
        }
        e.flags &= ~ln;
      }
      t & Ua && (e.flags &= ~Ua);
    }
    function rb(e, t, a) {
      Uf = a, Af = t, Se = e, IC(e, t, a), Uf = null, Af = null;
    }
    function IC(e, t, a) {
      for (var i = (e.mode & xe) !== Ce; Se !== null; ) {
        var u = Se, s = u.child;
        if (u.tag === ze && i) {
          var f = u.memoizedState !== null, p = f || Tm;
          if (p) {
            OS(e, t, a);
            continue;
          } else {
            var v = u.alternate, y = v !== null && v.memoizedState !== null, g = y || jr, b = Tm, x = jr;
            Tm = p, jr = g, jr && !x && (Se = u, ib(u));
            for (var N = s; N !== null; )
              Se = N, IC(
                N,
                // New root; bubble back up to here and stop.
                t,
                a
              ), N = N.sibling;
            Se = u, Tm = b, jr = x, OS(e, t, a);
            continue;
          }
        }
        (u.subtreeFlags & Er) !== Le && s !== null ? (s.return = u, Se = s) : OS(e, t, a);
      }
    }
    function OS(e, t, a) {
      for (; Se !== null; ) {
        var i = Se;
        if ((i.flags & Er) !== Le) {
          var u = i.alternate;
          Bt(i);
          try {
            Ww(t, u, i, a);
          } catch (f) {
            sn(i, i.return, f);
          }
          Rn();
        }
        if (i === e) {
          Se = null;
          return;
        }
        var s = i.sibling;
        if (s !== null) {
          s.return = i.return, Se = s;
          return;
        }
        Se = i.return;
      }
    }
    function ab(e) {
      for (; Se !== null; ) {
        var t = Se, a = t.child;
        switch (t.tag) {
          case de:
          case qe:
          case ft:
          case Ve: {
            if (t.mode & Qe)
              try {
                Bl(), al(or, t, t.return);
              } finally {
                Pl(t);
              }
            else
              al(or, t, t.return);
            break;
          }
          case se: {
            jf(t, t.return);
            var i = t.stateNode;
            typeof i.componentWillUnmount == "function" && _S(t, t.return, i);
            break;
          }
          case ue: {
            jf(t, t.return);
            break;
          }
          case ze: {
            var u = t.memoizedState !== null;
            if (u) {
              QC(e);
              continue;
            }
            break;
          }
        }
        a !== null ? (a.return = t, Se = a) : QC(e);
      }
    }
    function QC(e) {
      for (; Se !== null; ) {
        var t = Se;
        if (t === e) {
          Se = null;
          return;
        }
        var a = t.sibling;
        if (a !== null) {
          a.return = t.return, Se = a;
          return;
        }
        Se = t.return;
      }
    }
    function ib(e) {
      for (; Se !== null; ) {
        var t = Se, a = t.child;
        if (t.tag === ze) {
          var i = t.memoizedState !== null;
          if (i) {
            WC(e);
            continue;
          }
        }
        a !== null ? (a.return = t, Se = a) : WC(e);
      }
    }
    function WC(e) {
      for (; Se !== null; ) {
        var t = Se;
        Bt(t);
        try {
          Gw(t);
        } catch (i) {
          sn(t, t.return, i);
        }
        if (Rn(), t === e) {
          Se = null;
          return;
        }
        var a = t.sibling;
        if (a !== null) {
          a.return = t.return, Se = a;
          return;
        }
        Se = t.return;
      }
    }
    function lb(e, t, a, i) {
      Se = t, ub(t, e, a, i);
    }
    function ub(e, t, a, i) {
      for (; Se !== null; ) {
        var u = Se, s = u.child;
        (u.subtreeFlags & Aa) !== Le && s !== null ? (s.return = u, Se = s) : ob(e, t, a, i);
      }
    }
    function ob(e, t, a, i) {
      for (; Se !== null; ) {
        var u = Se;
        if ((u.flags & cn) !== Le) {
          Bt(u);
          try {
            sb(t, u, a, i);
          } catch (f) {
            sn(u, u.return, f);
          }
          Rn();
        }
        if (u === e) {
          Se = null;
          return;
        }
        var s = u.sibling;
        if (s !== null) {
          s.return = u.return, Se = s;
          return;
        }
        Se = u.return;
      }
    }
    function sb(e, t, a, i) {
      switch (t.tag) {
        case de:
        case qe:
        case Ve: {
          if (t.mode & Qe) {
            qg();
            try {
              Vo(Ur | ur, t);
            } finally {
              Gg(t);
            }
          } else
            Vo(Ur | ur, t);
          break;
        }
      }
    }
    function cb(e) {
      Se = e, fb();
    }
    function fb() {
      for (; Se !== null; ) {
        var e = Se, t = e.child;
        if ((Se.flags & jt) !== Le) {
          var a = e.deletions;
          if (a !== null) {
            for (var i = 0; i < a.length; i++) {
              var u = a[i];
              Se = u, vb(u, e);
            }
            {
              var s = e.alternate;
              if (s !== null) {
                var f = s.child;
                if (f !== null) {
                  s.child = null;
                  do {
                    var p = f.sibling;
                    f.sibling = null, f = p;
                  } while (f !== null);
                }
              }
            }
            Se = e;
          }
        }
        (e.subtreeFlags & Aa) !== Le && t !== null ? (t.return = e, Se = t) : db();
      }
    }
    function db() {
      for (; Se !== null; ) {
        var e = Se;
        (e.flags & cn) !== Le && (Bt(e), pb(e), Rn());
        var t = e.sibling;
        if (t !== null) {
          t.return = e.return, Se = t;
          return;
        }
        Se = e.return;
      }
    }
    function pb(e) {
      switch (e.tag) {
        case de:
        case qe:
        case Ve: {
          e.mode & Qe ? (qg(), al(Ur | ur, e, e.return), Gg(e)) : al(Ur | ur, e, e.return);
          break;
        }
      }
    }
    function vb(e, t) {
      for (; Se !== null; ) {
        var a = Se;
        Bt(a), mb(a, t), Rn();
        var i = a.child;
        i !== null ? (i.return = a, Se = i) : hb(e);
      }
    }
    function hb(e) {
      for (; Se !== null; ) {
        var t = Se, a = t.sibling, i = t.return;
        if (HC(t), t === e) {
          Se = null;
          return;
        }
        if (a !== null) {
          a.return = i, Se = a;
          return;
        }
        Se = i;
      }
    }
    function mb(e, t) {
      switch (e.tag) {
        case de:
        case qe:
        case Ve: {
          e.mode & Qe ? (qg(), al(Ur, e, t), Gg(e)) : al(Ur, e, t);
          break;
        }
      }
    }
    function yb(e) {
      switch (e.tag) {
        case de:
        case qe:
        case Ve: {
          try {
            Vo(or | ur, e);
          } catch (a) {
            sn(e, e.return, a);
          }
          break;
        }
        case se: {
          var t = e.stateNode;
          try {
            t.componentDidMount();
          } catch (a) {
            sn(e, e.return, a);
          }
          break;
        }
      }
    }
    function gb(e) {
      switch (e.tag) {
        case de:
        case qe:
        case Ve: {
          try {
            Vo(Ur | ur, e);
          } catch (t) {
            sn(e, e.return, t);
          }
          break;
        }
      }
    }
    function Sb(e) {
      switch (e.tag) {
        case de:
        case qe:
        case Ve: {
          try {
            al(or | ur, e, e.return);
          } catch (a) {
            sn(e, e.return, a);
          }
          break;
        }
        case se: {
          var t = e.stateNode;
          typeof t.componentWillUnmount == "function" && _S(e, e.return, t);
          break;
        }
      }
    }
    function Eb(e) {
      switch (e.tag) {
        case de:
        case qe:
        case Ve:
          try {
            al(Ur | ur, e, e.return);
          } catch (t) {
            sn(e, e.return, t);
          }
      }
    }
    if (typeof Symbol == "function" && Symbol.for) {
      var Op = Symbol.for;
      Op("selector.component"), Op("selector.has_pseudo_class"), Op("selector.role"), Op("selector.test_id"), Op("selector.text");
    }
    var Cb = [];
    function Rb() {
      Cb.forEach(function(e) {
        return e();
      });
    }
    var Tb = k.ReactCurrentActQueue;
    function xb(e) {
      {
        var t = (
          // $FlowExpectedError – Flow doesn't know about IS_REACT_ACT_ENVIRONMENT global
          typeof IS_REACT_ACT_ENVIRONMENT < "u" ? IS_REACT_ACT_ENVIRONMENT : void 0
        ), a = typeof jest < "u";
        return a && t !== !1;
      }
    }
    function GC() {
      {
        var e = (
          // $FlowExpectedError – Flow doesn't know about IS_REACT_ACT_ENVIRONMENT global
          typeof IS_REACT_ACT_ENVIRONMENT < "u" ? IS_REACT_ACT_ENVIRONMENT : void 0
        );
        return !e && Tb.current !== null && S("The current testing environment is not configured to support act(...)"), e;
      }
    }
    var wb = Math.ceil, LS = k.ReactCurrentDispatcher, MS = k.ReactCurrentOwner, Hr = k.ReactCurrentBatchConfig, ul = k.ReactCurrentActQueue, fr = (
      /*             */
      0
    ), qC = (
      /*               */
      1
    ), Vr = (
      /*                */
      2
    ), Oi = (
      /*                */
      4
    ), ku = 0, Lp = 1, Ws = 2, wm = 3, Mp = 4, XC = 5, NS = 6, xt = fr, xa = null, Nn = null, dr = $, Yl = $, zS = Lo($), pr = ku, Np = null, bm = $, zp = $, _m = $, Up = null, qa = null, US = 0, KC = 500, ZC = 1 / 0, bb = 500, Du = null;
    function Ap() {
      ZC = gn() + bb;
    }
    function JC() {
      return ZC;
    }
    var km = !1, AS = null, Ff = null, Gs = !1, Bo = null, jp = $, jS = [], FS = null, _b = 50, Fp = 0, HS = null, VS = !1, Dm = !1, kb = 50, Hf = 0, Om = null, Hp = nn, Lm = $, e1 = !1;
    function Mm() {
      return xa;
    }
    function wa() {
      return (xt & (Vr | Oi)) !== fr ? gn() : (Hp !== nn || (Hp = gn()), Hp);
    }
    function $o(e) {
      var t = e.mode;
      if ((t & xe) === Ce)
        return ke;
      if ((xt & Vr) !== fr && dr !== $)
        return fo(dr);
      var a = Tx() !== Rx;
      if (a) {
        if (Hr.transition !== null) {
          var i = Hr.transition;
          i._updatedFibers || (i._updatedFibers = /* @__PURE__ */ new Set()), i._updatedFibers.add(e);
        }
        return Lm === Fn && (Lm = Yv()), Lm;
      }
      var u = Pa();
      if (u !== Fn)
        return u;
      var s = uT();
      return s;
    }
    function Db(e) {
      var t = e.mode;
      return (t & xe) === Ce ? ke : aa();
    }
    function vr(e, t, a, i) {
      Jb(), e1 && S("useInsertionEffect must not schedule updates."), VS && (Dm = !0), vu(e, a, i), (xt & Vr) !== $ && e === xa ? n_(t) : (Ea && Ic(e, t, a), r_(t), e === xa && ((xt & Vr) === fr && (zp = Ke(zp, a)), pr === Mp && Yo(e, dr)), Xa(e, i), a === ke && xt === fr && (t.mode & xe) === Ce && // Treat `act` as if it's inside `batchedUpdates`, even in legacy mode.
      !ul.isBatchingLegacy && (Ap(), eE()));
    }
    function Ob(e, t, a) {
      var i = e.current;
      i.lanes = t, vu(e, t, a), Xa(e, a);
    }
    function Lb(e) {
      return (
        // TODO: Remove outdated deferRenderPhaseUpdateToNextBatch experiment. We
        // decided not to enable it.
        (xt & Vr) !== fr
      );
    }
    function Xa(e, t) {
      var a = e.callbackNode;
      Hv(e, t);
      var i = du(e, e === xa ? dr : $);
      if (i === $) {
        a !== null && m1(a), e.callbackNode = null, e.callbackPriority = Fn;
        return;
      }
      var u = On(i), s = e.callbackPriority;
      if (s === u && // Special case related to `act`. If the currently scheduled task is a
      // Scheduler task, rather than an `act` task, cancel it and re-scheduled
      // on the `act` queue.
      !(ul.current !== null && a !== WS)) {
        a == null && s !== ke && S("Expected scheduled callback to exist. This error is likely caused by a bug in React. Please file an issue.");
        return;
      }
      a != null && m1(a);
      var f;
      if (u === ke)
        e.tag === Mo ? (ul.isBatchingLegacy !== null && (ul.didScheduleLegacyUpdate = !0), ix(r1.bind(null, e))) : J0(r1.bind(null, e)), ul.current !== null ? ul.current.push(No) : sT(function() {
          (xt & (Vr | Oi)) === fr && No();
        }), f = null;
      else {
        var p;
        switch (lr(i)) {
          case Ln:
            p = gc;
            break;
          case Wi:
            p = iu;
            break;
          case Ci:
            p = Ei;
            break;
          case po:
            p = Sc;
            break;
          default:
            p = Ei;
            break;
        }
        f = GS(p, t1.bind(null, e));
      }
      e.callbackPriority = u, e.callbackNode = f;
    }
    function t1(e, t) {
      if (qx(), Hp = nn, Lm = $, (xt & (Vr | Oi)) !== fr)
        throw new Error("Should not already be working.");
      var a = e.callbackNode, i = Lu();
      if (i && e.callbackNode !== a)
        return null;
      var u = du(e, e === xa ? dr : $);
      if (u === $)
        return null;
      var s = !Es(e, u) && !$v(e, u) && !t, f = s ? Pb(e, u) : zm(e, u);
      if (f !== ku) {
        if (f === Ws) {
          var p = Ol(e);
          p !== $ && (u = p, f = PS(e, p));
        }
        if (f === Lp) {
          var v = Np;
          throw qs(e, $), Yo(e, u), Xa(e, gn()), v;
        }
        if (f === NS)
          Yo(e, u);
        else {
          var y = !Es(e, u), g = e.current.alternate;
          if (y && !Nb(g)) {
            if (f = zm(e, u), f === Ws) {
              var b = Ol(e);
              b !== $ && (u = b, f = PS(e, b));
            }
            if (f === Lp) {
              var x = Np;
              throw qs(e, $), Yo(e, u), Xa(e, gn()), x;
            }
          }
          e.finishedWork = g, e.finishedLanes = u, Mb(e, f, u);
        }
      }
      return Xa(e, gn()), e.callbackNode === a ? t1.bind(null, e) : null;
    }
    function PS(e, t) {
      var a = Up;
      if (Qc(e)) {
        var i = qs(e, t);
        i.flags |= Tn, ZT(e.containerInfo);
      }
      var u = zm(e, t);
      if (u !== Ws) {
        var s = qa;
        qa = a, s !== null && n1(s);
      }
      return u;
    }
    function n1(e) {
      qa === null ? qa = e : qa.push.apply(qa, e);
    }
    function Mb(e, t, a) {
      switch (t) {
        case ku:
        case Lp:
          throw new Error("Root did not complete. This is a bug in React.");
        case Ws: {
          Xs(e, qa, Du);
          break;
        }
        case wm: {
          if (Yo(e, a), Vv(a) && // do not delay if we're inside an act() scope
          !y1()) {
            var i = US + KC - gn();
            if (i > 10) {
              var u = du(e, $);
              if (u !== $)
                break;
              var s = e.suspendedLanes;
              if (!pu(s, a)) {
                wa(), $c(e, s);
                break;
              }
              e.timeoutHandle = Fy(Xs.bind(null, e, qa, Du), i);
              break;
            }
          }
          Xs(e, qa, Du);
          break;
        }
        case Mp: {
          if (Yo(e, a), Bv(a))
            break;
          if (!y1()) {
            var f = jv(e, a), p = f, v = gn() - p, y = Zb(v) - v;
            if (y > 10) {
              e.timeoutHandle = Fy(Xs.bind(null, e, qa, Du), y);
              break;
            }
          }
          Xs(e, qa, Du);
          break;
        }
        case XC: {
          Xs(e, qa, Du);
          break;
        }
        default:
          throw new Error("Unknown root exit status.");
      }
    }
    function Nb(e) {
      for (var t = e; ; ) {
        if (t.flags & cs) {
          var a = t.updateQueue;
          if (a !== null) {
            var i = a.stores;
            if (i !== null)
              for (var u = 0; u < i.length; u++) {
                var s = i[u], f = s.getSnapshot, p = s.value;
                try {
                  if (!ge(f(), p))
                    return !1;
                } catch {
                  return !1;
                }
              }
          }
        }
        var v = t.child;
        if (t.subtreeFlags & cs && v !== null) {
          v.return = t, t = v;
          continue;
        }
        if (t === e)
          return !0;
        for (; t.sibling === null; ) {
          if (t.return === null || t.return === e)
            return !0;
          t = t.return;
        }
        t.sibling.return = t.return, t = t.sibling;
      }
      return !0;
    }
    function Yo(e, t) {
      t = Cs(t, _m), t = Cs(t, zp), Qv(e, t);
    }
    function r1(e) {
      if (Xx(), (xt & (Vr | Oi)) !== fr)
        throw new Error("Should not already be working.");
      Lu();
      var t = du(e, $);
      if (!ia(t, ke))
        return Xa(e, gn()), null;
      var a = zm(e, t);
      if (e.tag !== Mo && a === Ws) {
        var i = Ol(e);
        i !== $ && (t = i, a = PS(e, i));
      }
      if (a === Lp) {
        var u = Np;
        throw qs(e, $), Yo(e, t), Xa(e, gn()), u;
      }
      if (a === NS)
        throw new Error("Root did not complete. This is a bug in React.");
      var s = e.current.alternate;
      return e.finishedWork = s, e.finishedLanes = t, Xs(e, qa, Du), Xa(e, gn()), null;
    }
    function zb(e, t) {
      t !== $ && (Dd(e, Ke(t, ke)), Xa(e, gn()), (xt & (Vr | Oi)) === fr && (Ap(), No()));
    }
    function BS(e, t) {
      var a = xt;
      xt |= qC;
      try {
        return e(t);
      } finally {
        xt = a, xt === fr && // Treat `act` as if it's inside `batchedUpdates`, even in legacy mode.
        !ul.isBatchingLegacy && (Ap(), eE());
      }
    }
    function Ub(e, t, a, i, u) {
      var s = Pa(), f = Hr.transition;
      try {
        return Hr.transition = null, xn(Ln), e(t, a, i, u);
      } finally {
        xn(s), Hr.transition = f, xt === fr && Ap();
      }
    }
    function Ou(e) {
      Bo !== null && Bo.tag === Mo && (xt & (Vr | Oi)) === fr && Lu();
      var t = xt;
      xt |= qC;
      var a = Hr.transition, i = Pa();
      try {
        return Hr.transition = null, xn(Ln), e ? e() : void 0;
      } finally {
        xn(i), Hr.transition = a, xt = t, (xt & (Vr | Oi)) === fr && No();
      }
    }
    function a1() {
      return (xt & (Vr | Oi)) !== fr;
    }
    function Nm(e, t) {
      oa(zS, Yl, e), Yl = Ke(Yl, t);
    }
    function $S(e) {
      Yl = zS.current, ua(zS, e);
    }
    function qs(e, t) {
      e.finishedWork = null, e.finishedLanes = $;
      var a = e.timeoutHandle;
      if (a !== Hy && (e.timeoutHandle = Hy, oT(a)), Nn !== null)
        for (var i = Nn.return; i !== null; ) {
          var u = i.alternate;
          NC(u, i), i = i.return;
        }
      xa = e;
      var s = Ks(e.current, null);
      return Nn = s, dr = Yl = t, pr = ku, Np = null, bm = $, zp = $, _m = $, Up = null, qa = null, Ox(), Ji.discardPendingWarnings(), s;
    }
    function i1(e, t) {
      do {
        var a = Nn;
        try {
          if ($h(), DE(), Rn(), MS.current = null, a === null || a.return === null) {
            pr = Lp, Np = t, Nn = null;
            return;
          }
          if (tt && a.mode & Qe && gm(a, !0), rt)
            if (na(), t !== null && typeof t == "object" && typeof t.then == "function") {
              var i = t;
              uu(a, i, dr);
            } else
              ps(a, t, dr);
          iw(e, a.return, a, t, dr), s1(a);
        } catch (u) {
          t = u, Nn === a && a !== null ? (a = a.return, Nn = a) : a = Nn;
          continue;
        }
        return;
      } while (!0);
    }
    function l1() {
      var e = LS.current;
      return LS.current = pm, e === null ? pm : e;
    }
    function u1(e) {
      LS.current = e;
    }
    function Ab() {
      US = gn();
    }
    function Vp(e) {
      bm = Ke(e, bm);
    }
    function jb() {
      pr === ku && (pr = wm);
    }
    function YS() {
      (pr === ku || pr === wm || pr === Ws) && (pr = Mp), xa !== null && (Ss(bm) || Ss(zp)) && Yo(xa, dr);
    }
    function Fb(e) {
      pr !== Mp && (pr = Ws), Up === null ? Up = [e] : Up.push(e);
    }
    function Hb() {
      return pr === ku;
    }
    function zm(e, t) {
      var a = xt;
      xt |= Vr;
      var i = l1();
      if (xa !== e || dr !== t) {
        if (Ea) {
          var u = e.memoizedUpdaters;
          u.size > 0 && (Pp(e, dr), u.clear()), Od(e, t);
        }
        Du = Ts(), qs(e, t);
      }
      fn(t);
      do
        try {
          Vb();
          break;
        } catch (s) {
          i1(e, s);
        }
      while (!0);
      if ($h(), xt = a, u1(i), Nn !== null)
        throw new Error("Cannot commit an incomplete root. This error is likely caused by a bug in React. Please file an issue.");
      return xc(), xa = null, dr = $, pr;
    }
    function Vb() {
      for (; Nn !== null; )
        o1(Nn);
    }
    function Pb(e, t) {
      var a = xt;
      xt |= Vr;
      var i = l1();
      if (xa !== e || dr !== t) {
        if (Ea) {
          var u = e.memoizedUpdaters;
          u.size > 0 && (Pp(e, dr), u.clear()), Od(e, t);
        }
        Du = Ts(), Ap(), qs(e, t);
      }
      fn(t);
      do
        try {
          Bb();
          break;
        } catch (s) {
          i1(e, s);
        }
      while (!0);
      return $h(), u1(i), xt = a, Nn !== null ? (Tc(), ku) : (xc(), xa = null, dr = $, pr);
    }
    function Bb() {
      for (; Nn !== null && !yc(); )
        o1(Nn);
    }
    function o1(e) {
      var t = e.alternate;
      Bt(e);
      var a;
      (e.mode & Qe) !== Ce ? (Wg(e), a = IS(t, e, Yl), gm(e, !0)) : a = IS(t, e, Yl), Rn(), e.memoizedProps = e.pendingProps, a === null ? s1(e) : Nn = a, MS.current = null;
    }
    function s1(e) {
      var t = e;
      do {
        var a = t.alternate, i = t.return;
        if ((t.flags & ya) === Le) {
          Bt(t);
          var u = void 0;
          if ((t.mode & Qe) === Ce ? u = MC(a, t, Yl) : (Wg(t), u = MC(a, t, Yl), gm(t, !1)), Rn(), u !== null) {
            Nn = u;
            return;
          }
        } else {
          var s = jw(a, t);
          if (s !== null) {
            s.flags &= bv, Nn = s;
            return;
          }
          if ((t.mode & Qe) !== Ce) {
            gm(t, !1);
            for (var f = t.actualDuration, p = t.child; p !== null; )
              f += p.actualDuration, p = p.sibling;
            t.actualDuration = f;
          }
          if (i !== null)
            i.flags |= ya, i.subtreeFlags = Le, i.deletions = null;
          else {
            pr = NS, Nn = null;
            return;
          }
        }
        var v = t.sibling;
        if (v !== null) {
          Nn = v;
          return;
        }
        t = i, Nn = t;
      } while (t !== null);
      pr === ku && (pr = XC);
    }
    function Xs(e, t, a) {
      var i = Pa(), u = Hr.transition;
      try {
        Hr.transition = null, xn(Ln), $b(e, t, a, i);
      } finally {
        Hr.transition = u, xn(i);
      }
      return null;
    }
    function $b(e, t, a, i) {
      do
        Lu();
      while (Bo !== null);
      if (e_(), (xt & (Vr | Oi)) !== fr)
        throw new Error("Should not already be working.");
      var u = e.finishedWork, s = e.finishedLanes;
      if (_l(s), u === null)
        return Ec(), null;
      if (s === $ && S("root.finishedLanes should not be empty during a commit. This is a bug in React."), e.finishedWork = null, e.finishedLanes = $, u === e.current)
        throw new Error("Cannot commit the same tree as before. This error is likely caused by a bug in React. Please file an issue.");
      e.callbackNode = null, e.callbackPriority = Fn;
      var f = Ke(u.lanes, u.childLanes);
      Yc(e, f), e === xa && (xa = null, Nn = null, dr = $), ((u.subtreeFlags & Aa) !== Le || (u.flags & Aa) !== Le) && (Gs || (Gs = !0, FS = a, GS(Ei, function() {
        return Lu(), null;
      })));
      var p = (u.subtreeFlags & (Zu | ea | Er | Aa)) !== Le, v = (u.flags & (Zu | ea | Er | Aa)) !== Le;
      if (p || v) {
        var y = Hr.transition;
        Hr.transition = null;
        var g = Pa();
        xn(Ln);
        var b = xt;
        xt |= Oi, MS.current = null, Bw(e, u), eC(), nb(e, u, s), tT(e.containerInfo), e.current = u, Cd(s), rb(u, e, s), ro(), Dv(), xt = b, xn(g), Hr.transition = y;
      } else
        e.current = u, eC();
      var x = Gs;
      if (Gs ? (Gs = !1, Bo = e, jp = s) : (Hf = 0, Om = null), f = e.pendingLanes, f === $ && (Ff = null), x || p1(e.current, !1), eo(u.stateNode, i), Ea && e.memoizedUpdaters.clear(), Rb(), Xa(e, gn()), t !== null)
        for (var N = e.onRecoverableError, A = 0; A < t.length; A++) {
          var F = t[A], le = F.stack, Me = F.digest;
          N(F.value, {
            componentStack: le,
            digest: Me
          });
        }
      if (km) {
        km = !1;
        var we = AS;
        throw AS = null, we;
      }
      return ia(jp, ke) && e.tag !== Mo && Lu(), f = e.pendingLanes, ia(f, ke) ? (Gx(), e === HS ? Fp++ : (Fp = 0, HS = e)) : Fp = 0, No(), Ec(), null;
    }
    function Lu() {
      if (Bo !== null) {
        var e = lr(jp), t = sy(Ci, e), a = Hr.transition, i = Pa();
        try {
          return Hr.transition = null, xn(t), Ib();
        } finally {
          xn(i), Hr.transition = a;
        }
      }
      return !1;
    }
    function Yb(e) {
      jS.push(e), Gs || (Gs = !0, GS(Ei, function() {
        return Lu(), null;
      }));
    }
    function Ib() {
      if (Bo === null)
        return !1;
      var e = FS;
      FS = null;
      var t = Bo, a = jp;
      if (Bo = null, jp = $, (xt & (Vr | Oi)) !== fr)
        throw new Error("Cannot flush passive effects while already rendering.");
      VS = !0, Dm = !1, Uv(a);
      var i = xt;
      xt |= Oi, cb(t.current), lb(t, t.current, a, e);
      {
        var u = jS;
        jS = [];
        for (var s = 0; s < u.length; s++) {
          var f = u[s];
          Qw(t, f);
        }
      }
      Rd(), p1(t.current, !0), xt = i, No(), Dm ? t === Om ? Hf++ : (Hf = 0, Om = t) : Hf = 0, VS = !1, Dm = !1, Ha(t);
      {
        var p = t.current.stateNode;
        p.effectDuration = 0, p.passiveEffectDuration = 0;
      }
      return !0;
    }
    function c1(e) {
      return Ff !== null && Ff.has(e);
    }
    function Qb(e) {
      Ff === null ? Ff = /* @__PURE__ */ new Set([e]) : Ff.add(e);
    }
    function Wb(e) {
      km || (km = !0, AS = e);
    }
    var Gb = Wb;
    function f1(e, t, a) {
      var i = Is(a, t), u = oC(e, i, ke), s = Uo(e, u, ke), f = wa();
      s !== null && (vu(s, ke, f), Xa(s, f));
    }
    function sn(e, t, a) {
      if (Hw(a), Bp(!1), e.tag === re) {
        f1(e, e, a);
        return;
      }
      var i = null;
      for (i = t; i !== null; ) {
        if (i.tag === re) {
          f1(i, e, a);
          return;
        } else if (i.tag === se) {
          var u = i.type, s = i.stateNode;
          if (typeof u.getDerivedStateFromError == "function" || typeof s.componentDidCatch == "function" && !c1(s)) {
            var f = Is(a, e), p = fS(i, f, ke), v = Uo(i, p, ke), y = wa();
            v !== null && (vu(v, ke, y), Xa(v, y));
            return;
          }
        }
        i = i.return;
      }
      S(`Internal React error: Attempted to capture a commit phase error inside a detached tree. This indicates a bug in React. Likely causes include deleting the same fiber more than once, committing an already-finished tree, or an inconsistent return pointer.

Error message:

%s`, a);
    }
    function qb(e, t, a) {
      var i = e.pingCache;
      i !== null && i.delete(t);
      var u = wa();
      $c(e, a), a_(e), xa === e && pu(dr, a) && (pr === Mp || pr === wm && Vv(dr) && gn() - US < KC ? qs(e, $) : _m = Ke(_m, a)), Xa(e, u);
    }
    function d1(e, t) {
      t === Fn && (t = Db(e));
      var a = wa(), i = Wa(e, t);
      i !== null && (vu(i, t, a), Xa(i, a));
    }
    function Xb(e) {
      var t = e.memoizedState, a = Fn;
      t !== null && (a = t.retryLane), d1(e, a);
    }
    function Kb(e, t) {
      var a = Fn, i;
      switch (e.tag) {
        case Oe:
          i = e.stateNode;
          var u = e.memoizedState;
          u !== null && (a = u.retryLane);
          break;
        case Ot:
          i = e.stateNode;
          break;
        default:
          throw new Error("Pinged unknown suspense boundary type. This is probably a bug in React.");
      }
      i !== null && i.delete(t), d1(e, a);
    }
    function Zb(e) {
      return e < 120 ? 120 : e < 480 ? 480 : e < 1080 ? 1080 : e < 1920 ? 1920 : e < 3e3 ? 3e3 : e < 4320 ? 4320 : wb(e / 1960) * 1960;
    }
    function Jb() {
      if (Fp > _b)
        throw Fp = 0, HS = null, new Error("Maximum update depth exceeded. This can happen when a component repeatedly calls setState inside componentWillUpdate or componentDidUpdate. React limits the number of nested updates to prevent infinite loops.");
      Hf > kb && (Hf = 0, Om = null, S("Maximum update depth exceeded. This can happen when a component calls setState inside useEffect, but useEffect either doesn't have a dependency array, or one of the dependencies changes on every render."));
    }
    function e_() {
      Ji.flushLegacyContextWarning(), Ji.flushPendingUnsafeLifecycleWarnings();
    }
    function p1(e, t) {
      Bt(e), Um(e, Jr, Sb), t && Um(e, au, Eb), Um(e, Jr, yb), t && Um(e, au, gb), Rn();
    }
    function Um(e, t, a) {
      for (var i = e, u = null; i !== null; ) {
        var s = i.subtreeFlags & t;
        i !== u && i.child !== null && s !== Le ? i = i.child : ((i.flags & t) !== Le && a(i), i.sibling !== null ? i = i.sibling : i = u = i.return);
      }
    }
    var Am = null;
    function v1(e) {
      {
        if ((xt & Vr) !== fr || !(e.mode & xe))
          return;
        var t = e.tag;
        if (t !== nt && t !== re && t !== se && t !== de && t !== qe && t !== ft && t !== Ve)
          return;
        var a = We(e) || "ReactComponent";
        if (Am !== null) {
          if (Am.has(a))
            return;
          Am.add(a);
        } else
          Am = /* @__PURE__ */ new Set([a]);
        var i = yn;
        try {
          Bt(e), S("Can't perform a React state update on a component that hasn't mounted yet. This indicates that you have a side-effect in your render function that asynchronously later calls tries to update the component. Move this work to useEffect instead.");
        } finally {
          i ? Bt(e) : Rn();
        }
      }
    }
    var IS;
    {
      var t_ = null;
      IS = function(e, t, a) {
        var i = R1(t_, t);
        try {
          return _C(e, t, a);
        } catch (s) {
          if (px() || s !== null && typeof s == "object" && typeof s.then == "function")
            throw s;
          if ($h(), DE(), NC(e, t), R1(t, i), t.mode & Qe && Wg(t), ru(null, _C, null, e, t, a), ay()) {
            var u = dd();
            typeof u == "object" && u !== null && u._suppressLogging && typeof s == "object" && s !== null && !s._suppressLogging && (s._suppressLogging = !0);
          }
          throw s;
        }
      };
    }
    var h1 = !1, QS;
    QS = /* @__PURE__ */ new Set();
    function n_(e) {
      if (Gr && !Ix())
        switch (e.tag) {
          case de:
          case qe:
          case Ve: {
            var t = Nn && We(Nn) || "Unknown", a = t;
            if (!QS.has(a)) {
              QS.add(a);
              var i = We(e) || "Unknown";
              S("Cannot update a component (`%s`) while rendering a different component (`%s`). To locate the bad setState() call inside `%s`, follow the stack trace as described in https://reactjs.org/link/setstate-in-render", i, t, t);
            }
            break;
          }
          case se: {
            h1 || (S("Cannot update during an existing state transition (such as within `render`). Render methods should be a pure function of props and state."), h1 = !0);
            break;
          }
        }
    }
    function Pp(e, t) {
      if (Ea) {
        var a = e.memoizedUpdaters;
        a.forEach(function(i) {
          Ic(e, i, t);
        });
      }
    }
    var WS = {};
    function GS(e, t) {
      {
        var a = ul.current;
        return a !== null ? (a.push(t), WS) : mc(e, t);
      }
    }
    function m1(e) {
      if (e !== WS)
        return kv(e);
    }
    function y1() {
      return ul.current !== null;
    }
    function r_(e) {
      {
        if (e.mode & xe) {
          if (!GC())
            return;
        } else if (!xb() || xt !== fr || e.tag !== de && e.tag !== qe && e.tag !== Ve)
          return;
        if (ul.current === null) {
          var t = yn;
          try {
            Bt(e), S(`An update to %s inside a test was not wrapped in act(...).

When testing, code that causes React state updates should be wrapped into act(...):

act(() => {
  /* fire events that update state */
});
/* assert on the output */

This ensures that you're testing the behavior the user would see in the browser. Learn more at https://reactjs.org/link/wrap-tests-with-act`, We(e));
          } finally {
            t ? Bt(e) : Rn();
          }
        }
      }
    }
    function a_(e) {
      e.tag !== Mo && GC() && ul.current === null && S(`A suspended resource finished loading inside a test, but the event was not wrapped in act(...).

When testing, code that resolves suspended data should be wrapped into act(...):

act(() => {
  /* finish loading suspended data */
});
/* assert on the output */

This ensures that you're testing the behavior the user would see in the browser. Learn more at https://reactjs.org/link/wrap-tests-with-act`);
    }
    function Bp(e) {
      e1 = e;
    }
    var Li = null, Vf = null, i_ = function(e) {
      Li = e;
    };
    function Pf(e) {
      {
        if (Li === null)
          return e;
        var t = Li(e);
        return t === void 0 ? e : t.current;
      }
    }
    function qS(e) {
      return Pf(e);
    }
    function XS(e) {
      {
        if (Li === null)
          return e;
        var t = Li(e);
        if (t === void 0) {
          if (e != null && typeof e.render == "function") {
            var a = Pf(e.render);
            if (e.render !== a) {
              var i = {
                $$typeof: q,
                render: a
              };
              return e.displayName !== void 0 && (i.displayName = e.displayName), i;
            }
          }
          return e;
        }
        return t.current;
      }
    }
    function g1(e, t) {
      {
        if (Li === null)
          return !1;
        var a = e.elementType, i = t.type, u = !1, s = typeof i == "object" && i !== null ? i.$$typeof : null;
        switch (e.tag) {
          case se: {
            typeof i == "function" && (u = !0);
            break;
          }
          case de: {
            (typeof i == "function" || s === Ae) && (u = !0);
            break;
          }
          case qe: {
            (s === q || s === Ae) && (u = !0);
            break;
          }
          case ft:
          case Ve: {
            (s === Et || s === Ae) && (u = !0);
            break;
          }
          default:
            return !1;
        }
        if (u) {
          var f = Li(a);
          if (f !== void 0 && f === Li(i))
            return !0;
        }
        return !1;
      }
    }
    function S1(e) {
      {
        if (Li === null || typeof WeakSet != "function")
          return;
        Vf === null && (Vf = /* @__PURE__ */ new WeakSet()), Vf.add(e);
      }
    }
    var l_ = function(e, t) {
      {
        if (Li === null)
          return;
        var a = t.staleFamilies, i = t.updatedFamilies;
        Lu(), Ou(function() {
          KS(e.current, i, a);
        });
      }
    }, u_ = function(e, t) {
      {
        if (e.context !== oi)
          return;
        Lu(), Ou(function() {
          $p(t, e, null, null);
        });
      }
    };
    function KS(e, t, a) {
      {
        var i = e.alternate, u = e.child, s = e.sibling, f = e.tag, p = e.type, v = null;
        switch (f) {
          case de:
          case Ve:
          case se:
            v = p;
            break;
          case qe:
            v = p.render;
            break;
        }
        if (Li === null)
          throw new Error("Expected resolveFamily to be set during hot reload.");
        var y = !1, g = !1;
        if (v !== null) {
          var b = Li(v);
          b !== void 0 && (a.has(b) ? g = !0 : t.has(b) && (f === se ? g = !0 : y = !0));
        }
        if (Vf !== null && (Vf.has(e) || i !== null && Vf.has(i)) && (g = !0), g && (e._debugNeedsRemount = !0), g || y) {
          var x = Wa(e, ke);
          x !== null && vr(x, e, ke, nn);
        }
        u !== null && !g && KS(u, t, a), s !== null && KS(s, t, a);
      }
    }
    var o_ = function(e, t) {
      {
        var a = /* @__PURE__ */ new Set(), i = new Set(t.map(function(u) {
          return u.current;
        }));
        return ZS(e.current, i, a), a;
      }
    };
    function ZS(e, t, a) {
      {
        var i = e.child, u = e.sibling, s = e.tag, f = e.type, p = null;
        switch (s) {
          case de:
          case Ve:
          case se:
            p = f;
            break;
          case qe:
            p = f.render;
            break;
        }
        var v = !1;
        p !== null && t.has(p) && (v = !0), v ? s_(e, a) : i !== null && ZS(i, t, a), u !== null && ZS(u, t, a);
      }
    }
    function s_(e, t) {
      {
        var a = c_(e, t);
        if (a)
          return;
        for (var i = e; ; ) {
          switch (i.tag) {
            case ue:
              t.add(i.stateNode);
              return;
            case pe:
              t.add(i.stateNode.containerInfo);
              return;
            case re:
              t.add(i.stateNode.containerInfo);
              return;
          }
          if (i.return === null)
            throw new Error("Expected to reach root first.");
          i = i.return;
        }
      }
    }
    function c_(e, t) {
      for (var a = e, i = !1; ; ) {
        if (a.tag === ue)
          i = !0, t.add(a.stateNode);
        else if (a.child !== null) {
          a.child.return = a, a = a.child;
          continue;
        }
        if (a === e)
          return i;
        for (; a.sibling === null; ) {
          if (a.return === null || a.return === e)
            return i;
          a = a.return;
        }
        a.sibling.return = a.return, a = a.sibling;
      }
      return !1;
    }
    var JS;
    {
      JS = !1;
      try {
        var E1 = Object.preventExtensions({});
      } catch {
        JS = !0;
      }
    }
    function f_(e, t, a, i) {
      this.tag = e, this.key = a, this.elementType = null, this.type = null, this.stateNode = null, this.return = null, this.child = null, this.sibling = null, this.index = 0, this.ref = null, this.pendingProps = t, this.memoizedProps = null, this.updateQueue = null, this.memoizedState = null, this.dependencies = null, this.mode = i, this.flags = Le, this.subtreeFlags = Le, this.deletions = null, this.lanes = $, this.childLanes = $, this.alternate = null, this.actualDuration = Number.NaN, this.actualStartTime = Number.NaN, this.selfBaseDuration = Number.NaN, this.treeBaseDuration = Number.NaN, this.actualDuration = 0, this.actualStartTime = -1, this.selfBaseDuration = 0, this.treeBaseDuration = 0, this._debugSource = null, this._debugOwner = null, this._debugNeedsRemount = !1, this._debugHookTypes = null, !JS && typeof Object.preventExtensions == "function" && Object.preventExtensions(this);
    }
    var si = function(e, t, a, i) {
      return new f_(e, t, a, i);
    };
    function e0(e) {
      var t = e.prototype;
      return !!(t && t.isReactComponent);
    }
    function d_(e) {
      return typeof e == "function" && !e0(e) && e.defaultProps === void 0;
    }
    function p_(e) {
      if (typeof e == "function")
        return e0(e) ? se : de;
      if (e != null) {
        var t = e.$$typeof;
        if (t === q)
          return qe;
        if (t === Et)
          return ft;
      }
      return nt;
    }
    function Ks(e, t) {
      var a = e.alternate;
      a === null ? (a = si(e.tag, t, e.key, e.mode), a.elementType = e.elementType, a.type = e.type, a.stateNode = e.stateNode, a._debugSource = e._debugSource, a._debugOwner = e._debugOwner, a._debugHookTypes = e._debugHookTypes, a.alternate = e, e.alternate = a) : (a.pendingProps = t, a.type = e.type, a.flags = Le, a.subtreeFlags = Le, a.deletions = null, a.actualDuration = 0, a.actualStartTime = -1), a.flags = e.flags & ar, a.childLanes = e.childLanes, a.lanes = e.lanes, a.child = e.child, a.memoizedProps = e.memoizedProps, a.memoizedState = e.memoizedState, a.updateQueue = e.updateQueue;
      var i = e.dependencies;
      switch (a.dependencies = i === null ? null : {
        lanes: i.lanes,
        firstContext: i.firstContext
      }, a.sibling = e.sibling, a.index = e.index, a.ref = e.ref, a.selfBaseDuration = e.selfBaseDuration, a.treeBaseDuration = e.treeBaseDuration, a._debugNeedsRemount = e._debugNeedsRemount, a.tag) {
        case nt:
        case de:
        case Ve:
          a.type = Pf(e.type);
          break;
        case se:
          a.type = qS(e.type);
          break;
        case qe:
          a.type = XS(e.type);
          break;
      }
      return a;
    }
    function v_(e, t) {
      e.flags &= ar | ln;
      var a = e.alternate;
      if (a === null)
        e.childLanes = $, e.lanes = t, e.child = null, e.subtreeFlags = Le, e.memoizedProps = null, e.memoizedState = null, e.updateQueue = null, e.dependencies = null, e.stateNode = null, e.selfBaseDuration = 0, e.treeBaseDuration = 0;
      else {
        e.childLanes = a.childLanes, e.lanes = a.lanes, e.child = a.child, e.subtreeFlags = Le, e.deletions = null, e.memoizedProps = a.memoizedProps, e.memoizedState = a.memoizedState, e.updateQueue = a.updateQueue, e.type = a.type;
        var i = a.dependencies;
        e.dependencies = i === null ? null : {
          lanes: i.lanes,
          firstContext: i.firstContext
        }, e.selfBaseDuration = a.selfBaseDuration, e.treeBaseDuration = a.treeBaseDuration;
      }
      return e;
    }
    function h_(e, t, a) {
      var i;
      return e === Nh ? (i = xe, t === !0 && (i |= vt, i |= Ca)) : i = Ce, Ea && (i |= Qe), si(re, null, null, i);
    }
    function t0(e, t, a, i, u, s) {
      var f = nt, p = e;
      if (typeof e == "function")
        e0(e) ? (f = se, p = qS(p)) : p = Pf(p);
      else if (typeof e == "string")
        f = ue;
      else
        e:
          switch (e) {
            case ma:
              return Io(a.children, u, s, t);
            case pi:
              f = ht, u |= vt, (u & xe) !== Ce && (u |= Ca);
              break;
            case vi:
              return m_(a, u, s, t);
            case Te:
              return y_(a, u, s, t);
            case dt:
              return g_(a, u, s, t);
            case Xt:
              return C1(a, u, s, t);
            case an:
            case it:
            case Sr:
            case hi:
            case Un:
            default: {
              if (typeof e == "object" && e !== null)
                switch (e.$$typeof) {
                  case R:
                    f = ot;
                    break e;
                  case Y:
                    f = pn;
                    break e;
                  case q:
                    f = qe, p = XS(p);
                    break e;
                  case Et:
                    f = ft;
                    break e;
                  case Ae:
                    f = rn, p = null;
                    break e;
                }
              var v = "";
              {
                (e === void 0 || typeof e == "object" && e !== null && Object.keys(e).length === 0) && (v += " You likely forgot to export your component from the file it's defined in, or you might have mixed up default and named imports.");
                var y = i ? We(i) : null;
                y && (v += `

Check the render method of \`` + y + "`.");
              }
              throw new Error("Element type is invalid: expected a string (for built-in components) or a class/function (for composite components) " + ("but got: " + (e == null ? e : typeof e) + "." + v));
            }
          }
      var g = si(f, a, t, u);
      return g.elementType = e, g.type = p, g.lanes = s, g._debugOwner = i, g;
    }
    function n0(e, t, a) {
      var i = null;
      i = e._owner;
      var u = e.type, s = e.key, f = e.props, p = t0(u, s, f, i, t, a);
      return p._debugSource = e._source, p._debugOwner = e._owner, p;
    }
    function Io(e, t, a, i) {
      var u = si(bt, e, i, t);
      return u.lanes = a, u;
    }
    function m_(e, t, a, i) {
      typeof e.id != "string" && S('Profiler must specify an "id" of type `string` as a prop. Received the type `%s` instead.', typeof e.id);
      var u = si(mt, e, i, t | Qe);
      return u.elementType = vi, u.lanes = a, u.stateNode = {
        effectDuration: 0,
        passiveEffectDuration: 0
      }, u;
    }
    function y_(e, t, a, i) {
      var u = si(Oe, e, i, t);
      return u.elementType = Te, u.lanes = a, u;
    }
    function g_(e, t, a, i) {
      var u = si(Ot, e, i, t);
      return u.elementType = dt, u.lanes = a, u;
    }
    function C1(e, t, a, i) {
      var u = si(ze, e, i, t);
      u.elementType = Xt, u.lanes = a;
      var s = {
        isHidden: !1
      };
      return u.stateNode = s, u;
    }
    function r0(e, t, a) {
      var i = si(Ye, e, null, t);
      return i.lanes = a, i;
    }
    function S_() {
      var e = si(ue, null, null, Ce);
      return e.elementType = "DELETED", e;
    }
    function E_(e) {
      var t = si(Wt, null, null, Ce);
      return t.stateNode = e, t;
    }
    function a0(e, t, a) {
      var i = e.children !== null ? e.children : [], u = si(pe, i, e.key, t);
      return u.lanes = a, u.stateNode = {
        containerInfo: e.containerInfo,
        pendingChildren: null,
        // Used by persistent updates
        implementation: e.implementation
      }, u;
    }
    function R1(e, t) {
      return e === null && (e = si(nt, null, null, Ce)), e.tag = t.tag, e.key = t.key, e.elementType = t.elementType, e.type = t.type, e.stateNode = t.stateNode, e.return = t.return, e.child = t.child, e.sibling = t.sibling, e.index = t.index, e.ref = t.ref, e.pendingProps = t.pendingProps, e.memoizedProps = t.memoizedProps, e.updateQueue = t.updateQueue, e.memoizedState = t.memoizedState, e.dependencies = t.dependencies, e.mode = t.mode, e.flags = t.flags, e.subtreeFlags = t.subtreeFlags, e.deletions = t.deletions, e.lanes = t.lanes, e.childLanes = t.childLanes, e.alternate = t.alternate, e.actualDuration = t.actualDuration, e.actualStartTime = t.actualStartTime, e.selfBaseDuration = t.selfBaseDuration, e.treeBaseDuration = t.treeBaseDuration, e._debugSource = t._debugSource, e._debugOwner = t._debugOwner, e._debugNeedsRemount = t._debugNeedsRemount, e._debugHookTypes = t._debugHookTypes, e;
    }
    function C_(e, t, a, i, u) {
      this.tag = t, this.containerInfo = e, this.pendingChildren = null, this.current = null, this.pingCache = null, this.finishedWork = null, this.timeoutHandle = Hy, this.context = null, this.pendingContext = null, this.callbackNode = null, this.callbackPriority = Fn, this.eventTimes = Rs($), this.expirationTimes = Rs(nn), this.pendingLanes = $, this.suspendedLanes = $, this.pingedLanes = $, this.expiredLanes = $, this.mutableReadLanes = $, this.finishedLanes = $, this.entangledLanes = $, this.entanglements = Rs($), this.identifierPrefix = i, this.onRecoverableError = u, this.mutableSourceEagerHydrationData = null, this.effectDuration = 0, this.passiveEffectDuration = 0;
      {
        this.memoizedUpdaters = /* @__PURE__ */ new Set();
        for (var s = this.pendingUpdatersLaneMap = [], f = 0; f < ms; f++)
          s.push(/* @__PURE__ */ new Set());
      }
      switch (t) {
        case Nh:
          this._debugRootType = a ? "hydrateRoot()" : "createRoot()";
          break;
        case Mo:
          this._debugRootType = a ? "hydrate()" : "render()";
          break;
      }
    }
    function T1(e, t, a, i, u, s, f, p, v, y) {
      var g = new C_(e, t, a, p, v), b = h_(t, s);
      g.current = b, b.stateNode = g;
      {
        var x = {
          element: i,
          isDehydrated: a,
          cache: null,
          // not enabled yet
          transitions: null,
          pendingSuspenseBoundaries: null
        };
        b.memoizedState = x;
      }
      return yg(b), g;
    }
    var i0 = "18.3.1";
    function R_(e, t, a) {
      var i = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : null;
      return Yr(i), {
        // This tag allow us to uniquely identify this as a React Portal
        $$typeof: _r,
        key: i == null ? null : "" + i,
        children: e,
        containerInfo: t,
        implementation: a
      };
    }
    var l0, u0;
    l0 = !1, u0 = {};
    function x1(e) {
      if (!e)
        return oi;
      var t = Na(e), a = ax(t);
      if (t.tag === se) {
        var i = t.type;
        if (jl(i))
          return K0(t, i, a);
      }
      return a;
    }
    function T_(e, t) {
      {
        var a = Na(e);
        if (a === void 0) {
          if (typeof e.render == "function")
            throw new Error("Unable to find node on an unmounted component.");
          var i = Object.keys(e).join(",");
          throw new Error("Argument appears to not be a ReactComponent. Keys: " + i);
        }
        var u = ja(a);
        if (u === null)
          return null;
        if (u.mode & vt) {
          var s = We(a) || "Component";
          if (!u0[s]) {
            u0[s] = !0;
            var f = yn;
            try {
              Bt(u), a.mode & vt ? S("%s is deprecated in StrictMode. %s was passed an instance of %s which is inside StrictMode. Instead, add a ref directly to the element you want to reference. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-find-node", t, t, s) : S("%s is deprecated in StrictMode. %s was passed an instance of %s which renders StrictMode children. Instead, add a ref directly to the element you want to reference. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-find-node", t, t, s);
            } finally {
              f ? Bt(f) : Rn();
            }
          }
        }
        return u.stateNode;
      }
    }
    function w1(e, t, a, i, u, s, f, p) {
      var v = !1, y = null;
      return T1(e, t, v, y, a, i, u, s, f);
    }
    function b1(e, t, a, i, u, s, f, p, v, y) {
      var g = !0, b = T1(a, i, g, e, u, s, f, p, v);
      b.context = x1(null);
      var x = b.current, N = wa(), A = $o(x), F = bu(N, A);
      return F.callback = t ?? null, Uo(x, F, A), Ob(b, A, N), b;
    }
    function $p(e, t, a, i) {
      Ed(t, e);
      var u = t.current, s = wa(), f = $o(u);
      Td(f);
      var p = x1(a);
      t.context === null ? t.context = p : t.pendingContext = p, Gr && yn !== null && !l0 && (l0 = !0, S(`Render methods should be a pure function of props and state; triggering nested component updates from render is not allowed. If necessary, trigger nested updates in componentDidUpdate.

Check the render method of %s.`, We(yn) || "Unknown"));
      var v = bu(s, f);
      v.payload = {
        element: e
      }, i = i === void 0 ? null : i, i !== null && (typeof i != "function" && S("render(...): Expected the last optional `callback` argument to be a function. Instead received: %s.", i), v.callback = i);
      var y = Uo(u, v, f);
      return y !== null && (vr(y, u, f, s), Gh(y, u, f)), f;
    }
    function jm(e) {
      var t = e.current;
      if (!t.child)
        return null;
      switch (t.child.tag) {
        case ue:
          return t.child.stateNode;
        default:
          return t.child.stateNode;
      }
    }
    function x_(e) {
      switch (e.tag) {
        case re: {
          var t = e.stateNode;
          if (Qc(t)) {
            var a = bd(t);
            zb(t, a);
          }
          break;
        }
        case Oe: {
          Ou(function() {
            var u = Wa(e, ke);
            if (u !== null) {
              var s = wa();
              vr(u, e, ke, s);
            }
          });
          var i = ke;
          o0(e, i);
          break;
        }
      }
    }
    function _1(e, t) {
      var a = e.memoizedState;
      a !== null && a.dehydrated !== null && (a.retryLane = Iv(a.retryLane, t));
    }
    function o0(e, t) {
      _1(e, t);
      var a = e.alternate;
      a && _1(a, t);
    }
    function w_(e) {
      if (e.tag === Oe) {
        var t = gs, a = Wa(e, t);
        if (a !== null) {
          var i = wa();
          vr(a, e, t, i);
        }
        o0(e, t);
      }
    }
    function b_(e) {
      if (e.tag === Oe) {
        var t = $o(e), a = Wa(e, t);
        if (a !== null) {
          var i = wa();
          vr(a, e, t, i);
        }
        o0(e, t);
      }
    }
    function k1(e) {
      var t = _v(e);
      return t === null ? null : t.stateNode;
    }
    var D1 = function(e) {
      return null;
    };
    function __(e) {
      return D1(e);
    }
    var O1 = function(e) {
      return !1;
    };
    function k_(e) {
      return O1(e);
    }
    var L1 = null, M1 = null, N1 = null, z1 = null, U1 = null, A1 = null, j1 = null, F1 = null, H1 = null;
    {
      var V1 = function(e, t, a) {
        var i = t[a], u = Rt(e) ? e.slice() : lt({}, e);
        return a + 1 === t.length ? (Rt(u) ? u.splice(i, 1) : delete u[i], u) : (u[i] = V1(e[i], t, a + 1), u);
      }, P1 = function(e, t) {
        return V1(e, t, 0);
      }, B1 = function(e, t, a, i) {
        var u = t[i], s = Rt(e) ? e.slice() : lt({}, e);
        if (i + 1 === t.length) {
          var f = a[i];
          s[f] = s[u], Rt(s) ? s.splice(u, 1) : delete s[u];
        } else
          s[u] = B1(
            // $FlowFixMe number or string is fine here
            e[u],
            t,
            a,
            i + 1
          );
        return s;
      }, $1 = function(e, t, a) {
        if (t.length !== a.length) {
          $e("copyWithRename() expects paths of the same length");
          return;
        } else
          for (var i = 0; i < a.length - 1; i++)
            if (t[i] !== a[i]) {
              $e("copyWithRename() expects paths to be the same except for the deepest key");
              return;
            }
        return B1(e, t, a, 0);
      }, Y1 = function(e, t, a, i) {
        if (a >= t.length)
          return i;
        var u = t[a], s = Rt(e) ? e.slice() : lt({}, e);
        return s[u] = Y1(e[u], t, a + 1, i), s;
      }, I1 = function(e, t, a) {
        return Y1(e, t, 0, a);
      }, s0 = function(e, t) {
        for (var a = e.memoizedState; a !== null && t > 0; )
          a = a.next, t--;
        return a;
      };
      L1 = function(e, t, a, i) {
        var u = s0(e, t);
        if (u !== null) {
          var s = I1(u.memoizedState, a, i);
          u.memoizedState = s, u.baseState = s, e.memoizedProps = lt({}, e.memoizedProps);
          var f = Wa(e, ke);
          f !== null && vr(f, e, ke, nn);
        }
      }, M1 = function(e, t, a) {
        var i = s0(e, t);
        if (i !== null) {
          var u = P1(i.memoizedState, a);
          i.memoizedState = u, i.baseState = u, e.memoizedProps = lt({}, e.memoizedProps);
          var s = Wa(e, ke);
          s !== null && vr(s, e, ke, nn);
        }
      }, N1 = function(e, t, a, i) {
        var u = s0(e, t);
        if (u !== null) {
          var s = $1(u.memoizedState, a, i);
          u.memoizedState = s, u.baseState = s, e.memoizedProps = lt({}, e.memoizedProps);
          var f = Wa(e, ke);
          f !== null && vr(f, e, ke, nn);
        }
      }, z1 = function(e, t, a) {
        e.pendingProps = I1(e.memoizedProps, t, a), e.alternate && (e.alternate.pendingProps = e.pendingProps);
        var i = Wa(e, ke);
        i !== null && vr(i, e, ke, nn);
      }, U1 = function(e, t) {
        e.pendingProps = P1(e.memoizedProps, t), e.alternate && (e.alternate.pendingProps = e.pendingProps);
        var a = Wa(e, ke);
        a !== null && vr(a, e, ke, nn);
      }, A1 = function(e, t, a) {
        e.pendingProps = $1(e.memoizedProps, t, a), e.alternate && (e.alternate.pendingProps = e.pendingProps);
        var i = Wa(e, ke);
        i !== null && vr(i, e, ke, nn);
      }, j1 = function(e) {
        var t = Wa(e, ke);
        t !== null && vr(t, e, ke, nn);
      }, F1 = function(e) {
        D1 = e;
      }, H1 = function(e) {
        O1 = e;
      };
    }
    function D_(e) {
      var t = ja(e);
      return t === null ? null : t.stateNode;
    }
    function O_(e) {
      return null;
    }
    function L_() {
      return yn;
    }
    function M_(e) {
      var t = e.findFiberByHostInstance, a = k.ReactCurrentDispatcher;
      return Sd({
        bundleType: e.bundleType,
        version: e.version,
        rendererPackageName: e.rendererPackageName,
        rendererConfig: e.rendererConfig,
        overrideHookState: L1,
        overrideHookStateDeletePath: M1,
        overrideHookStateRenamePath: N1,
        overrideProps: z1,
        overridePropsDeletePath: U1,
        overridePropsRenamePath: A1,
        setErrorHandler: F1,
        setSuspenseHandler: H1,
        scheduleUpdate: j1,
        currentDispatcherRef: a,
        findHostInstanceByFiber: D_,
        findFiberByHostInstance: t || O_,
        // React Refresh
        findHostInstancesForRefresh: o_,
        scheduleRefresh: l_,
        scheduleRoot: u_,
        setRefreshHandler: i_,
        // Enables DevTools to append owner stacks to error messages in DEV mode.
        getCurrentFiber: L_,
        // Enables DevTools to detect reconciler version rather than renderer version
        // which may not match for third party renderers.
        reconcilerVersion: i0
      });
    }
    var Q1 = typeof reportError == "function" ? (
      // In modern browsers, reportError will dispatch an error event,
      // emulating an uncaught JavaScript error.
      reportError
    ) : function(e) {
      console.error(e);
    };
    function c0(e) {
      this._internalRoot = e;
    }
    Fm.prototype.render = c0.prototype.render = function(e) {
      var t = this._internalRoot;
      if (t === null)
        throw new Error("Cannot update an unmounted root.");
      {
        typeof arguments[1] == "function" ? S("render(...): does not support the second callback argument. To execute a side effect after rendering, declare it in a component body with useEffect().") : Hm(arguments[1]) ? S("You passed a container to the second argument of root.render(...). You don't need to pass it again since you already passed it to create the root.") : typeof arguments[1] < "u" && S("You passed a second argument to root.render(...) but it only accepts one argument.");
        var a = t.containerInfo;
        if (a.nodeType !== An) {
          var i = k1(t.current);
          i && i.parentNode !== a && S("render(...): It looks like the React-rendered content of the root container was removed without using React. This is not supported and will cause errors. Instead, call root.unmount() to empty a root's container.");
        }
      }
      $p(e, t, null, null);
    }, Fm.prototype.unmount = c0.prototype.unmount = function() {
      typeof arguments[0] == "function" && S("unmount(...): does not support a callback argument. To execute a side effect after rendering, declare it in a component body with useEffect().");
      var e = this._internalRoot;
      if (e !== null) {
        this._internalRoot = null;
        var t = e.containerInfo;
        a1() && S("Attempted to synchronously unmount a root while React was already rendering. React cannot finish unmounting the root until the current render has completed, which may lead to a race condition."), Ou(function() {
          $p(null, e, null, null);
        }), Q0(t);
      }
    };
    function N_(e, t) {
      if (!Hm(e))
        throw new Error("createRoot(...): Target container is not a DOM element.");
      W1(e);
      var a = !1, i = !1, u = "", s = Q1;
      t != null && (t.hydrate ? $e("hydrate through createRoot is deprecated. Use ReactDOMClient.hydrateRoot(container, <App />) instead.") : typeof t == "object" && t !== null && t.$$typeof === ei && S(`You passed a JSX element to createRoot. You probably meant to call root.render instead. Example usage:

  let root = createRoot(domContainer);
  root.render(<App />);`), t.unstable_strictMode === !0 && (a = !0), t.identifierPrefix !== void 0 && (u = t.identifierPrefix), t.onRecoverableError !== void 0 && (s = t.onRecoverableError), t.transitionCallbacks !== void 0 && t.transitionCallbacks);
      var f = w1(e, Nh, null, a, i, u, s);
      bh(f.current, e);
      var p = e.nodeType === An ? e.parentNode : e;
      return qd(p), new c0(f);
    }
    function Fm(e) {
      this._internalRoot = e;
    }
    function z_(e) {
      e && dy(e);
    }
    Fm.prototype.unstable_scheduleHydration = z_;
    function U_(e, t, a) {
      if (!Hm(e))
        throw new Error("hydrateRoot(...): Target container is not a DOM element.");
      W1(e), t === void 0 && S("Must provide initial children as second argument to hydrateRoot. Example usage: hydrateRoot(domContainer, <App />)");
      var i = a ?? null, u = a != null && a.hydratedSources || null, s = !1, f = !1, p = "", v = Q1;
      a != null && (a.unstable_strictMode === !0 && (s = !0), a.identifierPrefix !== void 0 && (p = a.identifierPrefix), a.onRecoverableError !== void 0 && (v = a.onRecoverableError));
      var y = b1(t, null, e, Nh, i, s, f, p, v);
      if (bh(y.current, e), qd(e), u)
        for (var g = 0; g < u.length; g++) {
          var b = u[g];
          Hx(y, b);
        }
      return new Fm(y);
    }
    function Hm(e) {
      return !!(e && (e.nodeType === Xr || e.nodeType === ai || e.nodeType === Kl || !V));
    }
    function Yp(e) {
      return !!(e && (e.nodeType === Xr || e.nodeType === ai || e.nodeType === Kl || e.nodeType === An && e.nodeValue === " react-mount-point-unstable "));
    }
    function W1(e) {
      e.nodeType === Xr && e.tagName && e.tagName.toUpperCase() === "BODY" && S("createRoot(): Creating roots directly with document.body is discouraged, since its children are often manipulated by third-party scripts and browser extensions. This may lead to subtle reconciliation issues. Try using a container element created for your app."), lp(e) && (e._reactRootContainer ? S("You are calling ReactDOMClient.createRoot() on a container that was previously passed to ReactDOM.render(). This is not supported.") : S("You are calling ReactDOMClient.createRoot() on a container that has already been passed to createRoot() before. Instead, call root.render() on the existing root instead if you want to update it."));
    }
    var A_ = k.ReactCurrentOwner, G1;
    G1 = function(e) {
      if (e._reactRootContainer && e.nodeType !== An) {
        var t = k1(e._reactRootContainer.current);
        t && t.parentNode !== e && S("render(...): It looks like the React-rendered content of this container was removed without using React. This is not supported and will cause errors. Instead, call ReactDOM.unmountComponentAtNode to empty a container.");
      }
      var a = !!e._reactRootContainer, i = f0(e), u = !!(i && Oo(i));
      u && !a && S("render(...): Replacing React-rendered children with a new root component. If you intended to update the children of this node, you should instead have the existing children update their state and render the new components instead of calling ReactDOM.render."), e.nodeType === Xr && e.tagName && e.tagName.toUpperCase() === "BODY" && S("render(): Rendering components directly into document.body is discouraged, since its children are often manipulated by third-party scripts and browser extensions. This may lead to subtle reconciliation issues. Try rendering into a container element created for your app.");
    };
    function f0(e) {
      return e ? e.nodeType === ai ? e.documentElement : e.firstChild : null;
    }
    function q1() {
    }
    function j_(e, t, a, i, u) {
      if (u) {
        if (typeof i == "function") {
          var s = i;
          i = function() {
            var x = jm(f);
            s.call(x);
          };
        }
        var f = b1(
          t,
          i,
          e,
          Mo,
          null,
          // hydrationCallbacks
          !1,
          // isStrictMode
          !1,
          // concurrentUpdatesByDefaultOverride,
          "",
          // identifierPrefix
          q1
        );
        e._reactRootContainer = f, bh(f.current, e);
        var p = e.nodeType === An ? e.parentNode : e;
        return qd(p), Ou(), f;
      } else {
        for (var v; v = e.lastChild; )
          e.removeChild(v);
        if (typeof i == "function") {
          var y = i;
          i = function() {
            var x = jm(g);
            y.call(x);
          };
        }
        var g = w1(
          e,
          Mo,
          null,
          // hydrationCallbacks
          !1,
          // isStrictMode
          !1,
          // concurrentUpdatesByDefaultOverride,
          "",
          // identifierPrefix
          q1
        );
        e._reactRootContainer = g, bh(g.current, e);
        var b = e.nodeType === An ? e.parentNode : e;
        return qd(b), Ou(function() {
          $p(t, g, a, i);
        }), g;
      }
    }
    function F_(e, t) {
      e !== null && typeof e != "function" && S("%s(...): Expected the last optional `callback` argument to be a function. Instead received: %s.", t, e);
    }
    function Vm(e, t, a, i, u) {
      G1(a), F_(u === void 0 ? null : u, "render");
      var s = a._reactRootContainer, f;
      if (!s)
        f = j_(a, t, e, u, i);
      else {
        if (f = s, typeof u == "function") {
          var p = u;
          u = function() {
            var v = jm(f);
            p.call(v);
          };
        }
        $p(t, f, e, u);
      }
      return jm(f);
    }
    var X1 = !1;
    function H_(e) {
      {
        X1 || (X1 = !0, S("findDOMNode is deprecated and will be removed in the next major release. Instead, add a ref directly to the element you want to reference. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-find-node"));
        var t = A_.current;
        if (t !== null && t.stateNode !== null) {
          var a = t.stateNode._warnedAboutRefsInRender;
          a || S("%s is accessing findDOMNode inside its render(). render() should be a pure function of props and state. It should never access something that requires stale data from the previous render, such as refs. Move this logic to componentDidMount and componentDidUpdate instead.", Ct(t.type) || "A component"), t.stateNode._warnedAboutRefsInRender = !0;
        }
      }
      return e == null ? null : e.nodeType === Xr ? e : T_(e, "findDOMNode");
    }
    function V_(e, t, a) {
      if (S("ReactDOM.hydrate is no longer supported in React 18. Use hydrateRoot instead. Until you switch to the new API, your app will behave as if it's running React 17. Learn more: https://reactjs.org/link/switch-to-createroot"), !Yp(t))
        throw new Error("Target container is not a DOM element.");
      {
        var i = lp(t) && t._reactRootContainer === void 0;
        i && S("You are calling ReactDOM.hydrate() on a container that was previously passed to ReactDOMClient.createRoot(). This is not supported. Did you mean to call hydrateRoot(container, element)?");
      }
      return Vm(null, e, t, !0, a);
    }
    function P_(e, t, a) {
      if (S("ReactDOM.render is no longer supported in React 18. Use createRoot instead. Until you switch to the new API, your app will behave as if it's running React 17. Learn more: https://reactjs.org/link/switch-to-createroot"), !Yp(t))
        throw new Error("Target container is not a DOM element.");
      {
        var i = lp(t) && t._reactRootContainer === void 0;
        i && S("You are calling ReactDOM.render() on a container that was previously passed to ReactDOMClient.createRoot(). This is not supported. Did you mean to call root.render(element)?");
      }
      return Vm(null, e, t, !1, a);
    }
    function B_(e, t, a, i) {
      if (S("ReactDOM.unstable_renderSubtreeIntoContainer() is no longer supported in React 18. Consider using a portal instead. Until you switch to the createRoot API, your app will behave as if it's running React 17. Learn more: https://reactjs.org/link/switch-to-createroot"), !Yp(a))
        throw new Error("Target container is not a DOM element.");
      if (e == null || !ss(e))
        throw new Error("parentComponent must be a valid React Component");
      return Vm(e, t, a, !1, i);
    }
    var K1 = !1;
    function $_(e) {
      if (K1 || (K1 = !0, S("unmountComponentAtNode is deprecated and will be removed in the next major release. Switch to the createRoot API. Learn more: https://reactjs.org/link/switch-to-createroot")), !Yp(e))
        throw new Error("unmountComponentAtNode(...): Target container is not a DOM element.");
      {
        var t = lp(e) && e._reactRootContainer === void 0;
        t && S("You are calling ReactDOM.unmountComponentAtNode() on a container that was previously passed to ReactDOMClient.createRoot(). This is not supported. Did you mean to call root.unmount()?");
      }
      if (e._reactRootContainer) {
        {
          var a = f0(e), i = a && !Oo(a);
          i && S("unmountComponentAtNode(): The node you're attempting to unmount was rendered by another copy of React.");
        }
        return Ou(function() {
          Vm(null, null, e, !1, function() {
            e._reactRootContainer = null, Q0(e);
          });
        }), !0;
      } else {
        {
          var u = f0(e), s = !!(u && Oo(u)), f = e.nodeType === Xr && Yp(e.parentNode) && !!e.parentNode._reactRootContainer;
          s && S("unmountComponentAtNode(): The node you're attempting to unmount was rendered by React and is not a top-level container. %s", f ? "You may have accidentally passed in a React root node instead of its container." : "Instead, have the parent component update its state and rerender in order to remove this component.");
        }
        return !1;
      }
    }
    mo(x_), cy(w_), Gc(b_), Gv(Pa), qv(Tr), (typeof Map != "function" || // $FlowIssue Flow incorrectly thinks Map has no prototype
    Map.prototype == null || typeof Map.prototype.forEach != "function" || typeof Set != "function" || // $FlowIssue Flow incorrectly thinks Set has no prototype
    Set.prototype == null || typeof Set.prototype.clear != "function" || typeof Set.prototype.forEach != "function") && S("React depends on Map and Set built-in types. Make sure that you load a polyfill in older browsers. https://reactjs.org/link/react-polyfills"), xv(IR), fc(BS, Ub, Ou);
    function Y_(e, t) {
      var a = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : null;
      if (!Hm(t))
        throw new Error("Target container is not a DOM element.");
      return R_(e, t, null, a);
    }
    function I_(e, t, a, i) {
      return B_(e, t, a, i);
    }
    var d0 = {
      usingClientEntryPoint: !1,
      // Keep in sync with ReactTestUtils.js.
      // This is an array for better minification.
      Events: [Oo, gf, _h, cc, ls, BS]
    };
    function Q_(e, t) {
      return d0.usingClientEntryPoint || S('You are importing createRoot from "react-dom" which is not supported. You should instead import it from "react-dom/client".'), N_(e, t);
    }
    function W_(e, t, a) {
      return d0.usingClientEntryPoint || S('You are importing hydrateRoot from "react-dom" which is not supported. You should instead import it from "react-dom/client".'), U_(e, t, a);
    }
    function G_(e) {
      return a1() && S("flushSync was called from inside a lifecycle method. React cannot flush when React is already rendering. Consider moving this call to a scheduler task or micro task."), Ou(e);
    }
    var q_ = M_({
      findFiberByHostInstance: As,
      bundleType: 1,
      version: i0,
      rendererPackageName: "react-dom"
    });
    if (!q_ && vn && window.top === window.self && (navigator.userAgent.indexOf("Chrome") > -1 && navigator.userAgent.indexOf("Edge") === -1 || navigator.userAgent.indexOf("Firefox") > -1)) {
      var Z1 = window.location.protocol;
      /^(https?|file):$/.test(Z1) && console.info("%cDownload the React DevTools for a better development experience: https://reactjs.org/link/react-devtools" + (Z1 === "file:" ? `
You might need to use a local HTTP server (instead of file://): https://reactjs.org/link/react-devtools-faq` : ""), "font-weight:bold");
    }
    Za.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = d0, Za.createPortal = Y_, Za.createRoot = Q_, Za.findDOMNode = H_, Za.flushSync = G_, Za.hydrate = V_, Za.hydrateRoot = W_, Za.render = P_, Za.unmountComponentAtNode = $_, Za.unstable_batchedUpdates = BS, Za.unstable_renderSubtreeIntoContainer = I_, Za.version = i0, typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop(new Error());
  }()), Za;
}
function sR() {
  if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function")) {
    if (process.env.NODE_ENV !== "production")
      throw new Error("^_^");
    try {
      __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(sR);
    } catch (Q) {
      console.error(Q);
    }
  }
}
process.env.NODE_ENV === "production" ? (sR(), y0.exports = ok()) : y0.exports = sk();
var ck = y0.exports, Gp = ck;
if (process.env.NODE_ENV === "production")
  Kp.createRoot = Gp.createRoot, Kp.hydrateRoot = Gp.hydrateRoot;
else {
  var $m = Gp.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;
  Kp.createRoot = function(Q, B) {
    $m.usingClientEntryPoint = !0;
    try {
      return Gp.createRoot(Q, B);
    } finally {
      $m.usingClientEntryPoint = !1;
    }
  }, Kp.hydrateRoot = function(Q, B, k) {
    $m.usingClientEntryPoint = !0;
    try {
      return Gp.hydrateRoot(Q, B, k);
    } finally {
      $m.usingClientEntryPoint = !1;
    }
  };
}
const qp = ({ title: Q, value: B, icon: k }) => /* @__PURE__ */ De.jsxs("div", { className: "bg-white dark:bg-gray-800 rounded-lg shadow p-4 flex items-center", children: [
  /* @__PURE__ */ De.jsx("div", { className: "text-3xl mr-4", children: k }),
  /* @__PURE__ */ De.jsxs("div", { children: [
    /* @__PURE__ */ De.jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: Q }),
    /* @__PURE__ */ De.jsx("p", { className: "text-2xl font-semibold text-gray-900 dark:text-white", children: B })
  ] })
] }), fk = ({ devices: Q, setActiveView: B }) => /* @__PURE__ */ De.jsx("div", { className: "bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden", children: /* @__PURE__ */ De.jsxs("table", { className: "min-w-full", children: [
  /* @__PURE__ */ De.jsx("thead", { className: "bg-gray-50 dark:bg-gray-700", children: /* @__PURE__ */ De.jsxs("tr", { children: [
    /* @__PURE__ */ De.jsx("th", { className: "px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider", children: "Name" }),
    /* @__PURE__ */ De.jsx("th", { className: "px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider", children: "Status" }),
    /* @__PURE__ */ De.jsx("th", { className: "px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider", children: "Model" }),
    /* @__PURE__ */ De.jsx("th", { className: "px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider", children: "MAC Address" })
  ] }) }),
  /* @__PURE__ */ De.jsx("tbody", { className: "divide-y divide-gray-200 dark:divide-gray-600", children: Q.map((k) => /* @__PURE__ */ De.jsxs("tr", { onClick: () => B({ view: "device", deviceId: k.serial }), className: "cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700", children: [
    /* @__PURE__ */ De.jsx("td", { className: "px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white", children: k.name || k.mac }),
    /* @__PURE__ */ De.jsx("td", { className: "px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300", children: k.status }),
    /* @__PURE__ */ De.jsx("td", { className: "px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300", children: k.model }),
    /* @__PURE__ */ De.jsx("td", { className: "px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300", children: k.mac })
  ] }, k.serial)) })
] }) }), dk = ({ setActiveView: Q, data: B }) => {
  if (!B)
    return /* @__PURE__ */ De.jsx("div", { children: "Loading dashboard..." });
  const { devices: k = [], ssids: Ze = [], networks: Dt = [] } = B, $e = {
    totalDevices: k.length,
    wirelessAps: k.filter((S) => {
      var ut;
      return (ut = S.model) == null ? void 0 : ut.startsWith("MR");
    }).length,
    switches: k.filter((S) => {
      var ut;
      return (ut = S.model) == null ? void 0 : ut.startsWith("MS");
    }).length,
    cameras: k.filter((S) => {
      var ut;
      return (ut = S.model) == null ? void 0 : ut.startsWith("MV");
    }).length,
    ssids: Ze.length
  };
  return /* @__PURE__ */ De.jsxs("div", { children: [
    /* @__PURE__ */ De.jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8", children: [
      /* @__PURE__ */ De.jsx(qp, { title: "Total Devices", value: $e.totalDevices, icon: "📱" }),
      /* @__PURE__ */ De.jsx(qp, { title: "Wireless APs", value: $e.wirelessAps, icon: "📡" }),
      /* @__PURE__ */ De.jsx(qp, { title: "Switches", value: $e.switches, icon: "🔄" }),
      /* @__PURE__ */ De.jsx(qp, { title: "Cameras", value: $e.cameras, icon: "📹" }),
      /* @__PURE__ */ De.jsx(qp, { title: "Virtual SSIDs", value: $e.ssids, icon: "📶" })
    ] }),
    /* @__PURE__ */ De.jsx("h2", { className: "text-xl font-semibold mb-4", children: "Networks" }),
    /* @__PURE__ */ De.jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: Dt.map((S) => /* @__PURE__ */ De.jsx(
      "button",
      {
        "data-testid": "network-card",
        className: "bg-white dark:bg-gray-800 rounded-lg shadow p-4 cursor-pointer text-left",
        onClick: () => Q({ view: "network", networkId: S.id }),
        children: /* @__PURE__ */ De.jsx("p", { className: "font-medium text-gray-900 dark:text-white", children: S.name })
      },
      S.id
    )) }),
    /* @__PURE__ */ De.jsx("h2", { className: "text-xl font-semibold mb-4 mt-8", children: "All Devices" }),
    /* @__PURE__ */ De.jsx(fk, { devices: k, setActiveView: Q })
  ] });
}, pk = ({ activeView: Q, setActiveView: B, data: k }) => {
  const Ze = k.devices.find((Dt) => Dt.serial === Q.deviceId);
  return Ze ? /* @__PURE__ */ De.jsxs("div", { children: [
    /* @__PURE__ */ De.jsx("button", { onClick: () => B({ view: "dashboard" }), className: "mb-4", children: "← Back to Dashboard" }),
    /* @__PURE__ */ De.jsx("h2", { className: "text-xl font-semibold mb-4", children: "Device Details" }),
    /* @__PURE__ */ De.jsxs("p", { children: [
      "Name: ",
      Ze.name || Ze.mac
    ] }),
    /* @__PURE__ */ De.jsxs("p", { children: [
      "Status: ",
      Ze.status
    ] }),
    /* @__PURE__ */ De.jsxs("p", { children: [
      "Model: ",
      Ze.model
    ] }),
    /* @__PURE__ */ De.jsxs("p", { children: [
      "MAC Address: ",
      Ze.mac
    ] }),
    /* @__PURE__ */ De.jsxs("p", { children: [
      "Serial: ",
      Ze.serial
    ] })
  ] }) : /* @__PURE__ */ De.jsx("div", { children: "Device not found" });
}, vk = ({ activeView: Q, setActiveView: B, data: k }) => {
  const Ze = k.networks.find((Dt) => Dt.id === Q.networkId);
  return Ze ? /* @__PURE__ */ De.jsxs("div", { children: [
    /* @__PURE__ */ De.jsx("button", { onClick: () => B({ view: "dashboard" }), className: "mb-4", children: "← Back to Dashboard" }),
    /* @__PURE__ */ De.jsx("h2", { className: "text-xl font-semibold mb-4", children: "Network Information" }),
    /* @__PURE__ */ De.jsxs("p", { children: [
      "Name: ",
      Ze.name
    ] }),
    /* @__PURE__ */ De.jsxs("p", { children: [
      "ID: ",
      Ze.id
    ] }),
    /* @__PURE__ */ De.jsxs("p", { children: [
      "Product Types: ",
      Ze.product_types.join(", ")
    ] })
  ] }) : /* @__PURE__ */ De.jsx("div", { children: "Network not found" });
}, hk = ({ hass: Q, config_entry_id: B }) => {
  const [k, Ze] = Ql.useState(null), [Dt, $e] = Ql.useState(!0), [S, ut] = Ql.useState(null), [de, se] = Ql.useState({ view: "dashboard" });
  if (Ql.useEffect(() => {
    if (!Q || !Q.connection) {
      ut("Home Assistant connection object not found."), $e(!1);
      return;
    }
    (async () => {
      try {
        const pe = await Q.connection.sendMessagePromise({
          type: "meraki_ha/get_config",
          config_entry_id: B
        });
        Ze(pe);
      } catch (pe) {
        console.error("Error fetching Meraki data:", pe), ut(`Failed to fetch Meraki data: ${pe.message || "Unknown error"}`);
      } finally {
        $e(!1);
      }
    })();
  }, [Q, B]), Dt)
    return /* @__PURE__ */ De.jsx("div", { className: "p-4", children: "Loading..." });
  if (S)
    return /* @__PURE__ */ De.jsxs("div", { className: "p-4 text-red-500", children: [
      "Error: ",
      S
    ] });
  const nt = () => {
    switch (de.view) {
      case "dashboard":
        return /* @__PURE__ */ De.jsx(dk, { setActiveView: se, data: k });
      case "device":
        return /* @__PURE__ */ De.jsx(pk, { activeView: de, setActiveView: se, data: k });
      case "network":
        return /* @__PURE__ */ De.jsx(vk, { activeView: de, setActiveView: se, data: k });
      default:
        return /* @__PURE__ */ De.jsx("div", { children: "Unknown view" });
    }
  };
  return /* @__PURE__ */ De.jsxs("div", { className: "p-4", children: [
    /* @__PURE__ */ De.jsx("h1", { className: "text-2xl font-bold mb-4", children: "Meraki Control" }),
    nt()
  ] });
};
class mk extends HTMLElement {
  constructor() {
    super(...arguments);
    Pm(this, "_root");
    Pm(this, "_hass");
    Pm(this, "_panel");
  }
  connectedCallback() {
    this._root = Kp.createRoot(this), this._render();
  }
  disconnectedCallback() {
    this._root && (this._root.unmount(), this._root = void 0);
  }
  set hass(k) {
    this._hass = k, this._render();
  }
  set panel(k) {
    this._panel = k, this._render();
  }
  _render() {
    !this._root || !this._hass || !this._panel || this._root.render(
      /* @__PURE__ */ De.jsx(rk.StrictMode, { children: /* @__PURE__ */ De.jsx(hk, { hass: this._hass, config_entry_id: this._panel.config.config_entry_id }) })
    );
  }
}
customElements.define("meraki-panel", mk);
