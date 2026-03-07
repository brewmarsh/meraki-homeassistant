/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const j = globalThis, J = j.ShadowRoot && (j.ShadyCSS === void 0 || j.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, Y = Symbol(), it = /* @__PURE__ */ new WeakMap();
let mt = class {
  constructor(t, e, i) {
    if (this._$cssResult$ = !0, i !== Y) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = t, this.t = e;
  }
  get styleSheet() {
    let t = this.o;
    const e = this.t;
    if (J && t === void 0) {
      const i = e !== void 0 && e.length === 1;
      i && (t = it.get(e)), t === void 0 && ((this.o = t = new CSSStyleSheet()).replaceSync(this.cssText), i && it.set(e, t));
    }
    return t;
  }
  toString() {
    return this.cssText;
  }
};
const At = (r) => new mt(typeof r == "string" ? r : r + "", void 0, Y), Z = (r, ...t) => {
  const e = r.length === 1 ? r[0] : t.reduce((i, s, o) => i + ((n) => {
    if (n._$cssResult$ === !0) return n.cssText;
    if (typeof n == "number") return n;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + n + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(s) + r[o + 1], r[0]);
  return new mt(e, r, Y);
}, St = (r, t) => {
  if (J) r.adoptedStyleSheets = t.map((e) => e instanceof CSSStyleSheet ? e : e.styleSheet);
  else for (const e of t) {
    const i = document.createElement("style"), s = j.litNonce;
    s !== void 0 && i.setAttribute("nonce", s), i.textContent = e.cssText, r.appendChild(i);
  }
}, rt = J ? (r) => r : (r) => r instanceof CSSStyleSheet ? ((t) => {
  let e = "";
  for (const i of t.cssRules) e += i.cssText;
  return At(e);
})(r) : r;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: bt, defineProperty: Et, getOwnPropertyDescriptor: kt, getOwnPropertyNames: xt, getOwnPropertySymbols: Pt, getPrototypeOf: Ct } = Object, v = globalThis, ot = v.trustedTypes, Nt = ot ? ot.emptyScript : "", B = v.reactiveElementPolyfillSupport, N = (r, t) => r, z = { toAttribute(r, t) {
  switch (t) {
    case Boolean:
      r = r ? Nt : null;
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
} }, Q = (r, t) => !bt(r, t), nt = { attribute: !0, type: String, converter: z, reflect: !1, useDefault: !1, hasChanged: Q };
Symbol.metadata ?? (Symbol.metadata = Symbol("metadata")), v.litPropertyMetadata ?? (v.litPropertyMetadata = /* @__PURE__ */ new WeakMap());
let k = class extends HTMLElement {
  static addInitializer(t) {
    this._$Ei(), (this.l ?? (this.l = [])).push(t);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(t, e = nt) {
    if (e.state && (e.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(t) && ((e = Object.create(e)).wrapped = !0), this.elementProperties.set(t, e), !e.noAccessor) {
      const i = Symbol(), s = this.getPropertyDescriptor(t, i, e);
      s !== void 0 && Et(this.prototype, t, s);
    }
  }
  static getPropertyDescriptor(t, e, i) {
    const { get: s, set: o } = kt(this.prototype, t) ?? { get() {
      return this[e];
    }, set(n) {
      this[e] = n;
    } };
    return { get: s, set(n) {
      const c = s == null ? void 0 : s.call(this);
      o == null || o.call(this, n), this.requestUpdate(t, c, i);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(t) {
    return this.elementProperties.get(t) ?? nt;
  }
  static _$Ei() {
    if (this.hasOwnProperty(N("elementProperties"))) return;
    const t = Ct(this);
    t.finalize(), t.l !== void 0 && (this.l = [...t.l]), this.elementProperties = new Map(t.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(N("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(N("properties"))) {
      const e = this.properties, i = [...xt(e), ...Pt(e)];
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
      for (const s of i) e.unshift(rt(s));
    } else t !== void 0 && e.push(rt(t));
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
    return St(t, this.constructor.elementStyles), t;
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
    var o;
    const i = this.constructor.elementProperties.get(t), s = this.constructor._$Eu(t, i);
    if (s !== void 0 && i.reflect === !0) {
      const n = (((o = i.converter) == null ? void 0 : o.toAttribute) !== void 0 ? i.converter : z).toAttribute(e, i.type);
      this._$Em = t, n == null ? this.removeAttribute(s) : this.setAttribute(s, n), this._$Em = null;
    }
  }
  _$AK(t, e) {
    var o, n;
    const i = this.constructor, s = i._$Eh.get(t);
    if (s !== void 0 && this._$Em !== s) {
      const c = i.getPropertyOptions(s), a = typeof c.converter == "function" ? { fromAttribute: c.converter } : ((o = c.converter) == null ? void 0 : o.fromAttribute) !== void 0 ? c.converter : z;
      this._$Em = s;
      const h = a.fromAttribute(e, c.type);
      this[s] = h ?? ((n = this._$Ej) == null ? void 0 : n.get(s)) ?? h, this._$Em = null;
    }
  }
  requestUpdate(t, e, i, s = !1, o) {
    var n;
    if (t !== void 0) {
      const c = this.constructor;
      if (s === !1 && (o = this[t]), i ?? (i = c.getPropertyOptions(t)), !((i.hasChanged ?? Q)(o, e) || i.useDefault && i.reflect && o === ((n = this._$Ej) == null ? void 0 : n.get(t)) && !this.hasAttribute(c._$Eu(t, i)))) return;
      this.C(t, e, i);
    }
    this.isUpdatePending === !1 && (this._$ES = this._$EP());
  }
  C(t, e, { useDefault: i, reflect: s, wrapped: o }, n) {
    i && !(this._$Ej ?? (this._$Ej = /* @__PURE__ */ new Map())).has(t) && (this._$Ej.set(t, n ?? e ?? this[t]), o !== !0 || n !== void 0) || (this._$AL.has(t) || (this.hasUpdated || i || (e = void 0), this._$AL.set(t, e)), s === !0 && this._$Em !== t && (this._$Eq ?? (this._$Eq = /* @__PURE__ */ new Set())).add(t));
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
        for (const [o, n] of this._$Ep) this[o] = n;
        this._$Ep = void 0;
      }
      const s = this.constructor.elementProperties;
      if (s.size > 0) for (const [o, n] of s) {
        const { wrapped: c } = n, a = this[o];
        c !== !0 || this._$AL.has(o) || a === void 0 || this.C(o, void 0, n, a);
      }
    }
    let t = !1;
    const e = this._$AL;
    try {
      t = this.shouldUpdate(e), t ? (this.willUpdate(e), (i = this._$EO) == null || i.forEach((s) => {
        var o;
        return (o = s.hostUpdate) == null ? void 0 : o.call(s);
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
k.elementStyles = [], k.shadowRootOptions = { mode: "open" }, k[N("elementProperties")] = /* @__PURE__ */ new Map(), k[N("finalized")] = /* @__PURE__ */ new Map(), B == null || B({ ReactiveElement: k }), (v.reactiveElementVersions ?? (v.reactiveElementVersions = [])).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const M = globalThis, at = (r) => r, L = M.trustedTypes, ct = L ? L.createPolicy("lit-html", { createHTML: (r) => r }) : void 0, $t = "$lit$", y = `lit$${Math.random().toFixed(9).slice(2)}$`, gt = "?" + y, Mt = `<${gt}>`, E = document, O = () => E.createComment(""), D = (r) => r === null || typeof r != "object" && typeof r != "function", X = Array.isArray, Ot = (r) => X(r) || typeof (r == null ? void 0 : r[Symbol.iterator]) == "function", F = `[
\f\r]`, C = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, lt = /-->/g, ht = />/g, w = RegExp(`>|${F}(?:([^\\s"'>=/]+)(${F}*=${F}*(?:[^
\f\r"'\`<>=]|("|')|))|$)`, "g"), dt = /'/g, ut = /"/g, yt = /^(?:script|style|textarea|title)$/i, Dt = (r) => (t, ...e) => ({ _$litType$: r, strings: t, values: e }), m = Dt(1), x = Symbol.for("lit-noChange"), u = Symbol.for("lit-nothing"), pt = /* @__PURE__ */ new WeakMap(), A = E.createTreeWalker(E, 129);
function vt(r, t) {
  if (!X(r) || !r.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return ct !== void 0 ? ct.createHTML(t) : t;
}
const Tt = (r, t) => {
  const e = r.length - 1, i = [];
  let s, o = t === 2 ? "<svg>" : t === 3 ? "<math>" : "", n = C;
  for (let c = 0; c < e; c++) {
    const a = r[c];
    let h, _, l = -1, $ = 0;
    for (; $ < a.length && (n.lastIndex = $, _ = n.exec(a), _ !== null); ) $ = n.lastIndex, n === C ? _[1] === "!--" ? n = lt : _[1] !== void 0 ? n = ht : _[2] !== void 0 ? (yt.test(_[2]) && (s = RegExp("</" + _[2], "g")), n = w) : _[3] !== void 0 && (n = w) : n === w ? _[0] === ">" ? (n = s ?? C, l = -1) : _[1] === void 0 ? l = -2 : (l = n.lastIndex - _[2].length, h = _[1], n = _[3] === void 0 ? w : _[3] === '"' ? ut : dt) : n === ut || n === dt ? n = w : n === lt || n === ht ? n = C : (n = w, s = void 0);
    const g = n === w && r[c + 1].startsWith("/>") ? " " : "";
    o += n === C ? a + Mt : l >= 0 ? (i.push(h), a.slice(0, l) + $t + a.slice(l) + y + g) : a + y + (l === -2 ? c : g);
  }
  return [vt(r, o + (r[e] || "<?>") + (t === 2 ? "</svg>" : t === 3 ? "</math>" : "")), i];
};
class T {
  constructor({ strings: t, _$litType$: e }, i) {
    let s;
    this.parts = [];
    let o = 0, n = 0;
    const c = t.length - 1, a = this.parts, [h, _] = Tt(t, e);
    if (this.el = T.createElement(h, i), A.currentNode = this.el.content, e === 2 || e === 3) {
      const l = this.el.content.firstChild;
      l.replaceWith(...l.childNodes);
    }
    for (; (s = A.nextNode()) !== null && a.length < c; ) {
      if (s.nodeType === 1) {
        if (s.hasAttributes()) for (const l of s.getAttributeNames()) if (l.endsWith($t)) {
          const $ = _[n++], g = s.getAttribute(l).split(y), R = /([.?@])?(.*)/.exec($);
          a.push({ type: 1, index: o, name: R[2], strings: g, ctor: R[1] === "." ? It : R[1] === "?" ? Ht : R[1] === "@" ? Rt : G }), s.removeAttribute(l);
        } else l.startsWith(y) && (a.push({ type: 6, index: o }), s.removeAttribute(l));
        if (yt.test(s.tagName)) {
          const l = s.textContent.split(y), $ = l.length - 1;
          if ($ > 0) {
            s.textContent = L ? L.emptyScript : "";
            for (let g = 0; g < $; g++) s.append(l[g], O()), A.nextNode(), a.push({ type: 2, index: ++o });
            s.append(l[$], O());
          }
        }
      } else if (s.nodeType === 8) if (s.data === gt) a.push({ type: 2, index: o });
      else {
        let l = -1;
        for (; (l = s.data.indexOf(y, l + 1)) !== -1; ) a.push({ type: 7, index: o }), l += y.length - 1;
      }
      o++;
    }
  }
  static createElement(t, e) {
    const i = E.createElement("template");
    return i.innerHTML = t, i;
  }
}
function P(r, t, e = r, i) {
  var n, c;
  if (t === x) return t;
  let s = i !== void 0 ? (n = e._$Co) == null ? void 0 : n[i] : e._$Cl;
  const o = D(t) ? void 0 : t._$litDirective$;
  return (s == null ? void 0 : s.constructor) !== o && ((c = s == null ? void 0 : s._$AO) == null || c.call(s, !1), o === void 0 ? s = void 0 : (s = new o(r), s._$AT(r, e, i)), i !== void 0 ? (e._$Co ?? (e._$Co = []))[i] = s : e._$Cl = s), s !== void 0 && (t = P(r, s._$AS(r, t.values), s, i)), t;
}
class Ut {
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
    const { el: { content: e }, parts: i } = this._$AD, s = ((t == null ? void 0 : t.creationScope) ?? E).importNode(e, !0);
    A.currentNode = s;
    let o = A.nextNode(), n = 0, c = 0, a = i[0];
    for (; a !== void 0; ) {
      if (n === a.index) {
        let h;
        a.type === 2 ? h = new H(o, o.nextSibling, this, t) : a.type === 1 ? h = new a.ctor(o, a.name, a.strings, this, t) : a.type === 6 && (h = new jt(o, this, t)), this._$AV.push(h), a = i[++c];
      }
      n !== (a == null ? void 0 : a.index) && (o = A.nextNode(), n++);
    }
    return A.currentNode = E, s;
  }
  p(t) {
    let e = 0;
    for (const i of this._$AV) i !== void 0 && (i.strings !== void 0 ? (i._$AI(t, i, e), e += i.strings.length - 2) : i._$AI(t[e])), e++;
  }
}
class H {
  get _$AU() {
    var t;
    return ((t = this._$AM) == null ? void 0 : t._$AU) ?? this._$Cv;
  }
  constructor(t, e, i, s) {
    this.type = 2, this._$AH = u, this._$AN = void 0, this._$AA = t, this._$AB = e, this._$AM = i, this.options = s, this._$Cv = (s == null ? void 0 : s.isConnected) ?? !0;
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
    t = P(this, t, e), D(t) ? t === u || t == null || t === "" ? (this._$AH !== u && this._$AR(), this._$AH = u) : t !== this._$AH && t !== x && this._(t) : t._$litType$ !== void 0 ? this.$(t) : t.nodeType !== void 0 ? this.T(t) : Ot(t) ? this.k(t) : this._(t);
  }
  O(t) {
    return this._$AA.parentNode.insertBefore(t, this._$AB);
  }
  T(t) {
    this._$AH !== t && (this._$AR(), this._$AH = this.O(t));
  }
  _(t) {
    this._$AH !== u && D(this._$AH) ? this._$AA.nextSibling.data = t : this.T(E.createTextNode(t)), this._$AH = t;
  }
  $(t) {
    var o;
    const { values: e, _$litType$: i } = t, s = typeof i == "number" ? this._$AC(t) : (i.el === void 0 && (i.el = T.createElement(vt(i.h, i.h[0]), this.options)), i);
    if (((o = this._$AH) == null ? void 0 : o._$AD) === s) this._$AH.p(e);
    else {
      const n = new Ut(s, this), c = n.u(this.options);
      n.p(e), this.T(c), this._$AH = n;
    }
  }
  _$AC(t) {
    let e = pt.get(t.strings);
    return e === void 0 && pt.set(t.strings, e = new T(t)), e;
  }
  k(t) {
    X(this._$AH) || (this._$AH = [], this._$AR());
    const e = this._$AH;
    let i, s = 0;
    for (const o of t) s === e.length ? e.push(i = new H(this.O(O()), this.O(O()), this, this.options)) : i = e[s], i._$AI(o), s++;
    s < e.length && (this._$AR(i && i._$AB.nextSibling, s), e.length = s);
  }
  _$AR(t = this._$AA.nextSibling, e) {
    var i;
    for ((i = this._$AP) == null ? void 0 : i.call(this, !1, !0, e); t !== this._$AB; ) {
      const s = at(t).nextSibling;
      at(t).remove(), t = s;
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
  constructor(t, e, i, s, o) {
    this.type = 1, this._$AH = u, this._$AN = void 0, this.element = t, this.name = e, this._$AM = s, this.options = o, i.length > 2 || i[0] !== "" || i[1] !== "" ? (this._$AH = Array(i.length - 1).fill(new String()), this.strings = i) : this._$AH = u;
  }
  _$AI(t, e = this, i, s) {
    const o = this.strings;
    let n = !1;
    if (o === void 0) t = P(this, t, e, 0), n = !D(t) || t !== this._$AH && t !== x, n && (this._$AH = t);
    else {
      const c = t;
      let a, h;
      for (t = o[0], a = 0; a < o.length - 1; a++) h = P(this, c[i + a], e, a), h === x && (h = this._$AH[a]), n || (n = !D(h) || h !== this._$AH[a]), h === u ? t = u : t !== u && (t += (h ?? "") + o[a + 1]), this._$AH[a] = h;
    }
    n && !s && this.j(t);
  }
  j(t) {
    t === u ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, t ?? "");
  }
}
class It extends G {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(t) {
    this.element[this.name] = t === u ? void 0 : t;
  }
}
class Ht extends G {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(t) {
    this.element.toggleAttribute(this.name, !!t && t !== u);
  }
}
class Rt extends G {
  constructor(t, e, i, s, o) {
    super(t, e, i, s, o), this.type = 5;
  }
  _$AI(t, e = this) {
    if ((t = P(this, t, e, 0) ?? u) === x) return;
    const i = this._$AH, s = t === u && i !== u || t.capture !== i.capture || t.once !== i.once || t.passive !== i.passive, o = t !== u && (i === u || s);
    s && this.element.removeEventListener(this.name, this, i), o && this.element.addEventListener(this.name, this, t), this._$AH = t;
  }
  handleEvent(t) {
    var e;
    typeof this._$AH == "function" ? this._$AH.call(((e = this.options) == null ? void 0 : e.host) ?? this.element, t) : this._$AH.handleEvent(t);
  }
}
class jt {
  constructor(t, e, i) {
    this.element = t, this.type = 6, this._$AN = void 0, this._$AM = e, this.options = i;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t) {
    P(this, t);
  }
}
const W = M.litHtmlPolyfillSupport;
W == null || W(T, H), (M.litHtmlVersions ?? (M.litHtmlVersions = [])).push("3.3.2");
const zt = (r, t, e) => {
  const i = (e == null ? void 0 : e.renderBefore) ?? t;
  let s = i._$litPart$;
  if (s === void 0) {
    const o = (e == null ? void 0 : e.renderBefore) ?? null;
    i._$litPart$ = s = new H(t.insertBefore(O(), o), o, void 0, e ?? {});
  }
  return s._$AI(r), s;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const S = globalThis;
class b extends k {
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
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Do = zt(e, this.renderRoot, this.renderOptions);
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
    return x;
  }
}
var ft;
b._$litElement$ = !0, b.finalized = !0, (ft = S.litElementHydrateSupport) == null || ft.call(S, { LitElement: b });
const K = S.litElementPolyfillSupport;
K == null || K({ LitElement: b });
(S.litElementVersions ?? (S.litElementVersions = [])).push("4.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const wt = (r) => (t, e) => {
  e !== void 0 ? e.addInitializer(() => {
    customElements.define(r, t);
  }) : customElements.define(r, t);
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Lt = { attribute: !0, type: String, converter: z, reflect: !1, hasChanged: Q }, Gt = (r = Lt, t, e) => {
  const { kind: i, metadata: s } = e;
  let o = globalThis.litPropertyMetadata.get(s);
  if (o === void 0 && globalThis.litPropertyMetadata.set(s, o = /* @__PURE__ */ new Map()), i === "setter" && ((r = Object.create(r)).wrapped = !0), o.set(e.name, r), i === "accessor") {
    const { name: n } = e;
    return { set(c) {
      const a = t.get.call(this);
      t.set.call(this, c), this.requestUpdate(n, a, r, !0, c);
    }, init(c) {
      return c !== void 0 && this.C(n, void 0, r, c), c;
    } };
  }
  if (i === "setter") {
    const { name: n } = e;
    return function(c) {
      const a = this[n];
      t.call(this, c), this.requestUpdate(n, a, r, !0, c);
    };
  }
  throw Error("Unsupported decorator location: " + i);
};
function V(r) {
  return (t, e) => typeof e == "object" ? Gt(r, t, e) : ((i, s, o) => {
    const n = s.hasOwnProperty(o);
    return s.constructor.createProperty(o, i), n ? Object.getOwnPropertyDescriptor(s, o) : void 0;
  })(r, t, e);
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function p(r) {
  return V({ ...r, state: !0, attribute: !1 });
}
var Vt = Object.defineProperty, Bt = Object.getOwnPropertyDescriptor, tt = (r, t, e, i) => {
  for (var s = i > 1 ? void 0 : i ? Bt(t, e) : t, o = r.length - 1, n; o >= 0; o--)
    (n = r[o]) && (s = (i ? n(t, e, s) : n(s)) || s);
  return i && s && Vt(t, e, s), s;
};
let U = class extends b {
  setConfig(r) {
    if (!r || !r.entity)
      throw new Error("Please define a Meraki content filter entity");
    this._config = r;
  }
  static getStubConfig() {
    return {
      entity: "select.meraki_network_content_filter",
      name: "Meraki Content Filter"
    };
  }
  render() {
    if (!this._config || !this.hass)
      return m``;
    const r = this._config.entity, t = this.hass.states[r];
    if (!t)
      return m`
        <ha-card>
          <div class="card-content">
            <ha-alert alert-type="error">Entity not found: ${r}</ha-alert>
          </div>
        </ha-card>
      `;
    const e = t.state, i = t.attributes.options || ["None", "Security", "Family", "Strict"], s = this._config.name || t.attributes.friendly_name || "Content Filter";
    return m`
      <ha-card>
        <div class="card-header">${s}</div>
        <div class="card-content">
          <div class="current-profile">
            Current Profile: <strong>${e}</strong>
          </div>
          <div class="profile-buttons">
            ${i.map((o) => m`
              <div
                class="profile-button ${e === o ? "active" : ""}"
                @click="${() => this._handleProfileSelect(o)}"
              >
                <span class="profile-name">${o}</span>
              </div>
            `)}
          </div>
        </div>
      </ha-card>
    `;
  }
  async _handleProfileSelect(r) {
    if (!(!this.hass || !this._config))
      try {
        await this.hass.callService("select", "select_option", {
          entity_id: this._config.entity,
          option: r
        });
      } catch (t) {
        console.error("Failed to call select_option service:", t);
      }
  }
};
U.styles = Z`
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
tt([
  V({ attribute: !1 })
], U.prototype, "hass", 2);
tt([
  p()
], U.prototype, "_config", 2);
U = tt([
  wt("meraki-content-filter-card")
], U);
window.customCards = window.customCards || [];
window.customCards.push({
  type: "meraki-content-filter-card",
  name: "Meraki Content Filter",
  description: "Control Meraki Content Filtering profiles.",
  preview: !0
});
var Ft = Object.defineProperty, Wt = Object.getOwnPropertyDescriptor, et = (r, t, e, i) => {
  for (var s = i > 1 ? void 0 : i ? Wt(t, e) : t, o = r.length - 1, n; o >= 0; o--)
    (n = r[o]) && (s = (i ? n(t, e, s) : n(s)) || s);
  return i && s && Ft(t, e, s), s;
};
let I = class extends b {
  setConfig(r) {
    if (!r)
      throw new Error("Invalid configuration");
    this._config = r;
  }
  static getStubConfig() {
    return {
      gateway_entity: "",
      switch_entity: "",
      ap_entity: "",
      throughput_entity: "",
      name: "Meraki Network Vitals"
    };
  }
  _renderStatusDot(r, t) {
    if (!r || !this.hass.states[r])
      return m`
        <div class="status-item">
          <svg height="12" width="12">
            <circle cx="6" cy="6" r="6" fill="var(--disabled-text-color)" />
          </svg>
          <span class="status-label">${t}</span>
        </div>
      `;
    const e = this.hass.states[r], i = e ? e.state.toLowerCase() : "unknown";
    let s = "var(--disabled-text-color)";
    return i === "ok" || i === "online" || i === "connected" ? s = "var(--success-color)" : i === "warning" ? s = "var(--warning-color)" : (i === "error" || i === "offline" || i === "failed") && (s = "var(--error-color)"), m`
      <div class="status-item">
        <svg height="12" width="12">
          <circle cx="6" cy="6" r="6" fill="${s}" />
        </svg>
        <span class="status-label">${t}</span>
      </div>
    `;
  }
  render() {
    if (!this._config || !this.hass)
      return m``;
    const r = this._config.throughput_entity, t = r && this.hass.states[r] ? this.hass.states[r].state + " " + (this.hass.states[r].attributes.unit_of_measurement || "") : "N/A";
    return m`
      <ha-card>
        <div class="card-content">
          <div class="vitals-container">
            <div class="status-dots">
              ${this._renderStatusDot(this._config.gateway_entity, "Gateway")}
              ${this._renderStatusDot(this._config.switch_entity, "Switches")}
              ${this._renderStatusDot(this._config.ap_entity, "APs")}
            </div>
            <div class="throughput-container">
              <ha-icon icon="mdi:swap-vertical"></ha-icon>
              <span class="throughput-value">${t}</span>
            </div>
          </div>
        </div>
      </ha-card>
    `;
  }
};
I.styles = Z`
    :host {
      display: block;
    }
    .card-content {
      padding: 12px 16px;
    }
    .vitals-container {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }
    .status-dots {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
    }
    .status-item {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-right: 16px;
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
      font-weight: 500;
      white-space: nowrap;
    }
    ha-icon {
      --mdc-icon-size: 18px;
    }
  `;
et([
  V({ attribute: !1 })
], I.prototype, "hass", 2);
et([
  p()
], I.prototype, "_config", 2);
I = et([
  wt("meraki-network-vitals-card")
], I);
window.customCards = window.customCards || [];
window.customCards.some((r) => r.type === "meraki-network-vitals-card") || window.customCards.push({
  type: "meraki-network-vitals-card",
  name: "Meraki Network Vitals",
  description: "Compact horizontal header for Meraki network health and throughput.",
  preview: !0
});
var q = /* @__PURE__ */ ((r) => (r.GET_CONFIG = "meraki_ha/get_config", r.SUBSCRIBE_MERAKI_DATA = "meraki_ha/subscribe_meraki_data", r.GET_CAMERA_STREAM_URL = "meraki_ha/get_camera_stream_url", r.GET_CAMERA_SNAPSHOT = "meraki_ha/get_camera_snapshot", r.GET_VERSION = "meraki_ha/get_version", r.GET_NETWORK_EVENTS = "meraki_ha/get_network_events", r.UPDATE_ENABLED_NETWORKS = "meraki_ha/update_enabled_networks", r.CREATE_GUEST_KEY = "meraki_ha/ipsk/create", r.GET_GUEST_KEYS = "meraki_ha/ipsk/get", r.REVOKE_GUEST_KEY = "meraki_ha/ipsk/revoke", r.TIMED_ACCESS_GET_POLICIES = "meraki_ha/timed_access/get_policies", r))(q || {});
const _t = async (r, t) => {
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
var Kt = Object.defineProperty, f = (r, t, e, i) => {
  for (var s = void 0, o = r.length - 1, n; o >= 0; o--)
    (n = r[o]) && (s = n(t, e, s) || s);
  return s && Kt(t, e, s), s;
};
const st = class st extends b {
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
        }), i = ((t = this._config) == null ? void 0 : t.config_entry_id) || (e.length > 0 ? e[0].entry_id : null);
        if (!i) {
          this._error = "Meraki integration not found. Please configure it first.", this._loading = !1;
          return;
        }
        const s = await _t(this.hass, {
          type: q.GET_CONFIG,
          config_entry_id: i
        });
        this._networks = (Array.isArray(s.networks) ? s.networks : []).filter((o) => {
          var n;
          return (n = o.productTypes) == null ? void 0 : n.includes("wireless");
        }), this._ssids = Array.isArray(s.ssids) ? s.ssids : [], this._networks.length > 0 && !this._selectedNetwork && (this._selectedNetwork = this._networks[0].id, this._fetchPolicies(this._selectedNetwork, i));
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
    var i;
    if (this.hass)
      try {
        let s = e || ((i = this._config) == null ? void 0 : i.config_entry_id);
        if (!s) {
          const n = await this.hass.callWS({
            type: "config_entries/get",
            domain: "meraki_ha"
          });
          s = n.length > 0 ? n[0].entry_id : void 0;
        }
        if (!s) return;
        const o = await _t(this.hass, {
          type: q.TIMED_ACCESS_GET_POLICIES,
          config_entry_id: s,
          network_id: t
        });
        this._policies = Array.isArray(o) ? o : (o == null ? void 0 : o.policies) || [];
      } catch (s) {
        console.error("Failed to fetch policies:", s), this._policies = [];
      }
  }
  render() {
    var e, i;
    if (this._loading && !this._networks.length)
      return m`
        <ha-card .header="${((e = this._config) == null ? void 0 : e.name) || "Meraki Guest Access"}">
          <div class="card-content flex justify-center p-8">
            <ha-circular-progress active></ha-circular-progress>
          </div>
        </ha-card>
      `;
    const t = (this._ssids || []).filter((s) => s.networkId === this._selectedNetwork);
    return m`
      <ha-card .header="${((i = this._config) == null ? void 0 : i.name) || "Meraki Guest Access"}">
        <div class="card-content">
          ${this._error ? m`
                <ha-alert alert-type="error" dismissable @alert-dismissed-clicked="${() => this._error = null}">
                  ${this._error}
                </ha-alert>
              ` : ""}
          ${this._success ? m`
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
      (s) => m`<mwc-list-item value="${String(s.id)}">${s.name}</mwc-list-item>`
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
      (s) => m`<mwc-list-item value="${String(s.number)}">${s.name} (SSID ${s.number})</mwc-list-item>`
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
      (s) => m`<mwc-list-item value="${String(s.groupPolicyId)}">${s.name}</mwc-list-item>`
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
st.styles = Z`
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
let d = st;
f([
  V({ attribute: !1 })
], d.prototype, "hass");
f([
  p()
], d.prototype, "_config");
f([
  p()
], d.prototype, "_selectedNetwork");
f([
  p()
], d.prototype, "_selectedSSID");
f([
  p()
], d.prototype, "_selectedPolicy");
f([
  p()
], d.prototype, "_selectedDuration");
f([
  p()
], d.prototype, "_customName");
f([
  p()
], d.prototype, "_customPassphrase");
f([
  p()
], d.prototype, "_creating");
f([
  p()
], d.prototype, "_error");
f([
  p()
], d.prototype, "_success");
f([
  p()
], d.prototype, "_networks");
f([
  p()
], d.prototype, "_ssids");
f([
  p()
], d.prototype, "_policies");
f([
  p()
], d.prototype, "_loading");
f([
  p()
], d.prototype, "_initDone");
customElements.get("meraki-guest-access-card") || customElements.define("meraki-guest-access-card", d);
window.customCards = window.customCards || [];
window.customCards.push({
  type: "meraki-guest-access-card",
  name: "Meraki Guest Access",
  description: "Create and manage Meraki IPSK guest access keys.",
  preview: !0
});
export {
  d as MerakiGuestAccessCard
};
