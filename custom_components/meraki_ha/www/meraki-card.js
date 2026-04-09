/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const xt = globalThis, te = xt.ShadowRoot && (xt.ShadyCSS === void 0 || xt.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, ee = Symbol(), ve = /* @__PURE__ */ new WeakMap();
let Le = class {
  constructor(t, e, s) {
    if (this._$cssResult$ = !0, s !== ee) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = t, this.t = e;
  }
  get styleSheet() {
    let t = this.o;
    const e = this.t;
    if (te && t === void 0) {
      const s = e !== void 0 && e.length === 1;
      s && (t = ve.get(e)), t === void 0 && ((this.o = t = new CSSStyleSheet()).replaceSync(this.cssText), s && ve.set(e, t));
    }
    return t;
  }
  toString() {
    return this.cssText;
  }
};
const ni = (n) => new Le(typeof n == "string" ? n : n + "", void 0, ee), D = (n, ...t) => {
  const e = n.length === 1 ? n[0] : t.reduce((s, i, r) => s + ((o) => {
    if (o._$cssResult$ === !0) return o.cssText;
    if (typeof o == "number") return o;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + o + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(i) + n[r + 1], n[0]);
  return new Le(e, n, ee);
}, ri = (n, t) => {
  if (te) n.adoptedStyleSheets = t.map((e) => e instanceof CSSStyleSheet ? e : e.styleSheet);
  else for (const e of t) {
    const s = document.createElement("style"), i = xt.litNonce;
    i !== void 0 && s.setAttribute("nonce", i), s.textContent = e.cssText, n.appendChild(s);
  }
}, be = te ? (n) => n : (n) => n instanceof CSSStyleSheet ? ((t) => {
  let e = "";
  for (const s of t.cssRules) e += s.cssText;
  return ni(e);
})(n) : n;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: oi, defineProperty: ai, getOwnPropertyDescriptor: ci, getOwnPropertyNames: li, getOwnPropertySymbols: di, getPrototypeOf: hi } = Object, K = globalThis, Ee = K.trustedTypes, ui = Ee ? Ee.emptyScript : "", zt = K.reactiveElementPolyfillSupport, ut = (n, t) => n, It = { toAttribute(n, t) {
  switch (t) {
    case Boolean:
      n = n ? ui : null;
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
} }, ie = (n, t) => !oi(n, t), Ce = { attribute: !0, type: String, converter: It, reflect: !1, useDefault: !1, hasChanged: ie };
Symbol.metadata ?? (Symbol.metadata = Symbol("metadata")), K.litPropertyMetadata ?? (K.litPropertyMetadata = /* @__PURE__ */ new WeakMap());
let et = class extends HTMLElement {
  static addInitializer(t) {
    this._$Ei(), (this.l ?? (this.l = [])).push(t);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(t, e = Ce) {
    if (e.state && (e.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(t) && ((e = Object.create(e)).wrapped = !0), this.elementProperties.set(t, e), !e.noAccessor) {
      const s = Symbol(), i = this.getPropertyDescriptor(t, s, e);
      i !== void 0 && ai(this.prototype, t, i);
    }
  }
  static getPropertyDescriptor(t, e, s) {
    const { get: i, set: r } = ci(this.prototype, t) ?? { get() {
      return this[e];
    }, set(o) {
      this[e] = o;
    } };
    return { get: i, set(o) {
      const a = i == null ? void 0 : i.call(this);
      r == null || r.call(this, o), this.requestUpdate(t, a, s);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(t) {
    return this.elementProperties.get(t) ?? Ce;
  }
  static _$Ei() {
    if (this.hasOwnProperty(ut("elementProperties"))) return;
    const t = hi(this);
    t.finalize(), t.l !== void 0 && (this.l = [...t.l]), this.elementProperties = new Map(t.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(ut("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(ut("properties"))) {
      const e = this.properties, s = [...li(e), ...di(e)];
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
      for (const i of s) e.unshift(be(i));
    } else t !== void 0 && e.push(be(t));
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
    return ri(t, this.constructor.elementStyles), t;
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
      const o = (((r = s.converter) == null ? void 0 : r.toAttribute) !== void 0 ? s.converter : It).toAttribute(e, s.type);
      this._$Em = t, o == null ? this.removeAttribute(i) : this.setAttribute(i, o), this._$Em = null;
    }
  }
  _$AK(t, e) {
    var r, o;
    const s = this.constructor, i = s._$Eh.get(t);
    if (i !== void 0 && this._$Em !== i) {
      const a = s.getPropertyOptions(i), c = typeof a.converter == "function" ? { fromAttribute: a.converter } : ((r = a.converter) == null ? void 0 : r.fromAttribute) !== void 0 ? a.converter : It;
      this._$Em = i;
      const d = c.fromAttribute(e, a.type);
      this[i] = d ?? ((o = this._$Ej) == null ? void 0 : o.get(i)) ?? d, this._$Em = null;
    }
  }
  requestUpdate(t, e, s, i = !1, r) {
    var o;
    if (t !== void 0) {
      const a = this.constructor;
      if (i === !1 && (r = this[t]), s ?? (s = a.getPropertyOptions(t)), !((s.hasChanged ?? ie)(r, e) || s.useDefault && s.reflect && r === ((o = this._$Ej) == null ? void 0 : o.get(t)) && !this.hasAttribute(a._$Eu(t, s)))) return;
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
        const { wrapped: a } = o, c = this[r];
        a !== !0 || this._$AL.has(r) || c === void 0 || this.C(r, void 0, o, c);
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
et.elementStyles = [], et.shadowRootOptions = { mode: "open" }, et[ut("elementProperties")] = /* @__PURE__ */ new Map(), et[ut("finalized")] = /* @__PURE__ */ new Map(), zt == null || zt({ ReactiveElement: et }), (K.reactiveElementVersions ?? (K.reactiveElementVersions = [])).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const ft = globalThis, Ae = (n) => n, Tt = ft.trustedTypes, $e = Tt ? Tt.createPolicy("lit-html", { createHTML: (n) => n }) : void 0, Be = "$lit$", j = `lit$${Math.random().toFixed(9).slice(2)}$`, Re = "?" + j, fi = `<${Re}>`, Z = document, pt = () => Z.createComment(""), mt = (n) => n === null || typeof n != "object" && typeof n != "function", se = Array.isArray, gi = (n) => se(n) || typeof (n == null ? void 0 : n[Symbol.iterator]) == "function", Ft = `[ 	
\f\r]`, ht = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, ke = /-->/g, Se = />/g, J = RegExp(`>|${Ft}(?:([^\\s"'>=/]+)(${Ft}*=${Ft}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`, "g"), Pe = /'/g, Ne = /"/g, Ue = /^(?:script|style|textarea|title)$/i, pi = (n) => (t, ...e) => ({ _$litType$: n, strings: t, values: e }), b = pi(1), it = Symbol.for("lit-noChange"), k = Symbol.for("lit-nothing"), xe = /* @__PURE__ */ new WeakMap(), Y = Z.createTreeWalker(Z, 129);
function Oe(n, t) {
  if (!se(n) || !n.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return $e !== void 0 ? $e.createHTML(t) : t;
}
const mi = (n, t) => {
  const e = n.length - 1, s = [];
  let i, r = t === 2 ? "<svg>" : t === 3 ? "<math>" : "", o = ht;
  for (let a = 0; a < e; a++) {
    const c = n[a];
    let d, l, h = -1, u = 0;
    for (; u < c.length && (o.lastIndex = u, l = o.exec(c), l !== null); ) u = o.lastIndex, o === ht ? l[1] === "!--" ? o = ke : l[1] !== void 0 ? o = Se : l[2] !== void 0 ? (Ue.test(l[2]) && (i = RegExp("</" + l[2], "g")), o = J) : l[3] !== void 0 && (o = J) : o === J ? l[0] === ">" ? (o = i ?? ht, h = -1) : l[1] === void 0 ? h = -2 : (h = o.lastIndex - l[2].length, d = l[1], o = l[3] === void 0 ? J : l[3] === '"' ? Ne : Pe) : o === Ne || o === Pe ? o = J : o === ke || o === Se ? o = ht : (o = J, i = void 0);
    const f = o === J && n[a + 1].startsWith("/>") ? " " : "";
    r += o === ht ? c + fi : h >= 0 ? (s.push(d), c.slice(0, h) + Be + c.slice(h) + j + f) : c + j + (h === -2 ? a : f);
  }
  return [Oe(n, r + (n[e] || "<?>") + (t === 2 ? "</svg>" : t === 3 ? "</math>" : "")), s];
};
class _t {
  constructor({ strings: t, _$litType$: e }, s) {
    let i;
    this.parts = [];
    let r = 0, o = 0;
    const a = t.length - 1, c = this.parts, [d, l] = mi(t, e);
    if (this.el = _t.createElement(d, s), Y.currentNode = this.el.content, e === 2 || e === 3) {
      const h = this.el.content.firstChild;
      h.replaceWith(...h.childNodes);
    }
    for (; (i = Y.nextNode()) !== null && c.length < a; ) {
      if (i.nodeType === 1) {
        if (i.hasAttributes()) for (const h of i.getAttributeNames()) if (h.endsWith(Be)) {
          const u = l[o++], f = i.getAttribute(h).split(j), g = /([.?@])?(.*)/.exec(u);
          c.push({ type: 1, index: r, name: g[2], strings: f, ctor: g[1] === "." ? yi : g[1] === "?" ? wi : g[1] === "@" ? vi : Lt }), i.removeAttribute(h);
        } else h.startsWith(j) && (c.push({ type: 6, index: r }), i.removeAttribute(h));
        if (Ue.test(i.tagName)) {
          const h = i.textContent.split(j), u = h.length - 1;
          if (u > 0) {
            i.textContent = Tt ? Tt.emptyScript : "";
            for (let f = 0; f < u; f++) i.append(h[f], pt()), Y.nextNode(), c.push({ type: 2, index: ++r });
            i.append(h[u], pt());
          }
        }
      } else if (i.nodeType === 8) if (i.data === Re) c.push({ type: 2, index: r });
      else {
        let h = -1;
        for (; (h = i.data.indexOf(j, h + 1)) !== -1; ) c.push({ type: 7, index: r }), h += j.length - 1;
      }
      r++;
    }
  }
  static createElement(t, e) {
    const s = Z.createElement("template");
    return s.innerHTML = t, s;
  }
}
function st(n, t, e = n, s) {
  var o, a;
  if (t === it) return t;
  let i = s !== void 0 ? (o = e._$Co) == null ? void 0 : o[s] : e._$Cl;
  const r = mt(t) ? void 0 : t._$litDirective$;
  return (i == null ? void 0 : i.constructor) !== r && ((a = i == null ? void 0 : i._$AO) == null || a.call(i, !1), r === void 0 ? i = void 0 : (i = new r(n), i._$AT(n, e, s)), s !== void 0 ? (e._$Co ?? (e._$Co = []))[s] = i : e._$Cl = i), i !== void 0 && (t = st(n, i._$AS(n, t.values), i, s)), t;
}
class _i {
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
    const { el: { content: e }, parts: s } = this._$AD, i = ((t == null ? void 0 : t.creationScope) ?? Z).importNode(e, !0);
    Y.currentNode = i;
    let r = Y.nextNode(), o = 0, a = 0, c = s[0];
    for (; c !== void 0; ) {
      if (o === c.index) {
        let d;
        c.type === 2 ? d = new Ct(r, r.nextSibling, this, t) : c.type === 1 ? d = new c.ctor(r, c.name, c.strings, this, t) : c.type === 6 && (d = new bi(r, this, t)), this._$AV.push(d), c = s[++a];
      }
      o !== (c == null ? void 0 : c.index) && (r = Y.nextNode(), o++);
    }
    return Y.currentNode = Z, i;
  }
  p(t) {
    let e = 0;
    for (const s of this._$AV) s !== void 0 && (s.strings !== void 0 ? (s._$AI(t, s, e), e += s.strings.length - 2) : s._$AI(t[e])), e++;
  }
}
class Ct {
  get _$AU() {
    var t;
    return ((t = this._$AM) == null ? void 0 : t._$AU) ?? this._$Cv;
  }
  constructor(t, e, s, i) {
    this.type = 2, this._$AH = k, this._$AN = void 0, this._$AA = t, this._$AB = e, this._$AM = s, this.options = i, this._$Cv = (i == null ? void 0 : i.isConnected) ?? !0;
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
    t = st(this, t, e), mt(t) ? t === k || t == null || t === "" ? (this._$AH !== k && this._$AR(), this._$AH = k) : t !== this._$AH && t !== it && this._(t) : t._$litType$ !== void 0 ? this.$(t) : t.nodeType !== void 0 ? this.T(t) : gi(t) ? this.k(t) : this._(t);
  }
  O(t) {
    return this._$AA.parentNode.insertBefore(t, this._$AB);
  }
  T(t) {
    this._$AH !== t && (this._$AR(), this._$AH = this.O(t));
  }
  _(t) {
    this._$AH !== k && mt(this._$AH) ? this._$AA.nextSibling.data = t : this.T(Z.createTextNode(t)), this._$AH = t;
  }
  $(t) {
    var r;
    const { values: e, _$litType$: s } = t, i = typeof s == "number" ? this._$AC(t) : (s.el === void 0 && (s.el = _t.createElement(Oe(s.h, s.h[0]), this.options)), s);
    if (((r = this._$AH) == null ? void 0 : r._$AD) === i) this._$AH.p(e);
    else {
      const o = new _i(i, this), a = o.u(this.options);
      o.p(e), this.T(a), this._$AH = o;
    }
  }
  _$AC(t) {
    let e = xe.get(t.strings);
    return e === void 0 && xe.set(t.strings, e = new _t(t)), e;
  }
  k(t) {
    se(this._$AH) || (this._$AH = [], this._$AR());
    const e = this._$AH;
    let s, i = 0;
    for (const r of t) i === e.length ? e.push(s = new Ct(this.O(pt()), this.O(pt()), this, this.options)) : s = e[i], s._$AI(r), i++;
    i < e.length && (this._$AR(s && s._$AB.nextSibling, i), e.length = i);
  }
  _$AR(t = this._$AA.nextSibling, e) {
    var s;
    for ((s = this._$AP) == null ? void 0 : s.call(this, !1, !0, e); t !== this._$AB; ) {
      const i = Ae(t).nextSibling;
      Ae(t).remove(), t = i;
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
  constructor(t, e, s, i, r) {
    this.type = 1, this._$AH = k, this._$AN = void 0, this.element = t, this.name = e, this._$AM = i, this.options = r, s.length > 2 || s[0] !== "" || s[1] !== "" ? (this._$AH = Array(s.length - 1).fill(new String()), this.strings = s) : this._$AH = k;
  }
  _$AI(t, e = this, s, i) {
    const r = this.strings;
    let o = !1;
    if (r === void 0) t = st(this, t, e, 0), o = !mt(t) || t !== this._$AH && t !== it, o && (this._$AH = t);
    else {
      const a = t;
      let c, d;
      for (t = r[0], c = 0; c < r.length - 1; c++) d = st(this, a[s + c], e, c), d === it && (d = this._$AH[c]), o || (o = !mt(d) || d !== this._$AH[c]), d === k ? t = k : t !== k && (t += (d ?? "") + r[c + 1]), this._$AH[c] = d;
    }
    o && !i && this.j(t);
  }
  j(t) {
    t === k ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, t ?? "");
  }
}
class yi extends Lt {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(t) {
    this.element[this.name] = t === k ? void 0 : t;
  }
}
class wi extends Lt {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(t) {
    this.element.toggleAttribute(this.name, !!t && t !== k);
  }
}
class vi extends Lt {
  constructor(t, e, s, i, r) {
    super(t, e, s, i, r), this.type = 5;
  }
  _$AI(t, e = this) {
    if ((t = st(this, t, e, 0) ?? k) === it) return;
    const s = this._$AH, i = t === k && s !== k || t.capture !== s.capture || t.once !== s.once || t.passive !== s.passive, r = t !== k && (s === k || i);
    i && this.element.removeEventListener(this.name, this, s), r && this.element.addEventListener(this.name, this, t), this._$AH = t;
  }
  handleEvent(t) {
    var e;
    typeof this._$AH == "function" ? this._$AH.call(((e = this.options) == null ? void 0 : e.host) ?? this.element, t) : this._$AH.handleEvent(t);
  }
}
class bi {
  constructor(t, e, s) {
    this.element = t, this.type = 6, this._$AN = void 0, this._$AM = e, this.options = s;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t) {
    st(this, t);
  }
}
const Vt = ft.litHtmlPolyfillSupport;
Vt == null || Vt(_t, Ct), (ft.litHtmlVersions ?? (ft.litHtmlVersions = [])).push("3.3.2");
const Ei = (n, t, e) => {
  const s = (e == null ? void 0 : e.renderBefore) ?? t;
  let i = s._$litPart$;
  if (i === void 0) {
    const r = (e == null ? void 0 : e.renderBefore) ?? null;
    s._$litPart$ = i = new Ct(t.insertBefore(pt(), r), r, void 0, e ?? {});
  }
  return i._$AI(n), i;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Q = globalThis;
class N extends et {
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
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Do = Ei(e, this.renderRoot, this.renderOptions);
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
    return it;
  }
}
var De;
N._$litElement$ = !0, N.finalized = !0, (De = Q.litElementHydrateSupport) == null || De.call(Q, { LitElement: N });
const jt = Q.litElementPolyfillSupport;
jt == null || jt({ LitElement: N });
(Q.litElementVersions ?? (Q.litElementVersions = [])).push("4.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Ci = { attribute: !0, type: String, converter: It, reflect: !1, hasChanged: ie }, Ai = (n = Ci, t, e) => {
  const { kind: s, metadata: i } = e;
  let r = globalThis.litPropertyMetadata.get(i);
  if (r === void 0 && globalThis.litPropertyMetadata.set(i, r = /* @__PURE__ */ new Map()), s === "setter" && ((n = Object.create(n)).wrapped = !0), r.set(e.name, n), s === "accessor") {
    const { name: o } = e;
    return { set(a) {
      const c = t.get.call(this);
      t.set.call(this, a), this.requestUpdate(o, c, n, !0, a);
    }, init(a) {
      return a !== void 0 && this.C(o, void 0, n, a), a;
    } };
  }
  if (s === "setter") {
    const { name: o } = e;
    return function(a) {
      const c = this[o];
      t.call(this, a), this.requestUpdate(o, c, n, !0, a);
    };
  }
  throw Error("Unsupported decorator location: " + s);
};
function L(n) {
  return (t, e) => typeof e == "object" ? Ai(n, t, e) : ((s, i, r) => {
    const o = i.hasOwnProperty(r);
    return i.constructor.createProperty(r, s), o ? Object.getOwnPropertyDescriptor(i, r) : void 0;
  })(n, t, e);
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function w(n) {
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
`, At = (n, t, e) => b`
  <ha-card class="status-card loading">
    <div class="card-content flex-col align-center p-8">
      <h1 class="status-title">${n}</h1>
      <ha-circular-progress active></ha-circular-progress>
      <div class="status-message mt-4">${t}</div>
    </div>
    <div class="version">v${e}</div>
  </ha-card>
`, $t = D`
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
const $i = async (n, t) => {
  if (!n)
    throw new Error("Home Assistant object is not available.");
  try {
    if (typeof n.callWS == "function")
      return await n.callWS(t);
    if (n.connection && typeof n.connection.sendMessagePromise == "function")
      return await n.connection.sendMessagePromise(t);
    throw new Error(
      "Home Assistant WebSocket communication methods not found."
    );
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
      }), s = e.length > 0 ? e[0].entry_id : null;
      if (!s)
        return { networks: [], ssids: [], groupPolicies: [], entryId: null };
      const i = await $i(t, {
        type: He.GET_CONFIG,
        config_entry_id: s
      }), r = (Array.isArray(i.networks) ? i.networks : []).filter((c) => {
        var d;
        return (d = c.productTypes) == null ? void 0 : d.includes("wireless");
      }), o = Array.isArray(i.ssids) ? i.ssids : [], a = [];
      if (i.group_policies && typeof i.group_policies == "object")
        for (const [c, d] of Object.entries(
          i.group_policies
        ))
          Array.isArray(d) && d.forEach((l) => {
            a.push({
              networkId: c,
              groupPolicyId: String(l.groupPolicyId),
              name: l.name
            });
          });
      return { networks: r, ssids: o, groupPolicies: a, entryId: s };
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
  static async pollConfig(t, e, s = 12, i = 5e3) {
    for (let r = 0; r < s; r++) {
      try {
        const o = await this.fetchConfig(t);
        if (o.networks.length > 0)
          return e("", !1), o;
        e(
          `Waiting for integration to sync... (Attempt ${r + 1}/${s})`,
          !0
        );
      } catch {
        e(
          `Error connecting to backend. Retrying... (Attempt ${r + 1}/${s})`,
          !0
        );
      }
      await new Promise((o) => setTimeout(o, i));
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
    const s = t.map((i) => ({ value: i.id, label: i.name }));
    return e ? [{ value: "", label: "All Networks" }, ...s] : s;
  }
  /**
   * Formats SSIDs for an ha-form dropdown.
   * @param valueType Determines if the dropdown returns the SSID's string name (for QR codes) or integer number (for Guest API calls).
   */
  static getSsidOptions(t, e, s = "name") {
    return (e ? t.filter((r) => r.networkId === e) : t).map((r) => ({
      value: s === "number" ? String(r.number) : r.name,
      label: `${r.name} (SSID ${r.number})`
    }));
  }
  /**
   * Formats Group Policies for an ha-form dropdown.
   */
  static getGroupPolicyOptions(t, e) {
    const i = (e ? t.filter((r) => r.networkId === e) : t).map((r) => ({
      value: r.groupPolicyId,
      label: r.name
    }));
    return [
      { value: "CREATE", label: "Create 'Home Assistant Guest' Policy" },
      { value: "NONE", label: "None (Network Default)" },
      ...i
    ];
  }
}
var kt = {}, ki = function() {
  return typeof Promise == "function" && Promise.prototype && Promise.prototype.then;
}, ze = {}, x = {};
let re;
const Si = [
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
x.getSymbolSize = function(t) {
  if (!t) throw new Error('"version" cannot be null or undefined');
  if (t < 1 || t > 40) throw new Error('"version" should be in range from 1 to 40');
  return t * 4 + 17;
};
x.getSymbolTotalCodewords = function(t) {
  return Si[t];
};
x.getBCHDigit = function(n) {
  let t = 0;
  for (; n !== 0; )
    t++, n >>>= 1;
  return t;
};
x.setToSJISFunction = function(t) {
  if (typeof t != "function")
    throw new Error('"toSJISFunc" is not a valid function.');
  re = t;
};
x.isKanjiModeEnabled = function() {
  return typeof re < "u";
};
x.toSJIS = function(t) {
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
var Pi = Fe;
function St(n) {
  if (!n || n < 1)
    throw new Error("BitMatrix size must be defined and greater than 0");
  this.size = n, this.data = new Uint8Array(n * n), this.reservedBit = new Uint8Array(n * n);
}
St.prototype.set = function(n, t, e, s) {
  const i = n * this.size + t;
  this.data[i] = e, s && (this.reservedBit[i] = !0);
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
var Ni = St, Ve = {};
(function(n) {
  const t = x.getSymbolSize;
  n.getRowColCoords = function(s) {
    if (s === 1) return [];
    const i = Math.floor(s / 7) + 2, r = t(s), o = r === 145 ? 26 : Math.ceil((r - 13) / (2 * i - 2)) * 2, a = [r - 7];
    for (let c = 1; c < i - 1; c++)
      a[c] = a[c - 1] - o;
    return a.push(6), a.reverse();
  }, n.getPositions = function(s) {
    const i = [], r = n.getRowColCoords(s), o = r.length;
    for (let a = 0; a < o; a++)
      for (let c = 0; c < o; c++)
        a === 0 && c === 0 || // top-left
        a === 0 && c === o - 1 || // bottom-left
        a === o - 1 && c === 0 || i.push([r[a], r[c]]);
    return i;
  };
})(Ve);
var je = {};
const xi = x.getSymbolSize, Ie = 7;
je.getPositions = function(t) {
  const e = xi(t);
  return [
    // top-left
    [0, 0],
    // top-right
    [e - Ie, 0],
    // bottom-left
    [0, e - Ie]
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
  n.isValid = function(i) {
    return i != null && i !== "" && !isNaN(i) && i >= 0 && i <= 7;
  }, n.from = function(i) {
    return n.isValid(i) ? parseInt(i, 10) : void 0;
  }, n.getPenaltyN1 = function(i) {
    const r = i.size;
    let o = 0, a = 0, c = 0, d = null, l = null;
    for (let h = 0; h < r; h++) {
      a = c = 0, d = l = null;
      for (let u = 0; u < r; u++) {
        let f = i.get(h, u);
        f === d ? a++ : (a >= 5 && (o += t.N1 + (a - 5)), d = f, a = 1), f = i.get(u, h), f === l ? c++ : (c >= 5 && (o += t.N1 + (c - 5)), l = f, c = 1);
      }
      a >= 5 && (o += t.N1 + (a - 5)), c >= 5 && (o += t.N1 + (c - 5));
    }
    return o;
  }, n.getPenaltyN2 = function(i) {
    const r = i.size;
    let o = 0;
    for (let a = 0; a < r - 1; a++)
      for (let c = 0; c < r - 1; c++) {
        const d = i.get(a, c) + i.get(a, c + 1) + i.get(a + 1, c) + i.get(a + 1, c + 1);
        (d === 4 || d === 0) && o++;
      }
    return o * t.N2;
  }, n.getPenaltyN3 = function(i) {
    const r = i.size;
    let o = 0, a = 0, c = 0;
    for (let d = 0; d < r; d++) {
      a = c = 0;
      for (let l = 0; l < r; l++)
        a = a << 1 & 2047 | i.get(d, l), l >= 10 && (a === 1488 || a === 93) && o++, c = c << 1 & 2047 | i.get(l, d), l >= 10 && (c === 1488 || c === 93) && o++;
    }
    return o * t.N3;
  }, n.getPenaltyN4 = function(i) {
    let r = 0;
    const o = i.data.length;
    for (let c = 0; c < o; c++) r += i.data[c];
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
    for (let a = 0; a < o; a++)
      for (let c = 0; c < o; c++)
        r.isReserved(c, a) || r.xor(c, a, e(i, c, a));
  }, n.getBestMask = function(i, r) {
    const o = Object.keys(n.Patterns).length;
    let a = 0, c = 1 / 0;
    for (let d = 0; d < o; d++) {
      r(d), n.applyMask(d, i);
      const l = n.getPenaltyN1(i) + n.getPenaltyN2(i) + n.getPenaltyN3(i) + n.getPenaltyN4(i);
      n.applyMask(d, i), l < c && (c = l, a = d);
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
var Ke = {}, Ut = {};
const gt = new Uint8Array(512), Mt = new Uint8Array(256);
(function() {
  let t = 1;
  for (let e = 0; e < 255; e++)
    gt[e] = t, Mt[t] = e, t <<= 1, t & 256 && (t ^= 285);
  for (let e = 255; e < 512; e++)
    gt[e] = gt[e - 255];
})();
Ut.log = function(t) {
  if (t < 1) throw new Error("log(" + t + ")");
  return Mt[t];
};
Ut.exp = function(t) {
  return gt[t];
};
Ut.mul = function(t, e) {
  return t === 0 || e === 0 ? 0 : gt[Mt[t] + Mt[e]];
};
(function(n) {
  const t = Ut;
  n.mul = function(s, i) {
    const r = new Uint8Array(s.length + i.length - 1);
    for (let o = 0; o < s.length; o++)
      for (let a = 0; a < i.length; a++)
        r[o + a] ^= t.mul(s[o], i[a]);
    return r;
  }, n.mod = function(s, i) {
    let r = new Uint8Array(s);
    for (; r.length - i.length >= 0; ) {
      const o = r[0];
      for (let c = 0; c < i.length; c++)
        r[c] ^= t.mul(i[c], o);
      let a = 0;
      for (; a < r.length && r[a] === 0; ) a++;
      r = r.slice(a);
    }
    return r;
  }, n.generateECPolynomial = function(s) {
    let i = new Uint8Array([1]);
    for (let r = 0; r < s; r++)
      i = n.mul(i, new Uint8Array([1, t.exp(r)]));
    return i;
  };
})(Ke);
const Ge = Ke;
function oe(n) {
  this.genPoly = void 0, this.degree = n, this.degree && this.initialize(this.degree);
}
oe.prototype.initialize = function(t) {
  this.degree = t, this.genPoly = Ge.generateECPolynomial(this.degree);
};
oe.prototype.encode = function(t) {
  if (!this.genPoly)
    throw new Error("Encoder not initialized");
  const e = new Uint8Array(t.length + this.degree);
  e.set(t);
  const s = Ge.mod(e, this.genPoly), i = this.degree - s.length;
  if (i > 0) {
    const r = new Uint8Array(this.degree);
    return r.set(s, i), r;
  }
  return s;
};
var Ii = oe, We = {}, G = {}, ae = {};
ae.isValid = function(t) {
  return !isNaN(t) && t >= 1 && t <= 40;
};
var U = {};
const Je = "[0-9]+", Ti = "[A-Z $%*+\\-./:]+";
let yt = "(?:[u3000-u303F]|[u3040-u309F]|[u30A0-u30FF]|[uFF00-uFFEF]|[u4E00-u9FAF]|[u2605-u2606]|[u2190-u2195]|u203B|[u2010u2015u2018u2019u2025u2026u201Cu201Du2225u2260]|[u0391-u0451]|[u00A7u00A8u00B1u00B4u00D7u00F7])+";
yt = yt.replace(/u/g, "\\u");
const Mi = "(?:(?![A-Z0-9 $%*+\\-./:]|" + yt + `)(?:.|[\r
]))+`;
U.KANJI = new RegExp(yt, "g");
U.BYTE_KANJI = new RegExp("[^A-Z0-9 $%*+\\-./:]+", "g");
U.BYTE = new RegExp(Mi, "g");
U.NUMERIC = new RegExp(Je, "g");
U.ALPHANUMERIC = new RegExp(Ti, "g");
const Di = new RegExp("^" + yt + "$"), Li = new RegExp("^" + Je + "$"), Bi = new RegExp("^[A-Z0-9 $%*+\\-./:]+$");
U.testKanji = function(t) {
  return Di.test(t);
};
U.testNumeric = function(t) {
  return Li.test(t);
};
U.testAlphanumeric = function(t) {
  return Bi.test(t);
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
})(G);
(function(n) {
  const t = x, e = Rt, s = Bt, i = G, r = ae, o = 7973, a = t.getBCHDigit(o);
  function c(u, f, g) {
    for (let y = 1; y <= 40; y++)
      if (f <= n.getCapacity(y, g, u))
        return y;
  }
  function d(u, f) {
    return i.getCharCountIndicator(u, f) + 4;
  }
  function l(u, f) {
    let g = 0;
    return u.forEach(function(y) {
      const A = d(y.mode, f);
      g += A + y.getBitsLength();
    }), g;
  }
  function h(u, f) {
    for (let g = 1; g <= 40; g++)
      if (l(u, g) <= n.getCapacity(g, f, i.MIXED))
        return g;
  }
  n.from = function(f, g) {
    return r.isValid(f) ? parseInt(f, 10) : g;
  }, n.getCapacity = function(f, g, y) {
    if (!r.isValid(f))
      throw new Error("Invalid QR Code version");
    typeof y > "u" && (y = i.BYTE);
    const A = t.getSymbolTotalCodewords(f), p = e.getTotalCodewordsCount(f, g), v = (A - p) * 8;
    if (y === i.MIXED) return v;
    const _ = v - d(y, f);
    switch (y) {
      case i.NUMERIC:
        return Math.floor(_ / 10 * 3);
      case i.ALPHANUMERIC:
        return Math.floor(_ / 11 * 2);
      case i.KANJI:
        return Math.floor(_ / 13);
      case i.BYTE:
      default:
        return Math.floor(_ / 8);
    }
  }, n.getBestVersionForData = function(f, g) {
    let y;
    const A = s.from(g, s.M);
    if (Array.isArray(f)) {
      if (f.length > 1)
        return h(f, A);
      if (f.length === 0)
        return 1;
      y = f[0];
    } else
      y = f;
    return c(y.mode, y.getLength(), A);
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
const Yt = x, Qe = 1335, Ri = 21522, Te = Yt.getBCHDigit(Qe);
Ye.getEncodedBits = function(t, e) {
  const s = t.bit << 3 | e;
  let i = s << 10;
  for (; Yt.getBCHDigit(i) - Te >= 0; )
    i ^= Qe << Yt.getBCHDigit(i) - Te;
  return (s << 10 | i) ^ Ri;
};
var Ze = {};
const Ui = G;
function nt(n) {
  this.mode = Ui.NUMERIC, this.data = n.toString();
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
  let e, s, i;
  for (e = 0; e + 3 <= this.data.length; e += 3)
    s = this.data.substr(e, 3), i = parseInt(s, 10), t.put(i, 10);
  const r = this.data.length - e;
  r > 0 && (s = this.data.substr(e), i = parseInt(s, 10), t.put(i, r * 3 + 1));
};
var Oi = nt;
const Hi = G, qt = [
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
  this.mode = Hi.ALPHANUMERIC, this.data = n;
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
    let s = qt.indexOf(this.data[e]) * 45;
    s += qt.indexOf(this.data[e + 1]), t.put(s, 11);
  }
  this.data.length % 2 && t.put(qt.indexOf(this.data[e]), 6);
};
var zi = rt;
const Fi = G;
function ot(n) {
  this.mode = Fi.BYTE, typeof n == "string" ? this.data = new TextEncoder().encode(n) : this.data = new Uint8Array(n);
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
var Vi = ot;
const ji = G, qi = x;
function at(n) {
  this.mode = ji.KANJI, this.data = n;
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
    let e = qi.toSJIS(this.data[t]);
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
var Ki = at, Xe = { exports: {} };
(function(n) {
  var t = {
    single_source_shortest_paths: function(e, s, i) {
      var r = {}, o = {};
      o[s] = 0;
      var a = t.PriorityQueue.make();
      a.push(s, 0);
      for (var c, d, l, h, u, f, g, y, A; !a.empty(); ) {
        c = a.pop(), d = c.value, h = c.cost, u = e[d] || {};
        for (l in u)
          u.hasOwnProperty(l) && (f = u[l], g = h + f, y = o[l], A = typeof o[l] > "u", (A || y > g) && (o[l] = g, a.push(l, g), r[l] = d));
      }
      if (typeof i < "u" && typeof o[i] > "u") {
        var p = ["Could not find a path from ", s, " to ", i, "."].join("");
        throw new Error(p);
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
})(Xe);
var Gi = Xe.exports;
(function(n) {
  const t = G, e = Oi, s = zi, i = Vi, r = Ki, o = U, a = x, c = Gi;
  function d(p) {
    return unescape(encodeURIComponent(p)).length;
  }
  function l(p, v, _) {
    const m = [];
    let E;
    for (; (E = p.exec(_)) !== null; )
      m.push({
        data: E[0],
        index: E.index,
        mode: v,
        length: E[0].length
      });
    return m;
  }
  function h(p) {
    const v = l(o.NUMERIC, t.NUMERIC, p), _ = l(o.ALPHANUMERIC, t.ALPHANUMERIC, p);
    let m, E;
    return a.isKanjiModeEnabled() ? (m = l(o.BYTE, t.BYTE, p), E = l(o.KANJI, t.KANJI, p)) : (m = l(o.BYTE_KANJI, t.BYTE, p), E = []), v.concat(_, m, E).sort(function($, M) {
      return $.index - M.index;
    }).map(function($) {
      return {
        data: $.data,
        mode: $.mode,
        length: $.length
      };
    });
  }
  function u(p, v) {
    switch (v) {
      case t.NUMERIC:
        return e.getBitsLength(p);
      case t.ALPHANUMERIC:
        return s.getBitsLength(p);
      case t.KANJI:
        return r.getBitsLength(p);
      case t.BYTE:
        return i.getBitsLength(p);
    }
  }
  function f(p) {
    return p.reduce(function(v, _) {
      const m = v.length - 1 >= 0 ? v[v.length - 1] : null;
      return m && m.mode === _.mode ? (v[v.length - 1].data += _.data, v) : (v.push(_), v);
    }, []);
  }
  function g(p) {
    const v = [];
    for (let _ = 0; _ < p.length; _++) {
      const m = p[_];
      switch (m.mode) {
        case t.NUMERIC:
          v.push([
            m,
            { data: m.data, mode: t.ALPHANUMERIC, length: m.length },
            { data: m.data, mode: t.BYTE, length: m.length }
          ]);
          break;
        case t.ALPHANUMERIC:
          v.push([
            m,
            { data: m.data, mode: t.BYTE, length: m.length }
          ]);
          break;
        case t.KANJI:
          v.push([
            m,
            { data: m.data, mode: t.BYTE, length: d(m.data) }
          ]);
          break;
        case t.BYTE:
          v.push([
            { data: m.data, mode: t.BYTE, length: d(m.data) }
          ]);
      }
    }
    return v;
  }
  function y(p, v) {
    const _ = {}, m = { start: {} };
    let E = ["start"];
    for (let C = 0; C < p.length; C++) {
      const $ = p[C], M = [];
      for (let V = 0; V < $.length; V++) {
        const B = $[V], dt = "" + C + V;
        M.push(dt), _[dt] = { node: B, lastCount: 0 }, m[dt] = {};
        for (let Ht = 0; Ht < E.length; Ht++) {
          const O = E[Ht];
          _[O] && _[O].node.mode === B.mode ? (m[O][dt] = u(_[O].lastCount + B.length, B.mode) - u(_[O].lastCount, B.mode), _[O].lastCount += B.length) : (_[O] && (_[O].lastCount = B.length), m[O][dt] = u(B.length, B.mode) + 4 + t.getCharCountIndicator(B.mode, v));
        }
      }
      E = M;
    }
    for (let C = 0; C < E.length; C++)
      m[E[C]].end = 0;
    return { map: m, table: _ };
  }
  function A(p, v) {
    let _;
    const m = t.getBestModeForData(p);
    if (_ = t.from(v, m), _ !== t.BYTE && _.bit < m.bit)
      throw new Error('"' + p + '" cannot be encoded with mode ' + t.toString(_) + `.
 Suggested mode is: ` + t.toString(m));
    switch (_ === t.KANJI && !a.isKanjiModeEnabled() && (_ = t.BYTE), _) {
      case t.NUMERIC:
        return new e(p);
      case t.ALPHANUMERIC:
        return new s(p);
      case t.KANJI:
        return new r(p);
      case t.BYTE:
        return new i(p);
    }
  }
  n.fromArray = function(v) {
    return v.reduce(function(_, m) {
      return typeof m == "string" ? _.push(A(m, null)) : m.data && _.push(A(m.data, m.mode)), _;
    }, []);
  }, n.fromString = function(v, _) {
    const m = h(v, a.isKanjiModeEnabled()), E = g(m), C = y(E, _), $ = c.find_path(C.map, "start", "end"), M = [];
    for (let V = 1; V < $.length - 1; V++)
      M.push(C.table[$[V]].node);
    return n.fromArray(f(M));
  }, n.rawSplit = function(v) {
    return n.fromArray(
      h(v, a.isKanjiModeEnabled())
    );
  };
})(Ze);
const Ot = x, Kt = Bt, Wi = Pi, Ji = Ni, Yi = Ve, Qi = je, Qt = qe, Zt = Rt, Zi = Ii, Dt = We, Xi = Ye, ts = G, Gt = Ze;
function es(n, t) {
  const e = n.size, s = Qi.getPositions(t);
  for (let i = 0; i < s.length; i++) {
    const r = s[i][0], o = s[i][1];
    for (let a = -1; a <= 7; a++)
      if (!(r + a <= -1 || e <= r + a))
        for (let c = -1; c <= 7; c++)
          o + c <= -1 || e <= o + c || (a >= 0 && a <= 6 && (c === 0 || c === 6) || c >= 0 && c <= 6 && (a === 0 || a === 6) || a >= 2 && a <= 4 && c >= 2 && c <= 4 ? n.set(r + a, o + c, !0, !0) : n.set(r + a, o + c, !1, !0));
  }
}
function is(n) {
  const t = n.size;
  for (let e = 8; e < t - 8; e++) {
    const s = e % 2 === 0;
    n.set(e, 6, s, !0), n.set(6, e, s, !0);
  }
}
function ss(n, t) {
  const e = Yi.getPositions(t);
  for (let s = 0; s < e.length; s++) {
    const i = e[s][0], r = e[s][1];
    for (let o = -2; o <= 2; o++)
      for (let a = -2; a <= 2; a++)
        o === -2 || o === 2 || a === -2 || a === 2 || o === 0 && a === 0 ? n.set(i + o, r + a, !0, !0) : n.set(i + o, r + a, !1, !0);
  }
}
function ns(n, t) {
  const e = n.size, s = Dt.getEncodedBits(t);
  let i, r, o;
  for (let a = 0; a < 18; a++)
    i = Math.floor(a / 3), r = a % 3 + e - 8 - 3, o = (s >> a & 1) === 1, n.set(i, r, o, !0), n.set(r, i, o, !0);
}
function Wt(n, t, e) {
  const s = n.size, i = Xi.getEncodedBits(t, e);
  let r, o;
  for (r = 0; r < 15; r++)
    o = (i >> r & 1) === 1, r < 6 ? n.set(r, 8, o, !0) : r < 8 ? n.set(r + 1, 8, o, !0) : n.set(s - 15 + r, 8, o, !0), r < 8 ? n.set(8, s - r - 1, o, !0) : r < 9 ? n.set(8, 15 - r - 1 + 1, o, !0) : n.set(8, 15 - r - 1, o, !0);
  n.set(s - 8, 8, 1, !0);
}
function rs(n, t) {
  const e = n.size;
  let s = -1, i = e - 1, r = 7, o = 0;
  for (let a = e - 1; a > 0; a -= 2)
    for (a === 6 && a--; ; ) {
      for (let c = 0; c < 2; c++)
        if (!n.isReserved(i, a - c)) {
          let d = !1;
          o < t.length && (d = (t[o] >>> r & 1) === 1), n.set(i, a - c, d), r--, r === -1 && (o++, r = 7);
        }
      if (i += s, i < 0 || e <= i) {
        i -= s, s = -s;
        break;
      }
    }
}
function os(n, t, e) {
  const s = new Wi();
  e.forEach(function(c) {
    s.put(c.mode.bit, 4), s.put(c.getLength(), ts.getCharCountIndicator(c.mode, n)), c.write(s);
  });
  const i = Ot.getSymbolTotalCodewords(n), r = Zt.getTotalCodewordsCount(n, t), o = (i - r) * 8;
  for (s.getLengthInBits() + 4 <= o && s.put(0, 4); s.getLengthInBits() % 8 !== 0; )
    s.putBit(0);
  const a = (o - s.getLengthInBits()) / 8;
  for (let c = 0; c < a; c++)
    s.put(c % 2 ? 17 : 236, 8);
  return as(s, n, t);
}
function as(n, t, e) {
  const s = Ot.getSymbolTotalCodewords(t), i = Zt.getTotalCodewordsCount(t, e), r = s - i, o = Zt.getBlocksCount(t, e), a = s % o, c = o - a, d = Math.floor(s / o), l = Math.floor(r / o), h = l + 1, u = d - l, f = new Zi(u);
  let g = 0;
  const y = new Array(o), A = new Array(o);
  let p = 0;
  const v = new Uint8Array(n.buffer);
  for (let $ = 0; $ < o; $++) {
    const M = $ < c ? l : h;
    y[$] = v.slice(g, g + M), A[$] = f.encode(y[$]), g += M, p = Math.max(p, M);
  }
  const _ = new Uint8Array(s);
  let m = 0, E, C;
  for (E = 0; E < p; E++)
    for (C = 0; C < o; C++)
      E < y[C].length && (_[m++] = y[C][E]);
  for (E = 0; E < u; E++)
    for (C = 0; C < o; C++)
      _[m++] = A[C][E];
  return _;
}
function cs(n, t, e, s) {
  let i;
  if (Array.isArray(n))
    i = Gt.fromArray(n);
  else if (typeof n == "string") {
    let d = t;
    if (!d) {
      const l = Gt.rawSplit(n);
      d = Dt.getBestVersionForData(l, e);
    }
    i = Gt.fromString(n, d || 40);
  } else
    throw new Error("Invalid data");
  const r = Dt.getBestVersionForData(i, e);
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
  const o = os(t, e, i), a = Ot.getSymbolSize(t), c = new Ji(a);
  return es(c, t), is(c), ss(c, t), Wt(c, e, 0), t >= 7 && ns(c, t), rs(c, o), isNaN(s) && (s = Qt.getBestMask(
    c,
    Wt.bind(null, c, e)
  )), Qt.applyMask(s, c), Wt(c, e, s), {
    modules: c,
    version: t,
    errorCorrectionLevel: e,
    maskPattern: s,
    segments: i
  };
}
ze.create = function(t, e) {
  if (typeof t > "u" || t === "")
    throw new Error("No input text");
  let s = Kt.M, i, r;
  return typeof e < "u" && (s = Kt.from(e.errorCorrectionLevel, Kt.M), i = Dt.from(e.version), r = Qt.from(e.maskPattern), e.toSJISFunc && Ot.setToSJISFunction(e.toSJISFunc)), cs(t, i, s, r);
};
var ti = {}, ce = {};
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
    const o = i.modules.size, a = i.modules.data, c = n.getScale(o, r), d = Math.floor((o + r.margin * 2) * c), l = r.margin * c, h = [r.color.light, r.color.dark];
    for (let u = 0; u < d; u++)
      for (let f = 0; f < d; f++) {
        let g = (u * d + f) * 4, y = r.color.light;
        if (u >= l && f >= l && u < d - l && f < d - l) {
          const A = Math.floor((u - l) / c), p = Math.floor((f - l) / c);
          y = h[a[A * o + p] ? 1 : 0];
        }
        s[g++] = y.r, s[g++] = y.g, s[g++] = y.b, s[g] = y.a;
      }
  };
})(ce);
(function(n) {
  const t = ce;
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
  n.render = function(r, o, a) {
    let c = a, d = o;
    typeof c > "u" && (!o || !o.getContext) && (c = o, o = void 0), o || (d = s()), c = t.getOptions(c);
    const l = t.getImageWidth(r.modules.size, c), h = d.getContext("2d"), u = h.createImageData(l, l);
    return t.qrToImageData(u.data, r, c), e(h, d, l), h.putImageData(u, 0, 0), d;
  }, n.renderToDataURL = function(r, o, a) {
    let c = a;
    typeof c > "u" && (!o || !o.getContext) && (c = o, o = void 0), c || (c = {});
    const d = n.render(r, o, c), l = c.type || "image/png", h = c.rendererOpts || {};
    return d.toDataURL(l, h.quality);
  };
})(ti);
var ei = {};
const ls = ce;
function Me(n, t) {
  const e = n.a / 255, s = t + '="' + n.hex + '"';
  return e < 1 ? s + " " + t + '-opacity="' + e.toFixed(2).slice(1) + '"' : s;
}
function Jt(n, t, e) {
  let s = n + t;
  return typeof e < "u" && (s += " " + e), s;
}
function ds(n, t, e) {
  let s = "", i = 0, r = !1, o = 0;
  for (let a = 0; a < n.length; a++) {
    const c = Math.floor(a % t), d = Math.floor(a / t);
    !c && !r && (r = !0), n[a] ? (o++, a > 0 && c > 0 && n[a - 1] || (s += r ? Jt("M", c + e, 0.5 + d + e) : Jt("m", i, 0), i = 0, r = !1), c + 1 < t && n[a + 1] || (s += Jt("h", o), o = 0)) : i++;
  }
  return s;
}
ei.render = function(t, e, s) {
  const i = ls.getOptions(e), r = t.modules.size, o = t.modules.data, a = r + i.margin * 2, c = i.color.light.a ? "<path " + Me(i.color.light, "fill") + ' d="M0 0h' + a + "v" + a + 'H0z"/>' : "", d = "<path " + Me(i.color.dark, "stroke") + ' d="' + ds(o, r, i.margin) + '"/>', l = 'viewBox="0 0 ' + a + " " + a + '"', u = '<svg xmlns="http://www.w3.org/2000/svg" ' + (i.width ? 'width="' + i.width + '" height="' + i.width + '" ' : "") + l + ' shape-rendering="crispEdges">' + c + d + `</svg>
`;
  return typeof s == "function" && s(null, u), u;
};
const hs = ki, Xt = ze, ii = ti, us = ei;
function le(n, t, e, s, i) {
  const r = [].slice.call(arguments, 1), o = r.length, a = typeof r[o - 1] == "function";
  if (!a && !hs())
    throw new Error("Callback required as last argument");
  if (a) {
    if (o < 2)
      throw new Error("Too few arguments provided");
    o === 2 ? (i = e, e = t, t = s = void 0) : o === 3 && (t.getContext && typeof i > "u" ? (i = s, s = void 0) : (i = s, s = e, e = t, t = void 0));
  } else {
    if (o < 1)
      throw new Error("Too few arguments provided");
    return o === 1 ? (e = t, t = s = void 0) : o === 2 && !t.getContext && (s = e, e = t, t = void 0), new Promise(function(c, d) {
      try {
        const l = Xt.create(e, s);
        c(n(l, t, s));
      } catch (l) {
        d(l);
      }
    });
  }
  try {
    const c = Xt.create(e, s);
    i(null, n(c, t, s));
  } catch (c) {
    i(c);
  }
}
kt.create = Xt.create;
kt.toCanvas = le.bind(null, ii.render);
kt.toDataURL = le.bind(null, ii.renderToDataURL);
kt.toString = le.bind(null, function(n, t, e) {
  return us.render(n, e);
});
class I {
  /**
   * Resolves a value that might be an entity ID or a raw string.
   */
  static getValue(t, e) {
    return !e || !t ? e || "" : t.states[e] ? t.states[e].state : e;
  }
  /**
   * Discovers a Wi-Fi password using manual overrides, entity IDs, or smart attribute mapping.
   */
  static getPasswordForSsid(t, e, s, i, r) {
    if (!t) return "";
    if (r && r !== "password123")
      return this.getValue(t, r);
    if (!s) return "";
    const o = parseInt(s, 10), a = e.find((l) => {
      const h = !i || l.networkId === i;
      return isNaN(o) ? l.name === s && h : l.number === o && h;
    });
    if (a)
      for (const l in t.states) {
        const h = t.states[l], u = h.attributes;
        if (u.network_id === a.networkId && u.ssid_number === a.number) {
          if (u.psk) return String(u.psk);
          if (u.password) return String(u.password);
          if (h.state && !["unknown", "unavailable"].includes(h.state) && (l.includes("password") || l.includes("psk")))
            return h.state;
        }
      }
    const d = (a ? a.name : s).toLowerCase().replace(/[^a-z0-9]/g, "_");
    for (const l in t.states)
      if (l.includes(d) && (l.includes("password") || l.includes("psk"))) {
        const h = t.states[l];
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
    const s = this.escapeWifiString(t), i = e ? this.escapeWifiString(e) : "";
    return i ? `WIFI:T:WPA;S:${s};P:${i};;` : `WIFI:T:nopass;S:${s};P:;;`;
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
    } catch (s) {
      return console.error("Failed to generate QR code SVG:", s), '<div style="text-align:center; padding: 24px;">QR Code Unavailable</div>';
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
    ], s = (i) => i[Math.floor(Math.random() * i.length)];
    return `${s(t)}-${s(e)}-${Math.floor(Math.random() * 1e3)}`;
  }
}
var fs = Object.defineProperty, W = (n, t, e, s) => {
  for (var i = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = o(t, e, i) || i);
  return i && fs(t, e, i), i;
};
const de = class de extends N {
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
    this.hass && await R.pollConfig(this.hass, (t, e) => {
      this._loadingMessage = t, this._isLoading = e;
    });
  }
  _discoverEntity() {
    if (this.hass)
      return Object.keys(this.hass.states).find((t) => {
        if (!t.startsWith("select.")) return !1;
        const s = this.hass.states[t].attributes.friendly_name, i = typeof s == "string" ? s.toLowerCase() : "";
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
    var l, h, u;
    if (!this.hass || !this._config) return b``;
    if (this._isLoading)
      return At(
        ((l = this._config) == null ? void 0 : l.name) || "Cisco Meraki Content Filter",
        this._loadingMessage,
        "2.3.0-beta.3625"
      );
    const t = this._config.entity || this._discoverEntity(), e = t ? this.hass.states[t] : void 0, s = this._config.entity ? this.hass.states[this._config.entity] : void 0, i = (h = s == null ? void 0 : s.attributes) == null ? void 0 : h.friendly_name, r = typeof i == "string" ? i : "Cisco Meraki", o = this._config.name || (this._config.entity ? `${r} Content Filter` : "Cisco Meraki Content Filter");
    if (!t || !e)
      return ne(
        "Entity Missing",
        "No content filter entity was found. Please check your configuration.",
        "2.3.0-beta.3625"
      );
    const a = e.state || "Unknown", c = ((u = e.attributes) == null ? void 0 : u.options) || [
      "None",
      "Security",
      "Family",
      "Strict"
    ], d = this._optimisticProfile || a;
    return b`
      <ha-card .header="${o}">
        <div class="card-content">
          <div class="button-grid">
            ${c.map((f) => {
      const g = d.toLowerCase() === f.toLowerCase(), y = this._isUpdating && this._optimisticProfile === f;
      return b`
                <button
                  class="filter-btn ${g ? "active" : ""} ${this._isUpdating && !y ? "disabled" : ""}"
                  ?disabled=${this._isUpdating}
                  @click=${() => this._setFilterProfile(f, t)}
                >
                  ${y ? b`<ha-circular-progress
                          active
                          size="small"
                        ></ha-circular-progress>
                        Saving...` : f}
                </button>
              `;
    })}
          </div>
        </div>
        <div class="version">v${"2.3.0-beta.3625"}</div>
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
        }), window.setTimeout(() => {
          this._optimisticProfile = null, this._isUpdating = !1;
        }, 8e3);
      } catch (s) {
        console.error("Failed to call select_option service:", s), this._optimisticProfile = null, this._isUpdating = !1;
      }
    }
  }
};
de.styles = [
  $t,
  D`
      :host {
        display: block;
      }
      ha-card {
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }
      .card-content {
        padding: 16px;
      }
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
        background: var(
          --secondary-background-color,
          rgba(255, 255, 255, 0.05)
        );
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
  w()
], H.prototype, "_config");
W([
  w()
], H.prototype, "_optimisticProfile");
W([
  w()
], H.prototype, "_isUpdating");
W([
  w()
], H.prototype, "_isLoading");
W([
  w()
], H.prototype, "_loadingMessage");
const he = class he extends N {
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
    this.dispatchEvent(
      new CustomEvent("config-changed", {
        detail: { config: e },
        bubbles: !0,
        composed: !0
      })
    );
  }
};
he.styles = D`
    .editor-container {
      padding: 16px;
    }
  `;
let wt = he;
W([
  L({ attribute: !1 })
], wt.prototype, "hass");
W([
  w()
], wt.prototype, "_config");
customElements.get("meraki-content-filter-card") || customElements.define("meraki-content-filter-card", H);
customElements.get("meraki-content-filter-card-editor") || customElements.define(
  "meraki-content-filter-card-editor",
  wt
);
window.customCards = window.customCards || [];
window.customCards.some(
  (n) => n.type === "meraki-content-filter-card"
) || window.customCards.push({
  type: "meraki-content-filter-card",
  name: "Cisco Meraki Content Filter",
  description: "Control Cisco Meraki Content Filtering profiles.",
  preview: !0
});
var gs = Object.defineProperty, T = (n, t, e, s) => {
  for (var i = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = o(t, e, i) || i);
  return i && gs(t, e, i), i;
};
const ue = class ue extends N {
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
      (s, i) => {
        this._loadingMessage = s, this._isLoading = i;
      }
    );
    this._networks = t, this._ssids = e;
  }
  _valueChanged(t) {
    if (!this._config) return;
    const e = t.detail.value, s = { ...this._config, ...e };
    this._config.networkId !== e.networkId && (s.ssid = ""), Object.keys(s).forEach((i) => {
      s[i] === "" && delete s[i];
    }), this.dispatchEvent(
      new CustomEvent("config-changed", {
        detail: { config: s },
        bubbles: !0,
        composed: !0
      })
    );
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
    const t = R.getNetworkOptions(
      this._networks,
      !0
    ), e = R.getSsidOptions(
      this._ssids,
      this._config.networkId,
      "name"
    ), s = [
      {
        name: "networkId",
        selector: { select: { options: t, mode: "dropdown" } }
      },
      {
        name: "ssid",
        selector: {
          select: {
            options: e,
            custom_value: !0,
            mode: "dropdown"
          }
        }
      },
      { name: "password", selector: { text: {} } },
      { name: "name", selector: { text: {} } }
    ];
    return b`
      <div class="editor-container">
        <ha-form
          .hass=${this.hass}
          .data=${this._config}
          .schema=${s}
          .computeLabel=${this._computeLabel}
          @value-changed=${this._valueChanged}
        ></ha-form>
      </div>
    `;
  }
};
ue.styles = D`
    .editor-container {
      padding: 16px;
    }
  `;
let z = ue;
T([
  L({ attribute: !1 })
], z.prototype, "hass");
T([
  w()
], z.prototype, "_config");
T([
  w()
], z.prototype, "_networks");
T([
  w()
], z.prototype, "_ssids");
T([
  w()
], z.prototype, "_isLoading");
T([
  w()
], z.prototype, "_loadingMessage");
const fe = class fe extends N {
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
      (e, s) => {
        this._loadingMessage = e, this._isLoading = s;
      }
    );
    this._ssids = t, this._generateQR();
  }
  updated(t) {
    (t.has("hass") || t.has("_config")) && this._generateQR();
  }
  async _generateQR() {
    if (!this._config) return;
    const t = I.getValue(this.hass, this._config.ssid), e = I.getPasswordForSsid(
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
    const s = I.generateWifiQrString(t, e);
    this._qrSvg = await I.generateQrSvg(s, 2);
  }
  render() {
    var s;
    if (!this._config || !this.hass) return b``;
    if (this._isLoading)
      return At(
        ((s = this._config) == null ? void 0 : s.name) || "Wi-Fi Access",
        this._loadingMessage,
        "2.3.0-beta.3625"
      );
    const t = I.getValue(this.hass, this._config.ssid), e = I.getPasswordForSsid(
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
          <div
            class="qr-container"
            style="width: 200px; height: 200px;"
            .innerHTML=${this._qrSvg}
          ></div>
          ${e ? b`<div class="password-display">
                Password: <code class="copyable-code">${e}</code>
              </div>` : ""}
        </div>
        <div class="version">v${"2.3.0-beta.3625"}</div>
      </ha-card>
    `;
  }
};
fe.styles = [
  $t,
  D`
      :host {
        display: block;
      }
      .card-content {
        padding: 16px;
        gap: 16px;
      }
      .ssid-display {
        font-size: 1.5em;
        font-weight: bold;
        color: var(--primary-text-color);
        text-align: center;
      }
      .password-display {
        color: var(--secondary-text-color);
        text-align: center;
      }
    `
];
let F = fe;
T([
  L({ attribute: !1 })
], F.prototype, "hass");
T([
  w()
], F.prototype, "_config");
T([
  w()
], F.prototype, "_qrSvg");
T([
  w()
], F.prototype, "_isLoading");
T([
  w()
], F.prototype, "_loadingMessage");
T([
  w()
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
var ps = Object.defineProperty, ct = (n, t, e, s) => {
  for (var i = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = o(t, e, i) || i);
  return i && ps(t, e, i), i;
};
const ge = class ge extends N {
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
    this.hass && await R.pollConfig(this.hass, (t, e) => {
      this._loadingMessage = t, this._isLoading = e;
    });
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
        const s = new CustomEvent("navigate", {
          detail: { path: e.navigation_path },
          bubbles: !0,
          composed: !0
        });
        this.dispatchEvent(s);
      } else {
        const s = new CustomEvent("hass-more-info", {
          detail: { entityId: t },
          bubbles: !0,
          composed: !0
        });
        this.dispatchEvent(s);
      }
  }
  _renderStatusDot(t, e, s) {
    const i = !!t && !!this.hass.states[t];
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
        class="status-item ${i ? "clickable" : ""}"
        @click="${() => i ? this._handleEntityClick(t, s) : null}"
        role="${i ? "button" : "presentation"}"
        tabindex="${i ? "0" : "-1"}"
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
    var i, r;
    if (!this._config || !this.hass)
      return b``;
    if (this._isLoading)
      return At(
        ((i = this._config) == null ? void 0 : i.name) || "Cisco Meraki Network Vitals",
        this._loadingMessage,
        "2.3.0-beta.3625"
      );
    const t = this._config.throughput_entity;
    t && this.hass.states[t] && console.log(
      "MERAKI CARD DIAGNOSTIC - Throughput Raw Entity State:",
      this.hass.states[t]
    );
    const e = t ? this.hass.states[t] : void 0, s = e ? (e.state || "0") + " " + (((r = e.attributes) == null ? void 0 : r.unit_of_measurement) || "") : "N/A";
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
              <span class="throughput-value">${s}</span>
            </div>
          </div>
        </div>
        <div class="version">v${"2.3.0-beta.3625"}</div>
      </ha-card>
    `;
  }
};
ge.styles = [
  $t,
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
  w()
], X.prototype, "_config");
ct([
  w()
], X.prototype, "_isLoading");
ct([
  w()
], X.prototype, "_loadingMessage");
const pe = class pe extends N {
  setConfig(t) {
    this._config = t;
  }
  render() {
    var t, e, s;
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
          .value=${((s = this._config.ap_tap_action) == null ? void 0 : s.action) || "more-info"}
          .configValue=${"ap_tap_action"}
          @input=${this._valueChanged}
        ></ha-textfield>
      </div>
    `;
  }
  _valueChanged(t) {
    var o;
    if (!this._config) return;
    const e = t.target, s = e.configValue;
    let i = ((o = t.detail) == null ? void 0 : o.value) ?? e.value;
    s && s.endsWith("_tap_action") && typeof i == "string" && (i.startsWith("/") ? i = { action: "navigate", navigation_path: i } : i = { action: i });
    const r = { ...this._config, [s]: i };
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
  w()
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
var ms = Object.defineProperty, lt = (n, t, e, s) => {
  for (var i = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = o(t, e, i) || i);
  return i && ms(t, e, i), i;
};
const me = class me extends N {
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
    this.hass && await R.pollConfig(this.hass, (t, e) => {
      this._loadingMessage = t, this._isLoading = e;
    });
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
      const e = this.hass.states[t], s = e.attributes.vlan_name, i = e.attributes.friendly_name;
      let r = "Unknown VLAN";
      return typeof s == "string" ? r = s : typeof i == "string" && (r = i.replace(" DHCP", "")), {
        entity_id: t,
        name: r,
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
      return At(
        ((e = this._config) == null ? void 0 : e.name) || "Cisco Meraki VLANs",
        this._loadingMessage,
        "2.3.0-beta.3625"
      );
    const t = this._getVlanEntities();
    return t.length === 0 ? ne(
      "No VLANs Found",
      "No Meraki VLAN DHCP switches were found. Ensure VLAN management is enabled in the integration options.",
      "2.3.0-beta.3625"
    ) : b`
      <ha-card .header="${this._config.name || "Cisco Meraki VLANs"}">
        <div class="card-content">
          <div class="vlan-table">
            <div class="table-header">
              <div class="col-vlan">VLAN</div>
              <div class="col-network">Subnet / Gateway</div>
              <div class="col-dhcp">DHCP</div>
            </div>
            ${t.map(
      (s) => b`
                <div class="table-row">
                  <div class="col-vlan">
                    <span class="vlan-name">${s.name}</span>
                  </div>
                  <div class="col-network">
                    <div class="subnet">${s.subnet}</div>
                    <div class="gateway">${s.gateway}</div>
                  </div>
                  <div class="col-dhcp">
                    <ha-switch
                      .checked=${s.state === "on"}
                      @change=${() => this._toggleDhcp(s.entity_id)}
                    ></ha-switch>
                  </div>
                </div>
              `
    )}
          </div>
        </div>
        <div class="version">v${"2.3.0-beta.3625"}</div>
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
  $t,
  D`
      :host {
        display: block;
      }
      .card-content {
        padding: 0 16px 16px 16px;
      }

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

      .col-vlan {
        flex: 2;
        display: flex;
        align-items: center;
      }
      .col-network {
        flex: 3;
      }
      .col-dhcp {
        flex: 1;
        display: flex;
        justify-content: flex-end;
      }

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
  w()
], tt.prototype, "_config");
lt([
  w()
], tt.prototype, "_isLoading");
lt([
  w()
], tt.prototype, "_loadingMessage");
const _e = class _e extends N {
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
    this.dispatchEvent(
      new CustomEvent("config-changed", {
        detail: { config: e },
        bubbles: !0,
        composed: !0
      })
    );
  }
};
_e.styles = D`
    .editor-container {
      padding: 16px;
    }
  `;
let bt = _e;
lt([
  L({ attribute: !1 })
], bt.prototype, "hass");
lt([
  w()
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
var _s = Object.defineProperty, si = (n, t, e, s) => {
  for (var i = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = o(t, e, i) || i);
  return i && _s(t, e, i), i;
};
const ye = class ye extends N {
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
    this.dispatchEvent(
      new CustomEvent("config-changed", {
        detail: { config: e },
        bubbles: !0,
        composed: !0
      })
    );
  }
};
ye.styles = D`
    .editor-container {
      padding: 16px;
    }
  `;
let Et = ye;
si([
  L({ attribute: !1 })
], Et.prototype, "hass");
si([
  w()
], Et.prototype, "_config");
customElements.get("meraki-guest-access-card-editor") || customElements.define(
  "meraki-guest-access-card-editor",
  Et
);
var ys = Object.defineProperty, P = (n, t, e, s) => {
  for (var i = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = o(t, e, i) || i);
  return i && ys(t, e, i), i;
};
const we = class we extends N {
  constructor() {
    super(...arguments), this._formData = {
      network: "",
      ssid: "",
      passphrase: "",
      policy: "",
      duration: "60",
      guestName: ""
    }, this._networks = [], this._ssids = [], this._policies = [], this._creating = !1, this._error = null, this._success = null, this._qrSvg = "", this._isLoading = !0, this._loadingMessage = "Connecting to Meraki...", this._configEntryId = null, this._provisioning = !1, this._countdown = 30, this._computeLabel = (t) => t.name === "network" ? "Network" : t.name === "ssid" ? "SSID" : t.name === "policy" ? "Group Policy (Required)" : t.name === "passphrase" ? "Passphrase / PSK (Auto-discovered)" : t.name === "duration" ? "Duration" : t.name === "guestName" ? "Guest Name" : t.name;
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
  disconnectedCallback() {
    super.disconnectedCallback(), this._stopProvisioningTimer();
  }
  updated(t) {
    var e;
    super.updated(t), t.has("hass") && this.hass && ((e = this.hass.user) != null && e.name) && !this._formData.guestName && (this._formData = {
      ...this._formData,
      guestName: this._generateUniqueGuestName()
    });
  }
  _generateUniqueGuestName() {
    var s, i;
    const t = ((i = (s = this.hass) == null ? void 0 : s.user) == null ? void 0 : i.name) || "Home Assistant", e = Math.floor(Math.random() * 1e4).toString().padStart(4, "0");
    return `${t} - Guest ${e}`;
  }
  async _loadCentralizedData() {
    var d;
    if (!this.hass) return;
    const { networks: t, ssids: e, groupPolicies: s, entryId: i } = await R.pollConfig(this.hass, (l, h) => {
      this._loadingMessage = l, this._isLoading = h;
    });
    if (t.length === 0) {
      this._isLoading = !1;
      return;
    }
    this._networks = t, this._ssids = e, this._policies = s || [], this._configEntryId = ((d = this._config) == null ? void 0 : d.config_entry_id) || i;
    let r = this._formData.network, o = this._formData.ssid, a = this._formData.passphrase, c = this._formData.policy;
    if (t.length > 0 && !r && (r = t[0].id), r && !o) {
      const l = e.filter((h) => h.networkId === r);
      l.length > 0 && (o = String(l[0].number));
    }
    if (r && o && !a && (a = I.getPasswordForSsid(
      this.hass,
      this._ssids,
      o,
      r
    ), a || (a = I.generateNaturalPassword())), r && !c) {
      const l = this._policies.filter(
        (h) => h.networkId === r
      );
      l.length > 0 ? c = String(
        l[0].groupPolicyId || l[0].id
      ) : c = "NONE";
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
    const e = t.detail.value, s = this._formData.network, i = { ...this._formData, ...e };
    if (i.network !== s) {
      i.ssid = "", i.passphrase = "", i.policy = "";
      const r = this._ssids.filter(
        (a) => a.networkId === i.network
      );
      r.length > 0 && (i.ssid = String(r[0].number));
      const o = this._policies.filter(
        (a) => a.networkId === i.network
      );
      o.length > 0 ? i.policy = String(
        o[0].groupPolicyId || o[0].id
      ) : i.policy = "NONE";
    }
    !i.passphrase && i.network && i.ssid && (i.passphrase = I.getPasswordForSsid(
      this.hass,
      this._ssids,
      i.ssid,
      i.network
    ) || I.generateNaturalPassword()), this._formData = i;
  }
  _startProvisioningTimer() {
    this._stopProvisioningTimer(), this._provisioning = !0, this._countdown = 30, this._timerInterval = window.setInterval(() => {
      this._countdown -= 1, this._countdown <= 0 && this._stopProvisioningTimer();
    }, 1e3);
  }
  _stopProvisioningTimer() {
    this._timerInterval && (clearInterval(this._timerInterval), this._timerInterval = void 0), this._provisioning = !1;
  }
  render() {
    var h, u, f;
    if (this._isLoading)
      return At(
        ((h = this._config) == null ? void 0 : h.name) || "Cisco Meraki Guest Access",
        this._loadingMessage,
        "2.3.0-beta.3625"
      );
    if (this._networks.length === 0)
      return ne(
        "No Wireless Networks",
        "No Cisco Meraki wireless networks found. Ensure the integration is configured.",
        "2.3.0-beta.3625"
      );
    const t = R.getNetworkOptions(
      this._networks
    ), e = R.getSsidOptions(
      this._ssids,
      this._formData.network,
      "number"
    ), i = this._policies.filter(
      (g) => g.networkId === this._formData.network
    ).map((g) => ({
      value: String(g.groupPolicyId || g.id),
      label: g.name
    }));
    i.length === 0 && i.push({ value: "NONE", label: "Network Default" });
    const r = [
      {
        name: "network",
        selector: { select: { options: t, mode: "dropdown" } }
      },
      {
        name: "ssid",
        selector: { select: { options: e, mode: "dropdown" } }
      },
      {
        name: "policy",
        selector: {
          select: { options: i, mode: "dropdown" }
        }
      },
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
    ], o = this._formData.network && this._formData.ssid && this._formData.policy, a = parseInt(this._formData.ssid, 10), c = this._ssids.find(
      (g) => g.networkId === this._formData.network && g.number === a
    ), d = (c == null ? void 0 : c.authMode) === "ipsk-without-radius", l = c && !d;
    if (this._success && this._qrSvg) {
      const g = this._networks.find(
        (p) => p.id === this._formData.network
      ), y = parseInt(this._formData.ssid, 10), A = this._ssids.find(
        (p) => p.networkId === this._formData.network && p.number === y
      );
      return b`
        <ha-card .header="${((u = this._config) == null ? void 0 : u.name) || "Share Access"}">
          <div class="card-content success-ui">
            <ha-alert alert-type="success">${this._success}</ha-alert>

            ${this._provisioning ? b`
                  <div class="provisioning-ui">
                    <ha-circular-progress
                      active
                      size="large"
                    ></ha-circular-progress>
                    <p>Syncing to Meraki Access Points...</p>
                    <p class="timer">
                      Please wait ${this._countdown}s for the password to
                      activate.
                    </p>
                  </div>
                ` : b`
                  <div
                    class="qr-container"
                    style="width: 200px; height: 200px;"
                    .innerHTML="${this._qrSvg}"
                  ></div>

                  <div class="credentials-block">
                    <div class="credential-item">
                      <span class="label">Network:</span>
                      <span class="value"
                        >${(g == null ? void 0 : g.name) || "Unknown"}</span
                      >
                    </div>
                    <div class="credential-item">
                      <span class="label">SSID:</span>
                      <span class="value"
                        >${(A == null ? void 0 : A.name) || "Unknown"}</span
                      >
                    </div>
                    <div class="credential-item">
                      <span class="label">Password:</span>
                      <code class="copyable-code"
                        >${this._formData.passphrase}</code
                      >
                    </div>
                  </div>
                `}

            <ha-button raised @click=${this._resetForm}>
              Create Another
            </ha-button>
          </div>
          <div class="version">v${"2.3.0-beta.3625"}</div>
        </ha-card>
      `;
    }
    return b`
      <ha-card .header="${((f = this._config) == null ? void 0 : f.name) || "Cisco Meraki Guest Access"}">
        <div class="card-content">
          ${this._error ? b`<ha-alert
                alert-type="error"
                dismissable
                @alert-dismissed-clicked="${() => this._error = null}"
                >${this._error}</ha-alert
              >` : ""}

          <div class="form-container">
            ${l ? b`
                  <ha-alert
                    alert-type="warning"
                    title="SSID Configuration Required"
                  >
                    The selected SSID "${c.name}" is not
                    configured for Identity PSK. Please change the security
                    mode to "Identity PSK without RADIUS" in your Meraki
                    Dashboard. See the integration README to learn how to do
                    this safely without dropping existing devices.
                  </ha-alert>
                ` : ""}

            <ha-form
              .hass=${this.hass}
              .data=${this._formData}
              .schema=${r}
              .computeLabel=${this._computeLabel}
              @value-changed=${this._formValueChanged}
            ></ha-form>

            <ha-button
              raised
              .disabled=${this._creating || !o || l}
              @click=${this._generateAccessKey}
            >
              ${this._creating ? b`<ha-circular-progress
                    active
                    size="small"
                  ></ha-circular-progress>` : "Generate Access Key"}
            </ha-button>
          </div>
        </div>
        <div class="version">v${"2.3.0-beta.3625"}</div>
      </ha-card>
    `;
  }
  _resetForm() {
    this._stopProvisioningTimer(), this._success = null, this._error = null, this._qrSvg = "", this._formData = {
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
        const e = parseInt(this._formData.ssid, 10), s = this._ssids.find(
          (a) => a.networkId === this._formData.network && a.number === e
        ), i = s ? s.name : "Guest WiFi", r = this._formData.passphrase, o = I.generateWifiQrString(i, r);
        this._qrSvg = await I.generateQrSvg(o), this._success = "Guest access key created successfully!", this._startProvisioningTimer();
      } catch (t) {
        this._error = `Failed to create guest key: ${t instanceof Error ? t.message : t}`;
      } finally {
        this._creating = !1;
      }
    }
  }
};
we.styles = [
  $t,
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
      .provisioning-ui {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 24px;
        text-align: center;
        gap: 8px;
      }
      .timer {
        font-weight: bold;
        color: var(--primary-color);
      }
    `
];
let S = we;
P([
  L({ attribute: !1 })
], S.prototype, "hass");
P([
  w()
], S.prototype, "_config");
P([
  w()
], S.prototype, "_formData");
P([
  w()
], S.prototype, "_networks");
P([
  w()
], S.prototype, "_ssids");
P([
  w()
], S.prototype, "_policies");
P([
  w()
], S.prototype, "_creating");
P([
  w()
], S.prototype, "_error");
P([
  w()
], S.prototype, "_success");
P([
  w()
], S.prototype, "_qrSvg");
P([
  w()
], S.prototype, "_isLoading");
P([
  w()
], S.prototype, "_loadingMessage");
P([
  w()
], S.prototype, "_configEntryId");
P([
  w()
], S.prototype, "_provisioning");
P([
  w()
], S.prototype, "_countdown");
customElements.get("meraki-guest-access-card") || customElements.define("meraki-guest-access-card", S);
window.customCards = window.customCards || [];
window.customCards.some(
  (n) => n.type === "meraki-guest-access-card"
) || window.customCards.push({
  type: "meraki-guest-access-card",
  name: "Cisco Meraki Guest Access",
  description: "Manage temporary guest WiFi access. Version: 2.3.0-beta.3625",
  preview: !0,
  version: "2.3.0-beta.3625"
});
export {
  S as MerakiGuestAccessCard
};
