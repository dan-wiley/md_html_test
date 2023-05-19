function removePTagsInLiBlocks (element)
  if element.tag == "BulletList" or element.tag == "OrderedList" then
    -- Iterate through the list items
    for i, item in ipairs(element.content) do
      -- Check if the item contains a paragraph block
      if item.tag == "Plain" then
        -- Replace the paragraph block with its inline contents
        element.content[i] = pandoc.walk_inline(item, {
          Str = function (el)
            return el.content
          end,
          Space = function ()
            return {}
          end
        })
      end
    end
  end
  return element
end

return {
  { Inline = removePTagsInLiBlocks },
  { Block = removePTagsInLiBlocks }
}
