/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const xt = globalThis, te = xt.ShadowRoot && (xt.ShadyCSS === void 0 || xt.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, ee = Symbol(), ve = /* @__PURE__ */ new WeakMap();
let Le = class {
  constructor(t, e, i) {
    if (this._$cssResult$ = !0, i !== ee) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = t, this.t = e;
  }
  get styleSheet() {
    let t = this.o;
    const e = this.t;
    if (te && t === void 0) {
      const i = e !== void 0 && e.length === 1;
      i && (t = ve.get(e)), t === void 0 && ((this.o = t = new CSSStyleSheet()).replaceSync(this.cssText), i && ve.set(e, t));
    }
    return t;
  }
  toString() {
    return this.cssText;
  }
};
const ns = (n) => new Le(typeof n == "string" ? n : n + "", void 0, ee), D = (n, ...t) => {
  const e = n.length === 1 ? n[0] : t.reduce((i, s, r) => i + ((o) => {
    if (o._$cssResult$ === !0) return o.cssText;
    if (typeof o == "number") return o;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + o + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(s) + n[r + 1], n[0]);
  return new Le(e, n, ee);
}, rs = (n, t) => {
  if (te) n.adoptedStyleSheets = t.map((e) => e instanceof CSSStyleSheet ? e : e.styleSheet);
  else for (const e of t) {
    const i = document.createElement("style"), s = xt.litNonce;
    s !== void 0 && i.setAttribute("nonce", s), i.textContent = e.cssText, n.appendChild(i);
  }
}, be = te ? (n) => n : (n) => n instanceof CSSStyleSheet ? ((t) => {
  let e = "";
  for (const i of t.cssRules) e += i.cssText;
  return ns(e);
})(n) : n;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: os, defineProperty: as, getOwnPropertyDescriptor: cs, getOwnPropertyNames: ls, getOwnPropertySymbols: ds, getPrototypeOf: hs } = Object, G = globalThis, Ee = G.trustedTypes, us = Ee ? Ee.emptyScript : "", zt = G.reactiveElementPolyfillSupport, ut = (n, t) => n, Mt = { toAttribute(n, t) {
  switch (t) {
    case Boolean:
      n = n ? us : null;
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
} }, se = (n, t) => !os(n, t), Ce = { attribute: !0, type: String, converter: Mt, reflect: !1, useDefault: !1, hasChanged: se };
Symbol.metadata ?? (Symbol.metadata = Symbol("metadata")), G.litPropertyMetadata ?? (G.litPropertyMetadata = /* @__PURE__ */ new WeakMap());
let et = class extends HTMLElement {
  static addInitializer(t) {
    this._$Ei(), (this.l ?? (this.l = [])).push(t);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(t, e = Ce) {
    if (e.state && (e.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(t) && ((e = Object.create(e)).wrapped = !0), this.elementProperties.set(t, e), !e.noAccessor) {
      const i = Symbol(), s = this.getPropertyDescriptor(t, i, e);
      s !== void 0 && as(this.prototype, t, s);
    }
  }
  static getPropertyDescriptor(t, e, i) {
    const { get: s, set: r } = cs(this.prototype, t) ?? { get() {
      return this[e];
    }, set(o) {
      this[e] = o;
    } };
    return { get: s, set(o) {
      const a = s == null ? void 0 : s.call(this);
      r == null || r.call(this, o), this.requestUpdate(t, a, i);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(t) {
    return this.elementProperties.get(t) ?? Ce;
  }
  static _$Ei() {
    if (this.hasOwnProperty(ut("elementProperties"))) return;
    const t = hs(this);
    t.finalize(), t.l !== void 0 && (this.l = [...t.l]), this.elementProperties = new Map(t.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(ut("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(ut("properties"))) {
      const e = this.properties, i = [...ls(e), ...ds(e)];
      for (const s of i) this.createProperty(s, e[s]);
    }
    const t = this[Symbol.metadata];
    if (t !== null) {
      const e = litPropertyMetadata.get(t);
      if (e !== void 0) for (const [i, s] of e) this.elementProperties.set(i, s);
    }
    this._$Eh = /* @__PURE__ */ new Map();
    for (const [e, i] of this.elementProperties) {
      const s = this._$Eu(e, i);
      s !== void 0 && this._$Eh.set(s, e);
    }
    this.elementStyles = this.finalizeStyles(this.styles);
  }
  static finalizeStyles(t) {
    const e = [];
    if (Array.isArray(t)) {
      const i = new Set(t.flat(1 / 0).reverse());
      for (const s of i) e.unshift(be(s));
    } else t !== void 0 && e.push(be(t));
    return e;
  }
  static _$Eu(t, e) {
    const i = e.attribute;
    return i === !1 ? void 0 : typeof i == "string" ? i : typeof t == "string" ? t.toLowerCase() : void 0;
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
    for (const i of e.keys()) this.hasOwnProperty(i) && (t.set(i, this[i]), delete this[i]);
    t.size > 0 && (this._$Ep = t);
  }
  createRenderRoot() {
    const t = this.shadowRoot ?? this.attachShadow(this.constructor.shadowRootOptions);
    return rs(t, this.constructor.elementStyles), t;
  }
  connectedCallback() {
    var t;
    this.renderRoot ?? (this.renderRoot = this.createRenderRoot()), this.enableUpdating(!0), (t = this._$EO) == null || t.forEach((e) => {
      var i;
      return (i = e.hostConnected) == null ? void 0 : i.call(e);
    });
  }
  enableUpdating(t) {
  }
  disconnectedCallback() {
    var t;
    (t = this._$EO) == null || t.forEach((e) => {
      var i;
      return (i = e.hostDisconnected) == null ? void 0 : i.call(e);
    });
  }
  attributeChangedCallback(t, e, i) {
    this._$AK(t, i);
  }
  _$ET(t, e) {
    var r;
    const i = this.constructor.elementProperties.get(t), s = this.constructor._$Eu(t, i);
    if (s !== void 0 && i.reflect === !0) {
      const o = (((r = i.converter) == null ? void 0 : r.toAttribute) !== void 0 ? i.converter : Mt).toAttribute(e, i.type);
      this._$Em = t, o == null ? this.removeAttribute(s) : this.setAttribute(s, o), this._$Em = null;
    }
  }
  _$AK(t, e) {
    var r, o;
    const i = this.constructor, s = i._$Eh.get(t);
    if (s !== void 0 && this._$Em !== s) {
      const a = i.getPropertyOptions(s), c = typeof a.converter == "function" ? { fromAttribute: a.converter } : ((r = a.converter) == null ? void 0 : r.fromAttribute) !== void 0 ? a.converter : Mt;
      this._$Em = s;
      const l = c.fromAttribute(e, a.type);
      this[s] = l ?? ((o = this._$Ej) == null ? void 0 : o.get(s)) ?? l, this._$Em = null;
    }
  }
  requestUpdate(t, e, i, s = !1, r) {
    var o;
    if (t !== void 0) {
      const a = this.constructor;
      if (s === !1 && (r = this[t]), i ?? (i = a.getPropertyOptions(t)), !((i.hasChanged ?? se)(r, e) || i.useDefault && i.reflect && r === ((o = this._$Ej) == null ? void 0 : o.get(t)) && !this.hasAttribute(a._$Eu(t, i)))) return;
      this.C(t, e, i);
    }
    this.isUpdatePending === !1 && (this._$ES = this._$EP());
  }
  C(t, e, { useDefault: i, reflect: s, wrapped: r }, o) {
    i && !(this._$Ej ?? (this._$Ej = /* @__PURE__ */ new Map())).has(t) && (this._$Ej.set(t, o ?? e ?? this[t]), r !== !0 || o !== void 0) || (this._$AL.has(t) || (this.hasUpdated || i || (e = void 0), this._$AL.set(t, e)), s === !0 && this._$Em !== t && (this._$Eq ?? (this._$Eq = /* @__PURE__ */ new Set())).add(t));
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
    var i;
    if (!this.isUpdatePending) return;
    if (!this.hasUpdated) {
      if (this.renderRoot ?? (this.renderRoot = this.createRenderRoot()), this._$Ep) {
        for (const [r, o] of this._$Ep) this[r] = o;
        this._$Ep = void 0;
      }
      const s = this.constructor.elementProperties;
      if (s.size > 0) for (const [r, o] of s) {
        const { wrapped: a } = o, c = this[r];
        a !== !0 || this._$AL.has(r) || c === void 0 || this.C(r, void 0, o, c);
      }
    }
    let t = !1;
    const e = this._$AL;
    try {
      t = this.shouldUpdate(e), t ? (this.willUpdate(e), (i = this._$EO) == null || i.forEach((s) => {
        var r;
        return (r = s.hostUpdate) == null ? void 0 : r.call(s);
      }), this.update(e)) : this._$EM();
    } catch (s) {
      throw t = !1, this._$EM(), s;
    }
    t && this._$AE(e);
  }
  willUpdate(t) {
  }
  _$AE(t) {
    var e;
    (e = this._$EO) == null || e.forEach((i) => {
      var s;
      return (s = i.hostUpdated) == null ? void 0 : s.call(i);
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
et.elementStyles = [], et.shadowRootOptions = { mode: "open" }, et[ut("elementProperties")] = /* @__PURE__ */ new Map(), et[ut("finalized")] = /* @__PURE__ */ new Map(), zt == null || zt({ ReactiveElement: et }), (G.reactiveElementVersions ?? (G.reactiveElementVersions = [])).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const ft = globalThis, $e = (n) => n, Tt = ft.trustedTypes, Ae = Tt ? Tt.createPolicy("lit-html", { createHTML: (n) => n }) : void 0, Be = "$lit$", j = `lit$${Math.random().toFixed(9).slice(2)}$`, Re = "?" + j, fs = `<${Re}>`, Z = document, pt = () => Z.createComment(""), mt = (n) => n === null || typeof n != "object" && typeof n != "function", ie = Array.isArray, gs = (n) => ie(n) || typeof (n == null ? void 0 : n[Symbol.iterator]) == "function", Ft = `[ 	
\f\r]`, ht = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, ke = /-->/g, Se = />/g, J = RegExp(`>|${Ft}(?:([^\\s"'>=/]+)(${Ft}*=${Ft}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`, "g"), Pe = /'/g, Ne = /"/g, Ue = /^(?:script|style|textarea|title)$/i, ps = (n) => (t, ...e) => ({ _$litType$: n, strings: t, values: e }), b = ps(1), st = Symbol.for("lit-noChange"), A = Symbol.for("lit-nothing"), xe = /* @__PURE__ */ new WeakMap(), Y = Z.createTreeWalker(Z, 129);
function Oe(n, t) {
  if (!ie(n) || !n.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return Ae !== void 0 ? Ae.createHTML(t) : t;
}
const ms = (n, t) => {
  const e = n.length - 1, i = [];
  let s, r = t === 2 ? "<svg>" : t === 3 ? "<math>" : "", o = ht;
  for (let a = 0; a < e; a++) {
    const c = n[a];
    let l, d, h = -1, u = 0;
    for (; u < c.length && (o.lastIndex = u, d = o.exec(c), d !== null); ) u = o.lastIndex, o === ht ? d[1] === "!--" ? o = ke : d[1] !== void 0 ? o = Se : d[2] !== void 0 ? (Ue.test(d[2]) && (s = RegExp("</" + d[2], "g")), o = J) : d[3] !== void 0 && (o = J) : o === J ? d[0] === ">" ? (o = s ?? ht, h = -1) : d[1] === void 0 ? h = -2 : (h = o.lastIndex - d[2].length, l = d[1], o = d[3] === void 0 ? J : d[3] === '"' ? Ne : Pe) : o === Ne || o === Pe ? o = J : o === ke || o === Se ? o = ht : (o = J, s = void 0);
    const f = o === J && n[a + 1].startsWith("/>") ? " " : "";
    r += o === ht ? c + fs : h >= 0 ? (i.push(l), c.slice(0, h) + Be + c.slice(h) + j + f) : c + j + (h === -2 ? a : f);
  }
  return [Oe(n, r + (n[e] || "<?>") + (t === 2 ? "</svg>" : t === 3 ? "</math>" : "")), i];
};
class _t {
  constructor({ strings: t, _$litType$: e }, i) {
    let s;
    this.parts = [];
    let r = 0, o = 0;
    const a = t.length - 1, c = this.parts, [l, d] = ms(t, e);
    if (this.el = _t.createElement(l, i), Y.currentNode = this.el.content, e === 2 || e === 3) {
      const h = this.el.content.firstChild;
      h.replaceWith(...h.childNodes);
    }
    for (; (s = Y.nextNode()) !== null && c.length < a; ) {
      if (s.nodeType === 1) {
        if (s.hasAttributes()) for (const h of s.getAttributeNames()) if (h.endsWith(Be)) {
          const u = d[o++], f = s.getAttribute(h).split(j), g = /([.?@])?(.*)/.exec(u);
          c.push({ type: 1, index: r, name: g[2], strings: f, ctor: g[1] === "." ? ys : g[1] === "?" ? ws : g[1] === "@" ? vs : Lt }), s.removeAttribute(h);
        } else h.startsWith(j) && (c.push({ type: 6, index: r }), s.removeAttribute(h));
        if (Ue.test(s.tagName)) {
          const h = s.textContent.split(j), u = h.length - 1;
          if (u > 0) {
            s.textContent = Tt ? Tt.emptyScript : "";
            for (let f = 0; f < u; f++) s.append(h[f], pt()), Y.nextNode(), c.push({ type: 2, index: ++r });
            s.append(h[u], pt());
          }
        }
      } else if (s.nodeType === 8) if (s.data === Re) c.push({ type: 2, index: r });
      else {
        let h = -1;
        for (; (h = s.data.indexOf(j, h + 1)) !== -1; ) c.push({ type: 7, index: r }), h += j.length - 1;
      }
      r++;
    }
  }
  static createElement(t, e) {
    const i = Z.createElement("template");
    return i.innerHTML = t, i;
  }
}
function it(n, t, e = n, i) {
  var o, a;
  if (t === st) return t;
  let s = i !== void 0 ? (o = e._$Co) == null ? void 0 : o[i] : e._$Cl;
  const r = mt(t) ? void 0 : t._$litDirective$;
  return (s == null ? void 0 : s.constructor) !== r && ((a = s == null ? void 0 : s._$AO) == null || a.call(s, !1), r === void 0 ? s = void 0 : (s = new r(n), s._$AT(n, e, i)), i !== void 0 ? (e._$Co ?? (e._$Co = []))[i] = s : e._$Cl = s), s !== void 0 && (t = it(n, s._$AS(n, t.values), s, i)), t;
}
class _s {
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
    const { el: { content: e }, parts: i } = this._$AD, s = ((t == null ? void 0 : t.creationScope) ?? Z).importNode(e, !0);
    Y.currentNode = s;
    let r = Y.nextNode(), o = 0, a = 0, c = i[0];
    for (; c !== void 0; ) {
      if (o === c.index) {
        let l;
        c.type === 2 ? l = new Ct(r, r.nextSibling, this, t) : c.type === 1 ? l = new c.ctor(r, c.name, c.strings, this, t) : c.type === 6 && (l = new bs(r, this, t)), this._$AV.push(l), c = i[++a];
      }
      o !== (c == null ? void 0 : c.index) && (r = Y.nextNode(), o++);
    }
    return Y.currentNode = Z, s;
  }
  p(t) {
    let e = 0;
    for (const i of this._$AV) i !== void 0 && (i.strings !== void 0 ? (i._$AI(t, i, e), e += i.strings.length - 2) : i._$AI(t[e])), e++;
  }
}
class Ct {
  get _$AU() {
    var t;
    return ((t = this._$AM) == null ? void 0 : t._$AU) ?? this._$Cv;
  }
  constructor(t, e, i, s) {
    this.type = 2, this._$AH = A, this._$AN = void 0, this._$AA = t, this._$AB = e, this._$AM = i, this.options = s, this._$Cv = (s == null ? void 0 : s.isConnected) ?? !0;
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
    t = it(this, t, e), mt(t) ? t === A || t == null || t === "" ? (this._$AH !== A && this._$AR(), this._$AH = A) : t !== this._$AH && t !== st && this._(t) : t._$litType$ !== void 0 ? this.$(t) : t.nodeType !== void 0 ? this.T(t) : gs(t) ? this.k(t) : this._(t);
  }
  O(t) {
    return this._$AA.parentNode.insertBefore(t, this._$AB);
  }
  T(t) {
    this._$AH !== t && (this._$AR(), this._$AH = this.O(t));
  }
  _(t) {
    this._$AH !== A && mt(this._$AH) ? this._$AA.nextSibling.data = t : this.T(Z.createTextNode(t)), this._$AH = t;
  }
  $(t) {
    var r;
    const { values: e, _$litType$: i } = t, s = typeof i == "number" ? this._$AC(t) : (i.el === void 0 && (i.el = _t.createElement(Oe(i.h, i.h[0]), this.options)), i);
    if (((r = this._$AH) == null ? void 0 : r._$AD) === s) this._$AH.p(e);
    else {
      const o = new _s(s, this), a = o.u(this.options);
      o.p(e), this.T(a), this._$AH = o;
    }
  }
  _$AC(t) {
    let e = xe.get(t.strings);
    return e === void 0 && xe.set(t.strings, e = new _t(t)), e;
  }
  k(t) {
    ie(this._$AH) || (this._$AH = [], this._$AR());
    const e = this._$AH;
    let i, s = 0;
    for (const r of t) s === e.length ? e.push(i = new Ct(this.O(pt()), this.O(pt()), this, this.options)) : i = e[s], i._$AI(r), s++;
    s < e.length && (this._$AR(i && i._$AB.nextSibling, s), e.length = s);
  }
  _$AR(t = this._$AA.nextSibling, e) {
    var i;
    for ((i = this._$AP) == null ? void 0 : i.call(this, !1, !0, e); t !== this._$AB; ) {
      const s = $e(t).nextSibling;
      $e(t).remove(), t = s;
    }
  }
  setConnected(t) {
    var e;
    this._$AM === void 0 && (this._$Cv = t, (e = this._$AP) == null || e.call(this, t));
  }
}
class Lt {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(t, e, i, s, r) {
    this.type = 1, this._$AH = A, this._$AN = void 0, this.element = t, this.name = e, this._$AM = s, this.options = r, i.length > 2 || i[0] !== "" || i[1] !== "" ? (this._$AH = Array(i.length - 1).fill(new String()), this.strings = i) : this._$AH = A;
  }
  _$AI(t, e = this, i, s) {
    const r = this.strings;
    let o = !1;
    if (r === void 0) t = it(this, t, e, 0), o = !mt(t) || t !== this._$AH && t !== st, o && (this._$AH = t);
    else {
      const a = t;
      let c, l;
      for (t = r[0], c = 0; c < r.length - 1; c++) l = it(this, a[i + c], e, c), l === st && (l = this._$AH[c]), o || (o = !mt(l) || l !== this._$AH[c]), l === A ? t = A : t !== A && (t += (l ?? "") + r[c + 1]), this._$AH[c] = l;
    }
    o && !s && this.j(t);
  }
  j(t) {
    t === A ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, t ?? "");
  }
}
class ys extends Lt {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(t) {
    this.element[this.name] = t === A ? void 0 : t;
  }
}
class ws extends Lt {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(t) {
    this.element.toggleAttribute(this.name, !!t && t !== A);
  }
}
class vs extends Lt {
  constructor(t, e, i, s, r) {
    super(t, e, i, s, r), this.type = 5;
  }
  _$AI(t, e = this) {
    if ((t = it(this, t, e, 0) ?? A) === st) return;
    const i = this._$AH, s = t === A && i !== A || t.capture !== i.capture || t.once !== i.once || t.passive !== i.passive, r = t !== A && (i === A || s);
    s && this.element.removeEventListener(this.name, this, i), r && this.element.addEventListener(this.name, this, t), this._$AH = t;
  }
  handleEvent(t) {
    var e;
    typeof this._$AH == "function" ? this._$AH.call(((e = this.options) == null ? void 0 : e.host) ?? this.element, t) : this._$AH.handleEvent(t);
  }
}
class bs {
  constructor(t, e, i) {
    this.element = t, this.type = 6, this._$AN = void 0, this._$AM = e, this.options = i;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t) {
    it(this, t);
  }
}
const Vt = ft.litHtmlPolyfillSupport;
Vt == null || Vt(_t, Ct), (ft.litHtmlVersions ?? (ft.litHtmlVersions = [])).push("3.3.2");
const Es = (n, t, e) => {
  const i = (e == null ? void 0 : e.renderBefore) ?? t;
  let s = i._$litPart$;
  if (s === void 0) {
    const r = (e == null ? void 0 : e.renderBefore) ?? null;
    i._$litPart$ = s = new Ct(t.insertBefore(pt(), r), r, void 0, e ?? {});
  }
  return s._$AI(n), s;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Q = globalThis;
class P extends et {
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
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Do = Es(e, this.renderRoot, this.renderOptions);
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
    return st;
  }
}
var De;
P._$litElement$ = !0, P.finalized = !0, (De = Q.litElementHydrateSupport) == null || De.call(Q, { LitElement: P });
const jt = Q.litElementPolyfillSupport;
jt == null || jt({ LitElement: P });
(Q.litElementVersions ?? (Q.litElementVersions = [])).push("4.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Cs = { attribute: !0, type: String, converter: Mt, reflect: !1, hasChanged: se }, $s = (n = Cs, t, e) => {
  const { kind: i, metadata: s } = e;
  let r = globalThis.litPropertyMetadata.get(s);
  if (r === void 0 && globalThis.litPropertyMetadata.set(s, r = /* @__PURE__ */ new Map()), i === "setter" && ((n = Object.create(n)).wrapped = !0), r.set(e.name, n), i === "accessor") {
    const { name: o } = e;
    return { set(a) {
      const c = t.get.call(this);
      t.set.call(this, a), this.requestUpdate(o, c, n, !0, a);
    }, init(a) {
      return a !== void 0 && this.C(o, void 0, n, a), a;
    } };
  }
  if (i === "setter") {
    const { name: o } = e;
    return function(a) {
      const c = this[o];
      t.call(this, a), this.requestUpdate(o, c, n, !0, a);
    };
  }
  throw Error("Unsupported decorator location: " + i);
};
function L(n) {
  return (t, e) => typeof e == "object" ? $s(n, t, e) : ((i, s, r) => {
    const o = s.hasOwnProperty(r);
    return s.constructor.createProperty(r, i), o ? Object.getOwnPropertyDescriptor(s, r) : void 0;
  })(n, t, e);
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function y(n) {
  return L({ ...n, state: !0, attribute: !1 });
}
const ne = (n, t, e) => b`
  <ha-card class="status-card warning">
    <div class="card-content flex-col align-center p-8">
      <ha-icon icon="mdi:alert-circle" style="--mdc-icon-size: 48px; margin-bottom: 16px;"></ha-icon>
      <h1 class="status-title">${n}</h1>
      <div class="status-message mt-4">${t}</div>
    </div>
    ${b`<div class="version">v${e}</div>`}
  </ha-card>
`, $t = (n, t, e) => b`
  <ha-card class="status-card loading">
    <div class="card-content flex-col align-center p-8">
      <h1 class="status-title">${n}</h1>
      <ha-circular-progress active></ha-circular-progress>
      <div class="status-message mt-4">${t}</div>
    </div>
    <div class="version">v${e}</div>
  </ha-card>
`, At = D`
  ha-card.status-card {
    --ha-card-background: var(--warning-color, #ffeb3b);
    background-color: var(--warning-color, #ffeb3b) !important;
    border-radius: 12px;
    overflow: hidden;
  }
  ha-card.status-card.loading {
    --ha-card-background: var(--info-color, #2196f3);
    background-color: var(--info-color, #2196f3) !important;
  }
  ha-card.status-card.warning {
    --ha-card-background: var(--warning-color, #ffeb3b);
    background-color: var(--warning-color, #ffeb3b) !important;
  }

  /* Force high-contrast dark text on bright colored backgrounds in light mode */
  .status-card .status-title,
  .status-card .status-message {
    color: #111111 !important;
    text-align: center;
  }

  .status-card .status-title {
    margin: 0;
    font-size: 1.5rem;
    font-weight: bold;
  }

  @media (prefers-color-scheme: dark) {
    ha-card.status-card.warning {
      --ha-card-background: rgba(255, 193, 7, 0.2);
      background-color: rgba(255, 193, 7, 0.2) !important;
    }
    ha-card.status-card.loading {
      --ha-card-background: rgba(33, 150, 243, 0.2);
      background-color: rgba(33, 150, 243, 0.2) !important;
    }
    .status-card .status-title,
    .status-card .status-message {
      color: var(--primary-text-color) !important;
    }
  }

  .flex-col { display: flex; flex-direction: column; }
  .flex-col-center { display: flex; flex-direction: column; align-items: center; justify-content: center; }
  .align-center { align-items: center; }
  .p-8 { padding: 32px; }
  .mt-4 { margin-top: 16px; }

  .qr-container {
    background: white;
    padding: 16px;
    border-radius: 12px;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: var(--ha-card-box-shadow, 0 2px 2px 0 rgba(0, 0, 0, 0.14));
  }

  .qr-container svg {
    width: 100%;
    height: 100%;
  }

  .copyable-code {
    background: var(--card-background-color);
    padding: 4px 8px;
    border-radius: 4px;
    border: 1px solid var(--divider-color);
    font-family: var(--code-font-family, monospace);
    user-select: all;
  }

  .version {
    font-size: 9px;
    color: var(--secondary-text-color);
    text-align: right;
    padding: 4px 12px;
    opacity: 0.4;
  }

  /* Legacy styles for backward compatibility during transition */
  .meraki-warning {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px;
    background-color: var(--warning-color);
    color: var(--primary-text-color);
    border-radius: 8px;
  }
  .meraki-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 24px;
    gap: 12px;
  }
`;
var He = /* @__PURE__ */ ((n) => (n.GET_CONFIG = "meraki_ha/get_config", n.SUBSCRIBE_MERAKI_DATA = "meraki_ha/subscribe_meraki_data", n.GET_CAMERA_STREAM_URL = "meraki_ha/get_camera_stream_url", n.GET_CAMERA_SNAPSHOT = "meraki_ha/get_camera_snapshot", n.GET_VERSION = "meraki_ha/get_version", n.GET_NETWORK_EVENTS = "meraki_ha/get_network_events", n.UPDATE_ENABLED_NETWORKS = "meraki_ha/update_enabled_networks", n.CREATE_GUEST_KEY = "meraki_ha/ipsk/create", n.GET_GUEST_KEYS = "meraki_ha/ipsk/get", n.REVOKE_GUEST_KEY = "meraki_ha/ipsk/revoke", n.TIMED_ACCESS_GET_POLICIES = "meraki_ha/timed_access/get_policies", n))(He || {});
const As = async (n, t) => {
  if (!n)
    throw new Error("Home Assistant object is not available.");
  try {
    if (typeof n.callWS == "function")
      return await n.callWS(t);
    if (n.connection && typeof n.connection.sendMessagePromise == "function")
      return await n.connection.sendMessagePromise(t);
    throw new Error("Home Assistant WebSocket communication methods not found.");
  } catch (e) {
    throw console.error(`Cisco Meraki HA: WebSocket error [${t.type}]:`, e), e;
  }
};
class R {
  /**
   * Fetches wireless networks, SSIDs, and group policies directly from the integration's backend cache.
   */
  static async fetchConfig(t) {
    try {
      const e = await t.callWS({
        type: "config_entries/get",
        domain: "meraki_ha"
      }), i = e.length > 0 ? e[0].entry_id : null;
      if (!i)
        return { networks: [], ssids: [], groupPolicies: [], entryId: null };
      const s = await As(t, {
        type: He.GET_CONFIG,
        config_entry_id: i
      }), r = (Array.isArray(s.networks) ? s.networks : []).filter((c) => {
        var l;
        return (l = c.productTypes) == null ? void 0 : l.includes("wireless");
      }), o = Array.isArray(s.ssids) ? s.ssids : [], a = [];
      if (s.group_policies && typeof s.group_policies == "object")
        for (const [c, l] of Object.entries(
          s.group_policies
        ))
          Array.isArray(l) && l.forEach((d) => {
            a.push({
              networkId: c,
              groupPolicyId: String(d.groupPolicyId),
              name: d.name
            });
          });
      return { networks: r, ssids: o, groupPolicies: a, entryId: i };
    } catch (e) {
      return console.error("Failed to fetch Meraki data via WS:", e), { networks: [], ssids: [], groupPolicies: [], entryId: null };
    }
  }
  /**
   * Intelligently polls the backend until the API backoffs clear and data is populated.
   * @param hass The Home Assistant instance
   * @param onStatusUpdate Callback fired whenever the loading state or message changes
   * @param maxRetries Maximum number of polling attempts (default: 12 attempts / ~1 minute)
   * @param delayMs Delay between attempts in milliseconds (default: 5000ms)
   */
  static async pollConfig(t, e, i = 12, s = 5e3) {
    for (let r = 0; r < i; r++) {
      try {
        const o = await this.fetchConfig(t);
        if (o.networks.length > 0)
          return e("", !1), o;
        e(
          `Waiting for integration to sync... (Attempt ${r + 1}/${i})`,
          !0
        );
      } catch {
        e(
          `Error connecting to backend. Retrying... (Attempt ${r + 1}/${i})`,
          !0
        );
      }
      await new Promise((o) => setTimeout(o, s));
    }
    return e(
      "Integration failed to initialize after 1 minute. Please check backend logs.",
      !1
    ), { networks: [], ssids: [], groupPolicies: [], entryId: null };
  }
  /**
   * Formats networks for an ha-form dropdown.
   */
  static getNetworkOptions(t, e = !1) {
    const i = t.map((s) => ({ value: s.id, label: s.name }));
    return e ? [{ value: "", label: "All Networks" }, ...i] : i;
  }
  /**
   * Formats SSIDs for an ha-form dropdown.
   * @param valueType Determines if the dropdown returns the SSID's string name (for QR codes) or integer number (for Guest API calls).
   */
  static getSsidOptions(t, e, i = "name") {
    return (e ? t.filter((r) => r.networkId === e) : t).map((r) => ({
      value: i === "number" ? String(r.number) : r.name,
      label: `${r.name} (SSID ${r.number})`
    }));
  }
  /**
   * Formats Group Policies for an ha-form dropdown.
   */
  static getGroupPolicyOptions(t, e) {
    const s = (e ? t.filter((r) => r.networkId === e) : t).map((r) => ({
      value: r.groupPolicyId,
      label: r.name
    }));
    return [
      { value: "CREATE", label: "Create 'Home Assistant Guest' Policy" },
      { value: "NONE", label: "None (Network Default)" },
      ...s
    ];
  }
}
var kt = {}, ks = function() {
  return typeof Promise == "function" && Promise.prototype && Promise.prototype.then;
}, ze = {}, N = {};
let re;
const Ss = [
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
N.getSymbolSize = function(t) {
  if (!t) throw new Error('"version" cannot be null or undefined');
  if (t < 1 || t > 40) throw new Error('"version" should be in range from 1 to 40');
  return t * 4 + 17;
};
N.getSymbolTotalCodewords = function(t) {
  return Ss[t];
};
N.getBCHDigit = function(n) {
  let t = 0;
  for (; n !== 0; )
    t++, n >>>= 1;
  return t;
};
N.setToSJISFunction = function(t) {
  if (typeof t != "function")
    throw new Error('"toSJISFunc" is not a valid function.');
  re = t;
};
N.isKanjiModeEnabled = function() {
  return typeof re < "u";
};
N.toSJIS = function(t) {
  return re(t);
};
var Bt = {};
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
  n.isValid = function(i) {
    return i && typeof i.bit < "u" && i.bit >= 0 && i.bit < 4;
  }, n.from = function(i, s) {
    if (n.isValid(i))
      return i;
    try {
      return t(i);
    } catch {
      return s;
    }
  };
})(Bt);
function Fe() {
  this.buffer = [], this.length = 0;
}
Fe.prototype = {
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
var Ps = Fe;
function St(n) {
  if (!n || n < 1)
    throw new Error("BitMatrix size must be defined and greater than 0");
  this.size = n, this.data = new Uint8Array(n * n), this.reservedBit = new Uint8Array(n * n);
}
St.prototype.set = function(n, t, e, i) {
  const s = n * this.size + t;
  this.data[s] = e, i && (this.reservedBit[s] = !0);
};
St.prototype.get = function(n, t) {
  return this.data[n * this.size + t];
};
St.prototype.xor = function(n, t, e) {
  this.data[n * this.size + t] ^= e;
};
St.prototype.isReserved = function(n, t) {
  return this.reservedBit[n * this.size + t];
};
var Ns = St, Ve = {};
(function(n) {
  const t = N.getSymbolSize;
  n.getRowColCoords = function(i) {
    if (i === 1) return [];
    const s = Math.floor(i / 7) + 2, r = t(i), o = r === 145 ? 26 : Math.ceil((r - 13) / (2 * s - 2)) * 2, a = [r - 7];
    for (let c = 1; c < s - 1; c++)
      a[c] = a[c - 1] - o;
    return a.push(6), a.reverse();
  }, n.getPositions = function(i) {
    const s = [], r = n.getRowColCoords(i), o = r.length;
    for (let a = 0; a < o; a++)
      for (let c = 0; c < o; c++)
        a === 0 && c === 0 || // top-left
        a === 0 && c === o - 1 || // bottom-left
        a === o - 1 && c === 0 || s.push([r[a], r[c]]);
    return s;
  };
})(Ve);
var je = {};
const xs = N.getSymbolSize, Me = 7;
je.getPositions = function(t) {
  const e = xs(t);
  return [
    // top-left
    [0, 0],
    // top-right
    [e - Me, 0],
    // bottom-left
    [0, e - Me]
  ];
};
var qe = {};
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
  n.isValid = function(s) {
    return s != null && s !== "" && !isNaN(s) && s >= 0 && s <= 7;
  }, n.from = function(s) {
    return n.isValid(s) ? parseInt(s, 10) : void 0;
  }, n.getPenaltyN1 = function(s) {
    const r = s.size;
    let o = 0, a = 0, c = 0, l = null, d = null;
    for (let h = 0; h < r; h++) {
      a = c = 0, l = d = null;
      for (let u = 0; u < r; u++) {
        let f = s.get(h, u);
        f === l ? a++ : (a >= 5 && (o += t.N1 + (a - 5)), l = f, a = 1), f = s.get(u, h), f === d ? c++ : (c >= 5 && (o += t.N1 + (c - 5)), d = f, c = 1);
      }
      a >= 5 && (o += t.N1 + (a - 5)), c >= 5 && (o += t.N1 + (c - 5));
    }
    return o;
  }, n.getPenaltyN2 = function(s) {
    const r = s.size;
    let o = 0;
    for (let a = 0; a < r - 1; a++)
      for (let c = 0; c < r - 1; c++) {
        const l = s.get(a, c) + s.get(a, c + 1) + s.get(a + 1, c) + s.get(a + 1, c + 1);
        (l === 4 || l === 0) && o++;
      }
    return o * t.N2;
  }, n.getPenaltyN3 = function(s) {
    const r = s.size;
    let o = 0, a = 0, c = 0;
    for (let l = 0; l < r; l++) {
      a = c = 0;
      for (let d = 0; d < r; d++)
        a = a << 1 & 2047 | s.get(l, d), d >= 10 && (a === 1488 || a === 93) && o++, c = c << 1 & 2047 | s.get(d, l), d >= 10 && (c === 1488 || c === 93) && o++;
    }
    return o * t.N3;
  }, n.getPenaltyN4 = function(s) {
    let r = 0;
    const o = s.data.length;
    for (let c = 0; c < o; c++) r += s.data[c];
    return Math.abs(Math.ceil(r * 100 / o / 5) - 10) * t.N4;
  };
  function e(i, s, r) {
    switch (i) {
      case n.Patterns.PATTERN000:
        return (s + r) % 2 === 0;
      case n.Patterns.PATTERN001:
        return s % 2 === 0;
      case n.Patterns.PATTERN010:
        return r % 3 === 0;
      case n.Patterns.PATTERN011:
        return (s + r) % 3 === 0;
      case n.Patterns.PATTERN100:
        return (Math.floor(s / 2) + Math.floor(r / 3)) % 2 === 0;
      case n.Patterns.PATTERN101:
        return s * r % 2 + s * r % 3 === 0;
      case n.Patterns.PATTERN110:
        return (s * r % 2 + s * r % 3) % 2 === 0;
      case n.Patterns.PATTERN111:
        return (s * r % 3 + (s + r) % 2) % 2 === 0;
      default:
        throw new Error("bad maskPattern:" + i);
    }
  }
  n.applyMask = function(s, r) {
    const o = r.size;
    for (let a = 0; a < o; a++)
      for (let c = 0; c < o; c++)
        r.isReserved(c, a) || r.xor(c, a, e(s, c, a));
  }, n.getBestMask = function(s, r) {
    const o = Object.keys(n.Patterns).length;
    let a = 0, c = 1 / 0;
    for (let l = 0; l < o; l++) {
      r(l), n.applyMask(l, s);
      const d = n.getPenaltyN1(s) + n.getPenaltyN2(s) + n.getPenaltyN3(s) + n.getPenaltyN4(s);
      n.applyMask(l, s), d < c && (c = d, a = l);
    }
    return a;
  };
})(qe);
var Rt = {};
const q = Bt, Pt = [
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
], Nt = [
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
Rt.getBlocksCount = function(t, e) {
  switch (e) {
    case q.L:
      return Pt[(t - 1) * 4 + 0];
    case q.M:
      return Pt[(t - 1) * 4 + 1];
    case q.Q:
      return Pt[(t - 1) * 4 + 2];
    case q.H:
      return Pt[(t - 1) * 4 + 3];
    default:
      return;
  }
};
Rt.getTotalCodewordsCount = function(t, e) {
  switch (e) {
    case q.L:
      return Nt[(t - 1) * 4 + 0];
    case q.M:
      return Nt[(t - 1) * 4 + 1];
    case q.Q:
      return Nt[(t - 1) * 4 + 2];
    case q.H:
      return Nt[(t - 1) * 4 + 3];
    default:
      return;
  }
};
var Ge = {}, Ut = {};
const gt = new Uint8Array(512), It = new Uint8Array(256);
(function() {
  let t = 1;
  for (let e = 0; e < 255; e++)
    gt[e] = t, It[t] = e, t <<= 1, t & 256 && (t ^= 285);
  for (let e = 255; e < 512; e++)
    gt[e] = gt[e - 255];
})();
Ut.log = function(t) {
  if (t < 1) throw new Error("log(" + t + ")");
  return It[t];
};
Ut.exp = function(t) {
  return gt[t];
};
Ut.mul = function(t, e) {
  return t === 0 || e === 0 ? 0 : gt[It[t] + It[e]];
};
(function(n) {
  const t = Ut;
  n.mul = function(i, s) {
    const r = new Uint8Array(i.length + s.length - 1);
    for (let o = 0; o < i.length; o++)
      for (let a = 0; a < s.length; a++)
        r[o + a] ^= t.mul(i[o], s[a]);
    return r;
  }, n.mod = function(i, s) {
    let r = new Uint8Array(i);
    for (; r.length - s.length >= 0; ) {
      const o = r[0];
      for (let c = 0; c < s.length; c++)
        r[c] ^= t.mul(s[c], o);
      let a = 0;
      for (; a < r.length && r[a] === 0; ) a++;
      r = r.slice(a);
    }
    return r;
  }, n.generateECPolynomial = function(i) {
    let s = new Uint8Array([1]);
    for (let r = 0; r < i; r++)
      s = n.mul(s, new Uint8Array([1, t.exp(r)]));
    return s;
  };
})(Ge);
const Ke = Ge;
function oe(n) {
  this.genPoly = void 0, this.degree = n, this.degree && this.initialize(this.degree);
}
oe.prototype.initialize = function(t) {
  this.degree = t, this.genPoly = Ke.generateECPolynomial(this.degree);
};
oe.prototype.encode = function(t) {
  if (!this.genPoly)
    throw new Error("Encoder not initialized");
  const e = new Uint8Array(t.length + this.degree);
  e.set(t);
  const i = Ke.mod(e, this.genPoly), s = this.degree - i.length;
  if (s > 0) {
    const r = new Uint8Array(this.degree);
    return r.set(i, s), r;
  }
  return i;
};
var Ms = oe, We = {}, K = {}, ae = {};
ae.isValid = function(t) {
  return !isNaN(t) && t >= 1 && t <= 40;
};
var U = {};
const Je = "[0-9]+", Ts = "[A-Z $%*+\\-./:]+";
let yt = "(?:[u3000-u303F]|[u3040-u309F]|[u30A0-u30FF]|[uFF00-uFFEF]|[u4E00-u9FAF]|[u2605-u2606]|[u2190-u2195]|u203B|[u2010u2015u2018u2019u2025u2026u201Cu201Du2225u2260]|[u0391-u0451]|[u00A7u00A8u00B1u00B4u00D7u00F7])+";
yt = yt.replace(/u/g, "\\u");
const Is = "(?:(?![A-Z0-9 $%*+\\-./:]|" + yt + `)(?:.|[\r
]))+`;
U.KANJI = new RegExp(yt, "g");
U.BYTE_KANJI = new RegExp("[^A-Z0-9 $%*+\\-./:]+", "g");
U.BYTE = new RegExp(Is, "g");
U.NUMERIC = new RegExp(Je, "g");
U.ALPHANUMERIC = new RegExp(Ts, "g");
const Ds = new RegExp("^" + yt + "$"), Ls = new RegExp("^" + Je + "$"), Bs = new RegExp("^[A-Z0-9 $%*+\\-./:]+$");
U.testKanji = function(t) {
  return Ds.test(t);
};
U.testNumeric = function(t) {
  return Ls.test(t);
};
U.testAlphanumeric = function(t) {
  return Bs.test(t);
};
(function(n) {
  const t = ae, e = U;
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
  function i(s) {
    if (typeof s != "string")
      throw new Error("Param is not a string");
    switch (s.toLowerCase()) {
      case "numeric":
        return n.NUMERIC;
      case "alphanumeric":
        return n.ALPHANUMERIC;
      case "kanji":
        return n.KANJI;
      case "byte":
        return n.BYTE;
      default:
        throw new Error("Unknown mode: " + s);
    }
  }
  n.from = function(r, o) {
    if (n.isValid(r))
      return r;
    try {
      return i(r);
    } catch {
      return o;
    }
  };
})(K);
(function(n) {
  const t = N, e = Rt, i = Bt, s = K, r = ae, o = 7973, a = t.getBCHDigit(o);
  function c(u, f, g) {
    for (let w = 1; w <= 40; w++)
      if (f <= n.getCapacity(w, g, u))
        return w;
  }
  function l(u, f) {
    return s.getCharCountIndicator(u, f) + 4;
  }
  function d(u, f) {
    let g = 0;
    return u.forEach(function(w) {
      const k = l(w.mode, f);
      g += k + w.getBitsLength();
    }), g;
  }
  function h(u, f) {
    for (let g = 1; g <= 40; g++)
      if (d(u, g) <= n.getCapacity(g, f, s.MIXED))
        return g;
  }
  n.from = function(f, g) {
    return r.isValid(f) ? parseInt(f, 10) : g;
  }, n.getCapacity = function(f, g, w) {
    if (!r.isValid(f))
      throw new Error("Invalid QR Code version");
    typeof w > "u" && (w = s.BYTE);
    const k = t.getSymbolTotalCodewords(f), _ = e.getTotalCodewordsCount(f, g), v = (k - _) * 8;
    if (w === s.MIXED) return v;
    const m = v - l(w, f);
    switch (w) {
      case s.NUMERIC:
        return Math.floor(m / 10 * 3);
      case s.ALPHANUMERIC:
        return Math.floor(m / 11 * 2);
      case s.KANJI:
        return Math.floor(m / 13);
      case s.BYTE:
      default:
        return Math.floor(m / 8);
    }
  }, n.getBestVersionForData = function(f, g) {
    let w;
    const k = i.from(g, i.M);
    if (Array.isArray(f)) {
      if (f.length > 1)
        return h(f, k);
      if (f.length === 0)
        return 1;
      w = f[0];
    } else
      w = f;
    return c(w.mode, w.getLength(), k);
  }, n.getEncodedBits = function(f) {
    if (!r.isValid(f) || f < 7)
      throw new Error("Invalid QR Code version");
    let g = f << 12;
    for (; t.getBCHDigit(g) - a >= 0; )
      g ^= o << t.getBCHDigit(g) - a;
    return f << 12 | g;
  };
})(We);
var Ye = {};
const Yt = N, Qe = 1335, Rs = 21522, Te = Yt.getBCHDigit(Qe);
Ye.getEncodedBits = function(t, e) {
  const i = t.bit << 3 | e;
  let s = i << 10;
  for (; Yt.getBCHDigit(s) - Te >= 0; )
    s ^= Qe << Yt.getBCHDigit(s) - Te;
  return (i << 10 | s) ^ Rs;
};
var Ze = {};
const Us = K;
function nt(n) {
  this.mode = Us.NUMERIC, this.data = n.toString();
}
nt.getBitsLength = function(t) {
  return 10 * Math.floor(t / 3) + (t % 3 ? t % 3 * 3 + 1 : 0);
};
nt.prototype.getLength = function() {
  return this.data.length;
};
nt.prototype.getBitsLength = function() {
  return nt.getBitsLength(this.data.length);
};
nt.prototype.write = function(t) {
  let e, i, s;
  for (e = 0; e + 3 <= this.data.length; e += 3)
    i = this.data.substr(e, 3), s = parseInt(i, 10), t.put(s, 10);
  const r = this.data.length - e;
  r > 0 && (i = this.data.substr(e), s = parseInt(i, 10), t.put(s, r * 3 + 1));
};
var Os = nt;
const Hs = K, qt = [
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
function rt(n) {
  this.mode = Hs.ALPHANUMERIC, this.data = n;
}
rt.getBitsLength = function(t) {
  return 11 * Math.floor(t / 2) + 6 * (t % 2);
};
rt.prototype.getLength = function() {
  return this.data.length;
};
rt.prototype.getBitsLength = function() {
  return rt.getBitsLength(this.data.length);
};
rt.prototype.write = function(t) {
  let e;
  for (e = 0; e + 2 <= this.data.length; e += 2) {
    let i = qt.indexOf(this.data[e]) * 45;
    i += qt.indexOf(this.data[e + 1]), t.put(i, 11);
  }
  this.data.length % 2 && t.put(qt.indexOf(this.data[e]), 6);
};
var zs = rt;
const Fs = K;
function ot(n) {
  this.mode = Fs.BYTE, typeof n == "string" ? this.data = new TextEncoder().encode(n) : this.data = new Uint8Array(n);
}
ot.getBitsLength = function(t) {
  return t * 8;
};
ot.prototype.getLength = function() {
  return this.data.length;
};
ot.prototype.getBitsLength = function() {
  return ot.getBitsLength(this.data.length);
};
ot.prototype.write = function(n) {
  for (let t = 0, e = this.data.length; t < e; t++)
    n.put(this.data[t], 8);
};
var Vs = ot;
const js = K, qs = N;
function at(n) {
  this.mode = js.KANJI, this.data = n;
}
at.getBitsLength = function(t) {
  return t * 13;
};
at.prototype.getLength = function() {
  return this.data.length;
};
at.prototype.getBitsLength = function() {
  return at.getBitsLength(this.data.length);
};
at.prototype.write = function(n) {
  let t;
  for (t = 0; t < this.data.length; t++) {
    let e = qs.toSJIS(this.data[t]);
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
var Gs = at, Xe = { exports: {} };
(function(n) {
  var t = {
    single_source_shortest_paths: function(e, i, s) {
      var r = {}, o = {};
      o[i] = 0;
      var a = t.PriorityQueue.make();
      a.push(i, 0);
      for (var c, l, d, h, u, f, g, w, k; !a.empty(); ) {
        c = a.pop(), l = c.value, h = c.cost, u = e[l] || {};
        for (d in u)
          u.hasOwnProperty(d) && (f = u[d], g = h + f, w = o[d], k = typeof o[d] > "u", (k || w > g) && (o[d] = g, a.push(d, g), r[d] = l));
      }
      if (typeof s < "u" && typeof o[s] > "u") {
        var _ = ["Could not find a path from ", i, " to ", s, "."].join("");
        throw new Error(_);
      }
      return r;
    },
    extract_shortest_path_from_predecessor_list: function(e, i) {
      for (var s = [], r = i; r; )
        s.push(r), e[r], r = e[r];
      return s.reverse(), s;
    },
    find_path: function(e, i, s) {
      var r = t.single_source_shortest_paths(e, i, s);
      return t.extract_shortest_path_from_predecessor_list(
        r,
        s
      );
    },
    /**
     * A very naive priority queue implementation.
     */
    PriorityQueue: {
      make: function(e) {
        var i = t.PriorityQueue, s = {}, r;
        e = e || {};
        for (r in i)
          i.hasOwnProperty(r) && (s[r] = i[r]);
        return s.queue = [], s.sorter = e.sorter || i.default_sorter, s;
      },
      default_sorter: function(e, i) {
        return e.cost - i.cost;
      },
      /**
       * Add a new item to the queue and ensure the highest priority element
       * is at the front of the queue.
       */
      push: function(e, i) {
        var s = { value: e, cost: i };
        this.queue.push(s), this.queue.sort(this.sorter);
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
})(Xe);
var Ks = Xe.exports;
(function(n) {
  const t = K, e = Os, i = zs, s = Vs, r = Gs, o = U, a = N, c = Ks;
  function l(_) {
    return unescape(encodeURIComponent(_)).length;
  }
  function d(_, v, m) {
    const p = [];
    let E;
    for (; (E = _.exec(m)) !== null; )
      p.push({
        data: E[0],
        index: E.index,
        mode: v,
        length: E[0].length
      });
    return p;
  }
  function h(_) {
    const v = d(o.NUMERIC, t.NUMERIC, _), m = d(o.ALPHANUMERIC, t.ALPHANUMERIC, _);
    let p, E;
    return a.isKanjiModeEnabled() ? (p = d(o.BYTE, t.BYTE, _), E = d(o.KANJI, t.KANJI, _)) : (p = d(o.BYTE_KANJI, t.BYTE, _), E = []), v.concat(m, p, E).sort(function($, I) {
      return $.index - I.index;
    }).map(function($) {
      return {
        data: $.data,
        mode: $.mode,
        length: $.length
      };
    });
  }
  function u(_, v) {
    switch (v) {
      case t.NUMERIC:
        return e.getBitsLength(_);
      case t.ALPHANUMERIC:
        return i.getBitsLength(_);
      case t.KANJI:
        return r.getBitsLength(_);
      case t.BYTE:
        return s.getBitsLength(_);
    }
  }
  function f(_) {
    return _.reduce(function(v, m) {
      const p = v.length - 1 >= 0 ? v[v.length - 1] : null;
      return p && p.mode === m.mode ? (v[v.length - 1].data += m.data, v) : (v.push(m), v);
    }, []);
  }
  function g(_) {
    const v = [];
    for (let m = 0; m < _.length; m++) {
      const p = _[m];
      switch (p.mode) {
        case t.NUMERIC:
          v.push([
            p,
            { data: p.data, mode: t.ALPHANUMERIC, length: p.length },
            { data: p.data, mode: t.BYTE, length: p.length }
          ]);
          break;
        case t.ALPHANUMERIC:
          v.push([
            p,
            { data: p.data, mode: t.BYTE, length: p.length }
          ]);
          break;
        case t.KANJI:
          v.push([
            p,
            { data: p.data, mode: t.BYTE, length: l(p.data) }
          ]);
          break;
        case t.BYTE:
          v.push([
            { data: p.data, mode: t.BYTE, length: l(p.data) }
          ]);
      }
    }
    return v;
  }
  function w(_, v) {
    const m = {}, p = { start: {} };
    let E = ["start"];
    for (let C = 0; C < _.length; C++) {
      const $ = _[C], I = [];
      for (let V = 0; V < $.length; V++) {
        const B = $[V], dt = "" + C + V;
        I.push(dt), m[dt] = { node: B, lastCount: 0 }, p[dt] = {};
        for (let Ht = 0; Ht < E.length; Ht++) {
          const O = E[Ht];
          m[O] && m[O].node.mode === B.mode ? (p[O][dt] = u(m[O].lastCount + B.length, B.mode) - u(m[O].lastCount, B.mode), m[O].lastCount += B.length) : (m[O] && (m[O].lastCount = B.length), p[O][dt] = u(B.length, B.mode) + 4 + t.getCharCountIndicator(B.mode, v));
        }
      }
      E = I;
    }
    for (let C = 0; C < E.length; C++)
      p[E[C]].end = 0;
    return { map: p, table: m };
  }
  function k(_, v) {
    let m;
    const p = t.getBestModeForData(_);
    if (m = t.from(v, p), m !== t.BYTE && m.bit < p.bit)
      throw new Error('"' + _ + '" cannot be encoded with mode ' + t.toString(m) + `.
 Suggested mode is: ` + t.toString(p));
    switch (m === t.KANJI && !a.isKanjiModeEnabled() && (m = t.BYTE), m) {
      case t.NUMERIC:
        return new e(_);
      case t.ALPHANUMERIC:
        return new i(_);
      case t.KANJI:
        return new r(_);
      case t.BYTE:
        return new s(_);
    }
  }
  n.fromArray = function(v) {
    return v.reduce(function(m, p) {
      return typeof p == "string" ? m.push(k(p, null)) : p.data && m.push(k(p.data, p.mode)), m;
    }, []);
  }, n.fromString = function(v, m) {
    const p = h(v, a.isKanjiModeEnabled()), E = g(p), C = w(E, m), $ = c.find_path(C.map, "start", "end"), I = [];
    for (let V = 1; V < $.length - 1; V++)
      I.push(C.table[$[V]].node);
    return n.fromArray(f(I));
  }, n.rawSplit = function(v) {
    return n.fromArray(
      h(v, a.isKanjiModeEnabled())
    );
  };
})(Ze);
const Ot = N, Gt = Bt, Ws = Ps, Js = Ns, Ys = Ve, Qs = je, Qt = qe, Zt = Rt, Zs = Ms, Dt = We, Xs = Ye, ti = K, Kt = Ze;
function ei(n, t) {
  const e = n.size, i = Qs.getPositions(t);
  for (let s = 0; s < i.length; s++) {
    const r = i[s][0], o = i[s][1];
    for (let a = -1; a <= 7; a++)
      if (!(r + a <= -1 || e <= r + a))
        for (let c = -1; c <= 7; c++)
          o + c <= -1 || e <= o + c || (a >= 0 && a <= 6 && (c === 0 || c === 6) || c >= 0 && c <= 6 && (a === 0 || a === 6) || a >= 2 && a <= 4 && c >= 2 && c <= 4 ? n.set(r + a, o + c, !0, !0) : n.set(r + a, o + c, !1, !0));
  }
}
function si(n) {
  const t = n.size;
  for (let e = 8; e < t - 8; e++) {
    const i = e % 2 === 0;
    n.set(e, 6, i, !0), n.set(6, e, i, !0);
  }
}
function ii(n, t) {
  const e = Ys.getPositions(t);
  for (let i = 0; i < e.length; i++) {
    const s = e[i][0], r = e[i][1];
    for (let o = -2; o <= 2; o++)
      for (let a = -2; a <= 2; a++)
        o === -2 || o === 2 || a === -2 || a === 2 || o === 0 && a === 0 ? n.set(s + o, r + a, !0, !0) : n.set(s + o, r + a, !1, !0);
  }
}
function ni(n, t) {
  const e = n.size, i = Dt.getEncodedBits(t);
  let s, r, o;
  for (let a = 0; a < 18; a++)
    s = Math.floor(a / 3), r = a % 3 + e - 8 - 3, o = (i >> a & 1) === 1, n.set(s, r, o, !0), n.set(r, s, o, !0);
}
function Wt(n, t, e) {
  const i = n.size, s = Xs.getEncodedBits(t, e);
  let r, o;
  for (r = 0; r < 15; r++)
    o = (s >> r & 1) === 1, r < 6 ? n.set(r, 8, o, !0) : r < 8 ? n.set(r + 1, 8, o, !0) : n.set(i - 15 + r, 8, o, !0), r < 8 ? n.set(8, i - r - 1, o, !0) : r < 9 ? n.set(8, 15 - r - 1 + 1, o, !0) : n.set(8, 15 - r - 1, o, !0);
  n.set(i - 8, 8, 1, !0);
}
function ri(n, t) {
  const e = n.size;
  let i = -1, s = e - 1, r = 7, o = 0;
  for (let a = e - 1; a > 0; a -= 2)
    for (a === 6 && a--; ; ) {
      for (let c = 0; c < 2; c++)
        if (!n.isReserved(s, a - c)) {
          let l = !1;
          o < t.length && (l = (t[o] >>> r & 1) === 1), n.set(s, a - c, l), r--, r === -1 && (o++, r = 7);
        }
      if (s += i, s < 0 || e <= s) {
        s -= i, i = -i;
        break;
      }
    }
}
function oi(n, t, e) {
  const i = new Ws();
  e.forEach(function(c) {
    i.put(c.mode.bit, 4), i.put(c.getLength(), ti.getCharCountIndicator(c.mode, n)), c.write(i);
  });
  const s = Ot.getSymbolTotalCodewords(n), r = Zt.getTotalCodewordsCount(n, t), o = (s - r) * 8;
  for (i.getLengthInBits() + 4 <= o && i.put(0, 4); i.getLengthInBits() % 8 !== 0; )
    i.putBit(0);
  const a = (o - i.getLengthInBits()) / 8;
  for (let c = 0; c < a; c++)
    i.put(c % 2 ? 17 : 236, 8);
  return ai(i, n, t);
}
function ai(n, t, e) {
  const i = Ot.getSymbolTotalCodewords(t), s = Zt.getTotalCodewordsCount(t, e), r = i - s, o = Zt.getBlocksCount(t, e), a = i % o, c = o - a, l = Math.floor(i / o), d = Math.floor(r / o), h = d + 1, u = l - d, f = new Zs(u);
  let g = 0;
  const w = new Array(o), k = new Array(o);
  let _ = 0;
  const v = new Uint8Array(n.buffer);
  for (let $ = 0; $ < o; $++) {
    const I = $ < c ? d : h;
    w[$] = v.slice(g, g + I), k[$] = f.encode(w[$]), g += I, _ = Math.max(_, I);
  }
  const m = new Uint8Array(i);
  let p = 0, E, C;
  for (E = 0; E < _; E++)
    for (C = 0; C < o; C++)
      E < w[C].length && (m[p++] = w[C][E]);
  for (E = 0; E < u; E++)
    for (C = 0; C < o; C++)
      m[p++] = k[C][E];
  return m;
}
function ci(n, t, e, i) {
  let s;
  if (Array.isArray(n))
    s = Kt.fromArray(n);
  else if (typeof n == "string") {
    let l = t;
    if (!l) {
      const d = Kt.rawSplit(n);
      l = Dt.getBestVersionForData(d, e);
    }
    s = Kt.fromString(n, l || 40);
  } else
    throw new Error("Invalid data");
  const r = Dt.getBestVersionForData(s, e);
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
  const o = oi(t, e, s), a = Ot.getSymbolSize(t), c = new Js(a);
  return ei(c, t), si(c), ii(c, t), Wt(c, e, 0), t >= 7 && ni(c, t), ri(c, o), isNaN(i) && (i = Qt.getBestMask(
    c,
    Wt.bind(null, c, e)
  )), Qt.applyMask(i, c), Wt(c, e, i), {
    modules: c,
    version: t,
    errorCorrectionLevel: e,
    maskPattern: i,
    segments: s
  };
}
ze.create = function(t, e) {
  if (typeof t > "u" || t === "")
    throw new Error("No input text");
  let i = Gt.M, s, r;
  return typeof e < "u" && (i = Gt.from(e.errorCorrectionLevel, Gt.M), s = Dt.from(e.version), r = Qt.from(e.maskPattern), e.toSJISFunc && Ot.setToSJISFunction(e.toSJISFunc)), ci(t, s, i, r);
};
var ts = {}, ce = {};
(function(n) {
  function t(e) {
    if (typeof e == "number" && (e = e.toString()), typeof e != "string")
      throw new Error("Color should be defined as hex string");
    let i = e.slice().replace("#", "").split("");
    if (i.length < 3 || i.length === 5 || i.length > 8)
      throw new Error("Invalid hex color: " + e);
    (i.length === 3 || i.length === 4) && (i = Array.prototype.concat.apply([], i.map(function(r) {
      return [r, r];
    }))), i.length === 6 && i.push("F", "F");
    const s = parseInt(i.join(""), 16);
    return {
      r: s >> 24 & 255,
      g: s >> 16 & 255,
      b: s >> 8 & 255,
      a: s & 255,
      hex: "#" + i.slice(0, 6).join("")
    };
  }
  n.getOptions = function(i) {
    i || (i = {}), i.color || (i.color = {});
    const s = typeof i.margin > "u" || i.margin === null || i.margin < 0 ? 4 : i.margin, r = i.width && i.width >= 21 ? i.width : void 0, o = i.scale || 4;
    return {
      width: r,
      scale: r ? 4 : o,
      margin: s,
      color: {
        dark: t(i.color.dark || "#000000ff"),
        light: t(i.color.light || "#ffffffff")
      },
      type: i.type,
      rendererOpts: i.rendererOpts || {}
    };
  }, n.getScale = function(i, s) {
    return s.width && s.width >= i + s.margin * 2 ? s.width / (i + s.margin * 2) : s.scale;
  }, n.getImageWidth = function(i, s) {
    const r = n.getScale(i, s);
    return Math.floor((i + s.margin * 2) * r);
  }, n.qrToImageData = function(i, s, r) {
    const o = s.modules.size, a = s.modules.data, c = n.getScale(o, r), l = Math.floor((o + r.margin * 2) * c), d = r.margin * c, h = [r.color.light, r.color.dark];
    for (let u = 0; u < l; u++)
      for (let f = 0; f < l; f++) {
        let g = (u * l + f) * 4, w = r.color.light;
        if (u >= d && f >= d && u < l - d && f < l - d) {
          const k = Math.floor((u - d) / c), _ = Math.floor((f - d) / c);
          w = h[a[k * o + _] ? 1 : 0];
        }
        i[g++] = w.r, i[g++] = w.g, i[g++] = w.b, i[g] = w.a;
      }
  };
})(ce);
(function(n) {
  const t = ce;
  function e(s, r, o) {
    s.clearRect(0, 0, r.width, r.height), r.style || (r.style = {}), r.height = o, r.width = o, r.style.height = o + "px", r.style.width = o + "px";
  }
  function i() {
    try {
      return document.createElement("canvas");
    } catch {
      throw new Error("You need to specify a canvas element");
    }
  }
  n.render = function(r, o, a) {
    let c = a, l = o;
    typeof c > "u" && (!o || !o.getContext) && (c = o, o = void 0), o || (l = i()), c = t.getOptions(c);
    const d = t.getImageWidth(r.modules.size, c), h = l.getContext("2d"), u = h.createImageData(d, d);
    return t.qrToImageData(u.data, r, c), e(h, l, d), h.putImageData(u, 0, 0), l;
  }, n.renderToDataURL = function(r, o, a) {
    let c = a;
    typeof c > "u" && (!o || !o.getContext) && (c = o, o = void 0), c || (c = {});
    const l = n.render(r, o, c), d = c.type || "image/png", h = c.rendererOpts || {};
    return l.toDataURL(d, h.quality);
  };
})(ts);
var es = {};
const li = ce;
function Ie(n, t) {
  const e = n.a / 255, i = t + '="' + n.hex + '"';
  return e < 1 ? i + " " + t + '-opacity="' + e.toFixed(2).slice(1) + '"' : i;
}
function Jt(n, t, e) {
  let i = n + t;
  return typeof e < "u" && (i += " " + e), i;
}
function di(n, t, e) {
  let i = "", s = 0, r = !1, o = 0;
  for (let a = 0; a < n.length; a++) {
    const c = Math.floor(a % t), l = Math.floor(a / t);
    !c && !r && (r = !0), n[a] ? (o++, a > 0 && c > 0 && n[a - 1] || (i += r ? Jt("M", c + e, 0.5 + l + e) : Jt("m", s, 0), s = 0, r = !1), c + 1 < t && n[a + 1] || (i += Jt("h", o), o = 0)) : s++;
  }
  return i;
}
es.render = function(t, e, i) {
  const s = li.getOptions(e), r = t.modules.size, o = t.modules.data, a = r + s.margin * 2, c = s.color.light.a ? "<path " + Ie(s.color.light, "fill") + ' d="M0 0h' + a + "v" + a + 'H0z"/>' : "", l = "<path " + Ie(s.color.dark, "stroke") + ' d="' + di(o, r, s.margin) + '"/>', d = 'viewBox="0 0 ' + a + " " + a + '"', u = '<svg xmlns="http://www.w3.org/2000/svg" ' + (s.width ? 'width="' + s.width + '" height="' + s.width + '" ' : "") + d + ' shape-rendering="crispEdges">' + c + l + `</svg>
`;
  return typeof i == "function" && i(null, u), u;
};
const hi = ks, Xt = ze, ss = ts, ui = es;
function le(n, t, e, i, s) {
  const r = [].slice.call(arguments, 1), o = r.length, a = typeof r[o - 1] == "function";
  if (!a && !hi())
    throw new Error("Callback required as last argument");
  if (a) {
    if (o < 2)
      throw new Error("Too few arguments provided");
    o === 2 ? (s = e, e = t, t = i = void 0) : o === 3 && (t.getContext && typeof s > "u" ? (s = i, i = void 0) : (s = i, i = e, e = t, t = void 0));
  } else {
    if (o < 1)
      throw new Error("Too few arguments provided");
    return o === 1 ? (e = t, t = i = void 0) : o === 2 && !t.getContext && (i = e, e = t, t = void 0), new Promise(function(c, l) {
      try {
        const d = Xt.create(e, i);
        c(n(d, t, i));
      } catch (d) {
        l(d);
      }
    });
  }
  try {
    const c = Xt.create(e, i);
    s(null, n(c, t, i));
  } catch (c) {
    s(c);
  }
}
kt.create = Xt.create;
kt.toCanvas = le.bind(null, ss.render);
kt.toDataURL = le.bind(null, ss.renderToDataURL);
kt.toString = le.bind(null, function(n, t, e) {
  return ui.render(n, e);
});
class M {
  /**
   * Resolves a value that might be an entity ID or a raw string.
   */
  static getValue(t, e) {
    return !e || !t ? e || "" : t.states[e] ? t.states[e].state : e;
  }
  /**
   * Discovers a Wi-Fi password using manual overrides, entity IDs, or smart attribute mapping.
   */
  static getPasswordForSsid(t, e, i, s, r) {
    if (!t) return "";
    if (r && r !== "password123")
      return this.getValue(t, r);
    if (!i) return "";
    const o = parseInt(i, 10), a = e.find((d) => {
      const h = !s || d.networkId === s;
      return isNaN(o) ? d.name === i && h : d.number === o && h;
    });
    if (a)
      for (const d in t.states) {
        const h = t.states[d], u = h.attributes;
        if (u.network_id === a.networkId && u.ssid_number === a.number) {
          if (u.psk) return String(u.psk);
          if (u.password) return String(u.password);
          if (h.state && !["unknown", "unavailable"].includes(h.state) && (d.includes("password") || d.includes("psk")))
            return h.state;
        }
      }
    const l = (a ? a.name : i).toLowerCase().replace(/[^a-z0-9]/g, "_");
    for (const d in t.states)
      if (d.includes(l) && (d.includes("password") || d.includes("psk"))) {
        const h = t.states[d];
        if (h.state && !["unknown", "unavailable"].includes(h.state))
          return h.state;
      }
    return "";
  }
  /**
   * Escapes special characters for Wi-Fi QR strings.
   */
  static escapeWifiString(t) {
    return t.replace(/([\\;,:"])/g, "\\$1");
  }
  /**
   * Generates a standard Wi-Fi QR string.
   */
  static generateWifiQrString(t, e) {
    const i = this.escapeWifiString(t), s = e ? this.escapeWifiString(e) : "";
    return s ? `WIFI:T:WPA;S:${i};P:${s};;` : `WIFI:T:nopass;S:${i};P:;;`;
  }
  /**
   * Generates an SVG QR code from a string.
   */
  static async generateQrSvg(t, e = 1) {
    try {
      return await kt.toString(t, {
        type: "svg",
        margin: e,
        color: {
          dark: "#000000",
          light: "#ffffff"
        }
      });
    } catch (i) {
      return console.error("Failed to generate QR code SVG:", i), '<div style="text-align:center; padding: 24px;">QR Code Unavailable</div>';
    }
  }
  /**
   * Generates a random, human-readable natural password.
   */
  static generateNaturalPassword() {
    const t = [
      "hot",
      "cold",
      "fast",
      "slow",
      "red",
      "blue",
      "green",
      "tall",
      "short",
      "loud",
      "quiet",
      "happy",
      "brave",
      "calm",
      "cool",
      "smart",
      "bright",
      "clear",
      "warm",
      "wild",
      "free",
      "solid",
      "swift",
      "dark",
      "light"
    ], e = [
      "butter",
      "potato",
      "apple",
      "tiger",
      "lion",
      "bear",
      "hawk",
      "tree",
      "river",
      "mountain",
      "ocean",
      "breeze",
      "cloud",
      "star",
      "moon",
      "forest",
      "stone",
      "water",
      "fire",
      "wood",
      "metal",
      "glass",
      "sky",
      "earth",
      "sun"
    ], i = (s) => s[Math.floor(Math.random() * s.length)];
    return `${i(t)}-${i(e)}-${Math.floor(Math.random() * 1e3)}`;
  }
}
var fi = Object.defineProperty, W = (n, t, e, i) => {
  for (var s = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = o(t, e, s) || s);
  return s && fi(t, e, s), s;
};
const de = class de extends P {
  constructor() {
    super(...arguments), this._optimisticProfile = null, this._isUpdating = !1, this._isLoading = !0, this._loadingMessage = "Connecting...";
  }
  static async getConfigElement() {
    return document.createElement("meraki-content-filter-card-editor");
  }
  setConfig(t) {
    if (!t)
      throw new Error("Invalid configuration");
    this._config = { ...t };
  }
  firstUpdated(t) {
    super.firstUpdated(t), this._loadCentralizedData();
  }
  async _loadCentralizedData() {
    this.hass && await R.pollConfig(
      this.hass,
      (t, e) => {
        this._loadingMessage = t, this._isLoading = e;
      }
    );
  }
  _discoverEntity() {
    if (this.hass)
      return Object.keys(this.hass.states).find((t) => {
        var s;
        if (!t.startsWith("select.")) return !1;
        const i = ((s = this.hass.states[t].attributes.friendly_name) == null ? void 0 : s.toLowerCase()) || "";
        return t.includes("content_filter") || i.includes("content filter") || t.includes("meraki");
      });
  }
  static getStubConfig() {
    return {
      entity: "",
      name: ""
    };
  }
  render() {
    var l, d, h;
    if (!this.hass || !this._config) return b``;
    if (this._isLoading)
      return $t(
        ((l = this._config) == null ? void 0 : l.name) || "Cisco Meraki Content Filter",
        this._loadingMessage,
        "2.3.0-beta.3534"
      );
    const t = this._config.entity || this._discoverEntity(), e = t ? this.hass.states[t] : void 0, i = this._config.entity ? this.hass.states[this._config.entity] : void 0, s = ((d = i == null ? void 0 : i.attributes) == null ? void 0 : d.friendly_name) || "Cisco Meraki", r = this._config.name || (this._config.entity ? `${s} Content Filter` : "Cisco Meraki Content Filter");
    if (!t || !e)
      return ne(
        "Entity Missing",
        "No content filter entity was found. Please check your configuration.",
        "2.3.0-beta.3534"
      );
    const o = e.state || "Unknown", a = ((h = e.attributes) == null ? void 0 : h.options) || ["None", "Security", "Family", "Strict"], c = this._optimisticProfile || o;
    return b`
      <ha-card .header="${r}">
        <div class="card-content">
          <div class="button-grid">
            ${a.map((u) => {
      const f = c.toLowerCase() === u.toLowerCase(), g = this._isUpdating && this._optimisticProfile === u;
      return b`
                <button
                  class="filter-btn ${f ? "active" : ""} ${this._isUpdating && !g ? "disabled" : ""}"
                  ?disabled=${this._isUpdating}
                  @click=${() => this._setFilterProfile(u, t)}
                >
                  ${g ? b`<ha-circular-progress active size="small"></ha-circular-progress> Saving...` : u}
                </button>
              `;
    })}
          </div>
        </div>
        <div class="version">v${"2.3.0-beta.3534"}</div>
      </ha-card>
    `;
  }
  async _setFilterProfile(t, e) {
    if (!(!this.hass || !e || !t || this._isUpdating)) {
      this._isUpdating = !0, this._optimisticProfile = t;
      try {
        await this.hass.callService("select", "select_option", {
          entity_id: e,
          option: t
        }), setTimeout(() => {
          this._optimisticProfile = null, this._isUpdating = !1;
        }, 8e3);
      } catch (i) {
        console.error("Failed to call select_option service:", i), this._optimisticProfile = null, this._isUpdating = !1;
      }
    }
  }
};
de.styles = [
  At,
  D`
      :host { display: block; }
      ha-card {
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }
      .card-content { padding: 16px; }
      .button-grid {
        display: flex;
        flex-direction: column;
        gap: 8px;
      }
      
      .filter-btn {
        width: 100%;
        padding: 12px;
        background: transparent;
        color: var(--primary-text-color, #ffffff);
        border: 1px solid var(--divider-color, #444444);
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.2s ease;
        font-family: inherit;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
      }
      .filter-btn:hover:not(:disabled) {
        background: var(--secondary-background-color, rgba(255,255,255,0.05));
      }
      .filter-btn.active {
        background: var(--success-color, #4caf50);
        color: #ffffff;
        border-color: var(--success-color, #4caf50);
        font-weight: bold;
      }
      .filter-btn.disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }
      
      /* Style the circular progress to match the text color */
      ha-circular-progress {
        --mdc-theme-primary: currentColor;
      }
    `
];
let H = de;
W([
  L({ attribute: !1 })
], H.prototype, "hass");
W([
  y()
], H.prototype, "_config");
W([
  y()
], H.prototype, "_optimisticProfile");
W([
  y()
], H.prototype, "_isUpdating");
W([
  y()
], H.prototype, "_isLoading");
W([
  y()
], H.prototype, "_loadingMessage");
const he = class he extends P {
  constructor() {
    super(...arguments), this._schema = [
      {
        name: "entity",
        selector: { entity: { domain: "select" } }
      },
      {
        name: "name",
        selector: { text: {} }
      }
    ], this._computeLabel = (t) => t.name === "entity" ? "Entity (Optional)" : t.name === "name" ? "Display Name (Optional)" : t.name;
  }
  setConfig(t) {
    this._config = t;
  }
  render() {
    return !this.hass || !this._config ? b`` : b`
      <div class="editor-container">
        <ha-form
          .hass=${this.hass}
          .data=${this._config}
          .schema=${this._schema}
          .computeLabel=${this._computeLabel}
          @value-changed=${this._valueChanged}
        ></ha-form>
      </div>
    `;
  }
  _valueChanged(t) {
    if (!this._config) return;
    const e = { ...this._config, ...t.detail.value };
    this.dispatchEvent(new CustomEvent("config-changed", {
      detail: { config: e },
      bubbles: !0,
      composed: !0
    }));
  }
};
he.styles = D`
    .editor-container { padding: 16px; }
  `;
let wt = he;
W([
  L({ attribute: !1 })
], wt.prototype, "hass");
W([
  y()
], wt.prototype, "_config");
customElements.get("meraki-content-filter-card") || customElements.define("meraki-content-filter-card", H);
customElements.get("meraki-content-filter-card-editor") || customElements.define("meraki-content-filter-card-editor", wt);
window.customCards = window.customCards || [];
window.customCards.some((n) => n.type === "meraki-content-filter-card") || window.customCards.push({
  type: "meraki-content-filter-card",
  name: "Cisco Meraki Content Filter",
  description: "Control Cisco Meraki Content Filtering profiles.",
  preview: !0
});
var gi = Object.defineProperty, T = (n, t, e, i) => {
  for (var s = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = o(t, e, s) || s);
  return s && gi(t, e, s), s;
};
const ue = class ue extends P {
  constructor() {
    super(...arguments), this._networks = [], this._ssids = [], this._isLoading = !0, this._loadingMessage = "Connecting...", this._computeLabel = (t) => t.name === "networkId" ? "Network (Optional filter)" : t.name === "ssid" ? "SSID (Required)" : t.name === "password" ? "Password (Optional override or Entity ID)" : t.name === "name" ? "Card Title (Optional)" : t.name;
  }
  setConfig(t) {
    this._config = t;
  }
  firstUpdated(t) {
    super.firstUpdated(t), this._loadCentralizedData();
  }
  async _loadCentralizedData() {
    if (!this.hass) return;
    const { networks: t, ssids: e } = await R.pollConfig(
      this.hass,
      (i, s) => {
        this._loadingMessage = i, this._isLoading = s;
      }
    );
    this._networks = t, this._ssids = e;
  }
  _valueChanged(t) {
    if (!this._config) return;
    const e = t.detail.value, i = { ...this._config, ...e };
    this._config.networkId !== e.networkId && (i.ssid = ""), Object.keys(i).forEach((s) => {
      i[s] === "" && delete i[s];
    }), this.dispatchEvent(new CustomEvent("config-changed", { detail: { config: i }, bubbles: !0, composed: !0 }));
  }
  render() {
    if (!this.hass || !this._config) return b``;
    if (this._isLoading)
      return b`
        <div class="editor-container">
          <ha-circular-progress active></ha-circular-progress>
          <div style="margin-top: 16px; color: var(--secondary-text-color);">
            ${this._loadingMessage}
          </div>
        </div>
      `;
    const t = R.getNetworkOptions(this._networks, !0), e = R.getSsidOptions(this._ssids, this._config.networkId, "name"), i = [
      { name: "networkId", selector: { select: { options: t, mode: "dropdown" } } },
      { name: "ssid", selector: { select: { options: e, custom_value: !0, mode: "dropdown" } } },
      { name: "password", selector: { text: {} } },
      { name: "name", selector: { text: {} } }
    ];
    return b`
      <div class="editor-container">
        <ha-form
          .hass=${this.hass}
          .data=${this._config}
          .schema=${i}
          .computeLabel=${this._computeLabel}
          @value-changed=${this._valueChanged}
        ></ha-form>
      </div>
    `;
  }
};
ue.styles = D`.editor-container { padding: 16px; }`;
let z = ue;
T([
  L({ attribute: !1 })
], z.prototype, "hass");
T([
  y()
], z.prototype, "_config");
T([
  y()
], z.prototype, "_networks");
T([
  y()
], z.prototype, "_ssids");
T([
  y()
], z.prototype, "_isLoading");
T([
  y()
], z.prototype, "_loadingMessage");
const fe = class fe extends P {
  constructor() {
    super(...arguments), this._qrSvg = "", this._isLoading = !0, this._loadingMessage = "Connecting...", this._ssids = [];
  }
  static async getConfigElement() {
    return document.createElement("meraki-wifi-qr-card-editor");
  }
  setConfig(t) {
    if (!t || !t.ssid)
      throw new Error("Please select an SSID");
    this._config = t;
  }
  static getStubConfig() {
    return {
      ssid: "",
      name: "Wi-Fi Access"
    };
  }
  firstUpdated(t) {
    super.firstUpdated(t), this._loadCentralizedData();
  }
  async _loadCentralizedData() {
    if (!this.hass) return;
    const { ssids: t } = await R.pollConfig(
      this.hass,
      (e, i) => {
        this._loadingMessage = e, this._isLoading = i;
      }
    );
    this._ssids = t, this._generateQR();
  }
  updated(t) {
    (t.has("hass") || t.has("_config")) && this._generateQR();
  }
  async _generateQR() {
    if (!this._config) return;
    const t = M.getValue(this.hass, this._config.ssid), e = M.getPasswordForSsid(
      this.hass,
      this._ssids,
      t,
      this._config.networkId,
      this._config.password
    );
    if (!t) {
      this._qrSvg = "";
      return;
    }
    const i = M.generateWifiQrString(t, e);
    this._qrSvg = await M.generateQrSvg(i, 2);
  }
  render() {
    var i;
    if (!this._config || !this.hass) return b``;
    if (this._isLoading)
      return $t(
        ((i = this._config) == null ? void 0 : i.name) || "Wi-Fi Access",
        this._loadingMessage,
        "2.3.0-beta.3534"
      );
    const t = M.getValue(this.hass, this._config.ssid), e = M.getPasswordForSsid(
      this.hass,
      this._ssids,
      t,
      this._config.networkId,
      this._config.password
    );
    return b`
      <ha-card .header=${this._config.name || "Wi-Fi Access"}>
        <div class="card-content flex-col-center">
          <div class="ssid-display">${t}</div>
          <div class="qr-container" style="width: 200px; height: 200px;" .innerHTML=${this._qrSvg}></div>
          ${e ? b`<div class="password-display">Password: <code class="copyable-code">${e}</code></div>` : ""}
        </div>
        <div class="version">v${"2.3.0-beta.3534"}</div>
      </ha-card>
    `;
  }
};
fe.styles = [
  At,
  D`
      :host { display: block; }
      .card-content { padding: 16px; gap: 16px; }
      .ssid-display { font-size: 1.5em; font-weight: bold; color: var(--primary-text-color); text-align: center; }
      .password-display { color: var(--secondary-text-color); text-align: center; }
    `
];
let F = fe;
T([
  L({ attribute: !1 })
], F.prototype, "hass");
T([
  y()
], F.prototype, "_config");
T([
  y()
], F.prototype, "_qrSvg");
T([
  y()
], F.prototype, "_isLoading");
T([
  y()
], F.prototype, "_loadingMessage");
T([
  y()
], F.prototype, "_ssids");
customElements.get("meraki-wifi-qr-card") || customElements.define("meraki-wifi-qr-card", F);
customElements.get("meraki-wifi-qr-card-editor") || customElements.define("meraki-wifi-qr-card-editor", z);
window.customCards = window.customCards || [];
window.customCards.some((n) => n.type === "meraki-wifi-qr-card") || window.customCards.push({
  type: "meraki-wifi-qr-card",
  name: "Cisco Meraki Wi-Fi QR Card",
  description: "Display a scannable Wi-Fi QR code for guests.",
  preview: !0
});
var pi = Object.defineProperty, ct = (n, t, e, i) => {
  for (var s = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = o(t, e, s) || s);
  return s && pi(t, e, s), s;
};
const ge = class ge extends P {
  constructor() {
    super(...arguments), this._isLoading = !0, this._loadingMessage = "Connecting...";
  }
  static async getConfigElement() {
    return document.createElement("meraki-network-vitals-card-editor");
  }
  setConfig(t) {
    if (!t)
      throw new Error("Invalid configuration");
    this._config = {
      ...t,
      gateway_tap_action: t.gateway_tap_action || { action: "more-info" },
      switch_tap_action: t.switch_tap_action || { action: "more-info" },
      ap_tap_action: t.ap_tap_action || { action: "more-info" }
    };
  }
  firstUpdated(t) {
    super.firstUpdated(t), this._loadCentralizedData();
  }
  async _loadCentralizedData() {
    this.hass && await R.pollConfig(
      this.hass,
      (t, e) => {
        this._loadingMessage = t, this._isLoading = e;
      }
    );
  }
  static getStubConfig() {
    return {
      gateway_entity: "",
      switch_entity: "",
      ap_entity: "",
      throughput_entity: "sensor.speedtest_download",
      name: "Cisco Meraki Network Vitals",
      gateway_tap_action: { action: "more-info" },
      switch_tap_action: { action: "more-info" },
      ap_tap_action: { action: "more-info" }
    };
  }
  _handleEntityClick(t, e) {
    if (!(!t || !e))
      if (e.action === "navigate" && e.navigation_path) {
        const i = new CustomEvent("navigate", {
          detail: { path: e.navigation_path },
          bubbles: !0,
          composed: !0
        });
        this.dispatchEvent(i);
      } else {
        const i = new CustomEvent("hass-more-info", {
          detail: { entityId: t },
          bubbles: !0,
          composed: !0
        });
        this.dispatchEvent(i);
      }
  }
  _renderStatusDot(t, e, i) {
    const s = !!t && !!this.hass.states[t];
    if (!t || !this.hass.states[t])
      return b`
        <div class="status-item">
          <svg height="12" width="12">
            <circle cx="6" cy="6" r="6" fill="var(--disabled-text-color)" />
          </svg>
          <span class="status-label">${e}</span>
        </div>
      `;
    const r = this.hass.states[t];
    console.log(
      `MERAKI CARD DIAGNOSTIC - Status Dot (${e}) Raw Entity State:`,
      r
    );
    const o = r ? r.state.toLowerCase() : "unknown";
    let a = "var(--disabled-text-color)";
    return o === "ok" || o === "online" || o === "connected" ? a = "var(--success-color)" : o === "warning" ? a = "var(--warning-color)" : (o === "error" || o === "offline" || o === "failed") && (a = "var(--error-color)"), b`
      <div
        class="status-item ${s ? "clickable" : ""}"
        @click="${() => s ? this._handleEntityClick(t, i) : null}"
        role="${s ? "button" : "presentation"}"
        tabindex="${s ? "0" : "-1"}"
      >
        <ha-state-icon
          .hass=${this.hass}
          .stateObj=${r}
          class="status-icon"
        ></ha-state-icon>
        <svg height="12" width="12">
          <circle cx="6" cy="6" r="6" fill="${a}" />
        </svg>
        <span class="status-label">${e}</span>
      </div>
    `;
  }
  render() {
    var s, r;
    if (!this._config || !this.hass)
      return b``;
    if (this._isLoading)
      return $t(
        ((s = this._config) == null ? void 0 : s.name) || "Cisco Meraki Network Vitals",
        this._loadingMessage,
        "2.3.0-beta.3534"
      );
    const t = this._config.throughput_entity;
    t && this.hass.states[t] && console.log(
      "MERAKI CARD DIAGNOSTIC - Throughput Raw Entity State:",
      this.hass.states[t]
    );
    const e = t ? this.hass.states[t] : void 0, i = e ? (e.state || "0") + " " + (((r = e.attributes) == null ? void 0 : r.unit_of_measurement) || "") : "N/A";
    return b`
      <ha-card>
        <div class="card-content">
          <div class="vitals-container">
            <div class="status-dots">
              ${this._renderStatusDot(
      this._config.gateway_entity,
      "Gateway",
      this._config.gateway_tap_action
    )}
              ${this._renderStatusDot(
      this._config.switch_entity,
      "Switches",
      this._config.switch_tap_action
    )}
              ${this._renderStatusDot(
      this._config.ap_entity,
      "APs",
      this._config.ap_tap_action
    )}
            </div>
            <div class="throughput-container">
              <ha-icon icon="mdi:swap-vertical"></ha-icon>
              <span class="throughput-value">${i}</span>
            </div>
          </div>
        </div>
        <div class="version">v${"2.3.0-beta.3534"}</div>
      </ha-card>
    `;
  }
};
ge.styles = [
  At,
  D`
      :host {
        display: block;
      }
      ha-card {
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
      }
      .card-content {
        padding: 12px 16px;
      }
      .vitals-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
      }
      .status-dots {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
      }
      .status-item {
        display: flex;
        align-items: center;
        gap: 8px;
      }
      .status-item.clickable {
        cursor: pointer;
      }
      .status-icon {
        --mdc-icon-size: 16px;
        color: var(--secondary-text-color);
      }
      .status-label {
        font-size: 14px;
        font-weight: 500;
        color: var(--primary-text-color);
        white-space: nowrap;
      }
      .throughput-container {
        display: flex;
        align-items: center;
        gap: 4px;
        color: var(--secondary-text-color);
      }
      .throughput-value {
        font-size: 14px;
        font-weight: 600;
        white-space: nowrap;
      }
    `
];
let X = ge;
ct([
  L({ attribute: !1 })
], X.prototype, "hass");
ct([
  y()
], X.prototype, "_config");
ct([
  y()
], X.prototype, "_isLoading");
ct([
  y()
], X.prototype, "_loadingMessage");
const pe = class pe extends P {
  setConfig(t) {
    this._config = t;
  }
  render() {
    var t, e, i;
    return !this.hass || !this._config ? b`` : b`
      <div class="card-config">
        <ha-textfield
          label="Custom Title"
          .value=${this._config.name || ""}
          .configValue=${"name"}
          @input=${this._valueChanged}
        ></ha-textfield>
        <ha-entity-picker
          label="Gateway Status"
          .hass=${this.hass}
          .value=${this._config.gateway_entity}
          .configValue=${"gateway_entity"}
          @value-changed=${this._valueChanged}
        ></ha-entity-picker>
        <ha-entity-picker
          label="Switch Aggregation"
          .hass=${this.hass}
          .value=${this._config.switch_entity}
          .configValue=${"switch_entity"}
          @value-changed=${this._valueChanged}
        ></ha-entity-picker>
        <ha-entity-picker
          label="AP Aggregation"
          .hass=${this.hass}
          .value=${this._config.ap_entity}
          .configValue=${"ap_entity"}
          @value-changed=${this._valueChanged}
        ></ha-entity-picker>
        <ha-entity-picker
          label="Throughput Sensor"
          .hass=${this.hass}
          .value=${this._config.throughput_entity}
          .configValue=${"throughput_entity"}
          @value-changed=${this._valueChanged}
        ></ha-entity-picker>
        <ha-textfield
          label="Gateway Tap Action"
          .value=${((t = this._config.gateway_tap_action) == null ? void 0 : t.action) || "more-info"}
          .configValue=${"gateway_tap_action"}
          @input=${this._valueChanged}
        ></ha-textfield>
        <ha-textfield
          label="Switch Tap Action"
          .value=${((e = this._config.switch_tap_action) == null ? void 0 : e.action) || "more-info"}
          .configValue=${"switch_tap_action"}
          @input=${this._valueChanged}
        ></ha-textfield>
        <ha-textfield
          label="AP Tap Action"
          .value=${((i = this._config.ap_tap_action) == null ? void 0 : i.action) || "more-info"}
          .configValue=${"ap_tap_action"}
          @input=${this._valueChanged}
        ></ha-textfield>
      </div>
    `;
  }
  _valueChanged(t) {
    var o;
    if (!this._config) return;
    const e = t.target, i = e.configValue;
    let s = ((o = t.detail) == null ? void 0 : o.value) ?? e.value;
    i && i.endsWith("_tap_action") && (s.startsWith("/") ? s = { action: "navigate", navigation_path: s } : s = { action: s });
    const r = { ...this._config, [i]: s };
    this.dispatchEvent(
      new CustomEvent("config-changed", {
        detail: { config: r },
        bubbles: !0,
        composed: !0
      })
    );
  }
};
pe.styles = D`
    ha-textfield,
    ha-entity-picker {
      display: block;
      margin-bottom: 16px;
      width: 100%;
    }
  `;
let vt = pe;
ct([
  L({ attribute: !1 })
], vt.prototype, "hass");
ct([
  y()
], vt.prototype, "_config");
customElements.get("meraki-network-vitals-card") || customElements.define("meraki-network-vitals-card", X);
customElements.get("meraki-network-vitals-card-editor") || customElements.define(
  "meraki-network-vitals-card-editor",
  vt
);
window.customCards = window.customCards || [];
window.customCards.some(
  (n) => n.type === "meraki-network-vitals-card"
) || window.customCards.push({
  type: "meraki-network-vitals-card",
  name: "Cisco Meraki Network Vitals",
  description: "Compact horizontal health header.",
  preview: !0
});
var mi = Object.defineProperty, lt = (n, t, e, i) => {
  for (var s = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = o(t, e, s) || s);
  return s && mi(t, e, s), s;
};
const me = class me extends P {
  constructor() {
    super(...arguments), this._isLoading = !0, this._loadingMessage = "Connecting...";
  }
  static async getConfigElement() {
    return document.createElement("meraki-vlan-card-editor");
  }
  setConfig(t) {
    if (!t)
      throw new Error("Invalid configuration");
    this._config = { ...t };
  }
  firstUpdated(t) {
    super.firstUpdated(t), this._loadCentralizedData();
  }
  async _loadCentralizedData() {
    this.hass && await R.pollConfig(
      this.hass,
      (t, e) => {
        this._loadingMessage = t, this._isLoading = e;
      }
    );
  }
  static getStubConfig() {
    return {
      name: "Meraki VLANs"
    };
  }
  _getVlanEntities() {
    return this.hass ? Object.keys(this.hass.states).filter((t) => {
      if (!t.startsWith("switch.")) return !1;
      const e = this.hass.states[t];
      return e.attributes.vlan_id !== void 0 && e.attributes.subnet !== void 0;
    }).map((t) => {
      var i;
      const e = this.hass.states[t];
      return {
        entity_id: t,
        name: e.attributes.vlan_name || ((i = e.attributes.friendly_name) == null ? void 0 : i.replace(" DHCP", "")) || "Unknown VLAN",
        subnet: e.attributes.subnet,
        gateway: e.attributes.gateway,
        state: e.state
      };
    }).sort((t, e) => t.name.localeCompare(e.name)) : [];
  }
  render() {
    var e;
    if (!this.hass || !this._config) return b``;
    if (this._isLoading)
      return $t(
        ((e = this._config) == null ? void 0 : e.name) || "Cisco Meraki VLANs",
        this._loadingMessage,
        "2.3.0-beta.3534"
      );
    const t = this._getVlanEntities();
    return t.length === 0 ? ne(
      "No VLANs Found",
      "No Meraki VLAN DHCP switches were found. Ensure VLAN management is enabled in the integration options.",
      "2.3.0-beta.3534"
    ) : b`
      <ha-card .header="${this._config.name || "Cisco Meraki VLANs"}">
        <div class="card-content">
          <div class="vlan-table">
            <div class="table-header">
              <div class="col-vlan">VLAN</div>
              <div class="col-network">Subnet / Gateway</div>
              <div class="col-dhcp">DHCP</div>
            </div>
            ${t.map((i) => b`
              <div class="table-row">
                <div class="col-vlan">
                  <span class="vlan-name">${i.name}</span>
                </div>
                <div class="col-network">
                  <div class="subnet">${i.subnet}</div>
                  <div class="gateway">${i.gateway}</div>
                </div>
                <div class="col-dhcp">
                  <ha-switch
                    .checked=${i.state === "on"}
                    @change=${() => this._toggleDhcp(i.entity_id)}
                  ></ha-switch>
                </div>
              </div>
            `)}
          </div>
        </div>
        <div class="version">v${"2.3.0-beta.3534"}</div>
      </ha-card>
    `;
  }
  async _toggleDhcp(t) {
    if (this.hass)
      try {
        await this.hass.callService("switch", "toggle", {
          entity_id: t
        });
      } catch (e) {
        console.error("Failed to toggle DHCP switch:", e);
      }
  }
};
me.styles = [
  At,
  D`
      :host { display: block; }
      .card-content { padding: 0 16px 16px 16px; }

      .vlan-table {
        display: flex;
        flex-direction: column;
        width: 100%;
      }

      .table-header {
        display: flex;
        padding: 8px 0;
        border-bottom: 1px solid var(--divider-color);
        font-weight: bold;
        color: var(--secondary-text-color);
        font-size: 12px;
        text-transform: uppercase;
      }

      .table-row {
        display: flex;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid var(--divider-color);
      }

      .table-row:last-child {
        border-bottom: none;
      }

      .col-vlan { flex: 2; display: flex; align-items: center; }
      .col-network { flex: 3; }
      .col-dhcp { flex: 1; display: flex; justify-content: flex-end; }

      .vlan-name {
        font-weight: 500;
        color: var(--primary-text-color);
      }

      .subnet {
        font-size: 14px;
        color: var(--primary-text-color);
      }

      .gateway {
        font-size: 12px;
        color: var(--secondary-text-color);
      }

      ha-switch {
        --switch-checked-button-color: var(--success-color, #4caf50);
        --switch-checked-track-color: var(--success-color, #4caf50);
      }
    `
];
let tt = me;
lt([
  L({ attribute: !1 })
], tt.prototype, "hass");
lt([
  y()
], tt.prototype, "_config");
lt([
  y()
], tt.prototype, "_isLoading");
lt([
  y()
], tt.prototype, "_loadingMessage");
const _e = class _e extends P {
  constructor() {
    super(...arguments), this._schema = [
      {
        name: "name",
        selector: { text: {} }
      }
    ], this._computeLabel = (t) => t.name === "name" ? "Display Name (Optional)" : t.name;
  }
  setConfig(t) {
    this._config = t;
  }
  render() {
    return !this.hass || !this._config ? b`` : b`
      <div class="editor-container">
        <ha-form
          .hass=${this.hass}
          .data=${this._config}
          .schema=${this._schema}
          .computeLabel=${this._computeLabel}
          @value-changed=${this._valueChanged}
        ></ha-form>
      </div>
    `;
  }
  _valueChanged(t) {
    if (!this._config) return;
    const e = { ...this._config, ...t.detail.value };
    this.dispatchEvent(new CustomEvent("config-changed", {
      detail: { config: e },
      bubbles: !0,
      composed: !0
    }));
  }
};
_e.styles = D`
    .editor-container { padding: 16px; }
  `;
let bt = _e;
lt([
  L({ attribute: !1 })
], bt.prototype, "hass");
lt([
  y()
], bt.prototype, "_config");
customElements.get("meraki-vlan-card") || customElements.define("meraki-vlan-card", tt);
customElements.get("meraki-vlan-card-editor") || customElements.define("meraki-vlan-card-editor", bt);
window.customCards = window.customCards || [];
window.customCards.some((n) => n.type === "meraki-vlan-card") || window.customCards.push({
  type: "meraki-vlan-card",
  name: "Cisco Meraki VLAN Card",
  description: "Overview and management of configured VLANs.",
  preview: !0
});
var _i = Object.defineProperty, is = (n, t, e, i) => {
  for (var s = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = o(t, e, s) || s);
  return s && _i(t, e, s), s;
};
const ye = class ye extends P {
  constructor() {
    super(...arguments), this._computeLabel = (t) => t.name === "name" ? "Title (Optional)" : t.name === "config_entry_id" ? "Config Entry ID (Optional override)" : t.name;
  }
  setConfig(t) {
    this._config = t;
  }
  render() {
    if (!this.hass || !this._config) return b``;
    const t = [
      { name: "name", selector: { text: {} } },
      { name: "config_entry_id", selector: { text: {} } }
    ];
    return b`
      <div class="editor-container">
        <ha-form
          .hass=${this.hass}
          .data=${this._config}
          .schema=${t}
          .computeLabel=${this._computeLabel}
          @value-changed=${this._valueChanged}
        ></ha-form>
      </div>
    `;
  }
  _valueChanged(t) {
    if (!this._config) return;
    const e = { ...this._config, ...t.detail.value };
    this.dispatchEvent(new CustomEvent("config-changed", {
      detail: { config: e },
      bubbles: !0,
      composed: !0
    }));
  }
};
ye.styles = D`
    .editor-container { padding: 16px; }
  `;
let Et = ye;
is([
  L({ attribute: !1 })
], Et.prototype, "hass");
is([
  y()
], Et.prototype, "_config");
customElements.get("meraki-guest-access-card-editor") || customElements.define("meraki-guest-access-card-editor", Et);
var yi = Object.defineProperty, x = (n, t, e, i) => {
  for (var s = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = o(t, e, s) || s);
  return s && yi(t, e, s), s;
};
const we = class we extends P {
  constructor() {
    super(...arguments), this._formData = {
      network: "",
      ssid: "",
      passphrase: "",
      policy: "",
      duration: "60",
      guestName: ""
    }, this._networks = [], this._ssids = [], this._policies = [], this._creating = !1, this._error = null, this._success = null, this._qrSvg = "", this._isLoading = !0, this._loadingMessage = "Connecting to Meraki...", this._configEntryId = null, this._computeLabel = (t) => t.name === "network" ? "Network" : t.name === "ssid" ? "SSID" : t.name === "policy" ? "Group Policy (Required)" : t.name === "passphrase" ? "Passphrase / PSK (Auto-discovered)" : t.name === "duration" ? "Duration" : t.name === "guestName" ? "Guest Name" : t.name;
  }
  static async getConfigElement() {
    return document.createElement("meraki-guest-access-card-editor");
  }
  setConfig(t) {
    if (!t) throw new Error("Invalid configuration");
    this._config = t;
  }
  firstUpdated(t) {
    super.firstUpdated(t), this._loadCentralizedData();
  }
  updated(t) {
    var e;
    super.updated(t), t.has("hass") && this.hass && ((e = this.hass.user) != null && e.name) && !this._formData.guestName && (this._formData = { ...this._formData, guestName: this._generateUniqueGuestName() });
  }
  _generateUniqueGuestName() {
    var i, s;
    const t = ((s = (i = this.hass) == null ? void 0 : i.user) == null ? void 0 : s.name) || "Home Assistant", e = Math.floor(Math.random() * 1e4).toString().padStart(4, "0");
    return `${t} - Guest ${e}`;
  }
  async _loadCentralizedData() {
    var l;
    if (!this.hass) return;
    const { networks: t, ssids: e, groupPolicies: i, entryId: s } = await R.pollConfig(this.hass, (d, h) => {
      this._loadingMessage = d, this._isLoading = h;
    });
    if (t.length === 0) {
      this._isLoading = !1;
      return;
    }
    this._networks = t, this._ssids = e, this._policies = i, this._configEntryId = ((l = this._config) == null ? void 0 : l.config_entry_id) || s;
    let r = this._formData.network, o = this._formData.ssid, a = this._formData.passphrase, c = this._formData.policy;
    if (t.length > 0 && !r && (r = t[0].id), r && !o) {
      const d = e.filter((h) => h.networkId === r);
      d.length > 0 && (o = String(d[0].number));
    }
    if (r && o && !a && (a = M.getPasswordForSsid(this.hass, this._ssids, o, r), a || (a = M.generateNaturalPassword())), r && !c) {
      const d = this._policies.filter(
        (h) => h.networkId === r
      );
      d.length > 0 && (c = String(
        d[0].groupPolicyId || d[0].id
      ));
    }
    this._formData = {
      ...this._formData,
      network: r,
      ssid: o,
      passphrase: a,
      policy: c
    }, this._isLoading = !1;
  }
  _formValueChanged(t) {
    const e = t.detail.value, i = this._formData.network;
    let s = { ...this._formData, ...e };
    if (s.network !== i) {
      s.ssid = "", s.passphrase = "", s.policy = "";
      const r = this._ssids.filter(
        (a) => a.networkId === s.network
      );
      r.length > 0 && (s.ssid = String(r[0].number));
      const o = this._policies.filter(
        (a) => a.networkId === s.network
      );
      o.length > 0 && (s.policy = String(
        o[0].groupPolicyId || o[0].id
      ));
    }
    !s.passphrase && s.network && s.ssid && (s.passphrase = M.getPasswordForSsid(
      this.hass,
      this._ssids,
      s.ssid,
      s.network
    ) || M.generateNaturalPassword()), this._formData = s;
  }
  render() {
    var o, a, c;
    if (this._isLoading)
      return $t(
        ((o = this._config) == null ? void 0 : o.name) || "Cisco Meraki Guest Access",
        this._loadingMessage,
        "2.3.0-beta.3534"
      );
    if (this._networks.length === 0)
      return ne(
        "No Wireless Networks",
        "No Cisco Meraki wireless networks found. Ensure the integration is configured.",
        "2.3.0-beta.3534"
      );
    const t = R.getNetworkOptions(
      this._networks
    ), e = R.getSsidOptions(
      this._ssids,
      this._formData.network,
      "number"
    ), i = this._policies.filter((l) => l.networkId === this._formData.network).map((l) => ({
      value: String(l.groupPolicyId || l.id),
      label: l.name
    })), s = [
      {
        name: "network",
        selector: { select: { options: t, mode: "dropdown" } }
      },
      {
        name: "ssid",
        selector: { select: { options: e, mode: "dropdown" } }
      },
      ...i.length > 0 ? [
        {
          name: "policy",
          selector: {
            select: { options: i, mode: "dropdown" }
          }
        }
      ] : [],
      { name: "passphrase", selector: { text: {} } },
      {
        name: "duration",
        selector: {
          select: {
            options: [
              { value: "15", label: "15 Minutes" },
              { value: "30", label: "30 Minutes" },
              { value: "60", label: "1 Hour" },
              { value: "120", label: "2 Hours" },
              { value: "240", label: "4 Hours" },
              { value: "480", label: "8 Hours" },
              { value: "720", label: "12 Hours" },
              { value: "1440", label: "24 Hours" },
              { value: "2880", label: "48 Hours" },
              { value: "10080", label: "7 Days" }
            ],
            mode: "dropdown"
          }
        }
      },
      { name: "guestName", selector: { text: {} } }
    ], r = this._formData.network && this._formData.ssid && this._formData.policy;
    if (this._success && this._qrSvg) {
      const l = this._networks.find(
        (u) => u.id === this._formData.network
      ), d = parseInt(this._formData.ssid, 10), h = this._ssids.find(
        (u) => u.networkId === this._formData.network && u.number === d
      );
      return b`
        <ha-card .header="${((a = this._config) == null ? void 0 : a.name) || "Share Access"}">
          <div class="card-content success-ui">
            <ha-alert alert-type="success">${this._success}</ha-alert>

            <div class="qr-container" style="width: 200px; height: 200px;" .innerHTML="${this._qrSvg}"></div>

            <div class="credentials-block">
              <div class="credential-item">
                <span class="label">Network:</span>
                <span class="value"
                  >${(l == null ? void 0 : l.name) || "Unknown"}</span
                >
              </div>
              <div class="credential-item">
                <span class="label">SSID:</span>
                <span class="value">${(h == null ? void 0 : h.name) || "Unknown"}</span>
              </div>
              <div class="credential-item">
                <span class="label">Password:</span>
                <code class="copyable-code">${this._formData.passphrase}</code>
              </div>
            </div>

            <ha-button raised @click=${this._resetForm}>
              Create Another
            </ha-button>
          </div>
          <div class="version">v${"2.3.0-beta.3534"}</div>
        </ha-card>
      `;
    }
    return b`
      <ha-card .header="${((c = this._config) == null ? void 0 : c.name) || "Cisco Meraki Guest Access"}">
        <div class="card-content">
          ${this._error ? b`<ha-alert
                alert-type="error"
                dismissable
                @alert-dismissed-clicked="${() => this._error = null}"
                >${this._error}</ha-alert
              >` : ""}

          <div class="form-container">
            <ha-form
              .hass=${this.hass}
              .data=${this._formData}
              .schema=${s}
              .computeLabel=${this._computeLabel}
              @value-changed=${this._formValueChanged}
            ></ha-form>

            <ha-button
              raised
              .disabled=${this._creating || !r}
              @click=${this._generateAccessKey}
            >
              ${this._creating ? b`<ha-circular-progress
                    active
                    size="small"
                  ></ha-circular-progress>` : "Generate Access Key"}
            </ha-button>
          </div>
        </div>
        <div class="version">v${"2.3.0-beta.3534"}</div>
      </ha-card>
    `;
  }
  _resetForm() {
    this._success = null, this._error = null, this._qrSvg = "", this._formData = {
      ...this._formData,
      guestName: this._generateUniqueGuestName(),
      passphrase: ""
    }, this._loadCentralizedData();
  }
  async _generateAccessKey() {
    if (!(!this._formData.network || !this._formData.ssid || !this._formData.policy)) {
      this._creating = !0, this._error = null, this._success = null, this._qrSvg = "";
      try {
        const t = {
          network_id: this._formData.network,
          ssid: parseInt(this._formData.ssid, 10),
          duration: parseInt(this._formData.duration, 10)
        };
        this._formData.policy && this._formData.policy !== "NONE" && this._formData.policy !== "CREATE" && (t.group_policy = this._formData.policy), this._formData.guestName && (t.guest_name = this._formData.guestName), this._formData.passphrase && (t.passphrase = this._formData.passphrase), await this.hass.callService(
          "meraki_ha",
          "generate_guest_access",
          t
        );
        const e = parseInt(this._formData.ssid, 10), i = this._ssids.find(
          (a) => a.networkId === this._formData.network && a.number === e
        ), s = i ? i.name : "Guest WiFi", r = this._formData.passphrase, o = M.generateWifiQrString(s, r);
        this._qrSvg = await M.generateQrSvg(o), this._success = "Guest access key created successfully!";
      } catch (t) {
        this._error = `Failed to create guest key: ${t.message || t}`;
      } finally {
        this._creating = !1;
      }
    }
  }
};
we.styles = [
  At,
  D`
      .form-container {
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
      ha-button {
        width: 100%;
        margin-top: 8px;
      }
      .success-ui {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 16px;
        padding-bottom: 16px;
      }
      .credentials-block {
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 8px;
        background: var(--secondary-background-color);
        padding: 16px;
        border-radius: 8px;
      }
      .credential-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .credential-item .label {
        font-weight: bold;
        color: var(--secondary-text-color);
      }
      ha-alert {
        width: 100%;
      }
    `
];
let S = we;
x([
  L({ attribute: !1 })
], S.prototype, "hass");
x([
  y()
], S.prototype, "_config");
x([
  y()
], S.prototype, "_formData");
x([
  y()
], S.prototype, "_networks");
x([
  y()
], S.prototype, "_ssids");
x([
  y()
], S.prototype, "_policies");
x([
  y()
], S.prototype, "_creating");
x([
  y()
], S.prototype, "_error");
x([
  y()
], S.prototype, "_success");
x([
  y()
], S.prototype, "_qrSvg");
x([
  y()
], S.prototype, "_isLoading");
x([
  y()
], S.prototype, "_loadingMessage");
x([
  y()
], S.prototype, "_configEntryId");
customElements.get("meraki-guest-access-card") || customElements.define("meraki-guest-access-card", S);
window.customCards = window.customCards || [];
window.customCards.some(
  (n) => n.type === "meraki-guest-access-card"
) || window.customCards.push({
  type: "meraki-guest-access-card",
  name: "Cisco Meraki Guest Access",
  description: "Manage temporary guest WiFi access. Version: 2.3.0-beta.3534",
  preview: !0,
  version: "2.3.0-beta.3534"
});
export {
  S as MerakiGuestAccessCard
};
