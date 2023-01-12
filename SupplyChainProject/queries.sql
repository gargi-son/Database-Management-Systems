/*
Name:Gargi Sunil Sontakke
Gno: G01334018
DB Project Part 2
*/

-- Query 1

create view shippedVSCustDemand as
	select c.customer as customer, c.item as item, sum(nvl(so.qty, 0)) as suppliedQty, c.qty as demandQty
		from customerDemand c left outer join shipOrders so on c.item = so.item and c.customer = so.recipient
		group by c.customer,c.item,c.qty
		order by c.customer, c.item
		;

-- Query 2

create view totalManufItems as
	select ManOrd.item as item, sum(ManOrd.qty) as totalManufQty
		from manufOrders ManOrd
		group by ManOrd.item
		order by ManOrd.item
		;

-- Query 3
create view matsUsedVsShipped as
	select Req.manuf, req.matItem, req.requiredQty, nvl(sum(ShOrd.qty),0) as shippedQty
	from(
		select ManOrd.manuf as manuf , BOM.matItem as matItem, sum( ManOrd.qty * BOM.QtyMatPerItem) as requiredQty
		from manufOrders ManOrd,billOfMaterials BOM
		where ManOrd.item = BOM.prodItem
		group by ManOrd.manuf, BOM.matItem) Req left outer join shipOrders ShOrd on Req.manuf = ShOrd.recipient and Req.matItem = ShOrd.item
		group by Req.manuf, req.matItem,req.requiredQty
		order by Req.manuf, req.matItem
		;

-- Query 4
create view producedVsShipped as
	select	ManOrd.item as item, ManOrd.manuf as manuf,nvl(sum(distinct ShipOrd.qty),0) as shippedOutQty, ManOrd.qty as  orderedQty
	from manufOrders ManOrd left outer join shipOrders ShipOrd on ManOrd.item = ShipOrd.item and ManOrd.manuf = ShipOrd.sender
	group by ManOrd.item, ManOrd.manuf, ManOrd.qty
	order by ManOrd.item, ManOrd.manuf
	;



-- Query 5
create view suppliedVsShipped as
	select	SupOrd.item as item, SupOrd.supplier as supplier, SupOrd.qty as suppliedQty, nvl(sum(distinct ShOrd.qty),0) as shippedQty
	from supplyOrders SupOrd left outer join shipOrders ShOrd on SupOrd.item = ShOrd.item and SupOrd.supplier = ShOrd.sender
	group by SupOrd.item, SupOrd.supplier, SupOrd.qty
	order by SupOrd.item, SupOrd.supplier
	;

-- Query 6
create view perSupplierCost as
	select SupDis.supplier,
	nvl((case

		when cal.totalcost>SupDis.amt2 then ((SupDis.amt1+(SupDis.amt2-SupDis.amt1)*(1-SupDis.disc1))+(cal.totalcost - SupDis.amt2)*(1-SupDis.disc2))
		when cal.totalcost>SupDis.amt1 and cal.totalcost<SupDis.amt2 then (SupDis.amt1+(cal.totalcost - SupDis.amt1)*(1-SupDis.disc1))
		when cal.totalcost<SupDis.amt1 then cal.totalcost
	end),0) as cost
	from (select SupOrd.supplier as supplier, sum(SupOrd.qty*SupUP.ppu) as totalcost
		from supplyOrders SupOrd, supplyUnitPricing SupUP
		where SupOrd.item = SupUP.item and SupOrd.supplier = SupUP.supplier
		group by SupOrd.supplier) cal right outer join supplierDiscounts SupDis on cal.supplier = SupDis.supplier
	order by SupDis.supplier
	;


-- Query 7
create view perManufCost as
	select ManDis.manuf,
	nvl((case

	when cal.totalcost > ManDis.amt1 then (ManDis.amt1+(cal.totalcost - ManDis.amt1)*(1-ManDis.disc1))
	when cal.totalcost < ManDis.amt1 then cal.totalcost
	end),0) as cost
	from (select ManOrd.manuf as manuf, sum(ManUP.setUpCost+(ManOrd.qty*ManUP.prodCostPerUnit)) as totalcost
		from manufOrders ManOrd, manufUnitPricing ManUP
		where ManOrd.item = ManUP.prodItem and ManOrd.manuf = ManUP.manuf
		group by ManOrd.manuf) cal right outer join manufDiscounts ManDis on cal.manuf = ManDis.manuf
	order by ManDis.manuf
	;



