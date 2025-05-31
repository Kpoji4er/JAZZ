function MoveItem_RecieveNetArgs(data, except)
	local item, src_container, src_container_slot_name, dest_container, dest_container_slot_name, dest_x, dest_y, amount, merge_up_to_amount, exec_locally, src_x, src_y, item_at_dest, alternative_swap_pos, sync_unit, player_id, no_ui_respawn, multi_items  = unpack_params(data)
	local args = {}
	args.item = g_ItemIdToItem[item]	
	args.src_container = (except and except["src_container"])   and src_container   or GetContainerFromContainerNetId(src_container)
	args.dest_container = (except and except["dest_container"]) and dest_container or GetContainerFromContainerNetId(dest_container)
	args.src_container_slot_name = (except and except["src_container"]) and src_container_slot_name or GetContainerSlotFromContainerSlotNetId(args.src_container, src_container_slot_name)
	args.dest_container_slot_name = (except and except["dest_container"]) and dest_container_slot_name or GetContainerSlotFromContainerSlotNetId(args.dest_container, dest_container_slot_name)
	args.dest_x = dest_x
	args.dest_y = dest_y
	args.amount = amount
	args.merge_up_to_amount = merge_up_to_amount
	args.exec_locally = exec_locally
	args.s_src_x = src_x
	args.s_src_y = src_y
	args.s_sync_unit = (except and except["unit"]) and sync_unit or GetContainerFromContainerNetId(sync_unit)
	assert(not item_at_dest or g_ItemIdToItem[item_at_dest])
	args.s_item_at_dest = item_at_dest and g_ItemIdToItem[item_at_dest]
	args.s_player_id = player_id
	args.sync_call = true
	args.alternative_swap_pos = alternative_swap_pos
	args.no_ui_respawn = no_ui_respawn
	args.multi_items = multi_items
	return args
end