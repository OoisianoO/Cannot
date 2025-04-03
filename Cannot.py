import math

ac = 1140710
fw = 10
pw = 8888
bg = [10, 30, 60]
xz = [10, 30, 60, 100]
tq = [2.00, 2.03, 2.22, 2.33, 3.14, 3.14, 5.55, 5.55, 6.18, 8.88]

def lm(mv, qp):
    dk = 1 if qp < 5 else 10
    return (mv // dk) * dk

rb = { (0, 0, pw): (pw, 0, []) }

for nv in range(fw):
    zs = {}
    vh = bg if nv < 5 else xz
    
    for (yk, oj, cu), (dx, ea, if_) in list(rb.items()):
        if yk != nv or dx <= 0:
            continue
        for um in vh:
            ae = math.ceil(dx * um / 100)
            if ae > dx:
                ae = dx
            sj = tq[ea] if ea < len(tq) else tq[-1]
            ng = math.ceil(sj * ae)
            ba = dx + ng
            zn = ea + 1
            vx = if_ + [f"第{nv+1}輪贏{um}%"]
            mi = lm(ba, nv)
            wu = (nv+1, zn, mi)
            if wu not in zs or abs(zs[wu][0] - ac) > abs(ba - ac):
                zs[wu] = (ba, zn, vx)
            yj = dx - ae
            if yj <= 0:
                continue
            ks = if_ + [f"第{nv+1}輪輸{um}%"]
            tx = lm(yj, nv)
            lp = (nv+1, 0, tx)
            if lp not in zs or abs(zs[lp][0] - ac) > abs(yj - ac):
                zs[lp] = (yj, 0, ks)
    
    rb = zs
    gf = min(rb.values(), key=lambda jd: abs(jd[0]-ac))
    print(f"\r處理進度: {nv+1}/{fw} 輪, 最佳本金: {gf[0]:,}, 狀態數: {len(rb)}", end="")
we, nr, op = min(rb.values(), key=lambda uz: abs(uz[0]-ac))
print("\n===== 最佳結果 =====")
print("最終本金：", we)
print("與目標差距：", abs(we - ac))
print("最佳投注策略：")
for qf in op:
    print(qf)
