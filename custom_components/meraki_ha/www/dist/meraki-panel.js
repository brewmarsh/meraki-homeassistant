var gr = Object.defineProperty;
var xr = (u, l, i) => l in u ? gr(u, l, { enumerable: !0, configurable: !0, writable: !0, value: i }) : u[l] = i;
var K = (u, l, i) => (xr(u, typeof l != "symbol" ? l + "" : l, i), i);
import se, { useState as G, useEffect as yr } from "react";
import br from "react-dom";
var ie = { exports: {} }, M = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ne;
function _r() {
  if (Ne)
    return M;
  Ne = 1;
  var u = se, l = Symbol.for("react.element"), i = Symbol.for("react.fragment"), d = Object.prototype.hasOwnProperty, R = u.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, E = { key: !0, ref: !0, __self: !0, __source: !0 };
  function g(p, m, k) {
    var y, T = {}, j = null, Y = null;
    k !== void 0 && (j = "" + k), m.key !== void 0 && (j = "" + m.key), m.ref !== void 0 && (Y = m.ref);
    for (y in m)
      d.call(m, y) && !E.hasOwnProperty(y) && (T[y] = m[y]);
    if (p && p.defaultProps)
      for (y in m = p.defaultProps, m)
        T[y] === void 0 && (T[y] = m[y]);
    return { $$typeof: l, type: p, key: j, ref: Y, props: T, _owner: R.current };
  }
  return M.Fragment = i, M.jsx = g, M.jsxs = g, M;
}
var W = {};
/**
 * @license React
 * react-jsx-runtime.development.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var De;
function Er() {
  return De || (De = 1, process.env.NODE_ENV !== "production" && function() {
    var u = se, l = Symbol.for("react.element"), i = Symbol.for("react.portal"), d = Symbol.for("react.fragment"), R = Symbol.for("react.strict_mode"), E = Symbol.for("react.profiler"), g = Symbol.for("react.provider"), p = Symbol.for("react.context"), m = Symbol.for("react.forward_ref"), k = Symbol.for("react.suspense"), y = Symbol.for("react.suspense_list"), T = Symbol.for("react.memo"), j = Symbol.for("react.lazy"), Y = Symbol.for("react.offscreen"), oe = Symbol.iterator, Ae = "@@iterator";
    function Fe(e) {
      if (e === null || typeof e != "object")
        return null;
      var r = oe && e[oe] || e[Ae];
      return typeof r == "function" ? r : null;
    }
    var P = u.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;
    function x(e) {
      {
        for (var r = arguments.length, t = new Array(r > 1 ? r - 1 : 0), a = 1; a < r; a++)
          t[a - 1] = arguments[a];
        Ie("error", e, t);
      }
    }
    function Ie(e, r, t) {
      {
        var a = P.ReactDebugCurrentFrame, c = a.getStackAddendum();
        c !== "" && (r += "%s", t = t.concat([c]));
        var f = t.map(function(o) {
          return String(o);
        });
        f.unshift("Warning: " + r), Function.prototype.apply.call(console[e], console, f);
      }
    }
    var Me = !1, We = !1, $e = !1, Le = !1, Ve = !1, le;
    le = Symbol.for("react.module.reference");
    function Ye(e) {
      return !!(typeof e == "string" || typeof e == "function" || e === d || e === E || Ve || e === R || e === k || e === y || Le || e === Y || Me || We || $e || typeof e == "object" && e !== null && (e.$$typeof === j || e.$$typeof === T || e.$$typeof === g || e.$$typeof === p || e.$$typeof === m || // This needs to include all possible module reference object
      // types supported by any Flight configuration anywhere since
      // we don't know which Flight build this will end up being used
      // with.
      e.$$typeof === le || e.getModuleId !== void 0));
    }
    function Ue(e, r, t) {
      var a = e.displayName;
      if (a)
        return a;
      var c = r.displayName || r.name || "";
      return c !== "" ? t + "(" + c + ")" : t;
    }
    function ce(e) {
      return e.displayName || "Context";
    }
    function C(e) {
      if (e == null)
        return null;
      if (typeof e.tag == "number" && x("Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue."), typeof e == "function")
        return e.displayName || e.name || null;
      if (typeof e == "string")
        return e;
      switch (e) {
        case d:
          return "Fragment";
        case i:
          return "Portal";
        case E:
          return "Profiler";
        case R:
          return "StrictMode";
        case k:
          return "Suspense";
        case y:
          return "SuspenseList";
      }
      if (typeof e == "object")
        switch (e.$$typeof) {
          case p:
            var r = e;
            return ce(r) + ".Consumer";
          case g:
            var t = e;
            return ce(t._context) + ".Provider";
          case m:
            return Ue(e, e.render, "ForwardRef");
          case T:
            var a = e.displayName || null;
            return a !== null ? a : C(e.type) || "Memo";
          case j: {
            var c = e, f = c._payload, o = c._init;
            try {
              return C(o(f));
            } catch {
              return null;
            }
          }
        }
      return null;
    }
    var S = Object.assign, A = 0, ue, fe, de, ve, he, pe, me;
    function ge() {
    }
    ge.__reactDisabledLog = !0;
    function Be() {
      {
        if (A === 0) {
          ue = console.log, fe = console.info, de = console.warn, ve = console.error, he = console.group, pe = console.groupCollapsed, me = console.groupEnd;
          var e = {
            configurable: !0,
            enumerable: !0,
            value: ge,
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
        A++;
      }
    }
    function qe() {
      {
        if (A--, A === 0) {
          var e = {
            configurable: !0,
            enumerable: !0,
            writable: !0
          };
          Object.defineProperties(console, {
            log: S({}, e, {
              value: ue
            }),
            info: S({}, e, {
              value: fe
            }),
            warn: S({}, e, {
              value: de
            }),
            error: S({}, e, {
              value: ve
            }),
            group: S({}, e, {
              value: he
            }),
            groupCollapsed: S({}, e, {
              value: pe
            }),
            groupEnd: S({}, e, {
              value: me
            })
          });
        }
        A < 0 && x("disabledDepth fell below zero. This is a bug in React. Please file an issue.");
      }
    }
    var H = P.ReactCurrentDispatcher, X;
    function U(e, r, t) {
      {
        if (X === void 0)
          try {
            throw Error();
          } catch (c) {
            var a = c.stack.trim().match(/\n( *(at )?)/);
            X = a && a[1] || "";
          }
        return `
` + X + e;
      }
    }
    var Z = !1, B;
    {
      var Je = typeof WeakMap == "function" ? WeakMap : Map;
      B = new Je();
    }
    function xe(e, r) {
      if (!e || Z)
        return "";
      {
        var t = B.get(e);
        if (t !== void 0)
          return t;
      }
      var a;
      Z = !0;
      var c = Error.prepareStackTrace;
      Error.prepareStackTrace = void 0;
      var f;
      f = H.current, H.current = null, Be();
      try {
        if (r) {
          var o = function() {
            throw Error();
          };
          if (Object.defineProperty(o.prototype, "props", {
            set: function() {
              throw Error();
            }
          }), typeof Reflect == "object" && Reflect.construct) {
            try {
              Reflect.construct(o, []);
            } catch (_) {
              a = _;
            }
            Reflect.construct(e, [], o);
          } else {
            try {
              o.call();
            } catch (_) {
              a = _;
            }
            e.call(o.prototype);
          }
        } else {
          try {
            throw Error();
          } catch (_) {
            a = _;
          }
          e();
        }
      } catch (_) {
        if (_ && a && typeof _.stack == "string") {
          for (var s = _.stack.split(`
`), b = a.stack.split(`
`), v = s.length - 1, h = b.length - 1; v >= 1 && h >= 0 && s[v] !== b[h]; )
            h--;
          for (; v >= 1 && h >= 0; v--, h--)
            if (s[v] !== b[h]) {
              if (v !== 1 || h !== 1)
                do
                  if (v--, h--, h < 0 || s[v] !== b[h]) {
                    var w = `
` + s[v].replace(" at new ", " at ");
                    return e.displayName && w.includes("<anonymous>") && (w = w.replace("<anonymous>", e.displayName)), typeof e == "function" && B.set(e, w), w;
                  }
                while (v >= 1 && h >= 0);
              break;
            }
        }
      } finally {
        Z = !1, H.current = f, qe(), Error.prepareStackTrace = c;
      }
      var D = e ? e.displayName || e.name : "", O = D ? U(D) : "";
      return typeof e == "function" && B.set(e, O), O;
    }
    function Ke(e, r, t) {
      return xe(e, !1);
    }
    function Ge(e) {
      var r = e.prototype;
      return !!(r && r.isReactComponent);
    }
    function q(e, r, t) {
      if (e == null)
        return "";
      if (typeof e == "function")
        return xe(e, Ge(e));
      if (typeof e == "string")
        return U(e);
      switch (e) {
        case k:
          return U("Suspense");
        case y:
          return U("SuspenseList");
      }
      if (typeof e == "object")
        switch (e.$$typeof) {
          case m:
            return Ke(e.render);
          case T:
            return q(e.type, r, t);
          case j: {
            var a = e, c = a._payload, f = a._init;
            try {
              return q(f(c), r, t);
            } catch {
            }
          }
        }
      return "";
    }
    var F = Object.prototype.hasOwnProperty, ye = {}, be = P.ReactDebugCurrentFrame;
    function J(e) {
      if (e) {
        var r = e._owner, t = q(e.type, e._source, r ? r.type : null);
        be.setExtraStackFrame(t);
      } else
        be.setExtraStackFrame(null);
    }
    function ze(e, r, t, a, c) {
      {
        var f = Function.call.bind(F);
        for (var o in e)
          if (f(e, o)) {
            var s = void 0;
            try {
              if (typeof e[o] != "function") {
                var b = Error((a || "React class") + ": " + t + " type `" + o + "` is invalid; it must be a function, usually from the `prop-types` package, but received `" + typeof e[o] + "`.This often happens because of typos such as `PropTypes.function` instead of `PropTypes.func`.");
                throw b.name = "Invariant Violation", b;
              }
              s = e[o](r, o, a, t, null, "SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED");
            } catch (v) {
              s = v;
            }
            s && !(s instanceof Error) && (J(c), x("%s: type specification of %s `%s` is invalid; the type checker function must return `null` or an `Error` but returned a %s. You may have forgotten to pass an argument to the type checker creator (arrayOf, instanceOf, objectOf, oneOf, oneOfType, and shape all require an argument).", a || "React class", t, o, typeof s), J(null)), s instanceof Error && !(s.message in ye) && (ye[s.message] = !0, J(c), x("Failed %s type: %s", t, s.message), J(null));
          }
      }
    }
    var He = Array.isArray;
    function Q(e) {
      return He(e);
    }
    function Xe(e) {
      {
        var r = typeof Symbol == "function" && Symbol.toStringTag, t = r && e[Symbol.toStringTag] || e.constructor.name || "Object";
        return t;
      }
    }
    function Ze(e) {
      try {
        return _e(e), !1;
      } catch {
        return !0;
      }
    }
    function _e(e) {
      return "" + e;
    }
    function Ee(e) {
      if (Ze(e))
        return x("The provided key is an unsupported type %s. This value must be coerced to a string before before using it here.", Xe(e)), _e(e);
    }
    var I = P.ReactCurrentOwner, Qe = {
      key: !0,
      ref: !0,
      __self: !0,
      __source: !0
    }, Re, je, ee;
    ee = {};
    function er(e) {
      if (F.call(e, "ref")) {
        var r = Object.getOwnPropertyDescriptor(e, "ref").get;
        if (r && r.isReactWarning)
          return !1;
      }
      return e.ref !== void 0;
    }
    function rr(e) {
      if (F.call(e, "key")) {
        var r = Object.getOwnPropertyDescriptor(e, "key").get;
        if (r && r.isReactWarning)
          return !1;
      }
      return e.key !== void 0;
    }
    function tr(e, r) {
      if (typeof e.ref == "string" && I.current && r && I.current.stateNode !== r) {
        var t = C(I.current.type);
        ee[t] || (x('Component "%s" contains the string ref "%s". Support for string refs will be removed in a future major release. This case cannot be automatically converted to an arrow function. We ask you to manually fix this case by using useRef() or createRef() instead. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-string-ref', C(I.current.type), e.ref), ee[t] = !0);
      }
    }
    function nr(e, r) {
      {
        var t = function() {
          Re || (Re = !0, x("%s: `key` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://reactjs.org/link/special-props)", r));
        };
        t.isReactWarning = !0, Object.defineProperty(e, "key", {
          get: t,
          configurable: !0
        });
      }
    }
    function ar(e, r) {
      {
        var t = function() {
          je || (je = !0, x("%s: `ref` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://reactjs.org/link/special-props)", r));
        };
        t.isReactWarning = !0, Object.defineProperty(e, "ref", {
          get: t,
          configurable: !0
        });
      }
    }
    var ir = function(e, r, t, a, c, f, o) {
      var s = {
        // This tag allows us to uniquely identify this as a React Element
        $$typeof: l,
        // Built-in properties that belong on the element
        type: e,
        key: r,
        ref: t,
        props: o,
        // Record the component responsible for creating this element.
        _owner: f
      };
      return s._store = {}, Object.defineProperty(s._store, "validated", {
        configurable: !1,
        enumerable: !1,
        writable: !0,
        value: !1
      }), Object.defineProperty(s, "_self", {
        configurable: !1,
        enumerable: !1,
        writable: !1,
        value: a
      }), Object.defineProperty(s, "_source", {
        configurable: !1,
        enumerable: !1,
        writable: !1,
        value: c
      }), Object.freeze && (Object.freeze(s.props), Object.freeze(s)), s;
    };
    function sr(e, r, t, a, c) {
      {
        var f, o = {}, s = null, b = null;
        t !== void 0 && (Ee(t), s = "" + t), rr(r) && (Ee(r.key), s = "" + r.key), er(r) && (b = r.ref, tr(r, c));
        for (f in r)
          F.call(r, f) && !Qe.hasOwnProperty(f) && (o[f] = r[f]);
        if (e && e.defaultProps) {
          var v = e.defaultProps;
          for (f in v)
            o[f] === void 0 && (o[f] = v[f]);
        }
        if (s || b) {
          var h = typeof e == "function" ? e.displayName || e.name || "Unknown" : e;
          s && nr(o, h), b && ar(o, h);
        }
        return ir(e, s, b, c, a, I.current, o);
      }
    }
    var re = P.ReactCurrentOwner, we = P.ReactDebugCurrentFrame;
    function N(e) {
      if (e) {
        var r = e._owner, t = q(e.type, e._source, r ? r.type : null);
        we.setExtraStackFrame(t);
      } else
        we.setExtraStackFrame(null);
    }
    var te;
    te = !1;
    function ne(e) {
      return typeof e == "object" && e !== null && e.$$typeof === l;
    }
    function ke() {
      {
        if (re.current) {
          var e = C(re.current.type);
          if (e)
            return `

Check the render method of \`` + e + "`.";
        }
        return "";
      }
    }
    function or(e) {
      {
        if (e !== void 0) {
          var r = e.fileName.replace(/^.*[\\\/]/, ""), t = e.lineNumber;
          return `

Check your code at ` + r + ":" + t + ".";
        }
        return "";
      }
    }
    var Te = {};
    function lr(e) {
      {
        var r = ke();
        if (!r) {
          var t = typeof e == "string" ? e : e.displayName || e.name;
          t && (r = `

Check the top-level render call using <` + t + ">.");
        }
        return r;
      }
    }
    function Ce(e, r) {
      {
        if (!e._store || e._store.validated || e.key != null)
          return;
        e._store.validated = !0;
        var t = lr(r);
        if (Te[t])
          return;
        Te[t] = !0;
        var a = "";
        e && e._owner && e._owner !== re.current && (a = " It was passed a child from " + C(e._owner.type) + "."), N(e), x('Each child in a list should have a unique "key" prop.%s%s See https://reactjs.org/link/warning-keys for more information.', t, a), N(null);
      }
    }
    function Se(e, r) {
      {
        if (typeof e != "object")
          return;
        if (Q(e))
          for (var t = 0; t < e.length; t++) {
            var a = e[t];
            ne(a) && Ce(a, r);
          }
        else if (ne(e))
          e._store && (e._store.validated = !0);
        else if (e) {
          var c = Fe(e);
          if (typeof c == "function" && c !== e.entries)
            for (var f = c.call(e), o; !(o = f.next()).done; )
              ne(o.value) && Ce(o.value, r);
        }
      }
    }
    function cr(e) {
      {
        var r = e.type;
        if (r == null || typeof r == "string")
          return;
        var t;
        if (typeof r == "function")
          t = r.propTypes;
        else if (typeof r == "object" && (r.$$typeof === m || // Note: Memo only checks outer props here.
        // Inner props are checked in the reconciler.
        r.$$typeof === T))
          t = r.propTypes;
        else
          return;
        if (t) {
          var a = C(r);
          ze(t, e.props, "prop", a, e);
        } else if (r.PropTypes !== void 0 && !te) {
          te = !0;
          var c = C(r);
          x("Component %s declared `PropTypes` instead of `propTypes`. Did you misspell the property assignment?", c || "Unknown");
        }
        typeof r.getDefaultProps == "function" && !r.getDefaultProps.isReactClassApproved && x("getDefaultProps is only used on classic React.createClass definitions. Use a static property named `defaultProps` instead.");
      }
    }
    function ur(e) {
      {
        for (var r = Object.keys(e.props), t = 0; t < r.length; t++) {
          var a = r[t];
          if (a !== "children" && a !== "key") {
            N(e), x("Invalid prop `%s` supplied to `React.Fragment`. React.Fragment can only have `key` and `children` props.", a), N(null);
            break;
          }
        }
        e.ref !== null && (N(e), x("Invalid attribute `ref` supplied to `React.Fragment`."), N(null));
      }
    }
    var Oe = {};
    function Pe(e, r, t, a, c, f) {
      {
        var o = Ye(e);
        if (!o) {
          var s = "";
          (e === void 0 || typeof e == "object" && e !== null && Object.keys(e).length === 0) && (s += " You likely forgot to export your component from the file it's defined in, or you might have mixed up default and named imports.");
          var b = or(c);
          b ? s += b : s += ke();
          var v;
          e === null ? v = "null" : Q(e) ? v = "array" : e !== void 0 && e.$$typeof === l ? (v = "<" + (C(e.type) || "Unknown") + " />", s = " Did you accidentally export a JSX literal instead of a component?") : v = typeof e, x("React.jsx: type is invalid -- expected a string (for built-in components) or a class/function (for composite components) but got: %s.%s", v, s);
        }
        var h = sr(e, r, t, c, f);
        if (h == null)
          return h;
        if (o) {
          var w = r.children;
          if (w !== void 0)
            if (a)
              if (Q(w)) {
                for (var D = 0; D < w.length; D++)
                  Se(w[D], e);
                Object.freeze && Object.freeze(w);
              } else
                x("React.jsx: Static children should always be an array. You are likely explicitly calling React.jsxs or React.jsxDEV. Use the Babel transform instead.");
            else
              Se(w, e);
        }
        if (F.call(r, "key")) {
          var O = C(e), _ = Object.keys(r).filter(function(mr) {
            return mr !== "key";
          }), ae = _.length > 0 ? "{key: someKey, " + _.join(": ..., ") + ": ...}" : "{key: someKey}";
          if (!Oe[O + ae]) {
            var pr = _.length > 0 ? "{" + _.join(": ..., ") + ": ...}" : "{}";
            x(`A props object containing a "key" prop is being spread into JSX:
  let props = %s;
  <%s {...props} />
React keys must be passed directly to JSX without using spread:
  let props = %s;
  <%s key={someKey} {...props} />`, ae, O, pr, O), Oe[O + ae] = !0;
          }
        }
        return e === d ? ur(h) : cr(h), h;
      }
    }
    function fr(e, r, t) {
      return Pe(e, r, t, !0);
    }
    function dr(e, r, t) {
      return Pe(e, r, t, !1);
    }
    var vr = dr, hr = fr;
    W.Fragment = d, W.jsx = vr, W.jsxs = hr;
  }()), W;
}
process.env.NODE_ENV === "production" ? ie.exports = _r() : ie.exports = Er();
var n = ie.exports, V = {}, $ = br;
if (process.env.NODE_ENV === "production")
  V.createRoot = $.createRoot, V.hydrateRoot = $.hydrateRoot;
else {
  var z = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;
  V.createRoot = function(u, l) {
    z.usingClientEntryPoint = !0;
    try {
      return $.createRoot(u, l);
    } finally {
      z.usingClientEntryPoint = !1;
    }
  }, V.hydrateRoot = function(u, l, i) {
    z.usingClientEntryPoint = !0;
    try {
      return $.hydrateRoot(u, l, i);
    } finally {
      z.usingClientEntryPoint = !1;
    }
  };
}
const L = ({ title: u, value: l, icon: i }) => /* @__PURE__ */ n.jsxs("div", { className: "bg-white dark:bg-gray-800 rounded-lg shadow p-4 flex items-center", children: [
  /* @__PURE__ */ n.jsx("div", { className: "text-3xl mr-4", children: i }),
  /* @__PURE__ */ n.jsxs("div", { children: [
    /* @__PURE__ */ n.jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: u }),
    /* @__PURE__ */ n.jsx("p", { className: "text-2xl font-semibold text-gray-900 dark:text-white", children: l })
  ] })
] }), Rr = ({ devices: u, setActiveView: l }) => /* @__PURE__ */ n.jsx("div", { className: "bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden", children: /* @__PURE__ */ n.jsxs("table", { className: "min-w-full", children: [
  /* @__PURE__ */ n.jsx("thead", { className: "bg-gray-50 dark:bg-gray-700", children: /* @__PURE__ */ n.jsxs("tr", { children: [
    /* @__PURE__ */ n.jsx("th", { className: "px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider", children: "Name" }),
    /* @__PURE__ */ n.jsx("th", { className: "px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider", children: "Status" }),
    /* @__PURE__ */ n.jsx("th", { className: "px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider", children: "Model" }),
    /* @__PURE__ */ n.jsx("th", { className: "px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider", children: "MAC Address" })
  ] }) }),
  /* @__PURE__ */ n.jsx("tbody", { className: "divide-y divide-gray-200 dark:divide-gray-600", children: u.map((i) => /* @__PURE__ */ n.jsxs("tr", { onClick: () => l({ view: "device", deviceId: i.serial }), className: "cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700", children: [
    /* @__PURE__ */ n.jsx("td", { className: "px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white", children: i.name || i.mac }),
    /* @__PURE__ */ n.jsx("td", { className: "px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300", children: i.status }),
    /* @__PURE__ */ n.jsx("td", { className: "px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300", children: i.model }),
    /* @__PURE__ */ n.jsx("td", { className: "px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300", children: i.mac })
  ] }, i.serial)) })
] }) }), jr = ({ setActiveView: u, data: l }) => {
  if (!l)
    return /* @__PURE__ */ n.jsx("div", { children: "Loading dashboard..." });
  const { devices: i = [], ssids: d = [], networks: R = [] } = l, E = {
    totalDevices: i.length,
    wirelessAps: i.filter((g) => {
      var p;
      return (p = g.model) == null ? void 0 : p.startsWith("MR");
    }).length,
    switches: i.filter((g) => {
      var p;
      return (p = g.model) == null ? void 0 : p.startsWith("MS");
    }).length,
    cameras: i.filter((g) => {
      var p;
      return (p = g.model) == null ? void 0 : p.startsWith("MV");
    }).length,
    ssids: d.length
  };
  return /* @__PURE__ */ n.jsxs("div", { children: [
    /* @__PURE__ */ n.jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8", children: [
      /* @__PURE__ */ n.jsx(L, { title: "Total Devices", value: E.totalDevices, icon: "📱" }),
      /* @__PURE__ */ n.jsx(L, { title: "Wireless APs", value: E.wirelessAps, icon: "📡" }),
      /* @__PURE__ */ n.jsx(L, { title: "Switches", value: E.switches, icon: "🔄" }),
      /* @__PURE__ */ n.jsx(L, { title: "Cameras", value: E.cameras, icon: "📹" }),
      /* @__PURE__ */ n.jsx(L, { title: "Virtual SSIDs", value: E.ssids, icon: "📶" })
    ] }),
    /* @__PURE__ */ n.jsx("h2", { className: "text-xl font-semibold mb-4", children: "Networks" }),
    /* @__PURE__ */ n.jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: R.map((g) => /* @__PURE__ */ n.jsx(
      "button",
      {
        "data-testid": "network-card",
        className: "bg-white dark:bg-gray-800 rounded-lg shadow p-4 cursor-pointer text-left",
        onClick: () => u({ view: "network", networkId: g.id }),
        children: /* @__PURE__ */ n.jsx("p", { className: "font-medium text-gray-900 dark:text-white", children: g.name })
      },
      g.id
    )) }),
    /* @__PURE__ */ n.jsx("h2", { className: "text-xl font-semibold mb-4 mt-8", children: "All Devices" }),
    /* @__PURE__ */ n.jsx(Rr, { devices: i, setActiveView: u })
  ] });
}, wr = ({ activeView: u, setActiveView: l, data: i }) => {
  const d = i.devices.find((R) => R.serial === u.deviceId);
  return d ? /* @__PURE__ */ n.jsxs("div", { children: [
    /* @__PURE__ */ n.jsx("button", { onClick: () => l({ view: "dashboard" }), className: "mb-4", children: "← Back to Dashboard" }),
    /* @__PURE__ */ n.jsx("h2", { className: "text-xl font-semibold mb-4", children: "Device Details" }),
    /* @__PURE__ */ n.jsxs("p", { children: [
      "Name: ",
      d.name || d.mac
    ] }),
    /* @__PURE__ */ n.jsxs("p", { children: [
      "Status: ",
      d.status
    ] }),
    /* @__PURE__ */ n.jsxs("p", { children: [
      "Model: ",
      d.model
    ] }),
    /* @__PURE__ */ n.jsxs("p", { children: [
      "MAC Address: ",
      d.mac
    ] }),
    /* @__PURE__ */ n.jsxs("p", { children: [
      "Serial: ",
      d.serial
    ] })
  ] }) : /* @__PURE__ */ n.jsx("div", { children: "Device not found" });
}, kr = ({ activeView: u, setActiveView: l, data: i }) => {
  const d = i.networks.find((R) => R.id === u.networkId);
  return d ? /* @__PURE__ */ n.jsxs("div", { children: [
    /* @__PURE__ */ n.jsx("button", { onClick: () => l({ view: "dashboard" }), className: "mb-4", children: "← Back to Dashboard" }),
    /* @__PURE__ */ n.jsx("h2", { className: "text-xl font-semibold mb-4", children: "Network Information" }),
    /* @__PURE__ */ n.jsxs("p", { children: [
      "Name: ",
      d.name
    ] }),
    /* @__PURE__ */ n.jsxs("p", { children: [
      "ID: ",
      d.id
    ] }),
    /* @__PURE__ */ n.jsxs("p", { children: [
      "Product Types: ",
      d.product_types.join(", ")
    ] })
  ] }) : /* @__PURE__ */ n.jsx("div", { children: "Network not found" });
}, Tr = ({ hass: u, config_entry_id: l }) => {
  const [i, d] = G(null), [R, E] = G(!0), [g, p] = G(null), [m, k] = G({ view: "dashboard" });
  if (yr(() => {
    if (!u || !u.connection) {
      p("Home Assistant connection object not found."), E(!1);
      return;
    }
    (async () => {
      try {
        const j = await u.connection.sendMessagePromise({
          type: "meraki_ha/get_config",
          config_entry_id: l
        });
        d(j);
      } catch (j) {
        console.error("Error fetching Meraki data:", j), p(`Failed to fetch Meraki data: ${j.message || "Unknown error"}`);
      } finally {
        E(!1);
      }
    })();
  }, [u, l]), R)
    return /* @__PURE__ */ n.jsx("div", { className: "p-4", children: "Loading..." });
  if (g)
    return /* @__PURE__ */ n.jsxs("div", { className: "p-4 text-red-500", children: [
      "Error: ",
      g
    ] });
  const y = () => {
    switch (m.view) {
      case "dashboard":
        return /* @__PURE__ */ n.jsx(jr, { setActiveView: k, data: i });
      case "device":
        return /* @__PURE__ */ n.jsx(wr, { activeView: m, setActiveView: k, data: i });
      case "network":
        return /* @__PURE__ */ n.jsx(kr, { activeView: m, setActiveView: k, data: i });
      default:
        return /* @__PURE__ */ n.jsx("div", { children: "Unknown view" });
    }
  };
  return /* @__PURE__ */ n.jsxs("div", { className: "p-4", children: [
    /* @__PURE__ */ n.jsx("h1", { className: "text-2xl font-bold mb-4", children: "Meraki Control" }),
    y()
  ] });
};
class Cr extends HTMLElement {
  constructor() {
    super(...arguments);
    K(this, "_root");
    K(this, "_hass");
    K(this, "_panel");
  }
  connectedCallback() {
    this._root = V.createRoot(this), this._render();
  }
  disconnectedCallback() {
    this._root && (this._root.unmount(), this._root = void 0);
  }
  set hass(i) {
    this._hass = i, this._render();
  }
  set panel(i) {
    this._panel = i, this._render();
  }
  _render() {
    !this._root || !this._hass || !this._panel || this._root.render(
      /* @__PURE__ */ n.jsx(se.StrictMode, { children: /* @__PURE__ */ n.jsx(Tr, { hass: this._hass, config_entry_id: this._panel.config.config_entry_id }) })
    );
  }
}
customElements.define("meraki-panel", Cr);
