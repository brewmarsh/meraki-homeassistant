var xr = Object.defineProperty;
var yr = (u, l, i) => l in u ? xr(u, l, { enumerable: !0, configurable: !0, writable: !0, value: i }) : u[l] = i;
var G = (u, l, i) => (yr(u, typeof l != "symbol" ? l + "" : l, i), i);
import oe, { useState as H, useEffect as br } from "react";
import _r from "react-dom";
var se = { exports: {} }, $ = {};
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
function Er() {
  if (Ne)
    return $;
  Ne = 1;
  var u = oe, l = Symbol.for("react.element"), i = Symbol.for("react.fragment"), d = Object.prototype.hasOwnProperty, R = u.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, y = { key: !0, ref: !0, __self: !0, __source: !0 };
  function g(h, m, w) {
    var b, k = {}, O = null, T = null;
    w !== void 0 && (O = "" + w), m.key !== void 0 && (O = "" + m.key), m.ref !== void 0 && (T = m.ref);
    for (b in m)
      d.call(m, b) && !y.hasOwnProperty(b) && (k[b] = m[b]);
    if (h && h.defaultProps)
      for (b in m = h.defaultProps, m)
        k[b] === void 0 && (k[b] = m[b]);
    return { $$typeof: l, type: h, key: O, ref: T, props: k, _owner: R.current };
  }
  return $.Fragment = i, $.jsx = g, $.jsxs = g, $;
}
var L = {};
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
function Rr() {
  return De || (De = 1, process.env.NODE_ENV !== "production" && function() {
    var u = oe, l = Symbol.for("react.element"), i = Symbol.for("react.portal"), d = Symbol.for("react.fragment"), R = Symbol.for("react.strict_mode"), y = Symbol.for("react.profiler"), g = Symbol.for("react.provider"), h = Symbol.for("react.context"), m = Symbol.for("react.forward_ref"), w = Symbol.for("react.suspense"), b = Symbol.for("react.suspense_list"), k = Symbol.for("react.memo"), O = Symbol.for("react.lazy"), T = Symbol.for("react.offscreen"), S = Symbol.iterator, Fe = "@@iterator";
    function Ie(e) {
      if (e === null || typeof e != "object")
        return null;
      var r = S && e[S] || e[Fe];
      return typeof r == "function" ? r : null;
    }
    var D = u.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;
    function x(e) {
      {
        for (var r = arguments.length, t = new Array(r > 1 ? r - 1 : 0), a = 1; a < r; a++)
          t[a - 1] = arguments[a];
        We("error", e, t);
      }
    }
    function We(e, r, t) {
      {
        var a = D.ReactDebugCurrentFrame, c = a.getStackAddendum();
        c !== "" && (r += "%s", t = t.concat([c]));
        var f = t.map(function(o) {
          return String(o);
        });
        f.unshift("Warning: " + r), Function.prototype.apply.call(console[e], console, f);
      }
    }
    var Me = !1, $e = !1, Le = !1, Ve = !1, Ye = !1, le;
    le = Symbol.for("react.module.reference");
    function Ue(e) {
      return !!(typeof e == "string" || typeof e == "function" || e === d || e === y || Ye || e === R || e === w || e === b || Ve || e === T || Me || $e || Le || typeof e == "object" && e !== null && (e.$$typeof === O || e.$$typeof === k || e.$$typeof === g || e.$$typeof === h || e.$$typeof === m || // This needs to include all possible module reference object
      // types supported by any Flight configuration anywhere since
      // we don't know which Flight build this will end up being used
      // with.
      e.$$typeof === le || e.getModuleId !== void 0));
    }
    function Be(e, r, t) {
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
        case y:
          return "Profiler";
        case R:
          return "StrictMode";
        case w:
          return "Suspense";
        case b:
          return "SuspenseList";
      }
      if (typeof e == "object")
        switch (e.$$typeof) {
          case h:
            var r = e;
            return ce(r) + ".Consumer";
          case g:
            var t = e;
            return ce(t._context) + ".Provider";
          case m:
            return Be(e, e.render, "ForwardRef");
          case k:
            var a = e.displayName || null;
            return a !== null ? a : C(e.type) || "Memo";
          case O: {
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
    var P = Object.assign, I = 0, ue, fe, de, ve, he, pe, me;
    function ge() {
    }
    ge.__reactDisabledLog = !0;
    function qe() {
      {
        if (I === 0) {
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
        I++;
      }
    }
    function Je() {
      {
        if (I--, I === 0) {
          var e = {
            configurable: !0,
            enumerable: !0,
            writable: !0
          };
          Object.defineProperties(console, {
            log: P({}, e, {
              value: ue
            }),
            info: P({}, e, {
              value: fe
            }),
            warn: P({}, e, {
              value: de
            }),
            error: P({}, e, {
              value: ve
            }),
            group: P({}, e, {
              value: he
            }),
            groupCollapsed: P({}, e, {
              value: pe
            }),
            groupEnd: P({}, e, {
              value: me
            })
          });
        }
        I < 0 && x("disabledDepth fell below zero. This is a bug in React. Please file an issue.");
      }
    }
    var X = D.ReactCurrentDispatcher, Z;
    function B(e, r, t) {
      {
        if (Z === void 0)
          try {
            throw Error();
          } catch (c) {
            var a = c.stack.trim().match(/\n( *(at )?)/);
            Z = a && a[1] || "";
          }
        return `
` + Z + e;
      }
    }
    var Q = !1, q;
    {
      var Ke = typeof WeakMap == "function" ? WeakMap : Map;
      q = new Ke();
    }
    function xe(e, r) {
      if (!e || Q)
        return "";
      {
        var t = q.get(e);
        if (t !== void 0)
          return t;
      }
      var a;
      Q = !0;
      var c = Error.prepareStackTrace;
      Error.prepareStackTrace = void 0;
      var f;
      f = X.current, X.current = null, qe();
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
            } catch (E) {
              a = E;
            }
            Reflect.construct(e, [], o);
          } else {
            try {
              o.call();
            } catch (E) {
              a = E;
            }
            e.call(o.prototype);
          }
        } else {
          try {
            throw Error();
          } catch (E) {
            a = E;
          }
          e();
        }
      } catch (E) {
        if (E && a && typeof E.stack == "string") {
          for (var s = E.stack.split(`
`), _ = a.stack.split(`
`), v = s.length - 1, p = _.length - 1; v >= 1 && p >= 0 && s[v] !== _[p]; )
            p--;
          for (; v >= 1 && p >= 0; v--, p--)
            if (s[v] !== _[p]) {
              if (v !== 1 || p !== 1)
                do
                  if (v--, p--, p < 0 || s[v] !== _[p]) {
                    var j = `
` + s[v].replace(" at new ", " at ");
                    return e.displayName && j.includes("<anonymous>") && (j = j.replace("<anonymous>", e.displayName)), typeof e == "function" && q.set(e, j), j;
                  }
                while (v >= 1 && p >= 0);
              break;
            }
        }
      } finally {
        Q = !1, X.current = f, Je(), Error.prepareStackTrace = c;
      }
      var F = e ? e.displayName || e.name : "", N = F ? B(F) : "";
      return typeof e == "function" && q.set(e, N), N;
    }
    function Ge(e, r, t) {
      return xe(e, !1);
    }
    function He(e) {
      var r = e.prototype;
      return !!(r && r.isReactComponent);
    }
    function J(e, r, t) {
      if (e == null)
        return "";
      if (typeof e == "function")
        return xe(e, He(e));
      if (typeof e == "string")
        return B(e);
      switch (e) {
        case w:
          return B("Suspense");
        case b:
          return B("SuspenseList");
      }
      if (typeof e == "object")
        switch (e.$$typeof) {
          case m:
            return Ge(e.render);
          case k:
            return J(e.type, r, t);
          case O: {
            var a = e, c = a._payload, f = a._init;
            try {
              return J(f(c), r, t);
            } catch {
            }
          }
        }
      return "";
    }
    var W = Object.prototype.hasOwnProperty, ye = {}, be = D.ReactDebugCurrentFrame;
    function K(e) {
      if (e) {
        var r = e._owner, t = J(e.type, e._source, r ? r.type : null);
        be.setExtraStackFrame(t);
      } else
        be.setExtraStackFrame(null);
    }
    function ze(e, r, t, a, c) {
      {
        var f = Function.call.bind(W);
        for (var o in e)
          if (f(e, o)) {
            var s = void 0;
            try {
              if (typeof e[o] != "function") {
                var _ = Error((a || "React class") + ": " + t + " type `" + o + "` is invalid; it must be a function, usually from the `prop-types` package, but received `" + typeof e[o] + "`.This often happens because of typos such as `PropTypes.function` instead of `PropTypes.func`.");
                throw _.name = "Invariant Violation", _;
              }
              s = e[o](r, o, a, t, null, "SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED");
            } catch (v) {
              s = v;
            }
            s && !(s instanceof Error) && (K(c), x("%s: type specification of %s `%s` is invalid; the type checker function must return `null` or an `Error` but returned a %s. You may have forgotten to pass an argument to the type checker creator (arrayOf, instanceOf, objectOf, oneOf, oneOfType, and shape all require an argument).", a || "React class", t, o, typeof s), K(null)), s instanceof Error && !(s.message in ye) && (ye[s.message] = !0, K(c), x("Failed %s type: %s", t, s.message), K(null));
          }
      }
    }
    var Xe = Array.isArray;
    function ee(e) {
      return Xe(e);
    }
    function Ze(e) {
      {
        var r = typeof Symbol == "function" && Symbol.toStringTag, t = r && e[Symbol.toStringTag] || e.constructor.name || "Object";
        return t;
      }
    }
    function Qe(e) {
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
      if (Qe(e))
        return x("The provided key is an unsupported type %s. This value must be coerced to a string before before using it here.", Ze(e)), _e(e);
    }
    var M = D.ReactCurrentOwner, er = {
      key: !0,
      ref: !0,
      __self: !0,
      __source: !0
    }, Re, je, re;
    re = {};
    function rr(e) {
      if (W.call(e, "ref")) {
        var r = Object.getOwnPropertyDescriptor(e, "ref").get;
        if (r && r.isReactWarning)
          return !1;
      }
      return e.ref !== void 0;
    }
    function tr(e) {
      if (W.call(e, "key")) {
        var r = Object.getOwnPropertyDescriptor(e, "key").get;
        if (r && r.isReactWarning)
          return !1;
      }
      return e.key !== void 0;
    }
    function nr(e, r) {
      if (typeof e.ref == "string" && M.current && r && M.current.stateNode !== r) {
        var t = C(M.current.type);
        re[t] || (x('Component "%s" contains the string ref "%s". Support for string refs will be removed in a future major release. This case cannot be automatically converted to an arrow function. We ask you to manually fix this case by using useRef() or createRef() instead. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-string-ref', C(M.current.type), e.ref), re[t] = !0);
      }
    }
    function ar(e, r) {
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
    function ir(e, r) {
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
    var sr = function(e, r, t, a, c, f, o) {
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
    function or(e, r, t, a, c) {
      {
        var f, o = {}, s = null, _ = null;
        t !== void 0 && (Ee(t), s = "" + t), tr(r) && (Ee(r.key), s = "" + r.key), rr(r) && (_ = r.ref, nr(r, c));
        for (f in r)
          W.call(r, f) && !er.hasOwnProperty(f) && (o[f] = r[f]);
        if (e && e.defaultProps) {
          var v = e.defaultProps;
          for (f in v)
            o[f] === void 0 && (o[f] = v[f]);
        }
        if (s || _) {
          var p = typeof e == "function" ? e.displayName || e.name || "Unknown" : e;
          s && ar(o, p), _ && ir(o, p);
        }
        return sr(e, s, _, c, a, M.current, o);
      }
    }
    var te = D.ReactCurrentOwner, we = D.ReactDebugCurrentFrame;
    function A(e) {
      if (e) {
        var r = e._owner, t = J(e.type, e._source, r ? r.type : null);
        we.setExtraStackFrame(t);
      } else
        we.setExtraStackFrame(null);
    }
    var ne;
    ne = !1;
    function ae(e) {
      return typeof e == "object" && e !== null && e.$$typeof === l;
    }
    function ke() {
      {
        if (te.current) {
          var e = C(te.current.type);
          if (e)
            return `

Check the render method of \`` + e + "`.";
        }
        return "";
      }
    }
    function lr(e) {
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
    function cr(e) {
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
    function Se(e, r) {
      {
        if (!e._store || e._store.validated || e.key != null)
          return;
        e._store.validated = !0;
        var t = cr(r);
        if (Te[t])
          return;
        Te[t] = !0;
        var a = "";
        e && e._owner && e._owner !== te.current && (a = " It was passed a child from " + C(e._owner.type) + "."), A(e), x('Each child in a list should have a unique "key" prop.%s%s See https://reactjs.org/link/warning-keys for more information.', t, a), A(null);
      }
    }
    function Ce(e, r) {
      {
        if (typeof e != "object")
          return;
        if (ee(e))
          for (var t = 0; t < e.length; t++) {
            var a = e[t];
            ae(a) && Se(a, r);
          }
        else if (ae(e))
          e._store && (e._store.validated = !0);
        else if (e) {
          var c = Ie(e);
          if (typeof c == "function" && c !== e.entries)
            for (var f = c.call(e), o; !(o = f.next()).done; )
              ae(o.value) && Se(o.value, r);
        }
      }
    }
    function ur(e) {
      {
        var r = e.type;
        if (r == null || typeof r == "string")
          return;
        var t;
        if (typeof r == "function")
          t = r.propTypes;
        else if (typeof r == "object" && (r.$$typeof === m || // Note: Memo only checks outer props here.
        // Inner props are checked in the reconciler.
        r.$$typeof === k))
          t = r.propTypes;
        else
          return;
        if (t) {
          var a = C(r);
          ze(t, e.props, "prop", a, e);
        } else if (r.PropTypes !== void 0 && !ne) {
          ne = !0;
          var c = C(r);
          x("Component %s declared `PropTypes` instead of `propTypes`. Did you misspell the property assignment?", c || "Unknown");
        }
        typeof r.getDefaultProps == "function" && !r.getDefaultProps.isReactClassApproved && x("getDefaultProps is only used on classic React.createClass definitions. Use a static property named `defaultProps` instead.");
      }
    }
    function fr(e) {
      {
        for (var r = Object.keys(e.props), t = 0; t < r.length; t++) {
          var a = r[t];
          if (a !== "children" && a !== "key") {
            A(e), x("Invalid prop `%s` supplied to `React.Fragment`. React.Fragment can only have `key` and `children` props.", a), A(null);
            break;
          }
        }
        e.ref !== null && (A(e), x("Invalid attribute `ref` supplied to `React.Fragment`."), A(null));
      }
    }
    var Oe = {};
    function Pe(e, r, t, a, c, f) {
      {
        var o = Ue(e);
        if (!o) {
          var s = "";
          (e === void 0 || typeof e == "object" && e !== null && Object.keys(e).length === 0) && (s += " You likely forgot to export your component from the file it's defined in, or you might have mixed up default and named imports.");
          var _ = lr(c);
          _ ? s += _ : s += ke();
          var v;
          e === null ? v = "null" : ee(e) ? v = "array" : e !== void 0 && e.$$typeof === l ? (v = "<" + (C(e.type) || "Unknown") + " />", s = " Did you accidentally export a JSX literal instead of a component?") : v = typeof e, x("React.jsx: type is invalid -- expected a string (for built-in components) or a class/function (for composite components) but got: %s.%s", v, s);
        }
        var p = or(e, r, t, c, f);
        if (p == null)
          return p;
        if (o) {
          var j = r.children;
          if (j !== void 0)
            if (a)
              if (ee(j)) {
                for (var F = 0; F < j.length; F++)
                  Ce(j[F], e);
                Object.freeze && Object.freeze(j);
              } else
                x("React.jsx: Static children should always be an array. You are likely explicitly calling React.jsxs or React.jsxDEV. Use the Babel transform instead.");
            else
              Ce(j, e);
        }
        if (W.call(r, "key")) {
          var N = C(e), E = Object.keys(r).filter(function(gr) {
            return gr !== "key";
          }), ie = E.length > 0 ? "{key: someKey, " + E.join(": ..., ") + ": ...}" : "{key: someKey}";
          if (!Oe[N + ie]) {
            var mr = E.length > 0 ? "{" + E.join(": ..., ") + ": ...}" : "{}";
            x(`A props object containing a "key" prop is being spread into JSX:
  let props = %s;
  <%s {...props} />
React keys must be passed directly to JSX without using spread:
  let props = %s;
  <%s key={someKey} {...props} />`, ie, N, mr, N), Oe[N + ie] = !0;
          }
        }
        return e === d ? fr(p) : ur(p), p;
      }
    }
    function dr(e, r, t) {
      return Pe(e, r, t, !0);
    }
    function vr(e, r, t) {
      return Pe(e, r, t, !1);
    }
    var hr = vr, pr = dr;
    L.Fragment = d, L.jsx = hr, L.jsxs = pr;
  }()), L;
}
process.env.NODE_ENV === "production" ? se.exports = Er() : se.exports = Rr();
var n = se.exports, U = {}, V = _r;
if (process.env.NODE_ENV === "production")
  U.createRoot = V.createRoot, U.hydrateRoot = V.hydrateRoot;
else {
  var z = V.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;
  U.createRoot = function(u, l) {
    z.usingClientEntryPoint = !0;
    try {
      return V.createRoot(u, l);
    } finally {
      z.usingClientEntryPoint = !1;
    }
  }, U.hydrateRoot = function(u, l, i) {
    z.usingClientEntryPoint = !0;
    try {
      return V.hydrateRoot(u, l, i);
    } finally {
      z.usingClientEntryPoint = !1;
    }
  };
}
const Y = ({ title: u, value: l, icon: i }) => /* @__PURE__ */ n.jsxs("div", { className: "bg-white dark:bg-gray-800 rounded-lg shadow p-4 flex items-center", children: [
  /* @__PURE__ */ n.jsx("div", { className: "text-3xl mr-4", children: i }),
  /* @__PURE__ */ n.jsxs("div", { children: [
    /* @__PURE__ */ n.jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: u }),
    /* @__PURE__ */ n.jsx("p", { className: "text-2xl font-semibold text-gray-900 dark:text-white", children: l })
  ] })
] }), jr = ({ devices: u, setActiveView: l }) => /* @__PURE__ */ n.jsx("div", { className: "bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden", children: /* @__PURE__ */ n.jsxs("table", { className: "min-w-full", children: [
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
] }) }), Ae = ({ setActiveView: u, data: l }) => {
  if (!l)
    return /* @__PURE__ */ n.jsx("div", { children: "Loading dashboard..." });
  const { devices: i = [], ssids: d = [], networks: R = [] } = l, y = {
    totalDevices: i.length,
    wirelessAps: i.filter((g) => {
      var h;
      return (h = g.model) == null ? void 0 : h.startsWith("MR");
    }).length,
    switches: i.filter((g) => {
      var h;
      return (h = g.model) == null ? void 0 : h.startsWith("MS");
    }).length,
    cameras: i.filter((g) => {
      var h;
      return (h = g.model) == null ? void 0 : h.startsWith("MV");
    }).length,
    ssids: d.length
  };
  return /* @__PURE__ */ n.jsxs("div", { children: [
    /* @__PURE__ */ n.jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8", children: [
      /* @__PURE__ */ n.jsx(Y, { title: "Total Devices", value: y.totalDevices, icon: "📱" }),
      /* @__PURE__ */ n.jsx(Y, { title: "Wireless APs", value: y.wirelessAps, icon: "📡" }),
      /* @__PURE__ */ n.jsx(Y, { title: "Switches", value: y.switches, icon: "🔄" }),
      /* @__PURE__ */ n.jsx(Y, { title: "Cameras", value: y.cameras, icon: "📹" }),
      /* @__PURE__ */ n.jsx(Y, { title: "Virtual SSIDs", value: y.ssids, icon: "📶" })
    ] }),
    /* @__PURE__ */ n.jsx("h2", { className: "text-xl font-semibold mb-4", children: "Networks" }),
    /* @__PURE__ */ n.jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: R.map((g) => /* @__PURE__ */ n.jsx(
      "div",
      {
        "data-testid": "network-card",
        className: "bg-white dark:bg-gray-800 rounded-lg shadow p-4 cursor-pointer",
        style: { display: "block" },
        onClick: () => u({ view: "network", networkId: g.id }),
        children: /* @__PURE__ */ n.jsx("p", { className: "font-medium text-gray-900 dark:text-white", children: g.name })
      },
      g.id
    )) }),
    /* @__PURE__ */ n.jsx("h2", { className: "text-xl font-semibold mb-4 mt-8", children: "All Devices" }),
    /* @__PURE__ */ n.jsx(jr, { devices: i, setActiveView: u })
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
  const [i, d] = H(null), [R, y] = H(!0), [g, h] = H(null), [m, w] = H({ view: "dashboard" });
  if (br(() => {
    if (!u || !u.connection) {
      h("Home Assistant connection object not found."), y(!1);
      return;
    }
    const O = (async () => {
      try {
        return await u.connection.subscribeMessage(
          (S) => {
            S.type === "result" ? (S.success ? d(S.result) : h(`Subscription failed: ${S.error.message}`), y(!1)) : S.type === "event" ? d(S.event) : (d(S), y(!1));
          },
          {
            type: "meraki_ha/subscribe_meraki_data",
            config_entry_id: l
          }
        );
      } catch (T) {
        console.error("Error subscribing to Meraki data:", T), h("Failed to subscribe to Meraki data. See console for details."), y(!1);
      }
    })();
    return () => {
      O.then((T) => {
        T && T();
      });
    };
  }, [u, l]), R)
    return /* @__PURE__ */ n.jsx("div", { className: "p-4", children: "Loading..." });
  if (g)
    return /* @__PURE__ */ n.jsxs("div", { className: "p-4 text-red-500", children: [
      "Error: ",
      g
    ] });
  const b = () => {
    switch (m.view) {
      case "dashboard":
        return /* @__PURE__ */ n.jsx(Ae, { setActiveView: w, data: i });
      case "device":
        return /* @__PURE__ */ n.jsx(wr, { activeView: m, setActiveView: w, data: i });
      case "network":
        return /* @__PURE__ */ n.jsx(kr, { activeView: m, setActiveView: w, data: i });
      default:
        return /* @__PURE__ */ n.jsx(Ae, { setActiveView: w, data: i });
    }
  };
  return /* @__PURE__ */ n.jsxs("div", { className: "p-4", children: [
    /* @__PURE__ */ n.jsx("h1", { className: "text-2xl font-bold mb-4", children: "Meraki HA Web UI" }),
    b()
  ] });
};
class Sr extends HTMLElement {
  constructor() {
    super(...arguments);
    G(this, "_root");
    G(this, "_hass");
    G(this, "_panel");
  }
  connectedCallback() {
    this._root = U.createRoot(this), this._render();
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
      /* @__PURE__ */ n.jsx(oe.StrictMode, { children: /* @__PURE__ */ n.jsx(Tr, { hass: this._hass, config_entry_id: this._panel.config.config_entry_id }) })
    );
  }
}
customElements.define("meraki-panel", Sr);
