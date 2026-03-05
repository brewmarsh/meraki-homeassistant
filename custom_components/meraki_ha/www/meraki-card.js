/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const I = globalThis, K = I.ShadowRoot && (I.ShadyCSS === void 0 || I.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, q = Symbol(), Y = /* @__PURE__ */ new WeakMap();
let lt = class {
  constructor(t, e, s) {
    if (this._$cssResult$ = !0, s !== q) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = t, this.t = e;
  }
  get styleSheet() {
    let t = this.o;
    const e = this.t;
    if (K && t === void 0) {
      const s = e !== void 0 && e.length === 1;
      s && (t = Y.get(e)), t === void 0 && ((this.o = t = new CSSStyleSheet()).replaceSync(this.cssText), s && Y.set(e, t));
    }
    return t;
  }
  toString() {
    return this.cssText;
  }
};
const $t = (r) => new lt(typeof r == "string" ? r : r + "", void 0, q), ft = (r, ...t) => {
  const e = r.length === 1 ? r[0] : t.reduce((s, i, n) => s + ((o) => {
    if (o._$cssResult$ === !0) return o.cssText;
    if (typeof o == "number") return o;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + o + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(i) + r[n + 1], r[0]);
  return new lt(e, r, q);
}, mt = (r, t) => {
  if (K) r.adoptedStyleSheets = t.map((e) => e instanceof CSSStyleSheet ? e : e.styleSheet);
  else for (const e of t) {
    const s = document.createElement("style"), i = I.litNonce;
    i !== void 0 && s.setAttribute("nonce", i), s.textContent = e.cssText, r.appendChild(s);
  }
}, Z = K ? (r) => r : (r) => r instanceof CSSStyleSheet ? ((t) => {
  let e = "";
  for (const s of t.cssRules) e += s.cssText;
  return $t(e);
})(r) : r;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: gt, defineProperty: yt, getOwnPropertyDescriptor: At, getOwnPropertyNames: vt, getOwnPropertySymbols: wt, getPrototypeOf: Et } = Object, y = globalThis, Q = y.trustedTypes, St = Q ? Q.emptyScript : "", L = y.reactiveElementPolyfillSupport, N = (r, t) => r, D = { toAttribute(r, t) {
  switch (t) {
    case Boolean:
      r = r ? St : null;
      break;
    case Object:
    case Array:
      r = r == null ? r : JSON.stringify(r);
  }
  return r;
}, fromAttribute(r, t) {
  let e = r;
  switch (t) {
    case Boolean:
      e = r !== null;
      break;
    case Number:
      e = r === null ? null : Number(r);
      break;
    case Object:
    case Array:
      try {
        e = JSON.parse(r);
      } catch {
        e = null;
      }
  }
  return e;
} }, F = (r, t) => !gt(r, t), X = { attribute: !0, type: String, converter: D, reflect: !1, useDefault: !1, hasChanged: F };
Symbol.metadata ?? (Symbol.metadata = Symbol("metadata")), y.litPropertyMetadata ?? (y.litPropertyMetadata = /* @__PURE__ */ new WeakMap());
let b = class extends HTMLElement {
  static addInitializer(t) {
    this._$Ei(), (this.l ?? (this.l = [])).push(t);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(t, e = X) {
    if (e.state && (e.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(t) && ((e = Object.create(e)).wrapped = !0), this.elementProperties.set(t, e), !e.noAccessor) {
      const s = Symbol(), i = this.getPropertyDescriptor(t, s, e);
      i !== void 0 && yt(this.prototype, t, i);
    }
  }
  static getPropertyDescriptor(t, e, s) {
    const { get: i, set: n } = At(this.prototype, t) ?? { get() {
      return this[e];
    }, set(o) {
      this[e] = o;
    } };
    return { get: i, set(o) {
      const h = i == null ? void 0 : i.call(this);
      n == null || n.call(this, o), this.requestUpdate(t, h, s);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(t) {
    return this.elementProperties.get(t) ?? X;
  }
  static _$Ei() {
    if (this.hasOwnProperty(N("elementProperties"))) return;
    const t = Et(this);
    t.finalize(), t.l !== void 0 && (this.l = [...t.l]), this.elementProperties = new Map(t.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(N("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(N("properties"))) {
      const e = this.properties, s = [...vt(e), ...wt(e)];
      for (const i of s) this.createProperty(i, e[i]);
    }
    const t = this[Symbol.metadata];
    if (t !== null) {
      const e = litPropertyMetadata.get(t);
      if (e !== void 0) for (const [s, i] of e) this.elementProperties.set(s, i);
    }
    this._$Eh = /* @__PURE__ */ new Map();
    for (const [e, s] of this.elementProperties) {
      const i = this._$Eu(e, s);
      i !== void 0 && this._$Eh.set(i, e);
    }
    this.elementStyles = this.finalizeStyles(this.styles);
  }
  static finalizeStyles(t) {
    const e = [];
    if (Array.isArray(t)) {
      const s = new Set(t.flat(1 / 0).reverse());
      for (const i of s) e.unshift(Z(i));
    } else t !== void 0 && e.push(Z(t));
    return e;
  }
  static _$Eu(t, e) {
    const s = e.attribute;
    return s === !1 ? void 0 : typeof s == "string" ? s : typeof t == "string" ? t.toLowerCase() : void 0;
  }
  constructor() {
    super(), this._$Ep = void 0, this.isUpdatePending = !1, this.hasUpdated = !1, this._$Em = null, this._$Ev();
  }
  _$Ev() {
    var t;
    this._$ES = new Promise((e) => this.enableUpdating = e), this._$AL = /* @__PURE__ */ new Map(), this._$E_(), this.requestUpdate(), (t = this.constructor.l) == null || t.forEach((e) => e(this));
  }
  addController(t) {
    var e;
    (this._$EO ?? (this._$EO = /* @__PURE__ */ new Set())).add(t), this.renderRoot !== void 0 && this.isConnected && ((e = t.hostConnected) == null || e.call(t));
  }
  removeController(t) {
    var e;
    (e = this._$EO) == null || e.delete(t);
  }
  _$E_() {
    const t = /* @__PURE__ */ new Map(), e = this.constructor.elementProperties;
    for (const s of e.keys()) this.hasOwnProperty(s) && (t.set(s, this[s]), delete this[s]);
    t.size > 0 && (this._$Ep = t);
  }
  createRenderRoot() {
    const t = this.shadowRoot ?? this.attachShadow(this.constructor.shadowRootOptions);
    return mt(t, this.constructor.elementStyles), t;
  }
  connectedCallback() {
    var t;
    this.renderRoot ?? (this.renderRoot = this.createRenderRoot()), this.enableUpdating(!0), (t = this._$EO) == null || t.forEach((e) => {
      var s;
      return (s = e.hostConnected) == null ? void 0 : s.call(e);
    });
  }
  enableUpdating(t) {
  }
  disconnectedCallback() {
    var t;
    (t = this._$EO) == null || t.forEach((e) => {
      var s;
      return (s = e.hostDisconnected) == null ? void 0 : s.call(e);
    });
  }
  attributeChangedCallback(t, e, s) {
    this._$AK(t, s);
  }
  _$ET(t, e) {
    var n;
    const s = this.constructor.elementProperties.get(t), i = this.constructor._$Eu(t, s);
    if (i !== void 0 && s.reflect === !0) {
      const o = (((n = s.converter) == null ? void 0 : n.toAttribute) !== void 0 ? s.converter : D).toAttribute(e, s.type);
      this._$Em = t, o == null ? this.removeAttribute(i) : this.setAttribute(i, o), this._$Em = null;
    }
  }
  _$AK(t, e) {
    var n, o;
    const s = this.constructor, i = s._$Eh.get(t);
    if (i !== void 0 && this._$Em !== i) {
      const h = s.getPropertyOptions(i), a = typeof h.converter == "function" ? { fromAttribute: h.converter } : ((n = h.converter) == null ? void 0 : n.fromAttribute) !== void 0 ? h.converter : D;
      this._$Em = i;
      const c = a.fromAttribute(e, h.type);
      this[i] = c ?? ((o = this._$Ej) == null ? void 0 : o.get(i)) ?? c, this._$Em = null;
    }
  }
  requestUpdate(t, e, s, i = !1, n) {
    var o;
    if (t !== void 0) {
      const h = this.constructor;
      if (i === !1 && (n = this[t]), s ?? (s = h.getPropertyOptions(t)), !((s.hasChanged ?? F)(n, e) || s.useDefault && s.reflect && n === ((o = this._$Ej) == null ? void 0 : o.get(t)) && !this.hasAttribute(h._$Eu(t, s)))) return;
      this.C(t, e, s);
    }
    this.isUpdatePending === !1 && (this._$ES = this._$EP());
  }
  C(t, e, { useDefault: s, reflect: i, wrapped: n }, o) {
    s && !(this._$Ej ?? (this._$Ej = /* @__PURE__ */ new Map())).has(t) && (this._$Ej.set(t, o ?? e ?? this[t]), n !== !0 || o !== void 0) || (this._$AL.has(t) || (this.hasUpdated || s || (e = void 0), this._$AL.set(t, e)), i === !0 && this._$Em !== t && (this._$Eq ?? (this._$Eq = /* @__PURE__ */ new Set())).add(t));
  }
  async _$EP() {
    this.isUpdatePending = !0;
    try {
      await this._$ES;
    } catch (e) {
      Promise.reject(e);
    }
    const t = this.scheduleUpdate();
    return t != null && await t, !this.isUpdatePending;
  }
  scheduleUpdate() {
    return this.performUpdate();
  }
  performUpdate() {
    var s;
    if (!this.isUpdatePending) return;
    if (!this.hasUpdated) {
      if (this.renderRoot ?? (this.renderRoot = this.createRenderRoot()), this._$Ep) {
        for (const [n, o] of this._$Ep) this[n] = o;
        this._$Ep = void 0;
      }
      const i = this.constructor.elementProperties;
      if (i.size > 0) for (const [n, o] of i) {
        const { wrapped: h } = o, a = this[n];
        h !== !0 || this._$AL.has(n) || a === void 0 || this.C(n, void 0, o, a);
      }
    }
    let t = !1;
    const e = this._$AL;
    try {
      t = this.shouldUpdate(e), t ? (this.willUpdate(e), (s = this._$EO) == null || s.forEach((i) => {
        var n;
        return (n = i.hostUpdate) == null ? void 0 : n.call(i);
      }), this.update(e)) : this._$EM();
    } catch (i) {
      throw t = !1, this._$EM(), i;
    }
    t && this._$AE(e);
  }
  willUpdate(t) {
  }
  _$AE(t) {
    var e;
    (e = this._$EO) == null || e.forEach((s) => {
      var i;
      return (i = s.hostUpdated) == null ? void 0 : i.call(s);
    }), this.hasUpdated || (this.hasUpdated = !0, this.firstUpdated(t)), this.updated(t);
  }
  _$EM() {
    this._$AL = /* @__PURE__ */ new Map(), this.isUpdatePending = !1;
  }
  get updateComplete() {
    return this.getUpdateComplete();
  }
  getUpdateComplete() {
    return this._$ES;
  }
  shouldUpdate(t) {
    return !0;
  }
  update(t) {
    this._$Eq && (this._$Eq = this._$Eq.forEach((e) => this._$ET(e, this[e]))), this._$EM();
  }
  updated(t) {
  }
  firstUpdated(t) {
  }
};
b.elementStyles = [], b.shadowRootOptions = { mode: "open" }, b[N("elementProperties")] = /* @__PURE__ */ new Map(), b[N("finalized")] = /* @__PURE__ */ new Map(), L == null || L({ ReactiveElement: b }), (y.reactiveElementVersions ?? (y.reactiveElementVersions = [])).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const x = globalThis, tt = (r) => r, j = x.trustedTypes, et = j ? j.createPolicy("lit-html", { createHTML: (r) => r }) : void 0, ct = "$lit$", g = `lit$${Math.random().toFixed(9).slice(2)}$`, dt = "?" + g, bt = `<${dt}>`, S = document, T = () => S.createComment(""), O = (r) => r === null || typeof r != "object" && typeof r != "function", J = Array.isArray, kt = (r) => J(r) || typeof (r == null ? void 0 : r[Symbol.iterator]) == "function", z = `[
\f\r]`, C = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, st = /-->/g, it = />/g, A = RegExp(`>|${z}(?:([^\\s"'>=/]+)(${z}*=${z}*(?:[^
\f\r"'\`<>=]|("|')|))|$)`, "g"), rt = /'/g, nt = /"/g, ut = /^(?:script|style|textarea|title)$/i, Pt = (r) => (t, ...e) => ({ _$litType$: r, strings: t, values: e }), v = Pt(1), k = Symbol.for("lit-noChange"), d = Symbol.for("lit-nothing"), ot = /* @__PURE__ */ new WeakMap(), w = S.createTreeWalker(S, 129);
function pt(r, t) {
  if (!J(r) || !r.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return et !== void 0 ? et.createHTML(t) : t;
}
const Ct = (r, t) => {
  const e = r.length - 1, s = [];
  let i, n = t === 2 ? "<svg>" : t === 3 ? "<math>" : "", o = C;
  for (let h = 0; h < e; h++) {
    const a = r[h];
    let c, p, l = -1, f = 0;
    for (; f < a.length && (o.lastIndex = f, p = o.exec(a), p !== null); ) f = o.lastIndex, o === C ? p[1] === "!--" ? o = st : p[1] !== void 0 ? o = it : p[2] !== void 0 ? (ut.test(p[2]) && (i = RegExp("</" + p[2], "g")), o = A) : p[3] !== void 0 && (o = A) : o === A ? p[0] === ">" ? (o = i ?? C, l = -1) : p[1] === void 0 ? l = -2 : (l = o.lastIndex - p[2].length, c = p[1], o = p[3] === void 0 ? A : p[3] === '"' ? nt : rt) : o === nt || o === rt ? o = A : o === st || o === it ? o = C : (o = A, i = void 0);
    const m = o === A && r[h + 1].startsWith("/>") ? " " : "";
    n += o === C ? a + bt : l >= 0 ? (s.push(c), a.slice(0, l) + ct + a.slice(l) + g + m) : a + g + (l === -2 ? h : m);
  }
  return [pt(r, n + (r[e] || "<?>") + (t === 2 ? "</svg>" : t === 3 ? "</math>" : "")), s];
};
class U {
  constructor({ strings: t, _$litType$: e }, s) {
    let i;
    this.parts = [];
    let n = 0, o = 0;
    const h = t.length - 1, a = this.parts, [c, p] = Ct(t, e);
    if (this.el = U.createElement(c, s), w.currentNode = this.el.content, e === 2 || e === 3) {
      const l = this.el.content.firstChild;
      l.replaceWith(...l.childNodes);
    }
    for (; (i = w.nextNode()) !== null && a.length < h; ) {
      if (i.nodeType === 1) {
        if (i.hasAttributes()) for (const l of i.getAttributeNames()) if (l.endsWith(ct)) {
          const f = p[o++], m = i.getAttribute(l).split(g), R = /([.?@])?(.*)/.exec(f);
          a.push({ type: 1, index: n, name: R[2], strings: m, ctor: R[1] === "." ? xt : R[1] === "?" ? Mt : R[1] === "@" ? Tt : G }), i.removeAttribute(l);
        } else l.startsWith(g) && (a.push({ type: 6, index: n }), i.removeAttribute(l));
        if (ut.test(i.tagName)) {
          const l = i.textContent.split(g), f = l.length - 1;
          if (f > 0) {
            i.textContent = j ? j.emptyScript : "";
            for (let m = 0; m < f; m++) i.append(l[m], T()), w.nextNode(), a.push({ type: 2, index: ++n });
            i.append(l[f], T());
          }
        }
      } else if (i.nodeType === 8) if (i.data === dt) a.push({ type: 2, index: n });
      else {
        let l = -1;
        for (; (l = i.data.indexOf(g, l + 1)) !== -1; ) a.push({ type: 7, index: n }), l += g.length - 1;
      }
      n++;
    }
  }
  static createElement(t, e) {
    const s = S.createElement("template");
    return s.innerHTML = t, s;
  }
}
function P(r, t, e = r, s) {
  var o, h;
  if (t === k) return t;
  let i = s !== void 0 ? (o = e._$Co) == null ? void 0 : o[s] : e._$Cl;
  const n = O(t) ? void 0 : t._$litDirective$;
  return (i == null ? void 0 : i.constructor) !== n && ((h = i == null ? void 0 : i._$AO) == null || h.call(i, !1), n === void 0 ? i = void 0 : (i = new n(r), i._$AT(r, e, s)), s !== void 0 ? (e._$Co ?? (e._$Co = []))[s] = i : e._$Cl = i), i !== void 0 && (t = P(r, i._$AS(r, t.values), i, s)), t;
}
class Nt {
  constructor(t, e) {
    this._$AV = [], this._$AN = void 0, this._$AD = t, this._$AM = e;
  }
  get parentNode() {
    return this._$AM.parentNode;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  u(t) {
    const { el: { content: e }, parts: s } = this._$AD, i = ((t == null ? void 0 : t.creationScope) ?? S).importNode(e, !0);
    w.currentNode = i;
    let n = w.nextNode(), o = 0, h = 0, a = s[0];
    for (; a !== void 0; ) {
      if (o === a.index) {
        let c;
        a.type === 2 ? c = new H(n, n.nextSibling, this, t) : a.type === 1 ? c = new a.ctor(n, a.name, a.strings, this, t) : a.type === 6 && (c = new Ot(n, this, t)), this._$AV.push(c), a = s[++h];
      }
      o !== (a == null ? void 0 : a.index) && (n = w.nextNode(), o++);
    }
    return w.currentNode = S, i;
  }
  p(t) {
    let e = 0;
    for (const s of this._$AV) s !== void 0 && (s.strings !== void 0 ? (s._$AI(t, s, e), e += s.strings.length - 2) : s._$AI(t[e])), e++;
  }
}
class H {
  get _$AU() {
    var t;
    return ((t = this._$AM) == null ? void 0 : t._$AU) ?? this._$Cv;
  }
  constructor(t, e, s, i) {
    this.type = 2, this._$AH = d, this._$AN = void 0, this._$AA = t, this._$AB = e, this._$AM = s, this.options = i, this._$Cv = (i == null ? void 0 : i.isConnected) ?? !0;
  }
  get parentNode() {
    let t = this._$AA.parentNode;
    const e = this._$AM;
    return e !== void 0 && (t == null ? void 0 : t.nodeType) === 11 && (t = e.parentNode), t;
  }
  get startNode() {
    return this._$AA;
  }
  get endNode() {
    return this._$AB;
  }
  _$AI(t, e = this) {
    t = P(this, t, e), O(t) ? t === d || t == null || t === "" ? (this._$AH !== d && this._$AR(), this._$AH = d) : t !== this._$AH && t !== k && this._(t) : t._$litType$ !== void 0 ? this.$(t) : t.nodeType !== void 0 ? this.T(t) : kt(t) ? this.k(t) : this._(t);
  }
  O(t) {
    return this._$AA.parentNode.insertBefore(t, this._$AB);
  }
  T(t) {
    this._$AH !== t && (this._$AR(), this._$AH = this.O(t));
  }
  _(t) {
    this._$AH !== d && O(this._$AH) ? this._$AA.nextSibling.data = t : this.T(S.createTextNode(t)), this._$AH = t;
  }
  $(t) {
    var n;
    const { values: e, _$litType$: s } = t, i = typeof s == "number" ? this._$AC(t) : (s.el === void 0 && (s.el = U.createElement(pt(s.h, s.h[0]), this.options)), s);
    if (((n = this._$AH) == null ? void 0 : n._$AD) === i) this._$AH.p(e);
    else {
      const o = new Nt(i, this), h = o.u(this.options);
      o.p(e), this.T(h), this._$AH = o;
    }
  }
  _$AC(t) {
    let e = ot.get(t.strings);
    return e === void 0 && ot.set(t.strings, e = new U(t)), e;
  }
  k(t) {
    J(this._$AH) || (this._$AH = [], this._$AR());
    const e = this._$AH;
    let s, i = 0;
    for (const n of t) i === e.length ? e.push(s = new H(this.O(T()), this.O(T()), this, this.options)) : s = e[i], s._$AI(n), i++;
    i < e.length && (this._$AR(s && s._$AB.nextSibling, i), e.length = i);
  }
  _$AR(t = this._$AA.nextSibling, e) {
    var s;
    for ((s = this._$AP) == null ? void 0 : s.call(this, !1, !0, e); t !== this._$AB; ) {
      const i = tt(t).nextSibling;
      tt(t).remove(), t = i;
    }
  }
  setConnected(t) {
    var e;
    this._$AM === void 0 && (this._$Cv = t, (e = this._$AP) == null || e.call(this, t));
  }
}
class G {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(t, e, s, i, n) {
    this.type = 1, this._$AH = d, this._$AN = void 0, this.element = t, this.name = e, this._$AM = i, this.options = n, s.length > 2 || s[0] !== "" || s[1] !== "" ? (this._$AH = Array(s.length - 1).fill(new String()), this.strings = s) : this._$AH = d;
  }
  _$AI(t, e = this, s, i) {
    const n = this.strings;
    let o = !1;
    if (n === void 0) t = P(this, t, e, 0), o = !O(t) || t !== this._$AH && t !== k, o && (this._$AH = t);
    else {
      const h = t;
      let a, c;
      for (t = n[0], a = 0; a < n.length - 1; a++) c = P(this, h[s + a], e, a), c === k && (c = this._$AH[a]), o || (o = !O(c) || c !== this._$AH[a]), c === d ? t = d : t !== d && (t += (c ?? "") + n[a + 1]), this._$AH[a] = c;
    }
    o && !i && this.j(t);
  }
  j(t) {
    t === d ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, t ?? "");
  }
}
class xt extends G {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(t) {
    this.element[this.name] = t === d ? void 0 : t;
  }
}
class Mt extends G {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(t) {
    this.element.toggleAttribute(this.name, !!t && t !== d);
  }
}
class Tt extends G {
  constructor(t, e, s, i, n) {
    super(t, e, s, i, n), this.type = 5;
  }
  _$AI(t, e = this) {
    if ((t = P(this, t, e, 0) ?? d) === k) return;
    const s = this._$AH, i = t === d && s !== d || t.capture !== s.capture || t.once !== s.once || t.passive !== s.passive, n = t !== d && (s === d || i);
    i && this.element.removeEventListener(this.name, this, s), n && this.element.addEventListener(this.name, this, t), this._$AH = t;
  }
  handleEvent(t) {
    var e;
    typeof this._$AH == "function" ? this._$AH.call(((e = this.options) == null ? void 0 : e.host) ?? this.element, t) : this._$AH.handleEvent(t);
  }
}
class Ot {
  constructor(t, e, s) {
    this.element = t, this.type = 6, this._$AN = void 0, this._$AM = e, this.options = s;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t) {
    P(this, t);
  }
}
const B = x.litHtmlPolyfillSupport;
B == null || B(U, H), (x.litHtmlVersions ?? (x.litHtmlVersions = [])).push("3.3.2");
const Ut = (r, t, e) => {
  const s = (e == null ? void 0 : e.renderBefore) ?? t;
  let i = s._$litPart$;
  if (i === void 0) {
    const n = (e == null ? void 0 : e.renderBefore) ?? null;
    s._$litPart$ = i = new H(t.insertBefore(T(), n), n, void 0, e ?? {});
  }
  return i._$AI(r), i;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const E = globalThis;
class M extends b {
  constructor() {
    super(...arguments), this.renderOptions = { host: this }, this._$Do = void 0;
  }
  createRenderRoot() {
    var e;
    const t = super.createRenderRoot();
    return (e = this.renderOptions).renderBefore ?? (e.renderBefore = t.firstChild), t;
  }
  update(t) {
    const e = this.render();
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Do = Ut(e, this.renderRoot, this.renderOptions);
  }
  connectedCallback() {
    var t;
    super.connectedCallback(), (t = this._$Do) == null || t.setConnected(!0);
  }
  disconnectedCallback() {
    var t;
    super.disconnectedCallback(), (t = this._$Do) == null || t.setConnected(!1);
  }
  render() {
    return k;
  }
}
var ht;
M._$litElement$ = !0, M.finalized = !0, (ht = E.litElementHydrateSupport) == null || ht.call(E, { LitElement: M });
const V = E.litElementPolyfillSupport;
V == null || V({ LitElement: M });
(E.litElementVersions ?? (E.litElementVersions = [])).push("4.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Ht = (r) => (t, e) => {
  e !== void 0 ? e.addInitializer(() => {
    customElements.define(r, t);
  }) : customElements.define(r, t);
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Rt = { attribute: !0, type: String, converter: D, reflect: !1, hasChanged: F }, It = (r = Rt, t, e) => {
  const { kind: s, metadata: i } = e;
  let n = globalThis.litPropertyMetadata.get(i);
  if (n === void 0 && globalThis.litPropertyMetadata.set(i, n = /* @__PURE__ */ new Map()), s === "setter" && ((r = Object.create(r)).wrapped = !0), n.set(e.name, r), s === "accessor") {
    const { name: o } = e;
    return { set(h) {
      const a = t.get.call(this);
      t.set.call(this, h), this.requestUpdate(o, a, r, !0, h);
    }, init(h) {
      return h !== void 0 && this.C(o, void 0, r, h), h;
    } };
  }
  if (s === "setter") {
    const { name: o } = e;
    return function(h) {
      const a = this[o];
      t.call(this, h), this.requestUpdate(o, a, r, !0, h);
    };
  }
  throw Error("Unsupported decorator location: " + s);
};
function _t(r) {
  return (t, e) => typeof e == "object" ? It(r, t, e) : ((s, i, n) => {
    const o = i.hasOwnProperty(n);
    return i.constructor.createProperty(n, s), o ? Object.getOwnPropertyDescriptor(i, n) : void 0;
  })(r, t, e);
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function $(r) {
  return _t({ ...r, state: !0, attribute: !1 });
}
var W = /* @__PURE__ */ ((r) => (r.GET_CONFIG = "meraki_ha/get_config", r.SUBSCRIBE_MERAKI_DATA = "meraki_ha/subscribe_meraki_data", r.GET_CAMERA_STREAM_URL = "meraki_ha/get_camera_stream_url", r.GET_CAMERA_SNAPSHOT = "meraki_ha/get_camera_snapshot", r.GET_VERSION = "meraki_ha/get_version", r.GET_NETWORK_EVENTS = "meraki_ha/get_network_events", r.UPDATE_ENABLED_NETWORKS = "meraki_ha/update_enabled_networks", r.CREATE_GUEST_KEY = "meraki_ha/ipsk/create", r.GET_GUEST_KEYS = "meraki_ha/ipsk/get", r.REVOKE_GUEST_KEY = "meraki_ha/ipsk/revoke", r.TIMED_ACCESS_GET_POLICIES = "meraki_ha/timed_access/get_policies", r))(W || {});
const at = async (r, t) => {
  if (!r)
    throw new Error("Home Assistant object is not available.");
  try {
    if (typeof r.callWS == "function")
      return await r.callWS(t);
    if (r.connection && typeof r.connection.sendMessagePromise == "function")
      return await r.connection.sendMessagePromise(t);
    throw new Error("Home Assistant WebSocket communication methods not found.");
  } catch (e) {
    throw console.error(`Meraki HA: WebSocket error [${t.type}]:`, e), e;
  }
};
var Dt = Object.defineProperty, jt = Object.getOwnPropertyDescriptor, _ = (r, t, e, s) => {
  for (var i = s > 1 ? void 0 : s ? jt(t, e) : t, n = r.length - 1, o; n >= 0; n--)
    (o = r[n]) && (i = (s ? o(t, e, i) : o(i)) || i);
  return s && i && Dt(t, e, i), i;
};
let u = class extends M {
  constructor() {
    super(...arguments), this._selectedNetwork = "", this._selectedSsid = "", this._selectedPolicy = "", this._duration = "60", this._customName = "", this._customPassphrase = "", this._creating = !1, this._error = null, this._success = null, this._networks = [], this._ssids = [], this._policies = [], this._loading = !0;
  }
  setConfig(r) {
    if (!r)
      throw new Error("Invalid configuration");
    this._config = r;
  }
  static getStubConfig() {
    return {
      name: "Meraki Guest Access"
    };
  }
  firstUpdated(r) {
    super.firstUpdated(r), this._fetchInitialData();
  }
  updated(r) {
    super.updated(r), r.has("hass") && this.hass && !this._networks.length && this._fetchInitialData();
  }
  async _fetchInitialData() {
    var r;
    if (this.hass) {
      this._loading = !0;
      try {
        const t = await this.hass.callWS({
          type: "config_entries/get",
          domain: "meraki_ha"
        }), e = ((r = this._config) == null ? void 0 : r.config_entry_id) || (t.length > 0 ? t[0].entry_id : null);
        if (!e) {
          this._error = "Meraki integration not found. Please configure it first.", this._loading = !1;
          return;
        }
        const s = await at(this.hass, {
          type: W.GET_CONFIG,
          config_entry_id: e
        });
        this._networks = s.networks.filter((i) => {
          var n;
          return (n = i.productTypes) == null ? void 0 : n.includes("wireless");
        }) || [], this._ssids = s.ssids || [], this._networks.length > 0 && !this._selectedNetwork && (this._selectedNetwork = this._networks[0].id, this._fetchPolicies(this._selectedNetwork, e));
      } catch (t) {
        this._error = `Failed to fetch Meraki data: ${t.message || t}`;
      } finally {
        this._loading = !1;
      }
    }
  }
  async _fetchPolicies(r, t) {
    var e;
    if (this.hass)
      try {
        let s = t || ((e = this._config) == null ? void 0 : e.config_entry_id);
        if (!s) {
          const n = await this.hass.callWS({
            type: "config_entries/get",
            domain: "meraki_ha"
          });
          s = n.length > 0 ? n[0].entry_id : void 0;
        }
        if (!s) return;
        const i = await at(this.hass, {
          type: W.TIMED_ACCESS_GET_POLICIES,
          config_entry_id: s,
          networkId: r
        });
        this._policies = i;
      } catch (s) {
        console.error("Failed to fetch policies:", s), this._policies = [];
      }
  }
  render() {
    var t, e;
    if (this._loading && !this._networks.length)
      return v`
        <ha-card .header="${((t = this._config) == null ? void 0 : t.name) || "Meraki Guest Access"}">
          <div class="card-content flex justify-center p-8">
            <ha-circular-progress active></ha-circular-progress>
          </div>
        </ha-card>
      `;
    const r = this._ssids.filter((s) => s.networkId === this._selectedNetwork);
    return v`
      <ha-card .header="${((e = this._config) == null ? void 0 : e.name) || "Meraki Guest Access"}">
        <div class="card-content">
          ${this._error ? v`
                <ha-alert alert-type="error" dismissable @alert-dismissed-clicked="${() => this._error = null}">
                  ${this._error}
                </ha-alert>
              ` : ""}
          ${this._success ? v`
                <ha-alert alert-type="success" dismissable @alert-dismissed-clicked="${() => this._success = null}">
                  ${this._success}
                </ha-alert>
              ` : ""}

          <div class="form-container">
            <ha-select
              label="Network"
              .value="${this._selectedNetwork}"
              @selected="${this._handleNetworkChanged}"
              fixedMenuPosition
              naturalMenuWidth
            >
              ${this._networks.map(
      (s) => v`<mwc-list-item .value="${s.id}">${s.name}</mwc-list-item>`
    )}
            </ha-select>

            <ha-select
              label="SSID"
              .value="${this._selectedSsid}"
              .disabled="${!this._selectedNetwork}"
              @selected="${this._handleSsidChanged}"
              fixedMenuPosition
              naturalMenuWidth
            >
              ${r.map(
      (s) => v`<mwc-list-item .value="${s.number.toString()}">${s.name} (SSID ${s.number})</mwc-list-item>`
    )}
            </ha-select>

            <ha-select
              label="Group Policy"
              .value="${this._selectedPolicy}"
              .disabled="${!this._selectedNetwork}"
              @selected="${(s) => this._selectedPolicy = s.target.value}"
              fixedMenuPosition
              naturalMenuWidth
            >
              <mwc-list-item .value="">None (Default)</mwc-list-item>
              ${this._policies.map(
      (s) => v`<mwc-list-item .value="${s.groupPolicyId}">${s.name}</mwc-list-item>`
    )}
            </ha-select>

            <ha-select
              label="Duration"
              .value="${this._duration}"
              @selected="${(s) => this._duration = s.target.value}"
              fixedMenuPosition
              naturalMenuWidth
            >
              <mwc-list-item .value="${"30"}">30 Minutes</mwc-list-item>
              <mwc-list-item .value="${"60"}">1 Hour</mwc-list-item>
              <mwc-list-item .value="${"240"}">4 Hours</mwc-list-item>
              <mwc-list-item .value="${"1440"}">24 Hours</mwc-list-item>
              <mwc-list-item .value="${"10080"}">7 Days</mwc-list-item>
            </ha-select>

            <ha-textfield
              label="Name (Optional)"
              placeholder="e.g. Guest-John"
              .value="${this._customName}"
              @input="${(s) => this._customName = s.target.value}"
            ></ha-textfield>

            <ha-textfield
              label="Passphrase (Optional)"
              placeholder="Leave empty to auto-generate"
              .value="${this._customPassphrase}"
              @input="${(s) => this._customPassphrase = s.target.value}"
            ></ha-textfield>

            <ha-button
              raised
              .disabled="${this._creating || !this._selectedNetwork || !this._selectedSsid}"
              @click="${this._handleCreate}"
            >
              ${this._creating ? "Creating..." : "Generate access key"}
            </ha-button>
          </div>
        </div>
      </ha-card>
    `;
  }
  _handleNetworkChanged(r) {
    const t = r.target.value;
    t !== this._selectedNetwork && (this._selectedNetwork = t, this._selectedSsid = "", this._selectedPolicy = "", this._fetchPolicies(t));
  }
  _handleSsidChanged(r) {
    this._selectedSsid = r.target.value;
  }
  async _handleCreate() {
    if (!(!this._selectedNetwork || !this._selectedSsid)) {
      this._creating = !0, this._error = null, this._success = null;
      try {
        await this.hass.callService("meraki_ha", "create_guest_key", {
          network_id: this._selectedNetwork,
          ssid_number: parseInt(this._selectedSsid, 10),
          duration_minutes: parseInt(this._duration, 10),
          name: this._customName || void 0,
          passphrase: this._customPassphrase || void 0,
          group_policy_id: this._selectedPolicy || void 0
        }), this._success = "Guest access key created successfully!", this._customName = "", this._customPassphrase = "";
      } catch (r) {
        this._error = `Failed to create guest key: ${r.message || r}`;
      } finally {
        this._creating = !1;
      }
    }
  }
};
u.styles = ft`
    :host {
      display: block;
    }
    .card-content {
      padding: 16px;
    }
    .form-container {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    ha-select, ha-textfield, ha-button {
      width: 100%;
    }
    ha-alert {
      display: block;
      margin-bottom: 16px;
    }
    .flex {
      display: flex;
    }
    .justify-center {
      justify-content: center;
    }
    .p-8 {
      padding: 32px;
    }
  `;
_([
  _t({ attribute: !1 })
], u.prototype, "hass", 2);
_([
  $()
], u.prototype, "_config", 2);
_([
  $()
], u.prototype, "_selectedNetwork", 2);
_([
  $()
], u.prototype, "_selectedSsid", 2);
_([
  $()
], u.prototype, "_selectedPolicy", 2);
_([
  $()
], u.prototype, "_duration", 2);
_([
  $()
], u.prototype, "_customName", 2);
_([
  $()
], u.prototype, "_customPassphrase", 2);
_([
  $()
], u.prototype, "_creating", 2);
_([
  $()
], u.prototype, "_error", 2);
_([
  $()
], u.prototype, "_success", 2);
_([
  $()
], u.prototype, "_networks", 2);
_([
  $()
], u.prototype, "_ssids", 2);
_([
  $()
], u.prototype, "_policies", 2);
_([
  $()
], u.prototype, "_loading", 2);
u = _([
  Ht("meraki-guest-access-card")
], u);
window.customCards = window.customCards || [];
window.customCards.push({
  type: "meraki-guest-access-card",
  name: "Meraki Guest Access",
  description: "Create and manage Meraki IPSK guest access keys.",
  preview: !0
});
export {
  u as MerakiGuestAccessCard
};
