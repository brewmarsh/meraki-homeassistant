/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Ct = globalThis, Yt = Ct.ShadowRoot && (Ct.ShadyCSS === void 0 || Ct.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, Qt = Symbol(), fe = /* @__PURE__ */ new WeakMap();
let Pe = class {
  constructor(t, e, i) {
    if (this._$cssResult$ = !0, i !== Qt) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = t, this.t = e;
  }
  get styleSheet() {
    let t = this.o;
    const e = this.t;
    if (Yt && t === void 0) {
      const i = e !== void 0 && e.length === 1;
      i && (t = fe.get(e)), t === void 0 && ((this.o = t = new CSSStyleSheet()).replaceSync(this.cssText), i && fe.set(e, t));
    }
    return t;
  }
  toString() {
    return this.cssText;
  }
};
const Ze = (n) => new Pe(typeof n == "string" ? n : n + "", void 0, Qt), F = (n, ...t) => {
  const e = n.length === 1 ? n[0] : t.reduce((i, s, r) => i + ((o) => {
    if (o._$cssResult$ === !0) return o.cssText;
    if (typeof o == "number") return o;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + o + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(s) + n[r + 1], n[0]);
  return new Pe(e, n, Qt);
}, Xe = (n, t) => {
  if (Yt) n.adoptedStyleSheets = t.map((e) => e instanceof CSSStyleSheet ? e : e.styleSheet);
  else for (const e of t) {
    const i = document.createElement("style"), s = Ct.litNonce;
    s !== void 0 && i.setAttribute("nonce", s), i.textContent = e.cssText, n.appendChild(i);
  }
}, ge = Yt ? (n) => n : (n) => n instanceof CSSStyleSheet ? ((t) => {
  let e = "";
  for (const i of t.cssRules) e += i.cssText;
  return Ze(e);
})(n) : n;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: ts, defineProperty: es, getOwnPropertyDescriptor: ss, getOwnPropertyNames: is, getOwnPropertySymbols: ns, getPrototypeOf: rs } = Object, q = globalThis, pe = q.trustedTypes, os = pe ? pe.emptyScript : "", Rt = q.reactiveElementPolyfillSupport, dt = (n, t) => n, $t = { toAttribute(n, t) {
  switch (t) {
    case Boolean:
      n = n ? os : null;
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
} }, Zt = (n, t) => !ts(n, t), me = { attribute: !0, type: String, converter: $t, reflect: !1, useDefault: !1, hasChanged: Zt };
Symbol.metadata ?? (Symbol.metadata = Symbol("metadata")), q.litPropertyMetadata ?? (q.litPropertyMetadata = /* @__PURE__ */ new WeakMap());
let X = class extends HTMLElement {
  static addInitializer(t) {
    this._$Ei(), (this.l ?? (this.l = [])).push(t);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(t, e = me) {
    if (e.state && (e.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(t) && ((e = Object.create(e)).wrapped = !0), this.elementProperties.set(t, e), !e.noAccessor) {
      const i = Symbol(), s = this.getPropertyDescriptor(t, i, e);
      s !== void 0 && es(this.prototype, t, s);
    }
  }
  static getPropertyDescriptor(t, e, i) {
    const { get: s, set: r } = ss(this.prototype, t) ?? { get() {
      return this[e];
    }, set(o) {
      this[e] = o;
    } };
    return { get: s, set(o) {
      const c = s == null ? void 0 : s.call(this);
      r == null || r.call(this, o), this.requestUpdate(t, c, i);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(t) {
    return this.elementProperties.get(t) ?? me;
  }
  static _$Ei() {
    if (this.hasOwnProperty(dt("elementProperties"))) return;
    const t = rs(this);
    t.finalize(), t.l !== void 0 && (this.l = [...t.l]), this.elementProperties = new Map(t.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(dt("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(dt("properties"))) {
      const e = this.properties, i = [...is(e), ...ns(e)];
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
      for (const s of i) e.unshift(ge(s));
    } else t !== void 0 && e.push(ge(t));
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
    return Xe(t, this.constructor.elementStyles), t;
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
      const o = (((r = i.converter) == null ? void 0 : r.toAttribute) !== void 0 ? i.converter : $t).toAttribute(e, i.type);
      this._$Em = t, o == null ? this.removeAttribute(s) : this.setAttribute(s, o), this._$Em = null;
    }
  }
  _$AK(t, e) {
    var r, o;
    const i = this.constructor, s = i._$Eh.get(t);
    if (s !== void 0 && this._$Em !== s) {
      const c = i.getPropertyOptions(s), a = typeof c.converter == "function" ? { fromAttribute: c.converter } : ((r = c.converter) == null ? void 0 : r.fromAttribute) !== void 0 ? c.converter : $t;
      this._$Em = s;
      const l = a.fromAttribute(e, c.type);
      this[s] = l ?? ((o = this._$Ej) == null ? void 0 : o.get(s)) ?? l, this._$Em = null;
    }
  }
  requestUpdate(t, e, i, s = !1, r) {
    var o;
    if (t !== void 0) {
      const c = this.constructor;
      if (s === !1 && (r = this[t]), i ?? (i = c.getPropertyOptions(t)), !((i.hasChanged ?? Zt)(r, e) || i.useDefault && i.reflect && r === ((o = this._$Ej) == null ? void 0 : o.get(t)) && !this.hasAttribute(c._$Eu(t, i)))) return;
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
        const { wrapped: c } = o, a = this[r];
        c !== !0 || this._$AL.has(r) || a === void 0 || this.C(r, void 0, o, a);
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
X.elementStyles = [], X.shadowRootOptions = { mode: "open" }, X[dt("elementProperties")] = /* @__PURE__ */ new Map(), X[dt("finalized")] = /* @__PURE__ */ new Map(), Rt == null || Rt({ ReactiveElement: X }), (q.reactiveElementVersions ?? (q.reactiveElementVersions = [])).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const ht = globalThis, _e = (n) => n, St = ht.trustedTypes, ye = St ? St.createPolicy("lit-html", { createHTML: (n) => n }) : void 0, Te = "$lit$", j = `lit$${Math.random().toFixed(9).slice(2)}$`, Ne = "?" + j, as = `<${Ne}>`, Q = document, ft = () => Q.createComment(""), gt = (n) => n === null || typeof n != "object" && typeof n != "function", Xt = Array.isArray, cs = (n) => Xt(n) || typeof (n == null ? void 0 : n[Symbol.iterator]) == "function", Ut = `[ 	
\f\r]`, lt = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, we = /-->/g, ve = />/g, W = RegExp(`>|${Ut}(?:([^\\s"'>=/]+)(${Ut}*=${Ut}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`, "g"), be = /'/g, Ee = /"/g, Ie = /^(?:script|style|textarea|title)$/i, ls = (n) => (t, ...e) => ({ _$litType$: n, strings: t, values: e }), b = ls(1), tt = Symbol.for("lit-noChange"), $ = Symbol.for("lit-nothing"), Ae = /* @__PURE__ */ new WeakMap(), J = Q.createTreeWalker(Q, 129);
function Me(n, t) {
  if (!Xt(n) || !n.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return ye !== void 0 ? ye.createHTML(t) : t;
}
const ds = (n, t) => {
  const e = n.length - 1, i = [];
  let s, r = t === 2 ? "<svg>" : t === 3 ? "<math>" : "", o = lt;
  for (let c = 0; c < e; c++) {
    const a = n[c];
    let l, d, h = -1, u = 0;
    for (; u < a.length && (o.lastIndex = u, d = o.exec(a), d !== null); ) u = o.lastIndex, o === lt ? d[1] === "!--" ? o = we : d[1] !== void 0 ? o = ve : d[2] !== void 0 ? (Ie.test(d[2]) && (s = RegExp("</" + d[2], "g")), o = W) : d[3] !== void 0 && (o = W) : o === W ? d[0] === ">" ? (o = s ?? lt, h = -1) : d[1] === void 0 ? h = -2 : (h = o.lastIndex - d[2].length, l = d[1], o = d[3] === void 0 ? W : d[3] === '"' ? Ee : be) : o === Ee || o === be ? o = W : o === we || o === ve ? o = lt : (o = W, s = void 0);
    const f = o === W && n[c + 1].startsWith("/>") ? " " : "";
    r += o === lt ? a + as : h >= 0 ? (i.push(l), a.slice(0, h) + Te + a.slice(h) + j + f) : a + j + (h === -2 ? c : f);
  }
  return [Me(n, r + (n[e] || "<?>") + (t === 2 ? "</svg>" : t === 3 ? "</math>" : "")), i];
};
class pt {
  constructor({ strings: t, _$litType$: e }, i) {
    let s;
    this.parts = [];
    let r = 0, o = 0;
    const c = t.length - 1, a = this.parts, [l, d] = ds(t, e);
    if (this.el = pt.createElement(l, i), J.currentNode = this.el.content, e === 2 || e === 3) {
      const h = this.el.content.firstChild;
      h.replaceWith(...h.childNodes);
    }
    for (; (s = J.nextNode()) !== null && a.length < c; ) {
      if (s.nodeType === 1) {
        if (s.hasAttributes()) for (const h of s.getAttributeNames()) if (h.endsWith(Te)) {
          const u = d[o++], f = s.getAttribute(h).split(j), g = /([.?@])?(.*)/.exec(u);
          a.push({ type: 1, index: r, name: g[2], strings: f, ctor: g[1] === "." ? us : g[1] === "?" ? fs : g[1] === "@" ? gs : Tt }), s.removeAttribute(h);
        } else h.startsWith(j) && (a.push({ type: 6, index: r }), s.removeAttribute(h));
        if (Ie.test(s.tagName)) {
          const h = s.textContent.split(j), u = h.length - 1;
          if (u > 0) {
            s.textContent = St ? St.emptyScript : "";
            for (let f = 0; f < u; f++) s.append(h[f], ft()), J.nextNode(), a.push({ type: 2, index: ++r });
            s.append(h[u], ft());
          }
        }
      } else if (s.nodeType === 8) if (s.data === Ne) a.push({ type: 2, index: r });
      else {
        let h = -1;
        for (; (h = s.data.indexOf(j, h + 1)) !== -1; ) a.push({ type: 7, index: r }), h += j.length - 1;
      }
      r++;
    }
  }
  static createElement(t, e) {
    const i = Q.createElement("template");
    return i.innerHTML = t, i;
  }
}
function et(n, t, e = n, i) {
  var o, c;
  if (t === tt) return t;
  let s = i !== void 0 ? (o = e._$Co) == null ? void 0 : o[i] : e._$Cl;
  const r = gt(t) ? void 0 : t._$litDirective$;
  return (s == null ? void 0 : s.constructor) !== r && ((c = s == null ? void 0 : s._$AO) == null || c.call(s, !1), r === void 0 ? s = void 0 : (s = new r(n), s._$AT(n, e, i)), i !== void 0 ? (e._$Co ?? (e._$Co = []))[i] = s : e._$Cl = s), s !== void 0 && (t = et(n, s._$AS(n, t.values), s, i)), t;
}
class hs {
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
    const { el: { content: e }, parts: i } = this._$AD, s = ((t == null ? void 0 : t.creationScope) ?? Q).importNode(e, !0);
    J.currentNode = s;
    let r = J.nextNode(), o = 0, c = 0, a = i[0];
    for (; a !== void 0; ) {
      if (o === a.index) {
        let l;
        a.type === 2 ? l = new vt(r, r.nextSibling, this, t) : a.type === 1 ? l = new a.ctor(r, a.name, a.strings, this, t) : a.type === 6 && (l = new ps(r, this, t)), this._$AV.push(l), a = i[++c];
      }
      o !== (a == null ? void 0 : a.index) && (r = J.nextNode(), o++);
    }
    return J.currentNode = Q, s;
  }
  p(t) {
    let e = 0;
    for (const i of this._$AV) i !== void 0 && (i.strings !== void 0 ? (i._$AI(t, i, e), e += i.strings.length - 2) : i._$AI(t[e])), e++;
  }
}
class vt {
  get _$AU() {
    var t;
    return ((t = this._$AM) == null ? void 0 : t._$AU) ?? this._$Cv;
  }
  constructor(t, e, i, s) {
    this.type = 2, this._$AH = $, this._$AN = void 0, this._$AA = t, this._$AB = e, this._$AM = i, this.options = s, this._$Cv = (s == null ? void 0 : s.isConnected) ?? !0;
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
    t = et(this, t, e), gt(t) ? t === $ || t == null || t === "" ? (this._$AH !== $ && this._$AR(), this._$AH = $) : t !== this._$AH && t !== tt && this._(t) : t._$litType$ !== void 0 ? this.$(t) : t.nodeType !== void 0 ? this.T(t) : cs(t) ? this.k(t) : this._(t);
  }
  O(t) {
    return this._$AA.parentNode.insertBefore(t, this._$AB);
  }
  T(t) {
    this._$AH !== t && (this._$AR(), this._$AH = this.O(t));
  }
  _(t) {
    this._$AH !== $ && gt(this._$AH) ? this._$AA.nextSibling.data = t : this.T(Q.createTextNode(t)), this._$AH = t;
  }
  $(t) {
    var r;
    const { values: e, _$litType$: i } = t, s = typeof i == "number" ? this._$AC(t) : (i.el === void 0 && (i.el = pt.createElement(Me(i.h, i.h[0]), this.options)), i);
    if (((r = this._$AH) == null ? void 0 : r._$AD) === s) this._$AH.p(e);
    else {
      const o = new hs(s, this), c = o.u(this.options);
      o.p(e), this.T(c), this._$AH = o;
    }
  }
  _$AC(t) {
    let e = Ae.get(t.strings);
    return e === void 0 && Ae.set(t.strings, e = new pt(t)), e;
  }
  k(t) {
    Xt(this._$AH) || (this._$AH = [], this._$AR());
    const e = this._$AH;
    let i, s = 0;
    for (const r of t) s === e.length ? e.push(i = new vt(this.O(ft()), this.O(ft()), this, this.options)) : i = e[s], i._$AI(r), s++;
    s < e.length && (this._$AR(i && i._$AB.nextSibling, s), e.length = s);
  }
  _$AR(t = this._$AA.nextSibling, e) {
    var i;
    for ((i = this._$AP) == null ? void 0 : i.call(this, !1, !0, e); t !== this._$AB; ) {
      const s = _e(t).nextSibling;
      _e(t).remove(), t = s;
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
  constructor(t, e, i, s, r) {
    this.type = 1, this._$AH = $, this._$AN = void 0, this.element = t, this.name = e, this._$AM = s, this.options = r, i.length > 2 || i[0] !== "" || i[1] !== "" ? (this._$AH = Array(i.length - 1).fill(new String()), this.strings = i) : this._$AH = $;
  }
  _$AI(t, e = this, i, s) {
    const r = this.strings;
    let o = !1;
    if (r === void 0) t = et(this, t, e, 0), o = !gt(t) || t !== this._$AH && t !== tt, o && (this._$AH = t);
    else {
      const c = t;
      let a, l;
      for (t = r[0], a = 0; a < r.length - 1; a++) l = et(this, c[i + a], e, a), l === tt && (l = this._$AH[a]), o || (o = !gt(l) || l !== this._$AH[a]), l === $ ? t = $ : t !== $ && (t += (l ?? "") + r[a + 1]), this._$AH[a] = l;
    }
    o && !s && this.j(t);
  }
  j(t) {
    t === $ ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, t ?? "");
  }
}
class us extends Tt {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(t) {
    this.element[this.name] = t === $ ? void 0 : t;
  }
}
class fs extends Tt {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(t) {
    this.element.toggleAttribute(this.name, !!t && t !== $);
  }
}
class gs extends Tt {
  constructor(t, e, i, s, r) {
    super(t, e, i, s, r), this.type = 5;
  }
  _$AI(t, e = this) {
    if ((t = et(this, t, e, 0) ?? $) === tt) return;
    const i = this._$AH, s = t === $ && i !== $ || t.capture !== i.capture || t.once !== i.once || t.passive !== i.passive, r = t !== $ && (i === $ || s);
    s && this.element.removeEventListener(this.name, this, i), r && this.element.addEventListener(this.name, this, t), this._$AH = t;
  }
  handleEvent(t) {
    var e;
    typeof this._$AH == "function" ? this._$AH.call(((e = this.options) == null ? void 0 : e.host) ?? this.element, t) : this._$AH.handleEvent(t);
  }
}
class ps {
  constructor(t, e, i) {
    this.element = t, this.type = 6, this._$AN = void 0, this._$AM = e, this.options = i;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t) {
    et(this, t);
  }
}
const Ot = ht.litHtmlPolyfillSupport;
Ot == null || Ot(pt, vt), (ht.litHtmlVersions ?? (ht.litHtmlVersions = [])).push("3.3.2");
const ms = (n, t, e) => {
  const i = (e == null ? void 0 : e.renderBefore) ?? t;
  let s = i._$litPart$;
  if (s === void 0) {
    const r = (e == null ? void 0 : e.renderBefore) ?? null;
    i._$litPart$ = s = new vt(t.insertBefore(ft(), r), r, void 0, e ?? {});
  }
  return s._$AI(n), s;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Y = globalThis;
class N extends X {
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
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Do = ms(e, this.renderRoot, this.renderOptions);
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
    return tt;
  }
}
var ke;
N._$litElement$ = !0, N.finalized = !0, (ke = Y.litElementHydrateSupport) == null || ke.call(Y, { LitElement: N });
const Ft = Y.litElementPolyfillSupport;
Ft == null || Ft({ LitElement: N });
(Y.litElementVersions ?? (Y.litElementVersions = [])).push("4.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const _s = { attribute: !0, type: String, converter: $t, reflect: !1, hasChanged: Zt }, ys = (n = _s, t, e) => {
  const { kind: i, metadata: s } = e;
  let r = globalThis.litPropertyMetadata.get(s);
  if (r === void 0 && globalThis.litPropertyMetadata.set(s, r = /* @__PURE__ */ new Map()), i === "setter" && ((n = Object.create(n)).wrapped = !0), r.set(e.name, n), i === "accessor") {
    const { name: o } = e;
    return { set(c) {
      const a = t.get.call(this);
      t.set.call(this, c), this.requestUpdate(o, a, n, !0, c);
    }, init(c) {
      return c !== void 0 && this.C(o, void 0, n, c), c;
    } };
  }
  if (i === "setter") {
    const { name: o } = e;
    return function(c) {
      const a = this[o];
      t.call(this, c), this.requestUpdate(o, a, n, !0, c);
    };
  }
  throw Error("Unsupported decorator location: " + i);
};
function H(n) {
  return (t, e) => typeof e == "object" ? ys(n, t, e) : ((i, s, r) => {
    const o = s.hasOwnProperty(r);
    return s.constructor.createProperty(r, i), o ? Object.getOwnPropertyDescriptor(s, r) : void 0;
  })(n, t, e);
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function v(n) {
  return H({ ...n, state: !0, attribute: !1 });
}
var ot = {}, ws = function() {
  return typeof Promise == "function" && Promise.prototype && Promise.prototype.then;
}, xe = {}, P = {};
let te;
const vs = [
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
  return vs[t];
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
  te = t;
};
P.isKanjiModeEnabled = function() {
  return typeof te < "u";
};
P.toSJIS = function(t) {
  return te(t);
};
var Nt = {};
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
})(Nt);
function De() {
  this.buffer = [], this.length = 0;
}
De.prototype = {
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
var bs = De;
function bt(n) {
  if (!n || n < 1)
    throw new Error("BitMatrix size must be defined and greater than 0");
  this.size = n, this.data = new Uint8Array(n * n), this.reservedBit = new Uint8Array(n * n);
}
bt.prototype.set = function(n, t, e, i) {
  const s = n * this.size + t;
  this.data[s] = e, i && (this.reservedBit[s] = !0);
};
bt.prototype.get = function(n, t) {
  return this.data[n * this.size + t];
};
bt.prototype.xor = function(n, t, e) {
  this.data[n * this.size + t] ^= e;
};
bt.prototype.isReserved = function(n, t) {
  return this.reservedBit[n * this.size + t];
};
var Es = bt, Be = {};
(function(n) {
  const t = P.getSymbolSize;
  n.getRowColCoords = function(i) {
    if (i === 1) return [];
    const s = Math.floor(i / 7) + 2, r = t(i), o = r === 145 ? 26 : Math.ceil((r - 13) / (2 * s - 2)) * 2, c = [r - 7];
    for (let a = 1; a < s - 1; a++)
      c[a] = c[a - 1] - o;
    return c.push(6), c.reverse();
  }, n.getPositions = function(i) {
    const s = [], r = n.getRowColCoords(i), o = r.length;
    for (let c = 0; c < o; c++)
      for (let a = 0; a < o; a++)
        c === 0 && a === 0 || // top-left
        c === 0 && a === o - 1 || // bottom-left
        c === o - 1 && a === 0 || s.push([r[c], r[a]]);
    return s;
  };
})(Be);
var Le = {};
const As = P.getSymbolSize, Ce = 7;
Le.getPositions = function(t) {
  const e = As(t);
  return [
    // top-left
    [0, 0],
    // top-right
    [e - Ce, 0],
    // bottom-left
    [0, e - Ce]
  ];
};
var Re = {};
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
    let o = 0, c = 0, a = 0, l = null, d = null;
    for (let h = 0; h < r; h++) {
      c = a = 0, l = d = null;
      for (let u = 0; u < r; u++) {
        let f = s.get(h, u);
        f === l ? c++ : (c >= 5 && (o += t.N1 + (c - 5)), l = f, c = 1), f = s.get(u, h), f === d ? a++ : (a >= 5 && (o += t.N1 + (a - 5)), d = f, a = 1);
      }
      c >= 5 && (o += t.N1 + (c - 5)), a >= 5 && (o += t.N1 + (a - 5));
    }
    return o;
  }, n.getPenaltyN2 = function(s) {
    const r = s.size;
    let o = 0;
    for (let c = 0; c < r - 1; c++)
      for (let a = 0; a < r - 1; a++) {
        const l = s.get(c, a) + s.get(c, a + 1) + s.get(c + 1, a) + s.get(c + 1, a + 1);
        (l === 4 || l === 0) && o++;
      }
    return o * t.N2;
  }, n.getPenaltyN3 = function(s) {
    const r = s.size;
    let o = 0, c = 0, a = 0;
    for (let l = 0; l < r; l++) {
      c = a = 0;
      for (let d = 0; d < r; d++)
        c = c << 1 & 2047 | s.get(l, d), d >= 10 && (c === 1488 || c === 93) && o++, a = a << 1 & 2047 | s.get(d, l), d >= 10 && (a === 1488 || a === 93) && o++;
    }
    return o * t.N3;
  }, n.getPenaltyN4 = function(s) {
    let r = 0;
    const o = s.data.length;
    for (let a = 0; a < o; a++) r += s.data[a];
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
    for (let c = 0; c < o; c++)
      for (let a = 0; a < o; a++)
        r.isReserved(a, c) || r.xor(a, c, e(s, a, c));
  }, n.getBestMask = function(s, r) {
    const o = Object.keys(n.Patterns).length;
    let c = 0, a = 1 / 0;
    for (let l = 0; l < o; l++) {
      r(l), n.applyMask(l, s);
      const d = n.getPenaltyN1(s) + n.getPenaltyN2(s) + n.getPenaltyN3(s) + n.getPenaltyN4(s);
      n.applyMask(l, s), d < a && (a = d, c = l);
    }
    return c;
  };
})(Re);
var It = {};
const V = Nt, Et = [
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
It.getBlocksCount = function(t, e) {
  switch (e) {
    case V.L:
      return Et[(t - 1) * 4 + 0];
    case V.M:
      return Et[(t - 1) * 4 + 1];
    case V.Q:
      return Et[(t - 1) * 4 + 2];
    case V.H:
      return Et[(t - 1) * 4 + 3];
    default:
      return;
  }
};
It.getTotalCodewordsCount = function(t, e) {
  switch (e) {
    case V.L:
      return At[(t - 1) * 4 + 0];
    case V.M:
      return At[(t - 1) * 4 + 1];
    case V.Q:
      return At[(t - 1) * 4 + 2];
    case V.H:
      return At[(t - 1) * 4 + 3];
    default:
      return;
  }
};
var Ue = {}, Mt = {};
const ut = new Uint8Array(512), kt = new Uint8Array(256);
(function() {
  let t = 1;
  for (let e = 0; e < 255; e++)
    ut[e] = t, kt[t] = e, t <<= 1, t & 256 && (t ^= 285);
  for (let e = 255; e < 512; e++)
    ut[e] = ut[e - 255];
})();
Mt.log = function(t) {
  if (t < 1) throw new Error("log(" + t + ")");
  return kt[t];
};
Mt.exp = function(t) {
  return ut[t];
};
Mt.mul = function(t, e) {
  return t === 0 || e === 0 ? 0 : ut[kt[t] + kt[e]];
};
(function(n) {
  const t = Mt;
  n.mul = function(i, s) {
    const r = new Uint8Array(i.length + s.length - 1);
    for (let o = 0; o < i.length; o++)
      for (let c = 0; c < s.length; c++)
        r[o + c] ^= t.mul(i[o], s[c]);
    return r;
  }, n.mod = function(i, s) {
    let r = new Uint8Array(i);
    for (; r.length - s.length >= 0; ) {
      const o = r[0];
      for (let a = 0; a < s.length; a++)
        r[a] ^= t.mul(s[a], o);
      let c = 0;
      for (; c < r.length && r[c] === 0; ) c++;
      r = r.slice(c);
    }
    return r;
  }, n.generateECPolynomial = function(i) {
    let s = new Uint8Array([1]);
    for (let r = 0; r < i; r++)
      s = n.mul(s, new Uint8Array([1, t.exp(r)]));
    return s;
  };
})(Ue);
const Oe = Ue;
function ee(n) {
  this.genPoly = void 0, this.degree = n, this.degree && this.initialize(this.degree);
}
ee.prototype.initialize = function(t) {
  this.degree = t, this.genPoly = Oe.generateECPolynomial(this.degree);
};
ee.prototype.encode = function(t) {
  if (!this.genPoly)
    throw new Error("Encoder not initialized");
  const e = new Uint8Array(t.length + this.degree);
  e.set(t);
  const i = Oe.mod(e, this.genPoly), s = this.degree - i.length;
  if (s > 0) {
    const r = new Uint8Array(this.degree);
    return r.set(i, s), r;
  }
  return i;
};
var Cs = ee, Fe = {}, K = {}, se = {};
se.isValid = function(t) {
  return !isNaN(t) && t >= 1 && t <= 40;
};
var D = {};
const He = "[0-9]+", $s = "[A-Z $%*+\\-./:]+";
let mt = "(?:[u3000-u303F]|[u3040-u309F]|[u30A0-u30FF]|[uFF00-uFFEF]|[u4E00-u9FAF]|[u2605-u2606]|[u2190-u2195]|u203B|[u2010u2015u2018u2019u2025u2026u201Cu201Du2225u2260]|[u0391-u0451]|[u00A7u00A8u00B1u00B4u00D7u00F7])+";
mt = mt.replace(/u/g, "\\u");
const Ss = "(?:(?![A-Z0-9 $%*+\\-./:]|" + mt + `)(?:.|[\r
]))+`;
D.KANJI = new RegExp(mt, "g");
D.BYTE_KANJI = new RegExp("[^A-Z0-9 $%*+\\-./:]+", "g");
D.BYTE = new RegExp(Ss, "g");
D.NUMERIC = new RegExp(He, "g");
D.ALPHANUMERIC = new RegExp($s, "g");
const ks = new RegExp("^" + mt + "$"), Ps = new RegExp("^" + He + "$"), Ts = new RegExp("^[A-Z0-9 $%*+\\-./:]+$");
D.testKanji = function(t) {
  return ks.test(t);
};
D.testNumeric = function(t) {
  return Ps.test(t);
};
D.testAlphanumeric = function(t) {
  return Ts.test(t);
};
(function(n) {
  const t = se, e = D;
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
  const t = P, e = It, i = Nt, s = K, r = se, o = 7973, c = t.getBCHDigit(o);
  function a(u, f, g) {
    for (let y = 1; y <= 40; y++)
      if (f <= n.getCapacity(y, g, u))
        return y;
  }
  function l(u, f) {
    return s.getCharCountIndicator(u, f) + 4;
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
      if (d(u, g) <= n.getCapacity(g, f, s.MIXED))
        return g;
  }
  n.from = function(f, g) {
    return r.isValid(f) ? parseInt(f, 10) : g;
  }, n.getCapacity = function(f, g, y) {
    if (!r.isValid(f))
      throw new Error("Invalid QR Code version");
    typeof y > "u" && (y = s.BYTE);
    const S = t.getSymbolTotalCodewords(f), _ = e.getTotalCodewordsCount(f, g), w = (S - _) * 8;
    if (y === s.MIXED) return w;
    const m = w - l(y, f);
    switch (y) {
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
    let y;
    const S = i.from(g, i.M);
    if (Array.isArray(f)) {
      if (f.length > 1)
        return h(f, S);
      if (f.length === 0)
        return 1;
      y = f[0];
    } else
      y = f;
    return a(y.mode, y.getLength(), S);
  }, n.getEncodedBits = function(f) {
    if (!r.isValid(f) || f < 7)
      throw new Error("Invalid QR Code version");
    let g = f << 12;
    for (; t.getBCHDigit(g) - c >= 0; )
      g ^= o << t.getBCHDigit(g) - c;
    return f << 12 | g;
  };
})(Fe);
var ze = {};
const Kt = P, je = 1335, Ns = 21522, $e = Kt.getBCHDigit(je);
ze.getEncodedBits = function(t, e) {
  const i = t.bit << 3 | e;
  let s = i << 10;
  for (; Kt.getBCHDigit(s) - $e >= 0; )
    s ^= je << Kt.getBCHDigit(s) - $e;
  return (i << 10 | s) ^ Ns;
};
var Ve = {};
const Is = K;
function st(n) {
  this.mode = Is.NUMERIC, this.data = n.toString();
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
  let e, i, s;
  for (e = 0; e + 3 <= this.data.length; e += 3)
    i = this.data.substr(e, 3), s = parseInt(i, 10), t.put(s, 10);
  const r = this.data.length - e;
  r > 0 && (i = this.data.substr(e), s = parseInt(i, 10), t.put(s, r * 3 + 1));
};
var Ms = st;
const xs = K, Ht = [
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
function it(n) {
  this.mode = xs.ALPHANUMERIC, this.data = n;
}
it.getBitsLength = function(t) {
  return 11 * Math.floor(t / 2) + 6 * (t % 2);
};
it.prototype.getLength = function() {
  return this.data.length;
};
it.prototype.getBitsLength = function() {
  return it.getBitsLength(this.data.length);
};
it.prototype.write = function(t) {
  let e;
  for (e = 0; e + 2 <= this.data.length; e += 2) {
    let i = Ht.indexOf(this.data[e]) * 45;
    i += Ht.indexOf(this.data[e + 1]), t.put(i, 11);
  }
  this.data.length % 2 && t.put(Ht.indexOf(this.data[e]), 6);
};
var Ds = it;
const Bs = K;
function nt(n) {
  this.mode = Bs.BYTE, typeof n == "string" ? this.data = new TextEncoder().encode(n) : this.data = new Uint8Array(n);
}
nt.getBitsLength = function(t) {
  return t * 8;
};
nt.prototype.getLength = function() {
  return this.data.length;
};
nt.prototype.getBitsLength = function() {
  return nt.getBitsLength(this.data.length);
};
nt.prototype.write = function(n) {
  for (let t = 0, e = this.data.length; t < e; t++)
    n.put(this.data[t], 8);
};
var Ls = nt;
const Rs = K, Us = P;
function rt(n) {
  this.mode = Rs.KANJI, this.data = n;
}
rt.getBitsLength = function(t) {
  return t * 13;
};
rt.prototype.getLength = function() {
  return this.data.length;
};
rt.prototype.getBitsLength = function() {
  return rt.getBitsLength(this.data.length);
};
rt.prototype.write = function(n) {
  let t;
  for (t = 0; t < this.data.length; t++) {
    let e = Us.toSJIS(this.data[t]);
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
var Os = rt, qe = { exports: {} };
(function(n) {
  var t = {
    single_source_shortest_paths: function(e, i, s) {
      var r = {}, o = {};
      o[i] = 0;
      var c = t.PriorityQueue.make();
      c.push(i, 0);
      for (var a, l, d, h, u, f, g, y, S; !c.empty(); ) {
        a = c.pop(), l = a.value, h = a.cost, u = e[l] || {};
        for (d in u)
          u.hasOwnProperty(d) && (f = u[d], g = h + f, y = o[d], S = typeof o[d] > "u", (S || y > g) && (o[d] = g, c.push(d, g), r[d] = l));
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
})(qe);
var Fs = qe.exports;
(function(n) {
  const t = K, e = Ms, i = Ds, s = Ls, r = Os, o = D, c = P, a = Fs;
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
    return c.isKanjiModeEnabled() ? (p = d(o.BYTE, t.BYTE, _), E = d(o.KANJI, t.KANJI, _)) : (p = d(o.BYTE_KANJI, t.BYTE, _), E = []), w.concat(m, p, E).sort(function(C, M) {
      return C.index - M.index;
    }).map(function(C) {
      return {
        data: C.data,
        mode: C.mode,
        length: C.length
      };
    });
  }
  function u(_, w) {
    switch (w) {
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
    for (let A = 0; A < _.length; A++) {
      const C = _[A], M = [];
      for (let z = 0; z < C.length; z++) {
        const x = C[z], ct = "" + A + z;
        M.push(ct), m[ct] = { node: x, lastCount: 0 }, p[ct] = {};
        for (let Lt = 0; Lt < E.length; Lt++) {
          const B = E[Lt];
          m[B] && m[B].node.mode === x.mode ? (p[B][ct] = u(m[B].lastCount + x.length, x.mode) - u(m[B].lastCount, x.mode), m[B].lastCount += x.length) : (m[B] && (m[B].lastCount = x.length), p[B][ct] = u(x.length, x.mode) + 4 + t.getCharCountIndicator(x.mode, w));
        }
      }
      E = M;
    }
    for (let A = 0; A < E.length; A++)
      p[E[A]].end = 0;
    return { map: p, table: m };
  }
  function S(_, w) {
    let m;
    const p = t.getBestModeForData(_);
    if (m = t.from(w, p), m !== t.BYTE && m.bit < p.bit)
      throw new Error('"' + _ + '" cannot be encoded with mode ' + t.toString(m) + `.
 Suggested mode is: ` + t.toString(p));
    switch (m === t.KANJI && !c.isKanjiModeEnabled() && (m = t.BYTE), m) {
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
  n.fromArray = function(w) {
    return w.reduce(function(m, p) {
      return typeof p == "string" ? m.push(S(p, null)) : p.data && m.push(S(p.data, p.mode)), m;
    }, []);
  }, n.fromString = function(w, m) {
    const p = h(w, c.isKanjiModeEnabled()), E = g(p), A = y(E, m), C = a.find_path(A.map, "start", "end"), M = [];
    for (let z = 1; z < C.length - 1; z++)
      M.push(A.table[C[z]].node);
    return n.fromArray(f(M));
  }, n.rawSplit = function(w) {
    return n.fromArray(
      h(w, c.isKanjiModeEnabled())
    );
  };
})(Ve);
const xt = P, zt = Nt, Hs = bs, zs = Es, js = Be, Vs = Le, Gt = Re, Wt = It, qs = Cs, Pt = Fe, Ks = ze, Gs = K, jt = Ve;
function Ws(n, t) {
  const e = n.size, i = Vs.getPositions(t);
  for (let s = 0; s < i.length; s++) {
    const r = i[s][0], o = i[s][1];
    for (let c = -1; c <= 7; c++)
      if (!(r + c <= -1 || e <= r + c))
        for (let a = -1; a <= 7; a++)
          o + a <= -1 || e <= o + a || (c >= 0 && c <= 6 && (a === 0 || a === 6) || a >= 0 && a <= 6 && (c === 0 || c === 6) || c >= 2 && c <= 4 && a >= 2 && a <= 4 ? n.set(r + c, o + a, !0, !0) : n.set(r + c, o + a, !1, !0));
  }
}
function Js(n) {
  const t = n.size;
  for (let e = 8; e < t - 8; e++) {
    const i = e % 2 === 0;
    n.set(e, 6, i, !0), n.set(6, e, i, !0);
  }
}
function Ys(n, t) {
  const e = js.getPositions(t);
  for (let i = 0; i < e.length; i++) {
    const s = e[i][0], r = e[i][1];
    for (let o = -2; o <= 2; o++)
      for (let c = -2; c <= 2; c++)
        o === -2 || o === 2 || c === -2 || c === 2 || o === 0 && c === 0 ? n.set(s + o, r + c, !0, !0) : n.set(s + o, r + c, !1, !0);
  }
}
function Qs(n, t) {
  const e = n.size, i = Pt.getEncodedBits(t);
  let s, r, o;
  for (let c = 0; c < 18; c++)
    s = Math.floor(c / 3), r = c % 3 + e - 8 - 3, o = (i >> c & 1) === 1, n.set(s, r, o, !0), n.set(r, s, o, !0);
}
function Vt(n, t, e) {
  const i = n.size, s = Ks.getEncodedBits(t, e);
  let r, o;
  for (r = 0; r < 15; r++)
    o = (s >> r & 1) === 1, r < 6 ? n.set(r, 8, o, !0) : r < 8 ? n.set(r + 1, 8, o, !0) : n.set(i - 15 + r, 8, o, !0), r < 8 ? n.set(8, i - r - 1, o, !0) : r < 9 ? n.set(8, 15 - r - 1 + 1, o, !0) : n.set(8, 15 - r - 1, o, !0);
  n.set(i - 8, 8, 1, !0);
}
function Zs(n, t) {
  const e = n.size;
  let i = -1, s = e - 1, r = 7, o = 0;
  for (let c = e - 1; c > 0; c -= 2)
    for (c === 6 && c--; ; ) {
      for (let a = 0; a < 2; a++)
        if (!n.isReserved(s, c - a)) {
          let l = !1;
          o < t.length && (l = (t[o] >>> r & 1) === 1), n.set(s, c - a, l), r--, r === -1 && (o++, r = 7);
        }
      if (s += i, s < 0 || e <= s) {
        s -= i, i = -i;
        break;
      }
    }
}
function Xs(n, t, e) {
  const i = new Hs();
  e.forEach(function(a) {
    i.put(a.mode.bit, 4), i.put(a.getLength(), Gs.getCharCountIndicator(a.mode, n)), a.write(i);
  });
  const s = xt.getSymbolTotalCodewords(n), r = Wt.getTotalCodewordsCount(n, t), o = (s - r) * 8;
  for (i.getLengthInBits() + 4 <= o && i.put(0, 4); i.getLengthInBits() % 8 !== 0; )
    i.putBit(0);
  const c = (o - i.getLengthInBits()) / 8;
  for (let a = 0; a < c; a++)
    i.put(a % 2 ? 17 : 236, 8);
  return ti(i, n, t);
}
function ti(n, t, e) {
  const i = xt.getSymbolTotalCodewords(t), s = Wt.getTotalCodewordsCount(t, e), r = i - s, o = Wt.getBlocksCount(t, e), c = i % o, a = o - c, l = Math.floor(i / o), d = Math.floor(r / o), h = d + 1, u = l - d, f = new qs(u);
  let g = 0;
  const y = new Array(o), S = new Array(o);
  let _ = 0;
  const w = new Uint8Array(n.buffer);
  for (let C = 0; C < o; C++) {
    const M = C < a ? d : h;
    y[C] = w.slice(g, g + M), S[C] = f.encode(y[C]), g += M, _ = Math.max(_, M);
  }
  const m = new Uint8Array(i);
  let p = 0, E, A;
  for (E = 0; E < _; E++)
    for (A = 0; A < o; A++)
      E < y[A].length && (m[p++] = y[A][E]);
  for (E = 0; E < u; E++)
    for (A = 0; A < o; A++)
      m[p++] = S[A][E];
  return m;
}
function ei(n, t, e, i) {
  let s;
  if (Array.isArray(n))
    s = jt.fromArray(n);
  else if (typeof n == "string") {
    let l = t;
    if (!l) {
      const d = jt.rawSplit(n);
      l = Pt.getBestVersionForData(d, e);
    }
    s = jt.fromString(n, l || 40);
  } else
    throw new Error("Invalid data");
  const r = Pt.getBestVersionForData(s, e);
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
  const o = Xs(t, e, s), c = xt.getSymbolSize(t), a = new zs(c);
  return Ws(a, t), Js(a), Ys(a, t), Vt(a, e, 0), t >= 7 && Qs(a, t), Zs(a, o), isNaN(i) && (i = Gt.getBestMask(
    a,
    Vt.bind(null, a, e)
  )), Gt.applyMask(i, a), Vt(a, e, i), {
    modules: a,
    version: t,
    errorCorrectionLevel: e,
    maskPattern: i,
    segments: s
  };
}
xe.create = function(t, e) {
  if (typeof t > "u" || t === "")
    throw new Error("No input text");
  let i = zt.M, s, r;
  return typeof e < "u" && (i = zt.from(e.errorCorrectionLevel, zt.M), s = Pt.from(e.version), r = Gt.from(e.maskPattern), e.toSJISFunc && xt.setToSJISFunction(e.toSJISFunc)), ei(t, s, i, r);
};
var Ke = {}, ie = {};
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
    const o = s.modules.size, c = s.modules.data, a = n.getScale(o, r), l = Math.floor((o + r.margin * 2) * a), d = r.margin * a, h = [r.color.light, r.color.dark];
    for (let u = 0; u < l; u++)
      for (let f = 0; f < l; f++) {
        let g = (u * l + f) * 4, y = r.color.light;
        if (u >= d && f >= d && u < l - d && f < l - d) {
          const S = Math.floor((u - d) / a), _ = Math.floor((f - d) / a);
          y = h[c[S * o + _] ? 1 : 0];
        }
        i[g++] = y.r, i[g++] = y.g, i[g++] = y.b, i[g] = y.a;
      }
  };
})(ie);
(function(n) {
  const t = ie;
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
  n.render = function(r, o, c) {
    let a = c, l = o;
    typeof a > "u" && (!o || !o.getContext) && (a = o, o = void 0), o || (l = i()), a = t.getOptions(a);
    const d = t.getImageWidth(r.modules.size, a), h = l.getContext("2d"), u = h.createImageData(d, d);
    return t.qrToImageData(u.data, r, a), e(h, l, d), h.putImageData(u, 0, 0), l;
  }, n.renderToDataURL = function(r, o, c) {
    let a = c;
    typeof a > "u" && (!o || !o.getContext) && (a = o, o = void 0), a || (a = {});
    const l = n.render(r, o, a), d = a.type || "image/png", h = a.rendererOpts || {};
    return l.toDataURL(d, h.quality);
  };
})(Ke);
var Ge = {};
const si = ie;
function Se(n, t) {
  const e = n.a / 255, i = t + '="' + n.hex + '"';
  return e < 1 ? i + " " + t + '-opacity="' + e.toFixed(2).slice(1) + '"' : i;
}
function qt(n, t, e) {
  let i = n + t;
  return typeof e < "u" && (i += " " + e), i;
}
function ii(n, t, e) {
  let i = "", s = 0, r = !1, o = 0;
  for (let c = 0; c < n.length; c++) {
    const a = Math.floor(c % t), l = Math.floor(c / t);
    !a && !r && (r = !0), n[c] ? (o++, c > 0 && a > 0 && n[c - 1] || (i += r ? qt("M", a + e, 0.5 + l + e) : qt("m", s, 0), s = 0, r = !1), a + 1 < t && n[c + 1] || (i += qt("h", o), o = 0)) : s++;
  }
  return i;
}
Ge.render = function(t, e, i) {
  const s = si.getOptions(e), r = t.modules.size, o = t.modules.data, c = r + s.margin * 2, a = s.color.light.a ? "<path " + Se(s.color.light, "fill") + ' d="M0 0h' + c + "v" + c + 'H0z"/>' : "", l = "<path " + Se(s.color.dark, "stroke") + ' d="' + ii(o, r, s.margin) + '"/>', d = 'viewBox="0 0 ' + c + " " + c + '"', u = '<svg xmlns="http://www.w3.org/2000/svg" ' + (s.width ? 'width="' + s.width + '" height="' + s.width + '" ' : "") + d + ' shape-rendering="crispEdges">' + a + l + `</svg>
`;
  return typeof i == "function" && i(null, u), u;
};
const ni = ws, Jt = xe, We = Ke, ri = Ge;
function ne(n, t, e, i, s) {
  const r = [].slice.call(arguments, 1), o = r.length, c = typeof r[o - 1] == "function";
  if (!c && !ni())
    throw new Error("Callback required as last argument");
  if (c) {
    if (o < 2)
      throw new Error("Too few arguments provided");
    o === 2 ? (s = e, e = t, t = i = void 0) : o === 3 && (t.getContext && typeof s > "u" ? (s = i, i = void 0) : (s = i, i = e, e = t, t = void 0));
  } else {
    if (o < 1)
      throw new Error("Too few arguments provided");
    return o === 1 ? (e = t, t = i = void 0) : o === 2 && !t.getContext && (i = e, e = t, t = void 0), new Promise(function(a, l) {
      try {
        const d = Jt.create(e, i);
        a(n(d, t, i));
      } catch (d) {
        l(d);
      }
    });
  }
  try {
    const a = Jt.create(e, i);
    s(null, n(a, t, i));
  } catch (a) {
    s(a);
  }
}
ot.create = Jt.create;
ot.toCanvas = ne.bind(null, We.render);
ot.toDataURL = ne.bind(null, We.renderToDataURL);
ot.toString = ne.bind(null, function(n, t, e) {
  return ri.render(n, e);
});
const Je = (n, t, e) => b`
  <ha-card class="status-card warning">
    <div class="card-content flex-col align-center p-8">
      <ha-icon icon="mdi:alert-circle" style="--mdc-icon-size: 48px; margin-bottom: 16px;"></ha-icon>
      <h1 class="status-title">${n}</h1>
      <div class="status-message mt-4">${t}</div>
    </div>
    ${b`<div class="version">v${e}</div>`}
  </ha-card>
`, Dt = (n, t, e) => b`
  <ha-card class="status-card loading">
    <div class="card-content flex-col align-center p-8">
      <h1 class="status-title">${n}</h1>
      <ha-circular-progress active></ha-circular-progress>
      <div class="status-message mt-4">${t}</div>
    </div>
    <div class="version">v${e}</div>
  </ha-card>
`, Bt = F`
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
  .align-center { align-items: center; }
  .p-8 { padding: 32px; }
  .mt-4 { margin-top: 16px; }

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
var Ye = /* @__PURE__ */ ((n) => (n.GET_CONFIG = "meraki_ha/get_config", n.SUBSCRIBE_MERAKI_DATA = "meraki_ha/subscribe_meraki_data", n.GET_CAMERA_STREAM_URL = "meraki_ha/get_camera_stream_url", n.GET_CAMERA_SNAPSHOT = "meraki_ha/get_camera_snapshot", n.GET_VERSION = "meraki_ha/get_version", n.GET_NETWORK_EVENTS = "meraki_ha/get_network_events", n.UPDATE_ENABLED_NETWORKS = "meraki_ha/update_enabled_networks", n.CREATE_GUEST_KEY = "meraki_ha/ipsk/create", n.GET_GUEST_KEYS = "meraki_ha/ipsk/get", n.REVOKE_GUEST_KEY = "meraki_ha/ipsk/revoke", n.TIMED_ACCESS_GET_POLICIES = "meraki_ha/timed_access/get_policies", n))(Ye || {});
const oi = async (n, t) => {
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
class L {
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
      const s = await oi(t, {
        type: Ye.GET_CONFIG,
        config_entry_id: i
      }), r = (Array.isArray(s.networks) ? s.networks : []).filter((a) => {
        var l;
        return (l = a.productTypes) == null ? void 0 : l.includes("wireless");
      }), o = Array.isArray(s.ssids) ? s.ssids : [], c = [];
      if (s.group_policies && typeof s.group_policies == "object")
        for (const [a, l] of Object.entries(
          s.group_policies
        ))
          Array.isArray(l) && l.forEach((d) => {
            c.push({
              networkId: a,
              groupPolicyId: String(d.groupPolicyId),
              name: d.name
            });
          });
      return { networks: r, ssids: o, groupPolicies: c, entryId: i };
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
var ai = Object.defineProperty, G = (n, t, e, i) => {
  for (var s = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = o(t, e, s) || s);
  return s && ai(t, e, s), s;
};
const re = class re extends N {
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
      return Dt(
        ((l = this._config) == null ? void 0 : l.name) || "Meraki Content Filter",
        this._loadingMessage,
        "2.3.0-beta.3505"
      );
    const t = this._config.entity || this._discoverEntity(), e = t ? this.hass.states[t] : void 0, i = this._config.entity ? this.hass.states[this._config.entity] : void 0, s = ((d = i == null ? void 0 : i.attributes) == null ? void 0 : d.friendly_name) || "Meraki", r = this._config.name || (this._config.entity ? `${s} Content Filter` : "Meraki Content Filter");
    if (!t || !e)
      return Je(
        "Entity Missing",
        "No content filter entity was found. Please check your configuration.",
        "2.3.0-beta.3505"
      );
    const o = e.state || "Unknown", c = ((h = e.attributes) == null ? void 0 : h.options) || ["None", "Security", "Family", "Strict"], a = this._optimisticProfile || o;
    return b`
      <ha-card .header="${r}">
        <div class="card-content">
          <div class="button-grid">
            ${c.map((u) => {
      const f = a.toLowerCase() === u.toLowerCase(), g = this._isUpdating && this._optimisticProfile === u;
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
        <div class="version">v${"2.3.0-beta.3505"}</div>
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
re.styles = [
  Bt,
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
let R = re;
G([
  H({ attribute: !1 })
], R.prototype, "hass");
G([
  v()
], R.prototype, "_config");
G([
  v()
], R.prototype, "_optimisticProfile");
G([
  v()
], R.prototype, "_isUpdating");
G([
  v()
], R.prototype, "_isLoading");
G([
  v()
], R.prototype, "_loadingMessage");
const oe = class oe extends N {
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
oe.styles = F`
    .editor-container { padding: 16px; }
  `;
let _t = oe;
G([
  H({ attribute: !1 })
], _t.prototype, "hass");
G([
  v()
], _t.prototype, "_config");
customElements.get("meraki-content-filter-card") || customElements.define("meraki-content-filter-card", R);
customElements.get("meraki-content-filter-card-editor") || customElements.define("meraki-content-filter-card-editor", _t);
window.customCards = window.customCards || [];
window.customCards.some((n) => n.type === "meraki-content-filter-card") || window.customCards.push({
  type: "meraki-content-filter-card",
  name: "Meraki Content Filter",
  description: "Control Meraki Content Filtering profiles.",
  preview: !0
});
var ci = Object.defineProperty, I = (n, t, e, i) => {
  for (var s = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = o(t, e, s) || s);
  return s && ci(t, e, s), s;
};
const ae = class ae extends N {
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
    const t = L.getNetworkOptions(this._networks, !0), e = L.getSsidOptions(this._ssids, this._config.networkId, "name"), i = [
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
ae.styles = F`.editor-container { padding: 16px; }`;
let U = ae;
I([
  H({ attribute: !1 })
], U.prototype, "hass");
I([
  v()
], U.prototype, "_config");
I([
  v()
], U.prototype, "_networks");
I([
  v()
], U.prototype, "_ssids");
I([
  v()
], U.prototype, "_isLoading");
I([
  v()
], U.prototype, "_loadingMessage");
const ce = class ce extends N {
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
      (e, i) => {
        this._loadingMessage = e, this._isLoading = i;
      }
    );
    this._ssids = t, this._generateQR();
  }
  updated(t) {
    (t.has("hass") || t.has("_config")) && this._generateQR();
  }
  _getValue(t) {
    return !t || !this.hass ? t || "" : this.hass.states[t] ? this.hass.states[t].state : t;
  }
  _getPasswordForSsid(t) {
    var r, o;
    if (!this.hass) return "";
    if ((r = this._config) != null && r.password && this._config.password !== "password123")
      return this._getValue(this._config.password);
    if (!t) return "";
    const e = (o = this._config) == null ? void 0 : o.networkId, i = this._ssids.find(
      (c) => c.name === t && (!e || c.networkId === e)
    );
    if (i)
      for (const c in this.hass.states) {
        const a = this.hass.states[c], l = a.attributes;
        if (l.network_id === i.networkId && l.ssid_number === i.number) {
          if (l.psk) return String(l.psk);
          if (l.password) return String(l.password);
          if (a.state && !["unknown", "unavailable"].includes(a.state) && (c.includes("password") || c.includes("psk")))
            return a.state;
        }
      }
    const s = t.toLowerCase().replace(/[^a-z0-9]/g, "_");
    for (const c in this.hass.states)
      if (c.includes(s) && (c.includes("password") || c.includes("psk"))) {
        const a = this.hass.states[c];
        if (a.state && !["unknown", "unavailable"].includes(a.state))
          return a.state;
      }
    return "";
  }
  _generateWifiString(t, e) {
    const i = t.replace(/([\\;,":])/g, "\\$1"), s = e ? e.replace(/([\\;,":])/g, "\\$1") : "";
    return s ? `WIFI:T:WPA;S:${i};P:${s};;` : `WIFI:T:nopass;S:${i};P:;;`;
  }
  async _generateQR() {
    if (!this._config) return;
    const t = this._getValue(this._config.ssid), e = this._getPasswordForSsid(t);
    if (!t) {
      this._qrSvg = "";
      return;
    }
    try {
      const i = this._generateWifiString(t, e);
      this._qrSvg = await ot.toString(i, {
        type: "svg",
        margin: 2,
        color: { dark: "#000000", light: "#ffffff" }
      });
    } catch (i) {
      console.error("Failed to generate QR code", i), this._qrSvg = "";
    }
  }
  render() {
    var i;
    if (!this._config || !this.hass) return b``;
    if (this._isLoading)
      return Dt(
        ((i = this._config) == null ? void 0 : i.name) || "Wi-Fi Access",
        this._loadingMessage,
        "2.3.0-beta.3505"
      );
    const t = this._getValue(this._config.ssid), e = this._getPasswordForSsid(t);
    return b`
      <ha-card .header=${this._config.name || "Wi-Fi Access"}>
        <div class="card-content">
          <div class="ssid-display">${t}</div>
          <div class="qr-container" .innerHTML=${this._qrSvg}></div>
          ${e ? b`<div class="password-display">Password: <code>${e}</code></div>` : ""}
        </div>
        <div class="version">v${"2.3.0-beta.3505"}</div>
      </ha-card>
    `;
  }
};
ce.styles = [
  Bt,
  F`
      :host { display: block; }
      .card-content { display: flex; flex-direction: column; align-items: center; padding: 16px; gap: 16px; }
      .ssid-display { font-size: 1.5em; font-weight: bold; color: var(--primary-text-color); text-align: center; }
      .qr-container { width: 200px; height: 200px; background: white; padding: 8px; border-radius: 8px; }
      .qr-container svg { width: 100%; height: 100%; }
      .password-display { color: var(--secondary-text-color); text-align: center; }
      code { background: var(--secondary-background-color); padding: 2px 4px; border-radius: 4px; font-family: monospace; }
    `
];
let O = ce;
I([
  H({ attribute: !1 })
], O.prototype, "hass");
I([
  v()
], O.prototype, "_config");
I([
  v()
], O.prototype, "_qrSvg");
I([
  v()
], O.prototype, "_isLoading");
I([
  v()
], O.prototype, "_loadingMessage");
I([
  v()
], O.prototype, "_ssids");
customElements.get("meraki-wifi-qr-card") || customElements.define("meraki-wifi-qr-card", O);
customElements.get("meraki-wifi-qr-card-editor") || customElements.define("meraki-wifi-qr-card-editor", U);
window.customCards = window.customCards || [];
window.customCards.some((n) => n.type === "meraki-wifi-qr-card") || window.customCards.push({
  type: "meraki-wifi-qr-card",
  name: "Meraki Wi-Fi QR Card",
  description: "Display a scannable Wi-Fi QR code for guests.",
  preview: !0
});
var li = Object.defineProperty, at = (n, t, e, i) => {
  for (var s = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = o(t, e, s) || s);
  return s && li(t, e, s), s;
};
const le = class le extends N {
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
      name: "Meraki Network Vitals",
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
    let c = "var(--disabled-text-color)";
    return o === "ok" || o === "online" || o === "connected" ? c = "var(--success-color)" : o === "warning" ? c = "var(--warning-color)" : (o === "error" || o === "offline" || o === "failed") && (c = "var(--error-color)"), b`
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
          <circle cx="6" cy="6" r="6" fill="${c}" />
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
      return Dt(
        ((s = this._config) == null ? void 0 : s.name) || "Meraki Network Vitals",
        this._loadingMessage,
        "2.3.0-beta.3505"
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
        <div class="version">v${"2.3.0-beta.3505"}</div>
      </ha-card>
    `;
  }
};
le.styles = [
  Bt,
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
      .version {
        font-size: 9px;
        color: var(--secondary-text-color);
        text-align: right;
        padding: 0 12px 4px;
        opacity: 0.4;
      }
    `
];
let Z = le;
at([
  H({ attribute: !1 })
], Z.prototype, "hass");
at([
  v()
], Z.prototype, "_config");
at([
  v()
], Z.prototype, "_isLoading");
at([
  v()
], Z.prototype, "_loadingMessage");
const de = class de extends N {
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
de.styles = F`
    ha-textfield,
    ha-entity-picker {
      display: block;
      margin-bottom: 16px;
      width: 100%;
    }
  `;
let yt = de;
at([
  H({ attribute: !1 })
], yt.prototype, "hass");
at([
  v()
], yt.prototype, "_config");
customElements.get("meraki-network-vitals-card") || customElements.define("meraki-network-vitals-card", Z);
customElements.get("meraki-network-vitals-card-editor") || customElements.define(
  "meraki-network-vitals-card-editor",
  yt
);
window.customCards = window.customCards || [];
window.customCards.some(
  (n) => n.type === "meraki-network-vitals-card"
) || window.customCards.push({
  type: "meraki-network-vitals-card",
  name: "Meraki Network Vitals",
  description: "Compact horizontal health header.",
  preview: !0
});
var di = Object.defineProperty, Qe = (n, t, e, i) => {
  for (var s = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = o(t, e, s) || s);
  return s && di(t, e, s), s;
};
const he = class he extends N {
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
he.styles = F`
    .editor-container { padding: 16px; }
  `;
let wt = he;
Qe([
  H({ attribute: !1 })
], wt.prototype, "hass");
Qe([
  v()
], wt.prototype, "_config");
customElements.get("meraki-guest-access-card-editor") || customElements.define("meraki-guest-access-card-editor", wt);
var hi = Object.defineProperty, T = (n, t, e, i) => {
  for (var s = void 0, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = o(t, e, s) || s);
  return s && hi(t, e, s), s;
};
const ue = class ue extends N {
  constructor() {
    super(...arguments), this._formData = {
      network: "",
      ssid: "",
      passphrase: "",
      policy: "",
      // Added Policy field
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
    super.updated(t), t.has("hass") && this.hass && ((e = this.hass.user) != null && e.name) && !this._formData.guestName && (this._formData = { ...this._formData, guestName: this.hass.user.name });
  }
  async _loadCentralizedData() {
    var l;
    if (!this.hass) return;
    const { networks: t, ssids: e, groupPolicies: i, entryId: s } = await L.pollConfig(this.hass, (d, h) => {
      this._loadingMessage = d, this._isLoading = h;
    });
    if (t.length === 0) {
      this._isLoading = !1;
      return;
    }
    this._networks = t, this._ssids = e, this._policies = i, this._configEntryId = ((l = this._config) == null ? void 0 : l.config_entry_id) || s;
    let r = this._formData.network, o = this._formData.ssid, c = this._formData.passphrase, a = this._formData.policy;
    if (t.length > 0 && !r && (r = t[0].id), r && !o) {
      const d = e.filter((h) => h.networkId === r);
      d.length > 0 && (o = String(d[0].number));
    }
    if (r && o && !c && (c = this._getPasswordForSelectedSsid(r, o), c || (c = this._generateSecurePassword())), r && !a) {
      const d = this._policies.filter(
        (h) => h.networkId === r
      );
      d.length > 0 && (a = String(
        d[0].groupPolicyId || d[0].id
      ));
    }
    this._formData = {
      ...this._formData,
      network: r,
      ssid: o,
      passphrase: c,
      policy: a
    }, this._isLoading = !1;
  }
  _getPasswordForSelectedSsid(t, e) {
    if (!this.hass || !t || !e) return "";
    const i = parseInt(e, 10);
    let s = "";
    const r = this._ssids.find(
      (o) => o.networkId === t && o.number === i
    );
    r && (s = r.name);
    for (const o in this.hass.states) {
      const a = this.hass.states[o].attributes;
      if (a.network_id === t && a.ssid_number === i) {
        if (s || (s = a.ssid_name || a.ssid || ""), a.psk) return String(a.psk);
        if (a.password) return String(a.password);
      }
    }
    if (s) {
      const o = s.toLowerCase().replace(/[^a-z0-9]/g, "_");
      for (const c in this.hass.states)
        if (c.includes(o) && (c.includes("password") || c.includes("psk"))) {
          const a = this.hass.states[c];
          if (a.state && !["unknown", "unavailable"].includes(a.state))
            return a.state;
        }
    }
    return "";
  }
  _generateSecurePassword(t = 12) {
    const e = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let i = "";
    for (let s = 0, r = e.length; s < t; ++s)
      i += e.charAt(Math.floor(Math.random() * r));
    return i;
  }
  _formValueChanged(t) {
    const e = t.detail.value, i = this._formData.network, s = this._formData.ssid;
    let r = { ...this._formData, ...e };
    if (r.network !== i) {
      r.ssid = "", r.passphrase = "", r.policy = "";
      const o = this._ssids.filter(
        (a) => a.networkId === r.network
      );
      o.length > 0 && (r.ssid = String(o[0].number));
      const c = this._policies.filter(
        (a) => a.networkId === r.network
      );
      c.length > 0 && (r.policy = String(
        c[0].groupPolicyId || c[0].id
      ));
    }
    r.ssid && r.ssid !== s && (r.passphrase = this._getPasswordForSelectedSsid(
      r.network,
      r.ssid
    ), r.passphrase || (r.passphrase = this._generateSecurePassword())), this._formData = r;
  }
  render() {
    var o, c, a;
    if (console.debug("Meraki Guest Access Card Render State:", {
      isLoading: this._isLoading,
      networks: this._networks.length,
      ssids: this._ssids.length,
      policies: this._policies.length,
      formData: this._formData
    }), this._isLoading)
      return Dt(
        ((o = this._config) == null ? void 0 : o.name) || "Meraki Guest Access",
        this._loadingMessage,
        "2.3.0-beta.3505"
      );
    if (this._networks.length === 0)
      return Je(
        "No Wireless Networks",
        "No Meraki wireless networks found. Ensure the integration is configured.",
        "2.3.0-beta.3505"
      );
    const t = L.getNetworkOptions(
      this._networks
    ), e = L.getSsidOptions(
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
      // Only show the policy dropdown if policies successfully loaded for this network
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
        <ha-card .header="${((c = this._config) == null ? void 0 : c.name) || "Share Access"}">
          <div class="card-content success-ui">
            <ha-alert alert-type="success">${this._success}</ha-alert>

            <div class="qr-container" .innerHTML="${this._qrSvg}"></div>

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
          <div class="version">v${"2.3.0-beta.3505"}</div>
        </ha-card>
      `;
    }
    return b`
      <ha-card .header="${((a = this._config) == null ? void 0 : a.name) || "Meraki Guest Access"}">
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
        <div class="version">v${"2.3.0-beta.3505"}</div>
      </ha-card>
    `;
  }
  _escapeWifi(t) {
    return t.replace(/([\\;,:])/g, "\\$1");
  }
  _resetForm() {
    this._success = null, this._error = null, this._qrSvg = "", this._loadCentralizedData();
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
          (l) => l.networkId === this._formData.network && l.number === e
        ), s = i ? i.name : "Guest WiFi", r = this._formData.passphrase, o = this._escapeWifi(s), c = this._escapeWifi(r), a = `WIFI:T:WPA;S:${o};P:${c};;`;
        this._qrSvg = await ot.toString(a, {
          type: "svg",
          margin: 1,
          color: {
            dark: "#000000",
            light: "#ffffff"
          }
        }), this._success = "Guest access key created successfully!";
      } catch (t) {
        this._error = `Failed to create guest key: ${t.message || t}`;
      } finally {
        this._creating = !1;
      }
    }
  }
};
ue.styles = [
  Bt,
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
      .flex {
        display: flex;
      }
      .justify-center {
        justify-content: center;
      }
      .p-8 {
        padding: 32px;
      }
      .success-ui {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 16px;
        padding-bottom: 16px;
      }
      .qr-container {
        background: white;
        padding: 16px;
        border-radius: 12px;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 200px;
        height: 200px;
        box-shadow: var(--ha-card-box-shadow, 0 2px 2px 0 rgba(0, 0, 0, 0.14));
      }
      .qr-container svg {
        width: 100%;
        height: 100%;
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
      .copyable-code {
        background: var(--card-background-color);
        padding: 4px 8px;
        border-radius: 4px;
        border: 1px solid var(--divider-color);
        font-family: var(--code-font-family, monospace);
        user-select: all;
      }
      ha-alert {
        width: 100%;
      }
    `
];
let k = ue;
T([
  H({ attribute: !1 })
], k.prototype, "hass");
T([
  v()
], k.prototype, "_config");
T([
  v()
], k.prototype, "_formData");
T([
  v()
], k.prototype, "_networks");
T([
  v()
], k.prototype, "_ssids");
T([
  v()
], k.prototype, "_policies");
T([
  v()
], k.prototype, "_creating");
T([
  v()
], k.prototype, "_error");
T([
  v()
], k.prototype, "_success");
T([
  v()
], k.prototype, "_qrSvg");
T([
  v()
], k.prototype, "_isLoading");
T([
  v()
], k.prototype, "_loadingMessage");
T([
  v()
], k.prototype, "_configEntryId");
customElements.get("meraki-guest-access-card") || customElements.define("meraki-guest-access-card", k);
window.customCards = window.customCards || [];
window.customCards.some(
  (n) => n.type === "meraki-guest-access-card"
) || window.customCards.push({
  type: "meraki-guest-access-card",
  name: "Meraki Guest Access",
  description: "Manage temporary guest WiFi access. Version: 2.3.0-beta.3505",
  preview: !0,
  version: "2.3.0-beta.3505"
});
export {
  k as MerakiGuestAccessCard
};
