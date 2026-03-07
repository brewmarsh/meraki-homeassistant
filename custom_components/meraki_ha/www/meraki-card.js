/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const ft = globalThis, Ht = ft.ShadowRoot && (ft.ShadyCSS === void 0 || ft.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, Ft = Symbol(), Zt = /* @__PURE__ */ new WeakMap();
let ge = class {
  constructor(t, e, s) {
    if (this._$cssResult$ = !0, s !== Ft) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = t, this.t = e;
  }
  get styleSheet() {
    let t = this.o;
    const e = this.t;
    if (Ht && t === void 0) {
      const s = e !== void 0 && e.length === 1;
      s && (t = Zt.get(e)), t === void 0 && ((this.o = t = new CSSStyleSheet()).replaceSync(this.cssText), s && Zt.set(e, t));
    }
    return t;
  }
  toString() {
    return this.cssText;
  }
};
const Ue = (n) => new ge(typeof n == "string" ? n : n + "", void 0, Ft), zt = (n, ...t) => {
  const e = n.length === 1 ? n[0] : t.reduce((s, i, r) => s + ((o) => {
    if (o._$cssResult$ === !0) return o.cssText;
    if (typeof o == "number") return o;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + o + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(i) + n[r + 1], n[0]);
  return new ge(e, n, Ft);
}, Le = (n, t) => {
  if (Ht) n.adoptedStyleSheets = t.map((e) => e instanceof CSSStyleSheet ? e : e.styleSheet);
  else for (const e of t) {
    const s = document.createElement("style"), i = ft.litNonce;
    i !== void 0 && s.setAttribute("nonce", i), s.textContent = e.cssText, n.appendChild(s);
  }
}, Xt = Ht ? (n) => n : (n) => n instanceof CSSStyleSheet ? ((t) => {
  let e = "";
  for (const s of t.cssRules) e += s.cssText;
  return Ue(e);
})(n) : n;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: Oe, defineProperty: xe, getOwnPropertyDescriptor: He, getOwnPropertyNames: Fe, getOwnPropertySymbols: ze, getPrototypeOf: Ve } = Object, L = globalThis, te = L.trustedTypes, je = te ? te.emptyScript : "", $t = L.reactiveElementPolyfillSupport, tt = (n, t) => n, gt = { toAttribute(n, t) {
  switch (t) {
    case Boolean:
      n = n ? je : null;
      break;
    case Object:
    case Array:
      n = n == null ? n : JSON.stringify(n);
  }
  return n;
}, fromAttribute(n, t) {
  let e = n;
  switch (t) {
    case Boolean:
      e = n !== null;
      break;
    case Number:
      e = n === null ? null : Number(n);
      break;
    case Object:
    case Array:
      try {
        e = JSON.parse(n);
      } catch {
        e = null;
      }
  }
  return e;
} }, Vt = (n, t) => !Oe(n, t), ee = { attribute: !0, type: String, converter: gt, reflect: !1, useDefault: !1, hasChanged: Vt };
Symbol.metadata ?? (Symbol.metadata = Symbol("metadata")), L.litPropertyMetadata ?? (L.litPropertyMetadata = /* @__PURE__ */ new WeakMap());
let K = class extends HTMLElement {
  static addInitializer(t) {
    this._$Ei(), (this.l ?? (this.l = [])).push(t);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(t, e = ee) {
    if (e.state && (e.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(t) && ((e = Object.create(e)).wrapped = !0), this.elementProperties.set(t, e), !e.noAccessor) {
      const s = Symbol(), i = this.getPropertyDescriptor(t, s, e);
      i !== void 0 && xe(this.prototype, t, i);
    }
  }
  static getPropertyDescriptor(t, e, s) {
    const { get: i, set: r } = He(this.prototype, t) ?? { get() {
      return this[e];
    }, set(o) {
      this[e] = o;
    } };
    return { get: i, set(o) {
      const c = i == null ? void 0 : i.call(this);
      r == null || r.call(this, o), this.requestUpdate(t, c, s);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(t) {
    return this.elementProperties.get(t) ?? ee;
  }
  static _$Ei() {
    if (this.hasOwnProperty(tt("elementProperties"))) return;
    const t = Ve(this);
    t.finalize(), t.l !== void 0 && (this.l = [...t.l]), this.elementProperties = new Map(t.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(tt("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(tt("properties"))) {
      const e = this.properties, s = [...Fe(e), ...ze(e)];
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
      for (const i of s) e.unshift(Xt(i));
    } else t !== void 0 && e.push(Xt(t));
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
    return Le(t, this.constructor.elementStyles), t;
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
    var r;
    const s = this.constructor.elementProperties.get(t), i = this.constructor._$Eu(t, s);
    if (i !== void 0 && s.reflect === !0) {
      const o = (((r = s.converter) == null ? void 0 : r.toAttribute) !== void 0 ? s.converter : gt).toAttribute(e, s.type);
      this._$Em = t, o == null ? this.removeAttribute(i) : this.setAttribute(i, o), this._$Em = null;
    }
  }
  _$AK(t, e) {
    var r, o;
    const s = this.constructor, i = s._$Eh.get(t);
    if (i !== void 0 && this._$Em !== i) {
      const c = s.getPropertyOptions(i), a = typeof c.converter == "function" ? { fromAttribute: c.converter } : ((r = c.converter) == null ? void 0 : r.fromAttribute) !== void 0 ? c.converter : gt;
      this._$Em = i;
      const l = a.fromAttribute(e, c.type);
      this[i] = l ?? ((o = this._$Ej) == null ? void 0 : o.get(i)) ?? l, this._$Em = null;
    }
  }
  requestUpdate(t, e, s, i = !1, r) {
    var o;
    if (t !== void 0) {
      const c = this.constructor;
      if (i === !1 && (r = this[t]), s ?? (s = c.getPropertyOptions(t)), !((s.hasChanged ?? Vt)(r, e) || s.useDefault && s.reflect && r === ((o = this._$Ej) == null ? void 0 : o.get(t)) && !this.hasAttribute(c._$Eu(t, s)))) return;
      this.C(t, e, s);
    }
    this.isUpdatePending === !1 && (this._$ES = this._$EP());
  }
  C(t, e, { useDefault: s, reflect: i, wrapped: r }, o) {
    s && !(this._$Ej ?? (this._$Ej = /* @__PURE__ */ new Map())).has(t) && (this._$Ej.set(t, o ?? e ?? this[t]), r !== !0 || o !== void 0) || (this._$AL.has(t) || (this.hasUpdated || s || (e = void 0), this._$AL.set(t, e)), i === !0 && this._$Em !== t && (this._$Eq ?? (this._$Eq = /* @__PURE__ */ new Set())).add(t));
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
        for (const [r, o] of this._$Ep) this[r] = o;
        this._$Ep = void 0;
      }
      const i = this.constructor.elementProperties;
      if (i.size > 0) for (const [r, o] of i) {
        const { wrapped: c } = o, a = this[r];
        c !== !0 || this._$AL.has(r) || a === void 0 || this.C(r, void 0, o, a);
      }
    }
    let t = !1;
    const e = this._$AL;
    try {
      t = this.shouldUpdate(e), t ? (this.willUpdate(e), (s = this._$EO) == null || s.forEach((i) => {
        var r;
        return (r = i.hostUpdate) == null ? void 0 : r.call(i);
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
K.elementStyles = [], K.shadowRootOptions = { mode: "open" }, K[tt("elementProperties")] = /* @__PURE__ */ new Map(), K[tt("finalized")] = /* @__PURE__ */ new Map(), $t == null || $t({ ReactiveElement: K }), (L.reactiveElementVersions ?? (L.reactiveElementVersions = [])).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const et = globalThis, ne = (n) => n, pt = et.trustedTypes, ie = pt ? pt.createPolicy("lit-html", { createHTML: (n) => n }) : void 0, pe = "$lit$", D = `lit$${Math.random().toFixed(9).slice(2)}$`, _e = "?" + D, Ke = `<${_e}>`, V = document, it = () => V.createComment(""), st = (n) => n === null || typeof n != "object" && typeof n != "function", jt = Array.isArray, Ge = (n) => jt(n) || typeof (n == null ? void 0 : n[Symbol.iterator]) == "function", Pt = `[
\f\r]`, X = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, se = /-->/g, re = />/g, x = RegExp(`>|${Pt}(?:([^\\s"'>=/]+)(${Pt}*=${Pt}*(?:[^
\f\r"'\`<>=]|("|')|))|$)`, "g"), oe = /'/g, ae = /"/g, me = /^(?:script|style|textarea|title)$/i, qe = (n) => (t, ...e) => ({ _$litType$: n, strings: t, values: e }), N = qe(1), G = Symbol.for("lit-noChange"), b = Symbol.for("lit-nothing"), ce = /* @__PURE__ */ new WeakMap(), H = V.createTreeWalker(V, 129);
function ye(n, t) {
  if (!jt(n) || !n.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return ie !== void 0 ? ie.createHTML(t) : t;
}
const Je = (n, t) => {
  const e = n.length - 1, s = [];
  let i, r = t === 2 ? "<svg>" : t === 3 ? "<math>" : "", o = X;
  for (let c = 0; c < e; c++) {
    const a = n[c];
    let l, h, f = -1, d = 0;
    for (; d < a.length && (o.lastIndex = d, h = o.exec(a), h !== null); ) d = o.lastIndex, o === X ? h[1] === "!--" ? o = se : h[1] !== void 0 ? o = re : h[2] !== void 0 ? (me.test(h[2]) && (i = RegExp("</" + h[2], "g")), o = x) : h[3] !== void 0 && (o = x) : o === x ? h[0] === ">" ? (o = i ?? X, f = -1) : h[1] === void 0 ? f = -2 : (f = o.lastIndex - h[2].length, l = h[1], o = h[3] === void 0 ? x : h[3] === '"' ? ae : oe) : o === ae || o === oe ? o = x : o === se || o === re ? o = X : (o = x, i = void 0);
    const u = o === x && n[c + 1].startsWith("/>") ? " " : "";
    r += o === X ? a + Ke : f >= 0 ? (s.push(l), a.slice(0, f) + pe + a.slice(f) + D + u) : a + D + (f === -2 ? c : u);
  }
  return [ye(n, r + (n[e] || "<?>") + (t === 2 ? "</svg>" : t === 3 ? "</math>" : "")), s];
};
class rt {
  constructor({ strings: t, _$litType$: e }, s) {
    let i;
    this.parts = [];
    let r = 0, o = 0;
    const c = t.length - 1, a = this.parts, [l, h] = Je(t, e);
    if (this.el = rt.createElement(l, s), H.currentNode = this.el.content, e === 2 || e === 3) {
      const f = this.el.content.firstChild;
      f.replaceWith(...f.childNodes);
    }
    for (; (i = H.nextNode()) !== null && a.length < c; ) {
      if (i.nodeType === 1) {
        if (i.hasAttributes()) for (const f of i.getAttributeNames()) if (f.endsWith(pe)) {
          const d = h[o++], u = i.getAttribute(f).split(D), _ = /([.?@])?(.*)/.exec(d);
          a.push({ type: 1, index: r, name: _[2], strings: u, ctor: _[1] === "." ? Ye : _[1] === "?" ? Qe : _[1] === "@" ? Ze : yt }), i.removeAttribute(f);
        } else f.startsWith(D) && (a.push({ type: 6, index: r }), i.removeAttribute(f));
        if (me.test(i.tagName)) {
          const f = i.textContent.split(D), d = f.length - 1;
          if (d > 0) {
            i.textContent = pt ? pt.emptyScript : "";
            for (let u = 0; u < d; u++) i.append(f[u], it()), H.nextNode(), a.push({ type: 2, index: ++r });
            i.append(f[d], it());
          }
        }
      } else if (i.nodeType === 8) if (i.data === _e) a.push({ type: 2, index: r });
      else {
        let f = -1;
        for (; (f = i.data.indexOf(D, f + 1)) !== -1; ) a.push({ type: 7, index: r }), f += D.length - 1;
      }
      r++;
    }
  }
  static createElement(t, e) {
    const s = V.createElement("template");
    return s.innerHTML = t, s;
  }
}
function q(n, t, e = n, s) {
  var o, c;
  if (t === G) return t;
  let i = s !== void 0 ? (o = e._$Co) == null ? void 0 : o[s] : e._$Cl;
  const r = st(t) ? void 0 : t._$litDirective$;
  return (i == null ? void 0 : i.constructor) !== r && ((c = i == null ? void 0 : i._$AO) == null || c.call(i, !1), r === void 0 ? i = void 0 : (i = new r(n), i._$AT(n, e, s)), s !== void 0 ? (e._$Co ?? (e._$Co = []))[s] = i : e._$Cl = i), i !== void 0 && (t = q(n, i._$AS(n, t.values), i, s)), t;
}
class We {
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
    const { el: { content: e }, parts: s } = this._$AD, i = ((t == null ? void 0 : t.creationScope) ?? V).importNode(e, !0);
    H.currentNode = i;
    let r = H.nextNode(), o = 0, c = 0, a = s[0];
    for (; a !== void 0; ) {
      if (o === a.index) {
        let l;
        a.type === 2 ? l = new ct(r, r.nextSibling, this, t) : a.type === 1 ? l = new a.ctor(r, a.name, a.strings, this, t) : a.type === 6 && (l = new Xe(r, this, t)), this._$AV.push(l), a = s[++c];
      }
      o !== (a == null ? void 0 : a.index) && (r = H.nextNode(), o++);
    }
    return H.currentNode = V, i;
  }
  p(t) {
    let e = 0;
    for (const s of this._$AV) s !== void 0 && (s.strings !== void 0 ? (s._$AI(t, s, e), e += s.strings.length - 2) : s._$AI(t[e])), e++;
  }
}
class ct {
  get _$AU() {
    var t;
    return ((t = this._$AM) == null ? void 0 : t._$AU) ?? this._$Cv;
  }
  constructor(t, e, s, i) {
    this.type = 2, this._$AH = b, this._$AN = void 0, this._$AA = t, this._$AB = e, this._$AM = s, this.options = i, this._$Cv = (i == null ? void 0 : i.isConnected) ?? !0;
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
    t = q(this, t, e), st(t) ? t === b || t == null || t === "" ? (this._$AH !== b && this._$AR(), this._$AH = b) : t !== this._$AH && t !== G && this._(t) : t._$litType$ !== void 0 ? this.$(t) : t.nodeType !== void 0 ? this.T(t) : Ge(t) ? this.k(t) : this._(t);
  }
  O(t) {
    return this._$AA.parentNode.insertBefore(t, this._$AB);
  }
  T(t) {
    this._$AH !== t && (this._$AR(), this._$AH = this.O(t));
  }
  _(t) {
    this._$AH !== b && st(this._$AH) ? this._$AA.nextSibling.data = t : this.T(V.createTextNode(t)), this._$AH = t;
  }
  $(t) {
    var r;
    const { values: e, _$litType$: s } = t, i = typeof s == "number" ? this._$AC(t) : (s.el === void 0 && (s.el = rt.createElement(ye(s.h, s.h[0]), this.options)), s);
    if (((r = this._$AH) == null ? void 0 : r._$AD) === i) this._$AH.p(e);
    else {
      const o = new We(i, this), c = o.u(this.options);
      o.p(e), this.T(c), this._$AH = o;
    }
  }
  _$AC(t) {
    let e = ce.get(t.strings);
    return e === void 0 && ce.set(t.strings, e = new rt(t)), e;
  }
  k(t) {
    jt(this._$AH) || (this._$AH = [], this._$AR());
    const e = this._$AH;
    let s, i = 0;
    for (const r of t) i === e.length ? e.push(s = new ct(this.O(it()), this.O(it()), this, this.options)) : s = e[i], s._$AI(r), i++;
    i < e.length && (this._$AR(s && s._$AB.nextSibling, i), e.length = i);
  }
  _$AR(t = this._$AA.nextSibling, e) {
    var s;
    for ((s = this._$AP) == null ? void 0 : s.call(this, !1, !0, e); t !== this._$AB; ) {
      const i = ne(t).nextSibling;
      ne(t).remove(), t = i;
    }
  }
  setConnected(t) {
    var e;
    this._$AM === void 0 && (this._$Cv = t, (e = this._$AP) == null || e.call(this, t));
  }
}
class yt {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(t, e, s, i, r) {
    this.type = 1, this._$AH = b, this._$AN = void 0, this.element = t, this.name = e, this._$AM = i, this.options = r, s.length > 2 || s[0] !== "" || s[1] !== "" ? (this._$AH = Array(s.length - 1).fill(new String()), this.strings = s) : this._$AH = b;
  }
  _$AI(t, e = this, s, i) {
    const r = this.strings;
    let o = !1;
    if (r === void 0) t = q(this, t, e, 0), o = !st(t) || t !== this._$AH && t !== G, o && (this._$AH = t);
    else {
      const c = t;
      let a, l;
      for (t = r[0], a = 0; a < r.length - 1; a++) l = q(this, c[s + a], e, a), l === G && (l = this._$AH[a]), o || (o = !st(l) || l !== this._$AH[a]), l === b ? t = b : t !== b && (t += (l ?? "") + r[a + 1]), this._$AH[a] = l;
    }
    o && !i && this.j(t);
  }
  j(t) {
    t === b ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, t ?? "");
  }
}
class Ye extends yt {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(t) {
    this.element[this.name] = t === b ? void 0 : t;
  }
}
class Qe extends yt {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(t) {
    this.element.toggleAttribute(this.name, !!t && t !== b);
  }
}
class Ze extends yt {
  constructor(t, e, s, i, r) {
    super(t, e, s, i, r), this.type = 5;
  }
  _$AI(t, e = this) {
    if ((t = q(this, t, e, 0) ?? b) === G) return;
    const s = this._$AH, i = t === b && s !== b || t.capture !== s.capture || t.once !== s.once || t.passive !== s.passive, r = t !== b && (s === b || i);
    i && this.element.removeEventListener(this.name, this, s), r && this.element.addEventListener(this.name, this, t), this._$AH = t;
  }
  handleEvent(t) {
    var e;
    typeof this._$AH == "function" ? this._$AH.call(((e = this.options) == null ? void 0 : e.host) ?? this.element, t) : this._$AH.handleEvent(t);
  }
}
class Xe {
  constructor(t, e, s) {
    this.element = t, this.type = 6, this._$AN = void 0, this._$AM = e, this.options = s;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t) {
    q(this, t);
  }
}
const Nt = et.litHtmlPolyfillSupport;
Nt == null || Nt(rt, ct), (et.litHtmlVersions ?? (et.litHtmlVersions = [])).push("3.3.2");
const tn = (n, t, e) => {
  const s = (e == null ? void 0 : e.renderBefore) ?? t;
  let i = s._$litPart$;
  if (i === void 0) {
    const r = (e == null ? void 0 : e.renderBefore) ?? null;
    s._$litPart$ = i = new ct(t.insertBefore(it(), r), r, void 0, e ?? {});
  }
  return i._$AI(n), i;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const F = globalThis;
class z extends K {
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
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Do = tn(e, this.renderRoot, this.renderOptions);
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
    return G;
  }
}
var fe;
z._$litElement$ = !0, z.finalized = !0, (fe = F.litElementHydrateSupport) == null || fe.call(F, { LitElement: z });
const Tt = F.litElementPolyfillSupport;
Tt == null || Tt({ LitElement: z });
(F.litElementVersions ?? (F.litElementVersions = [])).push("4.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const we = (n) => (t, e) => {
  e !== void 0 ? e.addInitializer(() => {
    customElements.define(n, t);
  }) : customElements.define(n, t);
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const en = { attribute: !0, type: String, converter: gt, reflect: !1, hasChanged: Vt }, nn = (n = en, t, e) => {
  const { kind: s, metadata: i } = e;
  let r = globalThis.litPropertyMetadata.get(i);
  if (r === void 0 && globalThis.litPropertyMetadata.set(i, r = /* @__PURE__ */ new Map()), s === "setter" && ((n = Object.create(n)).wrapped = !0), r.set(e.name, n), s === "accessor") {
    const { name: o } = e;
    return { set(c) {
      const a = t.get.call(this);
      t.set.call(this, c), this.requestUpdate(o, a, n, !0, c);
    }, init(c) {
      return c !== void 0 && this.C(o, void 0, n, c), c;
    } };
  }
  if (s === "setter") {
    const { name: o } = e;
    return function(c) {
      const a = this[o];
      t.call(this, c), this.requestUpdate(o, a, n, !0, c);
    };
  }
  throw Error("Unsupported decorator location: " + s);
};
function wt(n) {
  return (t, e) => typeof e == "object" ? nn(n, t, e) : ((s, i, r) => {
    const o = i.hasOwnProperty(r);
    return i.constructor.createProperty(r, s), o ? Object.getOwnPropertyDescriptor(i, r) : void 0;
  })(n, t, e);
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function v(n) {
  return wt({ ...n, state: !0, attribute: !1 });
}
var sn = Object.defineProperty, rn = Object.getOwnPropertyDescriptor, Kt = (n, t, e, s) => {
  for (var i = s > 1 ? void 0 : s ? rn(t, e) : t, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = (s ? o(t, e, i) : o(i)) || i);
  return s && i && sn(t, e, i), i;
};
let ot = class extends z {
  setConfig(n) {
    if (!n || !n.entity)
      throw new Error("Please define a Meraki content filter entity");
    this._config = n;
  }
  static getStubConfig() {
    return {
      entity: "select.meraki_network_content_filter",
      name: "Meraki Content Filter"
    };
  }
  render() {
    if (!this._config || !this.hass)
      return N``;
    const n = this._config.entity, t = this.hass.states[n];
    if (!t)
      return N`
        <ha-card>
          <div class="card-content">
            <ha-alert alert-type="error">Entity not found: ${n}</ha-alert>
          </div>
        </ha-card>
      `;
    const e = t.state, s = t.attributes.options || ["None", "Security", "Family", "Strict"], i = this._config.name || t.attributes.friendly_name || "Content Filter";
    return N`
      <ha-card>
        <div class="card-header">${i}</div>
        <div class="card-content">
          <div class="current-profile">
            Current Profile: <strong>${e}</strong>
          </div>
          <div class="profile-buttons">
            ${s.map((r) => N`
              <div
                class="profile-button ${e === r ? "active" : ""}"
                @click="${() => this._handleProfileSelect(r)}"
              >
                <span class="profile-name">${r}</span>
              </div>
            `)}
          </div>
        </div>
      </ha-card>
    `;
  }
  async _handleProfileSelect(n) {
    if (!(!this.hass || !this._config))
      try {
        await this.hass.callService("select", "select_option", {
          entity_id: this._config.entity,
          option: n
        });
      } catch (t) {
        console.error("Failed to call select_option service:", t);
      }
  }
};
ot.styles = zt`
    :host {
      display: block;
    }
    ha-card {
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .card-header {
      padding: 16px 16px 0;
      font-size: 24px;
      line-height: 1.2;
    }
    .card-content {
      padding: 16px;
    }
    .network-name {
      font-weight: 500;
      margin-bottom: 4px;
    }
    .current-profile {
      color: var(--secondary-text-color);
      font-size: 0.9em;
      margin-bottom: 16px;
    }
    .profile-buttons {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .profile-button {
      flex: 1 1 calc(50% - 4px);
      --mdc-theme-primary: var(--primary-text-color);
      --mdc-theme-on-primary: var(--card-background-color);
      border: 1px solid var(--divider-color);
      border-radius: 8px;
      padding: 8px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s ease-in-out;
      background-color: var(--card-background-color);
    }
    .profile-button:hover {
      background-color: var(--secondary-background-color);
    }
    .profile-button.active {
      background-color: var(--primary-color);
      color: var(--text-primary-color);
      border-color: var(--primary-color);
    }
    .profile-button.active .profile-name {
       color: var(--text-primary-color);
    }
    .profile-name {
      font-weight: bold;
      display: block;
    }
  `;
Kt([
  wt({ attribute: !1 })
], ot.prototype, "hass", 2);
Kt([
  v()
], ot.prototype, "_config", 2);
ot = Kt([
  we("meraki-content-filter-card")
], ot);
window.customCards = window.customCards || [];
window.customCards.push({
  type: "meraki-content-filter-card",
  name: "Meraki Content Filter",
  description: "Control Meraki Content Filtering profiles.",
  preview: !0
});
var lt = {}, on = function() {
  return typeof Promise == "function" && Promise.prototype && Promise.prototype.then;
}, Ee = {}, T = {};
let Gt;
const an = [
  0,
  // Not used
  26,
  44,
  70,
  100,
  134,
  172,
  196,
  242,
  292,
  346,
  404,
  466,
  532,
  581,
  655,
  733,
  815,
  901,
  991,
  1085,
  1156,
  1258,
  1364,
  1474,
  1588,
  1706,
  1828,
  1921,
  2051,
  2185,
  2323,
  2465,
  2611,
  2761,
  2876,
  3034,
  3196,
  3362,
  3532,
  3706
];
T.getSymbolSize = function(t) {
  if (!t) throw new Error('"version" cannot be null or undefined');
  if (t < 1 || t > 40) throw new Error('"version" should be in range from 1 to 40');
  return t * 4 + 17;
};
T.getSymbolTotalCodewords = function(t) {
  return an[t];
};
T.getBCHDigit = function(n) {
  let t = 0;
  for (; n !== 0; )
    t++, n >>>= 1;
  return t;
};
T.setToSJISFunction = function(t) {
  if (typeof t != "function")
    throw new Error('"toSJISFunc" is not a valid function.');
  Gt = t;
};
T.isKanjiModeEnabled = function() {
  return typeof Gt < "u";
};
T.toSJIS = function(t) {
  return Gt(t);
};
var Et = {};
(function(n) {
  n.L = { bit: 1 }, n.M = { bit: 0 }, n.Q = { bit: 3 }, n.H = { bit: 2 };
  function t(e) {
    if (typeof e != "string")
      throw new Error("Param is not a string");
    switch (e.toLowerCase()) {
      case "l":
      case "low":
        return n.L;
      case "m":
      case "medium":
        return n.M;
      case "q":
      case "quartile":
        return n.Q;
      case "h":
      case "high":
        return n.H;
      default:
        throw new Error("Unknown EC Level: " + e);
    }
  }
  n.isValid = function(s) {
    return s && typeof s.bit < "u" && s.bit >= 0 && s.bit < 4;
  }, n.from = function(s, i) {
    if (n.isValid(s))
      return s;
    try {
      return t(s);
    } catch {
      return i;
    }
  };
})(Et);
function Ae() {
  this.buffer = [], this.length = 0;
}
Ae.prototype = {
  get: function(n) {
    const t = Math.floor(n / 8);
    return (this.buffer[t] >>> 7 - n % 8 & 1) === 1;
  },
  put: function(n, t) {
    for (let e = 0; e < t; e++)
      this.putBit((n >>> t - e - 1 & 1) === 1);
  },
  getLengthInBits: function() {
    return this.length;
  },
  putBit: function(n) {
    const t = Math.floor(this.length / 8);
    this.buffer.length <= t && this.buffer.push(0), n && (this.buffer[t] |= 128 >>> this.length % 8), this.length++;
  }
};
var cn = Ae;
function ht(n) {
  if (!n || n < 1)
    throw new Error("BitMatrix size must be defined and greater than 0");
  this.size = n, this.data = new Uint8Array(n * n), this.reservedBit = new Uint8Array(n * n);
}
ht.prototype.set = function(n, t, e, s) {
  const i = n * this.size + t;
  this.data[i] = e, s && (this.reservedBit[i] = !0);
};
ht.prototype.get = function(n, t) {
  return this.data[n * this.size + t];
};
ht.prototype.xor = function(n, t, e) {
  this.data[n * this.size + t] ^= e;
};
ht.prototype.isReserved = function(n, t) {
  return this.reservedBit[n * this.size + t];
};
var ln = ht, Se = {};
(function(n) {
  const t = T.getSymbolSize;
  n.getRowColCoords = function(s) {
    if (s === 1) return [];
    const i = Math.floor(s / 7) + 2, r = t(s), o = r === 145 ? 26 : Math.ceil((r - 13) / (2 * i - 2)) * 2, c = [r - 7];
    for (let a = 1; a < i - 1; a++)
      c[a] = c[a - 1] - o;
    return c.push(6), c.reverse();
  }, n.getPositions = function(s) {
    const i = [], r = n.getRowColCoords(s), o = r.length;
    for (let c = 0; c < o; c++)
      for (let a = 0; a < o; a++)
        c === 0 && a === 0 || // top-left
        c === 0 && a === o - 1 || // bottom-left
        c === o - 1 && a === 0 || i.push([r[c], r[a]]);
    return i;
  };
})(Se);
var Ce = {};
const hn = T.getSymbolSize, le = 7;
Ce.getPositions = function(t) {
  const e = hn(t);
  return [
    // top-left
    [0, 0],
    // top-right
    [e - le, 0],
    // bottom-left
    [0, e - le]
  ];
};
var be = {};
(function(n) {
  n.Patterns = {
    PATTERN000: 0,
    PATTERN001: 1,
    PATTERN010: 2,
    PATTERN011: 3,
    PATTERN100: 4,
    PATTERN101: 5,
    PATTERN110: 6,
    PATTERN111: 7
  };
  const t = {
    N1: 3,
    N2: 3,
    N3: 40,
    N4: 10
  };
  n.isValid = function(i) {
    return i != null && i !== "" && !isNaN(i) && i >= 0 && i <= 7;
  }, n.from = function(i) {
    return n.isValid(i) ? parseInt(i, 10) : void 0;
  }, n.getPenaltyN1 = function(i) {
    const r = i.size;
    let o = 0, c = 0, a = 0, l = null, h = null;
    for (let f = 0; f < r; f++) {
      c = a = 0, l = h = null;
      for (let d = 0; d < r; d++) {
        let u = i.get(f, d);
        u === l ? c++ : (c >= 5 && (o += t.N1 + (c - 5)), l = u, c = 1), u = i.get(d, f), u === h ? a++ : (a >= 5 && (o += t.N1 + (a - 5)), h = u, a = 1);
      }
      c >= 5 && (o += t.N1 + (c - 5)), a >= 5 && (o += t.N1 + (a - 5));
    }
    return o;
  }, n.getPenaltyN2 = function(i) {
    const r = i.size;
    let o = 0;
    for (let c = 0; c < r - 1; c++)
      for (let a = 0; a < r - 1; a++) {
        const l = i.get(c, a) + i.get(c, a + 1) + i.get(c + 1, a) + i.get(c + 1, a + 1);
        (l === 4 || l === 0) && o++;
      }
    return o * t.N2;
  }, n.getPenaltyN3 = function(i) {
    const r = i.size;
    let o = 0, c = 0, a = 0;
    for (let l = 0; l < r; l++) {
      c = a = 0;
      for (let h = 0; h < r; h++)
        c = c << 1 & 2047 | i.get(l, h), h >= 10 && (c === 1488 || c === 93) && o++, a = a << 1 & 2047 | i.get(h, l), h >= 10 && (a === 1488 || a === 93) && o++;
    }
    return o * t.N3;
  }, n.getPenaltyN4 = function(i) {
    let r = 0;
    const o = i.data.length;
    for (let a = 0; a < o; a++) r += i.data[a];
    return Math.abs(Math.ceil(r * 100 / o / 5) - 10) * t.N4;
  };
  function e(s, i, r) {
    switch (s) {
      case n.Patterns.PATTERN000:
        return (i + r) % 2 === 0;
      case n.Patterns.PATTERN001:
        return i % 2 === 0;
      case n.Patterns.PATTERN010:
        return r % 3 === 0;
      case n.Patterns.PATTERN011:
        return (i + r) % 3 === 0;
      case n.Patterns.PATTERN100:
        return (Math.floor(i / 2) + Math.floor(r / 3)) % 2 === 0;
      case n.Patterns.PATTERN101:
        return i * r % 2 + i * r % 3 === 0;
      case n.Patterns.PATTERN110:
        return (i * r % 2 + i * r % 3) % 2 === 0;
      case n.Patterns.PATTERN111:
        return (i * r % 3 + (i + r) % 2) % 2 === 0;
      default:
        throw new Error("bad maskPattern:" + s);
    }
  }
  n.applyMask = function(i, r) {
    const o = r.size;
    for (let c = 0; c < o; c++)
      for (let a = 0; a < o; a++)
        r.isReserved(a, c) || r.xor(a, c, e(i, a, c));
  }, n.getBestMask = function(i, r) {
    const o = Object.keys(n.Patterns).length;
    let c = 0, a = 1 / 0;
    for (let l = 0; l < o; l++) {
      r(l), n.applyMask(l, i);
      const h = n.getPenaltyN1(i) + n.getPenaltyN2(i) + n.getPenaltyN3(i) + n.getPenaltyN4(i);
      n.applyMask(l, i), h < a && (a = h, c = l);
    }
    return c;
  };
})(be);
var At = {};
const U = Et, ut = [
  // L  M  Q  H
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  2,
  2,
  1,
  2,
  2,
  4,
  1,
  2,
  4,
  4,
  2,
  4,
  4,
  4,
  2,
  4,
  6,
  5,
  2,
  4,
  6,
  6,
  2,
  5,
  8,
  8,
  4,
  5,
  8,
  8,
  4,
  5,
  8,
  11,
  4,
  8,
  10,
  11,
  4,
  9,
  12,
  16,
  4,
  9,
  16,
  16,
  6,
  10,
  12,
  18,
  6,
  10,
  17,
  16,
  6,
  11,
  16,
  19,
  6,
  13,
  18,
  21,
  7,
  14,
  21,
  25,
  8,
  16,
  20,
  25,
  8,
  17,
  23,
  25,
  9,
  17,
  23,
  34,
  9,
  18,
  25,
  30,
  10,
  20,
  27,
  32,
  12,
  21,
  29,
  35,
  12,
  23,
  34,
  37,
  12,
  25,
  34,
  40,
  13,
  26,
  35,
  42,
  14,
  28,
  38,
  45,
  15,
  29,
  40,
  48,
  16,
  31,
  43,
  51,
  17,
  33,
  45,
  54,
  18,
  35,
  48,
  57,
  19,
  37,
  51,
  60,
  19,
  38,
  53,
  63,
  20,
  40,
  56,
  66,
  21,
  43,
  59,
  70,
  22,
  45,
  62,
  74,
  24,
  47,
  65,
  77,
  25,
  49,
  68,
  81
], dt = [
  // L  M  Q  H
  7,
  10,
  13,
  17,
  10,
  16,
  22,
  28,
  15,
  26,
  36,
  44,
  20,
  36,
  52,
  64,
  26,
  48,
  72,
  88,
  36,
  64,
  96,
  112,
  40,
  72,
  108,
  130,
  48,
  88,
  132,
  156,
  60,
  110,
  160,
  192,
  72,
  130,
  192,
  224,
  80,
  150,
  224,
  264,
  96,
  176,
  260,
  308,
  104,
  198,
  288,
  352,
  120,
  216,
  320,
  384,
  132,
  240,
  360,
  432,
  144,
  280,
  408,
  480,
  168,
  308,
  448,
  532,
  180,
  338,
  504,
  588,
  196,
  364,
  546,
  650,
  224,
  416,
  600,
  700,
  224,
  442,
  644,
  750,
  252,
  476,
  690,
  816,
  270,
  504,
  750,
  900,
  300,
  560,
  810,
  960,
  312,
  588,
  870,
  1050,
  336,
  644,
  952,
  1110,
  360,
  700,
  1020,
  1200,
  390,
  728,
  1050,
  1260,
  420,
  784,
  1140,
  1350,
  450,
  812,
  1200,
  1440,
  480,
  868,
  1290,
  1530,
  510,
  924,
  1350,
  1620,
  540,
  980,
  1440,
  1710,
  570,
  1036,
  1530,
  1800,
  570,
  1064,
  1590,
  1890,
  600,
  1120,
  1680,
  1980,
  630,
  1204,
  1770,
  2100,
  660,
  1260,
  1860,
  2220,
  720,
  1316,
  1950,
  2310,
  750,
  1372,
  2040,
  2430
];
At.getBlocksCount = function(t, e) {
  switch (e) {
    case U.L:
      return ut[(t - 1) * 4 + 0];
    case U.M:
      return ut[(t - 1) * 4 + 1];
    case U.Q:
      return ut[(t - 1) * 4 + 2];
    case U.H:
      return ut[(t - 1) * 4 + 3];
    default:
      return;
  }
};
At.getTotalCodewordsCount = function(t, e) {
  switch (e) {
    case U.L:
      return dt[(t - 1) * 4 + 0];
    case U.M:
      return dt[(t - 1) * 4 + 1];
    case U.Q:
      return dt[(t - 1) * 4 + 2];
    case U.H:
      return dt[(t - 1) * 4 + 3];
    default:
      return;
  }
};
var ve = {}, St = {};
const nt = new Uint8Array(512), _t = new Uint8Array(256);
(function() {
  let t = 1;
  for (let e = 0; e < 255; e++)
    nt[e] = t, _t[t] = e, t <<= 1, t & 256 && (t ^= 285);
  for (let e = 255; e < 512; e++)
    nt[e] = nt[e - 255];
})();
St.log = function(t) {
  if (t < 1) throw new Error("log(" + t + ")");
  return _t[t];
};
St.exp = function(t) {
  return nt[t];
};
St.mul = function(t, e) {
  return t === 0 || e === 0 ? 0 : nt[_t[t] + _t[e]];
};
(function(n) {
  const t = St;
  n.mul = function(s, i) {
    const r = new Uint8Array(s.length + i.length - 1);
    for (let o = 0; o < s.length; o++)
      for (let c = 0; c < i.length; c++)
        r[o + c] ^= t.mul(s[o], i[c]);
    return r;
  }, n.mod = function(s, i) {
    let r = new Uint8Array(s);
    for (; r.length - i.length >= 0; ) {
      const o = r[0];
      for (let a = 0; a < i.length; a++)
        r[a] ^= t.mul(i[a], o);
      let c = 0;
      for (; c < r.length && r[c] === 0; ) c++;
      r = r.slice(c);
    }
    return r;
  }, n.generateECPolynomial = function(s) {
    let i = new Uint8Array([1]);
    for (let r = 0; r < s; r++)
      i = n.mul(i, new Uint8Array([1, t.exp(r)]));
    return i;
  };
})(ve);
const $e = ve;
function qt(n) {
  this.genPoly = void 0, this.degree = n, this.degree && this.initialize(this.degree);
}
qt.prototype.initialize = function(t) {
  this.degree = t, this.genPoly = $e.generateECPolynomial(this.degree);
};
qt.prototype.encode = function(t) {
  if (!this.genPoly)
    throw new Error("Encoder not initialized");
  const e = new Uint8Array(t.length + this.degree);
  e.set(t);
  const s = $e.mod(e, this.genPoly), i = this.degree - s.length;
  if (i > 0) {
    const r = new Uint8Array(this.degree);
    return r.set(s, i), r;
  }
  return s;
};
var un = qt, Pe = {}, O = {}, Jt = {};
Jt.isValid = function(t) {
  return !isNaN(t) && t >= 1 && t <= 40;
};
var k = {};
const Ne = "[0-9]+", dn = "[A-Z $%*+\\-./:]+";
let at = "(?:[u3000-u303F]|[u3040-u309F]|[u30A0-u30FF]|[uFF00-uFFEF]|[u4E00-u9FAF]|[u2605-u2606]|[u2190-u2195]|u203B|[u2010u2015u2018u2019u2025u2026u201Cu201Du2225u2260]|[u0391-u0451]|[u00A7u00A8u00B1u00B4u00D7u00F7])+";
at = at.replace(/u/g, "\\u");
const fn = "(?:(?![A-Z0-9 $%*+\\-./:]|" + at + `)(?:.|[\r
]))+`;
k.KANJI = new RegExp(at, "g");
k.BYTE_KANJI = new RegExp("[^A-Z0-9 $%*+\\-./:]+", "g");
k.BYTE = new RegExp(fn, "g");
k.NUMERIC = new RegExp(Ne, "g");
k.ALPHANUMERIC = new RegExp(dn, "g");
const gn = new RegExp("^" + at + "$"), pn = new RegExp("^" + Ne + "$"), _n = new RegExp("^[A-Z0-9 $%*+\\-./:]+$");
k.testKanji = function(t) {
  return gn.test(t);
};
k.testNumeric = function(t) {
  return pn.test(t);
};
k.testAlphanumeric = function(t) {
  return _n.test(t);
};
(function(n) {
  const t = Jt, e = k;
  n.NUMERIC = {
    id: "Numeric",
    bit: 1,
    ccBits: [10, 12, 14]
  }, n.ALPHANUMERIC = {
    id: "Alphanumeric",
    bit: 2,
    ccBits: [9, 11, 13]
  }, n.BYTE = {
    id: "Byte",
    bit: 4,
    ccBits: [8, 16, 16]
  }, n.KANJI = {
    id: "Kanji",
    bit: 8,
    ccBits: [8, 10, 12]
  }, n.MIXED = {
    bit: -1
  }, n.getCharCountIndicator = function(r, o) {
    if (!r.ccBits) throw new Error("Invalid mode: " + r);
    if (!t.isValid(o))
      throw new Error("Invalid version: " + o);
    return o >= 1 && o < 10 ? r.ccBits[0] : o < 27 ? r.ccBits[1] : r.ccBits[2];
  }, n.getBestModeForData = function(r) {
    return e.testNumeric(r) ? n.NUMERIC : e.testAlphanumeric(r) ? n.ALPHANUMERIC : e.testKanji(r) ? n.KANJI : n.BYTE;
  }, n.toString = function(r) {
    if (r && r.id) return r.id;
    throw new Error("Invalid mode");
  }, n.isValid = function(r) {
    return r && r.bit && r.ccBits;
  };
  function s(i) {
    if (typeof i != "string")
      throw new Error("Param is not a string");
    switch (i.toLowerCase()) {
      case "numeric":
        return n.NUMERIC;
      case "alphanumeric":
        return n.ALPHANUMERIC;
      case "kanji":
        return n.KANJI;
      case "byte":
        return n.BYTE;
      default:
        throw new Error("Unknown mode: " + i);
    }
  }
  n.from = function(r, o) {
    if (n.isValid(r))
      return r;
    try {
      return s(r);
    } catch {
      return o;
    }
  };
})(O);
(function(n) {
  const t = T, e = At, s = Et, i = O, r = Jt, o = 7973, c = t.getBCHDigit(o);
  function a(d, u, _) {
    for (let y = 1; y <= 40; y++)
      if (u <= n.getCapacity(y, _, d))
        return y;
  }
  function l(d, u) {
    return i.getCharCountIndicator(d, u) + 4;
  }
  function h(d, u) {
    let _ = 0;
    return d.forEach(function(y) {
      const $ = l(y.mode, u);
      _ += $ + y.getBitsLength();
    }), _;
  }
  function f(d, u) {
    for (let _ = 1; _ <= 40; _++)
      if (h(d, _) <= n.getCapacity(_, u, i.MIXED))
        return _;
  }
  n.from = function(u, _) {
    return r.isValid(u) ? parseInt(u, 10) : _;
  }, n.getCapacity = function(u, _, y) {
    if (!r.isValid(u))
      throw new Error("Invalid QR Code version");
    typeof y > "u" && (y = i.BYTE);
    const $ = t.getSymbolTotalCodewords(u), m = e.getTotalCodewordsCount(u, _), w = ($ - m) * 8;
    if (y === i.MIXED) return w;
    const p = w - l(y, u);
    switch (y) {
      case i.NUMERIC:
        return Math.floor(p / 10 * 3);
      case i.ALPHANUMERIC:
        return Math.floor(p / 11 * 2);
      case i.KANJI:
        return Math.floor(p / 13);
      case i.BYTE:
      default:
        return Math.floor(p / 8);
    }
  }, n.getBestVersionForData = function(u, _) {
    let y;
    const $ = s.from(_, s.M);
    if (Array.isArray(u)) {
      if (u.length > 1)
        return f(u, $);
      if (u.length === 0)
        return 1;
      y = u[0];
    } else
      y = u;
    return a(y.mode, y.getLength(), $);
  }, n.getEncodedBits = function(u) {
    if (!r.isValid(u) || u < 7)
      throw new Error("Invalid QR Code version");
    let _ = u << 12;
    for (; t.getBCHDigit(_) - c >= 0; )
      _ ^= o << t.getBCHDigit(_) - c;
    return u << 12 | _;
  };
})(Pe);
var Te = {};
const Dt = T, Me = 1335, mn = 21522, he = Dt.getBCHDigit(Me);
Te.getEncodedBits = function(t, e) {
  const s = t.bit << 3 | e;
  let i = s << 10;
  for (; Dt.getBCHDigit(i) - he >= 0; )
    i ^= Me << Dt.getBCHDigit(i) - he;
  return (s << 10 | i) ^ mn;
};
var Ie = {};
const yn = O;
function J(n) {
  this.mode = yn.NUMERIC, this.data = n.toString();
}
J.getBitsLength = function(t) {
  return 10 * Math.floor(t / 3) + (t % 3 ? t % 3 * 3 + 1 : 0);
};
J.prototype.getLength = function() {
  return this.data.length;
};
J.prototype.getBitsLength = function() {
  return J.getBitsLength(this.data.length);
};
J.prototype.write = function(t) {
  let e, s, i;
  for (e = 0; e + 3 <= this.data.length; e += 3)
    s = this.data.substr(e, 3), i = parseInt(s, 10), t.put(i, 10);
  const r = this.data.length - e;
  r > 0 && (s = this.data.substr(e), i = parseInt(s, 10), t.put(i, r * 3 + 1));
};
var wn = J;
const En = O, Mt = [
  "0",
  "1",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9",
  "A",
  "B",
  "C",
  "D",
  "E",
  "F",
  "G",
  "H",
  "I",
  "J",
  "K",
  "L",
  "M",
  "N",
  "O",
  "P",
  "Q",
  "R",
  "S",
  "T",
  "U",
  "V",
  "W",
  "X",
  "Y",
  "Z",
  " ",
  "$",
  "%",
  "*",
  "+",
  "-",
  ".",
  "/",
  ":"
];
function W(n) {
  this.mode = En.ALPHANUMERIC, this.data = n;
}
W.getBitsLength = function(t) {
  return 11 * Math.floor(t / 2) + 6 * (t % 2);
};
W.prototype.getLength = function() {
  return this.data.length;
};
W.prototype.getBitsLength = function() {
  return W.getBitsLength(this.data.length);
};
W.prototype.write = function(t) {
  let e;
  for (e = 0; e + 2 <= this.data.length; e += 2) {
    let s = Mt.indexOf(this.data[e]) * 45;
    s += Mt.indexOf(this.data[e + 1]), t.put(s, 11);
  }
  this.data.length % 2 && t.put(Mt.indexOf(this.data[e]), 6);
};
var An = W;
const Sn = O;
function Y(n) {
  this.mode = Sn.BYTE, typeof n == "string" ? this.data = new TextEncoder().encode(n) : this.data = new Uint8Array(n);
}
Y.getBitsLength = function(t) {
  return t * 8;
};
Y.prototype.getLength = function() {
  return this.data.length;
};
Y.prototype.getBitsLength = function() {
  return Y.getBitsLength(this.data.length);
};
Y.prototype.write = function(n) {
  for (let t = 0, e = this.data.length; t < e; t++)
    n.put(this.data[t], 8);
};
var Cn = Y;
const bn = O, vn = T;
function Q(n) {
  this.mode = bn.KANJI, this.data = n;
}
Q.getBitsLength = function(t) {
  return t * 13;
};
Q.prototype.getLength = function() {
  return this.data.length;
};
Q.prototype.getBitsLength = function() {
  return Q.getBitsLength(this.data.length);
};
Q.prototype.write = function(n) {
  let t;
  for (t = 0; t < this.data.length; t++) {
    let e = vn.toSJIS(this.data[t]);
    if (e >= 33088 && e <= 40956)
      e -= 33088;
    else if (e >= 57408 && e <= 60351)
      e -= 49472;
    else
      throw new Error(
        "Invalid SJIS character: " + this.data[t] + `
Make sure your charset is UTF-8`
      );
    e = (e >>> 8 & 255) * 192 + (e & 255), n.put(e, 13);
  }
};
var $n = Q, ke = { exports: {} };
(function(n) {
  var t = {
    single_source_shortest_paths: function(e, s, i) {
      var r = {}, o = {};
      o[s] = 0;
      var c = t.PriorityQueue.make();
      c.push(s, 0);
      for (var a, l, h, f, d, u, _, y, $; !c.empty(); ) {
        a = c.pop(), l = a.value, f = a.cost, d = e[l] || {};
        for (h in d)
          d.hasOwnProperty(h) && (u = d[h], _ = f + u, y = o[h], $ = typeof o[h] > "u", ($ || y > _) && (o[h] = _, c.push(h, _), r[h] = l));
      }
      if (typeof i < "u" && typeof o[i] > "u") {
        var m = ["Could not find a path from ", s, " to ", i, "."].join("");
        throw new Error(m);
      }
      return r;
    },
    extract_shortest_path_from_predecessor_list: function(e, s) {
      for (var i = [], r = s; r; )
        i.push(r), e[r], r = e[r];
      return i.reverse(), i;
    },
    find_path: function(e, s, i) {
      var r = t.single_source_shortest_paths(e, s, i);
      return t.extract_shortest_path_from_predecessor_list(
        r,
        i
      );
    },
    /**
     * A very naive priority queue implementation.
     */
    PriorityQueue: {
      make: function(e) {
        var s = t.PriorityQueue, i = {}, r;
        e = e || {};
        for (r in s)
          s.hasOwnProperty(r) && (i[r] = s[r]);
        return i.queue = [], i.sorter = e.sorter || s.default_sorter, i;
      },
      default_sorter: function(e, s) {
        return e.cost - s.cost;
      },
      /**
       * Add a new item to the queue and ensure the highest priority element
       * is at the front of the queue.
       */
      push: function(e, s) {
        var i = { value: e, cost: s };
        this.queue.push(i), this.queue.sort(this.sorter);
      },
      /**
       * Return the highest priority element in the queue.
       */
      pop: function() {
        return this.queue.shift();
      },
      empty: function() {
        return this.queue.length === 0;
      }
    }
  };
  n.exports = t;
})(ke);
var Pn = ke.exports;
(function(n) {
  const t = O, e = wn, s = An, i = Cn, r = $n, o = k, c = T, a = Pn;
  function l(m) {
    return unescape(encodeURIComponent(m)).length;
  }
  function h(m, w, p) {
    const g = [];
    let E;
    for (; (E = m.exec(p)) !== null; )
      g.push({
        data: E[0],
        index: E.index,
        mode: w,
        length: E[0].length
      });
    return g;
  }
  function f(m) {
    const w = h(o.NUMERIC, t.NUMERIC, m), p = h(o.ALPHANUMERIC, t.ALPHANUMERIC, m);
    let g, E;
    return c.isKanjiModeEnabled() ? (g = h(o.BYTE, t.BYTE, m), E = h(o.KANJI, t.KANJI, m)) : (g = h(o.BYTE_KANJI, t.BYTE, m), E = []), w.concat(p, g, E).sort(function(C, M) {
      return C.index - M.index;
    }).map(function(C) {
      return {
        data: C.data,
        mode: C.mode,
        length: C.length
      };
    });
  }
  function d(m, w) {
    switch (w) {
      case t.NUMERIC:
        return e.getBitsLength(m);
      case t.ALPHANUMERIC:
        return s.getBitsLength(m);
      case t.KANJI:
        return r.getBitsLength(m);
      case t.BYTE:
        return i.getBitsLength(m);
    }
  }
  function u(m) {
    return m.reduce(function(w, p) {
      const g = w.length - 1 >= 0 ? w[w.length - 1] : null;
      return g && g.mode === p.mode ? (w[w.length - 1].data += p.data, w) : (w.push(p), w);
    }, []);
  }
  function _(m) {
    const w = [];
    for (let p = 0; p < m.length; p++) {
      const g = m[p];
      switch (g.mode) {
        case t.NUMERIC:
          w.push([
            g,
            { data: g.data, mode: t.ALPHANUMERIC, length: g.length },
            { data: g.data, mode: t.BYTE, length: g.length }
          ]);
          break;
        case t.ALPHANUMERIC:
          w.push([
            g,
            { data: g.data, mode: t.BYTE, length: g.length }
          ]);
          break;
        case t.KANJI:
          w.push([
            g,
            { data: g.data, mode: t.BYTE, length: l(g.data) }
          ]);
          break;
        case t.BYTE:
          w.push([
            { data: g.data, mode: t.BYTE, length: l(g.data) }
          ]);
      }
    }
    return w;
  }
  function y(m, w) {
    const p = {}, g = { start: {} };
    let E = ["start"];
    for (let A = 0; A < m.length; A++) {
      const C = m[A], M = [];
      for (let R = 0; R < C.length; R++) {
        const I = C[R], Z = "" + A + R;
        M.push(Z), p[Z] = { node: I, lastCount: 0 }, g[Z] = {};
        for (let vt = 0; vt < E.length; vt++) {
          const B = E[vt];
          p[B] && p[B].node.mode === I.mode ? (g[B][Z] = d(p[B].lastCount + I.length, I.mode) - d(p[B].lastCount, I.mode), p[B].lastCount += I.length) : (p[B] && (p[B].lastCount = I.length), g[B][Z] = d(I.length, I.mode) + 4 + t.getCharCountIndicator(I.mode, w));
        }
      }
      E = M;
    }
    for (let A = 0; A < E.length; A++)
      g[E[A]].end = 0;
    return { map: g, table: p };
  }
  function $(m, w) {
    let p;
    const g = t.getBestModeForData(m);
    if (p = t.from(w, g), p !== t.BYTE && p.bit < g.bit)
      throw new Error('"' + m + '" cannot be encoded with mode ' + t.toString(p) + `.
 Suggested mode is: ` + t.toString(g));
    switch (p === t.KANJI && !c.isKanjiModeEnabled() && (p = t.BYTE), p) {
      case t.NUMERIC:
        return new e(m);
      case t.ALPHANUMERIC:
        return new s(m);
      case t.KANJI:
        return new r(m);
      case t.BYTE:
        return new i(m);
    }
  }
  n.fromArray = function(w) {
    return w.reduce(function(p, g) {
      return typeof g == "string" ? p.push($(g, null)) : g.data && p.push($(g.data, g.mode)), p;
    }, []);
  }, n.fromString = function(w, p) {
    const g = f(w, c.isKanjiModeEnabled()), E = _(g), A = y(E, p), C = a.find_path(A.map, "start", "end"), M = [];
    for (let R = 1; R < C.length - 1; R++)
      M.push(A.table[C[R]].node);
    return n.fromArray(u(M));
  }, n.rawSplit = function(w) {
    return n.fromArray(
      f(w, c.isKanjiModeEnabled())
    );
  };
})(Ie);
const Ct = T, It = Et, Nn = cn, Tn = ln, Mn = Se, In = Ce, Ut = be, Lt = At, kn = un, mt = Pe, Bn = Te, Rn = O, kt = Ie;
function Dn(n, t) {
  const e = n.size, s = In.getPositions(t);
  for (let i = 0; i < s.length; i++) {
    const r = s[i][0], o = s[i][1];
    for (let c = -1; c <= 7; c++)
      if (!(r + c <= -1 || e <= r + c))
        for (let a = -1; a <= 7; a++)
          o + a <= -1 || e <= o + a || (c >= 0 && c <= 6 && (a === 0 || a === 6) || a >= 0 && a <= 6 && (c === 0 || c === 6) || c >= 2 && c <= 4 && a >= 2 && a <= 4 ? n.set(r + c, o + a, !0, !0) : n.set(r + c, o + a, !1, !0));
  }
}
function Un(n) {
  const t = n.size;
  for (let e = 8; e < t - 8; e++) {
    const s = e % 2 === 0;
    n.set(e, 6, s, !0), n.set(6, e, s, !0);
  }
}
function Ln(n, t) {
  const e = Mn.getPositions(t);
  for (let s = 0; s < e.length; s++) {
    const i = e[s][0], r = e[s][1];
    for (let o = -2; o <= 2; o++)
      for (let c = -2; c <= 2; c++)
        o === -2 || o === 2 || c === -2 || c === 2 || o === 0 && c === 0 ? n.set(i + o, r + c, !0, !0) : n.set(i + o, r + c, !1, !0);
  }
}
function On(n, t) {
  const e = n.size, s = mt.getEncodedBits(t);
  let i, r, o;
  for (let c = 0; c < 18; c++)
    i = Math.floor(c / 3), r = c % 3 + e - 8 - 3, o = (s >> c & 1) === 1, n.set(i, r, o, !0), n.set(r, i, o, !0);
}
function Bt(n, t, e) {
  const s = n.size, i = Bn.getEncodedBits(t, e);
  let r, o;
  for (r = 0; r < 15; r++)
    o = (i >> r & 1) === 1, r < 6 ? n.set(r, 8, o, !0) : r < 8 ? n.set(r + 1, 8, o, !0) : n.set(s - 15 + r, 8, o, !0), r < 8 ? n.set(8, s - r - 1, o, !0) : r < 9 ? n.set(8, 15 - r - 1 + 1, o, !0) : n.set(8, 15 - r - 1, o, !0);
  n.set(s - 8, 8, 1, !0);
}
function xn(n, t) {
  const e = n.size;
  let s = -1, i = e - 1, r = 7, o = 0;
  for (let c = e - 1; c > 0; c -= 2)
    for (c === 6 && c--; ; ) {
      for (let a = 0; a < 2; a++)
        if (!n.isReserved(i, c - a)) {
          let l = !1;
          o < t.length && (l = (t[o] >>> r & 1) === 1), n.set(i, c - a, l), r--, r === -1 && (o++, r = 7);
        }
      if (i += s, i < 0 || e <= i) {
        i -= s, s = -s;
        break;
      }
    }
}
function Hn(n, t, e) {
  const s = new Nn();
  e.forEach(function(a) {
    s.put(a.mode.bit, 4), s.put(a.getLength(), Rn.getCharCountIndicator(a.mode, n)), a.write(s);
  });
  const i = Ct.getSymbolTotalCodewords(n), r = Lt.getTotalCodewordsCount(n, t), o = (i - r) * 8;
  for (s.getLengthInBits() + 4 <= o && s.put(0, 4); s.getLengthInBits() % 8 !== 0; )
    s.putBit(0);
  const c = (o - s.getLengthInBits()) / 8;
  for (let a = 0; a < c; a++)
    s.put(a % 2 ? 17 : 236, 8);
  return Fn(s, n, t);
}
function Fn(n, t, e) {
  const s = Ct.getSymbolTotalCodewords(t), i = Lt.getTotalCodewordsCount(t, e), r = s - i, o = Lt.getBlocksCount(t, e), c = s % o, a = o - c, l = Math.floor(s / o), h = Math.floor(r / o), f = h + 1, d = l - h, u = new kn(d);
  let _ = 0;
  const y = new Array(o), $ = new Array(o);
  let m = 0;
  const w = new Uint8Array(n.buffer);
  for (let C = 0; C < o; C++) {
    const M = C < a ? h : f;
    y[C] = w.slice(_, _ + M), $[C] = u.encode(y[C]), _ += M, m = Math.max(m, M);
  }
  const p = new Uint8Array(s);
  let g = 0, E, A;
  for (E = 0; E < m; E++)
    for (A = 0; A < o; A++)
      E < y[A].length && (p[g++] = y[A][E]);
  for (E = 0; E < d; E++)
    for (A = 0; A < o; A++)
      p[g++] = $[A][E];
  return p;
}
function zn(n, t, e, s) {
  let i;
  if (Array.isArray(n))
    i = kt.fromArray(n);
  else if (typeof n == "string") {
    let l = t;
    if (!l) {
      const h = kt.rawSplit(n);
      l = mt.getBestVersionForData(h, e);
    }
    i = kt.fromString(n, l || 40);
  } else
    throw new Error("Invalid data");
  const r = mt.getBestVersionForData(i, e);
  if (!r)
    throw new Error("The amount of data is too big to be stored in a QR Code");
  if (!t)
    t = r;
  else if (t < r)
    throw new Error(
      `
The chosen QR Code version cannot contain this amount of data.
Minimum version required to store current data is: ` + r + `.
`
    );
  const o = Hn(t, e, i), c = Ct.getSymbolSize(t), a = new Tn(c);
  return Dn(a, t), Un(a), Ln(a, t), Bt(a, e, 0), t >= 7 && On(a, t), xn(a, o), isNaN(s) && (s = Ut.getBestMask(
    a,
    Bt.bind(null, a, e)
  )), Ut.applyMask(s, a), Bt(a, e, s), {
    modules: a,
    version: t,
    errorCorrectionLevel: e,
    maskPattern: s,
    segments: i
  };
}
Ee.create = function(t, e) {
  if (typeof t > "u" || t === "")
    throw new Error("No input text");
  let s = It.M, i, r;
  return typeof e < "u" && (s = It.from(e.errorCorrectionLevel, It.M), i = mt.from(e.version), r = Ut.from(e.maskPattern), e.toSJISFunc && Ct.setToSJISFunction(e.toSJISFunc)), zn(t, i, s, r);
};
var Be = {}, Wt = {};
(function(n) {
  function t(e) {
    if (typeof e == "number" && (e = e.toString()), typeof e != "string")
      throw new Error("Color should be defined as hex string");
    let s = e.slice().replace("#", "").split("");
    if (s.length < 3 || s.length === 5 || s.length > 8)
      throw new Error("Invalid hex color: " + e);
    (s.length === 3 || s.length === 4) && (s = Array.prototype.concat.apply([], s.map(function(r) {
      return [r, r];
    }))), s.length === 6 && s.push("F", "F");
    const i = parseInt(s.join(""), 16);
    return {
      r: i >> 24 & 255,
      g: i >> 16 & 255,
      b: i >> 8 & 255,
      a: i & 255,
      hex: "#" + s.slice(0, 6).join("")
    };
  }
  n.getOptions = function(s) {
    s || (s = {}), s.color || (s.color = {});
    const i = typeof s.margin > "u" || s.margin === null || s.margin < 0 ? 4 : s.margin, r = s.width && s.width >= 21 ? s.width : void 0, o = s.scale || 4;
    return {
      width: r,
      scale: r ? 4 : o,
      margin: i,
      color: {
        dark: t(s.color.dark || "#000000ff"),
        light: t(s.color.light || "#ffffffff")
      },
      type: s.type,
      rendererOpts: s.rendererOpts || {}
    };
  }, n.getScale = function(s, i) {
    return i.width && i.width >= s + i.margin * 2 ? i.width / (s + i.margin * 2) : i.scale;
  }, n.getImageWidth = function(s, i) {
    const r = n.getScale(s, i);
    return Math.floor((s + i.margin * 2) * r);
  }, n.qrToImageData = function(s, i, r) {
    const o = i.modules.size, c = i.modules.data, a = n.getScale(o, r), l = Math.floor((o + r.margin * 2) * a), h = r.margin * a, f = [r.color.light, r.color.dark];
    for (let d = 0; d < l; d++)
      for (let u = 0; u < l; u++) {
        let _ = (d * l + u) * 4, y = r.color.light;
        if (d >= h && u >= h && d < l - h && u < l - h) {
          const $ = Math.floor((d - h) / a), m = Math.floor((u - h) / a);
          y = f[c[$ * o + m] ? 1 : 0];
        }
        s[_++] = y.r, s[_++] = y.g, s[_++] = y.b, s[_] = y.a;
      }
  };
})(Wt);
(function(n) {
  const t = Wt;
  function e(i, r, o) {
    i.clearRect(0, 0, r.width, r.height), r.style || (r.style = {}), r.height = o, r.width = o, r.style.height = o + "px", r.style.width = o + "px";
  }
  function s() {
    try {
      return document.createElement("canvas");
    } catch {
      throw new Error("You need to specify a canvas element");
    }
  }
  n.render = function(r, o, c) {
    let a = c, l = o;
    typeof a > "u" && (!o || !o.getContext) && (a = o, o = void 0), o || (l = s()), a = t.getOptions(a);
    const h = t.getImageWidth(r.modules.size, a), f = l.getContext("2d"), d = f.createImageData(h, h);
    return t.qrToImageData(d.data, r, a), e(f, l, h), f.putImageData(d, 0, 0), l;
  }, n.renderToDataURL = function(r, o, c) {
    let a = c;
    typeof a > "u" && (!o || !o.getContext) && (a = o, o = void 0), a || (a = {});
    const l = n.render(r, o, a), h = a.type || "image/png", f = a.rendererOpts || {};
    return l.toDataURL(h, f.quality);
  };
})(Be);
var Re = {};
const Vn = Wt;
function ue(n, t) {
  const e = n.a / 255, s = t + '="' + n.hex + '"';
  return e < 1 ? s + " " + t + '-opacity="' + e.toFixed(2).slice(1) + '"' : s;
}
function Rt(n, t, e) {
  let s = n + t;
  return typeof e < "u" && (s += " " + e), s;
}
function jn(n, t, e) {
  let s = "", i = 0, r = !1, o = 0;
  for (let c = 0; c < n.length; c++) {
    const a = Math.floor(c % t), l = Math.floor(c / t);
    !a && !r && (r = !0), n[c] ? (o++, c > 0 && a > 0 && n[c - 1] || (s += r ? Rt("M", a + e, 0.5 + l + e) : Rt("m", i, 0), i = 0, r = !1), a + 1 < t && n[c + 1] || (s += Rt("h", o), o = 0)) : i++;
  }
  return s;
}
Re.render = function(t, e, s) {
  const i = Vn.getOptions(e), r = t.modules.size, o = t.modules.data, c = r + i.margin * 2, a = i.color.light.a ? "<path " + ue(i.color.light, "fill") + ' d="M0 0h' + c + "v" + c + 'H0z"/>' : "", l = "<path " + ue(i.color.dark, "stroke") + ' d="' + jn(o, r, i.margin) + '"/>', h = 'viewBox="0 0 ' + c + " " + c + '"', d = '<svg xmlns="http://www.w3.org/2000/svg" ' + (i.width ? 'width="' + i.width + '" height="' + i.width + '" ' : "") + h + ' shape-rendering="crispEdges">' + a + l + `</svg>
`;
  return typeof s == "function" && s(null, d), d;
};
const Kn = on, Ot = Ee, De = Be, Gn = Re;
function Yt(n, t, e, s, i) {
  const r = [].slice.call(arguments, 1), o = r.length, c = typeof r[o - 1] == "function";
  if (!c && !Kn())
    throw new Error("Callback required as last argument");
  if (c) {
    if (o < 2)
      throw new Error("Too few arguments provided");
    o === 2 ? (i = e, e = t, t = s = void 0) : o === 3 && (t.getContext && typeof i > "u" ? (i = s, s = void 0) : (i = s, s = e, e = t, t = void 0));
  } else {
    if (o < 1)
      throw new Error("Too few arguments provided");
    return o === 1 ? (e = t, t = s = void 0) : o === 2 && !t.getContext && (s = e, e = t, t = void 0), new Promise(function(a, l) {
      try {
        const h = Ot.create(e, s);
        a(n(h, t, s));
      } catch (h) {
        l(h);
      }
    });
  }
  try {
    const a = Ot.create(e, s);
    i(null, n(a, t, s));
  } catch (a) {
    i(a);
  }
}
lt.create = Ot.create;
lt.toCanvas = Yt.bind(null, De.render);
lt.toDataURL = Yt.bind(null, De.renderToDataURL);
lt.toString = Yt.bind(null, function(n, t, e) {
  return Gn.render(n, e);
});
var qn = Object.defineProperty, Jn = Object.getOwnPropertyDescriptor, bt = (n, t, e, s) => {
  for (var i = s > 1 ? void 0 : s ? Jn(t, e) : t, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = (s ? o(t, e, i) : o(i)) || i);
  return s && i && qn(t, e, i), i;
};
let j = class extends z {
  constructor() {
    super(...arguments), this._qrSvg = "";
  }
  setConfig(n) {
    if (!n || !n.ssid)
      throw new Error("Please define an SSID");
    this._config = n;
  }
  static getStubConfig() {
    return {
      ssid: "Guest WiFi",
      password: "password123",
      name: "Wi-Fi Access"
    };
  }
  updated(n) {
    var t, e, s, i;
    if (n.has("hass") || n.has("_config")) {
      const r = n.has("hass") ? this._getValueFromHass((t = this._config) == null ? void 0 : t.ssid, n.get("hass")) : null, o = this._getValue((e = this._config) == null ? void 0 : e.ssid), c = n.has("hass") ? this._getValueFromHass((s = this._config) == null ? void 0 : s.password, n.get("hass")) : null, a = this._getValue((i = this._config) == null ? void 0 : i.password);
      (n.has("_config") || r !== o || c !== a) && this._generateQR();
    }
  }
  _getValueFromHass(n, t) {
    return !n || !t ? n || "" : t.states[n] ? t.states[n].state : n;
  }
  _getValue(n) {
    return !n || !this.hass ? n || "" : this.hass.states[n] ? this.hass.states[n].state : n;
  }
  _generateWifiString(n, t) {
    const e = n.replace(/([\\;,":])/g, "\\$1"), s = t ? t.replace(/([\\;,":])/g, "\\$1") : "";
    return s ? `WIFI:T:WPA;S:${e};P:${s};;` : `WIFI:T:nopass;S:${e};P:;;`;
  }
  async _generateQR() {
    if (!this._config) return;
    const n = this._getValue(this._config.ssid), t = this._getValue(this._config.password);
    if (!n) {
      this._qrSvg = "";
      return;
    }
    const e = this._generateWifiString(n, t);
    try {
      this._qrSvg = await lt.toString(e, {
        type: "svg",
        margin: 2,
        color: {
          dark: "#000000",
          light: "#ffffff"
        }
      });
    } catch (s) {
      console.error("Failed to generate QR code", s), this._qrSvg = "";
    }
  }
  render() {
    if (!this._config || !this.hass)
      return N``;
    const n = this._getValue(this._config.ssid), t = this._getValue(this._config.password);
    return N`
      <ha-card .header="${this._config.name || "Wi-Fi Access"}">
        <div class="card-content">
          <div class="ssid-display">${n}</div>
          <div class="qr-container" .innerHTML="${this._qrSvg}"></div>
          ${t ? N`<div class="password-display">Password: <code>${t}</code></div>` : ""}
        </div>
      </ha-card>
    `;
  }
};
j.styles = zt`
    :host {
      display: block;
    }
    .card-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 16px;
      gap: 16px;
    }
    .ssid-display {
      font-size: 1.5em;
      font-weight: bold;
      color: var(--primary-text-color);
      text-align: center;
    }
    .qr-container {
      width: 200px;
      height: 200px;
      background: white;
      padding: 8px;
      border-radius: 8px;
    }
    .qr-container svg {
      width: 100%;
      height: 100%;
    }
    .password-display {
      color: var(--secondary-text-color);
      text-align: center;
    }
    code {
      background: var(--secondary-background-color);
      padding: 2px 4px;
      border-radius: 4px;
      font-family: monospace;
    }
  `;
bt([
  wt({ attribute: !1 })
], j.prototype, "hass", 2);
bt([
  v()
], j.prototype, "_config", 2);
bt([
  v()
], j.prototype, "_qrSvg", 2);
j = bt([
  we("meraki-wifi-qr-card")
], j);
customElements.get("meraki-wifi-qr-card") || customElements.define("meraki-wifi-qr-card", j);
window.customCards = window.customCards || [];
window.customCards.push({
  type: "meraki-wifi-qr-card",
  name: "Meraki Wi-Fi QR Card",
  description: "Display a scannable Wi-Fi QR code for guests.",
  preview: !0
});
var xt = /* @__PURE__ */ ((n) => (n.GET_CONFIG = "meraki_ha/get_config", n.SUBSCRIBE_MERAKI_DATA = "meraki_ha/subscribe_meraki_data", n.GET_CAMERA_STREAM_URL = "meraki_ha/get_camera_stream_url", n.GET_CAMERA_SNAPSHOT = "meraki_ha/get_camera_snapshot", n.GET_VERSION = "meraki_ha/get_version", n.GET_NETWORK_EVENTS = "meraki_ha/get_network_events", n.UPDATE_ENABLED_NETWORKS = "meraki_ha/update_enabled_networks", n.CREATE_GUEST_KEY = "meraki_ha/ipsk/create", n.GET_GUEST_KEYS = "meraki_ha/ipsk/get", n.REVOKE_GUEST_KEY = "meraki_ha/ipsk/revoke", n.TIMED_ACCESS_GET_POLICIES = "meraki_ha/timed_access/get_policies", n))(xt || {});
const de = async (n, t) => {
  if (!n)
    throw new Error("Home Assistant object is not available.");
  try {
    if (typeof n.callWS == "function")
      return await n.callWS(t);
    if (n.connection && typeof n.connection.sendMessagePromise == "function")
      return await n.connection.sendMessagePromise(t);
    throw new Error("Home Assistant WebSocket communication methods not found.");
  } catch (e) {
    throw console.error(`Meraki HA: WebSocket error [${t.type}]:`, e), e;
  }
};
var Wn = Object.defineProperty, P = (n, t, e, s) => {
  for (var i = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = o(t, e, i) || i);
  return i && Wn(t, e, i), i;
};
const Qt = class Qt extends z {
  constructor() {
    super(...arguments), this._selectedNetwork = "", this._selectedSSID = "", this._selectedPolicy = "", this._selectedDuration = "60", this._customName = "", this._customPassphrase = "", this._creating = !1, this._error = null, this._success = null, this._networks = [], this._ssids = [], this._policies = [], this._loading = !0, this._initDone = !1;
  }
  setConfig(t) {
    if (!t)
      throw new Error("Invalid configuration");
    this._config = t;
  }
  static getStubConfig() {
    return {
      name: "Meraki Guest Access"
    };
  }
  firstUpdated(t) {
    super.firstUpdated(t), this._fetchInitialData();
  }
  updated(t) {
    var e;
    super.updated(t), t.has("hass") && this.hass && (!this._initDone && this.hass && this._fetchInitialData(), (e = this.hass.user) != null && e.name && !this._customName && (this._customName = this.hass.user.name));
  }
  async _fetchInitialData() {
    var t;
    if (this._initDone = !0, !!this.hass) {
      this._loading = !0;
      try {
        const e = await this.hass.callWS({
          type: "config_entries/get",
          domain: "meraki_ha"
        }), s = ((t = this._config) == null ? void 0 : t.config_entry_id) || (e.length > 0 ? e[0].entry_id : null);
        if (!s) {
          this._error = "Meraki integration not found. Please configure it first.", this._loading = !1;
          return;
        }
        const i = await de(this.hass, {
          type: xt.GET_CONFIG,
          config_entry_id: s
        });
        this._networks = (Array.isArray(i.networks) ? i.networks : []).filter((r) => {
          var o;
          return (o = r.productTypes) == null ? void 0 : o.includes("wireless");
        }), this._ssids = Array.isArray(i.ssids) ? i.ssids : [], this._networks.length > 0 && !this._selectedNetwork && (this._selectedNetwork = this._networks[0].id, this._fetchPolicies(this._selectedNetwork, s));
      } catch (e) {
        this._error = `Failed to fetch Meraki data: ${e.message || e}`;
      } finally {
        this._loading = !1;
      }
    }
  }
  async _fetchSSIDs() {
  }
  async _fetchPolicies(t, e) {
    var s;
    if (this.hass)
      try {
        let i = e || ((s = this._config) == null ? void 0 : s.config_entry_id);
        if (!i) {
          const o = await this.hass.callWS({
            type: "config_entries/get",
            domain: "meraki_ha"
          });
          i = o.length > 0 ? o[0].entry_id : void 0;
        }
        if (!i) return;
        const r = await de(this.hass, {
          type: xt.TIMED_ACCESS_GET_POLICIES,
          config_entry_id: i,
          network_id: t
        });
        this._policies = Array.isArray(r) ? r : (r == null ? void 0 : r.policies) || [];
      } catch (i) {
        console.error("Failed to fetch policies:", i), this._policies = [];
      }
  }
  render() {
    var e, s;
    if (this._loading && !this._networks.length)
      return N`
        <ha-card .header="${((e = this._config) == null ? void 0 : e.name) || "Meraki Guest Access"}">
          <div class="card-content flex justify-center p-8">
            <ha-circular-progress active></ha-circular-progress>
          </div>
        </ha-card>
      `;
    const t = (this._ssids || []).filter((i) => i.networkId === this._selectedNetwork);
    return N`
      <ha-card .header="${((s = this._config) == null ? void 0 : s.name) || "Meraki Guest Access"}">
        <div class="card-content">
          ${this._error ? N`
                <ha-alert alert-type="error" dismissable @alert-dismissed-clicked="${() => this._error = null}">
                  ${this._error}
                </ha-alert>
              ` : ""}
          ${this._success ? N`
                <ha-alert alert-type="success" dismissable @alert-dismissed-clicked="${() => this._success = null}">
                  ${this._success}
                </ha-alert>
              ` : ""}

          <div class="form-container">
            <ha-select
              label="Network"
              value="${this._selectedNetwork}"
              @closed="${this._handleNetworkChange}"
              fixedMenuPosition
              naturalMenuWidth
            >
              ${(this._networks || []).map(
      (i) => N`<mwc-list-item value="${String(i.id)}">${i.name}</mwc-list-item>`
    )}
            </ha-select>

            <ha-select
              label="SSID"
              value="${this._selectedSSID}"
              .disabled="${!this._selectedNetwork}"
              @closed="${this._handleSSIDChange}"
              fixedMenuPosition
              naturalMenuWidth
            >
              ${(t || []).map(
      (i) => N`<mwc-list-item value="${String(i.number)}">${i.name} (SSID ${i.number})</mwc-list-item>`
    )}
            </ha-select>

            <ha-select
              label="Group Policy"
              value="${this._selectedPolicy}"
              .disabled="${!this._selectedNetwork}"
              @closed="${this._handlePolicyChange}"
              fixedMenuPosition
              naturalMenuWidth
            >
              <mwc-list-item value="">None (Default)</mwc-list-item>
              ${(this._policies || []).map(
      (i) => N`<mwc-list-item value="${String(i.groupPolicyId)}">${i.name}</mwc-list-item>`
    )}
            </ha-select>

            <ha-select
              label="Duration"
              value="${this._selectedDuration}"
              @closed="${this._handleDurationChange}"
              fixedMenuPosition
              naturalMenuWidth
            >
              <mwc-list-item value="${"30"}">30 Minutes</mwc-list-item>
              <mwc-list-item value="${"60"}">1 Hour</mwc-list-item>
              <mwc-list-item value="${"240"}">4 Hours</mwc-list-item>
              <mwc-list-item value="${"1440"}">24 Hours</mwc-list-item>
              <mwc-list-item value="${"10080"}">7 Days</mwc-list-item>
            </ha-select>

            <ha-textfield
              label="Name (Optional)"
              placeholder="e.g. Guest-John"
              .value="${this._customName}"
              @input="${(i) => this._customName = i.target.value}"
            ></ha-textfield>

            <ha-textfield
              label="Passphrase (Optional)"
              placeholder="Leave empty to auto-generate"
              .value="${this._customPassphrase}"
              @input="${(i) => this._customPassphrase = i.target.value}"
            ></ha-textfield>

            <ha-button
              raised
              .disabled="${this._creating || !this._selectedNetwork || !this._selectedSSID}"
              @click="${this._handleCreate}"
            >
              ${this._creating ? "Creating..." : "Generate access key"}
            </ha-button>
          </div>
        </div>
      </ha-card>
    `;
  }
  _handleNetworkChange(t) {
    const e = t.target.value;
    e !== this._selectedNetwork && (this._selectedNetwork = e, this._selectedSSID = "", this._selectedPolicy = "", this._fetchSSIDs(), this._fetchPolicies(e));
  }
  _handleSSIDChange(t) {
    this._selectedSSID = t.target.value;
  }
  _handlePolicyChange(t) {
    this._selectedPolicy = t.target.value;
  }
  _handleDurationChange(t) {
    this._selectedDuration = t.target.value;
  }
  async _handleCreate() {
    if (!(!this._selectedNetwork || !this._selectedSSID)) {
      this._creating = !0, this._error = null, this._success = null;
      try {
        await this.hass.callService("meraki_ha", "create_guest_key", {
          network_id: this._selectedNetwork,
          ssid_number: parseInt(this._selectedSSID, 10),
          duration_minutes: parseInt(this._selectedDuration, 10),
          name: this._customName || void 0,
          passphrase: this._customPassphrase || void 0,
          group_policy_id: this._selectedPolicy || void 0
        }), this._success = "Guest access key created successfully!", this._customName = "", this._customPassphrase = "";
      } catch (t) {
        this._error = `Failed to create guest key: ${t.message || t}`;
      } finally {
        this._creating = !1;
      }
    }
  }
};
Qt.styles = zt`
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
let S = Qt;
P([
  wt({ attribute: !1 })
], S.prototype, "hass");
P([
  v()
], S.prototype, "_config");
P([
  v()
], S.prototype, "_selectedNetwork");
P([
  v()
], S.prototype, "_selectedSSID");
P([
  v()
], S.prototype, "_selectedPolicy");
P([
  v()
], S.prototype, "_selectedDuration");
P([
  v()
], S.prototype, "_customName");
P([
  v()
], S.prototype, "_customPassphrase");
P([
  v()
], S.prototype, "_creating");
P([
  v()
], S.prototype, "_error");
P([
  v()
], S.prototype, "_success");
P([
  v()
], S.prototype, "_networks");
P([
  v()
], S.prototype, "_ssids");
P([
  v()
], S.prototype, "_policies");
P([
  v()
], S.prototype, "_loading");
P([
  v()
], S.prototype, "_initDone");
customElements.get("meraki-guest-access-card") || customElements.define("meraki-guest-access-card", S);
window.customCards = window.customCards || [];
window.customCards.push({
  type: "meraki-guest-access-card",
  name: "Meraki Guest Access",
  description: "Create and manage Meraki IPSK guest access keys.",
  preview: !0
});
export {
  S as MerakiGuestAccessCard
};
