function removePTagsInLiBlocks (element)
  if element.tag == "BulletList" or element.tag == "OrderedList" then
    -- Iterate through the list items
    for i, item in ipairs(element.content) do
      -- Recursively process the item
      element.content[i] = pandoc.walk_block(item, {
        Para = function (para)
          -- Check if the paragraph is within an <li> block
          if para.parent and para.parent.tag == "ListItem" then
            -- Replace the paragraph with its inline contents
            return pandoc.Span(para.content)
          end
        end
      })
    end
  end
  return element
end

return {
  { Block = removePTagsInLiBlocks }
}