-- Query 8
create view perShipperCost as
	select sp.shipper,
	nvl(sum(greatest((case
	when temp.basecost<sp.amt1 then temp.basecost
	when temp.basecost>sp.amt2 then ((sp.amt1+(sp.amt2-sp.amt1)*(1-sp.disc1))+(temp.basecost - sp.amt2)*(1-sp.disc2))
	when temp.basecost>sp.amt1 and temp.basecost<sp.amt2 then (sp.amt1+(temp.basecost - sp.amt1)*(1-sp.disc1))
	end),sp.minPackagePrice)),0) as cost
	from (select so.shipper, be.shipLoc as fromloc, be1.shipLoc as toloc , sum(distinct so.qty*itm.unitWeight*shp.pricePerLb) as basecost
		from shipOrders so, busEntities be, busEntities be1, items itm, shippingPricing shp
		where so.sender = be.entity and so.recipient = be1.entity and so.item = itm.item and so.shipper = shp.shipper and be.shipLoc = shp.fromloc and be1.shipLoc = shp.toloc
		group by so.shipper, be.shipLoc, be1.shipLoc) temp right outer join shippingPricing sp on temp.shipper = sp.shipper and temp.fromloc = sp.fromloc and temp.toloc = sp.toloc
	group by sp.shipper
	order by sp.shipper
	;

-- Query 9
create view totalCostBreakDown as
	select SupCost.cost as supplyCost, ManCost.cost as manufCost,  ShipCost.cost as shippingCost, (SupCost.cost+ManCost.cost+ShipCost.cost) as totalCost
	from(
		select sum(perSupCost.cost) as cost from perSupplierCost perSupCost) SupCost,
			(select sum(perManCost.cost) as cost from  perManufCost perManCost) ManCost,
				(select sum(perShipCost.cost) as cost from perShipperCost perShipCost) ShipCost
	;

-- Query 10
create view customersWithUnsatisfiedDemand as
	select distinct cal.customer
	from(
		select CustDem.customer,CustDem.item, nvl(sum(distinct ShOrd.qty),0) as recieved
		from customerDemand CustDem left outer join shipOrders ShOrd on CustDem.customer = ShOrd.recipient and CustDem.item = ShOrd.item
		group by CustDem.customer,CustDem.item
		order by CustDem.customer) cal,customerDemand CD
		where CD.item = cal.item and CD.customer = cal.customer and CD.qty>cal.recieved
		order by cal.customer
	;


-- Query 11
create view suppliersWithUnsentOrders as
	select distinct Sup_Ord.supplier as supplier
	from(
		select SupOrd.supplier,SupOrd.item, nvl(sum(ShOrd.qty),0) as sent
		from supplyOrders SupOrd left outer join shipOrders ShOrd on SupOrd.supplier = ShOrd.sender and SupOrd.item = ShOrd.item
		group by SupOrd.supplier,SupOrd.item
		order by SupOrd.supplier) cal, supplyOrders Sup_Ord
		where  Sup_Ord.item = cal.item and Sup_Ord.supplier = cal.supplier and Sup_Ord.qty > cal.sent
	;



-- Query 12
create view manufsWoutEnoughMats as
	select distinct reqd.manuf
	from (
		select ManOrd1.manuf, BOM1.matitem, sum(distinct ManOrd1.qty * BOM1.QtyMatPerItem) as need
		from manufOrders ManOrd1, billOfMaterials BOM1
		where ManOrd1.item = BOM1.prodItem
		group by ManOrd1.manuf, BOM1.matitem) reqd,
			(select Temp.manuf, Temp.item, nvl(sum(distinct ShipOrd.qty),0) as supplied
			from
				(select ManOrd2.manuf, BOM2.matitem as item
					from manufOrders ManOrd2, billOfMaterials BOM2
					where ManOrd2.item = BOM2.prodItem
					) Temp left outer join shipOrders ShipOrd on Temp.Item = ShipOrd.item and ShipOrd.recipient = Temp.manuf
group by Temp.manuf, Temp.item) Got
where reqd.manuf = Got.manuf and reqd.matItem = Got.Item and reqd.need > Got.supplied
order by reqd.manuf
;

-- Query 13
create view manufsWithUnsentOrders as
	select distinct ManOrd2.manuf
	from(
		select ManOrd.manuf, ManOrd.item, nvl(sum(ShOrd.qty),0) as sent
		from manufOrders ManOrd left outer join shipOrders ShOrd on ManOrd.manuf = ShOrd.sender and ManOrd.item = ShOrd.item
		group by ManOrd.manuf,ManOrd.item
		order by ManOrd.manuf) cal, manufOrders ManOrd2
		where ManOrd2.manuf = cal.manuf and ManOrd2.item = cal.item and ManOrd2.qty > cal.sent
	;
