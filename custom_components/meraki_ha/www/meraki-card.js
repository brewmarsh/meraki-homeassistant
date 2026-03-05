/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const I = globalThis, K = I.ShadowRoot && (I.ShadyCSS === void 0 || I.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, q = Symbol(), Y = /* @__PURE__ */ new WeakMap();
let le = class {
  constructor(e, t, s) {
    if (this._$cssResult$ = !0, s !== q) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = e, this.t = t;
  }
  get styleSheet() {
    let e = this.o;
    const t = this.t;
    if (K && e === void 0) {
      const s = t !== void 0 && t.length === 1;
      s && (e = Y.get(t)), e === void 0 && ((this.o = e = new CSSStyleSheet()).replaceSync(this.cssText), s && Y.set(t, e));
    }
    return e;
  }
  toString() {
    return this.cssText;
  }
};
const $e = (r) => new le(typeof r == "string" ? r : r + "", void 0, q), fe = (r, ...e) => {
  const t = r.length === 1 ? r[0] : e.reduce((s, i, o) => s + ((n) => {
    if (n._$cssResult$ === !0) return n.cssText;
    if (typeof n == "number") return n;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + n + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(i) + r[o + 1], r[0]);
  return new le(t, r, q);
}, me = (r, e) => {
  if (K) r.adoptedStyleSheets = e.map((t) => t instanceof CSSStyleSheet ? t : t.styleSheet);
  else for (const t of e) {
    const s = document.createElement("style"), i = I.litNonce;
    i !== void 0 && s.setAttribute("nonce", i), s.textContent = t.cssText, r.appendChild(s);
  }
}, Z = K ? (r) => r : (r) => r instanceof CSSStyleSheet ? ((e) => {
  let t = "";
  for (const s of e.cssRules) t += s.cssText;
  return $e(t);
})(r) : r;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: ge, defineProperty: ye, getOwnPropertyDescriptor: Ae, getOwnPropertyNames: ve, getOwnPropertySymbols: Ee, getPrototypeOf: Se } = Object, y = globalThis, Q = y.trustedTypes, we = Q ? Q.emptyScript : "", L = y.reactiveElementPolyfillSupport, N = (r, e) => r, D = { toAttribute(r, e) {
  switch (e) {
    case Boolean:
      r = r ? we : null;
      break;
    case Object:
    case Array:
      r = r == null ? r : JSON.stringify(r);
  }
  return r;
}, fromAttribute(r, e) {
  let t = r;
  switch (e) {
    case Boolean:
      t = r !== null;
      break;
    case Number:
      t = r === null ? null : Number(r);
      break;
    case Object:
    case Array:
      try {
        t = JSON.parse(r);
      } catch {
        t = null;
      }
  }
  return t;
} }, F = (r, e) => !ge(r, e), X = { attribute: !0, type: String, converter: D, reflect: !1, useDefault: !1, hasChanged: F };
Symbol.metadata ?? (Symbol.metadata = Symbol("metadata")), y.litPropertyMetadata ?? (y.litPropertyMetadata = /* @__PURE__ */ new WeakMap());
let b = class extends HTMLElement {
  static addInitializer(e) {
    this._$Ei(), (this.l ?? (this.l = [])).push(e);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(e, t = X) {
    if (t.state && (t.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(e) && ((t = Object.create(t)).wrapped = !0), this.elementProperties.set(e, t), !t.noAccessor) {
      const s = Symbol(), i = this.getPropertyDescriptor(e, s, t);
      i !== void 0 && ye(this.prototype, e, i);
    }
  }
  static getPropertyDescriptor(e, t, s) {
    const { get: i, set: o } = Ae(this.prototype, e) ?? { get() {
      return this[t];
    }, set(n) {
      this[t] = n;
    } };
    return { get: i, set(n) {
      const h = i == null ? void 0 : i.call(this);
      o == null || o.call(this, n), this.requestUpdate(e, h, s);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(e) {
    return this.elementProperties.get(e) ?? X;
  }
  static _$Ei() {
    if (this.hasOwnProperty(N("elementProperties"))) return;
    const e = Se(this);
    e.finalize(), e.l !== void 0 && (this.l = [...e.l]), this.elementProperties = new Map(e.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(N("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(N("properties"))) {
      const t = this.properties, s = [...ve(t), ...Ee(t)];
      for (const i of s) this.createProperty(i, t[i]);
    }
    const e = this[Symbol.metadata];
    if (e !== null) {
      const t = litPropertyMetadata.get(e);
      if (t !== void 0) for (const [s, i] of t) this.elementProperties.set(s, i);
    }
    this._$Eh = /* @__PURE__ */ new Map();
    for (const [t, s] of this.elementProperties) {
      const i = this._$Eu(t, s);
      i !== void 0 && this._$Eh.set(i, t);
    }
    this.elementStyles = this.finalizeStyles(this.styles);
  }
  static finalizeStyles(e) {
    const t = [];
    if (Array.isArray(e)) {
      const s = new Set(e.flat(1 / 0).reverse());
      for (const i of s) t.unshift(Z(i));
    } else e !== void 0 && t.push(Z(e));
    return t;
  }
  static _$Eu(e, t) {
    const s = t.attribute;
    return s === !1 ? void 0 : typeof s == "string" ? s : typeof e == "string" ? e.toLowerCase() : void 0;
  }
  constructor() {
    super(), this._$Ep = void 0, this.isUpdatePending = !1, this.hasUpdated = !1, this._$Em = null, this._$Ev();
  }
  _$Ev() {
    var e;
    this._$ES = new Promise((t) => this.enableUpdating = t), this._$AL = /* @__PURE__ */ new Map(), this._$E_(), this.requestUpdate(), (e = this.constructor.l) == null || e.forEach((t) => t(this));
  }
  addController(e) {
    var t;
    (this._$EO ?? (this._$EO = /* @__PURE__ */ new Set())).add(e), this.renderRoot !== void 0 && this.isConnected && ((t = e.hostConnected) == null || t.call(e));
  }
  removeController(e) {
    var t;
    (t = this._$EO) == null || t.delete(e);
  }
  _$E_() {
    const e = /* @__PURE__ */ new Map(), t = this.constructor.elementProperties;
    for (const s of t.keys()) this.hasOwnProperty(s) && (e.set(s, this[s]), delete this[s]);
    e.size > 0 && (this._$Ep = e);
  }
  createRenderRoot() {
    const e = this.shadowRoot ?? this.attachShadow(this.constructor.shadowRootOptions);
    return me(e, this.constructor.elementStyles), e;
  }
  connectedCallback() {
    var e;
    this.renderRoot ?? (this.renderRoot = this.createRenderRoot()), this.enableUpdating(!0), (e = this._$EO) == null || e.forEach((t) => {
      var s;
      return (s = t.hostConnected) == null ? void 0 : s.call(t);
    });
  }
  enableUpdating(e) {
  }
  disconnectedCallback() {
    var e;
    (e = this._$EO) == null || e.forEach((t) => {
      var s;
      return (s = t.hostDisconnected) == null ? void 0 : s.call(t);
    });
  }
  attributeChangedCallback(e, t, s) {
    this._$AK(e, s);
  }
  _$ET(e, t) {
    var o;
    const s = this.constructor.elementProperties.get(e), i = this.constructor._$Eu(e, s);
    if (i !== void 0 && s.reflect === !0) {
      const n = (((o = s.converter) == null ? void 0 : o.toAttribute) !== void 0 ? s.converter : D).toAttribute(t, s.type);
      this._$Em = e, n == null ? this.removeAttribute(i) : this.setAttribute(i, n), this._$Em = null;
    }
  }
  _$AK(e, t) {
    var o, n;
    const s = this.constructor, i = s._$Eh.get(e);
    if (i !== void 0 && this._$Em !== i) {
      const h = s.getPropertyOptions(i), a = typeof h.converter == "function" ? { fromAttribute: h.converter } : ((o = h.converter) == null ? void 0 : o.fromAttribute) !== void 0 ? h.converter : D;
      this._$Em = i;
      const c = a.fromAttribute(t, h.type);
      this[i] = c ?? ((n = this._$Ej) == null ? void 0 : n.get(i)) ?? c, this._$Em = null;
    }
  }
  requestUpdate(e, t, s, i = !1, o) {
    var n;
    if (e !== void 0) {
      const h = this.constructor;
      if (i === !1 && (o = this[e]), s ?? (s = h.getPropertyOptions(e)), !((s.hasChanged ?? F)(o, t) || s.useDefault && s.reflect && o === ((n = this._$Ej) == null ? void 0 : n.get(e)) && !this.hasAttribute(h._$Eu(e, s)))) return;
      this.C(e, t, s);
    }
    this.isUpdatePending === !1 && (this._$ES = this._$EP());
  }
  C(e, t, { useDefault: s, reflect: i, wrapped: o }, n) {
    s && !(this._$Ej ?? (this._$Ej = /* @__PURE__ */ new Map())).has(e) && (this._$Ej.set(e, n ?? t ?? this[e]), o !== !0 || n !== void 0) || (this._$AL.has(e) || (this.hasUpdated || s || (t = void 0), this._$AL.set(e, t)), i === !0 && this._$Em !== e && (this._$Eq ?? (this._$Eq = /* @__PURE__ */ new Set())).add(e));
  }
  async _$EP() {
    this.isUpdatePending = !0;
    try {
      await this._$ES;
    } catch (t) {
      Promise.reject(t);
    }
    const e = this.scheduleUpdate();
    return e != null && await e, !this.isUpdatePending;
  }
  scheduleUpdate() {
    return this.performUpdate();
  }
  performUpdate() {
    var s;
    if (!this.isUpdatePending) return;
    if (!this.hasUpdated) {
      if (this.renderRoot ?? (this.renderRoot = this.createRenderRoot()), this._$Ep) {
        for (const [o, n] of this._$Ep) this[o] = n;
        this._$Ep = void 0;
      }
      const i = this.constructor.elementProperties;
      if (i.size > 0) for (const [o, n] of i) {
        const { wrapped: h } = n, a = this[o];
        h !== !0 || this._$AL.has(o) || a === void 0 || this.C(o, void 0, n, a);
      }
    }
    let e = !1;
    const t = this._$AL;
    try {
      e = this.shouldUpdate(t), e ? (this.willUpdate(t), (s = this._$EO) == null || s.forEach((i) => {
        var o;
        return (o = i.hostUpdate) == null ? void 0 : o.call(i);
      }), this.update(t)) : this._$EM();
    } catch (i) {
      throw e = !1, this._$EM(), i;
    }
    e && this._$AE(t);
  }
  willUpdate(e) {
  }
  _$AE(e) {
    var t;
    (t = this._$EO) == null || t.forEach((s) => {
      var i;
      return (i = s.hostUpdated) == null ? void 0 : i.call(s);
    }), this.hasUpdated || (this.hasUpdated = !0, this.firstUpdated(e)), this.updated(e);
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
  shouldUpdate(e) {
    return !0;
  }
  update(e) {
    this._$Eq && (this._$Eq = this._$Eq.forEach((t) => this._$ET(t, this[t]))), this._$EM();
  }
  updated(e) {
  }
  firstUpdated(e) {
  }
};
b.elementStyles = [], b.shadowRootOptions = { mode: "open" }, b[N("elementProperties")] = /* @__PURE__ */ new Map(), b[N("finalized")] = /* @__PURE__ */ new Map(), L == null || L({ ReactiveElement: b }), (y.reactiveElementVersions ?? (y.reactiveElementVersions = [])).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const x = globalThis, ee = (r) => r, j = x.trustedTypes, te = j ? j.createPolicy("lit-html", { createHTML: (r) => r }) : void 0, ce = "$lit$", g = `lit$${Math.random().toFixed(9).slice(2)}$`, de = "?" + g, be = `<${de}>`, w = document, T = () => w.createComment(""), O = (r) => r === null || typeof r != "object" && typeof r != "function", J = Array.isArray, ke = (r) => J(r) || typeof (r == null ? void 0 : r[Symbol.iterator]) == "function", z = `[
\f\r]`, C = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, se = /-->/g, ie = />/g, A = RegExp(`>|${z}(?:([^\\s"'>=/]+)(${z}*=${z}*(?:[^
\f\r"'\`<>=]|("|')|))|$)`, "g"), re = /'/g, oe = /"/g, ue = /^(?:script|style|textarea|title)$/i, Pe = (r) => (e, ...t) => ({ _$litType$: r, strings: e, values: t }), v = Pe(1), k = Symbol.for("lit-noChange"), d = Symbol.for("lit-nothing"), ne = /* @__PURE__ */ new WeakMap(), E = w.createTreeWalker(w, 129);
function pe(r, e) {
  if (!J(r) || !r.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return te !== void 0 ? te.createHTML(e) : e;
}
const Ce = (r, e) => {
  const t = r.length - 1, s = [];
  let i, o = e === 2 ? "<svg>" : e === 3 ? "<math>" : "", n = C;
  for (let h = 0; h < t; h++) {
    const a = r[h];
    let c, p, l = -1, f = 0;
    for (; f < a.length && (n.lastIndex = f, p = n.exec(a), p !== null); ) f = n.lastIndex, n === C ? p[1] === "!--" ? n = se : p[1] !== void 0 ? n = ie : p[2] !== void 0 ? (ue.test(p[2]) && (i = RegExp("</" + p[2], "g")), n = A) : p[3] !== void 0 && (n = A) : n === A ? p[0] === ">" ? (n = i ?? C, l = -1) : p[1] === void 0 ? l = -2 : (l = n.lastIndex - p[2].length, c = p[1], n = p[3] === void 0 ? A : p[3] === '"' ? oe : re) : n === oe || n === re ? n = A : n === se || n === ie ? n = C : (n = A, i = void 0);
    const m = n === A && r[h + 1].startsWith("/>") ? " " : "";
    o += n === C ? a + be : l >= 0 ? (s.push(c), a.slice(0, l) + ce + a.slice(l) + g + m) : a + g + (l === -2 ? h : m);
  }
  return [pe(r, o + (r[t] || "<?>") + (e === 2 ? "</svg>" : e === 3 ? "</math>" : "")), s];
};
class U {
  constructor({ strings: e, _$litType$: t }, s) {
    let i;
    this.parts = [];
    let o = 0, n = 0;
    const h = e.length - 1, a = this.parts, [c, p] = Ce(e, t);
    if (this.el = U.createElement(c, s), E.currentNode = this.el.content, t === 2 || t === 3) {
      const l = this.el.content.firstChild;
      l.replaceWith(...l.childNodes);
    }
    for (; (i = E.nextNode()) !== null && a.length < h; ) {
      if (i.nodeType === 1) {
        if (i.hasAttributes()) for (const l of i.getAttributeNames()) if (l.endsWith(ce)) {
          const f = p[n++], m = i.getAttribute(l).split(g), R = /([.?@])?(.*)/.exec(f);
          a.push({ type: 1, index: o, name: R[2], strings: m, ctor: R[1] === "." ? xe : R[1] === "?" ? Me : R[1] === "@" ? Te : G }), i.removeAttribute(l);
        } else l.startsWith(g) && (a.push({ type: 6, index: o }), i.removeAttribute(l));
        if (ue.test(i.tagName)) {
          const l = i.textContent.split(g), f = l.length - 1;
          if (f > 0) {
            i.textContent = j ? j.emptyScript : "";
            for (let m = 0; m < f; m++) i.append(l[m], T()), E.nextNode(), a.push({ type: 2, index: ++o });
            i.append(l[f], T());
          }
        }
      } else if (i.nodeType === 8) if (i.data === de) a.push({ type: 2, index: o });
      else {
        let l = -1;
        for (; (l = i.data.indexOf(g, l + 1)) !== -1; ) a.push({ type: 7, index: o }), l += g.length - 1;
      }
      o++;
    }
  }
  static createElement(e, t) {
    const s = w.createElement("template");
    return s.innerHTML = e, s;
  }
}
function P(r, e, t = r, s) {
  var n, h;
  if (e === k) return e;
  let i = s !== void 0 ? (n = t._$Co) == null ? void 0 : n[s] : t._$Cl;
  const o = O(e) ? void 0 : e._$litDirective$;
  return (i == null ? void 0 : i.constructor) !== o && ((h = i == null ? void 0 : i._$AO) == null || h.call(i, !1), o === void 0 ? i = void 0 : (i = new o(r), i._$AT(r, t, s)), s !== void 0 ? (t._$Co ?? (t._$Co = []))[s] = i : t._$Cl = i), i !== void 0 && (e = P(r, i._$AS(r, e.values), i, s)), e;
}
class Ne {
  constructor(e, t) {
    this._$AV = [], this._$AN = void 0, this._$AD = e, this._$AM = t;
  }
  get parentNode() {
    return this._$AM.parentNode;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  u(e) {
    const { el: { content: t }, parts: s } = this._$AD, i = ((e == null ? void 0 : e.creationScope) ?? w).importNode(t, !0);
    E.currentNode = i;
    let o = E.nextNode(), n = 0, h = 0, a = s[0];
    for (; a !== void 0; ) {
      if (n === a.index) {
        let c;
        a.type === 2 ? c = new H(o, o.nextSibling, this, e) : a.type === 1 ? c = new a.ctor(o, a.name, a.strings, this, e) : a.type === 6 && (c = new Oe(o, this, e)), this._$AV.push(c), a = s[++h];
      }
      n !== (a == null ? void 0 : a.index) && (o = E.nextNode(), n++);
    }
    return E.currentNode = w, i;
  }
  p(e) {
    let t = 0;
    for (const s of this._$AV) s !== void 0 && (s.strings !== void 0 ? (s._$AI(e, s, t), t += s.strings.length - 2) : s._$AI(e[t])), t++;
  }
}
class H {
  get _$AU() {
    var e;
    return ((e = this._$AM) == null ? void 0 : e._$AU) ?? this._$Cv;
  }
  constructor(e, t, s, i) {
    this.type = 2, this._$AH = d, this._$AN = void 0, this._$AA = e, this._$AB = t, this._$AM = s, this.options = i, this._$Cv = (i == null ? void 0 : i.isConnected) ?? !0;
  }
  get parentNode() {
    let e = this._$AA.parentNode;
    const t = this._$AM;
    return t !== void 0 && (e == null ? void 0 : e.nodeType) === 11 && (e = t.parentNode), e;
  }
  get startNode() {
    return this._$AA;
  }
  get endNode() {
    return this._$AB;
  }
  _$AI(e, t = this) {
    e = P(this, e, t), O(e) ? e === d || e == null || e === "" ? (this._$AH !== d && this._$AR(), this._$AH = d) : e !== this._$AH && e !== k && this._(e) : e._$litType$ !== void 0 ? this.$(e) : e.nodeType !== void 0 ? this.T(e) : ke(e) ? this.k(e) : this._(e);
  }
  O(e) {
    return this._$AA.parentNode.insertBefore(e, this._$AB);
  }
  T(e) {
    this._$AH !== e && (this._$AR(), this._$AH = this.O(e));
  }
  _(e) {
    this._$AH !== d && O(this._$AH) ? this._$AA.nextSibling.data = e : this.T(w.createTextNode(e)), this._$AH = e;
  }
  $(e) {
    var o;
    const { values: t, _$litType$: s } = e, i = typeof s == "number" ? this._$AC(e) : (s.el === void 0 && (s.el = U.createElement(pe(s.h, s.h[0]), this.options)), s);
    if (((o = this._$AH) == null ? void 0 : o._$AD) === i) this._$AH.p(t);
    else {
      const n = new Ne(i, this), h = n.u(this.options);
      n.p(t), this.T(h), this._$AH = n;
    }
  }
  _$AC(e) {
    let t = ne.get(e.strings);
    return t === void 0 && ne.set(e.strings, t = new U(e)), t;
  }
  k(e) {
    J(this._$AH) || (this._$AH = [], this._$AR());
    const t = this._$AH;
    let s, i = 0;
    for (const o of e) i === t.length ? t.push(s = new H(this.O(T()), this.O(T()), this, this.options)) : s = t[i], s._$AI(o), i++;
    i < t.length && (this._$AR(s && s._$AB.nextSibling, i), t.length = i);
  }
  _$AR(e = this._$AA.nextSibling, t) {
    var s;
    for ((s = this._$AP) == null ? void 0 : s.call(this, !1, !0, t); e !== this._$AB; ) {
      const i = ee(e).nextSibling;
      ee(e).remove(), e = i;
    }
  }
  setConnected(e) {
    var t;
    this._$AM === void 0 && (this._$Cv = e, (t = this._$AP) == null || t.call(this, e));
  }
}
class G {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(e, t, s, i, o) {
    this.type = 1, this._$AH = d, this._$AN = void 0, this.element = e, this.name = t, this._$AM = i, this.options = o, s.length > 2 || s[0] !== "" || s[1] !== "" ? (this._$AH = Array(s.length - 1).fill(new String()), this.strings = s) : this._$AH = d;
  }
  _$AI(e, t = this, s, i) {
    const o = this.strings;
    let n = !1;
    if (o === void 0) e = P(this, e, t, 0), n = !O(e) || e !== this._$AH && e !== k, n && (this._$AH = e);
    else {
      const h = e;
      let a, c;
      for (e = o[0], a = 0; a < o.length - 1; a++) c = P(this, h[s + a], t, a), c === k && (c = this._$AH[a]), n || (n = !O(c) || c !== this._$AH[a]), c === d ? e = d : e !== d && (e += (c ?? "") + o[a + 1]), this._$AH[a] = c;
    }
    n && !i && this.j(e);
  }
  j(e) {
    e === d ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, e ?? "");
  }
}
class xe extends G {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(e) {
    this.element[this.name] = e === d ? void 0 : e;
  }
}
class Me extends G {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(e) {
    this.element.toggleAttribute(this.name, !!e && e !== d);
  }
}
class Te extends G {
  constructor(e, t, s, i, o) {
    super(e, t, s, i, o), this.type = 5;
  }
  _$AI(e, t = this) {
    if ((e = P(this, e, t, 0) ?? d) === k) return;
    const s = this._$AH, i = e === d && s !== d || e.capture !== s.capture || e.once !== s.once || e.passive !== s.passive, o = e !== d && (s === d || i);
    i && this.element.removeEventListener(this.name, this, s), o && this.element.addEventListener(this.name, this, e), this._$AH = e;
  }
  handleEvent(e) {
    var t;
    typeof this._$AH == "function" ? this._$AH.call(((t = this.options) == null ? void 0 : t.host) ?? this.element, e) : this._$AH.handleEvent(e);
  }
}
class Oe {
  constructor(e, t, s) {
    this.element = e, this.type = 6, this._$AN = void 0, this._$AM = t, this.options = s;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(e) {
    P(this, e);
  }
}
const B = x.litHtmlPolyfillSupport;
B == null || B(U, H), (x.litHtmlVersions ?? (x.litHtmlVersions = [])).push("3.3.2");
const Ue = (r, e, t) => {
  const s = (t == null ? void 0 : t.renderBefore) ?? e;
  let i = s._$litPart$;
  if (i === void 0) {
    const o = (t == null ? void 0 : t.renderBefore) ?? null;
    s._$litPart$ = i = new H(e.insertBefore(T(), o), o, void 0, t ?? {});
  }
  return i._$AI(r), i;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const S = globalThis;
class M extends b {
  constructor() {
    super(...arguments), this.renderOptions = { host: this }, this._$Do = void 0;
  }
  createRenderRoot() {
    var t;
    const e = super.createRenderRoot();
    return (t = this.renderOptions).renderBefore ?? (t.renderBefore = e.firstChild), e;
  }
  update(e) {
    const t = this.render();
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(e), this._$Do = Ue(t, this.renderRoot, this.renderOptions);
  }
  connectedCallback() {
    var e;
    super.connectedCallback(), (e = this._$Do) == null || e.setConnected(!0);
  }
  disconnectedCallback() {
    var e;
    super.disconnectedCallback(), (e = this._$Do) == null || e.setConnected(!1);
  }
  render() {
    return k;
  }
}
var he;
M._$litElement$ = !0, M.finalized = !0, (he = S.litElementHydrateSupport) == null || he.call(S, { LitElement: M });
const V = S.litElementPolyfillSupport;
V == null || V({ LitElement: M });
(S.litElementVersions ?? (S.litElementVersions = [])).push("4.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const He = (r) => (e, t) => {
  t !== void 0 ? t.addInitializer(() => {
    customElements.define(r, e);
  }) : customElements.define(r, e);
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Re = { attribute: !0, type: String, converter: D, reflect: !1, hasChanged: F }, Ie = (r = Re, e, t) => {
  const { kind: s, metadata: i } = t;
  let o = globalThis.litPropertyMetadata.get(i);
  if (o === void 0 && globalThis.litPropertyMetadata.set(i, o = /* @__PURE__ */ new Map()), s === "setter" && ((r = Object.create(r)).wrapped = !0), o.set(t.name, r), s === "accessor") {
    const { name: n } = t;
    return { set(h) {
      const a = e.get.call(this);
      e.set.call(this, h), this.requestUpdate(n, a, r, !0, h);
    }, init(h) {
      return h !== void 0 && this.C(n, void 0, r, h), h;
    } };
  }
  if (s === "setter") {
    const { name: n } = t;
    return function(h) {
      const a = this[n];
      e.call(this, h), this.requestUpdate(n, a, r, !0, h);
    };
  }
  throw Error("Unsupported decorator location: " + s);
};
function _e(r) {
  return (e, t) => typeof t == "object" ? Ie(r, e, t) : ((s, i, o) => {
    const n = i.hasOwnProperty(o);
    return i.constructor.createProperty(o, s), n ? Object.getOwnPropertyDescriptor(i, o) : void 0;
  })(r, e, t);
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function $(r) {
  return _e({ ...r, state: !0, attribute: !1 });
}
var W = /* @__PURE__ */ ((r) => (r.GET_CONFIG = "meraki_ha/get_config", r.SUBSCRIBE_MERAKI_DATA = "meraki_ha/subscribe_meraki_data", r.GET_CAMERA_STREAM_URL = "meraki_ha/get_camera_stream_url", r.GET_CAMERA_SNAPSHOT = "meraki_ha/get_camera_snapshot", r.GET_VERSION = "meraki_ha/get_version", r.GET_NETWORK_EVENTS = "meraki_ha/get_network_events", r.UPDATE_ENABLED_NETWORKS = "meraki_ha/update_enabled_networks", r.CREATE_GUEST_KEY = "meraki_ha/ipsk/create", r.GET_GUEST_KEYS = "meraki_ha/ipsk/get", r.REVOKE_GUEST_KEY = "meraki_ha/ipsk/revoke", r.TIMED_ACCESS_GET_POLICIES = "meraki_ha/timed_access/get_policies", r))(W || {});
const ae = async (r, e) => {
  if (!r)
    throw new Error("Home Assistant object is not available.");
  try {
    if (typeof r.callWS == "function")
      return await r.callWS(e);
    if (r.connection && typeof r.connection.sendMessagePromise == "function")
      return await r.connection.sendMessagePromise(e);
    throw new Error("Home Assistant WebSocket communication methods not found.");
  } catch (t) {
    throw console.error(`Meraki HA: WebSocket error [${e.type}]:`, t), t;
  }
};
var De = Object.defineProperty, je = Object.getOwnPropertyDescriptor, _ = (r, e, t, s) => {
  for (var i = s > 1 ? void 0 : s ? je(e, t) : e, o = r.length - 1, n; o >= 0; o--)
    (n = r[o]) && (i = (s ? n(e, t, i) : n(i)) || i);
  return s && i && De(e, t, i), i;
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
        const e = await this.hass.callWS({
          type: "config_entries/get",
          domain: "meraki_ha"
        }), t = ((r = this._config) == null ? void 0 : r.config_entry_id) || (e.length > 0 ? e[0].entry_id : null);
        if (!t) {
          this._error = "Meraki integration not found. Please configure it first.", this._loading = !1;
          return;
        }
        const s = await ae(this.hass, {
          type: W.GET_CONFIG,
          config_entry_id: t
        });
        this._networks = (Array.isArray(s.networks) ? s.networks : []).filter((i) => {
          var o;
          return (o = i.productTypes) == null ? void 0 : o.includes("wireless");
        }), this._ssids = Array.isArray(s.ssids) ? s.ssids : [], this._networks.length > 0 && !this._selectedNetwork && (this._selectedNetwork = this._networks[0].id, this._fetchPolicies(this._selectedNetwork, t));
      } catch (e) {
        this._error = `Failed to fetch Meraki data: ${e.message || e}`;
      } finally {
        this._loading = !1;
      }
    }
  }
  async _fetchPolicies(r, e) {
    var t;
    if (this.hass)
      try {
        let s = e || ((t = this._config) == null ? void 0 : t.config_entry_id);
        if (!s) {
          const o = await this.hass.callWS({
            type: "config_entries/get",
            domain: "meraki_ha"
          });
          s = o.length > 0 ? o[0].entry_id : void 0;
        }
        if (!s) return;
        const i = await ae(this.hass, {
          type: W.TIMED_ACCESS_GET_POLICIES,
          config_entry_id: s,
          networkId: r
        });
        this._policies = Array.isArray(i) ? i : (i == null ? void 0 : i.policies) || [];
      } catch (s) {
        console.error("Failed to fetch policies:", s), this._policies = [];
      }
  }
  render() {
    var e, t;
    if (this._loading && !this._networks.length)
      return v`
        <ha-card .header="${((e = this._config) == null ? void 0 : e.name) || "Meraki Guest Access"}">
          <div class="card-content flex justify-center p-8">
            <ha-circular-progress active></ha-circular-progress>
          </div>
        </ha-card>
      `;
    const r = (this._ssids || []).filter((s) => s.networkId === this._selectedNetwork);
    return v`
      <ha-card .header="${((t = this._config) == null ? void 0 : t.name) || "Meraki Guest Access"}">
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
              ${(this._networks || []).map(
      (s) => v`<md-select-option .value="${String(s.id)}">${s.name}</md-select-option>`
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
              ${(r || []).map(
      (s) => v`<md-select-option .value="${String(s.number)}">${s.name} (SSID ${s.number})</md-select-option>`
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
              <md-select-option .value="">None (Default)</md-select-option>
              ${(this._policies || []).map(
      (s) => v`<md-select-option .value="${String(s.groupPolicyId)}">${s.name}</md-select-option>`
    )}
            </ha-select>

            <ha-select
              label="Duration"
              .value="${this._duration}"
              @selected="${(s) => this._duration = s.target.value}"
              fixedMenuPosition
              naturalMenuWidth
            >
              <md-select-option .value="${"30"}">30 Minutes</md-select-option>
              <md-select-option .value="${"60"}">1 Hour</md-select-option>
              <md-select-option .value="${"240"}">4 Hours</md-select-option>
              <md-select-option .value="${"1440"}">24 Hours</md-select-option>
              <md-select-option .value="${"10080"}">7 Days</md-select-option>
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
    const e = r.target.value;
    e !== this._selectedNetwork && (this._selectedNetwork = e, this._selectedSsid = "", this._selectedPolicy = "", this._fetchPolicies(e));
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
u.styles = fe`
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
  _e({ attribute: !1 })
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
  He("meraki-guest-access-card")
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
