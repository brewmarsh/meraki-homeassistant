/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const $t = globalThis, Qt = $t.ShadowRoot && ($t.ShadyCSS === void 0 || $t.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, Zt = Symbol(), ge = /* @__PURE__ */ new WeakMap();
let Ne = class {
  constructor(t, e, s) {
    if (this._$cssResult$ = !0, s !== Zt) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = t, this.t = e;
  }
  get styleSheet() {
    let t = this.o;
    const e = this.t;
    if (Qt && t === void 0) {
      const s = e !== void 0 && e.length === 1;
      s && (t = ge.get(e)), t === void 0 && ((this.o = t = new CSSStyleSheet()).replaceSync(this.cssText), s && ge.set(e, t));
    }
    return t;
  }
  toString() {
    return this.cssText;
  }
};
const Xe = (n) => new Ne(typeof n == "string" ? n : n + "", void 0, Zt), F = (n, ...t) => {
  const e = n.length === 1 ? n[0] : t.reduce((s, i, r) => s + ((o) => {
    if (o._$cssResult$ === !0) return o.cssText;
    if (typeof o == "number") return o;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + o + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(i) + n[r + 1], n[0]);
  return new Ne(e, n, Zt);
}, ti = (n, t) => {
  if (Qt) n.adoptedStyleSheets = t.map((e) => e instanceof CSSStyleSheet ? e : e.styleSheet);
  else for (const e of t) {
    const s = document.createElement("style"), i = $t.litNonce;
    i !== void 0 && s.setAttribute("nonce", i), s.textContent = e.cssText, n.appendChild(s);
  }
}, pe = Qt ? (n) => n : (n) => n instanceof CSSStyleSheet ? ((t) => {
  let e = "";
  for (const s of t.cssRules) e += s.cssText;
  return Xe(e);
})(n) : n;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: ei, defineProperty: ii, getOwnPropertyDescriptor: si, getOwnPropertyNames: ni, getOwnPropertySymbols: ri, getPrototypeOf: oi } = Object, G = globalThis, me = G.trustedTypes, ai = me ? me.emptyScript : "", Ut = G.reactiveElementPolyfillSupport, dt = (n, t) => n, St = { toAttribute(n, t) {
  switch (t) {
    case Boolean:
      n = n ? ai : null;
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
} }, Xt = (n, t) => !ei(n, t), _e = { attribute: !0, type: String, converter: St, reflect: !1, useDefault: !1, hasChanged: Xt };
Symbol.metadata ?? (Symbol.metadata = Symbol("metadata")), G.litPropertyMetadata ?? (G.litPropertyMetadata = /* @__PURE__ */ new WeakMap());
let tt = class extends HTMLElement {
  static addInitializer(t) {
    this._$Ei(), (this.l ?? (this.l = [])).push(t);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(t, e = _e) {
    if (e.state && (e.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(t) && ((e = Object.create(e)).wrapped = !0), this.elementProperties.set(t, e), !e.noAccessor) {
      const s = Symbol(), i = this.getPropertyDescriptor(t, s, e);
      i !== void 0 && ii(this.prototype, t, i);
    }
  }
  static getPropertyDescriptor(t, e, s) {
    const { get: i, set: r } = si(this.prototype, t) ?? { get() {
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
    return this.elementProperties.get(t) ?? _e;
  }
  static _$Ei() {
    if (this.hasOwnProperty(dt("elementProperties"))) return;
    const t = oi(this);
    t.finalize(), t.l !== void 0 && (this.l = [...t.l]), this.elementProperties = new Map(t.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(dt("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(dt("properties"))) {
      const e = this.properties, s = [...ni(e), ...ri(e)];
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
      for (const i of s) e.unshift(pe(i));
    } else t !== void 0 && e.push(pe(t));
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
    return ti(t, this.constructor.elementStyles), t;
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
      const o = (((r = s.converter) == null ? void 0 : r.toAttribute) !== void 0 ? s.converter : St).toAttribute(e, s.type);
      this._$Em = t, o == null ? this.removeAttribute(i) : this.setAttribute(i, o), this._$Em = null;
    }
  }
  _$AK(t, e) {
    var r, o;
    const s = this.constructor, i = s._$Eh.get(t);
    if (i !== void 0 && this._$Em !== i) {
      const a = s.getPropertyOptions(i), c = typeof a.converter == "function" ? { fromAttribute: a.converter } : ((r = a.converter) == null ? void 0 : r.fromAttribute) !== void 0 ? a.converter : St;
      this._$Em = i;
      const l = c.fromAttribute(e, a.type);
      this[i] = l ?? ((o = this._$Ej) == null ? void 0 : o.get(i)) ?? l, this._$Em = null;
    }
  }
  requestUpdate(t, e, s, i = !1, r) {
    var o;
    if (t !== void 0) {
      const a = this.constructor;
      if (i === !1 && (r = this[t]), s ?? (s = a.getPropertyOptions(t)), !((s.hasChanged ?? Xt)(r, e) || s.useDefault && s.reflect && r === ((o = this._$Ej) == null ? void 0 : o.get(t)) && !this.hasAttribute(a._$Eu(t, s)))) return;
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
tt.elementStyles = [], tt.shadowRootOptions = { mode: "open" }, tt[dt("elementProperties")] = /* @__PURE__ */ new Map(), tt[dt("finalized")] = /* @__PURE__ */ new Map(), Ut == null || Ut({ ReactiveElement: tt }), (G.reactiveElementVersions ?? (G.reactiveElementVersions = [])).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const ht = globalThis, ye = (n) => n, kt = ht.trustedTypes, we = kt ? kt.createPolicy("lit-html", { createHTML: (n) => n }) : void 0, Te = "$lit$", j = `lit$${Math.random().toFixed(9).slice(2)}$`, Me = "?" + j, ci = `<${Me}>`, Z = document, ft = () => Z.createComment(""), gt = (n) => n === null || typeof n != "object" && typeof n != "function", te = Array.isArray, li = (n) => te(n) || typeof (n == null ? void 0 : n[Symbol.iterator]) == "function", Ot = `[ 	
\f\r]`, lt = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, ve = /-->/g, be = />/g, J = RegExp(`>|${Ot}(?:([^\\s"'>=/]+)(${Ot}*=${Ot}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`, "g"), Ee = /'/g, Ce = /"/g, Ie = /^(?:script|style|textarea|title)$/i, di = (n) => (t, ...e) => ({ _$litType$: n, strings: t, values: e }), b = di(1), et = Symbol.for("lit-noChange"), $ = Symbol.for("lit-nothing"), Ae = /* @__PURE__ */ new WeakMap(), Y = Z.createTreeWalker(Z, 129);
function xe(n, t) {
  if (!te(n) || !n.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return we !== void 0 ? we.createHTML(t) : t;
}
const hi = (n, t) => {
  const e = n.length - 1, s = [];
  let i, r = t === 2 ? "<svg>" : t === 3 ? "<math>" : "", o = lt;
  for (let a = 0; a < e; a++) {
    const c = n[a];
    let l, d, h = -1, u = 0;
    for (; u < c.length && (o.lastIndex = u, d = o.exec(c), d !== null); ) u = o.lastIndex, o === lt ? d[1] === "!--" ? o = ve : d[1] !== void 0 ? o = be : d[2] !== void 0 ? (Ie.test(d[2]) && (i = RegExp("</" + d[2], "g")), o = J) : d[3] !== void 0 && (o = J) : o === J ? d[0] === ">" ? (o = i ?? lt, h = -1) : d[1] === void 0 ? h = -2 : (h = o.lastIndex - d[2].length, l = d[1], o = d[3] === void 0 ? J : d[3] === '"' ? Ce : Ee) : o === Ce || o === Ee ? o = J : o === ve || o === be ? o = lt : (o = J, i = void 0);
    const f = o === J && n[a + 1].startsWith("/>") ? " " : "";
    r += o === lt ? c + ci : h >= 0 ? (s.push(l), c.slice(0, h) + Te + c.slice(h) + j + f) : c + j + (h === -2 ? a : f);
  }
  return [xe(n, r + (n[e] || "<?>") + (t === 2 ? "</svg>" : t === 3 ? "</math>" : "")), s];
};
class pt {
  constructor({ strings: t, _$litType$: e }, s) {
    let i;
    this.parts = [];
    let r = 0, o = 0;
    const a = t.length - 1, c = this.parts, [l, d] = hi(t, e);
    if (this.el = pt.createElement(l, s), Y.currentNode = this.el.content, e === 2 || e === 3) {
      const h = this.el.content.firstChild;
      h.replaceWith(...h.childNodes);
    }
    for (; (i = Y.nextNode()) !== null && c.length < a; ) {
      if (i.nodeType === 1) {
        if (i.hasAttributes()) for (const h of i.getAttributeNames()) if (h.endsWith(Te)) {
          const u = d[o++], f = i.getAttribute(h).split(j), g = /([.?@])?(.*)/.exec(u);
          c.push({ type: 1, index: r, name: g[2], strings: f, ctor: g[1] === "." ? fi : g[1] === "?" ? gi : g[1] === "@" ? pi : Tt }), i.removeAttribute(h);
        } else h.startsWith(j) && (c.push({ type: 6, index: r }), i.removeAttribute(h));
        if (Ie.test(i.tagName)) {
          const h = i.textContent.split(j), u = h.length - 1;
          if (u > 0) {
            i.textContent = kt ? kt.emptyScript : "";
            for (let f = 0; f < u; f++) i.append(h[f], ft()), Y.nextNode(), c.push({ type: 2, index: ++r });
            i.append(h[u], ft());
          }
        }
      } else if (i.nodeType === 8) if (i.data === Me) c.push({ type: 2, index: r });
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
function it(n, t, e = n, s) {
  var o, a;
  if (t === et) return t;
  let i = s !== void 0 ? (o = e._$Co) == null ? void 0 : o[s] : e._$Cl;
  const r = gt(t) ? void 0 : t._$litDirective$;
  return (i == null ? void 0 : i.constructor) !== r && ((a = i == null ? void 0 : i._$AO) == null || a.call(i, !1), r === void 0 ? i = void 0 : (i = new r(n), i._$AT(n, e, s)), s !== void 0 ? (e._$Co ?? (e._$Co = []))[s] = i : e._$Cl = i), i !== void 0 && (t = it(n, i._$AS(n, t.values), i, s)), t;
}
class ui {
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
        let l;
        c.type === 2 ? l = new vt(r, r.nextSibling, this, t) : c.type === 1 ? l = new c.ctor(r, c.name, c.strings, this, t) : c.type === 6 && (l = new mi(r, this, t)), this._$AV.push(l), c = s[++a];
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
class vt {
  get _$AU() {
    var t;
    return ((t = this._$AM) == null ? void 0 : t._$AU) ?? this._$Cv;
  }
  constructor(t, e, s, i) {
    this.type = 2, this._$AH = $, this._$AN = void 0, this._$AA = t, this._$AB = e, this._$AM = s, this.options = i, this._$Cv = (i == null ? void 0 : i.isConnected) ?? !0;
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
    t = it(this, t, e), gt(t) ? t === $ || t == null || t === "" ? (this._$AH !== $ && this._$AR(), this._$AH = $) : t !== this._$AH && t !== et && this._(t) : t._$litType$ !== void 0 ? this.$(t) : t.nodeType !== void 0 ? this.T(t) : li(t) ? this.k(t) : this._(t);
  }
  O(t) {
    return this._$AA.parentNode.insertBefore(t, this._$AB);
  }
  T(t) {
    this._$AH !== t && (this._$AR(), this._$AH = this.O(t));
  }
  _(t) {
    this._$AH !== $ && gt(this._$AH) ? this._$AA.nextSibling.data = t : this.T(Z.createTextNode(t)), this._$AH = t;
  }
  $(t) {
    var r;
    const { values: e, _$litType$: s } = t, i = typeof s == "number" ? this._$AC(t) : (s.el === void 0 && (s.el = pt.createElement(xe(s.h, s.h[0]), this.options)), s);
    if (((r = this._$AH) == null ? void 0 : r._$AD) === i) this._$AH.p(e);
    else {
      const o = new ui(i, this), a = o.u(this.options);
      o.p(e), this.T(a), this._$AH = o;
    }
  }
  _$AC(t) {
    let e = Ae.get(t.strings);
    return e === void 0 && Ae.set(t.strings, e = new pt(t)), e;
  }
  k(t) {
    te(this._$AH) || (this._$AH = [], this._$AR());
    const e = this._$AH;
    let s, i = 0;
    for (const r of t) i === e.length ? e.push(s = new vt(this.O(ft()), this.O(ft()), this, this.options)) : s = e[i], s._$AI(r), i++;
    i < e.length && (this._$AR(s && s._$AB.nextSibling, i), e.length = i);
  }
  _$AR(t = this._$AA.nextSibling, e) {
    var s;
    for ((s = this._$AP) == null ? void 0 : s.call(this, !1, !0, e); t !== this._$AB; ) {
      const i = ye(t).nextSibling;
      ye(t).remove(), t = i;
    }
  }
  setConnected(t) {
    var e;
    this._$AM === void 0 && (this._$Cv = t, (e = this._$AP) == null || e.call(this, t));
  }
}
class Tt {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(t, e, s, i, r) {
    this.type = 1, this._$AH = $, this._$AN = void 0, this.element = t, this.name = e, this._$AM = i, this.options = r, s.length > 2 || s[0] !== "" || s[1] !== "" ? (this._$AH = Array(s.length - 1).fill(new String()), this.strings = s) : this._$AH = $;
  }
  _$AI(t, e = this, s, i) {
    const r = this.strings;
    let o = !1;
    if (r === void 0) t = it(this, t, e, 0), o = !gt(t) || t !== this._$AH && t !== et, o && (this._$AH = t);
    else {
      const a = t;
      let c, l;
      for (t = r[0], c = 0; c < r.length - 1; c++) l = it(this, a[s + c], e, c), l === et && (l = this._$AH[c]), o || (o = !gt(l) || l !== this._$AH[c]), l === $ ? t = $ : t !== $ && (t += (l ?? "") + r[c + 1]), this._$AH[c] = l;
    }
    o && !i && this.j(t);
  }
  j(t) {
    t === $ ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, t ?? "");
  }
}
class fi extends Tt {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(t) {
    this.element[this.name] = t === $ ? void 0 : t;
  }
}
class gi extends Tt {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(t) {
    this.element.toggleAttribute(this.name, !!t && t !== $);
  }
}
class pi extends Tt {
  constructor(t, e, s, i, r) {
    super(t, e, s, i, r), this.type = 5;
  }
  _$AI(t, e = this) {
    if ((t = it(this, t, e, 0) ?? $) === et) return;
    const s = this._$AH, i = t === $ && s !== $ || t.capture !== s.capture || t.once !== s.once || t.passive !== s.passive, r = t !== $ && (s === $ || i);
    i && this.element.removeEventListener(this.name, this, s), r && this.element.addEventListener(this.name, this, t), this._$AH = t;
  }
  handleEvent(t) {
    var e;
    typeof this._$AH == "function" ? this._$AH.call(((e = this.options) == null ? void 0 : e.host) ?? this.element, t) : this._$AH.handleEvent(t);
  }
}
class mi {
  constructor(t, e, s) {
    this.element = t, this.type = 6, this._$AN = void 0, this._$AM = e, this.options = s;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t) {
    it(this, t);
  }
}
const Ht = ht.litHtmlPolyfillSupport;
Ht == null || Ht(pt, vt), (ht.litHtmlVersions ?? (ht.litHtmlVersions = [])).push("3.3.2");
const _i = (n, t, e) => {
  const s = (e == null ? void 0 : e.renderBefore) ?? t;
  let i = s._$litPart$;
  if (i === void 0) {
    const r = (e == null ? void 0 : e.renderBefore) ?? null;
    s._$litPart$ = i = new vt(t.insertBefore(ft(), r), r, void 0, e ?? {});
  }
  return i._$AI(n), i;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Q = globalThis;
class M extends tt {
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
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Do = _i(e, this.renderRoot, this.renderOptions);
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
    return et;
  }
}
var Pe;
M._$litElement$ = !0, M.finalized = !0, (Pe = Q.litElementHydrateSupport) == null || Pe.call(Q, { LitElement: M });
const Ft = Q.litElementPolyfillSupport;
Ft == null || Ft({ LitElement: M });
(Q.litElementVersions ?? (Q.litElementVersions = [])).push("4.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const yi = { attribute: !0, type: String, converter: St, reflect: !1, hasChanged: Xt }, wi = (n = yi, t, e) => {
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
function z(n) {
  return (t, e) => typeof e == "object" ? wi(n, t, e) : ((s, i, r) => {
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
  return z({ ...n, state: !0, attribute: !1 });
}
const De = (n, t, e) => b`
  <ha-card class="status-card warning">
    <div class="card-content flex-col align-center p-8">
      <ha-icon icon="mdi:alert-circle" style="--mdc-icon-size: 48px; margin-bottom: 16px;"></ha-icon>
      <h1 class="status-title">${n}</h1>
      <div class="status-message mt-4">${t}</div>
    </div>
    ${b`<div class="version">v${e}</div>`}
  </ha-card>
`, Mt = (n, t, e) => b`
  <ha-card class="status-card loading">
    <div class="card-content flex-col align-center p-8">
      <h1 class="status-title">${n}</h1>
      <ha-circular-progress active></ha-circular-progress>
      <div class="status-message mt-4">${t}</div>
    </div>
    <div class="version">v${e}</div>
  </ha-card>
`, It = F`
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
var Be = /* @__PURE__ */ ((n) => (n.GET_CONFIG = "meraki_ha/get_config", n.SUBSCRIBE_MERAKI_DATA = "meraki_ha/subscribe_meraki_data", n.GET_CAMERA_STREAM_URL = "meraki_ha/get_camera_stream_url", n.GET_CAMERA_SNAPSHOT = "meraki_ha/get_camera_snapshot", n.GET_VERSION = "meraki_ha/get_version", n.GET_NETWORK_EVENTS = "meraki_ha/get_network_events", n.UPDATE_ENABLED_NETWORKS = "meraki_ha/update_enabled_networks", n.CREATE_GUEST_KEY = "meraki_ha/ipsk/create", n.GET_GUEST_KEYS = "meraki_ha/ipsk/get", n.REVOKE_GUEST_KEY = "meraki_ha/ipsk/revoke", n.TIMED_ACCESS_GET_POLICIES = "meraki_ha/timed_access/get_policies", n))(Be || {});
const vi = async (n, t) => {
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
class L {
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
      const i = await vi(t, {
        type: Be.GET_CONFIG,
        config_entry_id: s
      }), r = (Array.isArray(i.networks) ? i.networks : []).filter((c) => {
        var l;
        return (l = c.productTypes) == null ? void 0 : l.includes("wireless");
      }), o = Array.isArray(i.ssids) ? i.ssids : [], a = [];
      if (i.group_policies && typeof i.group_policies == "object")
        for (const [c, l] of Object.entries(
          i.group_policies
        ))
          Array.isArray(l) && l.forEach((d) => {
            a.push({
              networkId: c,
              groupPolicyId: String(d.groupPolicyId),
              name: d.name
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
var bt = {}, bi = function() {
  return typeof Promise == "function" && Promise.prototype && Promise.prototype.then;
}, Re = {}, P = {};
let ee;
const Ei = [
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
P.getSymbolSize = function(t) {
  if (!t) throw new Error('"version" cannot be null or undefined');
  if (t < 1 || t > 40) throw new Error('"version" should be in range from 1 to 40');
  return t * 4 + 17;
};
P.getSymbolTotalCodewords = function(t) {
  return Ei[t];
};
P.getBCHDigit = function(n) {
  let t = 0;
  for (; n !== 0; )
    t++, n >>>= 1;
  return t;
};
P.setToSJISFunction = function(t) {
  if (typeof t != "function")
    throw new Error('"toSJISFunc" is not a valid function.');
  ee = t;
};
P.isKanjiModeEnabled = function() {
  return typeof ee < "u";
};
P.toSJIS = function(t) {
  return ee(t);
};
var xt = {};
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
})(xt);
function Le() {
  this.buffer = [], this.length = 0;
}
Le.prototype = {
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
var Ci = Le;
function Et(n) {
  if (!n || n < 1)
    throw new Error("BitMatrix size must be defined and greater than 0");
  this.size = n, this.data = new Uint8Array(n * n), this.reservedBit = new Uint8Array(n * n);
}
Et.prototype.set = function(n, t, e, s) {
  const i = n * this.size + t;
  this.data[i] = e, s && (this.reservedBit[i] = !0);
};
Et.prototype.get = function(n, t) {
  return this.data[n * this.size + t];
};
Et.prototype.xor = function(n, t, e) {
  this.data[n * this.size + t] ^= e;
};
Et.prototype.isReserved = function(n, t) {
  return this.reservedBit[n * this.size + t];
};
var Ai = Et, Ue = {};
(function(n) {
  const t = P.getSymbolSize;
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
})(Ue);
var Oe = {};
const $i = P.getSymbolSize, $e = 7;
Oe.getPositions = function(t) {
  const e = $i(t);
  return [
    // top-left
    [0, 0],
    // top-right
    [e - $e, 0],
    // bottom-left
    [0, e - $e]
  ];
};
var He = {};
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
    let o = 0, a = 0, c = 0, l = null, d = null;
    for (let h = 0; h < r; h++) {
      a = c = 0, l = d = null;
      for (let u = 0; u < r; u++) {
        let f = i.get(h, u);
        f === l ? a++ : (a >= 5 && (o += t.N1 + (a - 5)), l = f, a = 1), f = i.get(u, h), f === d ? c++ : (c >= 5 && (o += t.N1 + (c - 5)), d = f, c = 1);
      }
      a >= 5 && (o += t.N1 + (a - 5)), c >= 5 && (o += t.N1 + (c - 5));
    }
    return o;
  }, n.getPenaltyN2 = function(i) {
    const r = i.size;
    let o = 0;
    for (let a = 0; a < r - 1; a++)
      for (let c = 0; c < r - 1; c++) {
        const l = i.get(a, c) + i.get(a, c + 1) + i.get(a + 1, c) + i.get(a + 1, c + 1);
        (l === 4 || l === 0) && o++;
      }
    return o * t.N2;
  }, n.getPenaltyN3 = function(i) {
    const r = i.size;
    let o = 0, a = 0, c = 0;
    for (let l = 0; l < r; l++) {
      a = c = 0;
      for (let d = 0; d < r; d++)
        a = a << 1 & 2047 | i.get(l, d), d >= 10 && (a === 1488 || a === 93) && o++, c = c << 1 & 2047 | i.get(d, l), d >= 10 && (c === 1488 || c === 93) && o++;
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
    for (let l = 0; l < o; l++) {
      r(l), n.applyMask(l, i);
      const d = n.getPenaltyN1(i) + n.getPenaltyN2(i) + n.getPenaltyN3(i) + n.getPenaltyN4(i);
      n.applyMask(l, i), d < c && (c = d, a = l);
    }
    return a;
  };
})(He);
var Dt = {};
const q = xt, Ct = [
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
], At = [
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
Dt.getBlocksCount = function(t, e) {
  switch (e) {
    case q.L:
      return Ct[(t - 1) * 4 + 0];
    case q.M:
      return Ct[(t - 1) * 4 + 1];
    case q.Q:
      return Ct[(t - 1) * 4 + 2];
    case q.H:
      return Ct[(t - 1) * 4 + 3];
    default:
      return;
  }
};
Dt.getTotalCodewordsCount = function(t, e) {
  switch (e) {
    case q.L:
      return At[(t - 1) * 4 + 0];
    case q.M:
      return At[(t - 1) * 4 + 1];
    case q.Q:
      return At[(t - 1) * 4 + 2];
    case q.H:
      return At[(t - 1) * 4 + 3];
    default:
      return;
  }
};
var Fe = {}, Bt = {};
const ut = new Uint8Array(512), Pt = new Uint8Array(256);
(function() {
  let t = 1;
  for (let e = 0; e < 255; e++)
    ut[e] = t, Pt[t] = e, t <<= 1, t & 256 && (t ^= 285);
  for (let e = 255; e < 512; e++)
    ut[e] = ut[e - 255];
})();
Bt.log = function(t) {
  if (t < 1) throw new Error("log(" + t + ")");
  return Pt[t];
};
Bt.exp = function(t) {
  return ut[t];
};
Bt.mul = function(t, e) {
  return t === 0 || e === 0 ? 0 : ut[Pt[t] + Pt[e]];
};
(function(n) {
  const t = Bt;
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
})(Fe);
const ze = Fe;
function ie(n) {
  this.genPoly = void 0, this.degree = n, this.degree && this.initialize(this.degree);
}
ie.prototype.initialize = function(t) {
  this.degree = t, this.genPoly = ze.generateECPolynomial(this.degree);
};
ie.prototype.encode = function(t) {
  if (!this.genPoly)
    throw new Error("Encoder not initialized");
  const e = new Uint8Array(t.length + this.degree);
  e.set(t);
  const s = ze.mod(e, this.genPoly), i = this.degree - s.length;
  if (i > 0) {
    const r = new Uint8Array(this.degree);
    return r.set(s, i), r;
  }
  return s;
};
var Si = ie, Ve = {}, K = {}, se = {};
se.isValid = function(t) {
  return !isNaN(t) && t >= 1 && t <= 40;
};
var B = {};
const je = "[0-9]+", ki = "[A-Z $%*+\\-./:]+";
let mt = "(?:[u3000-u303F]|[u3040-u309F]|[u30A0-u30FF]|[uFF00-uFFEF]|[u4E00-u9FAF]|[u2605-u2606]|[u2190-u2195]|u203B|[u2010u2015u2018u2019u2025u2026u201Cu201Du2225u2260]|[u0391-u0451]|[u00A7u00A8u00B1u00B4u00D7u00F7])+";
mt = mt.replace(/u/g, "\\u");
const Pi = "(?:(?![A-Z0-9 $%*+\\-./:]|" + mt + `)(?:.|[\r
]))+`;
B.KANJI = new RegExp(mt, "g");
B.BYTE_KANJI = new RegExp("[^A-Z0-9 $%*+\\-./:]+", "g");
B.BYTE = new RegExp(Pi, "g");
B.NUMERIC = new RegExp(je, "g");
B.ALPHANUMERIC = new RegExp(ki, "g");
const Ni = new RegExp("^" + mt + "$"), Ti = new RegExp("^" + je + "$"), Mi = new RegExp("^[A-Z0-9 $%*+\\-./:]+$");
B.testKanji = function(t) {
  return Ni.test(t);
};
B.testNumeric = function(t) {
  return Ti.test(t);
};
B.testAlphanumeric = function(t) {
  return Mi.test(t);
};
(function(n) {
  const t = se, e = B;
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
})(K);
(function(n) {
  const t = P, e = Dt, s = xt, i = K, r = se, o = 7973, a = t.getBCHDigit(o);
  function c(u, f, g) {
    for (let y = 1; y <= 40; y++)
      if (f <= n.getCapacity(y, g, u))
        return y;
  }
  function l(u, f) {
    return i.getCharCountIndicator(u, f) + 4;
  }
  function d(u, f) {
    let g = 0;
    return u.forEach(function(y) {
      const S = l(y.mode, f);
      g += S + y.getBitsLength();
    }), g;
  }
  function h(u, f) {
    for (let g = 1; g <= 40; g++)
      if (d(u, g) <= n.getCapacity(g, f, i.MIXED))
        return g;
  }
  n.from = function(f, g) {
    return r.isValid(f) ? parseInt(f, 10) : g;
  }, n.getCapacity = function(f, g, y) {
    if (!r.isValid(f))
      throw new Error("Invalid QR Code version");
    typeof y > "u" && (y = i.BYTE);
    const S = t.getSymbolTotalCodewords(f), _ = e.getTotalCodewordsCount(f, g), w = (S - _) * 8;
    if (y === i.MIXED) return w;
    const m = w - l(y, f);
    switch (y) {
      case i.NUMERIC:
        return Math.floor(m / 10 * 3);
      case i.ALPHANUMERIC:
        return Math.floor(m / 11 * 2);
      case i.KANJI:
        return Math.floor(m / 13);
      case i.BYTE:
      default:
        return Math.floor(m / 8);
    }
  }, n.getBestVersionForData = function(f, g) {
    let y;
    const S = s.from(g, s.M);
    if (Array.isArray(f)) {
      if (f.length > 1)
        return h(f, S);
      if (f.length === 0)
        return 1;
      y = f[0];
    } else
      y = f;
    return c(y.mode, y.getLength(), S);
  }, n.getEncodedBits = function(f) {
    if (!r.isValid(f) || f < 7)
      throw new Error("Invalid QR Code version");
    let g = f << 12;
    for (; t.getBCHDigit(g) - a >= 0; )
      g ^= o << t.getBCHDigit(g) - a;
    return f << 12 | g;
  };
})(Ve);
var qe = {};
const Kt = P, Ge = 1335, Ii = 21522, Se = Kt.getBCHDigit(Ge);
qe.getEncodedBits = function(t, e) {
  const s = t.bit << 3 | e;
  let i = s << 10;
  for (; Kt.getBCHDigit(i) - Se >= 0; )
    i ^= Ge << Kt.getBCHDigit(i) - Se;
  return (s << 10 | i) ^ Ii;
};
var Ke = {};
const xi = K;
function st(n) {
  this.mode = xi.NUMERIC, this.data = n.toString();
}
st.getBitsLength = function(t) {
  return 10 * Math.floor(t / 3) + (t % 3 ? t % 3 * 3 + 1 : 0);
};
st.prototype.getLength = function() {
  return this.data.length;
};
st.prototype.getBitsLength = function() {
  return st.getBitsLength(this.data.length);
};
st.prototype.write = function(t) {
  let e, s, i;
  for (e = 0; e + 3 <= this.data.length; e += 3)
    s = this.data.substr(e, 3), i = parseInt(s, 10), t.put(i, 10);
  const r = this.data.length - e;
  r > 0 && (s = this.data.substr(e), i = parseInt(s, 10), t.put(i, r * 3 + 1));
};
var Di = st;
const Bi = K, zt = [
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
function nt(n) {
  this.mode = Bi.ALPHANUMERIC, this.data = n;
}
nt.getBitsLength = function(t) {
  return 11 * Math.floor(t / 2) + 6 * (t % 2);
};
nt.prototype.getLength = function() {
  return this.data.length;
};
nt.prototype.getBitsLength = function() {
  return nt.getBitsLength(this.data.length);
};
nt.prototype.write = function(t) {
  let e;
  for (e = 0; e + 2 <= this.data.length; e += 2) {
    let s = zt.indexOf(this.data[e]) * 45;
    s += zt.indexOf(this.data[e + 1]), t.put(s, 11);
  }
  this.data.length % 2 && t.put(zt.indexOf(this.data[e]), 6);
};
var Ri = nt;
const Li = K;
function rt(n) {
  this.mode = Li.BYTE, typeof n == "string" ? this.data = new TextEncoder().encode(n) : this.data = new Uint8Array(n);
}
rt.getBitsLength = function(t) {
  return t * 8;
};
rt.prototype.getLength = function() {
  return this.data.length;
};
rt.prototype.getBitsLength = function() {
  return rt.getBitsLength(this.data.length);
};
rt.prototype.write = function(n) {
  for (let t = 0, e = this.data.length; t < e; t++)
    n.put(this.data[t], 8);
};
var Ui = rt;
const Oi = K, Hi = P;
function ot(n) {
  this.mode = Oi.KANJI, this.data = n;
}
ot.getBitsLength = function(t) {
  return t * 13;
};
ot.prototype.getLength = function() {
  return this.data.length;
};
ot.prototype.getBitsLength = function() {
  return ot.getBitsLength(this.data.length);
};
ot.prototype.write = function(n) {
  let t;
  for (t = 0; t < this.data.length; t++) {
    let e = Hi.toSJIS(this.data[t]);
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
var Fi = ot, We = { exports: {} };
(function(n) {
  var t = {
    single_source_shortest_paths: function(e, s, i) {
      var r = {}, o = {};
      o[s] = 0;
      var a = t.PriorityQueue.make();
      a.push(s, 0);
      for (var c, l, d, h, u, f, g, y, S; !a.empty(); ) {
        c = a.pop(), l = c.value, h = c.cost, u = e[l] || {};
        for (d in u)
          u.hasOwnProperty(d) && (f = u[d], g = h + f, y = o[d], S = typeof o[d] > "u", (S || y > g) && (o[d] = g, a.push(d, g), r[d] = l));
      }
      if (typeof i < "u" && typeof o[i] > "u") {
        var _ = ["Could not find a path from ", s, " to ", i, "."].join("");
        throw new Error(_);
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
})(We);
var zi = We.exports;
(function(n) {
  const t = K, e = Di, s = Ri, i = Ui, r = Fi, o = B, a = P, c = zi;
  function l(_) {
    return unescape(encodeURIComponent(_)).length;
  }
  function d(_, w, m) {
    const p = [];
    let E;
    for (; (E = _.exec(m)) !== null; )
      p.push({
        data: E[0],
        index: E.index,
        mode: w,
        length: E[0].length
      });
    return p;
  }
  function h(_) {
    const w = d(o.NUMERIC, t.NUMERIC, _), m = d(o.ALPHANUMERIC, t.ALPHANUMERIC, _);
    let p, E;
    return a.isKanjiModeEnabled() ? (p = d(o.BYTE, t.BYTE, _), E = d(o.KANJI, t.KANJI, _)) : (p = d(o.BYTE_KANJI, t.BYTE, _), E = []), w.concat(m, p, E).sort(function(A, x) {
      return A.index - x.index;
    }).map(function(A) {
      return {
        data: A.data,
        mode: A.mode,
        length: A.length
      };
    });
  }
  function u(_, w) {
    switch (w) {
      case t.NUMERIC:
        return e.getBitsLength(_);
      case t.ALPHANUMERIC:
        return s.getBitsLength(_);
      case t.KANJI:
        return r.getBitsLength(_);
      case t.BYTE:
        return i.getBitsLength(_);
    }
  }
  function f(_) {
    return _.reduce(function(w, m) {
      const p = w.length - 1 >= 0 ? w[w.length - 1] : null;
      return p && p.mode === m.mode ? (w[w.length - 1].data += m.data, w) : (w.push(m), w);
    }, []);
  }
  function g(_) {
    const w = [];
    for (let m = 0; m < _.length; m++) {
      const p = _[m];
      switch (p.mode) {
        case t.NUMERIC:
          w.push([
            p,
            { data: p.data, mode: t.ALPHANUMERIC, length: p.length },
            { data: p.data, mode: t.BYTE, length: p.length }
          ]);
          break;
        case t.ALPHANUMERIC:
          w.push([
            p,
            { data: p.data, mode: t.BYTE, length: p.length }
          ]);
          break;
        case t.KANJI:
          w.push([
            p,
            { data: p.data, mode: t.BYTE, length: l(p.data) }
          ]);
          break;
        case t.BYTE:
          w.push([
            { data: p.data, mode: t.BYTE, length: l(p.data) }
          ]);
      }
    }
    return w;
  }
  function y(_, w) {
    const m = {}, p = { start: {} };
    let E = ["start"];
    for (let C = 0; C < _.length; C++) {
      const A = _[C], x = [];
      for (let V = 0; V < A.length; V++) {
        const D = A[V], ct = "" + C + V;
        x.push(ct), m[ct] = { node: D, lastCount: 0 }, p[ct] = {};
        for (let Lt = 0; Lt < E.length; Lt++) {
          const R = E[Lt];
          m[R] && m[R].node.mode === D.mode ? (p[R][ct] = u(m[R].lastCount + D.length, D.mode) - u(m[R].lastCount, D.mode), m[R].lastCount += D.length) : (m[R] && (m[R].lastCount = D.length), p[R][ct] = u(D.length, D.mode) + 4 + t.getCharCountIndicator(D.mode, w));
        }
      }
      E = x;
    }
    for (let C = 0; C < E.length; C++)
      p[E[C]].end = 0;
    return { map: p, table: m };
  }
  function S(_, w) {
    let m;
    const p = t.getBestModeForData(_);
    if (m = t.from(w, p), m !== t.BYTE && m.bit < p.bit)
      throw new Error('"' + _ + '" cannot be encoded with mode ' + t.toString(m) + `.
 Suggested mode is: ` + t.toString(p));
    switch (m === t.KANJI && !a.isKanjiModeEnabled() && (m = t.BYTE), m) {
      case t.NUMERIC:
        return new e(_);
      case t.ALPHANUMERIC:
        return new s(_);
      case t.KANJI:
        return new r(_);
      case t.BYTE:
        return new i(_);
    }
  }
  n.fromArray = function(w) {
    return w.reduce(function(m, p) {
      return typeof p == "string" ? m.push(S(p, null)) : p.data && m.push(S(p.data, p.mode)), m;
    }, []);
  }, n.fromString = function(w, m) {
    const p = h(w, a.isKanjiModeEnabled()), E = g(p), C = y(E, m), A = c.find_path(C.map, "start", "end"), x = [];
    for (let V = 1; V < A.length - 1; V++)
      x.push(C.table[A[V]].node);
    return n.fromArray(f(x));
  }, n.rawSplit = function(w) {
    return n.fromArray(
      h(w, a.isKanjiModeEnabled())
    );
  };
})(Ke);
const Rt = P, Vt = xt, Vi = Ci, ji = Ai, qi = Ue, Gi = Oe, Wt = He, Jt = Dt, Ki = Si, Nt = Ve, Wi = qe, Ji = K, jt = Ke;
function Yi(n, t) {
  const e = n.size, s = Gi.getPositions(t);
  for (let i = 0; i < s.length; i++) {
    const r = s[i][0], o = s[i][1];
    for (let a = -1; a <= 7; a++)
      if (!(r + a <= -1 || e <= r + a))
        for (let c = -1; c <= 7; c++)
          o + c <= -1 || e <= o + c || (a >= 0 && a <= 6 && (c === 0 || c === 6) || c >= 0 && c <= 6 && (a === 0 || a === 6) || a >= 2 && a <= 4 && c >= 2 && c <= 4 ? n.set(r + a, o + c, !0, !0) : n.set(r + a, o + c, !1, !0));
  }
}
function Qi(n) {
  const t = n.size;
  for (let e = 8; e < t - 8; e++) {
    const s = e % 2 === 0;
    n.set(e, 6, s, !0), n.set(6, e, s, !0);
  }
}
function Zi(n, t) {
  const e = qi.getPositions(t);
  for (let s = 0; s < e.length; s++) {
    const i = e[s][0], r = e[s][1];
    for (let o = -2; o <= 2; o++)
      for (let a = -2; a <= 2; a++)
        o === -2 || o === 2 || a === -2 || a === 2 || o === 0 && a === 0 ? n.set(i + o, r + a, !0, !0) : n.set(i + o, r + a, !1, !0);
  }
}
function Xi(n, t) {
  const e = n.size, s = Nt.getEncodedBits(t);
  let i, r, o;
  for (let a = 0; a < 18; a++)
    i = Math.floor(a / 3), r = a % 3 + e - 8 - 3, o = (s >> a & 1) === 1, n.set(i, r, o, !0), n.set(r, i, o, !0);
}
function qt(n, t, e) {
  const s = n.size, i = Wi.getEncodedBits(t, e);
  let r, o;
  for (r = 0; r < 15; r++)
    o = (i >> r & 1) === 1, r < 6 ? n.set(r, 8, o, !0) : r < 8 ? n.set(r + 1, 8, o, !0) : n.set(s - 15 + r, 8, o, !0), r < 8 ? n.set(8, s - r - 1, o, !0) : r < 9 ? n.set(8, 15 - r - 1 + 1, o, !0) : n.set(8, 15 - r - 1, o, !0);
  n.set(s - 8, 8, 1, !0);
}
function ts(n, t) {
  const e = n.size;
  let s = -1, i = e - 1, r = 7, o = 0;
  for (let a = e - 1; a > 0; a -= 2)
    for (a === 6 && a--; ; ) {
      for (let c = 0; c < 2; c++)
        if (!n.isReserved(i, a - c)) {
          let l = !1;
          o < t.length && (l = (t[o] >>> r & 1) === 1), n.set(i, a - c, l), r--, r === -1 && (o++, r = 7);
        }
      if (i += s, i < 0 || e <= i) {
        i -= s, s = -s;
        break;
      }
    }
}
function es(n, t, e) {
  const s = new Vi();
  e.forEach(function(c) {
    s.put(c.mode.bit, 4), s.put(c.getLength(), Ji.getCharCountIndicator(c.mode, n)), c.write(s);
  });
  const i = Rt.getSymbolTotalCodewords(n), r = Jt.getTotalCodewordsCount(n, t), o = (i - r) * 8;
  for (s.getLengthInBits() + 4 <= o && s.put(0, 4); s.getLengthInBits() % 8 !== 0; )
    s.putBit(0);
  const a = (o - s.getLengthInBits()) / 8;
  for (let c = 0; c < a; c++)
    s.put(c % 2 ? 17 : 236, 8);
  return is(s, n, t);
}
function is(n, t, e) {
  const s = Rt.getSymbolTotalCodewords(t), i = Jt.getTotalCodewordsCount(t, e), r = s - i, o = Jt.getBlocksCount(t, e), a = s % o, c = o - a, l = Math.floor(s / o), d = Math.floor(r / o), h = d + 1, u = l - d, f = new Ki(u);
  let g = 0;
  const y = new Array(o), S = new Array(o);
  let _ = 0;
  const w = new Uint8Array(n.buffer);
  for (let A = 0; A < o; A++) {
    const x = A < c ? d : h;
    y[A] = w.slice(g, g + x), S[A] = f.encode(y[A]), g += x, _ = Math.max(_, x);
  }
  const m = new Uint8Array(s);
  let p = 0, E, C;
  for (E = 0; E < _; E++)
    for (C = 0; C < o; C++)
      E < y[C].length && (m[p++] = y[C][E]);
  for (E = 0; E < u; E++)
    for (C = 0; C < o; C++)
      m[p++] = S[C][E];
  return m;
}
function ss(n, t, e, s) {
  let i;
  if (Array.isArray(n))
    i = jt.fromArray(n);
  else if (typeof n == "string") {
    let l = t;
    if (!l) {
      const d = jt.rawSplit(n);
      l = Nt.getBestVersionForData(d, e);
    }
    i = jt.fromString(n, l || 40);
  } else
    throw new Error("Invalid data");
  const r = Nt.getBestVersionForData(i, e);
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
  const o = es(t, e, i), a = Rt.getSymbolSize(t), c = new ji(a);
  return Yi(c, t), Qi(c), Zi(c, t), qt(c, e, 0), t >= 7 && Xi(c, t), ts(c, o), isNaN(s) && (s = Wt.getBestMask(
    c,
    qt.bind(null, c, e)
  )), Wt.applyMask(s, c), qt(c, e, s), {
    modules: c,
    version: t,
    errorCorrectionLevel: e,
    maskPattern: s,
    segments: i
  };
}
Re.create = function(t, e) {
  if (typeof t > "u" || t === "")
    throw new Error("No input text");
  let s = Vt.M, i, r;
  return typeof e < "u" && (s = Vt.from(e.errorCorrectionLevel, Vt.M), i = Nt.from(e.version), r = Wt.from(e.maskPattern), e.toSJISFunc && Rt.setToSJISFunction(e.toSJISFunc)), ss(t, i, s, r);
};
var Je = {}, ne = {};
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
    const o = i.modules.size, a = i.modules.data, c = n.getScale(o, r), l = Math.floor((o + r.margin * 2) * c), d = r.margin * c, h = [r.color.light, r.color.dark];
    for (let u = 0; u < l; u++)
      for (let f = 0; f < l; f++) {
        let g = (u * l + f) * 4, y = r.color.light;
        if (u >= d && f >= d && u < l - d && f < l - d) {
          const S = Math.floor((u - d) / c), _ = Math.floor((f - d) / c);
          y = h[a[S * o + _] ? 1 : 0];
        }
        s[g++] = y.r, s[g++] = y.g, s[g++] = y.b, s[g] = y.a;
      }
  };
})(ne);
(function(n) {
  const t = ne;
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
    let c = a, l = o;
    typeof c > "u" && (!o || !o.getContext) && (c = o, o = void 0), o || (l = s()), c = t.getOptions(c);
    const d = t.getImageWidth(r.modules.size, c), h = l.getContext("2d"), u = h.createImageData(d, d);
    return t.qrToImageData(u.data, r, c), e(h, l, d), h.putImageData(u, 0, 0), l;
  }, n.renderToDataURL = function(r, o, a) {
    let c = a;
    typeof c > "u" && (!o || !o.getContext) && (c = o, o = void 0), c || (c = {});
    const l = n.render(r, o, c), d = c.type || "image/png", h = c.rendererOpts || {};
    return l.toDataURL(d, h.quality);
  };
})(Je);
var Ye = {};
const ns = ne;
function ke(n, t) {
  const e = n.a / 255, s = t + '="' + n.hex + '"';
  return e < 1 ? s + " " + t + '-opacity="' + e.toFixed(2).slice(1) + '"' : s;
}
function Gt(n, t, e) {
  let s = n + t;
  return typeof e < "u" && (s += " " + e), s;
}
function rs(n, t, e) {
  let s = "", i = 0, r = !1, o = 0;
  for (let a = 0; a < n.length; a++) {
    const c = Math.floor(a % t), l = Math.floor(a / t);
    !c && !r && (r = !0), n[a] ? (o++, a > 0 && c > 0 && n[a - 1] || (s += r ? Gt("M", c + e, 0.5 + l + e) : Gt("m", i, 0), i = 0, r = !1), c + 1 < t && n[a + 1] || (s += Gt("h", o), o = 0)) : i++;
  }
  return s;
}
Ye.render = function(t, e, s) {
  const i = ns.getOptions(e), r = t.modules.size, o = t.modules.data, a = r + i.margin * 2, c = i.color.light.a ? "<path " + ke(i.color.light, "fill") + ' d="M0 0h' + a + "v" + a + 'H0z"/>' : "", l = "<path " + ke(i.color.dark, "stroke") + ' d="' + rs(o, r, i.margin) + '"/>', d = 'viewBox="0 0 ' + a + " " + a + '"', u = '<svg xmlns="http://www.w3.org/2000/svg" ' + (i.width ? 'width="' + i.width + '" height="' + i.width + '" ' : "") + d + ' shape-rendering="crispEdges">' + c + l + `</svg>
`;
  return typeof s == "function" && s(null, u), u;
};
const os = bi, Yt = Re, Qe = Je, as = Ye;
function re(n, t, e, s, i) {
  const r = [].slice.call(arguments, 1), o = r.length, a = typeof r[o - 1] == "function";
  if (!a && !os())
    throw new Error("Callback required as last argument");
  if (a) {
    if (o < 2)
      throw new Error("Too few arguments provided");
    o === 2 ? (i = e, e = t, t = s = void 0) : o === 3 && (t.getContext && typeof i > "u" ? (i = s, s = void 0) : (i = s, s = e, e = t, t = void 0));
  } else {
    if (o < 1)
      throw new Error("Too few arguments provided");
    return o === 1 ? (e = t, t = s = void 0) : o === 2 && !t.getContext && (s = e, e = t, t = void 0), new Promise(function(c, l) {
      try {
        const d = Yt.create(e, s);
        c(n(d, t, s));
      } catch (d) {
        l(d);
      }
    });
  }
  try {
    const c = Yt.create(e, s);
    i(null, n(c, t, s));
  } catch (c) {
    i(c);
  }
}
bt.create = Yt.create;
bt.toCanvas = re.bind(null, Qe.render);
bt.toDataURL = re.bind(null, Qe.renderToDataURL);
bt.toString = re.bind(null, function(n, t, e) {
  return as.render(n, e);
});
class T {
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
    const o = parseInt(s, 10), a = e.find((d) => {
      const h = !i || d.networkId === i;
      return isNaN(o) ? d.name === s && h : d.number === o && h;
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
    const l = (a ? a.name : s).toLowerCase().replace(/[^a-z0-9]/g, "_");
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
    const s = this.escapeWifiString(t), i = e ? this.escapeWifiString(e) : "";
    return i ? `WIFI:T:WPA;S:${s};P:${i};;` : `WIFI:T:nopass;S:${s};P:;;`;
  }
  /**
   * Generates an SVG QR code from a string.
   */
  static async generateQrSvg(t, e = 1) {
    try {
      return await bt.toString(t, {
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
var cs = Object.defineProperty, W = (n, t, e, s) => {
  for (var i = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = o(t, e, i) || i);
  return i && cs(t, e, i), i;
};
const oe = class oe extends M {
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
    this.hass && await L.pollConfig(
      this.hass,
      (t, e) => {
        this._loadingMessage = t, this._isLoading = e;
      }
    );
  }
  _discoverEntity() {
    if (this.hass)
      return Object.keys(this.hass.states).find((t) => {
        var i;
        if (!t.startsWith("select.")) return !1;
        const s = ((i = this.hass.states[t].attributes.friendly_name) == null ? void 0 : i.toLowerCase()) || "";
        return t.includes("content_filter") || s.includes("content filter") || t.includes("meraki");
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
      return Mt(
        ((l = this._config) == null ? void 0 : l.name) || "Cisco Meraki Content Filter",
        this._loadingMessage,
        "2.3.0-beta.3524"
      );
    const t = this._config.entity || this._discoverEntity(), e = t ? this.hass.states[t] : void 0, s = this._config.entity ? this.hass.states[this._config.entity] : void 0, i = ((d = s == null ? void 0 : s.attributes) == null ? void 0 : d.friendly_name) || "Cisco Meraki", r = this._config.name || (this._config.entity ? `${i} Content Filter` : "Cisco Meraki Content Filter");
    if (!t || !e)
      return De(
        "Entity Missing",
        "No content filter entity was found. Please check your configuration.",
        "2.3.0-beta.3524"
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
        <div class="version">v${"2.3.0-beta.3524"}</div>
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
      } catch (s) {
        console.error("Failed to call select_option service:", s), this._optimisticProfile = null, this._isUpdating = !1;
      }
    }
  }
};
oe.styles = [
  It,
  F`
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
let U = oe;
W([
  z({ attribute: !1 })
], U.prototype, "hass");
W([
  v()
], U.prototype, "_config");
W([
  v()
], U.prototype, "_optimisticProfile");
W([
  v()
], U.prototype, "_isUpdating");
W([
  v()
], U.prototype, "_isLoading");
W([
  v()
], U.prototype, "_loadingMessage");
const ae = class ae extends M {
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
ae.styles = F`
    .editor-container { padding: 16px; }
  `;
let _t = ae;
W([
  z({ attribute: !1 })
], _t.prototype, "hass");
W([
  v()
], _t.prototype, "_config");
customElements.get("meraki-content-filter-card") || customElements.define("meraki-content-filter-card", U);
customElements.get("meraki-content-filter-card-editor") || customElements.define("meraki-content-filter-card-editor", _t);
window.customCards = window.customCards || [];
window.customCards.some((n) => n.type === "meraki-content-filter-card") || window.customCards.push({
  type: "meraki-content-filter-card",
  name: "Cisco Meraki Content Filter",
  description: "Control Cisco Meraki Content Filtering profiles.",
  preview: !0
});
var ls = Object.defineProperty, I = (n, t, e, s) => {
  for (var i = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = o(t, e, i) || i);
  return i && ls(t, e, i), i;
};
const ce = class ce extends M {
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
    const { networks: t, ssids: e } = await L.pollConfig(
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
    }), this.dispatchEvent(new CustomEvent("config-changed", { detail: { config: s }, bubbles: !0, composed: !0 }));
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
    const t = L.getNetworkOptions(this._networks, !0), e = L.getSsidOptions(this._ssids, this._config.networkId, "name"), s = [
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
          .schema=${s}
          .computeLabel=${this._computeLabel}
          @value-changed=${this._valueChanged}
        ></ha-form>
      </div>
    `;
  }
};
ce.styles = F`.editor-container { padding: 16px; }`;
let O = ce;
I([
  z({ attribute: !1 })
], O.prototype, "hass");
I([
  v()
], O.prototype, "_config");
I([
  v()
], O.prototype, "_networks");
I([
  v()
], O.prototype, "_ssids");
I([
  v()
], O.prototype, "_isLoading");
I([
  v()
], O.prototype, "_loadingMessage");
const le = class le extends M {
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
    const { ssids: t } = await L.pollConfig(
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
    const t = T.getValue(this.hass, this._config.ssid), e = T.getPasswordForSsid(
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
    const s = T.generateWifiQrString(t, e);
    this._qrSvg = await T.generateQrSvg(s, 2);
  }
  render() {
    var s;
    if (!this._config || !this.hass) return b``;
    if (this._isLoading)
      return Mt(
        ((s = this._config) == null ? void 0 : s.name) || "Wi-Fi Access",
        this._loadingMessage,
        "2.3.0-beta.3524"
      );
    const t = T.getValue(this.hass, this._config.ssid), e = T.getPasswordForSsid(
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
        <div class="version">v${"2.3.0-beta.3524"}</div>
      </ha-card>
    `;
  }
};
le.styles = [
  It,
  F`
      :host { display: block; }
      .card-content { padding: 16px; gap: 16px; }
      .ssid-display { font-size: 1.5em; font-weight: bold; color: var(--primary-text-color); text-align: center; }
      .password-display { color: var(--secondary-text-color); text-align: center; }
    `
];
let H = le;
I([
  z({ attribute: !1 })
], H.prototype, "hass");
I([
  v()
], H.prototype, "_config");
I([
  v()
], H.prototype, "_qrSvg");
I([
  v()
], H.prototype, "_isLoading");
I([
  v()
], H.prototype, "_loadingMessage");
I([
  v()
], H.prototype, "_ssids");
customElements.get("meraki-wifi-qr-card") || customElements.define("meraki-wifi-qr-card", H);
customElements.get("meraki-wifi-qr-card-editor") || customElements.define("meraki-wifi-qr-card-editor", O);
window.customCards = window.customCards || [];
window.customCards.some((n) => n.type === "meraki-wifi-qr-card") || window.customCards.push({
  type: "meraki-wifi-qr-card",
  name: "Cisco Meraki Wi-Fi QR Card",
  description: "Display a scannable Wi-Fi QR code for guests.",
  preview: !0
});
var ds = Object.defineProperty, at = (n, t, e, s) => {
  for (var i = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = o(t, e, i) || i);
  return i && ds(t, e, i), i;
};
const de = class de extends M {
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
    this.hass && await L.pollConfig(
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
      return Mt(
        ((i = this._config) == null ? void 0 : i.name) || "Cisco Meraki Network Vitals",
        this._loadingMessage,
        "2.3.0-beta.3524"
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
        <div class="version">v${"2.3.0-beta.3524"}</div>
      </ha-card>
    `;
  }
};
de.styles = [
  It,
  F`
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
let X = de;
at([
  z({ attribute: !1 })
], X.prototype, "hass");
at([
  v()
], X.prototype, "_config");
at([
  v()
], X.prototype, "_isLoading");
at([
  v()
], X.prototype, "_loadingMessage");
const he = class he extends M {
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
    s && s.endsWith("_tap_action") && (i.startsWith("/") ? i = { action: "navigate", navigation_path: i } : i = { action: i });
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
he.styles = F`
    ha-textfield,
    ha-entity-picker {
      display: block;
      margin-bottom: 16px;
      width: 100%;
    }
  `;
let yt = he;
at([
  z({ attribute: !1 })
], yt.prototype, "hass");
at([
  v()
], yt.prototype, "_config");
customElements.get("meraki-network-vitals-card") || customElements.define("meraki-network-vitals-card", X);
customElements.get("meraki-network-vitals-card-editor") || customElements.define(
  "meraki-network-vitals-card-editor",
  yt
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
var hs = Object.defineProperty, Ze = (n, t, e, s) => {
  for (var i = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = o(t, e, i) || i);
  return i && hs(t, e, i), i;
};
const ue = class ue extends M {
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
ue.styles = F`
    .editor-container { padding: 16px; }
  `;
let wt = ue;
Ze([
  z({ attribute: !1 })
], wt.prototype, "hass");
Ze([
  v()
], wt.prototype, "_config");
customElements.get("meraki-guest-access-card-editor") || customElements.define("meraki-guest-access-card-editor", wt);
var us = Object.defineProperty, N = (n, t, e, s) => {
  for (var i = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (i = o(t, e, i) || i);
  return i && us(t, e, i), i;
};
const fe = class fe extends M {
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
    var s, i;
    const t = ((i = (s = this.hass) == null ? void 0 : s.user) == null ? void 0 : i.name) || "Home Assistant", e = Math.floor(Math.random() * 1e4).toString().padStart(4, "0");
    return `${t} - Guest ${e}`;
  }
  async _loadCentralizedData() {
    var l;
    if (!this.hass) return;
    const { networks: t, ssids: e, groupPolicies: s, entryId: i } = await L.pollConfig(this.hass, (d, h) => {
      this._loadingMessage = d, this._isLoading = h;
    });
    if (t.length === 0) {
      this._isLoading = !1;
      return;
    }
    this._networks = t, this._ssids = e, this._policies = s, this._configEntryId = ((l = this._config) == null ? void 0 : l.config_entry_id) || i;
    let r = this._formData.network, o = this._formData.ssid, a = this._formData.passphrase, c = this._formData.policy;
    if (t.length > 0 && !r && (r = t[0].id), r && !o) {
      const d = e.filter((h) => h.networkId === r);
      d.length > 0 && (o = String(d[0].number));
    }
    if (r && o && !a && (a = T.getPasswordForSsid(this.hass, this._ssids, o, r), a || (a = T.generateNaturalPassword())), r && !c) {
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
    const e = t.detail.value, s = this._formData.network;
    let i = { ...this._formData, ...e };
    if (i.network !== s) {
      i.ssid = "", i.passphrase = "", i.policy = "";
      const r = this._ssids.filter(
        (a) => a.networkId === i.network
      );
      r.length > 0 && (i.ssid = String(r[0].number));
      const o = this._policies.filter(
        (a) => a.networkId === i.network
      );
      o.length > 0 && (i.policy = String(
        o[0].groupPolicyId || o[0].id
      ));
    }
    !i.passphrase && i.network && i.ssid && (i.passphrase = T.getPasswordForSsid(
      this.hass,
      this._ssids,
      i.ssid,
      i.network
    ) || T.generateNaturalPassword()), this._formData = i;
  }
  render() {
    var o, a, c;
    if (this._isLoading)
      return Mt(
        ((o = this._config) == null ? void 0 : o.name) || "Cisco Meraki Guest Access",
        this._loadingMessage,
        "2.3.0-beta.3524"
      );
    if (this._networks.length === 0)
      return De(
        "No Wireless Networks",
        "No Cisco Meraki wireless networks found. Ensure the integration is configured.",
        "2.3.0-beta.3524"
      );
    const t = L.getNetworkOptions(
      this._networks
    ), e = L.getSsidOptions(
      this._ssids,
      this._formData.network,
      "number"
    ), s = this._policies.filter((l) => l.networkId === this._formData.network).map((l) => ({
      value: String(l.groupPolicyId || l.id),
      label: l.name
    })), i = [
      {
        name: "network",
        selector: { select: { options: t, mode: "dropdown" } }
      },
      {
        name: "ssid",
        selector: { select: { options: e, mode: "dropdown" } }
      },
      ...s.length > 0 ? [
        {
          name: "policy",
          selector: {
            select: { options: s, mode: "dropdown" }
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
          <div class="version">v${"2.3.0-beta.3524"}</div>
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
              .schema=${i}
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
        <div class="version">v${"2.3.0-beta.3524"}</div>
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
        const e = parseInt(this._formData.ssid, 10), s = this._ssids.find(
          (a) => a.networkId === this._formData.network && a.number === e
        ), i = s ? s.name : "Guest WiFi", r = this._formData.passphrase, o = T.generateWifiQrString(i, r);
        this._qrSvg = await T.generateQrSvg(o), this._success = "Guest access key created successfully!";
      } catch (t) {
        this._error = `Failed to create guest key: ${t.message || t}`;
      } finally {
        this._creating = !1;
      }
    }
  }
};
fe.styles = [
  It,
  F`
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
let k = fe;
N([
  z({ attribute: !1 })
], k.prototype, "hass");
N([
  v()
], k.prototype, "_config");
N([
  v()
], k.prototype, "_formData");
N([
  v()
], k.prototype, "_networks");
N([
  v()
], k.prototype, "_ssids");
N([
  v()
], k.prototype, "_policies");
N([
  v()
], k.prototype, "_creating");
N([
  v()
], k.prototype, "_error");
N([
  v()
], k.prototype, "_success");
N([
  v()
], k.prototype, "_qrSvg");
N([
  v()
], k.prototype, "_isLoading");
N([
  v()
], k.prototype, "_loadingMessage");
N([
  v()
], k.prototype, "_configEntryId");
customElements.get("meraki-guest-access-card") || customElements.define("meraki-guest-access-card", k);
window.customCards = window.customCards || [];
window.customCards.some(
  (n) => n.type === "meraki-guest-access-card"
) || window.customCards.push({
  type: "meraki-guest-access-card",
  name: "Cisco Meraki Guest Access",
  description: "Manage temporary guest WiFi access. Version: 2.3.0-beta.3524",
  preview: !0,
  version: "2.3.0-beta.3524"
});
export {
  k as MerakiGuestAccessCard
};
