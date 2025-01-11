import { defineComponent as d, inject as x, computed as m, ref as y, onMounted as k, nextTick as T, onUnmounted as v, watch as s, openBlock as f, createElementBlock as B } from "vue";
import { Axis as r } from "@unovis/ts";
import { useForwardProps as F, arePropsEqual as g } from "../../utils/props.js";
import { axisAccessorKey as _ } from "../../utils/context.js";
const b = { "data-vis-axis": "" }, M = r.selectors, O = /* @__PURE__ */ d({
  __name: "index",
  props: {
    position: {},
    type: {},
    fullSize: { type: Boolean },
    label: {},
    labelFontSize: {},
    labelMargin: {},
    labelColor: {},
    gridLine: { type: Boolean },
    tickLine: { type: Boolean },
    domainLine: { type: Boolean },
    minMaxTicksOnly: { type: Boolean },
    minMaxTicksOnlyWhenWidthIsLess: {},
    tickFormat: { type: Function },
    tickValues: {},
    numTicks: {},
    tickTextFitMode: {},
    tickTextWidth: {},
    tickTextSeparator: {},
    tickTextForceWordBreak: { type: Boolean },
    tickTextTrimType: {},
    tickTextFontSize: {},
    tickTextAlign: {},
    tickTextColor: {},
    tickTextAngle: {},
    tickTextHideOverlapping: { type: Boolean },
    tickPadding: {},
    x: {},
    y: {},
    id: { type: Function },
    color: {},
    xScale: { type: [Object, Function] },
    yScale: { type: [Object, Function] },
    excludeFromDomainCalculation: { type: Boolean },
    duration: {},
    events: {},
    attributes: {},
    data: {}
  },
  setup(p, { expose: u }) {
    const o = x(_), a = p, n = m(() => o.data.value ?? a.data), i = F(a), t = y();
    return k(() => {
      T(() => {
        var e;
        t.value = new r(i.value), (e = t.value) == null || e.setData(n.value), o.update(t.value);
      });
    }), v(() => {
      var e;
      (e = t.value) == null || e.destroy(), o.destroy(a.type);
    }), s(i, (e, c) => {
      var l;
      g(e, c) || (l = t.value) == null || l.setConfig(i.value);
    }), s(n, () => {
      var e;
      (e = t.value) == null || e.setData(n.value);
    }), u({
      component: t
    }), (e, c) => (f(), B("div", b));
  }
});
export {
  M as VisAxisSelectors,
  O as default
};
//# sourceMappingURL=index.js.map
